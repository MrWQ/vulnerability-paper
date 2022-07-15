> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/k1AHbCYzdEg29qoyfbNaNQ)

1. 简介

TZ 是一个由 golang 开发跨全平台，集主机发现，漏洞扫描，漏洞利用为一体的内网渗透工具。

配合 cs 插件生态，目标是为了做到内网渗透 all in one，以及常见漏洞检测利用的 all in。

1.1 cobaltstrike 插件加载

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXfuM0XJ3KfqgTAox4N6Hf4EP1AAHjyjcltOT0xDxbEo6VRAVkyEDOAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXDS548QtMic4XKkjOpiaviapu40FeHCvDC4F00dAgZg33pfiaQcRQu7Gia4A/640?wx_fmt=png)

在被控主机上使用 TZ 之前，请先初始化 TZ, 会将 TZ 文件上传到客户端 c:\windows\temp\ 下，方便后期使用

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXxHD1UAndwtarEZVp3c6LWA4zrXxy2ajDQibs6GBNVZs3SVrVGMtwibVw/640?wx_fmt=png)

1.2. 公共参数介绍：

```
-c string
               c
  -ip string
               ip list
  -p string
               PlusName
  -port string
               port
  -t int
               thread (default 8)
```

-ip 目标 ip，Examples：192.168.3.1 或者 192.168.3.1/24

-p 调用插件名称

-t 线程数，默认为 8

-port 目标端口，部分插件无此参数

1.3 目录结构

```
|____res              资源文件夹
| |____server         frp linux客户端
| |____server.exe     frp window客户端
|____main.exe         TZ window客户端
|____main.cna         cs插件文件
|____main             TZ linux客户端
```

1.4 开发计划

```
1.weblogic扫描
2.提权辅助插件
3.shiro利用
4.fastjson检测，利用
5. ....
```

**3. Scan plus**  

3.1 FuzzPortScan

FuzzPortScan 1-65535 全端口扫描

Examples:main.exe -p FuzzPortScan -ip 127.0.0.1

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXkv4fu2iaBfLFsfVMoVnofR2wkRaQXW7tISb9BVQlJiaasAicF2aTjIWnQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXx9IkYSibFHia6qpSW8YXibxZfvWGnk8XfGic0YjMtTDEd54Tia1MliaHMgQA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXahUMOVG52qF66ia7OT9KEU9uThJCJxJB9SicB7sujweUPS3RcwXKzkgw/640?wx_fmt=png)

3.2 ImcpScan

ImcpScan imcp 探测主机存活，使用 ping 命令探测主机是否存活

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXOeWYOhTBaCsIFicicrJicXcWgLjz678ApFc3KeibXbtaFVEKYKYH2EOFhg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKX5VaLe7OjgpNfq100efHMoqwRZBWoXZBCwPaiccjic4yeJ4Vdb1hKd3hQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKX3aVUYicKbCHqjb03lkNrkibC3Ziah3yGFWzic3QTFbiaysxaB2AP4VghHtA/640?wx_fmt=png)

3.3 Ms17010Scan

MS17_010 永恒之蓝漏洞扫描

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKX3KrDcQjOIZSPhrP5Yia0ucbqicxK4R7W4QltIbUARZzLeNHtfo9x6iakA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXuEBic72uzLebRCowvwvWAwfic3akP5pJpy0T1hd5EGO2XnEwkDuahxew/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXRrInDicn4lxFJfjAuUKibUZFLXzsEIHMVAiaCib9u0rTO22WWGj1a4JsRQ/640?wx_fmt=png)

3.4 NetbiosScan

Netbios 扫描，可用于探测存活主机，获取存活主机名，隐蔽性强。

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXic5HOicFuSicX92hT7wNRYShu1CDGCBVgd5XOv7VXAI7Lvkhjx2aFyAmA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKX6o0bPrwkpF8O5ibxrhiaPGL0t0OxicV9ICdAGI8ibamF3DqJ0uPb48mUvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXSTcHV5WxxRIiciaZvYAtbxKT4qNxiafxWTKFzGRTuOFGHzvUykFoupInQ/640?wx_fmt=png)

3.5 PortScan

常见端口扫描，默认扫描一下端口

```
{"22", "80,", "81", "135", "139", "443", "445", "1433", "3306", "3389", "6379", "7001", "8009 ", "8080","9200", "17001"}
```

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXd1J5DgJics0GsBmotyDqtV33NcNgWXOkd59k6YEb4hloC6pickNoG65w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXiaiaplKLFOmpgXrZh3UibmXHatNusWXfnEtIib9hzDHrXKqp2gRAiaK6Oicg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXRrnqdRAdHMFmCb9llib3dK3JJvCenJUAqdgxaKia4icIicfbZ63fa9y8BQ/640?wx_fmt=png)

3.6 SmbGhostScan

远程扫描 SmbGhost 漏洞，漏洞编号 CVE-2020-0796, 考虑到实际效果，暂未集成到 CS 菜单，可通过命令行使用

```
shell c://windows//temp//main.exe -ip 192.168.189.1/24 -p SmbGhostScan -t 16
```

3.7 WebInfoScan

扫描

```
"80", "81", "443","888", "7001", "8080", "8888","17001", "18080","8081"
```

端口中开放的 WEB 服务并获取 Title  

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXP4XJgWhxibViaTJZHpZz1rT0vgywDAdAJOp6kagUfaJNTwh33HwyTfRQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXx79g8jP77AavvIxxKicON87s4M5y3q97KBnstsdoO3Q9dWVXpZd4axw/640?wx_fmt=png)

4.Exploit plus

4.1 FTP_crack

ftp 弱口令破解

使用账号密码

```
Examples:main.exe -p FTP_crack -ip 192.168.189.1/24 -p 21 -c ftp:ftp
```

使用字典破解, 字典文件需自行上传到被控主机上

```
Examples:main.exe -p FTP_crack -ip 192.168.189.1/24 -port 21 -c username.txt:password.txt
```

或者

```
Examples:main.exe -p FTP_crack -ip 192.168.189.1/24 -port 21 -c root:password.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXzG1HQ1tF2s1TFKe1CYyLMKE5kYZxV8ibajLx5SKWqIIT3QPRY1PDVqQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXjsHdm6wAhkqBnhvMkoG6wEZrhnGUeF4HzsN1s8S8P2QEIcM3bmTRCw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKX9H5icajkTmnV1EcbBgAkOlsVescHiclTkHTVC8GAEFMvxNkYpsykAnIA/640?wx_fmt=png)

4.2 MONGODB_crack

mongodb 弱口令破解

4.3 SMB_crack

smb 弱口令破解

4.4 SSH_crack

ssh 弱口令破解

使用账号密码

```
Examples:main.exe -p SSH_crack -ip 192.168.189.1/24 -port 22 -c root:root
```

使用字典破解, 字典文件需自行上传到被控主机上

```
Examples:main.exe -p SSH_crack -ip 192.168.189.1/24 -port 22 -c username.txt:password.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXlhAbaPjloGcCL8SnMsTPrJqQ0XF674uTyDqjKfpD9PglzZMsoW9ribQ/640?wx_fmt=png)

4.5 Frp

在服务器上设置 frp 服务端如下，token 可自定义，server port 可自定义。然后启动 frp 服务器端，后续会在 1w-2w 这个范围内随机生成一个端口号来建立 socket5 服务器，注意在服务端设置好安全组放行。

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXyRoptGu6Xiax3rMbpcA5Boy7zH1dia73JOMktzFTxJAzFppaqZOGcnsA/640?wx_fmt=png)

点击 frp，点击以后会卡住是正常现象，因为此时在上传 frp 客户端

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXgMucK4wZoupzP3MQXPQLnPeLBuZEjoNCTicLanN3RlLtQH6mQ2chHcw/640?wx_fmt=png)

填写 frp 服务端 ip，以及端口

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXgicfqQ0qww20sic2TB7Ey1ddKB40jj2fHPKX3vIjlpuqkiaZXlh0I6QUQ/640?wx_fmt=png)

会使用 frp 启动 socks5 代理，将内网代理出来。

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXgWFkfmoB4V2Sl1Emzd0QzkcTG52ofKDjlkrOZnAA1Tlic0c54FibiaxJw/640?wx_fmt=png)

通过 TZ 启动的 frp 客户端，连接参数使用 AES 强加密并使用随机密钥，避免服务器连接信息泄露

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXtP1YiaxVibFfDtbVkAic3nQqIMultwDRKScB3hdZCog9jjOialacFPfE0A/640?wx_fmt=png)

5. 获取 TZ

仅仅面向知识星球用户开放下载，后续会持续在知识星球更新。

现在公众号粉丝福利加入知识星球前一百名，半价优惠

![](https://mmbiz.qpic.cn/mmbiz_png/noZJ3Kqbu1fRaARYdsuzbXIQLaWmBVKXeQhdS42PCbyHO5eiaYkN2SohjKdNB1WCibaCyUWuT1PYibPEa5yboQ04g/640?wx_fmt=png)