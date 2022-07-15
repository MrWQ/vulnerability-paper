> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/7SZra5ZCE_0E3IPQjGkSvQ)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39tpy3C5BlSicTuYshtqpzXcZwSicJIjSeoHm4Miblzibb7WFzIW3wuUax3Z9owJNWC6AQ6ONDia6qHfqA/640?wx_fmt=jpeg)

关于 MeterPwrShell
----------------

MeterPwrShell 是一款功能强大的自动化工具，**可以帮助广大研究人员以自动化的形式生成完美的 PowerShell Payload。**MeterPwrShell 基于 Metasploit 框架和 amsi.fail 实现其功能，可以生成 PowerShell One-Liner，并能够创建 Meterpreter Shell，而且还可以绕过 AMSI、防火墙、UAC 和任意反病毒产品。

功能介绍
----

使用 PrependMigrate 实现自动化免杀；

自动从普通用户提权为 SYSTEM 权限；

禁用所有的防火墙配置；

绕过 Windows Defender 实时保护功能；

Payload 免杀；

绕过 AMSI；

简单的代码，One-Liner；

绕过防火墙；

方便的命令行接口；

……

注意事项
----

切勿将此程序生成的 Payload 上传到任何在线扫描服务；

切勿将此程序用于恶意目的；

请不要尝试 Fork 这个代码库；

所有的 Payload 功能都已在 Windows 10 v20H2 平台上进行过测试。

MeterPwrShell 和 Metasploit 框架中的 web_delivery 模块对比
-------------------------------------------------

更简短的脚本代码（One-Liner）；

不需要为 Stager 安装服务器；

支持内置 Ngrok；

自动内置 Privesc；

可轻松绕过 Windows Defender；

工具要求
----

Kali Linux、Ubuntu 或 Debian；

Metasploit 框架；

接入网络（目标主机和攻击者主机都需要）；

工具下载
----

广大研究人员可以使用下列命令将该项目源码克隆至本地：

```
git clone https://github.com/GetRektBoy724/MeterPwrShell.git
```

工具使用
----

```
# ./MeterPwrShell2Kalix64 -c help

 Available arguments : help, version, showbanner, showlastdebuglog help : Show this page version : Show MeterPwrShell's version showbanner : Show MeterPwrShell's Banner                   

 showlastdebuglog : Well,Its kinda self-explanatory tho
```

攻击向量
----

BadUSB

恶意快捷方式（lnk2pwn）

恶意宏文档 Payload

MS DDE 漏洞利用

在目标设备上执行命令以利用任意漏洞

```
项目地址：https://github.com/GetRektBoy724/MeterPwrShell
```

参考资料

```
https://github.com/rapid7/metasploit-framework
https://amsi.fail/
https://gist.github.com/GetRektBoy724/9383c9580cb1c9935fc04cc7eb7ef004
https://blog.sevagas.com/Bypass-Antivirus-Dynamic-Analysis
https://github.com/it-gorillaz/lnk2pwn/
```

作者：Alpha_h4ck，转载于 freebuf。

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC7IHABFmuMlWQkSSzOMicicfBLfsdIjkOnDvssu6Znx4TTPsH8yZZNZ17hSbD95ww43fs5OFEppRTWg/640?wx_fmt=gif)

●[干货 | 渗透学习资料大集合（书籍、工具、技术文档、视频教程）](http://mp.weixin.qq.com/s?__biz=MzIwMzIyMjYzNA==&mid=2247490892&idx=2&sn=5820f8871f23ffc525a27e1c6ae1ae4c&chksm=96d3e649a1a46f5f88051b88fb05efd4cda4c885a4f47ac63795354cbfe5e3a93de747f3f10a&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3b9EpYTX241vj3pudtgtj7V0XFvzpxP5tBHCOtpXZmmHcpPBq4STTxVe56CdHHUb8hmAD6fzRrpA/640?wx_fmt=jpeg)

**关注公众号: HACK 之道**

公众号

如文章对你有帮助，请支持点下 “赞”“在看”