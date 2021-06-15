> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/k1X4TR0c0xq-ND12SEMm9Q)

**在某爱论坛上看到有个师傅写了个 Crackme**

**关于如何绕过 IsDebuggerPresent 的反调试的, 闲来无事复现调试一下**

**先上原文链接:****https://www.52pojie.cn/thread-1432590-1-1.html**

**反调试**

**什么是反调试技术**

*   反调试技术，顾名思义就是用来防止被调试的一种技术
    
*   简单的反调试往往是识别是否被调试，如果是则退出程序，封禁账号等等    （检测）
    
*   再复杂些可以在反汇编代码中插入花指令，使调试器的反汇编引擎无法正确解析反汇编指令（干扰）
    
*   门槛较高的反调试则可以是从驱动层将调试权限清零，使得调试器失效等等   （权限清零）
    
*   反调试的手段可以大致归纳为：检测、干扰、权限清零 三种
    

**反调试常见手段**

反调试手段层出不穷，可以分为两类：

*   0 环, 内核级调试
    
*   3 环, 用户应用层调试
    

之前写对抗沙盒的时候: 判断父进程是否是 explorer.exe, 不是则退出, 似乎也可以作为一种简单的反调试手段, 之前没怎么了解过反调试, 最多听海哥说过可以检查句柄表, 今天就学习一下, 先看看 windows 的反调试 API，0 环反调试等以后知识储备够了再学习

**IsDebuggerPresent**

https://docs.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-isdebuggerpresent

确定调用过程是否正在由用户模式调试器调试。

**CheckRemoteDebuggerPresent**

https://docs.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-checkremotedebuggerpresent

确定是否正在调试指定的进程。

**开始调试**

打开就是一个人畜无害的样子

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOhwzzoNY2fvicTicVa72W1vXRUHKkGmedN8hkDSl8rWX7z7l7t9icqu6Og/640?wx_fmt=png)

**查壳**

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOg0uuGwsqdTajcsGDSmrnRsqRrnDWwyt07bkeODHibEiagzwH6icGVqqlg/640?wx_fmt=png)

64 位, MFC 做的, c++ 写的, 没壳  

**ASLR**

**什么是 ASLR**

维基百科: 在计算机科学中，**地址空间配置随机加载**（英语：Address space layout randomization，缩写 ASLR，又称**地址空间配置随机化**、**地址空间布局随机化**）是一种防范内存损坏漏洞被利用的计算机安全技术。ASLR 通过随机放置进程关键数据区域的地址空间来防止攻击者能可靠地跳转到内存的特定位置来利用函数。现代操作系统一般都加设这一机制，以防范恶意程序对已知地址进行 Return-to-libc 攻击。

总的来说就是将内存地址虚拟化, 我们看到的内存地址并不是真正的内存地址偏移

**ASLR 的作用**

地址空间配置随机加载利用随机方式配置数据地址空间，使某些敏感数据配置到一个恶意程序无法事先获知的地址，令攻击者难以进行攻击

粗俗地说，就是使得每次调试工具（如 OD、x64dbg 等）加载程序后，地址是随机动态分配的，无法使用固定的地址进行定位

**ASLR 的体现**

用 x64 debug 打开程序

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOKxZ1mhiagkPS85bpcibVROLZUbqoobQsso10ibBhXrtuWBwrJF3gCfwvA/640?wx_fmt=png)

到达系统断点, 我们需要让他到达 oep, 即程序入口点  

ALT+F9

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO6icYG2WgsxCl7x7jT1A3qyIptiaaJ91vZv9NZ4pMbxxfLfKlJARz11ibg/640?wx_fmt=png)

这里地址是 7FF6E.....  

再看真实的入口点:

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOK2dXuCzicYia9pl25wfJJtW4TwJibWlBxZ8uks0mRR5yFcaKRbJeA8aGg/640?wx_fmt=png)

明显不一样  

**用 MFC 编译出的 64 位程序默认是开启 ASLR 的**

**关闭 ASLR**

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOUOZbbRUDz7I6Q1738F0bEqI2hgJemibLfQUuibkYhOykKm9LnrMW0HIg/640?wx_fmt=png)

找到可选 pe 头的 DllCharacteristics 属性, 取消 DYNAMIC_BASE  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOZQic3u8IC62xjJGzYiaYBWP7ucRpajPIzodhcxuyhf0rrE7ORN45OYgA/640?wx_fmt=png)

回到真正的内存偏移  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOTMUP0ichicMYFFdU2rTDJx6LyfrDib5T1Dic3ichEE1xL2pnIE2SrwUaMiaQ/640?wx_fmt=png)

关于 DllCharacteristics 可以参考:

https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_optional_header64  

**x64 反调试**

F9 让程序运行, 但是一运行程序就会直接结束, 不会弹出窗口

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOUAMhzAT2GmbBrq0qFcBibNEr1tB950QU7oyQRecqRsKIN5Nffne4GjA/640?wx_fmt=png)

 做到这里不禁让我想到直接写反杀箱的时候一样, 一运行就挂

大概代码是这样:

```
if (explorer_id == parent_id)
{
CeatRemoThread(explorer_id);
}
else
{
exit(1);
}
```

只不过他这里是其他判断, 比如是否被调试, 是就直接 exit, 不是则执行下面的

于是对 ExitProcess 下断点

bp ExitProcess

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOHgXeicEH2Vjmmr03jvkRmaBvvQE4WGAvshGCS06BN9mOVPosJ4blhoQ/640?wx_fmt=png)

下断点后直接 F9 运行到断点处  

观察此时的堆栈

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO72IMnyC1XBVVhbgfg1Aib98hU9Nl4m49CyRDBKnGQt0hOEp4GFGicAwA/640?wx_fmt=png)

这里又返回到 crakeme, 猜想是否是判断是否在调试之后又回到原本的函数  

选中这一行按回车, 跟进反汇编

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOhFYyOJhTmS9qibnK5G2FowxBcUKvcKicBnjDLj8UYDFV26Mz0J8459Ww/640?wx_fmt=png)

看到使用了 IsDebuggerPresent 来反调试

**IDA Pro x64 反调试**

进入 ida 后, 按 G, 并输入刚刚反汇编开始的地址

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO8EwcYedIPBTxhNltXxZVK2v6cVNLDGMnYIgMrw8eNgHcGOW7dTWlQA/640?wx_fmt=png)

跳转后

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOvJP4N7rZulCpicGNFS6ZAB8fiblwbfESrTrgPRmiadM6W2jme0QnKcNbg/640?wx_fmt=png)

选择 startaddress  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOONWiavEaTn8kUFSg8GFFBtVnIFgcibqV9BptlLKk0TKZcc1CGFRE2Qwdg/640?wx_fmt=png)

F5 进入伪代码  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOa45qQH12a5SnhBiapJKGcNte5U0YKAqcZiawIEkMOMLU4l0sOFvb8dhQ/640?wx_fmt=png)

这里很明确了, 就是这个在反调试

**IDA pro 反反调试处理**

可以直接在函数头部就直接 ret, 让他不走 IsDebuggerPresent

这里要用到 IDA Pro 的 KeyPatch 功能：

选中函数的头部，然后右键 → Key Patch → Patch：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOOswy7npH32d4V72kIFwibUtm24Dw5GwSK4KCbPvxohJfoKdVJKkbnhQ/640?wx_fmt=png)

接下来要将 Patch 完的结果导出到文件：

Edit→ Patch Program → Apply patches to input file

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO8AVXggBeLeCupmgibnsB2VPsgJI6iciajz55s692UicW9tLyib0ylQibqtXw/640?wx_fmt=png)

OK 即可  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO91QFb7Upgcicfq2fgClQdnxlHuCJCxlEYf3gnT7cJiaCCPLXZGoLElLA/640?wx_fmt=png)

**验证反反调试处理**

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOYmqs41by8nicZURbprKgD3zTusKhDmbyRBrESYVqKGpJ7a2v1ibtnWFg/640?wx_fmt=png)

**正式 Crack**

先随便输入一个数看看

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOrwn5GEQDSyyXoG2ibQYAGO1JkydGQWJMj9kD9Dl8htibkfLUd2bYRG7g/640?wx_fmt=png)

本来这里可以搜索字符串, 但我发现定位有些问题  

换一种思路, 定位 API, 以前写 win32 程序的时候, 要想在 dialog 中输出一段字符串, 用 SetWindowText, 这里可以用这个 api 定位

bp SetWindowTextW

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO4vAtg2YFA86bhby49OYL2LACvjrtAClOTn1reSUUyCDKpNluxlgib3A/640?wx_fmt=png)

回车, 断点就设置好了  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOqOpfWsVuYyfo6sBDia3DhKHsXSCOsPMnEria9j4TKWQvYhY3hWTW4z6g/640?wx_fmt=png)

然后再点确定  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOC3fKOE1nPTKgVADtEq5NcUtdqJzz4b9R6jWEMk4fDJ8Y9HxpphBicDw/640?wx_fmt=png)

观察此时堆栈, 出现了 100 和密码错误, 并且有个返回函数  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO5bTC35LA052kqcXKcaH1dTibFJk5OtSJTVD9wcelqB1nibCmicNyxdibbw/640?wx_fmt=png)

选中返回函数那一行，回车  

找到附近的 "密码正确"

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOsp2dInX3iapHFf3O9ThWSqSTe4YD1eTPGoKV23NHjicpptiaWcibspCVMw/640?wx_fmt=png)

**IDA Pro 分析**

跳转到刚刚 "密码正确的地址"

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO2iaNIZmtoy2hNnzA8bycicoTfLdck3ZZbb0icXT4fTibmOlicWG0In7vvsA/640?wx_fmt=png)

  选中函数头部 F5, 进入伪代码

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOBicnXWcvIl7B0MIGvDiamzvQuodqm7NqT4bvQRL8OoMyy9xOPfYsC9dw/640?wx_fmt=png)

得到:

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOZQhz5SyScq6euEaSsLAm1Zkw6jtmTYibiaCXtkD5s4XtBjF1mSzggzSg/640?wx_fmt=png)

说实话, 这个伪代码不是很能直接看得懂, 看了下原作者的, 他调试的是 Debug 版的, 更这个 release 版的还是有差别的, 感觉 release 版 ida 很多都识别不了了  

附上作者关于密码的源代码

```
void encodeCString(CString str) {                   //简单的字符串加密函数
for (int i=0;i<str.GetLength();i++)
{
str.SetAt(i, -str[i]);                      //简单的加密
}
}


CString correctStr = L"密码正确";
CString errorStr = L"密码错误";
CString debugStr = L"检测到被调试";
void CMFCApplication2Dlg::OnBnClickedButton1()      //按钮"确定"的响应事件
{


// TODO: 在此添加控件通知处理程序代码
//获取到edit1的内容 然后给edit2赋值
CString str;
edit1.GetWindowTextW(str);                  //获取输入的密码


WCHAR out[1024];
CString strList[4];
CString correctList[4];                     //用来存放正确的密码，后面拿来比较
BOOL flag = TRUE;                           //标志，用来标记密码是否正确
correctList[0] = "016";
correctList[1] = "025";
correctList[2] = "666";
correctList[3] = "332";


encodeCString(correctStr);                  //简单的加密
encodeCString(errorStr);                    //简单的加密
encodeCString(debugStr);                    //简单的加密


long t1 = GetTickCount64();                 //获取开始时间


if (str.GetLength() > 25 || str.GetLength() < 15) {       //字符串长度判断
flag = FALSE;
encodeCString(errorStr);
GetDlgItem(IDC_STATIC)->SetWindowTextW(errorStr);
}
else {
//password
//610 - 520 - 666 - 233
CString sToken = _T("");                            //用来接收每次分割的字符串
int i = 0; // substring index to extract
while (AfxExtractSubString(sToken, str, i, '-'))    //以-进行分割
{
//..
//work with sToken
//..


strList[i] = sToken.Trim();                     //字符串去空格
i++;
if (i > 4) {                                 //如果分割大于4，则不满足条件
flag = FALSE;
encodeCString(errorStr);
GetDlgItem(IDC_STATIC)->SetWindowTextW(errorStr);
break;
}
}
if (i != 4) {                                       //如果分割不等于4，不满足条件
flag = FALSE;
encodeCString(errorStr);
GetDlgItem(IDC_STATIC)->SetWindowTextW(errorStr);
}
else {
for (i = 0; i < 4; i++) {
//比较字符串
if(strList[i].CompareNoCase(correctList[i].MakeReverse())==-1){ //注意这里的MakeReverse()
flag = FALSE;
encodeCString(errorStr);
GetDlgItem(IDC_STATIC)->SetWindowTextW(errorStr);
break;
}
}
}


}
//判断标记
if (flag) {
encodeCString(correctStr);
GetDlgItem(IDC_STATIC)->SetWindowTextW(correctStr);
}


Sleep(500);


long t2 = GetTickCount64();             //获取结束时间
if (t2 - t1 >= 560) {                    //如果时间差大于等于560则超时，是被调试的情况
encodeCString(debugStr);
GetDlgItem(IDC_STATIC)->SetWindowTextW(debugStr);
}


}
```

可以看到跟 ida 生成的伪代码差距还是比较大, 但还是不影响用源码分析一波算法

1. 通过 GetTickCount64 获取自系统启动以来经过的毫秒数, 变量 t1

GetTickCount64:https://docs.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64

2. 获取输入的密码长度, 如果长度小于 15, 或大于 25, 就赋值 flag=false, 然后 SetWindowText"密码错误", 并且可以看到这个字符串是由 encodeCString 加密了的, 所以如果一开始如果想直接找字符串，可能就无法准确定位

3.AfxExtractSubString:https://docs.microsoft.com/en-us/cpp/mfc/reference/cstring-formatting-and-message-box-display?view=msvc-160

这个 API 可用于从给定的源字符串中提取子字符串, 通过这个 api 的返回值可以判断有几个 "-"，如果是 4 段密码, 且以 “-” 分割, 就可以进入比较字符串环节

4.CompareNoCase:https://docs.microsoft.com/en-us/windows/win32/api/chstring/nf-chstring-chstring-comparenocase

该函数这个函数使用 lstrcmpi 函数对一个 CString 和另一个 CString 进行比较

返回值为:

**由参数 lpsz 指定这个用于比较的 string。如果两个对象完全一致则返回 0，如果小于 lpsz，则返回 - 1，否则返回 1.**

这里不等于 - 1 就行, 也就是不小于

5.MakeReverse:https://docs.microsoft.com/en-us/windows/win32/api/chstring/nf-chstring-chstring-makereverse

功能大概就是反转字符串, 所以四个数为 610，520，666，233

6. 最后有一个计算时间差

所以总结一下就是: 长度满足 15<= 长度 <=25, 以“-” 分割密码且 4 个子密码, 在分隔符之间数字依次大于等于 610，520，666，233 就能密码正确

比如这样

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO2uTkrWt6Zicfoe5UGI09SySbWrKGgxhENzaKHptGuntcWUUsj7SZP0Q/640?wx_fmt=png)

 但是这个小程序我还是发现不少 bug

比如:

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOO9dWlv3SdXcf3VGxviaxib0rSTmAEBO0auC40M5KFkC9usMMDewkEibCCQ/640?wx_fmt=png)

 还有这样写的话程序会直接崩掉

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvouic6N5VZ783VxKVpYkQuLsOOibaYcqzK5gl0zZWicZy8bGMvW7RoVh7V7PO2U1fSvybIiaUZ9q4vXjohg/640?wx_fmt=png)

**后记**

作为学习反反调试初级, 重要的是使用 x64 debug 和 ida pro 分析的过程, 这个还是很有帮助的。

脑海中又浮现了海哥的话:"没有好的正向基础就不会有好的逆向基础。"

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

**推荐阅读：**

本月报名可以参加抽奖送暗夜精灵 6Pro 笔记本电脑的优惠活动

[![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibHHibNbEpsAMia19jkGuuz9tTIfiauo7fjdWicOTGhPibiat3Kt90m1icJc9VoX8KbdFsB6plzmBCTjGDibQ/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247496998&idx=1&sn=da047300e19463fc88fcd3e76fda4203&chksm=ec1ca019db6b290f06c736843c2713464a65e6b6dbeac9699abf0b0a34d5ef442de4654d8308&scene=21#wechat_redirect)

**点赞，转发，在看**

投稿作者：Buffer

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)