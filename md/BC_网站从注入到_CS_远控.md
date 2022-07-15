\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/R7\_tbNghqiWSbNqq5W42Yg)

前言

本着三好青年的光环下, 进行对非法网站的取缔工作。

过程

通过 fofa 搜索目标 BC 网站关键指纹

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhLWomcXg7tcbBQM8FO4KXReLRv5oT1l2VqzfPxnoEtVbEJgXu59nYKg/640?wx_fmt=png)

打开任意一个 fofa 搜索出来的页面

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhOpDlSJOMaVlGTe00oZiaYuVo0dYv0PkLEtdq0lBsLwZsonIkTnJCWtQ/640?wx_fmt=png)

浏览器打开代理抓取登陆数据包

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhnnGgiceRVo0iaCvLvfL8fX70w7cz7TSJ9XaJQicZQ1FwqPjiahujtjgYdQ/640?wx_fmt=png)

利用 sqlmap 进行数据包注入

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhx7ZreplnWa673D8AibNdKfnsdePG2YYSo4pWtInIw6mnayrPPJyMiczw/640?wx_fmt=png)

发现存在注入点

测试权限看下能否直接 os-shell, 如果有权限的话，方便接下来的 CS 多人运动

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhVnlWC5oiaA57gpHP8ayowQc3LC037sLtC5Wmz6UqiblsvEeibFxFF5bkw/640?wx_fmt=png)

存在 dba 权限，直接 os-shell 执行命令

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhMdum25rOHmAj74VoEJ50wh5SvOVibHBfnm3kxelialIaFrXWFgiatve6g/640?wx_fmt=png)

利用 cs 生成一个 powershell 无落地马，前提是配置好监听器。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhbVXGQGhWekZIYPX0WWfNUapadGkbJlT9epKVZAoIOEBpDDGO9DicbXw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhhavzkQj7knCLt8iaN1ZE7rciacBHGiccmylr2gTHicywzfZa0icOh9kwUcA/640?wx_fmt=png)

点击开始的时候会生成一个 powershell 链接

把生成的 powershell 链接填写到 os-shell 里面

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWheTpmglz6phbXlvtknbEUPyiaxBzxlSw215jOEsMZOOnyGwyZ866KBhA/640?wx_fmt=png)

执行结果

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhbCAiaNC1rngIsqC3OkLiaEaoJSxlGVrlNBVoULqGSxKUGwzaMNlicibVNA/640?wx_fmt=png)

查看 CS 多人运动工具

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhhKpIEThBATrNRx5kHBURp1S7SZGd1buh0kP3UcS7JVLBUezicJDulrw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhics8DTFUSZXhWzYpyCv210ia1A74H3YFqJoFokej7rwEzljwbIib2QqUQ/640?wx_fmt=png)

发现只是普通权限。接下来进一步的提权

利用 CS 的插件 -- 梼杌

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhAHCpu2OeJA4663AFvfnYwGecg4Eje6IVlssADtvt3dgL2z5A5loLEg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhskaF9xdKOU4B4Onj37dsr4L6jPWZXQSGTaBpo6MXibaTe60t7JpoibdA/640?wx_fmt=png)

(139 是我的监听器的名称)

其实也就是利用 MS16-075 的漏洞进行提权

执行结果

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhr3YwibXuk7VBcV0pdancHgP2gDgFxfoDS24WbLHspfIURiaxg6ZMXPZQ/640?wx_fmt=png)

提权成功

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWh3EwIDicQiaFUtBicwroTqM2KrPCzNSjPqhLiaNGfJRfcDy8ZtoKUM7qm9w/640?wx_fmt=png)

读取账户密码

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhNqFDmayBDRMAOGTO9mejb5RVzjqIdicatDkQW9gcudTby8aibHvgicdbg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhJibaRlIJEHTczIhkfDnDB3Mjea1TzIdkKsv9ejxpFycbZJyTfMdIXYQ/640?wx_fmt=png)

成功读取到账户密码

进行权限维持

读取进程 利用进程的绑定，避免 shell 被干掉

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhPX1DYicJrg1QW7A2NEQwO49twicZfVqNC6k22ObrQjsINLekickibVebicA/640?wx_fmt=png)

查找有相等权限的进程进行注入

我们目前是 system 权限了

就利用有 system 权限的进行注入就可以

**小 tip**: 非必要的条件下，不要去登陆 3389 远程桌面。尽量避免留下没有必要的痕迹。

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09xQ7frAX1Yx0oFCQphLBWhicicley20IZcF5iabiaEEA9ib4tyjqEepFAuplERldD6UahiccwvIPlj5qiaA/640?wx_fmt=png)