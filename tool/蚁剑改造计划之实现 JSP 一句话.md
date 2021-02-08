> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/O28USxZyMaxN_pMfrEPZtg)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacXc5zqbsHRudnlsvQuFzkEwZogvdlntl1YV7BIu81HCo9uST0ejm9Mg/640?wx_fmt=png)

点击蓝字关注我哦

转载  

  

**前言**

转载来自：yzddMr6 师傅 blog  

原文链接：https://yzddmr6.tk/posts/node-edit-java-class/

本人有意写一份系列文章，主要内容是分享蚁剑改造过程中的一些技巧与经验。  

因为蚁剑的相关文档实在比较少，可能很多同学都像自己当初一样想要二次开发可是不知如何下手。

不敢贸然称之为教程，只是把改造的过程发出来供大家借鉴，希望其他同学能够少走弯路。

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacHC3DHzjopMfb1HFNiaBqlpuaUNR5f1XeMrZqnGTsG1hOIeiaEzLXrraQ/640?wx_fmt=png)

**历史遗留问题**

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacHC3DHzjopMfb1HFNiaBqlpuaUNR5f1XeMrZqnGTsG1hOIeiaEzLXrraQ/640?wx_fmt=png)

我在前面几篇文章提到过，蚁剑一直有一个硬伤就是它对于其他参数的处理仅仅是一层 base64。这就导致了不管怎么对主 payload 加密，WAF 只要分析到其他的参数就能知道你在做什么。

例如你在执行 cmd 的时候，就一定会发送一个经过 base64 编码的 cmd 字符串，这就留下了一个被 WAF 识别的特征。

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacpsT8Iurzjr5WzPeqX8zkwXsvxKNU3xEcVsYwjN7UnbibRCbOp8VHknA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacolpiaZlgCicrbloMTorag7NalTdiaxYu8l7ibMKibsJFUViaibJsOH13AfFvQ/640?wx_fmt=png)

即使是蚁剑编码器仓库中的 aes 编码器也只是对主 payload 加了密，防护方在不需要解密主 payload 的情况下只要看到其他参数传的什么内容就能推测攻击者的行为。

yan 表哥曾经在公众号中的 WAF 拦了蚁剑发送的其它参数时怎么操作文章中给出了一种解决方案。主要思想就是在不修改主 payload 的情况下，配合客户端额外再把它加密解密一遍。

可以是可以，但是很麻烦，对于普通的 shell 不具有适用性。

这篇文章的目的就是解决掉这个历史遗留问题。

**随机化方式的选择**

想要从根本上解决问题就要修改核心 payload，那么怎么改呢？

以前师傅们的文章提出过两个方法，一种是把其他参数 base64 两次，还有一种是在其他参数前面加两个随机字符，然后主 payload 中再把它给 substr 截掉，来打乱 base64 的解码。

如果方法是写死的话，无非只是 WAF 增加两条规则而已。蚁剑这么有名的项目，一定是防火墙商眼中紧盯的目标。最好的解决办法就是加入一个用户可控的参数，能够让用户自定义修改。这样才有可能最大程度的逃过 WAF 的流量查杀。

所以本文采用的方法就是在每个第三方参数前，加入用户自定义长度的随机字符串，来打乱 base64 的解码。

这时，如果 WAF 不能获得主 payload 中用户预定义的偏移量，也就无法对其他参数进行解密。此时我们的强加密型编码器才能真正起到作用。

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacJrJCggzazO4MOB04OP3TEcIUfvDERAcWblx0RVJjLvoIj2rBACP6Cg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacJrJCggzazO4MOB04OP3TEcIUfvDERAcWblx0RVJjLvoIj2rBACP6Cg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacrg4tUdEmogiaOWURbdjjrNFqHukHGujHViczJCRpSD7swAPgPFoxKkpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacnVXtLl5rxlW80tefebB6cicBOZMjGLrG5eUYY5Ue8YwicW1bphghEO5A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacnVXtLl5rxlW80tefebB6cicBOZMjGLrG5eUYY5Ue8YwicW1bphghEO5A/640?wx_fmt=png)

**具体实现**

思路  

```
获取用户预定义前缀偏移量->修改核心payload模版->给其他参数前增加随机字符串
```

前端的话首先写一个 text 框，来获取用户的输入

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacu4TUiabIJHhW2oc8nqojzibx2DjB5KfvSjZicz2bDeAevhzn11eXCleibQ/640?wx_fmt=png)

在 \ source\core\base.js 中定义 randomPrefix 变量

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacic440cCK8FIccnFlwlyypPpiaV2npPea2nIBa2r7qUOzia3H2Xib4BXJfg/640?wx_fmt=png)

在 \ source\modules\settings\adefault.js 中设置默认值

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniac1IKqMsSpng8oial2VttTlMWlibP7d1Uiafgutb0DHIjFAlsgIeF0GznEA/640?wx_fmt=png)

然后后端就可以通过 opts.otherConf["random-Prefix"] 来获取用户定义的随机前缀的长度值。

修改模版前要简单了解一下蚁剑对于参数的处理流程

在各类型 shell 的模版文件中，会定义默认的 payload 以及他们所需要的参数，还有对于参数的编码方式。

source\core\php\template\filemanager.js

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacicV9VU8olQibfSLicZYgicicwHDj0KgtgYJ3lX5MaMFf8Qkvl7aOzjicTecQ/640?wx_fmt=png)

在获取到模版之后，parseTemplate 会对其中的参数进行提取、解析、组合，形成要发送的 payload

source\core\base.js

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacRUmA6Eic8RxpRz122udK6PgnquDJ1hyup1WFYLAsELDKxsibIQWa0xTQ/640?wx_fmt=png)

所以我们要把用户预定义的前缀偏移量传入到两个地方：

（1）核心 payload 模版

（2）其他参数的组合模块

在核心 payload 中，我们将要修改的偏移量用 #randomPrefix# 进行标记，到 parseTemplate 函数组合最终数据包的时候将其替换。

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniactiaMEsPlO4DcZVHCgMEviaOA5ZR0zYBKOBGoj4uRm1QeqmTrsqalME1g/640?wx_fmt=png)

然后定义一个新类型的编码处理器 newbase64，在模板中修改对于参数的处理函数。   

```
/**
 * 增加随机前缀的base64编码
 * @param  {String} str 字符串
 * @return {String}     编码后的字符串
 */
newbase64(str) {
  let randomString=(length)=>{
    let chars='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let result = '';
    for (let i = length; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
    return result;
}
  return randomString(randomPrefix)+Buffer.from(iconv.encode(Buffer.from(str), encode)).toString('base64');
}
```

修改后的模板长这个样

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacuVf3UjXAjAoq9jSSoSPv40oh7vtxTEPdYvsic6faPRibAvffeytpN8pA/640?wx_fmt=png)

期间遇到一个小坑，就是无法在 format() 函数中获取 opts 的值

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacp4HsYSXBOrraMvJPibqxAEHTj6cAHmmeBKKhromjT6eWLAU76I55K1g/640?wx_fmt=png)

后来发现蚁剑中是这样写的

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacvQDScyWficFiaeG98k8H0qNEQYqOFrkYv1K9icDONMtYD8rx1dib0Ag3Zw/640?wx_fmt=png)

还特意把原来的 new this.format 给注释掉换成 Base.prototype.format 的形式，具体原因我也不知道为什么。如果有知道的师傅麻烦告诉我一下。

既然追求刺激，那就贯彻到底，直接把 opts 传给 format 函数，然后在 format 中重新取所需要的变量。

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniac0rDyLgguBfnSIPTCcdzsVhmP1MDD16EUxI2V9l0EIv8GibBTkaxj1pg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacG0o1ib908w19USRs8YHc6GJFx939Y0WlKj1icVRVWyfFsFIEkyjT8neA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniac2CwxmjPzia4yWciclDC5NEDDv2PHdbibtsrV6E4oUVzccPGLC9ZdgTcDg/640?wx_fmt=png)

**测试**

前缀长度默认为 2，可以自行修改，只要不是 4 的倍数即可 (原因自己思考一下)。

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacEQmqZiaT8bfRCLfZyFLeFKZ5sHj0yfdYsC8MfoYg695tLmP6EhLSuyg/640?wx_fmt=png)

可以正常使用

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacVb0V6sPSMwjcjPetOMCNmKBkZzTqXdAmDtvQ1sibac77tSRovqrq9og/640?wx_fmt=png)

其中 prototype 为我们传入的第三方参数的值，在这里是要打开目录的绝对路径

```
prototype=ojRDovcGhwU3R1ZHkvUEhQVHV0b3JpYWwvV1dXL3BocE15QWRtaW4v
```

直接 base64 解码会是乱码

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniacOkbAN1R9cpjT4Nwicm95aXQDqyVqkiaLXQibjMtXyrG5C9mgVpvPicaXEQ/640?wx_fmt=png)

去掉前两位后我们进行解码则可以得到正确的结果。

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtWwKTBicxPx5KTp71fIXniack6bpoQwacFIP8WNb8QQ3eYbcyNxJ9b6bKzmkBC0bLwlL4DBVLndoPg/640?wx_fmt=png)

  

 最 后 

  

偏移两位的效果可能还不是很明显，容易被猜出。但是当前缀长度达到 10 位以上的时候，就很难分析出最后的结果。

对 php 类型修改后我在本地测试了主要的 13 个功能，均可以正常使用。但是由于涉及到修改核心 payload，等确定没有 bug 了再改其他的。

由于我是在父类 Base 中修改的编码模块，想修改其他类型的 shell 只需要照葫芦画瓢改一下对应的模版即可。

修改后的项目地址：

https://github.com/yzddmr6/antSword/tree/v2.1.x

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

END

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtIZ5VYusLbEoY8iaTjibTWg6AKjAQiahf2fctN4PSdYm2O1Hibr56ia39iaJcxBoe04t4nlYyOmRvCr56Q/640?wx_fmt=gif)

**看完记得点赞，关注哟，爱您！**

**请严格遵守网络安全法相关条例！此分享主要用于学习，切勿走上违法犯罪的不归路，一切后果自付！**

  

关注此公众号，各种福利领不停，轻轻松松学习 hacker 技术！

  

**在看你就赞赞我！**

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbThXaInFkmyjOOcBoNCXGun5icNbT4mjCjcREA3nMN7G8icS0IKM3ebuLA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTkwLkofibxKKjhEu7Rx8u1P8sibicPkzKmkjjvddDg8vDYxLibe143CwHAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/96Koibz2dODt7492lKcjVLXNwERFNUQJVkkKj3EYBiboRWmHfnymrDxeEVrYapXicBGbRLhPzWv5wbhXR59PDyC8Q/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTicALFtE3HLbUiamP3IAdeINR1a84qnmro82ZKh4lpl5cHumDfzCE3P8w/640?wx_fmt=gif)

扫码关注我们

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTicALFtE3HLbUiamP3IAdeINR1a84qnmro82ZKh4lpl5cHumDfzCE3P8w/640?wx_fmt=gif)

扫码领 hacker 资料，常用工具，以及各种福利

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTnHS31hY5p9FJS6gMfNZcSH2TibPUmiam6ajGW3l43pb0ySLc1FibHmicibw/640?wx_fmt=gif)

转载是一种动力 分享是一种美德