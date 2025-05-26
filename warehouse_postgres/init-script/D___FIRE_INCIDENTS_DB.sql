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


-- RAW DATA TABLES
CREATE TABLE IF NOT EXISTS raw.fire_incidents (
    incident_number TEXT,
    exposure_number INTEGER,
    id TEXT PRIMARY KEY,
    address TEXT,
    incident_date TIMESTAMP,
    call_number TEXT,
    alarm_dttm TIMESTAMP,
    arrival_dttm TIMESTAMP,
    close_dttm TIMESTAMP,
    city TEXT,
    zipcode TEXT,
    battalion TEXT,
    station_area TEXT,
    box TEXT,
    suppression_units INTEGER,
    suppression_personnel INTEGER,
    ems_units INTEGER,
    ems_personnel INTEGER,
    other_units INTEGER,
    other_personnel INTEGER,
    first_unit_on_scene TEXT,
    estimated_property_loss NUMERIC,
    estimated_contents_loss NUMERIC,
    fire_fatalities INTEGER,
    fire_injuries INTEGER,
    civilian_fatalities INTEGER,
    civilian_injuries INTEGER,
    number_of_alarms INTEGER,
    primary_situation TEXT,
    mutual_aid TEXT,
    action_taken_primary TEXT,
    action_taken_secondary TEXT,
    action_taken_other TEXT,
    detector_alerted_occupants TEXT,
    property_use TEXT,
    area_of_fire_origin TEXT,
    ignition_cause TEXT,
    ignition_factor_primary TEXT,
    ignition_factor_secondary TEXT,
    heat_source TEXT,
    item_first_ignited TEXT,
    human_factors_associated_with_ignition TEXT,
    structure_type TEXT,
    structure_status TEXT,
    floor_of_fire_origin TEXT,
    fire_spread TEXT,
    no_flame_spread TEXT,
    number_of_floors_with_minimum_damage INTEGER,
    number_of_floors_with_significant_damage INTEGER,
    number_of_floors_with_heavy_damage INTEGER,
    number_of_floors_with_extreme_damage INTEGER,
    detectors_present TEXT,
    detector_type TEXT,
    detector_operation TEXT,
    detector_effectiveness TEXT,
    detector_failure_reason TEXT,
    automatic_extinguishing_system_present TEXT,
    automatic_extinguishing_sytem_type TEXT,
    automatic_extinguishing_sytem_perfomance TEXT,
    automatic_extinguishing_sytem_failure_reason TEXT,
    number_of_sprinkler_heads_operating INTEGER,
    supervisor_district INTEGER,
    neighborhood_district TEXT,
    point TEXT,
    data_as_of TIMESTAMP,
    data_loaded_at TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT (now() AT TIME ZONE 'utc')
);

-- Grant all privileges on the raw.fire_incidents table to airflow and dbt users
GRANT ALL PRIVILEGES ON TABLE raw.fire_incidents TO airflow;
GRANT ALL PRIVILEGES ON TABLE raw.fire_incidents TO dbt;