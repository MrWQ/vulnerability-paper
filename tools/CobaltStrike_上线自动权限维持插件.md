> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/GTldV9PG26i9Vdv51FOfwg)

**点击蓝字**

![](https://mmbiz.qpic.cn/mmbiz_gif/4LicHRMXdTzCN26evrT4RsqTLtXuGbdV9oQBNHYEQk7MPDOkic6ARSZ7bt0ysicTvWBjg4MbSDfb28fn5PaiaqUSng/640?wx_fmt=gif)

**关注我们**

  

**_声明  
_**

本文作者：H0e4a0r1t

本文字数：900

阅读时长：10 分钟

附件 / 链接：点击查看原文下载

**本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载**

  

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，狼组安全团队以及文章作者不为此承担任何责任。

狼组安全团队有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经狼组安全团队允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

公众号

一、

**_动手_**

刚开始准备写的时候我就想到了 Server 酱的插件脚本，因为他那个功能就是一上线就会自动提醒，所以上网找了下脚本大概看了下代码

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjp0d36rsTHgM40Ikhvn0rbuklGKIEXAkEQ9kkTibDibUkJml6zJF6Wl70w/640?wx_fmt=png)

目前我只想要一上线就会有所动作的功能，大概看了下只有那个循环是我想要的，它会循环判断第一个 session，类似于下图中如果有新的 session 就会放在第一个上面

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjpgHQhQzEFccBh0vJaP4afhkvPnvKKCpnxbvY4HTTcS9bmDN8j6CL22A/640?wx_fmt=png)

当前的做权限维持的方法主要是靠远程下载 shell 然后添加计划任务

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjpxibeAmaSFzbe7ChDElzibnrQtw6m6fVwwsODUGwa8TCia5O3u3Wwaokew/640?wx_fmt=png)

中间我也做了权限判断，如果是普通权限，那么计划任务弹回的 shell 也是普通权限；如果是管理员权限，则计划任务会设置两种权限的 shell 弹回来，分别为 administrator 和 System 权限

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjpG9Wt48rCrFFCP1DVLc54MwGpUJ5TXYBzhmABx3RoRR0iaKRDzrTLIOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjpqHdvrFnSnQ7CcfcMVd39RL5v3QlpTAJYPbAhhicfY77qF4HuJoQ6MlA/640?wx_fmt=png)

Windows 2012  

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjpkcvL2eSWicvZWOb3oAo8Nia7HJ2fWh8PVeOO4O35C0w0HpanbyYKl0yw/640?wx_fmt=png)

Windows 2008  

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjpoFH0NKQorRwOPdI5ucnhQ0dIUMJVwRGHzpiaFYnuxPr4OHCmxribEwaA/640?wx_fmt=png)  

Windows 7  

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjpwCT8l0J0OlWHlKaOJojHgDicSkYwvIhJg4l5pES8fRg72bSAicdk1CxQ/640?wx_fmt=png)

Windows 10  

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjpdgdzqJgR2UfcCyWbFKl185NFlAJobHOFXR55RSFvpaIfYnRnKxyzcQ/640?wx_fmt=png)

写插件的过程中有考虑过，因为是循环，所以每次上线新 session 的话会不会陷入死循环，即无限重写计划任务、远程下载，导致动静过大或计划任务无法正常执行，但是之后经过实验发现：计划任务执行成功后会占用 exe，而因为我们并没有做交互所以也不会覆盖原有的计划任务。

使用方法及原理也很简单，首先要生成一个可执行文件通过 CS 的 Host File 挂在上面，通过 bitsadmin 远程下载后写入计划任务

需要修改的地方只有远程下载的地址，文件保存地址及计划任务的一些配置，我在 Server 酱的源代码保留的基础上写的插件，所以也可以配合 Server 酱做上线提醒  

运行方法和 Server 酱相同，可以直接通过 CS 客户端调用；不过想要随时监控的话最好还是在服务器上运行以下命令：

```
./agscript localhost 端口 用户名 密码 script/server_test/serverJ.cna

```

![](https://mmbiz.qpic.cn/mmbiz_png/FEAYq454okZbfNzbDKKdgHLSwyThJLjp6gtqJ2p135oic0QxBtxug4vdZhj08rDOrfOE6HVLKH3CCad1qKIogGw/640?wx_fmt=png)

感谢荣哥，彩蛋附上  

![](https://mmbiz.qpic.cn/mmbiz_jpg/FEAYq454okZbfNzbDKKdgHLSwyThJLjpqsEEN4WrcAQD9hg0WDFK9J6fV3SJGEHxhoMUFQ04FXcQG0hP3V99xQ/640?wx_fmt=jpeg)

  

**_后记_**

  

最后附上地址（点点 start~）  

https://github.com/wgpsec/Automatic-permission-maintenance

  

**_作者_**

  

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzDpicQ7hgKj2aFEtqw8Rebiab6BSSRiaQQuI4VpHL7SfmUuF9YX14nicL6JpPptrm0dEFa8uFfdyaaRJA/640?wx_fmt=jpeg)

H0e4a0r1t

一介凡夫俗子，勉强算个漏洞猎人

  

**_扫描关注公众号回复加群_**

**_和师傅们一起讨论研究~_**

  

**长**

**按**

**关**

**注**

**WgpSec 狼组安全团队**

微信号：wgpsec

Twitter：@wgpsec

![](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzBhAsD8IU7jiccdSHt39PeyFafMeibktnt9icyS2D2fQrTSS7wdMicbrVlkqfmic6z6cCTlZVRyDicLTrqg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/gdsKIbdQtWAicUIic1QVWzsMLB46NuRg1fbH0q4M7iam8o1oibXgDBNCpwDAmS3ibvRpRIVhHEJRmiaPS5KvACNB5WgQ/640?wx_fmt=gif)