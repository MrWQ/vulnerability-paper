> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yeMhVYJks_wf6Po-sA6iOg)

0x00: 前言
========

       Smarbi 是由思迈特软件开发的一款企业级商业智能和大数据分析平台，满足用户在企业级报表、数据可视化分析、自助分析平台、数据挖掘建模、AI 智能分析等大数据分析需求。致力于打造产品销售、产品整合、产品应用的生态系统，与上下游厂商、专业实施伙伴和销售渠道伙伴共同为最终用户服务，通过 Smartbi 应用商店（BI + 行业应用）为客户提供场景化、行业化数据分析应用。通过官网可知国内大部分银行，央企，部委都部署有该系统。在一次安全评估项目中遇到该平台，在网上找到相关源码后遂对该平台进行分析审计，挖掘出了一些问题。

0x01:SQL 注入
===========

       本来是想找个 RCE 的漏洞。但发现存在 SQL 注入。打开 web.xml 文件。发现一个 FileResource 类。感觉像是一个文件的读写类。我们追踪到 class，然后看下类实现方法，通过浏览代码语法我们可以了解到该系统使用 Servlet 实现 http 的交互。这里简单的阐述一下 Servlet 的概念，方便后续理解。

     大家都知道 Servlet，但是不一定很清楚 servlet 框架，这个框架是由两个 Java 包组成: javax.servlet 和 javax.servlet.http，在 javax.servlet 包中定义了所有的 Servlet 类都必须实现或扩展的的通用接口和类，在 javax.servlet.http 包中定义了采用 HTTP 通信协议的 HttpServlet 类，Servlet 的框架的核心是 javax.servlet.Servlet 接口, 所有的 Servlet 都必须实现这一接口，在 Servlet 接口中定义了 5 个方法, 如图琐事哦，其中前 3 个方法代表了 Servlet 的声明周期:

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6vgJpxFInKCapEsic3Z5YetafncM1oTwMcsqSOuz4VdmzMjiaKWvlla4A/640?wx_fmt=png)

当 Web 容器接收到某个 Servlet 请求时, Servlet 把请求封装成一个 HttpServletRequest 对象, 然后把对象传给 Servlet 的对应的服务方法。HTTP 的请求方式包括 DELETE,GET,OPTIONS,POST,PUT 和 TRACE, 在 HttpServlet 类中分别提供了相应的服务方法, 它们是, doDelete(),doGet(),doOptions(),doPost(), doPut() 和 doTrace().。当我们了解了这些前置知识后。大大的方便了我们理解接下来的代码。

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6NW9ZTYdEnFcfv6xcTiaibc4IImibWaicWicuRlbddyiaGKxv8Jib6fXicYNLew/640?wx_fmt=png)

根据我们前面所了解到的一些前置知识。我们来看 doGet 方法的实现。

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6Qha6jRxib75DrWkwDwGovDBTScjeQM8Nm6QEsyem8ZbrzIWzicbUf0LQ/640?wx_fmt=png)

前面一堆巴拉巴拉我们先不讲。我们直接来看 353-363 行。resID 通过 getParameter 获取。我们可控，然后直接在 363 行就将变量拼接到 SQL 语句里去了。而且直接就 executeQuery 了，前面都用了 prepareStatement 来预防 SQL 注入。为啥这里就直接拼接 SQL 语句了呢。我严重怀疑这是临时工写的代码。很明显这里存在 SQL 注入了。

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6QTAB7AuP0xx78v3FAjL8KHkXtY6lsdVWOLvKsxzuG5wFYNaZFdV7Gg/640?wx_fmt=png)

我们直接构造 payload 注入即可：

 http://www.xxx.com//vision/FileResource?op=OPEN&resId=LOGIN_BG_IMG

由于数据库存在差异。大家直接丢 sqlmap 跑就行了

0x02: 任意文件上传
============

         挖注入不是我的本来目的，任何以渗透测试为目的的代码审计最终的目标都是 RCE 或者任意文件上传。于是我继续寻找涉及文件操作的相关代码。PS: 此处踩了很多坑。通过寻找 web.xml 里的配置信息。我快速定位到了一处上传接口 UploadImageServlet。跟进看看

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6VROCvYmYuzFDRfNUH5yMHaMT8jgUesOMN3UBg1h5yrlAF4dMLqF3kw/640?wx_fmt=png)

        如果 type 不为 download 和 view 则进入 uploadImage。跟进

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6TGI6AB3oysWasGeGicMZ3rcZlZ1GB6ohLLWYaSUaJvwbJo9VE4SnH5g/640?wx_fmt=png)

        看 uploadImage 前面的代码看的我很开心，仿佛好像没有过滤后缀之类的。仿佛任意文件上传就在眼前，代码的执行逻辑我写在注释里了。看到 base64 的操作我很疑惑。正常不应该直接写文件了么。直到我看到 saveImageContent 时，我的心一凉。根据函数名不难理解为保存图片内容。跟进看看。是否为我猜想的直接把文件内容入库了。

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6eMtYEVFjLWjibRVZee4e3bXdNG5yyib03lia23WhVGOeC6ibKzXHJp3N3A/640?wx_fmt=png)

        跟进 saveImageContent，看到 PageDAO 后心彻底凉了。这里可以确定文件入库了，并没有落地到目录。就算没有过滤后缀。也没办法利用。

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6wSRN3s1VSzY6iaDzlpTaMt0YD03YvP7yJK9v1ib3Gk1DibUA87vejbP3Q/640?wx_fmt=png)

        于是乎我就继续找呀找呀。发现这套系统百分之 99 的文件上传都是写到数据库里，着实恶心到我了。这时候我转战寻找 jsp 文件。我寻思独立写的 jsp 文件应该没有这么严谨。山重水复疑无路，柳暗花明又一村。经过耐心的寻找。终于定位到一个 上传文件。  

/vision/designer/imageimport.jsp

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6NTcE6FE34HcFQ82hXtpw7OSWC1SkQsZLd9RnAu1IcNcfYWN9XcXjWQ/640?wx_fmt=png)

      纵观代码逻辑。先定义写入目录。然后判断目录是否存在，如果不存在则创建目录。然后读取 header 里的两个参数，用来作为文件名和文件类型，随后简单的判断一下 type 是否为 image。然后就直接 fos.write 了。文件落地到 / vision/designer/images/。一个比后门还要后门的文件上传写法。要不是我看到同目录其他的一些文件我差点以为这是一个后门了。构造上传也就很简单了。在 header 里面添加两个参数。X-File-Name 为文件名。POST 正文为你要上传的文件内容。请求即可

```
Payload:
POST /vision/designer/imageimport.jsp HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Cookie: UserLogging=false; FQConfigLogined=; FQPassword=; JSESSIONID=AAEDEBC8984E4F540DFAAF8C0F932035
X-File-Type: image
X-File-Name: 1.jsp
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: multipart/form-data; boundary=---------------------------2927288396864
Content-Length: 374

test
```

![](https://mmbiz.qpic.cn/mmbiz_png/Lu7eicMrZheHKhv15ia6TlyEIxUpPkpQj6vyo77BHFwDsHGUblmVGAbge9cFSjwSocT5jtmRzSMl3udFMAwytJSQ/640?wx_fmt=png)

0x03: 结语 
=========

      通过对 smartBI 的代码进行分析。不难看出开发设计人员还是很具备安全意识的，文件上传操作几乎都是直接入库了。大部分请求也通过 RMIServlet 进行处理。且接口请求数据和返回数据都加密处理了。但是百密终有一疏，出现拼接 SQL 注入这种写法着实不应该。这篇文章有很多不足，写的也很浅显。只做抛砖引玉。欢迎各位师傅多多指正。  

PS：此漏洞修复状态未知，谨慎测试。  

=====================