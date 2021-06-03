> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Hw2ltbr96ZcfSgrL2TT3Hw)

**![](https://mmbiz.qpic.cn/mmbiz_gif/ll2PVky3MmaYz8UWHicLDSC4e3NqcibOLicCiaYtmQm9A0Ied3OLs4Wibj6bLz8jmf0gB3k0h1aQNNVKNqjKFcZV0Mg/640?wx_fmt=gif)**
===================================================================================================================================================

**0**

引言

工业网络安全公司 Claroty 研究人员近日发现了一个严重的漏洞，未经认证的远程攻击者可以利用这个漏洞攻击西门子旗下的可编程逻辑控制器 (PLC)。该漏洞被编号为 CVE-2020-15782，是一个高危的内存保护绕过漏洞，允许攻击者通过网络访问 TCP 102 端口在受保护的内存区域中写、读数据。这一远程可利用漏洞引发了研究者对西门子控制器安全问题的深入思考。

工业巨头西门子公司表示，该安全漏洞影响其 SIMATIC S7-1200 和 S7-1500 cpu，可通过新的漏洞远程攻击其 PLC 产品。西门子已经为一些受影响的设备发布了固件更新，并为尚未发布补丁的产品提供了变通方案。

根据 Claroty 公司的说法，该漏洞可绕过通常工程代码运行的沙箱，直接访问设备内存，从而在西门子 S7 PLC 上获得本机代码执行。研究人员展示了攻击者如何绕过保护直接将 shellcode 写入受保护的内存中。沙箱逃逸意味着攻击者可以从 PLC 的任何地方读写，并可用恶意代码修补内存中现有的 VM 操作码，从而对设备进行 Root 权限的操作。重点强调的是，利用这一漏洞的攻击将很难被发现。

研究成果的披露是西门子和 Claroty 公司紧密关系的结果，这不仅促进了工业网络安全研究团队和供应商在漏洞披露方面的合作，也促进了整个工业生态系统的安全。西门子和 Claroty 之间的密切合作包括技术细节、攻击技术和缓解建议的交流，这些都有助于促成西门子及时发布更新补丁。西门子和 Claroty 希望，鉴于此漏洞的关键性质，用户应尽快更新 S7-1200、S7-1500 CPU，以及其他受影响产品。

![](https://mmbiz.qpic.cn/mmbiz_png/GoUrACT176kDhibgCg5KODP2w2fzcUB3oVY1Tibibz6BDp6oEFxLeTqFSDyLcmNXLOZv9oqwtBWvjvs0MB8ypTwdA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_jpg/GoUrACT176kDhibgCg5KODP2w2fzcUB3oDmyWdycN01XH5akvheCp36P4IYjBMNmLsZOhhbMPkQdKhGJNv2licLg/640?wx_fmt=jpeg)

**一**

漏洞简介及受影响产品

1.1 漏洞概况

编号：CVE-2020-15782，在内存缓冲区范围内对操作的不当限制。CVSS v3.1 得分: 8.1。在知名漏洞网站 vuldb.com 上给的基本信息如下。

![](https://mmbiz.qpic.cn/mmbiz_png/GoUrACT176kDhibgCg5KODP2w2fzcUB3oRcBd9qGrKVJjfU8oNvOJyKpxHVqnyhNLMXjThmrp5obS2VRLnI7Iqg/640?wx_fmt=png)

1.2 受影响产品

受影响的设备容易受到内存保护绕过而实施特定的操作。对 TCP 端口 102 进行网络访问的远程未经身份验证的攻击者可能会将任意数据和代码写入受保护的内存区域，或读取敏感数据以发动进一步攻击。

5 月 28 日，西门子发布了警告 SSA-434534，向用户通报该漏洞相关信息。西门子还发布了包括 S7-1500、S7-1200 的各种产品的更新，建议用户更新到最新版本以弥补漏洞。该公司表示，正在为尚未更新的产品准备进一步更新。西门子还提供了用户可用于降低风险的具体缓解措施。

![](https://mmbiz.qpic.cn/mmbiz_png/GoUrACT176kDhibgCg5KODP2w2fzcUB3oslsplac7HHG7yfVib0bEqCMoMBrJEpFUibLjawC1vtedsPNSl1v1TrMw/640?wx_fmt=png)

**二**

西门子 PLC 本地代码执行的演进

CVE-2020-15782 之所以受到如此关注，主要是这一漏洞的成功利用，将有可能将工业网络安全研究者对西门子控制器攻击研究提高到新层次，而攻击者实施成功攻击的限制则越少越易，原因就是该漏洞的条件太优越。

在可编程逻辑控制器 (PLC) 等工业控制系统上实现本机代码执行是那些高级水平高能力攻击者已经实现的最终目标。因为这些复杂的系统有许多内存保护，攻击者不仅为了能够运行他们选择的代码，而且还要不被发现，因此必须要跨越这些保护措施。

早期的攻击尝试需要对 PLC 的物理访问和连接，或者以工程师工作站为目标的技术和通向 PLC 的其他链接，以获得那种级别的代码执行。而此次 Claroty 公司利用一个新发现的漏洞，在西门子 SIMATIC S7-1200 和 S7-1500 PLC cpu 内绕过 PLC 沙箱，在内存保护区域运行本机代码，进一步提升了这种攻击思路的远程可行性。攻击者可以利用这个 CVE-2020-15782 漏洞，远程获取难以检测和删除的读写内存访问。

从攻击者的角度来看，PLC 漏洞利用的终极目标就是在 PLC 上实现不受限制和不被检测的代码执行。这意味着，能够将代码隐藏在 PLC 内部深处，而不被操作系统或任何诊断软件检测到。

多年来，鉴于西门子 PLC 在市场上的领先地位，已经出现了许多在西门子 PLC 上实现这种能力的尝试。

**首先，史上最著名的震网攻击（Stuxnet），它在旧的 SIMATIC S7-300 和 S7-400 上获得了用户级的代码执行。**代码修改本身是通过操作本地 step7 项目文件来完成。然后，Stuxnet 能够通过操纵本地工程站上的 WinCC 二进制文件来隐藏 PLC 上的代码更改。这样一来，恶意软件不仅可以偷偷地将自己安装在 PLC 上，而且当控制软件试图从 PLC 读取受感染的内存块时，还可以保护自己不受 WInCC 检测。当然，通过对其 Windows 操作系统的 Microsoft 更新和 SSA-110665 和 SSA-027884 中记录的西门子产品更新的组合，这个问题早已得到解决。

**第二个经典型的 PLC 攻击，是 2019 年的 Rogue7 的攻击**（出自论文 Rogue7:Rogue Engineering-Station attacks on S7 Simatic PLCs）。《Rogue7》背后的研究人员能够创建一个流氓工程站，它可以伪装成 TIA（TIA Portal 是一系列无缝集成的自动化解决方案）通往 PLC 的门户，并注入任何有利于攻击者的信息。通过理解密码信息是如何交换的，他们能够将代码隐藏在用户内存中，而 TIA 工程站是看不见的。西门子部分解决了此问题，并提供了缓解措施，详见 SSA-232418。

**第三个，同在 2019 年，德国波鸿鲁尔大学 (Ruhr University Bochum) 安全研究专家 Ali Abbasi 和 Tobias Scharnowski 介绍了他们如何通过物理攻击 SIMATIC 1200 来获得在西门子 S7 PLC 上的代码执行。**他们使用 UART（通用异步收发传输器（Universal Asynchronous Receiver/Transmitter)，通常称作 UART。它将要传输的资料在串行通信与并行通信之间加以转换。作为把并行输入信号转成串行输出信号的芯片，UART 通常被集成于其他通讯接口的连结上。）物理连接来转储固件，并发现了一个漏洞链，使他们能够将代码隐藏在系统中更深的地方，并获得不受限制的代码执行。西门子在 SSA-686531 中解决了这个问题。

**本次，claroty 研究团队将这项研究向前推进了一大步，他们展示了一种新的复杂的远程攻击，它允许攻击者在西门子 S7 PLC 上获得本机代码执行。**攻击目标是内核的深处，并避免了任何检测，因为能够逃离用户沙箱，并在受保护的内存区域中编写 shellcode。CVE-2020-15782 漏洞恰恰是促成 PLC 沙箱逃逸的关键条件。

![](https://mmbiz.qpic.cn/mmbiz_png/GoUrACT176kDhibgCg5KODP2w2fzcUB3ofa5r82qdb5u3vf8zWJ8xeUFiaG6dIj7nVXiciasFaveo1kXmaMYRV2ELw/640?wx_fmt=png)

西门子 PLCs 本地代码执行攻击发展历程

**三**

PLC 沙箱逃逸

PLC 的完整性对操作人员和工程师来说至关重要，而攻击者的目标就是通过隐藏于控制器上的代码和提升权限来破坏这种完整性。本次利用的漏洞 CVE-2020-15782，绕过了 PLC 执行环境中的现有保护，包括工程代码通常会运行的沙箱。Claroty 能够利用这个漏洞实现沙箱逃逸，以便直接访问内存，然后编写并注入 shellcode 来执行其对西门子 1200/1500 PLC 的攻击。

为了执行这种攻击，需要对 PLC 进行网络访问。此外，攻击者还需要 PLC 下载权限。自从 TIA Portal V12 以来，西门子提供了各种缓解控制，以限制用户网络和对 PLC 的读写访问，特别是口令保护机制。此外，从 V17 开始，西门子引入了在 PLC、HMI 和 TIA Portal 之间使用个人证书的 TLS 通信，这大大减少了潜在的攻击面。

3.1PLC 的通用结构（以 S7 PLC 为例）

为了理解 Claroty 的具体攻击，首先要概述一个标准 PLC 的通用结构。它的 CPU 是一个 16 或 32 位微处理器，由一个内存芯片和集成电路组成，管理控制逻辑、过程监控和通信。CPU 指导 PLC 执行控制指令，与其他设备通信，执行逻辑和算术操作，并执行内部诊断。它还运行内存例程，不断检查 PLC，以避免编程错误，并确保内存没有损坏。逻辑运行在沙盒环境（有时也被称为 “监狱”）中。传输到控制器的逻辑仅限于供应商提供的特定内存区域和 API。

以西门子 S7 PLC 为例，它运行在 ADONIS 内核和 ARM 或 MIPS 处理器上，有许多编程语言可用于配置控制器，包括语句列表 (STL)、梯形图(LD)、功能框图(FBD) 和结构化控制语言(SCL)。

不管何种输入源，PLC 程序都会编译成 MC7/MC7 + 字节码，这是一种低级别的代码表示。经工程站编译后 - 西门子 TIA 门户 - 代码块 (MC7/MC7 + 格式) 通过西门子的 S7Comm/S7Comm + 协议下载并安装到 PLC 中。然后，PLC 中的 MC7 虚拟机将对代码块进行分派，并对字节码进行解释和执行。

![](https://mmbiz.qpic.cn/mmbiz_png/GoUrACT176kDhibgCg5KODP2w2fzcUB3oghI4Qmuoc1rMkictmKZZKYRabGCmjfZB4GY9ibK9nLiajiczwFzibsKcC4A/640?wx_fmt=png)

PLC 程序执行过程

如果不具备逆向工程能力，是不可能解码 MC7/MC7 + 字节码的，因为西门子没有公开提供这种技术文档。因此，研究才必须用逆向工程分析 MC7/MC7 + 字节码语言集，以便理解其内部机制并发现 bug。

3.2S7PLC 沙箱逃逸

由于虚拟机限制了用户程序访问的资源，因此编译后的字节码只能用于访问操作系统允许的资源，而不能直接用于硬件操作。这是为了将用户和运行代码限制在一组被认为是安全且已定义的操作中。例如，操作系统将限制对受保护内存的任何直接访问，但会允许使用 Siemens 提供的标准库中的任何函数 (例如 ADD_I - Add Integer 子例程)。换句话说，操作系统将用户代码“锁定” 在一个沙盒 / 容器中，对资源、内存和功能的访问是有限的，这可能会破坏 PLC 和 / 或整个进程。

为了逃逸或 “越狱” 本地 SIMATIC S7-1200 和 S7-1500 沙箱，Claroty 利用了其内存保护绕过漏洞。该漏洞使攻击者能够将任意数据和代码写入所谓的受保护的内存区域，或读取敏感数据以发动进一步攻击。

![](https://mmbiz.qpic.cn/mmbiz_png/GoUrACT176kDhibgCg5KODP2w2fzcUB3otx6nfooNSZjHtffTx1G7LdtrZlBAY1eVhjs8icFwj4xT7e6FduHc8ibg/640?wx_fmt=png)

利用 CVE-2020-15782 实现沙箱逃逸

沙箱逃逸意味着攻击者可以从 PLC 上的任何地方读写，并可以用恶意代码修补内存中现有的 VM 操作码来实现对设备的 ROOT 权限操作。例如，Claroty 能够直接将 ARM/MIPS shellcode 注入到内部操作系统结构中，这样当操作系统使用其选择的特定操作码时，恶意 shellcode 就会执行，从而远程执行代码。Claroty 使用这种技术安装了一个内核级程序，它具有一些对操作系统完全隐藏的功能。

**四**

四、防范建议

4.14.1 缓解措施

西门子已经确定了以下具体的解决方案和缓解措施，并强烈建议客户采用它们来降低风险:

*   S7 通信采用口令保护
    
*   通过 S7-1200 或 S7-1500CPU 的 ENDIS_PW 指令禁止客户端连接 (这将阻塞远程客户端连接，即使客户端可以提供正确的口令)
    
*   使用显示配置额外的访问保护 S7-1500 CPU(这将阻止远程客户端连接，即使客户端可以提供正确的口令)
    
*   应用 “纵深防御”，如工业操作指南第 12ff 页所述安全措施, 特别是:
    
    1. 工厂安全: 对关键部件的物理防护；
    
    2. 网络安全: 确保 PLC 系统没有连接到不可信的网络；
    
    3. 系统完整性: 配置、维护和保护设备应用适用的补偿饱和控制和使用内置的安全能力。
    
*   将整个解决方案更新到 TIA Portal V17，并使用 PLC、HMI 和 PG/PC 之间的个人证书 TLS 通信
    

4.2 通用的安全建议

作为一种通用的安全措施，西门子强烈建议使用适当的保护机制对设备网络访问。为了在受保护的 IT 环境中运行设备，西门子建议按照西门子工业安全操作指南进行环境配置 (https://www.siemens.com/cert/operational-guidelines-industrial-security)。

请按照产品手册中的建议操作。关于西门子工业安全的更多信息可以在

https://www.siemens.com/industrialsecurity 上找到。

**五**

小结

CVE-2020-15782 漏洞可以绕过通常工程代码运行的沙箱，直接访问设备的内存，从而在西门子 S7 PLC 上获得本机代码执行。Claroty 研究人员展示了攻击者如何绕过保护，直接将 shellcode 写入受保护的内存中。沙箱逃逸意味着攻击者可以从 PLC 的任何地方读写，并可以用恶意代码修补内存中现有的 VM 操作码，从而对设备进行 Root 权限的操作。需要特别注意的是，该漏洞如果被攻击者利用发起恶意攻击，将很难被检测发现。该项成果披露是西门子和 Claroty 公司紧密合作的结果，这有利于促进工业网络安全行业和工业设备供应商在漏洞披露方面的合作，也有利于整个工业生态系统的安全。

### 参考文献：

1、https://claroty.com/2021/05/28/blog-research-race-to-native-code-execution-in-plcs/

2、https://www.securityweek.com/newly-disclosed-vulnerability-allows-remote-hacking-siemens-plcs

3、SSA-434534: Memory Protection Bypass Vulnerability inSIMATIC

S7-1200and S7-1500 CPU Families

4、Rogue7: Rogue Engineering-Station attacks on S7 SimaticPLCs

5、Doors ofDurin:The Veiled Gate to Siemens S7 Silicon

6、https://vuldb.com/?id.176062

**往期精选**  

![图片](https://mmbiz.qpic.cn/mmbiz_gif/ll2PVky3MmYrt8sZBqiah8aNInQspzccnPAAhd0OKLQ5Ziad4ovQEohiamyrpYjQcwVAWROpYWmMXia1YRKPiczFSQw/640?wx_fmt=gif)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/ll2PVky3Mma4ibTfp7sC3ibt8WmetoDfiaGTpYxDHvJ6aZLsabUZelH2n9nWicm103pgGonoGYW9Fu2qj5zRFUtnnw/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzU3ODQ4NjA3Mg==&mid=2247499087&idx=1&sn=2321d0276f43b2350dc7225dc9022cd5&chksm=fd761718ca019e0e57a3fdb9fd073ff851d6f28e4ff851fcb3bb50ce340d550e26d1a99a3c37&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/ll2PVky3MmYd0Co7GNxTIib2DnpibJwlESNYb9n2xklNAvh89vWMWI8YhDjfoiceYywNZMRZAx2fxibEScMxfdzk1Q/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzU3ODQ4NjA3Mg==&mid=2247497825&idx=1&sn=228635ab78fb7c6b445a23d7d774a7b9&chksm=fd761236ca019b20ee7576033c2384b045c9ee9045649c10dd1d05842b8533e74b4d3e62b327&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/ll2PVky3MmbiaN8vT8xXhicoenf3MWQm5iba3ibKV7DtRrI4jSrIHCcU6oorfZqHkKibDmAicJrWyqRe6lWLibibInrt7w/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzU3ODQ4NjA3Mg==&mid=2247500032&idx=1&sn=e7fe6c0c75a22e005b85bf7d94eebc46&chksm=fd762b57ca01a241f8963ae6cd51caab586062974d1c820ca9f3825cc3a79f444b6a2fce4c99&scene=21#wechat_redirect)

**安帝科技**丨 **ANDISEC**

  

北京安帝科技有限公司是新兴的工业网络安全能力供应商，专注于网络化、数字化、智能化背景下的工业网络安全技术、产品、服务的探索和实践，创新应用网络空间行为学及工业网络行为验证，构建了工业大数据深度分析、威胁情报共享、威胁感知和协同响应等核心能力优势，为电力、石油石化、煤炭、烟草、轨道交通、智能制造等关键信息基础设施行业提供安全产品、服务和综合解决方案，工业网络安全态势感知平台已部署 4000 余家电厂。

  

![](https://mmbiz.qpic.cn/mmbiz_gif/ll2PVky3Mma4ibTfp7sC3ibt8WmetoDfiaGHEb7VOiaemeFbuCTupYgus7NTKkibwKwpsEDfzqZdXh1skHff6A6VNgA/640?wx_fmt=gif)

**点击 “在看” 鼓励一下吧**

![](https://mmbiz.qpic.cn/mmbiz_png/ll2PVky3MmZOFFgf4oTyfUTx7y0ZBV9yIg8qmaSwAvbjiba2KQn7VgmXYIriagc9H0hMu1u0UIZr98JYSmyG9tibg/640?wx_fmt=png)