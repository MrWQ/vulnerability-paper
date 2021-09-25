> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yMS_Rf6WbRVC_MSXYIe4KQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **165** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/LcN5ZibxypT4ZquODsTZNAnXQXiaroUzDV7Jl3iabjQPTNRqGI4oqjDAgicIhUqqNov46scp8yMEPVMBzHr335FITw/640?wx_fmt=png)

  

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/200

靶机难度：疯狂（5.0/10）

靶机发布日期：2020 年 3 月 1 日

靶机描述：

Rope is an insane difficulty Linux machine covering different aspects of binary exploitation. The

web server can be exploited to gain access to the file system and download the binary. The

binary is found to be vulnerable to format string exploitation, which is leveraged to get remote

code execution. After gaining foothold, the user is found to have access to a shared library, which

can be modified to execute code as another user. A service running on localhost can be exploited

via a ROP (Return Oriented Programming) attack to gain a root shell.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/nwVxrsE7EViaefzH6Zqupw9JNicPLwkLuSAYJib3qChCe0T62E1ErLqTKwfkKT9c7beA5Uic0SltXLVSdUDrBSZhrQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/7vBu6OIvS5MqCqrfIrt8m9PqCAwIOKsoIibkg9ERXOT2hAm60YmwmoiatImzxBVFvjcptuNWwmGmAvPEhvXzibwfw/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msYoDic3BPB7EyqD8iczOnibODfncZnOQzncdBqsopbJYwfNqVQn2Y20Vrg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.147...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msCiaqOV4pibNUKR608ddibeSOaAosaWXE5OKicQjJcaA5SFhR1pshXjDgMQ/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 22，9999 端口，在利用 nmap 详细的扫描了两个端口情况.. 看图即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msFT0ZTVaGSQXswWfBzCTq1bY6nNTIHOjgt4jeD6gnribDiaABSEEoXBPQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8ms4Xia5khExOlFmqpqd3TGnsVBlT9JicIE3hqBr39OF6hCLKcZN8omT16Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msLpzYD6zmD0bS3ABmdgul8gzHriaYZebLyRfkO4VVCyEFMR9couBLc9A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8mss6wZMJa2PRV2oTqic0jSOzrWLFd55WfWa5VLia5a8t5f4tXtI9ybQHBw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msGUgfKmLfXhniag9YWZsIicib7EfAHicNUlnwr8L16LXEvIDFszibeAqDVWQ/640?wx_fmt=png)

脚本循环运行，并在 httpserver 二进制文件崩溃或退出时执行。让我们

下载二进制文件并进行分析。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8ms7360ice0lzas9ddfWNQ33LgM4IT1o1bStUy727DpCrTCkzniaAHjWvIA/640?wx_fmt=png)

32 位的 elf...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msKBVyL1YwEnYgb8Tlf4enywZpg5hfdDaPKzuOP1K7T3E0oTxwbMwasg/640?wx_fmt=png)

NX 开启，目前受保护状态...

NX 位是：CPU 中使用的一项技术，可确保某些内存区域（例如堆栈和堆）无法执行，而其他部分（例如一段代码）无法写入，这样可以防止我们将 shellcode 写入堆栈并执行它...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msO3gtsaraSUjgaJ73BUlGibCuzgfJPibTKZ24ia8rdRajUOyp98u1OaS6A/640?wx_fmt=png)

简单的测试，存在 / 的输出，和字符串有关系？

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msbpJt3ibI5kmqJ93cqg5mT5fyjP2fibcUVdfibZdeuW6LyncbLGM2p7JicQ/640?wx_fmt=png)

木有 IDA，mac 最新版系统没法安装 IDA，只能用 ghidra 进行逆向分析了...

直接查看 main，发现了其中的规律...

从 main 开始，还在底部看到一个输出 accept...

初始设置后，二进制文件调用 open_listenfd 绑定到所需的端口（local）并启动监听请求，然后它打印一些信息，然后放入循环中，直到发出请求为止，最后通过 accept（）收到...

收到请求后，输入文件描述符 local_12c 传递给 process（）函数以及 sockaddr 结构，二进制文件调用 fork（）生成一个子进程，然后其余的执行继续在新产生的过程中，然后调用 parse_request（），该文件将文件路径返回到 local_xx 缓冲区，进行 open（）syscall 来访问文件并检查文件是否存在...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msN4U8cnuDYbhPlYdg2ZnwQCeFtHg9VvlV1Mnib6PjsTzT9vN7Aqztbpg/640?wx_fmt=png)

查看 log_access，保留了 sockaddr 结构中的主机地址，并且调用 printf（）来打印日志。第一个 printf 打印状态码和地址，第二个 printf 不使用％s 格式字符串直接打印请求的文件，这里在二进制文件中就引发了格式字符串漏洞，会导致任意读取和写入访问...

这就是攻入点...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8ms8A6icbibQibneNJORpoO7F2tS73cmDpibiauiaLPkaDAMYlH92PudNjbJ5qw/640?wx_fmt=png)

知道了格式字符串漏洞后，通过测试，从堆栈读取数据...

知道了 41414141（AAAA）和 42424242（BBBB）的偏移分别为 53 和 54...（0x41414141-AAAA）

知道了控制内存地址的偏移量以及由写入的字节数 printf，我们可以使用 pwntools fmtstr_payload 生成格式字符串有效负载... 写入 EXP 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8ms3W7rYk8d8bNS06hG44xasic1AmwH3t1rmhlc1h5sVAW8keicOVf02SVg/640?wx_fmt=png)

最后，程序加载的地址和程序使用的库...

有了 565ad000 和 f7dac000，可以利用它来执行 libc 库的路径...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msbBrRbPibHhJZ4SCUpn1dLUCPp1rfibAco8PeA52zjrq9S5iakibdHkwYLQ/640?wx_fmt=png)

最后根据分析，我在 EXP 创建了一个命令，该命令将一些 base64 回显到中 base64 -d 中，可看到执行后的 shell 以 base64 进行写入执行... 获得了反向外壳...

继续查看用户的 sudo 特权，发现可以以 r4j 用户身份运行 readlogs...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msHE599XR89fxlF0HlADLUKXOwJ34JDCqZq8unhUtw1WdjLLVYgtnNibA/640?wx_fmt=png)

这里不太稳定，直接利用 ssh 输入 key，直接登录更放心稳定...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msKoxhVceyyeV49ibWJDJkMPTmmPicrZIk9STPT9VscODYy6CLCTEWdm8A/640?wx_fmt=png)

二进制文件在执行时打印出 / var/log/auth.log 的内容...

执行中查看下 liblogs 状态...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msVHxBgibb6jaCHv0J5Ipb1ibmIIV4LsFkbQFULico4UrJGZRbOX2WHqpicw/640?wx_fmt=png)

可以看到具有写入权限... 写入个 shell，他会自动带 liblogs 执行直接就能获得外壳了...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msXpoGLa9P0chLAe7p3KnHdAkib1yX4VS6yO3ZmU8Fpkyy8e41mMTh15A/640?wx_fmt=png)

简单的 gcc 编写的 shell（不陌生了），然后 gcc 编译后，通过 ssh 的 scp 上传覆盖即可...

然后执行该程序，获得了 r4j 用户权限.... 读取到了 user_flag 信息...

这真是太难了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8ms3tyGbk9icf6xsib9FEQZYz08csJRZia5qp2f3HvricsNZbxz9Fqu1Bwe1g/640?wx_fmt=png)

不多说，直接 ssh-key 继续利用 ssh 登录 r4j 用户... 方便后面渗透...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msj2oDdHHCn0X6FjCiab4MVCJBvlRILcNd1H46GWNSiajp41VCrhl2NbRw/640?wx_fmt=png)

由于该靶机就是二进制提权的靶机，我继续 ps aux 直接查看了所有 root 权限执行的程序...

发现了 contact 可以分析... 开始吧

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msVBdtTfvmXleARYzfIg2jiaHTN5Ig7wiaVy9MS7nnlsR97sxdibJXstokw/640?wx_fmt=png)

可看到靶机本地还开放了 1337 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msicCb8AObtDClV5CRribKLGCvU9l03eqzkhyNCFmYc1VIvPKtp28bZAxA/640?wx_fmt=png)

将文件下载下来后... 开始检查...

Checksec 显示所有保护机制均已启用....

这里堆栈金丝雀和 PIE 绝对是大麻烦.... 都开启了保护机制....

后面不得不绕过这两个保护机制来利用二进制文件提权.... 了解下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msxib06ZyxLGibtVnHEFtWtkPmicT2sYpfG41ZiboWGgr0d93jCI7p5gSzuA/640?wx_fmt=png)

这就是金丝雀.... 百度百科...google 也很多解释，自己查吧

下面思路就是，查找并溢出缓冲区位置，然后找到金丝雀的可利用处进行利用...

由于 PIE 已激活，需要找到有效的偏移量.... 这是最难点.... 就是查找内存泄漏以计算加载库的地址...

最后构建一个 ROP 植入 shell....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msHibXCo6yjuwpaISpDRmvK642UAiaJCm2kshT5gib0BbroE497KZYWorYA/640?wx_fmt=png)

IDA 打算晚点 windows 虚拟机装...

目前没有 IDA，只能勉强用 Ghidra 神器进行逆向分析...

可以看到最重要的点是 FUN_0010140e，双击查看下该进程的怎么执行的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msicM0yoXiaq3LfGHI5mRCm1LxaJibjbmTvyJU8dic0BC9H1Pj2hpPpnx8Jg/640?wx_fmt=png)

这里包含我们在启动二进制文件时看到的 printf，此功能很可能是主要功能....

它在端口 1337 上设置侦听器（0x539）...

该 forkProcess() 函数创建一个子进程以与客户端进行交互...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8ms9Cmyic2ElAo6rtyGnkTTLUiaUeQ5ItibejhLvKULNWogWMGrosDRvjQBw/640?wx_fmt=png)

函数 FUN_001014ee 收到连接后立即用 fd 进行调用....

FUN_001014ee 是处理功能，该函数执行 fork（）并生成一个子进程，然后使用 write（）函数

向客户端发送提示，然后调用另一个函数....

流程函数创建一个子流程来处理请求，这是有好处的，因为堆栈金丝雀对于子进程不会更改，程序中似乎存在实际的编程错误，可看到它不打印 PID，而是调用 getuid（）并打印用户 ID，然后通过多次连接到实例...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msOj4Imr2kryNHccjf91dqjYXo9m324TxJqQgY3Znzue8sibxwicia1cdrA/640?wx_fmt=png)

通过测试可看到显著的效果...

pid 始终为 0（进程由 root 运行，因此 uid 为 0），fd 为 4（稍后将对此进行介绍）....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msibugSzZBpqYRERchvnVib279zf5hZibTbMb9maDd2kEhib9WyrDx5ke67w/640?wx_fmt=png)

FUN_0010159a：此函数调用 recv（）函数并从客户端读取 0x400，即 128 个字节，此输入被写入 local_48 缓冲区，该缓冲区的长度为 56 个字节....

如果输入发送的长度大于 56 会导致缓冲区溢出... 但是由于以下原因，无法直接利用此溢出：

堆栈金丝雀的存在，堆栈金丝雀是一个包含 8 个随机字节的值，它位于在堆栈底部上方。在该功能存在之前，将存储此值后并检查是否有更改....（重要）金丝雀的任何更改都将导致异常并退出流程...

recv_data（）函数从用户接收多达 1024（0x400) 个字节，并将其写入 56 字节大缓冲区中，这是此二进制文件的攻击媒介，可以从这儿入手...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8mszwJq51GWNB8uFDkelIB78gDMBrhLUvG4o18dyyBr2NQmEiaX3oqHbyw/640?wx_fmt=png)

在开始利用漏洞之前，让我们下载使用的 libc 文件... 以在本地运行拿权更方便... 省的还要镜像 1337 过来网络不稳定...

![](https://mmbiz.qpic.cn/mmbiz_gif/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msibmUCicDOicIqH7hFqLCzial2eYH6zO7Adqwibaq9q8IdluU60grSs9egvg/640?wx_fmt=gif)

```
https://made0x78.com/bseries-defeat-stack-cookies/
```

这张图很好解释了接下来的事情，利用蛮力逐字节堆栈金丝雀的原理在本文中有很好的解释....

基本思想是我们一次将堆栈中的值覆盖一个字节，如果我们得到完成的消息，知道被覆盖的值没有更改，并且我们有一个正确的字节，然后可以转到下一个字节，依此类推....

可以参考文章里的思路，但是 EXP 得自己编写.... 这里我就不多介绍了，都是无限测试中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOBfICibgz7uDvazEkrzC8msicld6hZ0WyMAyl7FbrzYgEicvjXPpCJlibiaFHiaO2JgOwowjpz4RVhRxoQ/640?wx_fmt=png)

这里坚信只有自己知道，这里一定要 libc.so 文件下载到本地，先从本地跑测试，本地能拿 shell 了，在直接进行靶机即可... 省很多时间... 每次找金丝雀裂缝点，都要 10 多 20 分钟....

![](https://mmbiz.qpic.cn/mmbiz_png/LcN5ZibxypT4ZquODsTZNAnXQXiaroUzDV7Jl3iabjQPTNRqGI4oqjDAgicIhUqqNov46scp8yMEPVMBzHr335FITw/640?wx_fmt=png)

  

  

可看到获得了 root 权限和 flag....

我还进一步的利用 ssh，登录了 root，稳定的外壳... 然后进行了各种信息收集枚举....

这是个简单的系统... 只有二进制漏洞可以利用，没有别的地方可以提权了....

好难，这是深入版的缓冲区溢出吗？花了我两三天时间.... 学到很多东西... 需要继续脑补下代码审计写 EXP 的功率，和栈堆二进制的一些理论原理....

加油加油！！

最后我会在每篇 NO 文章后面注明，我不会在每个图片下面附上命令了，我没有心情像 NO1~50 一样去详细解释每个知识点了，望理解。

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台疯狂的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/nwVxrsE7EViaefzH6Zqupw9JNicPLwkLuSAYJib3qChCe0T62E1ErLqTKwfkKT9c7beA5Uic0SltXLVSdUDrBSZhrQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)