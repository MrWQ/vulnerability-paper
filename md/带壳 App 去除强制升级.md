\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/6J5cHRfQYJmMNuLRxod7Mg)

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RXu3bXekvbOVFvAicpfFJwIOcQOuakZ6jTmyNoeraLFgI4cibKrDRiaPAljUry4dy4e2zK8lUMyKfkGg/640?wx_fmt=png)

这是一款带壳的 APP，打开之后要求强制升级最新版，否则无法使用，针对此 APP 可以进行脱壳后定位关键代码，然后重打包进行消除强制升级弹窗。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYb95uiaLYmsSSroNJkZRiahyYbPCD6EDibu5PdTTpZicdYHeh4WL8I26ozg/640?wx_fmt=jpeg)

DEXDump 三种使用模式脱壳
----------------

1、使用`objection`加载`frida_dexdump`

```
objection -g com.xxx explore
plugin load /root/.objection/plugins/dexdump/frida\_dexdump
plugin dexdump dump
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneY0y35me67Cb4JkNSrMK2zXLjb8n99C7N3haz3XQ99jiaC1iaskFgt28ng/640?wx_fmt=jpeg)

2、直接运行

```
objection -g com.xxx explore
python3 main.py
```

会自动判断前台运行的 App

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneY5KGh84cAByPibOQRVz5NGZLMeQPQYNib9RbW5icFC5o2J4o3R3Ihbf3fw/640?wx_fmt=jpeg)

3、利用 pip 安装后运行`frida-dexdump`

```
objection -g com.xxx explore
pip3 install frida-dexdump
frida-dexdump
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneY7Qb565Oxsib3VxdK6xS4KK2EhZdRjmGFdFLMaeCyBGyaFPwjAWoAEUA/640?wx_fmt=jpeg)

脱壳成功后，发现生成了 4 个 dex 文件，然后搜索带有`MainActivity`的 dex 文件

```
android hooking list activities
```

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYICKbPOSGXHiaKk0DosQQazI4Ettcl1CrRqKibRrk8gPQ2Yjah2uWDotA/640?wx_fmt=png)

Objection 快速自动化定位
-----------------

正常方式首先以开发者的角度来思考是如何实现窗口弹出功能

`https://www.jianshu.com/p/18e1f518c625`

一 activity 以窗口形式呈现

二 Android: 将 activity 设置为弹出式的并设置为透明的

三 Dialog

1、如果是弹出的 activity, 可以 hook 所有的 activities 进行启动查看

```
android intent launch\_activity xxx.ui.activity.About Activity
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYgibthFLTFJXpahVicfWLXNQCuRsL1H8PZXictp8sZGSibANicrZfa1w4oRQ/640?wx_fmt=jpeg)

启动可疑的 Activity，尝试能不能绕过，然后发现界面到了 app 信息页面，但是返回后还是要求升级的界面，说明此路不通。

```
android hooking list classes
cat .objection/objection.log |grep -i window   
```

查看一个函数能不能 hook，可以将它所有的类打印出来，然后过滤，如果有则可以 hook

```
objection -g com.xxx explore --startup-command "android hooking watch class android.view.Window"
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYjpzicuWAP0ItaubE2qMrfS3TkJlvC3YHLQnOfWW7LMEqPeia59EMWeMA/640?wx_fmt=jpeg)

发现有`android.view.Window`，然后尝试 hook

```
cat .objection/objection.log |grep -i dialog
```

注：

> 也可以不需要`--startup-command`，进去 app 之后再 hook 也来得及

当点击 “立即升级” 发现会立即跳出下图内容，说明与升级框相关`android.view.Window.getWindowManager()`

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYkTSYiag3fNZNWqtZmX9Ul0Cnictnz4fLBkDJFEQI8SlmrPNfmH8dbGibQ/640?wx_fmt=jpeg)

2、尝试下 dialog

```
android hooking watch class android.app.AlertDialog
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYqWT7pe6MvdHhv9fO91wlMkicNz7y1opMmvUhr2uvyJN6xwzt6mU0O3Q/640?wx_fmt=jpeg)

先 hook 看一下`android.app.AlertDialog`

```
objection -g com.xxx explore --startup-command "android hooking watch class android.app.Dialog"
```

发现点升级没有任何反应，故判断此 API 与升级框没关系

然后再尝试 hook 下`android.app.Dialog`看有没有反应

```
android hooking watch class\_method android.app.Dialog.setCancelab le --dump-args --dump-backtrace --dump-return
```

点击新版本框空白地方会出现

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYTUk0Iia5go3Zglko0b18UAnlSjVL6SH2UGTqZ83GVLnzPgFcWvibhoSQ/640?wx_fmt=jpeg)

点击 “立即升级” 出现

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYLBmBKjPm3C7HkETcwpwVddqJZGKffhTtNlXW26RHvO8SmTbDw9cicDg/640?wx_fmt=jpeg)

看到存在`android.app.Dialog.setCancelable` （用返回键无法取消）

然后 hook 该方法

```
plugin load /root/.objection/plugins/Wallbreaker
plugin wallbreaker objectsearch xxx.ui.fragment.dialog.UpdateDialogFragment
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYkR3sOMeZ0ZasmA8Mw2vcFYsiaSNIIyTnEnkJVrecOJKagGm3VGGVXbg/640?wx_fmt=jpeg)

找到对应位置，发现与界面上的版本号、文件升级相关联，从而定位到了代码的关键位置。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYZpO5UEqpHKepO00MLGPZMEDDnuoe1icLFaTvw35UAOSLC5XVATzzbBg/640?wx_fmt=jpeg)

这里是明文，所以很明显就可以判断定位的对错。如果关键字符串做了加密混淆，搜索大法也就无效了，可以使用 wallbreaker 内存可视化漫游，所见即所得。

Wallbreaker 内存可视漫游
------------------

wallbreaker 四种模式：

```
plugin wallbreaker objectdump --fullname 0x276a
```

使用 objection 加载 Wallbreaker 搜索值得怀疑的地方

```
plugin wallbreaker objectdump --fullname 0x2266
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneY8NAouG1ruyiccfxfd5DPxnxjlmuCXgcY0djnKL4oAbgvvfQLvib01xSA/640?wx_fmt=jpeg)

找到之后，打印该对象的属性

```
android hooking watch class xxx.ui.fragment.dialog.UpdateDialogFragment
```

看到`xxx.bean.VersionBean$Version _a; => [0x2266]:`

然后将其打印出来

```
android hooking watch class\_method xxx.ui.fragment.d
ialog.UpdateDialogFragment.b --dump-args --dump-backtrace --dump-return
```

可以看到打印出的内容，与界面所展示的一致，验证了所见即所得原理。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneY8icRCFia4CKTXItmyM67ZAnt2hC1QQTMOCzeriamUjQlvZZHLvz64FUSQ/640?wx_fmt=jpeg)

所见即所得的代码定位思路
------------

定位完之后，我们继 hook`xxx.ui.fragment.dialog.UpdateDialogFragment`

```
apktool -s d xxx.apk
rm classes.dex
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYqeUia7qJnR3NgmjBiaiaebws3zFAgiaIjzDoGD4bNd7omGOCvtl23cJxLA/640?wx_fmt=jpeg)

打印调用栈

`xxx.ui.fragment.dialog.UpdateDialogFragment.b`

```
 apktool b xxx
 keytool  -genkey -alias abc.keystore -keyalg RSA -validity 20000 -keystore abc.keystore   # 生成keytool
 jarsigner -verbose -keystore abc.keystore -signedjar xxxsigned.apk xxx.apk abc.keystore
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYcwc4o8XjAia0ZWXMXTxRHUn7gicmfqcYr6UMHQahSeZ0fJjsqsz5eic1g/640?wx_fmt=jpeg)

根据打印的结果看到

`xxx.ui.fragment.dialog.UpdateDialogFragment.b`是从`xxx.ui.activity.MainActivity.a`该类过来，然后定位该类，发现也是做了个条件判断。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYNficiaDiaibqXQiart4nNBBiaa65pQXOV19kbyZJU6g4ibTIlIw5HVAAJhwUg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYRu0ltBsM07qwdCqd1nxLyAILwr6nkyrty7VjcjHdTTJaIib0KHnNIaw/640?wx_fmt=jpeg)

修改源码重打包去强制升级
------------

接着我们进行修改代码去掉升级框并重打包，首先因为是带壳的 APP，无法直接使用 apktool 进行反编译，不然壳也会被反编译为 smali。所以我们使用 apktool 保留 classes.dex 文件进行解包，然后删除 apk 原有的 classes.dex 文件，并将脱壳后的 classes.dex 放入

```
 apktool d xxxsigned.apk
 tree -NCfhl |grep -i MainActivity
 nano smali/cn/net/tokyo/ccg/ui/activity/MainActivity.smali
```

按照文件大小重命名后放入该文件夹中

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYclfwiasFxkAhWgw7YibeOrMiaEG5r4YrZlRUfict8nT8vnTj03m1DufsfQ/640?wx_fmt=jpeg)

搜索`extends Application`

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYwqMTBhjnyESB7M17ulMGMF7icicAMJrwdHeCwsOZ1muCpD7NN0Br9pMQ/640?wx_fmt=jpeg)

查找`AndroidManifest.xml`内容，将`android:name`的内容替换为`xxx.base.App`将入口点改为脱壳后的入口点

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYlcQ6IP9icpesp4oQTfKKiaCohJWLfhwfiaYOWvcuke4VfPCiaeK2fQGECA/640?wx_fmt=jpeg)

然后回编译、首次使用需先生成 keytool、签名

```
 apktool b xxxsigned/
 jarsigner -verbose -keystore abc.keystore -signedjar xxx2signed.apk xxx2.apk abc.keystore
```

测试可以成功运行后，我们接着反编译，搜索之前定位的类名含`MainActivity`的 smali 文件，编辑查找`UpdateDialogFragment`找到之后修改判断语句

```
 apktool d xxxsigned.apk
 tree -NCfhl |grep -i MainActivity
 nano smali/cn/net/tokyo/ccg/ui/activity/MainActivity.smali
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYf3UDn2o5ciaiaOeejNBc2hiblWvwia3rCb7I3VRsPtrch28PMiaCkU3ygCg/640?wx_fmt=jpeg)

改完之后回编译、签名、运行

```
 apktool b xxxsigned/
 jarsigner -verbose -keystore abc.keystore -signedjar xxx2signed.apk xxx2.apk abc.keystore
```

发现已经没有了强制升级的弹窗。

       ![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RVQe9LTRawH0WBSmic2nCneYMjsWSmyMDLd4B9tQoLiaQzd0ia27xzibsrm1iaiaTH6FBh1lUj62tzyPN1g/640?wx_fmt=jpeg)

E

N

D

  

  

我知道你**在看**哟

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8Ogkicew5KMd52mUWzJfFj3dJZvlic64DFticvDw8cFIBUwubIQAkF5IXQtw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8OgTqzpHQhUIM8BG5s07pmhaElGiclG2tlw7ceJtrgVwZepMEpQpdvic1xg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8Og23eRiaUlSIpFGAOzOUv2fVVWr1ZKozfELyDaWWnpGmfabNTNiblArbdw/640?wx_fmt=gif)