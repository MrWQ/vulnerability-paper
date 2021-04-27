> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/jiGXv-UHexw5R1JSpCHQyg)

![](https://mmbiz.qpic.cn/mmbiz_png/WadiaHnUicJKNk4Qwqc1YMic1icctOy3JickVjbwdxfhZ7cxF47NjHxKAvuK9738OLaHSSUS2Aicj2RT8TvULECygTrA/640?wx_fmt=png)

**目录**

John the Ripper

破解 Linux 系统密码

破解 Windows 系统密码

* * *

  

---

![](https://mmbiz.qpic.cn/mmbiz_png/TN05MmJLxMqMTrcicggdTRKW3Iod235KxHXS0ViaYmQMwu2Qg3ccvpL3EvzRxJewl9S7f3trmH3WC6TkMKmdj2uA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/TN05MmJLxMqMTrcicggdTRKW3Iod235KxmO80TBPVharoCzpHzobJwtoMSqialD3PuvfgaErtyEW9UDf8MsB5uTg/640?wx_fmt=png)

John the Ripper

![](https://mmbiz.qpic.cn/mmbiz_png/c6gqmhWiafyr9hQWuUCPvGMbftRydTk26qAibaE9icrNUeaeGicUjfhFH6ENBknDQ5mWcbEaCxVRuOKvaI0oUMzpPg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/US10Gcd0tQFGib3mCxJr4oMx1yp1ExzTEpzJmgxRa0SwicW55ISLyAvne5xYTdHCf8XBbC681gwPZVTMicsHTzatg/640?wx_fmt=png)

**John the Ripper** 是一个快速的密码破解工具，用于在已知密文的情况下尝试破解出明文，支持目前大多数的加密算法，如 DES、MD4、MD5 等。它支持多种不同类型的系统架构，包括 Unix、Linux、Windows、DOS 模式、BeOS 和 OpenVMS，主要目的是破解不够牢固的 Unix/Linux 系统密码。除了在各种 Unix 系统上最常见的几种密码哈希类型之外，它还支持 Windows LM 散列，以及社区增强版本中的许多其他哈希和密码。它是一款开源软件。Kali 中自带 John  

*   可执行文件位置：    /usr/sbin/john
    
*   密码字典所在目录：/usr/share/john/
    

John the Ripper 支持字典破解方式和暴力破解方式。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8kjdj5Qy5VOZ1HKN6XvqlzdOPOvlTSEfhgADtiaFpTgBKIk30wF7Pibng/640?wx_fmt=png)

###   

![](https://mmbiz.qpic.cn/mmbiz_png/TN05MmJLxMqMTrcicggdTRKW3Iod235KxHXS0ViaYmQMwu2Qg3ccvpL3EvzRxJewl9S7f3trmH3WC6TkMKmdj2uA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/TN05MmJLxMqMTrcicggdTRKW3Iod235KxmO80TBPVharoCzpHzobJwtoMSqialD3PuvfgaErtyEW9UDf8MsB5uTg/640?wx_fmt=png)

破解 Linux 系统密码

![](https://mmbiz.qpic.cn/mmbiz_png/c6gqmhWiafyr9hQWuUCPvGMbftRydTk26qAibaE9icrNUeaeGicUjfhFH6ENBknDQ5mWcbEaCxVRuOKvaI0oUMzpPg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/US10Gcd0tQFGib3mCxJr4oMx1yp1ExzTEpzJmgxRa0SwicW55ISLyAvne5xYTdHCf8XBbC681gwPZVTMicsHTzatg/640?wx_fmt=png)

破解 Linux 用户密码需要使用到两个文件（包含用户的信息和密码 hash 值）  

*   /etc/passwd       包含用户信息的文件
    
*   /etc/shadow       包含密码信息的文件
    

然后我们创建一个 test 用户，密码设置为 password ，用来测试

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8MDCC01hyMQhPPegG3iaYnrWFdxEjfPXIVOw1bu4fnibQsfktPCxu1zMA/640?wx_fmt=png)

使用 unshadow 命令组合 /etc/passwd 和 /etc/shadow ，组合成 test_passwd 文件。其他 test_passwd 就是 /etc/passwd 和 /etc/shadow

的简单组合:   unshadow  /etc/passwd  /etc/shadow >  test_passwd

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8CIAkh2zZQicnB9ZINhUAIicHuTvAdCUk57UwaHxictoIiapvqWL93pPg7A/640?wx_fmt=png)

然后就开始用 John 破解密码了。我们可以使用 John 自带的密码字典，位于 /usr/share/john/password.lst ，也可以使用我们自己的密码字典。我这里就用 John 自带的密码字典为例： john  test_passwd

如果要使用自己的密码字典的话： john  --wordlist = 字典路径    test_passw

可以看到，john 已经把我们 test 用户的密码给破解出来了

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8awFPibBicfTP3Wic4Lv8OW5lLN2IYvBBZXvQiaLmTlbD6QeQvvXuWwgtcA/640?wx_fmt=png)

查看破解信息：john  --show  test_passwd

这里 root 用户的密码是之前破解的，所以一共破解了 2 个用户的密码  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8Sb1ibrfqHNF1BZQCseZS7jJBojw8FNAJD87vT3YpWkcDMfLX29e20Og/640?wx_fmt=png)

相关文章：Python 脚本破解 Linux 口令

###   

###   

![](https://mmbiz.qpic.cn/mmbiz_png/TN05MmJLxMqMTrcicggdTRKW3Iod235KxHXS0ViaYmQMwu2Qg3ccvpL3EvzRxJewl9S7f3trmH3WC6TkMKmdj2uA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/TN05MmJLxMqMTrcicggdTRKW3Iod235KxmO80TBPVharoCzpHzobJwtoMSqialD3PuvfgaErtyEW9UDf8MsB5uTg/640?wx_fmt=png)

破解 Windows 系统密码

![](https://mmbiz.qpic.cn/mmbiz_png/c6gqmhWiafyr9hQWuUCPvGMbftRydTk26qAibaE9icrNUeaeGicUjfhFH6ENBknDQ5mWcbEaCxVRuOKvaI0oUMzpPg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/US10Gcd0tQFGib3mCxJr4oMx1yp1ExzTEpzJmgxRa0SwicW55ISLyAvne5xYTdHCf8XBbC681gwPZVTMicsHTzatg/640?wx_fmt=png)

首先，执行以下命令通过 reg 的 save 选项将注册表中的 SAM、System 文件导出到本地磁盘。需要管理员权限！  

```
reg save hklm\sam sam.hive
reg save hklm\system system.hive
```

```
samdump2 system.hive sam.hive > hash.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm82avjhfF3ibos5nKLq18Uyk3wYuVZB4aicviaxYS3xxbVbVBicdcgT0DhtA/640?wx_fmt=png)

 把这两个文件放到 John 的目录下，执行以下命令将哈希提取到 hash.txt 文件中

```
john -format=NT hash.txt  #破解,使用john自带的密码字典
john --show -format=NT hash.txt    #查看破解结果
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8lyKg5Tw84YicdKZW290D44jM5RdCtD1KQWAh2SEcveG3AXA5PFMjTOQ/640?wx_fmt=png)

执行以下命令进行破解

```
john -format=NT hash.txt  #破解,使用john自带的密码字典
john --show -format=NT hash.txt    #查看破解结果
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8AykjnTDEdXku7WsZOoXiaicq1xcQ9LfHkSnCyInGp98gJyxbakTDQAwQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2el8IVJb5iaQMuhOH5eb7lm8Omjjn7whwQhNk4v8QW0tXHDBfEvXMMqbO8IBTG1x92Iiaw5VLdGaXnA/640?wx_fmt=png)