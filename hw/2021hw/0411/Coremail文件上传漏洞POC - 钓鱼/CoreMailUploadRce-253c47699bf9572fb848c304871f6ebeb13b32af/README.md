# README
Coremail文件上传漏洞POC
-----------------

Coremail产品诞生于1999年，经过二十多年发展，如今从亿万级别的运营系统，到几万人的大型企业，都有了Coremail的客户。截止2020年，Coremail邮件系统产品在国内已拥有10亿终端用户，是目前国内拥有邮箱使用用户最多的邮件系统。其特定版本范围内存在任意文件上传漏洞，攻击者可以上传webshell，从而造成远程代码执行。

安装
--

    pip3 install -r requirements.txt

工具利用
----

    python3 coremail_upload.py -u http://127.0.0.1:1111 单个url测试
    python3 coremail_upload.py -f url.txt 批量检测

免责声明
----

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，作者不为此承担任何责任。