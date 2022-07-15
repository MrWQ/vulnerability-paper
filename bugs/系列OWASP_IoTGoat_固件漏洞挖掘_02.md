> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/vHPFYp5_Fjwg2Ewf7Z6KLA)

    继续接着上一章，本章节主要从弱、可猜测或硬编码的密码和不安全的网络服务入手。

**1. 弱、可猜测或硬编码的密码**  

查看固件中用户密码文件 / etc/shadow

```
root:$1$Jl7H1VOG$Wgw2F/C.nLNTC.4pwDa4H1:18145:0:99999:7:::
daemon:*:0:0:99999:7:::
ftp:*:0:0:99999:7:::
network:*:0:0:99999:7:::
nobody:*:0:0:99999:7:::
dnsmasq:x:0:0:99999:7:::
dnsmasq:x:0:0:99999:7:::
iotgoatuser:$1$79bz0K8z$Ii6Q/if83F1QodGmkb4Ah.:18145:0:99999:7:::
```

加密密码格式 **$id$salt$encrypted**

id 为 1 时，采用 md5 进行加密；

id 为 5 时，采用 SHA256 进行加密；

id 为 6 时，采用 SHA512 进行加密；

该固件使用的加密方式为 md5 加密；

**可以采用暴力破解方式获取默认凭证；**

查找网上暴力破解字典

```
$ git clone git://github.com/danielmiessler/SecLists.git
$ cd Malware
$ awk '{print $2}' mirai-botnet.txt > /home/iot/Desktop/password.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEyvJMIS5T4ZfvlJrQFRuYXic2Q7RYqmiaTnJkwHiac7vNAdwZL6LszlgeA/640?wx_fmt=png)

**2.  不安全的网络服务**

快速端口扫描 (速度较快，但不一定准确)

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEQsUrB3BzBw280wu4ibcANTbka2WJavXtYtmMzeS2OmeW6LictUFKyHvQ/640?wx_fmt=png)

22 端口 根据暴力破解得到的密码进行登录

53 端口 dnsmasq 安全漏洞

5000 端口 upnp 允许未经授权的设备修改网络配置

###  **① SSH 服务**

使用僵尸网络字典暴力破解

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEyvJMIS5T4ZfvlJrQFRuYXic2Q7RYqmiaTnJkwHiac7vNAdwZL6LszlgeA/640?wx_fmt=png)

获取用户密码 (iotgoatuser/7ujMko0vizxv)  

###  **② MiniUPnPd 服务**

扫描 upnp 详细信息

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWE4fFWsPOW5ibuAz7WWFDcBIeHwbY25qXicgt3LeVRlE7ZpIbia215h5uZg/640?wx_fmt=png)

https://zhuanlan.zhihu.com/p/51562785 攻击利用方式详细介绍

UPnP 由于设计上的缺陷而产生的漏洞，这些其中大多数漏洞是由于服务配置错误或实施不当造成的

**2.1  获得 SCPD(服务控制协议文档)**

查看开启了那些服务

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWESTCULoqVxVDFWmd9kxVibLd8aXdVKbXlA3e1FH8lexXtibu9vDVxJVEg/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEI8TDORWPxD1iaAmQiaJD4q8jUckkrgbOPk77Sxn9CvYibgCWzD1TEryiaQ/640?wx_fmt=png)

开启服务汇总

```
<serviceType>urn:schemas-upnp-org:service:Layer3Forwarding:1</serviceType>
<serviceId>urn:upnp-org:serviceId:L3Forwarding1</serviceId>
<SCPDURL>/L3F.xml</SCPDURL>
<controlURL>/ctl/L3F</controlURL>
<eventSubURL>/evt/L3F</eventSubURL>

<serviceType>urn:schemas-upnp-org:service:DeviceProtection:1</serviceType>
<serviceId>urn:upnp-org:serviceId:DeviceProtection1</serviceId>
<SCPDURL>/DP.xml</SCPDURL>
<controlURL>/ctl/DP</controlURL>
<eventSubURL>/evt/DP</eventSubURL>

<serviceType>urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1</serviceType>
<serviceId>urn:upnp-org:serviceId:WANCommonIFC1</serviceId>
<SCPDURL>/WANCfg.xml</SCPDURL>
<controlURL>/ctl/CmnIfCfg</controlURL>
<eventSubURL>/evt/CmnIfCfg</eventSubURL>

<serviceType>urn:schemas-upnp-org:service:WANIPConnection:2</serviceType>
<serviceId>urn:upnp-org:serviceId:WANIPConn1</serviceId>
<SCPDURL>/WANIPCn.xml</SCPDURL>
<controlURL>/ctl/IPConn</controlURL>
<eventSubURL>/evt/IPConn</eventSubURL>

<serviceType>urn:schemas-upnp-org:service:WANIPv6FirewallControl:1</serviceType>
<serviceId>urn:upnp-org:serviceId:WANIPv6Firewall1</serviceId>
<SCPDURL>/WANIP6FC.xml</SCPDURL>
<controlURL>/ctl/IP6FCtl</controlURL>
<eventSubURL>/evt/IP6FCtl</eventSubURL
```

    xml 还包含 ControlURL，这是与该特定服务进行通信的 SOAP 端点（实质上，该 URL 的 GET / POST 将触发操作）。

 **SOAP**

    控制消息使用 SOAP 协议，也以 xml 表示，看起来和 RPC 类似（但没有任何身份验证）, 即通告 SOAP 来实现服务操作。

#### **2.2 SOAP 控制**

    浏览器直接访问控制 URL，出现如下报错

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEJyXzuXA8lYZPsdG50HXcibedHkCUEkvRjZOcTJXdh60ZuFQiabDOLyMQ/640?wx_fmt=png)

    查看具体 action 和对应参数 (以 DP.xml)

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEgen9JuCeDjv5vvJguYPXKNvnDVL0jY7xrWPWBZ5c2PkJ9nFQHaNCtQ/640?wx_fmt=png)

    工具 miranda

 **路由器 80 端口的服务映射到外网端口 8080 上**

```
upnp> host send 0 WANConnectionDevice WANIPConnection AddPortMapping
```

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEHG3kAIQYuBXJPbaibyVicWfX8aFw3OYXlLAg0waPicGCFGufBEmVa0fAQ/640?wx_fmt=png)

 **获取端口映射目录**

```
upnp> host send 0 WANConnectionDevice WANIPConnection GetSpecificPortMappingEntry
```

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWElYDOTruuI6ic1qEGYVuMP3I7zib6EiatU0jOza5EvAsXRl6P9BXr5ExYA/640?wx_fmt=png)

    无需认证就可以完成上述操作

 **查看网页端口是否添加成功以及是否映射成功**

*   是否添加成功
    

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWEOogwCd1xcEA0daYDc8MibyOuqk6emPz2hrHd25JFT59KaOvAao0QFKg/640?wx_fmt=png)

*   是否映射成功
    

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQXCad3m4oKv1b79YMBYwWE9KW2MwzusKBwjyOUIMvVicnATKLVPKckmrx1Z9NXIvT0FdOwNBSt27Q/640?wx_fmt=png)

其余的控制 URL，大家可以自己去尝试，看会发生什么样的结果。

**总结**

1.  脆弱的 miniupnp 配置允许未经授权的设备修改网络配置，例如防火墙规则、端口映射。

2.  启动时侦听的传统网络服务。

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnTqMVczDE3GyGU1hPA7RQQlIESOibcZaWMeJVMicz1JUKnoSKhomypNO0J7q4BAxqjgxmpWYYe17ia2A/640?wx_fmt=png)

如果您有意向加入我们，请留言: )，

或邮件投递简历：akast@hillstonenet.com