> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/4GCIUyK-EJm3spLsbMZ9Zg)

_**声明**_

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测以及文章作者不为此承担任何责任。  
雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_**No.1  
**_

_**信息收集**_

**1． 搜索局域网中的靶机，这里的靶机 IP 为 192.168.168.104**

a)arp-scan -l 探测局域网中存活主  

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJl01n1Z6gvomgOQWPIhkUnicic7BOrdEX1UicQkO4FQvPXQmldWXuaXITw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJ0Zv0aGlqLPR6GzId68Yj3DxSicIRzqWjfQF3pTw5kQfKa7nJPtxY1Qw/640?wx_fmt=png)

b）nmap 192.168.68.0/24(与攻击机相同的网段)  

**2.nmap 扫描端口**

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJNwib8s2DuXDbOevXDzwycfexVqlTAic8TrAYkyyE1DUf6LkG4nXibLZDA/640?wx_fmt=png)

利用 - A 参数获取详细信息  

**3. 发现 80 端口，dirsearch 扫描敏感目录**

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJmN74RbVhfdkasicg27R9rgpFcvKTBibeCYgvdQefOE8xxMucI2AibpOWA/640?wx_fmt=png)

_**No.2  
**_

_**漏洞查找与利用**_

  

**利用 nmap 获得的开放端口查看端口处是否存在漏洞**

a) 21 端口

i. Nmap-A 扫描得出，21 端口任意访问

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJUR5WtZI3bh9vpibggCS8bDHDH9SXCgjRL2oN1rqxNLSswLSd6hsmmiaA/640?wx_fmt=png)

ii. 暂未发现敏感文件

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJazBhcUNoE3DhHDODswsMueEFD59Y1vxgQ1fMsiaj9HbzoWaYO8YoXVg/640?wx_fmt=png)

b) 22 端口：openssh 的版本号为 6.6.1p 存在用户名枚举漏洞  
i. searchspolite 查看是否存在 poc 脚本

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJfEmGVV2zQ61lnG3f96znxs5MLYJKOib0xiaf1NicdvxV8mHibMt22hC6Rw/640?wx_fmt=png)

ii. 利用 cewl 在 web 页面爬取可能的用户名，同时加入常用的 username 字典

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJWh8dsWI0x1yIMdvn0CUjmgMib3t3k6N1F8c8Er0qdKrdMnamX3ibzjiaA/640?wx_fmt=png)

iii. 使用枚举用户名脚本枚举用户名

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJgVYEL91z1AibkvMHCpibkgxqqKTxBpicjv1jtH8cCZav8acOR9u93DRsA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJROibQ3DTgKE9hezq0EricI1d8bdE5icd9rq8Y4MuPGlOzRib9CV4ew9WDw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJfKtnkQOcU944tTwzHLcH2Mdc0Bm0jO7WN1jxjScvw0Va3wib8Q7tGrg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJx16eD1MbnQ3nguuhzaAXIsBHaaIicWnwH2pTSHD9cc6K1nXgWJ9s4rA/640?wx_fmt=png)

iv. 使用 hydra 破解密码 ，密码为 metallica

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJwxt4qu96feSghIemsicZkWjleK0fcuJmZ9n1dmbAPr9LAIOnkSuZGlQ/640?wx_fmt=png)

c) 80 端口: dirsearch 扫描后台获取敏感目录

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJmN74RbVhfdkasicg27R9rgpFcvKTBibeCYgvdQefOE8xxMucI2AibpOWA/640?wx_fmt=png)

i. /cms

① 发现是 LotusCMS 框架，利用 searchsploit 看有无漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJkMNB5ekaAA8ps6icHJ695YibiaHO0F9md1rsANERWiaVnb5DhHhmkY7ZKg/640?wx_fmt=png)

② 利用 msf, 尝试 getshell

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJns7QrDnbX31UrHWcF9hibuibThctTlcLSNHzU3VoORe7iaH1hqnibzbkSA/640?wx_fmt=png)

③ 成功 getshell

ii. 查看 / robots.txt

① 发现 / mongoadmin / 目录

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJn2uZ5lvykmCwBLnLI2DTGWlLkohz8HgXH1hrCewiam5ET7DYKPyNYpw/640?wx_fmt=png)

② 发现 phpadmin 的数据库管理页面，获得账号密码

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJQ2AOialibOWicJf5vNzGwbDIyfFE7SNVa3MPEp5DehZWZqSdIPmug0MVw/640?wx_fmt=png)

iii. 查看 / drupal

① 发现是 drupal 框架的页面，利用 wappalyzer 查看网页指纹，发现 drupal 版本为 8

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJRWxSKnZ698Zriaqks6TthsjLyDFyXCGLmzClMGhuvygTyrsjEFubLEQ/640?wx_fmt=png)

② 利用 searchspolite 查看，有无可利用的脚本

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJaOClqW40jSV50WiagbHiayiaqtuDcjsGThH6AE2dWInj0ian2c2iblu1iaGw/640?wx_fmt=png)

③ msfconsole 利用，getshell

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJibMvuVibrZUA5aNvXyDgXyr0mic9d4RV1sV0Feics2K9QuIqDOnzyXhaPA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJ0T2nPCuHePSF8icFcgbEQ6hl7dRsnEjHzozhib5W5jL9BZjFRQuw8wPQ/640?wx_fmt=png)

_**No.3  
**_

_**提权**_

**1.sudo 提权**  
a) 利用 admin, metallica 登录  
b) Sudo –l 查看 sudo 支持的命令

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJfHkFszicswDYUJyzMiakk4icZIueMqWIRGeXD1G6u6BKg7dlM22TDTV2A/640?wx_fmt=png)

c) 发现支持命令为 ALL, 直接 sudo –i 提权

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJtDWtCX1DCxSxEfMrBkBTwTh9kCb9V9Vqf1zMHXibNTibibEnLyv7KEKsg/640?wx_fmt=png)

**2. 内核提权**  
a) 查看当前系统信息

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJ2lydln7aiafWJFFN7eqVPAUp7SLsds2pRTV4cxJ0Nm7kjPpq7OGt1mA/640?wx_fmt=png)

b) 在 msf 上查找是否存在当前内核版本的漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJdssfjhEcwCmCjEKjMSqybY3B5ZjvqcnvXFpVFVWkZhtQ3xfxxvbL9g/640?wx_fmt=png)

c) 编译

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJSWkRYQiaaicHghLl5icBPxTl23wZHZcZvCsI2WDCM7qfvTWCp6KHemibww/640?wx_fmt=png)

d) 在服务器上搭建简单的 http 服务，在被控靶机上使用 wget 获取文件

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJKLb9zV4uzUVOS4bibSBAAcAiclfhXT6mK6dv7Bichrd3rFLj65DibEibtMQ/640?wx_fmt=png)

e) 提权成功

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJ7HcTxvRZmWJ4sT2a1JTC4KGk6BLovugNiciasUtmQllxnbRWP0C4SLKg/640?wx_fmt=png)

_**招聘启事**_

  

安恒雷神众测 SRC 运营（实习生）  
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

设计师（实习生）

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
3、有品牌传播、产品设计或新媒体视觉工作经历；  
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
岗位：Web 安全 安全研究员  
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

岗位：安全红队武器自动化工程师  
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

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJcTib286GQcKicWTGz6ayWdjqYrzq36VzSq6TnRORY3GKoHntMQ2LBkKg/640?wx_fmt=jpeg)

专注渗透测试技术

全球最新网络攻击技术

END

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JWUFSUTshk23sjjpXhJrMu2z6MIL9pdkYkm0wicXRrgNLWvr04znZtqs8wexe5qbZxyOzRerwpSotg/640?wx_fmt=jpeg)