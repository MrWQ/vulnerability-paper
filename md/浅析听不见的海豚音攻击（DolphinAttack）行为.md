> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/CUjoArHlKQo7Si0wUbRwUQ)

摘要
--

对攻击语音识别系统的研究表明，某些隐藏的语音命令人类无法听见，但是这些声音却可以控制系统。在最近的一些实验中，研究者设计了一个完全听不见的攻击：DolphinAttack，通过将人声负载在高频载波上，可以通过 Siri 使 iPhone 发起 FaceTime 通话。

进一步设想如果手机上的语音助手如果被他人控制，手机上的任何 App 就会被随意运行、打开网站、关闭飞行模式，能够下达开门解锁（已经绑定智能门锁）等命令或是手机偷偷拨打攻击者的电话，变身成为监听器，或是借助获取验证码使手机绑定的银行卡会自动转账到他人名下……,

海豚音攻击” 将上述设想变得可行，并不易察觉。首先，“海豚音攻击” 绕过智能设备的声纹识别系统，启动智能语音系统；然后，使用人耳听不到的超声波信号，注入控制指令，让被攻击的设备执行相应操作，从而实现包含但不限于上述场景所描述的一系列攻击。

随着人工智能 (AI) 的快速发展和应用，智能语音成为一种越来越普遍的人机交互方式，用户只需要通过对话的方式即可控制智能设备进行相应操作，免去了手动输入等方式的繁琐过程。

目前，几乎所有的科技巨头都有自己主打的智能语音系统，包括苹果公司的 Siri、亚马逊的 Alexa 和 Echo、谷歌公司的 Google Assistant、阿里巴巴的天猫精灵、京东的叮咚以及手机语音助手 APP 等, 智能语音系统（如各主流智能语音助手）已使各种系统成为语音可控系统！

然而，人们在享受这些智能语音助手带来的便利的同时，对其中的安全问题却没有给予足够的重视。实际上，与其他产品一样，智能语音系统在软硬件上存在各类安全问题，而且这些安全问题一旦爆发，导致的后果也将非常严重。

**一、语音识别控制系统及其风险分析**
--------------------

“海豚音攻击（DolphinAttack）” 原理就是通过将人类发布的语音命令频率转换成为**超声波频率（**频率高于 20kHz），即将人类的声音搭载在人耳无法听见的高频载波上，这些高频载波可以被麦克风识别，并转换为系统指令，达到操纵被攻击系统的目的。

一个典型的语音控制系统主要包括三个子系统：语音捕获、语音识别和命令执行。如图 1 所示，语音采集系统记录的声音是模拟信号，需要经过信号放大，信号过滤和数字化，最后变成数字信号被传递到语音识别系统。语音识别系统可以将数字信号转化为文本，然后转化为命令执行系统可识别的命令。如果这个命令是系统预先定义的可识别的命令，那么系统将会执行相应的操作。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icW7mDRGfJmibGkaWjSC1qTstZnr1TQnp91qRxlfcSyAH47k9H8penNU8GXy0FfkQpNJ3jlTLmduDg/640?wx_fmt=jpeg)

图 1

“海豚音攻击” 的是麦克风本身的硬件漏洞。一般人能听到的语音频率在 20Hz-20kHz 之间，麦克风本应该只记录人可以听见的声音，即 f<20kHz，但出于提高麦克风性能和减小体 积的需要，麦克风实际必然能捕获到高频信号，即可以接收 f>20kHz 的信号。

**二、安全问题或攻击事件描述**
-----------------

智能语音系统包括苹果的 Siri、谷歌的 Google Assistant、亚马逊的 Alexa、三星的 SVoice、微软的 Cortana 以及华为的 HiVoice 等，被越来越多的搭载在各种系统上。这些语音系统可以识别各种语言，将语言转化为系统可识别的指令，完成系统操作。

我们以 siri 为例，“海豚音攻击”不需要攻击者对设备有物理上的实质接触，也不需要在系统中植入后门或者安装恶意软件，当 iPhone 所有者设置可以通过 “Hey,Siri” 唤醒黑屏状态下的 iPhone 时，攻击者便可以完成“海豚音攻击”。

攻击者可以事先录下 iPhone 所有者讲的相关语句，例如 “喝（he）”、“西（xi）”、“瑞（rui）”、“谁（shei）”。通过谷歌的 TTS 的技术，攻击者将这些词语的相关音节合成 “Hey,Siri”，如图 2 所示；并通过语音合成技术，合成的语音会模仿 iPhone 所有者的音色、音高和发声方法，以绕过声纹识别技术。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icW7mDRGfJmibGkaWjSC1qTs72IL2lgmL0dq9ApwmoOQGFAbficlOyT6LmIkMZttAf8ibVgEWkfGlUZQ/640?wx_fmt=jpeg)

图 2

随后攻击者将合成的语音命令调制到超声波载波上，下面就是幅度调制的原理，如图 3 所示。把正常的频率范围的语音信号（用于语音识别的语音一般是 16KHz 采样，由奈奎斯特率可知其信号的最高频率是 8KHz，这里称为 Baseband 信号），利用幅度调制的方法把 Baseband 信号调制到超声范围，该超声信号称为载波（Carrier）。这么做主要目的是把命令信号调制到被攻击的用户无法听到的超声波范围。 

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icW7mDRGfJmibGkaWjSC1qTsWf2iaLI132GkBuAgVpE5qIFLce5nricsFMMZAx1TeIs8sicOGeaXGuhCQ/640?wx_fmt=jpeg)

图 3

将三星手机 S6 和放大器制成一个简易便携式超声波信号发生器，如图 4 所示。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icW7mDRGfJmibGkaWjSC1qTsZMibiba4FuW1zW5iaLk7ICCicgytjSoqY3ibnH0tyT1uEfysSka1XyOL7Ww/640?wx_fmt=jpeg)

图 4

利用该装置便可以将超声波信号发送给 iPhone，成功唤醒黑屏状态下的 iPhone 和 apple watch。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icW7mDRGfJmibGkaWjSC1qTsLwrnMHnaGQVaGD0QzNicfib4xnk3bF50ok2uEUqZcImd5b6xBMGpSHiag/640?wx_fmt=jpeg)

图 5

语音控制系统分为两个部分：激活和识别，在激活阶段，系统不能识别任意的语音输入，预先定义好的唤醒词或按特殊键。例如苹果 Siri 可以通过按下和保持主页按钮大约一秒钟或 “Hey,Siri” 激活，但是系统只接受同一个人即 iPhone 所有者的“Hey Siri”。一旦激活，语音控制系统进入识别阶段。

在识别阶段，语音控制系统识别可识别任意一种语音，不仅限于 iPhone 所有者，攻击者即可通过 TTS 技术合成自己需要的系统可识别命令来完成攻击，拨打任意电话、发短信、视频通话以及将手机切换到飞行模式等。

**三、攻击行为分析与解决方案**
-----------------

产生 “海豚音攻击” 的原因主要包括硬件和软件两方面。麦克风可以识别 20kHz 以上的声音是硬件本身的漏洞，其次现行的语音识别系统无法对语音进行有效的鉴别，声纹识别技术形同虚设。

在模拟攻击中，我们发现声音嘈杂的环境和长距离传输会对 “海豚音攻击” 产生较大影响，如图 5 和图 6 所示，噪声越大的环境，“海豚音攻击”被识别率越低；距离越远，“海豚音攻击”被识别率越低。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icW7mDRGfJmibGkaWjSC1qTsJBW12cxyGnpoNmmAVtlQaJpGfOnKicJxtwrkhGcsaYicAfohu7b9fNiaQ/640?wx_fmt=jpeg)

图 6

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icW7mDRGfJmibGkaWjSC1qTsQ6gErm5TkYNyRWBOu4iahIYWO5icm63wbMF2dPWVYXg8ia0kEdLuZu77w/640?wx_fmt=jpeg)

图 7

目前，有专家认为，抑制 “海豚音攻击” 有两种方法。一是让语音助手只听取特定人（手机拥有者）的语音，这需要在语音助手上运用声纹识别技术。对此，浙江大学徐文渊说，声纹识别技术是利用每个人的音域、音高、发声方法的差别对发声者身份进行辨识。实验表明，“海豚音攻击”只是攻击麦克风，并不改变每个人的声音，因此，“海豚音攻击”可以绕过声纹识别技术。

二是在语音助手软件中增加数字滤波功能，徐文渊表示，滤波是将高于人耳范围的信号过滤掉以后再进行识别。“海豚音攻击” 攻击的是硬件漏洞，麦克风在录音过程已经把语音提取下来，此时，滤波已经无法发挥作用。

应对措施包括软件和硬件解决方案。其中硬件解决方案是最终的解决办法，需要麦克风生产商针对性地改良硬件设计，让麦克风不再能获取高频率的声音。

### 1、硬件解决方案：

a） 再增加一个低通滤波器，进一步减少高频成分的泄露。

b） 采用抗混叠更好的 ADC，进行更严格的抗混叠测试。

c） 采用更高的采样频率，比如采样率是 16K 的话，16~24K 的信号就能混叠进来。如果采样率是 48Khz 的话，要 24Khz 以上的信号才有可能混叠进来。实际上 24Khz 信号要发射和采集都要困难很多。

d） 采用动态的采样频率，让攻击者无法及时调整。

从硬件解决方案上可以看出来需要对整体硬件进行重新的设计开发，难度相对较大，且周期长，对于存量用户无法保证绝对安全。

### 2、其次可行性较高的是软件方案，便于应急处理相关攻击：

a）用户应关闭语音激活功能，减少语音助手的权限。

b）软件开发者应改良语音识别系统，优化**声纹识别**技术，只识别语音频率在 20Hz-20kHz 之间的、不识别超声波信号，使其更好的识别使用者的声音。

c）必要情况下，使用屏蔽设备屏蔽高频信号。

**针对上述攻击产生原因，实例中采取关闭 iPhone“Hey,Siri” 功能的措施，“海豚音攻击” 的超声波无法唤醒此类 iPhone 和 apple watch。**

**四、攻击总结及物联网安全**
----------------

“海豚音攻击” 除了可以在苹果的 Siri 实现，对其他语音识别系统也可以完成攻击，包括谷歌的 Google Assistant、亚马逊的 Alexa、三星的 SVoice、微软的 Cortana 和联想 ThinkPad T440p，华为的 HiVoice、甚至是操纵奥迪 Q3 汽车上的导航系统等，如下图 8 所示。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3icW7mDRGfJmibGkaWjSC1qTsW4ZIeU3bdeY62JpZ0Ik7XtthImTiaJwNMxibpMxib0F4icxMJibIadtaDibQ/640?wx_fmt=jpeg)

图 8

以上仅是针对移动智能设备上语音识别系统的分析，现今智能语音系统已经在工业系统，门禁系统，车联网和物联网等中广泛使用。攻击者无需依靠大型信号发生设备即可进行攻击，我们需要对语音识别系统进行改良，加强对语音身份者的鉴权分析（4A），限制语音识别系统的非法操作。

起于安全、不止安全。“海豚音攻击” 其实是一种传感器攻击（传感器是把物理量的变化转变成电信号的设备）。

传感器被攻击的另一个例子是乔纳森佩蒂特（2015 年）利用激光来唤醒智能的 LiD AR 传感器，使汽车突然变速或停止。传感器攻击原因是大多数传感器 (IoT) 设备缺乏内在的安全设计机制，不能应对物理攻击。传感器在还没有明确安全风险前就设计出来了。

研究人员发现，攻击者不仅可以引发 DOS 攻击，而且还可以使用恶意的模拟信号控制传感器的输出。漏洞往往存在于模拟传感器的内部。随着物联网 IoT、智能汽车等智能化的发展，传感器的使用、功能和所起的作用也会越来越重要。

传感器作为一个智能化程度和安全系数都不高的攻击入口，相信许多攻击者都会使用不同的办法来攻击传感器，而传感器安全问题也将是物联网发展中的长期不可轻视的一个现实攻击面，相关传感器攻击事件也会越来越多、越来越严重！  

![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR38Tm7G07JF6t0KtSAuSbyWtgFA8ywcatrPPlURJ9sDvFMNwRT0vpKpQ14qrYwN2eibp43uDENdXxgg/640?wx_fmt=gif)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf + 小程序：把安全装进口袋 小程序

  

精彩推荐

  

  

  

  

****![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib2xibAss1xbykgjtgKvut2LUribibnyiaBpicTkS10Asn4m4HgpknoH9icgqE0b0TVSGfGzs0q8sJfWiaFg/640?wx_fmt=jpeg)****

  

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR3ic1YSqMEGaoBvQqUqGqTVW4KwVA6ePJbEc5lPmoicqjfWV2T2BgH6icQDvAhvhqHQvxSl3cjacCulqQ/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486459&idx=1&sn=74658ddb6cd1bfb2d224bc7c3a236015&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ibnOz2Slh3icgLwEyRibxE9Qa7ziag03WLN71NL5icWxBsNPGzNlDEQrNVpjoIRnmglkpJ61iaP7giaBZww/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486404&idx=1&sn=6d434a8d335887fc665287732933091d&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR384iaX6B8n12ebKz8LqibnrDQTyFTVGgeUQ20OH45Z1KqtjzL83XLEjDicq9Sbvd5SeXyUbd7iaWFdmHw/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486350&idx=1&sn=ce56524dc187468146dc23a991b0596a&scene=21#wechat_redirect)

**************![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR3icF8RMnJbsqatMibR6OicVrUDaz0fyxNtBDpPlLfibJZILzHQcwaKkb4ia57xAShIJfQ54HjOG1oPXBew/640?wx_fmt=gif)**************