CREATE DATABASE Smart_watch_Health;
use Smart_watch_Health;

select * from health_data;

DESCRIBE health_data;

ALTER TABLE health_data
CHANGE `User ID` user_id text;

SELECT `Heart Rate (BPM)`
FROM health_data
WHERE `Heart Rate (BPM)` IS NULL
   OR `Heart Rate (BPM)` = '';
   
UPDATE health_data
SET `Heart Rate (BPM)` = 0.0
WHERE `Heart Rate (BPM)` = ''
;

ALTER TABLE health_data
CHANGE `Heart Rate (BPM)` heart_rate_BPM DECIMAL(4,1);

SELECT `Blood Oxygen Level (%)`
FROM health_data
WHERE `Blood Oxygen Level (%)` IS NULL
   OR `Blood Oxygen Level (%)` = ''
;

ALTER TABLE health_data
CHANGE `Blood Oxygen Level (%)` blood_oxygen_level DECIMAL(4,1);

SELECT `Step Count`
FROM health_data
WHERE `Step Count` IS NULL
	OR `Step Count` = '';

select max(`Step Count`)
from health_data;

ALTER TABLE health_data
CHANGE `Step Count` step_count DECIMAL(6,1);

select `Sleep Duration (hours)`
from health_data
WHERE `Sleep Duration (hours)` IS NULL
	OR `Sleep Duration (hours)` = 'ERROR'
    OR `Sleep Duration (hours)` = ''
;

UPDATE health_data
SET `Sleep Duration (hours)` = 0.0
WHERE `Sleep Duration (hours)` = 'ERROR'
	OR `Sleep Duration (hours)` = ''
;

SELECT min(`Sleep Duration (hours)`)
from health_data;

ALTER TABLE health_data
CHANGE `Sleep Duration (hours)` sleep_duration_hr DECIMAL(3,1);

select min(sleep_duration_hr)
from health_data;

select DISTINCT(`Activity Level`)
from health_data;

select count(`Activity level`)
from health_data
where `Activity Level` = 'nan';

UPDATE health_data
SET `Activity Level` = 'Active'
WHERE `Activity Level` = 'Actve';

UPDATE health_data
SET `Activity Level` = 'Sedentary'
WHERE `Activity Level` = 'Seddentary';

UPDATE health_data
SET `Activity Level` = 'Highly_Active'
WHERE `Activity Level` = 'Highly Active';

SELECT DISTINCT(`Activity Level`), COUNT(`Activity Level`)
from health_data
GROUP BY `Activity Level`;

UPDATE health_data
SET `Activity Level` = 'Sedentary'
WHERE `Activity Level` = 'nan'
;

ALTER TABLE health_data
CHANGE `Activity Level` activity_level varchar(100);

SELECT `Stress Level`
from health_data
order by `Stress Level`;

-- CREATE TEMPORARY TABLE user_id
-- select user_id,
-- ROW_NUMBER() OVER(partition by user_id) as row_num
-- from health_data;

-- select * from user_id;

CREATE TABLE health_data_backup AS
SELECT * FROM health_data;

UPDATE health_data
SET user_id = NULL
WHERE user_id = 0
	OR user_id = '';
    
CREATE TEMPORARY TABLE tmp_user_ids
SELECT
    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS new_user_id,
    user_id
FROM health_data;
-- (SELECT NULL) means “don’t care about order”

UPDATE health_data h
JOIN tmp_user_ids t
ON h.user_id <=> t.user_id
SET h.user_id = t.new_user_id;
-- error - lost connection to server

SET @i := 0;

UPDATE health_data
SET user_id = (@i := @i + 1)
ORDER BY user_id;

ALTER TABLE health_data
MODIFY user_id INT NOT NULL,
ADD PRIMARY KEY (user_id);

SELECT MIN(user_id), MAX(user_id), COUNT(*)
FROM health_data;

ALTER TABLE health_data
CHANGE `Stress Level` stress_level INT;

select * from health_data;

CREATE TABLE health_data_backup_2 AS
SELECT * FROM health_data;

