> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247485839&idx=1&sn=f352fde0a840838d80e6b62ff3411f46&chksm=eaad89b2ddda00a4850dabbdd46f3b2bb3c1fdf71bacc80fc3f0441a3160ff346906c1b31428&scene=21#wechat_redirect)

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/jWnm4eP1qjE2MLnDz9Dbul1DkkwIuluX126sdKbVHfjwWgOicfWcF2ibK8J9icZrIXBiaHic8U7Wnv1CfRWfLTrSGrw/640?wx_fmt=png)

  

  

**目录**  

搭建代理

添加路由

搭建 Socks4a 代理

搭建 Socks5 代理

连接代理 

  

  

* * *

> 注：通过 MSF 起的 socks 代理，经常性的不监听端口，也就导致代理失败。试过好多次都是这样，应该是 MSF 的一个 bug。

  

---

  

---

![](https://mmbiz.qpic.cn/mmbiz_jpg/ckiaYOYicQpQTDr3pypAVR9jKaIrn4Qu4136sLAqdnPLuFibU36mEo9b71j3nFUgSa3Vg2hEUb3bHNJMWkWibAAWeQ/640?wx_fmt=jpeg)

搭建代理

当我们通过 MSF 拿到一个机器的权限后，想通过 MSF 搭建 socks 代理，然后通内网。  

MSF 中有三个代理模块，分别是 socks4a、socks5、socks_unc。我们一般用 socks4a 和 socks5 进行代理。socks5 可以设置用户名和密码。这里运行代理后，有时候 MSF 不会监听端口 (有可能是个 bug，试了好多次都有这种情况)，所以也就导致代理失败。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8uySPc1icaXvRe0Fv0848BsXSI7QH7Vj5oibfLgiczHOPW1wMN0LMWUvicw/640?wx_fmt=png)

###   

### 添加路由

在使用代理之前，我们需要先添加路由，让 MSF 能到达目标机器内网。因为这里 socks 模块只是将代理设置为监听的端口 (默认是 1080)，即通过 proxychains 的流量都转给本地的 1080 端口，又因为这是 MSF 起的监听端口，所以通过代理走的流量也都能到达内网。

执行以下命令添加路由

```
route add 0.0.0.0 0.0.0.0 1
```

```
use auxiliary/server/socks4a
set SRVHOST  0.0.0.0
set SRVPORT  1080
run
```

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8gIsWtYQjdHk5TTeznHpeBwicvoeFHVgtS8msy6BicgSCMich0Leo4okicw/640?wx_fmt=png)  
  

###   

![](https://mmbiz.qpic.cn/mmbiz_jpg/ckiaYOYicQpQTDr3pypAVR9jKaIrn4Qu4136sLAqdnPLuFibU36mEo9b71j3nFUgSa3Vg2hEUb3bHNJMWkWibAAWeQ/640?wx_fmt=jpeg)

搭建 Socks4a 代理

```
#使用socks5代理
use auxiliary/server/socks5
set SRVHOST  0.0.0.0
set SRVPORT  1080
set USERNAME root
set PASSWORD Password@
run
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8DKRnupnvokqouQo0GbSOexTNiaSpBbqQRwc1oLOOsxniaZxSKnm3bgyw/640?wx_fmt=png)

###   

### 搭建 Socks5 代理

```
#然后就可以使用其他命令了，比如nmap
proxychains4 nmap -p 1-10000 -Pn -sT x.x.x.x     #在打开其他程序前加上proxychains
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/ckiaYOYicQpQTDr3pypAVR9jKaIrn4Qu4136sLAqdnPLuFibU36mEo9b71j3nFUgSa3Vg2hEUb3bHNJMWkWibAAWeQ/640?wx_fmt=jpeg)

连接代理 

首先修改 / etc/proxychains.conf 文件  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8tBgYib1OWEXN2L1ibFA0HkREg6NW9ZXgn80ZVuEYibMoClqvITGg7JgRA/640?wx_fmt=png)

然后执行命令前加上 proxychains 命令

```
#然后就可以使用其他命令了，比如nmap
proxychains4 nmap -p 1-10000 -Pn -sT x.x.x.x     #在打开其他程序前加上proxychains
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8oBUFWXHfSYHQIHt4PZQUzkOYRs0ZOl6epVs0t8XEpY996iaVUz2o7Tg/640?wx_fmt=png)