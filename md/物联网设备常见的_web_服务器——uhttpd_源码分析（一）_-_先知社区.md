> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/9543)

[![](https://xzfile.aliyuncs.com/media/upload/picture/20210507182014-cfd37d3e-af1d-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20210507182014-cfd37d3e-af1d-1.png)  
0x00 前言  
uHTTPd 是一个 OpenWrt/LUCI 开发者从头编写的 Web 服务器。 它着力于实现一个稳定高效的服务器，能够满足嵌入式设备的轻量级任务需求，且能够与 OpenWrt 的配置框架 (UCI) 整合。默认情况下它被用于 OpenWrt 的 Web 管理接口 LuCI。当然，uHTTPd 也能提供一个常规 Web 服务器所需要的所有功能。  
0x01 简介  
讲解 uhttpd 的主要原因是：uhttpd 是物联网设备很常见的一个 web 服务器，在物联网设备漏洞挖掘的过程中，最常见的漏洞都是出现在 web 服务器上，如果能熟悉各个开源的 web 服务器的开发流程，更容易理解其他厂商的开发者是如何开发自己的 web 服务器，那么对物联网漏洞挖掘将事倍功半。  
下载地址：[https://git.openwrt.org/?p=project/uhttpd.git;a=summary](https://git.openwrt.org/?p=project/uhttpd.git;a=summary) 点击 snapshot 即可下载  
0x02 主函数 main

```
int main(int argc, char **argv) 
{ 
        struct alias *alias; 
        bool nofork = false; 
        char *port; 
        int opt, ch; 
        int cur_fd; 
        int bound = 0; 
#ifdef HAVE_TLS 
        int n_tls = 0; 
        const char *tls_key = NULL, *tls_crt = NULL, *tls_ciphers = NULL; 
#endif 
#ifdef HAVE_LUA 
        const char *lua_prefix = NULL, *lua_handler = NULL; 
#endif 
    // 如果没有LUA插件,才会执行 
        BUILD_BUG_ON(sizeof(uh_buf) < PATH_MAX); 

        uh_dispatch_add(&cgi_dispatch); // 添加cgi_dispatch到dispatch_handlers链表中,后续解析cgi或者lua用 
        init_defaults_pre(); //初始化默认参数,如:cgi的前缀名为 /cgi-bin 
    /*设置信号屏蔽*/ 
        signal(SIGPIPE, SIG_IGN); 
    /*用户输入的参数*/ 
        while ((ch = getopt(argc, argv, "A:aC:c:Dd:E:e:fh:H:I:i:K:k:L:l:m:N:n:P:p:qRr:Ss:T:t:U:u:Xx:y:")) != -1) { 
                switch(ch) { 
#ifdef HAVE_TLS 
                case 'C': 
                        tls_crt = optarg; 
                        break; 

                case 'K': 
                        tls_key = optarg; 
                        break; 

                case 'P': 
                        tls_ciphers = optarg; 
                        break; 

                case 'q': 
                        conf.tls_redirect = 1; 
                        break; 

                case 's': 
                        n_tls++; 
                        /* fall through */ 
#else 
                case 'C': 
                case 'K': 
                case 'P': 
                case 'q': 
                case 's': 
                        fprintf(stderr, "uhttpd: TLS support not compiled, " 
                                        "ignoring -%c\n", ch); 
                        break; 
#endif 
                case 'p': 
                        optarg = strdup(optarg); 
                        bound += add_listener_arg(optarg, (ch == 's')); 
                        break; 

                case 'h': 
                        if (!realpath(optarg, uh_buf)) { 
                                fprintf(stderr, "Error: Invalid directory %s: %s\n", 
                                                optarg, strerror(errno)); 
                                exit(1); 
                        } 
                        conf.docroot = strdup(uh_buf); 
                        break; 

                case 'H': 
                        if (uh_handler_add(optarg)) { 
                                fprintf(stderr, "Error: Failed to load handler script %s\n", 
                                        optarg); 
                                exit(1); 
                        } 
                        break; 

                case 'E': 
                        if (optarg[0] != '/') { 
                                fprintf(stderr, "Error: Invalid error handler: %s\n", 
                                                optarg); 
                                exit(1); 
                        } 
                        conf.error_handler = optarg; 
                        break; 

                case 'I': 
                        if (optarg[0] == '/') { 
                                fprintf(stderr, "Error: Invalid index page: %s\n", 
                                                optarg); 
                                exit(1); 
                        } 
                        uh_index_add(optarg); 
                        break; 

                case 'S': 
                        conf.no_symlinks = 1; 
                        break; 

                case 'D': 
                        conf.no_dirlists = 1; 
                        break; 

                case 'R': 
                        conf.rfc1918_filter = 1; 
                        break; 

                case 'n': 
                        conf.max_script_requests = atoi(optarg); 
                        break; 

                case 'N': 
                        conf.max_connections = atoi(optarg); 
                        break; 
                /*cgi文件路径前缀*/ 
                case 'x': 
                        fixup_prefix(optarg); 
                        conf.cgi_prefix = optarg; 
                        break; 

                case 'y': 
                        alias = calloc(1, sizeof(*alias)); 
                        if (!alias) { 
                                fprintf(stderr, "Error: failed to allocate alias\n"); 
                                exit(1); 
                        } 
                        alias->alias = strdup(optarg); 
                        alias->path = strchr(alias->alias, '='); 
                        if (alias->path) 
                                *alias->path++ = 0; 
                        list_add(&alias->list, &conf.cgi_alias); 
                        break; 

                case 'i': 
                        optarg = strdup(optarg); 
                        port = strchr(optarg, '='); 
                        if (optarg[0] != '.' || !port) { 
                                fprintf(stderr, "Error: Invalid interpreter: %s\n", 
                                                optarg); 
                                exit(1); 
                        } 

                        *port++ = 0; 
                        uh_interpreter_add(optarg, port); 
                        break; 

                case 't': 
                        conf.script_timeout = atoi(optarg); 
                        break; 

                case 'T': 
                        conf.network_timeout = atoi(optarg); 
                        break; 

                case 'k': 
                        conf.http_keepalive = atoi(optarg); 
                        break; 

                case 'A': 
                        conf.tcp_keepalive = atoi(optarg); 
                        break; 

                case 'f': 
                        nofork = 1; 
                        break; 

                case 'd': 
                        optarg = strdup(optarg); 
                        port = alloca(strlen(optarg) + 1); 
                        if (!port) 
                                return -1; 

                        /* "decode" plus to space to retain compat */ 
                        for (opt = 0; optarg[opt]; opt++) 
                                if (optarg[opt] == '+') 
                                        optarg[opt] = ' '; 

                        /* opt now contains strlen(optarg) -- no need to re-scan */ 
                        if (uh_urldecode(port, opt, optarg, opt) < 0) { 
                                fprintf(stderr, "uhttpd: invalid encoding\n"); 
                                return -1; 
                        } 

                        printf("%s", port); 
                        return 0; 
                        break; 

                /* basic auth realm */ 
                case 'r': 
                        conf.realm = optarg; 
                        break; 

                /* md5 crypt */ 
                case 'm': 
                        printf("%s\n", crypt(optarg, "$1$")); 
                        return 0; 
                        break; 

                /* config file */ 
                case 'c': 
                        conf.file = optarg; 
                        break; 

#ifdef HAVE_LUA 
                case 'l': 
                case 'L': 
                        if (ch == 'l') { 
                                if (lua_prefix) 
                                        fprintf(stderr, "uhttpd: Ignoring previous -%c %s\n", 
                                                ch, lua_prefix); 

                                lua_prefix = optarg; 
                        } 
                        else { 
                                if (lua_handler) 
                                        fprintf(stderr, "uhttpd: Ignoring previous -%c %s\n", 
                                                ch, lua_handler); 

                                lua_handler = optarg; 
                        } 

                        if (lua_prefix && lua_handler) { 
                                add_lua_prefix(lua_prefix, lua_handler); 
                                lua_prefix = NULL; 
                                lua_handler = NULL; 
                        } 

                        break; 
#else 
                case 'l': 
                case 'L': 
                        fprintf(stderr, "uhttpd: Lua support not compiled, " 
                                        "ignoring -%c\n", ch); 
                        break; 
#endif 
#ifdef HAVE_UBUS 
                case 'a': 
                        conf.ubus_noauth = 1; 
                        break; 

                case 'u': 
                        conf.ubus_prefix = optarg; 
                        break; 

                case 'U': 
                        conf.ubus_socket = optarg; 
                        break; 

                case 'X': 
                        conf.ubus_cors = 1; 
                        break; 

                case 'e': 
                        conf.events_retry = atoi(optarg); 
                        break; 
#else 
                case 'a': 
                case 'u': 
                case 'U': 
                case 'X': 
                case 'e': 
                        fprintf(stderr, "uhttpd: UBUS support not compiled, " 
                                        "ignoring -%c\n", ch); 
                        break; 
#endif 
                default: 
                        return usage(argv[0]); 
                } 
        } 
        /*配置文件解析*/ 
        uh_config_parse(); 

        if (!conf.docroot) { 
                if (!realpath(".", uh_buf)) { //uh_buf为当前工作目录的绝对路径指针 
                        fprintf(stderr, "Error: Unable to determine work dir\n"); 
                        return 1; 
                } 
                conf.docroot = strdup(uh_buf); //docroot字段保存了当前工作路径 
        } 
        /*初始化默认主页和cgi绝对路径*/ 
        init_defaults_post(); 

        if (!bound) { //如果没有监听端口成功,则报错退出 
                fprintf(stderr, "Error: No sockets bound, unable to continue\n"); 
                return 1; 
        } 

#ifdef HAVE_TLS // 如果有TLS插件才会执行,也就是https 
        if (n_tls) { 
                if (!tls_crt || !tls_key) {//没有公匙或者没有私匙，则报错退出 
                        fprintf(stderr, "Please specify a certificate and " 
                                        "a key file to enable SSL support\n"); 
                        return 1; 
                } 

                if (uh_tls_init(tls_key, tls_crt, tls_ciphers))//初始化加密 
                    return 1; 
        } 
#endif 

#ifdef HAVE_LUA // 有LUA插件才会执行 
        if (lua_handler || lua_prefix) { 
                fprintf(stderr, "Need handler and prefix to enable Lua support\n"); 
                return 1; 
        } 
    /*uh_plugin_init会初始化lua的插件,也就是会执行uhttpd_lua.so中的初始化函数,然后再判断是否存在lua文件,类似执行 lua luci 命令,使用lua执行自己创建的文件,如果执行错误,或者缺少某些文件则不能继续执行*/ 
        if (!list_empty(&conf.lua_prefix) && uh_plugin_init("uhttpd_lua.so")) 
                return 1; 
#endif 
#ifdef HAVE_UBUS // 有UBUS插件才会执行 
    /*原理和LUA差不多*/ 
        if (conf.ubus_prefix && uh_plugin_init("uhttpd_ubus.so")) 
                return 1; 
#endif 
        /* 加了-f 则 nofork==1,这样则不会通过fork创建子进程*/ 
        /* fork (if not disabled) */ 
        if (!nofork) { 
                switch (fork()) { 
                case -1: 
                        perror("fork()"); 
                        exit(1); 

                case 0: 
                        /* daemon setup */ 
                        if (chdir("/")) 
                                perror("chdir()"); 

                        cur_fd = open("/dev/null", O_WRONLY); 
                        if (cur_fd > 0) { 
                                dup2(cur_fd, 0); 
                                dup2(cur_fd, 1); 
                                dup2(cur_fd, 2); 
                        } 

                        break; 

                default: 
                        exit(0); 
                } 
        } 
    /*运行服务器的主要函数*/ 
        return run_server(); 
}
```

0x03 signal 函数  
位置：main-->signal

```
signal(SIGPIPE, SIG_IGN);
根据信号的默认处理规则SIGPIPE信号的默认执行动作是terminate(终止、退出)。简单的理解就是在发送或接受数据时，可能会产生一个SIGPIPE信号，可能会导致进程退出，但是我们却不想进程退出，为了避免进程退出, 可以捕获SIGPIPE信号, 或者忽略它, 给它设置SIG_IGN信号(屏蔽)处理函数。
参考：
1. https://blog.csdn.net/sysleo/article/details/95984946
2. https://www.runoob.com/cprogramming/c-function-signal.html
3. https://my.oschina.net/u/2252538/blog/2993724
```

0x04 uh_config_parse 函数  
位置：main-->uh_config_parse

```
static void uh_config_parse(void) 
{ 
        const char *path = conf.file; 
        FILE *c; 
        char line[512]; 
        char *col1; 
        char *col2; 
        char *eol; 
        /*如果conf.file没有赋值,则默认为/etc/httpd.conf*/ 
        if (!path) 
                path = "/etc/httpd.conf"; 

        c = fopen(path, "r"); 
        if (!c) 
                return; 

        memset(line, 0, sizeof(line)); 
        /*配置文件的逐步解析*/ 
        while (fgets(line, sizeof(line) - 1, c)) { 
                if ((line[0] == '/') && (strchr(line, ':') != NULL)) { 
                        if (!(col1 = strchr(line, ':')) || (*col1++ = 0) || 
                                !(col2 = strchr(col1, ':')) || (*col2++ = 0) || 
                                !(eol = strchr(col2, '\n')) || (*eol++  = 0)) 
                                continue; 

                        uh_auth_add(line, col1, col2); 
                } else if (!strncmp(line, "I:", 2)) { 
                        if (!(col1 = strchr(line, ':')) || (*col1++ = 0) || 
                                !(eol = strchr(col1, '\n')) || (*eol++  = 0)) 
                                continue; 

                        uh_index_add(strdup(col1)); 
                } else if (!strncmp(line, "E404:", 5)) { 
                        if (!(col1 = strchr(line, ':')) || (*col1++ = 0) || 
                                !(eol = strchr(col1, '\n')) || (*eol++  = 0)) 
                                continue; 

                        conf.error_handler = strdup(col1); 
                } 
                else if ((line[0] == '*') && (strchr(line, ':') != NULL)) { 
                        if (!(col1 = strchr(line, '*')) || (*col1++ = 0) || 
                                !(col2 = strchr(col1, ':')) || (*col2++ = 0) || 
                                !(eol = strchr(col2, '\n')) || (*eol++  = 0)) 
                                continue; 

                        uh_interpreter_add(col1, col2); 
                } 
        } 

        fclose(c); 
}
```

0x05 init_defaults_post 函数  
位置：main-->init_defaults_post

```
static void init_defaults_post(void) 
{ 
    /*将这四个文件设置为默认主页*/ 
        uh_index_add("index.html"); 
        uh_index_add("index.htm"); 
        uh_index_add("default.html"); 
        uh_index_add("default.htm"); 
        /*如果设置有cgi前缀,则将当前工作路径加上cgi的工作路径,默认情况(默认情况cgi是/cgi-bin)如：/xxx/xxx/xxx/cgi-bin(绝对路径加 /cgi-bin)*/ 
        if (conf.cgi_prefix) { 
                char *str = malloc(strlen(conf.docroot) + strlen(conf.cgi_prefix) + 1); 

                strcpy(str, conf.docroot); 
                strcat(str, conf.cgi_prefix); 
                conf.cgi_docroot_path = str; 
                conf.cgi_prefix_len = strlen(conf.cgi_prefix); 
        }; 
}
```

0x00 uh_index_add 函数  
位置：main-->init_defaults_post-->uh_index_add

```
void uh_index_add(const char *filename) 
{ 
        struct index_file *idx; 

        idx = calloc(1, sizeof(*idx)); 
        idx->name = filename; 
        list_add_tail(&idx->list, &index_files);//将传进来的默认主页添加到index_files双向列表中 
}
```

0x06 uh_plugin_init 函数  
位置：main-->uh_plugin_init

```
/*通过so库初始化插件*/ 
int uh_plugin_init(const char *name) 
{ 
        struct uhttpd_plugin *p; 
        const char *sym; 
        void *dlh; 
    /* 路径默认：/usr/lib/ + name 如果路径不对的话,则会报错*/ 
        dlh = dlopen(name, RTLD_LAZY | RTLD_GLOBAL); 
        if (!dlh) { 
                fprintf(stderr, "Could not open plugin %s: %s\n", name, dlerror()); 
                return -ENOENT; 
        } 

        sym = "uhttpd_plugin"; 
        p = dlsym(dlh, sym); 
        if (!p) { 
                fprintf(stderr, "Could not find symbol '%s' in plugin '%s'\n", sym, name); 
                return -ENOENT; 
        } 

        list_add(&p->list, &plugins); 
        return p->init(&ops, &conf);//比如ubus:p->init == uh_ubus_plugin_init 
}
```

0x00 dlopen 函数  
位置：main-->uh_plugin_init-->dlopen

```
dlh = dlopen(name, RTLD_LAZY | RTLD_GLOBAL);
相当于打开so动态链接库，并返回一个句柄，如果打开失败则会返回NULL（本人只出现过没有该文件，八成就是没有在/usr/lib/路径下创建该动态链接库），以供后续调用该动态链接库中的函数，或其他操作。
参考：
https://man7.org/linux/man-pages/man3/dlopen.3.html
https://blog.csdn.net/teleger/article/details/80857900
```

0x01 dlsym 函数  
位置：main-->uh_plugin_init-->dlsym

```
sym = "uhttpd_plugin";
p = dlsym(dlh, sym);
dlsym是一个计算机函数，功能是根据动态链接库操作句柄与符号，返回符号对应的地址，不但可以获取函数地址，也可以获取变量地址。uhttpd则是获取一个初始化的函数。如果初始化失败，则会返回NULL。
参考：
https://baike.baidu.com/item/dlsym/6603915?fr=aladdinsym = "uhttpd_plugin";
p = dlsym(dlh, sym);
dlsym是一个计算机函数，功能是根据动态链接库操作句柄与符号，返回符号对应的地址，不但可以获取函数地址，也可以获取变量地址。uhttpd则是获取一个初始化的函数。如果初始化失败，则会返回NULL。
参考：
https://baike.baidu.com/item/dlsym/6603915?fr=aladdin
```

0x07 run_server 函数  
位置：main-->run_server