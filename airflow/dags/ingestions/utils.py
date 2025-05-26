import pandas as pd
from sodapy import Socrata
from airflow.providers.postgres.hooks.postgres import PostgresHook
from io import BytesIO
import tempfile
from datetime import datetime
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log



def get_fire_incidents(app_token,**context):
    client = Socrata(domain="data.sfgov.org",app_token=app_token)
    last_updated = context['ti'].xcom_pull(key='last_updated')
    logger.info(f"Last updated timestamp: {last_updated}")
    last_updated_format = last_updated.strftime('%Y-%m-%dT%H:%M:%S') if last_updated else None
    where_clause = f"data_loaded_at > '{last_updated_format}'" if last_updated else None
    logger.info(f"Where clause: {where_clause}")
    results = client.get("wr8u-xric",content_type='csv', limit=1000000, where=where_clause)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df.columns = results_df.iloc[0,:]
    results_df = results_df[1:]
    context['ti'].xcom_push(key='fire_incidents_df', value=results_df.to_json())

def insert_data(**context):
    first_load = context['ti'].xcom_pull(key='first_load', task_ids='decide_load')
    df_json = context['ti'].xcom_pull(key='fire_incidents_df')
    df = pd.read_json(df_json)
    df['created_at'] = datetime.utcnow()
    df['updated_at'] = datetime.utcnow()
    if df.empty:
        logger.info("No new data to insert.")
        return
    csv_buffer = BytesIO()  
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    # Insert rows into fire_incidents table
    if first_load:
        # Use COPY command for bulk loading
        # Write CSV to a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=True) as tmpfile:
            df.to_csv(tmpfile, index=False)
            tmpfile.flush()
            tmpfile.seek(0)
            tmpfile_path = tmpfile.name
            pg_hook.copy_expert(
                "COPY raw.fire_incidents FROM STDIN WITH CSV HEADER",
                tmpfile_path
            )
    else:
        # Insert rows one by one or update if exists
        # Assuming 'id' is the primary key
        df.replace('',None, inplace=True)  # Replace empty strings with None
        update_cols = [col for col in df.columns if col not in ['id', 'created_at', 'updated_at']]
        set_clause = ', '.join([f"{col}=EXCLUDED.{col}" for col in update_cols])
        set_clause += ", updated_at = (now() AT TIME ZONE 'utc')"
        for _, row in df.iterrows():
            pg_hook.run(
                f"INSERT INTO RAW.fire_incidents ({','.join(df.columns)}) VALUES ({','.join(['%s'] * len(df.columns))}) "
                f"ON CONFLICT(id) DO UPDATE SET {set_clause}",
                parameters=tuple(row)
            )

def decide_load(**context):
    # Pull the result from XCom (PostgresOperator returns a list of tuples)
    last_loaded = context['ti'].xcom_pull(task_ids='get_last_loaded')
    # last_loaded will be [[max_value]] or [[None]]
    last_loaded_value = last_loaded[0][0] if last_loaded and last_loaded[0] else None
    if last_loaded_value:
        context['ti'].xcom_push(key='last_updated', value=last_loaded_value)
        context['ti'].xcom_push(key='first_load', value=False)
        logger.info("Not first load, inserting by row.")
    else:
        context['ti'].xcom_push(key='last_updated', value=None)
        context['ti'].xcom_push(key='first_load', value=True)
        logger.info("First load, inserting by bulk.")