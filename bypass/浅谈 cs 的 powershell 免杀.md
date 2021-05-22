> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FY-MG9dEeOvmJSaBMW_9Xg)

原理：“免杀”，顾名思义就是逃避杀毒软件的查杀，目前用得比较多的免杀方法有加壳、修改特征码、加花指令和修改源码四种，通常黑客们会针对不同的情况来运用不同的免杀方法。杀毒软件的工作方式一般是特征码匹配杀毒，而病毒只有能够逃避过杀毒软件的查杀，才能顺利实现其入侵系统、盗取用户私密信息的目的。

0x01    加载 payload

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZ9LTQgtt8jqfjULKI8d4ZW9vrruw3pV2a7dy8RDqdjpSfqkJfMGgJ4Q/640?wx_fmt=png)

首先生成一个 cs 自带的 payload。  

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZicdvSciaaeibFnBJw5oUAjLGq5pf6Lz1O8FzofHWr8fp0zQCUaUj88w9w/640?wx_fmt=png)

看一下 payload 本身的源码：

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZauEQjVyhADqbRTIecmTjMrfMaA7jr2o7fHQJ61L0LlRWv5ozibZF91Q/640?wx_fmt=png)

主要是把 shellcode 加载到内存中的代码放到字符串中，然后 IEX 执行代码。

查杀效果：

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZq3UPVg5gJgeHQiauIBz0yTqIzvqlJkJarZNcqibJyHSgiaHpTjWWkuvWA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZgM3QiaY40eiahoA49fvNmAjDiczSPiakvfbBkG8kb8G2A2icCPokofhzgWw/640?wx_fmt=png)

可以看到，本身的 payload 的特征值已经被大多数防护软件记录。  

0x02    混淆开始

首先我们可以先更改 payload 的变量名和函数名，这里可以使用替换关键字代替, 避免漏掉变量名没有更换。

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZSLIiak1VDM8HQRVqQsjpSIxQRNZNfibYyEgnuvu2TG8DpLOzjWE7fybQ/640?wx_fmt=png)

因为这个 payload 最重要的是它的恶意代码，所以我们把 [Byte[]]$var_code 更换一种编码方式。  

```
在powershell里执行下列代码，把恶意代码直接解密。
$string = ''
$s = [Byte[]]$var_code = [System.Convert]::FromBase64String('【cs生成的shellcode】')
$s |foreach { $string = $string + $_.ToString()+','}
$string  
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZE0rqxTdEfNHz5Lm4MktQTHJhLUtwwfsVwfuW52mQ1JvsoQqqo7gicYw/640?wx_fmt=png)

最后在给 payload 整个代码进行 base64 加密，原理：让整个 payload 在加载之前都不会被识别，在需要加载的时候，把代码解压出来。

```
[System.Convert]::FromBase64String(加密后变量)---powershell的base64解密
[System.Text.Encoding]::UTF8.GetString(加密后变量)---powershell的UTF8解密
```

‍

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZlYMMtGKupfCicPOkibmXgKKicsxibbUm10vMJZrXL5W0a3oozsX7s6ssdw/640?wx_fmt=png)

查杀效果：

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZ2Eib1azX863yhavHkqw0GJN8fpHuqYaHqN0BCX9YYYBRaLl20aKzuBg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZUe8exTN3iaqv7eJ7mEgsPohkB2euYehZFVw71QI1zeW1iaFpw26pyeaw/640?wx_fmt=png)

虽然还是有防护软件可以检测出来，但是和自带的 payload 相比已经明显减少了。一般使用的火绒软件也没有检测出病毒，还是有作用的。好了，我们试试改过的 payload 能否上线把。接下来，我们在试试把代码中 base64 加密的数据分开几份，也能达到绕过的目的，看我们试试看能否成功。

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZ2Yicqeia0fzj9rpPL9ibtViaM8QB067iaHyl1lQ1g1sXgImg8k58kCP25uQ/640?wx_fmt=png)

查杀效果：  

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZe12NiaGtKDIXlqLcLkp6xheLicSP0wMsNY1ldpN10iacRIKfGegjdBYGQ/640?wx_fmt=png)

发现没有什么作用。。。（技术有限，我这个小菜鸡就先做到这了 / 卑微）

在受害机上执行代码，看查能否上线。

```
Powershell -ExecutionPolicy Bypass -File .\payload.ps1
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZkIQwKvdYgj8za0S7JHGssydiaBg8lZePoHWicQvPtvGB6W6SibQicWHaqA/640?wx_fmt=png)

上线成功，试试上防护防护。

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFCrYcl4PqicfKOukkiapsASBZG5PfJNx9BP6sib3iczqaKg1g7NFTtDvsKsbzwgWgU6KCHcLlGiaeWAOmQ/640?wx_fmt=png)

运行的时候还是发现木马了。不说了，继续学习去了。

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFDibHEbJnpWR5auWic9K3FhMMFgWQfdsatqDxN159FRwSIS5mNHia9aXlFBYnJzAuvlNfib6mHw72Rl0A/640?wx_fmt=jpeg)

0x03    总结

1.  虽然实现真正的免杀，还是有点困难的，但是可以绕过大部分的防护软件。
    
2.  免杀重要的是：混淆代码。给代码加壳、更换关键字、把代码块分段都是有效的绕过技巧。在其他地方的免杀也可以用到。