> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qKWux5NoGrSvRLauPoMilQ)

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV2NarG7nEcGSGiatQ8bLQLNSXvKOoM4Jr6iawlsIRwckvQ4LicNFvABAhl5ca6acA4CiaBjzWXO66n0xg/640?wx_fmt=png)

Nginxpwner 是一个简单的工具，可以查找常见的 Nginx 错误配置和漏洞。    

**安装：**

```
cd /opt
git clone https://github.com/stark0de/nginxpwner
cd nginxpwner
chmod +x install.sh
./install.sh
```

**用法：**

```
Target tab in Burp, select host, right click, copy all URLs in this host, copy to a file

cat urllist | unfurl paths | cut -d"/" -f2-3 | sort -u > /tmp/pathlist 

Or get the list of paths you already discovered in the application in some other way. Note: the paths should not start with /

Finally:

python3 nginxpwner.py https://example.com /tmp/pathlist
```

**用途：**

        - 获取 Ngnix 版本并使用 searchsploit 获取其可能的利用，并告知其是否已过时

        - 通过 gobuster 抛出一个特定于 Nginx 的单词表

        - 通过在重定向中使用 $ uri 的常见错误配置，检查它是否容易受到 CRLF 攻击

        - 在所有提供的路径中检查 CRLF

        - 检查是否可以从外部使用 PURGE HTTP 方法

        - 检查变量泄漏配置错误

        - 通过设置为 off 的 merge_slashes 检查路径遍历 漏洞

        - 测试使用逐跳标头时请求长度的差异（例如：X-Forwarded-Host）

        - 使用 Kyubi 通过错误配置的别名测试路径遍历漏洞

        - 使用 X-Accel-Redirect 测试 401/403 旁路

        - 显示有效载荷以检查原始后端读取响应是否配置错误

        - 检查网站是否使用 PHP，并建议针对 PHP 网站的一些 Nginx 特定测试

        - 测试 Nginx 的范围过滤器模块中的常见整数溢出漏洞（CVE-2017-7529）