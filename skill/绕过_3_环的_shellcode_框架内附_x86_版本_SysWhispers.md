> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/1Ozh-u-2dDQyuXSptpjifg)

绕过 3 环的 shellcode 框架内附 x86 版本 SysWhispers

1

概述

之前分析 CS4 的 stage 时，有老哥让我写下 CS 免杀上线方面知识，遂介绍之前所写 shellcode 框架，该框架的 shellcode 执行部分利用系统特性和直接系统调用（Direct System Call）执行，得以免杀主流杀软（火绒、360 全部产品、毒霸等）, 该方式也是主流绕过 3 环 AV、EDR、沙箱的常用手段。Ps: 感谢邪八 Moriarty 的分享课。

2

简要介绍

该框架主要由四个项目组成：

GenerateShellCode：负责生成相关功能的 shellcode。

EncryptShellCode：负责以 AES128 加密所将执行的 shellcode。 

FunctionHash：负责计算 shell 中所用到函数的 hash 值。 

XShellCodeLoader：负责执行加密后的 shellcode。

**2.1 GenerateShellCode**

写 shellcode 有几个原则：不能有全局变量、不能调用系统函数、不能嵌套调用函数。下面以简单弹窗 messagebox 生成的 shellcode 作介绍，先看定义的入口函数 MyEntry()，里面定义了 GetProcAddr()、LoadLibaryA() 和 MessageBoxA() 三个函数对应的 hash，然后通过 MyGetProcAddress() 传入 hash 值和 kernel32 基址返回相关函数地址再进行调用。

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujpicww4QpEUOGyLUXnmgicNoT90b66T7NWbZtRu4O8bdqKphl9cqrWvAg/640?wx_fmt=png)

自定义函数入口需在项目属性 -> 链接器 -> 入口点中进行设置：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujWbchCJQDwWq1iaiawT2hF0LttBCicBJ2Eb4VXicKAeu1SKuvE8ialM1J4Pw/640?wx_fmt=png)

通过 GetKernel32Base() 函数获得 kernel32 基址：作比较：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujcN33Ph9xZcrwxFQiaaAsNlN8zuns8YtDnl8icOEHDDcYUh1BhliaeicTQg/640?wx_fmt=png)

通过 MyGetProcAddress() 函数传入 hash 值找出对应的函数名，函数内容就是解析 kernel32 的导出表，遍历每个函数并计算出相应 hash 并与传入的 hash 作比较：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujWbicfC63ytaBNP81zfm9HV03gKXrwgTojEBBibicttkTjLan2jDLcibHgg/640?wx_fmt=png)

GetProcHash() 把函数名转为相应的 hash:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujtvny9PBoz7byhyN59NmwH2iag4iaZ1HTEEiaaRKjrUojYyAInuerluklQ/640?wx_fmt=png)

Release x86 模式生成后 exe 程序后，010editor 打开找到. text 代码段，将其抠出后得到 shellcode：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujAP6WENnrakRFFXlWEmY3SicW9KYoicBzr8KUGoEhBlPRefhBEFUHztsQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujFK6U3fzo3kZmrcdepBD6WgbNiahsdiabibV2M0x212MJS2HFg78eDmmJQ/640?wx_fmt=png)

**2.2、EncryptShellCode** 

首先打开已经抠出的 shellcode 文件，并将器读入内存：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujaRNE5siaa5hl8qagNmMpeXFADxIyRHTic0hjQGKFricG39tEmqbQA4P8w/640?wx_fmt=png)

AES 循环加密 0x10 个字节 AES 加密的实现是 WjCryptLib_Aes 开源项目:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujeEG1564FhzKGZxkkoFgCyRduicYoOIfl26DdzrEdX69o7sColJaBpAA/640?wx_fmt=png)

加密后保存到新文件：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujEiap0NuBpYdibK4CAa4CEV6sBvRXmjbr5CZVibY6iatMs4ANUu0QDjfzEw/640?wx_fmt=png)

**2.3、FunctionHash**

这个比较简单，计算所需要用到函数的 hash 值：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujYcrUZhDgcVkEbGl5jL5YibFZONPlibc1vSFo9RPGvQxaKb2yAxYuosCQ/640?wx_fmt=png)

**2.4、XShellCodeLoader**

下面着重介绍下 shellcode 的执行实现，因为 x86、x64 进 0 环进 3 环的方式不同，在这里简单介绍下不同版本 3 环进 0 环的方式：

一、32 位的程序在 32 位系统上运行有两种方式进 0 环，第一个是中断门 int 02Eh，第二种是 sysenter

二、32 位的程序在 64 位系统上运行，通过 FastSystemCall 进 0 环

三、64 位的程序在 64 位系统上运行，通过 syscall 进 0 环

这里用 vs 的 Release x86 来进行编译，所生成的 32 位 exe 程序在 32 位系统运行使用 sysenter 进 0 环，在 64 位系统则使用 FastSystemCall 进 0 环。

下面我们先以 32 位程序运行在 32 位系统的 sysenter 进行讲解：

首先自定义一个区段，该区段的属性最好只为 read，一定不要 read、write、execute 全上，这种全属性在内存中会显得很可疑，区段名最好为系统常用的而这个程序又没用到的，如. edata，因为 360 杀毒可能会对不常见的区段名报毒，另外不建议使用 #pragma section(".edata",read,execute,nopage) 该方式定义区段名，因为该方式生成的区段会出现在程序中所有区段的最前面，360 杀毒报毒，特征较明显。使用以下方式去定义区段，区段的内容为已 AES 加密的 shellcode：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujnXLuC4IYLuEfQrqxLUbS2gOkCcxABoWaJapd6OBvtMbcpYyYxiaFKAw/640?wx_fmt=png)

然后通过遍历自身程序的区段查找出自定义的区段：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3uj6xFzTSnammnwS7P7c6LSsd4UBQ3GlWoWFNWDrTx9ibMTXAgwG8g6B7A/640?wx_fmt=png)

接着调用 NtProtectVirtualMemory() 修改自定义区段的属性为可读可写，即 readwrite，

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujdfoST7kIYTHjxBlgSTdue3WUPeGiawciczCrTnfiajpoiazNFsickBfGhVQ/640?wx_fmt=png)

而 NtProtectVirtualMemory() 是由汇编所写的直接系统调用：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujY3uaVoH2PPc9KFrWiaPSNKw8tur3P3GuLtuODL6fVWsHDdeThfpNS6g/640?wx_fmt=png)

解析上述汇编，首先把 001911B13h 这个对应 NtProtectVirtualMemory 函数名的 hash 值压栈，然后调用 SW2_GetSyscallNumber 函数（后面解析 syswhier 框架时会提及），该函数会返回 NtProtectVirtualMemory 对应的系统调用号，mov ecx，5h 是把函数个数赋值给 ecx，再把 NtProtectVirtualMemory() 函数所传入的参数相继压栈，然后调用 sysenter。

接着循环把自定义区段解密出来：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujNpNiagJRZP5CaJ3wx3sYPCr6RpOfBdiaUhxmsvG5mzot5hKqI525DxdQ/640?wx_fmt=png)

把自定义区段的属性还原到 read、execute：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujhydD6Yw4icIvZNJp5khLtXIKm57ic1X0MibRoHiaZGXktgibTVnzCfHpMbw/640?wx_fmt=png)

执行 shellcode：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujAS1wTRibUZtv59Zu38AwruXcBAQ4oFibQlFzpgNpcpYPbcTnnNwVNWww/640?wx_fmt=png)

再来看看 32 位程序运行在 64 位系统的 KiFastSystemCall，其主要区别只在于汇编部分：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3uj8gWxoXGVQx6E4RyE56ZFBbJO5xBq9zLB54D53V91Eq4AUxiaDIQRV4Q/640?wx_fmt=png)

Call internal_cleancall_wow64_gate,

internal_cleancall_wow64_gate 的值为__readfsdword(0xC0)，即 FS[0xC0]  WOW32Reserved

3

执行效果

**3.1、实验环境：**

Team server: Kali 2020 ip: 192.168.202.131

控制端：win7 32 位 ip:192.168.202.134

受控端 1：win 7 32 位 ip: 192.168.202.140

受控端 2：win10 1907 位 ip: 192.168.202.1

**3.2、32 位系统执行**

火绒版本号：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujCTTROMVicPD8x8CrCKVU9wLse65CicxcH4KbslEvANeyVo5bFOVhM3dw/640?wx_fmt=png)

静态查杀，未发现风险：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujicl9bnibS8s3OmnKTn9g5VbYUKbdhnWVvv8WJSOSAOolhouziaE35aialA/640?wx_fmt=png)

360 安全管家及 360 杀毒版本号：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3uj1XH4iak2TmnTic9YaibK8aBtzCAOMibUoiaolDl6V0yLCJpN57hz0dQb1vQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujMuDWwTvphA3OqrOBibsC4zibHITWaCgcnrOt087yiaicMZbMib9Uq8ptrWg/640?wx_fmt=png)

静态查杀，未发现风险：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujCMGZM6oib2DYBoR3qMYpMXiccqEgyyUcJmuDuIIzAmxddHYib9ia2B5yIA/640?wx_fmt=png)

执行均未拦截，运行上线：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujIYDMIKssia65H40eUMv7TSbgpbH5AmaPugib2XQibPnzibZbLGqtia9A8ew/640?wx_fmt=png)

卡巴斯基，静态扫描未发现风险：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujLyvIwj8doSApV3n17zZnvkZUUFicYLt7Y1o4Pg5Osjj2IfOreHiaKbVw/640?wx_fmt=png)

执行时则被查杀：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujGR1GrbJvePib9AphBz2PSAPtDJkY6c5iaUFvwRyduIZMc7qtB4IjDjyw/640?wx_fmt=png)

原因是 stage 执行下载后的 Beacon.dll 在内存中反射调用时被卡巴斯基规则检测到，也有相应的解决办法，等下篇文章魔改 cobalt strike 再来相应解决。

**3.3、64 位系统执行**

同样成功执行并上线（测试过程同上）

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3uj5QqibUnfvboyje4cvBicJuzIePGAlWZqMD2ChoPgrMXjenesS6Z5v2Ag/640?wx_fmt=png)

附上框架项目地址：

https://github.com/mai1zhi2/ShellCodeFramework

4

SysWhispers2 项目简介

该项目较为简单，主要方法有三个：

**一、SW2_HashSyscall()**

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujdOhFOFh3icCwal0iaaR9LiaLKJB6n6HKTZmdDCj0npM2z6n7briaCJhicjQ/640?wx_fmt=png)

该方法是计算传入的函数名的 hash 值。

**二、SW2_PopulateSyscallList()**

该函数中首先找到 ntdll 的基址：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujgwzr3vyLf71YHIFlwMWsVRfQoBISkfnhwRmurYJSmw32Hkic9BXAsLA/640?wx_fmt=png)

遍历 ntdll.dll 的导出函数，并将其函数名对应的 hash 值和函数地址保存在 SW2_SYSCALL_ENTRY 结构体中：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujOsmoiansS3ohB8XYYRvvdiarwrEeExfwletfEyfiaFJQfTibKAuRqklibZg/640?wx_fmt=png)

将 SW2_SYSCALL_ENTRY 的列表按照函数地址进行从小到大冒泡排序：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujicoko2lYnmyI2S1prfvLcuiaTRj2Yn6TYO1fbbQ2GuKCl2RxwRkCFsnQ/640?wx_fmt=png)

**三、SW2_GetSyscallNumber**

该函数传入需要的函数 hash 值，遍历列表，返回对应的序号即系统调用号

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujsglFL2efreRTe1R4gpAHIxwJAIic4VBhD5egtk4VxKGISRWibYvjSBnw/640?wx_fmt=png)

原版只有 64 位程序运行在 64 系统的 syscall，最后附上该项目修改后的 32 位程序运行在 32 位系统的 sysenter 和 32 位程序运行在 64 位系统的 KiFastSystemCall 版本，使用方法均与原版一致：https://github.com/mai1zhi2/SysWhispers2_x86

5

关注公众号

本公众号不定期更新视频和文章 欢迎关注

![](https://mmbiz.qpic.cn/mmbiz_jpg/Jvbbfg0s6AAvPfTRnicopS7fBgLw2r3ujdoic21pWU8ehsqsbggRxTKKwfsnCu8vnaHoaXYPES0iaibD8qzH6KibSaA/640?wx_fmt=jpeg)

  

  

END