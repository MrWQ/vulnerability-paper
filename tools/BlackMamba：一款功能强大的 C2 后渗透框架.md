> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/gIsHne-SrJoFbhZzu5Ek8Q)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38aadGAnQic8Czao3L0wOiak2fZqUwrrvjMQlfcY5rxX70hEohtB1IJJt6bToo0uHU4icncibY7iaTyaUw/640?wx_fmt=jpeg)

来自 | FreeBuf

BlackMamba
----------

BlackMamba 是一款多客户端 C2 / 后渗透框架，并且还支持某些网络间谍软件的功能。该工具基于 Python 3.8.6 和 QT 框架开发，可以在渗透测试任务中为广大研究人员提供帮助。

**BlackMamba 的功能如下：**

> 多客户端支持：支持同时连接多个客户端；
> 
> 实时通信更新：支持客户端和服务器端之间的实时通信和更新；
> 
> 通信加密：支持对除了屏幕视频流之外的所有通信信息进行加密；
> 
> 截屏收集：从客户端获取实时截屏；
> 
> 视频流：实时查看客户端屏幕视频流；
> 
> 客户端锁定：锁定和解锁客户端设备；
> 
> 文件传输加密（上传 / 下载）：可从客户端下载文件，或向客户端上传文件；
> 
> 键盘记录：记录客户端键盘按键信息；
> 
> Web 下载器：支持从 URL 下载文件；

工具安装 - 服务器端
-----------

首先，使用下列命令将该项目源码克隆至本地：

```
git clone https://github.com/loseys/BlackMamba.git

```

接下来，安装 PIP 包：

```
pip install -r requirements.txt

PyQt5

Pillow

PyAutoGUI

pytest-shutil

cryptography

pynput

pygame

```

接下来，在网关或路由器打开端口 65000 和 65005，具体端口号可选。为 BlackMamba 创建防火墙例外规则，或直接禁用防火墙。

打开 “BlackMamba/bin/profile/socket.txt” 文件，然后输入打开的端口号：

```
SERVER_IP=0.0.0.0

PORT=65000

PORT_VIDEO=65005

IMPORTANT: Do not change the 0.0.0.0.

```

打开 BlackMamba 目录，然后打开 “keygen.py” 文件。拷贝结果密钥并拷贝到 “BlackMamba/bin/profile/crypt_key.py” 文件中。

返回 BlackMamba 根目录，然后打开 “main.py” 文件：

### WINDOWS

```
python main.py

```

### GNU/LINUX

```
sudo chmod 777 main.py

sudo python3.8 main.py

    KALI LINUX

    (sudo chmod 777 main.py)

(sudo python3 main.py)

```

点击一个人形和加号的按钮，输入待创建 Python 文件的路径，输入端口号和主机的 IP 地址，然后点击 “创建” 按钮。

工具安装 - 客户端
----------

创建好客户端脚本之后，你将需要在目标主机上运行该脚本。

### Windows

```
python script.py

```

### GNU/Linux

下载代码包：

```
scrot -y

python3-pip -y

python3-tk -y

python3-dev -y

```

然后运行下列命令：

```
sudo python3.8 script.py

KALI LINUX

(sudo python3 script.py)

```

注意事项：客户端脚本并不会实现持久化运行，如果你想实现持久化，你得需要自行动手实现。除此之外，客户端脚本可能会有几秒钟或几分钟的延迟，具体取决于通信连接的质量。

工具运行截图
------

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38aadGAnQic8Czao3L0wOiak2J4TmUdrCgzE45A9gRblaxiaTDZO8WTfD6Riayltpb1msnjExrGXMLOiaA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38aadGAnQic8Czao3L0wOiak2ha85NZkW9KNCMuLZZuP8TVHzdBFBVVRKkM1eulYnt0Xq2BMKn1OL5w/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38aadGAnQic8Czao3L0wOiak2e7FxRskp5XxDSljH4YakNfHhWDWDuTrNnzvVBl3gk64YXyCxRfic2bQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38aadGAnQic8Czao3L0wOiak2LvjslEVicWUCBicLAcCB31j5yxu6Tv9lMuz2OdTkDNXEe4IQAhxPGW0g/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38aadGAnQic8Czao3L0wOiak29tvc7icrXMmdFOH0u3mPkiawJ3PDOORcHTmYfjiax0cqQM8tjVCJB6D2w/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38aadGAnQic8Czao3L0wOiak2icXribIbzYpCZSPX19E4XeGDDVr9GsLEEt4DyibYQDy3BUcwSzh0e6BMA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**