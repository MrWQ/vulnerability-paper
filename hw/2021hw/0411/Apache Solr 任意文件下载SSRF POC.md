# Apache Solr 任意文件下载/SSRF POC
Apache Solr是美国阿帕奇（Apache）软件基金会的一款基于Lucene（全文搜索引擎）的搜索服务器。该产品支持层面搜索、垂直搜索、高亮显示搜索结果等。

该漏洞是由于Apache Solr在默认安装时不会开启身份验证，攻击者在未授权情况下访问Config API打开requestDispatcher.requestParsers.enableRemoteStreaming开关，进而通过构造恶意请求，执行SSRF攻击，读取目标服务器的任意文件。

影响范围
----

≤8.8.1

运行环境
----

python3.6 及以上

**运行截图**
--------

![image](Apache%20Solr%20%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BDSSRF%20POC/112407628-661d5d80-8d51-11eb-8edc-59ebf4f31c9a.png)

仅供学习
----