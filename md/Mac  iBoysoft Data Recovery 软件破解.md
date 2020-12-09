> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/eq4JByS_IYxhX2agrHXviw)

 iBoysoft Data Recovery 是一个数据恢复软件，可以恢复硬盘中丢失的文档。

我在移动硬盘上创建了个 APFS 加密分区用来保存文档，前段时间发现这个分区挂载不了，磁盘工具也急救不了。只能找些数据恢复软件来尝试恢复文档，发现 mac 上面的数据恢复软件很少，支持 APFS 加密分区恢复文档的软件只有 iBoysoft Data Recovery 。赶紧下载下来，扫描下坏掉的分区，输入分区密码，发现可以恢复文档，得救了！！！点击恢复，居然要购买才可以恢复，一看价格，90 刀一个月，无奈囊中羞涩，只好把它破解了。

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3O1rpAPcx859e6XusrRiaSIiaiaMKawicU6v518JYDnsF10IIMMY74mRxBoSLnciaFetcZ6GILPbtdviaGg/640?wx_fmt=png)

**工具准备  
**

*   IDA
    
    IDA 用来查看反汇编代码、F5 查看反编译代码，网上很多资源，这里用的是 IDA 7.0 ，装个 windows 虚拟机，然后在虚拟机里面装 IDA 就行。
    
      
    
*   Radare2
    
    Radare2 用来方便转化反汇编代码，如果安装了 brew ，可以直接通过以下命令安装，没安装的可以查下安装 brew 的教程。
    
    ```
    brew install radare2
    ```
    
      
    
*   Xcode 
    
    Xcode 主要用到它的签名工具，可以直接在 AppStore 安装，或者使用下面命令安装工具箱：
    
    ```
    xcode-select --install
    ```
    
      
    

**安装使用软件**

下载 iBoysoft Data Recovery ， 目前是版本是 3.6

https://iboysoft.com/download/iboysoftdatarecovery.dmg

安装后打开软件，插上移动硬盘，选择加密的 APFS 分区，输入分区密码进入

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3O1rpAPcx859e6XusrRiaSIia9eNwOmK1MrKudK1NiadS35qDnSYtBlaNVpX0CVSGopj3DNO8Cl4lwyw/640?wx_fmt=png)

然后它会扫描分区上的文件，即使是坏掉挂载不上的分区，也可以进入扫描。选择一个要恢复的文件，点击 Recover

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3O1rpAPcx859e6XusrRiaSIiaCPQTKh4ibw9VESibK4zYWP64lECR2a4uIYTc9ZHrqxGchDickt63dKxug/640?wx_fmt=png)

发现免费版本不能恢复加密 APFS 分区的文件

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3O1rpAPcx859e6XusrRiaSIia8rPO6wvs5PjIDXkLBJDHfr7X30XgMCnhEbMiaYtopGmvL9TaFo0YC3Q/640?wx_fmt=png)

**开始破解  
**

在应用程序目录里找到 iBoysoft Data Recovery.app， 右键显示包内容

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJHv7KnG2MwEHeb7gbVI9vEbicKrWhmxjemP8h2Dic46vazE9L7oE3COcA/640?wx_fmt=png)

在 / Applications/iBoysoft Data Recovery.app/Contents/MacOS 目录下还有个 iBoysoft Data Recovery.app ，继续显示该文件的包内容

在 Contents/MacOS/ 目录下的二进制程序就是直接运行的程序，路径如下  

/Applications/iBoysoft Data Recovery.app/Contents/MacOS/iBoysoft Data Recovery.app/Contents/MacOS/iBoysoft Data Recovery

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJU2IicN6VYvMMlXiaHnIiakHElIBSuHKermmyQubzTNtojqBxUb1OaGYTw/640?wx_fmt=png)

把该文件复制到虚拟机中，用 IDA x64 打开

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJdA0PicibBAWRQpTcEv7G2U3SCvrMSVRzjicIes1kBjCk61T8Vcicxtl84g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJqlwcr6s4PE3cuTwCYPA302kFBiczgq0AAqh1VdNvQTTaXzW6KDfMd9A/640?wx_fmt=png)

由于激活弹窗是点击 recover 按钮才出现的，先在 IDA 的函数窗口按 Ctrl+F 搜索下有没有对应的函数，发现有个 recover_click 函数  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJAs1H25pUHIiaibqiaDA55Oa7AiaZbzzAtVhJoq2WOcW7fAPjLeQ96jZSkg/640?wx_fmt=png)

点击该函数，按 F5 反编译代码，可以看到是用 object-c 写的  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJ1LMQApR5b4BYib6iaUzs9c3QOT4vzofeZq9AeWZhXDAHn9r3yY6z767Q/640?wx_fmt=png)

查看代码，发现在 229 行处获取了个版本号，然后在 231 行处判断如果不等于 16 进入 if 语句，在 236 行处弹出激活窗口。在这里可以猜测 productVersion 是一个版本号，不同版本号对应不同的功能。  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJasNhNPfkfy5MwuG6LgZQBGw2XibnTgiaoFr81DKjEm6caD11uCnjFicNQ/640?wx_fmt=png)

在前面也有版本号的判断，如果大于 17，就跳到 LABEL_14

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJvEM3STicR2UmrqeosTo4bNf2TvOhftNNxicBBFL2zfYWVBVR17NKhbicw/640?wx_fmt=png)

双击 LABEL_14 ，跳到该处的代码

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJqSKn5oaxsWGicIpXdLkxQXWjlqoxDnCicbYMDo3NuYjiawCDZ0qicyhxmg/640?wx_fmt=png)

一直看到 300 多行的地方，发现这里是有点像处理恢复数据的代码了，可以确定上面 198 行处的 goto LABEL_14 是关键跳转

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJCaratBNvRHH4CxCT5Y3eVqD6kZsYRbFnicKyaWRyNSHEPjBuxuJzklg/640?wx_fmt=png)

这里为了方便，直接修改 197 行处的判断，让代码总是跳转到 LABEL 14，看看是否可以直接恢复文件。

点一下 if 语句这里

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJoS1jLKMIheKTBP9j9GUMic2gIRtfuy5wichjPqUbh2YIaZicUkLqQtZAw/640?wx_fmt=png)

然后切换到 IDA View-A 窗口，在窗口中右键选择 Synchronize with Psedocode-A 

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJab1EulZOgO8icM03Ytjx07sqeSjAsp50fKC9J1wFEPRJakn8YPCAQVQ/640?wx_fmt=png)

此时汇编代码窗口的汇编代码会和反编译代码的 if 语句同步，  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJMafBng7ktlWj0F2UgoKamclXAYKWD0VeDiaNlovJ4yibu2KTlibFk7scg/640?wx_fmt=png)

选中箭头处汇编代码的十六进制数据，右键复制

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJ5CqG2tQLXm0tPjP68uYAybx14cvedkW7K1nfr4dHjLTVzkDXcBhLFQ/640?wx_fmt=png)

回到 mac 系统，使用 rasm2 命令把这段数据翻译成汇编代码

```
rasm2 -a x86 -b 64 -d '0F 8F DC 00 00 00'
```

可以看到是 jg 0xe2 指令， 这条指令是如果大于，则跳转到 0xe2 处，我们把它直接修改成 jmp 0xe2 这样无论是否大于，都会跳转到 0xe2 处。使用下面命令生成 jmp 0xe2 对应的十六进制数据

```
rasm2 -a x86 -b 64 'jmp 0xe2'
```

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJhBiaDuCHDgk6Ek0UW8HxSb7rprCwR1e3mlcFMBVl1756MFHDaHOuj0A/640?wx_fmt=png)

jmp 0xe2 对应的十六进制数据是 e9dd000000 ，回到 IDA  ，把

jg loc_100018BFE 处的十六进制数据修改成 e9dd000000，具体操作如下：

把鼠标放在 0F 处，点击菜单的 Edit - Patch program - Change byte

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NCX1icZF48HffAETTl05txJWnzyO5No6tnJmTLnLpWDmJo24M99JK3qNtgsgHF0MMP3U0m1SWVGEg/640?wx_fmt=png)

把前六个字节修改成 E9DD0000090， 90 为 nop 指令，什么也不做

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtU943lfJlPATHp78iaHNEborhPnia5pZiaBiaruE0iaEIo2fibfCRL3hQdiaTw/640?wx_fmt=png)

修改后就该处的汇编就变成了 jmp  loc_100018BFE

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtLvS9rFAibAnSmHJnXcaXBWgw46EjiaDecoibS46Co4BT8TDsp6XicoXR5w/640?wx_fmt=png)

修改完后，在 IDA 中 Edit - Patch program - Apply patches to input file 处把修改后的内容写到程序中

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4Htlica8wq4Ih9L9D7dNn3ujb2ibvW273Ww7zjgRBajMBZR3BL0PyCMXOhQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtrAFC3ctLAkRgRNVVcwIaZMqY1ibjFcY9kbS16aRRrQMjZJ0iaWhYRQjQ/640?wx_fmt=png)

接着备份下原来的程序，把下面文件复制到一个目录中，如果上面的修改出错了，就用这个还原程序

/Applications/iBoysoft Data Recovery.app/Contents/MacOS/iBoysoft Data Recovery.app/Contents/MacOS/iBoysoft Data Recovery

然后把虚拟机中修改后的 iBoysoft Data Recovery 替换上面路径中的原程序

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtkdMV9pVAYAUccAHGic4Gb6CH4gcEPwCNFZLZUN3cKtsRPLicFPeljw3A/640?wx_fmt=png)

修改过后的程序，需要使用 codesign 命令对它重新签名，因为 mac 的 

GateKeeper 安全机制，如果不重新签名，软件会闪退。  

先生成一个证书，然后用这个证书去签名，打开系统自带的钥匙串访问 APP

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4Hto3SrsOWNibfV5icWxPp7oo41Qt60iacgnWk9YcUZ4AFUicYoy6RUpOxoQA/640?wx_fmt=png)

点菜单栏 - 证书助理 - 创建证书

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4Ht3ZaPrFoQquhtJVeBhc698FbhulO15nPY6uASaDhWCOGHklue8uHoGw/640?wx_fmt=png)

输入证书名，身份类型选自签名根证书，证书类型选代码签名，勾选选项  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtFHbaULficn8N2DTZ0eyqBR8Cs3ibcvt1cDgIyjuODr563vpKuenK4hIg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtgegNz6ibU3UE0Ke33rqWaju1ic81tMnfIibwqcKPyfhdVwBaicLTIDzZfw/640?wx_fmt=png)

随意填些信息一直点继续即可

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtpyqVbdQgclKAbeLW2GIfyqeY4dnicic4hy4j97uH5oXGLibnU8uNJSAyg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtPSicX8clP9zl5Y8UCT8OI0icKLtViaGljx5vQEcI4GmOQhicDe9RibDbvEg/640?wx_fmt=png)

创建完成后，使用下面命令给修改后的程序签名，在弹出的窗口中输入密码允许使用签名

```
codesign -f -s testcert '/Applications/iBoysoft Data Recovery.app/Contents/MacOS/iBoysoft Data Recovery.app/Contents/MacOS/iBoysoft Data Recovery'
```

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtlG0KERgUowibJlxce16oYsL60O57OibQ8xJeST9hfc3J5biaKia5UuSpIw/640?wx_fmt=png)  

签完名后重新打开 APP，打开加密的 APSF 分区，选择一个小于 1G 的文件，点击 Recover

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtLEial4WHvFrlj1qlIzqlmtIJD3thiba9hqOjcwHicyC5Jnh565R66SUtQ/640?wx_fmt=png)

成功恢复，似乎破解成功了！

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4Ht9aNWSKOG9MR9MImcdIvYGjMdT2bEFiauG3wJz94mqChLyibSSATHrRGw/640?wx_fmt=png)

接下来选择一个大于 1G 的文件进行恢复

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtCJNqJSLTAjiatfjvgV21S41spCGRxHmAuJLa1jJicqEf6GyYcwhFvhhQ/640?wx_fmt=png)

激活窗口又出来了。。。提示说免费版本只支持恢复 1000 M 的数据，看来是在恢复的时候也检查了版本号。

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4Ht4y3fRmyRHj6ST0nIOq2Yl8pgdv0ojibtWDraSSdwOPKFT9wpPNlsHIg/640?wx_fmt=png)

只能继续肝了，毕竟我的分区里面的数据可不止 1G 。通过刚才的分析，这个软件检查激活的方式是检查版本号大于某个值，所以看下所有引用到版本号的地方，看看有什么线索。  

在反编译的地方把鼠标放到 productVersion 字符串上，然后回到 IDA View-A 窗口

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtHmYb67Gdf4dBwPxc8Dgphq8DytWXEAw8piadG1otLLiatrSRuxrl3cgA/640?wx_fmt=png)

可以看到已经同步到该字符串的汇编代码处

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4Htjox3ftXDUrpChb1KjTOwRW0L9WYJonJQVwe4aa5LGBcic0DDw6V2IRg/640?wx_fmt=png)

在此处按下 x 键，查看交叉引用，看看哪些地方引用了版本号  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4Ht4865icon1FI6JbAial2icJfAeSqe1gKjBC7aOubZDm1ibD4gpib6VGTKshw/640?wx_fmt=png)

可以看到引用到版本号的地方有 18 处，一处处的点进去，然后按 F5 查看反编译代码。

在 [ViewControllerManager __updateWindowTitle] 方法里面发现了各版本号对应的名称

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4Ht7x329SygKFicAZoSibFf9OgKMmf0N51VV2fGEh8j8hGPHPTdiadicMtZUw/640?wx_fmt=png)

可以看到版本号是 16 时是免费版本、17 是标准版本、18 是专业版本、19 和 20 是专家版本。  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtTSc5buT3THhlyaTF0CkXocxO1PteDUURGR0pTv1EdIors1QQicfKobA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtlfBZzcfvc8qK30en0qt45ayxn7IdLuBsLAEjhfwxWtdkPmVH9aZ8Pg/640?wx_fmt=png)

但经过查看，没有发现通过检查版本号，然后提示免费版本不能复制 1000 M 以上的地方，估计是在恢复文件的库里面检查的。

既然这么多地方检查了版本号，如果我们直接修改返回版本号的函数，让它直接返回 20 ，这样就可以一劳永逸了。  

查看前面获取版本的地方，可以看到是调用了 iBoysoftVersionManager 类的 instance 方法获取了一个实例，然后调用实例的 productVersion 方法  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3ORA8b5F16fDJk2ohRfG4HtdHOdJK8Vo5ShZlW3TSCDASqeeDKhbmR95ZKe7ZQXxRogxKtg3aM3wg/640?wx_fmt=png)

iBoysoftVersionManager 的颜色是粉红色的，说明是引用的外部库中的类。在 IDA 的 Import 窗口按 Ctrl + F，输入 iBoysoftVersion 过滤导入表，

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYfvUqjOmeyNic96cKuJDn6rb4AG3aeUia64XK5VQ2sgTLnA3lvC1CufTQ/640?wx_fmt=png)

可以看到该类是从下面库中导入的

@rpath/DataRecoveryWapper.framework/Versions/A/DataRecoveryWapper

对应在本机的实际路径是

/Applications/iBoysoft Data Recovery.app/Contents/MacOS/iBoysoft Data Recovery.app/Contents/Frameworks/DataRecoveryWapper.framework/Versions/A/DataRecoveryWapper

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYKsN97k02h4HdB7cBmV6xoibH3riaqTTvTsvebEVejLegic2wwwy9LAsPQ/640?wx_fmt=png)

把这个文件复制到虚拟机中，用 IDA 打开，在函数窗口中 Ctrl+F 搜索 

productVersion

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYuQtSaofgCzbaiaucLum8L4ctlhRHG0FALXPkDcSsn1CgTTopDoCu2eA/640?wx_fmt=png)

点击该方法，F5 反编译，可以看到这个方法大概的功能是从本地读取版本号然后返回。

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbY126VwWMfL6O0ngT3ukhX9bS8gjc2GlKc8ptb9iaDBKkNPj7tTtldkBA/640?wx_fmt=png)

我们的目的是让它直接返回 20 ，现在看看怎么修改汇编代码。先查看开头的汇编代码：

先保存了寄存器的值，然后增加栈空间，在 0x882E 处给 ebx 赋值 0x12h，也就是 18，接着比较 al 的值，如果是 0 则跳转到 loc_89D0  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbY72N54KaoHjsCj0La8xadII4iciaRrVEUticlTmYQxicEft00VHKZ0jM63g/640?wx_fmt=png)

双击 loc_89D0 ，发现是函数结束处， 先把 ebx 的值复制给 eax ，然后减小栈空间，接着恢复寄存器。所以如果我们在前面把 20 赋值给 ebx ，然后直接跳到这里，就可以让函数返回 20 了。

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYKjljLYAUWhOJPhadRt0qPfPDR0F0SsfZKR2ZkFicZ7zdBsp9M974GOg/640?wx_fmt=png)

回到前面的汇编代码，把 mov ebx, 12h 修改成 mov ebx, 14h，也就是把该处的二进制数据从 BB 12 00 00 00 修改成 BB 14 00 00 00  

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYKIdBiaxyiae24Hmia6O7hOPOknwrI4nQXPqiaqJfpxcNrMTKiaicZ00B0ricw/640?wx_fmt=png)

然后把 0x882E 处 jnz loc_89D0 指令的数据 0F 85 95 01 00 00 复制出来，使用下面命令还原，查看偏移值，和生成 jmp 指令。

```
// 查看数据对应汇编，获取偏移
rasm2 -a x86 -b 64 -d '0F 85 95 01 00 00'
// 生成跳到该偏移处的汇编
rasm2 -a x86 -b 64 'jmp 0x19b'
```

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYnqGmCRQJ0qniaIEFuYrFia33Pdc7YoYTnywk4HeYa4ia6waEdT6sdoa1g/640?wx_fmt=png)  

也就是要把 0x8835 处修改成 e99601000090

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYeFTYYCjgwRmP5nPtRkVNDm0zocmYpibicroFSc1WuYibt4OhhcctrSJbw/640?wx_fmt=png)

修改后保存到文件，然后复制替换原本的文件

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYy4HO3RLApMDaqu116ibEeTSuujGupicnH4oBplsvDvHCzq7aQdvficLdg/640?wx_fmt=png)

使用下面命令重新签名

```
codesign -f -s testcert '/Applications/iBoysoft Data Recovery.app/Contents/MacOS/iBoysoft Data Recovery.app/Contents/Frameworks/DataRecoveryWapper.framework/Versions/A/DataRecoveryWapper
```

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYOQpkJGQ9uFbYG18OLg7icAJOUl2VTmdt9FVEFwyQkUFB0JIvKeoMt3g/640?wx_fmt=png)

再次打开 APP，从菜单处可以看到已经没有激活的功能了，而且标题是专家版本。

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYhD5JGdN2ECeGIVdDHRics3OCJW4h4kB6xloQ2X8fzfSyanpiasD3yFGQ/640?wx_fmt=png)

再次恢复 APFS 分区中大于 1G 的文件，发现可以成功恢复了，成功破解！

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYCUR043WaG5wFR16Rcxc2rwuyP913Xn8Pgk9nflX76iaNtmKQQ498Nnw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbYzfdleYwye9k6455JXoIY2vJrwhvObU3tZDCxiblm1MxUHGk8oPe9VibQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FBqhGNuyQ3NYInAzPFpiaeB2DjCCNHhbY5Mn3S7pdO1k1jiaubJ6W6FGNmqMWQdEyiar2cicm5AEQxoqF8QTnFahYA/640?wx_fmt=png)

终于取回了损坏分区的文件~~~