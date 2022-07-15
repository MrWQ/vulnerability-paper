> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/U2jEVDipu2hJSon1X8o5jA)

工具地址：https://github.com/codeyso/CodeTest

上篇文章：https://mp.weixin.qq.com/s/xwh81ZeE0Lgx-iIpqZI1_g

    工具集成了常用的命令执行 payload，在识别出特定的中间件、服务后，针对性的进行测试。  

*   **0x01 界面介绍**
    

![](https://mmbiz.qpic.cn/mmbiz_png/6fAcExS2iadciaV3LLZeXOy03X8ibuNaCdQRGp49y66KfHLiaONJTsxXliaZUcBFcxILXhj5a7T5PcM2n09veKgqqKw/640?wx_fmt=png)

从上至下，从左到右：  

*   目标地址：目标 URL；
    
*   Cookie：暂时没有用处；
    
*   漏洞名称：payload 加载处，可以选择测试所有，或者测试特定的模块；
    
*   编辑文件：编辑加载的 payload，方便实时调试；
    
*   参数配置：可选择 payload 的用途（命令执行 or 漏洞测试），设置请求超时时间；
    
*   备注：备注；
    
*   命令执行：执行命令并显示测试结果的区域
    

*   **0x02 使用示例**
    

    当前集成了 ApacheShiro、Fastjson、ApacheTomcat 等测试脚本，脚本可自行添加。

（1）场景一：ApacheShiro 的命令执行回显。

![](https://mmbiz.qpic.cn/mmbiz_png/6fAcExS2iadciaV3LLZeXOy03X8ibuNaCdQSu8krv9Z5aBDibt5xAr6xVYabksK9h7uyez2HBibiciaVsl3ldlXWkTaHQ/640?wx_fmt=png)

此时可以看到目标地址存在 ApacheShiro 反序列化漏洞，并返回了相关的测试信息：

[key: 1QWLxg+NYmxraMoxAXu/Iw==] [gadget: CommonsBeanutils1 ] [echo: SpringEcho1 ] [platform: linux ]

![](https://mmbiz.qpic.cn/mmbiz_png/6fAcExS2iadciaV3LLZeXOy03X8ibuNaCdQAibVHJgkcJfIQicc9OO1ib6icpicU8VckH7K7KLPPrBnnvPDNyicyPRXU6rw/640?wx_fmt=png)

命令执行回显

![](https://mmbiz.qpic.cn/mmbiz_png/6fAcExS2iadciaV3LLZeXOy03X8ibuNaCdQ3Z56IDXgAHOZdiaOAlqjO0L3nRiaDicySyxQrb4KBGKibFWjTkJQPFEDaw/640?wx_fmt=png)

（2）场景二：ApacheSolr 任意文件读取。

测试发现存在任意文件读取漏洞。

![](https://mmbiz.qpic.cn/mmbiz_png/6fAcExS2iadciaV3LLZeXOy03X8ibuNaCdQpISAmsB2wxH6bqJj1MPZ9HFfNscDVX3c7FVqHPpRtUDPc0PGIA8jiag/640?wx_fmt=png)

当使用漏洞测试功能发现存在该漏洞后，通过选择具体的漏洞名称，同时配置相关参数，即可利用该漏洞实现相应的功能。  

![](https://mmbiz.qpic.cn/mmbiz_png/6fAcExS2iadciaV3LLZeXOy03X8ibuNaCdQmzdicxjNxqo3Dn39r5f3sCpqxY6z03Ma3lGOEbj1bibRe5LycMiabE6bg/640?wx_fmt=png)

返回读取的文件内容。

![](https://mmbiz.qpic.cn/mmbiz_png/6fAcExS2iadciaV3LLZeXOy03X8ibuNaCdQFzLdldg8LEIgZB9gGQuMry3GwPDLSbIZ1EZuTvgpxVSIsLdiaF3fweA/640?wx_fmt=png)

*   **0x03 参考链接**
    

https://github.com/Ascotbe/Medusa

https://github.com/zhzyker/vulmap