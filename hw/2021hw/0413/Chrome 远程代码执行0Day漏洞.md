# Chrome 远程代码执行0Day漏洞
漏洞简述
----

攻击者利用此漏洞，可以构造一个恶意的web页面，当用户访问该页面时，会造成远程代码执行。  
目前该漏洞已在最新版本Chrome上得到验证

影响版本
----

Google Chrome: ≤89.0.4389.114 && Windows系统 && 关闭安全沙箱（--no-sandbox）

![](Chrome%20%E8%BF%9C%E7%A8%8B%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C0Day%E6%BC%8F%E6%B4%9E/image.png)

[https://github.com/r4j0x00/exploits/tree/master/chrome-0day](https://github.com/r4j0x00/exploits/tree/master/chrome-0day)