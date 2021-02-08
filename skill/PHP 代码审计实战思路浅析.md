> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Yi4-0Z0C1GDtyaJAeCB1wQ)

_**声明**_

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测以及文章作者不为此承担任何责任。  
雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_**No.1  
**_

_**前言**_

每一次总结，都可以看作是对前面所学做一次 “大扫除”，就像电脑硬盘，只有将那些缓存文件都清掉，才能腾出更多空间来存新的内容。这次的“大扫除”，以 PHPCMS 为例，以“通读全文”、“敏感函数回溯”、“定向功能点审计” 为切入点，重新梳理一遍平时的审计思路。

望大佬们多多指教！

_**No.2  
**_

_**通读全文**_

通读全文！从字面意思来看，可以理解成把所有的代码都读一遍，把所有的代码都 “读透”。那么问题来了，现在的 cms 大多数都是参照 mvc 模式进行开发，一个大的系统被拆分成视图（View）、模型（Model）、控制器（Controller）三个部分。这种软件架构虽然能使得程序的结构变得更加直观，但也只能说是逻辑上的直观，因为在使得程序结构变得直观的同时，也增加了系统结构和实现的复杂度，所以在审计这类 cms 时，很难通过目录结构或者直接搜索危险函数来进行快速审计。原因在于，基于 mvc 模式开发出来的 cms 不像面向过程化开发的 cms 那样，一个目录就是一个功能模块，一个 php 文件就是一个功能点。基于 mvc 模式开发的 cms，会有一个统一的入口，所有的请求都从该入口进入，然后由框架统一进行调度，且程序中的一些可重用的操作，例如数据库操作、缓存、安全过滤等都会被封装成框架的核心类库，需要时再去调框架封装好的方法。如果在没了解程序的结构前，就贸然去跟某段代码，很容易迷失在一个个类库的调用链里。

那么，我们在审计这类 cms 时，首要目的就是，了解程序的基本结构。前面提到，基于 mvc 模式开发的 cms，会有一个统一的入口，所有的请求都从该入口进入。如果我们想读懂这套源码，这个入口倒是个很好的切入点。在正式上手分析前，先来思考下，当一个请求进入这套程序的入口后，程序内部会对它做哪些操作。例如，这个 url 会怎么解析？程序内部是怎么将 url 与控制器关联到一起的？实际分析时会经常看到 “Demo::test()” 这种调用方式，但 Demo 类并不在这个文件内，而且文件内也没看到 include 或 require，所以这些在程序内部又是怎么实现的呢？

俗话说，要用魔法来打败魔法。既然这是属于开发的东西，在正式分析前，还得来找开发取一下经。先来看下框架的运行流程。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk5seb2asVTIibPEg8MDvTvr2VaGybHny8VGG8twht1Z9Nx1fwcKN3Bicg/640?wx_fmt=png)

入口文件，对应着前面说的统一入口，虽然说是统一入口，但实际情况中入口文件可能有多个，前台一个、后台一个、接口一个。入口文件的职责在于，定义一些全局性的常量，加载函数库，加载框架启动类等等。这里的自动加载类，说成类自动加载会更加合适，主要目的是，为了简化类加载的步骤，通常会将类文件的加载操作封装成一个函数或者方法，然后在框架启动前或者在框架启动时，通过 spl_autoload_register 将类加载函数注册到 SPL__autoload 函数队列中，当程序内的代码调用某个类时，php 会调用类加载函数，类加载函数就会到正确的地方去把类库文件加载进来；当然也可以不使用 spl_autoload_register 函数来自动调用，而是在需要时手动去调用。再下一步，就是启动框架。框架启动后，可能会去加载一些配置文件，然后去调用路由类来解析请求 url，根据解析的结果来调用相应的控制器，最后返回结果。

通常情况下，入口文件的位置在网站的根目录下，一般会命名成 index.php、admin.php 或者 api.php。观察当前项目的目录及文件。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkKiaNZsHNEhAiaMxHnzI3VYRRPknMT0wSwnib5GI56wgmymLuFTBBSj4ug/640?wx_fmt=png)

这里的 index.php、admin.php、api.php 和 plugin.php 都挺像入口文件的，这里选择先跟进 index.php。原因是，一般情况下，前台的入口都叫 index.php。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk7XK13ZG7cdmYtBYlhFvQVmaGYvth09wjsZG9ZCM04ChODlIjCTSA2g/640?wx_fmt=png)

代码很简单，定义了一个常量，然后是加载一个 php 文件，最后调用 pc_base 类的 create_app 方法。入口文件、定义常量，那下面的 pc_base 很大可能就是框架启动类了，跟进到 / phpcms/base.php。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZky1kODOCvgs6MppPnHrMib6o3X7bcygVA6mAxkpA2XicfAiaActffjlDRg/640?wx_fmt=png)

往下翻，能看到很多定义常量，还有加载函数库的操作。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkPgKuvjHnCSHySndqQ5njjY9c2QbxlRmdSETOyDXA19LJ9VibgLkkF8A/640?wx_fmt=png)

继续往下看，就看到了在入口文件中调用的 pc_base::create_app 方法

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkq2VvvaiaDwNHJMnYSBMkmcEZl84K4MnS9Wq5h0wiaES8mRDv5sxa4kgQ/640?wx_fmt=png)

从注释来看，该方法的作用是初始化应用程序，继续跟进 load_sys_class 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkGL3o6lu2YBNzHGa0axTaRx91MJxXaokcKaXalorhoibPFibGLQUpbNcw/640?wx_fmt=png)

从注释来看，该方法用于加载系统类，继续跟进_load_class 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkC24CBhovibApxib3HGss9l523IpQ1yABiaDwoQPwtILvZhW8k5dn4GLRQ/640?wx_fmt=png)

同样，也可以通过注释来了解该方法的作用。

_load_class 方法用于加载类文件，对应着前面说的类自动加载，找到类加载函数后，继续分析类文件的加载逻辑。从代码中可得知，类库目录在 phpcms 框架目录下的 $path 目录，也就是 / phpcms 目录下，类文件名为 “类名. class.php”，如果 $path 参数为空，则默认到 / phpcms/libs/classes 目录下去加载类文件，然后根据 $initialize 参数来决定是否实例化该类。前面的 load_sys_class 方法在调用 load_class 时，传入的 $path 参数是空的，且 $initialize=1，也就是说，/phpcms/libs/classes 目录下放的是系统类，且加载系统类库时会自动实例化该类。除了 load_sys_class，还有 load_app_class 和 load_model，三者的底层都是调用了_load_class，区别在于传入的 $path 不同。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkssvcDDRCrISOkmLU2UfTatxfcSmpUV1K3icJI8WUMxrVqaiaBfRgkgLw/640?wx_fmt=png)

除了加载类库的_load_class，还有加载函数库的_load_func，和加载配置文件的_load_config。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkopiccAxpCzjCPajicZBVf2Pg3bib7OmBg1H91uqghy2PtuzCe0DyRQjxg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkAQicsoPsZufXnsrO46IhnflNpSffkicoVIauTNW7BvBMHXlUYPLn90Eg/640?wx_fmt=png)

通过对类加载方法、函数库加载方法、配置文件加载方法的分析，就能找出程序的基本目录结构。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk7ia0ENINc8xo6eSjaEmibUOIibahERf3LD8VxWSCOcicOetYMJDyFIakTw/640?wx_fmt=png)

回到前面用来初始化应用程序的 create_app 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkORYKicXgKHibGWTYiaMyqmdnhfUjGVNLVA5ricGMIwLAoPtFEZmR8zcz6A/640?wx_fmt=png)

跟进到 application 类

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkKJA553Y242blQ9iblM5HexfDk6wmwqHHmxib5X5whKkFczrhNv9evsZw/640?wx_fmt=png)

回顾前面提到的框架运行流程，从入口文件，到类自动加载，到启动框架，框架启动后，下一步就是路由解析，那 param 类很大可能就是路由类，继续跟进 param 类。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkxmicBRAjeTb1tw8e437TrG5ia7Q6ZP3icD3iaiaKnicpDuHeiazdyPyebOn0A/640?wx_fmt=png)

在 param 类的构造方法中会使用封装后的 addslashes 函数对 $_POST、$_GET、$_COOKIE 数组进行转义。再往后就是调用 route_m、route_c、route_a 方法解析路由，获取模块、控制器和方法名。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkahqnib2fzVGsmBIwbN0siaC7GZeR5F6RCyzsIAf67JUb3XMkuibY9oI1A/640?wx_fmt=png)

route_m 方法获取 m 参数的值作为模块名，同理，route_c 则是获取 c 参数的值，route_a 则是获取 a 参数的值。同时还会调用 safe_deal 方法对传入的值做过滤。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkTyQib6L1BzicWpoAPwAyHJGqvvXZzBEskw4kkZZkE0KkV89OR4nMicaKg/640?wx_fmt=png)

路由解析完后，再下一步就是加载控制器。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkBpx1zxJWiaD1GOLic1HefkoHsHCibfxsd3F6pjYDgIWdHAdEXNyRH0eZA/640?wx_fmt=png)

继续跟进 init 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkPqYwJQ24wcxAKLrCQCwjOFJa1h9QX8VDY6PoUmMCLGSZlYoTfoJ6ew/640?wx_fmt=png)

继续跟进 load_controller 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkQZWXZnXibI7HBYfsgPLl02MC0OAjfb5l7WUxjlb7xco42RpDichcM9KA/640?wx_fmt=png)

load_controller 方法先到 “/phpcms/modules / 模块名 /” 目录下加载控制器文件，然后实例化并返回对象。

init 方法通过 load_controller 方法获取到控制器实例后，通过 call_user_func 方法来执行具体的动作，最后返回结果，请求结束。

_**No.3  
**_

_**敏感函数回溯**_

当输入的数据，被当作代码去执行，或者会改变原本设定好的代码逻辑，就可能产生漏洞。拿 SQL 注入来说，当外部输入的数据被带到数据中执行，并且能通过构造特殊的内容来修改原有的 SQL 语句结构，就会产生 SQL 注入。如果我们想挖掘 SQL 注入漏洞，就应该把关注点放在数据库查询操作上，而 PHP 中能执行 SQL 语句的函数有 mysql_query、mysqli_query 等，这些函数就可以称为敏感函数。从代码中找到这些敏感函数的调用位置，然后去回溯其参数来源，如果来源可控，就存在漏洞。同理，如果想找代码执行漏洞，可以去找能执行代码的函数，例如 assest、eval、call_user_func 等；如果想找命令执行，就去找能执行系统命令的函数，例如 system、shell_exec、popen 等。通常的做法有，使用编辑器进行全文检索敏感函数的函数名，然后人工一个个去回溯参数来源，还可以使用一些代码审计工具来进行扫描分析，然后再手动去验证。为了节省时间，一般会先工具扫描一遍，快速找出那些比较明显的漏洞。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkiau3ybY4pyaFweT3eYk9rd3r5mTNiac0tq4L1s9cwTfb0P2d3FQWgDBw/640?wx_fmt=png)

扫描结果里的代码注入看到倒是很吸引人，那就先从它入手。从代码来看，很明显的一个 eval 代码注入。这段代码存在于 / phpsso_server/phpcms/libs/functions/global.func.php，从文件名和文件路径来看，string2array 函数位于系统函数库中。从左下角的调用链来看，在 / phpsso_server/phpcms/modules/admin/credit.php 文件中调用了 string2array，/phpsso_server 目录下的结构于上面的分析的一样，根据上面的分析结果，可得知，credit.php 是一个控制类文件。跟进到 credit.php 的 94 行。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkUOl41jT3jiaJbdRTGIvsFdg4VrWqHJGXR82Eku3cXyWcR0xibdyO3icwA/640?wx_fmt=png)

在 92 行的位置，将 ps_send 函数的返回结果赋值给 $res，观察左下角的调用链，发现最后调用了 fread 函数，同时结合传入给 ps_send 函数的参数名推测，该函数应该是用来发起 http 请求的，后续跟进分析，得到的结果也是。那 creditlist 方法的作用应该发起一个请求，将请求结果转换成数组，然后遍历输出。如果能控制响应结果，就能形成代码执行漏洞，而控制了请求 url，就能控制响应的结果。

继续分析，在 88 行的位置，将 $applist[$appid][‘url’] . $applist[$appid][‘apifilename’] 赋值给 $url。

在 87 行，将 getcache 函数的返回结果赋值给 $applist。$appid 由 get 传入，可控。如果 getcache 的返回结果可控，就有希望实现代码执行。跟进 getcache，根据前面的分析，知道在框架启动前会加载系统的函数库，所以可以到系统函数库中寻找 getcache 函数。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkO1oBA7OrwO6nSiaysa69YurIibJr35mcsyhhDibVaAic1YIveiab7XcAbjw/640?wx_fmt=png)

先是加载配置文件，然后调用 cache_factory::get_instance()，配置文件内容如下。  

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkGGl8xzEFuGQZqdK8gvDG12fEQoeKbE0icicc5Dzs4pmdhJDZvPq5lwSw/640?wx_fmt=png)

跟进 cache_factory::get_instance

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkQMWfjt74eRmfIpDs1vV8Y7ibEGqjozSNWicfLjZCfO6kqmNibwCN726tA/640?wx_fmt=png)

跟进 get_cache 方法

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkw9LKKkJB93HrDZbibScqTKb55roN8RuOH3npHC6nDk7Ivg8MrpKL7OA/640?wx_fmt=png)

跟进 load 方法  

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkzbpNCoiaoBazro5q2DYhpV87s3QicYLETSNEmPmb6Duk7xrfsyLT3hNQ/640?wx_fmt=png)

load 方法根据传入的缓存配置信息来决定是加载文件缓存还是 memcache，而默认情况是加载文件缓存。回到前面的 getcache 函数，获取到缓存类的实例后，调用该类的 get 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkmicCwEycalGWXsezlW8H5zYB01Umfeg6q17JLd8nxekOChBMFw3qLUQ/640?wx_fmt=png)

默认情况下使用文件缓存，所以该方法应该是位于 cache_file 类。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkkISxDR1VNgOnKKhuicq9RG67fvFQImNFCLreiaAM6f1PISp3KMScKLHQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkbwp4F0DSyfD3EFAibCtJps9ibnIKkEoKCCssicJpYmPoODjEV3JlMMcmw/640?wx_fmt=png)

从 get 方法内的代码来看，缓存文件的路径在 / caches/caches_模块名 / caches_$type / 下，默认情况下通过 require 引入并将结果复制给 $data 返回。

回到 credit.php 的 creditlist 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkWa8PzPKAxXX6yyMyFbiaLUfNSIcDvDH4SOOp7buqTXjDstAh0XCZqew/640?wx_fmt=png)

87 行，将 getcache 的返回结果赋值给 $applist，getcache 的调用链如下。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkiadWhlpxoz1ibicPdibibMUjOh8ib0sX9DMrKm4JzDecJcfXgmobpEpQ7adw/640?wx_fmt=png)

$applist 的内容如下：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkKe8baQNd7nVr2VxfolpfoK0k2uH7oicfyzNnAEmxLDLG6wQNrQdzhZg/640?wx_fmt=png)

既然 $applist 来源于缓存文件，那如果能找到写入缓存的点，没准就能控制缓存的内容，配合前面的 creditlist 方法实现代码执行。找到写入缓存的方法为 set，文件路径拼接跟 get 差不多。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk0MSMiahVPicWo1epxqbaC0IF9iapAWY5YJSnicaZmibrVaI0NMezXHEYicSA/640?wx_fmt=png)

通过回溯 set 方法的调用链即可找出写入缓存的点。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkEyQuMfcw1t6b4tAEwh9ia6w9guQ6pynsxFvEkmjg7Jg5LgrjMDicbDtw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkSFzXOAYQm4KooluYYRkq4DicpZ4oXWlgm7tbNYYoly7oADmCXPuX6nA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkY9hfE2UvhZFxG3kHoJWDvic08H9LiaaVQ4plUCFRMwhicR4WprbH5Lx9g/640?wx_fmt=png)

最后在 applications 控制器的 add 方法中找到写入缓存的点。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkIicicNGex0KXjKlOx65knh8dj3qGetwKBecpkI7mtoqD9xxUO4LZswhA/640?wx_fmt=png)

在 applications 类的 add 方法，39 行处，将 url 写入数据库，回溯 $url 的来源，发现在 26 行处通过 post 传入。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkoaShffhIsscdXbTr5e1bBfXNgQ7scicOxOVozaKktXsziaDZZTl9F5lQ/640?wx_fmt=png)

确定 url 可控，接下来开始构造利用链。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk0dTncIdkzRL15FfJg0hMETZEiac2vlMrKnE2hKia5EvklGhbVnnGp99g/640?wx_fmt=png)

**漏洞利用过程：**

1. 访问 http://192.168.195.1/phpsso_server/index.php，登录 phpsso。

2. 访问 http://192.168.195.1/phpsso_server/index.php?m=admin&c=applications&a=add。

3. 填入应用地址，既 url，点提交，即可将 url 写入 applist 缓存。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkT1Jaics8RgrooWqlhe3wstyBmiaXRWJJjcicOp0NiakK4P7JY96Yb2mTsg/640?wx_fmt=png)

添加成功后跳转回应用管理页面

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkuV7VQsxCibOeyqc68LwIZcVgwOK8eBOyvx0pvaRnajN3M5FV1y6TR0w/640?wx_fmt=png)

在编辑按钮的请求 url 中可以得到刚刚添加的 appid。

1. 服务器启动一个 php 的 server，并创建一个 evil.php，内容如下：

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk9R786he4dibWJ8ldUP61JHX14E5o89biaU8olXsguj28RkRkYpyXkBKQ/640?wx_fmt=png)

2. 访问 http://192.168.195.1/phpsso_server/index.php?m=admin&c=credit&a=creditlist&appid=2 即可触发代码执行。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkZGtcKJ6AOYnU8Kz7GGZjROV7j8HqmS2tqRsYVviaCm3Uh4jicy4DhJqA/640?wx_fmt=png)

_**No.4  
**_

_**定向功能点审计**_

定向功能点审计感觉更像是黑盒白盒的结合体，通过去浏览网站的功能，对可能存在问题的功能点的代码进行审计，检查是否存在问题。例如，发表留言、发送站内信这些功能，比较容易产生跨站脚本漏洞，审计时可以优先关注 php 代码中，数据在输入输出时是否有被 html 编码，如果没有，那就看下，有没有 xss 代码过滤，如果两者都没有，那很大可能就存在 xss，如果有 xss 过滤，则可以通过分析过滤了那些特殊字符或关键字，如果能找到没有过滤的关键字，就能绕过过滤。前面分析框架运行流程时，对控制器和模型的存放位置，以及调用方式都有所了解，但 mvc，除了 m 和 c，还有个 v。视图解析，这个贯穿全局的功能，一般情况下是不太容易出问题，但如果存在二次解析，那出现漏洞的概率就要高上不少。

如果不清楚哪个是模板解析类，可以选取一个功能点作为切入点，一步步定位到模板解析类，例如，首页。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZksmxezeBPaoCe153as2ERQ3NJXVKuZSQaFxWyWlp2MibK1tfe95ZibUFQ/640?wx_fmt=png)

其他代码不是我们的关注点，getcache 函数是获取缓存的，seo 怎么看也不像视图解析的，直接到系统函数库找 template 函数。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkB7Cn21jl9U2UoUooKQiaU8swUBGicb8ur0icqI7ZehHNNgo6oXwMKo5iag/640?wx_fmt=png)

无关紧要的代码先忽略，优先找跟模板加载有关的代码。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkrIlbhUHTttQRibtEL577NA3FjzBHkgiclOEPspH193BtTSEQ00HnbBEg/640?wx_fmt=png)

在 456 行的位置，将 template_cache 类加载进来。然后到 / caches/caches_template / 下找模板文件，推测这里存的应该是编译后的模板文件。

如果 $compiledtplfile 存在则返回 $compiledtplfile 的路径给 template 函数进行包含。

如果 $compiledtplfile 不存在，则调用 $template_cache->template_compile 方法进行编译生成 $compiledtplfile 文件，然后再包含，跟进 template_compile 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk07mqTvFFftOEhLaZAia94CLE8RzdezdesPGwntdKECWm2DtCGnWbQyQ/640?wx_fmt=png)

从代码中可得知，16-34 行的主要作用是到 / templates/default / 模块 / 目录下读取模板文件。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk7kh6b95EHYyFLrusceO1rUiaCnHes7zEXKx2tJeTHU3Fxv39jbLG7rw/640?wx_fmt=png)

然后调用 template_parse 方法解析模板内容，将解析后的结果写入模板缓存。继续跟进 template_parse 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkhsPconP10JO2h6CbqbvvR6wu0RAzYTp0lKfTIyGWcJQoVUul7teXhg/640?wx_fmt=png)

解析规则如上图，直接解析成 php 代码的不在关注范围内，原因是，通常情况下，这些标签内容都是不可控的。模板内容不可控的情况下，一般会把注意力放在，那些将解析后的结果交给其他方法再进行一次处理的的解析规则上。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk6UWEVbXaOSqqYU76fL7TuG0Fb1xpIUwSeZg7aTl6cOWoroEDy7H6gA/640?wx_fmt=png)

例如 91 行，93 行。91 行将从模板中匹配到交给 $this->addquote 进行处理，但 $this->addquote 方法仅仅是将传入的内容再转义一下，没什么特别的地方，继续看 93 行处的 self::pc_tag 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkJPq4bICkDXPpXfaFVwAqqb5rzG8BwicHAVjUq9lX7JxYEpfdkSww33w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkenRWHMiblC7xncWyrnCkYd9jtyV8SCcaFwVUDeicD1icjJ7IAIjkJbeiaQ/640?wx_fmt=png)

从注释来看，pc_tag 会对前面解析到的内容再进行一次解析，同时还会在解析后的代码前面加入一段 “死亡代码 “。

当 $op 为 block 时，会生成以下代码。最后将二次解析后的代码写入模板缓存，然后在访问相关页面时去包含。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkzwDIYDYCLCWIQQr0Wm94vlIMRHiaCqJhwcde0MltDia2Tn2AU5Nstfaw/640?wx_fmt=png)

当上述生成的模板缓存被包含时，会去调用应用类 block_tag 的 pc_tag 方法，跟进 block_tag->pc_tag 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkWJ7gApnvxZSCBichRSNrSKQXbqyVdNQWex9icxNse8gicGECbVsbRnyfw/640?wx_fmt=png)

该方法根据传入的参数到数据库中查询，然后将查询结果转换成变量，然后走到 string2array，也就是前面那个代码注入的点，但这里存在漏洞的点不是这，原因在于，$data 是从模板中提取出来的，而模板的内容我们是不可控的，继续往下走，进到 $template_url 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkjjs9v460OT3QCWXRqiculUiaGXafwu1ySEZyqsQ7cata8Cra6Ur70yLA/640?wx_fmt=png)

如果 $template 变量不为空，则将 $template 的内容写入 / caches/caches_template/block/$id.php

如果 $template 的值为空，则根据 $id 到数据库中取出 template 字段的内容，并写入 / caches/caches_template/block/$id.php 文件中，如果能同时控制 $id 和 $template，或者能控制数据库中的内容，就可以构造一个恶意文件，然后利用上面的 pc 标签解析功能包含该文件，实现代码执行。

回到前面的模板解析步骤，分析具体的解析规则。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkIo6p14JQlx8hfStxJxUHhq6rn6w4picvgUNW9aEqgfYUM75Ht3DazyQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkjnNxzicfVpRSjjCZPkafP3oXzibxqx2Qv3reSBBnLQHDqiaqb7kJHPlpQ/640?wx_fmt=png)

通过分析上面的正则可得知，pc 标签的格式应该为 {pc:xx xxx}。

在 self::pc_tag 方法中将 $data 按照 116 行的正则再进行一次提取，将提取的结果通过循环，写到 $datas 数组中。所以，pc 标签的格式应该为 {pc:xx xx=xx}。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkv7WdkE4b9QpeaNaRiclSQSjF0Kia28cpPiaIQL5Ukerh7uKgNNUQuyEKQ/640?wx_fmt=png)

当 $op 等于 block 时，将前面提取的 $datas 传入 arr_to_html 方法，转成 array(key=>value) 这种格式，然后生成以下代码。所以，如果想进入以下分支，pc 标签的格式应该为 {pc:block xx=xx}。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk4nJbTxgc8CoPx4dg5qItw27BTSicAicGibSSbBEZiagRGasWY9c0wFa9icw/640?wx_fmt=png)

继续跟进 $block_tag->tag 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkolRvjQtzHAVvIoPk3icS7tzwU9OpRfJkReVv4icaHp06hH2YbaZ76F8g/640?wx_fmt=png)

发现会将 $data[‘pos’] 带入数据库查询，如果结果为空，就不会进入到包含点。所以，pc 标签的格式应该为 {pc:block pos=xx}，通过搜索 pc 标签找到相关触发点。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkjKRdzVJQicP7uDvTS6CuP51PicmuUBCsNe0EvjhibbLJkUbUhMhalHc8Q/640?wx_fmt=png)

根据前面的分析，可得知，触发点在 link 模块下，在 link 模块的 index 控制器中找到的 register 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkN6HnLqj8UIibULoVqSTbGrnib1iaaFibmLOGjB8tz2UqMyn1QJaWVA3SicQ/640?wx_fmt=png)

但仅有触发点还不够，前面提到，被包含的文件的内容从数据库中获取，所以还需要找到一个讲恶意代码写入数据库的点，或者找一处调用了 block_tag->template_url 方法的点，但 id 和 template 参数需可控。如果想找写入数据库的点，可以优先到与 block_tag 类位于同一个模块的 block_admin 类下找。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkLZuxL4V1e8ibr6UH5rb692siaCyQD5iaqWJcVUHNfsKDZKVynOgj5Nrsw/640?wx_fmt=png)

经过一番寻找，发现 add 方法有写入数据库的操作，但并没有发现写入 template 字段的代码。除了插入数据库，还可以找找更新数据库的点。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkrfFrElVWAT47eJc44lQGG0JbElTdtRT2Ff9ia7vn704wuAjbSABkU0w/640?wx_fmt=png)

发现在 block_update 方法中执行了 update 操作，还会将 template 写入数据库，同时 template 还是从 post 传入。146 行处虽然有调用 template_url 方法，但 $id 并不可控，原因是，在 128 行将 id 带入到数据库中查询，如果查询结果为空，则不会进入到下面的操作。而 id 在数据库中是递增的，未必能控制在 [1、2、3] 中。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkVzzrdicj7a3uCbs8Yw6tF6YiclhjlHLZlOjl5KG1RBTMzOSd0sKe0GIg/640?wx_fmt=png)

但可以先利用 add 方法添加一条记录，然后利用 block_update 将恶意代码写入数据库，最后通过访问相关页面触发 pc 标签解析，生成并包含恶意文件。

**漏洞利用思路：**

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkXDgPRddRwCV6qsZNPCN7tnZWvtsN2nl4ndonkgv3vWbktbz57zsSxg/640?wx_fmt=png)

**漏洞触发流程：**

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk6N1A5to7w7D6VaHfTTiaKTxmgNnPxr7eR6B59Ill30Uh3vGc8O4icS6Q/640?wx_fmt=png)

**漏洞利用过程：**

先向数据库中添加一条记录，pos 的值须在 [1, 2, 3] 中，type 的值为 2，pc_hash 登录后自动生成，需替换成当前登录用户的**。**

```
URL:http://192.168.0.1/index.php?m=block&c=block_admin&a=add&pos=1&pc_hash=gh43rD

POST:dosubmit=&name=bb&type=2
```

‍

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkaewL0cBefxZf08eM0xLOLP3icP0xczqOz0WSViaiazvEz5pGT1CLnliaJg/640?wx_fmt=png)

然后更新数据库记录将恶意代码写入数据库，从上一条请求的放回结果中获取 id。

```
URL:http://192.168.0.1/index.php?m=block&c=block_admin&a=block_update&id=1&pc_hash=gh43rD

POST: dosubmit=&template=\<?php phpinfo();?\>
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZk7uKfW8cmXyI2RbfyDZBckhxJQUdOMl2AicR8Sl7cWbSXznqEmE8wiaqQ/640?wx_fmt=png)

访问 http://192.168.195.1/index.php?m=link&c=index&a=register&siteid=1 触发 pc 标签解析，包含恶意文件。

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXSdlqEBQJSPEmQ3Y66zaZkFd3Z7taKRictKEibhV7sVNawkWIrdeOl5S7UEnumpOAHJcTY4Euc2s4Q/640?wx_fmt=png)

_**招聘启事**_

安恒雷神众测 SRC 运营（实习生）  
————————  
【职责描述】  
1.  负责 SRC 的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2.  负责白帽子提交漏洞的漏洞审核、Rank 评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

简历投递至

bountyteam@dbappsecurity.com.cn

设计师（实习生）

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
3、有品牌传播、产品设计或新媒体视觉工作经历；  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦 19 楼  
学历要求：本科及以上  
工作年限：1 年及以上，条件优秀者可放宽

简历投递至 

bountyteam@dbappsecurity.com.cn

安全招聘  
————————  
公司：安恒信息  
岗位：Web 安全 安全研究员  
部门：战略支援部  
薪资：13-30K  
工作年限：1 年 +  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
【岗位职责】  
1. 定期面向部门、全公司技术分享;  
2. 前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3. 负责完成部门渗透测试、红蓝对抗业务;  
4. 负责自动化平台建设  
5. 负责针对常见 WAF 产品规则进行测试并落地 bypass 方案  
【岗位要求】  
1. 至少 1 年安全领域工作经验；  
2. 熟悉 HTTP 协议相关技术  
3. 拥有大型产品、CMS、厂商漏洞挖掘案例；  
4. 熟练掌握 php、java、asp.net 代码审计基础（一种或多种）  
5. 精通 Web Fuzz 模糊测试漏洞挖掘技术  
6. 精通 OWASP TOP 10 安全漏洞原理并熟悉漏洞利用方法  
7. 有过独立分析漏洞的经验，熟悉各种 Web 调试技巧  
8. 熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
【加分项】  
1. 具备良好的英语文档阅读能力；  
2. 曾参加过技术沙龙担任嘉宾进行技术分享；  
3. 具有 CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP 等安全相关资质者；  
4. 具有大型 SRC 漏洞提交经验、获得年度表彰、大型 CTF 夺得名次者；  
5. 开发过安全相关的开源项目；  
6. 具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7. 个人技术博客；  
8. 在优质社区投稿过文章；

岗位：安全红队武器自动化工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 熟练使用 Python、java、c/c++ 等至少一门语言作为主要开发语言；  
2. 熟练使用 Django、flask 等常用 web 开发框架、以及熟练使用 mysql、mongoDB、redis 等数据存储方案；  
3: 熟悉域安全以及内网横向渗透、常见 web 等漏洞原理；  
4. 对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5. 具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JXsXUiaDfpQ6MaRHMZ6YOVmJcTib286GQcKicWTGz6ayWdjqYrzq36VzSq6TnRORY3GKoHntMQ2LBkKg/640?wx_fmt=jpeg)

专注渗透测试技术

全球最新网络攻击技术

END

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JWUFSUTshk23sjjpXhJrMu2z6MIL9pdkYkm0wicXRrgNLWvr04znZtqs8wexe5qbZxyOzRerwpSotg/640?wx_fmt=jpeg)