> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/zt91-M1TSg1o6Jq5yzHK8Q)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **112** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/AhUATAqa6tibYa4zTrlvc4l1rFIH7HV8c7ibcicw1jgibbwVW2zia9JeVCleEKLjkT0RO7sJS34DVSzMJ9sGsIAn5Fg/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/57

靶机难度：初级（3.5/10）

靶机发布日期：2017 年 10 月 10 日

靶机描述：

Apocalyst is a fairly straightforward machine, however it requires a wide range of tools and techniques to complete. It touches on many different topics and can be a great learning resource for many.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/oQI1m5hhwD5Gicl7xUf6kh3ISTH6iacM05s8G12QVAykGzh7S5Po8EgeS5XJvZbiacbS8AuRQJ1VaRic18jlToOhVQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0fb0Y1M6icJJia7t9xsBuUuxZQgOLeWHYicicRpfEiahMz3mlpK0icx8qLpfMLDojhD7IwSE2IalXVBBFs9E1Z88Ka3Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/PRVgXdHra5CzBfuOaOX4dpiaoOia6WZfdos1RiaJEZJG7nrnxTkXBoianpRmkQTmqkmW3zkbaQqjAu6WwBYAmyGibiaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaS6xRQ7y04BMkCgBEHTfOMQwF9AjKfxUtvIxzLCTseibOZ1A0RxYO4B9Q/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.46....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSNUAcqibzZxdpWXEEsp6fEUz5ia8Vaf8g3sKgNwiaoM9yZtk7PpYoics2KQ/640?wx_fmt=png)

nmap 发现开放了 ssh 和 apache 服务...apache 存在 WordPress 博客...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSQhRCyKRoqagelsloKqxMKFXNFtKbicMMTtrDiaoiajuFBug2E2g7GIvYw/640?wx_fmt=png)

讲了一篇帖子... 应该是博客文章内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSuAIBMNhfDw9Y2MIfeeS3bNPS8X41qEzvSUH7zJZWLBcPM1zodVUIbg/640?wx_fmt=png)

测试是存在的... 找登录密码吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSEezoxvITn5KLsaCBicXWvgvjsbwMEIu9w6Kib21AKzEwjGKuqalTD5Bg/640?wx_fmt=png)

爆破目录发现 Rightiousness.... 原因是所有的长度值都是 157，它的是 175... 检查

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSjPWb435l81pUWqa9AibAUPnpRWUXW09VaSCq2rdnBiaOL6giaMicXB06OA/640?wx_fmt=png)

访问是一张图... 下载图片...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSMHkLTqwcUiaKNbMZCIzfhXz5EyYWfVEIHsiaibMmZlQvq4Z2LaHfn7xdA/640?wx_fmt=png)

这里利用 Steghide 提取图像中的文件... 获得了一个单词表... 应该是爆破用的

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaS8eKCKAMY4ibjT3P8ctgMednHYTLHsZ42wPId0DYYoPMRvicB21FePfmg/640?wx_fmt=png)

```
wpscan --url http://apocalyst.htb/ -e
```

通过 wpscan 枚举了 wordpress 博客用户名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSibJKGcGp1Pwr6ZMQyThqsY3TA7bNU9xwEibCOuNrvU6I1NgYTC0HxxVg/640?wx_fmt=png)

```
wpscan -U falaraki -P --url http://apocalyst.htb/
```

通过前面获得的 list 单词表... 继续利用 wpscan 进行了用户的密码爆破...

可看到获得了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/0fb0Y1M6icJJia7t9xsBuUuxZQgOLeWHYicicRpfEiahMz3mlpK0icx8qLpfMLDojhD7IwSE2IalXVBBFs9E1Z88Ka3Q/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/PRVgXdHra5CzBfuOaOX4dpiaoOia6WZfdos1RiaJEZJG7nrnxTkXBoianpRmkQTmqkmW3zkbaQqjAu6WwBYAmyGibiaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSSiarPdO3ia9fqnSwzcIjdYclWjohQibq6kYw3J8L9V6ZAVcaBMVTbGxNg/640?wx_fmt=png)

登录就是一个常见的 wordpress 框架页面...

直接 shell 注入即可... 右边很多 php 都可以写入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSMLodxIBxcCqlnHsfT4ACkibl6hj7ENib7yTCjl4ibQWbia3WDNf6ibexAGw/640?wx_fmt=png)

测试正常...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSdV9xmzb2Hhw428fZ2WvIgzZMywGaibuYypfLHT8mVzUXMicFic1DqMyxg/640?wx_fmt=png)

简单一句话 shell 提权... 获得了低权 www

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaS8cyA0s5ZibDCtuE8CZL9JuGDEzNwUyk9ePBSuEyyWPqicT0ia4gia1jdwA/640?wx_fmt=png)

通过手动枚举，获得了 user_flag 信息，在同目录下获得了一串 base64 值....

通过破译，获得了一串密码....

测试发现密码是 falaraki 用户的登录密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSFGQO9icT2GMhISrpQ6xhCM9K4LUKo9axk3icQ5V55SqT2nBxQDmicU46A/640?wx_fmt=png)

继续在 www-data 权限下进行枚举... 上传 LinEnum.sh 枚举发现 / etc/passwd 存在可写入的权限...

直接创建一个用户具有 root 权限登录即可获得 root...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSH6V7qZxoTOJjVZYyrGmWTUCcdsylMa41RGTh1VFtWDsPiaLicyzJWtEQ/640?wx_fmt=png)

利用本地 openssl passwd 简单创建具有 root 权限的新用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9Z9NnWia9jhgXLa7ibwTiaaSB2QjhqEjACBM9zV3tue4j69ekbKFRPo8RPQuV7HNXElib0hqAPzibX5g/640?wx_fmt=png)

echo 写入... 登录后成功获得 root 权限，并获得 root_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/AhUATAqa6tibYa4zTrlvc4l1rFIH7HV8c7ibcicw1jgibbwVW2zia9JeVCleEKLjkT0RO7sJS34DVSzMJ9sGsIAn5Fg/640?wx_fmt=png)

周日花了些时间重新部署了 2020.2 最新版本的 kali 系统，并使用了新发布的 KDE，使用了一天 K 桌面的环境，首次使用还是不太习惯，但是我个人比较喜欢接触新的东西，旧的东西可以熟悉记住，新的早接触早了解...

加油！！

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/oQI1m5hhwD5Gicl7xUf6kh3ISTH6iacM05s8G12QVAykGzh7S5Po8EgeS5XJvZbiacbS8AuRQJ1VaRic18jlToOhVQ/640?wx_fmt=png)

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