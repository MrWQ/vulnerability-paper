> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/stULVINT0SIQuvjyMnW0hw)

![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWjRNXHaZHEfrMNCcDian3sGpzQd8HYquBhOibiaglQNQ9jL6QVibtefLCHNvymxAu0ZGKjnGf4x2hBLFA/640?wx_fmt=png)

点击蓝字 / 关注我们

01

_靶机介绍_

这次的靶机是 Internal, 重点在于爆破，文件上传和一个简单的内网环境渗透。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpxbbXNEEoxVKdSibBPoeH62cmT426mRWJtokpPfibYgNXficIPcR2IIfibQ/640?wx_fmt=png)

02

_信息收集_

首先还是使用 autorecon 进行一个信息收集。这次只开了 22 和 80 端口。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpop2SJQYzBmbVtPoazh4kYr2dLC0zYnnwLIP2mOtDUweU8sRQWgsicYA/640?wx_fmt=png)

可以正常访问的目录也比较少，只有 /blog 和 /phpmyadmin

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpAJSxNwLP6ibLiaPMFicyHRO3j0x0ptBoAYzAicUFrgFldFbrmUtXPyiaCKQ/640?wx_fmt=png)

如果有看到前面的介绍内容的话会建议改改 /etc/hosts。这里查了一下最后要改的域名应该为 Internal.thm

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpWO3hpBhYiclx44JicsDju6E5dNuDP1OqcXSYzYb9LXMKsuj0enkbYqKg/640?wx_fmt=png)

现在访问 IP 或者是 Internal.thm 是可以正常访问的。经典的 wordpress 站点。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpibWf1FNOZPjKcZywFxtUibkicff1w42MvS7gdVPKTuPadyFzoGynWnjFw/640?wx_fmt=png)

03

_爆破 wordpress 后台_

由于网站简单的可怕首先使用 wpscan 获取些基础的信息。可以找到一个用户名 admin

命令:wpscan –-url ip -eu 

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpN5ib33yp76wudssU4NMPl5V4Z2EM1yg33qoziba2UOadorstUkSySIPQ/640?wx_fmt=png)

枚举了插件也发现没啥漏洞只能使用爆破后台方法了指定用户名 admin 以后搭配 kali 自带的字典 rockyou.txt, 可以爆破出一个后台密码出来。密码为 my2boys

命令:woscan –-url ip -u admin -P /usr/share/wordlists/rockyou.txt

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpvw2p4UEo7o1JchTXgefrEiciajKMCD5LqTxegQF3NCPO569ea008pACw/640?wx_fmt=png)

登录后台成功。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpxDt9eBDXz0OdDuRr8tqlTHDppUno9GN8ial7cJQRdF1H3niaJJj6LcsQ/640?wx_fmt=png)

04

_上传反弹 shell_

这里点开左侧的 AppearanceàTheme Editor 发现是个经典的 Twenty Seventeen 模板。这个模板是可以编辑 PHP 代码的地方所以可以上传反弹 shell, 我选择 404 模板。  

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLp6WB8Ea1XiahrUhuhYa61DK7Fn9puPzMeAiaichk2wiaHjLNkwLuqNujtUA/640?wx_fmt=png)

这里把 kali 自带的 php-reverse-shell 复制粘贴进来，稍微修改下自己的 IP 就可。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpKsGNT8IlKQYfZbS8SbgkPYx7x9Yb3y6084zs1iaMnekmzEe0g8pp2Lw/640?wx_fmt=png)

前台访问 ip/wp-content/themes/twentyseventeen/404.php 就可接收 shell 了。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpKITvkn1MGMxuL5E6c5uhKDJjWNAVfDwWpby8zW7l6pmJWaeMstoU3Q/640?wx_fmt=png)

在转了很久以后终于在 /opt 下找到个.txt 文件上面有一个正常用户的账号密码。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpS4U0icKDg8ia5yiaicswoWW5LVbXGzflLNrydwjcmYib2A49RqJ9TbEocsg/640?wx_fmt=png)

用 su 切换成功以后发现 /home/aubreanna 目录下有个 Jenkins.txt，里面提示内网里面还有另外一台机子上有个 Jenkins 服务。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpZPR7gh2iabVSLdyCRZ9FMgMwH8QQvaBwRfuajl6UFDGicP9mib8eNmgaw/640?wx_fmt=png)

05

_内网机器渗透_

既然提示内网还有台机子是运行 Jenkins 服务的可以过去看看。为了能让浏览器可以访问过去，我们首先需要挖一条 SSH 的反向隧道让我们可以通过去。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpOKh4DI8zbqyYRtMuia78Wow4NyEtl8641ibqMGKHg5MDQfnI1ZQ9ibl8A/640?wx_fmt=png)

输入完密码以后在浏览器输入 127.0.0.1 可以访问到 Jenkins 服务了。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLptumJxia0sGrIC5Fn2FD1d8kuPicjpfasUiaAQLWSx7QzwagQWGTdog1QA/640?wx_fmt=png)

这里了尝试了弱密码都失败了。只能又开始爆破了。在 MSF 下搜索 Jenkins 可以找到一个登录爆破的模块。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLp5lE7tP0atFwL6TibyC6R2BgIHEHNm5qIttFC8sODMRcN512u5I90Ghw/640?wx_fmt=png)

填入以下参数后静待爆破

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpyA70o19dnXa9JTUSkayCwcEXFOvSrX5MuWGbXHJSM6VOibRSdWfd7NQ/640?wx_fmt=png)

最好跑出密码为 spongebob

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpUAxVQxUN6xEsmXSL3VKEbiaSBpaoKFP6KXlS5xxLG0aSCDBHtttT8xg/640?wx_fmt=png)

可以登录成功。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpKV4rAO2nq2v80Hqr3KXxCibdzcOLduX0XA3XicX8P3mRAyMHx4lBHwCw/640?wx_fmt=png)

Jenkins 有一个命令执行漏洞是在 Manage Jenkins àScript Console 这里。往下拉就可找到。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpAib5qUrkmCOD03DTJsSqIePe9rCcWfoDgLm33CjHskkeGaNqQuqU6oA/640?wx_fmt=png)

这里就是最终利用点。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLp1ZrSib5qE1oD8V6hOGs0sTQyTgpAhL5qDQahiarL9ticoK9F2PM63JsfQ/640?wx_fmt=png)

填入关键词 whoami 可以执行。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpe2CGiagZ95xOJVWq9pwNmAh3CZJJfTA3iazd8ZLY3MH4TsD02zlAFX1A/640?wx_fmt=png)

这里又转了以下 /opt 又有.txt 文件。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLpKuOXW2hKe6ibutn1N9vnrorcWsibCfFJK4GWLvcO8qWmh0rYWYqjAIGQ/640?wx_fmt=png)

最后发现是 root 的密码信息。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9TEAWtEPJte5mceuGuaetLptqltzcBlQEKtYzXZmyrOof8MEEXicza7UKDNyIsWklluTfCVesxfRGA/640?wx_fmt=png)