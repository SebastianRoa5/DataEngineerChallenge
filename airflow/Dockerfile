FROM python:3.9-slim AS base

RUN apt update && apt install -y make ssh curl && \
    pip install --upgrade pip
# Copy All files from the current directory to /project/airflow
COPY ./airflow /project/airflow
# Set files from dbt
#COPY ../dbt/fire_incidents_transformations /project/airflow/dags/dbt/fire_incidents_transformations
# Set the working directory
WORKDIR /project/airflow
# Build the project
RUN pip install --no-cache-dir -r requirements.txt

ENV AIRFLOW_HOME=/project/airflow

FROM base AS dev
CMD ["airflow", "standalone"]