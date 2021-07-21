> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/p_2OtYijhkF90LMNnDB8XA)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **99** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/15

靶机难度：中级（4.3/10）

靶机发布日期：2017 年 10 月 30 日

靶机描述：

October is a fairly easy machine to gain an initial foothold on, however it presents a fair challenge for users who have never worked with NX/DEP or ASLR while exploiting buffer overflows.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

  

  

一、信息收集

  

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapn2iaBZI6Y7icevkCS7ZxAcN2gJ7VXqyxnjIBicZ3WYn2h7eaMic2IjQ9kg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.16....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapQTyleAHrQGHtOHS1f1GCr7tTOgtia9VDFDKJ9cCspgmGCwibsk8uJviaA/640?wx_fmt=png)

Nmap 发现只有两个开放的服务，OpenSSH 和 Apache 服务器....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapMB3kyu0FX88usN0Jjq7icPxqRhLKkEQcygLVwD5yMllYJMiaaQhGVkhg/640?wx_fmt=png)

可以看到服务器运行着 October CMS... 先爆破目录看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapyFd73DVWOwAuc02zUVGAu0NCnmZiaSFHh1qf0dW2hgfIazNL3Ye61gA/640?wx_fmt=png)

利用 dirb 爆破目录发现了默认目录：backend

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapL0RtX80kpbe1jnPYNbU8ST0A53b9icr1hEFSNibib2bv4OLnLPO78KsGA/640?wx_fmt=png)

这是 October CMS 的默认目录登陆页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapexyQIYNDvTUKSIvsZdvPiab3uCJWSnkm5Mt3ryJohgcpDkBJWOh6XoQ/640?wx_fmt=png)

进来后利用默认账号密码登陆了... 可以看到在 media 下可以 upload.... 直接上传文件即可...（这里可以看到限制了 php5 格式文件修改下）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapPqGsI7vFV7KxzjEC42F3GFH5eYKcJYXZ4ZujSDfOEqfhUVOKQd5nWA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiap5zYtjUMq27EXJxwN3vylALibYQW4vrRzian807UQMT9HZGvo4VUcap7w/640?wx_fmt=png)

可以看到成功提权 root... 并且获得了所有信息... 有点快....???

做到这一步我有点蒙... 因为发现的 user 和 root 信息都是假的... 存在的 root 用户却是有效的... 这里是我没看懂的地方...

因为提交的 flag 官方提示是错误的...

那就重新查看下把...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapbhhpxDtFTXqsxwlOLWYcx1vRaCibzeLQhECFu394PEladgBZtS5IVpA/640?wx_fmt=png)

前面执行的是 web 输入上传的链接反弹回来却是 root 权限... 但是信息都是虚假的...

这次是通过模块触发...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapPeTUXKxmKD0Hkj8ue3CDwn1UXlZ1IPibvJxMDTjOssCdhV55oib6f44A/640?wx_fmt=png)

获得了 www 权限外壳... 这里的 user 信息确是正确的...（那前面的 root 权限哪里来的... 有小伙伴知道请告知我谢谢）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapk5FF7ZibacMbEPLkCh9VKW3TsYTib2z0yWCwsG01iaN4repYRkmwa3nrA/640?wx_fmt=png)

通过 LinEnum.sh 枚举了所有信息... 在 SUID 发现了不正常的程序 ovrflw，以 root 权限运行着... 按照经验应该是存在缓冲区溢出提 shell... 试试吧

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapPbs21JCk75SYoaW1oOWrUFToMqwZibMXeQ62PF1l7jGoFbBxX45PIsg/640?wx_fmt=png)

直接利用靶机自带的 nc 把文件传到本地分析...（这里传输方法很多）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapzgauDACQGpOancqS6HgmohX5IN10XeYm6TicRyia6tiaveCZhw4H2YMNA/640?wx_fmt=png)

虽然 ovrflw 是 ELF 32 位最低有效位可执行文件... 这里前面讲过太多缓冲区溢出的文章...

直接利用 pattern_create 和 pattern_offset 获得偏移量为 112...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiapqI4LpZQS8wTHmEG4uHlfib1KicKsuSNgM7vPOtqmwZZTCS50QuYibPQhQ/640?wx_fmt=png)

然后找到函数绝对值... 在找个断点... 直接输入提权 root 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMRyYqwe9TiasuxKiaVMpWHiap14Z57NYewS694GC8XGgERMlOFYyzicbZWqxaZMm6t0bQ037KHkiaT7VQ/640?wx_fmt=png)

```
while true; do ./ovrflw $(python -c 'print "A"*112 + "\x10\x13\x5e\xb7\x60\x42\x5d\xb7\xac\x3b\x70\xb7"');done
```

成功利用偏移量 + 函数绝对值和断点.. 直接获得了 root 权限... 当然还有很多种操作的方法，甚至写 python 写入 shell 也可以....

这里成功获得了正确的 root 权限...

估计前面的 root 权限是一个 BUG 吧...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中等难度的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/nLSlp1hFMwsA5K49ZxLYXtEibosgIZkIlYqhXqx03XbFqNrVBAm5axMu7OLyRv4RXEQdpzTBFs5wfhaLhvqw41Q/640?wx_fmt=png)

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