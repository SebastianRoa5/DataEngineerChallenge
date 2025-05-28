from airflow import DAG
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from utils.utils import check_upstream_skips

# This DAG orchestrates the ingestion and transformation of fire incidents data


with DAG(
    "master_ingestion_transformations_fire_incidents",
    schedule_interval="@daily",
    start_date=datetime(2025, 5, 25),
    catchup=False,
    tags=["master"],
) as master_dag:
    
    start = DummyOperator(task_id="start")
    
    # Trigger the ingestion DAG
    trigger_ingestion = TriggerDagRunOperator(
        task_id="trigger_dag_fire_incidents_ingestion",
        trigger_dag_id="fire_incidents_ingestion",
        wait_for_completion=True,
        reset_dag_run=True,
        poke_interval=10,
    )

    # Conditional trigger
    trigger_or_skip = PythonOperator(
        task_id='check_upstream_skips_no_data',
        python_callable=check_upstream_skips,
        op_kwargs={
            "dag_id": "fire_incidents_ingestion",
        },
        provide_context=True,
    )
    
    # Trigger the transformation DAG
    trigger_transformation = TriggerDagRunOperator(
        task_id="trigger_dag_dbt_fire_incidents_transformation",
        trigger_dag_id="dbt_fire_incidents_transformations",
        wait_for_completion=True,
        reset_dag_run=True,
        poke_interval=10,
    )
    
    end = DummyOperator(task_id="end")
    
    # Set the execution flow
    start >> trigger_ingestion >> trigger_or_skip >> trigger_transformation >> end