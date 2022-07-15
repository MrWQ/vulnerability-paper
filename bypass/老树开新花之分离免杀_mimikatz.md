> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/N9UPWtwUICmEzozMxD2ZgA)

    之前也给大家分享过类似的免杀的 mimikatz，想必现在已经被杀得没办法用了，这里介绍一种更简单的方法，利用分离免杀的方法加载 mimikatz。

     先来看下免杀情况：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08X61v71vcvRJTOFYMuWGEibGw4fvKe1o5IU42BtwDa2jFT6BW41tKIuakzCOZSLVo6ZbeRkCY1LgSA/640?wx_fmt=png)

最新版 360 是没有任何问题的，这里使用的是 K8 的抓密码版的 mimikatz，自带 log 功能，然后使用加载器加载，注意将 mz64.bin 与 mimikatz_load.exe 放到同一目录下面，不可改名，因为名字已经写死在了程序之中。加载器大小 13k、bin 大小 900k，实战中完全可行。

   执行效果：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08X61v71vcvRJTOFYMuWGEibGYiaqNObha3H3f706picTkQ6coAdhtnwmbtYZ2Zj0683VgiagHf754LCiaA/640?wx_fmt=png)

目前为 x64 版本，原理很简单，打开 bin 文件，相比大家就知道了，剩下的就看大家发挥了。  

文件地址：

https://github.com/lengjibo/RedTeamTools/tree/master/windows/mimikatz_bypassAV

**顺便说一下，团队近期准备搞个公开课，免费的，讲一讲 powershell 的一些东西，内容较基础，希望到时候大家能给捧个场，具体时间到时候在公众号通知。**

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)