> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/mIyq3oaGKyyq36y-4CLvmw)

1. 病毒文件的基本信息分析

![](https://mmbiz.qpic.cn/mmbiz_png/F5fjqXxeV4BpyqyFY96joAs95uctK5C40icC7GfefCs1Unjrp7ZaVd90g37d8gDNic1qgtwTFLM9V2ydbH8Zvwdg/640?wx_fmt=png)

1.1 病毒文件具体展示

病毒文件用的**资源图标是 wps 的图标**，以此让大家误认为是 docx 文件，最终是为了诱导大家点击打开病毒文件。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJO5gWJpicEdsyicV3Otp3m7MqbKqO3LIPI7NV8C3Mm6HZ7fs3zfjEQb4sg/640?wx_fmt=png)

1.2 病毒信息具体提示

打开解压病毒文件以及打开病毒文件就会被杀毒软件提示是恶意软件，它属于 **trojan.generic 病毒**。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOxKwcCFJJATCldc5elBjtDsPgmX37Y3faTIPxn7TmgBjtYzNbXicXxtw/640?wx_fmt=png)

1.3 trojan.generic 病毒的定义信息

**trojan.generic** 它是计算机木马名称，**启动后会从体内资源部分释放出病毒文件**，有些在 WINDOWS 下的木马程序会绑定一个文件，将病毒程序和正常的应用程序捆绑成一个程序，释放出病毒程序和正常的程序，用正常的程序来掩盖病毒。病毒在电脑的后台运行，并发送给病毒制造者。这些病毒除有正常的危害外，还会造成主流杀毒软件和个人防火墙无法打开，甚至导致杀毒时系统出现 “蓝屏”、自动重启、死机等状况。

1.4 分析病毒的加壳情况

通过 **Exeinfo PE 工具**可以分析出该病毒样本是没有加壳的样本，并且是 64 位程序。通过区段表信息可以看到它是个常规的 **PE 文件**。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJO59byC00skibRzm54nh4pZI3mfibGDicqClyhmjhmEg1uGpaENhvZ9xcdg/640?wx_fmt=png)

1.5 分析病毒所依赖的模块信息

通过 **CFF Explorer 工具**可以查看该病毒样本主要依赖如下的 5 个模块信息。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOURuRRUNk9ibyyQvicrhL8fBR8uRjWjvHdFIUvIqpr827HicVia8SlPicoVg/640?wx_fmt=png)

1.6 监控病毒文件行为

通过 **Procmon 进程监控工具**进行可以监控进程启动时，该病毒文件会删除自身文件，并重新创建一个新 docx 文件并将原来的文件内容写入到文件中。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOH68ibPv2mvjjCYiasJYicSXVq1eGOkXMpAmg1uV7xCKP2DH9zvFvicY6DA/640?wx_fmt=png)

下面是病毒运行后释放出来的原始文件，第二个文件是为了分析用，不让其进行自动删除病毒文件。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJO7Jumcty3OYGMXXrwLLW2gOjsPrTndyx6YGQQ13BAVX7Kqmcqp8IQgw/640?wx_fmt=png)

2. 病毒文件的关键功能信息分析

![](https://mmbiz.qpic.cn/mmbiz_png/F5fjqXxeV4BpyqyFY96joAs95uctK5C40icC7GfefCs1Unjrp7ZaVd90g37d8gDNic1qgtwTFLM9V2ydbH8Zvwdg/640?wx_fmt=png)

2.1 病毒样本的反调试功能

背景：**ollydbg 动态逆向分析工具**附加病毒文件进程，病毒文件就直接退出了，所以猜测该病毒样本具体反调试功能。

**病毒样本的反调试功能函数：IsDebuggerPresent()**

过掉反调试功能：通过 **API Hook(可以用微软 Detours 库) 方式将反调试功能函数给 Hook** 掉，让其反调试功能失效，这样我们的 ollydbg 动态调试工具才能正常调试。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOXEiaMDiaqjrvQ2O5qIthqdHia3ZpOG1acbmff4ibkF9s0ic2TWxKcRqpvfg/640?wx_fmt=png)

**IsProcessorFeaturePresent() 函数详解**

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOlOQTkjteqZGyUnprpiap4INxnlsnT4Gib9VnJalPJFbCXWr7DfYP96Qw/640?wx_fmt=png)

**IsDebuggerPresent() 函数详解**

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOiaaToRiaqfSwFiasrEpA8Do6V5DsxPQ2cdsib2qCJ8POrTuOGwt7UEM0Hw/640?wx_fmt=png)

2.2 每次只能启动一个病毒样本实例

通过创建互斥体 **CreateMutexA()** 方式进行实现功能

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOGNc88ptdB7ZQdRCGNgrDqFz19kG3skEVWmkBJcpgic8lDeaHibh7mbhA/640?wx_fmt=png)

**CreateMutex() 函数详解**

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOyOkmB4SeSibubYyHhZabXFAVYySE0HPU3pB8sCZEVSzSqfuYjhTRgRA/640?wx_fmt=png)

2.3 病毒文件结束自身进程

释放完原始的 docx 文件后，病毒文件就通过如下方式进行结束自身进程，并通过获取 **mscofee 模块**中未导出的函数并调用 **corExitProcesss 函数**实现关闭当前进程的非托管进程。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOxYE0lZibr6dTY8ONcyGHzZxNVGAZXItlVdiaAyK82eoD4yUBBicB7ias8g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJO0HtfAic1SNoQty5rCP98DORibXOAFKkeYevhT2B0qY9SryyZkGgRKr9w/640?wx_fmt=png)

2.4 启动原始的 docx 文件

通过 **CreateProcess() 函数**方式进行启动打开 docx 文件。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOD3ibQyR9O9xtanv80s8Dw0LpSicOztxhlI6lI7uXaMicQJ3iaId6OSS3jA/640?wx_fmt=png)

2.5 进行信息收集上传

通过 **TCP 网络传输**方式进行数据的信息收集并上传到病毒服务器 (服务器 ip 在山西某地) 上，其中服务器信息及上传的内容通过进行 **MD5 加密**并进行处理。

![](https://mmbiz.qpic.cn/mmbiz_png/jVCRndy8Lr68E8ibibtq7zQ2LicX7VibibsJOSBH2faM32R7nhXd1KryMesMyZg2m29EgQxeYQnFGKwBHLibaOgTgibIw/640?wx_fmt=png)

3. 总结

![](https://mmbiz.qpic.cn/mmbiz_png/F5fjqXxeV4BpyqyFY96joAs95uctK5C40icC7GfefCs1Unjrp7ZaVd90g37d8gDNic1qgtwTFLM9V2ydbH8Zvwdg/640?wx_fmt=png)

通过对该病毒样本的基本信息分析，可以了解到该**病毒的整个流程是**：启动病毒文件获取病毒文件的路径及文件相关信息，释放出原始的文件到病毒文件所在的路径，并将运行的环境信息上传到病毒服务器，接着自动删除病毒文件，最后启动原始的文件。

通过对病毒逆向分析，可以了解到调用 IsDebuggerPresent() 函数可以实现反调试检测功能。

公众号