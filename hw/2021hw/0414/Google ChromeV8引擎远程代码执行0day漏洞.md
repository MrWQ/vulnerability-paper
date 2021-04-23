# Google ChromeV8引擎远程代码执行0day漏洞
漏洞描述
----

Google ChromeV8引擎远程代码执行0day漏洞，该漏洞影响Chrome最新正式版（89.0.4389.128）以及基于Chromium内核的Microsoft Edge正式版（89.0.774.76）。攻击者可通过构造特制web页面并诱导受害者访问来利用此漏洞获得远程代码执行。

影响范围
----

Google Chrome <= 89.0.4389.128

基于Chromium内核的Microsoft Edge <= 89.0.774.76

其他基于V8引擎的浏览器

测试截图
----

![图片](Google%20ChromeV8%E5%BC%95%E6%93%8E%E8%BF%9C%E7%A8%8B%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C0day%E6%BC%8F%E6%B4%9E/640.png)

![图片](Google%20ChromeV8%E5%BC%95%E6%93%8E%E8%BF%9C%E7%A8%8B%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C0day%E6%BC%8F%E6%B4%9E/1_640.png)

处置建议
----

鉴于该漏洞目前处于0Day漏洞状态，无相应的漏洞补丁，用户采取如下临时解决方案以避免受漏洞所导致风险影响：

1\. 慎重打开来源不明的文件或网页链接。

2\. 暂时停止使用V8相关引擎的浏览器，如Chrome、基于Chromium内核的Microsoft Edge，换Firefox等浏览器。

来源
--

[https://github.com/avboy1337/1195777-chrome0day](https://github.com/avboy1337/1195777-chrome0day)

[https://twitter.com/frust93717815/status/1382301769577861123](https://twitter.com/frust93717815/status/1382301769577861123)