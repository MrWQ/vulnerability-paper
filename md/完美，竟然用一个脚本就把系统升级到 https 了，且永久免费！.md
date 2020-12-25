> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/4jmz6MQ6jJ2ooA-tBhbAag)

> **来自：今日头条，作者：猿话  
> **
> 
> **链接：https://www.toutiao.com/i6674393673007890957**

现在很多站长都会考虑将自己的站点从 http 升级到 https，不仅是基于安全的考虑，有的也是因为第三方平台的限制，如谷歌浏览器会将 http 站点标记为不安全的站点，微信平台要求接入的微信小程序必须使用 https 等。  

那如何将一个 http 站点升级为 https 站点呢？

### http 与 https 的区别

为了数据传输的安全，https 在 http 的基础上加入了 ssl 协议，ssl 协议依靠证书来验证服务器的身份，并为浏览器和服务器之间的通信加密。要想将 http 升级为 https，只需要给 http 站点增加一个 CA 证书即可。

目前获取 CA 证书有两种途径：

*   购买收费的 CA 证书
    
*   获取免费的证书
    

收费的 CA 证书各大服务提供商都有卖，如阿里云、腾讯云等。

![](https://mmbiz.qpic.cn/mmbiz_jpg/JfTPiahTHJhqb70PXlibAQnB3XVPgu4DM4dtvPlpDYMnkQtHDia394RVadFZpYyTHGxOSBib0zjNHMSIOMZYyATEsw/640?wx_fmt=jpeg)

收费的证书不便宜，从阿里云官方网站看，它的价格可以从几千元到上万元不等。

![](https://mmbiz.qpic.cn/mmbiz_jpg/JfTPiahTHJhqb70PXlibAQnB3XVPgu4DM4dWSkKwktWAtYngcolXZplXMmLOdOXFunYtnCt6iawHB1ia712oCdgAtg/640?wx_fmt=jpeg)

这对于小公司平台，甚至是个人站点来说，是一个不小的开支。

Letsencrypt 是一个免费、自动化和开放的证书颁发机构，其颁发的证书一次有效期为三个月，但是只要能持续更新，基本可以永久使用。

今天推荐的这个脚本 acme.sh，实现了 acme 协议, 可以帮你持续自动从 Letsencrypt 更新 CA 证书。

下载地址如下：

> https://github.com/Neilpang/acme.sh

### 安装 acme.sh

安装 acme.sh 很简单，一个命令即可：

```
curl https://get.acme.sh | sh
```

普通用户和 root 用户都可以安装使用。安装过程进行了以下几步：

1、把 acme.sh 安装到你的 home 目录下:

```
~/.acme.sh/
```

并创建 一个 bash 的 alias，方便你使用：alias acme.sh=~/.acme.sh/acme.sh

2、自动为你创建 cronjob，每天 0:00 点自动检测所有的证书。如果快过期了，需要更新，则会自动更新证书，安装过程不会污染已有的系统任何功能和文件，所有的修改都限制在安装目录中： `~/.acme.sh/`

### 生成证书

acme.sh 实现了 acme 协议支持的所有验证协议， 一般有两种方式验证：http 和 dns 验证。

1、http 方式需要在你的网站根目录下放置一个文件, 来验证你的域名所有权，完成验证，然后就可以生成证书了。

```
acme.sh --issue -d mydomain.com -d www.mydomain.com --webroot /home/wwwroot/mydomain.com/
```

acme.sh 会全自动的生成验证文件, 并放到网站的根目录，然后自动完成验证。最后会聪明的删除验证文件，整个过程没有任何副作用。

如果你用的是 apache 服务器，acme.sh 还可以智能的从 apache 的配置中自动完成验证，你不需要指定网站根目录:

```
acme.sh --issue -d mydomain.com --apache
```

如果你用的是 nginx 服务器，或者反代，acme.sh 还可以智能的从 nginx 的配置中自动完成验证，你不需要指定网站根目录:

```
acme.sh --issue -d mydomain.com --nginx
```

> 注意：无论是 apache 还是 nginx 模式，acme.sh 在完成验证之后，会恢复到之前的状态，都不会私自更改你本身的配置。好处是你不用担心配置被搞坏，但也有一个缺点，你需要自己配置 ssl 的配置，否则，只能成功生成证书，你的网站还是无法访问 https。但是为了安全，你还是自己手动改配置吧。

如果你还没有运行任何 web 服务，80 端口是空闲的, 那么 acme.sh 还能假装自己是一个 webserver, 临时听在 80 端口，完成验证:

```
acme.sh --issue -d mydomain.com --standalone
```

2、dns 方式，在域名上添加一条 txt 解析记录，验证域名所有权。

这种方式的好处是，你不需要任何服务器，不需要任何公网 ip，只需要 dns 的解析记录即可完成验证。不过，坏处是，如果不同时配置 Automatic DNS API，使用这种方式 acme.sh 将无法自动更新证书，每次都需要手动再次重新解析验证域名所有权。

```
acme.sh --issue --dns -d mydomain.com
```

然后，acme.sh 会生成相应的解析记录显示出来，你只需要在你的域名管理面板中添加这条 txt 记录即可。

等待解析完成之后, 重新生成证书:

```
acme.sh --renew -d mydomain.com
```

> 注意：第二次这里用的是 --renew

dns 方式的真正强大之处在于可以使用域名解析商提供的 api 自动添加 txt 记录完成验证。

acme.sh 目前支持 cloudflare, dnspod, cloudxns, godaddy 以及 ovh 等数十种解析商的自动集成。

### copy / 安装 证书

前面证书生成以后，接下来需要把证书 copy 到真正需要用它的地方。

> 注意：默认生成的证书都放在安装目录下：~/.acme.sh/，请不要直接使用此目录下的文件。例如，不要直接让 nginx/apache 的配置文件使用这下面的文件。这里面的文件都是内部使用，而且目录结构可能会变化。

正确的使用方法是使用 --installcert 命令，并指定目标位置，然后证书文件会被 copy 到相应的位置，例如：

```
acme.sh --installcert -d <domain>.com \--key-file /etc/nginx/ssl/<domain>.key \--fullchain-file /etc/nginx/ssl/fullchain.cer \--reloadcmd "service nginx force-reload"
```

一个小提醒，这里用的是 service nginx force-reload，不是 service nginx reload，据测试, reload 并不会重新加载证书，所以用的 force-reload。

Nginx 的配置 ssl_certificate 使用 `/etc/nginx/ssl/fullchain.cer`，而非 `/etc/nginx/ssl/<domain>.cer` ，否则 SSL Labs 的测试会报 Chain issues Incomplete 错误。

--installcert 命令可以携带很多参数，来指定目标文件。并且可以指定 reloadcmd, 当证书更新以后，reloadcmd 会被自动调用, 让服务器生效。

值得注意的是，这里指定的所有参数都会被自动记录下来，并在将来证书自动更新以后，被再次自动调用。

### 更新证书

目前证书在 60 天以后会自动更新，你无需任何操作。今后有可能会缩短这个时间，不过都是自动的，你不用关心。

### 更新 acme.sh

目前由于 acme 协议和 Letsencrypt CA 都在频繁的更新，因此 acme.sh 也经常更新以保持同步。

升级 acme.sh 到最新版 :

```
acme.sh --upgrade
```

如果你不想手动升级, 可以开启自动升级:

```
acme.sh --upgrade --auto-upgrade
```

之后, acme.sh 就会自动保持更新了。

你也可以随时关闭自动更新:

```
acme.sh --upgrade --auto-upgrade 0
```

### 出错怎么办：

如果出错, 请添加 debug log：

```
acme.sh --issue ..... --debug
```

或者：

```
acme.sh --issue ..... --debug 2
```

最后，本文并非完全的使用说明，还有很多高级的功能，更高级的用法请参看其他 wiki 页面。

> https://github.com/Neilpang/acme.sh/wiki

**推荐↓↓↓**

![](https://mmbiz.qpic.cn/mmbiz_jpg/NVvB3l3e9aG5kWic5P8XOwFOhXKjibAt6Yfb1QuqSRZaV5QGHtqqXZFWkia50TDjpWTBqG8Huj3aMlA6cOE9cBVkQ/640?wx_fmt=jpeg)

**Linux 学习**