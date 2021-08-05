> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/oA_ttVzOpNIfcUjz3daFmg)

![](https://mmbiz.qpic.cn/mmbiz_gif/YTZvSeuD5nIeohKxjibV27ic9ONIUUAZTVQgy0j2daDSYpxic2KsqxWRtxAdSvxrXTebxA1AzwsUWzYOGDIzlgCpA/640?wx_fmt=gif)

**作者：风起 @知道创宇 404 实验室**

**时间：2021** **年 7 月 28 日**

**项目地址：https://github.com/knownsec/Kunyu**

0x00 介绍

**工具介绍**

Kunyu (坤舆)，名字取自 <坤舆万国全图> ，测绘实际上是一个地理信息相关的专业学科，针对海里的、陆地的、天上的地理信息进行盘点。同样应用于网络空间，发现未知、脆弱的资产也是如此，更像是一张网络空间地图，用来全面描述和展示网络空间资产、网络空间各要素及要素之间关系，以及网络空间和现实空间的映射关系。所以我认为 “坤舆” 还是比较贴合这个概念的。

Kunyu(坤舆)，是一款基于 ZoomEye API 开发的信息收集工具，旨在让企业资产收集更高效，使更多的安全从业者了解、使用网络空间资源测绘技术。

**应用场景**  

对于 kunyu 的使用，应用场景可以有很多，例如：

• 企业内遗忘的，孤立的资产进行识别并加入安全管理。

• 企业外部暴露资产进行快速排查，统计。

• 红蓝对抗相关需求使用，对捕获 IP 进行批量检查。

• 批量收集脆弱资产 (0day/1day) 影响内的设备、终端。

• 新型网络犯罪涉案站点信息进行快速收集，合并，进行更高效的研判、分析。

• 对互联网上受相关漏洞影响的脆弱资产，进行统计、复现。

•.......

 ![](http://wx.qlogo.cn/finderhead/PiajxSqBRaEJ6RrNWsWsDOdo8rrB5tIVplNUzTtfNsCrX1pyU6fYHWA/0) **黑哥说安全** Kunyu(坤舆) - 更高效的企业资产收集 by 风起 @知道创宇 404 实验室 https://paper.seebug.org/1654/ #ZoomEye 视频号

0x01 安装

**需要 Python3 以上的支持**

```
git clone https://github.com/knownsec/Kunyu.git
tar -xvf Kunyu.tar
cd Kunyu
pip3 install -r requirements.txt

Linux:
    python3 setup.py install
    kunyu console

Windows:
    cd kunyu
    python3 console.py
```

0x02 配置说明

在第一次运行程序时通过输入以下命令进行初始化操作，提供了其他登录方式，但是推荐使用 API 的方式，因为用户名 / 密码登录需要额外做一次请求，所以理论上 API 的方式会更加高效。

```
kunyu init --apikey <your zoomeye key> --seebug <your seebug key>
```

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBQ27qK49T2VtHbOMMTlZgiasBjjhft8VictN8Gdj29EKngGxIrdwEuQzw/640?wx_fmt=png)

0x03 工具使用

**命令详解**

```
kunyu console
```

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwB1Re13vjm17r41j3uibQick0tOLe7eHv6vOe16XW6cUb6nXNDJKaErvAQ/640?wx_fmt=png)

**ZoomEye**

```
Global commands:
       info                                    Print User info
       SearchHost <query>                      Basic Host search
       SearchWeb <query>                       Basic Web search
       SearchIcon <File>/<URL>                 Icon Image search
       SearchBatch <File>                      Batch search Host
       SearchCert <Domain>                     SSL certificate Search
       SearchDomain <Domain>                   Domain name associated/subdomain search
       Seebug <Query>                          Search Seebug vulnerability information
       set <Option>                            Set arguments values
       ExportPath                              Returns the path of the output file
       clear                                   Clear the console screen
       show                                    Show can set options
       help                                    Print Help info
       exit                                    Exit KunYu &
```

**OPTIONS**

```
ZoomEye:
    page <Number>    查询返回页数(默认查询一页，每页20条数据)
    dtype <0/1>      查询关联域名/子域名(设置0为查询关联域名，反之为子域名)
    btype <host/web> 设置批量查询的API接口(默认为HOST)
```

****使用案例****

这里我们使用 ZoomEye 模块进行演示

用户信息

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwB7XV9a61zHgK3WLe1qBwH6CNRty29fctCT0hZ7ZuC4uTzib4uSjGXicGw/640?wx_fmt=png)

HOST 主机搜索

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBltQmib9X14oTGpHIPqMB1icykE3EMl1VbZcic3ibgTcDlz0VibrGJ7ibNuZg/640?wx_fmt=png)

Web 主机搜索

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwB9Kqsrroo9KpLtzk4UfspZVYDgXLhfckpmia7wluTQPicx2nTV5PtR6cQ/640?wx_fmt=png)

批量 IP 搜索

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBBWPylJDeLLQzgibqib72wCiaoGOFIyf4icZqPlJXFQQjXM3b3JzXhK2mxQ/640?wx_fmt=png)

Icon 搜索

在搜集企业资产时，我们可以使用这样的方式进行检索相同 ico 图标资产，在关联相关企业资产时，通常会有不错的效果。但是需要注意的是如果某些站点也使用这个 ico 图标，可能会关联出无关资产 (但是无聊用别人 ico 图标的人总归是少数吧)。支持 url 或本地文件的方式搜索。

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBTJh8zjrcyhfIiabogibomoZUC84d56UA8VxBwMicoLr1aEyurLxm9wApg/640?wx_fmt=png)

SSL 证书搜索

通过 SSL 证书的序列号进行查询，这样关联出来的资产较为精准，能搜索出使用相同证书的服务。碰到 https 站点时，可以通过这样的方式。

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBJLAprOudtM5OrsXibR23qb2bibPWEnYOiccicZeb4IylgcZjMmwStfNCyA/640?wx_fmt=png)

关联域名 / 子域名搜索

对关联域名以及子域名进行搜索，默认查询关联域名，可以通过设置 dtype 参数设置两种模式。

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwB3zV9iaGoLUbGqbP7DwiaicwThONX1cZTDbBppWtj3YdiaPlpae9Ma9IpPQ/640?wx_fmt=png)

Seebug 漏洞查询

通过输入想要查找的框架、设备等信息，查询历史相关漏洞，但是需要注意仅支持英文，这里后期会进行改进，升级。

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBbtMX2GMtdk8dzVPN12E3iaD3MDeqiaPnBAU6gx6wh6iak6bq2wcQT3ZTA/640?wx_fmt=png)

设置参数

当设置 set page = 2 时，返回结果为 40 条，大家可以通过修改 page 参数，设置查询的页数，需要注意 1 page = 20 / 条 ，可以根据需求修改该值，获取更多返回结果。

通过 show 显示可配置的参数，以及参数当前的值。

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBnODflFPtrYnQfLlRc0cOQyV4uzLpZv7Oib0HJouexAJIL016SWcnBBQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBorlRyyH7aiaibZZlZCicechUDRLiblzmKSY0a6g68wBr7HehrIicFu66t6A/640?wx_fmt=png)

数据结果

搜索的所有结果都保存在用户根目录下，并根据当前时间戳创建目录。单次启动的所有查询结果都在一个目录下，保存为 Excel 格式，给予更加直观的体验。可以通过 ExportPath 命令返回输出路径。

![](https://mmbiz.qpic.cn/mmbiz_png/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwB4cR3kNlgx4Y52K6lWddOXTtAp3LicdTSRJDe6jDLlB5PziaFialbDNHiag/640?wx_fmt=png)

0x04 Loading

其实还有很多的思路，但是作为 Alpha 版本先这样，后期会不断进行完善的，希望 Kunyu (坤舆) 能够让更多安全从业者所知，谢谢各位的支持。  

工具框架有参考昆仑镜、Pocsuite3，都是非常棒的作品。

感谢 KnownSec 404 Team 的全体小伙伴。

> “看得清” 是能力的体现，是 “ 器 ” ，而 “ 看得见 ” 就是思想的体现，那最后关联的是 “ 道 ”。
> 
> --SuperHei

0x05 Issue

**1、多因素搜索**

ZoomEye 搜索可以使用多因素搜索，dork：cisco +port:80(注意空格) 可以搜索符合 cisco 以及 port:80 条件的所有数据，如果没有中间的空格则为同一搜索条件，则为满足 cisco 并且端口为 80 的所有数据。Kunyu 的 dork 无需引号。

**2、高精地理位置**

ZoomEye 给予特权用户高精地理位置的数据，但是需要注意的是普通用户，则不具备该功能，望周知。

**3、用户名 / 密码登录**

如果您使用的是 username/password 作为初始化条件，那么所获得 token 时效为 12 小时，如果发现您的搜索不能返回数据，那么不妨 info 一下，如果会话超时则会返回初始化命令提示。绝大多数情况下我们建议您使用 API KEY 的方式，则不存在失效问题。这样的设计也是为了您账号密码的安全性，毕竟 API KEY 可以重置，token 会失效，但是有了账号密码，则有可能登录您的 ZoomEye 账户。

**4、Cert 证书搜索**

需要注意的是，按照常规逻辑，您需要将目标 ssl 证书的序列号进行十六进制编码后才能配合语句搜索，但是 Kunyu 则仅需要提供 Domain 地址则可以检索。原理是对目标站做了一次请求获取到了序列号并进行处理，但是如果您的主机无法访问需要搜索的目标则无法检索，这时您也可以按照常规方法配合语句搜索。

**5、Favicon 图标搜索**

ico 图标搜索既支持 URL 检索，又支持本地 ico 图标文件搜索，这样有了更好的延展性，以及兼容性。

**6、查询数据保存路径**

默认情况下您的查询数据在用户目录下的 Kunyu 文件夹中，您也可以在 console 模式中使用 ExportPath 命令查询路径。

**7、自动补全**

Kunyu 的自动补全支持大小写，命令记录等，使用 Tab 进行补全，用法参见 Metasploit 即可。

0x06 Contributions

风起 @knownsec 404 Team  
wh0am1i@knownsec 404 Team  
fenix@knownsec 404 Team  
0x7F@knownsec 404 Team

0x07 Community

如果有问题可以在项目下提交 issue，或扫描以下维码添加 ZoomEye 运营微信，并备注坤舆，会把大家拉到 ZoomEye 网空测绘交流群中。

![](https://mmbiz.qpic.cn/mmbiz_jpg/YTZvSeuD5nJv1vxJHmlLnMGBibc0vdQwBY7hsFf2Qh1jIlukXlSDk9wib5ajODoLjfNkpMEQDdoEaN6DicjeULUjA/640?wx_fmt=jpeg)

 **![](https://mmbiz.qpic.cn/mmbiz_gif/1Jw2DbGRWIh2YbQUBTocYt1ib81zImFCIekh0IMHdvQSgvLsIrRn00ib8Pgdh53z5ZBriaicwiba7q11CuibXpBErb5g/640?wx_fmt=gif)**   

**往 期 热 门**

**(点击图片跳转)**

[

![](https://mmbiz.qpic.cn/mmbiz_jpg/3k9IT3oQhT3Jmw11rt08W22M7hl7FS59Z46EQHtYnGPicwNNn0csURAndDCxwp61EXe50ia5Nf1iaJ1uZvKWQvRdQ/640?wx_fmt=jpeg)

加密固件之依据老固件进行解密







](http://mp.weixin.qq.com/s?__biz=MzAxNDY2MTQ2OQ==&mid=2650948028&idx=1&sn=6e06eb405bed8dffa5a66d8cd41ae2a9&chksm=8079038eb70e8a98c881b5afa0cda541a6b0b95b12c67b06b5f4e1b7e9f94cd97bbcfd73d9d7&scene=21#wechat_redirect)

  

[

![](https://mmbiz.qpic.cn/mmbiz_jpg/3k9IT3oQhT2HuekFwFZVWIGM7ibTG65jiaiblpDZHoEvDwjzBqp3ibGFPrBjl4qiaJiaKCLD1uJRxmj5Pia0FnEnicCy2w/640?wx_fmt=jpeg)

D-Link DIR 3040 从信息泄露到 RCE







](http://mp.weixin.qq.com/s?__biz=MzAxNDY2MTQ2OQ==&mid=2650948003&idx=1&sn=19275bed5cf72dbe81b742e5ac1b2dc4&chksm=80790391b70e8a87bfe977369e51e5ba4d266ce963f44d6cbd2edcc331b3ec119ffc3ced26f3&scene=21#wechat_redirect)

  

[

![](https://mmbiz.qpic.cn/mmbiz_jpg/3k9IT3oQhT3azzeVwiahwN2PtGgibb2ELp5cZHicCLRKWbzJ5FhQpC6awicZpQFTmicibhvkUGojt1wEHEPFHKq6zhog/640?wx_fmt=jpeg)

VPN 原理以及实现







](http://mp.weixin.qq.com/s?__biz=MzAxNDY2MTQ2OQ==&mid=2650947968&idx=1&sn=45e66431cca37622a4441c9207a2305b&chksm=807903b2b70e8aa4e0ce42f7458f9821bf254283e65f7b369970daba93f1b07f94bb12257e92&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/3k9IT3oQhT0Z79Hq9GCticVica4ufkjk5xK8te0JrCrcOiatDWNPRndZzq1N80rlbyxU9bGuTvekqEGu5utyHqicicw/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT09IJjs3wGQbICd50va8zMqN2SkNrrQyWIiaCQvodo60ZfrQIhWic0TSeglsSGiboXx1wjbOxwdu5jQw/640?wx_fmt=jpeg)

**觉得不错点个 “在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**