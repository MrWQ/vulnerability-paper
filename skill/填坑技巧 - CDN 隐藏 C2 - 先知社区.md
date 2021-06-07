> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9616)

> 先知社区，先知安全技术社区

cs 的基础用法、修改端口、密码的教程网上很多，此处不再赘述。

但在搭建域名 + CDN 隐藏版 c2 时楼主遇到了不少的坑，在这里顺着搭建的思路慢慢把踩的坑填上。
--------------------------------------------------

*   1.CS 证书特征配置  
    Cobalt Strike 是一款美国 Red Team 开发的渗透测试神器，常被业界人称为 CS。  
    1.1 去除证书特征：基于 keytool 生成自签证书  
    用 JDK 自带的 keytool 证书工具即可生成新证书：
    
    ```
    keytool命令:
    -certreq            生成证书请求
    -changealias        更改条目的别名
    -delete             删除条目
    -exportcert         导出证书
    -genkeypair         生成密钥对
    -genseckey          生成密钥
    -gencert            根据证书请求生成证书
    -importcert         导入证书或证书链
    -importpass         导入口令
    -importkeystore     从其他密钥库导入一个或所有条目
    -keypasswd          更改条目的密钥口令
    -list               列出密钥库中的条目
    -printcert          打印证书内容
    -printcertreq       打印证书请求的内容
    -printcrl           打印 CRL 文件的内容
    -storepasswd        更改密钥库的存储口令
    ```
    

例如：  
国内 baidu

```
keytool -keystore cobaltStrike.store -storepass 123456 -keypass 123456 -genkey -keyalg RSA -alias baidu.com -dname "CN=ZhongGuo, OU=CC, O=CCSEC, L=BeiJing, ST=ChaoYang, C=CN"
```

国外 gmail：

```
keytool -keystore cobaltstrike.store -storepass 123456 -keypass 123456 -genkey -keyalg RSA -alias gmail.com -dname "CN=gmail.com, OU=Google Mail, O=Google GMail, L=Mountain View, ST=CA, C=US"
```

（Windows 版也可使用 java 安装目录下自带工具 <java_home>\bin\keytool.exe）  
然后使用 keytool 工具可查看生成的证书：</java_home>

```
keytool -list -v -keystore cobaltstrike.store
```

**其中的坑：**

要么生成 cobaltstrike.store 替换默认位置对应文件，要么在 teamserver 启动文件中指定，例如生成 baidu.store，就要修改 teamserver 为：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210526221035-23db51b4-be2c-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210526221035-23db51b4-be2c-1.png)

```
http-stager {
    set uri_x86 "/get32.gif";
    set uri_x64 "/get64.gif";
    client {
            parameter "id" "1234";
            header "Cookie" "SomeValue";
    }
    server {
            header "Content-Type" "image/gif";
            output {
                prepend "GIF89a";
                print;
            }
    }
}
```

**填坑 2：**使用 cloudflare 隐藏 c2 还要设置 profile 中的 head 的 mime-type，具体为：需要在 http-config 将头设置为 header "Content-Type" "application/*; charset=utf-8"，不然可能会出现能上线但是无法回显命令的情况：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210526221934-64fff78e-be2d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210526221934-64fff78e-be2d-1.png)  
**填坑 3：**在 profile 中设置 user-agent 可避免各种被检测，同时也是 https 反向代理的有力识别标志例如将 ua 设置为 Mozilla/5.0 (Windows NT 6.1; Trident/8.0; rv:12.0)：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210526221952-6ffc6460-be2d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210526221952-6ffc6460-be2d-1.png)  
在使用 nginx 反向代理时即可过滤：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210526222004-7740192e-be2d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210526222004-7740192e-be2d-1.png)  
此时如果有多个工具生成 shellcode 上线 ua 不同，可设置多条件过滤，满足多人运动的需求：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210526222023-821fed42-be2d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210526222023-821fed42-be2d-1.png)  
最后在 https-certificate 配置中还要对 https 证书进行声明：

```
https-certificate {
     set keystore “api.xxx.com.store”;
     set password “123456”;
}
```

最后检查配置文件有效性：

```
./c2lint malleable.profile
```

即可在 teamserver 启动时加载 profile：

```
./teamserver 1.1.1.1(你的ip) ******(密码) malleable.profile
```

*   2.3 服务器反向代理限制访问  
    最重要的一个知识点就是使用反向代理限制你的 c2 被别人发现，例如配置：
    
    ```
    location ~*/jquery {
          if ($http_user_agent != "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko") {
          return 302 $REDIRECT_DOMAIN$request_uri;
          }
          proxy_pass          https://127.0.0.1:5553;
    }
    ```
    
    就可以很好地隐藏自己，但这里有一些坑点，楼主是踩了又跳出来;  
    **填坑 1：**在 nginx 配置信息中 location ~*/ 位置，需配置 x-forword 信息，同时在 profile 设置，否则上线的外网 ip 为自己的 vps，或 cdn 地址，无法获取外部信息：  
    nginx.conf 文件：
    
    ```
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    ```
    
    profile 文件：
    
    ```
    http-config {
      set trust_x_forwarded_for "true";
    }
    ```
    
    **填坑 2：**在 nginx 反向代理配置中，启动监听器时 http host 可为域名地址，bind port 可另选一个，作为 proxy_pass 内容：  
    [![](https://xzfile.aliyuncs.com/media/upload/picture/20210526222248-d89d4a48-be2d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210526222248-d89d4a48-be2d-1.png)  
    其中 bind port 可在本机使用防火墙屏蔽，只允许内部访问：
    
    ```
    iptables -I INPUT -p tcp --dport 45559 -j DROP
    iptables -I INPUT -s 127.0.0.1 -p tcp --dport 45559 -j ACCEPT
    ```
    
    但 proxy_pass [http://127.0.0.1:45559; 的地址选择也有门道，reverse](http://127.0.0.1:45559;的地址选择也有门道，reverse) http 类型可填写任意本机真实 ip 信息，如 localhost，127.0.0.1，甚至有外网网卡的直接外网真实 ip 都可以正常上线。

但 reverse https 类型只能填写 127.0.0.1，如使用真实 ip，如 99.199.99.199，proxy_pass [https://99.199.99.199.:45559 的请求 cdn 会一直超时，造成无法上线。](https://99.199.99.199.:45559的请求cdn会一直超时，造成无法上线。)