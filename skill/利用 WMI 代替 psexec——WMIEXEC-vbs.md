> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [blog.csdn.net](https://blog.csdn.net/qq_27446553/article/details/46008473)

内网渗透中经常用到 psexec 这个工具，可以很方便的得到一个半交互式的 cmd shell。

但是 psexec 也有一些问题：psexec 需要对方开启 ADMIN$ 共享，而且需要安装服务；另外，psexec 退出时有可能服务删除失败，这个情况只是偶尔，但是我碰到过。

安装服务会留下明显的日志，而且服务没有删除的风险更大，管理员很容易就会发现。

WMI 可以远程执行命令，所以我就想用 VBS 脚本调用 WMI 来模拟 psexec 的功能，于是乎 WMIEXEC 就诞生了。基本上 psexec 能用的地方，这个脚本也能够使用。

**0x02 WMIEXEC 功能**
-------------------

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-e3e8e7ce5f1f01e53130f2dcc0d38cff_1.jpg)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-e3e8e7ce5f1f01e53130f2dcc0d38cff_1.jpg)

WMIEXEC 支持两种模式，一种是半交互式 shell 模式，另一种是执行单条命令模式。

WMIEXEC 需要提供账号密码进行远程连接，但是如果没有破解出账号密码，也可以配合 WCE 的 hash 注入功能一起使用，先进行 hash 注入，然后再使用 WMIEXEC 即可。

**半交互式 shell 模式**

提供账号密码，执行如下命令：

```
cscript.exe //nologo wmiexec.vbs /shell 192.168.1.1 username password
```

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-b023950f07f917c0a887cae936cd8fb9_2.jpg)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-b023950f07f917c0a887cae936cd8fb9_2.jpg)

这样就获得了一个半交互式的 shell，这个 shell 和 psexec 的 shell 没什么区别。之所以称为半交互式，是因为这个 shell 也不能执行实时交互的命令，和 psexec 是一样的。

上个执行命令的图：

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-fb501cb1c58062d6e254d5da2ab50a69_3.jpg)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-fb501cb1c58062d6e254d5da2ab50a69_3.jpg)

左边是虚拟机里面执行的命令，右边是 WMIEXEC 里面执行的。

还可以抓取 hash:

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-80ceca561d03e132cacbfc470a3c9467_4.jpg)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-80ceca561d03e132cacbfc470a3c9467_4.jpg)

**单个命令执行的模式**

这个模式适用于只需要执行一个命令，或者说当前的环境不是交互式 shell，没法运行 WMIEXEC 的 shell 模式时（比如在 webshell 里面）。

```
cscript.exe wmiexec.vbs /cmd 192.168.1.1 username password "command"
```

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-d3c3b3bbd4c16f748e0023ed64a37586_5.jpg)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-d3c3b3bbd4c16f748e0023ed64a37586_5.jpg)

上面是提供账号密码的情况，如果有时候我们抓取到的是 hash，破解不了时可以利用 WCE 的 hash 注入，然后再执行 WMIEXEC（不提供账号密码）就可以了。

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-ac139612cc7033bc6a8e742c35f8c726_6.jpg)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-ac139612cc7033bc6a8e742c35f8c726_6.jpg)

Tips：

如果抓取的 LM hash 是 AAD3 开头的，或者是 No Password 之类的，就用 32 个 0 代替 LM hash 即可。

**0x03 原理和相关问题**
----------------

整个过程是先调用 WMI 通过账号密码或者 NTLM 认证（WCE 注入）连接到远程计算机，然后如果提供了账号密码，则用这个账号密码建立一个到目标的 IPC 连接。随后 WMI 会建立一个共享文件夹，用于远程读取命令执行结果。

当用户输入命令时，WMI 创建进程执行该命令，然后把结果输出到文件，这个文件位于之前创建的共享文件夹中。最后，通过 FSO 组件访问远程共享文件夹中的结果文件，将结果输出。当结果读取完成时，调用 WMI 执行命令删除结果文件。最后当 WMIEXEC 退出时，删除文件共享。

由于 WMI 只负责创建进程，没有办法可以判断命令是否执行完毕，所以脚本采用的方法是延迟 1200ms 后读取结果文件，但是如果命令执行的时间大于 1200ms，比如 systeminfo 或者 ping 之类的，这时候读取结果文件会导致读取的结果不完整，然后在删除结果文件时会出错。

比如正常的执行 ping:

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-9d82e887846ee247161aa7d5baa2b085_7.jpg)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-9d82e887846ee247161aa7d5baa2b085_7.jpg)

Ping 结果没有读取完整，而且命令执行完后目标服务器上的 wmi.dll 结果文件并没有被删除！

为了防止出现这种情况，于是在 shell 模式里面加入了 - waitTIME 选项，TIME 是要等待的时间。当执行的命令后面跟上 - wait5000 时，表示这个命令等待 5s 后再读取结果.

![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-3e9c26c65e1c19f7fc3f5f0b0b01ce00_8.jpg)

由于正常的命令都要查看结果，所以执行的命令后面都会加上重定向符，把结果输出到文件中。

所以用这个执行木马会有问题，因为木马进程会一直存在，导致结果文件被占用，不能删除，也不能改写，如果执行不带任何参数的 nc.exe 也是这种效果

出现这种情况后由于结果文件被占用，所以 WMIEXEC 不能工作，除非手动更改脚本中的结果文件名。或者可以用 taskkill 远程结束掉卡死的进程，然后 WMIEXEC 可以恢复工作。

为了解决这个问题，加入了 - persist 选项。

当命令加了 persist 选项后，程序会在后台运行，不会有结果输出，而且会返回这个命令进程的 PID，方便结束进程。

这样就可以运行 nc 或者木马程序了。

下面是测试 nc 的结果：

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-a55b0ca878eb92459bbad46a86919c73_9.jpg)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-a55b0ca878eb92459bbad46a86919c73_9.jpg)

相关设定：

```
Const Path = "C:\"

Const FileName = "wmi.dll"

Const timeOut = 1200
```

这段代码在脚本的一开始，是控制结果文件路径、文件名、以及默认代码执行时间的，可以自行更改

**0x04 题外话：UAC 的探讨**
--------------------

测试中发现在 Server 2008 以及 2012 中, 只有 Administrator 账号能进行远程连接，并且 psexec 也是一样的情况，还有 IPC 连接也是。就算是管理员用户组的其他用户也不能进行远程连接。

后来发现是 UAC 的问题 (**参见安全脉搏《[过 Windows 7/8 UAC 技术浅析](http://www.secpulse.com/archives/1561.html)》)**，默认 UAC 是开启的，这时候只有 Administrator 账户能够远程访问共享或者连接 WMI。

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-eddd0e7318e8d95c82c05248d5420903_10.png)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-eddd0e7318e8d95c82c05248d5420903_10.png)

图中 hehe 是管理员用户组的用户，但是 PSEXEC 在连接时提示拒绝访问，WMIEXEC 也是一样。

Google 查到可以通过禁用 UAC 然后 psexec 就可以使用了，如何禁用参考：[http://support.microsoft.com/kb/942817](http://support.microsoft.com/kb/942817)

禁用之后 psexec 可以通过 hehe 账户连接，但是是普通的权限，此时要加上 - h 选项即可获得管理员的权限。

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-ea05a913cbb0f69d907c15064f6379e8_11.png)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-ea05a913cbb0f69d907c15064f6379e8_11.png)

禁用 UAC 后 WMIEXEC 用 hehe 账户连接直接就是管理员权限

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-30542e1c772d3435740e0f60f8cd9433_12.png)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-30542e1c772d3435740e0f60f8cd9433_12.png)

值得一提的是，UAC 并不会拦截域管理员，就算 UAC 是开启的，域管理员也可以直接连接，可以直接使用 PSEXEC 或者 WMIEXEC。

**0x05 WMIEXEC 使用实例**
---------------------

还是用抓取 server 2012 域控上的 hash 作为例子吧，具体操作步骤就不介绍了，直接上图：

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-9e91ac1f89dac745d134f50121a0c208_13.png)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-9e91ac1f89dac745d134f50121a0c208_13.png)

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-abb6bb15a0bad1092a37a2ef93a16998_14.png)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-abb6bb15a0bad1092a37a2ef93a16998_14.png)

[![](http://www.secpulse.com/wp-content/uploads/2015/05/cache-652fe71227d9a6e29e556fa5eedd5f7b_15.png)](http://www.secpulse.com/wp-content/uploads/2015/05/cache-652fe71227d9a6e29e556fa5eedd5f7b_15.png)

抓预控 hash 还有好用的工具可以在安全脉搏上发现 <[NTDS.dit 密码快速提取工具](http://www.secpulse.com/archives/6301.html) >。

**0x06 总结**
-----------

运行时间长的命令时，如 ping,systeminfo 之类的，记得加上 - wait5000 或者更久的时间选项

运行 nc 反弹或者木马等不需要输出结果、同时需要一直运行的程序时，一定要加上 - persist 选项，不然你就只能去 taskkill 远程结束进程了

应该还会有不少 bug, 大家用了有什么问题可以回帖或者直接 PM

WMIEXEC.vbs: ~wmiexec.rar (2.97 KB)~

12.15 更新：

现在单命令执行模式（/cmd）也可以解析 - waitTIME 和 -persist 选项了，这样就可以用单命令模式运行 nc 或者远控

下载地址： [wmiexec v1.1.rar](http://www.secpulse.com/wp-content/uploads/2015/05/cache-a360611dc24d240989799c29c555e4b7_wmiexec-v1_1.rar)  (wmiexec v1.1.vbs)