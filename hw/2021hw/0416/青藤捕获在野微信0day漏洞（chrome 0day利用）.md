# 青藤捕获在野微信0day漏洞（chrome 0day利用）
近日，青藤主机安全产品捕获了一个高威胁的在野微信0day漏洞。黑客只需要通过微信发送一个特制web链接，用户一旦点击链接，微信PC(windows)版进程wechatweb.exe会加载shellcode执行，整个过程无文件落地，无新进程产生。青藤检测出wechatweb.exe存在内存恶意代码，继而排查出了0day漏洞，并在第一时间报告腾讯安全应急响应中心并协助其修复漏洞。

![](%E9%9D%92%E8%97%A4%E6%8D%95%E8%8E%B7%E5%9C%A8%E9%87%8E%E5%BE%AE%E4%BF%A10day%E6%BC%8F%E6%B4%9E%EF%BC%88chrome%200day%E5%88%A9%E7%94%A8%EF%BC%89/640wx_fmt%3Djpeg%26tp%3Dwebp%26wxfrom%3D5%26wx_lazy%3D1%26wx_co%3D1.webp)

青藤检测出wechatweb.exe存在内存恶意代码

目前微信已修复漏洞并发布了更新版本，强烈建议大家立即将微信更新到3.2.1.141以上版本修复漏洞。官方下载链接：

https://dldir1.qq.com/weixin/Windows/WeChatSetup.exe