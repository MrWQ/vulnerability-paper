\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/rdHHxcbJKkcIeoIO4dQmFw)

C 格式 shellcode 异或加密生成 dll 可过免杀过 Windows Defender

1

简介

项目地址：https://github.com/k-fire/shellcode-To-DLL

测试环境: winserver2016  cs 4.0 

编译环境: win10 VS2019

2

原理

C 格式 shellcode 异或加密写入 dll 文件

当 dll 被调用或者被注入进其他进程时触发功能

dll 功能：解密 shellcode 并将其注入 rundll32.exe 进程

3

使用

msf 或者 cs 生成的 shellcode 要为 32 位的

使用 dll 注入器将其注入其他进程或者调用 dll

提供测试调用 shellcode.dll 程序

https://github.com/k-fire/shellcode-To-DLL/blob/master/Release/call\_dll.exe

注意：输入的 shellcode 为 C 格式替换 \\x 为 （空格）

4

测试

cs4.0 

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADWEiaicWAEnicazZ64yBgMjlFTRaDvxQbVTGANZNic5A6ny5Yy2fquCUQhZA3ibhoDIxAVoGPusfrqFDg/640?wx_fmt=png)  

dll 生成

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADWEiaicWAEnicazZ64yBgMjlF3icN9MTeaLUgxgPDS8Sic7BDmq2VnAia5AAPYpOXuXozNEZuXXaurtSCw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADWEiaicWAEnicazZ64yBgMjlFaBt9lhcVsCvXqw7SNUX6PKI2YXib2OCsibwyHBYfty9J80eIbKkYpJ4Q/640?wx_fmt=png)

详细

https://kfi.re/816.html

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADWEiaicWAEnicazZ64yBgMjlFAzicNnEHEYnpWLkicY9fqZblnQh73QdgXHPqRibtFd4vRsvSaOdoCxt1Q/640?wx_fmt=png)

5

关注

本公众号长期更新红蓝对抗实用技术

手机扫描关注一下

![](https://mmbiz.qpic.cn/mmbiz_jpg/Jvbbfg0s6ADWEiaicWAEnicazZ64yBgMjlFA7cKXUSibSjiclIkkBfJeenmJaArib2u2rvFGsAE2o0NhGnTxibUHaCT1w/640?wx_fmt=jpeg)

END