> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Qxpc3icE2fHBZjjRvwXYTQ)

![](https://mmbiz.qpic.cn/mmbiz_gif/3k9IT3oQhT09IJjs3wGQbICd50va8zMqfnXZfD5LGdibcuOrtia3P4DpMAVfibZ8J4MsbHt0JW20QL8Wh0SO8zpyA/640?wx_fmt=gif)

**作者：0x7F@知道创宇 404 实验室  
时间：2021 年 4 月 12 日**

**0x00 前言**

一直对 P2P 和 NAT 穿透的知识比较感兴趣，正巧最近看到一篇不需要第三方服务器实现 NAT 穿透的项目 (https://github.com/samyk/pwnat)，经过学习研究后发现这个项目也有很多局限性；借此机会，学习了下 NAT 原理和 UDP 穿透的实现。

本文详细介绍了 NAT 的原理，并以此作为基础介绍了 UDP 穿透的原理和实现。

  
**0x01 NAT 基础和分类**

NAT(Network Address Translation) 全称为「网络地址转换」，用于为了解决 IPv4 地址短缺的问题。NAT 可以将私有地址转换为公有 IP 地址，以便多台内网主机只需要一个公有 IP 地址，也可以正常与互联网进行通信。

NAT 可以分为两大类：

1. 基础 NAT：网络地址转换 (Network Address Translation)

2.NAPT：网络地址端口转换 (Network Address Port Translation)

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyLvDQwdrUicbuoBPSFQPr2I6nqAd45tRCaIYVOSwsVxZe6soTBKOahqhw/640?wx_fmt=png)

[1.NAT 分类]

**1. 基础 NAT**  
基础 NAT 仅对网络地址进行转换，要求对每一个当前连接都要对应一个公网 IP 地址，所以需要有一个公网 ip 池；基础 NAT 内部有一张 NAT 表以记录对应关系，如下

| 

内网 ip

 | 

外网 ip

 |
| --- | --- |
| 

192.168.1.1

 | 

1.2.3.4

 |
| 

192.168.1.12

 | 

1.2.3.5

 |
| 

192.168.1.123

 | 

1.2.3.6

 |

> 基础 NAT 又分为：静态 NAT 和 动态 NAT，其区别在于：静态要求内网 ip 和外网 ip 存在固定的一一对应关系，而动态不存在这种固定的对应关系。

**2.NAPT**  
NAPT 需要对网络地址和端口进行转换，这种类型允许多台主机共用一个公网 ip 地址，NAPT 内部同样有一张 NAT 表，并标注了端口，以记录对应关系，如下：

| 

内网 ip

 | 

外网 ip

 |
| --- | --- |
| 

192.168.1.1:1025

 | 

1.2.3.4:1025

 |
| 

192.168.1.1:3333

 | 

1.2.3.5:10000

 |
| 

192.168.1.12:7788

 | 

1.2.3.6:32556

 |

> NAPT 又分为：锥型 NAT 和 对称型 NAT，其对于映射关系有不同的权限限制，锥型 NAT 在网络拓扑图上像圆锥，我们在下文进行深入了解。

**0x02 NAPT**

**目前常见的都是 NAPT 类型，我们常说的 NAT 也是特指 NAPT(我们下文也遵循这个)**。如图 1 所示，NAPT 可分为四种类型：1. 完全锥型，2. 受限锥型，3. 端口受限锥型，4. 对称型。

**1. 完全锥型**  
从同一个内网地址端口 (`192.168.1.1:7777`) 发起的请求都由 NAT 转换成公网地址端口 (`1.2.3.4:10000`)，`192.168.1.1:7777` 可以收到任意外部主机发到 `1.2.3.4:10000` 的数据报。

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyLXV3H0pa7ABZ8rlBibTUgFlONIoenoa985P3ped4MDhGyKOanzCCcicGw/640?wx_fmt=png)

[2. 完全锥型 NAT]

**2. 受限锥型**  
受限锥型也称地址受限锥型，在完全锥型的基础上，对 ip 地址进行了限制。

从同一个内网地址端口 (`192.168.1.1:7777`) 发起的请求都由 NAT 转换成公网地址端口 (`1.2.3.4:10000`)，其访问的服务器为 `8.8.8.8:123`，只有当 `192.168.1.1:7777` 向 `8.8.8.8:123` 发送一个报文后，`192.168.1.1:7777` 才可以收到 `8.8.8.8` 发往 `1.2.3.4:10000` 的报文。

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyLBJoooOI8ib1dk46K0alpHFAib8bibEAn15zqgZ2cSmolnvJnBiaZrSwb2g/640?wx_fmt=png)

[3. 受限锥型 NAT]  

**3. 端口受限锥型**  
在受限锥型的基础上，对端口也进行了限制。

从同一个内网地址端口 (`192.168.1.1:7777`) 发起的请求都由 NAT 转换成公网地址端口 (`1.2.3.4:10000`)，其访问的服务器为 `8.8.8.8:123`，只有当 `192.168.1.1:7777` 向 `8.8.8.8:123` 发送一个报文后，`192.168.1.1:7777` 才可以收到 `8.8.8.8:123` 发往 `1.2.3.4:10000` 的报文。

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyLULJ5VC7l0tTuuPpuddU9mic9dJ60JLN7qAYCpO1FxZlib2AxWLoude9A/640?wx_fmt=png)

[4. 端口受限锥型 NAT]

**4. 对称型**  
在 对称型 NAT 中，只有来自于同一个内网地址端口 、且针对同一目标地址端口的请求才被 NAT 转换至同一个公网地址端口，否则的话，NAT 将为之分配一个新的公网地址端口。

如：内网地址端口 (`192.168.1.1:7777`) 发起请求到 `8.8.8.8:123`，由 NAT 转换成公网地址端口 (`1.2.3.4:10000`)，随后内网地址端口 (`192.168.1.1:7777`) 又发起请求到 `9.9.9.9:456`，NAT 将分配新的公网地址端口 (`1.2.3.4:20000`)

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyLOM7BVQB8hY33CHIGfRyUiavCoWRddHp8MmKLuKCpppAZsyuHWV3CricA/640?wx_fmt=png)

[5. 对称型 NAT]

> 可以这么来理解，在 锥型 NAT 中：映射关系和目标地址端口无关，而在 对称型 NAT 中则有关。锥型 NAT 正因为其于目标地址端口无关，所以网络拓扑是圆锥型的。  
> 补充下 锥型 NAT 的网络拓扑图，和对称型进行比较

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyLsheKcHtMkdDe8G06Vpx11psCoyQhKSb4NV2aiaiau5b6n2icNQORNGvhw/640?wx_fmt=png)

[6. 锥型 NAT]

  
**0x03 NAT 的工作流程**

按照上文描述，我们可以很好的理解 NAT 对传输层协议 (TCP/UDP) 的处理，这里举例来更加深入的理解 NAT 的原理。

**1. 发送数据**  
当一个 TCP/UDP 的请求 (`192.168.1.1:7777 => 8.8.8.8:123`) 到达 NAT 网关时 (`1.2.3.4`)，由 NAT 修改报文的源地址和源端口以及相应的校验码，随后再发往目标：

```
192.168.1.1:7777 => 1.2.3.4:10000 => 8.8.8.8:123
```

**2. 接收数据**  
随后 `8.8.8.8:123` 返回响应数据到 `1.2.3.4:10000`，NAT 查询映射表，修改目的地址和目的端口以及相应的校验码，再将数据返回给真实的请求方：

```
8.8.8.8:123 => 1.2.3.4:10000 => 192.168.1.1:7777
```

**3. 其他协议**  
不同协议的工作特性不同，其和 TCP/UDP 协议的处理方式不同；比如 ICMP 协议工作在 IP 层，没有端口信息，NAT 以 ICMP 报文中的 `identifier` 作为标记，以此来判断这个报文是内网哪台主机发出的。

下图为 `Cisco Packet Tracer` 下，在客户端发起 `TCP/UDP/ICMP` 请求后的 `NAT translations`：

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyLxZWeW4GTezQndhnfVM0NXZDgsLKciaT7ua9mHHYR4TzFjbqcZDFibfFg/640?wx_fmt=png)

[7.PacketTracer 模拟环境下的 NAT 表]

> 当然还有一些特殊的协议，比如 FTP 协议，当请求一个文件传输时，主机在发送请求的同时也通知对方自己想要在哪个端口接受数据，NAT 必须进行特殊处理才能支持这种通信机制。  
> 在 NAT 中有一个应用网关层 (Application Layer Gateway, ALG)，以此来统一处理这些协议问题。

**4. 映射老化时间**  
建立了 NAT 映射关系后，这些映射什么时候失效呢？

不同协议有不同的失效机制，比如 TCP 的通信在收到 RST 过后就会删除映射关系，或 TCP 在某个超时时间后也会自动失效，而 ICMP 在收到 ICMP 响应后就会删除映射关系，当然超时后也会自动失效。具体的实现还和各个厂商有关系。

**0x04 NAT 类型探测**

探测 NAT 的类型是 NAT 穿透中的第一步，我们可以通过客户端和两个服务器端的交互来探测 NAT 的工作类型，以下是来源于 STUN 协议 (https://tools.ietf.org/html/rfc3489) 的探测流程图，在其上添加了一些标注：

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyLX1tD7l6ibhHrZCY8MiaROCr7BzXXUs3dFr2kx2UKxqMezvL8xFQWFsZA/640?wx_fmt=png)

[8.NAT 类型探测流程]

如图所示，我们可以整理出：

1. 客户端使用同一个内网地址端口分别向主服务器和协助服务器 (不同 IP) 发起 UDP 请求，主服务器获取到客户端出口地址端口后，返回给客户端，客户端对比自己本地地址和出口地址是否一致，如果是则表示处于 Open Internet 中。

2. 协助服务器同样也获取到了客户端出口地址端口，将该信息转发给主服务器，同样将该信息返回给客户端，客户端对比两个出口地址端口 (1. 主服务器返回的，2. 协助服务器返回的) 是否一致，如果是则表示处于 Symmetric NAT 中。

3. 客户端再使用不同的内网地址端口分别向主服务器和协助服务器 (不同 IP) 发起 UDP 请求，主服务器和协助服务器都可以获得一个新的客户端出口地址端口，协助服务器将客户端出口地址端口转发给主服务器。

4. 主服务器向协助服务器获取到的客户端出口地址端口发送 UDP 数据，客户端如果可以收到数据，则表示处于 Full-Cone NAT 中。

5. 主服务器使用另一个端口，向主服务器获取到的客户端出口地址端口发送 UDP 数据，如果客户端收到数据，则表示处于 Restricted NAT 中，否则处于 Restricted-Port NAT 中。

按照该步骤，我们编写了 NAT 类型探测的示例脚本 nat_check.py。

```
#!/usr/bin/python3
#coding=utf-8

import socket
import sys

def server(addr):
    print("[NAT CHECK launch as server on %s]" % str(addr))

    # listen UDP service
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr)

    # [1. check "Open Internet" and "Symmetric NAT"]
    # recevie client request and return export ip
    data, cconn = sock.recvfrom(1024)
    print("server get client info: %s" % str(cconn))
    data = "%s:%d" % (cconn[0], cconn[1])
    sock.sendto(data.encode("utf-8"), cconn)

    # receive assist data about client another export ip
    data, aconn = sock.recvfrom(1024)
    print("server get client info (from assist): %s" % data.decode("utf-8"))
    sock.sendto(data, cconn)

    # [2. check "Full-Cone NAT", "Restricted NAT" and "Restricted-Port NAT"]
    # recevie client request
    data, cconn = sock.recvfrom(1024)
    print("server get client info: %s" % str(cconn))
    # receive assist data about client another export ip
    data, aconn = sock.recvfrom(1024)
    print("server get client info (from assist): %s" % data.decode("utf-8"))

    # send data to client through (assist get) export ip
    print("send packet for testing Full-Cone NAT")
    array = data.decode("utf-8").split(":")
    caconn = (array[0], int(array[1]))
    sock.sendto("TEST FOR FULL-CONE NAT".encode("utf-8"), caconn)

    # send data to client through (server get) export ip and with different port
    sock.recvfrom(1024) # NEXT flag
    print("send packet for testing Restricted NAT")
    cdconn = (cconn[0], cconn[1] - 1)
    sock.sendto("TEST FOR Restricted NAT".encode("utf-8"), cdconn)

    # send data to client through (server get) export ip
    sock.recvfrom(1024) # NEXT flag
    print("send packet for testing Restricted-Port NAT")
    sock.sendto("TEST FOR Restricted-Port NAT".encode("utf-8"), cconn)
# server()

def assist(addr, serv):
    print("[NAT CHECK launch as assist on %s && server=%s]" %
                                                    (str(addr), str(serv)))

    # listen UDP service
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr)

    # [1. check "Open Internet" and "Symmetric NAT"]
    # recevie client request and forward to server
    data, conn = sock.recvfrom(1024)
    print("assist get client info: %s" % str(conn))
    data = "%s:%d" % (conn[0], conn[1])
    sock.sendto(data.encode("utf-8"), serv)

    # [2. check "Full-Cone NAT", "Restricted NAT" and "Restricted-Port NAT"]
    # recevie client request and forward to server
    data, conn = sock.recvfrom(1024)
    print("assist get client info: %s" % str(conn))
    data = "%s:%d" % (conn[0], conn[1])
    sock.sendto(data.encode("utf-8"), serv)
# assist()

def client(serv, ast):
    print("[NAT CHECK launch as client to server=%s && assist=%s]" %
                                                    (str(serv), str(ast)))

    # [1. check "Open Internet" and "Symmetric NAT"]
    print("send data to server and assist")
    # get local address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(serv)
    localaddr = sock.getsockname()

    # send data to server and assist with same socket
    # and register so that the server can obtain the export ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("register".encode("utf-8"), serv)
    sock.sendto("register".encode("utf-8"), ast)

    # receive export ip from server
    data, conn = sock.recvfrom(1024)
    exportaddr = data.decode("utf-8")
    print("get export ip: %s, localaddr: %s" % (exportaddr, str(localaddr)))

    # check it is "Open Internet"
    if exportaddr.split(":")[0] == localaddr[0]:
        print("[Open Internet]")
        return
    # end if

    # receive another export ip (assist) from server
    data, conn = sock.recvfrom(1024)
    anotheraddr = data.decode("utf-8")
    print("get export ip(assist): %s, export ip(server): %s" % (anotheraddr, exportaddr))

    # check it is "Symmetric NAT"
    if exportaddr != anotheraddr:
        print("[Symmetric NAT]")
        return
    # end if

    # [2. check "Full-Cone NAT", "Restricted NAT" and "Restricted-Port NAT"]
    # send data to server and assist with different socket
    # receive the data sent back by the server through the export ip(assist) mapping
    ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ssock.sendto("register".encode("utf-8"), serv)
    asock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    asock.sendto("register".encode("utf-8"), ast)

    asock.settimeout(5)
    try:
        data, conn = asock.recvfrom(1024)
        print("[Full-Cone NAT]")
        return
    except:
        pass

    # receive the data sent back by the server with different port
    ssock.sendto("NEXT".encode("utf-8"), serv)
    ssock.settimeout(5)
    try:
        data, conn = ssock.recvfrom(1024)
        print("[Restricted NAT]")
        return
    except:
        pass

    # receive the data sent back by the server
    ssock.sendto("NEXT".encode("utf-8"), serv)
    ssock.settimeout(5)
    try:
        data, conn = ssock.recvfrom(1024)
        print("[Restricted-Port NAT]")
    except:
        print("[Unknown, something error]")
# client()

def usage():
    print("Usage:")
    print("  python3 nat_check.py server [ip:port]")
    print("  python3 nat_check.py assist [ip:port] [server]")
    print("  python3 nat_check.py client [server] [assist]")
# end usage()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        exit(0)
    # end if

    role = sys.argv[1]
    array = sys.argv[2].split(":")
    address1 = (array[0], int(array[1]))
    if role == "assist" or role == "client":
        if len(sys.argv) > 3:
            array = sys.argv[3].split(":")
            address2 = (array[0], int(array[1]))
        else:
            usage()
            exit(0)
    # end if

    # server/client launch
    if role == "server":
        server(address1)
    elif role == "assist":
        assist(address1, address2)
    elif role == "client":
        client(address1, address2)
    else:
        usage()
# end main()
```

> 实际网络往往都更加复杂，比如：防火墙、多层 NAT 等原因，会导致无法准确的探测 NAT 类型。

**0x05 UDP 穿透**

在 NAT 的网络环境下，p2p 网络通信需要穿透 NAT 才能够实现。在熟悉 NAT 原理过后，我们就可以很好的理解如何来进行 NAT 穿透了。NAT 穿透的思想在于：如何复用 NAT 中的映射关系？

在 锥型 NAT 中，同一个内网地址端口访问不同的目标只会建立一条映射关系，所以可以复用，而 对称型 NAT 不行。同时，由于 TCP 工作比较复杂，在 NAT 穿透中存在一些局限性，所以在实际场景中 UDP 穿透使用得更广泛一些，这里我们详细看看 UDP 穿透的原理和流程。

> 我们以 `Restricted-Port NAT` 类型作为例子，因为其使用得最为广泛，同时权限也是最为严格的，在理解 `Restricted-Port NAT` 类型穿透后，`Full-Cone NAT` 和 `Restricted NAT` 就触类旁通了；  
> 在实际网络场景下往往都是非常复杂的，比如：防火墙、多层 NAT、单侧 NAT，这里我们选择了两端都处于一层 NAT 的场景来进行演示讲解，可以让我们更容易的进行理解。

在我们的演示环境下，有 `PC1，Router1，PC2，Router2，Server` 五台设备；公网服务器用于获取客户端实际的出口地址端口，UDP 穿透的流程如下：

1.`PC1(192.168.1.1:7777)` 发送 UDP 请求到 `Server(9.9.9.9:1024)`，此时 Server 可以获取到 PC1 的出口地址端口 (也就是 Router1 的出口地址端口) `1.2.3.4:10000`，同时 Router1 添加一条映射 `192.168.1.1:7777 <=> 1.2.3.4:10000 <=> 9.9.9.9:1024`

2.`PC2(192.168.2.1:8888)` 同样发送 UDP 请求到 Server，Router2 添加一条映射 `192.168.2.1:8888 <=> 5.6.7.8:20000 <=> 9.9.9.9:1024`

3.Server 将 PC2 的出口地址端口 (`5.6.7.8:20000`) 发送给 PC1

4.Server 将 PC1 的出口地址端口 (`1.2.3.4:10000`) 发送给 PC2

5.PC1 使用相同的内网地址端口 (`192.168.1.1:7777`) 发送 UDP 请求到 PC2 的出口地址端口 (`Router2 5.6.7.8:20000`)，此时 Router1 添加一条映射 `192.168.1.1:7777 <=> 1.2.3.4:10000 <=> 5.6.7.8:20000`，与此同时 Router2 没有关于 `1.2.3.4:10000` 的映射，这个请求将被 Router2 丢弃

6.PC2 使用相同的内网地址端口 (`192.168.2.1:8888`) 发送 UDP 请求到 PC1 的出口地址端口 (`Router1 1.2.3.4:10000`)，此时 Router2 添加一条映射 `192.168.2.1:8888 <=> 5.6.7.8:20000 <=> 1.2.3.4:10000`，与此同时 Router1 有一条关于 `5.6.7.8:20000` 的映射 (上一步中添加的)，Router1 将报文转发给 `PC1(192.168.1.1:7777)`

7. 在 Router1 和 Router2 都有了对方的映射关系，此时 PC1 和 PC2 通过 UDP 穿透建立通信。  

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3UZ6iaKEmz1MBpqYVHCUbyL2F8alOicvrLlUxPFBtLSeeyia9Guk0OL9tXYhtjiaPAORicTjofuVOPuqQ/640?wx_fmt=png)

[9.UDP 打洞流程]

按照该步骤，我们编写了 UDP 穿透的示例脚本：

server.py

```
#!/usr/bin/python3
#coding=utf-8

import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.bind(("0.0.0.0", 1024))

    # 1.receive message and get one export ip:port (PC1)
    data, conn1 = sock.recvfrom(1024)
    addr1 = "%s:%d" % (conn1[0], conn1[1])
    print("1.get PC1 export ip:port = %s" % addr1)

    # 2.receive message and get another export ip:port (PC2)
    data, conn2 = sock.recvfrom(1024)
    addr2 = "%s:%d" % (conn2[0], conn2[1])
    print("2.get PC2 export ip:port = %s" % addr2)

    # 3.send export address of PC1 to PC2
    sock.sendto(addr1.encode("utf-8"), conn2)
    print("3.send export address of PC1(%s) to PC2(%s)" % (addr1, addr2))

    # 4.send export address of PC2 to PC1
    sock.sendto(addr2.encode("utf-8"), conn1)
    print("4.send export address of PC2(%s) to PC1(%s)" % (addr2, addr1))

    print("done")
    sock.close()
# end main()
```

client.py

```
#!/usr/bin/python3#coding=utf-8import randomimport socketimport stringimport timeif __name__ == "__main__":    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     #serv = ("10.0.1.1", 1024)    serv = ("192.168.50.55", 1024)    print("server =>", serv)    # 1/2.send message to server, server can get our export ip:port    sock.sendto("REGISTER".encode("utf-8"), serv)    print("1/2.send REGISTER message to server")    # 3/4.receive the export address of the peer from the server    data, conn = sock.recvfrom(1024)    array = data.decode("utf-8").split(":")    addr = (array[0], int(array[1]))    print("3/4.receive the export address of the peer, %s" % str(addr))    # 5/6.send KNOCK message to export address of peer    wait = random.randint(2, 5)    print("5/6.send KNOCK message to export address of peer (wait %d s)" % wait)    # in order to stagger the two clients    # so that the router can better create the mapping    time.sleep(wait)    sock.sendto("KNOCK".encode("utf-8"), addr)    name = "".join(random.sample(string.ascii_letters, 8))    print("my name is %s, start to communicate" % name)    # 7.communicate each other    count = 0    while True:        sock.settimeout(5)        try:            data, conn = sock.recvfrom(1024)            print("%s => %s" % (str(conn), data.decode("utf-8")))        except Exception as e:            print(e)        msg = "%s: %d" % (name, count)        count += 1        sock.sendto(msg.encode("utf-8"), conn)        time.sleep(1)    # end while()    sock.close()# end main()
```

  
**0x06 拓展**

在实践了以上步骤后，我们对 锥型 NAT 下的 UDP 穿透已经有了大致的了解，那我们接着再拓展研究一下「其他场景」。

**1.Symmetric NAT 可以穿透吗？**  
根据 `Symmetric NAT` 的特性我们可以知道当请求的目标端口地址改变后，会创建新的一对映射关系，我们无法知晓新的映射关系中的端口号；但是在实际场景下，**部分路由器**对于 `Symmetric NAT` 的生成算法过于简单，新的端口可能呈现于：递增、递减、跳跃等特征，所以这种条件下，我们可以基于端口猜测，来穿透 `Symmetric NAT`。

> 如果两端的 `Symmetric NAT` 路由器是已知的，我们可以直接逆向分析映射生成算法，即可准确预测端口号。

**2.TCP 穿透有哪些难点？**  
TCP 穿透的流程基本和 UDP 穿透一样。

在标准 socket 规范中，UDP 可以允许多个 socket 绑定到同一个本地端口，但 TCP 不行，在 TCP 中我们不能在同一个端口上既 `listen` 又进行 `connect`；不过在**部分操作系统**下 socket 提供了端口复用选项 (`SO_REUSEADDR / SO_REUSEPORT`) 可以允许 TCP 绑定多个 socket。

在使用端口复用选项后，TCP 就按照 UDP 穿透的流程一样借助公网服务器然后向对端发送 `syn` 报文了，其中靠后的 `syn` 报文就可以正确穿透完成 TCP 握手并建立连接。

**但是**在实际场景下还有诸多的阻碍，不同厂商的 NAT 实现机制有一些差异，比如某些针对 TCP 的实现有：

1. 对端 NAT 在接收到 syn 由于没有找到映射而返回 RST 报文，而本端 NAT 在接收到 RST 报文后删除了此条映射

2. 由于主机生成的 syn 报文中的 seq 序号为随机值，如果 NAT 开启了 syn 过滤，对于没有标记过的 seq 的报文将直接丢弃

3. 等等

**3. 无第三方服务器的穿透**  
我们回到文章开头提到的「不需要第三方服务器实现 NAT 穿透」的方法，文中作者先提出了一种便于理解的网络拓扑，客户端位于公网，服务器位于 NAT 下，我们必须预先知道服务器的公网地址；在这个方法下，服务器不断的向外部未分配的地址发送 `ICMP(ECHO REQUEST)` 消息，服务器端的 NAT 将保留一条 ICMP 响应的映射，由于目的地址未分配所以没有设备会响应服务器发出的请求，此时由客户端发送一条伪装的 `ICMP(DESTINATION UNREACHABLE)` 给服务器，服务器可以收到该条消息并从中获取到客户端的地址；随后便可以根据预先约定的端口进行穿透并通信了。

但是如果客户端也位于 NAT 下呢，由于 NAT 可能会更改源端口信息 (不同厂商的 NAT 实现不同)，导致无法向上文一样使用预设端口进行通信，所以这里需要和 `Symmetric NAT` 穿透一样进行端口猜测。

  
**0x07 总结**

本文从 NAT 原理出发，详细介绍了不同 NAT 类型的工作流程和原理，在此基础上我们深入学习和实现了 锥型 NAT 的穿透，并拓展介绍了一些特殊的穿透场景。

NAT 的出现极大的缓解了 IPv4 地址短缺，同时也延迟了 IPv6 的推广，但 IPv6 是大势所趋，未来使用 NAT 的场景可能会慢慢减少；但无论怎样， NAT 的原理和策略都非常值得我们学习，比如：1.NAT 是一个天然的防火墙，2.NAT 其实可以看作是代理服务器，3.NAT 可以作为负载均衡服务器，4. 等等。

References:  
_https://en.wikipedia.org/wiki/Network_address_translation  
https://tools.ietf.org/html/rfc1631  
https://tools.ietf.org/html/rfc2663  
https://tools.ietf.org/html/rfc3022  
https://tools.ietf.org/html/rfc7857  
https://www.cnblogs.com/GO-NO-1/p/7241556.html  
http://xdxd.love/2016/10/18 / 对称 NAT 穿透的一种新方法 /_

_https://tools.ietf.org/html/rfc3489  
https://www.cnblogs.com/monjeo/p/9394825.html  
http://midcom-p2p.sourceforge.net/draft-ford-midcom-p2p-01.txt  
https://www.linkinstar.wiki/2020/04/25/network/nat/  
https://bford.info/pub/net/p2pnat/index.html  
https://stackoverflow.com/questions/39545461/tcp-based-hole-punching  
https://github.com/samyk/pwnat  
http://samy.pl/pwnat/pwnat.pdf_

_http://tutorials.ptnetacad.net/tutorials80.htm  
https://help.cisco.yueplus.ink/Simplified%20Chinese/index.htm  
https://so.csdn.net/so/search/blog?q=packet&t=blog&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=gengkui9897_

![](https://mmbiz.qpic.cn/mmbiz_gif/3k9IT3oQhT0Z79Hq9GCticVica4ufkjk5xiarRicG97E3oEcibNSrgdGSsdicWibkc8ycazhQiaA81j3o0cvzR5x4kRIcQ/640?wx_fmt=gif)

**往 期 热 门**

(点击图片跳转)

[![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1icVJtykEDjXcJpn5q0VicfGzCuwp3EUQGCyaghjx3QZXaQ98gUUC4rZl1dlV5FduJib1TEukpmzQ7A/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzAxNDY2MTQ2OQ==&mid=2650947055&idx=1&sn=0ba26e71b2bd54dae35c5d602089ef6b&chksm=80797fddb70ef6cbda658450c30f410d50485ea603afe5518ec4cc0133c00f132d794987eb28&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3Y2cicicsLic7K5nAuuhcQymGPV7f8bFc3MBmZaymo8lW59A92DFzE3EsmjdoaCyQOl3ZK80ib4rklMg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzAxNDY2MTQ2OQ==&mid=2650946879&idx=1&sn=bbbbcf997021b0f8fcb5fc7f10c30815&chksm=80797f0db70ef61bdbde86a4f20eed8aa3d2b041e3468509752e846c8d53005d5a57016b739f&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT3d0oEibxrLd9GS6db3OCJNq6ekHQX3ib6SgR8ccCC5jdvRM7icicNRHOYia4efric1Qdc6AUFB7HvLHD5w/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzAxNDY2MTQ2OQ==&mid=2650946446&idx=1&sn=683e0486d60873b132a5746e12d54aaa&chksm=807979bcb70ef0aa0090a9416c11c762d4e76f4de4662cd00122b1702ed3da911840d2650dc8&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/3k9IT3oQhT0Z79Hq9GCticVica4ufkjk5xK8te0JrCrcOiatDWNPRndZzq1N80rlbyxU9bGuTvekqEGu5utyHqicicw/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT09IJjs3wGQbICd50va8zMqN2SkNrrQyWIiaCQvodo60ZfrQIhWic0TSeglsSGiboXx1wjbOxwdu5jQw/640?wx_fmt=jpeg)

**觉得不错点个 “在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**