> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/scvplq3CZTZYnFd7wzSQKw)

**API 安全概述  
**  
      Application Programma Interface (API) 由一组定义和协议组合而成，可用于构建和企业集成应用软件。随着数字化转型的深入，API 产品的价值日益增高，特别是与微服务、DevOps 等技术的融合，使得 API 成为企业战略发展加速的利器，但随之而来的安全问题也不容忽视。常见的 API 安全漏洞有以下五种：  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icmg9dxPTRVwDbXeoPyIIq2qvDTl3tQxy3oXRomK2Rp3A1U2NEn612xCt5XgBXCia7JD89zCSHyxgIA/640?wx_fmt=png)

  1. 首先是 API 应该与应用系统一样在设计之初就考虑安全的因素，比如防篡改（签名）、防重放（时间戳）、防止敏感信息泄露（传输加密与数据最小化）等。  
 2. API 规范性带来的一个问题就是 API 很容易被发现，比如在 URL 中出现的 v1/login，参数中出现的 "function": "login" 等。  
  3.  安全配置错误常常包括：未使用加密传输协议、CSRF、CORS 等。  
  4.  参数过多就会导致信息泄露以及便于攻击者执行频率分析攻击，

比如 "role": "user" 容易让攻击者联想到 "role": "admin" 等。  
  5. 数据过多：传输过多的数据、返回过多的数据、参数值暴露敏感信息等都是数据过多导致的安全问题。  
    同时 OWASP 在 2019 年也列举了 API 最受关注的十大安全问题：  
  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icmg9dxPTRVwDbXeoPyIIq2qKBIYjnG8IJiaytaFdPvelTPicokOTL2rzicibz77FjEg8lc8Nr7RdEQt3g/640?wx_fmt=png)

    从上述的两张图中我们就可以大体了解 API 常面临的风险是什么，那么如何来解决这些安全问题？

**API 安全测试方法**  
     要想全面解决 API 的安全问题，就要在每次 API 研发完成之后进行全面的安全测试，为了防止测试过程中出现的遗漏，我们可以准备一个检查列表 v1.0（本列表主要来自：https://github.com/shieldfy/API-Security-Checklist/blob/master/README-zh.md，添加了一些自己的分类依据、测试方法、修复方案等）：  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icmg9dxPTRVwDbXeoPyIIq2qEUoibmRicUwXoEnnrb4QxPfCQryLW1UtL39h5zcAlTsahgMMzlakp7Ng/640?wx_fmt=png)

**API 安全测试工具**  
   很多时候重复的劳动力是不必要的，所以利用好工具事半功倍（工欲善其事必先利其器）。

  
Astra  
https://github.com/flipkart-incubator/Astra  
安装 Astra 非常简单，我们直接使用 Docker 部署即可（官网已经有了详细说明，值得注意的是编译 Astra 时网络是个大问题，自行扶墙）

  
Burp Suite  
Burp 的强大之处不用多说，但是针对 API 的测试，我更喜欢把 BurpSuite 与 Postman 结合起来使用。

  
fuzzapi  
https://github.com/Fuzzapi/fuzzapi  
安装过程不赘述。

  
Postman  
结合 Burp 来使用，后期有空专门写 BurpSuite + Postman。  
其实写本文主要是为了帮自己梳理一下 API 的安全漏洞和检查要点，上面的图只是一个 1.0 版本，并且本表的很多列我也暂时没有共享出来，后期 2.0 会更新。

  
reference  
    API Security Checklist：

```
https://github.com/shieldfy/API-Security-Checklist
```

    API 的五个常见漏洞：  

```
https://min.news/zh-cn/tech/24cceb1c0d9169a7dc68e58e0e669864.html
```

    API 接口渗透测试：

```
https://xz.aliyun.com/t/2412
```

    应用程序接口（API）安全：  

```
https://www.freebuf.com/articles/web/248251.html
```

————————————————  
转自 CSDN 原文链接：

https://blog.csdn.net/bloodzero_new/article/details/112479328  

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**