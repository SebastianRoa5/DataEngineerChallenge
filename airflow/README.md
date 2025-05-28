# Airflow Local Setup

This folder contains the Airflow DAGs and configuration for the DataEngineerChallenge project. The airflow is build in standalone mode for dev purposes.

## Local Development Setup (without Docker)

1. **Set the `AIRFLOW_HOME` environment variable:**

   ```sh
   export AIRFLOW_HOME=$(pwd)
   ```

   (Run this command inside the `DataEngineerChallenge/airflow` directory.)

2. **Create and activate a Python virtual environment (try using python 3.9 as this project is built with it):**

   ```sh
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```



6. **Initialize and Start Airflow services:**


   ```sh
   airflow standalone
   ```

   The Airflow UI will be available at [http://localhost:8080](http://localhost:8080).

---

## Cleaning Up

To remove logs, database files, and cache, run:

```sh
make clean
```

---

## Using Docker

- The `Dockerfile` in this folder is used to build the Airflow image.
- To run Airflow with Docker Compose, use the `docker-compose.yml` in the project root directory.
- Example:

  ```sh
  cd ../..
  docker-compose up --build
  ```

  This will build the Airflow image and start all required services (Airflow, Postgres, etc.) in containers.

---

## Notes

- Place your DAGs in the `dags/` subfolder.
- Environment variables and connections can be set in the `.env` file or via the Airflow UI.
- If you encounter issues with missing dependencies or database connections, check your environment variables and Docker Compose configuration.

---