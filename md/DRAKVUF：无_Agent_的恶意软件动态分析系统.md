> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ETUXXpcvtYLW6gRAZ18hpg)

**介绍**
------

DRAKVUF 是一款无 Agent 的恶意软件动态分析系统，它基于 Xen、LibVMI、Volatility、Rekall。它能深度追踪病毒样本，从内存中提取被删除的文件，并且无需在虚拟机里安装别的分析软件。

**硬件要求**
--------

DRAKVUF 使用 Intel CPU 中的硬件虚拟化扩展技术。你需要支持虚拟化 (VT-x) 和 EPT(ExtendedPage Tables)的 Intel CPU。DRAKVUF 不能在其他 CPU 上运行 (如 AMD) 或者不支持虚拟化扩展的 CPU。

**支持系统**
--------

DRAKVUF 目前支持 Windows 7，32 位和 64 位系统

**演示**
------

使用 DRAKVUF 追踪 Windows 内部内核函数，包括堆分配

这个演示展示的是 DRAKVUF 中的进程注入组件，它能够在客机中执行任意可执行文件，不需要任何在客机中安装的帮助程序。演示中我们劫持了 Windows 任务管理器来执行我们的任务。

从内存中提取被删除的文件。很多病毒 droppes 的文件只会出现在内存中，不会在硬盘出现。

目前状态
----

目前有以下的核心功能：

> 无 Agent 执行恶意软件;
> 
> 无 Agent 监控 Windows 内部内核函数;
> 
> 客机多 vCPU 支持;
> 
> 追踪堆分配;
> 
> 追踪被访问的文件;
> 
> 在文件被删除前从内存中提取文件;
> 
> 通过写时拷贝内存和硬盘来克隆分析虚拟机;

注意 DRAKVUF 仍在早期开发阶段，因此缺少其他恶意软件分析器具备的功能。还有很多的提升空间，例如：

> 生成 JSON/MySQL/MongoDB 的结构化的日志;
> 
> 将提取的文件自动提交到 VirusTotal;
> 
> Linux 支持;
> 
> 使用 Run-time 重复数据删除技术删除 Xen 共享内存中未使用的内存;
> 
> 整合恶意软件分析功能，如 CRITS;

由于 DRAKVUF 是一个开源项目，欢迎移步 Github 主页提交补丁和 bug。更多信息可访问项目 Wiki

**安装指导**
--------

12/31/2015 更新

如果安装了旧版本的 DRAKVUF，阅读指导打开系统中的 Xen altp2m！

要在基于 Debian 的 Linux 上 buildXen 和 DRAKVUF 就需要安装以下的包。以下内容在 Debian Jessie 和 Ubuntu14.04 LTS 上测试通过

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xrDmtBqYQVdoTibSpdtkVv0icTibkYfRuc7OWoibaNPAyh7LCljeNwWMHJQ/0?wx_fmt=png)  

你可以从 repository 安装 Xen，但是我们还是建议用源码 build

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xhxogRxnjFahia8HEtNV2BDaplYdppHqGBZlibLBQI0ibmHleyzq5y2P4Q/0?wx_fmt=png)  

结果应该显示：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xhuI31HYF4KEMQHdC26fvicHAuXOQDMPViadBz0WPRYw5drXku0D29gJA/0?wx_fmt=png)  

安装 Xen dom0，分配 4GB RAM 和两个专用的 CPU 内核：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xDU4RSwGDX0HibURC5F4zmDrRUHmfmWazsPSm3x2LWqRpIkdKTfRDcng/0?wx_fmt=png)  

还要确保你的内核相对较新 (版本大于 3.8 应该就行了

```
uname -r
```

进入 Xen 之后，验证一切是否正常：

sudo xen-detect

输出的结果应该是：Running in PV context on Xen v4.6

```
输入xl list
```

输出的结果应该类似于：

建立一个 LVM 卷组存档虚拟机磁盘，然后创建卷：

```
lvcreate -L20G -n windows7-sp1 vg
```

用 ISO 安装 Windows 7：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xvzZZLmuhoENgNPkticNWcjojsGaib2beBcRice3I2RcvgWwefYqfgmRmA/0?wx_fmt=png)  

下载 LibVMI 的 DRAKVUF 分支，并准备 build：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xeLhHibn6jJLhUZjfvW7nwITtpNdE7Xic5EiauhdB0lvtHJQFTxZicicBnpA/0?wx_fmt=png)

输出的结果应该类似于：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xr8iciaO8QUs6yr8PkEZZgZ7SHq5StYXTkLvibtpjL3zUF2w2Vl5lXOwmQ/0?wx_fmt=png)  

Build 并安装 LibVMI：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xzDgxlicXn8rBygNUg1rleLWlRuJ46oLibbnRQpjdmgibAQS4gHgK92PRg/0?wx_fmt=png)  

下载 Volatility：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xYLPHZULkIew6fxM3JTibSk1fyFjkDzpp1VNlvCLvAjsD6zmNcIXc8EQ/0?wx_fmt=png)  

下载 Rekall 并安装：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xpZTkG00iagQ5Q4icibT9V4m1Nx99HCvXT0BjZrPdMCNdRMibfbNNHibiaRkw/0?wx_fmt=png)  

接下来我们要为 Windows 域创建 Rekall 档案，首先我们要用 LibVMI win-guid 工具获得 WIndows 内核的调试信息。例如：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xIbE3y7k5jILqPxPz87ia0AQEMqfrWSiaI0ibaBM0P31TJJu4GlOFvcXHA/0?wx_fmt=png)  

关键的地方：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xpfHvaGmJRealf95v04Wiau981icoVKyn8f0GSCQTEK6bjujPz93nn8Kg/0?wx_fmt=png)  

生成 Rekall 档案：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xSnVmHK03Hbm0aSicZMkm54n0t3esNSlDDcnRrwkNImOlicP5ibE6N8nrg/0?wx_fmt=png)  

档案生成后我们可以创建 LibVMI config：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xWl70pSZrV34cROtf7Eia0yPDicltJVt46BvV92to4IGiahgdjSxzyMhNw/0?wx_fmt=png)  

用进程列表查看 LibVMI 是否在运行：

```
process-list windows7-sp1
```

输出结果应该类似于：

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dnA6S8eCtYo24mE09Yx9U1xHCXC1cKqicI6mqp823PaR76xib6Wh6ecWJmwicYBzITFyJWgMmLJkAYwA/0?wx_fmt=png)  

开始 build 并安装 DRAKVUF：

```
git clone https://github.com/tklengyel/drakvufcd drakvufautoreconf -vi./configuremake
```

追踪系统的执行：

```
./src/drakvuf -r <rekall profile> -d <domid>
```

例如：  

```
./src/drakvuf -r /root/windows7-sp1.rekall.json -d 7
```

![](http://mmbiz.qpic.cn/mmbiz/beW9MrR87dkcnlOAg7Prg7JAn46BWEqHVlGjRAgIZWumVgAF5ImfzkibFAnvWjxWic8n8cPQknqVQV08fb0dIFJg/0?wx_fmt=png)