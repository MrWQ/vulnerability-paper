> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/1RqMwJevHShFQmHc8QnsjQ)

**0x00 前言**
===========

邮件钓鱼通常出现在 APT 攻击里面，但是在日常生活中我们的邮箱也会经常出现一些钓鱼邮件，为了更好的了解原理，我在本地探索了一下宏上线钓鱼邮件，分享出来供师傅们交流。

**0x01 原理初探**
=============

宏（Macro）是一种批量处理的称谓，是指能组织到一起作为独立的命令使用的一系列 Word 命令，可以实现任务执行的自动化，简化日常的工作。那么关于宏的安装和录制就不在这里详述了，我们再来把视线转向我们今天的主角——宏病毒

宏病毒是一种寄存在文档或模板的宏中的计算机病毒，存在于数据文件或模板中（字处理文档、数据表格、数据库、演示文档等），使用宏语言编写，利用宏语言的功能将自己寄生到其他数据文档

一旦打开带有宏病毒的文档，宏就会被执行，宏病毒就会被激活，转移到计算机上，驻留在 Normal 模板上。在此之后所有自动保存的文档都会 “感染” 上这种宏病毒，如果其他用户打开了感染病毒的文档，宏病毒又会转移到他的计算机上

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbCC6mliaWBDp4BZscmia9Ootc6IGgc0XVr2iaPAKiaC3jp2aP5djxLRc1xw/640?wx_fmt=png)

在 Word 和其他微软 Office 系列办公软件中，宏分为两种

内建宏：局部宏，位于文档中，对该文档有效，如文档打开（AutoOpen）、保存、打印、关闭等

全局宏：位于 office 模板中，为所有文档所共用，如打开 Word 程序（AutoExec）

宏病毒的传播路线如下：

单机：单个 Office 文档 => Office 文档模板 => 多个 Office 文档（文档到模块感染）

网络：电子邮件居多

首先 Office 文档被感染病毒，当文档打开会执行自动宏，如果宏被执行，它会去检测当前模板是否被感染病毒，如果没有被感染，它会将释放自身的病毒代码。当模板被感染之后，系统中任何一个文档被打开，都会执行模板中的病毒，宏病毒进行传播

宏病毒的感染方案就是让宏在这两类文件之间互相感染，即数据文档、文档模板

宏病毒也可以通过网络进行传播，譬如电子邮件

**0x02 宏病毒的实现**
---------------

**0x02.1 本地加载**
---------------

用 cs 生成一个 Office 类型的后门

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbjGpU198vlSmOLlTh7mPv2eHbVxX4zibian7lhjh6Yic6yVYY5J5NCbfwg/640?wx_fmt=png)

使用实现设置好的监听器

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbtrRJjqVEXLbADyW2AnbjujPJcxFG76vngcQickJXdbENHIJiarYPeQ2g/640?wx_fmt=png)

复制宏代码

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbzksVoVH6UbJcD0aE8VacJHX2IsEXwtZFRrxeib9QnknbGghIbn4aZ8g/640?wx_fmt=png)

新建一个 word 文档生成一个宏

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbxiaaX1BT35b8fy6ByAjCkJvv7rokfeg9ibL1Z0XWibQFeWoZaFaD72sHQ/640?wx_fmt=png)

找到 project 里面的 Word 对象，将代码粘贴

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbGQXXGiar5wSXDLItgWRr3phQCfz3tkiaFVCmpiazr9n0Xs9MPueayVfNQ/640?wx_fmt=png)

ctrl+s 保存，这里可以保存成. dotm 或. docm 都可以，这两个文件格式都是启用宏的 Word 格式

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbLgH3cpfuuviargYmWTDA7iajWABWUpCJqKZvbvDMQWicaNrVvJBFS6DQg/640?wx_fmt=png)

我这里生成一个. dotm 模板文件

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbryqbvHoa8DDtJtnXrIEZYicQRQptnXeVJy2FY6jseVZicpeTvasbH7IQ/640?wx_fmt=png)

这里我假设已经将 word 发给了我要钓鱼的主机上，可以使用社工的方法使诱导被害者点击启用这个宏，具体方法我就不说了，师傅们自行拓展

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbLP1Uib9roeiajibr2rmjhvBw5rj2iaqfmSQZ6ZxGINicGUKy4m3kPsIQRYA/640?wx_fmt=png)

点击过后发现已经上线了 

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbRibRy66JsCe2MzAe2zjlNDagd31XcGK2JayZj8YTLVQqq3Y2TOcbXSg/640?wx_fmt=png)

看一下上线方式是调用了 rundii32.exe 这个 dll

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbyRbm85SMRAIQW8NaIMlvZCmVqzrFB6f4MnriaN8FUI9w4eONm7nq3fg/640?wx_fmt=png)

科普一下 rundll32.exe 如下：

rundll32 的正常位置：c:\windows\system32

rundll32.exe 是什么？顾名思义，“执行 32 位或者 64 位的 DLL 文件”。它的作用是执行 DLL 文件中的内部函数，这样在进程当中，只会有 Rundll32.exe，而不会有 DLL 后门的进程，这样，就实现了进程上的隐藏。如果看到系统中有多个 Rundll32.exe，不必惊慌，这证明用 Rundll32.exe 启动了多少个的 DLL 文件。当然，这些 Rundll32.exe 执行的 DLL 文件是什么，我们都可以从系统自动加载的地方找到。

对于 Rundll32.exe 这个文件，意思上边已经说过，功能就是以命令行的方式调用动态链接程序库。这里要注意一下。在来看看 Rundll32.exe 使用的函数原型：

```
Void CALLBACK FunctionName (
HWND hwnd,
HINSTANCE hinst,
LPTSTR lpCmdLine,
Int nCmdShow
);
```

其命令行下的使用方法为：Rundll32.exe DLLname,Functionname [Arguments]

DLLname 为需要执行的 DLL 文件名；Functionname 为前边需要执行的 DLL 文件的具体引出函数；[Arguments] 为引出函数的具体参数。

**工作方式**

Rundll 执行以下步骤：

1.　它分析命令行。

2.　它通过 LoadLibrary() 加载指定的 DLL。

3.　它通过 GetProcAddress() 获取 <entrypoint> 函数的地址。

4.　它调用 <entrypoint> 函数，并传递作为 <optional arguments> 的命令行尾。

5.　当 <entrypoint> 函数返回时，Rundll.exe 将卸载 DLL 并退出。

所以说 rundll32 在杀软里肯定是检测重点，因为他要调用 dll，果不其然，被杀，所以我们光制作好钓鱼邮件是不够的，还要能够免杀，这个在下文会提到

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPboaFfu0rTTWyj4hcN0meXd602tqc5icynribW6Kq1pVRicLKAp1V2MQfjQ/640?wx_fmt=png)

**0x02.2 远程加载**
---------------

在 word 里新建一个模板

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbroN88KxpW97M4owKmu6ImyEllIOibfvnQDPJQ61Y8tL4B0ibGa9J3zmQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbBS6PStY3jZ0sSwSHBCl0LP4aWDcN2xvVXyAYe9AewwgxqylM1glNCA/640?wx_fmt=png)

将模板另存为一个新的 docx 

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbIpvkpnibzgNEvnKnbXOcdl8O5O97mba9nuaTmrbjvOxtH5Ak4TM7kRw/640?wx_fmt=png)

把 docx 后缀名改为 zip 后缀

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPb9nsicg9mjeibgCDLt9DFKQDqcrEGk9uwHtLVe9KhvibAgcRSQExc1srlQ/640?wx_fmt=png)

对 zip 进行解压得到以下几个文件

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbRYj1s02mmPDgJD4kuUeIkRGpBoggtMKE7QQuKFia1riaGKBhWGQd5ewQ/640?wx_fmt=png)

找到 word 路径下的_rels 目录再找到 settings.xml_rels 这个文件

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbTfWWRbEDt6OALhBrbg3BicSiaNA4UQ3A0X3IUevVvw3s2Iic9J6B1XvnA/640?wx_fmt=png)

我这里用 notepad++ 打开发现这里他是加载了一个远程的网站，因为他要加载模板就会访问远程

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbIJb1KPKGv2dr7kWUOlnFgu7Hib9tj1suT0uns4jTgKKUpWibeicCEOPjQ/640?wx_fmt=png)

这里用 github 实现远程加载的作用，将之前生成好的. dotm 或. docm 文件上传到 github

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbFkN249ZBYyJb0hOY9KchLeEKZxJibV8uVDt3xMGWKo1ktFNlewIcA1w/640?wx_fmt=png)

将链接复制并在后缀加上? raw=true 放入 xmlns 里

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbYQkEspNTOPSDKoh4PryjyV92MJs7ft10RhpP0KPNg2LafMwLpnnWdQ/640?wx_fmt=png)

再将这几个文件压缩成 zip

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbbyM0O2Rm1hZrHXvhPFB6mrF15ooL5nz6cMZIPKgg4fR4jMErffON2w/640?wx_fmt=png)

改成 docx 后缀

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbHxSbeSyvwVSsVIFeeR1zVAfgKnKUdfmN46HClQnRX6GwMgrEEwD9GA/640?wx_fmt=png)

此时钓鱼邮件就制作好了，这里又假设我已经开始钓鱼，被害人点开了这个文档，还是社工各种方式让被害人点击启用这个宏

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbticzVkba6pmKLYXK4h8vhrGF0VEw9PAtfRZIz0KrnQP4vxfCk6PxiaHA/640?wx_fmt=png)

回到 cs 发现已经上线

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbRibRy66JsCe2MzAe2zjlNDagd31XcGK2JayZj8YTLVQqq3Y2TOcbXSg/640?wx_fmt=png)

老生常谈的还是过不了杀软，因为我最近也在看杀软这一部分，其实免杀最好的方法就是自己的方法去免杀，而不是用网上的工具，因为你拿的网上的工具每个人都可以拿到，免杀效果很差。

但是这里我还没有到能够自己免杀的水平，所以这里先用一款工具进行免杀

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbCKkDYLSsYXy7fMYQZlia1Oib9OHib1Y4KI4iaURZtz9C5KR8fvGpIP0UIw/640?wx_fmt=png)

**0x03 免杀**
===========

免杀这里我选择了一款软件：EvilClippy

github 链接如下：https://github.com/outflanknl/EvilClippy/releases/tag/v1.3

关于 EvilClippy 的介绍如下：

EvilClippy 是一款专用于创建恶意 MS Office 测试文档的跨平台安全工具，它可以隐藏 VBA 宏和 VBA 代码，并且可以对宏代码进行混淆处理以增加宏分析工具的分析难度。当前版本的 EvilClippy 支持在 Linux、macOS 和 Windows 平台上运行，实现了跨平台特性。

关于 EvilClippy 的原理如下：

EvilClippy 使用了 OpenMCDF 库来修改 MS Office 的 CFBF 文件，并利用了 MS-OVBA 规范和特性。该工具重用了部分 Kavod.VBA.Compression 代码来实现压缩算法，并且使用了 Mono C# 编译器实现了在 Linux、macOS 和 Windows 平台上的完美运行。

如果有 vs 环境的可以直接编译生成 exe 进行运行，命令如下：

```
csc /reference:OpenMcdf.dll,System.IO.Compression.FileSystem.dll /out:EvilClippy.exe *.cs
```

我这里用的是在 linux 环境进行免杀，需要先安装 mono 环境，我这里是 ubuntu 系统，如果是 kali 或 cent 命令会不一样

```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb http://download.mono-project.com/repo/debian wheezy main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list
sudo apt-get update
sudo apt-get install mono-completesudo
apt-get install monodevelop
```

安装好了用 mono -V 验证一下  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbBsNzDAp2LGyeAhuy1IJdD7FmVKaB0hFvfxhGBadciaFGgIbJ0Mbx6SA/640?wx_fmt=png)

先对软件进行编译

```
mcs /reference:OpenMcdf.dll,System.IO.Compression.FileSystem.dll /out:EvilClippy.exe *.cs
```

再查看下软件能否正常运行

```
mono EvilClippy.exe -h
```

然后进行免杀操作：

首先需要创建一个 vba 文件，后续需要进行混淆，vba 内容如下

```
Sub Hello()
Dim X
X=MsgBox("Hello VBS")
```

科普一下 vba 文件：

VBA（Visual Basic for Applications）是 Visual Basic 的一种宏语言，是在其桌面应用程序中执行通用的自动化 (OLE) 任务的编程语言。  
主要能用来扩展 Windows 的应用程序功能，特别是 Microsoft Office 软件。它也可说是一种应用程式视觉化的 Basic 脚本。  
VBA stomping  

VBA 在 Office 文档中可以以下面三种形式存在

1、源代码: 宏模块的原始源代码被压缩，并存储在模块流的末尾。可以删除源代码，并不影响宏的执行

2、P-Code: 与 VB 语言相同，VBA 同样有 P-Code，通过内置的 VB 虚拟机来解释 P-Code 并执行，平常我们 Alt+F11 打开所看到的正是反编译的 P-Code。

3、ExeCodes: 当 P-Code 执行一次之后，其会被一种标记化的形式存储在 SRP 流中, 之后再次运行时会提高 VBA 的执行速度，可以将其删除，并不影响宏的执行。

每一个流模块中都会存在一个未被文档化的 PerformanceCache，其中包含了被编译后的 P-Code 代码，如果 _VBA_PROJECT 流中指定的 Office 版本与打开的 Office 版本相同，则会忽略流模块中的源代码，去执行 P-Code 代码  
这种特性很适合用于定向攻击，且不容易被发现。通过信息收集得知目标的 Office 版本，利用 VBA stomping 使宏被特定版本的 Office 打开时才会执行恶意行为宏代码，除此之外的 Office 版本打开时执行正常宏代码

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbcuoLvBLmWeicHMJe3vZCGdbSwta9o0MsruHAsjLoXuSEP5ploouIveg/640?wx_fmt=png)

再进行混淆操作

#先使用一个模块来设置随机模块名，混淆了一些分析工具，会生成一个以_EvilClippy.docm 结尾的文件  

```
mono EvilClippy.exe -r Doc1.docm
```

#其次使用之前设置的 vba 文件对生成文件进行伪装混淆  

```
mono EvilClippy.exe -s 3.vba Doc1_EvilClippy.docm
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbZeTFPibQHOk3MibrcNiaGoVgtibypY3pzO9yDbkrjxCHPls9OcKcQvHYKw/640?wx_fmt=png)

成功后就会生成一个 test_EvilClippy.dotm 文件，这时候把文件拿去 vt 检测一下，免杀效果还是比之前强了很多

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbsc7rtjEcceWsTx6Rz2YwfmMcYj02zSHHsyPH94J1NXd6bfEKiceiakLg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbpQ41tHKFNnWsPhZlBGM9txwdNzpXRfiaRcIvc1BvrUu5NqFSLEQAzYQ/640?wx_fmt=png)

再放进火绒看一下，已经免杀

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbsdZYbeXyD3y6MhWEwyGFt8n0S8OwlfjhicYPbTQCCkhAvjWujSHEveA/640?wx_fmt=png)

**0x04 后记**
===========

我们知道宏加载使用的是 rundll32，而 rundll32 在正常情况下启动的路径应该为：

```
c:\windows\system32
```

所以不是这个路径启动的一定不是计算机主动调用的，我用 procexe64 查看了一下这个 dll 启动的位置，如图所示，很明显不为 c:\windows\system32

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicQ2lV1IQXl7fBp8OsLYmPbjgicjg0KtlDDxOmrIAgm7tNrhAS6aZGCcyKp59TeKaVYENRVb5m4lHA/640?wx_fmt=png)  

宏钓鱼有两个重点，一是怎样社工受害人点击启用宏这个选项，二是怎样躲避杀软的查杀。

目前杀软查杀 VBA 基本上都是静态查杀，所以静态免杀至关重要，从源头上讲 Word 是一个 zip 文件，解压之后的 vbaProject.bin 包含着要执行的宏信息，也是杀软的重点关注对象。

很多诱饵文档喜欢在 VBA 中启动脚本程序执行 ps 或者从网络上下载一段 shellcode 或恶意程序等等，这样非常容易被杀软的行为拦截拦住，同时沙箱可以根据进程链和流量判定该 word 文档是恶意的，安全分析人员可以轻易的通过监控进程树的方式观察恶意行为。

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

**推荐阅读：**

**[干货 ｜ 如何编写 Word 宏木马](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247496318&idx=1&sn=38f4cd6527f79c8ce8298dba78bb00d1&chksm=ec1ca741db6b2e578779c28d7fdd6a907d78281f368fdd97e6ae3e419d1c1579a55e3dcadfc1&scene=21#wechat_redirect)  
**

**[干货 | 恶意代码分析之 Office 宏代码分析](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247493020&idx=1&sn=a6e06e20e32fd14d7723ca014eac3a04&chksm=ec1cb0a3db6b39b5bd5c0bb1d77057be1faa86c3b5a8d1b7025220bbcbbe8872d828be18c024&scene=21#wechat_redirect)  
**

[**Office 如何快速进行宏免杀**](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247492416&idx=1&sn=c444b28f7aa67e9ee15d42bc1aeef10d&chksm=ec1cb67fdb6b3f69d33753fd68cad86f401c07f5fddb3157c81468cab144978a5fb3840da037&scene=21#wechat_redirect)  

[**利用 DOCX 文档远程模板注入执行宏**](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247487401&idx=1&sn=55821cd34f91e44b5b95934878f8430b&chksm=ec1f5a96db68d3807e3dc359870e30ef68cdca47ba206b3d7788d91ec57b98576586e99f5bea&scene=21#wechat_redirect)  

本月报名可以参加抽奖送暗夜精灵 6Pro 笔记本电脑的优惠活动  

[![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvouibfico2qhUHkxIvX2u13s7zzLMaFdWAhC1MTl3xzjjPth3bLibSZtzN9KGsEWibPgYw55Lkm5VuKthibQ/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247496352&idx=1&sn=df6ddbf35ac56259299ce37681d56e5b&chksm=ec1ca79fdb6b2e8946f91d54722a7abb04f83111f9d348090167b804bc63b40d3efeb9beabbe&scene=21#wechat_redirect)

**点赞，转发，在看**

原创投稿作者：HopeVenus

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)