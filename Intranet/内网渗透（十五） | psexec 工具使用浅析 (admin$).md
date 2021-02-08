> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247493004&idx=1&sn=e908ac6ef03c0b5ae0cc5a2cabba7ebb&chksm=fc7be151cb0c684789bbc5f6a54e5906a3fed929eeffdba7667839491826fbb029bba295ef82&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFhLz1H5qAkgh9wkAnWtKQNJd5gpJXE7XFR5qAuM2JpmdfLVUoDkug3r0BJF0TiaMK5vyiaYCEzwqeag/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490017&idx=1&sn=426336dfeeda818b0772b3c44703e173&chksm=fc781d3ccb0f942a7c07662752bb2f6983eb9c249c0d6b833f058b1d95fc7080d2d2598054ac&scene=21#wechat_redirect)

作者：谢公子

  

CSDN 安全博客专家，擅长渗透测试、Web 安全攻防、红蓝对抗。其自有公众号：谢公子学安全

免责声明：本公众号发布的文章均转载自互联网或经作者投稿授权的原创，文末已注明出处，其内容和图片版权归原网站或作者本人所有，并不代表 安世加 的观点，若有无意侵权或转载不当之处请联系我们处理，谢谢合作！

**欢迎各位添加微信号：qinchang_198231** 

**加入 安世加 交流群 和大佬们一起交流安全技术**

Psexec

psexec 是 windows 下非常好的一款远程命令行工具。psexec 的使用不需要对方主机开机 3389 端口，只需要对方开启 admin$ 共享 (该共享默认开启)。但是，假如目标主机开启了防火墙，psexec 也是不能使用的，会提示找不到网络路径。由于 psexec 是 windows 提供的工具，所以杀毒软件会将其添加到白名单中。

psexec 的基本原理是：通过管道在远程目标机器上创建一个 psexec 服务，并在本地磁盘中生成一个名为 "PSEXESVC" 的二进制文件。然后，通过 psexec 服务运行命令，运行结束后删除服务。

在使用 psexec 执行远程命令时，会在目标系统中创建一个 psexec 服务。命令执行后，psexec 服务将会被自动删除。由于创建或删除服务时会产生大量的日志，所以会在攻击溯源时通过日志反推攻击流程。

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZSklicGl9LFVGzSX3aHvyYt27UCSxZBIiaI7u2AgMje2YBuKlO478wiaNw/640?wx_fmt=png)

**psexec 使用前提：**

*   对方主机开启了 admin$ 共享，如果关闭了 admin$ 共享，会提示：找不到网络名
    
*   如果是工作组环境，则必须使用 administrator 用户连接，使用普通用户连接会提示：登录失败: 未授予用户在此计算机上的请求登录类型。
    
*   如果是域环境，连接普通域主机可以用普通域用户，连接域控需要域管理员。
    

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZPYabhyT3kpQAI1oJGibjiaEJJoFo2KjUU1V1ib7obIbDu1BRogjI8XlKg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZfklMxV3dKs01nYK38mmiahhgoyR1vrzeny0aXHdzglqqpN9ac9pAKag/640?wx_fmt=png)

参数：

*   -u：指定用户名
    
*   -p：指定密码
    
*   -accepteula：第一次运行 psexec 会弹出确认框，使用该参数就不会弹出确认框
    
*   -s：以 system 权限运行运程进程，获得一个 system 权限的交互式 shell。如果不使用该参数，会获得一个 administrator 权限的 shell
    

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZWGdLA8yz7kOEMC6oYTI90j7MykgAQ46ruCviazyUzicSqNc75uap9icDg/640?wx_fmt=gif)

**工作组环境**  

如果是在非域环境下即工作组环境，psexec 只能使用 administrator 账号登录，使用其他账号 (包括管理员组中的非 administrator 用户) 登录都会提示访问拒绝访问。

目标机器：192.168.10.131

*   管理员：administrator  密码：root
    
*   管理员：test 密码：root
    
*   非管理员：hack  密码：root
    

```
psexec.exe \\192.168.10.131 -u administrator -p root cmd
```

由图可知，只有 administrator 用户可使用 psexec 登陆。即使 test 用户也在管理员组内，也不能登录。 

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZTgrLpuLdo4Biczl5Es8BrXgWVSK7fsFpfVMrEuGyDAFqmP71IlibV6WQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZWGdLA8yz7kOEMC6oYTI90j7MykgAQ46ruCviazyUzicSqNc75uap9icDg/640?wx_fmt=gif)

**域环境**  

**登录域控**

域控只能使用域管理员组内账号密码登录，不能使用域普通成员账号登录，也不能本地登录。

域控：192.168.10.131

*   域管理员：xie\test 密码：x123456./
    

```
psexec.exe \\192.168.10.131 -u xie\test -p x123456./ cmd
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZ65Bib3r77Gs8ldKmy80CmuMyfUOw2rmEibbN6IP12cstics5yb6mticeuQ/640?wx_fmt=png)

  

**以域用户登录域成员主机**

域成员主机：192.168.10.130

*   域普通用户：xie\hack  密码：x123456./
    

域成员主机可以使用普通域用户登录

```
psexec.exe \\192.168.10.130 -u xie\hack -p x123456./ cmd
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZNMYdSib6kGdycTG7DS0P15PYdITqImhBOLRpZPYiawfiaOZ7OWXicN8ZHg/640?wx_fmt=png)

  

**以本地用户登录域成员主机**

域成员主机：192.168.10.22 (pc-win2008)

*   本地管理员：administrator  密码：root
    

使用本地用户登录域成员主机，也只能使用本地的 administrator 用户登录，前提是该主机没禁用 administrator 用户。

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZy4q1reoicBaDwpVib7qAAdJVBs2C7icJpE2DUCoZNwAxtViaQvicRN4FmGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZWGdLA8yz7kOEMC6oYTI90j7MykgAQ46ruCviazyUzicSqNc75uap9icDg/640?wx_fmt=gif)

MSF 中的 psexec 模块

MSF 中的 psexec，主要讲以下两个：

*   exploit/windows/smb/psexec：该模块生成的 payload 是 exe 程序
    
*   exploit/windows/smb/psexec_psh  ：该模块生成的 payload 主要是由 powershell 实现的
    

显然 powershell 生成的 payload 免杀效果比 exe 的要好，但是 windows xp、server2003 默认不包含 powershell 环境。所以，这两个模块各有各自的优势。

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZsOAcnn3fM8HfXTvicCqMic9x3dOnlI4QSk9r0u1QAG4cibflUediaBfCQA/640?wx_fmt=png)

```
use exploit/windows/smb/psexec
set rhost 192.168.10.131
set smbuser administrator
set smbpass x123456./@
exploit
```

攻击成功后，会返回一个 meterpreter 类型的 session 

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZcI7tvsNaue4ku1L9Lh42icZzLcQueUDJLF3G1qzufrjMicIKZkTrtIRg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZWGdLA8yz7kOEMC6oYTI90j7MykgAQ46ruCviazyUzicSqNc75uap9icDg/640?wx_fmt=gif)

Impacket 中的 psexec.py

关于如何安装 Impacket 框架

```
git clone https://github.com/CoreSecurity/impacket.git
cd impacket/
python setup.py install
cd examples
./psexec.py xxx
```

这里由于我是在自己的 VPS 上安装的 Impacket 框架，而靶机处在内网，所以我用代理实现互通。

```
#用明文密码连接
./psexec.py xie/administrator:密码@192.168.10.131
#用哈希值连接
./psexec.py xie/administrator@192.168.10.131 -hashes AADA8EDA23213C025AE50F5CD5697D9F:6542D35ED5FF6AE5E75B875068C5D3BC
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZnNaJicDtFiaZbsgte2OnibMaszibbQ58pvic0TnibOzkvqoHrnqj6icLatibBQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFialSIIWQfe3P9x0UFKlibHzZwSak7Raj2UAkPj1f8DCF11weGUWtfMfRV5HohCSw2v8zw1OrMEReTA/640?wx_fmt=jpeg)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFjWI9QibTmpF13L33cHIh2bSMLAI4tW7sTgTkzh4lRcZ6JR7SrOibCTYUEsg8ZsmyKnUBm7h4J5klZw/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=MzA3NzM2MjAzMg==&mid=2657228904&idx=1&sn=aa0d7a52864f19cbd6245a46ce162a1f&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFjGibCQezQKY4NzE1WGn6FBCbq3pQVl0oONnYXT354mlVw0edib6X6flYib9JRTic4DTibgib15WZC7sDUA/640?wx_fmt=png)

[内网渗透（十四） | 工具的使用 | Impacket 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247492731&idx=1&sn=570c1d9e12ef39709e289b5cc9e2447f&chksm=fc7be0a6cb0c69b0d94c41408b862214beaa631b04ba32f2307819a8b3ac445726849cb24e7f&scene=21#wechat_redirect)  

[内网渗透（十三） | WinRM 远程管理工具的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247492427&idx=1&sn=af3a862d78184e93b6e9377f12bce354&chksm=fc7be796cb0c6e80a057dff2a7d67e3483c33e8da2d3a7acb84d04fdd997f28cb89f1fd617fd&scene=21#wechat_redirect)  

[内网渗透（十二） | 利用委派打造隐蔽后门 (权限维持)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247491363&idx=1&sn=e5d6670b0f76299d92110d7b679ad70b&chksm=fc781bfecb0f92e8aacaa6f4f7788ed48577e25f943d92073b1b26e68bfbc8f505b2dd2fa4d8&scene=21#wechat_redirect)  

[内网渗透（十一） | 哈希传递攻击 (Pass-the-Hash,PtH)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490908&idx=1&sn=97594fbbef40346d07b5a6e5185ce77e&chksm=fc781981cb0f9097d18f4b32ff39f59b3512cedd35f0810ad5f61b661e631153f8c4e157d875&scene=21#wechat_redirect)  

[技术干货 | 工具：Social engineering tookit 钓鱼网站](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490513&idx=2&sn=10afb29a20f37df05ebb12ea4d540e1f&chksm=fc781f0ccb0f961a85e646dd54e977dbcaeb5569be6701db4c29b9e204d964bab3ded6bf1999&scene=21#wechat_redirect)

[技术干货 | 工具的使用：CobaltStrike 上线 Linux 主机 (CrossC2)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490608&idx=1&sn=f2b2ea93b109447aa8cc2c872aa87c52&chksm=fc7818edcb0f91fbf85fa53f71e9967fc29fc93f6a783eed154707ca2dec24ca7f419fde5705&scene=21#wechat_redirect)

[内网渗透（十） | 票据传递攻击](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490376&idx=2&sn=c070dd4c761b49d3fabd573cc9c96b5a&chksm=fc781f95cb0f9683b0f6c64f5db5823973c1b10e87b1452192bbed6c1159eccf6e8f2fd0290b&scene=21#wechat_redirect)  

[内网渗透（九） | Windows 域的管理](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490197&idx=1&sn=4682065ddcab00b584918bc267e33f53&chksm=fc781e48cb0f975eddc44d77698fbb466d0eac7d745a6e5bbaf131560b3d4f9e22c1a359d241&scene=21#wechat_redirect)  

[内网渗透（八） | 内网转发工具的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490042&idx=1&sn=136d4057044a7d6f6cb5b57d20f7954a&chksm=fc781d27cb0f9431ec590662ab4e6bcd31b303e7caa20a2b116fd9a9b97e9e3be0bc34408490&scene=21#wechat_redirect)  

[内网渗透 | 域内用户枚举和密码喷洒攻击 (Password Spraying)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489985&idx=1&sn=0b7bce093e501b9817f263c24e0ed5b8&chksm=fc781d1ccb0f940aad0c9b2b06b68c7a58b0b4c513fe45f7da6e6438cac76d4778e61122faf8&scene=21#wechat_redirect)  

[内网渗透（七） | 内网转发及隐蔽隧道：网络层隧道技术之 ICMP 隧道 (pingTunnel/IcmpTunnel)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489736&idx=2&sn=0cb551ee520860878c2c33108033c00c&chksm=fc781c15cb0f9503f672aa0bd18cb13fef4c60124ba5978ab947c34272b2d8a28c584a99219d&scene=21#wechat_redirect)  

[内网渗透（六） | 工作组和域的区别](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489205&idx=1&sn=24f9a2e0e6b92a167f3082bb6e09c734&chksm=fc781268cb0f9b7e3c11d19a9fb41567124055eb0e8dd526cbbaf1e9393ff707f9fa9d10c32b&scene=21#wechat_redirect)  

[内网渗透（五） | AS-REP Roasting 攻击](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489128&idx=1&sn=dac676323e81307e18dd7f6c8998bde7&chksm=fc7812b5cb0f9ba3a63c447468b7e1bdf3250ed0a6217b07a22819c816a8da1fdf16c164fce2&scene=21#wechat_redirect)

[内网渗透 | 内网穿透工具 FRP 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489057&idx=3&sn=f81ef113f1f136c2289c8bca24c5deb1&chksm=fc7812fccb0f9beaa65e5e9cf40cf9797d207627ae30cb8c7d42d8c12a2cb0765700860dab84&scene=21#wechat_redirect)  

[内网渗透（四） | 域渗透之 Kerberoast 攻击_Python](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488972&idx=1&sn=87a6d987de72a03a2710f162170cd3a0&chksm=fc781111cb0f98070f74377f8348c529699a5eea8497fd40d254cf37a1f54f96632da6a96d83&scene=21#wechat_redirect)  

[内网渗透（三） | 域渗透之 SPN 服务主体名称](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488936&idx=1&sn=82c127c8ad6d3e36f1a977e5ba122228&chksm=fc781175cb0f986392b4c78112dcd01bf5c71e7d6bdc292f0d8a556cc27e6bd8ebc54278165d&scene=21#wechat_redirect)  

[内网渗透（二） | MSF 和 CobaltStrike 联动](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488905&idx=2&sn=6e15c9c5dd126a607e7a90100b6148d6&chksm=fc781154cb0f98421e25a36ddbb222f3378edcda5d23f329a69a253a9240f1de502a00ee983b&scene=21#wechat_redirect)  

[内网渗透 | 域内认证之 Kerberos 协议详解](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488900&idx=3&sn=dc2689efec7757f7b432e1fb38b599d4&chksm=fc781159cb0f984f1a44668d9e77d373e4b3bfa25e5fcb1512251e699d17d2b0da55348a2210&scene=21#wechat_redirect)  

[内网渗透（一） | 搭建域环境](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488866&idx=2&sn=89f9ca5dec033f01e07d85352eec7387&chksm=fc7811bfcb0f98a9c2e5a73444678020b173364c402f770076580556a053f7a63af51acf3adc&scene=21#wechat_redirect)