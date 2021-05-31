> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/omgxa4Z0jAD95rdNiSxIog)

前言
==

官方已于 5 月 14 日上午将代码整合进官方项目~ 所以，友友们只需要搭建好自己的 Gotify 然后直接加载官方的 session_notifier 插件就可以了~

**但是，**官方整合的代码是我按照官方要求修改后的代码，与下文贴出代码有所差别

> 重点是 HTTPS 的实现，目前不知道是证书签发的问题还是其他原因，无法完成正常的 HTTPS 认证过程，需要屏蔽证书认证，而官方表示 “I don’t think we want to be disabling SSL by default. This could be it’s own option though.” 因此给官方提交的代码是一个证书路径，不使用证书时，通过 HTTP 请求实现
> 
> 具体流程各位可以看一下代码啦~

各位大佬各取所需。

如果有能够帮忙解决证书问题的，直接评论或者私信我都可以，感激不尽！

0x00 前言
=======

老早的时候就看网上各路大佬晒过自己的 “xx.xx.xx.xx 主机已上线” 的上线提醒，好家伙当时就羡慕的不得了。但是一直没得机会研究研究，后来因为自己有别的提醒需求，于是去四方寻找了一下比较成熟简单的解决方案。

偶然之中发现了这个简单好使的解决方案，但是好像并没有人写过相关方面的介绍，然后就自己写一下吧。

重在分享，大家有更好的想法可以一起交流。

### 现有解决方案

目前大家比较熟知的类似的解决方案应该有 **Server 酱**，而 MSF 之前也有一位表哥 @cn-kali-teamCommit 了一个**钉钉 Webhook** 机器人的方法。大家有兴趣的可以去看看官方的 Commit 记录，此处特别感谢这位大佬。我此次的代码也 pull 给官方了，希望能早日 merge 进去吧鹅鹅鹅。

但是这些都会借助第三方的服务（虽然你的云服务器也是第三方服务鹅鹅鹅），但是为了尽量减少第三方的服务，我又去四处寻找别的方法。

那么最终我也找到了这个我个人很喜欢的解决方案：**Gotify**

0x01 Gotify 简介
--------------

关于 Gotify 我可能后续会再写一篇文章专门介绍 Gotify。

Gotify 是 “A self-hosted push notification service.” 一个自主推送通知服务。一个开源、Web、简易、快速、便于部署的消息通知服务，使用 Go 语言编写，这也大概就是为什么叫做 Gotify，即“Go+Notify”。

官方 Github：https://github.com/gotify

官方主页：https://gotify.net/

重点需要使用的几个项目是 server、android、cli、website。另外两个看名字就很好理解了（安卓分支仅为客户端），简单说一下 server 和 website，server 是官方二进制编译的内容，从 release 下载或自行编译后直接运行即可，website 是借助 npm 进行编译运行的，需要本身环境的 nodejs 支持。

我们此处的演示均以 server 的 release 为例。

这是我部署之后的页面

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAObmficObbfqEwFib3ZIh26rGLYJA9s5icVgBC0wUJI3C3eZ4xicNQuSACrA/640?wx_fmt=jpeg)

同时因为官方提供安卓的支持，可以前往 https://github.com/gotify/android/releases / 下载安卓版本多端协同。

【安卓的后台服务对电量和流量消耗真的很小很小很小，可以忽略不记鹅鹅鹅】

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOMhbhJkGRb3pgvDDsV7lPzkIBxibqFrcgShqqdj9p9iadmXsMZQ5C7D7A/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOSiaL1EO6Km5xUmoINDazs5VKCHP8olic6Qd5Ttne7jicp0L67hfG80kaQ/640?wx_fmt=jpeg)

以上是主页面和通知栏效果

0x02 Gotify 部署
--------------

下面的所有部署方案采用傻瓜式操作，如果有额外需求，请移步 官方文档。

前往 https://github.com/gotify/server/releases 下载对应的二进制文件，解压后直接运行。![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOtV0a6XKTUWOO3KdlRiaxdxiaY2chbyIqukHXahcPuISyibXVqGCZ1d8Xw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAO2ZPZloHpzTlRbctS4lUXMPKcUic19oULhdUHmDmiapduEyJGFlML1EgA/640?wx_fmt=jpeg)

运行后会在你本地 /etc/gotify/config.yml 自动创建默认配置文件

> 注：gotify 运行时会在
> 
> ./config.yml
> 
> /etc/gotify/config.yml
> 
> 以上两个位置寻找配置文件并自动加载
> 
> 没有配置文件时，会自动在 / etc/gotify/config.yml 创建默认配置文件

此时可以停掉服务，修改自己的配置文件。![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOQKKcyjBfu57FSyQ7YqR9AqdkpmVoRVSFMtDpMkHPYXnrhg2woHibwbA/640?wx_fmt=jpeg)

这里的每一项基本都带有注释，我就不一一解释了，重点说一下关于 **SSL** 的选项。

启用 SSL 时直接在 **enabled** 设置为 **true** 即可，同时如果要**禁用 HTTP Plain** 功能，将第二个 SSL 选项重定向设为 **true** 即可，反之设为 **false** 就可以实现 https 和 http 的共用。

SSL 的证书可以自行生成，我本地测试时以下两种方法生成的证书都是可用的：

https://wangbin.io/blog/it/https-ca.html

https://www.cnblogs.com/asker009/p/13354656.html?utm_source=tuicool

生成后的证书和密钥文件的对应路径直接如图写在 **certfile** 和 **certkey** 即可。

> 【注意：如果使用了 HTTPS，那么在安卓登陆时需要选择**不验证 https** 或将生成的 **server.crt** 拷贝至手机并加载，即可实现 HTTPS 登录】
> 
> 【二次注意：部分脚本，如 python，登录时如果需要进行 https 验证，那么需要 ca-chain(certificate chain file) 进行验证，生成方法如下：https://jamielinux.com/docs/openssl-certificate-authority/create-the-intermediate-pair.html 从头到尾按照文档执行对应命令，即可生成 ca-chain.pem 证书文件】

由于本篇文章重点在于和 MSF 联动，其余参数这里就不做说明了，大家可以根据官方文档或个人需求进行修改。

将程序放入后台运行的方法很多，在此也不做过多赘述，有需要的各位自行百度哈哈~

先说一下 Gotify 的接口格式

> http://yourIP/message?token=
> 
> POST 方式发送 json 数据
> 
> `{ "message": "推送内容", "priority": 2, "title": "推送标题"}`

首先运行服务，然后登录到 web 页面，默认账密 admin/admin。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOeAvbOBQt4Z3FMGKClyMShWyD6RPz3NW93NxiaEnibiafMwCWRrH6DC6Cg/640?wx_fmt=jpeg)

进入 **USERS** 页面，我们就可以创建新的用户，并且决定此用户是否具有管理员权限，点击对应账户后面的 “笔” 按钮即可直接修改对应账户的密码。【一定记得改你的 admin 嗷】

然后我们需要访问 **APPS**，创建一个对应的 **Application**，用来发送我们的推送消息。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAO2fCRlMXQ7IriciaO4ZBeHSdicaIGfsNd5S9iahXAzgEkVZYUvKG0yQv9oQ/640?wx_fmt=jpeg)

流程图如上，这里创建后我们可以获得到一个 **token**，然后我们利用这个 **token** 实现信息的发送。如果你想区分不同类型的推送，那么可以创建多个 **Application**，利用不同的 **token** 进行分类。

同时每个 **token**，我们都可以点击那个上传按钮上传不同的**头像**，推送发出后即可快速区分。

如果我们需要删除历史推送，可以以用户身份删除，或在 **Clients** 里新建一个 **DELETE_TOKEN**，用这个 **token** 来进行删除历史推送。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOheAjgbxlv9gPrtz9LW4ianpcSvghNEYlozLcmRgY1OSQ9Eaeeo0DSXQ/640?wx_fmt=jpeg)

这里我自己写的有一个自己用的半成品 python 脚本，各位按需自行参考取用【代码写的烂，轻喷轻喷】

```
#!/usr/bin/py3.8
#-*- coding:utf-8 -*-
import argparse
from requests import post,get,delete
from sys import argv# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class gotify():
    """gotify_http
    """
    def __init__(self, title = 'defaultTitle', message = 'defaultMsg', priority = 0, 
        host = '0.0.0.0', token = 'app_token'):
        self.title = title
        self.message = message
        self.priority = priority
        self.host = host
        self.token = token

    def set_host(self, host):
        self.host = host

    def set_token(self, token):
        self.token = "?token=" + token

    def send(self):
        self.params={
            "title":self.title,
            "message":self.message,
            "priority":self.priority
        }

        res = post(url = "https://{}/message?token={}".format(self.host,self.token), data=self.params, verify="/root/cert/ca-chain.cert.pem")
        print(res.status_code)

    def delete(self):
        self.headers = {
            'Host':self.host,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept':'application/json, text/plain, */*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate',
            'X-Gotify-Key':self.token,
            'Origin':'https://'+self.host,
            'DNT':'1',

            'Connection':'close',
            'Referer':'https://{}/'.format(self.host)
        }
        res = delete(url ="https://{}/message".format(self.host), headers=self.headers, verify = "./ca-chain.cert.pem")
        print(res.status_code)

if __name__ == '__main__':
    # print(len(argv))
    parser = argparse.ArgumentParser(description='Gotify Controller')
    parser.add_argument('-t','-title',type=str, default='defaultTitle',help='Title')
    parser.add_argument('-m','-message',type=str, default='Default Message',help='Message')
    parser.add_argument('-l','-level',type=int, default=0,help='Msg Priority, 0-10, min:<1, low:1-3, normal:4-7, high:>7')
    parser.add_argument('-host',type=str, default='0.0.0.0')
    parser.add_argument('--token-push',type=str, default='app_token')
    parser.add_argument('--token-del',type=str, default='delete_token')
    args = parser.parse_args()
    print(args)
    gotify(args.t,args.m,args.l,args.host,args.token_push).send()
    # gotify(host = args.host,token = args.token_del).delete()

```

官方的推送案例如下：https://gotify.net/docs/more-pushmsg

```
{
    "message": "Well hello there.",
    "priority": 2,
    "title": "This is my title"
}

```

message 和 title 就不解释了，priority 是 gotify 引入的推送消息分级机制。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOs1N5AbBZbCSJBicJF8jTeoVawZ1RqFrIDzlCDC8NKB7cjiana8vvD3ZQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOpFfQumE8RzBMJGwGiaXElE0Sp7XlD1QXwyz6apic6x0WbrOE2NxVDHibw/640?wx_fmt=jpeg)

在安卓上我们也可以调整其不同等级推送的提醒方式，根据各自手机系统的不同，设置可能略有不同，但是基本可以设置**是否是静默提醒**，**不同提醒音**，**是否震动**等。（因为是直接推送到系统通知栏的，所以手环或者手表应该也可以收到，但是我没有这些设备（之前的三星 watch active 让我给卖了）所以嗯…… 没测试鹅鹅鹅）

这里的等级其实对浏览器也是有效的，但是官方并没有说而已，因为在浏览器我们能够有效区分的只有声音，当具有高优先级的推送到达时，电脑会有声音提醒。

0x03 MSF 插件修改
-------------

参看之前那位表哥的代码，本质上是魔改了对钉钉 Webhook 的设置。

我们需要修改 **/opt/metasploit-framework/embedded/framework/plugins/session_notifier.rb** 文件以实现 msf 的推送请求【注：个人建议拷贝一份进行修改，并重命名，因为每次更新都会从官方获取源码并覆盖掉同名文件，会导致你的修改直接丢失…… 我之前就丢过一份…… 当时人都快裂开了……】

链接地址： 

https://github.com/rapid7/metasploit-framework/pull/15125/files

此处贴出的是 github 代码对比，大家可以参 zhao 考 chao 一下

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOV8xA4sswFDAuP4J2kVeZ3UCERTNC15YsHBSRucr2bd0NyChtEJG21w/640?wx_fmt=jpeg)

增加全局变量 **gotify_address gotify_ssl**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOzOnFFwKibqH5D2B8WJMTdBjxaiakibUNMuJjNQGnshiaNeucCrQlIZdx5w/640?wx_fmt=jpeg)

增加 plugin 选择模块

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOZEz2UQJqm8f6hXF5pxRtbn2O6GF6Gm9X1ReJbnr1bFsK3SfqG5utIg/640?wx_fmt=jpeg)

增加 gotify 推送地址设置函数

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOYumPRRECXW9icMBEgZsawDHUXFHMcxeFwl5ZCVt98uqmibnrU1HwCFrg/640?wx_fmt=jpeg)

和钉钉推送提醒并行

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOicr5UzGsw4V3dewicwmltLkaMFrQfogOZuWmxjWS0llhIIYvzibfXjHcw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOBZvqDicU1VgspaLy9Ovu2EWiaW68klEYBTckVYUwulLgMVfvugicQEaNA/640?wx_fmt=jpeg)

设置保存添加 gotify 配套功能

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOTDkWicLRibbKZNJAM1GQicARDfroria5QO9BtaPvnvH29jrRo92aQvic86Q/640?wx_fmt=jpeg)

实现推送函数的主体

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAO2ib2vib77xGiaydarL6XiagicdPWlKicM79Q88kCw0oKfODeIHqtdiaTibLvfQ/640?wx_fmt=jpeg)

调用发送函数

整套的代码在这里↓

```
require 'net/https'
require 'net/http'
require 'uri'
module Msf
  class Plugin::SessionNotifier < Msf::Plugin

    include Msf::SessionEvent

    class Exception < ::RuntimeError; end

    class SessionNotifierCommandDispatcher

      include Msf::Ui::Console::CommandDispatcher

      attr_reader :sms_client
      attr_reader :sms_carrier
      attr_reader :sms_number
      attr_reader :smtp_address
      attr_reader :smtp_port
      attr_reader :smtp_username
      attr_reader :smtp_password
      attr_reader :smtp_from
      attr_reader :minimum_ip
      attr_reader :maximum_ip
      attr_reader :dingtalk_webhook
      attr_reader :gotify_address
      attr_reader :gotify_ssl

      def name
        'SessionNotifier'
      end

      def commands
        {
          'set_session_smtp_address'       => 'Set the SMTP address for the session notifier',
          'set_session_smtp_port'          => 'Set the SMTP port for the session notifier',
          'set_session_smtp_username'      => 'Set the SMTP username',
          'set_session_smtp_password'      => 'Set the SMTP password',
          'set_session_smtp_from'          => 'Set the from field of SMTP',
          'set_session_mobile_number'      => 'Set the 10-digit mobile number you want to notify',
          'set_session_mobile_carrier'     => 'Set the mobile carrier of the phone',
          'set_session_minimum_ip'         => 'Set the minimum session IP range you want to be notified for',
          'set_session_maximum_ip'         => 'Set the maximum session IP range you want to be notified for',
          'set_session_dingtalk_webhook'   => 'Set the DingTalk webhook for the session notifier (keyword: session).',
          'set_session_gotify_address'     => 'Set the Gotify address for the session notifier',
          'set_session_gotify_ssl'         => 'Set whether use ssl for Gotify push or not (1/0)',
          'save_session_notifier_settings' => 'Save all the session notifier settings to framework',
          'start_session_notifier'         => 'Start notifying sessions',
          'stop_session_notifier'          => 'Stop notifying sessions',
          'restart_session_notifier'       => 'Restart notifying sessions'
        }
      end

      def initialize(driver)
        super(driver)
        load_settings_from_config
      end

      def cmd_set_session_smtp_address(*args)
        @smtp_address = args[0]
      end

      def cmd_set_session_smtp_port(*args)
        port = args[0]
        if port =~ /^\d+$/
          @smtp_port = args[0]
        else
          print_error('Invalid port setting. Must be a number.')
        end
      end

      def cmd_set_session_smtp_username(*args)
        @smtp_username = args[0]
      end

      def cmd_set_session_smtp_password(*args)
        @smtp_password = args[0]
      end

      def cmd_set_session_smtp_from(*args)
        @smtp_from = args[0]
      end

      def cmd_set_session_mobile_number(*args)
        num = args[0]
        if num =~ /^\d{10}$/
          @sms_number = args[0]
        else
          print_error('Invalid phone format. It should be a 10-digit number that looks like: XXXXXXXXXX')
        end
      end

      def cmd_set_session_mobile_carrier(*args)
        @sms_carrier = args[0].to_sym
      end

      def cmd_set_session_minimum_ip(*args)
        ip = args[0]
        if ip.blank?
          @minimum_ip = nil
        elsif Rex::Socket.dotted_ip?(ip)
          @minimum_ip = IPAddr.new(ip)
        else
          print_error('Invalid IP format')
        end
      end

      def cmd_set_session_maximum_ip(*args)
        ip = args[0]
        if ip.blank?
          @maximum_ip = nil
        elsif Rex::Socket.self.dotted_ip?(ip)
          @maximum_ip = IPAddr.new(ip)
        else
          print_error('Invalid IP format')
        end
      end

      def cmd_set_session_gotify_address(*args)
        webhook_url = args[0]
        if webhook_url.blank?
          @gotify_address = nil
        elsif !(webhook_url =~ URI::DEFAULT_PARSER.make_regexp).nil?
          @gotify_address = webhook_url
        else
          print_error('Invalid gotify_address')
        end
      end

      def cmd_set_session_gotify_ssl(*args)
        ssl_options = args[0]
        if ssl_options == '1'
          @gotify_ssl = 1
          print_status('Set Gotify ssl_mode ON!')
        elsif ssl_options == '0'
          @gotify_ssl = 0
          print_status('Set Gotify ssl_mode OFF!')
        end
      end

      def cmd_set_session_dingtalk_webhook(*args)
        webhook_url = args[0]
        if webhook_url.blank?
          @dingtalk_webhook = nil
        elsif !(webhook_url =~ URI::DEFAULT_PARSER.make_regexp).nil?
          @dingtalk_webhook = webhook_url
        else
          print_error('Invalid webhook_url')
        end
      end

      def cmd_save_session_notifier_settings(*_args)
        save_settings_to_config
        print_status('Session Notifier settings saved in config file.')
      end

      def cmd_start_session_notifier(*_args)
        if session_notifier_subscribed?
          print_status('You already have an active session notifier.')
          return
        end

        begin
          framework.events.add_session_subscriber(self)
          if validate_sms_settings?
            smtp = Rex::Proto::Sms::Model::Smtp.new(
              address: smtp_address,
              port: smtp_port,
              username: smtp_username,
              password: smtp_password,
              login_type: :login,
              from: smtp_from
            )
            @sms_client = Rex::Proto::Sms::Client.new(carrier: sms_carrier, smtp_server: smtp)
            print_status('Session notification started.')
          end
          if !dingtalk_webhook.nil?
            print_status('DingTalk notification started.')
          end
          if !gotify_address.nil?
            print_status('Gotify notification started.')
          end
        rescue Msf::Plugin::SessionNotifier::Exception, Rex::Proto::Sms::Exception => e
          print_error(e.message)
        end
      end

      def cmd_stop_session_notifier(*_args)
        framework.events.remove_session_subscriber(self)
        print_status('Session notification stopped.')
      end

      def cmd_restart_session_notifier(*args)
        cmd_stop_session_notifier(args)
        cmd_start_session_notifier(args)
      end

      def on_session_open(session)
        subject = "You have a new #{session.type} session!"
        msg = "#{session.tunnel_peer} (#{session.session_host}) #{session.info ? "\"#{session.info}\"" : nil}"
        notify_session(session, subject, msg)
      end

      private

      def save_settings_to_config
        config_file = Msf::Config.config_file
        ini = Rex::Parser::Ini.new(config_file)
        ini.add_group(name) unless ini[name]
        ini[name]['smtp_address']     = smtp_address
        ini[name]['smtp_port']        = smtp_port
        ini[name]['smtp_username']    = smtp_username
        ini[name]['smtp_password']    = smtp_password
        ini[name]['smtp_from']        = smtp_from
        ini[name]['sms_number']       = sms_number
        ini[name]['sms_carrier']      = sms_carrier
        ini[name]['minimum_ip']       = minimum_ip.to_s unless minimum_ip.blank?
        ini[name]['maximum_ip']       = maximum_ip.to_s unless maximum_ip.blank?
        ini[name]['dingtalk_webhook'] = dingtalk_webhook.to_s unless dingtalk_webhook.blank?
        ini[name]['gotify_address']   = gotify_address.to_s unless gotify_address.blank?
        ini[name]['gotify_ssl']       = gotify_ssl
        ini.to_file(config_file)
      end

      def load_settings_from_config
        config_file = Msf::Config.config_file
        ini = Rex::Parser::Ini.new(config_file)
        group = ini[name]
        if group
          @sms_carrier      = group['sms_carrier'].to_sym     if group['sms_carrier']
          @sms_number       = group['sms_number']             if group['sms_number']
          @smtp_address     = group['smtp_address']           if group['smtp_address']
          @smtp_port        = group['smtp_port']              if group['smtp_port']
          @smtp_username    = group['smtp_username']          if group['smtp_username']
          @smtp_password    = group['smtp_password']          if group['smtp_password']
          @smtp_from        = group['smtp_from']              if group['smtp_from']
          @minimum_ip       = IPAddr.new(group['minimum_ip']) if group['minimum_ip']
          @maximum_ip       = IPAddr.new(group['maximum_ip']) if group['maximum_ip']
          @dingtalk_webhook = group['dingtalk_webhook']       if group['dingtalk_webhook']
          @gotify_address   = group['gotify_address']         if group['gotify_address']
          @gotify_ssl       = group['gotify_ssl']             if group['gotify_ssl']
          print_status('Session Notifier settings loaded from config file.')
        end
      end

      def session_notifier_subscribed?
        subscribers = framework.events.instance_variable_get(:@session_event_subscribers).collect(&:class)
        subscribers.include?(self.class)
      end

      def send_text_to_dingtalk(session)
        # https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq/9e91d73c
        uri_parser = URI.parse(dingtalk_webhook)
        markdown_text = "## You have a new #{session.type} session!\n\n" \
        "**platform** : #{session.platform}\n\n" \
        "**tunnel** : #{session.tunnel_to_s}\n\n" \
        "**arch** : #{session.arch}\n\n" \
        "**info** : > #{session.info ? session.info.to_s : nil}"
        json_post_data = JSON.pretty_generate({
          msgtype: 'markdown',
          markdown: { title: 'Session Notifier', text: markdown_text }
        })
        http = Net::HTTP.new(uri_parser.host, uri_parser.port)
        http.use_ssl = true
        request = Net::HTTP::Post.new(uri_parser.request_uri)
        request.content_type = 'application/json'
        request.body = json_post_data
        res = http.request(request)
        body = JSON.parse(res.body)
        print_status((body['errcode'] == 0) ? 'Session notified to DingTalk.' : 'Failed to send notification.')
      end

      def send_text_to_gotify(session)
        # https://gotify.net/docs/more-pushmsg
        uri_parser = URI.parse(gotify_address)
        message_text =
        "Platform : #{session.platform}\n" \
        "Tunnel : #{session.tunnel_to_s}\n" \
        "Arch : #{session.arch}\n" \
        "Info : > #{session.info ? session.info.to_s : nil}"
        json_post_data = JSON.pretty_generate({
          title: "#{session.platform}主机#{session.type}会话上线!",
          message: message_text,
          priority: 10
        })
        http = Net::HTTP.new(uri_parser.host, uri_parser.port)
        if gotify_ssl == 1
          http.use_ssl = true
          http.verify_mode = OpenSSL::SSL::VERIFY_NONE
        end
        request = Net::HTTP::Post.new(uri_parser.request_uri)
        request.content_type = 'application/json'
        request.body = json_post_data
        res = http.request(request)
        body = JSON.parse(res.body)
        print_status((body['priority'] == 10) ? 'Session notified to Gotify.' : 'Failed to send notification.')
      end

      def notify_session(session, subject, msg)
        if in_range?(session) && validate_sms_settings?
          @sms_client.send_text_to_phones([sms_number], subject, msg)
          print_status("Session notified to: #{sms_number}")
        end
        if in_range?(session) && !dingtalk_webhook.nil?
          send_text_to_dingtalk(session)
        end
        if in_range?(session) && !gotify_address.nil?
          send_text_to_gotify(session)
        end
      end

      def in_range?(session)
        # If both blank, it means we're not setting a range.
        return true if minimum_ip.blank? && maximum_ip.blank?

        ip = IPAddr.new(session.session_host)

        if minimum_ip && !maximum_ip
          # There is only a minimum IP
          minimum_ip < ip
        elsif !minimum_ip && maximum_ip
          # There is only a max IP
          maximum_ip > ip
        else
          # Both ends are set
          range = minimum_ip..maximum_ip
          range.include?(ip)
        end
      end

      def validate_sms_settings?
        !(smtp_address.nil? || smtp_port.nil? ||
        smtp_username.nil? || smtp_password.nil? ||
        smtp_from.nil?)
      end

    end

    def name
      'SessionNotifier'
    end

    def initialize(framework, opts)
      super
      add_console_dispatcher(SessionNotifierCommandDispatcher)
    end

    def cleanup
      remove_console_dispatcher(name)
    end

    def desc
      'This plugin notifies you a new session via SMS.'
    end

  end
end

```

直接复制粘贴保存为 **session_gotify.rb** 并置于 **msf 的 plugin 目录**下即可

Ruby 这个语言确实之前了解不多，参考了 github 一位大佬的 examples，很齐全，参考意义很强。

地址在此：https://github.com/augustl/net-http-cheat-sheet

此处由于之前多次尝试时，SSL 的认证无法正常进行，因此直接忽略掉了 SSL 认证。

同时在原有的基础上增加了 SSL 认证功能，通过设置 gotify_ssl 参数，选择是否发送向 HTTPS 地址。之后可能会考虑尝试添加 HTTPS 证书验证的方式进行推送。

保存修改之后就是我们的实际调用阶段了。

0x04 MSF 推送调用
-------------

上一步我们已经说到其实我们魔改的就是一个官方的 plugin。

那么我们直接加载这个 plugin 就可以了。由于官方还未整合这个魔改后的模块，因此我调用的是一个拷贝复件，名为 **session_gotify.rb**

首先在本地机器生成一个 msf 木马，用来测试连接

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAO5VU7Q3FUAI3s95PqLOgbFRNGD6z4xPSl7wvGqfhTxlZzBTKRDibMbQQ/640?wx_fmt=jpeg)

然后我们在 msf 终端配置好监听尝试一下正常连接

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOtqqCJq1hkOibGic5TYVyNUWBsjE68pHicEXKNmQNqzCfsxlF3LxAWOoWw/640?wx_fmt=jpeg)

然后我们加载提醒模块

【2021.5.14 更新，因为官方现已整合该代码，此处直接 **load session_notifier** 即可，如有额外需要也可新建脚本加载】

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOQtX9aPXIicsnpd8X1M7mXaNTDrfQuG8ZBSP5R0rdAnTymb54beqhsIA/640?wx_fmt=jpeg)

接下来我们进行参数设置【因为我之前保存过钉钉 webhook，所以每次加载模块也会自动加载钉钉的设置，此处会看到钉钉也被启动了】

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOlJWGVx1qJD3SrLdvAW24ju7b3ANpia4fic8iauSxiamuzrwWNpuJ2s1JlA/640?wx_fmt=jpeg)

之后我们就可以收到 gotify 给我们发来的提醒

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOUhG8elqZpJnwfGvjeF8mxmOO5M4z8ib4Jnh62yNfDHKQRXz51HoVDiaA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOEoqjwdJIGhkWwUSialPYv89zYFPDH0ZyIHMgtbNFdriacMXutO94tTlg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAOdAic88lbCDmEw1oJITXwAibmv78K3lcokibNhRtVqgQmvnE1Me1INPtLg/640?wx_fmt=jpeg)

如果我们使用的是 HTTPS，那么按照如下设置就可以了

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibdSSiaa0zZNbMhfZtt1oOAObPfuFNdcvDks0BYicSpu1PEYSIWHGvDPnPuiaYGyAgudQvAmaKgbaSAg/640?wx_fmt=jpeg)

到此，我们就可以成功实现基于 Gotify 的 MSF 上线消息提醒。

0x05 结语
-------

Gotify 也可以很方便的用在其他提醒上，CS 上线提醒也 OK，下一篇可能就写 CS 上线了吧哈哈哈~

它的使用范围和场景很广，而且多端同步做的也不错（ios 暂不支持），有想法的朋友真的可以去试试用它做别的一些工作。我平常一直用这个做为我服务器上定时任务的执行结果提醒。

上线提醒确实是很实用的一个功能，gotify 的使用也是一个意外之喜，原本只是为了自动签到啊啥的一些其他脚本挂机，找的一个消息推送软件，刚好又看到了有人说 msf 可以用钉钉 webhook 了，于是按捺不住躁动的心，去翻了翻源码照着修改调试，前后用的时间也不短。

然后就是 SSL 证书生成那一块，好家伙是真折腾，但是那个英文文档写的也是真的棒，有需要的朋友本人强烈建议去读一读看一看。

后续可能会在 Gotify 上搞一些花活，毕竟我觉得这个东西是真的简单好使~

这也是我的第一篇公开博客，之前都是给社团内部写一些的简单的知识介绍短文，如果有不足的地方还希望各位表哥表姐多多建议，轻喷轻喷哈哈

公众号