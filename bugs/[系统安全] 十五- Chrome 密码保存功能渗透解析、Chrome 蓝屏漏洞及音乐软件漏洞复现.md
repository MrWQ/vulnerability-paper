> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/-E4_NSiXrGtnZqcWk8zo0A)

作者前面详细介绍了熊猫烧香病毒的逆向分析过程。这篇文章换个主题，通过三种类型的漏洞利用普及系统安全，具体内容包括：对 Chrome 浏览器保留密码的功能进行渗透解析；复现一个最近流行的漏洞，通过 Chrome 浏览器实现 Win10 蓝屏；最后介绍音乐软件的加密功能及漏洞复现。这些基础性知识不仅和系统安全相关，同样与我们身边的 APP、常用软件及操作系统紧密联系，希望这些知识对您有所帮助，更希望大家提高安全意识，开发厂商进行相关的漏洞修补，安全保障任重道远。  

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmGic9tBPPgICG3JbGYxnMFwZgGDtJicP8OyC1kq4KjyhYRpOXlXHynwPA/640?wx_fmt=png)

> 从 2019 年 7 月开始，我来到了一个陌生的专业——网络空间安全。初入安全领域，是非常痛苦和难受的，要学的东西太多、涉及面太广，但好在自己通过分享 100 篇 “网络安全自学” 系列文章，艰难前行着。感恩这一年相识、相知、相趣的安全大佬和朋友们，如果写得不好或不足之处，还请大家海涵！  
> 接下来我将开启新的安全系列，叫 “系统安全”，也是免费的 100 篇文章，作者将更加深入的去研究恶意样本分析、逆向分析、内网渗透、网络攻防实战等，也将通过在线笔记和实践操作的形式分享与博友们学习，希望能与您一起进步，加油~
> 
> 推荐前文：网络安全自学篇系列 - 100 篇
> 
> https://blog.csdn.net/eastmount/category_9183790.html

话不多说，让我们开始新的征程吧！您的点赞、评论、收藏将是对我最大的支持，感恩安全路上一路前行，如果有写得不好或侵权的地方，可以联系我删除。基础性文章，希望对您有所帮助，作者目的是与安全人共同进步，加油~

文章目录：

*   一. Chrome 浏览器密码保存功能解析
    
*   二. Chrome 致 Win10 蓝屏漏洞复现
    
*   三. 音乐软件漏洞复现
    
*   四. 总结
    

作者的 github 资源：  

*   逆向分析：https://github.com/eastmountyxz/
    
    SystemSecurity-ReverseAnalysis
    
*   网络安全：https://github.com/eastmountyxz/
    
    NetworkSecuritySelf-study
    

> 声明：本人坚决反对利用教学方法进行犯罪的行为，一切犯罪行为必将受到严惩，绿色网络需要我们共同维护，更推荐大家了解它们背后的原理，更好地进行防护。该样本不会分享给大家，分析工具会分享。

一. Chrome 浏览器密码保存功能解析
=====================

1.Chrome 密码保存功能
---------------

大家可能都见过浏览器保存密码的功能，那么，Chrome 浏览器是如何存储这些用户名和密码的呢？它又是否安全呢？我们以 Chrome 浏览器为例进行安全渗透测试普及。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmxlSViaf7jKEdfSTfArF3unG6HVQuLBo8ACluB2H2oOLS9MboV0sqeyQ/640?wx_fmt=png)

首先，打开密码管理器。设置 -> 高级 -> 密码，或者输入：

*   chrome://settings/passwords
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmE1aB3WqQQMXjzQibNIevQfamGl1ezJQW8lTPSJ625BrhOhicRg6ySadg/640?wx_fmt=png)

然后，我们查看某个网站的密码。所幸，Chrome 浏览器对显示的密码进行了一道验证，需要输入正确的电脑账户密码才能查看，如下图所示。

*   为了执行加密（在 Windows 操作系统上），Chrome 使用了 Windows 提供的 API，该 API 只允许用于加密密码的 Windows 用户账户去解密已加密的数据。所以基本上来说，你的主密码就是你的 Windows 账户密码。所以，只要你登录了自己的 Windows 账号，Chrome 就可以解密加密数据。
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmeGwhbqktKkaMNNbyJ7mJ2vJ8WuTDUCQpcVib6iaJk92NaqaibjakbI5IA/640?wx_fmt=png)

最后，输出 Windows 账户正确显示对应网站的密码。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmG9wsqNSglicm05fW59lyUzKZCRtRDd4XbfNMPoFE0hC5M9AxB56CfQA/640?wx_fmt=png)

浏览器安全普及：  
由于 Windows 账户密码是一个常量，并不是只有 Chrome 才能读取 “主密码”，其他外部工具也能获取加密数据，同样也可以解密加密数据。比如使用 NirSoft 的免费工具 ChromePass（NirSoft 官方下载），就可以看得你已保存的密码数据，并且可以轻松导出为文本文件。既然 ChromePass 可以读取加密的密码数据，那么恶意软件也是能读取的。

*   值得注意的是，当 ChromePass.exe 被上传至 VirusTotal（在线沙箱）时，超过半数的反病毒（AV）引擎会标记这一行为是危险级别。不过微软的 Security Essentials 并没有把这一行为标记为危险。
    

假设你的电脑被盗，小偷重设了 Windows 账号密码。如果他们随后尝试在 Chrome 中查看你的密码，或用 ChromePass 来查看，密码数据都是不可用的。原因很简单，因为 “主密码” 并不匹配，所以解密失败。此外，如果有人把那个 SQLite 数据库文件复制走了，并尝试在另外一台电脑上打开，ChromePass 也将显示空密码，原因同上。

*   综合结论：Chrome 浏览器中已保存密码的安全性一定程度上取决于用户本身。
    

2. 密码元素定位
---------

我们在 Web 渗透或 Python 网络爬虫中，都知道分析网页 DOM 树结构可以定位指定元素。那么，作者能不能修改 input 密码的属性，让它显示密码呢？如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmo9hHwpXw2HMibr0ia88w3WpficazNZgJ90xaGSXrHjSa4NjLN9WPKicRJg/640?wx_fmt=png)

比较幸运，Chrome 应该已经解决了该漏洞，显示空白。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmAbpBpN7XB8vCwbcO50q2whokbKCgKeAMZ8Ebu1WAmzdktWrjJNvqVQ/640?wx_fmt=png)

3. 密码提取复现
---------

接下来，作者尝试获取本地 Chrome 浏览器登录的账户信息。

第一步，找到密码存储的位置，文件或者是注册表。  
这个时候需要开启监控工具 Process Monitor（后续文章会详细介绍），查看打开注册表和文件操作信息。然后到 chrome 密码管理界面，随便删除一条记录，然后看看 chrome 本身对哪些文件或者注册表进行了修改。推荐 TK13 大神文章：

*   https://blog.csdn.net/u013761036/article/details/53822036
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjm6t95mMJU9mWLJ6I6EGo20EUnJOQwLNSH7LVWyMF4Mib2fuxQWSAR13w/640?wx_fmt=png)

同样，可以直接寻找文件，通常用户名文件的存储路径为：

*   C:\Users \ 用户名 \ AppData\Local\Google
    
    \Chrome\User Data\Default
    

第二步，找到如下图所示的文件——Login Data。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjm4wbDk3Ad6dzUGrMia8ER1ltLxu7gss0WEDTLsHInXMWEGbFYsvpYic5A/640?wx_fmt=png)

第三步，打开这个文件，还好这个文件是加密的，而不是明文存储。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmNsIic5oAVcTicibYpu1EG75YaQGWfZa10BxIVmlR5eDqFXJRCOVtrJk9A/640?wx_fmt=png)

虽然该文件加密了，但是可以看到它是 SQLite format 3 的格式。接着通过工具读取该数据。这里使用 Navicat Premium 工具。

> Navicat premium 是一款数据库管理工具, 是一个可多重连线资料库的管理工具，它可以让你以单一程式同时连线到 MySQL、SQLite、Oracle 及 PostgreSQL 资料库，让管理不同类型的资料库更加的方便。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmpiaXy9vwavodV00HIt5xfJjuAAd2LvcLvPtOnyMl6ibvRClE4GqlK4icw/640?wx_fmt=png)

第四步，打开 Navicat premium，新建连接。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmic5eStla0plZ3Yn81rvhaQvW7jcAGia083xhhe5y01b9yGJyfw9SfEVQ/640?wx_fmt=png)

第五步，输入连接名如 “test0803”，并导入本地的“Login Data” 数据。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmsSdPDzknr7SpKfwMS9E9RIRKrX5Q3xMkApsXfWfvDBPtosdCDvwmSg/640?wx_fmt=png)

第六步，打开之后在 “main” 数据库中包含了三张表，其中 logins 为登录表。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmr4ea6pfXOnMCCzldSGKdia2bTiaDQn124yokO6K4wSOAIxVBlq4x0Cqg/640?wx_fmt=png)

新版本表增加如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmUCuOwHxeZhibckt6iaOOoCOj0l3MOPxmQV7QndNDoS9XVHJYBczHwXDQ/640?wx_fmt=png)

第七步，打开如下所示，比如 163 邮箱的用户名为我的电话，密码是加密的。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjm4xvDalqp4vZDcCohA1w6XNSpOvcTN6Nt6Rl274VDMTZFB7hSeY6w3g/640?wx_fmt=png)

第八步，解密。  
想要解密一个加密算法是很难的。这学习 TK13 大神的文章，了解到 Chrome 开源的加密函数 CryptProtectData 和 CryptUnprotectData。这对加解密函数非常特别，调用的时候会去验证本地登录身份，这也就是为什么别人的那个密码文档不能直接拷贝到我们自己 chrome 相关文件夹下去看的原因了。

接下来是代码实现，找到开源的 Sqllite3 库，把数据库解析出来，然后得到密码的加密数据，用 CryptUnprotectData 解密。注意，如果 chrome 开启的时候直接对这个数据库文件操作会失败，建议每次操作先把文件拷贝出来再处理。

第九步，使用 AnalysisChrome Login.exe 工具进行解密。将 Login Data 放置到同一个文件夹下运行即可。下载地址如下：

*   http://download.csdn.net/detail/u013761036/9719029
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmhiaicIW9WNmE9XENVg7GOk3OicvFiaDWZGAqS8khsucTBwgicLzfLBV3svw/640?wx_fmt=png)

渗透结论：Chrome 保存的密码存在泄漏风险，尤其是操作系统用户名被攻破后。是不是很可怕，所以个人电脑大家一定要保护好开机密码，别轻易让坏人使用。后续尝试破壳看看这个 EXE 程序源代码是如何解析的。

4.Chrome 浏览器密码存储机制
------------------

下面分享 N1ckw0rm 大神讲解的 Chrome 浏览器密码存储机制。谷歌浏览器加密后的密钥存储于 %APPDATA%…\Local\Google\ Chrome\User Data\Default\Login Data 下的一个 SQLite 数据库中。那么他是如何加密的呢？通过开源的 Chromium，我们来一探究竟：

首先，我们作为用户登录一个网站时，会在表单提交 Username 以及 Password 相应的值，Chrome 会首先判断此次登录是否是一次成功的登录，部分判断代码如下：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmr4V8ic0ZSM5jZOibZSDRF7CLctWypDJ8GNAXiax5icCvGZNjeP1pADM7dw/640?wx_fmt=png)

当我们登录成功时，并且使用的是一套新的证书（也就是 xx 次登录该网站），Chrome 就会询问我们是否需要记住密码。

那么登录成功后，密码是如何被 Chrome 存储的呢？答案在 EncryptedString 函数，通过调用 EncryptString16 函数，代码如下：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmIdAf3MQsxIJz11XVOygUxibOfAvjRvv0Hic7BsRHnuYpsicVFWic2Jk9ibg/640?wx_fmt=png)

代码利用了 Widows API 函数 CryptProtectData（前面提到过）来加密。当我们拥有证书时，密码就会被回复给我们使用。在我们得到服务器权限后，证书的问题已经不用考虑了，所以接下来就可以获得这些密码。

下面通过 Python 代码实现从环境变量中读取 Login Data 文件的数据，再获取用户名和密码，并将接收的结果通过 win32crypt. CryptUnprotectData 解密密码。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmfduBfGsXibq8icAybkNf6v9Oeia1ib5XxIXYFicnzG1AGkaCmdpmM6RYASw/640?wx_fmt=png)

用 CryptUnprotectData 函数解密，与之对应的是前面提到的 CryptProtectData，理论上来说 CryptProtectData 加密的文本内容，都可以通过 CryptUnprotectData 函数来解密。对其他服务的解密方式，大家可以自行尝试。

完整的脚本代码如下所示：

```
#coding:utf8  import os, sys  import sqlite3  import win32crypt    google_path = r'Google\Chrome\User Data\Default\Login Data' db_file_path = os.path.join(os.environ['LOCALAPPDATA'],google_path)  conn = sqlite3.connect(db_file_path)  cursor = conn.cursor()  cursor.execute('select username_value, password_value, signon_realm from logins')   #接收全部返回结果  for data in cursor.fetchall():      passwd = win32crypt.CryptUnprotectData(data[1],None,None,None,0)            if passwd:          print '-------------------------'         print u'[+]用户名: ' + data[0]           print u'[+]密码: ' + passwd[1]           print u'[+]网站URL: ' + data[2]
```

5. 安全建议
-------

最后作者给出浏览器安全保护的建议：

*   电脑不用轻易借给他人使用，除非身边非常信任的人。
    
*   非私人电脑一定不能让浏览器保存密码。
    
*   非重要网站设定一些易于记住的密码，浏览器里登录时重要账户选择不要保存密码，每次登录手动输入。
    
*   离开电脑务必记得随时锁屏或者关机，登录系统一定要设定密码。
    
*   使用一个极高强度的 Windows 账号密码。必须记住，有不少工具可以解密 Windows 账号密码。如果有人获取了你的 Windows 账号密码，那他也就可以知道你在 Chrome 已保存的密码。
    
*   远离各种各样的恶意软件及钓鱼攻击。如果工具可以轻易获取你已保存的密码，那恶意软件和那些伪安全软件同样可以做到。如果非得下载软件，请到软件官方网站去下载。
    
*   把密码保存至密码管理软件中（如 KeePass），或使用可以整合到 Chrome 中的第三方工具（如 LastPass），使用主密码来管理你的那些密码。
    
*   用工具（如 TrueCrypt）完全加密整个硬盘，并且非私人电脑一定不能让浏览器保存密码。
    

二. Chrome 致 Win10 蓝屏漏洞复现
========================

接下来补充一个 2021 年初大家会遇到的 Chrome 浏览器导致 Win10 蓝屏的漏洞。

> 注意：该漏洞请勿轻易测试，需要在个人虚拟机上测试，测试前先保存好资料。本人坚决反对利用教学方法进行犯罪的行为，一切犯罪行为必将受到严惩，绿色网络需要我们共同维护，更推荐大家了解它们背后的原理，更好地进行防护。

第一步，在 Win10 谷歌浏览器（建议使用虚拟机测试）中输入命令。

```
\\.\globalroot\device\condrv\kernelconnect
```

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmVQhich26hAXt015dWL6nMUpF9ufqMYk8Mzib1Fb4JWkMB65yKeIdaNeQ/640?wx_fmt=png)

第二步，我们的计算机就会自动蓝屏死机重启。  
该漏洞请勿轻易测试，个人虚拟机测试前先保存好资料。漏洞可用于拒绝服务攻击，并且微软还未修复该漏洞，微软 edge 浏览器也具有相同的效果。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjm2DJJicfashGtBbEHd26icCoZJxzBXKaAfDR0oUjmPXnSIj1ribTVklDPA/640?wx_fmt=png)

第三步，分析漏洞原因，参考网站 bleeping computer。

*   https://www.bleepingcomputer.com/news/security/windows-10-bug-crashes-your-pc-when-you-access-this-location/
    

该 Windows 10 中的错误是通过在浏览器的地址栏中打开特定路径或使用其他 Windows 命令，即可使操作系统崩溃并显示蓝屏死机。据 BleepingComputer 了解，这是 Windows 安全研究人员在 Twitter 上披露的两个错误，攻击者可以在各种攻击中滥用这些错误。

*   第一个错误允许无特权的用户或程序输入单个命令，该命令会导致 NTFS 卷被标记为已损坏。该测试表明该命令导致硬盘驱动器损坏，从而导致 Windows 无法启动，本文不复现该漏洞。
    
*   第二个漏洞是 Windows 10 通过尝试打开一条异常路径导致 BSOD（Blue Screen of Death，蓝屏死机）崩溃，致使电脑蓝屏重启。
    

自去年 10 月以来，Windows 安全研究员 Jonas Lykkegaard 已经多次在推特上发布了一个路径，当输入到 Chrome 浏览器地址栏时，该路径会立即导致 Windows 10 崩溃并显示 BSOD（蓝屏死机）。

当开发人员想要直接与 Windows 设备进行交互时，他们可以将 Win32 设备命名空间路径作为参数传递给 Windows 编程函数。例如，允许应用程序直接与物理磁盘进行交互，而无需通过文件系统。Lykkegaard 发现以 “控制台多路复用器驱动程序” 的 Win32 设备命名空间路径，他认为该路径用于 “内核 / 用户模式 ipc”。当以各种方式打开该路径时，即使是低权限用户，也会导致 Windows 10 崩溃。

```
\\.\globalroot\device\condrv\kernelconnect
```

当连接到该设备时，开发人员应传递 “attach” 扩展属性以与该设备正确通信。如果你试图在没有传递属性的情况下由于错误检查不当而连接到该路径，它将导致一个异常，最终导致 Win10 出现 BSOD 崩溃。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmIEF5WzWXb0H2JOZA6nicZp3kpibW0nKg3VdB7fXkoF7c6QibgCO4xTr0A/640?wx_fmt=png)

更糟糕的是，特权低的 Windows 用户可以尝试使用此路径连接到设备，从而使计算机上执行的任何程序都很容易让 Windows 10 崩溃。在测试中，已经确认此错误在 Windows 10 1709 版及以后的版本中存在。

```
winver
```

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmcB2H9MBWyuOvZmBcjGVRdGhXlekLDPeGMTASNJ2a4gbyb9H3yKpUJg/640?wx_fmt=png)

查看 windows 版本信息如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmI5qlnykhBIT3ibwyd0P7NCuono3aZpIRcXkwcUDUdOZ2dHC1fYfdncA/640?wx_fmt=png)

BleepingComputer 公司上周与 Microsoft 联系，以了解他们是否已经知道该错误以及是否会修复该错误。微软表示：“调查了已报告的安全问题，并承诺会尽快为受影响的设备提供更新。”

虽然目前尚不确定此漏洞是否可用于远程执行代码或提升特权，但可以将其以当前形式用作对计算机的拒绝服务攻击。BleepingComputer 通过共享一个 Windows URL 文件（.url），其设置指向路径：

*   \\.\globalroot\device\condrv\kernelconnect
    

当下载文件后，Windows 10 会尝试从有问题的路径中呈现 URL 文件的图标，并自动使 Windows 10 崩溃。此后，BleepingComputer 发现了许多其他利用此 bug 的方法，包括在 Windows 登录时自动导致 BSOD 的方法。

*   **浏览器能致使蓝屏死机，最新微信客户端打开文件导致 BSOD 的变体也出现。确实，如果浏览器能导致计算机直接死机，各种变体是非常容易实现的，提醒大家升级该漏洞！谨防钓鱼及陌生文件。**
    

在现实生活中，该漏洞可能会被攻击者滥用，他们可以访问网络并希望在攻击过程中掩盖自己的踪迹。如果他们具有管理员权限，则可以远程执行访问网络上所有 Windows 10 设备上的此路径的命令，以使它们崩溃。在网络上造成的破坏可能会延迟调查或阻止管理控件检测到特定计算机上的攻击。比如 2017 年，远东国际银行（FEIB）银行就遭遇了类似的攻击手法。在该攻击中，攻击者在网络上部署了爱马仕勒索软件（the Hermes ransomware），以延迟对攻击的调查。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjm34HqeQTibaiaJxeR31SlKibbPGfic53vf0jfatnYDAu3cCjaV61NXTbxOg/640?wx_fmt=png)

最后，作为安全白帽子，我们应该发现漏洞即时通知相关厂商进行漏洞修补。同时，既然操作系统、浏览器存在一些漏洞，那么常用的软件会存在漏洞吗？下面继续补充。

三. 音乐软件漏洞复现
===========

该部分内容将复现 “鬼手 56” 大神的文章，他的网络安全、Crackme、病毒分析、软件逆向等系列文章真心推荐大家学习，包括他开源的项目。

第一步，打开 PC 端某音乐客户端，比如想下载周杰伦的 “骑士精神”，通常会被拒绝。

第二步，此时点开设置，选中 “下载设置”，找到缓存文件目录。

**C:\Users \ 用户名 \ AppData\Local\Netease\****CloudMusic\Cache\Cache**

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmbuYJg9K4vrI0PfqqibxMIfJhHx8icrXT7MuXNf1l1U7XnxXTo8KqFmibg/640?wx_fmt=png)

第三步，双击播放该歌曲，然后按照寻找最新的文件或只保留一首歌，其中后缀名为 “.uc” 的最大文件就是加密过后的文件。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmPS6OUUXan1Uzz25ScMsibWuKRBEP0nQUqxo16umaAxQNNTHExtunT7w/640?wx_fmt=png)

第四步，接着再将文件拖动到 010 Editor 软件，如下图所示：它是一个加密文件，最多的数据是 A3，猜测其是加密后的无意义 0（逆向熟练后的感觉），通常音频的加密方式不会太复杂，而最简单的异或加密（可逆）。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmVJ4JUmjDkk9TATr6bdrx9rfzp8lfmK4j27yLHHuFsTfqXgZIlRjJAA/640?wx_fmt=png)

第五步，接着点开菜单，Tools（工具），将其转换为 “十六进制”，进行“二进制异或” 操作，修改数据为无符号十六进制，并对 A3 进行异或即可。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmPibxkrD9xIvrqqLmh8fZRTqQXLD5afqypgqKKq0ITQWnghsjC0ewiaiaA/640?wx_fmt=png)

注意选择无符号（Unsigned Byte）和异或 A3。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmofxmCq2PTCQ8ib77KdWeU0UMcLnpQfjcrZkpdXpyeY59iaO0VRRUmvFA/640?wx_fmt=png)

异或加密解密：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmicDE0qzic1EUVdEicRSPVCaiaTYkbFey7kLmhRRjwQH68qMQicFmAA7BkdQ/640?wx_fmt=png)

A3 ⊕ A3 = 00

```
A 01100001  3  00000011A 01100001  3  000000110 00000000  0  00000000
```

文件解密如下所示，其中 A3 变换为 00，解密完之后的字符变得有意义。前三个字节是 ID3，这个是 MP3 文件格式的头部。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjm01cBXU7icAMBmvT0SLicqPw6ib5fTzjqyQsyCcKE2OBu1QchBH4MMB7sw/640?wx_fmt=png)

最后，将文件重命名为 “.mp3”，此时可以听歌了，“骑士精神” 走起。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRN0rsmcT6ELT5cupaCGJbjmmbIMArCOljcsel8LYF2sR2zZ8fCjq6CvoiaUO5iblLJqic82tias6qnNUQ/640?wx_fmt=png)

注意：这是一个简单的加密过程，推荐读者们下载正版歌曲，共同维护版权和绿色网络环境。同时，异或加密音乐已经很多年了，希望这些开发公司优化下加密算法，解决这些常见漏洞。

四. 总结
=====

写到这里，这篇文章介绍结束，分别叙述了三个漏洞：

*   浏览器漏洞
    
    CryptProtectData 和 CryptUnprotectData 加解密
    
*   Windows10 蓝屏漏洞
    
    正常程序会传递 attach 扩展属性与该设备正确通信。如果你在没有传递属性的情况下，错误检查不当而连接到该路径，它将导致一个异常，最终造成 Win10 出现 BSOD 崩溃。
    
*   音乐软件漏洞
    
    异或 A3 解密 Cache 文件
    

如果你是一名新人，一定要踏踏实实亲自动手去完成这些基础的逆向分析，相信会让你逐步提升，过程确实很痛苦，但做什么事又不辛苦呢？加油！希望你能成长为一名厉害的系统安全工程师或病毒分析师，到时候记得回到这篇文章的起点，告诉你的好友。

家人永远是最珍贵的礼物！珍爱前行。

学安全一年，认识了很多安全大佬和朋友，希望大家一起进步。这篇文章中如果存在一些不足，还请海涵。作者作为网络安全和系统安全初学者的慢慢成长路吧！希望未来能更透彻撰写相关文章。同时非常感谢参考文献中的安全大佬们的文章分享，深知自己很菜，得努力前行。编程没有捷径，逆向也没有捷径，它们都是搬砖活，少琢磨技巧，干就对了。什么时候你把攻击对手按在地上摩擦，你就赢了，也会慢慢形成了自己的安全经验和技巧。加油吧，少年希望这个路线对你有所帮助，共勉。

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
    
*   [系统安全] 十五. Chrome 密码保存功能渗透解析、Chrome 蓝屏漏洞及音乐软件漏洞复现  
    

2020 年 8 月 18 新开的 “娜璋 AI 安全之家”，主要围绕 Python 大数据分析、网络空间安全、人工智能、Web 渗透及攻防技术进行讲解，同时分享 CCF、SCI、南核北核论文的算法实现。娜璋之家会更加系统，并重构作者的所有文章，从零讲解 Python 和安全，写了近十年文章，真心想把自己所学所感所做分享出来，还请各位多多指教，真诚邀请您的关注！谢谢。2021 年继续加油！

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZePZ27y7oibNu4BGibRAq4HydK4JWeQXtQMKibpFEkxNKClkDoicWRC06FHBp99ePyoKPGkOdPDezhg/640?wx_fmt=png)

(By:Eastmount 2021-01-21 周四夜于武汉)