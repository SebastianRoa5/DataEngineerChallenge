from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig, ExecutionMode
from cosmos.constants import SourceRenderingBehavior
import os

airflow_home = os.environ["AIRFLOW_HOME"]
PROJECT_DIR = "dags/dbt/fire_incidents_transformations"
DBT_IMAGE = "challenge-dbt:latest"
NETWORK = "challenge_default"

env = {
    "DBT_HOST": os.environ.get("DBT_HOST", "postgres"),
    "DBT_PORT": int(os.environ.get("DBT_PORT", "5432")),
    "DBT_USER": os.environ.get("DBT_USER", "dbt"),
    "DBT_PASS": os.environ.get("DBT_PASS", "dbt"),
    "DBT_DBNAME": os.environ.get("DBT_DBNAME", "fire_incidents_db_dev"),
    "DBT_SCHEMA": os.environ.get("DBT_SCHEMA", "refined"),
}

profile_config = ProfileConfig(
    profile_name="fire_incidents_transformations",
    target_name="dev",
    profiles_yml_filepath=f"{airflow_home}/{PROJECT_DIR}/profiles.yml"
    )

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig( 
        execution_mode=ExecutionMode.DOCKER,
        dbt_project_path=PROJECT_DIR,  
        dbt_executable_path=f"{airflow_home}/dbt_venv/bin/dbt"
    ),
    operator_args={
        "image": DBT_IMAGE,
        "network_mode": "challenge_default",
        "auto_remove": "force",
        "environment": env,     
    },
    render_config=RenderConfig(
        dbt_project_path=PROJECT_DIR,
        source_rendering_behavior=SourceRenderingBehavior.WITH_TESTS_OR_FRESHNESS
    ),
    dag_id="dbt_fire_incidents_transformations",
    tags= ["transformations"]
)