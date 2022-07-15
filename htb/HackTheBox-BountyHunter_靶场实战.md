> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/a4HOCdytZCmELQPDhILcew)<table><tbody><tr><td width="557" valign="top" height="62"><section><strong>声明：</strong>该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。</section><section>请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。</section></td></tr></tbody></table>

感谢群友 @rural 老哥的投稿，感谢分享 ![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeibyfk9D0ibkDtz55LQT8zLHC9SYk7SWIfYia8I7tCnZbEtiaHicHWA0sMmemsicdIic7yDFjPUqPtCPErg/640?wx_fmt=png) 。在这篇文章详细记录了他打 “HackTheBox-BountyHunter” 靶场的整个过程，希望大家能够从中有所收获。![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOc5ZcSNTBqibEmpic3ibyWnkRLx9tqqTaZMhMEFGau1e7POs9LoCZzqlnOSyl2qO8KACkLY9h4ziaDBJQ/640?wx_fmt=png)  

首先用 nmap 扫描靶机开放了那些端口和服务

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ93epKHeVDmZticV3hbppOiamJa2UDANDr9LK4iaHmv4AuMMVsAzZGyufHg/640?wx_fmt=png)

22 就不爆破了，来访问 80 端口试试

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9Iml4sPAnaxD2T5R8Z68WOeSGXnP6uBjKWfwT0ia0uyAb7eKhzoXEI9Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9DdanNuSj9SpRDOictQOJ0oXcicibLELpVbwrNiazD8yQrTCWsFdIBOM7hA/640?wx_fmt=png)

点着点着就来到了一个页面

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9X8nljVxibAtic3sSUrSicoTWgIa0VCWqDSkPicicmlyzkDcw86WSaO0s7Qg/640?wx_fmt=png)

随便试了一下，开始抓包

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9FxS1KibhhyicsnKSy3cGDLMqicsJMAkvD1m2EmaxD9d7JDeUSlMxiazULw/640?wx_fmt=png)

Data 是一串被编码的字符串他是先用的 bases64 加密之后在用 url 编码加密，解出来之后是个 xml 的实体

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9qpWuV7cS0Wiajdiaj6yfsjTycuWgmlTlq5v6SrgxjSBHicXcHcDNYnPibQ/640?wx_fmt=png)

这个就是试试 xml 实体注入了

xml 实体注入，先把代码写出来在加密之后发送给服务器

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9A8kjXrT3j84uALVkHRZ6UhbIKYicLe0tQv5wIg2nZ13vabWr7hYibCkw/640?wx_fmt=png)

*   第 1 行是一个 XML 文档声明，告诉解析器这是一个 XML 文件。
    
*   第 2-4 行是 DTD，调用了一个外部实体，将本机 test.txt 文件的内容赋值给实体 test。此处造成了 XML 实体注入攻击。
    
*   最后一行是输出实体的值
    

在编码之后发送给服务器

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9wwDSk3s20Cg3xQ08U8rpH1jGB7rXpC2ltjmCtiap637mgNTLmcjaiaZg/640?wx_fmt=png)

这样就证明了 xml 实体注入的存在，而且获取到了 passwd 文件知道了服务器的用户名，这里陷入了僵局，不知道咋办了，在看了教程之后明白了要读取 db.php 看名字就和数据库有关

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9oibrDm6M18HQ7gCIcPlgNUcJ1fCUiajVfOPXDnYyUcDADL5ZDt7GAGhw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ94icW8xumx9b16ZdJkqjxPhic0N0XJ3pYRU4uAumfU48u0UAJRBqDvp6w/640?wx_fmt=png)

返回了一串加密字符串我们解密看看

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9wMxEPC3QPyO5KUw5UWSb2KgmVw7LG85S6iaflfEQAHyovlic6SuDUjQQ/640?wx_fmt=png)

是个连接数据库的 php 代码

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

用密码尝试登录 admin 和 test 用户没有成功，我门在 passwd 里面获得了用户名可以用这个密码爆破一波

```
┌──(root💀kali)-[/tools]
└─# cut -d : -f 1 passwd.txt >user
```

得到用户名文本 user，现在用 hydra 爆破用户名

```
┌──(root💀kali)-[/tools]
└─# hydra -L /tools/user -p m19RoAU0hP41A1sTsq6K 10.10.11.100 ssh
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ98mKPFz9qnHwt7Ha1SZ0rpYrHQt4QBqLujhQuCRMdUq3zBoCfrDV0pQ/640?wx_fmt=png)

爆破成功得到用户名密码

```
[22][ssh] host: 10.10.11.100   login: development   password: m19RoAU0hP41A1sTsq6K
```

登录服务器查看权限

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9v4ICLU8exBR0iaUhywVgGFWmxoiboT6cyT9tk9A1Fyf7r3hVMHGbWyDQ/640?wx_fmt=png)

普通用户权限，尝试提权

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9Uw6ho4IwBagthicn8cCf4VpPERwYLBibSwxunyQmXpVR7YGjh1MxuN0A/640?wx_fmt=png)

sudo -l 之后发现它可以无密执行一个 python 文件和 python3.8 的环境，我们打开文件看看是一个 python 脚本

```
#Skytrain Inc Ticket Validation System 0.1
#Do not distribute this file.

def load_file(loc):\\判断文件是否是md后缀
    if loc.endswith(".md"):
        return open(loc, 'r')
    else:
        print("Wrong file type.")
        exit()

def evaluate(ticketFile):
    #Evaluates a ticket to check for ireggularities.
    code_line = None
    for i,x in enumerate(ticketFile.readlines()):
        if i == 0:\\判断文件第一行是否是# Skytrain Inc
            if not x.startswith("# Skytrain Inc"):
                return False
            continue
        if i == 1:\\同上
            if not x.startswith("## Ticket to "):
                return False
            print(f"Destination: {' '.join(x.strip().split(' ')[3:])}")
            continue

        if x.startswith("__Ticket Code:__"):\\判断__Ticket Code:__在第几行
            code_line = i+1
            continue

        if code_line and i == code_line:
            if not x.startswith("**"):\\判断地四行开头是否有**
                return False
            ticketCode = x.replace("**", "").split("+")[0]\\取这一行**和+中间的数字
            if int(ticketCode) % 7 == 4:\\ ticketCode和7取余等于4
                validationNumber = eval(x.replace("**", ""))\\用eval()执行**后面的命令
                print(validationNumber)
                if validationNumber > 100:
                    return True
                else:
                    return False
    return False

def main():
    fileName = input("Please enter the path to the ticket file.\n")
    ticket = load_file(fileName)
    #DEBUG print(ticket)
    result = evaluate(ticket)
    if (result):\\判断result是否为ture
        print("Valid ticket.")
    else:
        print("Invalid ticket.")
    ticket.close

main()
```

这里我对代码进行了注释，方便理解，我们构造一个 asd.md 文件

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9oaNS9en04n4cRkRqEAOJW6CXOWNVYaicW32ggfCOUP3kWSUOrtydtwA/640?wx_fmt=png)

这里使 and 后面的执行等于 falsh 从而给代码返回 1414 是的函数 return 一个 true

我们在 kali 监听并在靶机执行脚本

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9uibpEAHAGKvPz3FMHuxFJQMCOCGbm1ibvzNgtp7YKj20jMexoUgZKvLw/640?wx_fmt=png)

成功返回 root 权限的 shell，之后获取 flag，取得胜利！！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf06pqnvwSsBvz61sfpJTZ9Ue2iaWR7k4RQNCic1rE4pSJPOAqkANJ3cuibO835IddxoyJm2dmiaYspqQ/640?wx_fmt=png)

关注公众号回复 “9527” 可免费获取一套 HTB 靶场文档和视频，“1120” 安全参考等安全杂志 PDF 电子版，“1208” 个人常用高效爆破字典，“0221”2020 年酒仙桥文章打包，还在等什么？赶紧点击下方名片关注学习吧！

公众号

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcAcRDPBsTMEQ0pGhzmYrBp7pvhtHnb0sJiaBzhHIILwpLtxYnPjqKmibA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247487086&idx=1&sn=37fa19dd8ddad930c0d60c84e63f7892&chksm=cfa6aa7df8d1236bb49410e03a1678d69d43014893a597a6690a9a97af6eb06c93e860aa6836&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcIJDWu9lMmvjKulJ1TxiavKVzyum8jfLVjSYI21rq57uueQafg0LSTCA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486961&idx=1&sn=d02db4cfe2bdf3027415c76d17375f50&chksm=cfa6a9e2f8d120f4c9e4d8f1a7cd50a1121253cb28cc3222595e268bd869effcbb09658221ec&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)