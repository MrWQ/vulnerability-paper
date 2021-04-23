# 浅析Cobalt Strike Team Server扫描
**前言**
------

Cobalt Strike 是由Strategic Cyber公司开发的一款商业化渗透测试工具。该软件具有简单易用、可扩展性高等优点，并且具备团队协作等特点，因此被广大黑客、白帽子和安全研究人员等大量装备使用。网络空间测绘就是利用扫描发掘互联网中一切可发掘的资产和目标。Cobalt Strike 的发掘，是360 Quake团队一直以来的核心目标之一。

在本文中我们将站在蓝方角度思考，通过研究Cobalt Strike客户端与服务端交互的代码逻辑，来发掘出Cobalt Strike Team Server特征，并且进行进一步探测与分析。

**逻辑分析**
--------

Cobalt Strike 的是C/S（Client-Server）架构，有一个客户端与Team Server进行通信。首先，简单看下代码。在完成Swing组件的加载后，用户输入用户名、密码等信息后，点击Connect按钮，触发`aggressor.dialogs`下的Connet类的dialogAction方法。如图所示，代码逻辑会将密码传入一个SecureSocket实例的authenticate方法中。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

然后创建数据输出流实例，将`\x00\x00\xbe\xef+ 密码长度 + 密码 + 填充字符`等数据传给Team Server，如果返回`51966（\x00\x00\xco\xfe）`则证明密码正确。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/1_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

查看服务端的代码认证逻辑`(ssl.SecureServerSocket.java)`，发现在密码正确后返回`51966(\x00\x00\xca\xfe)`，密码错误返回`0（\x00\x00\x00\x00）`。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/2_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

通过Wireshark抓包如图所示，可以看到客户端发送的密码及填充字符串。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/3_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

通过以上代码逻辑，可以找到一个识别Cobalt Strike Team Server的方法，流程图及部分代码如下图所示：

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/4_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/5_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

为了利用该特征获取更多资产，我们希望把Cobalt Strike 中被控制的IP给提取出来，就是Cobalt Strike 登陆后的Session Table提取出来，如图所示。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/6_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

同样先看下代码，在通过密码验证后，会创建一个TeamQueue的实例。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

通过查看该类的构造方法，发现在创建该实例的时候，同时启动了两个线程来对TeamQueue中请求和响应进行监控。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/7_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

如图所示，TeamQueue类的call方法中会根据传入的参数实例化一个Request对象,并添加进队列，之后TeamQueue Writer线程从队列获取请求对象，使用socket进行发送。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/8_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/9_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

TeamQueue Reader时刻监听着来自Team Server的响应。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/10_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

以上就是Cobalt Strike客户端发包和接收响应的大致逻辑。在创建TeamQueue实例后开始调用call方法来发送不同阶段的请求。我们进一步抓包分析。如图所示:

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/11_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

结合抓包和查看代码发现客户端与服务端交互的流程如下图所示。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/12_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

在客户端发送aggressor.ready请求后，表示一切准备就绪，开始和服务端进行数据同步，这其中就有session table的数据。根据以上的逻辑，然后手动代码实现这几个请求，就能够在识别出Cobalt Strike后进一步爆破密码，在爆破出密码后提取出目标的受控IP。如图所示。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/13_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

最终的扫描流程图见附录。

**扫描结果分析**
----------

网络空间测绘始于扫描，不止于扫描。在找到该特征后，我们开始在互联网中进行挖掘。

使用搜索语句：`response:"\\x00\\x00\\xca\\xfe" AND port: "50050"`，可以找到存在弱口令的Cobalt Strike，我们只对部分主机进行了受控IP的提取，这步骤稍微敏感，大家可以自行操作。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/14_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/15_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/16_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

随机登录一台如图：

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/17_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

通过搜索语法`response:"\\x00\\x00\\x00\\x00" AND port: "50050" AND service: "http/ssl"`

可以找到没有爆破出密码的Cobalt Strike，可以看到共有5173条扫描记录，1049个IP。

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/18_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

**部分IoC**
---------

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/19_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

**结论**
------

网络空间测绘，始于资产，但不止于资产。

我们认为，主动测绘数据将会与终端行为样本数据、网络流量通信数据一样，是未来网络安全大数据&&威胁情报数据的重要源头。主动测绘数据和基于测绘数据分析后形成的知识将能够极大补充我们的视野，从而开拓出更多的攻击面和领域。更多网络空间测绘领域研究内容，敬请期待~

**附录**
------

![](%E6%B5%85%E6%9E%90Cobalt%20Strike%20Team%20Server%E6%89%AB%E6%8F%8F/20_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)