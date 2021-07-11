> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [forum.butian.net](https://forum.butian.net/share/233)

> 奇安信攻防社区 - PHP 反序列化漏洞这么学（细）！

简介
--

要想学习反序列化就要知道序列化的原理和作用，序列化就是把对象的成员变量转换为可以保存的和传输的字符串的过程，而反序列化就是把字符串再转换为原来的对象的变量，而这两个过程就很好的做到存储和传输数据。而序列化和反序列化分别通过函数 serialize() 和 unserialize() 来实现。

正文
--

介绍一下反序列化漏洞究竟是怎么产生的，其实在反序列化对象的时候，就会触发一些 PHP 的魔术方法，我知道大家都想知道这些魔术方法是怎么来的为什么会调用，这些魔术方法其实在设计类的时候写在类里面的，魔术方法函数有很多，要写那些就要看具体要实现那些功能了，PHP 中的魔术方法通常以__(两个下划线) 开始，并且不需要显示的调用而是由某种特定的条件触发。  
例子：

```
<?php
```

这就是一个典型的构造函数和析构函数，学过面向对象的都知道，举这个例子是比较好理解，这也就是魔术方法的用法。所以在反序列化的时候就是会调用这一些魔术方法，如果在魔术方法里面写了一些具有特定功能的函数，比如写入，读取，查询等。那么漏洞就产生了，但是没有写功能的话（如：仅仅只是做输出操作且输出的内容是定好的了，且输出信息没价值）那么漏洞也就不会产生，所以有反序列化不一定有漏洞，如果有反序列化漏洞那么在实战过程中肯定会有很多过滤的这时候就要代码审计绕过了。  
下面我就介绍一些实战中的一些魔术方法。

*   __construct()，类的构造函数
    
*   __destruct()，类的析构函数
    
*   __call()，在对象中调用一个不可访问方法时调用
    
*   __get()，访问一个不存在的成员变量或访问一个 private 和 protected 成员变量时调用
    
*   __set()，设置一个类的成员变量时调用
    
*   __isset()，当对不可访问属性调用 isset() 或 empty() 时调用
    
*   __unset()，当对不可访问属性调用 unset() 时被调用。
    
*   __sleep()，执行 serialize() 时，先会调用这个函数
    
*   __wakeup()，执行 unserialize() 时，先会调用这个函数
    
    构造和析构相信大家都很了解就不说了。
    
    ### __call()
    
    当调用一个成员函数时如果它存在就运行它，如果它不存在这就会调用__call() 函数。
    
    ```
    class Person
    ```
    
    结果：  
    [![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-2b566bf0f4fb8232e6aabbeacf66b901365909a5.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-2b566bf0f4fb8232e6aabbeacf66b901365909a5.png)  
    在这里我们可以看到创建了一个对象这个对象它调用了 say 函数和 run 函数，say 函数作为成员函数里面有但是 run 函数就没有了这时候就会调用__call() 这个魔术方法。
    
    ### __get()
    
    当访问一个不存在的成员变量或访问一个 private 和 protected 成员变量时调用  
    1、当访问一个不存在成员变量时调用
    

```
{
```

结果：  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-3eab59aecb5c96eef0b5f54c27d4247a80d14756.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-3eab59aecb5c96eef0b5f54c27d4247a80d14756.png)  
在这里实例化的对象它访问了这个成员变量 n，他存在在类中所以不调用__get() 函数，当它调用 A 时就会调用，因为根本就没有成员变量 A。  
2、当访问一个 private 和 protected 成员变量时调用

```
public $name;
```

对象它访问了一个私有的属性，正常情况下是不能直接访问的，这样就触发了这个__get() 魔术方法。

### __set()

这个的实质是给成员变量赋值是会调用它（其中包括给公有、私有、保护成员变量或者根本不存在的成员函数赋值，实质是这个赋值操作！），在参数初始化的时候是不会调用__set（）函数的。

```
public function __construct($)
```

结果：  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-808c3f3eacb9244c4f800fd695bd1fac63be4fe3.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-808c3f3eacb9244c4f800fd695bd1fac63be4fe3.png)  
在这里他分别调用了保护的成员变量和不存在的成员变量赋值了，所以自动调用了这个__set 魔术方法。

### __isset()

当对不可访问属性调用 isset() 或 empty() 时，__isset() 会被调用。

```
{
```

结果：  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-61d298fea9f3676da2ec6f9a32e8e77c8cb71c7a.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-61d298fea9f3676da2ec6f9a32e8e77c8cb71c7a.png)  
从在这里可以看出在访问公有 sex 的时候他直接判断了是否被设定，而在判断 name 和 age 这两个私有成员函数的时候他就会调用__isset() 这个魔术方法。

### __unset()

这个魔术方法触发的条件是在类外使用 unset 函数来删除私有和保护成员函数时会自动调用，但是在删除公有成员函数是不会调用它。

```
$this->name = $name;
```

结果：  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-9209a7009730b4d0a5955a9096f4871ecaa1f1a4.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-9209a7009730b4d0a5955a9096f4871ecaa1f1a4.png)  
在这里它调用了 sex，name，age 三个成员变量，其中 sex 为 public，name 和 age 是 private，所以 public 的没有调用__unset，另外两个就会调用了。

### __sleep()

要触发它的条件是序列化对象的时候就会触发，可以指定要序列化的对象属性，意思就是说他可以选择要序列化的成员变量。

```
}
```

结果：  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-ac6c0355a259db2758101d8e82ee1313f88c88e4.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-ac6c0355a259db2758101d8e82ee1313f88c88e4.png)  
在这里，我们可以看到他只序列化了 name 和 age，这个就是__sleep() 控制的（被 return 控制了），对于序列化之后的字符串对于新手师傅来说有点不好理解，我这里就给一张图片。  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-0ba5321decdb7d3dd8e14c7fff80ac098d1effa5.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-0ba5321decdb7d3dd8e14c7fff80ac098d1effa5.png)

```
function __destruct(){
```

这里 O 是代表序列号的为对象，2 就是代表这个对象它又两个字符，第三个就是代表具体的类值了，到了第二个 2 就是代表他所序列化的成员变量为 2 个，再之后大括号里面的就是具体的序列化的变量了，其中到第一个分号为止是代表第一个序列化的成员变量，s 是代表为字符串，4 位变量长度，冒号里面的就是具体的值了，再到第二个分号就是代表这个变量的具体值得数据类型，个数和具体值了，后面的就依次类推。但是数据类型有很多具体序列化之后，分别用什么表示这里我推荐大家看下这篇文章：[https://blog.csdn.net/phphot/article/d](https://blog.csdn.net/phphot/article/d) etails/1754911

### __wakeup()

他和序列化相反是在反序列化之后就会调用。

```
echo "完毕";
```

结果：  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-3095a6725e2523fcff5358c69e73af1d9ca75586.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-3095a6725e2523fcff5358c69e73af1d9ca75586.png)  
从结果可以看出他先序列化再反序列化，在反序列化的时候他调用了__wakeup() 函数，我们可以看到在初始化对象的时候我们给 name 和 sex 变量的值为小陈和男，反序列化之后就变成了小吴和女了，这就是触发了这个魔术方法，他里面有赋值功能所以就改变了，那大家想一想如果功能是其他的写入或者读取，数据库查询语句等，那么漏洞不就产生了。

实战演示
----

我们序列化和反序列化原理和常见的魔术方法都学了，那么就举个具体的反序列化漏洞试一试。  
举一个 pikachu 靶场：  
查看下源代码  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-7ec61a9c808d897c21f774d50877b9fd88386a21.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-7ec61a9c808d897c21f774d50877b9fd88386a21.png)  
可以看到他是以 post 传参，它对传入的数据赋值给 s 在对 s 进行反序列化，如果不能放序列化就会把 “大兄弟, 来点劲爆点儿的!“写入到网页中，如果能就会用反序列化后的对象访问 test 成员变量，把它输出发到网页上，这里 test 变量值可控，就可以构造 js 代码构造 XSS 漏洞，这里仅仅只是一个输出，如何写了其他功能，如写了，读取等那么就有更大的危害了。  
那么我们就构造 payload，有两种方法。  
第一种就是看些 PHP 代码进行序列化把结果写入到参数中

```
}
```

[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-806a9f47d69f19937fe2d2b04bdf759c8edbc7ff.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-806a9f47d69f19937fe2d2b04bdf759c8edbc7ff.png)  
第二种就是看源码直接写它的 payload

```
/**
```

其实也都差不多吧，只要知道原理，两种都能熟练掌握。  
由于是 post 型，我们就直接在框框里输入或者抓个包改下参数就 ok 了。  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-c15c10ba85f8ff6c82faf9dceee8d09b80ad09ac.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-c15c10ba85f8ff6c82faf9dceee8d09b80ad09ac.png)  
[![](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-1e8dea7c6ac678490f454a765f9ac710e47027ba.png)](https://shs3.b.qianxin.com/attack_forum/2021/07/attach-1e8dea7c6ac678490f454a765f9ac710e47027ba.png)  
其实这个 pikachu 靶场它的反序列化漏洞，是通过反序列化之后的对象，让这个对象来访问这个 test 变量来实现的。  
再来看下今年第五届强网杯的 web 的赌徒这一题：

```
* hello方法
```

在这里我们可以看到他是以 get 方式传参的，在进行反序列化，这可以看到他是考我们一个典型的 pop 链，什么是 pop 链？个人看来 pop 链就是魔术方法触发魔术方法，触发的是另外一个类里面的魔术方法，环环相扣。回到正题，我们整理一下 pop 链。

```
*/
```

可以看到反序列化 start 类的时候他触发了 wakeup 的魔术方法，在里面他调用了 sayhello（）函数，里面他输出了 name 变量，那如果这个 name 是个实例化的 info 类呢？那么就会触发 info 类的构造函数，在里面他输出来一个 promise 的字符串，如果 promise 是个实例化的 Info 类, 就会触发这个__toString(){**当把类作为字符串输出是触发**}，在 tostring 里面他有个 r**eturn $this->file[‘filename’]->ffiillee[‘ffiilleennaammee’];**，我们把 file[‘filename’] 赋值成一个 room 类那么就相当于访问实例化的 room 类的 **ffiillee[‘ffiilleennaammee’]** 显然这个成员变量不存在那么就会调用 get() 这个魔术方法，在里面他吧变量 a 当成一个函数出来了，我们就可以把 room 类赋值进去，不就触发了 invoke 魔术方法了吗 {**当把类作为函数是触发**}，最后我们看下 invoke 函数，他调用了 Get_hint($file) 函数，而这个函数他直接打开 / flag 这个文件，并且 b ase64 加密输出了，得到 flag 之后解密下就 Ok 了。  
payload：

```
public function hello()
```

结果：

```
{
```

要注意下 phonenumber 他是私有的会加上 %00 类名 %00。其实也可以手写 payload 的直接看源码写，只要学的精通两种方法都是很好的。

总结
--

这里我主要讲了一些魔术方法，和调用条件，漏洞产生的原理，和怎么看漏洞和写 payload，我个人是怎么看有没有漏洞呢，首先我是看类里面有没有一些危险的功能，看下能不能利用，能的话就逆推一下，看看怎么才能调用它，有没有一些可利用的魔术方法再看看他和其它类有没有关联，找找有没有 pop 链。最后在构造 payload 的。

**ps**: 本文章单纯是我个人的看法，如果有误，希望各位师傅指出，谢谢各位师傅，嘻嘻。