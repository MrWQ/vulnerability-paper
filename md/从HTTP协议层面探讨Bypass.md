\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzI0NzEwOTM0MA==&mid=2652484543&idx=1&sn=a5b4a8d7fa7627a01caea643a47cc4e3&chksm=f258100cc52f991aa13756c5f2a44a98491e680c35efc88d67158676996e2b384c2d7743ca60&mpshare=1&scene=1&srcid=1018Im16lvptonPYqtZDi3vW&sharer\_sharetime=1602995155511&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=4cf40c946f4d610ce40905a41132f104acbc7c396da4674b9af2b2c0573a17ae2b6f58870efd845017a271d81141b367d0b81ce01ec16b704e7829fa353d6f33598f766b6b981e62642fa007da9db317c4b09e012146f735632ac80e2eb07f62f2532cf9db86f0dbf6239cb603d7f6d4a1b4b17995385b121aceebcd1ea68c80&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=AbSo3SWPc8kZ5usebO3xHpw%3D&pass\_ticket=fNc1mNErgeHhn4jm0DcjBlD5hkXepEyD08VA%2B16wYw5QmvtETgayFa%2BrZuz3ot9i&wx\_header=0)

_**声明**_

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测以及文章作者不为此承担任何责任。  
  
雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_**No.1  
**_

_**什么是waf？**_

Web应用防护系统（也称为：网站应用级入侵防御系统。英文：Web Application Firewall，简称：WAF）。利用国际上公认的一种说法：Web应用防火墙是通过执行一系列针对HTTP/HTTPS的安全策略来专门为Web应用提供保护的一款产品。

_**No.2  
**_

_**waf为什么可以绕过？**_

1、性能的原因，为了增加性能，waf就没必要去检测一些无用的数据包。  
2、甲方为了waf不会使用，该开的不开，默认配置，一切无所谓，佛性甲方。  
3、厂商忽略了某些语言、中间件的特性。  
4、厂商的waf就是有问题。

_**No.3  
**_

_**常规绕waf的方式**_

大小写、转意、编码、坏字符等，都是对于一个输入内容的改变

_**No.4  
**_

_**HTTP特性绕过waf**_

**4.1pipeline绕过**  
HTTP Pipelining是这样一种技术：在等待上一个请求响应的同时，发送下一个请求。(译者注：作者这个解释并不完全正确，HTTP Pipelining其实是把多个HTTP请求放到一个TCP连接中一一发送，而在发送过程中不需要等待服务器对前一个请求的响应。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JWIbZsJQfYEOehPF1lPGPvDHxIAklhILN1wvTyIM0c5WziavN7mN5ic8TH83RadibILuobMzkDMdwIog/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

通过使用HTTP头 Connection: keep-alive 达到1次传输多个http包效果,Content-Length表示数据的长度，所以在使用的时候必须把bp的Content-Length自动更新关闭，然后在一个HTTP包嵌套多个数据包。当waf识别到第一个http请求，因为content-length字段标识了到此结束，waf为了性能，就不再检测这个数据包了，多夹带几个数据包，然后再把payload夹藏到某个数据包，达到一个bypass的过程。（数据包太多影响效率。）

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JWIbZsJQfYEOehPF1lPGPvDyRUE7icaZHHwnb1KbcibfQHC05z3ciaYUrWw0RIlBCWhdmaecl8znmKbg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**4.2HTTP分块传输**  
HTTP分块传输可以将数据分块，然后进行传输。从而达到绕过某些WAF的作用。操作方式很简单通过使用HTTP头 Transfer-Encoding: chunked 设置达到分割参数的效果。先看一下图片，再来谈谈分块的格式。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

其中数据中的第一个数字（16进制）表示当前分块的长度，下一个值表示数据内容。依次类推，末尾需要一个0以及两个回车，代表结束，整块拼接起来就是a=dbappsecurity。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这种方式，在定义分块长度处，添加；注释，从而达到一个混淆。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

burp有一个插件，支持一键编码。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

https://github.com/c0ny1/chunked-coding-converter/tree/master/src/main/java/burp  
**4.3协议未覆盖**  
以下四种常见的content-type类型，我们可以尝试互相替换尝试绕过WAF过滤机制。注：如图常见的绕过方式为使用 multipart/form-data 标签，并把name设为参数名内容写入注入语句

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

某些waf认为其是上传的过程，可以和4.2的内容进行组合拳利用，达到你根本肉眼看不出原本的内容。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**4.4利用Content-type编码绕过**  
一些特定的版本是可以，自定义编码方式的，然后在对数据进行编码，即可绕过。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**4.5HTTP头部问题**  
构造以下请求包，HOST为空。并在第二行加上HOST的值，发现是可以正常发送的，waf来说为了效率为题，这样错误的包就直接不检测，从而达到绕过目的

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**以上各种方法可以互相结合，各种各样的骚操作自行发挥**

  

  

  

_**招聘启事**_

安恒雷神众测SRC运营（实习生）  
————————  
【职责描述】  
1\.  负责SRC的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2\.  负责白帽子提交漏洞的漏洞审核、Rank评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3\.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4\.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5\.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

  

简历投递至 strategy@dbappsecurity.com.cn

  

设计师（实习生）

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
  
【职位要求】  
1、从事平面设计相关工作1年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；精通photoshop/illustrator/coreldrew/等设计制作软件；  
3、有品牌传播、产品设计或新媒体视觉工作经历；  
  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦19楼  
学历要求：本科及以上  
工作年限：1年及以上，条件优秀者可放宽

  

简历投递至 strategy@dbappsecurity.com.cn

安全招聘  
————————  
  
公司：安恒信息  
岗位：Web安全 安全研究员  
部门：战略支援部  
薪资：13-30K  
工作年限：1年+  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
  
【岗位职责】  
1.定期面向部门、全公司技术分享;  
2.前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3.负责完成部门渗透测试、红蓝对抗业务;  
4.负责自动化平台建设  
5.负责针对常见WAF产品规则进行测试并落地bypass方案  
  
【岗位要求】  
1.至少1年安全领域工作经验；  
2.熟悉HTTP协议相关技术  
3.拥有大型产品、CMS、厂商漏洞挖掘案例；  
4.熟练掌握php、java、asp.net代码审计基础（一种或多种）  
5.精通Web Fuzz模糊测试漏洞挖掘技术  
6.精通OWASP TOP 10安全漏洞原理并熟悉漏洞利用方法  
7.有过独立分析漏洞的经验，熟悉各种Web调试技巧  
8.熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
  
【加分项】  
1.具备良好的英语文档阅读能力；  
2.曾参加过技术沙龙担任嘉宾进行技术分享；  
3.具有CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP等安全相关资质者；  
4.具有大型SRC漏洞提交经验、获得年度表彰、大型CTF夺得名次者；  
5.开发过安全相关的开源项目；  
6.具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7.个人技术博客；  
8.在优质社区投稿过文章；

  

岗位：安全红队武器自动化工程师  
薪资：13-30K  
工作年限：2年+  
工作地点：杭州（总部）  
  
【岗位职责】  
1.负责红蓝对抗中的武器化落地与研究；  
2.平台化建设；  
3.安全研究落地。  
  
【岗位要求】  
1.熟练使用Python、java、c/c++等至少一门语言作为主要开发语言；  
2.熟练使用Django、flask 等常用web开发框架、以及熟练使用mysql、mongoDB、redis等数据存储方案；  
3:熟悉域安全以及内网横向渗透、常见web等漏洞原理；  
4.对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5.具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
  
【加分项】  
1.有高并发tcp服务、分布式等相关经验者优先；  
2.在github上有开源安全产品优先；  
3:有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4.在freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5.具备良好的英语文档阅读能力。

  

简历投递至 strategy@dbappsecurity.com.cn

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

专注渗透测试技术

全球最新网络攻击技术

END

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)