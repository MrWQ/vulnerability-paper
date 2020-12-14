> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/VTxmMk4EdgZD6SxJKSAsvg)

在内网打洞的时候，frp 因为跨平台性好，性能稳定，所以上场率很高。

使用的时候，一般需要上传两个文件。frpc.exe 和 frpc.ini 两个文件，ini 文件里面要写入配置攻击者自己公网服务器的 ip、和 frp 配置信息等等。有两个问题，第一，上传两个文件，比较麻烦。第二如果配置文件有被溯源的风险。

所以我们希望能够把配置信息硬编码到可执行文件中，这样使用可以更方便一些。  

首先 clone 一下 github 上的源码  

> https://github.com/fatedier/frp

找到如下文件, runClient 函数

> cmd/frpc/sub/root.go

做如下修改，把前面几行注释掉，然后在 content 变量中写入配置信息

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1ds683mtzTAPlEQmia7QIuic5wyV4YdJLJeOZBdqf2IlqbK89GGbSkKjU6ViceBPrUyzCzLxbpgYFwicw/640?wx_fmt=png)

然后编译, 即可无参数启动

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1ds683mtzTAPlEQmia7QIuic5ZzdNQgpvBRcPWibGCJNnkM7lWZATLvSDCxsnWfrYK8NWQkWOqQ3UK8g/640?wx_fmt=png)