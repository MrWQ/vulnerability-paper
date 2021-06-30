> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Z0SpYJBikdwA_foPkxnWFQ)

Go 默认编译会自带一堆信息，通过这些信息基本可以还原 Go 的源码架构，

本文就是研究如何消除或者混淆这些信息，记录了这个研究过程，如果不想看可以直接跳到文章末尾，文章末尾提供了一款工具，可以一键消除 Go 二进制中的这些敏感信息。

但还是推荐看看研究过程，可以明白这个工具的运行原理。

从逆向 Go 开始
---------

先写一个简单的程序

我的 go 版本是

```
go version go1.16.2 windows/amd64
```

```
package mainimport (	"fmt"	"log"	"math/rand")func main() {	fmt.Println("hello world!")	log.SetFlags(log.Lshortfile | log.LstdFlags)	for i:=0;i<10;i++{		log.Println(rand.Intn(100))	}	panic("11")}
```

编译

```
go build main.go
```

它运行后会如下输出

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJm8orficQXcibENK4wky4a8Wy3PL0jetVxdcdF9oLflkEsTc0CngWH1LeQ/640?wx_fmt=png)image-20210628160551219

可以观察到程序日志打印时打印了文件名，panic 抛出错误的时候堆栈的文件名也抛出了，可以想象 Go 编译的二进制程序内部肯定有个数据结构存储了这些信息。

用 IDA 打开这个二进制

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmvFQ8a0HFg8HsvQMJnml2jXE2tYwpbYYqOUJhLbvpgPuBibwm3hlTpkQ/640?wx_fmt=png)image-20210628161302422

能够看到函数符号的名称。

查看 PE 的结构发现有个`symtab`区段

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmQ6H5BNOpflj8ibK7616vDnTfNSWxUOZohdHYjO9taE2OibYiaScqZrRyg/640?wx_fmt=png)image-20210628161644212

原来普通的使用`go build .`进行编译，会连符号和调试信息一起编译到里面。

重新使用命令编译

```
go build -ldflags "-s -w" main.go
```

再次用 IDA 打开，发现符号信息都不见了。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmkwnlQ5OD8ojiaGJpygFP5N8Nk0M8VUJH2g1Tc7A64lTSfHTzSZkbdtw/640?wx_fmt=png)image-20210628162432087

再次运行程序，却发现文件路径信息还是存在。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmnCg2M40fMAGIUPGtZdbUN0gouffkyYURhEmXVhTvjP7K5WdNunNzeg/640?wx_fmt=png)image-20210628162501129

但是自己写的代码中根本没有这些字符啊，只可能是 go 在编译的时候自己打包进去的。

所以引出两个问题

*   Go 为什么要打包这些信息
    
*   Go 打包了哪些信息
    

### Go 为什么要打包这些信息

> Go 二进制文件里打包进去了 「runtime」 和 「GC」 模块，还有独特的 「Type Reflection」(类型反射) 和 「Stack Trace」 机制，都需要用到这些信息。

来自 Go 二进制文件逆向分析从基础到进阶——综述 - 安全客，安全资讯平台 (anquanke.com)

长按识别二维码查看原文

https://www.anquanke.com/post/id/214940 标题：Go 二进制文件逆向分析从基础到进阶——综述 - 安全客，安全资讯平台 (anquanke.com)

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmv10BlicJMXotkM9ACG4zSqRPibqAArTqPAkmaw5lfib8sHYaTgLx38liaw/640?wx_fmt=png)      

### Go 打包了哪些信息

*   Go Version
    
*   Go BuildID
    
*   GOROOT
    
*   函数名称和源码路径
    
*   struct 和 type 和 interface
    

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmNe7nC6oznuclTJDdiasUJZJicuXvd1jBAvIyiaEcp6KZEmoJPicib3aF2bQ/640?wx_fmt=png)img

### Go 逆向方式

看 https://www.anquanke.com/post/id/214940 这篇文章就能知道，通过解析 Go 二进制中这些内置的数据结构，就可以还原出符号信息。

> 有安全研究员发现除了可以从 「pclntab」 结构中解析、恢复函数符号，Go 二进制文件中还有大量的类型、方法定义的信息，也可以解析出来。这样就可以大大方便对 Go 二进制文件中复杂数据结构的逆向分析。

基于这种方式，已经有人写好了 ida 的脚本来恢复

*   https://github.com/0xjiayu/go_parser
    

*   仅支持到 Go1.6，Go1.6 之后数据结构有略微的改动，但是项目还没更新
    

*   https://github.com/renzhexigua/go_parser/tree/py3_1.16
    

*   支持到 Go1.6 的脚本
    

运行这些脚本，就能还原一些符号信息了。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmbwr6k8kr8ZOwtvMwaUic656IDHEN6iaBWaYjvtBCwia1zUy2kmqN5YNMg/640?wx_fmt=png)image-20210628172800127

redress 和 gore
--------------

前面的是基于 IDA 的脚本，因为 Go 也内置了自己的数据结构，用 Go 来解析 Go 更方便。

goretk/redress: Redress - A tool for analyzing stripped Go binaries

*   https://github.com/goretk/redress
    

```
.\redress.exe -pkg -std -filepath  -interface main.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmrYMyhCuwBwuJ7OwMS4l106FYuKCmRoffEy4jc7KRqXGBiaic1lHl0uLg/640?wx_fmt=png)image-20210628185810359![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmOF0YxCxk7Pgib8s7L4ScFITdtSp1nDnicQnxfCQKwtIXNGIvic0Way7ibA/640?wx_fmt=png)image-20210628185822332

redress 只是工具的前端，如果看它代码的话会发现，实际的解析代码在

*   https://github.com/goretk/gore
    

这款工具能从 Go 二进制中获取非常多的信息，几乎可以用它来还原 Go 的源码结构，这么神奇的工具，怎能不看看它是如何实现的呢。

GoRE 代码学习
---------

在 GoRE 中，`PCLNTab`是直接使用内置的`debug/gosym`生成，可用于获取源码路径和函数名称。

其他解析数据结构的地方很枯燥，有兴趣可以看 @J!4Yu 师傅的文章，很全面的讲解了 Go 的数据结构

*   https://www.anquanke.com/post/id/214940
    

我就说说看得几个有意思的点

### Go version 获取

go 官方命令`go version`不仅可以获取自身的 go 版本信息，如果后面跟一个 Go 文件路径， 就能获得那个文件的 go 的编译器信息。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmj4VdiamzzQhvo7TD8U3mZUy8LoRiadwocKxsZtJwr31S03IEg45y3JeA/640?wx_fmt=png)image-20210628111740455

查看 Go 源代码，看看是怎么实现的

`src\cmd\go\internal\version\version.go`

```
var buildInfoMagic = []byte("\xff Go buildinf:")
```

Go 官方是通过搜索这个魔术字符，用 IDA 定位到这个地方，可以看到，这个魔术字符后面就跟着 Go 版本信息的地址偏移。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJm8HzEPPLXwARFCodvjSxwwKswCariaPl8R4KmpTJu8PIG64Dm9tMyNLQ/640?wx_fmt=png)image-20210628110615071

官方实现代码

```
// The build info blob left by the linker is identified by// a 16-byte header, consisting of buildInfoMagic (14 bytes),// the binary's pointer size (1 byte),// and whether the binary is big endian (1 byte).var buildInfoMagic = []byte("\xff Go buildinf:")// findVers finds and returns the Go version and module version information// in the executable x.func findVers(x exe) (vers, mod string) {	// Read the first 64kB of text to find the build info blob.	text := x.DataStart()	data, err := x.ReadData(text, 64*1024)	if err != nil {		return	}	for ; !bytes.HasPrefix(data, buildInfoMagic); data = data[32:] {		if len(data) < 32 {			return		}	}	// Decode the blob.	ptrSize := int(data[14])	bigEndian := data[15] != 0	var bo binary.ByteOrder	if bigEndian {		bo = binary.BigEndian	} else {		bo = binary.LittleEndian	}	var readPtr func([]byte) uint64	if ptrSize == 4 {		readPtr = func(b []byte) uint64 { return uint64(bo.Uint32(b)) }	} else {		readPtr = bo.Uint64	}	vers = readString(x, ptrSize, readPtr, readPtr(data[16:]))	if vers == "" {		return	}	mod = readString(x, ptrSize, readPtr, readPtr(data[16+ptrSize:]))	if len(mod) >= 33 && mod[len(mod)-17] == '\n' {		// Strip module framing.		mod = mod[16 : len(mod)-16]	} else {		mod = ""	}	return}// readString returns the string at address addr in the executable x.func readString(x exe, ptrSize int, readPtr func([]byte) uint64, addr uint64) string {	hdr, err := x.ReadData(addr, uint64(2*ptrSize))	if err != nil || len(hdr) < 2*ptrSize {		return ""	}	dataAddr := readPtr(hdr)	dataLen := readPtr(hdr[ptrSize:])	data, err := x.ReadData(dataAddr, dataLen)	if err != nil || uint64(len(data)) < dataLen {		return ""	}	return string(data)}
```

### GoRE version 获取

交叉引用上文的`runtime_buildVersion`字符串，可以看到三处调用的地方。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmSpII2UbNNYQd4aZq3micwhLI44BNZve5uKl2VTqfbWq6ibApOuHuHBvA/640?wx_fmt=png)image-20210628110443042

前两个是`runtime_schedinit`内部的实现，第三个是官方工具 go version 的实现方式。

转到`runtime_schedinit`地址查看

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmMic3cyWv5iaRZR5HAQzBLSRR1RRR96v0Q6QVX9WLQKpzzAOpH7OYUoaQ/640?wx_fmt=png)image-20210628110321170

GoRE 的 verison 实现就是基于`runtime_schedinit`的，首先找到`runtime_schedinit`函数的地址，反汇编寻找`lea`的机器码，寻找基于 EIP 或 RIP 的地址。这种寻找地址的办法和我之前学习的直接用机器码匹配的方式不同，算是学习到了~

在后面这种方式也帮助我成功解析到了 Go Root。

### Go Root 解析

GoRe 已经是解析 Go 的比较完美的工具，但是发现没有解析 Go Root，这个也是能作为一个字符特征的，所以我准备加上这个功能。

我的 go 环境是

```
go version go1.16.2 windows/amd64
```

可以直接用这个测试代码

```
package mainimport (	"fmt"	"runtime")func main() {	fmt.Println("hello world!")	fmt.Println(runtime.GOROOT())}
```

```
go build . 编译
```

编译后运行会输出 GOROOT 路径

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmaG8TcQYYsEDibicrn5F0sibicHc5pb6Is5icw2mkshcI1WP6tJeRI45z6PQ/640?wx_fmt=png)image-20210628115628061

用 IDA 搜索这个字符串 `C:/Program Files/Go`，但是并没有搜到。于是转到 Main 函数，看到了符号信息。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmXDJRDU5HCSo636II5A06jzbpbrdU3P7GULLibibuQvTCOGjzKMgs3nOw/640?wx_fmt=png)image-20210628122150026

原来它是`C:\\Program Files\\Go`字符串，输出的时候将它改变了。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJm1MVvwgKJ9FHyONrvlJ7wTp8dTibbyK2TPB7ic1DPQhahRlokL7CRePeg/640?wx_fmt=png)image-20210628122244273

交叉引用查看

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmI99DiaWfkkBKR3j2K1iaonLoibc2DHB06fx4uo0Kiaw9uog5moR1IwbPKQ/640?wx_fmt=png)image-20210628122317564

有两个地方，一个是 main 函数我们调用的地方，一个是`time_init`，这个是内部函数的实现。

我们就可以通过这个函数来定位到它。

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmDx0dXxSdCibXj3YGo7FNn7MB5qkTiaRs31uQlibCok8MmFV9MNIqHqd9Q/640?wx_fmt=png)image-20210628122453999

刚刚新学了反汇编寻找地址方式，现在正好派上了用场，程序先解析 pclntab 获取函数`time_init`的地址范围，从这个地址开始反汇编，寻找`mov rax，立即数`指令。

因为这个赋值的汇编指令是 mov，写代码的时候还要注意 32 位和 64 位寻址的不同。

```
func tryFromTimeInit(f *GoFile) (string, error) {	// Check for non supported architectures.	if f.FileInfo.Arch != Arch386 && f.FileInfo.Arch != ArchAMD64 {		return "", nil	}	is32 := false	if f.FileInfo.Arch == Arch386 {		is32 = true	}	// Find shedinit function.	var fcn *Function	std, err := f.GetSTDLib()	if err != nil {		return "", nil	}pkgLoop:	for _, v := range std {		if v.Name != "time" {			continue		}		for _, vv := range v.Functions {			if vv.Name != "init" {				continue			}			fcn = vv			break pkgLoop		}	}	// Check if the functions was found	if fcn == nil {		// If we can't find the function there is nothing to do.		return "", nil	}	// Get the raw hex.	buf, err := f.Bytes(fcn.Offset, fcn.End-fcn.Offset)	if err != nil {		return "", nil	}	s := 0	mode := f.FileInfo.WordSize * 8	for s < len(buf) {		inst, err := x86asm.Decode(buf[s:], mode)		if err != nil {			return "", nil		}		s = s + inst.Len		if inst.Op != x86asm.MOV {			continue		}		if inst.Args[0] != x86asm.RAX && inst.Args[0] != x86asm.ECX {			continue		}		kindof := reflect.TypeOf(inst.Args[1])		if kindof.String() != "x86asm.Mem" {			continue		}		arg := inst.Args[1].(x86asm.Mem)		addr := arg.Disp		if arg.Base == x86asm.EIP || arg.Base == x86asm.RIP {			addr = addr + int64(fcn.Offset) + int64(s)		} else if arg.Base == 0 && arg.Disp > 0 {		} else {			continue		}		b, _ := f.Bytes(uint64(addr), uint64(0x20))		if b == nil {			continue		}		r := bytes.NewReader(b)		ptr, err := readUIntTo64(r, f.FileInfo.ByteOrder, is32)		if err != nil {			// Probably not the right instruction, so go to next.			continue		}		l, err := readUIntTo64(r, f.FileInfo.ByteOrder, is32)		if err != nil {			// Probably not the right instruction, so go to next.			continue		}        		ver := string(bstr)		if !IsASCII(ver) {			return "", nil		}		return ver, nil	}	return "", nil}
```

此外还要注意一个版本问题。`go1.16`以上版本的 GoRoot 是这样解析，`go1.16`以下可以直接定位到`runtime_GoRoot`函数，再使用上述方式解析即可。

我也向 GoRe 提交了这部分代码

*   https://github.com/boy-hack/gore
    
*   https://github.com/goretk/gore/pull/42/files
    

Go-Strip
--------

GoRe 可以读取 Go 二进制的信息，反过来，把读取的文本修改成替换文本，不就达到了消除 / 混淆 go 编译信息的目的吗。

基于此写了一个工具，可以一键混淆 Go 编译的二进制里的信息。

还是以最开始的 Go 代码为例

```
package mainimport (	"fmt"	"log"	"math/rand")func main() {	fmt.Println("hello world!")	log.SetFlags(log.Lshortfile | log.LstdFlags)	for i:=0;i<10;i++{		log.Println(rand.Intn(100))	}	panic("11")}
```

编译

```
go build -ldflags "-s -w" main.go
```

使用程序消除信息

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmPgVoa7bjRicNXFY0t3lEaLibxbvEdUGk2GxSo2syH3ZnDm3ic48KgqCMg/640?wx_fmt=png)image-20210628192127364

运行新的程序

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmibRwib2S8Oaau2U0H49ZG08bbKGiakG0C3KiajRRFuge4gWdxyRVwGfHTQ/640?wx_fmt=png)image-20210628192157142

运行没有问题，之前含有的文件信息都用随机字符串填充了。

用之前的 IDA 脚本查看

![](https://mmbiz.qpic.cn/mmbiz_png/eLgL5R4W3FhV1YHEcOQuFUgkYHdB3vJmEbhG2ibicwJkGVibK1VlpA5ibJfJJ9x6JK9NqQSYe9bR1Z7gjiaG12W3MIg/640?wx_fmt=png)image-20210628192353333

函数名称也都填充了。

### 与其他工具的对比

知名的 Go 混淆工具有`gobfuscate`、`garble`

像`gobfuscate`, 核心思想是将源码以及源码引入的包转移到一个随机目录，然后基于 AST 语法树修改代码信息，但这样效率有很大问题。之前测试过`deimos-C2`和`sliver`的生成混淆，生成一个简单的源码需要半个多小时甚至更长时间，并且混淆的不彻底，像 Go 的一些内置包、文件名都没有混淆。

像`garble`采取的混淆中间语言的方法，但是也有混淆不彻底和效率的问题。

相比之下`go-strip`混淆更彻底，效率快，支持多个平台架构，能比较方便的消除 Go 编译的信息。

### **程序下载**

在微信公众号回复 go-strip 即可获得下载地址

参考
--

*   Go 语言逆向初探
    

*   https://bbs.pediy.com/thread-268042.htm
    

*   Go 二进制文件逆向分析从基础到进阶——综述 - 安全客，安全资讯平台
    

*   https://www.anquanke.com/post/id/214940
    

*   https://github.com/goretk/gore
    
*   https://github.com/goretk/redress