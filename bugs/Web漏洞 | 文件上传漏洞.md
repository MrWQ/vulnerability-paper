> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ZE7a8OsRD168UdXaSOWEug)

  

**目录**

  

  

            文件上传漏洞

            文件上传的过滤

            上传文件过滤的绕过

            上传html文件

            文件上传的防御

            upload-libs

  

![图片](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6mpt7JbBoCdIbkf4IeUUsjTLpicJFnj5ZvTLv2tc9HW06OdNicgdZ9V90GGUonok8nibSiagrTZUicbiag/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)

**文件上传漏洞**是指攻击者上传了一个可执行的文件到服务器并执行。这里上传的文件可以是木马，病毒，恶意脚本或者WebShell等。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

         

 文件上传漏洞

  

**文件上传漏洞条件：**

· 上传的文件能被Web服务器当做脚本来执行

· 我们能够访问到上传文件的路径

**服务器上传文件命名规则：**

· 第一种：上传文件名和服务器命名一致

· 第二种：上传文件名和服务器命名不一致(随机，时间日期命名等)，但是后缀一致

· 第三种：上传文件名和服务器命名不一致(随机，时间日期命名等)，后缀也不一致

**漏洞成因**：由于程序员在对用户文件上传部分的控制不足或者处理缺陷，而导致用户可以越过其本身权限向服务器上传可执行的动态脚本文件。打个比方来说，如果你使用 php 作为服务器端的脚本语言，那么在你网站的上传功能处，就一定不能让用户上传 php 类型的文件，否则他上传一个木马文件，你服务器就被他控制了。因此文件上传漏洞带来的危害常常是毁灭性的，Apache、Tomcat、Nginx等都曝出过文件上传漏洞。

一般我们会利用文件上传漏洞上传一句话木马，然后用菜刀连接获取 webshell。但是这里有两个问题：

· 第一你的文件能上传到web服务器

· 第二你的文件能被当成脚本文件执行，所以要想让上传文件被当成脚本执行，我们经常会和文件包含漏洞和文件解析漏洞一起利用

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

文件上传过滤

1. 前端脚本检测文件扩展名。当客户端选择文件点击上传的时候，客户端还没有向服务器发送任何消息，前端的 js 脚本就对文件的扩展名进行检测来判断是否是可以上传的类型

```
<script type="text/javascript">
  function selectFile(fnUpload) {
    var filename = fnUpload.value; 
    var mime = filename.toLowerCase().substr(filename.lastIndexOf(".")); 
    if(mime!=".jpg") 
    { 
      alert("请选择jpg格式的照片上传"); 
      fnUpload.outerHTML=fnUpload.outerHTML;     
      }  
  }
</script>

```

2. 后端脚本检测文件扩展名，数据提交到后端，后端的函数对上传文件的后缀名进行检测，比如黑名单检测不允许上传 .php 、.asp 后缀格式的文件；白名单检测只允许上传 .jpg 格式的文件

```
#后端php检测
$info=pathinfo($_FILES["file"]["name"]);
    $ext=$info['extension'];// 得到文件扩展名
    if (strtolower($ext) == "php") {   #黑名单检测，不允许上传php格式的文件
            exit("不允许的后缀名");
          }

```

3. 后端通过对上传文件的 Content-Type 类型进行黑白名单检测过滤 

```
#后端对上传文件的 Content-Type类型进行检测，只允许上传 image/gif、image/jpeg、image/pjpeg格式的文件
if (($_FILES["file"]["type"] != "image/gif") && ($_FILES["file"]["type"] != "image/jpeg") 
    && ($_FILES["file"]["type"] != "image/pjpeg")){
    exit($_FILES["file"]["type"]);
    exit("不允许的格式");

```

4. 通过函数比如 getimagesize()  函数检测你上传的图片的大小是否是正常的图片大小，防止上传一句话木马。通过分析图片头部来判断这个是不是一个有效的图片格式，比如 jpg 格式图片头部是 JFIF ，gif头部是GIF89a，png头部是%PNG

```
#后端检测上传的文件是否是正常大小的图片
if(!getimagesize($_FILES["file"]["tmp_name"])){
        exit("不允许的文件");
      }

```

注意：在生产环境中的过滤，往往是这些方法都会结合的，而不只是单单的某一个过滤方法。生产环境中的过滤是很严格的

  

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

上传文件过滤的绕过

· 对于第一种前端脚本检测过滤，上传的时候上传 jpg 后缀的文件，然后用butpsuite进行抓包修改为.php的即可绕过。

· 对于第二种后端过滤，如果是后端黑名单过滤的话，我们可以想尽任何办法绕过黑名单进行上传。比如如果目标服务器是windows系统的话，我们可以利用windows系统的解析漏洞，用burpsuite抓包，将文件名后缀改为 .php. 或者 .php ，因为在windows系统内是不允许文件以 . 或者空格结尾的。所以在绕过上传之后windows系统会自动去掉 点和空格。所以，该文件最终还是会被解析成 .php 。或者还可以将php三个字母变换大小写，因为在windows系统里面是不区分大小写的。如果是白名单检测的话，我们可以采用00截断绕过。00截断利用的是php的一个漏洞。在 php<5.3.4 版本中，存储文件时处理文件名的函数认为0x00是终止符。于是在存储文件的时候，当函数读到 0x00(%00) 时，会认为文件已经结束。  
例如：我们上传 1.php%00.jpg 时，首先后缀名是合法的jpg格式，可以绕过前端的检测。上传到后端后，后端判断文件名后缀的函数会认为其是一个.jpg格式的文件，可以躲过白名单检测。但是在保存文件时，保存文件时处理文件名的函数在遇到%00字符认为这是终止符，于是丢弃后面的 .jpg，于是我们上传的 1.php%00.jpg 文件最终会被写入 1.php 文件中并存储在服务端。

· 对于第三种过滤，可以使用burpsuite进行抓包修改 Content-Type 类型

· 对于第四种过滤，可以将一句话木马写入到正常的图片中：copy  /b  1.jpg+1.php  2.jpg 。然后在利用burpsuite修改后缀为 .php ，或者利用文件包含漏洞或者文件解析漏洞，将其解析成 php脚本即可

· 还有其他的过滤，比如多文件上传时，有时服务器只对第一个上传的文件进行了检查，这时通过上传多个文件并将恶意文件掺杂进其中也可绕过服务器的过滤。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

00截断实验：

http://ctf5.shiyanbar.com/web/upload/

这个实验对用户上传文件是这样处理的，首先会对用户上传文件的后缀名进行检测，只能上传 jpg/gif/png 格式的文件，然后会对上传后的文件路径进行判断，如果是以 php 为后缀的就会返回flag，如果是以 jpg/gif/png 为后缀就会显示存储路径为固定的：./uploads/8a9e5f6a7a789acb.php 。

  

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

上传html文件

  

有很多网站采用黑名单的过滤机制，但是他们忘记了过滤 html 文件，这就造成了上传html文件形成存储型XSS。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

文件上传的防御

1. 客户端检测，使用 js 对上传图片检测，包括文件大小、文件扩展名、文件类型等

2. 服务端检测，对文件大小、文件路径、文件扩展名、文件类型、文件内容检测、对文件重命名等

3. 服务器端上传目录设置不可执行权限

4. 检查网站有没有文件解析漏洞和文件包含漏洞

5. 将文件上传到单独的文件服务器，并且单独设置文件服务器的域名

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

upload-libs

upload-labs是一个使用php语言编写的，专门收集渗透测试和CTF中遇到的各种上传漏洞的靶场。旨在帮助大家对上传漏洞有一个全面的了解。目前一共20关，每一关都包含着不同上传方式。upload-libs的项目地址：https://github.com/c0ny1/upload-labs

1：前端js限制文件后缀，抓包修改进行绕过

2：后端检测Content-Type类型，抓包修改Content-Type进行绕过

3：后端黑名单限制，禁止上传asp、aspx、php、jsp后缀的文件，可以上传php2进行绕过

4:  后端黑名单限制，禁止上传了很多后缀的文件。我们可以上传.htaccess文件，

5:  后端黑名单限制，但是只过滤了小写后缀的文件，于是我们可以将文件后缀大写

6：后端黑名单限制，可以利用windows系统特性，利用空格进行绕过

7：后端黑名单限制，可以利用windows系统特性，利用.进行绕过

8：后端黑名单限制，可以利用windows+php系统特性，利用 ::$DATA 进行绕过

9：后端黑名单限制，可以利用windows系统特性，利用.空格. 进行绕过

10: 后端黑名单限制，可以 双写后缀名 进行绕过

11: 后端白名单限制，需结合特定环境利用 00截断 绕过

12: 后端白名单限制，需结合特定环境利用 00截断 绕过

13: 后端检测上传文件的开头两个字节，制作图片马，利用服务器的文件包含漏洞

14: 后端检测上传文件的大小，制作图片马，利用服务器的文件包含漏洞

15: 后端检测图片类型，制作图片马，利用服务器的文件包含漏洞

16: 后端对上传文件做二次渲染，利用二次渲染绕过

17: 条件竞争

18: 条件竞争

19: ./ 绕过

20: 数组/.绕过

  

  

关于upload-libs的详情做法：upload-labs  ，这个文章总结的很好

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

```
版权申明：内容来源网络，版权归原创者所有。除非无法确认，都会标明作者及出处，如有侵权烦请告知，我们会立即删除并表示歉意。祝愿每一位读者生活愉快！谢谢!

```