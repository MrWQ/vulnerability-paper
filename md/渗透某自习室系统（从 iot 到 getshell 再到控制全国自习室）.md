> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/9dgUD7VpT8Zoj0lKYly4yQ)

![](https://mmbiz.qpic.cn/mmbiz_png/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fuBhZCW25hNtiawibXa6jdibJO1LiaaYSDECImNTbFbhRx4BTAibjAv1wDBA/640?wx_fmt=png)

扫码领资料

获黑客教程

免费 & 进群

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSFJNibV2baHRo8G34MZhFD1sjTz4LHLiaKG9208VTU6pdTIEpC9jlW6UVfhIb9rHorCvvMsdiaya4T6Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fchVnBLMw4kTQ7B9oUy0RGfiacu34QEZgDpfia0sVmWrHcDZCV1Na5wDQ/640?wx_fmt=png)

****作者：acoke****

****原文地址：https://forum.90sec.com/t/topic/1537****

前段时间找了个自习室学习，因为自习室网络不太好就无聊扫了一下网段，发现了一台 Ampak Technology 机器

  
以为是笔记本电脑（自习室一般都是用手机比较多），就扫了一下详细信息：

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNexpNVEjJ9mUxWqkoqoTdkjjfqLKhIswK26fzDKQobUthrVZPaJfibSQ/640?wx_fmt=png)

发现开了 5555，之前对这个端口没了解过，就百度了一下发现是 adb 服务，刚好看到一篇文章（https://www.cnblogs.com/guaishoujingling/p/11101649.html）

是打靶机，不过看到说是 2016 年的洞了，也没想能利用成功，就 msf 用了一下： 

search adb use exploit/android/adb/adb_server_exec

设置目标 ip：  
`set RHOSTS 192.168.2.34`

  
设置自己的 ip：  
`set LHOST 192.168.2.136`

  
我直接贴 run 的截图了：

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZN9Tk5fl9f0VRZuop1c73UfoMr9n3NCQbqart8BI64SeQGIqPddSpD1Q/640?wx_fmt=png)

这里利用成功后是不返回 shell 的，要利用 adb 连接，安装 adb：

  
brew cask install android-platform-tools  

安装成功后连接目标：

                                 
adb connect 192.168.2.34:5555

adb devices 查看一下连接状态是成功连接了：

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNNpmuIraXB3IfaDBHYjjv2mPLevXPibck8WBWkk2ST2wyDg2hiaiaDfoww/640?wx_fmt=png)

adb shell 直接远程命令执行发现不是 root 权限，su 成功拿到 root 权限：  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNmccL95v81krxgvcP2IefyLaxg13A3fNL14ZjKHCZkTtSDPJzias89Vg/640?wx_fmt=png)

  
截个图看看：  
adb shell screencap -p /sdcard/screen.png

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNIlAFO9iaVyzElnSQqdXYqzXWPsrHcz1233Kgen9EykC7doMQiaWlmmaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNgje1n9NouU9KGj9SeI4o1XT5P6eaJ0tm21PSEdH2CsjOibr57ib0caKQ/640?wx_fmt=png)

 通过 adb 漏洞实际已经可以利用 root 来操控门禁系统了（比如 kill 掉服务，清除锁屏密码等），但是这些操作会被自习室管理员知道，我想要通过远程在管理员不知道的情况下来操控门禁系统还是不行的...  

继续利用，通过收集平板上面的信息知道了用户 id 是 xxxxxx，还知道了平板是 xx 科技的，然后谷歌和扫描找到了 xx 科技的用户管理登录界面和 api 文档，

知道了要实现操控门禁系统需要用户 apiid 和 apikey 还要 acsurl，这些信息都是登录后要找的，通过爆破无果，找 xx 科技的客服要了测试账号和密码看了看后台也没有什么能利用的洞

  
只能返回到平板，既然是通过网络对接平板，平板上肯定有用户信息，

通过抓取网络数据包和查看安装 app 包发现 com.xxx.aidoor 是 xx 科技对接门禁的 app，

于是 find 了一下 com.xxx.aidoor，找到了 com.xxx.aidoor 的数据库，在数据库中并没有找到 api 对接所需要的信息，但是找到了一个 web 网址：

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNaP4lPwDAOH2KSrOnqTS36VwgnfsO6k4DX1E8n7CrqiahdC3OXLNrmow/640?wx_fmt=png)

通过这个地址继续收集信息知道自习室系统的的管理登录界面和用户登录界面，扫了一下端口和信息，发现是阿里云的服务器，宝塔面板  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNEFvwJafYicVcdqUWNiaNnLEZ5Wk5ndO6m1MiaBXexqvyWLlCicB78YKchQ/640?wx_fmt=png)

这里 21，22 的利用肯定是放到后面没办法了再回来搞，看了看 svn 也没什么可以搞的，几个页面也没什么信息，宝塔和 think6.0.2，搜了下相关漏洞也没什么能搞的，只能靠自己了

在自习室系统的登录界面（上面说的 xx 科技登录是 iot 设备的登录界面）发现了可以找客户要试用账号，于是加上客服微信要到了试用账号：

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZN4VrPOXAQ8BvCciajlxdG4Nw9vmHzQnRZgBESRrXB7H7hJdybQva1qGA/640?wx_fmt=png)

拿到后台试用账号后就看有没有什么能利用的漏洞，因为后台的所有上传都是用的腾讯云储存（其实有一处上传点的）

所以找别的能利用的漏洞，找到了 xss 和越权，但是比较鸡肋，利用困难，不是重点这里就不贴了，一直找啊找找啊找终于找到一处上传点不是传到腾讯云储存的，

因为后台和美团还有商户微信对接，所以要上传证书文件，可以直接改后缀上传，传了一个 phpinfo 看了一下  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNL5bZibFAsYicHgXeUP4ic12oEeIxUlEQtm3P2v5ib7vCI6nAEEaniaia4Jfw/640?wx_fmt=png)

宝塔禁用的函数实在是太多了，加上阿里云会报警，

**这里小技巧：**  

传个过宝塔函数的免杀马 + python 反弹 shell 可以避免阿里云报警成功无痕迹 getshell  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZN5RPZNo6GcCDibEaCcdyiaWLnwbpfPzdpO1msGcwicDkzJRqia9N6INHl7A/640?wx_fmt=png)

有了交互 shell 接下来的事情就好办多了，find 一下 config 找到了 mysql 信息：

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNwNkFHicAyHgSLFAko78TUCibRBFFmt0pK7JtQMVSTTQskwSiarDPLDsVg/640?wx_fmt=png)

这里发现用的是阿里云的 rds 数据库，站库分离，我本地连接不上，推测是做了白名单限制，有了交互式 shell 白名单限制形同虚设好嘛～wget 一份 phpmyadmin 过去，成功绕过：

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNvMTKLN9q2krD4hebI9KQ69QswiaUDPKulZ1Ogsa57A0TiaWt0xZ5ia1WA/640?wx_fmt=png)

不过数据都是进行加密的，连着查了几条都解不开，推测是自写加密。

这能难倒我？

渗透测试的本质就是信息收集好吧，通过对服务器文件进行信息收集发现在 xxx 文件夹下存放着用户登录的 log，通过 log 可以直接查看用户登录的明文密码：

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNHHurVQUeqsUtHC6qbia8GWCic4JlO0PJkzaVD54OqlXEpkr2FOia7h08Q/640?wx_fmt=png)

成功拿到总管理账号，这套自习室系统的用户还是不少的，全国 170 多家：  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNSceN7rGqGibOxiavlb2dDPK60lcf0KggoorQL8OUDYYrrVJMgVcqYOuA/640?wx_fmt=png)

这个自习室管理系统是和我一开始 adb 漏洞利用的那个门禁平板的公司合作的，因为后台对接了门禁系统，所以可以直接在后台通过对自习室管理看到门禁系统的账号密码，进而可以远程控制全国 170 多家自习室的 iot 设备  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZN6JWQib9lZLCRe9ia6AWVBL2YQXj4YMqzJeRTN79ocBtsJhuEx2IzYibsg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSG0iaesCWia3iaHuWdU8picAEZNIFHIfxYUVswg1X9N3VRKiabhiauSqjGZxicCpjCCiccylSicgBsqR530JPA/640?wx_fmt=png)

完   

学习更多黑客技能！体验靶场实战练习  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSFl47EYg6ls051qhdSjLlw0BxJG577ibQVuFIDnM6s3IfO3icwAh4aA9y93tNZ3yPick93sjUs9n7kjg/640?wx_fmt=png)

（黑客视频资料及工具）  

![](https://mmbiz.qpic.cn/mmbiz_gif/CBJYPapLzSEDYDXMUyXOORnntKZKuIu5iaaqlBxRrM5G7GsnS5fY4V7PwsMWuGTaMIlgXxyYzTDWTxIUwndF8vw/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSFTib5w98ocX6Sx1YcmgS0tfPOIyEmD8jse5YLoeZzDibM8rNrQibZPsibKXekZaR8FFV3flUT84nU0LQ/640?wx_fmt=png)

往期内容回顾

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSFTib5w98ocX6Sx1YcmgS0tfPOIyEmD8jse5YLoeZzDibM8rNrQibZPsibKXekZaR8FFV3flUT84nU0LQ/640?wx_fmt=png)

[渗透某赌博网站杀猪盘的经历！](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247493616&idx=1&sn=0299bced5d71aa60c9cea5b77a3b8fe7&chksm=ebeaaedddc9d27cb805b5e970f5554c47c32a69fdb9ee39acd1642a163e55b17f429e5db06a7&scene=21#wechat_redirect)  

[【教程】利用木马远程控制目标手机](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247502800&idx=1&sn=3c0c6ba8f469a6a08560fb8f61094ed7&chksm=ebea82fddc9d0bebb4a2a85308f44028aa484da945a35de801687532410f896b06ec3bdc1a24&scene=21#wechat_redirect)  

[黑客网站大全！都在这了！速看被删就没了](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247493025&idx=1&sn=97a10a4eca361ad2f66435f89bdcf2a3&chksm=ebeaac8cdc9d259ac26623014a38181b60ba57af9577f4e062e0ed9f33baef84ff60e645a6e6&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/CBJYPapLzSFTib5w98ocX6Sx1YcmgS0tfPyjxT8Q78w0uBADoIltpF1KribvWfHicVlFwShJRIxZls99XR1jaEYow/640?wx_fmt=gif)