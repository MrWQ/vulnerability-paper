> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247483903&idx=1&sn=b95ed788d07f3df23d6ca04871f80387&chksm=eaad81c2ddda08d4d941edd00f85f6bb4015774d2897ca79b031466b39cec28adc1e8c06c65a&scene=21#wechat_redirect)

**目录**

  

Shodan

*   Shodan 工作原理
    
*   Shodan 的使用
    
*   使用搜索过滤
    
*   Kali 中安装 Shodan
    
*   Kali 中 Shodan 的使用
    

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HzZrTT4UZAcukC3cKqetSHpGJABL8ZCM8yibLyNpvY2Zia3IAY3P6yE9A/640?wx_fmt=gif)

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7H2bowpqCQLXiczqD2rfB49Avt1ucibvLB4q9MAuuhkvWv8hKVicVV1LEWTpLjIPm2yK65AmQiaX2OnA/640?wx_fmt=png)

  

Shodan 是一个搜索引擎，但它与 Google 这种搜索网址的搜索引擎不同，Shodan 是用来搜索网络空间中在线设备的，你可以通过 Shodan 搜索指定的设备，或者搜索特定类型的设备，其中 Shodan 上最受欢迎的搜索内容是：webcam，linksys，cisco，netgear，SCADA 等等。

Shodan 工作原理

那么 Shodan 是怎么工作的呢？Shodan 通过扫描全网设备并抓取解析各个设备返回的 banner 信息，通过了解这些信息 Shodan 就能得知网络中哪一种 Web 服务器是最受欢迎的，或是网络中到底存在多少可匿名登录的 FTP 服务器，或者哪个 ip 对应的主机是哪种设备。

在 windows 系统上访问 Shodan 只需要访问链接：https://www.shodan.io/

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HoaHEjBLqmAGrZlH8BTIAaGKt4xLxqt7gEL9Jj00Y7u9ic8Xy6EYiaVBQ/640?wx_fmt=gif)

Shodan 的使用

我们在左上角输入我们要搜索的关键字，然后下面就出来搜索结果了。比如我们搜索 SSH

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvArVIxh7QsKLagsyibwsIp6sl5lLqpmTesHzJbfTficLcona2z8LLjVpw/640?wx_fmt=png)

上图的搜索结果包含两个部分，左侧是大量的汇总数据包括：

· Results map – 搜索结果展示地图

· Top services (Ports) – 使用最多的服务 / 端口

· Top organizations (ISPs) – 使用最多的组织 / ISP

· Top operating systems – 使用最多的操作系统

· Top products (Software name) – 使用最多的产品 / 软件名称

随后，在中间的主页面我们可以看到包含如下的搜索结果：

· IP 地址

· 主机名

· ISP

· 该条目的收录收录时间

· 该主机位于的国家

· Banner 信息

想要了解每个条目的具体信息，只需要点击每个条目下方的 details 按钮即可。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxv1EQ9D9zlnKNPC22brQicmmUaAbguicU43Prey3o6sRf5CgCiaY34XMcDA/640?wx_fmt=png)

我们还可以点击 Exploits ，Shodan 就会帮我们查找针对不同平台、不同类型可利用的 exploits。当然也可以通过直接访问网址来自行搜索：https://exploits.shodan.io/welcome；

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxv65P8gIPow0XBeqicp0bynibm5EjiazNTw1NkQ7XYE9ep68wHgLRpbguxA/640?wx_fmt=png)

我们还可以点击 Maps，查看设备分布的地图

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvq0TPibv4e35VaicvVucGAZV5CwXReIqwaEz6cGgCe4rIicyRlBu2s1R7g/640?wx_fmt=png)

如果我们想生成报表，我们可以点击 Create Report

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvNmL5fiaDakMl0G9yERuypb7z5AXp1srMNl3fdhDdqvaAqIGMDrnLDbA/640?wx_fmt=png)

我们还可以直接点击 Explore ，看网络上其他用户使用最多的搜索

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvczupoKcyprds3vicYYdJ8ib8Le0ol5qIN9FCcibPw0bhHiayaOrWK0zsibA/640?wx_fmt=png)

如果像前面单纯只使用关键字直接进行搜索，搜索结果可能不尽人意，那么此时我们就需要使用一些特定的命令对搜索结果进行过滤

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HoaHEjBLqmAGrZlH8BTIAaGKt4xLxqt7gEL9Jj00Y7u9ic8Xy6EYiaVBQ/640?wx_fmt=gif)

使用搜索过滤

· **hostname**：搜索指定的主机或域名，例如 hostname:"google"

· **port**：搜索指定的端口或服务，例如 port:"21"

· **country**：搜索指定的国家，例如 country:"CN"

· **city**：搜索指定的城市，例如 city:"Hefei"

· **org**：搜索指定的组织或公司，例如 org:"google"

· **isp**：搜索指定的 ISP 供应商，例如 isp:"China Telecom"

· **product**：搜索指定的操作系统 / 软件 / 平台，例如 product:"Apache httpd"

· **version**：搜索指定的软件版本，例如 version:"1.6.2"

· **geo**：搜索指定的地理位置，参数为经纬度，例如 geo:"31.8639, 117.2808"

· **before/after**：搜索指定收录时间前后的数据，格式为 dd-mm-yy，例如 before:"11-11-15"

· **net**：搜索指定的 IP 地址或子网，例如 net:"210.45.240.0/24"  

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HoaHEjBLqmAGrZlH8BTIAaGKt4xLxqt7gEL9Jj00Y7u9ic8Xy6EYiaVBQ/640?wx_fmt=gif)

Kali 中安装 Shodan

Shodan 是由官方提供的 Python 库

安装命令：

```
git clone https://github.com/achillean/shodan-python.git && cd shodan-python

python setup.py install
```

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HoaHEjBLqmAGrZlH8BTIAaGKt4xLxqt7gEL9Jj00Y7u9ic8Xy6EYiaVBQ/640?wx_fmt=gif)

Kali 中 Shodan 的使用

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvVb0q5iauMa0pwiciaWiakbQ4XLR3wZ6rnw1OvUfNYImkxYMI1ygl8KAVAQ/640?wx_fmt=png)

```
Commands:
  alert       Manage the network alerts for your account  # 管理账户的网络提示
  convert     Convert the given input data file into a...  # 转换输入文件
  count       Returns the number of results for a search  # 返回查询结果数量
  download    Download search results and save them in a...  # 下载查询结果到文件
  honeyscore  Check whether the IP is a honeypot or not.  # 检查 IP 是否为蜜罐
  host        View all available information for an IP...  # 显示一个 IP 所有可用的详细信息
  info        Shows general information about your account  # 显示账户的一般信息
  init        Initialize the Shodan command-line  # 初始化命令行
  myip        Print your external IP address  # 输出用户当前公网IP
  parse       Extract information out of compressed JSON...  # 解析提取压缩的JSON信息，即使用download下载的数据
  scan        Scan an IP/ netblock using Shodan.  # 使用 Shodan 扫描一个IP或者网段
  search      Search the Shodan database  # 查询 Shodan 数据库
  stats       Provide summary information about a search...  # 提供搜索结果的概要信息
  stream      Stream data in real-time.  # 实时显示流数据
```

   初始化 Shodan：shodan  init   API_Key

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvY72YF6qVeyk26UCica7ZdzatmBUcT72Hwy2Btaia85hibJlRGrIaP4SIw/640?wx_fmt=png)

   返回查询结果的数量：shodan  count  SSH

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvXGK2ShARYqzicvWh9ib0VJniaN532wNeOU9srSjCv4fCBA4HyONADUgQw/640?wx_fmt=png)

将查询到的结果下载：shodan  download  microsoft-data microsoft iis 6.0  。将搜索结果下载到  ssh-data 文件中，文件中的每一行都是 JSON 格式存储的目标 banner 信息。默认情况下，该命令只会下载 100 条结果。如果我们想获取更多的结果，需要我们花钱注册，然后下载的时候指定 --limit 参数。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvMGfoogMnEGm8vUKpwqda7ibfuLsdvf2ufKJC9sPtM6hianH0NR8ibNNKA/640?wx_fmt=png)

解析下载的数据：shodan parse --fields ip_str,port,org --separator , microsoft-data.json.gz![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvhA0zHyP6I0OdIKjHE7G7PdWGtDmnh1UHJBUevBUxtd9Hx757KCwicoQ/640?wx_fmt=png)

查看指定主机的相关信息，如地理位置信息，开放端口，甚至是否存在某些漏洞等信息。![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvxjbKf6c7IRfpCR9wf53xdQvywW8hnQnTlq0uaO6lgx4n3PUezoXOjg/640?wx_fmt=png)

shodan  search  microsoft iis 6.0

search 查找，直接将查询结果展示在命令行中，默认情况下只显示 IP、端口号、主机名和 HTTP 数据![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvFNykj23xia7mNiagpSV6waDMicibDX1LjKZTYGpj1uNicEePx6FYGWrcFhA/640?wx_fmt=png)

当然我们也可以通过使用 –fields 来自定义显示内容，例如，我们只显示 IP、端口号、组织名称和主机名：

shodan search --fields ip_str,port,org,hostnames microsoft iis 6.0![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvnLS65H6lxNDdxYhw29TSAibWXJEnW1UCDVSzTtTwO0JYt9omjD1PJkA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvAKOaVnz60hOe7y3wAHiclddyK53lpEKIQlx4DKOq6EojHibVicgibDB2aQ/640?wx_fmt=gif)

来源：谢公子的博客

责编：梁粉

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)