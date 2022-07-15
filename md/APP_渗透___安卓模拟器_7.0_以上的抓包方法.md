\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/1gMiWGiFevwvPFE8R2LSDA)

**抓包前准备：**
----------

模拟器: 雷电模拟器 4.0 Android7.1 内核版本

Proxifier、代理抓包工具 (burpsuite、Fiddler) 均可

通常情况下需要在模拟器中修改 wifi 代理其实我觉得这种是比较麻烦的、何必不只要我运行了 burpsuite 和 Proxifier 之后就可以抓模拟器包，不需要修改其内部配置呢。并且某些 app 也会检测代理情况，如果修改了或开启了代理 app 就无法正常运行，我们通过在模拟器外部进行抓包来绕过 app 检测。

**开始配置：**

首先运行 burpsuite 监听默认 8080 端口

Proxifier 第一步

打开 Proxifier 添加代理服务器

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSbUyib31VVbBvKHgbuSarJDABWKDQmKagRbW6AezfmeeFofq1Ghxiaetg/640?wx_fmt=png)

地址 127.0.0.1 端口 8080 协议 https

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSo7m5WU9qWhThV3eQNR3yr0H3Ya4WibKxWELLuRRChfRMYIv7zVGMwWg/640?wx_fmt=png)

开始测试通过即可（在进行这一步之前你要确保你的电脑已经安装了 burpsuite 的证书并且可以正常抓取 https 的包）

**Proxifier 第二步**

添加代理规则

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSkiaXiawLiaiaZzoy1wvImL6icYUsETibywiagQXsLXs20LPleM3UP2n7Guh2g/640?wx_fmt=png)

应用程序选择 dnplayer.exe;LdVBoxHeadless.exe;

dnplayer 雷电模拟器启动程序和模拟器主程序

LdVBoxHeadless 雷电模拟器对外网络协议走的都是这个程序

动作选择刚才添加的代理服务器。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCS639HhBelNycHwlExibI3xzxyepSeDuicss25SrzTX1EYIcmTpibxnic1yw/640?wx_fmt=png)

进行到这一步后我们在模拟器中打开浏览器就可以从 Proxifier 中看到流量情况，但是目前我们只能抓取 http 的包还不能抓 https 的包。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSjUQkhdXk4M78YjWun8ak4GISy1DFGkcFhIMe8LxX0pQPA4UKFyZtibQ/640?wx_fmt=png)

浏览器提示证书问题

**解决抓取 https 问题：**
------------------

不能抓取 https 的包肯定是没多大意义的。所以我们要来解决这个问题，经过查询资料了解到安卓 7.0 以上后默认不在信任用户自行安装的证书文件、如果需要抓包我们就要把自己的证书放到系统目录下、或者对 app 进行修改从而进行抓包。在这里我选择安装系统证书的方式进行更加通用的方式进行处理。

1: 从浏览器中导出 burpsuite 的证书

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCS4vUat7u2j7P1reuJawNdkiaHqOh2LHEGnib8lp1r7keAlAph5ddf4pcg/640?wx_fmt=png)

在谷歌浏览器设置中搜索管理证书 - 安全下找到管理证书。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSRPh1zrR4EnUyGUYfEYutwG338E9rRmRpSInnnHw6clVHczX6Ebk4Pw/640?wx_fmt=png)

我的证书是安装在受信任的根证书颁发机构然后找到 PortSwigger CA

选择导出

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSyUibkgnnLll01rubR86KzYianPrLNkwhIJ1Q21MibMFyu5F9xCr3s7ALQ/640?wx_fmt=png)

导出格式选择 base64 编码 cer 方式、保存文件名任意 xxxx.cer 即可

2：导入模拟器

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCS1k5Y1qWw44cSqYKyATPViaLUmljXg39dGvyMHh9eyGZb2xSDURJmVbg/640?wx_fmt=png)模拟器右边的功能条中选择共享文件、打开电脑文件夹

把导出的证书拖放其中

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSP0TEVPuuq0ibiajH1oZewM0h2Bb4QspLLRY0EDrMVGsPaXicgUnRJgJnw/640?wx_fmt=png)

或者直接把文件放到 C:\\Users\\Administrator\\Documents\\leidian\\Pictures 目录下即可

3：安装证书

在模拟器中找到设置 - 安全 - 从 SD 卡中安装

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSkIbNatpMYBD2L2LbXNOmbOthXECZLh37I5nmEGP19w7MM11miaola9A/640?wx_fmt=png)

找到放入的证书进行安装

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSTGhBsHpbdl2sqYB7zf7vibX6gyhMSqAHicGjlLXHtL4YWgByHiamfFWIQ/640?wx_fmt=png)

安装完毕后在模拟器中下载 re 文件管理器

进入：/data/misc/user/0/cacerts-added 这个文件夹下（该目录存储的是用户自己安装的证书文件）

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSX6N4yJT2icsiaYaga9byIPkp9BIULvp5ppOekCF5hS7oES3nZJIsGHQg/640?wx_fmt=png)

复制该. 0 文件（文件名可能是不一样的）

复制到系统证书目录 / etc/security/cacerts 下（re 文件管理器需要挂载读写权限、模拟器中自带 root 管理授权即可）

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCS74wyeSKfCyL3EYkGENzY95FJrhHXKSlMNia3tA95BroCzEibg946rtkw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSdpVoIzJoSFmYFzapCv3gk4yvrPrC0IgMVWllPg5SSWiaicibqvrTutVLQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCS5U7YyZJN5ragq5AjckZm0ovXukEHtfzic0N5ZibOJEj5mrlXo8I5nialw/640?wx_fmt=png)

确认后把证书已经放到系统证书目录即可。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCS3dDEWyEMwjTNKyF6LTc1XaRDyvFicj93F89Z7CKcicicyKkLBlVSibBdSg/640?wx_fmt=png)

重新刷新即可正常抓取 https。

**其他拓展：**
---------

双向认证 app，有些 app 会认证客户端和服务器证书。一般反编译 app 到其中找到其内置的证书。但是我们可以通过 xposed 框架对 ssl 进行 hook 从而来绕过检测。

百度下载 xposed installer

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSVRlNicePRM3EVWLITYxhTbEhXfRQic7Cv87zmEhgZy5gFjT3iaVkMRQ5Q/640?wx_fmt=png)

安装

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibJ4BpGrFprIYoMibFpTxbCSh1UcicA4SSjlMMjSBlrcXAkAcOgV3kkIb5Opdep2I8jVv0DiaZu9eaPw/640?wx_fmt=png)

justtrustme 模块、有时候启用这个模块就会出问题、我更加推荐 SSLUnpinning 这个 xposed 模块，安装完毕后选择有双向认证的 app 即可愉快的进行抓包调试。

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

[![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou80h6Jor7Py4sKIwfiaowozsMP0Yjn9RcoJAmPMKa5hQVczeXoDxIic2QaZYKKrLDlJFT5v6EpREmjg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247490909&idx=1&sn=efdbd98bd302159324cb431f3d735165&chksm=ec1f4862db68c174c21d98f46847bba21a19602c4823ec17fb7363662751c385817e85d9c6ce&scene=21#wechat_redirect)

**点赞，转发，在看**  

投稿作者：cacker

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)
