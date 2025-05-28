{{ config(materialized='view')}}
--SELECT distinct on (id) *
--FROM {{ source('raw', 'fire_incidents') }}

{{ dbt_utils.deduplicate(
    relation=source('raw', 'fire_incidents'),
    partition_by="id",
    order_by="updated_at desc",
   )
}}