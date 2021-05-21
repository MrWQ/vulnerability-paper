> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI0NzEwOTM0MA==&mid=2652492016&idx=1&sn=65dda868965a025bb78c2f4e6bb3ec9e&chksm=f2587343c52ffa55f3162b9aca445a2b7441b587d7b4157a1abdc976368c0bb63a92fb7ed84c&scene=21#wechat_redirect)

**STATEMENT**

**声明**

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测及文章作者不为此承担任何责任。

雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

**Oracle 体系结构**

与其他数据库不同, Oracle 引入了一个特殊的概念: 表空间 (Tablespace)。

Oracle 关系型数据库管理系统从逻辑上把数据保存在表空间内, 在物理上以数据文件的形式存储。表空间可以包含多种类型的内存区块，例如数据区块（Data Segment）、索引区块（Index Segment）等等。区块相应的由一个或多个扩展（extent）组成。数据文件就是由多个表空间组成的，这些数据文件和相关文件形成一个完整的数据库，目录下以 DBF 后缀结尾的就是数据库默认创建的表空间。此概念的引入相对与其他数据库而言，对 oracle 来说一个用户就是一个 “库”（后面会详细解释）。

**逻辑存储结构**

主要阐述 oracle 数据库内部是怎么管理数据的。

**实例、数据库、表空间、schema、表、视图之间的关系**

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsI471PzlewNFqQllZh8SrYEvHGZ5U6Qiak5W6t0OOcl19Y8gOFp49KhKw/640?wx_fmt=png)

此处说的上述六个概念，特指在 Oracle 数据库服务内，不一定适用于其他数据库服务。上图是一个简化之后关系图，不涉及段、区和块，因为这对我们了解整个体系结构帮助不大。“数据库服务” 是 Oracle 数据库提供的一切数据管理功能的总和。“实例” 是 Oracle 数据库服务提供服务所需要的逻辑容器，本质是一组进程、线程和内存。进程和线程是为了处理相关的数据而建立的，也就是为了加载并处理数据库。“数据库” 可以看做是磁盘上一堆数据库相关的文件的总和。实例和数据库可以存在 1 对 N 的关系，也就是说一个实例加载一个数据库，但是通常是 1 对 1。常见的 1 对 N 的部署场景是并行数据库（笔者没有实际操作过），一个数据库与多个实例相对应，在同一时间内，一个用户只与一个实例相联系，当一个实例出现问题时，其他自动服务，保证服务正常运行。（Oracle12c 后引入了 CDB 和 PDB 的概念，需要另做考虑，可以是一对多的概念）而表空间和 Schema 则都是用来做数据分离的，表空间更加倾向于这个表表示储存于磁盘上哪个文件，而 Schama 倾向于这个表属于哪个用户。

**服务名和 SID 的区别**

1)SID(Site ID)：一个由字母和数字组成的系统标识符用来做实例的唯一性区别，包含了至少一个应用程序的实例和数据存储设备

2) 实例 (Instance): 由一个实例数字 (或是一个引导 ID：SYS.V_$DATABASE.ACTIVATION#）表示，包含了一个操作系统程序的集合和与存储设备进行交谈的内部结构

ORACLE 实例 = 进程 + 进程所使用的内存 (SGA)

进程：负责接受和处理客户端传来的数据，如 Windows 下由 oracle.exe 进程负责分发和处理请求

SGA: 全称为 System Global Area(系统全局区域)。实际上是内存中的一片共享区域，其中包含实例配置、数据缓存、操作日志、SQL 命令、用户信息等信息，由后台进程进行共享

3) 数据库：一般指物理存储的文件，Oracle 数据库除了基本的数据文件，还有控制文件和 Redo 日志 (重做文件 + 控制文件 + 数据文件 + 临时文件)，这些文件一般存储在 $ORACLE_HOME\oradata... 路径下，后缀名为 DBF

实例和数据库的关系：

实例是临时性的，数据库是永久性的，一个数据库可以对应多个实例，而一个实例只能对应一个数据库

**物理存储结构**

Oracle 数据库中的信息在操作系统文件系统中的体现。

⚫ 控制文件 

⚪ 数据库实例启动后，通过家在控制文件来定位数据文件、Redo 文件的路径  

⚪ 路径：\path\ORADATA\ORCL\CONTROL.CTL

⚫ 数据文件

⚪ 数据文件存在状态，可通过 SQL 语句进行查询，分别是：SYSTEM、ONLINE、OFFLINE、RECOVER，其中只有 SYSTEM 表空间会有 SYSTEM 状态

⚪ 路径：\path\ORADATA\ORCL\SYSTEM.DBF

⚪ 路径：\path\ORADATA\ORCL\SYSAUX.DBF

⚪ 路径：\path\ORADATA\ORCL\UNDOTBS.DBF

⚪ ...

⚫ 临时文件

⚪ 当 Oracle 进行需要占用大内存操作时，一般是指超过内存，此时会讲数据临时存储在 TEMP 表空间作为中转，类似共享虚拟内存

⚪ 路径：\path\ORADATA\ORCL\TEMP.DBF

⚫ 日志文件

⚪ Oracle 在执行修改操作后，并不会马上将相应的字符写入数据文件，而是生成 Redo 信息，将该信息写入到内存中固定区域 LOG_BUFFER，当区域数据达到某个触发器条件是，会将该内存区域的内容写入到 Redo 日志文件中

⚪ 日志文件存在多种状态，分别为 UNUSED、CURRENT、ACTIVE、INACTIVE、CLEARING、CLEARING_CUREENT

⚪ 路径：\path\ORADATA\ORCL\REDO0.LOG

⚫ 参数文件

⚪ 记录 Oracle 数据库的基本参数信息，包括数据库名、控制文件等信息所在路径

⚪ 文件名称：SPFILEsid.ora

**数据字典**

_https://book.huihoo.com/oracle-internals/04.Dictionary.pdf_

数据字典 (Data Dictionary) 是 Oracle 数据库的一个重要组成部分，是元数据(Metadata) 的存储地点。Oracle RDBMS 使用数据字典记录和管理对象信息和安全信息等，用户和数据库 系统管理员可以通过数据字典来获取数据库相关信息。

数据字典包括以下内容:

⚫ 所有数据库 Schema 对象的定义 (表、视图、索引、聚簇、同义词、序列、过程、函数、包、触发器等等)

⚫ 数据库的空间分配和使用情况

⚫ 字段的缺省值

⚫ 完整性约束信息

⚫ Oracle 用户名称、角色、权限等信息

⚫ 审计信息

⚫ 其他数据库信息

**总之，数据字典是数据库核心，通过数据字典，Oracle 数据库基本上可以实现自解释。**

一般来说，数据字典是只读的，通常不建议对任何数据字典表中的任何信息进行手工更新或改动，**对于数据字典的修改很容易就会导致数据库紊乱，造成无法恢复的后果**，而且 Oracle 公司不对此类操作带来的后果负责。

通常所说的数据字典由四部分组成: 内部 RDBMS(X $) 表、数据字典表、动态性能 (V$) 视图和数据字典视图。作为数据字典的辅助管理，还可以为对象创建同义词。

**Schema、表空间与系统表**

**Schema**

Schema 是用户表的逻辑容器。让我们分析下 navicat 从 oracle 成功连接之后展开一级结构时候的动作

展开之后就是这样的，然而这并不是表空间

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsIsduNYmn75zZrGMKjlBYMeLKEWAVBw3xa7KjXbPsjFCRwnrxHy0yzGg/640?wx_fmt=png)

现在显示出来的每一项是不是就是表空间，为什么要显示这些？让我们通过调试 navicat 来知道它执行了哪些语句，从而揣摩出它的意图。

它首先去查了一个 sessionid，这个感觉和我们的意图无关。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsIrHpHibWWLWe6Sj1Ug48bTuQtgqaoErCpsoibCuEkP3nISa4aH1bPO5OQ/640?wx_fmt=png)

几乎每次执行语句之前都会执行这一句 

alter session set current_schema= xxx

结合此语句的意义，不难发现它的目的。这句的作用可以理解为相当于 mysql 数据库中的切换数据库，oracle 叫做切换当前模式（直译，大部分中文资料也是这个翻译，亦或译为架构），主要是提供了对架构（模式）内的对象一种简便的访问方式，不指定架构（模式）时，默认从当前架构（模式）内查找。例如，执行 alter session set current_schema= xxx，然后执行 select* from user，此时的 user 表默认从 xxx 架构下寻找。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsI3AsSSQh9jnxKV4h4KKibq3TSTY7amDZh4dC2HmUw8MePIX0FNLPMqlA/640?wx_fmt=png)

官网文档的叙述

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsIstDVrRKpF72Z8Cs1k4S0ZQBGKvpDpmepI30DeNdAvcLthk4ibB9aoxA/640?wx_fmt=png)

但是以上语句并没有出现软件界面中显示的内容，这和不足以支撑我们的推断，但是如果结合接下来这句 select username , case when (username=user) then 1 else 0 end iscurrentuser from sys.all_users;

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsIAOHzt4NNwE6CuGdIgU2Xla8O2bQyCQaNsM6Laxq4gD80QRpRnKVZAg/640?wx_fmt=png)

查看此语句的返回结果

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsI9YCssXSUI27EkmJaBnogC43xB5ZgatIZ1icGlIsy9O3Lp03kTK9D6sA/640?wx_fmt=png)

这段语句很多但是细看可以知道 navicat 首先去查了 SYS.ALL_USERS。当我们选定其中某一项的内容查看下方的叙述，navicat 将它看做一个 “数据库”。可以得出一个结论：在 oracle 中一个用户就是一个“数据库”（这里的数据库跟前文提到的代表文件的数据库不同），一个“库” 就是某一个用户架构（模式）下所有表的集合。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsIkC2D2O1HFBowTQXadmuvCeicZRHEoaSt3ibiaRY0z0CPXaT9Tib36yPBMQ/640?wx_fmt=png)

所以，打开 navicat 看到的那竖排以用户名命名的 “数据库” 既不是表空间也不是数据库，而是以用户名为命名的用户所拥有的表的集合的列表，这也就是 schema 的具体表现，我们看出，运行状态中的（也就是实例）oracle 主要用 Schema 进行数据的分离，因为 Schema 和表空间都有一个很重要的特性，就是对表的独占性。默认情况下，Schema 同用户名称相同。Schema 是表的逻辑集合，是所有应用访问表必须指定的对象（不指定的话就是默认的 schema）。

**表空间**

在 oracle 中数据库是一个整体的逻辑概念。表空间是啥

如果创建用户时，不指定其永久表空间，则会使用默认的表空间。

当 Oracle 创建数据库时，会默认创建五个表空间：

**SYSTEM：**用于存储系统表和管理配置等基本信息

**SYSAUX：**类似于 SYSTEM，主要存放一些系统附加信息，以便减轻 SYSTEM 的空间负担

**UNDOTBS：**用于事务回退等

**TEMP：**作为缓存空间减少内存负担

**USERS：**存储定义的表和数据

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUkYTBicUH0B7jbtdfAyhVsItS4FI6R0GgG0IqHOoOGJ98rQJtlkkgSG1T6J19I32ia519ria6mKUDNg/640?wx_fmt=png)

_（上图中 EXAMPLE 是安装数据库实例的表空间）_

SYSAUX 表空间做为 SYSTEM 表空间的辅助表空间，主要存放 EM 相关的内容以及表统计信息，AWR 快照，审计信息等

**系统表**

Oracle 的系统表:

**dba_tables :** 系统里所有的表的信息，需要 DBA 权限才能查询

**all_tables :** 当前用户有权限的表的信息

**user_tables:** 当前用户名下的表的信息

**DBA_ALL_TABLES：**DBA 用户所拥有的或有访问权限的对象和表

**ALL_ALL_TABLES：**某一用户拥有的或有访问权限的对象和表

**USER_ALL_TABLES：**某一用户所拥有的对象和表

user_tables 的范围最小，all_tables 看到的东西稍多一些，而 dba_tables 的信息最全

**ORACLE 的一些常用系统表说明和介绍**

_https://www.huaweicloud.com/articles/0f2cb0917e686e6de3551ea381fdb25b.html_

**dba_开头**

```
dba_tables  --用户表信息
 dba_users  --数据库用户信息
 dba_segments  --表段信息
 dba_extents  --数据区信息
 dba_objects  --数据库对象信息
 dba_tablespaces  --数据库表空间信息
 dba_data_files  --数据文件设置信息
 dba_temp_files  --临时数据文件信息
 dba_rollback_segs  --回滚段信息
 dba_ts_quotas  --用户表空间配额信息
 dba_free_space  --数据库空闲空间信息
 dba_profiles  --数据库用户资源限制信息
 dba_sys_privs  --用户的系统权限信息
 dba_tab_privs  --用户具有的对象权限信息
 dba_col_privs  --用户具有的列对象权限信息
 dba_role_privs   --用户具有的角色信息
 dba_audit_trail  --审计跟踪记录信息
 dba_stmt_audit_opts  --审计设置信息
 dba_audit_object  --对象审计结果信息
 dba_audit_session  --会话审计结果信息
 dba_indexes  --用户模式的索引信息
```

**user_开头**

```
user_objects  --用户对象信息
 user_source  --数据库用户的所有资源对象信息
 user_segments  --用户的表段信息
 user_tables  --用户的表对象信息
 user_tab_columns  --用户的表的列信息
 user_constraints  --用户的对象约束信息
 user_sys_privs  --当前用户的系统权限信息
 user_tab_privs  --当前用户的对象权限信息
 user_col_privs  --当前用户的表列权限信息
 user_role_privs  --当前用户的角色权限信息
 user_indexes  --用户的索引信息
 user_ind_columns  --用户的索引对应的表列信息
 user_cons_columns  --用户的约束对应的表列信息
 user_clusters  --用户的所有簇信息
 user_clu_columns  --用户的簇所包含的内容信息
 user_cluster_hash_expressions  --散列簇的信息
```

**v$ 开头**

```
v$database  --数据库信息
 v$datafile  --数据文件信息
 v$controlfile  --控制文件信息
 v$logfile  --重做日志信息
 v$instance  --数据库实例信息
 v$log  --日志组信息
 v$loghist  --日志历史信息
 v$sga  --数据库SGA信息
 v$parameter  --初始化参数信息
 v$process  --数据库服务器进程信息
 v$bgprocess  --数据库后台进程信息
 v$controlfile_record_section  --控制文件记载的各部分信息
 v$thread  --线程信息
 v$datafile_header  --数据文件头所记载的信息
 v$archived_log  --归档日志信息
 v$archive_dest  --归档日志的设置信息
 v$logmnr_contents  --归档日志分析的DML DDL结果信息
 v$logmnr_dictionary  --日志分析的字典文件信息
 v$logmnr_logs  --日志分析的日志列表信息
 v$tablespace  --表空间信息
 v$tempfile  --临时文件信息
 v$filestat  --数据文件的I/O统计信息
 v$undostat  --Undo数据信息
 v$rollname  --在线回滚段信息
 v$session  --会话信息
 v$transaction  --事务信息
 v$rollstat  --回滚段统计信息
 v$pwfile_users  --特权用户信息
 v$sqlarea  --当前查询过的sql语句访问过的资源及相关的信息
 v$sql  --与v$sqlarea基本相同的相关信息
 v$sysstat  --数据库系统状态信息
```

**all_开头**

```
all_users  --数据库所有用户的信息
 all_objects  --数据库所有的对象的信息
 all_def_audit_opts  --所有默认的审计设置信息
 all_tables  --所有的表对象信息
 all_indexes  --所有的数据库对象索引的信息
```

**session_开头**

```
session_roles  --会话的角色信息
 session_privs  --会话的权限信息
```

**index_开头**

```
index_stats  --索引的设置和存储信息
```

**伪表**

```
dual  系统伪列表信息  --用于查询结果和任何表没有关系的时候，用于补全sql的from
```

  

本文主要介绍了 Oracle 的体系结构，下一章我们将介绍 Oracle Java 支持、Oracle CLR 和 Oracle SQL 注入技巧。

  

  

**RECRUITMENT**

**招聘启事**

**安恒雷神众测 SRC 运营（实习生）**  
————————  
【职责描述】  
1.  负责 SRC 的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2.  负责白帽子提交漏洞的漏洞审核、Rank 评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

**设计师（实习生）**  

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；

3、精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
4、有品牌传播、产品设计或新媒体视觉工作经历；  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦 19 楼  
学历要求：本科及以上  
工作年限：1 年及以上，条件优秀者可放宽

简历投递至 

bountyteam@dbappsecurity.com.cn

安全招聘  

————————  
公司：安恒信息  
岗位：**Web 安全 安全研究员**  
部门：战略支援部  
薪资：13-30K  
工作年限：1 年 +  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
【岗位职责】  
1. 定期面向部门、全公司技术分享;  
2. 前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3. 负责完成部门渗透测试、红蓝对抗业务;  
4. 负责自动化平台建设  
5. 负责针对常见 WAF 产品规则进行测试并落地 bypass 方案  
【岗位要求】  
1. 至少 1 年安全领域工作经验；  
2. 熟悉 HTTP 协议相关技术  
3. 拥有大型产品、CMS、厂商漏洞挖掘案例；  
4. 熟练掌握 php、java、asp.net 代码审计基础（一种或多种）  
5. 精通 Web Fuzz 模糊测试漏洞挖掘技术  
6. 精通 OWASP TOP 10 安全漏洞原理并熟悉漏洞利用方法  
7. 有过独立分析漏洞的经验，熟悉各种 Web 调试技巧  
8. 熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
【加分项】  
1. 具备良好的英语文档阅读能力；  
2. 曾参加过技术沙龙担任嘉宾进行技术分享；  
3. 具有 CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP 等安全相关资质者；  
4. 具有大型 SRC 漏洞提交经验、获得年度表彰、大型 CTF 夺得名次者；  
5. 开发过安全相关的开源项目；  
6. 具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7. 个人技术博客；  
8. 在优质社区投稿过文章；

岗位：**安全红队武器自动化工程师**  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 熟练使用 Python、java、c/c++ 等至少一门语言作为主要开发语言；  
2. 熟练使用 Django、flask 等常用 web 开发框架、以及熟练使用 mysql、mongoDB、redis 等数据存储方案；  
3: 熟悉域安全以及内网横向渗透、常见 web 等漏洞原理；  
4. 对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5. 具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。

简历投递至

bountyteam@dbappsecurity.com.cn

岗位：**红队武器化 Golang 开发工程师**  

薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 掌握 C/C++/Java/Go/Python/JavaScript 等至少一门语言作为主要开发语言；  
2. 熟练使用 Gin、Beego、Echo 等常用 web 开发框架、熟悉 MySQL、Redis、MongoDB 等主流数据库结构的设计, 有独立部署调优经验；  
3. 了解 docker，能进行简单的项目部署；  
3. 熟悉常见 web 漏洞原理，并能写出对应的利用工具；  
4. 熟悉 TCP/IP 协议的基本运作原理；  
5. 对安全技术与开发技术有浓厚的兴趣及热情，有主观研究和学习的动力，具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式、消息队列等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。  
简历投递至

bountyteam@dbappsecurity.com.cn

END

![图片](https://mmbiz.qpic.cn/mmbiz_gif/CtGxzWjGs5uX46SOybVAyYzY0p5icTsasu9JSeiaic9ambRjmGVWuvxFbhbhPCQ34sRDicJwibicBqDzJQx8GIM3AQXQ/640?wx_fmt=gif)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JX1av2ACppVAI0QeqjSPTdCPpJXkaYMAlxSH7KZtiblmPBzy8TjXL6vRyAZRNJgVBwTUrkryxAJUaw/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/0BNKhibhMh8eiasiaBAEsmWfxYRZOZdgDBevusQUZzjTCG5QB8B4wgy8TSMiapKsHymVU4PnYYPrSgtQLwArW5QMUA/640?wx_fmt=gif)

**长按识别二维码关注我们**