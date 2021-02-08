> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yvMdotfJ-eEe77K73M_mng)

原理
--

### 脏牛漏洞

漏洞是 Linux 内核的内存子系统在处理写时拷贝（Copy-on-Write) 时存在条件竞争漏洞，导致可以破坏私有只读内存映射。黑客可以获取低权限的本地用户后，利用此漏洞获取其他只读内存映射的写权限，进一步获取 root 权限。

### [vdso]

“vDSO”(虚拟动态共享对象) 是一个内核会自动映射到每个用户进程的地址空间的小型共享库。用户的程序通常不需要关心 vdso 的内部细节, 因为这个库主要是提供给 c 语言库使用的。你只需要使用 c 语言库提供的函数, 而 c 语言库会在某些必要的函数中使用到 vdso 提供的功能。  
一个常用的系统调用就是 gettimeofday。这个系统调用既会被用户直接调用, 也可能被 c 语言库调用. 内核将获得答案 (时间) 所需要的信息放置在程序可以访问的到的内存空间中。现在调用 gettimeofday 从需要进行系统调用变成了普通的函数调用和一些内存访问。  
所有进程的 [vdso] 均指向同一块物理地址。

### 环境 及 poc

#### 主机

Ubuntu 14.04.5  
kernel version 4.4.0-31-generic  
![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMVRn4Ov35IibdogKFtia9ibBmppmsn571TPhJGl9fU6zoswAkG35PaZMgw/640?wx_fmt=png)  
docker version 18.06.3-ce  
![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMr3gE36RC2AMgGWFJzT1ABCZFSsvLjmJVBhQ2f9HRWgHoW2MXW7VqPw/640?wx_fmt=png)  
flag  
![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMJE7c2RL7ZZQcr0S6sATXeDK7KDP8nIIjbp94fL6LeFoUSNgKfSbC8Q/640?wx_fmt=png)

#### 容器

![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMAICibIvsyICBnhQW8SFhUKInu3tjhSJyAGdXViasoURiaWge2G2ZHjHow/640?wx_fmt=png)  
容器内 flag  
![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMFIUzsYamYqHobDRZiacDtuxblOp2gIQicMhWWWgGwjiaVTv3EciaquMJWQ/640?wx_fmt=png)

#### POC

https://github.com/scumjr/dirtycow-vdso  
本例中忽略 poc 下载和编译的过程

复现
--

本次选择的 shellcode 功能为 tcp 反弹 shell，设定地址 192.168.10.101:65534  
1. 在远程主机上监听 port：65534  
![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMM5teZhstRBG2kHvBjhA7aouUrs3Mq2s3rMhaKZzKWe51cu0Zt74JiaQ/640?wx_fmt=png)  
2. 在容器中运行编译好的 elf  
![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMSoibX4yXI2h6jia5wS4VfeNPs8nJqRstxaFysYuezMJROlCSzmlYWy4w/640?wx_fmt=png)  
3. 远程主机上收到反弹的 shell 结束  
![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMmFjCoubtuJ0FXOXHvCtCXaeX4loJoqHU3XBmics2o6yGmHNK0mVXodg/640?wx_fmt=png)

分析
--

利用后果
----

本例 poc 永久的修改来内存中 [vdso] 的内容，即便容器已经停止或删除，[vdso]依旧存在 shellcode，但重新启动主机（即重新 load[vdso]）即可修复

#### 漏洞利用前后的 [vdso] 内存内容

![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMZ6UUICyffoia2yK1apbZ1WAHFBnjemyD7nribDvEh02NBxgXJZPJRJrw/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bB3DmyhhHyET0RSTyhz8nMCqzTdz4WI9icJj5icic3Kc4B2tZkTyzABU6T9soSMmLkppICBzl92yEWw/640?wx_fmt=png)（左：漏洞利用后 [vsdo] 的内容；右：漏洞利用前 [vsdo] 的内容）  
位置 0x0960 被替换为了 汇编指令: call near ptr 1EF7h  
位置 0x1ef8 之后的内容 被替换为了 shellcode

![](https://mmbiz.qpic.cn/mmbiz_png/uxzyPCzbE3bW732RU7NAiaZc4JT6DxmZyUNeZGuxDkFCEEStghYzbBh4Va87vPYuw6llsvJzAmVg3I2f9icYTcKA/640?wx_fmt=png)