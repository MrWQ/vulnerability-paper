> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/nhqa_qZK6ELABfwczDdTbQ)

### **0x00 前言**

大家好，我是 Jihan，最近复现了一个非常有意思的靶机，就想把它分享出来。本人小白一个，文章写的不是很好，希望会的大佬勿喷

### **0x01 靶机环境**

#### **1. 靶机下载**

###### 下载地址：https://download.vulnhub.com/meandmygirlfriend/Me-and-My-Girlfriend-1.ova

###### **2. 靶机介绍**  

```
靶机难度：简单
靶机目标：拿到两个flag
```

#### **3. 靶机导入**

##### **第一步：导入（打开虚拟机 --> 选择下载的靶机 --> 选择存储路径 --> 导入）**

注：会报导入失败的错误，点击重试即可。  

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibwt3IXsN9WJch11JkRPpicIrTF2giagd52F3Cpgz3b5wdyemJO1sEHLdw/640?wx_fmt=png)  

                              ![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibibryF7XWVMkZcX0FATdcQkqdA1Fr9SeiaaXkBq5pXgv0kjO1pl0tp8Cw/640?wx_fmt=png)

**第二步：导入后，删除网卡并重新添加（NAT 网卡）  
**

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNib1KxIF7gB1GADr4HiaFUJEnd3hMlfYJxNicwrPFHaCADYSQF0ESJmDTFA/640?wx_fmt=png)

**第三步：启动虚拟机  
**

### **0x02** **信息收集**

### **1.  nmap 扫描确定靶机 ip**  

```
nmap -sS -Pn 192.168.159.0/24
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibEmGh9vueg9GWdibvmg3SSv1SaBDmiaZbcnZBFr58o2HLRDnqM1jR3BbA/640?wx_fmt=png)
==============================================================================================================================================

继续扫描

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibpYtQ354K7Zh0jeSFJW1AxYib4OvBCpON3T7repXtsY7g0ctBx4ASz2w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibB0iaLoykibjsAMD4m3gtichhfl7VoshLNjO5HyPHLGZZQqdbwl3NjoUbg/640?wx_fmt=png)

获得靶机 ip：192.168.159.173

开放端口：22、80 等端口，是 Apache 服务器

#### **2. web 界面访问**

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibupqEn8ftseapcae4PrwZqXic0MeejQ1ouKib4cKZxCcUzyFQMKgt5qOQ/640?wx_fmt=png)

发现拒绝访问，试着查看一下页面源代码

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibvayhL6OkXrSU5LuEsbBN6BRy9ejguhIZdVdibcxunLc7e3Uy7DkR59g/640?wx_fmt=png)

### **0x03 漏洞利用**

**1. 使用 firefox 插件 ModHeader，添加请求头 X-Forwarded-For**

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibv2wweYoRjias8QicR8J9c5RJdFqU3auRyUNIjXkIIg6fqQZE6s9Cb8Og/640?wx_fmt=png)

然后刷新页面，发现可以成功访问

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibPsGzSeexmsIvpkJkDPJvw3zzUKkhqFlcujjavYWaLnt4X9oR2HyX6w/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibJuVZOlYV1Tr3GU5wAhWIkdI3GGXNWlCE7CR84vnDIViag82JPibvvqIg/640?wx_fmt=png)

我们发现，有登录界面

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibRBCficIjK35u0ibfKS86F3ojqjGephPtGrAp64g6GQ36Bvvgxdhb9s8g/640?wx_fmt=png)

**2. dirb 目录扫描**

既然来到这里了，那我们就扫一下目录试试

```
dirb http://192.168.159.173

格式：dirb <url_base> [<wordlist_file(s)>] [options]

-a 设置user-agent

-p <proxy[:port]>设置代理

-c 设置cookie

-z 添加毫秒延迟，避免洪水攻击

-o 输出结果

-X 在每个字典的后面添加一个后缀

-H 添加请求头



-i 不区分大小写搜索
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibS98WNLeUJuTQ6TNhoicOXP6RNHkxppsCsE6RTmqWZeZicRoTcSNg5DoQ/640?wx_fmt=png)

扫出 / config 和 / misc 两个目录，我们试着访问一下这两个目录

**3. 访问目录**

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibPUvL4xYb0rWHqL9U1A466mmQiamJCS4cov6ibItxCKY188tz1GibsicCDQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibaJINYwCibfjbMqOsaibcoicicsMp1QYWlohQuVicVwl6Ymku0EaD581icJUg/640?wx_fmt=png)

打开 config.php 和 process.php，发现是一片空白

有个 robots.txt，访问下看看

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibmoohfdtZH4r6UEKlXKuYB5eetzS5x54LTTEUzWXq9puQVeGZ38nRibA/640?wx_fmt=png)

发现下面有个 heyhoo.txt，哇，有惊喜，打开看看

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibvjSAXThRNs3IcRMtFTNYUNtlXsdGZnfvH2NRDibUrsfFjmq3zy3xXMg/640?wx_fmt=png)

是我胡思乱想了，还是老老实实拿 shell 吧，我们回到登录页面

**4. 登录页面**

在这里一顿乱试，输了个 username：admin，password：123，居然成功了。登录进去![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibNEyyD41FtyIVKzSNb2pvCBjrb83UJs1LxIhqXFkAPUy0S9eX5oOibVw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibPUjycCuUh5LsneJD2kVVPA68spHIyjRZJibicRKibtH0FAhF3NkCd71Lg/640?wx_fmt=png)

我们发现里面有个 profile 文件，点一下试试，跳转到我登录的页面，好了，开整！！！

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibsXayBtCA0T9Az6JTgqj1sNjlXicU0GoIemK5k2jicllMWbWffIEkfa5Q/640?wx_fmt=png)

眼睛亮的童志们想必发现了，在登录后的 url 的参数 user_id=14，而不是 1，那么之前的那些用户名中是不是藏有管理员的登陆密码呢？

**5. 修改参数**

修改 url 的参数为 1：

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibURcgeVZibFlrD1So8xa4kB5voiarGLnQhrWLo3ysEHSp7cx7icdtO3zZA/640?wx_fmt=png)

突然发现框中值都变了，那么我们依次输入值，那么数字那么多，最大应该是多少呢？

最大的数值是 14，因为我们登录账号后，我们的 ID 是 14

想看到 Password 的值也非常简单，右键点击检查，from 表单中 input value 的值即为密码，或者把 type="password" 为 type="text"

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibfUuYyR4BiaGbN1kq0Af1VmwPEuy6yIdUegeHY1j6YNEfRq29WNPR29A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibEkahAnwGcKcGsc3QkAecvHGc0t5a9KgJic9Pibuq3moLp5AHbiblDGc0w/640?wx_fmt=png)

依次类推

将这些密码遍历出来，先放到记事本中。当然这里可以写脚本，本人小白一个，不是很会写，会的大佬可以试一试

```
Eweuh Tandingan
eweuhtandingan
skuyatuh

Aing Maung
aingmaung
aingmaung

Sunda Tea
sundatea
indONEsia

Sedih Aing Mah
sedihaingmah
cedihhihihi

Alice Geulis
alice
4lic3

Abdi Kasep
abdikasepak
dorrrrr
```

这里遍历出 6 个账号密码，那么既然账号密码有了，就尝试呗，还犹豫什么。

**6. 登录靶机**

因为下载靶机的时候，有一个靶机背景 description，所以我们首先尝试 用户名：alice，密码：4lic3

居然成功了

查看一下目录文件

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibI8qouvd3U9BjKoXg0wY2yuerC290icBYWdTUpkcRgTNN4eAtIBYKOiaA/640?wx_fmt=png)

发现一个小秘密，查看一下

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibZr1TPlXoSYiampXmV7z4D92Rs3Bb5WQCkXGcW1gKHfHP7P9EIKUabNQ/640?wx_fmt=png)

得到第一个 flag![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibVzW319WNepEmRX8QwrBlPShtORm5KaribypA0ED1Iw0jdAWiaRGP11pg/640?wx_fmt=png)，并且有一段提示，翻译一下，意思是第二个 flag 必须要提权了

```
格雷特，我哥哥！你看到爱丽丝的便条了！现在保存记录信息给bob！我知道如果给了他，鲍勃会受伤的，但这总比鲍勃被骗好！

现在您的最后一个任务是访问根目录并读取flag^_^
```

再查看一下 my_notes.txt

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibzBtW5s4uxYk3z9iaPppbluZS9FHCwNibKCK17gkibpwdjvdAmFAbhBibGg/640?wx_fmt=png)

```
哇哦！我喜欢这家公司，我希望这里有一个比鲍勃更好的合作伙伴，希望鲍勃不知道我的笔记
```

没啥用，那就整 root 吧

### **0x04 提权**

因为是 apache 服务器，看一下网站的配置文件 / var/www/html

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibWrudoTV4IFO1BtemS2fficwFOpHialOXH1EwE10iaSepWv8JCEmXtMA6A/640?wx_fmt=png)

得到数据库账号密码，尝试提权

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibkf86wux8yRvYwIUOBAFpH2B1TvCUKyuQUENPeUJTpVNWK8pTrO12Ww/640?wx_fmt=png)

拿到第二个 flag，over！！！![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTrnL03eqxgzBYI850HUdUNibl33PWUYzCs4UH6icTZcuGo2Gb36WtrGQ50ibfptphSKCFArjCw2mF7Qg/640?wx_fmt=png)