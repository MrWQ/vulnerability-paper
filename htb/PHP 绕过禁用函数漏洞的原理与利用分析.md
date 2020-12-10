> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/_KCqGJnHaCBjCZ0VPo898Q)

![](https://mmbiz.qpic.cn/mmbiz_gif/Az5ZsrEic9ot90z9etZLlU7OTaPOdibteeibJMMmbwc29aJlDOmUicibIRoLdcuEQjtHQ2qjVtZBt0M5eVbYoQzlHiaw/640?wx_fmt=gif) 聚焦源代码安全，网罗国内外最新资讯！

  

漏洞简介

PHP 发布公告，旧版本的 php_array_merge_recursive 函数中存在 UAF 风险，被利用可能导致用来绕过禁用函数。

**受影响的版本**

PHP 7.2 - 7.4.9

安全专家建议用户尽快升级到安全版本，以解决风险。

  

漏洞原理

**一、array_merge_recursive 函数实现**

在 array_merge_recursive 函数的实现中，通过遍历源数组键值，如果键值不存在，则将对应的值直接插入目标数组；如果键值存在，则查询相应的目标数组。在目标数组不存在此键值时，将键值与相应的值插入目标数组；如果存在相同的键值，则会尝试将相应的值加入到目标数组中。具体处理如下图，在目标值为 NULL 时，将其转变为数组类型并在数组中加入 NULL，在源数组中的值为对象类型时将其转换为数组类型，尝试为 src_entry 添加引用后将 src_zval 添加到数组中；如果源数组中的值类型为数组则递归调用 php_array_merge_recursive 函数。

![](https://mmbiz.qpic.cn/mmbiz_png/oBANLWYScMQG1jMe23NIBFayvOpTc7yocwExcc4MteicvLUE89bIia6UKwOL5SJXovPSTgmo89jQzS9KVz97H7Nw/640?wx_fmt=png)

**二****、****原理分析**

在尝试为源数组中的值添加引用计数的时候错误地调用了 Z_TRY_ADDREF_P(src_entry)， src_entry 此时为对源数组中的值的引用，此时引用计数被添加到了引用而不是源数组中的值。

如果在 array_merge_recursive 函数中传入可变的字符串（通过直接赋值获得的字符串不可变，在尝试添加引用计数时会失败），此时 src_zval 即可变字符串的引用计数并没有增加，在数组被销毁时，因为可变字符串的引用计数提前变为 0 导致 UAF。

**三、利用分析**

 _注: 以下调试直接在 php 调试而不是在服务器加载 php 调试，但是差别不大。_

1、在字符串被释放后，创建一个新的对象占位，进行类型混淆，此时字符串的 len 被新创建对象的 ce 覆盖。ce 是一个地址，所以后续不会影响字符串的写入。

![](https://mmbiz.qpic.cn/mmbiz_png/oBANLWYScMQG1jMe23NIBFayvOpTc7yoq0L0J1t58g4o0Zs9cVNYkwQ1Iyu0tsWQUGtQXvBrA9aEO19I7ibYdHQ/640?wx_fmt=png)

占位前后对比图如下：

字符串对象被释放后，创建对象前：

![](https://mmbiz.qpic.cn/mmbiz_png/oBANLWYScMQG1jMe23NIBFayvOpTc7yo4kae0G1WzmLFqJAKhdWyfwtndJkMskoxLiavx2UzwWfZhM5QZNtZh2A/640?wx_fmt=png)

创建对象后：

![](https://mmbiz.qpic.cn/mmbiz_png/oBANLWYScMQG1jMe23NIBFayvOpTc7yoCJYicpXvd37c8nEGoBKlwRZQpmFicmxQOpicsBdkIfiaChKAR34XnlMdOQ/640?wx_fmt=png)

2、读取新创建对象的 handlers 方便之后泄露内存信息，handers 的值即为上图的 0x0000000008dfe500，在后面可以达到任意内存读取后可以用来泄露 php 基地址。读取新创建对象中包含堆地址的区域，获取被释放的字符串地址，例如可以读取 0x7ffffb080540 中的堆地址，减去 0xc8 即为字符串对象中的字符串地址 hex(0x00007ffffb0805b0 - 0xc8) = 0x7ffffb0804e8 即为字符串对象的 val 属性的地址。

3、将新创建对象的一个属性的值指向的类型改写为引用，引用的地址为一个伪造的引用字符串对象。可以将新创建对象的第一个属性即 properties_table 数组中的第一个元素的类型改为引用，地址改为伪造的引用字符串对象的地址。地址 0x7ffffb0804f8 保存的即为新创建对象的第一个属性的地址，地址 0x7ffffb080500 中存储的 0xa 代表引用类型。

![](https://mmbiz.qpic.cn/mmbiz_png/oBANLWYScMQG1jMe23NIBFayvOpTc7yopakQbc7cjEaa9k5gibcAiasQm1WoLDF6Gy4LEqibq0M1eT31hZPtZoA1g/640?wx_fmt=png)

其指向的地址 0x00007ffffb080548 保存的为伪造引用对象的地址，伪造的对象的第三个八字节需置为 6 （引用对象的类型）。引用字符串对象的内存布局如下图。可以看到，引用中保存类型为 0x6 代表字符串类型，但是地址为 0x0，之后可以通过写入任意地址来达到内存读取。

![](https://mmbiz.qpic.cn/mmbiz_png/oBANLWYScMQG1jMe23NIBFayvOpTc7yomIuTCBbeRjCu9jwshsicA51Wbolh7PpYdWXP1oTc3WTI5nnptjE97UA/640?wx_fmt=png)

4、通过修改伪造的字符串的起始地址来达到任意内存读取，利用之前泄露的 handlers 地址来获取 elf 基址，之后遍历内存获取 zif_system 函数的地址。

5、伪造一个闭包对象，从一个真实存在的闭包对象拷贝其存储的值，修改函数类型为内置函数类型，has_dimension 属性地址为 zif_system，修改后如下图。

![](https://mmbiz.qpic.cn/mmbiz_png/oBANLWYScMQG1jMe23NIBFayvOpTc7yoljT5Oon3vyv4nuAU4xcZIkTiaRStTVWibgTJx5XicUn22WVBAQ4mRhiaCQ/640?wx_fmt=png)

6、修改对象的一个属性地址为伪造的闭包对象的地址，调用对象的属性函数即可完成禁用函数的绕过。

  

漏洞验证

**一、在 7.4.5 版本中进行攻击尝试**

在目标服务器上传利用脚本，执行命令。

**二、7.4.10 版本修复分析**

修改 Z_TRY_ADDREF_P(src_entry) 为 Z_TRY_ADDREF_P(src_zval)。

![](https://mmbiz.qpic.cn/mmbiz_png/oBANLWYScMQG1jMe23NIBFayvOpTc7yokjma2RKgZaj3Gib7p8EttWmAw2Hic6tfqS7IXCrjCnvCEhEYVNdU0ibibw/640?wx_fmt=png)

  

参考

*   https://bugs.php.net/bug.php?id=79930
    

  

![](https://mmbiz.qpic.cn/mmbiz_gif/oBANLWYScMQUGmGl5DEIvfgYZ064WQYaxjN2cKvlbL3OEXEecGHBaIgqpwGaiavDx3ZVSvZ3ibP4ujibAqNjKCYOQ/640?wx_fmt=gif)  

**别走，代码安全实验室招人****了！**

  

**奇安信代码安全实验室**正在寻找漏洞挖掘安全研究员，针对常见操作系统、应用软件、网络设备、智能联网设备等进行安全研究、漏洞挖掘。

> 奇安信代码安全实验室是奇安信集团旗下，专注于软件源代码安全分析技术、二进制漏洞挖掘技术研究与开发的团队。实验室支撑国家级漏洞平台的技术工作，多次向国家信息安全漏洞库 （CNNVD）和国家信息安全漏洞共享平台 （CNVD）报送原创通用型漏洞信息；帮助微软、谷歌、苹果、Cisco、Juniper、Red Hat、Ubuntu、Oracle、Adobe、VMware、阿里云、飞塔、华为、施耐德、Mikrotik、Netgear、D-Link、Netis、以太坊公链等大型厂商或机构的产品发现了数百个安全漏洞。目前，实验室拥有国家信息安全漏洞库特聘专家一名，多名成员入选微软全球 TOP 安全研究者。在 Pwn2Own 2017 世界黑客大赛上，实验室成员获得 Master of Pwn 破解大师冠军称号。

如果你：

> *   对从事漏洞研究工作充满热情
>     
> *   熟悉操作系统原理，熟悉反汇编，逆向分析能力较强
>     
> *   了解常见编程语言，具有一定的代码阅读能力
>     
> *   熟悉 Fuzzing 技术及常见漏洞挖掘工具
>     
> *   挖掘过系统软件、网络设备等漏洞者（有 cve 编号）优先
>     
> *   具有漏洞挖掘工具开发经验者优先
>     

那么，你将得到：

> *     富有竞争力的薪酬，期望赏金猎人上线
>     
> *   补充医疗保险 + 定期体检 ---- 你的健康我来保障  
>     
> *   定期团建 ---- 快乐工作交给我
>     
> *   福利年假 + 带薪病假 ---- 满足各种休假需求
>     
> *   下午茶 ---- 满足你每天的味蕾
>     

**注：工作地点为北京、西安。**

心动不如行动！不要犹豫！赶紧给 **zhuqian@qianxin.com** 投简历吧！我们会在 3 个工作日内找到你~

**推荐阅读**

[Apache Solr 未授权上传（RCE）漏洞（CVE-2020-13957）的原理分析与验证](http://mp.weixin.qq.com/s?__biz=MzI2NTg4OTc5Nw==&mid=2247495566&idx=1&sn=37c395075b237c3ff6ea763635da2fdd&chksm=ea94dee4dde357f23b034136b8a2ac4cd24b2fb35f7cf3b6021cb117dfa45b99f88e48f3c712&scene=21#wechat_redirect)  

[Netlogon 特权提升漏洞 (CVE-2020-1472) 原理分析与验证](http://mp.weixin.qq.com/s?__biz=MzI2NTg4OTc5Nw==&mid=2247495053&idx=1&sn=0037b8fbf3cdedeca52a0f50ab901cea&chksm=ea94dce7dde355f1177dcf9691ee5d8c76df6b921f5626eafcdeebeec5af51d9ee4b173ff938&scene=21#wechat_redirect)  

[QEMU CVE-2020-14364 漏洞分析（含 PoC 演示）](http://mp.weixin.qq.com/s?__biz=MzI2NTg4OTc5Nw==&mid=2247494803&idx=1&sn=6785d0329c6cbfb615776e3980a7f4ec&chksm=ea94ddf9dde354ef0c3a45b8dcc79c7813684a7249065fb5eafc391e2e20c09a9394f989dea7&scene=21#wechat_redirect)  

题图：Pixabay License

**转载请注明 “转自奇安信代码卫士 https://codesafe.qianxin.com”。**

![](https://mmbiz.qpic.cn/mmbiz_jpg/oBANLWYScMSf7nNLWrJL6dkJp7RB8Kl4zxU9ibnQjuvo4VoZ5ic9Q91K3WshWzqEybcroVEOQpgYfx1uYgwJhlFQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/oBANLWYScMQjfQ8ZhaOGYOwiaOkCe6UVnwG4PcibqI6sJ3rojqp5qaJa0wA2lxYb0VKwria7pHqS9rJwSPSykjMsA/640?wx_fmt=jpeg)

**奇安信代码卫士 (codesafe)**

国内首个专注于软件开发安全的

产品线。

   ![](https://mmbiz.qpic.cn/mmbiz_gif/oBANLWYScMQ5iciaeKS21icDIWSVd0M9zEhicFK0rbCJOrgpc09iaH6nvqvsIdckDfxH2K4tu9CvPJgSf7XhGHJwVyQ/640?wx_fmt=gif) 觉得不错，就点个 “在看” 吧~