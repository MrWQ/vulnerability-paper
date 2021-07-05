> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/H9ue_ghi15L0g6_uALP1Mg)

**文章源自【字节脉搏社区】- 字节脉搏实验室**

**作者 - K.Fire** 

**扫描下方二维码进入社区：**

**![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK3Fc7MgHHCICGGSg2l58vxaP5QwOCBcU48xz5g8pgSjGds3Oax0BfzyLkzE9Z6J4WARvaN6ic0GRQ/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLiaUtskPUd2Ks1HsanFjaibzGKRXs9CZLaIGic1WQjXs7UQ80m5RcGpRE5iaPhLBNdnrH5KHfqAJyemQ/640?wx_fmt=png)

> 在不少的攻防演练中，许多人都会使用 CDN 来隐藏真实的主机地址来防止溯源，需要攻击者自行购买带有公网 IP 的主机以及域名，一旦被发现真实 IP 地址和域名并被类似微步这样的威胁情报标记，就不得不放弃使用该主机以及域名，造成资源浪费。以下内容将演示零成本隐藏 CobaltStrike 主机，仅供技术研究与授权测试，请勿用于非法用途。

演示环境
====

*   Kali-Linux-2021.2
    
*   Windows 10 专业版 21H1（靶机）
    

工具清单
====

*   cloudflared（基于 cloudflare 的内网穿透工具）
    
*   ding（基于钉钉的内网穿透工具）
    
*   cobaltstrike 4.3
    

运行 teamserver
=============

```
./cloudflared tunnel --url http://127.0.0.1:44444
```

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLiaUtskPUd2Ks1HsanFjaibzXQxpyibfXZzALhD86icKg9Er2k1mkGuvicCkvAjfvwiar1MjKx5gNiaFtoA/640?wx_fmt=png)

ding
----

<pre andale=""mono",="""ubuntu="" monospace;=""word-spacing:="" normal;=""word-break:="" overflow-wrap:=""line-height:="" 1.5;=""tab-size:="" 4;=""hyphens:="" none;"="">./ding -config=./ding.cfg -subdomain=kfire 44444

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLiaUtskPUd2Ks1HsanFjaibzaZxh2QZKDxP7n6wAkFZYeu7hiaKtnOVK9kp8DaE2fxG8k26YdIjQHxQ/640?wx_fmt=png)

配置监听器
=====

> 接下来的内容以 cloudflared 为例，使用 ding 大同小异。

1.  获取 CDN 使用的 IP  
    ![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLiaUtskPUd2Ks1HsanFjaibzvdiaASSA257uuHkGj1jjVObn5bg6kWpM4au1lLmuXwa5Ajh80PuPiamA/640?wx_fmt=png)
    
2.  配置监听器  
    ![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLiaUtskPUd2Ks1HsanFjaibzZqtpFPvZ6pZuxmcx0ibyTmU4DUg1pBibicibterhiaUhpTH742a64lh3ibZg/640?wx_fmt=png)
    

测试上线
====

1.  生成后门  
    ![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLiaUtskPUd2Ks1HsanFjaibzON4L0aEUhKBsMdZEJB0pDYFfXjBUibib5cmjIianRqEyCB07WOicTcOkBw/640?wx_fmt=png)
    
2.  上线成功  
    ![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLiaUtskPUd2Ks1HsanFjaibziaKPHIm9Ntb9wLuEyCPn8P9ZicDBS8OAall4KiaHPn51SKdQUeEibdv1aQ/640?wx_fmt=png)
    

主机隐藏测试
======

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLiaUtskPUd2Ks1HsanFjaibzlJUf4MU0ZcTVtC4V9e2tvofhRcvAB7Qr24bWDQfiaxic7naAg601McIQ/640?wx_fmt=png)  
通过微步云沙箱检测，完美的隐藏了 CS 主机的真实 IP。

**通知！**

**公众号招募文章投稿小伙伴啦！只要你有技术有想法要分享给更多的朋友，就可以参与到我们的投稿计划当中哦~ 感兴趣的朋友公众号首页菜单栏点击【商务合作 - 我要投稿】即可。期待大家的参与~**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/ia3Is12pQKnKRau1qLYtgUZw8e6ENhD9UWdh6lUJoISP3XJ6tiaibXMsibwDn9tac07e0g9X5Q6xEuNUcSqmZtNOYQ/640?wx_fmt=jpeg)**

**记得扫码**

**关注我**