> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ltOlhzOSb0wwle7vCooM4w)

**本文首发于****奇安信攻防社区**  

**社区有奖征稿**

· 基础稿费、额外激励、推荐作者、连载均有奖励，年度投稿 top3 还有神秘大奖！

· 将稿件提交至奇安信攻防社区（点击底部 阅读原文 ，加入社区）

[点击链接了解征稿详情](https://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489051&idx=1&sn=0f4d1ba03debd5bbe4d7da69bc78f4f8&scene=21#wechat_redirect)

**0x00 简介**
-----------

近日，国外安全研究员 Mathy Vanhoef 公布了 FragAttack 系列 WiFi 漏洞，其中 802.11 协议设计漏洞影响几乎所有 WiFi 设备。

针对 WiFi 的漏洞大致可以分为三类:

1.  802.11 协议设计漏洞 : 协议标准层面的设计漏洞，通常为逻辑漏洞，由于是协议标准层面的漏洞，所以影响极为广泛。
    
2.  802.11 协议栈实现漏洞 : 即 WiFi 芯片、WiFi 驱动在实现 WiFi 功能时出现在代码层面的漏洞。
    
3.  WiFi 应用层漏洞 : 针对于 WiFi 应用层的漏洞点并不广泛，多是一些 SSID 或 Vendor 字段在上层应用发生漏洞，或者是在一些特殊的机制如 smartconfig 配网中出现问题。
    

FragAttacks 主要涉及 3 个 802.11 协议设计漏洞：

1.  **A-MSDU 帧注入攻击 (CVE-2020-24588)**
    
2.  **混合密钥攻击 (CVE-2020-24587)**
    
3.  **分片缓存攻击 (CVE-2020-24586)**
    

与多个协议栈代码实现漏洞:

1.  接受纯文本广播片段作为完整帧 (CVE-2020-26145)
    
2.  在加密网络中接收 RFC1042 标准开头的纯文本 A-MSDU 帧 (CVE-2020-26144)
    
3.  在受保护的网络中接收纯文本数据帧 (CVE-2020-26140)
    
4.  在受保护的网络中接收分片帧的纯文本数据帧 (CVE-2020-26143)
    
5.  尚未完成对发送发身份验证的情况下转发 EAPOL 帧 (CVE-2020-26139)
    
6.  重新组装具有非连续数据包编号的加密片段 (CVE-2020-26146)
    
7.  重新组装混合的加密 / 明文片段 (CVE-2020-26147)
    
8.  将碎片帧作为完整帧处理 (CVE-2020-26142)
    
9.  未验证分段帧的 TKIP MIC(CVE-2020-26141)
    

其中协议栈代码实现漏洞大多是与 3 个协议设计漏洞相关联的漏洞，本文主要对 3 个协议设计漏洞进行分析。

**0x01 802.11 协议基础知识**
----------------------

此章节简单介绍 802.11 协议一些基础知识。

我们以手机通过 WiFi 连接路由器这一通信流程为例，来对 802.11 协议有一个快速的了解。

通常我们将提供 WiFi 信号的设备定义为接入点 (AP)，连接到接入点的设备称之为工作站 (STA)，在当前例子中路由器为 AP，手机为 STA。

802.11 协议中存在**信道**这一概念，WiFi 信号依照 802.11 协议运行在不同频段上，信道便是区分频段的一个定义，国内使用 1 至 13 信道 (2.4GHz)。

路由器在某一信道广播 Beacon 帧，Beacon 帧中包含 AP 的一些基本信息如 SSID、速率。

手机在扫描时会不断切换无线网卡信道来接收不同信道的 AP 信号。

以 WPA2 认证方式为例，STA 与 AP 建立链接流程为:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ69ahVR4gdVq38Ttkc5dWicIYzCxLNTicypibC7eXGHjjVR2rXMYh5Aot6w/640?wx_fmt=png)

1.  AP 广播 Beacon 帧。
    
2.  STA 发送 Probe Request 帧请求连接。
    
3.  经过 Authentication、Association 交互流程后，双方进入 4 步握手流程。
    
4.  通过 4 步握手，双方协商通信密钥。
    
5.  STA 与 AP 使用密钥加密通信流量，但 802.11 帧头部不做加密。
    

以上交互的帧均可通过无线网卡进行嗅探，但攻击者在不知道通信密钥的情况下，无法解密加密数据。

### **1.** **硬件设备**

经笔者测试，可以使用 3070 芯片系列网卡复现攻击。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6icLibuOb1Q9Bd6hZbyJ1QWvvzYzASNHFkAEia4hWJYez3uWOibuyjJ7vIg/640?wx_fmt=png)

### **2. Multi-Channel MitM （多信道中间人攻击）**

多信道中间人攻击是 Fragattack 中提到的一种攻击场景。

攻击者在不同信道上克隆目标 AP，搭建一个伪 AP。

可以使用 Deauth 攻击迫使目标 STA 连接到伪 AP，进而转发目标 STA 和目标 AP 之间的通信流量。由于只是单纯转发 802.11 协议帧，此攻击不需要知晓目标 AP 的 wifi 密码。

802.11 协议有提及对抗这种中间人攻击的方案，但实际上并没有实行。所以在实际中，这种攻击可以稳定实现，不过需要以下条件:

1.  2 个无线网卡，一个用于搭建伪 AP，一个用于连接目标 AP 实现流量转发，其中伪 AP 与目标 STA 同一信道，流量转发网卡与目标 AP 同一信道。
    
2.  攻击者需要在目标 AP 与目标 STA 无线信号工作范围内。
    

Multi-Channel MitM 示意图:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6PgTibiaLUObeWtI79FhuVib7UsXGaialYvXcs0NVZ2iccXsckpnSXiayw6zA/640?wx_fmt=png)

### **3. 聚合帧（A-MSDU）**

每个 802.11 帧在传输时都必须带上头部，当多个 802.11 帧的数据段很小时，可以将多个帧聚合到一个帧中，复用一个头部以提高传输效率。

正常的 IP/TCP 协议帧封装在 802.11 数据帧中的格式为:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6eIUMKXAh3OG9qVV9HPUEonGpYWeDuusVDFhagUcYic7pXqfAMlQicvlQ/640?wx_fmt=png)

在 Wireshark 中可以看到更直观的结构:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6tiajEBXicDGibaiax6GNSDxCibZYdGhfKagSDZwaoSxvZLSyRPk9kVqWNicA/640?wx_fmt=png)

判断当前 WiFi 数据帧是不是 A-MSDU 帧的依据是 802.11 头部的 Qos Control 字段中的 flag 标志位:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ66GvrWJCufw7cFeXCbwrHgGHhWGHwRjWOKY0rXZRN7Ygom4kqrPzeUw/640?wx_fmt=png)

A-MSDU 帧中可以包含多个子帧，A-MSDU 子帧包含 TCP/IP 层数据，并在头部添加 Destination、Source 与 Length 字段。

A-MSDU 帧在 wireshark 中的结构如下:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ650S4Mf7ZTCpXLOeSg2sMFSJSCYzmFONfydT5XiasGhNrWmIpRX0uGQQ/640?wx_fmt=png)

### **4. 分片帧 (Fragment)**

当单个 802.11 帧长度过大时，通过分片机制可将单个帧分为多个分片帧进行传输，单个分片帧与正常 802.11 帧格式相同。分片帧通过 802.11 帧头部 FC 字段中的标志位表示当前分片是否为最后一分片:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6DPCr4qwMNv5BUKGEbicBjiaXPdaiafa2fEvsic44ILJ3jkNpPRwnl5Uk3g/640?wx_fmt=png)

同一序列的分片必须拥有相同的序列号 (`Sequence number`) 与递增的分片号 (`Fragment number`)

`Sequence number`与`Fragment number`同样在 802.11 帧头部定义:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6GkGTp8hsyfR3OOqKSzmjqrlUwzNSvIlY2kC8CcdEyNjhzMqwSFErlQ/640?wx_fmt=png)

**0x02 A-MSDU 帧注入攻击 (CVE-2020-24588)**
--------------------------------------

*   攻击条件
    

1.  近场
    
2.  客户端需请求攻击者服务器
    

*   利用效果
    
    在不接入 AP 网络的情况下向网络中任意设备注入 TCP/IP 协议数据帧，如向某个设备端口发送 tcp/udp 探测报文。
    
*   原理
    
    此攻击需要使用`Multi-Channel MitM`攻击场景，攻击者作为中间人转发 STA 与 AP 的无线通信流量，**并且攻击者不知晓目标 AP WiFi 密码**。
    
    当 STA 与 AP 建立链接并开始进行 TCP/IP 数据通信时，攻击者拦截通信的数据帧，数据帧的数据段虽然被加密，但 802.11 头部是明文传输，所以 A-MSDU flag 不受保护 (802.11 协议定义了 SPP 机制，可对 A-MSDU flag 进行认证，但实际中并没有实施此措施)，攻击者可将此标志位设置为 1。
    
    那么数据段被解密后就会按照 A-MSDU 格式进行解析。
    
    但攻击者无法加解密数据段，所以需要一个场景来使攻击者可修改数据段明文信息。通过社工使 STA 访问攻击者的服务器，通过修改服务器返回的 Response 来控制部分 802.11 数据帧的数据端内容。
    
    ![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6vN9mmJlxUT8nicEuGa70GuLWcTbAGqpcibneZ6cic9ibmS61pryeL3F6bw/640?wx_fmt=png)
    
    上图红色部分不可控，绿色部分可控，黄色部分可控一部分。
    
    `LLC/SNAP`字段会被解析为 A-MSDU 子帧的 Destination 等字段，导致第一个 A-MSDU 子帧的各个字段被填入不合法数据，目标解析第一个子帧时会将其丢弃。所以攻击者需要构造第二个 A-MSDU 子帧完成注入攻击。
    
*   攻击流程:
    

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ63fc0UpPDLMCqsugibuI3LsTnic3zoXInDbgqo8CsPVq4xJCicBpH5tHww/640?wx_fmt=png)

1.  攻击者使用`Multi-Channel MitM`攻击转发 STA 与 AP 802.11 通信流量，并社工 STA 访问攻击者服务器上的资源，比如图片。
    
2.  服务器收到 request 之后，将 response 的 TCP/IP 层的数据按照 A-MSDU 子帧格式进行构造。由于 LLC/SNAP 字段不可控，所以第一个 A-MSDU 子帧的头部会被 LLC/SNAP 填充，我们需要构造 IP 层的数据，将第一个子帧格式修复。并构造合法的第二个 A-MSDU 子帧。
    
3.  AP 将 response 封装为 802.11 数据帧，攻击者截取此数据帧，并将其头部 A-MSDU flag 标志位修改为 1(数据帧的数据段会被加密，但头部是明文)。
    
4.  STA 解密此数据帧后会使用 A-MSDU 格式解析数据，第一个子帧由于头部字段不合法而被丢弃，第二个子帧为合法子帧，会被正常解析为 TCP/IP 层数据帧。最终，攻击者达到注入任意 TCP/IP 帧的攻击效果。
    

攻击者修改后的数据帧 (**解密视图**):

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6DFJnQE7AMqgm2bwiaiaiaZSov2uJyyHvoYF8CC3iaV8rVaNEMBSLHVGicjQ/640?wx_fmt=png)

这里攻击者注入了一个 icmp request 包，通信方向为: 192.168.100.1 ==> 192.168.100.2

在 192.168.100.1 机器上抓包，观察到 192.168.100.2 返回的 icmp response，攻击成功:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6bIUictDeWGcp6Dbib70Y6XsbYwQuYSVWY2Le7ia9qvSyUXgK9icFn18a5Q/640?wx_fmt=png)

**0x03 混合密钥攻击 (CVE-2020-24587)**
--------------------------------

*   攻击条件
    

1.  近场
    
2.  客户端需请求攻击者服务器
    

*   利用效果
    
    在不接入 AP 网络的情况下，泄露网络中某个分片帧的明文内容。
    
*   原理
    
    当单个数据帧长度过大时，可以使用帧分片机制，将一个帧分为多个帧进行传输。
    
    AP 收到单个分片帧后会将其解密并存放在内存中，但并不会判断这些分片是否使用同一密钥加解密，而是单纯的使用序列号将解密后的分片帧组合起来，这就导致了混合密钥攻击。
    
    **此攻击无需知晓目标 AP WiFi 密码**。
    
*   攻击流程
    

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6CN1BQYibXR9DHR0aicMeDQ2kYs8Eic3cCMzPWCjBn7bcfRpacgSzQhExw/640?wx_fmt=png)

1.  攻击者使用`Multi-Channel MitM`攻击转发 STA 与 AP 802.11 通信流量
    
2.  攻击者社工诱使 STA 访问攻击者服务器较大资源 (图片、Js 文件)。STA 发送分片帧，并使用密钥 k 加密分片帧，其中分片的序列号 (`Sequence number`) 为 s1，分片号 (`Fragment number`) 分别为 n，n+1
    
3.  攻击者转发分片号为 n 的分片 (Frag0)，并丢弃分片号为 n+1 的分片。分片 n 中携带 IP 头部等信息，AP 使用密钥 k 解密 Frag0 并存放在内存中。
    
4.  STA 与 AP 重新握手 (AP 在配置 rekey 机制时，STA 与 AP 会定时重新握手更新密钥)，协商密钥为 m。
    
5.  当攻击者嗅探到 STA 发送分片时，捕获分片号为 n+1 的分片 (Frag1)，将其序列号 (`Sequence number`) 修改为 s1，并设置为最后一个分片，该分片可能携带敏感信息 (HTTP 协议)。AP 使用密钥 m 解密 Frag1 并存放在内存中。
    
6.  AP 将 Frag0 与 Farg1 组合为完整数据包，由于分片 Frag0 中的地址指向攻击者的服务器 (3.5.1.1)，该数据包则会发送至攻击者的服务器，导致分片 Frag1 中的内容泄露。
    

**0x04 分片缓存攻击 (CVE-2020-24586)**
--------------------------------

*   攻击条件
    

1.  近场
    
2.  已知 AP WiFi 密码
    

*   利用效果
    
    泄露网络中某个分片帧的明文内容
    
*   原理
    
    分片缓存攻击基于混合密钥攻击，区别在于第一组分片由攻击者发送而不是 STA，所以攻击者需要知道 AP 的 WiFi 密码。此攻击能够实现在于即使 STA 断开连接，AP 依然会将解密的分片缓存在内存中。
    
*   攻击流程
    

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6kG2dKTn5EicBYsyzlqnkJ6uYre8Swzgcw40UOwib9uyeyCgSWcVxMpGRScTA6NASIyqR8g8D8mH7w/640?wx_fmt=png)

1.  攻击者伪装成 STA 与 AP 建立链接，并请求攻击者服务器较大资源，之后只发送第一个分片。
    
2.  AP 使用密钥 k 将 Frag0 解密后存在内存中。之后攻击者与 AP 断开链接。
    
3.  STA 与 AP 建立链接，攻击者使用`Multi-Channel MitM`攻击转发 STA 与 AP 802.11 通信流量
    
4.  当攻击者嗅探到 STA 发送分片时，捕获分片号为 n+1 的分片 (Frag1)，将其序列号 (`Sequence number`) 修改为 s1，并设置为最后一个分片，该分片可能携带敏感信息。AP 使用密钥 m 解密 Frag1 并存放在内存中。
    
5.  AP 将 Frag0 与 Farg1 组合为完整数据包，由于分片 Frag0 中的地址指向攻击者的服务器 (3.5.1.1)，该数据包则会发送至攻击者的服务器，导致分片 Frag1 中的内容泄露。
    

**0x05 参考资料**
-------------

1.  https://papers.mathyvanhoef.com/usenix2021.pdf
    
2.  https://www.youtube.com/embed/88YZ4061tYw
    
3.  https://www.fragattacks.com/#notpatched
    
4.  https://github.com/vanhoefm/fragattacks
    
5.  https://inet.omnetpp.org/docs/showcases/wireless/aggregation/doc/index.html
    

**0x06 关于我们**
-------------

**天工实验室**隶属于奇安信技术研究院，专注于**物联网、车联网**领域的安全研究，包括物联网协议安全、固件安全、无线安全、智能网联汽车及自动驾驶安全等，服务于国家和社会对网络空间安全的战略需求。团队成员秉承 “天工开物、匠心独运” 的创新使命和工匠精神，在物联网漏洞挖掘与攻防领域有丰富的经验积累，漏洞研究成果连续在 GeekPwn、天府杯等漏洞破解赛事中斩获多个奖项，漏洞挖掘创新型方法发表于 Usenix 等国际顶级会议。

END

  

【版权说明】本作品著作权归天工实验室所有，授权补天漏洞响应平台独家享有信息网络传播权，任何第三方未经授权，不得转载。

**敲黑****板！转发≠学会，课代表给你们划重点了**

**复习列表**

  

  

  

  

  

[特斯拉 TBONE 漏洞分析](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247490085&idx=1&sn=2a9d747c2fe5de3f04aecfb3d8583a35&chksm=eafa5269dd8ddb7f8196c3677df6056c0b71082cef769b9b56c9e0e462a06924d24a201f38a0&scene=21#wechat_redirect)

  

[关于影响超 600W 设备的通用型路由循环漏洞分析](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489890&idx=1&sn=fcf3b50d242f2363c937094ca284a32f&chksm=eafa512edd8dd83856478b212ea35f84071e3d931aee6fdf75324139daea83a42983189e936e&scene=21#wechat_redirect)

‍

  

‍[某邮件系统后台管理员任意登录分析‍](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247490009&idx=1&sn=ea120cc287ad0735237a831a7b4847cb&chksm=eafa5195dd8dd8837c3d39040368110d77d2b30f0251fa2f7e4d5e656779249b1d30fce329a0&scene=21#wechat_redirect)

  

[代码审计之 eyouCMS 最新版 getshell 漏洞](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489781&idx=1&sn=a2d0ccd466dfa95067f223c8318a316d&chksm=eafa50b9dd8dd9af45ef4fcf23074aeecc196dc72b3ff447282a9e6ea9904dcc08fe72430d30&scene=21#wechat_redirect)

‍

  

[某行业通用流程管控平台 RCE 之旅‍](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489976&idx=1&sn=a7b450efb495ab424f77d06fe4c2d1ad&chksm=eafa51f4dd8dd8e21cf2a3311161db98c8d5a53951e7d548f62112b49712e978501f0cc5a699&scene=21#wechat_redirect)

  

[某开源 ERP 最新版 SQL 与 RCE 的审计过程](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489992&idx=1&sn=6a510d12d06ccf4a365f41b386a3e197&chksm=eafa5184dd8dd892fd3e9c8779571939b6dc6465cf86ac8e1d094b3994302500c394fb12ecfe&scene=21#wechat_redirect)

  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6D8InhXuGX2q6Cbw7zhMJLFcmlcnz38EApnEkFiaISicklcwbo3gnI17t54PqyYOE8LV4yczIfjdqw/640?wx_fmt=png)  

  

分享、点赞、在看，一键三连，yyds。

![](https://mmbiz.qpic.cn/mmbiz_gif/FIBZec7ucChYUNicUaqntiamEgZ1ZJYzLRasq5S6zvgt10NKsVZhejol3iakHl3ItlFWYc8ZAkDa2lzDc5SHxmqjw/640?wx_fmt=gif)

  

点击阅读原文，加入社区，获取更多技术干货！