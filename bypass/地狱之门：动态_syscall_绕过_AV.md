> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/KAzeqsHWIhRKV5uLSsKC4Q)

**前言：**

 **地狱之门是一个动态调用 syscall 的工具，在绕过杀软、EDR 等防护软件上有不错的效果，其原理可以查看：**

**https://github.com/am0nsec/HellsGate/blob/master/hells-gate.pdf**

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UhDCXVCoMF3A5K56NHSgzYpooJKpNrHEzBricIq9sr96gHHaOaraGNUZ1ZTEJGatB5xqmCWp4elCg/640?wx_fmt=png)

在 windows 中所有的用户模式进程 (Ring 3) 默认情况下都是隐式链接 NTDLL.dll，然后 NTDLL.dll 包含一个数组的功能，用户模式的 API 调用将通过系统调用过渡到内核内存地址空间（Ring 0）的位置。换句话说，NTDLL.dll 模块中的功能是对系统调用的包装。而地狱之门则是利用该特性进行了操作。

其中的 PE 解析可以参考 http://undocumented.ntinternals.net/

比如：

```
typedef struct _LDR_MODULE {



  LIST_ENTRY              InLoadOrderModuleList;
  LIST_ENTRY              InMemoryOrderModuleList;
  LIST_ENTRY              InInitializationOrderModuleList;
  PVOID                   BaseAddress;
  PVOID                   EntryPoint;
  ULONG                   SizeOfImage;
  UNICODE_STRING          FullDllName;
  UNICODE_STRING          BaseDllName;
  ULONG                   Flags;
  SHORT                   LoadCount;
  SHORT                   TlsIndex;
  LIST_ENTRY              HashTableEntry;
  ULONG                   TimeDateStamp;

} LDR_MODULE, *PLDR_MODULE;
```

```
typedef struct _PEB {
 BOOLEAN InheritedAddressSpace;
 BOOLEAN ReadImageFileExecOptions;
 BOOLEAN BeingDebugged;
 BOOLEAN Spare;
 HANDLE Mutant;
 PVOID ImageBase;
 PPEB_LDR_DATA LoaderData;
 PVOID ProcessParameters;
 PVOID SubSystemData;
 PVOID ProcessHeap;
 PVOID FastPebLock;
 PVOID FastPebLockRoutine;
 PVOID FastPebUnlockRoutine;
 ULONG EnvironmentUpdateCount;
 PVOID* KernelCallbackTable;
 PVOID EventLogSection;
 PVOID EventLog;
 PVOID FreeList;
 ULONG TlsExpansionCounter;
 PVOID TlsBitmap;
 ULONG TlsBitmapBits[0x2];
 PVOID ReadOnlySharedMemoryBase;
 PVOID ReadOnlySharedMemoryHeap;
 PVOID* ReadOnlyStaticServerData;
 PVOID AnsiCodePageData;
 PVOID OemCodePageData;
 PVOID UnicodeCaseTableData;
 ULONG NumberOfProcessors;
 ULONG NtGlobalFlag;
 BYTE Spare2[0x4];
 LARGE_INTEGER CriticalSectionTimeout;
 ULONG HeapSegmentReserve;
 ULONG HeapSegmentCommit;
 ULONG HeapDeCommitTotalFreeThreshold;
 ULONG HeapDeCommitFreeBlockThreshold;
 ULONG NumberOfHeaps;
 ULONG MaximumNumberOfHeaps;
 PVOID** ProcessHeaps;
 PVOID GdiSharedHandleTable;
 PVOID ProcessStarterHelper;
 PVOID GdiDCAttributeList;
 PVOID LoaderLock;
 ULONG OSMajorVersion;
 ULONG OSMinorVersion;
 ULONG OSBuildNumber;
 ULONG OSPlatformId;
 ULONG ImageSubSystem;
 ULONG ImageSubSystemMajorVersion;
 ULONG ImageSubSystemMinorVersion;
 ULONG GdiHandleBuffer[0x22];
 ULONG PostProcessInitRoutine;
 ULONG TlsExpansionBitmap;
 BYTE TlsExpansionBitmapBits[0x80];
 ULONG SessionId;
} PEB, *PPEB;
```

我以此为基础编写了一个 POC，地址如下：

  
https://github.com/lengjibo/RedTeamTools/tree/master/windows/HellGatePoc

效果如下

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UhDCXVCoMF3A5K56NHSgzYsISEpXlibwCOzkXhnEuzGHCWvNZIlpP9iaibN4Y3ic1syIhxC4iauQNVg7A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UhDCXVCoMF3A5K56NHSgzYDQB0T6Ow8GDeLcsoG81XVqALFMcegarNvJ6DKIlHfPWqw3ribHfWcFg/640?wx_fmt=png)

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)