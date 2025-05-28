import pandas as pd
from sodapy import Socrata
from airflow.providers.postgres.hooks.postgres import PostgresHook
import tempfile
from datetime import datetime
from airflow.utils.log.logging_mixin import LoggingMixin
import great_expectations as gx
from great_expectations.core.expectation_suite import (
    ExpectationSuite
)
from airflow.exceptions import AirflowSkipException
from airflow.utils.state import State
from airflow.models import DagRun
import os
import json


logger = LoggingMixin().log

def get_fire_incidents(app_token, key_csv_path, **context):
    """
    Fetch fire incidents data from the Socrata API and save it to a temporary CSV file.
    This function is designed to be used in an Airflow DAG.
    """
    client = Socrata(domain="data.sfgov.org", app_token=app_token)
    last_updated = context['ti'].xcom_pull(key='last_updated')
    logger.info(f"Last updated timestamp: {last_updated}")
    last_updated_format = last_updated.strftime('%Y-%m-%dT%H:%M:%S') if last_updated else None
    where_clause = f"data_loaded_at > '{last_updated_format}'" if last_updated else None
    logger.info(f"Where clause: {where_clause}")
    results = client.get("wr8u-xric", content_type='csv', limit=1000000, where=where_clause)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df.columns = results_df.iloc[0, :]
    results_df = results_df[1:]
    results_df['created_at'] = datetime.utcnow()
    results_df['updated_at'] = datetime.utcnow()
    # Save DataFrame to a temporary CSV file for testing purposes, for more serious with AWS, should be S3
    if not results_df.empty:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
            results_df.to_csv(tmpfile.name, index=False)
            tmpfile_path = tmpfile.name
        context['ti'].xcom_push(key=key_csv_path, value=tmpfile_path)
        logger.info(f"Saved fire incidents to temporary file: {tmpfile_path}")
    else:
        logger.info("No new fire incidents data to process.")
        context['ti'].xcom_push(key=key_csv_path, value=None)
        raise AirflowSkipException("No new data to insert or file not found.")


def insert_csv_raw_data(table,key_csv_path,**context):
    """
    Insert or update data from a CSV file into the raw table in PostgreSQL
    """
    first_load = context['ti'].xcom_pull(key='first_load', task_ids='decide_load')
    csv_path = context['ti'].xcom_pull(key=key_csv_path)
    if not csv_path or not os.path.exists(csv_path):
        logger.info("No new data to insert or file not found.")
        raise AirflowSkipException("No new data to insert or file not found.")
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    if first_load:
        # Use COPY command for bulk loading
        pg_hook.copy_expert(
            f"COPY raw.{table} FROM STDIN WITH CSV HEADER",
            csv_path
        )
    else:
        # Insert rows one by one or update if exists
        df = pd.read_csv(csv_path)
        # Replace NaN and 'NaN' strings with None
        df = df.replace({pd.NA: None, 'NaN': None, float('nan'): None})
        df.replace('', None, inplace=True)
        update_cols = [col for col in df.columns if col not in ['id', 'created_at', 'updated_at']]
        set_clause = ', '.join([f"{col}=EXCLUDED.{col}" for col in update_cols])
        set_clause += ", updated_at = (now() AT TIME ZONE 'utc')"
        for _, row in df.iterrows():
            pg_hook.run(
                f"INSERT INTO RAW.{table} ({','.join(df.columns)}) VALUES ({','.join(['%s'] * len(df.columns))}) "
                f"ON CONFLICT(id) DO UPDATE SET {set_clause}",
                parameters=tuple(row)
            )
    # Optionally, clean up the temp file
    os.remove(csv_path)

def decide_load(**context):
    """
    Decide whether to perform a first load or incremental load based on the last loaded timestamp
    """
    last_loaded = context['ti'].xcom_pull(task_ids='get_last_loaded')
    last_loaded_value = last_loaded[0][0] if last_loaded and last_loaded[0] else None
    if last_loaded_value:
        context['ti'].xcom_push(key='last_updated', value=last_loaded_value)
        context['ti'].xcom_push(key='first_load', value=False)
        logger.info("Not first load, inserting by row.")
    else:
        context['ti'].xcom_push(key='last_updated', value=None)
        context['ti'].xcom_push(key='first_load', value=True)
        logger.info("First load, inserting by bulk.")


def validate_csv_data(key_csv_path,expectation_suite_path,**context):
    """
    Validate the CSV data against a Great Expectations Expectation Suite
    """
    csv_path = context['ti'].xcom_pull(key=key_csv_path)
    context = gx.get_context()
    validator = context.sources.pandas_default.read_csv(csv_path)
    # Define the Expectation to test:
    with open(expectation_suite_path, 'r') as f:
        expectation_suite = json.load(f)
    expectation = ExpectationSuite(**expectation_suite)
    # Test the Expectation:
    validation_results = validator.validate(expectation)
    logger.info(f"Validation results: {validation_results}")


def check_upstream_skips(dag_id,**context):
    """
    Check if any tasks in the upstream DAG were skipped
    Returns True if we should trigger the downstream DAG, False to skip
    """
    dag_runs = DagRun.find(dag_id=dag_id, external_trigger=True)
    dag_runs.sort(key=lambda x: x.execution_date, reverse=True)
    upstream_dag_run = dag_runs[0] if dag_runs else None
   
    if not upstream_dag_run:
        return True  # no previous run, proceed with trigger
    
    skipped_tasks = [
        ti for ti in upstream_dag_run.get_task_instances()
        if ti.state == State.SKIPPED
    ]
    
    if skipped_tasks:
        context['ti'].log.info(
            f"Skipping downstream DAG trigger because these tasks were skipped: "
            f"{[t.task_id for t in skipped_tasks]}"
        )
        raise AirflowSkipException(
            "Upstream tasks were skipped, skipping downstream DAG trigger."
        )
