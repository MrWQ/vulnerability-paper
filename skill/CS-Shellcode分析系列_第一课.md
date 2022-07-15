> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzIyMjkzMzY4Ng==&mid=2247487086&idx=1&sn=281e468c8ba38d53a50bf9eae24772fe&chksm=e824a9b7df5320a1c105dd5fe484ff44f62a1421a1e1686a90cb5d7604bbb6532f3b45006457&scene=21#wechat_redirect)

**点击蓝字**

![图片](https://mmbiz.qpic.cn/mmbiz_gif/4LicHRMXdTzCN26evrT4RsqTLtXuGbdV9oQBNHYEQk7MPDOkic6ARSZ7bt0ysicTvWBjg4MbSDfb28fn5PaiaqUSng/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)

**关注我们**

  

  

**_声明  
_**

本文作者：Gality  
本文字数：3000

阅读时长：60分钟

附件/链接：点击查看原文下载

声明：请勿用作违法用途，否则后果自负

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCRdEUkWjnADMBeY9cRyYo7UwyjdSU8dcm3AzduFQpjTX8Cta5xQVGAdjdaNiae0yof2agC45uR2pg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

  

  

![](http://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDjy8pCtpvJKBibCLXQDm14MbdlTqXYESXADHkVpL6f81Z4TVFOGQMjBjgxPpUcYnzahRhibQUdcKzQ/0?wx_fmt=png)WgpSec狼组安全团队推荐搜索安全研究漏洞复现

  

  

  

**_前言_**

  

        本文是CS的shellcode分析的第一篇文章，该系列文章旨在帮助具有一定二进制基础的朋友看懂cs的shellcode的生成方式，进而可以达到对shellcode进行二进制层面的改变与混淆，用于免杀相关的研究。

一、

**_生成_**

首先设置一个监听器并生成一个原始格式的shellcode（Attacks -> Packages -> Payload Generator）

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmFlUCE0AAAUxQWAAljXic9mzHJhR0g0HPGzdicFJB6gOY2RpicNu3M4WhQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)  
这里我们就得到了一个原始的CS的shellcode：

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmpLy842WPbU05sIt46ib3gLj2M4ticFPALfHAnDaicfnX2CpuXl2h15A8A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

buf中的其实是二进制的可执行代码，然而该代码是没有办法直接运行的，因为他到可执行文件（exe）之间还差了一些必要的文件结构，所以我们需要写一个加载器去执行他，一个最简单的加载器如下：

```
`#include <windows.h>``int main()``{` `unsigned char Scode[] = "Your shellcode";` `//申请内存（权限为rwx）` `void* exec = VirtualAlloc(0, 1024, MEM_COMMIT, PAGE_EXECUTE_READWRITE);` `//将shellcode复制进申请的内存中` `RtlMoveMemory(exec, Scode, 1024);` `//执行shellcode` `((void(*)())exec)();` `return 0;``}`
```

用vs2019编译该C代码，选择Debug-X64模式编译，便于调试（这里的位数应与shellcode的位数保持一致）

生成exe后我们就可以对其进行静态/动态分析了

  

二、

**_静态分析_**

### **加载器部分**

使用IDA打开生成的exe

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmm4g4Be1JoSuUicaIYNHsNHkN6Tm6P67cPxzQEqwv3jibVHJVF30t1RsQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

可以看到main函数其实非常的短，除了由编译器自动生成的代码如checkForDeguggerJustMyCode这种外，我们重点注意两点，第一是图中黄色的unk_140019c30,这个地方其实就是shellcode的储存的位置

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmMYAmasviaXxzqaRic8lIrXqRuweud9JKG53FJA3a8M1KT4NiaibXia9Exlw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

这里通过逐字节的复制将shellcode放入到了[rbp+550+Src]的位置其实也就是rbp+10的位置，跟进unk_140019c30可以看到十六进制形式的shellcode：

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmLnz5pNvkH0K1KpdFeHnvqGGKXTJhGBXdUq33Ko3ORibfx9OUoMvfsWg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

另外一处就是标注evilCode的位置，上面看到memmove将[rbp+550h+Src]位置的shellcode复制到了[rbp+550h+var_1A8],然后直接call这个地址执行了shellcode代码，顺便说一句，x64的函数调用可以不依赖于栈实现，如memmove的参数就是通过寄存器来传递的，关于MSVC的x64函数调用可以参考官方文档

加载器部分基本就没什么可说的了，我们来看shellcode的部分，他又做了什么

  

### **shellcode部分**

我们可以使用IDApython来将shellcode导出出来

> IDApython是一个IDA增强插件，允许用户用python编写IDA脚本，IDA7.0自带IDApython，只需要确保本机装有相应的python环境即可（py2/py3均可），但是需要注意IDA7.0已经切换到x64构架了，所以对应的python版本也需要是x64版本才能正常使用，如果没有什么问题，那么当使用IDA打开任意exe时应会有类似的提示：
> 
> ```
> IDAPython Hex-Rays bindings initialized.  
> ---------------------------------------------------------------------------------------------  
> Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]   
> IDAPython 64-bit v7.4.0 final (serial 0) (c) The IDAPython Team <idapython@googlegroups.com>  
> ---------------------------------------------------------------------------------------------  
> 
> ```

首先从File选项中找到script command选项,并输入如下脚本：

```
`import idaapi``start_address = 0x140019C30 #替换成对应的shellcode的起始地址``data_length = 1024``data = idc.get_bytes(start_address , data_length)``fp = open('D:\\project\\CS-shellcode-analysis\\shellcode\\shellcode.bin', 'wb') #替换成保存的路径``fp.write(data)``fp.close()`
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmXbta58Cyhoiawyn7Yx0UJt7QYickJc66F9r7aHasPCKS0EE684EhhgAQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

执行后可以得到shellcode的原始文件（其实也就是刚刚生成的文件中buf部分按16进制写入的文件）

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmnPyPr9AjeqNdwmWBCLcc0E6SqfW5erqDMHTfyJiciaYTnFKjSWAMYkow/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

然后我们再用IDA打开这个文件进行分析：

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmAmevCdZRUXseIc4mMNmGRJKxCaMmwmYvW4wbbKLRyiaZZBvopa9RzPQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

先看第一个call的内容

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmMVwOLQiafISvVDjJsu928MOV3h7abda4Gicibr1NQus6q6fVzXCuZeGibg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

这里`pop rbp` 相当于将call的返回地址pop到了rbp中，然后把teniniw这个字符串放到了RCX中，这里由于是在栈上传递数据，所以其实是颠倒的wininet这个字符串，在动态调试时可以清晰的看到这点

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后后面`call rbp`就相当于返回刚刚代码中继续执行，其中的mov操作相当于是函数传参了

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmRmv4Nb9eoQWLA1HzMCuG7PibtS7XP22jIwvyXKN9m7XhUIHorQ7JP9Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

接着看，将参数压栈，然后取了gs段60h处的东西，这里gs段在用户态是指向TEB(Thread Environment Block，线程环境块)这个结构的

> 此结构体包含进程中运行的线程的各种信息，进程中的每个线程都对应一个 TEB 结构体,而TEB中又存储着PEB的地址，通过遍历PEB可以获取到kernel32和ntdll的基址(关于PEB的简介，可以参考这里)，进而实现调用系统函数，对于shellcode来说这是一种很常见的在程序中定位动态链接库的地址进而获取函数地址的方法，得到函数地址后就可以调用相应函数了，借助这篇文章我们也可以看到他的遍历方式
> 
> 为了看到TEB的结构信息，建议使用windbg在全局模式下使用`dt _TEB`来查看TEB的结构（因为微软的符号服务器被墙了= =所以说需要全局）

我们来看怎么手动遍历TEB并获取函数地址的：在gs:[60h]的位置是ProcessEnvironmentBlock(也就是PEB)这个结构里面(如果60h在User32Reversed中的话，是windbg调试的不是64位程序，随意调试一个64位程序就能看到如下的TEB表了)

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmtLkd0DAWtNVwCbXEuqzsRzxxXYDaic9icMKCOlVrwvKmLItMShf1ssPA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

也就是说现在取到了PEB的地址放入rdx，然后又接着取PEB的0x18h的内容，需要接着看PEB的结构：

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegmjPPUS4h9h43TAfYOSic6o65BUnnSfWTibyico2KpOvmhuYQyjlpiaQAS2g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

同样接着去看`_PEB_LDR_DATA`这个结构,又取了0x20这里：

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegm5kfMhlWFcm56FbaZZsIA1qwsozPJfVNlc9KkCibEA6PSNkuFrAEPibxA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

在接着往下说之前，我们先插入讲点PEB相关的东西。我们看到，在PEB_LDR_DATA结构中，又包含三个LIST_ENTRY结构体分别命名为:

```
InLoadOrderModuleList;                模块加载顺序  
InMemoryOrderModuleList;              模块在内存中的顺序  
InInitializationOrderModuleList;     模块初始化装载顺序  

```

LIST_ENTRY其结构定义如下：

```
typedef struct _LIST_ENTRY {  
   struct _LIST_ENTRY *Flink;  
   struct _LIST_ENTRY *Blink;  
} LIST_ENTRY, *PLIST_ENTRY, *RESTRICTED_POINTER PRLIST_ENTRY;  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

微软是怎么解释LIST_ENTRY结构中成员作用的呢?来看看MSDN

> The head of a doubly-linked list that contains the loaded modules for the process. Each item in the list is a pointer to an LDR_DATA_TABLE_ENTRY structure

这个双链表指向进程装载的模块，结构中的每个指针，指向了一个LDR_DATA_TABLE_ENTRY 的结构,同样可以通过`dt _LDR_DATA_TABLE_ENTRY`来查看该结构：

```
0:000> dt _LDR_DATA_TABLE_ENTRY  
ntdll!_LDR_DATA_TABLE_ENTRY  
   +0x000 InLoadOrderLinks : _LIST_ENTRY  
   +0x010 InMemoryOrderLinks : _LIST_ENTRY  
   +0x020 InInitializationOrderLinks : _LIST_ENTRY  
   +0x030 DllBase          : Ptr64 Void  
   +0x038 EntryPoint       : Ptr64 Void  
   +0x040 SizeOfImage      : Uint4B  
   +0x048 FullDllName      : _UNICODE_STRING  
   +0x058 BaseDllName      : _UNICODE_STRING  
   +0x068 FlagGroup        : [4] UChar  
   +0x068 Flags            : Uint4B  
   +0x068 PackagedBinary   : Pos 0, 1 Bit  
   +0x068 MarkedForRemoval : Pos 1, 1 Bit  
   +0x068 ImageDll         : Pos 2, 1 Bit  
   +0x068 LoadNotificationsSent : Pos 3, 1 Bit  
   +0x068 TelemetryEntryProcessed : Pos 4, 1 Bit  
   +0x068 ProcessStaticImport : Pos 5, 1 Bit  
   +0x068 InLegacyLists    : Pos 6, 1 Bit  
   +0x068 InIndexes        : Pos 7, 1 Bit  
   +0x068 ShimDll          : Pos 8, 1 Bit  
   +0x068 InExceptionTable : Pos 9, 1 Bit  
   +0x068 ReservedFlags1   : Pos 10, 2 Bits  
   +0x068 LoadInProgress   : Pos 12, 1 Bit  
   +0x068 LoadConfigProcessed : Pos 13, 1 Bit  
   +0x068 EntryProcessed   : Pos 14, 1 Bit  
   +0x068 ProtectDelayLoad : Pos 15, 1 Bit  
   +0x068 ReservedFlags3   : Pos 16, 2 Bits  
   +0x068 DontCallForThreads : Pos 18, 1 Bit  
   +0x068 ProcessAttachCalled : Pos 19, 1 Bit  
   +0x068 ProcessAttachFailed : Pos 20, 1 Bit  
   +0x068 CorDeferredValidate : Pos 21, 1 Bit  
   +0x068 CorImage         : Pos 22, 1 Bit  
   +0x068 DontRelocate     : Pos 23, 1 Bit  
   +0x068 CorILOnly        : Pos 24, 1 Bit  
   +0x068 ChpeImage        : Pos 25, 1 Bit  
   +0x068 ReservedFlags5   : Pos 26, 2 Bits  
   +0x068 Redirected       : Pos 28, 1 Bit  
   +0x068 ReservedFlags6   : Pos 29, 2 Bits  
   +0x068 CompatDatabaseProcessed : Pos 31, 1 Bit  
   +0x06c ObsoleteLoadCount : Uint2B  
   +0x06e TlsIndex         : Uint2B  
   +0x070 HashLinks        : _LIST_ENTRY  
   +0x080 TimeDateStamp    : Uint4B  
   +0x088 EntryPointActivationContext : Ptr64 _ACTIVATION_CONTEXT  
   +0x090 Lock             : Ptr64 Void  
   +0x098 DdagNode         : Ptr64 _LDR_DDAG_NODE  
   +0x0a0 NodeModuleLink   : _LIST_ENTRY  
   +0x0b0 LoadContext      : Ptr64 _LDRP_LOAD_CONTEXT  
   +0x0b8 ParentDllBase    : Ptr64 Void  
   +0x0c0 SwitchBackContext : Ptr64 Void  
   +0x0c8 BaseAddressIndexNode : _RTL_BALANCED_NODE  
   +0x0e0 MappingInfoIndexNode : _RTL_BALANCED_NODE  
   +0x0f8 OriginalBase     : Uint8B  
   +0x100 LoadTime         : _LARGE_INTEGER  
   +0x108 BaseNameHashValue : Uint4B  
   +0x10c LoadReason       : _LDR_DLL_LOAD_REASON  
   +0x110 ImplicitPathOptions : Uint4B  
   +0x114 ReferenceCount   : Uint4B  
   +0x118 DependentLoadFlags : Uint4B  
   +0x11c SigningLevel     : UChar  

```

所以[rdx+50h]就指向了FullDllName这个`_UNICODE_STRING`的结构体：

```
0:000> dt _UNICODE_STRING  
ntdll!_UNICODE_STRING  
   +0x000 Length           : Uint2B  
   +0x002 MaximumLength    : Uint2B  
   +0x008 Buffer           : Ptr64 Wchar  

```

换算下应该是0x48+0x8=0x50，也就是Buffer的内容，这里存储的就是Dll的全名，可以通过这个名字确定当前遍历到的dll是不是自己想要的，默认第一个指向的就是自己这个程序，我们可以通过一个Demo来证实：

```
`#include <stdio.h>``int main()``{` `void* peb = 0;` `void* PEB_LDR_DATA = 0;` `void* InMemoryOrderModuleList = 0;` `wchar_t* DllName = 0;` `__asm {` `mov rdx, gs:[60h]` `mov peb, rdx` `mov rdx, [rdx+18h]` `mov PEB_LDR_DATA, rdx` `mov rdx, [rdx+20h]` `mov InMemoryOrderModuleList, rdx` `mov rdx, [rdx + 50h]` `mov DllName, rdx` `}` `printf("peb address:\t%p\n", peb);` `printf("PEB_LDR_DATA address:\t%p\n", PEB_LDR_DATA);` `printf("InMemoryOrderModuleList address:\t%p\n", InMemoryOrderModuleList);` `printf("Dllname address:\t%p\n", DllName);` `wprintf(L"DllName:\t%s\n", DllName);` `return 0;``}`
```

注意，这里由于msvc是不支持64位的C++内嵌汇编的，所以想运行如上代码需要做以下设置：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如果没有`llvm(clang-cl)`这个选项可以通过visual studio 2019 installer来安装：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后运行就可以验证我们刚刚说的：

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegma0jw56szvlF9sgDVmYoSjSWX1Wb3mzQAe3ib4mVUSFDVMibljL62udFg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

那么再借助`_LIST_ENTRY`就可以遍历这整个由`_LIST_ENTRY` 组织起来的双向循环链表了。

我们接着看shellcode代码：

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegm02RE23ibJU1QTH2gzibHgib0m86UfGCo9jCRe8VPsFXu0EuIdu2VvVTbQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

这里将模块名放入rsi，最大长度放入rcx，之后做了一步字符变大写的操作（如果字符小于a，那么ASCII值减0x20，正好变成对应的大写字符），便于后面进行比较，具体怎么比较的，师傅们可以先自己尝试看能不能看懂。

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDbmIfZu2n2cMbArWltiaegm3JOXOVz8UYVfsHgFl221t2U3L3AZy5ucBgzTy5MXrLIibmOIHmtEyibg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)  
OK，这篇文章就先到这里，有上述铺垫后各位师傅可以自己尝试手撸汇编来遍历整个`_LDR_DATA_TABLE_ENTRY`结构来获取ntdll和kernel32的地址来调用函数，这是木马很常见的一种调用系统函数的方式，同时遍历方法也比较多变，可以在这里做文章对shellcode进行混淆，也可以接着阅读shellcode代码，剩下的部分我会在下一篇文章中接着说。

  

  

**_后记_**

  

  

  

**有想一起研究免杀技术或者二进制技术的师傅萌**

**简历请砸** **Gality@wgpsec.org****，欢迎各位师傅一起交流学习**

  

**【系列文章在c.wgpsec.org 狼组安全社区小书连载，可免费阅读】**  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

  

**_扫描关注公众号回复加群_**

**_和师傅们一起讨论研究~_**

  

**长**

**按**

**关**

**注**

**WgpSec狼组安全团队**

微信号：wgpsec

Twitter：@wgpsec

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)