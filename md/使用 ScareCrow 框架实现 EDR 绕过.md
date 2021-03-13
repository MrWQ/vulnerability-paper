> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FP3ooddGTkcyHrq6sKfGtw)

ScareCrow 是一款 Go 语言编写的一个免杀框架，地址为：https://github.com/optiv/ScareCrow

安装：

首先 down 下来该工具

```
git clone https://github.com/optiv/ScareCrow.git
```

然后编译即可

```
go build ScareCrow.go
```

若编译过程中出现超时问题，可尝试使用下面的命令解决：

```
go env -w GO111MODULE=on
go env -w GOPROXY=https://goproxy.cn,direct
```

编译之后运行截图如下：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xib7PZv3TePk5ibvlicwcnhC00OtowalNOgHYJ8fG7glZ6BNNJCcFYRg5hrrSomURGyWjQib1kvByfGg/640?wx_fmt=png)

简单使用

首先使用各类Ｃ2 工具生成 raw 的文件

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xib7PZv3TePk5ibvlicwcnhC0wgicMhD1sznkvSem66g7ssnDLgnBewACCf6NeW2etUVQ20emlFH0E5g/640?wx_fmt=png)

然后使用下面的命令来进行生成我们的载荷：

```
ScareCrow -I /root/payload.bin -Loader binary -domain www.acme.com
```

-Loader：指定输出的类型，目前支持 binary、control、dll、excel 、 wscript

-domain：指定一个域名进行代码签名

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xib7PZv3TePk5ibvlicwcnhC0jLoAObnVgNVUFVEVicAT31UnMJWrHEPp9NaOTOwDweT8HWqnRaib60Hw/640?wx_fmt=png)

不过效果不是很好，可能跟我没加反沙箱有关。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xib7PZv3TePk5ibvlicwcnhC0joOMmlFmq63ALqhDR1QJmvc67c8lx8MWGexGutMbDQPbP9r5X79Xwg/640?wx_fmt=png)

不过火绒还是没什么问题的

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Xib7PZv3TePk5ibvlicwcnhC0054OYXLxzUGuHqUTI5vfI0IhCiaAFNIsv70R7cJ1PJ5QHsU3Ric9vuWw/640?wx_fmt=png)

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)