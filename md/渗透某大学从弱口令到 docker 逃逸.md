> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/P2m-JbUnsAEIIdfJ7_-S2A)

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2a0WOjbISaibFBsKibQoER7zXtDLficB4pZlv8w7K013AGMtHc4Ij4SKEQ/640?wx_fmt=png)

前两天一直在敲代码写工具，主要目的是想方便自己在渗透测试中前期的信息收集。在测试脚本进行批量扫描的时候， 看见一个熟悉的 edu 域名，欸? 这不是之前交过 edusrc 平台的某个站点吗， 又给我扫到啥敏感信息了?  

### 0x01 前期信息收集

打开网站瞎转悠一波，不出意外的话是个静态站点

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2o7QsB6CnuaWIvmkSAo9ypH55ibBAh9owviaicxdBpWGc9hj4iac6tPQIibQ/640?wx_fmt=png)

往下翻这几个点击全部跳转到了一个登陆口，前端大概就这样：

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU282sKCvVj5JIYA3LtpWwQsjVGFXlgTBkI7zCfULUib6K29Vq3hGqicS6g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2Xk4GaDPXICj0DpWVD6a1mAby6RuhstvXJyLDBENJXc90LRDnzZITtQ/640?wx_fmt=png)

Web 整体架构

```
操作系统: Ubuntu
Web 服务器: Nginx1。18。0 + Java
端口开放信息: 80 443
```

先进行一波目录扫描

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU25m3ib1vhjGmD5VAu2HiaU4sNIYZ3GbSgqVM0lPgJibGMgo0rILJibh7EoA/640?wx_fmt=png)

### 0x02 挨个测试

可以看到，扫描到了一个 "jira" 目录，看这眼熟的目录盲猜是 Jupyter NoteBook 组件

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2BGXzhy0n7zMckyBerqF55oB8wLfRtx8hlnR6tASibLehibZ5JK7DfFkQ/640?wx_fmt=png)

访问果不其然， Jupyter NoteBook 组件的登陆点

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2ZaJR7EQicCv1MpEvdA8y3tu2JEVCmgtk3UyuwkLg36q1Nib8lLU8JG3Q/640?wx_fmt=png)

然后我们挨个其他 3 个有效目录， 都是登录口

> /gitlab

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2YCCicsYicbBrqTfZXShW4vU0lIrh2gvNDszfWcMyBLrvCUQHpd1sLbxQ/640?wx_fmt=png)

> /owncloud

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2YLQTw2ebQqbPUBwEcG3bGJicsGnuTSnDic5bcibcibvvFVnoy8YcDDaZ9A/640?wx_fmt=png)

> /confluence

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU23icI65VhpfWH1YszzvRsNKNvTkKGh6qlwDgW9q9ZmKnGg0H3fPqia7ww/640?wx_fmt=png)

我晕~ 要让我爆破吗? 这三个登陆点先放着

由于是 Jupyter Notebook 组件， 印象中应该是有相关漏洞的。当机立断去 Google 一波历史漏洞，**有 2 处信息泄露 + 未授权访问 RCE。**

#### 信息泄露

利用信息泄露可以用来爆破用户， Exp1:

> /jira/secure/ViewUserHover。jspa?username=admin

Exp2:

> /jira/rest/api/latest/groupuserpicker?query=admin&maxResults=50&showAvatar=true

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2QKmHIyHUmAiaPl5p2ajGVZYQ0msmpsypd2ruh8eBjKgaQCNapjZOUrQ/640?wx_fmt=png)存在用户的话是会返回用户信息的，然后爆破~

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2YkOxT7fvMIncaV07wDv9jHNbjbSfpeG7ObL8VaiaFjickbfUVJfibPX4Q/640?wx_fmt=png)

欸我这一看， 爆破出一个 "Kevin" 用户， 掏出我们陈年密码本再继续爆破一波密码:

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2lOLnqJPDeibeLAfIIhRq0DiclxzgWUXueaXzCbq2nZysXCdgzmxtrFVA/640?wx_fmt=png)

上个厕所回来一看，啥都没出来。爆破这事儿就此告一段落

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2TV1CMs44lfokZ7JoqPDCf9jZib2X92GVkiaB3eIEQJnsp0v6mR2IlDNQ/640?wx_fmt=png)

#### 未授权访问

看了网上几篇相关此组件未授权访问漏洞，都是直接访问能够在控制台运行 "Terminal" 直接执行命令。但是这边我拿到的域名访问是大学的某系统， 猜测修复了未授权漏洞，加了验证。

### 0x03 突破点

想起之前官网主页跳转的登陆口，貌似好像就是修复了未授权漏洞加的验证点，需要输入密码登陆。

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU25icu098mJOsiardEGQVK8kZicWXC08MWiaf70AkwXseD0xHicSxC3icMPMtg/640?wx_fmt=png)

来到之前登陆口，随手输入一个 "123456"，点击登陆

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2ImScE67vKsBXrMbRnBnkKOmthFkib2ZGM0s3hyB8NrG9E1x86wjcpmw/640?wx_fmt=png)

竟然。。。给我进来了 (这开发真的是，这里弄个平民口令)

那么进来了就好办了，按照历史漏洞

> New->Terminal

打开了一个终端， 直接可以执行命令

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2b873Yycs3ZA8icqx5pN6DbqVT841UccnUEEic0rKUXXEsHqpCPeehmqA/640?wx_fmt=png)

习惯性的去根目录，看看有啥文件

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2lu3JvTDJGb0aVfuEjfauiaTJYfoxE9vJQ0HMcf2KrszYhbqT6xj6cxA/640?wx_fmt=png)

看到 `。dockerenv` 文件，不是吧不是吧，在裸奔的我有点慌，难道踩罐了?

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2V41GXwRxDdMBoW7UOy57f40mMibLZiaxjkLfqWFX3ATwQvTziaKMtbveg/640?wx_fmt=png)

为了验证我的想法，查询系统进程的 cgroup 信息

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2Kz5n4QIEkibLELbnCebfq7w53tZ7gM6qyleV421wpOMaeOJ0ZrpwK3w/640?wx_fmt=png)

是 Docker 没错了，猜想为蜜罐的可能性不大，部署了某大学的一个办公系统。

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2NcgL8N792Bs8ah5sicT7PdR7hTEzkC2zV4y5mibDIxuGicWBEOsTF9icRw/640?wx_fmt=png)

### 0x04 Docker 逃逸

由于在 Docker 容器中，想到 **"Docker 逃逸"** 这个漏洞，也不知道能不能逃逸出来，于是想尝试一下。

之前从没实战碰到过 Docker，也没有复现过 Docker 逃逸这个洞，查阅了大量文章。这个点就折腾的比较久。参考文章:

> https://www。freebuf。com/articles/web/258398。html

CVE-2019-5376 这个漏洞是需要重新进入 Docker 才能触反弹 shell。而我们上面正好是可以直接进入 Docker 终端，是尝试利用，Poc:

> https://github。com/Frichetten/CVE-2019-5736-PoC

修改 main。go 文件，此处更改为弹 shell 命令

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2dbHUIw2ZoFLyplbSXOFopcrBdBhr8ll8cmCBxgrVL3wunaNV8YNMDw/640?wx_fmt=png)

完了之后发现自己没有 Go 语言环境

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2jmBWzz5N4ic1gOsvia0Knbw89N8EkgzMgE5TiaNuVc9khPugNrgq7MyhA/640?wx_fmt=png)

听说 Mac 自带 Go 语言环境，认识个表哥正好用的 Mac，于是找他帮忙编译

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2VXibKRWZ6VtTR2ufvpPMl07IKDFhjqtaM1ibXbp8qGMzSA6qODQVJLzg/640?wx_fmt=png)

原来这就是 "尊贵的 Mac 用户"~~

自己又倒腾了一套 Go 语言环境。然后编译我们的 Poc

到 go 文件同目录下，使用命令:

> CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build main。go

(注: GOOS 参数为生成的可执行文件运行环境，由于我们标靶站点是 Linux，故此处使用 Linux)

到之前弱口令进入的 Jupyter NoteBook 控制台上传 Exp 到默认目录

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2hX3bMpRGiap9JFIaxgVX1MSDWLhI1bSLWY1Hy0wbibPUFhdlib3G4UicnQ/640?wx_fmt=png)

我们这边 VPS 监听 1314 端口

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2FvKvENiatUOFkjFEtcSC1IMyr4hH7Uhhla8T2fgBPWAgRg28R2ZUJUQ/640?wx_fmt=png)

靶机运行我们的 Exp

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU29EeKibA0o2h3OGmjib9HUChvto7JA1LAQkeS17dqQzQGd6gSvOsgDhCQ/640?wx_fmt=png)

然后我们回到 Jupyter 控制台，重新进入终端界面

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2gzEsnyHJOs4TVVa35IYUsORtrqrR7xibf3lVUf4cjTzSkmtM9gR0enw/640?wx_fmt=png)

VPS 等待一会儿没弹回来 shell，后面才发现是我自己 VPS 端口策略问题，换个连通的端口，重复步骤，Exp 生效，成功弹回来主机 shell

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAffRXcbAictNsCljMmBql8iaU2INYbXxAuc3AkGsBKBurWm80orFz7PL9C7WcicbJPbAh1gqaYVJDIwtA/640?wx_fmt=png)

### 0x05 结语

貌似是部署在阿里云的服务器，未授权原因就不再继续深入了。其实一开始的想法是弄个 Webshell 的，但是对这种架构不熟悉，知识欠缺。没找到 Web 目录~~(果然还是我太菜了哈哈)

(相关漏洞已提交至 edusrc)

![](https://mmbiz.qpic.cn/mmbiz_png/sGfPWsuKAfcPwicnhSf4ocAPbZiaytiaRhLzficHI9ENRXNT0ib8ibGbiccypgwlb94nqeD4ebC4VjU960nmS6Itoz6Yw/640?wx_fmt=png)