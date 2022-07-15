> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/bmzuESPs7Q1SBBOf3Ze4gQ)

今早发现冰蝎 webshell 更新至 beta8，其中一点更新比较稳，如图

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7h6QiaRsH3h5HEzMBRFib9M4NQ70BtYgjsCB1snMibSwRicQxEBf3QHTlQg/640?wx_fmt=png)

其中新增了内存马防查杀机制，话不多说，盘它。

对比新增的代码，有一点比较突出，如图

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7KQyxf52Rxbpf28OGFjWg9wfl2dAMiboJfZ3R80ZvR4AfS5T2Zia9diboQ/640?wx_fmt=png)

个人猜想，作者可能是想通过关闭某些 pipe，以防止应急响应加载 javaagent。正好，我看到很多人都想禁止第三方加载 javaagent 以保证自己的内存马不被查杀。下面我们来分析一下`sun.tools.attach`都做了什么，为什么无法做到无法禁止 javaagent 的加载。

要解决上面这个问题，我们需要思考，`sun.tools.attach`是如何于目标 JVM 通信的，是怎么于目标 JMV 传递数据的？只有搞清楚这两个问题，我们才能解决怎样禁止 javaagent 加载

> 以下分析基于 windows

1. java 层
---------

我们先从最基础的，向一个正在运行的 JVM 加载 agent 的操作开始分析。很多恶意 javaagent，都在想方设法禁止后续 javaagent 加载

```
List<VirtualMachineDescriptor> vms = VirtualMachine.list();        for(VirtualMachineDescriptor vm:vms){            if (vm.displayName().contains("catalina")){                VirtualMachine v = VirtualMachine.attach(vm);         v.loadAgent("D:\\sources\\AgentMemShellScanner\\tools_0.jar", "L2E=|L2E=");            }        }
```

其实调用的是如下代码

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7sdbMd7qicjIegOIBOzvniasGyZKohfQsE6YolD0VsvumkfFBl0wfHfEg/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7Cf7BFL1Qv0wWzh9avqlic6e01cIfd3RGFzNZLoyjUMz94DQYrBZOWSw/640?wx_fmt=png)

上面的操作其实就是打开目标 JVM 的进程。`loadagent`方法的代码如下

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7AsrHo5fj3icfniaOicCAbt4PTo0CZYlWmsEZBuz4o8SxXCr8TWDN8SjGQ/640?wx_fmt=png)

最终其实调用的是

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7g9picPyLXo1mcOgJRUUZlP1SrnrbhvljROAjnGbROAFzpgTNrdibhGGA/640?wx_fmt=png)

加载 agent 这个操作，首先打开目标进程 JVM，然后再创建一个 pipe，后缀数字为随机数。然后再通过某些操作，执行命令。上图中大多数函数都为 JNI 函数，我们接着分析

2. JNI 部分
---------

openprocess 这个函数就不过多详细介绍了，只是调用 windows api 打开进程，如图

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7eRs8NtbUwdNFVvI6KxlRk9FzgYdmB0qvLicqNvW9436oiaYjpiaC8sL1g/640?wx_fmt=png)

我们知道，在 windows 进程 ipc 通信中，如果两个进程需要使用 Pipe 通信，则通信双方都需要打开 pipe。而在这里，我们的 java 创建了 Pipe，但是目标 JVM 并不知道我们的 pipe 名称。如果不知道名称就无法做 IPC 通信。下面分析一下怎么通知目标 JVM 需要读取 pipe 数据的。

在 java 中，首先创建 Pipe，然后通过`enqueue`方法，同过管道向目标 JVM 写入命令。在`enqueue`的 JNI 方法中，我们看到了如下的代码

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7PV6mfjw3MPzDatb0eX0H8AHKaqGbARzkRPdwWUf0px57HZwaesaODA/640?wx_fmt=png)

典型的 shellcode 注入代码，向目标内存申请内存，类型为可读可写可执行，然后复制 shellcode 到刚才申请的内存中，然后通过 CreateRemoteThread 调用 shellcode。当然，这段 shellcode 可不是什么而已操作，只是完成某些 JVM 指令。

这段 shellcode 是通过`generateStub`函数生成，同样也是一个 native 函数。分析一下`generateStub`

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl71OVKaHyMtxBOziayiaZLOseiaKKbSCufRWz7CSY7ibedN1fC4UxSKNAv0g/640?wx_fmt=png)

很明显，这段 shellcode 的内容，其实为`jvm_attach_thread_func`的内容。当然，在这里就不详细介绍了，学一些简单的 c 就能看懂上面的代码。

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdE40vtulsu14VSklibJ00ibl7BRDZj4b6kkt4KG1eISONWAJCAfGibopQBeNuMib7PZh0tByVv1X7LDTg/640?wx_fmt=png)

简单概括，就是我们的 java 进程，通过向目标 JVM 注入 shellcode 来执行我们与目标 JVM 的通信指令。Pipe 只是一种通信手段，关闭 pipe 并不能影响我们向目标 JVM 加载 javaagent。

当然，目标 JVM 都做了什么操作，在这里就不分析了。

回到最初疑问，我们通过分析可以得出以下结论：

> 要想禁止 javaagent 加载，首先需要禁止目标 JVM 进程被打开或者禁止向目标 JVM 注入 shellcode。JVM 可能无法完成禁止 javaagent 加载这个操作。但这是不是给了某些 edr 产品的防护 javaagent 内存马的思路？？

至于冰蝎的内存马，看样子依旧可以正常查杀，毫不影响。

不过，我看到内存马中多了另外一种 JVM 持久化方法，正好前段时间研究过。兄弟们转发支持，多多加入星球。明后天更新基于 Classpath 的 jvm 持久化方法。

我正在「宽字节安全」和朋友们讨论有趣的话题，你⼀起来吧？https://t.zsxq.com/qJe2JEi

![](https://mmbiz.qpic.cn/mmbiz_png/cOCqjucntdGgXGuibZ56sAeSjVFPyWEw25uaZEmwaGKmltLREfSVu5J7C9y8q7qg7GoGW5iapmeHKPoFY74Ha1fA/640?wx_fmt=png)