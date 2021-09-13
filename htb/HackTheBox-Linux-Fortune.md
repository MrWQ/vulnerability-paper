> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FmlYK9b1khY8nj_jf8OPrw)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **151** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/178

靶机难度：高级（5.0/10）

靶机发布日期：2019 年 5 月 21 日

靶机描述：

Fortune is an insane difficulty OpenBSD box which hosts a web app vulnerable to RCE. Using the RCE the CA key can be read, which is used to create HTTPS client certificates. The client certificate leads to an SSH login, which helps to bypass the firewall. This allows mounting of an NFS share and dropping a suid to be executed as the user. An application is found to be using faulty encryption logic, which allows for escalation of privileges to root.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_gif/2fbDBvOuXZGbHjYNeGaf58HwAy5zyicCibuONy8NJRDialwYN16NDejaTZxiaHapm2Q1zd5MrD9UhRpicVyNDXNR7iaw/640?wx_fmt=gif)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/9WTLCp0tMMcojGXDZGvGR6pjfePKGt7J4xJfHdVyqSFcf84XuVxG16zHn35EWxeCK8zoXKItn2YPK0ILu6Uj3Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwY5vTeOq3fZcrWycbTOsgo8icHoicHnX1xHcKQGsEYzQhfD2f1oygcDicWQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.127...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYgYxhGFtSsI1qWcNDVwUfiamW5lKsea6mb0sR8u5zQ3a3vy1bLmn99Ow/640?wx_fmt=png)

nmap 发现开放了 ssh、http 和 https 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYx1npphZ1Z0Z5kiaX1u6HGHUMu087MSH9T2LoH0gaY1AG58icOlVsT3gg/640?wx_fmt=png)

访问 http 页面，简单的选项页面，每个选项都会有一段语言描述...burpsuit 试试有没有注入..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYhDm0aCxwb8XQsVMlC6ZSSgj5oRUNM1oBwEmlqWVB914ogCx1iae8o8w/640?wx_fmt=png)

拦截...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYsaH56iawyvdypxQmaeZ9r8y3oLrPT7nGEbWuuVtiaVjDHVEqib4tDMEzw/640?wx_fmt=png)

简单命令注入漏洞利用... 可以查看到用户有哪些，重要的有三个用户目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYb9zzjiavRf1zrX8piamNXuVMD5toUdZZqzPGnmk5RFOyXolGTpFL4z7Q/640?wx_fmt=png)

在 bob 目录下 / ca/intermediate/certs 发现了 openssl 的 key 文件信息...

主要用来创建客户端证书的，这里存在私钥 key 信息... 读取保存到本地

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYTzCHW4mG97v837iaicnLssdyEG1mH8367zoJnicJicSbqYqbuz9wrSvWvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYMDrYNhWib2sw7l2Ebl9MnIHTjbfqXTFOYjGZXok35PA75OE4sprBGrg/640?wx_fmt=png)

读取了 intermediate.cert.pem 和 intermediate.key.pem 凭证... 利用 openssl 创建一个客户端证书即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYRt2F6h02WT94Nv13m9NKNBf7VbYz56WgVrbIBUDYDTk5uKWHKaO9QQ/640?wx_fmt=png)

```
openssl pkcs12 -in intermediate.cert.pem -inkey intermediate.key.pem -out /tmp/intermediate.cert.pfx -export
```

创建了 intermediate.cert.pfx 证书... 利用火狐浏览器载入即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYz0pUcQ1Cr4wIMxtz8mgMZt5Io9gJ03HnKnmEG4UyvicPcMoe9b21vcw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYc1yGnwTBWMoEXyya6fibicCJbSEZoPgY0DKDE9ebwX3E4TgFOYQ2KiamA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYbloeZth1OzIdIpluVqlE4uw4ZeOXqliaccAWRFAiawTyfeqCFIDMDV8w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYN62YyYibicD8YUyKiapKSyrZR3aOXicKxZNpTss21slp59Nz0T8HNoicndw/640?wx_fmt=png)

可以看到，将证书载入浏览器中，重新访问靶机 http 页面，会自动认证是否载入创建的客户端凭证...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYxNz8CHyAB0CAPmScw249QicGmK20yXvYMobibojOicuWOPGAZ5DficzK1w/640?wx_fmt=png)

利用创建的凭证，跳转到另一页面...

说到您将需要使用本地 authpf 服务来获得提升的网络访问权限。如果您还没有合适的 SSH 密钥对，则需要生成一个，并适当配置本地系统才能继续...

点击 generate...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYdgarw3E1NZpglaOcxlH6DPTXfRNWUiazLG0icglozc90xEp5JZiaAL5AA/640?wx_fmt=png)

generate 跳转页面，提供了 SSH 登陆的凭证密匙...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYGkrW1KojquC9xSzVKks00xbPoVGcopUianRlszDWJEK3zRKertQONNg/640?wx_fmt=png)

当利用密匙登陆后... 提示已进入认证范围... 猜测是打开了某些端口，类似放行了权限白名单模式...

利用 nmap 扫描发现 NFS、RPC 和 8081 端口都打开了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYn0d3E6yQ2WnKxSRNehTtgZMlonV0X4rG6nQg6HD1CLPdtPLPHRr28w/640?wx_fmt=png)

导航到端口 8081 会看到此消息... 提示的信息，服务停止了... 此路不通

查看下 NFS 看看..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYlDeYqyLg4A3a7Ro6GHFEXTjuUMcbGtCDibcTpFw7NDGtIq0ZS740tCQ/640?wx_fmt=png)

```
showmount -e 10.10.10.127
sudo mkdir mnt
mount -t nfs 10.10.10.127:/home ./mnt
```

通过挂载... 获得了 charlie 用户目录... 等权限，读取发现 dayu 用户 uid 和 gid 就可以查看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwY3SfTia0iauciblKfdPq9oAE8ibd8shnTdKu6kLHZsNB4iavnVVPq5XczYwg/640?wx_fmt=png)

我的 uid 和 gid 是 1000，直接进入了 charlie 目录中，查看到 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwY6E1Tvy33U09s4nNgrFH1WZD7Ft3jGAM4Ycx07bYop74RxQBMlR66lA/640?wx_fmt=png)

```
ssh-keygen -t rsa -b 2048 -f id_rsa_charlie
```

由于目前只能查看 1000uid 的 charlie 目录权限信息...

查看到该目录可利用的目录. ssh，这里利用 ssh-keygen 在本地创建了 rsa 密匙凭证...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYSBFYpqfbf4MibNW8icp2LDwbnXEP7Vejs37rk8QWMVs02NcgvTdiaJSNg/640?wx_fmt=png)

然后上传对应密匙，ssh 登陆 charlie 用户，获得了整个 charlie 用户的外壳... 更利于后面的信息枚举...

查看到改目录下 mbox 文件信息...

给了很大的提示，意思是说在 pgadmin4 的文件中，存在 dba 密码信息，和 root 密码相同...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwY2NibVJveEaDibN9YiaofS782XEiciaia4Odycfv9DR3rRPa9bu1WMmGbtlSg/640?wx_fmt=png)

```
find / -iname '*pgadmin4*' -type f 2>/dev/null
```

根据提示，我找到了 pgadmin4 下的所有可能有用的文件，直接查看了. db 数据库文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYg0MSXezgSuTI9bY3XHj9nfdypPoG4LHWk6h6yLQwRFge84EcbXvJ2Q/640?wx_fmt=png)

sqlite 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYfr7AaXa8bAlG9YoYs3kRYMdVMpftKDuO5MII73y26NF0g3O4icZp2eA/640?wx_fmt=png)

```
sqlitebrowser pgadmin4.db
```

下载到本地，利用 sqlitebrowser 查看了内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYrrRQia1FbnORRUl1HyteNevZcGTgh5q77VFTmxibQsFzhengcxfKuA3w/640?wx_fmt=png)

在最下面有 user 目录... 进入后发现了 bob 用户的密码... 根据提示，这就是 root 密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYnJGsQ8X2KXtKgSkoEmVMmx0AYQ2WBv2iax0q1bWRIUB2R6vdxKSPQww/640?wx_fmt=png)

在枚举信息中，找到了 crypto.py 脚本... 这是破解密码的关键

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYEtmy1WSFTBnPZ5DHWYwPvBiapYVNWchvIysXibOq0IbCL8phniaNH6ocA/640?wx_fmt=png)

该脚本内容，可以利用转换获得 bob 的密码信息... 接手密文和密匙，解密等...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYwAZUlpnJKSIkTHLIUVGZDQe0qMlWnSxX4oBuGIbULVX9U45L79Fo9A/640?wx_fmt=png)

```
sqlite3 pgadmin4.db "select * from server"
```

现在有了 dba 哈希和 bob 哈希，可以使用解密函数脚本对其进行解密...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYOLucZiaXlv5ZW9pJvCYpvADvrLU3Iyue564yVNr50DZcQkS5Lbv7z6g/640?wx_fmt=png)

通过脚本提示利用 dba 和 bob hash 获得了 bob 的登陆密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNKQQxdiaicicmAsxfeeba8rwYRjyAIlO6UzVz1PLicvGH01Fajsv7uphC9DhK8UnJM6Pz8DCXcOHxd3g/640?wx_fmt=png)

bob 的登陆密码就是 root 登陆密码...

su 获得了 root 权限，并获得了 root_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_gif/vlvamJrTPeG5nET2PXlWHKQ3vLE8qBnoicLE2Rob1c9IwHp17PmKusuaFIP9exOic3G6SRppL4GWWhjhyJnXQg5A/640?wx_fmt=gif)

这台靶机挺难的，也复习了以前的技术...

sql 命令注入 --openssl 创建客户端凭证 --showmount 挂载技术 -- 利用 ssh-keygen 创建密匙 -- 最后的密码破译...

最后一步说实话，我也很难做出来... 我是查看了大量文件，通过理解，才抄近道理解了并做了出来...

自个琢磨估计要好多天..

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台高级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/C4gxftskfhPHbgia3ShTwT8zUkJK7U8wCNeRmXOiac3SZ7W7uxhJgtdPP455e48IGjk8jcgkTcg9outvozseH3Wg/640?wx_fmt=png)

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