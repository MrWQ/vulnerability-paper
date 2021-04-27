> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247484705&idx=1&sn=d621a0f668be59c9473ec66f2e0f8b98&chksm=eaad851cddda0c0a5a618e1f1907bbd59acaee7b2b454496e98fbd200ab1ea832f2d3f288d59&scene=21#wechat_redirect)

**目录**

                     

Set

钓鱼攻击

网站克隆

**Set**(Social engineering tookit) 是一款社会工程学工具，该工具用的最多的就是用来制作钓鱼网站。  

Kali 中自带了该工具。

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HzZrTT4UZAcukC3cKqetSHpGJABL8ZCM8yibLyNpvY2Zia3IAY3P6yE9A/640?wx_fmt=gif)

钓鱼攻击

在应用程序中的漏洞利用工具集里面。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29CricE3fmQnH4JiaNQxsQXo2icicxQxOUkm6ZNShBW7mROFxibiaPichoEHJPw/640?wx_fmt=png)

打开之后，我们看到了如下的界面。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29rB0btH1m42emCuf0XNlic6DqyNom30SUibuAbFPVCTpsnGbicicLeYAJzg/640?wx_fmt=png)

1) 社会工程学攻击

2) 快速追踪测试

3) 第三方模块

4) 升级软件

5) 升级配置

6) 帮助

99) 退出

 我们利用它来制作钓鱼网站，选择 1 社会工程学攻击 ，然后又跳出了下面的选择

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29IO3YLnQIC3shqgaJanLjFGNTGc5bjdE30tZTaLqJVuTMjs0G0vpw3w/640?wx_fmt=png)

1) 鱼叉式网络钓鱼攻击

2) 网页攻击

3) 传染媒介式（俗称木马）

4) 建立 payloaad 和 listener

5) 邮件群发攻击（夹杂木马啊 payload 的玩意发给你）

6)Arduino 基础攻击

7) 无线接入点攻击

8) 二维码攻击

9)Powershell 攻击

10) 第三反模块

99) 返回上级

我们选择 2 网页攻击 ，然后又跳出了下面的选择

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29bS4eR3EYGIRZ5uLJNss5oTeMAu2xBt1ias3kzU9iaic5YLSrK3JG1k8sg/640?wx_fmt=png)

1)java applet 攻击（网页弹窗那种）

2)Metasploit 浏览器漏洞攻击

3) 钓鱼网站攻击

4) 标签钓鱼攻击

5) 网站 jacking 攻击（这个真心不明白，好像也和 java 的攻击方式有些相同）

6) 多种网站攻击方式

7) 全屏幕攻击（不明所以的玩意，只能够对谷歌邮箱和脸书用）

8)HTA 攻击方式

99) 返回主按钮

 我们选择 3 钓鱼网站攻击，然后跳出来下面的选择

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29RYAp1ib4ubKMbUv0IwTTt0SWWuD6MQt60HZ7Dgqq3IAZFyToZ7kqZJg/640?wx_fmt=png)

1）网站模版

2）设置克隆网站

3）导入自己的网站

99）返回到上一级

如果我们选择 1 网站模板的话，会提示我们输入 POST 返回的地址，我们输入自己主机的地址，然后会叫我们选择网站的模板，我们选择 2 google

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29iaTpJbeicPib3LDxSicAQeOTjp5o4OBibED5v5VibPBboIEx480icnL7An5DA/640?wx_fmt=png)

然后我们访问该主机，和谷歌的页面一模一样，如果我们输入用户名和密码登录的话，

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29Y28FwDxvI7yJUbjd6hmoU3KPZ8gbPMGgeiaryz7jiaMJQb7BplGYpYZQ/640?wx_fmt=png)

我们就会收到用户输入的用户名和密码，这样就完成了一次钓鱼网站攻击了

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29w7Jic6AzjlFwHc2jQHsNic2jp61Mx72VmuibGLm937Tb6dkic4ojUY8S3g/640?wx_fmt=png)

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HoaHEjBLqmAGrZlH8BTIAaGKt4xLxqt7gEL9Jj00Y7u9ic8Xy6EYiaVBQ/640?wx_fmt=gif)

网站克隆

网站模板只有几个网站的模板，不能满足我们的需求。于是，在上一步我们可以选择克隆网站。这个克隆网站的要求就是最好是静态页面而且有 POST 返回的登录界面，现在的百度、QQ、163 对于都克隆没用了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29Av3dMpibgEyhl3XQ3C8YvoxLvDiazxbKH2ECwBrZjxvPWSvnbDfNZXyA/640?wx_fmt=png)

访问网站，和百度页面一模一样，不过这并不能获取到用户输入的用户名和密码，只是外观一模一样

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29R7DfzwQRPPGJJrbes7ZHZ8jlNa15wvVTAywEqXycajHmNOIe0XyBzg/640?wx_fmt=png)

  

  

                           

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvAKOaVnz60hOe7y3wAHiclddyK53lpEKIQlx4DKOq6EojHibVicgibDB2aQ/640?wx_fmt=gif)

来源：谢公子的博客

责编：浮夸

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)