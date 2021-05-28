> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/cFK73WyHm7uE3L5aRa2D5w)

**为什么会有此文：**

原因一：保护个人隐私是是第一出发点；科技进步飞快，网络也渗透入生活中的方方面面，近几年的隐私泄露事故时有发生，我们该如何保护个人隐私？

原因二：得到了大佬的帮助和指点，希望把对我的指点内容记录一下，也能为其他人提供一点点帮助！

**测试方式：**

通过 CS4.2 生成测试程序，测试回连 C2 服务器时能否达到隐藏服务器的 IP

公网服务器真实 IP：1.2.3.4

Cobalt Strike 版本：4.2

所有需要注册帐号的步骤，都建议使用自己安全的邮箱！

一、使用隧道转发进行代理
------------

一句话核心原理：利用内网穿透，将 C2 回连端口映射到其他公网地址 64.x.x.x，以达到测试程序通过其他公网地址进行回连，隐藏 C2 真实 ip；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfibVOC9BL6DrYZrfmlBeqVvRXVaeB0x9yS940Cp3IEibbuvtbOBcPzBrg/640?wx_fmt=jpeg)

### **方案分析：**

适合用户：这种隐藏 ip 的方案适合于没有公网服务器，使用自己本地电脑进行测试的用户；或者有公网服务器，通过本方案隐藏服务器真实 ip 的用户；  
优点：免费使用他人提供的隧道服务，可以快速的用来测试，0 成本；  
缺点：使用了他人提供的隧道服务 (增加了风险)；且注册账号时还需要完成微信绑定 (增加了风险)；国内平台 (增加了风险)；

### 使用流程：

1. 打开网站

https://www.ngrok.cc/ 注册 ngrok 账号  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfQr71uacbT0BQaN8Oia126nYoJlcWrsWp9j2WphvLx6Usn6ibIkCfYG0Q/640?wx_fmt=jpeg)

2. 登录后配置 ngrok 代理

2.1 购买一个免费通道

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfG1FcE7ZqYl21b8oJps4f06KYztMftDHM5U3rjhkWFs70T8O92dGbrw/640?wx_fmt=jpeg)

2.2 配置通道

隧道类型分为 http、https、tcp  
我们本次测试 tcp 通道，http、https 各位有兴趣的自己尝试；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfqE4iaia8RM1VHON3FfWNJJsmqBZEIAhztz9vGa7TQzicccH5uZ3PPQpFg/640?wx_fmt=jpeg)

因为映射到公网的远程端口有限，所以我们需要多次查询可用的远程端口，例如：查询到 10001 端口可用，那就选择 tcp 端口映射 公网服务器的 10001 端口←—- 映射—→本地 127.0.0.1:8080 端口

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfIsnu6VOeSCmba89MZDEia0l1uKlWkjshDPe6RgLQbBWFdKdlAQtdWmQ/640?wx_fmt=jpeg)

最终配置如下，其中隧道 ID 就是我们后面要用到的；隧道域名就是对外部公网提供访问时的公网域名；  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfBcThiaZtz8rJWFJIJBprqy3OeicLquoZUS2MYZx571CNyqHfJV9jM6aA/640?wx_fmt=jpeg)

3. 穿透工具使用说明 

https://www.ngrok.cc/_book/

3.1 下载可执行程序 

https://www.ngrok.cc/download.html  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapf2vMXRcpT2dWhWVAiafUAsh8kve99k9XJAm1Uo1qY7VKVxrUsRDYYIWA/640?wx_fmt=jpeg)

3.2 运行隧道穿透

```
#./sunny clientid 45e3634aAAAAAAAAAA #隧道id
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfzymprf7opSO99FPbzuKbJeeBkIZYAjywaiaWxHeQ2woYgtwQHjplf4A/640?wx_fmt=jpeg)

运行成功后，所有访问 

xxx.xxxxxgye.com:10001 会和本地 8080 端口打通透明传输；

4. 配置 listener

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapf1icj6EobJRX7y3BQs26SaofaojLFlwxuyapS0H7PajQj1YbLzf4S36g/640?wx_fmt=jpeg)

5. 生成 payload，运行测试

5.1 运行 payload，主机可以成功上线；  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfk0zoIMXNzc86z5BNylSiajmVhtzyspPuDwIM4dktqPCcJ0wUBr51GfQ/640?wx_fmt=jpeg)

5.2 查看本地回接 C2 服务器的 ip 地址为

xxx.xxxxxgye.com:10001(67.x.x.x:1001)；而不是我们自己服务器的真实 ip!  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfzgSET8JmadevSHhEiaQibIns3kRZyjVQNrQcqDvuL15WTPXmwfbcynbA/640?wx_fmt=jpeg)

上面的 64.X.X.X 就是 ngrok 的公网 ip

搞定！

二、使用 CDN
--------

一句话核心原理：使用 CDN 内容分发网络的多节点分布式技术，通过 “加速、代理、缓存” 隐藏在后面的静态文件或服务；最终实现对外暴露的是 CDN 多节点的公网域名 IP，很难甚至无法溯源真实后端服务器的域名或 IP！

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfZhZ5Yk2iagDJRomxGPUSkVXNTZzYRMVA3xbF6WAgPGAcdJUiahSSDw5g/640?wx_fmt=jpeg)

### 方案分析：

适合用户：这种隐藏 ip 的方案适合于有公网服务器，通过本方案 CDN 进行 “加速、代理、缓存” 实现隐藏服务器真实 ip 或域名的用户；使用国内 CDN 服务商的产品的域名必须完成 ICP 实名备案；  
优点：利用 CDN 分布式技术，不同区域的主机就近连接到 CDN 服务，优化了访问质量，隐藏了真实服务器的 ip；且 CDN 分布式技术可以在一定程度抵抗 DDOS 大流量攻击；使用国内 CDN 适合用于做红蓝对抗技术比拼等合法目的;  
缺点：受控主机还是通过我们自己的域名进行回连，对外还是能看到连接域名；且如果使用国内 CDN 的服务 (增加了风险)，域名就必须完成 ICP 备案 (增加了风险)；而且还有一些方法可能溯源到真实 IP(请一定要按照原文中的参考文章 1、2，进行子查一下！)；

### 使用流程：

(匿名注册新域名且无需备案 + 使用国外免费 CDN 服务)

1. 匿名注册新域名：

https://www.freenom.com/zh/index.html?lang=zh  
1.1 完成账号注册登录 (注册可以先不做，继续选域名后面会有一步骤让我们注册账号)；

1.2 搜索域名：

> 小坑提醒：这里有一个坑，搜索 wikisoft, 会显示所有域名不可用；但是搜索 wikisoft.tk 就可以；所以一定要搜索域名全称！

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfwcialZ9yheruyvdbNz4NTH0PKUic0D6pm2VU3aeSQlMGwX8J10IloFXg/640?wx_fmt=jpeg)1.3 下单确认：  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapflaZyDn7Uw2INrQtLS5CtEVc09EPV9KqySNia42TP9icZqNgibe8ibibRNEQ/640?wx_fmt=jpeg)如果之前没有注册过域名，点击 “继续” 按钮，会让我们进行注册账号，或者验证邮箱；然后进行登录再进行选购域名；(这里如果注册失败，可以用 gmail 注册。)

1.4 配置域名的 NameServer 域名解析服务 (这样做，后面再解释为什么；现在不修改，默认配置，也可以后面再修改)

1.4.1 进入我的域名：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfI44qK4oibickWv0kdAf1kQ3YOciaWrvTHLnUDvx6Y3YCMhEiabp6oRmFpw/640?wx_fmt=jpeg)

1.4.2 选择域名管理：  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapf1UEQcnbu39vsKbNZNDGQbmU9d30ibTEqTqLXd4YxqGIaFIAicBZ80wgg/640?wx_fmt=jpeg)1.4.3 选择域名解析服务进行修改  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapffX3aee4WcW1WUKj2Oe2xpsMFfDXicHibcKL9fKGiaGHs8ic7Og8UrvnAEw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfYPTeibQl9FrQicRm8u1JbVicbkw6Hj2cvWqySZl0BHSfOWd6lUJ6Xicicug/640?wx_fmt=jpeg)

```
ASPEN.NS.CLOUDFLARE.COM COLEMAN.NS.CLOUDFLARE.COM
```

匿名域名注册及配置完毕！

2. 匿名注册免费 CDN 服务 Cloudflare

2.1 登录注册账号

https://www.cloudflare.com/zh-cn/

2.2 配置域名使用 CDN

2.2.1 添加站点  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfY1ib5L3kEOl95pshicdPM7GtaBQeAQ8BQwq3N0LOAWErfSQjVVaR93eA/640?wx_fmt=jpeg)

2.2.3 选择免费计划  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfBebXQB4Y9x1yoUImyuBbC9ib4yU0MbkQUx5oKCYJygsksdEB3p1uy7Q/640?wx_fmt=jpeg)

2.2.4 直接配置使用 CDN 代理模式进行域名解析提供服务

上面 1.4，配置 NameServer 更换解析服务器的原因就是，将 wikisoft.tk 域名的所有解析功能都托管在 Cloudflare，这样 Cloudflare 可以提供 CDN 的解析功能！

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfvHKkeLCL1sAn05V6UmopFibWBniahYAyJXCcmWBcALMiaTjx4LiancrJug/640?wx_fmt=jpeg)

2.2.5 自动配置全部选择关闭

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfjAunsyMOQQSdFHibj68UQSmWjL83wrNRkiaR3VkcAVxP7DrlUhqmKJIg/640?wx_fmt=jpeg)

2.2.6 配置 SSL/TLS 加密方式 (默认不加密，有兴趣的自己尝试其他加密的区别)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapf3v33VtIYf4iaP4x6no4cSC7jG1dDhtiaA5TaLBe29G2qLzXkM0H3qV4g/640?wx_fmt=jpeg)注意：Cloudflare 的 CDNhttp、https 代理模式有个特点，如果用其他端口的话，是监听不到的！

因为我是使用的国内云主机，且 zh.wikisoft.tk 没有进行备案，所以没有办法使用 80、8080、443、8443 端口提供服务；所以我真实云主机的回连端口使用的是 http—2095！如果你用的是国外云主机，那就直接用 80！

```
Cloudflare支持的HTTP端口是：80,8080,8880,2052,2082,2086,2095 Cloudflare支持的HTTPs端口是：443,2053,2083,2087,2096,8443
```

到此域名 + CDN 全部搞定！开始测试！

3. 配置 listener

HTTP Host Header，必须填写你的域名！这是 CDN 技术的原理要求；在下面的 “域名前置方” 案中我们再解释

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfzvlCG4UlVL4aje3vRuPHG7v9jFoms0PffsZiaaPGnzPEciaCJwhWeiclw/640?wx_fmt=jpeg)

4. 生成 payload，运行测试

4.1 运行 payload，主机可以成功上线；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapf8at1ZgVwb6BWxM5J51ziaThERkhl7509U6IWWFCIFm1nqZOTqiaxviclA/640?wx_fmt=jpeg)

4.2 查看受控主机本地回接 C2 服务器的 ip 地址为 172.67.159.243:2095（CDN 节点 ip）；而不是我们自己服务器的真实 ip

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfRzq5L6svB5GibCTyDhUQWicDm57shzkibHK1cL0jJbg3lZZ1WowXUnhLA/640?wx_fmt=jpeg)

4.3 再来说一下这个 ip 是啥：这个 ip 就是我们使用的 Cloudflare 的最近 CDN 节点的公网 ip

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfASoAhyiagkennVNxM0V8h71SavSEbEelBaJNtEMjIkdcI7CfIga2uNA/640?wx_fmt=jpeg)

搞定！

三、使用域名前置 (Domain Fronting)
--------------------------

一句话核心原理：底层技术还是上面的 CDN，但是我们使用了其他正规可靠的域名进行连接 (比如：www.baidu.com)，通过设置 HOST=zh.wikisoft.tk 修改 host 头的原理，让 CDN 将连接指向我们期望的 C2 服务器；最终实现受控主机通过回连！如果使用 https 的话，除非逆向程序获取 host 头信息，否则无法获取到真实连接域名！

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfVUwOc2RGshbNicWgjiaIVVicpLrzxgX3vQrcbqXRLP7tN4Vbzo2xmkdHw/640?wx_fmt=jpeg)

### 方案分析：

适合用户：这种隐藏域名及 ip 的方案适合于有公网服务器  
优点：本方案使用高信誉域名进行连接，通常安全设备很难检测，也很难封堵；  
缺点：配置和准备条件较多步骤比较复杂；如果能利用好上面的域名 + CDN 也挺好。

### 使用流程：

小坑提醒：我尝试使用 http 域名前置进行原理演示，因为 Cloudflare 免费版 CDN 不支持上传自定义 ssl 网站证书，只能升级成企业版才可以实现 https！(如果你是企业版，就是通过修改上面的 “2.2.6 配置 SSL/TLS 加密方式” 这一节就能完成 https 通的联通及域名前置！可需要申请域名的 https 证书，现在各种云平台都有一年免费证书可用，方法“参考文章 4、5”。)

1. 完成上面域名 + CDN 的所有配置

2. 获取其他也托管在 Cloudflare 并使用 CDN 的合法域名 (比如：commonlit.app)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfE4G7iczEJnkueVUPWBRRHokJRYmAMia9fjs3dfmHHqiacNF2icYe8yfiaZg/640?wx_fmt=jpeg)

3. 配置 listener

HTTP Host Header，必须填写你的域名 zh.wikisoft.tk, 这是 CDN 技术的原理要求；CDN 的 ip 都一样，如何判断用户访问的时候 baidu 还是 qq 呢？实际上就是通过 http 头里面的 host 字段进行判断的！详细内容学习 “参考文章 6、7、8”

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfI3cldDkeFWpIBJbpnkPia7oHwYzLUF7gMvkEH6EibGu14UoibJLibej1kg/640?wx_fmt=jpeg)

4. 生成 payload，运行测试

4.1 运行 payload，主机可以成功上线；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfSS8MIAiaTicEuSFXISY28s2Nb69ibkDH6ibicBYYCEbs9MicN2ia7xhKZlSXg/640?wx_fmt=jpeg)4.2 查看受控主机本地回接 C2 服务器的 ip 地址为 104.21.41.43:2095（CDN 节点 ip）；而不是我们自己服务器的真实 ip  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfhbRMhAw3NLZ1qzYmicp2TxZQfdNh8r8lc0yict9W0e5z8ia8iaDK94icibhA/640?wx_fmt=jpeg)

4.2.1 查看 DNS 数据包，可以确认连接过程是查询 commonlit.app:2095 这个地址，进行连接的；  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfLSlsXWWrAUVLfXBZ6WdTCLSBEztKZBxGwMJEiap5FBYFicHzPOlGfBmg/640?wx_fmt=jpeg)

4.2.2 查看连接数据包，http 方式还是可以看到 host 信息的；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfY2VLWCjD9JWhh6g9SIwXfGw2FH1qpyicKaMyuWRz6qh3iaibpKIQic7CKQ/640?wx_fmt=jpeg)

4.3 再来说一下这个 ip 是啥：这个 ip 就是我们使用的 Cloudflare 的最近 CDN 节点的公网 ip  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfYF1HkuV69TXxhsfHXDbAT9ee0WNsSDUkV6WmDYQfQibstdfoeQDAJFw/640?wx_fmt=jpeg)

备注：使用 https 的方式进行域名前置，除非逆向程序获取 shellcode 里面的 host 内容，否则无法获取真实域名 zh.wikisoft.tk, 也无法溯源真实后端服务器的 IP！使用了 https 域名前置，就是在上面的 CDN 直接使用 zh.wikisoft.tk 域名的基础上又增加了一层安全保障！如何逆向二进制，也有教程文档 “参考文章 9”

搞定！

四、使用云服务 API 网关 / 云函数
--------------------

一句话核心原理：api 网关透明转发代理后端服务！(了解一 kong 网关，原理一样)；云函数底层使用的就是 api 网关，只是云函数的功能更高级一点，当 client 调用网关接口时，通过编程进行修改输入参数；同理 api 网关接受到代理的后台服务返回的内容是可以再次修改返回内容，最终将信息返回给 client;

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfsDQ9NYMxqMa8AQHicnACgTYv2sQWUXN0oJeia0bBdomavBRs3hxgKsaQ/640?wx_fmt=jpeg)

### 方案分析：

适合用户：这种隐藏域名及 ip 的方案适合于有公网服务器，注册了云服务商网关或者云函数产品；  
优点：本方案使用高信誉域名进行连接，通常安全设备很难检测，也很难封堵；  
缺点：配置和准备条件较多步骤比较复杂；如果能利用好上面的域名 + CDN 也挺好。

### 使用流程：

备注：这一方案，只是原理学习，没有考虑到安全性；所以直接用了国内的云服务产品！！！各位可以自己寻找 “安全” 的云服务！云函数的学习“参考文章 10、11”，下面只说明底层的 api 网关内容

1. 注册 Q 云，完成相关认证

2. 配置 API 网关透明传输

2.1 新建 service

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfMkEnw7AR0kM0M0GZibogtWHNCrqhOKCa4QtHccnH3SXV3xeeyqgHRKA/640?wx_fmt=jpeg)

2.2 新建 API 代理并完成透明代理配置  
小坑提示：前端、后端代理的超时时间都设置的长一点！以免超时！  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfBJ97rpxlicpuO0xRonvmhggtqBq71LR1mibDHTiaIUHZhf56135KtYReg/640?wx_fmt=jpeg)![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfYnhnVKN7RKmGqfVzgz6SvxicDLeN1JJgOzEvIKpNDgnNlzwmGPZP2zQ/640?wx_fmt=jpeg)

后端域名：如果是 80 端口，就直接填写域名，如果是其他端口，就写成 域名: 端口

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfX2hNf1OwVTYkVe2Gt4jhBz159y2BNcsfQZpOCt3fsXBx5HuW8TIpaQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfZKWCk97eV0lq9z7t3GywZic13wDRg6fWGULYFggbRkjECKe1ficzCxCA/640?wx_fmt=jpeg)

2.3 查看公网接口调用地址

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfpRFLTWXZ9Hq9heHHYibY7N2gic0q0v2hvEeMicPRr33hyWyQibqZiczkZog/640?wx_fmt=jpeg)

3. 配置 listener

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapfG3c6b7bZ0fNTdXgWNIUefAqY5Uhy0pzJZrTqg1nKkIdGjUlRBO9qFQ/640?wx_fmt=jpeg)

4. 生成 payload，运行测试

4.1 运行 payload，主机可以成功上线；  
![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapf6yFxwEXic2EFliboDzib8HPFVyHicCqoQvVwhiaLS5WNMwNyx0icCBBbianTQ/640?wx_fmt=jpeg)

4.2 查看受控主机本地回接 C2 服务器的 ip 地址为 152.136.8.215:80（Q 网关节点 ip）；而不是我们自己服务器的真实 ip

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39icHkZwHa8fToiaYbVIewapf3FibibewicGwzrOYFyFiaOoz0mer6GUcic2LG4hjkUCyx2bciaRuialLuI7IA/640?wx_fmt=jpeg)

搞定！！

五、再说点其他的
--------

1. 域名直接使用 CDN 解析删除其他解析 (安全分数 + 1)：既然注册了匿名免费的域名，使用目的狠命聊！那就别添加太多解析，越多维护越麻烦，泄露信息风险越大！而且，这个域名后面的所有测试过程都不要不适用代理的模式解析到 ip 或者 CNAME 到其他域名！任何历史操作都是泄露你个人信息的风险点！

2. 服务器访问 IP 源限制 (安全分数 + 1)：既然使用了 CDN 服务，为了更安全，就将真实服务器防火墙 + 安全组的访问源 ip 做网段限制！设置成仅允许 Cloudflare 网段进行访问！防止其他小伙伴扫描 hack 你的 c2 服务！

3. 域名前置一定要用 https(安全分数 + 2)：使用 http 的方式玩域名前置是没意义的，抓包就能看到 http 里面的 host 信息；而使用 https 的域名前置方式，除非二进制逆向获取 shellcode 里面的 host 信息！(这一点，，我可能说错了，https 也能看到 host 信息~~)

4.C2 服务器安全加固 (安全分数 + 1)：C2 服务器的客户端连接的 50050 端口，做好安全防护！(配置好证书确认登录指纹信息！修改其他端口避免其他网络扫描！不用的时候就防火墙安全组都 deny 或者限制登录 ip 范围！)

![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR38Tm7G07JF6t0KtSAuSbyWtgFA8ywcatrPPlURJ9sDvFMNwRT0vpKpQ14qrYwN2eibp43uDENdXxgg/640?wx_fmt=gif)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf + 小程序：把安全装进口袋 小程序

  

精彩推荐

  

  

  

  

****![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib2xibAss1xbykgjtgKvut2LUribibnyiaBpicTkS10Asn4m4HgpknoH9icgqE0b0TVSGfGzs0q8sJfWiaFg/640?wx_fmt=jpeg)****

  

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR39sqjaLlJOnNYV4AEasAdibTzrH7PyIuE8MbnS21dOWVXNguibdAWFTQSXMxjy2GSJodYHLFhQ1ficDQ/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486112&idx=1&sn=296cf1bc4e88502ec3c5f73199949135&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR38seEkNn8TH7jZibkFTmoEsk6RKElsJrrsciaM7x32aqsPkBRK96QbqftgV9wWoG4HzVibedTiaZffTcg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MjM5NjA0NjgyMA==&mid=2651124157&idx=2&sn=f122abf33374d9bb2d105bb7afa93c74&chksm=bd1f63368a68ea20963d042cbc7e65e763a169b27f9cab26b3ce940603ac7fe8976260701a35&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR39dEsdO2GpOvH87GrfzuscAMuA4JpicWAFbJtfakgMF2hheeTcSSwguAbjO45btx8ws2etnvSJlOzQ/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486070&idx=1&sn=c6957ca2d1878f316b7947b5ff990a01&chksm=ce1cf0e9f96b79fff5b27a3c146f9e8828728c33625a97366b0cae3df1853dbeda368c59177f&scene=21#wechat_redirect)

**************![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR3icF8RMnJbsqatMibR6OicVrUDaz0fyxNtBDpPlLfibJZILzHQcwaKkb4ia57xAShIJfQ54HjOG1oPXBew/640?wx_fmt=gif)**************