> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/KXs6yhLpzCHamSWZbwrzfw)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **168** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/HhnEClSmc37Bxb1zZj7tialnNnk1dnmft6ibz6n2lZaheQClZ7FHjs4RElm391lFKwznAZicyxB8VmZvSSEGHrXHQ/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/207

靶机难度：中级（3.9/10）

靶机发布日期：2019 年 1 月 8 日

靶机描述：

Bitlab is a medium difficulty Linux machine running a Gitlab server. The website is found to contain a bookmark, which can autofill credentials for the Gitlab login. After logging in, the user's developer access can be used to write to a repository and deploy a backdoor with the help of git hooks. The PostgreSQL server running locally is found to contain the user's password, which is used to gain SSH access. The user's home folder contains Windows binary, which is analyzed to obtain the root password.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/KLN26icsnib2XYJCRIIHRBibXLekicoWWj63pjFjuYHlBicDncmnjctDfZtAbAodw3tO4bOczk4fxTl7EO5Pq2IM2LA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/fw07L4QCL8zxn8yLTxgxtaKEBOmKyfeXzaxN31SQFNho0f9EIq2uoMDO2O2PzQEJB0sCg2O6oeeyT10sNPHgSQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/65kKfpfiaHYJb5Dich6GdMtnZre8jhjTibGVwwOgApImzZWplXUib7CrRLG0ZlcicwWM9spLF5qwfdicWeLtwabw5VWw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwquJcUZYVZWgupqqNONs7mD1OMgkZ3bpsLnkDK8L4fJ3wN5uibdic1oLQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.114...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwSPTURac7OIiauzped4YDHYjM9kOye2q4lQfagBGylbibomRXEPKewjbg/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 22，80 端口，在利用 nmap 详细的扫描了这些端口情况.. 看图即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwH76c2mm3bibicFPCnhzX0y0fyaWhhv4gJYC7rJs4cEDxyAOtgkf40z7w/640?wx_fmt=png)

浏览 web 页面，可看到这是 Gitlab 的登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwSPh9UrBrIEOJcqA1Wg9ykP8LDLxx2xSPicIT8pvic24FOvjErExlAtNQ/640?wx_fmt=png)

发现了很多目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUw8WIPZ5z8FZiayXY9jPx0zAtwhib5odFECJDKxQ7YHGKPqOGSI5dEhHrg/640?wx_fmt=png)

存在 html 页面信息，访问....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwDn1RWl3u4cbXxz3sticGezupwQWw2Wd43kLtcWaB1CcePUXNedyVI3w/640?wx_fmt=png)

这是一些访问页面... 枚举发现了问题...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwOSt156LyMw2JicT0zh6Plt6wMTAqq4PLIRDX2SbRnuoSEA9AKRicxNbg/640?wx_fmt=png)

可看到查看前段源码发现了，Gitlab 中包含了 JavaScript 代码.... 翻译看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUw7dibAUyV2l46FG4hffRU2O4qdibOlvaka4eIvJAvPicooWlrje2PLIictg/640?wx_fmt=png)

```
https://beautifiler.io
```

进入 JavaScript 页面，转译发现了一些规则函数... 利用浏览器自带的 JavaScript 执行看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwjjU6gUJ3tSIEvh9OvIU0W62PEQ99ibwrEibISRw54lHGzJRJr8RDDylA/640?wx_fmt=png)

编译获得了用户名密码... 这是隐藏信息呀

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUw5xqV8R4QzKaX0vPMiaQrPVDaHLribQpu0zRTrRK97Aay5kHyiabgcOWOw/640?wx_fmt=png)

获得了用户名密码后，尝试成功登录...

看到管理员拥有两个存储库，继续没两个储存库看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwE8RxTpXNRsFNMwFCwy8yfSRKbqibhCF9Xj3L7icudvSZI5EB88jJkGiaw/640?wx_fmt=png)

Profile 存在简单的三个文件信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwwszEr6zEN20ZlGiaHrE6BvYCBvicKBXz6KxZ9GHFzzYpkibcP1ibtuBhuA/640?wx_fmt=png)

查看 index.php 源代码，看到在查找过程中发现了相同的名称和描述...

该站很可能托管此存储库中的文件，还发现用户 Clave 具有开发人员访问权限....

URL 中 / profile 目录在前面 robots 也发现了...（记录好）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwgfHysTuVwP97VsxIicaj1fYfZ2yJtfGXxicVLNia5KSy52rcTvksMAaqA/640?wx_fmt=png)

另外 Repository 也存在 index...

查看源代码，该页面接受 JSON 输入并从中读取属性，当一个发出合并请求，代码进入配置文件夹并执行 git pull，它将自动将分支中的更改合并到配置文件中？？难道存在 git pull 漏洞？？

测试看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwAIYCialVypNuW7wlGy8ZxgMo8WBmIeb9h7iap16nibz9naSuXEibsiaicq7g/640?wx_fmt=png)

创建一个新的项目...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwk9IZxm7fQNhRrmRKzpCrproicpLj8ZicjsKt883m5cJqv5N4ZNkLLezw/640?wx_fmt=png)

命名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwiawf5FkycOk9YtDd8awRa4fl9nYRPpu1WjD270c1F5ibibLMoJMSnE5PA/640?wx_fmt=png)

创建新的库信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwj1DdwwawibWcvvkkfiaW0HR590NicMhZVcMTGwR5ZfSSxBRTzltEfnBRA/640?wx_fmt=png)

写入 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwzQRPWPVKiaCsE8G4fjuh2X6qicmJ6G04UEhep94CyIQNztXEVrcOictHA/640?wx_fmt=png)

保存同步...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUw6cl4M98s7cM1KTE30wrmIYDulj9XUZXEOZ3aV0WXdaebdbI2qN0uWQ/640?wx_fmt=png)

保存同步...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUws0dFEf7iaomxXMRQNDrAezw4xyibOibgJ2q9cGJZkGZGRKTiaeLSOdf3yQ/640?wx_fmt=png)

可看到成功写入恶意文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwOkQzeuhlI8HEAj2QSRKwOvFa57Se9w3MvCx56a2RqyNm4KvAs8rKVw/640?wx_fmt=png)

尝试后果然成功了.... 获得了反向外壳...

但是无法获得 flag 信息... 低权用户

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwxTgnpK3ficxSXqkhiarTuy5kcejSKeSQGyYV01TTjSAuTZQ1ic6xvCxDQ/640?wx_fmt=png)

可看到开启了 5432 端口...

5432 端口是 PostgreSQL 服务器的默认端口....

在前面枚举的时候，就发现了已经有 PostgreSQL 的代码库泄露的情况...

由于 postgres 服务器是在 docker 中运行，我们将无法访问客户端二进制文件，但是可以使用 PHP...

利用前面的代码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwxfAwlGLexc8qHjwyQX8LHkaicLVpzfW4023g0H47xW7szQoiczVP4DUw/640?wx_fmt=png)

这里我重新截图获取过的代码信息...

利用即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwIxXuSjFgkDHibWB4gZ171SvvoiczRmRric1TLoasKxibExHc85picA4MXIA/640?wx_fmt=png)

成功获得了其中的信息，用户名密码...

这里如果没有 PostgreSQL 代码的利用... 可以利用 https://github.com/jpillora/chisel 工具把 5432 端口流量镜像到本地，然后从本地..

然后 psql -h 127.0.0.1 -p 5432 -U profiles 登录可枚举到用户名密码信息... 不演示了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwPThJXuCbGqvxKfzDyicWghOPxEgnvVxwPzlOW2xiczsrLTQT20FLMiaicQ/640?wx_fmt=png)

成功获得 useer_flag 信息...

这里还存在二进制缓冲区溢出文件...

这里我不进一步分析了，最近 IDA 出了问题，等我部署好了在自己演示学习... 在另外的地方我就发现了可提权 root 的地方... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwT4NJXC42sqjH70PibZfhp13DsWm7YBQ7Hc6QDSzYibzCBVXHIjEnllibA/640?wx_fmt=png)

```
https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
```

可看到 sudo -l 存在 git pull 漏洞提权到 root...

这里的原理和前面 dayu.php 拿 shell 原理一样... 开始吧... 不懂的可以看看我给的链接文章更深入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUw6nDYfS0u5AYTEibVErRbVypD9qeVIYa9AnAbkriaEA9OfO5OtWCal3JQ/640?wx_fmt=png)

将 profile 存储库放入到本地随意的文件夹，可以是自己创建的...

然后在 hooks 目录下创建 shell 文件... 赋权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOlT21L2XoiaXUfzKgic21wUwqKaoVfMURJ5jweVwqmguWEuG1onHFCDT3QVfwibToTlMYFMsFy8PE8Q/640?wx_fmt=png)

最后记得在 profile 网站页面创建一个新的项目... 然后在创建新的库信息... 和前面步骤一样...

![](https://mmbiz.qpic.cn/mmbiz_png/HhnEClSmc37Bxb1zZj7tialnNnk1dnmft6ibz6n2lZaheQClZ7FHjs4RElm391lFKwznAZicyxB8VmZvSSEGHrXHQ/640?wx_fmt=png)

在本地执行 git pull 即可获得 root 权限...

成功获得了 root_flag 信息...

中规中矩的靶机... 有几种方式可以获得 root 权限... 缓冲区应该是难点吧... 但是我跳过了... 加油

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/KLN26icsnib2XYJCRIIHRBibXLekicoWWj63pjFjuYHlBicDncmnjctDfZtAbAodw3tO4bOczk4fxTl7EO5Pq2IM2LA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/fw07L4QCL8zxn8yLTxgxtaKEBOmKyfeXzaxN31SQFNho0f9EIq2uoMDO2O2PzQEJB0sCg2O6oeeyT10sNPHgSQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)