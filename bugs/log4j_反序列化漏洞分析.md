> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/9hkZJZYNYvmX7uKFKl2SzA)

0x00 前言
-------

前段时间在看某个 cms 代码的时候，发现 log4j 组件版本存在漏洞，并且开启了端口，但 web 站点是 nginx 反向代理的，而在外网并没有开放到该端口，所以并没有利用成功。但该漏洞遇到的比较少，就算一些 cms 中 log4j 组件版本存在漏洞，该漏洞需要使用`SimpleSocketServer`开启端口才能够接受 socket 中的数据进行反序列化操作，从而才能利用。

0x01 log4j 漏洞简介
---------------

### 漏洞简介

log4j 用的其实还是比较多，记录一些 Java 的日志，这个相信接触过 Java 的都知道，在此不做多的赘诉。

**漏洞版本：CVE-2019-17571**

```
1.2.4 <= Apache Log4j <= 1.2.17
```

漏洞原因是因为调用`SimpleSocketServer.main`开启一个端口，进行接受数据，进行反序列化操作。

根据官方描述作用是把接受到的`LoggingEvent`作为本地的日志记录事件，再使用在服务器端配置的 Log4J 环境来记录日志。默认可能会开启在 4560 端口中。

0x02 log4j 反序列化分析
-----------------

### 漏洞复现

配置漏洞代码

```
import org.apache.log4j.net.SimpleSocketServer;
public class log4j {
   public static void main(String[] args) {
       System.out.println("INFO: Log4j Listening on port 1234");
       String[] arguments = {"1234", (new log4j()).getClass().getClassLoader().getResource("log4j.properties").getPath()};
       SimpleSocketServer.main(arguments);
       System.out.println("INFO: Log4j output successfuly.");
  }
}
```

配置 log4j 文件

```
log4j.rootCategory=DEBUG,stdout
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.threshold=DEBUG
log4j.appender.stdout.layout.ConversionPattern=[%d{yyy-MM-dd HH:mm:ss,SSS}]-[%p]-[MSG!:%m]-[%c\:%L]%n
```

然后使用 yso 生成 gadget 的序列化数据，直接使用 nc 进行发送。但是 nc 发送传输有时候会有些问题，有时候传输数据缺失，会反序列化失败。

```
nc 127.0.0.1 1234 < log4j.curl.bin
```

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar26T7Vhcr3UVWicUgkzgxbs1km42KTKTwO3XmSLFLQfBvMCHJKtX1LRpw/640?wx_fmt=png)

### 漏洞分析

漏洞比较简单，还是现在漏洞位置先下断点。

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2K0dJgHWjYTUPLbx3nl8uWibOcWSJ0qkObsPevZkLl79edUAGIW84Emg/640?wx_fmt=png)

跟进查看  

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2w5FpLicARkqPm3YqQT5k7nTfjFTXOF7pcQMBiboK6fEoLfywHNccRnSg/640?wx_fmt=png)

在这里开启`serverSocket`进行监听，也就是 socket 的服务端，然后 new 了`SocketNode`进行传入。  

继续跟进

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2VcbevJCsfW95sVp0YlbV9uBo0wvlaY4MqJP1v8A6LrqMlakFTV4sOw/640?wx_fmt=png)

而在这里接受了 socket 的数据。  

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2KwjSIYIC8M2hw1ibLm15dMEWLW8ha45jk9u3NcoSSOpqTc6BENYHLAg/640?wx_fmt=png)

下一步会来到 run 的这个方法里面，是因为前面调用了线程的 start，而 start 的底层会调用 run

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2AzDIld9tGsp1OdSAZlBL1r48cI8rGiash84GHHLjtw7FlQ9K8RvYfug/640?wx_fmt=png)

直接就对`ois`也就是刚刚接受的 socket 数据，调用 readobject 进行反序列化。  

0x03 工具编写
---------

在复现的时候，使用 nc 发送数据时数据传输不完整，导致反序列化失败。就随手写了一个小工具，方便下次遇到的时候使用（可能也极少能遇到，比较鸡肋）

命令执行：

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2EZicwdDMfp0kDZbRN61ZcFZglNTVc3a6qyCFz3FQHHw4Vrvcaj9ZkFw/640?wx_fmt=png)

反弹 shell：  

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2NAicPZSK2OLUO5rbhUytRv4cKibt2OQCdyMojOKUxxKib3EPiaDiaddPLicA/640?wx_fmt=png)

POC:

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2XruPr4icPfZUUmg6XibqygiaCmeU76CSUMFqpvwrRWoKPLJDW0NK9rbBA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar2VMoCeryxGMibs5IoasWx2m7YpbZlAohKComW8RXgLtJbq0iaY8bqMnCA/640?wx_fmt=png)

由于比较少见，反序列化回显暂不构造。  

github 地址：https://github.com/nice0e3/log4j_POC

**动动小手点点 start**

0x04 结尾
-------

log4j 的反序列化漏洞比较简单，而类似于这种反序列化工具原理其实差不多，只是发包构造的数据包不一样，分析一下漏洞知道漏洞怎么形成的。原理其实比较简单，但也会遇到很多细节问题，如回显方式，或 gui 的优化问题。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qr5uyVXdEvfdvaAb7uDyhUQ5L3vKcar24PwV5icSTN4TCC9SEctCUlTaC4kHbGdNOBJLiax2LK76ghdsHy0nNneQ/640?wx_fmt=jpeg)