> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ar2cBIlAawczT3O0vWSRxQ)

版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。
----------------------------------------------------

本文链接：https://blog.csdn.net/weixin_46654114/article/details/117574855

一. python 正则表达式介绍
-----------------

1.  正则表达式是一个特殊的字符序列，它能帮助你方便的检查一个字符串是否与某种模式匹配。
    
2.  Python 自 1.5 版本起增加了 re 模块，它提供 Perl 风格的正则表达式模式。
    
3.  re 模块使 Python 语言拥有全部的正则表达式功能。
    
4.  compile 函数根据一个模式字符串和可选的标志参数生成一个正则表达式对象。该对象拥有一系列方法用于正则表达式匹配和替换。
    
5.  re 模块也提供了与这些方法功能完全一致的函数，这些函数使用一个模式字符串做为它们的第一个参数。
    

二. re 模块
--------

### 2.1 match 方法

> re.match 尝试从字符串的起始位置匹配一个规则，匹配成功就返回 match 对象，否则返回`None`。可以使用`group()`获取匹配成功的字符串。

1.  语法：`re.match(pattern, string, flags=0)`
    
2.  参数说明：
    

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuoJtOiatUWSfvGkvm4yzarhdNOJWO5OJlTPswuKqDg0UjsH5cglssfYg/640?wx_fmt=png)

3.  我们可以使用`group(num)` 或 `groups()` 匹配对象函数来获取匹配表达式。
    

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuoqSOGrOpGcQM54fj0nQcqu9sJSH4DXUABibT0TicJwPh5C9uXeLNbw4g/640?wx_fmt=png)

4.  代码演示
    

```
'''
修饰符  描述
re.I  使匹配对大小写不敏感
re.L  做本地化识别（locale-aware）匹配
re.M  多行匹配，影响 ^ 和 $
re.S  使 . 匹配包括换行在内的所有字符
re.U  根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
re.X  该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。
'''
```

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTu6jb37gqHIwhfbIxR5DicCM5QCyJhB8xkkzewFEuKVzCfNhluBib3ynqA/640?wx_fmt=png)

输出：  
![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuYCI8t95icCk3JXncxrgdnRVfKiczqMfKcN5ds5X5ssYOn0jgarjsSHlQ/640?wx_fmt=png)

### 2.2 匹配规则

#### 2.2.1 匹配字符

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTun2dlj1gloGO7qSyaYpQL50sYFltRCpytf8FQ5bPAaPukibR3cqDcA2A/640?wx_fmt=png)

1.  `.`点的使用, 匹配除了换行符之外的任意一个字符字符，还可以`.*`输出后面的字符串
    

```
import re
data='python'
parrtern='..'#匹配规则，这里匹配两个字符
res=re.match(parrtern,data)
print(res.group())#输出：py
'''测试二'''
names='运智在学习python','运气','换人'
pattern='运.'#匹配规则：会匹配运开头的
for item in names:
    chen=re.match(pattern,item)
    if chen:
        print(chen.group())#输出运智，运气
```

输出：  
![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuCPicFicM6oQ1MMeZ7QdePrRMv8FZj1nic08AyAkticMuLcejh7Ak1p6W8A/640?wx_fmt=png)  
2. `[]` 中括号：匹配中括号中的任意一个字符，

```
str1='hello'
res=re.match('[he]',str1)
print(res.group())#输出：h
```

#### 2.2.2 分组匹配

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuPSfRXPphXfibb2bmiafQUwkQ3X1vHRBicEJlZqyibFzOJbpDy9mVdBYCOg/640?wx_fmt=png)

代码按例：

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuxzqicNIB1qZZKazE83iccTWCeudjAImfZuNcLeHlAk1AjTjxnulIeYFg/640?wx_fmt=png)

#### 2.2.3 限定匹配字符规则

> 原理: 就是匹配数量

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuz4ScZluyJ3rEicxdAAKVpH55cuYLnajAW3InIUMa19OZpkBro4nWwYA/640?wx_fmt=png)

1.  `*` 匹配前一个字符出现 0 次或者无限次，即可有可无  
    代码：
    

```
res=re.match('[A-Z]*','Cy')#匹配0次
print(res.group())#C
res=re.match('[A-Z][a-z]*','Che')#也可以写成" [A-Za-z]* "
print(res.group())
# re.match('[a-zA-Z]+[\w]*','na99m_e')
#re.match('\d{4}','1234')#精确匹
```

输出：

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuOxpmvXgwib2mldibtoozMQ5wSHm2rFZPicdBxRmbMGnm20Mhp5Gcyib2gg/640?wx_fmt=png)  
2. 代码按例匹配邮箱

```
regexMail=re.match('[a-zA-Z0-9]{6,11}@qq.com','chenyunzhi@qq.com')
if regexMail:
    print('匹配成功{}'.format(regexMail.group()))
    pass
```

输出：  
![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTukDEiavamNn2NdB65S2xwJTBdAkjbrI2Zvib4JdCJjbFtk9V8NBxB3Usw/640?wx_fmt=png)

#### 2.2.4 转义字符

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTu9yNMjna0Gcy5VkrUr5UENLFibsXynPhyyoWziaNOzQHC6c3h2VWfGWMw/640?wx_fmt=png)

```
import re
# 在正则前加r，表示原生字符串，python字符串不转义 或者直接\\\\a。
print(re.match(r'c:\\a.txt','c:\\a.txt').group())#c:\a.txt

dt='python is chen'
result=re.match('^p.*',dt)#开头是对的就输出
chen=re.match('^p\w{5}',dt)
End=re.match('\w{5,12}@[\w]{1,9}.\w{3}$','chenyunzhi@qq.com')
if result:
    print(result.group())#python is chen
    print(chen.group())#python
    print(End.group())#chenyunzhi@qq.com
```

输出：  
![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuduXy1kpe9iaEV79g2pNeQLFfvgCQaibckMS2RyAk11nlibibT8MGLODxgA/640?wx_fmt=png)

三. re 中的编译函数
------------

### 3.1 compile 方法

1.  `compile` 可以把一个字符串编译成字节码
    
2.  优点：在使用正则表达式进行 match 的操作时，python 会将字符串转为正则表达式对象，
    
3.  而如果使用`compile`只需要一次转换，以后再使用模式对象的话 无需转换
    

```
import re
rs=re.compile('\w.*')
res=rs.match('chenyunzhi')
print(res.group())#输出：chenyunzhi
```

### 3.2 search 方法

1.  `search` ：在全文中匹配一次，匹配到就返回
    
2.  语法：`re.search(pattern, string, flags=0)`
    

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTusbOvkohBwibj8sial6MPd3Y1rW7fwIpSvFRKwLKl4347YTKpmLNrVF0g/640?wx_fmt=png)

3.  代码
    

```
'''
print(re.search('python','人生苦短，我用python').group())
#输出：python
```

### 3.3 finall 方法

1.  `finall（）`：查询字符串中某个正则表达式全部的非重复出现的情况 返回是一个符合正则表达式的结果列表
    
2.  语法：`findall(string[, pos[, endpos]])`
    

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTulgZtVkM76qYd4a1Tg33V2q7icpnl8gGNM28HmsYABG4Mp3YdbZmsFgg/640?wx_fmt=png)

             3. 代码

```
print(re.findall('p','python的开头是p'))#输出：['p', 'p']
```

> 小结：search 找到就返回，finall 全部找到才返回

### 3.4 sub 方法

1.  `sub`：将匹配到的数据进行替换, 实现目标的搜索和查找
    
2.  语法：`sub(pattern, repl, string, count=0, flags=0)`
    

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuoAUFXWwQNnzHZZFXquibjKl1uOcvYay516XajgCQxpHaFcicSdOxkrDA/640?wx_fmt=png)

3.  代码
    

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuBibWhUx7jE6AYDs8bfFicX5E8xbW5NnQk3vNrNOeoTHV0tvsXQwHWIFA/640?wx_fmt=png)

输出：  
![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuD0XzzAJwNnKOEQicpL0595QPHm6cVLiaf13kwPFnE58RjWSXbGkpSqXA/640?wx_fmt=png)

### 3.5 split 方法

1.  split：实现分割字符串, 以列表形式返回
    
2.  语法：`split(pattern, string, maxsplit=0, flags=0)`
    

![](https://mmbiz.qpic.cn/mmbiz_png/ULibHgXIt3jwOc26oic1y0T05Qcuk8DiaTuywb3w63iapBicrADLxu7s0chXJE9GkQOr8nT1hNOOkXM7Ur759qlFdpQ/640?wx_fmt=png)

```
print(re.split(',','chen,yun,zhi'))#输出：['chen', 'yun', 'zhi']
```

四. 贪婪模式与非贪婪模式
-------------

> 默认条件下为贪婪模式

1.  贪婪：在满足条件情况下尽可能匹配到数据
    
2.  非贪婪：满足条件就可以，在`"*","?","+","{m,n}"`后面加上`？`，就能将贪婪变成非贪婪.
    

代码

```
#贪婪模式
pattern=re.compile('a.*b')
result=pattern.search('abcabcd')
print(result.group())#abcab

#非贪婪
pattern=re.compile('a.*?b')
result=pattern.search('abcabcd')
print(result.group())#ab
```

输出：

> abcab  
> ab

> 上面可以看出，贪婪模式要匹配到最后一个 b 才停止，然而非贪婪模式匹配到第一个 b 就停止了

**如果对你有帮助的话，不妨点个赞和在看吧！**