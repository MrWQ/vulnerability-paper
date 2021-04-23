# PHP zerodium后门漏洞
![](PHP%20zerodium%E5%90%8E%E9%97%A8%E6%BC%8F%E6%B4%9E/php-source-code.jpg)

漏洞类型
----

任意代码执行

触发条件
----

提交的请求包中，如果字符串以'zerodium'开头，那么该行将从useragent HTTP标头（“ HTTP\_USER\_AGENTT”）中执行PHP代码