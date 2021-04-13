> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9394)

0x0 前言  
D-Link DIR-816 A2 是中国台湾友讯（D-Link）公司的一款无线路由器。攻击者可借助‘datetime’参数中的 shell 元字符利用该漏洞在系统上执行任意命令。

0x1 准备  
固件版本 1.10B05：[http://support.dlink.com.cn:9000/ProductInfo.aspx?m=DIR-816](http://support.dlink.com.cn:9000/ProductInfo.aspx?m=DIR-816)

漏洞存在的程序：goahead

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142228-ccba80b0-937b-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142228-ccba80b0-937b-1.jpg)

0x2 工具  
静态分析工具：IDA

系统文件获取：binwalk

动态调试工具：qemu、IDA

0x3 测试环境  
本人使用 Ubuntu 16.04 虚拟机测试环境，qemu 模拟器模拟 D-Link DIR-816 A2 固件运行真实情景。

0x4 goahead 程序调试  
使用 binwalk 进行固件解包 (binwalk -Me DIR-816A2_v1.10CNB03_D77137.img)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142244-d5b99c96-937b-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142244-d5b99c96-937b-1.jpg)

通过 binwalk 可以解包出如下图的文件，squashfs-root 就是我们需要的文件系统。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142252-dad90f72-937b-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142252-dad90f72-937b-1.jpg)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142303-e14fe272-937b-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142303-e14fe272-937b-1.jpg)

一般可以通过 find -name "_index_" 可以搜索出 web 的根目录在哪个具体目录下。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142316-e9066856-937b-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142316-e9066856-937b-1.jpg)

通过 file ../../bin/goahead 命令 (由于本人已经进入到根目录下面，所以是../../bin/goahead)，可以看出该系统是 MIPS 架构，则 qemu 模拟器需要使用 MIPS 方式的模拟器。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142325-ee87ed22-937b-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142325-ee87ed22-937b-1.jpg)

sudo qemu-mipsel -L ../../ -g 1234 ../../bin/goahead

-g 使用 qemu 并将程序挂载在 1234 端口，等待调试。

-L 是根目录的所在的位置。

可以使用 IDA 远程调试连接 1234 端口，进行调试，获取使用 gdb 也可以调试。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142337-f5c5b9fc-937b-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142337-f5c5b9fc-937b-1.jpg)

如下图操作，IDA 即可开启远程调试。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142348-fc0397bc-937b-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142348-fc0397bc-937b-1.jpg)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142357-01785476-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142357-01785476-937c-1.jpg)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142407-074b3d78-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142407-074b3d78-937c-1.jpg)

经过测试，我们需要在 0x45C728 处下一个断点，因为此处的 bnez 会使程序退出，所以需要将 V0 寄存器的值修改为 1。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142420-0f30f708-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142420-0f30f708-937c-1.jpg)

同理需要在 0x45cdbc 地址下断点，并将 V0 寄存器修改为 0。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142434-1765d024-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142434-1765d024-937c-1.jpg)

两处地址都通过后，在网址中输入 [http://192.168.184.133/dir_login.asp，即可访问到登录页面。](http://192.168.184.133/dir_login.asp%EF%BC%8C%E5%8D%B3%E5%8F%AF%E8%AE%BF%E9%97%AE%E5%88%B0%E7%99%BB%E5%BD%95%E9%A1%B5%E9%9D%A2%E3%80%82)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142448-2029a85c-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142448-2029a85c-937c-1.jpg)

想进入路由器 web 操作页面，就必须先登录，在 web 服务器程序中用户名为空，而 web 页面有 JS 校验，必须需要输入用户名才能进行登录校验，那么可以修改登录校验的寄存器，让其成功运行登录。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142458-25bfdc64-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142458-25bfdc64-937c-1.jpg)

在 0x4570fc 地址处下断点，修改 V0 寄存器的值为 0。因为此处的 V0 是用户名的值，在登录页面中，我们是随意输入，所以肯定是不会正确的，那么就只有修改为 0 后才能跳转到正确的登录流程。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142509-2c2b27a2-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142509-2c2b27a2-937c-1.jpg)

登录成功后，会出现页面错误。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142517-31756d08-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142517-31756d08-937c-1.jpg)

再在网址中输入 [http://192.168.184.133/d_wizard_step1_start.asp，即可进入到登录成功后的页面。看到如下图，即可证明已经登录成功。](http://192.168.184.133/d_wizard_step1_start.asp%EF%BC%8C%E5%8D%B3%E5%8F%AF%E8%BF%9B%E5%85%A5%E5%88%B0%E7%99%BB%E5%BD%95%E6%88%90%E5%8A%9F%E5%90%8E%E7%9A%84%E9%A1%B5%E9%9D%A2%E3%80%82%E7%9C%8B%E5%88%B0%E5%A6%82%E4%B8%8B%E5%9B%BE%EF%BC%8C%E5%8D%B3%E5%8F%AF%E8%AF%81%E6%98%8E%E5%B7%B2%E7%BB%8F%E7%99%BB%E5%BD%95%E6%88%90%E5%8A%9F%E3%80%82)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142528-37d3058e-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142528-37d3058e-937c-1.jpg)

登录认证后，点击维护，再点击时间与日期，最后点击应用，此处便是漏洞触发点。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142540-3ebdfa98-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142540-3ebdfa98-937c-1.jpg)

最终可以通过构造 datetime 的值，执行任意命令。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142549-44056194-937c-1.jpg)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142549-44056194-937c-1.jpg)

0x5 总结  
这个固件可以锻炼 qemu 模拟器的使用以及 IDA 简单调试能力，在没有真实路由器的情况下 qemu 是非常好用的一款模拟工具，模拟很多款路由器。该程序还存在多个命令执行漏洞，非常适合练手。命令执行漏洞相对来说比较简单，但是杀伤力巨大，很适合新手入门。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210402142620-56d770aa-937c-1.gif)](https://xzfile.aliyuncs.com/media/upload/picture/20210402142620-56d770aa-937c-1.gif)