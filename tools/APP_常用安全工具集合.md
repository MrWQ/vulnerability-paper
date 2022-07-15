> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/eAFIpqNUqqpoHjwVClAc8g)

### 一. 抓包

#### HTTP 请求类

*   Fiddler/Charles（必备常用工具之一）
    

最常见的代理抓包工具，这两个就不用多说了吧？应该都知道了。

*   ProxyDroid（必备常用工具之一）
    

强制全局代理工具，详细介绍见当你写爬虫抓不到 APP 请求包的时候该怎么办？【初级篇】

*   PacketCapture/HTTPCanary（必备常用工具之一）
    

VPN 抓包工具，详细介绍见当你写爬虫抓不到 APP 请求包的时候该怎么办？【初级篇】

*   JustTrustMe（必备常用工具之一）
    

基于 Xposed 写的反 SSL Pinning 工具，详细介绍见当你写爬虫抓不到 APP 请求包的时候该怎么办？【中级篇】

*   ObjectionUnpinningPlus（必备常用工具之一）
    

瘦蛟舞写的一个 Frida 脚本，功能与 JustTrustMe 相同，但因为 Frida 的特殊性，可以随时修改内容，面对一些特殊情况时会很方便。

*   WireShark
    

也是一个很常见的抓包工具，但由于工作方式过于底层，对 HTTPS 请求的处理比较麻烦，一般不建议对使用 HTTP 协议的 APP 使用。

#### 非 HTTP 请求类

*   WireShark
    

非 HTTP 的还是使用 WireShark 这类工具方便些，通常需要配合反编译找到协议的组成方式。  
建议使用方式：电脑端开热点，然后指定用于创建热点的虚拟网卡，再把手机连上热点开始抓包。

*   Tcpdump
    

在使用没有无线网卡的电脑或无法开热点的情况下可以直接在手机上运行 Tcpdump 然后导出文件在电脑端 WireShark 中打开，与直接使用 WireShark 抓包效果相同。

### 二. 解密相关

#### Java 层

*   Jadx（必备常用工具之一）
    

一个非常方便的 Java 反编译工具，一般用到的功能主要是搜索、反混淆、查找方法调用这几样，性能和反编译出来的代码效果都比使用 dex2jar+jd-gui 之类的方式好。

*   Xposed（必备常用工具之一）
    

Xposed 框架大家应该都知道吧？这是一个功能十分强大的 Hook 框架，很多逆向工具都是基于它来写的，有特殊需求时也可以自己写一个模块使用。

*   Frida（必备常用工具之一）
    

相对于 Xposed 而言，Frida 算是一个在安全圈外没有那么高知名度的 Hook 工具了，但它的功能在某些方面要比 Xposed 强得多（当然也有缺点），举个常用到的例子：用它来 Hook So 库中的函数~。

*   inspeckage（必备常用工具之一）
    

这是一个基于 Xposed 写的动态分析工具，Hook 了大量逆向时常见的方法，下面是它的 GitHub 中给出的列表：

> Shared Preferences (log and file);  
> Serialization;  
> Crypto;  
> Hashes;  
> SQLite;  
> HTTP (an HTTP proxy tool is still the best alternative);  
> File System;  
> Miscellaneous (Clipboard, URL.Parse());  
> WebView;  
> IPC;
> 
> Hooks (add new hooks dynamically)

注意它 Hook 列表中有 Crypto 和 Hash，这两个类型在破解大部分 APP 的加密参数时可以说是降维打击，因为大部分 APP 的加密参数都逃不过 MD5、SHA1、AES、DES 这四种，而它们都被 Hook 了（不仅仅只有这四种）。基本上就是打开 Inspeckage 再打开它的 Web 端，然后打开指定的 APP 操作一下，一个搜索，加密参数就原形毕露了。

*   DeveloperHelper
    

一个基于 Xposed 写的辅助工具，通常会用到的功能是查看 Activity 名、查看加固类型、查看 Activity 结构、自动脱壳这几个。

*   UCrack
    

也是一个基于 Xposed 写的辅助工具，集成了自动网络抓包、网络堆栈爆破、文件日志、WebView 调试环境、自动脱壳、Native 函数注册监控、记录程序自杀堆栈等功能，这个工具是我之前偶然发现的，还没有使用过，有兴趣的同学可以用用看。

#### C/C++ 层（So 库）

*   IDA（必备常用工具之一）
    

非常强大的反汇编和动态调试工具，强烈不推荐使用 NSA 开源的 Ghidra，效果跟 IDA 比起来差太多了。IDA 可以在反汇编之后将汇编代码转成伪 C 代码，并且能在手机端启动了服务端之后注入 APP 进程使用动态调试功能。

*   Frida（必备常用工具之一）
    

上面讲过了

*   有壳（加固）的
    
*   DeveloperHelper
    

上面讲过了

*   UCrack
    

上面讲过了

*   FDex2
    

其实就是把几行代码包了一层而已，原理就是 Hook ClassLoader 的 loadClass 方法，反射调用 getDex 方法取得 Dex(com.android.dex.Dex 类对象)，再将里面的 dex 写出。 

注：文章内容仅供学习交流使用，任何人不得将其用于非法用途，否则后果自行承担！

文章如有侵权，请联系删除。  

**推荐阅读****[![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyIDG0WicDG27ztM2s7iaVSWKiaPdxYic8tYjCatQzf9FicdZiar5r7f7OgcbY4jFaTTQ3HibkFZIWEzrsGg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzAwMjA5OTY5Ng==&mid=2247493726&idx=2&sn=ea7c8b6a9a2814777ef818d2d4032f4e&chksm=9acd38c1adbab1d7c352c6a7258b9b4c65e6a6524eab769950f76016c667f4efa8cb8d1f5d4c&scene=21#wechat_redirect)**

公众号