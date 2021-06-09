> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Q8-iGzGYZVc4Dm0F2I8vKw)

**怎样的 APP 是安全的呢？**

只要攻击者所花费的时间成本和精力超过其攻击逆向破解后获取到的收益，那么你的 APP 就相对安全。

对于个人开发者或者某些小企业开发者而言，APP 安全的始终是一件让人非常头疼的事情。下面我以安全开发角度出发，进行梳理了一个 APP 需要关注的 APP 安全的问题 **(没有绝对的安全)。**

主要分为四个方向分别为: 应用安全、组件安全、运行时安全、通信安全。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkZsRRQHaXu64YP4U32szmibRTdwCl77umu4Br4LIl6CJJIjuYu16C7NA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/My1Gumia3SKLeW5YKmZRUj1DicOJWicDUhqMc122V9S8icg9o3WlJxW962Q63Qp26ickjDaDMCCvFZgCc5Gvt1DibBLA/640)

应用安全

![](https://mmbiz.qpic.cn/mmbiz_png/N5gGFPMEm3B6B4eKDcfNt5VFLvBOq8S7oicKicuouHJxltjKNXAiaZs9SYym7mgmx7gkBnKyD2eibkaRJYwoBHwKDw/640)

![](https://mmbiz.qpic.cn/mmbiz_png/hMjlYNLvPyRpUl2m3A1sdiawdLBktzcYbRjdeeXvJtOWbehuJxMOEUK9zxqK8c0PkoxZAVxv4B7PicGMo6sC3OcQ/640)

  

![](https://mmbiz.qpic.cn/mmbiz_png/xicQVVic8TfFvDuZ1oRzgNicaicaRIsA1tE7Csu27FgSnBGgnbZNKdMLVbIwayvdMTA1Is6V3kp0SK7EDGjznOibzeQ/640)

在开发 APP 过程中，不安全的代码编写方式和没有周全考虑到相应的安全性，从而给开发的 APP 带来一定的安全风险，那么应用安全这个最重要的安全需要关注哪些方面？

应用安全主需要关注：二进制安全、敏感数据安全、敏感资源安全、完整性安全、证书存储安全。这五个方面处理的好会一定程度提高 APP 安全性，下面就对这五方面进行做个详细分析。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkHq6hniaEtyKROicVxjVC9fLYibwQicDYrVHIicuG4tE2Ua9PGecQOWH2qZg/640?wx_fmt=png)

  

  

  

二进制安全

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkuKLZEjpRvheZrBUUkEO1swBHZjQhnBRyDjFWvWK8oxwVhQv8Ukbe4g/640?wx_fmt=png)

**1. 环境检测**

**环境检测主要关注点: 模拟器检测、root 检测**。

目前主流的模拟器: 夜神模拟器、雷电模拟器、逍遥模拟器、mumu 模拟器、腾讯手游模拟器。

对模拟器实现原理: 一种基于 Qemu，一种基于 Genymotion(VirtualBox)

**模拟器的检测主要方式: 模拟器的特有文件、模块、特征，代理类等等。**

root: 获取手机超级管理员权限，android 系统是基于 linux 内核，默认情况下并不提供超级管理员权限，所有获取 su 的权限就是所谓 root。

**检测 root 的方式: 特有刷 root 工具的包名称、特有 root 的文件路径。**

**2. 反注入检测**

目前主要的注入: **zygote 属于全局注入 (xposed 工具)、ptrace 单进程注入 (frida 工具)**。

注入的检测方式 (只是检测规则一小部分):

1.  检测 APP 自身的 / proc/%d/maps 模块是否有第三方 so 模块，
    

    2. 优先把自身 ptrace, 那么就其他就无法注入。

下图是个简单的 ptrace 反注入方式。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlk27xBKkbdSGicrp7slFsu2rCHiboqggO6FG08XWnmE5DGCTu4jGniaQanA/640?wx_fmt=png)

**3. 反调试检测**

目前调试工具: jeb、IDA、GDB 等调试工具进行调试分析代码和数据。

反调试方式 (检测规则一小部分):

1.  检测 / proc/%d/status 和 / proc/pid/stat 和 /proc/pid/task/pid/stat 状态值。
    

    2. 检测调速器端口和名称和通信的关键文件信息。

下图是个简单的 tracePid 检测实现

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkYc8SuZV4wC8Ig12rlqcgfzrvYkZU8iaHSib503icb4zJL35uetgIdueiaA/640?wx_fmt=png)

**4. 代理检测**

目前 app 应用面临的严峻问题之一: 数据被抓包分析。

App 目前的抓包流程以 **charles 抓包工具**为例 (http 和 socket)(https 需要安装 SSL 证书): 电脑端上 charles 工具上进行设置代理端口，模拟器或者手机环境，安装 charles 证书，设置代理模式，设置电脑端的 ip 和代理的端口。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkStEIDicd3k6e486ZdxGlH6t4spX77hC5IfAauicBTgwzunayBeG4alwg/640?wx_fmt=png)

对 APP 抓包问题可以检测校验抓包所需要安装的证书信息。

  

  

  

敏感数据安全

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkQYicgnzAlyGWLuJafYuCddk7mANEPsAy6WboQL8qEGkgNz2OWNn6D3g/640?wx_fmt=png)

 **1. 代码中敏感 URL**  

直接将访问的网址或访问的 IP 地址硬编码写到代码中，那么攻击者可以通过反编译 app 进行静态分析 (jeb,jadx,IDA)，搜索 URL 或 IP 相关的信息，那么这些 URL 或 IP 信息就会成为攻击者的一个利用目标。

**2.  APP 中敏感数据**

在 APP 的代码或配置文件中，存储着敏感而且没有进行做加密保护的数据。

攻击者攻击方式有两种

1. 利用 **apktool 反编译 APP** 应用，并进行查看二进制代码数据就能直观的看到敏感的操作调用敏感数据。

2. 通过**代理模式进行抓包**就可以直接抓到 APP 运行中的操作的敏感数据。

**3. 通用加密算法参数**

代码中往往会出现一些保护敏感信息的常量字符串，例如在代码中硬编码 AES 加密的 key、iv 等，或者用户的 VPN 密码等等。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkjNgThNiacJPPWtXJU4ibmHnEYUiaXab2p3ibdzoMpQq0c2P612XOytHwwQ/640?wx_fmt=png)

  

  

  

敏感资源安全

APP 中的一些关键资源文件没有进行加密保护，攻击者可以从 APP 中提取关键的资源文件，进行二次使用或从资源文件中获取本地业务逻辑代码，从而对 APP 发起攻击。例如对 APP 进行关键逻辑篡改，植入恶意代码，网络协议分析等等。

  

  

  

完整性校验

APP 开发者如果没有对开发的 APP 进行做完整性校验的话，那么攻击者用 androidkiller 工具进行对 APP 功能的逆向修改，例如对 app 植入恶意代码，木马、广告等等，那么这些修改 APP 后，并进行重新签名发布，这会导致包的完整性被破坏，那么如果有包完整性校验，校验包被破坏了就进行检验并做对应闪退效果。

  

  

  

证书存储风险

APP 中使用的数字证书可被用来校验服务器的合法身份，以及在于服务器进行做通信的过程中对传输数据进行加解密的运算，保证传输数据的保密性，完整性。

明文存储的数字证书如果被篡改，APP 客户端可能会连接到攻击者的服务器上，导致 APP 的敏感信息被盗取。如果明文证书被盗取，可能会造成传输数据被拦截解密，伪造第三方的 APP 客户端向服务器进行发送请求，篡改服务器中的关键数据或者造成服务器响应异常。

![](https://mmbiz.qpic.cn/mmbiz_png/My1Gumia3SKLeW5YKmZRUj1DicOJWicDUhqMc122V9S8icg9o3WlJxW962Q63Qp26ickjDaDMCCvFZgCc5Gvt1DibBLA/640)

组件安全

![](https://mmbiz.qpic.cn/mmbiz_png/N5gGFPMEm3B6B4eKDcfNt5VFLvBOq8S7oicKicuouHJxltjKNXAiaZs9SYym7mgmx7gkBnKyD2eibkaRJYwoBHwKDw/640)

![](https://mmbiz.qpic.cn/mmbiz_png/hMjlYNLvPyRpUl2m3A1sdiawdLBktzcYbRjdeeXvJtOWbehuJxMOEUK9zxqK8c0PkoxZAVxv4B7PicGMo6sC3OcQ/640)

  

![](https://mmbiz.qpic.cn/mmbiz_png/xicQVVic8TfFvDuZ1oRzgNicaicaRIsA1tE7Csu27FgSnBGgnbZNKdMLVbIwayvdMTA1Is6V3kp0SK7EDGjznOibzeQ/640)

**什么是组件？**

Android 是以组件为单位进行权限声明和生命周期管理。

**组件的作用是什么？**

Android 系统共有四大组件: 活动组件、服务组件、广播组件、内容组件。

Activity(活动组件): 用于展示用户交互的界面，它是最常见的组件。

Service(服务组件): 用于后台运行服务不提供界面展示，常见于监控类应用。

Content Provider(内容组件): 不同的 APP 应用进行数据共享，比如通讯录数据，图片数据。

Broadcast Receiver(广播组件): 用于注册特定的事件，并在其发生时被激活。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkjPGZx0ouxn6rftib8mgW6VBDtleDc4ibKO7uyVyb0OxvgKCibHJLU6Shg/640?wx_fmt=png)

组件安全方面：需要关注四大组件以及第三方 sdk 中的组件安全。如果组件暴露会影响到 APP 应用的逻辑核心和泄露用户敏感信息，这个是很严重安全问题，攻击者只要通过组件利用的方式就可以获取到关键信息，那么就会导致关键信息被泄露的风险。所以在 APP 应用中如果非必要的组件不要进行导出，在 AndroidManifest.xml 文件中, 设置组件的 exported 属性为 false，如果组件一定要提供给外部进行调用的话，可以对组件的权限进行控制。

![](https://mmbiz.qpic.cn/mmbiz_png/My1Gumia3SKLeW5YKmZRUj1DicOJWicDUhqMc122V9S8icg9o3WlJxW962Q63Qp26ickjDaDMCCvFZgCc5Gvt1DibBLA/640)

运行时安全

![](https://mmbiz.qpic.cn/mmbiz_png/N5gGFPMEm3B6B4eKDcfNt5VFLvBOq8S7oicKicuouHJxltjKNXAiaZs9SYym7mgmx7gkBnKyD2eibkaRJYwoBHwKDw/640)

![](https://mmbiz.qpic.cn/mmbiz_png/hMjlYNLvPyRpUl2m3A1sdiawdLBktzcYbRjdeeXvJtOWbehuJxMOEUK9zxqK8c0PkoxZAVxv4B7PicGMo6sC3OcQ/640)

  

![](https://mmbiz.qpic.cn/mmbiz_png/xicQVVic8TfFvDuZ1oRzgNicaicaRIsA1tE7Csu27FgSnBGgnbZNKdMLVbIwayvdMTA1Is6V3kp0SK7EDGjznOibzeQ/640)

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlk5uOzIIuGxKXpJ31zvtYIDK91UibZGNko1N7w3iaF1eYBxbNicFP0ncONQ/640?wx_fmt=png)

  

  

  

日志输出

开发人员在开发调试 APP 过程中, 会进行做一些日志的输出，日志信息往往会记录着一些敏感信息如: 用户名、密码、函数调用栈信息、Token、Cookies、网络请求 IP 或 URL 等等，在发布的 APP 过程中往往会漏掉或者忘记将日志输出的信息进行删除。那么只要用 monitor 工具就可以分成 APP 运行的敏感日志信息。这就给 APP 的安全带来一定的威胁，攻击者通过分析日志信息就可以作为攻击的入口点。

  

  

  

数据存储

APP 运行时候会进行记录或存储一些敏感信息：个人隐私、登录信息、本地验证码、聊天记录等等。

Android 主要有五种数据存储方式: 1. 文件存储、2.SharedPreferences 轻量级存储、3.SQLite 数据库存储、4.ContentProvider 数据共享、5. 网络存储。

从下图的截图中，某个 APP 沙盒目录下的数据存储目录 shared_prefs(SharedPreferences 实现)，该目录主要记录存储一些一些数据量较小的信息。存储的信息直接可以用 MT 管理工具或者直接用 adb 复制传输到外部电脑主机上，再通过可视化工具进行打开查看文件，会造成配置信息或敏感的账号信息泄露。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkNeAptvqy0QjSIpFzwibeRKhzLkZnuribgBMBR4r39aWAHIicPadicU2VYg/640?wx_fmt=png)

配置文件中获取运行环境的 IMEI 值

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkCL6rv5yJdP5ff88CupibN9DdKtlnwzw0DqYJdTQXBF5vu4mK1erMkeA/640?wx_fmt=png)

所以对于运行时的读写操作本地数据存储，在本地操作关键敏感信息，进行用一些加密算法进行做保护，以此提高 APP 运行时数据存储的安全性。

![](https://mmbiz.qpic.cn/mmbiz_png/My1Gumia3SKLeW5YKmZRUj1DicOJWicDUhqMc122V9S8icg9o3WlJxW962Q63Qp26ickjDaDMCCvFZgCc5Gvt1DibBLA/640)

通信安全

![](https://mmbiz.qpic.cn/mmbiz_png/N5gGFPMEm3B6B4eKDcfNt5VFLvBOq8S7oicKicuouHJxltjKNXAiaZs9SYym7mgmx7gkBnKyD2eibkaRJYwoBHwKDw/640)

![](https://mmbiz.qpic.cn/mmbiz_png/hMjlYNLvPyRpUl2m3A1sdiawdLBktzcYbRjdeeXvJtOWbehuJxMOEUK9zxqK8c0PkoxZAVxv4B7PicGMo6sC3OcQ/640)

  

![](https://mmbiz.qpic.cn/mmbiz_png/xicQVVic8TfFvDuZ1oRzgNicaicaRIsA1tE7Csu27FgSnBGgnbZNKdMLVbIwayvdMTA1Is6V3kp0SK7EDGjznOibzeQ/640)

在 APP 通信过程中数据传输协议以及字段数据保护。

以下通过 charles 抓某个 APP 包的检测更新功能性数据包，可以看到抓包的数据看到具体通信的功能，攻击者可以通过对这些包进行分析伪造假的数据包等进行做影响 APP 安全的事情。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr4fbs5TmjLueWRJTRM9kXlkFGRhpzicyvbr3SicbHM1yqBT7beBJoPviawaibibxR9wHEI2EmFALGtyeYg/640?wx_fmt=png)

建议在通信传输功能可以采用 SSL 协议进行传输, 并在客户端和服务端证书信息和关键数据加密和进行校验。加密过程中尽量避免使用 CBC 模式。

![](https://mmbiz.qpic.cn/mmbiz_png/3heAguJrdPwwb5AxgeyO4QBNh18Fn6zdHoLUI5icibB4ibJKHvDsZTm7oBibUMPBk2ccibiawFdUyRsxdwsHjdAVjYuw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3heAguJrdPwFnSZ4ST9beGd5aICibCzeudnBgkU2jxkNicmkoJOqCRpRTuZ66zKQRXahaCXcwyxugx5paBygA1aw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3heAguJrdPzLicKwibCOrj4LSdPHyjzIeCec4cT7TKYicpltRA9sjls9gnl2G8aQ2xxbEMDPklOXS9Qq1PiaWicxcjA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0ldUk3oPhlia2DqOE7MBlRhSZEWM8GQP6oC1FNG5CImW62Wel397icVYqydTs17F2gDBiaancZN3GBJBJMAmPnPBw/640?wx_fmt=png)

点个

![](https://mmbiz.qpic.cn/mmbiz_png/FqwU1eRAibjCDLrwliayiaYtUMl7belPnM4aooRmRo4QBPpciaBGib9Y9vUkUTPQOYmlxw24mnOkSqtq0etz5UFSYbQ/640?wx_fmt=png)

在看

你最好看