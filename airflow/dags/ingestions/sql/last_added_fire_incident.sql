SELECT MAX(data_loaded_at)
FROM {{ params.schema_name }}.{{ params.table_name }};