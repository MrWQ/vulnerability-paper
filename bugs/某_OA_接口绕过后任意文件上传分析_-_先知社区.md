> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9581)

> 先知社区，先知安全技术社区

最近公开了某 OA 的任意文件上传 POC，想着来分析一下，下面截图代码为 github 找到。  
上传漏洞的利用接口如下所示：

```
/weaver/weaver.common.Ctrl/.css?arg0=com.cloudstore.api.service.Service_CheckApp&arg1=validateApp
```

看 POC 注意到接口后面多了一个`.css`, 根据以往的经验应该是用于权限认证绕过。抓包进行验证结果如下所示：

当接口后面跟`.css`, 请求返回状态码为 200，如下所示：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517192742-e4ea8ca2-b702-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517192742-e4ea8ca2-b702-1.png)  
当接口后面不跟`.css`时，返回状态码为 403，如下所示：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517192816-f91ada10-b702-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517192816-f91ada10-b702-1.png)  
由此可以判断`.css`是用于权限绕过。接下来通过 POC 入口逆向来分析该漏洞成因。

翻阅资料知道该系统写了全局安全防护规则，当用户请求触发相应防护规则时会记录触发规则及 IP 等信息。查看日志发现触发了该条规则`weaver.security.rules.SecurityRuleQX20`  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517192857-11d77658-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517192857-11d77658-b703-1.png)  
该规则防护源码如下所示：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517192918-1e364b04-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517192918-1e364b04-b703-1.png)  
当请求 URL 中包含字符`weaver`，`common` ,`ctrl`等字符时就会触发该条防护规则。这时就又有一个疑惑。绕过访问控制的 POC`/weaver/weaver.common.Ctrl/.css`中不是同样存在这些字符嘛为啥没有触发该规则。根据经验判断可能是该系统的全局过滤器在处理 URL 后缀为`.css`时，进行了白名单验证放过，不进入防护规则判断。  
查看`web.xml`文件中的安全防护规则`filter`入口为`weaver.filter.SecurityFilter`, 匹配过滤全局路径，如下所示：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517192957-3594732a-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517192957-3594732a-b703-1.png)  
`weaver.filter.SecurityFilter`源代码中的`initFilterBean`函数用于初始化系统防火墙即加载所有防护规则:  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193025-4621dd72-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193025-4621dd72-b703-1.png)  
跟入`weaver.security.filter.SecurityMain`的`initFilterBean`函数启动并导入所有规则类：[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193050-54e98134-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193050-54e98134-b703-1.png)  
`weaver.filter.SecurityFilter`中初始化系统防火墙后之后进行`doFilterInternal`用于过滤校验前端传入数据是否满足安全要求：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193114-63a83544-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193114-63a83544-b703-1.png)  
请求数据及 FilterChain 传入`weaver.security.filter.SecurityMain`的`process`函数继续跟入，idea 反编译失败 wtf：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193144-758b4eb8-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193144-758b4eb8-b703-1.png)  
使用 JD 进行反编译发现如下所示代码：

```
Object localObject7 = str2.toLowerCase().trim();          
if ((((String)localObject7).endsWith(".cur")) || (((String)localObject7).endsWith(".ico")) || (((String)localObject7).endsWith(".css")) || (((String)localObject7).endsWith(".png")) || (((String)localObject7).endsWith(".jpg")) || (((String)localObject7).endsWith(".gif")))
          {
            if (!localSecurityCore.null2String(localSecurityCore.getRule().get("OA-Server")).equals("")) {
              localHttpServletResponse.addHeader("Server", localSecurityCore.null2String(localSecurityCore.getRule().get("OA-Server")));
            }
            localSecurityCore.addHeader(localHttpServletRequest, localHttpServletResponse);
            paramFilterChain.doFilter(paramHttpServletRequest, paramHttpServletResponse);


```

`str2`为获取的请求 URL，故上述代码为 URL 后缀为`cur、ico、css、png、jpg、gif`时即可条过该 filter 链校验即不用进行上述 weaver.security.rules.SecurityRuleQX20 的校验，之后跟进调用`paramFilterChain.doFilter`进入下一条`filter链`：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193213-866ae644-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193213-866ae644-b703-1.png)  
将`POC`中的绕过`.css`换成`.cur`发现同样绕过访问限制，如下所示：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193233-9281176e-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193233-9281176e-b703-1.png)  
`web.xml`之后的 filter 并未对器防护过滤故直接进入最终的`resource`处即`weaver.common.Ctrl`方法：  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193255-9f56c632-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193255-9f56c632-b703-1.png)  
前台传入`arg0`，`arg1`参数，并调用`doInvoke`以`arg0`参数为类对象，`arg1`参数为相应类的方法。跟进 POC 中的`arg0=com.cloudstore.api.service.Service_CheckApp&arg1=validateApp`, 获取前端数据流导入 zip 压缩包再进行文件解压：

**validateApp 函数**  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193318-ad2c69d8-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193318-ad2c69d8-b703-1.png)  
**createLocalApp 函数**  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193337-b8e08264-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193337-b8e08264-b703-1.png)  
**decompress 函数**  
[![](https://xzfile.aliyuncs.com/media/upload/picture/20210517193357-c4a3f252-b703-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210517193357-c4a3f252-b703-1.png)  
由上利用链最终造成绕过权限访问造成任意文件上传。