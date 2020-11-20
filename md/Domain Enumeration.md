\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/TuNGxV0M15foJw49xRAXyw)

  总结一些域枚举的艺术，希望能对大家有用，文中用到的工具为 powerview 与 powershell AD 模块。全文共 41 张图，阅读时间约为 10-15 分钟。

域的查看可以使用下面的 powershell 去进行查看

```
$ADClass = \[System.DirectoryServices.ActiveDirectory.Domain\] 
$ADClass::GetCurrentDomain()
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZuDYpYPW1umIsAqvoicVg9R3icCveUUkDszViaf68HlicaUicramhYv3RJjQ/640?wx_fmt=png)

一句话操作

```
powershell "$ADClass = \[System.DirectoryServices.ActiveDirectory.Domain\];$ADClass::GetComputerDomain()"
```

详细的操作可以使用 PowerSploit 中的 PowerView 进行操作，如果缺少 AD powershell 模块，可以去 msdn 前去下载 (github ADMoudle)。

查看当前域的信息，可以使用下面的命令

```
Get-NetDomain --> powerview 
Get-ADDomain --> ADMoudle
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZibIOGmtWlibMFawJKCEjiaic5uCI8uoRchL6n3lQ9ugcv8Xem3WIFTNI0g/640?wx_fmt=png)

查看域对象信息

```
Get-NetDomain -Domain Domain Name --> powerview 
Get-ADDomain -Identity Domain Name --> ADMoudle
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZhm41fQkEH8c2zVCOfDhfmC4rTrY1tZFicgH4lR7QRh5gaJsxxeeb9JA/640?wx_fmt=png)

查看域的 SID

```
Get-DomainSID --> powerview 
(Get-ADDomain).DomainSID --> ADMoudle
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZmIQkndLeo0JSicF4z6tvMiblmHb8yveuvdLw00mTD2LOUQUMLsOMtDLg/640?wx_fmt=png)

查看组策略

```
Get-DomainPolicy 
(Get-DomainPolicy)."systemaccess" 
(Get-DomainPolicy)."kerberospolicy"
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZLdpbG4W38L28h2sDiakgI4GEb8N8FrNORhrEnuCTG6uCfgPgEKd812w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZnYMZ6wjk3ukK3WjqIOYYfKPBP5NlLGrC3ystk2NnyiccuKu5aRRCsiaQ/640?wx_fmt=png)

查看域控制器

```
Get-NetDomainController
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZHX3fBzPwFw51e6hyx4Gzh08BBKtAH13bQU3GdvWhXViasV14GPXThgA/640?wx_fmt=png)

```
Get-ADDomainController
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZ18c3fbZMKg8Y85jQBeibcQ6T6cPcfPTbts3Fr3Y82yKwENnym6qV2IQ/640?wx_fmt=png)

查看域内的用户

```
Get-NetUser
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZhUiaXSyZrOdDdbDDlSibhrvhxxpbnzbfO5BVT6hGxKhvgGibpwIhC2eeg/640?wx_fmt=png)

```
Get-ADUser -Filter \* -Properties \*
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZOduBbfeJIbiacz1MrbAnTcOmmiccGh4oJ0qOkSo7uqDWdRnoSOZICAqg/640?wx_fmt=png)

查看用户信息

```
Get-UserProperty
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZyfJKiaCrDw0Hm3Q0dIIaqGZkC0ZBPGzicsFKnJsVcb3qaRO4HMLdm6gQ/640?wx_fmt=png)

这里就包含了所有用户相关信息。可以使用 -Properties 查看具体的某一项，比如查看最后的密码设置时间。

```
Get-UserProperty -Properties pwdlastset
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZ79z3Fq1ibRc4orgwDd3cZFmqPfAHXZUlraicqJ2LN50LJj834VGSXg5A/640?wx_fmt=png)

枚举计算机信息

```
powerview

Get-NetComputer Get-NetComputer -OperatingSystem "\*2012\*" //系统为2012 
Get-NetComputer -Ping //ping操作 
Get-NetComputer -FullData //详细数据
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZicTSfcq5pmB93hX5fNaDKwwZfKSz3xNJMMflwM7xJ45LiccKJLlssfzA/640?wx_fmt=png)

```
AD模块

Get-ADComputer -Filter \* 
Get-ADComputer -Filter \* -Properties \*
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZC5lRhF68IwL8E0T9Eo6mYZT5mJcibDDpX2yb54O0xhRkjc0CaYhQNww/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZuyFjsAatHJSAONvxpQQtFwjJl5VaRFzvbCdNNcrUoBxib549oQJW8tQ/640?wx_fmt=png)

获取组信息

```
Get-NetGroup 
Get-NetGroup -Domain contoso.com
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZgrsU43JE2Zo6TokoTAxNSmTP1K2LC7V0WQtQsCSGcgTSddgEuF0jtQ/640?wx_fmt=png)

```
Get-ADGroup -Filter \*
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZrGNGucHC9HH93MicB0pxUgic6jQgfPHJ8NvO68bakkdX3KupicdZCVZhw/640?wx_fmt=png)

查看组内成员

```
Get-NetGroupMember -GroupName "Domain Admins" -Recurse
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZVde8Xib5UJorPDevmiaicgj14gBevMwLKwggicbcChqAD7BsfXOiah00Ptw/640?wx_fmt=png)

```
Get-ADGroupMember -Identity "Domain Admins" -Recursive
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZ7CCu205EvCPiamuPmqkpnbFpeXCOw2bxJJjCM3ibgJRwXzAPzyugpIgQ/640?wx_fmt=png)

查看一个用户所属的组

```
Get-NetGroup -UserName "bypass" 
Get-ADPrincipalGroupMembership -Identity bypass
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZ9fJCxjLHeiaAPFh7sqk2Od9VYFicxPCjE3R8Fme0wKNaXoENXa9xVlng/640?wx_fmt=png)

列出指定机器的本地组 (需要管理员权限)

```
Get-NetLocalGroup -ComputerName WIN-2TRELPSBMUD.contoso.com -ListGroups
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZ9X8By43HahrSvDicdOGD4KB8JVuZ8JMibXTtoFRZU4xZlZzMNQbSGVMQ/640?wx_fmt=png)

查看指定机器的登录活动信息 (需要目标的本地管理权限)

```
 Get-NetLoggedon -ComputerName WIN-2TRELPSBMUD.contoso.com 
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZ5hAcdALXvchkumAkK4WVah3WGJzyhO2BwCtH9icjTxDZsTDG4kwUUlw/640?wx_fmt=png)

查看当前域的共享信息

```
Invoke-ShareFinder -Verbose
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZkHBlnQboT6Albhxpdw6TKeaZEUxdu17Ckk328HQaSdHWkALAKVibkiaQ/640?wx_fmt=png)

查看当前域的敏感文件

```
Invoke-FileFinder -Verbose
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZyhP4gX688iauYuWk3p0dCK2ahrOOK4gwTYq0sIAIt4U7cSdDYSibFnRA/640?wx_fmt=png)

GPO 相关

```
Get-NetGPO
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZUrnUnVmKxafR128Fv9kPcLG5ODoqPeYFeX13KpQ6JAMjMicac4obAIQ/640?wx_fmt=png)

```
Get-GPO -All //使用GPO模块
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZtvkTAxWYKXcDddjeGLQuicDibOSfZbiaqqFMT3wxzxKnAcm3BzH4Kp1kw/640?wx_fmt=png)

将 GPO 导出成 html

```
PS C:\\Users\\Administrator\\Desktop> Get-GPResultantSetOfPolicy -ReportType Html -Path C:\\Users\\Administrator\\Desktop\\repo rt.html
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZj7FsQFbic6gNpZDt8lKSXNPDicPwjTC1VG7wUKNbDj8Q9EiciaiarBLyARA/640?wx_fmt=png)

gpo 信息查看

```
Find-GPOComputerAdmin -ComputerName WIN-2TRELPSBMUD.contoso.com 
Find-GPOLocation -UserName bypass
```

查看容器信息

```
Get-NetOU -FullData
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZjkib4OoYDHrQvOUvDibhfUELKu6ukLrKIAIQrpaxZRodSMWcw4BGM9iaw/640?wx_fmt=png)

```
Get-ADOrganizationalUnit -Filter \* -Properties \*
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZR4rtFqncVUnCic3Z6HUibCV9Dg1DwzseicApgxWmgicMqSn9rMPduBQDGA/640?wx_fmt=png)

查看指定对象的 ACL

```
Get-ObjectAcl -SamAccountName bypass -ResolveGUIDs
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZ2dIaqJVyJkNdia4BLIr0DLHqQJCCDcS8Xq20EpuiaWR3icCzqOocC2EJQ/640?wx_fmt=png)

查找指定前缀对象的 ACL

```
Get-ObjectAcl -ADSprefix 'CN=administrator,CN=users' -Verbose
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZxoq3J1ibwKicRsVabYPhibKx4Fh0ULeyd4hdJc5r9icWdXB0oKNeykS7yQ/640?wx_fmt=png)

使用自带的 AD 模块来枚举 ACL

```
(Get-ACL 'AD:\\cn=administrator,cn=users,dc=contoso,dc=com').access
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZCMSNN9zdzv23E238QeicBYurW831InbWJm29uuriaNn751ImbBgMTddg/640?wx_fmt=png)

查找有趣的 ACE

```
Invoke-ACLScanner -ResolveGUIDs
```

查看指定路径的 ACL

```
Get-PathAcl -Path "C:\\Users"
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZ09B9vNEG6uJ6icX5xqOmFbasttdF86hecPicHk7iaMFrBGmv3IvQ3zOTA/640?wx_fmt=png)

域信任

获取域信任

```
Get-NetDomainTrust
```

获取当前林信息

```
Get-NetForest
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZYOricxKszNGN2v9pXxcGA8F1JqhCfub51lgdHEces1lrOeLWZDGmicqQ/640?wx_fmt=png)

```
Get-ADForest
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZdclmRFicjnSKyLp9TWbqrxvj1cygcFGFxU9o7wfeR2KjgSeYRicvOsew/640?wx_fmt=png)

获取当前林的所有域

```
Get-NetForestDomain
(Get-ADForest).Domains
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZXIsdWbEsLGmLaHHJHJS8ibU3sAIJtFmib2c9qDDibrxuY43aiavZlUWyicA/640?wx_fmt=png)

获取当前林的全局编录

```
Get-NetForestCatalog
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZYia4Mrg4sQI1riaZDNYPrVI8JwvdaZQN8waqOtrup7V73NxiaYzibz5h1w/640?wx_fmt=png)

user hunting

查找当前用户可作为管理员进行登录的域内机器

```
Find-LocalAdminAccess -Verbose
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZKB5f5djW9WfcfM7cviab59NRiaN0UibiaQrNvO3c3Dk9pqhicX0uBZ8hIhg/640?wx_fmt=png)

攻击利用链如下：

```
Get-NetComputer --> Invoke-CheckLocalAdminAccess
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZZHsCBAenAhbbya3ccs1ysWpJhLnZRbMOlxpAa4kSmxrdxcpicfStgibA/640?wx_fmt=png)

注：具有同样功能的还有 Find-WMILocalAdminAcccess.ps1

查找域内所有机器的本地管理

```
Invoke-EnumerateLocalAdmin -Verbose
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZEQEMOUiajvQo9iaqtKy5xET3GlzudyRX7K1brCswU82pH5Go0H3DPshA/640?wx_fmt=png)

查找用户 session

```
Invoke-UserHunter 
Get-NetSession 
Get-NetLoggedon
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08U5s2jicY9C9S1ghzlpgEDTZQthaicSrnaibgd9cjUomCiaRw0ObPJBFphuxicybJI4gyrdhCHGytxscSA/640?wx_fmt=png)

**以上便是总结的一些域枚举的手法，如有错误，还望指出以免误人子弟，如有帮助，希望点个转发，点个再看。**

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)