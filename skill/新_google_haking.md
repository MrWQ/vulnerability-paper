\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzI2ODU2MjM0OA==&mid=2247488247&idx=1&sn=d823180453143d07843dcf31fc5636ea&chksm=eaece834dd9b61226d85a1302f6c9fac2b00ba7c86046a7802e22f404ec5eb21d29418a6bb81&mpshare=1&scene=1&srcid=1023EpULdxuKfKNteCopcRa5&sharer\_sharetime=1603413102212&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=10b5f81a683662230b882237e74e494a9fc9d5bef8d63d2105bb34e7b2b53949d62aa304f953e3b1159687bd54a4b9cef76c634a9c188aa7fecbc6c319a84a911353bc9dce2e2dfa0c4ce8ca3b574955aac2c0b6cca4a7ec454d54a64ee06633a474a01153477943303fab102d40075b312d3db02642c5e6c9d03ac50d7c4cbc&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=AXtIRODau%2FiYpDZw31NwGNY%3D&pass\_ticket=MIC5Ar%2FikzMcOH1F8HNnc411WxyFMo1Kw3L353SY3XmezYiEUuovrlDORbkreA49&wx\_header=0)

****文章源自 - 投稿****

**作者 - kong**

**扫描下方二维码进入社区：**

**![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnK3Fc7MgHHCICGGSg2l58vxaP5QwOCBcU48xz5g8pgSjGds3Oax0BfzyLkzE9Z6J4WARvaN6ic0GRQ/640?wx_fmt=png)**

**基础语法:**

**逻辑与：and  
**

**逻辑或：or 、|**

**逻辑非：-**

**完整匹配：” 关键词”**

**通配符：\* ?**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png)****

**骚操作语法：**

**intitle: 搜索网页标题中包含有特定字符的网页。例如输入 “intitle: cbi”，这样网页标题中带有 cbi 的网页都会被搜索出来。  
**

**inurl：搜索包含有特定字符的 URL。例如输入 “inurl:cbi”，则可以找到带有 cbi 字符的 URL。**

**intext: 搜索网页正文内容中的指定字符，例如输入 “intext:cbi”。这个语法类似我们平时在某些网站中使用的“文章内容搜索” 功能。**

**filetype: 搜索指定类型的文件。例如输入 “filetype:cbi”，将返回所有以 cbi 结尾的文件 URL。**

**site：找到与指定网站有联系的 URL。例如输入 “Site：imshixu.com”。所有和这个网站有联系的 URL 都会被显示。**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png)****

**指定目标包含后台的页面：**

**示例 ：**

**site:".com" inurl:/admin intext: 后台管理系统 intitle:login** 

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png)****

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnJ3ZdEsD97giaKkQfNRNZZFrIDK3ROIjSOL5ZxM13aW1Dqsh3VPDDhFcl7nVZqh5sRXNxC9M9PNdRg/640?wx_fmt=png)

**搜索目标是否有列目录：**

**示例：**

**site:".com" intext:index of / | ../ | Parent Directory**  

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png)****

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnJ3ZdEsD97giaKkQfNRNZZFr7icUbSPe5lEDeqL1VkYTFzh3DzJyKdCxdmAIlbHkoJdkZgHagIt20EQ/640?wx_fmt=png)

**related: 列出所有和查询网页类似的网页。**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png)****

![](https://mmbiz.qpic.cn/mmbiz_png/ia3Is12pQKnJ3ZdEsD97giaKkQfNRNZZFriaSs38bJvtYYSmWYSIp63IHadnQvsYrnvliaibd5HB9pVDomk22PD6asA/640?wx_fmt=png)

**allinanchor****: anchor 是一处说明性的文字，它标注说明了这个链接可能跳转到其它的网页或跳转到当前网页的不同地方。当我们用 allinanchor 提交查询的时候，Google 会限制搜索结果必须是那些在 anchor 文字里包含了我们所有查询关键词的网页。例 \[allinanchor: best museums Sydney\] , 提交这个查询，Google 仅仅会返回在网页 anchor 说明文字里边包含了关键词”best” “museums” 和”Sydney” 的网面**

**allintext****: 当我们用 allintext 提交查询的时候，Google 会限制搜索结果仅仅是在网页正文里边包含了我们所有查询关键词的网页。例 \[allintext: travel packing list\], 提交这个查询，Google 仅仅会返回在一个网页包含了三个关键词”travel” “packing” 和”list”的网页。**

**allintitle****: 当我们用 allintitle 提交查询的时候，Google 会限制搜索结果仅是那些在网页标题里边包含了我们所有查询关键词的网页。例 \[allintitle: detect plagiarism\]，提交这个查询，Google 仅会返回在网页标题里边包含了”detect” 和”plagiarism”这两个关键词的网页。**

**allinurl****: 当我们用 allinurl 提交查询的时候，Google 会限制搜索结果仅是那些在 URL(网址)里边包含了我们所有查询关键词的网页。例 \[allinurl: google faq\]，提交这个查询，Google 仅会返回在 URL 里边包含了关键词”google” 和”faq”的网页，象** **http://www.****google.com/help/faq.htm****l** **等的网页。**

**author****: 当我们用 author 进行查询的时候，Google 会限制返回结果仅仅是那些在 Google 论坛里边，包含了特定作者的新闻文章。在这里，作者名可以是全名，也可以是一部分或邮件地址。例 \[children author:john author:doe\] 或\[children author:****doe@someaddress.com****\] 返回结果将是作者 John Doe 或是** **doe@someaddress.com** **写的，关于包含关键词 children 的文章。**

**bphonebook****: 用 bphonebook 进行查询的时候，返回结果将是那些商务电话资料。**

**cache****: 提交 cache:url ，Google 会显示当前网页的快照信息，从而替换网页的当前信息。例 \[cache:****Electronic Frontier Foundation****\]，提交这个查询，Google 会返回所有抓取的关于** **Electronic Frontier Foundation** **的网页快照信息。在显示的网页快照信息里边，Google 会高亮显示查询关键词。(在 cache: 和 URL 之间不能有空格)**

**datarange****: 当我们使用 datarange 进行查询的时候，Google 会将查询结果限制在一个特定的时间段内，这个时间相对于网站来说，是按网站被 google 收录的时间算的。例　"Geri Halliwell" "Spice Girls" daterange:2450958-2450968　。这里的时间日期格式是按天文学的儒略日。(这个搜索语法 Google 并不推荐使用，因为它会返回一些莫名其妙的东西)**

**define****: 当我们用 define 进行查询的时候，Google 会返回包含查询关键词定义的网面。例 \[define: blog\]，这个查询将会返回 Blog 的定义。**

**ext****: 这是一个没有证实的语法，可以用于 filetype: 查找扩散名为 ext 的文件。**

**filetype****: 当我们在查询里边包含 filetype: 扩展名的时候，Google 会限制查询结果仅返回特定文件类型的网页。例 \[资产评估　filetype:pdf\]，这个查询将会返回所有文件类型为 pdf 的资产评估信息。**

**group****: 当我们用 group 查询的时候，Google 会限制我们的论坛查询结果仅是某几个固定的论坛组或是某些特定主题组的新闻文章。例 \[sleep group:misc.kids.moderated\]，提交这个查询，Google 仅会返回在用户组 misc.kids.moderated 里边包含了查询关键字”sleep” 的文章。**

**inanchor****: 当我们用 inanchor 提交查询的时候，Google 会限制结果是那些在网页 anchor 链接里边包含了查询关键词的网页。例 \[restaurants inanchor:gourmet\]，提交这个查询，Google 会查询那些在 anchor 信息里包含了关键词”restaurants” 和关键词”gourmet”的网页。**

**info****: 列出某网站在 google 上存在那些资料。**

**robots.txt   可查看有那些目录，文档不希望被存取**

**"robots.txt" "disallow:" filetype:txt**

**insubject****: 当我们用 insubject 进行查询的时候，Google 会限制论坛搜索结果仅是那些在主题里边包含了查询关键词的网面。\[insubject:"falling asleep"\]，提交这个查询，Google 会返回在文章主题里边包含了”falling asleep” 的文章。**

**link****: 当我们使用 link:URL 提交查询的时候，Google 会返回跟此 URL 做了链接的网站。例 \[link:****back****\]，提交这个查询，我们将得到所有跟** **HugeDomains.com** **这个网站做了链接的网站。(link 是个单独的语法，只能单独使用，且后面不能跟查询关键词，跟能跟 URL)**

**location****: 当我们提交 location 进行 Google 新闻查询的时候，Google 仅会返回你当前指定区的跟查询关键词相关的网页。例 \[queen location:canada\]，提交这个查询，Google 会返回加拿大的跟查询关键词”queen” 相匹配的网站。**

**movie****: 当我们用 movie 提交查询的时候，Google 会返回跟查询关键词相关的电影信息。(当前只支持英文 Google)**

**phonebook****: 当我们用 phonebook 进行查询的时候，Google 会返回美国当地跟查询关键词相关的电话信息。(使用 phonebook 的时候需要指定详细的州名和地点名) 例，\[phonebook:smith ca\]**

**rphonebook****: 这个查询用来搜索美国当地跟查询关键词相关的住宅电话信息。**

**safesearch****: 用 safesearch 提交查询的时候，Google 会过滤你搜索的结果，其中过滤的内容可能包括一些色情的，暴力，赌博性质的，还有传染病毒的网页。但是它不是百分之百确保安全的。例，\[safesearch:breasts\]。**

**source****: 当用 source 提交查询的时候，Google 新闻会限制我们的查询仅是那些我们指定了特定 ID 或新闻源的网址。例 \[election source:new\_york\_times\]，提交这个查询，Google 将会显示纽约时报包含了查询关键词”election” 的相关文章。(我们也可以通过 Google news 高级搜索完成查询)**

**stocks****: 当我们用 stocks 提交查询的时候，Google 会返回跟查询关键词相关的股票信息，这些信息一般来自于其它一些专业的财经网站。**

**store****: 当我们用 store 提交查询的时候，Google Froogle 仅会显示我们指定了 store ID 的结果。例 \[polo shirt store:llbean\]，提交这个查询，仅会搜索商店 L. L. Bean. 跟关键词”polo” “shirt” 相关的结果。(只支持英文 Google)**

**weather****: 当我们用 weather 提交查询的时候，如果我们指出一个 Google 可以识别的地区或城市，Google 会返回该地区或城市当前的天气状况。**

**extension****:  指定扩展名搜索**

**例如 extension:properties jdbc**

****![](https://mmbiz.qpic.cn/mmbiz_png/Ljib4So7yuWgiazacZwcozhIIJkbibEWTcfRmJfpFw8RCkn9iaZOyT4YJ5JCqCIvRvCLC5RznuKbdPrlfXuXPkevEQ/640?wx_fmt=png)****

**通知！**

**公众号招募文章投稿小伙伴啦！只要你有技术有想法要分享给更多的朋友，就可以参与到我们的投稿计划当中哦~ 感兴趣的朋友公众号首页菜单栏点击【商务合作 - 我要投稿】即可。期待大家的参与~**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/ia3Is12pQKnKRau1qLYtgUZw8e6ENhD9UWdh6lUJoISP3XJ6tiaibXMsibwDn9tac07e0g9X5Q6xEuNUcSqmZtNOYQ/640?wx_fmt=jpeg)**

**记得扫码**

**关注我们**