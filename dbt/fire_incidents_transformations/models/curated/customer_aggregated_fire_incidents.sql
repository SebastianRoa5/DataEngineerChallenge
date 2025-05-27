{{ config(schema='curated') }}
SELECT
    *
FROM
   {{ ref('aggregated_fire_incidents') }}
WHERE
    neighborhood_district not in ('Treasure Island')