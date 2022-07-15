> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [github.com](https://github.com/r0eXpeR/redteam_vul)

[](#红队中易被攻击的一些重点系统漏洞整理)红队中易被攻击的一些重点系统漏洞整理
=========================================

配合 EHole(棱洞)- 红队重点攻击系统指纹探测工具使用效果更佳：[https://github.com/ShiHuang-ESec/EHole](https://github.com/ShiHuang-ESec/EHole)

[](#一oa系统)一、OA 系统
-----------------

#### [](#泛微weaver-ecology-oa)泛微 (Weaver-Ecology-OA)

🔸 [泛微 OA E-cology RCE(CNVD-2019-32204)](https://xz.aliyun.com/t/6560) - 影响版本 7.0/8.0/8.1/9.0  
🔸 [泛微 OA WorkflowCenterTreeData 接口注入 (限 oracle 数据库)](https://zhuanlan.zhihu.com/p/86082614)  
🔸 [泛微 ecology OA 数据库配置信息泄露](https://www.cnblogs.com/whoami101/p/13361254.html)  
🔸 [泛微 OA 云桥任意文件读取](https://www.cnblogs.com/yuzly/p/13677238.html) - 影响 2018-2019 多个版本  
🔸 [泛微 e-cology OA 前台 SQL 注入漏洞](https://www.cnblogs.com/ffx1/p/12653555.html)  
🔸 [泛微 OA 系统 com.eweaver.base.security.servlet.LoginAction 参数 keywordid SQL 注入漏洞](https://www.seebug.org/vuldb/ssvid-91089)  
🔸 [泛微 OA sysinterface/codeEdit.jsp 页面任意文件上传](https://www.seebug.org/vuldb/ssvid-90524)  

#### [](#致远seeyon)致远 (Seeyon)

🔸 [致远 OA-A8 htmlofficeservlet getshell 漏洞](https://www.cnblogs.com/nul1/p/12803555.html)  
🔸 [致远 OA Session 泄漏漏洞](https://www.zhihuifly.com/t/topic/3345)  
🔸 [致远 OA A6 search_result.jsp sql 注入漏洞](https://www.cnblogs.com/AtesetEnginner/p/12106741.html)  
🔸 [致远 OA A6 setextno.jsp sql 注入漏洞](https://www.cnblogs.com/AtesetEnginner/p/12106741.html)  
🔸 [致远 OA A6 重置数据库账号密码漏洞](https://www.cnblogs.com/AtesetEnginner/p/12106741.html)  
🔸 [致远 OA A8 未授权访问](https://www.cnblogs.com/AtesetEnginner/p/12106741.html)  
🔸 [致远 OA A8-v5 任意用户密码修改](http://wy.zone.ci/bug_detail.php?wybug_id=wooyun-2015-0104942)  
🔸 [致远 OA A8-m 后台万能密码](https://www.cnblogs.com/AtesetEnginner/p/12106741.html)  
🔸 [致远 OA 帆软报表组件 前台 XXE 漏洞](https://landgrey.me/blog/8/)  
🔸 [致远 OA 帆软报表组件反射型 XSS&SSRF 漏洞](https://landgrey.me/blog/7/) Thinks:LandGrey  

#### [](#蓝凌oa)蓝凌 OA

暂无 (希望大佬能提供)

#### [](#通达oa)通达 OA

🔸 [通达 OA 任意文件删除 & 文件上传 RCE 分析 (2020 年 hw 8 月 0day)](https://xz.aliyun.com/t/8430)  
🔸 [通达 OA 任意文件上传 / 文件包含 GetShell](https://xz.aliyun.com/t/7437)  
🔸 [通达 OA<11.5 版本 任意用户登录](http://www.adminxe.com/1095.html)  
🔸 [通达 OA 11.2 后台 getshell](https://www.cnblogs.com/yuzly/p/13606314.html)  
🔸 [通达 OA 11.7 后台 sql 注入 getshell 漏洞](https://www.cnblogs.com/yuzly/p/13690737.html)  

#### [](#金蝶oa)金蝶 OA

🔸 [金蝶协同办公系统 GETSHELL 漏洞](https://www.seebug.org/vuldb/ssvid-93826)  

[](#二e-mail)二、E-mail
--------------------

#### [](#exchange)Exchange

🔸 [CVE-2020-17083 Microsoft Exchange Server 远程执行代码漏洞](https://srcincite.io/advisories/src-2020-0025/)  
🔸 [Microsoft Exchange 远程代码执行漏洞（CVE-2020-16875）](https://github.com/rapid7/metasploit-framework/pull/14126)  
🔸 [CVE-2020-0688_微软 EXCHANGE 服务的远程代码执行漏洞](https://xz.aliyun.com/t/7321)  
🔸 [Microsoft Exchange 任意用户伪造漏洞](https://xz.aliyun.com/t/3670)  
🔸 [Exchange 历史漏洞合集](https://sploitus.com/?query=Exchange#exploits)  

#### [](#coremail)coremail

🔸 [coremail 配置信息泄露及接口未授权漏洞](https://www.lsablog.com/networksec/penetration/coremail-info-leakage-and-webservice-unauthorization-reproduce/)  
🔸 [Coremail 的存储型 XSS 漏洞](https://www.seebug.org/vuldb/ssvid-94754)  
🔸 [Coremail 历史漏洞合集](https://sploitus.com/?query=Coremail#exploits)  

[](#三web中间件)三、web 中间件
---------------------

#### [](#apache)Apache

🔸 [Apache Solr RCE—【CVE-2019-0192】](https://xz.aliyun.com/t/4422)  
🔸 [CVE-2018-1335：Apache Tika 命令注入](https://xz.aliyun.com/t/4452)  
🔸 [Apache Axis1（<=1.4 版本） RCE](https://xz.aliyun.com/t/5513)  
🔸 [Apache Solr 模版注入漏洞 (RCE)](https://xz.aliyun.com/t/6700)  
🔸 [Apache Shiro 权限绕过漏洞 (CVE-2020-11989)](https://xz.aliyun.com/t/7964)  
🔸 [Shiro remeberMe 反序列化漏洞（Shiro-550）](https://www.cnblogs.com/sup3rman/p/13322898.html)  
🔸 [Apache 历史漏洞合集](https://sploitus.com/?query=Apache#exploits)  

#### [](#tomcat)Tomcat

🔸 [Tomcat 信息泄漏和远程代码执行漏洞【CVE-2017-12615/CVE-2017-12616】](https://xz.aliyun.com/t/54)  
🔸 [Tomcat Ghostcat - AJP 协议文件读取 / 文件包含漏洞](https://xz.aliyun.com/t/7683)  
🔸 [Tomcat 全版本命令执行漏洞 CVE-2019-0232](https://github.com/pyn3rd/CVE-2019-0232)  
🔸 [Tomcat 后台部署 war 木马 getshell](https://blog.csdn.net/weixin_43071873/article/details/109532160)  
🔸 [CVE-2016-1240 Tomcat 本地提权漏洞](https://blog.csdn.net/jlvsjp/article/details/52776377)  
🔸 [Tomcat 历史漏洞合集](https://sploitus.com/?query=tomcat#exploits)  

#### [](#weblogic)Weblogic

🔸 [CVE-2020–14882 Weblogic 未经授权绕过 RCE](https://www.cnblogs.com/Savior-cc/p/13916900.html)  
🔸 [Weblogic 远程命令执行漏洞分析 (CVE-2019-2725)](https://xz.aliyun.com/t/5024)  
🔸 [CVE-2019-2618 任意文件上传漏洞](https://www.cnblogs.com/lijingrong/p/13049569.html)  
🔸 [WebLogic XMLDecoder 反序列化漏洞（CVE-2017-10271）](https://www.cnblogs.com/xiaozi/p/8205107.html)  
🔸 [Weblogic 任意文件读取漏洞（CVE-2019-2615) 与文件上传漏洞（CVE-2019-2618）](https://xz.aliyun.com/t/5078)  
🔸 [Weblogic coherence 组件 iiop 反序列化漏洞 (CVE-2020-14644)](https://xz.aliyun.com/t/8155)  
🔸 [Weblogic 历史漏洞合集](https://sploitus.com/?query=weblogic#exploits)  

#### [](#jboss--感谢lx)JBoss 感谢 @Lx

🔸 [CVE-2017-7504-JBoss JMXInvokerServlet 反序列化](https://www.cnblogs.com/null1433/p/12704908.html)  
🔸 [JBoss 5.x/6.x 反序列化漏洞（CVE-2017-12149）](https://www.cnblogs.com/kuaile1314/p/12060366.html)  
🔸 [JBoss 4.x JBossMQ JMS 反序列化漏洞（CVE-2017-7504）](https://www.cnblogs.com/iamver/p/11282928.html)  
🔸 [JBOSS 远程代码执行漏洞](https://www.cnblogs.com/Safe3/archive/2010/01/08/1642371.html)  
🔸 [JBoss JMX Console 未授权访问 Getshell](https://www.cnblogs.com/rnss/p/13377321.html)  
🔸 [JBoss 历史漏洞合集](https://sploitus.com/?query=JBoss#exploits)  

[](#四源代码管理)四、源代码管理
------------------

#### [](#gitlab)GitLab

🔸 [GitLab 任意文件读取漏洞 CVE-2020-10977](https://github.com/thewhiteh4t/cve-2020-10977)  
🔸 [GitLab 远程代码执行漏洞分析 -【CVE-2018-14364】](https://xz.aliyun.com/t/2661)  
🔸 [GitLab 任意文件读取 (CVE-2016-9086) 和任意用户 token 泄露漏洞](https://xz.aliyun.com/t/393)  
🔸 [GitLab 历史漏洞合集](https://sploitus.com/?query=Gitlab#exploits)  

#### [](#svn)SVN

🔸 [SVN 源码泄露漏洞](https://blog.csdn.net/qq_36869808/article/details/88846945)  

[](#五项目管理系统)五、项目管理系统
--------------------

#### [](#禅道)禅道

🔸 [【组件攻击链】禅道项目管理系统 (ZenTaoPMS) 高危漏洞分析与利用](https://www.4hou.com/posts/VoOW)  
🔸 [CNVD-C-2020-121325 禅道开源版文件上传漏洞](https://blog.csdn.net/qq_36197704/article/details/109385695)  
🔸 [禅道 9.1.2 免登陆 SQL 注入漏洞](https://xz.aliyun.com/t/171/)  
🔸 [禅道 ≤ 12.4.2 后台管理员权限 Getshell](https://www.cnblogs.com/ly584521/p/13962816.html)  
🔸 [禅道 9.1.2 权限控制逻辑漏洞](https://xz.aliyun.com/t/186)  
🔸 [禅道 826 版本一定条件 getshell](https://xz.aliyun.com/t/188)  
🔸 [禅道远程代码执行漏洞](https://anquan.baidu.com/article/996)  
🔸 [禅道 11.6 任意文件读取](https://wiki.bylibrary.cn/01-CMS%E6%BC%8F%E6%B4%9E/%E7%A6%85%E9%81%93/%E7%A6%85%E9%81%9311.6%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96/)  

#### [](#jira)Jira

🔸 [Atlassian Jira 漏洞大杂烩](https://caiqiqi.github.io/2019/11/03/Atlassian-Jira%E6%BC%8F%E6%B4%9E%E5%A4%A7%E6%9D%82%E7%83%A9/)  
🔸 [Jira 服务工作台路径遍历导致的敏感信息泄露漏洞（CVE-2019-14994）](https://cloud.tencent.com/developer/article/1529135)  
🔸 [Jira 未授权 SSRF 漏洞 (CVE-2019-8451)](https://www.cnblogs.com/backlion/p/11608371.html)  
🔸 [Atlassian JIRA 服务器模板注入漏洞（CVE-2019-11581）](https://www.cnblogs.com/backlion/p/11608439.html)  
🔸 [CVE-2019-8449 JIRA 信息泄漏漏洞](https://xz.aliyun.com/t/7219)  
🔸 [遇到 Jira 时可以尝试的一些 CVE](https://twitter.com/harshbothra_/status/1346109605756116995)  
🔸 [Jira 历史漏洞合集](https://sploitus.com/?query=Jira#exploits)  

[](#六数据库)六、数据库
--------------

#### [](#redis)Redis

🔸 [Redis 未授权访问漏洞利用总结](https://xz.aliyun.com/t/256)  
🔸 [Redis 4.x RCE](https://xz.aliyun.com/t/5616)  
🔸 [redis 利用姿势收集](https://www.webshell.cc/5154.html)  
🔸 [Redis 历史漏洞合集](https://sploitus.com/?query=redis#exploits)  

#### [](#mysql)Mysql

🔸 [Mysql 提权 (CVE-2016-6663、CVE-2016-6664 组合实践)](https://xz.aliyun.com/t/1122)  
🔸 [Mysql 数据库渗透及漏洞利用总结](https://xz.aliyun.com/t/1)  
🔸 [Mysql 注入专辑](https://www.lshack.cn/596/)  
🔸 [PhpMyadmin 的几种 getshell 方法](https://www.cnblogs.com/muxueblog/p/13043768.html)  
🔸 [高版本 MySQL 之 UDF 提权](https://xz.aliyun.com/t/2199)  
🔸 [Mysql 历史漏洞合集](https://sploitus.com/?query=mysql#exploits)  

#### [](#mssql)Mssql

🔸 [Mssql 利用姿势整理 (史上最全)](https://forum.ywhack.com/thread-114737-1-1.html)  
🔸 [Mssql 数据库命令执行总结](https://xz.aliyun.com/t/7534)  
🔸 [利用 mssql 模拟登录提权](https://xz.aliyun.com/t/8195)  
🔸 [高级的 MSSQL 注入技巧](https://xz.aliyun.com/t/8513)  
🔸 [MSSQL 使用 CLR 程序集来执行命令](https://xz.aliyun.com/t/6682)  

Author:Unomi 持续更新中.......😄 欢迎 **Star**