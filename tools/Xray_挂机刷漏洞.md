> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/2fYkzInyOMzeucJ0gsWeCA)

公众号

xray 是北京长亭科技其下的一款漏洞扫描工具，工具很好用只是没有批量扫描的功能，今天就带大家一起批量扫描。

**官方网站****:https://xray.cool/**

**直接下载就好**

  
**xray 使用：**

cd E:\ 渗透工具 \ xray_windows_amd64.exe

  
基本爬虫扫描  
./xray_windows_amd64.exe webscan —basic-crawler url —html-output 1.html

代理模式与浏览器联动  
.\xray_windows_amd64.exe webscan —listen 127.0.0.1:8080 —html-output 123.html

批量检查的 1.file 中的目标, 一行一个目标，带端口 没有基本爬虫功能！！！

./xray_windows_amd64.exe webscan —url-file 60.txt —html-output 1.html

python pppXray.py -r target.txt

  
有这些就够用了

我习惯使用 powershell 运行 xray，因为 powershell 颜色分明更好看一些。

第一次使用的时候要初始化一下。

cd 到 xray 的目录 

比如: cd E:\ 渗透工具 \ xray_windows_amd64.exe

  
之后./xray_windows_amd64.exe webscan —basic-crawler {要扫描的 url} —html-output 1.html

初始化完会出现 config.yaml 的配置文件

xray 默认是不扫描 edu.cn 的，想挖教育 src 的需要手动更改

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGPiby2gswDHPqYCuORXD0H4BibqAdWmQYIEiakvMYfO8f3dgyJxcPPicMeNdsfBjzD2icBlWPdy7HrDUA/640?wx_fmt=jpeg)  
  

要更改的地方长这样，在 config.yaml 里，把 edu.cn 删掉就好了，应该一共有两处。

当然以上都不是重点

重点: github 上有这样一款工具可以让 xray 批量进行扫描

**下载链接：**

**https://github.com/Cl0udG0d/pppXray**

  
运行需要 python3 的环境

  
pppXray 和 xray 要放在相同的文件夹下

  
首先要 pip 安装 click

  
cmd 运行：pip install click

  
![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGPiby2gswDHPqYCuORXD0H4DURlCNO1TbLwkpicWONAAbdAO2vEjQortx8o7hzCHbCgTehZ1hZI2vA/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGPiby2gswDHPqYCuORXD0H4kKooU21Nic1zBzs67SXiaesL0Zic19Q0ibg9gV01S0f3RS9IuicwOsesZZA/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGPiby2gswDHPqYCuORXD0H4yD77FmrwcCh9PJ2th6hbxiaK9IibibmWPLfUmlCM6GtJpsyh99nTVsjIg/640?wx_fmt=png)  

还有几个位置是需要手动更改的，在 pppXray.py 中

  
![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGPiby2gswDHPqYCuORXD0H4ndsPpaVtubITfZrqQrWibP7iaWFNxsNnTNJIOtpdEbUrHNeicaXrqhGqA/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGPiby2gswDHPqYCuORXD0H4Jz8czsZJpS08OAJicxdQRbBfrGGlGVa14Zkj9eXl3orNFFNt8iayxfFA/640?wx_fmt=png)  

这个位置要改成你电脑里 xray 的名字

使用工具时输入

python pppXray.py -r target.txt

target.txt 里可以直接放 url，没有 http:// 的也可以工具会自动加上。  
  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGPiby2gswDHPqYCuORXD0H4iatxG3QMJRProVvGngpajvmB1aTXjT01S6laibBAZ0Sf3mn8gN77jMFw/640?wx_fmt=png)  

运行时大概就是这样的

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGPiby2gswDHPqYCuORXD0H42woX6RDcpF78D9icjibHGWGHMev1N920lHbwy4FEh1NPgfPQzFYSCkxg/640?wx_fmt=png)  

—basic-crawler 是基本爬虫扫描会使用 xray 自带的爬虫爬取 url 进行漏洞扫描

—html-output

是以 html 形式输出漏洞报告， E:\ 渗透工具

\xray_windows_amd64.exe\save\a41c7ff9f598c880a1fa99ca9fbdc65a.html 是输出文件路径和文件名，这一步是自动的。

之后我魔改了一下原版的 pppXray

```
import hashlib
import re
import time
import os
import click
import config
import winsound
@click.command()
@click.option('-r', '--readfile',default='target.txt',help='xray批量扫描读取文件名,按行读取',type=str)
@click.option('--plugins',help='自定义xray插件 plugins')
def init(readfile,plugins):
    """pppXray : xray 批量扫描\n
       https://github.com/Cl0udG0d/pppXray
    """
    try:
        if not os.path.exists(config.saveDir):
            os.makedirs(config.saveDir)
        config.targetFileName=readfile
        if plugins:
            config.plugins=plugins
        click.echo("读取文件 {} ".format(readfile))
    except Exception as e:
        print(e)
        pass
def xrayScan(targeturl,outputfile):
    scanCommand = "xray_windows_amd64.exe  webscan {} --basic-crawler {} --html-output {}\\{}.html".format('--plugins {}'.format(config.plugins) if config.plugins else '',targeturl, config.saveDir,
                                                                                         outputfilename)
    print(scanCommand)
    os.system(scanCommand)
    return
def pppGet():
    f = open(config.targetFileName)
    lines = f.readlines()
    pattern = re.compile(r'^http')
    for line in lines:
        try:
            if not pattern.match(line.strip()):
                targeturl="https://"+line.strip()
            else:
                targeturl=line.strip()
            print(targeturl.strip())
            outputfile))
            xrayScan(targeturl.strip(), outputfilename.hexdigest())
            # print(type(line))
        except Exception as e:
            print(e)
            pass
    f.close()
    print("Xray Scan End~")
    winsound.Beep(600,5000)
    return
def main():
    try:
        print(config.logo())
        init.main(standalone_mode=False)
        pppGet()
    except Exception as e:
        print(e)
        pass
    return
if __name__ == '__main__':
    main()
```

导入包

import winsound

扫描结束时

winsound.Beep(600,5000)

系统 beep 响 5 秒钟

  
扫描漏洞的时候人可以一边休息，扫完有提示音的时候再回来看就好了。

漏洞报告会在 pppxray 下的一个 save 文件夹里

  
之后漏洞报告是这样的

  
![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGPiby2gswDHPqYCuORXD0H4Iejs3L5VN0pibKRSoNcKbFtAj64h7Rls9l7w5FAnBypAVN0QXpvuJIg/640?wx_fmt=png)  
图中表示漏洞为 XSS 触发参数为 colurnmid

学习更多黑客技能！体验靶场实战练习

![图片](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSFl47EYg6ls051qhdSjLlw0BxJG577ibQVuFIDnM6s3IfO3icwAh4aA9y93tNZ3yPick93sjUs9n7kjg/640?wx_fmt=png)

（黑客视频资料及工具）  

![图片](https://mmbiz.qpic.cn/mmbiz_gif/CBJYPapLzSEDYDXMUyXOORnntKZKuIu5iaaqlBxRrM5G7GsnS5fY4V7PwsMWuGTaMIlgXxyYzTDWTxIUwndF8vw/640?wx_fmt=gif)

往期推荐

  

[

干货 | 23 个非常实用的 Shell 拿来就用脚本实例



](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247514925&idx=1&sn=2985d6240fcd8ad7bba1c61337b8e2f9&chksm=ebeaf200dc9d7b16c0608da1766b11c4983245eed702dfcbd967179e3f011f2bcbd89fdc8483&scene=21#wechat_redirect)

[

用 Python 写了一个窃取摄像头照片的软件



](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247514824&idx=1&sn=8ad8e29124a421ccefab003a729e9b34&chksm=ebeaf3e5dc9d7af342cbec14220f3d6b2d1c96e582d580568844691103a35566ee92b424121c&scene=21#wechat_redirect)

[

实战 | 深入某诈骗团队



](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247513227&idx=1&sn=93d40498015cc99f76c055a438f302f6&chksm=ebeafda6dc9d74b0f7a4358e73f972db13647068dca87b5a0b5866b1bae246d8186dfcbe8631&scene=21#wechat_redirect)

[

被勒索 15 亿，与黑客之间的佛系斗智斗勇，笑喷了……



](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247509195&idx=1&sn=a1cc6484367475ed2558a78e3389474c&chksm=ebeaede6dc9d64f00ac324d7881ec400d98abdc10ed701b01b9497bc3e3abc2529fe8696453a&scene=21#wechat_redirect)

[

Fofa+Xray 联合实现批量挖洞



](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247507465&idx=1&sn=33bbfae575988803225594e26f5391e8&chksm=ebea9724dc9d1e3263f7403fbb34e14424311d0e9145b7d48d0815fef5ce54f6c81a164a0cce&scene=21#wechat_redirect)

[

【教程】局域网内截断别人的网络



](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247506774&idx=1&sn=aec7a3668dfe733bf9b59de04031f115&chksm=ebea927bdc9d1b6d371807bd838a4bda48bbb6094564fe8d5db9d5c4a5b85a98c596f8cb7b84&scene=21#wechat_redirect)

[

真香实战：从弱口令到批量拿下服务器



](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247502098&idx=1&sn=f2a2312cb691d04f0c5a576fb95072ba&chksm=ebea803fdc9d092975c6bb6c7cf7e03af904a278a374c7ee143e9acb82e2c34556f595259006&scene=21#wechat_redirect)

[get 新技能 ! 用手机也能秒变黑客](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247492144&idx=1&sn=496cbb580cd168e6eb1110dbc13b4730&chksm=ebeaab1ddc9d220b89caf041855d799671dfc21b7f490c0f1b40b4f6b796cf1c4bb47e7b11b9&scene=21#wechat_redirect)