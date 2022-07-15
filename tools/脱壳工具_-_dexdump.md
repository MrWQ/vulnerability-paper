> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/kHpnRi4yG6d3EAIFNcphHg)

前言
==

        脱壳工具只是帮助我们了解 apk 的一个途径，并不能完整的 dump 出全部的 dex 文件。不能完全的依赖于脱壳工具，但一款好的工具能带我们了解如何脱壳。

工具安装
----

### Frida

**安装过程**

*   第一步，安装 pyhton3(过程略)、pip3.
    
    安装 pip3
    

```
https://pypi.org/project/pip/#files
更新pip
python.exe -m pip install --upgrade pip
```

        使用 pip 安装 frida 模块

```
pip install frida
pip install frida-tools
```

        安装完毕后查看 frida 版本

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGYpKlmenyPt58uibI1K7PRICnzxLguxkKnsAsZaJ9nY5VxKjqjuPqjoQ/640?wx_fmt=gif)

*   第二步：安装 ADB
    
    下载地址：
    

```
https://developer.android.com/studio/releases/platform-tools
```

将 adb 添加进环境变量

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGjsBkhicMFGX86P7S6Lce2gKFibXAhib6AVAjURicYICaCe0zAk7IfBkrGA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGlLBnAeSOYuicgc3gpOIEjZpj0gOmbfEAvqgoewDcsWoicR01yL4kyEJQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGnticgAQEoAtxP4xCHaerH8rKyjP0JtEE34conl7AHQfpHVFEhcxVX1Q/640?wx_fmt=gif)

*   第三步：安装 frida 服务端
    
    首先查看手机版本，根据对应的版本下载对应的 frida
    

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGloicNiaHfyDF1yj41jxKCTCxJL6gPqchX1RU6nKLa7unZibrSjNic21N6w/640?wx_fmt=gif)

        下载对应的版本，下载完毕后解压软件。

```
https://github.com/frida/frida/releases
```

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGRassNJiclWGAC7Q0N5zpeu7h53gqpT0ymEbs0qP66wLj2WRtamj3lTg/640?wx_fmt=gif)

*   第四步：使用 adb 链接模拟器
    

```
adb connect 127.0.0.1:7555
adb devices
```

    利用 adb 的发送功能，将 frida-server 导入到模拟器的 / data/local/tmp 目录下

```
adb push .\frida-server-14.2.18-android-x86_64 /data/local/tmp
```

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGyOHO46hNkkar4o8zY5iamdwLoSQZQ3KFRsJ4XP7hpsHZ4U6aQCCRiccg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGwhgNvE8hYULO9M6W5dfgNXqDXHGxtCMiaMpBfNWPYH756sVKpyvBbyg/640?wx_fmt=gif)

        可以直接运行 frida-server  

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGA7qCdJ0fKZhGHAR1e5qGpj3p4tIEDy0fIEW0MJfIwfURHHp448WIaA/640?wx_fmt=gif)  

        一些 app 有反调试功能，会检查 frida，改变 frida-server 的名字，可以过掉一些反调试。

```
mv frida-server-14.2.18-android-x86_64 f
```

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckG8yes1AeGFkgpTKv6veMc0GU74lTpjEp49pWK5kBicibuehdFqG9A4I1Q/640?wx_fmt=gif)

        一部分反调试还会对端口进行检查，27042 是 frida-server 的默认端口，改掉这个端口也能过掉一些反调试。比如修改到 10000

```
./f -l 0.0.0.0:10000
在外面使用adb进行一次端口转发
adb forward tcp:27042 tcp:10000
```

        利用 frida-dexdump 脱壳

        安装 frida dexdump

```
https://github.com/hluwa/FRIDA-DEXDump
```

        pip 安装模块

```
pip install click
pip install frida-dexdump
```

        安装完毕后打开 frida-dexdump

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckG7Zx0VVp8FLbiagroOUibmAEO5bicjwl4nNC7yoyFkNyz3iaGUlf5yoGttQ/640?wx_fmt=gif)

```
-n:[可选]指定目标进程名，在生成模式下，需要一个应用程序包名。如果没有指定，请使用最前面的应用程序。
-p:[可选]当multiprocess时指定pid。如果没有指定，转储全部。
-f:[可选]使用刷出模式，默认为禁用。
-s:[可选]当刷出模式，在休眠几秒后开始转储工作。默认是10年代。
-d:[可选]启用深度搜索可能会检测到更多的dex，但速度会更慢。
- h:显示帮助。
```

        首先启动 frida，然后打开需要脱壳的 app，这里在商店随便下载了一个 app。

        使用 jadx 打开源码，确实是 360 加固。

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckG934gFe50RImkg0934bFWhFCg6Lc1evpEiazYoKm1ib8t9gU4TfRhlyZA/640?wx_fmt=gif)

        打开 mumu 模拟器，运行需要脱壳的 app。

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGGoayhYMoefVPtHRWHkYxyR1Oiatvos9JVpt2rTYP3aaWO0jJ3ypsKFA/640?wx_fmt=gif)

        在`frida-dexdump`中运行 `python ./main.py打开frida-dexdump`

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckG2WkMsbicccJ1nbW6jxkDDF75IoMibhUCpDPXxdZZyjoYBU0Y7yUx5KzA/640?wx_fmt=gif)

        运行完毕后，在文件夹目录下，生成了很多 dex 文件。

![](https://mmbiz.qpic.cn/mmbiz_png/v6ap3LYR6w9rYibBnCdM1fS0DGJ2NkckGkzdObdzB7rClyQFp7mqkKEphLWazichZfdRV0A3RSyHjOrVIW5Crd8g/640?wx_fmt=gif)

        将 dex 文件拖入 apk 文件中，脱壳就结束了。

总结
--

脱壳工具是很看 "运气" 的，运行后默数三秒，不是成就是败。

这也是加固更新换代的结果，脱壳工具，对于普通的加固，可以应付，但对于企业级加固就无计可施了。

我也不说太多，大家只要知道 frida-dexdump 是通过利用 dex 文件头的特征值，从内存中检索已经加载的 dex 文件即可。