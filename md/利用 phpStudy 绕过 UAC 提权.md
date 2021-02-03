> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Lc7SgrIkv32bnpIrWhJLgA)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

 |

**0x01 前言**

这篇文章主要记录的是笔者在一次实战测试中发现的一个小问题，就是可以直接利用目标主机已安装的 phpStudy 软件来绕过 Windows10 的 UAC 限制实现权限提升，事后也在本地机器和朋友 @sin 的机器上做了复现测试，都是可以成功利用的。

其他更多可用于绕过 UAC 的常用第三方软件和相关服务还有待挖掘，这应该也算是一种绕过思路吧！

**本地测试环境信息：**

```
操作系统：Windows 10教育版17134
软件版本：phpStudy2018
phpStudy安装路径：D:\phpStudy\
phpStudy进程名：phpStudy.exe、httpd.exe、nginx.exe、mysql.exe等
```

**0x02 绕过原理分析**

因为管理员运行 phpStudy.exe 时已经在 Windows UAC 弹窗中允许执行了，httpd.exe 自然也就继承了相应权限，就是说 php 环境是在已过 UAC 状态下运行的，所以也就不用再去绕过了，其实就与以管理员身份运行 cmd.exe 是一样的。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xoNobmrLI7ickPobZictfVzziasu4k8JwDGPhMDicMu56lNO1qWgwU3CbBZA/640?wx_fmt=png)

这里笔者用 Everything 软件来进一步验证，打开 Everything 时会先出现一个 UAC 弹窗，直接点击允许执行。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xo78rakKScCF1R86g8jJdI8ibza6xF0CG0qE1PTXibBibExVibwFs7uVu80w/640?wx_fmt=png)

然后搜索 cmd.exe 文件并直接打开，无需以管理员身份运行，然后执行添加管理员用户命令时发现不会再出现`“发生系统错误 5。拒绝访问。”`。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xo4B0tH0ryIUtZicsYibeRDmV9vfYfhNIrkqPUr3zW3ic8FEcVrXy00PzfA/640?wx_fmt=png)

**0x03 模拟实战测试**

(1) 通过钓鱼或者其他方式得到一些个人 PC 主机权限，但由于开启 Windows UAC，目前暂时没办法得到 SYSTEM 权限，更不用说抓取目标主机明文密码和添加管理员用户了。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xorYedvkulklqNEntQ3VICDWlm3z1rzAhAJqUxtSHUj6uoBicWic9YBYSA/640?wx_fmt=png)

(2) 信息搜集时在返回的进程列表中看到有`phpStudy.exe、httpd.exe`进程，而且都不是以当前`Shadow9`用户运行的，这就说明它们的运行权限可能要高于 Shadow9，如果是以当前登录用户运行的 phpStudy.exe、httpd.exe 进程时可能就不能利用了。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xoUxtODx2HicPjcOICpp4rF5uDWAdfmJvlVoBYcjY03mUxcXSdGIyniccg/640?wx_fmt=png)

(3) 如果 phpStudy.exe 是以 “非服务模式” 运行的 Apache 和 MySQL，那就不能用`sc qc`命令来查找路径，因为 UAC 权限问题也不能用`wmic`命令来查找进程路径，不过我们还可以用`dir`命令来列出 phpStudy 目录下 httpd.exe、nginx.exe、mysql.exe 等文件的所在路径。

```
wmic process where  get processid,name,executablepath
fsutil fsinfo drives
dir D:\httpd.exe /b/s
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xotHFAgy41AArF5fmoz8uB1cudzdNetNmics0ew30lqCLwjwwUP12SzfQ/640?wx_fmt=png)

(4) 找到 phpStudy 路径后我们接着写一个 php 一句话木马进去，注意尖括号处的转义，然后中国菜刀连接后即可在虚拟终端内添加管理员用户，全程再无 UAC 拦截弹窗。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xoGqRsLhRIborCNpMdaKUvo4so1GI4jQBQXjKz4k7dNlnz7hJp17ia77g/640?wx_fmt=png)

(5) 利用 MSF 中的 hta_server 模块成功得到目标会话，再使用 Incognito 扩展命令查看当前可用令牌中已有 SYSTEM，这时再用 getsystem 命令即可将当前会话权限提升至 SYSTEM。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xovklUGhdSvNXLiaszPw99g5pYh4ib3rcf4tnpic3eU1ts5iaTicC4bGDqBibA/640?wx_fmt=png)

只需在公众号回复 “9527” 即可领取一套 HTB 靶场学习文档和视频，“1120” 领取安全参考等安全杂志 PDF 电子版，“1208” 领取一份常用高效爆破字典，还在等什么？

* * *

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xong5AN4sVjsv6p71ice1qcHHQZJIZ09xK3lQgJquhqTLfoa9qcQ7cVYw/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486401&idx=1&sn=1104aa3e7f2974e647d924dfde83e6af&chksm=cfa6afd2f8d126c47d81afd02f112daea41bce45305636e3bba9a67fbdcf6dbd0e88ff786254&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfUDrsHTbibHAhlaWGRoY4yMzOsSHefUAVibW0icEMD8jum4JprzicX3QbT6icvA6vDcyicDlBI4BTKQauA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484585&idx=1&sn=28a90949e019f9059cf9b48f4d888b2d&chksm=cfa6a0baf8d129ac29061ecee4f459fa8a13d35e68e4d799d5667b1f87dcc76f5bf1604fe5c5&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfSyD5Wo2fTiaYRzt5iaWg1GJk2Cx54PBIoc0Ia3z1yIfeyfUV61mn3skB5bGP3QHicHudVjMEGhqH4A/640?wx_fmt=png)