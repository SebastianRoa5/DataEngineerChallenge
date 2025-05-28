# DBT Local Setup

This folder contains the DBT project and configuration for the DataEngineerChallenge.

## Local Development Setup (without Docker)

1. **Create a Python virtual environment (Python 3.9 recommended):**
   ```sh
   python3.9 -m venv env
   ```

2. **Activate your virtual environment:**
   ```sh
   source env/bin/activate
   ```

3. **Verify Python path (optional):**
   ```sh
   which python
   env/bin/python
   ```

4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   Make sure your `requirements.txt` includes `dbt-core` and the appropriate adapter (e.g., `dbt-postgres`).

5. **Initialize DBT (if not already initialized):**
   ```sh
   dbt init
   ```
   This will set up the necessary DBT project files.

6. **Configure your DBT profile:**
   - Edit the `profiles.yml` file to set your database connection details (host, user, password, etc.).

7. **Run DBT commands:**
   - Run models:
     ```sh
     dbt run
     ```
   - Run tests:
     ```sh
     dbt test
     ```
   - Check source freshness:
     ```sh
     dbt source freshness
     ```

---

## Using Docker

- The `Dockerfile` in this folder can be used to build a DBT image.
- To run DBT in a container, use the `docker-compose.yml` in the project root directory.
- Example:
  ```sh
  cd ../..
  docker-compose run dbt bash
  ```
  This will start a shell in the DBT container where you can run DBT commands as above.

---

## Notes

- Place your DBT models in the `models/` directory.
- Make sure your database is accessible from your local machine or Docker container.
- For troubleshooting, check your `profiles.yml` and database connectivity.
- Use make clean for cleaning unnecesary files in the project.
