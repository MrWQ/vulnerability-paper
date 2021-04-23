# 冰蝎beta8内存马防查杀破解
今早发现冰蝎webshell 更新至beta8，其中一点更新比较稳，如图

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

其中新增了内存马防查杀机制，话不多说，盘它。

对比新增的代码，有一点比较突出，如图

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/1_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

个人猜想，作者可能是想通过关闭某些pipe，以防止应急响应加载javaagent。正好，我看到很多人都想禁止第三方加载javaagent以保证自己的内存马不被查杀。下面我们来分析一下`sun.tools.attach`都做了什么，为什么无法做到无法禁止javaagent的加载。

要解决上面这个问题，我们需要思考，`sun.tools.attach`是如何于目标JVM通信的，是怎么于目标JMV传递数据的？只有搞清楚这两个问题，我们才能解决怎样禁止javaagent加载

> 以下分析基于windows

1\. java层
---------

我们先从最基础的，向一个正在运行的JVM加载agent的操作开始分析。很多恶意javaagent，都在想方设法禁止后续javaagent加载

    List<VirtualMachineDescriptor> vms = VirtualMachine.list();
    for(VirtualMachineDescriptor vm:vms){
        if (vm.displayName().contains("catalina")){
            VirtualMachine v = VirtualMachine.attach(vm);
            v.loadAgent("D:\\sources\\AgentMemShellScanner\\tools_0.jar", "L2E=|L2E=");
        }
    }

其实调用的是如下代码

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/1_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

上面的操作其实就是打开目标JVM的进程。`loadagent`方法的代码如下

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/2_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

最终其实调用的是

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/3_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

加载agent这个操作，首先打开目标进程JVM，然后再创建一个pipe，后缀数字为随机数。然后再通过某些操作，执行命令。上图中大多数函数都为JNI函数，我们接着分析

2\. JNI 部分
----------

openprocess这个函数就不过多详细介绍了，只是调用windows api打开进程，如图

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/4_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

我们知道，在windows 进程ipc通信中，如果两个进程需要使用Pipe通信，则通信双方都需要打开pipe。而在这里，我们的java创建了Pipe，但是目标JVM并不知道我们的pipe名称。如果不知道名称就无法做IPC通信。下面分析一下怎么通知目标JVM需要读取pipe数据的。

在java中，首先创建Pipe，然后通过`enqueue`方法，同过管道向目标JVM写入命令。在`enqueue`的JNI方法中，我们看到了如下的代码

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/5_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

典型的shellcode注入代码，向目标内存申请内存，类型为可读可写可执行，然后复制shellcode到刚才申请的内存中，然后通过CreateRemoteThread调用shellcode。当然，这段shellcode可不是什么而已操作，只是完成某些JVM指令。

这段shellcode是通过`generateStub`函数生成，同样也是一个native函数。分析一下`generateStub`

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/6_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

很明显，这段shellcode的内容，其实为`jvm_attach_thread_func`的内容。当然，在这里就不详细介绍了，学一些简单的c就能看懂上面的代码。

![](%E5%86%B0%E8%9D%8Ebeta8%E5%86%85%E5%AD%98%E9%A9%AC%E9%98%B2%E6%9F%A5%E6%9D%80%E7%A0%B4%E8%A7%A3/7_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

简单概括，就是我们的java进程，通过向目标JVM注入shellcode来执行我们与目标JVM的通信指令。Pipe只是一种通信手段，关闭pipe并不能影响我们向目标JVM加载javaagent。

当然，目标JVM都做了什么操作，在这里就不分析了。

回到最初疑问，我们通过分析可以得出以下结论：

> 要想禁止javaagent加载，首先需要禁止目标JVM进程被打开或者禁止向目标JVM注入shellcode。JVM可能无法完成禁止javaagent加载这个操作。但这是不是给了某些edr产品的防护javaagent内存马的思路？？

至于冰蝎的内存马，看样子依旧可以正常查杀，毫不影响。