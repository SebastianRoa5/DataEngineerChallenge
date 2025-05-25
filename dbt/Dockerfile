FROM python:3.9

# Install latest libpq and PostgreSQL client
RUN apt-get update && apt-get install -y libpq-dev postgresql-client

COPY ./dbt/requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV POSTGRES_DATABASE=fire_incidents_db_dev
ENV POSTGRES_HOST=host.docker.internal
ENV POSTGRES_PASSWORD=dbt
ENV POSTGRES_PORT=5432
ENV POSTGRES_SCHEMA=refined
ENV POSTGRES_USER=dbt

RUN mkdir /root/.dbt
COPY ./dbt/fire_incidents_transformations/profiles.yml /root/.dbt/profiles.yml


COPY ./airflow/dags dags
COPY ./dbt/fire_incidents_transformations/ dags/dbt/fire_incidents_transformations
COPY ./dbt/fire_incidents_transformations/dbt_project.yml dags/dbt/fire_incidents_transformations/dbt_project.yml

WORKDIR /dags/dbt/fire_incidents_transformations