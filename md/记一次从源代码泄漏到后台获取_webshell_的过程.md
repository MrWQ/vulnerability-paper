\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/uPrg3Q7N6DXCSToLDDH-sw)

**0x01 前言**
-----------

在一次授权测试中对某网站进行测试时，marry 大佬发现了一个网站的备份文件，里面有网站源代码和数据库备份等。根据网站信息和代码都可以发现该系统采用的是微擎 cms，利用数据库备份中的用户信息解密后可以登录系统，接下来要看是否可以获取 webshell。

**0x02 WEBSHELL 获取的尝试**
-----------------------

有了数据库备份文件，然后找一下是否有用户的信息，能否登录系统。

### 1\. 登录后台

解压备份文件可以从`data/backup`目录下找到数据库的备份，从中找到了用户表`ims_users`。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvsXaViccwZE5KoA8Jo7Gp5teZlRl8XzicoicZK74QicUntRjYRDleeU4uDw/640?wx_fmt=png)

知道了用户名、加密后的密码和 salt，我们去看一下密码加密的算法。

我这里直接搜索`password`，在 forget.ctrl.php 中找到了一处。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvyxY5dIucnfZBD6Pp9069sotIicgnr6M5Co0Nf0rv14WiaCN8ZXW0N9ew/640?wx_fmt=png)

密码加密方法是`$password = md5($password . $member_info['salt'] . $_W['config']['setting']['authkey']);`。是根据`原密码+salt+authkey`的形式进行拼接，然后进行 md5 加密。

authkey 在`data/config.php`文件中。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvrh5nI8PLpeeOTc8JjIMGIbLNib2q1kImrPsuZ7cVicABgibPP0ib6cJ3IA/640?wx_fmt=png)

现在 salt 和 authkey 以及加密后的密码已经获得，开始去解密密码是多少。这里我们将`salt`和`authkey`拼接为新的`salt`，然后使用`md5($pass.$salt)`的加密方式进行解密。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvVTibnZlfwPZLlytM7vjMcr9wGmjiadhvuf0riczYV7UlaCWiciaKUPOHicxQ/640?wx_fmt=png)

解密后即可登录后台。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDviapLwYaJJ4bXJOPQRzpq4TjEibhQRgW1vjgD8fISaVaAZhWWWBbINSSA/640?wx_fmt=png)

接下来就是 webshell 的获取了。

本以为都已经是管理员了，获取 shell 就是分分钟的事，然而事情远远没有那么简单。

### 2\. 失败的获取 shell 过程

根据搜索发现，该 cms 后台获取 shell 的方法也不少，主要还是围绕执行 sql 这里。但我这里都失败了，就简单的提一下。

**第一种方法：**

站点管理 - 附件设置 - 图片附件设置 - 支持文件后缀，任意添加一个类型，例如添加`pppppp`。

然后执行 sql 语句

| 

```
UPDATE ims\_core\_settings SET value = replace(value, 'pppppp', 'php ')
```

 |

更新缓存，之后就可以上传`"*.php "`文件了。但是有限制，适用于 apache 下，而且版本有限制。目标站不使用该方法的原因有二，一是该系统上传的位置是腾讯云 COS 上，二是 server 是 Tengine。

**第二种方法：**

第二种方法也是和 sql 执行有关，利用日志文件写 shell。

| 

```
show variables like '%general%';  #查看配置
set global general\_log = on;  #开启general log模式
set global general\_log\_file = '/var/www/html/1.php';   #设置日志目录为shell地址
select '<?php eval($\_POST\[cmd\]);?>'  #写入shell
```

 |

或者通过慢查询（slow\_query\_log）的方法写 shell。但目标系统也是失败，执行 sql 的时候报错。

还有一些其他的方法，这里测试也是失败的，就不再列举了。

**0x03 代码审计**
-------------

病急乱投医，熬成老中医。既然之前的方法不管用，只好去翻代码吧，找找是否有新的利用方式。翻出之前的一个文档，从里面找到之前的审计过程，看能否对现在有用。结果打开发现只有一个数据包和还有一句未实现的结论。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvHicMibXWhaQACElatkzV9Y79jYAb8U779uaaONhWmp2ZdK9tBopSbCCg/640?wx_fmt=png)

没办法，只好重新围着这个点继续审计，看是否能有所进展。

### 1\. 分析

打开文件`web/source/cloud/dock.ctrl.php`，找到执行的`download`方法。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvNiafa5rme42tbxEGxkZW7ocUge16pjHR1cfNicdWKWFMicaa8B2WyrzCg/640?wx_fmt=png)

代码比较简单，我大概说一下这里的流程：

如果请求包非 Base64 加密的格式，那么`$data`就是请求包的内容。然后对`$data`进行发序列化返回`$ret`，接下来获取`$ret['file']`并 Base64 解密返回`$file`。当存在`gzcompress`和`gzuncompress`这两个函数时，就会利用`gzuncompress`函数对`$file`进行解压操作。

将获取的`$file`进行 md5 加密后，与`$ret['path']`以及获取的`$_W['setting']['site']['token']`进行拼接为`$string`。当满足`$_W['setting']['site']['token']`非空并且`$string`md5 加密后的结果与`$ret['sign']`一致时，才可以进行下面的操作。下面就是文件的写入了，根据`$ret['path']`进行判断，然后写入的位置不一样。

这里关键的一点就是`$_W['setting']['site']['token']`这个值的获取。这个是利用 authcode 函数对`cache_load(cache_system_key('cloud_transtoken'))`进行解密获取的。

`authcode`函数位于`framework/function/global.func.php`文件中。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvOL6oOHTbyVe3qWT78vgPSDoRY7vLFoBDgFxrqHhDkHnGgI4sK90Z3A/640?wx_fmt=png)

由上面代码可以看出，要想使用`authcode`加解密，需要知道`$GLOBALS['_W']['config']['setting']['authkey']`，在上面提到过，authkey 在`data/config.php`文件中。

那么如果想任意写文件，就需要知道`cache_system_key('cloud_transtoken')`的内容了。

### 2.cloud\_transtoken 的获取

通过搜索发现，这个值是在文件`framework/model/cloud.mod.php`中的`cloud_build_transtoken`函数中被写入的，通过进入`cache_write`方法，发现会写入数据库中。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvNic28sudtocxV8KMtQxkZlufeOGicibdcz09KESyOTHXBCNzmBicVYFEicg/640?wx_fmt=png)

既然会写入到数据库中，而且目标系统下载到时候有数据库的备份文件，我们直接在数据库备份文件中搜索`cloud_transtoken`。结果并没有找到，可能原因是没有写入`cloud_transtoken`的时候就进行了数据库备份。

我们往上回溯，看哪里调用了`cloud_build_transtoken`。

发现了其中的一条利用链：

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDv4D6bGDoia262Y2UUmoceMMKYYHko1XA61JXh3pia8VfX1gzE5s2icANWA/640?wx_fmt=png)

当访问 http://ip:port/web/index.php?c=cloud&a=profile 时，就会判断站点 ID 和通信密钥是否为空（即站点是否注册），如果站点注册了，就会调用`cloud_site_info()`函数获取站点信息。函数`cloud_site_info()`调用了`cloud_api('site/info')`，这里的 method 为`site/info`，所以继续调用`cloud_build_transtoken`从会而将`cloud_transtoken`的内容写入数据库。然后通过数据库备份的功能，就可以看到数据库中保存的`cloud_transtoken`，进而可以利用之前的分析写 shell。

### 3\. 自定义数据库备份

由于数据库备份需要关闭站点，为了不影响目标站点的使用，这里我们搭建一个环境演示一下过程（需要注册站点）。

登录成功后更新缓存，然后访问 http://ip:port/web/index.php?c=cloud&a=profile ，关闭站点后进行数据库备份。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvibcsdia81GfTXVl4jahMickDiaeOPqbl0trFTiasbLEVgruTibSm2PkDJmRA/640?wx_fmt=png)

发现可以获取`cloud_transtoken`，但是数据库目录和文件的名字是随机的。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvDRRIib0DLQWPerDXRnMLGYD9BgwmpibyYFdicM8EIlatibzNl1WaibBwZIw/640?wx_fmt=png)

而且如果备份文件里面的数据库文件不是最新的，那么即使获取到`cloud_transtoken`也无法利用，我们需要最新的备份文件。

然后我们看一下数据库备份是怎么实现的，打开`web/source/system/database.ctrl.php`。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDv0SgCNCH27kKqUkeLziaMIjccjZ7kmp5DunXtuy4TXcC6qO93N64yVuQ/640?wx_fmt=png)

发现文件夹和分卷名可以自定义，如果为空或不满足条件的话，文件夹是时间戳、下划线和 8 位随机字符串的拼接，分卷名是`volume-10位随机字符串-1.sql`的形式，既然可以自定义，那么就简单多了。

访问链接 http://ip:port/web/index.php?c=system&a=database&do=backup&status=1&start=2&folder\_suffix=123&volume\_suffix=456 进行数据库备份，则数据库备份文件的地址为：http://ip:port/data/backup/123/volume-456-1.sql

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvicF3zsdfhfS5tmbI1SNEfic3FzQMnkl0DrNZY1R5QqR6MexVmHpIQ6Hw/640?wx_fmt=png)

然后就可以随时获取`cloud_transtoken`了。接下来就可以进行 shell 的获取了。

### 4\. 获取 WEBSHELL

根据上面的分析，`cloud_transtoken`、`authkey`已经知道了，接下来就是构造 payload 了。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvx5bbXia97tEBlShJjpzsJ2iaShQB4IYohtCvWrpH14kDMiaJJdHyqibRJQ/640?wx_fmt=png)

然后请求 http://ip:port/web/index.php?c=cloud&a=dock&do=download ，data 为生成的 payload。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvgsIW6LdS1HBnXd1t71SXPL9OwrcBUbLTqafCbUjaeVYl1xVIDibggAA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvajDRoJ7lH9fYnVBXghnaFGIxTarVmvwQ3ABwqSqWrd2gf8qyFuI9wQ/640?wx_fmt=png)

可以进行任意文件的写入，对目标系统进行测试，也成功获取了 shell。

### 5\. 延伸

上面是因为有系统文件备份，然后获取`/data/config.php`中的`authkey`。如果没有文件备份，登录了一个管理员权限的用户，能否获取 shell 呢。答案也是可以的。

该系统有一个木马查杀功能，可以根据这个功能读取文件内容。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvAEXsne0K7ScyMcFAqX6UEQuJ8mZjMyKMKPDBq4vzTEJ0l3Ndylia9kg/640?wx_fmt=png)

选择一个目录，然后提交并拦截数据库包，修改查杀目录为`data/.`，特征函数为`password`。然后就可以看到查杀结果，获取`authkey`的值。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvTfg2N7BibLulmr1asqpZ191Tea6EcVBjcUHKq5mkibtZVC33xR32Bz2A/640?wx_fmt=png)

在对最新版 v2.5.7（202002140001）进行木马查杀的时候，可以从查杀报告中看到该文件，但是查看时提示文件不存在。原因是最新版利用正则对文件路径进行匹配，如果匹配成功就提示文件不存在（windows 下可以利用大写路径绕过）。

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavwo8BGPNYVo7nI4M5icjjsDvW6Md0nJCEEokcxialbc0EG0TibpPxpKzMicxow0iaMf7ibibdibBOhnsxfhRQ/640?wx_fmt=png)

**0x04 总结**
-----------

根据上面对分析过程，该漏洞的利用过程如下：

1\. 成功登录后台，且拥有管理员权限。

2\. 更新缓存（非必须），访问链接 http://ip:port/web/index.php?c=cloud&a=profile 写入`cloud_transtoken`到数据库中。

3\. 关闭站点并进行使用自定义的目录进行数据库备份，链接地址：http://ip:port/web/index.php?c=system&a=database&do=backup&status=1&start=2&folder\_suffix=123&volume\_suffix=456 。然后下载数据库备份，地址为：http://ip:port/data/backup/123/volume-456-1.sql （多个分卷的话文件名为 volume-456-2.sql、volume-456-3.sql… ）, 然后找到`cloud_transtoken`。

4\. 生成 payload，请求 http://ip:port/web/index.php?c=cloud&a=dock&do=download ，写入 shell。

总的来说，利用上述方法获取 shell 需要满足两个条件，第一是拥有一个管理员权限的用户，第二就是该站点注册了云服务。

作者： 浮萍，文章来源：浮萍's Blog

****扫描关注乌云安全****

![](https://mmbiz.qpic.cn/mmbiz_jpg/bMyibjv83iavz34wLFhdnrWgsQZPkEyKged4nfofK5RI5s6ibiaho43F432YZT9cU9e79aOCgoNStjmiaL7p29S5wdg/640?wx_fmt=jpeg)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**