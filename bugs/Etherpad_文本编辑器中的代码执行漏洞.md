> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/bJBk8olMW7q7kX4IWwUwXA)

![](https://mmbiz.qpic.cn/mmbiz_png/OhKLyqyFoP9mJwX65uY3o0wwuMo2eWPeFuDIhxJlAjMcIicKFSYLVZ6fjicY0dNle24gfmiaVpwCcP2PeZuZyaRzw/640?wx_fmt=png)点击上方蓝字关注我们

![](https://mmbiz.qpic.cn/mmbiz_jpg/DQk5QiaQiciakYDxc1NGsstJOmicNIFsV0W3RN4ecIOEfARY4Evoh1icVvFcUHU4EtcSOcqiaAxp3f1RLh3ve1SaHBhg/640?wx_fmt=jpeg)

概述


------

Etherpad 是一个开源的，基于 Web 的在线文本编辑器，它允许实时协作处理文档。Etherpad 拥有 250 多个可用插件并具有版本历史记录和在线聊天功能，用户可以使用插件进行自定义。Etherpad 非常受欢迎，在全球拥有数百万活跃用户。

研究人员在 Etherpad 1.8.13 中发现了两个关键漏洞。其中一个是 XSS 跨站脚本漏洞 (CVE-2021-34817)，另一个是参数注入漏洞 (CVE-2021-34816)。攻击者可以组合利用这两个漏洞，以完全接管 Etherpad 实例及其数据。

影响


------

XSS 跨站脚本漏洞 (CVE-2021-34817) 允许攻击者接管 Etherpad 用户 (包括管理员)，可被用于窃取或操纵敏感数据。参数注入漏洞(CVE-2021-34816) 允许攻击者在服务器上执行任意代码，攻击者可以窃取、修改或删除所有数据，或针对可从服务器访问的其他内部系统。

攻击者可以在默认配置的 Etherpad 实例上，利用 XSS 漏洞获得管理员权限。之后结合利用参数注入漏洞 (CVE-2021-34816)，从而在服务器上执行任意代码。以下是结合利用这两个漏洞在服务器上获得 shell 的演示视频：

技术细节


--------

**聊天消息中的持久性 XSS(CVE-2021-34817)**

Etherpad 支持在线聊天功能，用户可以在每个群聊中交换消息。消息存储在服务器上，每个人都可以查看聊天记录。

当用户打开键盘时，聊天消息会在前端渲染，这涉及从该数据创建 HTML 元素。在渲染期间，聊天消息的 userId 属性被插入到 DOM 中，特殊字符没有被正确转义：

src/static/js/chat.js

```
173    const html =
174        `<p data-authorId='${msg.userId}' …> …` +
175        `<span …`;
176    if (isHistoryAdd) $(html).insertAfter('#chatloadmessagesbutton');
177    else $('#chattext').append(html);
```

在第 174 行，userId 值被用于构建一个 HTML 标记字符串，随后该字符串在第 176 和 177 行被插入到 DOM 中。如果攻击者成功控制了聊天者的用户 ID，那么他们将能够插入 XSS 有效载荷，并以受害者用户身份执行操作。那么攻击者如何才能控制用户 ID 呢？

Etherpad 还具有处理多种格式的导出 / 导入功能，包括基于 JSON 的自定义格式。这种格式的文件可以包含键盘内容、它的修订历史和所有相关的聊天消息。然后可以通过导入这样的文件来创建键盘的副本。示例导出文件如下所示：

example.etherpad

```
{
    "pad:1": {
        "chatHead": 0
    },
    "pad:1:chat:0": {
        "text": "Hello World!",
        "userId": "aE45C6209"
    }
}
```

某些值在导入期间会被验证，但聊天消息的用户 ID 将按原样使用。由于导入功能默认启用，攻击者可以使用该功能创建一个带有用户 ID 的聊天消息键盘，用户 ID 由任意数据组成。

当该数据包含 HTML 标记时，然后将标记插入到 DOM 中，DOM 将执行任何内联 JavaScript 代码。因此，攻击者能够将恶意 JavaScript 代码注入聊天记录，然后在访问键盘时在管理员的浏览器中执行该代码。这使攻击者能够在管理员的浏览器上下文中发起进一步的攻击请求。

**插件管理中的参数注入 (CVE-2021-34816)**

Etherpad 还具有一个管理区域，可供管理员用户使用。它允许他们管理插件、编辑设置和查看系统信息。

管理员安装插件时，带有插件名称的消息会通过 WebSocket 连接发送到后端。后端然后安装与该名称对应的 NPM 包：

src/static/js/pluginfw/installer.js

```
49    exports.install = async (pluginName, cb = null) => {
 …      // ...
52      try {
 …        // ...
56        await runCmd(['npm', 'install', /* ... */ pluginName]);
57      } catch (err) {
 …        // ...
61      }
 …      // ...
66    };
```

在第 56 行，插件名称直接被用作 npm install 系统命令的参数，没有进行任何验证或过滤。这使得攻击者可以从 NPM 存储库中指定恶意包，或者仅使用指向攻击者服务器上包的 URL。

攻击者可以制作一个挂接到 Etherpad 内部的插件，例如创建一个后门 API 端点，或者只使用一个带有 post-install 脚本的包，该脚本将在安装包后立即执行。因此，攻击者可以执行任意代码和系统命令来完全破坏 Etherpad 实例及其数据。

总结  



---------

总而言之，当这两个漏洞被组合利用时，攻击者可以先使用 XSS 接管管理员的客户端，然后通过安装其所控制的插件来访问服务器。

![](https://mmbiz.qpic.cn/mmbiz_png/RQoDdorCu0V5znWFiaMBVWiaibdvAvmGeUvfC5LJ60x1Kq5wiaQ5UtMKEDcwQJ3ibicBdGBKxGs1V2AuZcg3ISoDto1g/640?wx_fmt=png)

  

END

  

![](https://mmbiz.qpic.cn/mmbiz_png/DQk5QiaQiciakarCFnYafgYGpNRiaX2oibtiawYX92ytrKp9MpmQeOqARcreRBybBX1fDbv2guZxExicn7f0wn2dkVwqw/640?wx_fmt=png)

好文！必须在看