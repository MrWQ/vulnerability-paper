> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247492427&idx=1&sn=af3a862d78184e93b6e9377f12bce354&chksm=fc7be796cb0c6e80a057dff2a7d67e3483c33e8da2d3a7acb84d04fdd997f28cb89f1fd617fd&scene=21#wechat_redirect)

[内网渗透（十二） | 利用委派打造隐蔽后门 (权限维持)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247491363&idx=1&sn=e5d6670b0f76299d92110d7b679ad70b&chksm=fc781bfecb0f92e8aacaa6f4f7788ed48577e25f943d92073b1b26e68bfbc8f505b2dd2fa4d8&scene=21#wechat_redirect)  

[![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFhLz1H5qAkgh9wkAnWtKQNJd5gpJXE7XFR5qAuM2JpmdfLVUoDkug3r0BJF0TiaMK5vyiaYCEzwqeag/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490017&idx=1&sn=426336dfeeda818b0772b3c44703e173&chksm=fc781d3ccb0f942a7c07662752bb2f6983eb9c249c0d6b833f058b1d95fc7080d2d2598054ac&scene=21#wechat_redirect)

作者：谢公子

  

CSDN 安全博客专家，擅长渗透测试、Web 安全攻防、红蓝对抗。其自有公众号：谢公子学安全

免责声明：本公众号发布的文章均转载自互联网或经作者投稿授权的原创，文末已注明出处，其内容和图片版权归原网站或作者本人所有，并不代表 安世加 的观点，若有无意侵权或转载不当之处请联系我们处理，谢谢合作！

**欢迎各位添加微信号：qinchang_198231** 

**加入 安世加 交流群 和大佬们一起交流安全技术**

WinRM  

WinRM 是 Windows Remote Managementd（Windows 远程管理）的简称。它基于 Web 服务管理 (WebService-Management) 标准，WinRM2.0 默认端口 5985（HTTP 端口）或 5986（HTTPS 端口）。如果所有的机器都是在域环境下，则可以使用默认的 5985 端口，否则的话需要使用 HTTPS 传输(5986 端口)。使用 WinRM 我们可以在对方有设置防火墙的情况下远程管理这台服务器，因为启动 WinRM 服务后，防火墙默认会放行 5985 端口。WinRM 服务在 Windows Server 2012 以上服务器自动启动。在 WindowsVista 上，服务必须手动启动。WinRM 的好处在于，这种远程连接不容易被察觉到，也不会占用远程连接数！

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxia5AOAdOZGpicpHRpokVKKnePS3Hdj5RXS1SkJcpBXLl145AhxZacIog/640?wx_fmt=png)

**WinRM 官方文档：**

https://docs.microsoft.com/en-us/windows/win32/winrm/portal

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxHjk5oKk5rB66ng1HCNUfsEpVsygyGYBTzkpDwaC3FgibAJQCZL2cNVA/640?wx_fmt=gif)

  

**WinRM 的配置**

```
#查看WinRM状态
winrm enumerate winrm/config/listener

#开启WinRM远程管理
Enable-PSRemoting –force

#设置WinRM自启动
Set-Service WinRM -StartMode Automatic

#对WinRM服务进行快速配置，包括开启WinRM和开启防火墙异常检测,默认的5985端口
winrm quickconfig -q
#对WinRM服务进行快速配置，包括开启WinRM和开启防火墙异常检测，HTTPS传输，5986端口
winrm quickconfig -transport:https

#查看WinRM的配置
winrm get winrm/config

#查看WinRM的监听器
winrm e winrm/config/listener

#为WinRM服务配置认证
winrm set winrm/config/service/auth '@{Basic="true"}'

#修改WinRM默认端口
winrm set winrm/config/client/DefaultPorts '@{HTTPS="8888"}'

#为WinRM服务配置加密方式为允许非加密：
winrm set winrm/config/service '@{AllowUnencrypted="true"}'

#设置只允许指定IP远程连接WinRM
winrm set winrm/config/Client '@{TrustedHosts="192.168.10.*"}'

#执行命令
winrm invoke create wmicimv2/win32_process -SkipCAcheck -skipCNcheck '@{commandline="calc.exe"}'

#执行指定命令程序
winrm invoke create wmicimv2/win32_process -SkipCAcheck -skipCNcheck '@{commandline="c:\users\administrator\desktop\test.exe"}'
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxafaxGW2PyPE06r6xnOoCSgTic1dZV3wicbFsPqlsmrm0LLr9aZlhicKkQ/640?wx_fmt=png)

  

开启 WinRM 的过程，做了如下几件事：

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxwNrZG8BDBdWdtNsfSibnh36mEyymltNcxKDRQRnNXOxpLrOHge4ZLZQ/640?wx_fmt=png)

快速配置 WinRM

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxiaM4wrn4YUpfFNibKNnMl8GH2u3Jhh0p7dlMpHgn5cTGRhuo6H5ZiaHXQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxrGZBSeGaNTl9hjL5YIDG2jxz40lNSiaibpuITIW5O9nMEicGJgC86nnHA/640?wx_fmt=png)

设置只允许指定 IP 远程连接 WinRM

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxcKlHiaibDVcNzJibn09WLgVeDQuGJc9c6QfSib3TcqKbItPsQIXJRcA6SA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxHjk5oKk5rB66ng1HCNUfsEpVsygyGYBTzkpDwaC3FgibAJQCZL2cNVA/640?wx_fmt=gif)

  

**通过 WinRM 执行程序**

执行 calc.exe 程序

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxBKgxicGepRGkgCicM2gwmWR5dQKZwZuwVYVFpHiaibxsmldN82FzTiaIo2w/640?wx_fmt=png)

执行指定命令程序，我们这里执行木马

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxZQQYO9sZiaC9cH29eSU8RNlkSn8uccRBqfl1dDSvtOVWia2X6NzWNJcA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxHjk5oKk5rB66ng1HCNUfsEpVsygyGYBTzkpDwaC3FgibAJQCZL2cNVA/640?wx_fmt=gif)

  

利用 WinRM 远程连接主机

**客户端连接**

客户端连接的话，也需要启动 WinRM，然后再执行以下命令进行连接。

**方法一：使用 winrs 连接**

在 cmd 窗口执行以下命令

```
winrs -r:http://192.168.10.20:5985 -u:administrator -p:root cmd
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxJlG4Ra3QV9IVf2iaLBCmFQe1tSo1kty4KiacPn83HcjtYcNCyF6sa6rQ/640?wx_fmt=png)

**方法二：使用 Enter-PSSession 连接**

```
Enter-PSSession -computer win2008.xie.com -Credential xie\administrator -Port 5985
或
New-PSSession -Name test -ComputerName win7.xie.com -Credential xie\administrator
Enter-PSSession -Name test
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxxpVXl4n9csRuPPJicczicsvRagSnKMOa2M4yMyiaHRVKPFNxwtniatCcwA/640?wx_fmt=png)

  

```
查看WinRM远程会话
Get-PSSession

进入ID为2的WinRM会话中
Enter-PSSession -id 2

退出WinRM会话
Exit-PSSession
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxdcCycolWkwq6j3gicpLKGKs5O2Gl9gnwTdh5vj2KaALkawonakwSQXw/640?wx_fmt=png)

  

如果是工作组环境运行，或客户端未加入域，则需要在客户端执行此命令：

```
Set-Item wsman:\localhost\Client\TrustedHosts -value *
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLx8UkdVnE7To4EbOcQEgmV2B2mpoHGYicWx0zRA2p0oGPw9UqXtgflglQ/640?wx_fmt=png)

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxHjk5oKk5rB66ng1HCNUfsEpVsygyGYBTzkpDwaC3FgibAJQCZL2cNVA/640?wx_fmt=gif)

  

**使用 Python 远程连接 WinRM**

首先，需要服务端 WinRM 配置如下，在 cmd 窗口执行以下命令：

```
#为winrm service 配置auth:
winrm set winrm/config/service/auth @{Basic="true"}
#为winrm service 配置加密方式为允许非加密：
winrm set winrm/config/service @{AllowUnencrypted="true"}
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLx2KtqsWxF7fYglymMLdRHaicRqR0kcfCPzgvWSVdjHvzUlzYWibAa7gAQ/640?wx_fmt=png)

  

以下是 python 脚本

```
import winrm
while True:
  cmd = input("$: ")
  wintest = winrm.Session('http://192.168.10.20:5985/wsman',auth=('administrator','root'))
  ret = wintest.run_cmd(cmd)
  print(ret.std_out.decode("GBK")) 
  print(ret.std_err.decode())
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxWKkWBBNN27KrYqibkrVygECLJphicBeHlu94lGt5cTexTfxKVZvLbAnQ/640?wx_fmt=png)

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxHjk5oKk5rB66ng1HCNUfsEpVsygyGYBTzkpDwaC3FgibAJQCZL2cNVA/640?wx_fmt=gif)

  

**注意事项**

这里需要注意的是，通过 WinRM 远程连接也是受到 LocalAccountTokenFilterPolicy 的值影响的。在 Windows Vista 以后的操作系统中，LocalAccountTokenFilterPolicy 的默认值为 0，这种情况下内置账户 administrator 进行远程连接时会直接得到具有管理员凭证的令牌，而其他账号包括管理员组内账号远程连接时会提示权限不足。而在域环境中，只要是域管理员都可以建立具备管理员权限的远程连接。

如果要允许本地管理员组的其他用户登录 WinRM，需要修改注册表设置。

**修改 LocalAccountTokenFilterPolicy 为 1**

```
reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
```

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFiaN9PiaczdMbQOHacDxuPdLxHjk5oKk5rB66ng1HCNUfsEpVsygyGYBTzkpDwaC3FgibAJQCZL2cNVA/640?wx_fmt=gif)

  

WinRM 其他命令

```
winrm
winrm help auth
winrm help uris How to construct resource URIs.
winrm help aliases Abbreviations for URIs.
winrm help config Configuring WinRM client and service settings.
winrm help certmapping Configuring client certificate access.
winrm help remoting How to access remote machines.
winrm help auth Providing credentials for remote access.
winrm help input Providing input to create, set, and invoke.
winrm help switches Other switches such as formatting, options, etc.
winrm help proxy Providing proxy information.
```

[![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFjWI9QibTmpF13L33cHIh2bSMLAI4tW7sTgTkzh4lRcZ6JR7SrOibCTYUEsg8ZsmyKnUBm7h4J5klZw/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=MjM5NDY1OTA1NQ==&mid=2650791647&idx=1&sn=400183ea5bea0a3156a2b3a016a0f4d7&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFjGibCQezQKY4NzE1WGn6FBCbq3pQVl0oONnYXT354mlVw0edib6X6flYib9JRTic4DTibgib15WZC7sDUA/640?wx_fmt=png)

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