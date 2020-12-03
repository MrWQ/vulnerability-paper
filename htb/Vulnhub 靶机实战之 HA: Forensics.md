> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/RDuacUsuXscTY3wghWtY9Q)

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDWthuxj2TXBsNCVHu70z5pcUkEHkWCrichUzI2esFfCrwUOpkB24XedQ/640?wx_fmt=gif)

亲爱的, 关注我吧

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDWthuxj2TXBsNCVHu70z5pcUkEHkWCrichUzI2esFfCrwUOpkB24XedQ/640?wx_fmt=gif)

**12/3**

本文字数 2161

图片流量消耗预警！

**来和我一起阅读吧**

描述：这是一个中等难度的取证挑战环境，通过网络取证调查方法和工具，找到关键证据获取`flag`。

目标：获得 4 个`flag`

```
靶机下载地址：https://www.vulnhub.com/entry/ha-forensics,570/
```

**本文涉及知识点实操练习 --Vulnhub 渗透测试实战靶场 Drupal** 

https://www.hetianlab.com/expc.do?ec=ECIDb885-0a46-4953-8c62-d915348eae0f&pk_campaign=weixin-wemedia  

靶机共有 5 个 flag，通过信息收集、找漏洞、提权去获得最终 / root 下的 flag。

##### **0x1 基本信息收集**

确定目标主机`IP`

使用`nmap` 扫描

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QvpNHUaiaDGicBPibp73gFws1pPloBVibp7k6JDVuxiabqWweh81j4JB1Edg/640?wx_fmt=jpeg)image-20201105162717223

排除网络内其他的`ip`，`10.1.1.152`就是目标机器

使用`nmap`扫描主机更加详细的信息

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QicomsNPBia7rskcxuC08JCQSEE5jpZxAHiaLNx2ricG7IwM0pXnHzNqzyQ/640?wx_fmt=jpeg)image-20201105162941053

可以把扫描处理的信息记录下来

目标开放的端口：`22`、`80`端口，服务有：`ssh`服务和`http`服务。

##### **0x2、收集网站信息**

浏览目标网站看看可以获取哪些信息

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qc2kJWWAeyR5BD9kbicHfIhrLRDLaS71FOvGDrkhX3gt1lx1qHpJib9gQ/640?wx_fmt=jpeg)image-20201105163204069

网页上有四张图，还有一些描述文字。点击`"Click here to get flag!"` 试试

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QAMSkU6kfO3vX6ibibr38AfHE277ZAQicibzHwWRunRZcdciaiahmibicAibeHAg/640?wx_fmt=jpeg)image-20201105163338207

有一张`gif`图片。可以把网站的图片收集 一下，放到一个文件夹。既然是取证，不要放过任何蛛丝马迹

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QYSYwyw9S0wAo0DldlXAno35Mxp6XYLnYfHEbxOXNMpLs08zRhoplhQ/640?wx_fmt=jpeg)image-20201105163651855

看看网站源代码里面有什么吧：

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QmFptGJCGZvr58SGeJ3D0y9nALEtR4cV84Du4QGagibpB4F7O6bjg9OA/640?wx_fmt=jpeg)image-20201105163736266

我们发现有一个`images`的目录，访问试试

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QfdaAd9xdmF6kJouogxr90bxQtkn5vyeqKFkBf553UDQQkWrAT8M2lA/640?wx_fmt=jpeg)image-20201105163947838

发现有多张图片，除了网页上显示的几张之外，还有一个`"dna.jpg"`和`"fingerprint.jpg"`的图片，同样把它们下载下来。

这个`"fingerprint.jpg"` 看起来是个暗示，我们看看图片的信息。

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QbkqAr4gzz11RjNEicWNehNEqibPwULoVtx5HKlFxhwvNicr6Nk1k3pmFw/640?wx_fmt=jpeg)image-20201105164719909

直接`file`查看文件信息，发现`exif`信息里面存在 `flag`，这样第一个`flag`就到手了

别的图片也可以看一下：

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qpd7HBPJzTdchx5p1c0A794tVmSOY8gNicCuPqAcKP5SRdjEm7Snb0zw/640?wx_fmt=jpeg)image-20201106124758843

好像没啥东西。

我们继续对网站下手，试试扫描网站文件和目录

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QLPnWf5BTTcsaDPwFZYIa4VV1PwJhRKvYaoebKWbXBI6tfulWz9HFKw/640?wx_fmt=jpeg)image-20201106125103545

`dirb`除了可以扫描目录之外，还可以扫描指定文件后缀的方式来扫描文件，比如我们可以扫描是否存在备份文件之类的，比如`.backup`、`.git`、`.txt`什么的

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QhHibm3Fvo720icxZicJKObFBKm1vdo83TdI1dBuqicrDDvdoOLaMp2lc9Q/640?wx_fmt=jpeg)image-20201106125304554

发现一个`txt`文件，看看是什么内容

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QvAvvyrGkxkA7icADnxxf37YMCUILTK2Af7akokXSesmlLSKHMurQ5Gw/640?wx_fmt=jpeg)image-20201106125418777

`"tips.txt"`中记录了两个文件路径，访问看看

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QRe9HqHouQC9FbNYZDn5Eia9qhsNthibbibU6v8iciaLxDoxzZXIQygweL9Q/640?wx_fmt=jpeg)image-20201106125534423

`igolder`目录下有一个文件，我们下载下来，`zip`文件也下载下来

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QxwcbXeEicMFLz94TUnUIOfJibGb3YdqXtZgn2IjkmtEOXmwTQ2wmcXsA/640?wx_fmt=jpeg)image-20201106125615750

##### **0x3、文件信息收集**

打开`"clue.txt"`看看

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QBZ6yYCG2ZBB8ORFsIrkAwfbd0jC7tFyRgAMOPovoX14jaC2Aaw2W6Q/640?wx_fmt=jpeg)image-20201106125705850![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QEibpg8gT0DAF0dRSwDWpkrOMzp6VkL4p1nPbtVtez6AdKaF8xbxoKTQ/640?wx_fmt=jpeg)image-20201106130041774

应该是一个`PGP`密钥，还有一部分`PGP`加密的消息

再看看`zip`文件

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QyKXrr20emeicEZ1sN4VFic9HR0icJLZ3KJ21ltMcYeDLk28OQOL4wGWMA/640?wx_fmt=jpeg)image-20201106125751439

`zip`文件似乎被加密了。密码应该是`PGP`密钥里面。

我们可以拿到在线`PGP`解密网站上解密一下那串消息。

当我搜索 `PGP`在线解密的时候出来的就是 `igolder`这个网站

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QgSwQqTleyK88XAWuQWsuaROMSIF5byo2XzD3tey9oDlGwgmBQ16jnA/640?wx_fmt=jpeg)image-20201106130213617

我们把`PGP`私钥和消息粘贴进去，解密出来是一个提示：

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QQQ3LPPWc7r0Rawz2sQKqiacPAlOfm93Wljs7T2BaEO6UWibvCJicabSyQ/640?wx_fmt=jpeg)image-20201106130341552

提示说：取证人员忘记密码了。但是记得是`6`位数，前三位是`"for"`, 后三位是纯数字。

既然这样我们只能暴力猜解了。我们可以先用`"crunch"`工具生成字典，然后用`"fcrackzip"`去破解`zip`文件

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QDAyMYnNcsiapMRXbUU2Wpv4RFvAD9CiaQnmQEoMaxfucwFZFmb6QuIRQ/640?wx_fmt=jpeg)image-20201106131118578![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QQPNbKphibibrDBRVUfTwo2iav522ToMjQUNhao34NZLt3micR9iaLyiaGpyQ/640?wx_fmt=jpeg)image-20201106131209606

解出来密码是`"for007"`，然后解压文件

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QD4Iibm4EfAzYrJmSf7j1zpFfTk6RsCMInbugHmYVGZH8pZvbUlCuKwg/640?wx_fmt=jpeg)image-20201106131540632

有两个文件，一个是`pdf`文件，一个是`dmp`文件，从名字来看，是`windows`的`lsass`进程的内存转储文件。

先打开`pdf`文件看看

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QygMUzh3XibtOmdibUurxN8h1slHOT2ib4SsSdWFP4IVoZabr83ApAjoFA/640?wx_fmt=jpeg)image-20201106131742744

找到第二个`flag`了。

这里我们可以用`mimikatz`工具检查`dump`文件

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Ql6w3c52icx9AqF9M85s2N39vLccJELF5qliccqz9h2sgfsqSILx7udmA/640?wx_fmt=jpeg)image-20201106133433730![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qu8AxbxibAkp5lbib41ia8dg33MERJ1Hyusgr5Wd1Du93xuI3Vft61ibSxg/640?wx_fmt=jpeg)image-20201106133535792![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Q9ooKqZQFAZUC98ZsSeXL9DUXdjVnIx4PsXQticicB9Ln4U0IVdibH1nKQ/640?wx_fmt=jpeg)image-20201106133610778

可以发现有两个用户，一个是`jasoos`，一个是`raj`，`mimikatz`没有直接读取出密码明文，我们可以试试破解`NT Hash`，用`John the Ripper` 工具试试

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qko2p5kD4n45RPXADmAkicUeobicp3XGMm9RlgKicP5IWiao9rQhUrhVrug/640?wx_fmt=jpeg)image-20201106135456622

emm，很慢，我们也可以找一个在线网站破解

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QqwnHVoebrY0rdFvibp8r3Ld1Eq0GalowSAd2lInjhEWjaqm7ibibMJvjA/640?wx_fmt=jpeg)image-20201106135529943

快多了，一下子就出来了。

##### **0x4、目标主机信息收集**

`NT hash`解密出来了。但是目标机器是一个`Linux`，开放了`22`端口。难道就是用的这个密码吗？

试一试吧，为了方便后渗透，这里我们使用`msf`里面的`ssh_login`模块

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QZ4oYa9ITxexBayLhZsxmqj7pw0LSoy4HcVQgTBhfYacrmsBS0VHXAw/640?wx_fmt=jpeg)image-20201106140300466

可以看到登录成功了。我们可以用`session -u` 升级成一个`meterpreter`会话

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QFibvjOpw6Z8n0bJIRxK4iaF0FDDZnODaPMNt7yyTufMSiab55C14HtcZg/640?wx_fmt=jpeg)image-20201106140524468

我们发现目标主机上有多个网络连接

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qy9FWqCXFCSrWxLZLp2ZwK5XASjnaygxtWBvOdrxVib92X1MwGg0DG4Q/640?wx_fmt=jpeg)image-20201106140656545

##### **0x5、横向渗透**

我们利用`msf`后渗透模块的路由添加功能，添加网络路由，然后对目标网络进行扫描

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QQgqHT5b2F3pOibLTxq8icBicNeE0khvsN4DJPB6icLR6VDzuCQTuyhEqZQ/640?wx_fmt=jpeg)image-20201106141113677

然后探测一下目标主机

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QX1aetNiaIzILpUlsqXibCtia0n9pIibRYFhqjehqn85LpSpH8CZ7FcaPOA/640?wx_fmt=jpeg)image-20201106141200851

发现一台目标机器 `172.17.0.2`

接着对目标进行一下端口扫描

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qkr0yvuIpCla8o1F1045Nga0cP0OBBL9PeXhxkdQ84IgPHiaNSo5ciaaw/640?wx_fmt=jpeg)image-20201106143201694

发现目标开放了`21`端口。我们可以试试`ftp`登录

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QtYLecXic7cVm1MJYxX6yAmmOBOlbV4zbp5WyUpXHoy0yTvB3uocXmJQ/640?wx_fmt=jpeg)image-20201106143319458

发现可以使用匿名登录，我们试试登录到`ftp`中。先切换到目标主机的`shell`中

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qx5OszRNU7j7RoDiaSPwp7s8U34J8sLwCMxBbhVAOgnC6Yeb5BicKPmHQ/640?wx_fmt=jpeg)image-20201106143556803

但是这个`shell`有点难用，我们可以调用`python`实现一个友好一点的`shell`，然后用匿名账号登录到`ftp`

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QGiaDJDn6hKzhUWJQ0312g7icnC3Xk3b99rNxJ3HRGJytzRRd8PEvSa5g/640?wx_fmt=jpeg)image-20201106143944579

看看`ftp`中都有什么文件

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QUur6kgfaw4K2SJW3kibED5SxI8t9QOziaH8LkxaZILCEWSUmGBviatbGg/640?wx_fmt=jpeg)image-20201106144042450

里面有一个`pub`目录，目录中有一个`saboot.001`的文件，我们把它下载下来

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QtAftaDj7JBzmiccvxrL4E1ibQYuFiahICAuS75DdbWa4m0VsocT20iaoZg/640?wx_fmt=jpeg)image-20201106144127636

然后把这个文件下载到我们自己的机器上

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QY8U6H4Oj8cvVURmkNRDVfbWhZyqQDiaiaArHogvFefrF4FwRV9XpRqSA/640?wx_fmt=jpeg)image-20201106144456573![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Q4FpKcBaLhIXoN7FHpGP5gw6X6u3MAELX4UtnIfA5g04Zo2dXdMHzUQ/640?wx_fmt=jpeg)image-20201106144510774

下载下来后，看一下文件的信息

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QYWJDFCCl8dsLcJHoTttkIFGc8ibfkHdbGdGz0hEsaPwCyEF5oeDM96Q/640?wx_fmt=jpeg)image-20201106144704788

看起来是一个磁盘镜像文件。我们可以用`autospy`加载文件进行分析。

##### **0x6、磁盘取证分析**

在`Kali`中找到`autospy`

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Q4oibpv9p11P6tMJyx7J7jQbAHNhm0g819HVEZzlALpcPFATv6rN8ncQ/640?wx_fmt=jpeg)image-20201106144840575

打开软件然后加载 `saboot.001`文件，新建`case`过程就一一详细说明了

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QeIXgtbicWWiczqP5QNOYyEEsro6WDqPNDc7esOqnWbcMM0L9JqaOep9Q/640?wx_fmt=jpeg)image-20201106145245972![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QEZddw8khqg7S3MPlCiba3Sybv7J2Dv3TocgDo2jqRcLNCwBsovxVr6A/640?wx_fmt=jpeg)image-20201106145442620![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QPcoDOKHrxqMoicib1ib62F1ZibqicAlAicVJA3L15MibKxqS6X9XRrvmlRibzA/640?wx_fmt=jpeg)image-20201106145503515![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qvgq2NaQibfLfmSeQAjzpcJ2Z5LiasHbpaGGwhrKUXCDtkdYroT5ag3pg/640?wx_fmt=jpeg)image-20201106145543802

把镜像文件加载进来：

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QYyJbCVAaG1CVSjsclgU9rrgqd08ficUMdJ0uiaA2SakO2iamyHYcvmjEQ/640?wx_fmt=jpeg)image-20201106145609394![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Q66m0xPicmIiaicBplMo6cDvianm05Sh8uwibwqyzDTSeXnZ5xd2wsIPXkMw/640?wx_fmt=jpeg)image-20201106145707624![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QdWuzPwXNIOsVTmvDEK5GrElNYRjUq1spc1FuypdvicjibucBdHU4KMMg/640?wx_fmt=jpeg)image-20201106145731771

添加完成之后，点分析文件

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QUuW6Kzp7k4K1rWia6EnzmlianCicqJH2ELl0sMtQ1gZ0xqXibmS8oZmOsA/640?wx_fmt=jpeg)image-20201106145814152![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QTh4HpwIqoGAPJBfBskPJ3eXwiaQic2XQu3pCGiaWjmKZ8HZWRTyKiaGlzw/640?wx_fmt=jpeg)image-20201106150226617

然后我们发现有一些文件

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QUlL4EmwOhRl7ibZCL6Tgczx1z0xTQZVXtUbhFKrNN25eWa9j9ByPsnA/640?wx_fmt=jpeg)image-20201106150253228![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Q8dDuor7aTEJUMmg9qeNx7PwFRsapF8asoUbSqT95Kc8GPjWQqYTtbw/640?wx_fmt=jpeg)image-20201106150350825

发现一个`flag3.txt`打开看看

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QN8KeoChlbeFYywS0lOIveCw1YrNInLQcbUTY1vm4NUZuSBicrZgaDPA/640?wx_fmt=jpeg)image-20201106150431393

第三个`flag`到手

还有一个`creds.txt`的文件，我们打开看看是什么

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QaE9l9VrV43iagUnewWqBeRxCqdp33QFtqZ4tYFFNNibkxlwGQnYckF5A/640?wx_fmt=jpeg)image-20201106150525538

看起来像一串被加密的字符串，有点像`base64`编码的

试试解密

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QKMDE9M2zibvp07jTHutoNfadI4p3k37VDhOZZiawj8aHiazAqWKUzuOfA/640?wx_fmt=jpeg)image-20201106150642121

解密出来是`“jeenaliisagoodgirl”`

然后这个`saboot.001`就找不到其他有价值的信息了。

当然也可以使用`FTK Imager`之类的软件加载磁盘镜像也是可以的

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QLAnuUEgIcgO54Fv8veHaHxLoXHbMdAjfdEcAbicIYABvZt71aU4k3xw/640?wx_fmt=jpeg)image-20201106163528001![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Qbs4h7Zu5g6C2zEhAiaIdk0gYcGJFibjN76meiaJcpjyXojCMARVudPkCQ/640?wx_fmt=jpeg)image-20201106163044823

##### **0x7、目标主机分析**

我们再次回到目标主机，看看目标主机还有什么线索

目前我们得到的目标主机`shell`是一个普通用户

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QBdHCL3CKr5ia7uPicQeETvIibLR3VIoEZwSbfiatCdQc9hGGRRBjxWiciaiaw/640?wx_fmt=jpeg)image-20201106151108615

看看是否还有其他用户

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QiavpwSBqbGLCoXJNWpUyUjyKPbD5pCNria2rwvT4pav5otJ5NgtuuOvg/640?wx_fmt=jpeg)image-20201106151129721

发现一个 `forensic`用户，进去看看

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QIl8bChKeoeVGBiab86jd9iaN3Y4h9ueLVXUJWLJQhDu5bsWx3FvtDvaQ/640?wx_fmt=jpeg)image-20201106151224335

没有发现什么有价值的线索。

看看`root`用户下面有什么？

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QdVRXjmQzLasJNZXffrPZd6LASEW48k39yY4R1BNsAqtm6lglL8CXXA/640?wx_fmt=jpeg)image-20201106151307993

发现没有权限查看。

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QSH25ia5U3zic2aibY9gY0KibKE3VIzqSRrSNq0eJNm0TWgx5NuPictQ65ibw/640?wx_fmt=jpeg)image-20201106151442855

`sudo`也不行

试试找找`suid`程序

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Q2HYGbrQP26ODpnmKXlugT8fXOELYic89Wy9VR3D7mibhDBSj69zqicsPA/640?wx_fmt=jpeg)image-20201106151751409

发现没有可利用的。

试试切换到`forensic`用户，尝试用`jeenaliisagoodgirl`这个密码

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QZYgkJrncg2TxttY4rQsm33qkexaCZbyfwdVmicCO4vzkH8FpWxhbTWA/640?wx_fmt=jpeg)image-20201106152034288

发现成功了

试试这个用户是否有`sudo`权限

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9Q2JM9KhMj1Yxy6ibh1TntZqibDRxFX9r0GSh9eNicuoWaiazhT1Se0dFxtA/640?wx_fmt=jpeg)image-20201106152225409

发现是可以的。而且可以执行命令的路径有`/sbin/ /bin`这种。那么就可以直接`sudo` 查看`root`目录中的文件了

![](https://mmbiz.qpic.cn/mmbiz_jpg/3RhuVysG9LeFicm6xWQC7riamk1UCELQ9QHWFibTT3Q9G8TUN5x8pTmyYqKiciciaWIHyv1YUYq4S5w7UuVaKfVMM7xw/640?wx_fmt=jpeg)image-20201106152515067

成功得到第四个`flag`

至此，四个`flag`都到手了。成功完成了我们的任务，比如 node 只在原型链污染有接触过一点点，但却没有深入，还是要继续努力。

**12/3**

欢迎投稿至邮箱：**EDU@antvsion.com**  

了解稿件投递相关

请点击公众号菜单：【来撩我吧】- 原创征集

有才能的你快来投稿吧！

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDH643dgKUQ7JK7bkJibUEk8bImjXrQgvtr4MZpMnfVuw7aT2KRkdFJrw/640?wx_fmt=gif)

快戳 “阅读原文” 做学习人