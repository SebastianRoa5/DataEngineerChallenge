--DATABASE INITIALIZATION
CREATE DATABASE fire_incidents_db_dev;
\connect fire_incidents_db_dev;
CREATE SCHEMA raw;
CREATE SCHEMA refined;
CREATE SCHEMA curated;


-- USER AIRFLOW
CREATE user airflow WITH PASSWORD 'airflow';
GRANT ALL PRIVILEGES ON DATABASE fire_incidents_db_dev TO airflow;
GRANT ALL ON SCHEMA raw TO airflow;
GRANT ALL ON SCHEMA refined TO airflow;
GRANT ALL ON SCHEMA curated TO airflow;


-- USER DBT
CREATE user dbt WITH PASSWORD 'dbt';
GRANT ALL PRIVILEGES ON DATABASE fire_incidents_db_dev TO dbt;
GRANT ALL ON SCHEMA raw TO dbt;
GRANT ALL ON SCHEMA refined TO dbt;
GRANT ALL ON SCHEMA curated TO dbt;
