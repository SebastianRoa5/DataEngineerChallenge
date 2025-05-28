# DataEngineerChallenge

This repository provides a comprehensive, containerized data engineering solution for the DataEngineerChallenge. It includes orchestration with Apache Airflow, data transformation with dbt, and a Postgres data warehouse. The project is optimized for local development and testing using Docker Compose, ensuring easy setup and reproducibility. For a detailed guide on using the model—including ingestion, transformation, and orchestration processes—please refer to the `Report.md` file.

---

## Project Structure

- **airflow/**: Contains DAGs, configuration, and a Dockerfile for Airflow orchestration.
- **dbt/**: Contains the dbt project, models, and a Dockerfile for dbt transformations.
- **warehouse_postgres/init-script/**: Contains SQL scripts for initializing the Postgres data warehouse.
- **fire_incidents_exploration.ipynb**: Jupyter notebook with initial data exploration.

---

## Quick Start

### 1. Build and Start All Services

To build and start the entire stack (Airflow, dbt, and Postgres warehouse), simply run:

```sh
docker-compose up --build
```

- This will build images for each system: Airflow, dbt, and the warehouse.
- The Postgres database is used for development purposes.
- The dbt service will be built but not started automatically; Airflow will trigger dbt jobs as needed using the built dbt image.

### 2. Cleaning the Project

To remove cache, logs, and other unnecessary files that may cause errors, use:

```sh
make clean
```

This will clean up all subprojects using their respective Makefiles.

---

## Development Notes

- **DBT & Airflow Integration:**  
  This project uses the [Cosmos](https://github.com/astronomer/astronomer-cosmos) library to seamlessly integrate dbt with Airflow. Cosmos allows you to orchestrate and monitor dbt runs as native Airflow tasks, making it easy to manage your data transformations within your DAGs.
- **Environment Variables**:  
  Use a `.env` file to set environment variables as needed. Default values are provided in the `docker-compose.yml` for development convenience.
- **.gitignore**:  
  Make sure to use `.gitignore` to avoid committing sensitive or unnecessary files.
- **Standalone Development**:  
  You can run Airflow or dbt locally outside Docker if you wish, but the Airflow DAGs are configured to expect the dbt container/image for transformations.
- **Initial Data Exploration**:  
  See `fire_incidents_exploration.ipynb` for an initial analysis of the source data used in this challenge.

---

## Additional Tips

- All SQL scripts in `warehouse_postgres/init-script/` are executed automatically when the Postgres container starts. Ensure scripts are idempotent.
- Airflow and dbt have their own README files with detailed local setup instructions if you want to develop or test them outside Docker.
- The system is designed for easy local development, but can be adapted for production with appropriate changes to environment variables, secrets management, and resource scaling.

---
```
