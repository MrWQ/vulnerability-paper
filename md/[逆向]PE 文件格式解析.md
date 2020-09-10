\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.cnblogs.com\](https://www.cnblogs.com/-mo-/p/12659333.html)

简单对 PE 文件做一个格式上的概括，随笔记点东西，可能会存在部分疏漏，初学者可以拿来入门随便看看。

### 0x01 简介

PE（Portable Execute）文件是 Windows 下可执行文件的总称，常见的有 DLL， EXE， OCX，SYS 等，事实上，一个文件是否是 PE 文件与其扩展名无关， PE 文件可以是任何扩展名。那 Windows 是怎么区分可执行文件和非可执行文件的呢？我们调用 LoadLibrary 传递了一个文件名，系统是如何判断这个文件是一个合法的动态库呢？这就涉及到 PE 文件结构了。PE 文件的结构一般来说如下图所示：从起始位置开始依次是 DOS 头， NT 头，节表以及具体的节。

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200408125343199-290496379.png)

这里拿 windows 系统目录中的 ndis.sys 当做一个 PE 文件例子

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200408134041766-857218536.png)

### 0x02 DOS 头

DOS 头是用来兼容 MS-DOS 操作系统的，目的是当这个文件在 MS-DOS 上运行时提示一段文字，大部分情况下是： This program cannot be run in DOS mode. 还有一个目的，就是指明 NT 头在文件中的位置。

```
typedef struct \_IMAGE\_DOS\_ { // DOS .EXE header
    // offset: 0H
    WORD e\_magic; // Magic number
    // offset: 2H
    WORD e\_cblp; // Bytes on last page of file
    // offset: 4H
    WORD e\_cp; // Pages in file
    // offset: 6H
    WORD e\_crlc; // Relocations
    // offset: 8H
    WORD e\_cparhdr; // Size of header in paragraphs
    // offset: AH
    WORD e\_minalloc; // Minimum extra paragraphs needed
    // offset: CH
    WORD e\_maxalloc; // Maximum extra paragraphs needed
    // offset: EH
    WORD e\_ss; // Initial (relative) SS value
    // offset: 10H
    WORD e\_sp; // Initial SP value
    // offset: 12H
    WORD e\_csum; // Checksum
    // offset: 14h
    WORD e\_ip; // Initial IP value
    // offset: 16H
    WORD e\_cs; // Initial (relative) CS value
    // offset: 18H
    WORD e\_lfarlc; // File address of relocation table
    // offset: 1AH
    WORD e\_ovno; // Overlay number
    // offset: 1CH
    WORD e\_res\[4\]; // Reserved words
    // offset: 24H
    WORD e\_oemid; // OEM identifier (for e\_oeminfo)
    // offset: 26H
    WORD e\_oeminfo; // OEM information; e\_oemid specific
    // offset: 28H
    WORD e\_res2\[10\]; // Reserved words
    // offset: 3CH
    LONG e\_lfanew; // File address of new exe header
} IMAGE\_DOS\_HEADER, \*PIMAGE\_DOS\_HEADER;

#注： WORD 为一个 16bit 的无符号数


```

#### 2.1 e\_magic

e\_magic 是 一个 WORD 类型， 值是一个常数 0x4D5A，用文本编辑器查看该值位‘MZ’，可执行文件必须都是'MZ'开头。

注：4DH 为 M 的 ASCLL 码的 16 进制, 5AH 为 Z 的 ASCLL 码的 16 进制。

#### 2.2 e\_lfanew

e\_lfanew 为 32 位可执行文件扩展的域，用来表示 DOS 头之后的 NT 头相对文件起始地址的偏移。

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200408131153584-2134420048.png)

### 0x03 NT 头

NT 头包含 windows PE 文件的主要信息，其中包括一个‘PE’字样的签名， PE 文件头（IMAGE\_FILE\_HEADER）和 PE 可选头（IMAGE\_OPTIONAL\_HEADER32）。

```
typedef struct \_IMAGE\_NT\_HEADERS {
    // offset: 0H
    DWORD Signature;
    // offset: 4H
    IMAGE\_FILE\_HEADER FileHeader;
    // offset: 18H
    IMAGE\_OPTIONAL\_HEADER32 OptionalHeader;
} IMAGE\_NT\_HEADERS32, \*PIMAGE\_NT\_HEADERS32;


```

#### 3.1 Signature

类似于 DOS 头中的 e\_magic，其高 16 位是 0，低 16 是 0x4550，用字符表示是’PE’。  
批： 45H 为 P 的 ASCLL 码的 16 进制, 50H 为 E 的 ASCLL 码 16 进制。

#### 3.2 IMAGE\_FILE\_HEADER

IMAGE\_FILE\_HEADER 是 PE 文件头， C 语言的定义是这样的：

```
typedef struct \_IMAGE\_FILE\_HEADER {
    +4H WORD Machine;
    +6H WORD NumberOfSections;
    +8H DWORD TimeDateStamp;
    +CH DWORD PointerToSymbolTable;
    +10H DWORD NumberOfSymbols;
    +14H WORD SizeOfOptionalHeader;
    +16H WORD Characteristics;
} IMAGE\_FILE\_HEADER, \*PIMAGE\_FILE\_HEADER;


```

每个域的具体含义：

```
Machine              显示该文件的运行平台，是 x86、 x64 还是 I64 等等，常见的值列举如下：
                     #define IMAGE\_FILE\_MACHINE\_I386 0x014c    // Intel 386.
                     #define IMAGE\_FILE\_MACHINE\_ARM 0x01c0     // ARM
                     #define IMAGE\_FILE\_MACHINE\_POWERPC 0x01F0 // IBM PowerPC
                     #define IMAGE\_FILE\_MACHINE\_IA64 0x0200    // Intel 64
                     #define IMAGE\_FILE\_MACHINE\_AMD64 0x8664   // AMD64 (K8)

NumberOfSections     该 PE 文件中有多少个节，也就是节表中的项数。
TimeDateStamp        PE 文件的创建时间，一般有连接器填写。 表明文件是何时被创建的。这个值是自 1970 年 1 月 1 日以来用格林威治时间（GMT）计算的秒数
PointerToSymbolTable COFF 文件符号表在文件中的偏移，主要指向调式信息
NumberOfSymbols      符号表的数量。
SizeOfOptionalHeader 紧随其后的可选头的大小,对于 32 位系统，通常为 0X00E0H ,64 位系统为 0X00F0H 。
Characteristics      可执行文件的属性，定义在 winnt.h 头文件中。


```

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200408142726775-1608662988.png)

#### 3.3 IMAGE\_OPTIONAL\_HEADER32

IMAGE\_OPTIONAL\_HEADER32 是 PE 可选头，别看他名字叫可选头，其实一点都不能少， 它在不同的平台下是不一样的，例如 32 位下是 IMAGE\_OPTIONAL\_HEADER32，而在 64 位下是 IMAGE\_OPTIONAL\_HEADER64。为了简单起见，我们只看 32 位：

```
typedef struct \_IMAGE\_OPTIONAL\_HEADER {

// 必选部分
+18H WORD Magic;
+1AH BYTE MajorLinkerVersion;
+1BH BYTE MinorLinkerVersion;
+1CH DWORD SizeOfCode;
+20H DWORD SizeOfInitializedData;
+24H DWORD SizeOfUninitializedData;
+28H DWORD AddressOfEntryPoint;
+2CH DWORD BaseOfCode;
+30H DWORD BaseOfData;

// 可选部分
+34H DWORD ImageBase;
+38H DWORD SectionAlignment;
+3CH DWORD FileAlignment;
+40H WORD MajorOperatingSystemVersion;
+42H WORD MinorOperatingSystemVersion;
+44H WORD MajorImageVersion;
+46H WORD MinorImageVersion;
+48H WORD MajorSubsystemVersion;
+4AH WORD MinorSubsystemVersion;
+4CH DWORD Win32VersionValue;
+50H DWORD SizeOfImage;
+54H DWORD SizeOfHeaders;
+58H DWORD CheckSum;
+5CH WORD Subsystem;
+5EH WORD DllCharacteristics;
+60H DWORD SizeOfStackReserve;
+64H DWORD SizeOfStackCommit;
+68H DWORD SizeOfHeapReserve;
+6CH DWORD SizeOfHeapCommit;
+70H DWORD LoaderFlags;
+74H DWORD NumberOfRvaAndSizes;
+78H IMAGE\_DATA\_DIRECTORY
DataDirectory\[IMAGE\_NUMBEROF\_DIRECTORY\_ENTRIES\];
} IMAGE\_OPTIONAL\_HEADER32, \*PIMAGE\_OPTIONAL\_HEADER32;


```

1\. 必选部分

```
Magic  表示可选头的类型：
#define IMAGE\_NT\_OPTIONAL\_HDR32\_MAGIC 0x10b // 32 位 PE 可选头
#define IMAGE\_NT\_OPTIONAL\_HDR64\_MAGIC 0x20b // 64 位 PE 可选头
#define IMAGE\_ROM\_OPTIONAL\_HDR\_MAGIC 0x107

MajorLinkerVersion  链接器的版本号
MinorLinkerVersion  链接器的版本号

SizeOfCode  代码段的长度，如果有多个代码段，则是代码段长度的总和 
SizeOfInitializedData  初始化的数据长度 
SizeOfUninitializedData  未初始化的数据长度 

AddressOfEntryPoint  程序入口的 RVA(相对虚拟地址)，对于 exe 可以理解为 WinMain 的 RVA。对于 DLL 可以理解为 DllMain 的 RVA，如果在一个可执行文件上附加了一段代码并想让这段代码首先被执行，那么只需要将这个入口地址指向附加的代码就可以了。在脱壳时第一件事就是找入口点，指的就是这个值。

BaseOfCode  代码段起始地址的 RVA
BaseOfData  数据段起始地址的 RVA


```

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200408150532510-1821653435.png)

从上面的图中可以看出该 PE 文件的 AddressOfEntryPoint 为：0x011C010 ，由于此文件是 64 位的，我们可以拿 IDA64 进行验证：

文件载入 IDA64 后，找到 EXPORTS 菜单选项，拉到最后，即可看到 Main 入口：

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200408153529744-523933547.png)

双击步入，即可看到相应的地址参数，能够对应上：

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200408153624231-339868474.png)

2\. 可选字段部分

```
ImageBase：映象（加载到内存中的 PE 文件）的基地址，这个基地址是建议，对于 DLL 来说，如果无法加载到这个地址，系统会自动为其选择地址。 
链接器产生可执行文件的时候对应这个地址来生成机器码，所以当文件被装入这个地址时不需要进行重定位操作，装入的速度最快。当文件被装载到其他地址时，进行重定位操作，会慢一点。
对于 EXE 文件来说，由于每个文件总是使用独立的虚拟地址空间，优先装入地址不可能被其他模块占据，所以 EXE 总是能够按照这个地址装入。这也意味着 EXE 文件不再需要重定位信息。
对于 DLL 文件来说，由于多个 DLL 文件全部使用宿主 EXE 文件的地址空间，不能保证优先装入地址没有被其他的 DLL 使用，所以 DLL 文件中必须包含重定位信息以防万一。
因此，在前面介绍的 IMAGE\_FILE\_HEADER 结构的 Characteristics 字段中，DLL 文件对应的 IMAGE\_FILE\_RELOCS\_STRIPPED 位总是为 0，而 EXE 文件的这个标志位总是为 1，即 DLL 中不删除重定位信息， EXE 文件中删除重定位信息。
一般 EXE 文件的默认优先装入地址被定为 00400000h，而 DLL 文件的默认优先装入地址被定为 10000000h。

SectionAlignment  节对齐，PE 中的节被加载到内存时会按照这个域指定的值来对齐，比如这个值是 0x1000，那么每个节的起始地址的低 12 位都为 0。
FileAlignment     节在文件(磁盘)中按此值对齐，SectionAlignment 必须大于或等于 FileAlignment。

MajorOperatingSystemVersion   所需操作系统的版本号，随着操作系统版本越来越多，这个好像不是那么重要了。
MinorOperatingSystemVersion   所需操作系统的版本号，随着操作系统版本越来越多，这个好像不是那么重要了。
MajorImageVersion 映象的版本号，这个是开发者自己指定的，由连接器填写。
MinorImageVersion 映象的版本号，这个是开发者自己指定的，由连接器填写。
MajorSubsystemVersion  所需子系统版本号。
MinorSubsystemVersion  所需子系统版本号。
Win32VersionValue 保留，必须为 0。
SizeOfImage       映象的大小， PE 文件加载到内存中空间是连续的，这个值指定占用虚拟空间的大小。
SizeOfHeaders     所有文件头（包括节表）的大小，这个值是以 FileAlignment 对齐的。
CheckSum          映象文件的校验和。

Subsystem         运行该 PE 文件所需的子系统，可以是下面图5定义中的某一个：(图见代码段下)
DllCharacteristics  DLL 的文件属性，只对 DLL 文件有效

SizeOfStackReserve  运行时为每个线程栈保留内存的大小
SizeOfStackCommit   运行时每个线程栈初始占用内存大小
SizeOfHeapReserve   运行时为进程堆保留内存大小。
SizeOfHeapCommit    运行时进程堆初始占用内存大小
LoaderFlags         保留，必须为 0
NumberOfRvaAndSizes 数据目录的项数，即下面这个数组的项数

DataDirectory       数据目录，是一个数组，数组的项定义如下：

    typedef struct \_IMAGE\_DATA\_DIRECTORY {
        DWORD VirtualAddress;
        DWORD Size;
    } IMAGE\_DATA\_DIRECTORY, \*PIMAGE\_DATA\_DIRECTORY;

有两个值：VirtualAddress，Size。一个是地址，一个是大小


```

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200408133310664-272368086.png)

### 0X04 节表

节表是 PE 文件后续节的描述， Windows 根据节表的描述加载每个节。 PE 文件中所有节的属性都被定义在节表中，节表由一系列的 IMAGE\_SECTION\_HEADER 结构排列而成，每个结构用来描述一个节，结构的排列顺序和它们描述的节在文件中的排列顺序是一致的。全部有效结构的最后以一个空的 IMAGE\_SECTION\_HEADER 结构作为结束，所以节表中 IMAGE\_SECTION\_HEADER 结构数量等于节的数量加一。

节表总是被存放在紧接在 PE 文件头的地方。节表中 IMAGE\_SECTION\_HEADER 结构的总数总是由 PE 文件头 IMAGE\_NT\_HEADERS(注：即本资料中的 NT 头) 结构中的 FileHeader.NumberOfSections 字段来指定的。

```
typedef struct \_IMAGE\_SECTION\_HEADER {
 BYTE Name\[IMAGE\_SIZEOF\_SHORT\_NAME\];
 union {
     DWORD PhysicalAddress;
     DWORD VirtualSize;
 } Misc;
 DWORD VirtualAddress;
 DWORD SizeOfRawData;
 DWORD PointerToRawData;
 DWORD PointerToRelocations;
 DWORD PointerToLinenumbers;
 WORD NumberOfRelocations;
 WORD NumberOfLinenumbers;
 DWORD Characteristics;
} IMAGE\_SECTION\_HEADER, \*PIMAGE\_SECTION\_HEADER;


```

#### 4.1 节表中的域

Name 是一个区块名，由 8 个 ASCII 码组成，用来定义区块的名称的数组。多数区块名都习惯性以一个 “.” 作为开头（例如： .text），这个“.” 实际上不是必须的。如果区块名达到 8 个字节，后面就没有 0 字符了。

CopyCopyCopy

注意：前边带有一个

`“$”`

的区块名字会从连接器那里得到特殊的待遇，前边带有

`“$”`

的相同名字的区块在载入时候将会被合并，在合并之后的区块中，他们是按照

`“$”`

后边的字符的字母顺序进行合并的。每个区块的名称都是唯一的，不能有同名的两个区块。但事实上节的名称不代表任何含义，他的存在仅仅是为了正规统一编程的时候方便程序员查看方便而设置的一个标记而已。

```
VirtualSize        对表对应的区块的大小，这是区块的数据在没有进行对齐处理前的实际大小。
VirtualAddress     该区块装载到内存中的 RVA 地址。这个地址是按照内存页来对齐的，因此它的数值总是 SectionAlignment 的值的整数倍。
PointerToRawData   指出节在磁盘文件中所处的位置。这个数值是从文件头开始算起的偏移量。
SizeOfRawData      该区块在磁盘中所占的大小，这个数值等于 VirtualSize 字段的值按照 FileAlignment 的值对齐以后的大小。
Characteristics    该区块的属性。该字段是按位来指出区块的属性（如代码/数据/可读/可写等）的标志。


```

#### 4.2 装载过程

依靠 PointerToRawData， SizeOfRawData， VirtualAddress， VirtualSize 这 4 个字段的值，装载器就可以从 PE 文件中找出某个节 (从 PointerToRawData 偏移开始的 SizeOfRawData 字节) 的数据，并将它映射到内存中去(映射到从模块基地址偏移 VirtualAddress 的地方，并占用以 VirtualSize 的值按照页的尺寸对齐后的空间大小)。

### 0X05 节块

#### 5.1 简介

每个节实际上是一个容器，可以包含代码、数据等等，每个节可以有独立的内存权限，比如代码节默认有读 / 执行权限，节的名字和数量可以自己定义。

通常，区块中的数据在逻辑上是关联的。 PE 文件一般至少都会有两个区块：一个是代码块，另一个是数据块。每一个区块都需要有一个截然不同的名字，这个名字主要是用来表达区块的用途。例如有一个区块叫. rdata，表明他是一个只读区块。注意：区块在映像中是按起始地址（RVA）来排列的，而不是按字母表顺序。

另外，使用区块名字只是人们为了认识和编程的方便，而对操作系统来说这些是无关紧要的。微软给这些区块取了个有特色的名字，但这不是必须的。当编程从 PE 文件中读取需要的内容时，如输入表、输出表，不能以区块名字作为参考，正确的方法是按照数据目录表中的字段来进行定位。

#### 5.2 块的偏移地址

块起始地址在磁盘中是按照 IMAGE\_OPTIONAL\_HEADER32 中的 FileAlignment 字段的值进行对齐的，而当被加载到内存中时是按照同一结构中的 SectionAlignment 字段的值设置对齐的，两者的值可能不同。所以一个块表被装载到内存后相对于文件头的偏移地址和磁盘中的偏移地址可能是不同的。

#### 5.3 区块的对齐值

之前我们简单了解过区块是要对齐的，无论是在内存中存放还是在磁盘中存放，但他们一般的对齐值是不同的。

PE 文件头里边的 FileAligment 定义了磁盘区块的对齐值。每一个区块从对齐值的倍数的偏移位置开始存放。而区块的实际代码或数据的大小不一定刚好是这么多，所以在多余的地方一般以 00h 来填充，这就是区块间的间隙。例如，在 PE 文件中，一个典型的对齐值是 200h ，这样，每个区块都将从 200h 的倍数的文件偏移位置开始，假设第一个区块在 400h 处，长度为 90h，那么从文件 400h 到 490h  
为这一区块的内容，而由于文件的对齐值是 200h，所以为了使这一区块的长度为 FileAlignment 的整数倍， 490h 到 600h 这一个区间都会被 00h 填充，这段空间称为区块间隙，下一个区块的开始地址为 600h 。

一般在 X86 系列的 CPU 中，页是按 4KB（1000h）来排列的；在 IA-64 上，是按 8KB（2000h）来排列的。所以在 X86 系统中， PE 文件区块的内存对齐值一般等于 1000h，每个区块按 1000h 的倍数在内存中存放。

#### 5.4 RVA 和文件偏移的转换

RVA 是相对虚拟地址（Relative Virtual Address）的缩写，顾名思义，它是一个 “相对地址”。 PE 文件中的各种数据结构中涉及地址的字段大部分都是以 RVA 表示的。更为准确的说，RVA 是当 PE 文件被装载到内存中后，某个数据位置相对于文件头的偏移量。

CopyCopy

举个例子，如果 Windows 装载器将一个 PE 文件装入到 00400000h 处的内存中，而某个区块中的某个数据被装入

`0040**xh`

处，那么这个数据的 RVA 就是

`（0040**xh - 00400000h ）= **xh`

，反过来说，将 RVA 的值加上文件被装载的基地址，就可以找到数据在内存中的实际地址。