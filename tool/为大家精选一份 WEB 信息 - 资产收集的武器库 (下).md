> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/PXNcgBwI4KxhshT1fhx-0g)

知己知彼，百战不殆
=========

在 WEB 实战渗透中，信息收集，资产收集至关重要。

所收集到的信息，资产决定了最后成果的产生。

信息收集个人理解更偏向于单一系统下组件，指纹等常规信息的收集，整合。

资产收集则更偏向于针对一个网站，一个公司，一个域名全方面的信息收集，信息资产包括但不限于子域名，app，小程序等。

当然最主要的是找一些不对外公开的线上系统，往往这些系统更容易出现漏洞，也可以拿到很高的奖励或积分。

两者收集的思路不能局限，发散而聚合，特此整合一些优秀的信息收集，资产收集文章，分享出来一起学习大佬们的思路，最终形成自己的收集体系。

**今天分享一些 WEB 信息 / 资产收集的武器库。**

武器库
---

### 1、ARL 资产侦察灯塔系统

```
https://github.com/TophantTechnology/ARL
```

**简介：**

旨在快速侦察与目标关联的互联网资产，构建基础资产信息库。协助甲方安全团队或者渗透测试人员有效侦察和检索资产，发现存在的薄弱点和攻击面。

![](https://mmbiz.qpic.cn/mmbiz_png/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS006Y0J4hxZ0V4l83oRJInqv5cI0icuakfhiaWa0E9Zy09lewqvQmv5Gh1sA/640?wx_fmt=png)

### 2、LangSrcCurise 资产监控系统  

```
https://github.com/LangziFun/LangSrcCurise
```

**简介：**

LangSrcCurise 资产监控系统是一套通过网络搜索引擎监控其下指定域名，并且能进行持续性信息收集整理的自动化资产监控管理系统，基于 Django 开发。

![](https://mmbiz.qpic.cn/mmbiz_png/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS0067qgCYZZhxrxBlmysvVYen7FquOjgUia1Vp9nnam7Nub5JBC92sDIboA/640?wx_fmt=png)

### 3、hawkeye  

```
https://github.com/0xbug/Hawkeye
```

**简介：**

监控 github 代码库，及时发现员工托管公司代码到 GitHub 行为并预警，降低代码泄露风险。

![](https://mmbiz.qpic.cn/mmbiz_png/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS00653icrZA8b7zSnnOS94mf8IBJxKW4wGCR36UMk3dptrnVTMIEzNTlKWQ/640?wx_fmt=png)

### 4、dirsearch  

```
https://github.com/maurosoria/dirsearch
```

**简介：**

Dirsearch 是一个成熟的命令行工具，主要用于探测 WEB 服务器下的敏感文件 / 目录。

**快速使用：**

```
python3 dirsearch.py -u <URL> -e *
-e *：代表探测所有后缀目录文件。也可以指定特定文件后缀，比如：-e php
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS0068ibTTduVFg17DV71Y3SD3r3dy7xGQIhMBcwVbXhVJO5HOXNcBUyicEVg/640?wx_fmt=jpeg)

### 5、JSfinder

```
https://github.com/Threezh1/JSFinder
```

**简介：**

JSFinder 是一款用作快速在网站的 js 文件中提取 URL，子域名的工具。

**快速使用：**

```
python JSFinder.py -u http://www.baidu.com
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS006kMpcy3qA2k3BlLibuq46XWo4DAibwIyH58pyBiab5fNksA1NzHjylxcrA/640?wx_fmt=jpeg)

### 6、Linkfinder

```
https://github.com/GerbenJavado/LinkFinder
```

**简介：**

Linkfinder 基于 python，是一款用于发现 JavaScript 脚本中链接以及敏感参数的工具

**快速使用：**

```
python3 linkfinder.py -i http://www.baidu.com -d
-i：指定url，或者js文件地址
-d：如果只指定域名，则配合-d参数自动枚举js文件
```

![](https://mmbiz.qpic.cn/mmbiz_png/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS006RicBURibHO6d9wbXIiatQcC9GMIHPI6Kk7kH0z9FXTzTaQ8AY3vjTRc5Q/640?wx_fmt=png)

### 7、httpx  

```
https://github.com/projectdiscovery/httpx
```

**简介：**

httpx 可以用于批量检测域名存活性，并且可以根据规则获取响应 title，ip 地址，响应状态码等，具体如下：

**快速使用：**

```
httpx -l 域名列表txt -title -content-length -status-code
```

![](https://mmbiz.qpic.cn/mmbiz_png/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS0068yb9Fs9WFHmgmrVk4gOd1hD8bnibRvUCvojmltt9kL0lEczel7uJ1pg/640?wx_fmt=png)

### 8、MarkInfo  

```
https://github.com/UUUUnotfound/BurpSuite-Extender-MarkInfo
```

**简介：**

一款用于 Burp 标记敏感信息的插件工具

**快速使用：**

```
BurpSuite -> Tab:Extender -> Tab:Extensions -> Add
```

![](https://mmbiz.qpic.cn/mmbiz_png/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS006S5siavRzdUkdTKdZfkGqlic8icriaN3BjNiclS5Jr9B9g2TksP4JAPWaW2g/640?wx_fmt=png)

### 9、白鹿社工字典生成器  

```
链接：https://pan.baidu.com/s/1UDP7QSyenroHQBCgfYD4EA
提取码：wyh3
```

**简介：**

一款可以用于自定义字典的工具

**快速使用：**

![](https://mmbiz.qpic.cn/mmbiz_jpg/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS006v7cLmybWvyntdbLeulF5vXw1c7No1Z7OJFC9zkPHGZQjxZL2wmjY1g/640?wx_fmt=jpeg)

### 10、TheKingOfDuck 的 FuzzDicts  

```
https://github.com/TheKingOfDuck/fuzzDicts
```

**简介：**

Web Pentesting Fuzz 字典, 一个就够了。

**快速使用：**

![](https://mmbiz.qpic.cn/mmbiz_jpg/4CQUZJ9euSyNaTBeoOicicibJsEr4DmS006azyT5ao9ic1seBCPEgiaex7olFr5T75h8qjJv3sshPib4uaIF9oUJbhQA/640?wx_fmt=jpeg)

### 11、网盘在线搜索工具  

```
凌风云：https://www.lingfengyun.com/
蓝菊花：http://www.lanjuhua.com/
大力盘：https://www.dalipan.com/
猪猪盘：http://www.zhuzhupan.com/
PanSou：http://www.pansou.com/
盘飞飞：https://panfeifei.com/
```

### 12、一些在线网站、

```
https://iao.su/2495/
http://www.beianbeian.com/
https://www.dnsdb.io/zh-cn/
https://www.shodan.io/
https://who.is/
https://www.virustotal.com/gui/home/search
https://www.netcraft.com/apps/?r=toolbar
```

玄魂工作室整理。  

渗透路漫漫其修远兮，祝君一路顺畅。