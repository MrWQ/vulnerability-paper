> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rEPfrmJvxkDNHRKakf0qNA)

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XwxlNAtsDKIzVHoKDHQf12wsPyLr329UNvbj4gv0vviaNbNmcpXqkzqQ/640?wx_fmt=png)  
  2020 年 12 月，写作背景是一个宁静的夜晚，本篇文章主要是为大家带来一些开源 WAF 的介绍方便可以使用开源产品搭建靶机环境，增强对 waf 的认识，大佬们路过轻喷。

Web 应用防护系统（也称：网站应用级入侵防御系统。英文：Web Application Firewall，简称：WAF），利用国际上公认的一种说法：Web 应用防火墙是通过执行一系列针对 HTTP/HTTPS 的安全策略来专门为 Web 应用提供保护的一款产品。

WAF 是通过检测应用层的数据来进行访问控制或者对应用进行控制，而传统防火墙对三、四层数据进行过 0 滤. 从而进行访问控制，不对应用层数据进行分析，不过这里笔者需要友情提醒下，现在有的防火墙也是可以对应用层进行包过滤 (状态防火墙)，不过毕竟这不是他的本职工作。

mod_security 大规模同步 在一个大规模的网络环境下，批量管理上千台 web 服务器的情况下，当防护策略发生变化，规则的同步将会是一个麻烦的事情。在运维团队得力的情况下，可以通过内部 github 与 Jenkins 的整合进行规则文件的同步。网络复杂情况下如何部署 中大型的公司中，一套系统可能会用到多种语言，某些情况下无法保证 mod_security 无法支持，例如 tomcat。在此种情况下，我们可以使用将 waf 推送至 nginx 的反向代理节点，进行全方位的防护。实际情况下，网络的复杂多变导致很多子站点无法得到防护，将 waf 部署于前端的反向代理会是个理论上很好的方案，但实际情况下，很容易导致整个网站触发误报，为此正式上线 waf 前需要各种各样的耐心测试。

对于企业上 WAF 常见的解决方案基本包括以下方面：

-> 购买硬件 waf  
-> 使用云 waf  
-> 部署应用交付，使用内置的 waf 功能

-> 使用开源 waf  
-> 使用集成化软件，如 360 主机卫士

这次主要给大家介绍一个不错的开源 WAF-**ModSecurity**，ModSecurity 是一个开源的 Web 软件防火墙。它可以作为 Apache Web 服务器的一个模块或单独的应用程序来运行. ModSecurity 的目的是为增强 Web 应用程序的安全性和保护 Web 应用程序避免遭受来自已知与未知的攻击. 类似在 web 应用这条高速路上设了一道关卡，负责对来往的应用数据包进行检查，并且对恶意攻击的数据包进行处理。同时该产品提供了打分机制对危险评分，当分值达到我们预设的值时，将会讲该包丢弃，设计这个主要是有些业务可能会触发报警，但是属于正常业务，所以关键的地方就是分值设定调优，设定一个理想的值。

ModSecurity 处理事件分为 5 个阶段，分别为请求头阶段（Request-Headers）、请求头阶段（Request-Headers）、响应头阶段（Response_Headers）、响应体阶段（Request_Body）、记录阶段（Logging） ，具体每个阶段工作原理这里不细说。这里我是把 waf 装在了 web 容器里面，如果你们公司有很多服务器，同时做了负载均衡解决高并发，可以把 waf 推到负载上面过滤所有网站的流量。

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XvaCm01Pek7oUTJvic2uM2bbQlxZhv5MV1BpRT4iawZiaAUmEZw2XpPNRg/640?wx_fmt=png)

**下面为大家详细讲解安装过程**

**1.** **下载服务器包信息到本地** -> "yum makecac"  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8X6AagY6nT45XImPOAjfUY3Z8OplYh83K6Aguib7BQlJoFkWUic1HxHdiaQ/640?wx_fmt=png)

**2.** **搜索 mod_security 模块相关包内容** -> "yum list |grep mod_security "  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XIxkw0RE22Q2sd2axPHYPyNibIyibkcvdicZpNQgxbTMqvibucicbKibKzufA/640?wx_fmt=png)  

**3.** 我们直接全部**安装**（-> "yum -y install mod_security*"） 或者只装 1 和 3 (1 是搜索引擎, 3 是规则库)

**4.** **重启 Apache 服务** -> "systemctl restart httpd", 重启后，会发现之前能进去的 dvwa 现在打不开了 是因为 waf 配置所导致的，默认不允许 ip 访问，绑定 hosts 就可以了![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XJb2klAkm3XTavf9nyumMS0egrfEicrQyFOfsjWNJdCHEK7xdT9og2Ow/640?wx_fmt=png)  

**5.** 以下为 **ModSecurity 相关配置文件介绍**，这个是 waf 引擎的主要配置文件, 定义开关主要配置。如下图  
![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8X9JtdcUDzoOgogP4shqiaqtDn9AW4mOwblEJDHHFWFl6PybkMS8kA5yA/640?wx_fmt=png)  

这个是控制 waf 的开关  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XWQibxNk2f0I2oXbrpOMaxXS2G5wIEd1oeR3GU31SQDjmAjcxdP57wicw/640?wx_fmt=png)

处理 post body 内容 只有打开了才会查看 body 必开开关

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XTbanrQV8uON9DB0zSTu8mZ0XiaBVHlHLUpFKSluwG4pzBkbicmzaDXnQ/640?wx_fmt=png)

第一个是 最大处理 body 的数量  
第二个是 当没有文件的时候最大能处理多少  
第三个是 内存的占用大小  
根据网站的实际情况设置  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XUBib2VhibQfonPKOgazmQITujfjVVpW7aRiaH8zA1SPG8GvQReqoVCKQA/640?wx_fmt=png)

waf 审计的日志 路径  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XSjl8aDpTOTu1UZBzMPQibynsgBQpL52kvAWf3V6IqGnVjqV4dQbuAgw/640?wx_fmt=png)

**6.** **这个****配置文件是定义 activaged_rules 文件夹规则的配置文件**，它比主要配置文件更细致化 -> "vi /etc/httpd/modsecurity.d/modsecurity_crs_10_config.conf"  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8X3jk47U3MEcfXEPRfBJjEo7O1MgMlkIe7Z56ykVR0VI2Jc2EW3hlDqA/640?wx_fmt=png)

**7.** **这个文件夹内是规则文件** -> "/etc/httpd/modsecurity.d/activated_rules"  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XpNHywL8fluCzP3MES0xxMq2EiajavQQGNd8POkq6qmibPicd7ZWDpmDiaA/640?wx_fmt=png)  

**8.** **定义规则的配置文件**，不像很多 waf，遇到一个敏感输入就阻断这种不讲武德的方式，modsecurity 提供了两种模式，模式 1: 撞到一条规则直接阻断，模式 2：对行为进行测算决定要不要阻断; 如果想使用模式 2，在模式 1 前面加 #号注释掉，并且把模式 2 中的 deny 改为 pass 就可以 
===================================================================================================================================================================

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XbAbS8EiadEkXMXTm2o8J9E09evJ0WqTIP6AMtDmgxLMMTZJ0ebunNbA/640?wx_fmt=png)
============================================================================================================================================

**9. 撞到的级别算分值，分值到达指定后就阻断**
==========================

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XoFkgyIG1SPGS0oFayKv59iadfA8xqPkMUT4KnJY9b8pMWGoR4gzqbEQ/640?wx_fmt=png)

**10.** **出入站分值设定**  

setvar:tx.inbound_anomaly_score_level=5, \ 这个定义的是进站分值，定义出站分值的是 setvar:tx.outbound_anomaly_score_level=4, \  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XZfrqXiacWeCqsjL1okIrQZxicb1wqv5okP1TK3DssjqqPy2ibJGtCOWlQ/640?wx_fmt=png)

11. 还有**最关键的一步是触发这条规则**，默认是注释的，所以第二种模式是不会阻断的，使用第二种模式 需要把注释取消了。  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XqRedquNGQXzOahic05Va1e4vAeugf8BN4SB2z9sbY8nqrWicykLlfQRQ/640?wx_fmt=png)

ip 属于哪个城市的数据库 可以下载启用 针对国家或地区阻断

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XyYXMhpgTlDeLqScfoqLmqicnE7vria9EgOLBkicibc4WJhOZ7eoULyRqTA/640?wx_fmt=png)

设定最大字符长度

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XBJmJ9MtFyHD9JvAF8gdBxOk1a5BAnCmLrkgOTJlueaAuPrGgVLxicibA/640?wx_fmt=png)

设置参数值 长度

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XBT5osWicoDDiaCE7Yp14MscdpXe5S5bT94ygXQibpHwtBLGpKK2oJHRog/640?wx_fmt=png)

文件上传的大小

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XMt6GibStzRJIHUtI88kibEyicN7DeTiclbRFIrEsEribNu6TTfTicYM58BQQ/640?wx_fmt=png)  

setvar:'tx.allowed_methods=GET HEAD POST OPTIONS', \ 定义了只允许 get,head,post,options 请求方式

setvar:'tx.restricted_extensions=.asa/.asax/.ascx/.axd / 定义请求文件的后缀 遇到直接阻拦  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8X2n0EhdBMRersw8UC3euzDM9WzI71bM4NibkhzM9WSnT7wFdjaTg9suQ/640?wx_fmt=png)

**13. 查看日志** -> "tail -f modsec_audit.log"  
A 板块可以看出哪个时间段谁来访问我。它的 ip 和端口，B 板块对应的是请求包、F 板块是返回包、整个 H 对应的是 WAF 的检测日志  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8X9NHUWSRh0cqPIMzK8eJ6ElRKSrPEhBaqRkvKLplQlWZQtlnbX33tYg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XmI4aOB0wdobiaQPBiaFTXgKFjic3ckpub3vfQtDNRdWT0YjHS83UWyqYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8Xibv0OCS0cRPR8CjdFeVc8iaILfbHkXKQ0COAGqYRShDxq3VNjpCJ2icUg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicFSIczQQMl4xdYskRE0SB8XkKpfbVCVg5iax8kgfb45eWu7Ric36P5hnMcibPDPZRT8YxkyG6ic7J5Pqg/640?wx_fmt=png)  

**14. 规则四部分**
=============

**第一规则：基础规则集**  
modsecurity_crs_20_protocol_violations.conf HTTP 协议规范相关规则  
modsecurity_crs_21_protocol_anomalies.conf HTTP 协议规范相关规则  
modsecurity_crs_23_request_limits.conf HTTP 协议大小长度限制相关规则  
modsecurity_crs_30_http_policy.conf HTTP 协议白名单相关规则  
modsecurity_crs_35_bad_robots.conf 恶意扫描器与爬虫规则  
modsecurity_crs_40_generic_attacks.conf 常见的攻击例如命令执行，代码执行，注入，文件包含、敏感信息泄露、会话固定、HTTP 响应拆分等相关规则  
modsecurity_crs_41_sql_injection_attacks.conf SQL 注入相关规则（竟然有一条 MongoDB 注入的规则，很全）  
modsecurity_crs_41_xss_attacks.conf XSS 相关规则  
modsecurity_crs_42_tight_security.conf 目录遍历相关规则  
modsecurity_crs_45_trojans.conf webshell 相关规则  
modsecurity_crs_47_common_exceptions.conf Apache 异常相关规则  
modsecurity_crs_49_inbound_blocking.conf 协同防御相关规则  
modsecurity_crs_50_outbound.conf 检测 response_body 中的错误信息，警告信息，列目录信息  
modsecurity_crs_59_outbound_blocking.conf 协同防御相关规则  
modsecurity_crs_60_correlation.conf 协同防御相关规则

**第二规则：SLR 规则集**

来自确定 APP 的 PoC，不会误报，检测方法是先检查当前请求的文件路径是否出现在 data 文件中，若出现再进行下一步测试，否则跳过该规则集的检测  
modsecurity_crs_46_slr_et_joomla_attacks.conf JOOMLA 应用的各种漏洞规则  
modsecurity_crs_46_slr_et_lfi_attacks.conf 各种 APP 的本地文件包含相关规则  
modsecurity_crs_46_slr_et_phpbb_attacks.conf PHPBB 应用的各种漏洞规则  
modsecurity_crs_46_slr_et_rfi_attacks.conf 各种 APP 的远程文件包含相关规则  
modsecurity_crs_46_slr_et_sqli_attacks.conf 各种 APP 的 SQL 注入相关规则  
modsecurity_crs_46_slr_et_wordpress_attacks.conf WORDPRESS 应用的各种漏洞规则  
modsecurity_crs_46_slr_et_xss_attacks.conf 各种 APP 的 XSS 相关规则  
  

**第三规则：可选规则集**

modsecurity_crs_10_ignore_static.conf 静态文件不过 WAF 检测的相关规则  
modsecurity_crs_11_avs_traffic.conf AVS（授权的漏洞扫描器）的 IP 白名单规则  
modsecurity_crs_13_xml_enabler.conf 请求体启用 XML 解析处理  
modsecurity_crs_16_authentication_tracking.conf 记录登陆成功与失败的请求  
modsecurity_crs_16_session_hijacking.conf 会话劫持检测  
modsecurity_crs_16_username_tracking.conf 密码复杂度检测  
modsecurity_crs_25_cc_known.conf CreditCard 验证  
modsecurity_crs_42_comment_spam.conf 垃圾评论检测  
modsecurity_crs_43_csrf_protection.conf 与 modsecurity_crs_16_session_hijacking.conf 联合检测，使用内容注入动作 append 注入 CSRF Token  
modsecurity_crs_46_av_scanning.conf 使用外部脚本扫描病毒  
modsecurity_crs_47_skip_outbound_checks.conf modsecurity_crs_10_ignore_static.conf 的补充  
modsecurity_crs_49_header_tagging.conf 将 WAF 规则命中情况配合 Apache RequestHeader 指令注入到请求头中，以供后续应用进一步处理  
modsecurity_crs_55_application_defects.conf 安全头 (X-XSS-Protection,X-FRAME-OPTIONS,X-Content-Type-Options) 设置, 安全 Cookie 设 置（Domain，httponly,secure)，字符集设置等规则  
modsecurity_crs_55_marketing.conf 记录 MSN/Google/Yahoo robot 情况  

**第四规则：实验性规则集**  

modsecurity_crs_11_brute_force.conf 防御暴力破解相关规则  
modsecurity_crs_11_dos_protection.conf 防 DoS 攻击相关规则  
modsecurity_crs_11_proxy_abuse.conf 检测 X-Forwarded-For 是否是恶意代理 IP，IP 黑名单  
modsecurity_crs_11_slow_dos_protection.conf Slow HTTP DoS 攻击规则  
modsecurity_crs_25_cc_track_pan.conf 检测响应体 credit card 信息  
modsecurity_crs_40_http_parameter_pollution.conf 检测参数污染  
modsecurity_crs_42_csp_enforcement.conf CSP 安全策略设置  
modsecurity_crs_48_bayes_analysis.conf 使用外部脚本采取贝叶斯分析方法分析 HTTP 请求，区分正常与恶意请求  
modsecurity_crs_55_response_profiling.conf 使用外部脚本将响应体中的恶意内容替换为空  
modsecurity_crs_56_pvi_checks.conf 使用外部脚本检测 REQUEST_FILENAME 是否在 osvdb 漏洞库中  
modsecurity_crs_61_ip_forensics.conf 使用外部脚本收集 IP 的域名、GEO 等信息  
modsecurity_crs_40_appsensor_detection_point_2.0_setup.conf APPSENSOR 检测设置文件  
modsecurity_crs_40_appsensor_detection_point_3.0_end.conf APPSENSOR 检测设置文件  
modsecurity_crs_16_scanner_integration.conf 对扫描器设置 IP 白名单，并调用扫描器 API 来进行检测  
modsecurity_crs_46_scanner_integration.conf 使用 modsecurity_crs_40_appsensor_detection_point_2.0_setup.conf，modsecurity_crs_40_appsensor_detection_point_3.0_end.conf 来跟踪 XSS 漏洞参数与 SQLI 漏洞参数  
modsecurity_crs_40_appsensor_detection_point_2.1_request_exception.conf 使用外部脚本检测请求方法，参数个数，参数名字，参数长度，参数字符等限制  
modsecurity_crs_40_appsensor_detection_point_2.9_honeytrap.conf 使用隐藏参数设置蜜罐  

**检测模式**  

===========

**a. 传统检测模式**

传统检测模式是默认的检测模式。所有的规则逻辑都是独立的。规则之间不会互相协作，且规则不知道前面的规则匹配了什么。规则仅仅使用它自己的逻辑进行检测。在这种模式下，如果匹配了一个规则，就会根据该规则进行阻断或记录日志。

如果需要配置 mod_security 以传统的模式运行，可以将配置文件的 SecDefaultAction 是否使用了如 deny 的干扰动作。

在这种情况下，当请求匹配到一条规则后则直接会拒绝访问，同时告警信息会记录在日志中。

传统检测模式的优缺点：

优点：很容易理解逻辑；提高性能。

缺点：不便于管理；一个意外可能导致全站崩溃；当规则更新时，难以更新规则。  

**b. 异常权值模式**

在这种模式下，检测逻辑从规则的阻断功能中解脱出来。单独的规则依然能够检测，但是匹配到规则后不是直接执行干扰的动作，而且会累加到请求异常权值之中。另外，会在一个临时的请求变量中存储每条规则匹配的元数据。  
如果想让 mod_security 以异常权值模式运行，可以将配置文件的 SecDefaultAction 修改为 pass 的干扰动作。

新的模式下，匹配规则不会直接阻断，而是使用 modsecurity 的 setvar 动作累加异常权值。

### **c. 开启 / 关闭阻断模式**  

SecRuleEngine 指令可以让你打开阻断模式（on）或者只打开检测模式（DetectionOnly）.

配置了异常权值模式，当想打开阻断模式，需要设置 SecRuleEngine On， 如果只使用检测模式，需要配置为 DetectionOnly。  

设置异常权值  
-> "vi modsecurity_crs_10_config.conf"  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxGE3qRzHwcl1DPra9lKg5v7Pdf5nr9ZLyC6dbJlF7K73ruD6XqJfmsg/640?wx_fmt=png)

调整模式 使用异常权值模式  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxRa9esk1N55zRZYaDrnoiaKfZmNuGrl0qX4ib00aWTvk5iaAiaEzOb3JNAA/640?wx_fmt=png)

调整入站出站分值  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxN0rmDiaruzu87PkmupQ9BJPCEUJIrlQDJIribZxNwI0MHLasbBWgLbxQ/640?wx_fmt=png)

打开阻断  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxm9ztd3o7IBLxFIPqu5h5pEBvacYCHfKbGianuqjOjmIPzN4I4U3gpkg/640?wx_fmt=png)

保存后并重启阿帕奇  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxeQd0qKqfSbcicbZ3aADO2QBlYWjTPZ3OnY49aMQC7ZROdLlibKiaicGpcg/640?wx_fmt=png)

我们可以通过日志查看到异常权值是如何变化的 -> "tail -f /var/log/httpd/modsec_audit.log"  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxw0nUiaYHLJIfSf64brt9BiabKmBomcoaHbJzHWiaZuPn4nC0qfTnKy2hQ/640?wx_fmt=png)

检测到一个 一个参数值 id 检测到的规则是 sql 注入规则 在 64 行 id 是 981318  
打印出一个日志 有人在进行 sql 注入 检测到的数字是 1'  

Message: Warning. Pattern match "(^[\"'`\xc2\xb4\xe2\x80\x99\xe2\x80\x98;]+|[\"'`\xc2\xb4\xe2\x80\x99\xe2\x80\x98;]+$)" at ARGS:id. [file"/etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_41_sql_injection_attacks.conf"] [line "64"] [id "981318"] [rev "2"] [msg "SQL Injection Attack: Common Injection Testing Detected"] [data "Matched Data:' found within ARGS:id: 1'"]

因为我设置的进站分值为 10 它检测出来的规则是 10 分 所以就导致访问被阻断了  
Message: Warning. Operator GE matched 10 at TX:inbound_anomaly_score. [file "/etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_60_correlation.conf"] [line "37"] [id "981204"] [msg "Inbound Anomaly Score Exceeded (Total Inbound Score: 10, SQLi=6, XSS=0): 981242-Detects classic SQL injection probings 1/2"]

**分值不能大了或者小了 大了会导致 waf 没用 小了会影响 web 的业务**

如果想要调整异常权值，来减少对正常用户的请求阻断，可以提高入站的阈值, 当某些规则与我们的网站冲突很严重的情况下，我们可以选择注释掉规则, 所以我们需要调整成只使用检测模式 把模式配置成 DetectionOnly 

进入到主配置文件内 设置 SecRuleEngine On 为 DetectionOnly  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxsg7GjrcQNITr1rofYicJyfNwO7pHX1vicWLiblPic9iclAsRJLK6KqW4TIw/640?wx_fmt=png)  

然后重启服务  

**实际场景中遇到问题**

waf 与 网站有冲突

有条规则每一个页面正常访问都会报一个分值, 每人都加 5 分, 所以我们注销规则, 总的分值减掉 5 分

**  
注销规则**  

  
**第一种方式：**  

SecRuleRemoveById 指令：

在规则文件中加入这一条命令  

通过 Rule ID 禁用指定规则

#waf whitelist

<LocationMatch .*>

SecRuleRemoveById 960017 #allow Host Header is a IP address

</LocationMatch>

**第二种方式：规则前加#**

**第三种方式：针对位置注销。**

查看日志发现 981242 这条规则是检测到 1' 放在 args id 后面

[file"/etc/httpd/modsecurity.d/activated_rules/modsecu-  

rity_crs_41_sql_injection_attacks.conf"] [line"237"] [id"981242"]  

[msg "Detects classic SQL injection probings 1/2"] [data "Matched  

Data: 1'found within ARGS:id: 1'"]  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxXJPJIkvDNdBEQ6zGGp4szlENfSyEUbLbrUVAwAnC4z0InLhX8SnqQg/640?wx_fmt=png)

我们告诉 waf 不检测 id  
**编辑规则文件**  
"vi/etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_41_sql_injection_attacks.conf" 我们在这个规则中加入 |!ARGS:/id/|  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWx6M3w0Al2kiaJg1JETnJd8ELX1hNePM0S79z6HUndThfiaYybdJDr6YOA/640?wx_fmt=png)

然后重启服务

然后我们在观察日志 看看这个规则的分值还会加吗？

没有找到那条规则 并且分值也由 10 分降低至 5 分  

![](https://mmbiz.qpic.cn/mmbiz_png/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxOf6JFHCyuZXPtyFczTAictVxPyePEOibyKH3jHHonD3apIV84ooKKH2g/640?wx_fmt=png)

注销规则尽量保持好防护功能  

![](https://mmbiz.qpic.cn/mmbiz_gif/N87TJFr6bicHia6znSFczIBE2wS7CwgYWxoB1PV9F9szut9J0ETkbpYbNNnAJvjRrLt0WoXpcwjgyopswhPzssOw/640?wx_fmt=gif)

15. 当然我们都知道，**攻防重来都是一个动态的模式**，对于绕 waf，笔者也总结过几种方式，希望能帮到你们：

(1) 目录扫描绕过 waf（修改 UA 为百度 UA 进行绕过）

(2) 大小写变种

(3) 使用 sql 注释

(4) 使用 URL 编码

(5) 使用空字节

(6) 使用嵌套

(7) 使用非标准入口点

(8) 避开自定义扫描器

(9) sqlmap 注入绕过 waf 一般可以使用－tamper-.py 脚本绕过，可以自己写绕过规则

(10) 使用％00 截断绕过，有些网站认可空字节可能会绕过

同时我们还应该考虑免杀以及 webshell 管理器连接流量绕过 waf，上传绕 waf，提权绕开 waf 等因素。  

  

**总结：**

对于 waf 我们应该定时更新规则，并且我们同时也应该关注 waf 是否对业务造成误伤，前期的调试磨合很重要，毕竟公司得靠业务挣钱，离开业务谈安全都是行不通的。

  

本文选自 : https://www.freebuf.com/sectool/256502.html