> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/q7If5oX9I9-n_kg3IJ2uww)

之前很火的一个项目，https://github.com/Apr4h/CobaltStrikeScan，查找内存中的 cobaltstrike 信标，学习原理、绕过并记录。

首先要明白内存的分类

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdEC1G73WvOe99XfrboasGO6Q1LcI6zF1rEguibHCnzkqPQ83VVZibjfJrrjpPQ2GR0B0iawHhnuBgBjA/640?wx_fmt=png)

从类型上分以下三种

*   Private memory
    

*   无法与其他进程共享的内存。通过 NTDLL.DLL!NtAllocateVirtualMemory 分配的内存
    

*   Mapped memory
    

*   映射视图。这不包括从使用 SEC_IMAGE 标志创建的部分映射的 PE 文件
    

*   Image memory
    

*   磁盘上 PE 文件中使用 SEC_IMAGE 标志创建的部分的映射视图。也就是 EXE、dll 等映射过来的内存 分类对应 MEMORY_BASIC_INFORMATION  结构体的中的 type 字段 (https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-memory_basic_information)
    

  

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdEC1G73WvOe99XfrboasGO6muicdJ1Tb5iaRkokhPJGWHlBcE201obVCSbAfTJHlAyyRE0u30O391tg/640?wx_fmt=png)

用 cs 注入 calc.exe 后，用 Get-InjectedThread 检测，可以看见成功列出了被注入的程序。

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdEC1G73WvOe99XfrboasGO67aHC8neQ6CLRvcjicWOKIaxIVE7iaptRH1dPtibshoks4GLzaPKPCF23A/640?wx_fmt=png)

**检测原理**

判断线程的起始地址现关联的内存属性，是否为 IMAGE 类型。如果不是则很可能是动态分配的内存中运行的。即可判断为可疑。之后在对该内存进行 cs profile 特征的硬编码匹配。完成检测。

查看内存属性 -> VirtualQueryEx 遍历线程 -> CreateToolhelp32Snapshot 获取线程起始地址 -> NtQueryInformationThread 用 C 写一个简单的可以内存查找

```
#include <windows.h>#include <stdio.h>#include <tlhelp32.h>#define ThreadQuerySetWin32StartAddress 9typedef NTSTATUS(WINAPI* NTQUERYINFORMATIONTHREAD)(HANDLE ThreadHandle,ULONG ThreadInformationClass,PVOID ThreadInformation,ULONG ThreadInformationLength,PULONG ReturnLength);NTQUERYINFORMATIONTHREAD NtQueryInformationThread =(NTQUERYINFORMATIONTHREAD)GetProcAddress(LoadLibraryW(TEXT("ntdll.dll")), "NtQueryInformationThread”);BOOL GetThreadMemoryInfo(HANDLE process,HANDLE thread){PVOID startAddress = 0;NtQueryInformationThread(thread, ThreadQuerySetWin32StartAddress, &startAddress, sizeof(startAddress), NULL);MEMORY_BASIC_INFORMATION pb= { 0 };if (VirtualQueryEx(process, startAddress, &pb, sizeof(pb))){if (pb.State == MEM_COMMIT && pb.Type != MEM_IMAGE){printf("ProcessId : %d ",GetProcessId(process));return TRUE;}}}VOID main(){HANDLE h_thread = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,0);HANDLE hprocess = NULL;HANDLE hthread = NULL;THREADENTRY32 th{};th.dwSize = sizeof(THREADENTRY32);BOOL flag = Thread32First(h_thread, &th);while (flag){hthread = OpenThread(THREAD_ALL_ACCESS, FALSE, th.th32ThreadID );if (hthread != NULL){hprocess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, th.th32OwnerProcessID);if (hprocess != NULL){GetThreadMemoryInfo(hprocess, hthread);}CloseHandle(hprocess);}CloseHandle(hthread);flag = Thread32Next(h_thread, &th);}}
```

**绕过**

*   setThreadContent 启动远程线程时指定任意 dl l 为起始地址，先挂起，更改指向 shellcode，再执行。
    

其他内存特征消除的方法之后在其他笔记补充

**cs 设置**

CS 自己就集成了 setThreadContent 的方法，只是没人拿出来说，只需要在 profile 设置就好，成功规避 CobaltStrikeScan 的查杀

The CreateThread and CreateRemoteThread options have variants that spawn a suspended thread with the address of another function, update the suspended thread to execute the injected code, and resume that thread. Use [function] “module!function+0x##” to specify the start address to spoof. For remote processes, ntdll and kernel32 are the only recommended modules to pull from. The optional 0x## part is an offset added to the start address. These variants work x86 -> x86 and x64 -> x64 only. The execute options you choose must cover a variety of corner cases. These corner cases include self injection, injection into suspended temporary processes, cross-session remote process injection, x86 -> x64 injection, x64 -> x86 injection, and injection with or without passing an argument. The c2lint tool will warn you about contexts that your execute block does not cover.

```
process-inject {    # set how memory is allocated in a remote process    set allocator "NtMapViewOfSection";        # shape the memory characteristics and content    set min_alloc "16384";    set startrwx  "true";    set userwx    "false";    transform-x86 {        prepend "\x90\x90";    }    transform-x64 {        # transform x64 injected content    }    # determine how to execute the injected code    execute {        CreateThread "ntdll.dll!RtlUserThreadStart";        CreateRemoteThread "ntdll.dll!RtlUserThreadStart";    }}
```

可以看到设置完 profile 已经检测不到了。完成绕过。

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdEC1G73WvOe99XfrboasGO6olEiaV7IUz8Ziceq9fUU4Fibw7gldEXSBBjhuAv54lrDQTXSIReAJTLGw/640?wx_fmt=png)

号外  

-----

宽字节安全团队第一期线下网络安全就业班 7 月 1 日开班了，由宽字节安全团队独立运营，一线红队大佬带队，有丰富的漏洞研究、渗透测试、应急响应的经验与沉淀，干货多多，欢迎添加客服咨询。**最后几天，过了这个村就没这个店了！！！想上车的小伙伴抓紧时间上车！！！**  

[点击查看详情](https://mp.weixin.qq.com/s?__biz=MzUzNTEyMTE0Mw==&mid=2247484744&idx=1&sn=705508138f99f87f5111289e5e68a344&scene=21#wechat_redirect)

客服微信：unicodesec

![](https://mmbiz.qpic.cn/mmbiz_jpg/cOCqjucntdEhsMUjTPslVricKT94iaKpb5sL2PolmEf1WwcEEuwFaIGL9U3ePh1KXDDK8yggpMPHwDUibcn5b17wg/640?wx_fmt=jpeg)