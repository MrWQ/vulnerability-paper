> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/j3RECd7W1nLymhJJZVxoHQ)

> 本文作者：****掉到鱼缸里的猫****（Ms08067 内网安全小组成员）

掉到鱼缸里的猫微信（欢迎骚扰交流）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1HGZh34ibLF8iaiaI5cQEPLgibMocOiaZc0VkvztzB0XKX3UJiaFJw5sHWKHg/640?wx_fmt=jpeg)  

**说明**：本文仅在 Windows Server 2016 R2 上进行测试，不保证其他版本环境下结果一致。  

**Windows 域关系学习**  

1. 基本概念

2. 林中的信任关系  

*   2.1 父子域
    
*   2.2 林中树之间
    

3. 不同林中的信任关系  

*   3.1 外部信任
    

*   3.1.1 两个林根域之间
    

        单向外传信任  

        单向内传信任

*   3.1.2 外部域和子域之间
    
*   3.1.3 外部域与林中树
    

4. 林信任

5. 总结

6. 在其他主机中使用 dsquery

**1. 基本概念**

    1. **域**是 Windows 网络操作系统的安全边界，域内主机各种策略由域控制器统一设定，域中所有主机共享一个集中式的**目录数据库**，包含着整个域内的对象。父域和子域之间构成**域树**，多个域树构成**域林**，林中的第一个被创建的域，作为该林的根域。Windows NT 中，名称空间是平行的，尽管可以将 NT 域配置为彼此信任，但每个域都是一个完全独立的实体。  

    目录林根级域包含 Enterprise Admins 和 Schema Admins 组。这些服务管理员组用于管理林级操作，例如添加和删除域以及实现架构更改。  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1iaj0xLtHqDGSia8Kbl68jXOQ0ZIdf2kq2dwwibKI7pRotCzSEcJTfldDg/640?wx_fmt=png)

**2. 信任方向：**  

1.  **内传**（内向信任，Direct Inbound）：信任此域的域，这个域（当前域）中的用户，可以在指定域、领域或林中得到身份验证。  
    
2.  **外传**（外向信任，Direct Outbound）：受此域信任的域，指定的域、领域或林中的用户可以在这个域中得到身份验证。  
    
3.  **双向**：内传 + 外传
    

3. **信任传递**：企业内部来自间接信任域的用户可以在信任域中进行身份验证。  

4. **信任类型**：

1.  **外部信任**：林外部的两个域之间的**不可传递的**信任。
    
2.  **林信任**：两个林之间的可传递信任，允许一个林中的任何域中用户在另一个林中的任何域收到身份验证。只有**林的根域**之间才可以使用这个选项。
    

5. **身份验证级别**：

1.  **全域性身份验证**：windows 将自动对指定域用户使用本地域的所有资源进行身份验证，在默 认情况下可以进行 IPC 连接。
    
2.  **选择性身份验证**：windows 将不会自动对指定域的用户使用本地域的任何资源进行身份验证，需要由管理员向指定域用户授予每个服务器的访问权。
    

这样一来，域之间的相互信任关系就可以大致分为三类：林中父子域、林中树和树、不同林的域之间的信任关系。  

**2. 林中的信任关系**

**2.1 父子域**

实验环境：

    **dc1**：创建域 lab1.local ，作为父域，同时也是该林的根。

   **dc2**：作为子域 sub.lab1.local 加入父域 lab1.local

*   加入域之前，dc2 是无法查询到域中的任何信息
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1a2jyQ0pmjrXRwz846lgowxmFwI1p8TAzjvtrHqsuSJe94VVpHPWnNg/640?wx_fmt=png)  

*   加入域（查询目标域，可以使用域用户，但是加入域的时候需要使用**域管理员用户**的凭据）
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1pzayWR64mZh5LSqBCgTPIzhqUJVx8ED4SZqQJw3YuBDPZMOmQLDIibQ/640?wx_fmt=png)  
    
*   加入域之后可以查询到信任关系如下：  
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1JRBRMEYe1pIhqXWicdNI9w4tD7iaj6IhMGfc2O9ss6Y2Mw6PTw5H5FYQ/640?wx_fmt=png)

*   可以查询另外的域中的信息，并且两个域之间的身份凭据是相互认可的。  
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1cLxrYb4vib3LiaNeiabiaCMZnkwpAX1IWwMictia9JWLcBDZmZM6EfICA4Vw/640?wx_fmt=png)

*   但是在没有分配权限时，是没有权限访问远程目录的；同时父域用户因为未在子域中登记，所以无法通过认证。
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1ZUGmFxdliakRt3py2R4wCU6cbkNCaPeu9tz5bu9QhCWA1ib4djCMGuQw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1ibd8HuDRDWebtMlyzYP70eNm8Wic4aQmeSzlD3DLO4rUTs6mvPrmxMwA/640?wx_fmt=png)

但是父域的**域管用户**可以访问子域的资源，而子域的**域管用户**没有父域的权限。  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1HPmrWeictOwTCMvQcgiaqVEQv9gLRZzL2XrWQ6aT9eyKdRycrb0BibUcA/640?wx_fmt=png)

**2.2 林中树之间**

*   实验环境：
    

    **dc1**：创建域 lab1.local

    **dc2**：作为子域 sub.lab1.local 加入父域 lab1.local

    **dc3**：作为林中的另一个树 lab3.local

*   信任情况如下：可以看到， lab1.local 和 lab3.local 之间存在双向信任，但是 lab3.local 和 sub.lab1.local 之间没有方向记录。
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1YicUCn4eWTDqGYYD2Gqsu3bJm6jsiaSsnB84ziciaRVicqyxcmljDL9kulg/640?wx_fmt=png)
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1nianYOJQsD3NeBmvHFUlxF7XiajsfwDtTQeCr90lF83v8W1EhDp33tjw/640?wx_fmt=png)

*   此时 lab3.local 域中用户可以查询同林 lab1.local 以及其子域 sub.lab1.local 的信息，用户凭据也可得到认证。  
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1LVeZvmV1R0JJrjYWJP5JsFUIUjPvlP9U6WUIyYNia4Vgicuwic6bn5RNQ/640?wx_fmt=png)

*   此时**林根的域管用户**可以访问 lab3.local 的资源，但是 lab3.local 的域管用户没有其他资源的权限。
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1ogKYd9sTPJD82eAyuN8aTd2C02Ih3wu3O5DNibRXYLtctjj4L8oVAWQ/640?wx_fmt=png)
    
*   查询林根域的方法：
    

1. powershell：

```
Get-ADRootDSE|select rootDomainNamingContext
```

2. vbs：

```
Set objRootDSE = GetObject("LDAP://RootDSE")
Wscript.Echo "Root Domain: " &
objRootDSE.Get("RootDomainNamingContext")
```

**3. 不同林中的信任关系**

*   实验环境：
    

    **dc1**：创建域 lab1.local

    **dc2**：创建子域 sub.lab1.local

    **dc3**：创建域树 lab3.local

    **dc4**：创建域 lab4.local

**3.1 外部信任**

**3.1.1 两个林根域之间**

**单向外传信任**

使用全域性身份验证时，信任查询如下：对于 lab4 是传出，则对于 lab1 就是传入。  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1QEJfB97ab5TH3atBrF6G6kbwXgSfKsWerYfYy9IwoCvia5QZahM0ukg/640?wx_fmt=png)

lab1 的用户身份在 lab4 中可以得到有效认证，但是在未授权的情况下无法访问资源：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1Agpauz00kibVAu5iatb0YnpSuoicVsVLbM0hZygHFhfIAmKUJ0XdatY3w/640?wx_fmt=png)

而子域 sub.lab1.local 和同林树域 lab3 中的用户无法在 lab4 中得到认证。  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1IpUL6jGMftkVPaFzCiboAywT4Kx2KHAHGxzoIrv2dwheuuqiaMEjMb2Q/640?wx_fmt=png)

使用选择性身份认证时，当不进行任何配置时，lab1 的用户无法通过 lab4 的认证：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1ejgZjeuicDpA8Qm2cDRKcS5Vp84ibtuDfRkgFOIiat3uso4m2Mtt0U5icA/640?wx_fmt=png)

**单向内传信任**

信任关系查询  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1TaK1b2XgY2yRwwuP8rxwEEWicd736FqvnnLxaSF7iajlfibpVhodgDLeQ/640?wx_fmt=png)

选择性身份验证时，lab4 的用户无法进行身份验证。  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1Bv1tYRJZz8LicEJ0SianCdlyBOK96Niap4ckafj43zhnZGsOcFszdHOFA/640?wx_fmt=png)

修改为全域认证后，可以访问 lab1 ，但是无法访问子域和同林域。  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1z9S1w2Gg39iaX6lsKdoaIQ3AkhWqYyLlgervWoH8CL4R1eg8ZQ3CpgQ/640?wx_fmt=png)

**3.1.2 外部域和子域之间**

**单向外传信任时**，信任关系查询结果：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia17VleFwQW5sC8iauZq5jLFIXEVhA0CicV8pAxwbDk2Ut8g8jHib9SfekdA/640?wx_fmt=png)

这里虽然通过命令无法查询到，但是直接查看子域的信任关系属性，是可以看到的：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1KzfWibJNkkZmoLeVJDwNm4f1mgr4dGe5o2VWtibHpSSBkOSsWlfXKEDg/640?wx_fmt=png)

仅 lab4 可以查询 sub ， lab1 、 lab3 均无法查询：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1VgU6hicKS9l9Fr6y4ibyKUvy0cJUOfqJqOnN4dyDhGon3yLH0iaZCuFNg/640?wx_fmt=png)

**修改为双向之后**，仅 sub 、 lab4 之间可以互相认证， lab3 、 lab1 与 lab4 之间均无法查询：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1JyTLPEh2jglFwkLar9ffm4COdzDBFtofML7YibZwWjQPwNv2vP4hlAA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1TUODEJW8h4a2R7PDtt3ok7zzq6EibQ6p25mmicqQn7UbibicVzmrujsupg/640?wx_fmt=png)

**3.1.3 外部域与林中树**

仅在 lab3 和 lab4 之间可以查询到信任关系，同样通过可视化工具可以在其他域控（比如 dc2 ）上查询到 lab3 和 lab4 之间的信任记录，此时， lab3 和 lab4 之间可以完成用户的认证， lab1 、 sub 与 lab4 之间无法完成。  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1Hic8dxDSkHvhIM0Kgia1cIaXmr0HI5sBBpChnc2J5BIrfjaawUNSJjxQ/640?wx_fmt=png)

**4. 林信任**

**林根域和其他林的子域、树根域之间只能外部信任**

添加林之间的信任时会提示目标林中的其他名称后缀情况：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1ylzYr4Y918XsLVvPlJeEWnrzVSB0HjzxZb1FibEwVdHLp4icr2iayLvwQ/640?wx_fmt=png)

添加双向信任后：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1TNeBcgNxTjGjnvg4XIembWAsP0BHypFic0PNIMviaSqkgKXhvYVVQSSw/640?wx_fmt=png)  

添加信任后，两个林之间所有的域用户身份都可以在其他域中得到认证：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1Osd8H3938ibTtlqsicy4xHicIiaMMnqp1IOSNtC2foz8QJ6RI30Io6qGvw/640?wx_fmt=png)

**5. 总结**

**默认配置下：**

1. **父域和子域之间**：自动产生可传递的双向信任关系，两个域之间的身份凭据相互认可，同时父域管理员可以访问子域资源，反之不行。

2. **林中的树之间**：树根之间自动产生双向可传递信任关系，另一个域树的子域也会显示出来（但是不 会显示信任传递方向），任意域的用户在其他域中都可以得到认证，仅**林根域**管理员具有其他同林 域资源的访问权限。

3. **外部信任**：只能访问**参与配置**的域的信息（也就是 nltest 中有显示的域），无法获取到林中其他域的信息。

4. **林信任**：任意域之间的用户都能得到认证。  

_**林根域之间的外部信任和林信任的区别：**_

*   林信任下，另一个根域的信任信息中会标记 Attr: 0x8；
    
*   外部信任则是 Attr: quarantined
    

5. 外传、内传是站在命令执行者角度观察；只有参与配置的两个域之间可以通过 nltest 命令查询到另一方。

dsquery 和 net use 在不同情形下的提示：  

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1vvsffFDjjUaDiae8ApaNK2JkQkMBfdicMAzGtTTcAEsYXibz2oxywdKvg/640?wx_fmt=png)

**6. 在其他主机中使用 dsquery**

在其他主机上无法使用 dsquery，因为没有这个程序 这不是废话

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1aXVCk9UJK1aerVcAdJX4Vp6NVnp7QsGZBaVViaQKXdtyQVEfhIcDkzw/640?wx_fmt=png)

以 win10 为例，将 2016 的文件拷出

dsquery.exe.mui 放入：C:\Windows\zh-CN

dsquery.exe 放入：C:\Windows\System32

使用 PTH 可以进行查询

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1yO53JfsITk01oJgmXJoRmRoLOHoVnBRiaF0azanhZ1rbU9Yf6cxc8uA/640?wx_fmt=png)

但是 IPC 不行

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaibld24IhPCibn1E7iapRtiaaia1W7icEmSJOdw7x0h3mndr4IUXiaDFEkRZdquxxmqGTR3PZowkpicBHHTGg/640?wx_fmt=png)

**学习更多文章，****加入内网小组，扫描二维码！**

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cRey7icGjpsvppvqqhcYo6RXAqJcUwZy3EfeNOkMRS37m0r44MWYIYmg/640?wx_fmt=png)

**扫描二维码学习各类安全技术，邀请进入内部微信群！**

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cniaUZzJeYAibE3v2VnNlhyC6fSTgtW94Pz51p0TSUl3AtZw0L1bDaAKw/640?wx_fmt=png) ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cT2rJYbRzsO9Q3J9rSltBVzts0O7USfFR8iaFOBwKdibX3hZiadoLRJIibA/640?wx_fmt=png)

 ![](https://mmbiz.qpic.cn/mmbiz_jpg/XWPpvP3nWaicjovru6mibAFRpVqK7ApHAwiaEGVqXtvB1YQahibp6eTIiaiap2SZPer1QXsKbNUNbnRbiaR4djJibmXAfQ/640?wx_fmt=jpeg)![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicJ39cBtzvcja8GibNMw6y6Amq7es7u8A8UcVds7Mpib8Tzu753K7IZ1WdZ66fDianO2evbG0lEAlJkg/640?wx_fmt=png)

**目前 30000 + 人已关注加入我们**  

![](https://mmbiz.qpic.cn/mmbiz_gif/XWPpvP3nWa9FwrfJTzPRIyROZ2xwWyk6xuUY59uvYPCLokCc6iarKrkOWlEibeRI9DpFmlyNqA2OEuQhyaeYXzrw/640?wx_fmt=gif)