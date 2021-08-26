> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/lX4QoI1CVS9SGTPM6KuS6A)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **136** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/154

靶机难度：中级（3.3/10）

靶机发布日期：2019 年 2 月 4 日

靶机描述：

Ypuffy is medium difficulty machine which highlights the danger of allowing LDAP null sessions. It also features an interesting SSH CA authentication privilege escalation, via the OpenBSD doas command. An additional privilege escalation involving Xorg is also possible.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/o62ddIpxjBd0kv6p3zb6uf1GiaCo9PiaF12hWQQSurxFPuVIDtsNTgUpjjvmib7GxKXNePVMAwJfzuib52MWoORPYg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/Clq0o4fE5u6X5A1maTmqcvtEibdrsDO41kZPibRCHsX3Koj69GFK2qOyPwdcrgcDkHklrdJzBCiaQPuMVe11oSYHA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27giccETuFDRz9dNpuVgPCoD4mqiaiaqwW4AbGQicZztWROicicJ5MROtCrRj4pg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.107..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicWtUTnQj60VrTcozLvSet76YyMOHnfAFpYaVT30WOkYaQGcbEfao7eQ/640?wx_fmt=png)

Nmap 发现开放了 SSH，Samba，LDAP 和 OpenBSD 的 httpd Web 服务....

这里访问 web 拒绝链接... 无法访问....

smbmap -H 也拒绝访问....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicxvSwhTlloevFxRicoKnV0ibP7nPyb5jG6lJ20eBb8qianQXcZicws0TpCg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicYWxd97gkBd78XaQxWMOEzzDrslvrodGfCUQib3YYOWSbZ1LmD6yIN4A/640?wx_fmt=png)

```
nmap -p 389 --script ldap-search ypuffy.htb
```

直接利用 nmap 枚举 LDAP... 发现了 uid 和 password....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gic0jQyv7X7CsIfZmYbKdDwEwic2UK6SaDS02NMT9K4ehYKibFXHSRgl9Ww/640?wx_fmt=png)

直接利用获得的 uid 和 password 进入了 smb...

并下载了 key....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicJ2EfMf2CuqPnh4qNmFqLLyDSnEhMehIaofe5M2raBQKdCMzKmBIpOg/640?wx_fmt=png)

发现这是 key... 要将其转换为 OpenSSH 格式，使用 puttygen 即可....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicYhlTibQjib6RXxxoUHw1prib7DicqpiaECRo4wGQqTSXDfYHnjFCn6JgibibQ/640?wx_fmt=png)

利用 puttygen 直接转换，然后成功 ssh 登陆到 ypuffy 用户权限中，获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicohKHgQzIvvCUg53GL7rib3sY2S3icCWiaLmTPgSrEdI9BfZskcicshWricA/640?wx_fmt=png)

开始 http 无法访问，吸引了我注意，我开始枚举信息...

在 httpd.conf 发现了 location "/userca*" 和 location "/sshauth*"...home 下存在 userca 目录... 可用于 ssh?

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicuhe7tDcicaJoq1zyFygZia84AooKMWhdz9Y53k9g9R4qVoiby8RKEPISw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicqR90vLyLEeNyKicAl0hozVTWiazWHpnKBtlXdmZwDyBIRyAEYTZ0mPfA/640?wx_fmt=png)

可看到该用户可以以 / usr/bin/ssh-keygen 的权限运行命令 userca，枚举 / home/userca 目录发现目录中存在 ca 私有 SSH 密钥和 ca.pub 公共 SSH 密钥....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicYfClTIMPYas59DlYPUW2ygswOUz8xDmElWg8uEEsAdI9NY1AREiboLQ/640?wx_fmt=png)

枚举 ssh 目录，查看 ssh_config 发现了可利用的信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicibaLykonJpZokausB7yLGm6ngZ1v2nib0yOddcbPWhqic2ViaICqKshuhw/640?wx_fmt=png)

curl 枚举，获得了 root 的密码信息....

这里只需要使用 ssh-keygen 为 userca 创建一个有效的密钥即可提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gicv2Mn2exzADGWiaibicVGTj20wuibIKibDezh4ZSNqtNnHic27GyequFibx0KQ/640?wx_fmt=png)

创建 key...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOYTajr9ycSfkCZmibIL27gic87nc57Dia2qjy7Vpx1ubhszUfRefGweEAYm2zoANpb7ibAzYaH0Kn7nQ/640?wx_fmt=png)

这里利用了 doas 命令对密钥进行了签名...

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=png)

然后成功获得了 root 权限，并获得 root_flag 信息...

LDAP 枚举 --ssh 提权....

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/o62ddIpxjBd0kv6p3zb6uf1GiaCo9PiaF12hWQQSurxFPuVIDtsNTgUpjjvmib7GxKXNePVMAwJfzuib52MWoORPYg/640?wx_fmt=png)

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