> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/OUxKcNYsuoogC5WS_1YnIg)

从项目中看BypassUAC和BypassAMSI

1

一、概述

在日常渗透过程中，无论执行exe程序还是执行ps1脚本，都可能会遇到UAC或AMSI的阻挠。本文将结合UACME和Dount项目介绍BypassUAC与BypassAMSI的方法。若有不足之处，请大家指出。

  

2

二、BypassUAC

  

---

BypassUAC自然绕不开UACME这个项目https://github.com/hfiref0x/UACME，项目里包含了很多不同种类的方法，其中DllHijack 、Registrykey manipulation、ElevatedCOMinterface这三种方法是项目中出现的较多且好用的，对应23、33、41这三个方法号，下面就动态调试下UACME项目中的这几个方法，有坑的地方会加以说明：

调试前要修改两步：

**第一步：增加方法号参数：**

![图片](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADeyr6lv1lOuxOmFyibSHDZoI5QCNbqGJInmFVbX4oGCIIIqmcAMSPBzthnbpyCIhs6XJ6QVfCN0dw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**第二步：global.h中注释掉KUMA_STUB**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

#### **2.1 调试DllHijack**

可见23这个方法从Win7到win10各版本都还没修复：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADeyr6lv1lOuxOmFyibSHDZoYIeicTa70hQouzTPrIyL28He479MfYbuic6ib0kHiawiaLDaROws8DFR5tg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

在ucmInit()方法中得到方法号，后面也会获得第二个参数即需要执行的命令，默认是打开cmd：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADeyr6lv1lOuxOmFyibSHDZoMk0ubGYjic9pqibKsjDQkTHHZiaaViaSyOMKbVGZ2uuJIhOEiad8dPDVMYA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

然后进行进程伪装，就是根据PEB中的ProcessParameters来获取自己进程信息并修改为系统可信进程：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADeyr6lv1lOuxOmFyibSHDZocKgapeJrKPIQFJYYPuuPYVa3uiafLFvOECvKGSvl0ZxeTxTkZZm6vvQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

然后进行进程伪装，就是根据PEB中的ProcessParameters来获取自己进程信息并修改为系统可信进程：![图片](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADeyr6lv1lOuxOmFyibSHDZonc4MAfbbSaNOsBaiao5mUY3rsPS8o57QQzNyMDy6lK80ibeBMviboUvIw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

接着调用MethodsManagerCall()方法，该方法为主要功能调用的方法，参数为对应的方法号：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADeyr6lv1lOuxOmFyibSHDZoWiaia5S7nWlnQBKfzlmWniaGdfexh27mJUhvBDfC3lCib7WvibIjFpdiaCaA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

经过一系列初始化后根据Method号在ucmMethodsDispatchTable结构体数组找到对应调用方法和所需资源：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADeyr6lv1lOuxOmFyibSHDZovqAAl2ibk7B2wCqnNWDmgsMJ9j4k76g3VVRHw74lUnl2qF1GwXweyTg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

元素结构体的定义，第一个为调用方法函数指针和第三个为所需资源号：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADeyr6lv1lOuxOmFyibSHDZomwzjco9pgcsticoFEKn0ibFibVG8Bqf9qr63nuqWshTrEic7CibOfvibLDibg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

接着判断传入的方法号是否需要相应的资源，如果需要则加载并执行解密操作，我这里修改代码不要解密，直接加载，加密因为是为了让要加载的dll躲避查杀：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

加载的dll内容：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这个dll是资源需要生成的，注意这里需要IDR_FUBUKI64的dll，所以用Fububi项目生成，并存放在bin目录下，并修改名称：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

接着根据UCM_API_DISPATCH_ENTRY结构体里的函数指针调用相应方法：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

23号调用的是MethodDism()：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

继续跟入ucmDismMethod()，先进行版本判断后，再跟入ucmxGenericAutoelevation()函数，在该方法中主要实现对FUBUKI64dll的移动和改名：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

该函数内先调用supWriteBufferToFile()把读取到的资源释放到C:\Users\kent\AppData\Local\Temp\dismcore.dl!:

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

调用ucmMasqueradedMoveFileCOM()函数，该函数中用com接口{3AD05575-8857-4850-9277-11B85BDB8E09}提升权限提升后使用IFileOperation对象将其移动到C:\Windows\system32\：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

移动后用调用ucmMasqueradedRenameElementCOM()修改名字，该函数也是上移动的操作类似：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

上述对劫持的dll操作完后，开始执行相应的命令：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

跟入ucmxDisemer()，函数中拼接好C:\Windows\system32\pkgmgr.exe要执行的程序和/ip/m:pe386 /quiet参数，传入supRunProcess2()调用:

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

构造SHELLEXECUTEINFO对象，传入ShellExecuteEx()调用：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

后面会执行些清理方法，至此23号DllHijack方法分析结束。

  

##### **2.2  调试Registrykey manipulation**

可见33这个方法只支持win10，需要在win7使用可用用25方法号，方式是一样的。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

该方法的原理就是：fodhelper.exe进程会启动时，会先查询HKCU\Classes\ms-settings\shell\open\command注册表中的数据，如果发现没数据，则查询HKCR\Classes\ms-settings\shell\open\command的数据

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

所以构造程序路径并写入注册表，那么fodhelper.exe启动时，相应的程序便启动。

  

修改调试的参数，运行，前面流程是一样的，直接跟入MethodsManagerCall()：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

33号方法没有相应的paylaod（DLL）：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

根据方法号进入到UCM_API_DISPATCH_ENTRY结构体中函数指针的具体方法：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

构造完TargetApp(fodhelper.exe)和payload(所要打开的程序C:\Windows\system32\cmd.exe)传入并调用ucmShellRegModMethod()，先创建键{7E99FF98-7D66-40E8-A095-B6467768C28A}：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

再创建了command键：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后设置SymbolicLinkValue键值，DATA即是要创建连接的注册表名上面所创建的{7E99FF98-7D66-40E8-A095-B6467768C28A}：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

构造SHELLEXECUTEINFO结构体，传入ShellExecute()启动fodhelper.exe：![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

后面清理相应的注册表键值。

  

##### **2.3 COM接口提升ElevatedCOM interface**

41号方法基本覆盖全版本windows系统:

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

该漏洞的原理是利用COM接口提升对ICMLuaUtil接口进行提权，然后利用ShellExec()方法来执行命令。因为要通过CoCreateInstanceAsAdmin()创建COM类，系统会判断程序身份是否可信，若不可信则会触发弹窗，所以这里有两种方法去操作：

做成DLL，使用rundll32去调用，或者注入到其他可信进程

进程伪装，修改PEB中自身的进程信息为系统可信进程

UACME用了第二种方法，进程伪装在2.1中已提及，下面介绍COM接口的相关操作：

由于该方法跟2.2一样是没有要加载的payload，所以直接运行后根据方法号进入到UCM_API_DISPATCH_ENTRY结构体中函数指针所对应的具体方法：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

先初始化COM环境：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

设置BIND_OPTS3，并以管理员权限{3E5FC7F9-9A51-4367-9063-A120244FBEC7}创建名称对象及获取COM对象

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

调用CMLuaUtil对象虚表中的ShellExec函数启动相应的进程：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

对于COM接口提升这类BypassUAC，要满足两点条件：

1、elevation属性为True，AutoApproval为True

先编译出UACME中自带的Yuubari程序，该程序能找出系统下可利用的程序及COM组件：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后使用OleView.Net工具根据CLSID查看找到的接口信息：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

2、COM组件中的接口存在可以命令执行的地方

其中COM接口对应cmlua.dll的虚函数表就有ShellExec()：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

41号这个方法挺好使的，用来做C2的launch来部署环境个人觉得很适合。

  

3

三、BypassAMSI：

##### **3.1AMSI简介**

AMSI（AntimalwareScan Interface），即反恶意软件扫描接口，在Windows Server2016和Win10上默认安装并启用，但安装有些杀软会被关掉，可通过接口来扫描文件，内存、数据，常用于检测ps脚本。

  

##### 3.2BypassAMSI方式

网上看到目前能BypassAMSI主要有三种方法：

修改相应的注册表。

将HKCU\Software\Microsoft\WindowsScript\Settings\AmsiEnable的表项值置为0。关闭WindowsDefender使系统自带的AMSI检测无效化。

Dll劫持powershell程序

在powershell.exe执行目录放置一个伪造AMSI.dll，从而实现DLL劫持。

InlineHookAMSI.dll

Dount是一个基于.Net的免杀混淆组件，这里根据Dount项目介紹下三种方式来BypassAMSI，项目地址：https://github.com/TheWover/donut

把原来amsi.dll中的AmsiScanString()和AmsiScanBuffer()扫描函数替换，让其返回S_OK:

替换成自己的函数AmsiScanStringStub()：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

求AmsiScanStringStub()编码长度：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

改变内存属性，把AmsiScanStringStub()覆盖到AmsiScanString():

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

2、修改其返回验证传递的AMSI上下文参数，使Signature值不为“AMSI”（_0x49534D41_）

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

但现在一旦出现AmsiScanBuffer()该字符串都有可能被WindowsDefender查杀，所以就EggHunter这种方法，也是先加载别的不相关的函数，如DllCanUnloadNow()：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后再通过保存AmsiScanBuffer()前24个字符：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

最后调用FindAddress()从内存捞出AmsiScanBuffer()相应的地址：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

谢谢大家观看。

参考链接：

https://modexp.wordpress.com/2019/06/03/disable-amsi-wldp-dotnet/

https://www.contextis.com/en/blog/amsi-bypass

4

关注

本公众号不定期更新视频和文章 欢迎前来关注观看

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)