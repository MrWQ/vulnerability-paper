> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/8332)

```
译文声明
本文是翻译文章，文章原作者 S3cur3Th1sSh1t
原文地址：https://s3cur3th1ssh1t.github.io/Building-a-custom-Mimikatz-binary/

译文仅供参考，具体内容表达以及含义原文为准
```

这篇文章将介绍如何通过修改源码来构建一个定制的 Mimikatz，以达到 Bypass AV/EDR 的目的。

### 0x00 介绍

如同上一篇文章文末说承诺的一样，本文主要讲述如何构建一个定制的 Mimikatz 二进制文件。在几个月前，我第一次进行尝试，将二进制文件集成到 [WinPwn](https://github.com/S3cur3Th1sSh1t/WinPwn) 中，使用反射的方式加载。那时候有人问我，这个混淆的 Mimikatz 是怎么来的，因此我现在分享这个混淆定制的过程。

只要有心，在搜索引擎中确实能够发现很多关于如何混淆 Mimikatz 的文章。但大多数文章都集中在绕过 AMSI 的 `Invoke-Mimikatz` 及使用其他混淆工具，但几乎没有发现重新定制一个 Mimikatz。但是，在几个月前的一个[发现](https://gist.github.com/imaibou/92feba3455bf173f123fbe50bbe80781) 对我有了很大的启发，为此构建了一个 Mimikatz 的定制版。

```
# This script downloads and slightly "obfuscates" the mimikatz project.
# Most AV solutions block mimikatz based on certain keywords in the binary like "mimikatz", "gentilkiwi", "benjamin@gentilkiwi.com" ..., 
# so removing them from the project before compiling gets us past most of the AV solutions.
# We can even go further and change some functionality keywords like "sekurlsa", "logonpasswords", "lsadump", "minidump", "pth" ....,
# but this needs adapting to the doc, so it has not been done, try it if your victim's AV still detects mimikatz after this program.

git clone https://github.com/gentilkiwi/mimikatz.git windows
mv windows/mimikatz windows/windows
find windows/ -type f -print0 | xargs -0 sed -i 's/mimikatz/windows/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/MIMIKATZ/WINDOWS/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/Mimikatz/Windows/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/DELPY/James/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/Benjamin/Troy/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/benjamin@gentilkiwi.com/jtroy@hotmail.com/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/creativecommons/python/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/gentilkiwi/MSOffice/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/KIWI/ONEDRIVE/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/Kiwi/Onedrive/g'
find windows/ -type f -print0 | xargs -0 sed -i 's/kiwi/onedrive/g'
find windows/ -type f -name '*mimikatz*' | while read FILE ; do
    newfile="$(echo ${FILE} |sed -e 's/mimikatz/windows/g')";
    mv "${FILE}" "${newfile}";
done
find windows/ -type f -name '*kiwi*' | while read FILE ; do
    newfile="$(echo ${FILE} |sed -e 's/kiwi/onedrive/g')";
    mv "${FILE}" "${newfile}";
done


```

`We can even go further` - 挑战由此诞生。

### 0x01 Mimikatz 含有病毒

如果你曾经尝试过在开启 AV 的情况下去下载 Mimikatz 的二进制，你会发现，这压根是不可能，因为它的每一个版本都会被标记。这完全可以理解，因为如今的大环境中，很多攻击者都会在渗透测试过程中使用 Mimikatz 及其他开源项目。但是可以肯定的是， Mimikatz 是最常用的工具，因为它可以从 lsass 进程或 SAM 数据库中提取凭证信息，从而进行哈希传递、DPAPI 解码等等操作。在 [ADSecurity.org](https://adsecurity.org/?page_id=1821) 和 [Mimikatz Wiki](https://github.com/gentilkiwi/mimikatz/wiki) 上可以找到关于 Mimikatz 完整的功能概述。

很多人显然不知道这些开源项目为什么会被标记，以及如何被标记。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172743-08bbd3c2-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172743-08bbd3c2-fd7f-1.jpeg)

当然，有些能力的攻击者，一般都不会使用 Github 上的发布版本，而是下载源代码，重新编译。并且通常情况下，他们只使用 / 编译了 Mimikatz 的部分功能代码。在这种情况下，我们不会阉割 Mimikatz 的任何功能，而是通过修改源代码，从而降低检测率，甚至完全 绕过。因此编译一个定制的 Mimikatz 是完全有必要的。

### 0x02 基本特征

我们已经从上面总结出了一些常见的 Mimikatz 特征。首先，我们必须替换以下字符串：

*   mimikatz, MIMIKATZ and Mimikatz
*   DELPY, Benjamin, benjamin@gentilkiwi.com
*   creativecommons
*   gentilkiwi
*   KIWI, Kiwi and kiwi

把自己放在 AV-Vendor 的位置上。首先要标记的是二进制文件中包含的明显字符串。如果你打开 Mimikatz 的菜单，你会看到以下内容：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172755-1001711e-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172755-1001711e-fd7f-1.jpeg)

图片中所出现的所有字符，都可以作为 Mimikatz 运行的特征，因此我们首先第一步要做的就是将其替换：

*   “A La Vie, A L’Amour”
*   [http://blog.gentilkiwi.com/mimikatz](http://blog.gentilkiwi.com/mimikatz)
*   Vincent LE TOUX
*   vincent.letoux@gmail.com
*   [http://pingcastle.com](http://pingcastle.com/)
*   [http://mysmartlogon.com](http://mysmartlogon.com/)

我们也可以直接对 [mimikatz.c](https://github.com/gentilkiwi/mimikatz/blob/master/mimikatz/mimikatz.c) 进行修改，主要是把 `banner` 进行删除或者换成其他字符信息。

正如前文提到的，我们可以进一步替换命名功能名称关键字。在写这篇文章的时候，Mimikatz 的主要模块有以下几个：

*   crypto, dpapi, kerberos, lsadump, ngc, sekurlsa
*   standard, privilege, process, service, ts, event
*   misc, token, vault, minesweeper, net, busylight
*   sysenv, sid, iis, rpc, sr98, rdm, acr

也许我需要一些 Mimikatz 基础教程，因为 Wiki 并没有说明如何列出所有模块。但仍然可以通过输入一个无效的模块名称来做到这一点，比如 `::` ：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172811-18fb4510-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172811-18fb4510-fd7f-1.jpeg)

这里我们有两个选择：

*   要么在原来的基础上，对功能名称进行随机大小写化，比如 `crypto -> CryPto`；
*   要么就全部更改，比如 `crypto -> cccccc`。

对于第一种，熟悉的命令不变，在使用时，可以有效的分辨出名称对应的功能。对于第二种，我们必须要记住新的函数名。

目前，我们将会使用熟悉的函数名，我这里并没有使用简短的函数名进行替换，因为这些字符串也可能存在于代码的其他字符串中，这可能会损坏当前的代码结构。为了给每一个新的版本建立一个自定义的二进制，我们用随机的名字替换与函数名无关的字符串。

还有一个重要的东西要更换，就是二进制的图标。因此在修改后的 gist 版本中，我们用一些随机下载的图标来替换现有的图标。

主菜单中的每个函数都有子函数。比如最常用的 `sekurlsa` 函数就有以下子函数：

*   msv, wdigest, kerberos, tspkg
*   livessp, cloudap, ssp, logonpasswords
*   process, minidump, bootkey, pth
*   krbtgt, dpapisystem, trust, backupkeys
*   tickets, ekeys, dpapi, credman

为确保已经对 Mimikatz 做出了修改，我们使用该 [bash 脚本](https://gist.github.com/S3cur3Th1sSh1t/08623de0c5cc67d36d4a235cec0f5333) 替换了子功能名称。然后编译代码，并将其上传到 `VirusTotal` 进行检测，检测结果如下：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172822-1fab7ed4-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172822-1fab7ed4-fd7f-1.jpeg)

25/67 次检测。 不错，但还不够好。

### 0x03 netapi32.dll

为了能够找到更多的特征，可以使用 `head -c byteLength mimikatz.exe > split.exe` 将文件分割成若干部分。如果生成的文件被删除，则说明被删除的文件至少包含一个特征。如果没有被删除，则说明文件未包含特征。也可以使用 Matt Hands 的 [DefenderCheck](https://github.com/matterpreter/DefenderCheck) 项目完成这个工作（该工具的缺陷及修改建议在第二篇文章中已经阐明）。让我们检查一下生成的二进制文件:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172836-282fa684-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172836-282fa684-fd7f-1.jpeg)

从图中可以看出，Defender 标记了`netapi32.dll` 库的三个函数：

*   I_NetServerAuthenticate2
*   I_NetServerReqChallenge
*   I_NetServerTrustPasswordsGet

通过在网上搜索，我找到了下面[这篇文章](https://sudonull.com/post/27330-Getting-around-Windows-Defender-cheaply-and-cheerfully-obfuscating-Mimikatz-THunter-Blog)，它解释了如何用不同的结构建立一个新的 `netapi32.min.lib`。正如文章中所说，我们可以通过创建一个内容如下的 `.def` 文件来建立一个自定义的 `netapi32.min.lib`。

```
LIBRARY netapi32.dll
EXPORTS
  I_NetServerAuthenticate2 @ 59
  I_NetServerReqChallenge @ 65
  I_NetServerTrustPasswordsGet @ 62


```

之后，我们在 Visual Studio 开发者控制台中通过以下命令来构建 `netapi32.min.lib` 文件。

```
lib /DEF:netapi32.def /OUT:netapi32.min.lib


```

我们将这个新文件嵌入到 `lib\x64\` 目录中，然后重新编译。再次运行 DefenderCheck，将无法检测到任何内容：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172847-2e814d30-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172847-2e814d30-fd7f-1.jpeg)

这意味着我们已经绕过了 Windows Defender 的 "实时保护" 功能。但如果我们启用云保护并将文件复制到另一个位置，它又无了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172856-33d619d2-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172856-33d619d2-fd7f-1.jpeg)

### 0x04 替换更多的字符串

这里还有很多需要更换的字符。一开始，我们只是更换了明显的字符串。但在 Mimikatz 菜单中包含了每个功能函数的描述，例如 `privilege` 函数有如下描述：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172904-390860b8-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172904-390860b8-fd7f-1.jpeg)

所有的描述都需要进行删除或替换。我们可以将它们添加到上面提到的 bash 脚本中，以便一次性全部替换。可以全部替换，也可以保留一些无关紧要的特色，比如 `answer` 和 `ocffee`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172912-3d7f4382-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172912-3d7f4382-fd7f-1.jpeg)

许多 AV 产品都会标记二进制文件中与功能相关的加载 DLL 文件的区域。Mimikatz 从 `.DLL` 文件中加载了很多功能。为了找到 Mimikatz 源代码中所有相关的 DLL 文件，我们打开 Visual Studio，然后使用 `STRG + SHIFT + F` 组合键，这将打开整个项目的搜索。搜索 `.dll` 会给我们提供项目中使用的所有 DLL 文件名。我们还将在我们的 bash 脚本中使用不同的大小写来替换 DLL 名称。

`sekurlsa` 的子函数 `logonpasswords` 是最常用的函数，它几乎可以转存机器上所有的证书，因此，该函数也是 AV 的重点照顾对象。可以来看看 [kuhl_m_sekurlsa.c](https://github.com/gentilkiwi/mimikatz/blob/master/mimikatz/modules/sekurlsa/kuhl_m_sekurlsa.c) ，看看 `kprintf()` 中都有哪些可能被标记的字符串。我们一直在寻找误报率低的字符串，因为 AV 也不想意外地将其他二进制进行标记。我们最终会得到这样的字符串：

*   Switch to MINIDUMP, Switch to PROCESS
*   UndefinedLogonType, NetworkCleartext, NewCredentials, RemoteInteractive, CachedInteractive, CachedRemoteInteractive, CachedUnlock
*   DPAPI_SYSTEM, replacing NTLM/RC4 key in a session, Token Impersonation , UsernameForPacked, LSA Isolated Data

如果我们看一下默认的函数 [standard kuhl_m_standard.c](https://github.com/gentilkiwi/mimikatz/blob/master/mimikatz/modules/kuhl_m_standard.c)，应该还有其他可能被标记的字符串。

*   isBase64InterceptInput, isBase64InterceptOutput
*   Credential Guard may be running, SecureKernel is running

这种方法也适用于其他的源代码文件，但篇幅的原因，就不多介绍了。总之，你替换的字符串越多，检测率就越低。

### 0x05 文件夹及文件结构

我还看了一下整个 Mimikatz 项目的结构，看看有哪些字符串是反反复复出现的。这个过程，有一点引起了我的注意：所有的变量名和函数名的头部都是以 `kuhl_` 和 `KULL_` 起头。如下图所示：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172924-44bab76c-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172924-44bab76c-fd7f-1.jpeg)

我们也可以通过以下方式进行替换：

很容易就能完全替换掉所有这些出现的地方。这可能也会大大改变生成文件的签名。所以我们也在脚本中加入以下几行。

```
kuhl=$(cat /dev/urandom | tr -dc "a-z" | fold -w 4 | head -n 1)
find windows/ -type f -print0 | xargs -0 sed -i "s/kuhl/$kuhl/g"

kull=$(cat /dev/urandom | tr -dc "a-z" | fold -w 4 | head -n 1)
find windows/ -type f -print0 | xargs -0 sed -i "s/kull/$kull/g"

find windows/ -type f -name "*kuhl*" | while read FILE ; do
    newfile="$(echo ${FILE} |sed -e "s/kuhl/$kuhl/g")";
    mv "${FILE}" "${newfile}";
done


find windows/ -type f -name "*kull*" | while read FILE ; do
    newfile="$(echo ${FILE} |sed -e "s/kull/$kull/g")";
    mv "${FILE}" "${newfile}";
done

under=$(cat /dev/urandom | tr -dc "a-z" | fold -w 4 | head -n 1)
find windows/ -type f -print0 | xargs -0 sed -i "s/_m_/$under/g"

find windows/ -type f -name "*_m_*" | while read FILE ; do
    newfile="$(echo ${FILE} |sed -e "s/_m_/$under/g")";
    mv "${FILE}" "${newfile}";
done


```

将上面提到的所有字符串添加到我们的 bash 脚本中，此时的脚本是长[这样](https://gist.github.com/S3cur3Th1sSh1t/cb040a750f5984c41c8f979040ed112a)的。

执行 bash 脚本，编译并上传到 Virustotal，结果如下:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172934-4ab52b8e-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172934-4ab52b8e-fd7f-1.jpeg)

在原有的基础上替换更多的字符串，看起来并没有能够很好的绕过 AV。但是在编写本文时，这个二进制文件足以绕过 Defender 的云保护。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172944-50902392-fd7f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172944-50902392-fd7f-1.png)

### 0x06 还有更多要做的事情

如果还想更进一步，试图获得 FUD，其实可以做得更多。比如可以替换 fuction 名称，而不是使用大小写混淆；也可以通过所有的其他的 C 源码文件和库文件来搜索可能被标记的特征等，并将其进行替换或者删除不需要的函数。

再比如，Mimikatz 输出的错误信息也有可能是特征之一，如果我们并不需要它详细的错误信息，那么可以直接删除它们。可以使用 `STRG + SHIFT + H` 组合键，搜索并替换整个项目中的字符串。例如以下操作：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20200923172958-59432a70-fd7f-1.jpeg)](https://xzfile.aliyuncs.com/media/upload/picture/20200923172958-59432a70-fd7f-1.jpeg)

大部分 AV/EDR 厂商也使用了关于 API 导入的检测方法。关于混淆 C/C++ 源码以隐藏 API 导入，Plowsec 有两篇非常好的文章。它们分别是 [Engineering antivirus evasion](https://blog.scrt.ch/2020/06/19/engineering-antivirus-evasion/) 和 [Engineering antivirus evasion (Part II)](https://blog.scrt.ch/2020/07/15/engineering-antivirus-evasion-part-ii/)。

在 Mimikatz 中，使用了很多 Windows API，为了能够更好的隐藏 API，可以借鉴以下的例子。例如要隐藏 LSAOpenSecret，在 Mimikatz 中可以使用以下代码：

```
typedef NTSTATUS(__stdcall* _LsaOSecret)(
    __in LSA_HANDLE PolicyHandle,
    __in PLSA_UNICODE_STRING SecretName,
    __in ACCESS_MASK DesiredAccess,
    __out PLSA_HANDLE SecretHandle
    );
char hid_LsaLIB_02zmeaakLCHt[] = { 'a','d','v','a','p','i','3','2','.','D','L','L',0 };
char hid_LsaOSecr_BZxlW5ZBUAAe[] = { 'L','s','a','O','p','e','n','S','e','c','e','t',0 };
HANDLE hhid_LsaLIB_asdasdasd = LoadLibrary(hid_LsaLIB_02zmeaakLCHt);
_LsaOSecret ffLsaOSecret = (_LsaOSecret)GetProcAddress(hhid_LsaLIB_asdasdasd, hid_LsaOSecr_BZxlW5ZBUAAe);


```

通过隐藏 `SamEnumerateUserDomain`、`SamOpenUser`、`LsaSetSecret`、`I_NetServerTrustPasswordsGet` 等 API，结合上面的技术，应该可以通过修改源代码来进行 FUD。

但源码修改只是达到目标的一种方式。通过对 Phras 的文章 [Designing and Implementing PEzor, an Open-Source PE Packer](https://iwantmore.pizza/posts/PEzor.html) 的学习，发现还有很多的方法可以实现，比如 Syscall 内联 Shellcode 注入，移除用户级别的 Hook ，生成具有多态性的可执行文件等等。

### 0x07 结论

我们通过字符串替换方法以及其他技术来构建一个自定义的 Mimikatz 二进制。我们发现，在替换了最常用的字符串后进行检测，检测率降低到 1/3 左右，但可以通过添加其他更多的字符串来降低检测率。其他技术，比如 API Import 隐藏之类的也会进一步降低检测率。

顺便说一下，使用本文中的 bash 脚本处理过的 Mimikatz 二进制文件，是不会触发 AMSI 的，因此如果仅为了绕过 AMSI，则可以直接使用该脚本生成 Base64 编码的 Mimikatz，以便集成到别的工具，例如：`Invoke-ReflectivePEINjection` 及 subTee 的 [C＃PE-Loader](https://github.com/S3cur3Th1sSh1t/Creds/blob/master/Csharp/PEloader.cs)。

我希望本文能够为需要定制 Mimikatz 的人有一些启发。