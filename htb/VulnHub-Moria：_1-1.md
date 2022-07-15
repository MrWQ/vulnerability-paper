> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/PHwoFzdk7-XDvN8fIDCJpQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **46** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/leMkDaXRbiboDwJS3ickCDzX18rO7YT3QKjDn2b7PFbb9VqmfDhlTtobtDvDHuAXEibFmZs7HL7W0Wq66sSl7vk2w/640?wx_fmt=png)

  

  

靶机地址：https://www.vulnhub.com/entry/moria-1,187/

靶机难度：中级（CTF）

靶机发布日期：2017 年 4 月 29 日

靶机描述：

+---------------------------------------------------------+

|                     Name: Moria                         |

|                       IP: Through DHCP                  |

|               Difficulty: Not easy!                     |

|                     Goal: Get root                      |

+---------------------------------------------------------+

|                                                         |

| DESCRIPTION:                                            |

| Moria is NOT a beginner-oriented Boot2Root VM, it will  |

| require good enum skills and a lot of persistence.      |

|                                                         |

| VM has been tested on both VMware and VirtualBox, and   |

| gets its IP through DHCP, make sure you're on the same  |

| network.                                                |

|                                                         |

| Special thanks to @seriousblank for helping me create it|

| and @johnm and @cola for helping me test it.            |

|                                                         |

|     Link: dropbox.com/s/r3btdcmwjigk62d/Moria1.1.rar    |

|     Size: 1.56GB                                        |

|      MD5: 2789bca41a7b8f5cc48e92c635eb83cb              |

|     SHA1: e3bddd4133320ae42ff65aec41b9f6516d33bb89      |

|                                                         |

| CONTACT:                                                |

| You can find me on NetSecFocus slack, twitter at        |

| @abatchy17 or occasionally on #vulnhub for questions.   |

|                                                         |

| PS: No Lord of The Rings knowledge is required ;)       |

|                                                         |

| -Abatchy                                                |

+---------------------------------------------------------+

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/FAf3SbzREv1yEsWZqMDExrPvhOutWaLH9VkgQiaS11ia5Y3Xun2olnDwIhLlOiaMWe0UGE1uMpeHx4ma7lOjn8xpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VtRWAxRvv7GXYcc2w086cwOxcc4libkI8ibn6rD3yBlZ7vd0fH2TaYMKicrgibMcRBbxTQ5fbCJs4AgldkHtBiaPOdA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_svg/kSiaeFj92SMyLghhftE2Ls37f4uZP8ZCOxbnsSQ1P6n6AsfOBzt5PrmdTAS3OOhPMXiabAsyKKf4QuEfoCrj9yLNlmkc5ddlpQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibCibCRcqPHLnfHJvzssrym9H7nNyOU2wOGnW7gP5TZ2iazOtArDN6DvvQ/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibJNsWZSx4svEAcHSgatC8ylnHcjJGhibecOqgT97lhUOnc8AwLwibaZRg/640?wx_fmt=png)我们已经找到了此次 CTF 目标计算机 IP 地址：

```
192.168.182.145
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibUXATPlNhiawsRM7Ak5zy6yPnFWibbEaqOIx0Dcqlf5zLZFGqia3GjB9zw/640?wx_fmt=png)

nmap 发现了 21、22、80 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ib9QHWc6xCmCnulLw5vib2HMXPu8z1LepESUH9Is3G1HwIHAOUGH6NFGg/640?wx_fmt=png)

图像显示的是魔戒，这是《指环王》电影中的矮人城市，打开门有一个谜....

可以看到有 Moria：.... 谷歌的翻译是说：Mellon 必须是密码之一???

先放着吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibMtvq2Uxh0icXsGZcKCAlkHOWC1kYicvYpjLviarlAmRDGcrrhK256DYCQ/640?wx_fmt=png)

dirb 发现了 W 目录... 看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibj7ibjBHFCB5ia3GJNnVumCXItkIZBLXPK8Eypicj2zI9p0qDRwsUSib04A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ib4aOjlS7Tia621SowGN18qexwvSr28TH28cOtQWb0uQIahLEIHWgNtxg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibXNRLLfJPFibd5yMhkQNXiaibcYHMgHa06icLGengvoVEhBwHkicrhvQVY2A/640?wx_fmt=png)

让我们安静点...Balrog 会听到我们的声音？？

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ib6jsXqlU9zKf7yfyx59I60XwWsSgkzibBf7wL5uU3BrcRVxDyOiaHyxww/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibMloIMcz9UZkkLoIoibrnKobm5bJVquSzibf5wUkPvQW76sVHVmedeh9g/640?wx_fmt=png)

每次 F5 刷新，都会发现内容变化了.... 这应该是个随机文本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibxP0gzZQdTTjUv79ZG4IficxfAVoGcJUNFHSQHPypMHia9XCnLILvz9Bw/640?wx_fmt=png)

```
dirb http://192.168.182.145/w/h/i/s/p/e/r/the_abyss/ -X .txt .img .html
```

找到一个名为 random.txt 的文件，果然隐藏在里面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibvJpicuYo2icbaUlB9J5vN3qMCicT1CMIhM8vR0KbeY4Ahm8rT3wbeBcYQ/640?wx_fmt=png)

这里面有很多大写开头得名称：Balin，Oin，Ori，Fundin，Nain，Eru，Balrog... 都有可能是用户名...

还有就是出现了一个词，knock 这是敲端口？？估计和我上一章内容一样，要完成某顺序得端口敲震，然后才会打开某些服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibJm5aTPEHamL1zppD4SVkY9XvnuzZPQiapARLpaC7EYwecMFkNV9oic0Q/640?wx_fmt=png)

我使用 Wireshark 抓包，刷新了下页面，发现了一些敲门事件，嘿嘿

这边我将 77 101 108 108 111 110 54 57 端口按顺序进行敲震...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibVw0rUryia5YMXfZgzAMc8QvdwmAIpECjib4WDfff5jSqNQGZxpINeR9g/640?wx_fmt=png)

```
for x in 77 101 108 108 111 110 54 57; do nmap -Pn --host-timeout 201 --max-retries 0 -p $x 192.168.182.145; done
```

运行命令依次敲了这八个端口...

敲完后，nmap 扫描并没发现什么东西...

想了半天，发现 77 101 108 108 111 110 54 57 会不会是和我 no.31 当时做得 ASCII 是这里面得值？？？我去找下看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibtWR5ARHticZJp1Tyl76VS8sa4JX2PUZGwl1jOLlYiah4OcibZrabg8ITg/640?wx_fmt=png)

通过对 ASCII 表进行翻译，发现：Mellon69.... 在端口 80 的索引页上的门的图像中就有提到，Mellon 是 Elvish 的朋友... 看到方向是对的...

The Balrog is not around, hurry 有这一句，让我们别吵，Balrog 会听到我们的声音...

用户应该是 Balrog，密码是 Mellon69，试试把，猜测

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibjmu9nVw7jbhjS2mGR3PhxGhhKCL8CpqQQtia92MDZrXGB5b3fp1IKXw/640?wx_fmt=png)

进不去... 但是 Balrog 是有效的用户名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibfETltzwmtaQUUPps11ibYodUtFD5C36xLsAHrQz6RiaVg71vxcjZyw4g/640?wx_fmt=png)

FTP 进去了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ib7abKo4jow1lc71UDw8Q1QeYrGjSicaqYIOA42xkEaLMJ85qxKuI2Libw/640?wx_fmt=png)

直接奔向 ftp 的上传目录，就是 html 目录下，发现了

```
QlVraKW4fbIkXau9zkAPNGzviT3UKntl
```

隐藏目录....  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ib5398SPicN54vvRPna0fBHT82pn7ZARm2C7OjibjZjicJIRWL3KALXaS3g/640?wx_fmt=png)

囚犯的姓名和密码.... 使用在线哈希值破解，发现破解不了，返回信息 0...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibMR7VreRnByVX88JnfCb4qr9enMeLEHrQ9mMHxyz73WfbrEG1BU0B3A/640?wx_fmt=png)

发现了 Salt value... 解密

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibvqE4JzvqmLy3tXv4kZuVGAzIVUOkFIhAyXb4nwBCl4Zh5J5zNQ5KGQ/640?wx_fmt=png)

结合了用户名，哈希和 salt...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibt0diaS373xoUObJ6X58p2BIy1Ncc16hz3DIs96iaULx6pGt3LgPW4XDw/640?wx_fmt=png)

```
john -form=dynamic_6 dayupass.txt
```

使用开膛手 john 进行破解... 成功

```
spanky           (Ori)
```

先使用第一个用户密码登陆...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibWboxVJM3h9ue05Yln2Q6s2EFnWvWsYicJic2GGJbMkavtHJzAI2B5z8A/640?wx_fmt=png)

发现了一首诗.... 没啥用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibdo5UVvK0PqgL9xfiaqBTVIbU1UEsuAAovU4bQxkuGK8OWPZql7AMGPw/640?wx_fmt=png)

在. ssh 目录下发现了 id_rsa，密匙啊... 直接用登陆看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMhvUmJ5U8KGaNALTCp9M9ibGvvRdtDtgCibEZiaqalddMF6Z56NicBgFXnF058DKpWmr8iauUy5d4ib0aA/640?wx_fmt=png)

使用本地密匙登陆，成功登陆... 获得 root 权限并查看 flag...

![](https://mmbiz.qpic.cn/mmbiz_png/leMkDaXRbiboDwJS3ickCDzX18rO7YT3QKjDn2b7PFbb9VqmfDhlTtobtDvDHuAXEibFmZs7HL7W0Wq66sSl7vk2w/640?wx_fmt=png)

  

  

这边开始对 80 端口的文字翻译解答... 利用 dirb 进行目录爆破发现 W 目录... 在 W 目录发现随机文件通过继续通过爆破发现了 random 文件... 通读意思后经过 Wireshark 抓包发现端口序列.... 通过 ASCII 列表解译获得密码...FTP 登陆后发现隐藏目录... 经过 john 破解密码... 最后发现 id_rsa 密匙进行渗透成功... 不错的经历，加油！！！

由于我们已经成功得到 root 权限并查看 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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