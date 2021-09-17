> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/952xMUo_o0TAi4uK8_S6xg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **155** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/188

靶机难度：初级（4.2/10）

靶机发布日期：2019 年 6 月 17 日

靶机描述：

SwagShop is an easy difficulty linux box running an old version of Magento. The version is vulnerable to SQLi and RCE leading to a shell. The www user can use vim in the context of root which can abused to execute commands.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/pAKQibdZxLPFVjp9K5Pbx0gGWhXGIT5Y2ia1H4pSEP9CRUwCRRq8xl1ZxMiaeALB35QAJQce6DlTktLVBXhucFkQg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ZrqZaezpWclmao6Vp2LSrkuD0NTO9TiclXmiaWSh0NibqeKL1xJ4qBoJbPODkzJ3g0OvTdUGll3Otz9978tOYib32Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkicZhuo4PSHNkaAxyseTcCZu2RDwL0bYUic92Crlb5pxxnt5nP5ibyWpUQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.140...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkRqDhkXAG3YwFJPRhkGbYfgQ02w2gByJ3iblalF4iapogH5iaBT5tA2HjQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkfgMGlA5ot9Kc76NskTjsnogKLXSSHEQc21JUjYQeiariaCrWZLAuVH7g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wk9bZQH17lwib6nZysoUP9yVCWs6fZmH7twWuCGqCYnRV0EsYd0tZ026w/640?wx_fmt=png)

2014 Magento Demo Store. All Rights Reserved

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkJuTXb88aNEMOhvH0tic5ICfF8uwfPbaECOUGbIm69OAcuKFn6f29YYw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkbwjRYFlaMZAZmpr5VeLR3FmvILKIRyURsC6EQjZ38Mdg5tt15FUpaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkLHOQ5AIApoBd0harFQlITvluEfQ2NZRMibvGlvwpklWJCPI7B3Tc0Qw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkEgb2jN9j2n1g1ibcjdzZT5FZPb4NefyNYFTQzHm1gGLRQJUCJYmgUJg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/wibLMEtPxf6EkD9f6Evlem2Z3Kwx8Wsf3ibbJxgNhMufMWibuhVC8fraoR28ibQBwCWXQhOkZMM2ezUHCoHQLjxNYQ/640?wx_fmt=png)

  

方法 1：

  

文件上传提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkOC3iccxdyFyGDVn2SicvrCw0B9VcHTTPXexFfUstlFvObOTvLEiako6fw/640?wx_fmt=png)

选择 System---Configuration

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wktZECLyAsuIfz1ibtFvoKlankHQcBwFAnWAfA6QkRdUowkV7aq8LVicVQ/640?wx_fmt=png)

选择 Developer...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkbyDh72XgdOckHhqdlSjt3v4vBKAiaPibqN19FmcfHTzb5iaoGUFnTbvWg/640?wx_fmt=png)

选择 yes，获得 png 图像... 文件上传前提条件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkpyUnW9oACQ2iaxBFnb0PIl9iaDzfmrlhpB9r1DmTw985yXMyQfDxVib6g/640?wx_fmt=png)

写入简单的 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkd5B363giamArEv76ayFONDRZtXJaaILXUqOyCbZWLXxclP71PUn8jGw/640?wx_fmt=png)

选择 Catalog---Manage Categories 上传刚创建的 shell 文件即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkTa8mkAKmZ3EZan4IUDEfR3WEUHZyCFvKaGNIKoyefFPl74pViaibFTVA/640?wx_fmt=png)

选择 Newsletter---Newsletter Templates 创建新闻稿模板并注入有效负载...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkrViaC6SdDlb2fGPTLLKhov1cptnpGbgaHiaDf3AHkSrFcUiaSbwrl0PWg/640?wx_fmt=png)

```
{{block type='core/template' template='../../../../../../media/catalog/category/dayu.php.png'}}
```

引用目录图片即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wklwEnA2k67VvQ4MaZZ5H0sQ6L3XQh8kKqXDwsQff52iaeluFdluvNIHg/640?wx_fmt=png)

获得了反弹外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/wibLMEtPxf6EkD9f6Evlem2Z3Kwx8Wsf3ibbJxgNhMufMWibuhVC8fraoR28ibQBwCWXQhOkZMM2ezUHCoHQLjxNYQ/640?wx_fmt=png)

  

方法 2：

  

内核提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkefgQdJ4QWQuy2AOxdvW3WjQXxWnWCE9Oh2PGAUBJiczKKIeVHiaw7TLw/640?wx_fmt=png)

利用 37811.py 提权即可... 这里需要注意的是 pip install mechanize 模块，然后是基于用户名密码和时间进行的 EXP.... 需要爆破目录，获得 app 目录后里面有 html 文件信息可获取时间信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNhP0oiabYqlWFj3L0y4T5wkdQ9JnKnibUczGiaBvWtS9kKUQtub7ZSvwBd5cuqltDcfaxz95RxdwfNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ZREXjsC2nJKx0JHGsC5rFpiaQjsk60OEibhDJ4vLJgUl7n0nCnGoCmtcS6TWpecmKRlG5IwNnyjGHau71NkOwyTw/640?wx_fmt=png)

检查 sudo 并发现它 www-data 可以 vi 作为 root 运行在以下 / var/www/html / 任何文件中....

在 vi 中以 root 身份打开了 index.php... 并输入!/bin/bash... 获得 root 外壳....

获得了 root 权限和 root_flag 信息...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/9h3lBeicPhRCbL55vicQK1Qj4FqoebibNv9EhH20XgIRH3RZicuNRbKdZqdDr5c2JMCyJWH8zicp8cJH9gJCp0Zy8Qg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)