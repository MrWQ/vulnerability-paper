> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247483881&idx=1&sn=79d714e324694b8ac9bc399b0d44202b&chksm=eaad81d4ddda08c25a735ca6c173159bc16ff1c991e80fe876a1eb7388371a57e5aec1c78a80&scene=21#wechat_redirect)

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7H2bowpqCQLXiczqD2rfB49Avt1ucibvLB4q9MAuuhkvWv8hKVicVV1LEWTpLjIPm2yK65AmQiaX2OnA/640?wx_fmt=png)

  

  

  

  

目录

  

  

  

  

whatweb

一些常见的 Whatweb 的扫描

常规扫描

批量扫描

详细回显扫描

扫描强度等级控制

快速本地扫描 (扫描内网的主机)

将扫描结果导出至文件内

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6mpt7JbBoCdIbkf4IeUUsjTLpicJFnj5ZvTLv2tc9HW06OdNicgdZ9V90GGUonok8nibSiagrTZUicbiag/640?wx_fmt=gif)

**whatweb** 是 kali 中网站指纹识别的工具，使用 Ruby 语言开发。whatweb 可识别 web 技术，包括内容管理系统 (CMS)、博客平台、统计 / 分析包、JavaScript 库，Web 服务器和嵌入式设备等。它有超过 900 个插件，每个插件都能识别不同的东西。Whatweb 还可以识别版本号，电子邮件地址、账户 ID、Web 框架模块，SQL 错误等。

WhatWeb 可以隐秘、快速、彻底或缓慢扫描。WhatWeb 支持攻击级别来控制速度和可靠性之间的权衡。当在浏览器中访问网站时，该交易包含许多关于 Web 技术为该网站提供支持的提示。有时，单个网页访问包含足够的信息来识别网站，但如果没有，WhatWeb 可以进一步询问网站。默认的攻击级别称为 “被动”，速度最快，只需要一个网站的 HTTP 请求。这适用于扫描公共网站。在渗透测试中开发了更积极的模式。

用法： **weatweb  域名**

· -i  指定要扫描的文件

· -v 详细显示扫描的结果

· -a  指定运行级别

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6mpt7JbBoCdIbkf4IeUUsjGrBMAlHicO29manAkibywYt5sYVtd7QoJiaicrHSfeIJCcIQib4PJuoYt9g/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HzZrTT4UZAcukC3cKqetSHpGJABL8ZCM8yibLyNpvY2Zia3IAY3P6yE9A/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vX9vXicvL86eYMxClIadcXxMJ6YrZHMkVAeu0QFJgnFsJqHm0Ohn1ZVbg/640?wx_fmt=png)

 常规扫描

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vXP4kmnG0ITetrvpfxbsHWClNnbEDw4YnibREnpzCP0k1XAKeLqCZDGTg/640?wx_fmt=png)

**whatweb   域名**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1foKzZVHEQY7rsq3dgSm72ATNwFAibicTHh53RibSHtFRGxIbIjic6xQbQUw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC64Jegp0lgLDGafrdvU8MV8qoGNeoxAib3sCumicibOUMK9cV15pvaUmzOgibiarVT9QnwHKbaLAQyYshg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vX9vXicvL86eYMxClIadcXxMJ6YrZHMkVAeu0QFJgnFsJqHm0Ohn1ZVbg/640?wx_fmt=png)

批量扫描

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vXP4kmnG0ITetrvpfxbsHWClNnbEDw4YnibREnpzCP0k1XAKeLqCZDGTg/640?wx_fmt=png)

我们可以通过将很多要扫描的网站域名写入文件内，然后扫描时指定该文件即可。

比如，我们现在在 root 目录下有 target.txt 文件，如下。# 号表示扫描时不扫描该域名

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1frfl7OP8DtP9Pk891icNEANFJsjHt4Mo7waX1fEvJtuwbtZvpuEUnPiaA/640?wx_fmt=png)

使用命令：**whatweb  -i  /root/target.txt**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fCyXBico7QnmGp6VlhFVkyic5RSNWSXiaZJmVj8YuYV7xo2XqP9ickxBIJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC64Jegp0lgLDGafrdvU8MV8qoGNeoxAib3sCumicibOUMK9cV15pvaUmzOgibiarVT9QnwHKbaLAQyYshg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vX9vXicvL86eYMxClIadcXxMJ6YrZHMkVAeu0QFJgnFsJqHm0Ohn1ZVbg/640?wx_fmt=png)

详细回显扫描

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vXP4kmnG0ITetrvpfxbsHWClNnbEDw4YnibREnpzCP0k1XAKeLqCZDGTg/640?wx_fmt=png)

**whatweb  -v  域名**  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fT032RCuyj01EWaKaneSOctWcLH57lOwib2cd6amxoMfByqfic8ubwcoQ/640?wx_fmt=png)

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC64Jegp0lgLDGafrdvU8MV8qoGNeoxAib3sCumicibOUMK9cV15pvaUmzOgibiarVT9QnwHKbaLAQyYshg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vX9vXicvL86eYMxClIadcXxMJ6YrZHMkVAeu0QFJgnFsJqHm0Ohn1ZVbg/640?wx_fmt=png)

扫描强度等级控制

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vXP4kmnG0ITetrvpfxbsHWClNnbEDw4YnibREnpzCP0k1XAKeLqCZDGTg/640?wx_fmt=png)

**whatweb  -a  等级  域名**      可以和 - v 参数结合使用

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fT032RCuyj01EWaKaneSOctWcLH57lOwib2cd6amxoMfByqfic8ubwcoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC64Jegp0lgLDGafrdvU8MV8qoGNeoxAib3sCumicibOUMK9cV15pvaUmzOgibiarVT9QnwHKbaLAQyYshg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vX9vXicvL86eYMxClIadcXxMJ6YrZHMkVAeu0QFJgnFsJqHm0Ohn1ZVbg/640?wx_fmt=png)

快速本地扫描（扫描本地主机）

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vXP4kmnG0ITetrvpfxbsHWClNnbEDw4YnibREnpzCP0k1XAKeLqCZDGTg/640?wx_fmt=png)

**whatweb  --no-errors  -t  255   内网网段** 可以和 - a 和 - v 参数结合使用 

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fOS2Dib6w5uqfC6JFAosypyqicm1olicKXElPFUKEkdFMbkgDibzDKu8neQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC64Jegp0lgLDGafrdvU8MV8qoGNeoxAib3sCumicibOUMK9cV15pvaUmzOgibiarVT9QnwHKbaLAQyYshg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vX9vXicvL86eYMxClIadcXxMJ6YrZHMkVAeu0QFJgnFsJqHm0Ohn1ZVbg/640?wx_fmt=png)

将扫描结果导入到文件内

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC7rcIPiaOpGhxC0LicZoAT7vXP4kmnG0ITetrvpfxbsHWClNnbEDw4YnibREnpzCP0k1XAKeLqCZDGTg/640?wx_fmt=png)

**whatweb  www.baidu.com  --log-xml=baidu.xml**   将结果导入到 baidu.xml 文件中

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1f2icgClwY2jzjwc782BmHVtgKnkibABNyAZ9MsNoHYkEWgTC8xPwLyb2Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5Q3Q2JPcAgQibyJut3L80CAvxE9FKNHZ3MlZdLMhD7oYO7k0siaiciblpNuFV6xoenXkrQe3pTRnweVw/640?wx_fmt=gif)

来源：谢公子的博客

责编：梁粉

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)