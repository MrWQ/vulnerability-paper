> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI0MDY1MDU4MQ==&mid=2247496339&idx=2&sn=0e00fdf3842442686fc730046ed36ff3&chksm=e91522a9de62abbf94c47374121f6bc8d84ee28e98ce8e4380ac121eff4acf8360b6956e19f8&mpshare=1&&srcid=&sharer_sharetime=1574856568652&sharer_shareid=11b10227ef89bc31e305a25ecefd5973&from=timeline&scene=2&subscene=1&clicktime=1574857821&enterid=1574857821#rd)

![](https://mmbiz.qpic.cn/mmbiz_gif/wpkib3J60o297rwgIksvLibPOwR24tqI8dGRUah80YoBLjTBJgws2n0ibdvfvv3CCm0MIOHTAgKicmOB4UHUJ1hH5g/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X7YajvLJtXHyvHIUuRscsAzxcWf9yOD17bFr3dCVSpiaEhOl5V7mU1tpA/640?wx_fmt=png) 背景  

2019 年 10 月 29 日，有研究人员在 GitHub 上公布了 Apache Solr RCE 漏洞的 PoC 代码。Solr 是 Apache Lucene 内置的开源平台。PoC 公布之初，该漏洞没有 CVE 编号也没有来自 Apache 的官方确认。Tenable 研究人员分析确认了 Apache Solr v7.7.2 到 8.3 版本都受到该漏洞的影响，研究人员还推测包含 Config API 的老版本也受该漏洞的影响。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X7YajvLJtXHyvHIUuRscsAzxcWf9yOD17bFr3dCVSpiaEhOl5V7mU1tpA/640?wx_fmt=png) 分析

根据该 PoC，攻击者在识别出 Solr core 名后可以攻击有漏洞的 Apache Solr 实例。在识别出 core 名后，攻击者可以发送精心伪造的 HTTP POST 请求到 Config API 来将 solrconfig.xml 文件的 Velocity Response Writer 的 params resource loader 值修改为 true。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X77El35vhnNickkJ2qqCPjaShH7A67sMPUNHIz2iaLJmo6ERrRQicibMpwKA/640?wx_fmt=png)

启用该参数使得攻击者可以在伪造的 Solr 请求中使用 velocity template 参数，最终引发 RCE。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X7zDzkU7Ekq12rsenicaVKJLqUJiaflE4iaFBLTI51GGZJCVnXP1ODTuoSQ/640?wx_fmt=gif)

虽然最近发布的 Apache Solr 8.3 解决了 7 月报告的默认配置漏洞，但 Velocity template 漏洞仍然没有修复。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X7YajvLJtXHyvHIUuRscsAzxcWf9yOD17bFr3dCVSpiaEhOl5V7mU1tpA/640?wx_fmt=png) PoC

研究人员于 2019 年 10 月 29 日将 PoC 上传到了 Github Gist。今天后，漏洞利用脚本也公布在 Github 上。

Github Gist：https://gist.github.com/s00py/a1ba36a3689fa13759ff910e179fc133

漏洞利用脚本：https://github.com/jas502n/solr_rce

![](https://mmbiz.qpic.cn/sz_mmbiz_png/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X7YajvLJtXHyvHIUuRscsAzxcWf9yOD17bFr3dCVSpiaEhOl5V7mU1tpA/640?wx_fmt=png) 解决方案

截至目前，官方仍没有发布补丁。在补丁发布前，研究人员建议更新在 Apache Solr 中添加实例来防止该漏洞被攻击者利用。检查 solrconfig.xml 配置中的 VelocityResponseWriter 类来确保 params resource loader 的值是 false。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X7l605Seicgbp7Ephd5Tf58qnIM4ByJT5eian8e4YIuHsUDK0xq6dicQHNw/640?wx_fmt=png)

除非 Config API 被锁定，攻击者还可以修改 solrconfig.xml 文件。

注：本文翻译自：https://zh-cn.tenable.com/blog/apache-solr-vulnerable-to-remote-code-execution-zero-day-vulnerability

![](https://mmbiz.qpic.cn/sz_mmbiz_png/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X70MY64L6hFPMJrB1n01icre9Pf6OvQ3EGBs84mtQIcIoaTfIqqcEMgMg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/wpkib3J60o29ibXfNoXSQvEqmBU3MvR4X7h5CD1fhMBAh1eGjkG6khPP1fKWW0ib5TVJ9pWKRIzo4sgxanj4c8ZFw/640?wx_fmt=jpeg)