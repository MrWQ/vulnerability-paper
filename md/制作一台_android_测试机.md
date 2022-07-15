> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Rqx21iSP7FyjdoBQjC2q4A)

**STATEMENT**

**声明**

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测及文章作者不为此承担任何责任。

雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

**NO.1 前言**

刷机用到的工具：win10 电脑 + pixel 1 手机 + sailfish+ Magisk+ twrp  
初始版本 Android 8.0.0

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSvw7TFOJ2uvdx5HswlicatkveLvgp3XTaSOOLT7nNwAZHyaZqBbZOgsw/640?wx_fmt=png)

官网刷机包地址：

https://developers.google.com/android/images

选择自己想要的 android 版本，我这边选择的是 8.1.0 (OPM1.171019.011, Dec 2017) 版本，点击 link 进行下载

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzS1kBTLf74eITiaSp9eiazgmNicichhwkwp6F1JxI6zVpv4NmMXIv37GUicyQ/640?wx_fmt=png)

下载并解压后的刷机包

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSgF7aK3JcsDgePP0rCBL4VfGPLJiaqx1rzapFPGVDMZqRoImxCW7A8mg/640?wx_fmt=png)

**NO.2 官方刷机教程**

谷歌官方的提供的在 Windows 平台的刷机教程比较简单：手机（移动设备）与电脑以 USB 数据线连接正常，只需关闭手机设备，手机设备进入 Fastboot Mode 模式（在手机完全关机的情况下，先按住音量向下键再按住开机键即可进入），然后在电脑上运行刷机脚本 flash-all.bat 就可以开始刷机之旅了，在刷机的过程中不要随意拔掉 USB 数据连接线，静静的等待刷机完成 -- 提示脚本运行成功，点击任意键手机设备重启，刷机成功。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSzumI3Tj9k4JcHWd8rsJzrmY7bWRzwmQSN8Dk8LtFS61CdMb93WGccw/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzS6iaUibQiavZ2Qytzj8w1QiazLrYCaXMUpia6CyiadP7LFZlm6k8ibHRnFz1KA/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSLzoQpzwY0Wj5YSkicPC9FkuZa4xAgg2V3vGev7zwR4ezbDzRiaZLgewg/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSsgaIZKWEJ7JHlyRK5A7vtnYcMNnwRc4KhLtrScTXFEC5lJbsCFxD6g/640?wx_fmt=png)

**NO.3 如何 root 测试机**

我选择使用的是 TWRP  
官方下载地址：https://twrp.me/  
TWRP 是国外 android 爱好者开发的一款工具，全名是：TeamWin Recovery Project。TWRP 的主要作用包括刷机（cm7、cm9、miui 等），备份，恢复等。修复的时候 TWRP 是必不可少的工具。是一款知名第三方 recovery 刷机工具，功能强大，支持触屏操作。  
选择 device 搜索我们刷入的手机型号

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSYMPiaeicqIu3t0ibBl0cNyV740q5pdpkicib4GmyBKUODvGSUPM7C8HUCXg/640?wx_fmt=png)

选择 Primary (Americas)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSGO1A4XsANtJdgA5SeicicSyaX4cuVxWgJs51iaqUO9zjOeWMFufMMRTcw/640?wx_fmt=png)

我这边选择下载的是 Download twrp-3.3.0-0-sailfish.img 版本

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSlqgIo2Vias3YwmWtorgonicQgNjbGVX8iasIkcQqytTNNBjxeqiaPV1pkQ/640?wx_fmt=png)

下载 Magisk ：

https://github.com/topjohnwu/Magisk/releases  
Magisk 是一套用于定制 Android 的开源工具，支持高于 Android 4.2 的设备。它涵盖了 Android 定制的基本部分：root、引导脚本、SELinux 修补、移除 AVB2.0 / dm-verity / 强制加密等。  

两个工具都下载完成后我们进行 root，首先将 Magisk-v21.4.zip push 到手机的 sd 卡中  

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSSmFiaO6QX17zBWI4y9KQQno5N6H7iblfDpF4icsLI805qiaVc97ibxpZJHQ/640?wx_fmt=png)

接下来进入 Fastboot Mode 模式，刷入 twrp-3.3.0-0-sailfish.img，推送进入后请立刻拔掉 usb 线

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzS1hxrWR5uk2yZWrQgmDKQ6od5EfGNqaF72v4R0aFLvqIGepxqf9EhkQ/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSc6DQVzialSpdk9Oo8qa1Cw73aJkQ30f2TngdWVdfIFos8fLTmynGsxg/640?wx_fmt=png)

选择 install，选择我们 push 的 Magisk-v21.4.zip，最后重启系统

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSCWvICzaaKlZD8jfA0mDrm0bmO5ib7s0drAlf6YxLAHIeVO71sl2uf9Q/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSz3IEZjEoTRZ6GoDsib0hjjWhjsWpaCokxIY1WLkMDvxzU65icdTH6kOQ/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzS3Yp98VMQGElubZquDAYylnwlcMCZgvfWiaknepHYHKueFG8I5SZzbMA/640?wx_fmt=png)

至此完成整个刷机流程，尝试 adb shell 连接手机，能 su 进入 root 模式说明成功。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSXRaB4qINvuNbCxK9tuyIQCicchxXk7ibibnzh4urKWZEWbVFibJOFRuiccA/640?wx_fmt=png)

**NO.4 遇到的问题**

新刷的手机打开连接无线网会有 “已连接，但无法访问互联网” 开机后 wifi 有感叹号, 时间无法同步，导致无法上网的问题  
**解决办法：**  
在手机的 shell 里以 root 用户执行：

**settings put global captive_portal_http_url** 

**https://www.google.cn/generate_204**

**settings put global captive_portal_https_url** 

**https://www.google.cn/generate_204**

**settings put global ntp_server 1.hk.pool.ntp.org**

**reboot**

之后可以安装一些平时用到的抓包工具，先安装 Xposed，下载安装后重启设备

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzS48pMibgjLrW75wvF3T5DzF5Bu2jDlaE4M8Ua1zibwlVNeibMEzncoK0zw/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSEwF3zgV3GVQO3yeOWoicGZvxf5wS5pl8GyoXQkiaI4Cgy6FeDI0aCSJQ/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzS7bUewAiaJMzz3QVF4XuuP8vbFibD8KiaZAPUZUOibu3WKVLRap0miaMvLxw/640?wx_fmt=png)

Xposed 安装成功后，安装一些抓包用的模块，重启手机后生效

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVhxHzr9NEoNClMT0vOcPzSBeYHpAaBMmQHpgEqcL0icocFhuIXoT1nPyWZvM8c1srseepGWnRmLPQ/640?wx_fmt=png)

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

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JXvfaMY5ZXX5gb052XAfZ3JMtlHBexoN9Y3JQIEYib0sJZEavMzAbvpxLSRZgpUw6v1W9fEMBcB6iaw/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/0BNKhibhMh8eiasiaBAEsmWfxYRZOZdgDBevusQUZzjTCG5QB8B4wgy8TSMiapKsHymVU4PnYYPrSgtQLwArW5QMUA/640?wx_fmt=gif)

**长按识别二维码关注我们**