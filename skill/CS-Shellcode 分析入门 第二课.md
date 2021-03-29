> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/uQjkf5fTf8s_qAOwZkcpLA)

**点击蓝字**

![](https://mmbiz.qpic.cn/mmbiz_gif/4LicHRMXdTzCN26evrT4RsqTLtXuGbdV9oQBNHYEQk7MPDOkic6ARSZ7bt0ysicTvWBjg4MbSDfb28fn5PaiaqUSng/640?wx_fmt=gif)

**关注我们**

  

**_声明  
_**

本文作者：Gality  
本文字数：3700

阅读时长：20~30 分钟

附件 / 链接：点击查看原文下载

**本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载**

  

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，狼组安全团队以及文章作者不为此承担任何责任。

狼组安全团队有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经狼组安全团队允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCRdEUkWjnADMBeY9cRyYo7UwyjdSU8dcm3AzduFQpjTX8Cta5xQVGAdjdaNiae0yof2agC45uR2pg/640?wx_fmt=png)

![](http://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDjy8pCtpvJKBibCLXQDm14MbdlTqXYESXADHkVpL6f81Z4TVFOGQMjBjgxPpUcYnzahRhibQUdcKzQ/0?wx_fmt=png)WgpSec 狼组安全团队推荐搜索安全工具安全研究漏洞复现

  

**_前言_**

  

        本文是 [CS-Shellcode 分析系列 第一课](http://mp.weixin.qq.com/s?__biz=MzIyMjkzMzY4Ng==&mid=2247487086&idx=1&sn=281e468c8ba38d53a50bf9eae24772fe&chksm=e824a9b7df5320a1c105dd5fe484ff44f62a1421a1e1686a90cb5d7604bbb6532f3b45006457&scene=21#wechat_redirect) 第二篇文章，该系列文章旨在帮助具有一定二进制基础的朋友看懂 cs 的 shellcode 的生成方式，进而可以达到对 shellcode 进行二进制层面的改变与混淆，用于免杀相关的研究

免杀加载器：https://github.com/wgpsec/CS-Avoid-killing

一、

**_SehllCode 分析_**

        接上文, 我们接着说, 具体怎么比较的. 其实在前面有段代码的一个细节我是直接略过没有提的, 不知道师傅萌是否有疑问, 就是这个  

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7KlxltYrXerluWcyKSYHtvdCJVspOR9xZSs4icR7Bibb6rbYoqmQ8IzRnGQ/640?wx_fmt=png)

最开始的跳转中其实传递了一个`726774C`的 16 进制值, 这个值有什么含义呢, 这个会在这一篇中说到

我们直接来看后续的操作:

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7Kl37FAibtoBhUCO68sUBibI9F5W7fSZZ0XfWSib1ZWW9xWW53rqvwibNWraA/640?wx_fmt=png)

        这个部分的操作比较诡异, 上文说到了这里有一步将小写字母变大写字母的操作, rcx 中存的是当前程序名的长度, 然后后续`ror r9d, 0Dh`以及`add r9d, eax`这两步其实是在做一个类似于求特征值的这么一个操作, `lodsb`从 rsi 指向的地方取字符 (也就是程序名字符串), 然后通过 ror 的循环右移以及加法, 对应求出了该字符串的一个特征值, 这里我想了很多天也没有想清楚为什么一定是右移`0xD`次, 整个 shellcode 中求字符串特征值的操作都是通过这种循环右移取特征值的方式来计算的, 是否有什么理论基础如果有师傅懂的话请务必评论赐教 Orz(只查到说是这是一套用于将当前函数名称转化为 DWORD 的 hash 数据值的算法，目的是方便比对)

在将自己程序字符全部大写取特征字符串后压栈, 然后就是如下操作

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7Kl70RyntuyvUicBPicZPUiaibRNQz8icl9VYibZuEJxNhwH8TgD3QqptIC6qXg/640?wx_fmt=png)

        这里 rdx 还是指向之前的`_LDR_DATA_TABLE_ENTRY`这个结构， 同样是查表， 可以发现取到了其 0x20h 对应的`InMemoryOrderLinks`这一项对应的值，为什么是对应`InMemoryOrderLinks`, 是因为其实在`_PEB_LDR_DATA`中 `InMemoryOrderModuleList`成员的指向的是`_LDR_DATA_TABLE_ENTRY`中`InMemoryOrderLinks`成员的地址，也就是说此时通过`InMemoryOrderModuleList`找到的`_LDR_DATA_TABLE_ENTRY`结构的地址并不是该结构的起始地址，真实的起始地址还需要减`0x10`, 所以说该`_LDR_DATA_TABLE_ENTRY`的真实起始地址其实是`rdx-10`, 所以`[rdx+20]`减去偏移后其实是该`_LDR_DATA_TABLE_ENTRY`结构的 0x30 处的偏移，也就是 DllBase 这个成员， 该成员存储了该 dll 的基地址，此时，rdx 指向 Dll 的基地址

> PEB 里的 ldr 域中的那三个值 (Ldr.InInitializationOrderModuleList Ldr.InLoadOrderModuleList Ldr.InMemoryOrderModuleList) 并不是直接就是链表中_ldr_data_table_entry 结构体的基址
> 
> Ldr.InLoadOrderModuleList 的值指向的是`_ldr_data_table_entry`中 InLoadOrderLinks 成员的地址 (恰恰是`_ldr_data_table_entry`的基址, 因为 InLoadOrderLinks 正是该结构体的第一个成员), Ldr.InMemoryOrderModuleList 的值指向的是`_ldr_data_table_entry`中 InMemoryOrderLinks 成员的地址, 同样, Ldr.InInitializationOrderModuleList 的值指向的是`_ldr_data_table_entry`中 InInitializationOrderLinks 成员的地址. 因此, 使用 Ldr.InMemoryOrderModuleList 和 Ldr.InInitializationOrderModuleList 进行链表遍历查看的时候, 应该将其值相应的减去 0x10 和 0x20 才对, 通过 windbg 也可以证实这一点：
> 
> ```
> 1:001> dt _LDR_DATA_TABLE_ENTRY
> ntdll!_LDR_DATA_TABLE_ENTRY
>    +0x000 InLoadOrderLinks : _LIST_ENTRY
>    +0x010 InMemoryOrderLinks : _LIST_ENTRY
>    +0x020 InInitializationOrderLinks : _LIST_ENTRY
>    +0x030 DllBase          : Ptr64 Void
>    +0x038 EntryPoint       : Ptr64 Void
>    +0x040 SizeOfImage      : Uint4B
>    +0x048 FullDllName      : _UNICODE_STRING
>    +0x058 BaseDllName      : _UNICODE_STRING
>    +0x068 FlagGroup        : [4] UChar
>    +0x068 Flags            : Uint4B
>    +0x068 PackagedBinary   : Pos 0, 1 Bit
>    +0x068 MarkedForRemoval : Pos 1, 1 Bit
>    +0x068 ImageDll         : Pos 2, 1 Bit
>    +0x068 LoadNotificationsSent : Pos 3, 1 Bit
>    +0x068 TelemetryEntryProcessed : Pos 4, 1 Bit
>    +0x068 ProcessStaticImport : Pos 5, 1 Bit
>    +0x068 InLegacyLists    : Pos 6, 1 Bit
>    +0x068 InIndexes        : Pos 7, 1 Bit
>    +0x068 ShimDll          : Pos 8, 1 Bit
>    +0x068 InExceptionTable : Pos 9, 1 Bit
>    +0x068 ReservedFlags1   : Pos 10, 2 Bits
>    +0x068 LoadInProgress   : Pos 12, 1 Bit
>    +0x068 LoadConfigProcessed : Pos 13, 1 Bit
>    +0x068 EntryProcessed   : Pos 14, 1 Bit
>    +0x068 ProtectDelayLoad : Pos 15, 1 Bit
>    +0x068 ReservedFlags3   : Pos 16, 2 Bits
>    +0x068 DontCallForThreads : Pos 18, 1 Bit
>    +0x068 ProcessAttachCalled : Pos 19, 1 Bit
>    +0x068 ProcessAttachFailed : Pos 20, 1 Bit
>    +0x068 CorDeferredValidate : Pos 21, 1 Bit
>    +0x068 CorImage         : Pos 22, 1 Bit
>    +0x068 DontRelocate     : Pos 23, 1 Bit
>    +0x068 CorILOnly        : Pos 24, 1 Bit
>    +0x068 ChpeImage        : Pos 25, 1 Bit
>    +0x068 ReservedFlags5   : Pos 26, 2 Bits
>    +0x068 Redirected       : Pos 28, 1 Bit
>    +0x068 ReservedFlags6   : Pos 29, 2 Bits
>    +0x068 CompatDatabaseProcessed : Pos 31, 1 Bit
>    +0x06c ObsoleteLoadCount : Uint2B
>    +0x06e TlsIndex         : Uint2B
>    +0x070 HashLinks        : _LIST_ENTRY
>    +0x080 TimeDateStamp    : Uint4B
>    +0x088 EntryPointActivationContext : Ptr64 _ACTIVATION_CONTEXT
>    +0x090 Lock             : Ptr64 Void
>    +0x098 DdagNode         : Ptr64 _LDR_DDAG_NODE
>    +0x0a0 NodeModuleLink   : _LIST_ENTRY
>    +0x0b0 LoadContext      : Ptr64 _LDRP_LOAD_CONTEXT
>    +0x0b8 ParentDllBase    : Ptr64 Void
>    +0x0c0 SwitchBackContext : Ptr64 Void
>    +0x0c8 BaseAddressIndexNode : _RTL_BALANCED_NODE
>    +0x0e0 MappingInfoIndexNode : _RTL_BALANCED_NODE
>    +0x0f8 OriginalBase     : Uint8B
>    +0x100 LoadTime         : _LARGE_INTEGER
>    +0x108 BaseNameHashValue : Uint4B
>    +0x10c LoadReason       : _LDR_DLL_LOAD_REASON
>    +0x110 ImplicitPathOptions : Uint4B
>    +0x114 ReferenceCount   : Uint4B
>    +0x118 DependentLoadFlags : Uint4B
>    +0x11c SigningLevel     : UChar
> 
> ```
> 
> 可以看到`InLoadOrderModuleList`和`InMemoryOrderModuleList`的 Flink 与 Blink 都差了 0x10 的长度，InInitializationOrderModuleList 同理

这里再次放一个`_LDR_DATA_TABLE_ENTRY`结构, 方便对照：

```
IMAGE_DOS_HEADER {
    WORD   e_magic;                // +0000h   -   EXE标志，“MZ”
    WORD   e_cblp;                 // +0002h   -   最后（部分）页中的字节数
    WORD   e_cp;                   // +0004h   -   文件中的全部和部分页数
    WORD   e_crlc;                 // +0006h   -   重定位表中的指针数
    WORD   e_cparhdr;              // +0008h   -   头部尺寸，以段落为单位
    WORD   e_minalloc;             // +000ah   -   所需的最小附加段
    WORD   e_maxalloc;             // +000ch   -   所需的最大附加段
    WORD   e_ss;                   // +000eh   -   初始的SS值（相对偏移量）
    WORD   e_sp;                   // +0010h   -   初始的SP值
    WORD   e_csum;                 // +0012h   -   补码校验值
    WORD   e_ip;                   // +0014h   -   初始的IP值
    WORD   e_cs;                   // +0016h   -   初始的CS值
    WORD   e_lfarlc;               // +0018h   -   重定位表的字节偏移量
    WORD   e_ovno;                 // +001ah   -   覆盖号
    WORD   e_res[4];               // +001ch   -   保留字00
    WORD   e_oemid;                // +0024h   -   OEM标识符
    WORD   e_oeminfo;              // +0026h   -   OEM信息
    WORD   e_res2[10];             // +0028h   -   保留字
    LONG   e_lfanew;               // +003ch   -   PE头相对于文件的偏移地址
  }

```

而我们知道 dll 的结构其实跟 PE 的文件结构基本是一致的，dll 的头也是由 DOS 头，PE 头等组成的

> PE 结构可以大致分为:
> 
> *   DOS 部分
>     
> *   PE 文件头
>     
> *   节表 (块表)
>     
> *   节数据 (块数据)
>     
> *   调试信息
>     

此时 rdx 指向的就是 dos 头的起始，这里提供一个 dos 头的定义：

```
IMAGE_NT_HEADERS {
    DWORD Signature;                      // +0000h   -   PE文件标识，“PE00”
    IMAGE_FILE_HEADER FileHeader;                   // +0004h   -   PE标准头
    IMAGE_OPTIONAL_HEADER32 OptionalHeader;         // +0018h   -   PE扩展头
}

```

我们可以看到 0x3c 处储存了 e_lfanew，该变量指明了 PE 头相对于文件的偏移地址， 所以`rdx+3c`处得到的偏移值加上基地址就是该 dll 的 PE 头的地址。

而 PE 头的结构如下：

```
typedef struct _IMAGE_OPTIONAL_HEADER64 {
    WORD        Magic; // +0018h   -   标志字, ROM 映像（0107h）,32位普通可执行文件（010Bh）,64位可执行文件（0x20B）。
    BYTE        MajorLinkerVersion;
    BYTE        MinorLinkerVersion;

    //以下3个字段都是FileAlignment的整数倍，已弃用。
    DWORD       SizeOfCode;
    DWORD       SizeOfInitializedData;
    DWORD       SizeOfUninitializedData;

    DWORD       AddressOfEntryPoint;    //RVA address!!!!

    DWORD       BaseOfCode;


    ULONGLONG   ImageBase;        
    DWORD       SectionAlignment;        //内存中区块的对齐大小 0x1000==4kB
    DWORD       FileAlignment;            //文件中区块的对齐大小 0x0200==512B


    WORD        MajorOperatingSystemVersion;
    WORD        MinorOperatingSystemVersion;
    WORD        MajorImageVersion;
    WORD        MinorImageVersion;
    WORD        MajorSubsystemVersion;
    WORD        MinorSubsystemVersion;
    DWORD       Win32VersionValue;
    DWORD       SizeOfImage;
    DWORD       SizeOfHeaders;
    DWORD       CheckSum;
    WORD        Subsystem;        //how to build the initial gui
    WORD        DllCharacteristics;
    ULONGLONG   SizeOfStackReserve;
    ULONGLONG   SizeOfStackCommit;
    ULONGLONG   SizeOfHeapReserve;
    ULONGLONG   SizeOfHeapCommit;
    DWORD       LoaderFlags;
    DWORD       NumberOfRvaAndSizes; 
    IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES]; //0x88
} IMAGE_OPTIONAL_HEADER64, *PIMAGE_OPTIONAL_HEADER64;

```

这里 PE 标准头的内容我们暂且不关注，看 0x18 处，也就是 PE 扩展头的结构：

该位置是一个魔数，用于标明类型：

```
typedef struct _IMAGE_EXPORT_DIRECTORY {
    DWORD   Characteristics;        // +0000h
    DWORD   TimeDateStamp;          // +0004h
    WORD    MajorVersion;           // +0008h
    WORD    MinorVersion;           // +000Ah
    DWORD   Name;                   // +000Ch
    DWORD   Base;                   // +0010h
    DWORD   NumberOfFunctions;      // +0014h
    DWORD   NumberOfNames;          // +0018h 以函数名字导出的函数个数
    DWORD   AddressOfFunctions;     // +001Ch  导出函数地址表RVA:存储所有导出函数地址(表元素宽度为4，总大小NumberOfFunctions * 4)
    DWORD   AddressOfNames;         // +0020h  存储函数名字符串所在的地址RVA(表元素宽度为4，总大小为NumberOfNames * 4)
    DWORD   AddressOfNameOrdinals;  // +0024h  存储函数序号RVA(表元素宽度为2，总大小为NumberOfNames * 2)
} IMAGE_EXPORT_DIRECTORY, *PIMAGE_EXPORT_DIRECTORY;

```

所以，这里我们就明白了`cmp word ptr [rax+18h], 20Bh`这一步其实就是判断是否是 64 位可行文件，如果是，则将 PE 头 0x88 处的值放入 eax 中，同样去找该偏移对应的是什么，可以看到在 0x78 后是 16 个 IMAGE_DATA_DIRECTORY 结构

> 数据目录项 IMAGE_DATA_DIRECTORY
> 
> *   IMAGE_OPTIONAL_HEADER 结构的最后一个字段为 DataDirectory。
>     
> *   该字段定义了 PE 文件中出现的所有不同类型的数据的目录信息，从 Windows NT 3.1 操作系统开始到现在，该数据目录中定义的数据类型一直是 16 种。
>     
> *   PE 中使用了一种称作 “数据目录项 IMAGE_DATA_DIRECTORY” 的数据结构来定义每种数据。
>     
> 
> ```
> typedef struct _IMAGE_DATA_DIRECTORY {
>   DWORD VirtualAddress;                   /**指向某个数据的相对虚拟地址   RAV  偏移0x00**/
>   DWORD Size;                             /**某个数据块的大小                 偏移0x04**/
> } IMAGE_DATA_DIRECTORY, *PIMAGE_DATA_DIRECTORY;
> 
> 
> ```
> 
> *   总的数据目录一共由 16 个相同的 IMAGE_DATA_DIRECTORY 结构连续排列在一起组成。
>     
> *   如果想在 PE 文件中寻找特定类型的数据，就需要从该结构开始。
>     
> *   这 16 个元组的数组每一项均代表 PE 中的某一个类型的数据，各数据类型为:
>     
> *   ![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7KlTk5zruF6lgEujBRZ9k1ZLSGZoPY37rKjkc0YVdWG2wNxN8ZRLibNUiag/640?wx_fmt=png)
>     

所以其实这里获取到了第一项也就是导出表的 RVA， 而我们知道 dll 是一定有导出表的，而一般 exe 没有导出表，所以这里为 0，表示不存在导出表

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7Klibia359uyLNGMM00mia6Jy0uicFtON4ZlaS1dTd7oIlLBUkyqf9Uc9lyPg/640?wx_fmt=png) 所以这里就相当于判断了是不是 dll，如果是，则 rax 不为 0，流程接着往后走，而如果不是，rax 会为 0，则跳转 loc_c7

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7Kl4xGrLj61OxWNP8CBuFlkT9wkg4ksSjueUpwSjrB893S6auCZRjHmEw/640?wx_fmt=png)

这里`pop`出了 r9 和 rdx， 将 rdx 指向的值放入 rdx 中并跳转到`loc_21`处， 这里弹出的两个值就是之前压栈的 r9 和 rdx 的值， 对应着本程序名的特征字符串和`_LDR_DATA_TABLE_ENTRY`的地址， 然后`mov rdx, [rdx]`就是取`InMemoryOrderLinks`中的`Flink`的值存入了 rdx， 对应着模块加载顺序中的前一个`_LDR_DATA_TABLE_ENTRY`的地址，而后就是一样的操作开始循环`InMemoryOrderLinks`这个列表中的`_LDR_DATA_TABLE_ENTRY`结构了

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7Klpic8QMyMtSpq0FtmCmhib5Q0JicFMk3wE1UUib8bXRKMRmmhV6a626nX9Q/640?wx_fmt=png)

为了便于理解，梳理整个流程， 我做了如下的图表：

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7KlcMcJbbUoia0kEqortKEMEHZsm3QeGJvXmWibGK2kVk3f8l5xXs1LHswA/640?wx_fmt=png)

那么， 当遍历的模块是个 dll 时，会执行如下操作：

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7KlAPUnGJwvDIRHT2ibhiaGSoswdTBibCtvosiamyYc8uaAPkLr3hviaqJRqmg/640?wx_fmt=png)

`add rax，rdx`并`push rax`， 我们之前说了 Export Directoy RVA 储存的是相对虚拟地址，可以理解为文件被装载到虚拟内存 (拉伸) 后先对于基址的偏移地址，所以基址加 RVA 得到其导出表 (IMAGE_EXPORT_DIRECTORY) 的真实地址，而该表的定义又如下：

所以又分别将 NumberOfNames 放入 ecx，AddressOfNames 放入 r8d, 为后面遍历所有导出函数做准备， `add r8, rdx`取到了导出函数名字符串储存地址表

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCicmtP2h2SM3ukEYyySF7KlfChs8zSoxPrXnWYlSguXqicBCU8LHHHSyXuInCYUibnhMiaSib3cHMHsicQ/640?wx_fmt=png)

接着其实就是对遍历所有函数名，求函数名的特征字符值，然后与`726774C`进行比较（`726774C`存在 r10d 中）如果不同，则代表不是想要的函数，如果是则进行后面的步骤。而该值，其实就是 LoadLibraryA 函数的特征字符值，由于需要自己加载 dll，而又不想在程序中直接出现调用 LoadLibraryA 的特征，所以只能使用这种方法来找到该函数的地址来调用他，这种调用方式在 shellcode 中非常常见，是一种通用的 shellcode 调用 LoadLibraryA 的方式，同时也比较隐蔽

        这一章就先到这里，通过到目前为止的分析，我们已经可以找到 LoadLibraryA 函数的地址用于调用，那么后续如何，请听下回分解

  

**_后记_**

  

有想一起研究免杀技术或者二进制技术的师傅萌，简历请砸 Gality@wgpsec.org，欢迎各位师傅一起交流学习

公众号

**_扫描关注公众号回复加群_**

**_和师傅们一起讨论研究~_**

  

**长**

**按**

**关**

**注**

**WgpSec 狼组安全团队**

微信号：wgpsec

Twitter：@wgpsec

![](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzBhAsD8IU7jiccdSHt39PeyFafMeibktnt9icyS2D2fQrTSS7wdMicbrVlkqfmic6z6cCTlZVRyDicLTrqg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/gdsKIbdQtWAicUIic1QVWzsMLB46NuRg1fbH0q4M7iam8o1oibXgDBNCpwDAmS3ibvRpRIVhHEJRmiaPS5KvACNB5WgQ/640?wx_fmt=gif)