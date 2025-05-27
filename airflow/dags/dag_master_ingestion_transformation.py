from airflow import DAG
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator

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
        task_id="trigger_fire_incidents_ingestion",
        trigger_dag_id="fire_incidents_ingestion",
        wait_for_completion=True,
        execution_date='{{ ds }}',
        reset_dag_run=True,
        poke_interval=10,
    )
    
    # Trigger the transformation DAG
    trigger_transformation = TriggerDagRunOperator(
        task_id="trigger_dbt_fire_incidents_transformation",
        trigger_dag_id="dbt_fire_incidents_transformations",
        wait_for_completion=True,
        execution_date='{{ ds }}',
        reset_dag_run=True,
        poke_interval=10,
    )
    
    end = DummyOperator(task_id="end")
    
    # Set the execution flow
    start >> trigger_ingestion >> trigger_transformation >> end