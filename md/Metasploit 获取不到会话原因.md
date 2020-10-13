\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/hZG-r78Dj3vgWbhu\_0XUmg)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。  

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

 |

**前言**  

我们在用 Metasploit 进行渗透测试时经常会遇到这样的情况，已经成功执行了 Payload，但始终获取不到会话。这篇文章就来给大家讲一下获取不到会话的一些常见原因，已经知道了问题所在，至于要怎么解决就看大家自己的了，该绕的绕，该免杀的免杀！

**一般常见情况有：**

*   1、直接获取不到会话；
    
*   2、获取到会话后自动断开；
    
*   3、获取到会话但是卡住不动了。
    

  

**(1) 快速判断 Metasploit 会话完整性**

如果直接通过浏览器访问监听 IP:Port，或者是在获取会话的过程中按 Ctrl+C 键强制结束掉了，这时我们获取到的会话可能都是不完整的，即使成功得到了会话，进去之后会发现很多命令都执行不了。

这时可以通过 session 命令来快速判断我们得到的会话完整性，如果 “Information” 列中为空白则是不完整，反之则完整。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5s6m44gvt9aEEyQE42ZX6OmWicrDMibydh1tPUB4MyDicI4Rn34vbFT8vwQ/640?wx_fmt=png)

**(2) Payload 与目标系统架构不一样**

这里说的系统架构不一样是因为我们生成的 Msf Payload 是 x64，而目标系统是 x86，在执行 Payload 过程中会出现 “不是有效的 Win32 应用程序” 报错，所以无法获取到会话。

这种情况一般出现在 XP/2003 机器上，不过 x86 的 Payload 可以在 x64 上成功运行，不存在兼容性问题。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5s9ZPzJSBDaXtGlZMhyrQMpTLYJ5qPgNau9hWdjcibW4MlT2jADEYicMnA/640?wx_fmt=png)

**(3) Payload 与监听模块设置不一样**

我们生成的 Msf Payload 是 x86 的，但是在 handler 监听模块里设置的 Payload 为 x64 时就会出现这种会话自动断开的情况。

不过在这种情况下如果 Payload 是可执行的，我们只需要将 handler 监听模块里设置的 Payload 改为对应的 x86 即可解决。

**重点注意：**

*   1、目标系统架构；
    
*   2、Msfvenom 生成 Payload；
    
*   3、handler 监听模块 Payload。
    

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5sC56U6KPzfGMPhibtMf9dmQSj6ru5n2mFMfSoGQ9bILntTynTxt6ysbQ/640?wx_fmt=png)

**(4) 目标配置系统防火墙出入站规则**

有时会遇到这样的情况，即使我们生成的 Msf Payload、handler 监听模块 Payload 和目标系统架构都是相对应的，但在执行 Payload 时仍然获取不到会话。

这可能是因为目标已开启 Windows 自带防火墙并设置了出入站规则，也有可能是被其它流量监测类的安全设备所拦截，可以通过 netstat -ano 命令来查看我们执行的 Payload 与目标机器建立的网络连接状态是否为 SYN\_SENT？  

**SYN\_SENT 的几种常见情况：**

*   1、MSF 里没有监听；
    
*   2、Windows 系统防火墙；
    
*   3、其它的安全设备等。
    

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5sQicRh13UDXOib6HiaybnJ8JRhibkG3GGgwFsDZOuPCCiceckJukt3xgouOA/640?wx_fmt=png)

**(5) VPS 配置系统防火墙出入站规则**

记一次与朋友 @Sin 在他的 Centos VPS 上做测试时发现获取不到会话，在经过排查之后发现问题出在 “宝塔防火墙”，其实也就是 Centos 自带防火墙，在宝塔安装过程中会自动配置系统防火墙，默认规则只允许特定端口能出网：21、22、80、8888，如下图。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5siawibbulQ7wLHyfuo1CFh32Eoiczh77W6LPZK6OiaYxjlXoZl8eiatJuq9A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5sthBNsGMHnB332FPBC2tK8GPQDvLbCeZ49oAoLdIricFFxloTOul5XLw/640?wx_fmt=png)

**解决方案：  
**

在宝塔控制面板中没有找到关闭防火墙的相关设置选项，只能设置放行端口，不过我们可以使用以下命令来关闭 Centos 自带防火墙，或者使用默认规则中的放行端口进行 bind\_tcp 正向连接即可成功获取会话，可通过这个文件来查看防火墙规则（/etc/firewalld/zones/public.xml）。

```
1、查看防火墙状态：
firewall-cmd --state
systemctl status firewalld.service

2、开启防火墙：
systemctl start firewalld.service

3、临时关闭防火墙：
systemctl stop firewalld.service

4、永久关闭防火墙：
systemctl disable firewalld.service

5、查看所有放行端口：
firewall-cmd --list-port
```

**(6) 反病毒软件特征查杀或流量检测**

在上传、执行 Payload 文件时可能会被反病毒软件的特征、行为、内存、流量检测并查杀，笔者本地测试发现当我们把火绒 “黑客入侵拦截” 或赛门铁克 “Enable Network intrusion prevention” 开启后再执行 Payload 时就会出现发送 stage 到目标，但无法建立一个完整的会话回来，关闭后就能立即获取到目标会话，关于免杀和绕过不在本节讨论范围内。

*   特征查杀：上传的 Payload 以及各种恶意 PE 文件直接会被拦截并查杀（360 杀毒）
    
*   流量检测：成功执行 Payload 并发送 stage 到目标，但一直卡着不动（ESET NOD32）
    

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5sy2qdcuIp5vZPKHppG7reToEyvsEticuwcibc2btBO8NH3kc1laJqYHdw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5sPSJ6thHjwEgsZpElFf1KbRm2WdVkezr1iaGMEICaxWsTnUr1ZwKF6kg/640?wx_fmt=png)

**(7) IIS 应用程序池 - 启用 32 位应用程序**

以往的渗透渗透过程中遇到过在浏览器访问 Metasploit 的 Aspx Payload 秒解析，但是没能获取会话的情况。

这可能是因为目标机器的 IIS 应用程序池中设置了 “启用 32 位应用程序” 选项为 True 或 False 了，可以尝试换到 x86/x64 的 Payload 再试试看。

*   当 “启用 32 位应用程序” 选项为 True 时 Aspx Payload 32 可以获取会话，64 无法获取会话。
    
*   当 “启用 32 位应用程序” 选项为 False 时 Aspx Payload 64 可以获取会话，32 无法获取会话。
    

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5s2e1u0QxLUYhqFu07TCRiaIgvpXffGbnibefPfHTXFYalwxzZZZw0ukicg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeYYdvgHjChhbzBYuibkup5sXXWPxuMD2rfOaZHFa4BWMqiaicH1jgIXvOxFV9GJGA43ia4HNrvsYKXNQ/640?wx_fmt=png)

**【推荐书籍】**