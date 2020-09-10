\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.freebuf.com\](https://www.freebuf.com/column/227843.html)

在发生网页篡改、服务器被植入挖矿木马等安全攻击事件时，日志能协助进行安全事件还原，能尽快找到事件发生的时间、原因等，所以日志收集还是很重要的。本文整理了部分常见中间件、数据库、操作系统的日志收集方法。

一、中间件日志
-------

### 1.1 weblogic

weblogic 在安装结束后默认开启了日志记录功能，默认配置情况下，weblogic 会有 3 种日志，分别是 accesslog, Server log 和 domain log，WebLogic8.x 和 9 及以后的版本目录结构有所不同。

WebLogic 9 及以后版本：

access log 在 $MW\_HOME\\user\_projects\\domains\\\\servers\\\\logs\\access.log

server log 在 $MW\_HOME\\user\_projects\\domains\\\\servers\\\\logs\\.log

domain log 在 $MW\_HOME\\user\_projects\\domains\\\\servers\\\\logs\\.log

WebLogic 8.x 版本：

access log 路径如下：$MW\_HOME\\user\_projects\\domains\\\\\\access.log

server log 路径如下：$MW\_HOME\\user\_projects\\domains\\\\\\.log

domain log 路径如下： $MW\_HOME\\user\_projects\\domains\\\\.log

其中:

$MW\_HOME 是 WebLogic 的安装目录

是域的实际名称，是在创建域的时候指定的

是 Server 的实际名称，是在创建 Server 的时候指定的

是 Admin Server 的实际名称，是在创建 Admin Server 的时候指定的。

**access.log**

主要记录 http 请求，默认情况下日志记录处于启用状态，服务器将 http 请求保存在单独的日志文件中，日志格式如下，主要记录了 http 请求请求 ip 地址、请求时间、访问页面、响应状态等信息：

![](https://image.3001.net/images/20200220/1582191873_5e4e55013842c.png!small)**server log**

主要用于服务器的一般日志记录，比如 weblogic 的启动、关闭、部署应用等相关记录，日志格式：依次为时间戳，严重程度，子系统，计算机名，服务器名，线程 ID。其后消息正文中的行仅表示记录的一次例外并显示该例外的堆栈跟踪式如下：![](https://image.3001.net/images/20200220/1582191883_5e4e550b00a92.png!small)**domain log**

主要记录了一个 domain 的运行情况，一个 domain 中的各个 weblogic server 可以把它们的一些信息（如：严重错误）发送到 AdminServer 上，AdminServer 把这些信息传递到 domain.log 上![](https://image.3001.net/images/20200220/1582191892_5e4e551418656.png!small)

### 1.2 tomcat

tomcat 日志默认路径：在安装目录下的 logs 文件夹下：![](https://image.3001.net/images/20200220/1582191903_5e4e551f9ffea.png!small)

如果在安装中默认修改了日志存储位置，可在 conf/logging.properties 文件中查看![](https://image.3001.net/images/20200220/1582191911_5e4e5527aad83.png!small)

tomcat 日志一般分为 catalina.out、localhost、manager、localhost\_access\_log4 种格式日志。

**catalina.out**

运行中的日志，主要记录运行中产生的一些信息，尤其是一些异常错误日志信息，内容如下：![](https://image.3001.net/images/20200220/1582191921_5e4e55316e10c.png!small)

**catalina.Y-M-D.log**

是 tomcat 自己运行的一些日志，这些日志还会输出到 catalina.out，

但是应用向 console 输出的日志不会输出到 catalina.{yyyy-MM-dd}.log![](https://image.3001.net/images/20200220/1582191935_5e4e553fa77df.png!small)

**localhost.Y-M-D.log**

程序异常没有被捕获的时候抛出的地方，

Tomcat 下内部代码丢出的日志（jsp 页面内部错误的异常，org.apache.jasper.runtime.HttpJspBase.service 类丢出的，日志信息就在该文件！）

应用初始化 (listener,filter, servlet) 未处理的异常最后被 tomcat 捕获而输出的日志，而这些未处理异常最终会导致应用无法启动。![](https://image.3001.net/images/20200220/1582191950_5e4e554e99cd7.png!small)

**manager.Y-M-D.log**

管理日志![](https://image.3001.net/images/20200220/1582191957_5e4e5555817a9.png!small)

**localhost\_access\_log**

主要记录访问日志信息，记录访问的的时间、ip 地址等信息，也是应急中经常用到的日志信息![](https://image.3001.net/images/20200220/1582191966_5e4e555e1926f.png%21small)

此部分日志可通过查看 server.xml 文件的如下内容，来确定是否启用了访问日志记录![](https://image.3001.net/images/20200220/1582191995_5e4e557bf043a.png!small)

### 1.3apache

apache 日志一般分为 access\_log 和 error\_log 两种，通过查看 httpd.conf 文件查看 apache 日志路径：

grep -i"CustomLog" /etc/httpd/conf/httpd.conf![](https://image.3001.net/images/20200220/1582192008_5e4e5588e3912.png!small)

grep -i"ErrorLog" /etc/httpd/conf/httpd.conf![](https://image.3001.net/images/20200220/1582192017_5e4e55910fd29.png!small)

**access\_log**

访问日志, 记录所有对 apache 服务器进行请求的访问![](https://image.3001.net/images/20200220/1582192026_5e4e559a03fe4.png!small)

**error\_log**

错误日志, 记录下任何错误的处理请求，通常服务器出现什么错误，可对该日志进行查看![](https://image.3001.net/images/20200220/1582192032_5e4e55a03caca.png!small)

### 1.4nginx

nginx 的日志主要分为 access.log、error.log 两种，可通过查看 nginx.conf 文件来查找相关日志路径，如下图

![](https://image.3001.net/images/20200220/1582192038_5e4e55a6e2eb9.png!small)![](https://image.3001.net/images/20200220/1582192047_5e4e55afa749f.png!small)

**access.log**

主要记录访问日志，记录访问客户端 ip 地址、访问时间、访问页面等信息![](https://image.3001.net/images/20200220/1582192056_5e4e55b8a055a.png!small)

error.log, 主要记录一些错误信息。

### 1.5 iis

查看日志文件位置：![](https://image.3001.net/images/20200220/1582192064_5e4e55c059c13.png!small)

打开文件夹下其中一个名为 ex170910.log，日志内容具体如下，包括访问域名时间、ip、访问 url 等信息。![](https://image.3001.net/images/20200220/1582192071_5e4e55c79a1d1.png!small)

二、数据库日志
-------

本次主要介绍关于 mysql、sqlserver、oracle 的一些日志信息。

### 2.1 mysql：

status：查看当前数据库状态![](https://image.3001.net/images/20200220/1582192082_5e4e55d2271f1.png!small)

mysql 的日志主要分为以下几种：

ErrorLog：记录 Mysql 运行过程中的 Error、Warning、Note 等信息，系统出错或者某条记录出问题可以查看 Error 日志；

GenaralQuery Log：记录 mysql 的日常日志，包括查询、修改、更新等的每条 sql；

Binary Log ：二进制日志，包含一些事件，这些事件描述了数据库的改动，如建表、数据改动等，主要用于备份恢复、回滚操作等；

Slow QueryLog\*：记录 Mysql 慢查询的日志；

showvariables like 'log\_%'; ![](https://image.3001.net/images/20200220/1582192089_5e4e55d97c761.png!small)

可见 mysql 默认只是开启了错误日志，错误日志内容如下：![](https://image.3001.net/images/20200220/1582192097_5e4e55e1d6965.png!small)

此处重点分析 GenaralQuery Log，也是应急中经常会查看到的，其他日志类型可查看大牛已经整理好的详细笔记，链接如下：[https://www.jianshu.com/p/db19a1d384bc](https://www.jianshu.com/p/db19a1d384bc)

通过开启日志，来记录所有查询和执行的 sql 语句：

GLOBAL general\_log='ON'；

SHOWVARIABLES LIKE 'general%';![](https://image.3001.net/images/20200220/1582192106_5e4e55ea152cb.png!small)

general\_log：日志功能是否开启，默认关闭 OFF

general\_log\_file：日志文件保存位置

到对应路径下查看日志内容如下，会记录当前针对数据库所做的所有操作![](https://image.3001.net/images/20200220/1582192113_5e4e55f153689.png!small)

### 2.2 sqlserver：

SQL Server 日志记录了完整的 SQL Server 数据库运行的状态信息，并以消息的形式记录系统级、应用级操作。

可以使用 SQL Server Management Studio 中的日志文件查看器来访问有关在以下日志中捕获的错误和事件的信息：

SQL Server Management Studio 连接 sqlserver 数据库，查看与常规 SQL Server 活动相关的日志。

1.  在对象资源管理器中，展开 **“\*\*** 管理”\*\* 。
    
2.  执行下列任一操作：
    

1\. 右键单击 “SQL Server 日志”，指向 “查看” ，然后单击 “SQL Server 日志” 或 “SQLServer 和 Windows 日志” 。

2\. 展开 “SQL Server 日志” ，右键单击任何日志文件，然后单击 “查看 SQL Server 日志” 。 还可以双击任何日志文件，日志格式如下：![](https://image.3001.net/images/20200220/1582192123_5e4e55fb463c0.png!small)

查询最近一次启动 sqlserver 时间：

select sqlserver\_start\_time fromsys.dm\_os\_sys\_info;![](https://image.3001.net/images/20200220/1582192129_5e4e56017c4e0.png!small)

历史 sql 记录查询：SQLServer 并没有这样的实现，只有 sys.dm\_exec\_query\_stats 缓存了一部分 (sql server 服务开启后执行的语句，某些不被缓存执行计划的语句并不记录)。

这个视图主要是对执行计划的统计，包含消耗成本，运行次数等等，并没有 session，user，每次被执行的时间等信息：

启动 sql server 审计功能，会记录所有的操作记录，可以通过查看 Audits 来查看日志的存储路径![](https://image.3001.net/images/20200220/1582192138_5e4e560a4ac1e.png!small)

Sqlserver 开启日志审计功能可参考：[https://blog.51cto.com/gaowenlong/1908381](https://blog.51cto.com/gaowenlong/1908381)

### 2.3 oracle：

Oracle 日志文件分为两种：重做日志文件（redo log file）、归档日志文件，其中重做日志文件主要记录了数据库的操作过程，可以在进行数据库恢复时，将重做日志文件在还原的数据库上进行执行，以达到数据库的最新状态。

Oracle 数据库默认只是对数据库的登录情况记录，但是不对数据库的查询记录统计，可通过 show parameter audit，查看审计功能是否开启，若 audit\_sys\_operations 值为 DB。![](https://image.3001.net/images/20200220/1582192145_5e4e5611e8866.png!small)

None：是默认值，不做审计；

DB：将 audit trail 记录在数据库的审计相关表中，如 aud$，审计的结果只有连接信息；

audit\_file\_dest 为存放的日志路径，可查看 adump 下相关文件，内容如下：![](https://image.3001.net/images/20200220/1582192152_5e4e56188c3b2.png!small)

DB,Extended：这样审计结果里面除了连接信息还包含了当时执行的具体语句；

OS：将 audit trail 记录在操作系统文件中，文件名由 audit\_file\_dest 参数指定；

开启审计功能：

alter system set audit\_sys\_operations=TRUEscope=spfile;

alter system set audit\_trail=db,extendedscope=spfile;

重启实例即可![](https://image.3001.net/images/20200220/1582192160_5e4e56200f95f.png!small)

开启后会把审计内容记录到 sys 库的 AUD$ 表中![](https://image.3001.net/images/20200220/1582192165_5e4e5625b6769.png!small)

修改将日志文件记录在操作系统中:alter system set audit\_trail='OS'scope=spfile;![](https://image.3001.net/images/20200220/1582192171_5e4e562bd6b12.png!small)

Audit\_file\_dest 即为日志保存的具体路径。

关于日志的详细配置可以参考：[http://blog.itpub.net/31397003/viewspace-2145164/](http://blog.itpub.net/31397003/viewspace-2145164/)

三、操作系统日志
--------

### 3.1 windows 日志

查看 windows 日志方法：开始 -> 运行 -> 输入 eventvwr ![](https://image.3001.net/images/20200220/1582192180_5e4e563408f09.png!small)

<table><colgroup><col width="24.914383561643834%"><col width="25%"><col width="25.085616438356162%"><col width="25.17123287671233%"></colgroup><thead><tr><th>类型</th><th>事件类型</th><th>描述</th><th>文件名</th></tr></thead><tbody><tr><td>Windows 日志</td><td>系统</td><td>系统日志包含 Windows 系统组件记录的事件。例如，在启动过程中加载驱动程序或其他系统组件失败将记录在系统日志中。系统组件所记录的事件类型由 Windows 预先确定。</td><td>%SystemRoot%\System32\Winevt\Logs\System.evtx</td></tr><tr><td>安全</td><td>安全日志包含诸如有效和无效的登录尝试等事件，以及与资源使用相关的事件，如创建、打开或删除文件或其他对象。管理员可以指定在安全日志中记录什么事件。例如，如果已启用登录审核，则对系统的登录尝试将记录在安全日志中。</td><td>%SystemRoot%\System32\Winevt\Logs\Security.evtx</td></tr><tr><td>应用程序</td><td>应用程序日志包含由应用程序或程序记录的事件。例如，数据库程序可在应用程序日志中记录文件错误。程序开发人员决定记录哪些事件。</td><td>%SystemRoot%\System32\Winevt\Logs\Application.evtx</td></tr><tr><td>转发事件</td><td>ForwardedEvents 日志用于存储从远程计算机收集的事件。若要从远程计算机收集事件，必须创建事件订阅。</td><td>%SystemRoot%\System32\Winevt\Logs\ForwardedEvents.evtx</td></tr></tbody></table>

可通过查看帮助手册进一步获取日志信息：![](https://image.3001.net/images/20200220/1582192192_5e4e564041da6.png!small)

Windows 的日志以事件 id 来标识具体发生的动作行为，可通过微软查询具体 id 对应的操作：

![](https://image.3001.net/images/20200220/1582192203_5e4e564b9cfc4.png!small)

也可访问如下网站查看：![](https://image.3001.net/images/20200220/1582192213_5e4e56553a880.png!small)

之前也已经有大牛写过关于 windows 日志查看内容，可参考如下链接：

[https://www.freebuf.com/vuls/175560.html](https://www.freebuf.com/vuls/175560.html)

### 3.2 linux 日志

通过查看 /etc/rsyslog.conf ，可查看相关系统日志配置情况。![](https://image.3001.net/images/20200220/1582192220_5e4e565c8e3e1.png!small)

linux 系统日志一般存放在 / var/log / 目录下。![](https://image.3001.net/images/20200220/1582192228_5e4e5664acbd5.png!small)

/var/log/messages：记录 Linux 内核消息及各种应用程序的公共日志信息，包括启动、IO 错误、网络错误、程序故障等。对于未使用独立日志文件的应用程序或服务，一般都可以从该文件获得相关的事件记录信息。

/var/log/cron：记录 crond 计划任务产生的事件消息。

/varlog/dmesg：记录 Linux 系统在引导过程中的各种事件信息。

/var/log/maillog：记录进入或发出系统的电子邮件活动。

/var/log/lastlog：最近几次成功登录事件和最后一次不成功登录事件。

/var/log/rpmpkgs：记录系统中安装各 rpm 包列表信息。

/var/log/secure：记录用户登录认证过程中的事件信息。

/var/log/wtmp：记录每个用户登录、注销及系统启动和停机事件。

/var/log/utmp：记录当前登录的每个用户的详细信息

**secure**

是应急中最常用的文件，主要记录系统存取数据的文件，如 POP3、ssh、telnet、ftp 等相关记录，从日志中可看出系统服务是否遭受到安全威胁，从如下日志中可看到 ftp 服务一直在被破解。![](https://image.3001.net/images/20200220/1582192237_5e4e566d4dd63.png!small)

**用户日志**

wtmp 日志记录了用户的登录、退出、重启等情况，可以查看系统是否存在异常用户登录，判断攻击者是否已经登录服务器，由于 wtmp 日志为二进制文件，所以利用用 last 命令查看，last -t 20190426120950 , 可查看这个时间之前的日志。![](https://image.3001.net/images/20200220/1582192244_5e4e5674a3288.png!small)

utmp 日志记录当前用户的一些信息，由于 utmp 日志文件同样为二进制文件，可通过 w、who 命令查看![](https://image.3001.net/images/20200220/1582192251_5e4e567b491c3.png!small)

lastlog 命令，用于显示系统中所有用户最近一次登录信息。lastlog 文件在每次有用户登录时被查询。可以使用 lastlog 命令检查某特定用户上次登录的时间，并格式化输出上次登录日志 / var/log/lastlog 的内容。它根据 UID 排序显示登录名、端口号（tty）和上次登录时间。如果一个用户从未登录过，lastlog 显示 Never logged。注意需要以 root 身份运行该命令。

简单整理了在应急中如何查找常见中间件、数据库、操作系统的日志，从而能方便我们快速进行溯源，当然仅限于在日志开启的情况下。