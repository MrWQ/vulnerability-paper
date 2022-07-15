> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ZtWRmC8F4V_k1F51_dkOnA)

**STATEMENT**

**声明**

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测及文章作者不为此承担任何责任。

雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

**NO.1 SMTP**

简单邮件传输协议（Simple Mail Transfer Protocol，SMTP）是在 Internet 传输电子邮件的事实标准。

  
SMTP 是一个相对简单的基于文本的协议。在其之上指定了一条消息的一个或多个接收者（在大多数情况下被确认是存在的），然后消息文本会被传输。可以很简单地通过 telnet 程序来测试一个 SMTP 服务器。SMTP 使用 TCP 端口 25。要为一个给定的域名决定一个 SMTP 服务器，需要使用 MX (Mail eXchange) DNS。

  
——摘自 百度百科

**原理**

使用 SMTP RCPT TO：返回 250 状态码，证明邮箱地址存在；返回 550 状态码，证明邮箱地址不存在。

**注意**

有些邮箱服务设置为 Catch-all，这意味该域名下的每个邮箱地址，都会被认为是存在的。

**Catch-all**

Catch-all 邮箱：全域设置 (以该邮箱为后缀的任何邮箱名，该邮箱服务器都会接收)

  
例如这个域 microsci.com，会设置一个 Catch-all 邮箱地址如: info@microsci.com，该地址可以用来接收拼错或者无效的来自 microsci.com 域的邮箱。

  
如 sales1@microsci.com 是不存在无效的账户。当给这个邮箱 sales1@microsci.com 发邮件时，由于 sales1@microsci.com 邮箱不存在就会把邮件自动转到 info@microsci.com (Catch-all 邮箱里)。

  
这样的话，就造成检测该域的邮箱都是通过的。因为该域的邮箱会接受该域下的所有邮箱。然而也有这样的情况，收件人邮件服务器可能会默默地放弃该邮件或事后发送退回邮件。

  
**[如何配置 catch-all，官网文档 配置 catch-all 邮箱]**

https://docs.microsoft.com/zh-cn/previous-versions/office/exchange-server-2010/bb691132(v=exchg.141

**NO.2 验证过程**

**查找 MX 记录**

```
nslookup -type=MX mail.com
```

找到两条 MX 记录，SMTP 服务器的地址分别为：  
mail.commail exchanger = 10 mx2.mail.com.  
mail.commail exchanger = 10 mx.mail.com.

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUniauOoMcAWkJibdLeQSOZTFPnvicyRbhqyVCgz9zItRZaA2LGvUzKOSwbgJ8WLWlBh7GswVubt431g/640?wx_fmt=png)

**建立连接**

SMTP 默认是 TCP 端口 25，使用 telnet 命令进行 TCP 的连接。

```
❯ telnet mx.mail.com 25
Trying 180.xx.xx.199...
Connected to mx.mail.com.
Escape character is '^]'.
220 mx.mail.com ESMTP
```

响应码 220，证明连接成功。

**HELO/EHLO**

向服务器表明邮件发送的服务器

```
❯ HELO mx.mail.com
250 mx.mail.com

❯ EHLO mx.mail.com
250-mx.mail.com
250-8BITMIME
250-SIZE 68157440
250 STARTTLS
```

响应码 250，证明成功。

**MAIL FROM**

表明发件人

```
❯ MAIL FROM:<test@mail.com>
250 sender <test@mail.com> ok
```

**RCPT TO**

如果 RCPT TO 的响应码是 250 或者 251 都表示邮件地址存在，如果响应码是 5xx，则表明邮件地址不存在，如果是 4xx 则代表无法确认。

```
❯ MAIL FROM:<test@mail.com>
250 sender <test@mail.com> ok

❯ RCPT TO:<mailsec@mail.com>
250 recipient <mailsec@mail.com> ok

❯ RCPT TO:<mail@mail.com>
550 # 5.1.0 Address rejected.
```

**NO.3 工具化**

**Python**

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUniauOoMcAWkJibdLeQSOZTF70pyqU3UPNeOzItkmEW2dWfpzbn0cNuibuBovBsHRjicexzibcQn2TibxA/640?wx_fmt=png)

**Metasploit**

开篇提到过 Catch-all 。实际上，MAIL 服务器如果做了这种配置，任何邮箱地址通过 SMTP 这种方法都会校验通过。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUniauOoMcAWkJibdLeQSOZTFiaCC3hoPmCeFsrohZydicSyXnbBl0MtFBsTjSLmg0q50zO9klKYEEreQ/640?wx_fmt=png)

可以使用 MSF 的 auxiliary/scanner/msmail/onprem_enum 模块进行验证，该模块利用 OWA (Outlook Webapp) 基于时间的用户枚举。

  
**[作者文档 onprem_enum.md]**

https://github.com/rapid7/metasploit-framework/blob/master/documentation/modules/auxiliary/scanner/msmail/onprem_enum.md

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUniauOoMcAWkJibdLeQSOZTFyaIxibicWb619ZLSHXaY4lhIlgRyQnVv7saibMWKaAWtw870LQNxyJ8mw/640?wx_fmt=png)

**NO.4 附: Python 代码**

```
# -*- coding: utf-8 -*-
import dns.resolver
import argparse
from socket import *
import random

def ColorPrint(string="", flag="", verbose=""):
    colors = {
        u"gray": "2",
        u"red": "31",
        u"green": "32",
        u"yellow": "33",
        u"blue": "34",
        u"pink": "35",
        u"cyan": "36",
        u"white": "37",
    }
    flags = {
        u"error": "[-] ",
        u"warning": "[!] ",
        u"info": "[*] ",
        u"success": "[+] ",
        u"debug": ">>> ",
        u"echo": ">>> "
    }
    try:
        if flag == 'error':
            print(u"\033[%sm%s%s" % (colors[u"red"], flags[flag], string))
        if flag =="info":
            print(u"\033[%sm%s%s" % (colors[u"white"], flags[flag], string))
        if flag == 'echo' or flag == '' or flag == 0:
            print(u"\033[%sm%s%s" % (colors[u"white"], flags[flag], string))
        if flag == 'success':
            print(u"\033[%sm%s%s" % (colors[u"green"], flags[flag], string))
        if verbose == 1:
            if flag == 'warning':
                print(u"\033[%sm%s%s" % (colors[u"yellow"], flags[flag], string))
            if flag == 'debug':
                print(u"\033[%sm%s%s" % (colors[u"white"], flags[flag], string))
    except:
        return 0

# 第一步: 获取域名MX 记录
def DNSQuery(mailaddr):
    dns_resolver = dns.resolver.Resolver(configure=False)
    dns_resolver.timeout = 5
    dns_resolver.lifetime = 5
    dns_resolver.nameservers = ['119.29.29.29']
    record = "MX"
    domain = mailaddr[mailaddr.find(u"@") + 1:]
    ColorPrint("query MX of DNS for %s" % domain, flag= "echo", verbose=verbose)
    try:
        MX = dns_resolver.resolve(domain, record)
        m = random.randint(0, len(MX))
        mx = MX[0].exchange
        strMx = str(mx)[:-1]
        assert strMx != u""
    except Exception as e:
        ColorPrint("query MX of %s failed: %s" % (strMx, e), flag="error", verbose=verbose)
        return 0
    ColorPrint("MX Server: %s" % strMx, flag="info", verbose=verbose)
    return strMx

# 第二步: 请求mail服务器
def smtpsend(server, port=20, mail_rcptTo=""):
    mailserver = (server, port)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    helloDomain = server[server.find(u".") + 1:]
    mail_from = "mail@gmail.com"
    ColorPrint("connect to %s:%.f" % (server, port), flag="debug", verbose=verbose)
    try:
        clientSocket.connect(mailserver)
        recv = clientSocket.recv(1024)
        recv = recv.decode()
        if recv[0:3] != '220':
            ColorPrint("info: " + recv, flag="debug", verbose=verbose)
            return 0
    except Exception as e:
        ColorPrint("Error: %s" % e, flag="error", verbose=verbose)
        ColorPrint("Done. " , flag="info", verbose=verbose)
        return 0
    ColorPrint("Message after connection request: \n" + recv, flag="debug", verbose=verbose)
    hello_command = "EHLO %s\r\n" % helloDomain
    clientSocket.send(hello_command.encode())
    recv1 = clientSocket.recv(1024)
    recv1 = recv1.decode()
    ColorPrint("Message after EHLO command:\n" + recv1, flag="debug", verbose=verbose)
    if recv1[:3] != '250':
        ColorPrint("250 reply not received from server." + recv1, flag="error", verbose=verbose)
        return 0
    mail_from_command = "MAIL FROM:<%s>\r\n" % mail_from
    clientSocket.send(mail_from_command.encode())
    recv2 = clientSocket.recv(1024)
    recv2 = recv2.decode()
    ColorPrint("After MAIL FROM command: " + recv2, flag="debug", verbose=verbose)
    rcptTo = "RCPT TO:<%s>\r\n" % mail_rcptTo
    clientSocket.send(rcptTo.encode())
    recv3 = clientSocket.recv(1024)
    recv3 = recv3.decode()
    if recv3[:3] == '550':
        ColorPrint("Account: %s does not exist." % mail_rcptTo,  flag="error", verbose=verbose)
        ColorPrint("Done. ", flag="info", verbose=verbose)
        return 0
    ColorPrint("Account: %s exists." % mail_rcptTo, flag="success", verbose=verbose)
    ColorPrint("After RCPT TO command: %s" % recv3, flag="debug", verbose=verbose)
    quit = "QUIT\r\n"
    clientSocket.send(quit.encode())
    recv4 = clientSocket.recv(1024)
    clientSocket.close()
    ColorPrint("Done. " , flag="info", verbose=verbose)
    return mail_rcptTo


if __name__ == "__main__":
    '''
    port = 25
    verbose = False # 详细输出,可输出debug信息
    mailaddr = "xxxx@mail.com" # 需要验证的邮箱地址
    mail_rcptTo = mailaddr
    server = DNSQuery(mailaddr)
    smtpsend(server, port, mail_rcptTo)
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email",
                        help="Verification Email Address.", required=True)
    parser.add_argument("-s", "--server",
                        help="Smtp Server.")
    parser.add_argument("-p", "--port",
                        help="Smtp Server Port.", default=25, type=int)
    parser.add_argument("-v", "--verbose",
                        help="verbose info (choice in [True, False])", default=False, type=bool)

    args = parser.parse_args()

    port = args.port
    verbose = args.verbose
    mailaddr = args.email
    mail_rcptTo = mailaddr
    server = args.server
    if server == None:
        server = DNSQuery(mailaddr)
    smtpsend(server, port, mail_rcptTo)
```

**RECRUITMENT**

**招聘启事**

**安恒雷神众测 SRC 运营（实习生）**  
————————  
【职责描述】  
1.  负责 SRC 的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2.  负责白帽子提交漏洞的漏洞审核、Rank 评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

**设计师（实习生）**  

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；

3、精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
4、有品牌传播、产品设计或新媒体视觉工作经历；  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦 19 楼  
学历要求：本科及以上  
工作年限：1 年及以上，条件优秀者可放宽

简历投递至 

bountyteam@dbappsecurity.com.cn

安全招聘  

————————  
公司：安恒信息  
岗位：**Web 安全 安全研究员**  
部门：战略支援部  
薪资：13-30K  
工作年限：1 年 +  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
【岗位职责】  
1. 定期面向部门、全公司技术分享;  
2. 前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3. 负责完成部门渗透测试、红蓝对抗业务;  
4. 负责自动化平台建设  
5. 负责针对常见 WAF 产品规则进行测试并落地 bypass 方案  
【岗位要求】  
1. 至少 1 年安全领域工作经验；  
2. 熟悉 HTTP 协议相关技术  
3. 拥有大型产品、CMS、厂商漏洞挖掘案例；  
4. 熟练掌握 php、java、asp.net 代码审计基础（一种或多种）  
5. 精通 Web Fuzz 模糊测试漏洞挖掘技术  
6. 精通 OWASP TOP 10 安全漏洞原理并熟悉漏洞利用方法  
7. 有过独立分析漏洞的经验，熟悉各种 Web 调试技巧  
8. 熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
【加分项】  
1. 具备良好的英语文档阅读能力；  
2. 曾参加过技术沙龙担任嘉宾进行技术分享；  
3. 具有 CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP 等安全相关资质者；  
4. 具有大型 SRC 漏洞提交经验、获得年度表彰、大型 CTF 夺得名次者；  
5. 开发过安全相关的开源项目；  
6. 具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7. 个人技术博客；  
8. 在优质社区投稿过文章；

岗位：**安全红队武器自动化工程师**  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 熟练使用 Python、java、c/c++ 等至少一门语言作为主要开发语言；  
2. 熟练使用 Django、flask 等常用 web 开发框架、以及熟练使用 mysql、mongoDB、redis 等数据存储方案；  
3: 熟悉域安全以及内网横向渗透、常见 web 等漏洞原理；  
4. 对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5. 具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。

简历投递至

bountyteam@dbappsecurity.com.cn

岗位：**红队武器化 Golang 开发工程师**  

薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 掌握 C/C++/Java/Go/Python/JavaScript 等至少一门语言作为主要开发语言；  
2. 熟练使用 Gin、Beego、Echo 等常用 web 开发框架、熟悉 MySQL、Redis、MongoDB 等主流数据库结构的设计, 有独立部署调优经验；  
3. 了解 docker，能进行简单的项目部署；  
3. 熟悉常见 web 漏洞原理，并能写出对应的利用工具；  
4. 熟悉 TCP/IP 协议的基本运作原理；  
5. 对安全技术与开发技术有浓厚的兴趣及热情，有主观研究和学习的动力，具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式、消息队列等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。  
简历投递至

bountyteam@dbappsecurity.com.cn

END

![图片](https://mmbiz.qpic.cn/mmbiz_gif/CtGxzWjGs5uX46SOybVAyYzY0p5icTsasu9JSeiaic9ambRjmGVWuvxFbhbhPCQ34sRDicJwibicBqDzJQx8GIM3AQXQ/640?wx_fmt=gif)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JWOzTqH7mvbF7crSm0xYteSsKx0ZEHM9VtnsDnaCSLfUILrdkXfH62L0tB9wrbzsGxHITbaa3so7A/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/0BNKhibhMh8eiasiaBAEsmWfxYRZOZdgDBevusQUZzjTCG5QB8B4wgy8TSMiapKsHymVU4PnYYPrSgtQLwArW5QMUA/640?wx_fmt=gif)

**长按识别二维码关注我们**