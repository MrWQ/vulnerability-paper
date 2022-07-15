\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/4lZvVZv3w1Ug5YLDDNW3AQ)

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDWthuxj2TXBsNCVHu70z5pcUkEHkWCrichUzI2esFfCrwUOpkB24XedQ/640?wx_fmt=gif)

亲爱的, 关注我吧

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDWthuxj2TXBsNCVHu70z5pcUkEHkWCrichUzI2esFfCrwUOpkB24XedQ/640?wx_fmt=gif)

**11/6**

文章共计 2940 个词

预计阅读 10 分钟

来和我一起阅读吧

```
作者：国光
转自先知社区：https://xz.aliyun.com/t/8459
```

前言
==

前几天看到 B 站 up 主公孙田浩投稿的视频「QQ 被盗后发布赌博广告，我一气之下黑了他们网站」，看完后不禁感叹为啥自己没有那么好的运气...... 实际上这就是一个中规中矩的 XSS 漏洞案例，在安全圈子里面应该也算是基本操作，正好博客以前没有记录过类似的文章，那么本文就来还原一下这个攻击过程。

鉴别网站
====

下面是一个经典的 QQ 空间钓鱼网站：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmBgroO3teU6picEyhr5wkqPDNadia9dp9tAg0sXPZvic437oIkLox0m6VA/640?wx_fmt=png)

域名分析
----

钓鱼网站最直观的就是看域名，可以看到目标网站域名 ：qq.xps.com 尽管域名中出现了 qq 字样，但是一级域名却是 xps.com 这一点就直接暴露了钓鱼网站的本性。

早期还有一种**利用拉丁字母**注册的域名伪造钓鱼网站的案例，这种就比较逼真了，下面国光简单列举一些：

**OPPO 官网 真假域名**

```
http://qq.xps.com/admin/login.php
```

**Pornhub 官网真假域名**  

```
官方项目地址为：https://github.com/firesunCN/BlueLotus\_XSSReceiver
```

**唯品会官网 真假域名**  

```
Github 项目地址为：
https://github.com/trustedsec/social-engineer-toolkit
```

关于这类域名就不再列举了，早期这种方法成功率是非常的高的，有时候甚至都可以欺骗到我们这种专业的信息安全从业者。

功能分析
----

钓鱼网站既然是要钓鱼的话，说那么多半还会有后台管理功能。所以使用常规的目录扫描工具多半可以扫描出一些端倪出来：

```
Select from the menu:

   1) Social-Engineering Attacks         # 社会工程攻击
   2) Penetration Testing (Fast-Track)   # 渗透测试（快速通道）
   3) Third Party Modules                # 第三方模块
   4) Update the Social-Engineer Toolkit # 更新 SET
   5) Update SET configuration           # 更新 SET 配置
   6) Help, Credits, and About           # 帮助

  99) Exit the Social-Engineer Toolkit   # 退出

set> 1
```

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmSQPZJbYnMItxU7pZCrLiaj9emgG3jnnElOmXEUzzPIhyxjaibrVicVGkQ/640?wx_fmt=png)

果然扫描出了这个 QQ 空间钓鱼网站的后台登录口了：

```
Select from the menu:

   1) Spear-Phishing Attack Vectors        # 鱼叉式网络钓鱼攻击
   2) Website Attack Vectors               # 网站攻击
   3) Infectious Media Generator           # 感染性介质生成
   4) Create a Payload and Listener        # 创建 Payload 和 监听器
   5) Mass Mailer Attack                   # 群发邮件
   6) Arduino-Based Attack Vector          # 基于 Arduino 的攻击
   7) Wireless Access Point Attack Vector  # 无线接入点攻击
   8) QRCode Generator Attack Vector       # 二维码生成器攻击
   9) Powershell Attack Vectors            # Powershell 攻击
  10) Third Party Modules                  # 第三方模块

  99) Return back to the main menu.        # 返回主菜单

set> 2
```

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmFSJIY5FJTmC6Y79AeKETTtliaMNc4OvzFH7gmO9Z0ib9eouwDVw3bcaA/640?wx_fmt=png)

至此基本上已经可以确定这个目标网站就是传说中的钓鱼网站了，下面来看一下这个钓鱼网站是如何运作的吧。

钓鱼流程
----

小白用户前台输入自己的 QQ 账号和密码信息，点击登录后域名跳转到真正的 QQ 官网：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1Fgm4kLrLSIgeMzQbF2y0N8DIkjQtFaKBgJw8BctLCoomfbiaLJ2ynicNIqg/640?wx_fmt=png)

然后用户再输入自己的 QQ 账号和密码就可以成功登陆了。

目前很多钓鱼网站都是这种思路，这可以让被钓者产生一种自己第一次是密码不小心输入错误的错觉，从而放松警惕，妙啊！真是妙蛙种子吃着妙脆角，妙进了米奇妙妙屋，妙到家了

然后钓鱼网站的管理员每天会到自己的 QQ 空间钓鱼管理中心里面看看今天又有哪些菜鸡上钩了：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1Fgmuxlq5Ir9AB4neNIHtNpB9j7H1WLU5cXxqIa2ds8DrR6gibo61M0pQpg/640?wx_fmt=png)

可以看到上钩者的 QQ 号为：1314520 密码为：sbhac... 唉，不对劲？貌似自己被羞辱了一番......  

攻击思路
====

本文主要是来梳理一下 XSS 常剑的攻击思路，关于 XSS 以为的思路不在本文的叙述范围内，另外如果有小伙伴要不错新的姿势的话欢迎评论区里面或者邮件留言，国光日后会继续完善本文的。

思路一：XSS 盲打
----------

如果目标网站存在 XSS 的话且没有 httponly 防御 cookie 那么就可以直接盲打 XSS。首先准备一个 XSS 靶场，国光这里比较推荐 Github 上面开源的蓝莲花 XSS 平台。

```
1) Java Applet Attack Method           # Java Applet 攻击
   2) Metasploit Browser Exploit Method   # Metasploit Browser 浏览器攻击
   3) Credential Harvester Attack Method  # 凭证窃取攻击
   4) Tabnabbing Attack Method            # 标签页劫持       
   5) Web Jacking Attack Method           # 网页劫持攻击
   6) Multi-Attack Web Method             # 综合网页攻击
   7) HTA Attack Method                   # HTA 攻击

  99) Return to Main Menu                 # 返回主菜单

set:webattack> 3
```

可惜已经清空数据了，还好国光我 fork 了一份：

国光 fork 的项目地址为：https://github.com/sqlsec/BlueLotus\_XSSReceiver

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmJNN1jszBr2PAiaTx7VpX59QgvadFMF70CreOHJUm2N0lVXA0j2Gxb6w/640?wx_fmt=png)

然后使用 XSS 平台里面的模块来生成一个 XSS payload：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmlOPHb8nx5WXxXa5v9XjwrYuzRJHCecmVFL7hstE3P3lqNLnfRzyHCQ/640?wx_fmt=png)

可以去掉多余的双引号：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmJ3nXk1uoVUMqGPTuicImhjsqZEhRVicQp744xZicg6oEpGJy8BiclfCSEw/640?wx_fmt=png)

然后回到钓鱼网站前台，在用户名或者密码出插入 payload（理论上来说 密码处成功率要高一点），如果有表单长度限制的话，可以手工审查元素修改 input 的长度限制：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1Fgmkia4ISJEe2ppPDQlJ2Z7DJAt9baz5zvxxobNRharVGWWOsgK3Bq04Hw/640?wx_fmt=png)

这样黑客攻击的步骤基本上就走完了，下面回到钓鱼网站管理员的视角。  

钓鱼网站的搭建者到自己的 QQ 空间钓鱼管理中心里面看看今天又有哪些菜鸡上钩了：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmtJ3zdxUq9qgbrKYMdfBpKNrcCAqxUesLIZ6zgQvq0GY3o9Az9eyZmg/640?wx_fmt=png)

发现真的有菜鸡上钩，密码居然是 1111111111 嘴角忍不住上仰。

此时他不知道的是，用户账号旁边实际上有一串 JS 代码被解析了，而此时黑客在 XSS 平台里面可以直接看到管理员已经上钩了：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmlgoiaibiawdPD7NchdEmWpO55Ja39QBSWsKonNdr5ohMA1zbsgLrMzSDA/640?wx_fmt=png)

可以直接看到管理员的后台地址和 cookie 信息，拿到后台地址和 Cookie 信息就可以直接抓包替换 Cookie 登录到钓鱼网站的后台，这些基本操作国光我就不在啰嗦了，下面来说一下另一种思路。

思路二：SET 钓鱼
----------

假设目标网站存在 httppnly 的话，我们拿到的 cookie 信息也是不完整的，所以传统的思路是行不通的，这种情况下该怎么办呢？仔细想想，既然不能正面肛 httponly 的话，那么为什么不考虑绕过他呢？

下面国光主要描述一下如何使用 Kali Linux 里面的 set 社工工程学工具包来进行钓鱼。

SET 在 Kali Linux 里面的全称是 social engineering toolkit：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1Fgm2vYib9d9icIIrMLlTMZ665hxS1vVkkZUbWwm1lNLQPALYWneUOC8kBhw/640?wx_fmt=png)

```
1) Web Templates       # 网站模板
   2) Site Cloner         # 站点克隆
   3) Custom Import       # 自定义导入

  99) Return to Webattack Menu # 返回主菜单

set:webattack> 2
```

点击即可直接启动，首先会看到如下的菜单：

```
项目地址：
https://github.com/Wileysec/adobe-flash-phishing-page
```

选择 1 后进入到下面的菜单：

```
项目地址：
https://github.com/r00tSe7en/Flash-Pop
```

选择 2 后进入到下面的菜单：

```
为 Cobalt Strike exe 木马添加图标
https://www.sqlsec.com/2020/10/csexe.html
```

选择 3 进入到下面的菜单：

```
https://www.hetianlab.com/expc.do?ec=ECID172.19.104.182014103117160200001
本实验主要介绍了401认证钓鱼，通过本实验你能了解到401认证，学会利用401认证进行钓鱼。
```

选择 2 然后具体看下下面的操作：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1Fgm1ZulOldvVTHe0LKibedAE3XUJSpB7HibVgr9KDvoHTjkDw4CF4OLIAAw/640?wx_fmt=png)

这个时候一个假的钓鱼网站就制作完成了，访问 Kali Linux 的 80 端 10.20.25.39 效果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmHVd7WghkmCxKCTJBl2WvhKsk0JSmoic1bY9zSvPIs8pqVxOB6tspTbA/640?wx_fmt=png)

这个登录入口和 qq.xps.com/admin/login.php 的登录口一模一样：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmPibbsJdvmhoZYHMBVdNr39rOGiaEMTqlh1ibH0kJlqwODDKbeJoQOHvHg/640?wx_fmt=png)

现在的任务就是想办法让管理员在假的网站里面输入网站的后台用户名和密码信息，那么该怎么诱导管理员点击呢？对，聪明的网友肯定想到了，还是利用 XSS，准备下方的 payload，这个 XSS 的作用就是普通的链接跳转：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmJ8x0aPSCU9AAib9MV5r4aSvUibUsmpEjfmllO0q7P3RMJ19KWDVKA0AQ/640?wx_fmt=png)

然后将这个 payload 插入到钓鱼网站的后台中：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmmKt9s9pr7fiay8Xjics9jMK1ZpBCHCE9KckicG39l5hAr4DkAoJs6btUg/640?wx_fmt=png)

此时管理员到自己的 QQ 空间钓鱼管理中心里面看看今天又有哪些菜鸡上钩了，结果没想到网站浏览器却跳转到了：10.20.25.39 页面，这个就是我们制作的假的 QQ 空间钓鱼管理中心的登录界面。

如果管理员大意的话，这个时候会以为登录会话超期了，需要重新登录，就在我们假的网站后台里面输入了真正的密码：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmLcmf3RtKGzEIZodwQgIIib8VeHCs0ibcL5G62eG0nTEhWzSfUJHJtCLg/640?wx_fmt=png)

我们这个假的网站也非常妙，登录后自动转发到正确的网站登录成功，真是学以致用呀~~

管理员放松警惕的同时，我们的 Kali Linux 里也窃取到管理员的明文账号和密码信息了：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmY7MDGr76ZQGF2upcmGwUWLOkc4vXicE7Ievf4RV22vRMricpFe3xXACg/640?wx_fmt=png)

拿到这个后台就可以成功登陆了，Bingo ~

当然如果管理员是一个有很高安全意识的人，可能是不会上当的，本案例仅供意淫参考使用，实际运用还是得看运气。

思路三：Flash 钓鱼
------------

这也是 B 站 视频里面提到过的方法，首先我们需要准备一个钓鱼页面，这里在 Github 上搜索到了 2 个 相关的项目，下面分别展示一下：

```
项目地址：
https://github.com/Wileysec/adobe-flash-phishing-page
```

模仿的 Flash Player 中文官网的页面

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmRmpib8p0snfhSfEjD0ZK1honuceSibNfj33bXOTSW8kJyYvYjSs0loag/640?wx_fmt=png)

```
项目地址：
https://github.com/r00tSe7en/Flash-Pop
```

这种的就要稍微激进一点，强迫症都会忍不住去点击下载的：  

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmuumKXoLYdhw3KAzBH9tPvKvb5I0YueLd8BfdMuQLbClSOrZl79QT1w/640?wx_fmt=png)

国光这里选择了第 2 种激进的方法，点击立即升级的这个按钮点击会下载好国光我准备好的 CS 木马。如果管理员以为自己的 Flash 版本过低的话，可能会下载并运行这个木马：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmNpnhMfibUsPasmxn2NxZXc9l4cdELTu6LEAumZue5IbhzCJTdLKWC5A/640?wx_fmt=png)

这里偷懒了没有给 Flash.exe 添加图标伪造一下，关于图标伪造大家可以参考之前的文章：

```
为 Cobalt Strike exe 木马添加图标
https://www.sqlsec.com/2020/10/csexe.html
```

如果顺利的话就会成功上线 CS：  

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfCC9efnKbyBoY3w3mR1FgmeOpqTIOH2Ccb7DSmtWYJ6YIQmktYCBAP9sS3NULDerLPQ9YtgfKcOA/640?wx_fmt=png)

总结
==

免责声明：本文出现的思路案例仅供网络安全学习和研究技术使用，禁止使用本文的攻击技术工具用于非法用途，否则后果自负，另外文中所使用的 QQ 空间钓鱼网站是人为修改的漏洞靶场。

相关实验：401 基础认证钓鱼 

```
https://www.hetianlab.com/expc.do?ec=ECID172.19.104.182014103117160200001
本实验主要介绍了401认证钓鱼，通过本实验你能了解到401认证，学会利用401认证进行钓鱼。
```

**11/6**

欢迎投稿至邮箱：**EDU@antvsion.com**  

有才能的你快来投稿吧！

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDH643dgKUQ7JK7bkJibUEk8bImjXrQgvtr4MZpMnfVuw7aT2KRkdFJrw/640?wx_fmt=gif)

戳 “阅读原文” 我们一起进步