> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.bylibrary.cn](https://www.bylibrary.cn/%E6%BC%8F%E6%B4%9E%E5%BA%93/01-CMS%E6%BC%8F%E6%B4%9E/DedeCMS/DedeCMS_v5.7_carbuyaction_%E5%AD%98%E5%82%A8%E5%9E%8BXSS/)

> 白阁文库是白泽 Sec 团队维护的一个漏洞 POC 和 EXP 披露以及漏洞复现的开源项目，欢迎各位白帽子访问白阁文库并提出宝贵建议。

[](https://github.com/BaizeSec/bylibrary/blob/main/docs/%E6%BC%8F%E6%B4%9E%E5%BA%93/01-CMS%E6%BC%8F%E6%B4%9E/DedeCMS/DedeCMS_v5.7_carbuyaction_%E5%AD%98%E5%82%A8%E5%9E%8BXSS.md "编辑此页")

Affected Version[¶](#affected-version "Permanent link")
-------------------------------------------------------

DedeCMS-V5.7-UTF8-SP2 （ 发布日期 2017-03-15 ）

需要站点启用商城功能。

下载地址： 链接: [https://pan.baidu.com/s/1bprjPx1](https://pan.baidu.com/s/1bprjPx1) 密码: mwdq

PoC[¶](#poc "Permanent link")
-----------------------------

该漏洞 通过用户在编写订单收货地址的相关参数 注入 XSS Payload，导致 前台查看订单的页面和后台管理员查看订单详情的页面都会被 XSS。

所以说，可以用来打管理员 Cookie 。

测试：

1.  首先管理员添加一项商城的商品

![](https://www.bylibrary.cn/%E6%BC%8F%E6%B4%9E%E5%BA%93/01-CMS%E6%BC%8F%E6%B4%9E/DedeCMS/DedeCMS_v5.7_carbuyaction_%E5%AD%98%E5%82%A8%E5%9E%8BXSS/add_good.png)

1.  前台用户选定商品添加购物车

![](https://www.bylibrary.cn/%E6%BC%8F%E6%B4%9E%E5%BA%93/01-CMS%E6%BC%8F%E6%B4%9E/DedeCMS/DedeCMS_v5.7_carbuyaction_%E5%AD%98%E5%82%A8%E5%9E%8BXSS/add_shopcar.png)

1.  前台用户编辑订单的收货地址，在这里 address,des,email,postname 都是存在 XSS 的，插入 XSS Payload

![](https://www.bylibrary.cn/%E6%BC%8F%E6%B4%9E%E5%BA%93/01-CMS%E6%BC%8F%E6%B4%9E/DedeCMS/DedeCMS_v5.7_carbuyaction_%E5%AD%98%E5%82%A8%E5%9E%8BXSS/edit_address.png)

1.  查看订单详情发现前台已经被 XSS

![](https://www.bylibrary.cn/%E6%BC%8F%E6%B4%9E%E5%BA%93/01-CMS%E6%BC%8F%E6%B4%9E/DedeCMS/DedeCMS_v5.7_carbuyaction_%E5%AD%98%E5%82%A8%E5%9E%8BXSS/xssed.png)

1.  管理员进入后台查看商城订单同样也会被 XSS :p

![](https://www.bylibrary.cn/%E6%BC%8F%E6%B4%9E%E5%BA%93/01-CMS%E6%BC%8F%E6%B4%9E/DedeCMS/DedeCMS_v5.7_carbuyaction_%E5%AD%98%E5%82%A8%E5%9E%8BXSS/back_xssed.png)

References[¶](#references "Permanent link")
-------------------------------------------

1.  [https://www.seebug.org/vuldb/ssvid-92855](https://www.seebug.org/vuldb/ssvid-92855)

* * *

最后更新: 2021-03-24