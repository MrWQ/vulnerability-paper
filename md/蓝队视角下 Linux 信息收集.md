> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/TlCyifwRrzKFx7jJkJlF_A)

> 本文所有操作和截图皆在本地环境下的靶机中进行

前言
==

上一篇 [红队视角下 Linux 信息收集](https://mp.weixin.qq.com/s?__biz=MzI1MDEzMTMxNg==&mid=2247483898&idx=1&sn=592a976195f379c22a2818f274da7c64&chksm=e987a7e1def02ef71e6c4cea2e3371990de26f91dea7c3c3e679d6a27fb159e9357e5ab76afb&scene=21#wechat_redirect "红队视角下Linux信息收集") 我们谈到红队是以提权和后渗透为主要目的而进行的信息收集，本次谈一谈在蓝队应急响应中 Linux 系统下比较关键的内容。

* * *

日志
==

Linux 系统的日志功能非常强大且完善，几乎可以保存所有的操作记录，蓝队的信息收集主要就是针对日志的信息收集，先从系统自身的日志来说起。

系统上跑了很多程序，那么每个程序都会有相应的日志产生，而这些日志就被记录到这个目录下，具体在 /var/log 目录下

![](https://mmbiz.qpic.cn/mmbiz_png/N4olnK9BI9blMeOzFY0gsibSiaPseSJKMMvYfaxicOQTQpSYanYl4Dq3e0ZI0PxUGxAyLvROHFaQDFjicHuGYic7gkw/640?wx_fmt=png)

/var/log 下存放着各种程序的 Log 文件，特别是 login (/var/log/wtmp log 所有到系统的登录和注销) 和 syslog (/var/log/messages 里存储所有核心和系统程序信息. /var/log 里的文件经常不确定地增长，应该定期清除.

还有其中几个比较常用的日志文件:

•/var/log/dmesg : 核心启动日志，系统启动时会在屏幕显示与硬件有关的信息，这些信息会保存在这个文件里面.•/var/log/spooler : UUCP 和 news 设备相关的日志信息 •/var/log/cron : 与定时任务相关的日志信息 •/var/log/btmp : 记录错误登录日志, 这个文件是二进制文件, 可以使用 lastb 命令查看 •/var/log/boot : 系统引导日志 •/var/log/lastlog : 记录系统中所有用户最后一次登录时间的日志，这个文件是二进制文件，可以使用 lastlog 命令查看 •/var/log/mailog : 记录邮件信息

内核及系统日志
-------

> 内核为 2.6.18 时候使用的是 syslog 服务

> 注: 内核为 2.6.32 以后 syslog 被命名为 rsyslog，所以配置文件名称也不一样

这种日志由 syslog 统一管理，根据其主配置文件 /etc/syslog.conf 中的设置决定将内核消息及各种系统程序消息记录到什么位置。用户日志：这种日志数据用于记录 Linux 系统用户登录及退出系统的相关信息，包括用户名、登录的终端、登录时间、来源主机、正在使用的进程操作等。程序日志：有些应用程序运会选择自己来独立管理一份日志文件（而不是交给 syslog 服务管理），用于记录本程序运行过程中的各种事件信息。由于这些程序只负责管理自己的日志文件，因此不同的程序所使用的日志记录格式可能会存在极大差异。

通过查看 /etc/rsyslog.conf ，可查看相关系统日志配置情况。

![](https://mmbiz.qpic.cn/mmbiz_png/N4olnK9BI9blMeOzFY0gsibSiaPseSJKMMd7AUZUc5ddUuMydjEqia8F30BB7Ahxet06Vvhay7ybCJqgZVGpXRnww/640?wx_fmt=png)

message 日志，一般内核及大多数系统消息都被记录到公共日志文件 /var/log/messages 中，而其他一些程序消息被记录到不同的文件中，日志消息还能够记录到特定的存储设备中，或者直接向用户发送。

![](https://mmbiz.qpic.cn/mmbiz_png/N4olnK9BI9blMeOzFY0gsibSiaPseSJKMMH48EW5icANuhZkZZMb9mwa8Fic3BfAQPCfbiaIuqthLIOXB0IDK2mia41Q/640?wx_fmt=png)

secure 是应急中最常用的文件，主要记录系统存取数据的文件，如 POP3、ssh、telnet、ftp 等相关记录，从日志中可看出系统服务是否遭受到安全威胁，从如下日志中可看到 SSH 服务一直在被破解。

![](https://mmbiz.qpic.cn/mmbiz_png/N4olnK9BI9blMeOzFY0gsibSiaPseSJKMMoJtXbZiaT2vq4Hw3dDYQHs46AtCq4ddiaRaMbl95QmFojT80dUJtmwDg/640?wx_fmt=png)

用户日志
----

wtmp 日志记录了用户的登录、退出、重启等情况，可以查看系统是否存在异常用户登录，判断攻击者是否已经登录服务器，由于 wtmp 日志为二进制文件，所以利用用 last 命令查看，last -t 20190426120950 , 可查看这个时间之前的日志。

![](https://mmbiz.qpic.cn/mmbiz_png/N4olnK9BI9blMeOzFY0gsibSiaPseSJKMMibFLgZiarkiaFf8jiahXfG7MQmXcWqBPyzOAXUktO64iaKZNysRjNJzVjFA/640?wx_fmt=png)

lastlog 命令，用于显示系统中所有用户最近一次登录信息。lastlog 文件在每次有用户登录时被查询。可以使用 lastlog 命令检查某特定用户上次登录的时间，并格式化输出上次登录日志 /var/log/lastlog 的内容。它根据 UID 排序显示登录名、端口号（tty）和上次登录时间。如果一个用户从未登录过，lastlog 显示 Never logged。注意需要以 root 身份运行该命令。

![](https://mmbiz.qpic.cn/mmbiz_png/N4olnK9BI9blMeOzFY0gsibSiaPseSJKMMGC9PSaQq4hY9AWkWExCuae9JHb1Z9CShPTVK5j9xmKFBm6XJf6MSYw/640?wx_fmt=png)

所以查询登录情况的几个命令，本质上就是在查日志 /var/log/btmp、/var/log/lastlog、/var/log/wtmp

```
last       #登录成功记录
lastb      #登录失败记录
lastlog    #最后一次登录
```

日志分析技巧
------

查看尝试暴力破解机器密码的人

```
# Debian 系的发行版
sudo grep "Failed password for root" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr | more

# Red Hat 系的发行版
sudo grep "Failed password for root" /var/log/secure | awk '{print $11}' | sort | uniq -c | sort -nr | more
```

查看暴力猜用户名的人

```
# Debian 系的发行版
sudo grep "Failed password for invalid user" /var/log/auth.log | awk '{print $13}' | sort | uniq -c | sort -nr | more

# Red Hat 系的发行版
sudo grep "Failed password for invalid user" /var/log/secure | awk '{print $13}' | sort | uniq -c | sort -nr | more
grep "Failed password" /var/log/secure | awk {'print $9'} | sort | uniq -c | sort -nr
grep -o "Failed password" /var/log/secure|uniq -c
grep "Accepted " /var/log/secure | awk '{print $1,$2,$3,$9,$11}
```

IP 信息

```
# Debian 系的发行版
grep "Failed password for root" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr | more

# Red Hat 系的发行版
grep "Failed password for root" /var/log/secure | awk '{print $11}' | sort
```

登录成功

```
# Debian 系的发行版
grep "Accepted " /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr | more

# Red Hat 系的发行版
grep 'Accepted' /var/log/secure | awk '{print $11}' | sort | uniq -c | sort -nr
grep "Accepted " /var/log/secure* | awk '{print $1,$2,$3,$9,$11}'
```

* * *

系统
==

系统完整性
-----

通过 rpm 自带的 -Va 来校验检查所有的 rpm 软件包，查看哪些命令是否被替换了

```
rpm -Va > rpm.log

# 如果一切均校验正常将不会产生任何输出，如果有不一致的地方，就会显示出来，输出格式是8位长字符串，每个字符都用以表示文件与RPM数据库中一种属性的比较结果 ，如果是. (点) 则表示测试通过。
验证内容中的8个信息的具体内容如下：
- S         文件大小是否改变
- M         文件的类型或文件的权限（rwx）是否被改变
- 5         文件MD5校验是否改变（可以看成文件内容是否改变）
- D         设备中，从代码是否改变
- L         文件路径是否改变
- U         文件的属主（所有者）是否改变
- G         文件的属组是否改变
- T         文件的修改时间是否改变
```

查看对外开放端口
--------

检查异常端口

```
ss -tnlp
ss -tnlp | grep ssh
ss -tnlp | grep ":22"

netstat -tnlp
netstat -tnlp | grep ssh
```

这里推荐一个很好用的防止端口扫描脚本 https://github.com/EtherDream/anti-portscan

防火墙
---

```
firewall-cmd --state                    # 显示防火墙状态
firewall-cmd --get-zones                # 列出当前有几个 zone
firewall-cmd --get-active-zones         # 取得当前活动的 zones
firewall-cmd --get-default-zone         # 取得默认的 zone
firewall-cmd --get-service              # 取得当前支持 service
firewall-cmd --get-service --permanent  # 检查下一次重载后将激活的服务

firewall-cmd --zone=public --list-ports # 列出 zone public 端口
firewall-cmd --zone=public --list-all   # 列出 zone public 当前设置
```

用户
--

```
awk -F: '{if($3==0||$4==0)print $1}' /etc/passwd            # 查看 UID\GID 为0的帐号
awk -F: '{if($7!="/usr/sbin/nologin")print $1}' /etc/passwd # 查看能够登录的帐号
lastlog                                                     # 系统中所有用户最近一次登录信息
lastb                                                       # 显示用户错误的登录列表
users                                                       # 打印当前登录的用户，每个用户名对应一个登录会话。如果一个用户不止一个登录会话，其用户名显示相同次数
```

计划任务和启动项
--------

```
chkconfig                   # 查看开机启动服务命令
chkconfig --list | grep "3:启用\|3:开\|3:on\|5:启用\|5:开\|5:on"
ls /etc/init.d              # 查看开机启动配置文件命令
cat /etc/rc.local           # 查看 rc 启动文件
ls /etc/rc.d/rc[0~6].d
runlevel                    # 查看运行级别命令
crontab -l                  # 计划任务列表
ls -alh /var/spool/cron     # 默认编写的 crontab 文件会保存在 /var/spool/cron/用户名 下
ls -al /etc/ | grep cron
ls -al /etc/cron*
cat /etc/cron*
cat /etc/at.allow
cat /etc/at.deny
cat /etc/cron.allow
cat /etc/cron.deny
cat /etc/crontab
cat /etc/anacrontab
cat /var/spool/cron/crontabs/root
```

可疑文件
----

查看敏感目录，如 / tmp 目录下的文件，同时注意隐藏文件夹，以 “..” 为名的文件夹具有隐藏属性，针对可疑文件查看创建修改时间。

```
find / -ctime -2                # 查找72小时内新增的文件
find ./ -mtime 0 -name "*.jsp"  # 查找24小时内被修改的 JSP 文件
find / *.jsp -perm 4777         # 查找777的权限的文件
ls -a /tmp                      # 查看临时目录
strings /usr/sbin/sshd | egrep '[1-9]{1,3}.[1-9]{1,3}.'    # 分析 sshd 文件，是否包括IP信息
```

后门检查
----

1. 检查 /etc/passwd 文件是否有异常 2. 检测对应 vim 进程号虚拟目录的 map 文件是否有 python 字眼.3. 通过排查 shell 的配置文件或者 alias 命令即可发现, 例如 ~/.bashrc 和 ~/.bash_profile 文件查看是否有恶意的 alias 问题.4. 进入 /home 各帐号目录下的 .bash_history 查看普通帐号的历史命令 5.Rootkit 检查 chkrootkit 或 Rootkit Hunter 工具进行

* * *

分割日志工具
======

目前大部分 linux 系统都会默认安装有 logrotate，日志分割工具. 而这个工具的功能就是大家在 /var/log/ 目录下面看到的形如 messages-20181028 样式的日志，在使用 logrotate 进行配置后就可以按照时间或者大小对日志进行分割存储. 如果对 /etc/logrotate.conf 文件和 /etc/logrotate.d/ 目录没有改动，可以看到 /etc/logrotate.conf 默认配置:

```
vim /etc/logrotate.conf
# 按周轮训
weekly
# 保留4周日志备份
rotate 4# 标记分割日志并创建当前日志
create
# 使用时间作为后缀
dateext
# 对 logrotate.d 目录下面的日志种类使用
include /etc/logrotate.d
# 对于wtmp 和 btmp 日志处理在这里进行设置
/var/log/wtmp {
    monthly
    create 0664 root utmp
 minsize 1M
    rotate 1
}
/var/log/btmp {
    missingok
    monthly
    create 0600 root utmp
    rotate 1
}
```

此外，如果你在服务器上面安装了 mysql，httpd 或者其他应用服务后，logrotate 它会自动在 /etc/logrotate.d/ 下面创建对应的日志处理方式，基本是继承 logrotate.conf. 因此，不论是你服务器上面系统日志还是应用日志，面对日志量太大的问题，都可以使用 logrotate 进行设置处理. 当然还有 Loganalyzer 这类日志收集系统，这里由于篇幅缘故，就不细讲了。

* * *

总结
==

本文模拟了常见的应急场景，通过各种技术手段，在机器上捕捉红队人员的痕迹，并且排查是否有后门残留。在实际环境中，会存在各种复杂的场景，特别是针对系统上不同的应用，存在各种隐藏后门的手段，蓝方人员不仅需要掌握系统、应用的加固知识还需要掌握相应的漏洞利用知识，熟悉红队的进攻手段，才可以做到更好的防护。

**文章来源：江苏智慧安全可信技术研究院**

**【往期推荐】**  

[未授权访问漏洞汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484804&idx=2&sn=519ae0a642c285df646907eedf7b2b3a&chksm=ea37fadedd4073c87f3bfa844d08479b2d9657c3102e169fb8f13eecba1626db9de67dd36d27&scene=21#wechat_redirect)

[【内网渗透】内网信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485796&idx=1&sn=8e78cb0c7779307b1ae4bd1aac47c1f1&chksm=ea37f63edd407f2838e730cd958be213f995b7020ce1c5f96109216d52fa4c86780f3f34c194&scene=21#wechat_redirect)  

[【内网渗透】域内信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485855&idx=1&sn=3730e1a1e851b299537db7f49050d483&chksm=ea37f6c5dd407fd353d848cbc5da09beee11bc41fb3482cc01d22cbc0bec7032a5e493a6bed7&scene=21#wechat_redirect)  

[记一次 HW 实战笔记 | 艰难的提权爬坑](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=2&sn=5368b636aed77ce455a1e095c63651e4&chksm=ea37f965dd407073edbf27256c022645fe2c0bf8b57b38a6000e5aeb75733e10815a4028eb03&scene=21#wechat_redirect)

[【超详细】Microsoft Exchange 远程代码执行漏洞复现【CVE-2020-17144】](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485992&idx=1&sn=18741504243d11833aae7791f1acda25&chksm=ea37f572dd407c64894777bdf77e07bdfbb3ada0639ff3a19e9717e70f96b300ab437a8ed254&scene=21#wechat_redirect)

[【超详细】Fastjson1.2.24 反序列化漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=1&sn=1178e571dcb60adb67f00e3837da69a3&chksm=ea37f965dd4070732b9bbfa2fe51a5fe9030e116983a84cd10657aec7a310b01090512439079&scene=21#wechat_redirect)

[【超详细】CVE-2020-14882 | Weblogic 未授权命令执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485550&idx=1&sn=921b100fd0a7cc183e92a5d3dd07185e&chksm=ea37f734dd407e22cfee57538d53a2d3f2ebb00014c8027d0b7b80591bcf30bc5647bfaf42f8&scene=21#wechat_redirect)  

[【奇淫巧技】如何成为一个合格的 “FOFA” 工程师](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485135&idx=1&sn=f872054b31429e244a6e56385698404a&chksm=ea37f995dd40708367700fc53cca4ce8cb490bc1fe23dd1f167d86c0d2014a0c03005af99b89&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_**走过路过的大佬们留个关注再走呗**_![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEATexewVNVf8bbPg7wC3a3KR1oG1rokLzsfV9vUiaQK2nGDIbALKibe5yauhc4oxnzPXRp9cFsAg4Q/640?wx_fmt=png)

**往期文章有彩蛋哦****![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHtVfEjbedItbDdJTEQ3F7vY8yuszc8WLjN9RmkgOG0Jp7QAfTxBMWU8Xe4Rlu2M7WjY0xea012OQ/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTECbvcv6VpkwD7BV8iaiaWcXbahhsa7k8bo1PKkLXXGlsyC6CbAmE3hhSBW5dG65xYuMmR7PQWoLSFA/640?wx_fmt=png)

**分享前辈知识，一起学习共同进步！！如侵权请私聊公众号删文![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHvn9mkHr2IDq5kEwPCgRujhTODPKjATDtE4qk0CydBmWFTcpib456YNCEvicv93MB9diavFXYqJV0UA/640?wx_fmt=png)**