> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/SnDl6LFeg1JvIFZFJadSlg)

> Sourcell@海特实验室

*   **_一个通过 ProVerif 形式化分析挖出的漏洞，且威力被低估。_**
    
*   **_个人觉得 BLESA 没有得到广泛关注的原因是研究团队准备的 demo 太 low 了。_**
    

BLESA (BLE Spoofing Attacks) 是 WOOT2020 上公开的攻击方法（https://www.usenix.org/conference/woot20/presentation/wu）。它揭示了 BLE GATT client 与 server 在重连时的认证逻辑缺陷。最基本的，利用 BLESA 攻击者可以在 client 无感的情况下伪装成 server，并将恶意数据注入其中。

当 client 重新连接先前已经绑定 (bonding) 的 server 时，BLE 提供了有两种可用的认证方法：

*   reactive authentication
    
*   proactive authentication
    

这两种认证方法都用于保护 server 中的高安全级 attribute 不被无权限的 client 访问，且它们均受 BLESA 的影响。本文将先后分析上述两种认证方法的原理以及漏洞点，并构造一个 PoC 用于验证漏洞。

Reactive Authentication 的缺陷
---------------------------

当 client 使用 reactive authentication（被动验证）重连 server 时，会先使用低安全级请求访问 server 的高安全级 attribute。如果 server 返回了错误的信息，告诉 client，“我们所处的安全级不同，你应该使用高安全级读取这些 attribute”，那么 client 再改为高安全级来访问 server 的这个 attribute。高安全级 attribute 意味着，client 在操作它时需要加密通信流量并通过权限验证。该认证方法的流程如下：

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7fibiavmBwJgNO612gQERJTbXRe6eibZ3KQjM1iawWObdrU3OEQxxNAbyEcg/640?wx_fmt=png)

可以发现，client 是否从 low security level 转换为 high security level，取决于 server 是否返回 `ATT_ERROR_RSP` PDU。一个实际的例子如下，首先 client 使用 `ATT_READ_REQ` PDU 在低安全级下读取 server 中高安全级的 attribute (0x0022):

```
BluetoothAttributeProtocol
Opcode:ReadRequest(0x0a)
0.......=AuthenticationSignature:False
.0......=Command:False
..001010=Method:ReadRequest(0x0a)
Handle:0x0022
```

然后 server 返回携带 Insufficient Authentication (0x05) 错误码的 `ATT_ERROR_RSP` PDU，告诉 client 应该转换为高安全级再访问：

```
BluetoothAttributeProtocol
Opcode:ErrorResponse(0x01)
0.......=AuthenticationSignature:False
.0......=Command:False
..000001=Method:ErrorResponse(0x01)
RequestOpcodeinError:ReadRequest(0x0a)
0.......=AuthenticationSignature:False
.0......=Command:False
..001010=Method:ReadRequest(0x0a)
HandleinError:0x0022
ErrorCode:InsufficientAuthentication(0x05)
```

此时，如果攻击者伪装成 server，在 client 使用低安全等级请求数据时，不用 `ATT_ERROR_RSP` PDU 返回错误码，而直接返回成功，即响应携带 attribute 值的 `ATT_READ_RSP` PDU，那么攻击者就可以在没有 bonding information 的情况下将恶意数据打入 client：

```
BluetoothAttributeProtocol
Opcode:ReadResponse(0x0b)
0.......=AuthenticationSignature:False
.0......=Command:False
..001011=Method:ReadResponse(0x0b)
Value:5465737443686172616321
```

被错误实现的 Proactive Authentication
-------------------------------

当 client 使用 proactive authentication 重连 server 时，client 会主动与 server 建立高安全级的连接，并使用配对 / 绑定阶段与 server 交换的各种 key 来证明自己有权限读取高安全级的 attribute 以及做流量加密。它与 reactive authentication 最大的区别是 client 不会再用低安全级尝试读取 server 中的 attribute，而直接在高安全级下读取。下面是这种重连情况的流程：

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7f16Fj3bRPsgwy5gIAbVKwt9RE9SM3pQia0kia62pGqGbpdtzB74lFcsQQ/640?wx_fmt=png)

从上面的流程可以看出，client 连接建立后，就立即使用与 server 绑定后共享的 LTK (Long Term Key) 进入了高安全级。之后 client 与 server 的交互全部都在高安全级下完成。这种方式虽然在设计上是相对安全的，然而很多蓝牙协议栈，比如 Android 11 使用的 Fluoride 蓝牙协议栈，并没有正确的实现整个流程，从而导致了安全问题。

现在来阐述具体的漏洞点。当 client 使能高安全级的连接时，server 也需要使用同样的 LTK 将连接带入高安全级。显然由于攻击者并没有在先前与 client 绑定，所以拿不出有效的 LTK，即无法伪装成 server 欺骗 client 开启高全级进行通讯。

合理的情况是，一旦 client 发现 server 没有有效的 LTK，那么连接就应该终止，但是以 Android 11 Fluoride 蓝牙协议栈为例，它的实现并没有终止连接，而是回到低安全级试图继续访问恶意 server 中的 attribute。最终导致 server 可以对该协议栈注入恶意数据。

PoC 构造与复现
---------

现在构造一个 PoC 来验证 Proactive Authentication 情形下的 BLESA 漏洞。

首先我们需要自己造一个配置了高安全级 attribute 并且可控的 GATT server。这点直接使用蓝牙协议栈提供的接口即可。然后让该 server 与 Android 手机完成绑定，如下：

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7fI1lOSoX03vXePlDGaAxsSSXZSdsuaJibNphdmJYHib7sFicKy70nM0kMQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7f8ooNxJHnocuA68vxyOUQY6XsYjLc2csBK4RhXK0w4wswU8WxNkn6og/640?wx_fmt=png)

此时在高安全级下，client 读取 server 的 attribute 可得到数据 “TestCharac”：

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7fFSYZG5LibAbM7Rg0sPSuWLUqmuUErpzkofxD5ZgRpJfp8qxw5gQQUuA/640?wx_fmt=png)

接着，断开恶意 server 与 Android 手机的蓝牙连接，并删除 server 里存放的 bonding information，比如：

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7f0ib8CY4VRaAz87DqBzibibegfO8rETeFxqTt6ZUDGUkbK51LiaiaNriaiathA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7fGfSF5IRKrrG1d9k22ibAgxzIO3GoZiaVxoHlzeQjKbpOlQwZE7F5ibH5A/640?wx_fmt=png)

此时我们的 server 已经失去了再次进入高安全级所需的 bonding information。随后我们修改 server 中 attribute 的 value，并将其置为低安全级。接着重启蓝牙服务与恶意 server。最后让 Android 手机重连该恶意 server，并读取 attribute。可以发现这次读取 attribute 后，Android 仍显示与 server 成绑定状态，且攻击者的数据 “BLESA PoC” 已经在低安全级下注入到了 Android 手机中：

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7f3icjco7VJ7VH6fdamW9LXDvkvQGl2qb3zY9BMGZY8ntK0VibdhSaGdHQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncVBr7MWYEAW6nncK1Bhh7ficJnLHDez6RudsenZeNKvFtspiamD3P7RGM93faEe73fCKuNRAGPMleg/640?wx_fmt=png)

**HatLab 知识星球**

![](https://mmbiz.qpic.cn/mmbiz_jpg/AvAjnOiazvndGfGrpT80YdwrFNbKjkeGcfu7ecKgWELGIYNZicVHd4W9kiabmWia8iadzzNziaJmq8HKiaykUoGAh15icQ/640?wx_fmt=jpeg)

**关于我们**

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncqK93hfU0vQk8aC2V9ibNnulgspSmTkHM6CuE76mJb49regfNeG5viaAc8nPDXEa6y1iacxtgN7Htfw/640?wx_fmt=png)

**人才招聘**

**一、IoT 无线电安全研究员**

**岗位职责：**

- 无线通信协议的通用漏洞挖掘；

- 无线通信应用系统的漏洞挖掘，如智能设备等。

**任职要求：**

- 掌握无线通信基本原理及数字信号处理理论，熟悉各种调制解调算法，信道编码算法等；

- 熟悉 C/C++、MatLab、Python 等编程语言；

- 熟悉至少一种常见无线通信协议及其安全问题，如 Wi-Fi、Bluetooth、Zigbee、4/5G 等；

- 熟练掌握 SDR 外设和 GNURadio 等工具的使用。

**加分项：**

- 具有信息安全公司实习经验；

- 有嵌入式固件逆向分析经验；

- 参加 CTF 比赛并获奖；

- 有智能设备的破解经验；

- 通信工程、信息安全专业

**二、IoT 固件安全研究****员**

**岗位职责：**

- 物联网设备固件、二进制安全研究和漏洞挖掘

- 物联网安全项目支撑

- 跟进最新公开的 1day 漏洞，进行漏洞分析

- 物联网安全前沿技术、创新性项目研究

**任职要求：**

- 熟悉 C/C++/Perl/Python/PHP/Go/Java 其中一门或多门编程语言

- 熟悉二进制常见安全漏洞，有具体设备漏洞调试的经验

- 熟悉固件漏洞分析和调试，掌握 MIPS、ARM 指令集架构的漏洞利用方法

- 掌握常见物联网设备通信协议，如 HTTP、RTSP、UPNP、MQTT 协议等。

- 掌握使用 python 语言编写 exp 脚本的能力

- 掌握物联网云端、APP 端的基本测试方法

- 较强的独立工作和学习能力，有钻研精神，乐于分享

**加分项：**

- 熟悉硬件调试、分析、通过硬件方式提取固件的能力

- 熟悉常见无线通信协议原理，如 BLE/LE/Zigbee/Sub-1G 等。

- 具有嵌入式固件、裸机固件逆向分析的经验

- 具有第三方开源组件、大型网络设备的漏洞挖掘经验

- 具有物联网实战漏洞挖掘经验并获取过 CVE（CNVD、CNNVD）编号

- 参与国内外安全大会的议题演讲

- 参与 GeekPWN、补天杯破解赛、天府杯等智能设备破解大赛并取得名次

**三、IoT 高级固件安全研究员**

**岗位职责：**

- 物联网设备固件、二进制安全研究和漏洞挖掘

- 物联网安全项目支撑

- 跟进最新公开的 1day 漏洞，进行漏洞分析

- 物联网安全前沿技术、创新性项目研究

**任职要求：**  

- 熟悉 C/C++/Perl/Python/PHP/Go/Java 其中一门或多闷编程语言

- 熟悉二进制常见安全漏洞，有具体设备漏洞调试的经验

- 熟悉固件漏洞分析和调试，掌握 MIPS、ARM 指令集架构的漏洞利用方法

- 掌握常见物联网设备通信协议，如 HTTP、RTSP、UPNP、MQTT 协议等。

- 掌握使用 python 语言编写 exp 脚本的能力

- 掌握物联网云端、APP 端的基本测试方法

- 较强的独立工作和学习能力，有钻研精神，乐于分享

**加分项：**

- 熟悉硬件调试、分析、通过硬件方式提取固件的能力

- 熟悉常见无线通信协议原理，如 BLE/LE/Zigbee/Sub-1G 等。

- 具有嵌入式固件、裸机固件逆向分析的经验

- 具有第三方开源组件、大型网络设备的漏洞挖掘经验

- 具有物联网实战漏洞挖掘经验并获取过 CVE（CNVD、CNNVD）编号

- 参与国内外安全大会的议题演讲

- 参与 GeekPWN、补天杯破解赛、天府杯等智能设备破解大赛并取得名次

**四、IoT 硬件安全研究员**

**岗位职责：**

- 嵌入式方向的安全漏洞挖掘；

- 辅助嵌入式系统硬件软件设计与研发。

**任职要求：**

- 至少掌握 Go、Lua 中的一种编程语言的基本用法。

- 熟练使用 C 语言，了解基本的 libc 原理，二进制漏洞挖掘原理；

- 熟练使用 Linux 操作系统，对 Linux 工作原理有比较深入的研究；

- 掌握阅读电路原理图的能力，具有一定的 PCB 逆向至原理图的能力；

- 了解一种 RTOS 操作系统的栈 / 堆分配结构、任务调度实现方法；

- 了解数字电路原理，具有较扎实的计算机系统结构知识，理解操作系统原理；

- 了解一种嵌入式 Bootloader 和一种嵌入式操作 OS 的编译及开发方法；

- 对常见存储器类芯片的工作原理和通用访问方式有了解；

- 了解 WEB 或 PWN 方向的漏洞挖掘过程，会使用相关工具如 Zap、IDA 等，会自行编写漏洞利用工具；

- 了解基本的侧信道攻击的原理，至少包含电压注入攻击和时钟注入攻击；

**加分项：**

- 具有网络安全公司实习经验；

- 具有知名 IoT 网络安全赛事经验；

- 有设计原理图或 PCB 布局经验；

- 熟练掌握飞线、挖板技巧；

- 有 AVR，ARM，MIPS，Xtensa 等内核的 MCU/SoC 开发经验；

- 向知名平台提交过物联网方向的漏洞报告；

- 了解芯片侵入式固件提取原理及流程，具有代码保护逆向破解经验（芯片抄板）；

- 了解各种芯片安全认证等级规范（包含银联方向和车联网方向），可独立分析其认证流程中的漏洞；

**五、嵌入式安全研发工程师**

**岗位职责：**

- 嵌入式系统硬件软件设计与研发；

- 辅助安全研究人员设计研究所使用的实验设备；

- Allwinner、MediaTek SoC 方案开发；

- Xilinx Zynq PetaLinux 开发（仅 PS Linux 侧开发）；

- 一般性 8 位 / 32 位 MCU 开发；

**任职要求：**

- 熟练使用 C 语言，可规范使用指针，结构体，联合体，了解基本的 libc 原理；

- 基本掌握 Go 语言，了解 Go 的设计思想、语法规则；

- 熟练使用 Linux 操作系统，对 Linux 工作原理有比较深入的研究，可自主开发内核态外设驱动（PCI-e 类）；

- 掌握一种 RTOS 操作系统的开发流程及其工作原理。

- 熟练掌握交叉编译工具链的使用方法，掌握主流的 buildroot、openwrt 项目的使用方法；

- 熟练掌握原理图绘制能力，至少可以独立完成数字电路部分的设计；

- 熟练焊接 0402，0201，QFN，BGA 等元器件封装（非焊工，调试板子基本技能）；

**加分项：**

- 对网络安全行业、物联网安全有一定理解；

- 实现过 ARM 或 MIPS 或 PowerPC 指令集的 x86 虚拟机；

- 了解芯片侵入式固件提取原理及流程，具有代码保护逆向破解经验（芯片抄板）；

**感兴趣的小伙伴请联系姜女士，或将简历投送至下方邮箱。（请注明来源 “研究院公众号”）**

**联系人：姜女士  
邮箱：double.jiang@dbappsecurity.com.cn  
手机；15167179002，微信同号**