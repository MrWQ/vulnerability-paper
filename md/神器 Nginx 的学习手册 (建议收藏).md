> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/TV3LwIh4YQnUWqHPQRtAEg)

```
来源：blog.csdn.net/yujing1314/article/details/107000737

作者：渐暖°
```

前段时间有粉丝请教关于 Nginx 的问题，今天给大家推荐一篇关于 Nginx 的介绍，Nginx 学习起来挺简单的，主要还是多练习！  

![](https://mmbiz.qpic.cn/mmbiz_jpg/lbvmSLlcGOicTia6bHuGgibJ6gkJtj1QQZAJQoQzvJk2PjGwZ4Ojd7miavh3HRuIib8eEDzBIia1MUwlc5icrGcxX9cvg/640?wx_fmt=jpeg)

Nginx 是一个高性能的 HTTP 和反向代理服务器，特点是占用内存少，并发能力强，事实上 Nginx 的并发能力确实在同类型的网页服务器中表现较好。Nginx 专为性能优化而开发，性能是其最重要的要求，十分注重效率，有报告 Nginx 能支持高达 50000 个并发连接数。

**01**

**Nginx 知识网结构图**

Nginx 的知识网结构图如下：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070f2NxYCRUkenCHGZCibFJicDiaCv9BcXgL4kRDibhCteU6zwOCEOvH5mO3Q/640?wx_fmt=png)

**02**

**反向代理**

  

**正向代理：**局域网中的电脑用户想要直接访问网络是不可行的，只能通过代理服务器来访问，这种代理服务就被称为正向代理。

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070PPlwbISQSBzhf1sAeeqNwUHQagLPtWwvHjA00mWluTYThibZnqnnia4g/640?wx_fmt=png)

**反向代理：**客户端无法感知代理，因为客户端访问网络不需要配置，只要把请求发送到反向代理服务器，由反向代理服务器去选择目标服务器获取数据，然后再返回到客户端。  

  

此时反向代理服务器和目标服务器对外就是一个服务器，暴露的是代理服务器地址，隐藏了真实服务器 IP 地址。  

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070CW3mYFhBcrgyGPrAXajVNPYB77RxkwVMjjY6HzEMIGCRaQXkWnbMxg/640?wx_fmt=png)

**03**

**负载均衡**

  

客户端发送多个请求到服务器，服务器处理请求，有一些可能要与数据库进行交互，服务器处理完毕之后，再将结果返回给客户端。  

  

普通请求和响应过程如下图：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070ElynCNRq7Pwz1v2fjupnaIib9ury1RpHVfqicNeYsymMB1Lsh6yZLjHA/640?wx_fmt=png)

但是随着信息数量增长，访问量和数据量飞速增长，普通架构无法满足现在的需求。  

  

我们首先想到的是升级服务器配置，可以由于摩尔定律的日益失效，单纯从硬件提升性能已经逐渐不可取了，怎么解决这种需求呢？  

  

我们可以增加服务器的数量，构建集群，将请求分发到各个服务器上，将原来请求集中到单个服务器的情况改为请求分发到多个服务器，也就是我们说的负载均衡。  

  

图解负载均衡：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070mYLYl3fEeXcNmh01c5Ue9cf72y8JVHPujiabqzn3PRG0icicrKg5jvibiag/640?wx_fmt=png)

假设有 15 个请求发送到代理服务器，那么由代理服务器根据服务器数量，平均分配，每个服务器处理 5 个请求，这个过程就叫做负载均衡。

**04  
**

**动静分离**

  

为了加快网站的解析速度，可以把动态页面和静态页面交给不同的服务器来解析，加快解析的速度，降低由单个服务器的压力。  

  

动静分离之前的状态：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070FwK0Z5yaibzTV33iccaV5HuMQaLr1oibDbXJyRnphUdrNePibbibNLLJORw/640?wx_fmt=png)

动静分离之后：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u0701NlibJ7Qibnr5AoewJdI8nMEhLO3tqEUqQV9X60HvqXcQh5g7yib2kYlg/640?wx_fmt=png)

**06  
**

**Nginx 安装**

Nginx 如何在 Linux 安装

  

参考链接：

```
https://blog.csdn.net/yujing1314/article/details/97267369
```

Nginx 常用命令

  

查看版本：

```
./nginx -v
```

  

启动：

```
./nginx
```

  

关闭（有两种方式，推荐使用 ./nginx -s quit）：

```
 ./nginx -s stop
 ./nginx -s quit
```

  

重新加载 Nginx 配置：

```
./nginx -s reload
```

  

Nginx 的配置文件

  

配置文件分三部分组成：

  

##### **①全局块**

  

从配置文件开始到 events 块之间，主要是设置一些影响 Nginx 服务器整体运行的配置指令。

  

并发处理服务的配置，值越大，可以支持的并发处理量越多，但是会受到硬件、软件等设备的制约。  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070ceEurAwxEr7fReXN8soaFFM0UVYoEN5nxmSl1Nmh2F5Sx07lCuFxrA/640?wx_fmt=png)

  

##### **②events 块**

  

影响 Nginx 服务器与用户的网络连接，常用的设置包括是否开启对多 workprocess 下的网络连接进行序列化，是否允许同时接收多个网络连接等等。

  

支持的最大连接数：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070ZSQBARRvI1m3ictwCkCIc7FT5lpxZXED9Oz7EpAUI3viaQEtuZuOercA/640?wx_fmt=png)

  

##### **③HTTP 块**

  

诸如反向代理和负载均衡都在此配置。  

```
location[ = | ~ | ~* | ^~] url{

}
```

  

location 指令说明，该语法用来匹配 url，语法如上：  

*   **=：**用于不含正则表达式的 url 前，要求字符串与 url 严格匹配，匹配成功就停止向下搜索并处理请求。
    
*   **~：**用于表示 url 包含正则表达式，并且区分大小写。
    
*   **~*：**用于表示 url 包含正则表达式，并且不区分大小写。
    
*   **^~：**用于不含正则表达式的 url 前，要求 Nginx 服务器找到表示 url 和字符串匹配度最高的 location 后，立即使用此 location 处理请求，而不再匹配。
    
*   如果有 url 包含正则表达式，不需要有 ~ 开头标识。
    

**07**

**反向代理实战**

  

### **①配置反向代理**

  

目的：在浏览器地址栏输入地址 www.123.com 跳转 Linux 系统 Tomcat 主页面。  

  

**②具体实现**  

  

先配置 Tomcat，因为比较简单，此处不再赘叙，并在 Windows 访问：  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070H8YfyRgdjbvTxU07bdqckAczlpC9Edc71DDkuwd2TW1he4PD3qhiaNA/640?wx_fmt=png)  

  

具体流程如下图：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070k1odBlOv9xC0smZE7f9KMaJ4askgGh8Sic5bPKNg0t7fIC89mcxFibfg/640?wx_fmt=png)  

修改之前：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070PpzocXYnpJebzLmIDLKHmGOfr5AVCmquota4ylIuDEu6H19z37tCbA/640?wx_fmt=png)

  

配置如下：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070yLGd7yicBY5tYMlAlgA6iag3rH7c7YR6ZXhQforXDAayQUvrr2amUV9w/640?wx_fmt=png)

再次访问：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070Y5UQ5Cf1JrrMy2t3wr4p8NQqHFLzeRpWqicsfpRk0frVnATteHNZTzQ/640?wx_fmt=png)

  

**③反向代理 2**

  

目标：

*   访问 http://192.168.25.132:9001/edu/ 直接跳转到 192.168.25.132:8080
    
*   访问 http://192.168.25.132:9001/vod/ 直接跳转到 192.168.25.132:8081  
    

  

  

**准备：**配置两个 Tomcat，端口分别为 8080 和 8081，都可以访问，端口修改配置文件即可。

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u0706H62Sg72IoxrTBEuUu8aFsNiarB0LiaGIe6pzK1oOUfKbyunkHdcwwqg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070I2fsgic1O8TY0C0hJGxM7X0VnYxzXk14ehDrBuW1Xzib8kskB7jPzcVw/640?wx_fmt=png)  

新建文件内容分别添加 8080！！！和 8081！！！  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070g0gdPTzx0m4vS6WyBtKBicUDTQHG0j7qTEY424lmib7hX4EXPriaHZ8lg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070BMfElQMuXK2zRvPbYaTu5scZzQDcU3ibE1QIV3NzCecULNibefre4WiaQ/640?wx_fmt=png)  

响应如下图：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070kBsRZwMwG8XwkplKFFtbqZxF08QXFHYSXwsIkl8gt4WYQmA1ib32WPg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070bGAacKJzwPq2Dtsb3ufOOXhuZbRu084EptVAJg5QJXUknTNZic00rTw/640?wx_fmt=png)  

具体配置如下：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070OHYLoHb3ewhcQZUE9VQklNYia7vKbgBYfpoMuvTHy8XJHic9MiaOqDyVA/640?wx_fmt=png)

重新加载 Nginx：

  

```
./nginx -s reload
```

  

访问：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070kBdTVdKNOSdE3MTicS4cSulTIWSibueLrVFMOkEIEEgdSyaacRc5ibLLg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070kBdTVdKNOSdE3MTicS4cSulTIWSibueLrVFMOkEIEEgdSyaacRc5ibLLg/640?wx_fmt=png)

实现了同一个端口代理，通过 edu 和 vod 路径的切换显示不同的页面。

  

**反向代理小结**

  

**第一个例子：**浏览器访问 www.123.com，由 host 文件解析出服务器 ip 地址  
192.168.25.132 www.123.com。

  

然后默认访问 80 端口，而通过 Nginx 监听 80 端口代理到本地的 8080 端口上，从而实现了访问 www.123.com，最终转发到 tomcat 8080 上去。

  

第二个例子：

*   访问 http://192.168.25.132:9001/edu/ 直接跳转到 192.168.25.132:8080
    
*   访问 http://192.168.25.132:9001/vod/ 直接跳转到 192.168.25.132:8081  
    

  

实际上就是通过 Nginx 监听 9001 端口，然后通过正则表达式选择转发到 8080 还是 8081 的 Tomcat 上去。

  

  

**08  
**

**负载均衡实战**

  

  

①修改 nginx.conf，如下图：  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u0706HibdMeX4ZGoOloiaytW9cbmZUevic7zhCjhaCrIRuaIzVdricUZd5oLsQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070tZR9ow4AbibMy4IS5ibBydBAwvhexiatORjMMoMfiac4F7k4Hyru0OeKHA/640?wx_fmt=png)

  

②重启 Nginx：  

```
./nginx -s reload
```

  

③在 8081 的 Tomcat 的 webapps 文件夹下新建 edu 文件夹和 a.html 文件，填写内容为 8081！！！！

  

④在地址栏回车，就会分发到不同的 Tomcat 服务器上：  

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070AE4cFBZV8poPm4yMX6OLqODKktFOGPwrfNRPicqlMicEzUO6o8owE1JA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u0704MwPKwdyKKByy7QmFXjC2wjnHWDRBsaKv9tODDtCyFbWGnRIX7Zdww/640?wx_fmt=png)  

负载均衡方式如下：

*   轮询（默认）。
    
*   weight，代表权，权越高优先级越高。
    
*   fair，按后端服务器的响应时间来分配请求，相应时间短的优先分配。  
    
*   ip_hash，每个请求按照访问 ip 的 hash 结果分配，这样每一个访客固定的访问一个后端服务器，可以解决 Session 的问题。
    

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u0701YP460onMRSUz1EViaG60zFc3eibkJVibsOpD4sI4e2W4AOQ5qeTSW9eg/640?wx_fmt=png)  

-------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u0703OL89ibL8iag83gRicVLLicv4j7CVZE57FickVCHF6gdJvglic38fYP1G9AQ/640?wx_fmt=png)  

----------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070tLvpqiaUJST9yzwS78snQnANPBwkcNfmAYTict12ry4ibfjnvE8k1AtTw/640?wx_fmt=png)
----------------------------------------------------------------------------------------------------------------------------------------------

**09**


----------

**动静分离实战**

  

-----------------

  

什么是动静分离？把动态请求和静态请求分开，不是讲动态页面和静态页面物理分离，可以理解为 Nginx 处理静态页面，Tomcat 处理动态页面。
-----------------------------------------------------------------------

  

动静分离大致分为两种：

*   纯粹将静态文件独立成单独域名放在独立的服务器上，也是目前主流方案。
    
*   将动态跟静态文件混合在一起发布，通过 Nginx 分开。
    

####   

#### 动静分离图析：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070LdXqsEJibWwcVz4zFdQamlpIp5FZlxh4AU3lxibTqSFyo2vr9VfkUJYg/640?wx_fmt=png)

  

实战准备，准备静态文件：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070bO5Fp4GaokbPWMUQVN5qVTEezeTnmy9t6qCibIOeOvfGQDj6HofJ2rA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070V5pH79DnRABQFtmCTaibBwoNcRd2iaMeNle8FqLNrn2xZ75I2uO5WEOg/640?wx_fmt=png)

配置 Nginx，如下图：  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070iaVlGlNUe0fjsAxYU2v21rhaZZ0JuPOXfsVMibC2AESt5blIPkoRL1gA/640?wx_fmt=png)

Nginx 高可用

如果 Nginx 出现问题：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070r6rib3ltNLZicw5iceYtRvz7sgY8yZQmMXldgpG3Q3ZOWZ5o0rbkibib9qA/640?wx_fmt=png)

解决办法：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070AbQ0KH4Wu5y5pRwUnUbOXibR3UQoldXQ0lqMibXUhTvNGSQ6rTicIfxfA/640?wx_fmt=png)

前期准备：

*   **两台 Nginx 服务器**
    
*   **安装 Keepalived**
    
*   **虚拟 ip**
    

  

安装 Keepalived：
--------------

```
[root@192 usr]# yum install keepalived -y
[root@192 usr]# rpm -q -a keepalived
keepalived-1.3.5-16.el7.x86_64
```

  

修改配置文件：

```
[root@192 keepalived]# cd /etc/keepalived
[root@192 keepalived]# vi keepalived.conf
```

  

分别将如下配置文件复制粘贴，覆盖掉 keepalived.conf，虚拟 ip 为 192.168.25.50。  

  

对应主机 ip 需要修改的是：  

*   smtp_server 192.168.25.147（主）smtp_server 192.168.25.147（备）
    
*   state MASTER（主） state BACKUP（备）
    

  

```
global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.25.147
   smtp_connect_timeout 30
   router_id LVS_DEVEL # 访问的主机地址
}

vrrp_script chk_nginx {
  script "/usr/local/src/nginx_check.sh"  # 检测文件的地址
  interval 2   # 检测脚本执行的间隔
  weight 2   # 权重
}

vrrp_instance VI_1 {
    state BACKUP    # 主机MASTER、备机BACKUP    
    interface ens33   # 网卡
    virtual_router_id 51 # 同一组需一致
    priority 90  # 访问优先级，主机值较大，备机较小
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.25.50  # 虚拟ip
    }
}
```

  

启动代码如下：

```
[root@192 sbin]# systemctl start keepalived.service
```

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070rxeYx90zzrcUfHmnJwRelYdnJr1sXrBScUPSD8yIib6D4nQkxKdqweQ/640?wx_fmt=png)

  

访问虚拟 ip 成功：

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070JJMVSYVJnVhySneVp7C1Y7jMmcMoPwbVjZzGVe1iczcqJzpDrSRLVoA/640?wx_fmt=png)

关闭主机 147 的 Nginx 和 Keepalived，发现仍然可以访问。  

  

原理解析

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u0706jB3SfG0RrqdmaU8HE6e5A4qTynwactlhBMmM0wqNicGGws98kCdiaqQ/640?wx_fmt=png)

如下图，就是启动了一个 master，一个 worker，master 是管理员，worker 是具体工作的进程。  

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070muQU3rnx4KFwDOmx2ovwgFbmpu6o6ey0kZKWuWgjhSwDhohkpVNeCA/640?wx_fmt=png)

worker 如何工作？如下图：

  

![](https://mmbiz.qpic.cn/mmbiz_png/MOwlO0INfQrRD4Mcr0icGmGAj3uB9u070giaYRsmv7NU97QWqHra8HENYBGZib3DyEnVg0Qbky5Xzk1D9Tu87DFqA/640?wx_fmt=png)

  

小结

  

worker 数应该和 CPU 数相等；一个 master 多个 worker 可以使用热部署，同时 worker 是独立的，一个挂了不会影响其他的。

_**-END-**_

**![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)**   **小贴士**

隐藏菜单：返回上一级 回复 “ **1024** " 关键词，即可获取**内部**学习资料

![](https://mmbiz.qpic.cn/mmbiz_gif/eLGbtHI53ibupFlAgJ2icY5y2kQXvbbd1b6AJNFxfOc6QK51I9A1EQkXKFRGVgGHpy2q3lmbasEkic74NZxdfciaKg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_jpg/CclibSeTViaL4b5uTYsMTnuf9v502qvJdhwxygQq0X54J8icdic2Pch9haFbH7fkzia03yDPrEqyjqOcdmdIoeltibaw/640?wx_fmt=jpeg)

一个认真分享的小编

前沿技术 / 名气内推 / 干货分享

![](https://mmbiz.qpic.cn/mmbiz_png/DdnDrjTQp57k6GTcUxqFrqPZ93qbrjuGaP9vuZlZvf2megI2TsnT5FkdhaSfo8QAe8SmAM2AMZhR4G0obMISrw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CclibSeTViaL4b5uTYsMTnuf9v502qvJdhSRSM63T0pzcKibeb1ocGC8PicwA5nXzXibz1nzUKRAIDdCeBBKxGYeUew/640?wx_fmt=png)商务合作：dot3721

![](https://mmbiz.qpic.cn/mmbiz_png/DdnDrjTQp57k6GTcUxqFrqPZ93qbrjuGRmSoOs2K1rAUSTw95sTsUXbicicBDwy2Vt1fLBGeynrJxz2FoR5cy4pw/640?wx_fmt=png) 长按左侧二维码添加

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWjKiapL98Oria66bg57VxkiaJwKTjRKYLpzn1Qo9w8Z575nyRVSwGXlw8k4XjEHib1Vic3007YLryicbQhw/640?wx_fmt=gif)

点分享

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWjKiapL98Oria66bg57VxkiaJwyNXHpzrB5P8ic30yv2VxDiaFFXmaXkZ959KKYiaPAOAFjGze6Wibdw2N9Q/640?wx_fmt=gif)

点点赞

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWjKiapL98Oria66bg57VxkiaJwo6zuLZ0zJLXjb8m2ARia9vUF7rGlBXGb9FVN0ZC12MRT0WOZWp7tDibQ/640?wx_fmt=gif)

点在看