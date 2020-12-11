> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247485130&idx=1&sn=1ce6b4556044caf47d91bc450b1d40d2&chksm=eaad86f7ddda0fe1f42729664a458c4dbc8ce0a371b838bbbe22d2bf3af732b7d361229c3aa3&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtNMnYqdKH2KnKdib2DpvdTGYYTsiaENC4m8jBs389sNnibfOreCmJt44CQ/640?wx_fmt=png)

CobaltStrike 证书修改躲避流量审查

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtRQPUFue4ecb4tvn7zJWo7PKgv7aIibXghxKvYsh21G0eZY8Nv2e3uFg/640?wx_fmt=png)

目录

Keytool

keystore

创建新的 CobaltStrike.store

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtGhDFaqjDTccw1MX8nQSssfgfIicqRlWOraQNsC4J2ficQAJc5VEmJ6GQ/640?wx_fmt=png)

在红蓝对抗中，防守方往往会有很多的设备审计流量。Cobalt Strike 服务端和客户端是通过 SSL 加密通讯的，默认情况下的 SSL 配置文件和代理配置文件导致 keystore 文件内容被用于防火墙识别。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtnUyvnXvArXNQ7DWDzuSibDOMKmHcT8KemcKEqUtQJcJC4sYfic0HiaOQg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtGhDFaqjDTccw1MX8nQSssfgfIicqRlWOraQNsC4J2ficQAJc5VEmJ6GQ/640?wx_fmt=png)

### ✦Keytool

Keytool 是一个 java 数据证书的管理工具，Keytool 将密钥 和 证书 存放在一个称为 keystore 的文件中, 即. store 后缀的文件中。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtTUmng6Pwib6IlP3r8uTOSAAu7bn3Jz0vZNtjd9ANrB5nFvmjuianXllQ/640?wx_fmt=png)

```
查看证书文件：keytool -list -v -keystore xx.store
修改证书密码：keytool -storepasswd -keystore test.store
修改keystore的alias别名：keytool -changealias -keystore test.store -alias source_name -destalias new_name
修改alias（别名）的密码：keytool -keypasswd -keystore test.store -alias source_name
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtGhDFaqjDTccw1MX8nQSssfgfIicqRlWOraQNsC4J2ficQAJc5VEmJ6GQ/640?wx_fmt=png)

### ✦keystore

Keystore 是什么？keystore 是 java 的密钥库，用来进行通信加密，如数字签名。keystore 就是用来保存密钥对的，公钥和私钥。Keystore 可理解为一个数据库，可以存放很多个组数据。

每组数据主要包含以下两种数据:

*   密钥实体 --- 密钥 (secret key) 又或者私钥和配对公钥(采用非对称加密)
    
*   可信任的证书实体 --- 只包含公钥
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtOORP6aR67dvnaMomd0puicRHr9XSbcFibTZTicPcQqdaGmAze2ibBCPqww/640?wx_fmt=png)

查看 CobaltStrike 的默认 store 文件

```
keytool -list -v -keystore cobaltstrike.store
```

可以看出 CobaltStrike 默认的 store 文件中的 Alias name 、Onwer 和 Issuer 的信息，特征都比较明显。

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtL0nuYvaPbES3PeWY1IO8E1qoREHQKWJ5ib6T7eb6D7LF1I3KRhr31Sg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtGhDFaqjDTccw1MX8nQSssfgfIicqRlWOraQNsC4J2ficQAJc5VEmJ6GQ/640?wx_fmt=png)

### ✦创建新的 CobaltStrike.store

而为了掩盖默认 SSL 证书存在的特征，需要重新创建一个新的不一样的证书 。使用以下命令创建证书：

```
keytool -keystore cobaltstrike.store -storepass 密码 -keypass 密码 -genkey -keyalg RSA -alias google.com -dname "CN=(名字与姓氏), OU=(组织单位名称), O=(组织名称), L=(城市或区域名称), ST=(州或省份名称), C=(单位的两字母国家代码)"
```

*   -alias 指定别名
    
*   -storepass pass 和 -keypass pass 指定密钥
    
*   -keyalg 指定算法
    
*   -dname 指定所有者信息
    

删除 CobaltStrike 自带的 cobaltstrike.store，使用以下命令生成一个新的 cobaltstrike.store 即可！然后客户端连接即可。

```
keytool -keystore cobaltstrike.store -storepass 123456 -keypass 123456 -genkey -keyalg RSA -alias baidu.com -dname "CN=(名字与姓氏), OU=(组织单位名称), O=(组织名称), L=(城市或区域名称), ST=(州或省份名称), C=(单位的两字母国家代码)"
 
keytool -importkeystore -srckeystore cobaltstrike.store -destkeystore cobaltstrike.store -deststoretype pkcs12
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtKclSFWcdovSfqtRWqCd0eGeo8q1GhRsXDGKpkPoaW3Ma83nDoejswQ/640?wx_fmt=png)

**注：**我看很多其他文章还需要将 cobaltstrike.store 文件下载至客户端本地，然后保存为`ssl.store` 和 `proxy.store`两个文件。然后，将它们放入 cobaltstrike.jar 中的 resources 目录中。但是实际我在配置过程中，并不需要这些步骤。并且，在 CobaltStrike3.14 版本下，重新生成 cobaltstrike.store 后启动 CobaltStrike 会报错无法正常启动。本次环境在 CobaltStrike4.0 环境下配置成功。

参考文章：http://test666.me/archives/227/

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtGhDFaqjDTccw1MX8nQSssfgfIicqRlWOraQNsC4J2ficQAJc5VEmJ6GQ/640?wx_fmt=png)

责编：Vivian

来源：谢公子博客

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEt3mZ0WohIhKXT7X9ewrSurKzdK64DXn9qxiaspahiafk3K2rfBVibLiaM0w/640?wx_fmt=png)

如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。  
最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtaBibuQG6SUv2EKJaGak7Y5z6LLO5mXiap0PahVdhAopuxReAn3Ffz3Gw/640?wx_fmt=png)