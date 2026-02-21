use smart_watch_health;

SELECT * FROM health_data;

DESCRIBE health_data;

select distinct(stress_level)
from health_data
order by stress_level;

select min(heart_rate_BPM), max(heart_rate_BPM), min(blood_oxygen_level), max(blood_oxygen_level), min(step_count), max(step_count), min(sleep_duration_hr), max(sleep_duration_hr)
from health_data;