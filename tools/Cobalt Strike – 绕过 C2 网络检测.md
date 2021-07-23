> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/4yJ38Kn2NiItiX2rEaMloQ)<table><tbody><tr><td width="557" valign="top" height="62"><section><strong>声明：</strong>该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。</section><section>请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。</section></td></tr></tbody></table>

这篇文章为机器翻译文，如有英文阅读能力建议阅读原文：https://newtonpaul.com/cobalt-strike-bypassing-c2-network-detections/

**0x01 介绍**

在这篇小博文中，我们将研究如何轻松绕过 Cobalt Strike beacon 的网络检测。Symantec Endpoint Protection (SEP) 等许多 AV 产品都具有网络检测功能，可以监控通过设备网络接口的流量。此外，IDS 和 IPS 还具有对 C2 流量的基本检测，这些检测基本上是在网络数据包中寻找特定的模式。  

对于像 Cobalt Strike 这样的流行工具，beacon 的基本 “开箱即用” 设置由供应商进行指纹识别，因此会被检测到。  

在 Cobalt Strike 中，Malleable 配置文件用于定义 C2 的设置。您可以为 C2 选择不同的协议，HTTP、HTTPS 和 DNS 是三种流行的协议。由于有效负载未加密，HTTP beacon 很容易被检测到。对于 HTTPS 连接，会在用于加密的证书上进行检测。

与任何利用工具一样，如果您使用默认值，很可能会被检测到。GitHub 上有可供使用的 Malleable 配置文件，这些配置文件将更改您的默认 C2 设置。然而，这些也已经被指纹识别，并且也会产生检测。GitHub 上提供的配置文件更多地旨在测试您对过去在野外看到的不同 APT 和 CrimeWare C2 的检测能力。

https://github.com/rsmudge/Malleable-C2-Profiles

**0x02 解决方案**

幸运的是，Cobalt Strike Malleable C2 配置文件是高度可定制的。事实上，定制化是 Cobalt Strike 如此受欢迎且如此有效的原因之一。您可以编写自己的个人资料，并且有一些在线指南向您展示如何执行此操作。

但是，还有一种更简单的方法，C2 Concealer。该工具由 FortyNorth Security 创建，于去年发布，具有 Python 脚本，可根据用户定义的几个变量生成 C2 配置文件。

https://github.com/FortyNorthSecurity/C2concealer

**0x03 演示**

安装很简单，只需克隆 GitHub 存储库，然后运行安装脚本即可。

安装完成后，运行脚本并定义您希望使用的主机名。

```
C2concealer --hostname newtpaul.com  --variant 1
```

接下来，C2Concealer 将扫描您的主机以定位 c2lint 所在的位置。C2lint 是 CobaltStrike 附带的一个工具，用于在使用配置文件之前对其进行测试 / 故障排除。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcqe5oGsYIGfXUylL1dGHbcNEeDYcxKqWyJcIHTFAl1UQGnE6iblFQHurzMjflPppwApbsL4utRg8A/640?wx_fmt=png)

扫描完成后，系统会要求您选择 SSL 选项。使用合法的 LetsEncrypt 证书显然是避免检测的最有效方法。但是，这需要您将 A 记录指向您的团队服务器。为此，我们将只使用自签名证书。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcqe5oGsYIGfXUylL1dGHbcOPC2aKpEQYBmicpqHVAias25bsknCDkDUVdfazJlWTzOzZic5Je7IViakA/640?wx_fmt=png)

系统会要求您填写证书的一些基本信息，你在这里放什么并不重要。

完成后，您应该会收到配置文件已通过 c2lint 检查的确认信息。还将显示新创建的配置文件的名称。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcqe5oGsYIGfXUylL1dGHbcZUvZsrUdD6Lfbia13tTlK3KrIARWhoCjCK0O2HJd4lumXxgwEVmL0XA/640?wx_fmt=png)

接下来，启动您的团队服务器，但这次定义要加载的配置文件。

```
sudo ./teamserver 192.168.1.21 *Password* ~/C2concealer/C2concealer/34c5a462.profile
```

生成您选择的新监听器和有效载荷。

**0x05 之前 VS 之后**

在使用我们新创建的配置文件之前，SEP 阻止了与 Cobalt Strike 团队服务器的出站连接。这是仅使用默认 C2 配置文件时的情况。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcqe5oGsYIGfXUylL1dGHbc4melpdA4K05FlaNHRUUFGfnGhEvRliaSdU1Vu0PjBkO2vnVkkXmkPYA/640?wx_fmt=png)

但是，在使用我们新创建的配置文件后，没有任何内容被阻止，我们能够成功建立 C2。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcqe5oGsYIGfXUylL1dGHbc3LVwtMActWrnYcawYq7qbGIt5Bn2XWYsGiaU4pibicAh3GBG5HnZRBsKA/640?wx_fmt=png)

关注公众号回复 “9527” 可免费获取一套 HTB 靶场文档和视频，“1120” 安全参考等安全杂志 PDF 电子版，“1208” 个人常用高效爆破字典，“0221”2020 年酒仙桥文章打包，还在等什么？赶紧点击下方名片关注学习吧！

公众号

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcAcRDPBsTMEQ0pGhzmYrBp7pvhtHnb0sJiaBzhHIILwpLtxYnPjqKmibA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247487086&idx=1&sn=37fa19dd8ddad930c0d60c84e63f7892&chksm=cfa6aa7df8d1236bb49410e03a1678d69d43014893a597a6690a9a97af6eb06c93e860aa6836&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcIJDWu9lMmvjKulJ1TxiavKVzyum8jfLVjSYI21rq57uueQafg0LSTCA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486961&idx=1&sn=d02db4cfe2bdf3027415c76d17375f50&chksm=cfa6a9e2f8d120f4c9e4d8f1a7cd50a1121253cb28cc3222595e268bd869effcbb09658221ec&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)