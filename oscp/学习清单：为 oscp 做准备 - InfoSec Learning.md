> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [whale3070.github.io](https://whale3070.github.io/experience/2019/11/22/06-x/)

Offensive Security Certified Professional

参考资料：

*   [官方考试要点](https://www.offensive-security.com/documentation/penetration-testing-with-kali.pdf)
*   [oscp faq](https://blog.csdn.net/qq_34304107/article/details/87617133#_243)
*   [非常全的 oscp 备考资料](https://www.lshack.cn/656/)

考试规则
----

时间：23 小时 45 分钟考试，结束后 24 小时内编写并提交渗透测试报告。

随机抽取 5 个主机，每个主机有低权限 flag 和代表以获取最高权限的 flag，分数不一。拿到 70 分代表考试合格。

考试要准备的
------

*   护照
*   人民币 5600——8050 不等，根据购买 lab 时长而定。第一次没考过，可以续费 lab，每次续费都附赠一次考试机会。也可以直接再次考试，费用 150$ 一次。 有把握必过的人，建议购买 30 天的 lab + 考试; 没把握的人，建议购买 60 天 + 的 lab + 考试。然后推荐提交课程报告（有 5 分加分）

**考试地点**：线上 + 摄像头监考

**提交报告要求**：

*   必须在截图中展示找到的 flag 文件内容和目标的 ip；
*   在考试结束前提交 local.txt 和 proof.txt 两个 flag 到控制面板；
*   必须获得 windows 或者 linux 机器的最高权限才能获得满分。；

**禁止的事项：**

*   作弊（这个不用说了）
*   使用商业工具（msf pro、burp pro)
*   自动利用工具（sqlmap 等自动 sql 注入、db_autopwn、browser_autopwn .etc）
*   大规模漏扫工具（nessus、openvas .etc）
*   可以使用的工具：nmap 和 nmap script、nikto、burp free、dirbuster .etc

**限制事项：**

*   只能在一台机器上使用 metasploit，你可以选择用在哪一台机器上。对于非选定的机器，不能使用 msf，哪怕是测试漏洞是否存在。

如果你在选定的机器上，没有拿到权限，也不能在第二台机器上使用 msf。

但是可以在所有机器上使用以下模块：

```
multi handler监听器
msfvenom
pattern_create.rb
pattern_offset.rb
```

**考试通过条件** 满分 100 分，通过 70 分。 违反上述规则，将不得分。

考点
--

实际上都很重要，但是标重点是是要重点学习的，因为基本不会。。

1.  kali linux
2.  必要的工具
3.  被动信息搜集
4.  主动信息搜集
5.  漏洞扫描
6.  缓冲区溢出（重点）
7.  win32 缓冲区溢出利用（重点）
8.  linux 缓冲区溢出利用（重点）
9.  使用 exp
10.  文件传输（重点）
11.  提权（重点）
12.  客户端攻击
13.  web 应用攻击（重点）
14.  密码攻击
15.  端口转发和隧道（重点）
16.  msf 框架
17.  绕过杀软（重点）
18.  汇编渗透测试断点（重点）

时间分配
----

明年 6 月中旬考试。

##

*   google “VulnHub OSCP like machines”
*   hackthebox
*   根据考试大纲找资料熟练知识点，以便报名 oscp 后快速完成 pdf 上的练习，完成 10 台 lab 机器后获取 5 分加分。