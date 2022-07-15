> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Bw8Kft2JgrleC9HRlkX3bw)

无文件落地的木马主要是一段可以自定位的 shellcode 组成, 特点是没有文件，可以附加到任何进程里面执行。一旦特征码被捕获甚至是只需要 xor 一次就能改变特征码. 由于传统安全软件是基于文件检测的, 对目前越来越多的无文件落地木马检查效果差.

**基于内存行为特征的检测方式, 可以通过检测执行代码是否在正常文件镜像区段内去识别是否是无文件木马. 由于 cobaltstrike 等无文件木马区段所在的是 private 内存, 所以在执行 loadimage 回调的时候可以通过堆栈回溯快速确认是否是无文件木马**

检测只需要 40 行代码:

> 在 loadimagecallback 上做堆栈回溯
> 
> 发现是 private 区域的内存并且是 excute 权限的 code 在加载 dll, 极有可能, 非常有可能是无文件木马或者是 shellcode 在运行

```
void LoadImageNotify(PUNICODE_STRING pFullImageName, HANDLE pProcessId, PIMAGE_INFO pImageInfo)
{
    UNREFERENCED_PARAMETER(pFullImageName);
    UNREFERENCED_PARAMETER(pProcessId);
    UNREFERENCED_PARAMETER(pImageInfo);
    if (KeGetCurrentIrql() != PASSIVE_LEVEL)
        return;
    if (PsGetCurrentProcessId() != (HANDLE)4 && PsGetCurrentProcessId() != (HANDLE)0) {
        if (WalkStack(10) == false) {

            DebugPrint("[!!!] CobaltStrike Shellcode Detected Process Name: %s\n", PsGetProcessImageFileName(PsGetCurrentProcess()));
            ZwTerminateProcess(NtCurrentProcess(), 0);
            return;
        }
    }
    return;
}
```

堆栈回溯:

```
bool WalkStack(int pHeight)
{
    bool bResult = true;
    PVOID dwStackWalkAddress[STACK_WALK_WEIGHT] = { 0 };
    unsigned __int64  iWalkChainCount = RtlWalkFrameChain(dwStackWalkAddress, STACK_WALK_WEIGHT, 1);
    int iWalkLimit = 0;
    for (unsigned __int64 i = iWalkChainCount; i > 0; i--)
    {
        if (iWalkLimit > pHeight)
            break;
        iWalkLimit++;
        if (CheckStackVAD((PVOID)dwStackWalkAddress[i])) {
            DebugPrint("height: %d address %p \n", i, dwStackWalkAddress[i]);
            bResult = false;
            break;
        }
    }
    return bResult;
}
```

使用:

编译好驱动, 加载驱动, 之后运行测试看看:

普通生成 (x32 与 x64) 测试:

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibFGe1lZRQcfOGAsfUXwBWnLLzmSQYRicDltjiayiacZSZLvfVGlic0kPE4mt1Dlrm0oHG9iaxtG4Q3YVA/640?wx_fmt=jpeg)

基于 VirtualAlloc 的 C 代码测试:

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibFGe1lZRQcfOGAsfUXwBWnKblKVQriaLdianiczNLc5Ebcibyibf7ctNeibJSJqyQWx4riaj2KoBKYQYXjQ/640?wx_fmt=jpeg)

测试结果:

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibFGe1lZRQcfOGAsfUXwBWnoIgUickM0roicoqLoIWYMHBqde21coRudfecPuj8lWB7iaXQOEWZxxHUQ/640?wx_fmt=jpeg)基于 powershell 的测试:

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibFGe1lZRQcfOGAsfUXwBWnU8RSmPKaph0Rvfia4eRyRjyOxH0TfdYugswNBtuK49dE2K9zXePpgmA/640?wx_fmt=jpeg)

基于 python 的测试

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibFGe1lZRQcfOGAsfUXwBWnNg1G1L72H8JcicoVRhaTfvuUibicXT8z2kLhKqHBibv35zD1fVxCwwS65g/640?wx_fmt=jpeg)

测试结果:

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibFGe1lZRQcfOGAsfUXwBWntqVxRRVzicpnUVqbUYmIPO3Jg5OZibz4WP4n3ibCUcatBZsiaFA7LQVVDQ/640?wx_fmt=jpeg)

弊端:  
目前已知的 ngentask.exe、sdiagnhost.exe 服务会触发这个检测规则 (看样子是为了执行一些更新服务从微软服务端下载了一些 shellcode 之类的去运行). 如果后续优化则需要做一个数字签名校验等给这些特殊的进程进行加白操作. 这是工程问题, 不是这个 demo 的问题  
一如既往的 github:  
https://github.com/huoji120/CobaltStrikeDetected  

![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR38Tm7G07JF6t0KtSAuSbyWtgFA8ywcatrPPlURJ9sDvFMNwRT0vpKpQ14qrYwN2eibp43uDENdXxgg/640?wx_fmt=gif)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf + 小程序：把安全装进口袋 小程序

  

精彩推荐

  

  

  

  

****![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib2xibAss1xbykgjtgKvut2LUribibnyiaBpicTkS10Asn4m4HgpknoH9icgqE0b0TVSGfGzs0q8sJfWiaFg/640?wx_fmt=jpeg)****

  

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR3ic1YSqMEGaoBvQqUqGqTVW4KwVA6ePJbEc5lPmoicqjfWV2T2BgH6icQDvAhvhqHQvxSl3cjacCulqQ/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486459&idx=1&sn=74658ddb6cd1bfb2d224bc7c3a236015&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibnOz2Slh3icgLwEyRibxE9Qa7ziag03WLN71NL5icWxBsNPGzNlDEQrNVpjoIRnmglkpJ61iaP7giaBZww/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486404&idx=1&sn=6d434a8d335887fc665287732933091d&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR384iaX6B8n12ebKz8LqibnrDQTyFTVGgeUQ20OH45Z1KqtjzL83XLEjDicq9Sbvd5SeXyUbd7iaWFdmHw/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486350&idx=1&sn=ce56524dc187468146dc23a991b0596a&scene=21#wechat_redirect)

**************![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR3icF8RMnJbsqatMibR6OicVrUDaz0fyxNtBDpPlLfibJZILzHQcwaKkb4ia57xAShIJfQ54HjOG1oPXBew/640?wx_fmt=gif)**************