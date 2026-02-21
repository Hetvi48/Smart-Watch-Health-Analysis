use smart_watch_health;

CREATE TABLE activity_intensity_table AS
SELECT
    user_id,
    (step_count * heart_rate_BPM) AS activity_intensity
FROM health_data;

select * from activity_intensity_table;
select min(activity_intensity), max(activity_intensity) 
from activity_intensity_table;

CREATE TABLE stress_sleep_ratio_table AS
SELECT
    user_id,
    CASE
        WHEN sleep_duration_hr > 0
        THEN (stress_level / sleep_duration_hr)
        ELSE NULL
    END AS stress_sleep_ratio
FROM health_data;

select * from stress_sleep_ratio_table;
select min(stress_sleep_ratio), max(stress_sleep_ratio) 
from stress_sleep_ratio_table;

CREATE TABLE health_score_table AS
SELECT
    user_id,
    (
        (blood_oxygen_level / 100) * 0.4 +
        (sleep_duration_hr / 8) * 0.3 +
        (1 - stress_level / 10) * 0.3
    ) AS health_score
FROM health_data;

select * from health_score_table;
select min(health_score), max(health_score)
from health_score_table;

SELECT 
    h.*,
    a.activity_intensity,
    s.stress_sleep_ratio,
    hs.health_score

FROM health_data h

LEFT JOIN activity_intensity_table a
    ON h.user_id = a.user_id

LEFT JOIN stress_sleep_ratio_table s
    ON h.user_id = s.user_id

LEFT JOIN health_score_table hs
    ON h.user_id = hs.user_id;

-- -----------------------------------------------------------------
CREATE TEMPORARY TABLE temp_health_joined AS
SELECT 
    h.*,
    a.activity_intensity,
    s.stress_sleep_ratio,
    hs.health_score

FROM health_data h

LEFT JOIN activity_intensity_table a
    ON h.user_id = a.user_id

LEFT JOIN stress_sleep_ratio_table s
    ON h.user_id = s.user_id

LEFT JOIN health_score_table hs
    ON h.user_id = hs.user_id;
    
    
select * from temp_health_joined;

ALTER TABLE temp_health_joined
ADD COLUMN health VARCHAR(20);

UPDATE temp_health_joined
SET health =
    CASE
        WHEN health_score >= 0.85 THEN 'Excellent'
        WHEN health_score >= 0.70 THEN 'Good'
        WHEN health_score >= 0.50 THEN 'Moderate'
        ELSE 'Poor'
    END;
    
select * from temp_health_joined;

select count(health_score)
from temp_health_joined
where (health_score <= 0.50);

select count(health)
from temp_health_joined
where (health = 'Poor');

create table health_data_feature_added AS
select * from temp_health_joined;

ALTER TABLE health_data_feature_added
DROP COLUMN activity_intensity,
DROP COLUMN stress_sleep_ratio,
DROP COLUMN health_score;

select * from health_data_feature_added;