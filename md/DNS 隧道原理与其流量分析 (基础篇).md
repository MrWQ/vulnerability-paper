> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Hxf73WjspCUK8IriiK3CWA)

**前言：**

因工作需要，最近正在出 XX 局应急响应方面的题。其中某个题便考察了某个 APT 组织利用 DNS 隧道对政府、金融、能源、电信等行业进行攻击的场景。实话讲，一听到与 DNS 流量有关的内容，脑子里就乱乱的，总感觉很麻烦。根本原因就是对 DNS 协议这块理解还不透彻。百度，谷歌找了一堆资料，但总感觉还是看不太懂。所以，打算静下心来好好整理整理，希望可以对初学者一个帮助。(PS：下文中参考资料的段落基本上都进行了语句调整与优化，毕竟原理性的东西我不能乱写，只能引用了)

我愿称 PPT 为最强，画图真的太好使了，等哪天练练，我也画个柯南出来，哈哈哈。

经测试，本文在手机上浏览时排版可能不是特别好，会出现文字间距特别大的情况，如果想仔细好好看的话建议通过电脑微信访问该链接。

文章主体目录如下：

**一、DNS 协议概述**

****二、DNS 报文解析****

******三、DNS 工作原理******

**********四、********************DNS 隧道工作原理**********

**********五、********************DNS 隧道搭建**********

**********六、********************DNS 隧道恶意流量分析**********

在本文的基础篇中，会主要讲解前三个主题的内容，在后续的进阶篇中会重点讲解后续的三个主题。

**一、DNS 协议概述**

**DNS**(**D**omain **N**ame **S**ystem) 是互联网的一项服务。它作为将**域名**和 **IP 地址**相互映射的**分布式数据库**，能够使人更方便的访问互联网。DNS 使用 TCP 53 和 UDP 53 端口。当前每一级域名长度的限制是 63 个字符，域名总长度不能超过 253 个字符。 [1]

DNS 域名系统好比是一个 Internet 电话簿，人们通过例如 baidu.com 或 google.com 等域名在线访问信息。Web 浏览器通过 Internet 协议 (IP) 地址进行交互。DNS 将域名转换为 IP 地址，以便浏览器能够加载 Internet 资源。连接到 Internet 的每个设备都有一个唯一 IP 地址，其他计算机可使用该 IP 地址查找此设备。DNS 服务器使人们无需存储例如 192.168.1.1(IPv4 中)等 IP 地址或更复杂的较新字母数字 IP 地址，例如 2400:cb00:2048:1::c629:d7a2(IPv6 中)。 [2]

简单来说就是 IP 地址面向主机，域名面向用户。

**二、DNS 报文解析**

查了很多关于 DNS 报文格式的文章，其中不乏出现各种花里胡哨的名词。比如：标识数，标识，标志，事务 ID，问题计数，回答资源记录，授权资源记录等等。基本上换一篇文章就能看到几个新名词，尽管都是说的同一个东西。也许这就是让我感到头疼的原因吧。好乱，好乱。这应该就是每个人翻译不同导致的吧。例如，**_Identification_** 与 **_Flags_**、**_标识_**与**_标志_** 。你品，你细品。明明相差这么多的两个名词，翻译过来后，却有种模棱两可的感觉。所以下面的部分名词就不翻译了，直接采用英文表示。

DNS 只有两种报文格式：**Queries(查询) 报文**和 **Replies(响应) 报文。**这两种报文具有相同的格式。这两种报文都包含 1 个 **Header** 和 4 个 **Sections**。这 4 个 **Sections** 分别是：**_Question Section_**、**_Answer Section_**、**_Authority Section_**、**_Additional Section_**。**Header** 部分中的 Flags 控制着这 4 个 **Sections** 的内容。

**Header** 部分包含以下 6 个字段：

_Identification_、_**Flags**、**Number of Questions**、**Number of Answers**、__**Number of authority resource records (RRs)**、_**Number of additional RRs**_。_

这 6 个字段每个都是 16bit 长，并按照指定的数据进行排列。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1VlLwh2cNJd1GU1Z1WSPPemCP0lxiaSBRa1qRicyAYr9afOSnjhyVjfIia9Q/640?wx_fmt=png)

**(1)****Identification** 字段：DNS 报文的 ID 标识 (Transaction ID)。对于 **Queries(查询) 报文**和其 **Responses(响应) 报文**，该字段的值是相同的。通过它可以区分 DNS **Responses(响应) 报文**是对哪个查询请求进行的响应。

**(2)****Flags** 字段：**_Flags_** 字段包含多个子字段。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1Vl6lEMvmxKyicuZlC7AULWiakmvCTib5dUmISR83k3wP32qL0Q2BKnvl54g/640?wx_fmt=png)

各子字段的功能如下：

*   **QR：**表示该报文的类型**。**0 表示 **Queries(查询) 报文**，1 表示 **Responses(响应) 报文**。
    
*   **OPCode：****OPCode** 的类型可以是 QUERY、IQUERY 或 STATUS。其中，0 表示 **Standard Query(标准查询)**，1 表示 **Inverse Query(反向查询)**，2 表示 **Server Status Request(服务器状态请求)**。
    
*   **AA：Authoritative Answer，**权威应答，用来指示 DNS 服务器对于查询的主机名是否具有权威性。该字段仅在响应报文中有效。值为 0 时，表示_名称服务器_不是权威服务器；值为 1 时，表示_名称服务器_ [3] 是权威服务器。
    
*   **TC：TurnCation**，截断标志位。用来指示此消息由于长度过长而被截断。以响应消息为例：值为 0 时，表示此响应消息未被截断；值为 1 时，表示此响应消息已超过 512 字节并被截断，只返回前 512 个字节的内容。
    
*   **RD：Recursion Desired**，期望递归。表示客户端是否希望使用递归查询。值为 0 时，且请求的域名服务器没有一个授权回答，服务器则会返回一个能解答该查询的其他名称服务器列表，以供客户端自己去其他名称服务器查询到正确的结果，这种方式称为**迭代查询** [4]；值为 1 时，表示客户端期望使用**递归查询** [4]，这会告诉服务器必须处理完这个查询，并返回给客户端查询结果。
    
*   **RA：Recursion Available**，递归可用性。表示可用的 DNS 服务器是否支持递归查询。该字段仅出现在响应报文中。值为 0 时，表示服务器不支持递归查询；值为 1 时，表示服务器支持递归查询。(大多数名称服务器都提供递归查询，部分根服务器不提供递归查询)
    
*   **Z：Zero，**保留字段。保留以备将来使用。它的值必须为 0。
    
*   **RCode：Response code**，响应代码。值为 0 时，表示没有错误 (No error)；值为 1 时，表示报文格式错误 (Format error)，服务器不能理解请求的报文；值为 2 时，域名服务器失败 (Server failure)，因为服务器的原因导致无法处理这个请求；值为 3 时，表示域名不存在错误 (Non-Existent Domain)，仅对授权域名解析服务器有意义，指出解析的域名不存在。值为 4 时，表示查询类型不支持 (Not Implemented)，即域名服务器不支持此类查询类型；值为 5 时，表示查询被拒绝 (Query Refused)，一般是服务器由于设置的策略拒绝给出应答。
    

**(3)****Number of Questions** 字段：该字段表示 DNS 查询请求的数目。

**(4)****Number of Answers** 字段：该字段表示 DNS 查询后响应的数目。

**(5)****Number of authority resource records (RRs) [6]** 字段：**Authority RRs** 是 NS 类型的记录，指向名称服务器。该字段故可表示为权威名称服务器资源数目。(RRs 即 Resource Records)

**(6)****Number of additional RRs [6]** 字段：**Additional** RRs 是名称服务器认为可能对客户端有用的记录。该字段表示附加资源记录数。此字段最常用的用途是列出名称服务器的 A 地址记录数目，可以理解为权威名称服务器对应 IP 地址的数目。

以上 6 个主要字段在 WireShark 中抓包显示结果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1Vl9otp7icicGegKGFdPQuNRdHVAOyibiaB0EdN3CR7EEiaxY0xM3Z2lIic0kSA/640?wx_fmt=png)

```
Domain Name System (query)
    Transaction ID: 0x66cc         #DNS报文的ID标识
    Flags: 0x0100 Standard query   #Flags字段
        0... .... .... .... = Response: Message is a query            #QR字段：值为0，故是一个查询报文
        .000 0... .... .... = Opcode: Standard query (0)              #OPCode字段：值为0，故是标准查询
        .... ..0. .... .... = Truncated: Message is not truncated     #TC字段：值为0，故此消息未被截断
        .... ...1 .... .... = Recursion desired: Do query recursively #RD字段：值为1，表示期望递归查询
        .... .... .0.. .... = Z: reserved (0)                         #Z字段：保留字段，值为0
        .... .... ...0 .... = Non-authenticated data: Unacceptable    
    Questions: 1       #表示DNS查询请求的数目为1个
    Answer RRs: 0      #表示DNS查询后响应的数目为0个
    Authority RRs: 0   #表示权威名称服务器资源数目为0个
    Additional RRs: 0  #表示附加资源记录数为0个
    Queries
    [Response In: 276]
```

下面继续介绍剩下的 4 个 **Sections**：

**_Question Section_**、**_Answer Section_**、**_Authority Section_**、**_Additional Section_**。

**_Question Section_：**

DNS 查询始终在 **_Question Section_** 中包含至少一个条目，这个条目指定了客户端想要查询的信息。下图为 **_Question Section_** 部分中每个条目所通用的格式：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1VltPyESZ8vGiczHUDA3h3icxY23M61HPtibKibhDiaiaud7bgPme6U9FaQbI1Q/640?wx_fmt=png)

**(1)_Question Names_** 字段：查询名，该字段一般为要查询的域名 (有时也会是 IP 地址，用于反向查询)，该字段的长度并不固定。

**(2)_Question Type_** 字段：查询类型，该字段表示 DNS 查询请求的资源类型，常见的查询类型如：A、AAAA、MX、TXT 等。通常查询类型为 A 类型，表示由要查询的域名获取对应的 IP 地址。(后面在 **“DNS 工作原理”** 一小节中会详细讲到这些 DNS 查询类型)。

**(3)_Question Class_** 字段：查询类，该字段表示 DNS 查询请求的地址类型。通常该字段的值为 1 (IN)，表示互联网地址。

**_Question Section_** 字段在 WireShark 中抓包显示结果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1VlPfJwxGexZGd4LpDic5NJgNklFOoUdgSoS1fLn0l6xc6aCWhCicIFdHfw/640?wx_fmt=png)

```
Domain Name System (query)              #查询请求
    Transaction ID: 0x0509
    Flags: 0x0100 Standard query
    Questions: 1
    Answer RRs: 0
    Authority RRs: 0
    Additional RRs: 0
    Queries                              #Question Section
        www.baidu.com: type A, class IN  #Question Name字段，这里请求的域名是www.baidu.com
            Name: www.baidu.com          
            [Name Length: 13]
            [Label Count: 3]
            Type: A (Host Address) (1)   #Question Type字段，这里请求类型是A类型。表示希望获取该域名的IP地址
            Class: IN (0x0001)           #Question Class字段，这里Class的值为1。表示这里的地址为互联网地址
    [Response In: 549]
```

后面剩下的 **_Answer Section、**_Authority Section、**_Additional Section_**_**_** 被统称为 **Resource Records Section(资源记录部分)**。这三个 **Section** 均采用一种称为 **Resource Record**(资源记录) 的格式。格式如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1VlN8tCwmcS0svxQical3KdAOq6xicskUZpKZ3RsB7E5FAcrmA3VZRRNVoA/640?wx_fmt=png)

各字段的功能如下：

**(1)_Name_** 字段：包含作为资源记录主题的对象 (Object)，域名(Domain) 或区域名称(Zone name)。通常指表示为请求的域名。

**(2)**_Type_ 字段：表示资源记录的类型。与 _Question_ _Section_ 中的 _Type_ 字段的类型值一致。

**(3)**_**Class**_ 字段：表示资源记录的类。与 **_Question_ _Section_** 中的 **_Class_** 字段的类一致。

**(4)_Time To Live(TTL)_** 字段：表示资源记录的生命周期，以秒为单位。一般用于当域名地址解析协议取出资源记录后决定保存及使用缓存数据的时间。

**(5)_Resource Data Length_** 字段：表示资源记录数据部分 (Resource Data) 的长度。

**(6)_Resource Data_** 字段：资源记录的数据部分。

**Resource Records Section****(资源记录部分)** 只有在 DNS 响应包中才会出现。在 WireShark 中抓包显示结果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1Vl2q6r2eSDt0M6PAv5r9xx3Ngqo5CuNKubEBrbBfdz9uK9Ltnbqfkzjw/640?wx_fmt=png)

_Answer Section_ 字段的资源记录部分信息如下：  

```
Answers                                                 #Answer Section字段

    baidu.com: type A, class IN, addr 220.181.38.148    #资源记录部分(1)
        Name: baidu.com                                 #Name字段，请求的域名为baidu.com。
        Type: A (Host Address) (1)                      #Type字段，表示资源记录的类型为A记录。
        Class: IN (0x0001)                              #Class字段，该字段的值为1 (IN)，表示互联网地址。
        Time to live: 253 (4 minutes, 13 seconds)       #表示资源记录的生命周期，以秒为单位。这里为4分钟13秒。
        Data length: 4                                  #资源记录数据部分(Resource Data)的长度。
        Address: 220.181.38.148                         #资源数据, 这里为IP地址220.181.38.148。

    baidu.com: type A, class IN, addr 39.156.69.79      #资源记录部分(2)
        Name: baidu.com                                 #Name字段，请求的域名为baidu.com  
        Type: A (Host Address) (1)                      #Type字段，表示资源记录的类型为A记录。
        Class: IN (0x0001)                              #Class字段，该字段的值为1 (IN)，表示互联网地址。
        Time to live: 253 (4 minutes, 13 seconds)       #表示资源记录的生命周期，以秒为单位。这里为4分钟13秒。
        Data length: 4                                  #资源记录数据部分(Resource Data)的长度。
        Address: 39.156.69.79                           #资源数据, 这里为IP地址39.156.69.79。
```

其中，Name 的值为 baidu.com，表示 DNS 请求的域名为 baidu.com；Type 的类型为 A，表示要获取该域名对应的 IP 地址。Address 的值显示了该域名对应的 IP 地址。这里获取到了 2 个 IP 地址，分别为 220.181.38.148 和 39.156.69.79。

_Additional Section_ 字段的资源记录部分信息如下：

```
Additional records                              #Additional Section字段

    <Root>: type OPT                            #资源记录部分(1)
        Name: <Root>                            #Name字段，MUST be 0 (root domain) 
        Type: OPT (41)                          #Type字段，表示资源记录的类型为OPT记录(这是专门为EDNS创建的新型DNS记录)。
        UDP payload size: 512                   #请求者的UDP有效负载大小为512bit。
        Higher bits in extended RCODE: 0x00     #扩展的RCODE和Flags
        EDNS0 version: 0
        Z: 0x0000
        Data length: 0
PS：详细说明请参考 Extension Mechanisms for DNS (EDNS(0))  [7]
```

**Authority Section** 字段的资源记录部分信息如下：  

```
Authoritative nameservers                               #Authority Section字段

    baidu.com: type NS, class IN, ns ns2.baidu.com      #资源记录部分(1)
        Name: baidu.com                                 #Name字段，请求的域名为baidu.com。
        Type: NS (authoritative Name Server) (2)        #Type字段，表示资源记录的类型为NS记录。
        Class: IN (0x0001)                              #Class字段，该字段的值为1 (IN)，表示互联网地址。
        Time to live: 5                                 #表示资源记录的生命周期，以秒为单位。这里为5秒
        Data length: 6                                  #资源记录数据部分(Resource Data)的长度。
        Name Server: ns2.baidu.com                      #资源数据, 这里为权威名称服务器即ns2.baidu.com。

    baidu.com: type NS, class IN, ns dns.baidu.com      #资源记录部分(2)
        Name: baidu.com                                 #Name字段，请求的域名为baidu.com。
        Type: NS (authoritative Name Server) (2)        #Type字段，表示资源记录的类型为NS记录。
        Class: IN (0x0001)                              #Class字段，该字段的值为1 (IN)，表示互联网地址。
        Time to live: 5                                 #表示资源记录的生命周期，以秒为单位。这里为5秒
        Data length: 6                                  #资源记录数据部分(Resource Data)的长度。
        Name Server: dns.baidu.com                      #资源数据, 这里为权威名称服务器即dns.baidu.com。
PS: 该部分本地复现时未抓取到携带该Authority Section字段的流量包，故借用该网站的演示数据进行说明。[8]
```

其中，Name 的值为 baidu.com，表示 DNS 请求的域名为 baidu.com；Type 的类型为 NS，表示要获取该域名的权威名称服务器名称。Name Server 的值显示了该域名对应的权威名称服务器名称。这里总共获取到了 2 个，如 ns2.baidu.com。

**三、DNS 工作原理**

### 1.Hosts 文件

在引入 **DNS**(域名系统) 之前，网络中的主机是将容易记忆的域名映射到 IP 地址并将它保存在一个共享的静态文件 **Hosts** 中，再由 hosts 文件来实现网络中域名的管理。

最初的 Internet 非常小，仅使用这个集中管理的 **hosts** 文件就可以通过 FTP 为连入 Internet 的站点和主机提供域名的发布和下载。每个 Internet 站点将定期地更新其主机文件的副本，并且发布主机文件的更新版本来反映网络的变化。

但是，当 Internet 上的计算机迅速增加时，通过一个中心授权机构为所有 Internet 主机管理一个主机文件的工作将无法进行。**Hosts** 文件会随着时间的推移而增大，这样按当前和更新的形式维持文件以及将文件分配至所有站点将变得非常困难，甚至无法完成，于是便产生了 DNS 服务器。

按照操作系统的规定，在进行 DNS 请求以前，会先检查自己的 **Hosts** 文件中是否有这个域名和 IP 的映射关系。如果有，则直接访问这个 IP 地址指定的网络位置；如果没有，再向已知的 DNS 服务器提出域名解析请求。也就是说 **Hosts** 文件内的 IP 解析优先级比 DNS 服务器要高。 **[9]**

### 2.DNS 域名空间 **[10]**

由于因特网的用户数量较多，所以因特网在命名时采用的是**层次树状结构**的命名方法。任何一个连接在因特网上的主机或路由器，都有一个唯一的层次结构的名字，即**域名 (domain name)**。这里，**域 (domain)** 是名字空间中一个可被管理的划分。从语法上讲，每一个域名都是有**标号 (label) 序列**组成，而各标号之间用**点 (.)** 隔开。域名可以划分为各个子域，子域还可以继续划分为子域的子域，这样就形成了**根域**、**顶级域**、**二级域**、**子域**、**主机**等。

需要注意的是，域名系统必须要保持唯一性。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1VlQHIzVh0rEjbib2fKgMMWqvpUdanSjt5svW4mtCwib46UQkszX4dsdVnA/640?wx_fmt=png)

#### (1) 根域

这是 DNS 的最上层，根域用 “**.**” 表示。当下层的任何一台 DNS 服务器无法解析某个 DNS 名称时，便可以向根域的 DNS 寻求助。理论上讲，只要所查找的主机是按规定注册的，那么无论它位于何处，从根域的 DNS 服务器往下层查找，一定可以解析出其 IP 地址。

#### (2) 顶级域

顶级域处于根域的下一层。一般代表一种类型的组织机构或国家地区。

早期的顶级域只有 6 个：com、net、org、edu、gov、mil。每个顶级域都有预设的用途，例如 com 域名用于商业公司，edu 域名用于教育机构，gov 域名用于政府机关等。由于互联网诞生于美国，起初只有美国的公司或组织在顶级域下面申请二级域名，后来互联网走向了全世界，其他国家的公司或组织也需要注册二级域名，所以这 6 个顶级域就被分为两类:

*   国际通用的顶级域：net、com、org。
    
*   美国专用的顶级域：edu、gov、mil。
    

世界上所有国家的组织或个人都可以在国际通用顶级域名下面注册，而美国专用的顶级域名则只有美国的组织或个人可以使用。

随着互联网上的网站越来越多，只有 3 个国际通用顶级域就无法满足需求了。所以后来就为每个国家都单独设置了一个顶级域，这就是国家 (地区) 顶级域，如 cn 代表中国， uk 代表英国，jp 代表日本等。国家 (地区) 顶级域名为每个国家所专有，只有该国的组织或个人可在其下面注册。

目前又出现了很多新的顶级域，如 top、vip、xyz 等，不过使用最多、影响力最大的依然是传统的 3 个国际通用顶级域，以及国家 (地区) 顶级域。

#### (3) 二级域

二级域处于顶级域的下一层。一般代表顶级域内的一个特定的组织。

国际通用顶级域下面的二级域由 ICANN 负责管理，国家顶级域下面的二级域名则是由所在国家的网络部门统一管理，例如中国互联网管理中心在 cn 顶级域名下面又设置了一些二级域：com.cn、net.cn、edu.cn 等。

#### (4) 子域

在二级域之下所创建的各级域统称为子域，各个组织或用户都可以在子域中自由申请注册自己的域名。

域名结构理论上最多可以有 127 级，但通常最多使用到三级域，例如, 域名 "apple.com.cn" 就是一个三级域。

#### (5) 主机

主机处于域名空间的最下面一层，也就是一台具体的计算机。

如上图中的 www、 mail、app 都是具体的计算机的名字，我们可以用 **www.baidu.com.**、**mail.baidu.com.**、**app.baidu.com.** 来表示它们，这种表示方式称为 FQDN 名 (完全合格域名)，也就是这台主机在域中的全名。我们平时上网时所输入的网址也都是一些 FQDN 名，如 www.baidu.com，其实就是表示我们要访问 "baidu.com" 域中一台名为 "www" 的计算机。

DNS 服务器的作用就是将每个域中的 FQDN 名解析为这些计算机所对应的 IP 地址，以使用户可以通过名字访问它们。在一般的网络应用中，FQDN 名最右侧的点可以省略，但在 DNS 服务器配置中这个点不能随便省略。因为这个点代表了 DNS 的根，有了这个点，完全合格域名就可以表达为一个绝对路径，去掉了点则会出现问题。

##### 以 "www.apple.com.cn." 为例：

*   "**.**"：是根域。
    
*   "**.cn**"：是顶级域名。
    
*   ".**com.cn**"：是二级域名。
    
*   "**.apple.com.cn**"：是三级域名。
    
*   "**www.apple.com.cn**"：是该域中的一台名为 www 的主机。
    

### 3.DNS 域名解析过程 

域名是分层结构，域名 DNS 服务器也是对应的层级结构。有了域名结构，还需要有域名 DNS 服务器去解析域名，且是需要由遍及全世界的域名 DNS 服务器去解析，域名 DNS 服务器实际上就是装有 DNS 域名系统的主机。域名解析过程涉及 4 种 DNS 服务器 **[12]**，分别如下：

### (1) 根 DNS 服务器

本地域名服务器在本地查询不到解析结果时，第一步则会向根 DNS 服务器进行查询，并获取顶级域名服务器的 IP 地址。

#### (2) 顶级域名服务器

顶级域名服务器负责管理在该顶级域名下注册的二级域名，例如 "**baidu.com**"。".**com**"则是顶级域名服务器的域名，在向它查询时，可以返回二级域名"**baidu.com**" 所在的权威域名服务器的地址。

#### (3) 权威域名服务器

权威名称服务器在特定区域内具有唯一性，负责维护该区域内的域名与 IP 地址之间的对应关系。

#### (4) 本地域名服务器

本地域名服务器是响应来自客户端的递归请求，并最终跟踪直到获取到解析结果的 DNS 服务器。

总结：每个层的域名上都有自己的域名服务器，最顶层的是根域名服务器。每一级域名服务器都知道下级域名服务器的 IP 地址，以便于一级一级向下查询。

DNS 服务器是如何进行域名解析的? 假设域名 apple.com.cn 被指定由 IP 地址为 114.114.114.100 的 DNS 服务器负责解析这个域名，那么其他的 DNS 服务器是怎么知道由 114.114.114.100 负责解析 apple.com.cn 域名的呢?

现有一个互联网用户想解析 www.apple.com.cn **[10]**，其解析过程如下所示：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Ucv7hK1VZ1ygPe0Xiaceib1Vl9shickicQc3HAgicMtMXokQ85icVhiaaxjF4D73cMcrCQwZdIN0jc5qjQtw/640?wx_fmt=png)

**(1)** 客户端首先会查询本地的 **Hosts** 文件，因为本地的 **Hosts** 文件中不存在 "www.apple.com.cn" 对应的 IP 地址信息，所以，会把解析请求发送到本机设置的首选 DNS 服务器上 (也可称之为**本地域名服务器**)，本地域名服务器发现自己无法解析 "www.apple.com.cn" 这个域名，所以就会将这个解析请求发送到**根 DNS 服务器**。

**(2)** **根 DNS 服务器**知道这个域名是以 "**.cn**"结尾的，于是便告诉本地域名服务器这个域名应该询问负责解析"**.cn**" 的**顶级域名服务器**，并将 "**.cn 服务器** " 的地址返回给**本地域名服务器**。这时**本地域名服务器**就会转而向 "**.cn 服务器** " 发出查询请求。

**(3)**"**.cn 服务器** "同样会将".**com****.cn**" 的**次级域名服务器**的地址返回给本地域名服务器，本地域名服务器则会再向 ".**com****.cn 服务器** " 发出查询请求。

**(4)**".**com****.cn 服务器** "会响应说"**apple.com.cn**"这个域名已经被委派到 DNS 服务器 114.114.114.100 了，因此这个域名的解析应该询问"**apple.com.cn 服务器** "(也可称之为**权威域名服务器**) 即 IP 地址 114.114.114.100。

**(5)** 接着，本地域名服务器最后向 ".**com****.cn 服务器** "发出查询请求，这次查询终于可以如愿以偿，".**com****.cn 服务器** " 会返回查询者所需要的答案。

**(6)** 本地域名服务器拿到这个 IP 和域名的对应关系之后，会在结果返回给客户端的同时，把查询结果放入到自己的缓存中。如果在缓存的有效期内有其他的客户端再次请求这个域名，该本地域名服务器就会利用自己缓存中的结果响应给用户，而不用再去根服务器那里再查询一遍了。

**(7)** 最后，客户端通过本地域名服务器返回的域名对应的 IP 地址成功的访问到域名 "www.apple.com.cn"。

### 4. 递归查询与迭代查询 **[10]**

在上面域名解析的过程中，分别用到了两种不同类型的查询，分别是**用户**和**本地域名服务器**之间的递归查询，以及**本地域名服务器**与**其它 DNS 服务器**之间的迭代查询。

**(1)** **递归查询**：DNS 客户端发出查询请求后，如果本地域名服务器内没有所需的数据，则服务器会代替客户端向其它的 DNS 服务器进行查询。在这种方式中，客户端只需发出一次查询请求，而域名服务器必须要给客户端做出回答。普通上网用计算机和所设置的 DNS 服务器之间都是采用递归查询的方式。

**(2)** **迭代查询**：DNS 服务器与其他服务器之间进行的查询，需要多次反复发出查询请求。也就是上面的例子中，本地域名服务器从根服务器开始逐级往下查询，直到最终找到负责解析 "www.apple.com.cn" 域名的 DNS 服务器为止的过程。

### 5.DNS 记录类型 **[10]**

DNS 记录类型是 DNS 资源和域名之间的映射。每条 DNS 记录都有类型 (名称和编号)、到期时间(存留时间) 和特定类型的数据。

一些常用的记录类型如下：

**(1)** **主机记录 (A 记录)**

将域名指向一个 IPv4 地址。用于描述目标域名与 IPv4 地址的映射关系。

**(2)** **主机记录 (AAAA 记录)**

将域名指向一个 IPv6 地址。用于描述目标域名与 IPv6 地址的映射关系。

**(3)** **别名记录 (CNAME 记录)**

将域名指向另一个域名，用于指定别名。

**(4)** **指针记录 (PTR 记录)**

与 A 记录的作用相反，用于将 IP 地址解析成主机名，即进行反向查询。

**(5)** **邮件交换记录** **(MX 记录)**

用于说明哪台服务器是当前区域的邮件服务器。

**(6)** **名称服务器记录** **(NS 记录)**

用于说明当前区域由哪些域名服务器负责解析。NS 记录是任何一个 DNS 区域都必须要有的记录，而且当前区域中有几台 DNS 服务器，就应相应地设置几条 NS 记录。

**(7)** **起始授权记录** **(SOA 记录)**  

用于说明哪台服务器是当前区域的主域名服务器，同时还定义了一些域的全局参数。如果区域中只有一台 DNS 服务器，那么 SOA 也就是当前服务器。SOA 也是任何一个 DNS 区域都不可缺少的记录，而且每个区域只能有一条 SOA 记录，另外 SOA 记录应位于区域配置文件的起始位置。

**参考引用：**

> [1] 百度百科，域名系统。
> 
> https://baike.baidu.com/item/%E5%9F%9F%E5%90%8D%E7%B3%BB%E7%BB%9F/2251573?fromtitle=DNS&fromid=427444&fr=aladdin

> [2] CloudFlare，什么是 DNS？
> 
> https://www.cloudflare.com/zh-cn/learning/dns/what-is-dns/

> [3] 百度知道，什么是名称服务器？
> 
> https://zhidao.baidu.com/question/303808676.html

> [4] 博客园，迭代查询与递归查询。
> 
> http://cnblogs.com/qingdaofu/p/7399670.html

> [5] DNS 报文 Flags 字段功能，Wikipedia-Domain Name System-DNS message format、知乎 - DNS 协议 (报文解析)、C 语言中文网 - DNS 报文格式解析、百度百科 - DNS 协议、Domain Name System (DNS) Parameters-DNS RCODEs。
> 
> https://en.wikipedia.org/wiki/Domain_Name_System https://zhuanlan.zhihu.com/p/143360037 http://c.biancheng.net/view/6457.html https://baike.baidu.com/item/DNS%E5%8D%8F%E8%AE%AE/1860066 https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-6

> [6] _**Number of authority RRs**、_**Number of additional RRs ，**DNS Protocol Overview、C 语言中文网 - DNS 报文格式解析。
> 
> https://www.freesoft.org/CIE/Topics/77.htm http://c.biancheng.net/view/6457.html

> [7] Extension Mechanisms for DNS (EDNS(0))
> 
> https://tools.ietf.org/html/rfc6891#page-6

> [8] 资源记录部分——权威名称服务器区域字段的资源记录部分信息。
> 
> http://c.biancheng.net/view/6457.html

> [9] 百度百科，Hosts 文件。
> 
> https://baike.baidu.com/item/hosts/10474546?fromtitle=Hosts%E6%96%87%E4%BB%B6&fromid=8971674&fr=aladdin
> 
>   

> [10] 曲广平，《Linux 系统管理初学者指南——基于 CentOS7.6》续篇——DNS 服务配置与管理。

> [11] JavaScript GuideBook，DNS 域名解析系统。
> 
> https://tsejx.github.io/javascript-guidebook/computer-networks/computer-network-architecture/dns