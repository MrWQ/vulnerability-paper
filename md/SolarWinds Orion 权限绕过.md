> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/bM9uUoo08uMvLAnUzRFIsQ)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa26HCks2ickpY8x8HM4esUCVMgNQD00ABDh2HvkrBoic8ia9qORkOBibbLCzP49GibAaVucO3O4kBLL3icGw/640?wx_fmt=jpeg)

(CVE-2020-10148)

**前言:**

SolarWinds 是提供管理软件产品帮助管理网络系统和信息技术的一款基础架构。SolarWinds 正在改变各类规模的企业监控和管理其企业网络的方式。

**漏洞描述：**  

SolarWinds Orion 平台中存在权限绕过漏洞，攻击者通过访问指定路径绕过身份认证。

如 WebResource.adx ， ScriptResource.adx ，i18n.ashx 或 Skipi18n 并传入特制的参数，导致 SolarWinds 错误的对该系列请求设置 SkipAuthorization 标志，绕过权限验证。

**漏洞复现：**

访问 / Orion/invalid.aspx.js 路径，截取请求头中 Location 中 data 获取

```
https://gist.githubusercontent.com/0xsha/75616ef6f24067c4fb5b320c5dfa4965/raw/0d7db4f2ea5aacc0ada7b1a7b23f2ce8ba39315f/CVE-2020-10148.py
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa26HCks2ickpY8x8HM4esUCVMCagLMW7bjwpVWFcebbQfZL9ZCOx9giaMHnZLEm6mIzu120Fial8cLyMA/640?wx_fmt=png)  

将 .js.i18n.ashx?l=en-US&v=43005.14.L 携带到下个访问路径，从而绕过身份认证。 这里访问的是 web.config 文件。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa26HCks2ickpY8x8HM4esUCVMtxOTnL3XP9E4kCdEjyjibt9FJYLu6HwZ812N5D6qQhA0ZLXhzPiaicH8A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa247G03zjhCZGSQD3vMsfDBTnBgtPa21jyEcA2pjduMEwA5GK8TbCWZ0YHW5tqbb7FUtI5XwpeObZw/640?wx_fmt=jpeg)

poc 链接：  

```
https://gist.githubusercontent.com/0xsha/75616ef6f24067c4fb5b320c5dfa4965/raw/0d7db4f2ea5aacc0ada7b1a7b23f2ce8ba39315f/CVE-2020-10148.py
```

**影响版本:**

solarwinds:orion : <2020.2.1HF2  

solarwinds:orion :<2019.4HF6

**修复建议:**

及时更新到最新版本。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa260lZABWwEo49lodRtpGIOoYYt5Ojm4Y1sdMD4ez7rL55g1IW3icCTOia91YicOrh1sjuOB5TiaUibCiaiaA/640?wx_fmt=jpeg)

一起学习，请关注我![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24an9TvS6grA3sWoTRYSQr4hZQYrCwcz8gD1evatvHgAquT3YhfNMxgqib63eQ1mRnQVjQA6W9icxFg/640?wx_fmt=png)

免责声明：本站提供安全工具、程序 (方法) 可能带有攻击性，仅供安全研究与教学之用，风险自负!

转载声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。