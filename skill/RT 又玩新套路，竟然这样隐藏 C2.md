> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/wT9y-c9IHsxo_guIUV1p0g)

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaThnJ05AlVoSnzqboLq8IcGZUD3dZA4a0ibwB3YB71QD9mK6iaIoJbxdVA/640?wx_fmt=png)

  

  

  

**背景**

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTORicBZ1ZU9J6WrEAXeSwH5XqgWw3ZJvp4XcLHdZ0zQbQgTwmcrhiaGpA/640?wx_fmt=png)

  

平静的一天，吉良吉影，哦不，微步情报局样本组突然收到这样一个样本。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaT2YMX0CdDGEyoR0ibxpKjwTCJ9Lnk49vtfsuz1ltDG9OZ15SCvDfr58w/640?wx_fmt=png)

  

连接域名是 #######cs.com 相关子域名。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYicYBBz9dxUbmsJnwnsorQJtOJ5xplHhvTbQQSTOicYGocBM1dbXcXlmb9AO0O2hR78z8w3RQibrGFHzw/640?wx_fmt=png)

  

乍一看，域名都是白的，应该没什么问题。

  

我定睛细瞧，最终确认，这是大名鼎鼎的 Cobalt Strike 木马（以下简称为 CS 马）。

  

仔细搜索，发现不简单。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTu1K13gYTrmJRPUDTFE6u1xVA80ib88Kbh2DIMmiaBEQeozGTNjj1tbPQ/640?wx_fmt=png)

  

推测应该是最近非常流行的利用国内某 B 公有云云函数隐藏攻击资产的方法。

  

小样本不讲武德，竟然欺负一个注册了快 5 年的白域名，啪一下，很快啊~

  

![](https://mmbiz.qpic.cn/mmbiz_gif/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTWicVgBQ0NIf6S0pQj5icSnpBGE4rF4J29hAVXsjtU8owzckPOaUb8KDw/640?wx_fmt=gif)

  

我们花了一个周末，弄清了云函数的来龙去脉。

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaThnJ05AlVoSnzqboLq8IcGZUD3dZA4a0ibwB3YB71QD9mK6iaIoJbxdVA/640?wx_fmt=png)

  

  

**总体分析**

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTORicBZ1ZU9J6WrEAXeSwH5XqgWw3ZJvp4XcLHdZ0zQbQgTwmcrhiaGpA/640?wx_fmt=png)

  

这个方法是最近除了 “域前置” 以外，另外一个 RT 特别喜欢的隐藏攻击资产的方法。可能是国内某 C 公有云平台最近修复了其云 IP 可以绕过对添加的 CDN 加速域名所有权的验证，导致现存的一些域前置域名成了“绝版货”，其云域前置攻击变得成本很高。而国内某 B 公有云云函数转发这种方式一方面免费，且部署成本较低，成为了一种新的选择。

  

总体攻击流程如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTQkSdy6B4FzVel9arvXHYQBUeBtmHjId4n4vvH1Lb0DsB61SFibiabqeQ/640?wx_fmt=png)

主要思路为，以往是受害主机运行木马后，通过 HTTP 的 GET 和 POST 方法去请求攻击者的服务器，从而实现持续控制。

而国内某 B 云转发的方法，其实跟我们平时用的 VPN 差不多，通过构造国内某 B 云函数，让函数实现转发请求流量的功能。

最后实现的效果就是在攻击机和受害机之间架设一层” 中转站”，受害机只能看到自己的流量发送给了国内某 B 公有云，从而实现以下目的：

1.  让受害机只能看到和高可信域名的通讯，放松警惕性。
    
2.  隐藏 CS 服务器的 IP，从而实现攻击资产的隐蔽。
    
3.  云服务器使连接更稳定，部分网络状况不好的服务器主机可以避免因为网络问题导致受害机下线。
    

这其实与之前的域前置攻击手法类似。

之前的域前置攻击手法为：

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTN8DJNHibIR75Wxn7mtSnOwXlicztsKKJpWbe2Ziam9HrH73ZQLdDl4CNg/640?wx_fmt=png)

都是通过一个中间件，将自己的流量转发，从而隐藏攻击资产，通过高可信目的地址迷惑用户。

只能说 RT 的手法真的是越来越多了，防不胜防。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTNYt7XvYv3jasGxBUq4hsTVvTDo1PYp56pr4ia5I4icOfXYiat0gT1EbPQ/640?wx_fmt=png)

图片源自网络

基于此的应对方法其实很简单：     

*   **上策**：监测疑似 CS 马的攻击流量，例如请求 /pixel，/__utm.gif，/ga.js 等类似 URL 的流量进行重点监测，或者使用微步在线情报识别 CS 马的外联地址，我们已经收集了较多的某 B 云云函数地址情报以及相关的 CS 服务器地址。（要恰饭的嘛）
    
*   **中策**：确认自己资产中是否有某 B 云函数的正常业务，若无的话直接封禁 *.apigw.#######cs.com 等子域名。
    
*   **下策**：直接断网，只开放静态网页服务（bushi）![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYicYBBz9dxUbmsJnwnsorQJtOV9LEYPUugibpBbQQxge5rFWl9skYyfibibm3U7Iukgd4HQSu020fAPFqQ/640?wx_fmt=png)
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYicYBBz9dxUbmsJnwnsorQJtOdvFIEx18BOuq3rX3Z6TyWMwiaTHCSJ8Qqq1btya4KjMOm8mxjrU32cg/640?wx_fmt=png)
    

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaThnJ05AlVoSnzqboLq8IcGZUD3dZA4a0ibwB3YB71QD9mK6iaIoJbxdVA/640?wx_fmt=png)

  

  

**BT 视角攻击**复现****

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTORicBZ1ZU9J6WrEAXeSwH5XqgWw3ZJvp4XcLHdZ0zQbQgTwmcrhiaGpA/640?wx_fmt=png)

在发现此类攻击之后，我们寻找了相关的攻击细节。

本文部分细节参考了「风起」的文章《## 攻防基础建设—— C2 IP 隐匿技术》， 感谢他~

有人说文章已经写过了如何利用，你为啥还要再写一遍?

主要是文章是 RT 同学写出来的，正所谓 “绝知此事要躬行”，很多事实只有验证一遍才能证实方法的存在，同时以 BT 的身份重新复现攻击手法，也可以有一些之后怎么应对的思路。

首先，要去某 B 公有云官网申请一个个人账号，同时要通过个人认证，用微信扫一下就好了， 不过微信要绑定自己的银行卡且实名。这个安全措施让我不禁想到，一旦拿到攻击者的云函数，拿到账号，理论上是应该可以拿到对应绑定的姓名手机号和身份证号的。

如下图，我就已经完成认证了，认证状态是 “已认证”。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaT9kwgrPsyic97RLQ1Fmop9RE1R7lmpovibpLvaER4ickpEic0nn030V0GiaA/640?wx_fmt=png)

然后打开云函数模块。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTXibE9icmlePFicY1dbp0YknvJs2qWdscGQwhvEkOAPjGefJcmjesYKaqw/640?wx_fmt=png)

初次访问需要授权。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTTVByfsVZEcKlQheW2tymJpyj8LSryj02c6Wn3grMjcefwKFibxw5HEg/640?wx_fmt=png)

点击 “同意授权”，出卖自己的灵魂。（主要是不同意也不给你用）

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTlsVVsLvvnw8s68kn93F9Ak9VyHicCPLMcYaic8IfDOd6P1SvVg1Mzw0A/640?wx_fmt=png)

然后我们就可以开始创建云函数了。

首先，我们选择自定义创建的方式，函数名称可以自己随便起一个，注意函数名不要起个人 ID 或者是独一无二的名字，因为之后我们可以通过访问云 API 抓包获取函数名称的，如果是个人 ID，RT 的小同学小心我们溯源哦~ ![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTDPSA2Hh3ZJicmsXalibCan7h7IicyX4zBkR5JOxoVVuNpqibSHrso9AWaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTdJlUkdLvNKbmEp3GtAiaJlGWQThgBnahQfevZsia34pa2wyhTf8UpsJw/640?wx_fmt=png)

因为笔者比较喜欢 Python，所以运行环境选择了 Python，当然也可以选别的语言。正所谓 Python 有 Python 的好，其他语言有其他语言的坏嘛。

创建成功之后，需要先点进 “触发管理 -> 创建触发器”。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaT0kv3C1xVJ5NtbA8IhGPhyr49ibVqx09DHXibVeXQpm9PjsF0c98wlX0A/640?wx_fmt=png)

这时候可能就有人问了，为啥要创建触发器呢？

简单解释就是，没有触发器，你的函数只能自己访问，创建触发器之后，国内某 B 公有云会给你一个公网的 API 地址，且每次访问这个地址都可以触发一次函数。

在创建触发器的时候，仍然需要赋予云函数触发器的权限，如下图所示（红框部分）。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTx48nc8utlMjh2uWjtptmbKFVwY1VSiagiccJLADoS57B28uulDd9j4Tg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTUYy9OJtwNmVpVdLyhf54y5UoibH66XMo0IXP1BMiaAVmCibngP55icCLeg/640?wx_fmt=png)

赋予成功之后，立马就收到了通知。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTOibzHNCiaA6WuNMB0BEYbG21gGJWK1NzAZbOFZC4QAwfdFKqhLOcswrQ/640?wx_fmt=png)

下面开始编写函数。

我们先简单写一个函数，直接返回页面。

PS：某 B 公有云云函数有自己的一套规则，一套特别麻烦的标准和规则，我建议大家不要纠结细节，直接复制我的代码就好了。

下面这个图就是， 先简单写一个返回测试数据的函数， 返回格式需要如下图这种非常严格的字段。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaT6XiauVckHibUweIz6icpxDzXXS5Nh2fEF9qUCZaEyTCmoUMD4VrJia20vw/640?wx_fmt=png)

访问我们的云函数地址，发现可以顺利返回数据。（当然，我被函数搞了几十次的失败就不表了~ ![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYicYBBz9dxUbmsJnwnsorQJtOdoaPLLhyibq51xtKkVLscRibmEYKeZuH0b8KgZw1WKkWwf97MNHficJFQ/640?wx_fmt=png)）

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTyA4Da8Tmw6ia0ZaDCBA4ibCmKzhFKmoL3iaEicHjWJtNyibRRZhewFIm4Mw/640?wx_fmt=png)

关于请求的所有字段，比如 headers，body，status code 这些内容都集成在 Event 这个输入字段中了，详细解释的地址在下面：

Event 字段说明地址 ：https://cloud.########.com/document/product/583/12513#apiStructure

我建议大家还是不要了解了，如果以后不需要搞这种基于云的服务开发，完全没有必要重新学一遍。

![](https://mmbiz.qpic.cn/mmbiz_jpg/pOGBCic4vYicYBBz9dxUbmsJnwnsorQJtOEriciclaXy9gYt0YkkslfiaAoO70cNPsR9V5DGWQrPqwicQict8BDal61DQ/640?wx_fmt=jpeg)

所以大家可以看到，要是我在里面写一个请求方法，请求一个固定地址，会发生什么呢，会不会云函数自动代替我完成对目标地址的请求，就像 VPN 或者某科学上网工具一样?

所以，我动手试了一下。

把请求地址写成了我们的官网：

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTbpBhUt3mkq8ZtGJ9U1KOmXApceCjRtHIegiaV70kHicxEZiaZWIbXZrGQ/640?wx_fmt=png)

可以看到， 访问之后果然是代替我们请求了我们公司官网的地址。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTQ4npCh1dDTqiad803czEBIvYBARUSk2ObkER2LfBlxCnwH9ZjzLc0pA/640?wx_fmt=png)

到这里就是正式编写我们的函数了。

我们要实现一个效果就是收集请求端的数据包，收集请求包请求数据，然后把请求包原样发送给我们的 CS 服务器，最后收集 CS 服务器的返回包返回给请求方。

具体的代码如下：

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTnynHz7nrIRnme1eRTCutsStpaiafAXVicZMxKKj6Rg2T7fo2eyQGMib9w/640?wx_fmt=png)

后面的代码参考了「风起」的文章中把 body 中标识字节的 b’’ 字段舍弃的方法。

注意这里是某 B 公有云云函数的规定，必须要返回一个带  "sBase64Encoded，statusCode， headers，body 字段的一个字典。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTWptKMFUNIHLcNgJlJDpfWYQUvbxR6QYTjXwu4c7RIWCTtxEvyeVU5g/640?wx_fmt=png)

另外一个坑是，某 B 公有云云函数的超时时间的问题。

当我们配置好之后，访问可能会遇到下图所示报错：

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaT0Y8U1IMlYTCmZBxOQcGH69BNHibltknMNDmDLWeibzibXScyR2oCA8fdg/640?wx_fmt=png)

是因为 CS 马在运行后会先下载一个 200K+ 的配置文件（这个研究过 CS 马的童靴应该很了解），而我们的云函数在下载这么大的文件的时候会超时。

所以这个问题很难发现，直接让笔者整个周末都在研究这个问题。

顺便吐槽下某 B 公有云的错误返回，实在是太概括了，根据返回根本定位不到问题在哪里，要自己一行一行的 re 代码…… ![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTLneuz0AsibuvrHYOxH1lzympTUUosbTErxgeow2g7ICkLCmeziabPCpg/640?wx_fmt=png)

这里超时时间直接给他拉满，设成 100s。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTmia9coSSY1sj8zibUN0icoJEnc3DhNIetFjakKsL3iaP7mOqWDA4WUmkbw/640?wx_fmt=png)

函数配置好之后，我们就可以用我们的地址上线啦。期待，呲溜~

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTsJ7iaNQBGSwSibMtVVSGqLJ11yUVVuVkceULJeDKZCuMcWJHpsXyOGqg/640?wx_fmt=png)

虚拟机运行：

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTrwy9gQgOib6wAButLCxq4N0FBZOECbhEyz9uvjia4cOO0HaPIu5viaInw/640?wx_fmt=png)

虚拟机抓包发现请求包已经发出去了。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaT63WsSVm5BpxCQSUyP6GkjA2Ju6mEo9jUFXj2omLgNtT8D3QiaiaZYzfw/640?wx_fmt=png)

仔细看一下，确实发出去的包的地址确实是某 B 公有云主机的地址。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTdEFYgEJbCBZ0sRla5jWJgA5fzPvyDoJ03U7MDC41ibrYkGu43OvUODQ/640?wx_fmt=png)

没问题，CS 服务器检测到我的虚拟机上线了。

![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaT2OaqVJoD4qDcucsaeF3WaK7ChWAbTQkOZYyicpYW6azvicuCOibYp9ibQQ/640?wx_fmt=png)

最后，感谢一下「风起」的文章。虽然域前置，某 B 公有云云函数隐藏这些攻击方法我们都已经掌握了，但是参照仍然让我们少走了一些弯路（虽然有的坑也没避掉）。

通过域前置，某 B 公有云云函数隐藏等这些虽然给溯源增加了一层难度，但也不是完全不可能，如果得到有关方面的协助还是有办法找到攻击机的。

比如，某 C 公有云云的域前置，只要找到上线时连接的 Host 在某 C 云内部的 DNS 对应的 IP，就可以拿到其对应的攻击 IP 了。

某 B 公有云云函数这种方法呢，就更简单了，反正每个触发器对应的 API 地址就一个，发现了封了就行了，自己也没法改，因为 CS 马的上线地址填的这个。另外在请求 API 截止的时候会函数名，如果起的有特色一点，也不是完全没有溯源的可能。

攻防双方永远在博弈中共同进步，最近爆出来的域前置攻击，某 B 公有云云函数转发， 还有我们最新发现的微软子域名劫持， 其实都是 RT 在应对各种防守工具想出来的比较好的方法，我们也在不断提升对这种攻击的检测的能力。

攻防双方应该像两条藤蔓一样互相攀爬着向上。从攻击方最开始不停地开扫描器扫描，企业封堵 IP；到攻击方发送无数个钓鱼邮件，企业进行样本分析溯源；最终转变为更高手段的攻防博弈。攻防水平不断提升，双方过招之后应该是直呼 “有点东西”，而不是 “几天不见，怎么这么拉了”。

如果大家看完能有些收获，我们整整一个周末研究这个方法就没有浪费。![](https://mmbiz.qpic.cn/mmbiz_png/pOGBCic4vYica3iaToL269rBa94VTBSTXiaTySQ2BQbwMvHDh8PUfxW0Opk60fn8l0eaBK0WVwJfN0pt4n1COXrxng/640?wx_fmt=png)

- END -

  

**关于微步在线研究响应团队**

微步情报局，即微步在线研究响应团队，负责微步在线安全分析与安全服务业务，主要研究内容包括威胁情报自动化研发、高级 APT 组织 & 黑产研究与追踪、恶意代码与自动化分析技术、重大事件应急响应等。

微步情报局由精通木马分析与取证技术、Web 攻击技术、溯源技术、大数据、AI 等安全技术的资深专家组成，并通过自动化情报生产系统、云沙箱、黑客画像系统、威胁狩猎系统、追踪溯源系统、威胁感知系统、大数据关联知识图谱等自主研发的系统，对微步在线每天新增的百万级样本文件、千万级 URL、PDNS、Whois 数据进行实时的自动化分析、同源分析及大数据关联分析。微步情报局自设立以来，累计率先发现了包括数十个境外高级 APT 组织针对我国关键基础设施和金融、能源、政府、高科技等行业的定向攻击行动，协助数百家各个行业头部客户处置了肆虐全球的 WannaCry 勒索事件、BlackTech 定向攻击我国证券和高科技事件、海莲花长期定向攻击我国海事 / 高科技 / 金融的攻击活动、OldFox 定向攻击全国上百家手机行业相关企业的事件。

  

  

**内容转载与引用**

  

1. 内容转载，请微信后台留言：转载 + 转载平台 + 转载文章

2. 内容引用，请注明出处：以上内容引自公众号 “微步在线研究响应中心”

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/pOGBCic4vYicZnSxLEdVd7S098eib2I4wib6QibO5sfnlXUvvTPXhSQwlQ2bHwYiab3dUvkyzjRHaZm2xXmydX9BibXbA/640?wx_fmt=jpeg)

**微步在线**

**研究响应中心**

- 长按二维码关注我们 -