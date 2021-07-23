> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/IPedDrZv5AcYI1PpE4Gcww)

这是之前 Empire 的一些学习记录笔记，比较基础，有需要的可以看看。大佬可以略过  

一、Empire 简介：

Empire 是一款基于 powershell 的后渗透工具，主要针对 windows 平台，实现了无需 powershell 也可以运行 powershell 代理的功能，内置了很多用于不同渗透场景的利用模块 (内网信息收集、提权、横向移动、权限维持等)，主要用于后渗透中，操作方式与 MSF 类似，程序安装运行在 Linux 系统上。

二、Empire 安装：

①在 github 克隆新版 Empire 项目

```
git clone https://github.com/BC-SECURITY/Empire.git
```

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW4OWZK5WPLQJPJDtic6SaInBBzT4rFMKibmgAP7uL7hyoHXFvoOvpsqEMILaLIibZkAMVD5Ad9RPia0Kg/640?wx_fmt=png)  

②进入 setup 目录，执行安装 Empire 脚本：

```
cd Empire/setup
./install.sh
```

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW4OWZK5WPLQJPJDtic6SaInBCamoBA9D8Gia084EuCItf9dcq4vtsoWBAiadFhicogGPPFJxuvq2gk7iaw/640?wx_fmt=png)

然后就会开始下载安装运行依赖文件，最后设置数据库密码那里可以默认回车，也可以自己设置

**##如果安装途中，遇到网络问题，多次执行./install.sh 文件安装全部依赖，运行主目录下 empire 启动程序前，先执行 setup 目录下的 reset.sh 后再执行主目录 empire 文件**

**##如果启动 empire 时，提示缺少 module，执行以下命令进行安装：**

```
python3 -m pip install iptools
python3 -m pip install netifaces
python3 -m pip install pydispatch
python3 -m pip install pydispatcher
python3 -m pip install zlib_wrapper
python3 -m pip install macholib
python3 -m pip install xlrd
python3 -m pip install xlutils
python3 -m pip install pyminifier
python3 -m pip install dropbox
python3 -m pip install M2Crypto
```

然后执行 reset.sh

```
./reset.sh
```

③安装完成后，启动 Empire

```
./empire
```

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW4OWZK5WPLQJPJDtic6SaInBnibZsKvqCModCUyEFRLa6MQnFNpkVDoJcneaexZ2r4yfJP3qPnsicdfw/640?wx_fmt=png)

启动成功后可以看到当前版本是 3.2.1，有 299 个模块，0 个监听器，0 个会话

**点个赞和在看吧，欢迎转发！**

**点个赞和在看吧，欢迎转发！**

**点个赞和在看吧，欢迎转发！**

![](https://mmbiz.qpic.cn/mmbiz_gif/ehibzaP4CvW5hb2Px7LJVkWEktazM0liacYxsJOVsyUz8lx6MSWyGTmJyJsPsgj9sOSueI5JRuQLTCPW5njR68aA/640?wx_fmt=gif)