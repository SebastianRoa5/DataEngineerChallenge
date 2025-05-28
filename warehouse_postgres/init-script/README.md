# Warehouse Postgres Init-Script

This folder contains SQL scripts and other files necessary for initializing and administering the Postgres data warehouse for the DataEngineerChallenge project.

## Usage

- All `.sql` files in this directory will be automatically executed when the Postgres container is first started (via Docker Compose).
- Use this folder to add:
  - Table creation scripts
  - Seed data
  - Schema migrations
  - Any other warehouse administration queries

## Notes

- Scripts are executed in alphanumeric order.
- Make sure your SQL files are idempotent if you plan to restart the container multiple times.