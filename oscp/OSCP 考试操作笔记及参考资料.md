> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/H9w9vP9VtLTEKd0iwlRjjA)

[![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfdvuhDianSK18U8QvWTC1smjictCEibz7FOLcXD4geBCcOWe8OILoRNOmxBAibnvnnq8FBmCuvYHc5waw/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzI5MDQ2NjExOQ==&mid=2247494461&idx=1&sn=2c4d86a41041df8970eb58b8d6e4be4f&chksm=ec1ddb15db6a5203313fdda2545255d801111c1a10475bdedb425b0017417c63cad6b1ab0a07&scene=21#wechat_redirect)

OSCP 认证，是一个专门针对 Kali Linux 渗透测试培训课程的专业认证。该认证机构声称，OSCP 认证是一个区别于所有其它认证的考试，考试全程采取手动操作的方式，而不设笔试环节。  

每个 OSCP 考生，都拥有 24 小时的时间（实际是 23 小时 45 分钟）去完成考试，具体如何分配时间由考生自己决定。题目是 5 台主机（随机抽取），目标是攻入并拿到最高权限（ROOT/SYSTEM）。基于难度级别，成功执行的攻击会获得相应的积分。

以下是我用于测试目标实验机器的具体步骤，在考试期间这些都可以放入自动化代码中。

1、Nmap 基本扫描

> Nmap -Pn -p- -vv 
> 
> Nmap -Pn -p- -sU -vv 

2、针对端口指纹和漏洞的扫描

> Nmap -Pn -sV -O -pT:{TCP ports found in step 1},U:{UDP ports found in step 1} -script _vuln_ <ip address>

使用 NC 查看 banner

> nc -nv <ip-address> <port>

3、针对 web 端口的枚举

> Nikto -port {web ports} -host <ip address> -o <output file.txt>

目录扫描

> Dirb http{s}://<ip address>:<port> /usr/share/wordlist/dirb/{common/small/vulns}.txt

> Gobuster -u http://<ip-address> -w /usr/share/Seclists/Discovery/Web_Content/common.txt

如果想测试文件包含漏洞，可以使用 fimap：

> fimap -u <ip-address>

4、针对已知的服务进行攻击尝试，搜索漏洞信息

> Searchsploit <service name>

漏洞来源：

> https://www.securityfocus.com/vulnerabilities

5、针对 web 页面的测试

检查页面信息，审查元素、查看 cookie、tamper 数据、可以使用 curl/wget

在线搜索资源（比如 github），如果应用程序是开源的，根据网站枚举的信息猜测版本，然后找出可能存在的风险

检查 HTTP 选项

测试输入表单参数（比如 1'or 1=1 limit 1; # AND 1' or 1=1--）

*   NULL 或 null
    
*   ',", ;, <!
    

*   中断 SQL 字符串或查询，常用于 SQL、XPath、XML 注入
    

*   -, =, +, "
    

*   用于手工 SQL 注入测试
    

*   ', &, ! , ¦ , <,>
    

*   用于找出命令执行漏洞
    

*   ../
    

*   目录穿越漏洞
    

6、针对 NETBIOS、SMB、RPC 端口的测试

> enum4linux -a <ip address>
> 
> Rpcclient <ip address> -U "" -N
> 
> Rpcinfo -p <target ip>

关于 RPC 历史漏洞的合集：

> http://etutorials.org/Networking/network+security+assessment/Chapter+12.+Assessing+Unix+RPC+Services/12.2+RPC+Service+Vulnerabilities/

以下是常用的远程测试命令

> Showmount -e <ip address>/<port>
> 
> Mount -t cifs //<server ip>/<share> <local dir> -o username=”guest”,password=””
> 
> Rlogin <ip-address>
> 
> Smbclient -L <ip-address> -U “” -N
> 
> Nbtscan -r <ip address>
> 
> Net use <ip-address>$Share “” /u:””
> 
> Net view <ip-address>

还可以使用 NMAP 的脚本测试 SMB、DCERPC、NETBIOS

7、针对 SMTP 端口的尝试

枚举用户，使用 VRFY 和 EXPN 命令

8、针对 SNMP 端口的测试

默认共享名称如：public, private, cisco, manager

使用工具：

> Onesixtyone –c <community list file> -I <ip-address>
> 
> Snmpwalk -c <community string> -v<version> <ip address>

默认 MIB：

> 1.3.6.1.2.1.25.1.6.0 System Processes
> 
> 1.3.6.1.2.1.25.4.2.1.2 Running Programs
> 
> 1.3.6.1.2.1.25.4.2.1.4 Processes Path
> 
> 1.3.6.1.2.1.25.2.3.1.4 Storage Units
> 
> 1.3.6.1.2.1.25.6.3.1.2 Software Name
> 
> 1.3.6.1.4.1.77.1.2.25 User Accounts
> 
> 1.3.6.1.2.1.6.13.1.3 TCP Local Ports

比如枚举运行的进程

> nmpwalk -c public -v1 192.168.11.204 1.3.6.1.2.1.25.4.2.1.2

9、针对 FTP 端口测试

*   anonymous 是否可以登录
    
*   如果可以登录是否可以使用 get 或 send 操作文件
    
*   使用浏览器是否可以访问，ftp://<ip-address>
    

10、密码破解

在 linux 下可以使用 unshadow 命令合并 passwd 和 shadow 文件：

> unshadow [passwd-file] [shadow-file] > unshadowed.txt

可以使用的 hash-identifier 识别 hash 类型，使用 hashcat 破解 hash

> hashcat -m 400 -a 0 <hash file> <wordlist file>

对于其他服务，可以使用 Medusa 或 hydra

> Hydra -L <username file> -P <Password file> -v <ip-address> ssh
> 
> Medusa -h <ip-address> -U <username file> -P <password file> -M http -m DIR:/admin -T 30

11、数据包抓取

使用 wireshark / tcpdump 获取目标主机的流量

> “tcpdump -i tap0 host tcp port 80 and not arp and not icmp -vv”

#### 参考资料

NMAP Cheatsheet

> https://blogs.sans.org/pen-testing/files/2013/10/NmapCheatSheetv1.1.pdf

Exploit-DB

> https://www.exploit-db.com/

Kernel Exploits 

> https://www.kernel-exploits.com/

Privilege Escalation Linux

> https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/

Linux Pentest Commands

> http://www.networkpentest.net/p/linuxunix-command-list.html

Windows Command Line Cheatsheet

> https://www.sans.org/security-resources/sec560/windows_command_line_sheet_v1.pdf

Privilege Escalation Windows:

> http://www.fuzzysecurity.com/tutorials/16.html

> http://toshellandback.com/2015/11/24/ms-priv-esc/

Windows Priv Esc cheatsheet

> http://it-ovid.blogspot.com/2012/02/windows-privilege-escalation.html

Pentest References:

> http://www.vulnerabilityassessment.co.uk/

> http://www.0daysecurity.com/penetration-testing/enumeration.html

Reverse Shell:

> https://www.asafety.fr/reverse-shell-one-liner-cheat-sheet/

> http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet

> http://bernardodamele.blogspot.com/2011/09/reverse-shells-one-liners.html

> http://www.lanmaster53.com/2011/05/7-linux-shells-using-built-in-tools/

Web Shells

> http://repository.root-me.org/Exploitation - Web/EN - Webshells In PHP, ASP, JSP, Perl, And ColdFusion.pdf

Shell Escape:

> https://speakerdeck.com/knaps/escape-from-shellcatraz-breaking-out-of-restricted-unix-shells

> https://pen-testing.sans.org/blog/2012/06/06/escaping-restricted-linux-shells

> https://null-byte.wonderhowto.com/how-to/use-misconfigured-suid-bit-escalate-privileges-get-root-0173929/

Pentestmonkey Cheat Sheets (SQL Injection)

> http://pentestmonkey.net/category/cheat-sheet

![](https://mmbiz.qpic.cn/mmbiz_gif/sGfPWsuKAfdvuhDianSK18U8QvWTC1smjLnicbphtypgvecNktJQquOiaiaeCFTZgE8vOZT9WAibHeHhExHLia2fAbFA/640?wx_fmt=gif)

点击**阅读原文**查看原文