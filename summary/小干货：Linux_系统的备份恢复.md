> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/0WXPJXdH34mgkLa6T6lkpQ)

![](https://mmbiz.qpic.cn/mmbiz_png/K0TMNq37VN34SjBkXD1F1bzoW99Sgt0vnTfAgzHwic97l5buhJT5eEFMpM75h9gRsH2F36t2STxWBLl7u7gCj7w/640?wx_fmt=jpeg)

**tar 命令**
==========

### 副本（本机备份整个系统，以后还原还是还原到本机）

注意根目录下要有充足的可用空间用于备份。

```
cd /<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">#tar.gz格式<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">tar cvpzf system_backup.tar.gz / --exclude=/proc --exclude=/lost+found --exclude=/system_backup.tar.gz --exclude=/mnt --exclude=/sys<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;"><br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">#tar.bz2格式<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">tar cvpjf system_backup.tar.bz2 / --exclude=/proc --exclude=/lost+found --exclude=/system_backup.tar.bz2 --exclude=/mnt --exclude=/sys<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;"><br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;"><br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;"># 恢复系统<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">cd /<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">#上传文件到根目录下<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">tar xvpfz system_backup.tar.gz -C /<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">或<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">tar xvpfj system_backup.tar.bz2 -C /<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;"><br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">#创建备份时排除的目录<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">mkdir proc<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">mkdir lost+found<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">mkdir mnt<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">mkdir sys<br style="max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">
```

*   /proc 权限：文件所有者：root 群组：root 所有者：读取 执行 群组：读取 执行 其它：读取 执行
    
*   /lost+found 权限：文件所有者：root 群组：root 所有者：读取 写入 执行 群组：读取 执行 其它：读取 执行
    
*   /mnt 权限：文件所有者：root 群组：root 所有者：读取 写入 执行 群组：读取 执行 其它：读取 执行
    
*   /sys 权限：文件所有者：root 群组：root 所有者：读取 写入 执行 群组：读取 执行 其它：读取 执行
    

恢复完成重启以后，所以的事情都会和你备份的时候一模一样。

### 镜像（本机备份系统，还原到新主机上）

```
1,检查系统版本，在目标机上安装一样版本的系统(最简安装即可),分区格式，类型也一样（我没试过不一样的情况，不知道能否成功）lsb_release -auname -adf -Thfree -h2，备份源系统# 因为目标机和源主机硬件配置不同，所以排除dev，tmp；再适当增加你要排除的文件，如：--exclude=/root/*.bz2# 这里再mnt下有充足空间，所以保存到mnt下。cd /tar cvpzf /mnt/system_backup.tar.gz / --exclude=/mnt/system_backup.tar.gz \--exclude=/proc --exclude=/lost+found --exclude=/mnt --exclude=/sys --exclude=/dev \--exclude=/tmp --exclude=/media# 上传到目标主机scp /mnt/system_backup.tar.gz root@192.168.0.166:/mnt3,在目标机上用ISO、LiveCD等启动，挂载磁盘（一般会自动挂载到/media文件夹）sudo -s  cd /media/<对应的uuid号># 备份重要配置文件/boot/gurb/gurb.cfg /etc/fstab记录里面的UUID，# 删除重复文件# 除了上面备份系统时排除的一些文件夹外，比如说dev mnt media sys这些文件夹，其他全部删除。rm -rf root home usr lib lib64 etc var bin sbin opt boot run selinux vmlinuz initrd.img# 还原备份mount /dev/vda1 /mnt/1# 这里注意千万不要写/目录，会把现有的系统搞挂！！！应该是挂载的目录tar xvpfz system_backup.tar.gz -C /mnt/1cd /mnt/1       #此时你可以看到根目录的结构，但是编辑fstab文件发现是现有系统的fstabchroot ./       #执行chroot后会以./目录为根目录，这时编辑的文件就是真正的目标源文件了。还原后修改/etc/fstab里的UUID为刚刚备份的文件里面的信息，注意分区格式也要对应。修改/boot/gurb/gurb.cfg里的UUID为刚刚备份的文件里面的信息。修改网卡、IP配置文件，以防无法分配IP。（如果是虚拟机记得添加网卡，配置中等性能的显卡）如果有依赖于原有平台的服务，如内建NTP，Agent等监控程序；关闭服务，关闭开机自启；Ubuntu：在命令行输入runleve可以查看当前运行级别，一般默认是2查看/etc/rc2.d目录中的S开头的服务都是会开机自动运行的；里面是软链接，想添加的话自己建一个链接文件就可以，S代表start，后面数字是启动顺序，删除软链接。同时删除/etc/init.d/下对应的脚本。vim /etc/init.d/rc.localCentos:用systemctl完成上述步骤后exit      #退出chrootcd ~umount /mnt/1# 一切完成后就可以重启了，不出意外就正常启动系统了（启动后原来安装系统时设置的账户等全部消失；账户和源主机一致）。若开机Grub提示“boot error 15 :Error 15 file not found”解决方法：请检查GRUB相关文件的内核文件所在位置。通常与/boot分区有关。若开机Grub提示“dracut:dono't how to hand root=f078”解决方法：将root=UUID改成root=/dev/sdaX这种格式。若开机系统提示/usr/libexec/gconf-sanity-check-2退出状态256的解决解决方法：chmod 777 /tmp
```

**rsync 命令**
------------

注意目标分区的格式最好是 NTFS、FAT、EXT 之类的格式，避免遇到大于 4G 的文件无法备份的问题。

```
#最好有其他分区或外接存储设备，挂载好，df -lh看挂载点。#备份rsync -Pa / /media/usb/backup_20170410 --exclude=/media/* --exclude=/sys/* --exclude=/proc/* --exclude=/mnt/* --exclude=/tmp/*#恢复rsync -Pa /media/usb/backup_20170410 /
```

**dd 命令**
---------

dd 命令属于扇区克隆，目标分区要比备份分区要大，即使没有使用的空间也会被原样克隆下来，会比较慢。

```
#备份df -h   #查看系统所在分区dd if=/dev/sda1 of=/dev/sdb3     #备份sda1到sdb3中#恢复dd if=/dev/sdb3 of=/dev/sda1     #恢复sdb3到sdb1中
```

> 作者：LeoLan's Blog
> 
> https://reurl.cc/gm5ZkQ

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**