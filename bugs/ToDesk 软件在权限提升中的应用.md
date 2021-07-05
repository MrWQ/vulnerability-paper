> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/dnatpGxOb73tmF_DS5PR7Q)<table><tbody><tr><td width="557" valign="top" height="62"><section><strong>声明：</strong>该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。</section><section>请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。</section></td></tr></tbody></table>

**0x01 前言**

ToDesk 是一款类似向日葵的远程控制软件，但比向日葵、TV 和 AD 更为流畅和稳定，它同样也具备着内网穿透、文件传输、云端同步和流量加密等功能，有绿色精简版和全功能版两个版本。

这里我就不再做过多介绍了，详情可通过 ToDesk 官网自行了解：https://www.todesk.com。

**0x02 信息搜集**

```
操作系统：Windows Server 2008 R2 x64
软件版本：ToDesk 3.0.1.0（精简版和全功能版）
精简版默认安装路径：%userprofile%\AppData\Local\ToDesk
全功能版默认安装路径：C:\Program Files (x86)\ToDesk\
ToDesk进程名：ToDesk_Lite.exe、ToDesk_Service.exe、ToDesk.exe
ToDesk服务名：ToDesk_Service
ToDesk端口号：35600
```

**0x03 场景 1：安装版低权限下的利用**

已经拿到目标主机 Webshell，而且还是 Administrator 管理员权限，但由于存在杀软或 WAF 拦截了添加管理员用户、3389 远程桌面连接、也查杀了我们传的木马和抓明文哈希等工具。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rdcYQia5GhVoQpNdPxw6m4MM1vVzuOJHqNKs994QYYnAJ1j0Nick5dlWw/640?wx_fmt=png)

在前期的信息搜集中发现进程列表中有个 ToDesk_Lite.exe 进程，这是 ToDesk 绿色精简版，由于之前有测试过这个，所以知道配置文件路径。

```
%userprofile%\AppData\Local\ToDesk
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rezuib0IuvWQibESpsyOXRJibHTaibN115dgT6b15RrPDib9mAxgzfTAvBrg/640?wx_fmt=png)

我们在上图中可以看到有个 config.ini 配置文件，它存储着 ToDesk 远程控制软件中的各项设置，包括有显示语言、设备代码、临时密码、开机自启等，全功能版中的常见设置说明可见下表。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rLjaeicKfVyupCU7Eltsk31NibN4yZfQLwfXnrzTMs7jPStNTscA7CSRA/640?wx_fmt=png)

但这精简版的 config.ini 配置文件中只有显示语言、临时密码、密码更新时间和开机自启。

目前有两个问题：1. 没有设备代码，2. 密码不能解密，那么要怎么连接呢？

```
[ConfigInfo]
language=936
tempAuthPassEx=6ca3ab52e01cfd45cbb306f3765b5bfddf0f7a15b7877309443af14ab699b21e22680011ee2******
updatePassTime=20210529
autoStart=0
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rzV7ibrlZ72tdweOWtU4Oq919u5liaglEibWxuTjfEB3EpgsK3KfoX7l9A/640?wx_fmt=png)

**① 没有找到设备代码。**

这个我在测试时发现在以下路径中还有一个 config.ini 配置文件，它存储着本地端口、设备代码和私有数据，一般存在于 SysWOW64 目录下，默认只有 Administrators、SYSTEM 具备完全控制权限，所以绿色精简版只有在高权限下才能利用。

```
C:\Windows\System32\config\systemprofile\AppData\Local\ToDesk\config.ini
C:\Windows\SysWOW64\config\systemprofile\AppData\Local\ToDesk\config.ini
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rmWffozfOD96ic9o86tawhOMiasPDXsWSbbrkT1pKKtPFG8C62lw9cYbw/640?wx_fmt=png)

**② 临时密码不能解密。**

这里我们可以将目标主机 tempAuthPassEx 替换到本机 tempAuthPassEx，重新运行 ToDesk 软件后即可得到他的明文密码；

或者直接将我们本机 tempAuthPassEx 替换到目标主机 tempAuthPassEx，然后用本机临时密码去连接即可，这种方式需要结束 ToDesk 进程后重启才会生效，比较被动。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9r7GZshZKtO2aGCGm7cwCRpibiazwQkTeCyzfHy3Q2MOIZPF2FN4yJlGEQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rJSoM13eHiaG6WiadxzWmtD6vDLhkT8GGwSL4sIicRHQNOYbaqvVYZAsUQ/640?wx_fmt=png)

**0x04 场景 2：安装版低权限下的利用**

已经拿到目标主机 Webshell，但只是一个 Users 低权限用户，还需要进行权限提升。在前期信息搜集中通过翻找磁盘文件或查看进程发现安装的有 ToDesk 全功能版。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rhTIVwmrbrbFUrCIZ4iayPHDbwH8HrNIWJAMNXjwuN37ICoAoibUR7Xsg/640?wx_fmt=png)

我们再用 icacls 命令来看下 ToDesk 全功能版的默认安装目录权限如何？这里可以看到 ToDesk 这款软件的缺陷就是在默认安装状态下就已经具备了 Users 的完全控制权限。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rYsMc3a2sia9BfGb5DiauVDRqYH42rjXQXK0w8MslwEdVWmpiaiaXOS5rzg/640?wx_fmt=png)

ToDesk 安装路径下同样有 config.ini 配置文件，可以看到存储的有设备代码、临时密码、安全密码以及登录用户和密码等重要敏感信息，可参考场景 1 的常见设置说明表。

```
[ConfigInfo]
localPort=35600
clientId=636938855
PrivateData=b0ceea6d978c590e2684627f2394731bced2cf45d6fc92a5208d7a5c9f688ebbb2f840e65e546c2a8968063937156a58fd5f4b4dbfde8ff61f
language=936
tempAuthPassEx=beba9584fe8d1ef3082cb4d86a5d0bd0586a3aa4d2ce9af3dca455cacf9e115421cdbfaf8fa8267bac392c4cd7507f2ecc7ab6b9361f
updatePassTime=20210626
saveUserPass=1
autoLogin=1
user=493***344@qq.com
passex=cafe2d34f80a85d94f45755df94c5705b55406e89451f1056712bb8b16ecf49bcf2813474158ce4526d2c75928b6516c0315cb339c83fc485d9b34ad
authPassEx=e760f849eae5ea763d80068c2fda1632f9cabd26828d8bf1112561e62c0ae7e9bcef518eaa989de00716121ed94618c2360ee81bfc87
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rcKAuDxyeZXP9FaXbniaEiaVibtMeFsmsJn8tdf5zybfARsyMTTm7JucRw/640?wx_fmt=png)

我们在上图中可以看到他的 ToDesk 远控软件已经设置了 “临时密码和安全密码都可以使用”，也就是说只需拿 tempAuthPassEx 或 authPassEx 在我们本地 ToDesk 配置文件中替换到 tempAuthPassEx，然后重新运行 ToDesk 软件后即可得到他的明文密码。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9ribCuV6NicKCVibo23kSjicTiaLiaY7QOQvbw6AmdETDKzw5VpmuTGuIlMBsw/640?wx_fmt=png)

也可以使用 ToDesk.exe 命令行参数中的 - getid 获取设备代码，-setpasswd 设置安全密码等，但是这种方式需要重启 ToDesk，可以再给他设置个开机自启什么的。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9ryVGs5RwH5WQsu4ia5ibSNvxTib3Fx27u1CaQZ6egVmBicUnTlO8CfY9MIw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rapqkZA5GH7aRffuITCQQ3wHFBj4js3vu2WeseTuuxp8fzBTWH0Y9ag/640?wx_fmt=png)

我们还可以在 ToDesk 的配置文件给他设置个自动更新，然后替换掉安装目录下的 ToDeskUpd.exe 更新程序来进行被动提权和权限维持。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rwv48TibeiaStOMiatCNemhQvxpjibrYrnWtibsasibFv57ZQ4kR3lVCdBroQ/640?wx_fmt=png)

只要运行 ToDesk 就会以 SYSTEM 权限去执行 ToDeskUpd.exe，这样就能得到目标主机 SYSTEM 权限，越深入好玩的姿势越多，还是自己去研究一下吧。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9raDz8bGJaML04E1mvSiaLN0icMa7QreKzey4ibFicv04kf4eOGpK9aywd8g/640?wx_fmt=png)

**注：**笔者只是为写这篇文章在本地模拟了两个场景，但大家在实战中如果遇到类似场景时当然也可以用免杀、绕过或其他方式进行测试，条条大路通 “罗马” 嘛，思路不要过于局限了，根据个人习惯，怎么方便怎么来，请不要做一个杠精！！！

**0x05 注意事项**

千万不要去尝试拷贝 user、passex、autoLogin 登录他的 ToDesk，因为在新设备登录时会提示为第一次登录，并且官方会给注册邮箱或手机号发送一条验证信息

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9rvIHEyve0rOlo6BID0H0dhfJePF4VT47lukCG2vCicJSa1a65qmTujTg/640?wx_fmt=png)

收到的 ToDesk 新设备登录授权邮件中详细记录了登录新设备的设备代码、名称、时间、IP 地址以及地理位置等信息，必须点击允许以后才可以正常登录，一定注意！！！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcGcbiaZAGqM0ibTib92hd0w9r7CDudIS5S7acTvAFE0kyLlumib85FNg2ce3aXn3JQrrdhVTnHe7F3Kw/640?wx_fmt=png)

**一个小 BUG：**

ToDesk 有个和向日葵一样的通病，就是在连接上另一台主机后可能会使用不了复制粘贴，或者是存在冲突导致粘贴到对方拷贝的内容等问题。

向日葵可以按两次 Ctrl 键后再进行复制粘贴，而 ToDesk 则需要使用右边的 Ctrl 键进行复制粘贴。

关注公众号回复 “9527” 可免费获取一套 HTB 靶场文档和视频，“1120” 安全参考等安全杂志 PDF 电子版，“1208” 个人常用高效爆破字典，“0221”2020 年酒仙桥文章打包，还在等什么？赶紧点击下方名片关注学习吧！

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcAcRDPBsTMEQ0pGhzmYrBp7pvhtHnb0sJiaBzhHIILwpLtxYnPjqKmibA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247487086&idx=1&sn=37fa19dd8ddad930c0d60c84e63f7892&chksm=cfa6aa7df8d1236bb49410e03a1678d69d43014893a597a6690a9a97af6eb06c93e860aa6836&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcIJDWu9lMmvjKulJ1TxiavKVzyum8jfLVjSYI21rq57uueQafg0LSTCA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486961&idx=1&sn=d02db4cfe2bdf3027415c76d17375f50&chksm=cfa6a9e2f8d120f4c9e4d8f1a7cd50a1121253cb28cc3222595e268bd869effcbb09658221ec&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)