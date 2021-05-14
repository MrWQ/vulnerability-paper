> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/5I1YvCfU-pkZkSAvWw71Cw)

**前言**

IATHOOK 局限性较大, 当我们想 HOOK 一个普通函数, 并不是 API, 或者 IAT 表里并没有这个 API 函数 (有可能他自己 LoadLibrary, 自己加载的), 那我们根本就从导入表中找不到这个函数, 自然也就在 IAT 表中无法找到, InlineHook 算是对 IATHOOK 一个升级版吧

**大体思路**

用 JMP 改变函数入口, JMP 到我们自己的函数, 然后又 JMP 回去执行刚刚的没执行完的函数。

过程无论怎么变, 一定要让堆栈平衡和保留原来的寄存器, 这是 Hook 是否成功的关键.

**具体实现**

**创建钩子**

```
 DWORD SetInlineHook(LPBYTE HookAddr,LPVOID HookProc,DWORD num)  //要挂钩子的地址,钩子函数(如何处理),要改多少个的硬编码
 {
     if (HookAddr == NULL || HookProc == NULL)
     {
         printf("地址填错了");
         return 0;
     }
     if (num < 5)
     {
         printf("HOOK不了");
         return 0;
     }
     //改变修改地址为可写属性
     DWORD OldProtect = 0;
     DWORD bret = VirtualProtect((LPBYTE)HookAddr,num, PAGE_EXECUTE_READWRITE,&OldProtect);
     if (bret == 0)
     {
         printf("修改可写属性失败");
         return 0;
     }
     Buffer = malloc(num * sizeof(char));

     memcpy(Buffer, HookAddr, num);  //存起来把原来的值

     memset(HookAddr,0x90,num);   //先全部nop
     //计算跳到我们自己函数的硬编码,E9后面的值 = 要跳转的地址 - E9的地址 - 5
     DWORD JmpAddr = (DWORD)HookProc - (DWORD)HookAddr - 5;

     *(LPBYTE)HookAddr = 0xE9;
     *(PDWORD)((LPBYTE)HookAddr + 1) = JmpAddr;

     GlobleHookAddr = (DWORD)HookAddr;
     RetGlobleHookAddr = (DWORD)HookAddr + num;  //等会的返回地址
     dw_ifHOOK = 1;
 }
```

这里别忘了改属性, 然后就是有个公式, JMP 后面的值并不是我们真正想要去的地址

E9 后面的值 = 要跳转的地址 - E9 的地址 - 5, 这里要算一下.

**卸载钩子**

```
 DWORD UnInlineHook(DWORD num)
 {
     if (!dw_ifHOOK)
     {
         printf("还没hook呢");
         return 0;
     }
     memcpy((LPVOID)GlobleHookAddr, Buffer, num);

     Buffer = NULL;
     dw_ifHOOK = 0;
     return 1;
 }
```

这里把我们在创建钩子的时候定义的全局变量 Buffer 的值重新写回来就行了

**钩子函数**

```
 extern "C" _declspec(naked) void HookProc()   //裸函数,编译器不帮我们平衡堆栈
 {
     //先把现场保留了
     _asm
     {
         pushad    //保留寄存器
         pushfd   //保留标志寄存器
     }
     _asm
     {
         mov reg.EAX, eax
         mov reg.EBX, ebx
         mov reg.ECX, ecx
         mov reg.EDX, edx
         mov reg.EDI, edi
         mov reg.ESI, esi
         mov reg.ESP, esp
         mov reg.EBP, ebp
     }
     _asm
     {
         mov eax, DWORD PTR ss : [esp + 0x28]
         mov x, eax
         mov eax, DWORD PTR ss : [esp + 0x2c]
         mov y, eax
         mov eax, DWORD PTR ss : [esp + 0x30]
         mov z, eax

     }
     printf("EAX:%x EBX:%x ECX:%x EDX:%x EDI:%x ESI:%x ESP:%x EBP:%x \n", reg.EAX, reg.EBX, reg.ECX, reg.EDX, reg.EDI, reg.ESI, reg.ESP, reg.EBP);

     printf("参数:%d %d %d\n", x, y, z);

     _asm
     {
         popfd
         popad
     }

     _asm
     {
         push        ebp
         mov         ebp, esp
         sub         esp, 0C0h
     }

     _asm
     {
         jmp RetGlobleHookAddr;
     }
 }
```

上来先把寄存器的值保存下来, 后面我们要还原现场. 这里我先创建了一个结构体用于接收寄存器的值, 等会方便打印

```
typedef struct _regeist
{
DWORD EAX;
DWORD EBX;
DWORD ECX;
DWORD EDX;
DWORD EBP;
DWORD ESP;
DWORD ESI;
DWORD EDI;
}regeist;
regeist reg = { 0 };
```

然后第 22~28 行的值由于 pushad 和 pushfd 了, 偏移不能是 + 4 +8 +c 了, 这里要算一下, 40~45 行, 我们将原来没执行的代码执行一下, 不然堆栈出问题了, 最后跳转到原函数的下一个位置, 继续执行原函数

**被 HOOK 的函数**

```
DWORD Test(int x, int y, int z)
{
return x + y + z;
}
```

**测试**

```
 DWORD TestInlineHook()
 {
     PAddr = (BYTE*)Test + 1;
     PAddr += *(DWORD*)PAddr+ 4;

     SetInlineHook((LPBYTE)Test, HookProc,9);

     Test(1, 2, 3);

     UnInlineHook(9);

     Test(1, 2, 3);
     return 0;
 }
```

这里有一个小的细节, 我们用函数名 Test 传参的话, 传进去的这个参数的值并不是真正的函数地址, 而是一个间接地址, 间接地址里面的值是 JMP 到真正的函数地址。也就是我们平时看反汇编时, 如果我们 F11 一个 CALL 我们会发现他先到一个地址, 然后再 F11, 才会到真正的函数地址。用函数名传参的话得到的并不是真正的函数地址, 但其实也是个间接地址嘛, JMP + 真正函数地址经过运算后的地址, 我们还是用 “E9 后面的值 = 要跳转的地址 - E9 的地址 - 5” 这个公式算一下。

这里我找到一篇文章说明为什么有这种机制:

https://blog.csdn.net/x_iya/article/details/13161937

**测试结果**

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibdFdCbzWE5J6QgjegMbEGsd07Pk6QKIj4OsBLfnBRnWg2YdDGnCbedWEGfd12rGD0jYr17DibIbfA/640?wx_fmt=png)

 我调用了两次函数，但只有一次输出说明卸载也成功了

**完整代码**

```
// InlineHook.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//


#include <iostream>
#include <windows.h>


//保留原来的硬编码
LPVOID Buffer;
typedef struct _regeist
{
DWORD EAX;
DWORD EBX;
DWORD ECX;
DWORD EDX;
DWORD EBP;
DWORD ESP;
DWORD ESI;
DWORD EDI;
}regeist;
regeist reg = { 0 };
DWORD x;
DWORD y;
DWORD z;
DWORD GlobleHookAddr;
DWORD RetGlobleHookAddr;
DWORD dw_ifHOOK = 0;
DWORD Test(int x, int y, int z);
PBYTE PAddr;
//typedef DWORD(*MyTest)(int x, int y, int z);
//MyTest pAddr =Test;
extern "C" _declspec(naked) void HookProc()   //裸函数,编译器不帮我们平衡堆栈
{
//先把现场保留了
_asm
{
pushad    //保留寄存器
pushfd   //保留标志寄存器
}
_asm
{
mov reg.EAX, eax
mov reg.EBX, ebx
mov reg.ECX, ecx
mov reg.EDX, edx
mov reg.EDI, edi
mov reg.ESI, esi
mov reg.ESP, esp
mov reg.EBP, ebp
}
_asm
{
mov eax, DWORD PTR ss : [esp + 0x28]
mov x, eax
mov eax, DWORD PTR ss : [esp + 0x2c]
mov y, eax
mov eax, DWORD PTR ss : [esp + 0x30]
mov z, eax


}
printf("EAX:%x EBX:%x ECX:%x EDX:%x EDI:%x ESI:%x ESP:%x EBP:%x \n", reg.EAX, reg.EBX, reg.ECX, reg.EDX, reg.EDI, reg.ESI, reg.ESP, reg.EBP);


printf("参数:%d %d %d\n", x, y, z);


_asm
{
popfd
popad
}


_asm
{
push        ebp
mov         ebp, esp
sub         esp, 0C0h
}


_asm
{
jmp RetGlobleHookAddr;
}
}
DWORD SetInlineHook(LPBYTE HookAddr,LPVOID HookProc,DWORD num)  //要挂钩子的地址,钩子函数(如何处理),要改多少个的硬编码
{
if (HookAddr == NULL || HookProc == NULL)
{
printf("地址填错了");
return 0;
}
if (num < 5)
{
printf("HOOK不了");
return 0;
}
//改变修改地址为可写属性
DWORD OldProtect = 0;
DWORD bret = VirtualProtect((LPBYTE)HookAddr,num, PAGE_EXECUTE_READWRITE,&OldProtect);
if (bret == 0)
{
printf("修改可写属性失败");
return 0;
}
Buffer = malloc(num * sizeof(char));


memcpy(Buffer, HookAddr, num);


memset(HookAddr,0x90,num);   //先全部nop
//计算跳到我们自己函数的硬编码,这里用E8方便平衡堆栈,E8后面的值 = 要跳转的地址 - E8的地址 - 5
DWORD JmpAddr = (DWORD)HookProc - (DWORD)HookAddr - 5;


*(LPBYTE)HookAddr = 0xE9;
*(PDWORD)((LPBYTE)HookAddr + 1) = JmpAddr;


GlobleHookAddr = (DWORD)HookAddr;
RetGlobleHookAddr = (DWORD)HookAddr + num;
dw_ifHOOK = 1;
}


DWORD UnInlineHook(DWORD num)
{
if (!dw_ifHOOK)
{
printf("还没hook呢");
return 0;
}
memcpy((LPVOID)GlobleHookAddr, Buffer, num);


Buffer = NULL;
dw_ifHOOK = 0;
return 1;
}
DWORD Test(int x, int y, int z)
{
return x + y + z;
}
DWORD TestInlineHook()
{
PAddr = (BYTE*)Test + 1;
PAddr += *(DWORD*)PAddr + 4;


SetInlineHook((LPBYTE)PAddr, HookProc,9);


Test(1, 2, 3);


UnInlineHook(9);


Test(1, 2, 3);
return 0;
}
int main()
{


TestInlineHook();
//Test(1, 2, 3);
return 1;
}
```

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

**推荐阅读：**

**[远程线程注入 Dll，突破 Session 0](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247496299&idx=1&sn=a3c3ac02810b31b728648cb52f8601d5&chksm=ec1ca754db6b2e423418323353e2e00a85c8cb2c261dd407e6fa2587c6f657680c0b5c909901&scene=21#wechat_redirect)  
**

[**红队 | IAT Hook 技术实现**](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247496403&idx=1&sn=4d8d1d67425a5a7c9a2ee2a303aa0573&chksm=ec1ca7ecdb6b2efa9db86310c85ecdf83130a7d99754c80ed79d409ff57713076d95b74ef478&scene=21#wechat_redirect)  

本月报名可以参加抽奖送暗夜精灵 6Pro 笔记本电脑的优惠活动

[![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibHHibNbEpsAMia19jkGuuz9tTIfiauo7fjdWicOTGhPibiat3Kt90m1icJc9VoX8KbdFsB6plzmBCTjGDibQ/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247496352&idx=1&sn=df6ddbf35ac56259299ce37681d56e5b&chksm=ec1ca79fdb6b2e8946f91d54722a7abb04f83111f9d348090167b804bc63b40d3efeb9beabbe&scene=21#wechat_redirect)

**点赞，转发，在看**

原创投稿作者：Buffer

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)