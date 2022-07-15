> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qww6xUNtRS4biXVoBvmhRg)

#### **![](https://mmbiz.qpic.cn/mmbiz_jpg/RpxgdDjibJqdjpNzAh6qTBCo4ewU5Cr6fgiaIWlan1ApJL2GadNficI3ajoraCAQZsbSQm468vDUkHk8XklCb2MQw/640?wx_fmt=jpeg)**

#### **通达 OA 信息收集**

```
http[s]://TongDaOA.domain/inc/expired.php 判断通达版本
http[s]://TongDaOA.domain/inc/reg_trial.php
http[s]://TongDaOA.domain/inc/reg_trial_submit.php
http[s]://TongDaOA.domain/ispirit/retrieve_pwd.php
GET 参数username、email 可爆用户、邮箱
http[s]://TongDaOA.domain/resque/worker.php 计算机名
```

```
http[s]://TongDaOA.domain/module/crm2010/imageOperation/deleteImage.php 
http[s]://TongDaOA.domain/module/crm2010/product/type_tree.php 
http[s]://TongDaOA.domain/module/crm2010/select/getData.php 
http[s]://TongDaOA.domain/module/crm2010/select/getValue.php 
http[s]://TongDaOA.domain/module/crm2010/select/index.php 
http[s]://TongDaOA.domain/module/crm2010/share/update.php 
http[s]://TongDaOA.domain/portal/webportals/source/oa/news.php
http[s]://TongDaOA.domain/portal/webportals/source/oa/notify.php?LOGIN_USER_ID=
http[s]://TongDaOA.domain/task/crm/account_care_remind.php
http[s]://TongDaOA.domain/task/crm/action_link_remind.php
http[s]://TongDaOA.domain/task/crm/contract_birthday_remind.php
http[s]://TongDaOA.domain/task/crm/contract_near_remind.php
http[s]://TongDaOA.domain/task/crm/contract_remind.php
http[s]://TongDaOA.domain/task/crm/crm_account_contact_bir_remind.php
http[s]://TongDaOA.domain/task/crm/crm_complain_remind.php
http[s]://TongDaOA.domain/task/crm/crm_opportunity_status_remind.php
http[s]://TongDaOA.domain/task/crm/crm_salepay_remind.php
http[s]://TongDaOA.domain/task/crm/crm_stockout_remind.php
http[s]://TongDaOA.domain/task/crm/marketing_near_remind.php
http[s]://TongDaOA.domain/task/crm/order_to_stockout_remind.php
http[s]://TongDaOA.domain/task/crm/payment_near_remind.php
http[s]://TongDaOA.domain/task/crm/storage_near_remind.php
http[s]://TongDaOA.domain/ispirit/myoa.php
http[s]://TongDaOA.domain/ispirit/retrieve_pwd.php
```

#### **2013-2017(SQLi path)**

```
http[s]://TongDaOA.domain/general/approve_center/list/roll_config.inc.php
http[s]://TongDaOA.domain/general/bi_design/reportshop/report_bi.func.php
http[s]://TongDaOA.domain/general/data_center/console/autocode/autocode.php
http[s]://TongDaOA.domain/general/data_center/model_design/console/autocode/autocode.php
http[s]://TongDaOA.domain/general/data_center/model_design/design/report/action.php
http[s]://TongDaOA.domain/general/reportshop/design/report/action.php
http[s]://TongDaOA.domain/general/project/portal/details/budget/table.php
http[s]://TongDaOA.domain/general/reportshop/design/report/console/autocode/autocode.php
http[s]://TongDaOA.domain/general/reportshop/workshop/report/attachment-remark/form3.php
http[s]://TongDaOA.domain/general/system/user/get_key_user_info.php
http[s]://TongDaOA.domain/general/workflow/list/roll_config.inc.php
http[s]://TongDaOA.domain/interface/GetNewAPP.php
http[s]://TongDaOA.domain/interface/GetNewAPP1.php
http[s]://TongDaOA.domain/general/workflow/plugin/turn/kd_k3_applly/kd_k3_applly.php
http[s]://TongDaOA.domain/general/workflow/document_list/roll_config.inc.php
```

```
http[s]://TongDaOA.domain/module/appbuilder/assets/print.php 任意文件删除
```

#### **v11~v11.6 [0day]**

```
http[s]://TongDaOA.domain/general/approve_center/list/roll_config.inc.php
http[s]://TongDaOA.domain/general/bi_design/reportshop/report_bi.func.php
http[s]://TongDaOA.domain/general/data_center/console/autocode/autocode.php
http[s]://TongDaOA.domain/general/data_center/model_design/console/autocode/autocode.php
http[s]://TongDaOA.domain/general/data_center/model_design/design/report/action.php
http[s]://TongDaOA.domain/general/reportshop/design/report/action.php
http[s]://TongDaOA.domain/general/project/portal/details/budget/table.php
http[s]://TongDaOA.domain/general/reportshop/design/report/console/autocode/autocode.php
http[s]://TongDaOA.domain/general/reportshop/workshop/report/attachment-remark/form3.php
http[s]://TongDaOA.domain/general/system/user/get_key_user_info.php
http[s]://TongDaOA.domain/general/workflow/list/roll_config.inc.php
http[s]://TongDaOA.domain/interface/GetNewAPP.php
http[s]://TongDaOA.domain/interface/GetNewAPP1.php
http[s]://TongDaOA.domain/general/workflow/plugin/turn/kd_k3_applly/kd_k3_applly.php
http[s]://TongDaOA.domain/general/workflow/document_list/roll_config.inc.php
```

#### **v11.6 [RCE]**

```
http[s]://TongDaOA.domain/module/appbuilder/assets/print.php 任意文件删除
```

#### **参考文章**

**通达 OA 漏洞一些漏洞点 (Github)**