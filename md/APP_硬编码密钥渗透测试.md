\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/FHhF-6kgj2dC7KvtJI0nmg)

![](https://mmbiz.qpic.cn/mmbiz_png/CWibxlhHlwicOVZT5NrsOFictAv7qpgjUySOkmPZibsL50vUyOroiafAicZmk4bBFXuKDQQ2XjGaZ4Ltnq2yAAlY32qQ/640?wx_fmt=png)

背景

![](https://mmbiz.qpic.cn/mmbiz_png/rI84CG7Yg06vmZB90Zj1aCINibewG0S21vncYicgUqQc1X3yGycYK7cCNE4y7lSuTsC8RCzVjNUiat7gtHevbicrLg/640?wx_fmt=png)

接到一个任务，做 app 的测试，使用 postern+charles+burpsuite 抓包，观察到

charles 请求流量中有阿里云开放存储服务（oss）的地址

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAMiaywia4oUzFZumU33QU38sjepSOaAjzKDx9JR0zcTicIlkqVRdUbEhdg/640?wx_fmt=png)

那么 app 中的资源一定用到了阿里云 oss，遂怀疑 app 可能会编码了 oss 的登陆账号和密码，闲话不多说，直接开搞！

![](https://mmbiz.qpic.cn/mmbiz_png/CWibxlhHlwicOVZT5NrsOFictAv7qpgjUySOkmPZibsL50vUyOroiafAicZmk4bBFXuKDQQ2XjGaZ4Ltnq2yAAlY32qQ/640?wx_fmt=png)

正文

![](https://mmbiz.qpic.cn/mmbiz_png/rI84CG7Yg06vmZB90Zj1aCINibewG0S21vncYicgUqQc1X3yGycYK7cCNE4y7lSuTsC8RCzVjNUiat7gtHevbicrLg/640?wx_fmt=png)

把 apk 拖入 jadx 发现 qihoo.util, 用 360 加固了  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaA5ziaDvPUBSDUC0K6qs1lbm9OzHAUVu88CInzLSF9jwXuuQZQRWfCydg/640?wx_fmt=png)

使用 Objection 加载 huluwa 的 dexdump 脱之！

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAUBv9X6x4aWXODu1G06C3VXKveyhHANTjRxK8j4KgYv4iaNdG7fVdugw/640?wx_fmt=png)

使用 grep 查找关键字符串

```
grep -rnl "cn-beijing"
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAcbwgGX5LVmkgDfU2eBIppsTmDyzllPaxp75e09M7nKIhfC9zpP8C2A/640?wx_fmt=png)

定位到 0xc28b2000.dex 文件，拖入 Jadx，继续搜搜字符串 "cn-beijing"

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaACnVc5xqf52NlRvaOQM0EXCsv89KVMpuGYlXRfF2scadeiaxHBp6eClw/640?wx_fmt=png)

如上图，定位到 OSSutils.sign 方法，该登录方法 传入 Accesskeyid 和 AccessKeySecret 用于登录 oss 存储桶，这里发现他传了两个加密的字符串，那

么我们跟进 AESUtils.decrypt(String str) 方法  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAGgEKepfxaZCR2Su9nNhPT2GAsQ6QiaXeD1OzC7LhLtvtvibPdQJnOP2A/640?wx_fmt=png)

又调用了 AESUtilsChat.decrypt(str) 方法，继续跟进：

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaANWibe2LiaX5JJBOZVIugUWt19o44Oib1LFhjUcSDic54OUx1z3fKSnrfcQ/640?wx_fmt=png)

发现调用了 AESUtils.decrypt(1.str)，继续跟进, 我去这是俄罗斯套娃啊。。。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAFUHyGcvC7ayibLF51ZxmdbhHf9ZVLq23ehQCV9fyUc0tedicsAetIuLg/640?wx_fmt=png)

i==1, 发现又调用了 decryptByAes(str)........ 继续跟进去，看看

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAiaKbmToWyTx3xDTxialIjNhicaDnf7drUz3jmXia0ZMbBHBWuPRjrYpqaA/640?wx_fmt=png)

找到了 decryptByAes 方法，又调用了 decryptByAESWithKey 方法，这个方法

的声明就在下面，终于在我不懈努力下找到了加密的方法，我们可以看到这个方法传了 CRYPT_KEY，IV_STRING，str 三个值，CRYPT_KEY 是密码，IV_STRING 是偏移量，str 是要解密的值，AES\_CODE 是加密算法，填充模式，继续查看这几个值是啥

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAdiaX2G1MxuL6E9fOX5s7TG0P4Wtib8WMhAiaiaibaJvZ2oNAqOyAKOVv8JA/640?wx_fmt=png)

ok, 明文的加密值都有了，放到在线解密去解一下

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAnn5epVrAFRhzibAPkzExWlZ91yia3DXt1RAkyxR6osEjfc0SiaUX3vK8g/640?wx_fmt=png)

把两个加密字符串解密之后，我们打开阿里云的官方工具 OSS 文件管理器，填写对应的值，尝试登陆

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaA6IFTPpyjf1Wia8bIp7qmq2YjugwdiavhLknBk8ZwicNnzQjZNQ9vHrQDg/640?wx_fmt=png)

成功~~

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAddI6vf3iayTnUhJhpQ7GXVk7dAXTiaugqfY3rI2ao7OUiaSXBWCBJ1Yhg/640?wx_fmt=png)

ok, 一个密钥硬编码导致阿里云 OSS 账户接管漏洞到手了。

![](https://mmbiz.qpic.cn/mmbiz_png/CWibxlhHlwicOVZT5NrsOFictAv7qpgjUySOkmPZibsL50vUyOroiafAicZmk4bBFXuKDQQ2XjGaZ4Ltnq2yAAlY32qQ/640?wx_fmt=png)

后话

![](https://mmbiz.qpic.cn/mmbiz_png/rI84CG7Yg06vmZB90Zj1aCINibewG0S21vncYicgUqQc1X3yGycYK7cCNE4y7lSuTsC8RCzVjNUiat7gtHevbicrLg/640?wx_fmt=png)

在渗透测试过程中我们要细心观察流量，遇到这种有 endpoint 的都可以尝试看看，app 内有没有存储的密码。或者我们可以直接在 app 里搜 “Accesskeyid”，“aliyuncs” 等字符串也可以发现此类漏洞  

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ib31bYPNTMSLwibxLzaMZJaAmzvhPQxDTrCZmofCicldyJtia5R657l3jUuLv0AeVhg4Nq2kSXOTGjQg/640?wx_fmt=png)