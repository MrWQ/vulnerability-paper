\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzUyMTA0MjQ4NA==&mid=2247494911&idx=2&sn=224f8d17f049d4dd265380e1a74f3637&chksm=f9e383a4ce940ab27510ff78e7e867eea3f1cd9ebed6936f95a081c1ed0e6a0deaf6123220ad&mpshare=1&scene=1&srcid=1018d0wWSH7Te3BdrlPLk0P2&sharer\_sharetime=1602994646541&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=4cf40c946f4d610cfd92cf5446916951cdae9f4a51b473b5193281622a4763b11d59b47d6fcd57d6fc642f4cfe2bd69d994939a4d5cd7e4f8c2d443836b49ac266157aa26e09891c54e07704dbe8516019a7325f451f08022f429d07d5567c31e0676696845e94ce43359ee2c744b039ca273201c8de87c30646c2a2da96da5f&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=Ad2HqQ20FDe68MtV36qHLQc%3D&pass\_ticket=fNc1mNErgeHhn4jm0DcjBlD5hkXepEyD08VA%2B16wYw5QmvtETgayFa%2BrZuz3ot9i&wx\_header=0)

在公司同事的要求下写了这份android APP测试点说明  
此文章无技术性原理阐述，完全是对测试点的测试步骤的描述。  
适合不要求理论与经验的人直接上手傻瓜式干活。  
像这种毫无理论性的傻瓜式文章也适合我这种菜鸟写出。  

大佬可绕行( •͈ᴗ⁃͈)ᓂ- - -♡﻿

![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icnm6kCgy7CSoPyDcs9g8o59fOyvHOzcMSl7tpC9TIV0h3uXIZwW1nEaMqWOTbpMNz53oM86qu98iaA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

个人总结经验来看

拿到APP，首先从两方面测试：APP自身漏洞以及APP常规漏洞（与web差不多，思路以及技术性要求较多，本章不做阐述）

APP自身漏洞：反编译、代码混淆、二次打包、activity组件调用、so动态注入等。下面对于测试点做简单描述

**一、反编译：**

1、简单方式、可借助图形化工具：ApkIDE，直接将测试的APP拖拽到ApkIDE中进行反编译。  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icnm6kCgy7CSoPyDcs9g8o59cZ74r15icLQYHCS2ibIPcCog9a6LIYoKWKNib68fW6fI95bZOpjKiaTbxw/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

反编译可以看APP是否加壳，加壳文件一般都在lib文件中。（一般第三方SDK文件也会存在lib文件中）

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

加壳后的app即使反编译也是反编译出来的壳文件，不是APP真实源码。

2、利用apktool命令行也可进行反编译。

反编译命令如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

重新打包命令：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

3、利用dex2jar 、JD-GUI可反编译查看dex文件

找到我们准备测试用的apk，并将 后缀.apk改为.zip

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

将test.zip解压，并查看目录，找到classes.dex

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

并将这个文件拷至**dex2jar工具存放目录**下

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

打开控制台，使用cd指令进入到dex2jar工具存放的目录下，如图

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

进入到dex2jar目录下后，输入“dex2jar.bat    classes.dex”指令运行

执行完毕，查看dex2jar目录，会发现生成了classes.dex.dex2jar.jar文件

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

上一步中生成的classes.dex.dex2jar.jar文件，可以通过JD-GUI工具直接打开查看jar文件中的代码

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如果APP被加壳的话，反编译出来的dex文件也会是壳文件。

**二、代码混淆**

 按照1的步骤，在APP没有加壳的条件下，进行反编译出来源码。

代码混淆风险分为两种:一种是没有做任何混淆保护，另一种是对里面的关键函数进行了替换，只是增加了攻击者分析代码的难度。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

反编译出来后的源码

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

一般的代码混淆，都是用Android SDK自带的混淆器ProGuard。混淆器可以通过一些方法来保护你的代码不被反编译，他们不会阻止反编译器或者dex2jar对你的代码进行逆向工程，但是他们会使反编译后的代码变得更难以理解，

最简单的方法，他们将APK中所有的变量和方法的名字和字符串转换成一到两个字符的字符串，这就是从Java源码中去掉了很多代码的含义，使其更难找到一些特定的信息，比如说找到一个API key 或者你存储用户登录信息的位置，好的混淆器还会改变代码的流程，，大多数情况下可以把业务逻辑隐藏起来，混淆器不会阻止一个一心想要破解你这个应用的黑客去理解你代码所做的事情，但他会让这个过程明显更难了。

**三、二次打包**

二次打包就直接在一上反编译的基础上、进行修改代码后的再回编。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

      此二次代码只是在图片上进行了打X修改。

**四、activity组件调用**

组件调用，就是测试组件的权限问题，比如一些组件只有在用户登陆的状态下才可以访问，但是我们却可以借助工具直接调用并访问。

需借助工具drezer，在手机端安装drozer.apk，电脑端进入drozer目录下运行CMD命令。

电脑端连接手机。普通模式，需要开启USB调试，

adb forward  tcp:31415  tcp:31415   //将pc端31415的所有数据转发到手机上的31415端口

drozer.bat console connect   //使用drozer console 连接agent

获取手机上所有安装的app包名：run app.package.list  加上”-f \[app关键字\]”查找某个app，如 run app.package.list -f sieve

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

得到sieve的包名为com.mwr.example.sieve

获取sieve的基本信息 run app.package.info -a com.mwr.example.sieve

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以看到sieve的版本信息，数据存储目录，用户ID，组ID，共享库，权限等信息

查找攻击面，主要关注Android 固有的IPC通信机制的脆弱性，这些特点导致了这个App泄漏敏感信息给同一台设备上的其它App

run app.package.attacksurface  com.mwr.example.sieve

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

进一步获取每个组件的攻击面信息，如activity

run app.activity.info -a com.mwr.example.sieve

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

其中. MainLoginActivity是app启动时的主界面，必须可以导出，但其他两个activity正常情况下是不能导出的

用drozer来启动可导出且不需要权限的activity

run  app.activity.start  --component  com.mwr.example.sieve  com.mwr.example.sieve.PWList

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**五、so动态注入**

进入so进程文件目录运行CMD命令

连接root过的Android设备或者打开模拟器。将inject和libhello.so拷入设备，设执行权限，执行：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

先看看被注入进程（surfaceflinger）的mmap，可以看到我们的so已经被加载了，紧接着的那一块就是我们mmap出来的：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

从logcat中也可以看到so注入成功，并且以被注入进程的身份执行了so中的代码：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

简单的注入成功

**六、通信数据风险**

即明文传输，抓取流量包截取账号密码，以下截图只是对账号的抓取：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**七、通讯传输风险**

采用安全的通信协议，对通信数据进行多层加密，防止通信中敏感数据泄露。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**八、设备root检测**

app安装在root后手机上可正常运行

通常已经root的设备会提供给恶意应用查看或修改自身配置文件、缓存文件等的相关权限，已经对应用进行非法操作；而恶意攻击者也常使用已经root的设备对应用发起攻击。

在Native层增加root检测的相关功能。

**九、模拟器检测**

app安装在模拟器后手机上可正常运行

通常自动化检测设备会将应用安装在模拟器中运行，一些恶意攻击者也常常使用模拟器来对应用发起攻击，而普通用户几乎很少使用模拟器来运行非游戏类的应用。

在Native层增加模拟器识别的相关功能。

**十、本地数据文件存储**

我们的app里面用到sqlite数据库的时候， 会生成一个db文件，保存在我们手机中。有的时候，在调试数据库，很想看一下里面的表结构是否正确，这个时候就十分苦恼，因为这个db文件不能够直接拿出来，我们知道，在DDMS里面有一个FileExplorer，它里面保存着手机中的各个文件夹，但是尝试打开里面的文件夹的时候，却发现怎么点都没有东西，是真的没有吗？其实是我们没有获取到访问这个文件夹的权限。下面我们就开始一步一步的拿到真机调试中的db文件。

注意：确保你的手机是root过的。

1）、打开adb.exe

 到sdk目录下，找到platform-tools，adb.exe就在这个文件夹下，尝试双击打开，发现cmd一闪而过，然后就没了，打不开？这里提供一个打开adb.exe的方法，在文件夹空白区域，按住键盘shift，同时点击鼠标右键，在弹窗中选择“在此处打开命令窗口”，会弹出如下cmd窗口(也可以直接打开cmd，然后进入相应的路径):

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

2）、打开DDMS（Android Device Monitor）

打开DDMS后，选择FileExplorer，然后我们可以看到其下的各个文件夹，我们要找的.db文件就保存在data文件夹下

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如果FileExplorer下没有东西的话，可以尝试选择左边的手机型号。此时我们点击data，会发现data是无法打开的，然后我们进行下一步，通过cmd执行命令为我们获取相应的权限。

3）、获取权限

在获取权限的时候，需要一步一步的获取文件夹权限。

1、获取data文件夹权限

 在第一步打开的cmd中， 输入命令 adb shell su -c "chmod 777 /data" ， 回车。

 这时data文件夹的权限就获取到了，打开data可以看到其下的文件夹，

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

2、获取dada/dada文件夹权限

 与第一步类似，继续输入命令  adb shell su -c "chmod 777 /data/data"，回车。

 这样就获取到了dada/dada文件夹权限，打开dada/dada,里面保存了个个应用包名文件夹，找到我们需要找的app包名，然后再进一步打开，

3、获取应用db文件

 继续输入命令  adb shell su -c "chmod 777 /data/data/包名"，回车。这时，就打开了这个app的文件夹，db文件，保存在databases里面。

 继续输入命令  adb shell su -c "chmod 777 /data/data/包名/databases"，回车。这时，databases可以打开了，我们可以看到保存在其中的db文件。

 继续输入命令  adb shell su -c "chmod 777 /data/data/包名/databases/\*"，回车。这时，databases下的db文件都被设为可读状态

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

4、导出db文件

 选择需要导出的文件，然后点击右上角的导出按钮，选择保存地址即可

4）、查看数据库结构

db文件已经拿到，那么查看数据库可以使用数据库工具，将db文件导入即可。我这边使用的是Navicat Premium

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**十一、app传输风险**

app具有大量的日志信息输出，其中包含敏感信息等

在SDK包中\\tools文件中，运行ddms

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

即打开实时日志界面。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

写的不全，傻瓜式步骤，不喜勿喷

  

  

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

[ctf系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493664&idx=1&sn=40df204276e9d77f5447a0e2502aebe3&chksm=f9e3877bce940e6d0e26688a59672706f324dedf0834fb43c76cffca063f5131f87716987260&scene=21#wechat_redirect)

[日志安全系列-安全日志](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494122&idx=1&sn=984043006a1f65484f274eed11d8968e&chksm=f9e386b1ce940fa79b578c32ebf02e69558bcb932d4dc39c81f4cf6399617a95fc1ccf52263c&scene=21#wechat_redirect)

[【干货】流量分析系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494242&idx=1&sn=7f102d4db8cb4dddb5672713803dc000&chksm=f9e38539ce940c2f488637f312fb56fd2d13a3dd57a3a938cd6d6a68ebaf8806b37acd1ce5d0&scene=21#wechat_redirect)

[【干货】超全的 渗透测试系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494408&idx=1&sn=75b61410ecc5103edc0b0b887fd131a4&chksm=f9e38453ce940d450dc10b69c86442c01a4cd0210ba49f14468b3d4bcb9d634777854374457c&scene=21#wechat_redirect)

[【干货】持续性更新-内网渗透测试系列文章](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494623&idx=1&sn=f52145509aa1a6d941c5d9c42d88328c&chksm=f9e38484ce940d920d8a6b24d543da7dd405d75291b574bf34ca43091827262804bbef564603&scene=21#wechat_redirect)  

[【干货】android安全系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494707&idx=1&sn=5b2596d41bda019fcb15bbfcce517621&chksm=f9e38368ce940a7e95946b0221d40d3c62eeae515437c040afd144ed9d499dcf9cc67f2874fe&scene=21#wechat_redirect)  

  

【好书推荐】

* * *

****扫描关注LemonSec****  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)