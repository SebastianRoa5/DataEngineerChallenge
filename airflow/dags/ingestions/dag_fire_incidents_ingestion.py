from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
from ingestions.utils import get_fire_incidents, insert_data, decide_load

API_TOKEN= Variable.get("FIRE_INCIDENTS_API_TOKEN")

with DAG(
    dag_id="fire_incidents_ingestion",
    catchup=False,
    tags=["ingestion"],
) as dag:
    get_last_loaded = PostgresOperator(
        task_id='get_last_loaded',
        postgres_conn_id='postgres_default',
        sql="last_added_fire_incident.sql",
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
        },
        provide_context=True,
    )

    insert_task = PythonOperator(
        task_id='insert_fire_incidents',
        python_callable=insert_data,
        # first_load will be pulled from XCom in the function
        provide_context=True,
    )

    get_last_loaded >> decide_load_task >> fetch_task >> insert_task