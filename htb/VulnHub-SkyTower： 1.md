> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/OIsgEawebB_3SRg6za_wTA)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **16** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/Hju2o35jBmTq6KFH2V0l2rpO9o6GicBiaYibgkMVJKERutggHic6HP3Cv9MbAmNwCsjW8knnZZgmA1yceegAFSN4OA/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/skytower-1,96/

靶机难度：中级（CTF）

靶机发布日期：2014 年 6 月 26 日

靶机描述：该 CTF 是由 Telspace Systems 在 ITWeb 安全峰会和 BSidesCPT（开普敦）上为 CTF 设计的。目的是测试中级到高级的安全爱好者使用多方面方法攻击系统并获得 “标志” 的能力。

目标：得到 root 权限 & 找到 flag.txt

![](https://mmbiz.qpic.cn/mmbiz_png/IhUDNJicR5NCFnPJhYUTqib6NmY4leia2t3Fs2QenHUiaZRPguibTFokOE3Lput5g5a5tTlkf5GagGpiaojrZrVtnXvA/640?wx_fmt=png)

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/D8K0hdvKJ0HXTG7lbicJpbKFahh3c1OHvyubVdcSpTNpsiam24fQnUoMlMTbT0NNSBSpicaCmf5nw7byndwJUpNJg/640?wx_fmt=png)

一、信息收集

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCQUzK3w3KibSZqCP2gKDfyVovnicwnclaibN07Vlj0icgaTpCsVQe3EfArQ/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：

```
192.168.56.101
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCgA8IvxHvVUkeDNUEe8eEmV78EjNZbL4GSsacqIHm3yDa2uscPJClibw/640?wx_fmt=png)

```
nmap -sS -sV -T5 -A -p- 192.168.56.101
```

开放了 22（filtered）、80、3128 代理端口... 盒子都有代理...

直接对 80 端口展开 web 渗透...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCFHzXk2xbvBVu46UJJTrXVEqiczmZiaS9OjpPuN35Esw18xrGasgQbbkg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnC9boYspuVs1LLh1rjMA7SDAcUgmEO960lwQyTUmwdicVndEAoVjWRiaibw/640?wx_fmt=png)

尝试用 admin 登录，失败...

这边用 bp 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCp8MuvfCUA8S3Eicszicm74ww2eIyCgncCUGl4h9VCJHmOm4pq8ek6PWg/640?wx_fmt=png)

把它发到 Repeater 继续分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCaC5DmyyVW7a4ZZrg3PqZn4Q1mIG0XB996icjazT6ibChibnd6oAE1Pmbw/640?wx_fmt=png)

加了一点，可以进行 sql 注入攻击

尝试看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCwZFGcYibqht2n5JiaJkNUHIibHohe5mM5ryUic095CDUmKvkZvkjAcuJAw/640?wx_fmt=png)

这边代码不行，将代码在本地用 sqlmap 注入攻击进行攻击

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCqxiaqmg81X3v54KaD3YVC8ibe04F3DS3cVZruUw7uXu8zldjW1PZfjNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCqxiaqmg81X3v54KaD3YVC8ibe04F3DS3cVZruUw7uXu8zldjW1PZfjNg/640?wx_fmt=png)

这边 sqlmap 让它慢慢扫，我们继续用 bp 来执行 sql 注入，这边先查看 Order by 注入方式...（不会的找资料学下 sql，看两遍就会了）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCk9f4QnHolCREzSw6OvLiaBE6Yw9aDrEZjshVfbYO1gOUbgGVTzFVd7g/640?wx_fmt=png)

发现'dey 这里 or 没有用？？？

继续测试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCc9LoS719SlLoa5G2tbbNI9rgewEVJVxxCy0eyxKibFceXAahkc10E1g/640?wx_fmt=png)

这里 OR 还是没效果... 在测试下，

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnC6QO8mp9ZZjjSqeEguJstYIOTJOu9jyfj1cicNas6uMzuLqn1j95yOFg/640?wx_fmt=png)

RR... 这边总结 or 注入不能用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCvUHTd0FibJzALrnf0DndUnElicOF3mot4gBgdJXxXIrAicwuQNgZ36ISQ/640?wx_fmt=png)

AND 也不行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCgCnXiapFicUQ4BRpM9Fic8KmfsDIAnxPUGBIUKibe5XIhmIO51bvxPUyOA/640?wx_fmt=png)

这边 || 1 #成功注入，看看信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnC5KHPtTsSRN3bRBkmoNwbsVk8l919icNfrmCUDjd0eREu6ZmMh196ahw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCgzCZcHrXaicj8C8qxaibFLhNCgYqAYiaqGHgjYktEIwDj5jZw08Wjfg7g/640?wx_fmt=png)

```
Username: john
Password: hereisjohn
```

前面 sqlmap 扫描就不分析了... 因为比较顺利发现了 john 用户密码... 稳，继续下去

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCfAfgib95DQgPfbyuMUlkck6Huewgc9g0GFK7ic0x03Gp9ibhyLMK6lQfA/640?wx_fmt=png)

尝试 ssh 登录 john 发现不行，回想 nmap 扫描出 ssh 是不可用的，但是开了代理，我这边使用代理访问 ssh 试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCPdpSw4kgYIhVCqFicOHTOyDrSBSWQWJGZrh1fibIy5qKHWhlShdevAlQ/640?wx_fmt=png)

```
proxytunnel -p 192.168.56.101:3128 -d 127.0.0.1:22 -a 6666
```

使用 proxytunnel 设置代理服务器隧道（-H 可以查看帮助）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCnx11RgQDjZe4q0AEx5PPGVN7URzGDZDV5coPwFI6kFnhyDzJASHTrA/640?wx_fmt=png)

正常访问，但是密码错误，回复：Funds have been withdrawn（已经提取了信息，可以理解已登录，但是登录失败）测试看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCv8LoSQia9WBFBQ8Nvic36g6wkSnibuzfjHPlWwzK4HLpayJicK5Ryao8xA/640?wx_fmt=png)

二、提权

通过代理 ssh 可以登录，但是进不去目录，但是可以通过命令查看 john 目录信息...！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCulLiaBmzoCt2XwAiaaLjj3UzialhP8dSJ8gibxriblcqEQuFfFsDC9U1tOQ/640?wx_fmt=png)

可以看到，我想修改他，但是 vi .bashrc 提示只可读不可写... 好吧，我 rm 删除它

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCp32abwicoRawiaiageWDmtACBk1oNk19VqAkxTAYbyeH46mAuWUbV2QIw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCZwUibAOqjg5iatpLbjuLYeXX4cg0ia4rLTrJViax5CvzG6hcF8MwVfcFzw/640?wx_fmt=png)

这边用 bin/bash 的注释

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCYl6zrVquo2f6THceN8OUUGo8XWAPPg86Y6jdNDtabue1ZaqYbO8tGA/640?wx_fmt=png)

成功登录，顺利！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnC1o1oe1B2EfS67enAEf6KTMn4hcfUX9sRXtv8n4WXiaXbYPpYD9QHicXA/640?wx_fmt=png)

Sorry, user john may not run sudo on SkyTower.

直接 sudo 提权... 提示不能提权，就知道没这么简单...

查看 mysql 根凭证，action 是一个参数传递给 login.php 处理，我来看看 login.php...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCZmOYx0qibA7gicZW3EH4vmpzeq7htN2ZQ0Cb5IkjtWoPGIQlxepqSCNw/640?wx_fmt=png)

发现 root、root 信息... 那么登录 mysql

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCNSfKJB0LQErV457xJgaWyRYyDzcIsFAGgqDK3ZTdhQ4bMHvVtDEvzw/640?wx_fmt=png)

列出数据库当前用户：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnC4yIFy1U8tfAYbBKvcb7DH4Jhe51U6Fx0Ff6Y2IqUxSyekll3bSjAZA/640?wx_fmt=png)

查看指定数据库中的所有表：login

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnC13W8tZad92qtZJg9cUxunZCFZ0zjNEicnNThjCWiceXxgRbZibDE2WU2A/640?wx_fmt=png)

```
|  1 | john@skytech.com    | hereisjohn   |
|  2 | sara@skytech.com    | ihatethisjob |
|  3 | william@skytech.com | senseable |
```

找到三组账号密码.... 尝试第二个

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCOX9CCqxbaAicuF8b4RRL6l4Hht3NAsTvh8Iykiclk0X25iaLib6ywTtsuQ/640?wx_fmt=png)

好吧，老问题... 循环后直接登录

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnC6EI8Z29DzyNn9X1ozcpsgcUVzKqE5wf0U5lHuOrjK34DLlibwzwMN8w/640?wx_fmt=png)

成功登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCPOQuD7jk3sPdgummoC765MSadopSSCPGUQEJib9Royf4gRibCNVefhTQ/640?wx_fmt=png)

这边也直接 sudo 提权试试，发现有方法可进入 root 用户！！！！

```
/bin/cat /accounts/*, (root) /bin/ls /accounts/*
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCVVqkltt3EsdEAN2lUbKx4ExtpWqrbHPnnl0h45p77hUIT0NRib22lAw/640?wx_fmt=png)

找到 accounts 目录查看用户信息... 发现有 root 用户信息，可读...cat 看他！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCL37sQ7k9NMAQIgVyZiaiaTmK7MjiceHoShmGlSjC6fmW0O4Fw84wXzrIg/640?wx_fmt=png)

用户 sara 具有对二进制文件的 sudo 访问权限 / bin/cat，使用路径遍历来查找其内容 / root/flag.txt 包含根密码的目录，这边成功查看到了 root 密码：theskytower

继续...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCjqRDvwNEylxh3ibhWZkianflnVEWJcW6LDrsyAVmVUAbm37ctiaBCaX6w/640?wx_fmt=png)

Congratz, have a cold one to celebrate!

root password is theskytower

这次靶机是 ITWeb 安全峰会和 BSidesCPT（开普敦）上为 CTF 设计的，主要学习到了 ssh 的运用、SQL 注入攻击的理解、mysql 的基础知识！！很好的一台靶机，大家也去试试吧！！

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/D8K0hdvKJ0HXTG7lbicJpbKFahh3c1OHvyubVdcSpTNpsiam24fQnUoMlMTbT0NNSBSpicaCmf5nw7byndwJUpNJg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)