# 某weblogic的T3反序列化0day分析
公司小兄弟发给我一个py样本，是今日捕获的某weblogic 0day，咱们来分析一下。

使用我的javaSerializationTools工具，来分析这个样本。结果如图

![](%E6%9F%90weblogic%E7%9A%84T3%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%960day%E5%88%86%E6%9E%90/640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

jdk7u21调试一下

![](%E6%9F%90weblogic%E7%9A%84T3%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%960day%E5%88%86%E6%9E%90/1_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

当然，weblogic 12已经不支持在jdk版本低于1.8的jdk下运行。

![](%E6%9F%90weblogic%E7%9A%84T3%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%960day%E5%88%86%E6%9E%90/2_640wx_fmt%3Dpng%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.png)

我们可以很明显的看到，这个是反序列化gadgets中7u21的变种。唯一不同的是`com.sun.org.apache.xalan.internal.xsltc.trax`被用`java.rmi.MarshalledObject`代替。要了解这个为什么可以绕过weblogic黑名单，我们要了解一下weblogic 反序列化的黑名单究竟是什么

在java反序列化的过程中，会层层解析所需要的类，而weblogic就是控制解析反序列化的类，如果碰到可能触发恶意操作的类的名称，则直接打断反序列化流程。

而weblogic在处理jdk 7u21这条反序列化gadgets中，为了平衡拦截的效果与不影响业务，选择拦截`com.sun.org.apache.xalan.internal.xsltc.trax`这个类。而这个类恰恰也是绝大多数java反序列化中最为关键的一环。

所以，如果我们想要绕过weblogic针对7u21的反序列化拦截的黑名单，则需要找到`com.sun.org.apache.xalan.internal.xsltc.trax`的替代。

我在这里简单分析一下7u21中`AnnotationInvocationHandler`到`com.sun.org.apache.xalan.internal.xsltc.trax`的过程。因为在poc中只有这里改变了。

`Templates`类的`newTransformer`方法，会将属性`_bytecodes`，通过调用java的`defineClass`去生成一个类，并将其实例化，也就是调用静态代码块的代码。

而`AnnotationInvocationHandler`，创建一个`Templates`的jdk动态代理，在hashmap出现哈希碰撞的时候，在hashmap中会调用`AnnotationInvocationHandler`的equal方法，equal方法会调用自身的equalImpl方法。最终会调用被代理对象的每个方法，去生成结果，相关代码如下

    private Boolean equalsImpl(Object var1) {
           // 判断var1是否为AnnotationInvocationHandle,var1是templates，pass
            if (var1 == this) {
                return true;
              // 构造限制点，type属性限制了var1必须为this.type的类实例
            } else if (!this.type.isInstance(var1)) {
                return false;
            } else {
                //这里获取了当前成员的方法
                Method[] var2 = this.getMemberMethods();
                int var3 = var2.length;
                for(int var4 = 0; var4 < var3; ++var4) {
                    Method var5 = var2[var4]; //遍历获取方法
                    String var6 = var5.getName(); //获取方法名字
                    Object var7 = this.memberValues.get(var6);//获取memberValues中的值
                    Object var8 = null;
                    // Proxy.isProxyClass(var1.getClass()
                    // 判断varl是不是代理类,显然不是，pass
                    AnnotationInvocationHandler var9 = this.asOneOfUs(var1);
                    if (var9 != null) {
                        var8 = var9.memberValues.get(var6);
                    } else {
                        try {
                            // 这里直接进行了方法的调用核心。
                            // var5是方法名,var1是可控的类
                            // var1.var5()
                            var8 = var5.invoke(var1);
                            private Method[] getMemberMethods() {
            if (this.memberMethods == null) {
                this.memberMethods = (Method[])AccessController.doPrivileged(new PrivilegedAction<Method[]>() {
                    public Method[] run() {
                        Method[] var1 = AnnotationInvocationHandler.this.type.getDeclaredMethods();
                        AccessibleObject.setAccessible(var1, true);
                        return var1;
                    }
                });
            }
            return this.memberMethods;
        }

因为`newTransformer`方法恰好为`Templates`的第一个方法，如果是第二个方法的话，会导致执行第一个方法的时候出错而中断整个反序列化链。

而poc中，使用了`java.rmi.MarshalledObject`这个类，我们来分析一下。

在`java.rmi.MarshalledObject`中，`getMemberMethods`方法返回的一个方法是`get`。`get`代码如下

        public T get() throws IOException, ClassNotFoundException {
            if (objBytes == null)   // must have been a null object
                return null;
            ByteArrayInputStream bin = new ByteArrayInputStream(objBytes);
            // locBytes is null if no annotations
            ByteArrayInputStream lin =
                (locBytes == null ? null : new ByteArrayInputStream(locBytes));
            MarshalledObjectInputStream in =
                new MarshalledObjectInputStream(bin, lin);
            @SuppressWarnings("unchecked")
            T obj = (T) in.readObject();
            in.close();
            return obj;

一看就懂了，将`objBytes`属性作为反序列化的流，从中解析对象。我们知道，weblogic中，必须要调用`FilteredObjectInputStream`，才可以在反序列化过程中使用反序列化的黑名单。如果类中私自调用`ObjectInputStream`，则不会应用weblogic反序列化的黑名单。从而绕过

剩下的流程就与7u21的触发流程就一样了，只需要把`objBytes`随心所欲的替换为你喜欢的反序列化就可以，在这里无视weblogic黑名单。

当然，我拿到的样本，只是一个简单的回显代码，并没有太复杂的操作。

解决方案
----

1.  这个反序列化漏洞并不只是影响jdk7u21，因为我们知道8u21是7u21的变种，理论上将jdk 8u21以下的jdk都受到此反序列化gadget的影响。
2.  直接关闭iiop/t3这两个协议

poc的java生成代码，大家可能一看就明白了