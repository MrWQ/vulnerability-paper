> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/tgQO9ILHudfkkOzeahICTg)

简介
--

weblogic 服务器的特点为架构庞大复杂，蓝队一般很难防御，且多部署于外网。而且 weblogic 的攻击成本比较低，只要存在漏洞，一般可以直接获取目标服务器的 root 权限。在 hw 中被各大攻击队，防守方重点关注。

当然，目前网上公开的各种 exp 程序，当然也包括我自己的工具，或多或少都有点问题。于是近期在朋友的要求下，整理了部分攻击方法以及” 完美 “利用。红队可以用来完善自己的工具，蓝队可以用来写溯源报告。

1. 探测 weblogic 是否存在漏洞
---------------------

目前网上公开的资料中，没有一种比较好的方法去判断 weblogic 是否存在漏洞。通常各类工具做法是用 exp 打一遍，如果成功了则自然存在漏洞，如果失败了则不存在漏洞。再或者，通过 dnslog 的方式去探测。这两种方法受限于各种因素，导致漏报误报的比例很高。还有可能触发蜜罐，waf 等等安全设备的规则。

当然在这里我介绍一种更简便的方式去查看是否存在漏洞，那就是利用 T3 RMI 的 CODEBASE 功能查看 weblogic 的黑名单 。

> codebase: 简单说，codebase 就是远程装载类的路径。当对象发送者序列化对象时，会在序列化流中附加上 codebase 的信息。这个信息告诉接收方到什么地方寻找该对象的执行代码。

那我们是不是可以发散一下思维，如果这个类是 weblogic 的黑名单类呢？？而且 weblogic 的 codebase 利用 http 协议去传输类。

利用方法如下，使用你的浏览器，确认好对方是 weblogic 服务器后，url 如下

> T3 反序列化的黑名单`http://xx:7001/bea_wls_internal/classes/weblogic/utils/io/oif/WebLogicFilterConfig.class`

> xmldecoder 黑名单`http://192.168.119.130:8088//bea_wls_internal/classes/weblogic/wsee/workarea/WorkContextXmlInputAdapter.class`

### 1.1 T3 codebase 分析

在`weblogic.rjvm.InternalWebAppListener#contextInitialized`处代码，注册处理 codebase 的代码，也就是请求路径为 classes

```
if (!server.isClasspathServletDisabled()) {            servletContext.addServlet("classes", "weblogic.servlet.ClasspathServlet").addMapping(new String[]{"/classes/*"});        }
```

下面我们来看一下 weblogic.servlet.ClasspathServlet 的处理代码，很简单，就是读取类名然后写入到 http 响应中。

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdGgXGuibZ56sAeSjVFPyWEw2puicFiapfMCHaBCaApNL04YEe1GAh9VVXJpXUIjV2byAmFzs6KGiarQDg/640?wx_fmt=png)image-20210329120233323

当然，这里是不是也存在任意文件读取漏洞呢？答案是的，只不过有一个黑名单，禁止某些后缀的文件被读取。黑名单列表如下

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdGgXGuibZ56sAeSjVFPyWEw2yiaVABJBoNCjVlDHyvIeZPjLvH8Iibs1RRK9EvmOtoGmicEvNgAicb9Pyg/640?wx_fmt=png)

image-20210329120332791

理论上讲，你也可以通过 CODEBASE 去读取用户的类下载到本地做代码分析。前提是你需要知道用户的类名是什么。当然，也有黑名单，黑名单如下

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdGgXGuibZ56sAeSjVFPyWEw2yiaVABJBoNCjVlDHyvIeZPjLvH8Iibs1RRK9EvmOtoGmicEvNgAicb9Pyg/640?wx_fmt=png)image-20210329120542711

2. weblogic xmldecoder 反序列化漏洞
-----------------------------

漏洞不做过多介绍，在这里不谈该漏洞的成因原理以及分析。

漏洞探测的 url

*   /wls-wsat/CoordinatorPortType
    
*   RegistrationPortTypeRPC
    
*   ParticipantPortType
    
*   RegistrationRequesterPortType
    
*   CoordinatorPortType11
    
*   RegistrationPortTypeRPC11
    
*   ParticipantPortType11
    
*   RegistrationRequesterPortType11
    

该漏洞利用的难点我认为有如下几个方面

1.  网上只有回显代码，没有利用代码，例如内存马
    
2.  写马的话，可能会遇到路径的问题。wenlogic 的路径为随机，目前网上公开的解决办法是爆破。
    
3.  怎么寻找所有的 Context？
    

下面我们来一一解决，以 weblogic 10.x 的 exp 为例

xmldecoder 的 xml payload 做了以下的工作

1.  调用 weblogic.utils.Hex.fromHexString 函数，将 hex 编码的 class 文件转换为二进制格式
    
2.  调用 org.mozilla.classfile.DefiningClassLoader 的 defineClass 方法，将上面的 class 文件加载到虚拟机中
    
3.  调用 newInstance 方法生成上面被添加至 JVM 的类的实例
    
4.  调用实例的方法以完成攻击
    

payload 其实你知道稍微看一下，就知道 xmldecoder 的写法，这里就不再赘述

上面所有的问题，其实都可以归结为一个问题，那就是怎么寻找 weblogic 下，所有 web 应用的上下文？

在这里我公开一个方法，该方法在 weblogic 10/12 下经过测试，且不受协议影响，也就是说，你只要能在 weblogic 里执行代码，我就可以获取 weblogic 所有的 webcontext。代码如下

```
java.lang.reflect.Method m = Class.forName("weblogic.t3.srvr.ServerRuntime").getDeclaredMethod("theOne");        m.setAccessible(true);        ServerRuntime serverRuntime = (ServerRuntime) m.invoke(null);        List<WebAppServletContext> list = new java.util.ArrayList();        StringBuilder sb = new StringBuilder();        for (weblogic.management.runtime.ApplicationRuntimeMBean applicationRuntime : serverRuntime.getApplicationRuntimes()) {            java.lang.reflect.Field childrenF = applicationRuntime.getClass().getSuperclass().getDeclaredField("children");            childrenF.setAccessible(true);            java.util.HashSet set = (java.util.HashSet) childrenF.get(applicationRuntime);            java.util.Iterator iterator = set.iterator();            while (iterator.hasNext()) {                Object key = iterator.next();                if (key.getClass().getName().equals("weblogic.servlet.internal.WebAppRuntimeMBeanImpl")) {                    Field contextF = key.getClass().getDeclaredField("context");                    contextF.setAccessible(true);                    WebAppServletContext context = (WebAppServletContext) contextF.get(key);                    list.add(context);                }            }        }        return list;
```

### 2.1 获取随机路径

利用上面的代码，获取到 weblogic 加载的所有的 web context 后，我们可以调用`context.getRootTempDir().getAbsolutePath()`方法去获取目录的位置，然后写入 webshell。

我的代码如下

```
List<WebAppServletContext> contexts = findAllContext();        Iterator<WebAppServletContext> i = contexts.iterator();        StringBuilder sb = new StringBuilder();        while (i.hasNext()) {            WebAppServletContext context = i.next();            sb.append(String.format("name %30s\turl %30s\tDocroot %s\n", context.getAppName(), context.getContextPath(), context.getRootTempDir().getAbsolutePath()));        }        return new ByteArrayInputStream((sb.toString()).getBytes());
```

截图如下![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdGgXGuibZ56sAeSjVFPyWEw2haDG71ugISwP1EFpgNAvHUlj7nwP29mCm4R8cIATPZatUDVoK48oLA/640?wx_fmt=png)

### 2.2 weblogic 12.x payload

weblogic 12.x 中，没有 org.mozilla.classfile.DefiningClassLoader 这个类，况且我也不太喜欢这种不灵活的方式去写 exp。在这里我换一种方式，那就是通过 java 调用 js。

从 JDK 1.8 开始，Nashorn 取代 Rhino(JDK 1.6, JDK1.7) 成为 Java 的嵌入式 JavaScript 引擎。Nashorn 完全支持 ECMAScript 5.1 规范以及一些扩展。它使用基于 JSR 292 的新语言特性，其中包含在 JDK 7 中引入的 invokedynamic，将 JavaScript 编译成 Java 字节码。

> 注意，不支持 1.5 以及 1.5 以下的 JVM

在 java 执行 js 时，可以调用任意 java 对象，方法，类。需要注意的是，java 是强类型语言，而 js 是弱类型语言，js 有的时候可能会代码意想不到的类型转换。这里需要注意

只需要将上面加载 context 的代码，改成 js 就可以，在这里我贴一张截图

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdGgXGuibZ56sAeSjVFPyWEw2QCNtpjqOvicYCwB8uPnr84Xc7Xkp9Sq6k2S5zLibcBoweyPWlY8jrCUw/640?wx_fmt=png)

> 在 nashorn 中，默认最后一个变量作为调用本次 js 的返回值

3. weblogic T3 反序列化
-------------------

在这里我推荐一下 r4v3zn 老哥的 weblogic-framework 利用工具， 。当然也有一点点 bug，不过这是一款非常好用的工具。工具地址 https://github.com/0nise/weblogic-framework

漏洞探测的话，参考前面的黑名单下载方式

当然，T3 反序列化中也有很多坑，例如 cve-2020-2555 等，无法做到类似于 CC 链的任意代码执行，目前同行的大部分做法是上传一个 jar 至 tmp 目录或者通过 urlclassloader 去远程加载 jar 包，部署恶意代码。

但是我们依旧可以通过反序列化的链式执行，调用 nashorn 的方式，间接做到任意代码执行。

而我们待执行的 js，通过反射调用 javaassist 包去组装一个 ClusterMasterRemote 类并绑定 JNDI 实例以作回显。js 代码如下

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdGgXGuibZ56sAeSjVFPyWEw2OL1WzuqSu1zicGrZLiaXCq9Gu8uVPGC02qM3ibcYqgJqAcVMSnna5MoTw/640?wx_fmt=png)image-20210329124530132

当然，corherence gadget 处需要修改成如下

```
private static ChainedExtractor getChainedExtractor() {        return new ChainedExtractor(new ReflectionExtractor[]{                new ReflectionExtractor(                        "newInstance", new Object[]{}                ),                new ReflectionExtractor(                        "getEngineByName", new Object[]{"nashorn"}                ),                new ReflectionExtractor(                        "eval", new Object[]{getJsCode()}                )        });    }
```

当然，如果您还是无法写出 payload，建议直接加入我们创建的知识星球，只需要 66 元。即支持我们工作，你又可以得到工具，何乐而不为呢。

我正在「宽字节安全」和朋友们讨论有趣的话题，你⼀起来吧？https://t.zsxq.com/qJe2JEi  

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdGgXGuibZ56sAeSjVFPyWEw25uaZEmwaGKmltLREfSVu5J7C9y8q7qg7GoGW5iapmeHKPoFY74Ha1fA/640?wx_fmt=png)