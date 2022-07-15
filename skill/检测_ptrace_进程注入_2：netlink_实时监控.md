> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/0Jnm3IbqyFUovAqublae1Q)

> 通过`Netlink`方式来实时获取`ptrace`事件

一般`ptrace`注入过程时间非常短，而遍历`/proc`的时间会比较长，往往会错过那些快速注入的恶意进程。而把扫描频次调高，又会引起对系统性能的占用。

那么有没有一种实时获取的方式呢？

要实时获取，就要和内核打交道，这时候，又要祭起`netlink`了。

`netlink socket`在`Kernel Connector`方式是支持进程实时监控的，看一下有没有监控到`ptrace`事件。

看一下`/usr/include/linux/cn_proc.h`

```
/* SPDX-License-Identifier: LGPL-2.1 WITH Linux-syscall-note *//* * cn_proc.h - process events connector * * Copyright (C) Matt Helsley, IBM Corp. 2005 * Based on cn_fork.h by Nguyen Anh Quynh and Guillaume Thouvenin * Copyright (C) 2005 Nguyen Anh Quynh <aquynh@gmail.com> * Copyright (C) 2005 Guillaume Thouvenin <guillaume.thouvenin@bull.net> * * This program is free software; you can redistribute it and/or modify it * under the terms of version 2.1 of the GNU Lesser General Public License * as published by the Free Software Foundation. * * This program is distributed in the hope that it would be useful, but * WITHOUT ANY WARRANTY; without even the implied warranty of * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. */#ifndef CN_PROC_H#define CN_PROC_H#include <linux/types.h>/* * Userspace sends this enum to register with the kernel that it is listening * for events on the connector. */enum proc_cn_mcast_op { PROC_CN_MCAST_LISTEN = 1, PROC_CN_MCAST_IGNORE = 2};/* * From the user's point of view, the process * ID is the thread group ID and thread ID is the internal * kernel "pid". So, fields are assigned as follow: * *  In user space     -  In  kernel space * * parent process ID  =  parent->tgid * parent thread  ID  =  parent->pid * child  process ID  =  child->tgid * child  thread  ID  =  child->pid */struct proc_event { enum what {  /* Use successive bits so the enums can be used to record   * sets of events as well   */  PROC_EVENT_NONE = 0x00000000,  PROC_EVENT_FORK = 0x00000001,  PROC_EVENT_EXEC = 0x00000002,  PROC_EVENT_UID  = 0x00000004,  PROC_EVENT_GID  = 0x00000040,  PROC_EVENT_SID  = 0x00000080,  PROC_EVENT_PTRACE = 0x00000100,  PROC_EVENT_COMM = 0x00000200,  /* "next" should be 0x00000400 */  /* "last" is the last process event: exit,   * while "next to last" is coredumping event */  PROC_EVENT_COREDUMP = 0x40000000,  PROC_EVENT_EXIT = 0x80000000 } what; __u32 cpu; __u64 __attribute__((aligned(8))) timestamp_ns;  /* Number of nano seconds since system boot */ union { /* must be last field of proc_event struct */  struct {   __u32 err;  } ack;  struct fork_proc_event {   __kernel_pid_t parent_pid;   __kernel_pid_t parent_tgid;   __kernel_pid_t child_pid;   __kernel_pid_t child_tgid;  } fork;  struct exec_proc_event {   __kernel_pid_t process_pid;   __kernel_pid_t process_tgid;  } exec;  struct id_proc_event {   __kernel_pid_t process_pid;   __kernel_pid_t process_tgid;   union {    __u32 ruid; /* task uid */    __u32 rgid; /* task gid */   } r;   union {    __u32 euid;    __u32 egid;   } e;  } id;  struct sid_proc_event {   __kernel_pid_t process_pid;   __kernel_pid_t process_tgid;  } sid;  struct ptrace_proc_event {   __kernel_pid_t process_pid;   __kernel_pid_t process_tgid;   __kernel_pid_t tracer_pid;   __kernel_pid_t tracer_tgid;  } ptrace;  struct comm_proc_event {   __kernel_pid_t process_pid;   __kernel_pid_t process_tgid;   char           comm[16];  } comm;  struct coredump_proc_event {   __kernel_pid_t process_pid;   __kernel_pid_t process_tgid;   __kernel_pid_t parent_pid;   __kernel_pid_t parent_tgid;  } coredump;  struct exit_proc_event {   __kernel_pid_t process_pid;   __kernel_pid_t process_tgid;   __u32 exit_code, exit_signal;   __kernel_pid_t parent_pid;   __kernel_pid_t parent_tgid;  } exit; } event_data;};#endif /* CN_PROC_H */
```

可以看到有`PROC_EVENT_PTRACE`和`ptrace_proc_event`处理`ptrace`事件。

写一个小程序`procmon.c`看看

```
#include <unistd.h>#include <string.h>#include <sys/socket.h>#include <linux/netlink.h>#include <linux/connector.h>#include <linux/cn_proc.h>#include <errno.h>#include <sys/select.h>#include <sys/types.h>#include <sys/time.h>#include <stdio.h>#include <stdlib.h>typedef struct __attribute__((aligned(NLMSG_ALIGNTO))) {    struct nlmsghdr nl_hdr;    struct __attribute__((__packed__))    {        struct cn_msg cn_msg;        enum proc_cn_mcast_op cn_mcast;    };} register_msg_t;typedef struct __attribute__((aligned(NLMSG_ALIGNTO))){    struct nlmsghdr nl_hdr;    struct __attribute__((__packed__))    {        struct cn_msg cn_msg;        struct proc_event proc_ev;    };} event_msg_t;int main( ){    int rc;    int nl_sock;    struct sockaddr_nl sa_nl;    register_msg_t nlcn_msg;    event_msg_t proc_msg;    fd_set readfds;    int max_fd;    struct timeval tv;    nl_sock = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_CONNECTOR);    if (nl_sock == -1)    {        printf("Can't open netlink socket\n");        return -1;    }    sa_nl.nl_family = AF_NETLINK;    sa_nl.nl_groups = CN_IDX_PROC;    sa_nl.nl_pid = getpid();    rc = bind(nl_sock, (struct sockaddr *)&sa_nl, sizeof(sa_nl));    if (rc == -1)    {        printf(  "Can't bind netlink socket\n");        close(nl_sock);        return -1;    }    // create listener    memset(&nlcn_msg, 0, sizeof(nlcn_msg));    nlcn_msg.nl_hdr.nlmsg_len = sizeof(nlcn_msg);    nlcn_msg.nl_hdr.nlmsg_pid = getpid();    nlcn_msg.nl_hdr.nlmsg_type = NLMSG_DONE;    nlcn_msg.cn_msg.id.idx = CN_IDX_PROC;    nlcn_msg.cn_msg.id.val = CN_VAL_PROC;    nlcn_msg.cn_msg.len = sizeof(enum proc_cn_mcast_op);    nlcn_msg.cn_mcast = PROC_CN_MCAST_LISTEN ;    rc = send(nl_sock, &nlcn_msg, sizeof(nlcn_msg), 0);    if (rc == -1)    {        printf( "can't register to netlink\n");        close( nl_sock );        return -1;    }    while (1)    {        FD_ZERO(&readfds);        FD_SET(nl_sock, &readfds);        max_fd = nl_sock + 1;        rc = select(max_fd, &readfds, NULL, NULL, NULL);        if (-1 == rc)        {            if (errno == EINTR)            {                continue;            }            printf( "failed to listen to netlink socket, errno=(%d:%m)\n", errno);            return rc;        }        if (FD_ISSET(nl_sock, &readfds))        {            rc = recv(nl_sock, &proc_msg, sizeof(proc_msg), 0);            if (rc > 0)            {                switch (proc_msg.proc_ev.what)                {                case proc_event::PROC_EVENT_PTRACE:                    if ( proc_msg.proc_ev.event_data.ptrace.tracer_pid != 0 )                    {                        printf("tracer pid:%d, tracer thread id: %d, tracee pid:%d, tracee thread id:%d\n",                                 proc_msg.proc_ev.event_data.ptrace.tracer_tgid,                                 proc_msg.proc_ev.event_data.ptrace.tracer_pid,                                proc_msg.proc_ev.event_data.ptrace.process_tgid,                                proc_msg.proc_ev.event_data.ptrace.process_pid);                        char cmd[64];                        memset( cmd , 0, 64 );                        snprintf( cmd , 63, "cat /proc/%d/cmdline", proc_msg.proc_ev.event_data.ptrace.tracer_tgid );                        system(  cmd );                        printf("\n");                    }                    break;                default:                    break;                }            }            else if (rc == -1)            {                if (errno == EINTR)                {                    continue;                }            }        }    }    return 0;}
```

里面这一段是打印出`tracer`的信息的

```
printf("tracer pid:%d, tracer thread id: %d, tracee pid:%d, tracee thread id:%d\n",                                 proc_msg.proc_ev.event_data.ptrace.tracer_tgid,                                 proc_msg.proc_ev.event_data.ptrace.tracer_pid,                                proc_msg.proc_ev.event_data.ptrace.process_tgid,                                proc_msg.proc_ev.event_data.ptrace.process_pid);                        char cmd[64];                        memset( cmd , 0, 64 );                        snprintf( cmd , 63, "cat /proc/%d/cmdline", proc_msg.proc_ev.event_data.ptrace.tracer_tgid );                        system(  cmd );                        printf("\n");
```

运行一下`procmon`

```
[root@localhost proc]# ./procmon 
```

启动一下`GDB`看看

```
[root@localhost code]# gdb -p 2238 -q
Attaching to process 2238
```

`procmon`的窗口信息变成如下

```
[root@localhost proc]# ./procmon 
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2238
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2265
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2267
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2268
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2269
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2270
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2271
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2272
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2273
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2274
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2275
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2276
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2277
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2278
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2279
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2280
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2293
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2300
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2301
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2306
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2307
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2308
gdb-p2238-q
tracer pid:33008, tracer thread id: 33008, tracee pid:2238, tracee thread id:2309
gdb-p2238-q
```

看进程 2238 下的线程，是和上面对应的。

```
[buckxu@localhost proc]$ ls /proc/2238/task/
2238  2265  2267  2268  2269  2270  2271  2272  2273  2274  2275  2276  2277  2278  2279  2280  2293  2300  2301  2306  2307  2308  2309
```

说明这个方式可以检测到`ptrace`事件，而且是实时。那么，针对那些一附加上去立马注入的短时间存在的`tracer`, 能否实时获取到`tracer`的信息?

重新调整一下`gdb`的参数， 让它一附加到进程立马解绑，再退出

```
[root@localhost code]# gdb -p 2238 -q -ex "detach" -ex "q"
Attaching to process 2238
[New LWP 2265]
[New LWP 2267]
[New LWP 2268]
[New LWP 2269]
[New LWP 2270]
[New LWP 2271]
[New LWP 2272]
[New LWP 2273]
[New LWP 2274]
[New LWP 2275]
[New LWP 2276]
[New LWP 2277]
[New LWP 2278]
[New LWP 2279]
[New LWP 2280]
[New LWP 2293]
[New LWP 2300]
[New LWP 2301]
[New LWP 2306]
[New LWP 2307]
[New LWP 2308]
[New LWP 2309]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
0x00007f2f1f5a10f7 in epoll_wait () from /lib64/libc.so.6
Detaching from program: /var/ossec/bin/ossec-remoted, process 2238
[Inferior 1 (process 2238) detached]
[root@localhost code]# 
```

再看一下`procmon`的打印

```
[root@localhost proc]# ./procmon 
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2238
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2265
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2267
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2268
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2269
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2270
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2271
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2272
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2273
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2274
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2275
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2276
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2277
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2278
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2279
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2280
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2293
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2300
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2301
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2306
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2307
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2308
gdb-p2238-q-exdetach-exq
tracer pid:33146, tracer thread id: 33146, tracee pid:2238, tracee thread id:2309
gdb-p2238-q-exdetach-exq
```

说明它是可以实时抓取`tracer`的信息。

这种方法有一处不足就是，无法获取`ptrace`的，是附加，解绑，还是获取 / 设置寄存器，读 / 写内存。

=========================================

**文中和文末的小广广，渴望你手指的触碰！！！**

**请关注，转发，点 “在看”，谢谢！！**

**如需要转载，请在公众号留言！！**

![](https://mmbiz.qpic.cn/mmbiz_jpg/QXsgGBUcicbz1VnU8EV2vjtY6FOibQx28yd7dMqTwvOuDfVtuenjlMdNfaKv5Mia3pejJFpGlHibSicgFHFhHHNtAqw/640?wx_fmt=jpeg)