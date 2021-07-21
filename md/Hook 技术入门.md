> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FlWmYGH2NgCdhpkIfVe4Kw)

0x00 前言

要说在 Hook 技术里面最基础的，那就是 IAT Hook，它的原理就是通过修改 PE 结构中的 IAT 表，将其替换成我们自己定义的函数，最终实现 Hook，所以在进行 Hook 之前，我们得很清楚的 PE 结构，接下来我们先讲解一下怎么索引到 IAT 表。

0x01 PE 文件格式解析  

随便拖一个程序进入 Uedit 进行分析  

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFBJibKMiaxqribTA72eoibBSDxibyjHfn3RRokLKmQib7qgS2gKbEYkEahLXafQbSnSuGzPWqNzUu9BmlZw/640?wx_fmt=png)

这一部分就是 PE 文件的 DOS 头，先看看 DOS 头的结构体，咱边看结构体边分析：  

```
typedef struct IMAGE_DOS_HEADER
　　{
　　      WORD e_magic;　　      WORD e_cblp;
　　      WORD e_cp;
　　      WORD e_crlc;
　　      WORD e_cparhdr;
　　      WORD e_minalloc;
　　      WORD e_maxalloc;
　　      WORD e_ss;
　　      WORD e_sp;
　　      WORD e_csum;
　　      WORD e_ip;
　　      WORD e_cs;
　　      WORD e_lfarlc;
　　      WORD e_ovno;
　　      WORD e_res[4];
　　      WORD e_oemid;
　　      WORD e_oeminfo;
　　      WORD e_res2[10];
　　      DWORD e_lfanew;            
　　}IMAGE_DOS_HEADER, *PIMAGE_DOS_HEADER;
```

在 DOS 头里面最关键是两个成员就是 e_magic，e_lfanew（其他的可以忽略），e_magic 就是 DOS 头的标识，也就是 MZ，为什么是 MZ 呢，其实就是 Mark Zbikowski，他是 MS-DOS 主要开发者之一，为了纪念老人家，e_lfanew 就是下一个头的偏移（基于文件基址），可能有同学要有疑问了，为啥现在还要有这个 DOS 头呢，因为微软为了向下兼容，所以才没有删除 DOS 头，那么加上偏移我们来看看：

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFBJibKMiaxqribTA72eoibBSDxib9O3kqAb1atge6pqZpvAazu67gjR6NlicAxM5YicZXCOXNZ5mt0AWtzUw/640?wx_fmt=png)

PE 头也有它自己的结构体，Signature 和 e_magic 是一个道理，这里的 Signature 是 PE。

```
typedef struct IMAGE_NT_HEADERS 　　{ 　　     
     DWORD Signature; 　　      
     IMAGE_FILE_HEADER FileHeader;
     IMAGE_OPTIONAL_HEADER32 OptionalHeader; 　　
} IMAGE_NT_HEADERS,*PIMAGE_NT_HEADERS;
```

选择的区域是上面结构体中的 FileHeader

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFBJibKMiaxqribTA72eoibBSDxibWwUDHia4YgYlSEC4n0OeOXUBAwTvkSksib9fdO7JflFTVEoANM1lMhxA/640?wx_fmt=png)

它也有自己的结构体，感兴趣的小伙伴可以自己去查查每个字段的具体含义，这里就不展开了：

```
typedef struct _IMAGE_FILE_HEADER {   
        WORD      Machine;                 //运行平台 
        WORD      NumberOfSections;        //节表数目    
        DWORD     TimeDateStamp;           //时间戳     
        DWORD     PointerToSymbolTable;    
        DWORD     NumberOfSymbols;         //符号数  
        WORD      SizeOfOptionalHeader;    //可选部首长度 
        WORD      Characteristics;         //文件属性 
}
```

说完 FileHeader，重点就来了，那就是 OptionalHeade，除去 Signature，FileHeader 剩下的就是 OptionalHeade：

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFBJibKMiaxqribTA72eoibBSDxib8lD8cjIPZ2dgDExUbpp8mKYbK2Ok0VNuicfWXHqorQr6Ow6OfSYznzg/640?wx_fmt=png)

结构体如下，我们关注其最重要的一个成员 DataDirectory（数据目录），它包含了我们要替换的导入表。

```
typedef struct _IMAGE_OPTIONAL_HEADER {
  WORD                 Magic;
  BYTE                 MajorLinkerVersion;
  BYTE                 MinorLinkerVersion;
  DWORD                SizeOfCode;
  DWORD                SizeOfInitializedData;
  DWORD                SizeOfUninitializedData;
  DWORD                AddressOfEntryPoint;
  DWORD                BaseOfCode;
  DWORD                BaseOfData;
  DWORD                ImageBase;
  DWORD                SectionAlignment;
  DWORD                FileAlignment;
  WORD                 MajorOperatingSystemVersion;
  WORD                 MinorOperatingSystemVersion;
  WORD                 MajorImageVersion;
  WORD                 MinorImageVersion;
  WORD                 MajorSubsystemVersion;
  WORD                 MinorSubsystemVersion;
  DWORD                Win32VersionValue;
  DWORD                SizeOfImage;
  DWORD                SizeOfHeaders;
  DWORD                CheckSum;
  WORD                 Subsystem;
  WORD                 DllCharacteristics;
  DWORD                SizeOfStackReserve;
  DWORD                SizeOfStackCommit;
  DWORD                SizeOfHeapReserve;
  DWORD                SizeOfHeapCommit;
  DWORD                LoaderFlags;
  DWORD                NumberOfRvaAndSizes;
  IMAGE_DATA_DIRECTORY DataDirectory[IMAGE_NUMBEROF_DIRECTORY_ENTRIES];
} IMAGE_OPTIONAL_HEADER, *PIMAGE_OPTIONAL_HEADER;
```

它妥妥的有十六张表，我们只关注导入表：  
![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFBJibKMiaxqribTA72eoibBSDxibCADS44oqM2l5MjmsFzk2EN1ZIlje4C5aFkTmsdqrmfUibVq5icDYxdhQ/640?wx_fmt=png)  

```
typedef struct _IMAGE_IMPORT_DESCRIPTOR {
union {
DWORD Characteristics;
DWORD OriginalFirstThunk;    
} DUMMYUNIONNAME;
DWORD TimeDateStamp; 
DWORD ForwarderChain; 
DWORD Name;                   //指向DLL名字的RVA
DWORD FirstThunk;         
} IMAGE_IMPORT_DESCRIPTOR;
```

这里面最重要的就是 OriginalFirstThunk，Name，FirstThunk  

其中 OriginalFirstThunk，FirstThunk 分别指向 INT 和 IAT 表，心心念念的 IAT 表终于登场了，这两个成员指向的都是同一个表，为什么这样做等下说

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFBJibKMiaxqribTA72eoibBSDxibSTkAn5yaXg9QI8CDOMepIPo7YRAEktFA9UF9PTJpXBlXic14CI2KOeA/640?wx_fmt=png)

当我们的函数加载完成后，我们 IAT 指向了函数真正的地址

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFBJibKMiaxqribTA72eoibBSDxibKDv2xMTszVNnfLR4ALBBaJykw7FjanMic6PeoYyib0piaibwbEOXhl4tAg/640?wx_fmt=png)

在 IAT 在加载完真正的函数地址之后，如果没有 INT 表来标识具体的函数名称的话，操作系统就完全不知道它加载的这个函数名称是啥，只有一个函数的实现偏移和实现，并不知道它是啥，所以才会有 INT 表的存在。  

0x02 IAT Hook 代码编写  

到此 PE 结构也就讲解完了，也就可以开始写 IAT Hook  

我们的代码应该包含以下功能：

1. 定义我们自己的 Hook 后的函数

```
int WINAPI MyMessageBoxA(HWND hWnd, LPCSTR lpText, LPCSTR lpCaption, UINT uType)
{
  return OldMessageBoxA(hWnd, "Hello NSDA", lpCaption, uType);
}
```

我们自己的 MessageBox 必须和原来的 MessageBox 的参数一模一样，这样才能保证在调用自己的函数的时候不会报错  

2. 接下来就是找到 IAT 表

```
HMODULE ImageBase = GetModuleHandle(NULL);  //获得模块基地址                            
PIMAGE_DOS_HEADER pDosHead = (PIMAGE_DOS_HEADER)(DWORD)ImageBase;                  
DWORD dwTemp = (DWORD)pDosHead + (DWORD)pDosHead->e_lfanew;
PIMAGE_NT_HEADERS pNtHead = (PIMAGE_NT_HEADERS)dwTemp;                                                           
PIMAGE_OPTIONAL_HEADER pOpHead = (PIMAGE_OPTIONAL_HEADER)&pNtHead->OptionalHeader;

DWORD dwInputTable = pOpHead->DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress;  
DWORD dwTemp = (DWORD)GetModuleHandle(NULL) + dwInputTable;
PIMAGE_IMPORT_DESCRIPTOR   pImport = (PIMAGE_IMPORT_DESCRIPTOR)dwTemp;
PIMAGE_IMPORT_DESCRIPTOR   pCurrent = pImport;
```

通过 GetModuleHandle 获得模块基地址之后，我们就可以拿到程序的 DOS 头，PE 头，文件头，可选头

3. 接下来就是遍历 IAT 将其替换成我们自己函数的地址

```
while (*(DWORD*)pFirstThunk != NULL)                        
    {
      if (*(DWORD*)pFirstThunk == (DWORD)OldMessageBoxA)       
      {
        DWORD oldProtected;
        VirtualProtect(pFirstThunk, 0x1000, PAGE_EXECUTE_READWRITE, &oldProtected);  
        memcpy(pFirstThunk, (DWORD *)&dwTemp, 4);                                    
        VirtualProtect(pFirstThunk, 0x1000, oldProtected, &oldProtected);            
      }
      pFirstThunk++;
    }
```

通过遍历 IAT 表找到 MessageBox 的地址之后进行替换，有一点需要注意的，需要先修改文件的页属性才能进行替换（在 XP 系统上不用）

完整代码就不贴了，大伙们可以自己去尝试把完整的代码写出来，下面看看 Hook 完的效果：

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFBJibKMiaxqribTA72eoibBSDxib4qoHXkVtV6xJ0lam6ty59yQ4lmuNjulcico6oKbUQhYFQeAChFz7HsA/640?wx_fmt=png)