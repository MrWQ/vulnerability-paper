> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/gJFiw-_F0_Murvfv_kkfEQ)

> **作者：** **悠悠 i**
> 
> **链接：https://www.cnblogs.com/youyoui/p/10680329.html**

Linux 环境变量配置
------------

在自定义安装软件的时候，经常需要配置环境变量，下面列举出各种对环境变量的配置方法。

下面所有例子的环境说明如下：

*   系统：Ubuntu 14.0
    
*   用户名：uusama
    
*   需要配置 MySQL 环境变量路径：/home/uusama/mysql/bin
    

### Linux 读取环境变量

读取环境变量的方法：

*   `export`命令显示当前系统定义的所有环境变量
    
*   `echo $PATH`命令输出当前的`PATH`环境变量的值
    

这两个命令执行的效果如下

```
uusama@ubuntu:~$ export
declare -x HOME="/home/uusama"
declare -x LANG="en_US.UTF-8"
declare -x LANGUAGE="en_US:"
declare -x LESSCLOSE="/usr/bin/lesspipe %s %s"
declare -x LESSOPEN="| /usr/bin/lesspipe %s"
declare -x LOG
declare -x MAIL="/var/mail/uusama"
declare -x PATH="/home/uusama/bin:/home/uusama/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
declare -x SSH_TTY="/dev/pts/0"
declare -x TERM="xterm"
declare -x USER="uusama"

uusama@ubuntu:~$ echo $PATH
/home/uusama/bin:/home/uusama/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

其中`PATH`变量定义了运行命令的查找路径，以冒号`:`分割不同的路径，使用`export`定义的时候可加双引号也可不加。

### Linux 环境变量配置方法一：  export  PATH

使用`export`命令直接修改`PATH`的值，配置 MySQL 进入环境变量的方法:

```
export PATH=/home/uusama/mysql/bin:$PATH

# 或者把PATH放在前面
export PATH=$PATH:/home/uusama/mysql/bin
```

注意事项：

*   生效时间：立即生效
    
*   生效期限：当前终端有效，窗口关闭后无效
    
*   生效范围：仅对当前用户有效
    
*   配置的环境变量中不要忘了加上原来的配置，即`$PATH`部分，避免覆盖原来配置
    

### Linux 环境变量配置方法二：     vim ~/.bashrc

通过修改用户目录下的`~/.bashrc`文件进行配置：

```
vim ~/.bashrc

# 在最后一行加上
export PATH=$PATH:/home/uusama/mysql/bin
```

注意事项：

*   生效时间：使用相同的用户打开新的终端时生效，或者手动`source ~/.bashrc`生效
    
*   生效期限：永久有效
    
*   生效范围：仅对当前用户有效
    
*   如果有后续的环境变量加载文件覆盖了`PATH`定义，则可能不生效
    

### Linux 环境变量配置方法三：  vim ~/.bash_profile

和修改`~/.bashrc`文件类似，也是要在文件最后加上新的路径即可：

```
vim ~/.bash_profile

# 在最后一行加上
export PATH=$PATH:/home/uusama/mysql/bin
```

注意事项：

*   生效时间：使用相同的用户打开新的终端时生效，或者手动`source ~/.bash_profile`生效
    
*   生效期限：永久有效
    
*   生效范围：仅对当前用户有效
    
*   如果没有`~/.bash_profile`文件，则可以编辑`~/.profile`文件或者新建一个
    

### Linux 环境变量配置方法四：vim /etc/bashrc   

该方法是修改系统配置，需要管理员权限（如 root）或者对该文件的写入权限：

```
# 如果/etc/bashrc文件不可编辑，需要修改为可编辑
chmod -v u+w /etc/bashrc

vim /etc/bashrc

# 在最后一行加上
export PATH=$PATH:/home/uusama/mysql/bin
```

注意事项：

*   生效时间：新开终端生效，或者手动`source /etc/bashrc`生效
    
*   生效期限：永久有效
    
*   生效范围：对所有用户有效
    

### Linux 环境变量配置方法五：    vim /etc/profile

该方法修改系统配置，需要管理员权限或者对该文件的写入权限，和`vim /etc/bashrc`类似：

```
# 如果/etc/profile文件不可编辑，需要修改为可编辑
chmod -v u+w /etc/profile

vim /etc/profile

# 在最后一行加上
export PATH=$PATH:/home/uusama/mysql/bin
```

注意事项：

*   生效时间：新开终端生效，或者手动`source /etc/profile`生效
    
*   生效期限：永久有效
    
*   生效范围：对所有用户有效
    

### Linux 环境变量配置方法六：vim /etc/environment

该方法是修改系统环境配置文件，需要管理员权限或者对该文件的写入权限：

```
# 如果/etc/bashrc文件不可编辑，需要修改为可编辑
chmod -v u+w /etc/environment

vim /etc/profile

# 在最后一行加上
export PATH=$PATH:/home/uusama/mysql/bin
```

注意事项：

*   生效时间：新开终端生效，或者手动`source /etc/environment`生效
    
*   生效期限：永久有效
    
*   生效范围：对所有用户有效
    

  Linux 环境变量加载原理解析
------------------

上面列出了环境变量的各种配置方法，那么 Linux 是如何加载这些配置的呢？是以什么样的顺序加载的呢？

特定的加载顺序会导致相同名称的环境变量定义被覆盖或者不生效。

### 环境变量的分类

环境变量可以简单的分成用户自定义的环境变量以及系统级别的环境变量。

*   用户级别环境变量定义文件：`~/.bashrc`、`~/.profile`（部分系统为：`~/.bash_profile`）
    
*   系统级别环境变量定义文件：`/etc/bashrc`、`/etc/profile`(部分系统为：`/etc/bash_profile`）、`/etc/environment`
    

另外在用户环境变量中，系统会首先读取`~/.bash_profile`（或者`~/.profile`）文件，如果没有该文件则读取`~/.bash_login`，根据这些文件中内容再去读取`~/.bashrc`。

### 测试 Linux 环境变量加载顺序的方法

为了测试各个不同文件的环境变量加载顺序，我们在每个环境变量定义文件中的第一行都定义相同的环境变量`UU_ORDER`，该变量的值为本身的值连接上当前文件名称。

需要修改的文件如下：

*   /etc/environment
    
*   /etc/profile
    
*   /etc/profile.d/test.sh，新建文件，没有文件夹可略过
    
*   /etc/bashrc，或者 / etc/bash.bashrc
    
*   ~/.bash_profile，或者~/.profile
    
*   ~/.bashrc
    

在每个文件中的第一行都加上下面这句代码，并相应的把冒号后的内容修改为当前文件的绝对文件名。

`export UU_ORDER="$UU_ORDER:~/.bash_profile"`

修改完之后保存，新开一个窗口，然后`echo $UU_ORDER`观察变量的值：

```
uusama@ubuntu:~$ echo $UU_ORDER

$UU_ORDER:/etc/environment:/etc/profile:/etc/bash.bashrc:/etc/profile.d/test.sh:~/.profile:~/.bashrc
```

可以推测出 Linux 加载环境变量的顺序如下：

1.  /etc/environment
    
2.  /etc/profile
    
3.  /etc/bash.bashrc
    
4.  /etc/profile.d/test.sh
    
5.  ~/.profile
    
6.  ~/.bashrc
    

### Linux 环境变量文件加载详解

由上面的测试可容易得出 Linux 加载环境变量的顺序如下，：

系统环境变量 -> 用户自定义环境变量  
/etc/environment -> /etc/profile -> ~/.profile

打开`/etc/profile`文件你会发现，该文件的代码中会加载`/etc/bash.bashrc`文件，然后检查`/etc/profile.d/`目录下的`.sh`文件并加载。

```
# /etc/profile: system-wide .profile file for the Bourne shell (sh(1))
# and Bourne compatible shells (bash(1), ksh(1), ash(1), ...).

if [ "$PS1" ]; then
  if [ "$BASH" ] && [ "$BASH" != "/bin/sh" ]; then
    # The file bash.bashrc already sets the default PS1.
    # PS1='\h:\w\$ '
    if [ -f /etc/bash.bashrc ]; then
      . /etc/bash.bashrc
    fi
  else
    if [ "`id -u`" -eq 0 ]; then
      PS1='# '
    else
      PS1='$ '
    fi
  fi
fi

if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/*.sh; do
    if [ -r $i ]; then
      . $i
    fi
  done
  unset i
fi
```

其次再打开`~/.profile`文件，会发现该文件中加载了`~/.bashrc`文件。

```
# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
  . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin directories
PATH="$HOME/bin:$HOME/.local/bin:$PATH"
```

从`~/.profile`文件中代码不难发现，`/.profile`文件**只在用户登录的时候读取一次**，而`/.bashrc`会在每次运行`Shell`脚本的时候读取一次。

### 一些小技巧

可以自定义一个环境变量文件，比如在某个项目下定义`uusama.profile`，在这个文件中使用`export`定义一系列变量，然后在`~/.profile`文件后面加上：`sourc uusama.profile`，这样你每次登陆都可以在 Shell 脚本中使用自己定义的一系列变量。

也可以使用`alias`命令定义一些命令的别名，比如`alias rm="rm -i"`（双引号必须），并把这个代码加入到`~/.profile`中，这样你每次使用`rm`命令的时候，都相当于使用`rm -i`命令，非常方便。

**推荐↓↓↓**

![](https://mmbiz.qpic.cn/mmbiz_jpg/NVvB3l3e9aG5kWic5P8XOwFOhXKjibAt6Yfb1QuqSRZaV5QGHtqqXZFWkia50TDjpWTBqG8Huj3aMlA6cOE9cBVkQ/640?wx_fmt=jpeg)

**Linux 学习**