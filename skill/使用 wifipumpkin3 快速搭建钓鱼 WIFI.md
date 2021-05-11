> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/xQ2QV-g3SfQKmOVOt_07lA)

**文章源自【字节脉搏社区】- 字节脉搏实验室**

**作者 - Linuz**

**扫描下方二维码进入社区：**

**![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK3Fc7MgHHCICGGSg2l58vxaP5QwOCBcU48xz5g8pgSjGds3Oax0BfzyLkzE9Z6J4WARvaN6ic0GRQ/640?wx_fmt=png)**

正式使用之前，推荐查看 wifipumpkin3 官方文档：

> https://wifipumpkin3.github.io/

0x01 安装
-------

wifipumpkin3 官方文档中提到，仅支持 Linux 安装，以及 Mac OS X 的 docker 安装。

本次在 Kali Linux 下进行安装。

wifipumpkin3 需要依赖于 Python3.7 或者更高的版本，由于 Kali Linux 自带 Python3.8，所以安装 Python 的过程在此不再叙述。

### 安装系统软件包、依赖

```
sudo apt install libssl-dev libffi-dev build-essential
```

### 下载 wifipumpkin3

```
git clone https://github.com/P0cL4bs/wifipumpkin3.git
cd wifipumpkin3
```

### 安装 hostapd、pyqt5

```
sudo apt-get install hostapd
sudo apt install python3-pyqt5
```

### 检验 pyqt5 是否安装完成

```
python3 -c "from PyQt5.QtCore import QSettings; print('done')"
```

如果打印 done 则安装完成，否则失败。

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6G0nficic1dibuEdSwPDjae2SXxDyBJ9OsCxKZuVpVwzPUtjgpo3v73L8w/640?wx_fmt=png)

### 编译安装 wifipumpkin3

确保当前在 wifipumpkin3 目录下，然后执行

```
sudo python3 setup.py install
```

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6R208YHnQhbb4sQKwDBJa6RXdIcOLQfYa55LvF436MlKlh7JTjhXWrA/640?wx_fmt=png)








------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

0x02 简单使用  

首先需要将网卡挂载到 Kali Linux 上。

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD61o4U52ia3bqgib9zCiaMicWk0rLXNBZib0mOvmSGtboiblCaEicBQicOdfNKVg/640?wx_fmt=png)

然后启动 wifipumpkin3

```
sudo wifipumpkin3
```

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6UucB6NsOBPk4GWPKRLmY1bKzdXXEAvTKuKsibB9hjfs7Vpqn0nsNSmw/640?wx_fmt=png)

<span open=""sans",="""clear="" "helvetica="" neue",="" helvetica,=""arial,="" sans-serif;"="">wifipumpkin3 有点类似 msf，交互界面简单配置即可搭建完成

```
# 设置网络接口
set interface wlan0

# 设置钓鱼wifi的ssid
set ssid demo

# 设置代理插件
set proxy noproxy

# 忽略pydns_server的所有日志
ignore pydns_server

# 启动
start
```

启动后会一直处于监听状态

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD63nz7ic4kia3Ib10EsQrA531tEq8spia2FEGovQkwC4Af8G5tIqxm8oibYw/640?wx_fmt=png)

手机搜索发现开放 wifi，进行连接之后，随便找个登录页面登录

![](https://mmbiz.qpic.cn/mmbiz_jpg/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6qev9icAtqxx7n2WibzpjQgBia0ft9cfLq0uzpP0OiccREQ00mV6MdzicAHA/640?wx_fmt=jpeg)

效果：连接之后手机可以正常访问网络，不过期间所有流量都会被监听，进行登录操作时，wifipumpkin3 会自动抓取到账号密码，并且会显示到屏幕上。

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD68edOdaz1l3wXqpBBkKFrZV09dAhWia4IDeNkzyRwiabXkz83SqKwp6Cg/640?wx_fmt=png)

0x03 自定义钓鱼页面
------------

假设钓鱼场景发生在 XX 大学里，一般的校园网接入后会强制跳转到认证界面，输入账号密码认证成功后才可以上网。

利用 wifipumpkin3 的插件功能，可以轻松实现强制跳转到自定义的认证界面。

### 准备素材

这一步需要将认证界面的 html、css、js、等静态文件都下载到本地，并且修改至完全一样。

wifipumpkin3 有几个默认的钓鱼页面素材，位置在

```
wifipumpkin3/config/templates
```

目录结构如下

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6onDD88Huq583p8bbvxBxhFfBAOIn4yLy1dclBn13czbvf8puibnaFgA/640?wx_fmt=png)

preview.png 为预览图片，static 目录放置了页面的静态文件，templates 目录放置了登录页面以及登录成功跳转后的页面。

将自定义的页面静态资源路径改为以 static 为当前路径，例如：`static/css/login.css`

然后将制作好的素材复制到`wifipumpkin3/config/templates`目录下

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6c5zibzTEH73dxoibefEORfrkh2LZ5jBFK2jibibpq4ByJvSkuI9J59qWWg/640?wx_fmt=png)

`wifipumpkin3/wifipumpkin3/plugins/captiveflask`目录中存放了每个钓鱼页面的 py 文件，新增自定义的钓鱼页面也需要新建一个对应文件名的 py 文件，这里直接复制一个，修改一下里面的名字即可

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6ZCX8lNbWMGeStBSXMdOo4TgTquibeX48ORe5TiaFWj8S8OtqBWrdAicZQ/640?wx_fmt=png)

在`wifipumpkin3/config/app/captive-portal.ini`文件中新增一行

```
School=false
```

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6qOnPzuQVlwVuyUG71Q1CWTQTMdM9Kcv3q0s1A43W5KnIgP9JwGQUicA/640?wx_fmt=png)

最后一步，修改`wifipumpkin3/bin/captiveflask`文件，使 request 参数对应钓鱼页面的 input 参数。

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6WibicJpL7iaGv1GkvBcgqYwByfKKj07BRe7QonX5hJ4iaJuP2ecP5UuA0Q/640?wx_fmt=png)

全部准备好，需要重新编译安装，后续每次修改页面都需要重新编译安装。

```
sudo python3 setup.py install
```

### 页面测试

```
set interface wlan0
set ssid School
set proxy captiveflask
set captiveflask.School true
proxies
start
```

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD63IKlI29koJefeKl21xEXdcSiawpCvoVecic4Hiamia0EE4o3UibmiaftCXKQ/640?wx_fmt=png)

启动后将会发布一个 web 页面，注意本机 80 端口不能冲突

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6YJGnFROacyPMIk0vwWJdUrKfz3jLsQzPsKO7lvd7CjX9hF8mjLFuWA/640?wx_fmt=png)

手机连接 WIFI 后会提示需要认证，强制跳转至指定页面

![](https://mmbiz.qpic.cn/mmbiz_jpg/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6OlyUJo8LtJjIgNG9y00sR7rMot2zkwd3n5ghqFj6hgQanPq43RxjGA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6HOZiayTJkbVFFX9u7OXWjSHcktwJAY5leO46GoBzsyNg8GY7opxWcjA/640?wx_fmt=jpeg)

输入账号密码后，屏幕会显示

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnLFMiaK0PiczKIUaiabtc0YAD6bSsgt5ddibxbJg1ITSHA8OyBfibrgfRmQRzt4xyn77YaYj4UEsS7vCQA/640?wx_fmt=png)

wifipumpkin3 还有很多好玩的姿势，就靠大家亲自挖掘啦。

**通知！**

**公众号招募文章投稿小伙伴啦！只要你有技术有想法要分享给更多的朋友，就可以参与到我们的投稿计划当中哦~ 感兴趣的朋友公众号首页菜单栏点击【商务合作 - 我要投稿】即可。期待大家的参与~**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/ia3Is12pQKnKRau1qLYtgUZw8e6ENhD9UWdh6lUJoISP3XJ6tiaibXMsibwDn9tac07e0g9X5Q6xEuNUcSqmZtNOYQ/640?wx_fmt=jpeg)**

**记得扫码**

**关注我们**