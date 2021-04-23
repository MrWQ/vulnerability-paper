# Coremail 邮箱系统路径穿越漏洞
在蓝队游啊游的时候，微信群里有老哥发了一张截图，内容说coremail邮箱系统漏洞攻击事件，这就让我这本身困意慢慢顿时充满精神。

![](Coremail%20%E9%82%AE%E7%AE%B1%E7%B3%BB%E7%BB%9F%E8%B7%AF%E5%BE%84%E7%A9%BF%E8%B6%8A%E6%BC%8F%E6%B4%9E/640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.dat)

利用方法都在上面了，那就找随便找个资产试试(不能确定百分百成功嗷，成功几率咱也不知道)。

url:xxxxxxx   

![](Coremail%20%E9%82%AE%E7%AE%B1%E7%B3%BB%E7%BB%9F%E8%B7%AF%E5%BE%84%E7%A9%BF%E8%B6%8A%E6%BC%8F%E6%B4%9E/1_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.dat)

    `url+/lunkr/cache/;/;/../../manager.html`

![](Coremail%20%E9%82%AE%E7%AE%B1%E7%B3%BB%E7%BB%9F%E8%B7%AF%E5%BE%84%E7%A9%BF%E8%B6%8A%E6%BC%8F%E6%B4%9E/640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

访问过去会直接跳转到tomcat控制台，这里你就可以采用coremail/coremail弱口令尝试登陆，或者暴力破解。然后就是部署war包Getshell就ok了。(小鸡肋)

修复建议：对外隐藏tomcat控制台，修改默认口令。

 附一张成功的图：

![](Coremail%20%E9%82%AE%E7%AE%B1%E7%B3%BB%E7%BB%9F%E8%B7%AF%E5%BE%84%E7%A9%BF%E8%B6%8A%E6%BC%8F%E6%B4%9E/1_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

（fofa收集资产的收获百分之80资产都打不开了，别尝试了！）

\-END-