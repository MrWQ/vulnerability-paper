\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/qjLCgmSPOY0iaF53g7VzMg)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

**所有话题标签：**

[#Web 安全](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1558250808926912513&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#漏洞复现](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1558250808859803651&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#工具使用](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1556485811410419713&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#权限提升](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559100355605544960&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

[#权限维持](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1554692262662619137&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#防护绕过](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1553424967114014720&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#内网安全](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559102220258885633&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#实战案例](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1553386251775492098&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

[#其他笔记](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559102973052567553&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#资源分享](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559103254909796352&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect) [](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559103254909796352&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect) [#MSF](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1570778197200322561&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

 |

**0x01 前言**

本节内容是笔者在以前的渗透测试过程中搜集整理而来，大部分安全防护都有遇到过，只有小部分是找的一些知名安全厂商产品。大家可以根据我整理的这些进程、服务、拦截页以及相关项目快速识别目标机器存在哪些安全防护，然后对其进行针对性免杀处理和绕过测试。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfSyD5Wo2fTiaYRzt5iaWg1GJzhzXutyWbWyQCgkebOobPiaFBNeKyrJh1OJDw4sQgQ4WfsZzCxSGicsQ/640?wx_fmt=png)

**0x02 常见 WAF 进程和服务**

#### (1) D 盾

```
服务名：d\_safe
进程名：D\_Safe\_Manage.exe、d\_manage.exe
```

(2) 云锁  

```
服务端监听端口：5555
服务名：YunSuoAgent/JtAgent（云锁Windows平台代理服务）、YunSuoDaemon/JtDaemon（云锁Windows平台守护服务）
进程名：yunsuo\_agent\_service.exe、yunsuo\_agent\_daemon.exe、PC.exe
```

#### (3) 阿里云盾

```
服务名：Alibaba Security Aegis Detect Service、Alibaba Security Aegis Update Service、AliyunService
进程名：AliYunDun.exe、AliYunDunUpdate.exe、aliyun\_assist\_service.exe
```

#### (4) 腾讯云安全

```
进程名：BaradAgent.exe、sgagent.exe、YDService.exe、YDLive.exe、YDEdr.exe
```

#### (5) 360 主机卫士

```
服务名：QHWafUpdata
进程名：360WebSafe.exe、QHSrv.exe、QHWebshellGuard.exe
```

#### (6) 网站 / 服务器安全狗

```
服务名：SafeDogCloudHelper、Safedog Update Center、SafeDogGuardCenter（服务器安全狗守护中心）
进程名：SafeDogSiteApache.exe、SafeDogSiteIIS.exe、SafeDogTray.exe、SafeDogServerUI.exe、SafeDogGuardCenter.exe、CloudHelper.exe、SafeDogUpdateCenter.exe
```

#### (7) 护卫神 · 入侵防护系统

```
服务名：hws、hwsd、HwsHostEx/HwsHostWebEx（护卫神主机大师服务）
进程名：hws.exe、hwsd.exe、hws\_ui.exe、HwsPanel.exe、HwsHostPanel.exe/HwsHostMaster.exe（护卫神主机大师）
```

#### (8) 网防 G01 政府网站综合防护系统（“云锁” 升级版）

```
服务端监听端口：5555
服务名：YunSuoAgent、YunSuoDaemon（不知是否忘了替换了！）
进程名：gov\_defence\_service.exe、gov\_defence\_daemon.exe
```

****0x03 WAF 识别的相关项目****

#### (1) wafw00f/WhatWaf

利用 wafw00f 识别 WAF，可以在 WAF 指纹目录下自行编写脚本。这类 WAF 识别工具的原理基本都是根据 HTTP 头部信息、状态码以及 WAF 拦截页中的图片、文字做为特征来进行检测，如 wafw00f 工具中的 yunsuo.py 脚本就是根据 cookie 中的 security\_session\_verify 来检测的。

*   /usr/lib/python3/dist-packages/wafw00f/plugins  
    

```
#!/usr/bin/env python

NAME = 'Yunsuo'

def is\_waf(self):
    if self.matchcookie('^security\_session\_verify'):
        return True
    return False
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfSyD5Wo2fTiaYRzt5iaWg1GJWCv6fgRw6rUWB8PLtxzu6Qa4UBwdf3YhBcg0xeCoOymQxq0tEG8NtQ/640?wx_fmt=png)  

#### (2) sqlmap -identify-waf

利用 sqlmap -identify-waf 参数识别 WAF，一样可以在 WAF 指纹目录下根据原有脚本和 Awesome-WAF 项目自行编写 WAF 指纹识别脚本，但有时可能会因为 sqlmap 新老版本的原因而导致存放路径不一样。

*   更新前：/usr/share/sqlmap/waf
    
*   更新后：/usr/share/golismero/tools/sqlmap/waf
    

```
#!/usr/bin/env python

"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import re

from lib.core.enums import HTTP\_HEADER
from lib.core.settings import WAF\_ATTACK\_VECTORS

\_\_product\_\_ = "ModSecurity: Open Source Web Application Firewall (Trustwave)"

def detect(get\_page):
    retval = False

    for vector in WAF\_ATTACK\_VECTORS:
        page, headers, code = get\_page(get=vector)
        retval = code == 501 and re.search(r"Reference #\[0-9A-Fa-f.\]+", page, re.I) is None
        retval |= re.search(r"Mod\_Security|NOYB", headers.get(HTTP\_HEADER.SERVER, ""), re.I) is not None
        if retval:
            break

    return retval
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfSyD5Wo2fTiaYRzt5iaWg1GJfrYHf9XcDNADX3nZhObZJkdWBOLx0btBDCLjkkFV94kjWkbs0ULM4Q/640?wx_fmt=png)  

#### (3) 项目地址

*   https://github.com/sqlmapproject/sqlmap
    
*   https://github.com/EnableSecurity/wafw00f
    
*   https://github.com/Ekultek/WhatWaf
    
*   https://github.com/0xInfection/Awesome-WAF
    

**【往期 TOP5】**

[绕过 CDN 查找真实 IP 方法总结](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484585&idx=1&sn=28a90949e019f9059cf9b48f4d888b2d&chksm=cfa6a0baf8d129ac29061ecee4f459fa8a13d35e68e4d799d5667b1f87dcc76f5bf1604fe5c5&scene=21#wechat_redirect)

[站库分离常规渗透思路总结](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484281&idx=1&sn=4d9fdae999907b222b0890fccb25bbcc&chksm=cfa6a76af8d12e7c366e0d9c4f256ec6ee6322d900d14732b6499e7df1c13435f14238a19b25&scene=21#wechat_redirect)  

[谷歌浏览器插件 - 渗透测试篇](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484374&idx=1&sn=1bd055173debabded6d15b5730cf7062&chksm=cfa6a7c5f8d12ed31a74c48883ab9dfe240d53a1c0c2251f78485d27728935c3ab5360e973d9&scene=21#wechat_redirect)  

[谷歌浏览器插件推荐 - 日常使用篇](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484349&idx=1&sn=879073cc51e95354df3a36d0ed360b62&chksm=cfa6a7aef8d12eb8874da853904847c8c31ff96de4bab3038ce004c92f3b130c36f24c251cc9&scene=21#wechat_redirect)

[绕过 360 安全卫士提权实战案例](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484136&idx=1&sn=8ca3a1ccb4bb7840581364622c633395&chksm=cfa6a6fbf8d12fedb0526351f1c585a2556aa0bc2017eda524b136dd4c016e0ab3cdc5a3f342&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOfSyD5Wo2fTiaYRzt5iaWg1GJ6X5g7wBvlRrvCcGXUd61L5Aia8VREQibSXkfcwicxpAEoAUMFGfKhHuiaA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfSyD5Wo2fTiaYRzt5iaWg1GJk2Cx54PBIoc0Ia3z1yIfeyfUV61mn3skB5bGP3QHicHudVjMEGhqH4A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)  如果对你有所帮助，点个分享、赞、在看呗！![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)