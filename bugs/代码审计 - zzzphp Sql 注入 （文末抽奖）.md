> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/J7eJYqhHRkODaH13k6pYbQ)

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicHrTFkGiadCmbM3bXLoUV5RpVbd0wC2w5bh2RQ6U1w4rB3Qe2u0PvcUw/640?wx_fmt=png)

        zzzphp 免费开源建站系统采用 PHP 免费建站整站系统，所有源码开源完整，支持手机自动同步。

在本地搭建服务器，httpd-vhosts.conf 中设置本地绑定的域名：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicfmooLb1rkib7DYx2KicmicRN5xD9f2EWrUWO2ia7IibcbrnAgHgUqLU5mSQ/640?wx_fmt=png)

其中，zzzphp 为下载的 zzzphpcms 的内容。

然后，本机上的 zzzphp cms 的目录结构为如下：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicTOqM3Tygb2CL7HAxLPSvZjkDwJ2G940acG09DNFfQgx0pJ51YMfpEQ/640?wx_fmt=png)

在按照要求安装好 cms 后，本地 cms 的后台地址访问地址为 admin264.

在登陆后台后，使用 postman 发送如下请求：

必须在 cookie 中设置登陆服务器后返回的 cookie 值，否则执行将失败：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78Rice2JI6OSNFu8K3CkaYk8VH2j3hC6xAZQMKy4De56weEelMozBISqQDQ/640?wx_fmt=png)

该 cookie 值在成功登陆服务器后台后会自动获得。

在 postman 中绑定 cookie 之后，发送请求：

        http://[本地绑定的域名]/[后台地址]/save.php?act=content

        需要注意的是，需要在 act 中传参数 act=content。

使用 post 传的参数中其他都是无关项，但是 c_content 为关键项。

c_content 参数需要先使用单引号和括号闭合语句，然后插入想要执行的 sql 语句。

        这里 c_content 的值为 content’,1,9);createdatabase kaixinjiuhao;//

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78Ricmnt6rIt5skrJOxWTRJm8W3H3JyicKM62dVF2m6ia6yPZvmVobZAtwGGw/640?wx_fmt=png)

开始在 phpstorm 中进行跟踪：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicjTHuHQibkyLKibYRWMA5bVibGmJibxgt1c8M9zeUmOM9M8mIJvVSrI4rKw/640?wx_fmt=png)

可以看见此时 $act=”content”, 继续跟进:

        然后在 phpstorm 中跟踪，跟踪到 save_content() 方法：

其中 getform 函数为获得我们之前通过 post 提交的各种参数，需要注意的是 $c_content 参数

        此时，$c_content 参数的取值貌似被转义，但是不用着急，往下看。

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78Ric2wRicznxz2SIq1W1w0KH0c2aCRMvETLpcmMQqOolHnwiatXsb1uuq82g/640?wx_fmt=png)

        在第 299 行，$c_pagedesc 参数在 post 不传值的情况下，成功获得我们输入的 $_content 的值，并且该值未经过转义：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicoGeGdX4KMCu8H3sf12jepgLemXWxMDs4rW890pnXBVsUPxC96CYtPw/640?wx_fmt=png)

继续跟踪，在第 237 行执行 db_insert 函数，跟进：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicvSIo3HSUlbtgG9rkc8U2gBjPIt5QojiaEqKrAZmJW8ucCYCEMahoHJg/640?wx_fmt=png)

然后在在 db_insert 函数的第 243 行执行 db_exec 函数，继续跟进：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78Ric1FjdEIIPa3nlzoia0wPDZDzoRma4toUNvrxzMqZjhJUA7cRsqSLzRKw/640?wx_fmt=png)

$d->exec($sql) 执行命令

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicgeY6zfuExiahchVbcZHs1HmXnjFyic9N7lI9nVa7iaG1ia2GQOUYXWArmA/640?wx_fmt=png)

最后 postman 返回消息：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78Ricz6lcA8VpWYwLFOc2SkbicrBlm0M4icq0L0jbSAeRo0PSwkGrnH6XiaDqQ/640?wx_fmt=png)

继续往下执行，postman 接收到返回回来的数据：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicQ2lUpxYL4MC2ELqvk0x85YVVibDTibvvd1IdCnmeTlDicSzkfsx8UObuw/640?wx_fmt=png)

可见命令执行成功、可以成功在数据库中找到新创建的 kaixinjiuhao 数据库：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicaN4AiacfbemibHjDrZBnvDvHiadXibHGubCibgtlYia1Vvl40Qs0KumFOnvA/640?wx_fmt=png)

证明 sql 语句执行成功。

        同理，save_content() 函数中的 $c_title2 同样在 post 请求未传值时从 $c_title 处获取值，也存在 sql 注入的风险。

------------------------------------------------------------------------------  

**《企业信息安全建设与运维指南》**

（1）系统全面，讲述企业信息安全建设从 0 到 1 的全部过程。本书聚焦安全体系如何落地，从安全体系规划、方案设计、产品选型、产品开发、部署实施、日常运维等维度详细阐释，内容覆盖办公安全、IDC 安全、产品安全、数据安全、安全管理、安全自动化系统开发和业务安全体系建设，基本满足大多数中小企业的安全建设需求。

（2）结合作者实践经验，可操作性强。笔者有十多年信息安全从业经验，曾任职于国内知名网络安全厂商，为数十家企业和各类单位提供安全咨询和专业服务，熟悉企业的安全需求和痛点，本书将作者的实际工作经验总结为案例，具体实用。

（3）分析具体，深入浅出，易于理解。本书从与日常的生活与工作息息相关的安全问题着手，由浅入深循序渐进，讲解信息安全建设过程中的注意事项，便于读者理解安全架构的原理，进而使安全系统建设更加完备。

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78RicA9boic1Yp2MFsp1cia66a1lL1GnEUtIkATBbGxMpibnYtOjzmWaJj5ANw/640?wx_fmt=png)

**活动详情**

为了感谢一直关注我们 Khan 安全攻防实验室的粉丝们，我们将送出由北京大学出版社赞助的信息安全图书《企业信息安全建设与运维指南》

参与规则：

1. 关注 **Khan 安全攻防实验室**公众号  

2. 转发本文至朋友圈并保存至开奖时间不可设置分组（设置分组无效）点击**赞**、**在看**并加上一句祝福语说不定会增加中奖率哦。  

3. 抽奖结束凭朋友圈截图联系我  

上次抽奖的礼品，粉丝非常满意，感谢大家长久以来的支持！

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0ErVseDu7cngicnGa8j78Ric5GAB1VkdSLTxFQUic8hr2mgltGeKzS5iaVu6ZmTt4DUWDhr2MknVqDKg/640?wx_fmt=png)