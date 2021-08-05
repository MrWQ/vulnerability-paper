> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/wEVMorLBGH39YRY5ITv5TA)

本章主要介绍，IoTGoat 靶场的搭建以及测试工具的准备。  

**1.  介绍**

OWASP 开源的一款 IoT 基于 Openwrt 的固件，集成了多个漏洞。

**2.  环境搭建**

2.1  克隆项目

```
$ git clone https://github.com/OWASP/IoTGoat.git
$ cd IoTGoat/OpenWrt/openwrt-18.06.2/
$ ./scripts/feeds update -a
$ ./scripts/feeds install -a
```

2.2  配置 Openwrt  

*   设置架构 x86_64(自己编译需要选择 pcnet 驱动和无线网络驱动选项)
    

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEqXgNzic0Nbkqt7Aa3KWYDcXsb62c8KUEaXMDK269Mql7eu93mRQTvFg/640?wx_fmt=png)

*   设置生成 vmdk(可供调试)
    

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEiabDmJGkWFeegic2HBFm37TM0DuBMM8MMedJdGeqN3q8xuecH2gKbWbA/640?wx_fmt=png)

### 2.3   编译

```
$ make -j1 V=s
```

*   报错
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEaTzHEJViaMJmkcVQNvMbFyDpR7C3xp3M6oicjEiauWDbOhzTGoibAebaqg/640?wx_fmt=png)
    

修改 int-ll64.sh

```
__extension__ typedef unsigned long long __u64;
修改之后
__extension__ typedef unsigned long __u64;
```

find-utils 编译总是错误，猜测是系统版本过高，导致头文件引用出现问题

**使用 ubuntu 16.04 lts 版本进行重新编译**  

### 2.4 文件生成

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWE0zpP8AWGsb7OrviaiaM0WGBHcXkL1LwkgicG61AKa1WZwlgwNTl2DjMBA/640?wx_fmt=png)

这边官方提供 realse 版本，我们采用官方提供的版本。

**3.  虚拟机创建**

### 3.1 创建一个新的虚拟机

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEEggqicagDFib6E2fXHgZMoJvGVYDauQZ2q05crKwC15NmuezYLqKM3SA/640?wx_fmt=png)

### 3.2 选择使用现有的虚拟磁盘

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEEFqibx7qGxWK5nz1fWjEhtfiaMmvib0sa7ic4AOHHuCojPrCg8W301vJfg/640?wx_fmt=png)

### 3.3 运行虚拟机

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWE1cQM2yz8XUk9YvLf0FvKe4BhQRHMiaMFDs8rNy8NyQct7rJDZmlZhwQ/640?wx_fmt=png)

**4.  工具准备**  

#### 4.1 密码破解  

john 密码破解工具 (https://www.openwall.com/john/)

**编译**

```
# 进入src目录
$ cd src
$ ./configure 
$ make -s clean && make -sj4 V=s
```

**运行**

```
# 进入run目录
$ ./john
```

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEF5c06QuBH8Nj5YYicUibnA4AQtyaPuJamnG5WsObfYd7XQ1BjzX3ibaCQ/640?wx_fmt=png)

常用的密码字典项目

```
$ git clone git://github.com/danielmiessler/SecLists.git
```

该项目存储常见的密码字典

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEerB0tW0A7iaXaDeEuxkocwC930R6zrotThicHLjeibB0nQyzFkHApOdDw/640?wx_fmt=png)

#### 4.2 Hydra 工具

**hydra** 是一个支持众多协议的爆破工具。

**安装**

```
$ apt-get install hydra -y
```

**运行**

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEyvJMIS5T4ZfvlJrQFRuYXic2Q7RYqmiaTnJkwHiac7vNAdwZL6LszlgeA/640?wx_fmt=png)

#### 4.3 Upnp Client 工具

Miranda -- The interactive UPnP client

下载地址 https://github.com/isaacfife/miranda.git

**安装**

```
$ git clone https://github.com/isaacfife/miranda.git
$ cd miranda
$ sudo python setup.py install
```

**运行**

```
$ miranda
```

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEOicJaToPZicCyMRzm4ojuw04ZAAu8ZNplx1loGNniaGd1yewic0AOpRgHw/640?wx_fmt=png)

**5.  漏洞挖掘思路**

本次 IoTGoat 漏洞挖掘，主要根据 OWASP TOP10，来进行该固件的漏洞挖掘。

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEc5QAYc0SgVQp72hRgGmHxiaUNZkDRDwuPCAqnRkl01qGJ1BTRdfIuicQ/640?wx_fmt=png)

**总结**

    本篇系列文章，主要从漏洞环境搭建、工具准备、漏洞挖掘三个方面入手。对物联网设备漏洞挖掘过程有一个清晰的认识，接下来的几篇系列文章，也将从不同的角度，去发现未知的固件漏洞。

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnTqMVczDE3GyGU1hPA7RQQlIESOibcZaWMeJVMicz1JUKnoSKhomypNO0J7q4BAxqjgxmpWYYe17ia2A/640?wx_fmt=png)

如果您有意向加入我们，请留言: )，

或邮件投递简历：akast@hillstonenet.com