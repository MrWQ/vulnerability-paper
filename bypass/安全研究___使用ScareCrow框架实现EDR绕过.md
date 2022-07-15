> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FIjs_Mx7jpcNuX-7TkGqag)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38n37uvCbNicfbMpJLZxIGGD1OOzuq3J7ztCLxA5IMbN5zF9xraVuKpmdg0xwVewNzQzvGCMoZ4rLg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

ScareCrow
---------

ScareCrow是一款功能强大的Payload创建框架，可以帮助广大研究人员生成用于向合法Windows金册灰姑娘中注入内容的加载器，以绕过应用程序白名单控制。当DLL加载器加载进内存中之后，将会使用一种技术来将EDR钩子从正在进程内存中运行的系统DLL中清理掉，这是因为我们知道EDR的钩子是在这些进程被生成时设置的。ScareCrow可以通过使用API函数VirtualProtect来在内存中对这些DLL进行操作，该函数可以将进程的内存权限的一部分更改为不同的值，特别是将Execute-Read修改为Read-Write-Execute。

在执行过程中，ScareCrow将会复制存储在C:\Windows\System32\磁盘上的系统DLL的字节数据。这些DLL存储在EDR挂钩的“干净”磁盘上，因为系统使用它们在生成新进程时会将未更改的副本加载到新进程中。由于EDR只在内存中设置这些进程钩子，所以这部分数据将保持不变。ScareCrow不会复制整个DLL文件，而是只关注DLL的.text部分。DLL的这一部分包含可执行程序集，这样做有助于降低检测的可能性，因为重新读取整个文件会导致EDR检测到系统资源有修改。然后使用每个函数的偏移量将数据复制到内存的正确区域。每个函数都有一个偏移量，该偏移量表示它们所在的基址的确切字节数，提供函数在堆栈上的位置。为了做到这一点，ScareCrow选择使用VirtualProtect更改内存中.text区域的权限。尽管这是一个系统DLL，但由于它已加载到我们的进程（由我们控制）中，因此我们可以更改内存权限，而无需提升权限。

一旦这些钩子被移除，ScareCrow就会利用定制的系统调用在内存中加载和运行shellcode。ScareCrow甚至在移除EDR钩子之后也会这样做，以帮助避免被基于非用户钩子的遥测收集工具（如Event Tracing for Windows（ETW））或其他事件日志机制检测到。这些自定义系统调用还用于执行VirtualProtect调用，以移除由EDR放置的钩子（如上所述），从而避免被任何EDR的防篡改控件检测到。这是通过调用VirtualProtect系统调用的自定义版本NtProtectVirtualMemory来完成的。ScareCrow可以利用Golang来生成这些加载程序，然后对这些定制的系统调用函数进行编译。

ScareCrow首先会解密shellcode并将其加载进内存中，默认情况下，shellcode会使用AES加密和解密初始化向量密钥进行加密。一旦解密并加载成功，shellcode将会被执行。根据指定的加载程序选项，ScareCrow会为DLL设置不同的导出函数。加载的DLL也不包含所有DLL通常需要操作的标准DLLmain函数，不过我们不需要担心DLL的执行会出现问题。

代码样例
----

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在加载器的创建过程中，ScareCrow会使用到一个代码库，这个库会做两件事情：

> 代码对加载器进行签名：使用代码签名证书签名的文件通常受到较少的审查，这样就更容易执行而不会受到质疑，因为使用受信任名称签名的文件通常比其他文件更不可疑。大多数反恶意软件产品没有时间去验证这些证书。ScareCrow通过使用Go版本的工具limelighter来创建一个pfx12文件来创建这些证书。这个包可以使用用户指定的输入域名来为该域创建代码签名证书。如果需要，还可以通过有效的命令行选项来使用自己的代码签名证书。
> 
> 伪造加载器的属性：这是通过使用syso文件来完成的，syso文件是嵌入资源文件的一种形式，当与我们的加载程序一起编译时，它将修改我们编译代码的属性部分。在生成syso文件之前，ScareCrow将生成一个随机文件名（基于加载程序类型）以供使用。选择此文件名后，将映射到该文件名的关联属性，确保分配了正确的值。

文件属性样例
------

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

有了这些文件和go代码，ScareCrow将使用c-shared库选项将它们交叉编译成DLL文件。一旦DLL被编译，它就会被混淆成一个断开的Base64字符串，这个字符串将被嵌入到一个文件中。这将允许我们远程获取、访问或以编程方式执行目标文件。

工具安装
----

第一步我们首先要将该项目源码克隆至本地：

```


```
git clone https://github.com/optiv/ScareCrow.git
```




```

在编译ScareCrow之前，我们还需要安装响应的依赖组件：

```


```
`go get github.com/fatih/color``go get github.com/yeka/zip``go get github.com/josephspurrier/goversioninfo`
```




```

确保下列组件已经在你的操作系统上安装好了：

```


```
`openssl``osslsigncode``mingw-w64`
```




```

接下来，运行下列命令完成工具构建：

```


```
go build ScareCrow.go
```




```

工具帮助信息
------

```


```
`./ScareCrow -h` `_________                           _________`  `/   _____/ ____ _____ _______   ____ \_   ___ \_______  ______  _  __` `\_____  \_/ ___\\__  \\_  __ \_/ __ \/    \  \/\_  __ \/  _ \ \/ \/ /` `/        \  \___ / __ \|  | \/\  ___/\     \____|  | \(  <_> )     /``/_______  /\___  >____  /__|    \___  >\______  /|__|   \____/ \/\_/`  `\/     \/     \/            \/        \/`  `(@Tyl0us)` `“Fear, you must understand is more than a mere obstacle.` `Fear is a TEACHER. the first one you ever had.”``Usage of ./ScareCrow:` `-I string` `Path to the raw 64-bit shellcode.` `-Loader string` `Sets the type of process that will sideload the malicious payload:` `[*] binary - Generates a binary based payload. (This type does not benfit from any sideloading)` `[*] control - Loads a hidden control applet - the process name would be rundll32.` `[*] dll - Generates just a DLL file. Can executed with commands such as rundll32 or regsvr32 with DllRegisterServer, DllGetClassObject as export functions.` `[*] excel - Loads into a hidden Excel process.` `[*] wscript - Loads into WScript process.` `(default "dll")` `-O string` `Name of output file (e.g. loader.js or loader.hta). If Loader is set to dll or binary this option is not required.` `-console` `Only for Binary Payloads - Generates verbose console information when the payload is executed. This will disable the hidden window feature.` `-delivery string` `Generates a one-liner command to download and execute the payload remotely:` `[*] bits - Generates a Bitsadmin one liner command to download, execute and remove the loader.` `[*] hta - Generates a blank hta file containing the loader along with a MSHTA command to execute the loader remotely in the background.` `[*] macro - Generates an Office macro that will download and execute the loader remotely.` `-domain string` `The domain name to use for creating a fake code signing cert. (e.g. Acme.com)` `-password string` `The password for code signing cert. Required when -valid is used.` `-sandbox string` `Enables sandbox evasion using IsDomainedJoined calls.` `-url string` `URL associated with the Delivery option to retrieve the payload. (e.g. https://acme.com/)` `-valid string` `The path to a valid code signing cert. Used instead of -domain if a valid code signing cert is desired.`
```




```

项目地址
----

ScareCrow：点击底部【阅读原文】获取

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf+小程序：把安全装进口袋 小程序

精彩推荐

  

  

  

  

****![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

  

  

[![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)](https://mp.weixin.qq.com/s?__biz=MjM5NjA0NjgyMA==&mid=2651117192&idx=1&sn=0048bd232280972c444fbee4245e0d4c&scene=21#wechat_redirect)

[![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247485679&idx=1&sn=98231f665beaa2e51e310868a842bf49&scene=21#wechat_redirect)

[![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247485648&idx=1&sn=5541b19c332754ec2073879966e6b181&scene=21#wechat_redirect)

**************![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)**************