> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/evrIZCPz18Qa-MSBCprCJA)

**Preview**

由于自动化运行过程中需要 awvs 运行生成用户和文件，所以本人无法做到一步到位，文章底部有一步到位的 dockerfile

注：如认为本破解补丁存在某些后门或转载删版权者，请勿使用！  

![](https://mmbiz.qpic.cn/mmbiz_jpg/VfLUYJEMVsjyfiaOziatiaWkrvktg2XASiaC4wcO3r6vH3OUknHO9DQ2PxMrIRTlk4lxCMn6ofYYftTVibthh7LQp9A/640?wx_fmt=jpeg)

  
![](https://mmbiz.qpic.cn/mmbiz_jpg/VfLUYJEMVsjyfiaOziatiaWkrvktg2XASiaCMj1PjFPrsibCB1LWPPDL5ZaYZpLxBWjJ8ib7gbRk3CKyJwXSLhO54ibaw/640?wx_fmt=jpeg)

**Install**  

--------------

```
docker pull registry.cn-hangzhou.aliyuncs.com/xrsec/awvs:v14
docker run -it -d --name awvs -p 3443:3443 xrsec/awvs:v14
```

**Info**  

-----------

```
地址：https://ip:3443
账户：awvs@awvs.com
密码：Awvs@awvs.com
```

**File**
--------

### Dockerfile：  

```
FROM xrsec/awvs:test
LABEL maintainer="xrsec"
LABEL mail="troy@zygd.site"

ENTRYPOINT ["/awvs/awvs.sh"]

EXPOSE 3443

# ENV TZ='Asia/Shanghai'
# ENV LANG 'zh_CN.UTF-8'

STOPSIGNAL SIGQUIT

CMD ["/awvs/awvs.sh"]
```

### awvs.sh：  

```
#!/bin/bash
clear
echo -e "\033[1;31m      __          ____      _______   \033[0m"
echo -e "\033[1;32m     /\ \        / /\ \    / / ____|  \033[0m"
echo -e "\033[1;33m    /  \ \  /\  / /  \ \  / / (___    \033[0m"
echo -e "\033[1;34m   / /\ \ \/  \/ /    \ \/ / \___ \   \033[0m"
echo -e "\033[1;35m  / ____ \  /\  /      \  /  ____) |  \033[0m"
echo -e "\033[1;36m /_/    \_\/  \/        \/  |_____/   \033[0m"                                
echo -e "\033[1;34m -------------- \033[0m"                           
echo -e "\033[1;31m __  __  ____                      \033[0m"
echo -e "\033[1;32m \ \/ / |  _ \   ___    ___    ___  \033[0m"
echo -e "\033[1;33m  \  /  | |_) | / __|  / _ \  / __| \033[0m"
echo -e "\033[1;34m  /  \  |  _ <  \__ \ |  __/ | (__  \033[0m"
echo -e "\033[1;35m /_/\_\ |_| \_\ |___/  \___|  \___| \n\033[0m"
echo -e "\033[1;31m Thank's fahai && Timeline Sec \n\033[0m"
echo -e "\033[1;32m [ help ] \033[0m"
echo -e "\033[1;35m [ https://www.fahai.org/index.php/archives/110/ ] \033[0m"
echo -e "\033[1;33m [ https://blog.zygd.site/AWVS14%20Docker.html ] \n\033[0m"

su -l acunetix -c /home/acunetix/.acunetix/start.sh
```

### awvs_x86.sh:  

```
https://www.fahai.org/index.php/archives/110/
```

**Step**
--------

### Centos ❌  

```
RUN yum update -y \
    yum upgrade -y \
    && yum install -y libgdk_pixbuf-2.0.so.0 libsmime3.so libpango-1.0.so.0 \
    libX11.so.6 libasound.so.2 libgtk-3.so.0 libgbm.so.1 libcups.so.2 \
    libXfixes.so.3 libdrm.so.2 libxcb.so.1 libnspr4.so libXext.so.6 \
    libatk-1.0.so.0 libatspi.so.0 libXcomposite.so.1 libXrandr.so.2 \
    libcairo.so.2 libxkbcommon.so.0 libnssutil3.so libXdamage.so.1 \
    libnss3.so libgdk-3.so.0 libatk-bridge-2.0.so.0 libX11-xcb.so.1 \
    sudo
```

### Ubuntu18.04 ✅  

```
RUN apt update -y \
    && apt upgrade -y \
    && apt-get install libxdamage1 libgtk-3-0 libasound2 libnss3 libxss1 libx11-xcb-dev sudo libgbm-dev curl ncurses-bin unzip -y

RUN mkdir /awvs
COPY awvs_listen.zip /awvs
COPY awvs.sh /awvs
COPY Dockerfile /awvs

RUN chmod 777 /awvs/awvs.sh \
    && unzip -d /awvs/ /awvs/awvs_listen.zip \
    && cp /awvs/wvsc /home/acunetix/.acunetix/v_210503151/scanner/ \
    && cp /awvs/license_info.json /home/acunetix/.acunetix/data/license/ \
    && cp /awvs/wa_data.dat /home/acunetix/.acunetix/data/license/
```

### automate ❌  

```
FROM ubuntu:18.04
LABEL maintainer="xrsec"
LABEL mail="troy@zygd.site"

RUN mkdir /awvs
COPY awvs_listen.zip /awvs
COPY awvs.sh /awvs
COPY Dockerfile /awvs
COPY awvs_x86.sh /awvs

# init
RUN apt update -y \
    && apt upgrade -y \
    && apt-get install libxdamage1 libgtk-3-0 libasound2 libnss3 libxss1 libx11-xcb-dev sudo libgbm-dev curl ncurses-bin unzip -y

# init_install
RUN chmod 777 /awvs/awvs_x86.sh \
    && sed -i "s/read -r dummy/#read -r dummy/g" /awvs/awvs_x86.sh \
    && sed -i "s/pager=\"more\"/pager=\"cat\"/g" /awvs/awvs_x86.sh \
    && sed -i "s/read -r ans/ans=yes/g" /awvs/awvs_x86.sh \
    && sed -i "s/read -p \"    Hostname \[\$host_name\]:\" hn/hn=awvs/g" /awvs/awvs_x86.sh \
    && sed -i "s/host_name=\$(hostname)/host_ /awvs/awvs_x86.sh \
    && sed -i "s/read -p \"    Hostname \[\$host_name\]:\" hn/awvs/g" /awvs/awvs_x86.sh \
    && sed -i "s/read -p '    Email: ' master_user/master_user=admin@admin.com/g" /awvs/awvs_x86.sh \
    && sed -i "s/read -sp '    Password: ' master_password/master_password=Admin@admin.com/g" /awvs/awvs_x86.sh \
    && sed -i "s/read -sp '    Password again: ' master_password2/master_password2=Admin@admin.com/g" /awvs/awvs_x86.sh \
    && sed -i "s/systemctl/\# systemctl/g"  /awvs/awvs_x86.sh

# TODO
RUN su -l acunetix -c /home/acunetix/.acunetix/start.sh & sleep 10 && exit

# init_listen
RUN chmod 777 /awvs/awvs.sh \
    && unzip -d /awvs/ /awvs/awvs_listen.zip \
    && chmod 444 /awvs/license_info.json \
    && cp /awvs/wvsc /home/acunetix/.acunetix/v_210503151/scanner/ \
    && cp /awvs/license_info.json /home/acunetix/.acunetix/data/license/ \
    && cp /awvs/wa_data.dat /home/acunetix/.acunetix/data/license/ \
    && chown acunetix:acunetix /home/acunetix/.acunetix/data/license/wa_data.dat

ENTRYPOINT ["/awvs/awvs.sh"]

EXPOSE 3443

# ENV TZ='Asia/Shanghai'
# ENV LANG 'zh_CN.UTF-8'

STOPSIGNAL SIGQUIT

CMD ["/awvs/awvs.sh"]
```