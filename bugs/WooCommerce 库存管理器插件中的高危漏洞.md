> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/60cG_ySte890v09ItNPRAg)

![](https://mmbiz.qpic.cn/mmbiz_png/OhKLyqyFoP9mJwX65uY3o0wwuMo2eWPeFuDIhxJlAjMcIicKFSYLVZ6fjicY0dNle24gfmiaVpwCcP2PeZuZyaRzw/640?wx_fmt=png)点击上方蓝字关注我们

概述


------

WooCommerce 库存管理器插件是一个 WooCommerce 扩展程序，该插件使网站所有者能够在一个页面上集中管理所有电子商务网站产品的库存和详细信息。该插件的功能之一是能够导出所有产品并导入新产品。

2021 年 5 月 21 日，Wordfence 安全团队发现 WooCommerce 库存管理器插件中存在漏洞，漏洞编号为 CVE-2021-34619，CVSS 评分为 8.8。该漏洞使攻击者可以将任意文件上传到易受攻击的站点，并实现远程代码执行。攻击者只需诱使站点管理员执行诸如单击链接之类的操作即可触发漏洞。

漏洞细节


--------

经过检查发现，该漏洞是由于插件没有正确检查导入造成的。由于插件中缺少对请求来源的验证，使得攻击者可以通过特制的上传请求，诱使网站管理员点击链接，触发漏洞，从而导致网站被入侵，同时对易受攻击的站点进行身份验证。

```
<form method="post" action="" class="setting-form" enctype="multipart/form-data"> 
    <table class="table-bordered">
      <tr>
        <th><?php _e('Upload csv file', 'woocommerce-stock-manager'); ?></th>
        <td>
          <input type="file" >
        </td>
      </tr>
    </table>
    <div class="clear"></div>
  <input type="hidden"  />
  <input type="submit" class="btn btn-info" value="<?php _e('Upload', 'woocommerce-stock-manager'); ?>" />
</form>  
<?php
if(isset($_POST['upload'])){
 
    $target_dir = STOCKDIR.'admin/views/upload/';
    $target_dir = $target_dir . basename( $_FILES["uploadFile"]["name"]);
    $uploadOk   = true;
 
    if (move_uploaded_file($_FILES["uploadFile"]["tmp_name"], $target_dir)) {
 
        echo __('The file '. basename( $_FILES['uploadFile']['name']). ' has been uploaded.','woocommerce-stock-manager');
 
        $row = 1;
        if (($handle = fopen($target_dir, "r")) !== FALSE) {
 
            while (($data = fgetcsv($handle, 1000, ',')) !== FALSE) {
                $num = count($data);
```

此外没有对上传进行验证，以确认它是 CSV 文件，或者至少不是恶意文件。这意味着任意文件类型都可以上传到站点，包括但不限于可用于获取远程代码执行的 PHP 文件。

成功利用此漏洞的攻击者，可以通过使用远程命令将 PHP webshell 上传到站点，从而完全接管易受攻击的 WordPress 网站。

为避免遭受跨站请求伪造攻击，网站所有者在点击来自未知来源的链接或附件时，应保持谨慎，即使这些链接位于自身站点的评论或表单提交中。

总结


------

本文中，披露了 WooCommerce 产品管理器中的一个漏洞，攻击者可以通过诱使站点管理员执行某个操作来触发该漏洞，该漏洞使攻击能够上传恶意文件以实现远程代码执行。该漏洞现已在 2.6.0 版中被修复，建议受影响的用户立即更新到最新版本。

![](https://mmbiz.qpic.cn/mmbiz_png/RQoDdorCu0V5znWFiaMBVWiaibdvAvmGeUvfC5LJ60x1Kq5wiaQ5UtMKEDcwQJ3ibicBdGBKxGs1V2AuZcg3ISoDto1g/640?wx_fmt=png)

  

END

  

![](https://mmbiz.qpic.cn/mmbiz_png/DQk5QiaQiciakarCFnYafgYGpNRiaX2oibtiawYX92ytrKp9MpmQeOqARcreRBybBX1fDbv2guZxExicn7f0wn2dkVwqw/640?wx_fmt=png)

好文！必须在看