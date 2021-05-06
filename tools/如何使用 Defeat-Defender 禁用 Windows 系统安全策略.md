> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/eafVc-ZcISCWTmzhS2VUzQ)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icOw5eQ59svibfQnJiccnf9cZOzwwd2SGwB6AE9Lvgibx8lA6MokciaiavhC2oV69pxXovx42icCJ6xnZ8w/640?wx_fmt=jpeg)

Defeat-Defender
---------------

Defeat-Defender 是一款功能强大的 Batch 批处理脚本，该脚本可以帮助广大研究人员在渗透测试的过程中，完全禁用 Windows Defender、防火墙和 Smartscreen 的保护，并允许执行各种 Payload，在某些情况下甚至还可以绕过系统的篡改保护功能。

工具下载
----

广大研究人员可以使用下列命令将该项目源码克隆至本地：

```
git clone https://github.com/swagkarna/Defeat-Defender.git
```

工具使用
----

将该项目克隆至本地之后，打开项目根目录中的 Defeat-Defender.bat，然后编辑下面这行数据，并将直接 URL 替换为托管我们 Payload 的 URL 地址：

```
https://github.com/swagkarna/Defeat-Defender/blob/93823acffa270fa707970c0e0121190dbc3eae89/Defeat-Defender.bat#L72
```

接下来，运行 “run.vbs” 脚本，此时脚本将会要求获取管理员权限。如果授予脚本管理员权限的话，该脚本将会在后台静默运行，不会弹出任何命令行窗口。

获取到管理员权限之后，Defeat-Defender 将会禁用掉下列 Windows 安全防护机制：

> PUAProtection
> 
> 样本自动提交
> 
> Windows 防火墙
> 
> Windows Smart Screen（永久）
> 
> 禁用快速扫描
> 
> 在 Defender 设置中添加 exe 文件后缀至排除项
> 
> 禁用勒索软件保护

Virus Total 扫描结果（2021 年 04 月 08 日）
----------------------------------

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icOw5eQ59svibfQnJiccnf9cZiboIbwHh5Oh1HyB6rKCrz5gFa0EibvZTwpWOGFicL0FFC54B489p1W8dw/640?wx_fmt=jpeg)

绕过 Windows Defender 技术
----------------------

近期，Windows 推出了一种名为 “篡改保护” 的新功能。这个功能可以防止禁用实时保护以及使用 PowerShell 或 CMD 修改 Defender 注册表项的行为。如果需要禁用实时保护，则需要用户手动执行。但我们这里使用了 NSudo 来禁用实时保护功能，这样可以避免触发 Windows Defender 的警报。

运行 Defeat-Defender 脚本
---------------------

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icOw5eQ59svibfQnJiccnf9cZXgGH2wIpic1jGb6P8QHJTibXR0kV4IjNibeXJ9zibGhHxstiaUBDv5Psiajg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icOw5eQ59svibfQnJiccnf9cZ2x2dibxvYrWibwOhUGUGZkCUFZBL7dl7ibR4NVKkgUQEFSvWomnoEyYkQ/640?wx_fmt=jpeg)

运行机制
----

批处理文件执行之后，它将会要求获取管理员权限。在拿到管理员权限之后，它将会开始禁用 Windows Defender 实时保护功能、Windows 防火墙和 SmartScreen，并从远程服务器下载我们的后门程序，然后将后门存储至系统的启动目录之中。该后门在下载完成之后便会立刻运行，并随目标操作系统的启动而启动。

如果你想要禁用 Defender SmartScreen 的话，请直接执行 Smart Screen.bat 文件。

项目地址：点击底部【阅读原文】获取  

![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR38Tm7G07JF6t0KtSAuSbyWtgFA8ywcatrPPlURJ9sDvFMNwRT0vpKpQ14qrYwN2eibp43uDENdXxgg/640?wx_fmt=gif)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf + 小程序：把安全装进口袋 小程序

精彩推荐

  

  

  

  

****![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib2xibAss1xbykgjtgKvut2LUribibnyiaBpicTkS10Asn4m4HgpknoH9icgqE0b0TVSGfGzs0q8sJfWiaFg/640?wx_fmt=jpeg)****

  

  

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39n5GEibfNkw4IJCQ3PU5W4hScYnG2TeOSgTVGYX9BZfoBX4cvliaEolz3gepYFfNvlFMYvibbmn0Rzg/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486050&idx=1&sn=7e7d54cc1319f1dadfd36b4f92974c62&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ickibic6Dgs2dagP4sPMaribnGJf2HJeXWbGiaG2mczmUtPRibJwpSMpyOhBAic5QcAqONZKT7jOAKca57g/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MjM5NjA0NjgyMA==&mid=2651118893&idx=2&sn=552b6e841de517b324d16c0e36f5fe9c&chksm=bd1f4fa68a68c6b0f352209dab807f7094ba01cab6b7f7f802862ab6303c9e21362eac20a2a5&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39yuicicEmXN9NUz0Zs4xGcnRuJrJksAAFv1g4ibucaCJyueUebkDqRSNAdmUanTyNF0YHpV9iacm9RtA/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MjM5NjA0NjgyMA==&mid=2651121953&idx=1&sn=a6b2f2f78f09d293cb6238c6ad39fc4c&chksm=bd1f7baa8a68f2bc4c8907c1e2f89a3ead9c42b8c413e5184a6965040c7ff4bd3fbff4cb8368&scene=21#wechat_redirect)

**************![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR3icF8RMnJbsqatMibR6OicVrUDaz0fyxNtBDpPlLfibJZILzHQcwaKkb4ia57xAShIJfQ54HjOG1oPXBew/640?wx_fmt=gif)**************