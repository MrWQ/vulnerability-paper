> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FA8CXdMkUBqJeQ0xPCuWNA)

 **该漏洞已经提交，以下内容仅限学习**  

    在蓝队游啊游的时候，微信群里有老哥发了一张截图，内容说 coremail 邮箱系统漏洞攻击事件，这就让我这本身困意慢慢顿时充满精神。  

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaKhZo52wYFXre5Af2tVLLnYIsNI0HZR7H3fVtOKzrcibeXeHC9TR0A8P6YWvEe1XMW30gjRfuDchA/640?wx_fmt=png)

    利用方法都在上面了，那就找随便找个资产试试 (不能确定百分百成功嗷，成功几率咱也不知道)。  

    url:xxxxxxx   ![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaKhZo52wYFXre5Af2tVLLnHDET4k7062DkaYZI3JwFH8cWdJlodyt8PHB3p98SQmzKKkwk1cpyibQ/640?wx_fmt=png)

    url+/lunkr/cache/;/;/../../manager.html

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaKhZo52wYFXre5Af2tVLLnXpo8kyVGFlXgLkscVAC8huvEtOjgicHibSMA9nW7Yb2bUXOy8ryTiaTcw/640?wx_fmt=png)

    访问过去会直接跳转到 tomcat 控制台，这里你就可以采用 coremail/coremail 弱口令尝试登陆，或者暴力破解。然后就是部署 war 包 Getshell 就 ok 了。(小鸡肋)  

修复建议：对外隐藏 tomcat 控制台，修改默认口令。  

    附一张成功的图：  

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaKhZo52wYFXre5Af2tVLLnib26xw33JiabXoZnUlmdOEZYQzku1ic6ym8QXwic3msnLm5RrFnMPbFJIg/640?wx_fmt=png)

（fofa 收集资产的收获百分之 80 资产都打不开了，别尝试了！）

-END-

![](https://mmbiz.qpic.cn/mmbiz_gif/eqGGHicCG3MYLsiafhuCAGuOSuIhKap61miagSh8mlA1Yb2riaSibiaTE9wF0zoZfPOTIgSMKrvTjM6lSBWwSiaGx584g/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_jpg/eqGGHicCG3MYLsiafhuCAGuOSuIhKap61mrMsqiaz5Is1EjiayDv4AFiaFibBAdZjwTuhlVF0NaOM1A9DXx0qy48se8Q/640?wx_fmt=jpeg)

微信号：Zero-safety

- 扫码关注我们 -

带你领略不一样的世界

![](https://mmbiz.qpic.cn/mmbiz_gif/eqGGHicCG3MYLsiafhuCAGuOSuIhKap61mOnuN32N92RN4WvG94sL3diaBGSaFNMh2ZQXtibB0SiaLtyCuk6e6EKYoQ/640?wx_fmt=gif)