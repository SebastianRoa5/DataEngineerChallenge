from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos.constants import SourceRenderingBehavior
import os

airflow_home = os.environ["AIRFLOW_HOME"]
PROJECT_DIR = "dags/dbt/fire_incidents_transformations"

profile_config = ProfileConfig(
    profile_name="fire_incidents_transformations",
    target_name="dev",
    profiles_yml_filepath=f"{airflow_home}/{PROJECT_DIR}/profiles.yml"
    )

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        f"{airflow_home}/{PROJECT_DIR}",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{airflow_home}/dbt_venv/bin/dbt",
    ),
    render_config=RenderConfig(
        source_rendering_behavior=SourceRenderingBehavior.WITH_TESTS_OR_FRESHNESS,
    ),
    dag_id="dbt_fire_incidents_transformations",
)