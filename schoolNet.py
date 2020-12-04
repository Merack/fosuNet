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
import socket


def encrypt(e, m, message):
    """
    RSA加密函数
    :param e:
    :param m:
    :param message:
    :return:
    """
    en = Encrypt(e, m)
    return en.encrypt(message)


def getEncPassword(password):
    """
    获取加密后的密码
    :param password: 用户密码
    :return: 加密后的密码
    """
    doc = pq(url=cfg.serviceIndexURl, encoding='utf-8')
    keyStr = doc('#publicKey').attr('value')
    split = keyStr.split('&')
    publicKeyExponent = split[0]
    publicKeyModulus = split[1]
    # 此处传入的密码需要进行翻转, 因为网页的js中翻转了, 所以这里也要照做 -_-
    passwordEnc = encrypt(publicKeyExponent, publicKeyModulus, ''.join(reversed(password)))
    return passwordEnc


def getLocalIP():
    """
    返回本机ip
    :return: 本机ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.connect(('8.8.8.8',80))
        s.connect(('223.5.5.5', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    if len(ip) == 0:
        return -1
    else:
        return ip


def serviceLogin(studentID, password):
    """
    登陆校园网自助服务系统
    :param studentID: 学号
    :param password: 密码
    :return: cookie
    """
    data = {"from": "rsa", "name": studentID, "password": getEncPassword(password)}
    res = requests.post(cfg.serviceLoginURL, data=data, headers=cfg.header)
    if "errorMsg" in res.text:
        return -1
    cookie = res.cookies
    return cookie


def getDeviceList(cookie):
    """
    获取在线设备
    :param cookie: 登陆cookie
    :return: 在线设备列表
    """
    # 获取在线设备列表
    res = requests.get(cfg.deviceURl, headers=cfg.header, cookies=cookie)
    devices = []
    doc = pq(res.text)('#a1').parent().parent()
    if len(list(doc.items())) == 0:
        return -1
    for i in doc.items():
        d = {"id": i('label').attr('id'), "name": i('label').text(), "ip": i('#a1').text().split(':')[-1].strip()}
        devices.append(d)
    return devices


def showDevices(devices, cookie=None):
    """
    show 所有设备
    :param devices: 设备列表
    :param cookie: 登陆cookie, 可选
    :return: null
    """
    if cookie:
        devices = getDeviceList(cookie)
    if devices == -1:
        print("当前没有在线设备")
    else:
        for i, device in enumerate(devices):
            print("id: " + str(i), " 设备名称: " + device["name"], "  ip: " + device["ip"])


def offline(studentID, cookie, offlineAll=False, offlineLocal=False):
    """
    下线功能函数
    :param studentID: 学号
    :param cookie: 登陆cookie
    :param offlineAll: 是否下线所有设备
    :param offlineLocal: 是否下线本机
    :return:
    """
    # 下线功能
    devices = getDeviceList(cookie)
    if len(devices) == 0:
        return "当前没有设备在线"

    if offlineAll:
        if getDeviceList(cookie) != -1:
            for device in devices:
                data = {
                    "key": studentID + ':' + device["ip"]
                }
                res = requests.post(cfg.offlineURL, headers=cfg.header, cookies=cookie, data=data)
            if getDeviceList(cookie) == -1:
                return "下线所有设备成功"
            else:
                return -1

    elif offlineLocal:
        if getDeviceList(cookie) == -1:
            return "当前没有设备在线"
        else:
            ip = getLocalIP()
            data = {
                "key": studentID + ':' + ip
            }
            res = requests.post(cfg.offlineURL, headers=cfg.header, cookies=cookie, data=data)
            if res.ok:
                return "下线 本机 成功"
            else:
                return "下线设备失败"
    else:
        showDevices(devices)
        choice = input("输入设备id(按q取消操作): ")
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


def login(studentID, password, service):
    """
    校园网登陆函数
    :param studentID: 学号
    :param password: 密码
    :param service: 运营商名称
    :return: 0:登陆成功 , 1: 已经登录了, -1: 登陆失败, -2: 获取不到页面
    """
    res = requests.get(cfg.baseLoginURL, headers=cfg.header)
    queryString = re.search(r"index\.jsp\?(.*?)'<", res.text)
    if queryString is not None:
        queryString = queryString.group(1)
    elif "success.jsp" in res.url:
        # 用户已经登录校园网
        return 1, "您已经登录了校园网"
    else:
        # 获取页面不正确. 可能没有连接到校园网
        return -2, "获取页面不正确. 您可能没有连接到校园网"

        # return res.text
    data = {
        "userId": studentID,
        "password": getEncPassword(password),
        "passwordEncrypt": "true",
        "service": parse.quote(service),
        "queryString": queryString
    }
    res = requests.post(cfg.loginToURL, headers=cfg.header, data=data)
    res.encoding = 'utf-8'
    res = res.json()
    if res["result"] == "fail":
        # 登陆失败
        return -1, res["message"]
    else:
        # 登陆成功
        return 0, "登陆成功"
