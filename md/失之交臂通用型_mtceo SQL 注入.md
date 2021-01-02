> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/h8x1zNgMrcSIPLH-1MP09A)

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RXu3bXekvbOVFvAicpfFJwIOcQOuakZ6jTmyNoeraLFgI4cibKrDRiaPAljUry4dy4e2zK8lUMyKfkGg/640?wx_fmt=png)

### 下载地址

`http://61.155.169.167:81/code/201109/MTCEO_a5.zip`

### 项目背景

MTCEO 文库系统可转目前已知所有文档格式，设置监视文件夹和转换后文件夹，即可开始自动转换，无需人工干预，是文库网站必备软件！

1、具有文库基本功能

2、用户可以互为粉丝

3、可以对文档进行评分、收藏和推荐

4、完善了网站积分机制

5、完美整合 ucenter，可与 discuz 论坛互通头像、积分和用户

6、评论、评分更加完善，表情等可后台自定义

7、预览无压力，借用官方开放平台，不占用个人空间！

8、文库模板自由替换机制，详情可见教程区模板相关教程

9、后台在线升级、数据库备份与还原、缓存更新

10、腾讯、新浪微博和淘宝一键登录支持！

11、标签机制，自由更改模板内容

### 工具使用

1、运行环境 php5.4+mysql5.7

2、IDE phpstorm

3、审计工具 Rips + Burp Suite + sqlmap

### 影响版本

v2.6

### 搭建环境效果

前台：

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RV6gpl409V1NryhPA2obsqyiaNr2VUfBn5CCkQFsoEiaa6IKjrx7KicQCSia3Nhd4fyTbhKjLrKiaDoBCA/640?wx_fmt=jpeg)

后台：

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RV6gpl409V1NryhPA2obsqy3ccpzRMJ9GnScUYAtWM0ooiaD5zxDibgLpZsfR5YJf164lciamepcZxBA/640?wx_fmt=jpeg)

### 漏扫扫描结果

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RV6gpl409V1NryhPA2obsqypRG1ibACdicciaeIFhZsfEaqMF6psDMxUic7tq3vpZNx3TonzqPwHu4Xpg/640?wx_fmt=jpeg)

### 代码分析

通过上面的关键词`name_exists(`搜索定位，搜索到的含有这个函数的文件还是挺多的，下面笔者只分析一处，思路是相通的嘛。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RV6gpl409V1NryhPA2obsqyxSKy0RTbZS6hS80FzPU9jG699xuH9JtJFjW38FDB6OlOmPsRBicO8oQ/640?wx_fmt=jpeg)

所以我们分析哪一个呢，那就 article_cate 这个文件吧，我们来到这个包含这个关键词的方法体。

```
/**     * 入库数据整理     */    protected function _before_insert($data = '') {        //检测分类是否存在        if($this->_mod->name_exists($data['name'], $data['pid'])){            $this->ajaxReturn(0, L('article_cate_already_exists'));        }        //生成spid        $data['spid'] = $this->_mod->get_spid($data['pid']);        return $data;    }
```

那么这里的参数 data 是调用这个方法时，传的参数，那么是哪里调用的呢，来，接着全局扫搜，我们找到该控制器的父级里面，有这么一个方法，调用了它。

```
/**     * 添加     */    public function add() {        $mod = D($this->_name);                 if (IS_POST) {            if (false === $data = $mod->create()) {                IS_AJAX && $this->ajaxReturn(0, $mod->getError());                $this->error($mod->getError());            }            if (method_exists($this, '_before_insert')) {                $data = $this->_before_insert($data);            }                        if($data['spid']=='maxcate'){                //$data['spid']='';                IS_AJAX && $this->ajaxReturn(0, '分类限制为三级分类,级别太深不利于优化哦');                $this->error('分类限制为三级分类,级别太深不利于优化哦');                            }            if($data['spid']=='0|'){                                $data['spid']=0;            }            if( $mod->add($data) ){                if( method_exists($this, '_after_insert')){                    $id = $mod->getLastInsID();                    $this->_after_insert($id);                }                IS_AJAX && $this->ajaxReturn(1, L('operation_success'), '', 'add');                $this->success(L('operation_success'));            } else {                IS_AJAX && $this->ajaxReturn(0, L('operation_failure'));                $this->error(L('operation_failure'));            }                           } else {                                      $this->assign('open_validator', true);            if (IS_AJAX) {                                 $response = $this->fetch();                $this->ajaxReturn(1, '', $response);            } else {                                 $this->display();            }        }    }
```

在这个方法体的十二行，调用了这个方法，并且通过前面的判断，给 data 参数做了赋值操作，怎么赋值的呢，$mod->create(); 这个是赋值操作，然而，此处的变量 mod 是对应 article 的模型，不巧的是，这个文件不存在这个方法，那它在哪呢，不错，在它的父级里，这是 PHP 的继承性。于是乎，在它父级找到这个方法，如下:

```
/**     * 创建数据对象 但不保存到数据库     * @access public     * @param mixed $data 创建数据     * @param string $type 状态     * @return mixed     */    public function create($data='',$type='') {        // 如果没有传值默认取POST数据        if(empty($data)) {            $data   =   $_POST;        }elseif(is_object($data)){            $data   =   get_object_vars($data);        }        // 验证数据        if(empty($data) || !is_array($data)) {            $this->error = L('_DATA_TYPE_INVALID_');            return false;        }        // 检查字段映射        $data = $this->parseFieldsMap($data,0);        // 状态        $type = $type?$type:(!empty($data[$this->getPk()])?self::MODEL_UPDATE:self::MODEL_INSERT);        // 检测提交字段的合法性        if(isset($this->options['field'])) { // $this->field('field1,field2...')->create()            $fields =   $this->options['field'];            unset($this->options['field']);        }elseif($type == self::MODEL_INSERT && isset($this->insertFields)) {            $fields =   $this->insertFields;        }elseif($type == self::MODEL_UPDATE && isset($this->updateFields)) {            $fields =   $this->updateFields;        }        if(isset($fields)) {            if(is_string($fields)) {                $fields =   explode(',',$fields);            }            // 判断令牌验证字段            if(C('TOKEN_ON'))   $fields[] = C('TOKEN_NAME');            foreach ($data as $key=>$val){                if(!in_array($key,$fields)) {                    unset($data[$key]);                }            }        }        // 数据自动验证        if(!$this->autoValidation($data,$type)) return false;        // 表单令牌验证        if(C('TOKEN_ON') && !$this->autoCheckToken($data)) {            $this->error = L('_TOKEN_ERROR_');            return false;        }        // 验证完成生成数据对象        if($this->autoCheckFields) { // 开启字段检测 则过滤非法字段数据            $fields =   $this->getDbFields();            foreach ($data as $key=>$val){                if(!in_array($key,$fields)) {                    unset($data[$key]);                }elseif(MAGIC_QUOTES_GPC && is_string($val)){                    $data[$key] =   stripslashes($val);                }            }        }        // 创建完成对数据进行自动处理        $this->autoOperation($data,$type);        // 赋值当前数据对象        $this->data =   $data;        // 返回创建的数据以供其他调用        return $data;    }
```

这里面我们需要注意是哪里啊，没错，就是在第十行的位置，它没有过滤，直接把 $_POST 这么一个全局变量给了 data。如果说这是悲剧的开始，那么悲剧的最后一次防御的机会，它也没有守好。看代码。

```
/**     * 检测分类是否存在     *      * @param string $name     * @param int $pid     * @param int $id     * @return bool      */    public function name_exists($name, $pid, $id=0) {        $where = ";        $result = $this->where($where)->count('id');        if ($result) {            return true;        } else {            return false;        }    }
```

在判断存不存在的时候，没有遵循底层框架的书写规范，拿到这个 data 里面的 name 值，直接进行了参数的拼接啊，在 tp3 的版本里，至少要写个数据格式的吧，然而，最后把自己送到了鬼门关。

至此代码分析完。

### 工具验证阶段

说到验证 SQL 注入的最好的工具，肯定就是 sqlmap 啦。啥也不说了，抓个包埋点土吧，看看能长出来个啥。

抓取包的链接：主机地址 +/index.php?g=admin&m=article_cate

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RV6gpl409V1NryhPA2obsqyKqWPiau67ZOKqhnicRuQ6kvouPUFoEsDqTxp4PjGhYHwujanhiaLzw0yQ/640?wx_fmt=jpeg)

包内容如下：

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RV6gpl409V1NryhPA2obsqy0ia3I9mLzFRoJ4fbsyhSTNwU1fe5oo9dibqBr29t5DeAkV1LTX1EwGew/640?wx_fmt=jpeg)

将包导入 sqlmap 里。跑一下，看的能否跑出结果

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RV6gpl409V1NryhPA2obsqy4k7avkINQm16jao0KFlplo4aBeArg7lbNySuCUWsXzjCb1ef3EndYQ/640?wx_fmt=jpeg)

好，PHP 版本跑的很准确，MySQL 数据也是可以的。说明确实存在问题。

### 修复阶段

1、遵循开发手册，按照指定好的原则来，别手动拼接 SQL，很危险、很危险、很危险【重要的事说三遍】，如果按照规则来了，还有漏洞，这个锅可以甩给 tp 啦。

2、做特殊字符的过滤验证【推荐第一种修复】

E

N

D

**关**

**于**

**我**

**们**

Tide 安全团队正式成立于 2019 年 1 月，是新潮信息旗下以互联网攻防技术研究为目标的安全团队，团队致力于分享高质量原创文章、开源安全工具、交流安全技术，研究方向覆盖网络攻防、系统安全、Web 安全、移动终端、安全开发、物联网 / 工控安全 / AI 安全等多个领域。

团队作为 “省级等保关键技术实验室” 先后与哈工大、齐鲁银行、聊城大学、交通学院等多个高校名企建立联合技术实验室，近三年来在网络安全技术方面开展研发项目 60 余项，获得各类自主知识产权 30 余项，省市级科技项目立项 20 余项，研究成果应用于产品核心技术研究、国家重点科技项目攻关、专业安全服务等。对安全感兴趣的小伙伴可以加入或关注我们。

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RX4MU7S4WB8R6vF3JbUjA7K0ZtOPxqGSo1HGPhTDicQibOro93UYNBOwRPd4EFseGTDsl1tan0ZXcmw/640?wx_fmt=gif)

我知道你**在看**哟

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8Ogkicew5KMd52mUWzJfFj3dJZvlic64DFticvDw8cFIBUwubIQAkF5IXQtw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8OgTqzpHQhUIM8BG5s07pmhaElGiclG2tlw7ceJtrgVwZepMEpQpdvic1xg/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RVJq73PAV8iaQCPQyOPyU8Og23eRiaUlSIpFGAOzOUv2fVVWr1ZKozfELyDaWWnpGmfabNTNiblArbdw/640?wx_fmt=gif)