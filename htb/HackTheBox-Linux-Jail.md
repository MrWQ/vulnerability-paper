> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/BKZ_p-FV9K-9ZtkvCuvc_g)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **109** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/oIHlBAgsibibaZSBtkWaD9qOibMlGGKG1U6NJ4t4bgUXty0Q6AhXKFcYNEpsWiazic0HyVSyicaSjONOzZ6q74umEtwg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nrhQN3cHv2mGJ5Zp11NuKa7IBOxh9iaVia3yXjAYFuTnjSpCS81z1gb5T803gZDe8jRRykjtd0Oic9xYejeugEyuw/640?wx_fmt=png)

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/45

靶机难度：中级（4.3/10）

靶机发布日期：2017 年 10 月 31 日

靶机描述：

Jail, like the name implies, involves escaping multiple sandbox environments and escalating between multiple user accounts. It is definitely one of the more challenging machines on Hack The Box and requires fairly advanced knowledge in several areas to complete.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/A8ErDBmzzEsR7ggiaQSGgibribrg9F5UGDJHSzxDGGibMq2e9iaZoZ80WAoG5zC3erJpOOp8MVBso1u12B0fQOoUebA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0fb0Y1M6icJJia7t9xsBuUuxZQgOLeWHYicicRpfEiahMz3mlpK0icx8qLpfMLDojhD7IwSE2IalXVBBFs9E1Z88Ka3Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/PRVgXdHra5CzBfuOaOX4dpiaoOia6WZfdos1RiaJEZJG7nrnxTkXBoianpRmkQTmqkmW3zkbaQqjAu6WwBYAmyGibiaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticUJlejYEH840S8AU2OIOYfrwErS3TIn0T21zrMRlGwgrH5iaxGXTRpug/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.34....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJtic2lyYqaPIkVw84uoAINW4H5SeAdibLK24AQicVegUYNkQ213ANWPfgJ8w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticZJxJvQOQTz3NdJzAR9KkCG0VatrIey63SpaQia41kuBSfOBTwXa1flw/640?wx_fmt=png)

Nmap 发现了几个开放服务，Apache 和端口 7411 上的未知服务... 以及 NFS，还可以看出存在缓冲区溢出...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJtichziammYPZRNicRuxIa7icq9h9037RrrAntdKhaMO1ZicdMiaRnPsZP8c0RQ/640?wx_fmt=png)

访问 web，可以看到门口是 JAIL 字眼，要进入应该是和 JAIL 某程序有关...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticTtVg5NvqeEqAJDr2GbuHVXM8ZIYKLHROxAtSE3ovxuNa57x2SZmOvQ/640?wx_fmt=png)

通过爆破发现了该目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticDOSicicCYicicemj87BrPyY0Mjcibibicj8PTl90j2CEMRcib4cN5xxYg1Iqow/640?wx_fmt=png)

访问看到了三个文件，二进制文件、C 程序和 bash 脚本...

下载到本地分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJtic0HJlNunxibJDwKrwzjaXOHibmgx216zzZc0icUxUHOnFtqMkBPwQMdyhg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticEzMx9GhynZa4T7nCuf2kcibPas6oDAo5FC5VAribSHuiaic5mPRAgJoXug/640?wx_fmt=png)

打开 c 程序，发现它是用于某种身份验证的程序，我们还发现它对可变密码使用了 strcpy 函数... 还执行着 4711 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticrSyNagGwiaZQF6dCQI259L3O83DfmjbCZkJ6OXImYXYspK2osAsw97w/640?wx_fmt=png)

在 bash 脚本中，只有少数几个命令称为 jail 服务，通过检查 jail 二进制文件，我发现它是一个 ELF 文件... 通过 nmap 的前面的扫描，对比可以得出这应该存在缓冲区溢出了...

继续检查授予改二进制权限，执行后检查 netstat 并发现它打开了本地端口 7411....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticX0zSLZyRbice33QveAjn6hKlicIcys9GjegYzMGwNkNeSQpw6J9vKZAg/640?wx_fmt=png)

继续在 gdb 中打开二进制文件以查看汇编代码，该二进制文件通过将自身分叉到每个服务器调用而起作用，因此在发生崩溃的情况下，主进程仍将在运行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticccWSiamYLJsMYbBQB5yOjXq0lcBEmXSic7mYpia3LVZ9NbpZrmPsUC0pg/640?wx_fmt=png)

通过 pattern_生成字符串，传递字符串后，就会出现分段错误，并发现 EIP 寄存器被 0x62413961 覆盖...

通过 pattern_offset 获得了偏移量为 28，利用 28 字符写入 shellcode 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticuicDlrNFh5tiblBdgxGDibibfltS6gYre72Rf5Oia0w3lk6A2G7lDAGXL4w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJtic8hhJ1barhPOVhaQibVHhBmAT0iaPhQs8fyZDlaDBu0eVszibOan3nbVDg/640?wx_fmt=png)

这里 shellcode 我利用了 https://www.exploit-db.com/exploits/34060 进行编译... 将 shellcode 注入 28 字节中...

运行漏洞利用程序后，获得了 nobody 用户身份获得一个 shell...

但是 nobody 无权限获取 flag....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJtichLltb5ibmtuIPiaQ9fozG6cL57s8Kjic0bH0zDicTBoRRQNIuzu9Ah3cfw/640?wx_fmt=png)

需要进一步特权升级，目前知道该靶机正在运行 NFS 共享，通过 NFS 找到了共享文件夹...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticV6I7oldfAnaRyAPjhX9nrQqQDT3Zh72vOjGLDquujJLRtYjAhTOaLw/640?wx_fmt=png)

找到共享文件夹后，在本地安装挂载... 装入共享文件夹后，发现无法读取内容....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticsIRyIqfkMeTlC7PvrxDctkOdAiciaAF87pI7ucnacsiaMraibjebaZ6sTw/640?wx_fmt=png)

查看发现需要在本地伪造个 uid gid 1000 的 frank 用户，才能利用 nfs 挂载，然后在执行读取和写入等权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJtictGPJaRhAyQYs9HnkVPxvg7vXiaGyDeSv0QzuARQV1rQuuXUQYx8VDKg/640?wx_fmt=png)

由于 2020 的 kali 本地的 uid 和 gid1000 是 kali 用户占用了，创建了 frank 后修改了 uid 和 gid... 这里需要到靶机中执行个 shell... 才能通过挂在对 frank 用户具有权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticND5EzUghoWBicnWap5Oic6AJayzhCuic4k6eovZTj93dDTZgBeYms7w7w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticLduF1mSSmXOe1mibwl6jciaibOV1d9ecqxlWXGxSQ8ic1TiaUfWDQ6ibRZsw/640?wx_fmt=png)

我在本地创建的 frank 用户权限下，写入了 shell... 并在靶机中执行... 获得了 frank 的 shell 外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticp5iaP66O0iaCjyAvtcsHicdj9up1BPYCrM9pDGHdkgoyPYNbpZN5t02hw/640?wx_fmt=png)

通过 frank 权限用户获得了 user 信息... 并 sudo 时发现在 / var/www/html/jailuser 中以 rvim 作为 adm 用户在没有密码情况下可以打开 jail.c 文件... 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticObfWjd3Ej2IYsYxZ1wdJqqDJ1a5bQaqMV71vIzV5MWqUdwcwYicJZuA/640?wx_fmt=png)

```
https://github.com/vim/vim/issues/1543
```

通过浏览文章发现此版本的 vim 仍容易受到攻击，只需要将以下命令传递到 rvim 中即可...

```
:diffpatch $(sh <&2 >&2)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticibkMnKkQJm0CTrLHFAeOjs5SZia3w7QvMJ23gPEAxU8YMeHIjm3iaVeXg/640?wx_fmt=png)

通过写入命令回车，利用此 Vim 漏洞获得了 adm 用户权限....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticWkWrjYHyIlgLq4lr4vz8CNDu85wTKyYhhbmFjDswCJE5LjGibibH7xeg/640?wx_fmt=png)

在 adm 的主目录中，找到了一个名为. keys 的隐藏文件夹，在目录发现 keys.rar 和 note.txt 两个文件...

阅读 note.txt 文件的内容，并找到一个密码提示，指出密码将是用户 Frank 的姓氏，后跟 4 位数字和一个符号...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticgvQiahWMhCZPJuk1vqJY9hflGoB4U9khq11JRN7VqaI8j2Hjk3HMa2Q/640?wx_fmt=png)

继续查找隐藏目录时，找到另一个名为. local 的文件夹，然后进入该目录，找到一个名为. frank 的隐藏文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticxicc5QSm210xCa6VhkUibp3mffdjoqPzia1DNAt7EOE9FsShricM1ichicxA/640?wx_fmt=png)

使用网站 https://quipqiup.com 并找到解密的文本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticMvkc1RyD3JsiafQibMn3Bne03mogqjyLtRlQHFQv3sJvL3HfpzWpK4MQ/640?wx_fmt=png)

看不懂直接复制 google 搜索... 查看第一篇文章...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticUJxT3xBjlSj0TJnLDSic4JLk2icRan1PoJXicdK6Q1EMKA3MkNwH8hgIg/640?wx_fmt=png)

可以看到这与逃离恶魔岛的人有关，暗示一件事：臭名昭著逃犯在 1962 年从恶魔岛逃生，其中有三名囚犯从恶魔岛监狱中逃脱... 一个名叫弗兰克 · 莫里斯（Frank Morris）的人就是逃脱者之一....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJtic4m7EyNFskM0EtzgYXVFQ4Fg6QzSfcfL0bKzQoblicdaj3t2wFzyMyBA/640?wx_fmt=png)

通过转换程序为 base64 值，然后下载更准确...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticXNOXiaCNGJBGHAVaOHAjd9h6xI83W5UWPNS6KYSIjU5BLCxUMG9hLAA/640?wx_fmt=png)

然后在本地系统中解码字符串来重新创建文件...

解压后发现无法解压，需要密码...

通过前面 note.txt 的提示以及逃离恶魔岛的提示... 得出密码是作者名 + 逃离年份 + 符号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticpfDa08SQyfdiasc6y0icnQP2Vt7VQDiaiawhRVjk1ZiaT2K6mic4Eh7rTHZw/640?wx_fmt=png)

利用 crunch 创建了密码本... 然后通过 john 破解出了密码....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticCic8vbG9qdibpbFfiaFdHGMKfPW0MjFfSfDPIhic3jskcFmaJECTQPeqFA/640?wx_fmt=png)

通过找到的密码解压出了一个公共密钥...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticyjCKZ8fZfibOIcxzJzKs70ukoAkEia62TJoBjj6RAsraT0ChuxiaqmhNQ/640?wx_fmt=png)

```
python2.7 RsaCtfTool.py --publickey ~/Desktop/dayuJail/rootauthorizedsshkey.pub --private > ~/Desktop/dayuJail/id_rsa
```

https://github.com/Headorteil/RsaCtfTool

使用 rsactftool 将公钥转换为私钥，以便可以使用它通过 ssh 登录....（这里前面几章文章讲过了）

成功获得私钥... 记得赋予权限

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP4ZqqG8YcemBnn423ZjJticJd5Og8WgO03djbPiaM3Jh8wksGaCS64zWA8ia2PgvTbsUnGXYI4LglAQ/640?wx_fmt=png)

通过私钥成功登陆了 root 用户.. 获得了 root 的 flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/4MrQO6osIsVQf89k6cRQVkucDSPXwiaT2lKFBmAe70jsicOPXxtPRxL7cJALRNYtmVCO7cDLibmNbwcQoa6v81iasg/640?wx_fmt=png)

缓冲区溢出 + nfs 提权 + rvim 漏洞提权 + rar 解密 + rsa 解密....

学习思路，巩固工具的用法.... 加油

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/KEY1ajicY5OUiaJYibLLdbVsQkiaTQHdtvSQY5G0a5eNiawwMxUpl7wor6gNw2Vne7qqKm1eBnukvFotHvMstib7tCAQ/640?wx_fmt=png)

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