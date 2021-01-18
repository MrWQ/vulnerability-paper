> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/3Ha2lreTvDykVa5wHlQXCw)

_**声明**_

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测以及文章作者不为此承担任何责任。  
雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_**No.1  
**_

_**前言**_

最近在学习 java 的反序列化，而其中 java 的反射机制经常被提到，所以再深入学习一下 java 的反射，也算是给自己打一个基础。

_**No.2  
**_

_**反射概念**_

Java 的反射（reflection）机制是指在程序的运行状态中，可以构造任意一个类的对象，可以了解任意一个对象所属的类，可以了解任意一个类的成员变量和方法，可以调用任意一个对象的属性和方法。这种动态获取程序信息以及动态调用对象的功能称为 Java 语言的反射机制。反射被视为动态语言的关键。（自己的理解就是 当程序在运行的时候, 动态地去加载一些之前用不到的类, 不需要将其加载到 jvm 中, 而在运行时需要加载的。）

**举个栗子**  
一个项目底层需要使用 mysql，而有时候是使用 oracle，所以根据实际情况来使用数据库的驱动类，这时候就需要利用反射了，假设 com.java.dbtest.myqlConnection，com.java.dbtest.oracleConnection 这两个类我们要用，这时候我们的程序就写得比较动态化，通过 Class aClass = Class.forName("com.java.dbtest.TestConnection"); 通过类的全类名让 jvm 找到并加载这个类，而如果是 oracle 则传入的参数就变成另一个了。

_**No.3  
**_

_**反射获取类的信息**_

这里通过反射获得类的变量还有方法。  
先写一个实体类, 分别有 public private 修饰符修饰的变量和方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVXMG3nlSEdbxBvdAAcnC1SlRUaHFZbBiaNicvv4mmWcicq1TP3EkUC2wDB7pMK5qRhmYb3XZ4phE0ibQ/640?wx_fmt=png)

**2.1 类的变量信息**

这边先了解 Field 类, 代表了类的成员变量就行，获取方法苏需要的 method 类一样。

```
public class GetInformation {
public static void main(String[] args) throws Exception {
    //1.通过类名获取类,并且打印类名
    Class carClass = Car.class;
    System.out.println("类名称:"+carClass.getName());

    //2.1 获取修饰符为public的信息
    //通过getFields获取类的信息返回一个数组
    Field[] publicFields = carClass.getFields();

    //2.2 获取修饰符为private的信息
    //getDeclaredFields()不会在意修饰符
    Field[] privateFields = carClass.getDeclaredFields();

    //3.遍历数组获取反射得到的变量属性
    for(Field Fields:publicFields){
        //获取访问的权限并且输出变量属性
        //Field的g`etModifiers()方法返回int类型值表示该字段的修饰符。
        int modifiers = Fields.getModifiers();
        System.out.println("修饰符:"+Modifier.toString(modifiers)+
                " 变量的类型:"+Fields.getType()+
                " 变量的名称:"+Fields.getName()
                );

    }
    System.out.println("---------------");
    for(Field Fields:privateFields){
        //获取访问的权限并且输出变量属性
        int modifiers = Fields.getModifiers();
        System.out.println("修饰符:"+Modifier.toString(mo`difiers)+
                " 变量的类型:"+Fields.getType()+
                " 变量的名称:"+Fields.getName()
        );

    }
}
```

一些方法的解释都在注释上了, 这里就不在解释了, 主要是注意一下注释中 2.1 的 getFields() 与 2.2 的 getDeclaredFields() 之间的区别。

放上运行后的结果：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVXMG3nlSEdbxBvdAAcnC1Sx3I85SCPBzpZQ9Wj9fiaJHrziaBUnRGg3pvIYgPfepfouqWdmCYPTnDA/640?wx_fmt=png)

发现上面的 getFields 没有 private 修饰符的变量, 而 getDeclaredFields() 不管是 public 还是 private 的都输出了。  
对了, getModifiers() 方法解释在上面这边说一下运行后 int 数值所代表的修饰符  
对应表如下：  
PUBLIC: 1  
PRIVATE: 2  
PROTECTED: 4  
STATIC: 8  
FINAL: 16  
SYNCHRONIZED: 32  
VOLATILE: 64  
TRANSIENT: 128  
NATIVE: 256  
INTERFACE: 512  
ABSTRACT: 1024  
STRICT: 2048

**2.2 类的方法信息**

直接上代码

```
public class GetMethod {
public static void main(String[] args) {
    //1.通过类名获取类,并且打印类名
    Class carClass = Car.class;
    System.out.println("类名称:"+carClass.getName());

    //2.1 获取修饰符为public的方法
    //通过getMethods获取类的信息返回一个数组
    Method[] publicMethod = carClass.getMethods();

    //2.2 获取修饰符为private的方法
    //getDeclaredMethods()不会在意修饰符
    Method[] privateMethod = carClass.getDeclaredMethods();

    //3.对数组进行遍历获取类的方法
    for (Method method: publicMethod) {
        //获取访问的权限并且输出变量属性
        //getReturnType得到返回值的类型
        int modifiers = method.getModifiers();
        System.out.print(Modifier.toString(modifiers) + " ");
        //获取并输出方法的返回值类型
        Class returnType = method.getReturnType();
        System.out.print(returnType.getName() + " "
                + method.getName() + "( ");
        //获取并输出方法的所有参数
        Parameter[] parameters = method.getParameters();
        for (Parameter parameter :
                parameters) {
            System.out.print(parameter.getType().getName()
                    + " " + parameter.getName() + ",");
        }
        //获取并输出方法抛出的异常
        Class[] exceptionTypes = method.getExceptionTypes();
        if (exceptionTypes.length == 0) {
            System.out.println(" )");
        } else {
            for (Class c : exceptionTypes) {
                System.out.println(" ) throws "
                        + c.getName());
            }
        }
    }
}
```

直接放运行结果

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVXMG3nlSEdbxBvdAAcnC1SvXQIlg18ZoMQHdpMorxZOT2NeDz1jfl4BOvqxib6sGQ8EQ70IQ8ubMA/640?wx_fmt=png)

运行后发现 getMethods() 方法不光会获取 car 类的所有 public 方法, 还会获取 car 默认继承的 object 类的方法。

直接放上调用 getDeclaredMethods() 方法的结果，发现访问输出的全都是 car 类的方法, 没有 object 类的方法。

_**No.4  
**_

_**访问并且操作类的方法**_

上面, 仅是获取了类的变量信息, 方法的信息, 而在反序列化中 payload 都是进行对其方法的利用, 所以要对类的方法进行操作访问进行学习。

**3.1 操作 public 方法**

详细的介绍都在注释上  
public class UsePublicMethod {  
    public static void main(String[] args) throws Exception {  
        //1. 第一步获取 Class 类实例  
        //forName() 应该都很熟悉, 就是根据装载一个类, 返回与给定的字符串名称相关联类或接口的 Class 对象  
        Class aClass = Class.forName("ReflectionStudy.Information.Car");

```
//2.获取public方法
    //其中getMethod()需要两个参数,第一个参数为方法的名称
    //第二个参数为获取方法的参数的类型,参数为class
    Method getMSG = aClass.getMethod("getMSG", String.class, String.class);

    //3.开始操作方法
    //使用 invoke 反射调用public方法
    //getMSG 是获取到的public方法
    //aClass要操作的对象,由于aClass没有实例化,所以这边要加上newInstance()将其实例化
    //后面两个参数传实参
   getMSG.invoke(aClass.newInstance(),"QQ","Blue");

    System.out.println("=====分割线======");
    //尝试着利用java的链式编程进行两局话输出
    Class msg = Class.forName("ReflectionStudy.Information.Car");
    msg.getMethod("getMSG", String.class, String.class).invoke(msg.newInstance(),"QQ","black");
}
```

补充一下, invoke 对方法反射利用的时候加入了 newInstance 进行对象的实例化, 因为没有加上的话, 会报错误信息：object is not an instance of declaring class, 就是因为对象没有实例化. 所以发现 Class.forname 没有对 car 这个类进行实例化操作。  
运行截图放上：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVXMG3nlSEdbxBvdAAcnC1SS8guiaL8HzBBIn942fyhiauNVMiccbESMBhtnPY4JdOqLw9l60L4N5CrQ/640?wx_fmt=png)

**3.2 操作 private 方法**

接下来就是对 private 修饰符修饰的方法进行获取利用，不过相对于 public 方法 private 也就是多了一步对权限的更改和判断。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVXMG3nlSEdbxBvdAAcnC1SOJsZby6zgKUMWR45zeR2YO752Ustgkn1ZMPyIxH9R5oGCIhkW3KajQ/640?wx_fmt=png)

操作 private 方法需要使用 setAccessible(true), 将访问的权限设置为 true 然后对其正常的访问。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVXMG3nlSEdbxBvdAAcnC1SVoMenXvAmJG3JtftdkTQxiaXxbTpoQeMex5ULFFJCgHJk6Ts3qt7NGA/640?wx_fmt=png)

_**No.5  
**_

_**总结与补充**_

反射就是把 java 类中的各种成分映射成一个个的 Java 对象。  
Class.forName 的主要功能就是返回一个类, 要求 JVM 查找并加载指定的类，也就是说 JVM 会执行该类的静态代码段（注意是静态代码块）  
Class.forName 是一个静态方法，相同能够用来载入类。  
该方法有两种形式：Class.forName(String name, boolean initialize, ClassLoader loader) 和 Class.forName(String className)。  
第一种形式的參数 name 表示的是类的全名；initialize 表示是否初始化类。loader 表示载入时使用的类载入器。  
另外一种形式则相当于设置了參数 initialize 的值为 true，loader 的值为当前类的类载入器，而我们什么时候使用 class.forName 呢？为什么还需要加入了 newinstance？

比如说，给了一个字符串变量, 代表了一个类的包名类名, 怎么样实例化, 肯定想到的是 new：  
A a = (A)Class.forName(“pacage.A”).newInstance();  
这和你 A a = new A()；是一样的效果。  
在初始化一个类，生成一个实例的时候，newInstance() 方法和 new 关键字除了一个是方法，一个是关键字外。它们的区别在于创建对象的方式不一样，前者是使用类加载机制，后者是创建一个新类。  
这里给出 new 和 newinstance 调用的使用和结果：  
newInstance: 弱类型，低效率，只能调用无参构造。  
new: 强类型，相对高效，能调用任何 public 构造。  
Class.forName(“”) 返回的是类。  
Class.forName(“”).newInstance() 返回的是 object。

**参考**  
java 反射由浅入深  
Class.forName 详解

_**招聘启事**_

安恒雷神众测 SRC 运营（实习生）  
————————  
【职责描述】  
1.  负责 SRC 的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2.  负责白帽子提交漏洞的漏洞审核、Rank 评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

设计师（实习生）

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
3、有品牌传播、产品设计或新媒体视觉工作经历；  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦 19 楼  
学历要求：本科及以上  
工作年限：1 年及以上，条件优秀者可放宽

简历投递至 

bountyteam@dbappsecurity.com.cn

安全招聘  
————————  
公司：安恒信息  
岗位：Web 安全 安全研究员  
部门：战略支援部  
薪资：13-30K  
工作年限：1 年 +  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
【岗位职责】  
1. 定期面向部门、全公司技术分享;  
2. 前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3. 负责完成部门渗透测试、红蓝对抗业务;  
4. 负责自动化平台建设  
5. 负责针对常见 WAF 产品规则进行测试并落地 bypass 方案  
【岗位要求】  
1. 至少 1 年安全领域工作经验；  
2. 熟悉 HTTP 协议相关技术  
3. 拥有大型产品、CMS、厂商漏洞挖掘案例；  
4. 熟练掌握 php、java、asp.net 代码审计基础（一种或多种）  
5. 精通 Web Fuzz 模糊测试漏洞挖掘技术  
6. 精通 OWASP TOP 10 安全漏洞原理并熟悉漏洞利用方法  
7. 有过独立分析漏洞的经验，熟悉各种 Web 调试技巧  
8. 熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
【加分项】  
1. 具备良好的英语文档阅读能力；  
2. 曾参加过技术沙龙担任嘉宾进行技术分享；  
3. 具有 CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP 等安全相关资质者；  
4. 具有大型 SRC 漏洞提交经验、获得年度表彰、大型 CTF 夺得名次者；  
5. 开发过安全相关的开源项目；  
6. 具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7. 个人技术博客；  
8. 在优质社区投稿过文章；

岗位：安全红队武器自动化工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 熟练使用 Python、java、c/c++ 等至少一门语言作为主要开发语言；  
2. 熟练使用 Django、flask 等常用 web 开发框架、以及熟练使用 mysql、mongoDB、redis 等数据存储方案；  
3: 熟悉域安全以及内网横向渗透、常见 web 等漏洞原理；  
4. 对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5. 具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。

简历投递至

bountyteam@dbappsecurity.com.cn

岗位：红队武器化 Golang 开发工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 掌握 C/C++/Java/Go/Python/JavaScript 等至少一门语言作为主要开发语言；  
2. 熟练使用 Gin、Beego、Echo 等常用 web 开发框架、熟悉 MySQL、Redis、MongoDB 等主流数据库结构的设计, 有独立部署调优经验；  
3. 了解 docker，能进行简单的项目部署；  
3. 熟悉常见 web 漏洞原理，并能写出对应的利用工具；  
4. 熟悉 TCP/IP 协议的基本运作原理；  
5. 对安全技术与开发技术有浓厚的兴趣及热情，有主观研究和学习的动力，具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式、消息队列等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。  
简历投递至

bountyteam@dbappsecurity.com.cn

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JVXMG3nlSEdbxBvdAAcnC1SgVeFspBviccOVXq0cZQqGLw1y24PUiciaicj5ZopMXIPGbwwNfWeiazBgAA/640?wx_fmt=jpeg)

专注渗透测试技术

全球最新网络攻击技术

END

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JVXMG3nlSEdbxBvdAAcnC1SdKJdWuAExUn3SJdXRnOnzpONQ5N1F7nmrZws5vRPNbzqXHHQCMO9hg/640?wx_fmt=jpeg)