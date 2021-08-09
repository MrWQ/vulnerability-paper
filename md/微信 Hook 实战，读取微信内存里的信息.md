> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/UWbBbYH2ikEETiFQbSExlQ)

```
原始文章标题:读取微信内存里的信息
本文作者:九世
发布时间:2021-07-21, 00:34:51
最后更新:2021-07-21, 00:55:42
原始链接:http://422926799.github.io/posts/26c63b49.html
版权声明: "署名-非商用-相同方式共享 4.0" 转载请保留原文链接及作者。
```

实验过程
----

寻找对应的信息基本方法如下:  
打开 CE 附加微信进程，搜索微信号等关键字，然后找到基址 （绿色的就是），双击添加到地址列表  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkusZIqnsJpLtCIKJoPItXt7tnJv25HPBlEibicLp7mBw2DMiaZeZDl6WlQ/640?wx_fmt=png)

PS：这里重启了几次 wx，所以 CE 里的地址和上图对不上 (一开始忘记截了)  
对着地址双击就能看到对应的地址  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkXm6W4st18alYgjx28XIjHURWW73VovRylQuYkfy47pVIPwv0soaAxw/640?wx_fmt=png)

然后 OD 定位到对应的内存地址去查询  
command: dd

可以看到开头就是微信号 （打码的手机号）等信息

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkPNl1wfctrPwcictPJcedEnTmlWHRM5jictibNz8StVCAGcuShV7fEOOJg/640?wx_fmt=png)

我们只需要知道基址然后：模块加载地址 + 基址

怎么求基址 -> 偏移地址 - dll 加载地址 = 基址  
这里求手机号基址为例，在 od 鼠标在内存窗口单机刚刚找到的那个地址点击手机号第一个数字，然后记录下地址，在 CE 手动添加地址里面输入，类型选字符串  
即可看见手机号（手机号长度 11 所以长度设置 11）  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkWpvuOyv0BYTAiaRX8Fnsd2OTSPZjPRrUpsKibcjELTOSqibZxkuxKNbkQ/640?wx_fmt=png)

dll 加载地址，CE 点击手动添加地址，输入 dll 名称，类型选 4 字节  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkibYcqOD1El1PPibDVrEkI4XBNk9IlYzNjQb7qBeF4lsPXWSyiaVm1xklQ/640?wx_fmt=png)

然后将数值改为十六进制（即可得到地址）  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkyQ2TGLVWczmTt505mwG1BkoNerCO3DIg0uciaXDsSic7z05mH69b0MHQ/640?wx_fmt=png)

或者你也可以用 OD 或者 Process Explorer 里获取加载 dll 地址  

（注：这后面截的图与上方地址对不上）  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkwgSN5h5WxL112Ut07lvxZUAXbAUdr74JXb0ZIg8XvbiaUiaJY2pwPxBg/640?wx_fmt=png)

求出手机号基址  
53D0F560: 手机号内存地址  
52CC0000:dll 加载地址  
53D0F560-52CC0000=104F560 -> WeChatWin.dll(52CC0000)+104F560 = 手机号  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkHhqFt0uaRWtg2wj9HYdszIMPuVbGXiapBM6URojU01yJM6auOq30JicA/640?wx_fmt=png)

所以以此类推获取：微信号、微信名称等基址  
WeChatWin.dll+104F52C - wx 名  
WeChatWin.dll+104F690 - wx 号地址  
WeChatWin.dll+104F560 - 手机号

（找到信息的时候可以切成地址，然后往下滑）  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKks3CWUficPyAhR2G4yz9uibhv0UmNTPrD1Kw8mOhH6Puth1K648lTBLZQ/640?wx_fmt=png)

注意事项：遇到指针的话，先获取指针里的值。然后在用这个值当作地址找  
在找 wx 号的时候就遇到了  
（算出第一个基址后，求别的时候只需要把后面三个数字给替换掉就知道了, emmmmmm）  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKk64ZZgu8Nrj8SpuibyBwO19VNjic55ib8IY1Yicv9lN9xFxRhRNhictYrskw/640?wx_fmt=png)

此时 046F35D0 里面的地址放着微信号  
（PS: 这里地址微信重启过，和上面的图地址对不上）  

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKkEXJDhC5KTiaMBc66QiaX3BQ49CcH9WhTh0rrQYRTeuYoDCKicHSzpZt4Q/640?wx_fmt=png)

构造读取  
使用的 Windows API:OpenProcess、ReadProcessMemory

```
from ctypes import *
from win32con import *
from ctypes.wintypes import *
from win32process import (EnumProcessModules,GetModuleFileNameEx)
import os


CreateToolhelp32Snapshot=windll.Kernel32.CreateToolhelp32Snapshot
Process32First=windll.kernel32.Process32First
Process32Next=windll.kernel32.Process32Next
OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle


TH32CS_SNAPPROCESS=0x00000002
TH32CS_SNAPMODULE = 0x00000008


MAX_MODULE_NAME32 = 255


class PROCESSENTRY32A(Structure): #定义PROCESSENTRY32A类型
    _fields_ = [ ( 'dwSize' , c_ulong ) ,
                 ( 'cntUsage' , c_ulong) ,
                 ( 'th32ProcessID' , c_ulong) ,
                 ( 'th32DefaultHeapID' , c_size_t) ,
                 ( 'th32ModuleID' , c_ulong) ,
                 ( 'cntThreads' , c_ulong) ,
                 ( 'th32ParentProcessID' , c_ulong) ,
                 ( 'pcPriClassBase' , c_long) ,
                 ( 'dwFlags' , c_ulong) ,
                 ( 'szExeFile' , c_char * MAX_PATH ) ]






def getprocess_pid(processname):
    processimage=CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0)
    pe32=PROCESSENTRY32A()
    pe32.dwSize=sizeof(PROCESSENTRY32A)
    ret=Process32First(processimage,pointer(pe32))
    while ret:
        if pe32.szExeFile.decode()==processname:
            return pe32.th32ProcessID
        ret=Process32Next(processimage,pointer(pe32))


def getmodule_address(handle,dllname):
    for module in EnumProcessModules(handle):
        dllpath=GetModuleFileNameEx(handle,module)
        print(module,dllpath)


def main():
    wetchatwindlladdress=0x63B60000 #枚举WetChatWin.dll加载地址失败，就直接手动定义了
    phome = create_string_buffer(11)
    wxname=create_string_buffer(20)
    wxnumber=c_int(20)
    number=create_string_buffer(20)
    pid=getprocess_pid("WeChatStore.exe")
    print("WeChat PID:{}".format(pid))
    process=OpenProcess(PROCESS_ALL_ACCESS,False,pid)
    ReadProcessMemory(process,wetchatwindlladdress+0x104F560,byref(phome),11,None)
    ReadProcessMemory(process,wetchatwindlladdress+0x104F52C,byref(wxname),20,None)
    ReadProcessMemory(process,wetchatwindlladdress+0x104F690,byref(wxnumber),20,None)
    print("WX Phome:"+hex(wetchatwindlladdress + 0x104F560),phome.value.decode())
    print("WX Name:"+hex(wetchatwindlladdress+0x104F52C),wxname.value.decode())
    wxnumberaddress=wxnumber.value #可以不用转十六进制，直接十进制即可,py转十六进制默认是str类型。。hex函数转后填进地址读不到
    ReadProcessMemory(process,wxnumberaddress,byref(number),20,None)
    print("WX Number:"+number.value.decode())
    #getmodule_address(handle,"WeChatWin.dll")




if __name__ == '__main__':
    main()
```

![](https://mmbiz.qpic.cn/mmbiz_png/ewSxvszRhM6XTuQaTBI4RBMfN65ADeKk332DlK6cytJ9aaCmWic1aIHB6vjafIzhLdGXJ3gPUWuGah4VmLcj0Tg/640?wx_fmt=png)

踩坑记录：

```
* 调用EnumProcess和用Thread32First枚举模块，结果根本不能完全枚举。原本想模仿Process Explorer调用ZwQueryVirtualMemory函数枚举模块，py写起来太麻烦。。算了
```

公众号

最后  

-----

**由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。**

**无害实验室拥有对此文章的修改和解释权如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经作者允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的**