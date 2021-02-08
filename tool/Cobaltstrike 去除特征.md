> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/YKYtDPH6LFgp8_whbHDreg)

> 本文作者：**BlackCat**（Ms08067 实验室内网小组成员）

**前言：**

红蓝对抗的时候，如果未修改 CS 特征、容易被蓝队溯源。

**去特征的几种方法：**

**1、更改默认端口** 

**方法一、直接编辑 teamserver 进行启动项修改。**

vi teamserver

**方法二、启动时候指定 server_port**

java -XX:ParallelGCThreads=4 -Duser.language=en -Dcobaltstrike.server_port=50505 -Djavax.net.ssl.keyStore=./cobaltstrike.store -Djavax.net.ssl.keyStorePassword=123456 -server -XX:+AggressiveHeap -XX:+UseParallelGC -Xmx1024m -classpath ./cobaltstrike.jar server.TeamServer xxx.xxx.xx.xx test google.profile

**2、去除证书特征**

（1）、进入 CS 目录

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzangwIyZNUw11kMgmMD3to1kgBQXB5fBKqs9fmyCuiaPHksR7FHgyIicg/640?wx_fmt=png)

查看 keytool -list -v -keystore cobaltstrike.store 证书情况，输入默认密码 123456 回车，可以看到所有者、发布者中 Cobalt Strike 相关字样。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzasE8TzicxXnB3INRM0fD9PIialBbE9a98ej7Y4nDfhucg05IAMEut3vg/640?wx_fmt=png)

然后修改 keytool

**keytool** 是一个 Java 数据证书的管理工具，使用如下：

*   -keytool -keystore cobaltstrike.store -storepass 密码
    
*   -keypass 密码
    
*   -genkey -keyalg RSA
    
*   -alias google.com -dname "CN=(名字与姓氏),
    
*   OU=(组织单位名称), O=(组织名称),
    
*   L=(城市或区域名称),
    
*   ST=(州或省份名称),
    
*   C=(单位的两字母国家代码)。
    

keytool -keystore cobaltstrike.store -storepass 123456 -keypass 123456 -genkey -keyalg RSA -alias taobao.com -dname "CN=US, OU=”taobao.com“, O=“Sofatest”, L=Beijing, ST=Cyberspace, C=CN"

然后 在观测 keytool。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzdzMgriaEMr1uyfZ8gJLCVt5KXqLWqM2iaJOIUr7GfDiciaibWNsbtx4Qh4w/640?wx_fmt=png)

这时发现所以关于 cobaltstrike 的字眼都被替换掉了。

**3、绕过流量审计**

**（1）高信誉服务伪造**

传输过程中，把流量伪造成高信誉的网站，比如 Google 、bing 等 。

现在的大多数硬件 WAF 防护设备都能检测出来 Cs 的流量特征，所以我们必须要修改 CS 的流量特征，CS 的流量由 malleable C2 配置来掌控的，所以我们需要定向去配置这个 C2。

Malleable C2 是一种特定领域的语言，主要用来控制 “Cobalt Strike Beacon” 攻击载荷中的网络指针。

malleable C2 详细知识参考：

https://bluescreenofjeff.com/2017-01-24-how-to-write-malleable-c2-profiles-for-cobalt-strike/

去配置之前先了解下有关 Beacon 的通信基础：

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzia2lQDrYy3I5tQbznqAYibhvB3S9g4PUibKb3MCJqzDOwj8TNxp2tDHuQ/640?wx_fmt=png)

从 Cobalt Strike 3.6 版开始，可以将 HTTP 动词从 POST 更改为 GET。Beacon 忽略了此 POST 请求（配置文件中的 _http-post_ 服务器）的响应。默认情况下，Beacon 将 HTTP POST 请求用于上述步骤＃3 和＃4。根据您的目标环境或您正在模拟的流量，可能会注意到交替的 GET 和 POST 请求。在这种情况下，请将 _http-post_ 部分的动词设置为 GET。

**Beacon 与 teamserver 端 c2 的通信逻辑：**

1.stager 的 beacon 会先下载完整的 payload 执行  
2.beacon 进入睡眠状态，结束睡眠状态后用 http-get 方式 发送一个 metadata(具体发送细节可以在 malleable_profie 文件里的 http-get 模块进行自定义),metadata 内容大概是目标系统的版本，当前用户等信息给 teamserver 端 。如图的  1）  
3. 如果存在待执行的任务，则 teamserver 上的 c2 会响应这个 metadata 发布命令。beacon 将会收到具体会话内容与一个任务 id。  
4. 执行完毕后 beacon 将回显数据与任务 id 用 post 方式发送回 team server 端的 C2(细节可以在 malleable_profile 文件中的 http-post 部分进行自定义)，然后又会回到睡眠状态。

参考资料  
https://www.chabug.org/web/832.html

许多 Beacon 指标由一个 C2 拓展文件控制。一个 C2 拓展文件由设置和数据转换组成。数据转换是一 个简单的程序，它指定如何转换数据并将其存储在事务中。转换和存储数据的同一程序，向后解释，还 从事务中提取和恢复数据。

**配置文件语言：**

创建配置文件的最佳方法是修改现有的配置文件。

Malleable 配置文件下载：

git clone https://github.com/rsmudge/Malleable-C2-Profiles.git

CS 中集成了一个包含在 Linux 平台下的 C2lint 工具，下面是检测这段代码是否存在问题：

CD CobaltStrike

chmod 777 c2lint

./c2lint [/path/to/my.profile]   #这个路径是 Malleable 的配置文件路径

./c2lint /Users/blackcat/Desktop / 资源 / CS 学习 / Malleable-C2-Profiles/APT/havex.profile

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOz5bWD7Psp1S0Pp6uaIPFoMF8lWBM7hibTztsVNpy5IhiavJ8Ec8n1naLw/640?wx_fmt=png)

绿色为运行成功，黄色的为警告，红色的 error 为运行失败。

这里是运行成功；  

然后我们要修改里面的参数 思路就是，默认值坚决不使用，具体如下：

set sample_name "AL";      # 配置文件名称：

set sleeptime "50000";       #设置 sleep 时间，单位是毫秒

set useragent "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 5.2) Java/1.5.0_08";   #这个一般结合实战环境去配置，从目标机构中捕获一个真实的 user-agent 值并且插入到真实的流量中。

例如，可以向目标机构成员发送一封带有 web 漏洞的电子邮件并监视后续 GET 请求中发送的 user-agent 值。如果你使用的是明文的 HTTP 流量或者是目标环境中存在 SSL 拦截，那么与环境不匹配的 User-Agent 值就会被防御者发现。

再往下的代码是 http 部分。

这里分块来说明下。

http-get 模块：

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOznibSalUG7IfaJ9HS7rK8r3Kwmiaa1EbsiaSEhoicN7PiczfDnteibCcB5qGA/640?wx_fmt=png)

如上图所示。设定了 victim 的 beacon 发送给 c2 的 metadata 的相关配置。

  
1. 在 client 部分中，先设置了多个 http header 头，然后在 uri 中存储一个参数。把 Referer 伪造成 Google  
2. 然后又设置了在 metadata 数据在传输的时候，先 base64 加密然后将所有的值填写在 Cookie 字段中。  
3. 在 server 部分，先设置多个 header 头。然后更改相应内容然后 base64 编码，然后把数据放在在 body 里。

http-post 模块：

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOznBT8Kqh7EnqK9SbKM6QZGO40Hib3rCCtGr0sCKatchX02SiaawLcRTMw/640?wx_fmt=png)

先说下 Clinet 模块：

这里面的 id 代表的是 task id，任务执行后，beacon 需要利用 post 方式来与 c2 进行通信，需要传送一个唯一的 task id 值，还需要传送回显。例如 ipconfig 命令，就会传送命令的结果等。上面的 header 头就跟之前的 header 头的用途一致。

client 中的 output 代表的是客户端发送给服务端的响应用什么形式发送，

server 部分跟 client 比较类似所以不做太多讲述。

此处可以通过定制 C2 的配置，使得 C2 的流量混合在目标环境流量中，伪装为正常应用流量，达到欺骗的作用。

我这里伪造的是 Google 的流量，

然后运行这个 C2 配置文件：

服务端：

sudo ./teamserver 192.168.1.55 Malleable-C2-Profiles/APT/havex.profile

客户端：

./start.sh

然后连接后，点击 Cobalt Strike -- Listeners 创建一个监听模块。然后通过这个监听模块创建一个后门文件 ，然后去上线一台机器。

我这里靶机地址：192.168.93.128

然后点击 Attacks-- packages   --  Windows Executable

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzlic1sectOEMOZUe2jWtsjVibOl0rmJlHibJu6lI9VD5K8ujZF5IewCpKQ/640?wx_fmt=png)

生成一个 Windows 后门可执行文件 EXE。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzeQkkebTayg2UZaD8WRSqIY3icMp9bHPzxicCMniay0UeibnWCZ045NweiaQ/640?wx_fmt=png)

然后把这个后门放到靶机里使其上线。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzWNrYUncvpHWxyibK4FNGmPibHY4iahibmAL5H4dlvia5xj76ttJrVic36lOw/640?wx_fmt=png)

然后；

打开 wireshark，然后开启抓包

这里要做下筛选：

http and tcp.port == 80 #我这里 CS 监听端口是 80 可以根据自己需求定制

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOz9wd2nO40lBBj2utoictkroJ9jUhXSQJw1FLLfdkVXXJCJIdZLVtUwAA/640?wx_fmt=png)

然后  进入到被控机的 beacon 模式下。

执行命令 shell  dir

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzEpthibPWQ3zjJIbbnPEfdVGsh50UJqkebglkicqzg4icI4WCrGSYNnPzQ/640?wx_fmt=png)

然后发现已经抓取到包，查看下包的内容。

右键选定 ---  follow --- TCP Tream

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzghGyzosTNxB3Tw4XBDIIF4TEd3ia9ODsuSXFNvpmTHMbJ8bvAiahyXjg/640?wx_fmt=png)

此时发现 Referer 为 Google 证明实验成功，成功伪造流量。

下面的是基于 JQuery 的配置文件作为基础配  

下载：

git clone https://github.com/threatexpress/malleable-c2.git

然后运行语法：

./c2lint [/path/to/my.profile]   #这个路径是 Malleable 的配置文件路径

我这里用的是 CS4.0，所以选用这个 profile

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOz7MCN3WcqL58eXIQS1UGGNIwYNko040hibia7Y2Y4MiaAL7G7MbxwNGyGw/640?wx_fmt=png)

然后配置文件信息

参考前面的**配置文件名称，sleep 时间、用户代理**，同上 user-agent 还是使用目标机的真实的 user-agent 值。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOz8YHTOaQ2j1rD9QTB7Vz0cpNYamlJVUDP7eoewia5xfghwgHtRG5U1Wg/640?wx_fmt=png)

**SSL 证书设置 ：**

此设置控制用于 HTTPS 通信的 SSL 证书。如果可能的话，请为你正在使用的域使用真实的，正确发布的 SSL 证书。LetsEncrypt 可以发布所有主要操作系统和浏览器都信任的免费 SSL 证书，并且会让防御者更难以检查 Beacon 流量。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzAIbp2lUa8ibicdiaXjf7mZWbCiaax9BnFYEPydCpKqHRGpjWfV5NtFICcw/640?wx_fmt=png)

**SpawnTo 过程 ：**

spawnto 设置控制 beacon 生成的进程以便后渗透利用工作，以及何时使用 spawn 命令。该命令也可以使用命令行参数。

set %windir%\\sysnative\\svchost.exe -k localservice -p -s fdPHost

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOz9Q1ZH8IJ5Raw60HiaLTsicksHyv4BuYxAHLRQVJZq1338b6zUjADIgVw/640?wx_fmt=png)

svchost.exe 是微软 Windows 操作系统中的系统文件，微软官方对它的解释是：svchost.exe 是从动态链接库 (DLL) 中运行的服务的通用主机进程名称。这个程序对系统的正常运行是非常重要，而且是不能被结束的。许多服务通过注入到该程序中启动，所以会有多个该文件的进程。

如果防御者查看正在运行进程的命令行，额外的参数可以帮助 Beacon 进一步混淆。但是很难找到与 spawnto 一起使用的最合适的选项。选择前要进行实验和测试。

**SMB 信标：**

SMB 信标使用命名管道通过父信标进行通信。这允许在同一主机或网络上的信标之间进行点对点通信。可以配置 SMB 信标的管道名称。不要使用默认设置，因为一些防御性产品会查找这些默认设置。选择能够混合到目标环境的内容。  
关于 SMB 信标的更多能容，请访问：  
https://www.cobaltstrike.com/help-smb-beacon

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzBVzTMrhZKrpo9miasibInbia3Fg5l3lTibXQ6CxuciaxHOIa3515YoGfOsw/640?wx_fmt=png)

**DNS 信标**

DNS 信标使用 DNS 进行全部或部分通信。根据目标环境的防御技术，DNS 流量很容易就能被检测到，但通常是防御者的盲点。DNS 最适合用作低速和慢速备份通道。更改默认设置以更好地适应你遇到的环境。

  
有关 DNS 信标的更多信息，请访问如下链接：  
https://www.cobaltstrike.com/help-dns-beacon

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzwzQPMUwtYopgq3udNe6xia7ibJskIEyJ3VbcQTNjK1LpTbPh0xUhvpdQ/640?wx_fmt=png)

**分段过程（staging process）**

可以自定义信标分段过程。分段过程是用于完全加载信标的代码存根。  
了解有关 Beacon 分段过程的更多信息，

请阅读这篇文章：

https://blog.cobaltstrike.com/2013/06/28/staged-payloads-what-pen-testers-should-know/  
幸运的是，可以修改 Beacon stager 的 HTTP 特性。更改这些设置以模仿单个合法的 HTTP 请求 / 响应。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOz3yX1TUjVhwg9SC5XeTTmNNibwBNO9CFYPPgtT5riaROPicxehZ7p3zXpA/640?wx_fmt=png)

在此示例中，请求将发送到

/jquery-3.3.1.slim.min.js

或 / jquery-3.3.2.slim.min.js

（取决于目标进程体系结构），以开始分段过程。构建 HTTP 服务器参数以模仿 jQuery 请求。Beacon 命令和 payload 被混合到 jQuery javascript 文本块中。从 CDN 请求 jQuery 时，客户端发出一个合理的请求。

很多网站发出请求的实现方式如下：  

<script src =“jquery-3.3.1.min.js”> </ script>

可以将 URI 修改为类似其他 CDN 的形式。例如，你可以修改 http-stager，使其看起来好像是从 Microsoft jQuery CDN 中提取的。

<script src =“https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.min.js”> </script>

在某些情况下，使用 stageless payload 可能更好，因为分段过程可能会触发防御产品的报警。

**内存指示器**

一些最新的 Malleable C2 功能可以修改许多 Beacon 内存指示器。  
有关控制 Beacon 内存指示器的详细信息，请参阅下面链接：  
https://blog.cobaltstrike.com/2018/02/08/in-memory-evasion  
https://www.youtube.com/playlist?list=PL9HO6M_MU2nc5Q31qd2CwpZ8J4KFMhgnK  

此示例使用 peclone 工具从 explorer.exe 中提取内存元数据，另存为 Beaconpayload 的一部分，并且采用了 Raphael 发布的一篇博客 “In-Memory Evasion” 中的一些建议。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzM5ib1FUyQ2DOJJ839MgC5AjkJ5lFCyju0tVfbSK0y0tUMn8f9vDOqWQ/640?wx_fmt=png)

**http-get&http-post**

http-get 和 http-post 修改格式和上面基本类似

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzRPhiccYRVVVCibyaOugvxHgtFyYaicW46MG58ktiazuBKOs7vdRXK4CMrA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzwsiaqRibRUV5elR8SjLzrdevge2GCPt5F2l5mwL9vUCEEWygn9yDzXibw/640?wx_fmt=png)

这里  都是伪造成 jquery.com 的流量。

测试验证：

./c2lint c2lint jquery-c2.3.11.profile

Manual Testing(手工测试)  

除了使用 c2lint 进行测试外，还要在测试系统上手动测试 Beacon 的所有功能。

手动测试和验证的快速步骤

*   启动 wireshark
    
*   使用测试配置文件启动 teamserver
    

sudo ./teamserver 192.168.1.10 zaq123 jquery-c2.4.0profile

*   创建 HTTP 监听器（名为 http）
    
*   创建一个 Scripted Web Delivery 攻击来部署 HTTP 信标
    
*   Attacks - > Web Drive-by - >Scripted Web Delivery
    
*   在 Windows 测试系统上以管理员身份运行 PowerShell
    
*   查看数据包捕获数据以确保 http 流量符合你的预期
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOz24KA8aQhbeDKmsI512D0g2RtRKuybu4m03gOJGpAAekhaJ6pjgyKyg/640?wx_fmt=png)

这里检测没问题 流量特征都已经被修改。

还有一种 CDN 伪造技术 详细参考

https://paper.seebug.org/1349/#3cobalt-strike-dns_idle

参考：

CobalStrike 绕过流量审计：

https://paper.seebug.org/1349/

CobaltStrike」应用攻击手段实例分析：https://zhuanlan.zhihu.com/p/145505228

cobalt strike malleable C2 配置文件编写：https://blog.csdn.net/kongbaijun2000/article/details/109604547

深入研究 cobalt strike malleable C2 配置文件：https://xz.aliyun.com/t/2796

How to Write Malleable C2 Profiles for Cobalt Strike：https://bluescreenofjeff.com/2017-01-24-how-to-write-malleable-c2-profiles-for-cobalt-strike/

CobaltStrike 之 Malleable-C2-Profiles 配置：https://www.zzhsec.com/544.html

**学习更多文章，****加入内网小组，扫描二维码！**

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzKWkTtDU8iaQePhu5BbEibDolILr4Qrh9qa4f0xibBc0b9814Uiaq604kUQ/640?wx_fmt=png)

**扫描下方二维码邀请你进入内部微信群！**

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cniaUZzJeYAibE3v2VnNlhyC6fSTgtW94Pz51p0TSUl3AtZw0L1bDaAKw/640?wx_fmt=png) ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cT2rJYbRzsO9Q3J9rSltBVzts0O7USfFR8iaFOBwKdibX3hZiadoLRJIibA/640?wx_fmt=png)

 ![](https://mmbiz.qpic.cn/mmbiz_jpg/XWPpvP3nWaicjovru6mibAFRpVqK7ApHAwiaEGVqXtvB1YQahibp6eTIiaiap2SZPer1QXsKbNUNbnRbiaR4djJibmXAfQ/640?wx_fmt=jpeg)![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicJ39cBtzvcja8GibNMw6y6Amq7es7u8A8UcVds7Mpib8Tzu753K7IZ1WdZ66fDianO2evbG0lEAlJkg/640?wx_fmt=png)

**目前 30000 + 人已关注加入我们**

![](https://mmbiz.qpic.cn/mmbiz_gif/XWPpvP3nWa9FwrfJTzPRIyROZ2xwWyk6xuUY59uvYPCLokCc6iarKrkOWlEibeRI9DpFmlyNqA2OEuQhyaeYXzrw/640?wx_fmt=gif)