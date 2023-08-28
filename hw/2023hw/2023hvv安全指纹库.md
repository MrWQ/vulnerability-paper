# OpenEASM指纹清单 

 🔥🔥🔥由安全事件驱动的指纹库，持续更新中。

|    | product             | rule                                                                                                                                  | update_at   |
|---:|:--------------------|:--------------------------------------------------------------------------------------------------------------------------------------|:------------|
|  0 | ThinkPHP            | header:"X-Powered-By: ThinkPHP"                                                                                                       | 2023-08-08  |
|  1 | JBoss-EAP           | header:"JBoss-EAP"                                                                                                                    | 2023-08-08  |
|  2 | HAProxy-WI          | (html:"url=/app/overview.py" AND html:"Redirecting... Please wait" ) OR title:"HAProxy-WI"                                            | 2023-08-08  |
|  3 | 天融信-上网行为管理系统        | title:"Login @ Reporter" || html:"欢迎访问 Reporter"                                                                                      | 2023-08-08  |
|  4 | 网康下一代防火墙            | title:"网康下一代防火墙"                                                                                                                      | 2023-08-08  |
|  5 | 通达OA                | html:"http://www.tongda2000.com"                                                                                                      | 2023-08-08  |
|  6 | 用友NC                | html:"platform/pub/welcome.do"                                                                                                        | 2023-08-08  |
|  7 | 蓝凌OA                | html:"SoftDeleteEnableModules:"                                                                                                       | 2023-08-08  |
|  8 | 禅道                  | header:"zentaosid" OR html:"欢迎使用禅道集成运行环境"                                                                                             | 2023-08-08  |
|  9 | Confluence          | html:"https://support.atlassian.com/help/confluence" || header:"X-Confluence-Request-Time"                                            | 2023-08-08  |
| 10 | 泛微产品                | html:"上海泛微网络科技股份有限公司"                                                                                                                 | 2023-08-08  |
| 11 | Laravel             | header:"laravel_session"                                                                                                              | 2023-08-08  |
| 12 | Hadoop              | html:"It looks like you are making an HTTP request to a Hadoop IPC port" OR html:"/static/hadoop.css" OR html:"./main_files/yarn.css" | 2023-08-08  |
| 13 | Dynamicweb          | header:"Dynamicweb"                                                                                                                   | 2023-08-08  |
| 14 | jackrabbit          | title:"Apache Jackrabbit JCR Server"                                                                                                  | 2023-07-27  |
| 15 | Metabase            | title:"MetaBase"                                                                                                                      | 2023-07-27  |
| 16 | YAPI                | title:"YAPI"                                                                                                                          | 2023-07-17  |
| 17 | HadoopYarn_WebUI    | title:"All Applications" OR title:"JobHistory"                                                                                        | 2023-07-17  |
| 18 | Gitlab              | html:"https://about.gitlab.com"                                                                                                       | 2023-07-17  |
| 19 | NginxWebUI          | title:"NginxWebUI"                                                                                                                    | 2023-07-17  |
| 20 | Openfire_WebUI      | title:"Openfire"                                                                                                                      | 2023-07-17  |
| 21 | RocketMQName_Server | service:"rocketmq" OR banner:"serializeTypeCurrentRPC"                                                                                | 2023-07-14  |
| 22 | C2_DoNot_Team       | html:"This Page is Blocked by Mod Security teeeeddddddddddd"                                                                          | 2023-07-13  |
| 23 | MinioConsole        | title:"MinIO Console" OR title:"Minio Browser"                                                                                        | 2023-07-12  |
| 24 | Kibana              | headers:"Kbn-License-Sig"                                                                                                             | 2023-07-12  |
| 25 | 金山终端安全系统            | title:"云堤防病毒"                                                                                                                         | 2023-07-12  |
| 26 | JeecgBoot           | title:"JeecgBoot 企业级低代码平台"                                                                                                            | 2023-07-12  |