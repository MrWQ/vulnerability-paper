\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.cnpanda.net\](https://www.cnpanda.net/codeaudit/730.html)

0x01 写在前面
---------

本文为小续师傅提供的漏洞，我来分析，续师傅还是牛逼的呀~

0x02 seacms 介绍
--------------

海洋影视管理系统（seacms，海洋 cms）是一套专为不同需求的站长而设计的视频点播系统，采用的是 php5.X+mysql 的架构，使用 fofa 搜索可以看到存在 400 + 的记录：

![](https://www.cnpanda.net/usr/uploads/2020/06/1956800292.png)

0x03 漏洞分析
---------

漏洞文件：`./comment/api/index.php`，漏洞参数：`$rlist`

为了方便说明，加上这个文件也不是很长，所以把这个文件的内容贴出来分析：

关键内容如下：

```
<?php
session\_start();
require\_once("../../include/common.php");
$id = (isset($gid) && is\_numeric($gid)) ? $gid : 0;
$page = (isset($page) && is\_numeric($page)) ? $page : 1;
$type = (isset($type) && is\_numeric($type)) ? $type : 1;
$pCount = 0;
$jsoncachefile = sea\_DATA."/cache/review/$type/$id.js";

if($page<2)
{
    if(file\_exists($jsoncachefile))
    {
        $json=LoadFile($jsoncachefile);
        die($json);
    }
}
$h = ReadData($id,$page);
$rlist = array();
if($page<2)
{
    createTextFile($h,$jsoncachefile);
}
die($h);    


function ReadData($id,$page)
{
    global $type,$pCount,$rlist;
    $ret = array("","",$page,0,10,$type,$id);
    if($id>0)
    {
        $ret\[0\] = Readmlist($id,$page,$ret\[4\]);
        $ret\[3\] = $pCount;
        $x = implode(',',$rlist);
        if(!empty($x))
        {
        $ret\[1\] = Readrlist($x,1,10000);
        }
    }    
    $readData = FormatJson($ret);
    return $readData;
}

function Readmlist($id,$page,$size)
{
    global $dsql,$type,$pCount,$rlist;
    $rlist = str\_ireplace('@', "", $rlist);    
    $rlist = str\_ireplace('/\*', "", $rlist);
    $rlist = str\_ireplace('\*/', "", $rlist);
    $rlist = str\_ireplace('\*!', "", $rlist);
    $ml=array();
    if($id>0)
    {
        $sqlCount = "SELECT count(\*) as dd FROM sea\_comment WHERE m\_type=$type AND v\_id=$id ORDER BY id DESC";
        $rs = $dsql ->GetOne($sqlCount);
        $pCount = ceil($rs\['dd'\]/$size);
        $sql = "SELECT id,uid,username,dtime,reply,msg,agree,anti,pic,vote,ischeck FROM sea\_comment WHERE m\_type=$type AND v\_id=$id ORDER BY id DESC limit ".($page-1)\*$size.",$size ";
        $dsql->setQuery($sql);
        $dsql->Execute('commentmlist' );
        while($row=$dsql->GetArray('commentmlist'))
        {
            $row\['reply'\].=ReadReplyID($id,$row\['reply'\],$rlist);
            $ml\[\]="{\\"cmid\\":".$row\['id'\].",\\"uid\\":".$row\['uid'\].",\\"tmp\\":\\"\\",\\"nick\\":\\"".$row\['username'\]."\\",\\"face\\":\\"\\",\\"star\\":\\"\\",\\"anony\\":".(empty($row\['username'\])?1:0).",\\"from\\":\\"".$row\['username'\]."\\",\\"time\\":\\"".date("Y/n/j H:i:s",$row\['dtime'\])."\\",\\"reply\\":\\"".$row\['reply'\]."\\",\\"content\\":\\"".$row\['msg'\]."\\",\\"agree\\":".$row\['agree'\].",\\"aginst\\":".$row\['anti'\].",\\"pic\\":\\"".$row\['pic'\]."\\",\\"vote\\":\\"".$row\['vote'\]."\\",\\"allow\\":\\"".(empty($row\['anti'\])?0:1)."\\",\\"check\\":\\"".$row\['ischeck'\]."\\"}";
        }
    }
    $readmlist=join($ml,",");
    return $readmlist;
}


function Readrlist($ids,$page,$size)
{
    global $dsql,$type;
    $rl=array();
    $sql = "SELECT id,uid,username,dtime,reply,msg,agree,anti,pic,vote,ischeck FROM sea\_comment WHERE m\_type=$type AND id in ($ids) ORDER BY id DESC";
    $dsql->setQuery($sql);
    $dsql->Execute('commentrlist');
    while($row=$dsql->GetArray('commentrlist'))
    {
        $rl\[\]="\\"".$row\['id'\]."\\":{\\"uid\\":".$row\['uid'\].",\\"tmp\\":\\"\\",\\"nick\\":\\"".$row\['username'\]."\\",\\"face\\":\\"\\",\\"star\\":\\"\\",\\"anony\\":".(empty($row\['username'\])?1:0).",\\"from\\":\\"".$row\['username'\]."\\",\\"time\\":\\"".$row\['dtime'\]."\\",\\"reply\\":\\"".$row\['reply'\]."\\",\\"content\\":\\"".$row\['msg'\]."\\",\\"agree\\":".$row\['agree'\].",\\"aginst\\":".$row\['anti'\].",\\"pic\\":\\"".$row\['pic'\]."\\",\\"vote\\":\\"".$row\['vote'\]."\\",\\"allow\\":\\"".(empty($row\['anti'\])?0:1)."\\",\\"check\\":\\"".$row\['ischeck'\]."\\"}";
    }
    $readrlist=join($rl,",");
    return $readrlist;
}



function ReadReplyID($gid,$cmid,&$rlist)
{
    global $dsql;
    $rlist = str\_ireplace('@', "", $rlist);    
    $rlist = str\_ireplace('/\*', "", $rlist);
    $rlist = str\_ireplace('\*/', "", $rlist);
    $rlist = str\_ireplace('\*!', "", $rlist);
    if($cmid>0)
    {
        if(!in\_array($cmid,$rlist))$rlist\[\]=$cmid;
        $row = $dsql->GetOne("SELECT reply FROM sea\_comment WHERE id=$cmid limit 0,1");
        if(is\_array($row))
        {
            $ReplyID = ",".$row\['reply'\].ReadReplyID($gid,$row\['reply'\],$rlist);
        }else
        {
            $ReplyID = "";
        }
    }else
    {
        $ReplyID = "";
    }
    return $ReplyID;
}

function FormatJson($json)
{
    $x = "{\\"mlist\\":\[%0%\],\\"rlist\\":{%1%},\\"page\\":{\\"page\\":%2%,\\"count\\":%3%,\\"size\\":%4%,\\"type\\":%5%,\\"id\\":%6%}}";
    for($i=6;$i>=0;$i--)
    {
        $x=str\_replace("%".$i."%",$json\[$i\],$x);
    }
    $formatJson = jsonescape($x);
    return $formatJson;
}

function jsonescape($txt)
{
    $jsonescape=str\_replace(chr(13),"",str\_replace(chr(10),"",json\_decode(str\_replace("%u","\\u",json\_encode("".$txt)))));
    return $jsonescape;
}

```

首先引入外部文件：`require_once("../../include/common.php");`

在该文件的第二行引入了通用检测文件`require_once('webscan/webscan.php');`

该通用检测文件将我们通过 get 传入的值放进`webscan_StopAttack()`函数进行正则过滤，正则规则如下：

```
$getfilter = "\\\\<.+javascript:window\\\\\[.{1}\\\\\\\\x|<.\*=(&#\\\\d+?;?)+?>|<.\*(data|src)=data:text\\\\/html.\*>|\\\\b(alert\\\\(|confirm\\\\(|expression\\\\(|prompt\\\\(|benchmark\\s\*?\\(.\*\\)|sleep\\s\*?\\(.\*\\)|\\\\b(group\_)?concat\[\\\\s\\\\/\\\\\*\]\*?\\\\(\[^\\\\)\]+?\\\\)|\\bcase\[\\s\\/\\\*\]\*?when\[\\s\\/\\\*\]\*?\\(\[^\\)\]+?\\)|load\_file\\s\*?\\\\()|<\[a-z\]+?\\\\b\[^>\]\*?\\\\bon(\[a-z\]{4,})\\s\*?=|^\\\\+\\\\/v(8|9)|\\\\b(and|or)\\\\b\\\\s\*?(\[\\\\(\\\\)'\\"\\\\d\]+?=\[\\\\(\\\\)'\\"\\\\d\]+?|\[\\\\(\\\\)'\\"a-zA-Z\]+?=\[\\\\(\\\\)'\\"a-zA-Z\]+?|>|<|\\s+?\[\\\\w\]+?\\\\s+?\\\\bin\\\\b\\\\s\*?\\(|\\\\blike\\\\b\\\\s+?\[\\"'\])|\\\\/\\\\\*.\*\\\\\*\\\\/|<\\\\s\*script\\\\b|\\\\bEXEC\\\\b|UNION.+?SELECT\\s\*(\\(.+\\)\\s\*|@{1,2}.+?\\s\*|\\s+?.+?|(\`|'|\\").\*?(\`|'|\\")\\s\*)|UPDATE\\s\*(\\(.+\\)\\s\*|@{1,2}.+?\\s\*|\\s+?.+?|(\`|'|\\").\*?(\`|'|\\")\\s\*)SET|INSERT\\\\s+INTO.+?VALUES|(SELECT|DELETE)@{0,2}(\\\\(.+\\\\)|\\\\s+?.+?\\\\s+?|(\`|'|\\").\*?(\`|'|\\"))FROM(\\\\(.+\\\\)|\\\\s+?.+?|(\`|'|\\").\*?(\`|'|\\"))|(CREATE|ALTER|DROP|TRUNCATE)\\\\s+(TABLE|DATABASE)";

...
  
preg\_match("/".$ArrFiltReq."/is",$StrFiltValue)
  
  

```

绕过该正则检测后，返回到 `common.php`文件向下走：

采用 foreach 的方式赋值，以此来获取全局参数变量，如 以 GET 方式：

```
foreach($\_GET as $\_k=>$\_v)
{
    if( strlen($\_k)>0 && m\_eregi('^(cfg\_|GLOBALS|\_GET|\_POST|\_COOKIE|\_REQUEST|\_SERVER|\_FILES|\_SESSION)',$\_k))
    {
        Header("Location:$jpurl");
        exit('err2');
    }
}

```

首先判断传入变量的长度，然后再传入`m_eregi()`函数判断，该函数内容如下：

```
function m\_eregi($reg,$p){
    $nreg=chgreg($reg)."i";
    return preg\_match(chgreg($reg),$p);
}

```

`chgreg()`函数如下：

```
function chgreg($reg){
    $nreg=str\_replace("/","\\\\/",$reg);
    return "/".$nreg."/";
}

```

以上代码结合起来就相当于下面的代码：

```
preg\_match('/^(cfg\_|GLOBALS|\_GET|\_POST|\_COOKIE|\_REQUEST|\_SERVER|\_FILES|\_SESSION)/i',$\_k)

```

即验证传入的参数是否含有以上字符串，若有，则跳转到首页然后退出，这里其实是对前几个版本出现的变量覆盖漏洞的修复，有兴趣的朋友可以看这篇文章：[https://xz.aliyun.com/t/6198](https://xz.aliyun.com/t/6198) ，是对 seacms 历史版本变量覆盖漏洞的总结。

在经过以上判断后，就获得了通过 get 传入的参数值，然后回到`./comment/api/index.php`文件继续向下看：

```
function ReadData($id,$page)
{
    global $type,$pCount,$rlist;
    $ret = array("","",$page,0,10,$type,$id);
    if($id>0)
    {
        $ret\[0\] = Readmlist($id,$page,$ret\[4\]);
        $ret\[3\] = $pCount;
        $x = implode(',',$rlist);
        if(!empty($x))
        {
        $ret\[1\] = Readrlist($x,1,10000);
        }
    }    
    $readData = FormatJson($ret);
    return $readData;
}

```

首先进入了`Readmlist()`函数，内容如下：

```
function Readmlist($id,$page,$size)
{
    global $dsql,$type,$pCount,$rlist;
    $rlist = str\_ireplace('@', "", $rlist);    
    $rlist = str\_ireplace('/\*', "", $rlist);
    $rlist = str\_ireplace('\*/', "", $rlist);
    $rlist = str\_ireplace('\*!', "", $rlist);
    $ml=array();
    if($id>0)
    {
        $sqlCount = "SELECT count(\*) as dd FROM sea\_comment WHERE m\_type=$type AND v\_id=$id ORDER BY id DESC";
        $rs = $dsql ->GetOne($sqlCount);
        $pCount = ceil($rs\['dd'\]/$size);
        $sql = "SELECT id,uid,username,dtime,reply,msg,agree,anti,pic,vote,ischeck FROM sea\_comment WHERE m\_type=$type AND v\_id=$id ORDER BY id DESC limit ".($page-1)\*$size.",$size ";
        $dsql->setQuery($sql);
        $dsql->Execute('commentmlist' );
        while($row=$dsql->GetArray('commentmlist'))
        {
            $row\['reply'\].=ReadReplyID($id,$row\['reply'\],$rlist);
            $ml\[\]="{\\"cmid\\":".$row\['id'\].",\\"uid\\":".$row\['uid'\].",\\"tmp\\":\\"\\",\\"nick\\":\\"".$row\['username'\]."\\",\\"face\\":\\"\\",\\"star\\":\\"\\",\\"anony\\":".(empty($row\['username'\])?1:0).",\\"from\\":\\"".$row\['username'\]."\\",\\"time\\":\\"".date("Y/n/j H:i:s",$row\['dtime'\])."\\",\\"reply\\":\\"".$row\['reply'\]."\\",\\"content\\":\\"".$row\['msg'\]."\\",\\"agree\\":".$row\['agree'\].",\\"aginst\\":".$row\['anti'\].",\\"pic\\":\\"".$row\['pic'\]."\\",\\"vote\\":\\"".$row\['vote'\]."\\",\\"allow\\":\\"".(empty($row\['anti'\])?0:1)."\\",\\"check\\":\\"".$row\['ischeck'\]."\\"}";
        }
    }
    $readmlist=join($ml,",");
    return $readmlist;
}

```

首先对`$rlist`变量进行了字符串检查，若存在`@`、`/*`、`*/`、`*!`字符，则将这些字符置空，然后将`$type`、`$id`等变量传入 sql 语句，执行语句后取值输出

跳出`Readmlist()`回到`ReadData()`函数继续向下看

以`,`为连接符把`$rlist`数组元素组合为一个字符串，然后赋值给变量`$x`，最后将`$x`传入`Readrlist()`函数，来看该函数内容：

```
function Readrlist($ids,$page,$size)
{
    global $dsql,$type;
    $rl=array();
    $sql = "SELECT id,uid,username,dtime,reply,msg,agree,anti,pic,vote,ischeck FROM sea\_comment WHERE m\_type=$type AND id in ($ids) ORDER BY id DESC";
    $dsql->setQuery($sql);
    $dsql->Execute('commentrlist');
    while($row=$dsql->GetArray('commentrlist'))
    {
        $rl\[\]="\\"".$row\['id'\]."\\":{\\"uid\\":".$row\['uid'\].",\\"tmp\\":\\"\\",\\"nick\\":\\"".$row\['username'\]."\\",\\"face\\":\\"\\",\\"star\\":\\"\\",\\"anony\\":".(empty($row\['username'\])?1:0).",\\"from\\":\\"".$row\['username'\]."\\",\\"time\\":\\"".$row\['dtime'\]."\\",\\"reply\\":\\"".$row\['reply'\]."\\",\\"content\\":\\"".$row\['msg'\]."\\",\\"agree\\":".$row\['agree'\].",\\"aginst\\":".$row\['anti'\].",\\"pic\\":\\"".$row\['pic'\]."\\",\\"vote\\":\\"".$row\['vote'\]."\\",\\"allow\\":\\"".(empty($row\['anti'\])?0:1)."\\",\\"check\\":\\"".$row\['ischeck'\]."\\"}";
    }
    $readrlist=join($rl,",");
    return $readrlist;
}

```

`$x`为该函数中的`$ids`变量，直接传入了 SQL 语句，然后放入`setQuery()`函数，来看看`setQuery()`函数：

```
function SetQuery($sql)
    {
        $prefix="sea\_";
        $sql = str\_replace($prefix,$this->dbPrefix,$sql);
        $this->queryString = $sql;
    }

```

把 SQL 语句里的`sea_`替换为`$this->dbPrefix`(在配置文件中为`$cfg_dbprefix = '~dbprefix~';`) 再返回 sql 语句，继续传入`Execute()`：

```
function Execute($id="me", $sql='')
    {
        global $dsql;
        self::$i++;
        if($dsql->isClose)
        {
            $this->Open(false);
            $dsql->isClose = false;
        }
        if(!empty($sql))
        {
            $this->SetQuery($sql);
        }

        
        if($this->safeCheck)
        {
            CheckSql($this->queryString);
        }
    
    $t1 = ExecTime();
        
        $this->result\[$id\] = mysqli\_query($this->linkID,$this->queryString);
        
        if($this->result\[$id\]===false)
        {
            $this->DisplayError(mysqli\_error($this->linkID)." <br />Error sql: <font color='red'>".$this->queryString."</font>");
        }
}

```

该函数主要内容是对传入的 SQL 语句进行安全检测，若 SQL 语句安全则继续执行 SQL 语句。

`CheckSql($this->queryString);`函数内容如下：

```
function CheckSql($db\_string,$querytype='select')
{
    global $cfg\_cookie\_encode;
    $clean = '';
    $error='';
    $old\_pos = 0;
    $pos = -1;
    $log\_file = sea\_INC.'/../data/'.md5($cfg\_cookie\_encode).'\_safe.txt';
    $userIP = GetIP();
    $getUrl = GetCurUrl();    
    $db\_string = str\_ireplace('--', "", $db\_string);
    $db\_string = str\_ireplace('/\*', "", $db\_string);
    $db\_string = str\_ireplace('\*/', "", $db\_string);
    $db\_string = str\_ireplace('\*!', "", $db\_string);
    $db\_string = str\_ireplace('//', "", $db\_string);
    $db\_string = str\_ireplace('\\\\', "", $db\_string);
    $db\_string = str\_ireplace('hex', "he", $db\_string);    
    $db\_string = str\_ireplace('updatexml', "updatexm", $db\_string);
    $db\_string = str\_ireplace('extractvalue', "extractvalu", $db\_string);
    $db\_string = str\_ireplace('benchmark', "benchmar", $db\_string);
    $db\_string = str\_ireplace('sleep', "slee", $db\_string);
    $db\_string = str\_ireplace('load\_file', "load-file", $db\_string);
    $db\_string = str\_ireplace('outfile', "out-file", $db\_string);
    $db\_string = str\_ireplace('ascii', "asci", $db\_string);    
    $db\_string = str\_ireplace('char(', "cha", $db\_string);    
    $db\_string = str\_ireplace('substr', "subst", $db\_string);
    $db\_string = str\_ireplace('substring', "substrin", $db\_string);
    $db\_string = str\_ireplace('script', "scrip", $db\_string);
    $db\_string = str\_ireplace('frame', "fram", $db\_string);
    $db\_string = str\_ireplace('information\_schema', "information-schema", $db\_string);
    $db\_string = str\_ireplace('exp', "ex", $db\_string);
    $db\_string = str\_ireplace('GeometryCollection', "GeometryCollectio", $db\_string);
    $db\_string = str\_ireplace('polygon', "polygo", $db\_string);
    $db\_string = str\_ireplace('multipoint', "multipoin", $db\_string);
    $db\_string = str\_ireplace('multilinestring', "multilinestrin", $db\_string);
    $db\_string = str\_ireplace('linestring', "linestrin", $db\_string);
    $db\_string = str\_ireplace('multipolygon', "multipolygo", $db\_string);    

    
    if($querytype=='select')
    {
        $notallow1 = "\[^0-9a-z@\\.\_-\]{1,}(union|sleep|benchmark|load\_file|outfile)\[^0-9a-z@\\.-\]{1,}";

        
        if(m\_eregi($notallow1,$db\_string)){exit('SQL check');}
        if(m\_eregi('<script',$db\_string)){exit('SQL check');}
        if(m\_eregi('/script',$db\_string)){exit('SQL check');}
        if(m\_eregi('script>',$db\_string)){exit('SQL check');}
        if(m\_eregi('if:',$db\_string)){exit('SQL check');}
        if(m\_eregi('--',$db\_string)){exit('SQL check');}
        if(m\_eregi('char(',$db\_string)){exit('SQL check');}
        if(m\_eregi('\*/',$db\_string)){exit('SQL check');}
    }

    
    while (true)
    {
        $pos = stripos($db\_string, '\\'', $pos + 1);
        if ($pos === false)
        {
            break;
        }
        $clean .= substr($db\_string, $old\_pos, $pos - $old\_pos);
        while (true)
        {
            $pos1 = stripos($db\_string, '\\'', $pos + 1);
            $pos2 = stripos($db\_string, '\\\\', $pos + 1);
            if ($pos1 === false)
            {
                break;
            }
            elseif ($pos2 == false || $pos2 > $pos1)
            {
                $pos = $pos1;
                break;
            }
            $pos = $pos2 + 1;
        }
        $clean .= '$s$';
        $old\_pos = $pos + 1;
    }
    $clean .= substr($db\_string, $old\_pos);
    $clean = trim(strtolower(preg\_replace(array('~\\s+~s' ), array(' '), $clean)));

    if (stripos($clean, '@') !== FALSE  OR stripos($clean,'char(')!== FALSE  OR stripos($clean,'script>')!== FALSE   OR stripos($clean,'<script')!== FALSE  OR stripos($clean,'"')!== FALSE OR stripos($clean,'$s$$s$')!== FALSE)
        {
            $fail = TRUE;
            if(preg\_match("#^create table#i",$clean)) $fail = FALSE;
            $error="unusual character";
        }
    
    if (stripos($clean, 'union') !== false && preg\_match('~(^|\[^a-z\])union($|\[^\[a-z\])~s', $clean) != 0)
    {
        $fail = true;
        $error="union detect";
    }

    
    elseif (stripos($clean, '/\*') > 2 || stripos($clean, '--') !== false || stripos($clean, '#') !== false)
    {
        $fail = true;
        $error="comment detect";
    }

    
    elseif (stripos($clean, 'sleep') !== false && preg\_match('~(^|\[^a-z\])sleep($|\[^\[a-z\])~s', $clean) != 0)
    {
        $fail = true;
        $error="sleep detect";
    }
    elseif (stripos($clean, 'updatexml') !== false && preg\_match('~(^|\[^a-z\])updatexml($|\[^\[a-z\])~s', $clean) != 0)
    {
        $fail = true;
        $error="updatexml  detect";
    }
    elseif (stripos($clean, 'extractvalue') !== false && preg\_match('~(^|\[^a-z\])extractvalue($|\[^\[a-z\])~s', $clean) != 0)
    {
        $fail = true;
        $error="extractvalue  detect";
    }
    elseif (stripos($clean, 'benchmark') !== false && preg\_match('~(^|\[^a-z\])benchmark($|\[^\[a-z\])~s', $clean) != 0)
    {
        $fail = true;
        $error="benchmark detect";
    }
    elseif (stripos($clean, 'load\_file') !== false && preg\_match('~(^|\[^a-z\])load\_file($|\[^\[a-z\])~s', $clean) != 0)
    {
        $fail = true;
        $error="file fun detect";
    }
    elseif (stripos($clean, 'into outfile') !== false && preg\_match('~(^|\[^a-z\])into\\s+outfile($|\[^\[a-z\])~s', $clean) != 0)
    {
        $fail = true;
        $error="file fun detect";
    }

    
    elseif (preg\_match('~\\(\[^)\]\*?select~s', $clean) != 0)
    {
        $fail = true;
        $error="sub select detect";
    }
    if (!empty($fail))
    {
        fputs(fopen($log\_file,'a+'),"$userIP||$getUrl||$db\_string||$error\\r\\n");
        exit("<font size='5' color='red'>Safe Alert: Request Error step 2!</font>");
    }
    else
    {

        return $db\_string;
    }
}

```

至此，整个漏洞挖掘的链就形成了，如下图所示：

![](https://www.cnpanda.net/usr/uploads/2020/06/1898956867.png)

可以看到，其实该漏洞挖掘的关键点有两个：

*   如何绕过 webscan\_StopAttack()
*   如何绕过`CheckSql()`函数的检测

我们首先来看第一个关键点，我们知道一般的注入语句都是形如`union select 1,2,3,4,5,6,7,pass,9 from admin --`形式

但在该过滤点使用正则过滤了`union select`的形式：

```
UNION.+?SELECT\\s\*

```

这种过滤很容易绕，比如我们熟知的绕 waf 技巧`%23%0a` 就可以绕过该过滤，如下：

`union%23%0aselect%23%0a1,2,3,4,5,6,7,pass,9 from admin --`

（具体更多的方式可以阅读此文：[https://www.secpulse.com/archives/53328.html](https://www.secpulse.com/archives/53328.html)）

接下来就是第二个关键点，`CheckSql()`函数过滤了一大堆东西，这个函数原本是 80sec 写的，开发者对这个过滤函数进行了修改：

![](https://www.cnpanda.net/usr/uploads/2020/06/1992186737.png)

![](https://www.cnpanda.net/usr/uploads/2020/06/779418631.png)

可以看到，作者增加了对关键字符、关键字的过滤清空，但也正是这些多此一举的内容导致我们可以绕过这些过滤。

在 80sec 防注入程序中有个特征就是会将两个单引号之间的内容，用字符串`$s$`进行替换，例如`insert into admin(username,passdord) value ('admin','hello')`会被替换为`insert into admin(username,passdord) value ($s$,$s$)`

因此我们可以利用这个特性使得`$clean`变量中不会出现敏感字，从而绕过`CheckSql()`函数检测

我们知道在 Mysql 中，定义变量用 @字符，如我们可以使用`set @panda=’test’`，来为变量赋值

在这里我们为了合法的构造出一个单引号，就可以用 @'放入 sql 语句当中，来帮助我们绕过检查

需要注意的是，虽然我们绕过了检测，但我们的 SQL 语句中多了单引号，会导致原本的 SQL 语句失效，所以我们需要进一步来修改我们的注入语句, 来利用注释符 (`/*`/`*/`、`#`) 将单引号注释掉

因此语句为：

```
UNION%20SELECT%23%0a1,password,3,4,5,6,7,8,9,10,11%23%0afrom%23%0asea\_admin

```

但此时回头看，在`Readmlist()`函数最开始的地方：

```
    global $dsql,$type,$pCount,$rlist;
    $rlist = str\_ireplace('@', "", $rlist);    
    $rlist = str\_ireplace('/\*', "", $rlist);
    $rlist = str\_ireplace('\*/', "", $rlist);
    $rlist = str\_ireplace('\*!', "", $rlist);

```

对于这些字符进行了置空处理，因此如果我们直接传入，肯定会被过滤，导致我们的注释符失效，依旧不能达到我们的目的

但是注意，`$rlist`是全局变量，因此在`Readmlist()`函数中处理后的值，会保留继续传到`Readrlist()`函数（上方的流程图显示的很明白），也就是说如果我们直接传入上方我们构建的语句，就会被过滤成：

```
\`'\`,UNION%20SELECT%23%0a1,password,3,4,5,6,7,8,9,10,11%23%0afrom%23%0asea\_admin-- \`'\`

```

这显然传入 SQL 语句中会报错，因此我们需要双写符号从而构建注释符，最终结果如下：

这条语句首先进入`Readmlist()`函数，变成了

```
UNION%20SELECT%23%0a1,password,3,4,5,6,7,8,9,10,11%23%0afrom%23%0asea\_admin-- @\`'\`

```

然后继续传入`Readrlist()`函数，经过字符串替换变成了：

```
\`'\`,UNION%20SELECT%23%0a1,password,3,4,5,6,7,8,9,10,11%23%0afrom%23%0asea\_admin \`'\`

```

成功构造出两个单引号，最终使得传入的语句为：`$s$`，绕过所有的过滤

其实如果仅仅是这样, 我们也是无法绕过过滤的, 因为虽然我们绕过了检测, 但是经过层层过滤和转换, 最终的 SQL 语句并不是我们想要的，如果直接传入 `mysqli_query()`去执行是会出错的。

但是骚气的地方是：

![](https://www.cnpanda.net/usr/uploads/2020/06/2167077469.png)

![](https://www.cnpanda.net/usr/uploads/2020/06/1449914742.png)

可以看到，经过 `CheckSql()`函数过滤的 SQL 语句并没有传入 `mysqli_query()`中去执行，在`mysqli_query()`中执行的是原始的，在`Readmlist()`函数中处理后的语句。这里的 `CheckSql()`函数也仅仅是起到判断作用，根本是没有对传入的 SQL 语句进行处理。

我们可以看到最终传入 `mysqli_query()`中去执行的 SQL 语句如下图所示:

![](https://www.cnpanda.net/usr/uploads/2020/06/2037389285.png)

最终的执行效果：

![](https://www.cnpanda.net/usr/uploads/2020/06/1704596438.png)

0x04 结尾
-------

最终没有直接给出 payload，留下了两个坑点。文章内其实已经写得很明白了，注意参数变量类型，编码，基本上就可以构建出最后的 pyaload，此文的目的是想让大家进一步学习代码审计相关的知识，有的时候，并不是写得过滤内容越多越好，还是要看我们最终执行的地方是否存在问题。

使用微信扫描二维码完成支付

![](https://www.cnpanda.net/usr/themes/sec/img/alipay-2.jpg)