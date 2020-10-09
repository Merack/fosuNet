#!/usr/bin/env python
# _*_ coding:utf-8 _*_

# @Author: Merack
# @Email: merack@qq.com

import requests
from pyquery import PyQuery as pq
from urllib import parse
import re
import config as cfg
from Encrypt import Encrypt


def encrypt(e, m, message):
    en = Encrypt(e, m)
    return en.encrypt(message)


def getEncPassword(password):
    doc = pq(url=cfg.serviceIndexURl, encoding='utf-8')
    keyStr = doc('#publicKey').attr('value')
    split = keyStr.split('&')
    publicKeyExponent = split[0]
    publicKeyModulus = split[1]
    # 此处传入的密码需要进行翻转, 因为网页的js中翻转了, 所以这里也要照做 -_-
    passwordEnc = encrypt(publicKeyExponent, publicKeyModulus, ''.join(reversed(password)))
    return passwordEnc


def serviceLogin(studentID, password):
    data = {"from": "rsa", "name": studentID, "password": getEncPassword(password)}
    res = requests.post(cfg.serviceLoginURL, data=data, headers=cfg.header)
    cookie = res.cookies
    return cookie


def getDeviceList(cookie):
    # 获取在线设备列表
    res = requests.get(cfg.deviceURl, headers=cfg.header, cookies=cookie)
    devices = []
    doc = pq(res.text)('#a1').parent().parent()
    if len(list(doc.items())) == 0:
        return "当前没有在线设备"
    for i in doc.items():
        d = {"id": i('label').attr('id'), "name": i('label').text(), "ip": i('#a1').text().split(':')[-1].strip()}
        devices.append(d)
    return devices


def showDevices(devices, cookie=None):
    if cookie:
        devices = getDeviceList(cookie)

    for i, device in enumerate(devices):
        print("id: " + str(i), " 设备名称: " + device["name"])


def offline(studentID, cookie, offlineAll=False):
    # 下线功能
    devices = getDeviceList(cookie)
    # print("origin len: " + str(len(devices)))
    if not offlineAll:
        showDevices(devices)
        choice = input("输入设备id(按q返回): ")
        if choice == 'q':
            return -1
        try:
            ip = devices[int(choice)]["ip"]
            name = devices[int(choice)]["name"]
        except Exception as e:
            print("请输入正确的值: ")
            return offline(studentID, cookie, offlineAll)
        else:
            data = {
                "key": studentID + ':' + ip
            }
            res = requests.post(cfg.offlineURL, headers=cfg.header, cookies=cookie, data=data)
            # print("secLen: " + str(len(devices)))
            # print("len " + str(len(getDeviceList(cookie))))
            if res.ok:
                return "下线 " + name + " 成功"
            else:
                return "下线设备失败"
    else:
        for device in devices:
            data = {
                "key": studentID + ':' + device["ip"]
            }
            res = requests.post(cfg.offlineURL, headers=cfg.header, cookies=cookie, data=data)
        if len(getDeviceList(cookie)) == 0:
            return "下线所有设备成功"
        else:
            return -1


def login(studentID, password, service):
    res = requests.get(cfg.baseLoginURL, headers=cfg.header)
    queryString = re.search(r"index\.jsp\?(.*?)'<", res.text)
    if queryString is not None:
        queryString = queryString.group(1)
    else:
        return "获取页面不正确.您或许已经登录或者未连接校园网"
        # return res.text
    data = {
        "userId": studentID,
        "password": getEncPassword(password),
        "passwordEncrypt": "true",
        "service": parse.quote(service),
        "queryString": queryString
    }
    res = requests.post(cfg.loginToURL, headers=cfg.header, data=data)
    return "登陆成功"
