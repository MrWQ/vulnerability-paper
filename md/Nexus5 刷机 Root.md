> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/V3wwwGqKH4hBFLOQ3ojlXA)

Nexus 5 刷机
==========

一、检查手机是否解锁
----------

电脑有 adb，手机开启开发者模式，有 USB 调试

> adb reboot bootloader

或者在关机状态下，按住开机键和音量下键进入 bootloader 模式

如果未解锁请继续，解锁请跳到第二节 查看刷机过程

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFw5TYKweCwLicPeQwZum8YxwnXpKib592mLSfzD1ibJTLaNdbbrAAFkjldw/640?wx_fmt=png)

1.  首先在手机上打开开发者模式，然后打开 USB 调试
    
2.  进入到 bootloader 模式（参考上面的命令）
    
3.  打开命令行，输入`fastboot flashing unlock`
    
4.  然后选择`YES` 按`电源键`确认
    

二 、刷机
-----

刷机前先做一些准备

### 下载刷机工具

电脑没有 adb 工具的请下载（配置 adb 环境的忽略）

https://github.com/eseGithub/AndroidTools/blob/master/platform-tools.zip

### 下载官方的系统镜像文件

> https://developers.google.com/android/images

### 修改 boot.img 中的 ro.debuggable 属性

> 一个进程是否可以调试是由进程启动时候的参数决定的；普通的 App 进程如果是 debug keystore 默认是可以调试的，又或者你在 AndroidManifest 里面指定 debuggable 为 true 也是可以调试的。对系统进程，我们只有采取系统级别的手段：让整个系统可以调试——debug 版或者编译参数 debuggable 为 1 的系统。解决这个办法很简单：使用模拟器（真机也行，限 Nexus 系列刷原生 Android 系统，把系统启动的 debuggable 参数修改为 1）

为了后面可以更好的调试 APP ，这里我们需要修改 debuggable 属性，如果没有刷入 debuggable=1 属性，也可以使用 xposed 模块来完成相同的功能

将 nexus 5 的系统镜像解压，

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwafbs5mqm4qcWtjjLsbHn8MmL3f8YeKoLDQXThlhw9UuWVPjfdXOuaQ/640?wx_fmt=png)

在压缩文件中提取出 boot.img

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwC4cITmIuFOyAibqqHo4SWyL5f9NicVeXqlEicluzey2Npy7g90IqMOvcw/640?wx_fmt=png)

并拷贝到 booting.exe 所在目录

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwB1JAqMkBHr5kJOgUOlwiap24YJuQMFz3zicFJfUIm53P0a2icDOR2XJoQ/640?wx_fmt=png)

打开 cmd 命令环境，执行`bootimg.exe --unpack-bootimg` 命令对 boot.img 文件进行解压处理 （注意：存放的路径不要有中文，否则会报错）

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwkgdLp1hAxRbAMRs5fpcF2mUuZMnHROSLg7xMJV5oCgoIHRLdhr5K1w/640?wx_fmt=png)

找到`initrd`文件夹下找到`default.prop`文件，修改文件中的`ro.debuggable=0` 改为`ro.debuggable=1`，记得保存

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwKk6RFv43MHLTco1OLlCt2lCr53rctYYtDavUKHUM8klw8UEGrZQEcg/640?wx_fmt=png)

然后在 cmd 命令行执行`booting.exe --repack-bootimg`, 解压的文件夹会重新打包为新的 img 文件，

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwdjOWbmEv3iaHm3W85JLicONj4pLEBiazLGngJMdN23H9WlvY8o8JDXltA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwODSKYRjGQXlUrQYSSevMuewCib0NsKRAPRtcico4N6KAiafEvK4WU5uog/640?wx_fmt=png)

将`boot-new.img`改名为`boot.img`，放回原来的压缩包里，替换原压缩包的 boot.img 文件

### 刷入镜像

将下载的刷机工具和镜像放到同一个文件夹（有 adb 环境的忽略）

然后进入 bootloader  `adb.exe reboot-bootloader` 或 关机状态下，电源键加音量下键不放，知道进入 fastboot mode 模式（机器人）

运行 flash-all.bat 命令开始刷机，刷机成功后会重启进入桌面

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwnGJbRkQbFVkJRR85qRgQjT8La79LTvykQTFhlmuVVQJaAQiclrIkISg/640?wx_fmt=png)

#### 注意：这里如果遇到无限重启

1.  先按住关机键强行关机
    
2.  按住音量减键，然后按关机键，就会进入 bootloader
    
3.  解压镜像包中的 zip 文件
    

```
fastboot erase cache
fastboot erase userdata
fastboot erase boot
fastboot erase cache
fastboot erase recovery
fastboot erase system

fastboot flash bootloader bootloader-hammerhead-hhz20h.img (修改为对应的img)
fastboot reboot-bootloader

fastboot flash radio radio-hammerhead-m8974a-2.0.50.2.30.img (修改为对应的img)
fastboot reboot-bootloader

fastboot flash recovery recovery.img
fastboot flash boot boot.img
fastboot flash system system.img
fastboot flash cache cache.img
fastboot flash userdata userdata.img
```

> 无限重启解决方案：建议手动清除各个分区，并且手动刷各个分区 image

4.  重启手机
    

我们来验证一下 debug 模式是否成功，打开工具 ddms

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFw2mCqicBPxDick2bZB01F48KBIoOTZnJHXXJjOEuachib1vGh37sUA0jEQ/640?wx_fmt=png)

### Root

不需要刷 twrp ，直接使用 CT-Auto-Root 的工具包，操作步骤简单，无需替换内核

下载地址：https://download.chainfire.eu/363/CF-Root/CF-Auto-Root/CF-Auto-Root-hammerhead-hammerhead-nexus5.zip

解压下载 zip 文件

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFw3qRYdq3AbV3xL76frxibEmYThUjNvnricSLwKYkVmDfQlq91XG4CIBQw/640?wx_fmt=png)

手机进去 Fast boot Mode 模式 (手机关机状态，电源键加音量下键)

执行`root-windows.bat`

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6wicBzr6vhBAqsR4alKmCUBFwV4YszXI61EVic6L1iag8LhVJfaHv18dnWic7sPz1LJT81FibTaqupZUOFA/640?wx_fmt=png)

屏幕会出现一个红色 Android 机器人，此乃正常现象，无需担心

机器重启后，Nexus5 会获得 Root 权限，并自动安装 SuperSU 权限管理软件

持续更新 Android 安全、web 安全等原创文章，需要学习资料，技术交流可以关注我一起学习