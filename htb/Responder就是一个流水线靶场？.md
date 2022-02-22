> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/TzB04FfHVBVU6u5sKUQV3A)

![图片](https://mmbiz.qpic.cn/mmbiz_png/IBqeMoOWia87cQywVmLjK6AAibszyRe4IjVprUicyMBlshIC8KWa8V2akj65cGSn0nPwicTERSF8F1GWhYGuyhptkQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**特别声明:**

点此亲启

**致各位**

· 本公众号发布的靶场、文章项目中涉及的任何脚本工具，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断；

· 本文章、项目内靶场所有资源文件，禁止任何公众号、自媒体进行任何形式的擅自转载、发布

· PTEHUB 对任何脚本及工具问题概不负责，包括不限于由任何脚本错误导致的任何损失或损害及任何法律责任；

· 间接使用靶场、文章中的任何工具及技术，包括但不限于建立VPS或在某些行为违反国家/地区法律或相关法规的情况下进行传播, PTEHUB 对于由此引起的任何隐私泄漏或其他法律问题后果概不负责；

· 如果任何单位或个人认为该项目或文章的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关内容；

· 以任何方式查看或使用此项目的人或直接或间接使用项目的任何脚本的使用者都应仔细阅读此声明；

· PTEHUB 保留随时更改或补充此免责声明的权利；

·一旦使用访问 PTEHUB 项目，则视为您已接受此免责声明。

您在本声明未发出之时，使用或者访问了 PTEHUB ，则视为已接受此声明，请仔细阅读。  

此致

  

  

  

![图片](https://mmbiz.qpic.cn/mmbiz_svg/6t0VDe9bl5c19UhCoAqSJsbGVFE2AGkehUSwIJ80rLG7sicu1ibhEU9qTmG3WlBXLhTia05DLPKcq5lCaqWqXX5LXAdtVAQocxw/640?wx_fmt=svg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/IBqeMoOWia87diauw7JFeflsqdArF4ZcMrTZIBIWkICERBt50hUJn0NShfWNj6bmuxr75XdcOic0498gbteJ99gfg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

  

好久没有给大家更新hackmyvm系列了所以今天为大家带来一个Responder中等难度的靶场，话不多说，直接上手。

  

1

**探测靶机**

最开始肯定需要对ip进行探测。

采用nmap进行扫描，这里用到了-sS的参数，也就是SYN扫描，又被称为半开放扫描，主要特点就是执行快效率高。

扫描发现开放了80端口

![图片](https://mmbiz.qpic.cn/mmbiz_png/IBqeMoOWia87cQywVmLjK6AAibszyRe4IjFApxpgKfku0wyVszAyWu4rXBIiaxoibNYxQHuicadoia18ltz5wtMG4CJg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

打开后发现只有一段话，再无其他。

![图片](https://mmbiz.qpic.cn/mmbiz_png/IBqeMoOWia87cQywVmLjK6AAibszyRe4IjV8cIx5ia9OAMqGB0lgLw9cl7icLwKbvrO2JbMUVtbgsG9rMhETdryOLw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

2  

  

**Shell**

老规矩，爆破目录。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现一个有意思的文件，通过文件名得知是一个文件管理器，但访问就会跳转回首页，因该是没有正确参数的原因，继续爆破参数。

这里利用到一个fs的参数，因为扫描特性原因状态码都是302所以我们要利用fc这个参数屏蔽掉响应大小为0的参数，正确的参数的响应大小是不会为0的

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

知道了参数我们利用burp进行发包查看。

并且列出了系统现有的用户。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

既然这样的话就可以尝试是不是能直接利用伪协议。  

竟然成功的输出了phpinfo。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现其allow_url_include是开着的。  

那么直接利用伪协议写入WEBSHELL就可以了。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

利用哥斯拉直接连接WEBSHELL。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

权限为WWW-DATA

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

3  
  

3  
  

  

**权限提升  
**

做信息搜集发现网站目录下的filemanager.php内存在一个ssh私钥。

保存下来并进行破解

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

反弹一个shell回来。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

  

没发现有什么特殊权限，也没找到其他办法提权，这时想到了最近刚爆出exp的CVE-2021-4034。  

本地提前准备好了一个CVE-2021-4034的exp利用wget下载并运行。  

拿到了root的权限。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

4  
  

3  
  

  

**总结**

**思路：**

这个靶场主要是看大家对于伪协议的了解及掌握程度和对最新漏洞的关注程度，利用伪协议写入WEBSHELL利用最新的漏洞进行提权即可。

  

---

**工具：**

FFUF:模糊测试工具;

Godzilla:WEBSHELL管理工具

5

  

**福利**

**关注公众号获取以下福利**

**1.回复关键词** **密钥** **获取登录账户**

**2.回复关键词** **靶场** 获取所有在线靶场IP

**3.回复关键词** **Vul-2022-008** **获取该靶场访问IP**  

  

回家不迷路方法(防广告拉人头)

1.扫码添加机器人；

2.发送 PTEHub 验证消息；(必须是 PTEHub )

3.机器人自动通过好友后发送 我要加群

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**扫码加入PTEHub靶场3群****。没有了，太多营销僵尸，删的我心累。加机器人进群吧。**  

  

  

  

  

由宝鸡恩酷电子网络科技有限公司(零遁)提供网络技术支撑

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

* * *

**本期制作**

作者：0x3135

编辑：Shawn_bot、邹一、0x3135

审核：墨鱼

       点击下方名片关注我们～

 ![](http://mmbiz.qpic.cn/mmbiz_png/IBqeMoOWia86Ah75BNfkufWicVVia95bA1HwqO042MK4PTqIUXm79OH4nibIL1FnZg9NXTiaBHxrvxskJY2AIlKxLLA/0?wx_fmt=png) ** PTEHub ** PTE小技巧 13篇原创内容   公众号