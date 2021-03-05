> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sLlYVwykgzny_wrmT_iC-A)

作者前文介绍了微软证书漏洞 CVE-2020-0601，并讲解 ECC 算法、Windows 验证机制，复现可执行文件签名证书的例子。这篇文章将详细讲解逆向分析 OllyDbg 动态调试工具的基本用法，包括界面介绍、常用快捷键和 TraceMe 案例分析。

这些基础性知识不仅和系统安全相关，同样与我们身边常用的软件、文档、操作系统紧密联系，希望这些知识对您有所帮助，更希望大家提高安全意识，安全保障任重道远。本文参考了 B 站漏洞银行、安全网站和参考文献中的文章，并结合自己的经验和实践进行撰写，在此感谢这些大佬们。

文章目录：

*   **一. OllyDbg 界面介绍和配置**
    
*   **二. 常用快捷键**
    
*   **三. OllyDbg 动态爆破软件演示**
    
*   **四. 总结**  
    

> 从 2019 年 7 月开始，我来到了一个陌生的专业——网络空间安全。初入安全领域，是非常痛苦和难受的，要学的东西太多、涉及面太广，但好在自己通过分享 100 篇 “网络安全自学” 系列文章，艰难前行着。感恩这一年相识、相知、相趣的安全大佬和朋友们，如果写得不好或不足之处，还请大家海涵！  
> 接下来我将开启新的安全系列，叫 “系统安全”，也是免费的 100 篇文章，作者将更加深入的去研究恶意样本分析、逆向分析、内网渗透、网络攻防实战等，也将通过在线笔记和实践操作的形式分享与博友们学习，希望能与您一起进步，加油~
> 
> 推荐前文：网络安全自学篇系列 - 100 篇
> 
> https://blog.csdn.net/eastmount/category_9183790.htm

作者的 github 资源：  

*   逆向分析：https://github.com/eastmountyxz/
    
    SystemSecurity-ReverseAnalysis
    
*   网络安全：https://github.com/eastmountyxz/
    
    NetworkSecuritySelf-study
    

> 声明：本人坚决反对利用教学方法进行犯罪的行为，一切犯罪行为必将受到严惩，绿色网络需要我们共同维护，更推荐大家了解它们背后的原理，更好地进行防护。该样本不会分享给大家，分析工具会分享。（参考文献见后）

一. OllyDbg 界面介绍和配置  

=====================

OllyDbg 是一个动态追踪工具，将 IDA 与 SoftICE 结合起来的思想，Ring 3 级调试器，非常容易上手，是当今最为流行的调试解密工具之一。它还支持插件扩展功能，是目前最强大的调试工具之一。

> OD 和 IDA 可以说是逆向分析的 “倚天” 和“屠龙”，一个动态分析，一个静态分析。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibH0b5B4LVCESXXftnlWnEQ501rcz1dfIN2ibUF4NjPibiclDr3S9u2CkyEA/640?wx_fmt=png)

该系列文章参考 B 站漏洞 “游戏逆向交流” 大佬的视频，主要内容包括：

*   OllyDbg 界面介绍和配置
    
*   常用快捷键
    
*   OllyDbg 基本操作
    
*   常用断点 INT 3 断点原理解析
    
*   INT 3 断点的反调试与反反调试
    
*   常用断点之硬件断点原理解析
    
*   常用断点之内存断点原理解析
    
*   常用断点之消息断点原理解析
    
*   常用断点之条件断点原理解析
    
*   内存访问一次性断点和条件记录断点
    
*   插件
    
*   Run trace 和 Hit trace
    
*   调试符号
    
*   OllyDbg 的常见问题
    

推荐大家学习，参考网址：

*   https://www.bilibili.com/video/BV1cE411f7sE
    

OllyDbg 是逆向分析常用的调试工具，打开主界面如下图所示，包括反汇编窗口、寄存器窗口、信息窗口、数据窗口、堆栈窗口。

*   常见动态调试工具：OllyDbg、WinDbg、x64Dbg
    
*   常用静态调试工具：IDA
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHM4nrafaQyfynD9kia3Mayf58iakKQAKK8d7XlYeSP0maFG0SYIjQB9fA/640?wx_fmt=png)

如果我们打开的界面很乱像下图一样，可以点击顶部快捷键 C，然后主窗口最大化即可优化布局。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibH4xwlGzpMY8gTMYsVS9PniaBJpo3ThZaYuVU9LPm5zAkzTS7FyGyU6PQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHIaPZHB9icS6pb7mzLVtbPk0SVDF141mYHSGMvlDr6CZN9mibMWiaicxN8w/640?wx_fmt=png)

接着随便打开一个 EXE 程序，显示如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHyt9gOdhrLdu0JWn4rSTWUBljr66ZLhbp2kNXxvaVbAXSY67iavia237g/640?wx_fmt=png)

下面先讲解各个窗口的含义：

*   反汇编窗口： 显示被调试程序的反汇编代码，包括地址、HEX 数据、反汇编、注释
    
*   寄存器窗口： 显示当前所选线程的 CPU 寄存器内容，点击标签可切换显示寄存器的方式
    
*   信息窗口： 显示反汇编窗口中选中的第一个命令的参数及跳转目标地址、字符等
    
*   数据窗口： 显示内存或文件的内容，右键菜单可切换显示方式
    
*   堆栈窗口： 显示当前线程的堆栈，记录传递的参数或局部变量
    
*   子窗口的快捷方式
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHibPCSb1g3X3PdgHc8l2B1E6ppsmmzmNRW7LtAMIxqYNd8lgpEj7wluw/640?wx_fmt=png)

接着补充界面选项知识点，点击 “选项” -> “界面”，设置 UDD 路径和插件路径。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHzqia2gb4pDib7YiclQRMFRoQTB430FDibA3OfzUkPe4nYDZ49OMshXWJ3Q/640?wx_fmt=png)

UDD 路径用于保存我们调试的信息。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHqoG9OjrkozeiaVicthWDIZFl9lHcib1F3rnkBToIWiaRUHlQtNlKUP2SeQ/640?wx_fmt=png)

插件路径包含了各种插件，并且可以直接使用。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHrqCQaEzmNXhAWD1OTbKiaSH69THTf6icEl3HD5qYTY6GfOAAcmRia2DRQ/640?wx_fmt=png)

如果你想选中一个 EXE 文件，右键直接能够用 OllyDbg 打开，怎么设置呢？

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHazhbBCxmM9YqxkJIvYvBhTq5b2TntjJtJ6jdiaP22tmKkclneZzqZpg/640?wx_fmt=png)

点击 “选项” -> “添加到浏览器”，添加 OllyDbg 到系统资源管理器菜单。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHIol0VHO8sicGTmtuJzBlGibZY65ZrAuPxKHJrA3hFLrzoiaibyAZ17Drdg/640?wx_fmt=png)

如果我们每次运行 OD 都提示管理员权限运行，则可以进行快捷键简单的设置。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHTU0DaLCk4uACQz1JticbhYx8XMhX4NXZj4icXcLiaO2T7jzo7O0DYOJHg/640?wx_fmt=png)

设置方式如下：兼容性中选择 “以管理员身份运行此程序”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHGNn2NbUfV7oSDz445XibK5pyxFl6VHbkp5elA9BwUu3JgAc5ic2p8LDA/640?wx_fmt=png)

二. 常用快捷键
========

下面简单讲解常用的快捷键调试方式。

F2：设置断点  
设置断点，只要在光标定位的位置按下 F2 键即可，再按一次 F2 键会删除断点。如下图所示的红色位置，程序运行到此处会暂停。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibH1wTa1bA0ujvGEWOcErvbeuxSKYF3yzyKWX3gRp5jibHoozh1vO26EHA/640?wx_fmt=png)

F9：运行  
按下 F9 键运行程序，如果没有设置相应的断点，被调试的程序直接开始运行。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHCvqgicmUgKy8xRN6EsPNicQvhuXvPpLAmCpdR8u2iaDdZhicqic5ribQUVFw/640?wx_fmt=png)

F8：单步步过  
单步步过，每按一次这个按键，将执行反汇编窗口中的一条指令，遇到 CALL 等子程序不进入其代码。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHLvvtX5I4qDMRNZm8n1ibCGta1EIruzcwlKvVpe0MaCwDszlwK3lBIcA/640?wx_fmt=png)

F7：单步步入  
单步步入，功能与单步步过（F8）类似，区别是遇到 CALL 等子程序时会进入其中，进入后首先停留在子程序的第一条指令上。如下图进入 CALL 子程序。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHibkk0EhtaSUu2eXJKwtVicFZ7YvuqBTMV2U88pLP8xUo1kAoSGgwwLRw/640?wx_fmt=png)

CALL 表示进入函数，RETN 表示返回。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibH1ibBxNjzXuhJ3H0ncgiaec7wyjh7svkDFOWOKfyh0jTjR2qVyj3TS6OA/640?wx_fmt=png)

F4：运行到选定位置  
运行到选定位置，作用就是直接运行到光标所在位置处暂停。比如光标在 0x00401034 位置，我们接着从 0x00401027 运行，这会直接跳转到光标处。当我们调试过程中遇到循环，可以调至光标跳过循环。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHs0p3SbU8C0nOmiaJRtK6eKHO0JyR4Sjn9Mh7AicdGxPF8srTdp31ZbgA/640?wx_fmt=png)

CTRL+F9：执行到返回  
执行到返回，按下此键会执行到一个返回指令时暂停，常用于从系统领空返回到我们调试的程序领空。在调试程序时，按下 CTRL+F9 会一直运行程序，直到一个 RETURN 返回，比如我们进入下图所示的子程序，会运行至 RETN 10。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHk3g1wpOLT52UPwO43XFgK8YVeDBTtib8VsUXZZjCNLMADwH4Afib2Yiag/640?wx_fmt=png)

再在 RETN 10 位置按下 F8，则会返回如下图所示的位置，执行完 CALL 函数进入下一句。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHQZlWqMdoDiaEIh0lZ8IwPNKMvXice2wVkkicKNU1Q0t7UYg2ZiacbdX32g/640?wx_fmt=png)

CTRL+F2：重新开始  
当程序想重新调试时，按下 CTRL+F2 即可。

ALT+F9：执行到用户代码  
执行到用户代码，从系统领空快速返回我们调试的程序领空。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHv5VCQPcWJ78lAVlTGMJ2JCmAH9RhFSpvibZ5Ys92EDViae4xS9qH0eqg/640?wx_fmt=png)

三. OllyDbg 动态爆破软件演示
===================

下面以《加密与解密》的 “TraceMe.exe” 程序为例。程序下载地址：

*   https://github.com/eastmountyxz/Reverse-Analysis-Case
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHBiaFibrqooDIBDaXnFoxXibr90VKVfBpicJSDLIgUwtoMaRcltKib25qr2Q/640?wx_fmt=png)

当我们输入错误的用户名和序列号，点击 “Check” 按钮会显示输入错误。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHnpuN0NogzRgcrB1R07ibF7V4M69gUu5JVFbibdZKR73IG95BnzCYugEw/640?wx_fmt=png)

接下来我们需要用 OD 爆破，该程序的基本流程如下图所示，只有输入正确的用户名和序列号才能显示正确对话框。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHdWSKMeHHsPbIWnx06ALhl5NZZqst7G82iawgw806o3NyBhpmsFicNXNw/640?wx_fmt=png)

接着通过 OD 打开该程序，它会自动定位到模块入口点 0x004013A0 位置。作者 github 资源提供了各种 OD 版本供读者使用。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibH5jMhMFjcAKzHwaI1XWs48hzTMq66icAPLI5IVyhjHJG9siboM84PMQgg/640?wx_fmt=png)

第一步，首先按下 F9 程序就会运行起来，并且弹出对话框

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibH6PWEticmKHn2nPqrESHTkoUAMR59I2RfY3pX2UXGibqWc5nMH6ic3pGDA/640?wx_fmt=png)

第二步，我们需要知道输入对话框输入值的函数都有哪些  
点击 “API 断点设置工具” -> “常用断点设置”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHGZDwANBX4UOpibFtxib99JfIVcFvG8xlSblVpSdfibIIyF3XIdlESZkrw/640?wx_fmt=png)

勾选获取对话框的输入值的两个函数 “GetWindowTextA” 和 “GetDlgItemTextA”，这意味着给这两个函数下断点，当程序运行到某个函数即会停止。如果读者不确定对应的函数，可以勾选所有的函数。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHq7iak6r4P076TGVULrp2CHOAaBoLSUcEsXFp52JfJg5wpiasMEk5Ey6g/640?wx_fmt=png)

第三步，输入用户名和序列号并点击 “Check” 按钮  
此时程序进入 0x75CA4390 位置，并且显示调用 GetDlgItemTextA 函数。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHibkA7yN8Iu8V8GgwRriczhopCyMZhib7E2fIwkRHWwKibNtN8koIXaKKfQ/640?wx_fmt=png)

我们先按下 F2 将断点去掉，再按下 F9 执行代码，可以看到 “序列号错误，再来一次！” 的弹框。从而证明我们刚才的断点是有效果的。

> GetDlgItemTextA 的四个参数：对话框句柄，控件标识（ID 号），缓冲区指针，缓冲区最大字符数，参考 Win32.API 手册。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHxSruLf5Iwib9bVzDBwt1lBpiamdskyTCA73VgsPP00RZLXicpfo8fc5ZQ/640?wx_fmt=png)

接着我们再勾选 “GetDlgItemTextA” 函数，再点击 “Check” 按钮，它会继续定位到 0x75CA4390 位置，如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHoiav8KJ1ZmTdamfl2bIuHEtNeOVbQb030pr7AtbdKNdulqqrkQ7TEfA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHibkA7yN8Iu8V8GgwRriczhopCyMZhib7E2fIwkRHWwKibNtN8koIXaKKfQ/640?wx_fmt=png)

第四步，接着按下 Ctrl+F9 执行到返回位置。  
此时显示地址 0x75CA43C1。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHLMNXonf8k3uv5UicGxd63rGteNcuxau3ZxLVB8okVe1ygcUhB6cq9Tg/640?wx_fmt=png)

第五步，再按下 F8 键执行返回  
此时我们看到了 GetDlgItemTexeA 函数执行的位置，它会返回调用函数的下一行代码，注意是下一行。我们程序是有两个对话框值，所以会有两个 GetDlgItemTexeA 函数的调用。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHEG3xDuae5t1zZaVRuVxFfybObTCXIQib8SHtVUwHv5viccBXQBlKYeOg/640?wx_fmt=png)

接着我们继续按 F8 往下走，这两个值获取完成，接下来应该会是计算序列的过程，再进行判断是否正确。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHcb2hcWVKWoTxx1H36116TazMbxLxjaa9pjNgl3gGoTXQBr4s8yickTA/640?wx_fmt=png)

继续往下走，来到 0x004011E4 位置，我们可以看到右上角 EDX 和 EAX 的值就是我们输入的 “eastmount” 和“123456”。同时，右下角显示两个值都已经压到栈里面了。

*   EAX：123456
    
*   EDX：eastmount
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHGGDFicvwxXicbZdSOy41YujGAOUPPAdhibdaIolonhFH08VmZ8V7mJdxg/640?wx_fmt=png)

第六步，访问 TraceMe.00401340 函数  
我们可以猜测调用的 “call TraceMe.00401340” 函数是做判断，并添加如下注释。但也可能不是，我们在进行软件逆向分析或爆破时，通常需要依靠逻辑能力和编程能力来推测。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibH9lXuKGUYNltGiaChJKAdfCXos8zuS6BjHL1tJRN7ia9Whib8BzkFxiauHw/640?wx_fmt=png)

按下 F7 进入该程序，位置 0x00401340。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHAx4Uv0UzCWL4OB9UicRhYo87lDxKO981fv04VZEeliaoGRVe93OiaIacg/640?wx_fmt=png)

再按 F8 执行，可以发现这里存在一个循环，判断输入的值是否与它原始的值一致。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHDtIPuEMLEOWVENnJTxL1xdWuCL6dF3Hq2JLpBND013dCYGNEMROWaQ/640?wx_fmt=png)

循环完之后，继续执行可以看到一些序列号 “123456” 的判断信息。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHEv9ghf0hibUhZ8JvFFJYzMYbeQ7wWYluCQHGGfdQN9CamoiaxvXOITqg/640?wx_fmt=png)

最终它会返回一个值放到 EAX 中，该值等于 0，然后继续执行返回该值。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibH29NXibyv63qL9ppY7EDlMjZK7QxPWxFDYtajQA7LLdr4SYPZSSxzVVA/640?wx_fmt=png)

返回值就是 0，然后继续执行。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHUM0BlCN3w7tqXTyDPcjhyOe3S59pZSlcWX01PMWUibp7gbTZTPN8FJQ/640?wx_fmt=png)

第七步，跳转函数分析  
如果这个函数就是判断函数的话，那么下面这个跳转很可能就是关键跳转。就是我们需要修改的跳转，利用其来进行爆破。位置：0x004011F5

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHgAJpxFUlz1sTdIrhpyWCpuTgqccHvdd5LUcrvx78bnxrsibZnxk1mVg/640?wx_fmt=png)

增加断点，接着按 F8 继续运行。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHO8WOeTia9EofHJxPuOhXXWEU2qaqnX9E1rblenY61zfrpwmibiacRbOoQ/640?wx_fmt=png)

发现其直接跳转至 0x0040122E，然后提示 “序列号错误，再来一次！”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHKctLMB8Wicdv5bfWGkibUknibQ8cshf0zlQ326s67D9tjHaQnIc6QwovQ/640?wx_fmt=png)

再按下 F9 运行，后面果然弹出错误对话框，从而确定上面为关键跳转。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHNq1AaiaBibrc5QyAn8lTJtiawtuLgaxEiaOYricbC7kwrBBXADsxb9GEyicg/640?wx_fmt=png)

第八步，按下 Ctrl+F2 重新运行程序  
接着按 F9 执行程序，在弹出的对话框中输入内容，点击 “check”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHkOic2ibMqBQwN2QZbDKyxSPnVJHv2IxW15mspHdUPL7BW08wcNPyDfzQ/640?wx_fmt=png)

继续按下 F9 运行程序跳转到我们刚刚下断点的 “关键跳转” 位置。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHJUL5IxGOyoInCWBCkwrODibTwFHTjhOrbeVa7A3MPf3o47iaeMtMhmaw/640?wx_fmt=png)

关键步骤：修改汇编代码，JE 是实现跳转，修改为 JNZ 不跳转。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHB7ZicBrsC1tb6gicro92tkVpibPA8pgQ5taJHmW0ibLLPL38qJEoSIYxNA/640?wx_fmt=png)

继续按 F8 执行，或者直接按下 F9，可以提示 “恭喜你，成功” 的对话框。这就是爆破的基本流程。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHK53uoF0SibaDLiawTj7BaH6P6VsnyE7oHWzswqibU2WZJQSMklW1iatYCA/640?wx_fmt=png)

第九步，保存爆破软件  
选择修改的几行内容，然后右键鼠标，点击 “复制到可执行文件”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHFVNzVzdl9Gmwu7P931FicGEd3jefTOcnM0LqVVm4BW3iajGjZD691IicQ/640?wx_fmt=png)

选择 “TraceMe.exe” 文件右键保存文件，如“TraceMe_PO2.exe”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHm7d30ZLvT9V21s73TIwIUPaSYXTDpTFiayicX0lnP93awBuBBibfbZaGw/640?wx_fmt=png)

保存成功后，随便输入用户名和序列号，都提示成功！

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHIT4q6ibNrHGQvIuknfOTmza5vR4XbTNP5QvJZLyk1JKicns9CWY95fOA/640?wx_fmt=png)

同时，该程序输入长度还有一个判断，我们也可以尝试进行爆破。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDRML1ggoAWrXbpJAIZV9ibOibHvHZmW8a2ZFJq1G1GVsTd3YXEtgcQibJkPcQq0SbmRx8lAY4iaqsqHQWg/640?wx_fmt=png)

但其原理是什么呢？后续的文章我们会继续介绍。

四. 总结
=====

写到这里，这篇文章就介绍完毕，希望您喜欢~

*   OllyDbg 界面介绍和配置
    
*   常用快捷键
    
*   OllyDbg 动态爆破软件演示
    

这篇文章中如果存在一些不足，还请海涵。作者作为网络安全初学者的慢慢成长路吧！希望未来能更透彻撰写相关文章。同时非常感谢参考文献中的安全大佬们的文章分享，感谢师傅、师兄师弟、师姐师妹们的教导，深知自己很菜，得努力前行。

前文回顾（下面的超链接可以点击喔）：

*   [[系统安全] 一. 什么是逆向分析、逆向分析应用及经典扫雷游戏逆向](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484670&idx=1&sn=c31b15b73f27a7ce44ae1350e7f708a2&chksm=cfccb433f8bb3d25c25f044caac29d358fe686602011d8e4cbdc504e3a587e756215ce051819&scene=21#wechat_redirect)
    
*   [[系统安全] 二. 如何学好逆向分析及吕布传游戏逆向案例](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484756&idx=1&sn=ef95ff95474c51fa2bd4b9b4847ebb54&chksm=cfccb599f8bb3c8fa4852416cff6695fc8dcc9aadb3295c7249c12c03cad4c146a93e6250d56&scene=21#wechat_redirect)
    
*   [[系统安全] 三. IDA Pro 反汇编工具初识及逆向工程解密实战](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484812&idx=1&sn=9b77853a5b9da0f7a688e592dba3ddba&chksm=cfccb541f8bb3c57faffc7661a452238debe09cc7a57ae2d9e9d835d6520ee441bfd9d5ad119&scene=21#wechat_redirect)
    
*   [[系统安全] 四. OllyDbg 动态分析工具基础用法及 Crakeme 逆向破解](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484950&idx=1&sn=07d8f0b20f599586ef06035354b14630&chksm=cfccb6dbf8bb3fcd6d2efcc7b6757fabd8015d86f43e3bc8ae6cb9367d19492aec881374fca2&scene=21#wechat_redirect)
    
*   [[系统安全] 五. OllyDbg 和 Cheat Engine 工具逆向分析植物大战僵尸游戏](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485043&idx=1&sn=028c702990f722d087c6c349fb34f5fb&chksm=cfccb6bef8bb3fa8882994f7412db6b769d382abbafa6b5b3bd1b5ae62dffa20e81c7170ecb4&scene=21#wechat_redirect)
    
*   [[系统安全] 六. 逆向分析之条件语句和循环语句源码还原及流程控制](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485936&idx=1&sn=b1c282021280bb24646a9bf7c0f1fa6a&chksm=cfccb93df8bb302b51ae1026dba4f8839a1c68690df0e8da3242e9c1ead0182bf6c34dd44ada&scene=21#wechat_redirect)
    
*   [[系统安全] 七. 逆向分析之 PE 病毒原理、C++ 实现文件加解密及 OllyDbg 逆向](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485996&idx=1&sn=d5e323f16ce0b3d88c678a1fc1848596&chksm=cfccbae1f8bb33f7fad687d17ba7c10312bf2d756e460217a5d60ef2af0c012336292918128d&scene=21#wechat_redirect)
    
*   [[系统安全] 八. Windows 漏洞利用之 CVE-2019-0708 复现及蓝屏攻击](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486024&idx=1&sn=102ace20c2b15f4e7a9f910b56b84aec&chksm=cfccba85f8bb33939ac7e99cae23d1b6da5a0db4e6ff8bc7535a77a46a4204855de41aa446dd&scene=21#wechat_redirect)
    
*   [[系统安全] 九. Windows 漏洞利用之 MS08-067 远程代码执行漏洞复现及深度提权](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486057&idx=1&sn=7e7899b9285ac04f0d9745b4c455b005&chksm=cfccbaa4f8bb33b25ffcd780764ad86dc63edc7dd56d09e466254f6277851b5a4a545bb209a4&scene=21#wechat_redirect)
    
*   [[系统安全] 十. Windows 漏洞利用之 SMBv3 服务远程代码执行漏洞（CVE-2020-0796）复现](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486111&idx=1&sn=e2129fc8efa79d2356c3a2deec6d52a1&chksm=cfccba52f8bb3344479fa8d201494f88ac1b0cee3e0786797dd09a17c5f4aa4a5627fd0afef0&scene=21#wechat_redirect)
    
*   [[系统安全] 十一. 那些年的熊猫烧香及 PE 病毒行为机理分析](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486188&idx=1&sn=34a1d3f2d6880dfd60917b84d3efaa5a&chksm=cfccba21f8bb3337b45cc0fb98af3ab6a1333219fe2a06d3c3c8e38b996e1039e5b0f8d14f24&scene=21#wechat_redirect)
    
*   [[系统安全] 十二. 熊猫烧香病毒 IDA 和 OD 逆向分析（上）病毒初始化](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486260&idx=1&sn=0760360d286782209e9f93d37c177c73&chksm=cfccbbf9f8bb32ef5e54058ded6072a248e3156be64213a238b47b5fa65b6909889ab0c9b7c5&scene=21#wechat_redirect)
    
*   [[系统安全] 十三. 熊猫烧香病毒 IDA 和 OD 逆向分析（中）病毒释放机理](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486423&idx=1&sn=43f77342f8900b481eaa536b9e81f737&chksm=cfccbb1af8bb320ccc6f1bd93e358b916ccb6313f9bbdcf1d9c31deebf16a2e643ce0e121113&scene=21#wechat_redirect)
    
*   [[系统安全] 十四. 熊猫烧香病毒 IDA 和 OD 逆向分析（下）病毒感染配置](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486580&idx=1&sn=20b672097bf0be1fbdf5952bb53b23a6&chksm=cfccbcb9f8bb35affbc611fc92875f9250060914d94fa1d9a7c2b9e9482fd4a50bbb33ebc42f&scene=21#wechat_redirect)
    
*   [[系统安全] 十五. Chrome 密码保存功能渗透解析、Chrome 蓝屏漏洞及音乐软件漏洞复现](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486662&idx=1&sn=6506a733804564137d40c7c070287590&chksm=cfccbc0bf8bb351d1a82737e5dc310c048f80fb5fcfe3317c7bc1b38ac6b52de60923cb92ba7&scene=21#wechat_redirect)
    
*   [[系统安全] 十六. PE 文件逆向基础知识 (PE 解析、PE 编辑工具和 PE 修改)](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247486866&idx=1&sn=cd3bc433c0a6a7b1f8bcaa4295cf65ae&chksm=cfccbd5ff8bb34496b9dc20b2fd304ce1d1194fd076902127a6817362b3c52afc056126ca0ba&scene=21#wechat_redirect)
    
*   [[系统安全] 十七. Windows PE 病毒概念、分类及感染方式详解](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247487219&idx=1&sn=1e123c330cb0499400d5529cbd5f47f3&chksm=cfccbe3ef8bb3728118a0aab982a56b3ea66f320a221c6a318263104a35f5aee8d3545612683&scene=21#wechat_redirect)
    
*   [[系统安全] 十八. 病毒攻防机理及 WinRAR 恶意劫持漏洞 (bat 病毒、自启动、蓝屏攻击)](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247487311&idx=1&sn=95211524641975c5a5093f07df5e6ab2&chksm=cfccbf82f8bb36940f26a26bd8ed5870088823a9a97ccd81e699ed82aca3f579231c9b3e987e&scene=21#wechat_redirect)
    
*   [[系统安全] 十九. 宏病毒之入门基础、防御措施、自发邮件及 APT28 宏样本分析](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247487459&idx=1&sn=87d6296402fdb71f5dbb5a42f9bb6597&chksm=cfccbf2ef8bb363893337b31e8985361624280b90ee6ca65c2da67916fc78ba66f059a24e589&scene=21#wechat_redirect)
    
*   [[系统安全] 二十. PE 数字签名之 (上) 什么是数字签名及 Signtool 签名工具详解](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247487583&idx=1&sn=80203f44662f8e3902779c81669f33d5&chksm=cfcca092f8bb29844911039ef76fe74f5d746518fa8b617c704ea4f59534ea520521b1b3e673&scene=21#wechat_redirect)
    
*   [[系统安全] 二十一. PE 数字签名之 (中)Signcode、PEView、010Editor、Asn1View 工具用法](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247487960&idx=1&sn=02296bc6cdabb7ffba9acf1c6a922fc0&chksm=cfcca115f8bb2803860941471cc999b5d9c42401daa51ebf0b14c09d914f4c5b23d26d565182&scene=21#wechat_redirect)
    
*   [[系统安全] 二十二. PE 数字签名之 (下) 微软证书漏洞 CVE-2020-0601 复现及 Windows 验证机制分析](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488157&idx=1&sn=a1c920ff7151debc50f23f15b3c28c4e&chksm=cfcca250f8bb2b4604700ffa5ca4d89f3210a9522ea35a6a45f528f14f5bfde269cc51600fa8&scene=21#wechat_redirect)
    
*   [系统安全] 二十三. 逆向分析之 OllyDbg 动态调试复习及 TraceMe 案例分析  
    

2020 年 8 月 18 新开的 “娜璋 AI 安全之家”，主要围绕 Python 大数据分析、网络空间安全、人工智能、Web 渗透及攻防技术进行讲解，同时分享 CCF、SCI、南核北核论文的算法实现。娜璋之家会更加系统，并重构作者的所有文章，从零讲解 Python 和安全，写了近十年文章，真心想把自己所学所感所做分享出来，还请各位多多指教，真诚邀请您的关注！谢谢。2021 年继续加油！

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZePZ27y7oibNu4BGibRAq4HydK4JWeQXtQMKibpFEkxNKClkDoicWRC06FHBp99ePyoKPGkOdPDezhg/640?wx_fmt=png)

(By:Eastmount 2021-03-02 周二夜于武汉）

参考资料：

*   [1] 动态调试工具之 OllyDbg(OD) 教程 - B 站 yxfzedu
    
*   [2] [逆向笔记] OD 工具使用 - 逆向 TraceMe.exe- 17bdw 随手笔记
    
*   [3]《加密与解密》段钢等著
    
*   [4]《OllyDBG 入门教程》看雪学院 - CCDebuger
    
*   [5] 160 个 Crackme006 - 鬼手 56 大佬