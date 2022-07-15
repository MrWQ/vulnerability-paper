> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ubZIIoRSDIEq_WLKoSckhg)

![](https://mmbiz.qpic.cn/mmbiz_gif/GGOWG0fficjLTMIjhRPrloPMpJ4nXfwsIjLDB23mjUrGc3G8Qwo770yYCQAnyVhPGKiaSgfVu0HKnfhT4v5hSWcQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJBd3VYYdHaibuic2ibICgJtMibl9fJ6SE5hhNG8KRfrL9Jmh9iaRSD9S4C0UI3tdYfZS2CibmFgDMyx1MA/640?wx_fmt=png)

Goby 社区第 15 篇插件分享文章

全文共：3412 字   预计阅读时间：9 分钟

**前言：**站在红队的角度，Goby 是一款优秀的渗透测试工具，特点十分鲜明。在漏洞扫描上，一是设备规则集丰富，目前已支持超过 10 万种设备和业务系统，二是部署方便，可部署在任意单机，无需进行复杂的配置。在漏洞录入上，Goby 自研的漏洞扫描框架由 Golang 语言编写，目前的漏洞录入有两种形式，一是通过 JSON 格式录入漏洞发包和判断的逻辑，二是使用 Golang 代码编写发包和判断逻辑。在漏洞开发上，如果能够引入 Python 环境支持运行 Python 脚本，不仅可以提高开发效率，支持更多通信协议，而且能够以此种方式为模板，同其他工具进行联动，实现漏洞的更有效利用。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **01**

 **插件使用**

**1.1 插件效果**

![](https://mmbiz.qpic.cn/mmbiz_gif/GGOWG0fficjJBd3VYYdHaibuic2ibICgJtMiblkBFz6IPY2lVWCNX0dKnibj0PHMozHKtSeyUcfA01TG8b6lsib62DCyg/640?wx_fmt=gif)

**1.2 使用方法**

**1. 下载插件 PythonCall**

在 Goby 的扩展程序页面，找到 PythonCall，点击下载按钮

**2. 配置 Python 安装路径和存储 Python 脚本的文件夹路径**

在 Goby 的扩展程序页面中，在 “已下载” 标签中找到 PythonCall，点击配置按钮，填入配置信息

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJBd3VYYdHaibuic2ibICgJtMibCkwT9eUI8WR4Jiabmvm4sSyU3NpTSgFibUyRcibJqmGv9lfjDPXt40PeQ/640?wx_fmt=png)

> 注：Windows 系统下，在填写配置信息时，由于转义字符，文件路径需要使用两个反斜

示例：Python 安装路径为`C:\Python3\Python.exe`，存储 Python 脚本的文件夹路径为`C:\exp`

对应的配置信息为：

pythonInstallationPath：`C:\\Python3\\Python.exe`

pythonScriptFolder： `C:\\exp`

**3. 将你的 Python 脚本统一放置在存储 Python 脚本的文件夹中**

每个 Python 脚本的名称需要同漏洞名称保持一致

示例：针对漏洞 CVE-2019-0708 BlueKeep Microsoft Remote Desktop RCE，你需要将 Python 脚本保存至`c:\exp\CVE-2019-0708 BlueKeep Microsoft Remote Desktop RCE.py`

Python 脚本的启动方式：将目标的 url 作为启动参数

注：poctest1.py 的内容为：

```
import os
import sys
if __name__ == "__main__":
    print(sys.argv[1])
    a = input("wait")
```

**4. 单击漏洞相关页面上的 pyexp 按钮**

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **02**

 **插件开发**

**2.1 开发思路**

参考了插件示例中的漏洞列表页 - vulList，点击按钮可以一键调用本地 Metasploit 框架，对漏洞进行检测。

> 漏洞列表页 - vulList：https://cn.gobies.org/docs.html#%E6%BC%8F%E6%B4%9E%E5%88%97%E8%A1%A8%E9%A1%B5-vulList5

结合实际应用场景，简化用户操作，我对代码结构重新进行了设计。  

**2.1.1 漏洞匹配逻辑**

最简单的漏洞匹配方式是建立一个映射，每个漏洞对应一个 Python 脚本。但对于用户来说，如果有多个 Python 脚本，需要逐一建立映射。

为了简化用户操作，使用漏洞名称作为映射规则，每个 Python 脚本使用 Goby 定义的漏洞名称作为命名规则。这样一来，用户只需要设置存储 Python 脚本的文件夹即可。

实现代码：

```
goby.registerCommand('pyexp', function (content) {
        let config = goby.getConfiguration();
        let pythonInstallationPath = config.pythonInstallationPath.default; 
        let pythonScriptFolder = config.pythonScriptFolder.default;              
        let ip = content.hostinfo;

        if (!pythonInstallationPath) return goby.showInformationMessage('Please set the python installation path');
        if (!pythonScriptFolder) return goby.showInformationMessage('Please set the path of the folder where the python scripts are stored');

        let cmd = `${pythonInstallationPath} "${pythonScriptFolder}${content.name}.py" ${ip}`;
        if (os.type() == 'Windows_NT') {
            //windows        
            cp.exec(`start ${cmd}`);
    
        } else if (os.type() == 'Darwin') {
            //mac           
            cp.exec(`osascript -e 'tell application "Terminal" to do script "${cmd}"'`);
        } else if (os.type() == 'Linux') {
            //Linux
            cp.exec(`bash -c "${cmd}"`);
        }
    });
```

**2.1.2 按钮显示逻辑**

实现效果：只在有对应 Python 脚本的漏洞页面显示执行按钮

实现流程：

*   将按钮属性定义为变量 pyexp_visi
    
*   在启动插件时，通过 content.name 读出漏洞名称
    
*   拼接出 Python 脚本的绝对路径
    
*   调用 fs.statSync 判断 Python 脚本是否存在，如果存在，返回 true，显示按钮
    

> 注：判断 Python 脚本是否存在时需要使用同步方法 fs.statSync，获得正确的返回结果。如果使用异步方法 fs.stat，将无法返回正确结果。

实现代码：

```
goby.registerCommand('pyexp_visi', function (content) {

        let config = goby.getConfiguration();
        let pythonScriptFolder = config.pythonScriptFolder.default;
        let sub_str = pythonScriptFolder.substr(pythonScriptFolder.length - 1, 1);
        if (sub_str != '\\') {
            pythonScriptFolder = pythonScriptFolder + "\\";
        }              
        let scriptPath = `${pythonScriptFolder}${content.name}.py`;
        stats = fs.statSync(scriptPath);
        if (stats.isFile() == true) {
            return true;
        }

    });
```

**2.2 开发技巧**  

因为是第一次开发 Goby 插件，记录一下开发过程中需要注意的地方：  

*   extension.js 的语法格式参考 Node.js
    
*   windows 系统由于转义字符，反斜杠需要使用两个反斜杠表示
    
*   图标文件需要使用 png 格式，确保背景透明，否则无法适配不同主题
    
*   操作演示的 gif 文件需要图床地址，可以选择 https://ftp.bmp.ovh/
    
*   做好版本控制，每次更新插件时，package.json 中的 version 需要递增
    
*   默认文档使用英文编写，还需要添加中文翻译文件
    
*   上传插件需要使用 Goby 客户端，登录后进入个人插件管理，选择【新建插件】；若是需要更新插件版本，选择对应插件的【更新插件】即可。
    

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **03**

 **小结**

结合开发文档和插件示例，我们可以很容易的实现自己的想法，扩展 Goby 的能力。后续我会结合实战经验，继续开发一些后渗透插件，分享到社区。

> 插件开发文档及 Goby 开发版下载：  
> 
> https://gobies.org/docs.html

**关于插件开发在 B 站都有详细的教学，欢迎大家到弹幕区合影~**

*   https://www.bilibili.com/video/BV1u54y147PF/
    

  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWfiaAtUngV8rgLh0bIibv9SumD1Y9ZmphGxK9lKiakkOWDp2gRsLjZInPg/640?wx_fmt=png)

**更多插件分享****：**

[• Poc Sir | 可对网站进行一键扫描的 Packer Fuzzer](https://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247484533&idx=1&sn=d770a7a6e38cf5d670ae66898638fb57&chksm=eb87efd5dcf066c3b444db4d5b2e49bebbd8a2c416c962a21110e4ed7acd70892c5219f11cce&token=370089282&lang=zh_CN&scene=21#wechat_redirect)  

[• go0p | 可调用 Goby API 进行漏洞检测的 Goby_exp](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247496358&idx=1&sn=9eb86bdd2264226a4d17b344e3ffa763&chksm=eb841906dcf390106ead03c45859a4fba51f3bb4438e038d411a715517e423b191c9c39bbdb0&scene=21#wechat_redirect)

[• zhzyker | 可进行 Web 漏洞扫描和验证的 vulmap](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247496678&idx=1&sn=582294d705e2713ade8dd4313500c581&chksm=eb841846dcf39150803b09c3480a6dda82bd8f2911bf2f84d3cd4d8b75c995940cd4a35c20f3&scene=21#wechat_redirect)

[• h1ei1 | 如何快速上手 Zookeeper 未授权漏洞](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247500596&idx=1&sn=5b6a054f6987ced13e10315cb276b119&chksm=eb842894dcf3a18218741d0758af985f83a95c078e06b77bade0c0fdc08660ea664d8350fecf&scene=21#wechat_redirect)

[• 蜉蝣 | 可进行 Web 路径爆破的 Dirsearch](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247500656&idx=1&sn=52271e3fb524219e56f7a179f0e0042c&chksm=eb8428d0dcf3a1c627812a7937452ad1fb9a0d714c30b4a7d1eb09a980f060100f08ada5e135&scene=21#wechat_redirect)

更多 >>  插件分享  

如果表哥 / 表姐也想把自己上交给社区（获取红队专版）![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKEYyZh6YMicl2K5TDD26xJiaXMwReBoEFfWYSRkOGBMzrZ3VpbKu1DtFLprCibCrsuX3QlGJLMG79jg/640?wx_fmt=png)，戳这里领取一份插件任务？

> https://github.com/gobysec/GobyExtension/projects

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjI0MU6swxULP64s6OqQibfFqsCfmxP8BD4kzLf0ZVg9oroXxhbvDBmbHs7mDkKaTfv88fv3giac5r0A/640?wx_fmt=png)