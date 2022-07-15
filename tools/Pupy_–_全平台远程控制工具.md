> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/llYPZVtSoc28zw8MgE5QOw)

项目地址
----

https://github.com/n1nj4sec/pupy

项目简介
----

Pupy 是一个使用 python 编写并且开源的全平台远程控制工具，其客户端支持 Linux,Android,Windows,Osx 系统，并且提供多个利用模块, 用户也可以自己写模块，比如编写一个 D0ss 模块

安装方法
----

**安装**

需要 python 版本 >=2.7

> git clone –recursive git://github.com/n1nj4sec/pupy.git pupy  
> pip install -r requirements.txt

默认 clone 的时候是不带 payload_template 的，需要去其项目中单独下载

将 https://github.com/n1nj4sec/pupy-binaries/tree/0a95af476b4f5faf1a217ccf5badec2f3e762da9

这里的内容下载并放入 /pupy/payload_template 目录下即可。

**生成客户端**

其 windows 客户端支持下列类型：

> {exe_x86,exe_x64,dll_x86,dll_x64}

生成方法：

> ./pupygen.py -t exe_x86 simple –host 192.168.2.131:443 #Windows 客户端
> 
> ./pupygen.py -t apk simple –host 192.168.2.131:443 ＃安卓客户端

若需要生成 linux/osx 客户端，需要修改 **pp.py** 中的配置为你的主机地址即可

> LAUNCHER=”simple” # the default launcher to start when no argv  
> LAUNCHER_ARGS=shlex.split(“–host 127.0.0.1:443 –transport tcp_ssl”) # default launcher arguments

然后在 linux/osx 下安装 pyinstaller 模块将其打包成二进制文件。

> pyinstaller –onefile /full_path/pupy/pupy/pp.py

![](http://mmbiz.qpic.cn/mmbiz/cuBLf97ic7tycll83wStrCG2z0tDyauIVOW9rX0FLYia2W1hS132vxXR5DXlETBSAc5gmw7lTtNaVLCWAreSjt7Q/640?wx_fmt=jpeg)