> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247483811&idx=1&sn=43b38306f244b415f5b58b85d1c95a46&chksm=eaad819eddda0888ce7286b3e2f447e74861fa356fd7f02f4d89a5630effd6bc19b28bedb78b&scene=21#wechat_redirect)

  

CobaltStrike 的使用

  

**目录**

*   CobaltStrike
    
*   CobaltStrike 的安装
    
*   CobaltStrike 的使用
    
*   创建监听器：
    
*   创建 Attacks：
    
*   视图 View：
    
*   对被控主机的操作
    
*   抓取 hash 和 dump 明文密码
    
*   提权 (Elevate)
    
*   利用被控主机建立 Socks4 代理
    
*   进程列表 (注入进程，键盘监控)
    
*   生成黄金票据注入当前会话 (Golden Ticket)
    
*   凭证转换 (Make Token)
    

![](https://mmbiz.qpic.cn/mmbiz_gif/ldFaBNSkvHjHB7C85hnZBxEdY7XfdialFSs2sqkhU0hAQGG4vDn1nDOdXUGDicfaJ1rTeQDPNJRciaedicADLANghw/640)

01

CobaltStrike

**CobaltStrike** 是一款渗透测试神器，被业界人称为 CS 神器。CobaltStrike 分为客户端与服务端，服务端是一个，客户端可以有多个，可被团队进行分布式协团操作。

CobaltStrike 集成了端口转发、服务扫描，自动化溢出，多模式端口监听，windows exe 木马生成，windows dll 木马生成，java 木马生成，office 宏病毒生成，木马捆绑。钓鱼攻击包括：站点克隆，目标信息获取，java 执行，浏览器自动攻击等等强大的功能！

02

CobaltStrike 的安装

我这里以 Kali 安装为例：

先去下载 jdk 版本

```
上传到Kali中，解压：tar -xzvf jdk-8u191-linux-x64.tar.gz
移动到opt目录下：mv jdk1.8.0_191/ /opt/
进入jdk目录：cd  /opt/jdk1.8.0_191
 
执行 vim  ~/.bashrc ， 并添加下列内容
# install JAVA JDK
export JAVA_HOME=/opt/jdk1.8.0_191
export CLASSPATH=.:${JAVA_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
保存退出
执行: source ~/.bashrc
 
执行：
update-alternatives --install /usr/bin/java java /opt/jdk1.8.0_191/bin/java 1
update-alternatives --install /usr/bin/javac javac /opt/jdk1.8.0_191/bin/javac 1
update-alternatives --set java /opt/jdk1.8.0_191/bin/java
update-alternatives --set javac /opt/jdk1.8.0_191/bin/javac
 
查看结果：
update-alternatives --config java
update-alternatives --config javac
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0noaUVr4PIMwtdjkSD71mXoBDDRI8oHMjf4SwwyeQwqBzRvfljxnxfw/640?wx_fmt=png)

安装好了 java 之后，我们就去安装 CobaltStrike 了！

```
上传到Kali中，解压：unzip cobaltstrike-linux.zip
进入cobalstrike中：cd cobaltstrike-linux/
```

**启动服务端：**

```
启动服务端：./teamserver   192.168.10.11  123456    #192.168.10.11是kali的ip地址，123456是密码
后台运行，关闭当前终端依然运行：nohup  ./teamserver   192.168.10.11  123456  &
```

  这里 CobaltStrike 默认监听的是 50050 端口，如果我们想修改这个默认端口的话，可以打开 teamserver 文件，将其中的 50050 修改成任意一个端口号

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0tSBicSWMibFcrjH4srKZMO13ZicsTpqibITgAaDpIkl9HWotwwMnlcHmsA/640?wx_fmt=png)**

**启动客户端：**

```
./cobaltstrike
```

这里 host 填 kali 的 ip，密码就是刚刚我们启动的密码。

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0cP2tBpl48pQSyYP0mOPuO6HvxKedibwHFAsQXxJR4FLJK3UzpyQDic1A/640?wx_fmt=png)**

**启动后的客户端：**

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0AEqL2YOq6gY85XVvxI0Z5pSjRhqIzN0fmhLsZDDrib1L0Wlr5rzKTbw/640?wx_fmt=png)**

我们也可以打开 windows 下的 cobaltstrike 客户端，然后把 ip 设置为我们的启动时候的 ip 即可。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0l1NLR4zPrucqNOkibqVeBdiaWLicprsKPkweAR7Qn90icsQ0NGU73Q6nNQ/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/ldFaBNSkvHjHB7C85hnZBxEdY7XfdialFSs2sqkhU0hAQGG4vDn1nDOdXUGDicfaJ1rTeQDPNJRciaedicADLANghw/640)

03

CobaltStrike 的使用

**创建监听器：**

点击左上方 CobaltStrike 选项——> 在下拉框中选择 Listeners ——> 在下方弹出区域中单机 add

```
name：为监听器名字，可任意
payload：payload类型
Host: shell反弹的主机，也就是我们kali的ip
Port: 反弹端口
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0V4B8ljQ9uicEMqicaDxkZC6FG7u5Cxw1liaHiaTjFAstIBiaU9hOAEO2CBQ/640?wx_fmt=png)

这里 Payload 有 9 种选项，如下：

**内部的 Listener**

*   windows/beacon_dns/reverse_dns_txt
    
*   windows/beacon_dns/reverse_http
    
*   windows/beacon_http/reverse_http
    
*   windows/beacon_https/reverse_https 
    
*   windows/beacon_smb/bind_pipe
    

**外部的 Listener**

*   windows/foreign/reverse_dns_txt
    
*   windows/foreign/reverse_http
    
*   windows/foreign/reverse_https
    
*   windows/foreign/reverse_tcp
    
    Beacon 为内置的 Listener，即在目标主机执行相应的 payload，获取 shell 到 CS 上；其中包含 DNS、HTTP、HTTPS、SMB。Beacon 可以选择通过 DNS 还是 HTTP 协议出口网络，你甚至可以在使用 Beacon 通讯过程中切换 HTTP 和 DNS。其支持多主机连接，部署好 Beacon 后提交一个要连回的域名或主机的列表，Beacon 将通过这些主机轮询。目标网络的防护团队必须拦截所有的列表中的主机才可中断和其网络的通讯。通过种种方式获取 shell 以后（比如直接运行生成的 exe），就可以使用 Beacon 了。
    
    Foreign 为外部结合的 Listener，常用于 MSF 的结合，例如获取 meterpreter 到 MSF 上。
    
    不同的 beacon 支持的系统位数也不同，如下：
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0tJfdia8fkGnZeEkiaEiaNjiayZdSO4doossCPxrqvx4WOqTGwcXlBs2OCg/640?wx_fmt=png)
    

 **创建 Attacks：**

 **点击中间的 Attacks——>Packages**

 **![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0tg9Z3KqaT9P1QWD9uvOoIunumg4WzNGtd7BA5cj0ic2H5fza1h2ENzg/640?wx_fmt=png)** 

  这里 Attacks 有几种，如下：

*   HTML Application 　　　　　　 生成一个基于 powershell 的恶意 HTML Application 木马，后缀格式为 .hta
    
*   MS Office Macro 　　　　　　   生成 office 宏病毒文件；
    
*   Payload Generator 　　　　　   生成各种语言版本的 payload;
    
*   USB/CD AutoPlay 　　　　　　 生成利用自动播放运行的木马文件；
    
*   Windows Dropper 　　　　　　 捆绑器，能够对文档类进行捆绑；
    
*   Windows Executable 　　　　　生成可执行 exe 木马；
    
*   Windows Executable(S)　　　　生成无状态的可执行 exe 木马
    

 **点击中间的 Attacks——>Web Drive-by（网站钓鱼攻击）**

 **![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0Emz4icSbLDW32DIMeNUWLLUj8FYib4QWiaHQ8vSsLWqZicUpt32qS9agiaA/640?wx_fmt=png)** 

*   Manage　　　　　　　　　　 对开启的 web 服务进行管理；
    
*   Clone Site 　　 　　　　　　  克隆网站，可以记录受害者提交的数据；
    
*   Host File 　　　　　　　　　  提供一个文件下载，可以修改 Mime 信息；Host File 可以配合 DNS 欺骗实现挂马效果使用
    
*   Scripted Web Delivery              类似于 msf 的 web_delivery ;
    
*   Signed Applet Attack 　　       启动一个 Web 服务以提供自签名 Java Applet 的运行环境;
    
*   Smart Applet Attack 　　　　  自动检测 Java 版本并 l 利用已知的 exploits 绕过 security；
    
*   System Profiler　　　　　　   用来获取一些系统信息，比如系统版本，Flash 版本，浏览器版本等。
    
*   Spear Phish 　　　　　　　   用来邮件钓鱼的模块
    

###   视图 View：

  点击中间的 View

  ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0DcWj1Z5N8ibh326elHiaTdAxnX2YCGKW7xuVOhAEEGiaIPCFalP0tSf4A/640?wx_fmt=png)

*   Applications　　　　显示受害者机器的应用信息；
    
*   Credentials　　　　 显示受害者机器的凭证信息，能更方便的进行后续渗透；
    
*   Downloads 　　　　文件下载；
    
*   Event Log　　　　   可以看到事件日志，清楚的看到系统的事件, 并且团队可以在这里聊天;
    
*   Keystrokes　　　　 查看键盘记录；
    
*   Proxy Pivots　　　  查看代理信息；
    
*   Screenshots　　　  查看屏幕截图；
    
*   Script Console　　   在这里可以加载各种脚本以增强功能，脚本地址：https://github.com/rsmudge/cortana-scripts
    
*   Targets　　　　　   查看目标；
    
*   Web Log　　　　　 查看 web 日志。
    
*   Reporting　　　　  主要就是出报告用的
    

  

![](https://mmbiz.qpic.cn/mmbiz_gif/ldFaBNSkvHjHB7C85hnZBxEdY7XfdialFSs2sqkhU0hAQGG4vDn1nDOdXUGDicfaJ1rTeQDPNJRciaedicADLANghw/640)

04

对被控主机的操作

```
Interact       打开beacon
Access 
  dump hashes   获取hash
  Elevate       提权
  Golden Ticket 生成黄金票据注入当前会话
  MAke token    凭证转换
  Run Mimikatz  运行 Mimikatz 
  Spawn As      用其他用户生成Cobalt Strike的beacon
Explore
  Browser Pivot 劫持目标浏览器进程
  Desktop(VNC)  桌面交互
  File Browser  文件浏览器
  Net View      命令Net View
  Port scan     端口扫描
  Process list  进程列表
  Screenshot    截图
Pivoting
  SOCKS Server 代理服务
  Listener     反向端口转发
  Deploy VPN   部署VPN
Spawn            新的通讯模式并生成会话
Session          会话管理，删除，心跳时间，退出，备注
```

抓取 hash 和 dump 明文密码  

这两项功能都需要管理员或 System 权限

抓取密码哈希：右键被控主机——>Access——>Dump Hashes

   利用 mimikatz 抓取明文密码：右键被控主机——>Access——>Run Mimikatz

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI00KUJqkCiaaia1vEEk5sjyDyzWiaorl0RY69icicG4oh09Bw4g0ricWLvT2qQ/640?wx_fmt=png)

默认有三个提权 payload 可以使用，分别是 MS14-058、uac-dll、uac-token-duplication 。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0GIEwGyBYLPic08AYbwYvSumXmH3RMMOGpvkrVrtcX8WF7J00D3uToaQ/640?wx_fmt=png)

我们选中 MS14-058，点击 Launch

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0ItTe1O6EBtMLFs9OjaMlazU3U3rvMHdGNXHFicOvtcWHXfEdgZoaR4g/640?wx_fmt=png)

之后就弹回来一个 system 权限的 beacon

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI01XAo6VibSOhHMHlswg0ibickpDVAUj1yoGnpyCavhXIPr5R77icDRyt7xw/640?wx_fmt=png)

我们也可以自己加入一些提权脚本进去。在 Github 上有一个提权工具包，使用这个提权工具包可以增加几种提权方法：https://github.com/rsmudge/ElevateKit    。我们下载好该提权工具包后

如下：

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0kZfiaNQa5t8MicQzQVUVicgRLTIcTUibwyvllqINHicC2jiaFWYgUCgCZLOg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0JZIa3NoG604icW4eErgdml6lYnficXhac5bToQV1Xj4ic9ibtMwbL6QgTw/640?wx_fmt=png)

再打开我们的提权，可以看到多了几种提权方式了

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0zw7N4NwCKdicp21BqMBChSiahMsM2BzLoDXZ6TmOSdTa1hTx1Iwxiap1A/640?wx_fmt=png)

利用被控主机建立 Socks4 代理

当我们控制的主机是一台位于公网和内网边界的服务器 ，我们想利用该主机继续对内网进行渗透，于是，我们可以利用 CS 建立 socks4A 代理

右键被控主机——>Pivoting——>SOCKS Server

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0dBXc4z8SF4SKYPYoW4GsicwyicyCgmHSKMC6LeaTwq1fsjOaup81WBFg/640?wx_fmt=png)

这里是 SOCKS 代理运行的端口，任意输入一个未占用的端口即可，默认 CS 会给出一个，我们直接点击 Launch 即可

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0iaCgyE5agXsQcvPLbSafyuHeomL3bs55qxq3YG1vg5dyzOOQfws8p6A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0M1ianANZLHPHlDaD3fRmjibx91SaiaD67oQNMnHt8DEBzXmkXXdrPt5Yg/640?wx_fmt=png)

于是，我们在自己的主机上设置 Socks4 代理。代理 ip 是我们 CS 服务端的 ip，端口即是 38588。

如果我们想查看整个 CS 代理的设置，可以点击 View——>Proxy Pivots 

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0LjvibwAsIZUU7T5Libt6RlLpicNZ0G8HxaKE1zU8sfgFNb1wgVB2Nx3dg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0SRjsAGA7dic0Fiap7nV9a2F05jgHLicT84fsTv09e1oOYd22q4NMZVgVg/640?wx_fmt=png)

进程列表 (注入进程，键盘监控)

右键被控主机——>Explore——>Process List

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI04bsSv5OmNS9Yaticibib10ibsA6smfiazXqA8k77H5sUH08oicxBdFNriaG9A/640?wx_fmt=png)

即可列出进程列表

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0jUoN2x8pObAgTPNW2dysZW2iayA6H45IPWoIkKvFwcTNQntPyzaC3CA/640?wx_fmt=png)

选中该进程，Kill 为杀死该进程，Refresh 为刷新该进程，Inject 则是把 beacon 注入进程，Log Keystrokes 为键盘记录，Screenshot 为截图，Stea Token 为窃取运行指定程序的用户令牌

这里着重讲一下注入进程和键盘记录

**Inject 注入进程**

选择进程，点击 Inject，随后选择监听器，点击 choose，即可发现 CobaltStrike 弹回了目标机的一个新会话，这个会话就是成功注入到某进程的 beacon 会话。该功能可以把你的 beacon 会话注入到另外一个程序之中，注入之后，除非那个正常进程被杀死了，否则我们就一直可以控制该主机了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0Rp6BXuHU2ETLD5OsetoFXbuhiceu7VxAW9CHroUSQia3nyCzNh3bxqBg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0kF9ClPUo7Pu0WOU4oCl3LibUxY7wnRRB4APib8WKibIXvicJYaRgxXVEgw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0pNWicuy8QGd3onTozIaKaDH08louWvxM4T6PvaqibEsCRP7nZkRyicuRw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0MhwZFOoNoCibPnwtffeOpGZwFSDbQqnURl6MEqicb8djcpZ8C4cd4lKg/640?wx_fmt=png)

**键盘记录**

任意选择一个进程，点击 Log Keystrokes，即可监听该主机的键盘记录

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0onSrdCjGib1yw8Kv6qZiapgn85wSaib1W5YkLOo1gVcCkGLsRhribymfTg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0hfkJNrQv1HDGaAiatAkOQicAaDMclqOSuyhV8xtYlmvks1ia5D55lQpjw/640?wx_fmt=png)

查看键盘记录结果：点击钥匙一样的按钮，就可以在底下看到键盘记录的详细了，会监听所有的键盘记录，而不只是选中的进程的键盘记录

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0wQ9zmkkwHN7lwLibvibNX9AeV0niaibvulVFX2ySMA4UcxCpMM6LPDwdiaQ/640?wx_fmt=png)

键盘监听记录，也可以直接输入 **keylogger**

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0eHo2QFEcBvIVY3tcvlEoszib9SKaNAwK8uZVaaJRb0d865CZodz1BIg/640?wx_fmt=png)**

待更新**生成黄金票据注入当前会话 (Golden Ticket)** 和**凭证转换 (Make Token)** 以及 CobaltStrike 更多的用法。后续更新地址：https://blog.csdn.net/qq_36119192/article/details/89489609  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4bPsKsflkyUIGQBtwbrVON6aKpFXZCqiaJxibicEDVk4vC5BLSRDlk2ksibJPZxwdAWC17hqrUP1qptQ/640?wx_fmt=gif)

END

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4bPsKsflkyUIGQBtwbrVON6aKpFXZCqiaJxibicEDVk4vC5BLSRDlk2ksibJPZxwdAWC17hqrUP1qptQ/640?wx_fmt=gif)

来源：谢公子的博客

责编：Vivian

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)