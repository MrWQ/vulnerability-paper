> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/TWeWWPl28VwMLxBSPj1LFw)

**文末获取 SRC 漏洞挖掘技术文档合集哦**
------------------------

**前言**
------

**输出这篇文章的目的也是为了好多人在挖洞时，看到别的大佬钱拿的不要不要的时候，只能在我们自己自己电脑面前一筹莫展，这篇文章也是为了带大家打开新的思路。** 

**俗话说得好，“不是你套路不够深，是你的基础不够扎实。”**

**第一步：选择一条不拥挤的道路**
------------------

现在类似于漏洞盒子，补天这种平台企业 SRC 的开展，同时伴随着各个公司私有 SRC 挨个上线，我们可以讲目光聚焦到他们身上。

基础不扎实，如 SQL 注入，XSS，上传，稍微大一点的厂商，一个 WAF 就打死了一群工具小子，这里我暂且不谈，直接放弃，来选择扫描器无法的发现漏洞。

如果想挖洞赚钱，只有 2 条路：

> 1. 客户端漏洞
> 
> 这样的漏洞挖掘竞争的人会比常见 web 漏洞和主机端口漏洞少不少。
> 
> 2. 子域名下漏洞
> 
> 主要讲的是一些边缘业务或者是刚上线的业务。

**第二步：信息收集**
------------

老生常谈的一个东西了，举个简单的例子，像一些用户比较多的软件，一旦出现漏洞，影响的用户量是相当巨大的。

比如 struts 漏洞，这些框架漏洞也出了很久了吧，还是有人喜欢用它。

不管你去谷歌还是 bing 然后采集一波该特征的 URL，扔到这个批量验证工具里面，仍然存在大把的 ip 存在 struts 命令执行漏洞。

这就是信息收集的成功因素的之一，更何况，现在还有钟馗之眼，傻蛋，fofa 这些平台 API 的开放，无时无刻不在帮我们做着信息收集的工作，让我们多了一把更锋利的武器。

以上是废话，我们不赘诉了。

再谈谈 SRC，举个简单的例子，SRC 他们在平台上只声明了大致方向，只要属于他们的业务漏洞都收。

那么我们如何定位呢。

我的思路：

> 1. 他的域名对应的真实 IP，对应的 C 段，甚至 B 段；
> 
> 2. 他的子域名；
> 
> 3. 其他平台（如 hackerone）。

如:

https://hackerone.com/alibaba

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBicAiavrVP189Ecq9ojS3vSz7iaYSO4wibdX3RXRXJYmb0HDuMibkB9E19Hw/640?wx_fmt=jpeg)

梦寐以求的目标范围，只要去国外的漏洞网站就能轻轻松松看到。惊不惊喜，意不意外？

查找子域名的文章太多太多，这里也不讲太多了。

当然也可以收集 QQ 群，微信讨论组，暗网的信息然后去提交威胁情报。

**第三步：局部性挖掘**
-------------

这里就针对目标 SRC 的资产做一个收集。

以补天的专属为例：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBWuP2GqxTIviaL060R95ax9NpPzfLariaR3IAriaTS96Nod2DCuykJDibUA/640?wx_fmt=jpeg)

给了我们非常少的范围：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBXXl1nndr2VK2urafIeg1Q5VQqwiboia5pF3gmpaKsibfPpqrcFQQUFXzg/640?wx_fmt=jpeg)

我们先 whois 查询一下：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBB9IKMw23xZxSP5td3x7H8azL64ZeJz0icmwjkpAY1ZNmw99Fj8rw6eA/640?wx_fmt=jpeg)

然后反查：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrB81PB7V73cgG2icVAWSCqUC2o0mmSs1LKS9I55hU3Wu3ekl78nUzjEicQ/640?wx_fmt=jpeg)

查到该公司对应的域名。

这里可以收集顶级域名，然后通过子域名挖掘工具获取二级及三级域名。

李姐姐的神器：https://github.com/lijiejie/subDomainsBrute

高并发 DNS 暴力枚举，发现其他工具无法探测到的域名：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBftCjSUdMDRXaXO7hhBiaqdFxM92M2xjEKwwIq8Z8BiaJ1fTxhyczLoibA/640?wx_fmt=jpeg)效果：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBK1uvBpFCAunWibKMqREnqjlgT0e9tXNT2G6ApYxw1EibNtBHpDXhJibQA/640?wx_fmt=jpeg)

或者在线版的：

https://phpinfo.me/domain/

![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBcP8kHsicrictEgdCZmWBnckcNYxCS57B1L1WIcPqXiargg9e929HOibzsg/640?wx_fmt=jpeg)

利用下面的脚本处理结果：

```
#coding=utf8import reimport osdef getlist():    filename = raw_input('filename')    print filename    ft = open("url.txt",'w+')    with open(str(filename), 'r') as f:         lines = [line.strip() for line in f.readlines()]         for x in lines:            lists=x.split('-')            result = lists[1]            ft.write(result+'\n')            print resultgetlist()print 'done'
```

删除重复项：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBT3cN7gicKCPQhwUjhgsAicZerwXKAtk2OGC1d662TTZ7L1iavxZEkm4AA/640?wx_fmt=jpeg)

上面 2 个方法分别导出的结果如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBHZo2NcPyyIlxLuXWRAeqsDe8at00xbIKQVzXtJbZ80d7ia6ZrpfHTmA/640?wx_fmt=jpeg)这里就回答了好多人经常问我的，为啥子域名挖掘工具要用那么多，因为你用的越多，你收集的越全面。

大部分大公司基本都是整个 C 段买下来，这里因为这里的目标使用的是代理商，所以我没有跑 C 段，不然资产可以爆炸多，包大家挖洞挖到眼泪流下来。

**第三步：处理收集到的信息**
----------------

把筛选出来的 ip 保存到 url.txt，然后使⽤ nmap 命令将结果输出为. gnmp ⽂件：

```
nmap -sS -p 80,443,8080 -Pn -iL url.txt -oA [绝对路径]
```

我用的命令是：

```
nmap -sS -O -sV -iL url.txt -p 80,8080,443 -v -T4 -Pn -oA C:\Users\Administrator.DESKTOP-0MHPHKA\Desktop\result
```

再使用 python 转化为 xsl 格式：

```
#coding:utf8import syslog = open("result.gnmap","r")xls = open("output.csv","a")xls.write("IP,port,status,protocol,service,version\n")for line in log.readlines(): if line.startswith("#") or line.endswith("Status: Up\n"): continue result = line.split(" ") #print result host = result[0].split(" ")[1] #print host port_info = result[1].split("/, ") #print port_info port_info[0] = port_info[0].strip("Ports: ") #print port_info[0] for i in port_info: j = i.split("/") #print j output = host + "," + j[0] + "," + j[1] + "," + j[2] + ","+ j[4] + "," + j[6] + "\n" xls.write(output)
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBGHOJexnDGlibe3sSM7lAW5QgZp7oeZibzuvg4iaQlE1iaZU3FWPQeTibibOg/640?wx_fmt=jpeg)

然后本地搭建一个 php 环境，写一个 url 跳转代码：

```
<?php $url = $_GET['url']; Header("Location:$url"); ?>
```

抓包：

```
GET /url.php?url=http://1.1.1.1:80 HTTP/1.1Host: 127.0.0.1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBGIR5p03JXyfSDJVKZeMTkDIDX51C3TndcexJick0k4Km1VDNXddtqhw/640?wx_fmt=jpeg)![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrB8nHhVGqAnA8W8kKnibnFyJjgus9iaOtdC7bV5SiaHTlLQs8hFskcSciaibw/640?wx_fmt=jpeg)

burpsuite 跑结果：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBMmz38d6Uicbz6Qib7BYDxaibUm0Ye1fUwS43tYwHNZ6ib9rzTsZjTcDxzg/640?wx_fmt=jpeg)

全文不涉及敏感信息，就不打码了。

**第四步：结束语**
-----------

献给所有在挖洞道路走的越来越远的兄弟们。

本文脚本已全部上传 github：https://github.com/tangxiaofeng7/SRCinformation-gathering。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibseuBE3vpiazgy4oHZicgzrBia0Jeo5lWf6wIu6jjmOkt3T6SaJayGIa1hkqM0MUP5VO7pC6dnOcvzA/640?wx_fmt=jpeg)

文章参考:

[https://mp.weixin.qq.com/s/yl1LgC_DHPJtaWh92va_Vw](https://mp.weixin.qq.com/s?__biz=MzUzNzAzNzUzMA==&mid=2247483675&idx=1&sn=3d747238798e8b2162375a97398825b0&scene=21#wechat_redirect)

https://blog.csdn.net/qq_21405949/article/details/78487062

**本文作者：zhukaiang7，**转载**于 FreeBuf。**

**END**

**关注公众号: HACK 之道**  

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3qL1R1NCVbY1ElanNngBlMTUKUibAUoQNQuufs7QibuMXoBHX5ibneNiasMzdthUAficktvRzexoRTXuw/640?wx_fmt=jpeg)

回复：**src**，获取下载链接