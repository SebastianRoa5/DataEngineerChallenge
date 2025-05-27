
SELECT
    DATE_TRUNC('month', incident_date) AS month,
    supervisor_district,
    neighborhood_district,
    battalion,
    COUNT(*) AS total_incidents,
    SUM(estimated_property_loss) AS total_property_loss,
    SUM(fire_fatalities) AS total_fire_fatalities
FROM
   {{ ref('fire_incidents_stg') }}
GROUP BY
    month,
    supervisor_district,
    neighborhood_district,
    battalion
ORDER BY
    month DESC,
    supervisor_district,
    battalion