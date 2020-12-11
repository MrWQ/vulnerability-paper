> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247484751&idx=1&sn=7952d0c731c6da201224f4f0a4c1f24b&chksm=eaad8572ddda0c64dd9e39e209f05ba57518751048569e3aab74611102d7196921883b6a5f1e&scene=21#wechat_redirect)

  

搜索引擎 Fofa 的简单使用

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dELXTTh0prjcXZh1zDyGL9va7TJbhmSBnyiabAAAjbbB1B42spahrfuzcyIY4jPp8FU4Jib61R0ibxw/640?wx_fmt=png)

目

录

Fofa

    逻辑运算符

    查找使用指定应用的 IP

    查找使用指定协议的 IP

    查找开放指定端口的 IP

    查找 IP 或网段的信息

    查找使用指定 css 或 js 的网站

    使用 Fofa API 接口

    其他

  

Fofa

     Fofa 是白帽汇推出的一款网络空间搜索引擎，它通过进行网络空间测绘，能够帮助研究人员或者企业迅速进行网络资产匹配。例如进行漏洞影响范围分析、应用分布统计、应用流行度等。在渗透测试过程中，Fofa 能帮助测试人员快速发现目标资产。

  

逻辑运算符  

●&& ：表示逻辑与

●|| ：表示逻辑或

```
#查找使用coremail并且在中国境内的网站
app="Coremail" &&  country=CN          
#查找title中含有管理后台或者登录后台的网站
title="管理后台" ||  title="登录后台"    
```

  

  

### 查找使用指定应用的 IP

  

```
#查找使用Coremail的网站
app="Coremail"
#查找使用Weblogic的网站
app="BEA-WebLogic-Server"
#查找使用九安视频监控的网站
app="CCTV-Cameras"
```

  

  

查找使用指定协议的 IP

```
#查找使用mysql的ip
protocol=mysql
#查找使用mssql的ip
protocol=mssql
#查找使用oracle的ip
protocol=oracle
#查找使用redis的ip
protocol=redis
```

  

  

查找开放指定端口的 IP

```
#查找开放3389端口的主机
port="3389"
#查找开放了1433,3306,3389端口的主机
ports="1433,3306,3389"
#查找只开放了1433,3306,3389端口的主机
ports=="1433,3306,3389"
```

  

  

查找 IP 或网段的信息

```
#查找指定ip的信息
ip="220.181.38.148"   
#查找指定网段的信息
ip="220.181.38.0/24"  
```

  

  

查找使用指定 css 或 js 的网站

      有时候，我们碰到一个使用框架的网站，现在我们想找到所有使用该框架的网站。可以查看源代码，找到这个框架特有的 css 或 js 文件，然后将该 css 或 js 的路径复制粘贴到 Fofa 进行查找。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dELXTTh0prjcXZh1zDyGL9UhGR4OORNhfsDBEDIeKzvMMZFDlibiapicCPMqicRpbgg1n0Nc7QwibEicaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dELXTTh0prjcXZh1zDyGL9qHFcicAwKbWvPDqtnARXWrxXvOKGoJwAf0GJxmT8AAtlkoAIibg3gKyg/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dELXTTh0prjcXZh1zDyGL9SSEgRJDd57LsNroDjFMhWUXcDPoNv1xADuQzRTX0wtQ3GIDgamYRog/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dELXTTh0prjcXZh1zDyGL9yPzPZBuGNCG0owpPNI7ggygoNCPf49ia0z15Z3naKbsBP3rGzOtibDGg/640?wx_fmt=png)

  

使用 Fofa API 接口

使用 Fofa API 接口需要有 Fofa 的会员。我这里以 Bash 脚本为例

```
echo 'domain="fofa.so"' | base64 - | xargs -I{} curl "https://fofa.so/api/v1/search/all?email=test@qq.com&key=b7573a06ec469619aedbd4dce37f0f&qbase64={}" >  result.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2d5zNOgUy9gHrKpBdAQ9zvLAib1nzFcDyA73Pua4mz0zRucPe7Diak9le7Vs2Wzic2vVZf8NFNzFlGIw/640?wx_fmt=png)

  

  

其他

```
#查找title含有管理后台的ip
title="管理后台"     
#查找响应头含有thinkphp的ip
header="thinkphp"   
#查找响应包含有thinkphp的ip
body="管理后台"      
#查找指定根域的所有子域
domain="baidu.com"  
#查找域名中带有指定词的ip
host="test"         
#查找中国境内的ip，主要结合其他语句一起
country=CN          
#搜索证书(如https证书、imaps证书等)中含有"phpinfo.me"关键词的网站和IP
cert="phpinfo.me"   
```

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvAKOaVnz60hOe7y3wAHiclddyK53lpEKIQlx4DKOq6EojHibVicgibDB2aQ/640?wx_fmt=gif)

来源：谢公子的博客

责编：Shawn

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)