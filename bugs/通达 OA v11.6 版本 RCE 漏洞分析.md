> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=Mzg4NTA0MDg2MA==&mid=2247484173&idx=1&sn=f81f44880b0b97910e2ac464c03b8d86&chksm=cfafb0bef8d839a815b5f7294a4e83e3f086f9ee3f2c5afe85b984fa331f764b192347af1428&mpshare=1&scene=1&srcid=0820PwnG92KfBkwwClZqH0Am&sharer_sharetime=1597894721833&sharer_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=4cf40c946f4d610c47153e395b1ac6b26d37d72e4a779dfc6bb7b06a28069393c8f3b219f64430511dab66bc4df7d22075e588e8756e0d582e646bcc8996f0c4c2668a784951fb32720124ed86ef57400a73f2b20057903b401834f2bdd7ca56d7c610b1a87d604cf2b30585e03eda3346f2fe67626bf17153b7be4409c30785&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=62090529&lang=zh_CN&exportkey=Af8OdjuMk2zZZz%2FLKkUYuH8%3D&pass_ticket=QUkfifECucyiVv936NsxrIyhEw4S9KLasENoEVN%2F4Ro1xFkFjyg9q88s%2FDI4p7kZ)

**1. 任意文件删除**

根据网传的 Exploit，可以看到首先调用

```
/module/appbuilder/assets/print.php
```

接口，具体代码如下：  

```
<?php

$s_tmp = __DIR__ . '/../../../../logs/appbuilder/logs';
$s_tmp .= '/' . $_GET['guid'];
if (file_exists($s_tmp)) {
    $arr_data = unserialize(file_get_contents($s_tmp));
    unlink($s_tmp);
    $s_user = $arr_data['user'];
}
```

其实是将传入 guid 的值作为文件删除，当前操作路径为：D:/MYOA/logs/app/appbuilder/logs / 所以想删除 web 文件，需要构造:

```
../../../../webroot/web文件名
```

**2. 任意文件上传**

然后调用了 / general/data_center/utils/upload.php 进行上传，看到代码如下：

```
<?php

include_once 'inc/auth.inc.php';
include_once './utils.func.php';
$HTML_PAGE_TITLE = _('上传文件');
include_once 'inc/header.inc.php';
```

其中 inc/auth.inc.php 用于校验用户是否登录，所以在第一步任意文件删除时，删除了该文件导致未授权 RCE。

接着看代码：

```
<?php
...
if ($action == 'upload') {
    if ($filetype == 'xls') {
        $uploaddir = MYOA_ATTACH_PATH . '/data_center/templates/';
        if (!is_dir(MYOA_ATTACH_PATH . '/data_center/templates')) {
            if (!is_dir(MYOA_ATTACH_PATH . '/data_center')) {
                mkdir(MYOA_ATTACH_PATH . '/data_center');
            }
            mkdir(MYOA_ATTACH_PATH . '/data_center/templates');
        }
        if (move_uploaded_file($_FILES['FILE1']['tmp_name'], $uploaddir . $_FILES['FILE1']['name'])) {
        }
    }
```

当 $action 为 upload 时，且 filetype 为 xls 时，也时可以任意文件上传的。其中 MYOA_ATTACH_PATH 全局变量的值为：D:/MYOA/webroot/attachment / 也在 web 目录下，尝试调用该点进行上传：

![](https://mmbiz.qpic.cn/mmbiz_png/BibfH6dHpibZKc2tNPhTuyDGw5n7IciaEhv8pxIMsBmrCNOfpy5GNOgvuiboQ0RyLrawbdXswHAogv8OUDepEWwg9g/640?wx_fmt=png)

然后到服务器中查看：

![](https://mmbiz.qpic.cn/mmbiz_png/BibfH6dHpibZKc2tNPhTuyDGw5n7IciaEhvtHOS0Ml2Jzlxtoics1L8G7icxdw3DGDfA2JmtmlSI5ZQvgyBI7M7Ywicg/640?wx_fmt=png)

访问 shell：

![](https://mmbiz.qpic.cn/mmbiz_png/BibfH6dHpibZKc2tNPhTuyDGw5n7IciaEhvpb5gxZMWGJ1QFQjjUTszkIxXiaGB6WSog89jBy4IURibTXebQvOqV3SQ/640?wx_fmt=png)

发现 D:/MYOA/webroot/attachment 目录下默认没有执行权限，继续往下看逻辑：

当 filetype 不为 xls 或 img 时会执行以下代码：

```
// 46行开始
if (isset($from_rep)) {
    if ($from_rep != '' && $from_rep[0] == '{') {
        $repkid = GetRepKIDBySendId($from_rep);
        if ($repkid != $to_rep) {
            if (file_exists($uploaddir . '/' . $repkid . '_' . $filename)) {
                copy($uploaddir . '/' . $repkid . '_' . $filename, $uploaddir . '/' . $to_rep . '_' . $filename);
            }
        }
    } else {
        $arr = explode(',', $from_rep);
        for ($i = 0; $i < count($arr); $i++) {
            $p = strpos($arr[$i], '.');
            $repno = substr($arr[$i], 0, $p);
            $repkid = GetRepKIDByNo($repno);
            if ($repkid != $to_rep) {
                if (file_exists($uploaddir . '/' . $repkid . '_' . $filename)) {
                    copy($uploaddir . '/' . $repkid . '_' . $filename, $uploaddir . '/' . $to_rep . '_' . $filename);
                    break;
                }
            }
        }
    }
}
else {
    $s_n = $_FILES['FILE1']['name'];
    if ($s_n[0] != '{') {
        $s_n = $repkid . '_' . $s_n;
    }
    if (move_uploaded_file($_FILES['FILE1']['tmp_name'], $uploaddir . $s_n)) {
    }
}
```

看到当 from_rep 参数不存在时，会进入到另一个可以任意文件上传的 else 语句当中.

我们可以通过控制 $repkid 参数，达到控制文件目录的效果，如：传入 repkid=../../../，则最终的 $s_n 为：../../../_filename

从而达到目录穿越，上传任意文件的效果。

![](https://mmbiz.qpic.cn/mmbiz_png/BibfH6dHpibZKc2tNPhTuyDGw5n7IciaEhvJib2VH1pUscLibzm40OCWYlAa6qINoeZmtpmNRYqN6Yq4kjuxuSY4JPQ/640?wx_fmt=png)

最终 shell 地址为：http://192.168.56.135/_admintony.php

![](https://mmbiz.qpic.cn/mmbiz_png/BibfH6dHpibZKc2tNPhTuyDGw5n7IciaEhv3EEzJ0McVkw3icK0vgSZ0SMXWicRYfSvVkG1HXgrghudjDEDDa5kK7lQ/640?wx_fmt=png)

**3. 影响版本**

仅通达 OA v11.6 版本

**4. 总结**

*   如果不想破坏文件可以在登陆后任意文件上传 getshell
    

*   因为 auth.inc.php 中无网站特殊内容，所以可以使用 exp 删掉后，getshell 以后再上传一个。无 auth.inc.php 时，登录后台如下：
    

![](https://mmbiz.qpic.cn/mmbiz_png/BibfH6dHpibZKc2tNPhTuyDGw5n7IciaEhvOdUMicXg8gjY87WzQ4Nln6xZXs2mqWLfVicHF0WUChwnnnJbhkN9ThtQ/640?wx_fmt=png)