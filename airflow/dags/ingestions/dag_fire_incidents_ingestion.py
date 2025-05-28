from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
from utils.utils import get_fire_incidents, insert_csv_raw_data, decide_load, validate_csv_data
import os

API_TOKEN= Variable.get("FIRE_INCIDENTS_API_TOKEN")
expectation_suite_path = os.path.join(os.environ["AIRFLOW_HOME"], "dags", "ingestions", "expectations", "expectation_raw_fire_incidents.json")


with DAG(
    dag_id="fire_incidents_ingestion",
    catchup=False,
    tags=["ingestion"],
    schedule=None
) as dag:
    
    begin = DummyOperator(
        task_id='begin'
        )

    get_last_loaded = PostgresOperator(
        task_id='get_last_loaded',
        postgres_conn_id='postgres_default',
        sql="sql/last_added_fire_incident.sql",
        params={ "schema_name": "raw", "table_name": "fire_incidents"}
    )

    decide_load_task = PythonOperator(
        task_id='decide_load',
        python_callable=decide_load,
        provide_context=True,
    )

    fetch_task = PythonOperator(
        task_id='fetch_fire_incidents',
        python_callable=get_fire_incidents,
        op_kwargs={
            "app_token": API_TOKEN,
            "key_csv_path": "fire_incidents_csv_path"
        },
        provide_context=True,
    )

    validation_task = PythonOperator(
        task_id='validate_fire_incidents_batch',
        python_callable= validate_csv_data,
        op_kwargs={
            "key_csv_path": "fire_incidents_csv_path",
            "expectation_suite_path": expectation_suite_path
        },
        provide_context=True,
    )

    insert_task = PythonOperator(
        task_id='insert_fire_incidents',
        python_callable=insert_csv_raw_data,
        op_kwargs={
            "table": "fire_incidents",
            "key_csv_path": "fire_incidents_csv_path"
        },
        provide_context=True,
    )

    end = DummyOperator(
        task_id='end'

    )

    begin >> get_last_loaded >> decide_load_task >> fetch_task >> validation_task >> insert_task >> end
    