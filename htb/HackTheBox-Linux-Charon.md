> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/srKC3Te68UrhN3Wtd8RVAA)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **108** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/42

靶机难度：中级（3.5/10）

靶机发布日期：2017 年 10 月 7 日

靶机描述：

Charon is definitely one of the more challenging machines on HackTheBox. It does not require any advanced techniques, however there are many subtle tricks needed at almost every step of exploitation.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/eLJRzA69wl7hIRHbBfpwg183icXPqYhOnfYicXOtt4iclEsBT585JmXFvq05Ieibib0szIulE9r8BG58HzUePwUpxhw/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/a4ItSXeSn34KK6iaF0mInaXAJY0DKkhF28NjydHiauDm4iauOatMfIFxgh9L8ic23wb77htyqURBGSWK3yib68EZUQQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPNwpMTVeicswMxbfAHOM8Fj7ibSw8aEudibQhKE2ib2st3wsJL34IDmxVaA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.31....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPhRybQHUWIUJZ31YbAMtnmkClOgkTzIjOb8dWMp5rnQCDbq1VbdmB3g/640?wx_fmt=png)

nmap 发现开放了 OpenSSH 和 Apache 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fP2icbHZUcPar2L24FBcZ0tBJsibwibArBkbUZgAVf1tSib0ib58AEfctd33A/640?wx_fmt=png)

查看主页面没发现有用的信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPWjwhhf5K4EQeGU1TQ2FnjQPPZPad1I6GT2d5SkeAhwbibDw3w87YLXg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPImQxUtNZU5fWDhDYnxAj6kpibeTM8WB73Urer4O3SKIvWYVfcDicDSZg/640?wx_fmt=png)

通过 gobuster 爆破发现了有利的 cmsdata 目录信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPAPrJ5ibrjSwb0j9vhb6myGCtcv7sLGWKcUZNjhSqfPsPOiadF6Dibx0jw/640?wx_fmt=png)

通过访问，这是个登录页面还是 SuperCMS 架构... 又要注入了... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPwrGHgFejf9ch752WAdQu4a1ovXBiappXy1icY5canN5IVGSd1qGHA4xw/640?wx_fmt=png)

通过点击 Forgot password 跳转到了 email 页面...

使用 burpsuite 捕获页面的请求，并将其发送给转发器....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPwzujdRF8letYfeTR6oHWqiaH3g5Wf9r6UPPHzap2SEQpLicvRVeu4Gyw/640?wx_fmt=png)

通过简单的测试后...

知道该站点容易受到 SQL 注入的攻击，首先我找到列数，使用 ORDER BY 命令查找表中的列数，找到列数后，我使用 UNION SELECT 命令为输出列名称提供相应的编号，由于 UNION 和 union 已列入黑名单，因此我将 UNion 用于 SQL 注入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPYZrqQ6o8SmFZYwmEl6091zxwWeHiaDOVELOJOVOibjblY4TOdqfF38bw/640?wx_fmt=png)

```
for i in $(seq 0 100); do
        payload="email=a@b.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ':', TABLE_NAME, ':', COLUMN_NAME, '@b.com') FROM INFORMATIoN_SCHEMA.COLUMNS WHERE TABLE_SCHEMA != 'InformatiOn_Schema' LIMIT 1 OFFSET $i-- -"
        curl -s -d "$payload" http://10.10.10.31/cmsdata/forgot.php | grep -o '[^ ]*b.com'
        done
```

经过大量的测试，我创建了简单的脚本，方便查找用户的 user 邮件名称信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPGITibCEfGUOJYdgIibk8xjFlosbc4XGP43iaygwMGj9gnxOoWMUhcyuNA/640?wx_fmt=png)

通过执行自动化脚本，获得了 `__username_@b.com` 和 `__password_@b.com` 两个有用的信息... 这里利用这两个邮箱信息继续编辑获取密匙...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPwzBW2Em9XwiangmxlqFNCddynEBXqne1QFib0tFaTWIVq8viaMJBic9C0Q/640?wx_fmt=png)

```
for i in $(seq 0 300); do
        payload="email=a@b.com' UNIoN SELECT 1,2,3,CONCAT(__username_, ':', __password_, '@b.com') FROM supercms.operators LIMIT 1 OFFSET $i-- -"
        curl -s -d "$payload" http://10.10.10.31/cmsdata/forgot.php | grep -o '[^ ]*@b.com'
        done
```

继续简单修改了自动化脚本，测试时 100 输出都是重复的 hash 值.. 我改成了 300 后，出现了有用的信息...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPh5ACJNWsYGvdsD74YOHK8LLx0iaibBA4mBj0gD8JjibmnvBBd7bBdMFcw/640?wx_fmt=png)

看到，在 201 后，获得了 super.... 的用户邮箱和密匙 hash，这应该是有用的，试试....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fP8AZ2l89U9RHHhIGNOWDEIxRT1IvQLpvlibHlyLXQAfqJN6MDeHcw29g/640?wx_fmt=png)

成功破解获得了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPe2AtYL5iafc2DhXZFDxunqbhbYYjj7CWcUzPpyXWHePZibgaoCOfoHmA/640?wx_fmt=png)

通过账号密码成功登陆了页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPPPHgChUDOa3etEJov7ibodoQF1O4sBw2krZb8ItaFGLALQ9Fkrhxiapg/640?wx_fmt=png)

发现页面存在文件上传功能，通过上传文件简单测试只允许 jpg、gif、png 格式文件上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPXMias88M1GhMAcibQaiaUZdkAtvH1T7wAtNf5Gib9Mlg829LTSTqKajNIQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPuoSXyDFoE2O3eUGEVULMsmkNkg6ELJzzP4ZzaOkItLO75YB83gnXQA/640?wx_fmt=png)

修改文件名，上传后发现报错了，仅仅能上传图像文件....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPrUXuMAmbU5Iic2pbScS98YCriaRzNiaOmT1fEddKKruqgIyysXyUVLRiaA/640?wx_fmt=png)

并在前段源码中发现了 base64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPYG0fI5lGlAJGZEWPfibCBAibFJBMAibDIbZMN4pzyuXwRl9ghwz8hNqSg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPTEuk4xMM0ANSCmwF0Aoia0P0jHYa6ia2iaykPUDawBgxmwnLKaugryeew/640?wx_fmt=png)

解码后得到 testfile1，所以很明显，这是一个测试上传的工具模块....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPYE7I9ibZCUMmyBHoNCumVMDpNNQtezfYcmtvzpyQMW7IyEQmwibVianVA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPk9BPurgpR7t4yvCaopbh4rgPJEUSBt0wyfC4JgwXw5p6WYeia6PLzcA/640?wx_fmt=png)

尝试上传 shell，命名文件名，并将一个反向 PHP shell 插入其中，以绕过图像限制... 成功上传了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPvveLRMeYs7vVInFrFNaxpXfOCFrpdiaxkRF7pe0WWKN90qp0jKUU2Bw/640?wx_fmt=png)

简单成功测试输出...whoami

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fP7ibdwa5viabFoHZxezGVvYOOibAfXr7TicnqlpeW08Txiag5bCga9lfautw/640?wx_fmt=png)

利用简单 shell，获得了反向外壳，获得了 www 低权却无法读取 user_flag 信息...

需要继续提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPPPveeymy03WPzFuvslP0XhH0zmpp4xD4G3ic6mmwsv64btPxO7ibl4JQ/640?wx_fmt=png)

在 home/decoder 目录下发现两个 rsa 密匙文件... 下载到本地进行爆破看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPGibM16Zgl9W0ZHWnXAvQHevf5ciamy1aMh4sCMQVHwowIiaCAMDM9svsA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPXau9mSuthoVOMm17nYDCgicTqSsVsJsvfa0fVicVGXwoVOLtjUqV3Umw/640?wx_fmt=png)

google 对该两文件进行搜索，需要利用：

```
[RSA](https://github.com/Ganapati/RsaCtfTool)
```

工具进行解密... 下载即可  

执行查看 help，利用 --publickey 和 --uncipherfile 命令顺利破解，获得了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPl3gNMGYibZuad3KThqULyhl6XybE7YBetzKiaF2EqYyyutcZoxjR8QPg/640?wx_fmt=png)

namp 前面就扫到开放了 SSH，利用用户密码成功登录... 并获得 user_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPLtS5mjtY4XPFgnGfic5PSoADkVUZ4YWoTGR550pfic79xjaqP3Vk71Lw/640?wx_fmt=png)

上传 LinEnum 工具枚举所有可利用信息... 在 SUID 发现了 supershell 二进制程序.... 进行下载到本地进行分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPZiazibpwG2Owmw4zfHVmia6r4cXubvjpI7kSibemFdQsIzGsCuhq6xtdEA/640?wx_fmt=png)

利用 IDA 对二进制程序进行了分析，可发现改程序仅在运行 / bin/ls...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPzKicSQtX72ibHc6hEYcSzXN3YT2f3Oyg5zey08HodiaYkP3AGtlsfs1Sg/640?wx_fmt=png)

经过一些测试后，利用运行 / bin/ls 会输出完整文件内容.... 因此输出了 root_flag 信息... 但是还是想要获得 root 权限...

通过另外的测试，创建了文件夹 dayu，尽然可以因此执行 root 权限读取文件信息，利用执行 / bin/ls 也可以将文件提权到 root 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fP2iaHj5SHqK4RC4mUmUaUIoHWia897jEYWwR3ibNWzhFXHOY1tI1ibedhtA/640?wx_fmt=png)

为了获得 root 权限，我简单编写了二进制编码，并利用 GCC 编译，如果由 root 用户运行（或设置了 SUID 位），则将 uid 和 gid 设置为 0.....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fP4IxvUYjAhya7bAK2xjtoVzDge5laiawNBKLfNcwp05alDSDeJFtEChQ/640?wx_fmt=png)

将二进制上传后，利用 / bin/ls 提权 dayu.me 二进制位 root 权限执行....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEBuy1iceZicWmqEEr7gn6fPkcwxhGh4kK1ibbZLhdYDl0qUGq5OVAgM6xIEGdgkcDQYXz40IBCibU5A/640?wx_fmt=png)

通过设置为 root 权限的 dayu.me，直接执行获得了 root 外壳.....

![](https://mmbiz.qpic.cn/mmbiz_png/QkjvmbC1CD0zJ9hBlrElSv4ZqETGn3otgH8VHW1QuoOec3JMAbUyr0iaurJy4DPHBwUsDXiadJ3aha4CvJwyYVew/640?wx_fmt=png)

爆破 + 注入 + 破解密匙 + 解码编译 + 分析二进制程序到制作 shell 提权的过程....

又学到了新的东西和巩固了以往的知识....

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)