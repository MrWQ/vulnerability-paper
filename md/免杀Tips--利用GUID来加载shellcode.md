> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/9N5IN-695S2jbpKi02NUkA)

 前几天，很多的公众号都复现了来自Lazarus组织的加载器的实现方法，UUID法，具体链接可以查看：https://research.nccgroup.com/2021/01/23/rift-analysing-a-lazarus-shellcode-execution-method/，然后今天带来一个类似的方法，即使用GUID来加载shellcode。原文链接可点击原文链接查看。

  

        GUID：一个全球唯一标识符 或 GUID 是一个假随机数用于软件中。虽然每个产生的GUID是不保证唯一的，但不同的标识符总数是（2128 也就是3.4028×1038）如此之大，以至于相同的数字被产生两次的机率是很相当小的。而这种加载方法也是从一个样本之中发现的。起初是国外的安全人员在样本中发现了大量的GUID字样，如下：

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UI754BPzGHsfVW2ku5iamKCANeGUBIt8vy9Ovdj1g7dGYyyX7svNcGRibHXLEvtHICtuiaeoPONIRvA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

然后在IDA里分析是，发现了其加载代码以及解密代码（GUID做了部分变化）：

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UI754BPzGHsfVW2ku5iamKCjohu3NhFBIf2pljztHUPadspt6yfdM4kXic2RnAicicvq8Y4kOVFxcibOw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UI754BPzGHsfVW2ku5iamKCjQFbaVQSNEKNZ7KzyZDqeg7oqUrbt6cGau81y4k5icI5GSyhVsqhibZA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

然后我们发现，其中比较罕见的就是GUIDFromStringW该函数的调用。而作者也通过使用下面的方法成功的将GUID还原成立bin文件：

  

```
`$GUIDs = Get-Content .\guid.txt``foreach ($GUID in $GUIDs){` `$Bytes += [System.Guid]::new($GUID).ToByteArray()``}``[io.file]::WriteAllBytes("C:\Users\Administrator\Desktop\2.bin",$Bytes)`
```

  

然后通过火眼的https://github.com/fireeye/speakeasy工具得到了目标的部分信息(蓝队同学的工具+1)

  

那么了解到了这些之后，我们便可以学习这种思路，来编写我们自己的GUID的loader，首先就是GUID的生成。C#中提供了现成的代码：

  

```
`using System;``using System.Collections.Generic;``using System.Linq;``using System.Text;``using System.Threading.Tasks;``namespace Part8``{` `class Program` `{` `static void Main(string[] args)` `{` `string hex = "0F1F006666660F1F8400000000000F1F";` `Guid guid = new Guid(hex);` `Console.WriteLine(guid);` `}` `}``}`
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UI754BPzGHsfVW2ku5iamKCe6hCrxJ7SqWKsFFRD9HGfu5vOqH1Tj9HaZ8SRHUY4SJm2jcFHicddlg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

剩下的就是像IDA里面一样，编写一个加载器来加载就好了，这边就不放代码出来了，有兴趣的小伙伴可以自己实现一下。

  

     ▼

更多精彩推荐，请关注我们

▼

![图片](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)