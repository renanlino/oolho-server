SELECT
  extract(year from m.occurrence_date) as year,
  extract(month from m.occurrence_date) as month,
  extract(day from m.occurrence_date) as day,
  extract(hour from m.occurrence_date) as hour,
  --extract(minute from m.occurrence_date) as minute,
  direction,
  count(m.id)

FROM app_movement m

WHERE
  DATE(occurrence_date)::text >= '2017-10-15'
  AND DATE(occurrence_date)::text <= '2017-10-15'

GROUP BY 1, 2, 3, 4, 5

LIMIT 100
