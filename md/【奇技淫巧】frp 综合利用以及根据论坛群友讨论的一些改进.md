\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/tFt-FlX5ziemI0jFB6wqtw)

**![](https://mmbiz.qpic.cn/mmbiz/Wqr9SokRcTWcKgdMIz6KrDJxEeibLFHr3yNgsRElic1xaian4Yp469kv3ZpkfOZeXORYpicEwAVoMqG7Mt7XFO1Jfg/640?wx_fmt=gif)**

frp 是一个强大的穿透代理工具, 基于 go 编写, 所以在并发和网络处理上具有天然优势。  
基本使用在此不再赘述, 大家可以查看 frp 官方文档, 主要挑一些实战重点进行描述。  
1\. 使用 frp 做为 http 代理和 socks5 代理服务器并经行穿透转发。  
frp 通过插件模块支持 http 代理和 socks5 代理；官方文档描述如下:  
客户端插件模式是为了在客户端提供更加丰富的功能，目前内置的插件有 unix\_domain\_socket、http\_proxy、socks5、static\_file。通过 plugin 指定需要使用的插件，插件的配置参数都以 plugin\_ 开头。使用插件后 local\_ip 和 local\_port 不再需要配置。  
使用 http\_proxy 插件的示例:

```
\# frpc.ini
\[http\_proxy\]
type = tcp
remote\_port = 6000
plugin = http\_proxy
plugin\_http\_user = abc
plugin\_http\_passwd = abc
```

2\. 使用 frp 作为一个简单文件服务器；  
对外提供简单的文件访问服务  
通过 static\_file 插件可以对外提供一个简单的基于 HTTP 的文件访问服务。  
启动 frpc，启用 static\_file 插件，配置如下：

```
\# frpc.ini\[common\]server\_addr = x.x.x.xserver\_port = 7000\[test\_static\_file\]type = tcpremote\_port = 6000plugin = static\_file# 要对外暴露的文件目录plugin\_local\_path = /tmp/file# 访问 url 中会被去除的前缀，保留的内容即为要访问的文件路径plugin\_strip\_prefix = staticplugin\_http\_user = abcplugin\_http\_passwd = abc
```

3.frp 进行多次代理;  
通过代理连接 frps  
在只能通过代理访问外网的环境内，frpc 支持通过 HTTP PROXY 和 frps 进行通信。  
可以通过设置 HTTP\_PROXY 系统环境变量或者通过在 frpc 的配置文件中设置 http\_proxy 参数来使用此功能。  
仅在 protocol = tcp 时生效。

```
\# frpc.ini\[common\]server\_addr = x.x.x.xserver\_port = 7000http\_proxy = http://user:pwd@192.168.1.128:8080
```

4\. 通过 tls 和算法加密 frp 流量  
4.1 加密与压缩  
这两个功能默认是不开启的，需要在 frpc.ini 中通过配置来为指定的代理启用加密与压缩的功能，压缩算法使用 snappy：

```
\# frpc.ini\[ssh\]type = tcplocal\_port = 22remote\_port = 6000use\_encryption = trueuse\_compression = true
```

如果公司内网防火墙对外网访问进行了流量识别与屏蔽，例如禁止了 ssh 协议等，通过设置 use\_encryption = true，将 frpc 与 frps 之间的通信内容加密传输，将会有效防止流量被拦截。  
如果传输的报文长度较长，通过设置 use\_compression = true 对传输内容进行压缩，可以有效减小 frpc 与 frps 之间的网络流量，加快流量转发速度，但是会额外消耗一些 cpu 资源。  
4.2TLS  
从 v0.25.0 版本开始 frpc 和 frps 之间支持通过 TLS 协议加密传输。通过在 frpc.ini 的 common 中配置 tls\_enable = true 来启用此功能，安全性更高。  
为了端口复用，frp 建立 TLS 连接的第一个字节为 0x17。  
通过将 frps.ini 的 \[common\] 中 tls\_only 设置为 true，可以强制 frps 只接受 TLS 连接。  
5\. 把 frpc.ini 隐藏到应用里。  
这个功能 frpc 官方并没有进行实现, 本菜对代码进行了粗糙的更改。  

![](https://mmbiz.qpic.cn/mmbiz_png/Wqr9SokRcTU4oyhEmyCgnNicicKAEicj9odXIdfMDg5LfKYYtwV0ZaZuicxbnnyXRVTjn6ibAQUHkrpicW5p0zlRnnzA/640?wx_fmt=png)

  
github 地址:https://github.com/nbsp-null/frp/  
首先安装 go 环境,https://golang.org/ win 环境下支持一键安装  
然后把 File\_contet 内的配置文件替换成自己的配置文件  
最后在项目根目录运行: go build ./cmd/frpc  
就生成了自带 ini 文件的 frpc.exe

******![](https://mmbiz.qpic.cn/mmbiz_png/Wqr9SokRcTWXcxZtiaMibnvovwBicjfhIibT2t5ty0s12WMUR6mvPjH8ibwXsF2bEt64NVvThjYgNvfctEOYB3UdYgA/640?wx_fmt=jpeg)******