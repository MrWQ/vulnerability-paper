> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/e3yPkNa9VDc_IKBB2AqDmQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **139** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/4gCJbFBBaxgr0WD3mMgto4yFaYwwjQMbuxDDBKibrhNlW5YFLV3K1XvkGj1sP1BiaYtibMLdQVrvth08BVUWP7oGw/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/159

靶机难度：中级（4.0/10）

靶机发布日期：2019 年 2 月 18 日

靶机描述：

Zipper is a medium difficulty machine that highlights how privileged API access can be leveraged to gain RCE, and the risk of unauthenticated agent access. It also provides an interesting challenge in terms of overcoming command processing timeouts, and also highlights the dangers of not specifying absolute paths in privileged admin scripts/binaries.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svxUqMr3yZfHHUyOmCeGPAXs1fFROMVtsufnUTuTnMpwfIksITm9Kr7A/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.108..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1sveKficljmTIrLpRPy158ZuSqNpB9Vmjd8NqdRMbewicJmhA3QibqAtL7Dw/640?wx_fmt=png)

nmap 发现开放了 ssh 和 apache 服务，还开放了 10050 端口，google 查找该端口与 Zabbix 代理相关联..Zabbix 是一种开源监视软件工具，是监视一系列网络，设备和服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1sv8LlSNSweg2J8llibc8gylPSibplekjYTOjkibTUw9gjJ84UaFx44OGQTw/640?wx_fmt=png)

访问 apache 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svnuibOYVwLDGQ9mTo7YOghHhdvV1ce3H7YZsfbAvG5Nxb8Dm5CJNvEjg/640?wx_fmt=png)

爆破发现了 zabbix 目录... 果然对称了 10050 端口

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svNpNlHMgTzVjBH8YZnOj1TWQ6uQicVmgS6GTrN7RoXgJZ4tMUDYPyticA/640?wx_fmt=png)

这是登陆页面... 可以直接查看监控状态

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svicGVfibN6t4tqOvibq4HEicIzJQFLnFASribB6TVOz86kGGBvNr7R7thNEQ/640?wx_fmt=png)

进入这是个监控状态，提供了监控指标，其中包括网络利用率，CPU 负载和磁盘空间消耗等...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svGb2iby82K4L1B3wzjSmjlf7X4jF9vjJJdbsHOtia8tianLfWcTsY7icYicA/640?wx_fmt=png)

Zapper's Backup Script，这里提供了用户 zapper....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svdojiarqepspH7gIIyaF7KpAh6lsIS5ibbe2oA3JoicjW7k5Ixbj1yfIkQ/640?wx_fmt=png)

使用默认 zapper 账号密码登陆报：GUI access disabled....

这里 google 搜索提示存在 zabbix 漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1sv18ibLeWwEZPnnox7Sop4tfT7wCMqibYObtld9bBoyuvqwDkuj9ZhYJdw/640?wx_fmt=png)

在监控状态下，ping 发现了 api 漏洞...hostid=10050

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svpB2OI74xMWps9WibniaicXZVAzLrmM5RGd80bvOUdRUicKfrn6nGLNzibIg/640?wx_fmt=png)

本地搜索，可以尝试利用 39937.py 漏洞进行提权....

下载到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1sv0KWE7t6b5yVaiaRyN30olibUoWNbZryyvp2VpGABZIgJJHyxjM5QXKew/640?wx_fmt=png)

按照 EXP 简单修改下即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svxzG780Ulp4rStheu67Oe1XEo1JDdm2NehOCvuPf3cqxe9oB9D8aKiaw/640?wx_fmt=png)

执行后成功利用....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svK68dfOn8aAJZJghghMaqsXGa5kxNkUmq883KelibVCHTdwicicEk3vHoA/640?wx_fmt=png)

由于 EXP 外壳极不稳定，直接利用 shell 提权...

枚举后通过 dockerenv 根目录，发现目前在容器中，在 zabbix 一些配置文件中发现了重要信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svCZuZict6vMsuIibD7ibAWEUUOMBUbAOQkTs9lICexniblHVHHjJEuhwr2g/640?wx_fmt=png)

获得了密码... 测试发现这是 mysql 的密码... 通过数据库枚举，发现这是 admin 页面密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svhAVDtePQ0sicic807XtBctBQnba1bYaggb3bFLicwqCGKtrcibf8SW7MLQ/640?wx_fmt=png)

通过 admin 登陆到页面中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1sviaTzeU38VsO0BsUcV6TJKctjLgPSWszzKdFbxcHv0Kw4IIlMkxic9wSg/640?wx_fmt=png)

zabbix 监视系统，多搜索点资料了解下...

创建 Script 然后写入 perl_shell 提权即可... 这里尝试过别的 shell，几分钟或者几秒钟就自动失效了...perl 最稳定

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svx7phicuoV3DQ7h0V1AmytpDU3vo1BR6l08UBcSAb2yzr8GEzRdA8p0Q/640?wx_fmt=png)

执行提 shell 外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svRRwKQBGDOOqmnzYibiaxVLRq3gcH0zTicuicMduiazfibhHz57lVWCJpCaIQ/640?wx_fmt=png)

通过 administrator 获得 shell 后，还是无法读取 user_flag 信息... 发现了 zapper 用户下存在了一些文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svatdiaS5PDMEk6IMWKHtk9hODw0JsIwShvibWETbdJLofCzmWktLuzJ6w/640?wx_fmt=png)

继续枚举 utils 目录，发现了密码....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svlh9b4iarV6T9oKGEyHqsWYQvmicmNaibXxiaqgv4IwAgGu4TENjibpMplBw/640?wx_fmt=png)

尝试 su 提权，成功在 zabbix 外壳下提升到了 zapper....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1sv0MUibFgga7HNhPARBO7SWZDqn8g9oSx5g0H3ygosXpOZd5VewxMYgYQ/640?wx_fmt=png)

LinEnum 枚举靶机信息... 发现了 SUID 里有可提权 root 信息... 这里主要匹配了：find /home/zapper/utils -perm -4000

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svC95sibNs1dLRfGT4n9vjKPia1GKTibEDoN8uFDZGhOdcOKpbBMloXibx5w/640?wx_fmt=png)

这里测试了发现该程序控制着 zabbix 的服务... 利用 strings 也能看出现象...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1sv8P0l3jNdtB1sqySFMUkD9MOsq8vOoAvVhwdIFPMVvbkplNtZmkYgLA/640?wx_fmt=png)

我这里直观的截图，在靶机本地利用了 ltrace 检查文件函数情况...

systemctl daemon-reload && systemctl start zabbix-agent 是以 root 用户身份执行着....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svVNj3icPySwunD9qeZ3OpvdhAsKibjsWlN0nYNJN3OWky8Fm6XPonLRMg/640?wx_fmt=png)

这里可以写 shell，命名 systemctl 即可... 替代执行

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMK4yzxtNsxtb49PBhTw1svQ1RFxVOib2owcKN9fK5G0KTvOHLOk5icicKc2aDmZfMt9wKFibrxjBfWDA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4gCJbFBBaxgr0WD3mMgto4yFaYwwjQMbuxDDBKibrhNlW5YFLV3K1XvkGj1sP1BiaYtibMLdQVrvth08BVUWP7oGw/640?wx_fmt=png)

本地我没有 stty，直接本地上传，添加变量即可... 成功获得了 root 权限... 并获得了 root_flag 信息...

信息收集目录爆破 --zabbix 漏洞 EXP 利用 -- 表单注入提权 -- 文件逆向提权

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)