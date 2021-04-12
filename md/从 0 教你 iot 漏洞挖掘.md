> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/CrbdyIHUWdd0fX-Q5Eckvg)

**1. 环境搭建**  

系统：Ubuntu18.04

固件：DIR822A1_FW103WWb03.bin

使用用 firmadyne 工具运行固件

注意：Firmadyne 安装之前，先安装 firmware-analysis-toolkit

*   由于过程比较复杂而且中间有错就会导致最后的失败。所以这里我把安装过程所需要的命令给 大家总结了一下：
    

```
git clone https://github.com/attify/firmware-analysis-toolkit 
cd firmware-analysis-toolkit
./setup.sh
```

"./setup.sh" 这个过程比较吃网络，如果网络慢的同学可以出门抽个烟、喝个酒、吃个火 锅再回来。

*   接着找到 fat.config 文件后修改 root 密码
    

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTYviaw4eiacSskLvagqbTWTfSLY28TsS6TfaKKIKRD5MOyzwhjwQduWicg/640?wx_fmt=png)

*   接着安装依赖  
    

```
sudo apt-get install busybox-static fakeroot git dmsetup kpartx netcat-openbsd nmap python-psycopg2 python3-psycopg2 snmp uml-utilities util-linux vlan
```

*   将固件拷贝到 firmadyne 文件夹下  
    

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTIKJibHbQNBVo9iaDYXlb2UnMxM2BWLrDGtltQsfutibiazmOhgKPeeHEnQ/640?wx_fmt=png)

*   重置文件
    

```
rm -rf images* 
python3 reset.py
```

*   安装配置数据库（由于我这里存在 firware，所以 database 提示存在）
    

```
sudo apt-get install postgresql 
sudo -u postgres createuser -P firmadyne 
sudo -u postgres createdb -O firmadyne firmware 
sudo -u postgres psql -d firmware < ./firmadyne/database/schema
```

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbT1YRy9CibAOU5P7AB3iaSGFSdfMOmLL35RXOxN2LlbDNbEPDhbmhfYv8g/640?wx_fmt=png)

*   对模拟环境进行配置
    

```
/sources/extractor/extractor.py -b Dlink -sql 127.0.0.1 -np-nk "DIR822A1_FW1 
./scripts/getArch.sh ./images/1.tar.gz 
./scripts/makeImage.sh 1 mipseb 
./scripts/inferNetwork.sh 1 mipseb 
./scratch/1/run.sh
```

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTWea1UEG920cLPCIM9tmRlbXF1VtjiaNRF7UicUkyrj4sTuK6M22N9T8w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTY5b93mCuzIaz5vxdic5Vibtaiat1Fp9tWialSlSER3uibjq8n6qMXSNTtMg/640?wx_fmt=png)

*   最后打开浏览器输入 ip 即可访问
    

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTAuXOLpvNeG5WfHfOEQ8r1ZjkzhNNhcxCcMtrdCczRmhtic0vk8FcJTg/640?wx_fmt=png)

**2. 漏洞分析**
===========

*   genacgi_main 函数是漏洞开始的触发点，通过 getenv 函数获取 “REQUEST_URI” 环境变量的内容，接着对其进行验证，最后进入 sub_40FCE0。
    

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTQ2QlYRiaPT7iaTOJkQXDFPUfbpnAqzKoniaDqnOLlAvoaLYaWJbzHohPg/640?wx_fmt=png)

*   下图是 sub_40FCE0 函数的内容，在上图中获得的值，最终通过 xmldbc_ephp 函数发送出 去，数据由 run.NOTIFY.php 进行处理。
    

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTYQOzvDefria87LpMXGMRC1EgRsxNOCBn8JJicugPF1b9QqZyLribXc5KQ/640?wx_fmt=png)

*   该 php 调用了 GENA_subscribe_new 函数，并且向里面传递了 cgibin 中获取到的数据，还 传递了 SHELL_FILE 参数。
    

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTlVDYy2IYt2RfY66ickT0USrZCqxgiaPCsicaBDZ4TdS3lXPCdAcibFiadeg/640?wx_fmt=png)

*   文件 gena.php 中是函数 GENA_subscribe_new 的实现代码。从代码中我们可以看到该函数并未对 shell_file 数据进行操作。但是在最后调用了 GENA_notify_init 函数传入了 shell_file。接下来在该文件下找到 GENA_notify_init 函。
    

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTIRZicXwDsCH3jKqWLvj1EZfwSHIicQHj6tfN0B5V1tI38SyckZJz34yQ/640?wx_fmt=png)

*   接下来在该文件下找到 GENA_notify_init 函数 第一次调用 fwrite 的时候创建了文件， 第二次调用 fwrite 的时候使用了 "rm -f" 命令。
    

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTgoJEeYlDF9vee7SZacxiaoOQpfvHdDZxJTLgpCDcFDFoHtnndibfu4xw/640?wx_fmt=png)

到此为止我们的攻击思路大致已经出来了。我们只需要插入一个反引号包裹的系统命 令，然后注入到 shell 脚本中即可。  

**3. 漏洞验证**

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbTEaSU6wjkrWyiaaCptwKSNrcoLAF48exAR10sb3BY3fiaoEs6TtI3xgew/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/PrTu58FA79ZZFtibn4ibyVglsNsVU9IqbT83ePt5A9Zk2zW8nVeEOgNPB2505DDdlGcwqUIGEI7VbJ2HHc8OUHJQ/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_jpg/PrTu58FA79bYUuGICO85hGrTyicvB3nMAtd7QY3C0H3CA2SOwaiaSkDbazCO8C1VXHx8ticGRxDeVATd9LZf62z4w/640?wx_fmt=jpeg)