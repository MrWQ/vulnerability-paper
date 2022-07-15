> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/u94rWFwDxD5QfYhmiv85PA)

       首先看一张图

![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icl3pQPhibXzOncheucUwG6VdydUiarzQBUscxNus4nNTLItq0wAqVZEib7zGyLWn9JrNiaP4BCHLBeOzg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icl3pQPhibXzOncheucUwG6Vdbf1rVxWEkcc7LslMIlHCp1icemibogptvWvPedFDIXF5CtIiaxyN099Kw/640?wx_fmt=jpeg)

       PHP 反序列化 原理：未对用户输入的序列化字符串进行检测，导致攻击者可以控制反序列化过程，从而导致代码执行，SQL 注入，目录遍历等不可控后果。在反序列化的过程中自动触发了某些魔术方法。当进行反序列化的时候就有可能会触发对象中的一些魔术方法。
---------------------------------------------------------------------------------------------------------------------------------

<table><tbody><tr><td><br></td><td><p>serialize()&nbsp;// 将一个对象转换成一个字符串</p></td></tr><tr><td><br></td><td><p>unserialize()&nbsp;// 将字符串还原成一个对象</p></td></tr><tr><td><br></td><td><p>反序列化分为有类和无类</p></td></tr></tbody></table>

       我们先来看序列化数据也就是序列化字符串  
       先上图  
![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icl3pQPhibXzOncheucUwG6Vd3dreHeA4n7s0hA2cA2e06pCflZvicndTseFlCklveaAAgnAFwicu2O5A/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icl3pQPhibXzOncheucUwG6VdSbliboib5EjzT30p2pMm4kS7P4nKccMWiazFZZvNfbT3x8MuwhX8ic5x5Q/640?wx_fmt=jpeg)  
       我们看看上面那张图  

```
s:8:"chixigua"s
```

       s 代表字符串，8 代表长度 “chixigua” 代表值  
       在无类中他调用了 unserialize() 将字符串还原为对象没有进行过滤我们可以观察其代码而构造 payload 进行 sql 注入，代码执行，getshell，目录遍历等等，主要看他的代码，他的代码有 sql 语句接收序列化字符串这样会产生反序列化 sql 注入其他漏洞也是如此，主要看代码来辨别危害。  

  
       反序列化也是我们面试的必考题，所以还是很重要的  
       在思维导图我们提到有类在有类的情况我们会设计到各种魔术方法

  
       我们首先来介绍一下各种魔术方法  
       __construct()  
       具有构造函数的类会在每次创建新对象时先调用此方法，所以非常适合在使用对象之前做一些初始化工作。  
       __destruct()  
       析构函数会在到某个对象的所有引用都被删除或者当对象被显式销毁时执行。  
       也就是说进行反序列化时，完成的就是从字符串创建新对象的过程，刚开始就会调用__construct(), 而对象被销毁时，例如程序退出时，就会调用__destruct()

  
       触发：unserialize 函数的变量可控，文件中存在可利用的类，类中有魔术方法：  
       参考：官方文档魔法方法部分  
       __construct()// 创建对象时触发  
       __destruct() // 对象被销毁时触发  
       __call() // 在对象上下文中调用不可访问的方法时触发  
       __callStatic() // 在静态上下文中调用不可访问的方法时触发  
       __get() // 用于从不可访问的属性读取数据  
       __set() // 用于将数据写入不可访问的属性  
       __isset() // 在不可访问的属性上调用 isset() 或 empty() 触发  
       __unset() // 在不可访问的属性上使用 unset() 时触发  
       __invoke() // 当脚本尝试将对象调用为函数时触发

  
       接下来我们先看一段魔术方法 php 代码  
![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icl3pQPhibXzOncheucUwG6VdC9wwsOwR2w9d25Y7C1uTfpr0STA32NPwamdC3qyVu0zFcKXo9k3p1Q/640?wx_fmt=jpeg)

       首先先分析一下代码创建了一个类  
       里面写了 3 个魔术方法  
       我们看结果首先输出了‘调用了构造函数’，为什么在魔术方法里的这串代码执行了呢？这是因为触发了他的魔术方法，因为我们将一个类进行了实体化，也就是新建了一个对象，触发了__construct() 方法里的代码，接下来又输出了‘调用了苏醒函数’在反序列话函数执行的时候会先检测__wakeup() 方法有该方法这会先执行这个方法里的代码

       详细参考这张图  
![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icl3pQPhibXzOncheucUwG6VdJhR5nJng9sS1YgKoXRHyQzk8Q1aqiaEgZIHwExv0RzqWj3m3W97ulKA/640?wx_fmt=jpeg)

       可以玩玩去年网鼎的青龙杯里的反序列化题我把解题思路写下来  
       网鼎杯青龙组 php 反序列化题

<table><tbody><tr><td><br></td><td><p>** 首先 ctf 命名及代码函数 unserialize 判断反序列化知识点</p></td></tr><tr><td><br></td><td><p>第一：获取 flag 存储 flag.php</p></td></tr><tr><td><br></td><td><p>第二：两个魔术方法__destruct __construct</p></td></tr><tr><td><br></td><td><p>第三：传输 str 参数数据后触发 destruct，存在 is_valid 过滤</p></td></tr><tr><td><br></td><td><p>第四：__destruct 中会调用 process, 其中 op=1 写入及 op=2 读取</p></td></tr><tr><td><br></td><td><p>第五：涉及对象 FileHandler，变量 op 及 filename,content，进行构造输出 **</p></td></tr></tbody></table>

**

<table><tbody><tr><td><br></td><td><p>&lt;?php</p></td></tr><tr><td><br></td><td><p>class&nbsp;FileHandler{</p></td></tr><tr><td><br></td><td><p>public $op='2';// 源码告诉我们 op 为 1 时候是执行写入为 2 时执行读</p></td></tr><tr><td><br></td><td><p>public $file;// 文件开头调用的是 flag.php</p></td></tr><tr><td><br></td><td><p>public $content="zmc";</p></td></tr><tr><td><br></td><td><p>}</p></td></tr><tr><td><br></td><td><p>$flag =&nbsp;new FileHandler();</p></td></tr><tr><td><br></td><td><p>$flag_1 = serialize($flag);</p></td></tr><tr><td><br></td><td><p>echo $flag_1;</p></td></tr><tr><td><br></td><td><p>?&gt;</p></td></tr></tbody></table><table><tbody><tr><td><br></td><td><p>涉及：反序列化魔术方法调用，弱类型绕过，ascii 绕过</p></td></tr><tr><td><br></td><td><p>使用该类对 flag 进行读取，这里面能利用的只有__destruct 函数（析构函数）。__destruct 函数对 $this-&gt;op 进行了 === 判断并内容在 2 字符串时会赋值为 1，process 函数中使用 == 对 $this-&gt;op 进行判断（为 2 的情况下才能读取内容），因此这里存在弱类型比较，可以使用数字 2 或字符串'2'绕过判断。</p></td></tr><tr><td><br></td><td><p>is_valid 函数还对序列化字符串进行了校验，因为成员被 protected 修饰，因此序列化字符串中</p></td></tr></tbody></table>

本文作者： **かくれんぼ**   
本文链接：https://www.cnblogs.com/zmcbk/p/14497408.html

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**