> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/MZknrH3GASOHCxVHZbFuMw)

之前老公众号的文章，本文章仅限于逆向学习，请不要用于祸害他人  

否则后果自负，与公众号 and 本人无关

某傻逼网友提供的色情软件 看视频需要付费  

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHO4bvxoOMiaFLelTJFhpdmPprZg2QawHqNLK1nTLtftkC1f8yTWcwnZw/640?wx_fmt=png)

老夫岂是看片给钱的人？  

反手就给你破解了

先 adb 查看一下当前的包名 + 类目

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKH2AaoTGNH1jXVFKwOkDPiaIrsYOJoXjfAvkURu4sv4xo2gelWnvfEoibA/640?wx_fmt=png)

使用 adb 大概看了一下 没有什么有价值的地方

当前程序目测是使用的侧滑面板 以及 其他的面板搞的

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHVnYhV4uDvsZ7icpTwNXTgzpNwYotNiaxcfn3XxVIMW2vJSbicA8qquoeg/640?wx_fmt=png)

这里直接搜索关键词 “过期提醒” 文本转 Unicode

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHURJulIOE3C37IWoiaExdRpdFh6IW18eukqYPUdfZibEtNy9PtSEjXL8A/640?wx_fmt=png)

搜索到了三个结果，大概分析一下逻辑

先利用 jeb 打开此页面

当前的字符串是在 showAlert 函数，返回值类型为 boolean  逻辑型

当前进行了几层判断，如果条件都不成立则 return 1

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHm823UibfybKtricqIlGMp3nrsCzO6nvuKgQ3oOYnZ7cSJlsUn5Og2tGQ/640?wx_fmt=png)

其余几个搜索出来的结果都是一样的，这里直接利用 Androidkiller 在所有函数的头部分直接返回 true

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHAWfSpC7SzGhOplqQ88uicVQEOiczOj4UznKfAOeWxWoibOpv9qWOBib8nw/640?wx_fmt=png)

改好后回编译回去  

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHwN0ru6TxwIyiaMDn0n3jC3zByRukq9a63rScicypyRhSiataKb7HqP5Eg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHiaKyCib5wxtuoBuWNEvj9iaYeSDPhxNgy2BOt76ZtsRVMD1W0JyHwhkEA/640?wx_fmt=png)

就基本上可以免费使用了

这里我又问了下我群里的傻逼网友

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHtMeuaAZzicISxvrlzJQpVz8oNyq5icT0BJg9w0S9Gcy32CaezfQPLuYQ/640?wx_fmt=png)

那就破解的再完美一点

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKH6lfj9mGY7X34njjh448bO7FNNsTJEvbnNPVe30TIBdQm9GOHIC43Ow/640?wx_fmt=png)

这里在 “我的” 这里显示了当前过期时间，这里再把时间显示给搞掉

这里搜索 “您已经过期” 文本转 Unicode

搜索到一条结果 MineFragment.smali

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHEQu4BzO3h612u0JleEH7hK31YGKIGXJm7tEibgYYJOXdSJc7nMZ0JPQ/640?wx_fmt=png)

使用 jeb 再次打开这个地址

使用 jeb 附加进程 进行动态调试

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHrt7ic6D9dYmyrKu72tuE0XcAIiaXp3eGMVAKRWMS1VoROybQNA8ovjGw/640?wx_fmt=png)

这里在 0000001A 进行下段，然后再切换当前界面，让当前程序再次获取当前过期时间，成功断下

这里使用了 if-lez 对 v2 寄存器以及 v4 寄存器进行了比较

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHrGialA3JticylMMSVqZJJx0FW5v0gIZULkYYiaPMekfDia1syoUB0AJJXQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHNQbvrLElOOnK4KA6zVSRwhPTfTTTvBUoMhPPIUOAoOCBydnmfictZlA/640?wx_fmt=png)

看了一下条件不成立跳转的 9A

9A 代码区域是 “**您已经过期，过期时间为**”

那么这里得让条件成立

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKH5utJuReDdGLzjZVt7uGiaeSM3lszcFmDZibnbOQiccWCziakibaknCYcWxw/640?wx_fmt=png)

把 v2 寄存器的值改成 1

V2 改成 1 后 跳转到了这里，这里利用 getExpired 与 currentTimeMillis 获取时间戳

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHMH8FSoqibkF6pdwSrTw1ErJqabcLDAGSZ9QDD4TxKdeBKBcmiaBibmZ7w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHrEUaCrelicQCicvoEtj6M7G5Hb29PcZtPRoqne39Gibpez27qmddA1nDQ/640?wx_fmt=png)

当前 getExpired 函数是 so 层函数，currentTimeMillis 是获取当前时间戳

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHL15xsM2FPfHnQ0Q3GdS1QHmIln18On6icP5FYTZ5MD4EkJHYq7Pfxng/640?wx_fmt=png)

然后再对获取到的时间戳 除以 1000，保存在 v4 寄存器

然后再进行比较 v2 寄存器 > v4 寄存器

这里将 v4 寄存器的值 +1 然后赋值给 v2 寄存器

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHarvVsFS1l8TL6dHLhwV2aQwIpH7NicyBBBeVu9koOWPSwkjOwRjeo0Q/640?wx_fmt=png)

条件成立后 跳转到此代码区域

然后进行 TextView->setText(CharSequence)V, v2, v1  
对 TextView 的 text 进行赋值 值为 v1  
这里将 v1 的类型改成 string，可以看到是  
"您的过期时间：1970-01-01 08:00:00"

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHdX7BFsjJmEJibhO9goOHbZslEAOYcmu8g5gOlh5HoWNwIAOxoerNrVA/640?wx_fmt=png)

这里直接修改 v1 寄存器的值，然后放开下段

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHH6sic8kvlsnOdfYJzUYHrnzE8N4Eotd5r6DzjBZc7EQ82vl691SbEfw/640?wx_fmt=png)

显示也就解决了，搞清楚逻辑后，这里返回 Androidkiller 修改对应的代码

这里 if-lez 是 v8 小于或者等于 0 等跳转到 ：cond_1 将条件反向改成 if-gtz >=0 则跳转

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKH80IaEzjFGGcISaDNMT1B5hYXKJahHhIw98SZAriacPPUdWaXZu7pNicg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHaQNKhF9pVeOGLTmlW9HDfI50Jfic3aHn93YbmyjHp7tThrIPuKgBTEQ/640?wx_fmt=png)

这里直接给 v1 寄存器赋值就好了

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHG4KAs6pyuzKiaD4CXw5gUBZnFAS7H4XowiajFArUZeslrGibsKlnktRww/640?wx_fmt=png)

你以为这样就完了吗

不不不，还没有完

这里还有一个更新的功能没有去除掉

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHlzbsglc99qKbOcEyWw5XAdZaic6PcYIxuxUic2Qls7XhJh6bBDodIJTQ/640?wx_fmt=png)

alertUpdate 函数，直接在入口出让其 return-void 即可

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHj4FgbJ4MzFg4bg4pW6YseJm18ArYK9I8wBzicxA0bWbbRibUc2JOamXQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1O0v9dIWg00FUeglEib5NpVQWTeFhHiaKHNnryVibtoib4147d7VDpMmuWic5BicRibK23Ts7m8OcFu9Etz6icSibfqLoiaQ/640?wx_fmt=png)

欧了，记得准备好纸巾。(这次就不提供样本下载链接了，怕了)

写文章不容易，既然看到这里了

各位表哥点个在看呗，不然药药酱会没有写文章的动力的 哭唧唧~