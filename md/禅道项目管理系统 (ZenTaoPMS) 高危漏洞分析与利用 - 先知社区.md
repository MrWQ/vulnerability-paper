> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/8692)

一、组件介绍
------

### 1.1 基本信息

ZenTaoPMS（ZenTao Project Management System），中文名为禅道项目管理软件。ZenTaoPMS 是易软天创公司为了解决众多企业在管理过程中出现的混乱，无序的现象，开发出来的一套项目管理软件。

禅道项目管理软件的主要管理思想基于国际流行的敏捷项目管理方式——Scrum。scrum 是一种注重实效的敏捷项目管理方式，但众所周知，它只规定了核心的管理框架，但具体的细节还需要团队自行扩充。禅道在遵循其管理方式基础上，又融入了国内研发现状的很多需求，比如 bug 管理，测试用例管理，发布管理，文档管理等。因此禅道不仅仅是一款 scrum 敏捷项目管理工具，更是一款完备的项目管理软件。基于 scrum，又不局限于 scrum。

禅道还首次创造性的将产品、项目、测试这三者的概念明确分开，产品人员、开发团队、测试人员，这三者分立，互相配合，又互相制约，通过需求、任务、bug 来进行交相互动，最终通过项目拿到合格的产品。

### 1.2 版本介绍

禅道项目管理软件基于自主研发的 PHP 开发框架 --- 禅道 PHP 框架开发而成，企业或者第三方的开发者可以通过这套框架，灵活的对禅道进行功能的修改或者扩展。经过逐年演化，禅道项目管理软件发展成为四大系列、功能完善的项目管理软件。禅道项目管理软件发展至今其核心开发系列共有以下三个，即禅道企业版、禅道专业版、禅道集团版、禅道开源版。其中禅道开源版是基础版本；而专业版、企业版是根据禅道开源版进行二次开发而成，其间仅存在功能性上的不同，所以专业版、企业版是兼容同级开源版的；而集团版仅为部署架构上的不同，核心还是企业版，具体如下：

（1）禅道开源版（2009-2020）是禅道项目管理软件的基础版本，属于禅道项目的开发框架，其中仅开发了项目管理的基本模块。

（2）禅道专业版（2012-2020）是在禅道开源版的基础上增加增强功能。专业版推出的初衷是为 IT 企业或部门提供更完善的服务，专业版增强功能更加适合企业的内部流程化管理。同时专业版的增强功能都以收费插件的方式发布在禅道官网里，为用户提供单独下载使用的服务。

（3）禅道企业版（2017-2020），在禅道专业版功能的基础上，增加了运维管理、OA 办公管理、反馈管理，以及文档的版本管理及在线预览等功能，可以为企业项目管理流程提供更全面的支撑。

（4）禅道集团版（2019-2020）主要包含主站平台和子站点两部分。集团版用户可以通过主站平台给旗下的 部门、 子公司或者第三方开发团队分别开通一个独立的子站点进行项目管理。集团版的子站点由禅道项目管理软件企业版提供项目管理服务， 每个子站点的数据都是独立且互不影响的。

版本细分如下图所示：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162133-8926c6d0-4365-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162133-8926c6d0-4365-1.png)

### 1.3 使用量及使用分布

根据全网数据统计，使用 ZenTaoPMS 的网站多达 4 万余个，其中大部分集中在国内，约占使用量的 75% 以上。其中，广东、浙江、北京、上海四省市使用量最高，由此可见，ZenTaoPMS 在国内被广泛应用。通过网络空间搜索引擎的数据统计和柱状图表，如下图所示。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162154-955aab60-4365-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162154-955aab60-4365-1.png)  
（数据来源：FOFA）

二、高危漏洞介绍
--------

通过对 ZenTaoPMS 漏洞的收集和整理，过滤出其中的高危漏洞，可以得出如下列表。

<table><thead><tr><th>漏洞名称</th><th>漏洞 ID</th><th>影响版本</th><th>漏洞披露日期</th></tr></thead><tbody><tr><td>禅道 8.2-9.2.1 SQL 注入导致前台 Getshell</td><td>无</td><td>禅道开源版 8.2-9.2.1</td><td>2018</td></tr><tr><td>禅道 后台代码注入漏洞</td><td>无</td><td>禅道开源版 &lt;= 11.6</td><td>2019</td></tr><tr><td>禅道 后台任意文件删除漏洞</td><td>无</td><td>禅道开源版 &lt;= 11.6</td><td>2019</td></tr><tr><td>禅道 后台任意文件读取漏洞</td><td>无</td><td>禅道开源版 &lt;= 11.6</td><td>2019</td></tr><tr><td>禅道 后台文件包含漏洞</td><td>无</td><td>禅道开源版 &lt;= 11.6</td><td>2019</td></tr><tr><td>禅道 后台 SQL 注入漏洞</td><td>无</td><td>禅道开源版 &lt;= 11.6</td><td>2019</td></tr><tr><td>禅道 任意文件上传漏洞</td><td>CNVD-C-2020-121325</td><td>10.x &lt; 禅道开源版 &lt; 12.4.3</td><td>2020</td></tr><tr><td>禅道 Pro 8.8.2 命令注入漏洞</td><td>CVE-2020-7361</td><td>禅道 Pro &lt;=8.8.2</td><td>2020</td></tr></tbody></table>

从以上表可以看出，近年来禅道漏洞频发，从 2018 年开始，每年都会爆出比较严重的高危漏洞，通过这些高危漏洞均可对服务器造成一定的影响，甚至获取服务器的最高权限。

从漏洞分布的情况来看，禅道大部分的漏洞均属于后台漏洞，这源于禅道属于项目管理软件，均需要登录授权后方可操作系统中的任意模块，而系统中的未授权接口很少，在 18 年爆发一个未授权漏洞后，官方将对外开放的接口全部筛选修复后，就导致对外开发接口极少，切很难有漏洞利用点，故截止到现在，禅道所爆发的漏洞均需要后台一定的权限账户方可执行。

我们可以看到 2018 年禅道爆发出多个漏洞，其实这些漏洞原理基本一致，均为越权调用 getModel 函数导致，后面我们会在详细分析中讲解该部分漏洞的原理。另外，我们发现禅道爆发的漏洞基本存在于开源版，但这不意味着这些漏洞仅存在于开源版，开源版是禅道其他系列的基础框架版本，所以开源版的漏洞大概率也会在于对应兼容系列的对应版本中。且禅道具有可扩展性，所以大部分使用者均可采用开源版，在进行二次开发，适用到自己项目中。

三、漏洞利用链
-------

基于 ZenTaoPMS 高危漏洞，我们可以得出几种可以利用的高危利用链。

#### 3.1 无需权限

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162258-bbc70618-4365-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162258-bbc70618-4365-1.png)

**ZenTaoPMS (8.2-9.2.1) - GetShell**

*   首先明确 ZenTao 框架系列版本, 访问该路径可获取版本信息：`/zentao/index.php?mode=getconfig`
*   如果利用此漏洞，需要系统有文件写入权限。

#### 3.2 仅需低权限

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162341-d5151de4-4365-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162341-d5151de4-4365-1.png)

**ZenTaoPMS <11.6 - GetShell**

*   首先明确 ZenTao 框架系列版本, 访问该路径可获取版本信息：`/zentao/index.php?mode=getconfig`
*   需要获取到 ZenTaoPMS 的后台用户登录账号密码或者 cookie，执行以上漏洞生成 shell，最终可 getshell。

#### 3.3 需要管理员权限

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162415-e9bef332-4365-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162415-e9bef332-4365-1.png)

**ZenTaoPMS < 12.4.3 - GetShell**

*   首先明确 ZenTao 框架系列版本, 访问该路径可获取版本信息：`/zentao/index.php?mode=getconfig`。
*   需要获取到 ZenTaoPMS 的后台管理员账户登录账号密码或者 cookie。
*   漏洞只适用于 Windows 一键安装版（未加安全限制）、Linux 一键安装版（未加安全限制）、安装包版。Windows/Linux 一键安装版 (加入安全限制) 由于做过新上传文件限制，无法执行上传后的文件，导致漏洞无法利用。

**ZenTaoPMS Pro <= 8.8.2 - GetShell**

*   需要获取到 ZenTaoPMS 的后台管理员账户登录账号密码或者 cookie。
*   该漏洞命令执行无回显，可通过 certutil.exe 下载安装远程可利用恶意软件，最终 getshell。

四、高可利用漏洞分析
----------

### 4.0 技术背景：禅道项目管理系统路由模式

禅道有两种路由模式 PATH_INFO、GET 方式，其中 GET 方式为常见的 m=module&f=method 形式传递模块和方法名，而 PATH_INFO 则是通过路径和分隔符的方式传递模块和方法名，路由方式及分隔符定义在 config/config.php 中。

*   PATHINFO：`user-login-L3plbnRhb3BtczEwLjMuMS93d3cv.html` 以伪静态形式在 html 名称中传参
*   GET：`index.php?m=block&f=main&mode=getblockdata` 类似于其他常规 cms 在 get 参数中传参我们

我们从禅道的入口 index.php 文件来进行讲解：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162447-fc6cd9fe-4365-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162447-fc6cd9fe-4365-1.png)

从`index.php`文件，首先看到加载了一些 framework 中的框架类，然后声明了一个路由 $app，之后就做了一些系统的基本判断，最重要的就在最下方的三句话，分别是三个功能：解析请求、检测权限、加载模块；

```
$app->parseRequest();
$common->checkPriv();
$app->loadModule();
```

即 parseRequest() 函数就是路由解析入口。进入到`\framework\base\router.class.php`文件中的`parseRequest()`函数：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162528-153de46e-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162528-153de46e-4366-1.png)

parseRequest() 函数首先用于解析判断 url 是否采用了'GET'或者是'PATH_INFO'模式，其中有一个点就是`isGetUrl()`函数，该函数用于判断 url 是否采用了 GET 模式，具体有以下三种模式：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162617-3210d77c-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162617-3210d77c-4366-1.png)

我们回到 parseRequest() 函数中可以得出，如果系统的默认解析模式是 PATH_INFO，而你的 url 采用的是 GET 模式，系统则会将此次访问的路由解析模式配置修改 GET，故当你的 url 模式与系统默认解析模式不同，系统也会解析，不会报错。所以禅道系统的两种路由解析模式可同时使用。

（1）路由解析中，GET 模式属于非默认模式，但是该种解析方式是 PHP 类 CMS 的常规解析模式，即 m=block&f=main，m 参数负责传递模块名（module），f 参数负责传递方法名（method），由此就可以定位到对应 module 中的`control.php`文件，以及该文件中对应的 method。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162720-579ed4da-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162720-579ed4da-4366-1.png)

（2）路由解析中，PATH_INFO 模式属于系统默认模式，我们在配置文件中可以看到系统默认模式以及对应的分隔符、参数含义:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162750-69d59882-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162750-69d59882-4366-1.png)

我们可以看出 PATH_INFO 的默认分隔符是 -，然后我们进入到 path_info 模式下的`setRouteByPathInfo()`函数，通过分隔符将 url 分割后，第一个值为模块名称`module`，第二个值即为方法`method`:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162816-7974b6b0-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162816-7974b6b0-4366-1.png)

总，两种解析模式解析后获取的最终 module、method 通过 `$this->setControlFile();`方法来寻找对应的文件：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162941-aba2fee4-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162941-aba2fee4-4366-1.png)

自此路由解析结束，定位到对应的模块方法后，就进行了权限验证，即使用者身份是否可以调用该模块与方法，`$common->checkPriv();`，文件`module/common/model.php`:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221163002-b829f7da-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221163002-b829f7da-4366-1.png)

从此方法看出，除了`isOpenMethod`之外，均需要登录后具有对应权限才可访问，不需登录的方法如下所示。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221163025-c5edc7ca-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221163025-c5edc7ca-4366-1.png)

### 4.1 禅道 8.2-9.2.1 SQL 注入漏洞导致 Getshell

#### 4.1.1 漏洞简介

漏洞名称：禅道 8.2-9.2.1SQL 注入前台 Getshell  
漏洞编号：无  
漏洞类型：SQL 注入  
CVSS 评分：无  
漏洞危害等级：高危

#### 4.1.2 漏洞概述

禅道项目管理软件集产品管理、项目管理、质量管理、文档管理、组织管理和事务管理于一体，是一款功能完备的项目管理软件。该漏洞影响版本为禅道 8.2--9.2.1。漏洞出现在系统 orm 框架中，在拼接 order by 的语句过程的时候，未对 limit 部分过滤并直接拼接，导致攻击者构造执行 SQL 语句。在 mysql 权限配置不当的情况下，攻击者可利用该漏洞获取 webshell。

#### 4.1.3 漏洞影响

禅道 8.2 - 9.2.1

#### 4.1.4 漏洞修复

1. 建议受影响的用户升级至 ZenTao 9.2.1 以上版本或打上对应补丁包，下载地址：[https://www.zentao.net/download.html](https://www.zentao.net/download.html)

#### 4.1.5 漏洞利用过程

0x0：随便访问一个不存在的路径，返回页面会出现报错，报错回显出文件的存放路径为。

0x1：根据报错回显的路径，构造 SQL 注入语句将木马写入系统的 EXP。

0x2：将上述 EXP 进行 ASCIIhex 加密，得到加密后的字符串。

0x3：然后将加密后的字符串放入：

```
{"orderBy":"order limit 1;SET @SQL=0x(加密后字符串);PREPARE pord FROM @SQL;EXECUTE pord;-- -","num":"1,1","type":"openedbyme"}
```

0x4：然后将上述语句进行 base64 加密。

0x5：最终通过访问以下语句执行漏洞

```
http://siteserver/zentao/index.php?m=block&f=main&mode=getblockdata&blockid=case&param=base64加密字符串
```

#### 4.1.6 代码分析

我们根据漏洞 PoC 来跟踪漏洞执行流程，从技术背景中的路由解析我们可以定位到漏洞存在的模块是 block 模块中的 main 方法，在经过路由解析后，系统将通过 loadModule() 方法加载对应模块，如下图所示：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221162855-9055d76a-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221162855-9055d76a-4366-1.png)

在处理完 url 路由后，就开始处理方法中的各种参数，通过 setParamsByGET() 函数将参数解析：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221163106-de538c78-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221163106-de538c78-4366-1.png)

在参数解析后，就对各个参数进行过滤检测，若没有问题，最终将解析过滤后的参数进行保存：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221163134-eefbff9c-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221163134-eefbff9c-4366-1.png)

在路由解析和参数解析过滤完之后，就需要通过 call_user_func_array() 函数来调用对应模块的对应方法，然后就进入到 block 模块中的 control.php 文件：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221163157-fd341e00-4366-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221163157-fd341e00-4366-1.png)

在 module/blocak/control.php 文件中的构造函数中，存在一个判断，即需要存在 referer，否则无法执行对应模块的函数。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221163225-0d630dfe-4367-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221163225-0d630dfe-4367-1.png)

在进入到 block 模块中的 main 函数中，通过 mode 参数进入到一下 if 分支，在该分支中，首先对 params 参数进行 base64 解码

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221163911-fff5309c-4367-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221163911-fff5309c-4367-1.png)

然后通过进一步的解析参数，获取到执行 getblocakdata 操作的的函数为 printCaseBlock()

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221163947-155f03b8-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221163947-155f03b8-4368-1.png)

然后进入到本文件中的 printCaseBlock() 函数中，通过解析 params 参数后，得到 type 属性为 openedbyme（可构造），进入到下面的 elseif 分支，我们可以看到参数要进入到 orderby 函数中进行处理，继续跟入到 orderby 函数中：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164035-31c9cd6c-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164035-31c9cd6c-4368-1.png)

在 oderby 函数，系统将 oder 参数进行解析，获取到 orders 和 limit 参数值

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164059-3ff970d6-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164059-3ff970d6-4368-1.png)

接下来就进入到了漏洞产生的关键，即`$order = join(',', $orders) . ' ' . $limit;`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164128-5192a736-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164128-5192a736-4368-1.png)

在该 SQL 语句中将 $limit 直接拼接到最后，导致`limit 1;`闭合了之前的 SQL 语句，而之后的攻击 PoC 就可被执行，由此就造成了该漏洞的 SQL 注入，该 SQL 注入可以写入文件，导致最终的 getshell。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164155-61b3cf28-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164155-61b3cf28-4368-1.png)

### 4.2 禅道 后台代码注入漏洞

#### 4.2.1 漏洞简介

漏洞名称：禅道后台代码注入漏洞  
漏洞编号：无  
漏洞类型：代码注入  
CVSS 评分：无  
漏洞危害等级：高危

#### 4.2.2 漏洞概述

禅道项目管理软件集产品管理、项目管理、质量管理、文档管理、组织管理和事务管理于一体，是一款功能完备的项目管理软件。漏洞属于一种越权调用，普通权限（用户组为 1-10）的攻击者可通过 module/api/control.php 中 getModel 方法，越权调用 module 目录下所有的 model 模块和方法，从而实现 SQL 注入、任意文件读取、远程代码执行、文件包含等攻击。

#### 4.2.3 漏洞影响

禅道开源版 < 11.6

#### 4.2.4 漏洞修复

1. 建议受影响的用户升级至 ZenTao 11.6 以上版本，下载地址：[https://www.zentao.net/download.html](https://www.zentao.net/download.html)

#### 4.2.5 漏洞利用过程

0x0：首先登陆获取登陆 cookie：zentaosid。

0x1：然后访问 api-getModel-editor-save-filePath 后再 api 中生成 shell。

0x2：最后访问 api-getModel-api-getMethod-filePath=，最后文件包含 shell，执行 PHP 代码。

#### 4.2.6 代码分析

我们根据漏洞 PoC 来跟踪漏洞执行流程，从技术背景中的路由解析我们可以定位到漏洞存在的模块是 api 模块中的 getModel 方法，在经过路由解析后，系统将通过 loadModule() 方法加载对应模块，如下图所示：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164253-84402abe-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164253-84402abe-4368-1.png)

进入到 api 的 getModel() 方法中，获取到需要调用的三个参数 module：editor，method：save，params：filePath。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164315-90f6ef72-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164315-90f6ef72-4368-1.png)

然后通过回调函数 call_user_func_array 进入到 editor 模块中：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164349-a5726026-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164349-a5726026-4368-1.png)

进入到 editor 模块中的 model.php 文件中的 save() 函数，通过 save 函数的 file_put_contents 将 fileContent 内容生成为一个文件，

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164424-b9fb84f0-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164424-b9fb84f0-4368-1.png)

最终将输出结果后，进程结束。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164445-c6cb2d3e-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164445-c6cb2d3e-4368-1.png)

然后通过访问 api-getModel-api-getMethod-filePath 文件，解析出 module 为 api，method 为 getModel()，在 getmodel() 函数中又调用了 api 模块的 getmethod() 方法，

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164515-d88a54aa-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164515-d88a54aa-4368-1.png)

进入到 getMethod 方法中，进入到 import 方法：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164621-ffed3bca-4368-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164621-ffed3bca-4368-1.png)

在 import() 方法中，通过 include() 函数包含了 filePath 下的文件，最终执行 PHP 代码

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164644-0d87fd1a-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164644-0d87fd1a-4369-1.png)

### 4.3 禅道 后台文件上传漏洞

#### 4.3.1 漏洞简介

漏洞名称：禅道后台代码注入漏洞  
漏洞编号：CNVD-C-2020-121325  
漏洞类型：文件上传  
CVSS 评分：无  
漏洞危害等级：高危

#### 4.3.2 漏洞概述

禅道官方发布了开源版 12.4.3 的更新公告，本次安全更新禅道官方修复了一个高危漏洞：禅道任意文件上传漏洞，漏洞编号：CNVD-C-2020-121325。登录后的任意攻击者可通过 fopen/fread/fwrite 方法结合 FTP、File 等协议上传或读取任意文件，成功利用该漏洞可以执行任意代码，最终获取服务器最高权限。

#### 4.3.3 漏洞影响

10.x < 禅道开源版 < 12.4.3

#### 4.3.4 漏洞修复

1. 建议受影响的用户升级至 ZenTao 12.4.3 及以上版本，下载地址：[https://www.zentao.net/download.html](https://www.zentao.net/download.html)

#### 4.3.5 漏洞利用过程

0x0：首先登陆获取登陆 cookie：zentaosid。

0x1：然后访问 client-download-[$version 参数]-[base64 加密后的恶意文件地址]-1.html 后再下载远程文件到服务器中

0x2：最后访问 data/cliten/1 / 文件，执行 PHP 代码。

#### 4.3.6 代码分析

我们根据漏洞 PoC 来跟踪漏洞执行流程，从技术背景中的路由解析我们可以定位到漏洞存在的模块是 client 模块中的 download 方法，在经过路由解析后，系统将通过 loadModule() 方法加载对应模块：

进入到 client 的 download() 方法中，获取到需要调用的 2 个参数 $version 和 $link

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164728-27a93592-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164728-27a93592-4369-1.png)

然后跟进到 download() 重点中的 downloadZipPackage() 函数，全局中共有两个 downloadZipPackage 函数，其中一个在 module/client/ext/model/xuanxuan.php：进入到该函数中，我们发现该函数首先将 $link 参数进行 base64 解码后，然后通过 pcre 进行过滤，即路径的协议无法使用 [http://，但是我们可以使用 HTTP 或者 file、ftp 等协议绕过该限制，然后返回到正式的 downloadZipPackage 函数，parent::downloadZipPackage($version](http://，但是我们可以使用HTTP或者file、ftp等协议绕过该限制，然后返回到正式的downloadZipPackage函数，parent::downloadZipPackage($version), $link);

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164749-343e8852-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164749-343e8852-4369-1.png)

接下来进入到 module/client/model.php 中的接下来进入到 module/client/model.php：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164845-56062b8e-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164845-56062b8e-4369-1.png)

在该方法中，我们可以看到 version 参数用于创建一个新的文件夹，即 / data/client/${version}，

然后将 link 参数值进行 base64 解码，最终在新建文件夹下新建文件，然后将远程文件写入到该文件中，最终达到远程文件上传漏洞的目的。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164913-669385fa-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164913-669385fa-4369-1.png)

### 4.4 禅道 Pro 版本任意命令执行漏洞

#### 4.4.1 漏洞简介

漏洞名称：禅道项目管理软件 Pro 版本任意命令执行漏洞  
漏洞编号：CVE-2020-7361  
漏洞类型：命令执行  
CVSS 评分：CVSS 2.0:9.0; CVSS 3.x:8.8  
漏洞危害等级：高危

#### 4.4.2 漏洞概述

EasyCorp ZenTao Pro 是中国自然易软网络技术（EasyCorp）公司的一套开源项目管理软件。该软件包括产品管理、项目管理、质量管理和文档管理等功能。EasyCorp ZenTao Pro 8.8.2 及之前版本中的 / pro/repo-create.html 文件存在操作系统命令注入漏洞。攻击者可借助‘path’参数利用该漏洞以 SYSTEM 权限执行任意命令。

#### 4.4.3 漏洞影响

禅道 Pro <= 8.8.2

#### 4.4.4 漏洞修复

目前厂商已发布升级补丁以修复漏洞，补丁获取链接：

1. 建议受影响的用户升级至 ZenTao pro 8.8.2 以上版本，下载地址：[https://www.zentao.net/download.html](https://www.zentao.net/download.html)

#### 4.4.5 漏洞利用过程

0x0：首先登陆到管理员账户。

0x1：通过`/repo-create.html(/index.php?m=repo&f=create)`页面下的 client 参数执行系统命令，将恶意软件下载到服务器中。

```
SCM=Git&name=test2&path=C%3A%5CProgramData&encoding=utf-8&client=cmd1
```

0x2：通过 repo-create.html 页面下的 client 参数执行系统命令，使用反弹 shell，以达到 getshell 的目的。

```
SCM=Git&name=test2&path=C%3A%5CProgramData&encoding=utf-8&client=cmd2
```

#### 4.4.6 代码分析

我们根据漏洞 PoC 来跟踪漏洞执行流程，从技术背景中的路由解析我们可以定位到漏洞存在的模块是 repo 模块中的 create 方法，在经过路由解析后，系统将通过 loadModule() 方法加载对应模块，如下图所示：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221164940-76d44382-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221164940-76d44382-4369-1.png)

然后通过 call_user_func_array() 函数调用对应模块以及对应方法：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221165040-9a284676-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221165040-9a284676-4369-1.png)

在 module/repo/control.php 文件中的 create() 函数中，如果是 post 的数据，首先进入到`$repoID = $this->repo->create();`该处的 create() 方法是调用的 model.php 文件中的 create() 方法：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221165106-a99c5dea-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221165106-a99c5dea-4369-1.png)

进入到 module/repo/model.php 方法中，首先进入到 create() 方法中，发现第一步需要执行 checkConnection():

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221170320-5f9bf4e2-436b-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221170320-5f9bf4e2-436b-1.png)

在 checkConnection() 函数中，首先获取到对应参数值，由此发现参数在此未做过滤，继续往下看：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221165233-dde7d6c4-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221165233-dde7d6c4-4369-1.png)

如果 SCM=git 的话，则判断 path 下的文件是否存在，如果不存在则返回 false。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221165311-f42d3514-4369-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221165311-f42d3514-4369-1.png)

然后进入到本漏洞的触发点了，command 参数直接与 tag 2>&1 拼接，带入到 exec() 函数执行:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20201221165344-0849ff64-436a-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20201221165344-0849ff64-436a-1.png)

五、漏洞利用
------

关注**深信服千里目安全实验室**微信订阅号观看漏洞利用完整视频。

六、深信服解决方案
---------

【**深信服下一代防火墙**】可轻松防御此类漏洞， 建议部署深信服下一代防火墙的用户更新至最新的版本，可轻松抵御此高危风险。

【**深信服云盾**】已第一时间从云端自动更新防护规则，云盾用户无需操作，即可轻松、快速防御此类高危风险。

【**深信服安全感知平台**】可检测利用该类漏洞的攻击，实时告警，并可联动【深信服下一代防火墙等产品】实现对攻击者 ip 的封堵。

【**深信服安全运营服务**】深信服云端安全专家提供 7*24 小时持续的安全运营服务。在漏洞爆发之初，云端安全专家即对客户的网络环境进行漏洞扫描，保障第一时间检查客户的主机是否存在此类漏洞。对存在漏洞的用户，检查并更新了客户防护设备的策略，确保客户防护设备可以防御此类漏洞风险。

【**深信服安全云眼**】在漏洞爆发之初，已完成检测更新，对所有用户网站探测，保障用户安全。不清楚自身业务是否存在漏洞的用户，可注册信服云眼账号，获取 30 天免费安全体验。

注册地址：[http://saas.sangfor.com.cn](http://saas.sangfor.com.cn/)

【**深信服云镜**】在漏洞爆发第一时间即完成检测能力的发布，部署了云镜的用户可以通过升级来快速检测网络中是否受该高危风险影响，避免被攻击者利用。离线使用云镜的用户需要下载离线更新包来获得漏洞检测能力，可以连接云端升级的用户可自动获得漏洞检测能力。