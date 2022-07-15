> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/xpI0e3X2zVNmL20BdKmcfA)

点击蓝字关注我哦

  

  

  

  

**前言**
------

Impacket 工具包是红队人员内网横向使用频率最多的工具包之一，而 Impacket 是一个标准 Python 类库，用于对 SMB1-3 或 IPv4 / IPv6 上的 TCP、UDP、ICMP、IGMP，ARP，IPv4，IPv6，SMB，MSRPC，NTLM，Kerberos，WMI，LDAP 等协议进行低级编程访问。在 impacket 工具包中用到最多的协议就是 smb 协议，SMB 是一种网络协议，也称为服务器消息块协议，它被用于在客户端和服务器之间进行通信，它 还可以用来共享文件，打印机和其他一些网络资源。其次就是 MSRPC，MSRPC 或 Microsoft 远程过程调用是 DCE / RPC 的修改版本，它是由 Microsoft 创建的，用于在 Windows 中无缝创建客户端 / 服务器模型，Windows Server 域协议完全基于 MSRPC。

  

使用  

-----

安装就无需多言了，实在不会的就百度吧！ 

```
git clone https://github.com/SecureAuthCorp/impacket.git
cd impacket/
ls
python setup.py install
```

所有生成的工具包文件都在 example 目录下：

这里喔演示，这里没有搭建域环境，如果域存在就在用户名前面加上域名，用户：administator 密码：123456

为啥要以 administrator 用户为演示，因为在打了 kb2871997 补丁下，禁 止 sid500 以外的的用户进行 pth，如果不存在域就不需要加上域名参数。

smbclient.py 

有时候，我们需要在攻击者计算机和目标计算机之间执行多项操作，那么 s mbclien.py 足够满足我们的所需，它可以列出共享和文件，重命名某些文件，上传二进制文件或从目标计算机下载文件，当然还有更多妙用。。。。句法：

```
smbclient.py [域] / [用户]：[密码/密码哈希] @ [目标 IP 地址]
```

通过密码建立 smb 服务连接

```
Python smbclient.py

redteamspace/Administrator:123456@192.168.75.141
```

通过 hash 建立 smb 服务连接

```
python3 smbclient.py -hashes 00000000000000000000000000000000:32ed87bdb5fdc5e9cba88547376818d4 administrator@192.168.75.141
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXongFmJwMJKTTtUe2ZqRdRjf382PyOn0I7cO5iaA8o5KuSWzktp62ntFUaQ/640?wx_fmt=png)

我们将连接到目标计算机，并且我们有了一个 smb shell，它可以运行各 种命令，例如 dir，cd，pwd，put，rename，更多，del，rm，mkdir，rmdir，信息等

lookupsid.py 

安全标识符（SID）是可变长度的唯一值，用于标识用户帐户，通过 SID 用 户枚举，我们可以提取有关存在的用户及其数据的信息，Lookupsid 脚本可以枚举本地和域用户。

句法：

```
lookupsid.py [域] / [用户]：[密码/密码哈希] @ [目标 IP 地址]
```

通过密码进行验证

```
Pyhton lookupsid.py
redteamspace/Administrator:123456@192.168.75.141
```

通过 hash 进行验证

```
Pyhton lookupsid.py -hashes 00000000000000000000000000000000: 
32ed87bdb5fdc5e9cba88547376818d4 
redteamspace/Administrator@192.168.75.141
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXongyD920bOmTuIjeUaP1gaKeteP136E6XpH7dUrpQAkM2G5uDJnzUQ41Q/640?wx_fmt=png)

reg.py 

Reg.exe 是一个可执行服务，当与 eh 分别结合查询，添加，删除关键字的组合使用时，可以读取，修改和删除注册表值, 该脚本就是利用 reg 服务，它可用于获取有关各种策略，软件的信息，还可以更改其中一些策略。

句法：

```
reg.py [域] / [用户]：[密码：密码哈希] @ [目标 IP 地址] [操作] [操作参数]
```

通过密码进行验证

```
Python3 reg.py Administrator:123456@192.168.75.141 query -
keyName HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows -s
```

通过 hash 进行验证

```
Pyhton reg.py -hashes 00000000000000000000000000000000: 
32ed87bdb5fdc5e9cba88547376818d
redteamspace/Administrator@192.168.75.141 query -keyName 
HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows -s
```

上面实例可以获取 windows 的安全策略

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXongUKv4LicUiaKh2pP0kYnh85EiamIpiaoMyiav8IAzzyG5WavX5lBOVUmhk7w/640?wx_fmt=png)

**rpcdump.py**

RPC 或远程过程调用是指计算机程序使过程在不同的地址空间中执行时（被编码为常规过程调用）。该脚本可以为我们枚举这些端点。

句法：

```
rpcdump.py [域] / [用户]：[密码/密码哈希] @ [目标 IP 地址]
```

通过密码进行验证：

```
Python rpcdump.py 
redteamspace/Administrator:123456@192.168.75.141
```

通过 hash 进行验证：

```
Python rpcdump.py -hashes 
00000000000000000000000000000000:32196B56FFE6F45E294117B91A83BF38 
redteamspace/Administrator@192.168.75.141
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXong4h9Uy7NC8OaUEH3hlLW6KjCUcKdBr36wIB4ElO9wW2BVS60eI496KQ/640?wx_fmt=png)

opdump.py  

该脚本绑定到给定的主机名：端口，并连接到 DCERPC（分布式计算环境 / 远程过程调用）接口。连接后，它将尝试依次调用前 256 个操作号中的每个操作号，并报告每次调用的结果，这会生成与给定 host：port 的 TCP 连接信息。

句法：

```
opdump.py [目标 IP 地址] [端口接口版本]
opdump.py 192.168.75.141 135 76F226C3-EC14-4325-8A99-
6A46348418AF v1.0
```

**samrdump.py**

Samrdump 是一个使用安全帐户管理器（SAM）检索有关指定目标计算机的敏感信息的应用程序。它是一个远程接口，可以在 “分布式计算环境 / 远程过程调用（DCE / RPC）” 服务下进行访问。它列出了所有系统共享，用户帐户以及 有关目标在本地网络中的存在状态的其他有用信息。

句法：

```
samrdump.py [域] / [用户]：[密码/密码哈希] @ [目标 IP 地址]
```

通过密码进行验证：

```
Python samrdump.py Administrator:123456@192.168.75.141
```

通过 hash 进行验证：

```
Python samrdump.py -hashes 00000000000000000000000000000000:
32196B56FFE6F45E294117B91A83BF38 
redteamspace/Administrator@192.168.75.141
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXongRerb7WLkePJj35E3DXiacHia7UE82yib3a4rQgCnSWhUsSZau5HSHWvUA/640?wx_fmt=png)

**services.py**  

Impacket 的服务脚本在 MSRPC Interface 的帮助下与 Windows 服务进行通信。它可以启动，停止，删除，读取状态，配置，列出，创建和更改任何服务。

句法：

```
services.py [域] / [用户]：[密码/密码哈希] @ [目标 IP 地址] [操 作]
```

通过密码进行验证： 

```
Python services.py Administrator:123456@192.168.75.141 list
```

通过 hash 进行验证：

```
Python services.py -hashes 00000000000000000000000000000000:
32196B56FFE6F45E294117B91A83BF38 
redteamspace/Administrator@192.168.75.141 list
```

**![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXongI2JOoNBlquOnNIB4Xpyo6guJjm5S5r61ibJtgWmmNE4emonPmM3drjw/640?wx_fmt=png)**

**ifmap.py**

Ifmap 脚本最初绑定到目标计算机的 MGMT 接口。它会在获取接口 ID 的列 表后，将这些 ID 添加到其数据库中已经具有的 UUID 的另一个大型列表中，然 后，它尝试绑定每个接口并报告接口状态（该状态可以列出或正在监听），会 展示程序的 UUID（通用唯一标识符）列表，通过这些在互联网搜索此 uuid，来检索服务安全性。  

句法：  

```
ifmap.py [目标 IP 地址] [目标端口]
ifmap.py 192.168.75.141 135
```

**getArch.py**

使用 NDR64 传输语法编码的所有 PDU（协议数据单元）必须使用 0x10 的值作为数据表示格式标签。此值仅在 x64 位系统的传输中使用。当目标脚本提供该脚本时，该脚本试图与目标系统进行通信，并收集数据表示格式标签的值。然后将其与存储在其代码中的 NDR64 语法匹配。然后，如果操作系统是 64 位或 32 位系统，它可以将信息提供给攻击者。  

**句法：**

```
getArch.py -target [目标 IP 地址]
getArch.py -targets [目标列表]
getArch.py -targets target.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXongiaatcDOAkXMM331YogvYUup3JNkszW0edpFjppXjXEAKbZRa62wR7Gg/640?wx_fmt=png)

netview.py   

这是一个枚举工具, 它要求使用域名来枚举主机。也可以提供主机或目标列 表 一旦找到信息，它就不会停止。它不断循环查找找到的主机，并详细跟踪谁从远程服务器登录 / 注销, 它保持与目标系统的连接，并且非常隐蔽，因为它仅发送少量 DCERPC 数据包。此脚本要求攻击者计算机能够解析域计算机的 NetBIOS 名称, 这可以通过将攻击者计算机上的 DNS 设置为域 DNS 来实现。

句法：

```
netview.py [域] / [用户]-目标[目标 IP 地址]-用户[用户列表]
netview.py [域] / [用户]-目标[目标列表]-用户[用户列表]
netview.py redteamspace/Administrator -targets target.txt -users 
user.txt
```

总结
--

可以看到无论是 smb，还是 rpc，语法构成都基本上差不多，只是有些工具脚本需要一下特殊的参数，但是填写身份证验证这一块参数基本上一致，impackt 网络工具包博大精深，需要好好研究一番。

欢迎加入星球，一直会分享一些免杀实用工具！以及分享技术，独特的交互式技术交流，星球内免费提问，营造良好的学习氛围，如果你也热爱红队技术，那加入我们吧

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXong3zVAYcPgzfia9jwcsTxQ2zmrcHKYTgibcuPqtYZ7VM8yvm8Ria8N552AQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXong14cnuiacj1nOP3AWOj8wp5gtfbnbtmRicHzzEceulwrprcGBicVHILJpA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODu6EOOo9mRd00wOt9InXongj9fz3SLLGYU7hcd8NaZCCYiaGROtFI2B7n45icnqBVUkmpPeZaEq67Gw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

END

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtIZ5VYusLbEoY8iaTjibTWg6AKjAQiahf2fctN4PSdYm2O1Hibr56ia39iaJcxBoe04t4nlYyOmRvCr56Q/640?wx_fmt=gif)

**看完记得点赞，关注哟，爱您！**

**请严格遵守网络安全法相关条例！此分享主要用于学习，切勿走上违法犯罪的不归路，一切后果自付！**

  

关注此公众号，回复 "Gamma" 关键字免费领取一套网络安全视频以及相关书籍，公众号内还有收集的常用工具！

  

**在看你就赞赞我！**

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbThXaInFkmyjOOcBoNCXGun5icNbT4mjCjcREA3nMN7G8icS0IKM3ebuLA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTkwLkofibxKKjhEu7Rx8u1P8sibicPkzKmkjjvddDg8vDYxLibe143CwHAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/96Koibz2dODuKK75wg0AnoibFiaUSRyYlmhIZ0mrzg9WCcWOtyblENWAOdHxx9BWjlJclPlVRxA1gHkkxRpyK2cpg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTicALFtE3HLbUiamP3IAdeINR1a84qnmro82ZKh4lpl5cHumDfzCE3P8w/640?wx_fmt=gif)

扫码关注我们

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTicALFtE3HLbUiamP3IAdeINR1a84qnmro82ZKh4lpl5cHumDfzCE3P8w/640?wx_fmt=gif)

扫码领 hacker 资料，常用工具，以及各种福利

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTnHS31hY5p9FJS6gMfNZcSH2TibPUmiam6ajGW3l43pb0ySLc1FibHmicibw/640?wx_fmt=gif)

转载是一种动力 分享是一种美德