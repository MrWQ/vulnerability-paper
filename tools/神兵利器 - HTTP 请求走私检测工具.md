> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/RkMBbZ-UgUUCXsb2g08gpA)

        HTTP 请求走私是一种高危漏洞，是一种攻击者走私模糊的 HTTP 请求以绕过安全控制并获得未经授权的访问以执行恶意活动的技术，该漏洞早在 2005 年就被 watchfire 发现，后来在 2019 年 8 月重新发现由 James Kettle - (albinowax) 发现并在 DEF CON 27 和 Black-Hat USA 上展示，要了解有关此漏洞的更多信息，您可以参考他在 Portswigger 网站上的详细研究博客. 所以这个安全工具背后的想法是检测给定主机的 HRS 漏洞，检测基于给定排列的时间延迟技术，所以要了解更多关于这个工具的信息，我强烈建议你阅读我的博客文章这个工具。

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0Yu4C13Mic6gTictsQIcYkxsjnjtdegN3drPQUvfe0YDFqwoMQrUBPM7TJWbuuNpnYTFIgCgq3uF0A/640?wx_fmt=png)

        该工具是使用 python 编写的，要使用该工具，您必须在本地计算机上安装 python 3.x 版。它接受您需要在文本文件中提供的一个 URL 或 URL 列表的输入，并且通过遵循 HRS 漏洞检测技术，该工具具有内置的有效负载，其中包含大约 37 个排列和检测有效负载的 CL.TE 和 TE.CL 和对于每个给定的主机，它将使用这些有效载荷生成攻击请求对象，并计算收到每个请求的响应后经过的时间并确定漏洞，但大多数情况下它可能是误报，因此确认您可以使用 burp-suite turbo intruder 的漏洞并尝试您的有效载荷。

### 安装

```
git clone https://github.com/anshumanpattnaik/http-request-smuggling.git
cd http-request-smuggling
pip3 install -r requirements.txt
```

```
usage: smuggle.py [-h] [-u URL] [-urls URLS] [-t TIMEOUT] [-m METHOD]
                    [-r RETRY]

HTTP Request Smuggling vulnerability detection tool

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     set the target url
  -urls URLS, --urls URLS
                        set list of target urls, i.e (urls.txt)
  -t TIMEOUT, --timeout TIMEOUT
                        set socket timeout, default - 10
  -m METHOD, --method METHOD
                        set HTTP Methods, i.e (GET or POST), default - POST
  -r RETRY, --retry RETRY
                        set the retry count to re-execute the payload, default
```

### 扫描一个网址

```
python3 smuggle.py -u <URL>
```

### 扫描多个网址  

```
python3 smuggle.py -urls <URLs.txt>
```

```
"detection": [
  {
    "type": "CL.TE",
    "payload": "\r\n1\r\nZ\r\nQ\r\n\r\n",
    "content_length": 5
  },
  {
    "type": "TE.CL",
    "payload": "\r\n0\r\n\r\n\r\nG",
    "content_length": 6
  }
]
```

检测负载需要更改以使其更准确，那么您可以更新检测数组的 payloads.json 文件中的负载。

```
"detection": [
  {
    "type": "CL.TE",
    "payload": "\r\n1\r\nZ\r\nQ\r\n\r\n",
    "content_length": 5
  },
  {
    "type": "TE.CL",
    "payload": "\r\n0\r\n\r\n\r\nG",
    "content_length": 6
  }
]
```

https://github.com/anshumanpattnaik/http-request-smuggling