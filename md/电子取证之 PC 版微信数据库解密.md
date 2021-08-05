> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/kliyiZvdgXo4U71YowFlUg)

电子取证之 PC 版微信数据库解密
=================

记录学习「PC 版微信数据库解密」全过程，参考原文「PC 版微信数据库解密详细教程」链接：https://bbs.pediy.com/thread-251303-4.htm

### 1、环境 & 工具

*   Windows10：https://www.microsoft.com/
    
*   PC 版微信：https://pc.weixin.qq.com/
    
*   visual studio community 2019：https://visualstudio.microsoft.com/zh-hans/
    
*   Ollydbg (吾爱破解专用版)：https://down.52pojie.cn/Tools/Debuggers/%E5%90%BE%E7%88%B1%E7%A0%B4%E8%A7%A3%E4%B8%93%E7%94%A8%E7%89%88Ollydbg.rar
    
*   openssl 1.0.2：https://www.openssl.org/source/openssl-1.0.2r.tar.gz
    
*   SQLite DB Browser：https://sqlitebrowser.org/dl/
    

### 2、提取数据库文件密码

打开 微信（退出状态） 和 OD ：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmXtg7eKYVsYUiaO458IMOKRpQRzhD3ogwNzcDw3SKYfibQmw9uk8EH3qQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmuMFuWFBl5DqSa5BfCmqMcnJR50tBF0vWbEQoA4vxlnNrcEHlM4FgCQ/640?wx_fmt=png)

使用 OD 附加 微信进程， 点击 “文件” --> "附加"  会弹出新窗口， 找到名称是 wechat  的选中 点击附加：   

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmgGGbmHic54D4UgcZG5ecYwqFf8wc17xMpsLFtFqfkRJ9NpibM6q9HYLg/640?wx_fmt=png)

加载后 OD 标题处会显示 wechat.exe:  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmicUpw72aeUUJTibDDFD0PCgfAJeyyz2bYTTZPNHywCaI11JWKORG3wSg/640?wx_fmt=png)

点击菜单栏 “查看” --> "可执行模块" （快捷键：Alt+E）：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmUeuZ6OLl4ScrkR5D13PnoFVx7JibhsDGhjEdnmUqUBF1vU0J7CbePGw/640?wx_fmt=png)

打开后找到 名称为 “WeChatWi” 且路径以 WeChatWin.dll 结尾这一行，双击进入：  

```
Executable modules:
名称=WeChatWi
文件版本=3.3.0.115
路径=D:\Program Files (x86)\Tencent\WeChat\WeChatWin.dll
```

进入后 OD 标题末尾处会显示 WeChatWi , 接下来点击 “插件”-->“中文搜索引擎”--> "搜索 ASCII" ：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmXWF0OP8RGHlezrHQ3FVfhUBrFeGxPAesU9juTLTDoWU11UcBtNXGZA/640?wx_fmt=png)

点击后需要等等待一会，搜索结束后会跳转到搜索结果界面：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmvu1303sianfDmvmmOkonFRr55Zia9SYwLtenmvic82cJGibVgxksRRPXtQ/640?wx_fmt=png)

搜索结果展示，在此界面右键 选择 “Find” (快捷键：Ctrl+F)：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmnWC1zFQdr8NtGFVJyro1WARmZnTiafC5GG7gTs17qPhXbk1b9GpCOvQ/640?wx_fmt=png)

在搜索框中输入 “DBFactory::encryptDB”：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnm0xDiaibU2MIqnibI39icV9nuNQiamd8ZOePYHQic8wANuPibMW8U3MCno0AIA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnm0PoCOibvH9lnjwmf8cDdS90NTLxVcoNCWjiaMmYenBibRMBYZMgXgSrkw/640?wx_fmt=png)

搜索到后双击进入，会定位到 “push WeChatWi .XXXXXX"这个位置，然后向下 6 行找到”test edx , edx" :  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnm2wuKlWnM4pfcYAiaKnlu5dF8YibXIxqR4bY3LZLXT5RnT2MbRQnlWOCQ/640?wx_fmt=png)

在 “test edx,edx"这一行下断点， 直接双击本行（鼠标不要放在地址那一栏）或者 选中本行 按下快捷键”F2" , 断点设置成功后，本行地址栏会变成红色：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmLIwvmlz9sH7f0t7SZ5wiaoibdrmpibMDKIhuhVf3Icn9seia1S5CsmCGYA/640?wx_fmt=png)

断点设置好后，点击 “” 按钮（或者在调试菜单中选择 “运行”，快捷键 “F9”)，这时寄存器窗口中的 EDX 的值应该是 00000000。  

切换到微信登录页面，点击登录，然后到手机端确认登录。这是 OllyDbg 界面中的数据不断滚动，直到 EDX 不再为全 0 并且各个窗口内容停止滚动为止。

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnm5lnPr7uOytJIgMrw13tIYRuHkQSD68iczuP9PJRqzL4D52at0UfIIxg/640?wx_fmt=png)

此时断点生效了，寄存器的值也发生变化了，接下来单击选中 EDX 的值然后单击鼠标右键，在弹出的菜单里面选择 “数据窗口中跟随”，则数据窗口中显示的就是 EDX 的值也就是内存地址对应的内容：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmesaMekokhsGCxoONGuPCfxp5uUu6oY6lBUHxWQRia2V4MnCiawuQk6Dw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmrsREab1ibswtxPAbhALyUXSnT1zNPFibgamibp0Zh2tBtWcpYkSooVwZQ/640?wx_fmt=png)

从地址”05340DB8“ 开始选中 32 个字节, 就是微信数据库的加密密码，本图中密码如下：  

```
05340DB8  71 1A 1F FA 27 E6 41 D9 AB 8E 8D C0 F1 8A F9 66  
05340DC8  76 11 6F EF 95 30 48 91 B3 9B 40 9B 57 B1 35 00  
```

”711A1FFA27E641D9AB8E8DC0F18AF96676116FEF95304891B39B409B57B13500”    得到这个即密码提取结束，退出 OD。

将提取到的密码转换为 `0x` 格式备用，如下：

```
{0x71,0x1A,0x1F,0xFA,0x27,0xE6,0x41,0xD9,0xAB,0x8E,0x8D,0xC0,0xF1,0x8A,0xF9,0x66,0x76,0x11,0x6F,0xEF,0x95,0x30,0x48,0x91,0xB3,0x9B,0x40,0x9B,0x57,0xB1,0x35,0x00}
```

### 3、编译解密程序

本文使用编译工具：visual studio community 2019

#### 3.1 - 配置 openssl

在编译前需要配置 openssl  ，经过测试强制使用 openssl 1.0.2r 的版本，下载地址：https://www.openssl.org/source/openssl-1.0.2r.tar.gz

下载并解压， openssl 需要自己编译，网上教程有很多，我直接把编译后生成的文件打包：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmf6icrPvUuictpCkJCIrYHWCzFm67wCiaZU14R9KO4uBZbvufrmGvAiajmQ/640?wx_fmt=png)

将这个两个文件夹直接复制到 openssl 1.0.2r 解压的目录中：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmUkZ5zZA2Y7DcxqXbw2Rl2qREzDc707nVPAftRdmjOGb3seqMqheDDA/640?wx_fmt=png)

#### 3.2 - 配置 visual studio  

接下来配置 visual studio, 打开 visual studio，选择 “创建新项目”：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmJdlWEXLjpegaOqUlcIWz6M2n8lsLicxA0zSHgV77bBDWsZxqzTUqo5w/640?wx_fmt=png)

选择 “C++ 控制台应用”：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmphh3OtJo5XQedV13lgNru4Qp1iaCemyHODZz0eLbIAr5aNeH49ib3dXQ/640?wx_fmt=png)

配置项目：（名称和位置 自定义）设置好后点击创建  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmC81iaP6lMxo18P0AAjic32rrPZQRl3Q7rMR71whvXZia7uGf9HcrE20UQ/640?wx_fmt=png)

生成默认的 hello world 代码：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmXC4GeI6IULDS67KibUmVT5WsOWgl17dATKicoB65E7nP9bRHia4CT0ibwA/640?wx_fmt=png)

接下是添加 openssl 附加依赖库，单击 菜单栏的 “项目” --> "dewechatdb 属性"：（这个跟设置的项目名称一致）  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmeRtXfyhgrhQiaAmvJic7UndQ55nxZo1wzKiahoCGUMUwV3qDIichSxu8nQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnm2Kw7BuqJXYo2U7yTo2CFU3JJJ8OmPqIF2OE2ulvfBsJo7UhianhiaYWw/640?wx_fmt=png)

1. 配置与平台需要保持一致：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmYbubG2aZcLqEdDfma4FyBVibeVHmtG3PH1ibrxKyNsrlW8o1EzLPsN8w/640?wx_fmt=png)

2. 选择 C/C++ 下面的 “常规” --> 配置项 “附加包含目录” ：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmVCHIBGqOJJR9uZnVtV5bg0WOEHlJLXk7v2XwDaWFMMKibTkG9GZx7PQ/640?wx_fmt=png)

点击右侧空白处。在下拉框里选择 “编辑…”，在对话框中点击四个图标按钮最左侧的“新行” 按钮，会生成一个空白行，点击右侧的“…”：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnm7xK8vMfn6Frlm44KnpzI1BDTIaib50WkiaqcrEsRIj9o8JiapBBgxqQUQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmFB06P5V3t3ncMaBJCbo5guKXehVmOIMCpvf5T1EISxia5haib629s5gw/640?wx_fmt=png)

在弹出的对话框里选择前面解压的 openssl 目录（根据自己放目录选择，本文是`D:\tools\openssl-1.0.2r`）中的 include 目录。

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnm0USCYFt7vlohrncmRtR0ooibhzzBGS4WjaM7tWasZD98j9icvD4FFS3A/640?wx_fmt=png)

配置好后如图：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmPyBZ7vS18fp5MuRqeBHR0aC4hGvkkr0UZaLUWcHKbAS7pXpPV7LicjQ/640?wx_fmt=png)

3. 选择左侧 “链接器” 下面的“常规” --> “附加库目录”:

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmTJT25VNRXGzSNv809UGiaLdFDgoLUlq19XOMTTzspjGY3D9CkHOZ8oA/640?wx_fmt=png)

点击右侧空白处，选择 openssl 目录下的 lib 目录，设置完成后如下：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmMOd1gr9XicAVgjfdh6e0wb5DKOTXrVMPwp0LJ4niakiaeA43MCPQ6tO1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmUDtsuTqeL6eK0RoVkbh3j8oEMFgJLQgpSs9EqG4jm6Oa0JDicDhrePw/640?wx_fmt=png)

最后点击 “链接器 -->“输入”：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmAricHqIRauToic1iayaM5EsOic5Y1rH10gIc6pwib4LfECyExfW5OYWrEuw/640?wx_fmt=png)

右侧最上面有 “附加依赖项”，默认已经有一些系统库，点击右侧内容，选择 “编辑…”  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmteEnGbricNutyCOe8bISopyPolSibNb53deIibdszx7dP4BIoUrFrP3JQ/640?wx_fmt=png)

添加 `libeay32.lib` 、`ssleay32.lib` 依赖项。  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmSKVDMkWEVcd2QL7brt2dEfeXRxITOVehh6G2xxX3RdbkNqbONNNnxA/640?wx_fmt=png)

到此配置完成。  

#### 3.3 - 编译程序

复制大佬的源代码：

```
using namespace std;
#include <Windows.h>
#include <iostream>
#include <openssl/rand.h>
#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/hmac.h>

#undef _UNICODE
#define SQLITE_FILE_HEADER "SQLite format 3"
#define IV_SIZE 16
#define HMAC_SHA1_SIZE 20
#define KEY_SIZE 32

#define SL3SIGNLEN 20

#ifndef ANDROID_WECHAT
#define DEFAULT_PAGESIZE 4096       //4048数据 + 16IV + 20 HMAC + 12
#define DEFAULT_ITER 64000
#else
#define NO_USE_HMAC_SHA1
#define DEFAULT_PAGESIZE 1024
#define DEFAULT_ITER 4000
#endif
//pc端密码是经过OllyDbg得到的32位pass。
unsigned char pass[] = { 0x53,0xE9,0xBF,0xB2,0x3B,0x72,0x41,0x95,0xA2,0xBC,0x6E,0xB5,0xBF,0xEB,0x06,0x10,0xDC,0x21,0x64,0x75,0x6B,0x9B,0x42,0x79,0xBA,0x32,0x15,0x76,0x39,0xA4,0x0B,0xB1 };
char dbfilename[50];
int Decryptdb();
int main(int argc, char* argv[])
{
   if (argc >= 2)    //第二个参数argv[1]是文件名
       strcpy_s(dbfilename, argv[1]);  //复制    
          //没有提供文件名，则提示用户输入
   else {
       cout << "请输入文件名:" << endl;
       cin >> dbfilename;
  }
   Decryptdb();
   return 0;
}

int Decryptdb()
{
   FILE* fpdb;
   fopen_s(&fpdb, dbfilename, "rb+");
   if (!fpdb)
  {
       printf("打开文件错!");
       getchar();
       return 0;
  }
   fseek(fpdb, 0, SEEK_END);
   long nFileSize = ftell(fpdb);
   fseek(fpdb, 0, SEEK_SET);
   unsigned char* pDbBuffer = new unsigned char[nFileSize];
   fread(pDbBuffer, 1, nFileSize, fpdb);
   fclose(fpdb);

   unsigned char salt[16] = { 0 };
   memcpy(salt, pDbBuffer, 16);

#ifndef NO_USE_HMAC_SHA1
   unsigned char mac_salt[16] = { 0 };
   memcpy(mac_salt, salt, 16);
   for (int i = 0; i < sizeof(salt); i++)
  {
       mac_salt[i] ^= 0x3a;
  }
#endif

   int reserve = IV_SIZE;      //校验码长度,PC端每4096字节有48字节
#ifndef NO_USE_HMAC_SHA1
   reserve += HMAC_SHA1_SIZE;
#endif
   reserve = ((reserve % AES_BLOCK_SIZE) == 0) ? reserve : ((reserve / AES_BLOCK_SIZE) + 1) * AES_BLOCK_SIZE;

   unsigned char key[KEY_SIZE] = { 0 };
   unsigned char mac_key[KEY_SIZE] = { 0 };

   OpenSSL_add_all_algorithms();
   PKCS5_PBKDF2_HMAC_SHA1((const char*)pass, sizeof(pass), salt, sizeof(salt), DEFAULT_ITER, sizeof(key), key);
#ifndef NO_USE_HMAC_SHA1
   PKCS5_PBKDF2_HMAC_SHA1((const char*)key, sizeof(key), mac_salt, sizeof(mac_salt), 2, sizeof(mac_key), mac_key);
#endif

   unsigned char* pTemp = pDbBuffer;
   unsigned char pDecryptPerPageBuffer[DEFAULT_PAGESIZE];
   int nPage = 1;
   int offset = 16;
   while (pTemp < pDbBuffer + nFileSize)
  {
       printf("解密数据页:%d/%d \n", nPage, nFileSize / DEFAULT_PAGESIZE);

#ifndef NO_USE_HMAC_SHA1
       unsigned char hash_mac[HMAC_SHA1_SIZE] = { 0 };
       unsigned int hash_len = 0;
       HMAC_CTX hctx;
       HMAC_CTX_init(&hctx);
       HMAC_Init_ex(&hctx, mac_key, sizeof(mac_key), EVP_sha1(), NULL);
       HMAC_Update(&hctx, pTemp + offset, DEFAULT_PAGESIZE - reserve - offset + IV_SIZE);
       HMAC_Update(&hctx, (const unsigned char*)& nPage, sizeof(nPage));
       HMAC_Final(&hctx, hash_mac, &hash_len);
       HMAC_CTX_cleanup(&hctx);
       if (0 != memcmp(hash_mac, pTemp + DEFAULT_PAGESIZE - reserve + IV_SIZE, sizeof(hash_mac)))
      {
           printf("\n 哈希值错误! \n");
           getchar();
           return 0;
      }
#endif
       //
       if (nPage == 1)
      {
           memcpy(pDecryptPerPageBuffer, SQLITE_FILE_HEADER, offset);
      }

       EVP_CIPHER_CTX* ectx = EVP_CIPHER_CTX_new();
       EVP_CipherInit_ex(ectx, EVP_get_cipherbyname("aes-256-cbc"), NULL, NULL, NULL, 0);
       EVP_CIPHER_CTX_set_padding(ectx, 0);
       EVP_CipherInit_ex(ectx, NULL, NULL, key, pTemp + (DEFAULT_PAGESIZE - reserve), 0);

       int nDecryptLen = 0;
       int nTotal = 0;
       EVP_CipherUpdate(ectx, pDecryptPerPageBuffer + offset, &nDecryptLen, pTemp + offset, DEFAULT_PAGESIZE - reserve - offset);
       nTotal = nDecryptLen;
       EVP_CipherFinal_ex(ectx, pDecryptPerPageBuffer + offset + nDecryptLen, &nDecryptLen);
       nTotal += nDecryptLen;
       EVP_CIPHER_CTX_free(ectx);

       memcpy(pDecryptPerPageBuffer + DEFAULT_PAGESIZE - reserve, pTemp + DEFAULT_PAGESIZE - reserve, reserve);
       char decFile[1024] = { 0 };
       sprintf_s(decFile, "dec_%s", dbfilename);
       FILE * fp;
       fopen_s(&fp, decFile, "ab+");
      {
           fwrite(pDecryptPerPageBuffer, 1, DEFAULT_PAGESIZE, fp);
           fclose(fp);
      }

       nPage++;
       offset = 0;
       pTemp += DEFAULT_PAGESIZE;
  }
   printf("\n 解密成功! \n");
   return 0;
}
```

替换`pass[]` 的值为第一步获取的 密码：(转换成 0x 格式的密码值)

```
//pc端密码是经过OllyDbg得到的32位pass。
unsigned char pass[] = {}

//本文获取的密码为：
{0x71,0x1A,0x1F,0xFA,0x27,0xE6,0x41,0xD9,0xAB,0x8E,0x8D,0xC0,0xF1,0x8A,0xF9,0x66,0x76,0x11,0x6F,0xEF,0x95,0x30,0x48,0x91,0xB3,0x9B,0x40,0x9B,0x57,0xB1,0x35,0x00}
```

替换好后将代码复制到刚才在 visual studio 创建的 `dewechatdb.cpp` 中（删除默认生成的 hello world 代码）：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmHUxnIdqicC1ccUn4oCt9FF9SVnQiabORa6DYh4PWDticoCmIbic7AvRmAA/640?wx_fmt=png)

点击 “本地 windows 调试器”（或者按 F5 键），如果前面的步骤操作都正确，应该可以完成编译并自动运行，弹出一个命令行窗口，提示需要输入文件名则为成功：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmeJ2TG1ZKX64JADrxxNwzibCVVibgIDNp9n0C6wRPDUj5Qs6pHgzWbD9w/640?wx_fmt=png)

编译成功，生成了 `D:\wwwcode\c\dewechatdb\Debug\dewechatdb.exe`  文件，将 dewechatdb.exe 复制到微信的数据库文件夹中，  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmuoaZVr8bVfiad70U67xwzBJmRMEF9xy7icbpbzkHpticHhsvOicpibMzsvA/640?wx_fmt=png)

默认安装微信的文件夹路径为：`C:\Users\Administrator\Documents\WeChat Files\********\Msg` ，  

如果找不到路径可以在微信`设置`--> `文件管理` 中找到，可以使用`打开文件夹` 按钮直接打开：

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmOaQQgliaUesFgaBUejxwE93opHvbwtzhojJKo4n9tjpGqrYqHI2ugYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmnkNxrE7lFrzKjUDnvYY6HVyQ4HncibKMjyia32Fj7J4MfkoWNNTibvMQg/640?wx_fmt=png)

```
//使用：
dewechatdb.exe 数据库名
```

解密 `ChatMsg.db` 这个库：

```
dewechatdb.exe ChatMsg.db
```

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmZ99Ug64TvcfhBMatqRj0Qz02QRtBOKVIEbNKA3G9sZwVU0SQDwnHGw/640?wx_fmt=png)

解密成功后会生成 `dec_ChatMsg.db` 文件，即为解密后的数据库文件，使用 `DB Browser for SQLite` 工具打开即可查看内容：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmZ37Gum4NE76EhDmCB90qOB2xFmmticc2QkM3ZLVf9KSHtCVzbRQTNQA/640?wx_fmt=png)

解密后的数据（微信聊天记录）：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmOf058MZWpl3ya0qaNcOXF6l0mh0sMdUTFiaCRK8CpvOHQm66GxJ7Pjg/640?wx_fmt=png)

到此解密完成。  

### 4、常见问题汇总（踩坑记录）

> Q1：为什么我下载的 openssl 里面没有 lib 目录，而且 include 内为空？
> 
> A1: openssl 下载后需要编译（win 安装的 openssl 会出现位置错误），才会有 lib 目录 和 include 里面的内容，本文已打包 include 和 lib 文件夹。

> Q2: 设置断点之后微信就显示无法获取二维码或者无法登陆？
> 
> A2：OD 版本问题可以换一个 OD 试一试（建议使用与本文一致的 OD），或者是 设置好断点后 没有点击`运行` 。

> Q3: 为什么编译完成后使用生成的 exe 解密时显示 “打开文件错”？
> 
> A3：经过测试是因为在解密时微信是在登录状态，所以在解密数据库文件时要退出微信（一定还有其他情况会提示 “打开文件错”，我没遇到）。

> Q4: 编译好的 exe 运行时提示缺少`libeay32.dll`文件？
> 
> A4：下载一个根据系统版本放在指定的目录内就可以了：https://cn.dll-files.com/libeay32.dll.html
> 
> 下载后会有教程：  

![](https://mmbiz.qpic.cn/mmbiz_png/QgqjbLiaSQxx1B5QHjyejzLGITdsPXGnmUiczDzYniaiaBYjJ94RuJq7LEl5nu9ZV1LMicLSC1ibCtteqwDyhLZr1JicA/640?wx_fmt=png)