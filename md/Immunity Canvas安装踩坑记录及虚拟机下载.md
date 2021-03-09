> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Ri_MCXTKSsHqOKEGOse1Cw)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

 |

  

**0x01 前言**

这篇文章来自@Norah C.Ⅳ老哥投稿。爆肝两天，终于成功了……，从Windows物理机、Win10虚拟机、Ubuntu 20.04，到Ubuntu 18.04，太难了，简单记录下安装过程和踩坑记录。

  

**0x02 Immunity Canvas介绍**

Immunity CANVAS为全球的渗透测试人员和安全专业人员提供了数百种漏洞利用程序，一个自动化的漏洞利用系统以及一个全面，可靠的漏洞利用开发框架。详细使用请移步：

*   https://www.immunityinc.com/products/canvas/tutorials.html
    

  

****0x03 工具下载****

**安装工具下载链接：**

Immunity Canvas 7.26：

https://pan.baidu.com/s/1uQzvbxsAGLybKiA29Jby_Q

提取码：3wi5

  

**本人已安装完成的系统链接：**

Canvas：

https://pan.baidu.com/s/1AhHAQo2rr_eyYUaBNu1oTA

提取码：gaun

  

已打包好的系统为Ubuntu 18.04，用户名charon，密码root。下载解压后用VMware导入即可。

  

**0x04 安装过程**

下面简单写一下自己通宵肝出来的版本，之前在物理机（Windows 10）、虚拟机（Windows 10）、Ubuntu 20.04搭建并没有成功，小问题居多一些。

  

**一、虚拟机安装**

下载Ubuntu镜像，我使用的是ubuntu-18.04.5-desktop-amd64，其他环境自行测试。系统安装过程不进行赘述，不会安装的请移步：百度了还不会就不用玩了，安装Ubuntu时取消勾选更新选项，安装过程会快很多。

  

**二、备份源**

安装完成以后，先不要着急安装工具，备份一下原本的源。

```
sudo cp /etc/apt/sources.list /etc/apt/sources_init.list
```

  

**三、更换源**

```
sudo gedit /etc/apt/sources.list
```

我这里使用的是阿里源，更换之后保存退出。  

```
`# 阿里源``deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse``deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse``deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse``deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse``deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse``deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse``deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse``deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse``deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse``deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse`
```

  

**四、安装工具**
----------

解压工具之后改一下名字，原文件解压之后带有空格，文件名中有空格安装会报错。

  

换源之后先更新一下，上一步更新完后若执行过此步骤可忽略这一步。

```
sudo apt-get update
```

安装所需的依赖等，复制粘贴就好，多的不说。  

```
`sudo apt-get -y install python-pip``sudo apt-get -y install gtk2.0``sudo apt-get -y install python-glade2``sudo apt-get -y install python-nacl python-bcrypt``sudo pip install pycrypto``sudo pip install pyasn1``sudo pip install diskcache==4.1.0``sudo pip install asn1tools``sudo apt-get install -y python-pycurl``sudo apt-get install -y libcanberra-gtk-module``sudo pip install pycurl``sudo pip install requests``sudo pip install pygame==1.9.2`
```

全部安装完成以后，进入canvas目录下，执行安装命令。一路回车，等待工具安装完成。  

```
sudo bash install/linux_installer.sh
```

  

运行启动脚本，看到如下界面时即为成功安装。

```
sudo python runcanvas.py
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfvKMp6fX8iaYM7VJAXhzzuVy8C2400bC4hbNzAqKqxw0CQKwSwCLjo5XjNgPuQe1b3zHyLTt5RQrw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

**五、测试**
--------

打开Canvas的Configuration选项，查看一下是否可以配置，Windows环境下安装完成后无法进行配置。芜湖，起飞~~~~

![图片](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfvKMp6fX8iaYM7VJAXhzzuVC9IorZtoLpNt1I6teDvTBvdibqLgHh01e5uFEdQrznfwjBbKrUTAdng/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

**0x05 踩坑过程记录**

**一、Windows环境安装**

**Windows环境下的主要坑点为：**Canvas依赖包安装失败、依赖包安装不齐全、数据库无法启动、依赖包请求超时等……

  

并且在安装完成后会卡在启动界面很久，加上有后门版本的Canvas流传不断，即使是用Windows环境下测试，也尽量使用虚拟机去搭建测试。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOfvKMp6fX8iaYM7VJAXhzzuVRuVFia63eicPubCSCF1WkBB1flTyrbb001ZF4MHWEjflicuRcicoicb7PZg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

**二、Ubuntu环境安装**
----------------

第一次在Ubuntu 18.04中安装时出了点小问题，安装过程都正常完成，但就是无法启动，以下为报错内容

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

在Ubuntu最新版的安装过程中，python-glade2安装过不去，乖乖用回18.04。

  

**0x06 总结**

爆肝两天，测试了多个环境，总算是成功搞出来了。嫌麻烦的可以直接白嫖上面搞好的，感谢我捉少爷和蜻蜓大帝，在我安装过程中跟我唠嗑解闷。

  

* * *

  

只需关注公众号并回复“9527”即可获取一套HTB靶场学习文档和视频，“1120”获取安全参考等安全杂志PDF电子版，“1208”获取个人常用高效爆破字典，“0221”获取2020年酒仙桥文章打包，还在等什么？赶紧关注学习吧！

 ![潇湘信安](http://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6YLhRjHMxGMsH55CSVdlMC0XEwtoAQI06hia8rd371BcDnQ8bfRmP4YqA/0?wx_fmt=png) ** 潇湘信安 ** 一个不会编程、挖SRC、代码审计、渗透测试的业余网络安全人员，该公众号主要用于分享个人学习笔记、安全经验以及各类疑难杂症！ 73篇原创内容   公众号

* * *

**推 荐 阅 读**

  

  

  

[![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486401&idx=1&sn=1104aa3e7f2974e647d924dfde83e6af&chksm=cfa6afd2f8d126c47d81afd02f112daea41bce45305636e3bba9a67fbdcf6dbd0e88ff786254&scene=21#wechat_redirect)

[![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

[![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484585&idx=1&sn=28a90949e019f9059cf9b48f4d888b2d&chksm=cfa6a0baf8d129ac29061ecee4f459fa8a13d35e68e4d799d5667b1f87dcc76f5bf1604fe5c5&scene=21#wechat_redirect)

* * *

**欢 迎 私 下 骚 扰**

  

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)