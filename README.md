# awvsbatch
awvs批量添加扫描

## 使用
先修改scanner/awvs.py中self.host和api_key

awvs自行安装，如果有docker的话可以直接用docker安装

```buildoutcfg
docker pull secfa/docker-awvs
docker run -it -d -p 13443:3443 secfa/docker-awvs
```

安装依赖
```buildoutcfg
python3 -m pip install -r requirements.txt
```
启动服务
```buildoutcfg
python3 manage.py runserver
```

1. 访问http://127.0.0.1:5000/awvs/scan
2. 上传批量域名excel，必须是xlsx格式，单次最好在50个以内

上传完之后，如果成功开始扫描会返回类似如下信息
```buildoutcfg
{"count":10,"success":[{"domain":"http://www.testphp.com","targetid":"97e39f12-0d28-4bae-825c-ce779fda4237"},{"domain":"http://www.testasp.com","incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"97e39f12-0d28-4bae-825c-ce779fda4237","targetid":"175cc68c-e2c9-4cea-ae09-f8c222ce1e32","ui_session_id":null},{"domain":"http://www.testasp.com","incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"97e39f12-0d28-4bae-825c-ce779fda4237","targetid":"175cc68c-e2c9-4cea-ae09-f8c222ce1e32","ui_session_id":null},{"domain":"http://www.testjsp.com","incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"175cc68c-e2c9-4cea-ae09-f8c222ce1e32","targetid":"baadf3f2-96d9-4d81-be33-00db553572e1","ui_session_id":null},{"domain":"http://www.testjsp.com","incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"175cc68c-e2c9-4cea-ae09-f8c222ce1e32","targetid":"baadf3f2-96d9-4d81-be33-00db553572e1","ui_session_id":null},{"domain":"http://www.hacker101.com","incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"baadf3f2-96d9-4d81-be33-00db553572e1","targetid":"ac2cff0c-23ea-448d-a5e3-9c32c5ef43b9","ui_session_id":null},{"domain":"http://www.hacker101.com","incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"baadf3f2-96d9-4d81-be33-00db553572e1","targetid":"ac2cff0c-23ea-448d-a5e3-9c32c5ef43b9","ui_session_id":null},{"domain":"http://www.baidu.com","incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"ac2cff0c-23ea-448d-a5e3-9c32c5ef43b9","targetid":"1d72a9de-4165-4c78-8e63-7e1f197a951f","ui_session_id":null},{"domain":"http://www.baidu.com","incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"ac2cff0c-23ea-448d-a5e3-9c32c5ef43b9","targetid":"1d72a9de-4165-4c78-8e63-7e1f197a951f","ui_session_id":null},{"incremental":false,"max_scan_time":0,"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false,"triggerable":false},"target_id":"1d72a9de-4165-4c78-8e63-7e1f197a951f","ui_session_id":null}]}
```