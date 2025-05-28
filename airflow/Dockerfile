FROM python:3.9 AS base

RUN apt update && apt install -y make ssh curl && \
    pip install --upgrade pip
# Copy All files from the current directory to /project/airflow
COPY ./airflow /project/airflow
# Set files from dbt
#COPY ../dbt/fire_incidents_transformations /project/airflow/dags/dbt/fire_incidents_transformations
# Set the working directory
WORKDIR /project/airflow
# Build the project
ARG AIRFLOW_VERSION=2.8.3
ARG PYTHON_VERSION=3.9
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# Download constraints file and install Airflow with constraints
RUN pip install "apache-airflow[postgres]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
RUN pip install --no-cache-dir -r requirements.txt

ENV AIRFLOW_HOME=/project/airflow

FROM base AS dev
CMD ["airflow", "standalone"]