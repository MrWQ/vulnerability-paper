\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/aSD6kTTOdVgoZXJuqTSqDQ)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

**所有话题标签：**

[#Web 安全](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1558250808926912513&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#漏洞复现](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1558250808859803651&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#工具使用](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1556485811410419713&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#权限提升](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559100355605544960&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

[#权限维持](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1554692262662619137&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#防护绕过](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1553424967114014720&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#内网安全](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559102220258885633&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#实战案例](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1553386251775492098&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

[#其他笔记](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559102973052567553&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#资源分享](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559103254909796352&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect) [](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559103254909796352&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect) [#MSF](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1570778197200322561&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

 |

**0x00 CDN 简述**

> CDN 的全称是 Content Delivery Network，即内容分发网络。CDN 是构建在现有网络基础之上的智能虚拟网络，依靠部署在各地的边缘服务器，通过中心平台的负载均衡、内容分发、调度等功能模块，使用户就近获取所需内容，降低网络拥塞，提高用户访问响应速度和命中率。
> 
> 百度百科

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKC9UbAEFXUgfv8aicEyEOviaMejafk5vUHsCY8RwamfTtukeKlpkd5ueQ/640?wx_fmt=png)

**0x01 域名解析过程**

*   传统访问：用户访问域名 --> 解析 IP--> 访问目标主机
    
*   简单模式：用户访问域名 -->CDN 节点 --> 真实 IP--> 目标主机
    
*   360 网站卫士：用户访问域名 -->CDN 节点（云 WAF）--> 真实 IP--> 目标主机
    

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKq1EGSx8hUk24jibhicM9EvHlveII5ia1Pich3eZhJZ7a4v3Hg6sEa7tMxw/640?wx_fmt=png)

**注：**目前市面上大多数的 CDN 服务商都提供了云 WAF 配置选项，内置了多种安全防护策略，可对 SQL 注入、XSS 跨站、Webshell 上传、后门隔离保护、命令注入、恶意扫描等攻击行为进行有效拦截。

****0x02 CDN 配置方法****

*   将域名的 NS 记录指向 CDN 厂商提供的 DNS 服务器。  
    
*   给域名设置一个 cname 记录，将它指向 CDN 厂商提供的另一个域名。
    

**0x03 **CDN 检测方法****

利用 “全球 Ping” 快速检测目标是否存在 CDN，如果得到的 IP 归属地是某 CDN 服务商，或者每个地区得到的 IP 地址都不一样则说明可能存在 CDN，可用以下几个网站检测！

```
https://wepcc.com
http://ping.chinaz.com
https://asm.ca.com/en/ping.php
```

**注：**全球 Ping 有一定机率可以得到目标服务器真实 IP，因为有的 CDN 服务商可能没有某些地区的 CDN 节点。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKIoe6UOrB4QyzzyPUY3BKAIrrtvQELj1ZXWT9DVHYHAqkTbbZzAbYMQ/640?wx_fmt=png)  

****0x04 查找真实 IP 方法****

**(1) phpinfo 等探针找到真实 IP**  

通过 l.php、phpinfo.php 等这类探针文件即可得到真实 IP 地址，phpinfo.php 搜索 SERVER\_NAME。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKBS6V3gegoANGfhiaCFmFMTgLuZCvicJ0AavF3rCxKAWeoicCOlicuRliahQ/640?wx_fmt=png)

**(2) 网站根域或子域找到真实 IP**

大部分 CDN 服务都是按流量进行收费的，所以一些网站管理员只会给重要业务部署 CDN，也有很多人会忘了给顶级域名部署 CDN，所以尽可能的多去搜集一些子域名能提高找到真实 IP 地址的机率。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKRBpuZsFic7iczWw7IQ3yxwPYAX2icUbGBIKibq6fKVhPhTbc0IeeIOxpxw/640?wx_fmt=png)

**注：**有时多个子域名可能不会解析到同一台服务器，而是根据公司业务的重要与非重要性将子域名解析在内网或外网的不同服务器中，需要有一定的分析能力。

**(3) 利用邮件服务器找到真实 IP**

Web 和 Email 属同服务器时可以通过 Email 来查询目标真实 IP 地址，如果 Web 和 Email 属不同服务器时我们通过 Email 得到的可能只是邮件服务器的 IP 地址，所以在 hosts 文件中绑定真实 IP 后无法访问目标网站也属正常现象。常见发送邮件的功能有：注册用户、找回密码等。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKa7BFicTxnB4mo8zCDoBP6A7vTcSkQzvRuDCRaS1yY9ibqBGRvqLbmL3g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKSiaibjwI6DNFciat0klBSsIgibZ4X8b2WjtJFozDSp6Z6N3NGuhQF5aaHQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qK3x9GqpUNVdaM4U9OlJV9z5CMoFWTnpjrpFBTfNULInwEaQxRWMI2Jw/640?wx_fmt=png)

**(4) 域名历史解析记录找到真实 IP**

通过查询目标域名历史解析记录可能会找到部署 CDN 前的解析记录（真实 IP 地址），可以用以下几个网站来查询。

```
https://domain.8aq.net    //基于Rapid7 Open Data
https://x.threatbook.cn
https://webiplookup.com
https://viewdns.info/iphistory
https://securitytrails.com/#search
https://toolbar.netcraft.com/site\_report
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKsibYqD2XPJU5wBfmwQAlFmPe15ZVtEicFWeWMibknRWia0JOpCdQhZMdLg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKeiafXB139YsKyrEj4RP7xVOUdV7jcsmrPR97NXyXsLvcTckic99bvD7w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKiab0Th8xcZKQwoIVGWqiaa8NWKGl9JficZ88ibqMlXuTfYY9WxQqNohPiaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKiaTxe4HlXPOvGd3dNgNyH1PhOL5J3eeOeabZk0Xc8CWocte89u5ib11Q/640?wx_fmt=png)

**(5) FOFA 查询网站标题找到真实 IP**

利用 “FOFA 网络空间安全搜索引擎” 搜索目标网站源代码中的 title 标签内容即可得到真实 IP 地址。

```
title="\*\*\* \*\*\*\*\* – Multi Asset Fund"
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKEfQSTIUGkXxzicecJkth0icA3V0MWLuNdH7m5TIG78v4IGaWyYW92oEA/640?wx_fmt=png)

**(6) Censys 查询 SSL 证书找到真实 IP**

利用 “Censys 网络空间搜索引擎” 搜索目标域名的 SSL 证书和 HASH，https://crt.sh 上查找他 SSL 证书的 HASH，然后再用 Censys 搜索该 HASH 值即可得到真实 IP 地址。

```
443.https.tls.certificate.parsed.extensions.subject\_alt\_name.dns\_names:\*\*\*trade.com
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKY3OGu9IfYmUfL886Bjladrp2Ksj8ef14ia0779WyY8s48ib1lpFAuiavg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKFSiacmsXK6mgtFaqSxOCxsnoYoK0Jxbb5aO2B2iaMicBmA42iaYwMDLbfA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfuhds2qsa3WYibtA6lEf1qKdHX17vgmDPj8ib2uicF6FKDJ2YDU7mJe24K5lg3yEmByOS71a8UMbqwQ/640?wx_fmt=png)

**(7) 通过分析目标 C 段来判断真实 IP**

这种方法得看目标有多少子域名吧，如果子域够多，且又有多台服务器（同段），找一个没有部署 CDN 的子域名，然后扫描整个 C 段查找与目标站 Title 一致的即可找到他的真实 IP 地址！

目标站 111.test.com 解析在 192.168.1.10，title：90sec 社区，通过 333.test.com 子域名得到 333 真实 IP 地址 192.168.1.12，然后扫描整个 C 段，当扫到 192.168.1.10 这个 IP 时发现一个 title 同为 “90sec 社区” 的网站，域名也是 111.test.com，这样就能确定 192.168.1.10 为真实 IP 了。

| 

网站域名

 | 

域名解析 IP

 | 

CDN 节点 IP

 |
| 

111.test.com（目标）

 | 

192.168.1.10

 | 

8.8.8.8

 |
| 

222.test.com

 | 

192.168.1.11

 | 

9.9.9.9

 |
| 

333.test.com

 | 

192.168.1.12

 | 

没有 CDN

 |

**(8) 自建 CDN 节点服务器找到真实 IP**

这篇笔记当时没有记录下来，其实就是 MS17-010 刚出来时很多机器都还没打补丁，在批量过程中打了一台别人自建的 CDN 节点服务器，然后在里边发现很多解析到这边的 IP 地址，其实这些 IP 地址就是某些网站的真实 IP，所以这也算是一种思路吧，但是得先拿到 CDN 节点服务器权限。或者可以通过 DDOS 攻击方式将其流量耗尽后即会显示真实 IP，因为免费和自建 CDN 的流量都不会很多。  

**(9) 通过目标网站的漏洞找到真实 IP**

Web 安全漏洞：XSS、SSRF、命令执行、文件上传等，但可能需要先绕过云 WAF 安全防护。

敏感信息泄露：Apache status、Jboss status、SVN、Github 等敏感信息和网页源代码泄露。

**(10) 通过社工 CDN 控制台找到真实 IP**  

通过社会工程学将搜集到的信息组合生成用户名和密码字典对 CDN 控制台进行爆破或者手工尝试，但是得在没有验证码和登录次数限制的情况下，然后找到他的真实解析 IP 地址。

**(11) Zmap 全网扫描及 F5 LTM 解码法**

这两种方法都是前辈们以前写的，个人感觉较为复杂，并没有亲自实践过，不知是否真的可行？  

**注意事项：**

部署 CDN 的网站有必要设置严格访问控制策略，仅允许 CDN 节点访问网站真实服务器 80 端口，这样设置的好处就是即使在 hosts 文件中绑定了真实 IP 后仍然无法访问。

笔者曾经在一次渗透测试过程中就遇到过类似情况，就是成功绑定了真实 IP 后，虽然能够正常访问到目标网站，但是仍然没有绕过云 WAF，具体情况有点记不太清了，当时没有去细研究这个问题！

潇湘信安 发起了一个读者讨论 有没有表哥补充下自己用过的其他方法？ 精选讨论内容

有篇文章写过，思路是可行的，就是比较耗时！

余下 3 条讨论内容

借这次知识星球的官方活动推下我的个人星球，里边没有干货文章，也没有各种 0day/Exp，只有自己的临时笔记和优质资源分享，考虑好后再决定是否加入！！！  

 **星球活动：**

1.  20 张 30 元 “潇湘信安” 优惠券，与知识星球官方活动一起 “食用” 更佳！（潇湘信安活动）
    
2.  新用户和续费用户均可享受手续费最高 10% 补贴，额度有限，先到先得！（知识星球活动）
    

 **活动时间：**2020 年 11 月 6 日 0 点 - 14 日 24 点（9 天）

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfqE3rrpOMO9arvGibmJOjnU5RM0vNic03SLkqb37ticH3NAiauaSluzpx882lAeHyiadzTWxglclPIATg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRgjicUHG1ssz8JfRYaI9HSKjVfEfibFkKzsJPZ4GCaiaymLRrmXjRqD8ag/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)  如果对你有所帮助，点个分享、赞、在看呗！![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)