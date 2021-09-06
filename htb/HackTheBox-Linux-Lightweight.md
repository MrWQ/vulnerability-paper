> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/YZHIcNsTgygzVmdv4MtTyQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **145** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

  

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/166

靶机难度：中级（4.7/10）

靶机发布日期：2019 年 4 月 27 日

靶机描述：

Lightweight is a pretty unique and challenging box which showcases the common mistakes made by system administrators and the need for encryption in any kind protocol used. It deals with the abuse of Linux capabilities which can be harmful in bad hands and how unencrypted protocols like LDAP can be sniffed to gain information and credentials.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/aUOT8MibumibTezJtREQ7iabtA23O9WAFku4Bian1vXLOpxwIk705rqQvxdoBr6uT5hxFc9wq6XibJS5FjKdbsBC1dg/640?wx_fmt=png)

  

  

  

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0nSYibNpPuXwaMplGianE87fnU6bsk5cnqOsI6rBN6zuhs7oHwW6rfeicw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.119...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0rCGkBKk7V8EU8g3KhMBIWzNZcJ3d5HGNcjBBibGeRCd918mJXlwwzNw/640?wx_fmt=png)

发现开放了 ssh 和 apache 服务，还开放了 ldap 服务...

这里对 ldap 进行了 ldapsearch 工具枚举... 发现了两个用户名 ldapuser1 和 ldapuser2... 还存在 passwd 的 hash 值，但是都无法破解... 跳过了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0BGFFibrqw5paudo8ROHV9hBZAFzJDIMABfvq2UykjsiaKVlHMDWpjXicg/640?wx_fmt=png)

登陆 web 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0wLBBxWjI0kaAJPwCb9dq5elIlH3aeK6jRbiclG2KkiaNicBEqBzdea4ww/640?wx_fmt=png)

检查 info 发现，在 80 端口上有一个防止暴力破解的网站，因此不能使用 gobuster 或 dirbuster 之类的工具进行爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0pOiaPZnLWq9cnyFrbX3PTxrIGcGtTxQnGwBBj6MsJFSdsFSFWDK1YEw/640?wx_fmt=png)

这里提示说：该服务器让我可以使用 ssh 进行访问，ID 是我的 IP 地址... 登陆试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0R0NrIcfOicx7diakHQicvdpD6pvoBqlnRS1Gxd3icFwwc8ctXSBf8O5KGA/640?wx_fmt=png)

利用 IP 为 ID 成功登陆...

检查了整个文件系统中是否有运行功能增强的文件... 发现 tcpdump 具有 cap_net_admin,cap_net_raw+ep 功能...

此 tcpdump 设置了一些上限，允许普通用户捕获任何接口上的流量...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0SWusETuc4QPG9cibG1U37ibef0QuhkCJriaClEYBzjSqOvjmLBWiaJ6nGg/640?wx_fmt=png)

```
tcpdump -i lo port 389 -w capture.cap -v
scp 10.10.14.51@10.10.10.119:/home/10.10.14.51/capture.cap capture.cap
wireshark capture.cap
```

通过 tcpdump 抓取了流量包，利用 scp 传输. pcap 文件到本地....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0grRD7Ee66sQr82kbz0v9tsaVhxcK86j9YticH6kfR5icA8adMfQvzo3w/640?wx_fmt=png)

通过流量内容，获得了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0FB05YkxE2PXfxkvwgKfX7GcMcHhicm57E2kqT9KJW9AicvMdia1dxm4mg/640?wx_fmt=png)

提权到 ldapuser2 用户，获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0m6icvrF4FwdCA8wfCEhjLomg5ESU8xoPm5ke94iakd3FDw1JZkW03tUA/640?wx_fmt=png)

枚举发现本地存在 root 权限执行的 back.7z 压缩文件.... 尝试解压需要密码...

传输到本地..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs08azseYrqJNoFs2pXf9pWaRNzUJuTVzYgwnY30HbElEIlkg79loOicOQ/640?wx_fmt=png)

https://www.lostmypass.com / 破解即可...

这里还有很多方法破解，但是都没这里快...

我随意说两个把，例如利用 kali 本地的 / usr/share/john/7z2john.pl 转换下. 7z 的 hash 值，然后利用 john 进行爆破即可...

github 上存在 python_7z 的脚本可以爆破密码... 等等

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs07ic5zHqI7M6zkiaOXImogdlTslhdgK8v7dIicRSK6UAb6lCDuwibz2hXpA/640?wx_fmt=png)

通过破解的密码，成功解压...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0Bia5NxicpJ7uEicPLgHbZdNxsoF7ibF1H2sPMs8OpsLhjBSWmt0y30tBGA/640?wx_fmt=png)

枚举解压后的文件，在 status.php 发现 ldapuser1 的密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0MHI8nfuiaqM2IPC9deAxhzqiavJXQ4IPeKPvquicQ768rYVU9LVQq9gicA/640?wx_fmt=png)

su 登陆后，还是按照先前的思路，查找到了 openssl 也具有 root 执行读取写入的权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0ycIickH6g4SeO3PuEwDcUDU52qsZ4Yribt6ngPPGNn5LpX9icetXeULwQ/640?wx_fmt=png)

```
./openssl enc -base64 -in /etc/shadow -out ./passwd.b64
base64 -d passwd.b64 > passwd
```

这台靶机和前一台靶机类似了，前一台 Teacher 靶机也是 backup.sh 具有读取和写入的 root 权限...

操作就好... 我这里提权了...

直接将类似 linux 中 passwd 的用户密码文本复制到 ssh 的 ldapuser1 用户权限环境中..

然后查看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs02gicHGibMSZ1iaeLOYf70zVWHv2SqsbhS99Ra6NEgKDAS5bGnK1cvgalw/640?wx_fmt=png)

在创建 dayu 密码的 hash...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0ibkMFp8wbTqrLk0v1WGia82577iasedVYDamaicn4PLKTiaECic5dHIltOIw/640?wx_fmt=png)

然后修改复制的 passwd 文本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMVssImB0vXkVYnlEdqvOs0aXdX3OOUC472cRnL7VUHgiajJxC7lIVqNIwaLZ8rdSpc08Qj35N6Fbg/640?wx_fmt=png)

```
./openssl enc -in passwd -out /etc/shadow
./openssl enc -base64 -in /root/root.txt | base64 -d
```

  

  

  

在将 passwd 复制回 root 用户环境中进行覆盖... 利用创建的密码 su root 成功登陆... 获得了 user_flag 信息...

这里和上一篇也一样，直接通过 openssl 直接获得了 flag....

这篇靶机不难，枚举也很简答， 没隐藏很多... 学到了爆破 7z 的不同方法... 加油

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/aUOT8MibumibTezJtREQ7iabtA23O9WAFku4Bian1vXLOpxwIk705rqQvxdoBr6uT5hxFc9wq6XibJS5FjKdbsBC1dg/640?wx_fmt=png)

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