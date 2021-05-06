> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9497)

[https://github.com/EnableSecurity/wafw00f/](https://github.com/EnableSecurity/wafw00f/)  
Wafw00f 是一款知名的 WAF 识别工具，目前 Github 有 2300 的 Star，由 Python 编写。简单测试了几个网站，发现识别效果不是那么好

整体
--

[![](https://xuyiqing-1257927651.cos.ap-beijing.myqcloud.com/blog/17.png)](https://xuyiqing-1257927651.cos.ap-beijing.myqcloud.com/blog/17.png)

*   docs：sphinx 自动生成文档的工作
*   wafw00f：代码
*   setup.py：安装脚本

wafw00f
-------

[![](https://xuyiqing-1257927651.cos.ap-beijing.myqcloud.com/blog/19.png)](https://xuyiqing-1257927651.cos.ap-beijing.myqcloud.com/blog/19.png)

*   bin：启动文件，执行这里的脚本即可启动程序
*   lib：asciiarts 是 logo，evillib 是发请求的工具类，后续分析
*   plugins：指纹识别的规则，后续分析
*   main：核心代码
*   manager：管理规则的脚本
*   wafprio：指纹识别优先级规定

首先看一下 plugins 目录下的规则文件，每一个都是 py 文件，并且都有函数`is_waf`：

```
def is_waf(self):
    schemes = [
        self.matchHeader(('aeSecure-code', '.+?')),
        self.matchContent(r'aesecure_denied\.png')
    ]
    if any(i for i in schemes):
        return True
    return False
```

比如以上这个规则，是匹配响应头和响应 Body 中的关键字

正是分析代码，按照一般的规则，先从 main.py 分析  
一开始是常见的参数解析：  
`parser = OptionParser(usage='%prog url1 [url2 [url3 ... ]]\r\nexample: %prog http://www.victim.org/')`

338 行`print(randomArt())`调用`asciiarts.py`打印 LOGO

如果是`-l`参数那么就打印所有可用的 waf，从 wafprio 文件中读取：

```
if options.list:
    ......
    try:
        m = [i.replace(')', '').split(' (') for i in wafdetectionsprio]
        print(R+'  WAF Name'+' '*24+'Manufacturer\n  '+'-'*8+' '*24+'-'*12+'\n')
        max_len = max(len(str(x)) for k in m for x in k)
        ......
```

如果是`-v`参数那么就打印版本信息：

```
print('[+] The version of WAFW00F you have is %sv%s%s' % (B, __version__, E))
```

如果有自定义请求头，那么就尝试从指定的文件中解析请求头，`getheaders`函数较简单

```
extraheaders = getheaders(options.headers)
```

如果输入是一个完整的文件，尝试 JSON 解析：

```
with open(options.input) as f:
    try:
        urls = json.loads(f.read())
    except json.decoder.JSONDecodeError:
        log.critical("JSON file %s did not contain well-formed JSON", options.input)
        sys.exit(1)
```

另外也支持 CSV 文件和最基础的 txt 列表格式：

```
elif options.input.endswith('.csv'):
    columns = defaultdict(list)
    with open(options.input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k,v) in row.items():
                columns[k].append(v)
    targets = columns['url']
else:
    with open(options.input) as f:
        targets = [x for x in f.read().splitlines()]
```

然后进行了 URL 验证，比如是否 HTTP 开头，代理信息处理等操作，创建一个核心类`WAF00F`，并发请求：

```
attacker = WAFW00F(target, debuglevel=options.verbose, path=path,
            followredirect=options.followredirect, extraheaders=extraheaders,
                proxies=proxies)
global rq
rq = attacker.normalRequest()
```

`WAF00F`类在开头定义了五个 Payload，为了触发 WAF 而设计：

```
xsstring = '<script>alert("XSS");</script>'
sqlistring = "UNION SELECT ALL FROM information_schema AND ' or SLEEP(5) or '"
lfistring = '../../../../etc/passwd'
rcestring = '/bin/cat /etc/passwd; ping 127.0.0.1; curl google.com'
xxestring = '<!ENTITY xxe SYSTEM "file:///etc/shadow">]><pwn>&hack;</pwn>'
```

上面调用的`normalRequest`函数使用了 evillib 文件，简单的 requests 库使用：

```
if not headers: 
    h = self.headers
else: h = headers
req = requests.get(self.target, proxies=self.proxies, headers=h, timeout=timeout,
        allow_redirects=self.allowredir, params=params, verify=False)
```

拿到响应后，就要进行 WAF 探测的内容了。`options.findall`是传入的参数 - a，代表你想测试所有的 WAF，不因为探测到某一种而停止，这里作为一个布尔参数传入：

```
waf = attacker.identwaf(options.findall)
```

`identwaf`开头又调用了`performCheck`函数，这个函数作用是执行它的参数（函数传参），所以需要关心的是`centralAttack`是什么：

```
try:
    self.attackres = self.performCheck(self.centralAttack)
except RequestBlocked:
    return detected
```

可以看到是发请求，参数是上面的 payload，为了触发 WAF：

```
return self.Request(path=self.path, params={'a': self.xsstring, 'b': self.sqlistring, 'c': self.lfistring})
```

继续回到上层，如果响应为空，会抛出异常，返回检测失败；如果返回正常，那么会从上文提到的指纹识别优先级规定文件`wafprio`中读取并逐个检测，如果有`findall`表示就会一直执行：

```
for wafvendor in self.checklist:
    self.log.info('Checking for %s' % wafvendor)
    if self.wafdetections[wafvendor](self):
        detected.append(wafvendor)
        if not findall:
            break
self.knowledge['wafname'] = detected
return detected
```

`wafdetections`的代码如下，`load_plugins`是上文提到`manager.py`文件中的函数，加载所有插件进行检测，每一个规则都有`is_waf`函数，记录了规则匹配方式；最后求差集确保添加到`checklist`中，也就是上文的指纹识别优先级规定文件：

```
wafdetections = dict()

plugin_dict = load_plugins()
result_dict = {}
for plugin_module in plugin_dict.values():
    wafdetections[plugin_module.NAME] = plugin_module.is_waf
# Check for prioritized ones first, then check those added externally
checklist = wafdetectionsprio
checklist += list(set(wafdetections.keys()) - set(checklist))
```

注意一个写法值得思考，这里的`wafdetections`不是一个字典吗？使用索引`[]`得到某一个 item 后，为什么要在后面加一个`(self)`呢？

```
if self.wafdetections[wafvendor](self):
```

要回答这个问题其实很简单，因为这个字典中保存的是`key=string;value=function`这样的数据，item 的值就是函数，这时候可以使用`wafdetections[key](param)`的方式调用函数，而这个函数是什么呢？就是规则文件的`is_waf`函数：

```
def is_waf(self):
    schemes = [
        self.matchHeader(('aeSecure-code', '.+?')),
        self.matchContent(r'aesecure_denied\.png')
    ]
    if any(i for i in schemes):
        return True
    return False
```

而规则文件调用了`self.matchHeader`和`self.matchContent`函数，所以我们应该查看`WAFW00F`类的这两个函数，因为参数`self`就是`WAFW00F`类的`this`指针

`matchHeader`函数如下：解析响应头，处理 Cookie，然后正则匹配，比较简单

```
def matchHeader(self, headermatch, attack=False):
    if attack:
        r = self.attackres
    else: r = rq
    if r is None:
        return
    header, match = headermatch
    headerval = r.headers.get(header)
    if headerval:
        # set-cookie can have multiple headers, python gives it to us
        # concatinated with a comma
        if header == 'Set-Cookie':
            headervals = headerval.split(', ')
        else:
            headervals = [headerval]
        for headerval in headervals:
            if re.search(match, headerval, re.I):
                return True
    return False
```

`matchContent`函数也是这样的原理，正则匹配响应 Body：

```
def matchContent(self, regex, attack=True):
    if attack:
        r = self.attackres
    else: r = rq
    if r is None:
        return
    # We may need to match multiline context in response body
    if re.search(regex, r.text, re.I):
        return True
    return False
```

层层跳出，回到最开始的地方

```
waf = attacker.identwaf(options.findall)
```

当没有匹配到任何一个 WAF 的时候，会执行这样的代码：

```
if attacker.genericdetect():
    log.info('Generic Detection: %s' % attacker.knowledge['generic']['reason'])
    print('[*] The site %s seems to be behind a WAF or some sort of security solution' % target)
    print('[~] Reason: %s' % attacker.knowledge['generic']['reason'])
    results.append(buildResultRecord(target, 'generic'))
else:
    print('[-] No WAF detected by the generic detection')
    results.append(buildResultRecord(target, None))
```

观察`genericdetect`函数，先发一个常见的请求，然后发带有 payload 的请求，然后对比响应码，如果不相等，证明检测到了 WAF。也就是说这个函数为了验证某个站点是否是具有 WAF 的（但是 WAFW00F 本身并没有识别出来）

```
resp1 = self.performCheck(self.normalRequest)
......
resp2 = self.performCheck(self.xssAttack)
if resp1.status_code != resp2.status_code:
    return True
......
resp2 = self.performCheck(self.lfiAttack)
......
resp2 = self.performCheck(self.sqliAttack)
......
```

后续的代码没有什么值得分析之处，将识别结果打印到命令行或者输出文件这样的功能

*   wafw00f 有比较优秀的代码质量，丰富的输入输出（JSON、CSV、TXT）
*   规则用 py 直接编写，能否改进为 JSON，YML 等文件
*   作为一个拥有 2300 星的 python 项目，却没有使用任何高性能技术（多线程、多进程、协程）
*   可以参考它的 payload 触发 waf 识别的原理，编写更完善的工具

参考 wafw00f 的源码，我打算用 golang 做一下更完善的版本  
目前做了个开头：[https://github.com/EmYiQing/go-wafw00f](https://github.com/EmYiQing/go-wafw00f)