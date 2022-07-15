> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/SOD_aGWtqwsHS6AuI8nNsg)

公众号

### 前言  

本篇介绍几款优秀的 Windows 上的密码抓取工具，每个工具都有自己的特点非常实用，欢迎补充。

### 0x01 Mimikatz

> 个人点评：这款工具非常强大，公认的 Windows 密码神器。

#### 1. 简介

Mimikat 是一个法国人写的轻量级调试器。Mimikat 可以从内存中提取纯文本密码，hash，PIN 码和 kerberos 票证。mimikatz 还可以执行哈希传递，票证传递或构建 Golden 票证

项目地址：https://github.com/gentilkiwi/mimikatz/

#### 2. 使用

cmd 运行命令如下：

```
mimikatz.exe # cmd命令执行启动程序privilege::debug # 提升权限sekurlsa::logonpasswords # 抓取密码
```

> Mimikatz 功能非常强大，这里只简单介绍了常用的抓取密码命令。

### 0x02 BrowserGhost

> 个人点评：这款工具的亮点就是可以不用输入 windows 系统密码，直接提取谷歌浏览器中存储的密码。

#### 1. 简介

这是一个抓取浏览器密码的工具，后续会添加更多功能，已经完成的功能如下：

*   实现 system 抓机器上其他用户的浏览器密码 (方便横向移动时快速凭据采集)
    
*   用. net2 实现可兼容大部分 windows，并去掉依赖 (不需要 System.Data.SQLite.dll 这些累赘)
    
*   可以解密 chrome 全版本密码 (chrome80 版本后加密方式变了)
    
*   Chrome 已经可以获取 login data、cookie、history、book 了
    
*   IE 支持获取书签、密码、history 了 (.net2 提取密码太复杂了代码参考至 https://github.com/djhohnstein/SharpWeb/raw/master/Edge/SharpEdge.cs)
    

项目地址：https://github.com/QAX-A-Team/BrowserGhost

#### 2. 使用

cmd 运行如下命令：

```
BrowserGhost.exe
```

### 0x03 SharpDecryptPwd

> 个人点评：这款工具的亮点是可以提取一些 windows 上常用的第三方程序进行解析提取存储的密码。

#### 1. 简介

对密码已保存在 Windwos 系统上的部分程序进行解析, 包括：Navicat,TeamViewer,FileZilla,WinSCP,Xmangager 系列产品（Xshell,Xftp)。

项目地址：https://github.com/uknowsec/SharpDecryptPwd

#### 2. 使用

cmd 运行如下命令：

```
SharpDecryptPwd.exe
SharpDecryptPwd.exe -TeamViewer
SharpDecryptPwd.exe -NavicatCrypto
SharpDecryptPwd.exe -FileZilla
SharpDecryptPwd.exe -Xmangager -p D:\xshell\Xshell\Sessions

# Cobalt Strike
execute-assembly /path/to/SharpDecryptPwd.exe
```

### 0x04 LaZagne

> 个人点评：这款工具可以一键抓取本地计算机上的所有明文密码，可获取的软件密码种类非常多，支持 Windows、Linux、Mac。

#### 1. 简介

LaZagne 是用于开源应用程序获取大量的密码存储在本地计算机上。每个软件使用不同的技术（纯文本，API，自定义算法，数据库等）存储其密码。开发该工具的目的是为最常用的软件找到这些密码。该项目已作为开发后模块添加到 pupy 中。Python 代码将在内存中解释而无需接触磁盘，并且可以在 Windows 和 Linux 主机上运行。

项目地址：https://github.com/AlessandroZ/LaZagne

#### 2. 使用

安装依赖库

```
pip3 install -r requirements.txt
```

一键获取所有支持的类型密码

```
python3 lazagne.py all
```

支持的类型密码如下：

<table><thead><tr><th width="NaN">类型</th><th width="22">Windows</th><th width="85.33333333333333">Linux</th><th width="25">Mac</th></tr></thead><tbody><tr><td width="NaN">Browsers</td><td width="NaN">7Star,Amigo,BlackHawk,Brave,Centbrowser,Chedot,Chrome Canary,Chromium,Coccoc,Comodo Dragon,Comodo IceDragon,Cyberfox,Elements Browser,Epic Privacy Browser,Firefox,Google Chrome,Icecat,K-Meleon,Kometa,Opera,Orbitum,Sputnik,TorchUran,Vivaldi</td><td width="78.33333333333333">Brave,Chromium,Dissenter-Browser,Google Chrome,IceCat,Firefox,Opera,SlimJet,Vivaldi,WaterFox</td><td width="25">Chrome,Firefox</td></tr><tr><td width="NaN">Chats</td><td width="NaN">Pidgin,Psi,Skype</td><td width="78.33333333333333">Pidgin,Psi</td><td width="25"><br></td></tr><tr><td width="NaN">Databases</td><td width="NaN">DBVisualizer,Postgresql,Robomongo,Squirrel,SQLdevelopper</td><td width="78.33333333333333">DBVisualizer,Squirrel,SQLdevelopper</td><td width="25"><br></td></tr><tr><td width="NaN">Games</td><td width="NaN">GalconFusion,Kalypsomedia,RogueTale,Turba</td><td width="78.33333333333333"><br></td><td width="25"><br></td></tr><tr><td width="NaN">Git</td><td width="NaN">Git for Windows</td><td width="78.33333333333333"><br></td><td width="25"><br></td></tr><tr><td width="NaN">Mails</td><td width="NaN">Outlook,Thunderbird</td><td width="78.33333333333333">Clawsmail,Thunderbird</td><td width="25"><br></td></tr><tr><td width="NaN">Maven</td><td width="NaN">Maven Apache</td><td width="78.33333333333333"><br></td><td width="25"><br></td></tr><tr><td width="NaN">Dumps from memory</td><td width="NaN">Keepass,Mimikatz method</td><td width="78.33333333333333">System Password</td><td width="25"><br></td></tr><tr><td width="NaN">Multimedia</td><td width="NaN">EyeCON</td><td width="78.33333333333333"><br></td><td width="25"><br></td></tr><tr><td width="NaN">PHP</td><td width="NaN">Composer</td><td width="78.33333333333333"><br></td><td width="25"><br></td></tr><tr><td width="NaN">SVN</td><td width="NaN">Tortoise</td><td width="78.33333333333333"><br></td><td width="25"><br></td></tr><tr><td width="NaN">Sysadmin</td><td width="NaN">Apache Directory Studio,CoreFTP,CyberDuck,FileZilla,FileZilla Server,FTPNavigator,OpenSSH,OpenVPN,KeePass Configuration Files (KeePass1, KeePass2),PuttyCM,RDPManager,VNC,WinSCP,</td><td width="78.33333333333333"><br></td><td width="25"><br></td></tr><tr><td width="NaN">Windows Subsystem for Linux</td><td width="NaN">Apache Directory Studio,AWS,Docker,Environnement variable,FileZilla,gFTP,History files,Shares,SSH private keys,KeePass Configuration Files (KeePassX, KeePass2),Grub</td><td width="78.33333333333333"><br></td><td width="25"><br></td></tr><tr><td width="NaN">Wifi</td><td width="NaN">Wireless Network</td><td width="78.33333333333333">Network Manager,WPA Supplicant</td><td width="25"><br></td></tr><tr><td width="NaN">Internal mechanism passwords storage</td><td width="NaN">Autologon,MSCache,Credential Files,Credman,DPAPI Hash,Hashdump (LM/NT),LSA secret,Vault Files</td><td width="78.33333333333333">GNOME Keyring,Kwallet,Hashdump</td><td width="25">Keychains,Hashdump</td></tr></tbody></table>

作者: Luckysec  
链接: http://luckyzmj.cn/posts/9686fbeb.html  
本文章著作权归作者所有，任何形式的转载都请注明出处。

**推荐阅读**[**![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyIDG0WicDG27ztM2s7iaVSWKiaPdxYic8tYjCatQzf9FicdZiar5r7f7OgcbY4jFaTTQ3HibkFZIWEzrsGg/640?wx_fmt=png)**](http://mp.weixin.qq.com/s?__biz=MzAwMjA5OTY5Ng==&mid=2247494811&idx=1&sn=23ec661f57424184e43ea216a8398c58&chksm=9acd3c04adbab512e2a1c40156b05a5dc40ea07dacf239a9041235324a563d555a4e4625e988&scene=21#wechat_redirect)

公众号

**觉得不错点个 **“赞”**、“在看”，支持下小编****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**