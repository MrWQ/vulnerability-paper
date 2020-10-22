\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/lGdILATcEOY2goyRvFv9uQ)

****文章源自-投稿****

**作者-挽梦雪舞**

**扫描下方二维码进入社区：**

**![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK3Fc7MgHHCICGGSg2l58vxaP5QwOCBcU48xz5g8pgSjGds3Oax0BfzyLkzE9Z6J4WARvaN6ic0GRQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)**

**今天我们继续深入unserialize()，接着上文，我们已经讨论过PHP的反序列化如何导致漏洞，以及攻击者如何利用它来实现RCE攻击，现在让我们更深入地研究一些可以用来实现RCE的骚操作。**

**先对unserialize()漏洞原理整体认识一下：**

**当攻击者控制传递给 unserialize() 的序列化对象时，他便可以控制所创建对象的属性。然后，通过控制传递给\_\_wakeup() 之类函数的魔术方法的值，从而让攻击者有机可乘，他们可能以此来劫持应用程序流。**

**然后，攻击者可以使用其指定的参数执行魔术方法中包含的恶意攻击代码，或将魔术方法用作启动POP链的一种方式。**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)****

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnJCNuAmPAyiadBbLZMEnAysahCZMq6gZpxboHGmXFa6CFOmZ7Q31SYjB9SmkgU3ASXWg3kA4wN006g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**魔术方法：**

**尝试利用unserialize() 漏洞时，具体有四种魔术方法特别有用：\_\_wakeup()  \_\_destruct() \_\_toString() 和 \_\_call()。今天，笔者来讨论一下它们具体是什么，本质原理，他们能用来做什么，以及为什么它们对构建漏洞有用。**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

**\_\_wakeup()**

**\_\_wakeup() 是在unserialize() 上调用的魔术方法。它通常用于重新构建序列化过程中可能丢失的任何数据库链接，并执行其他重新初始化任务。  
**

**在unserialize() 漏洞利用期间, 它通常对攻击者很有帮助，因为如果为类定义它，则在对象反序列化中会自动调用它。因此，它便会为POP链提供一个便利的数据库或代码中其他功能的入口点，从而让攻击者有利用的可能。**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

**\_\_destruct()**

**但是，当不存在对反序列化对象实例的引用时，将会调用\_\_destruct()。它在进行垃圾回收时调用，通常用于清理并执行完结与该对象关联的其他未完成的任务线程。  
**

**由于它用于清理资源和关闭的功能，因此我们可以发现\_\_destruct() 在利用方面还包含有用的代码。例如，如果\_\_destruct() 魔术方法包含用于删除和清除与对象关联的文件的代码，则这可能使攻击者有机会利用，从而破坏文件系统的完整性。**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

**\_\_toString()**

**与上述的 \_\_wakeup() 和\_\_destruct() 不同，只有当将对象视为字符串时才调用 \_\_toString()魔术方法，这一点从该函数的命名上可以看出，尽管如此，但如果为该类定义了 \_\_toString()方法，它很可能会在某个地方被使用。**

**\_\_toString() 魔术方法允许一个类来决定当它被作为字符串处理时，它会如何执行。例如，如果将对象传递给echo() 或print()函数，可能会打印的内容。**

**这种魔术方法的可利用性根据实现方式的不同会存在很大差异。例如，下面是一个\_\_toString()函数，可用于开启POP链：**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**在这种情况下，将Example3实例视为字符串时，它会返回其$obj属性的getValue() 魔术方法的执行结果。并且由于$ obj属性可能完全在攻击者的控制之下，这可能使攻击者具有很大的权限和灵活性执行其他恶意操作，并且导致严重的漏洞。除此之外，\_\_toString() 通常也可以用来访问敏感文件。**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

**\_\_call()**

**\_\_call() 该方法是在未定义时被调用。例如，调用$object->undefined($args)时，将变成$object->\_\_call(‘undefined’, $args)，  
**

**同样，此魔术方法的可利用性根据实现方式的不同也存在很大差异。但是，在不安全的反序列化入口点之后开启POP链时，会发现它有更大的利用空间。**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

**总结：**

**尽管这四种魔术方法是最常用的，但是还有许多其他方法可用于利用unserialize（）漏洞。**  

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**如果上述四种方法不可用，可以尝试检查该类对其他魔术方法的实现，以及是否可以在某处开启利用链。**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

References：

**图源互联网，侵删**

**https : //www.php.net/manual/zh/language.oop5.magic.php**

**https://medium.com/swlh/diving-into-unserialize-magic-methods-386d41c1b16a**

**https://www.owasp.org/index.php/PHP\_Object\_Injection**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

**通知！**

**公众号招募文章投稿小伙伴啦！只要你有技术有想法要分享给更多的朋友，就可以参与到我们的投稿计划当中哦~感兴趣的朋友公众号首页菜单栏点击【商务合作-我要投稿】即可。期待大家的参与~**

**![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)**

**记得扫码**

**关注我们**