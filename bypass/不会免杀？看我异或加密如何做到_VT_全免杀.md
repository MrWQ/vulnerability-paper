> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/CN3DHF1ewVUj0WMusBldDw)

**前言**

最近逛 github 的时候发现一个 C 的免杀项目，项目介绍中，作者只利用了动态加载 windows api ，和异或加密的方法就达到了在 antiscan.me 上全免杀的效果：  
![](https://mmbiz.qpic.cn/mmbiz_jpg/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKNLus9JFiavgENmJ34sDOicUHeAa5XQM6HIwhC3AwiaTdCltsyUCG8YmoQ/640?wx_fmt=jpeg)  

于是，我怀着一颗学徒之心，研究了一下这个项目，下面是我在  vt 上的测试结果：  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKn9H2lDuqf44wK6K9xxiae11LicnxIqNiaibnhZH06IpSgjicA5ibyd9oqO0Q/640?wx_fmt=png)

**使用方法**

需要的环境：python3 、C++ 编译环境（我测试的时候是用 VS2017 编译的，如果是 Kali Linux 需要使用 apt-get install mingw-w64 * 命令安装相关编译环境）。  

先利用 msf 生成 shellcode（这里为了方便测试直接生成弹计算器的 shellcode）  

```
msfvenom -p windows/exec CMD=calc.exe EXITFUNC=thread -f raw -o beacon.bin
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKHucQUCHoW3mAUmVZN87jFq3w6hicVialFjKa6xZJIaesPYGPmEwhBocQ/640?wx_fmt=jpeg)  

然后运行 python charlotte.py：  

![](https://mmbiz.qpic.cn/mmbiz_jpg/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKpxblhGHyVsZsLfuYdclicZ1bpq5r9fZJHWk7DIoky1DSuz1Dy7e9Vibg/640?wx_fmt=jpeg)  

生成后的 dll 文件就是需要的恶意文件了，执行方法 rundll32 charlotte.dll, 随机函数名  
具体的命令在运行 charlotte.py 脚本后会显示，如下图：  

![](https://mmbiz.qpic.cn/mmbiz_jpg/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKcic86Fk13XNSIib6MNqyWzeQYd5icqOgAoQ37cqiaOzricgc84OgphAnc2w/640?wx_fmt=jpeg)

Bypass AV 无压力。  
                                                                       

**源码分析**

这个项目一共分为两个部分，大概的思路就是创建一个模板的 C++ 文件，然后利用 python 对字符串的处理，来解决 C++ 文件中 windows api 的混淆和 shellcode 的加密。（其实很简单，还是老一套），项目目录结构如下图：  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKTDteUpcveZvlciatXwHic9n1FyYjonvuDh16b23Fy8GFzk2fGgwXdXSw/640?wx_fmt=png)  
首先，我们来看下 C++ 模板文件的关键代码：  

```
// If all good, launch the payload
    if ( rvba != 0 ) {
                XOR((char *) createthread, ct_len, ct_key, sizeof(ct_key));
                pCreateThread = GetProcAddress(GetModuleHandle("kernel32.dll"), createthread);
            thba = pCreateThread(0, 0, (LPTHREAD_START_ROUTINE) exec_mem, 0, 0, 0);
                XOR((char *) waitforsingleobject, wfso_len, wfso_key, sizeof(wfso_key));
            pWaitForSingleObject = GetProcAddress(GetModuleHandle("kernel32.dll"), waitforsingleobject);
            pWaitForSingleObject(thba, -1);
    }
    return TRUE;
    }
```

可以看到，这个项目并没有用什么很复杂的技巧，模板 C++ 的代码流程大概是这样的：  
**申请内存空间——> 更改内存空间属性 ——> 创建线程——> 执行 shellcode**  
不过在调用的函数的时候，都采用了使用 GetProcAddress 动态获取函数的方式，这样的方法应该是让大部分杀软无法通过导入表中的函数去判断程序的黑白。  

接下来，我们看 py 文件的内容：  
第一个部分，读取 shellcode 内容，还有准备需要混淆的 api 名字，获取 key 随机字符串。  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKVdKmPicLFRWTjDH67VV9u3TO702ha2BflelhLjk8DAcQpuPHLZictVgg/640?wx_fmt=png)

第二部分，将 shellcode 和相关 api 字符串通通用异或进行混淆：  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKY5jhk3JXrFa6JkicwOibz27f9N0PjCHygrib2Ad2358j8EZArhG1zFqSg/640?wx_fmt=png)  

第三部分，将混淆后的字符串和混淆用的 key 替换模板中文件的对应部分：  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKB3L9472gibDHoRRW8ocFD5HSGOiaAZZ5WN7HxPVzdCiaKehGZbTrIkGgA/640?wx_fmt=png)  

第四部分，用 g++ 生成目标文件，清除中间产生的 cpp 文件：  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlK95AicWCQOEsWqexaOPH74wFv8vOH6Wicrk9yUaWRTsYs9rT0WSzW5w9A/640?wx_fmt=png)  

**总结**

这个项目免杀的原因大概有以下几点：

1.  VT 的多引擎查杀是静态查杀，或者说由于生成的是动态链接库文件，使得杀毒引擎只能使用启发式查杀和动态查杀去判断黑白。
    
2.  模板中的字符串赋值类似 char buf[] = {'h','e','l','l','o'};。这样让字符串存在于 text 段，而非常见的 rdata 段，字符串数据和代码混在一起，让杀毒引擎难以快速识别里面的字符串。（之所以说难以识别，是因为用 ida 之类的软件还是能看出来的，但是那样要求去用反汇编引擎反编译，识别语法树之类的，操作时间太长，为了平衡杀毒效率和杀毒准确性，一般会在云平台上运行）
    
3.  模板中调用 windows api 的使用都是动态加载，而且用字符串混淆的方式隐藏了 api 函数，而且每个字符串的 key 都不一样，导致杀毒引擎没法识别出本来的字符串，进一步识别。  
    总得来说，这个项目在静态查杀方面已经做到了免杀当前所有杀毒引擎，是个挺不错得项目。
    
  

由于比较懒，并没有按照项目推荐去下 g++ 环境踩坑，以下是在 vs2017 上存在得一些坑点，大家踩坑的时候自行斟酌。

这个项目的 python 脚本对 g++ 编译过程是隐藏的，所以一些编译时可能有的错会难以发现。如果发现运行脚本后没有自动生成 dll 文件的话，建议从编译的步骤开始自个手动编。像我就将脚本移除 cpp 文件的部分注释了，然后手动编译（结果发现没环境，最后看到作者有写要下环境~）

![](https://mmbiz.qpic.cn/mmbiz_jpg/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKo0VQwVlDsvLpv51ibm6BMibG2dk40W8aOrKicXxuNCjPbueG24OAWM8sg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKydhmNPXSvVElnDVBdBmx2T94CFDBzx1rktE6tLkGztXn5yLiczjicOWg/640?wx_fmt=jpeg)

模板 c++ 文件中对于类型转化的报错，项目中源码如下图，在 vs2017 上编译的话是会报类型不匹配的错的需要用到类型强转：  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKYLicecg73OwoARMLcRvPOCuBFIiaZjf9V3Cx40651EhDMgHPdJUSrLvQ/640?wx_fmt=png)  

改后的源码：  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKH9SEnsaiaOIrenzRBWN2YlphbsYWttKBdU1tzHjlJ6rppDmG2xK4Efg/640?wx_fmt=png)

模板 c++ 文件中对字符串的处理并没有加结束符，会导致解密后运行报错，所以需要在字符串末尾加上 **0x00**，就像这样：  

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKMibU5VoJ6AYes9Ierk6OnjyVNp0roGcbygpO74TQ5d3lSsciacbS72Hw/640?wx_fmt=png)  

当然，可以在脚本里面直接加：  

![](https://mmbiz.qpic.cn/mmbiz_jpg/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKwyNawVskaUXbgt9AxPF3mkFeMcBSXR24LJpt1CTQINIibRiaK28W825Q/640?wx_fmt=jpeg)

模板文件中的函数类型没有赋值，所以也会报错。需要加上类型说明和强制转换：

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKEhmWQPBCEDUqXJGhzuXQ1PtNGA0Ro7KVBZZDfeP0brf6RzDwqEkQhA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/yYePiaZj2cHibgq321Zxdn9KXiaIOlZGSlKiaNThF1AFD14mJSxHSrRxuwCmomWiaW8Do3ibHNe43CwuxyDufO6glvAQ/640?wx_fmt=png)

最后，祝大家上线如回家，免杀如喝水！！  

参考：https://github.com/9emin1/charlotte  

公众号