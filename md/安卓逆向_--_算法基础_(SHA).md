> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/D4nzykxjRUN2U32PR0YjGQ)

 ![](http://wx.qlogo.cn/finderhead/PiajxSqBRaEJ7Ik2tcpu1fLbiceIMq8ALz06e9g1ENj06MEeFBG1snVQ/0) **之乎者也吧** #安卓逆向 #算法基础 #SHA 视频号

一、SHA 算法  

SHA 由美国标准与技术研究所（NIST）设计并于 1993 年发表，该版本称为 SHA-0，由于很快被发现存在安全隐患，1995 年发布了 SHA-1。2002 年，NIST 分别发布了 SHA-256、SHA-384、SHA-512，这些算法统称 SHA-2。2008 年又新增了 SHA-224。由于 SHA-1 已经不太安全，目前 SHA-2 各版本已成为主流。

二、常用的 SHA-256 算法

1、SHA-256：32 个字节、64 个字符、256 个 bit

2、使用方式和 MD5 方法一样，只是传入算法名不一样

3、java 版

```
String bs= "逆向有你a";
MessageDigest shasf=MessageDigest.getInstance("SHA-256");//我要用md5算法
shasf.update(bs.getBytes());//我要加密的数据
byte[] ressha = shasf.digest();//给我加密
System.out.println("SHA-256加密（字节）："+Arrays.toString(ressha));
System.out.println("SHA-256加密（字符串）："+bytes2HexString(ressha));
MessageDigest shasf1 = MessageDigest.getInstance("sha-256");
shasf1.update("逆向".getBytes(StandardCharsets.UTF_8));
shasf1.update("有你".getBytes(StandardCharsets.UTF_8));
byte[] ressha1 = shasf1.digest("a".getBytes(StandardCharsets.UTF_8));
System.out.println(bytes2HexString(ressha1));
运行结果：
SHA-256加密（字节）：[-55, 52, -50, 36, -123, 97, 5, 78, -89, -81, -84, -15, -22, 80, 62, -1, -65, -124, -122, -49, -56, -56, 23, -2, 97, 99, -26, 71, 88, -111, 103, -88]
SHA-256加密（字符串）：C934CE248561054EA7AFACF1EA503EFFBF8486CFC8C817FE6163E647589167A8
C934CE248561054EA7AFACF1EA503EFFBF8486CFC8C817FE6163E647589167A8
```

4、JS 版，同样需要 CryptoJS 加密库配合

```
var CryptoJS=module.exports;
function test()
{
    return CryptoJS.SHA256("逆向有你a").toString().toUpperCase();
}
console.log(test());
```

禁止非法，后果自负

欢迎关注公众号：逆向有你

欢迎关注视频号：之乎者也吧

欢迎报名安卓逆向培训，报名微信 (QQ)：335158573

[培训课程内容](https://mp.weixin.qq.com/s?__biz=MzA4MzgzNTU5MA==&mid=2652024585&idx=2&sn=6697b52b0ab62434b086ea94e8bd65c4&scene=21#wechat_redirect)  

![](https://mmbiz.qpic.cn/mmbiz_png/WJRHqUiaud0oYsbdic2mh7FRvahCuFjINliacrYtkQxGbxya8tPYm9bf161Z9ntDkCo5UfSZIm3ngWo872cJk1aGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/WJRHqUiaud0oYsbdic2mh7FRvahCuFjINlC5aMC0qltA8KlHdUwRnNbg8zkDe9QuicAUxPVykTARV4muZ2ABNHb5w/640?wx_fmt=jpeg)