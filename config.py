#!/usr/bin/env python
# _*_ coding:utf-8 _*_

# @Author: Merack
# @Email: merack@qq.com


baseLoginURL = 'http://10.10.9.4'
loginToURL = 'http://10.10.9.4/eportal/InterFace.do?method=login'
serviceLoginURL = 'http://10.10.9.2:8080/selfservice/module/scgroup/web/login_judge.jsf'
serviceIndexURl = 'http://10.10.9.2:8080/selfservice/module/scgroup/web/login_self.jsf'
deviceURl = 'http://10.10.9.2:8080/selfservice/module/webcontent/web/onlinedevice_list.jsf'
offlineURL = 'http://10.10.9.2:8080/selfservice/module/userself/web/userself_ajax.jsf?methodName=indexBean.kickUserBySelfForAjax'

header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9.0; MI 8 SE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.119 Mobile Safari/537.36"
}

config_path = './config/'
config_name = 'config.ini'
dev_config_name = 'config.dev.ini'

debug = False
