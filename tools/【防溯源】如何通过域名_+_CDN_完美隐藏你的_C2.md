> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/S_REwcYlJGpyiJb3PIwsOQ)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **56** 篇文章，本公众号会记录一些红队攻击的笔记（由浅到深），不定时更新

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

C2 隐藏

对于一个攻击者来说，被防守方发现是一件很可耻的事情，更别说被溯源到了个人信息。本篇文章主要写如何隐藏 C2，我这里用 CobaltStrike 来做演示，这种方式是利用成本最少最高效的，毕竟能白嫖域名和 CDN，这种方式还能够避免被一些威胁情报平台溯源到真实的 VPS IP，打 hvv 够用了。

**域名 + CDN = 隐藏 CobaltStrike Server**

**前期准备**

首先需要去 freenom.com 注册一个域名，在注册的时候需要挂美国的代理，而且个人账号信息也需要填写为美国的信息！

具体参考这篇文章：https://mp.weixin.qq.com/s/4LDpKKMuOHNSPxWrkv3tFA

注册完成后就可以看到注册的域名了：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H41Mq8EFhZJicUFdZhSDZ1rxr0smfFyDV75qUic2tB0LJ0ELP0cPVwqQSA/640?wx_fmt=png)

之后在 cloudflare.com 注册一个账号，然后添加一个域名，就是刚刚组册的域名，然后选择最下面的：  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4QyRhErhmmIIyNRKiangdeKwQvvuSjYIx1IYmtxqjRNOA8w3svytGlYQ/640?wx_fmt=png)

然后来到 DNS 处，找到该 CDN 的 DNS：      

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4T9m2xjqEiakMlsXD6SL31TggyfZbl3tJ9y6Fv0ZKv5otMM1WwZnbtaA/640?wx_fmt=png)

填入到 freenom：  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4YtTgFj5C4fAv5tB5ncovNfLTkEZsUfb6b8GZO6HFEWymFmibSIXKDlg/640?wx_fmt=png)

之后来到 Cloudflare 缓存处开启一下，这样访问免费域名就不会出现访问延迟等情况：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4bS7OibL1NWVvicI2blX8ePgErhesmOAujHYo6rW1z9AYYPCtIKnbZc7w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4mwXFvGhBjIzoKeUN3Uo6nlh7IqjIVecFAXU6Ug8PiaErupRX5R8TwDQ/640?wx_fmt=png)

最后添加一个解析 A 记录到自己的 VPS，名称就是域名、内容就是 VPS 的 IP 地址：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4uAYaMBwbAWdw6rGnvOOnf5EjVAo4CoOicspEuFl42Ox06vQ5PrI112g/640?wx_fmt=png)

添加完成后就可以 ping 域名看看是否配置成功：  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4lGbobJUMGdksB2fXpIx8ePlvI4Y8Myhg9cuz9ruJ2OjP91pHTIvtGg/640?wx_fmt=png)

超级 Ping 发现 CDN 也配置完毕，没有 VPS 的真实 IP：      

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4PKOtLDJPPO1Uic90V0EX92fI5Ej7znzBd1ESCHtRqMF2EbAgzZAiboqg/640?wx_fmt=png)

**上线到  CobaltStrike 成功隐藏 IP**

之后我们来到 VPS Server，启动一下 teamserver，客户端连接 C2：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4Daoxr1OUsOwV1wqJG3GVu9jXnnsDUpgqgt7S8872FHLAbMJNiaHKFsQ/640?wx_fmt=png)

在这之后新建一个监听器为 http 的，然后 Hosts 和 Beacons 都设置为域名：  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4YNwA2ibQMzx4NPAnibq9K33ia5r3dJj6RZbtA2fQjw3tiaf7djgqPTNTFg/640?wx_fmt=png)

注意 http port 端口只能设置成以下几个：

```
80,8080,8880,2052,2082,2086,2095

```

如果是 https 的监听端口只能设置成以下几个：

```
443,2053,2083,2087,2096,8443;

```

因为这是 Cloudflare 仅支持的端口，所以没办法把监听器设置成其他端口。

最后生成一个 exe 上线看看：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4ZicfBwGwE5rSTnKD28XQEzV4TbicibQ3E3wl5hU6BFfWARX8mIVNBJGNQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4xiaNqn4bLTBepEOgrgf3IF4ulA3cPfDsibk0rRNuzXYfqA3hibENC9vMQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H49aUsQhgGFzZeLmY3ChUYEiccA3YYJHMP6eRia6Hxz8T1hhPicyOnkKt7g/640?wx_fmt=png)

最后分析网络连接发现连接的 IP 已经是 CDN 的 IP 地址：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4olrMywKkyfGyFAvjToskEbmfWSBXo3R0bHE71pmx9BVicd5tfk2PZNQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4CkuFhFMYOOfzUQG7TtFdM54tGN0u6aVHWZwAY803hibQibLvyNvqCLtg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4z1UibtR05RbcydqYxnXPmlky7HQfOewiaI10Y4bpCJjolQrGOiauicx9JA/640?wx_fmt=png)

通过微步在线沙箱分析发现成功隐藏了 C2 的真实 IP:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4YYatEBCObmQh6DYZIQd2prf0OvUqic1jkiaRqiaY4uVCawm5wuuBN4t3Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LIwLy831xGAXhiaHjWeic71H4866HtO1dafUFwXK8mZ3BiaTkYx43ozFuxZPaRzCHOIs359cyOCicTvsg/640?wx_fmt=png)

这种方式能够在一定程度上防止被 BT 溯源到真实的 IP 地址，即使溯源到了真实的 VPS 的 IP，毕竟是匿名的 VPS ，除非反制拿到了 ROOT，否则也是无济于事。

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

渗透攻击红队

一个专注于渗透红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDdjBqfzUWVgkVA7dFfxUAATDhZQicc1ibtgzSVq7sln6r9kEtTTicvZmcw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDY9HXLCT5WoDFzKP1Dw8FZyt3ecOVF0zSDogBTzgN2wicJlRDygN7bfQ/640?wx_fmt=png)

点分享

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDRwPQ2H3KRtgzicHGD2bGf1Dtqr86B5mspl4gARTicQUaVr6N0rY1GgKQ/640?wx_fmt=png)

点点赞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDgRo5uRP3s5pLrlJym85cYvUZRJDlqbTXHYVGXEZqD67ia9jNmwbNgxg/640?wx_fmt=png)

点在看