> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [blog.csdn.net](https://blog.csdn.net/qq_17831715/article/details/112754572)

前言
==

大家好，我是**陌溪**

昨天陌溪在**蘑菇博客交流群**和群里的小伙伴进行了一场**比较激烈的讨论**，主要是关于 **Nacos** 中一个**绕过安全认证**直接获取**微服务**项目的配置文件的 **安全漏洞**。

![](https://img-blog.csdnimg.cn/img_convert/7006dcffb2d3de105c6d6fdc11fe3bf0.png)

截止到昨天为止，该 **issue** 已经有 **50** 条评论。下面是该 **issue** 的地址，感兴趣的小伙伴可以跳转进行查看。

> [https://github.com/alibaba/nacos/issues/4593](https://github.com/alibaba/nacos/issues/4593)

漏洞起源
----

可能有些小伙伴还不太清楚 **Nacos** 是啥，它是 **SpringCloud** **Alibaba** 微服务架构中的一个组件，主要作用是**服务注册和发现**以及**分布式配置管理**。 也就是说我们的配置都可以在 **Nacos** 中存储，里面记录着 **MySQL**、**Redis** 等数据库的**账号**和**密码**，如果用户能够进入到 **Nacos** 中，也相当于我们的**数据**已经能够被脱库了。

因为 **Nacos** 官方仓库对该 **issue** 做了**脱敏**处理，**issue** 提主的描述也已经被删除了，但是从 **issue** 的回答中，陌溪能还原这个**安全漏洞**的一些描述。

> 用户发现通过设置请求头：User-Agent: Nacos-Server，就可以绕过 Nacos 的权限校验，而直接获取到项目的所有配置文件信息，然后题主建议 Nacos 官方立即对这个问题进行修复。

然后 **Nacos** 项目的开发者认为，这不是一个 **安全漏洞**，并且认为通过设置 **User-Agent** 就相当于开启了白名单，那么就可以忽略鉴权。

![](https://img-blog.csdnimg.cn/img_convert/b5cb063b3cada72eafa95cb8d34b37d1.png)

开发人员的答复马上就获得了 **300** 多人的反对意见。认为开发者将 **Nacos** 默认密码和本次**安全漏洞**说成是一个问题。

![](https://img-blog.csdnimg.cn/img_convert/bcd5ded734b21359f1dcf5bac4cea065.png)

我觉得上面这个回复非常中肯，就拿**陌溪**来说，当我部署完 **Nacos** 后，我首先第一件事就是修改 **Nacos** 默认的账号和密码，然后换成一个更加安全的。但是对于**忽略鉴权**这个机制，我并不知情的，所以其它用户也可以通过非法的**后门**来获取到我的配置。

漏洞复现
----

在我看完这个 **issue** 的时候，**陌溪**和**群里小伙伴**想着就拿线上部署的**蘑菇博客**来进行测试。首先我先介绍一下，**蘑菇博客**使用的 **Nacos** 版本是 **1.4.0**，也是前段时间，刚刚发布的最新的一个版本。

首先通过 **Chrome** 浏览器的 **F12** 观察 **nacos** 请求的 **Network**，找到了下面这条 **Nacos 配置文件**请求接口

```
# 开启鉴权
nacos.core.auth.enabled=true
# 关闭白名单功能
nacos.core.auth.enable.userAgentAuthWhite=false.
# 配置键值对 [键值对可以自定义]
nacos.core.auth.server.identity.key=aaa
nacos.core.auth.server.identity.value=bbb
```

然后打开 **Postman**，填写这个 **URL**，并设置 **GET** 请求，同时设置 **Headers** 请求头，加入 **User-Agent:Nacos-Server**，如下图所示

![](https://img-blog.csdnimg.cn/img_convert/c22048e613757d4eca9d377639b5d9a5.png)

从上面的请求 **URL** 中可以看出，陌溪没有设置任何 **Token** 相关的操作，只填写了一个固定的请求头，然后发送请求一个 **HTTP** 请求。

嗯... 果然不出我所料，我的 **Nacos** 配置**直接就获取到**了！！！

![](https://img-blog.csdnimg.cn/img_convert/22995aa6aedbc79c768c1b7f159081ca.png)

其中里面包含了 **MySQL** 的账号密码，**Redis** 的账号密码。而且因为之前**陌溪**为了方便，并没有对配置文件的用户和密码进行**加密处理**，所以直接显示的就是**明文**。同时因为经常为了远程调试方便，所以顺便开放了 **MySQL** 的 **3306** 端口，下面我通过找到的 **IP 地址** 和 **MySQL** 的账号密码，使用 **SQLyog** 工具，直接入侵了我的后台数据库

![](https://img-blog.csdnimg.cn/img_convert/712c91cbfc70eda999a667420523b4b2.png)

陌溪只需要执行 **SQL** 导出，就可以轻松将**蘑菇博客数据**进行**脱库**，同时我在 **issue** 中，也看到有小伙伴通过**端口扫描工具**，一共搜出来 **800** 多台暴露了公网的 **Nacos** 服务器，所以这些服务器无一例外，都有可能被**脱库**！！

![](https://img-blog.csdnimg.cn/img_convert/29b2d6fe8c485b25f0f9dc0da4bc6c00.png)

上次蘑菇博客删库事件：[大型生产事故, 开源项目蘑菇博客差点被删库](https://mp.weixin.qq.com/s/UprMwItKjJ-Bcj1Z5ija1g) 还历历在目，因为陌溪设置 **MySQL** 的密码而引起的，而这次很显然是 **Nacos** 出现的安全漏洞而造成的。

最后**陌溪**提醒一下，想**利用该漏洞搞事情**的小伙伴，我**劝你善良**。

![](https://img-blog.csdnimg.cn/img_convert/2561eb6e0e0d544ba915d6abec046c79.png)

解决方法
----

后面社区小伙伴们，踊跃的提出了自己的修改意见，最后决定通过增加自定义 **Key Value** 键值对对来解决，只有通过设置**正确的键值**对才能**获取配置**。

![](https://img-blog.csdnimg.cn/img_convert/0efa20f7dc63f3cbb0e4d86caf3328cf.png)

在今天 **Nacos** 开发人员已经重视了这个高危安全漏洞，并且紧急的发布了最新的 **1.4.1** 版本。

![](https://img-blog.csdnimg.cn/img_convert/d30fd6ff635292d30b8314b8f2850354.png)

我们只需要下载最新版本的 **Nacos 1.4.1** ，然后修改对应的 **application.properties** 文件，修改如下内容

```
# 开启鉴权
nacos.core.auth.enabled=true
# 关闭白名单功能
nacos.core.auth.enable.userAgentAuthWhite=false.
# 配置键值对 [键值对可以自定义]
nacos.core.auth.server.identity.key=aaa
nacos.core.auth.server.identity.value=bbb
```

最后我们再次使用刚刚的请求进行测试，发现已经无法获取到配置了

![](https://img-blog.csdnimg.cn/img_convert/ce611e4c9bc7bc86d703f5a3b66ee6ea.png)

那么我们需要怎么才能获取到配置呢？只需要在 **headers** 里面，填写刚刚配置文件中的**键值对**即可

![](https://img-blog.csdnimg.cn/img_convert/e17bc126875badbb266f187cff3b1c87.png)

因为**键值对**是我们自定义的，因此每个人的都是不相同的。到这里 **Nacos** 的**安全漏洞**已经算是解决了，最后**陌溪**希望看到本篇文章的小伙伴，如果公司还没有升级最新版的 **Nacos**，那么强烈建议进行升级！

结语
--

**陌溪**是一个从三本院校一路摸滚翻爬上来的互联网大厂程序员。独立做过几个开源项目，其中**蘑菇博客**在码云上有 **2K Star** 。目前就职于**字节跳动的 Data 广告部门**，是字节跳动全线产品的商业变现研发团队。本公众号将会持续性的输出很多原创小知识以及学习资源。如果你觉得本文对你有所帮助，欢迎各位小伙伴关注陌溪，让我们一起成长~

![](https://img-blog.csdnimg.cn/img_convert/bc6fe39b90741cbc97d334fb31082548.png)