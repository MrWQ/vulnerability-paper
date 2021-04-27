> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/GWVgRXHHiYx2bN62qhmuOQ)

作者前文介绍了宏病毒相关知识，它仍然活跃于各个 APT 攻击样本中，具体内容包括宏病毒基础原理、防御措施、自发邮件及 APT28 样本分析。本文将详细介绍什么是数字签名，并采用 Signtool 工具对 EXE 文件进行签名，后续深入分析数字签名的格式及 PE 病毒内容。这些基础性知识不仅和系统安全相关，同样与我们身边常用的软件、文档、操作系统紧密联系，希望这些知识对您有所帮助，更希望大家提高安全意识，安全保障任重道远。本文参考了参考文献中的文章，并结合自己的经验和实践进行撰写，也推荐大家阅读参考文献。  

文章目录：

*   **一. PE 文件的数字签名**
    
    1. 概念普及
    
    2.Github 网站证书验证过程
    
*   **二. 阮一峰老师告诉大家什么是数字签名**
    
*   **三. Signtool 签名 PE 文件**
    

> 从 2019 年 7 月开始，我来到了一个陌生的专业——网络空间安全。初入安全领域，是非常痛苦和难受的，要学的东西太多、涉及面太广，但好在自己通过分享 100 篇 “网络安全自学” 系列文章，艰难前行着。感恩这一年相识、相知、相趣的安全大佬和朋友们，如果写得不好或不足之处，还请大家海涵！  
> 接下来我将开启新的安全系列，叫 “系统安全”，也是免费的 100 篇文章，作者将更加深入的去研究恶意样本分析、逆向分析、内网渗透、网络攻防实战等，也将通过在线笔记和实践操作的形式分享与博友们学习，希望能与您一起进步，加油~
> 
> 推荐前文：网络安全自学篇系列 - 100 篇
> 
> https://blog.csdn.net/eastmount/category_9183790.htm

作者的 github 资源：  

*   逆向分析：https://github.com/eastmountyxz/
    
    SystemSecurity-ReverseAnalysis
    
*   网络安全：https://github.com/eastmountyxz/
    
    NetworkSecuritySelf-study
    

> 声明：本人坚决反对利用教学方法进行犯罪的行为，一切犯罪行为必将受到严惩，绿色网络需要我们共同维护，更推荐大家了解它们背后的原理，更好地进行防护。该样本不会分享给大家，分析工具会分享。（参考文献见后）

一. PE 文件的数字签名
=============

1. 概念普及
-------

(1) PE 文件  
PE 文件的全称是 Portable Executable，意为可移植的可执行的文件，常见的 EXE、DLL、OCX、SYS、COM 都是 PE 文件，PE 文件是微软 Windows 操作系统上的程序文件（可能是间接被执行，如 DLL）。后续文章会详细分析 PE 文件格式。

(2) 为什么要对 PE 文件进行数字签名呢？

*   防篡改：通过对数字签名的验证，保证文件未被非法篡改。
    
*   降低误报：安全软件通过验证文件是否有正规厂商的数字签名来降低误报。
    

(3) PE 文件数字签名及验证过程  
签名：

*   软件发布者使用散列算法（如 MD5 或 SHA）计算 PE 文件的散列值。
    
*   软件发布者使用私钥对散列值进行签名得到签名数据。
    
*   将签名私钥对应的公钥和签名数据等以证书的形式附加在 PE 文件之中，形成经过数字签名的 PE 文件。
    
*   软件发布者将经过数字签名的 PE 文件进行发布。
    

验证：

*   从 PE 文件证书中提取软件发布者的公钥、使用的散列算法、签名算法、原始散列值的签名数据。
    
*   使用提取的公钥和对应签名验证算法将签名数据还原为原始 PE 文件的原始散列值。
    
*   对现有 PE 文件使用同样的散列算法计算出对应的散列值。
    
*   对比两个散列值是否一致，从而判断数据是否被破坏和篡改。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7NFk1RUH6hia4icFDeWv5qIohfSPJt0B1icMcqaiciaReYEJ25F80oWXsGsw/640?wx_fmt=png)

(4) PE 文件数字签名的总体结构  
PE 文件数字签名信息存放在 Certificate Table 位置，同时 PE 文件可选文件头 DataDirecotry 第 5 项记录文件偏移及大小。

> 下一篇文章作者尝试详细讲解 PE 文件结构及签名解析。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7cczicFzVMe6XCrBtVMoib2EfDjPNWeLBhC5Y3BZkuNicIjkG0ME6icFSmQ/640?wx_fmt=png)

使用 PEView 查看签名前后对比图，可以看到 Certificate Table 存储相关签名信息。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7JeQAh8RojnobokXWXPjLSH2cLSGTbWp86rPjDGOhb3p6wO7zO1czlQ/640?wx_fmt=png)

(5) PE 文件数字签名查看  
这里以 Zoomit.exe 程序为例，我们可以看到经过数字签名后的 PE 文件还会多出一个 “数字签名” 的属性，点击详细信息可以查看对应的证书。  
![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7CUiansu2oWsjPB4Z8hjicIbVQiamyZiasNEpzOcxyZXKicE7B2BicVYWz8Hw/640?wx_fmt=png)

对应的证书信息及证书路径如下图所示，包括签名算法、哈希算法、有效期、颁发者信息等。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7iakA8T9hClEQoAQOWcwwTYEfPdkrc13v2MffTaqFFTgATMgjLLzyeHg/640?wx_fmt=png)

(6) 微软数字签名证书查看  
接着，我带领大家看看 Windows 证书。运行中输入 “certmgr.msc”，可以看到这里面有 5 个系统默认的 ECC 签名的根证书，如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7iak5KjzAMpjXxpnFjodlrMZTibCmLHFgtc6ibBstIl9CZibn1CvNpiaicnhQ/640?wx_fmt=png)

我们随意导出其中一个根证书，导出直接选择 Base64 编码那个就行。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7HPUwJaalf7w2YfjicNNG6AseMVgdHZLLiavC7gOm0gEHmXVf4Lo74CXA/640?wx_fmt=png)

可以看到导出的 ECC 密钥证书如下图所示，包括证书的有效期等信息。这就是微软在实现椭圆曲线加密（ECC）算法的数字证书，位于 CryptoAPI.dll 文件，也是被我们利用来伪造可信任来源的签名漏洞。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7lQlciaBLt3CyGe0uzfViadnSe5Cibiaic2AQytQpD8M98F8eQpIRaOfwWZQ/640?wx_fmt=png)

(7) 数字签名常用算法及应用领域  
数字签名常用算法包括：

*   RSA 数字签名算法  
    基于大整数分解问题，MD5、SHA
    
*   DSA 数字签名算法  
    基于离散对数问题
    
*   ECDSA 椭圆曲线数字签名算法  
    ECC+DSA，椭圆加密算法，属于 DSA 的一个变种，基于椭圆曲线上的离散对数问题
    

其应用领域包括：

*   PE 文件数字签名
    
*   HTTPS 数字签名
    
*   电子邮件数字签名
    
*   Office 文档数字签名
    
*   代码数字签名
    

2.Github 网站证书验证过程
-----------------

接着看看 Github 网站进行微软证书验证的过程。

*   在 Windows 系统访问一个网站 (例 Github.com) 时，该网站会向 Windows 系统发送由第三方权威机构 (CA) 签署的网站证书。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7CmD9ZibeP8LNuQibSibaExhaLjHxP5jjPW3dNicIqXR1xQibhFhvHQRk1tw/640?wx_fmt=png)

*   Windows 系统则会验证该证书是否由 CA 颁发，若验证通过，则 Windows 系统与网站成功建立 TLS 链接。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP78JPqelSbEqfUSGO6ApicXs2kibpGbgxqAxhuuQa4VQ46SnZhBYXPgWKg/640?wx_fmt=png)

*   为了方便下一次更快的访问，Windows 将验证成功的证书放入内存中一块 Certificate Cache（证书缓存）中。在下一次校验时，如果该证书存在于缓存中，则直接取缓存中的值进行校验。这里利用 CVE-2020-0601。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7RKjvrLiacZ4VgDwtOP38iaj0ZMRibu2o8h3CM9ariby32pAh5BeOdN1ofQ/640?wx_fmt=png)

*   在成功缓存证书数据后，根据下面描述的 Windows 证书缓存机制，恶意网站可以伪造虚假的网站（例 github.com）证书且通过 Windows 验证，将自身伪装成合法网站。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7OmFDk9FndbZaJV0uMhgX4w5UmdFUgvgFmOmQxFRIBSiahdFFsQhHLAA/640?wx_fmt=png)

*   当 Windows 接收到新的证书时，Windows 将新接收的证书与已缓存证书的证书的公钥进行遍历对比，寻找匹配的值。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7T6XZk9Y606HW4xlxwaXxnjZ22UjNKeHHbwHQF8OM1S0RhNAXmZwUJw/640?wx_fmt=png)

*   伪造的恶意证书与 Windows 系统中的缓存证书有同样的公钥，但 Curve 项没有在校验范围内，所以可以通过构造自定义 Curve 来伪造证书。使得证书验证流程依然成立，但通过验证的证书已经不是之前成功验证的安全证书。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7sIPObjQeB6aun7ru6wdtlyyQCFfnCyiaKGYrpGDFrWvombnPiaPeOSdQ/640?wx_fmt=png)

在第 23 篇文章中，我们将详细复现微软证书 CVE-2020-0601 漏洞。

二. 阮一峰老师告诉大家什么是数字签名
===================

> 参考文章：  
> 数字签名是什么？- 阮一峰  
> What is a Digital Signature? - 原始网站

写到这里，您可能还是很疑惑 “什么是数字签名”？下面我通过阮一峰老师的博客进行讲解，个人认为这是一篇讲得比较清晰的原理文章，同时也包含了网络安全中加密解密、信息传输等知识。

*   (1) 假设鲍勃有两把钥匙，一把是公钥，另一把是私钥。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7Dh2P3DFuy8qiaiaHStXIjic99aqiaibAlnrGjG04Oep8WxmknWUicWyYwBWQ/640?wx_fmt=png)

*   (2) 鲍勃把公钥送给他的朋友们 ---- 帕蒂、道格、苏珊 ---- 每人一把。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7p6xTN2Z3ktYWAGbTvKLnMiaoqXFLcibcibU9FyRBIgBMtKUUTAWdDnKyw/640?wx_fmt=png)

*   (3) 苏珊要给鲍勃写一封保密的信。她写完后用鲍勃的公钥加密，就可以达到保密的效果。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7UCiaRNjlia5yg9rw9Zo9cubNbP8mvIickFnnic29AI4OyWSngdACT5EnSQ/640?wx_fmt=png)

*   (4) 鲍勃收信后，用私钥解密，就看到了信件内容。这里要强调的是，只要鲍勃的私钥不泄露，这封信就是安全的，即使落在别人手里，也无法解密。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7FEgibibUxBgCdNg4Y1POZ6cmIhkONY5adXPn9IMlMxdnWOjPQB80ntCg/640?wx_fmt=png)

*   (5) 鲍勃给苏珊回信，决定采用 "数字签名"。他写完后先用 Hash 函数，生成信件的摘要（digest）。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7tg4ZOBwH6qO5SrZ2QUTEibfpp1Lrxeu89f2FIyaHW15JqF0K0PzuVMg/640?wx_fmt=png)

*   (6) 然后，鲍勃使用私钥，对这个摘要加密，生成 "数字签名"（signature）。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7934PhaOhLqiarpvb9GZyFJaibSEVTzMsTrbTVMpDJmSryn3W4ljyxZwA/640?wx_fmt=png)

*   (7) 鲍勃将这个签名，附在信件下面，一起发给苏珊。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP79Ly9DJqwYeslFKYO9A50QEDfsuIibDsur8UabwicTOcYCgL0Bib0Uj5rg/640?wx_fmt=png)

*   (8) 苏珊收信后，取下数字签名，用鲍勃的公钥解密，得到信件的摘要。由此证明，这封信确实是鲍勃发出的。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP750K3OBF9wicgWs5svnXQdO6toH0Nd8ZUnia1VoqZr3Hpm7CO8gWFiaTCQ/640?wx_fmt=png)

*   (9) 苏珊再对信件本身使用 Hash 函数，将得到的结果，与上一步得到的摘要进行对比。如果两者一致，就证明这封信未被修改过。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7bRITJNkgBtTf8nlnicNLX5icVLpN2m56xUU0FP5JJpCAcgxlURUCorJg/640?wx_fmt=png)

*   (10) 复杂的情况出现了。道格想欺骗苏珊，他偷偷使用了苏珊的电脑，用自己的公钥换走了鲍勃的公钥。此时，苏珊实际拥有的是道格的公钥，但是还以为这是鲍勃的公钥。因此，道格就可以冒充鲍勃，用自己的私钥做成 "数字签名"，写信给苏珊，让苏珊用假的鲍勃公钥进行解密。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7g8L2N6l3kicSm2xMG4CYNuoMFe1oB5jaD8ef7EzBxsPdfiaPjFrWNPVQ/640?wx_fmt=png)

*   (11) 后来，苏珊感觉不对劲，发现自己无法确定公钥是否真的属于鲍勃。她想到了一个办法，要求鲍勃去找 "证书中心"（certificate authority，简称 CA），为公钥做认证。证书中心用自己的私钥，对鲍勃的公钥和一些相关信息一起加密，生成 "数字证书"（Digital Certificate）。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7d42F1iaOibltnFaONCguMQNHLDuf7qG7UE75eGFFtQ7TqcQmQdFJicFTw/640?wx_fmt=png)

*   (12) 鲍勃拿到数字证书以后，就可以放心了。以后再给苏珊写信，只要在签名的同时，再附上数字证书就行了。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP793aGrHbG2C0J9c93QicscuRNG9s0oD6OlE2g48ib8icX6VJLmhjAWiacvA/640?wx_fmt=png)

*   (13) 苏珊收信后，用 CA 的公钥解开数字证书，就可以拿到鲍勃真实的公钥了，然后就能证明 "数字签名" 是否真的是鲍勃签的。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP74JlI3nM0lPH46g2DwHzJHWLQfF1sHTFkGhmrVpzNNZoZlsbACgSdmg/640?wx_fmt=png)

*   (14) 下面，我们看一个应用 "数字证书" 的实例：https 协议。这个协议主要用于网页加密。首先，客户端向服务器发出加密请求。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7plUQ0MQA0jjvraQqgfhYyyYYQABXcPribvib3Ql5ibOIyibScC1tCV4aAg/640?wx_fmt=png)

*   (15) 服务器用自己的私钥加密网页以后，连同本身的数字证书，一起发送给客户端。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7rCRklU4KzgsQHvaT5kqlGSCib5BOoD2yay6jBawXOX4N0sT2fcK5ia1Q/640?wx_fmt=png)

*   (16) 客户端（浏览器）的 "证书管理器"，有 "受信任的根证书颁发机构" 列表。客户端会根据这张列表，查看解开数字证书的公钥是否在列表之内。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7KSwicwOboiaL0TZx5wWfF1NKwKkbBC5xrTt1nUqHc13rdYEw4RjPwkwg/640?wx_fmt=png)

*   (17) 如果数字证书记载的网址，与你正在浏览的网址不一致，就说明这张证书可能被冒用，浏览器会发出警告。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7F7XlU258fpj38TjekBslbOxH0RQ5uq5W7KwOD5vPMIAaia8EVcRazPg/640?wx_fmt=png)

*   (18) 如果这张数字证书不是由受信任的机构颁发的，浏览器会发出另一种警告。如果数字证书是可靠的，客户端就可以使用证书中的服务器公钥，对信息进行加密，然后与服务器交换加密信息。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7IbYEia1O9iadtV3oNQV8U954c4AbA8lomtSeu7ITic7iczYFl1VEuwN3KQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7GGg3oDggibADzTdzbZV0M0FYMuGw0N9MTCbkXqHNTBzHu03zhcsPeEQ/640?wx_fmt=png)

数字签名是为了保证数据完整性。通过它可以判断数据是否被篡改，私钥加密完的数据所有知道公钥的都可以解密，这样不安全。私钥加密的作用是为了确认身份，用对应的公钥解密摘要，则证明摘要来自谁，起到签名的作用。

三. Signtool 签名 PE 文件
====================

*   逆向分析：https://github.com/eastmountyxz/
    
    SystemSecurity-ReverseAnalysis
    
*   软件安全：https://github.com/eastmountyxz/
    
    Software-Security-Course
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP79fHiaGEyBVhNMsrrKbg67jhanCM6tpwWgA2LOC2luCBNHF0ogDXBv9g/640?wx_fmt=png)

该 test.exe 程序后续文章也会分享，均上传至 Github。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7p1iacUG2cyic29KcAaYQ7TnFiae0U8gjuicOxKDk5wFXFOKteGN6s0PyqA/640?wx_fmt=png)

第一步，通过 makecert.exe 生成需要的证书，生成两个文件分别是 test.cer 和 test.PVK。

```
cd SignToolmakecert -$ "individual" -r /sv "test.PVK" /n "CN=Windows,E=microsoft,O=微软" test.cer
```

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP783RUcHWskSbgMI5iayhTDgajA2RfRLO3BiaesdUjRu6fJ9vzNiaO3hSqg/640?wx_fmt=png)

创建过程中需要输入私钥密码，这里设置为 “123456789”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7XzawdRsPuUicIo8sCMNTTUfTPd4ItCl9IezvoPlnQIS0uaCCZBx75zw/640?wx_fmt=png)

第二步，查看证书信息，如果未信任需要点击 “安装证书”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7G6bmfnKIjWmIPxoc5ITTR0UpU450tBeQkwnAhmNNrcdvAPYbo0Q6icA/640?wx_fmt=png)

安装并信任该证书。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP71KESvx2nIW0iateolul5PQ2GicDAcHaNia9pK71O9NFw1wd2y4OytCAKQ/640?wx_fmt=png)

第三步，利用 signcode.exe 工具进行数据签名，选择需要签名的 “test.exe” 程序。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7PhQpMlAj8oT51e166ROeFZIx7226rdeBHOqM0eWajMsN6Qep9Mb7Yg/640?wx_fmt=png)

第四步，自动选择自定义选项，然后点击从文件中选择 test.cer 文件，test.cer 文件在第一个步骤生成的目录中，然后下一步。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7a0lZSSyhUrRSGgKq6aicsbm4pxSulY5HXJkUWZjRItp3kxZftficicicgw/640?wx_fmt=png)

第五步，点击浏览按钮，添加文件 test.PVK，test.PVK 文件也是在第一步生成的目录中，点击下一步，哈希算法可以选 md5，也可以选 sha1，点击下一步。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7BmQXWIxTBSX7cgfhjovkiadoiah4q2tib6npFKnL9icIUDqyNFxHsed46g/640?wx_fmt=png)

第六步，默认点击下一步，出现数据描述框，自己可以填写，也可以不填。点击下一步。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7bdu4Qf1PmDaMkqpxXj8PARPJPfLg1F62FJogTXBAgHhBJxn43iaKxFg/640?wx_fmt=png)

第七步，填写时间戳服务器 URL：http://timestamp.wosign.com/timestamp，也可以不选添加时间戳，点击下一步，完成，弹出签名成功框。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7febYsLYupee3YcCjL7JVQsDXHoTicIJc25Y8e6THcziamxPkxAUyYfaQ/640?wx_fmt=png)

第八步，此时 test.exe 文件完成数字签名，打开该 exe 文件属性，如下图所示，可以看到签名相关信息。注意，该数字签名正常且颁发者为 Windows。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7yAibk1p6QE2dWbfY47Mv0wKL1jIuFkuMpNZGkSpYIFlpx58kpUYKoBw/640?wx_fmt=png)

最后我们使用 PEView 软件打开 PE 文件，可以看到签名前和签名后的结构存在 “CERTIFICATE Table” 区别。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7GBpKQyibbeDrcJsoDP7chaqPy6Dst1wJOUInPEcWgmYdc3jLhxnPD6A/640?wx_fmt=png)

下一篇文章将详细分析数字签名的结构。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRPkYiaxKttNf6B4JiaRd9LIP7cczicFzVMe6XCrBtVMoib2EfDjPNWeLBhC5Y3BZkuNicIjkG0ME6icFSmQ/640?wx_fmt=png)

四. 总结
=====

文章写到这里，就介绍完毕，希望文章对您有所帮助。这篇文章主要讲解：

*   PE 文件数字签名
    
*   分享阮一峰老师的博客，告诉大家什么是数字签名
    
*   结合 SignTool 工具对 EXE 文件进行签名
    

作者作为网络安全初学者的慢慢成长路吧！希望未来能更透彻撰写相关文章。同时非常感谢参考文献中的安全大佬们的文章分享，感谢小伙伴和师傅们的教导。从网络安全到系统安全，从木马病毒到后门劫持，从恶意代码到溯源分析，从渗透工具到二进制工具，还有 Python 安全、顶会论文、黑客比赛和漏洞分享。未知攻焉知防，人生漫漫其路远兮，作为初学者，自己真是爬着前行，感谢很多人的帮助，继续爬着，继续加油！

学安全一年，认识了很多安全大佬和朋友，希望大家一起进步。这篇文章中如果存在一些不足，还请海涵。作者作为网络安全和系统安全初学者的慢慢成长路吧！希望未来能更透彻撰写相关文章。同时非常感谢参考文献中的安全大佬们的文章分享，感谢师傅、实验室小伙伴的教导，深知自己很菜，得努力前行。编程没有捷径，逆向也没有捷径，它们都是搬砖活，少琢磨技巧，干就对了。什么时候你把攻击对手按在地上摩擦，你就赢了，也会慢慢形成了自己的安全经验和技巧。加油吧，少年希望这个路线对你有所帮助，共勉。

前文回顾（下面的超链接可以点击喔）：

*   [[系统安全] 一. 什么是逆向分析、逆向分析应用及经典扫雷游戏逆向](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484670&idx=1&sn=c31b15b73f27a7ce44ae1350e7f708a2&chksm=cfccb433f8bb3d25c25f044caac29d358fe686602011d8e4cbdc504e3a587e756215ce051819&scene=21#wechat_redirect)
    
*   [[系统安全] 二. 如何学好逆向分析及吕布传游戏逆向案例](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484756&idx=1&sn=ef95ff95474c51fa2bd4b9b4847ebb54&chksm=cfccb599f8bb3c8fa4852416cff6695fc8dcc9aadb3295c7249c12c03cad4c146a93e6250d56&scene=21#wechat_redirect)
    
*   [[系统安全] 三. IDA Pro 反汇编工具初识及逆向工程解密实战](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484812&idx=1&sn=9b77853a5b9da0f7a688e592dba3ddba&chksm=cfccb541f8bb3c57faffc7661a452238debe09cc7a57ae2d9e9d835d6520ee441bfd9d5ad119&scene=21#wechat_redirect)
    
*   [[系统安全] 四. OllyDbg 动态分析工具基础用法及 Crakeme 逆向破解](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484950&idx=1&sn=07d8f0b20f599586ef06035354b14630&chksm=cfccb6dbf8bb3fcd6d2efcc7b6757fabd8015d86f43e3bc8ae6cb9367d19492aec881374fca2&scene=21#wechat_redirect)
    
*   [[系统安全] 五. OllyDbg 和 Cheat Engine 工具逆向分析植物大战僵尸游戏](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485043&idx=1&sn=028c702990f722d087c6c349fb34f5fb&chksm=cfccb6bef8bb3fa8882994f7412db6b769d382abbafa6b5b3bd1b5ae62dffa20e81c7170ecb4&scene=21#wechat_redirect)
    
*   [[系统安全] 六. 逆向分析之条件语句和循环语句源码还原及流程控制](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485936&idx=1&sn=b1c282021280bb24646a9bf7c0f1fa6a&chksm=cfccb93df8bb302b51ae1026dba4f8839a1c68690df0e8da3242e9c1ead0182bf6c34dd44ada&scene=21#wechat_redirect)
    
*   [[系统安全] 七. 逆向分析之 PE 病毒原理、C++ 实现文件加解密及 OllyDbg 逆向](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485996&idx=1&sn=d5e323f16ce0b3d88c678a1fc1848596&chksm=cfccbae1f8bb33f7fad687d17ba7c10312bf2d756e460217a5d60ef2af0c012336292918128d&scene=21#wechat_redirect)
    
*   [[系统安全] 八. Windows 漏洞利用之 CVE-2019-0708 复现及蓝屏攻击](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486024&idx=1&sn=102ace20c2b15f4e7a9f910b56b84aec&chksm=cfccba85f8bb33939ac7e99cae23d1b6da5a0db4e6ff8bc7535a77a46a4204855de41aa446dd&scene=21#wechat_redirect)
    
*   [[系统安全] 九. Windows 漏洞利用之 MS08-067 远程代码执行漏洞复现及深度提权](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486057&idx=1&sn=7e7899b9285ac04f0d9745b4c455b005&chksm=cfccbaa4f8bb33b25ffcd780764ad86dc63edc7dd56d09e466254f6277851b5a4a545bb209a4&scene=21#wechat_redirect)
    
*   [[系统安全] 十. Windows 漏洞利用之 SMBv3 服务远程代码执行漏洞（CVE-2020-0796）复现](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486111&idx=1&sn=e2129fc8efa79d2356c3a2deec6d52a1&chksm=cfccba52f8bb3344479fa8d201494f88ac1b0cee3e0786797dd09a17c5f4aa4a5627fd0afef0&scene=21#wechat_redirect)
    
*   [[系统安全] 十一. 那些年的熊猫烧香及 PE 病毒行为机理分析](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486188&idx=1&sn=34a1d3f2d6880dfd60917b84d3efaa5a&chksm=cfccba21f8bb3337b45cc0fb98af3ab6a1333219fe2a06d3c3c8e38b996e1039e5b0f8d14f24&scene=21#wechat_redirect)
    
*   [[系统安全] 十二. 熊猫烧香病毒 IDA 和 OD 逆向分析（上）病毒初始化](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486260&idx=1&sn=0760360d286782209e9f93d37c177c73&chksm=cfccbbf9f8bb32ef5e54058ded6072a248e3156be64213a238b47b5fa65b6909889ab0c9b7c5&scene=21#wechat_redirect)
    
*   [[系统安全] 十三. 熊猫烧香病毒 IDA 和 OD 逆向分析（中）病毒释放机理](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486423&idx=1&sn=43f77342f8900b481eaa536b9e81f737&chksm=cfccbb1af8bb320ccc6f1bd93e358b916ccb6313f9bbdcf1d9c31deebf16a2e643ce0e121113&scene=21#wechat_redirect)
    
*   [[系统安全] 十四. 熊猫烧香病毒 IDA 和 OD 逆向分析（下）病毒感染配置](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486580&idx=1&sn=20b672097bf0be1fbdf5952bb53b23a6&chksm=cfccbcb9f8bb35affbc611fc92875f9250060914d94fa1d9a7c2b9e9482fd4a50bbb33ebc42f&scene=21#wechat_redirect)
    
*   [[系统安全] 十五. Chrome 密码保存功能渗透解析、Chrome 蓝屏漏洞及音乐软件漏洞复现](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486662&idx=1&sn=6506a733804564137d40c7c070287590&chksm=cfccbc0bf8bb351d1a82737e5dc310c048f80fb5fcfe3317c7bc1b38ac6b52de60923cb92ba7&scene=21#wechat_redirect)
    
*   [[系统安全] 十六. PE 文件逆向基础知识 (PE 解析、PE 编辑工具和 PE 修改)](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486866&idx=1&sn=cd3bc433c0a6a7b1f8bcaa4295cf65ae&chksm=cfccbd5ff8bb34496b9dc20b2fd304ce1d1194fd076902127a6817362b3c52afc056126ca0ba&scene=21#wechat_redirect)
    
*   [[系统安全] 十七. Windows PE 病毒概念、分类及感染方式详解](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247487219&idx=1&sn=1e123c330cb0499400d5529cbd5f47f3&chksm=cfccbe3ef8bb3728118a0aab982a56b3ea66f320a221c6a318263104a35f5aee8d3545612683&scene=21#wechat_redirect)
    
*   [[系统安全] 十八. 病毒攻防机理及 WinRAR 恶意劫持漏洞 (bat 病毒、自启动、蓝屏攻击)](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247487311&idx=1&sn=95211524641975c5a5093f07df5e6ab2&chksm=cfccbf82f8bb36940f26a26bd8ed5870088823a9a97ccd81e699ed82aca3f579231c9b3e987e&scene=21#wechat_redirect)
    
*   [[系统安全] 十九. 宏病毒之入门基础、防御措施、自发邮件及 APT28 宏样本分析](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247487459&idx=1&sn=87d6296402fdb71f5dbb5a42f9bb6597&chksm=cfccbf2ef8bb363893337b31e8985361624280b90ee6ca65c2da67916fc78ba66f059a24e589&scene=21#wechat_redirect)
    
*   [系统安全] 二十. PE 数字签名之 (上) 什么是数字签名及 Signtool 签名工具详解  
    

2020 年 8 月 18 新开的 “娜璋 AI 安全之家”，主要围绕 Python 大数据分析、网络空间安全、人工智能、Web 渗透及攻防技术进行讲解，同时分享 CCF、SCI、南核北核论文的算法实现。娜璋之家会更加系统，并重构作者的所有文章，从零讲解 Python 和安全，写了近十年文章，真心想把自己所学所感所做分享出来，还请各位多多指教，真诚邀请您的关注！谢谢。2021 年继续加油！

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZePZ27y7oibNu4BGibRAq4HydK4JWeQXtQMKibpFEkxNKClkDoicWRC06FHBp99ePyoKPGkOdPDezhg/640?wx_fmt=png)

(By:Eastmount 2021-02-07 周日夜于 1 点)

参考文献：

*   [1] 武大《软件安全》课程
    
*   [2] 数字签名是什么？- 阮一峰
    
*   [3] What is a Digital Signature? - 原始网站
    
*   [4] Windows 平台下 PE 文件数字签名的一些研究 - DoveFeng
    
*   [5] https://docs.microsoft.com/zh-cn/
    
    windows/win32/debug/pe-format
    
*   [6] 哈希 HASH· 数字签名 - Phant
    
*   [7] 恶意文件分析系统中的数字签名验证 - 绿盟科技
    
*   [8] [翻译]Windows PE 文件中的数字签名格式 - 看雪银雁冰大神
    
*   [9] PE 文件数字签名工具 - ahuo