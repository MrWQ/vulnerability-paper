> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/KF7Sj0ec8W7T7RQ5LXOTDg)

myccl 免杀 360 简单教程

这个工具很早就有了，通过修改特征码达到免杀

**0x01 特征码**

文件中的某一串二进制代码，杀毒软件识别到了就会认为这个文件为木马

myccl 将 00 覆盖到文件中，如果此时文件不报毒了说明说明覆盖的地方存在特征码

```
如M为特征码存在在某一段中
aaaaa
aMaaa
aaaaa

myccl将代码覆盖生成三个文件

aaaaa aaaaa aaaaa
----- aMaaa aMaaa
----- ----- aaaaa
不报毒  报毒 报毒

说明特征码在后面两个文件中，继续缩小范围得到特征码，详细的可以用二进制查看的工具就可以知道myccl的工作原理
```

然后就是继续这个过程得到特征码的准确位置，当然特征码可能有很多个，还有复合型特征码啥的，还是要具体看情况去找。

**0x02 免杀实践**

杀软用火绒，被杀的文件为 nc

用到的工具有 myccl 和 C32asm

360 每个文件都会丢到云上扫描，myccl 出来的文件一般都是很多的，可以扫一年）

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQRC85kQNVhH0ib12BYWTkKfwPNI69A0I1xIgFddlT11FofqA91wCMEBQ/640?wx_fmt=png)

起始位置可以自己定，也可以不用管就用默认的，数量选选 100 就好了，长度会自动算好的，点一下生成，会在被选中的文件同目录下生成 OUTPUT 文件夹

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQjhPjKC8lwCicPvaicbsWIKs7lBKL403ficefqV95tyiac3fyNsj2k4QDHg/640?wx_fmt=png)

第一段 0000 是文件的序号，第二段是文件开始的位置，第三段是单位长度

第二个文件是 0001，这里应该是文件名排序的问题，E0+17F 就是第二个文件的开始

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQdmrEdxMcBNMXtm8lSgce7eE2kDMHykpMSHicOwz9KgW6z2mtljNlDiag/640?wx_fmt=png)

接下来对文件夹杀毒，然后把扫出有毒的文件删除，点击二次处理，提示找到特征码是否继续，点击 yes

再次扫描文件夹发现没有报毒文件，点击二次处理，会给出一个特征码分布示意图，这个不用管

继续扫描文件夹，发现没有报毒

点击特征区间

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQV6cnv5QA6OZo479RzxDo3A6HiaWbIe5BB6CNnlq97mxOnqdmwib3AHDg/640?wx_fmt=png)

右键复合定位此处特征码

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQwMOiaxcu5Wegm83Qa2ybvd6nEYtAz6XqQtxndiaxpWwsEU5ak2XnUG0Q/640?wx_fmt=png)

可以看到缩小了特征码的范围，这里的数量也是可以改的，继续改成 100 重复之前的操作

生成 -> 扫描文件夹 -> 删除报毒文件 -> 二次处理 -> 发现没有报毒 -> 复合定位特征码

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQaOd0vlAicUF18DwxQXEiaclmYTssNBw7bB6N5I158L4f5QQHdKIk89ibg/640?wx_fmt=png)

现在范围已经确定在两个字节内了可以不用在继续缩小范围

用 C32asm 打开文件

将 nc 拖入然后以十六进制打开文件，找到 00006678 的位置，后面的两个字节就是特征码

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQlhfDscLV8nr1Hp4gwd0uOx4nicRbAJInCw0FfZicQXVIibqMPo2Tq4MkA/640?wx_fmt=png)

可以看到是一个中括号和一个换行符，这个就是 nc 打印出来的那些内容，修改一下应该不会使程序不能用，把中括号修改一下，随便换个符号

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQ5a6xiaKogK05hg1D2sQ4AQUic66oiaBqv7IwsM8fBJHq69VWw3qSIf2zA/640?wx_fmt=png)

修改好后另存为一下，看看这个修改后的文件能不能使用

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQRvAAZUrhBoteWvwDfGYmoxRagehhDXd03JxcKfiaMCdLbFpM2souVVw/640?wx_fmt=png)

是可以正常使用的，help 界面的输出被修改了，最后再看一下能不能免杀

![](https://mmbiz.qpic.cn/mmbiz_png/u5KqVShKUTal4wWPEst2ICibKWqjuibUnQ395tYYtYsWXteCmiaJHgtUO7NV9ssr0fkLYteN7rjUwCQ4Ia3XH3THQ/640?wx_fmt=png)

**0x03 总结**

这个方法还是有挺多局限的

也只能针对特定杀软，因为不同杀软直接特征码可能不一样

禁止非法，后果自负

欢迎关注公众号：web 安全工具库

欢迎关注视频号：之乎者也吧

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3UibvNdhnFT3V7RRPsye967HCKFibyIsnAV60JjliaFZlthLQ7GY462NXdS5zQN71mliaiau4RSjicIgwCWUA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3UibvNdhnFT3V7RRPsye967HCKNrMF1xicNibUyjWBhuoY9qOz585hyrvRtp6XCGe7UBfT9s6QuwVEp3jQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3UibscHhZMwoYdu5emj9UMOtXDTcau8DS3ffbV8RSTZrw5bff7hxibxNekwRktTGnMT0FEUMR9vCJCX3g/640?wx_fmt=jpeg)