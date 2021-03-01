> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/C6SXz61DsKeNiIwgevSp7w)

菜鸟入坑代码审计，听说 BlueCMS 比较合适初学者，特此学习，大佬勿喷

漏洞环境 & 搭建
=========

本地环境搭建，使用 phpstudy 集成系统，CMS 版本为`BlueCMS_v1.6`

访问`install`目录

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyT2X1wS8dSPHEzsqnzGQ70xNpS5XCyPeCp4ibM5iajic9uf30L6PmYtW3w/640?wx_fmt=png)

下一步，查看数据库文件有没有生成

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWy8xo4sWu7DC1zYHKuQ2pHugqFO8PaHDdLOGbxEqPGOUmaR02FBj7QZA/640?wx_fmt=png)

数据库有数据表显示，安装成功！

漏洞分析
====

丢进 seay 里面（新建项目 -> 选择 bluecms 安装目录 -> 自动审计 -> 开始）

1. 数字型 SQL 注入
-------------

产生此漏洞的文件为`ad_js.php`

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyUjcUicKnYpxUmaOiaSA6DxOgHyPkEhcVnicOpnvZv1zk1xUuh6m8a1Flw/640?wx_fmt=png)

seay 显示 19 行的`$ad_id`变量存在 sql 注入，而变量`$ad_id是`从`$_GET['ad_id']`中来的, 且只经过了`trim`。

> `trim()`：函数移除字符串两侧的空白字符或其他预定义字符。

而在 ad_js.php 文件的开头（第 10 行）引入了过滤文件`require_once dirname(__FILE__) . '/include/common.inc.php';`

查看`common.inc.php`文件, 发现对`$_POST`,`$_GET`,`$_COOKIE`,`$_REQUEST`传递的参数都进行了过滤

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyDbJGtGpbwJstIxjPNIJNiaMicdY53TwsiaTa2kNicD6xlBDe5SgFcqQ7MA/640?wx_fmt=png)

跟踪看看`deep_addslashes`是怎么实现的

```
function deep_addslashes($str)
{
if(is_array($str))
{
foreach($str as $key=>$val)
{
$str[$key] = deep_addslashes($val);
}
}
else
{
$str = addslashes($str);//
}
return $str;
}
```

使用`addslashes`过滤

```
$ad = $db->getone("SELECT * FROM ".table('ad')." WHERE ad_id =".$ad_id);
```

可以看出上面的是个数字型注入，`getone`函数我们也追踪一下, 代码在`mysql.class.php`中

```
function getone($sql, $type=MYSQL_ASSOC){
   $query = $this->query($sql,$this->linkid);
   $row = mysql_fetch_array($query, $type);
   return $row;
}
```

是一个执行 sql 语句的函数，这里就确认存在数字型 sql 注入漏洞

漏洞复现：因为我们这里是白盒测试，所以直接提取一下管理的用户名和密码

`http://www.bluecms16.com/ad_js.php?ad_id=1 UNION SELECT 1,2,3,4,5,6,GROUP_CONCAT(admin_name,0x3a,pwd) FROM blue_admin`

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWy7oNWMv6ymXgenMZZxNIhRAUuhiakozdNibib8uWkyrialZYOIoqWHZkMXg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyj6WdUeqclnAxByQAQqvqHGKhp5SrQctLXRZWSETend9tlWI5XaFe8w/640?wx_fmt=png)

> 38 行输出的时候注释掉了，因此我们需要查看源代码

还要注意一下`0x3a`->`:`, 因为上面使用了`addslashes`函数，该函数会将`单引号（'）`,`双引号（"）`, `反斜杠（\）`，`NULL`进行转义，而使用编码就很好的绕过了！

2. INSERT 型 SQL 注入
------------------

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyqjs7Uh2BZZibKOGlntWw2A3WW1M82793qkc18z7XbbrrBYqqcD8rulg/640?wx_fmt=png)

```
// include/common.fun.php 文件108行
function getip()
{
if (getenv('HTTP_CLIENT_IP'))
{
$ip = getenv('HTTP_CLIENT_IP');
}
elseif (getenv('HTTP_X_FORWARDED_FOR'))
{
$ip = getenv('HTTP_X_FORWARDED_FOR');
}
elseif (getenv('HTTP_X_FORWARDED'))
{
$ip = getenv('HTTP_X_FORWARDED');
}
elseif (getenv('HTTP_FORWARDED_FOR'))
{
$ip = getenv('HTTP_FORWARDED_FOR');
}
elseif (getenv('HTTP_FORWARDED'))
{
$ip = getenv('HTTP_FORWARDED');
}
else
{
$ip = $_SERVER['REMOTE_ADDR'];
}
return $ip;
}
```

由于第一分析中`common.inc.php`文件只对`$_POST`,`$_GET`,`$_COOKIE`,`$_REQUEST`进行了处理，但是遗漏了`$_SERVER`, 而`getip()`函数中恰好是通过该变量获取 ip 地址。我们可以通过`client-ip`或`x-forwarded-for`进行 ip 的伪造, 触发漏洞。

phpstorm 使用`ctrl+shift+F`搜索一下，看哪里调用了`getip()`, 如下图，我们跟进`comment.php`文件 114 行

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyW3sQrDucHict6gjC6Amt9a8DFXT5D4f1sjS1Fg9YVhBFKfF3aqcOjQA/640?wx_fmt=png)

```
$sql = "INSERT INTO ".table('comment')." (com_id, post_id, user_id, type, mood, content, pub_date, ip, is_check) VALUES ('', '$id', '$user_id', '$type', '$mood', '$content', '$timestamp', '".getip()."', '$is_check')";
$db->query($sql);
```

这里我们也分析一下其他变量插入会不会产生漏洞

```
$id = !empty($_REQUEST['id']) ? intval($_REQUEST['id']) : '';
// intval函数进行了转义
```

```
$user_id = $_SESSION['user_id'] ? $_SESSION['user_id'] : 0; //session  略
```

```
$mood = intval($_POST['mood']);
// intval函数进行了转义
```

```
$content = !empty($_POST['comment']) ? htmlspecialchars($_POST['comment']) : '';
// 对comment内容做了html转义，所以不存在xss
```

看来我们还是只能利用`getip()`来触发漏洞

漏洞复现：

这里是对评论区进行的 sql 注入，因此我们需要新建一篇文章，然后在评论区测试（白盒测试，为了方便理解，我将 sql 语句输出了）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyKO6akNaNFIHXocZtI9fLHFgy8gzIRTVBaI9SLYH9glicUiaRBQgZlxZw/640?wx_fmt=png)

poc 构造思路如下:

> 插入两条数据的思路, 进行构造（注入返回结果要显示在留言内容处）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyLIHbIfwSHUf8enfKx89IsYWUAdDnwMVL2uCpAnxwtNRwUueoeRVPrQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWybvukLtP0S5WqgTPbIU8814h7GbzB8eYAmaqoibYJIgLUWp60avsmjMQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyJI8vKyXROnDdgp4emCSOwQ0safycG4VY9E5JZBenZH9F00gkUicwSFg/640?wx_fmt=png)

3. 另一处 INSERT 型注入
-----------------

在文件`guest_book.php`77 行处

```
$sql = "INSERT INTO " . table('guest_book') . " (id, rid, user_id, add_time, ip, content) VALUES ('', '$rid', '$user_id', '$timestamp', '$online_ip', '$content')";
$db->query($sql);
```

这里有个`$online_ip`, 我们跟踪一下

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyDGF0yxWTFzgibxkH5Afe3IWic7icEfn8rfh0EGNqeI7gq7licmlZqDnR4g/640?wx_fmt=png)

```
// include/common.fun.php文件106行处
function getip()
{
  if (getenv('HTTP_CLIENT_IP'))
  {
     $ip = getenv('HTTP_CLIENT_IP');
  }
  elseif (getenv('HTTP_X_FORWARDED_FOR'))
  { 
     $ip = getenv('HTTP_X_FORWARDED_FOR');
  }
  elseif (getenv('HTTP_X_FORWARDED'))
  {
     $ip = getenv('HTTP_X_FORWARDED');
  }
  elseif (getenv('HTTP_FORWARDED_FOR'))
  {
     $ip = getenv('HTTP_FORWARDED_FOR');
  }
  elseif (getenv('HTTP_FORWARDED'))
  {
     $ip = getenv('HTTP_FORWARDED');
  }
  else
  {
     $ip = $_SERVER['REMOTE_ADDR'];
  }
  return $ip;
}
```

原理跟上面的 sql 注入一样，我们需要构造 http 头，加个`X-FORWARDED-FOR`

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyvWiarjQ4wRCkMYiancecdxeCYCLNJo5b6aoicSloZZxqoxouibY7rSSLbw/640?wx_fmt=png)

4. 本地文件包含
---------

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWycHIC2H1w3E2NMcuSbDTb4HA0wdYIrJL4icua4eNCOxwbWmEpq6m7Lnw/640?wx_fmt=png)

漏洞发生在`user.php`文件 750 行处

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyNz4RsVUPFQjDNFlFpxnGH704XEafIlVEdm0mQHKwFgicibl1nFIFB1oQ/640?wx_fmt=png)

`$_POST['pay']`并没有做多余的安全检测，而是直接进行拼接，但是后面有`index.php`文件，所以我们的重点是如何截断。如果 php 版本低于`5.3.4`且`magic_quotes_gpc=off`则可以使用`%00`截断。还可以使用系统文件路径长度限制来进行截断。

这里我们使用系统文件路径长度的限制来截断：

```
Windows 259个字节
Linux 4096个字节
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyRnJjVnQemFOdpw9ibjVgtfWabBn3gia0ufohQfvZiccQ0Qd48oJGo9Tvg/640?wx_fmt=png)

当然了，由于文件包含漏洞可以包含图片文件（例如 jpg），而且服务器会解析图片文件（当作 php 文件执行），那么我们就可以上传一个带木马的 jpg 文件，然后利用文件包含漏洞包含此 jpg 文件。执行恶意代码。

具体利用步骤如下:

在个人资料编辑, 上传头像处传 jpg 文件 -> 使用包含漏洞包含此文件

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyv8ibUsDhDfA63aSHiaGG4ibUvMjdJskcylULtMq8LE7llXvUdl56nulrA/640?wx_fmt=png)

5. 任意文件删除
---------

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyg8usWA1w9Q6pu3vUnR68ko6m7J4cDmZDoMUq7S7OGdbrLurfNvacbg/640?wx_fmt=png)

漏洞发生在`publish.php`文件 309 行处

```
elseif($act == 'del_pic')
{
$id = $_REQUEST['id'];
$db->query("DELETE FROM ".table('post_pic')." WHERE pic_path='$id'");
if(file_exists(BLUE_ROOT.$id))
{
@unlink(BLUE_ROOT.$id);
}
}
```

第 7 行`unlink`删除文件，传入`$id`，先删除数据库里的，然后判断本地有没有此文件，如果有，`unlink`函数也对其进行删除

漏洞复现：

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWypTgCiauOdqibfFUJN9I5CEBzyicI3gxOvoVVUh3CLncMPts8swufkQpYw/640?wx_fmt=gif)

6. 另一处任意文件删除
------------

漏洞触发在文件`user.php`中 788 行处

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWybKBz2HGJnGw31ic6JHMDKAysvib9USrQNCiarsxBD9iabjAIOVDdR53GRw/640?wx_fmt=png)

未做任何处理，直接导致任意文件删除漏洞

漏洞复现:

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWygVs6b12TVIvYF5FbphVHbjsrDTdnVgoDRXuH8xe8b2h6icXfXpeLAwg/640?wx_fmt=gif)

7. 发布文章处 XSS
------------

在`user.php`文件中的 266 行，有个对文章内容进行过滤

```
$content = !empty($_POST['content']) ? filter_data($_POST['content']) : '';
```

跟进一下`filter_data`函数, 看它过滤了什么（include/common.fun.php 文件 985 行）

```
function filter_data($str)
{
  $str = preg_replace("/<(\/?)(script|i?frame|meta|link)(\s*)[^<]*>/", "", $str);
  return $str;
}
```

就过滤了几个标签，我们可以用 img 标签绕过：`<img src=1 onerror=alert('Tao')>`

漏洞复现：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyHOrC9A3ibSY20LicuDK0YADD7sEkkAQlGibOAA20mRFHPsO3iaFd2URf6Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWys42Qq8QEohZzIA29a25oTnfgBW27FbkeBe5aBrbAuM7FseG0GSymeA/640?wx_fmt=png)

8. 用户注册处 xss
------------

在`user.php`文件中的 763 行处

```
//编辑个人资料
elseif($act == 'edit_user_info'){
 $user_id = intval($_SESSION['user_id']);
 if(empty($user_id)){
 return false;
}
$birthday = trim($_POST['birthday']);
$sex = intval($_POST['sex']);
   $email = !empty($_POST['email']) ? trim($_POST['email']) : '';
   $msn = !empty($_POST['msn']) ? trim($_POST['msn']) : '';
   $qq = !empty($_POST['qq']) ? trim($_POST['qq']) : '';
   $mobile_phone = !empty($_POST['mobile_phone']) ? trim($_POST['mobile_phone']) : '';
   $office_phone = !empty($_POST['office_phone']) ? trim($_POST['office_phone']) : '';
   $home_phone   = !empty($_POST['home_phone']) ? trim($_POST['home_phone']) : '';
$address = !empty($_POST['address']) ? htmlspecialchars($_POST['address']) : '';
    ..............
    ...............
    $sql = "UPDATE ".table('user')." SET birthday = '$birthday', sex = '$sex', face_pic = '$face_pic', email = '$email', msn = '$msn', qq = '$qq'," ." mobile_phone = '$mobile_phone', office_phone = '$office_phone', home_phone = '$home_phone', address='$address' WHERE user_id = ".intval($_SESSION['user_id']);
$db->query($sql);
showmsg('更新个人资料成功', 'user.php');
```

`$email`只是经过了`trim`, 其余未作处理，存在 xss

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWy9yvAthq5VQBpRm0pGstQjwwV3TRZAYnVKxVSpCpq4YBxSkRJZJSt3g/640?wx_fmt=png)

观察表结构，`email`长度是足够存储产生 xss 代码的

漏洞复现：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWy0MbNLrbotiaExwljlfnyRx5RELzYG9CmqqM1drzA3rqia2TFNEjZ1sow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyQQRS2m2twh4Ix1nJ3nxscoVWXAYJPTGqMJFqkMbdmHhObLkXPpJCFw/640?wx_fmt=png)

当管理登录后台，查看用户的时候，也会触发（可拿管理员 cookie），且具有隐藏性。这里模拟一下管理员登录后台。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDAHacHdYDIhJ5tvhWxOMJWyXibXGbLEpthqJvzianfs5u4BrSkoNT2ssVATc6vC50EqibPibsywujicdNw/640?wx_fmt=png)

9. 后台大量漏洞
---------

漏洞有点多，就先不写了😁

结束语
===

        第一次尝试 cms 审计，利用的方式写的也比较单一，还有一些漏洞没有一一列出来。这次入门级的 BlueCMS 审计算是自己入坑代码审计的第一步吧。同时也希望这篇文章可以帮助到像我一样的初学者。最后我还想说`慢慢走比较快`

        文章中有什么不足和错误的地方还望师傅们指正。