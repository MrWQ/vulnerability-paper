> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/g4QwYme86weuAFU_ZrFixA)

前言
--

**Elastic Security** 安全团队最近公布了一种反防病毒软件的行为查杀的新技术 **Process Ghosting**，即在 Windows 上通过篡改内存中的可执行文件映射达到绕过杀软的行为查杀。该技术是已知攻击方法（例如 Process Doppelgänging 和 Process Herpaderping）的演变。

简介
--

本文将要介绍以下内容：

*   Process Ghosting 原理
    
*   代码实例
    
*   利用思路
    
*   参考文章和项目
    

Process Ghosting 原理
-------------------

### 一个进程的创建

想要了解 Process Ghosting 的原理首先需要知道在 windows 中一个进程是如何被创建的。Windows 任务管理器可以显示系统中运行的进程列表。在操作系统中每一个进程都与磁盘上的一个可执行文件相关联，例如 进程 svchost.exe 与磁盘文件 c:\Windows\System32\svchost.exe 所对应。 这是因为 Windows 从可执行文件启动进程，可执行文件通常以 EXE 文件扩展名结尾。需要注意的是，进程不是可执行文件。如下图所示任务管理器中，有多个从 svchost.exe 启动的进程。

![](https://mmbiz.qpic.cn/mmbiz_jpg/cOCqjucntdGCRgelvMENaVfjia1qoXzibVcS5j5Jla8ytbBysj970vMQlEWPsLIhbJlic3gCL6MHiaicw0AibIsNriahQ/640?wx_fmt=jpeg)

Windows 启动一个新的进程就必须执行下面这一系列步骤。在现代版本的 Windows 中进程通常由 **NtCreateUserProcess** 函数创建。但是，windows 为了考虑向前兼容，其他 Windows  API（**NtCreateProcessEx** 等）也可以去创建一个进程。创建进程的步骤如下：

1. 打开要启动的可执行文件的句柄。

```
hFile = CreateFile("C:\Windows\System32\svchost.exe")
```

2. 为文件创建一个 image section。节将文件或文件的一部分映射到内存中。SEC_IMAGE 是一种特殊类型的节，对应于可移植可执行 (PE) 文件，并且只能从 PE（EXE、DLL 等）文件中创建。示例：

```
hSection = NtCreateSection(hFile, SEC_IMAGE)
```

3. 调用 NtCreateProcessEx 函数创建一个进程。示例：

```
hProcess = NtCreateProcessEx(hSection)
```

4. 分配环境变量。示例：

```
CreateEnvironmentBlock/NtWriteVirtualMemory
```

5. 创建一个线程在进程中执行。示例：

```
NtCreateThreadEx
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/cOCqjucntdGCRgelvMENaVfjia1qoXzibVe8st6TPwjpA7vmnsQbsZa3UGhxnTT4M0VzIPnZbAMx5CdEkicV8RsNA/640?wx_fmt=jpeg)

进程从可执行文件启动，但可执行文件中的某些数据在映射到进程时可能会被修改。Windows 内存管理器在创建时缓存 image sections。**这意味着 image sections 可以做修改，可以和原文件不保持一致**。

### 杀软扫描过程

Microsoft 为杀软开发厂商提供注册进程创建的回调的功能，这些回调将在系统上创建进程和线程时调用。驱动开发者可以调用 PsSetCreateProcessNotifyRoutineEx、PsSetCreateThreadNotifyRoutineEx 等 API 来接收此类事件。

尽管名称如此，**PsSetCreateProcessNotifyRoutineEx** 回调实际上并不是在创建进程时调用，而是在创建这些进程中的第一个线程时调用。这会在创建进程和通知杀软创建进程之间产生差距。它还为恶意软件作者提供了一个窗口，可以在安全产品扫描它们之前篡改 image 文件和 section。

请注意未记录的进程创建 API NtCreateProcess 如何处理一个 section，而不是文件：

```
NTSYSCALLAPINTSTATUSNTAPINtCreateProcess(    _Out_ PHANDLE ProcessHandle,    _In_ ACCESS_MASK DesiredAccess,    _In_opt_ POBJECT_ATTRIBUTES ObjectAttributes,    _In_ HANDLE ParentProcess,    _In_ BOOLEAN InheritObjectTable,    _In_opt_ HANDLE SectionHandle,    _In_opt_ HANDLE DebugPort,    _In_opt_ HANDLE ExceptionPort    );
```

启动进程时，安全产品会提供有关正在启动进程的以下信息：

```
typedef struct _PS_CREATE_NOTIFY_INFO {  SIZE_T              Size;  union {    ULONG Flags;    struct {      ULONG FileOpenNameAvailable : 1;      ULONG IsSubsystemProcess : 1;      ULONG Reserved : 30;    };  };  HANDLE              ParentProcessId;  CLIENT_ID           CreatingThreadId;  struct _FILE_OBJECT *FileObject;  PCUNICODE_STRING    ImageFileName;  PCUNICODE_STRING    CommandLine;  NTSTATUS            CreationStatus;} PS_CREATE_NOTIFY_INFO, *PPS_CREATE_NOTIFY_INFO;
```

有趣的是 FILE_OBJECT，它是与上一节中传递给 NtCreateSection 的 HANDLE 对应的内核对象。此 FILE_OBJECT 通常对应于磁盘上的文件，可以扫描该文件以查找恶意软件。

安全产品还可以使用文件系统微过滤回调，在文件创建、交互或关闭时接收通知。扫描每个读取和写入操作对系统的影响可能很大，因此出于性能原因，文件通常在打开和关闭时进行扫描。

还有其他潜在的安全产品拦截点请参阅 BlackHat2017 演讲。

### Process Ghosting

**Process Ghosting** 主要基于 **Process Doppelgänging** 和 **Process Herpaderping** ，允许运行有效负载并且使杀软无法检测。

**Process Doppelgänging** 和 **Process Herpaderping** 的详细介绍见下方：

*   代码注入技术 Process Doppelgänging 利用介绍
    
*   Process Herpaderping ：通过替换进程的映像文件来躲避杀软检测的技术
    

我们可以在 Doppelgänging 和 Herpaderping 的基础上运行已被删除的可执行文件。在 Windows 上有多种删除文件的方法：

*   在设置了 FILE_SUPERSEDE 或 CREATE_ALWAYS 标志的旧文件上创建一个新文件。
    
*   创建或打开文件时设置 FILE_DELETE_ON_CLOSE 或 FILE_FLAG_DELETE_ON_CLOSE 标志。
    
*   通过 NtSetInformationFile 调用 FileDispositionInformation 文件信息类时，将 FILE_DISPOSITION_INFORMATION 结构中的 DeleteFile 字段设置为 TRUE 。
    

Windows 尝试阻止修改映射的可执行文件。一旦文件被映射到图像部分，尝试使用 **FILE_WRITE_DATA** 打开它（以修改它）将失败并显示 **ERROR_SHARING_VIOLATION**。通过 **FILE_DELETE_ON_CLOSE/FILE_FLAG_DELETE_ON_CLOSE** 尝试删除失败并显示 **ERROR_SHARING_VIOLATION**。**NtSetInformationFile(FileDispositionInformation)** 需要 DELETE 访问权限。即使将 DELETE 访问权限授予映射到图像部分的文件，**NtSetInformationFile(FileDispositionInformation)** 也会因 **STATUS_CANNOT_DELETE** 而失败。通过 **FILE_SUPERCEDE/CREATE_ALWAYS** 尝试删除失败并显示 **ACCESS_DENIED**。

然而，一个重要的注意事项是，此删除限制仅在可执行文件映射到映像部分后才生效。这意味着可以创建一个文件，将其标记为删除，将其映射到 image 部分，关闭文件句柄以完成删除，然后从现在无文件部分创建一个进程。这就是 **Process Ghosting**。详细攻击流程如下所示：

![](https://mmbiz.qpic.cn/mmbiz_jpg/cOCqjucntdGCRgelvMENaVfjia1qoXzibV8ib38U3NVmEbo4xrqeTmKzxKBUGQkknqDfTribR2rb8DOicDY3QLHcx3g/640?wx_fmt=jpeg)

1.  创建文件
    
2.  使用 NtSetInformationFile(FileDispositionInformation) 将文件置于删除挂起状态。注意：尝试使用 FILE_DELETE_ON_CLOSE 不会删除文件。
    
3.  将有效负载可执行文件写入文件。内容未保留，因为文件已处于删除待处理状态。删除挂起状态还会阻止外部文件打开尝试。
    
4.  为文件创建一个 image section。
    
5.  关闭删除挂起句柄，删除文件。
    
6.  使用 image section 创建一个进程。
    
7.  分配流程参数和环境变量。
    
8.  创建一个线程在进程中执行。
    

代码实例
----

![](https://mmbiz.qpic.cn/mmbiz_jpg/cOCqjucntdGCRgelvMENaVfjia1qoXzibVJFj04HzsYy2BTg2HYH0YPgo6FtnQgATKJ8D2KCsVeKtWdbUcIgoGoQ/640?wx_fmt=jpeg)

https://github.com/hasherezade/process_ghosting

编译工具：VS2019

64 位程序适用 64 位系统

32 位程序适用 32 位系统

![](https://mmbiz.qpic.cn/mmbiz_jpg/cOCqjucntdGCRgelvMENaVfjia1qoXzibVVKLOB0zwXxHtXKaZic7QjIvPocBT37aIMWqZWR5uZCY4tmcsfAueSkg/640?wx_fmt=jpeg)

利用思路
----

在实际利用中，为了绕过静态查杀，需要对 POC 做进一步修改，利用思路如下：

首先对执行文件做加密，然后 PoC 在 buffer_payload 函数位置文件读入内存做解密，然后返回解密后的内存文件地址，最后执行。

补丁
--

Elastic 安全研究人员向 **Microsoft 安全响应中心** (MSRC) 报告了该问题，并提供了 PoC 的源代码。不过，微软认为问题并不严重，补丁的发布也不是必须的。

参考文章和项目
-------

https://www.elastic.co/cn/blog/process-ghosting-a-new-executable-image-tampering-attack

https://github.com/hasherezade/process_ghosting

https://www.andreafortuna.org/2021/06/18/how-process-ghosting-works/

https://www.youtube.com/watch?v=dZJEyveZwFE

号外  

[宽字节安全 JAVA 安全线上进阶课程：开讲啦！！！](https://mp.weixin.qq.com/s?__biz=MzUzNTEyMTE0Mw==&mid=2247484931&idx=1&sn=a71640ef96ffdc5e26b1c5df38dca0ba&scene=21#wechat_redirect)

宽字节安全首次推出 `JAVA安全进阶`课程，系统性讲解 JAVA 反序列化漏洞，代码执行漏洞等开发中可能出现的安全问题。

培训采用 线上授课 + 视频录播 的授课方式，交流群随问随答。首期班加入即送 宽字节安全知识星球  名额，涉及 **java 安全，红蓝对抗，漏洞研究****等安全领域。**

每周只安排两天课，共 6 周 36 课时，由浅入深，感受 java 安全魅力。

*   周三 **19:30 - 21:30**
    
*   周日 **14:00 -18:00**
    

  

现在报名即可享受立减 1000 元！！！名额有限欢迎咨询。

[点击查看详情](https://mp.weixin.qq.com/s?__biz=MzUzNTEyMTE0Mw==&mid=2247484931&idx=1&sn=a71640ef96ffdc5e26b1c5df38dca0ba&scene=21#wechat_redirect)  

扫码添加客服微信，期待您的加入

![](https://mmbiz.qpic.cn/mmbiz_jpg/cOCqjucntdEhsMUjTPslVricKT94iaKpb5sL2PolmEf1WwcEEuwFaIGL9U3ePh1KXDDK8yggpMPHwDUibcn5b17wg/640?wx_fmt=jpeg)