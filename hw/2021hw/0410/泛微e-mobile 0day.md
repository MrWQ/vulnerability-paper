# 泛微e-mobile 0day
mp.test.com:89 系统SQL注入getshell
------------------------------

### 漏洞类型：SQL注入

### 漏洞等级：严重

### 漏洞URL： 

[http://mp.test.com:89/message.do](http://mp.test.com:89/message.do)

### 漏洞描述: 

泛微Emobile系统配合SQL注入导出shell

### 漏洞详细：

泛微Emobile系统配合SQL注入导出shell

这里通过client.do接口（method为pullmsg），其中"udid"参数存在注入。

后端使用H2数据库，可以直接导出shell，操作过程如下：

因为emobile中限定只能访问action，像jsp等文件无法直接访问，所以这里选择覆盖/WEB-INF/page/message.jsp

当访问message.do接口时，会使用该jsp文件作为模板，这样就可以访问到写入的shell了。

第一步，将cmdshell写入表中：

![](%E6%B3%9B%E5%BE%AEe-mobile%200day/%E5%9B%BE%E7%89%871.png)

第二步，导出shell到指定文件：

![](%E6%B3%9B%E5%BE%AEe-mobile%200day/%E5%9B%BE%E7%89%872.png)

第三步，通过小马上传cmd写入到自身：

![](%E6%B3%9B%E5%BE%AEe-mobile%200day/%E5%9B%BE%E7%89%873.png)

第四步，访问shell 密码c：

http://mp.test.cn:89/message.do  
执行ipconfig：

![](%E6%B3%9B%E5%BE%AEe-mobile%200day/%E5%9B%BE%E7%89%874.png)

数据包字数超限制可以将获取到的信息转存至别的服务器。

### 平台方案：

1.修改Web应用服务的软件部分，增加对客户端提交数据的合法性验证，至少严格过滤SQL语句中的关键字，并且所有验证都应该在服务器端实现，以防客户端控制被绕过。验证GET、POST、COOKIE等方法中URL后面跟的参数，需过滤的关键字有' 单引号、""双引号、\\'反斜杠单引号、\\""反斜杠双引号、)括号、;分号、--双减号、+加号。以及SQL关键字，注意对于关键字要对大小写都识别。

2.建议降低Web应用访问使用较低权限的用户访问数据库。不要使用数据库管理员等高权限的用户访问数据库。

3.使用安全的框架如Qframe或使用通用防注入脚本。

4.尽量使用预编译的方式执行SQL。

5.对于将进入SQL语句拼接前的参数,数字型参数对数字进行数字型检测，并检测范围,字符型参数对参数进行转义。

6.为了防止二次注入，可以在二次拼接SQL语句前，对取出的参数进行转义。