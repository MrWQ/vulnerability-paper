> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/jf7TDbBcYh562b163Jk0ig)

微信搜索关注 安全族

  

  

**本文简介**

本文通过简单本地 FUZZ 找到漏洞溢出点

  

  

**1.shellcode 升级**

    在前面中，笔者将 shellcode 放在了 buffer 遍历里面，而想要寻找到 shellcode 的时候，笔者需要将 ret 后的地址修改为 buffer 的地址，这样定位 shellcode 的话，是非常不精准的，因为在更换系统或机器的话，漏洞利用成功率是不高的。  

    而本文要做的就是将 shellcode 进行一下升级，当 ret 返回的时候，能够能加准确的定位 shellcode。

    看如下图，属实没有绘画天赋.... 继续看图，ret 之后相当于执行了 pop eip，而此时 esp 也会加一个格子到 shellcode 这里，所以此时栈顶就是 shellcode，而如果此时我们将 ret 改为 jmp esp，则会跳转到栈顶，成功执行 shellcode。

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWyxlZFOsrqKS6hc005jdr6PicptILv9wNzFcWptyKzYr6EF3c8MrZCBGYeDfkIXbtE3EVt3saDy2X1Q/640?wx_fmt=png)

    那么如何将 ret 改为 jmp esp 的地址呢？jmp esp 的硬编码为 FFE4  

    而我们的应用程序，在运行时都会加载 dll 文件的，我们通过搜索 dll 文件里面的 jmp esp 地址，来进行使用，  

    下面是我写的一个代码。大家也可以自行去寻找。  

```
#include "stdafx.h"
#include <windows.h>
#include <stdlib.h>
int main(int argc, char* argv[])
{
  BYTE* ptr;
  HINSTANCE handle = LoadLibrary("user32.dll");
  int nums = TRUE;
  if (!handle){
    printf("载入dll失败");
    return 0;
  }
  else{
    ptr = (BYTE*)handle;
    for (int i = 0; nums; i++)
    if (ptr[i] == 0XFF && ptr[i + 1] == 0XE4){
      int address = (int)ptr + i;
      printf("user32.dll的Jmp ESP地址为%p\n", address);
      system("pause");
      return 0;
    }
  }
  
  system("pause");
  return 0;
}
```

然后直接将 ret 的内容写成这个即可，在 ret 后面写入 shellcode，并可以更加精确的定位 shellcode 了

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWyxlZFOsrqKS6hc005jdr6PiczbKPIUKuap2kiciaLZoqsRlJBS85FTKuKQRrqr9sFYNM1gxSYn8rbzjQ/640?wx_fmt=png)

  

  

  

**2**

    继续今天的内容，通过本地 FUZZ 进行查找漏洞点，当一个漏洞程序栈空间是很大的情况，我们是不确定漏洞溢出点在哪里，就可以通过 Windows 日志快速定位漏洞点，如下图，定位的偏移量就是漏洞溢出点了，那么这个地址就是 ret 的地址了。

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWyxlZFOsrqKS6hc005jdr6PicVlu89n9jIiafYxSSYzMqb7yw17hpAXPpEuQ1LaIe8YQibPa3ZOczFcNg/640?wx_fmt=png)

接下来打开我们的 password.txt 进行查看一下，成功找到 ret 的地方，修改为 jmp esp 的地址。

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWyxlZFOsrqKS6hc005jdr6PicEOBQCMjVhjpEAOyia1u7SYiba8scOyQ6iaE22Qp80TGBUyKsTuG682Wag/640?wx_fmt=png)

修改成如下图：这里的 shellcode 是我本地提取的。

![](https://mmbiz.qpic.cn/mmbiz_png/8miblt1VEWyxlZFOsrqKS6hc005jdr6PicJ3wZJibyNicia3zCpEelqsnTGaicyYX3bJ6icNfibdtecgI6fuEr8Xfyfwxg/640?wx_fmt=png)

运行一下程序看一下，通过简单的 Fuzz 成功定位漏洞点并成功执行 shellcode。**漏洞代码在最后**

![](https://mmbiz.qpic.cn/mmbiz_jpg/8miblt1VEWyxlZFOsrqKS6hc005jdr6PicTTJBsKs6mhn7zuIMkqpybbv9bMAcbwUfD4kVP9o9rhNQzxDQjCgt3Q/640?wx_fmt=jpeg)

  

  

  

  

  

漏洞代码

```
#include "stdafx.h"
#include <string.h>
#include <stdlib.h>
#include<windows.h>
#define PASSWORD "1234567"
int verify_password(char *password)
{
  int authenticated;
  char buffer[44];
  printf("%p\n",buffer);
  authenticated = strcmp(password, PASSWORD);
  strcpy(buffer, password);
  return authenticated;
}

int main(int argc, char* argv[])
{

  LoadLibrary("user32.dll");
  int valid_flag = 0;
  char password[1024];
  FILE* fp;
  if(!(fp= fopen("password.txt","rw+"))){
    printf("文件打开失败\n");
    system("pause");
    return 0;
  }
  fscanf(fp,"%s",password);
  valid_flag = verify_password(password);
  if (valid_flag)
  {
  printf("incorrect password!\n\n");
  }
  else
  {
    printf("Congratulation! You have passed the verification!\n"); 
  }
  system("pause");
  return 0;
}
```

  

  

  

  

**扫一扫关注本公众号**

![](https://mmbiz.qpic.cn/mmbiz_jpg/8miblt1VEWywCsRiaweFhRW8aDdjtoCoSU2eQAJ6KxKAoP0PSHvjGJvTZcRRXTAeSd9Qyib0ynLnBUwdiahhhOaSDQ/640?wx_fmt=jpeg)