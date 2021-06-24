> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/EgrGKEg53Dts4JH15duLuQ)

### 环境介绍

```
url:https://abc.com/login.doshiro框架Linux
```

### js 的危害

shiro 框架，没有跑出来。爆破用户名密码也无果。

```
尝试js读取。然后GET遍历。存在一个405页面https://jmc.com/fileDownload.do的文件405:请求的http方式不对。这里利用burp进行http方式修改成POST。返回200，说明存在。
```

POST 请求，需要参数的构造。一般思路

```
任意文件读取<br style="box-sizing: border-box;">命令执行漏洞<br style="box-sizing: border-box;">
```

这里看 fileDownload.do 为文件下载，尝试 fuzz 任意文件读取。

```
parms=/etc/passwd
```

利用参数字典去 fuzz-parms，最终 fuzz 成功。

```
data=/etc/passwd
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PZCtvaaOQSkAOZ0L5EkyP1zPz7601f8mVBtp9gw54YBq4P4LuNh6v4PRd4pBHyNC6NxrFMvXaZBE1GLT8VXMGA/640?wx_fmt=png)

### 任意文件之路  

开始之前，这里查阅了大量关于 “任意文件读取到 getshell” 对文章

### 重要的文件

### 历史命令

```
/root/.bash_history/home/username/.bash_history
```

```
从上述发现很多路径和密码。例如web日志路径例如:mysql -uroot -p 123456 直接在命令中输入密码真是坏习惯
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PZCtvaaOQSkAOZ0L5EkyP1zPz7601f8mdU2LFOk9QPfrr7DM52V8V2RK43URvb8a2ZNw5J22ITbzRU8zIgqRcg/640?wx_fmt=png)

### 私钥公钥  

```
/root/.ssh/id_rsa /root/.ssh/authorized_keys
```

```
一般都不会开放端口，无法利用。<br style="box-sizing: border-box;">
```

### 系统版本

```
/etc/redhat-release
```

### 非常重要的一个配置文件

```
var/lib/mlocate/mlocate.db
```

```
基于本地所有文件的信息的配置信息都知道。需要高权限用户才可以。<br style="box-sizing: border-box;">
```

### 其余的一些

```
/proc/sched_debug 配置文件可以看到当前运行的进程并可以获得对应进程的pid/proc/pid/cmdline   则可以看到对应pid进程的完整命令行。/proc/net/fib_trie   内网IP/proc/self/environ   环境变量/proc/self/loginuid   当前用户
```

### 过程

经过不停的测试。

```
读取到了目标:web日志最新的数据用户名密码shadowpasswdmlocate.db
```

### getshell

### 任意文件读取 getshell 一般方式

```
1.找源码<br style="box-sizing: border-box;">2.找数据库<br style="box-sizing: border-box;">
```

### getshell 过程

```
目标是shiro框架，这里尝试去利用shiro的反序列化漏洞去执行。利用公开的脚本没有跑出来key，那就要去读取目标的core.jar去主动寻找key值。
```

### 寻找 core.jar

```
因为任意文件读取为高权限，这里成功读取到目标的mlocate.db文件。
```

```
文件过大，可以下载下来。也可以利用burp返回包保存下来。<br style="box-sizing: border-box;">这里采用burp返回包保存下来，保存时，需要取消base64编码。<br style="box-sizing: border-box;">
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PZCtvaaOQSkAOZ0L5EkyP1zPz7601f8m18ibseQAXfxKjIMCprghHTXC6rSCgkNDsYE7G3X99kKPKibegcbBlNYw/640?wx_fmt=png)

```
ps:关于mlocate.db文件的打开，采用下载方式，利用sqlite3去打开，发现提示不是有效的数据文件，未解决。
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PZCtvaaOQSkAOZ0L5EkyP1zPz7601f8mkEGODzqFUQ8o72CNicgrHF0uEp1RhxiaEUK5ZMHhZeIMIu0PriaAPFoww/640?wx_fmt=png)

```
利用sublime打开搜索shiro
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PZCtvaaOQSkAOZ0L5EkyP1zPz7601f8mPTlG6P7eic4tcWovT8EK5vK8qdgE0L8AlVP2Y09liacCzcoaPpjQ5kcg/640?wx_fmt=png)

```
往上去寻找路径。得到shiro-core.jar的路径。下载下来。利用Luyten去寻找key 值。搜索Base64.decode
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PZCtvaaOQSkAOZ0L5EkyP1zPz7601f8m8x36icGNXdCXummN1oaP5jUpXw9l2uxuqnT21iajQv9icucB1qChg17dA/640?wx_fmt=png)

```
成功找到key。
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PZCtvaaOQSkAOZ0L5EkyP1zPz7601f8mn7ABYWG76lWDHjTjMuBuOH0gpcgWdwicLhicQCrxicYFGafwL9khRwbfA/640?wx_fmt=png)

```
利用网上shiro工具。拿到shell<br style="box-sizing: border-box;">
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PZCtvaaOQSkAOZ0L5EkyP1zPz7601f8m8xu8Geia3YhwadXKDHicWgrGoeDAgnY0zdqyolbnA6YhJ2MTg07VsBXg/640?wx_fmt=png)

就挺突然的。

#### 疑惑

```
通过key读取，发现key就是最简单的key。不知道目标如何防护的。无法找到key利用。但是直接用key，就成功执行命令。
```