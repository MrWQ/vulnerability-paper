\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/XkSzwHv7-wGu8V39saqhCw)

背景
--

通常在渗透的过程中会遇到很多 Weblogic 服务器，但通过 IIOP 协议进行发送序列化恶意代码包时，会面临着无法建立通讯请求发送恶意序列化失败。最近参与了一场在成都举办的《FreeTalk 2020 成都站》，有幸分享了关于 Weblogic IIOP 协议 NAT 绕过的几种方式。

PPT 下载地址：https://img.zhiiyun.com/Weblogic\_IIOP\_NAT.pptx

成果演示
----

Goby  工具中关于 Weblogic 基本都是用了 IIOP 协议绕过的方案，比较有代表性的漏洞为 CVE-2020-2551 漏洞。

![](https://mmbiz.qpic.cn/mmbiz_gif/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ2iaFOGlWvTx58T8tCuZjUpsvKIDpib63gr2lskEwAibicdK10XteEn7veA/640?wx_fmt=gif)

内部工具 `weblogic-framework` 使用了多项核心技术来进行优雅的测试 Weblogic，其中也使用了 IIOP 协议的绕过方案。

![](https://mmbiz.qpic.cn/mmbiz_gif/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQBSDujq4PQu7WZuSQntZJEw3a0xhUZx4SJtqjNWCO0Wvia5AH2Uv2dDA/640?wx_fmt=gif)

协议
--

在开始之前，非常有比较提及一下以下这些协议相关的内容：

*   RMI：远程方法调用，本质上是 RPC 服务的 JAVA 实现，底层实现是 JRMP 协议，主要场景是分布式系统。
    
*   CORBA：跨语言（C ++、Java 等）的通信体系结构，通常在 IIOP 协议中使用。
    
*   GIOP：主要提供标准的传输语法以及 ORB 通信的信息格式标准。
    
*   IIOP：CORBA 对象之间交流的协议，GIOP 的实现。
    
*   RMI-IIOP：解决 RMI 和 CORBA/IIOP 无法同时使用的技术方案。
    
*   Weblogic IIOP：Weblogic 自实现的 RMI-IIOP。
    
*   T3：WebLogic Server 中的 RMI 通信使用 T3 协议传输 WebLogic Server 和其他 Java 程序，包括客户端及其他 WebLogic Server 实例之间 数据。
    

T3 协议本质上 RMI 中传输数据使用的协议，但通过上面我们看到 RMI-IIOP 是可以兼容 RMI 和 IIOP 的，所以在 Weblogic 中只要可以通过 T3 序列化恶意代码的都可以通过 IIOP 协议进行序列化，正是因为这种情况，我进入 Weblogic 第三季度深度贡献者名单。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQjVltugkibHuCdU5iazD1HjUzcd8NDcicXMn9Rz64yHLw6eLMKeSoicC60A/640?wx_fmt=png)

流程
--

### IIOP 序列化攻击流程

![](https://mmbiz.qpic.cn/mmbiz_jpg/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ6hwXJX8do3cL57zZG8cdonu13liaqWX7DVfePztIsT1dyStlsOQQbTg/640?wx_fmt=jpeg)

一般 IIOP 序列化攻击的大致流程主要为首先构建恶意序列化代码，然后初始化上下文实例，最后通过 `bind/rebind` 进行发送恶意序列化代码，下图为关键代码。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQuOS02kFMLWRga71p1bkYkeBE1LnP98sAYLGf58ia4vMrODiaz5wZoib9w/640?wx_fmt=png)

### IIOP 初始化上下文流程

初始化上下文通过攻击流程中的 `new InitialContext(env)` 进行构建，最终的入口点通过 `getInitialContext` 方法进行构建，最终是进行流入到 `InitialContextFactoryImpl.getInitialContext` 进行初始化上下文。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQx6q78f5Xab3zubcgX1BB4dOnQNFseITfxbEpL25QOwjRicXsL4ka82w/640?wx_fmt=png)

在流入 `InitialContextFactoryImpl.getInitialContext` 之后会通过 `obj = ORBHelper.getORBHelper().getORBReference` 来进行获取 `NameService`，然后将获取到的 `NameService` 进行实例化创建上下文实例，提供后续的执行操作。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQHny7xhhPdjQVWwibbYgoS1oHbZlMzAT89aWTv56K6Lq41kpEjRs7uHg/640?wx_fmt=png)

### rebind 流程

执行 `rebind` 流程中，首先会通过 `this.getContext` 方法进行获取前面所讲的上下对象，然后通过 `rebind_any` 进行发发送序列化代码，当前在此之前已经通过经过序列化的了。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ8hLzvwuZ2uJFS70JkKUcKFr1eCwubZx5H2nrQzVF2KfheLlG2yNLRg/640?wx_fmt=png)

在 `rebind_any` 中，首先会通过 `this._request` 进行发送 `rebind_any` 建立 Socket 通讯，最后通过 `this._invoke` 方法进行执行最终的操作发送序列化代码。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQzIJKjR8cguiatzEF3BGDUs2QrOFSDzScrgSjAULle78hrez0pUp1icCw/640?wx_fmt=png)

### 大致流程

所以最终大致的执行流程是如下图，获取 `NameService`，基于获取的信息进行创建上下文实例（获取实际连接信息），然后进行发起 `request` 请求，最后进行执行 `rebind_any` 操作。

![](https://mmbiz.qpic.cn/mmbiz_jpg/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQhUPfJoIMQAdQdWlo51sSnsxw6DmRhoV2KENp0aFuqAFQMbjjgV6Egw/640?wx_fmt=jpeg)

环境准备
----

*   Weblogic：12.1.3.0
    
*   协议：IIOP
    
*   漏洞编号：CVE-2020-2555
    
*   内网（Windows）：http://10.10.10.173:7001
    
*   NAT 网络（ vulfocus ） ：http://118.193.36.37:32769/  内部 IP：172.17.0.5
    

NAT 网络构建通过 `http://vulfocus.fofa.so/` 进行搭建构造。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQSKSdOYp5QX0NVwf0B3lbjSpkZ24Q2gwV6h5DCOR44hpAV4nQpvia7icw/640?wx_fmt=png)

成因
--

在后续的调试以及研究中我们所使用的版本为 12.1.3.0 版本，漏洞为 CVE-2020-2555 漏洞，以下为漏洞 POC，以及漏洞执行链，在这里不多讲该漏洞，有兴趣的可以移步漫谈 Weblogic CVE-2020-2555。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQrL4f6VJgr62PS3v3q2AxsNZLicyNImicicPG5kAXy8sFWGvUkPuTNAnfA/640?wx_fmt=png)

执行链：

```
ObjectInputStream.readObject()
    BadAttributeValueExpException.readObject()
        LimitFilter.toString()
            ChainedExtractor.extract()
                ReflectionExtractor.extract()
                    Method.invoke()
                        Class.getMethod()
                ReflectionExtractor.extract()
                    Method.invoke()
                        Runtime.getRuntime()
                ReflectionExtractor.extract()
                    Method.invoke()
                        Runtime.exec()
```

当我们可以与 Weblogic 所处同一网段并且可达的时，可以看到是成功执行系统命令弹出计算器。

![](https://mmbiz.qpic.cn/mmbiz_gif/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ1RGdtgWKxI6EngcnZ74memwYYwYNYhib976WlFenFFRcrVgIXx2LFNQ/640?wx_fmt=gif)

通过 Wireshark 进行抓包可以，可以看到一共通讯了 2 次，第一次发送 `LocateRequest` 类型的 `LocateRequest` 的通讯操作获取 `NameService`，第二次发送 `Request` 类型的 `rebind_any` 操作进行发送序列化代码。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQYh1licebmSSovVaH8PC2dDumX5hFN2FBL91vV63uZYeA4tibiaa27bZow/640?wx_fmt=png)

而进行测试公网中的靶机时抛出 `Operation time out` 异常，具体信息如下图。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQYJQYenOLZC6V41xWKHwS7VYobojusJ9DibE2bHuqwULOrx1oSXht3aA/640?wx_fmt=png)

而在 Wireshark 中可以看到，与第一次获取`NameService`中的内网 IP、端口进行了 Socket 通信。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQU0W6a6Vqd8icYpFGGSrrfvXjd8XyOtOXq8RYPS1T5GRiaKJicjcqhUWBg/640?wx_fmt=png)

而在执行的流程中停留在了 `createEndPoint` 方法中，所以通信问题大概率是在此方法中引发的。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQDD5HyibXWHw2Gtl619ticPwwQ9ExCMsv8gKhtJXZZpntXnqV4un5WImA/640?wx_fmt=png)

在 `createEndPoint` 方法中，最后通过 `MuxableSocketIIOP.createConnection` 方法进行建立 Socket 通信，此时的通信变为了 Weblogic 运行的内网 IP 和端口。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQPOvIw5cNeAPZ9NUCbOcd3Rrt5B3et80Enibah9HxoFzrM3fxE2OWBLQ/640?wx_fmt=png)

所以大体的情况为如下图，问题出现在发起 `request` 时调用的 `createEndPoint` 方法中，由于 `createEndPoint` 无法正常建立 Socket 通信导致后续的操作无法正常秩序。

![](https://mmbiz.qpic.cn/mmbiz_jpg/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQiaJAgMeVhX9vrResWzS4eSicql2UJvAiaPJ2WkrEzSBhia2mHs52Bv16Gg/640?wx_fmt=jpeg)

其实，我们也可以在 Weblogic 启动日志中也可以看到 Weblogic 关于端口和协议分配的情况，基本分配都是内网网卡的 IP 和端口同时会进行监听 `0.0.0.0:7001` 来处理协议的请求操作，那么现在问题来了，公网中的 Weblogic 服务器 99% 分配的都是内网 IP 和端口。

IIOP NAT 绕过方案
-------------

由于问题发生在响应的 Weblogic 在获取 NameService 时，响应的 IP 和端口为内网中的端口，导致在后续 `createEndPoint` 建立 Socket 通信，所以我们可以进行在建立 Socket 通信之前修改为正确的 IP 和端口（公网中的 IP 和端口）。

![](https://mmbiz.qpic.cn/mmbiz_jpg/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ2hb4NybwwG8Ex8QibxyYJ9wMXmPaY7cTkO1quIEa3OuMmsv97s7PFag/640?wx_fmt=jpeg)

### GIOP 协议极简实现

当我们与服务器所处同一网段时，可以看到一共通讯了 2 次，第一次发送 `LocateRequest` 类型的 `LocateRequest` 的通讯操作获取 `NameService`，第二次发送 `Request` 类型的 `rebind_any` 操作进行发送序列化代码。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQm1fxJrIxIlBgZ15qMOCOqyLHnHkKoZg47S1AXknLJSXxDvzoD4bFuQ/640?wx_fmt=png)

所以我们根据 Wireshark 中的信息，可以进行构建极简的 GIOP 实现，大体如下：

1.  请求 LocateRequest，获取 NameService 以及获取 key
    
2.  请求 Request，执行 rebind\_any 操作，发送序列化代码
    

#### GIOP 协议

GIOP 协议大致由 Header 和 Message Type 进行构成，在 Header 包含了 Magic、Version、Message Type、Message Size。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQUiaxZPPI2pOcc8c9gE2IUNmbG8MYjJ37nsQpibJyFcHEu6VD41Uevfkg/640?wx_fmt=png)

Message Type 的类型如下：

<table data-tool="mdnice编辑器"><thead><tr><th>消息类型</th><th>始发方</th></tr></thead><tbody><tr><td>Request</td><td>Client</td></tr><tr><td>Request</td><td>Server</td></tr><tr><td>CancelRequest</td><td>Client</td></tr><tr><td>LocateRequest</td><td>Client</td></tr><tr><td>LocateReply</td><td>Server</td></tr><tr><td>CloseConnection</td><td>Server</td></tr><tr><td>MessageError</td><td>Both</td></tr><tr><td>Fragment</td><td>Both</td></tr></tbody></table>

#### 实现

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQibD5qNwEuZz2X50WaO2J8ZWicAJmXhBz6Ikb2SjOoWuK67e6IkPMp79g/640?wx_fmt=png)

获取 NameService 请求代码实现：

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ6Wiapwjyh2TgrNCFRJgk6VJqxBbk9wIwZqYCqrloW560zvQbAT4lK5Q/640?wx_fmt=png)

执行 rebind\_any 操作代码实现：

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQMhDnp6tH55kPjgl0icFTQmSicOIfMibbtYdOahA0k6Z2ReAQPITolfEOQ/640?wx_fmt=png)

最终效果：

![](https://mmbiz.qpic.cn/mmbiz_gif/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQxI39gTDpgyjEGLcP7GGTpQhjZPpRicGiat741Vfb1gSUa3djDLbkxicxg/640?wx_fmt=gif)

### Javassist 字节码库

Javassist (JAVA programming ASSISTant) 是在 Java 中编辑字节码的类库，它使 Java 程序能够在运行时定义一个新类，并在 JVM 加载时修改类文件。

*   Javassist.CtClass 是类文件的抽象表示形式
    
*   Javassist.CtMethod 是类方法的抽象表示形式
    

读取类

```
ClassPool pool = ClassPool.getDefault(); 
CtClass cc = pool.get("test.Rectangle");
```

创建类

```
ClassPool pool = ClassPool.getDefault(); 
CtClass cc = pool.makeClass("Point");
```

继承

`cc.setSuperclass(pool.get("test.Point"));`

写入

```
cc.writeFile();
cc.toClass();
```

需要注意的是 `toClass()` 会把当前修改的 Class 加入到当前的 `ClassLoader` 中。

创建方法

```
ClassPool pool = ClassPool.getDefault(); 
CtClass cc = pool.makeClass("Point");
CtMethod ctMethod = new CtMethod(CtClass.voidType, "printName", new CtClass\[\]{}, cc);
```

修改方法

```
CtMethod ctMethod = ctClass.getDeclaredMethod("hello");
ctMethod.setBody("System.out.println(\\"set body\\");");
ctMethod.insertBefore("System.out.println(\\"set before\\");");
ctMethod.insertAfter("System.out.println(\\"set after\\");");
```

通过 Javassist 进行实现时，可以通过修改建立 Socket 通信之前的方法，将 ip、端口替换为正常的 IP 和端口，在这里选取的是 `newSocket` 方法，在第一个参数为 `host`，第二个参数为 `port`。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ0JUx3DPSxmDGfTRQsciahkQlr3PzRZpfha3iaibpe3NQsQSibAicQWQblhw/640?wx_fmt=png)

最终修改的如下图：

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQUhtVda3W1146uyiaqrJjYmnRtY9OmvibuzfNhAQS7XiaefaX3F8OZ4O9A/640?wx_fmt=png)

#### 实现

在实现的过程中，仅需要在执行到 `newSocket` 方法时，将连接到 IP 和端口设置为正确的 IP 和 端口，核心代码如下图：

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ2wVxMEGVVFELO6ic8nyDkT3bDFF8fiaeYvIHCiaqdzQfsZNpjQ5GGe6icg/640?wx_fmt=png)

最终效果：

![](https://mmbiz.qpic.cn/mmbiz_gif/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQsc4x3IXyibgVW6R1RcicxA3aNsC2aOSp3iasvWFCicccrecxgI4MNzoO0A/640?wx_fmt=gif)

### 源代码修改

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQTz8Y7RQ9S6PichZhbQZ0MQ0RMAzibfeL1SnaggtEy6GfhmpiaC76VDXtg/640?wx_fmt=png)

在执行的流程中最终执行到了 `createEndPoint` 方法中，从执行流程来看主要如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_jpg/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQ4YhYcyuTib08JfVvAIdiaLqkC0lVjiabMkuyIIFSluiaeZCw2KRoLcwicNw/640?wx_fmt=jpeg)

在执行 `rebind` 方法发送序列化代码时，可以看到在此时已经变成了 Weblogic 内网中运行的 IP 和 端口，直到程序执行到 `createEndPoint` 抛出异常。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQibSvq8BjF3Eu6FC46JpwUqf6Tibg4lD82zwu1AWu7IQC6cSLtxibMahgg/640?wx_fmt=png)

而执行到 `getInvocationIOR` 方法时，会调用 `IIOPRemoteRef.locateIORForRequest` 方法来进行寻找 `IOR`，并且将寻找到的 `IOR` 设置为当作当前 `IOR` 进行返回提供使用。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQfOKcHJmRDWZsTib9HsYS7pKt6KD1Vd4nvsUklFZxoFRV9rTCn3piatibQ/640?wx_fmt=png)

在进入 `locateIORForRequest` 方法之后会通过 `EndPointManager.findOrCreateEndPoint` 来进行寻找或创建结束切点，可以看到此时 `IOR` 的 `host`、`port` 变成了内网中的 IP 和端口。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQpAkwaabyQIZeCE4T440hdqbAFOuJ8yNImbqJWQ678BvDeDVgjxDQjA/640?wx_fmt=png)

在进入 `EndPointManager.findOrCreateEndPoint` 最终会执行到 `createEndPoint` 方法中来进行建立 Socket 通信，在这里由于是内网的 IP 和端口无法成功建立通信，导致后续的利用也无法继续进行。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQeDc2u3sXnWN1NYibsD0GPrW7ARWA3DZ1bicLxuicBseXiaZVl1uJHDYQ9A/640?wx_fmt=png)

#### 实现

大致的问题点已经确认的清楚的情况下，我们可以通过修改原始代码的方式来进行实现绕过，大体思路为：

1.  修改 `weblogic.corba.j2ee.naming.ContextImpl` 类中的 `rebind` 方法
    
2.  修改 `weblogic.iiop.IIOPRemoteRef` 类中 `locateIORForRequest` 方法的 ior 参数，确保正常调用 `findOrCreateEndPoint`  创建结束切点
    

首先修改 `weblogic.corba.j2ee.naming.ContextImpl` 类中 `rebind` 方法将正确的连接 IP 和端口加入到系统环境变量中。

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQJMdGZ26toy5UDlb8oPgTb31Fz2KJ6xnwGuTZuZ0fpHo55vwDQvpp1A/640?wx_fmt=png)

最后在 `locateIORForRequest` 方法读取系统环境变量中正确的 IP 和端口并且修改 `ior` 变量中相关的连接信息。使之能够正常的执行 `findOrCreatePoint` 方法创建结束切点

![](https://mmbiz.qpic.cn/mmbiz_png/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQy5Wdn7icQT4ABFialwrM4lZNGkfl8LUDbYNGC44K2mf04xIofpFNLOMg/640?wx_fmt=png)

最终效果：

![](https://mmbiz.qpic.cn/mmbiz_gif/3Ca8kUeB8CbohXoibEfvxSTnkmeok9ILQKOO40L4bRTXXvQVWth8fDse3seCibuWkrYPyMdseR2exQzIkQbhs8zw/640?wx_fmt=gif)

IIOP NAT 绕过方案总结
---------------

*   GIOP 协议极简实现
    

*   优点：原始 Socket 发包，效率较快
    
*   缺点：构造难度较高，需要掌握协议相关知识
    

*   Javassist
    

*   优点：修改难度较低
    
*   缺点：程序使用完毕之后需要重启，如果使用动态加载等方案可能导致资源占用率过高
    

*   源代码修改
    

*   优点：原生代码兼容性较强
    
*   缺点：修改难度较大
    

参考
--

*   https://blog.csdn.net/weixin\_33913377/article/details/94134763
    
*   https://docs.oracle.com/cd/E13211\_01/wle/wle42/corba/giop.pdf
    
*   https://www.slideserve.com/milek/13-giop-iiop-ior
    
*   https://www.cnblogs.com/scy251147/p/11100961.html