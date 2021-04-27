> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247495828&idx=3&sn=64b978670f81deee0a5e07137799be05&chksm=fc7bf449cb0c7d5fdacd74bc9d760134228b94cf04003a2237e92755b1477f29a267f4e52046&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFiaP3dCW5gZgZBqrbEozrPZK5I8Pmtjy6f0iaVLLpvWIdqLTwHIc5UJTzmdib1a1XmwEUhyI3QFXj81Q/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=MzI1NjYyNTcxOQ==&mid=2247484052&idx=1&sn=61a00b6cef90b191d516bce635e528f2&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFgo0ScHDSvg0LnhSvoEWg7X9Oj17vMfPnaGaHkkcet0XG23HRQBEMskLnJ8ywIN4A9CVR9wxAD2Gg/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247495157&idx=1&sn=c1126a96b9da99bad4e8debea7c2aabe&chksm=fc7be928cb0c603e7ba1951a9ce7a0804f84a1b6e7aaa1d78cd434a7186a67abb1727ce60778&scene=21#wechat_redirect)

本公众号发布的文章均转载自互联网或经作者投稿授权的原创，文末已注明出处，其内容和图片版权归原网站或作者本人所有，并不代表安世加的观点，若有无意侵权或转载不当之处请联系我们处理，谢谢合作！

欢迎各位添加微信号：**asj-jacky**

加入**安世加** 交流群 和大佬们一起交流安全技术

![](https://mmbiz.qpic.cn/mmbiz_gif/VBXyERmr0fGhqCT8P1XGibdHSs6ibxOOQDwEvqNMufhKbBVeed02jow032wo243QyticdO6bKbpIWyANasZzWic9pg/640?wx_fmt=gif)

**目录**  

获取用户密码

抓取自动登录的密码

导出密码哈希

上传 mimikatz 程序

加载 kiwi 模块

加载 mimikatz 模块

![](https://mmbiz.qpic.cn/mmbiz_png/4EpCzKXdibPibicnYonkAeU6Ah89zyTox5dQZpJuEXzzYEohmmtozibYIjg6tTOV3MhobktVy0z2dlZXvBu3erZS2A/640?wx_fmt=png)

获取用户密码

![](https://mmbiz.qpic.cn/mmbiz_png/c6gqmhWiafyr9hQWuUCPvGMbftRydTk26KkMhMv3GyHGVzUaArA91tkdF6Ovo93CEVRHQJddq1BX3ZNNnzZETlg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8ZKQ8DibGukJsz3l6GawNw4qGWzqfbTRshnjQe6Er3sAJfXllmMgtmibg/640?wx_fmt=png)  

### 抓取自动登录的密码

**1：**很多用户习惯将计算机设置自动登录，可以使用  `run windows/gather/credentials/windows_autologin`  抓取自动登录的用户名和密码

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8halcJH83BIE7ib0XWmHnaMJgNE2kdUHicELdtxSTzp3WBGYwKL5HSnTw/640?wx_fmt=png)

### 导出密码哈希

**2：**hashdump 模块可以从 SAM 数据库中导出本地用户账号，执行：run hashdump ，该命令的使用需要**系统权限**

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8PocYblstAyGicrYTDHBhj226AbiaY44DPK0X0W9sQgWZL99Zy9icN4a0Q/640?wx_fmt=png)**

用户哈希数据的输出格式为：

```
用户名：SID：LM哈希：NTLM哈希:::
```

所以我们得到了三个用户账号，分别为 Administrator、Guest 和小谢。

其中 Administrator 和 Guest 的 LM 哈希（aad3b435b51404eeaad3b435b51404ee）和 NTLM 哈希（31d6cfe0d16ae931b73c59d7e0c089c0）对应的是一个空密码。所以，只有小谢的哈希有效。

接下来要处理的就是用户小谢 的密码（ a86d277d2bcd8c8184b01ac21b6985f6 ）了。我们可以使用类似 John 这样的工具来破解密码：John 破解 Windows 系统密码，或者使用在线网站解密：https://www.cmd5.com/default.aspx

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8jrKS3ytbk1ka2ZR214PmT2QR9nkrJ3owrH25KSibEMD0QnWobnEDt9A/640?wx_fmt=png)

还可以使用命令：run windows/gather/smart_hashdump  ，该命令的使用需要**系统权限。**该功能更强大，如果当前用户是域管理员用户，则可以导出域内所有用户的 hash

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8o9hIzibYEtA0nxn903Pp73CKRsaqXtBVf0fvJj2G60eOb07aLicNZn4Q/640?wx_fmt=png)

上传 mimikatz 程序

![](https://mmbiz.qpic.cn/mmbiz_png/c6gqmhWiafyr9hQWuUCPvGMbftRydTk26KkMhMv3GyHGVzUaArA91tkdF6Ovo93CEVRHQJddq1BX3ZNNnzZETlg/640?wx_fmt=png)

**3：**我们还可以通过上传 mimikatz 程序，然后执行 mimikatz 程序来获取明文密码。  

执行 mimikatz 必须 **System 权限**。

我们先 getsystem 提权至系统权限，然后执行  execute  -i  -f  mimikatz.exe ，进入 mimikatz 的交互界面。然后执行：

*   privilege::debug
    
*   sekurlsa::logonpasswords
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8QIKC9wn4OXTl7DS3oxFsTEoAIFTo0JZVCYJ7s7QYlaZ5iaRiczg57qGg/640?wx_fmt=png)

加载 kiwi 模块

![](https://mmbiz.qpic.cn/mmbiz_png/c6gqmhWiafyr9hQWuUCPvGMbftRydTk26KkMhMv3GyHGVzUaArA91tkdF6Ovo93CEVRHQJddq1BX3ZNNnzZETlg/640?wx_fmt=png)

**4：**加载 kiwi 模块，该模块的使用需要 **System 权限**。关于该模块的用法：  

[工具的使用 | MSF 中 kiwi 模块的使用](http://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247485520&idx=1&sn=afe7ab1dd663bf8dcc9811c840f33614&chksm=eaad886dddda017b5ca9f42ac926ec8abdb42e958561924144f79aad5969c7310bf059e9ba03&scene=21#wechat_redirect)  

加载 mimikatz 模块

![](https://mmbiz.qpic.cn/mmbiz_png/c6gqmhWiafyr9hQWuUCPvGMbftRydTk26KkMhMv3GyHGVzUaArA91tkdF6Ovo93CEVRHQJddq1BX3ZNNnzZETlg/640?wx_fmt=png)

### **5：**或者运行 MSF 里面自带的 mimikatz 模块 ，该模块的使用需要 **System 权限**。传送门：[工具的使用 | MSF 中 mimikatz 模块的使用](http://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247485867&idx=1&sn=0214e97984d0f85ae77f51e5b077c63e&chksm=eaad8996ddda0080eb00131f89a16fd429f10046fdb7409f6119497af317c13dc7e1d3fe33e7&scene=21#wechat_redirect)。目前该模块已经被 kiwi 模块代替了。  

[![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFjWI9QibTmpF13L33cHIh2bSMLAI4tW7sTgTkzh4lRcZ6JR7SrOibCTYUEsg8ZsmyKnUBm7h4J5klZw/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=MzA3NzM2MjAzMg==&mid=2657228904&idx=1&sn=aa0d7a52864f19cbd6245a46ce162a1f&scene=21#wechat_redirect)

[内网渗透（十七） | 内网转发及隐蔽隧道：使用 SSH 做端口转发以及反向隧道](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247494972&idx=1&sn=0e309e74481b64577b87c3802d75858c&chksm=fc7be9e1cb0c60f71eb23300f692cea9936327254e285851fb7f6ee9fcd57debef711d69766b&scene=21#wechat_redirect)  

[内网渗透（十六） | 域分析工具 BloodHound 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247494062&idx=1&sn=0c486f53daca08ee61abc51926db2b96&chksm=fc7bed73cb0c646557767e2e21d3c0113df80f831263dea4ce45bd6969da44f27ee700518427&scene=21#wechat_redirect)  

[内网渗透 | 红蓝对抗：Windows 利用 WinRM 实现端口复用打造隐蔽后门](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247493916&idx=2&sn=eacc42e5f8f68fc65dae1c8a1201f014&chksm=fc7bedc1cb0c64d7115c0c3bf84410e29102a25627891c9eb85cba2026b7bc3622a9ebb5e2b2&scene=21#wechat_redirect)  

[内网渗透（十五） | psexec 工具使用浅析 (admin$)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247493004&idx=1&sn=e908ac6ef03c0b5ae0cc5a2cabba7ebb&chksm=fc7be151cb0c684789bbc5f6a54e5906a3fed929eeffdba7667839491826fbb029bba295ef82&scene=21#wechat_redirect)  

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