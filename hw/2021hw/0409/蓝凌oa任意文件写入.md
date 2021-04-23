# 蓝凌oa任意文件写入
早上起来刷了下朋友圈,看到了一个新漏洞  
蓝凌 OA 存在任意文件写入???蓝凌????并且还有漏洞地址

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/image.png)

漏洞在`/sys/search/sys_search_main/sysSearchMain.do` 下面，这里也给出了 `method` 为 `editrParam`。参数为 `FdParameters`  
已经很明确了,那么复现一下。

在 `com.landray.kmss.sys.search.jar` 中的`com.landray.kmss.sys.search.actions.SysSearchMainAction` 类。  
`method` 为 `editrParam`。  
 

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/1_image.png)

看下流程。  
 

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/2_image.png)

大概就是对 `fdParemNames` 的内容进行了判空。如果不为空。进入  
`SysSearchDictUtil.getParamConditionEntry` 方法。其实这一步不重要。因为后面这  
一步也没啥用。就讲讲。。  
主要还是在 `setParametersToSearchConditionInfo` 方法。  
 

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/3_image.png)

也是对 `fdParemNames` 进行了一次判空。然后传入  
`ObjectXML.objectXMLDecoderByString` 方法。这里就是漏洞点了  
追过去就更好理解了。讲传入进来的 string 字符进行替换。然后讲其载入字节数组缓冲区,  
在传递给 `objectXmlDecoder`。

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/4_image.png)

在 `objectXmlDecoder` 中。就更明显了。典型的 xmlDecoder 反序列化。  
整体流程只对 `FdParameters` 的内容进行了一些内容替换。  
导致 `xmlDecoder` 反序列化漏洞。  
本地 POC:  
Xmldecoder payload 生成  
[https://github.com/mhaskar/XMLDecoder-payload-generator](https://github.com/mhaskar/XMLDecoder-payload-generator)

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/5_image.png)

这里尝试打开文稿 `pages.app`(第一次用 mac,气质没跟上)  
Code:

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/6_image.png)

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/7_image.png)

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/8_image.png)

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/9_image.png)

当然,别多想。这是个后台洞。因为开放的白名单只有以下几个:

![](%E8%93%9D%E5%87%8Coa%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E5%86%99%E5%85%A5/10_image.png)