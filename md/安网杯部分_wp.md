> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/P29l9HXFSMUsdU0Ef4t2wQ)

web1
====

webshell 上传

前端绕过。绕了半天才想起来是前端绕过。。burp 改个后缀就好了

```
function checkFile() {
    var file = document.getElementsByName('upload_file')[0].value;
    if (file == null || file == "") {
        alert("请选择要上传的文件!");
        return false;
    }
    //定义允许上传的文件类型
    var allow_ext = ".jpg|.png|.gif";
    //提取上传文件的类型
    var ext_name = file.substring(file.lastIndexOf("."));
    //判断上传文件类型是否允许上传
    if (allow_ext.indexOf(ext_name + "|") == -1) {
        var errMsg = "该文件不允许上传，请上传" + allow_ext + "类型的文件,当前文件类型为：" + ext_name;
        alert(errMsg);
        return false;
    }
}
```

拿到 shell 蚁剑上传 cat /flag

web3
====

http://172.20.2.4:9003/index.php?txt=../../../flag 任意文件读取，秒了

web7
====

知识点：SSTI,SSTI 读配置文件，/proc 目录的作用，flask session 伪造

首先，尝试登录 172.20.2.3:9006, 登录失败，访问了一下 robots.txt, 发现了有报错信息，观察 URL，考虑可能存在 XSS

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IRuwsZHhNeT44gpfjKiauBYOk9nUrnqYicFVh2wick0o21aDMVZoHPmbXg/640?wx_fmt=png)

这里看了一眼中间件分析结果，发现了 flask。。flask 人狂喜（。

直接 4

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5INcpRCGXMr7Wd8Dgy8hn0BJibcnwmbKZic2nRBqibMcZO0mYzNlyTxd4tg/640?wx_fmt=png)

懂得都懂，铁 ssti 了，尝试一步步 rce，检测发现没开 debug 模式，所以只能走常规的 rce 利用了。

当尝试到

```
''.__class__.__mro__[-1].__subclasses__()
```

时发现被 ban 了，单独测试了下小括号，发现是 ban 了小括号。既然 ban 了小括号，那么常规的 ssti rce 基本就走不通了。只能考虑读取一些敏感文件，比如 config，使用 payload 读取 config 文件，发现了 secret_key

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IhQ4VibicLPXPSutAg5licWTpzkGOaibHmlUZmnNBicicGQT8878ibJZcvgB0A/640?wx_fmt=png)

secret_key 的作用是生成 session，具体步骤我忘了，反正是根据 secret_key 可以还原和生成对应的 session。

github 有对应的工具，flask session manager。

接下来看了看源码，

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IRoKl5IOJEbn7MmNdtv5oBmHrPw0icqeEdCcd3n6j5YHKmV5uLY877gg/640?wx_fmt=png)

一个简单的前端验证，burp 抓返回包把 0 改成 1 就行，这样就顺利进入后台了。但是进入后台后提示我不是 admin

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IPPVhjfNVhkYAs69y68ZKldOp0FY8YiayxgNbwJqGMFGLrh43A80I1nQ/640?wx_fmt=png)

好吧，看起来是要伪造 admin 的 session 了。现在 secret_key 有了，用工具先解密当前 session，把用户名改成 admin 后再生成 session。如下图所示

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IVBZzflr7JTfq1cJvhnBGWQ6iapH5rKibRrYucfbpjL28qfCSescCDMHw/640?wx_fmt=png)

那么当前生成的 admin 的 session 就是

eyJ1c2VybmFtZSI6ImFkbWluIn0.YJo7Og.7WfYqubO5M7KZ-8IXXKIp6kMf5o，edit this cookie 换一下（我这 chrome 有 bug，用的 firefox）

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IicJLia68FAyj5W6jAbmd8G76gR40iaCAkhw2vQJ5eGqsn0tZeuKCnvyicg/640?wx_fmt=png)

已经给了 hint，考虑任意文件读取，首先尝试读取 / etc/passwd，成功。

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IvjERGRzLhcq40gopPuBpAqtlvUy3KwA2GlC9bmdK1ibvicfOGYoeIQxw/640?wx_fmt=png)

接下来尝试读 flag。直接 / flag 不行，关键字给过滤了。卡了好几个小时

用了挺多绕过方法 /fla? /f* 等等 但是可能中间有转义之类的，最终传到 Linux 层并不能识别通配符，所以卡了很长时间

最后的思路是之前比赛中读 flag，过滤了很多，师傅告诉我利用 / proc / 目录读文件，这里 / proc 目录是啥作用我就不说了，自己去查一下就好。

/proc/self/cmdline 代表当前的命令行输入内容，我读取了之后是这个

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IcEmQAI4bm5fOFibsUsBUf0J8T35zVmgJhQNVfjibahWfGE5eGRajia30g/640?wx_fmt=png)

好家伙 绝对路径有了，直接读文件

/app/app_a384gh1.py

程序代码如下，基本修复了 ssti->rce，然后看到了 import ffffffff111llllag 文件，那直接读当前 / app 目录下的 ffffffff111llllag.py 就好了。

```
from flask import Flask,request,render_template_string,redirect,render_template,session
import random
import string
import base64
import ffffffff111llllag

app = Flask(import_name=__name__,template_folder='templates',static_folder='static',static_url_path='/static')

app.config['SECRET_KEY'] =''.join(random.sample(string.ascii_letters + string.digits, 8))


@app.before_request
def before_request():
    if '/admin/' in request.path:
        sess_name='guest'
        print(session)
        if 'username' in session:
            sess_name=session['username']
        if sess_name!='admin':
            return 'Your current account is '+sess_name+' not admin'

@app.after_request
def makeheader(response):
    response.headers["X-Powered-By"] = "PHP/7.2.10"
    response.headers["Hint"] = "Wake up Neo, the Matrix has you"
    response.headers['Server']='Apache/2.4.35 (Win64) PHP/7.2.10'
    return response

@app.route('/')
def redirect_2_index():
    if 'username' not in session:
        print('not in session!')
        session['username']='guest'
    return redirect("./index.php", code=302)

@app.route("/err.php")
def err():
    #I patched the SSTI vulnerability.How clever I am!
    errorinfo=request.args.get("errorinfo")
    blacklist=["(",")"]
    for black in blacklist:
        if black in errorinfo:
            return "You're just a dirty hacker,aren't you?"
    return render_template_string("Oh no,there is an Error! Error info:<p> %s" % errorinfo)


@app.route("/index.php")
def index():
    return render_template("index.html")


@app.route("/login.php",methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']
    if "'" in username or "'" in password:
        return "You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '''"
    return '0'

@app.route("/admin/backendmanage.php")
def backendmanage():
    img=request.args.get("img")
    if not img:
        img='1.png'
    
    if "flag" in img:
        return "You're just a dirty hacker,aren't you?"
    content = ''
    with open(img, 'rb') as img_f:
        content = img_f.read()
        content = base64.b64encode(content)
    content=''.join([chr(i) for i in content])
    return '<h1>Current Image:{img}</h1><!-- ?img=1.png --><img  src="data:;base64,{content}">'.format(img=img,content=content)



@app.errorhandler(Exception)
def all_exception_handler(e):
    e=str(e)
    return redirect("/err.php?errorinfo="+e, code=302)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
```

读取 flag 文件后，拿到 flag。

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IjQOoiaFTv4uEktJo4QL63OQmwicVo7icZau5Ktq9oRB6ArMeQgDCK4Oxg/640?wx_fmt=png)

这题有几个坑点，首先是 HTTP 头里面的 PHP HEADER 容易迷惑人，其次是登录那的 sql 注入容易迷惑人，最后是 FLASK-SSTI 的利用方式需要掌握全面：

1. 直接 RCE

2. 开 DEBUG 时，SSTI 读文件 -> 构造 PIN 码 ->RCE

3. 伪造 session 登录

misc1
=====

流量包没看出来啥，直接分离 http 对象发现了 flag.php，压缩包被破坏了，修复下头

```
JPEG (jpg)，                        　　文件头：FFD8FF　　　　　　　　　　　　　　　　　　　　　　　 文件尾：FF D9　　　　　　　　　　　　　　　
PNG (png)，                       　　 文件头：89504E47　　　　　　　　　　　　　　　　　　　　　　文件尾：AE 42 60 82
GIF (gif)，                           　　文件头：47494638　　　　　　　　　　　　　　　　　　　　　　文件尾：00 3B                                                                 ZIP Archive (zip)，                     文件头：504B0304　　　　　　　　　　　　　　　　　　　　　　文件尾：50 4B

TIFF (tif)，                           　  文件头：49492A00　　　　　　　　　　　　　　　　　　　　　　文件尾：
Windows Bitmap (bmp)，      　  文件头：424D　　　　　　　　　　　　　　　　　　　　　　　　 文件尾：
CAD (dwg)，                        　  文件头：41433130　　　　　　　　　　　　　　　　　　　　　　文件尾：
Adobe Photoshop (psd)，          文件头：38425053　　　　　　　　　　　　　　　　　　　　　　文件尾：
Rich Text Format (rtf)，             文件头：7B5C727466　　　　　　　　　　　　　　　　　　　　  文件尾：
XML (xml)，                              文件头：3C3F786D6C　　　　　　　　　　　　　　　　　　　　 文件尾：
HTML (html)，                           文件头：68746D6C3E
Email [thorough only] (eml)，     文件头：44656C69766572792D646174653A
Outlook Express (dbx)，            文件头：CFAD12FEC5FD746F
Outlook (pst)，                         文件头：2142444E
MS Word/Excel (xls.or.doc)，      文件头：D0CF11E0
MS Access (mdb)，                    文件头：5374616E64617264204A
WordPerfect (wpd)，                  文件头：FF575043
Adobe Acrobat (pdf)，               文件头：255044462D312E
Quicken (qdf)，                         文件头：AC9EBD8F
Windows Password (pwl)，         文件头：E3828596

RAR Archive (rar)，                    文件头：52617221
Wave (wav)，                            文件头：57415645
AVI (avi)，                                 文件头：41564920
Real Audio (ram)，                     文件头：2E7261FD
Real Media (rm)，                       文件头：2E524D46
MPEG (mpg)，                           文件头：000001BA
MPEG (mpg)，                           文件头：000001B3
Quicktime (mov)，                     文件头：6D6F6F76
Windows Media (asf)，               文件头：3026B2758E66CF11
MIDI (mid)，                              文件头：4D546864
```

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IX20SqMhzcpa7WbZFmSOR1kuickPdKDAPia8K2D2pEqXDdAI6wKmZvicuQ/640?wx_fmt=png)

提取 rar

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5IAkgBl2mNUH8YicCvQiaoOM7NCcllO6TT2GOaVgkcoIia2eYwooialuOJ9g/640?wx_fmt=png)

十六进制转 ascii

flag{My_Name_is_AoBai}

misc2
=====

zip 文件头修复

得到密文 5a6e4665536e506248206579666b7b39733930733833742d393637312d3433626a2d616f69302d3235663176393138707030377d

十六进制转 ascii

ZnFeSnPbH  
eyfk{9s90s83t-9671-43bj-aoi0-25f1v918pp07}

维吉尼亚解密（captfencoder1.x 版本 维吉尼亚解密有 bug）

flag{9a90f83e-9671-43ac-bbd0-25b1d918ca07}

misc 3
======

压缩包头部修复，修改错了的 1 位

然后需要密码，直接 binwalk 分离出来一个 Linux 可执行文件，到这里卡住了。。然后后面看了看文件头应该是个 png，zhiweilai 加上 png 的为文件头后发现图片宽高有问题，Linux 打不开，用脚本爆破宽高修改即可。

脚本如下

```
import zlib
import struct
import sys
import binascii
filename = sys.argv[1]
with open(filename, 'rb') as f:
    all_b = f.read()
    crc32key = int(all_b[29:33].hex(),16)
    data = bytearray(all_b[12:29])
    n = 4095            #理论上0xffffffff,但考虑到屏幕实际/cpu，0x0fff就差不多了
    for w in range(n):          #高和宽一起爆破
        width = bytearray(struct.pack('>i', w))     #q为8字节，i为4字节，h为2字节
        for h in range(n):
            height = bytearray(struct.pack('>i', h))
            for x in range(4):
                data[x+4] = width[x]
                data[x+8] = height[x]
            crc32result = zlib.crc32(data)
            if crc32result == crc32key:
                print("宽为：",end="")
                width1=binascii.b2a_hex(width)
                width1=width1.decode('utf-8')
                width1=int(width1,16)
                print(width,width1)
                print("高为：",end="")
                height1=binascii.b2a_hex(height)
                height1=height1.decode('utf-8')
                height1=int(height1,16)
                print(height,height1)
                exit(0)
```

在对应的位置修改图片宽高的十六进制值即可。

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV1aibuiadgEbj0D5N0BLFEL5InafhF4BPCEqgniaJoTxxyiafntudkWvhYVibcEzRAchO0xfMTakrCxExw/640?wx_fmt=png)