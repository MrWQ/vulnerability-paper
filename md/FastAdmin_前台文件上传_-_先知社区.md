> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9395)

### 漏洞通告

FastAdmin 是一款基于 ThinkPHP 和 Bootstrap 的极速后台开发框架。

2021 年 3 月 28 日，360 漏洞云漏洞研究员发现，FastAdmin 框架存在有条件 RCE 漏洞，当攻击者具有一定用户权限的前提下，可以实现任意文件上传，导致 RCE。`--360漏洞云`

漏洞危害范围：< V1.2.0.20210401_beta

### 漏洞分析

由于 FastAdmin 的前台文件上传功能中提供了分片传输功能, 但在合并分片文件时因对文件路径的拼接处理不当导致可上传任意文件。

限制条件：

*   具有上传权限的账户
*   开启分片传输功能（默认关闭）

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212648-137f4432-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212648-137f4432-93b7-1.jpg)

漏洞文件位于：**application/api/controller/Common.php**

在上传文件时如果 POST 传递 `chunkid`参数即可进行分片文件传输, 其会调用 `Upload#chunk`方法, 参数均可控。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212648-13ffe952-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212648-13ffe952-93b7-1.jpg)

一起梳理一下`chunk`方法, 代码不多, 一行一行作解释。首先判断 `Content-Type`不为 `application/obtet-stream`则抛出 `UploadException`异常。接着会拼接分片文件存储路径为 `runtime/chunks`。文件名为 `$chunkid` + `-` + `$chunkindex` + `.part`。即当我们传递 `$chunkid`为 `hhh.php`, `$chunkindex`为 0, 则拼接出的分片文件名为 `hhh.php-0.part`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212649-149ffaf0-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212649-149ffaf0-93b7-1.jpg)

上传测试：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212650-15175938-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212650-15175938-93b7-1.jpg)

分片文件路径：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212651-15465abc-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212651-15465abc-93b7-1.jpg)

回到 `upload`方法, 当 `$action`为 `merge`时会调用 `Upload#merge`方法合并分片文件, 首先其将分片文件路径和 `$chunkid`拼接, 然后合并所有分片文件。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212652-1603767e-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212652-1603767e-93b7-1.jpg)

调用 `merge`方法合并分片文件：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212653-167bba80-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212653-167bba80-93b7-1.jpg)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212655-17acc156-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212655-17acc156-93b7-1.jpg)

漏洞利用脚本：[FastAdmin_Upload](https://github.com/exp1orer/FastAdmin_Upload)  
[![](https://tva1.sinaimg.cn/large/008eGmZEgy1gp5wksxuiaj311w09kamn.jpg)](https://tva1.sinaimg.cn/large/008eGmZEgy1gp5wksxuiaj311w09kamn.jpg)

### 修复方法

1.  关闭分片传输功能
2.  对 chunkid 做正则判断

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402212655-183cffa0-93b7-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402212655-183cffa0-93b7-1.jpg)

### 参考

[FastAdmin 最新 RCE 漏洞复现](https://mp.weixin.qq.com/s?src=11&timestamp=1617350437&ver=2983&signature=vuQa8YI3lz9mwVSyy1h4ZqfGTCcL5BObXgdeCApxNkKnsBm3bNJyW-xngUE0SG2uXndiwBi7tTVjurl4D01MH3Ci9jDUT*39lYQy5HYNWoqtu-BopcC5Zz2IKjWZZyna&new=1)