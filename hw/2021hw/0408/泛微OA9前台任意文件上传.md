# 泛微OA9前台任意文件上传
漏洞位于: `/page/exportImport/uploadOperation.jsp`文件中

Jsp流程大概是:判断请求是否是multipart请求,然就没有了,直接上传了,啊哈哈哈哈哈  
重点关注File file=new File(savepath+filename),  
Filename参数,是前台可控的,并且没有做任何过滤限制

![](%E6%B3%9B%E5%BE%AEOA9%E5%89%8D%E5%8F%B0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0/%E5%9B%BE%E7%89%879.png)

利用非常简单,只要对着  
`127.0.0.1/page/exportImport/uploadOperation.jsp`  
来一个multipartRequest就可以,利用简单,自评高危!!

![](%E6%B3%9B%E5%BE%AEOA9%E5%89%8D%E5%8F%B0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0/%E5%9B%BE%E7%89%8710.png)

然后请求路径:  
`view-source:http://112.91.144.90:5006/page/exportImport/fileTransfer/1.jsp`

![](%E6%B3%9B%E5%BE%AEOA9%E5%89%8D%E5%8F%B0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0/%E5%9B%BE%E7%89%8711.png)