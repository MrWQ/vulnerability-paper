> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/SQtcLf_73fggOBtyJgWtxw)

**_1_**

概括

在智能设备漏洞挖掘过程中，固件提取是分析的第一步，也是迈向成功的第一步。目前，已有多种关于固件提取的思路和技术，具体可参考看雪 2018 峰会回顾 [1]。

我以前分析的设备，固件存储于 tsop8 角封装的 nor flash，可以直接通过芯片夹夹取，或者直接焊下 flash 利用芯片座提取，然后无脑 binwalk 获得整个文件系统。但最近分析的设备，固件存储于 tsop48 角封装的 nand flash，没有对应的芯片夹，而且要求有一定的焊接技术。此外，由于 nandflash 存储的特性 [2]（如 OOB 数据的干扰），即使成功进行了物理提取，后续的数据处理也相当复杂。（在这里也希望有师傅能出一篇物理提取 nand flash 固件过程的教程，我实在不会 TAT）

接下来，我将结合最近的实验，与各位分享下本人在 nand flash 固件提取过程中，摸索和总结出来的一种利用 UART 串口调试提取固件的方法。由于本人能力有限，如有错误，还请各位师傅提出指正。

**_2_**

前提条件

UART 串口调试，可进入 linux 系统命令行。

**_3_**

基本概念

MTD（MemoryTechnology Device），存储技术设备，用于访问存储设备（ROM，flash）的 Linux 子系统。

通过 proc 文件系统查看 mtd 设备的分区情况，可以发现 mtdN 和 mtdblockN 描述的是同一个 MTD 分区，对应同一个硬件分区。两者是同一个 MTD 分区的两种不同描述：mtdN 是实现 MTD 分区所对应的字符设备，而 mtdblockN 设备则是在对应生成的块设备，两者内容一致，但具体的 ioctl 命令操作是不同的。

**_4_**

实例

出于保密性，在这里不透露具体型号。通过简要分析和丝印查阅，可以得知固件存储于红色框的 flash 中，如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_jpg/PUubqXlrzBTw3hYa7615LibsOe3Tt1gPKqdewKlVnNm84bQPm0J2CCV0svE104x7pAE2jbYznibejjficIt5pNCog/640?wx_fmt=jpeg)

但幸运的是，电路板上留存了 UART 调试串口，并且标注了各个接口的属性（GND、RX、TX 等）。接下来就可以通过连接 UART 进行串口调试的操作。

连接后，我使用的是 SecureCRT 与其进行通信。选择好正确的串口号和波特率（波特率的测试一般是从 9600 开始，可参照 SecureCRT 提供的常见波特率进行测试，如下图所示）。当界面有输出，且为正常字符，则连接正确。

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBTw3hYa7615LibsOe3Tt1gPKkEnVibxbuFAFG48LUFh58hYJRUx7HJCVN9XaLezbtKk1CviaA7JIYwtA/640?wx_fmt=png)

但是值得注意的是，系统在启动成功后，是关闭了 UART 调试 shell 的，此时只能看到系统日志的输出，而无法输入相关的命令对其进行操作，如下图所示。  

![](https://mmbiz.qpic.cn/mmbiz_jpg/PUubqXlrzBTw3hYa7615LibsOe3Tt1gPKibsNqTxYDjcmCymJ5EoqibYngqLSH6YuvFhdeT1Tkkls3ibPlrhGB0oCA/640?wx_fmt=jpeg)

仔细观察设备启动的全过程，我们发现其 bootloader 启动时，给我们提供了一次进入系统的机会，即在某个时候按下 f 可进入 failsafe mode，而在该模式下，我们可获取其中的 linux shell 并进行命令输入，即可 “看” 到整个设备的文件系统，如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBTw3hYa7615LibsOe3Tt1gPKsDXBj6J0LOHuUc2RgLXw2XdMkwe7scgM5c4ZbAYqM9wc31V51ia2qGA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBTw3hYa7615LibsOe3Tt1gPKOxbO5Ocm0SlraYvrHG9crUY9hEydbfAVscWxvKtUiaalTTmoa5ia5RlA/640?wx_fmt=png)

然而，由于此时设备并没有完全启动成功，所以其与外界是断联的，无法与外界进行通信。而这显然不能很好地帮助我们进行分析。那么如何在断网的情况下，导出整个文件系统，则是接下来需要解决的问题。

通过查看 / proc/mtd，可以得知各个 mtd 分区的基本信息描述，其中 mtd10，mtd11，mtd13 则有可能是我们所需分析的文件系统，如下图所示。

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBTw3hYa7615LibsOe3Tt1gPKgb1iaIO26iaLpSNjRvrSibbZW6v7OYdn5N0NBXDvVjBZLhrsvUzJab2hA/640?wx_fmt=png)

由于此时设备与我们的交互只能停留在命令行的回显中，一个很巧妙的方法则是将对应的 mtd 分区内容转换为可见字符（如 hexdump，base64），我们记录命令行的输出回显则可以获取整个文件系统。但是这里需要注意的是，由于 mtd 分区内容较多，且嵌入式设备处理性能有限，只能通过结合 SecureCRT 脚本编写，分段记录 mtd 分区。

关键代码如下：

```
def send_cmd(fp,offset,step):     crt.Screen.Synchronous = True      # Send the initial command then throw out the first linefeed that we      # see by waiting for it.         crt.Screen.Send("hexdump {} -s {} -n {}\n".format("/dev/mtdN",offset,step))      crt.Screen.WaitForString("\n")        # Create an array of strings to wait for.      promptStr = "root"       waitStrs = ["\n", promptStr]        row = 1       while True:          # Wait for the linefeed at the end of each line, or the shell          # prompt that indicates we're done.          result = crt.Screen.WaitForStrings( waitStrs )           # If we saw the prompt, we're done.          if result == 2:              break          # The result was 1 (we got a linefeed, indicating that we          # received another line of of output). Fetch current row number          # of the cursor and read the first 20 characters from the screen          # on that row.           #           # This shows how the 'Get' function can be used to read          # line-oriented output from a command, Subtract 1 from the          # currentRow to since the linefeed moved currentRow down by one.          #            screenrow = crt.Screen.CurrentRow - 1          readline = crt.Screen.Get(screenrow, 1, screenrow, 48)          readline = readline.strip()                  # NOTE: We read 48 characters from the screen 'readline' may          # contain trailing whitespace if the data was less than 48          # characters wide.           # Write the line out with an appended end-of-line sequence          fp.write(readline)             crt.Screen.Synchronous = False
```

offset 与 step 则是对应 hexdump 的偏移以及显示字节数，可根据实际需要进行设置。

**_5_**

总结

本文总结了一种利用 UART 串口调试获取设备的文件系统的方法，其关键在于通过 hexdump 或 base64 等将不可见字符转换为终端可回显的字符。

本方法的最大限制则是电路板中需要有 UART 调试串口并且设备存在相关的转换命令（虽然 hexdump 是很基本的命令了）。

**_6_**

参考链接

[1] https://bbs.pediy.com/thread-230095.htm

[2] https://zhuanlan.zhihu.com/p/26745577

![](https://mmbiz.qpic.cn/mmbiz_gif/PUubqXlrzBRH2vOmzbCqYb35uicIicQcxDR3lbWnKxpic9icIjYzbsJjISBQEicVFia5IOsHMULFVHiakxSAQSlj8cmVg/640?wx_fmt=gif)

结束

  

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组 IOT + 工控 + 样本分析 长期招新  

欢迎联系 admin@chamd5.org

  

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBR8nk7RR7HefBINILy4PClwoEMzGCJovye9KIsEjCKwxlqcSFsGJSv3OtYIjmKpXzVyfzlqSicWwxQ/640?wx_fmt=jpeg)