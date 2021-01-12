> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/25ncF8PuXh4Aob49TPFfbw)

**https://www.secquan.org/BugWarning/1071470**

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkJbH7OvXcj5aG3mibfyicthqUIxtCP8zz52rjcRv1fVj9gymtVAESLJRw/640?wx_fmt=png)**

**1. 环境搭建**
===========

**Windows Server 2012 R2 X64**
------------------------------

**范围：宝塔 Windows <= 6.5    或 liunx 只要有 IIS8.5 这个中间件的版本**
-------------------------------------------------------

**宝塔选择：MySQL + PHP-5.4+ IIS 8.5**
---------------------------------

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkJdia19VibNO9XyXjU53s7RtHUUfnpH3BicORXPH3aOF5Xaf0VX4Nr9Ldw/640?wx_fmt=png)**

**源码使用公开的 PHP 上传源码:**
=====================

**https://www.runoob.com/wp-content/uploads/2013/08/runoob-file-uplaod-demo.zip**
---------------------------------------------------------------------------------

**已做白名单限制，仅允许上传 .gif、.jpeg、.jpg、.png 文件，文件大小必须小于 200 kB**
---------------------------------------------------------

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkHlS1cJbsxfTpZelJDaT4EBBLBBaeAiaVlE8Zysn08ibFlUyA312U1ApA/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkz8X5jOicuaaLUguRnAaGpo64ib9qpicOemQQmwD4P7G0kaAicjXKWYic4Lg/640?wx_fmt=png)**

**2. 漏洞复现**
===========

**配置好网站以后：**
------------

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOk9qb7iasKZMaq0o4pCPuATicNiaiaaPib59tvB4RfEicWrnP9DMxXIaXMkjrA/640?wx_fmt=png)**

**本地写一个**
---------

**<?php  
phpinfo();**

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkIBLjFD9WzWTbdic1rrVRATOUEcQ2fGyN38AvibA6lFuR5Lk8IDlLal0A/640?wx_fmt=png)**

**另存为. jpg 格式**
---------------

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkXGCWia1ibWlpexfQp4ico6Bn0NfJqLLEaInsA2gxHmHa0SvnHtic4x79TQ/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkt7JToPtnfOqlRkucBx9VmHzdeZPVRuS1D6SBjlt6OfgwU2ZZ1I5H3A/640?wx_fmt=png)**

**直接上传文件，不需要做任何修改：**
--------------------

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkFp3WSMqmu0mS8cJ2qeBPWHmkzaZUvrXdW11Wgj2iaF9QDTP2otXa8tQ/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkRO1gicQWp7xT8cGRibF296EUEbibpxQD1IrIYfDN1X32niaVEEuehZckQA/640?wx_fmt=png)**

**访问上传文件地址：**
-------------

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkJSz26EsNibrWH1yNjS1OicGsmth34QCO2KXbib7IouNEEA82QjLO1TzrA/640?wx_fmt=png)**

**在 upload/1.jpg 后面加 /.php**
----------------------------

**![](https://mmbiz.qpic.cn/mmbiz_png/ORwL8p4cVxRNGJLVK7DFg6MGr6diahKOkRKnjRXh0soVnONNdsYqGN2FZwHoa5eBuXhqmp0ajhvAx4hKsWnBfibg/640?wx_fmt=png)**

**成功验证存在任意文件上传漏洞！**
-------------------

**（特此声明，本篇文章为原创文章！如要转载请标明来源！）**

![](https://mmbiz.qpic.cn/mmbiz_jpg/ORwL8p4cVxSlLTvUjLjuQUR6y6W6pLDulwBQClNzPtc9iayZO0lVTJHM8flTL0SKTbx3mLaTbzjUWMc8EFFsLFA/640?wx_fmt=jpeg)

  

  

扫码关注不迷路

简历请投递 admin@360bug.net

开普勒安全团队欢迎你

‍