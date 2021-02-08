\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/3tGh-tKIw7\_UXL16N-5mrA)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6nMLpJsdx2JaAc4H7HUnBnSuf1pvFO0OuyIxKwdUCOXU4EdrSK9ibboab8Sm9hlE38rj0Ev5oWbEQ/640?wx_fmt=png)

前言

eBPF 是 Linux 内核中的一个模块，主要作用是实现包过滤功能。由于 eBPF 提供了一种从用户面到 Linux 内核的接口，用户编写的 eBPF 程序可以在内核提供的虚拟机中执行，因此 eBPF 也是一个重要的内核提权的攻击面。本文将详细叙述 eBPF 的基本原理和实现方法，对 eBPF 内核提权漏洞 CVE-2020-8835 的 Root Cause 进行详细的分析。通过本文，期望即使对 eBPF 模块不熟悉的同学也能够理解该漏洞的原理。本文会对必要的 eBPF 原理进行介绍但是不会沉溺 eBPF 细节，更主要的是想向大家介绍 eBPF 是一个理想的内核提权攻击面。

eBPF 背景知识

为了能够对 eBPF 安全有个总体的了解，我们既需要对 eBPF 本身的设计以及实现有所了解，同时最好佐以漏洞实例进行分析，从而对 eBPF 这个内核攻击面建立更加具象的理解。

#### **eBPF 程序的基本功能**

linux 官方文档（点击 “阅读原文” 查看链接）对 eBPF 模块有个详细的介绍，可以配合本文进行理解。  
eBPF 是对 BPF 的扩展，BPF 即为 Berkeley Packet Filter，顾名思义这个东西主要是用来对网卡进入的数据包进行过滤和拷贝到用户层的。eBPF 对 BPF 很多功能进行了扩展，可以对更多的数据进行过滤，二者的编码方式有所不同，但是基本原理都一样。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6nMLpJsdx2JaAc4H7HUnBnDGnLicCbib399e2GjVs2XxNISBfYWqTypLXLC3oHfHhdXZ3QQ49GtjEw/640?wx_fmt=png)

eBPF 程序本身包含了一些过滤规则，例如验证包是 IP 包还是 ARP 包。 tcpDump（点击 “阅读原文” 查看链接）这个程序底层就是通过 BPF 实现的包 过滤功能的。  

#### **eBPF 是如何在内核中运行的**

eBPF 程序是使用一种低级的机器语言编写的，类似于汇编指令，例如下面这样

```
BPF\_MOV64\_REG(BPF\_REG\_2, BPF\_REG\_10),
BPF\_ALU64\_IMM(BPF\_ADD, BPF\_REG\_2, -8),
BPF\_LD\_MAP\_FD(BPF\_REG\_1, 0),
BPF\_RAW\_INSN(BPF\_JMP | BPF\_CALL, 0, 0, 0, BPF\_FUNC\_map\_lookup\_elem),
BPF\_EXIT\_INSN(),
```

但是他并不会被编译器提前编译为可执行文件然后交给内核执行，而是直接以这种类似汇编形式的语言经过一些编码（非编译）交给内核中的虚拟机执行。  
内核中是实现了一个小型的虚拟机负责动态的解析这些 eBPF 程序。也许有同学会思考为什么要用一个虚拟机去动态执行解析这些 eBPF 程序，而不是提前编译，直接执行编译好的过滤程序。  
对于这个问题我也搜了很多资料，但是并没有直接解答这个疑问的，在这里我提出自己的理解，不能保证正确，欢迎大家批评指正：  

> BPF 这种通过内核虚拟机执行包过滤规则的设计架构也是参考了别的包过滤器的。动态执行这种设计更加适合包过滤这种业务场景，由于包过滤的规则变化很快，而且可以很复杂，而且逻辑执行深度和数据包本身的字段内容强相关的，如果提前编译，可能有很大一块逻辑都不会执行，那么编译是完全浪费时间的，如果能够根据包本身的信息，对过滤代码动态编译就会节省很多时间，也更加灵活，所以最终采用了内核虚拟机动态解析过滤规则的方式实现 BPF。

#### **一个具体的 BPF 程序对数据包类别判断的例子**

例如下面这段代码

```
ldh \[12\]
jne #0x800, drop
ret #-1
drop: ret #0
```

这段代码的意思是从数据包的偏移 12 个字节的地方开始读取一个 half word 就是 16 个字节，然后判断这个值是否是 0x806, 如果不是，就执行 drop，否则执行返回 - 1。  
这个代码就是实现了判断包是否是 IPv4 包的功能，我们通过 wireshark 抓包可以发现  
在数据包偏移 12 字节的地方就是以太网头中 Type 字段。通过这个例子我们可以更加具体的了解 BPF 程序的工作原理。  

#### **eBPF 程序是如何交给内核执行的**

eBPF 程序虽然是有内核的虚拟机负责执行的，但是 eBPF 程序的编写确实完全由用户定义的，因此这也是 eBPF 模块是一个理想的内核提权攻击面的根本原因。  
eBPF 程序通过 BPF 系统调用，cmd 为 BPF\_PROG\_LOAD 就可以将 eBPF 程序发送给内核，还可以通过 cmd 为 BPF\_MAP\_CREATE 系统调用创建一个 map 数据结构，这个 map 数据结构就是用户侧运行的程序与内核中运行的 eBPF 程序进行数据交互的地方。其简要原理图为

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6nMLpJsdx2JaAc4H7HUnBnib7frGhJrPSAPR3Fkw1lzVmqDlCe5kicMMycNWQsAceLSHoYSzE6Zyvg/640?wx_fmt=png)

漏洞分析

通过上面对 eBPF 程序的设计架构和运行原理介绍之后，我们就可以对一个具体的 eBPF 提权漏洞 CVE-2020-8835 进行分析，披露这个漏洞的文章也出现了很多，本文更加侧重对漏洞原理的解释，希望读者能够掌握漏洞原理，能够对 eBPF 这个攻击面的安全性有更深入的思考，最好是也能挖到类似的漏洞。

#### **漏洞位置**

CVE-2020-8835 漏洞所涉及的函数为

```
static void \_\_reg\_bound\_offset32(struct bpf\_reg\_state \*reg)
{
    u64 mask = 0xffffFFFF;
    struct tnum range = tnum\_range(reg->umin\_value & mask,
                       reg->umax\_value & mask); // ----->1
    struct tnum lo32 = tnum\_cast(reg->var\_off, 4);
    struct tnum hi32 = tnum\_lshift(tnum\_rshift(reg->var\_off, 32), 32);

    reg->var\_off = tnum\_or(hi32, tnum\_intersect(lo32, range));
}
```

初看这个函数，很难理解 tnum，mask，tnum\_range，tnum\_cast 这些函数的作用，尽管 ZDI 博文中给了相关的解释，但我觉着还是对不了解 eBPF 模块的人不够友好，读完还是让人无法理解。由于这个漏洞和业务逻辑强相关，因此要想掌握漏洞原理，就必须能够理解代码的逻辑功能是什么，而代码中的 tnum 结构的数据类型是阻碍理解逻辑功能的关键。下面，本文将围绕 tnum 这个数据结构对此漏洞的根因进行分析。  

#### **Verifier**

漏洞函数\_\_reg\_bound\_offset32 所在文件为 verifier.c，verifier.c 文件实现了上图中 Verifier 的功能。eBPF 是用户侧编写的程序，但是却在内核虚拟机中执行，这显然是非常危险的，为了能够保障内核数据不被篡改和泄露，eBPF 在真正被虚拟机执行之前都会被 Verifier 检查，Verifier 会对 eBPF 指令的类型，跳转，是否有循环，以及操作数的取值范围进行检查，只有通过检查的 eBPF 的指令才可以被执行。  
那么 Verifier 到底是如何保证不会有 OOB 这种情况发生的呢？  
eBPF 程序的每个操作数的属性都会被`bpf_reg_state` 数据结构进行追踪  
`bpf_reg_state` 的结构如下

```
enum bpf\_reg\_type type;
    union {
        u16 range;
        struct bpf\_map \*map\_ptr;
        u32 btf\_id;
        unsigned long raw;
    };
    s32 off;
    u32 id;
    u32 ref\_obj\_id;
    struct tnum var\_off;
    s64 smin\_value;
    s64 smax\_value;
    u64 umin\_value;
    u64 umax\_value;
    struct bpf\_reg\_state \*parent;
    u32 frameno;
    s32 subreg\_def;
    enum bpf\_reg\_liveness live;
    bool precise;
```

可以看到对于每一个操作数，它的类型，值，取值范围都有详细的变量在追踪。常见的操作类型有 PTR 指针类型，或者 Scalar 这种常量类型的数据，为了防止越界，Verifier 禁止了很多类型的操作，比如禁止两个 PTR 类型的操作数运算，但是允许 PTR 类型与 Scalar 类型的操作数运算。即使允许 PTR 类型与 Scalar 类型操作，也不能保证安全性，因为如果 Scalar 比较大的话，还是可以导致 OOB，所以 Verifier 通过设置取值范围的方式来进行校验，如果操作数在运算后超过了被设定的最大最小值范围，也会被禁止。  
我们可以看到`bpf_reg_state`还定义了一个 tnum 变量，这个变量注释说是获得操作数各个位的信息的情况的，value，mask 两个字段一起表达操作数各个位的 0,1，或者未知的三种状态的。  

#### **tnum 数据结构的逻辑意义**

tnum 是为了描述那些不能有明确值的操作数，那么什么情况下操作数的值是不能确定的呢，例如从一个 packet 中读取一个 half word，这个值就是不能确定。而如果直接读取一个立即数，这种值就是确定的。对于这种不能确定的操作数，就可以用 umax,umin,smax,smin 这几种变量表示有符号和无符号的最大最小值，tnum 描述他们的每个位的信息。总之配合最大最小值，tnum 可以尽可能的对一个未知的变量进行预测。并且伴随着 eBPF 指令的执行，还会对 tnum，最大最小值进行更新，举个例子

```
if reg\_0 < 7    // 有符号比较
   reg\_1 = reg\_0
else
   reg\_1 = 1
```

在这个例子中，reg\_0 这个操作数会被跟踪，如果它小于 7，则可以对 reg\_0 的最大值进行设置，最大值为 7-1=6， 同时也得出高位都是 0，所以也可以对 tnum 进行设置。本文的`__reg_bound_offset32`函数就是负责处理 tnum 与最大最小值同步更新的工作的。  

tnum 到底是如何描述未知值的？  
假设拿到一个寄存器，这个寄存器就是不是一个确定值，用 tnum 表示他的位的状态，比如 64 位的一个数，那么某一位只可能三种状态，确定的 0，确定的 1，或者不知道是啥，就是这种数据结构是某个位有三种状态，而不是 2 种状态。

单纯的用一个 64 位的数据是不可能表达这种数据结构的，这种数据结构有 3 的 64 次方，而 64 位的二进制只有 2 的 64 方，但是如果有两个 64 位的数据就可以表达这个 64 位的三进制数据，2 的 128 次方。

所以就需要一种编码方式，用 2 个 64 位数编码这个三进制的数。

而 eBPF 的 tnum 的编码方式就是能确定是 1 的位，就 value 标识为确定 1，而能确定是 0 的位需要，value 位 0，并且 mask 对应位也为 0，相当于用 2 位去表达这个状态，，所以本质是用 2 位去表达三种状态，就是 x1，标识 1，01 标识 0，00 标识未知这种本质。

为了精确，模拟了一个 mask 和 value 的东西，就是 value 位能够决定某个位是 1，对应 mask 位的值必须为 0（有一个规定就是不能同时为 1），而对于确定是 0 的位，则必须 value 位为 0，mask 也要为 0，对于 unknown 的状态，需要 value 为 0，而 mask 为 1  
所以最终的表达为

```
value  mask    预测值
 0      0       0
 1      0       1
 0      1       unknown
 1      1       禁止出现
```

#### **\_\_reg\_bound\_offset32 漏洞函数解析**  

除了`__reg_bound_offset32`还有一个`__reg_bound_offset`函数，这个函数功能更加简洁

```
static void \_\_reg\_bound\_offset(struct bpf\_reg\_state \*reg)
{
    reg->var\_off = tnum\_intersect(reg->var\_off,
                      tnum\_range(reg->umin\_value,
                         reg->umax\_value));
}
```

`__reg_bound_offset32`是一种特殊情况，只有当操作数已经明知是 32 位的才会执行，而对于一般的是默认执行`__reg_bound_offset`操作，我们可以先从`__reg_bound_offset`去推测 \_\_reg\_bound\_offset32 的大概意义。  
`tnum_intersect`函数的输入是两个 tnum 的变量，根据名字和源码我们可以简要总结：当有两个 tnum 对同一个操作数进行描述的时候，可以结合两个 tnum 的信息，这样可以对这个操作数的描述更加精确，结合的规则就是，如果一个 tnum 的某个位已知，另外一个 tnum 的对应位为未知，那么结合后新 tnum 对应位则是已知的。  

`tnum_range` 函数作用是，根据一个更新后的最大最小值得到一个 tnum。这个 tnum 可以与目标操作数的 tnum 进行 tnum\_intersect，相当于融合了最大最小值的信息，这样可以实现对原来的操作数进行更准确的预测更新。

所以根据`__reg_bound_offset`的作用，我们知道了主要目的就是根据最大最小值对原来操作数的 tnum 进行更加准确的预测。那么`__reg_bound_offset32`又有什么不同呢？

`__reg_bound_offset32` 源码如下:

```
static void \_\_reg\_bound\_offset32(struct bpf\_reg\_state \*reg)
{
    u64 mask = 0xffffFFFF;
    struct tnum range = tnum\_range(reg->umin\_value & mask,
                       reg->umax\_value & mask); // ----->1
    struct tnum lo32 = tnum\_cast(reg->var\_off, 4);
    struct tnum hi32 = tnum\_lshift(tnum\_rshift(reg->var\_off, 32), 32);

    reg->var\_off = tnum\_or(hi32, tnum\_intersect(lo32, range));
}
```

我们利用理解`tnum_range`函数的方法，可以推得`tnum_cast`，`tnum_lshift`，`tnum_or`的作用，可以感觉出整个函数的目的是同样根据最大最小值对已有的 tnum 值进行更新。而且，相比于`__reg_bound_offset`函数，`__reg_bound_offset32`还有一个隐藏的信息可以对操作数进行更加准确的预测：  
32 位数的最大最小值不会超过 0xFFFFFFFF  

这个隐藏条件的表达就是 标注 1 所做的工作，漏洞代码尝试用截断低 32 位的方式来表达 32 位数的最大最小值不会超过 0xFFFFFFFF，但是实际上这个语句并不能表达这个功能。准确的表达是

```
new\_umin\_value = min(0xffffffff,umin\_value)
new\_umax\_value = min(0xffffffff,umax\_value)
 range  = tnum\_range(new\_umin\_value, new\_umax\_value)
```

上面两句话是笔者自己理解的实现 32 位隐藏条件的代码。  

#### **漏洞根因**

正是`struct tnum range = tnum_range(reg->umin_value & mask,  
reg->umax_value & mask);` 这一条语句导致的漏洞，这句话实现的是截断功能，而不是对于超出 32 位的数直接取值为 0xffff ffff 的功能。

由于这个错误的实现导致 Veifier 并不能正确的验证 eBPF 指令的执行情况，所以对一些本应该禁止的 OOB 操作，Verifier 还是通过了检查，最终可以实现对内核数据的越界读写。

小结

这个漏洞的 Root Cause 是和漏洞函数的业务功能逻辑强相关的，如果不理解代码的目的，很难对这个漏洞的根本原因理解，而由于 eBPF 的执行流程又比较特别，需要对背景知识，设计架构，运行机理有一定的了解才能够推理出漏洞函数的功能。为了能够让不熟悉 eBPF 的同学能够更加快速的了解 eBPF，接触 eBPF 这一个理想的内核攻击面。eBPF 程序由用户定义，但是在内核中执行，这是 eBPF 模块是一个值得重视的内核攻击面的根本原因。希望本文提供的思维路线，能够帮助到大家。

参考

1 https://www.kernel.org/doc/html/latest/networking/filter.html#networking-filter  
2 https://www.thezdi.com/blog/2020/4/8/cve-2020-8835-linux-kernel-privilege-escalation-via-improper-ebpf-program-verification  
3 https://www.anquanke.com/post/id/203416  
4 https://colorlight.github.io/2020/10/10 / 捉虫日记漏洞总结 /

（点击 “阅读原文” 查看链接）

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6OLwHohYU7UjX5anusw3ZzxxUKM0Ert9iaakSvib40glppuwsWytjDfiaFx1T25gsIWL5c8c7kicamxw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/Ok4fxxCpBb5ZMeq0JBK8AOH3CVMApDrPvnibHjxDDT1mY2ic8ABv6zWUDq0VxcQ128rL7lxiaQrE1oTmjqInO89xA/640?wx_fmt=gif)

**戳 “阅读原文” 查看更多内容**