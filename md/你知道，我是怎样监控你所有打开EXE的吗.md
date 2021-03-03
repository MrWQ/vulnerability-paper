> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/U4IlQ2XaEsjzjvSnYQvJpQ)

  

![图片](https://mmbiz.qpic.cn/mmbiz_gif/3xxicXNlTXLicwgPqvK8QgwnCr09iaSllrsXJLMkThiaHibEntZKkJiaicEd4ibWQxyn3gtAWbyGqtHVb0qqsHFC9jW3oQ/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)  

> **文章来****源：游戏安全攻防**

![图片](https://mmbiz.qpic.cn/mmbiz_png/4FRMwYHkzw4SOT1gRuFKeK59CFqqxl0ibFO802ibcZ3iceT1Dur1vPOzEfj0k2z6sibDiaicn2LltqLDTuUdCOmibdptg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

A

技术应用背景：

目前已知在杀毒厂商以及游戏厂商的安全对抗过程中，常常需要准确的监控收集并进行检测用户创建打开的EXE应用程序是否是安全的。同时也可以将此技术应用于其他应用的安全对抗方案中。那么如何去准确的监控和收集用户每次点击打开的EXE应用程序信息呢？接下来我就进行还原实现下如何准确的监控并收集用户每次点击打开EXE应用程序技术。

  

  

A

效果展示：

下图展示的是开启监控程序，这是进行监控电脑上包括系统自启动EXE程序以及用户主动点击启动应用程序的信息。

![图片](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr5z1Pkp8z74Agj9n9j6KibcviatdLk8UYVoqt3mcCPVdYgic0Xnw7e0LbJm9Xp0N4eV8fxvfAEmicclQA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

A

功能代码实现：

实现监控用户所有创建打开EXE程序的数据需要以下几个步骤：

1.通过调用CoInitializeEx函数，进行对COM初始化。

2.通过调用 CoCreateInstance函数， 获得WMI的定位器。

3.通过调用IWbemLocator::ConnectServer函数，并指定函数的参数 strNetworkResource 的值为 "root\cimv2", 从而实现连接到 "IWbemServices"服务器。

4. 通过调用CoSetProxyBlanket函数，进行设置 IWbemServices的代理，目的是为了WMI 服务能够模拟客户端角色。

5.通过调用 ExecNotificationQuery函数， 来进行查询接收事件。

![图片](https://mmbiz.qpic.cn/mmbiz_png/lYDNMgmFjur6mfkPywZNgKZYXia5C4lA8Kd6CUYOibay3HbIfxBnNXH3v6jQZf6QquSL5dt6qYMrtQGh7go67FZg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

下图这部分代码主要的目的是为了初始化COM和WMI的设置。

![图片](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr5z1Pkp8z74Agj9n9j6KibcvZvkXed3BpspebKdSuIEh6vRQCCJYtThzuIIicmclcBMDu3e4xMVMdVw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

下面代码主要实现查询接收事件，也就是通过ExecNotificationQuery查询来循环获取用户所创建打开的所有EXE的数据。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

A

知识背景清单：

概述：WMI技术算得上是一个很古老的技术，它是由微软提供的，同时也是一种非常可靠的解决方案。WMI它还有一个非常大的优势，可以进行访问远程电脑。它是Windows操作系统中管理数据和操作的基础模块，**它提供了一个通过操作系统、网络和企业环境去管理本地或远程计算机的统一接口集**。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**WMI技术可以应用于：**

1.  查询获取正在运行进程信息；
    
2.  查询获取正在运行线程信息；
    
3.  查询获取桌面信息；
    
4.  查询获取环境变量信息；
    
5.  查询获取驱动信息；
    
6.  查询获取文件夹信息；
    
7.  查询获取系统信息和系统服务；
    
8.  查询获取硬件信息；
    
9.  查询获取磁盘相关信息。
    
    ---
    

  

WMI相关概念

  

1.WBEM它的全称:**Web Based Enterprise Management(基于web的企业管理)**,它是一种行业规范，建立在企业网络中访问和共享管理信息的标准。

2.WMI它的全称**:Windows Management Instrumentation(Windows管理工具)**,它是WBEM的Windows实现，也就是它要遵守WBEM规则。通过WMI，我们可以获取关于硬件和软件的相关数据，也可以提供关于硬件或软件服务的数据给WMI。

3.COM 它的全称：**Component Object Model(组件对象模型)**，它是由微软推出的一套接口规范，通过设定不同组件之间需要遵守的标准与协议，主要用来跨语言、跨进程之间的模块通信。

  

  

WMI相关函数

  

**1.****CoInitializeEx函数详解**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**2.** **CoCreateInstance函数详解**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**3.** **ConnectServer函数详解**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

**4.** **CoSetProxyBlanket函数详解**

**![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)**

**5.****ExecNotificationQuery函数详解**

**![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)**

  

  

WMI架构解析

  

下图的WMI架构图来源于MSDN，我们可以从架构图中很清晰的看到WMI主要分为3的层结构。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**1.WMI providers****and Managed object(WMI提供者和管理对象)**

WMI提供者是一个监控一个或者多个的托管对象的COM接口。

托管对象是指逻辑或者物理组件，例如硬盘驱动器、网络适配器、数据库系统、操作系统、进程或者服务。

WMI提供者通过托管对象提供的数据向WMI服务提供数据，同时将WMI服务的请求传递给托管对象。

WMI提供者是由实现逻辑的DLL和承载着描述数据和操作的类的托管对象格式MOF(Managed Object Format)文件组成。其中这个两个文件都保存在\Windows\System32\wbem目录下。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**2.WMI Infrastructure(WMI基础结构)**

WMI的基础结构是Windows系统的系统组件。它主要包含两个模块：包含WMI Core(WMI核心)的**WMI Service(WMI服务)**和**WMI Repository(WMI存储库)**。

  WMI存储库是通过WMI Namespace(WMI命名空间)组织起来的。在系统启动时，WMI服务会创建例如root\cimv2、root\default、root\subscription等等命名空间。

**WMI服务扮演着WMi提供者、管理应用和WMI存储库之间的协调者角色。**一般来说，它是通过一个共享的服务进程svchost来实施工作的。当第一个管理应用向WMI命名空间发起连接时，WMI服务将会启动。当管理应用不再调用WMI时，WMI服务将会关闭或者进入低内存状态。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**3.WMI Consumers(WMI使用者)**

 它位于WMI构架的最顶层，它是WMI技术使用的载体。对于使用C++代码实现我们就可以直接通过COM技术直接与下层进行通信。对于.net平台语言，则要使用System.Management域相关功能与下层进行通信。WMI的使用者，可以进行查询、枚举数据，也可以运行Provider的方法，还可以向WMI订阅消息。其中这些数据操作都是要有相应的Provider来提供。

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "微信公众号文章素材之分割线大全")

  

推荐文章++++

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

*[泄露文件曝光任天堂侵入性监控黑客行动](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650497965&idx=2&sn=21342fd5e610d77da735edca9a35bb82&chksm=83ba0649b4cd8f5ff035996f1fa7dde71266d837c95a0ad03434cb3d9a2057199c43376bce1d&scene=21#wechat_redirect)  

*[不用买监控，教你用一部手机，就能监控家里的一切](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650461076&idx=4&sn=53831ab971a0e8c3d0f4c9fc6f706db4&chksm=83bbb670b4cc3f6613aefbc3e95d8ef875f7cecf3d00d380357af258f4ebfcee886eb5bfd1a6&scene=21#wechat_redirect)

*[国外黑客蠢蠢欲动，预攻击我国视频监控](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650459678&idx=1&sn=36f38d39a1df924e1df70e9d2053571a&chksm=83bbabfab4cc22ec42d01d6c42a05cc64964cabc85831c4d6ee4fa2f132efb4f15aebe522550&scene=21#wechat_redirect)

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)