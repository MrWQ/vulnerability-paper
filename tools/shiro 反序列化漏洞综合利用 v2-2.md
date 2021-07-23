> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qhIAxsFOklH_JXcA4s-Xgw)

免责声明
====

该项目仅供合法的渗透测试以及爱好者参考学习，请各位遵守《中华人民共和国网络安全法》以及相应地方的法律，禁止使用该项目进行违法操作，否则自行承担相关责任！

shiro 反序列化漏洞综合利用 v2.2
=====================

填坑, 修 bug。基于 javafx, 利用 shiro 反序列化漏洞进行回显命令执行以及注入各类内存马

1.  自定义关键字
    
2.  添加代理功能 (设置 -> 代理)
    
3.  检出默认 key (SimplePrincipalCollection) cbc/gcm
    
4.  Tomcat/Springboot 回显命令执行
    
5.  集成 CommonsCollectionsK1/K2/NoCC
    
6.  通过 POST 请求中 defineClass 字节码实现注入内存马
    
7.  resources 目录下 shiro_keys.txt 可扩展 key
    

内存马
---

注入类型：冰蝎, 哥斯拉, 蚁剑 [JSP 自定义返回包格式],neoreGeorg,reGeorg（均为默认配置, 当前最新版本）

1.  提示：注入 Servlet 内存马路径避免访问出错尽量选择静态资源目录。, Filter 无需考虑
    
2.  某些 spring 环境以 jar 包启动写 shell 麻烦
    
3.  渗透中找目录很烦, 经常出现各种写 shell 浪费时间问题
    
4.  无落地文件舒服
    
5.  主要参考哥斯拉以及 As-Exploits 兼容实现
    

TODO
----

1.  解决 serialVersionUID 匹配 cc/cb 多种 jar 包
    
2.  ...
    

![](https://mmbiz.qpic.cn/mmbiz_png/m41BLSafyI7ETrafdM48HHJiaxKBzZRFCaa9reOtPcaIibBHl6T6PfZSzMFshLaaENXB1icZq92iaWYFQ9GBxnwSkw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/m41BLSafyI7ETrafdM48HHJiaxKBzZRFC2ibIokwqIdCiawjK59X95O58MzfiaMpZkZqibnIPRDqfjzKO6ypOlZ7iadw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/m41BLSafyI7ETrafdM48HHJiaxKBzZRFCCg5YzCzWfbDOMbRhiaGsQlEwvl7TAP5YicDVUIOpCljREsTiaH3vq7bTw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/m41BLSafyI7ETrafdM48HHJiaxKBzZRFCZ32aaNKZ7hiaQACamTpu9Ic7hlEbbibDLyZlhlVxibicVibv9r6qW5bo6RQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/m41BLSafyI7ETrafdM48HHJiaxKBzZRFClPcfsd6x7qGGEPOIOzxcCQlRBkkqPbJqKD781LkH3ptcD3UTWk9bVg/640?wx_fmt=png)

**公众号内回复 “****shiro****” 获取工具包下载链接地址**

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

刚入行萌新热爱学习与收藏。感谢各位师傅支持与关注![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

 ****欢迎关注 系统安全运维****   

公众号

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**