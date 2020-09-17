\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/OTYdm3FEqdtKFIUnTHXjqg)

**点击蓝字关注我们**

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/kuIKKC9tNkCXmkJFce7LMg3r1vPjqfuiaJUIKzuIPniaKFicicOPLgtIr8icibPDeWPzGVxWYdKUSIghibfy3PibWdbo9Q/640?wx_fmt=png)

近日，安全公司 Secura 针对一个刚修补不久的 Windows 漏洞（CVE-2020-1472）开发了一个概念验证利用程序——Zerologon，可以 “三秒内” 接管企业内网的司令部——Active Directory 域控制器，“呵护”所有联网计算机。

CVE-2020-1472 是 Netlogon 远程协议（MS-NRPC）中的一个特权提升漏洞，被微软评定为危险级别最高的 “高危漏洞”，CVSS(常见漏洞评分系统) 评分为满分 10 分。要想利用该漏洞，攻击者必须在目标网络中找到立足点，通过没有特权的内部人员，或者对联网设备的入侵。该漏洞使攻击者可以操纵 Netlogon 的身份验证过程，进行以下操作：

**·** 可模拟网络上任何计算机的身份通过域控制器的身份验证

**·** 在 Netlogon 身份验证过程中禁用安全功能

**·** 更改域控制器的 Active Directory 上的计算机密码（所有加入域的计算机的数据库及其密码）

![](https://mmbiz.qpic.cn/mmbiz_jpg/kuIKKC9tNkCXmkJFce7LMg3r1vPjqfuiasyfic8pn1mtOAr8wibNaCvZZSEB8CCoU8SCFjv4JnLibRJMibB6Fw9qgoQ/640?wx_fmt=jpeg)

受漏洞影响的 Windows Server 版本（对 Active Directory 域控制器服务器来说尤其危险）  图表：奇安信威胁情报中心

**虽然微软 8 月 11 日为 CVE-2020-1472 发布了补丁程序，但这并非麻烦的终结，而是开始。**  

Secura 的研究人员在本周一发布了该漏洞的详细技术信息仅几个小时后，一些 PoC 漏洞利用 / 工具就已在 GitHub 上发布，这对那些尚未修补该漏洞的企业来说，构成极大威胁，可以使用 Secura 研究人员发布的这个 Python 脚本（https://github.com/SecuraBV/CVE-2020-1472），检查域控制器是否易受攻击。

**三秒攻击：任何人都可以成为管理员**

对于勒索软件或间谍软件的攻击者而言，该漏洞可谓价值连城。因为通常来说，攻击者诱使员工点击电子邮件中的恶意链接和附件感染端点相对容易，但是进一步的提权和横向移动并获取高价值信息则困难的多。  

通常，攻击者可能需要数周或数月的时间才能将低级特权升级为安装恶意软件或执行命令所需的特权。而使用 Zerologon 漏洞利用程序，**攻击者 “只需不到三秒” 可以立即获得对 Active Directory 的控制**，在企业网络中为所欲为、予取予求，例如，将新计算机添加到网络或用自己偏爱的恶意软件感染每台计算机。

Secura 的研究人员在上周五发布的白皮书（https://www.secura.com/blog/zero-logon）中写道：“这种攻击产生了巨大的影响。”“它使本地网络上的任何攻击者（例如恶意内部人员或任何有机会将设备接入内部网络端口的人）能完全破坏 Windows 域。攻击者甚至不需要任何用户账户凭据。”

Secura 研究人员发现了此漏洞并将其报告给微软，并表示已开发出一种可以可靠运行的漏洞利用程序，但由于存在风险，他们只有在确信 Microsoft 的补丁已广泛安装在易受攻击的服务器上，然后才发布此漏洞。但是，研究人员警告说，使用 Microsoft 的补丁程序逆向开发漏洞利用并不难。

但是，面对如此诱人的 “营销机会”，其他安全公司的独立研究人员自然不会坐失良机，纷纷发布了自己的概念验证攻击代码，例如：

**·**https://github.com/risksense/zerologon/  

**·**https://github.com/blackarrowsec/redteam-research/blob/master/CVE-2020-1472/CVE-2020-1472.py

**·**https://github.com/bb00/zer0dump

漏洞利用代码的很快引起了美国网络安全和基础设施安全局的关注，该机构致力于改善政府网络安全。周一，Twitter 也炸锅了，各界安全人士对该漏洞的巨大威胁纷纷发表评论。

“Zerologon（CVE-2020-1472），有史以来最疯狂的漏洞！” 一位 Windows 用户写道。攻击者可立即通过未经身份验证的网络访问来获得域管理员特权。”

“还记得有关最小访问权限安全原则可以缓解设备被入侵吗？是否有几个盒子被伪装都没关系吗？” 安全公司 ZecOps 的创始人兼首席执行官 Zuk Avraham 写道。“哦，好吧……CVE-2020-1472/#Zerologon 基本上会改变您的想法。”

“企业被攻击后，如果清理和恢复工作遗漏了任何其他恶意脚本，攻击者依然可以利用此漏洞在整个组织中部署勒索软件并长期驻留”Tenable 安全响应经理 Ryan Seguin 指出。

**利用与缓解**

Zerologon 通过在 Netlogon 身份验证参数中添加一串数字 “0” 作为参数来实施攻击（下图）。  

Windows 服务器依靠 Netlogon 协议执行各种任务，包括允许最终用户登录网络。只要攻击者能够与易受攻击的域控制器建立 TCP 连接，未经身份验证的人就可以使用该漏洞获取域管理账户凭据。

该漏洞源于 Windows 实施的 AES-CFB8，具体来说是使用带有密码反馈的 AES 加密协议来加密和验证内网中传输的身份验证消息。

AES-CFB8 正常工作的前提是为每个消息随机生成一个唯一的初始化向量。但 Windows 没能遵守此要求。Zerologon 通过在 Netlogon 消息的特定字段中填充数字 “0” 来利用此漏洞（下图）。Secura 在另外一篇文章中深入探讨了漏洞的原因以及利用此漏洞的五步方法。

![](https://mmbiz.qpic.cn/mmbiz_png/kuIKKC9tNkCXmkJFce7LMg3r1vPjqfuiaZrGGcArFia6gibkLibrlI7Ouhz83wsSm2PwUN0KZj4Zc1Zjkq6C0hTCjg/640?wx_fmt=png)

图片：Secura

微软在一份声明指出：安装八月份发布的补丁程序的系统可以免受攻击，因为补丁会对域中的所有 Windows 服务器和客户端强制执行安全的 NRPC。用户应该更新所有 Active Directory 域控制器，包括只读域控制器。  

微软解释说：“这些更新将使域控制器（DC）在默认情况下能够保护 Windows 设备，记录不兼容设备发现的事件，并可以选择为所有加入域的设备启用保护，但有明确的例外。”

但是，在企业部署域控制器（DC）强制模式之后，将需要进行彻底的修复，该模式要求所有 Windows 和非 Windows 设备都使用安全的 NRPC 或通过为任何不兼容的设备添加例外来明确允许该账户。

当前，企业可以手动通过启用特定的注册表项立即部署 DC 强制实施模式，2021 年 2 月 9 日后，DC 将自动置于强制执行模式。强制执行模式分两个阶段的原因主要有两个，一方面 Netlogon 远程协议的非 Windows 设备实现需要时间，此外，实现兼容的供应商也需要足够的时间为客户提供所需的更新。

对于 Zerologon 漏洞利用的危害性，安全专家们在社交媒体上展开了热议。一位专家认为关于该漏洞的危害有些耸人听闻，因为只要攻击者在内网中获得立足之地，游戏就已结束。

但也有专家反驳说，该论点与纵深防御原则背道而驰，纵深防御原则主张建立多层防御，通过冗余防护来缓解入侵后的攻击。

值得注意的是，由于管理员们对安装可能影响网络组件（如域控制器）的补丁更新非常谨慎，因此 CVE-2020-1472 补丁未能及时安装产生的风险要更大一些。强烈建议存在该漏洞的企业高度重视并尽快安装补丁程序。

**参考资料**

**CVE-2020-1472 漏洞补丁与建议：**

https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2020-1472

**Microsoft NetLogon 远程特权提升漏洞（CVE-2020-1472）通告：**

https://mp.weixin.qq.com/s/nRKuFAD-ev9k5icUmYdkvg

相关阅读

[微软本周二修复了一个 “震网” 级别的资深漏洞](http://mp.weixin.qq.com/s?__biz=MjM5Njc3NjM4MA==&mid=2651088974&idx=2&sn=3460dcaacdc153edfe577751936d153a&chksm=bd14d89d8a63518b6281176d8ace0f4bae697aa74c2ed97222ade2a4d25b93eec4a3813c77ec&scene=21#wechat_redirect)  

[不管是 CVE 还是 NVD  好多漏洞都被忽略](http://mp.weixin.qq.com/s?__biz=MjM5Njc3NjM4MA==&mid=2651078920&idx=2&sn=80447b42f850169f5f5652c48e1bf5b2&chksm=bd14f1db8a6378cde2da4ee1504d0ab88826b68b1dc81bbc67a9235aa94359b7fffff67cfec6&scene=21#wechat_redirect)  

[所有 Windows 都中招！微软爆出超级漏洞](http://mp.weixin.qq.com/s?__biz=MjM5Njc3NjM4MA==&mid=2651087587&idx=1&sn=58d15cb6605622a70377debc3fb8a056&chksm=bd14d2308a635b2600264e95f3489e38c57375def645e78300bb438882693cf364a32872a571&scene=21#wechat_redirect)  

![](https://mmbiz.qpic.cn/mmbiz_png/kuIKKC9tNkAfZibz9TQ8KWj4voxxxNSGMnicXSRCtG4URyLibbqPegjnnibfRB0z4zIzwghbLOkV5fqGYM8vhuQdqw/640?wx_fmt=png)

合作电话：18311333376  
合作微信：aqniu001  
投稿邮箱：editor@aqniu.com

![](https://mmbiz.qpic.cn/mmbiz_gif/kuIKKC9tNkAfZibz9TQ8KWj4voxxxNSGMAGiauAWicdDiaVl8fUJYtSgichibSzDUJvsic9HUfC38aPH9ia3sopypYW8ew/640?wx_fmt=gif)