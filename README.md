# redmine_statis

## 1、redmine表说明
表issues —用来存放issue的标准字段。

表custom_fields —该表字段都和创建自定义字段的web页面看到的选择项很像。

表custom_values—该表可以用custom_field_id字段和custom_fields表的id关联。 而customized_id 可以和issues表的id相关联

因此三个表issues, custom_fields和custom_values在一起表达了这么个关系。

一个issue的标准字段来自issues表，扩展字段来自custom_fields表，而custom_values和前custom_fields表关联，一起表示一个issue的某个自定义字段的值。

并且，当表示issue的自定义字段时，custom_fields.type的值是 'IssueCustomField' 而custom_values.customized_type的值是'Issue'.

所有issue的自定义字段值  
因此可以先将custom_fields表和custom_values表关联，获得如下结果：  
select customized_id as issue_id,custom_field_id,type,name,default_value,value from custom_fields a inner join custom_values b on a.id =b.custom_field_id and a.type = 'IssueCustomField' and b.customized_type='Issue' limit 2;

由此可以看出redmine的设计是用记录行数来表示扩展字段的值，所以可以不受mysql表字段的限制。

## 2、访问权限
基本知识了解：
grant select,excute on bitnami_redmine.* to 'redmine_static'@'200.200.169.162' identified by 'moatest';  
——授予  
select user,host,password from mysql.user;   
flush privileges;  
show grants for 'redmine_static'@'200.200.169.162'\G  
revoke select on bitnami_redmine.* from 'redmine_static'@'200.200.169.162' identified by 'moatest';  
grant all privileges on bitnami_redmine.* to 'redmine_static'@'200.200.169.162' identified by 'moatest';  
drop user redmine_static@'%';  
create user redmine_static@'%' identified by 'moatest'; 

## 3、redmine口袋助理项目统计说明
项目地址：200.200.169.162  
在redmine服务器中新增一个mysql用户：redmine_static/moatest  
——该用户只能在169.162中以用户名和密码的方式访问  
——见如上2说明

## 使用
切换到项目路径  
执行：python main.py [统计开始时间 统计结束时间]  
eg：python main.py 2016-9-1 2016-12-31




