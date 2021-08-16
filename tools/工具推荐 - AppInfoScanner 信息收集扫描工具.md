> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/A55bJS79touBACgfObrAFw)

### 项目地址

https://github.com/kelvinBen/AppInfoScanner

### AppInfoScanner  

一款适用于以 HW 行动 / 红队 / 渗透测试团队为场景的移动端 (Android、iOS、WEB、H5、静态网站) 信息收集扫描工具，可以帮助渗透测试工程师、攻击队成员、红队成员快速收集到移动端或者静态 WEB 站点中关键的资产信息并提供基本的信息输出, 如：Title、Domain、CDN、指纹信息、状态信息等。

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM5PHXR8IHpyHOCto8fwVImbkicJ45ZW6CT7Lh6WuclV1JrGRp7PRYZRzfffValiab1zsFOCa3T4T1xA/640?wx_fmt=png)

### 适用场景

*   日常渗透测试中对 APP 中进行关键资产信息收集，比如 URL 地址、IP 地址、关键字等信息的采集等。
    
*   大型攻防演练场景中对 APP 中进行关键资产信息收集，比如 URL 地址、IP 地址、关键字等信息的采集等。
    
*   对 WEB 网站源代码进行 URL 地址、IP 地址、关键字等信息进行采集等 (可以是开源的代码也可以是右击网页源代码另存为)。
    
*   对 H5 页面进行进行 URL 地址、IP 地址、关键字等信息进行采集等。
    
*   对某个 APP 进行定相信息收集等
    

### 功能介绍:

*   支持目录级别的批量扫描
    
*   支持 DEX、APK、IPA、MACH-O、HTML、JS、Smali、ELF 等文件的信息收集
    
*   支持 APK、IPA、H5 等文件自动下载并进行一键信息收集
    
*   支持自定义请求头、请求报文、请求方法
    
*   支持规则自定义，随心自定义扫描规则
    
*   支持自定义忽略资源文件
    
*   支持自定义配置 Android 壳规则
    
*   支持自定义配置中间件规则
    
*   支持 Android 加固壳、iPA 官方壳的检测
    
*   支持 IP 地址、URL 地址、中间件 (json 组件和 xml 组件) 的信息采集
    
*   支持 Android 对应包名下内容的采集
    
*   支持网络嗅探功能，可以提供基本的信息输出
    
*   支持 Windows 系统、MacOS 系统、*nux 系列的系统
    
*   具备简单的 AI 识别功能，可以快速过滤三方 URL 地址
    
*   指纹识别模块
    
*   添加国际化语言包
    
*   一键对 APK 文件进行自动修复
    
*   识别到壳后自动进行脱壳处理
    

### 环境说明

*   Apk 文件解析需要使用 JAVA 环境, JAVA 版本 1.8 及以下
    
*   Python3 的运行环境
    

### 基本操作指南

##### Android 相关基本操作

*   对本地 APK 文件进行扫描
    

```
python3 app.py android -i  C:\Users\Administrator\Desktop\Demo.apk
```

*   对本地 Dex 文件进行扫描
    

```
python3 app.py android -i  C:\Users\Administrator\Desktop\Demo.dex
```

```
python3 app.py android -i "https://127.0.0.1/Demo.apk"
```

*   对 URL 地址中包含的 APK 文件进行扫描
    

```
python3 app.py ios -i "C:\Users\Administrator\Desktop\Demo.ipa"
```

```
python3 app.py ios -i "C:\Users\Administrator\Desktop\Demo\Payload\Demo.app\Demo"
```

需要注意此处如果 URL 地址过长需要使用双引号 (") 进行包裹

##### iOS 相关基本操作

*   对本地 IPA 文件进行扫描
    

```
python3 app.py ios -i "https://127.0.0.1/Demo.ipa"
```

```
对本地Macho文件进行扫描
```

```
python3 app.py ios -i "C:\Users\Administrator\Desktop\Demo\Payload\Demo.app\Demo"
```

```
对URL地址中包含的IPA文件进行扫描
```

```
python3 app.py ios -i "https://127.0.0.1/Demo.ipa"
```

公众号

最后  

-----

**由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。**

**无害实验室 sec 拥有对此文章的修改和解释权如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经作者允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的**