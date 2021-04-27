> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247483915&idx=1&sn=5e20c88ba49262aa0236d67650368a10&chksm=eaad8236ddda0b2080534b859089d8d675449b1a62210046d0ec65bdc972a4e6e9045fe283f8&scene=21#wechat_redirect)

目录

Wireshark  

*       Wireshark 的简单使用  
    
*       数据包的过滤
    
*       数据流追踪 
    
*       专家信息说明
    
*       数据包的统计分析 
    
*       导出对象——>HTTP  
    
*       数据包分析过程中的一些小技巧 
    

WireShark
---------

WireShark 只要是学计算机的人应该都听过，也用过。一个非常好用的免费的抓包工具。Wireshark 使用 WinPcap 作为接口，直接与网卡进行数据报文交换。

### Wireshark 的简单使用

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReYsRq51XfFPSD7zkDgic4BKCZBb81iaeiaFsJd2x2vTJQc7mQEGhb0vSjA/640?wx_fmt=png)

双击选择了网卡之后，就开始抓包了

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReK2mJxdwCyunJRfMAa4ELBguOgNkUaBfNrgSYUARTLhhJIVBG58nXzA/640?wx_fmt=png)

停止抓包后，我们可以选择保存抓取到的数据包。文件——> 另存为——> 选择一个存储路径，然后就保存为后缀为 .pcap 格式的文件了，可以双击直接用 wireshark 打开。

### 数据包的过滤

数据包过滤是 wireshark 一个很实用的功能了，通常我们抓包会抓取到网卡通过的所有数据包。很多数据包对于我们来说是没用的，所以我们就需要对其进行过滤。数据包的过滤可以分为 **抓取时过滤** 和 **抓取后的过滤  。**这两种过滤的语法不同！

**抓取时过滤** 

捕获——> 捕获过滤器，这是 wireshark 默认的一些捕获过滤器，我们可以参照他的语法，自己在左下角自己添加或者删除捕获过滤器

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReU0sicbyclWyHj04GYk4254s0wXjD74vGJPoSUnt34WVfRiaFKdr3hYjA/640?wx_fmt=png)

然后如果我们想抓取时对数据包过滤，**捕获——> 选择**，然后选择我们要抓取数据包的网卡，在下面选择我们的过滤器。绿色的话表示语法没有问题，设置好了之后点击开始就可以抓取数据包了

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReibKFYQxrfMWQz3Gsa2eWFX69LtBqapLmbHXQsL0CJYJvDXsU2smkhUA/640?wx_fmt=png) **抓取后的过滤** 

我们一般都是抓取完数据包后进行过滤的，在上方输入我们的过滤语法

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReRARh4JGLsgmR7jTz42LVKA86OCnUhlmjoP6HI1jJUAoRtdwuQgY0qQ/640?wx_fmt=png)

### 数据流追踪 

我们的一个完整的数据流一般都是由很多个包组成的，所以，当我们想查看某条数据包对于的数据流的话，我们就可以：**右键——> 追踪流**，然后就会有 TCP 流、UDP 流、SSL 流、HTTP 流。当你这个数据包是属于哪种流，就可以选择对应的流

![](https://mmbiz.qpic.cn/mmbiz_jpg/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReiaEjjXlpIZmglTnOEl0Xrka3ObYPWMiaflArtj7efDEOywibJkRh1Cy1w/640?wx_fmt=jpeg)

当我们选择了追踪流时，会弹出该流的完整数据流。还有这个数据流中包含的数据包。顶部的过滤器就是该流的过滤规则

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReln7shbDIS1waX25ibkAFZfTlLb9icVoZcv83wLnNFOlDHeXlEVKQRnRQ/640?wx_fmt=png)

###  专家信息说明

功能：可以对数据包中特定的状态进行警告说明。

*   错误 (errors)
    
*   警告 (Warnings)
    
*   标记 (notes)
    
*   对话 (chats)
    

路径：**分析——> 专家信息**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXRe06zibSSlvoJEztH9164xBmx7MHM2ptKwnUOiceGktDMribplVVS740vgw/640?wx_fmt=png)

### 数据包的统计分析 

分析一栏中，可以对抓取的数据包进行进一步的分析，比如抓取的数据包的属性、已解析的地址、协议分级等等。我就不一一列出来了

![](https://mmbiz.qpic.cn/mmbiz_jpg/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReaES0sicwumdyKsEWBTURAa9BhI0THpokjcqeuHzD8w63xCSW8icsnsFw/640?wx_fmt=jpeg)

**已解析的地址** 

功能：统计通信流量中已经解析了的地址

路径：**统计——> 已解析的地址**

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReGMicwvZtbR9HibEptFtOOmvHQN3lwp557o9uODibmv6EvG3MaXP8X2rjA/640?wx_fmt=png)**

**协议分级**

功能：统计通信流量中不同协议占用的百分比

路径：**统计 -> 协议分级**

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXRe0wnpTHSv25UBUklozQZA05RNlth3lCEA9wRqmnscmcM3Fd5wh2rFaA/640?wx_fmt=png)**

**统计摘要说明**

功能：可以对抓取的数据包进行全局统计，统计出包的一些信息

路径：**统计 -> 捕获文件属性** 

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXRe7PjQQLAPO1IWLGR0vSkpLfIJvaf64QFanjRA1MzFcR1bHnLsTPqCoA/640?wx_fmt=png)**

### 导出对象——>HTTP

这个功能点非常有用，他可以查看并且导出 HTTP 流对象，这对于数据包分析非常有用！  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cicIa2iaKFdSNIncOhLKkXReyh8ILkv3jLWjS1fCRiavicDicP68uThic8iadGGIeOl3PzPlv4tNLEWlfbw/640?wx_fmt=png)

### 数据包分析过程中的一些小技巧 

*   大量 404 请求——> 目录扫描
    
*   大量 select....from 关键字请求——>SQL 注入
    
*   连续一个 ip 的多端口请求或多个 ip 的几个相同端口请求——> 端口扫描
    
*   黑客通过爆破账户和密码，则是 post 请求   http.request.method==POST
    
*   黑客修改文件，  ip.addr==219.239.105.18 and http.request.uri matches "edit|upload|modify"  
    
*   如果是用菜刀连接的包，则是 post 请求  ip.addr==219.239.105.18  and  http.request.method==POST
    

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvAKOaVnz60hOe7y3wAHiclddyK53lpEKIQlx4DKOq6EojHibVicgibDB2aQ/640?wx_fmt=gif)

来源：谢公子的博客

责编：浮夸

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)