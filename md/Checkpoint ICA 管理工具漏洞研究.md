> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/s44obrBw8kvNQa6dO3Ss0w)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4vsaNtw2cZPyvrb62ooINxy8xdLGUmicBjS7UaiazPaFESiayiau7qIXqjejZOTnUqCjbxYLPgiasTicHw/640?wx_fmt=png)

**0x01 漏洞背景**
-------------

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4vsaNtw2cZPyvrb62ooINxzrHQRZ3z5STrgU4KFFllAIYKVNEL57EsnYuQpsyOE63Oyib9aicre4Hw/640?wx_fmt=png)

今天，我们将分析 Check Point 安全管理模块中的 ICA 管理工具组件里发现的多个漏洞。

ICA 管理工具是管理用户证书的模块，有以下几方面内容：

*   运行搜索
    
*   重新创建 CRLs
    
*   配置 ICA
    
*   删除过期的证书
    

默认情况下此服务是关闭的，需要使用内置实用程序 cpca_client 去开启服务。可以使用下面指令开启

```
cpca_client set_mgmt_tool on -no_ssl

```

需要注意的是：如果运行该命令，那么在匿名条件下可以访问该服务，所以建议仅使用 SSL 运行此服务。开启 ssl 需要执行以下命令

```
cpca_client set_mgmt_tool on -u  [预先生成的证书]

```

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4vsaNtw2cZPyvrb62ooINxGvdiaRHje8PC8icYzTaZib1k2KbUSvib4laZusKxj7RlprNviahXSY0OvibQ/640?wx_fmt=png)

在启用该组件之后，ICA 管理工具可通过 http:// <smartcenter_ip>：18265 / 链接访问其 web 页面， 但在本文的研究环境中选择在不使用 SSL 的情况下启动该组件。  

在分析 ICA 管理工具期间，我们发现了两个漏洞，详情如下。

**0x02 参数注入**
-------------

第一个漏洞类似于命令注入，攻击者可以在给目标应用程序传递参数时插入自定义命令。在研究环境中，我们可以向内部系统命令注入自定义参数并且成功执行。

Web 接口最好用的功能之一是能够向用户发送有关证书初始化的通知，同时保留了修改电子邮件信息的能力，比如发件人，收件人，主题，邮件服务器地址等。最初试图将 shell 命令作为参数注入到邮件服务器地址参数中，比如在输入不正确的情况下利用错误的” ping” 命令，但是很快就确定该命令不能当作 / bin/sh 命令执行。

下一步是找到并研究邮件发送的过程。该服务监听在 18265 上，根据端口和进程之间的关系查询可以大概确定进程名为”cpca”。通过简单的字符串搜索确定了该程序与与 sendmail 进行了交互，并证实了是我们的需要研究的目标。cpca 二进制文件包含字符串” send_mail_file.txt”，这意味着它具有发送附件的功能。必须深入了解 sendmail 的命令行参数才能构造相对应的注入字符串。更多细节查看 sendmail 查询手册。

```
POST /file_init?_ HTTP/1.1
Host: checkpoint.host:18265
Cookie: _
Content-Length: 1

q

cpca crashed after receiving this request.

```

即使这样，也无法推导已执行的命令中参数的顺序，因此必须采用其他利用方式。将 sendmail 的命令行参数成功添加在 Web 界面的参数中：通过日志记录可以确认，在参数注入时指定的服务器文件已发送到攻击者控制的邮件服务器。如果从一开始就分析这里可能会更有效。

要利用此漏洞，使用 nc 监听本地 25 端口（使用本地端口检查漏洞，因为测试网络不允许我们向外部网络发送请求）。然后，在配置 CA 时，将” 管理工具邮件服务器” 的值更改为” 127.0.0.1 -m /etc/shadow％0a％0a”。修改时注意，”\n\n”（不带引号）应出现在字段的末尾。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4vsaNtw2cZPyvrb62ooINxd0JZPnwjbW1h5bODqddUWX2PUEHSp1CbRatUc5CYLXtibgZnotm3IXg/640?wx_fmt=png)

然后，我们发出一个触发电子邮件发送的请求。certs 参数包含状态为” 待定” 的证书 ID。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4vsaNtw2cZPyvrb62ooINxpGJUOCZr2xIIB0HFza5VM76Bos6wBjpEctA2ic4WjVZaxnQwDlG3YPg/640?wx_fmt=png)

如下图所示 / etc/shadow 的内容已发送到 nc 监听的 25 端口。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4vsaNtw2cZPyvrb62ooINx4Z7mGIicMIjXts0QhVB8hg5XqAHOCdpricPChYRAKrH4mx2QIThYOFuA/640?wx_fmt=png)

**0x03 拒绝服务**
-------------

拒绝服务漏洞是由于无法验证输入数据而引起的。如果远程客户端发送了特殊的 POST 请求，该请求的主体以意外的方式格式化，则这将导致程序意外关闭。

我们生成了以下 POST 请求作为 poc：

收到此请求后，cpca 直接崩溃。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4vsaNtw2cZPyvrb62ooINx1OHUDNYsEmbXgyZV5r4bT53oH5v8AKyKrac7MSgoc9XUvta6iapTJZg/640?wx_fmt=png)

**0x04 时间线**
------------

*   2020 年 3 月 16 日 - 向供应商报告了漏洞
    
*   2020 年 3 月 17 日 - 供应商做出回应
    
*   2020 年 3 月 18 日 - 供应商开始进行修复
    
*   2020 年 6 月 4 日 - 修复了漏洞
    
*   2020 年 9 月 24 日 - 分配得到 CVE
    

**译文声明**  

译文仅供参考，具体内容表达以及含义原文为准。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6OLwHohYU7UjX5anusw3ZzxxUKM0Ert9iaakSvib40glppuwsWytjDfiaFx1T25gsIWL5c8c7kicamxw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/Ok4fxxCpBb5ZMeq0JBK8AOH3CVMApDrPvnibHjxDDT1mY2ic8ABv6zWUDq0VxcQ128rL7lxiaQrE1oTmjqInO89xA/640?wx_fmt=gif)  

------------------------------------------------------------------------------------------------------------------------------------------------

  

**戳 “阅读原文” 查看更多内容**