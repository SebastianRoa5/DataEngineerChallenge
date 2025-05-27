from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from pendulum import datetime

from cosmos.operators.docker import DbtRunDockerOperator,DbtRunOperationDockerOperator, DbtSeedDockerOperator

# PATH within the Docker container for the DBT project
PROJECT_DIR = "dags/dbt/fire_incidents_transformations"

DBT_IMAGE = "challenge-dbt:latest"

PROJECT_SEEDS = ["raw_customers", "raw_payments", "raw_orders"]
with DAG(
    dag_id="dbt_test",
    start_date=datetime(2022, 11, 27),
    schedule=None,
    catchup=False,
) as dag:

    pre_dbt_workflow = EmptyOperator(task_id="pre_dbt_workflow")

    run = DbtRunDockerOperator(
                task_id="run_test",
                project_dir=PROJECT_DIR,
                schema="refined",
                conn_id="postgres_default",
                image=DBT_IMAGE,
                network_mode="challenge_default",
            )

    post_dbt_workflow = EmptyOperator(task_id="post_dbt_workflow")

    pre_dbt_workflow >> run >> post_dbt_workflow

