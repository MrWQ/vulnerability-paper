# Microsoft Exchange Server远程执行代码漏洞
漏洞概述
----

Microsoft   Exchange Server存在四个远程代码执行漏洞（CVE-2021-28480、CVE-2021-28481、CVE-2021-28482、CVE-2021-28483），这些漏洞被微软标记为“Exploitation More Likely”。其中，CVE-2021-28480和CVE-2021-28481的CVSS评分为9.8分，是预身份验证的远程代码执行漏洞，这意味着攻击者无需向易受攻击的Exchange服务器进行身份验证即可利用此漏洞。

CVE-2021-28480/CVE-2021-28481: 在未授权且无需用户交互的情况下可以通过此漏洞进行远程代码执行。

CVE-2021-28482/CVE-2021-28483: 在授权且无需用户交互的情况下可以通过此漏洞进行远程代码执行。

影响范围
----

Microsoft Exchange Server 2019 Cumulative Update 8

Microsoft Exchange Server 2019 Cumulative Update 7

Microsoft Exchange Server 2016 Cumulative Update 19

laMicrosoft Exchange Server 2016 Cumulative Update 18

Microsoft Exchange Server 2013 Cumulative Update 23

检测
--

以下目录下是否存在可疑WebShell文件

IIS服务目录：

    C:\inetpub\wwwroot\aspnet_client\
    C:\inetpub\wwwroot\aspnet_client\system_web\

Exchange Server安装目录：

    %PROGRAMFILES%\Microsoft\Exchange Server\V15\FrontEnd\HttpProxy\owa\auth\
    C:\Exchange\FrontEnd\HttpProxy\owa\auth\

可疑WebShell文件名称：

    web.aspx、help.aspx、document.aspx、errorEE.aspx、errorEW.aspx、errorFF.aspx、healthcheck.aspx、aspnet_www.aspx、aspnet_client.aspx、xx.aspx、shell.aspx、aspnet_iisstart.aspx、one.aspx等

C:\\ProgramData\\目录下是否有可疑压缩文件（\*.zip \*.rar \*.7z）

以下目录是否存在可疑LSASS Dump凭据文件

    C:\windows\temp\
    C:\root\

OWA服务概述
-------

通过访问Outlook Web Access页面，邮箱用户不需要安装Outlook2007客户端软件，直接使用 Web 浏览器通过 Internet 读取或发送电子邮件、管理他们的日历地址簿，任务等协同办公功能。

后来Outlook Web Access改名为Outlook Web App。

禁止外网访问OWA服务
-----------

可以在Server Manager Wizard，“IIS安全性”中添加“IP和域限制”功能来限制用户从外网访问。

![](Microsoft%20Exchange%20Server%E8%BF%9C%E7%A8%8B%E6%89%A7%E8%A1%8C%E4%BB%A3%E7%A0%81%E6%BC%8F%E6%B4%9E/1457425.png)

在IIS Manager中分别对owa、mapi和Rpc目录访问进行限制,选择IP and Domain Restrictions，将内部子网添加到“Allow IP address range”，

![](Microsoft%20Exchange%20Server%E8%BF%9C%E7%A8%8B%E6%89%A7%E8%A1%8C%E4%BB%A3%E7%A0%81%E6%BC%8F%E6%B4%9E/1457426.png)

打开“Edit Feature Settings”,将默认访问设置为“Deny”，从而实现仅允许内网访问OWA和Outlook，阻止外部IP地址访问。

![](Microsoft%20Exchange%20Server%E8%BF%9C%E7%A8%8B%E6%89%A7%E8%A1%8C%E4%BB%A3%E7%A0%81%E6%BC%8F%E6%B4%9E/1457423.png)