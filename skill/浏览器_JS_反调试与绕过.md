> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/cx0ABktkSr3cdxVqRUJdOQ)

一、背景介绍
------

在读《风控要略：互联网业务反欺诈之路》的时候，设备指纹章节中提到了可以通过检测控制台是否开启作为 WEB 作弊环境的检测方案之一。

可见：[](https://mp.weixin.qq.com/s?__biz=Mzg4ODU4ODYzOQ==&mid=2247483776&idx=6&sn=0880227b67c861bb26fa50aa6d8ab890&scene=21#wechat_redirect)[第四章 设备指纹](http://mp.weixin.qq.com/s?__biz=Mzg4ODU4ODYzOQ==&mid=2247483776&idx=6&sn=0880227b67c861bb26fa50aa6d8ab890&chksm=cff991b0f88e18a60886a1f617e3b8a4b71f0fee50d683e38a31565c263bc362302dc14cb100&scene=21#wechat_redirect)

又想到之前在真实环境中遇到过，所以学习一下。

二、反调试
-----

有时候我们在测试一个站点的时候，刚打开 F12，就发现暂停了，如下图所示，便可以判断目标页面做了 JS 反调试处理

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm71tDETpPRQnjzb78ibtIYaDk82LFhDnlDaaGTna6cK2xkKyZKSUNTGYQ/640?wx_fmt=png)

做 JS 反调试通常是通过检测控制台是否开启，当检测到控制台开启了，则进入反调试逻辑  

检测控制台是否开启的一些方案：

1、监听按键

如用户按 F12、Ctrl+Shift+i 的时候

2、窗口尺寸变化

利用打开控制台后 HTML 窗口的尺寸变化作为判断标准，如下是一个采用此方案作为检测依据的项目

https://github.com/sindresorhus/devtools-detect

3、debugger 命令的执行时间

打开开发者工具后，在遇到 debugger 时，会进入暂停，在 debugger 之前记录时间 start，debugger 之后记录时间 end，通过判断 end 与 start 的时间差来判断用户是否开启控制台。

尝试写一个简单的反调试代码，用浏览器访问的时候正常显示，打开开发者工具后则会暂停

```
<!DOCTYPE html>
<html>
<head>
   <meta charset="utf-8">
   <title>Debugger</title>
</head>
<body>
   <h2>Hello Debugger</h2>
   <script type="module">
       setInterval(function() {
           debugger
      }, 1000);
   </script>
</body>
</html>
```

三、绕过反调试
-------

我的 Chrome 是英文显示，Firefox 是中文显示  

### 1. 停用断点功能

停用断点功能，简单粗暴，缺点是你自己也无法使用断点。

Chrome - Sources - Deactivate breakpoints （Ctrl + F8）

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm7Pt8uVplVpw0QIxNOeNicq6GEbSGOgMAhWJekbAtJeBkjMfWzNRTzv2Q/640?wx_fmt=png)

FireFox - 调试器 - 停用断点  

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm75uf5jVic5vt36Md3QPlYHyBDgSh2cUxpOI4T4FBZs4NibWOMnzcZO2gQ/640?wx_fmt=png)

### 2. 设置断点条件  

为断点设置条件，当设置的条件表达式为真时，调试器才会暂停。当设置为`false`时，则永远不会暂停。

Chrome - 右键 - `Add Contitional Breakpoint`

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm7hoYM4S4B7lD7yrR7xBInWkxrqKK6AzHI5fIWDu0k1XeMzbM2iaVdrZg/640?wx_fmt=png)

设置为`false`  

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm7ViadLhqAuILCzCJ9mh0Ria0vqVv4ssnhHJtRGKDA1MdAxoW3GUYWRI5A/640?wx_fmt=png)

Firefox - 右键 - 添加条件  

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm76X2y6QNz85SnA7MZicPkiaiaj9N6yF2aQ6lREgNibDib7ExjDmKTfibwbicsw/640?wx_fmt=png)

### 3. 不在此处暂停  

类似白名单，在指定的位置不暂停。

Chrome - 右键 - Never Pause Here

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm7DZ6sbxpPiajDEYnKqzMDT5xy6ZU1cOwUBO3ic1g2rib5LoXlMYDUk5hyQ/640?wx_fmt=png)

Firefox - 右键 - 永不在此处暂停  

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm7YP93UQd0skqbSZUt5oynk0pmgiad4oTxLQsblgCNJtnDyLicC0Ok0icBw/640?wx_fmt=png)

### 4. 响应包替换关键字  

可以直接替换响应包中的 debugger 关键字

BurpSuite - Proxy - Options - Match and Replace 将`debugger`关键字设置为`console.log('debugger')`

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm7X7NbXFfeAsic2KRHmmMYbO3nLCl3BNHHYj8HiaPkz7T0zUzKwbqUAzkA/640?wx_fmt=png)

这个时候我们再打开开发者工具时，便可以看到没有进入暂停页面  

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm7ibjJMWZfR6Ph5ibUeTya0KNjb7eBX7rNpbMADceYABtAej0X8aIvMUhQ/640?wx_fmt=png)

四、案例分析  

---------

在 fofa 中搜索 body 里面有 bebugger 关键字的 WEB 站点，选一个 http://www.fyw0.cn/

反调试逻辑

1、每 1ms 执行一次检测

2、在开启开发者工具的时候进入调试

2、通过 debugger 语句执行的时间是否小于 50ms，判断是否重载页面

![](https://mmbiz.qpic.cn/mmbiz_png/L91dibvwuia4PlPQfZc1eXPXoSzvnpAWm7ic0wHFYqI7lUAUsele0tCK71hk1CVo3fRBrSvuic9cBdBVfy6bZQEH0Q/640?wx_fmt=png)

这里的逻辑比较简单且只有一个 debugger，所以通过**设置断点条件**或**不在此处暂停**绕过反调试非常快捷。  

五、相关文档
------

https://stackoverflow.com/questions/7798748/find-out-whether-chrome-console-is-open