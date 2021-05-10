> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [whale3070.github.io](https://whale3070.github.io/oscp/2019/12/25/07-x/)

发表于 2019-12-25 | 分类于 [oscp](https://whale3070.github.io/category/#/oscp) | 阅读数 次

参考资料：

*   [https://www.ssh.com/ssh/tunneling/example#remote-forwarding](https://www.ssh.com/ssh/tunneling/example#remote-forwarding)

修改 VPS ssh 配置
-------------

`vi /etc/ssh/sshd_config`

[![](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/1.PNG)](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/1.PNG) 与 portForwarding 相关的都改为 yes.

本地端口转发 LPF
----------

当本地不能直接连接外部服务的时候，使用 LPF

### 案例一：两个机器

```
-f 后台启用
-g 启用网关功能
-N 不打开远程shell，处于等待状态

ssh -fgN -L 9000:127.0.0.1:80 root@VPS 
这条命令中，使用的IP和端口含义如下

本地：127.0.0.1:9000
远程：VPS:80
一旦连接成功，访问以上两个地址效果相等。
```

[![](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/2.PNG)](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/2.PNG)

访问本地地址 = 访问（原先访问不了的）外网地址

### 案例二：三个机器

```
ssh -fgN -L 9000:211.103.214.132:80 root@VPS

该命令跟上一个案例不同的地方在于，从本地127.0.0.1修改为了远程地址211.103.214.132

本地：127.0.0.1:9000
远程：211.103.214.132:80
VPS: 做代理使用，使用22端口
```

[![](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/3.PNG)](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/3.PNG)

### 注意

只能使用 IP，不能使用域名指代地址 [![](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/4.PNG)](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/4.PNG)

远程端口转发 RPF
----------

当外网访问不了本地的服务的时候，使用 RPF

### 案例一：

首先，本地开启一个 web 服务

```
python -m SimpleHTTPServer 889

ssh -fgN -R 9000:127.0.0.1:889 root@VPS

本地：127.0.0.1:889
远程：VPS:9000

访问外网地址 = 访问（原先访问不了的）内网地址
```

[![](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/6.PNG)](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/6.PNG)

动态端口转发 DPF
----------

我们拥有一个内网机器 A 的 root 权限，可以通过 DPF，是的机器 A 作为我们的跳板机，可以成功访问内网其他机器。

ssh -fgN -D 本地代理端口 888 -p ssh 端口 目标 ip

本地配置浏览器代理，127.0.0.1，端口设置为本地代理端口 888（设置为本地未使用的任意端口）

[![](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/5.PNG)](https://raw.githubusercontent.com/Whale3070/Whale3070.github.io/master/images/12-25-07/5.PNG)

即可访问通过本地代理端口，访问内网主机

总结：
---

*   本地端口转发和远程端口转发有什么区别？

> 前者是内网访问不了外网等情况，一旦连接成功，访问**本地端口**即可。 后者是外网访问不了内网的情况，一旦连接成功，访问**外网端口**即可。 （=。=） 要选择哪种端口转发方式，要取决于要访问哪个服务，不能访问外网的服务，用本地端口转发；不能访问内网的服务，使用远程端口转发。

最后
--

killall -KILL sshd 一条命令关闭所有打开的 ssh 连接