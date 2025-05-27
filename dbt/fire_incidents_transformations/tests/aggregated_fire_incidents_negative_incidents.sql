SELECT *
FROM {{ ref('aggregated_fire_incidents') }}
WHERE
    total_incidents < 0