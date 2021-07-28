> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/3PvX5Cz04odUkInPbPUi9g)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **106** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/QkjvmbC1CD0zJ9hBlrElSv4ZqETGn3otCM8UZsEBuQBYVeoI2ibx5W6ZXPchGjiaGLjyicLfp0en3M5ibRfvG04pag/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/27

靶机难度：中级（5.0/10）

靶机发布日期：2017 年 10 月 5 日

靶机描述：

Calamity, while not over challenging to an initial foothold on, is deceivingly difficult. The privilege escalation requires advanced memory exploitation, having to bypass many protections put in place.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/D7MJlTPSSr6Oa72xMxnt7RPsQtO1D57IAib9HJAvDCTkxtAqwY6KZACpmdKNmDicNjb0hKiaicZIx1F1gnibbJ0Zmmw/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVD0DDiayCTCxSYialE7pvtfE1icvdmDCf8xW3XP25yELuDljfmoQFjHapKg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.27....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVD2C0x6LickEbGOZcx4rDjvQuiaJZwKkC1VU1ribPTa16xHq493WzFaqMJg/640?wx_fmt=png)

Nmap 发现开放了 OpenSSH 服务和 Apache 服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDicZgVMic82CO9L7CNbUpgUPHoHAMgacjsxbeP2Uste8KhnvD2CWib8nCw/640?wx_fmt=png)

在首页上没用有用的信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDkIUf0TLucYh4KFBYARibpZcFSr3QbJStDktBuOzVN86BoNz29AdNNIg/640?wx_fmt=png)

利用 dirb 进行爆破... 发现了 admin.php 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDwZM3ZEbPUr4uu51HMUQ1mWO3s8KSv0Egf0lIGpc2rfk7icylmOnOBZg/640?wx_fmt=png)

打开 admin.php 页面，是个登录的页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDAmuqOfFSmU2h5I023BxKhpHlRXicqAhkgUAFlEvhibIJacuapdGre1JA/640?wx_fmt=png)

在前端源码发现了 password....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDoKwXNK36M38V4ds2TbLJJJWFmBleOe77tWJprha3pELhZm1kPpItlw/640?wx_fmt=png)

利用 admin 加获得的密码，成功登录进来，看到该页面给的信息允许在其中运行 php 代码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDXyezxZJGpl3fz4W5ZAqqzceySs1omsCzLzTxfw9CHBIiaN0KYiciasz9g/640?wx_fmt=png)

测试发现，是可利用 php 代码的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDoqOPxjS8ic67X1YHxpFVrG1p9ecjZT2XGQGL2WnTfWtxTko8lW1xZNQ/640?wx_fmt=png)

这里经过直接简单代码 nc 获得 shell 外壳.... 但是获得的外壳直接 1 秒就中断了...

利用 burpsuit 进行拦截注入，查找到了 “列入黑名单的程序可能造成的干扰 nc” 信息...

这里不能使用 NC...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDeukUDahODzVU8NF97PNLvHLogOzqFg8tG3vDG73qYlDIhRicgaOz9jg/640?wx_fmt=png)

测试了一个想法，直接 copy 复制 NC 重命名为 dayu....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDmEGnI16syVa7SQlgguSYicAawVyeLdCEickHw3pItIt3kw8GwbaQIoCg/640?wx_fmt=png)

然后赋予权限....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDX9LVDml9IvM50HdWNGgyj00Isu0KV70rU8Y5tae2ZtEmt9W5EOd3tA/640?wx_fmt=png)

利用 dayu 提权，成功绕开了安全机制，获得了反向 shell....

这里通过反复测试，还可以利用 MSF 生成 base64 的 shell.... 直接利用 php 注入即可提权...

方法挺多...

成功获得了 user 的 flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDTdHjJibCO8nsj1q2s7o9vwDd4FxQv4UsudxFAm7Bw8QcCoUHe8l1clg/640?wx_fmt=png)

在 home 目录找到了一个名为 recov.wav 的文件... 以及在 alarmclocks 目录下发现了另外两个音频文件 rick.wav 和 xouzouris.mp3...

通过 NC 上传到了本地... 通过播放，没有任何信息？？？

经过 google 查找思路...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDXYV5U8jXtiamEcVAQ5Iz3OibvOfynNrhTJfjINVnOsAYvOia9MzvmwZ0A/640?wx_fmt=png)

利用 audacity 工具对音频文件进行播放，通过将两个文件导入 audacity 并反转其中的音轨，只需循环播放即可提供听到完整密码信息....

通过音频文件，获得：18547936..* 密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDyToABQYN8Bg9sWtV27ic9ib8XqHI17FGtiaOv6jx3e8BceW4WnGdOKHHg/640?wx_fmt=png)

利用音频密码，尝试 SSH 成功登录到 xalvas 用户中，通过挖掘信息...

发现用户已添加到 lxd 组中...

lxd 是一种容器技术，可以使用 lxd 以 root 身份运行进程，为了利用此漏洞，需要下载 lxd alpine builder 来创建 alpine Linux 的映像...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDzxdibIREuRzQATeqpicSib9YryUdwE9cNTc2Y3bY2p59R4TZBicRHOickXw/640?wx_fmt=png)

```
git clone https://github.com/saghul/lxd-alpine-builder.git
./build-alpine -a i686
```

可以看到成功下载 lxd alpine builder.....

使用 lxd alpine builder 创建一个 32 位的 Alpine Linux 映像.... 这里信息在前面 uname 可看到靶机是 i686...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDCzYmROMkqKFPp6nMlDedYqK0yReYvL9Hjpg0yIPxoFok7IDuN4oZ5Q/640?wx_fmt=png)

这儿会生成一个. tar.gz 的镜像文件... 上传即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDlxayNpfhibB5VUu7wVcmPpTo4n2yd1Nia2T9fudDJfhvLGdibQ1We65SA/640?wx_fmt=png)

```
scp alpine-v3.11-i686-20200520_0402.tar.gz xalvas@10.10.10.27:
```

利用 scp 上传了镜像...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDgWGPMcTvBQiaDe8XKgk0FtlpDV1BzzBqiaqFaiaMPNLLRUsbjQVZiaTFEQ/640?wx_fmt=png)

```
lxc image import alpine-v3.11-i686-20200520_0402.tar.gz --alias alpine
lxc image list
lxc init alpine ignite -c security.privileged=true
lxc config device add ignite host-root disk source=/ path=/mnt/root
lxc start ignite
lxc exec ignite /bin/sh
```

在靶机种导入 Linux 映像，并创建一个具有管理特权的 ignite 的映像...  

然后将整个文件系统安装到容器中，重新启动容器，并在容器执行后获得了 root 权限...

lxc 提权网上很多方法....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDJyyDbSltoVfmuFbpTdicNf7bsxO3ClfwIVgS9dqia3ozUDTichhHXnLuA/640?wx_fmt=png)

通过 root 权限获得了 root 的 flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMZsoDmnZYUbSvC8kkkDbVDKlibAm6uBOVhNf9Aa5uWbBOsC7YPaJZMN0WYM2eoTGB0HjtZsV9moJw/640?wx_fmt=png)

继续深入看看是否有别的方法..

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2HdeXfkKTZwpicwe5riaGpM6GQ52aA3Xguic1iaiakS5WCYu2mj57racBicPlbrH21Pz7p0Vyx1SU74MfVhkqhBGonTg/640?wx_fmt=png)

通过 LinEnum.sh 目测没发现可利用的什么地方...

但是在 app 中，存在 goodluck 程序... 存在缓冲区溢出... 这里缓冲区溢出漏洞只有 28 个字节可以注入 shellcode...

遇到了问题是没能跳转到 root 权限.. 应该是需要找到一种信息泄露的漏洞，利用缓冲区溢出程序跳转过去... 能力有限... 存放着这个问题，留着以后回来处理....

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

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