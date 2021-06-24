> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/y-shuUny-7DU8oIwjd67ZA)

转自鸿鹄实验室

whids 是一款 Go 语言开发的开源 EDR，其官方地址为：

https://github.com/0xrawsec/whids

其优点如下：  

*   Open Source
    
*   Relies on Sysmon for all the heavy lifting (kernel component)
    
*   Very powerful but also customizable detection engine
    
*   Built by an Incident Responder for all Incident Responders to make their job easier
    
*   Low footprint (no process injection)
    
*   Can co-exist with any antivirus product (advised to run it along with MS Defender)
    
*   Designed for high thoughput. It can easily enrich and analyse 4M events a day per endpoint without performance impact. Good luck to achieve that with a SIEM.
    
*   Easily integrable with other tools (Splunk, ELK, MISP ...)
    
*   Integrated with ATT&CK framework
    

官方给出的运行示意图如下：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xk9dbNyNmlmT9fVobH7HtxfBItgAfonv4xk9McxIowezsnvgltfcIupDCjuW16PS85X0zkgxGJRQ/640?wx_fmt=png)

**部署过程**

首先需要安装 Sysmon，最新版本为 13.1, 下载地址为：https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xk9dbNyNmlmT9fVobH7HtxgHnTEjYXX6moWySjd906t4znpH7CTARAC2T1UsTkKicg0ngkCP6Ltew/640?wx_fmt=png)

使用 - i 安装既可

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xk9dbNyNmlmT9fVobH7HtxgS6svZzVCY6O64Stt3MnB62tNcsyWSVdg9NRY5zh9aib16PX9aAq4Rg/640?wx_fmt=png)

然后导入其配置，地址为：https://github.com/0xrawsec/whids/tree/master/tools/sysmon/v13

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xk9dbNyNmlmT9fVobH7HtxCYXBXibqwiclzuWz2mGf3icEJ1mtFy0NrHpcq2KeKEvaiahQEYobcIFabA/640?wx_fmt=png)

如有需要，可以配置下面的两个的选项：

```
gpedit.msc -> Computer Configuration\Windows Settings\Security Settings\Advanced Audit Policy Configuration\System Audit Policies\System\Audit Security System Extension -> Enable
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xk9dbNyNmlmT9fVobH7HtxZGvyfC1laMWywDZNiba8eAz8T0PeY6TvibsOF7ro8ndngia8jzWdtT3Nw/640?wx_fmt=png)

和

```
gpedit.msc -> Computer Configuration\Windows Settings\Security Settings\Advanced Audit Policy Configuration\System Audit Policies\Object Access\Audit File System -> Enable
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xk9dbNyNmlmT9fVobH7Htx8jicwOK1vklXcJen6rtaTQic7ibAoUHOkNPF6xkqKvzLMicxaSsQwle7Rw/640?wx_fmt=png)

然后运行 agent

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xk9dbNyNmlmT9fVobH7HtxcWyDSX7BuAnvZv1RLBsX9pLH1ukjA9ia5QCHnJynkhD6clnDsXESIFQ/640?wx_fmt=png)

需要 server 的可以运行 server  

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xk9dbNyNmlmT9fVobH7HtxZWB4cxBiaK4a7DR0FQkBG3KX1BlJ5ibCUqIqT9yficTOAG6SozAOsqsKg/640?wx_fmt=png)

附一张效果图

https://github.com/0xrawsec/whids/blob/master/demo/whids.gif

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****关注 LemonSec****  

公众号

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**