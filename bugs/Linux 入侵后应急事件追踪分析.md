\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/NW6Ti9R1ty\_0gfYehdQBLg)

**0x01 情况概述**
=============

****监控软件监控到服务器存在异常的访问请求，故对此服务器进行安全检查。通过提供的材料发现内网机器对某公网网站存在异常的访问请求，网络环境存在着异常的网络数据的访问情况。针对其服务器进行综合分析发现了病毒文件两例，内网扫描器两例，通过以上的发现证实服务器已被黑客入侵。****

**0x02 取证情况**
=============

### 2.1 目标网络情况

下文中的内网内 ip 以及公网 ip 为替换后的脱敏 ip。

<table width="677"><tbody><tr><th>IP</th><th>所属</th><th>操作系统</th></tr><tr><td>1.168.xxx.xxx</td><td>某业务员服务器</td><td>Linux2.6.32 x86_64 操作系统</td></tr><tr><td>192.168.0.0/24</td><td>DMZ 区</td><td>Linux&amp;windows</td></tr><tr><td>10.10.0.0/24</td><td>核心区</td><td>Linux&amp;windows</td></tr><tr><td><br></td><td>防火墙</td><td><br></td></tr></tbody></table>

### 2.2 针对 xxx 服务器中间件的检测

监测存在异常的服务器开放了 80 端口和 21 端口，安装了 tomcat 中间件。首先进行 tomcat 中间件的排查，查询得知服务器对外开 tomcat 文件夹路径为`/home/XXX/tomcat/XXX _tomcat` ，查询 tomcat 未使用弱密码：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP48ibm4K05nL2RTxUpLII2v8Cp4f8wdLmXmxDj2libAZd3AicYmaibAgoFfg/640?wx_fmt=png)

针对 tomcat 部署服务进行检查，未发现可疑部署组件：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4L463CfVPRibzZxC0gAQb8wlpaWScalzggGyh4EvxWwbwTiaA249Bia5bw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4ov9V6hH8IEkIpcDWIQRDxkAMMN48kY3pAwB8cSu01ibsd6ppxVDbpwA/640?wx_fmt=png)

2.3 针对 xxx 服务器进程及端口的检测

针对目标服务器进行了进程以及端口的检测，发现了可疑现象入下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4UMcqZS5V9Pw6jhAYUPnJBDJAhic7zOIVpqmCibSHSHbRibciagplAO8mwA/640?wx_fmt=png)

发现可疑现象后查找 “l” 所在的路径，入下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4LaVGibn2R9sm7tcGHjuGS9ibsibrjm8cJl1mRx9cpF6Qt6xkhtEQTEJicQ/640?wx_fmt=png)

在 / dev/shm 路径下发现存在 “l” 与“conf.n”文件

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP428Qx4nRVMib8I52KHziaIMXCtttJ3Dgs9PN09bp7b8l3WrNWfGBM9tDA/640?wx_fmt=png)

将 “l” 与“conf.n”下载到本地进行分析，“l”程序为 inux 远控木马 Linux.DDOS.Flood.L，经本地分析 “l” 程序为 linux 下僵尸木马，同时具有远控的功能

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4UOGmbVZq6fxxNlOmGq5tKicQT7DNTPwwLbVa2rOhomCNicsXf4qZoMVw/640?wx_fmt=png)

通过继续分析目标服务器中的可以进程与端口占用情况，发现另外可疑文件，如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4v0zHWpHZicTU1USEWmReTXpIml8V01XLiceGl79tr6k6P7zkO3RkAmpA/640?wx_fmt=png)

将可疑文件进行本地分析，证实此文件为病毒文件：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4yWVg2fg0ss932IUrOVdVqZCsTSDtOA5t8qxTMUIG1CXjlPicETuiaZKg/640?wx_fmt=png)

### 2.4 发现攻击者的攻击操作

针对目标环境进行彻底排查，发现攻击者使用 wget 操作从 http://111.205.192.5:2356 服务器中下载 “l” 病毒文件，并执行了 “777” 加权的操作。

其记录文件如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4o6lxiaGvKibNicB3QntlbRSMoukBVDcy3DE8XA5SkBb5ymjMFZuw0U1Ew/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4jcg8SPC8yan9SySxBnaPmrWNicvhSuy2bL4E3liacCMbrqZmGIrZQN6A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4greHXat0CWdsI1CP5w4LHGWP9xOKKHRXvItqlbhMuB95OhPlAtrLRw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4kSqYvrtYV5YAn1JRghzYFzAc9dBy9QQrFNqKfTmxicmkUHwHshaFicnw/640?wx_fmt=png)

通过进一步的对可疑。通过分析目标服务器日志文件，发现攻击者下载病毒文件后又使用内网扫描软件 “.x” 调用其 “pascan” 和“scanssh”模块进行内网 ssh 扫描，通过分析发现攻击者收集到了目标网络环境中的常用密码来进行针对性的扫描测试。

如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP49sDiciaH1evuWzKk00xtL9ricS5I1JsR4VVqQib0C2YibgzEG2H0t5px0Rg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP44rPqYV5JGJ3VBFRDhBdsukibv3JN4SBsHz03fbSaBTibRiaDZpPnH0JRg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4zX1Sto5RDPuyxGxLVIO2eOAdXF70sUVwbyqARqbJatNUQbIqKbXfWA/640?wx_fmt=png)

通过继续对扫描软件进行深入挖掘，发现攻击者使用扫描软件得到的其他内网的 ip 地址（部分）：尝试使用此地址中的 192.168.21.231 和 192.168.21.218 进行 ssh 登录，可使用`root:huawei`成功进行 ssh 连接（其他地址及口令不再进行测试），并在内网机器中发现使用弱口令 “123456” 并发现了同样的 “l” 病毒文件。

其记录文件如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4YkmrcpemOqhBqELw7NibaD8l2MOibttKpL8wcftPib4fmRyrNncL6aGxQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4XUsTjXYYLicnXZgPibY2jc74DXHEsvnAurP2LQqDaiagc2qhvHHkKyDLg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4tUk46KicprtzBHic8BVJLIibaRMhmZdY2jImCyMEVVkWkz1mUCH5ZDgPA/640?wx_fmt=png)

在扫描器中发现了攻击者使用的 “passfile” 字典文件，从中可以发现攻击者使用的字典具有很强的针对性（初步断定攻击者为在网络环境中通过查询密码文件等操作获取的相关密码）：_隐私信息 -- 此处不贴图_

通过继续对日志文件进行排查，发现攻击者使用扫描器进行攻击的历史记录，验证了搜集到的信息：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4UW7uqGdhjPVSgF9fsWl8EA1YzH1JMuuYcWibMWPY6yCQR0xLibvstLFg/640?wx_fmt=png)

通过即系分析，发现攻击者在进入目标服务器后，又进行了防火墙权限修改、“udf”权限提升、远程连接等其他操作。其中 “udf 病毒文件” 未在目标服务器中发现，在后期进行反追踪中在攻击者服务器中获取到 “udf” 文件，进行本地检测后病毒文件。

其记录文件如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4WPg9QcibIvMsL9lOIhGJ4iaCeIcwMIXY0LujDP9m3Znx95RYQQ5odIwg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4SwwonRbn6XOwKHTdjK8hZVDjwm7oReUXe1m0BhSZMSKDs5yx9U14rA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4OkX8FUjiaia1bCXfBicOLJ1u0ozyKjJgic3px35GCBvREKQp3qXguGz18g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP45y43SdQSWcFly51M7pk6oUNojzFz1n9HUCvNeETibzK1aSl2NbL20Jg/640?wx_fmt=png)

通过对攻击者完整的攻击取证，可证实攻击者通过 SSH 连接的方式使用`guest_cm`用户而和`root`用户进行远程连接，连接之后使用 Wget 方式下载并种植在目标服务器中 “l” 和“vkgdqddusx”病毒文件，并使用 “udf” 进行进一步的权限操作，然后使用 “.x” 扫描软件配合针对性极强的密码字典进行内网的扫描入侵，并以目标服务器为跳板使用 root 和 xxx 账户登录了内网中的其他机器在入侵过程中入侵者将部分相关日志进行了清除操作。

**0x03 溯源操作**
=============

### 3.1 关于攻击者的反向检测

在取证过程中发现攻击者服务器使用以下三个 ip

xxx.xxx.xxx.x、xxx.xxx.xxx.xxx、xxx.xx.xxx.xx（打个马赛克）

通过对这三个 IP 进行溯源找到

http://111.205.192.5:2356/ 网站使用 hfs 服务器搭建，文件服务器内存储着各种病毒文件，其中找到了在 “l”“udf” 等病毒文件，证实前文中的判断。

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4vlRy2SMw7DX4qTCeGWkicVovGLPjYz50pWVBuFd5fMYdVLbXzPN6ic2g/640?wx_fmt=png)

通过其他手段查询得知使用 ip 地址曾绑定 www.xxxx.com 网站，并查找出疑似攻击者真实姓名 xxx、xxx，其团体使用 xxxxxx@qq.com、wangzxxxxxx.yes@gmail.com 等邮箱，使用 61441xx、3675xx 等 QQ。并通过某种手段深挖得知攻击者同事运营着多个博彩、私服类网站。  

其他信息请看下图：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4t9ojicHKJfxpWx6BLLI2LUZqg405OjIbhu7aUXnhgsibcA0hwJHficniaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP41Hwt86pQ1VO70bblVFUYNmWQk8ONn4MfPhU0pHWKbxqymlQR9yPicNg/640?wx_fmt=png)

**0x04 攻击源确定**
==============

### 4.1 确定攻击入口处

综合我们对内网多台服务器的日志分析，发现造成本次安全事件的主要原因是：

10.0.xx.xx 设备的网络部署存在安全问题，未对其进行正确的网络隔离，导致其 ssh 管理端口长期暴露在公网上，通过分析 ssh 登陆日志，该台设备长期遭受 ssh 口令暴力破解攻击，并发现存在成功暴力破解的日志，攻击者正是通过 ssh 弱口令获取设备控制权限，并植入木马程序进一步感染内网服务器。

具体攻击流程如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4gjw4UDYxZic3VjlnX48a0seVwTmvFGBibGAa1CtppMpxJywhwPyuibAhA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4Hg0n6REJXZFJmqHFeuKRuRqic8EA3g5ic441o3A3EovHaCOkWXD65ywQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4QPU6Cwmvy3m2LUKkPBonk2vOm30EOkibaOibc5dribojPgiaBHOTxAlQRA/640?wx_fmt=png)

经分析，2016 年 1 月 12 号公网 ip 为 211.137.38.124 的机器使用 ssh 爆破的方式成功登陆进入 10.0.xx.xx 机器，之后攻击者以 10.0.16.24 机器为跳板使用相同的账户登录进入 192.168.xxx.xxx 机器。  

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4ae0b9Lj0eoVV6jjWu8jbscDk9SHlqNxEzzT2qm80TXFZyLbEdjmnww/640?wx_fmt=png)

攻击者进入 192.168.150.160 机器后，于 2016 年 1 月 17 日使用 wget 的方式从 http://111.205.192.5:23561 网站中下载了 “Linux DDos” 木马文件，并使用扫描器对内网进行扫描的操作。  

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP4ESU6j8voGc5iaEgWSMUI7RccvicrV4uNU6GEf5MicmnJeVEaSVYlp8N5w/640?wx_fmt=png)

攻击者通过相同的手段在 2016 年 1 月 17 日使用 sftp 传输的方式进行了木马的扩散行为，详细情况见下图：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7cO3dQumQgMBG6jHrjejIP47l8HzYZO5QmrpBicmeX3gLpEHjavGiawGkSaoR2FsNMEEGSYEF3J77RA/640?wx_fmt=png)

**0x05 安全性建议**
==============

```
对使用密码字典中的服务器进行密码的更改。
对网络环境进行彻底的整改，关闭不必要的对外端口。
网络环境已经被进行过内网渗透，还需要及时排查内网机器的安全风险，及时处理。
SSH登录限制，修改sshd配置文件
```

由于服务器较多，防止病毒通过 ssh 互相传播，可通过修改`sshd_config`，实现只允许指定的机器连接，方法如下：

登录目标主机，编辑 / etc/ssh/sshd\_config

```
#!bash
# vi /etc/ssh/sshd\_confi
```

在文件的最后追加允许访问 22 端口的主机 IP，（IP 可用 \* 号通配，但不建议）

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)

**【好书推荐】**

![](https://mmbiz.qpic.cn/mmbiz_png/ffq88LJJ8oPhzuqa2g06cq4ibd8KROg1zLzfrh8U6DZtO1oWkTC1hOvSicE26GgK8WLTjgngE0ViaIFGXj2bE32NA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/x1FY7hp5L8Hr4hmCxbekk2xgNEJRr8vlbLKbZjjWdV4eMia5VpwsZHOfZmCGgia9oCO9zWYSzfTSIN95oRGMdgAw/640?wx_fmt=gif)

[2020hw 系列文章整理（中秋快乐、国庆快乐、双节快乐）](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247492405&idx=1&sn=c84692daf6077f5cc7c348d1e5b3a349&chksm=f9e38c6ece9405785260b092d04cfb56fec279178d4efcd34bf8121b89a28885bf20568cdfda&scene=21#wechat_redirect)  

[HW 中如何检测和阻止 DNS 隧道](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247492405&idx=2&sn=7afccd524c176b4912526d8f5d58dc3a&chksm=f9e38c6ece940578b5a4f0f102fa5a20b6facee51f23e3fa25598e9e7257c798180edcdf5802&scene=21#wechat_redirect)

[ctf 系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493664&idx=1&sn=40df204276e9d77f5447a0e2502aebe3&chksm=f9e3877bce940e6d0e26688a59672706f324dedf0834fb43c76cffca063f5131f87716987260&scene=21#wechat_redirect)

[日志安全系列 - 安全日志](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494122&idx=1&sn=984043006a1f65484f274eed11d8968e&chksm=f9e386b1ce940fa79b578c32ebf02e69558bcb932d4dc39c81f4cf6399617a95fc1ccf52263c&scene=21#wechat_redirect)

[【干货】流量分析系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494242&idx=1&sn=7f102d4db8cb4dddb5672713803dc000&chksm=f9e38539ce940c2f488637f312fb56fd2d13a3dd57a3a938cd6d6a68ebaf8806b37acd1ce5d0&scene=21#wechat_redirect)

[【干货】超全的 渗透测试系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494408&idx=1&sn=75b61410ecc5103edc0b0b887fd131a4&chksm=f9e38453ce940d450dc10b69c86442c01a4cd0210ba49f14468b3d4bcb9d634777854374457c&scene=21#wechat_redirect)

[【干货】持续性更新 - 内网渗透测试系列文章](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494623&idx=1&sn=f52145509aa1a6d941c5d9c42d88328c&chksm=f9e38484ce940d920d8a6b24d543da7dd405d75291b574bf34ca43091827262804bbef564603&scene=21#wechat_redirect)  

[【干货】android 安全系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494707&idx=1&sn=5b2596d41bda019fcb15bbfcce517621&chksm=f9e38368ce940a7e95946b0221d40d3c62eeae515437c040afd144ed9d499dcf9cc67f2874fe&scene=21#wechat_redirect)

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icnAsbXzXAVx0TwTHEy4yhBTShsTzrKfPqByzM33IVib0gdPRn3rJw3oz2uXBa4h2msAcJV6mztxvjQ/640?wx_fmt=png)